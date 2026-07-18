---
name: security-check
description: Scan for hardcoded secrets and sensitive data
argument-hint: "<file-or-dir>"
---

Perform a security scan for hardcoded secrets and sensitive data.

## 1. Scope Definition

Determine what to scan:
- Files provided by user (via @-mentions)
- Staged git changes: `git diff --staged`
- Specific directory or file patterns

## 2. High-Confidence Secret Patterns

Search for:
- AWS Access Keys: `AKIA[0-9A-Z]{16}`
- Stripe Keys: `sk[-_](live|test)_[A-Za-z0-9]{20,}`
- OpenAI Keys: `sk-[A-Za-z0-9]{32,}`
- GitHub Tokens: `gh[pousr]_[A-Za-z0-9_]{36,}`
- Slack Tokens: `xox[baprs]-[0-9-]{12,}-[a-zA-Z0-9]{24}`
- Google API Keys: `AIza[0-9A-Za-z_-]{35}`
- Private Keys: `-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----`

## 3. Medium-Confidence Patterns

Search for:
- Generic API key assignments: `api[_-]?key\s*[:=]\s*["'][^"']{16,}`
- Password assignments: `password\s*[:=]\s*["'][^"']{8,}`
- Database URLs with credentials: `(mysql|postgresql|mongodb)://[^:]+:[^@]+@`
- Internal IP addresses: `10\.`, `192\.168\.`, `172\.(1[6-9]|2[0-9]|3[0-1])\.`

## 4. Sensitive Data Check

Look for:
- SSN patterns: `\d{3}-\d{2}-\d{4}`
- Credit card patterns: `\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}`
- Real email addresses (non-example.com domains)

## 5. .gitignore Audit

Verify these patterns are ignored:
- `.env`, `.env.*`
- `*.pem`, `*.key`
- `*credentials*.json`, `*secrets*.json`
- `config/local.*`

## 6. Output Format

```markdown
# Security Scan Results

## Critical Findings
[CRITICAL] <pattern> found in <file>:<line>
- Action: <remediation>

## High Priority
[HIGH] <issue> in <file>:<line>

## Medium Priority
[MEDIUM] <issue>

## .gitignore Status
| Pattern | Ignored? |
|---------|----------|

## Summary
Critical: N | High: N | Medium: N
```
