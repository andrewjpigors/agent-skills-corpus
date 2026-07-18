---
name: art-bible
description: "Guided, evidence-backed Art Bible authoring. Creates or updates the visual identity source of truth that gates asset production, prompt generation, UI style, character/environment art, VFX direction, and later art-review checks. Run after /brainstorm is approved and before /map-systems or GDD authoring begins."
argument-hint: "[full|style|characters|environments|ui] [--review full|lean|solo] [--dry-run]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

# Art Bible Authoring Skill

## Skill Name

art-bible

## Mission

Create or update the project’s visual identity source of truth in a way that is specific, evidence-backed, reviewable, accessible, technically feasible, and useful for downstream production.

The art bible must gate:

- concept art,
- asset production,
- prompt generation,
- UI visual style,
- character art,
- environment art,
- material language,
- lighting direction,
- VFX direction,
- art review,
- technical-art planning,
- accessibility/readability checks.

The art bible must not merely describe “vibes.” It must define visual rules that a human artist, technical artist, UI implementer, asset-spec generator, or image-prompt system can follow and be reviewed against.

The core question is:

> Does this visual direction clearly state what the game should look like, what it must not look like, why those choices support the project, and how downstream assets will be judged?

---

## Operating Principles

1. **Evidence before invention**
   - Derive art direction from approved concept, pillars, brainstorm output, UX, GDD, architecture constraints, and existing production assets.
   - If evidence is missing, mark the gap. Do not invent project-defining art direction without approval.

2. **Facts, inferences, and recommendations are separate**
   - A fact comes from a repository source.
   - An inference is a reasoned conclusion from multiple sources.
   - A recommendation is a proposed art-direction choice requiring approval if it becomes canonical.

3. **Production-ready specificity**
   - Every visual rule must be concrete enough to guide asset creation and review.
   - Avoid vague terms unless paired with visual constraints, examples, anti-examples, or production rules.

4. **Negative rules are mandatory**
   - Define what is off-style.
   - Off-style prevention is as important as style description.

5. **Readability and accessibility are visual requirements**
   - Palette, contrast, silhouettes, VFX, UI, lighting, and camera readability must support gameplay and accessibility.
   - Visual beauty must not undermine playability.

6. **Technical feasibility matters**
   - Art direction must respect engine, platform, performance, rendering, memory, UI, and asset-pipeline constraints.
   - When feasibility is uncertain, flag it for Technical Artist / Technical Director review.

7. **Historical preservation**
   - Preserve prior art decisions unless superseded explicitly.
   - Prefer additive notes over destructive rewrites.

8. **Protected writes stay protected**
   - Routine writes are limited to declared outputs.
   - Existing file replacement, canonical document edits outside declared outputs, status changes, release readiness, sprint state, gates, or registry changes require explicit approval.

9. **Dry-run never writes**
   - In `--dry-run`, perform discovery, generate proposed artifacts, and validate the proposal, but do not call `Write` or `Edit`.

10. **Subagents are bounded reviewers**
    - Use subagents only when they materially improve confidence.
    - Pass bounded context and ask for specific verdicts.
    - Do not spawn duplicate reviewers.

11. **Self-healing before completion**
    - If sources are missing, contradictory, draft-only, inaccessible, or insufficient, classify the problem, narrow scope, use safe assumptions, or stop.

12. **Bounded self-learning**
    - Lessons from art bible reviews, asset drift, accessibility findings, technical-art findings, and user corrections may be stored only in approved, reviewable locations.
    - Lessons must be explicit, reversible, and subordinate to Creative Director / Art Director decisions and current user instructions.

---

## Supported Modes

The first positional argument may specify scope:

```text
full
style
characters
environments
ui
```

If no mode is provided, default to:

```text
full
```

unless the user request clearly implies a narrower scope.

### Mode Definitions

| Mode | Scope | Canonical Output Impact |
|---|---|---|
| `full` | Complete visual identity across all sections. | May create/update all three canonical outputs. |
| `style` | Visual pillars, rendering language, palette, materials, lighting, negative rules. | Primarily `art-bible.md` and `style-guide.md`. |
| `characters` | Character shape language, anatomy/stylization, costume, silhouette, readability, factions/species if relevant. | `art-bible.md`, `style-guide.md`, index entries for character assets. |
| `environments` | World look, biome rules, lighting, palette, material language, landmarks, environmental storytelling. | `art-bible.md`, `style-guide.md`, index entries for environment assets. |
| `ui` | HUD/menu visual language, typography, spacing, iconography, accessibility, VFX/audio-visual feedback interface. | `style-guide.md`, `art-bible.md`, UI entries in index. |

---

## Review Modes

Resolve review mode once:

1. Explicit `--review full|lean|solo`.
2. Else read:

```text
production/review-mode.txt
```

3. Else default to:

```text
lean
```

If the file is missing, malformed, or empty, default to `lean` and report the assumption once.

### Review Mode Semantics

| Review Mode | Subagent Review |
|---|---|
| `solo` | No subagents. Skill performs self-check only. |
| `lean` | Essential review only for the requested scope. |
| `full` | Cross-functional review for art direction, UX/accessibility, and technical feasibility. |

### Recommended Review Routing

