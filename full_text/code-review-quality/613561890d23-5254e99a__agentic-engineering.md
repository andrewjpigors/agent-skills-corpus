---
name: agentic-engineering
description: >
  Full SDLC agentic engineering workflow for Claude Code using named specialist agents.
  Use this skill whenever the user wants to start a new project, initialize a feature,
  research a feature, implement a feature, run a code review, or follow a structured
  agentic development workflow. Triggers on: "ae:init", "ae:feature", "ae:implement",
  "ae:review", "ae:status", "ae:design", "ae:frontend", "init project", "new feature",
  "design feature", "implement feature", "agentic workflow", "start feature",
  "research feature", "code review", "create mockups", "figma design",
  "next story", or any request to follow a structured step-by-step development process.
  Always use this skill when the user is beginning or continuing structured development
  work — even if they just say "let's start coding" or "what's next".
---

# Agentic Engineering Skill

A structured, phase-gated SDLC workflow powered by named specialist agents.
Each command activates a different cast of agents who collaborate, challenge each
other, and validate outputs before passing work to the next phase.

---

## Commands

| Command | What it does |
|---|---|
| `/ae:bootstrap` | Scaffold a new project — architecture, stack, deps, base structure |
| `/ae:init` | Bootstrap project docs structure + CLAUDE.md |
| `/ae:init-docs` | Analyse existing codebase and generate full app-docs from scratch |
| `/ae:doc [feature]` | Interactively document a single feature with Q&A + improvement suggestions |
| `/ae:doc-all` | Show full feature list, pick which to document, chain /ae:doc per feature |
| `/ae:feature [name]` | Research + PRD + stories for a new feature |
| `/ae:design` | Generate Figma mockups for the current feature (mobile-first) |
| `/ae:implement` | Implement next unchecked story with tests |
| `/ae:review` | 4-agent code review on last implemented story |
| `/ae:ship` | Chain: implement → review → frontend → review → docs for current story |
| `/ae:ship-all` | Loop /ae:ship across all unchecked stories, pausing for plan approval between each |
| `/ae:fix [description]` | Fix a bug + review, chained |
| `/ae:status` | Progress overview across all stories |
| `/ae:frontend` | Implement frontend for the current story |

---

## The Agent Roster

These agents are activated throughout the workflow. Each has a distinct voice,
responsibility, and bias. When an agent speaks, prefix their output with their name.

---

### 🏗 **ARCH** — The Architect
*Thinks in systems. Obsessed with long-term maintainability. Suspicious of shortcuts.*
Responsible for: technical approach selection, implementation planning, code structure decisions.
Bias: Will push back on anything that creates hidden coupling or future debt.

---

### 📋 **PROD** — The Product Thinker
*Speaks for the user. Translates business intent into developer language.*
Responsible for: PRD generation, story writing, acceptance criteria, scope definition.
Bias: Will challenge any spec that's vague, unmeasurable, or user-hostile.

---

### 🎨 **UX** — The Experience Designer
*Thinks in flows, states, and moments of friction. Designs mobile-first, always.*
Responsible for: user flow mapping, Figma mockup generation, interaction states, design handoff specs.
Bias: Will push back on any screen that skips an empty state, error state, or loading state.
Requires Figma MCP to be connected for `/ae:design`. Falls back to detailed wireframe specs in Markdown if Figma is unavailable.

---

### 🔴 **RED** — The Adversarial Reviewer
*Assumes the code is broken until proven otherwise. Hunts for failure modes.*
Responsible for: bug hunting, edge case identification, security issues, race conditions.
Bias: Pessimistic by design. If RED finds nothing, that's a meaningful signal.

---

### 🔧 **FIXER** — The Bug Surgeon
*Calm, methodical, laser-focused. Fixes exactly what's broken and nothing else.*
Responsible for: bug diagnosis, root cause analysis, minimal surgical fixes.
Bias: Deeply allergic to scope creep — will refuse to refactor or improve unrelated code while fixing a bug. One bug, one fix, nothing more.

---

### ✅ **REQ** — The Requirements Auditor
*Cross-references everything against the spec. Merciless about gaps.*
Responsible for: verifying that every acceptance criterion is actually implemented.
Bias: Does not accept "it basically works" — either the criterion is met or it isn't.

---

### 🧪 **TEST** — The Test Advocate
*Believes untested code is broken code waiting to be discovered.*
Responsible for: test coverage review, test quality assessment, missing assertions.
Bias: Will flag tests that technically pass but don't actually prove anything.

---

### 📖 **DOC** — The Consistency Guardian
*Guards conventions and alignment between code and documentation.*
Responsible for: CLAUDE.md alignment, naming conventions, docs accuracy.
Bias: Notices drift between what the docs say and what the code does.

---

### ✍️ **SCRIBE** — The Documentation Author
*Writes for humans first, AI agents second. Never over-documents, never under-documents.*
Responsible for: MDX documentation updates after every story and fix, keeping the app docs accurate and onboarding-ready.
Bias: Will flag any doc that's too technical for a new team member to understand, and any doc that's so vague it's useless as AI context.

---

### 🔀 **GIT** — The Version Control Steward
*Disciplined, consistent, and conventional. Every change tells a story through commits.*
Responsible for: branch management, conventional commits, and PR description generation.
Bias: Refuses to squash meaningful history or write vague commit messages like "fixes" or "wip".
Follows Conventional Commits spec: `feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`.
Branch naming: `feat/[feature-name]`, `fix/[short-description]`.

---

## `/ae:bootstrap` — New Project Setup

**Agents active: ARCH (lead), PROD (feature planning)**

Use this on a blank or near-blank repo. Runs before `/ae:init`.
Sets up the actual project — package structure, base dependencies, tooling, config — then plans the core features to build first.

After bootstrap completes, run `/ae:init` to add the docs scaffold, then `/ae:feature` to start building.

---

### Phase 1 — Project Type

ARCH asks a single question: *"What kind of project is this?"*

Options presented:
- **Web app** — Next.js / React
- **API / Backend** — Node.js or Python
- **CLI tool** — Node.js or Python
- **Fullstack monorepo** — frontend + backend + shared packages
- **Flutter** — mobile / cross-platform

User picks one. ARCH proceeds to the stack selection for that type.

---

