---
name: refactor
description: Identify refactoring opportunities with execution plan
argument-hint: "<file-or-module>"
---

Analyze the code for refactoring opportunities and propose improvements.

## 1. Current State Analysis
- Understand what the code does (not just how)
- Identify the code's responsibilities
- Map dependencies and coupling
- Note existing tests coverage

## 2. Identify Refactoring Opportunities

### Code Smells
- Long methods (>20 lines typically)
- Large classes (>200 lines typically)
- Long parameter lists (>4 parameters)
- Feature envy, data clumps, primitive obsession
- Duplicated code

### Structural Issues
- Deep nesting (>3 levels)
- Complex conditionals
- God objects
- Tight coupling
- Missing abstractions

## 3. Propose Refactorings

For each opportunity:
- Type: Extract Method / Extract Class / Rename / Move / etc.
- Show current vs proposed code
- Benefits and risks
- Verification steps

## 4. Execution Plan

Ordered list:
1. Safe refactorings first (renames, extracts with tests)
2. Structural changes
3. Risky changes last

Constraints:
- Preserve public API unless explicitly allowed to change
- Maintain backward compatibility
- Keep changes minimal and focused
