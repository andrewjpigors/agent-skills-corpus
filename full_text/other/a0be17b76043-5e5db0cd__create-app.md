---
name: create-app
description: Create a new NLA project through guided conversation. Relevant when the user wants to build a new project. AI: Suggest as an option; invoke only on user assent or `/create-app`.
---

# Create NLA Application

You are helping someone build a new Natural Language Application. This is often their first interaction with the NLA framework — make it a good one.

**Your job:** Have a short conversation to understand what they want to build, then generate a complete, working NLA project tailored to their domain. The result should be ready to start using immediately.

**Philosophy:** The first experience of an NLA framework should itself be an NLA interaction — flexible interface on top (conversation), structure underneath (generated project). Don't make the user fill out a form. Talk to them.

---

## Before You Begin

Read these to understand what a well-formed NLA project looks like:

1. **`core/nla-foundations.md`** — What NLAs are, key principles
2. **`install/CLAUDE-intent.md`** — What an NLA's runtime identity should establish
3. **`install/structure-intent.md`** — What directory structure and reference files an NLA needs
4. **`install/skills-intent.md`** — What skill wrappers an NLA should have

These intent files are your primary source for structural guidance. They describe WHAT each file should contain and WHY; you generate content that fits the user's domain.

---

## Conversation Flow

Guide an adaptive conversation. Core principle: **parse what the user provides, fill in what you can, ask about what's missing.** Never force Q&A when the user already gave you the answer.

### Information Targets

Gather these through conversation (not as a checklist):

1. **Project name** — used as directory name (lowercase, hyphens)
2. **What the NLA does** — domain description in a sentence or two
3. **Primary task(s)** — name and what the LLM should do for each
4. **Voice/tone** — how output should sound
5. **Values/tradeoffs** — what the NLA prioritizes when tradeoffs arise
6. **Output format** — Markdown, HTML, JSON, plain text, etc.
7. **Audience** — who reads the output
8. **Configuration** — what behaviors should users be able to customize?

### Phase A: Opening

Welcome the user. Briefly explain what `/create-app` does:

> I'll ask a few questions about what you want to build, then generate a complete NLA project for you. The whole thing takes a few minutes.

Then ask an open question: **What are you building?** Accept anything from a one-liner to a full paragraph. Parse whatever they provide — if they mention voice, tasks, and audience in one message, don't ask again.

### Between Phase A and Phase B: Recognize the mode

Before targeted follow-ups, recognize what conversation the user is inviting. The recognition shapes the rest of the skill — extracting fields the user hasn't filled is the wrong mode if the user is inviting refinement, and grinding through structured questions is the wrong mode if the user just wants scaffolding. Three shapes:

- **Extraction.** The user provided requirements (what tasks, what audience, what voice) and the AI's job is to fill remaining fields. Proceed to Phase B as written — structured follow-ups are the right mode.
- **Collaborative refinement.** The user provided rich conceptual work (a working prompt, a developed framing, half-formed intuitions) and/or explicitly invites your perspective. The AI's job is to translate their thinking into NLA structure — propose shape, name gaps, invite pushback, help articulate what they can feel but haven't named.
- **Bare scaffold.** The user wants the framework structure with a named project; they'll author content via `/maintain` later. The AI's job is *not* to extract or refine — it's to set up scaffolding and get out of the way. Don't invent voice, values, tasks, or domain content from a name plus a thin signal. Confirm in prose ("Sounds like you want a bare scaffold named X — empty stubs you'll author in `/maintain`. Right?") and on confirmation, skip Phase B's targeted follow-ups entirely and go to Phase C with a scaffold-only summary.

Extraction and collaborative refinement aren't exclusive — a rich-conceptual submission still has gaps, and Phase B's targeted follow-ups still apply for those. But the conversation should *lead* with refinement, not extraction. Bare scaffold *is* exclusive: when the user is asking for scaffolding, the right behavior is to provide it, not to extract or refine content they're deliberately deferring.