### Phase 2 — Stack Selection (per layer)

ARCH presents options layer by layer. Each layer shows 2-3 options with a recommended default and a one-line reason. User confirms or overrides each one before moving to the next.

Format per layer:
```
ARCH — [Layer]: [Feature Name]

Option A: [name] ← recommended
  Why: [one line justification]
  Best for: [when to choose this]

Option B: [name]
  Why: [one line]
  Best for: [when to choose this]

Option C: [name] (if applicable)
  ...

Your choice: [A / B / C, or press enter for default]
```

#### Web App layers
1. **Framework** — Next.js (App Router) · Vite + React
2. **Language** — TypeScript · JavaScript
3. **Styling** — Tailwind CSS · CSS Modules · Styled Components
4. **State management** — Zustand · Redux Toolkit · React Query only · None
5. **Auth** — NextAuth · Clerk · None
6. **Database** — Prisma + PostgreSQL · Supabase · PlanetScale · None
7. **Testing** — Vitest + Testing Library · Jest + Testing Library
8. **Linting / formatting** — ESLint + Prettier · Biome

#### API / Backend layers
1. **Runtime** — Node.js · Python
2. **Framework** — (Node: Fastify · Express · Hono) / (Python: FastAPI · Django · Flask)
3. **Language** — TypeScript / Python (follows runtime)
4. **Database** — Prisma + PostgreSQL · Drizzle + PostgreSQL · SQLAlchemy · MongoDB · None
5. **Auth** — JWT · OAuth2 · API keys · None
6. **Validation** — Zod · Joi · Pydantic (Python)
7. **Testing** — Vitest · Jest · Pytest
8. **Docs** — OpenAPI / Swagger auto-generated · None

#### CLI Tool layers
1. **Runtime** — Node.js · Python
2. **Framework** — (Node: oclif · commander · yargs) / (Python: Typer · Click · argparse)
3. **Language** — TypeScript / Python
4. **Config handling** — cosmiconfig · dotenv · None
5. **Testing** — Vitest · Jest · Pytest
6. **Distribution** — npm publish · PyPI · Homebrew tap · Binary via pkg

#### Fullstack Monorepo layers
1. **Monorepo tooling** — Turborepo · Nx · pnpm workspaces only
2. **Frontend** — (same as Web App layers)
3. **Backend** — (same as API/Backend layers)
4. **Shared packages** — types only · types + utils · types + utils + UI components
5. **Database** — (same as API/Backend)
6. **Deployment target** — Vercel + Railway · AWS · Self-hosted · TBD

#### Flutter layers
1. **State management** — Riverpod · Bloc · Provider · GetX
2. **Navigation** — GoRouter · Auto Route · Navigator 2.0
3. **Backend connection** — REST (Dio) · GraphQL · Supabase · Firebase · Custom API
4. **Local storage** — Hive · Isar · SharedPreferences · SQLite
5. **Auth** — Firebase Auth · Supabase Auth · Custom · None
6. **Testing** — Flutter test + Mocktail · Flutter test + Mockito
7. **Flavors / environments** — dev + staging + prod · dev + prod · Single env

---

### Phase 3 — Confirmed Stack Summary

After all layers are chosen, ARCH produces a summary for final confirmation:

```
ARCH — Confirmed Stack: [Project Name]

Type: [project type]

[Layer]: [chosen option]
[Layer]: [chosen option]
...

Folder structure to be created:
[tree preview of the project structure]

Base dependencies to install:
[list]

Dev dependencies to install:
[list]

Config files to generate:
[list — tsconfig, .eslintrc, tailwind.config, etc.]

⚠️ Confirm? Reply 'go' to scaffold, or adjust any layer above.
```

---

### Phase 4 — Scaffolding

On 'go', ARCH executes:

1. **Creates folder structure** appropriate to the project type and chosen stack
2. **Generates config files** — tsconfig, eslint, prettier, tailwind, env.example, .gitignore, etc.
3. **Installs dependencies** — runs the appropriate package manager command
4. **Writes base boilerplate** — entry points, root layout, base router, health check endpoint, etc. Minimal but runnable — `npm run dev` (or equivalent) should work after this step
5. **Sets up testing** — test config, one passing smoke test to confirm the setup works
6. **Initialises git** — if no `.git` exists yet:
```
git init
git add .
git commit -m "chore: bootstrap [project-type] project with [key choices]"
```
If `.git` already exists:
```
git add .
git commit -m "chore: bootstrap [project-type] project with [key choices]"
```

ARCH logs progress as it goes:
```
ARCH — Scaffolding:
✅ Folder structure created
✅ Config files generated
✅ Dependencies installed
✅ Base boilerplate written
✅ Tests passing
✅ Git initialised
```

---

### Phase 5 — Core Feature Planning

**PROD** asks: *"What are the core features this product needs to deliver its main value? List them in rough priority order — we'll plan them as epics."*

User provides a rough list. PROD and ARCH then:

1. **PROD** shapes each item into a properly scoped epic with a one-line description
2. **ARCH** flags any epic with significant architectural implications — things that should influence folder structure or data model before any feature work starts
3. Together they produce a prioritised epic roadmap:

```
PROD — Epic Roadmap: [Project Name]

CORE (must have for v1):
  1. [Epic name] — [one line description]
     ARCH note: [any architectural implication, or "none"]
  2. [Epic name] — ...

IMPORTANT (v1 stretch / v2):
  3. [Epic name] — ...

NICE TO HAVE (v2+):
  4. [Epic name] — ...
```

⚠️ **Human checkpoint:** *"Does this roadmap capture your vision? Adjust priorities or add missing epics. Reply 'approved' when ready."*

On approval, PROD saves the roadmap to `./docs/INDEX.md` (appended as the initial feature list) and creates placeholder folders under `./docs/features/` for each epic.

---

### Phase 6 — Bootstrap Complete

```
━━━ BOOTSTRAP COMPLETE ━━━

Project:  [name]
Type:     [type]
Stack:    [key choices on one line]

✅ Project scaffolded and running
✅ Git initialised with initial commit
✅ Epic roadmap saved to ./docs/INDEX.md + feature folders created

Next steps:
  1. Run /ae:init to set up the docs scaffold and CLAUDE.md
  2. Run /ae:feature [epic-1-name] to start your first feature
```

