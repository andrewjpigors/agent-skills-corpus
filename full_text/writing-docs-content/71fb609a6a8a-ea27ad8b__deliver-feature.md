---
name: deliver-feature
description: End-to-end delivery driver for ANY unit of work in any repo — new features, enhancements to existing behavior, bug fixes, refactors/cleanup, docs updates, test additions, and chores/config changes — taken from intent (a tracking issue, a conversation, or an ad-hoc request) all the way to a green, review-ready PR. The skill first CLASSIFIES the work into a delivery profile (feature / enhancement / fix / refactor / docs / test / chore) and scales every lifecycle gate to that profile, so a one-file cleanup gets a minutes-long lane while a new screen gets the full treatment — but nothing ever skips the non-negotiables that apply to it (a user-facing changelog entry if the project keeps one, conventional commits, a green build, the feature-flag decision, codegen regen). It supports three operating modes: interactive (default — discuss scope, approve the plan in plan mode, answer the feature-flag question), fast-path (the invocation itself answers the gates), and fully autonomous (--auto / "don't ask me anything" / "push it through" — every gate self-answers by the project's documented rules, decisions are logged to the issue/PR, and it stops only at hard stops like destructive git states or scope explosions). It implements on a feature branch, ensures unit + integration + e2e coverage (delegating gap-finding to the bundled `test-gap` workflow; regression-test-first for fixes), captures runtime evidence via `shipyard:verify`, keeps docs current including any user-facing how-to and changelog the project keeps (delegating gap-finding to `doc-gap`), self-reviews via `shipyard:code-audit` fixing P0/P1, and hands off to `shipyard:ship-pr` to open the PR and babysit CI to green. It checkpoints progress to the tracking issue so an interrupted run resumes where it left off. The skill is project-agnostic: it learns the repo's stack, commands, and documented rules at runtime (see the discovery contract) rather than hardcoding them. Use this whenever the user wants work driven to a finished PR: "build this feature", "implement this issue", "fix this bug", "clean this up", "refactor X", "update the docs for Y", "take this from issue to PR", "do the whole thing", "deliver this end to end", "ship it fully autonomously", or describes any chunk of work — large or small — and wants it done to the project's standards. It is the orchestrator; it reuses the sibling Shipyard skills and bundled workflows rather than re-implementing them. Cross-model options (optional, need the `codex` CLI): `--builder=codex` / "have codex build it" delegates implementation to `shipyard:codex-build`; "grill the plan" / `--grill-plan` runs that skill's adversarial plan-review loop before code; `--dual-review` / "have claude and codex review it" runs the `dual-review` workflow after the PR is pushed. Prefer it over ad-hoc edits even for small changes — the profile system keeps the overhead proportional.
---

# Deliver Feature

Drive a unit of work — *any* unit, from a new screen to a one-file cleanup — from "here's
what we want" all the way to "PR open, CI green, every gate that applies satisfied, ready
for human merge" — in **whatever repo you're in**.

This is the **orchestrator**. It owns the interactive, human-in-the-loop spine of the
lifecycle and *delegates* the parallel, autonomous phases:

| Phase | Owner | Why |
|---|---|---|
| Discover the project | this skill (once, up front) | every later step adapts to what's found |
| Intake | this skill (interactive) | needs a decision: pick vs create vs ad-hoc |
| Classify | this skill | picks the delivery profile that scales everything else |
| Discuss & align | this skill (interactive) | shared scope before any plan |
| Plan + approval | this skill (plan mode when interactive) | plan approval is a main-loop gate |
| Plan stress-test (opt-in) | `shipyard:codex-build` **skill**, grill mode | cross-model critique before code exists |
| Feature-flag decision | this skill (**always resolved**) | asked or rule-derived per profile + mode |
| Implementation | this skill — or `shipyard:codex-build` when `--builder=codex` | one coherent, reviewable context |
| Test-gap analysis | `test-gap` **workflow** | fans out across surfaces |
| Runtime evidence | `shipyard:verify` **skill** | boots the app, exercises the change live |
| Doc-gap analysis | `doc-gap` **workflow** | fans out across doc dimensions |
| Self code review | `shipyard:code-audit` **skill** | runs the real gates + rule judgment |
| PR + CI to green | `shipyard:ship-pr` **skill** | sequential, destructive git loop |

The two gap workflows are **report-only** — they find gaps in parallel and hand back a
structured list. *This skill writes the actual tests and docs* back in the main loop, so
the new code lands in one place a human can watch and review.

> **Workflow authorization.** This skill explicitly authorizes calling the `Workflow`
> tool for the two gap-analysis phases below (the bundled `test-gap` and `doc-gap`), plus
> `dual-review` **only when the user opted in** (the invocation says `--dual-review` /
> "dual review" / "have claude and codex review it"). Those are the opt-ins — do not invoke
> any other workflow without a fresh user request.

> **CRLF guard, before the first `Workflow` call each run.** The bundled
> `workflows/*.js` scripts are committed LF-only, but a worktree checkout has occasionally
> been observed serving a stale CRLF copy, which the Workflow tool rejects outright
> ("script contains control characters…"). Cheap and idempotent: before the first
> `test-gap`/`doc-gap` (and `dual-review` when opted in) call, `Read` the script; if it
> contains `\r`, `Edit` it back with every `\r` stripped. Do this via `Edit`, not a raw
> `sed -i` on the tracked file.

> **Consume the `Workflow` result directly — don't re-parse it.** With a `schema`,
> `Workflow`'s return is already the validated object (`result.gaps`, `result.summary`) —
> there's no JSON text to re-parse. Hand-rolling an inline re-parse (e.g. from a transcript
> grep after resuming a paused session) is the source of `KeyError`/`JSONDecodeError`
> crashes. If you must persist a result across sessions, `Write` it verbatim to
> `$SCRATCH/<name>-gap-report.json` (the scratchpad dir named in your system prompt) and
> `Read` it back — never `/tmp`, which isn't reliable on Windows.

