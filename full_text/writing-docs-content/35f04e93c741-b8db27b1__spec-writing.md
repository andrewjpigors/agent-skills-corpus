---
name: spec-writing
description: >-
  Creates detailed implementation specifications before coding. Use when planning
  any non-trivial feature to break work into testable, bite-sized tasks.
license: MIT
metadata:
  version: 1.0.0
  author: Adapted from obra/superpowers
  source-skills: obra/superpowers/writing-plans
allowed-tools: Read Write AskUserQuestion
---

# Spec Writing

Don't start coding without a plan. A good spec breaks work into small pieces and makes it obvious when you're done.

## When to Use This Skill

- Planning a non-trivial feature before writing any code — anything that touches more than one file or requires a design decision
- Breaking down a large task into TDD-compatible chunks where each piece can be verified independently
- Before starting work on a new subsystem, API, or integration point where the shape of the solution isn't obvious
- When a previous attempt got stuck mid-implementation because the plan wasn't clear enough
- When handing off work to another developer and need a shared understanding of what "done" looks like

## Quick Start

If the feature's scope isn't clear yet, read any related files (README, existing code for context), then **use `AskUserQuestion`** to gather requirements: "What should this feature do, and what does 'done' look like? Any constraints I should know about (existing APIs, data models, dependencies)?"

A complete spec has:
1. **Goal** — What you're building and why
2. **Architecture** — How it fits into the existing system
3. **Tasks** — Step-by-step implementation plan
4. **Acceptance criteria** — How you'll know it's done

Each task should take 2-5 minutes to complete.

## Core Structure

### Header Section

Start with context:

```markdown
# Feature: User Authentication

## Goal
Add login/logout functionality with session management.
Users should be able to log in with email/password and stay logged in for 30 days.

## Architecture
- Authentication middleware intercepts requests
- Sessions stored in Redis with 30-day TTL
- Password hashing uses bcrypt with cost factor 12
- Frontend gets JWT token, stores in httpOnly cookie

## Tech Stack
- Express.js middleware
- Redis 7.x for session storage
- bcrypt for password hashing
- jsonwebtoken for JWT generation
```

### Task List

Break implementation into TDD-compatible tasks. Each task follows this pattern:

```markdown
## Task 1: Session Storage

**File:** `src/auth/session.js`

**Test (write this first):**
```javascript
describe('SessionStore', () => {
  it('should store session with 30-day expiration', async () => {
    const store = new SessionStore(redis);
    await store.create('user123', {email: 'alice@example.com'});

    const session = await store.get('user123');
    assert.equal(session.email, 'alice@example.com');

    const ttl = await store.getTTL('user123');
    assert.approximately(ttl, 30 * 24 * 60 * 60, 60); // ~30 days
  });
});
```

**Implementation:**
```javascript
class SessionStore {
  constructor(redisClient) {
    this.redis = redisClient;
  }

  async create(userId, data) {
    const key = `session:${userId}`;
    await this.redis.setex(key, 30 * 24 * 60 * 60, JSON.stringify(data));
  }

  async get(userId) {
    const data = await this.redis.get(`session:${userId}`);
    return data ? JSON.parse(data) : null;
  }

  async getTTL(userId) {
    return await this.redis.ttl(`session:${userId}`);
  }
}
```

**Verify:**
```bash
$ npm test -- session.test.js
PASS  src/auth/session.test.js
  SessionStore
    ✓ should store session with 30-day expiration (45ms)
```

**Commit:**
```bash
git add src/auth/session.js src/auth/session.test.js
git commit -m "add session storage with redis TTL"
```
```

## Writing Guidelines

### Make Tasks Atomic

```markdown
# GOOD - Single, testable unit
## Task: Validate email format
Test that validator rejects malformed emails.
Implement regex-based email validation.

# BAD - Too broad
## Task: Add authentication
Write login, logout, password reset, email validation, session management.
```

### Include Exact Code

Don't write pseudocode or "implement X." Show the actual code you want.

```markdown
# GOOD - Actual implementation
**Implementation:**
```python
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

# BAD - Vague description
**Implementation:**
Use a regular expression to validate the email format.
```

### Test First, Always

Every task starts with the test. It's the only way to know if your implementation actually works. Show what should fail, what should pass, and the exact error messages.

```markdown
**Test (RED):**
```python
def test_rejects_invalid_email():
    assert not validate_email("notanemail")
    assert not validate_email("missing@domain")
    assert not validate_email("@example.com")
```

**Run test (should fail):**
```bash
$ pytest test_email.py
NameError: name 'validate_email' is not defined
```

This proves the test works.
```

### Specify File Paths

Don't say "create a new file." Say exactly where it goes.

```markdown
# GOOD
**File:** `src/validators/email.py`

# BAD
**File:** In the validators directory
```

### Show Expected Output

For commands, show what success looks like:

```markdown
**Run migration:**
```bash
$ npm run migrate
Running migration: 001_create_users_table
✓ Table 'users' created
✓ Index 'idx_users_email' created
Migration complete.
```
```

## Task Template

Copy this for each task:

```markdown
## Task N: Brief Description

**File:** `path/to/file.ext`

**Test (write first):**
```language
[Complete test code showing what should work]
```

**Run test (verify RED):**
```bash
[Command and expected failure output]
```

**Implementation:**
```language
[Minimal code to make test pass]
```

**Run test (verify GREEN):**
```bash
[Command showing all tests pass]
```

**Commit:**
```bash
git add [files]
git commit -m "brief description"
```
```

## Validation Checklist

Before calling a spec complete:

- [ ] Goal is clear and specific
- [ ] Architecture describes how components fit together
- [ ] Every task has a test written before implementation
- [ ] Code examples are complete (not pseudocode)
- [ ] File paths are exact
- [ ] Commands include expected output
- [ ] Tasks are 2-5 minutes each (if longer, break them down)
- [ ] Spec follows DRY and YAGNI principles

## Common Mistakes

### Spec Is Too Abstract

**Bad:**
```markdown
## Task: Add database layer
Implement repository pattern with CRUD operations.
```

**Good:**
```markdown
## Task: Create user repository

**File:** `src/db/user-repository.js`

**Test:**
```javascript
it('should insert and retrieve user', async () => {
  const repo = new UserRepository(db);
  await repo.insert({email: 'alice@example.com', name: 'Alice'});
  const user = await repo.findByEmail('alice@example.com');
  assert.equal(user.name, 'Alice');
});
```
```

### Tasks Are Too Large

If a task takes more than 5 minutes, it's too big -- break it down:

```markdown
# TOO BIG
## Task: Implement authentication

# BETTER - Split into multiple tasks
## Task 1: Hash passwords with bcrypt
## Task 2: Store user credentials
## Task 3: Validate login credentials
## Task 4: Generate JWT tokens
## Task 5: Verify JWT middleware
```

## Writing Style

Apply `natural-writing-style` to the spec document itself and any explanatory prose.

Specs should be direct and concrete: use real file paths, actual function names, and exact test assertions. Don't describe what you intend to build in vague terms — show the code. When stating a spec is complete, verify against the validation checklist, not by feel.

## Resources

- `references/task-sizing.md` — How to break work into 2-5 minute increments
- `references/tdd-in-specs.md` — Integrating test-first workflow into specs
- `assets/spec-template.md` — Copy-paste template for new specs