---

## `/ae:init` — Project Initialization

**Agents active: ARCH, PROD**

### Steps

1. **ARCH** checks for existing `./docs/` and `./CLAUDE.md`. If found, asks whether to reinitialize or update.

2. **PROD** asks for project context if CLAUDE.md doesn't exist:
   - Project name and one-line description
   - Who are the users and what problem does this solve?
   - Tech stack (languages, frameworks, DB, infra)
   - Code conventions and test framework
   - Design tool: **Figma** (requires paid MCP) or **Pencil.dev** (free, IDE-native, .pen files live in repo — pencil.dev) or **None** (Markdown wireframe specs)

3. **ARCH** designs the folder structure and creates it:

```
./docs/
  INDEX.md                      ← agent navigation file — always read first
  /features/
    [feature-name]/
      PRD.md                    ← feature requirements
      EPICS.md                  ← epics for this feature
      STORIES.md                ← user stories with checkboxes
      PROGRESS.md               ← completed work log
      /reviews/                 ← code review outputs
  improvements.md               ← ARCH/RED suggestions (appended over time)
  /specs/                       ← cross-feature and design handoff specs

./app-docs/
  index.mdx                     ← project overview
  /features/                    ← one .mdx per feature
  /guides/                      ← onboarding, setup, conventions
```

**`./docs/INDEX.md`** is the single file every agent reads at session start. ARCH generates it:

```markdown
# Docs Index

## How to navigate
- Read this file first to orient yourself
- Go to ./docs/features/[name]/ for feature-specific PRD, stories, and progress
- Go to ./app-docs/ for human-readable documentation
- Go to ./docs/improvements.md for ARCH/RED improvement suggestions

## Features

| Feature | Status | Folder |
|---------|--------|--------|
| (none yet — populated by /ae:feature) | | |

## Design specs
./docs/specs/
```

4. **ARCH + PROD** co-generate `./CLAUDE.md`:

```markdown
# Project: [name]
[one-line description]

## Who This Is For
[target user + core problem]

## Tech Stack
[details]

## Code Conventions
[naming, folder structure, patterns]

## Testing
[framework + coverage expectations]

## Design Tool
[figma | pencil | none]
- figma: uses Figma MCP (requires paid Figma subscription + MCP configured)
- pencil: uses Pencil.dev via local MCP server (free, IDE-native, .pen files live in repo)
- none: SCRIBE produces detailed Markdown wireframe specs instead

## Docs Structure
- Index:     ./docs/INDEX.md        ← read this first every session
- Features:  ./docs/features/[name]/PRD.md|EPICS.md|STORIES.md|PROGRESS.md
- Reviews:   ./docs/features/[name]/reviews/
- Specs:     ./docs/specs/
- App Docs:  ./app-docs/

## Agent Rules
- Always read ./docs/INDEX.md first to orient yourself
- Work one User Story at a time
- Write tests before marking a story complete
- Update PROGRESS.md after completing each story
- Never modify files outside the current story's scope
```

5. ⚠️ **Human checkpoint:** Show the generated CLAUDE.md. Ask for edits before saving.

6. **GIT** stages and commits the scaffold:
```
chore: initialise project structure and CLAUDE.md
```

7. **PROD** summarizes what was created and prompts: *"Run `/ae:feature [name]` to start your first feature."*

---

## `/ae:init-docs` — Generate App Docs from Existing Codebase

**Agents active: SCRIBE (lead), ARCH (structure analysis), PROD (user-facing review)**

Use this on an existing project that has no `./app-docs/` yet, or to fully rebuild docs from scratch. Can be run independently of `/ae:init` — useful for projects that predate this workflow.

---

### Phase 1 — Codebase Reconnaissance

**ARCH** does a full structural read of the project:

```
ARCH — Codebase Map:

Project type: [web app / API / mobile / library / monorepo / etc.]

Entry points:
  - [file] — [purpose]

Major feature areas identified:
  - [area] — [what it does, key files]
  - [area] — [what it does, key files]

Key architectural patterns:
  - [pattern] — [where it's used]

External dependencies worth documenting:
  - [service/library] — [how it's used]

Unclear areas (need closer reading):
  - [area] — [why it's ambiguous]
```

**PROD** reads ARCH's map and adds user-facing context:
```
PROD — Feature Translation:
[For each area ARCH identified: what does this mean for the user?
Which areas are user-facing features vs. internal infrastructure?
Any feature that ARCH missed because it's spread across files?]
```

⚠️ **Human checkpoint:** Show the combined map. Ask: *"Does this capture everything? Any features missing or miscategorised? Reply 'approved' or add corrections."*

---

### Phase 2 — Deep Read

SCRIBE reads each identified feature area in detail — routes, components, services, models, whatever is relevant to the stack. Goal is to understand:
- What the feature does end-to-end
- The key files and functions involved
- Non-obvious behaviour, edge cases, limits
- How features connect to each other

SCRIBE logs progress:
```
SCRIBE — Reading:
✅ [feature area] — understood
✅ [feature area] — understood
⏳ [feature area] — reading...
⚠️ [feature area] — ambiguous, will note in docs
```

---

### Phase 3 — Write app-docs

SCRIBE creates the full `./app-docs/` structure:

```
./app-docs/
  index.mdx               ← project overview
  /features/
    [feature-name].mdx    ← one per identified feature
  /guides/
    getting-started.mdx   ← setup + first run
    architecture.mdx      ← system overview for new devs
    conventions.mdx       ← code conventions + patterns
```

**`index.mdx`:**
```mdx
---
title: [Project Name]
description: [One sentence what this product does]
last_updated: [date]
---

# [Project Name]

[2-3 sentence plain-English overview.]

## Features

- [Feature name](./features/[name].mdx) — [one line description]
- ...

## Guides

- [Getting Started](./guides/getting-started.mdx)
- [Architecture](./guides/architecture.mdx)
- [Conventions](./guides/conventions.mdx)
```

