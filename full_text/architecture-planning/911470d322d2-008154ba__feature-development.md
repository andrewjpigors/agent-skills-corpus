---
name: feature-development
description: >-
  Systematic workflow for implementing new features from requirements to deployment.
  Use when adding significant functionality that requires planning, testing, and integration.
license: MIT
metadata:
  version: 2.0.0
  author: Original skill, extended for architecture context
allowed-tools: Read Write Edit Glob Grep Bash(ls *) Bash(find *) Bash(mkdir *) Task(Explore) AskUserQuestion Bash(cargo *) Bash(npm *) Bash(pytest *)
---

# Feature Development

## When to Use This Skill

- You're starting work on a non-trivial feature that will touch multiple files or systems
- Requirements are unclear and you need a structured process to clarify and plan before coding
- You've been asked to add functionality that needs architecture decisions documented
- A feature has security implications that require a threat model update
- You want to ensure implementation has complete test coverage and review before merging

Build features systematically from requirements through deployment. Plan, test, implement, review, ship — with architecture documentation evolving alongside code.

## Quick Start

The workflow:
1. **Discover current state** — Explore codebase, understand patterns (see `references/discovery-guide.md`)
2. **Assess architecture** — Review specs, ADRs, threat models for context (see `references/architecture-assessment.md`)
3. **Understand requirements** — Clarify what's needed
4. **Write spec** — Break work into testable tasks (use `spec-writing` skill)
5. **Create architecture artifacts** — Document decisions, update threat models (see `references/artifact-creation-guide.md`)
6. **Implement with TDD** — Test-first for each task (use `tdd-workflow` skill)
7. **Review** — Security and code quality checks (use `code-review` skill)
8. **Ship** — Merge, deploy, verify, update docs

Each phase has clear done criteria. Use the architecture checklist (`assets/architecture-checklist.md`) to track progress.

## Phase 0: Discover Current State

**YOU MUST complete this before gathering requirements.**

Understand what exists before planning what to build.

### Step 1: Explore Codebase

Use Task tool with Explore agent for "where" questions:

```
Task(
  subagent_type="Explore",
  thoroughness="medium",
  prompt="Find all authentication code: login, logout, session management, password handling. Document patterns, libraries, test coverage."
)
```

Or use direct tools for focused searches:
```bash
Glob: src/auth/**/*.{js,ts,py,rs}
Grep: "password.*reset" --output_mode content -C 3
```

**Document:**
- Existing similar features
- Architecture patterns in use
- Libraries and frameworks
- Code conventions
- Test coverage approach

### Step 2: Review Documentation

Check ALL relevant docs:
- [ ] `README.md` — project overview, conventions
- [ ] `CLAUDE.md` or `.claude/CLAUDE.md` — dev practices
- [ ] `docs/architecture/` or `docs/specs/` — system design
- [ ] `docs/api/` — API documentation
- [ ] `docs/adr/` — architecture decisions (if they exist)
- [ ] `docs/threat-models/` — security analysis (if exists)

**Note:** What's documented, what contradicts code, what's missing.

### Step 3: Conduct Gap Analysis

Create gap analysis using template at `references/gap-analysis-template.md`.

**Key questions:**
- What exists and works?
- What exists but doesn't work?
- What's missing that we need?
- What are the dependencies and risks?

For automated gap detection, use `implementation-review` skill.

### Step 4: Clarify Ambiguities

Use AskUserQuestion for unclear items:
- Conflicting docs vs code
- Multiple possible approaches
- Unclear requirements
- Missing context for decisions

Don't guess. Ask.

### Quality Gate: Phase 0 Complete

**ALL boxes must be checked:**

- [ ] Explored codebase (documented findings)
- [ ] Read relevant documentation (noted gaps)
- [ ] Analyzed current implementation (file list, test coverage)
- [ ] Created gap analysis (current vs desired state)
- [ ] Clarified ambiguities with user

**Evidence:** File lists, doc summaries, gap analysis document, user confirmations.

See `references/discovery-guide.md` for detailed techniques and examples.

## Phase 0.5: Assess Architecture Context

**Gate check:** Phase 0 must be complete.

Before requirements gathering, understand what architecture documentation exists.

### Step 1: Scan for Architecture Artifacts

```bash
# Find specs
find docs/ -name "*spec*.md" -o -name "FR-*.md"

# Find ADRs (Architecture Decision Records)
ls docs/adr/*.md 2>/dev/null

# Find threat models
ls docs/threat-models/*.md 2>/dev/null
```

**Record:**
- Number of each artifact type
- Last modification dates
- Directory organization

### Step 2: Assess Quality

For each artifact type (specs, ADRs, threat models), rate 0-2 on:
- **Completeness** — Has required sections?
- **Freshness** — Updated within 3 months?
- **Cross-references** — Links between docs (FR-NNN ↔ ADR-NNNN ↔ TM-XXX)?
- **Traceability** — Code references doc IDs?

**Healthy score:** 6-8 out of 8. Below 4 needs attention.

### Step 3: Identify Relevant Artifacts

