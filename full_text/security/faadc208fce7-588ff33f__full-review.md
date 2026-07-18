---
name: full-review
description: Code quality and security scanning in one comprehensive pass
argument-hint: "<file-or-dir>"
---

Perform a comprehensive review combining code quality analysis and security scanning in a single pass. For each file and function, check BOTH logic issues AND security concerns.

## 1. Context Gathering

- Identify the programming language and framework
- Check for related test files
- Look for existing patterns in surrounding code

## 2. Code Quality Analysis

For each file, check:
- Critical: security vulns, data corruption, race conditions, resource leaks, crashes
- Bugs: logic errors, null handling, type mismatches, error handling
- Performance: N+1 queries, unnecessary allocations, blocking async ops
- Maintainability: naming, complexity, duplication, pattern violations

## 3. Security Scan

In the same pass, check for:
- Hardcoded secrets (AWS keys, Stripe keys, GitHub tokens, private keys, DB URLs)
- Sensitive data patterns (SSN, credit cards, internal IPs)
- Security anti-patterns (SQL injection, unvalidated input, permissive CORS)
- .gitignore coverage for sensitive files

## 4. Output

### Code Quality Findings
For each: [SEVERITY] Title, Location, Problem, Impact, Fix

### Security Findings
For each: [SEVERITY] Title, Location, Pattern, Risk, Remediation

### Summary
- Code quality: counts by severity
- Security: counts by severity
- Overall: approve/request changes
- Priority order (security critical first)
