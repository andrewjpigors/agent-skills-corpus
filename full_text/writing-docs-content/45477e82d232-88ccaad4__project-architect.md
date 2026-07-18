---
name: project-architect
description: >
  Architect a new software project from scratch — interview the user about their idea,
  make design decisions, and generate lean architecture documentation and session safety
  rules for AI-assisted coding. Use this skill whenever the user wants to start a new
  project, set up a new codebase, plan an application architecture, bootstrap a repo, or
  think through how to structure a new app before coding begins. Also trigger when the
  user says things like "new project", "I want to build...", "let's start fresh", "set
  up a new app", "architect this", "plan out the structure", or any variation of starting
  something from zero. This skill front-loads architectural thinking while keeping docs
  lean enough to fit in Claude's context window.
---

# Project Architect

You are helping someone design a new software project from the ground up. Your job is to
interview them, understand what they're building, make smart architectural decisions, and
produce a lean set of documentation that future coding sessions can rely on.

Two insights drive this skill:

1. **Front-load the thinking.** Most AI-assisted projects add architecture docs reactively —
   you discover you need a domain ontology after the LLM hallucinates wrong categories,
   you add session safety rules after a file gets truncated. This skill prevents that.

2. **Keep docs thin at the start.** At project kickoff you know the LEAST about your
   project. Bloated Day 1 docs waste Claude's context window on speculation. Start with
   lean skeletons — decisions and constraints only — and grow them as the project reveals
   what actually matters.

## Context Window Management

This is the most important principle in the skill. Every `.md` file you generate will be
read by Claude at the start of future coding sessions. Claude's context window is finite.
Bloated docs mean less room for actual code, conversation, and problem-solving.

**The rule: At project start, each doc should be 30-60 lines max.**

Here's why this works:

- **Day 1 you know constraints, not details.** You know "Python backend, FastAPI, Supabase"
  but you don't know your exact middleware stack or all your Pydantic models. Write what
  you know. Leave the rest for when you build it.

- **Docs grow with the project.** Each coding session adds detail to the relevant doc.
  The CLAUDE.md Knowledge Base Monitoring rule ensures new patterns get captured as they
  emerge. By session 20, your BACKEND.md is rich and battle-tested — because it grew from
  real decisions, not upfront speculation.

- **Placeholder sections waste tokens.** A section that says "[TBD — decide during Phase 2]"
  costs tokens every session for zero value. Don't write it. Add it when Phase 2 arrives.

- **Cross-references beat duplication.** If BACKEND.md and DATABASE.md both describe the
  same table, you're paying double. Put it in one place, reference it from the other.

**Document budget for a typical project:**

| Doc | Target lines (Day 1) | Grows to |
|-----|---------------------|----------|
| CLAUDE.md | 40-70 | 70-100 (mostly stable) |
| MEMORY.md | 15-25 | Grows every session (most valuable by session 20) |
| IMPLEMENTATION_ROADMAP.md | 40-60 | Updates per phase |
| DOMAIN_ONTOLOGY.md | 30-50 | Grows with domain discovery |
| AI_STRATEGY.md | 30-50 | Grows with prompt iteration |
| BACKEND.md | 30-50 | Grows with services |
| FRONTEND.md | 30-50 | Grows with components |
| DATABASE.md | 20-40 | Grows with tables |
| SECURITY.md | 20-30 | Grows with implementation |

**Total Day 1 budget: ~300 lines across all docs.** That's roughly 6-8K tokens — leaving
plenty of room in Claude's context for actual coding work.

## The Interview

Start by understanding the project. Use AskUserQuestion to make this conversational, not
interrogative. The goal is to understand the *why* before the *what*.

### Round 1: The Vision (always ask these)

Ask 3-4 questions in a single AskUserQuestion call:

1. **What are you building?** — Get the elevator pitch. What problem does it solve, who
   is it for, what makes it different?

2. **How will people use it?** — Web app, mobile app, CLI tool, API service, desktop app?
   Single user or multi-user? Real-time collaboration needed?

3. **Does this project use AI/LLM?** — If yes, how central is it? Core product or feature?

4. **What's your experience level and preferred stack?** — Seasoned developer with stack
   preferences, or newer and want recommendations?

### Round 2: Adaptive Deep Dive

