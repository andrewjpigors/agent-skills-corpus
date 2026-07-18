---
name: hello-skill
description: Reference example showing the SKILL.md structure knackd expects. Use when authoring a new skill as a starting template.
---

# hello-skill

This is a minimal, valid Agent Skill. Copy this directory, rename it, and edit
the frontmatter (`name` must equal the directory name) and the body.

## When to use

Describe in the `description` above the situations where an agent should reach
for this skill — that text is what every agent semantic-matches against.

## Instructions

1. State the steps the agent should follow.
2. Keep the body focused; put long reference material in a `references/` folder
   next to this file (knackd symlinks those through to every agent).
