---
name: skill-reviewer
description: >-
  Reviews and refines existing agentic skills against quality gates and best practices.
  Lists all project skills for selection when none is specified, with an option to review
  all skills at once. Use when reviewing a skill, improving skill quality, checking
  compliance, or when user asks to review or refine an existing skill.
license: MIT
metadata:
  version: 1.0.0
  author: skills project
allowed-tools: Read Write Edit Glob Grep AskUserQuestion Bash(bash tests/*) Bash(python* tests/*) Bash(wc *) Bash(ls *)
---

# Skill Reviewer

Review and refine existing skills to meet quality standards and follow best practices.

## When to Use This Skill

- You want to check a skill against the quality gates before shipping it
- A validation script flagged issues (format, voice, structure) and you need to triage and fix them
- You're doing a periodic review pass over the whole skills library
- Someone reports a skill isn't working as expected in a specific tool (Claude Code, Crush, etc.)
- You've just written a new skill with `skill-creator` and want a second-pass quality check

## Quick Start

When reviewing a skill:

1. **Pick a skill** — If none specified, list all project skills and let the user choose
2. **Read the skill** — Load the complete SKILL.md and supporting files
3. **Run validations** — Check format, voice, and structure
4. **Analyze quality** — Compare against best practices and quality gates
5. **Provide feedback** — Specific, actionable improvements
6. **Iterate with user** — Clarify priorities and implement changes

## Review Workflow

### Phase 0: Skill Selection

If the user didn't specify which skill to review, discover what's available and ask.

**Discover all skills in the project:**

```bash
ls -d .claude/skills/*/SKILL.md 2>/dev/null | sed 's|.claude/skills/||;s|/SKILL.md||' | sort
```

For each discovered skill, you'll want to extract its description from the YAML frontmatter so you can show meaningful labels.

**Present the list with AskUserQuestion:**

Build options from all discovered skills. Each option's label should be the skill name and its description should be the skill's description from frontmatter. Add **"Review all skills"** as the first option with a description like "Run validation across every skill, then drill into individual reviews."

**When a single skill is selected:**
Proceed to Phase 1 with that skill.

**When "Review all skills" is selected:**

1. Run Phase 2 (Automated Validation) on every skill, collecting pass/fail results
2. Present a summary table showing each skill's validation status at a glance
3. Highlight any skills with critical failures (banned words, broken frontmatter, missing files)
4. Ask the user which skills need full review (Phase 3+), or whether to review all that failed validation

This batch approach avoids drowning the user in 20 separate review reports. Surface the problems first, then go deep where it matters.

### Phase 1: Initial Assessment

**Ask the user about review goals:**

Use AskUserQuestion to clarify:

- **Review scope**: Full review or specific areas (format, voice, structure)?
- **Priority concerns**: What's most important to fix?
- **Target models**: Which models should this work with?
- **Breaking changes OK**: Can we change the skill behavior, or just polish?

**Example questions:**
```
What aspects of the skill concern you most?

Are you looking for a full review, or focusing on specific areas?

Can we make breaking changes to improve the skill, or should we keep behavior unchanged?
```

### Phase 2: Automated Validation

**Run all quality gate checks:**

1. **Format validation:**
   ```bash
   bash tests/scripts/simple-validate.sh .claude/skills/skill-name/SKILL.md
   ```

   Check:
   - Valid YAML frontmatter
   - Name matches directory
   - Description under 1024 chars
   - Proper structure

2. **Voice compliance:**
   ```bash
   python3 tests/scripts/check-voice-compliance.py .claude/skills/skill-name/SKILL.md
   ```

   Check:
   - No banned words in content
   - Uses contractions naturally
   - Avoids AI-tell patterns
   - Lists don't have exactly 3 or 5 items

3. **Structure check:**
   - SKILL.md exists with frontmatter
   - tests/eval.yaml present
   - At least 2 test cases in tests/cases/
   - References (if any) are one level deep
   - Scripts (if any) are documented

4. **Size check:**
   ```bash
   wc -l .claude/skills/skill-name/SKILL.md
   ```

   Should be < 500 lines (body only, excluding frontmatter)

Report validation results to the user before proceeding. Don't skip straight to analysis.

### Phase 3: Quality Analysis

**Review against best practices:**

#### Description Quality

Check the description field:

- [ ] Includes WHAT the skill does
- [ ] Includes WHEN to use it
- [ ] Includes trigger keywords
- [ ] Written in third person
- [ ] Under 1024 chars
- [ ] Specific, not vague

**Bad description:**
```yaml
description: Helps with documents
```

**Good description:**
```yaml
description: >-
  Extracts text and tables from PDF files, fills forms, merges documents.
  Use when working with PDF files or when user mentions PDFs, forms, or
  document extraction.
```

#### Content Conciseness

Check if content isn't overdoing it:

- [ ] Assumes Claude is smart (no over-explaining)
- [ ] Challenges each sentence ("Does Claude need this?")
- [ ] Removes unnecessary background information
- [ ] Gets to the point quickly

#### Progressive Disclosure

Check if skill properly uses progressive disclosure. It's one of the most important patterns:

- [ ] Main SKILL.md is overview/navigation (< 500 lines)
- [ ] Detailed content in references/ files
- [ ] References are one level deep (no nested refs)
- [ ] Large reference files have table of contents
- [ ] Scripts for deterministic operations
- [ ] Clear distinction: execute vs read scripts

#### Voice and Style

Check writing quality:

**MUST have:**
- [ ] Contractions ("don't", "you'll", "it's")
- [ ] Addresses reader as "you"
- [ ] Varied sentence length
- [ ] Conversational tone
- [ ] Active voice

**MUST NOT have:**
- [ ] Banned words (utilize, leverage, robust, comprehensive, seamless, delve, synergy, cutting-edge, holistic, pivotal, paramount, endeavor) <!-- voice-ok -->
- [ ] "In conclusion", "Overall", "In summary" <!-- voice-ok -->
- [ ] Lists with exactly 3 or 5 items
- [ ] "The user" (should be "you")
- [ ] Overly formal language

#### Interactive Input Patterns

For skills that need input from the user, check:

- [ ] `AskUserQuestion` present in `allowed-tools` frontmatter (if absent, Claude literally can't call it)
- [ ] Skill body calls `AskUserQuestion` explicitly — not prose like "ask the user what they want"
- [ ] Research happens *before* any `AskUserQuestion` call — options are pre-populated from scanning project state
- [ ] Questions offer concrete choices derived from discovered files, gaps, or existing patterns
- [ ] Skill doesn't ask what it could have found by scanning the codebase itself

**Anti-pattern (open-ended ask, no research):**
```markdown
Ask the user: "What would you like to create?"
```

**Good (research-first, pre-populated options):**
```markdown
Scan .claude/skills/ to find gaps, then use AskUserQuestion with options:
  (a) Extend skill-X (overlaps with what you described)
  (b) Fill the gap in domain Y (nothing covers this yet)
  (c) Something else — describe it
```

#### Workflow Patterns

Check if complex workflows aren't missing:

- [ ] Have clear steps
- [ ] Include checklist for tracking progress
- [ ] Show feedback loops for quality-critical tasks
- [ ] Use conditional branching when appropriate

#### Hook Implementations

If skill includes hooks (especially Stop hooks), verify:

- [ ] Stop hooks check `stop_hook_active` to prevent infinite loops
- [ ] Hook script calls `os.chdir(hook_input["cwd"])` immediately after reading input — without this, all `Path()` checks run against the hook process launch directory, not the project
- [ ] Language detection returning `"unknown"` doesn't cause early exit — language-agnostic checks (docs, TODOs, secrets) must still run; only language-specific tool invocations should be skipped
- [ ] Gap messages write to stderr (>&2), not stdout
- [ ] Exit codes are correct: 0 = complete, 2 = continue with feedback
- [ ] Hook scripts are executable (chmod +x)
- [ ] Hooks reference correct script paths with `$CLAUDE_PROJECT_DIR`
- [ ] Hook behavior is documented in SKILL.md

See `references/hook-patterns.md` for complete patterns and templates.

#### Examples and Templates

Check if skill provides:

- [ ] Concrete examples (not abstract)
- [ ] Input/output pairs where helpful
- [ ] Templates when format matters
- [ ] Examples show realistic usage

#### Configuration Patterns

Check if the skill uses proper settings patterns when dealing with config files:

- [ ] Single `settings` option for structured config (JSON/YAML/TOML/INI)
- [ ] Not using multiple individual options to build config files
- [ ] Config generation uses format libraries where available
- [ ] Flexible for users to add arbitrary config keys

**Anti-pattern (multiple options building a config file):**

```yaml
# Bad: Individual options that get assembled into JSON
options:
  serverPort: 8080
  serverHost: "0.0.0.0"
  logLevel: "INFO"
  maxConnections: 100
  # ... then these get manually assembled into config.json
```

**Better (settings pattern):**

```yaml
# Good: Single settings option that maps to config format
settings = {
  server = {
    port = 8080;
    host = "0.0.0.0";
  };
  logging.level = "INFO";
  connections.max = 100;
  # Users can add any valid config keys
}
```

This applies to skills that generate config files and to tools/systems being configured. If you spot multiple options being used to construct a JSON/YAML/TOML file, recommend consolidating to a single `settings` option that directly maps to the target format.

**Why this matters:**
- More maintainable (one place to look)
- More flexible (users aren't limited to predefined options)
- Easier to document (point to upstream config docs)
- Less code to maintain

#### Testing

Check test quality:

- [ ] At least 2 test cases present
- [ ] tests/eval.yaml exists and is valid
- [ ] Test cases cover main use cases
- [ ] Assertions check expected behavior
- [ ] LLM-rubric tests for quality

### Phase 4: Provide Feedback

**Structure feedback by priority:**

#### Critical Issues (must fix)
- Format validation failures
- Voice violations (banned words)
- Missing required files
- Over size limit (> 500 lines)
- Broken references or structure

#### Important Issues (should fix)
- Description quality problems
- Missing contractions or poor voice
- Lists with exactly 3 or 5 items
- Lack of progressive disclosure
- Missing or poor test cases
- Over-explanation or verbosity

#### Suggestions (nice to have)
- Better examples or templates
- Improved organization
- Additional reference files
- Enhanced workflows
- Better naming or structure

**Provide specific, actionable feedback:**

Bad feedback:
```
The description could be better.
```

Good feedback:
```
The description is vague. Change:
  "Helps with documents"
To something specific like:
  "Extracts text and tables from PDF files, fills forms, merges documents.
   Use when working with PDF files or when user mentions PDFs, forms, or
   document extraction."
```

### Phase 5: Implementation Guidance

**After providing feedback, ask the user:**

Use AskUserQuestion:

```
Which issues should we prioritize?

Should I implement the fixes, or would you like to review the feedback first?

Are there any changes you disagree with or want to discuss?
```

**When implementing fixes:**

1. Start with critical issues
2. Move to important issues
3. Apply suggestions if user agrees
4. Re-run validations after each change — you don't want regressions

## Common Issues and Fixes

When you identify issues during review, refer to [references/common-issues.md](references/common-issues.md) for detailed before/after examples covering:

- Verbose content (over-explaining)
- Poor descriptions (vague, missing triggers)
- Missing contractions (formal tone)
- AI-tell patterns (exactly 3 or 5 items)
- Nested references
- No progressive disclosure
- Missing tests
- Banned words
- Weak workflows
- Config anti-pattern (multiple options instead of settings)

## Quality Checklist

Use this checklist when reviewing:

### Format and Structure
- [ ] Valid YAML frontmatter
- [ ] Name matches directory (lowercase-hyphens)
- [ ] Description under 1024 chars
- [ ] Description includes what + when + triggers
- [ ] SKILL.md body < 500 lines
- [ ] tests/eval.yaml exists
- [ ] At least 2 test cases present
- [ ] References one level deep
- [ ] Long references have table of contents

### Voice and Style
- [ ] Uses contractions naturally
- [ ] Addresses reader as "you"
- [ ] Varied sentence length
- [ ] Zero banned words in content
- [ ] No "In conclusion", "Overall", "In summary" <!-- voice-ok -->
- [ ] Lists have 2, 4, 6, or 7 items (not 3 or 5)
- [ ] Conversational and friendly
- [ ] Concise (no over-explaining)

### Interactive Input
- [ ] `AskUserQuestion` in `allowed-tools` (if skill asks users anything)
- [ ] Interactive steps call `AskUserQuestion`, not prose "ask the user"
- [ ] Research runs before questions — options pre-populated from project analysis
- [ ] No blank open-ended prompts for things Claude could discover by scanning

### Content Quality
- [ ] Assumes Claude is smart
- [ ] Gets to the point quickly
- [ ] Concrete examples (not abstract)
- [ ] Templates when format matters
- [ ] Workflows have clear steps
- [ ] Checklists for complex workflows
- [ ] Feedback loops for quality tasks
- [ ] Progressive disclosure used well
- [ ] Uses settings pattern for config files (not multiple options)
- [ ] Config generation leverages format libraries when available

### Testing
- [ ] Test cases cover main scenarios
- [ ] Assertions check expected behavior
- [ ] LLM-rubric for quality checks
- [ ] Tests use realistic prompts

## Reporting Results

**Structure your review report:**

### Summary

- Assessment level (Excellent / Good / Needs Work / Critical Issues)
- Top 2-4 strengths
- Top 2-4 issues to address

### Critical Issues

List issues that MUST be fixed:
- [ ] Issue with specific fix

### Important Issues

List issues that SHOULD be fixed:
- [ ] Issue with specific fix

### Suggestions

List nice-to-have improvements:
- [ ] Suggestion with reasoning

### Next Steps

Ask the user:
```
Which issues should we prioritize?

Would you like me to implement the fixes, or review the feedback first?

Any changes you disagree with or want to discuss?
```

## Script Path Resolution Review

When reviewing skills that include scripts, verify that script paths are correctly referenced. This is a common source of bugs when skills are used across different installation locations.

**Check for:**

1. **Correct environment variable usage**:
   - Project-local skills should use `$CLAUDE_PROJECT_DIR`
   - Global skills should use `$HOME`
   - Plugins should use `${CLAUDE_PLUGIN_ROOT}`

2. **Proper path quoting**:
   ```bash
   # Good: handles paths with spaces
   bash "$CLAUDE_PROJECT_DIR/.claude/skills/skill-name/scripts/validate.sh"

   # Bad: breaks on paths with spaces
   bash $CLAUDE_PROJECT_DIR/.claude/skills/skill-name/scripts/validate.sh
   ```

3. **Installation location documentation**:
   - Skill should document where it expects to be installed
   - If it only works in one location (project vs global), that should be clear

4. **Hook script paths**:
   - Check hooks in frontmatter reference scripts correctly
   - Verify scripts exist at the documented paths

5. **Fallback patterns** (if used):
   - Check that fallback logic is correct
   - Verify error messages are helpful when scripts aren't found

**Common issues:**

- Using relative paths like `./scripts/validate.sh` (breaks if CWD changes)
- Hardcoding paths like `/home/user/.claude/skills/` (not portable)
- Missing quotes around `$CLAUDE_PROJECT_DIR` or `$HOME`
- Not documenting which installation location is supported
- Scripts referenced but not included in skill directory

**When providing feedback:**

```markdown
❌ Bad: "The script paths need fixing"

✅ Good: "Script paths won't work for global installations. Change line 45:
   From: bash ./scripts/validate.sh
   To: bash \"$HOME/.claude/skills/skill-name/scripts/validate.sh\"

   Also document in the skill that it should be installed globally, not per-project."
```

**Add to quality checklist:**
- [ ] Scripts use correct environment variable for installation location
- [ ] Script paths are properly quoted
- [ ] Installation location is documented
- [ ] All referenced scripts exist in the skill directory
- [ ] Hook script paths (if any) are correct

## Writing Style

Apply `natural-writing-style` to all review output and findings.

Review feedback should be direct and specific — state what you found and where, not vague summaries. Provide concrete before/after examples. Don't claim a skill "passes" or is "complete" without actually running the validation scripts and checking the output.

## References

- Quality gates: `.claude/rules/quality-gates.md`
- Voice rules: `.claude/rules/writing-voice.md`
- Code style: `.claude/rules/code-style.md`
- [Agent Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [agentskills.io Specification](https://agentskills.io/specification)
- Example production skill: `.claude/skills/openbsd-knf-style/`