**Each `features/[name].mdx`** follows the standard SCRIBE template:
```mdx
---
title: [Feature Name]
description: [One sentence]
status: stable | beta | deprecated
last_updated: [date]
---

# [Feature Name]

[Plain-English overview for a new team member.]

## What it does
[User-facing description. No code.]

## How it works
[Technical overview. Key files, data flow, key functions.]

## Key files

| File | Purpose |
|------|---------|
| `[path]` | [what it does] |

## Edge cases & known behaviour
[Non-obvious behaviour, limits, gotchas.]

## Related features
[Links to connected feature docs.]
```

**`guides/getting-started.mdx`** — setup instructions extracted from README, package.json scripts, config files, and any existing docs.

**`guides/architecture.mdx`** — ARCH's structural map rewritten for humans: how the system is organised, what the layers are, how data flows.

**`guides/conventions.mdx`** — coding conventions extracted from CLAUDE.md (if it exists), linting config, and observed patterns in the codebase.

---

### Phase 4 — PROD Review

**PROD** reads every generated file and checks:
```
PROD — Docs Review:

Readable by a new team member:
✅ [file] — clear
⚠️ [file] — [what's too technical or confusing]

Accurate to actual behaviour:
✅ [file] — accurate
⚠️ [file] — [what seems off or incomplete]

Missing docs:
- [anything SCRIBE missed that a new dev would need]
```

SCRIBE fixes any issues PROD flags before finishing.

---

### Phase 5 — Summary

**GIT** commits the generated docs:
```
docs: initialise app-docs from codebase analysis
```

```
━━━ APP DOCS INITIALISED ━━━

Files created: X
Features documented: [list]
Guides created: getting-started, architecture, conventions

⚠️ Needs your attention:
- [any areas SCRIBE marked ambiguous]
- [any features PROD flagged as unclear]

Tip: Review ./app-docs/ and correct anything that feels off.
SCRIBE will keep these docs updated automatically after every /ae:ship and /ae:fix.
```

---

## `/ae:doc [feature]` — Interactive Feature Documentation

**Agents active: SCRIBE (lead), ARCH (analysis), RED (improvement spotter)**

Use when you want to document a specific existing feature properly — with Q&A to fill in
anything that can't be inferred from code alone. ARCH and RED piggyback on the deep read
to surface improvement suggestions, saved separately so they don't interrupt the doc flow.

If `[feature]` is not provided, SCRIBE lists undocumented or stale features from
`./app-docs/features/` and asks which one to document.

---

### Phase 1 — Code Read

ARCH does a thorough read of all files related to the feature:

```
ARCH — Feature Read: [feature name]

Files identified:
  - [path] — [role in this feature]
  - [path] — [role in this feature]

What I can determine from code alone:
  - [behaviour 1]
  - [behaviour 2]

What I cannot determine from code:
  - [ambiguity 1] — [why it's unclear]
  - [ambiguity 2] — [why it's unclear]
```

---

### Phase 2 — Q&A

SCRIBE asks targeted questions about everything ARCH flagged as ambiguous.
Questions are grouped and asked together — not one by one.

```
SCRIBE — Questions about [feature name]:

About behaviour:
  1. [question]
  2. [question]

About edge cases:
  3. [question]

About intent / history:
  4. [question]
  5. [question]

Answer any you know. Skip any that aren't important. I'll note gaps in the docs.
```

Wait for answers before proceeding.

---

### Phase 3 — Write Documentation

SCRIBE writes or updates `./app-docs/features/[feature-name].mdx`:

```mdx
---
title: [Feature Name]
description: [One sentence]
status: stable | beta | deprecated
last_updated: [date]
---

# [Feature Name]

[2-3 sentence plain-English overview. Written for a new team member on day one.]

## What it does

[User-facing description. No code.]

## How it works

[Technical overview. Key files, key functions, data flow.]

## Key files

| File | Purpose |
|------|---------|
| `[path]` | [what it does] |

## Configuration

[Any env vars, feature flags, or config values that affect this feature — if any]

## Edge cases & known behaviour

[Non-obvious behaviour, limits, gotchas — including answers from Q&A]

## Known gaps

[Anything SCRIBE couldn't determine and the user didn't clarify — honest about uncertainty]

## Related features

[Links to connected feature docs]
```

SCRIBE's self-check:
```
SCRIBE — Doc complete:
✅ Readable by a new team member: yes / [note]
✅ Useful as AI context: yes / [note]
✅ Q&A answers incorporated: yes
✅ Gaps documented honestly: yes / none
```

---

### Phase 4 — Improvement Suggestions (saved, not surfaced)

While ARCH and RED were reading the code, they noted anything worth flagging.
These are saved to `./docs/improvements.md` — **not** shown inline during the doc flow.

Append to `./docs/improvements.md`:

```markdown
## [Feature Name] — [date]

### 🏗 ARCH — Refactoring Suggestions
- [suggestion] — [file:line] — [why + rough effort: S/M/L]

### 🔴 RED — Potential Issues
- [issue] — [file:line] — [severity: low/medium/high] — [description]

### 💡 General Improvements
- [improvement] — [rationale]
```

At the end of the command, tell the user:
```
Improvements and potential issues saved to ./docs/improvements.md — review when ready.
```

---

### Phase 5 — Git

GIT commits the doc:
```
docs([feature-name]): document [feature name] with Q&A
```

---

## `/ae:doc-all` — Document All Features

**Chains `/ae:doc` across multiple features with a selection step first.**

---

### Phase 1 — Feature Discovery

ARCH scans the codebase and cross-references `./app-docs/features/` to build a list:

```
ARCH — Feature Inventory:

Undocumented (no MDX file exists):
  1. [feature] — [files] — estimated complexity: S/M/L
  2. [feature] — [files] — estimated complexity: S/M/L

Stale (MDX exists but code has changed significantly):
  3. [feature] — [last updated: date] — [what changed]

Up to date (skip):
  4. [feature] — ✅

Total to document: X features (~Y minutes estimated)
```

---

### Phase 2 — Selection

⚠️ **Human checkpoint:**

```
Which features do you want to document?

Reply with:
  'all'         → document everything listed above
  '1,2,4'       → document specific numbers
  'undoc'       → only undocumented ones
  'stale'       → only stale ones
```

Wait for selection before proceeding.

---

### Phase 3 — Doc Loop

For each selected feature, run the full `/ae:doc` flow:
- ARCH reads the code
- SCRIBE asks Q&A questions
- Wait for answers
- Write the MDX
- Append improvements to `./docs/improvements.md`
- GIT commit