| Scope | Lean Review | Full Review |
|---|---|---|
| `full` | `art-director` or equivalent visual owner if available | Art Director, UX/accessibility, Technical Artist, optional Creative Director gate |
| `style` | Art Director | Art Director + Technical Artist |
| `characters` | Art Director | Art Director + Narrative/World owner if character lore matters |
| `environments` | Art Director | Art Director + Level Designer/World Builder + Technical Artist |
| `ui` | UX/accessibility or UI visual reviewer | UX Designer + Accessibility Specialist + Art Director + UI Programmer/Technical Artist |

If the relevant subagent does not exist or Task is unavailable, mark review as skipped and do not claim review approval.

---

## Path Safety

All user-supplied paths must be repository-relative.

Reject:

- absolute paths,
- paths containing `..`,
- paths outside expected project roots,
- paths that would write outside declared outputs unless explicitly protected-approved.

Expected project roots:

```text
design/
docs/
production/
assets/
```

Declared routine output paths:

```text
design/art/art-bible.md
design/art/style-guide.md
design/art/asset-direction-index.md
```

If path is invalid, stop with:

```text
Path rejected: [reason]
```

---

## Write Policy

### Routine Writes Allowed By Invocation

If not in dry-run, routine writes may create missing files:

```text
design/art/art-bible.md
design/art/style-guide.md
design/art/asset-direction-index.md
```

Routine writes may also apply safe additive updates to those files if the existing structure supports it and no content is overwritten.

### Protected Operations Requiring AskUserQuestion

Require explicit confirmation before:

- overwriting an existing file,
- deleting a file,
- replacing a canonical source-of-truth document,
- editing canonical source-of-truth documents outside declared outputs,
- changing statuses,
- changing gates,
- changing stage files,
- changing sprint state,
- changing story state,
- changing release readiness,
- changing registries,
- running commands that modify files,
- installing dependencies,
- generating builds,
- publishing artifacts,
- deploying,
- tagging,
- committing,
- pushing,
- broadening scope beyond the requested mode.

### Write Matrix

| Operation | Routine? | Approval Required? |
|---|---:|---:|
| Create missing `design/art/art-bible.md` | Yes | No |
| Create missing `design/art/style-guide.md` | Yes | No |
| Create missing `design/art/asset-direction-index.md` | Yes | No |
| Add clearly scoped section to existing declared output | Yes, if non-destructive | No |
| Replace existing declared output | No | Yes |
| Edit concept/GDD/UX/architecture docs | No | Yes |
| Update stage/status/gate/story/release files | No | Yes |
| Delete/archive existing art docs | No | Yes |
| Write in dry-run | No | Not allowed |

---

## Missing-File Behavior

| Situation | Behavior |
|---|---|
| Primary concept source missing | Continue only if user supplied a visual brief or enough approved design sources exist for a narrower scope. Otherwise stop. |
| Required output directory missing | Create `design/art/` if writing is routine and not dry-run. |
| Existing target file present | Do not overwrite. Additive update only if safe, otherwise ask. |
| Referenced artifact missing | Record as gap/blocker. Do not invent details. |
| Ambiguous scope | Choose smallest evidence-backed scope unless multiple scopes are equally plausible. |
| Contradictory sources | Prefer explicit source-of-truth/status docs over generated reports. List contradiction. |
| Draft-only source | Use as provisional evidence only. Do not make it canonical without approval. |

---

## Source of Truth Hierarchy

When sources conflict, use this priority:

1. Current user instruction.
2. Approved Creative Director / Art Director decisions.
3. Approved brainstorm / concept document.
4. Art bible / style guide existing canonical content.
5. Design pillars / vision docs.
6. GDDs and UX specs.
7. Architecture/performance constraints.
8. Production asset manifests and shipped/approved assets.
9. Generated reports and drafts.
10. Working assumptions.

If conflict affects identity, style, scope, readability, or production feasibility, mark it as an open decision or blocker.

---

## Discovery Sources

Start with indexes, manifests, registries, and status files.

Primary sources:

```text
design/concept/game-concept.md
design/pillars.md
design/art/
design/gdd/**/*.md
design/ux/**/*.md
docs/architecture/**
production/assets/**
production/session-state/active.md
```

Optional sources if relevant:

```text
design/narrative/**
design/registry/**
docs/engine-reference/**
production/qa/accessibility/**
production/qa/art/**
```

### Discovery Rules

1. Prefer canonical source-of-truth files over generated reports.
2. Use `Glob` and `Grep` before reading large files.
3. Keep a source list for every final artifact.
4. When many files match, read the most relevant 5 to 10 first.
5. Summarize additional candidates as unread or lower-confidence sources.
6. Treat missing or draft-status dependencies as blockers or provisional evidence, not approval to invent.
7. Do not read unrelated large files merely to appear thorough.

---

## Evidence and Confidence Labels

Use these labels for every major visual conclusion:

```text
DIRECT_FACT — explicitly stated in a repository source.
SUPPORTED_INFERENCE — inferred from multiple consistent sources.
WEAK_INFERENCE — inferred from limited or draft evidence.
RECOMMENDATION — proposed by this skill, not yet approved.
OPEN_DECISION — requires user/owner decision.
BLOCKER — prevents safe artifact finalization.
CONTRADICTION — source conflict detected.
```

### Confidence Levels

```text
HIGH — directly sourced or repeatedly supported.
MEDIUM — supported by reasonable inference but not explicit.
LOW — weak evidence; must be framed as provisional.
UNKNOWN — cannot be established from available sources.
```