Signals you're in collaborative-refinement territory:

- The user supplied a working prompt or sample artifact, not just a description.
- The user wrote at length about *why* they want this NLA, not just *what* it does.
- The user explicitly invited your thoughts, questions, or concerns.
- The user named tensions they haven't resolved ("I want X but also Y — I'm not sure how to express that").

Signals you're in bare-scaffold territory:

- Explicit phrasing: "just give me a base app," "I want a bare scaffold," "I'll fill in the rest later," "scaffold only."
- A project name with little or no domain description.
- The user invokes the skill with essentially just a name.
- The user explicitly says they want to author content via `/maintain`.

### Phase B: Targeted Follow-ups

**If the mode-recognition beat landed on bare scaffold, this whole phase collapses.** Confirm the project name, then go to Phase C. Packages are handled normally — if the user mentioned a package (e.g., penny-post), include it in the submodule setup as usual; bare-scaffold mode only skips the *content-extraction* questions (voice, values, tasks, output format, audience, configuration). The user is deliberately deferring those to `/maintain`. Extracting them anyway would invent content the user didn't ask for.

Otherwise: based on what's missing after Phase A, ask focused follow-up questions. Group related items together. Max 2-3 questions at a time.

**Groupings that work well:**
- Voice + audience (they inform each other)
- Values/tradeoffs (a single lightweight question: "When your NLA faces a tradeoff — accuracy vs. speed, completeness vs. brevity, consistency vs. creativity — which side should it lean toward?" Even a sentence is enough to seed the file; values get refined through use.)
- Output format + task description (what the LLM produces shapes how it works)
- Multiple tasks (if hinted at — "Do you need separate tasks for X and Y, or is that one task?")
- Configuration (what should users be able to customize?)
- NLA shape (if ambiguous — "Will this maintain state across sessions?" or "Does it need to call external tools or APIs?")

**Configuration guidance:** Ask what behaviors the app developer wants users to be able to customize. Examples: "Should users be able to adjust the tone? Change output length? Modify specific task behaviors?" Some developers want tight control ("only output format"); others want maximum flexibility ("let them change anything — it's an LLM"). If the developer isn't sure, suggest starting with common settings (voice adjustments, output preferences) and note that `/maintain` can expand the config-spec later.

**Provide examples and suggestions** to help users who aren't sure:
- Voice: "Formal and authoritative? Warm and conversational? Technical and precise?"
- Output format: "Clean Markdown is the most common. Some projects use HTML, JSON, or structured plain text."
- Task naming: "Task names become skill names. Short, verb-based: `format-article`, `classify-ticket`, `draft-response`."

### Phase C: Summary and Confirmation

Present a summary of what will be created:

```
Project: [name]
Location: ../[name]/

What it does: [one-sentence description]
Voice: [tone summary]
Output: [format]

Tasks:
  - /[task-name]: [what it does]

Files to generate: [count]
```

**For bare scaffold mode, use this variant instead:**

```
Project: [name]
Location: ../[name]/

Bare scaffold — empty stubs for voice/values/patterns, no tasks yet.
The shared-context files will need to be authored in /maintain before
the NLA produces meaningful output. A starter friction-log entry will
flag this as work waiting.

Files to generate: [count]
```

**Wait for explicit confirmation before creating any files.** This is the last chance to catch misunderstandings.

### Conversation Edge Cases

