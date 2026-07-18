---
name: harness-builder
description: >-
  Scaffolds project-specific harness crates/modules that drive a project
  through its natural interface, observe and instrument outputs, and
  triage against documented requirements (stories, ADRs, specs, threat
  model items) to schedule and burn down implementation gaps and defects
  in a continuous loop. All agents run through a project-scoped
  nono-sandboxed opencode server. Generates a runtime quality harness
  (`<project>-harness/`), an implementation genesis harness
  (`<project>-genesis/`), or both. Use when asked to "build a harness",
  "scaffold project genesis", "drive X and fix what breaks", "loop until
  clean", "build a closed-loop harness", "burn down bugs agentically",
  or "drive implementation until scope is exhausted".
license: MIT
metadata:
  version: 2.3.0
  author: james-hebden
allowed-tools: >-
  Read Grep Glob Bash(git*) Bash(cargo*) Bash(go*) Bash(python*)
  Bash(bundle*) Bash(nix*) Bash(rg*) Bash(jq*) Edit Write
  AskUserQuestion TaskCreate TaskUpdate Agent
compatibility: >-
  Global install assumed at ~/.claude/skills/harness-builder/. Generated
  harnesses dispatch all agents through a project-scoped `opencode serve`
  process launched as `nono run … -- opencode serve` — both `opencode`
  and `nono` must be on PATH. Python and Nix harnesses use the legacy
  `claude -p` stream-json backend (opencode-server backend is a
  follow-up for those two).
---

# Harness Builder

A builder skill: it scaffolds project-specific harness crates or modules, then exits. The generated harnesses are owned by the project, live in the repo, and evolve with the code.

Two harness shapes, usable side-by-side:

| Harness shape | What it does | Lives at |
|---|---|---|
| **Runtime quality** | Spawns the project under test, drives it through its natural interface, captures output, judges with an adversarial reviewer, loops until clean. | `<project>-harness/` |
| **Implementation genesis** | Drives the project from documentation through code through done predicate. Orchestrates iteratotron + bug-burndown via in-session agents. | `<project>-genesis/` |

## The continuous loop

Both shapes run the same fundamental cycle until scope is exhausted:

```
INSTRUMENT → DRIVE → OBSERVE → TRIAGE → SCHEDULE → BURN DOWN → repeat
```

- **INSTRUMENT** — preflight (sandbox verdict, project state snapshot, requirements load)
- **DRIVE** — exercise the project through its natural interface (HTTP endpoint, CLI subcommand, daemon startup, test suite)
- **OBSERVE** — capture structured output, logs, metrics, error signals
- **TRIAGE** — compare observed behavior against documented requirements; the LLM reviewer + structural anti-rationalization audit classify each signal as pass / reject / gap
- **SCHEDULE** — map rejects and gaps to requirement items: which story, ADR, spec, or threat-model mitigation is violated?
- **BURN DOWN** — dispatch in-session agents via the opencode server to close each item; merge, re-instrument, continue

The loop runs until the runtime harness declares clean or the implementation harness's done predicate attests. Auto-resume keeps the loop alive across restarts without losing iteration state.

## Loop termination — the global fixpoint (MANDATORY)

> **The rule:** the harness may stop **only** when iterate (implementation), the adversarial review of documented requirements/state, **and** bug burndown **all** report zero remaining work **in the same pass**. A clean signal from any single phase is necessary but never sufficient. Stopping on one phase's clean result while another phase is still making progress — or was never re-run — is the canonical early-exit defect.

Make every phase return an explicit completion signal — a two-state `PhaseOutcome { Clean, WorkRemaining }`, not a bare `Ok(())`. Then wrap the whole phase plan in an **outer fixpoint loop** that terminates only when an entire round reports `Clean` for every phase:

```rust
loop {                                   // global fixpoint, bounded by max_rounds
    let mut round_clean = true;
    for phase in &plan {                 // implementation → test → runtime
        match run_phase(phase).await? {
            PhaseOutcome::Clean => {}
            PhaseOutcome::WorkRemaining => round_clean = false,
        }
    }
    if round_clean { break; }            // ALL phases clean THIS round → done
    // else: a later phase's fixes can reopen earlier scope → run another round
}
```

Why a single pass is not enough: progress made in a later phase routinely reopens work the earlier phases already "passed". Bugfixes from the runtime phase can violate a documented requirement the implementation/adversarial phase must re-examine; new scope surfaced by iterate produces code the test/runtime phases have never exercised. So the loop runs the **full** plan again whenever **any** phase reported work, and stops only at a true fixpoint.

What counts as `WorkRemaining` (never `Clean`):
- iterate/implementation reported "further progress next iteration" or its **done predicate is unsatisfied** (any of: scope queue non-empty, bug queue non-empty, tier-1 gates red, alignment gate not `ALIGNED`)
- the adversarial review found ≥1 reject, **or could not run at all** (see the outage rule below)
- bug burndown left any finding `Queued`/`InFlight`, or a fix turn made zero tool calls
- the phase hit its `max_iterations` cap or time budget (a cap is the opposite of proof-of-completeness)
- a `--dry-run` (it did no work and proved nothing)

Bound the outer loop (`max_rounds`, derive it from `max_iterations`) so cross-phase oscillation — phase A always reopening what phase B closes — terminates as a **loud error**, never as a success.

> **Reviewer/transport outage ≠ clean.** A phase that could not obtain an adversarial verdict (e.g. `POST /session` returned HTTP 500, every prompt hit the per-prompt deadline, the JSON never parsed) has **zero information** about the corpus — which is the opposite of "found nothing wrong". Treat a total review outage as a phase **error** (→ `WorkRemaining`), never as zero rejects. Concretely: the reviewer returns `Err` when *all* of its passes failed to produce a verdict, and the loop propagates that error instead of reading an empty verdict list as `ITERATION CLEAN`. A single surviving pass is still real signal and is fine. This is the 2026-06-14 false-clean incident: both reviewer passes 500'd, the loop logged `ITERATION CLEAN — zero rejects`, and the entire flow exited with documented scope still open.

## Size the deadlines to the workload — MANDATORY tuning step

The skeleton timing constants are tuned for a fast service watchdog (an HTTP daemon that responds in milliseconds, agent turns that edit a handful of files). **A build system, an E2E application harness, or any project whose drive surface or fix turns invoke heavy work needs much larger ceilings**, or the symptom is *phases timing out mid-flight and reported as false Timeouts* — the most expensive and most misleading failure mode, because a killed-but-healthy turn looks identical to a wedge and (per the outage rule above) can stall the loop.

When scaffolding (build mode) or auditing (audit mode), **classify the workload first, then set the ceilings to clear the slowest *productive* turn** — never the typical one. The hard ceilings are anti-wedge backstops, not the normal end of work: real completion is the three-way AND, and real wedges are caught far sooner by the stall watchdog. So generous hard ceilings cost nothing on a healthy run and prevent the false-Timeout failure; only the *liveness* window (stall) should stay tight.

