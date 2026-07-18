---
name: sensitive-surface-review
description: Use for cryptography, signing, key material, JWT, MFA, admin permissions, KYC / AML documents, payments, ledger postings, or any high-sensitivity code path. Pairs with sensitive-surfaces rule.
---

# Sensitive Surface Review

Use before and after changing sensitive behavior.

## Checklist

- What asset, identity, permission, or money-like state can be affected?
- Can this run twice? Can two triggers race?
- What happens if the first call succeeds but the response is lost?
- Which HTTP methods or transport operations are involved?
- What happens during logout/session transitions?
- Are secrets, PII, documents, tokens, or key material logged or exposed?
- Is there an explicit review requirement for this directory or module?

Unknown review requirements are blockers.