Based on Round 1 answers, ask 3-5 targeted follow-ups. Only go deep where it matters.

**If it's a web app:**
- Core screens/pages and main user flow?
- Auth approach? (email/password, OAuth, magic links, anonymous-first?)
- What data needs to persist? Core domain model in plain language?

**If it uses AI/LLM:**
- What does the AI do? (Generate, classify, extract, summarize, converse?)
- What inputs/outputs? Structured JSON or free text?
- Quality vs speed vs cost priority?

**If it's an API/backend service:**
- Who consumes it? Scale expectations? Compliance requirements?

**If the user is newer to development:**
- Budget for hosting? Want to learn a tech or want fastest path?

**For any project:**
- From-scratch or integrating with existing systems?
- Timeline? MVP in a week vs production over months?
- Strong opinions on specific tools to use (or avoid)?

### Round 3: Confirmation

Summarize your proposed architecture concisely — stack choices, major components, data
flow. Ask if it captures their vision using AskUserQuestion:
- "This looks right, generate the docs"
- "Mostly right, but I want to adjust..."
- "Let me clarify a few things"

## Deciding What Docs to Generate

Not every project needs every document. Use this decision framework:

### Always Generate

- **CLAUDE.md** — Session safety rules. Non-negotiable.
- **MEMORY.md** — Self-improving preferences file. Compounds across sessions.
- **IMPLEMENTATION_ROADMAP.md** — Phased build plan. Prevents scope creep.

### Generate Based on Project Shape

| Document | Generate when... |
|----------|-----------------|
| **AI_STRATEGY.md** | Project uses AI/LLM meaningfully |
| **DOMAIN_ONTOLOGY.md** | Project has domain concepts needing shared definitions |
| **BACKEND.md** | Project has server-side code |
| **FRONTEND.md** | Project has a user-facing interface |
| **DATABASE.md** | Project persists data beyond simple file storage |
| **API_CONTRACT.md** | Frontend and backend are separate |
| **SECURITY.md** | Handles user data, auth, payments, or compliance |
| **DEVOPS.md** | Needs CI/CD, deployment config, or infrastructure-as-code |

### Skip When Not Needed

A CLI tool doesn't need FRONTEND.md. A static site doesn't need AI_STRATEGY.md.
Don't generate docs just to have them.

## Generating the Documents

Generate docs in this order (each later doc can reference earlier ones):

**Phase 1: Architecture Docs**

1. CLAUDE.md first
2. MEMORY.md (always — starts near-empty, grows with sessions)
3. DOMAIN_ONTOLOGY.md if needed
4. AI_STRATEGY.md if needed
5. BACKEND.md / FRONTEND.md / DATABASE.md
6. API_CONTRACT.md if needed
7. SECURITY.md / DEVOPS.md if needed
8. IMPLEMENTATION_ROADMAP.md last (references everything above)

**Phase 2: Project Scaffolding** (see "Project Scaffolding" section below)