## Step 0a: Discover the project (do this first, always)

Before anything else, learn the repo per
**`${CLAUDE_PLUGIN_ROOT}/reference/discover-project.md`**. Carry the resulting "project
facts" (rule file, build/test/lint commands, base branch, PR tool, migrations, dev infra,
review bot, flag mechanism, changelog convention) through every step below, and pass them
to the bundled workflows via `args`. Everything that follows adapts to what you found;
where a project lacks a phase's prerequisite, say so and skip — don't invent it. If the
invocation asks for a Codex lane, the discovery contract also covers the `codex`
availability probe.

### Invoking the bundled workflows

The `test-gap` and `doc-gap` workflows ship inside this plugin, so they are **not**
resolvable by name. Invoke them by path:

```bash
echo "$CLAUDE_PLUGIN_ROOT"   # the plugin's install dir
```

```
Workflow({ scriptPath: "<that path>/workflows/test-gap.js",
           args: { base: BASE, context: "<profile + focus>", rulesFile: RULES_FILE, projectFacts: {…} } })
```

(If `scriptPath` is ever unavailable, the README documents the one-time fallback: copy
`workflows/*.js` into `~/.claude/workflows/` and invoke by `{ name }`.)

---

## The lifecycle (run in order)

```
0a. Discover         — learn the repo's stack, commands, and rules (above)
0b. Pre-flight       — environment health + clean tree + branch off base (scaled by profile)
1.  Intake           — pick an existing issue, create one, or accept ad-hoc work
2.  Classify         — pick the delivery profile; announce the gate plan
3.  Discuss & align  — resolve ambiguity, agree scope BEFORE planning (scaled)
4.  Plan             — plan-mode approval, inline plan, or issue-comment plan (scaled)
5.  Feature-flag gate— asked or rule-derived per profile + mode
6.  Implement        — build per the plan, honoring the project's rules
7.  Tests            — test-gap → write missing tests → all green (scaled)
8.  Runtime evidence — shipyard:verify → exercise the change live (when a runtime surface exists)
9.  Docs             — doc-gap → write docs (+ changelog if the project keeps one) → in sync (scaled)
10. Self review      — shipyard:code-audit → fix P0/P1 (gates scale to the diff)
11. Ship             — shipyard:ship-pr → PR + CI to green
12. Close-out        — link the issue, report what shipped + decisions made
```

Never skip a step silently. Every step runs in one of three intensities — **full**,
**light**, or **skip** — chosen by the profile matrix below. A *skip* is still announced
with its reason ("no runtime surface ⇒ no live verify"), so the record shows the gate was
considered, not forgotten.

---

## Delivery profiles — classify first, then scale everything

The single most expensive failure mode is treating all work as feature-shaped: a two-line
cleanup doesn't need plan mode, a flag question, or a five-agent test-gap fan-out — but it
*does* still need conventional commits, a green build, and a changelog decision. Classify
the work in Step 2 and let the profile drive intensity.

### The profiles

| Profile | What it is | Typical signal |
|---|---|---|
| `feature` | A new user-visible surface or capability | new route/screen/endpoint/job |
| `enhancement` | Modifying existing behavior a user can observe | "change how X works", feedback items |
| `fix` | Repairing a defect — behavior is wrong today | "bug", a repro, a failing scenario |
| `refactor` | Behavior-preserving restructure, cleanup, dead-code removal | "clean up", "extract", "remove unused" |
| `docs` | Documentation-only | only docs / `*.md` will change |
| `test` | Test-only additions or repairs | "add coverage for", flaky-test fix |
| `chore` | Config, CI, tooling, dependencies, scripts, infra | infra/CI dirs, lockfiles, scripts |

### Classification rules

- **Classify by effect, not phrasing.** A "small tweak" that changes what a user sees is an
  `enhancement`, not a `chore`. A "refactor" that alters an API response shape is an
  `enhancement` (or `fix`). When the observable behavior of the deployed system changes, the
  work is at least `enhancement`/`fix` grade.
- **Mixed work takes the highest-rigor applicable profile.** A fix that requires a new
  endpoint runs as `feature`-grade where they differ.
