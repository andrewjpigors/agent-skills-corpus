---
name: generated-artifact-sync
description: Use when generated files, mirrors, API clients, schemas, translations, or AI harness outputs may be stale. Regenerate from source and verify freshness.
---

# Generated Artifact Sync

Use when generated output is touched or suspected stale.

## Workflow

1. Identify the source artifact and generation command.
2. Confirm generated paths should not be hand-edited.
3. Run the repo generation command.
4. Run freshness/verification checks when available.
5. Repair consumers using mappers or wrappers, not casts.
6. Include source command, generated paths, and verification result in the final
   receipt.

