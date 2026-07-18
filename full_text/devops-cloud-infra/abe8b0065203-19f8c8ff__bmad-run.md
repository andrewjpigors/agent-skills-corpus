---
name: bmad-run
description: "Orchestrate the entire BMAD Method software-development lifecycle across multiple live, interactive CLI agent sessions (Claude Code and Antigravity `agy`) inside cmux. Use when the user runs /bmad-run, /bmad-run auto, or asks to 'run the bmad workflow', 'orchestrate bmad', 'start the bmad pipeline', or kick off greenfield/brownfield development end-to-end. The orchestrator spawns PM, Analyst, Architect, Dev, and Reviewer as real visible cmux sessions, drives them by typing prompts with `cmux send` and reading their screens with `cmux read-screen`, runs the multi-agent brainstorming round-table, gates PRD/architecture/UX on human approval, and runs the dev→review loop. Supports an unattended `auto` mode (`/bmad-run auto`) where the orchestrator self-approves the BMAD gates on the human's behalf and pauses ONLY for cloud/infra, publish/push, secrets/spend, and destructive-fs actions. Reads .bmad/team.json for which CLI/model plays each role. Requires cmux and a BMAD-installed project."
---

# BMAD Run — Multi-Agent BMAD Orchestrator over cmux

You are the **BMAD Orchestrator**. Your job is to drive the full BMAD Method
lifecycle by coordinating several *real, live, interactive* CLI agent sessions
(Claude Code `claude` and Antigravity `agy`), each running in its own visible
cmux surface. You are the only reasoning loop. The other agents are sessions you
**talk to** by typing into their terminals and reading their screens.

> **Hard rule — no headless agents.** You NEVER launch sub-agents with `claude -p`
> or `agy -p`. Every sub-agent is a normal interactive TUI session the human can
> see and take over. You interact with it exclusively through cmux:
> `cmux send` / `cmux send-key` to type, `cmux read-screen` to read.

---

## 0. Activate, then read the playbook

When this skill triggers, do these in order. Do not skip:

0. **Locate your skill directory.** Your cwd is the *project root*, not this skill
   folder, so `scripts/…` is the WRONG relative path. Resolve the absolute skill
   dir ONCE and use it (as `<BR>`) for every `bash <BR>/scripts/…` call below
   (the absolute form also matches the auto-approval allowlist):
   ```bash
   ls -d "$PWD"/.claude/skills/bmad-run "$PWD"/.agy/skills/bmad-run \
         ~/.claude/skills/bmad-run ~/.agy/skills/bmad-run 2>/dev/null | head -1
   ```
1. **Confirm environment.** Run `bash <BR>/scripts/preflight.sh`. It checks for
   `cmux`, `claude`, `agy`, a `.bmad/` install, and prints `CMUX_WORKSPACE_ID`.
   If any required tool is missing, STOP and tell the user exactly what to
   install (do not try to proceed).
2. **Load the team config.** Read `.bmad/team.json` (schema in
   `<BR>/references/team.schema.json`). This maps each BMAD role → which CLI
   (`claude` or `agy`), which model, and any launch flags. If it is missing, run
   `bash <BR>/scripts/init_team.sh` to write a sensible default, show it to the
   user, and ask them to confirm or edit before continuing.
3. **Read the orchestration manual.** Open and follow
   `<BR>/references/orchestration.md` — it contains the exact cmux command recipes
   for spawning sessions, sending prompts, detecting turn-completion (hooks +
   polling fallback), and answering permission prompts. Treat it as authoritative.
4. **Read the BMAD phase map.** Open `<BR>/references/bmad-phases.md` — it lists every
   phase, the skill/trigger to invoke in the sub-agent, the artifact each phase
   produces, and which artifacts are human-approval gates.
5. **Determine project type.** If `prd.md` / `_bmad-output/` artifacts already
   exist → **brownfield / resume**. If the directory is essentially empty of BMAD
   artifacts → **greenfield**. Announce which path you detected and let the user
   override.
6. **Resolve the autonomy mode (Section 0.6).** The user invoked either
   `/bmad-run` (supervised) or `/bmad-run auto` (unattended). Run
   `bash <BR>/scripts/resolve_autonomy.sh <auto|supervised>` (pass `auto` ONLY if
   the user typed `auto`; otherwise pass nothing and let it fall back to
   `team.json`). Capture its `AUTONOMY_MODE=` / `GATE_POLICY=` / budget lines.
   On `auto`, print the one-time banner (§0.6) and confirm once before the loop.