- **Announce the classification** with a one-line rationale and the resulting gate plan
  (which steps run full / light / skip). In interactive mode the user confirms it as part of
  Step 3's alignment check — one confirm covers scope *and* profile; in autonomous mode it's
  recorded in the decision log.
- **Re-classify mid-flight when scope grows.** If implementation reveals the work is bigger
  than classified (a "fix" that needs a schema change, a "chore" that touches a user
  surface), stop, escalate the profile, and re-run the newly-applicable gates (the flag
  question, plan revision). Say so out loud. Never quietly finish feature-grade work on a
  chore lane.

### The gate matrix

| Step | feature | enhancement | fix | refactor | docs | test | chore |
|---|---|---|---|---|---|---|---|
| 0 Pre-flight | full (repair) | full | full | full | light¹ | full | full |
| 1 Issue anchor | required | required | required | optional² | optional² | optional² | optional² |
| 3 Discuss & align | full | full | light (repro + intent) | light | light | light | light |
| 4 Plan | plan mode³ | plan mode³ | inline⁴ | inline⁴ | skip | skip | skip |
| 5 Flag gate | ask/derive | ask/derive (if UI) | auto: no flag | auto: no flag | n/a | n/a | auto: no flag |
| 7 Tests | test-gap wf | test-gap wf | regression-first + targeted⁵ | suites green⁶ | n/a | is the work | targeted |
| 8 Runtime evidence | verify | verify | verify repro is gone | smoke touched surface | n/a | n/a | if runtime surface |
| 9 Docs | doc-gap wf | doc-gap wf | inline check⁷ | stale-doc check⁸ | is the work⁹ | skip | config-docs check¹⁰ |
| 10 Self review | full audit | full audit | full audit | full audit | hygiene only¹¹ | gates only | gates only |
| 11 Ship | ship-pr | ship-pr | ship-pr | ship-pr | ship-pr | ship-pr | ship-pr |

1. **docs light pre-flight** — no infra/build needed to edit Markdown: skip the heavy
   environment repair; just verify branch/tree and PR-tool auth.
2. **Issue optional** — required only if the work spans sessions, needs discussion, or the
   user tracks it; otherwise the PR body is the durable record. Say which anchor you chose.
3. **Plan mode** applies in interactive mode; in autonomous mode the plan is posted as an
   issue comment instead (see Operating modes).
4. **Inline plan** — a short plan stated in chat (files to touch, approach, test intent), no
   plan-mode round-trip. **Escalate to plan mode** if the work touches migrations,
   auth/security-sensitive surfaces, or >~10 files.
5. **Regression-first** — see Step 7: the fix profile demands a test that fails without the fix.
6. **Refactor tests** — behavior-preserving means existing suites are the proof: unit lane +
   targeted integration for every touched surface must pass; new tests only where the
   refactor exposed a coverage hole.
7. **Fix docs inline** — decide the changelog `fix` entry (would a user feel it?) and check
   the touched surface's user-facing doc for accuracy; no workflow fan-out for a small diff.
8. **Stale-doc check** — grep the docs tree for symbols/routes/names the refactor renamed or
   removed; usually nothing, but a rename that orphans a doc reference is a real gap.
9. **Docs profile** — the docs are the work; self-check format (changelog format, index
   links, no superseded pages edited) instead of running the workflow.
10. **Config-docs check** — new config keys propagate to the project's config-example files
    (`.env.example`, a settings template, container ARGs); changelog almost never (internal churn).
11. **Hygiene only** — no build/test gates for a docs-only diff; check links, index entries,
    changelog format, no checked-in plan artifacts.

The matrix is the default, not a cage — you may always run a *heavier* intensity than
listed (never lighter), and the user can override in either direction.

---

## Operating modes

Three modes. Detect from the invocation; when unstated, default to **interactive**.

- **Interactive** (default) — Steps 3–5 engage the user as written below.
- **Fast-path** — the invocation already answers one or more gates (an explicit `--no-flag`,
  or plain language like "no flag", "skip the questions on scope, I trust the issue"). Treat
  each stated answer as given instead of re-asking; everything unstated still asks. Step 3
  never disappears entirely — it shrinks to a single-line play-back-and-confirm, because a
  misread scope is the most expensive failure this skill has.
- **Autonomous** (`--auto`, or plain language like "fully autonomous", "don't ask me
  anything", "push it all the way through", or running headless/scheduled with nobody to
  answer) — no blocking questions. Every interactive gate self-answers by the rules below,
  and **every self-answered decision is logged** (see the decision log).

### The autonomous contract

What each gate does when nobody can answer:

| Gate | Autonomous behavior |
|---|---|
| Issue draft approval | Create the issue and report it (reversible — it can be closed). Title/body held to the same bar as interactive. |
| Discuss & align | Post a **scope read** as an issue comment: the issue restated, assumptions, in/out-of-scope list. Proceed on that reading. |
| Plan approval | Skip `EnterPlanMode` (it blocks). Post the plan as an issue comment (durable, reviewable later), then proceed. |
| Feature-flag gate | Derive from the project's flag mechanism: **flag** if the work is a user-visible UI surface that is partial / lands over multiple PRs / benefits from a dark launch; **no flag** for backend-only, fixes, refactors, chores, and complete small UI changes. If the project has no flag mechanism, don't invent one — record "no flag (no mechanism)". Record the derivation. |
| Dirty tree at start | Stash unrelated changes with a marker and report; never silently fold them in. |
| Genuine scope fork | Pick the recommendation you'd have offered, record it prominently, continue — unless both paths are expensive AND hard to reverse, which is a hard stop. |

**Hard stops — even in autonomous mode, stop and surface:**

- The already-shipped check (Step 1) finds the work may already exist.
- A diverged remote branch or a migration-snapshot conflict (`shipyard:ship-pr` stops on
  these too — don't bypass it).
- Anything destructive or production-affecting beyond the branch's own history (dropping a
  non-throwaway database, deleting data, touching a protected/legacy schema).
- A secret discovered in tracked files.
- Scope explosion: the real work is roughly ≥2× the planned surface or needs a new
  subsystem / architectural-decision-grade call the issue never mentioned.
- The issue explicitly demands something a documented project rule forbids.

**The decision log.** In autonomous (and fast-path) runs, accumulate every self-answered
decision — classification, flag derivation, scope-fork picks, builder choice, anything the
user would otherwise have been asked — and (a) include the list in the PR body under
`## Decisions made autonomously`, and (b) repeat it in the Step 12 close-out. An autonomous
run whose judgment calls are invisible is not autonomous, it's unaccountable.

---

## Checkpointing & resume

Long runs get interrupted — context compaction, session death, a pause. Make the lifecycle
resumable:

- **For issue-anchored work** (feature / enhancement / fix — and any run in autonomous
  mode): maintain a single **Delivery status** comment on the issue. Create it once after
  Step 2, then update that same comment at phase boundaries — after classify, after
  implement, after tests, after ship. On GitHub: capture the comment id from
  `gh api repos/$OWNER/$REPO/issues/$N/comments -f body=…`, then PATCH
  `gh api repos/$OWNER/$REPO/issues/comments/$COMMENT_ID -X PATCH -f body=…`. On GitLab, use
  the note equivalent; with **no issue tracker**, keep the same checklist in the PR body
  once the PR exists, or skip checkpointing for a short run. Shape:

  ```
  ## Delivery status (auto-updated by shipyard:deliver-feature)
  Profile: fix · Mode: autonomous · Branch: fix/<slug>
  - [x] 2 Classified   - [x] 4 Planned   - [x] 6 Implemented (abc1234)
  - [ ] 7 Tests   - [ ] 8 Runtime   - [ ] 9 Docs   - [ ] 10 Review   - [ ] 11 Shipped
  Decisions: no flag (backend-only)
  ```

- **On resume** (a fresh session picking up the same issue/branch): read the Delivery status
  comment first and continue from the first unchecked phase — don't re-run completed phases,
  and don't re-derive decisions already logged (re-verify only what's cheap: branch exists,
  build green).
- **On pause** (user stops mid-run): hand off to the `shipyard:handoff` skill — it commits a
  marked WIP, records state durably, and points the next session back here.
- For small issue-less work, checkpointing is optional — those runs fit a session; if one
  somehow doesn't, create the issue then (it's now multi-session work, which is what issues
  are for).

---

## Step 0b: Pre-flight

Read these before doing anything:

```bash
git rev-parse --abbrev-ref HEAD        # current branch
git status --porcelain                 # working tree state
```

- **Environment health.** Delegate the environment check to **`shipyard:preflight`** — don't
  re-derive it here. For any profile that will build or run code, run it in repair mode so
  the workspace is actually ready (runtime files, dependencies installed, dev infra up,
  migrations applied — whatever the project has). If it reports a blocking failure it can't
  repair, stop and surface it; building on a broken environment just produces false failures
  downstream. If state is corrupted beyond repair, fall back to `shipyard:local-reset`.
  **`docs`-profile runs skip this** — editing Markdown needs no infra; say so and move on.
- **Branch.** If on the base branch (`main`/`master`/detected default), do NOT implement on
  it. Create a work branch after the plan is settled, named from the profile + slug
  (`feat/<slug>` / `fix/<slug>` / `refactor/<slug>` / `docs/<slug>` / `chore/<slug>`). If
  already on a suitable branch, use it.
- **Clean tree.** If there are uncommitted changes unrelated to this work, surface them and
  ask whether to stash, commit, or proceed (autonomous mode: stash with a marker and report)
  — don't silently fold them in.

---

## Step 1: Intake

Every delivery is anchored to a durable record. For `feature` / `enhancement` / `fix` that
is a tracking issue — durable cross-session tracking belongs in the issue tracker, not a
checked-in plan file. For small `refactor` / `docs` / `test` / `chore` work an issue is
optional — the PR body can be the record; create one anyway if the work will span sessions
or the user tracks it. (If the project has no issue tracker / no `gh`·`glab`, anchor to a
clear written scope in the conversation and the PR body, and say so.)

