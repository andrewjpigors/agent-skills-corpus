---
name: figma-read
description: Use when reading Figma designs for implementation or QA. Prefer deterministic REST/PAT extraction after policy approval and never expose token values.
---

# Figma Read

Use only after workspace policy approves Figma access from AI tooling.

## Workflow

1. Extract file key and node id from the Figma URL.
2. Read the Figma token from an approved local secret source at the moment of
   use. Never print it.
3. Fetch file or node JSON with `X-Figma-Token`.
4. Render target nodes at 2x when visual comparison is needed.
5. Summarize layout, components, tokens, states, and assets needed for the change.
6. Do not invent missing design states. Ask product/design or mark the gap.

Never commit Figma responses, screenshots, or token-bearing config unless the
repo explicitly expects that artifact.