| Knob | Service watchdog (skeleton default) | Build system / E2E / heavy-agent (this skill's recommended) | What it bounds — size it to clear the slowest of this |
|---|---|---|---|
| `--time` global budget | 8 h (`28_800`) | **days to weeks** (`604_800` = 7 days is a sane build-system default) | a *converging* run, not a single pass — heavy builds + VM boots + multi-round burndown legitimately take days |
| per-session drive deadline (`SESSION_DEADLINE`) | ~40 min | **2–4 h** | one agent fix/burndown/genesis turn that may drive its own `nix build` / `make` / `nixos-test` / VM boot *inside* its tool calls |
| per-session stall window (`STALL_TIMEOUT`) | ~5 min | **20–30 min** | the longest a productive turn emits ONLY keepalives — i.e. blocked inside one long synchronous tool call (a multi-minute-to-hour build) |
| full test/check-graph gate | ~1 h | **4–6 h** | the entire check graph on a cold cache: closures, image builds, KVM-gated VM tests |
| single build/compile gate | ~1 h | **2–4 h** | one heavy attr / image / closure / link step |
| eval / lint / fast gate | ~10 min | **20–30 min** | large-flake eval with IFD, whole-tree static analysis |

**The contract:** never lower a ceiling to "catch hangs faster" — that is the stall window's job, and it stays tight precisely so the hard ceilings can be generous. A hard ceiling that bites a *healthy* turn is always a bug. Conversely, every gate over ~30 s **must** carry a liveness heartbeat (see the test-effectiveness and Nix gotchas) so a silent multi-hour build is never mistaken for a hang and never tempts an operator into shrinking the ceiling.

Detecting the workload in Step 2: a `flake.nix` / `Cargo.toml` with image or VM-test outputs, a `Makefile` with a multi-stage build, a project whose `client`/gate surface shells out to `nix build` / `docker build` / `bazel` / `cargo build --release` / a test suite that boots VMs — all signal the build-system envelope. Default to the right-hand column for these; default to the watchdog column only for a pure request/response service. When in doubt, ask the operator for the expected run length and the slowest single build/test step, and size from that.

## Project surface integration

The harness doesn't just watch — it drives the project through the same surface a real operator uses:

- **HTTP services** — send test requests through the API surface (REST, gRPC, tarpc, GraphQL); assert on response shapes and latency; capture structured error payloads
- **CLI tools** — invoke subcommands with realistic inputs; capture stdout/stderr and exit codes
- **Daemons and servers** — spawn the process, wait for the ready signal (socket creation, health endpoint, log line), then drive it
- **Test suites** — run the project's own Tier-1/Tier-2/Tier-3 suite; track which tests are new failures vs prior failures vs newly green

The runtime `client.rs`/`client.go` module owns surface integration. It's the most project-specific module — the scaffold is a template; filling it in is the operator's first customization step.

## Requirements as the triage target

Documented requirements are the ground truth for "bug or gap?". The harness reads them at startup and builds the triage target queue.

| Artifact | What the harness checks | Status values to load |
|---|---|---|
| Stories | Are acceptance criteria met based on observed behavior? | `Draft`, `Implemented`, `Done` |
| ADRs | Does the running system match `accepted` decisions? | `proposed`, `accepted`, `deprecated`, `superseded` |
| Specs | Do referenced files exist and exhibit the specified behavior? | File presence + behavioral check |
| Threat model | Are `Not Started` or `PARTIAL` mitigations driving regressions? | `Not Started`, `PARTIAL`, `DESIGNED`, `IMPLEMENTED` |

Rejects and gaps link to their requirement items. The SCHEDULE phase determines priority: P0 = `Not Started` security mitigations, P1 = `Draft` stories with failing acceptance criteria, P2 = everything else.

Scaffold a `requirements.rs`/`requirements.go`/`requirements.rb` loader in both harness types that reads the relevant documents and returns the queue.

## Sandbox contract

Every agent runs inside a single project-scoped `opencode serve` instance, launched once at run start under `nono run`. The boundary is set at server launch — every session, subagent, bash call, MCP server, and LSP the opencode server spawns inherits it. There's no per-session sandboxing to forget. The server runs against the operator's **real** opencode config, so all host skills and LSPs are available inside the sandbox — the boundary restricts secrets, not capability.

> **The rule:** A generated harness may auto-approve permissions if and only if `opencode serve` was launched as a child of `nono run` with the project's least-privilege policy. A bare `opencode serve` with non-interactive permissions is a bug the eval must catch.

One server per run, per project. The driver starts the server, passes the handle into `inner_loop`, and disposes it on every exit path (success, error, signal) via `defer`/`ensure`/explicit cleanup. Agents only connect; they don't own the server.

Launch the server under the dedicated **`opencode-serve` nono profile** (`nono run -p opencode-serve --allow-cwd --open-port <PORT> -- opencode serve --hostname 127.0.0.1 --port <PORT>`). The profile extends `default` and grants only what a headless opencode server touches (project cwd, `~/.config/opencode`, `~/.local/share/opencode`, `~/.cache/opencode`, plus the `nix_runtime`/`opencode_linux`/`git_config` groups). Do **not** use the Claude Code `--network-profile claude-code` flag or its device-file/cache grants — those are TUI-binary specifics, not relevant to a headless server.

> **Capability contract — the loop is pointless without it.** The sandbox keeps secrets out of reach; it must **not** keep the fix agent from working. Run the sandboxed server against the operator's **real `~/.config/opencode`** so that **all** host skills, **all** configured LSPs, and the operator's agents are available — exactly as in an interactive session. Don't point the server at a minimal isolated config and hand-pick a skill subset; that's the iter-001 failure (an isolated config with no skills made the burndown agent no-op — 0 tokens, 0 tool calls — while the loop reported success and left 133 real findings unfixed). The nono profile loosens **capability** (skills, LSPs, toolchains, plugin/cache dirs) while `default`'s `deny_*` groups and the `.env` deny keep **secrets** out — two separate axes. When a plugin or MCP server EPERMs on its cache, **grant its dir**, don't strip the config; disable only the specific offending entry, last resort. Keep `"lsp": true` and grant every configured LSP's binary dir (never blanket-disable LSP). Keep `~/.local/share/opencode` (auth + store) granted. The fix agent still needs a **tool-capable model**, chosen per provider and verified by the no-op guard — for **GitLab Duo** that is the **`duo-chat-*` tier**, defaulting to Haiku (`gitlab/duo-chat-claude-haiku-4-5`; *not* `duo-workflow-*`, which returns empty no-tool completions on the observed servers), and for **direct Anthropic** (only when specifically required — Duo is preferred) a current tool-capable Claude defaulting to `anthropic/claude-haiku-4-5`. **Never default to Opus**, and raise to Sonnet only for the rare, genuinely very complex burn where Haiku has stalled; a fix turn that makes **zero tool calls is a failure**, never a silent success; and `bug-burndown` is invoked *as a skill* (load-and-run), not a `/`-slash-command string. Full detail: `references/opencode-server-integration.md` § 4.1.

If `nono --version` fails on PATH: hard-fail by default with an install message (brew, nix, .deb). With `--allow-unsandboxed`: start the server with interactive/`ask` permissions, never blanket auto-approve. Set `OPENCODE_DISABLE_AUTOUPDATE=1` and pass `OPENCODE_SERVER_PASSWORD` via env, never argv.

Full policy, the `opencode-serve` profile JSON, preflight algorithm, per-language wiring: `references/nono-integration.md` § "opencode server boundary".
Server lifecycle, HTTP+SSE API, three-way completion detection, per-language driver skeletons: `references/opencode-server-integration.md`.

## When to Use This Skill

- "Build a test harness" / "build a watchdog for my service" / "drive X and fix what breaks" / "loop until clean"
- "Scaffold project genesis" / "build an implementation harness" / "drive implementation to scope exhaustion"
- "Burn down bugs agentically" / "triage findings against our stories/ADRs" / "burn down everything that surfaces"
- "Build a closed-loop harness" / "requirements-driven bugfix loop" / "turn requirements into a work queue"
- After invoking `/iteratotron` or `/bug-burndown` and wanting a project-local binary that re-invokes them in a loop
- When you need to instrument an HTTP API, CLI tool, or daemon and run an LLM reviewer against its output continuously
- **Auditing or upgrading an existing harness** — "is my harness up to standard?", "find harness bugs", "bring this harness up to spec", "check the harness for opencode gotchas", "the harness exited early / leaked / missed adversarial review". This is **audit mode** (see below). When a harness of the requested type already exists, the skill *defaults* to auditing it rather than blindly regenerating.

**Don't use** for one-shot reproducers (use `bugfix`), unit-test scaffolding, or metrics dashboards without LLM review.

## Two modes: build and audit

The skill operates in one of two modes, auto-detected in Step 2:

- **Build mode** — no harness of the requested type exists. Scaffold one from the skeletons (Steps 4–9).
- **Audit mode** — a harness already exists. Treat the skill's own guidance as a compliance specification, check the existing harness against **every** requirement, report a scored gap analysis, and fix the gaps in place. Use this to bring an older or hand-modified harness up to the current standard and to catch regressions: missing adversarial review, loop-logic deficiencies (early exit, no global fixpoint, reviewer-outage-as-clean), opencode gotchas (per-session `/event` connections, out-of-band session `DELETE`s that corrupt the store, missing `properties` unwrap, idle-only completion), missing no-op guards, absent auto-resume, action-audit gaps, an **over-isolated sandbox / opencode config** (a minimal `XDG_CONFIG_HOME` with a hand-picked skill subset or disabled LSPs that starves the fix agent — audit mode loosens the existing harness's nono profile and opencode config so all host skills and LSPs load while the `deny_*` secret groups stay intact), and implementation+bugfix-loop features that were never wired. **Audit mode never silently regenerates** — it diffs against the standard and patches.

Audit mode is the default when an existing harness is detected. The full checklist and procedure live in `references/audit-mode.md`.