Between each feature:
```
✅ [feature] documented ([X] of [Y])

Next: [feature name]
Questions coming up — answer what you know, skip what you don't.
```

---

### Phase 4 — Session Complete

```
━━━ DOC-ALL COMPLETE ━━━

Documented: X features
Skipped:    Y features (already up to date)

Files created/updated:
  - ./app-docs/features/[name].mdx
  - ./app-docs/features/[name].mdx
  ...

Improvements report: ./docs/improvements.md
  ARCH suggestions: X items
  RED issues: Y items

Git: X commits
```

---

## `/ae:feature [name]` — Feature Research & Planning

**Agents active: PROD (lead), ARCH (validator)**

Read `./CLAUDE.md` and `./docs/INDEX.md` before starting.

**GIT** creates the feature branch before any work begins:
```
git checkout -b feat/[feature-name]
```

**ARCH** creates the feature folder:
```
./docs/features/[feature-name]/
  PRD.md
  EPICS.md
  STORIES.md
  PROGRESS.md
  /reviews/
```

---

### Stage 1: Research & Options

**ARCH** analyzes the codebase and proposes **3 implementation approaches**:

```
ARCH — Approach Analysis: [Feature Name]

Option A: [Name]
  What: [brief description]
  Pros: [strengths]
  Cons: [weaknesses / risks]
  Complexity: S / M / L
  Recommended: yes/no — [one sentence reason]

Option B: [Name]
  ...

Option C: [Name]
  ...

ARCH's pick: Option [X] because [reason].
```

**PROD** challenges ARCH's recommendation from the user perspective:
```
PROD — Challenge:
[Does ARCH's recommendation actually serve the user well?
Any implementation shortcut that would hurt the UX?
Any option that seems simpler but creates user confusion?]
```

⚠️ **Human checkpoint:** Ask the user to pick an approach before continuing.

---

### Stage 2: PRD Generation

**PROD** generates the PRD and saves to `./docs/features/[feature-name]/PRD.md`:

```markdown
# PRD: [Feature Name]
**Status:** Draft
**Approach:** [chosen]

## Problem
[What user pain does this solve?]

## Goals
[Measurable outcomes that define success]

## Non-Goals
[Explicitly out of scope]

## User Flows
[Step-by-step user experience]

## Acceptance Criteria
- [ ] [Specific, testable criterion]

## Technical Notes
[ARCH's architecture decisions, constraints, dependencies]
```

**ARCH** reviews the PRD:
```
ARCH — PRD Review:
[Any technical constraints PROD missed?
Any acceptance criteria that are technically ambiguous?
Any scope that will be harder than it looks?]
```

⚠️ **Human checkpoint:** *"Please review PRD.md. ARCH has left notes above. Reply 'approved' when ready."*

---

### Stage 3: Story Breakdown

**PROD** writes epics to `./docs/features/[feature-name]/EPICS.md` and stories to `./docs/features/[feature-name]/STORIES.md`:

```markdown
## [Feature Name] — Stories

- [ ] STORY-XXX: [Title]
  **As a** [user], **I want** [action] **so that** [benefit]
  **Acceptance Criteria:**
  - [ ] [criterion]
  **Notes:** [technical context from ARCH]
```

**ARCH** validates story independence:
```
ARCH — Story Review:
[Any stories with hidden dependencies?
Any story too large (>2hrs)?
Any missing story the breakdown overlooks?]
```

Stories must be: independent, small (≤2hrs), and testable.

**PROD** outputs a final summary: story count and recommended starting point.

**ARCH** updates `./docs/INDEX.md` to register the new feature:
```markdown
| [feature-name] | planning | ./docs/features/[feature-name]/ |
```

**GIT** commits the planning docs:
```
chore([feature-name]): add PRD, epics and stories
```

---

## `/ae:design` — UI/UX Design

**Agents active: UX (lead), PROD (flow validator)**

Read `./CLAUDE.md` and `./docs/features/[feature-name]/PRD.md` before starting. The PRD must be approved before running this command.

**UX** reads the `Design Tool` field from `./CLAUDE.md` and confirms:
```
UX — Design Tool: [figma | pencil | none]
[One line confirming which tool will be used and why]
```

---

### Stage 1: Flow Mapping

**PROD** extracts the user flows from the PRD and lists every screen needed:

```
PROD — Screen Inventory: [Feature Name]

Screens required:
  1. [Screen name] — [purpose]
  2. [Screen name] — [purpose]
  ...

States per screen (must be designed):
  - Default / loaded
  - Loading / skeleton
  - Empty state
  - Error state
  - [any feature-specific states]
```

**UX** reviews and challenges the list:
```
UX — Flow Review:
[Any screens PROD missed?
Any transition or modal that needs its own frame?
Any state that will be painful to implement without a design?]
```

⚠️ **Human checkpoint:** Confirm the screen list before any design work starts.

---

### Stage 2: Mobile Design

**UX** generates mobile-first mockups using the configured design tool.

Order of operations:
1. Main screens (the happy path, fully populated)
2. Empty states (first-time user, no data)
3. Loading states (skeleton screens, not spinners where possible)
4. Error states (what goes wrong and how the user recovers)
5. Modals and overlays

#### If design tool = `figma`
UX creates frames via Figma MCP. Requires Figma paid plan + MCP server configured.
```
UX — Figma Progress:
✅ [Screen] — mobile done
⏳ [Screen] — in progress
```

#### If design tool = `pencil`
UX creates frames in Pencil.dev via its local MCP server. Pencil must be running in the IDE (VS Code extension or desktop app). Design files are saved as `.pen` files in the project repo — Git-friendly and version controlled alongside code.
```
UX — Pencil Progress:
✅ [Screen] — mobile done
⏳ [Screen] — in progress
```

#### If design tool = `none`
UX produces detailed Markdown wireframe specs instead:

```markdown
## Screen: [Name]

Layout:
  - [element] at [position] — [purpose]
  - [element] at [position] — [purpose]

Interactions:
  - Tap [element] → [what happens]

States:
  - Loading: [description]
  - Empty: [description]
  - Error: [description]
```

⚠️ **Human checkpoint:** *"Mobile designs are ready. Please review in [Figma / Pencil / the specs above]. Edit anything that needs changing. Reply 'mobile approved' when ready."*

