---
name: building-skills
description: "Help design, refine, and validate OpenClaw skills, including SKILL.md structure, workflows, and helper scripts. Use when creating or updating skills that extend the OpenClaw agent with specialized knowledge, tools, or domain workflows. Not for general code development, system administration, or content creation without skill structure focus."
---

# Skill Creator

Use this skill to design, refine, and validate OpenClaw skills (SKILL.md + scripts + optional references/assets).

---

## 1. About OpenClaw Skills

### 1.1 What a skill is

An Agent skill is a **folder on disk** containing instructions for a specific domain, with specific tools, workflows, or rules. It typically lives in either:

- `<workspace>/skills/` (per-workspace), or
- `~/.openclaw/skills/` (shared).

Minimal layout:

```text
skill-name/
├── SKILL.md          # required
├── scripts/          # optional
├── references/       # optional
└── assets/           # optional
```

A good skill:
- Describes **what** it does. Its description clearly states when it should be used.
- Encodes **domain- or project-specific knowledge** the model would not know by default
- Provides **scripts** and **verification steps** for fragile or repeated operations

### 1.2 SKILL.md frontmatter

Frontmatter is a YAML block at the top of SKILL.md, delimited by `---` lines. OpenClaw reads it when deciding which skills to include in the prompt and when they should be used.

**Example with What-When-Not pattern:**

```yaml
---
name: processing-pdfs
description: "Extract text from local PDF files. Use when working with .pdf documents and text content is required. Not for image-based PDFs; use OCR skills instead."
metadata: {"openclaw":{"emoji":"📄","requires":{"bins":["python3"]}}}
---
```

**Guidelines:**
- **name** - Hyphen-case; lowercase letters, digits, and hyphens only (e.g. `processing-pdfs`)
- **description** - Use the **What-When-Not** pattern:
  - *What* it does
  - *Use when* … (trigger conditions/keywords)
  - *Not for* … (explicit exclusions)
- **metadata.openclaw** - `emoji` (optional), `requires.bins`, `requires.env` (API keys), `requires.config`
- **user-invocable** - `true` to expose as slash command
- **disable-model-invocation** - `true` if only humans should trigger

### 1.3 Bundled resources

Use optional subfolders to keep SKILL.md focused while providing powerful tools.