## Quick Start — interview first, build second

```
/harness-builder [arguments]

Arguments (skip the corresponding question when supplied):
  mode:<build|audit>           # default: auto (audit if a harness exists, else build)
  type:<runtime|implementation|both|bugfix-bridge>
  orchestration:<comma-separated: iteratotron-genesis, iteratotron-sweep, bug-burndown, none>
  language:<rust|go|python|ruby|nix>

Examples:
  /harness-builder type:both orchestration:iteratotron-genesis,bug-burndown language:rust
  /harness-builder type:runtime orchestration:bug-burndown language:go
  /harness-builder mode:audit                      # audit + fix the existing harness
  /harness-builder                                 # full interview / auto-detect mode
```

Run `AskUserQuestion` for each missing argument. Three questions cover the dispatch: harness type, orchestration (multi-select — runtime typically pairs `runtime + bug-burndown`; greenfield pairs `implementation + iteratotron-genesis + bug-burndown`), and language. Full option text in `references/interview-flow.md`.

Disallowed combinations:
- `type:runtime` + `language:python|ruby|nix` → reject with clear error; re-prompt for language
- `type:both` + `language:python|ruby|nix` → accept implementation, warn runtime unavailable, reduce to implementation

A `language:nix` project (a nixpkgs derivation/PR, a flake build, an image
build, or a repackaging effort) runs as an **implementation** harness whose
drive surface is the `nix` CLI and whose checks are the flake check-graph —
not a Rust/Go runtime daemon. The genesis loop drives eval/lint/build/test,
exercises the packaged software through its real tests + E2E scenarios, and
verifies supply-chain artifacts. Full wiring:
`references/implementation-nix.md` ("Nix as the deliverable") +
`references/nix-harness-toolchain.md`.

For `language:nix`, the implementation harness *is* the Nix-driving harness:
it drives `nix` (eval, lint, build, test, E2E, supply-chain) as its natural
interface, so the "runtime" surface is folded into the implementation path.
Pick `type:implementation` for nixpkgs PRs, flake builds, image builds, and
repackaging efforts. Details: `references/implementation-nix.md`.

## Workflow

```
Progress:
- [ ] 1. Run interview (or parse arguments)
- [ ] 2. Detect project context (language manifests, existing harnesses, .git state) → set mode
- [ ] 3. Reject incompatible combinations
--- BUILD MODE (no existing harness) ---
- [ ] 4. Scaffold the runtime crate (type ∈ {runtime, both})
- [ ] 5. Scaffold the implementation crate (type ∈ {implementation, both})
- [ ] 6. Wire orchestration bridges per orchestration: choices
- [ ] 7. Generate README documenting operator usage
- [ ] 8. Smoke-test the generated harness
- [ ] 9. Commit the scaffold
--- AUDIT MODE (existing harness detected) ---
- [ ] A1. Inventory the existing harness modules + manifest
- [ ] A2. Run the compliance checklist (references/audit-mode.md) → scored gap report
- [ ] A3. Fix gaps in place, highest-severity first (loop logic, opencode gotchas, adversarial review)
- [ ] A4. Build + test + clippy/vet; add regression tests for each fixed gap
- [ ] A5. Commit each fix with a message naming the guardrail it restores
```

### Step 2 — Detect project context

```bash
test -f Cargo.toml && lang="rust"
test -f go.mod && lang="go"
test -f pyproject.toml && lang="python"
test -f Gemfile && lang="ruby"
test -f flake.nix && nix_present=true

test -d "<project>-harness" && runtime_present=true
test -d "<project>-genesis" && implementation_present=true
rg --type rust 'service trait|#\[tarpc::service\]' || rg --type go 'service.*interface'
```

**Nix as the deliverable.** When `flake.nix` (or `default.nix`/a
`pkgs/by-name` tree) is present and there's *no* other-language manifest, or
the project is itself a nixpkgs contribution / NixOS module / image build /
repackaging effort, treat the Nix as the thing under test (`lang="nix"`,
Pattern 3). The harness drives `nix` like an operator — eval, lint, build,
test, E2E the packaged software, verify supply-chain artifacts — and burns
down gaps in both the Nix and the software it ships. See
`references/implementation-nix.md` ("Nix as the deliverable") and
`references/nix-harness-toolchain.md`.

If a harness of the requested type already exists, set `mode = audit` (unless the operator passed `mode:build`). Confirm via `AskUserQuestion`: **audit + fix (recommended)** / regenerate from scratch / abort. Audit is the default because regenerating discards local fixes and loses the project-specific `client` module. Proceed to the AUDIT MODE steps (A1–A5) and `references/audit-mode.md`.

### Steps 4–5 — Scaffold crates

**Runtime** → `references/runtime-rust-skeletons.md` or `references/runtime-go-skeletons.md`. Output: `<project>-harness/` with these modules:

```
main.rs | main.go          # outer loop + CLI + preflight + opencode server lifecycle
daemon.rs | daemon.go      # spawn / SIGTERM / SIGKILL teardown
client.rs | client.go      # drive the project's natural interface ← most project-specific
log_capture.rs | log.go    # tail until idle + heartbeats
reviewer.rs | reviewer.go  # three-pass adversarial review + fingerprinting
action_audit.rs            # MANDATORY structural anti-rationalization pass
findings.rs | findings.go  # write bug-burndown session
burndown.rs | burndown.go  # /bug-burndown bridge (if orchestration includes it)
```

**Implementation** → `references/implementation-<lang>.md`. Output: `<project>-genesis/` with the orchestration modules (state, bootstrap, gap_analysis, plan, inner_loop, constitution_check, streaming, adversarial_review, harness_runner, done_predicate, slsa).

Both harness types start and dispose the opencode server in the entry point:

```rust
// Rust — both harness types
let password = std::env::var("OPENCODE_SERVER_PASSWORD")
    .unwrap_or_else(|_| uuid::Uuid::new_v4().to_string());
// cli.opencode_port defaults to 0 → launch picks a free ephemeral port (and
// passes the resolved port to nono --open-port) so multiple harnesses can run
// side by side; a non-zero flag pins a stable address.
let server = ServerHandle::launch(&project_root, cli.opencode_port, &password).await?;
let result = inner_loop::run(state, &server).await;
server.shutdown(Duration::from_secs(10)).await.ok();  // always runs
result?;
```

Full server skeleton, HTTP+SSE contracts, three-way AND completion detection, **dynamic-port allocation**, and the `properties`-envelope unwrap: `references/opencode-server-integration.md §5–6, §10`.

### Step 6 — Wire orchestration bridges

- **`iteratotron-genesis`** → `inner_loop` dispatches in-session agents running iteratotron in genesis mode against worktree-isolated scopes
- **`iteratotron-sweep`** → same, with `mode:sweep`
- **`bug-burndown`** → `burndown.rs/go` bridge dispatches agents to close rejects; implementation `inner_loop` alternates iteratotron and burndown per worktree
- **`none`** → omit bridge modules; harness produces findings but doesn't dispatch closure

Patterns: `references/orchestration-integration.md`.

### Step 7 — README

The generated README must document:
- What orchestrators are invoked, with the interactive slash-command equivalents (`/iteratotron`, `/bug-burndown`)
- Invocation: `cargo run -p <project>-harness -- --config <config>` and `cargo run -p <project>-genesis -- --parallel 2 --time 604800` (7-day budget — size `--time` to the workload per "Size the deadlines to the workload"; a heavy build/E2E run is measured in days)
- Configuration surface: flags, environment variables, work directory
- That both orchestrators remain usable interactively without the harness

### Step 8 — Smoke test

```bash
cargo run -p <project>-harness -- --config <config> --no-burndown   # runtime
cargo run -p <project>-genesis -- --dry-run                          # implementation
```

Verify: build passes, preflight passes (nono found, opencode found), daemon spawn + log capture fires (runtime). Don't run a full loop yet.

### Step 9 — Commit

```
add <project>-harness scaffold (closed-loop watchdog + burndown bridge)
add <project>-genesis scaffold (iteratotron-driven implementation orchestrator)
```

## Audit mode — bring an existing harness up to standard (Steps A1–A5)

When a harness already exists, the skill becomes a compliance auditor. The
skill's own guidance is the spec; the existing harness is the implementation;
audit mode is a three-way diff (standard ↔ harness ↔ observed behaviour) that
ends in patches, not prose.

