---
name: creating-k-semantics
description: Build or extend an executable K-Framework semantics for a real language (JavaScript, Python, a bytecode, a DSL). Triggers — starting a K semantics for a language; adding the next language version or feature layer to an existing K definition; an autonomous loop driving oracle-checked semantics development. Also use when another skill needs the oracle-driven method for formalizing a language.
---

# Creating K Semantics for a Programming Language

You are writing an **executable** formal semantics: a K definition that runs real programs, not prose. The method that makes this tractable for a large language — and safe to run agentically or in a loop — has one root idea:

> **The oracle is the spec.** Every change is a *verifiable repair* against ground truth the system can check itself: a conformance vector flips green, the reference implementation agrees on a concrete input, the rule matches the cited spec clause. Where there is no oracle, there is nothing to verify, and a generated semantics is unfalsifiable — do not build there.

Two nested loops run this:

- **Inner loop (per feature):** read the spec clause → write the minimal K rules → run the oracle → iterate red→green.
- **Outer loop (per version):** walk language versions oldest-first; each is **done** only when its whole conformance subset is green *and a full re-run shows zero regression in every earlier layer*.

The failure mode to fear is **overfitting**: rules contorted to pass a test instead of modeling the spec. The spec document is the guard against it; the no-regression gate and the reference implementation are the net that catches it.

This skill is K-Framework-specific but language-agnostic. Bitcoin Script (a consensus stack machine) and Lox (a tree-walking imperative/OO language) are the worked examples, kept entirely in their case-study references so nothing here couples to either.

## The loop at a glance

```text
Mode    Ask mode + standing policies (the only question)    ── first
Step 0  Gate: does the language qualify? (3 oracles)        ── once
Step 1  Build the oracle harness                            ── once
Step 2  Pick the oldest unfinished version layer            ──┐
Step 3  Order its features by dependency → backlog          ──│ outer
Step 4  Per feature: read spec → write rules → run → green  ──│ loop
Step 5  Advance gate: full re-run, zero regression          ──┘
```

Pick the **operating mode** first (next section), then run the loop. Three design-decision boundaries (below) are where tests cannot settle the call. The run ends when every targeted version layer is green — or, in fully autonomous mode, when it reaches strict 100% coverage or you stop it.

## Operating mode — ask once, before Step 0, then never again

Before doing anything else, **ask the user which mode to run** — and treat this as the run's *only* question, so collect the standing policies with it in the same exchange:

- **Mode** — one of the two below.
- **Commit/push policy** — push after every gated commit, hold pushes, or feature branches? Settle it now; never ask again mid-run.
- **Scope pre-approvals** — may the loop take on risky-but-in-scope restructurings solo (staged, on a branch, gated)? What, if anything, is out of scope?

The modes:

- **Human-checkpoint** — a judge agent settles the architecture and spec-ambiguity calls as it goes (the loop never blocks on you for those), but it **pauses for your sign-off at every layer advancement**. The completed version layer is the milestone: you review its green snapshot and the judge's design calls before the next layer opens.
- **Fully autonomous** — the judge agent settles *all* design calls, advancement included, and the loop **never stops**. It runs until you manually stop it, or until it is confident it has reached **strict 100% oracle coverage** (defined under "Running it as a loop"). It pauses for nothing in between — the only exceptions are the safety stops enumerated under "What autonomy does not license."

The mode changes exactly one thing: who clears the **layer-advancement** boundary — you, or the judge. Everything else is identical in both modes: the inner loop, the per-feature anti-overfitting judge pass, the no-regression gate — and the **no-stopping discipline** below, which governs every turn of the run in both modes.

## Step 0 — Gate: qualify the language

A language is buildable this way only if you can name and **run** all three oracles. Find them before writing a single rule.