Not all docs matter for your feature. Focus on:
- Specs covering subsystems you're modifying
- ADRs about tech you'll use
- Threat models for components you're touching

### Step 4: Determine Create vs Update

**Outcomes:**
- **Healthy docs** → Plan to update existing in Phase 2.5
- **Stale docs** → Plan to update + cross-reference
- **Partial coverage** → Create new artifacts for gaps
- **No docs** → Consider `all-aboard` skill for project-wide setup

### Quality Gate: Phase 0.5 Complete

- [ ] Scanned for specs, ADRs, threat models
- [ ] Assessed quality (completeness, freshness, cross-refs, traceability)
- [ ] Identified artifacts relevant to feature
- [ ] Determined create vs update plan for Phase 2.5
- [ ] Documented findings (use template at `references/architecture-assessment.md`)

**Time budget:** 10-20 minutes

See `references/architecture-assessment.md` for quality matrix, validation scripts, and assessment template.

## Phase 1: Understand Requirements

**Gate check:** Phases 0 and 0.5 complete.

Clarify what needs to be built.

**Key questions:**
- What problem does this solve?
- Who is the user?
- What's the expected behavior?
- What are edge cases?
- What's out of scope?
- How will success be measured?

**Document answers in structured format** — see Phase 0 gap analysis or create requirements doc.

**Example:**
```markdown
## Feature: Password Reset

**Problem:** Users can't log in when they forget passwords.

**User:** Any registered user.

**Expected behavior:** Click "Forgot Password" → receive reset link → set new password.

### Edge Cases
- Email doesn't exist → Show generic message (don't leak user info)
- Token expired → Show error, offer to resend
- Token already used → Show error, offer to resend
- User already logged in → Redirect to dashboard

### Out of Scope
- SMS-based reset (future work)
- Security questions (not implementing)
- Admin password reset (separate feature)

### Success Metrics
- Support tickets for password issues drop 75%
- 90%+ of reset attempts succeed
- Process takes <2 minutes average
```

## Phase 2: Write a Spec

Create a detailed plan before coding. See the `spec-writing` skill for complete guidance.

**Spec should include:**
- Goal and architecture
- Task breakdown (2-5 min per task)
- Test code for each task (write before implementation)
- Expected file changes
- Commit strategy

**Example task from spec:**
```markdown
### Task 1: Generate Reset Token

**File:** `src/auth/reset-token.js`

**Test:**
```javascript
it('should generate unique token with 1-hour expiration', async () => {
  const token = await generateResetToken('user@example.com');

  assert.match(token, /^[a-f0-9]{64}$/);  // 256-bit hex

  const data = await getTokenData(token);
  assert.equal(data.email, 'user@example.com');
  assert.approximately(data.expiresAt, Date.now() + 3600000, 1000);
});
```
```

Reference spec items with FR-NNN IDs for traceability.

## Phase 2.5: Create Architecture Artifacts

**Gate check:** Phase 2 spec is written.

Document decisions and security implications as you plan the feature.

### Step 1: Identify What to Document

After writing spec, answer:
- [ ] Did I choose between alternatives? → Create ADR
- [ ] Did I add security-sensitive logic? → Update threat model
- [ ] Did I make architectural assumptions? → Create ADR
- [ ] Did I cross trust boundaries? → Update threat model

### Step 2: Create ADRs

For each architectural decision:
- Use `adr-create` skill or MADR template
- Document alternatives considered
- State rationale for choice
- List consequences (positive + negative)
- Reference spec (FR-NNN) and threats (TM-XXX)
- Save to `docs/adr/NNNN-decision-title.md`

**Time:** 10-15 min per ADR

### Step 3: Update Threat Model

For security-relevant features:
- Identify components affected
- Run STRIDE analysis
- Score threats with DREAD
- Define mitigations as spec requirements (FR-NNN)
- Document residual risk
- Cross-reference spec and ADRs

Use `threat-model-create` skill for templates and scoring.

**Time:** 15-20 min

### Step 4: Cross-Reference Everything

Ensure bidirectional links:
- [ ] Spec mentions ADR-NNNN and TM-XXX
- [ ] ADR mentions FR-NNN and TM-XXX
- [ ] Threat model mentions FR-NNN and ADR-NNNN
- [ ] Plan to add FR-NNN to code comments

**Validation script:** See `references/cross-reference-patterns.md`

### Quality Gate: Phase 2.5 Complete

- [ ] Created ADRs for decisions (1-2 typical)
- [ ] Updated threat model if security-relevant (2-4 entries typical)
- [ ] Cross-referenced all artifacts bidirectionally
- [ ] Spec has FR-NNN IDs, references ADRs and threats
- [ ] Used architecture checklist (`assets/architecture-checklist.md`)

**Time budget:** 30-45 min total

See `references/artifact-creation-guide.md` for ADR/threat model examples, ID conventions, and when-to-create guidance.

## Phase 3: Implement with TDD

**Gate check:** Phases 2 and 2.5 complete.

Follow test-driven development. Use `tdd-workflow` skill for details.

