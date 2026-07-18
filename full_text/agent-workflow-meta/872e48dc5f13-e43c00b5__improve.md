---
name: improve
description: Use when a repeated failure should become durable harness behavior - a Cursor rule, skill, hook script, subagent, template, or local note.
---

# Improve

Use after a task exposes repeatable friction.

## Workflow

1. Name the failure pattern.
2. Decide the smallest durable fix:
   - always-on rule for frequent high-impact behavior
   - scoped rule for file/subsystem patterns
   - skill for a workflow
   - script for deterministic checks
   - agent for bounded review/QA perspective
   - local note for workspace-specific facts not ready to share
3. Add or update the source artifact.
4. Run render, leak scan, and status.
5. Keep the change personal unless it is proven team-safe.