Never present `RECOMMENDATION`, `WEAK_INFERENCE`, or `OPEN_DECISION` as project fact.

---

## Artifact Lifecycle State Labels

Use these labels for artifacts and sections:

```text
NOT_STARTED
DISCOVERY_COMPLETE
DRAFTED
SOURCE_BACKED
INFERRED
REVIEW_REQUESTED
REVIEWED
APPROVED
PROVISIONAL
BLOCKED
NEEDS_USER_DECISION
NEEDS_ART_DIRECTOR_REVIEW
NEEDS_ACCESSIBILITY_REVIEW
NEEDS_TECHNICAL_ART_REVIEW
NEEDS_PRODUCTION_REVIEW
SUPERSEDED
DEPRECATED
```

### State Rules

- Do not mark a section `APPROVED` unless user/owner approval exists.
- Do not mark a section `SOURCE_BACKED` unless source evidence is named.
- Do not mark review complete if the subagent was skipped or failed.
- Do not mark production-ready if open decisions remain in critical sections.

---

## Build Working Model

Before producing artifacts, generate a concise working model.

```md
## Working Visual Model

- Genre:
- Camera:
- View distance:
- Player readability needs:
- Target platform assumptions:
- Tone:
- Visual fantasy:
- Existing visual evidence:
- Inferred visual direction:
- Accessibility constraints:
- Technical constraints:
- Confidence:
- Open decisions:
```

Derive from repository evidence:

- genre,
- camera,
- tone,
- target platform,
- player readability,
- core fantasy,
- visual pillars,
- silhouette rules,
- color logic,
- material logic,
- lighting language,
- animation feel,
- VFX language,
- UI style,
- accessibility constraints.

If the model is too weak to support the requested mode, stop or narrow scope.

---

## Visual Direction Quality Bar

The output must be:

- specific,
- reviewable,
- asset-production-ready,
- prompt-generation-ready,
- accessible,
- technically plausible,
- negative-rule complete,
- downstream-tool usable.

Bad:

```text
The game should feel dark and magical.
```

Better:

```text
Use low-saturation blue-green shadow palettes with warm amber interactable accents. Magical elements use soft internal glow and fine particle edges, never neon bloom or high-chroma rainbow gradients.
```

Bad:

```text
Characters should look heroic.
```

Better:

```text
Hero silhouettes use upright triangular posture, readable shoulder line, and one dominant asymmetrical prop. Avoid bulky armor shapes that obscure faction identity or weapon readability.
```

---

## Required Output Artifacts

Canonical outputs:

```text
design/art/art-bible.md
design/art/style-guide.md
design/art/asset-direction-index.md
```

### Output Selection By Mode

| Mode | Required Artifact Sections |
|---|---|
| `full` | Complete all canonical artifacts. |
| `style` | Visual pillars, rendering language, palette, lighting, materials, negative rules, style tokens. |
| `characters` | Character shape language, costume/material rules, silhouette tests, character asset directions. |
| `environments` | Environment palette, lighting, materials, props, landmarks, biome/world rules. |
| `ui` | UI visual language, typography, spacing, icons, HUD/menu visual standards, accessibility visual rules. |

---

## Art Bible Required Structure

`design/art/art-bible.md` must use:

```md
# Art Bible

## Document Status

- Status:
- Scope:
- Date:
- Owner:
- Review mode:
- Sources:
- Assumptions:
- Confidence:
- Open decisions:

## 1. Visual Pillars

## 2. Camera and Readability Constraints

## 3. Shape Language

## 4. Palette and Lighting

## 5. Character Direction

## 6. Environment Direction

## 7. UI and VFX Direction

## 8. Material and Rendering Language

## 9. Animation and Motion Feel

## 10. Accessibility and Readability Rules

## 11. Negative Rules / Off-Style Patterns

## 12. Asset Production Rules

## 13. Prompt Generation Rules

## 14. Review Checklist

## 15. Open Decisions

## 16. Sources Consulted
```

### Required Report Sections From Original Skill

At minimum, preserve:

- Visual pillars
- Camera and readability constraints
- Shape language
- Palette and lighting
- Character direction
- Environment direction
- UI/VFX direction
- Asset production rules
- Open decisions

---

## Section Standards

### 1. Visual Pillars

Each visual pillar must be falsifiable.

```md
### Visual Pillar: [Name]

- Player-facing purpose:
- Source evidence:
- Must include:
- Must avoid:
- Applies to:
- Review test:
```

Invalid:

```text
Stylized and immersive.
```

Valid:

```text
Readable silhouettes over surface detail. At gameplay distance, the player must identify faction, threat level, and interactability from silhouette and value grouping before texture detail is visible.
```

---

### 2. Camera and Readability Constraints

Define how camera and gameplay view constrain visual production.

```md
## Camera and Readability Constraints

- Camera type:
- Typical gameplay distance:
- Minimum readable silhouette size:
- Combat/readability priorities:
- UI/HUD readability relationship:
- Environmental landmark needs:
- VFX readability constraints:
- Accessibility constraints:
```

Rules:

- Asset detail must be scaled to camera distance.
- Silhouette and value contrast outrank tiny surface detail.
- VFX must not obscure gameplay-critical information.
- Environments must support navigation and objective readability.

