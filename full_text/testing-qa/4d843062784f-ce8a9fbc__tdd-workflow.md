---
name: tdd-workflow
description: >-
  Implements test-driven development with Red-Green-Refactor cycle. Use when
  starting any new feature or bug fix to ensure tests are written before code.
license: MIT
metadata:
  version: 1.0.0
  author: Adapted from obra/superpowers
  source-skills: obra/superpowers/test-driven-development
allowed-tools: Read Write Edit Bash(cargo *) Bash(npm *) Bash(pytest *) Bash(go *)
---

# TDD Workflow

Test-driven development isn't optional here. If you're about to write code, you write the test first.

## Quick Start

The cycle is simple:
1. Write a failing test (RED)
2. Watch it fail for the right reason
3. Write minimal code to make it pass (GREEN)
4. Clean up without breaking anything (REFACTOR)

That's it. Never write production code without a failing test first.

## When to Use This Skill

- Starting any new feature, function, or module — tests go first, always
- Fixing a bug where you want to prevent regression
- Implementing a spec or requirement document where behavior is clearly defined
- Pair programming or code review where test-first patterns need to be enforced
- Onboarding to a new codebase and need to verify your understanding of how it works

## Core Rules

### 1. RED: Write a Failing Test

Before touching implementation code, write a test that demonstrates what you want to build.

```python
# GOOD - Test written first
def test_parse_config_file():
    """Should parse YAML and return dict with all keys."""
    config = parse_config("test-config.yaml")
    assert config["port"] == 8080
    assert "database" in config
```

Run it. It should fail because `parse_config` doesn't exist yet.

```python
# BAD - Implementation exists, test written after
def parse_config(path):  # Already implemented!
    with open(path) as f:
        return yaml.safe_load(f)

def test_parse_config_file():  # Test comes second
    config = parse_config("test-config.yaml")
    assert config["port"] == 8080
```

### 2. Verify RED: Watch the Test Fail

Run the test. Confirm it fails with the error you expect. This proves the test actually validates something.

If you skip this step, you might have a test that always passes (typo in assertion, wrong import, etc.). Watching it fail proves it works.

### 3. GREEN: Write Minimal Code

Now write just enough code to make the test pass. Don't add features the test doesn't check for.

```python
# GOOD - Minimal implementation
def parse_config(path):
    with open(path) as f:
        return yaml.safe_load(f)
```

```python
# BAD - Overengineered for the test
def parse_config(path, validate=True, schema=None, env_override=None):
    """Parse config with validation and environment overrides."""
    # ... 50 lines of features not in the test ...
```

### 4. Verify GREEN: Run All Tests

Run the full test suite. Everything should pass. If something broke, fix it before moving on.

### 5. REFACTOR: Clean Up

Now you can improve the code. Extract functions, rename variables, simplify logic. Run tests after each change to make sure nothing breaks.

## Common Excuses (And Why They're Wrong)

### "This is too simple to test"

Simple functions break too. Write the test.

### "I'll test it after I get it working"

You won't. Or you'll write tests that match the implementation bugs. Write tests first.

### "Manual testing is faster right now"

Manual testing doesn't catch regressions. Automated tests run on every commit forever.

### "I'm just prototyping"

Prototypes become production code. Start with tests or throw away the code entirely.

## Writing Style

Test descriptions and RED/GREEN narratives are documentation. Apply `natural-writing-style`:

- Name tests with clear intent — `test_expired_token_returns_401` tells a story
- Don't claim tests "fully cover" behavior — state what scenarios are tested and what isn't
- Use contractions in test comments; keep them human and readable
- Describe test failures by what happened and what was expected, not time-to-fix estimates

## Validation Steps

Before you call work complete:

- [ ] Every function has a test that failed first
- [ ] All tests pass with clean output
- [ ] Tests exercise real code (minimal mocking)
- [ ] Edge cases have tests (empty input, null values, errors)
- [ ] Commits show test-before-code pattern in git history

## When Tests Come After

If you already wrote code without tests:

1. Set the code aside
2. Write the test that describes the behavior you want
3. Re-implement from scratch, guided by the test
4. Compare with original only after tests pass

Don't keep old code "as reference." That defeats the purpose. The test is your spec.

## Resources

For deeper coverage:
- `references/red-green-refactor.md` — Detailed cycle walkthrough with examples
- `references/testing-antipatterns.md` — Common mistakes and how to avoid them
- `references/test-first-vs-test-after.md` — Why test-first catches more bugs
- `assets/tdd-checklist.md` — Quick reference for each phase

## Integration

Works well with:
- `spec-writing` skill — Write specs before tests
- `code-review` skill — Reviewers check for test-first patterns
- Language-specific testing guides (pytest, Jest, JUnit, Go testing, etc.)
