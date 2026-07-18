---
name: security-assessment
description: >-
  End-to-end security assessment covering threat modeling, authentication and authorization
  flows, CWE/vulnerability identification, and attack surface analysis. Use when reviewing
  project security posture, conducting security audits, or designing secure systems. Triggers:
  threat model, security review, security audit, vulnerability assessment, attack surface,
  authn, authz, authentication, authorization.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Glob Grep Bash(find *) Bash(cppcheck *) Bash(clang *) Bash(cargo *) AskUserQuestion
---

# Security Assessment

Conduct end-to-end security assessments covering threat modeling, authentication/authorization design, vulnerability identification, and attack surface reduction.

## Quick Start

Security assessments follow a four-phase approach:

1. **Threat Modeling** — Define assets, threats, and trust boundaries
2. **Auth/Authz Review** — Analyze authentication and authorization flows
3. **Code-Level Review** — Identify CWEs and exploitable vulnerabilities (delegates to language-specific skills)
4. **Remediation** — Provide concrete guidance for improving security posture

Start by understanding the system architecture, then work through each phase systematically.

## When to Use This Skill

Use this skill when:

- Starting a security review or audit
- Designing security for a new system
- Investigating security posture or attack surface
- Reviewing authentication or authorization implementation
- User mentions: threat model, security review, security audit, vulnerability assessment, attack surface, authn, authz

Don't use this for:
- Language-specific code review (use c-security-review or rust-unsafe-ffi-review directly)
- Performance optimization
- General code quality review

## Assessment Workflow

Copy and track your progress:

```
Security Assessment Progress:
- [ ] Phase 0: Dependency Security Baseline (MANDATORY)
- [ ] Phase 1: Threat Modeling
- [ ] Phase 2: Authentication & Authorization Review
- [ ] Phase 3: Code-Level Security Review
- [ ] Phase 4: Remediation Guidance
```

### Phase 0: Dependency Security Baseline (MANDATORY)

**YOU MUST complete this phase BEFORE proceeding to threat modeling.**

This is a blocking requirement — outdated dependencies are a primary attack vector.

#### Step 0.1: Update All Dependencies

**CRITICAL:** Query actual package registries. Never rely on training data.

**Rust:**
```bash
cargo install cargo-edit  # If not installed
cargo outdated            # Check current state
cargo upgrade             # Update to latest
cargo update              # Update Cargo.lock
cargo audit               # Scan for vulnerabilities
```

**Go:**
```bash
go get -u ./...           # Update all dependencies
go mod tidy               # Clean up
govulncheck ./...         # Scan for vulnerabilities
```

**Python:**
```bash
pip list --outdated       # Check current state
pip install --upgrade -r requirements.txt
pip-audit                 # Scan for vulnerabilities
```

**JavaScript:**
```bash
npm install -g npm-check-updates
ncu -u                    # Update package.json
npm install               # Install updates
npm audit fix             # Fix vulnerabilities
```

**Ruby:**
```bash
bundle outdated           # Check current state
bundle update             # Update all gems
bundle audit check --update
```

#### Step 0.2: Verify No Outdated Dependencies

After updates, MUST verify:

- [ ] All dependencies at latest versions (verified with package registry)
- [ ] Zero known vulnerabilities (security audit clean)
- [ ] All tests still pass
- [ ] Breaking changes addressed

**Do NOT proceed** until this phase is complete.

### Phase 1: Threat Modeling

**Goal**: Understand what you're protecting and from whom.

#### Step 1.1: Identify Assets

Document what needs protection:

**Critical assets**:
- Data: User credentials, personal data, financial info, secrets, API keys
- Services: APIs, databases, admin interfaces
- Infrastructure: Servers, networks, build systems

