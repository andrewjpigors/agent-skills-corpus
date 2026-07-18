---
name: project-init
description: "Universal multi-agent bootstrap for ANY project. Auto-detects project type, interviews the user, generates matching agents/skills/rules/hooks. Supports predefined profiles (game, web, mobile, api, cli, library) and dynamic generation for any domain (trading, data science, content, research, etc.)."
argument-hint: "[--type <type>] [--team solo|small|large] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion
model: sonnet
---

When this skill is invoked, it bootstraps a complete multi-agent development environment for the current project — of ANY type.

---

## 0. Core Principle

This skill works for **any domain**, not just software. The key insight:

1. **Predefined profiles** exist for common software types (game, web-app, mobile-app, api-service, cli-tool, library) — these give fast, accurate configuration.
2. **Dynamic profile generation** handles everything else — the AI interviews the user about their domain, infers the needed roles and workflows, and generates a custom agent team from scratch.

Both paths converge at the same output: a fully configured `.claude/` infrastructure with agents, skills, hooks, rules, and coordination docs.

---

## 1. Detect Existing Configuration

Before doing anything, check if a multi-agent setup already exists:

```
Glob ".claude/agents/*.md"
Glob ".claude/skills/*/SKILL.md"
Read "CLAUDE.md" (if exists)
Read ".claude/config-meta.json" (if exists)
```

If `.claude/agents/` already contains 3+ agent files:
> AskUserQuestion: "This project already has a multi-agent configuration (N agents, M skills). What would you like to do?"
> - Options: "[A] Reconfigure — start fresh (existing files backed up)" / "[B] Extend — keep existing, add missing" / "[C] Evolve — switch project phase (e.g. prototype→production)" / "[D] Cancel"

If [C]: run the **Evolution Mode** flow (see Section 8). If [D]: exit. If [B]: run `/expand-team` logic instead. If [A]: back up `.claude/` to `.claude.backup.[timestamp]/`.

---

## 2. Phase 1 — Detection (Read the Project)

Scan the project directory to auto-detect characteristics. Run ALL scans before asking questions.

### 2a: Project Type Detection (Predefined Profiles)

For each predefined profile, scan for its `detect_signals`:

```
Read profiles/game.md
Read profiles/web-app.md
Read profiles/mobile-app.md
Read profiles/api-service.md
Read profiles/cli-tool.md
Read profiles/library.md
```

For each profile's signals, use Glob to count matches in the project root.

### 2b: General Project Signals

Also scan for general indicators that help characterize ANY project:

```
Glob "*.md" (root — README, docs)
Glob "*.py" / "*.ipynb" (data science, scripting)
Glob "*.json" / "*.yaml" / "*.toml" (config-heavy projects)
Glob "*.csv" / "*.xlsx" / "*.parquet" (data projects)
Glob "*.sql" / "migrations/" (database projects)
Glob "Makefile" / "Taskfile*" / "justfile" (build systems)
Glob "LICENSE" / "CHANGELOG*" (open-source library signals)
Glob ".github/" / ".gitlab-ci*" (CI/CD)
Glob "Dockerfile" / "docker-compose*" (containerized)
Glob "data/" / "notebooks/" / "scripts/" (data/analysis projects)
Glob "*.html" / "*.css" (web frontend)
Glob "*.sol" / "hardhat*" / "foundry*" (blockchain)
Glob "*.tex" / "*.bib" (academic/latex)
Glob "backend/" / "frontend/" / "miniprogram/" (multi-tier projects)
```

### 2c: Content Analysis

If a README.md exists, read it to understand the project's purpose.
If any existing docs exist (docs/, DESIGN.md, etc.), skim them for domain clues.

### 2d: Present Detection Results

```
## Project Detection Results

**Best match**: {{type}} ({{confidence}} — {{N}}/M signals matched)
  OR: **No predefined profile matches well** — will generate a custom profile

**Language**: {{lang}}
**Framework**: {{framework or "none detected"}}
**Domain clues**: {{extracted from README/content}}
**Existing config**: {{.claude/ exists?}}
```

---

## 3. Phase 2 — Interview (Understand the Domain)

