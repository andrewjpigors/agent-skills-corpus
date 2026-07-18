---
name: cognitive-heuristics
description: Use when a task is ambiguous, a bug is mysterious, or you catch yourself making no progress. 25 named moves from Think Like a Programmer that turn "now what?" into a small menu of explicit techniques.
---

# Cognitive Heuristics

A small set of named, repeatable moves to apply when the task is hard.
Adapted from V. Anton Spraul's *Think Like a Programmer*. Use these
explicitly: name the move you are using out loud, then make it.

## The 25 moves

1. **Restate the problem** in your own words and list constraints + the
   set of operations available. Most "impossible" puzzles are missing an
   operation in the enumeration.
2. **Plan, however roughly.** Without intermediate goals, every minute
   feels like a failure. Disposable plans beat no plan.
3. **Divide the problem.** Two pieces are usually less than half as hard
   as the whole. Write the pieces sequentially first, nest second.
4. **Reduce.** Strip a dimension, lower the count, fix a parameter, or
   drop a constraint. Solve the reduced version; then re-introduce
   what you stripped.
5. **Start with the most-constrained variable.** Sudoku rule: the cell
   with one possible value is where you start. Shrinks search space
   fastest.
6. **Start with what you know.** Even partial code "may stimulate your
   imagination" - seeing your own structure on screen unlocks moves.
7. **Look for an analogy.** Has anything you've solved before had this
   shape? Open that file. Don't try to remember it.
8. **Manufacture an analogy.** If no prior problem fits, invent a
   simpler synthetic problem that isolates the unknown, solve it, then
   port the solution back.
9. **Write a sample case first.** Pick nontrivial input, write down
   ALL inputs and expected outputs, then write code that transforms
   the first into the second.
10. **Draw the before/after state.** Especially for pointer, memory,
    list, queue, or graph work. Annotate what is invariant.
11. **Solve "compute both ways".** When an early commitment is
    impossible (e.g. Luhn length unknown), maintain BOTH candidate
    answers and decide at the end.
12. **Experiment in isolation.** Build a tiny separate program for the
    unknown piece. Don't probe behavior inside the half-built real
    solution.
13. **Difference tables.** When two sequences "look related," tabulate
    (input, output, candidate formula, delta) and look for a constant.
14. **Verify pointer identity, not just value equality.** When things
    should be distinct, prove they are. Cross-linking bugs hide in
    "looks the same."
15. **Pair every `new` / `open` / `connect` with its release at
    allocation time.** Lifetime is a programmer-managed property; state
    both endpoints up front.
16. **Trust recursive (or subagent, or library) calls** as if they
    were unrelated functions. Define the contract; ignore the
    internals. This is the Big Recursive Idea.
17. **Choose head recursion by default.** Minimizes the parameters you
    must thread; cleaner public signatures.
18. **Pick data structures by required operations**, not by
    familiarity. If you never re-access the data, use no structure at
    all.
19. **Default everything to private.** Promote only with a specific
    reason. Treat public signatures as frozen.
20. **Validate at write, not at every read.** Factor the predicate
    into a single named helper.
21. **After fixing a bug, write down the principle that was
    violated**, not just the fix. Repeats teach.
22. **Walk every special case before claiming done.** Empty, single,
    max, NULL, not-found, exactly-at-boundary.
23. **Refactor as an explicit phase**, not as an instinct during
    feature work.
24. **Create a restore point** (branch / git stash / copy / snapshot)
    before any nontrivial modification.
25. **Learning a new language / codebase: re-derive what you already
    know in it; then list what's different; then study expert code.
    Never start by editing it.**

## How to use this skill

- Name the move. "I am going to RESTATE the problem." This is the
  whole technique - explicit selection breaks decision paralysis.
- One move at a time. Cycle through if needed.
- After three moves with no progress, run `stuck-loop`.

## Pairing

- `decompose` runs the plan-restate-divide-reduce loop in a more
  procedural sequence; use it when the task is large.
- `stuck-loop` runs the prescriptions for when you've been stuck for
  >15 minutes.
- `verify-task` calls this skill when reproducing a bug or framing an
  ambiguous feature.
- `orchestrate` calls this skill during planning and the remediation
  loop.