**Asset inventory template** (save to `docs/security/assets.md`):
```markdown
# Asset Inventory

## Data Assets
- [ ] User credentials (passwords, tokens, sessions)
- [ ] Personal/sensitive data
- [ ] API keys and secrets
- [ ] Business-critical data

## Service Assets
- [ ] Public-facing APIs
- [ ] Admin interfaces
- [ ] Database services
- [ ] Authentication services

## Infrastructure Assets
- [ ] Production servers
- [ ] Build/CI systems
- [ ] Development environments
```

#### Step 1.2: Define Trust Boundaries

Map where trust transitions occur:

**Common boundaries**:
- External users → Application
- Application → Database
- Application → Third-party APIs
- Unauthenticated → Authenticated contexts
- User role → Admin role

For each boundary, document:
- What data crosses it
- What validation happens
- What trust assumptions change

#### Step 1.3: Identify Threats (STRIDE)

Use STRIDE framework to systematically identify threats:

| Category | Question | Example |
|---|---|---|
| **Spoofing** | Can attacker impersonate users/services? | Weak session tokens, missing signature validation |
| **Tampering** | Can attacker modify data in transit/rest? | Unvalidated inputs, missing integrity checks |
| **Repudiation** | Can attacker deny actions? | Missing audit logs, weak authentication |
| **Information Disclosure** | Can attacker access sensitive data? | Exposed secrets, verbose errors, missing access controls |
| **Denial of Service** | Can attacker make system unavailable? | No rate limiting, resource exhaustion |
| **Elevation of Privilege** | Can attacker gain unauthorized access? | Missing authz checks, privilege escalation bugs |

**Threat modeling checklist**: See [references/threat-modeling.md](references/threat-modeling.md) for detailed STRIDE analysis guide.

#### Step 1.4: Document Threat Model

Create `docs/security/threat-model.md` using this template from [assets/threat-model-template.md](assets/threat-model-template.md).

### Phase 2: Authentication & Authorization Review

**Goal**: Verify identity management and access control are secure.

#### Step 2.1: Authentication Flow Analysis

Map how users prove their identity:

**Check for**:
- [ ] Password requirements (length, complexity, hashing algorithm)
- [ ] Multi-factor authentication availability
- [ ] Session management (token generation, expiry, invalidation)
- [ ] Password reset flow security
- [ ] Account enumeration protection
- [ ] Brute force protection (rate limiting, lockouts)

**Common authentication vulnerabilities**:
- Weak password hashing (MD5, SHA1, bcrypt with low cost)
- Predictable session tokens
- Missing password reset token expiry
- Timing attacks in user lookup
- Missing rate limiting on login attempts

**Authentication patterns**: See [references/auth-patterns.md](references/auth-patterns.md) for secure implementations.

#### Step 2.2: Authorization Flow Analysis

Map how access decisions are made:

**Check for**:
- [ ] Authorization model (RBAC, ABAC, ACL)
- [ ] Permission checks at all entry points
- [ ] Consistent authorization enforcement
- [ ] Least privilege principle applied
- [ ] Horizontal privilege escalation prevention
- [ ] Vertical privilege escalation prevention

**Common authorization vulnerabilities**:
- Missing authorization checks (IDOR vulnerabilities)
- Client-side authorization only
- Inconsistent permission checks
- Over-privileged service accounts
- Confused deputy problems

**Test authorization**:
```markdown
For each sensitive operation:
1. Can unauthenticated users access it?
2. Can authenticated users access other users' data?
3. Can regular users access admin functions?
4. Are permission checks server-side?
```

#### Step 2.3: Trust Relationship Mapping

Document service-to-service trust:

**For each service interaction**:
- How does service A authenticate to service B?
- What permissions does service A have in service B?
- Can service A be compromised to attack service B?
- Are API keys/secrets properly scoped?

**Watch for**:
- Over-privileged service accounts
- Shared credentials across services
- Missing mutual TLS
- Ambient authority (confused deputy)

### Phase 3: Code-Level Security Review

**Goal**: Identify CWEs and exploitable vulnerabilities in implementation.

This phase delegates to language-specific security skills.

#### Step 3.1: Identify Codebase Languages