---

### 3. Shape Language

```md
## Shape Language

| Category | Primary Shapes | Meaning | Use Cases | Avoid |
|---|---|---|---|---|
```

Define:

- characters,
- enemies,
- interactables,
- hazards,
- rewards,
- architecture,
- props,
- UI shapes,
- VFX silhouettes.

Rules:

- Shape language must communicate gameplay function.
- Similar gameplay objects should share visual grammar.
- Opposing gameplay meanings should not share confusing silhouettes.

---

### 4. Palette and Lighting

```md
## Palette and Lighting

### Palette Roles

| Role | Color Family | Purpose | Accessibility Risk | Notes |
|---|---|---|---|---|

### Lighting Rules

- Key light:
- Fill:
- Rim/accent:
- Interactive accents:
- Hazard colors:
- Safe/rest colors:
- Narrative/emotional shifts:
```

Rules:

- Do not rely on color alone.
- Define value contrast, not only hue.
- Separate background palette from gameplay-signal colors.
- Define palette shifts by area/state if relevant.
- Include colorblind-safe alternatives or redundant cues.

---

### 5. Character Direction

```md
## Character Direction

### Character Silhouette Rules

### Anatomy / Proportion Rules

### Costume and Gear Rules

### Faction / Role Readability

### Face / Expression Direction

### Animation Pose Language

### Character Negative Rules
```

Each major character category should include:

```md
## Character Visual Rule: [Category]

- Role:
- Silhouette:
- Proportions:
- Costume/materials:
- Palette:
- Readability at distance:
- Variation rules:
- Off-style examples:
```

---

### 6. Environment Direction

```md
## Environment Direction

### World Visual Identity

### Biome / Area Rules

### Landmark Language

### Architecture

### Props

### Materials

### Environmental Storytelling

### Navigation Readability

### Environment Negative Rules
```

Area record:

```md
## Environment Visual Rule: [Area / Biome]

- Mood:
- Palette:
- Lighting:
- Materials:
- Architecture:
- Landmark rules:
- Gameplay readability:
- Narrative cues:
- Off-style patterns:
```

---

### 7. UI and VFX Direction

```md
## UI and VFX Direction

### UI Visual Language

- Layout density:
- Typography:
- Icon style:
- Borders/panels:
- Interaction states:
- HUD hierarchy:
- Menu hierarchy:
- Accessibility requirements:

### VFX Visual Language

- Shape:
- Color:
- Timing:
- Particle density:
- Glow/bloom policy:
- Hazard/readability rules:
- Performance considerations:
```

Rules:

- UI must support localization, scalable text, colorblind modes, and gamepad readability.
- VFX must not blind, clutter, or obscure priority information.
- Critical VFX states must have redundant signals beyond color.

---

### 8. Material and Rendering Language

```md
## Material and Rendering Language

| Material Class | Surface Traits | Roughness/Specular Feel | Detail Level | Use Cases | Avoid |
|---|---|---|---|---|---|
```

Include:

- organic,
- metal,
- cloth,
- stone,
- wood,
- water,
- magic/energy,
- UI surfaces,
- VFX surfaces.

Rules:

- Material language must match engine/rendering feasibility.
- Shader complexity must be flagged if uncertain.
- Style must not require unapproved pipeline features.

---

### 9. Animation and Motion Feel

```md
## Animation and Motion Feel

- Pose style:
- Timing:
- Exaggeration:
- Anticipation:
- Impact:
- Recovery:
- UI motion:
- Reduced-motion alternative:
```

Rules:

- Motion supports readability.
- Consequential actions need anticipation.
- UI transitions must respect reduced-motion settings.
- VFX timing should align with gameplay windows.

---

### 10. Accessibility and Readability Rules

```md
## Accessibility and Readability Rules

- Text scale:
- Contrast:
- Colorblind support:
- Non-color indicators:
- Motion sensitivity:
- Flashing effects:
- UI focus visibility:
- Subtitle/caption visual style:
- Minimum icon readability:
```

Rules:

- Visual direction cannot override accessibility requirements.
- Color-only communication is prohibited.
- Reduced-motion alternatives must be defined for major motion systems.

---

### 11. Negative Rules / Off-Style Patterns

Every major style rule needs anti-rules.

```md
## Negative Rule

- Off-style pattern:
- Why it breaks the identity:
- Where it is forbidden:
- Acceptable alternative:
```

Examples:

```text
Avoid neon rainbow gradients for magic unless a specific faction/area explicitly owns that language.
Avoid ultra-realistic grime if the game’s readability depends on clean stylized material blocks.
Avoid tiny faction markings that are unreadable at gameplay camera distance.
```

---

### 12. Asset Production Rules

```md
## Asset Production Rules

- Naming:
- File format:
- Scale/proportion:
- Texture/detail level:
- LOD/readability:
- Palette compliance:
- Accessibility compliance:
- Review evidence required:
```

Asset rule record:

```md
## Asset Production Rule: [Asset Category]

- Category:
- Naming pattern:
- Required variants:
- Size/resolution target:
- Material rules:
- Palette rules:
- Readability test:
- Accessibility test:
- Performance risk:
- Review owner:
```

---

### 13. Prompt Generation Rules

For image-generation or art-prompt tools, define safe prompt rules.