- **User provides everything upfront** — Skip to Phase C. Don't ask questions you already have answers to.
- **User arrives with rich conceptual work** — A working prompt, a developed framing, half-formed intuitions. The right mode is collaborative refinement (see "Between Phase A and Phase B: Recognize the mode"). Propose shape and invite pushback; don't grind through Phase B's questions when the user is asking for translation, not extraction. The most consequential decisions in this mode emerge from collaborative articulation, not structured Q&A — let them.
- **User wants a bare scaffold** — A name and minimal-to-no domain content; user intends to author everything via `/maintain`. The right mode is bare scaffold (see "Between Phase A and Phase B: Recognize the mode"). Phase B collapses; Category 3 files become stubs; a preloaded friction-log entry surfaces the authoring work for the user's first `/maintain` session. See "Bare Scaffold Mode" under File Generation for what gets generated and how.
- **Multiple tasks** — Generate a task doc and skill for each. All integration files (overview, CLAUDE.md) reflect all tasks.
- **User changes mind** — The confirmation step exists for this. Adjust and re-summarize.
- **Vague voice description** ("professional" or "friendly") — Generate a reasonable starter voice doc. Note to the user that `/maintain` can refine it later.
- **Complex project with many tasks** — If the user describes 4+ tasks or a domain with unclear boundaries, generate the full structure but only one or two starter tasks. Note which tasks were deferred and tell the user to add them via `/maintain` — iterating is better than generating shallow content for everything at once.

---

## File Generation

### Three Categories

**Category 1 — Generated from intent files (mechanical):**

These files have the same structure in every NLA. Read reference implementations from
`install/skills-intent.md` and templates from `install/structure-intent.md`.