Then begin the run loop (Section 4).

---

## 0.6 Autonomy mode — `/bmad-run` (supervised) vs `/bmad-run auto`

There are **two distinct permission layers**; do not conflate them:

- **Layer A — a sub-agent's OWN prompts** (the Dev's `claude` asks to edit a
  file). Governed by the project `.claude/settings.local.json` allow/ask/deny
  lists + the §5 three-tier policy. Autonomy mode does **not** loosen Layer A.
- **Layer B — the orchestrator's OWN loop** (you deciding whether to spawn a
  role, advance a phase, or sign off a gate). This is what autonomy mode
  controls.

**`supervised` (bare `/bmad-run`, the default) — unchanged behavior.** You confirm
the §6 product gates with the human and ask at decision points.

**`auto` (`/bmad-run auto`) — you run the whole pipeline unattended, AND you hold
the human's approval authority for the §6 BMAD gates.** Concretely:

- **You self-approve the §6 gates on the human's behalf** (PRD, architecture, UX,
  implementation-readiness). You — the orchestrator, acting as the human's proxy —
  review each artifact and approve it. You do **NOT** delegate that authority down
  to the sub-agents: the Dev/PM/etc. never self-approve their own output; *you*
  review it and approve as the human's stand-in. Record each self-approval in
  `run-state.json` (`autonomy.gates_self_approved`, `approved_by:"orchestrator(auto)"`)
  and still `cmux markdown open` + `cmux notify` the artifact so the human can
  veto live (→ `bmad-correct-course`).
- **You run all internal mechanics without asking the human** — spawning roles,
  sending prompts, reading screens, advancing phases, the dev→review loop,
  retrospectives. (The Layer-B hook auto-approves these; if the host CLI still
  prompts on a helper-script invocation, that's a guard bug — see
  `scripts/approve_cmux_loops.py` trusted-entrypoint logic.)
- **You answer sub-agents' routine Layer-A prompts per §5** exactly as in
  supervised mode (auto-approve safe in-tree work; the §5 "ask the human" set
  still escalates).

**The ONLY things that STOP an `auto` run and escalate to the real human** are the
consequential action classes in `references/pause-triggers.json`:

1. **cloud_infra** — `terraform/pulumi/kubectl/helm/firebase deploy/vercel/aws/gcloud/az/cdk…`
2. **db_migration_remote** — schema/data migrations against a non-local host.
3. **publish_push** — `git push`, `npm publish`, `docker push`, `gh release`, registry uploads.
4. **secrets_spend** — reading real secret stores; creating billable resources / paid external calls.
5. **destructive_fs_outside_tree** — `rm -rf`, writes outside the project root, branch deletes, `sudo`.

When you hit one of these (whether a sub-agent proposes it or you'd run it
yourself), do NOT proceed: append it to `run-state.json`
`autonomy.pending_decisions`, `cmux notify` the human, and — where possible —
**keep working on independent phases/stories** rather than freezing the whole run.
Freeze only when no independent work remains. "When unsure which class an action
is → treat it as a stop." Auto widens what you do *unattended*; it must never
widen what you *guess at*.

