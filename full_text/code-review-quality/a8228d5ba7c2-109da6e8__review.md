---
name: review
description: Thorough code review with severity-based findings for security, bugs, performance, and maintainability
argument-hint: "<file-or-dir>"
---

Perform a thorough code review. Follow this systematic process:

## 1. Context Gathering
- Identify the programming language and framework
- Check for related test files
- Look for existing patterns in surrounding code
- Read any relevant CLAUDE.md or documentation

## 2. Analysis Categories

### Critical Issues (must fix)
- Security vulnerabilities (injection, XSS, CSRF, auth bypass)
- Data corruption risks
- Race conditions
- Resource leaks (memory, file handles, connections)
- Crashes or unhandled exceptions

### Bugs (likely problems)
- Logic errors
- Off-by-one errors
- Null/undefined handling
- Type mismatches
- Incorrect error handling

### Performance (optimization opportunities)
- Unnecessary allocations
- N+1 queries
- Missing caching opportunities
- Inefficient algorithms
- Blocking operations in async code

### Maintainability (code quality)
- Unclear naming
- Missing or misleading comments
- Complex conditionals
- Duplicated logic
- Violation of project patterns

## 3. Output Format

For each finding:

### [SEVERITY] Issue Title

**Location**: file:line_number

**Problem**: Clear description of the issue

**Impact**: What could go wrong

**Fix**: Concrete suggestion

## 4. Summary

End with:
- Total issues by severity
- Overall assessment (approve/request changes)
- Priority order for fixes
