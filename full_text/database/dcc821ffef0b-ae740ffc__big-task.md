---
name: big-task
description: Engineering workflow router — picks direct / GSD-lite / full GSD based on RISK, not file count. AUTO-INVOKED for tasks touching 3+ files or creating new functionality, but defaults to LIGHT process unless the work has real architectural risk (concurrency, atomicity, protocol, schema). Hides /gsd-* internals behind one entry point. Skip for bug fixes, typos, single-function changes, and questions. RUNS AUTONOMOUSLY by default — only pauses on Critical Decision Triggers (see Phase -1).
---

# /big-task

One skill to route engineering work. Hides `/gsd-*`, `/audit-fix-loop`, `/pr-fix-loop`, `/codebase-sweep`, `/think-ultra`, etc. under a single memorable name.

**Auto-trigger:** User describes a task touching 3+ files or creating new functionality. See `rules/workflow.md` → Big Task Auto-Trigger.

**Override:** User says "skip workflow", "just do it directly", "quick and dirty" → drop to direct execution.

**Default bias: LIGHTER process.** GSD's multi-agent ceremony (plan-checker, CONTEXT/PLAN/SUMMARY docs, revision loops) only pays off when it catches real bugs that direct implementation would ship. For locked-design UI work, well-understood patterns, and single-responsibility additions, full GSD is pure overhead. Use risk, not file count, as the primary decision axis.

**Tier 4 engine routing — match the engine to the work shape, don't pick a single default:**

| Work shape | Engine | Why |
|---|---|---|
| Multi-phase implementation, 10+ tasks, clear dependency graph, expected runtime hours | `gsd-autonomous` (wave-based GSD) | Orchestrator stays ~15% budget, subagents self-load plan from disk, waves run parallel where deps allow. Built for long autonomous runs. |
| Pattern N+1 at scale (20-screen locked-design migration, API rename across 50 files) | `gsd-autonomous` | Mechanical parallel work across disjoint files is GSD's home turf. |
| Exploratory feature, novel pattern, architecture decisions required, spec unclear | superpowers (`brainstorming` → `writing-plans` → `subagent-driven-development` → `requesting-code-review` → `verification-before-completion`) | Strong on judgment and two-stage review gates. Serial per-task but catches spec drift before ship. |
| User says "brainstorm this" / "not sure where to start" | superpowers | Its strength. |

If unclear, **silently pick `superpowers`** (judgment-strong, two-stage review gates — safer default for ambiguous engine choice). Log the choice in the PR's `## Autonomous decisions` section. Do NOT ask the user — see Phase -1.

The `/gsd-*` **planning** overhead (CONTEXT / PATTERNS / RESEARCH / REVIEW / VALIDATION / VERIFICATION meta-artifacts per phase) is real — don't pay it for small Tier 4 work. But the **execute-phase engine itself is lean** (~15% orchestrator), so don't penalize GSD for the planning-phase overhead when long autonomous runs are the actual need.

---

## Phase -1 — Autonomous-by-default mode (DEFAULT ON — overrides every "ask once" elsewhere in this skill)

Once `/big-task` is invoked, the entire flow runs autonomously through to PR-merged. **Do NOT pause for confirmation between phases, between fix loops, between commits, between detection routings, or between audit rounds** unless one of the **Critical Decision Triggers** below is hit.

The user already opted into autonomous execution by invoking this skill — every additional checkpoint is friction they explicitly do not want. If the skill's wording elsewhere says "ask once" / "surface to user" / "wait for confirmation", **this section overrides it** unless the situation matches a Critical Decision Trigger.

### Critical Decision Triggers (the ONLY 4 reasons to pause)

Pause and ask the user ONLY if the next action falls into one of these classes:

1. **Irreversible architectural choice** — picking a database engine, ORM, primary framework, monorepo tool, deployment target, auth provider, or anything else that future code will copy and that costs >1 day to undo.
2. **Money / secrets / PII boundary** — code that moves money (charges, refunds, credits), introduces or rotates secrets, exfiltrates PII, or alters access boundaries (auth scopes, RBAC, row-level security, payment paths).
3. **Requirements ambiguity that would invalidate already-shipped work** — the user's prompt has multiple readings AND picking the wrong reading would mean reverting a meaningful chunk of already-committed code. Surface ONLY when re-reading the prompt twice still doesn't disambiguate AND there's no safer "do both / do neither" middle path.
4. **User-facing breaking change** — public API contract change, data migration that requires user action, removal of a documented feature, force-push to a shared branch.

If the next action is NOT in one of those 4 classes, **proceed without asking.** Pick the more conservative path silently and log the choice in a `## Autonomous decisions` section of the final PR description so the user can audit after-the-fact.

### Auto-resolutions (replace every "ask once" prompt with these silent defaults)

| Previously asked | Now silently picks |
|---|---|
| Tier 4 engine routing unclear (GSD vs superpowers) | **superpowers** (judgment-strong, two-stage review) |
| `light-project` task looks tier-4 (escalation exception) | **escalate to tier 4 silently**, note in PR `## Autonomous decisions` |
| Auto-detected profile looks wrong | **trust the auto-detect**; only re-route if 2+ phases produce FLAG verdicts pointing at the wrong profile |
| Tier rubric ambiguous | **pick the lighter tier** (per existing "bias toward lighter tier" rule) |
| Phase 2g visual verification: FLAG items | **open a TodoWrite follow-up**, continue to next phase. Surface ALL flagged items as a batch at end-of-milestone — never one-at-a-time mid-flight |
| Phase 2g visual verification: BLOCK items | **open a fix task and execute it inline** before declaring phase verified. NO confirmation needed — BLOCK = ship-blocking by definition, fix it |
| audit-fix-loop convergence | **run to convergence — fix every issue found, regardless of severity.** If it was worth flagging at confidence ≥80, it's worth fixing. Cap at 5 rounds. If still not converged, route remaining issues to a fresh opus subagent (one per cluster) rather than deferring. |
| pr-fix-loop "ready to merge?" | **DO ask before final merge** if no auto-merge configured (merging is itself a critical action — class 4). Otherwise proceed |
| Between-phase progression | **NEVER ask** when context usage < 40%. Proceed automatically once current phase verification is GREEN + multipass review clean. At ≥40% context, MAY surface ONE concise checkpoint: "Phase X complete (Y% used). Continue / compact / split?" — capacity decision, not review approval. See `rules/workflow.md` → Review Discipline → After review + fix |
| Between commits within a phase | **NEVER ask.** Commit per logical unit per `rules/workflow.md` `## Git` |
| Round 1 audit produced findings | **fix them and continue to Round 2 silently.** No "should I fix these?" prompt |
| Code review findings (any severity — CRITICAL / HIGH / MEDIUM / LOW / NIT / INFORMATIONAL) | **fix all of them.** Severity controls *how* (inline vs subagent), not *whether*. See "Fix routing" below. Never defer based on severity alone — including review-bot "non-blocking" findings. The audit already paid to find it. AX does not review — agent runs the multipass chain autonomously per `rules/workflow.md` → Review Discipline. |
| Plan / spec / design artifact produced (PLAN.md, ROADMAP.md, UI-SPEC.md, AI-SPEC.md, etc.) | **NEVER ask AX to review long-form artifacts.** Run `gsd-plan-checker` / `plan-design-review` / `gsd-ui-checker` autonomously and fix every finding (per severity rule). AX reviews ONLY if a sign-off gate is set (then surface a ≤10-line summary — objective, scope, risks, acceptance criteria — NOT the full doc) OR a Critical Decision Trigger fires. |
| End-of-phase commit needed | **commit autonomously** with conventional-commit message + HEREDOC body. Per `rules/workflow.md` `## Git` |
| Phase verification GREEN → next phase | **always invoke `neat-freak` first** (Phase 2f knowledge sync), then commit code + doc edits together. Skill is idempotent — safe to run every phase. No ask. |
| Open PR after final phase | **open it autonomously** (per Phase 6a). Don't ask "ready to PR?" |

