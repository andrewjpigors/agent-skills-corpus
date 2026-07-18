---
name: genshin-agent-persona
description: |
  Selects a female Genshin Impact character as the persona for a new agent, AI service, or standalone tool. Maps the agent's responsibility (orchestrator, healer, scout, knowledge core, security enforcer, lifecycle manager, etc.) to the strongest character match using lore role, personality, element, and weapon. Use when naming a new agent in a multi-agent platform, picking a codename for a service, choosing a persona for a tool, or building a persona library. Triggers: name an agent, agent name, agent codename, persona library, character name, tool codename, genshin persona, pick a persona, name a tool, name a service.
license: MIT
metadata:
  version: 1.0.0
---

# Genshin Agent Persona

Pick a Genshin Impact character as the named persona for an agent or tool, based on what the agent _does_, not just what it looks like.

## Quick Start

Four steps:

1. **Identify the agent's primary responsibility** in one sentence ("schedules background jobs", "validates auth tokens", "summarizes long docs").
2. **Match it to an archetype** from the table below — pick the most specific fit.
3. **Pick the top-ranked character**, or scan the next candidates if the top pick is taken or doesn't fit secondary attributes.
4. **Emit a structured persona record** (YAML) so it can drop into a persona library.

Deeper detail lives in [references/archetypes.md](references/archetypes.md), [references/roster.md](references/roster.md), and [references/special-cases.md](references/special-cases.md).

## When to Use This Skill

- Naming a new agent in a multi-agent platform (orchestrator, worker, supervisor, etc.).
- Choosing a codename for a standalone service or CLI tool.
- Building a persona library for an agent platform like Noelle.
- Refactoring an existing agent system and wanting consistent thematic naming.

## Selection Workflow

### Step 1: Describe the agent's job

Write one sentence on the agent's _primary_ responsibility. Resist the urge to list every secondary capability — pick the most specific job.

Good: "Garbage-collects orphaned database rows nightly."
Bad: "Does cleanup, also some monitoring, also writes reports."

### Step 2: Match to archetype

Use the table below. If two archetypes feel equally close, pick the one that maps to the riskiest or most user-visible part of the agent's job. The candidates are ranked — the leftmost is the strongest match for that archetype.

| Archetype | Top picks (in order) |
|---|---|
| Orchestrator / leader | Mavuika → Jean → Arlecchino → Ningguang |
| Knowledge core / RAG | Nahida → Lisa → Nicole → Faruzan |
| Forecaster / oracle | Mona → Citlali → Columbina → Linnea |
| Security / enforcement | Clorinde → Candace → Rosaria → Kujou Sara |
| Observability / logging | Charlotte → Yelan → Fischl → Lynette |
| Healer / healthcheck | Sigewinne → Barbara → Yaoyao → Mizuki |
| Cleanup / GC / lifecycle | Noelle → Hu Tao → Emilie → Qiqi |
| Tooling / builder / inventor | Xianyun → Xilonen → Aino → Sandrone |
| Pipeline / ETL / formatter | Xiangling → Yun Jin → Furina → Yoimiya |
| Compliance / arbitration | Yanfei → Furina → Keqing → Raiden Shogun |
| Scout / connector / courier | Mualani → Chasca → Amber → Kirara |
| Apprentice / supervised | Collei → Kachina |
| Mentor / senior consultant | Skirk |
| Burst / batch worker | Varesa → Eula |
| Chaos / fuzz testing | Klee |
| Automaton / Swiss-army | Ineffa → Sandrone |
| Procurement / vendor broker | Dori |
| Legacy / deprecated memorial | La Signora |
| External / collab integration | Aloy |

Need rationale on _why_ each character fits an archetype? See [references/archetypes.md](references/archetypes.md).

### Step 3: Confirm secondary fit

Before locking in the top pick, sanity-check it against:

- **Element + weapon vibes** — Hydro/Dendro pairings imply growth and reaction; Cryo implies freeze/delay; Pyro implies destructive bursts. Match if it adds flavor; ignore if it doesn't.
- **Already-used persona** — if the agent system already has a Sigewinne handling healthchecks, don't pick her again. Move to Barbara or Yaoyao.
- **Human vs non-human UX** — chatbots presenting as people should pick fully human personas. Overtly-AI agents can lean into kitsune/automaton/melusine flavor.