9. Create folder structure (stack-specific)
10. Generate .gitignore (stack-specific)
11. Generate .env.example (populated with project's env vars)
12. Generate .claude/rules/file-editing.md (session safety)
13. Generate AI_HANDOFF.md (empty template)
14. Generate pre-commit config (language-specific)
15. git init + initial commit (stage specific files only)
16. Give user the remote push instructions

### The Golden Rule for Every Template Below

**Write only what you KNOW from the interview. If you're guessing, don't write it.**

Every line in a Day 1 doc should be either:
- A confirmed decision (stack choice, auth approach, core entities)
- A hard constraint (budget, timeline, compliance requirement)
- An operational rule (session safety, commit discipline)

If it's speculative, leave it out. It'll be added when the project reaches that point.

---

### CLAUDE.md Template (~40-70 lines)

The most battle-tested document. Every rule prevents a real failure. Target 40-80 lines —
CLAUDE.md is an **index** that points to other docs, not an encyclopedia. Only add rules
that prevent recurring problems. Use hooks for code style, not CLAUDE.md instructions.

See `references/claude-md-best-practices.md` for the full rationale behind these choices.

```markdown
# [Project Name] — Session Rules

## Commands

\`\`\`bash
# Build & test
[PROJECT-SPECIFIC BUILD COMMAND]
[PROJECT-SPECIFIC TEST COMMAND]

# Session startup (run before any edits)
git log --oneline -5 && git status --short && [TEST COMMAND]
\`\`\`

If tests fail on startup, stop and diagnose before doing anything else.

## Caveats

- [Stack-specific gotcha, e.g., "Svelte 5 runes, not Svelte 4 stores"]
- [Framework version constraint, e.g., "Python 3.11+, no walrus operator in tests"]

## Key Patterns

- [Core architectural pattern, e.g., "Routes → Services → Repositories, never skip layers"]
- [Data flow rule, e.g., "All AI prompts consume DOMAIN_ONTOLOGY.md enums, never hardcode"]

## Session Safety

- **Merge gate:** No branch merges to main without human E2E test and approval
- **Scope:** One component/route/service per session, max ~150 lines new code
- **Commits:** Commit immediately after green tests, never batch unrelated changes
- **File edits >100 lines:** Targeted edits only, verify with parser after each edit
- **Git:** Stage specific files (never git add -A), conventional commits, no destructive commands
- **Deletion:** Never rm files — move to .quarantine/, document in handoff

## Code Quality

[LANGUAGE-SPECIFIC HOOKS — e.g., "Pre-commit hooks enforce Black + Ruff. Run `pre-commit run --all-files` to check manually."]
Do NOT add code style rules here — hooks enforce formatting automatically.

## Handoff

End of session, prepend to AI_HANDOFF.md: Date, Task, Friction Points, Questions for Human.
When new tools/patterns emerge, propose a Knowledge Base update with: name, date, what, impact.

## Path-Specific Rules

Architecture details live in scoped docs, not here:
- See BACKEND.md, FRONTEND.md, DATABASE.md for stack details
- See DOMAIN_ONTOLOGY.md for shared vocabulary
- See AI_STRATEGY.md for model/prompt decisions
- See MEMORY.md for accumulated preferences and patterns
```

---

### DOMAIN_ONTOLOGY.md Template (~30-50 lines)

Only the concepts you KNOW from the interview. Not every possible enum.

```markdown
# [Project Name] — Domain Ontology

Single source of truth for domain concepts. Consumed by: [list consumers].

## [Concept 1] (e.g., User Types, Vibe Tags, Content Categories)

| Key | Label | Definition | Constraints |
|-----|-------|-----------|-------------|
| `key` | User-facing label | Precise definition | Validation rules |

## [Concept 2]

[Same format]

## Update Protocol

When ontology changes, update in same branch: [list all consumers —
DB enums, Pydantic models, TypeScript types, AI prompts, tests]
```

---

### AI_STRATEGY.md Template (~30-50 lines)

Decisions and constraints only. Prompt details come when you build prompts.

```markdown
# [Project Name] — AI Strategy

## AI's Role

[One paragraph: what AI does, how user experiences it, visible or invisible]

## Capabilities

[For each AI capability — one line each:]
- [Capability]: [input] → [output format] — [quality bar]

## Model Strategy

- Current: [model] — [why]
- Fallback: [if any]
- Cost estimate: [rough tokens/call, calls/action]

## Output Validation

- [Validation approach: Pydantic, Zod, manual checks]
- [Fallback when validation fails]

## Known Gaps

- [Things to figure out when you start building the AI layer]
```

---

### BACKEND.md Template (~30-50 lines)

Stack + layers + what each layer does. NOT method signatures.

```markdown
# [Project Name] — Backend Architecture

## Stack

[Framework], [language version], [database], [hosting target]

## Architecture

[Layer description — e.g., Routes → Services → Repositories → External APIs]

## Services

- [ServiceName]: [what it does, key dependencies]
- [ServiceName]: [what it does, key dependencies]

## External Integrations

- [Service]: [purpose] — [status: planned/stubbed/working]

## Testing

[Framework], run with: [command]. Current status: [green/not yet set up]
```

---

### FRONTEND.md Template (~30-50 lines)

```markdown
# [Project Name] — Frontend Architecture

## Stack

[Framework], [language], [styling], [build tool]

## Design Direction

[Color approach, typography, animation style — 2-3 lines max]

## Key Routes

- `/` — [purpose]
- `/[route]` — [purpose]

## State Management

- [store/context]: [what it manages]

## API Integration

[How frontend talks to backend — client approach, error handling]
```

---

### DATABASE.md Template (~20-40 lines)

Core entities only. Column details come when you write migrations.

```markdown
# [Project Name] — Data Model

## Current State

[Honest: designed but not built / stubbed / operational]

## Core Entities

- **[table]**: [purpose, key relationships]
- **[table]**: [purpose, key relationships]

## Migration Strategy

[Tool, naming convention — e.g., Supabase CLI, YYYYMMDD_description.sql]

## Security

[RLS approach, access patterns — one paragraph]
```

---

### MEMORY.md Template (~15-25 lines)

This file creates a self-improving feedback loop across sessions. It starts nearly empty
and grows as Claude discovers preferences, patterns, and lessons. By session 20, this file
is invaluable — Claude knows exactly how this human works.

```markdown
# [Project Name] — Memory

Preferences and patterns learned across sessions. Claude appends to this file
when it discovers new preferences or when the human corrects a pattern.
Do not delete entries — they represent accumulated project knowledge.

## Coding Preferences

- [Will be populated as preferences emerge during development]

## Architectural Decisions

- [Key decisions and their rationale, added as they're made]

## Patterns That Work

- [Successful approaches worth repeating]

## Things That Went Wrong

- [Failure patterns to avoid repeating — added after incidents]
```

**CLAUDE.md integration:** The CLAUDE.md template already references MEMORY.md in its
Path-Specific Rules section. The handoff rule should also include: "When you discover
a new preference or recurring pattern, append it to MEMORY.md in the same commit."

---

### IMPLEMENTATION_ROADMAP.md Template (~40-60 lines)

This is the actionable build plan. Only Phase 0 needs branch-level detail.
Later phases get one-line descriptions — they'll be detailed when you get there.

```markdown
# [Project Name] — Implementation Roadmap

## Way of Working

- Merge approval gate: human review required
- One session = one branch ≤150 lines
- Commit on green, update AI_HANDOFF.md every session

## Phase 0: Foundation [DETAIL]

- Branch 1: [specific task, ~150 lines]
- Branch 2: [specific task]
- Branch 3: [specific task]

## Phase 1: Core Features [OUTLINE]

- [Feature A]: [one-line description]
- [Feature B]: [one-line description]
- [Feature C]: [one-line description]

## Phase 2+: [PLACEHOLDER]

- [High-level goals — integration, polish, deployment]
- [Will be detailed when Phase 1 completes]

## Open Questions

- [Decisions needed before or during build]
```

---

### SECURITY.md Template (~20-30 lines)

```markdown
# [Project Name] — Security Architecture

## Auth Strategy

[Provider, flow, token lifecycle — 2-3 lines]

## Data Protection

[Encryption approach, PII handling — 2-3 lines]

## API Security

[Rate limiting, validation, CORS — 2-3 lines]

## Pre-Launch Checklist

- [ ] [Concrete item to verify]
- [ ] [Concrete item to verify]
```

---

### DEVOPS.md Template (~20-30 lines)

```markdown
# [Project Name] — DevOps

## Hosting

[Where, why, cost estimate]

## CI/CD

[Build → Test → Deploy flow]

## Environments

[Dev, staging, prod — how they differ]
```

---

### API_CONTRACT.md Template (~20-40 lines)

```markdown
# [Project Name] — API Contract

## Base URL

[e.g., /api/v1/]

## Endpoints

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| POST | /[path] | [what it does] | [yes/no] |

## Error Format

[Standard error response shape]

## Contract Sync

[How to keep frontend types in sync — e.g., auto-generated from openapi.json]
```

---

## How Docs Grow (The Progressive Disclosure Strategy)

Day 1 docs are skeletons. Here's how they fill in naturally:

**Session 1-5 (Foundation):** CLAUDE.md is mostly complete. Other docs get their first
real content as you scaffold the project. BACKEND.md gets actual service names.
DATABASE.md gets real table definitions.

**Session 5-15 (Core Features):** FRONTEND.md grows with each component built.
AI_STRATEGY.md gets real prompt architecture after you build and test your first prompt.
DOMAIN_ONTOLOGY.md gets refined when you discover edge cases.

**Session 15+:** Docs are now battle-tested. Most growth is in IMPLEMENTATION_ROADMAP.md
(Phase 2/3 details) and KNOWLEDGE_BASE.md (patterns discovered during build).

**The rule for future sessions:** When you make a significant architectural decision or
discover something that changes how the system works, update the relevant doc in the
same commit. Don't defer it — context exhaustion is real and you might not remember
in the next session.

## After Generation: The Refinement Loop

Tell the user: "I've generated lean architecture docs — these are starting points that
will grow as we build. Here's what to review first: [1-2 docs most likely to need
adjustment]."