| File | Source |
|------|--------|
| `.claude/skills/startup/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/maintain/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/friction-log/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/preferences/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/validate/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/install/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/update/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/export/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/check-updates/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/think/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/debrief/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/close/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `.claude/skills/guide/SKILL.md` | Reference wrapper in `install/skills-intent.md` |
| `reference/friction-log-archive.md` | Structure in `install/structure-intent.md` |
| `reference/feedback-log-archive.md` | Structure in `install/structure-intent.md` |
| `lib/.gitkeep` | Empty file |
| `reference/sessions/.gitkeep` | Empty file |
| `config/.gitkeep` | Empty file |
| `.gitignore` | Template in `install/structure-intent.md` |

**Category 2 — Generated from intent files + conversation (structured framework files):**

These files follow framework-defined structures but are customized with conversation
content. Read reference structures from intent files, then generate content that fits
the user's domain.

| File | Structural source | What to customize |
|------|-------------------|-------------------|
| `.claude/settings.local.json` | `install/install.md` permissions section | Resolved framework path, package paths from conversation |
| `CLAUDE.md` | `install/CLAUDE-intent.md` reference structure | Project identity, skills table, modes, environment |
| `reference/design-rationale.md` | `install/structure-intent.md` | Starter rationale with creation decisions for this domain |
| `reference/system-status.md` | `install/structure-intent.md` | Actual tasks and skills from the conversation |
| `reference/friction-log.md` | `install/structure-intent.md` | Keep format and guidance, seed patterns for this domain |
| `reference/feedback-log.md` | `install/structure-intent.md` | Keep format and guidance |
| `reference/installed-packages.md` | `install/structure-intent.md` | Add framework as first entry with date and commit hash |
| `README.md` | `install/structure-intent.md` | Project name, tasks, skills, getting started |
| `app/config-spec.md` | `install/structure-intent.md` | Configurable behaviors from the conversation |
| `config.md` | `install/structure-intent.md` | Starter config with defaults from config-spec |
| `config/maintenance.md` | Always-active maintenance preferences | Propose before editing, summarize plans |

**Category 3 — Generated from conversation (domain-specific):**

These files are unique to the user's domain. No framework-level structural source exists
because they vary completely by project. The structural guidance below is all you need.

| File | Structure guidance |
|------|-------------------|
| `app/overview.md` | See "Domain File Structures" below |
| `app/shared/values.md` | See "Domain File Structures" below |
| `app/shared/voice.md` | See "Domain File Structures" below |
| `app/shared/common-patterns.md` | See "Domain File Structures" below |
| `app/shared/output-spec.md` | See "Domain File Structures" below (if output format warrants its own file) |
| `app/[task-name].md` | See "Domain File Structures" below (one per task) |
| `.claude/skills/[task-name]/SKILL.md` | Domain skill pattern in `install/skills-intent.md` (one per task) |

### Domain File Structures

**`app/overview.md`** — How the NLA's pieces connect and how users work with it:
- What this NLA does (1-2 paragraphs)
- Tasks table: Task name, what it does, source file
- How it connects (brief description or diagram of the workflow)
- Skills table: all skills with purpose
- The improvement pipeline (friction-log → maintain cycle)
- How users work with this: typical sessions, what to expect, the session rhythm (startup → work → close). Include why: startup loads context because the LLM starts cold; close preserves state so next session starts warm. Describe the domain-specific workflow — what a user does first, what they iterate on, when they're done. This helps new users find their footing and helps the AI provide contextual guidance.
- For humans: key workflow patterns (change behavior, debug, add tasks)
- Document hierarchy: tree of all `app/` files with descriptions
- Document index: links to all docs
- **Where Things Live** — the project's structure record per the structural change discipline (see `packages/nla-framework/core/nla-foundations.md`). Lists each top-level directory and top-level file with purpose and attribution. At creation, attribution is mostly `[framework default]` (inherited from `install/structure-intent.md`) with `[domain decision]` for choices specific to this project (e.g., multi-voice file structure, additional `app/shared/` files, custom `lib/` helpers). Include a brief Decision Sources table at the bottom for scan affordance. This section becomes the consultation target for future placement decisions; it's updated as part of any structural change per the discipline (recording is part of the change, not separate hygiene).
- Getting started: first-time setup

**`app/shared/values.md`** — Commitments, priorities, and non-negotiables:
- What we prioritize (1-3 value statements expressing tradeoff preferences)
- What we won't compromise (non-negotiables, if any)
- Start minimal — a sentence or two from the conversation is enough. The maintenance
  cycle refines values as real tradeoffs surface during use.

**`app/shared/voice.md`** — Tone, personality, style:
- Who we are (brief identity)
- Voice: 3-5 tone principles, each with a clear/not pattern (e.g., "Clear, not clever")
- The test: one question to check if output matches the voice
- Editorial standards: domain-relevant rules (attribution, links, structure, etc.)

**`app/shared/common-patterns.md`** — Recurring patterns the LLM should recognize:
- Start minimal — 2-4 patterns that are clearly relevant to the domain
- Each pattern: what to look for, what to do, when NOT to apply
- Note that patterns grow through `/friction-log` + `/maintain` iteration

**`app/shared/output-spec.md`** (optional) — Output format specification. Create this
when output format is complex or shared across multiple tasks. When output is simple
(a classification, a short response) or the NLA has only one task, output guidance
can go directly in the task doc instead.

When created, it should cover:
- Format: what format and why
- Structure: general template showing the shape of typical output
- Flexibility: what varies, what's consistent
- What stays raw: what the NLA should NOT change

**`.claude/settings.local.json`** — Claude Code shell command approvals:
- Include broad bash patterns: `Bash(git:*)`, `Bash(ls:*)`, `Bash(test:*)`
- If packages discussed during the conversation need additional bash patterns, include those too
- Format as valid JSON:

```json
{
  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(ls:*)",
      "Bash(test:*)"
    ]
  }
}
```

**`app/[task-name].md`** — One doc per task (the actual application logic):
- Purpose: what this task does in one sentence
- Input: what it receives
- Output: what it produces
- Prerequisites: which docs to read first (voice, patterns, output spec if it exists)
- Processing steps: numbered steps with enough detail for the LLM to follow
- Judgment calls: when to flag uncertainty, domain-specific edge cases

### Bare Scaffold Mode

When the mode-recognition beat landed on bare scaffold, generation runs differently. The user is deferring authoring to `/maintain` — generating substantive content from a domain name alone would invent material the user didn't ask for and carry authority it doesn't deserve.

**Category 1 files:** Unchanged. Identical to the regular path.

**Category 2 files:** Mostly unchanged. Generate `CLAUDE.md`, `README.md`, `system-status.md`, `design-rationale.md`, `friction-log.md`, `feedback-log.md`, `installed-packages.md`, `config-spec.md`, `config.md`, `settings.local.json` normally — but render task-related sections as empty. Skills tables still list the framework-default skills (startup, maintain, friction-log, preferences, validate, install, update, export, check-updates, think, debrief, close, guide); they just have no domain-task rows. Tasks lists in `system-status.md` and `README.md` are empty. The structural shape is preserved; the content reflects "no tasks yet."

**Category 3 files:** Generated as minimal stubs.

- **`app/overview.md`** — Full structural shape (Where Things Live, document hierarchy, skills table for the framework-default skills) but empty tasks table and a header note that this NLA is unauthored. The note belongs near the top, after the orientation paragraph, framed as: *"This NLA was created as a bare scaffold. Shared-context files and tasks need to be authored via `/maintain` before the NLA produces meaningful output. See the preloaded friction-log entry for the authoring checklist."*
- **`app/shared/values.md`, `voice.md`, `common-patterns.md`** — Each generated as a stub. The file contains a single header line, and nothing below it:

  *"Unauthored stub. This file was scaffolded by `/create-app`. Author it in `/maintain` before relying on it — content here is placeholder, not informed by the domain."*

  No invented content. No example values, no example voice principles, no example patterns. The stub header is the file.

- **`app/shared/output-spec.md`** — Not generated. Output spec is optional; bare scaffolds don't need one.
- **`app/[task-name].md`** and **`.claude/skills/[task-name]/SKILL.md`** — Not generated. No tasks exist yet.

**Preloaded umbrella friction-log entry.** `/create-app` adds an entry to the new project's `reference/friction-log.md` before completing generation. The entry uses the project creation date and surfaces the authoring work as the first item in the user's `/maintain` queue. Entry shape:

```markdown
### [YYYY-MM-DD project creation date] — Author shared-context and add first task (scaffolded NLA)