**A1 — Inventory.** Enumerate the harness's modules and manifest. Map each to
the canonical module list (Steps 4–5). A missing module (`reviewer`,
`action_audit`, `burndown`, `done_predicate`, …) is itself a finding.

**A2 — Compliance checklist → scored gap report.** Walk every item in
`references/audit-mode.md`, grouped into seven families:
1. **Loop logic** — global fixpoint present? every phase returns
   `Clean`/`WorkRemaining` (not bare `Ok`)? outer loop bounded by `max_rounds`
   and fails loud on exhaustion? reviewer/transport outage → `WorkRemaining`,
   never "zero rejects"? no early exit on a single phase's clean signal?
2. **Adversarial review** — three-pass reviewer present (overt + silent
   divergence + structural)? `action_audit` structural pass wired? post-merge
   `bugfix` review run on the harness's own code?
 3. **opencode gotchas** — **one shared `/event` connection, not per-session**?
   **NO out-of-band `DELETE /session/:id` (it corrupts the store; reclaim via
   server dispose, §13.2)**? `properties` envelope
   unwrapped? three-way AND completion (not idle alone)? process-group kill?
   dynamic port → both `--port` and nono `--open-port`? `agent`+`model`
   determinism? **interactive `question` tool detected and auto-answered (abort
   + re-prompt with autonomous-decision guidance), and every dispatched prompt
   carries the no-questions directive** (§14)?
4. **Sandbox** — nono as direct parent? `--add-dir`/`--allow` from one source?
   real config so **all** skills + LSPs load (over-isolation / hand-picked skill
   subset is a gap)? capability loosened while `deny_*` secret groups stay
   intact? no silent `bypassPermissions` fallthrough?
5. **No-op / completion guards** — zero-tool-call turn flagged as
   `WorkRemaining`? `done_predicate` clauses complete (incl. SLSA L3 in
   genesis)? unsubstantiated-claim verification re-queues scope?
6. **Resilience** — auto-resume by default with `--no-resume`? serial outer
   loop (`parallelism == 1`)? state persisted per iteration? teardown always
   runs?
7. **Implementation + bugfix loop completeness** — iteratotron/burndown bridges
   wired for the declared `orchestration:`? gap analysis → plan → inner loop →
   verification → done predicate all present? findings written in the burndown
   schema?

   Score each item PASS / GAP / N/A with a one-line evidence pointer
   (`file:line`). Emit a summary table sorted by severity.

**A3 — Fix in place, highest-severity first.** Loop-logic and opencode-gotcha
gaps outrank style. Patch the existing modules; preserve the project-specific
`client` module and any local customisation. Re-use the skeletons in
`references/` as the source of truth for the corrected code.