Common Day 1 refinements:
- Domain ontology needs a concept you forgot to mention
- Roadmap Phase 0 is too ambitious (split it)
- Stack choice needs reconsidering based on a constraint you just remembered

## File Placement

Place all docs in the project root. For monorepos with separate frontend/backend
directories, shared docs (CLAUDE.md, DOMAIN_ONTOLOGY.md, ROADMAP) go at the root.

Create `.claude/` at the project root for Claude-specific config if it doesn't exist.

---

## Project Scaffolding

Docs without structure are useless. After generating architecture docs, scaffold the
actual folder structure, git repo, and safety infrastructure. This is what separates
"a pile of markdown" from "a real project."

### Scaffolding Order

Run these steps AFTER all docs are generated:

1. Create the folder structure (based on interview answers)
2. Generate `.gitignore` (stack-specific)
3. Generate `.env.example` (secrets template, never `.env` itself)
4. Generate `.claude/rules/file-editing.md` (session safety)
5. Generate `AI_HANDOFF.md` (empty template for session handoffs)
6. Generate pre-commit config (language-specific hooks)
7. `git init -b main` + initial commit with all files
8. Tell user how to connect to their remote

### Folder Structure Templates

Generate ONLY the directories relevant to the project. Not every project needs every folder.

**Python Backend (FastAPI / Flask / Django):**