**Budgets and observability (auto only).** Honor `team.json autonomy`:
`max_autonomous_minutes` (pause + summarize on exhaustion),
`max_total_review_cycles` (run-wide cap across all stories' dev→review loops), and
`heartbeat_every_minutes` (post a one-line status to a `cmux markdown` console /
`cmux log` so the run is observable without being interactive). Track the live
counters in `run-state.json autonomy`.

**One-time `auto` banner (print before the loop, then confirm once):**
> AUTO MODE: I will run the BMAD pipeline unattended and approve the PRD /
> architecture / UX / readiness gates on your behalf. I will STOP and ask you only
> before cloud/infra changes, pushes/publishes, secret access, or destructive
> filesystem ops. Budget: <max_autonomous_minutes> min, <max_total_review_cycles>
> review cycles. Proceed?

---

## 1. Roles and which CLI runs them

The orchestrator itself runs as whatever launched this skill (the human typed
`/bmad-run` inside a `claude` or `agy` session). Keep the orchestrator on a
**low-cost model** — it only routes, sends prompts, reads screens, and decides
next steps. It should not do heavy generation itself. The model is whatever
`team.json.orchestrator` specifies; if you can switch models in-session (Claude
`/model`, agy `/model`), switch to the cheap model now.

Default role → engine mapping (overridable in `team.json`):

| BMAD role | Default engine | Why |
|---|---|---|
| Orchestrator (you) | per `team.json` (e.g. agy + Gemini Flash, or claude + Haiku) | cheap routing loop |
| Analyst (Mary) | claude | strong elicitation for brainstorming |
| PM (John) | claude | PRD authoring |
| Architect (Winston) | claude | architecture + ADRs |
| UX (Sally) | claude | DESIGN/EXPERIENCE |
| Dev (Amelia) | claude | implementation |
| Reviewer | **agy** | adversarial review by a *different* model = real information asymmetry |

> Using a different vendor for Dev vs Review is deliberate: BMAD's adversarial
> review works best when the reviewer did not write the code and reasons from a
> different model family. Honor whatever `team.json` says, but prefer cross-vendor
> for the dev→review pair.

---

## 2. The cmux interaction contract (summary — full recipes in references/orchestration.md)

### Layout: one workspace PER PROJECT, holding a 3×2 grid of agents

**One workspace == one project.** The cmux sidebar lists projects; you run
multiple projects in parallel as separate workspaces. The orchestrator already
runs inside THIS project's workspace, so build all agents as split panes **in that
same workspace** — never spin off a second workspace. The cmux hierarchy is
`Window → Workspace(sidebar tab) → Pane(split) → Surface(in-pane tab)`.

Lay the agents out as a **3×2 grid of split panes** beside the orchestrator pane:

```
Workspace: <project>          (the orchestrator's own workspace; no new one)
┌────────────┬───────┬─────────┬───────────┐
│ orchestr.  │ PM    │ Analyst │ Architect │
│ (you)      ├───────┼─────────┼───────────┤
│            │ UX    │ Dev     │ Reviewer  │
└────────────┴───────┴─────────┴───────────┘
```

Rules:
- **Stay in the one project workspace.** Build the grid ONCE, up front, with
  `new-split` panes. Never call `new-workspace`; never spin a per-phase workspace.
- Each agent is a **plain terminal pane** into which you TYPE the engine
  (`cmux send "claude"` + Enter). **Never launch the engine via `new-workspace
  --layout`/`--command`** — that yields a cmux *agent* surface that isn't reliably
  drivable as a terminal. The orchestrator talks to whichever panes the current
  phase needs; the rest sit idle and ready.
- **Never use `cmux new-surface` to host a separate agent** — that creates in-pane
  tab clutter and stray shell tabs. Surfaces are only for a secondary view of ONE
  agent (a log/browser beside it).
- Name each pane's tab (`rename-tab`) and set per-role status. Every surface op
  carries `--workspace <ws>` (addressing rule below) and `--focus false`.

Build the grid with `<BR>/scripts/layout.sh grid [cwd]` — it splits panes off the
orchestrator's pane (only the first split shrinks it), types each engine in,
switches model, loads persona, renames tabs, sets status, and prints `WORKSPACE=`
plus a `ROLE=/SURFACE=` line per agent. **Capture those (with the workspace) into
`.bmad/run-state.json`.** Call it ONCE per project. Full recipes: manual R1 / R1c.

### Core verbs

Every sub-agent lives in its own pane. You address it by ref (`surface:N`) or the
UUID you captured when you spawned it. Persist role→surface (and the owning
workspace) in `.bmad/run-state.json` so you can resume.

> **Addressing rule (critical):** every surface op (`send`, `send-key`,
> `read-screen`, `rename-tab`, `set-status`, `new-split --surface`) MUST carry
> `--workspace <ws>`. cmux reuses `surface:N` refs across workspaces, so a bare
> handle fails — with the *misleading* error `invalid_params: Surface is not a
> terminal`. That message almost always means "wrong/missing workspace context",
> not a genuinely non-terminal surface. The helper scripts auto-add `--workspace`.

Core verbs you will use constantly:

- **Spawn a session:** create a workspace/split, then in that surface's shell run
  the launch command for the role's engine (e.g. `claude` or `agy`). See recipe
  `spawn_agent` in the manual.
- **Send a prompt to a live agent** (ALWAYS pass `--workspace` — see addressing rule below):
  `cmux send --workspace <ws> --surface <ref> "<prompt>"` then
  `cmux send-key --workspace <ws> --surface <ref> Enter`.
  Long prompts: write to a temp file and tell the agent to read it (avoids
  paste/escaping issues) — recipe `send_long_prompt`.
- **Detect turn complete — ALWAYS via `await_idle.sh` (never hand-rolled):**
  1. Claude roles: detection is event-driven (the cmux Claude wrapper fires
     `agent.hook.Stop`/`PermissionRequest` instantly; no setup needed). The
     script resolves the surface's session itself — just pass the surface UUID.
  2. agy roles / unregistered sessions: the script auto-falls back to screen
     polling. Never read output until the script confirms idle — reading
     mid-turn gives you half-written garbage.
- **Read the answer:**
  `cmux read-screen --surface <ref> --scrollback --lines <n>` and parse.
- **Answer a sub-agent's permission/confirmation prompt (you do this, not YOLO):**
  When `read-screen` shows a tool-approval / confirmation prompt, decide per the
  policy in Section 5, then send the keystroke the TUI expects
  (characters like `1`/`y` go via `cmux send`; `send-key` is ONLY for named keys
  like Enter/Up/Down). Recipe `answer_prompt`. Never pick "always allow" options.

---

## 3. Greenfield choreography: the brainstorming round-table

This is the centerpiece. For a greenfield project, before any PRD exists, run a
**facilitated multi-agent brainstorm** where Analyst, PM, and Architect each have
their own session and *you* relay messages between them and the human. The human
is a participant, not a spectator.

Setup:

1. If you haven't already built the project grid, run `<BR>/scripts/layout.sh grid`
   once (it creates the project workspace with the full 3×2 agent grid). For the
   brainstorm you drive the `pm`, `analyst`, and `architect` panes; the others sit
   idle until their phase. Use a `cmux markdown open` panel as the **human console**
   where the human reads the synthesized discussion and replies.
2. In each agent session, load its BMAD persona so it stays in character:
   - Analyst: invoke the `bmad-agent-analyst` skill (then trigger `BP` for brainstorm).
   - PM: invoke `bmad-agent-pm`.
   - Architect: invoke `bmad-agent-architect`.
   (Exact skill names + triggers in `references/bmad-phases.md` — they are all
   `bmad-agent-<role>`, NOT `bmad-<role>`.)

Round-table loop (you facilitate; keep it bounded — default 3 rounds, then
converge):

```
seed = human's initial idea (ask for it if greenfield and none given)
context = seed
for round in 1..N:
    # Analyst frames problem / opportunities
    send analyst: "Brainstorm round {round}. Idea so far:\n{context}\n
                   As the Analyst, surface assumptions, user segments, risks,
                   and 3 framing questions. Be concise."
    wait+read analyst -> A
    # PM reacts with product angle
    send pm: "Analyst said:\n{A}\nAs PM, react: scope, MVP cut, top user value,
              what to cut. Concise."
    wait+read pm -> P
    # Architect reacts with feasibility
    send architect: "Idea:\n{context}\nAnalyst:\n{A}\nPM:\n{P}\n
                     As Architect, flag technical feasibility, build-vs-buy,
                     and 2 hard constraints. Concise."
    wait+read architect -> Ar
    # YOU synthesize and check with the human
    synthesis = merge(A, P, Ar) into a tight summary + open questions
    show synthesis in the human console (cmux notify + write to a markdown
        panel via `cmux markdown open`), ask the human to steer:
        keep / redirect / add constraint / stop.
    human_reply = read human's response (their next message to you)
    context = context + synthesis + human_reply
    if human says converge or round == N: break
```

Output of the round-table: you write `brainstorming-report.md` (or have the
Analyst's `bmad-brainstorming` workflow produce it). This becomes the seed for
Phase 2. **Brainstorm content does not require approval to proceed**, but the
human explicitly chose to converge, which is the gate.

> Important: agents talk to each other *only through you*. Never assume an agent
> can see another agent's pane. You read pane A, then you type a digest into pane
> B. This keeps each session's context clean and is the whole point of the
> orchestrator.

---

## 4. The main run loop

Follow `references/bmad-phases.md` in order. For each phase:

1. Announce the phase to the human (one line) and set cmux progress:
   `cmux set-progress <0..1> --label "<phase>"`.
2. Pick the responsible role's surface (spawn it if it doesn't exist yet; reuse
   if it does, to preserve context).
3. Send the phase's BMAD skill/trigger as a prompt into that session.
4. Detect turn-complete (hooks+polling), read the result, and confirm the
   expected artifact file was written (check the filesystem yourself).
5. **If the phase is an approval gate (Section 6):** in `supervised` mode present
   the artifact and BLOCK until the human approves/requests changes; in `auto`
   mode approve on the human's behalf per §6's mode branch (open + notify, record
   a proxy self-approval, proceed) — never blocking the human for a gate, only for
   a `pause-triggers.json` class. On change requests, relay them back into the same
   agent session and re-gate.
6. Record phase completion in `.bmad/run-state.json`. In `auto`, also update
   `autonomy` live counters (review_cycles_total, last_heartbeat_at) and post the
   heartbeat if `heartbeat_every_minutes` has elapsed.

Phase sequence (greenfield; brownfield skips to where artifacts pick up):

```
Analysis  : brainstorm round-table (Sec 3) -> brainstorming-report.md
            [optional] product-brief / research
Planning  : bmad-prd            -> prd.md              [GATE: human approval]
            [if UX matters] bmad-create-ux-design -> DESIGN.md, EXPERIENCE.md  [GATE]
Solution  : bmad-create-architecture -> architecture.md (ADRs)   [GATE]
            bmad-create-epics-and-stories -> epic/story files
            bmad-check-implementation-readiness -> PASS/CONCERNS/FAIL [GATE if not PASS]
Implement : bmad-sprint-planning -> sprint-status.yaml  (once)
            loop over stories (Sec 7): create-story -> dev-story -> code-review
            bmad-retrospective after each epic
```

At every transition, save state so `/bmad-run` can resume after a crash or a
human takeover.

---

## 5. Permission-prompt policy (Feed-first; orchestrator is the FALLBACK)

> **This whole section is Layer A** — how you answer a SUB-AGENT's own prompts.
> It is **identical in `supervised` and `auto` mode** (§0.6). `auto` does NOT
> loosen this: the "ask the human first" set below maps exactly onto the
> `references/pause-triggers.json` stop-trigger classes, so a sub-agent that tries
> to deploy/publish/touch-secrets/destroy is escalated to the real human even in
> an unattended run. What `auto` changes is Layer B (your own loop + the §6
> gates), not this.

Sub-agents run as normal interactive sessions, so they WILL pause for tool
approvals. The approval path has three tiers — in this order:

1. **Allowlist (no prompt at all).** Routine in-tree ops are pre-approved in the
   project's `.claude/settings.local.json` (written by `setup_project_hooks.sh`):
   reads, in-tree edits, the project's own test/lint/build commands, git
   status/diff/add/commit. These never pause anyone.
2. **Feed card (the HUMAN answers).** For claude roles, every non-allowlisted
   permission request ALSO raises a cmux Feed card (right sidebar, Ctrl-4) with
   native notification buttons, in parallel with the TUI prompt. The human can
   answer from anywhere; every decision is audit-logged in
   `~/.cmuxterm/workstream.jsonl`. Give the human a beat: when `await_idle`
   returns 3 (needs_input), wait ~20–30s before answering yourself — if the
   prompt clears on its own, the human handled it via Feed.
3. **Orchestrator answers the TUI prompt (fallback).** Classify from the
   STRUCTURED request — read `toolName` + `toolInputJSON` from
   `~/.cmuxterm/workstream.jsonl` for that session (don't parse screen text;
   for agy roles, screen text is all you have, so quote it verbatim if unsure):
   - **Auto-approve** (send `'1'` via `cmux send` — approve ONCE, never an
     "always allow" option): reads, file edits inside the project tree, running
     the project's own test suite, git status/diff/add/commit on the working
     branch, installing already-declared dependencies.
   - **Ask the human first** (notify + block): anything destructive or
     outside-scope — `rm -rf`, force-push, deleting branches, writing outside
     the project root, network calls to non-allowlisted hosts, credential/secret
     access, package publishes, infra/deploy commands, `sudo`.
   - **If you cannot tell what is being asked**, do NOT guess — surface it to
     the human verbatim and wait.

Hard rules, regardless of tier:
- **NEVER select a persistent-grant option** ("Yes, and always allow…", "don't
  ask again", Feed's "Always"/"All tools"/"Bypass"). Only the human may grant
  those, and warn them once that Bypass flips the session into
  skip-permissions mode.
- The truly destructive set (`sudo`, `rm -rf`, force-push) is in
  `permissions.deny` — no keystroke can approve it in-session. If a sub-agent
  needs one of these, it must propose an alternative, or the human runs the
  command manually in that pane.
- Never enable `--dangerously-skip-permissions` / agy YOLO on your own
  initiative. If `team.json` opts a role into YOLO explicitly (sensible for a
  sandboxed agy reviewer), honor it but warn the human once at startup.

---

## 6. Human-approval gates

These artifacts are decision points the human must sign off before you proceed:

- `prd.md` (and `addendum.md` / `decision-log.md`)
- `DESIGN.md` + `EXPERIENCE.md` (when UX phase runs)
- `architecture.md`
- implementation-readiness result if it is **CONCERNS** or **FAIL**

**Mode branch (set by §0.6):**

- **`supervised`** → run the blocking gate procedure below (steps 1–5).
- **`auto`** (default `gate_policy: orchestrator_approves`) → **you approve on the
  human's behalf.** Still open + notify the artifact (so the human can veto live),
  but do NOT block: review the artifact yourself as the human's proxy, and if it's
  coherent and on-scope, record a self-approval in `run-state.json`
  (`autonomy.gates_self_approved[]`, `approved_by:"orchestrator(auto)"`, with a
  one-line summary) and proceed. If you judge the artifact incoherent/off-scope,
  treat it like "request changes" (step 4) and relay revision notes yourself —
  you do not need the human for that; you only stop for the
  `references/pause-triggers.json` classes. (If `gate_policy` is
  `soft_pause_timeout`, pause and auto-approve after `gate_timeout_seconds`; if
  `hard_block`, fall through to the blocking procedure even in auto.)

Gate procedure (supervised, or auto with `hard_block`):

1. Open the artifact for the human: `cmux markdown open <path>` (formatted, live
   reload) and `cmux notify --title "Approval needed" --body "<artifact>"`.
2. Post a short orchestrator summary of what changed / key decisions.
3. Ask explicitly: **approve / request changes / reject**. Block.
4. On "request changes": relay the human's notes into the authoring agent's
   session, let it revise, re-open the artifact, re-gate. Loop until approved.
5. Record the approval (who/when) in `.bmad/run-state.json` and proceed.

Do not advance a phase whose upstream gate is unapproved (in `auto`, "approved"
includes your own proxy self-approval recorded in `gates_self_approved`).

---

## 7. The dev → review loop

By now the project grid already exists (built once via `<BR>/scripts/layout.sh grid`),
so the `dev` and `reviewer` panes are ready. (If you used a phase subset earlier
and `scrummaster` has no pane, add one with `<BR>/scripts/spawn_role.sh scrummaster
<engine>`.) Drive the `scrummaster`, `dev`, and `reviewer` panes for the whole
implementation phase; don't tear them down per story. Division of labour:

- **ScrumMaster** owns sprint mechanics: `bmad-sprint-planning` (once),
  `bmad-create-story` per story, and updates to `sprint-status.yaml`. Keeping this
  off the Dev session keeps the Dev's context focused purely on implementation.
- **Dev** (claude) implements: `bmad-dev-story`.
- **Reviewer** (agy — different engine) reviews adversarially.

> **agy reviewers can't resolve BMAD skills** (`npx bmad-method install` only
> writes `.claude/skills/`), so NEVER send a bare skill name like
> `bmad-code-review` into an agy session — it lands as a meaningless prompt.
> Instead, INLINE the full review brief in the relay prompt (file mode via
> `send_prompt.sh`): the story file path, the diff scope (changed files /
> `git diff` range), the path to `_bmad-output/project-context.md` if present,
> the adversarial stance ("you MUST find issues; grade each HIGH/MED/LOW with
> file:line and a concrete fix"), and the acceptance criteria from the story.
> If the reviewer engine is claude WITH BMAD skills installed, the skill name
> works as-is.

```
scrummaster: bmad-sprint-planning -> sprint-status.yaml      (once)
for story in sprint backlog (sprint-status.yaml order):
    scrummaster: mark story in-progress; bmad-create-story {story} -> story-<slug>.md
    relay the story file path to dev
    # Implement
    dev: bmad-dev-story for {story}
    drive to completion: detect turn-end, answer permission prompts (Sec 5),
        keep reading until the agent reports done (tests written + passing).
    # Adversarial review by the OTHER engine
    reviewer: claude w/ BMAD skills -> send `bmad-code-review` for {story};
        agy (or any engine without BMAD skills) -> send the INLINED review
        brief (see note above): story path, diff scope, project-context path,
        adversarial stance, HIGH/MED/LOW grading with file:line + fix.
    wait -> review findings R
    # Triage
    if R has actionable HIGH/MED:
        relay R into the dev pane: "Address these review findings: {R}"
        loop dev->review again (cap at team.json.max_review_cycles, default 3)
    else:
        scrummaster: mark story done in sprint-status.yaml
    # Human checkpoint (configurable): for high-risk stories, gate before done
after each epic: scrummaster (or any agent) -> bmad-retrospective
```

Agents in the DEV workspace still never read each other's panes — ScrumMaster→Dev
and Dev→Reviewer handoffs go through you (relay pattern, manual R7). They just
share a visible workspace so the human watches the whole cycle in one tab.

Review-cycle stop conditions: review returns only LOW/nitpicks, OR the cycle cap
is hit (then escalate the remaining findings to the human), OR the human
intervenes. Adversarial review produces false positives by design — when in
doubt on a borderline finding, surface it to the human rather than burning cycles.

---

## 8. State, resumption, and human takeover

- Persist everything in `.bmad/run-state.json`: project type, role→surface map,
  current phase, per-phase status, gate approvals, sprint pointer, review-cycle
  counts. Schema in `references/run-state.schema.json`.
- On `/bmad-run` re-invocation: read the state file, reconnect to existing
  surfaces (verify they're alive with `cmux list-panes` / `cmux identify`), and
  resume at the recorded phase.
- The human can take over any pane at any time (it's a real session). Before
  sending into a surface, glance at `read-screen` — if it shows the human is
  mid-conversation there, pause and ask before injecting.
- Use `cmux set-status` per role surface (e.g. `dev=implementing`,
  `review=blocked`) so the sidebar reflects live state.

---

## 9. Style and guardrails

- Be terse in the orchestrator's own output; the value is in coordination, not
  prose. One line per phase transition.
- Always verify artifacts on disk — don't trust an agent's "done" without
  checking the file exists and is non-trivial.
- Bound every loop (brainstorm rounds, review cycles). Never spin forever.
- Surface cost: prefer the cheap orchestrator model; only sub-agents do heavy
  work.
- When unsure whether something needs human judgment, it does. Ask.
- Read `references/orchestration.md` for the exact, copy-pasteable cmux command
  recipes before issuing cmux commands — do not improvise socket flags.
- **Always call the helper scripts** (`await_idle.sh`, `read_reply.sh`,
  `send_prompt.sh`, `layout.sh`, `spawn_role.sh`) for turn-detection, reading, and
  layout. Do NOT inline ad-hoc `for`/`while` poll loops with cmux inside them: a
  compound shell command can't be statically analyzed, so the host CLI prompts for
  permission every time. A single `bash <BR>/scripts/await_idle.sh <surface>` call is
  allowlisted and won't prompt. One cmux verb per command.

Helper scripts in `scripts/` (call them rather than re-deriving logic):
- `preflight.sh` — environment + BMAD install check
- `init_team.sh` — write default `.bmad/team.json` (incl. the `autonomy` block)
- `resolve_autonomy.sh <auto|supervised>` — resolve + persist the run's autonomy
  mode (§0.6); writes `.bmad/autonomy` (the Layer-B hook's cheap read) and
  `run-state.json autonomy.mode`, prints the resolved mode + budgets
- `layout.sh <brainstorm|design|dev>` — build a whole phase workspace (panes +
  launched agents + renamed tabs) in one call
- `spawn_role.sh <role> <engine> <cwd>` — create a single surface and launch the CLI
- `send_prompt.sh <surface> <file-or-text>` — send a prompt safely (file mode for long text)
- `await_idle.sh <surface> [timeout] [engine]` — block until turn-complete.
  Event-driven for claude (instant, via cmux agent hooks; pass the surface UUID
  so the session resolves); screen-polling for agy/unwrapped sessions.
  **exit 0**=idle, **exit 3**=agent paused on a permission prompt (answer it per
  §5, then re-await — this is what prevents multi-minute hangs while a sub-agent
  waits at its own approval prompt), **exit 4**=agent crashed/session ended
  (respawn via `cmux respawn-pane`, replay the prompt), **exit 2**=timeout
  (surface to human). Loop await→answer→await.
- `read_reply.sh <surface> [lines]` — read the latest agent reply