**A4 — Verify.** Build, run the test suite, run clippy/vet. **Add a regression
test for every fixed gap** (e.g. "N observers open one `/event` connection",
"reviewer outage returns Err not empty verdicts", "session deleted after
observe"). A fix without a test is a re-regression waiting to happen.

**A5 — Commit per fix.** One commit per restored guardrail, the message naming
the guardrail and incident (e.g. `harness: single shared /event reader (fixes
MaxListeners leak)`). Then run the post-merge `bugfix` review (Caveats).

Full per-item checklist, evidence patterns, and the scored-report template:
`references/audit-mode.md`.

## Auto-resume — MANDATORY for both harness types

The generated harness **must auto-resume by default** from the most recent prior iteration/session, with `--no-resume` to opt out. Resume is not a nice-to-have: an interrupted run that re-gathers logs from scratch wastes the most expensive part of the loop (driving the application) and, worse, throws away forensic logs that the review/burndown phase never got to consume.

| Harness | Resume target | Override |
|---|---|---|
| Runtime | Most recent `<work_dir>/iter-NNN/` — see the resume-state rule below | `--no-resume` |
| Implementation | Most recent `.iteratotron/<session-id>/state.json` | `--no-resume` |

Rules:
- Default is resume. Explicit `--resume-iter`/`--resume <id>` wins over both auto-detect and `--no-resume`.
- Pick the *most recent* candidate by directory/mtime order.
- The iteration counter continues from the resumed number — never restart at 1.
- Log the auto-resume decision at startup so the operator can see what was picked, which phase it resumes into, and how to override.

### Resume *into* the most recent incomplete iteration — reuse its logs

The single most important runtime-resume rule: **an iteration that has already gathered application logs but has not yet been reviewed/burned-down is the correct resume target, and the harness must reuse those logs instead of re-running the application.** Re-driving the app to re-collect identical logs is wasted work and can mask the very divergence the interrupted run captured.

An `iter-NNN/` directory is in one of three states; classify it by which artifacts are present, then act:

| State | Artifacts present | Resume action |
|---|---|---|
| **logs-gathered, unreviewed** | daemon/app log(s) present, **no** review/burndown verdict artifact | **Resume here.** Skip the daemon spawn + log collection entirely; feed the *existing* logs straight into the reviewer → action-audit → burndown phases. |
| **complete** | logs **and** a verdict/burndown artifact | Already done — start the *next* iteration (rebuild → fresh logs). |
| **empty / partial** | directory exists but no usable daemon log (daemon never logged) | Genuinely nothing to review — skip it and fall back to the next-most-recent candidate or a fresh iteration. |

So "incomplete" is not uniformly "skip". An iteration whose logs landed but whose review never ran is exactly what resume exists for. Only a *log-less* directory is skipped.

**The phase sequencing this implies:**
1. **Resumed (interrupted) iteration** — `phase = review`. Do **not** rebuild, do **not** respawn the daemon, do **not** call `collect_until_idle`. Load the logs already on disk and run reviewer + structural action-audit + burndown against them. This finishes the work the crash interrupted.
2. **Every subsequent iteration** — `phase = gather`. Rebuild the application (the fix from the previous burndown changed the code), respawn the daemon, drive it, and `collect_until_idle` into a *new* `iter-(NNN+1)/` directory, then review the fresh logs.

Reusing stale logs for more than the single resumed iteration would review code that no longer exists; that's why only the resumed iteration reuses logs and the next one always re-gathers after the rebuild.

```rust
enum ResumePhase {
    /// Resume into iter-NNN: logs are on disk, review/burndown never ran.
    /// Reuse the existing logs; skip rebuild + daemon spawn + collection.
    ReviewExisting { iter_dir: PathBuf, iteration: u32 },
    /// Start fresh at iteration N: rebuild, spawn, drive, gather new logs.
    GatherFresh { iteration: u32 },
}

async fn resolve_resume(work_dir: &Path, cli: &Cli) -> ResumePhase {
    if cli.no_resume {
        info!("--no-resume: fresh iteration");
        return ResumePhase::GatherFresh { iteration: 1 };
    }
    let target = match &cli.resume_iter {
        Some(p) => Some(p.clone()),
        None => latest_iter_dir(work_dir).await, // most recent iter-NNN by number
    };
    match target {
        Some(dir) if has_logs(&dir) && !has_verdict(&dir) => {
            // logs-gathered, unreviewed → THE resume case
            let n = iter_number(&dir);
            info!(from = %dir.display(), iteration = n,
                  "auto-resume: reviewing existing logs from interrupted iteration (no re-run)");
            ResumePhase::ReviewExisting { iter_dir: dir, iteration: n }
        }
        Some(dir) if has_verdict(&dir) => {
            let n = iter_number(&dir) + 1;
            info!(from = %dir.display(), next = n,
                  "auto-resume: prior iteration complete; starting fresh gather");
            ResumePhase::GatherFresh { iteration: n }
        }
        Some(dir) => { // exists but log-less: nothing to review
            warn!(from = %dir.display(), "auto-resume: candidate has no logs; falling through");
            ResumePhase::GatherFresh { iteration: iter_number(&dir) }
        }
        None => { info!("no prior iter found; fresh"); ResumePhase::GatherFresh { iteration: 1 } }
    }
}
```

`has_logs` checks for a non-empty daemon/app log (the artifact `collect_until_idle` writes); `has_verdict` checks for the review/burndown completion artifact (e.g. `burndown.log`, a verdicts JSON, or a `reviewed` marker) written only after the review phase finishes. Define both against your own iteration layout and keep them in one place — the same predicate that *decides* resume must be the one the review phase uses to *write* completion, or the two drift and resume loops forever.

**Reference implementation:** noelle-harness — `<work_dir>/.harness/iter-NNN/` holds `noelled.log` + `cargo.log` (gathered) and gains `burndown.log` only once reviewed. On restart it auto-resumes into the latest iter whose `burndown.log` is absent but whose `noelled.log` is present, runs the review/burndown against those logs, and only then rebuilds and gathers fresh logs for `iter-(NNN+1)`. The implementation-harness equivalent lives in `state::resolve_session` / `latest_session_state` (most-recent `state.json` by mtime, reconciled with `docs/` on load).

Don't merge `--no-resume` and `--resume-iter` — they mean different things. Don't auto-resume into a genuinely log-less directory (nothing to review). Don't reuse logs for more than the one resumed iteration — every iteration after the rebuild must gather fresh logs.

## Structural anti-rationalization pass — MANDATORY for runtime harnesses

The LLM reviewer isn't enough. Adversarial log wording defeats every prompt-based rubric tested, including ones that explicitly list euphemisms. The fix is a deterministic, language-immune pass that merges verdicts into the same reject set.

For each operation token (`action=X`, `task_kind=X`, `job=X`):
- `hard_failures` = count of lines matching the project's hard-failure marker list (WARN+, "Failed to", `kind="*_error"`, "deferred to designed error path")
- `hard_successes` = lines matching hard-upstream-success markers that carry **no** fallback marker ("cache-fallback", "seed-fallback", "designed fallback")
- If `hard_failures > 0 AND hard_successes == 0` → emit synthetic `Verdict(kind=cascade-failure, severity=critical)` into the reject set
- If `hard_failures == 0` → no verdict; operations with no failure signal pass silently

The canonical KEV incident (noelle iter-001..007, 2026-05-27): seven iterations accepted zero upstream fetches because "served from cached entries — designed cache-fallback live-query succeeded" satisfied the LLM rubric. A success marker next to a fallback marker is evidence of failure. The audit makes that impossible regardless of log wording.

> **Scan the failure CAUSE wherever it lives — msg AND structured error attrs — and count a failing lifecycle line itself.** The marker/token scan that reads only the log **message** has a silent hole: a unit/operation that **fails fast** emits only its terminal lifecycle line (`scenario failed` / `task failed` / `job aborted`) with the actionable cause in a **structured `error` attr**, not in the message, and no bulk `"failed to …"` message lines. Scanning only `msg` records **zero** hard failures for that unit → **no verdict** → the operation that failed *every iteration* is silently accepted. This is the 2026-06-18 wiz-evaluation gap: the wiz provider failed at creation with an OAuth `401` carried in `attrs.error`; the structural audit missed it for ~27 iterations and only caught it once an incidental message-level `"failed to query …"` line happened to appear (a DNS-era failure). Other providers escaped the hole only because their hundreds of message-level `"failed to ingest…"` lines tripped the marker independently. Two fixes, both required: (1) a **failing terminal lifecycle line is itself a hard failure** for the in-flight operation, independent of any message-level markers — the runner emits it only when the unit's run returned an error; (2) the failure **exemplar** must render the `error` attr (handle **both** a string and a **structured array/object**, e.g. a GraphQL error array) so the burndown agent sees the cause, not a bare "scenario failed". Keep the gate unchanged (`hard_failures>0 AND hard_successes==0`) so a unit that recorded a genuine non-fallback success before failing is still suppressed. Add tests: a fast-fail unit whose cause is **only** in `attrs.error` (string and structured-array forms) emits a reject; a passing unit is not flagged; a failed-but-genuine-success unit is not flagged.

### Whole-log correlation pass — non-error divergence the per-operation tally and the LLM both miss

The per-operation failure tally above catches *failure-shaped* divergence within one operation. It does **not** catch the class where **every individual line is a benign INFO** and the divergence only exists in the **relationship between lines spread across the whole run** — an inefficiency/correctness smell, not an error. The LLM reviewer can't see it either: it works on batched, deduplicated templates with no cross-batch memory, so a back-and-forth that spans batches is invisible to it. This needs a **second structural pass with whole-log scope**: correlate a key across the entire record set and flag a key whose state **oscillates** (revisits a value it already left) rather than converging.

The canonical instance (vulnmapper, 2026-06-17): advisories migrating between a CVE and a vendor alias repeatedly within one run — `migrated advisory from CVE to RHSA ID` … later `migrated advisory` (back toward the CVE) … later `migrated advisory from CVE to RHSA ID` again. Each line is a normal INFO. Held against the whole log, the same CVE's identity is bouncing A→B→A→B: two ingest paths disagree on the canonical id, so each pass undoes the other's migration — wasted row rewrites **and** a non-converging identity (a correctness bug). The pass:

- pick a correlation key from the structured attrs (here the `cve` attr) and a state value (the alias it migrated *to*, with a sentinel like `"CVE"` for migrations back toward the bare identity);
- for each key, build the **ordered sequence** of states across the whole run, collapsing consecutive duplicates (an idempotent re-emit is not a revisit);
- if a state **reappears after the key had moved away from it** (`A→B→A`), that's an oscillation → emit a synthetic `Verdict(kind=silent-divergence, severity=high)` with a **per-key stable fingerprint** so the burndown queue dedups it;
- one-way convergence (`A→B`, never back) is normal and is **never** flagged.

Feed the verdict's `reason` the **full state sequence** and an explicit instruction to inspect the **whole log** for the competing sites — the single exemplar line is not enough to fix a whole-log finding. The burndown bridge prompt must, for these whole-log findings, point the fix agent at the **complete iteration log** (not just the exemplar) and ask for a **structural, idempotent** fix plus a **re-ingest-twice regression test** asserting the state is stable.

Also teach the LLM silent-divergence rubric the within-batch shadow of this signal: a migration/identity-change template with a **high `[seen Nx]` count** is the same advisory being re-migrated and should be rejected even though the structural pass owns the cross-batch correlation (belt and suspenders — the structural pass can miss a provider whose line omits the correlation attr).

**Required unit tests** (the per-operation pass — four minimum, by name):
1. `failure_only_run_emits_synthetic_reject`
2. `cache_fallback_success_does_not_clear_failure`
3. `genuine_upstream_success_clears_failure`
4. `non_action_lines_ignored`

**Required unit tests** (the whole-log oscillation pass — by name):
5. `oscillation_back_and_forth_is_flagged` — `A→B→A` revisit emits a high silent-divergence reject
6. `one_way_convergence_is_not_flagged` — `A→B` (never back) is silent
7. `duplicate_snapshots_do_not_count_as_oscillation` — consecutive identical re-emits collapse
8. `distinct_keys_not_conflated` and `correlation_key_absent_is_ignored` — independence + graceful skip when the key attr is missing

Wire between LLM passes and burndown bridge:

```rust
let mut verdicts = reviewer::review(...).await?;
let mut audit_verdicts = action_audit::audit(&lines);
verdicts.append(&mut audit_verdicts);
let rejects: Vec<_> = verdicts.iter().filter(|v| v.is_reject()).collect();
```

Canonical implementation: `noelle-harness/src/action_audit.rs`. Three marker lists (failures, successes, fallbacks) are project-specific starters — document how to extend each in the generated code.

## Hard Anti-Patterns

- **Don't pipe daemon output to `/dev/null`.** No socket? That log is your only forensic record.
- **Don't hardcode `/tmp/<name>.sock`.** Project-local sockets work; `/tmp` is bind-mounted differently in sandboxes.
- **Don't run `cargo run`/`go run` inside the daemon spawn.** Pre-build first; spawn execs the binary. Build output needs to be visible.
- **Don't start the opencode server without `nono run` as its direct parent.** No nono = no bypass = loop stalls on permission prompts. Preflight must abort with an install message if nono is missing and `--allow-unsandboxed` isn't set. Never silently fall through to `bypassPermissions`.
- **Don't let `--add-dir` and nono `--allow` lists drift.** Both come from one source variable in `wrap_with_nono`; separate lists is the bug.
- **Don't let `POST /session` 500 stall the loop on a missing grant.** Session create touches three things the nono profile misses; grant all three in `DefaultAllowDirs` or the reviewer/burndown can never get a session: (1) the **`~/.opencode` install dir** (read of `package.json`), (2) **`models.dev`** egress (model-catalog fetch; 403 → models don't resolve), (3) **config symlink targets** — resolve `skills`/`commands`/`agents`/`plugins`/`themes` under `~/.config/opencode` and grant any target outside it (a symlinked `skills` dir is the usual culprit; without it bug-burndown/bugfix EACCES and the fix agent no-ops). And **`CreateSession` must capture the response body** on a `>= 300` status — a bare "status 500" is undebuggable; the body names the EACCES/403. This is the 2026-06-15 session-create incident. See "nono integration" § "session-create 500 / EACCES".
- **Don't let the freshness gate relaunch-loop.** A self-freshness gate must suppress the `binaryStale` signal when running under `go run`/`cargo run` (the build cache stamps the artefact older than compiled-in source → false positive → re-exec serves the same cached binary → infinite relaunch), and on a failed relaunch must log-and-continue with the current binary, never propagate an error that aborts the loop and lets the outer wrapper restart-and-retrigger. This is the 2026-06-15 relaunch-loop incident. See "Gotchas" § "The freshness relaunch loop".
- **Don't give the opencode server client a bare `&http.Client{}` / no-timeout `reqwest::Client`.** It hangs the whole harness right after `opencode server listening` (never reaching `healthy`) because (1) the client has no per-request bound and `waitHealthy` only checks its budget *between* probes, so one probe stuck inside the not-yet-ready nono proxy blocks forever; and (2) `&http.Client{}` uses `http.DefaultTransport`, which a runtime harness has often globally replaced with a transport guard (a dry-run guard over the project's API host) — routing opencode loopback through the guard, and making any `http.DefaultTransport.(*http.Transport)` "fix" **panic** at launch. Build a **fresh** `*http.Transport` (never clone/assert the global default) with `ResponseHeaderTimeout` set — **not** a client-level `Timeout`, which would sever the long-lived `/event` SSE body — and wrap each `waitHealthy` probe in its own short context. reqwest: `connect_timeout` + `read_timeout`, never a blanket `.timeout(...)`. Use the same constructor in the test handle. This is the 2026-06-16 health-probe-hang incident. See "opencode server integration" §6.1 and "Gotchas" § "The no-timeout HTTP client hangs forever after 'opencode server listening'".
- **Don't pre-filter on severity alone.** The most damaging bugs surface as INFO/DEBUG silent divergence. Run the second LLM pass with a silent-divergence rubric.
- **Don't scan only the log message for failure — the cause often lives in a structured `error` attr, and a failing lifecycle line is itself a failure.** A unit that fails fast (provider creation, auth, DNS) emits only its terminal lifecycle line (`scenario failed`/`task aborted`) with the cause in `attrs.error`, not in the message, and no bulk `"failed to …"` message lines. A structural audit that scans only `msg` records zero hard failures for it → no verdict → an operation that failed *every iteration* is silently accepted (the 2026-06-18 wiz gap: OAuth 401 in `attrs.error`, missed for ~27 iterations). Count the **failing terminal lifecycle line itself** as a hard failure, and render the failure **exemplar from `attrs.error`** (handle both a string and a structured array/object). Keep the `hard_failures>0 AND hard_successes==0` gate so a unit with a genuine prior success is still suppressed. See "Structural anti-rationalization pass — Scan the failure CAUSE wherever it lives".
- **Don't judge divergence only line-by-line — some lives in the relationship between lines across the whole run.** A class of bug is invisible to both the per-operation failure tally (every line is a benign INFO) and the LLM reviewer (batched, no cross-batch memory): a key whose state **oscillates** across the run — the canonical case being an advisory's identity migrating CVE→vendor-alias→CVE→alias repeatedly because two ingest paths disagree on the canonical id (wasted re-writes + a non-converging identity). Add a **whole-log correlation pass** that builds each key's ordered state sequence and flags a revisit (`A→B→A`) as a HIGH `silent-divergence`, with a per-key stable fingerprint and a `reason` that hands the burndown agent the **full sequence** and tells it to read the **complete iteration log** for the competing sites and fix it **structurally + idempotently** (re-ingest-twice regression test). One-way convergence (`A→B`) is never flagged. Also teach the LLM silent-divergence rubric to reject a migration/identity template with a high `[seen Nx]` count. This is the 2026-06-17 alias-oscillation incident. See "Structural anti-rationalization pass — Whole-log correlation pass".
- **Don't run a long test-effectiveness tool through a bare blocking call.** Mutation (`gremlins`/`cargo mutants`/`mutmut`) and full-suite coverage take 20–60 min with zero output; a single `cmd.Output()`/`cmd.Run()`/`subprocess.run` makes the phase go silent for the whole run — indistinguishable from a hang. Wrap every >30s tool in a liveness heartbeat (~30s `tool still running — phase alive` + a `tool finished` line) that stops on every return path and propagates the call's result unchanged. Mirror the agent-drive heartbeat; don't reinvent. This is the 2026-06-16 test-effectiveness-hang incident. See "Test-effectiveness baseline" § "Liveness".
 - **Don't log a tool call without its distinguishing parameters — in ANY phase.** Every deduped tool-use part gets one INFO line carrying the tool name **and a per-tool detail summary**, not just the tool name and not a generic first-string-field fallback. Codebase-mutating calls must be the *most* detailed in the stream: `edit` logs the `filePath` **plus** the change shape (`replaceAll` and/or an oldString→newString preview), `write` logs the `filePath` **plus** content size, `bash` logs the **full command** (+ `description`); read/grep/glob/skill/webfetch/task/todowrite each log their meaningful params; an unknown tool logs its full `k=v` field set. The reviewer/audit phase reconstructs *what the agent did to the project* from this stream, so the bar holds identically in the reviewer, genesis/iteratotron, done-gate, and burndown drives — a bare `agent tool call tool=edit` (no file/change) or `tool=bash` (no command) is the canonical observability defect. The heartbeat's `last_tool` carries the same detail. Defer the log until the input is present, once per part id, never silently dropped; single-line collapse + ~160-char truncation per value. Unit-test one tool family per row of the §4.1 table. See "opencode server integration" §4.1 "Observability".
 - **Don't double-log tool calls across routers.** When dispatch goes through the shared drive loop that already logs each tool call (with full per-tool detail) at INFO, the per-bridge router (`routeBurndownEvent`/`routeGenesisEvent`) must not re-log it — especially not a less-informative copy missing the detail. Keep the bridge router minimal; its distinct value is the verbatim event dump to the per-session forensic file. This is the 2026-06-16 genesis-double-log gap.