```
project-name/
├── app/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── routers/             # API route handlers
│   │   └── __init__.py
│   ├── services/            # Business logic
│   │   └── __init__.py
│   ├── repositories/        # Data access layer
│   │   └── __init__.py
│   ├── models/              # Pydantic models / schemas
│   │   └── __init__.py
│   └── middleware/           # Auth, logging, etc.
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── conftest.py
├── migrations/              # DB migrations (if needed)
├── scripts/                 # One-off utility scripts
├── .claude/
│   └── rules/
│       └── file-editing.md
├── .gitignore
├── .env.example
├── .pre-commit-config.yaml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── AI_HANDOFF.md
├── CLAUDE.md
├── MEMORY.md
└── [other architecture docs]
```

**Node/TypeScript Backend (Express / Fastify / NestJS):**

```
project-name/
├── src/
│   ├── index.ts             # Entry point
│   ├── routes/              # Route handlers
│   ├── services/            # Business logic
│   ├── repositories/        # Data access
│   ├── models/              # Types and interfaces
│   └── middleware/           # Auth, logging, etc.
├── tests/
├── .claude/
│   └── rules/
│       └── file-editing.md
├── .gitignore
├── .env.example
├── package.json
├── tsconfig.json
├── AI_HANDOFF.md
├── CLAUDE.md
├── MEMORY.md
└── [other architecture docs]
```

**Frontend (React / Svelte / Vue / Next.js):**

```
project-name/
├── src/
│   ├── routes/ or pages/    # Page components
│   ├── lib/ or components/  # Shared components
│   ├── stores/ or context/  # State management
│   ├── styles/              # Global styles
│   └── utils/               # Helper functions
├── static/ or public/       # Static assets
├── .claude/
│   └── rules/
│       └── file-editing.md
├── .gitignore
├── .env.example
├── package.json
├── AI_HANDOFF.md
├── CLAUDE.md
├── MEMORY.md
└── [other architecture docs]
```

**Monorepo (separate frontend + backend):**