This is where the skill becomes universal. The interview adapts based on whether a predefined profile matched.

### 3a: If Predefined Profile Matched (High Confidence)

AskUserQuestion with streamlined questions:

**Q1**: "Detected: **{{type}}** project. Is this correct?"
- Options: "{{type}} (Recommended)" / "It's something else" / "It's a mix"

**Q2**: "Team mode?"
- Options: "[A] Solo (Recommended)" / "[B] Small team (2-5)" / "[C] Large team (5+)"

**Q3**: "Collaboration style?"
- Options:
  - "[A] Hierarchical — Director → Lead → Specialist (Recommended for complex projects)"
  - "[B] Panel —平等评审, multiple experts review each decision"
  - "[C] Pipeline — linear stages, each agent handles one phase"
  - "[D] Flat — minimal hierarchy, agents collaborate freely"

**Q4**: "Review intensity?"
- Options: "[A] Lean (Recommended)" / "[B] Full" / "[C] Solo (no reviews)"

**Q5**: "Key focus areas?" (multi-select)
- Options vary by profile (e.g., Performance, Security, UX, Testability, Rapid iteration, Documentation)

If Q1 answer is "It's something else": skip to 3b (Dynamic Profile).

### 3b: If No Profile Matched OR User Says "Something Else" — DYNAMIC PROFILE GENERATION

This is the universal path. The AI interviews the user about their specific domain to build a custom agent team.

#### Step 1: Understand the Domain

AskUserQuestion (up to 4 questions at once):

**Q1 — What is this project?**
"Describe what this project does in one sentence. For example: 'A stock trading signal system', 'A personal finance tracker', 'A research paper writing pipeline', 'A content creation workflow'."
- Free text input via AskUserQuestion (Other option)

**Q2 — What are the main work areas?**
"What distinct types of work does this project involve? Pick all that apply."
- Options (domain-agnostic list):
  - "Data analysis / Processing"
  - "Strategy / Decision making"
  - "Content creation / Writing"
  - "Code / Engineering"
  - "Research / Investigation"
  - "Design / Creative"
  - "Operations / Deployment"
  - "Communication / Marketing"
- Multi-select: true

**Q3 — Team mode?**
- Options: "[A] Solo (Recommended)" / "[B] Small team (2-5)" / "[C] Large team (5+)"

**Q4 — What quality checks matter?**
"What would you want agents to review or validate?"
- Options:
  - "Correctness — logic, calculations, data accuracy"
  - "Strategy — decisions, risk assessment, alternatives"
  - "Quality — code quality, writing quality, design quality"
  - "Compliance — rules, regulations, standards"
  - "Performance — speed, efficiency, cost"
- Multi-select: true

#### Step 1b: Collaboration Style

AskUserQuestion: "How should agents work together?"
- Options:
  - "[A] Hierarchical — clear chain of command, top-down delegation (Recommended)"
  - "[B] Panel —平等评审, experts independently review and score"
  - "[C] Pipeline — linear stages, agent per phase"
  - "[D] Flat — agents collaborate freely, no strict hierarchy"

#### Step 2: Deep-Dive on Selected Work Areas

For each selected work area, ask follow-up questions to identify specific roles needed.

**If "Data analysis / Processing" selected:**
AskUserQuestion: "What kind of data work?"
- Options: "Financial/trading data" / "Scientific/research data" / "User/behavioral data" / "Content/media data" / "Operational metrics" / "Other"

**If "Strategy / Decision making" selected:**
AskUserQuestion: "What kind of decisions?"
- Options: "Investment/trading decisions" / "Product/feature decisions" / "Resource allocation" / "Risk management" / "Prioritization" / "Other"

**If "Code / Engineering" selected:**
AskUserQuestion: "What engineering work?"
- Options: "Backend/API" / "Frontend/UI" / "Data pipelines" / "Automation/scripts" / "Infrastructure" / "Other"

**If "Content creation / Writing" selected:**
AskUserQuestion: "What kind of content?"
- Options: "Documentation" / "Marketing/copy" / "Technical writing" / "Creative/narrative" / "Reports/analysis" / "Other"

#### Step 3: Infer the Agent Team