---

### Stage 3: Desktop Adaptation

**UX** extends approved mobile designs to desktop layout using the same tool.

```
UX — Desktop Notes:
[What changes from mobile to desktop for each screen?
Any layout that needs a fundamentally different treatment at wider widths?
Any mobile pattern that breaks on desktop?]
```

⚠️ **Human checkpoint:** *"Desktop designs are ready. Reply 'approved' when ready to proceed."*

---

### Stage 4: Design Handoff

**UX** produces a handoff spec saved to `./docs/specs/[feature-name]-design.md`:

```markdown
# Design Handoff: [Feature Name]

## Design Tool
[Figma | Pencil | Markdown specs]

## Link / Location
[URL if Figma or Pencil — or "see specs below" if none]

## Screens
| Screen | Mobile Frame | Desktop Frame | States covered |
|--------|-------------|---------------|----------------|
| [name] | [link/ref]  | [link/ref]    | default, empty, error, loading |

## Design Tokens Used
- Colors: [list any new tokens, or "uses existing system"]
- Typography: [same]
- Spacing: [same]

## Interaction Notes
- [anything non-obvious about transitions or animations]

## Open Questions
- [anything left for the developer to decide]
```

**PROD** signs off:
```
PROD — Handoff Review:
[Does this design cover every user flow in the PRD?
Any acceptance criterion that the design doesn't address?]
```

After approval, prompt: *"Design complete. Run `/ae:implement` to start backend, then `/ae:frontend` to build the UI from these designs."*

---

## `/ae:implement` — Implement Next Story

**Agents active: ARCH (planning), PROD (validation)**

Read `./CLAUDE.md`, `./docs/INDEX.md` and the current feature folder `./docs/features/[feature-name]/STORIES.md` and `PROGRESS.md` before starting.

### Steps

1. **PROD** finds the next unchecked story. Confirms with the user (or offers to skip to a specific one).

2. **ARCH** generates an implementation plan:

```
ARCH — Implementation Plan: STORY-XXX

Files to create:
  - [path] — [purpose]

Files to modify:
  - [path] — [what changes]

Functions / components:
  - [name] — [what it does]

Test plan:
  - [scenarios to cover]

Edge cases:
  - [case 1]

Risks:
  - [anything that could go wrong]
```

**PROD** reviews the plan:
```
PROD — Plan Review:
[Does this plan deliver all acceptance criteria?
Any criterion ARCH's plan doesn't address?]
```

⚠️ **Human checkpoint:** Show both. Ask: *"Reply 'go' to start implementation."*

3. Implement following ARCH's plan. Write tests alongside code.

4. **PROD** validates against each acceptance criterion:
```
PROD — Acceptance Check:
- [ ] Criterion 1: met / not met — [evidence]
- [ ] Criterion 2: met / not met — [evidence]
```

5. Update docs:
   - Mark story `- [x]` in `STORIES.md`
   - Append to `PROGRESS.md`:

```markdown
## STORY-XXX: [Title] — [date]
- Files changed: [list]
- Tests added: [what's covered]
- Notes: [anything notable]
```

6. Prompt: *"Story complete. Run `/ae:review` before moving to the next story."*

---

## `/ae:review` — Multi-Agent Code Review

**Agents active: RED, REQ, TEST, DOC**

Read `./CLAUDE.md` and `./docs/features/[feature-name]/PROGRESS.md` to identify the last completed story.

Each agent reports independently. RED doesn't soften findings because TEST found issues.
DOC doesn't repeat what REQ said. Genuine separation of concerns.

---

**RED — Bug Hunt 🔴**

```
RED — Bug Hunt: STORY-XXX

CRITICAL (must fix before next story):
1. [Issue] — [file:line] — [why] — [fix plan]

WARNINGS (fix soon):
1. [Issue] — [file:line] — [why] — [fix plan]

CLEAN: [areas RED reviewed and found nothing suspicious]
```

---

**REQ — Requirements Audit ✅**

```
REQ — Requirements Audit: STORY-XXX

✅ [Criterion] — MET — [evidence: file/function]
❌ [Criterion] — NOT MET — [what's missing] — [fix plan]
⚠️ [Criterion] — PARTIAL — [what's there vs. what's missing]

Summary: X/Y criteria fully met.
```

---

**TEST — Coverage Review 🧪**

```
TEST — Coverage Report: STORY-XXX

Covered well:
- [scenario] — [test location]

Missing coverage:
- [scenario] — [why it matters] — [suggested test]

Test quality issues:
- [test name]: [what it claims to test vs. what it actually tests]

Verdict: [honest assessment — would this suite catch real regressions?]
```

---

**DOC — Consistency Check 📖**

```
DOC — Consistency Report: STORY-XXX

Aligned with CLAUDE.md:
- [what's consistent]

Drift detected:
- [what doesn't match] — [what CLAUDE.md requires] — [fix plan]

Docs to update:
- [anything now out of date]
```

---

**Consolidated output after all 4 agents:**

```
━━━ CONSOLIDATED FIX LIST ━━━

Blockers (fix before next story):
1. [issue + source agent]

Should-fix (fix soon):
1. [issue + source agent]

Won't-fix (logged, not blocking):
1. [issue + reason]
```

Save full review to `./docs/features/[feature-name]/reviews/STORY-XXX-review.md`.

Ask: *"Should I fix the blockers now, or do you want to review them first?"*

---

## `/ae:ship` — Full Story Chain

**Chains: implement → review → frontend → review**

Use this after `/ae:design` is approved and you're ready to build a story end-to-end
without manually triggering each step.

### Flow

**Phase 1 — Backend**
Run the full `/ae:implement` flow for the next unchecked story.
- ARCH generates implementation plan
- PROD validates against acceptance criteria
- ⚠️ **Single human checkpoint:** Show both plans. Ask: *"Reply 'go' to start the full ship chain."*
- On 'go': implement with tests, update PROGRESS.md and STORIES.md
- **GIT** commits:
```
feat([feature-name]): STORY-XXX — [story title]
test([feature-name]): STORY-XXX — add tests
```

**Phase 2 — Backend Review** *(automatic, no pause)*
Run the full `/ae:review` flow immediately after implementation.
- RED, REQ, TEST, DOC each run their pass
- Produce consolidated fix list