```
project-name/                 # Shared CLAUDE.md lives here
├── CLAUDE.md                 # Shared session rules (both repos read this)
├── MEMORY.md
├── DOMAIN_ONTOLOGY.md
├── AI_STRATEGY.md
├── IMPLEMENTATION_ROADMAP.md
├── .gitignore
├── project-backend/          # Separate git repo (or subdirectory)
│   ├── app/ or src/
│   ├── tests/
│   ├── .claude/
│   │   └── rules/
│   │       └── file-editing.md
│   ├── .gitignore
│   ├── .env.example
│   ├── .pre-commit-config.yaml
│   ├── AI_HANDOFF.md
│   ├── CLAUDE.md             # Backend-specific rules
│   ├── BACKEND.md
│   └── API_CONTRACT.md
└── project-frontend/         # Separate git repo (or subdirectory)
    ├── src/
    ├── .claude/
    │   └── rules/
    │       └── file-editing.md
    ├── .gitignore
    ├── .env.example
    ├── AI_HANDOFF.md
    ├── CLAUDE.md             # Frontend-specific rules
    └── FRONTEND.md
```

**For project types not listed above:** Adapt the closest template. The key invariants
are: source code in `src/` or `app/`, tests in `tests/`, `.claude/rules/` exists,
`.gitignore` and `.env.example` are present, architecture docs at root.

---

### .gitignore Template

Generate a `.gitignore` tailored to the stack. Always include these base entries:

```gitignore
# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp
*.swo
*~

# Secrets — NEVER commit .env
.env
.env.local
.env.*.local

# Quarantine — files moved here by AI instead of deleting
.quarantine/
```

Then add stack-specific entries:

**Python additions:**
```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.venv/
venv/
*.egg-info/
dist/
build/
.coverage
.coverage.*
htmlcov/
.pytest_cache/
.ruff_cache/
```

**Node/TypeScript additions:**
```gitignore
# Node
node_modules/
dist/
build/
.next/
.svelte-kit/
.nuxt/
package-lock.json  # Only if using yarn/pnpm — keep if using npm
```

**Both (full-stack):** Combine Python + Node sections.

---

### .env.example Template

Create `.env.example` with placeholder values. NEVER create `.env` with real secrets.

```
# Copy this file to .env and fill in real values
# cp .env.example .env

# === Required ===
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# === Optional ===
# LOG_LEVEL=info
# PORT=8000
```

Populate with the actual env vars the project will need based on the interview:
- Database URLs, API keys (Supabase, OpenAI, Stripe, etc.)
- Auth secrets (JWT_SECRET, SUPABASE_JWT_SECRET)
- Service URLs (BACKEND_URL for frontend, etc.)
- Feature flags

Each line should be commented out with a descriptive placeholder.

---

### .claude/rules/file-editing.md Template

This file prevents the #1 cause of multi-session failures: silent file truncation.
Always generate this, regardless of project type.

```markdown
# File Editing Guardrails

## The Problem

The edit tool can silently truncate files >100 lines. The file appears "saved
successfully" even though content is missing. If committed, every future session
inherits the corruption.

## Mandatory Protocol for Files >100 Lines

1. **Use targeted edits, not full rewrites.** Always use the Edit tool with a
   unique `old_string` containing 3-5 lines of surrounding context. Never use
   the Write tool on an existing file >100 lines.

2. **Verify after every edit:**

   [LANGUAGE-SPECIFIC VERIFICATION — see below]

   ```bash
   # For any file — confirm the tail looks correct:
   tail -5 path/to/file
   ```

3. **Commit on green.** One logical change → one test run → one commit.
   Do not accumulate uncommitted edits across files.

4. **If a full rewrite is unavoidable** (file already corrupted):
   - Read the existing file first
   - Write new content in a single Write call
   - Verify with `wc -l`, `tail -5`, and language parser
   - Run test suite before touching any other file

## Session Startup

Run the test suite as the very first action to detect latent corruption
before making further changes.
```

Add language-specific verification commands:

**Python:** `python -c "import ast; ast.parse(open('file.py').read()); print('OK')"`
**TypeScript:** `npx tsc --noEmit` or project's `npm run check`
**Go:** `go vet ./...`
**Rust:** `cargo check`

---

### AI_HANDOFF.md Template

```markdown
# AI Handoff Log

Prepend new entries at the top. Each session documents what changed, what broke,
and what needs human attention. Future sessions read this FIRST.

---

(No entries yet — first session will add the initial handoff report here)
```

---

### Pre-commit Hook Configuration

Generate language-appropriate pre-commit hooks. This is the "hooks over rules"
principle in action — formatting and linting are enforced by git hooks, not by
writing rules in CLAUDE.md.

