---
name: record-decision
description: Use when a meaningful technical, design, or scoping decision is made and should be captured (what was chosen, what was rejected, and why). Adds one conflict-free entry file under doc/decisions/entries/ following the towncrier pattern, and a numbered ADR for large architectural choices. Never hand-edits the generated decisions table in a feature PR/MR.
---

# Skill: Record a decision

Captures meaningful choices in the decision log. The canonical conventions live in
[`doc/decisions/DECISIONS.md`](../../doc/decisions/DECISIONS.md) and the ADR template in
[`doc/decisions/0000-adr-template.md`](../../doc/decisions/0000-adr-template.md).

## Decide the type
- **Small per-issue trade-off** (scope, a design choice, in/out of scope) → one **entry file**.
- **Large, long-lived architectural choice** → a numbered **ADR** *and* a small entry that
  points to it.

## Add an entry (the conflict-free path)
1. Create **exactly one** file in `doc/decisions/entries/`, named
   `YYYY-MM-DD-<issue>-<slug>.md` (decision date, primary issue number, lowercase-kebab slug).
2. Frontmatter with `date:` and `issue:` (`"#NN"`, or `"#NN/#MM"` for several issues),
   then a `## Decision` section and a `## Rationale` section. Extra sections
   (alternatives, notes) are allowed and stay in the entry file.
3. **Do not hand-edit the generated table** in `DECISIONS.md` inside a feature PR/MR.
   One entry file per PR/MR is the entire conflict-free trick — git has nothing to clash on.

See [`entries/0000-00-00-00-example-entry.md`](../../doc/decisions/entries/0000-00-00-00-example-entry.md)
for the shape.

## Add an ADR (large choices)
1. Copy `0000-adr-template.md` to the next number, e.g. `0001-<slug>.md`.
2. Fill in context, decision, consequences, and alternatives considered.
3. Add a short entry (steps above) whose Decision line references the ADR number.

## Rule of thumb
Record it if a future maintainer would ask "why was it done this way?" and the answer is not
obvious from the code or git history. Do not log trivia the repo already captures.