### Step 4: Emit the persona record

Always produce a YAML block, ready to paste into a persona library:

```yaml
name: Sigewinne
epithet: Head Nurse, Fortress of Meropide
pronouns: she/her
non_human: melusine
element: Hydro
weapon: Bow
region: Fontaine
agent_archetype: Healer
agent_responsibilities:
  - 24/7 liveness probe
  - triage and diagnostics
  - rate-limited tranquilizer (cooldown enforcement)
  - mood-board for service health dashboards
rationale: >
  Always-on infirmary maps directly to a 24/7 healthcheck SLO.
  Tranquilizer-arrows match controlled cooldown / rate limiting.
```

## Pronoun Policy

Every character on this list uses **she/her** pronouns. There is no canonically non-binary playable character through patch 6.6 (May 20, 2026). The one nuance: **Arlecchino** holds the in-universe role title "Father" but uses she/her pronouns canonically. Store the title as role-language metadata, not as gender:

```yaml
name: Arlecchino
pronouns: she/her
in_universe_role_title: Father
```

The Rust class name can be `ParentSupervisor` or `HouseMaster` to evoke the title without misgendering her. See [references/special-cases.md](references/special-cases.md) for full nuance.

## Tagging Non-Human Personas

Some characters aren't fully human. Flag them so consumers can filter "human-presenting" vs. "non-human" agents:

- **adeptus** — Xianyun (Cloud Retainer), Ganyu (half-qilin), Shenhe (adeptal-trained)
- **kitsune** — Yae Miko
- **nekomata** — Kirara
- **melusine** — Sigewinne
- **archon** — Nahida, Mavuika, Furina, Raiden Shogun (Ei)
- **youkai** — Mizuki (yumekui-baku)
- **angel** — Nicole
- **automaton** — Ineffa, Sandrone
- **abyss-dweller** — Skirk
- **half-xiezhi** — Yanfei
- **fae** — Linnea (Snowland Fae)

If a tool's UX implies a human contact, prefer a fully human persona. If the agent is overtly an AI/automaton, the non-human tags can be a feature.

## Output Format

Always emit two things:

1. **A one-line headline** — `Sigewinne, Head Nurse of Meropide` followed by a one-sentence rationale.
2. **The structured persona record** — the YAML block above, ready to paste into a persona library.

Don't over-explain the lore. One sentence of rationale is enough; deeper background lives in the references.

## Anti-Patterns

**Don't pick by aesthetic alone.** Hu Tao is fun, but if the agent isn't doing lifecycle/decommission work, she's the wrong pick. Match responsibility first, vibe second.

**Don't reuse one persona across many agents.** If the platform already has a Noelle (cleanup), don't also call the GC daemon Noelle. Use Hu Tao or Emilie as the next-best fit.

**Don't ignore the deprecated tier.** La Signora is a memorial archetype — useful for documenting a legacy system that consumed itself, but don't apply her to a healthy new service.

**Don't hide pronouns.** If a tool's docs use a persona, the docs should use her pronouns naturally. Arlecchino is she/her even when her class name evokes "Father."

## Writing Style

The one-line rationale and any free-form notes in the persona record follow the `natural-writing-style` skill — apply its rules to every prose line you emit.

Domain-specific guidance on top of that:

- Use contractions ("don't", "she's", "it's") and address the reader as "you" if you address them at all.
- Keep the rationale concrete: cite the specific lore hook ("always-on infirmary", "Lightfall Sword charges then explodes") rather than vague flavor ("matches the agent's vibe").
- Don't claim a persona is "perfect" or that it makes the agent "production ready" — just describe why the lore matches the responsibility.

If the rationale spans more than one sentence, run it past `natural-writing-style` before emitting it.

## Source

Persona data derived from research through patch 6.6 "Luna VII" (May 20, 2026). Spans Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, Natlan, Nod-Krai, Fatui Harbingers, plus special cases (Skirk, Aloy). 76 characters total.