### Fix routing — inline vs subagent (severity-agnostic)

Once an issue is flagged, it WILL be fixed. The only question is who fixes it. Pick by **cost to main thread**, not by severity:

| Route to | When (any one trigger) |
|---|---|
| **Inline (main thread)** | Touches ≤2 files · mechanical change (rename, add type, remove dead code, fix typo) · well-understood domain · estimated ≤500 lines of code to read · no new tests needed |
| **Opus subagent** (`feature-dev:code-reviewer` for review-fix, or task-scoped agent for new-code fixes) | Touches 3+ files · requires deep refactor · unfamiliar domain (new lib, new pattern) · estimated 500+ lines to read · touches concurrency / race / security / payment / auth / data-mutation logic (regardless of size — these always go to opus for the extra reasoning budget) · requires test scaffolding for new behavior |

Subagent contract: receives `{issue_id, file_paths, severity, finding_text}`, loads context from disk, applies fix, runs build+typecheck+lint+tests, returns `{status: FIXED|BLOCKED, files_touched: [...], commit_sha}` ≤200 tokens. Main thread aggregates, never sees raw fix output.

**Anti-pattern to avoid:** flagging an issue at confidence ≥80 and then "deferring as MINOR follow-up" because it's tedious. That's the exact failure mode the user called out — the audit found it, so fix it. If the fix is expensive, that's what subagents are for.

### How to ask when a Critical Decision Trigger IS hit

Format (≤ 3 sentences total):

```
[CRITICAL DECISION] <one sentence: what's at stake and why this is class N>
A) <option> — <consequence>
B) <option> — <consequence>
Pick A / B / or describe a third path.
```

No essay. Just the decision. Then **wait** — do not proceed until user answers.

### Mid-flight escape hatch (user-initiated)

User can interrupt at ANY point with: "stop", "pause", "wait", "let me look", or by hitting Ctrl-C. Respect interruption immediately. Resume on user's explicit "continue" / "go" / "proceed" / "moveon".

### Status updates while autonomous

While running autonomously, emit ONE short progress line per phase boundary (≤ 80 chars):

```
▸ Phase 2b · parallel-worktree (4 tasks) · running
✓ Phase 2b · 4/4 green · committed (a1b2c3d) · → Phase 2c
✓ Phase 2c · review clean · → Phase 2g
✓ Phase 2g · 6/6 PASS · → Phase 6a
```

NOT a multi-paragraph essay per phase. The user will read commits + PR description for detail; mid-flight chatter steals their attention without informing them.

### Final report (at PR-opened or PR-merged)

ONE summary block (per existing Exit section, augmented):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /big-task ▸ COMPLETE  (autonomous run)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Phases shipped: N
 Commits: N      LOC: +A / -B
 Tests: unit X / integ Y / e2e Z
 Autonomous decisions made:
   • <decision 1 — what was silently picked and why>
   • <decision 2 — ...>
 Critical-decision pauses: N (none / list)
 Deferred follow-ups (FLAG batch): N (linked from PR)
 PR: <url>
```

The `## Autonomous decisions` log is non-optional — it's the receipt the user needs to audit autonomy after-the-fact.

---

## Phase 0.0 — Project workflow profile (FIRST, auto-detects)

Profile routing happens BEFORE the tier rubric. Three-step resolution:

### Step 1 — Explicit block in `./CLAUDE.md` (highest priority)

Grep for `workflow-profile:start` in `./CLAUDE.md`. If found, extract `<name>` from the `## Workflow Profile: <name>` line inside the block. That's the profile. Skip to Step 3.

(CLAUDE.md is loaded into session context at start — usually you can just scan existing context instead of re-reading the file.)

### Step 2 — Auto-detect from repo signals (runs only when no explicit block)

Run ONE bash command to collect signals (≤1s):

```bash
{
  # Schema: concrete file existence tests only — DO NOT use `ls glob | head` because that always succeeds on empty input in zsh
  ( [ -f prisma/schema.prisma ] || [ -f drizzle.config.ts ] || [ -f drizzle.config.js ] || [ -f drizzle.config.mjs ] || [ -f knexfile.js ] || [ -d db/migrations ] || { [ -d migrations ] && find migrations -maxdepth 1 -name "*.sql" 2>/dev/null | grep -q . ; } ) && echo schema
  # Auth / payment libs
  [ -f package.json ] && grep -qE '"(stripe|@stripe|better-auth|next-auth|@auth/core|lucia)"' package.json 2>/dev/null && echo auth-payment
  # Components dir (root OR src/ OR app/) + UI framework
  ( [ -d components ] || [ -d src/components ] || [ -d app/components ] ) && [ -f package.json ] && grep -qE '"(tailwindcss|@radix-ui|@chakra-ui|@mui/material|shadcn)"' package.json 2>/dev/null && echo components-ui
  # Locked design reference
  ( [ -f HANDOFF.md ] || [ -d directions ] || [ -d docs/design ] ) && echo design-ref
  # E2E framework
  [ -f package.json ] && grep -q '"@playwright/test"' package.json 2>/dev/null && echo playwright
  # Markdown content volume
  CONTENT=0
  for d in content/posts _posts content/blog docs/posts posts; do
    [ -d "$d" ] && CONTENT=$((CONTENT + $(find "$d" -maxdepth 2 -name "*.md" 2>/dev/null | wc -l | tr -d ' ')))
  done
  [ "$CONTENT" -gt 5 ] && echo "content-$CONTENT"
  # Backend language indicator
  ( [ -f go.mod ] || [ -f Cargo.toml ] || [ -f pyproject.toml ] ) && echo backend-lang
} 2>/dev/null
```