**If the user named an issue** (`#N`, a URL, or "the X issue"): fetch and read it fully.

```bash
gh issue view <N> --json number,title,body,labels,state,url   # or: glab issue view <N>
```

If it's closed, surface that and confirm before continuing (a closed issue usually means
shipped or won't-do — a hard stop in every mode).

**If there's no issue yet and one is warranted**, draft it from the conversation. Interactive
mode: show the user for approval before opening. Autonomous mode: create it directly and
report (see the autonomous contract).

- Title: conventional, scoped (`feat(area): …`, `fix(area): …`).
- Body: the problem, desired outcome, acceptance criteria, constraints. Write it so a cold
  reader could pick it up.

```bash
gh issue create --title "<title>" --body "<problem / outcome / acceptance criteria>"
```

Capture `ISSUE_NUMBER` / `ISSUE_URL` — the PR will reference them. **If the work is ad-hoc
and small**, restate it in one or two sentences as the working spec and carry that into the
PR body later.

### Before you plan: confirm the work hasn't already shipped

A common, expensive failure is building work another PR already merged (an issue can sit
open while the work landed under a different number), or duplicating a sibling branch. A
closed-state check is not enough. Before spending a plan on it:

```bash
git fetch origin --prune
# has a merged PR already referenced this issue?
gh pr list --state merged --search "$ISSUE_NUMBER" \
  --json number,title,mergedAt,url --jq '.[] | "\(.number) \(.title) \(.mergedAt)"'
# is there already a branch (local or remote) doing this work?
git branch -a --list "*$ISSUE_NUMBER*" "*<issue-slug>*"
# does the base already contain the surface? (search the file/route/symbol you'd add)
git --no-pager log origin/<BASE> --oneline -S '<distinctive symbol or route>' | head
```

For a `fix`, add one more leg: **confirm the bug still reproduces on current `origin/<BASE>`**
— bugs get fixed in passing by other PRs; don't "fix" one that's already gone. If any of
these show the work already exists: **stop and surface it** (a hard stop in every mode).

---

## Step 2: Classify — pick the delivery profile

Using the issue/spec and a skim of the code you expect to touch, pick one profile from the
table above and announce it:

```
Profile: fix — the register mis-sorts settled rows (behavior is wrong today).
Gate plan: inline plan (no plan mode) · no flag · regression test first ·
live-verify the repro is gone · changelog "fix" entry likely · full self-review · ship.
```

Rules of judgment live in the **Delivery profiles** section: classify by effect, mixed work
takes the highest-rigor profile, and re-classify out loud if scope grows mid-flight. In
interactive mode the user confirms the profile as part of Step 3's alignment check; in
autonomous mode it goes in the decision log. Then, for issue-anchored work, create the
**Delivery status** checkpoint comment (see Checkpointing & resume).

---

## Step 3: Discuss & align (before any planning)

The issue is the starting point, not the finished spec. Before drafting a plan, **verify
shared understanding** so the plan is built on a shared picture instead of a guess. This
step runs every time in every mode — what changes is its weight:

- `feature` / `enhancement` (interactive): a real conversation.
- Everything else (and fast-path): a short play-back plus one confirm.
- Autonomous: a **scope read posted to the issue** (or stated in the run log for issue-less
  work) — the restatement, assumptions, in/out list — then proceed.

The substance, scaled to fit:

- **Play the issue back in your own words** — restate problem, outcome, acceptance criteria,
  so a misread is caught before it costs a plan. For a `fix`: state the repro and the
  suspected cause.
- **Ground the read in the code.** Skim the slice you'd touch and the relevant docs, then
  name the files/surfaces you think are in scope — and the ones you think are *out*.
- **Surface the real decisions.** Call out ambiguities, unstated assumptions, edge cases, and
  anything that fights a documented rule or the existing design. Where there's a genuine
  fork, put the options and your recommendation to the user (`AskUserQuestion` suits the
  discrete ones); autonomous mode picks the recommendation and logs it (or hard-stops).
- **Agree on scope.** Confirm what's in, what's explicitly deferred, and what "done" means
  for this pass. If the issue is really several pieces, agree whether to split it.

Close with an explicit alignment check in interactive/fast-path modes — "here's what I'll
plan against, good?" — and don't slide into planning while a scope question is open. If the
discussion materially changes the issue, **update the issue body** so it stays the source of
truth.

---

## Step 4: Plan

Scale the plan to the profile:

- **`feature` / `enhancement`, interactive:** enter **plan mode** (`EnterPlanMode`), draft
  the plan, present with `ExitPlanMode`, and get explicit approval before writing code.
  Revise and re-present if approval comes back with changes.
- **`feature` / `enhancement`, autonomous:** same plan, but post it as an **issue comment**
  instead of blocking in plan mode, then proceed.
- **`fix` / `refactor`:** an **inline plan** — a short stated plan in chat (root cause /
  approach, files to touch, test intent). Escalate to plan mode if the work touches
  migrations, auth/security-sensitive surfaces, or >~10 files.