```md
## Prompt Generation Rules

- Approved descriptors:
- Forbidden descriptors:
- Required visual anchors:
- Style consistency constraints:
- Character constraints:
- Environment constraints:
- UI constraints:
- Negative prompt terms:
- Source references:
```

Rules:

- Prompts must not invent new canon visual identity.
- Prompts must include negative style rules.
- Prompts must cite or name the relevant art bible section.
- Generated concepts are not canon until reviewed.

---

### 14. Review Checklist

```md
## Art Review Checklist

- [ ] Matches visual pillars.
- [ ] Uses approved shape language.
- [ ] Uses approved palette/value logic.
- [ ] Preserves gameplay readability.
- [ ] Supports accessibility requirements.
- [ ] Avoids off-style patterns.
- [ ] Meets asset production rules.
- [ ] Does not contradict existing approved assets.
- [ ] Technical feasibility reviewed where relevant.
```

---

### 15. Open Decisions

```md
## Open Decision

- Decision:
- Impact:
- Owner:
- Options:
- Recommendation:
- Required before:
```

---

## Style Guide Required Structure

`design/art/style-guide.md` must define reusable visual tokens and execution rules.

```md
# Style Guide

## Document Status

- Status:
- Scope:
- Date:
- Sources:
- Confidence:

## Visual Tokens

### Color Tokens

| Token | Value / Family | Purpose | Accessibility Notes |
|---|---|---|---|

### Typography Tokens

| Token | Font / Style | Use | Constraints |
|---|---|---|---|

### Spacing / Layout Tokens

| Token | Value | Use |
|---|---|---|

### Shape Tokens

| Token | Shape | Meaning | Use |
|---|---|---|---|

### Material Tokens

| Token | Surface Rule | Use |
|---|---|---|

### Lighting Tokens

| Token | Rule | Use |
|---|---|---|

### VFX Tokens

| Token | Shape/Color/Motion | Use |
|---|---|---|
```

Rules:

- Tokens may use descriptive values if exact hex/font values are not approved yet.
- Mark exact values as `PROPOSED` unless approved.
- Accessibility notes are required for color and typography.

---

## Asset Direction Index Required Structure

`design/art/asset-direction-index.md` must map asset categories to source rules.

```md
# Asset Direction Index

## Document Status

- Status:
- Date:
- Sources:
- Confidence:

## Index

| Asset Category | Asset / Family | Direction Source | Status | Owner | Notes |
|---|---|---|---|---|---|
```

Asset statuses:

```text
PROPOSED
DIRECTION_READY
NEEDS_ART_DIRECTOR_REVIEW
NEEDS_TECHNICAL_ART_REVIEW
NEEDS_ACCESSIBILITY_REVIEW
BLOCKED
APPROVED
SUPERSEDED
```

Rules:

- Do not mark assets `APPROVED` without review evidence.
- Every asset category should point to art bible or style guide sections.
- Index rows must preserve unrelated content.

---

## Conflict Handling

### Conflict Types

```text
SOURCE_CONTRADICTION
DRAFT_SOURCE_RISK
STYLE_DRIFT
ACCESSIBILITY_CONFLICT
TECHNICAL_FEASIBILITY_CONFLICT
SCOPE_CONFLICT
PIPELINE_CONFLICT
MISSING_SOURCE_BLOCKER
```

### Conflict Record

```md
## Art Direction Conflict

- Type:
- Source A:
- Source B:
- Conflict:
- Impact:
- Recommended resolution:
- Owner:
- Status:
```

### Conflict Rules

- Do not resolve core visual identity conflicts silently.
- Prefer approved source-of-truth over generated reports.
- If conflict affects production asset creation, mark blocker.
- If conflict affects accessibility, escalate or mark `NEEDS_ACCESSIBILITY_REVIEW`.
- If conflict affects rendering/performance feasibility, mark `NEEDS_TECHNICAL_ART_REVIEW`.

---

## Review Delegation

Use `Task` subagents only when materially useful.

### Subagent Prompt Must Include

- user request,
- selected mode,
- relevant source paths,
- current draft/report,
- exact verdict needed,
- constraints,
- what not to review.

### Verdict Format Requested From Subagents

```text
APPROVE
CONCERNS
REJECT
```

Ask reviewers to include:

- blocking issues,
- high-risk issues,
- recommended changes,
- unresolved disagreements.

### Review Handling

If reviewer returns:

```text
APPROVE
```

record approval.

If reviewer returns:

```text
CONCERNS
```

- revise once if concerns are within scope,
- record remaining concerns.

If reviewer returns:

```text
REJECT
```

- stop production-ready claim,
- mark affected section `BLOCKED`,
- report required remediation.

If reviewer output is malformed:

- mark review `UNKNOWN`,
- do not claim approval.

---

## Validation

Before writing or finalizing, check:

1. Every conclusion cites or names a repository source.
2. Facts, inferences, and recommendations are separated.
3. All blockers have concrete next actions.
4. Proposed writes stay within declared output paths.
5. Existing files are not overwritten without approval.
6. Dry-run mode produced no writes.
7. Required sections for selected mode are present.
8. Negative rules exist.
9. Accessibility/readability rules exist.
10. Technical feasibility concerns are marked.
11. Subagent verdicts and disagreements are summarized.
12. Open decisions are explicit.

### Stop Conditions

Stop if:

- no concept or design context exists and no visual brief was supplied,
- requested scope requires missing primary source that cannot be safely inferred,
- target existing file would need replacement and user has not approved,
- core visual sources contradict each other and no safe provisional scope exists,
- review mode requires a reviewer that rejects the draft.

---

## Final Response

End with:

```md
## Art Bible Authoring Summary

### Written

- [file path] — [created/updated/skipped]

### Proposed Only

- [file path] — [reason]

### Skipped / Protected

- [operation] — [reason]

### Validation

- Source coverage:
- Review mode:
- Subagent verdicts:
- Open blockers:
- Confidence:

### Recommended Next Command

[command]
```

Recommended next command rules:

- After full art bible creation:

```text
/map-systems
```

or

```text
/design-review design/art/art-bible.md
```

depending on project workflow.

- If blockers remain:

```text
/art-bible [mode] --dry-run
```

after resolving blockers.

- If art bible is ready for review:

```text
/design-review design/art/art-bible.md
```

---

## Self-Learning Protocol

Self-learning means controlled improvement from approved art bible revisions, art-review findings, asset drift reviews, accessibility audits, technical-art reviews, production pipeline findings, and user corrections.

It does not mean hidden memory updates, autonomous visual identity changes, or treating one concept image as permanent direction.

### What May Be Learned

This skill may learn:

- approved visual pillars,
- approved color/palette rules,
- approved shape-language rules,
- approved material-language rules,
- approved UI visual tokens,
- approved VFX rules,
- approved asset naming/production conventions,
- accessibility findings,
- technical-art feasibility findings,
- asset drift findings,
- rejected visual directions and why.

### What Must Not Be Learned or Stored

Do not store:

- private user data,
- private chain-of-thought,
- secrets,
- credentials,
- unapproved visual preferences as canon,
- generated image artifacts as approved style,
- draft brainstorm ideas as art direction,
- one-off concept deviations as global rules,
- accessibility exceptions as normal policy,
- technical feasibility assumptions without review.

### Lesson Classification

Use:

```text
Confirmed Rule
Approved Art Direction
Visual Pillar Finding
Palette Finding
Shape Language Finding
Character Direction Finding
Environment Direction Finding
UI Direction Finding
VFX Direction Finding
Material Finding
Lighting Finding
Accessibility Finding
Technical Art Finding
Asset Drift Finding
Prompt Generation Finding
Rejected Approach
Working Assumption
Temporary Context
Superseded
```

### Lesson Storage

Durable lessons may be stored only in approved, reviewable locations such as:

```text
design/art/art-bible.md
design/art/style-guide.md
design/art/asset-direction-index.md
docs/art/art-direction-lessons.md
tasks/lessons.md
production/qa/art/
production/session-state/lessons.md
```

### Lesson Format

```md
## Lesson: [Short Name]

- Status:
- Source:
- Applies to:
- Lesson:
- Evidence:
- Date/session:
- Expiry/review trigger:
- Conflicts:
```

### Lesson Validation Rules

A lesson may be stored only if:

- it is specific,
- it is approved or evidence-backed,
- it applies to art direction or art production,
- it does not include sensitive data,
- it is not overgeneralized,
- it does not conflict with approved art bible/style guide,
- it has an owner or review trigger where appropriate.

### Lesson Expiry

Review or expire lessons when:

- art bible changes,
- style guide changes,
- visual pillars change,
- supported platforms change,
- rendering pipeline changes,
- accessibility requirements change,
- asset pipeline changes,
- Art Director supersedes it,
- Creative Director supersedes it,
- production evidence contradicts it,
- the lesson was temporary,
- the lesson is too broad.

---

## Self-Healing Protocol

Self-healing means detecting an art-authoring failure, containing the risk, repairing safely, verifying the repair, and reporting uncertainty.

### Failure Types

Monitor for:

- missing concept source,
- missing visual brief,
- contradictory sources,
- draft-only source treated as approved,
- unsupported visual claim,
- vague style language,
- missing negative rules,
- missing accessibility constraints,
- missing technical feasibility constraints,
- existing target file present,
- protected write requested,
- dry-run write attempt,
- failed subagent review,
- unresolved reviewer disagreement,
- asset index drift,
- source list missing,
- confidence missing.

### Recovery Loop

When failure occurs:

1. **Stop**
   - Do not mark artifact production-ready.

2. **Identify**
   - State the exact failure.

3. **Classify**
   - Source, scope, evidence, style quality, accessibility, technical feasibility, write safety, review, or validation issue.

4. **Contain**
   - Mark status:
     - `BLOCKED`,
     - `OPEN_DECISION`,
     - `LOW_CONFIDENCE`,
     - `NEEDS_REVIEW`,
     - `PROTECTED_WRITE_REQUIRED`,
     - `DRY_RUN_NO_WRITE`.

5. **Recover**
   - narrow scope,
   - ask for missing source decision,
   - separate inference from fact,
   - add negative rules,
   - add accessibility rules,
   - add technical review note,
   - preview protected write,
   - preserve existing content,
   - revise from reviewer concerns.

6. **Verify**
   - Re-check source list.
   - Re-check write paths.
   - Re-check selected-mode required sections.
   - Re-check dry-run status.
   - Re-check review status.

7. **Report**
   - Summarize issue, repair, remaining risk, and next action.

