---
name: gitlab-patterns
description: Discover, record, and apply codebase patterns for GitLab development
license: MIT
---

## Purpose

This skill teaches agents to learn from the GitLab codebase by
discovering patterns, recording them as conventions, and applying
them consistently in future work.

## Discovering Patterns

When implementing something new, search for similar existing code:

1. Use gitlab_semantic_code_search with a description of what
   you're building, scoped to the relevant directory
2. Read the top 3 results
3. Identify what's consistent across them (the pattern)
4. Identify what varies (implementation-specific details)

## Recording Conventions

When you observe a consistent pattern across 3+ files, record it:

```yaml
# project/conventions/<area>.yml
conventions:
  - id: CONV-<AREA>-<NNN>
    pattern: "<what the code consistently does>"
    source: "<file paths where observed>"
    confidence: high|medium|low
    triggers:
      - "<when this convention applies>"
    example: "<shortest code example>"
```

### Confidence Levels

- **high**: 5+ files follow this pattern, aligns with docs
- **medium**: 3-4 files follow, may not be in docs
- **low**: 1-2 files, could be an exception

### Promoting Conventions

When a convention reaches high confidence and has been applied
3+ times without issue, it can be promoted to the framework
level in framework/review/rules/gitlab-conventions.yml.

## Applying Conventions

Before writing new code, check project/conventions/ for
relevant conventions. The axiom-guard and context-retriever
agents do this automatically for trigger-matched actions.

## Convention Areas

Conventions are organized by area:
- services.yml — Service class patterns
- finders.yml — Finder patterns
- graphql.yml — GraphQL type/mutation patterns
- frontend.yml — Vue component patterns
- database.yml — Migration patterns
- testing.yml — RSpec/Jest patterns
- policies.yml — Authorization patterns