**For each task:**
1. Write failing test
2. Verify it fails for the right reason
3. Write minimal code to pass
4. Run all tests (must be green)
5. Refactor if needed
6. Commit with FR-NNN reference

**Example commit:**
```bash
git add src/auth/reset-token.js tests/auth/reset-token.test.js
git commit -m "add reset token generation (FR-042, ADR-0048)"
```

**Don't skip ahead.** Implement tasks in order. Small commits make review easier.

**Add cross-references in code:**
```rust
// FR-042: Secure token storage (ADR-0048, mitigates TM-AUTH-006)
fn store_token(token: &str) -> Cookie {
    Cookie::build("reset_token", token)
        .http_only(true)  // TM-AUTH-006: prevent XSS
        .secure(true)     // FR-043: HTTPS only
        .finish()
}
```

## Phase 4: Code Review

**Gate check:** Phase 3 implementation complete, all tests pass.

Review before merging. Use `code-review` skill for complete checklists.

**Self-review first:**
- [ ] All tests pass
- [ ] No commented-out code or debug statements
- [ ] Code follows project style
- [ ] Functions have clear names
- [ ] Edge cases tested
- [ ] Security checks (injection, XSS, auth)

**Request review:**
```markdown
## Review Request: Password Reset Feature

**Spec:** docs/specs/password-reset-spec.md (FR-040 through FR-052)
**ADRs:** ADR-0048 (reset tokens), ADR-0049 (email service)
**Threat model:** TM-AUTH-006, TM-AUTH-007

**Changes:**
- POST /api/auth/reset-password endpoint
- Email template for reset link
- Token generation (FR-042, FR-043, FR-044)
- Database migration for reset_tokens table

**Testing:** 12 unit tests, 4 integration tests (all passing)

Please review for security (token generation, email validation) and error handling.
```

For security-sensitive features, use `security-assessment` skill instead of basic code review.

## Phase 5: Ship It

**Gate check:** Review approved.

**1. Final verification:**
```bash
# Run full test suite
npm test  # or cargo test, pytest, etc.

# Run linter
npm run lint

# Check dependencies
npm audit  # or cargo audit, pip-audit
```

**2. Merge:**
```bash
git checkout main
git pull origin main
git merge feature/password-reset
git push origin main
```

**3. Deploy:**
Follow project's deployment process (CI/CD, manual, etc.).

**4. Verify in production:**
- Test feature live
- Check error logs
- Monitor metrics (error rates, latency)
- Verify rollback plan

**5. Update documentation:**
- User-facing docs (if applicable)
- API documentation
- **Update architecture docs with final cross-references**
- Mark spec as completed

**Important:** If implementation deviated from plan, update ADRs or threat models to reflect what was actually built.

## Writing Style

All prose output (specs, ADRs, review requests, status updates) must follow `natural-writing-style` guidelines:

- Don't claim completion without listing what was verified and what wasn't
- Never estimate timelines; describe remaining tasks and dependencies instead
- Use contractions in review requests; keep them conversational
- Frame reviews around specific concerns ("review for security") not vague asks
- Avoid AI-tell words (see `natural-writing-style` for full blocklist)

## Common Pitfalls

See `references/common-pitfalls.md` for detailed examples.

**Quick summary:**
1. **Skipping Phase 0** — Don't start requirements before exploring codebase
2. **Skipping Phase 0.5** — Missing architecture context leads to undocumented decisions
3. **Coding too soon** — Write spec first
4. **Tests as afterthought** — Write tests first (TDD)
5. **Tasks too big** — Break into 2-5 min chunks
6. **No code review** — Always review (even self-review after break)
7. **Forgetting docs** — Update before marking complete
8. **Skipping Phase 2.5** — Architecture artifacts prevent future confusion

## Integration with Other Skills

**Core workflow:**
- `spec-writing` — Phase 2 (planning)
- `adr-create` — Phase 2.5 (document decisions)
- `threat-model-create` — Phase 2.5 (security analysis)
- `tdd-workflow` — Phase 3 (implementation)
- `code-review` or `security-assessment` — Phase 4 (quality check)

**Project-wide documentation:**
- `all-aboard` — Alternative when project has NO architecture docs (creates baseline)

**Optional:**
- `systematic-debugging` — If blocked during implementation
- `refactor` — If existing code needs cleanup first
- `spec-review` — Validate spec before implementation
- `adr-review` — Validate ADRs for quality
- `threat-model-review` — Validate threat model completeness

See `references/skill-integration.md` for skill composition patterns and when to use each.

## References

- `references/discovery-guide.md` — Phase 0 detailed techniques, code patterns, red flags
- `references/architecture-assessment.md` — Phase 0.5 quality matrix, assessment template
- `references/artifact-creation-guide.md` — Phase 2.5 ADR/threat model examples, ID conventions
- `references/cross-reference-patterns.md` — Bidirectional linking, validation scripts
- `references/gap-analysis-template.md` — Template for current vs desired state
- `references/common-pitfalls.md` — Recurring mistakes and fixes
- `references/skill-integration.md` — Which skills to combine, workflow patterns
- `assets/architecture-checklist.md` — Phase-by-phase progress tracking