**Python (.pre-commit-config.yaml):**

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 24.10.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.6
    hooks:
      - id: ruff
        args: [--fix]
```

**Node/TypeScript (package.json scripts + .prettierrc):**

Add to package.json:
```json
{
  "scripts": {
    "format": "prettier --write .",
    "lint": "eslint . --fix",
    "check": "[FRAMEWORK-SPECIFIC TYPE CHECK]"
  }
}
```

Generate `.prettierrc`:
```json
{
  "useTabs": true,
  "singleQuote": true,
  "trailingComma": "none",
  "printWidth": 100
}
```

**Go:** No pre-commit config needed — `go fmt` and `go vet` are standard.

**Rust:** `cargo fmt` and `cargo clippy` — consider `.rustfmt.toml` if needed.

---

### Git Initialization

After all files are created, initialize the repo:

```bash
# Initialize with main branch (not master)
git init -b main

# Stage ONLY project files — NEVER use git add -A or git add .
# This prevents accidentally staging parent directories or system files
git add CLAUDE.md MEMORY.md AI_HANDOFF.md .gitignore .env.example
git add .claude/
git add [other specific files and directories]

# Initial commit
git commit -m "feat: initial project architecture and scaffolding"
```

**Critical git safety rules baked into every project:**
- `git add <specific-files>` — never `git add -A` or `git add .`
- Conventional commit messages: `feat:`, `fix:`, `chore:`, `docs:`
- No destructive commands without human instruction
- One session = one logical commit
- Never merge to main without human E2E approval

Then tell the user:

```
Your project is initialized locally. To push to GitHub:

1. Create a repo at https://github.com/new (don't initialize with README)
2. Run:
   git remote add origin https://github.com/YOUR_USERNAME/PROJECT_NAME.git
   git push -u origin main
```

---

### Monorepo Git Strategy

For monorepo projects, ask during the interview:

**Option A: Single git repo** — one `.git/` at the root, both frontend and backend
in subdirectories. Simpler, good for solo devs and small teams.

**Option B: Separate git repos** — each subdirectory is its own repo. Better for
teams with separate frontend/backend workflows, CI/CD pipelines, or deploy targets.

If Option B, initialize each repo separately and put shared docs (CLAUDE.md,
DOMAIN_ONTOLOGY.md, etc.) at the parent level. The parent itself can be a repo
or just a directory — ask the user which they prefer.

## Key Principles

1. **Lean over complete.** Write what you know. Leave out what you're guessing.
   A 30-line doc with 30 lines of truth beats a 200-line doc with 170 lines of speculation.

2. **Context window is sacred.** Every line costs tokens in every future session.
   If a line isn't earning its keep, cut it.

3. **Docs grow with the project.** Day 1 docs are skeletons. Session 20 docs are rich.
   That's the intended progression.

4. **Honest about the unknown.** "Open Questions" sections are valuable. They're also
   short — just a bulleted list of decisions to make, not essays about possible answers.

5. **Actionable, not aspirational.** The roadmap contains tasks completable in one session.
   If a branch description is vague ("build the auth system"), it's too big.

6. **The user knows their domain.** You know architecture patterns. They know their
   problem space. The interview draws out domain knowledge and maps it onto solid foundations.

7. **Hooks over rules.** Code style enforcement belongs in pre-commit hooks and linters,
   not in CLAUDE.md. CLAUDE.md should reference the hook setup, not duplicate what hooks do.

8. **CLAUDE.md is an index.** It points to other docs and contains session safety rules.
   Architecture details live in scoped docs (BACKEND.md, FRONTEND.md, etc.).

9. **Memory compounds.** MEMORY.md is the only doc that grows every single session. By
   session 20 it's the most valuable file in the project — Claude knows the human's patterns.

10. **Scaffold, don't just document.** Docs without folder structure, git, and safety
    infrastructure are just markdown files. The skill creates a real project — directories,
    .gitignore, pre-commit hooks, .claude/rules/, AI_HANDOFF.md, git init — so session 1
    starts coding, not configuring.

## Reference Files

The `references/` directory contains supplementary best practices:
- `claude-md-best-practices.md` — Distilled CLAUDE.md writing principles from community
  experience. Consult this when generating or refining CLAUDE.md files.