**Type:** core
**Severity:** minor
**Blast radius:** this NLA
**Status:** pending

**Observation:**
This NLA was created via /create-app as a bare scaffold. Shared-context
files (values.md, voice.md, common-patterns.md) are unauthored stubs, and
no tasks exist yet. The NLA won't produce meaningful output until this
work is done.

**Proposed fix:**
Use /maintain to author the following, in roughly this order:
1. Add the first task — what does this NLA actually do? Creates app/[task].md
   and .claude/skills/[task]/SKILL.md.
2. Author app/shared/values.md — what does this NLA prioritize when
   tradeoffs arise?
3. Author app/shared/voice.md — how should output sound?
4. Add common patterns as they emerge through use (start minimal).

Remove this entry once shared-context is authored and the first task exists.
```

**Why two surfaces.** The stub header in each file catches the gap at task-execution time — when something later reads `voice.md` and sees "unauthored," it knows not to rely on it. The friction-log entry catches the gap at `/maintain` session start — when the maintainer arrives, the authoring work is already in the queue. Different surfaces for the same epistemic signal; together they cover both ways the gap can surface.

### Generation Order

Follow this order — later files reference earlier ones. For bare-scaffold projects, the order is the same, but step 4 is skipped (no task docs or domain skills) and steps 3, 5, 6 follow the "Bare Scaffold Mode" rules above (stubs, empty tables, preloaded friction-log entry).

1. **Directory structure and git setup** — Create all directories with `mkdir -p`, then run `git init` in the project directory, then add submodules: `git submodule add --depth 1 https://github.com/mightytech/nla-framework.git packages/nla-framework` (and any discussed packages). This must happen before file generation because thin wrappers reference framework files via `packages/`.
1a. **Pin framework submodule to its tagged release** — after `git submodule add`, run `git -C packages/nla-framework tag --sort=-creatordate | head -1`. If the tag points at a different commit than HEAD, ask the user: "Framework HEAD is at [short-hash]; latest tagged release is [tag] (at [short-hash]). Pin to the tagged release (stable) or HEAD?" If tag chosen: `git -C packages/nla-framework checkout [tag]` then `git add packages/nla-framework`. Apply the same check for any other submodules added in the discussed-packages set. Tagged releases are the stable default for new projects.
1b. **Settings file** — `.claude/settings.local.json` (pre-approves common shell commands)
2. **Category 1 files** — Thin wrapper skills, .gitkeep files, archives, .gitignore
3. **Shared context** — values.md, voice.md, common-patterns.md, output-spec.md (if needed)
4. **Task docs and skills** — Task-specific files for each task
5. **Integration files** — overview.md, CLAUDE.md, README.md (generated last because they reference everything above)
6. **Reference files** — design-rationale.md, system-status.md, friction-log.md, feedback-log.md, installed-packages.md
7. **Config files** — config-spec.md, config.md, config/maintenance.md