If **blockers** are found → **pause and surface them:**
```
⚠️ SHIP PAUSED — blockers found by [agent]

[consolidated blocker list]

Fix these now? Reply 'fixed' to continue the chain, or 'abort' to stop.
```
If blockers were fixed → **GIT** amends or commits the fixes:
```
fix([feature-name]): STORY-XXX — address review blockers
```
If no blockers → continue automatically.

**Phase 3 — Frontend** *(automatic after clean review or 'fixed')*
Run the full `/ae:frontend` flow.
- UX reads design handoff spec
- ARCH plans components
- PROD validates flow
- Implement pixel-faithful to designs
- **GIT** commits:
```
feat([feature-name]): STORY-XXX — frontend implementation
```

**Phase 4 — Frontend Review** *(automatic, no pause)*
Run the full `/ae:review` flow on the frontend code.
- Same 4-agent pass
- If blockers found → pause and surface, same pattern as Phase 2
- If blockers were fixed → **GIT** commits:
```
fix([feature-name]): STORY-XXX — address frontend review blockers
```

**Phase 5 — Documentation** *(automatic after clean frontend review or 'fixed')*
SCRIBE updates `./app-docs/` to reflect what was just built.
- **GIT** commits:
```
docs([feature-name]): STORY-XXX — update app docs
```

**Phase 6 — PR Description** *(automatic, generated but not pushed)*

**GIT** generates a PR description ready to copy into GitHub/GitLab:

```markdown
## STORY-XXX: [Story title]

### What changed
[Plain-English summary of what was built]

### Why
[The user story — as a X, I want Y so that Z]

### Changes
- `feat:` [backend summary]
- `feat:` [frontend summary]
- `docs:` [what was documented]

### How to test
[Steps to verify the feature works, derived from acceptance criteria]

### Checklist
- [ ] Tests pass
- [ ] Docs updated
- [ ] No review blockers outstanding
```

**Chain complete:**
```
━━━ STORY-XXX SHIPPED ━━━
Backend:  ✅ implemented + reviewed
Frontend: ✅ implemented + reviewed
Docs:     ✅ updated
Git:      ✅ committed (see log above)
PR desc:  ✅ ready to copy
Stories:  [x] marked complete
Progress: updated

Next: run `/ae:ship` again for STORY-XXX+1, or `/ae:status` to review the board.
```

### Documentation rules (SCRIBE)

After every successful ship, SCRIBE:

1. Checks `./app-docs/features/` for an existing MDX file for this feature.
   - If it exists → update it
   - If not → create `./app-docs/features/[feature-name].mdx`

2. Each feature MDX follows this structure:

```mdx
---
title: [Feature Name]
description: [One sentence — what this feature does for the user]
status: stable | beta | deprecated
last_updated: [date]
---

# [Feature Name]

[2-3 sentence plain-English overview. Written for a new team member on day one.]

## What it does

[User-facing description. No code. What does the user experience?]

## How it works

[Technical overview. Key files, key functions, data flow. Enough for a developer
to orient without reading the code first.]

## Key files

| File | Purpose |
|------|---------|
| `[path]` | [what it does] |

## Edge cases & known behaviour

[Anything non-obvious. Error states, limits, gotchas.]

## Related features

[Links to other feature MDX files this connects to, if any]
```

3. Updates `./app-docs/index.mdx` if a new feature was added (append to the features list).

4. SCRIBE's self-check before finishing:
```
SCRIBE — Docs Update:
✅ Created / updated: [file path]
✅ Readable by a new team member: yes/no — [note if no]
✅ Useful as AI context: yes/no — [note if no]
✅ index.mdx updated: yes / not needed
```