1. **Formal spec** — the algorithmic ground truth you mirror in rules (ECMA-262 for JS; the Python Language Reference for Python).
2. **Conformance suite** — machine-checkable, tagged by version/feature; this is what flips green (test262 for JS; CPython's `Lib/test/` for Python).
3. **Reference implementation** — a differential oracle for behavior the suite misses (V8/Node for JS; the CPython binary for Python).

[references/oracle-harness.md](references/oracle-harness.md) has the concrete wiring for each.

**Hard gate:** no conformance suite *and* no runnable reference implementation → STOP. You would be generating unverifiable semantics — the one situation this method cannot protect you from. (A formal spec alone is not enough; you need something executable to check against.)

**Qualify the framework too.** Before committing to an architecture, prove every make-or-break framework capability with a **tiny throwaway probe definition** — minutes each. Backends of one framework implement *different* hook subsets, and one missing primitive for your core value domain can force the backend choice for the whole project. Probe mechanics — including keeping the probe scratchpad for the whole run to later bisect opaque kompile failures — are in [references/k-patterns.md](references/k-patterns.md); when a *build* fails inexplicably, rule out the environment first via [references/pyk-harness.md](references/pyk-harness.md) ("When builds fail").

**Completion criterion:** you have all three in hand, can run the suite and the reference impl locally, and have located the spec section for your first feature. If the suite is thin for some features, that is fine — Step 1 bootstraps coverage.

## Step 1 — Build the oracle harness (once)

Wire the three oracles into a single command that, given your current (possibly near-empty) K definition, reports structured pass/fail per vector and flags any disagreement with the reference implementation. See [references/oracle-harness.md](references/oracle-harness.md) for concrete JS and Python wiring. Build it as a real Python project that drives K through the **pyk library**, **never the `kompile`/`krun`/`kprove` CLI via subprocess**; [references/pyk-harness.md](references/pyk-harness.md) is the build/run/prove API surface and project setup.

The harness must:

- **Select** a vector subset by version/feature tag (so the loop can target one feature).
- **Run** the K definition on each program and compare result/error to expected.
- **Differential-check** inputs the static suite does not cover by running the reference implementation and diffing — any disagreement is a bug in your semantics (or your harness), never a "result."
- **Bootstrap** coverage where the static suite is thin: harvest real programs (open-source corpora, the reference impl's own test files, fuzzed inputs) and *label them with the reference implementation*. This is how a few thousand hand-written vectors become hundreds of thousands of checked inputs (see the case study).

**The suite's own harness is the first program your semantics must run.** Analyze its shared include files before ordering any feature work: one unsupported construct in a file prepended to every test multiplies into thousands of spurious "unsupported" results, so cluster raw parse errors *before* ranking features by failing-test counts (in a production JavaScript run of this method, a single post-target-edition comma form in one harness helper accounted for 61% of all unsupported tests). The shim strategy and the rest of the harness signal-integrity rules are in [references/oracle-harness.md](references/oracle-harness.md).

**Completion criterion:** one command runs a tagged subset end-to-end and prints structured pass/fail plus any differential mismatch; a trivial known-good program (e.g. `1 + 1`) is green through the full pipeline.

## Step 2 — Pick the oldest unfinished version layer

The outer loop is **chronological**: formalize the oldest version first and get it fully green before the next exists. For JS that is ES5 (or ES3) before ES2015 before later editions; for Python, the oldest dialect you target before newer ones. Earlier features are the substrate later ones execute on, so this order means you never build on unmodeled ground.

When the second layer opens, the K-level question becomes how a newer edition *changes* shared behaviour — K imports flatten all rules and cannot be subtracted from, so version variance needs deliberate seams (legacy modules, policy functions, per-edition entry targets). The mechanics are in [references/k-patterns.md](references/k-patterns.md) ("Version layering"); strictly-additive layering also makes regression scoping provable — an edit confined to a newer edition's module cannot regress older targets, and can skip their expensive re-runs.

**Completion criterion:** the current layer is named, and its conformance subset is selectable in the harness by tag.

## Step 3 — Order the layer's features by dependency

Within a version, order sub-goals by **execution dependency**, not spec page order and not failing-test count:

```text
lexing / values / types  →  expressions  →  statements & control flow
  →  functions & scope  →  objects / prototypes / classes  →  builtins & stdlib
```

Each feature becomes one **sub-goal** — the backlog item the loop consumes — binding one spec section to one conformance subset.

**At the builtins/stdlib stage, choose an architecture deliberately** (it is load-bearing enough to be a design-decision call — see below). Two approaches work: write each builtin as native K rules, or **self-host the library in the source language itself** — a prelude written in the language under study, layered over a small core of K-level abstract operations. Real references lean on the latter: much of the JavaScript standard library is specified that way and KJS implements it in JavaScript; much of CPython's stdlib is Python. Self-hosting trades K-rule volume for a source prelude and keeps the K core small and spec-shaped; native rules keep everything in one formalism. Whichever you pick, roll builtins out namespace-by-namespace bound **all-or-nothing** — unimplemented members as deliberately-stuck stubs ([references/oracle-harness.md](references/oracle-harness.md), mismatch purity) — and once a second edition layer exists, register per-edition builtins through the bootstrap seam in [references/k-patterns.md](references/k-patterns.md) ("Version layering").

**Completion criterion:** an ordered, written backlog of sub-goals for this layer; each item names its spec section and its test-subset tag.

## When K's grammar can't parse the language

The first sub-goal, lexing, can hit a wall the tutorial languages never expose: **K's GLR parser is error-driven and discards whitespace and newlines as layout, so a context-sensitive lexing rule the spec mandates cannot be written as a grammar production.** JavaScript Automatic Semicolon Insertion, Python and Haskell significant indentation, and the JavaScript `/`-division-versus-regex split are all in this class — clean-grammar toy languages have none of them, a real language hits one on day one.

The fix is architectural, so treat it as a **design-decision** call (see below): model the irregular part as a *separate K definition that rewrites source text into normalised source text* (an in-K lexer plus the transformation), then let the evaluator's grammar parse the normalised output, where the irregularity is gone — explicit statement terminators, explicit block delimiters. Two kompiled definitions, glued by a thin harness that moves one string between them. Decide this before writing the evaluator grammar; it shapes the whole front end. The scanner-level mechanics (custom tokens, non-ASCII, projection-reserved braces) are in [references/k-patterns.md](references/k-patterns.md).

## Step 4 — The inner loop, per feature: read → write → verify → green

Take the next sub-goal and run the inner loop:

1. **Read the spec clause first** — and mine any **existing formalization or the reference implementation's own source** alongside it. A prior K semantics (KJS, KEVM), a mechanized spec, or the engine's own C/Python source often pins down a step the prose leaves implicit. Mirror the spec's structure (for ECMA-262, mirror the abstract operations); adapt a borrowed algorithm to *your* configuration rather than copying its structure across, since architectures differ. See [references/k-patterns.md](references/k-patterns.md) for the K idioms: the `<k>` computation cell, `strict`/`seqstrict` for evaluation order, the env+store split, control operators, and using a type system as a *separate* semantics over the same grammar.
2. **Write the minimal rules** for this feature only.
3. **Run the harness** on this sub-goal's subset. Iterate red→green.
4. **No overfitting.** Every rule cites a spec clause. A vector that goes green only via a special-case with no spec basis means the real bug is elsewhere — usually a missing foundational rule. Fix the cause; the no-regression gate will later expose the debt.

**Implement at the level the spec defines the construct.** Approximating a spec construct at a different level than the spec places it leaks through observation: a compile-time predicate emulated as a runtime check overfits; an exotic object defined by overridden internal methods but emulated with surface accessors reproduces the data flow yet changes what reflection reports — often fixing the target tests while regressing a distant chapter, which only full-suite gating catches. And when a spec-faithful fix "regresses" something, re-derive the algorithm from the clause rather than patching the patch.

**Document-and-defer is a legitimate outcome.** When one failing vector demands a structural change whose regression risk dwarfs its reward, or the root cause lives in a component slated for replacement, write the divergence down instead of fixing. A deferral is a **judge-logged design decision** that names the tests it owns: those tests move out of the layer's target — the written ledger, never silence, is what shrinks the target — and stay visibly red; they are **not** eligible for the expected-fail list (that is reserved for oracle-side divergence — see xfail hygiene in [references/oracle-harness.md](references/oracle-harness.md)). Fix at the *owning* layer only: a compensating check in an adjacent layer (the harness patching over a semantics gap) entrenches the workaround and muddies the architecture.

**Completion criterion (exhaustive):** 100% of this sub-goal's targeted vectors are green — "targeted" excludes only tests owned by a judge-logged deferral — and completion is *provisional* until the anti-overfitting judge pass returns clean.

**Anti-overfitting judge pass:** an independent agent diffs every new or changed rule against its cited spec section and flags any rule with no spec basis. "The Coming Loop" warns unattended loops breed defensive, opaque code; for a semantics that means overfit rules, and this pass plus the spec-citation rule is the defense. The pass is more than an overfitting check: the corpus only detects divergences its programs can *observe*, so an independent read of each rule against its cited clause catches corner values with no observable yet (wrong attribute flags before reflection exists, signed-zero cases). Launch it as a background agent the moment the subset goes green and start the next sub-goal (waiting is not stopping); it must return clean **before the layer's Step 5 advance gate**, and a flagged rule reopens its sub-goal as the next backlog item. Additionally target an adversarial review at **abnormal-exit paths** (throw/return *through* the feature, non-local exits, detached receivers): hand-built happy-path test batteries structurally miss them, and in practice they are where composed control-flow features actually break.

## Step 5 — Advance gate: zero regression

Before starting the next sub-goal or layer, re-run the **full** suite across every prior layer plus this one. This is the operational meaning of "passes ALL tests." **One by-construction exception:** if every edit since the last gate is provably confined to a newer edition's module (verify from the diff's file list — nothing touched in the shared base, grammar, or harness), older targets' compiled definitions are unchanged and their re-runs may be skipped (see Step 2). Any shared-base edit, or any doubt about confinement, obligates the full re-run.

**Gate on failing-test *identity*, not aggregate counts.** The invariant is "no previously-passing test lost" — so diff the identity lists of failing tests before/after, not the totals: a net-zero count can hide a fix+regression swap, and a *rising* failure count after a front-end fix is usually the frontier moving, not a regression — tests that previously couldn't parse now run deeper and hit the next unimplemented feature. Prove each fresh failure was previously unrunnable (or reproduces without your change), then read the new failure clusters as free prioritization data: they name the next feature.

**Completion criterion:** the full re-run shows zero regressions *by identity diff* and the current layer's entire conformance subset is green. Record the green snapshot (passing count + failing-test list + commit) before advancing. A previously-passing test lost in any earlier layer blocks advancement — fix it first.

## Design-decision boundaries

Three points cannot be settled by a test — they are *design* calls. Who decides depends on the operating mode, but every decision is **recorded with its justification** either way:

- **Configuration / architecture design** — before adding or restructuring cells, sorts, or phases (this covers the builtins/stdlib and front-end-transform calls above). Config shape is load-bearing and not test-verifiable; a wrong shape is expensive to undo later. **A judge agent decides and logs it, in both modes** — it never halts the loop.
- **Spec ambiguity** — when the spec is unclear, or the suite and reference implementation disagree. **A judge agent picks an interpretation and records it, in both modes.** An irreducible conflict becomes a documented `xfail` with its justification, never a halt.
- **Layer advancement** — before opening a new version layer. **This is the one mode-dependent gate.** In **human-checkpoint** mode the loop stops here for your sign-off: you review the green snapshot *and the judge's architecture decisions from the layer*, so a bad call is caught before it compounds into the next layer. In **fully autonomous** mode the judge confirms the Step 5 advance gate and the loop continues.

The per-sub-goal **anti-overfitting judge pass** (Step 4) runs in both modes regardless — it is the routine check that keeps the autonomous decisions honest.

One more input to every design call: **re-verify remembered constraints before designing around them.** Notes about tool limitations record the workaround, not the true constraint, and they decay — before building a feature around a remembered limitation, reproduce it in a minimal probe (the real fix may be a one-attribute change), and before hand-rolling a primitive, re-check the platform's actual builtin surface. When new evidence overturns a recorded gotcha, correct the note in place so a future session doesn't re-apply the obsolete workaround.

## Running it as a loop

The inner loop (Step 4) is fully agentic; the driving agent loop runs Steps 3–5 — pick next sub-goal, write rules, run oracle, advance on green — and the operating mode sets where it stops.

- **Human-checkpoint:** run unattended within a layer, then **halt at each layer boundary** for sign-off before opening the next. Per-layer stopping condition: *advance on green, halt the layer when the subset is exhausted and the full re-run is clean.*
- **Fully autonomous:** **never halt.** At each design-decision boundary the judge decides and logs (irreducible conflicts → documented `xfail`); on green, advance to the next sub-goal or layer without pausing. The run ends on only two conditions — the user **manually stops** it, or it is **confident it has reached strict 100% oracle coverage**, which means all four of these hold on one *full* re-run (not a partial one):
  1. every targeted layer's entire conformance subset is green,
  2. zero regressions across every layer,
  3. zero differential mismatches on the harvested/labeled corpus (Step 1's bootstrap set), and
  4. the anti-overfitting judge pass is clean — no rule without a spec basis.

  Until all four hold, the layer is not done and the loop keeps going. A green static suite alone is **not** 100% coverage: the differential corpus and the judge pass are what make the claim trustworthy. The only mid-run pauses are the safety stops under "What autonomy does not license"; even those end by stating what happens next on unblock.

Running the loop at scale has its own rules: [references/agentic-operations.md](references/agentic-operations.md).

## The no-stopping discipline

The mode section defines *where* the loop may halt. Everything else is the loop's to decide — and the observed failure is one-sided: an agent running this method almost never stops too little; it stops **far too often**, and every needless stop costs a human round-trip. In one real two-week run the user had to type ~30 "keep going"-class nudges, escalating from "proceed with the next steps" to standing orders the loop still failed to sustain: *"I want you not to stop until [the layer] is complete"*, *"please proceed fully autonomously"*, *"don't stop for reports like this one"*, *"don't 'stop at the clean win boundary'"*. Each nudge answered a stop this section now forbids.

**The rule: a turn ends with the next sub-goal underway, or a legitimate stop condition met — never with a question, a menu of options, or an offer to continue.**

At any moment you feel the pull to ask, run this procedure instead of asking:

1. **"Which item next?"** — the Step 3 backlog order decides. Ties go to the higher-value item; log the tie-break and take it.
2. **"Deep risky fix, or safe small wins first?"** — both, in risk order: bank the safe wins as gated commits, then take the risky item with staged validation on a branch. (This exact question was asked in production; the answer was "Yes keep going on both".)
3. **"Is this design call mine?"** — the judge decides and logs it (design-decision boundaries above), in both modes. It never blocks the loop.
4. **"Should I commit/push/merge?"** — the standing policy from mode selection already answers it. Follow it silently.
5. **"A long build/sweep is still running."** — **waiting is not stopping.** Start the next backlog item that doesn't need the result: triage the last batch, design the next one, advance a parallel feature. If a command hangs, kill it, record it, and route around it — a hung command must never block the run.
6. **"I just resumed from a compacted or interrupted session."** — resume means *resume*: reconstruct state from the snapshot log, memory, and git, then continue the backlog. Do not greet the user with a status summary and wait to be told "resume" again.

**Reports accompany work; they never replace it.** Report at commit-worthy milestones, compactly — and the report's last line states what is *now underway* ("Next: <item> — starting now"), never a question. If a genuinely new fact changes the plan, state the decision you made and why, and keep going; the user can override asynchronously.

### Rationalizations — all observed in production, all wrong

| The thought | Reality |
|---|---|
| "This is a clean stopping point / good checkpoint" | Checkpoints are commits, not stops. The backlog isn't empty; take the next item. |
| "I'll summarize and let the user pick the next area" | The backlog order already picked it. Deliver the summary *and* keep working. |
| "The next feature is big/multi-slice; better not to half-start it" | Slice 1 is a normal backlog item. Start it. |
| "Both options are defensible — the user should choose" | Do both in risk order, or the judge picks and logs why. |
| "I should hold the push until the user confirms" | Push policy was settled at mode selection. |
| "The sweep is still running; nothing to do till it finishes" | Waiting is not stopping — advance a parallel item. |
| "I've done a lot; the user will want to review before more" | Review happens at the mode's declared checkpoints, nowhere else. |

**Red flags** — if the final paragraph of a turn contains one of these, you are about to violate: "Want me to…", "Should I…", "Shall I…", "just say which", "Happy to continue with…", "Ready to continue when you are", "This is a good stopping point", or any user-directed question mark outside the mode's declared checkpoints.

### What autonomy does not license

Never-stopping raises the bar on care, because nobody is watching:

- **Never endanger the host.** Resource-heavy conformance sweeps follow the safety rules in [references/performance.md](references/performance.md) ("Keep the sweep from killing the host") — capped workers, watchdogs, offload to a dedicated machine. The same production run that under-stopped also **kernel-panicked the user's workstation twice** with unattended full sweeps; "be more careful with running and cleaning up after your commands" is the other half of the autonomy contract.
- **Never fake progress to keep moving.** Worse than stopping is continuing on a lie: "builds clean" written before the build ran, a green claimed from a stale artifact, a shortcut that skips the semantics. The verification-boundary discipline (agentic-operations.md) is what makes never-stopping safe.
- **The legitimate stops, exhaustively:** the layer-advancement checkpoint in human-checkpoint mode; an action that is destructive or irreversible beyond the working tree *and* not already settled by a standing policy or this section (pushes under the settled policy and killing your own runaway jobs are settled — think deleting data outside the repo, or force-pushing over history you did not create); *every* backlog item blocked on a resource only the user can restore; strict-100% reached in autonomous mode. Even then, the last line states what happens next on unblock — not a question.

## Performance is part of "done"

An executable semantics that cannot run real-world-sized programs is not finished — KJS and KEVM both treated speed as a first-class result. Benchmark against the reference implementation and watch for K-specific cost cliffs (quadratic term concatenation, oversized result patterns).

**Completion criterion:** the semantics runs the reference implementation's own real-world corpus to completion within a stated factor of it (record the ratio), with no input timing out — or each remaining cliff is documented with its cause named. [references/performance.md](references/performance.md) is the K optimization toolkit; [references/case-study-bitcoin-script.md](references/case-study-bitcoin-script.md) is the worked 149×→2.1× path.

## References

- [references/k-patterns.md](references/k-patterns.md) — transferable K idioms for PL semantics, with verbatim examples from the K PL tutorial (LAMBDA, IMP, IMP++, SIMPLE) mapped to JS/Python; plus the front-end lessons real languages need beyond the tutorial's clean grammars (source→source transforms, scanner/token gotchas, unordered-`Map` enumeration).
- [references/oracle-harness.md](references/oracle-harness.md) — concrete oracle wiring for JS (test262 + V8/Node + ECMA-262) and Python (Lib/test + CPython), the bootstrap-by-differential-labeling technique, the pyk substrate for invoking K, keeping the reference oracle hermetic, and the signal-integrity rules: mismatch purity and fail-closed stubs, triage by failure signature, shimming the suite's own harness, identity-diff regression gating, xfail hygiene against a newer-edition oracle, and the false-pass classes differential agreement cannot see.
- [references/pyk-harness.md](references/pyk-harness.md) — building the harness as a proper Python project: drive K through the pyk library (kdist `Target` builds, in-process `kompile`/`llvm_interpret`, KORE-AST results, Kore-RPC `APRProof`) instead of subprocessing the K CLI, plus pyproject/uv/typing hygiene — and **build-failure debugging**: run the kompile CLI directly to read the diagnostic pyk swallows, then the environment-first checklist (fd exhaustion masquerading as parse errors, poisoned build caches, pipes hiding exit codes, A/B against a known-good commit). Verified against kimp, KEVM, and bitcoin-script.
- [references/performance.md](references/performance.md) — the K optimization toolkit when real inputs are too slow: the O(n²) `+Bytes`/`+List` trap and streamed accumulators, native bulk hooks with a pure-K twin and `[simplification]` equivalence, `[concrete]` result-cell cleanup, binary-KORE construction, bounding native-backend memory over long suite runs, the no-GC-inside-one-function-evaluation memory bomb, and keeping resource-heavy sweeps from killing the host.
- [references/agentic-operations.md](references/agentic-operations.md) — operating the loop at scale: artifact pinning during sweeps, verification-boundary commits and baseline capture, when parallel agents are safe (and when they are not), and long-run job hygiene (liveness monitoring, watcher teardown, artifact freshness, remote pre-flights).
- [references/case-study-bitcoin-script.md](references/case-study-bitcoin-script.md) — the proven success story: how this exact method built a Taproot-complete Bitcoin Script semantics, era by era, with zero mismatches over 288K real inputs.
- [references/case-study-lox.md](references/case-study-lox.md) — building a Lox (Crafting Interpreters) semantics chapter by chapter against its reference test suite; a legible end-to-end run of the loop, autonomous, from the gate through inheritance.