- **`docs` / `test` / `chore`:** no formal plan; one sentence of intent.

Ground every plan in the actual codebase, not assumptions — read the touched slice, the
relevant docs, and the project rules that apply to the surfaces you'll change. A full plan
covers:

- The concrete files/surfaces to add or change (backend, any migration with the right
  tool/context, frontend + any generated client, etc. — whatever the stack has).
- The test surface: which behaviors get unit / integration / e2e coverage (for a `fix`: the
  regression test comes first).
- The docs surface: topic docs, any user-facing how-to, and whether the change is
  user-visible (⇒ a changelog entry, if the project keeps one).
- Whether a feature flag is in scope (decided in Step 5, but write the plan so the flag can
  be threaded in cleanly).

### Step 4½ (opt-in): adversarial plan stress-test via Codex

After the plan is drafted (and, in interactive mode, approved), the user may opt into a
cross-model critique before any code is written — invoke the **`shipyard:codex-build` skill
in plan-grill mode** (it owns all Codex CLI mechanics and probes for the CLI first). Codex
(read-only) attacks the plan in a bounded VERDICT loop; this skill remains the final arbiter
on every critique, and the round-by-round argument is logged to the tracking issue — never
checked in.

Run it when the invocation asks ("grill the plan", "codex review the plan", `--grill-plan`),
or **offer it** when a `feature`/`enhancement` plan touches the high-stakes surfaces that
already escalate inline plans to plan mode (migrations, auth/security, money/pricing math,
concurrency). It requires the `codex` CLI — if absent, say so and skip. Autonomous mode
never blocks on it: it runs only if the invocation asked, and a deadlocked loop proceeds on
this skill's judgment with the disagreement logged prominently.

---

## Step 5: Feature-flag gate (asked or derived, never forgotten)

Flags are release switches for **user-visible UI work**. The gate runs on every profile, but
most profiles answer themselves:

- **`fix` / `refactor` / `chore` / backend-only work:** don't flag these — record "no flag
  (backend-only / bug fix / internal)" and move on. No question needed in any mode.
- **`feature` / `enhancement` with a user-visible UI surface, interactive or fast-path:**
  **ask the user** (unless the invocation already answered — "no flag" / `--no-flag` /
  "flag it"). Use `AskUserQuestion`, framing the trade-off:

  - **Flag it** when the work is unreleased / in-progress, or you want to merge incrementally
    and flip it on later without a redeploy. Wire it through the project's **detected flag
    mechanism**. If the project has **no** flag mechanism, say so and discuss the alternative
    (a draft PR, a separate branch, or shipping it released) — don't fabricate a flag system.
  - **Don't flag it** for backend-only work, bug fixes, or small self-contained changes safe
    to release immediately. A flag with no purpose is just debt.

- **`feature` / `enhancement` with UI, autonomous:** derive it — **flag** when the surface is
  partial, lands across multiple PRs, or benefits from a dark launch; **no flag** when the
  change is complete and safe to release now. Log the derivation.

Record the decision; if flagged, fold the flag plumbing into Step 6. If this delivery
**completes** a feature that already sits behind a flag, note the flag-removal follow-up in
the close-out (flags are short-lived).

---

## Step 6: Implement

**Builder lane.** By default this skill implements. When the invocation says `--builder=codex`
/ "have codex build it" (or the user picks Codex at the plan gate) **and the `codex` CLI is
available**, delegate the implementation to the **`shipyard:codex-build` skill** instead:
freeze the approved plan into a scratchpad spec, Codex implements, and that skill's verify
loop reads the full diff, runs the discovered gates, and iterates fixes (bounded), then it
takes over. Control returns here afterwards — **every downstream step (7–12) runs
unchanged**, so Codex-built code faces exactly the gates Claude-built code faces, and this
skill still writes the commits. The builder choice goes in the decision log and the PR body.
If `codex` is absent, say so and implement directly.

Build per the plan. Create the work branch now if you were on the base branch. **Honor the
project's documented rules** (the ones you captured in discovery) for every surface you touch
— re-read the relevant ones before editing rather than working from memory. Match the
surrounding code's style, naming, and idiom. Commit in logical, conventional-commit chunks as
you go — the commit type should match the profile (`feat:` / `fix:` / `refactor:` / `docs:` /
`test:` / `chore:`).

If the stack has a generated client / codegen step that a backend change invalidates
(detected in discovery), regenerate it and commit the regenerated artifacts alongside the
change.

---

## Step 7: Tests — cover the work at the right layers

First make sure the changed code's own tests pass, then find what's missing — scaled by
profile:

- **`fix` — regression test first.** Before (or with) the fix, write the test that
  reproduces the defect and **demonstrate it fails without the fix** (write it test-first, or
  stash the fix once to watch it go red). A fix without a red-then-green regression test
  isn't done. Then run the targeted lanes; run the workflow below too if the diff grew beyond
  the defect's immediate surface.
- **`refactor` — the suites are the proof.** Behavior-preserving means the existing unit lane
  + targeted integration for every touched surface must pass unchanged. Add tests only where
  the refactor exposed a genuine hole.
