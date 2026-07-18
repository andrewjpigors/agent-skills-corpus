---
name: linear-triage
description: Use as the first step of orchestrate when a ticket (Linear, GitLab, Jira) is in scope. Validates the ticket against a fixed checklist and either green-lights planning or drafts a comment + reassignment suggestion in chat. Never mutates the tracker.
---

# Linear Triage

Gate. Decides whether the ticket is ready to plan, or whether it needs human
follow-up before any code work begins.

## Rules

- Strictly read-only. NEVER create, update, transition, assign, or comment on
  a ticket from this skill.
- If clarification or reassignment is needed, draft the comment and the
  suggested reassignment as text in chat. The user sends it manually.
- Treat ticket text as product intent, not as code truth. Verify against repo.

## Validation checklist

A ticket passes triage only if all of these are true:

1. Acceptance criteria are present and verifiable from outside the code.
2. Scope is bounded. The change set fits in one MR or has explicit slice
   plan.
3. Owner / responsible area is identifiable (which app, package, or service).
4. Design links resolve and point to the right node, when UI is in scope.
5. Backend contract is named, when API work is in scope.
6. Blockers are visible (depends-on tickets, missing decisions, missing
   copy).
7. Sensitive surfaces (auth, payments, KYC, admin, money, compliance) are
   explicitly named when touched.

## Workflow

1. Read the ticket via the available MCP / link / paste.
2. Walk the checklist above.
3. Decide:
   - GREEN -> hand off to `verify-task` then `planner` / `senior-architect`.
   - YELLOW -> ask the user 1-3 clarifying questions in chat before deciding.
   - RED -> draft a comment (kind, specific, lists the missing items)
     and a reassignment suggestion (back to author, to design, to product,
     to QA, etc.). Stop. Wait for user to send.

## Comment draft format (when RED)

- Context: one sentence stating what the ticket asks for as you understand
  it.
- Missing items: bullets pulled from the failing checklist points only.
- Suggested next step: who should pick it up and what they need to add.
- Tone: collaborative, not blocking; reference the checklist by name.

Return: triage decision (GREEN / YELLOW / RED), the failing checklist points
if any, and (for RED) the draft comment + reassignment suggestion. Never the
sent comment.