### What still requires your input
- The single "go" at the start (you're approving the full plan upfront)
- Any blocker pause mid-chain
- Nothing else — warnings and non-blockers are logged to the review file, not surfaced during the chain

---

## `/ae:fix [description]` — Bug Fix Chain

**Chains: diagnose → fix → review**
**Agents active: FIXER (lead), RED (reviewer)**

Read `./CLAUDE.md` and any relevant feature docs in `./app-docs/features/` before starting.

**GIT** confirms the current branch before starting. If on `main`/`master`, warns the user:
```
⚠️ GIT: You're on main. /ae:fix expects to run on a feature branch.
Are you fixing a pre-merge bug? Reply 'yes' to continue on main, or switch to the relevant branch first.
```
Otherwise proceeds on the current branch silently.

### Steps

**Phase 1 — Diagnosis**

FIXER takes the bug description and investigates:

```
FIXER — Diagnosis: [bug description]

Reproduction path:
  [How does this bug occur? What triggers it?]

Root cause:
  [Exact file(s) and line(s) where the problem originates]
  [Why does it behave this way?]

Blast radius:
  [What else could be affected by this bug or by fixing it?]

Fix plan:
  [Exactly what will change — file, function, line-level detail]
  [What will NOT change — FIXER explicitly lists scope boundaries]

Risk:
  [Could this fix break anything else?]
```

⚠️ **Human checkpoint:** Show diagnosis. Ask: *"Does this match what you're seeing? Reply 'go' to fix."*

**Phase 2 — Fix** *(automatic after 'go')*

FIXER applies the minimal surgical fix. Rules:
- Change only what the diagnosis identified
- No refactoring unrelated code
- No "while I'm here" improvements
- Add or update a test that would have caught this bug

**Phase 3 — Review** *(automatic)*

RED runs a focused review on the changed code only:

```
RED — Fix Review:

Does the fix actually resolve the root cause? [yes/no — explanation]
Does the fix introduce any new risks? [yes/no — detail]
Is the test sufficient to prevent regression? [yes/no — detail]
Blast radius check: [anything adjacent that should be re-tested?]
```

If RED raises concerns → pause and surface them:
```
⚠️ FIX PAUSED — RED has concerns
[RED's findings]
Proceed anyway? Reply 'override' or 'revise'.
```

If clean → continue automatically.

**Phase 4 — Docs update** *(automatic)*

SCRIBE checks if the bug touched any documented behaviour in `./app-docs/`:
- If yes → update the relevant MDX to reflect correct behaviour or add an edge case note
- If no → logs "no doc update needed"

**GIT** commits everything:
```
fix([scope]): [short description of what was broken and how it's fixed]
test([scope]): add regression test for [bug description]
docs([scope]): update edge case notes    ← only if docs were changed
```

**GIT** outputs a note for the existing PR (not a new PR description):
```markdown
### Fix applied to this PR

**What was broken:** [plain-English bug description]
**Root cause:** [one line]
**Changed:** [files]
**Regression test:** [name/location]
```

**Fix complete:**
```
━━━ FIX COMPLETE ━━━
Bug:      [description]
Root cause: [one line]
Changed:  [files]
Test:     ✅ added / updated
Docs:     ✅ updated / not needed
Git:      ✅ committed on [branch name]
```

---

## `/ae:ship-all` — Ship All Unchecked Stories

**Loops `/ae:ship` across every unchecked story across all active features**

Read `./docs/INDEX.md` to identify in-progress features, then scan their `STORIES.md` files for unchecked stories.

Use when you want to build out all remaining stories in a feature without manually
triggering `/ae:ship` each time. You stay in the loop — every story pauses for plan
approval before code is written. Only the mechanical chaining is automatic.

---

### How it runs

**On start**, PROD gives you a session overview:

```
PROD — Ship-All Session: [Feature Name]

Stories to ship: X
  1. STORY-XXX: [title]
  2. STORY-XXX: [title]
  ...

You'll approve each implementation plan before it runs.
Reply 'go' to start, or 'stop' at any plan prompt to end the session.
```

---

**For each story**, the loop runs:

**Step 1 — Plan** *(always pauses)*

ARCH and PROD generate the implementation plan as in `/ae:ship`.

```
━━━ STORY-XXX ([X] of [Y]) ━━━

ARCH — Implementation Plan:
[plan]

PROD — Plan Review:
[validation]

Reply 'go' to ship · 'skip' to skip this story · 'stop' to end session
```

**Step 2 — Ship chain** *(runs automatically on 'go')*

Runs the full `/ae:ship` chain for this story:
implement → review → frontend → review → docs → git commits

Pauses only if review blockers are found, same as `/ae:ship`.

**Step 3 — Story complete summary**

```
✅ STORY-XXX shipped ([X] of [Y] done)
[1 line of what was built]

Moving to next story...
```

---

### Session complete

```
━━━ SHIP-ALL COMPLETE ━━━

Shipped:  X stories
Skipped:  Y stories
Stopped:  [early / no — ran to completion]

DONE ✅
- STORY-XXX: [title]
- STORY-XXX: [title]

SKIPPED ⏭
- STORY-XXX: [title] — [reason if given]

REMAINING 🔜
- STORY-XXX: [title] — [if stopped early]

Git: [X] commits on [branch]
PR desc: ✅ updated to cover all shipped stories
```

**GIT** generates a single PR description covering all stories shipped in the session,
not one per story.

---

### Guardrails

- **Never skips plan approval.** The 'go' prompt is non-negotiable between stories.
- **Blocker pauses propagate.** If a review finds blockers mid-chain, the session pauses exactly as in `/ae:ship`. After fixing, the session resumes from where it stopped.
- **'stop' is always available** at any plan prompt — it ends the session cleanly without abandoning in-progress work.
- **Skipped stories stay unchecked** in `STORIES.md` so `/ae:status` reflects reality.

---

## `/ae:status` — Progress Overview

**Agent active: PROD**

Read `./docs/INDEX.md` first, then scan all `./docs/features/*/STORIES.md` and `PROGRESS.md` files to build a complete picture across all features.

```
━━━ PROJECT STATUS ━━━

Features: X total

[Feature Name] — in-progress
  Completed: X / Y stories
  DONE ✅   STORY-001: [title]
  UP NEXT 🔜 STORY-002: [title] ← recommended next
  BLOCKED ⚠️ STORY-003: [reason]

[Feature Name] — complete ✅
  All X stories shipped

[Feature Name] — planning 📋
  Stories not yet created — run /ae:feature [name] to start

ARCH NOTE: [any cross-feature technical concerns?]
```

---

## `/ae:frontend` — Frontend Implementation

**Agents active: ARCH (structure), UX (fidelity check), PROD (UX validation)**

Read `./CLAUDE.md`, the target story, and `./docs/specs/[feature-name]-design.md`.
If `/ae:design` hasn't been run yet, prompt the user to run it first or confirm they want to proceed without designs.

### Steps

1. **UX** reads the design handoff spec and summarises what needs to be built:
```
UX — Design Brief: STORY-XXX
[Key screens and states this story covers]
[Any interaction notes from the handoff spec]
[Anything the developer needs to watch out for]
```

2. **ARCH** audits the existing design system and lists what's available to reuse vs. what needs building:

```
ARCH — Frontend Plan: STORY-XXX

Reuse:
  - [component] from [path]

Build new:
  - [component] — [props, variants, states needed]

Data connections:
  - [API call] → [expected shape]

Responsive:
  - [mobile / tablet / desktop notes from UX handoff]
```

3. **PROD** reviews the plan against user flow:
```
PROD — UX Review:
[Does this deliver every screen and state in the design handoff?
Any interaction state missing — loading, empty, error?
Any shortcut that would diverge from the approved design?]
```

⚠️ **Human checkpoint:** Show all three agents. Ask: *"Reply 'go' to implement."*

4. Implement following ARCH's plan, pixel-faithful to the design handoff.

5. **UX** does a final fidelity check:
```
UX — Fidelity Check:
[Does the implementation match the designs?
Any spacing, color, or interaction that drifted from the spec?
Any state that's missing or broken?]
```

6. **PROD** does a final UX spot-check:
```
PROD — Final Check:
[Does the overall experience feel right end-to-end?
Anything that works technically but feels wrong to use?]
```

---

## Core Principles (Always Enforced)

1. **Never skip a human checkpoint.** Every gate exists for a reason.
2. **Agents challenge each other.** PROD challenges ARCH. RED assumes failure. This tension is the point.
3. **One story at a time.** No batching.
4. **Tests are not optional.** Done = implemented + tested.
5. **Docs stay in sync.** PROGRESS.md, STORIES.md, and reviews must reflect reality.
6. **Plan before code.** ARCH shows a plan. PROD validates it. Then you build.