- **Don't treat `Unknown model ID … MODEL_MAPPINGS` as a bad-model-choice.** It's a server-side GitLab AI-Gateway rejection, almost always opencode version-skew: the harness launches an older pinned opencode (a devshell `pkgs.opencode` from a stale nixpkgs rev) whose gateway map lags the `opencode models` catalog. Upgrade the opencode the harness launches; don't downgrade the model. Confirm by probing the id against the actual server build. This is the 2026-06-16 version-skew incident. See "opencode server integration" §4.1.
- **Don't stop on one phase's clean signal.** Termination is a *conjunction* across iterate + adversarial review + bug burndown, evaluated as a global fixpoint over the whole phase plan — not three independent per-phase exits. A clean (or worse, falsely-clean) bug-burndown round must not end the flow while iterate reported "more next iteration" and the adversarial done-predicate review never re-ran. Each phase returns `Clean`/`WorkRemaining`; the outer loop repeats the full plan until every phase is `Clean` in the same round. See "Loop termination — the global fixpoint".
- **Don't read a reviewer/transport outage as zero rejects.** Zero verdicts because the reviewer *ran and found nothing* is `Clean`; zero verdicts because the reviewer *never ran* (HTTP 500 on session create, every prompt hit the deadline, unparseable JSON across all candidates) is **no information** and must surface as a phase error → `WorkRemaining`. An iteration the reviewer never judged can never end the loop. Fail loud only when *all* passes failed; one surviving pass is still real signal.
- **Don't let a flakey `session.error` kill the drive — but retry transient errors ONLY.** The opencode gateway/store is flakey; a `session.error` can fire mid-drive after real progress (the 2026-06-16 burndown incident: 8 productive tool calls, then a server error killed the iteration). The driver must absorb a *transient* hiccup (5xx/gateway, timeouts, connection resets, rate limits) with a **bounded** retry (capped attempts, backoff, **recreating a fresh session each attempt** — but never `DELETE`-ing the old one, §13.2) — and **fail fast** on a *deterministic* rejection (`Unknown model ID`/`MODEL_MAPPINGS` skew, `BadRequest`, `EACCES`, auth, **and the SQLite store errors `Failed to execute statement`/`FOREIGN KEY constraint failed`/`UnknownError` — a corrupt store fails every later session too, so retrying just burns budget; dispose the server instead**), defaulting an unrecognized error to deterministic. Two failure modes are both bugs: no retry (one hiccup throws away an expensive drive) and blind retry of everything (deterministic config bugs get masked as "flakiness" and burn budget). Deterministic markers take precedence over transient ones; a timeout/abort stays `completed:false` (NOT retried); an *exhausted* transient retry is still an error → `WorkRemaining`, never zero-rejects/clean; and the retry lives in the driver (`prompt_and_drive`), not per-caller. Always render `session.error` legibly (name + message + raw JSON, never `null`/empty) and preserve the partial reply. See "opencode server integration" §15.
- **Don't loop `parallelism > 1` on the outer runtime loop.** Inner burndown can fan out; the outer daemon loop must be serial. Two daemons fighting over the same DB break everything.
- **Don't declare a session complete on `session.idle` alone.** Idle can fire early. Require the three-way AND: `message.updated` with `info.time.completed` set AND `session.idle` AND `GET /session/:id/todo` returns empty.
- **Don't hardcode the SSE event vocabulary — it drifts across opencode builds.** The event `type` *values* change release-to-release, and a driver keyed on an older build's names classifies the new ones as `Other`, advances nothing, never closes the three-way AND, and rides every session to its deadline as a false Timeout — the reviewer-outage false-clean, slower. The fingerprint: `tool_calls` frozen at a round number and `idle_secs`/`progress_idle_secs` **pinned at a small constant** (the ~30s `server.heartbeat` keepalive resetting the activity clock) for the whole run. opencode **1.16.x** routes turn lifecycle through a **`session.next.*`** family (`tool.called`, `step.failed`, `text.delta`, …) and makes questions/permissions **first-class events** (`question.asked`/`question.v2.asked`, `permission.asked`/`permission.v2.asked` — `permission.updated` does **not** exist). Validate the classifier against the running server's `/doc` Event union for your pinned version; handle **both** tool vocabularies (`session.next.tool.called` and `message.part.updated` tool parts, the GitLab Duo shape) **deduped by `callID`/part id** so N re-emitted snapshots count once (not the inflated 600); treat `session.next.step.failed` as a turn-end error. Add two safety nets so the next drift is loud not silent: a **liveness stall watchdog** (reset on any turn-attributable frame, with only `server.heartbeat`/`server.connected` inert — see the next anti-pattern) that aborts in ~5 min instead of the 40-min deadline, and **unhandled-event-kind tracking + a per-session forensic frame log** that names the dropped kinds. This is the 2026-06-16 `session.next.*` incident. See "opencode server integration" §16.
- **Don't key the stall watchdog on "real work" — key it on LIVENESS, with the keepalive as the only inert frame.** The stall watchdog must reset its clock on **every turn-attributable frame** (new tool call, answer text, a *re-emitted* tool snapshot, a reasoning delta, `session.status`/`diff`/`updated`, `todo.updated`, any `session.next.*`) and treat **only** `server.heartbeat`/`server.connected` as inert — an `is_inert_kind` **denylist**, never an allowlist of "progress" kinds. Resetting only on new-tool-call/answer-text/completion aborts a genuinely busy agent: a long single tool call re-emits `message.part.updated` under the same `callID` (deduped → counted once → no "progress"), and reasoning/status/diff/todo frames classify `Other` — so a working agent (118 tool calls, 271 `message.part.updated`, 184 `session.status` in the window) reads as stalled and is killed at the 5-min mark. **Liveness ≠ progress:** the dedup that keeps `tool_calls` honest must NOT gate the stall clock — reset on the frame's *arrival* (kind not inert) and advance `tool_calls` only on a fresh id, as two independent decisions. A denylist also means a future opencode build's new progress events count as liveness by default, so a vocabulary drift can't silently resurrect the false-stall. This is the 2026-06-16 false-stall incident. See "opencode server integration" §16.3.
- **Don't open a `/event` SSE connection per session.** opencode does **not** multiplex `/event`: every connection registers its own listener on the server's internal event Bus, and Node logs `MaxListenersExceededWarning: Possible EventTarget memory leak detected. N event listeners added to [MY]` once ~11 accumulate. A harness that calls a per-session `run_event_loop` (one fresh `GET /event` per scope / batch / review / burndown / done-gate) leaks one server-side listener per session for the life of the run. Hold **exactly one** long-lived `/event` connection per server and fan every frame out to per-session observers over an in-process broadcast channel (Rust `tokio::sync::broadcast`, Go a `chan` + slice of subscribers). Observers subscribe in-process and drop their receiver when done; no server-side listener is ever created per session. This is the 2026-06-15 MaxListeners incident. See "opencode server integration" §13.
 - **Don't let an agent stall on the interactive `question` tool.** A dispatched agent that calls `question` / `AskUserQuestion` in an autonomous session blocks the turn on a human answer that never comes — the session never completes, never goes idle, and the whole drive rides to its deadline as a **false Timeout**. Two halves, both required: (1) prepend a standing "this is autonomous, do NOT call the question tool, decide for yourself" directive to **every** dispatched prompt (genesis, burndown, review); (2) classify the question tool-use part as its own `EventSignal::QuestionAsked` (case-insensitive, matching `question`/`AskUserQuestion`) and, on detection, **abort the blocked turn and re-prompt the same session/agent/tier with autonomous-decision guidance** — pick the option best meeting the documented intent (for a bug, the shape of the bug) weighing complexity against intent, or, if the choice is genuinely load-bearing, take the most reversible option and record the open decision in a note for later human review. Dedupe by part id and cap injections per session (≈3) so an agent that keeps asking is escalated, not spun. This is the 2026-06-15 question-stall incident. See "opencode server integration" §14. **Two refinements the cold review of this very fix exposed (2026-06-16):** (a) **drain the aborted turn's buffered settle frames *before* re-arming the completion atomics, and gate the next break on a fresh-output flag** — the abort makes the old turn emit its own `idle`/`completed`, and re-arming bare atomics lets that death-rattle break the loop as a false `Complete`; (b) **do NOT count the question as a tool call** — a question is the canonical no-op, and inserting it into `tool_parts` launders a question-only turn past the no-op guard as `Complete{tool_calls>0}`. Track questions in their own counter only. **Build-vocabulary note (2026-06-16):** on opencode **1.16.x** the question is a **first-class `question.asked`/`question.v2.asked` event** (not a tool-use part named `question`), answered by `POST /api/session/:id/question/request/:rid/reject` with the autonomous-decision message — which unblocks the turn server-side so it runs on to normal completion, retiring the abort + drain/re-arm dance entirely. Detect the event the *running build* emits (validate against `/doc`); the abort/re-prompt path above is the older-build fallback. See §16.
 - **Don't drive the project's test surface with a blanket `--workspace` / `./...` run.** Respect the project's own build/test guidance (`CLAUDE.md`, CI config). Build once incrementally, then **scope the test step to the crates/targets that changed** (git-derived changed set → `cargo test -p <crate>`), skip it on a clean tree, and degrade to the full run only when git is unavailable or a path won't map. A hardcoded `--workspace` both blows the project's documented per-crate resource envelope and produces the silent multi-minute phase that reads as a hang. This is the 2026-06-16 verification-surface incident. See "Gotchas" § "The verification surface must respect the project's own test scoping".
 - **Don't let a reviewer pass be defined but never wired.** A fully-implemented pass (hollow-completion / test-effectiveness pass-3, snapshot-drift audit) with **zero production call sites** is dead code — the three-pass requirement is unmet even though the source looks complete. `grep` for each pass's call site in `burn_down`; "the function exists" is not PASS. Wire every pass into the reject set (degrade safe: no scan tool → empty payload → zero verdicts). This is the 2026-06-16 dead-pass finding.
 - **Don't scope a change-based audit to the whole dirty worktree.** Any structural audit that reasons about "what the fix turn changed" (snapshot-drift, churn gating) must use the **set difference** between a pre-dispatch dirty snapshot and the post-dispatch dirty set — not `git diff HEAD` alone. Otherwise a `.snap` left dirty by an earlier phase/round/operator is attributed to this turn → a deterministic false reject that, with the always-WorkRemaining burndown rule, wedges the loop to `max_rounds`. This is the 2026-06-16 HIGH-3 finding.
 - **Don't let an unfixable reject spin to `max_rounds` silently.** Track the burndown reject **fingerprint set** across rounds (order-independent hash + recurrence counter, reset on a clean round); after ~3 byte-identical rounds, surface a **loud escalation** naming the stuck fingerprints and pointing at human review. A deterministic reject the agent can't close (coverage cliff, structural audit on immovable state) otherwise re-dispatches the same fix forever and exits NOT-done with no explanation. This is the 2026-06-16 anti-stall finding (HIGH-4).