**Classify from emitted signals** — apply rules in order, first match wins:

| # | Rule | Profile | Reasoning |
|---|------|---------|-----------|
| 1 | `content-N` where **N >= 20** | `light-project` | Overwhelmingly content-dominant (blog, docs repo). Even if the repo also has components or accidental schema artifacts, the content is what ships. Blog with 270 posts + MarkdownRenderer component is still a blog. |
| 2 | (`schema` OR `auth-payment`) AND (`backend-lang` OR NOT `components-ui`) | `heavy-project` | Real backend risk (migrations / auth / payments) in a codebase that's primarily backend-shaped. Requires TDD + spec discipline. |
| 3 | `components-ui` OR `design-ref` OR `playwright` | `ui-project` | UI work with visual verification stack. Shichuan/Elan canonical shape. |
| 4 | `content-N` where N >= 5 (fell through rule 1) | `light-project` | Moderately content-dominant but mixed. Still prefer light unless clear heavy signal. |
| 5 | Anything else (only `backend-lang`, or nothing) | `unknown` | Can't confidently classify — fall through to Phase 0 rubric. |

Call this the **repo-shape profile**. It reflects what the codebase IS, not what the current task IS.

### Step 2.5 — Task intent (judgment, NOT keyword matching)

The repo scan answers "what shape is this project?". Now you need to answer "what shape is this task?". Reason about the request — do NOT pattern-match words. You are an LLM; you can read the task holistically the way an experienced engineer would. Someone saying "I was reading about Stripe" is not the same as "integrate Stripe payments", even though both contain the word Stripe.

**The core question: what is the task actually doing to the system?**

Classify what the task modifies or introduces. These categories carry inherent risk regardless of repo shape:

**"Heavy by nature" — modification risk dominates any repo shape**
- Persistence layer changes — schema, data model, new tables, column adds, migrations
- Trust boundary changes — building or altering an auth/authz/session/permissions system
- Revenue path changes — code that actually moves money (charges, refunds, credits, paywall gating)
- Atomicity/concurrency guarantees — transactions, distributed locks, idempotency keys, race-condition fixes
- Cross-system contracts — API contract changes with external consumers, protocol versioning, webhook schemas between services
- New architectural subsystem introduction — something that doesn't exist yet in the repo and whose shape will be copied by future code

**"Light by nature" — task is content or cosmetic**
- Written prose work — articles, translations, copy edits, doc updates, typos, README changes
- Pure cosmetic visual tweaks — color, spacing, alignment, font-size — where no new UX pattern is being introduced
- Single config/script tweaks where the config schema is stable and the change is one line or one value

**"UI by nature" — rendered output, no system-risk boundary crossed**
- Building/restyling components, screens, routes that apply existing design patterns
- The N+1-th application of a pattern that already lives in the repo

**Framing questions when the above doesn't settle it cleanly:**
1. **Blast radius** — if this ships wrong, what breaks? A wrong color is a bad afternoon. A double-charge is a refund + customer anger + possible chargeback fees. Bigger blast → heavier tier.
2. **Reversibility** — can a single `git revert` undo this, or is there data migration / state mutation to unwind? Unwindable-with-data = heavier.
3. **Design vs. translation** — is the user asking for a *design decision* (which pattern? which trade-off?) or the *translation of an existing design* (apply HANDOFF.md to these 5 screens)? Decisions are heavier; translations are lighter.
4. **Pattern novelty** — is this the N+1 application of a known pattern, or does this task set a new pattern? New pattern = heavier.

### Combining rule → final profile

Apply in order, first match wins:

1. **Task is heavy by nature** (any of the 6 categories above) → `heavy` regardless of repo
2. **Task is light by nature** (pure content / cosmetic / trivial config) → `light` regardless of repo
3. **Task introduces a new subsystem or sets a new architectural pattern** → `max(repo, one-level-up)` — a blog getting a real-time comment subsystem promotes to ui or heavy, not light
4. **Task matches the repo's default shape** (UI work in a UI repo, content in a blog repo) → use the repo profile
5. **Genuinely ambiguous** — default to the lighter tier and proceed. If the task grows beyond the tier mid-flight, escalate then. Only ask the user upfront when the request is unparseable.

Print the reasoning, not a label: `Profile: heavy (repo: light; intent: task introduces a revenue boundary — Stripe paywall)`. State what you judged, not what you matched.

### Examples (showing judgment, not lookup)

- Blog repo + "translate this post" → `light` — task is prose translation; repo is light; align.
- Blog repo + "add Stripe paywall for premium posts" → `heavy` — task introduces a revenue boundary; blast radius is customer money; repo shape is irrelevant.
- Backend repo + "fix a typo in README" → `light` — task is prose; no system-risk boundary; repo shape is irrelevant.
- Backend repo + "add a new column to the users table" → `heavy` — task modifies persistence; even though it's a small diff, the blast radius of a bad migration is high.
- UI repo + "build a real-time notification subsystem from scratch" → `heavy` — task introduces a new architectural subsystem that will set patterns.
- UI repo + "restyle the button to match the new design reference" → `ui` — task is translation-of-design, N+1 pattern application.
- UI repo + "decide whether to use Zustand or Redux for state management" → `heavy` — task is a design decision that will be copied across the codebase.
- Any repo + "fix alignment of the footer on mobile" → `light` — pure cosmetic tweak, no pattern change.

### Step 3 — Route by final profile

**If `light-project`:**
- **Exit big-task immediately.** Execute the request directly in the current context — no subagents, no planning, no tier rubric, no superpowers cycle.
- This is the project's "just do it" stance for solo blog/content/script work.
- **Escalation exception:** if the request clearly involves schema migrations, cross-service protocol changes, atomicity, or concurrency, **silently escalate to Phase 0 rubric** (per Phase -1 auto-resolution table) and log the escalation in the PR's `## Autonomous decisions` section. Do NOT pause to confirm — schema/auth/concurrency are class-2 critical decisions only when the user is making the architectural choice itself, not when escalating tier.