### How to Generate Each File

**Category 1 (mechanical):**
Read the reference implementation from the intent file and reproduce it. These are
identical across all projects.

**Category 2 (intent + conversation):**
1. Read the reference structure from the relevant intent file
2. Use it as structural guidance — match the section organization and purpose
3. Generate content based on the conversation — don't use sample domain content
4. Keep framework references intact — paths like `packages/nla-framework/core/` must be preserved exactly

**Category 3 (conversation only):**
1. Read the structural guidance in "Domain File Structures" above
2. Generate content entirely from the conversation
3. Match the voice and domain the user described
4. Start minimal — especially common-patterns.md. Better to add through `/friction-log` + `/maintain` than to guess

**Critical path details:**
- Framework references: `packages/nla-framework/core/nla-foundations.md`, `packages/nla-framework/core/skills/`
- Domain references: `app/`, `reference/`, `.claude/skills/` (project-relative)
- Thin wrappers point to: `packages/nla-framework/core/skills/[skill].md`

---

## Narration

As you create files, narrate by concept — not file-by-file. A sentence or two per concept, teaching as you go.

| Concept | What to say |
|---------|-------------|
| **Two channels** | `app/` is what the LLM reads and executes. `reference/` is for maintainers. They stay separate on purpose. |
| **Values file** | Your NLA's commitments — what it prioritizes when tradeoffs arise. Loaded at startup, shapes every decision. |
| **Voice file** | How your NLA sounds — tone, personality, style. Shapes every piece of content it produces. |
| **Thin wrappers** | These delegate to the framework. When you run `/update`, they pick up framework improvements. |
| **Task doc** | This IS the application. Edit this file to change what the LLM does. |
| **Common patterns** | Starting minimal — as you use the system and run `/friction-log`, patterns will emerge and you'll add them here. |
| **Friction log** | Your learning journal. `/friction-log` captures observations, `/maintain` turns them into improvements. |
| **Working with the system** | This section helps you and the AI understand typical sessions — what to do first, when to use which skills, and how the pieces flow together. |
| **Config** | Config lets users personalize the NLA without editing the application. Their preferences live in `config.md`, separate from the app. `/preferences` creates and edits it. |
| **Validation** | `/validate` checks internal consistency, reviews architecture after restructuring, traces scenarios through docs, and debugs when output doesn't match expectations. |
| **Permissions** | This pre-approves common shell commands like git. Without it, Claude Code would prompt on routine operations. |
| **Submodules** | The framework lives inside your project as a git submodule in `packages/`. Your project is self-contained — `git clone` plus `git submodule update --init` gives anyone a working copy. |
| **Package management** | `/install` adds new capabilities from extension packages. `/update` keeps them current. Your install log tracks what's installed. |
| **Bare scaffold** | You're going bare — I'll create the framework structure with empty stubs. The first thing you'll do in `/maintain` is author the shared-context files and add your first task. I'm preloading a friction-log entry so that work is waiting for you when you get there. |