- **Don't delete opencode sessions out-of-band — reclaim the store by disposing the server.** (This *reverses* earlier guidance that told you to `DELETE /session/:id` per session; that mandate was the bug.) The session store is the server's private durable state. Turns are dispatched with `prompt_async`, so the server keeps writing a session's `message`/`part` rows in the background after the 204; deleting the parent `session` row mid-write — or on a non-clean `observe_session` exit (deadline, error bail, question budget) while the turn is still running — makes the server's cleanup INSERT fail with `FOREIGN KEY constraint failed`, and once the SQLite store hits that it poisons inserts for *every other* session too, wedging the whole run (the run then spins or hangs at 100% CPU). The earlier "Failed to execute statement" symptom was the *same* self-inflicted corruption, misdiagnosed as capacity growth. So: never add a `delete_session` to the driver; hold one server per run and reclaim the store via `POST /instance/dispose` at shutdown (already done). If a very long run needs mid-run reclamation, dispose + relaunch the server between rounds with auto-resume carrying state — never delete a live session. A `delete_session` call site is an audit finding to REMOVE. This is the 2026-06-16 FK-corruption incident. See "opencode server integration" §13.2.
- **Don't claim done without SLSA L3 attestation** (implementation genesis only). Done predicate clause 8 is non-optional in genesis mode.
- **Don't re-run the application on resume when logs were already gathered.** The most recent *incomplete* iteration — logs on disk, review/burndown never ran — is the resume target, and the harness must **reuse those logs** (skip rebuild + daemon spawn + collection) and run only the review/audit/burndown phases against them. Re-driving the app re-collects identical logs and throws away the forensic record the interrupted run captured. Only the *next* iteration rebuilds and gathers fresh logs. A genuinely log-less directory is the only "incomplete" state you skip. See "Auto-resume — Resume *into* the most recent incomplete iteration".
- **Don't ship without a post-merge `bugfix`-skill review.** Cold-context review of the harness's own code found seven defects across four follow-up commits on the canonical implementation.

