---
name: design-system
description: "Guided, section-by-section GDD authoring for a single game system. Gathers context from existing docs, walks through each required section collaboratively, cross-references dependencies, and writes incrementally to file."
argument-hint: "<system-name> [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion, TodoWrite
model: sonnet
---

When this skill is invoked:

## 1. Parse Arguments & Validate

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `.claude/docs/director-gates.md` for the full check pattern.

A system name or retrofit path is **required**. If missing:

1. Check if `design/gdd/systems-index.md` exists.
2. If it exists: read it, find the highest-priority system with status "Not Started" or equivalent, and use `AskUserQuestion`:
   - Prompt: "The next system in your design order is **[system-name]** ([priority] | [layer]). Start designing it?"
   - Options: `[A] Yes — design [system-name]` / `[B] Pick a different system` / `[C] Stop here`
   - If [A]: proceed with that system name. If [B]: ask which system to design (plain text). If [C]: exit.
3. If no systems index exists, fail with:
   > "Usage: `/design-system <system-name>` — e.g., `/design-system movement`
   > Or to fill gaps in an existing GDD: `/design-system retrofit design/gdd/[system-name].md`
   > No systems index found. Run `/map-systems` first to map your systems and get the design order."

**Detect retrofit mode:**
If the argument starts with `retrofit` or the argument is a file path to an
existing `.md` file in `design/gdd/`, enter **retrofit mode**:

1. Read the existing GDD file.
2. Identify which of the 8 required sections are present (scan for section headings).
   Required sections: Overview, Player Fantasy, Detailed Design/Rules, Formulas,
   Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria.
3. Identify which sections contain only placeholder text (`[To be designed]` or
   equivalent — blank, a single line, or obviously incomplete).
4. Present to the user before doing anything:
   ```
   ## Retrofit: [System Name]
   File: design/gdd/[filename].md

   Sections already written (will not be touched):
   ✓ [section name]
   ✓ [section name]

   Missing or incomplete sections (will be authored):
   ✗ [section name] — missing
   ✗ [section name] — placeholder only
   ```
5. Ask: "Shall I fill the [N] missing sections? I will not modify any existing content."
6. If yes: proceed to **Phase 2 (Gather Context)** as normal, but in **Phase 3**
   skip creating the skeleton (file already exists) and in **Phase 4** skip
   sections that are already complete. Only run the section cycle for missing/
   incomplete sections.
7. **Never overwrite existing section content.** Use Edit tool to replace only
   `[To be designed]` placeholders or empty section bodies.

If NOT in retrofit mode, normalize the system name to kebab-case for the
filename (e.g., "combat system" becomes `combat-system`).

---

## 2. Gather Context (Read Phase)

Read all relevant context **before** asking the user anything. This is the skill's
primary advantage over ad-hoc design — it arrives informed.

### 2a: Required Reads

- **Game concept**: Read `design/gdd/game-concept.md` — fail if missing:
  > "No game concept found. Run `/brainstorm` first."
- **Systems index**: Read `design/gdd/systems-index.md` — fail if missing:
  > "No systems index found. Run `/map-systems` first to map your systems."
- **Target system**: Find the system in the index. If not listed, warn:
  > "[system-name] is not in the systems index. Would you like to add it, or
  > design it as an off-index system?"
- **Entity registry**: Read `design/registry/entities.yaml` if it exists.
  Extract all entries referenced by or relevant to this system (grep
  `referenced_by.*[system-name]` and `source.*[system-name]`). Hold these
  in context as **known facts** — values that other GDDs have already
  established and this GDD must not contradict.
- **Reflexion log**: Read `docs/consistency-failures.md` if it exists.
  Extract entries whose Domain matches this system's category. These are
  recurring conflict patterns — present them under "Past failure patterns"
  in the Phase 2d context summary so the user knows where mistakes have
  occurred before in this domain.

### 2b: Dependency Reads

From the systems index, identify:
- **Upstream dependencies**: Systems this one depends on. Read their GDDs if they
  exist (these contain decisions this system must respect).
- **Downstream dependents**: Systems that depend on this one. Read their GDDs if
  they exist (these contain expectations this system must satisfy).

For each dependency GDD that exists, extract and hold in context:
- Key interfaces (what data flows between the systems)
- Formulas that reference this system's outputs
- Edge cases that assume this system's behavior
- Tuning knobs that feed into this system

### 2c: Optional Reads

- **Game pillars**: Read `design/gdd/game-pillars.md` if it exists
- **Existing GDD**: Read `design/gdd/[system-name].md` if it exists (resume, don't
  restart from scratch)