8. **Learn**
   - Propose durable lesson only if validated and approved.

---

## Error Recovery

### Missing Concept or Visual Brief

If no concept/design context exists and no visual brief was supplied:

- stop,
- report missing source,
- ask for concept brief or approved brainstorm,
- do not invent visual identity.

### Missing Source For Narrow Scope

If `full` lacks enough source context but `style`, `characters`, `environments`, or `ui` can be safely inferred:

- narrow scope,
- state the narrowing,
- mark missing sections as blockers.

### Contradictory Sources

If sources disagree:

- identify source priority,
- list contradiction,
- use approved source if clear,
- otherwise mark `OPEN_DECISION`.

### Existing Target File Present

If target exists:

- read it,
- preserve content,
- update additively if safe,
- ask before replacement.

### Vague Visual Language

If draft contains vague terms:

- replace with concrete visual rule,
- add examples and anti-examples,
- add review test.

### Missing Negative Rules

If off-style rules are missing:

- add negative rules for each major category,
- ensure they are actionable.

### Accessibility Conflict

If art direction conflicts with accessibility:

- mark `NEEDS_ACCESSIBILITY_REVIEW`,
- add redundant non-color indicators,
- revise palette/contrast rules,
- do not claim accessibility approval.

### Technical Feasibility Conflict

If direction may require unapproved rendering/pipeline capability:

- mark `NEEDS_TECHNICAL_ART_REVIEW`,
- add feasibility risk,
- add alternative lower-cost execution path.

### Failed Subagent Review

If subagent rejects or fails:

- do not claim review approval,
- revise once if possible,
- otherwise block production-ready status.

### Dry-Run Write Attempt

If dry-run is active:

- never write,
- show proposed files and exact status as proposed only.

---

## Memory Policy

### Short-Term Task Memory

Track during current invocation:

- selected mode,
- review mode,
- dry-run state,
- source files read,
- source confidence,
- visual pillars,
- inferred rules,
- recommendations,
- open decisions,
- target files,
- write decisions,
- review verdicts,
- validation gaps.

Short-term memory expires after invocation unless explicitly stored.

### Project Memory

Project memory may store:

- approved visual pillars,
- approved palette rules,
- approved style tokens,
- approved shape-language rules,
- approved material rules,
- approved prompt-generation rules,
- accessibility findings,
- technical-art findings,
- asset drift lessons,
- rejected visual directions.

### Never Store

Never store:

- private user data,
- private chain-of-thought,
- secrets,
- credentials,
- unapproved visual ideas as canonical,
- generated concept images as approved direction,
- one-off exceptions as global art rules,
- unsupported accessibility or feasibility claims.

---

## Feedback Policy

When the user, Creative Director, Art Director, UX Designer, Accessibility Specialist, Technical Artist, Producer, or relevant domain owner corrects art bible behavior:

1. Accept the correction.
2. Identify whether it affects:
   - visual pillars,
   - camera/readability,
   - shape language,
   - palette/lighting,
   - characters,
   - environments,
   - UI/VFX,
   - materials/rendering,
   - accessibility,
   - asset production,
   - prompt generation,
   - review workflow,
   - write policy.
3. Revise current draft or output.
4. Ask whether the correction should become durable art-direction guidance if reusable.
5. Store only if approved and evidence-backed.

---

## Tool-Use Policy

Allowed tools:

```text
Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
```

Rules:

- Use `Glob` and `Grep` before reading large file sets.
- Use `Read` for source-of-truth files and existing outputs.
- Use `Task` only for bounded review.
- Use `Write` for new canonical outputs.
- Use `Edit` for targeted additive updates.
- Use `AskUserQuestion` for protected writes, source conflicts, scope ambiguity, and owner decisions.
- Do not run shell commands unless tool permissions change.
- Do not claim image generation, asset review, contrast audit, or runtime validation happened unless evidence exists.

---

## Safety Guardrails

Never:

- invent the visual identity when concept context is absent,
- treat draft sources as approved direction,
- overwrite existing art docs without approval,
- write during dry-run,
- edit files outside declared outputs without approval,
- change gates/status/stories/releases/registries without approval,
- claim Art Director approval if no review occurred,
- claim accessibility compliance without evidence,
- claim technical feasibility without evidence,
- omit negative rules,
- omit source list,
- bury open decisions,
- present recommendations as facts.

---

## Output Standards

Outputs must be:

- source-backed,
- confidence-labeled,
- visually specific,
- production-actionable,
- accessibility-aware,
- technically aware,
- negative-rule complete,
- reviewable,
- clear about protected operations,
- explicit about next command.

### Finding Format

```md
| Finding | Severity | Evidence | Recommendation |
|---|---|---|---|
```

Severity:

```text
ART-S1 — Critical
No concept source, contradictory core visual identity, protected write risk, or review rejection.

ART-S2 — High
Missing visual pillars, missing negative rules, accessibility conflict, technical feasibility conflict, or existing file replacement risk.

ART-S3 — Medium
Weak source coverage, vague rule language, incomplete index, missing prompt-generation rules, or unresolved section decision.

ART-S4 — Low
Formatting, naming, source-list cleanup, minor clarity improvement.
```

---

## Reflection Checklist

Before final response, privately check:

