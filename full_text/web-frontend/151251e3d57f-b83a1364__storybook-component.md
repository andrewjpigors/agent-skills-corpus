---
name: storybook-component
description: Use when building or refining reusable UI components with Storybook or equivalent component previews.
---

# Storybook Component

Use for component-level development when the repo has Storybook or an equivalent.

## Workflow

1. Inspect existing stories and component conventions.
2. Build a stateless component where practical.
3. Add stories for default, loading, empty, error, disabled, long text, mobile,
   and domain-risk states as applicable.
4. Use design system tokens and existing primitives.
5. Verify the story visually and run relevant component checks.

Do not add Storybook infrastructure from scratch unless explicitly scoped.