Based on ALL answers, dynamically compose an agent team. The inference logic adapts to the selected collaboration mode:

**For Hierarchical mode** (default):
1. **One Director agent** always — the overall project authority
   - Name derived from domain: "trading-director" for trading, "research-lead" for research, etc.
   - Model: opus if stakes are high (financial, medical), sonnet otherwise

2. **One Lead per selected work area**:
   - Data analysis → "data-analyst" or "quant-analyst" (if financial)
   - Strategy → "strategist" or "risk-analyst" (if financial)
   - Code → "tech-lead"
   - Content → "content-lead"
   - Research → "research-lead"
   - Design → "design-lead"
   - Operations → "ops-lead"

3. **Specialists derived from deep-dive answers**:
   - Financial data → "market-analyst", "data-engineer"
   - Trading decisions → "signal-analyst", "risk-manager"
   - Data pipelines → "pipeline-dev", "data-engineer"
   - Documentation → "technical-writer"
   - Reports → "report-analyst"

4. **Quality agents based on Q4 answers**:
   - Correctness → "validator" or "fact-checker"
   - Strategy → "devil's-advocate" (adversarial reviewer)
   - Quality → "reviewer" or "critic"
   - Compliance → "compliance-auditor"
   - Performance → "optimizer"

**For Panel mode**:
- All agents are平等 tier — no Director/Lead/Specialist hierarchy
- Each agent is an independent expert reviewer
- A "moderator" agent synthesizes opinions and presents consensus
- Each agent gets opus model for equal decision weight

**For Pipeline mode**:
- Agents are organized as sequential stages: Stage 1 → Stage 2 → ... → Stage N
- Each stage has exactly one responsible agent
- A "pipeline-orchestrator" manages flow and handoffs
- Focus on clear input/output contracts between stages

**For Flat mode**:
- Minimal structure — typically 2-4 agents maximum
- No formal hierarchy; all agents are peers
- One "coordinator" agent tracks task status
- Agents communicate directly without escalation paths

#### Step 4: Infer Skills

Based on the work areas, quality needs, and collaboration mode, generate matching skills:

**Always generate**:
- `team-{{domain}}` — a pipeline skill for the core feature workflow (see Section 7)
- `code-review` or equivalent quality check skill

**For Analysis work area** → `analyze` skill (structured data analysis workflow)
**For Strategy work area** → `strategy-review` skill (evaluate decisions with pros/cons/risk)
**For Code work area** → `code-review` skill
**For Content work area** → `content-review` skill
**For Research work area** → `deep-research` skill
**For Correctness check** → `validate` skill (cross-check facts, data, calculations)
**For Strategy check** → `adversarial-review` skill (red-team a proposal)

#### Step 5: Present the Generated Plan

```
## Custom Agent Team — {{domain}}

Based on your answers, here's the agent team I'll generate:

### Agents ({{N}} total)
| Agent | Tier | Model | Role | Why needed |
|-------|------|-------|------|------------|
{{generated table}}

### Skills ({{M}} total)
| Skill | Description | Agents used |
|-------|-------------|-------------|
{{generated table}}

### Hooks ({{H}} total)
| Hook | Trigger | Purpose |
|------|---------|---------|
{{generated table from Section 7}}

### Workflow
{{How agents collaborate — inferred from the work areas and collaboration mode}}
```

AskUserQuestion: "Generate this configuration?"
- Options: "[A] Generate all" / "[B] Adjust — let me modify" / "[C] Add more roles" / "[D] Cancel"

---

## 4. Phase 3 — Generate Files

### 4a: Create Directory Structure

```
mkdir -p .claude/agents
mkdir -p .claude/skills
mkdir -p .claude/rules
mkdir -p .claude/docs
mkdir -p .claude/hooks
mkdir -p production/session-state
```

### 4b: Generate Agents

For each agent in the plan:

1. Read the appropriate template:
   - Director-tier → `templates/agent-director.md`
   - All others → `templates/agent-minimal.md`

2. Fill the template with **domain-specific** content:
   - `{{agent-name}}` → the agent's name
   - `{{Role Title}}` → derived from domain (e.g., "Quant Analyst" for trading)
   - `{{project-description}}` → from user's Q1 answer + detection
   - `{{Responsibilities}}` → 5 specific responsibilities for this role in this domain
   - `{{reports-to}}` → from the generated hierarchy

