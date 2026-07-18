---
name: decompose
description: Use when a task is large, vague, or has multiple valid approaches (cross-service redesign, contract change, migration with downstream effects, large client refactor). Runs the plan-restate-divide-reduce loop from Think Like a Programmer before any code is written.
---

# Decompose

A procedural skill for turning a large or vague task into a sequence of
small, named subproblems. Use BEFORE `planner` / `senior-architect` when
the task feels "I don't know where to start."

## The loop

Run these four steps in order. Stop at any step where you have a small
enough piece to hand to `planner` or implement directly.

### Step 1 — Restate

Write the problem in your own words, then list:

- **Inputs**: what the system already has when the task begins.
- **Outputs**: what must exist when the task is done.
- **Constraints**: business rules, performance bounds, deploy windows,
  legal/compliance, cross-service dependencies.
- **Operations available**: APIs, scripts, ORMs, services that can be
  modified. Be explicit - missed operations are the most common source
  of "impossible" problems.

If you cannot fill all four lists, the task is not coherent yet. Surface
the missing facts as questions for the user before continuing.

### Step 2 — Divide

Find a cut that splits the task into pieces that compose. Common cuts
in this codebase:

A good cut produces pieces that can be implemented and tested
independently, even if the final integration needs all of them.

Concrete examples:

- By service: piece A in service X, piece B in service Y.
- By layer: schema migration, repository, domain, controller, client.
- By flow phase: validate, persist, emit event, notify, audit.
- By time: synchronous response path, async consumer path.
- By blast radius: read-only changes first, then writes.

### Step 3 — Reduce

For each piece, ask: is there a smaller version of this piece that I
DO know how to solve? Common reductions:

- Drop a constraint (assume only one currency, one chain, one
  campaign).
- Drop a dimension (single user instead of N).
- Drop concurrency (sequential first, races second).
- Drop persistence (in-memory first, then DB).
- Drop the rare path (happy path first, edge cases as follow-up).

Solve the reduced version. Then re-introduce what you stripped, ONE
constraint at a time. Each re-introduction either succeeds (and you
keep going) or reveals exactly where the difficulty lives (and you
can name it precisely when asking for help).

### Step 4 — Find an analogy

Before you build anything new, ask: has this codebase solved a
structurally similar problem? Concrete prompts:

- A similar money flow likely exists somewhere already. Read it first.
- A similar idempotent Kafka consumer likely already exists. Read its
  dedup pattern.
- A similar ORM migration with the same shape probably already exists.
  Read the prefix style and the rolling-deploy story.
- A similar React state machine probably already exists. Read its
  reducer / listener middleware / state-machine library usage.

Port the pattern, do not transplant the code. Re-derive in the current
problem's vocabulary so the analogy is yours.

## Output of `decompose`

When the loop finishes, hand to the next skill / agent:

- The restated problem (inputs/outputs/constraints/operations).
- The cut (3-7 numbered subproblems).
- The reduced version for each subproblem.
- The analogy / prior pattern for each, with file path.
- Open questions for the user (if any).

The receiver (`planner`, `senior-architect`, or an implementer)
operates on the divided pieces, not the monolithic original task.

## Pairing

- `cognitive-heuristics` is the menu of named single moves. `decompose`
  is the procedural sequence.
- `verify-task` calls `decompose` when the request is ambiguous or
  high-risk.
- `orchestrate` step 3 calls `decompose` before producing the plan.
- `stuck-loop` returns the agent here when "no progress in 15
  minutes" is detected.
