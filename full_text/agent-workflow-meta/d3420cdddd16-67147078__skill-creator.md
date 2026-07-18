---
name: skill-creator
description: >-
  Creates new agentic skills following agentskills.io specification and project quality
  gates. Use when building a new skill, when user asks to create a skill, or mentions
  creating new capabilities or slash commands.
license: MIT
metadata:
  version: 1.0.0
  author: skills project
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash(mkdir *) Bash(wc *) Bash(ls *) Bash(find *)
---

# Skill Creator

Create new skills that follow the agentskills.io specification and this project's quality gates.

## Quick Start

When the user asks to create a new skill:

1. **Understand the goal** — Clarify what the skill does, its scope, triggers, and constraints
2. **Plan structure** — Determine if references/scripts are needed
3. **Create iteratively** — Build the skill, validate, and refine
4. **Verify quality** — Run all quality gates before considering complete

## When to Use This Skill

- User asks to create a new skill, command, or capability
- User mentions wanting a slash command or workflow automation
- You're building infrastructure for a new domain (e.g., "we need a skill for X reviews")
- A recurring task pattern would benefit from a structured skill rather than ad-hoc instructions
- User asks to formalize or package existing instructions into a reusable skill

## Workflow

### Phase 1: Discovery

**Research first, then ask.** Scan the project before presenting any questions — the answers you find shape better options.

**Step 1.1 — Scan existing skills:**

```bash
ls -d .claude/skills/*/SKILL.md 2>/dev/null | sed 's|.claude/skills/||;s|/SKILL.md||' | sort
```

Read the name and description from each SKILL.md frontmatter. Look for:
- Skills that overlap with what the user wants (so you can flag the overlap or suggest extending instead of creating)
- Patterns already in use (what tools, hooks, reference structures appear frequently)
- Gaps — domains not yet covered that the new skill might fit

**Step 1.2 — Scan the project context:**

```bash
# What's the target codebase?
ls Cargo.toml package.json go.mod pyproject.toml flake.nix 2>/dev/null
# Any existing docs or conventions?
find . -maxdepth 2 -name "CLAUDE.md" -o -name "*.md" -path "*/docs/*" | head -10
```

**Step 1.3 — Use `AskUserQuestion` to clarify, with pre-populated options from your research:**

Present what you found (similar skills, relevant patterns, target ecosystem) as context, then ask:

- **Primary purpose**: What should this skill accomplish? *(If similar skills exist, mention them and ask: extend one, or create new?)*
- **Trigger scenarios**: When should Claude load this automatically?
- **Scope**: What's explicitly in vs out?
- **Complexity**: Simple inline instructions, or needs references/scripts?

The research prevents asking questions Claude could have answered itself — and surfaces options the user might not have considered.

### Phase 2: Design

Based on discovery, determine:

**Skill structure:**
- Inline only (< 200 lines of instructions)
- With references (instructions + separate reference docs)
- With scripts (includes executable code)
- With assets (templates, checklists, schemas)

**Progressive disclosure strategy:**
- What goes in SKILL.md (always loaded)?
- What goes in references/ (loaded on demand)?
- What goes in scripts/ (executed, not loaded)?
- What goes in assets/ (static resources)?

**Name and description:**
- Use gerund form (creating-pdfs, analyzing-logs) or noun phrase (pdf-creation)
- Description must include: what it does + when to use it + trigger keywords
- Max 64 chars for name, max 1024 chars for description

### Phase 3: Implementation

**Create directory structure:**
```bash
mkdir -p .claude/skills/skill-name/{tests/cases,references,assets,scripts}
```

**Write SKILL.md with:**

1. **Frontmatter** (required):
   ```yaml
   ---
   name: skill-name
   description: >-
     What this does and when to use it. Include trigger keywords.
   license: MIT
   metadata:
     version: 1.0.0
     author: contributor-name
   ---
   ```

2. **Quick Start** (2-4 key points, NOT exactly 3 or 5):
   - Most important information first
   - Assume Claude is smart, don't over-explain
   - Use contractions ("you'll", "it's", "don't")
   - Address reader as "you"

3. **When to Use This Skill**:
   - Specific scenarios with concrete examples
   - NOT vague generalities

4. **Core Instructions**:
   - Step-by-step workflows (with checklists for complex processes)
   - Concrete examples over abstract descriptions
   - Templates when output format matters
   - Feedback loops for quality-critical tasks