3. Write to `.claude/agents/{{name}}.md`

**CRITICAL for dynamic profiles**: Generate REAL, domain-specific responsibilities. For a stock trading project:
- `market-analyst`: "Analyze price action patterns", "Monitor sector rotation", "Track institutional flow" — NOT generic "Analyze data"
- `risk-manager`: "Calculate position sizing via Kelly criterion", "Set stop-loss levels based on ATR", "Monitor portfolio correlation" — NOT generic "Manage risk"

**Adapt agent template based on collaboration mode**:
- **Panel mode**: Use a modified director template that includes scoring criteria instead of verdict format
- **Pipeline mode**: Each agent gets explicit input/output contract in its description
- **Flat mode**: Use minimal template but add peer coordination instructions

### 4c: Generate Skills

For each skill, read the appropriate template and fill with domain-specific workflow steps:

- **Workflow skills** → `templates/skill-workflow.md`
- **Review/gate skills** → `templates/skill-review.md`
- **Pipeline feature skills** → `templates/skill-pipeline.md` (see Section 7)

**Example for a trading project's `analyze-market` skill:**
```markdown
## 1. Load Data
Read market data files, check data freshness.

## 2. Technical Analysis
Spawn `market-analyst` via Task: analyze trend, momentum, volume signals.

## 3. Fundamental Check
Spawn `fundamental-analyst` via Task: check earnings, valuation, sector health.

## 4. Risk Assessment
Spawn `risk-manager` via Task: calculate position size, set stops, check correlation.

## 5. Synthesize
Present combined analysis with clear buy/hold/sell recommendation.
```

### 4d: Generate Pipeline Skill (if collaboration mode = Pipeline or feature-heavy project)

Generate at least one pipeline skill using `templates/skill-pipeline.md`. This skill orchestrates a complete feature development flow:

```
Phase 1: Design → domain-expert
Phase 2: Architecture → tech-lead
Phase 3: Implementation → specialists (parallel)
Phase 4: Integration → tech-lead + domain-expert
Phase 5: Validation → qa-engineer
Phase 6: Sign-off → director
```

Customize the phases and agents based on the project type. Every pipeline skill must have 4-6 phases and clear handoff criteria.

### 4e: Generate Rules

Generate domain-appropriate rules:

For **financial/trading** projects:
- No hardcoded values (use config files)
- All strategies must have backtested metrics
- Risk limits must be defined and enforced
- Every trade signal must include confidence level and stop-loss

For **data/science** projects:
- All data transformations must be reproducible
- Results must include confidence intervals
- Data sources must be cited
- Hypotheses must be stated before analysis

For **general software** projects:
- Standard coding standards based on detected language

**Also generate path-scoped rules** if the project has multiple distinct directories (e.g., `backend/`, `frontend/`, `lib/`):
- Create rule files per path scope: `rules/backend.md`, `rules/frontend.md`, etc.
- Each rule file applies only to its path scope
- Include a shared `rules/common.md` for cross-cutting concerns

### 4f: Generate Hooks

Read `templates/hooks-config.md` for the hooks generation guide. Generate hooks based on project type and collaboration mode:

**Always generate**:
1. `hooks/session-start.sh` — loads project context on session start
2. `hooks/validate-commit.sh` — pre-commit validation

**Conditionally generate**:
3. `hooks/validate-push.sh` — pre-push validation (if CI/CD detected)
4. `hooks/detect-gaps.sh` — periodic gap detection (if multi-agent team with 5+ agents)
5. `hooks/log-agent.sh` — agent activity logging (if panel or hierarchical mode)

Write each hook to `.claude/hooks/` directory. Each hook must:
- Be a bash script with `#!/bin/bash` shebang
- Include a comment block explaining what it does
- Exit 0 on success, non-zero on failure
- Include timeout handling (max 30 seconds per hook)

**Example hook generation logic**:
```
For web projects: validate-commit checks linting + test pass
For data projects: validate-commit checks data schema validity
For full-stack projects: validate-commit checks API contract sync
For all projects: session-start loads current branch, sprint status, recent changes
```

