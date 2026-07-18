---
name: code-review-response
description: Process manual code review comments marked with "ISSUE:" prefix. Finds all ISSUE comments across the codebase (inline in code files and in markdown review files), evaluates whether each is a genuine issue, generates a structured markdown report with lessons learned, and removes the ISSUE comments from the source files. Use when you have added ISSUE comments during code review and want to document them for planning/PRD generation.
---

# Code Review Response

Process `ISSUE: ` comments from manual code reviews into a structured report.

## Workflow

1. **Search for issues**
   - Grep for `ISSUE:` in all files
   - Check inline code comments (may span two lines)
   - Check markdown review files

2. **For each issue found:**
   - Extract the issue description
   - Note file path and line number
   - Read surrounding code context
   - Evaluate validity (is this a real issue?)

3. **Generate report**
   - Create `resources/code-review/` directory if needed
   - Determine next file number (code-review-N.md)
   - Write structured report including lessons learned

4. **Clean up source files**
   - Remove all processed `ISSUE:` comments from code files
   - Remove multi-line issue comments completely
   - Delete any markdown review files that only contained issues

## Issue Evaluation

For each `ISSUE:` comment, assess:

- **Valid issue**: Explain the problem, affected code, and potential fix approach
- **Not an issue**: Explain why (e.g., intentional design, already handled elsewhere, false positive)

## Lessons Learned

After evaluating all issues, identify patterns and extract general lessons:

- **Recurring themes** - Issues that appear multiple times (e.g., missing error handling)
- **Knowledge gaps** - Areas where coding standards may need clarification
- **Best practices** - Patterns that should be documented for the team
- **Tooling opportunities** - Issues that linters or formatters could catch

Format lessons as actionable recommendations for coding standards documentation.

## Report Format

Output to `resources/code-review/code-review-N.md`:

```markdown
# Code Review Report

Generated: YYYY-MM-DD

## Summary

- Total issues found: X
- Valid issues: Y
- Non-issues: Z

## Valid Issues

### Issue 1: [Brief title]

- **File**: `path/to/file.py`
- **Line**: 42
- **Comment**: ISSUE: [original comment text]
- **Context**: [relevant code snippet]
- **Assessment**: [explanation of the problem]
- **Suggested approach**: [brief fix direction]

## Non-Issues

### Non-Issue 1: [Brief title]

- **File**: `path/to/file.py`
- **Line**: 15
- **Comment**: ISSUE: [original comment text]
- **Reason not an issue**: [explanation]

## Lessons Learned

### Coding Standards Recommendations

1. **[Category: e.g., Error Handling]**
   - Observation: [pattern observed across issues]
   - Recommendation: [specific guideline to add to standards]
   - Example: [code example demonstrating the recommendation]

2. **[Category: e.g., Documentation]**
   - Observation: [pattern observed]
   - Recommendation: [guideline]
   - Example: [code example]

### Suggested Linter Rules

- [Rule suggestion that could catch similar issues automatically]

### Training Opportunities

- [Topics where team knowledge could be improved]
```

## Finding Multi-Line Issues

Issue comments may span two lines:

```python
# ISSUE: This function is too complex and should be
# refactored into smaller units
def complex_function():
```

When the line after `ISSUE:` starts with `#` and continues the sentence, include it.

## Cleanup Rules

When removing ISSUE comments:

- **Single-line comments**: Delete the entire line
- **Multi-line comments**: Delete all continuation lines
- **Inline comments**: Remove only the ISSUE portion if other code exists on the line
- **Markdown files**: Delete issue entries; delete the file if empty after cleanup
- **Preserve formatting**: Maintain surrounding code structure and indentation
