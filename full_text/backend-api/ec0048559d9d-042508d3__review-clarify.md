---
name: review-clarify
description: The clarify loop protocol — asking questions until intent is unambiguous
license: MIT
compatibility: opencode
metadata:
  audience: all-agents
  workflow: clarify-phase
---

## Clarify Loop Protocol

The clarify phase resolves ambiguity discovered during analysis. The agent asks
questions until every change in the diff has a clear, stated intent.

### When to Enter the Clarify Loop

Triggers (any of these):
- New endpoint, capability, or public interface with no matching convention or spec
- A pattern that contradicts an existing convention
- Ambiguous intent — multiple valid interpretations of a change
- First time seeing a pattern — no convention or history covers it
- A change that seems unrelated to the stated purpose of the MR/diff
- Removal of code with no obvious reason

### How to Ask

1. **State what you observe** in the diff (quote the relevant lines)
2. **State what you expected** based on rules, conventions, or specs
3. **Present the ambiguity** clearly — what are the possible interpretations?
4. **Ask one question at a time** — do not batch
5. **Present options** when possible, with tradeoffs for each

### Examples

```
I see you added a retry loop in handle_request() with a max of 3 attempts
and no backoff. The project doesn't have a convention for retry behavior.

Is this:
(a) A temporary workaround for a flaky upstream service
(b) The intended retry policy going forward

If (b), should I record a convention about retry behavior?
```

```
This MR removes the validate_input() call from the create endpoint.
Convention API-003 says "All API endpoints must validate input before processing."

Was this intentional? If so, what replaces the validation?
```

### Stop Condition

The clarify loop ends when ALL of the following are true:
- Every change in the diff has a clear, stated intent
- No contradictions with existing conventions remain unresolved
- All new patterns have been either explained or proposed as conventions
- The human has not raised new concerns

### After Each Answer

Evaluate whether the answer reveals:
1. A **new convention** worth recording — if so, transition to the learn phase
2. A **one-time exception** — note it in the review report but do not record
3. A **correction to an existing convention** — propose updating it

### Anti-Patterns

Do NOT:
- Ask questions the diff already answers (read carefully first)
- Ask about style preferences covered by existing conventions
- Re-ask questions answered in the history for similar diffs
- Ask more than one question at a time
- Ask leading questions that assume the answer