**scripts/** - Executable code (Python, Bash, Node, etc.) for:
- Deterministic, fragile, or repetitive operations
- Anything where "just write the code again" would be wasteful or risky

**Best practices:**
- Scripts should be **complete and runnable**, with error handling and clear arguments
- Document required env vars or config at the top of the script
- Prefer forward-slash relative paths (`scripts/helper.py`) for portability

**references/** - Documentation and reference material that is **too large or detailed** for SKILL.md:
- Database schemas and table relationships
- API documentation and error codes
- Company policies, legal templates, or long workflow guides

**Use references when:**
- Content is long (>5-10 pages or >500-700 lines) or dense
- It's clearly optional or specialist
- Simple cases are solvable from SKILL.md, needing references only for deeper work

Each reference file should start with a **"Purpose:"** note. Reference files should NOT include a **"When to read this"** instruction — that belongs in SKILL.md. Instead, reference files should be purely informational and explicitly referenced from SKILL.md with clear conditions for when to consult them.

**Example in SKILL.md:**
```markdown
## Advanced Configuration

For multi-region deployments, read `references/multi-region.md` before proceeding. This is REQUIRED.
```

**assets/** - Files that appear in outputs or are copied/modified, but are **not loaded into context**:
- Slide templates, logo files, custom fonts
- Starter projects or boilerplate repos
- Example documents that should be edited

### 1.4 What NOT to Include

A skill should only contain essential files that directly support its functionality. Do NOT create extraneous documentation or auxiliary files:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- TROUBLESHOOTING.md

The skill is for an AI agent to use, not for human documentation. Setup procedures, user-facing docs, and development history create clutter and confuse the agent's purpose.

---

## 2. Core Design Principles

### 2.1 The Delta Principle

The agent already knows:
- Programming basics, general libraries, common patterns
- How to read/write files and call tools once told to

**Use the Delta Principle:**
- Keep only *non-obvious*, *project-specific*, or *domain-specific* knowledge in SKILL.md
- Remove tutorials, generic definitions, and "how to use a for-loop" material
- Ask for each paragraph: "Does this encode a real rule, invariant, or decision specific to this project/domain?"

### 2.2 Context Budget and "Less is More"

Treat the context window as a **finite budget**:

**Priority order:**
1. Task objective and success criteria
2. Critical constraints (invariants, safety rules)
3. Domain-specific reference that cannot be easily inferred
4. Tool descriptions and examples, only as needed

**Avoid:**
- Repeating global rules across many skills (use global config instead)
- Writing 2–3 pages where 3–5 dense sentences would do

Short, dense SKILL.md files outperform long, repetitive ones.

### 2.3 Degrees of Freedom

Match guidance to task fragility. **Freedom level determines flexibility in approach, not whether to use strong wording.**

**High freedom** (flexible approach)
- Many valid approaches; errors are cheap
- Instructions: objectives, constraints, and examples
- Strong wording is still appropriate for critical rules (e.g., "Validate user input before processing. This is REQUIRED.")
- Examples: brainstorming, writing, exploratory analysis

**Medium freedom** (guided flexibility)
- Preferred patterns exist, but variation is OK
- Instructions: recommended templates or pseudocode, with MUST rules for key steps
- Examples: report generation, data processing

**Low freedom** (strict workflow)
- Errors are costly or dangerous
- Instructions: explicit commands, hard gates, checklists with MUST/ALWAYS/NEVER language
- Examples: database migrations, infrastructure changes

**Key distinction:**
- **Freedom level** = how much flexibility is allowed in *how* to accomplish the goal
- **Strong wording** = MUST/SHOULD/ALWAYS/NEVER for critical rules — appropriate at ANY freedom level

In OpenClaw, use high freedom for **everyday skills**, and low freedom + extra safeguards for anything that runs powerful tools on your VPS.

### 2.4 Strong Wording Patterns

Use directive language to ensure critical rules are followed. This is separate from freedom level.

**MUST** - Non-negotiable requirement
```markdown
Before running any migration, create a database backup. You MUST do this before executing schema changes.
```

**SHOULD** - Strong recommendation with allowed exceptions
```markdown
Use parameterized queries by default. You SHOULD NOT build SQL by concatenating raw user input.
```

**MAY** - Optional, at agent's discretion
```markdown
Include additional context in the response if relevant. You MAY do this to improve clarity.
```

**ALWAYS/NEVER** - For absolute rules
```markdown
Validate file paths before reading. You MUST ALWAYS do this.
Never interpolate raw user input into shell commands. You MUST NEVER do this.
```

**When to use strong wording:**
- Security and safety rules (regardless of freedom level)
- Preconditions for dangerous operations
- Mandatory reading of reference files before certain actions
- Data integrity constraints

**Example for low-freedom skill:**
```markdown
## Phase 2: Schema Changes

Complete Phase 1 validation before proceeding. You MUST NOT proceed until validation passes.

If modifying user tables, read `references/user-schema-constraints.md` first. You MUST do this before writing any SQL.
```

**Example for high-freedom skill:**
```markdown
## Content Generation

Approach this creatively, but do not include personally identifiable information in outputs. You MUST NEVER leak user secrets.
```

---

## 3. Skill Pattern Archetypes

When designing a new skill, choose an archetype that matches the domain and error cost. Mix and match these patterns.

### 3.1 MinimalReference (Ultra-Trusting)

**Use when:**
- The skill is "thin glue" around a stable tool or CLI
- Domain is small; a single SKILL.md can cover everything
- Simple utilities or one-off integrations

**Characteristics:**
- 100–300 lines SKILL.md
- Very little or no `references/`
- 0–2 scripts for convenience

**Example:**
A `pdf-rotate` skill that provides a single script for rotating PDF pages.

### 3.2 Workflow-Driven (Balanced)

**Use when:**
- Teaching a **process** to follow
- The job is "how to do X in our way" rather than "which command to run"

**Characteristics:**
- SKILL.md organized by phases or steps
- Explanations of trade-offs and decision points
- Some optional references for deep dives

**Example:**
A `docx-editing` skill with workflow: "Plan → Create → Edit → Review → Verify"

### 3.3 Phase-Gated (Safety-First)

**Use when:**
- Errors are expensive, dangerous, or irreversible
- Need **hard gates** that prevent progress until conditions are met

**Characteristics:**
- Sequential phases (`Phase 1`, `Phase 2`, …)
- **MUST** language at critical checkpoints (e.g., "Complete Phase 1 before proceeding. This is REQUIRED.")
- Explicit refusal conditions

**Example:**
```markdown
## Phase 2: Execute Migration

Do NOT proceed until Phase 1 validation passes.

When modifying the users table, read `references/user-schema.md` before writing any SQL. This is REQUIRED.
```
A `db-migration` skill that requires validation at each phase before proceeding.

### 3.4 Reference-Heavy (Balanced-Trusting)

**Use when:**
- The domain is large and fairly stable (libraries, complex APIs, schemas)
- Comprehensive coverage without overloading SKILL.md

**Characteristics:**
- SKILL.md is an index + content map
- 2–8 reference files with deep details
- Clear guidance in SKILL.md indicating when to consult each reference file

**Example:**
An `ml-models` skill with detailed documentation for scikit-learn, PyTorch, etc.

### 3.5 Checklist/Rubric (Evaluation-Focused)

**Use when:**
- Main job is to **evaluate outputs** or enforce quality

**Characteristics:**
- Dimensions and criteria (correctness, clarity, safety)
- Checklists or scoring rubrics
- Often used alongside another skill that generates outputs

**Example:**
A `code-review` skill that evaluates PRs against quality dimensions.

### 3.6 Database-Access (Single-Source)

**Use when:**
- Skill fronts a **single data source or API** (DB, registry, service)

**Characteristics:**
- SKILL.md documents capabilities, query patterns, limitations
- `references/` holds schemas and API docs
- `scripts/` bundles helper scripts

**Example:**
A `warehouse-query` skill for querying an internal analytics database.

### 3.7 Domain-Doctrine (Principles)

**Use when:**
- Value is primarily **doctrine**: principles, conventions, anti-patterns

**Characteristics:**
- Strong opinions, domain-specific dos and don'ts
- Less scripting; more "how to think" in that domain
- Great for correcting harmful defaults

**Example:**
A `mobile-ux` skill that teaches mobile design principles and anti-patterns.

---

## 4. Best-Practice Toolbox

This section provides reusable patterns to apply when creating any OpenClaw skill.

### 4.1 What-When-Not Descriptions

Every `description` should clearly define:
- **What** it does
- **When** to use it (triggers)
- **Not** for (exclusions)

**Critical:** Always use a one-line description with quotes. **Never use multiline with pipe (`|`) or fold (`>`).**

**Template:**
```yaml
description: "What it does. Use when [trigger conditions or example phrasings]. Not for [explicit exclusions or edge cases]."
```

**Examples:**

PDF text extraction:
```yaml
description: "Extracts text from local PDF files. Use when working with .pdf documents and needs text content. Not for image-based PDFs; use OCR skills instead."
```

Skill validation:
```yaml
description: "Validates skills against quality standards. Use when reviewing SKILL.md structure and frontmatter. Not for general code linting or application testing."
```

### 4.2 DO/DON'T: Writing Effective Constraints

For each constraint, pair **"Don't …"** with **"Instead, …"**:

### ✅ DO

- Use gerund names like `processing-pdfs` or `analyzing-data`
- Lead with **DO** bullets ("Use X", "Prefer Y")
- Follow with **DON'T** bullets for hard boundaries
- Explain **why** the constraint exists where helpful
- Always pair negative constraints with positive alternatives

### ❌ DON'T

- Use generic names like `helper` or `misc`
- Say only "Never use vague names" without examples
- Use negative constraints without positive alternatives
- Leave "why" unstated for critical rules

**Why effective:** Paired positive/negative examples are more memorable and actionable than negatives alone.

### 4.3 Good vs Bad Examples

Side-by-side comparisons clarify the difference between correct and incorrect patterns. Use this format whenever there are common mistakes.

#### Frontmatter Descriptions

❌ **Bad:**
```yaml
description: Provides guidance for working with hooks.
```

**Why bad:** Vague, no specific trigger phrases, doesn't say when to use

✅ **Good:**
```yaml
description: "Manage OpenClaw hooks for event-driven automation. Use when user asks to 'create a hook', 'add PreToolUse hook', 'validate tool use', or mentions hook events. Not for general event handling or cron scheduling."
```

**Why good:** Follows What-When-Not pattern, specific triggers, clear boundaries

---

#### Progressive Disclosure

❌ **Bad:**
```
skill-name/
└── SKILL.md  (8,000 words - everything in one file)
```

**Why bad:** Bloats context window, detailed content always loaded even when not needed

✅ **Good:**
```
skill-name/
├── SKILL.md  (1,800 words - core essentials)
└── references/
    ├── patterns.md (2,500 words)
    └── advanced.md (3,700 words)
```

**Why good:** Progressive disclosure, detailed content loaded only when needed

---

#### Description Field Format

❌ **Bad:**
```yaml
description: >
  This skill helps with PDF processing.
  It can handle various PDF-related tasks.
  Use it when you need to work with PDFs.
```

**Why bad:** Multiline fold (`>`), harder to parse, breaks some tooling, missing What-When-Not

✅ **Good:**
```yaml
description: "Extracts text from local PDF files. Use when working with .pdf documents and needs text content. Not for image-based PDFs; use OCR skills instead."
```

**Why good:** Single-line quotes, portable, What-When-Not pattern, specific triggers

---

#### Skill Naming

❌ **Bad:**
```yaml
name: helper
name: misc
name: utils
```

**Why bad:** Generic, collisions, unclear purpose, hard to discover

✅ **Good:**
```yaml
name: processing-pdfs
name: analyzing-sales-data
name: validating-skills
```

**Why good:** Hyphen-case, descriptive, discoverable, follows gerund convention

---

#### Writing Style in SKILL.md

❌ **Bad:**
```markdown
You should start by reading the config file. (Weak second-person)
You can use grep to search. (Weak second-person)
The agent must validate input. (Third-person indirection)
```

**Why bad:** Weak second-person and third-person indirection blur who is supposed to act and are easier to ignore than direct commands.

✅ **Good:**
```markdown
Start by reading the config file. (Imperative)
Use grep to search for patterns. (Imperative)
Validate input before processing. You MUST do this. (Imperative + Strong reinforcement)
```

**Why good:** Imperative/infinitive form, direct instructions, and strong reinforcement for critical rules ensure clear and actionable guidance.

---

### 4.4 Mission + Success Criteria Pattern

For complex skills, define a mission and success criteria at the top of SKILL.md:

```markdown
## Objective
Provide a clear notion of success for a Google Calendar skill.

## Success Criteria
- Triggers only for calendar-related requests
- Supports reading, creating, and deleting events with clear user consent
- Handles API errors and rate limits with informative messages
```

This provides a clear notion of "done" and helps with verifying work.

### 4.5 Verification and Self-Checks

Build verification into every skill:

**For workflows:**
- Add a short **"Before declaring success"** checklist
- Example: "Before finishing, re-read modified files and ensure all tests pass"

**For scripts:**
- Provide a simple **test script** or instructions
- Example: "Run `scripts/verify_examples.py` with sample inputs; all checks should pass"
- Log errors clearly; avoid silent failures
- **For multiple similar scripts:** Test a representative sample rather than every single script. If 10 scripts follow the same pattern, testing 2-3 provides confidence while balancing time to completion

### 4.6 Security and Safety on VPS

Because OpenClaw can run tools on your machine or VPS, skills must handle safety explicitly:

**Minimize privileges:**
- Only depend on tools and APIs that the skill truly needs
- Avoid generic "run arbitrary shell" skills without strong constraints

**Guard dangerous actions:**
- For destructive commands (deletes, DB changes), require explicit user confirmation
- Prefer reversible operations (move to trash instead of permanent delete)

**Sanitize inputs:**
- Do not interpolate raw user text directly into shell commands
- Consider whitelisting allowed arguments or using structured options

When in doubt, treat dangerous workflows as **low-freedom** Phase-Gated or Checklist patterns.

---

## 5. Common Mistakes to Avoid

Learn from these common pitfalls when creating skills.

### Mistake 1: Weak Trigger Description

❌ **Bad:**
```yaml
description: Provides guidance for working with hooks.
```

**Why bad:** Vague, missing specific trigger phrases, and does not specify trigger conditions for skill loading.

✅ **Good:**
```yaml
description: "Manage OpenClaw hooks for event-driven automation. Use when user asks to 'create a hook', 'add PreToolUse hook', 'validate tool use', or mentions hook events. Not for general event handling or cron scheduling."
```

**Why good:** What-When-Not pattern, specific phrases users actually say, clear boundaries

---

### Mistake 2: Multiline Description Field

❌ **Bad:**
```yaml
description: >
  Extract text from PDF files.
  Use when working with documents.
  Not for images.
```

**Why bad:** Multiline fold (`>`), harder to parse, breaks some tooling

✅ **Good:**
```yaml
description: "Extract text from local PDF files. Use when working with .pdf documents and needs text content. Not for image-based PDFs; use OCR skills instead."
```

**Why good:** Single-line with quotes, portable, follows What-When-Not

---

### Mistake 3: Everything in SKILL.md (if not everything is relevant on each potential activation of the skill)

❌ **Bad:**
```
skill-name/
└── SKILL.md  (8,000 words)
```

**Why bad:** Context bloat; results in loading unnecessary information for simple tasks.
**Note:** If everything is relevant on each skill activation (no conditional logic), KEEP IT as a single SKILL.md; it becomes a good example.

✅ **Good:**
```
skill-name/
├── SKILL.md  (1,800 words)
└── references/
    └── advanced.md (3,700 words)
```

**Why good:** Progressive disclosure, details loaded only when needed

---

### Mistake 4: Generic Skill Names

❌ **Bad:**
```yaml
name: helper
name: misc
name: utils
```

**Why bad:** Collisions, unclear purpose, hard to discover

✅ **Good:**
```yaml
name: processing-pdfs
name: analyzing-sales-data
name: validating-skills
```

**Why good:** Hyphen-case, descriptive, discoverable, follows gerund convention

---

### Mistake 5: Weak or Indirect Language in SKILL.md

❌ **Bad:**
```markdown
You should start by reading the config file. (Weak second-person)
You can use grep to search. (Weak second-person)
The agent must validate input. (Third-person indirection)
```

**Why bad:** Second-person with weak verbs ("you should", "you can") is less direct and easier to ignore. It also blurs who is supposed to act. Third-person indirection ("the agent should") is equally weak and creates a sense of narration rather than instruction.

✅ **Good:**
```markdown
Start by reading the config file. (Imperative)
Use grep to search for patterns. (Imperative)
Validate input before processing. You MUST do this. (Imperative + Strong reinforcement)
```

**Why good:** Imperative/infinitive form gives direct commands. Strong second-person lines like "You MUST..." may be used to emphasize critical rules, but weak phrasing such as "you should", "you can", or "the agent must" should be avoided.

---

### Mistake 6: Missing Progressive Disclosure When Needed

❌ **Bad:**
```
api-skill/
└── SKILL.md (7,500 words - full API docs, examples, patterns)
```

**Why bad:** Results in loading full API documentation even for simple calls.

✅ **Good:**
```
api-skill/
├── SKILL.md (1,200 words - quick start, common patterns)
└── references/
    ├── api-reference.md (4,000 words - full API)
    └── examples.md (2,500 words - detailed examples)
```

**Why good:** Quick access to basics, deep docs loaded on demand

---

### Mistake 7: Unreferenced Resources

❌ **Bad:**
```markdown
# SKILL.md

[Core content]

[No mention of references/]
```

**Why bad:** References remain hidden and unusable within the current context.

✅ **Good:**
```markdown
# SKILL.md

[Core content]

## Additional Resources

### Reference Files
- **`references/patterns.md`** - Detailed patterns and techniques
- **`references/advanced.md`** - Advanced configuration

**Examples (preferred):**
- Keep small, representative examples directly in SKILL.md near the instructions they illustrate.
- For long example collections or many variants, place them in a well-named file under `references/` (for example `references/examples-advanced.md`) and link to it explicitly from SKILL.md.
```

**Why good:** Load deep examples only when necessary to keep SKILL.md focused and immediately useful.

---

### Mistake 8: Including Generic Tutorials

❌ **Bad:**
```markdown
## What is a Loop?

A loop is a programming construct that repeats code...

## How to Write a For Loop

To write a for loop, use this syntax...
```

**Why bad:** Agent already knows basic programming, wastes context

✅ **Good:**
```markdown
## Processing Workflow

Use batch processing for files over 10MB to avoid memory issues:
```bash
scripts/process_batch.py input_dir/ --batch-size 100
```
```

**Why good:** Domain-specific knowledge, follows Delta Principle

---

## 6. Skill Creation Workflow

This section defines a **high-level workflow** for creating OpenClaw skills. Adapt it accordingly.

### Step 1 – Clarify the skill's purpose with examples

**Skip this step only when:** The skill's usage patterns are already clearly understood from existing examples or direct user requirements.

Identify these factors on your own if possible; do not ask the user unnecessarily:
- Identify what this skill helps with.
- Identify 3–5 example requests that should trigger it.
- List edge cases and failure modes to avoid.

**Concrete examples:**

When building a `pdf-merger` skill:
- What functionality should it support? "Merge multiple PDFs into one document"
- Example user requests: "Combine these three PDF files into one"
- What should NOT be included? PDF editing, text extraction, OCR

When building a `code-review` skill:
- What functionality should it support? "Review code changes for quality issues"
- Example user requests: "Review this PR for security issues"
- What should NOT be included? Writing new code, running tests, deployment

### Step 2 – Choose patterns and degrees of freedom

**Use archetypes for inspiration** (Section 3); combine them or create a novel structure accordingly:
- MinimalReference for simple utilities
- Workflow-Driven for multi-step processes
- Phase-Gated for dangerous operations
- Reference-Heavy for large stable domains
- Checklist/Rubric for evaluation tasks
- Database-Access for single data sources
- Domain-Doctrine for principles and guidelines

**Decide degrees of freedom:**
- **High freedom** for creative, low-risk tasks
- **Medium freedom** for standard workflows
- **Low freedom** for fragile or dangerous tasks

### Step 3 – Plan reusable components

For each example use case, ask:
- Which parts will repeat across runs?
- Which parts are **fragile** or must be consistent?

From this, derive a list of:
- Scripts to create (e.g., `scripts/rotate_pdf.py`)
- Reference docs potentially required (e.g., `references/schema.md`)
- Assets to include (e.g., templates)

**Only plan components** that give a real advantage over simple improvisation.

### Step 4 – Scaffold the skill folder

**Skip this step only when:** The skill folder already exists and you're iterating on an existing skill.

Create the skill folder structure manually or using your preferred method.

**Ensure folder sits under:**
- `<workspace>/skills/` for the current OpenClaw workspace, or
- `~/.openclaw/skills/` for user-wide skills

**Minimal structure:**
```
skill-name/
├── SKILL.md          # required
├── scripts/          # optional
├── references/       # optional
└── assets/           # optional
```

### Step 5 – Write or refine SKILL.md

**Focus on:**

1. **Frontmatter**
   - Set `name` using hyphen-case
   - Write a concise `description` using the What-When-Not pattern from Section 4.1
   - Add minimal `metadata.openclaw` gating as appropriate (required binaries, env vars)

2. **Body structure**
   - Start with: **Scope and boundaries** (what this skill covers and doesn't cover)
   - Add sections based on the chosen archetype from Step 2
   - Use MUST/SHOULD directives for critical rules (see Section 2.4)
   - Include a "Verification" section with checks to run

**Note:** Do NOT include a "When to use this skill" section — the skill is already loaded. Instead, define clear scope, boundaries, and explicit references to any `references/` files that must be read first.

3. **Keep it dense** but readable; prefer 300–800 lines over very long documents

### Step 6 – Implement scripts and assets

**For each planned script:**
- Implement it as **complete, runnable code**—no placeholders
- Handle errors and provide clear messages
- Document usage at the top of the script

**For assets:**
- Add templates or starter files as needed
- Mention their existence in SKILL.md

**Note:** Some skills require user-provided resources:
- **Assets:** Brand logos, templates, fonts (user must provide)
- **References:** Company schemas, policies, API docs (user must provide)
- **Scripts:** Domain-specific logic (may require user input for business rules)

Identify these requirements early and request from the user before implementation to avoid mid-workflow blockers.

### Step 7 – Validate and test

Before deploying a skill, verify:
- SKILL.md exists with valid YAML frontmatter
- `name` uses hyphen-case and `description` follows What-When-Not pattern
- Referenced files actually exist in the structure

Restart or reload OpenClaw so the new skill is discovered, then test via CLI, local UI, or chat interface.

**Use realistic prompts** from Step 1 and observe:
- Does the skill trigger when expected?
- Does it avoid triggering for out-of-scope requests?
- Do scripts run and handle errors correctly?

### Step 8 – Iterate based on behavior

Treat skill authoring as an iterative process. Skills evolve based on real usage:

**Iteration workflow:**

1. **Identify the struggle** - What went wrong? Where was the agent confused?
2. **Diagnose the root cause** - Is it a description issue? Missing reference? Unclear workflow?
3. **Implement targeted fixes** - Fix only what's broken; avoid over-engineering
4. **Test with the original failing case** - Verify the fix works for the specific scenario

**Common issues and fixes:**

**If the skill is misused:**
- Tighten or clarify `description` with stronger boundaries
- Add explicit "Not for" exclusions

**If the skill is ignored:**
- Make description triggers more explicit
- Add specific phrases users might say

**When errors occur in scripts:**
- Improve error handling and logging
- Update SKILL.md to suggest better usage patterns

**Key principle:** Iterate based on actual failures, not hypothetical improvements. The goal is a skill that works reliably for real workflows.

---

## 7. Validation Checklist

Use this comprehensive checklist before finalizing a skill.

### Structure

- [ ] SKILL.md file exists with valid YAML frontmatter
- [ ] Frontmatter has `name` and `description` fields
- [ ] `name` uses hyphen-case (lowercase, digits, hyphens only)
- [ ] Markdown body is present and substantial
- [ ] Referenced files actually exist

### Description Quality

- [ ] Uses **What-When-Not** pattern (What it does, Use when, Not for)
- [ ] **Single-line with quotes** (never multiline `|` or `>`)
- [ ] Includes specific trigger phrases users might say
- [ ] Lists concrete "Not for" exclusions
- [ ] Not vague or generic
- [ ] Accurately describes when skill should trigger

### Content Quality

- [ ] SKILL.md body uses **imperative/infinitive form**
- [ ] Content follows **Delta Principle** (non-obvious, domain-specific only)
- [ ] Content is dense but readable
- [ ] No generic tutorials or "how to code" material
- [ ] Examples are complete and working
- [ ] Scripts are executable with error handling
- [ ] Scripts document required env vars or config

### Progressive Disclosure

- [ ] Core concepts in SKILL.md
- [ ] Detailed docs in `references/` (only if >5-10 pages or >500-700 lines)
- [ ] Working code samples in SKILL.md or, if very long, in dedicated files under `references/` that are explicitly linked from SKILL.md
- [ ] Utilities in `scripts/`
- [ ] SKILL.md explicitly references these resources
- [ ] No deeply nested references (max one level from SKILL.md)

### Documentation Patterns

- [ ] **DO/DON'T** sections for critical patterns
- [ ] **Good/Bad** examples for common mistakes
- [ ] **Best Practices** summary included
- [ ] **Common Gotchas/Mistakes** section where applicable
- [ ] Examples explain "why" something is good/bad

### Testing

- [ ] Skill triggers on expected user queries
- [ ] Skill avoids triggering for out-of-scope requests
- [ ] Scripts run and handle errors correctly
- [ ] Tested with realistic prompts from Step 1
- [ ] Frontmatter is valid YAML with required fields

### Security

- [ ] Dangerous operations require explicit user confirmation
- [ ] Shell commands use whitelisting or structured options
- [ ] No raw user input interpolated into shell commands
- [ ] `metadata.openclaw.requires` gates appropriate dependencies
- [ ] Error messages don't leak sensitive information

---

## 8. Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - Prompt injected when skill triggers (<5k words)
3. **Bundled resources** - Available on-demand (Unlimited because scripts can be executed without reading into context window)

### Progressive Disclosure: A Guideline, Not a Rule

**Progressive disclosure is a good practice, but not a blind requirement.** AI agents are smart and efficient. The key decision factor is **"what should be read when?"**

**Decision framework:**

- **10 files of huge documentation?** → Put in `references/`. Load only when needed.
- **3 files that must be read on every skill activation?** → Combine into single `SKILL.md`. Avoid unnecessary friction.

**Focus on:**
- **Clarity** - Ensure instructions are clear and immediately applicable.
- **Conciseness** - Is every line earning its place? (Delta principle)
- **Delta rule** - Does this encode non-obvious, project-specific knowledge?

**The 700-line range is a guideline, not a hard rule.** If a skill needs 700-1000 lines because:
- All content is relevant on every activation
- The domain is complex but tightly integrated
- Splitting would create unnecessary file-hopping

...then keep it as one file. Don't split just to hit a number.

**Use progressive disclosure when:**
- Content is clearly optional or specialist (advanced features, edge cases)
- Multiple domains/variants rarely used together
- Documentation is large (>5-10 pages or >500-700 lines) and loaded on-demand
- Long example collections exist (move them to `references/EXAMPLES.md`)

**Avoid progressive disclosure when:**
- Splitting creates frequent back-and-forth file reading
- Content is needed for most tasks triggered by the skill
- The skill is already concise and focused (<500-700 lines)

**Note:** This meta-skill is intentionally written as a single SKILL.md to ensure all content is available when designing skills. Use separate reference files in your own skills only for large, case-specific templates or documentation.

---

### Progressive Disclosure Patterns

**Pattern 1: High-level guide with conditional links**

Basic content in SKILL.md, deep content in references/:

```markdown
## Quick Start
Extract text with pdfplumber:
[code example]

## Advanced Features
- **Form filling**: Read references/FORMS.md for complete guide
- **API reference**: Read references/API.md for all methods
- **Examples**: Read references/EXAMPLES.md for common patterns
```

**Pattern 2: Domain-specific organization**

When supporting multiple domains or variants:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── references/
    ├── finance.md (finance-specific tables)
    ├── sales.md (sales-specific tables)
    └── product.md (product-specific tables)
```

When a query concerns sales metrics, read only sales.md.

**Pattern 3: Conditional details**

Show common case, link to edge cases:

```markdown
## Editing Documents

For simple edits, modify the XML directly.

**For tracked changes**: Read references/REDLINING.md
**For OOXML details**: Read references/OOXML.md
```

**Important guidelines:**

- **Avoid deeply nested references** - Keep references one level deep from SKILL.md
- **Structure longer reference files** - For files >100 lines, include a table of contents at the top

---

## 9. Workflow and Output Patterns

### 9.1 Workflow Patterns

**Sequential Workflows**

For complex tasks, break operations into clear, sequential steps. Provide an overview at the beginning of SKILL.md:

```markdown
Filling a PDF form involves these steps:

1. Analyze the form (run analyze_form.py)
2. Create field mapping (edit fields.json)
3. Validate mapping (run validate_fields.py)
4. Fill the form (run fill_form.py)
5. Verify output (run verify_output.py)
```

**Conditional Workflows**

For tasks with branching logic, guide through decision points:

```markdown
1. Determine the modification type:
   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

### 9.2 Output Patterns

Apply these patterns to produce consistent, high-quality output.

**Template Pattern**

Provide templates for output format. Match the level of strictness to the task requirements.

**For strict requirements (like API responses or data formats):**

```markdown
## Report structure

ALWAYS use this exact template structure:

# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```

**For flexible guidance (when adaptation is useful):**

```markdown
## Report structure

Here is a sensible default format; apply best judgment based on context:

# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on discoveries]

## Recommendations
[Tailor to the specific context]

Adjust sections for the specific analysis type.
```

**Examples Pattern**

For skills where output quality depends on seeing examples, provide input/output pairs:

```markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

Follow this style: type(scope): brief description, then detailed explanation.
```

Examples provide clearer guidance on style and detail than descriptions alone.

---

## 10. Using Skills in OpenClaw

OpenClaw prioritizes skills from these locations:
- `<workspace>/skills/` - Workspace-specific (highest precedence)
- `~/.openclaw/skills/` - Shared folder (managed)
- Bundled skills - Shipped with install (lowest precedence)

Skills with the same name are overridden by higher-precedence locations.

### Testing Your Skill

1. Place the skill in the OpenClaw workspace (`<workspace>/skills/` or `~/.openclaw/skills/`)
2. Reload the agent or restart the gateway
3. Test via clawdbot (WhatsApp/Telegram) or local chat
4. Iterate based on observed behavior

### Security Considerations

- Skills are trusted code - only edit on trusted systems
- Scripts using `bash` must whitelist commands
- Never interpolate raw user input into shell commands
- Use `metadata.openclaw.requires` to gate on environment

---

## 11. Best Practices Summary

### ✅ DO

- Use **What-When-Not** pattern in descriptions
- Keep descriptions as **single-line quoted strings**
- Use **hyphen-case** for skill names
- Apply the **Delta Principle** (keep only non-obvious, domain-specific knowledge)
- Use **DO/DON'T** sections for critical patterns (with ✅/❌ markers)
- Provide **Good/Bad** examples for common mistakes
- Include **Validation Checklists** for quality gates
- Use **imperative/infinitive form** for direct instructions
- Reinforce critical rules with **strong second-person** (e.g., "You MUST")
- Apply **progressive disclosure** for optional or extensive content (>5-10 pages or >500-700 lines)
- Reference supporting files explicitly in SKILL.md
- Explain "why" when showing good/bad examples
- Use gerunds for skill names (e.g., `processing-pdfs`, `analyzing-data`)
- Keep SKILL.md focused and dense (300-800 lines ideal)

### ❌ DON'T

- Use multiline (`|` or `>`) in description fields
- Write vague descriptions without specific triggers
- Use generic names like `helper`, `misc`, `utils`
- Include tutorials or generic definitions already known
- Put everything in one file when progressive disclosure makes sense
- Use weak or indirect language ("you should", "you can", "the agent must")
- Leave resources unreferenced
- Skip validation steps
- Create deeply nested references (keep one level from SKILL.md)
- Write negative constraints without positive alternatives
- Use vague phrases like "provides guidance for X"

### Quick Decision Framework

**When to split content into references/:**
- Content is >5-10 pages (>500-700 lines) or loaded on-demand
- Domain-specific or specialist information not needed for most tasks
- Multiple domains/variants that are rarely used together

**When to keep content in SKILL.md:**
- Content needed for most tasks triggered by the skill
- Small enough to fit comfortably (<500-700 lines)
- Splitting would create frequent back-and-forth file reading

**When to use DO/DON'T sections:**
- Critical patterns where correctness matters
- Common mistakes or pitfalls
- Security or safety considerations

**When to use Good/Bad examples:**
- Frontmatter and descriptions
- Code structure patterns
- API usage patterns
- Common configuration mistakes

**When to use Validation Checklists:**
- Multi-step processes or workflows
- Quality gates or reviews
- Pre-deployment verification
- Skill finalization

**When to use Progressive Disclosure:**
- Large documentation sets (>5-10 pages or >500-700 lines)
- Domain-specific variants (e.g., AWS vs GCP vs Azure)
- Advanced features rarely accessed
- API references and detailed examples

---

## Learning From This Skill

This skill-creator skill serves as a **gold standard example** for effective skill documentation. Study its structure and approach when creating new skills.

### What This Skill Models

**Documentation Patterns:**
- **DO/DON'T sections** (4.2) with ✅/❌ visual markers for scannability
- **Good vs Bad examples** (4.3) with side-by-side comparisons and explanations
- **Common Mistakes** (Section 5) in Mistake #N format with "Why bad"/"Why good"
- **Validation Checklist** (Section 7) for comprehensive quality gates
- **Best Practices Summary** (Section 12) as quick reference
- **Quick Decision Framework** for when to use each pattern

**Structural Patterns:**
- Clear frontmatter with What-When-Not description
- Progressive disclosure explained but not forced (Section 9)
- Workflow patterns with examples (Section 10)
- High freedom throughout—guidelines, not rigid rules

### How This Skill Teaches

**High Freedom Approach:**
- Provides **options and frameworks**, not mandates
- Says "Adapt it accordingly" (Section 6)
- Explains **why** patterns work, not just what to do
- Uses "Guideline, not a rule" language (Section 9)
- Offers **archetypes as menu**, not prescription (Section 3)

**Teaching Patterns Used:**
1. **Concrete examples** for every abstract concept
2. **Side-by-side comparisons** to show differences clearly
3. **"Why" explanations** for every rule
4. **Decision frameworks** to help reasoning, not replace it
5. **Checklists** for validation, not for generating

**Avoids Low-Freedom Traps:**
- ❌ NOT a rigid template to fill in
- ❌ NOT a step-by-step generator
-  CAN BE a "you must" rulebook
- ✅ IS a guide for making good decisions
- ✅ IS a collection of effective patterns
- ✅ IS a reference for common pitfalls

### Steal These Patterns

When creating a new skill, consider borrowing:

| From Section | Pattern to Adapt | Use For |
|--------------|------------------|---------|
| 4.2 | DO/DON'T with ✅/❌ | Critical patterns, common mistakes |
| 4.3 | Good/Bad examples | Code patterns, configuration, naming — Prefer embedding examples near instructions in SKILL.md; move long example collections to `references/` |
| 5 | Common Mistakes (Mistake #N) | Recurring pitfalls in the specific domain |
| 7 | Validation Checklist | Quality gates, pre-deployment checks |
| 12 | Quick Decision Framework | Help with choosing between options |
| 9 | "Guideline, not a rule" | Avoiding over-prescription |

### Key Lesson: High Freedom

This skill maintains **high freedom** while teaching:

- **Offers archetypes** (Section 3) without forcing selection
- **Suggests patterns** (Section 4) while allowing adaptation
- **Provides workflow** (Section 6) and allows adaptation
- **Lists mistakes** (Section 5) with reasoning
- **Gives checklist** (Section 7) without mandating every item

**Result:** Principles-based application rather than rigid template following.

**Apply this approach:** Teach domain-specific knowledge with **examples, reasoning, and patterns**, not rigid procedures. Reserve low-freedom approaches (strict workflows, hard gates) only for dangerous or fragile operations.