**If `ui-project`:**
- **Force Tier 3 (GSD-lite), skip Phase 0 rubric entirely.** File count and "architectural risk" heuristics don't apply — UI work is visual-driven with Playwright verification, which inverts the usual risk calculus.
- Use superpowers `subagent-driven-development` for multi-component work. Invoke `brainstorming` ONLY for a truncated spec (1 page max) — do NOT produce inline code, TypeScript essays, or 1000+ line plans.
- Plans are checkbox task lists (files + Playwright assertion per task), not treatises.
- **Verification at Phase 2g is MANDATORY Playwright sweep**: Claude reads the PNGs directly (multimodal), compares against design reference. No LLM verifier agent.
- **Skip GSD entirely** — no `.planning/` phase directories, no CONTEXT/PATTERNS/RESEARCH/VALIDATION/VERIFICATION meta-artifacts.

**If `heavy-project`:**
- Proceed with Phase 0 rubric below, BUT at Tier 4 use superpowers full cycle (`brainstorming` → spec → `writing-plans` → `subagent-driven-development` → `requesting-code-review` → `verification-before-completion`), NOT the `/gsd-*` chain.
- Worktrees, TDD-mandatory, human + automated code review all apply.
- Invoke `/gsd-*` only on explicit user request ("use GSD", "/gsd-autonomous") OR when genuinely needed for cross-phase dependency tracking.

**If `unknown`:** fall through to Phase 0 rubric. Default Tier 4 engine is superpowers, NOT `/gsd-*` chain (see description paragraph above). When the task completes, if the project has durable character, suggest the user run `/workflow-profile <name>` to make routing sticky and skip the detection cost next time.

### Overrides

- User says "skip workflow" / "just do it" / "quick and dirty" → drop to direct execution regardless of profile.
- User says "use GSD" / "use superpowers" → override the engine choice for this one task.
- User wants durable override: run `Skill(skill="workflow-profile", args="<light|ui|heavy>")` to write an explicit block (wins against auto-detect forever after).

### When auto-detection gets it wrong