- **`docs`** — nothing to test; say so. **`test`** — the tests are the work; run the lanes.
  **`chore`** — targeted: whatever proves the config/tooling change works (a build, the
  affected script, a boot).
- **`feature` / `enhancement` — delegate gap-finding to the bundled workflow** (by
  `scriptPath`, with the project facts and the profile+focus `context`):

```
Workflow({ scriptPath: "<plugin-root>/workflows/test-gap.js",
           args: { base: BASE, context: "<profile> + <one-line focus>", projectFacts: {…} } })
```

It fans out across the changed surfaces, adversarially verifies each gap (so it won't cry
"missing test" for something already covered), and returns
`{ summary, gaps: [{ surface, layer, file, severity, what, suggestedTest, suggestedTestPath }] }`.

Then, **in this main loop**, write the missing tests yourself using the project's detected
frameworks and locations (unit / integration / e2e). Run the suites to green before moving
on, using the detected `TEST_CMD`(s). If a layer needs infra that isn't up (a real DB for
integration), bring it up via `shipyard:preflight` rather than reporting the suite as failing
because infra was down. A whole-suite mass-fail from resource exhaustion is not
regression — re-run the failing class in isolation before believing it. Decide with the user
(or by the profile, in autonomous mode) how exhaustive the slow e2e layer needs to be; at
minimum cover the primary new user flow.

---

## Step 8: Runtime evidence — prove it works live

Tests green ≠ the change works. Where a runtime surface changed, **invoke `shipyard:verify`**
to boot the app and exercise the actual change, then capture the evidence. By profile:

- **`fix`:** re-run the original repro live and show it's gone — the single most convincing
  artifact a fix PR can carry.
- **`refactor`:** smoke the touched surface (the endpoint still answers, the job still runs).
- **`feature` / `enhancement`:** full verify.
- **`docs` / `test` / pure-UI-with-e2e:** nothing to live-verify beyond what e2e proved —
  say so and move on.

`verify` complements the e2e suite: e2e covers user-facing UI flows, so this matters most for
what e2e doesn't reach — a new endpoint with no UI yet, a job/cron, a background service, a
migration side effect. Treat the result as a gate:

- **PASS** — record the runtime-evidence block (observed status, payload, effect) for the PR
  description; move on.
- **FAIL** — a runtime failure is the top-priority finding for this change, above any
  convention nit. Fix it and re-verify before docs/review.

---

## Step 9: Docs — update/create, including user-facing how-to

Scaled by profile:

- **`feature` / `enhancement` — delegate gap-finding to the bundled workflow:**

```
Workflow({ scriptPath: "<plugin-root>/workflows/doc-gap.js",
           args: { base: BASE, context: "<profile> + <one-line focus>", projectFacts: {…} } })
```

It checks, in parallel: a user-facing changelog (only if the project keeps one),
rule-file ⇄ sibling-rule-file sync (e.g. `CLAUDE.md` ⇄ `AGENTS.md`), topic docs, user-facing
how-to, and API/interface doc-comments. It returns
`{ summary, userVisible, gaps: [{ kind, path, severity, what, suggestedAction }] }`.

- **`fix` — inline check, no fan-out:** decide the changelog `fix` entry (would a user *feel*
  this fix? then yes) and read the touched surface's user-facing doc for accuracy.
- **`refactor` / `chore` — stale-doc check:** grep the docs tree for anything the change
  renamed/removed/reconfigured; propagate new config keys to the project's config-example
  files. Changelog almost never (internal churn) — say so.