Don't narrate every file. Group the thin wrappers, group the reference files. Focus on what helps the user understand the system.

---

## Post-Creation

After all files are created, provide:

```
Project created at ../[project-name]/

Next steps:
1. cd ../[project-name]
2. git add -A && git commit -m "Initial NLA project"
3. Start Claude Code
4. Run /startup to load foundational context
5. Try /[task-name] with some sample content

The project is ready to use, but it'll get better with use. Run `/maintain` to refine
your voice doc after seeing real output, add patterns as they emerge, or flesh out
additional tasks. `/friction-log` captures observations; `/maintain` turns them into
improvements. That's the development cycle.

To share this project: `git clone --recurse-submodules [url]` (or `git clone [url]` then `git submodule update --init` if cloned without recurse).
```

**For bare-scaffold projects, use this variant instead** — step 5 is `/maintain` rather than running a task, because no tasks exist yet:

```
Project created at ../[project-name]/

Next steps:
1. cd ../[project-name]
2. git add -A && git commit -m "Initial NLA scaffold"
3. Start Claude Code
4. Run /startup to load foundational context
5. Run /maintain — a preloaded friction-log entry will walk you through
   authoring shared-context files and adding your first task

The scaffold is empty by design. Shared-context stubs (values, voice, patterns)
are placeholders; the first /maintain session is where this NLA becomes real.

To share this project: `git clone --recurse-submodules [url]` (or `git clone [url]` then `git submodule update --init` if cloned without recurse).
```

**Tip for first-time users:** If they seem unsure or want to see a working example first, mention `/install-app` — it can install example NLA projects they can explore.

**Tip for orientation:** Mention that `/guide` is available if they want a walkthrough of how the system works, what skills do, or what to try next.

---

## Internal Consistency Check

Before reporting completion, verify:

1. **Skills table in CLAUDE.md** lists every skill in `.claude/skills/` (and no extras)
2. **Skills table in overview.md** matches CLAUDE.md
3. **Document index in overview.md** lists every file that exists
4. **system-status.md** tasks and skills match what was actually created
5. **Thin wrappers** all point to `packages/nla-framework/core/skills/[skill].md` with correct names
6. **README.md** references correct skill names
7. **config-spec.md** reflects configuration choices from the conversation
8. **config.md** has sensible defaults matching the config-spec
9. **.gitignore** excludes config.md and config/
10. **settings.local.json** contains valid JSON with Bash patterns

**For bare-scaffold projects, also verify:**

11. **No `app/[task].md` files exist** — bare scaffolds have no tasks
12. **No domain skill directories** in `.claude/skills/` beyond the framework defaults
13. **Shared-context files are stubs** — `app/shared/values.md`, `voice.md`, and `common-patterns.md` each contain only the unauthored-stub header; no invented content below
14. **`app/shared/output-spec.md` does not exist** — not generated for bare scaffolds
15. **Preloaded friction-log entry exists** in `reference/friction-log.md` with the project creation date and the authoring checklist (per "Bare Scaffold Mode")
16. **Overview reflects bare state** — empty tasks table in `app/overview.md` plus the unauthored-NLA header note
17. **Skills tables reflect framework-default skills only** — no domain skill rows in `CLAUDE.md` or `app/overview.md`

If anything doesn't match, fix it before reporting done.

---

## What You Don't Do

- **Don't skip `git init` and submodule setup** — These must happen before file generation so thin wrappers can resolve framework paths
- **Don't create `.env` or credentials** — Note in CLAUDE.md if the project will need them
- **Don't over-generate** — Common patterns should start minimal. Better to add through `/friction-log` + `/maintain` than to guess
- **Don't use sample domain content** — Generate fresh content for the user's domain. Article-formatter language shouldn't leak into a ticket-classification project.
- **Don't invent content when bare scaffold was confirmed** — A name plus a thin domain signal is not enough to seed voice, values, or patterns. The user signaled they're authoring later; respect the signal and generate stubs.