If detected profile is obviously wrong (e.g., auto-detected `ui` on a repo that's actually a backend-with-small-UI heavy project), **trust the auto-detect and proceed silently** (per Phase -1). Re-route ONLY mid-flight if 2+ phases produce FLAG verdicts pointing at the wrong profile — at that point the evidence is on disk, not a judgment call. Log the detected profile in PR `## Autonomous decisions` so the user can `/workflow-profile <name>` to pin a different one for next time.

---

## Phase 0 — Risk-tier decision (≤ 30s)

**Risk is the primary axis. File count is secondary.** A 15-file UI migration from a locked design spec is LOWER risk than a 3-file atomic credit-deduction change. Route accordingly.

### Decision rubric

| Tier | Signals | Process |
|------|---------|---------|
| **Tier 2 (Direct)** | Bug fix, typo, one-liner, single-function change, isolated refactor | Fix on branch → test → merge. No GSD, no big-task scaffolding. |
| **Tier 3 (GSD-lite)** | Feature addition on existing primitives, locked-design UI work, new endpoint in well-trodden pattern, component from design reference, 3-10 files, design / spec / acceptance already clear | Inline plan (≤1 page) → TDD → multipass review (`code-reviewer` + domain pass; +`security-reviewer` / `database-reviewer` if triggers fire) → PR. Skip plan-checker, skip CONTEXT/SUMMARY docs, skip revision loop. See `rules/workflow.md` → Review Discipline. |
| **Tier 4 (Full GSD)** | Atomicity / concurrency / schema / protocol change, unfamiliar domain, cross-phase dependencies, genuinely ambiguous requirements, 10+ files across multiple packages, regression-sensitive migrations | Full `gsd-*` chain: discuss → plan → plan-check → execute → verify → cleanup. Multi-wave parallelism pays off here. |

### When GSD is PURE OVERHEAD (skip full GSD even at tier 4 file count)

- **Locked-design UI migration:** design reference (HANDOFF.md, Figma export, `directions/*.jsx`, etc.) already specifies pixel-exact layout. Most of GSD's "what are we building?" scaffolding is redundant ceremony. Use Tier 3 GSD-lite instead.
- **Repetitive pattern application:** adding the N+1-th screen that follows the same shape as the existing N. Copy the pattern, adjust for new content, ship.
- **Solo dev + short horizon:** traceability / handoff artifacts exist to coordinate a team. If no one else will read them, they're writing docs for yourself at significant token cost.
- **Design already validated:** if `/gsd-spike` or `/gsd-sketch` already produced findings, don't re-plan those findings through another plan-checker loop. Apply them directly.

### When GSD is WORTH IT (insist on tier 4 even at low file count)

- **Atomic / concurrent / transactional logic:** plan-checker catches race conditions before execution. Cheaper than debugging production.
- **Schema changes / migrations:** compile-time types can pass while the live DB is broken. Full verification gates matter.
- **Multi-plan wave parallelism:** 2+ independent workstreams benefit from explicit dependency declaration + parallel executor agents.
- **Revenue-path code:** payment, credits, unlock flows — correctness > velocity.
- **Cross-cutting protocol changes:** shifting a message format or API contract across many call sites — plan-checker's coverage audit earns its keep.

**Tier ambiguity → silently pick the lighter tier and proceed** (per Phase -1 auto-resolution + the existing "bias toward lighter tier" rule). Log the chosen tier + the alternative considered in PR `## Autonomous decisions`. Do NOT ask the user mid-flight — if the lighter tier turns out wrong, escalate by promoting the *next* phase to a higher tier rather than backtracking the current one.

Default = proceed at the rubric-matched tier. **Bias toward the lighter tier when in doubt.**

---

## Phase 0.5 — Optional pre-phase (tier 4 only)

Use when an idea is unproven OR UI-heavy with unclear direction. Produces throwaway output that auto-wraps into a project skill, so the learnings persist after exploration.

- **Feasibility unknown** ("can we even do X?"): `Skill(skill="gsd-spike")` → throwaway experiment → `Skill(skill="gsd-spike-wrap-up")` to package findings into a project skill.
- **UI direction unclear** ("what should this look like?"): `Skill(skill="gsd-sketch")` → HTML multi-variant mockups → `Skill(skill="gsd-sketch-wrap-up")` to package.

Default = skip. Only invoke when requirements are genuinely ambiguous at the implementation or aesthetic level.

**External design artifacts (brownfield bundles):** If the user hands you a pre-made design bundle from an external tool (Claude Design, Figma export, v0 export, external spec/prototype, chat log with locked decisions), **copy it to a persistent repo path before Phase 1** — typically `docs/{project-slug}/reference/`. Do not leave references pointing at `/tmp/` or external URLs — they will break mid-project. Then cite these persistent paths in PROJECT.md so downstream phases always find them.

---

## Model selection (consistency across all subagents)

When `.planning/config.json` has `model_profile: "quality"`, **every GSD subagent spawned throughout the big-task flow should use Opus** — not just researcher/roadmapper as the current `gsd-tools` per-role defaults set. Pass `model: "opus"` explicitly on all `Task(subagent_type=...)` invocations:

- `gsd-research-synthesizer` (tool default is sonnet even under quality; override)
- `gsd-plan-checker`, `gsd-verifier`, `gsd-nyquist-auditor`
- `gsd-codebase-mapper` (both initial map and refresh scans)
- `feature-dev:code-reviewer` (Phase 4 tracks)
- `think-ultra` (Phase 2c, Phase 3)

For `balanced` profile: Sonnet everywhere. For `budget`: Haiku for simple retrieval/formatting only, Sonnet for anything requiring judgment. For `inherit`: match the current session model.

Rationale: Tier 4 multi-week scope amortizes the Opus cost across downstream planning/execution — cheaper than shipping a bad plan and rewriting phases. Don't let per-role defaults silently downgrade synthesis or verification.

---

## Subagent Dispatch Policy

Every phase below carries a **Subagent policy** line. The policy has four modes, chosen by the nature of the work, NOT by tier:

| Mode | When | Main-thread consumption |
|---|---|---|
| **parallel-worktree** | Implementation on disjoint files, no shared state | <20% — each subagent writes in its own worktree; orchestrator collects short summaries |
| **parallel-readonly** | Investigation, review, visual verification, audit, doc-check — anything that doesn't write | <20% — fan out one subagent per target; zero write-conflict risk |
| **serial-subagent** | Implementation on shared files, or sequential build-up where each task depends on the last | ~30% — `superpowers:subagent-driven-development`, one implementer at a time with fresh per-task context |
| **inline** | Single-file / single-function change, Tier 2 hotfix, trivial decision | 100% — no subagent overhead is worth paying |

**Default: NEVER inline when tier ≥ 3 AND independent task count ≥ 3.** Past that scale, inline bloats main-thread context and defeats the autonomous-run advantage of subagent architectures.

**Orchestrator discipline (applies to all subagent modes):**
- Subagents load inputs from disk themselves (plan file, design ref, diff snapshot). Do NOT inject full task text from controller into every prompt — that's how superpowers' orchestrator accidentally hoards context across a 20-task plan.
- Subagents return structured summaries ≤200 tokens (`{task, status, findings}`), not raw output.
- Orchestrator state lives on disk (`.planning/phases/N/state.json` for Tier 4, TodoWrite for Tier 3) — never in main-thread chat history.
- Use `superpowers:using-git-worktrees` before any parallel-worktree dispatch. Worktree isolation is what removes the shared-state bar that `superpowers:dispatching-parallel-agents` otherwise imposes on parallel implementers.

Announce the chosen mode when entering a phase: `Phase 2b · parallel-readonly (4 routes)`. Makes routing auditable and catches inline overuse.

---

## Phase 1 — Bootstrap

Route by tier from Phase 0.

**1a — Tier 3 GSD-lite (DEFAULT for most "big" tasks):**

Write a short inline plan directly in the response. Keep it ≤1 page:

```
## Plan

**Objective:** [1 sentence]
**Files to touch:** [bulleted list, 3-10 files]
**Key references:** [design spec, existing pattern file, API contract]
**Test plan:** [unit / integration / E2E scope — be specific]
**Acceptance criteria:** [3-5 verifiable conditions]
**Rollback:** [how to revert if needed — usually just `git revert <commit>`]
```

Then proceed to Phase 2 with this inline plan as the single implicit phase. **Do NOT spawn `gsd-planner`, `gsd-plan-checker`, `gsd-discuss-phase`, or any `.planning/` scaffolding.** The value of those agents is catching ambiguity and architectural risk that isn't present in tier 3 work.

Skip straight to TDD: write failing tests based on acceptance criteria → implement → verify.

**1b — Tier 4 full GSD, new project:** `Skill(skill="gsd-new-project")`. Creates `PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md`. For brownfield codebases, `gsd-new-project` will offer to run a codebase map — **accept it and choose `gsd-map-codebase` (comprehensive)**. The 4-agent parallel sweep produces 7 structured docs (STACK, INTEGRATIONS, ARCHITECTURE, STRUCTURE, **CONVENTIONS, TESTING, CONCERNS**). The last 3 — especially CONCERNS (README drift, tech debt, v2 migration blockers) — are what make downstream phase planning actually work for multi-week scope.

**1c — Tier 4 full GSD, existing `.planning/`:** If `.planning/codebase/` is missing or stale, refresh it first:
- **No existing map, or major codebase changes since last map:** `Skill(skill="gsd-map-codebase")` — 4 parallel agents, 7 comprehensive docs. Essential for Tier 4 — lightweight scans skip CONCERNS/CONVENTIONS/TESTING which planners need.
- **Recent map exists but one specific area changed substantially:** `Skill(skill="gsd-scan" args="--focus <area>")` — 1 agent, targeted refresh.

Then `Skill(skill="gsd-new-milestone")` — creates milestone ROADMAP.

**After ROADMAP.md is created (1b or 1c):** run `Skill(skill="gsd-analyze-dependencies")` to auto-suggest `Depends on:` entries for each phase.

---

## Phase 2 — Phase loop (per phase)

**Tier 3 (DEFAULT — GSD-lite):** route by independent task count (see Subagent Dispatch Policy).

- **≤2 tasks on same file/module** → **inline**. TDD → implement → `code-reviewer` agent → commit.
- **3+ tasks on shared files** → **serial-subagent** via `Skill(skill="superpowers:subagent-driven-development")`. Fresh implementer + spec reviewer + quality reviewer per task.
- **3+ tasks on disjoint files, mechanical work** (locked-design migration, pattern N+1 application) → **parallel-worktree**: isolate each task with `superpowers:using-git-worktrees`, then dispatch parallel `Task()` implementers. Worktree isolation removes the shared-file bar. If `.planning/` already exists, `Skill(skill="gsd-execute-phase")` does this natively.

Skip CONTEXT.md / PLAN.md / SUMMARY.md ceremony regardless. One phase, one commit batch, done.

**Tier 4 (full GSD):** `Skill(skill="gsd-autonomous")` runs the full loop: discuss → plan → plan-check → execute → verify → (audit/complete/cleanup) automatically. Use when risk justifies the multi-agent ceremony (see Phase 0 "When GSD is worth it").

**Manual / deep mode (tier 4 opt-in):** instead of (or before) `gsd-autonomous`, invoke sub-skills explicitly for finer control:

- `Skill(skill="gsd-spec-phase")` — Socratic spec refinement; use when WHAT the phase delivers is genuinely unclear.
- `Skill(skill="gsd-discuss-phase")` — adaptive context-gathering; use when autonomous would skip nuance the user must weigh in on.
- `Skill(skill="gsd-list-phase-assumptions")` — surface implicit assumptions BEFORE planning. Cheap way to front-load the plan-checker's most valuable catches.
- `Skill(skill="gsd-plan-phase")` — standalone plan creation with plan-checker loop.
- `Skill(skill="gsd-review")` — cross-AI peer review; invoke only for novel patterns or revenue-path changes.
- `Skill(skill="gsd-execute-phase")` — wave-based execution; pause between phases.

**Escape hatches for over-engineered tier-4 flows:**
- `Skill(skill="gsd-fast")` — trivial task inline, no subagents, no planning overhead. Use when you accidentally routed a tier-2 task through big-task.
- `Skill(skill="gsd-quick")` — atomic commits + state tracking but skip optional agents (plan-checker, verifier). Middle ground when you want GSD's commit discipline without the ceremony.

### 2a — Plan specification (by tier)

**Tier 3 (GSD-lite) — minimum viable plan:**
- **Unit tests:** TDD — failing test first, then implementation. Non-negotiable.
- **Design reference:** cite the authoritative source (HANDOFF.md, Figma URL, existing pattern file) in the inline plan. No need to generate a new UI-SPEC.md if one already exists upstream.
- **Acceptance criteria:** 3-5 verifiable conditions. Grep-checkable beats subjective.
- **Integration / E2E:** only if the task actually crosses system boundaries. A pure-UI component doesn't need integration tests.

**Tier 4 (full GSD) — every phase must include:**
- **Unit tests:** TDD.
- **Integration tests:** real APIs/DBs, no mocks (per `rules/engineering.md`).
- **E2E tests:** UI changes → `e2e-runner` agent.
- **UI spec:** frontend phase WITHOUT existing design reference → `Skill(skill="gsd-ui-phase")`. **Skip if a locked design reference already exists** (e.g., HANDOFF.md + directions/*.jsx authoritative). Don't double-spec.
- **AI spec:** AI-heavy phase (prompts, evals, guardrails) → `Skill(skill="gsd-ai-integration-phase")`.
- **Design doc:** 2-5 sentences covering data flow + key decisions.

**Before planning (tier 4):** `Skill(skill="gsd-list-phase-assumptions")` surfaces implicit assumptions BEFORE `gsd-plan-phase`. This is the single cheapest way to front-load the plan-checker's most valuable catches.

### 2b — Implement

**Subagent policy:**
- Tier 3, ≤2 tasks same file → **inline**
- Tier 3, 3+ tasks shared files → **serial-subagent** via `superpowers:subagent-driven-development`
- Tier 3, 3+ tasks disjoint files (mechanical) → **parallel-worktree** (set up worktrees with `superpowers:using-git-worktrees` first, then dispatch parallel `Task()` implementers)
- Tier 4 → **parallel-worktree**, orchestrated by `gsd-autonomous` (wave-based)

Announce: `Phase 2b · <mode> (<N> tasks)`.

TDD non-negotiable: tests red → minimal impl green → refactor. Per-phase atomic commit (from `/gsd-execute-phase` or inline commit).

### 2c — Review

**Multipass per `rules/workflow.md` → Review Discipline.** Tier 3+ runs ≥2 passes; never ship after a single pass. Tier 4 already enforces this via Phase 3/4. AX never reviews — agent runs every pass autonomously.

**Pass 1 — `code-reviewer` agent.** Reads diff, returns severity-classified findings.
- **Small diff (<500 LOC, <5 files):** single agent.
- **Large diff (≥500 LOC or ≥5 files):** **parallel-readonly** fan-out — one reviewer per concern (security / types / tests / logic / error-handling). Each returns `{concern, findings: [{severity, location, note}]}` ≤200 tokens. Aggregate, dedupe overlap.

**Pass 2 — domain reviewer.** Pick by language/stack — `Skill(skill="code-review")`, `python-review`, `go-review`, or equivalent. Catches idioms/anti-patterns Pass 1 misses.

**Triggered passes (any tier, parallel with Pass 2):**

| Trigger in diff | Pass |
|-----------------|------|
| Auth / secrets / user input / API endpoints | `security-reviewer` agent or `Skill(skill="security-review")` |
| Schema / migration | `database-reviewer` agent |
| New tests | Verify behavior assertions, not mock existence (built into Pass 1 brief) |

UI changes are covered by Phase 2g visual verification — don't double-pass.

Per Phase -1: **fix all findings**, severity controls how (inline vs subagent), not whether.

**Tier 3:** skip `think-ultra` unless the diff involves security / concurrency / data mutation.
**Tier 4:** `Skill(skill="think-ultra")` on the phase diff (`git diff <phase-base>...HEAD`) AFTER pass 1 + pass 2 + triggers. Focus: regressions, unused code, test gaps, architecture concerns, security. Address HIGH/CRITICAL before proceeding.

### 2d — Audit-fix loop (OPTIONAL for tier 3)

Only run if Phase 2c surfaced findings worth sweeping.

**Tier 3:** `Skill(skill="audit-fix-loop")` — iterative fix-test-verify. Skip entirely if review was clean.
**Tier 4:** `Skill(skill="gsd-audit-fix")` — integrated audit-to-fix pipeline with phase state.

Both terminate when zero high-confidence issues remain and changed-file coverage hits 80%+.

### 2e — Reflect (SKIP for tier 3 unless something surprising surfaced)

**Tier 4:** `Skill(skill="gsd-extract_learnings")` — structured extraction into the gsd learnings store for future phases.
**Tier 3:** only capture learning if it's genuinely new and cross-project-applicable (e.g., a framework gotcha, a surprising library behavior). Otherwise skip — project memory isn't a journal. Append to `~/.claude/projects/<project>/memory/` only for durable patterns.

### 2f — Knowledge sync (AUTO — runs every phase)

**Always invoke `Skill(skill="neat-freak")` at phase boundary.** Three-audience editorial pass:

1. **Agent memory** (`~/.claude/projects/<...>/memory/`) — relative dates → absolute, completed todos removed, conflicting facts merged
2. **Project root markdown** (`CLAUDE.md` / `AGENTS.md`) — routes / env vars / decisions kept current for the next session
3. **`docs/` + `README.md`** — integration-guide / architecture / runbook / handoff files reconciled against the diff (cross-project sync if upstream/downstream affected)

The skill is internally idempotent — it no-ops cleanly when there's nothing to reconcile, so running on every phase is safe. The doc edits land in the same end-of-phase commit as the code (per Phase -1 auto-resolution).

**Codemaps:** if codemaps exist AND were meaningfully affected → `Skill(skill="update-codemaps")` AFTER neat-freak. Codemap regeneration is its own concern (architecture diff visualization), not part of editorial reconciliation.

### 2g — Verify

**Tier 3, no UI changes:** **inline** UAT — list 2-3 verifiable behaviors, check each. Open the dev server and click through if frontend.
**Tier 4, no UI changes:** `Skill(skill="gsd-verify-work")` — conversational UAT with checklist.

**MANDATORY for ANY UI phase — visual verification pass:**

1. Boot dev server (`pnpm dev` or equivalent).
2. Playwright screenshot sweep via `webapp-testing` skill or `npx playwright` — capture every changed route × every theme variant, save to `docs/reports/{phase}-visual/`.
3. **Subagent policy — scale by screenshot count:**
   - **≤3 PNGs total (route × theme)** → **inline**: Claude reads each PNG with `Read` (multimodal), compares against design reference (`HANDOFF.md` / `directions/*.jsx` source / Figma PNG). Per-screen verdict in main thread.
   - **4+ PNGs** → **parallel-readonly**: dispatch one visual-verify subagent per PNG. Each receives `{screenshot_path, design_ref_path, route, theme}`, reads both with `Read`, returns `{route, theme, verdict: PASS|FLAG|BLOCK, concerns: [string]}` ≤150 tokens. Main thread aggregates into a verdict matrix — no raw screenshot data in main-thread context.
4. Per-screen verdict: PASS / FLAG / BLOCK. For BLOCK → open a fix task before declaring phase verified. For FLAG → surface specific concerns (spacing, color, alignment, missing element) to user for decision.
5. **FLAG handling — autonomous mode (Phase -1):** Open a `TodoWrite` follow-up for each FLAG with the specific concern (spacing, color, alignment, missing element, exact letter-spacing, etc.). **Continue to next phase without pausing.** Surface the entire batch of FLAG items at end-of-milestone in the PR description (`## Visual verification flags`). User reviews them post-merge or as a single follow-up PR — not one-at-a-time mid-flight. BLOCK items still halt the phase: open a fix task and execute it inline before declaring phase verified (per Phase -1 auto-resolution table).

Static-grep tests do NOT catch visual drift. Claude's visual comparison is the primary defense; user eyeball is the backup for subtleties. See Adaptation hints → "Locked design reference" for CI-integrated pixel-diff setup.

Phase complete only when verification passes.

**Proceed to next phase.**

---

## Phase 3 — Final ultra-review (TIER 4 ONLY)

**Tier 3 skips this entirely.** The Phase 2c review already covered the diff; re-reviewing a single-phase feature through `think-ultra` on the full milestone diff is the same diff twice. Jump to Phase 5 (docs) if applicable, then Phase 6 (PR).

**Tier 4 (multi-phase milestone):**

1. `Skill(skill="gsd-audit-uat")` — cross-phase audit of all outstanding UAT and verification items. Surface anything unverified before the ultra-review.
2. `Skill(skill="think-ultra")` on the full milestone diff (`git diff <main-or-base>...HEAD`). Flag anything slipped through per-phase reviews.
3. Address HIGH/CRITICAL. Defer MEDIUM with explicit "deferred follow-up" entries.

---

## Phase 4 — 8-track final cleanup (TIER 4 ONLY)

**Tier 3 skips this entirely.** The parallel 8-agent cleanup sweep is designed for milestone-scale accumulation of drift. For single-phase tier-3 work, the Phase 2c review + commit discipline already catches what matters. Running 8 parallel agents on a 300-LOC change is over-engineering.

**Tier 4 only:** spawn **parallel** `feature-dev:code-reviewer` agents, one per track. Each agent returns a structured report; you implement only high-confidence + low-regret changes.

| # | Track | Tools | Confidence bar |
|---|-------|-------|----------------|
| 1 | Dedupe/consolidate code (reduce complexity without obscuring intent) | manual read | High |
| 2 | Consolidate shared type definitions where drift causes inconsistency | manual read | High |
| 3 | Unused code — verify with `knip` / `ts-prune` / `depcheck` then **manually verify** before removing | tool-assisted | Very high |
| 4 | Circular deps — `madge`; prioritize cycles affecting maintainability/correctness | tool-assisted | High |
| 5 | Strengthen typing — replace unsafe `any`, narrow overly-broad types. **Preserve legitimate `unknown` at boundaries.** | manual read | High |
| 6 | Error handling — remove ONLY unnecessary/misleading defensive patterns. **Keep try/catch at real boundaries** (recovery, logging, cleanup, user-facing errors). | manual read | High |
| 7 | Legacy/dead/fallback paths — remove only clearly obsolete. Verify NOT needed for: compatibility, migration, config, active users. | manual read | Very high |
| 8 | AI artifacts — stubs, placeholder logic, redundant comments, TODO-narration, edit-history comments. **Keep intent-explaining comments.** | manual read | Very high |

### Rules (non-negotiable, apply to all tracks)

- **No speculative rewrites.**
- **No public behavior changes** unless clearly intended and justified.
- **Small reviewable commits**, grouped by concern.
- **Before removing anything**: check dynamic usage, configuration, reflection, registration, hooks, codegen, framework conventions.
- **Preserve compat** unless you can prove removal is safe.
- **Flag medium- and high-risk findings separately — do NOT auto-implement them.** Report them for human decision.
- **For each implemented change**: one-line "why safe" justification in the commit message.

### Per-track validation after changes

Each track's agent runs:
- Build
- Type check
- Lint
- Unit tests
- Integration tests (if touched)

Report per-track:

```
TRACK N — [name]
Issues found: CRITICAL:X / IMPORTANT:Y / MINOR:Z
Implemented: [count] (list with why-safe)
Deferred: [count] (list with risk rationale)
Validation: build=[pass/fail] types=[pass/fail] lint=[pass/fail] tests=[pass/fail]
```

---

## Phase 5 — Final verification + docs/memory

1. `Skill(skill="verify")` — E2E spot-check of core flows
2. **Knowledge sync (milestone scope):** `Skill(skill="neat-freak")` — same three-audience editorial pass as Phase 2f, but scoped to the full milestone diff (`git diff <main-or-base>...HEAD`) rather than the last phase. Catches drift that accumulated across phases (cross-project sync, terminology consistency, doc-structure additions).
3. **Tier 4 only — codebase-verified docs:** if the milestone introduces user-facing behavior or new architectural primitives, follow neat-freak with `Skill(skill="gsd-docs-update")` — adds codebase-verification on top of editorial sync (each doc claim grep-checked against actual code). Skip for internal-only milestones.
4. `Skill(skill="update-codemaps")` if codemaps exist and architecture meaningfully changed.

---

## Phase 6 — PR + @claude review loop

### 6a — Commit + push + open PR

**Tier 4 (gsd):** `Skill(skill="gsd-pr-branch")` first — creates a clean PR branch filtering out `.planning/` commits so reviewers see code-only changes. Then `Skill(skill="commit-commands:commit-push-pr")` to push + open the PR.
**Tier 3:** `Skill(skill="commit-commands:commit-push-pr")` directly.

PR description template (enforce):

```markdown
## Summary
- [3-5 bullets: what changed and why]

## Phases shipped
[list from ROADMAP, or single-phase description]

## Tests added
- Unit: N
- Integration (real APIs): N
- E2E: N

## Risks / follow-ups
- [Track 4 deferred items]
- [Any MEDIUM-severity findings not addressed]

## Test plan
- [ ] [specific manual checks]
- [ ] CI green

@claude please review.
```

### 6b — PR review + CI self-healing loop

`Skill(skill="pr-fix-loop")` — polls CI, reads `@claude` review comments, fixes, re-requests review. Auto-cleanup cron on merge.

---

## Exit

When PR merges OR user says "done" / "stop":

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 /big-task ▸ COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Phases shipped: N
 Commits: N
 Tests added: unit X / integ Y / e2e Z
 LOC: +A / -B
 Tracks cleaned: 8
 Deferred follow-ups: N
 PR: <url>
```

Delete cron monitor. Suggest memory append if cross-project learnings emerged.

---

## Non-goals

- Not for bug fixes, typos, single-function changes, or Q&A
- Not a replacement for `/gsd-*` skills — those remain available for direct use when user wants finer control
- Does **not** require every project to have `.planning/` (tier 3 skips GSD bootstrap)
- Does **not** override user saying "quick and dirty" or "skip workflow"

---

## Adaptation hints

- **No `.planning/` + tier 3** → skip GSD, single implicit phase, inline plan
- **No frontend changes** → skip `gsd-ui-phase`, skip E2E tests
- **Monorepo** → apply 8-track cleanup per package, parallelize agents per package
- **No existing tests in repo** → include a "test scaffolding" sub-phase in phase 1
- **Schema/migration involved** → bump to tier 4 regardless of file count
- **User already has `.planning/` for unrelated work** → use `gsd-new-milestone`, don't clobber existing
- **`gsd-scan` vs `gsd-map-codebase`** — `gsd-scan` is 1 agent covering 1-2 focus areas (tech, arch, quality, concerns, or tech+arch default). `gsd-map-codebase` is 4 parallel agents covering all 4 areas → 7 docs including CONCERNS/CONVENTIONS/TESTING. **Tier 4 initial mapping needs `gsd-map-codebase`** — the missing 3 docs are critical for downstream phase planning. Reserve `gsd-scan` for targeted refreshes when a specific area changed.
- **AI-heavy phase (LLM prompts, evals, prompt engineering)** → invoke `Skill(skill="gsd-ai-integration-phase")` before `gsd-plan-phase` to produce AI-SPEC.md (framework selection + eval planning + guardrails).
- **External design bundle** (Claude Design, Figma export, v0, prototype) → copy to `docs/{project}/reference/` **before Phase 1**. Cite persistent paths in PROJECT.md — never reference `/tmp/` or external URLs that will break mid-project.
- **Locked design reference (HANDOFF.md, directions/*.jsx, theme-ui.jsx, Figma URL, screenshots)** → static-grep tests only catch textual/structural drift, NOT visual drift. Every UI phase MUST include a **visual verification pass** after execution:
  1. **Playwright screenshot capture** via `webapp-testing` skill or direct `npx playwright` — boot the dev server, navigate to each changed route, capture PNG per theme variant (light/dark × each family), save to `docs/reports/{phase}-visual/`
  2. **Claude visual comparison (primary defense)** — Claude is multimodal: use `Read` on each captured PNG + `Read` on the design-reference file (JSX source or reference PNG). Directly compare layout, color, spacing, typography, component presence. Produce a per-screen verdict: PASS / FLAG / BLOCK. For BLOCK → open a fix task. For FLAG → surface specific concern to user for decision.
  3. **Human eyeball (backup only)** — triggered only for FLAGGED items or for subtle details Claude may miss (exact letter-spacing, 2px shadow offset, specific font-weight nuance). PASS screens don't require human review — saves iteration time.
  4. **For milestones with 2+ UI phases** — set up Playwright + pixelmatch/resemble.js pixel-diff against checked-in baseline PNGs (reference = `directions/*.jsx` rendered once, treated as canon). 30-60 min setup, catches regressions forever after. Runs in CI. Pixel-diff is stricter than Claude's visual eye and catches 1-2px subtleties Claude might call PASS.
  **Why:** past experience — agents working from a plan can interpolate "reasonable" styling that doesn't match the reference, and static-grep won't flag it. Screenshot → Claude visual compare → pixel-diff (if configured) is a 3-layer defense; each catches what the others miss.