Scan the codebase to determine which languages are present:

```bash
find . -type f \( -name "*.c" -o -name "*.h" -o -name "*.rs" -o -name "*.py" -o -name "*.js" -o -name "*.go" \) | head -20 | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

#### Step 3.2: Delegate to Language-Specific Skills

Based on identified languages:

**C/C++ code**: Use `/c-security-review` skill
- Memory safety issues
- Buffer overflows
- Use-after-free
- Integer overflows
- Format string vulnerabilities

**Rust code**: Use `/rust-unsafe-ffi-review` skill
- Unsafe block soundness
- FFI boundary safety
- Lifetime violations
- Data race potential

**Other languages**: Apply general CWE checklist (see [references/cwe-top25.md](references/cwe-top25.md))

#### Step 3.3: Cross-Language Issues

Check for security issues that span languages:

**Configuration & secrets**:
- [ ] Secrets in code or version control
- [ ] Hardcoded credentials
- [ ] Insecure defaults
- [ ] Missing environment-based config

**Input validation**:
- [ ] SQL injection (parameterized queries?)
- [ ] Command injection (shell=True usage?)
- [ ] Path traversal (user-controlled paths?)
- [ ] XML/XXE injection

**Cryptography**:
- [ ] Weak algorithms (MD5, SHA1, DES)
- [ ] Custom crypto implementations
- [ ] Insecure random number generation
- [ ] Missing encryption at rest/in transit

**Dependencies**:
- [ ] Known vulnerabilities in dependencies
- [ ] Outdated packages
- [ ] Unnecessary dependencies

**Test effectiveness on security-critical code paths**:

Linters and SAST tools find patterns. Mutation testing and CRAP scoring find a class of issue neither catches: security-sensitive code that *looks* tested but isn't actually constrained by the test suite. Both are mandatory for security review of code that handles auth, crypto, input validation, or trust boundaries.

- [ ] **Mutation testing on security-touching changes** — zero surviving mutants on auth / crypto / input-validation / authorization code. Rust: `cargo mutants --in-diff <(git diff origin/main) --timeout-multiplier 2.0`. Python: `mutmut`. JS/TS: Stryker. Go: go-mutesting. C/C++: mull.
- [ ] **CRAP score on security-sensitive modules** — anything above 30 is a P1 finding (refactor or add tests before any change). Rust: `cargo crap --lcov lcov.info`. Java: crap4java. .NET: NDepend. The Savoia & Evans formula `comp² × (1 − cov)³ + comp` makes the high-complexity / low-coverage cells explode — exactly where attackers find unhardened paths.

See `.claude/rules/static-analysis.md` for the canonical tool table and `bugfix/references/reproducer-and-mutation.md` for the mutation-testing runbook.

See [references/owasp-top10.md](references/owasp-top10.md) for web-specific vulnerabilities.

### Phase 4: Remediation Guidance

**Goal**: Provide actionable improvements to security posture.

#### Step 4.1: Prioritize Findings

Categorize by severity and exploitability:

**Critical** (fix immediately):
- Unauthenticated access to sensitive data
- SQL injection or command injection
- Hardcoded secrets or credentials
- Missing authentication on admin functions
- Known CVEs in dependencies

**High** (fix soon):
- Weak cryptography
- Missing authorization checks
- Insufficient input validation
- Information disclosure
- Missing rate limiting

**Medium** (schedule for fixing):
- Weak password requirements
- Missing security headers
- Verbose error messages
- Missing audit logging

**Low** (address during refactoring):
- Defense-in-depth improvements
- Security hardening opportunities

#### Step 4.2: Provide Concrete Fixes

For each finding, provide:

**What's wrong**:
```
The login endpoint doesn't rate limit authentication attempts.
```

**Why it matters**:
```
Attackers can brute force passwords without restriction, compromising user accounts.
```

**How to fix it**:
```python
# Add rate limiting with a library like Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # existing login code
```

**Verification**:
```
Test: Attempt 10 login requests in 30 seconds. Should receive 429 after the 6th.
```

#### Step 4.3: Attack Surface Reduction

Identify opportunities to reduce attack surface:

**Remove unnecessary features**:
- Unused API endpoints
- Debug interfaces in production
- Unnecessary admin capabilities

**Restrict access**:
- Network segmentation
- IP allowlisting for admin interfaces
- Principle of least privilege for service accounts

**Harden configuration**:
- Disable unnecessary services
- Remove default credentials
- Enable security headers
- Configure CSP, HSTS, etc.

#### Step 4.4: Generate Security Report

Create `docs/security/findings.md` using template from [assets/findings-template.md](assets/findings-template.md).

Structure the report:
1. Executive summary (for non-technical stakeholders)
2. Threat model summary
3. Findings by severity
4. Remediation roadmap
5. Risk acceptance decisions
6. Security improvements implemented

## Examples

### Example 1: Web Application Security Assessment

**User request**: "Review the security of our Flask web app"

**Response**:
1. Identify assets (user data, API keys, session tokens)
2. Map trust boundaries (browser → Flask → PostgreSQL)
4. Review authentication (password hashing, session management)
6. Check authorization (permission checks on endpoints)
7. Scan for OWASP Top 10 issues (SQL injection, XSS, CSRF)
8. Review Flask-specific security (SECRET_KEY, debug mode off, security headers)
9. Generate findings report with prioritized fixes

### Example 2: Microservices Architecture Review

**User request**: "Assess security of our microservices setup"

**Response**:
1. Map service-to-service trust relationships
2. Review API authentication (JWT validation, API keys)
4. Check for over-privileged service accounts
6. Identify lateral movement opportunities
7. Review secrets management (are API keys in code?)
8. Check network segmentation
9. Provide service mesh security recommendations

## Validation Steps

Before completing assessment:

- [ ] Threat model document created and reviewed
- [ ] All STRIDE categories analyzed
- [ ] Authentication and authorization flows documented
- [ ] Language-specific security reviews completed
- [ ] CWE Top 25 checklist reviewed
- [ ] Findings categorized by severity
- [ ] Concrete remediation provided for each finding
- [ ] Attack surface reduction opportunities identified
- [ ] Security report generated

## References

- [Threat Modeling Guide](references/threat-modeling.md) — STRIDE methodology and threat analysis
- [CWE Top 25](references/cwe-top25.md) — Most dangerous software weaknesses
- [OWASP Top 10](references/owasp-top10.md) — Web application security risks
- [Authentication Patterns](references/auth-patterns.md) — Secure authentication implementations
- [OWASP Cheat Sheets](references/owasp-cheatsheets.md) — Key management, cryptography, trust boundaries
- [Threat Model Template](assets/threat-model-template.md) — Template for documenting threat models
- [Findings Report Template](assets/findings-template.md) — Template for security assessment reports

## Writing Style

Apply `natural-writing-style` to all findings reports, threat model documents, and remediation guidance.

Findings should be direct and actionable: name the specific endpoint, function, or configuration that's vulnerable. Don't claim a dependency is up to date without running the relevant audit tool and seeing clean output. State what phases were completed and what wasn't covered.

## Tool Integration

Use these tools during assessment:

**Static analysis**:
```bash
# C/C++ — cppcheck and clang static analyzer
cppcheck --enable=warning,style,performance,portability .
clang --analyze -Xanalyzer -analyzer-output=text src/*.c

# Rust — clippy with security lints
cargo clippy -- -W clippy::all -W clippy::pedantic

# Dependency scanning
cargo audit  # Rust
npm audit    # Node.js
pip-audit    # Python
```

**Secret scanning**:
```bash
# Check for committed secrets
git log -p | grep -i "password\|secret\|api_key\|token"
```

**Manual testing**:
- Try authentication bypass
- Test authorization boundaries
- Attempt SQL injection in inputs
- Check for path traversal