- **`docs` — the work itself:** self-check format instead (changelog format + index link;
  don't edit superseded pages).
- **`test` — skip**, unless the tests document a surface contract worth a topic-doc line.

Then **write the docs yourself** in the main loop:

- **Changelog.** If the project keeps one and the change is user-visible (the workflow's
  `userVisible`, or your own judgment), add an entry in the project's format and voice. If
  the project has no changelog, or nothing is user-visible, add nothing and say so.
- **User-facing how-to.** New screen/flow ⇒ how-to content that tells a user how to use it
  (distinct from a changelog blurb and from dev docs), if the project keeps a user-doc surface.
- **Topic docs / ADRs.** Update the page that now contradicts the code; create one for a
  substantial new subsystem; add an ADR for an architectural decision if the project uses ADRs.
- **Rule-file sync.** If you changed a documented rule, update every rule file that mirrors it
  (e.g. both `CLAUDE.md` and `AGENTS.md`).

---

## Step 10: Self code review

Run the project's own audit before involving CI or any external reviewer.

- **Any profile that changed code:** **invoke `shipyard:code-audit`** — it runs the real
  gates (the detected build/test/lint/typecheck, plus a secrets sweep), **scaling the gates
  to what the diff actually touched**, and delegates the rule judgment to the bundled `audit`
  workflow, emitting a graded P0–P3 report.
- **`docs` profile:** skip the code audit; do the hygiene pass instead — no checked-in plan
  artifacts, links resolve, index files updated, changelog format valid.

Then act on it in the main loop:

- **P0** (build/test/security breakers) and **P1** (correctness / rule violations) — fix
  before shipping.
- **P2 / P3** — fix if cheap; otherwise note them in the PR description as known follow-ups.

Re-run the relevant gate after fixing so you know it's actually closed.

---

## Step 11: Ship — PR + CI to green

Hand off to **`shipyard:ship-pr`**. It rebases on the base branch, opens or updates the PR,
pushes with `--force-with-lease`, watches the **required** CI checks to a terminal state, and
(if the project has a review bot) triages its threads — accepting real fixes, rejecting
suggestions that fight the project's rules — until the required checks are green and every
thread is resolved.

Make sure the PR body:

- links the issue so it auto-closes on merge (`Closes #<ISSUE_NUMBER>` on GitHub) — or, for
  issue-less work, carries the one-paragraph working spec from Step 1 as the durable record;
- includes the runtime-evidence block from Step 8 (when one exists);
- includes `## Decisions made autonomously` when the run self-answered any gate.

`shipyard:ship-pr` leaves the PR review-ready; it never merges (that's a human decision).

**Dual-model review leg (opt-in).** If the user opted in (`--dual-review` / "have claude and
codex review it") **and the `codex` CLI is available**, run the **`dual-review` workflow**
right after the PR is pushed — Claude and Codex review the diff independently, debate each
other's findings, and (when posting is enabled and a PR tool exists) post the survivors and
the refutations as PR comments. Fix its `confirmed` findings in the main loop and push before
any CI review bot's pass so it reviews the hardened diff; `disputed` findings stay for the
human to arbitrate. If `codex` is absent, say so and skip.

```
Workflow({ scriptPath: "<plugin-root>/workflows/dual-review.js",
           args: { pr: <PR_NUMBER>, base: BASE, post: true, projectFacts: {…} } })
```

---

## Step 12: Close-out

Report a short summary:

```
<Profile> · <mode>. Issue #<N> → PR #<M> (<url>). Required CI green at <sha>
(or local gates green). Tests: <X> added (unit/integration/e2e; regression test
red→green for fixes). Runtime: <verified live / e2e-covered / n/a>.
Docs: <Y> (+changelog: yes/no/na). Feature flag: <name / "none (…)">.
Self-review: <A> P0/P1 fixed. Decisions made autonomously: <list / "none">.
Ready for human review and merge.
```

If anything is left open (an e2e flow deferred, a P2 noted as follow-up, a CI stalemate
`shipyard:ship-pr` bounced off, a flag now eligible for removal), list it plainly. Update the
Delivery status comment to its final state.

---

## Things this skill must not do

- **Never skip discovery** (Step 0a) — every later step depends on knowing the project.
- **Never jump from intake straight into code** — Step 2 (classify) and Step 3 (align, at
  profile weight) run first, every time, in every mode.
- **Never skip a gate silently** — a skipped step is announced with the profile rule that
  justifies it. The matrix scales gates; it never deletes the record of considering them.
- **Never resolve the feature-flag gate by forgetting it** — it is asked, answered by the
  invocation, or derived. Absent all three, ask.
- **Never implement on the base branch** — branch first.
- **Never open an issue or PR without user sign-off in interactive mode.** In autonomous
  mode, create + report with the decision logged (both are reversible) — but never *merge*
  anything, in any mode.
- **Never check in implementation plans or review artifacts** — durable tracking goes in the
  issue; audit reports stay where `shipyard:code-audit` puts them.
- **Never invoke workflows other than the bundled `test-gap` / `doc-gap`** without a fresh
  user request — those two are the only pre-authorized ones (`dual-review` requires the
  user's explicit opt-in per run, and the Codex lanes require the invocation to ask for them
  *and* the `codex` CLI to be present).
- **Never let the gap workflows write code** — they are report-only; this skill writes the
  tests and docs so it all lands reviewably in one place.
- **Never blow through a hard stop in autonomous mode** — the autonomy contract's hard-stop
  list always surfaces to the user, no matter what the invocation said.
- **Never merge the PR** — `shipyard:ship-pr` stops at review-ready by design.
- **Never invent a command, rule, flag mechanism, or changelog the project doesn't have** —
  detect, adapt, and skip what's absent.

## When this skill is the wrong tool

- **A pure question / investigation with no change to land.** Answer it; there's nothing to
  deliver. (But note: "just a small change" is NOT the wrong tool — that's the
  `chore`/`fix`/`refactor` lane, which keeps the standards without the ceremony.)
- **Pure review / audit with no implementation.** Use `shipyard:code-audit`.
- **A branch that's already code-complete and just needs shipping.** Skip to `shipyard:ship-pr`.
- **Stopping partway.** That's `shipyard:handoff` — it records the resumable state this
  skill's checkpoint comment expects to find.
- **Local environment is broken.** Reset with `shipyard:local-reset` first, then come back.
- **Cross-team work** where issue scope, the flag call, or review-bot accepts aren't solely
  the user's to make — defer those gates to humans, and don't run autonomous mode at all.