5. **Hooks** (if the skill needs Stop/Start behavior):
   ```yaml
   hooks:
     Stop:
       - hooks:
           - type: command
             command: python3 "$HOME/.claude/skills/skill-name/scripts/check-completion.py"
             timeout: 300
   ```
   **Required patterns in every hook script:**
   - Call `os.chdir(hook_input.get("cwd"))` immediately after reading stdin — without this, all `Path()` checks run against the wrong directory
   - Never early-exit on `language == "unknown"` — language-agnostic checks (docs, TODOs, secrets) must still run for greenfield projects
   - Check `hook_input.get("stop_hook_active")` to prevent infinite loops

   **Running in opencode:** opencode ignores the `hooks:` frontmatter. Keep
   it for Claude Code, and make the hook script reusable from opencode by
   sticking to the stdin-JSON-in / `{"decision": ...}`-out contract — the
   `.opencode/plugins/completion-loop.ts` plugin drives such scripts on the
   `session.idle` event. Add a short "Running in opencode" note to any skill
   you give a hook. See [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

6. **References** (if needed):
   - Link to reference files: `See [reference-name.md](references/reference-name.md)`
   - Keep one level deep (no nested references)
   - Use table of contents for long references

### Phase 4: Create Tests

**Every skill MUST have test cases.**

Create `tests/eval.yaml`:
```yaml
description: Test cases for skill-name
prompts:
  - file://cases/01-basic.yaml

providers:
  - id: anthropic:claude-haiku-4-5

defaultTest:
  assert:
    - type: llm-rubric
      value: |
        Score from 0-100 based on:
        - Completeness: addresses all requirements
        - Correctness: follows specifications
        - Quality: meets project standards
```

Create at least 2 test cases in `tests/cases/`:

**Example test case** (`tests/cases/01-basic.yaml`):
```yaml
description: Basic skill usage test
vars:
  request: "Use the skill to accomplish X"
assert:
  - type: contains
    value: "expected output pattern"
  - type: llm-rubric
    value: "Evaluates whether the output meets quality standards"
```

### Phase 5: Validation

**Run all quality gates:**

1. **Format validation**:
   ```bash
   bash tests/scripts/simple-validate.sh .claude/skills/skill-name/SKILL.md
   ```

2. **Voice compliance**:
   ```bash
   python3 tests/scripts/check-voice-compliance.py .claude/skills/skill-name/SKILL.md
   ```

3. **Structure check**:
   - SKILL.md exists with valid frontmatter
   - Name matches directory name
   - Description present and under 1024 chars
   - tests/eval.yaml exists
   - At least 2 test cases in tests/cases/

4. **Size check**:
   - SKILL.md body < 500 lines
   - Total skill < 5000 tokens

5. **Smoke test**:
   - Test the skill with 2+ realistic prompts
   - Verify expected behavior

6. **Voice check**:
   - Zero banned words in content
   - Warnings in reference titles acceptable
   - Uses contractions naturally
   - Avoids "In conclusion", "Overall", "In summary" <!-- voice-ok -->
   - No lists of exactly 3 or 5 items

## Content Guidelines

### Writing Style (CRITICAL)

Apply `natural-writing-style` to all skill content you produce. Follow this project's voice requirements:

**DO:**
- Use contractions: "don't", "you'll", "it's", "won't"
- Vary sentence length. Mix it up.
- Address reader as "you" (not "the user")
- Be conversational and friendly
- Use active voice
- Show enthusiasm when appropriate

**DON'T:**
- Use banned words: utilize, leverage, robust, comprehensive, seamless, delve, synergy, cutting-edge, holistic, pivotal, paramount <!-- voice-ok -->
- Start conclusions with "In conclusion", "Overall", "In summary" <!-- voice-ok -->
- Create lists with exactly 3 or 5 items (use 2, 4, 6, or 7)
- Over-explain what Claude already knows
- Use passive voice unnecessarily

### Conciseness Principle

**Challenge every sentence:**
- "Does Claude really need this?"
- "Can I assume Claude knows this already?"
- "Does this justify its token cost?"

**Example of conciseness:**

Bad (verbose):
```markdown
PDF files are a common document format that contains text and images.
To extract text from a PDF, you'll need to use a specialized library.
There are many libraries available, but we recommend pdfplumber.
First, install it with pip, then use the code below...
```

Good (concise):
```markdown
Extract PDF text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

### Progressive Disclosure

**Main SKILL.md should be:**
- High-level overview
- Core instructions
- Navigation to detailed resources

**Separate files (references/) for:**
- API documentation
- Detailed specifications
- Extended examples
- Domain-specific guides

**Pattern:**
```markdown
## Advanced Features

**Form filling**: See [references/forms.md](references/forms.md)
**API reference**: See [references/api.md](references/api.md)
**Examples**: See [references/examples.md](references/examples.md)
```

### Workflow Patterns

For complex multi-step processes, provide a checklist:

````markdown
## Workflow

Copy and check off as you complete:

```
Progress:
- [ ] Step 1: Analyze requirements
- [ ] Step 2: Create structure
- [ ] Step 3: Validate format
- [ ] Step 4: Test functionality
```

**Step 1: Analyze requirements**
[Instructions...]

**Step 2: Create structure**
[Instructions...]
````

## Common Patterns

### Template Pattern

When output format is important:

````markdown
## Output Format

Use this template:

```markdown
# [Title]

## Overview
[Brief description]

## Key Points
- Point 1
- Point 2
- Point 4 (note: not exactly 3!)

## Conclusion
[Summary without saying "In conclusion"] <!-- voice-ok -->
```
````

### Examples Pattern

Show input/output pairs:

````markdown
## Examples

**Example 1:**
Input: User asks to review C code
Output:
```
Reviews code for security issues, memory safety, buffer overflows...
```

**Example 2:**
Input: User asks about BSD porting
Output:
```
Provides Linux to BSD syscall mapping, header differences...
```
````

### Conditional Workflow Pattern

Guide through decision points:

```markdown
## Workflow Decision

**Creating new content?** → Follow creation workflow
**Editing existing content?** → Follow editing workflow

### Creation workflow:
1. [Steps...]

### Editing workflow:
1. [Steps...]
```

## Quality Checklist

Before considering the skill complete:

### Core Quality
- [ ] Description includes what + when + triggers
- [ ] Name follows convention (gerund or noun phrase)
- [ ] SKILL.md < 500 lines
- [ ] Uses progressive disclosure appropriately
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Concrete examples, not abstract
- [ ] References are one level deep
- [ ] Workflows have clear steps

### Voice and Style
- [ ] Uses contractions naturally
- [ ] Addresses reader as "you"
- [ ] Varies sentence length
- [ ] Zero banned words in content
- [ ] No "In conclusion" etc. <!-- voice-ok -->
- [ ] Lists have 2, 4, 6, or 7 items (not 3 or 5)
- [ ] Conversational and friendly tone
- [ ] Concise (no unnecessary explanations)

### Interactive Input
- [ ] `AskUserQuestion` in `allowed-tools` if skill asks users anything
- [ ] Interactive steps call `AskUserQuestion` (not prose "ask the user")
- [ ] Research runs before questions — scan project state, then present pre-populated options
- [ ] No blank open-ended questions for things Claude could find by scanning

### Structure
- [ ] YAML frontmatter valid
- [ ] Name matches directory
- [ ] Description under 1024 chars
- [ ] tests/eval.yaml present
- [ ] At least 2 test cases in tests/cases/
- [ ] References (if any) organized by domain
- [ ] Scripts (if any) documented

### Testing
- [ ] Format validation passes
- [ ] Voice compliance passes (warnings in refs OK)
- [ ] Structure validation passes
- [ ] Size check passes (< 500 lines, < 5000 tokens)
- [ ] Smoke tested with 2+ prompts
- [ ] Test cases written and verified

## Anti-Patterns to Avoid

**Don't assume knowledge of packages:**
```markdown
Bad: "Use the pdf library"
Good: "Install pdfplumber: pip install pdfplumber"
```

**Don't use Windows paths:**
```markdown
Bad: scripts\helper.py
Good: scripts/helper.py
```

**Don't offer too many options:**
```markdown
Bad: "Use pypdf, or pdfplumber, or PyMuPDF, or..."
Good: "Use pdfplumber for text extraction. For OCR, use pytesseract."
```

**Don't nest references deeply:**
```markdown
Bad: SKILL.md → advanced.md → details.md
Good: SKILL.md → advanced.md (one level)
```

## Referencing Scripts in Skills (CRITICAL)

**The path resolution problem:**

When a skill references scripts in its `scripts/` directory, the path must work regardless of where the skill is installed (global `~/.claude/skills/` or project-local `.claude/skills/`). Claude Code currently lacks a `$CLAUDE_SKILL_DIR` environment variable, so you must use different strategies depending on the skill's installation location.

**Available environment variables:**
- `$CLAUDE_PROJECT_DIR` — absolute path to the project root
- `${CLAUDE_PLUGIN_ROOT}` — absolute path to the plugin root (plugins only)
- `$HOME` — user's home directory
- No variable for the skill's own directory

**Best practices by installation type:**

### For project-local skills (.claude/skills/)

Reference scripts relative to the project root:

```bash
# In SKILL.md, when calling a script bundled with the skill
bash "$CLAUDE_PROJECT_DIR/.claude/skills/skill-name/scripts/validate.sh"
```

Always quote `$CLAUDE_PROJECT_DIR` to handle paths with spaces.

### For global skills (~/.claude/skills/)

Use absolute paths with `$HOME`:

```bash
# In SKILL.md, for a globally installed skill
bash "$HOME/.claude/skills/skill-name/scripts/validate.sh"
```

### For portable/distributed skills

If you're creating a skill that will be distributed and installed by others:

1. **Document the expected installation location** in the skill's description or README
2. **Provide installation instructions** that specify where users should install it
3. **Use project-local paths** (`$CLAUDE_PROJECT_DIR/.claude/skills/`) as the default recommendation
4. **Consider providing both path variants** with clear documentation

**Example for portable skill:**

```markdown
## Installation

This skill should be installed in your project's `.claude/skills/` directory:

\`\`\`bash
mkdir -p .claude/skills/skill-name
cp -r skill-name/* .claude/skills/skill-name/
\`\`\`

The skill references scripts using `$CLAUDE_PROJECT_DIR`, so it won't work correctly
if installed globally in `~/.claude/skills/`.
```

### In skill frontmatter hooks

When defining hooks in skill frontmatter that call bundled scripts:

```yaml
---
name: secure-operations
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: bash "$CLAUDE_PROJECT_DIR/.claude/skills/secure-operations/scripts/validate.sh"
---
```

**Hook exit codes and patterns:**

For correct hook behavior, especially Stop hooks:
- Exit 0 = Allow action to proceed (work complete)
- Exit 2 = Block action/continue working (send instructions via stderr)
- Always check `stop_hook_active` in Stop hooks to prevent infinite loops
- Write gap messages to stderr (>&2) not stdout

See `references/hook-patterns.md` for complete patterns, templates, and examples.

### Fallback strategy for shared scripts

If your skill uses scripts that should be shared across all skills in the repository:

```bash
# Try skill-specific script first, fall back to shared scripts
if [ -f "$CLAUDE_PROJECT_DIR/.claude/skills/skill-name/scripts/helper.sh" ]; then
  source "$CLAUDE_PROJECT_DIR/.claude/skills/skill-name/scripts/helper.sh"
elif [ -f "$CLAUDE_PROJECT_DIR/.claude/scripts/helper.sh" ]; then
  source "$CLAUDE_PROJECT_DIR/.claude/scripts/helper.sh"
else
  echo "Error: Required helper script not found" >&2
  exit 1
fi
```

**When documenting script usage in SKILL.md:**

Be explicit about paths:

```markdown
## Validation Script

This skill includes a validation script. When Claude uses this skill, it'll call:

\`\`\`bash
bash "$CLAUDE_PROJECT_DIR/.claude/skills/skill-name/scripts/validate.sh"
\`\`\`

The script checks that all required files exist and formats are correct.
```

**Testing script paths:**

After creating a skill with scripts, verify the paths work:

1. Install the skill in the expected location
2. Invoke the skill manually: `/skill-name`
3. Check that scripts execute without "file not found" errors
4. Test from different project directories if the skill is global

## When Complete

After all quality gates pass:

1. **Validate the full skill:**
   ```bash
   bash tests/scripts/simple-validate.sh .claude/skills/skill-name/SKILL.md
   python3 tests/scripts/check-voice-compliance.py .claude/skills/skill-name/SKILL.md
   ```

2. **Test with real scenarios:**
   - Load the skill in Claude Code
   - Try realistic prompts
   - Verify triggers work as expected

3. **Consider evaluation:**
   ```bash
   npx promptfoo eval -c .claude/skills/skill-name/tests/eval.yaml
   ```

4. **Document in catalog:**
   - Skill will appear in docs/SKILL-CATALOG.md
   - Update if needed for clarity

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Claude Code Skills](https://code.claude.com/docs/en/skills)
- Project quality gates: `.claude/rules/quality-gates.md`
- Project voice rules: `.claude/rules/writing-voice.md`
- Example skill: `.claude/skills/openbsd-knf-style/`