- **Related GDDs**: Glob `design/gdd/*.md` and read any that are thematically related
  (e.g., if designing a system that overlaps with another in scope, read the related GDD
  even if it's not a formal dependency)

### 2d: Present Context Summary

Before starting design work, present a brief summary to the user:

> **Designing: [System Name]**
> - Priority: [from index] | Layer: [from index]
> - Depends on: [list, noting which have GDDs vs. undesigned]
> - Depended on by: [list, noting which have GDDs vs. undesigned]
> - Existing decisions to respect: [key constraints from dependency GDDs]
> - Pillar alignment: [which pillar(s) this system primarily serves]
> - **Known cross-system facts (from registry):**
>   - [entity_name]: [attribute]=[value], [attribute]=[value] (owned by [source GDD])
>   - [item_name]: [attribute]=[value], [attribute]=[value] (owned by [source GDD])
>   - [formula_name]: variables=[list], output=[min–max] (owned by [source GDD])
>   - [constant_name]: [value] [unit] (owned by [source GDD])
>   *(These values are locked — if this GDD needs different values, surface
>   the conflict before writing. Do not silently use different numbers.)*
>
> If no registry entries are relevant: omit the "Known cross-system facts" section.

If any upstream dependencies are undesigned, warn:
> "[dependency] doesn't have a GDD yet. We'll need to make assumptions about
> its interface. Consider designing it first, or we can define the expected
> contract and flag it as provisional."

### 2e: Technical Feasibility Pre-Check

Before asking the user to begin designing, load runtime/stack context and surface any
constraints or knowledge gaps that will shape the design.

**Step 1 — Determine the runtime/stack domain for this system:**
Map the system's category (from systems-index.md) to a runtime/stack domain:

| System Category | Runtime/Stack Domain |
|----------------|--------------|
| Combat, rules, resolution | Core |
| Economy, loot, market | Persistence |
| API, endpoints, transport | API/Transport |
| Matchmaking, sessions, lobbies | Matchmaking |
| AI, pathfinding, bots | Concurrency |
| Realtime sync, replication | Networking |
| Auth, sessions, tokens | Auth |
| Save/load, persistence, data | Persistence |
| Caching, hot state | Caching |

**Step 2 — Read runtime/stack context (if available):**
- Read `.claude/docs/technical-preferences.md` to identify the runtime/stack and versions
- If a runtime/stack is configured, read `docs/engine-reference/nodejs/VERSION.md`
- Read `docs/engine-reference/nodejs/modules/[domain].md` if it exists
- Read `docs/engine-reference/nodejs/breaking-changes.md` for domain-relevant entries
- Glob `docs/architecture/adr-*.md` and read any ADRs whose domain matches
  (check the Runtime/Stack Compatibility table's "Domain" field)

**Step 3 — Present the Feasibility Brief:**

If runtime/stack reference docs exist, present before starting design:

```
## Technical Feasibility Brief: [System Name]
Runtime: Node.js [version] + [libraries]
Domain: [domain]

### Known Runtime/Library Capabilities (verified for [version])
- [capability relevant to this system]
- [capability 2]

### Runtime/Library Constraints That Will Shape This Design
- [constraint from runtime/stack reference or existing ADR]

### Knowledge Gaps (verify before committing to these)
- [post-cutoff feature this design might rely on — mark HIGH/MEDIUM risk]

### Existing ADRs That Constrain This System
- ADR-XXXX: [decision summary] — means [implication for this GDD]
  (or "None yet")
```

If no runtime/stack reference docs exist (stack not yet configured), show a short note:
> "No runtime/stack configured yet — skipping technical feasibility check. Run
> `/setup-engine` before moving to architecture if you haven't already."

**Step 4 — Ask before proceeding:**

Use `AskUserQuestion`:
- "Any constraints to add before we begin, or shall we proceed with these noted?"
  - Options: "Proceed with these noted", "Add a constraint first", "I need to check the runtime/stack docs — pause here"

---

Use `AskUserQuestion`:
- "Ready to start designing [system-name]?"
  - Options: "Yes, let's go", "Show me more context first", "Design a dependency first"

---

## 3. Create File Skeleton

Once the user confirms, **immediately** create the GDD file with empty section
headers. This ensures incremental writes have a target.

Use the template structure from `.claude/docs/templates/game-design-document.md`:

```markdown
# [System Name]

> **Status**: In Design
> **Author**: [user + agents]
> **Last Updated**: [today's date]
> **Implements Pillar**: [from context]

## Overview

[To be designed]

## Player Fantasy

[To be designed]

## Detailed Design

### Core Rules

[To be designed]

### States and Transitions

[To be designed]

### Interactions with Other Systems

[To be designed]

## Formulas

[To be designed]

## Edge Cases

[To be designed]

## Dependencies

[To be designed]

## Tuning Knobs

[To be designed]

## Operational Requirements

[To be designed]

## API/Contract Requirements

[To be designed]

## Acceptance Criteria

[To be designed]

## Open Questions

[To be designed]
```

Ask: "May I create the skeleton file at `design/gdd/[system-name].md`?"

If the user declines: Stop with the following message:
> "Verdict: **BLOCKED** — skeleton creation declined. The design session cannot proceed without the skeleton file, as all subsequent phases use it as the base. Re-run `/design-system [system]` when ready to create the file."
Do not proceed to Section A.

After writing, update `production/session-state/active.md`:
- Use Glob to check if the file exists.
- If it **does not exist**: use the **Write** tool to create it. Never attempt Edit on a file that may not exist.
- If it **already exists**: use the **Edit** tool to update the relevant fields.

File content:
- Task: Designing [system-name] GDD
- Current section: Starting (skeleton created)
- File: design/gdd/[system-name].md

---

## 4. Section-by-Section Design

Walk through each section in order. For **each section**, follow this cycle:

### The Section Cycle

```
Context  ->  Questions  ->  Options  ->  Decision  ->  Draft  ->  Approval  ->  Write
```

1. **Context**: State what this section needs to contain, and surface any relevant
   decisions from dependency GDDs that constrain it.

2. **Questions**: Ask clarifying questions specific to this section. Use
   `AskUserQuestion` for constrained questions, conversational text for open-ended
   exploration.

3. **Options**: Where the section involves design choices (not just documentation),
   present 2-4 approaches with pros/cons. Explain reasoning in conversation text,
   then use `AskUserQuestion` to capture the decision.

4. **Decision**: User picks an approach or provides custom direction.

5. **Draft**: Write the section content in conversation text for review. Flag any
   provisional assumptions about undesigned dependencies.

6. **Approval**: Immediately after the draft — in the SAME response — use
   `AskUserQuestion`. **NEVER use plain text. NEVER skip this step.**
   - Prompt: "Approve the [Section Name] section?"
   - Options: `[A] Approve — write it to file` / `[B] Make changes — describe what to fix` / `[C] Start over`

   **The draft and the approval widget MUST appear together in one response.
   If the draft appears without the widget, the user is left at a blank prompt
   with no path forward — this is a protocol violation.**

7. **Write**: Use the Edit tool to replace the placeholder with the approved content.
   **CRITICAL**: Always include the section heading in the `old_string` to ensure
   uniqueness — never match `[To be designed]` alone, as multiple sections use the
   same placeholder and the Edit tool requires a unique match. Use this pattern:
   ```
   old_string: "## [Section Name]\n\n[To be designed]"
   new_string: "## [Section Name]\n\n[approved content]"
   ```
   Confirm the write.

8. **Registry conflict check** (Sections C and D only — Detailed Design and Formulas):
   After writing, scan the section content for entity names, item names, formula
   names, and numeric constants that appear in the registry. For each match:
   - Compare the value just written against the registry entry.
   - If they differ: **surface the conflict immediately** before starting the next
     section. Do not continue silently.
     > "Registry conflict: [name] is registered in [source GDD] as [registry_value].
     > This section just wrote [new_value]. Which is correct?"
   - If new (not in registry): flag it as a candidate for registry registration
     (will be handled in Phase 5).

After writing each section, update `production/session-state/active.md` with the
completed section name. Use Glob to check if the file exists — use Write to create
it if absent, Edit to update it if present.

### Section-Specific Guidance

Each section has unique design considerations and may benefit from specialist agents:

---

### Section A: Overview

**Goal**: One paragraph a stranger could read and understand.

**Derive recommended options before building the widget**: Read the system's category and layer from the systems index (already in context from Phase 2), then determine the recommended option for each tab:
- **Framing tab**: Foundation/Infrastructure layer → `[A]` recommended. Player-facing categories (Combat, UI, Dialogue, Character, Animation, Visual Effects, Audio) → `[C] Both` recommended.
- **ADR ref tab**: Glob `docs/architecture/adr-*.md` and grep for the system name in the GDD Requirements section of any ADR. If a matching ADR is found → `[A] Yes — cite the ADR` recommended. If none found → `[B] No` recommended.
- **Fantasy tab**: Foundation/Infrastructure layer → `[B] No` recommended. All other categories → `[A] Yes` recommended.

Append `(Recommended)` to the appropriate option text in each tab.

**Framing questions (ask BEFORE drafting)**: Use `AskUserQuestion` with a multi-tab widget:
- Tab "Framing" — "How should the overview frame this system?" Options: `[A] As a data/infrastructure layer (technical framing)` / `[B] Through its player-facing effect (design framing)` / `[C] Both — describe the data layer and its player impact`
- Tab "ADR ref" — "Should the overview reference the existing ADR for this system?" Options: `[A] Yes — cite the ADR for implementation details` / `[B] No — keep the GDD at pure design level`
- Tab "Fantasy" — "Does this system have a player fantasy worth stating?" Options: `[A] Yes — players feel it directly` / `[B] No — pure infrastructure, players feel what it enables`

Use the user's answers to shape the draft. Do NOT answer these questions yourself and auto-draft.

**Questions to ask**:
- What is this system in one sentence?
- How does a player interact with it? (active/passive/automatic)
- Why does this system exist — what would the game lose without it?

**Cross-reference**: Check that the description aligns with how the systems index
describes it. Flag discrepancies.

**Design vs. implementation boundary**: Overview questions must stay at the behavior
level — what the system *does*, not *how it is built*. If implementation questions
arise during the Overview (e.g., "Should this use an Autoload singleton or a signal
bus?"), note them as "→ becomes an ADR" and move on. Implementation patterns belong
in `/architecture-decision`, not the GDD. The GDD describes behavior; the ADR
describes the technical approach used to achieve it.

---

### Section B: Player Fantasy

**Goal**: The emotional target — what the player should *feel*.

**Derive recommended option before building the widget**: Read the system's category and layer from Phase 2 context:
- Player-facing categories (Combat, UI, Dialogue, Character, Animation, Audio, Level/World) → `[A] Direct` recommended
- Foundation/Infrastructure layer → `[B] Indirect` recommended
- Mixed categories (Camera/input, Economy, AI with visible player effects) → `[C] Both` recommended

Append `(Recommended)` to the appropriate option text.

**Framing question (ask BEFORE drafting)**: Use `AskUserQuestion`:
- Prompt: "Is this system something the player engages with directly, or infrastructure they experience indirectly?"
- Options: `[A] Direct — player actively uses or feels this system` / `[B] Indirect — player experiences the effects, not the system` / `[C] Both — has a direct interaction layer and infrastructure beneath it`

Use the answer to frame the Player Fantasy section appropriately. Do NOT assume the answer.

**Questions to ask**:
- What emotion or power fantasy does this serve?
- What reference games nail this feeling? What specifically creates it?
- Is this a "system you love engaging with" or "infrastructure you don't notice"?

**Cross-reference**: Must align with the game pillars. If the system serves a pillar,
quote the relevant pillar text.

**Review mode check** (apply before spawning):
- `solo` → skip this agent spawn. Draft the section without the specialist. Add a note: "`game-designer` not consulted — Solo mode. Review manually before production."
- `lean` → skip unless this is a section with HIGH implementation risk (Sections D and H only). For other sections, draft without the agent.
- `full` → spawn as described below.

**Agent delegation (MANDATORY)**: After the framing answer is given but before drafting,
spawn `game-designer` via Task:
- Provide: system name, framing answer (direct/indirect/both), game pillars, any reference games the user mentioned, the game concept summary
- Ask: "Shape the Player Fantasy for this system. What emotion or power fantasy should it serve? What player moment should we anchor to? What tone and language fits the game's established feeling? Be specific — give me 2-3 candidate framings."
- Collect the game-designer's framings and present them to the user alongside the draft.

**Do NOT draft Section B without first consulting `game-designer`.** The framing
answer tells us *what kind* of fantasy it is; the game-designer shapes *how it's
described* — tone, language, the specific player moment to anchor to.

---

### Section C: Detailed Design (Core Rules, States, Interactions)

**Goal**: Unambiguous specification a programmer could implement without questions.

This is usually the largest section. Break it into sub-sections:

1. **Core Rules**: The fundamental mechanics. Use numbered rules for sequential
   processes, bullets for properties.
2. **States and Transitions**: If the system has states, map every state and
   every valid transition. Use a table.
3. **Interactions with Other Systems**: For each dependency (upstream and downstream),
   specify what data flows in, what flows out, and who owns the interface.

**Questions to ask**:
- Walk me through a typical use of this system, step by step
- What are the decision points the player faces?
- What can the player NOT do? (Constraints are as important as capabilities)

**Review mode check** (apply before spawning):
- `solo` → skip this agent spawn. Draft the section without the specialist. Add a note: "Specialist agents not consulted — Solo mode. Review manually before production."
- `lean` → skip unless this is a section with HIGH implementation risk (Sections D and H only). For other sections, draft without the agent.
- `full` → spawn as described below.

**Agent delegation (MANDATORY)**: Before drafting Section C, spawn specialist agents via Task in parallel:
- Look up the system category in the routing table (Section 6 of this skill)
- Spawn the Primary Agent AND Supporting Agent(s) listed for this category
- Provide each agent: system name, game concept summary, pillar set, dependency GDD excerpts, the specific section being worked on
- Collect their findings before drafting
- Surface any disagreements between agents to the user via `AskUserQuestion`
- Draft only after receiving specialist input

**Do NOT draft Section C without first consulting the appropriate specialists.** A `game-designer` reviewing rules and mechanics will catch design gaps the main session cannot.

**Cross-reference**: For each interaction listed, verify it matches what the
dependency GDD specifies. If a dependency defines a value or formula and this
system expects something different, flag the conflict.

---

### Section D: Formulas

**Goal**: Every mathematical formula, with variables defined, ranges specified,
and edge cases noted.

**Completion Steering — always begin each formula with this exact structure:**

```
The [formula_name] formula is defined as:

`[formula_name] = [expression]`

**Variables:**
| Variable | Symbol | Type | Range | Description |
|----------|--------|------|-------|-------------|
| [name] | [sym] | float/int | [min–max] | [what it represents] |

**Output Range:** [min] to [max] under normal play; [behaviour at extremes]
**Example:** [worked example with real numbers]
```

Do NOT write `[Formula TBD]` or describe a formula in prose without the variable
table. A formula without defined variables cannot be implemented without guesswork.

**Questions to ask**:
- What are the core calculations this system performs?
- Should scaling be linear, logarithmic, or stepped?
- What should the output ranges be at early/mid/late game?

**Review mode check** (apply before spawning):
- `solo` → skip this agent spawn. Draft the section without the specialist. Add a note: "`game-designer` not consulted — Solo mode. Review manually before production."
- `lean` → skip unless this is a section with HIGH implementation risk (Sections D and H only). For other sections, draft without the agent.
- `full` → spawn as described below.

**Agent delegation (MANDATORY)**: Before proposing any formulas or balance values, spawn specialist agents via Task in parallel:
- **Always spawn `game-designer`**: provide Core Rules from Section C, tuning goals from user, balance context from dependency GDDs. Ask them to propose formulas with variable tables and output ranges.
- **For economy/cost systems, also spawn `game-designer`**: provide placement costs, upgrade cost intent, and progression goals. Ask them to validate cost curves and ratios.
- Present the specialists' proposals to the user for review via `AskUserQuestion`
- The user decides; the main session writes to file
- **Do NOT invent formula values or balance numbers without specialist input.** A user without balance design expertise cannot evaluate raw numbers — they need the specialists' reasoning.

**Cross-reference**: If a dependency GDD defines a formula whose output feeds into
this system, reference it explicitly. Don't reinvent — connect.

---

### Section E: Edge Cases

**Goal**: Explicitly handle unusual situations so they don't become bugs.

**Completion Steering — format each edge case as:**
- **If [condition]**: [exact outcome]. [rationale if non-obvious]

Example (adapt terminology to the game's domain):
- **If [resource] reaches 0 while [protective condition] is active**: hold at minimum until condition ends, then apply consequence.
- **If two [triggers/events] fire simultaneously**: resolve in [defined priority order]; ties use [defined tiebreak rule].

Do NOT write vague entries like "handle appropriately" — each must name the exact
condition and the exact resolution. An edge case without a resolution is an open
design question, not a specification.

**Questions to ask**:
- What happens at zero? At maximum? At out-of-range values?
- What happens when two rules apply at the same time?
- What happens if a player finds an unintended interaction? (Identify degenerate strategies)

**Review mode check** (apply before spawning):
- `solo` → skip this agent spawn. Draft the section without the specialist. Add a note: "`game-designer` not consulted — Solo mode. Review manually before production."
- `lean` → skip unless this is a section with HIGH implementation risk (Sections D and H only). For other sections, draft without the agent.
- `full` → spawn as described below.

**Agent delegation (MANDATORY)**: Spawn `game-designer` via Task before finalising edge cases. Provide: the completed Sections C and D, and ask them to identify edge cases from the formula and rule space that the main session may have missed. Present their findings and ask the user which to include.

**Cross-reference**: Check edge cases against dependency GDDs. If a dependency
defines a floor, cap, or resolution rule that this system could violate, flag it.

---

### Section F: Dependencies

**Goal**: Map every system connection with direction and nature.

This section is partially pre-filled from the context gathering phase. Present the
known dependencies from the systems index and ask:
- Are there dependencies I'm missing?
- For each dependency, what's the specific data interface?
- Which dependencies are hard (system cannot function without it) vs. soft
  (enhanced by it but works without it)?

**Cross-reference**: This section must be bidirectionally consistent. If this system
lists "depends on Combat", then the Combat GDD should list "depended on by [this
system]". Flag any one-directional dependencies for correction.

---

### Section G: Tuning Knobs

**Goal**: Every designer-adjustable value, with safe ranges and extreme behaviors.

**Questions to ask**:
- What values should designers be able to tweak without code changes?
- For each knob, what breaks if it's set too high? Too low?
- Which knobs interact with each other? (Changing A makes B irrelevant)

**Agent delegation**: If formulas are complex, delegate to `game-designer`
to derive tuning knobs from the formula variables.

**Cross-reference**: If a dependency GDD lists tuning knobs that affect this system,
reference them here. Don't create duplicate knobs — point to the source of truth.

---

### Section H: Acceptance Criteria

**Goal**: Testable conditions that prove the system works as designed.

**Completion Steering — format each criterion as Given-When-Then:**
- **GIVEN** [initial state], **WHEN** [action or trigger], **THEN** [measurable outcome]

Example (adapt terminology to the game's domain):
- **GIVEN** [initial state], **WHEN** [player action or system trigger], **THEN** [specific measurable outcome].
- **GIVEN** [a constraint is active], **WHEN** [player attempts an action], **THEN** [feedback shown and action result].

Include at least: one criterion per core rule from Section C, and one per formula
from Section D. Do NOT write "the system works as designed" — every criterion must
be independently verifiable by a QA tester without reading the GDD.

**Review mode check** (apply before spawning):
- `solo` → skip this agent spawn. Draft the section without the specialist. Add a note: "`qa-tester` not consulted — Solo mode. Review manually before production."
- `lean` → skip unless this is a section with HIGH implementation risk (Sections D and H only). For other sections, draft without the agent.
- `full` → spawn as described below.

**Agent delegation (MANDATORY)**: Spawn `qa-tester` via Task before finalising acceptance criteria. Provide: the completed GDD sections C, D, E, and ask them to validate that the criteria are independently testable and cover all core rules and formulas. Surface any gaps or untestable criteria to the user.

**Questions to ask**:
- What's the minimum set of tests that prove this works?
- What performance budget does this system get? (tick time, request latency, memory)
- What would a QA tester check first?

**Cross-reference**: Include criteria that verify cross-system interactions work,
not just this system in isolation.

---

### Optional Sections: Operational, API/Contract Requirements, Open Questions

These sections are included in the template. Operational Requirements are **REQUIRED** for player-facing and stateful service categories — not optional. Determine the requirement level before asking:

**Operational Requirements are REQUIRED (mandatory — do not offer to skip) for these system categories:**
- Combat, damage, health resolution
- API / endpoint systems
- Matchmaking, sessions, lobbies
- Realtime sync, replication
- Economy, loot, market
- Persistence, save/load, data
- Auth, sessions, security

For required systems: **spawn `devops-engineer` via Task** before drafting this section. Provide: system name, game concept, game pillars, existing ADRs if they exist. Ask them to specify: (1) observability and metric requirements for this system's events, (2) any scaling, rate-limit, or availability constraints, (3) which operational principles most directly apply to this system. Present their output; do NOT leave this section as `[To be designed]` for these systems.

For **all other system categories** (pure formula/tuning systems, internal AI heuristics), offer the optional sections after the required sections:

Use `AskUserQuestion`:
- "The 8 required sections are complete. Do you want to also define Operational
  requirements, API/Contract requirements, or capture open questions?"
  - Options: "Yes, all three", "Just open questions", "Skip — I'll add these later"

For **Operational Requirements** (non-required systems): Coordinate with `devops-engineer` and `nodejs-specialist` if detail is needed. Often a brief note suffices at the GDD stage.

For **API/Contract Requirements**: Coordinate with `api-specialist` for systems exposing a request/response surface.
After writing this section, check whether it contains real content (not just
`[To be designed]` or a note that this system has no external API). If it does have real
API requirements, output this flag immediately:

> **📌 API Flag — [System Name]**: This system exposes a request/response surface. In Phase 4
> (Pre-Production), have `api-specialist` define the endpoint/contract spec for each route
> this system contributes **before** writing epics. Stories that reference the API should
> cite the contract spec, not the GDD directly.
>
> Note this in the systems index for this system if you update it.

For **Open Questions**: Capture anything that came up during design that wasn't
fully resolved. Each question should have an owner and target resolution date.

---

## 5. Post-Design Validation

After all sections are written:

### 5a: Self-Check

Read back the complete GDD from file (not from conversation memory — the file is
the source of truth). Verify:
- All 8 required sections have real content (not placeholders)
- Formulas reference defined variables
- Edge cases have resolutions
- Dependencies are listed with interfaces
- Acceptance criteria are testable

### 5a-bis: Game Designer Pillar Review

**Review mode check** — apply before spawning GD-GDD-ALIGN:
- `solo` → skip. Note: "GD-GDD-ALIGN skipped — Solo mode." Proceed to Step 5b.
- `lean` → skip (not a PHASE-GATE). Note: "GD-GDD-ALIGN skipped — Lean mode." Proceed to Step 5b.
- `full` → spawn as normal.

Before finalizing the GDD, spawn `game-designer` via Task using gate **GD-GDD-ALIGN** (`.claude/docs/director-gates.md`).

Pass: completed GDD file path, game pillars (from `design/gdd/game-concept.md` or `design/gdd/game-pillars.md`), MDA aesthetics target.

Handle verdict per the standard rules in `director-gates.md`. After resolution, record the verdict in the GDD Status header:
`> **Game Designer Review (GD-GDD-ALIGN)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

---

### 5b: Update Entity Registry

Scan the completed GDD for cross-system facts that should be registered:
- Named entities (enemies, NPCs, bosses) with stats or drops
- Named items with values, weights, or categories
- Named formulas with defined variables and output ranges
- Named constants referenced by value in more than one place

For each candidate, check if it already exists in `design/registry/entities.yaml`:
```
Grep pattern="  - name: [candidate_name]" path="design/registry/entities.yaml"
```

Present a summary:
```
Registry candidates from this GDD:
  NEW (not yet registered):
    - [entity_name] [entity]: [attribute]=[value], [attribute]=[value]
    - [item_name] [item]: [attribute]=[value], [attribute]=[value]
    - [formula_name] [formula]: variables=[list], output=[min–max]
  ALREADY REGISTERED (referenced_by will be updated):
    - [constant_name] [constant]: value=[N] ← matches registry ✅
```

Ask: "May I update `design/registry/entities.yaml` with these [N] new entries
and update `referenced_by` for the existing entries?"

If yes: append new entries and update `referenced_by` arrays. Never modify
existing `value` / attribute fields without surfacing it as a conflict first.

### 5c: Offer Design Review

Present a completion summary:

> **GDD Complete: [System Name]**
> - Sections written: [list]
> - Provisional assumptions: [list any assumptions about undesigned dependencies]
> - Cross-system conflicts found: [list or "none"]

> **To validate this GDD, open a fresh Claude Code session and run:**
> `/design-review design/gdd/[system-name].md`
>
> **Never run `/design-review` in the same session as `/design-system`.** The reviewing
> agent must be independent of the authoring context. Running it here would inherit
> the full design history, making independent critique impossible.

**NEVER offer to run `/design-review` inline.** Always direct the user to a fresh window.

### 5d: Update Systems Index

After the GDD is complete (and optionally reviewed):

- Read the systems index
- Update the target system's row:
  - If design-review was run and verdict is APPROVED: Status → "Approved"
  - If design-review was run and verdict is NEEDS REVISION: Status → "In Review"
  - If design-review was skipped: Status → "Designed" (pending review)
  - If the user chose "I'll review it myself first": Status → "Designed"
  - Design Doc: link to `design/gdd/[system-name].md`
- Update the Progress Tracker counts

Ask: "May I update the systems index at `design/gdd/systems-index.md`?"

### 5e: Update Session State

Update `production/session-state/active.md` with:
- Task: [system-name] GDD
- Status: Complete (or In Review if design-review was run)
- File: design/gdd/[system-name].md
- Sections: All 8 written
- Next: [suggest next system from design order]

### 5f: Suggest Next Steps

Use `AskUserQuestion`:
- "What's next?"
  - Options:
    - "Run `/consistency-check` — verify this GDD's values don't conflict with existing GDDs (recommended before designing the next system)"
    - "Design next system ([next-in-order])" — if undesigned systems remain
    - "Fix review findings" — if design-review flagged issues
    - "Stop here for this session"
    - "Run `/gate-check`" — if enough MVP systems are designed

---

## 6. Specialist Agent Routing

This skill delegates to specialist agents for domain expertise. The main session
orchestrates the overall flow; agents provide expert content.

| System Category | Primary Agent | Supporting Agent(s) |
|----------------|---------------|---------------------|
| **Foundation/Infrastructure** (event bus, config/resource loading, service bootstrap, lifecycle) | `game-designer` | `gameplay-programmer` (feasibility), `nodejs-specialist` (runtime integration) |
| Combat, damage, health resolution | `game-designer` | `game-designer` (formulas), `gameplay-programmer` (server AI), `gameplay-programmer` (authoritative logic) |
| Economy, loot, crafting | `game-designer` | `game-designer` (curves), `game-designer` (loops) |
| Progression, XP, skills | `game-designer` | `game-designer` (curves), `game-designer` (sinks) |
| Persistence, save/load, data | `game-designer` | `database-specialist` (schema, transactions), `nodejs-specialist` (state ownership) |
| API / endpoint systems | `game-designer` | `api-specialist` (contracts, validation), `game-designer` (rules behind the endpoint) |
| Matchmaking, sessions, lobbies | `game-designer` | `api-specialist` (session flow), `api-specialist` (transport), `gameplay-programmer` (matchmaking heuristics) |
| AI, pathfinding, behavior | `game-designer` | `gameplay-programmer` (implementation), `game-designer` (scoring) |
| Realtime sync, replication | `game-designer` | `api-specialist` (replication), `api-specialist` (tick loop, interest management), `game-designer` (state) |
| Auth, sessions, security | `game-designer` | `api-specialist` (session/auth flow), `security-engineer` (threat model), `database-specialist` (token storage) |
| Caching, hot state | `game-designer` | `database-specialist` (Redis, eviction), `nodejs-specialist` (hit-rate budgets) |
| Character systems (stats, archetypes) | `game-designer` | `game-designer` (stat formulas), `game-designer` (progression alignment) |

**When delegating via Task tool**:
- Provide: system name, game concept summary, dependency GDD excerpts, the specific
  section being worked on, and what question needs expert input
- The agent returns analysis/proposals to the main session
- The main session presents the agent's output to the user via `AskUserQuestion`
- The user decides; the main session writes to file
- Agents do NOT write to files directly — the main session owns all file writes

---

## 7. Recovery & Resume

If the session is interrupted (compaction, crash, new session):

1. Read `production/session-state/active.md` — it records the current system and
   which sections are complete
2. Read `design/gdd/[system-name].md` — sections with real content are done;
   sections with `[To be designed]` still need work
3. Resume from the next incomplete section — no need to re-discuss completed ones

This is why incremental writing matters: every approved section survives any
disruption.

---

## Collaborative Protocol

This skill follows the collaborative design principle at every step:

1. **Question -> Options -> Decision -> Draft -> Approval** for every section
2. **AskUserQuestion** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Ready to start, or need more context?"
   - Phase 3: "May I create the skeleton?"
   - Phase 4 (each section): Design questions, approach options, draft approval
   - Phase 5: "Run design review? Update systems index? What's next?"
3. **"May I write to [filepath]?"** before the skeleton and before each section write
4. **Incremental writing**: Each section is written to file immediately after approval
5. **Session state updates**: After every section write
6. **Cross-referencing**: Every section checks existing GDDs for conflicts
7. **Specialist routing**: Complex sections get expert agent input, presented to
   the user for decision — never written silently

**Never** auto-generate the full GDD and present it as a fait accompli.
**Never** write a section without user approval.
**Never** contradict an existing approved GDD without flagging the conflict.
**Always** show where decisions come from (dependency GDDs, pillars, user choices).

## Context Window Awareness

This is a long-running skill. After writing each section, check if the status line
shows context at or above 70%. If so, append this notice to the response:

> **Context is approaching the limit (≥70%).** Your progress is saved — all approved
> sections are written to `design/gdd/[system-name].md`. When you're ready to continue,
> open a fresh Claude Code session and run `/design-system [system-name]` — it will
> detect which sections are complete and resume from the next one.

---

## Recommended Next Steps

- Run `/design-review design/gdd/[system-name].md` in a **fresh session** to validate the completed GDD independently
- Run `/consistency-check` to verify this GDD's values don't conflict with other GDDs
- Run `/map-systems next` to move to the next highest-priority undesigned system
- Run `/gate-check pre-production` when all MVP GDDs are authored and reviewed