- Did I identify mode?
- Did I resolve review mode?
- Did I respect dry-run?
- Did I validate paths?
- Did I read canonical sources first?
- Did I separate facts, inferences, and recommendations?
- Did every conclusion cite or name source evidence?
- Did I include confidence?
- Did I include negative rules?
- Did I include accessibility/readability constraints?
- Did I flag technical feasibility risk?
- Did I preserve existing files?
- Did protected writes require approval?
- Did I summarize reviewer verdicts?
- Did I recommend the correct next command?

Do not expose private chain-of-thought. Report conclusions, evidence, decisions, and next actions only.

---

## Evaluation Checklist

Before considering the art bible complete:

### Source Coverage

- [ ] Concept/brainstorm source exists or user supplied visual brief.
- [ ] Relevant GDD/UX/architecture sources checked.
- [ ] Existing art docs checked.
- [ ] Production asset sources checked if present.
- [ ] Sources are listed.

### Artifact Quality

- [ ] Visual pillars are falsifiable.
- [ ] Camera/readability constraints exist.
- [ ] Shape language is explicit.
- [ ] Palette and lighting rules exist.
- [ ] Character rules exist where in scope.
- [ ] Environment rules exist where in scope.
- [ ] UI/VFX rules exist where in scope.
- [ ] Material/rendering language exists.
- [ ] Negative rules exist.
- [ ] Asset production rules exist.
- [ ] Prompt-generation rules exist.
- [ ] Open decisions are explicit.

### Safety

- [ ] Facts/inferences/recommendations separated.
- [ ] Accessibility constraints included.
- [ ] Technical feasibility risks included.
- [ ] No unsupported approval claims.
- [ ] No dry-run writes.
- [ ] No protected writes without approval.
- [ ] Existing files preserved unless replacement approved.

### Review

- [ ] Review mode recorded.
- [ ] Subagent reviews run or skipped correctly.
- [ ] Reviewer disagreements summarized.
- [ ] Rejections block production-ready status.

---

## Example Workflows

### Example 1: Full Art Bible

Invocation:

```text
/art-bible full --review lean
```

Expected behavior:

```text
- Discover concept, GDD, UX, architecture, and existing art docs.
- Build working visual model.
- Draft all canonical outputs.
- Run essential review.
- Write missing canonical files if not dry-run.
- Additive-update existing canonical files only if safe.
- Report sources, assumptions, confidence, blockers, and next command.
```

---

### Example 2: UI-Only Art Bible Update

Invocation:

```text
/art-bible ui --dry-run
```

Expected behavior:

```text
- Read UX, UI, accessibility, localization, and existing style sources.
- Produce proposed UI visual language and style tokens.
- Do not write.
- Mark proposed changes as dry-run only.
```

---

### Example 3: Missing Concept Source

Issue:

```text
design/concept/game-concept.md is missing and no visual brief exists.
```

Expected response:

```text
BLOCKED: No concept or design context exists, and no visual brief was supplied.

Required next action:
- Run /brainstorm and approve a concept, or
- Provide a visual brief with genre, camera, tone, references, constraints, and target experience.
```

---

### Example 4: Existing File Present

Issue:

```text
design/art/art-bible.md already exists.
```

Expected behavior:

```text
- Read existing file.
- Preserve historical content.
- Additive-update only if safe.
- Ask before replacement.
```

---

### Example 5: Vague Rule Repair

Bad draft:

```text
Characters should look cool and memorable.
```

Repair:

```text
Characters must be identifiable by silhouette at gameplay camera distance. Each major character type uses one dominant silhouette hook: weapon profile, head/helmet shape, cloak/coat outline, or posture. Avoid designs whose identity depends mainly on small texture details.
```

---

### Example 6: Accessibility Conflict

Issue:

```text
The palette uses red/green as the only enemy/ally distinction.
```

Expected response:

```text
Finding: Accessibility conflict.

Repair:
- Add shape/icon/frame-language distinction.
- Define colorblind-safe palette alternative.
- Mark UI/HUD use as requiring accessibility review.
```

---

### Example 7: Technical Feasibility Risk

Issue:

```text
Style direction requires heavy volumetric lighting and dense transparent particles on low-end target hardware.
```

Expected response:

```text
Finding: Technical-art feasibility risk.

Repair:
- Add low-cost lighting alternative.
- Add VFX density budget placeholder.
- Mark Technical Artist / Performance review required.
```

---

### Example 8: User Correction

User says:

```text
The world should use warm interiors and cold exteriors, not the other way around.
```

Response pattern:

```text
Understood. I’ll revise palette and lighting rules so interiors trend warm/safe and exteriors trend cold/exposed, unless a later approved art direction supersedes that. Store this as durable art bible guidance only if approved.
```

---

### Example 9: Case Where The Skill Must Not Learn

User says during exploration:

```text
Maybe everything should be neon cyberpunk.
```

Response pattern:

```text
I’ll treat that as exploratory, not approved visual direction. If it becomes canonical, it needs source status, visual-pillar alignment, palette rules, negative rules, and art director approval.
```

---

## Final Behavioral Rule

Art bible work must be:

- source-backed,
- confidence-labeled,
- visually specific,
- production-actionable,
- accessibility-aware,
- technically feasible or explicitly risk-marked,
- negative-rule complete,
- dry-run safe,
- protected-write safe,
- reviewable,
- and honest about unresolved visual identity decisions.