### 4g: Generate Docs

```
Write .claude/docs/coordination-rules.md
```
Read `templates/coordination-rules.md` and fill with the generated agent hierarchy. Adapt the rules to match the selected collaboration mode:

- **Hierarchical**: standard vertical delegation + conflict escalation
- **Panel**: independent review + synthesis protocol
- **Pipeline**: stage handoff contracts + rollback rules
- **Flat**: peer coordination + task tracking

```
Write .claude/docs/agent-coordination-map.md
```
Create hierarchy diagram and delegation table.

### 4h: Generate settings.json

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(git status*)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(ls *)",
      "Bash(dir *)",
      {{language-specific test runners}}
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force*)",
      "Bash(sudo *)",
      "Read(**/.env*)"
    ]
  }
}
```

### 4i: Generate CLAUDE.md

```markdown
# {{Project Name}}

{{Description from user's interview answers}}

## Domain

{{Domain description — what this project is about}}

## Technology Stack

- **Language**: {{detected or specified}}
- **Framework**: {{detected or "none"}}

## Project Structure

{{Auto-generated from directory scan}}

## Multi-Agent Team

This project uses {{N}} coordinated agents for {{domain}} work.
Collaboration mode: **{{collaboration-mode}}**

### Agents
{{List with one-line descriptions}}

### Available Skills
{{List with /commands}}

## Coordination Rules

@.claude/docs/coordination-rules.md

## Collaboration Protocol

Every task follows: **Question → Options → Decision → Draft → Approval**
- Agents must ask before writing to files
- Agents must show drafts before requesting approval

## Hooks

@.claude/hooks/
- `session-start.sh` — runs on session start
- `validate-commit.sh` — runs before commits
```

### 4j: Generate Config Metadata

Write `.claude/config-meta.json` for version tracking:

```json
{
  "version": "2.0",
  "generated_at": "{{current-timestamp}}",
  "profile": "{{profile-id or 'dynamic'}}",
  "collaboration_mode": "{{hierarchical|panel|pipeline|flat}}",
  "project_phase": "initial",
  "files": {
    "agents": [list of generated agent filenames],
    "skills": [list of generated skill directories],
    "hooks": [list of generated hook filenames],
    "rules": [list of generated rule filenames],
    "docs": [list of generated doc filenames]
  },
  "generated_by": "project-init",
  "generation_count": 1
}
```

This metadata enables:
- **Re-detection**: On re-run, know exactly which files were skill-generated vs user-created
- **Evolution tracking**: Track which phase the project is in
- **Conflict avoidance**: Don't overwrite user-modified files

### 4k: Generate Session State

```
Write production/session-state/active.md
```

---

## 5. Phase 4 — Verification & Summary

### 5a: Verification

1. Glob all expected agent and skill files — verify existence
2. Read each agent file — verify frontmatter parses correctly
3. For each skill — verify referenced agent names match generated agents
4. Verify CLAUDE.md `@` references are valid
5. Verify settings.json is valid JSON
6. Verify config-meta.json is valid JSON and lists all generated files
7. Verify each hook file starts with `#!/bin/bash` and is executable-ready
8. Verify at least one pipeline skill exists if team has 4+ agents

### 5b: Summary

```
## Multi-Agent Infrastructure Ready

**Project**: {{name}}
**Domain**: {{domain description}}
**Profile**: {{type}} {{or "Custom (dynamically generated)"}}
**Collaboration**: {{collaboration-mode}}

### Generated
- {{N}} agents in .claude/agents/
- {{M}} skills in .claude/skills/
- {{H}} hooks in .claude/hooks/
- Rules, docs, and settings configured
- Config metadata tracked in .claude/config-meta.json

### Available Commands
| Command | Description |
|---------|-------------|
{{table of /skills}}

### Hooks
| Hook | When it runs |
|------|-------------|
| session-start.sh | Session start |
| validate-commit.sh | Before commits |
{{conditional hooks}}

### Expanding
Run `/expand-team add <role>` to add more agents.
Run `/expand-team list` to see available roles.
Run `/expand-team evolve <phase>` to switch project phase.

### Getting Started
1. Try `/{{first-skill}}` to start
2. Or just describe what you need — the agents will coordinate
```

---

## 6. Collaboration Mode Details

### Hierarchical (Default)

```
[Human]
    ├── director (vision, gates)
    │   ├── lead-1 (domain A)
    │   │   ├── specialist-1
    │   │   └── specialist-2
    │   └── lead-2 (domain B)
    │       └── specialist-3
    └── ...
```

- Vertical delegation: Director → Lead → Specialist
- Conflict resolution: escalate to shared parent
- Best for: Complex multi-domain projects with clear separation of concerns

### Panel

```
[Human]
    └── moderator (synthesizes)
        ├── expert-1 (independent review)
        ├── expert-2 (independent review)
        ├── expert-3 (independent review)
        └── ...
```

- All experts independently evaluate the same artifact
- Moderator scores and synthesizes a consensus
- Best for: Research, academic, high-stakes decision projects

**Agent template adaptation**: Each expert agent gets a scoring rubric instead of implementation responsibilities. Output format includes numerical scores and structured feedback.

### Pipeline

```
[Human]
    └── orchestrator
        ├── stage-1: planner
        ├── stage-2: architect
        ├── stage-3: builder (parallel)
        ├── stage-4: integrator
        ├── stage-5: validator
        └── stage-6: closer
```

- Linear flow with clear handoff contracts
- Each stage has defined input → output
- Best for: Content production, CI/CD-like flows, sequential build processes

**Agent template adaptation**: Each agent gets explicit `Input:` and `Output:` sections defining the contract with adjacent stages.

### Flat

```
[Human]
    ├── agent-1 (peer)
    ├── agent-2 (peer)
    └── agent-3 (peer)
```

- No hierarchy; all agents are equal peers
- One coordinator tracks task status (rotating or fixed)
- Best for: Small projects (2-4 agents), brainstorming, creative exploration

**Agent template adaptation**: All agents use the minimal template with peer coordination instructions. No escalation paths.

---

## 7. Pipeline Skill Template

The pipeline skill is the most valuable generated artifact for complex features. It orchestrates agents through a structured development flow.

### Template Structure

Read `templates/skill-pipeline.md` for the full template. Key phases:

```
Phase 1: Design
  Agent: domain-expert or product-owner
  Input: requirements / user request
  Output: design document with acceptance criteria

Phase 2: Architecture
  Agent: tech-lead or architect
  Input: design document
  Output: technical spec with API contracts, data models

Phase 3: Implementation
  Agents: specialists (can run in parallel)
  Input: technical spec
  Output: code changes, files modified

Phase 4: Integration
  Agent: tech-lead or integrator
  Input: all code changes from Phase 3
  Output: integrated codebase, resolved conflicts

Phase 5: Validation
  Agent: qa-engineer or validator
  Input: integrated codebase + acceptance criteria
  Output: test results, issues found

Phase 6: Sign-off
  Agent: director or gate-keeper
  Input: all artifacts from previous phases
  Output: APPROVE / CONCERNS / REJECT verdict
```

### Per-Project Customization

Each project type should customize the pipeline:

| Project Type | Phase 1 | Phase 3 | Phase 5 |
|-------------|---------|---------|---------|
| Game | GDD design | gameplay + AI + VFX parallel | playtest |
| Web App | feature spec | frontend + backend parallel | E2E test |
| API Service | API design | endpoint + DB parallel | contract test |
| Data Science | hypothesis | data + model parallel | validation |
| Content | outline | sections parallel | editorial review |

### Handoff Criteria

Every phase transition must have explicit handoff criteria:

```markdown
## Phase N → Phase N+1 Handoff

**Phase N is complete when**:
- [ ] Output artifact exists and is non-empty
- [ ] Output passes completeness check (all required sections present)
- [ ] No BLOCKED status from any spawned agent

**Phase N+1 can start when**:
- [ ] Phase N output is available
- [ ] All dependent agents have been spawned
```

---

## 8. Evolution Mode

When the user selects "Evolve" from the existing configuration menu, the skill enters Evolution Mode. This supports switching project phases without regenerating everything.

### Supported Phase Transitions

| From | To | What changes |
|------|-----|-------------|
| `initial` | `prototype` | Relax rules, add fast-iteration hooks, reduce review strictness |
| `prototype` | `production` | Tighten rules, add full validation hooks, increase review intensity |
| `any` | `any` | Manual phase override with selective file updates |

### Evolution Flow

1. **Read current state**: Load `.claude/config-meta.json` to understand current config
2. **Ask target phase**: "What phase are you moving to?"
3. **Diff plan**: Show what will change:
   - Rules that will be added/removed/modified
   - Hooks that will be added/removed
   - Skills that will be added/removed
   - Agent configurations that will be updated
4. **Apply changes**: Update files, preserving user modifications
5. **Update config-meta.json**: Record the phase transition

### Phase-Specific Adaptations

**Prototype phase**:
- Rules: relax to "no hardcoded secrets" only
- Hooks: session-start only (skip validation hooks)
- Skills: skip review/gate skills, focus on implementation skills
- Agents: reduce review intensity, allow more autonomous operation

**Production phase**:
- Rules: full strictness, add security/compliance rules
- Hooks: all hooks enabled with strict validation
- Skills: enable all gate/review skills
- Agents: full review protocol, no autonomous file writes

---

## 9. Dynamic Profile Examples

To illustrate how dynamic generation works for non-software domains:

### Stock Trading Project

**User answers**: "A stock trading signal and portfolio management system"
**Work areas**: Data analysis, Strategy, Code
**Quality**: Correctness, Risk management
**Collaboration**: Hierarchical

**Generated agents**:
- `trading-director` (opus) — overall trading strategy authority
- `market-analyst` — technical analysis, price patterns, sector rotation
- `quant-analyst` — quantitative models, backtesting, statistical signals
- `risk-manager` — position sizing, stop-loss, portfolio correlation, drawdown limits
- `tech-lead` — system architecture, data pipelines, execution engine
- `data-engineer` — market data ingestion, cleaning, storage
- `reviewer` — validates signals against historical performance

**Generated skills**:
- `analyze-market` — multi-agent market analysis workflow
- `backtest-strategy` — backtesting pipeline with adversarial validation
- `risk-review` — portfolio risk assessment
- `signal-validate` — cross-check trading signals before execution

**Generated hooks**:
- `session-start.sh` — load portfolio status, open positions, market hours
- `validate-commit.sh` — check backtest metrics present, no hardcoded values

### Research / Academic Project

**User answers**: "A literature review and research synthesis tool"
**Work areas**: Research, Data analysis, Writing
**Quality**: Correctness, Quality
**Collaboration**: Panel

**Generated agents** (all平等 tier):
- `methodology-expert` — evaluates research methods and statistical rigor
- `domain-expert` — validates domain-specific claims and interpretations
- `writing-expert` — reviews clarity, structure, academic conventions
- `fact-checker` — verifies citations, data accuracy, logical consistency
- `moderator` — synthesizes panel reviews into consensus recommendation

**Generated skills**:
- `paper-review` — multi-expert panel review workflow
- `literature-survey` — systematic literature search and synthesis
- `methodology-audit` — research methodology validation

### Fullstack AI Project (Backend + Frontend + RAG/LLM)

**User answers**: "An e-commerce platform with AI-powered product search and chatbot"
**Work areas**: Code (Backend + Frontend), Data analysis (RAG), Design
**Quality**: Correctness, Quality
**Collaboration**: Hierarchical

**Generated agents**:
- `tech-director` (opus) — overall architecture and tech decisions
- `product-manager` — feature prioritization, scope control
- `backend-lead` — backend architecture, API design
- `frontend-lead` — web frontend + admin dashboard architecture
- `ai-lead` — RAG strategy, prompt engineering, retrieval optimization
- `db-engineer` — schema design, vector DB, indexing
- `api-developer` — RESTful endpoints, auth, validation
- `ui-developer` — page implementation, components, state management
- `rag-engineer` — embedding, retrieval, reranking pipeline
- `qa-engineer` — testing strategy, E2E, API contracts

**Generated pipeline skill** — `team-feature`:
```
Phase 1: Requirements → product-manager
Phase 2: Architecture → tech-director + relevant leads
Phase 3: Implementation → specialists (parallel per domain)
Phase 4: Integration → tech-lead (cross-domain merge)
Phase 5: Validation → qa-engineer
Phase 6: Sign-off → tech-director
```

**Generated hooks**:
- `session-start.sh` — load sprint status, current branch, recent changes
- `validate-commit.sh` — check API docs sync, DB migration files, page registration
- `validate-backend.sh` — run backend unit tests, check coverage
- `validate-frontend.sh` — run linting, check component registration
- `detect-gaps.sh` — check API contract vs implementation consistency

---

## 10. Adding New Predefined Profiles

If you frequently work on a certain type of project, add a custom profile:

1. In `profiles/`, create `my-type.md`
2. Follow the existing profile format with:
   - `detect_signals` — auto-detection patterns
   - Core agents — always-generated roles
   - Extended agents — available via `/expand-team`
   - Core skills — always-generated workflows
   - Hooks config — recommended hooks for this type
   - Hierarchy — reporting structure
3. Next run of `/project-init` will automatically match against the new profile

**Profile hooks convention**: Each profile can include a `## Hooks Configuration` section that defines:
- Which hooks are mandatory for this project type
- What each hook should validate
- Any project-type-specific validation logic

---

## 11. Hooks Reference

### Hook Types

| Type | When | Purpose | Required? |
|------|------|---------|-----------|
| `session-start` | Session begins | Load context, display status | Yes |
| `validate-commit` | Before git commit | Code quality checks | Yes |
| `validate-push` | Before git push | Pre-push validation | Optional |
| `detect-gaps` | Periodic/manual | Find missing pieces | Optional |
| `log-agent` | Agent invocation | Activity audit trail | Optional |

### Hook Template

Every generated hook follows this structure:

```bash
#!/bin/bash
# Hook: {{hook-name}}
# Trigger: {{when it runs}}
# Purpose: {{what it validates}}
# Generated by: project-init v2.0

set -euo pipefail

TIMEOUT=30  # Max seconds before hook is killed

# Run with timeout
timeout $TIMEOUT bash -c '
  # === Validation Logic Here ===
  # Exit 0 = pass, non-zero = fail
' 2>/dev/null

EXIT_CODE=$?

if [ $EXIT_CODE -eq 124 ]; then
  echo "⚠️  Hook timed out after ${TIMEOUT}s"
  exit 1
fi

exit $EXIT_CODE
```

### Project-Type Hook Presets

| Project Type | session-start | validate-commit |
|-------------|---------------|-----------------|
| Game | Load build status, active branch | Check scene files valid, no broken references |
| Web App | Load dev server status | Lint + type check + test |
| Mobile App | Load device/test status | Platform-specific build check |
| API Service | Load service health | API contract validation + migration check |
| CLI Tool | Load version info | Cross-platform compat check |
| Library | Load semver status | API surface backward compat check |
| Data Science | Load data freshness | Schema validation + reproducibility check |
| Full-stack AI | Load sprint + service status | API sync + lint + test per module |

---

## 12. Config Metadata Schema

The `.claude/config-meta.json` file tracks all generated configuration:

```json
{
  "version": "2.0",
  "generated_at": "2025-01-15T10:30:00Z",
  "profile": "web-app",
  "collaboration_mode": "hierarchical",
  "project_phase": "initial",
  "files": {
    "agents": ["tech-lead.md", "frontend-dev.md", "backend-dev.md"],
    "skills": ["feature-design", "code-review", "sprint-plan"],
    "hooks": ["session-start.sh", "validate-commit.sh"],
    "rules": ["common.md", "frontend.md", "backend.md"],
    "docs": ["coordination-rules.md", "agent-coordination-map.md"]
  },
  "user_created_files": [],
  "generated_by": "project-init",
  "generation_count": 1,
  "last_evolution": null
}
```

**Update rules**:
- `files` only lists files created by this skill
- `user_created_files` tracks files the user added manually (detected on re-run)
- `generation_count` increments on each re-generation
- `last_evolution` records the most recent phase transition
- On re-run, only update files listed in `files` — never touch `user_created_files`