## Running in opencode

The interview uses the `question` tool (maps from `AskUserQuestion`). Task tracking uses `todowrite`/`todoread` (maps from `TaskCreate`/`TaskUpdate`). Generated harnesses dispatch agents via `opencode serve` — already the native backend. Full mapping: [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## Writing Style

Apply `natural-writing-style` to the generated README and any operator-facing docs. The README must state what orchestrators are invoked, document the configuration surface (flags, env vars, work directory), and not claim the harness "fixes bugs" or "produces a production-ready system".

## References

**Sandbox and safety:**
- [nono integration](references/nono-integration.md) — sandbox contract, preflight algorithm, `wrap_with_nono` helper, per-language toolchain `--read` dirs, platform degradation, install instructions
- [opencode server integration](references/opencode-server-integration.md) — lifecycle state machine, HTTP+SSE API, three-way AND completion detection, per-language driver skeletons (Rust/Go/Ruby), eval assertions, **§13 session & event-stream lifecycle (shared `/event` reader; NEVER delete live sessions — reclaim via server dispose)**, **§14 interactive `question`-tool detection + autonomous auto-answer**
- [audit mode](references/audit-mode.md) — compliance checklist and scored-report procedure for bringing an existing harness up to standard and finding harness bugs / opencode gotchas / loop-logic deficiencies

**Runtime harness:**
- [Rust skeletons](references/runtime-rust-skeletons.md) — full code for all eight modules, three-pass reviewer
- [Go skeletons](references/runtime-go-skeletons.md) — Go variant, goroutine patterns
- [Reviewer rubric](references/runtime-reviewer-rubric.md) — three-pass rubric, fingerprinting, model assignment table
- [Gotchas](references/runtime-gotchas.md) — every debug cycle paid on the canonical implementation
- [Test-effectiveness baseline](references/runtime-test-effectiveness-baseline.md) — `.test-effectiveness/` schema, Pass 3 template
- [Orchestration integration](references/orchestration-integration.md) — iteratotron and bug-burndown invocation patterns, prompt templates, result protocol

**Implementation harness:**
- [Rust](references/implementation-rust.md), [Go](references/implementation-go.md), [Python](references/implementation-python.md), [Ruby](references/implementation-ruby.md), [Nix](references/implementation-nix.md)
- [Nix harness toolchain](references/nix-harness-toolchain.md) — `nix --json` driver wrappers, the lint/build/test/E2E/supply-chain ladder, the adversarial-review checklist (IFD, impurity, missing tests, FOD hashes, module regressions, reproducibility), and why not to embed tvix yet. Used when the Nix itself is the deliverable (nixpkgs, flake/image builds, repackaging).

## Companion skills

- **`iteratotron`** — lifecycle orchestrator; harnesses dispatch it as in-session agents, operators invoke it as `/iteratotron`. Not modified by harness-builder.
- **`bug-burndown`** — finding-closure driver; harnesses dispatch it as in-session agents, operators invoke it as `/bug-burndown`. Not modified.
- **`iterate`** — per-scope workhorse; dispatched transitively by iteratotron, not directly here
- **`bugfix`** — used for the post-merge review pass over the generated harness's own code

## Caveats

- **The generated harness has its own bugs.** New concurrency, persistence, and process-identity code always does. Run `bugfix` Path B (autonomous discovery) on the new modules after Step 9.
- **Runtime harnesses are Rust or Go only.** No canonical pattern exists for Python or Ruby runtime harnesses.
- **Python and Nix harnesses use the legacy `claude -p` stream-json backend.** The opencode-server backend for these two is a follow-up. If you explicitly need claude-stream for another language, pass `agent_host:claude-stream` as an argument — it's accepted but not the default.
- **Nix-as-deliverable E2E is KVM-gated and expensive.** `runNixOSTest` boots real QEMU VMs (needs `/dev/kvm`, ~4GB+ RAM, minutes per run); the heavy GitLab-style stack is multi-minute. Keep derivation-level (`passthru.tests`/`testVersion`) and module-eval (`lib.evalModules`) tests in the inner loop and gate full VM/E2E to a nightly tier. Don't embed tvix/snix as the evaluator — shell out to `nix`; see `references/nix-harness-toolchain.md`.
- **`<project>-genesis/` naming is historical.** Named after the mode, not the merged skill.
- **`type:both` may be delivered as ONE binary with two subcommands, not two crates.** When both harness types target the same repo and language (esp. Rust), folding genesis into the runtime crate as a `genesis` subcommand (`<bin> runtime|genesis`, top-level flatten so the historical no-subcommand invocation still works) is preferred: the two phases then share **one** `opencode_server` driver, **one** `sandbox` preflight, and one `opencode-serve` launch — no duplicate ~660-line driver to keep in sync. The genesis modules live under `src/genesis/` and reuse `crate::opencode_server` + `crate::sandbox`. Genesis dispatch drives one server session per scope/burndown; its adversarial verdict derives from the structured `SessionOutcome` (completion + `tool_calls`), not a stream-json log — an incomplete session requeues the scope, a zero-tool-call completion parks it for a human. This is the gitlab-harness shape (the standalone `gitlab-genesis` crate was merged in and deleted).
- **Runtime scenarios surface real project gaps — fix them in the project, don't relax the scenario.** A driven scenario that flags a missing response field or an unrouted endpoint (a bare 405) is a true API-parity defect. Fix the project (add the field to the serializer + all its query column lists; route the verb with a structured 501 that names the unwired backend, mirroring sibling write endpoints), add a project-level regression test, and the scenario flips from gap-detector to passing coverage. Keep the scenario asserting the **desired** outcome (the upstream-faithful status/shape) so it converts the moment the implementation lands — never weaken the assertion to make a gap "pass". Endpoints blocked on an unwired subsystem (e.g. a git/Gitaly write path) return a structured 501 that names the gap, never a bare 405 or a fake 201.
- **Multi-select `orchestration:` is real.** Use `AskUserQuestion` with `multiSelect: true` — don't force one choice.
- **Harness session state goes in `.gitignore`.** `.iteratotron/` and `.bug-burndown/` are transient. The harness source itself goes in source control.
- **The interview is the dispatch.** Picking options yourself "to be efficient" generates the wrong harness. `AskUserQuestion` is non-optional unless every argument is supplied.
