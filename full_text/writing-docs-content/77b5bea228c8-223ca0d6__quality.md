---
name: quality
description: Quality scorecard for code, tests, and documentation rated 1-5
argument-hint: "<file-or-dir>"
---

Perform a quality assessment scoring three dimensions: code quality, test coverage, and documentation completeness.

## 1. Code Quality (Score 1-5)
- Structure: function length, class responsibilities, module organization
- Correctness: logic errors, edge cases, error handling, type safety
- Patterns: consistency with project conventions, appropriate idioms

## 2. Test Coverage (Score 1-5)
- Existence: do tests exist? what framework?
- Coverage: which public functions are tested vs untested?
- Quality: descriptive names, independent tests, AAA pattern, appropriate mocking

## 3. Documentation (Score 1-5)
- Code docs: docstrings on public APIs, type annotations, exception docs
- Comments: explain WHY not WHAT, no outdated comments, no commented-out code
- External: README, usage examples, architecture docs

## 4. Output

### Quality Scorecard
| Dimension | Score | Details |
|-----------|-------|--------|
| Code Quality | N/5 | Summary |
| Test Coverage | N/5 | Summary |
| Documentation | N/5 | Summary |
| **Overall** | **N/5** | |

### Top Improvements (Priority Order)
For each: category, current state, suggested change, impact on score

### Action Items
- Quick wins (< 5 min)
- Medium effort (15-30 min)
- Larger refactors (1+ hour)
