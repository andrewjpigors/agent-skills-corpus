---
name: ultracodex
description: "Token-frugal orchestration — Claude/Opus stays the architect (decompose, judge, synthesize, verify critical work) and routes all token-heavy work (writing code, searching, running tests, bulk discovery) to the cheaper Codex lane (gpt-5.6) via codex exec, keeping artifacts on the filesystem instead of in Claude's context. Use for substantial coding/refactor/audit/migration tasks to minimize metered Bedrock tokens. Invoke as /ultracodex <task>, or when the user asks to offload work to Codex, save Claude tokens, or run the architect pattern."
---

# /ultracodex

Keep ultracode's thoroughness; move the token-heavy work off metered Claude onto the cheaper
Codex. **You (Opus) are the architect** — you emit the fewest tokens (judgment, specs,
verdicts). Every token-heavy unit routes to a Codex worker via the helper. See the full
design in `docs/DESIGN.md`.

## The worker helper

Run one unit of work on the cheaper Codex lane:

```
bash ~/.claude/skills/ultracodex/codex-worker.sh "<task prompt>" [workdir]
```

- **ALWAYS go through this wrapper — never call the raw `~/bin/codex` shim (or a
  hand-rolled `codex exec`) directly.** The wrapper is where the service tier, the
  per-call `ULTRACODEX_MODEL`/`_EFFORT` overrides, the retry-once, the JSONL telemetry
  (`~/.claude/ultracodex-worker.log`), and the clean "final-message-only" output all
  live. Bypassing it means: no per-unit right-sizing, no retry,
  no visibility into WHY a call hung — you're left tailing a temp file and guessing. The
  raw shim exists only as a PATH passthrough for interactive use; it is NOT the
  orchestration path.
- Resolves the Codex binary dynamically, runs `codex exec`, prints ONLY the worker's
  final message. Exit 0 = success.
- On failure/timeout/binary-missing it prints a line starting `ULTRACODEX_WORKER_ERROR:`
  and exits non-zero → that is your signal to run the **Codex-down fallback** (below).
- Run workers in PARALLEL by issuing multiple Bash calls in one turn.

### Large fan-out (research, bulk lookups) — spawn as many as you need

There is NO artificial cap on parallel Codex workers, and you should not impose one.
Codex concurrency is safe: verified at 12 simultaneous workers with zero SQLite
lock contention and clean DB integrity (they share `~/.codex` in WAL mode and coexist
fine). The real limits are your machine's CPU/RAM and how many Bash calls you can issue
per turn — not an ultracodex constraint. So for research-style work (many independent,
read-heavy, low-judgment questions), fan out freely.

For batches too large to hand-issue as separate Bash calls, use the batch helper:

```
bash ~/.claude/skills/ultracodex/codex-batch.sh <tasks-file|-> [base-workdir]
```

One task per line (blank lines and `#comments` skipped). Concurrency is unlimited by
default; set `ULTRACODEX_MAX=<n>` only if you want to spare CPU/RAM. All worker env knobs
pass through — e.g. `ULTRACODEX_MODEL=gpt-5.6-luna ULTRACODEX_EFFORT=low` for cheap bulk
lookups, or `ULTRACODEX_SEARCH=1` for web research. Launch the batch itself with the
Bash tool's `run_in_background:true` if it will run past ~2 min.

**Workdir mode — pick the right one or files land in the wrong place:**
- **default (ISOLATED):** each task gets its OWN throwaway workdir `<base>/u<idx>`. Correct
  for research / bulk-lookup fan-out (independent units writing to scratch). **WRONG for
  "edit N files in ONE repo"** — a worker's relative paths resolve against `u<idx>` (files
  land in `<repo>/u2/...`) and absolute writes to the repo are sandbox-DENIED (outside the
  `u<idx>` workspace). This mismatch has cost a whole session — do not use isolated for
  same-repo edits.
- **`--shared`:** EVERY worker runs in `<base>` itself (the repo), sharing one workspace-
  write sandbox. Use this when the tasks all edit files in the same repo. Bookkeeping
  (`results.jsonl`) is kept in a temp state dir, so the repo stays clean.
  `codex-batch.sh --shared <tasks> <repo>`. (For same-repo work also weigh the prompt-shape
  rule below: whole NEW files → Codex; scattered edits into one big existing file → you.)

**Retry only the failures:** `codex-batch.sh --retry <base>` re-runs ONLY the units whose
`rc != 0` from the prior run (same task + workdir), merges the outcome, and exits 0 once all
are green. Idempotent — repeat until clean. The normal-run footer prints the exact retry
command when any unit fails.

### Staged work (build → test → verify) — the pipeline helper

`codex-batch.sh` is single-stage. When each item needs to flow through ORDERED stages
(e.g. write a file → run its tests → verify), use the pipeline helper — the free-lane
equivalent of the (blocked) Workflow tool's `pipeline()`:

```
bash ~/.claude/skills/ultracodex/codex-pipeline.sh <items-file|-> <stage1> [stage2 ...] [-- base-workdir]
```

Each stage is a prompt TEMPLATE with two placeholders: `{item}` (the current line) and
`{prev}` (the previous stage's summary, empty at stage 1). Every (item, stage) is one
`codex-worker.sh` call in the item's own workdir, so stages share the filesystem within an
item. Items run in parallel with NO barrier between stages (item A can be verifying while
item B is still building); a stage that fails DROPS that item and skips its rest. Keep
stages few and mechanical — judgment stays with you. `ULTRACODEX_MAX` throttles concurrent
items; run it `run_in_background:true` (multi-stage easily exceeds 2 min).
- Env knobs (all optional; persistent default = gpt-5.6-sol/xhigh via ultracodex.env):
  - `ULTRACODEX_MODEL` / `ULTRACODEX_EFFORT` — pick these TOGETHER. **The big lever is
    EFFORT, not tier:** a cheaper model thinking longer matches/beats a pricier model
    thinking less (Artificial Analysis: for any Terra point there's a Luna-or-Sol point that's
    ≥ intelligent at ≤ cost — **Terra is Pareto-dominated on intelligence/$**; Berman's coding
    bench agrees Luna > Terra). So the default ladder is **Luna ↔ Sol, and Terra only for its
    one niche** (below). Models: `gpt-5.6-luna` (cheapest, 25/150 cr/1M) · `gpt-5.6-terra`
    (62.5/375) · `gpt-5.6-sol` (flagship, 125/750). Efforts: `low|medium|high|xhigh|max|ultra`
    (Luna has no `ultra`). **`ultra` = `max` + 4 parallel subagents for SPEED, not more
    intelligence** (Raschka) — so in the worker use **`max`, never `ultra`** (ultracodex already
    fans out at the Claude level; ultra = double, nested fan-out for zero intelligence gain).
    Effort raises reasoning-token VOLUME, not per-token rate.
    - **Routing by shape (short/normal context):** trivial/mechanical → **Luna high**
      (Luna high ≈ Sol low in cost, more intelligent — the sweet spot for most bulk units);
      real coding under a clear spec → **Luna xhigh/max** or **Sol medium/high**;
      hardest / ambiguous / safety-adjacent → **Sol max** (the ceiling; reserve for units that
      truly need it). Skip Sol xhigh — Terra max or Sol max bracket it better.
    - **CONTEXT SIZE overrides all of the above — it gates the tier (long-context evals):**
      **Luna COLLAPSES on large context** — OpenAI MRCR v2 8-needle retrieval ~41% at 256K–1M,
      *worse than gpt-5.5*, ~coin-flip, and NO effort level fixes it (effort adds reasoning,
      not attention over long input). So the moment a unit's context is big (read-a-big-file /
      many-files / long-history), Luna is DISQUALIFIED regardless of effort → **this is Terra's
      one niche: context-heavy mechanical work** (Terra ≈89% vs Sol ≈91% at 256–512K, ~half
      Sol's rate). Sol itself drops ~91%→~74% crossing 512K, so even Sol wants context kept
      under ~256–512K — **split a huge unit rather than feed one worker 1M tokens.**
  - `ULTRACODEX_SCHEMA` — path to a JSON Schema → deterministic verdict
    (`{"passed":bool,"summary":str}`) instead of prose. Use when a wrong "passed" is costly.
  - `ULTRACODEX_SEARCH=1` — allow live web search (maps to `-c tools.web_search=true`;
    NOT `--search`, which `codex exec` rejects). For research units needing current docs.
  - `ULTRACODEX_MCP` — comma-list of MCP servers to give THIS worker (`context7`,
    `playwright`). Injected per-call via `-c mcp_servers.*`, so the default worker stays
    zero-MCP and fast (every base-config server spawns per `codex exec`). See the
    MCP/skills section below for the doctrine on what belongs in the worker lane.
  - `ULTRACODEX_TIER` — service tier: `priority` (the "Fast, ~1.5x speed, increased
    usage" tier) or `default` (Standard). **Defaults to `priority`** since Codex is the
    cheap lane. Set `ULTRACODEX_TIER=default` to drop back to Standard. Stacks with the
    model/effort knobs (e.g. `gpt-5.6-luna` + `low` + `priority` = fastest).
  - `ULTRACODEX_PROFILE` — layer a `$CODEX_HOME/<name>.config.toml` (`-p`). Defaults to
    `ultracodex` if `~/.codex/ultracodex.config.toml` exists (it does — pins worker
    model/effort/sandbox independently of the interactive session).
  - `ULTRACODEX_NO_PREAMBLE=1` — skip the standing worker-instruction preamble.
  - `ULTRACODEX_VERIFY="<cmd>"` — **opt-in post-write compile/verify gate.** After the worker
    writes its files, run this FAST check in the workdir and append `ULTRACODEX_VERIFY: PASS/FAIL`
    to the summary. **Closes the #1 recurring miss: "Codex's read-back review passed but it never
    compiled"** — a model reviewing its own file is NOT a compile (a Sol Compose file passed its
    own review with 4 real `-Werror` errors). Use the module-scoped compile, never a full build:
    Kotlin/Compose → `./gradlew :app:compileDebugKotlin`, Rust → `cargo check`, TS → `npx tsc
    --noEmit`, Go → `go build ./...`. A verify FAIL does NOT flip the worker's exit code — it's a
    signal for YOU to read and fix, not a crash (files are already written). Bounded by
    `ULTRACODEX_VERIFY_TIMEOUT` (default 90s); the whole call still has the 2-min Bash-tool cap, so
    keep the command fast + background the call if needed.
  - `ULTRACODEX_EXPECT_FILES` — **guard against phantom success.** A unit whose job is to
    produce a deliverable can exit 0 having written NOTHING (it replied with the content inline
    instead of saving it) — and a naive session believes it succeeded. Set this to make the
    worker turn that false success into a LOUD failure (rc 66): `=1` requires ≥1 file
    created/modified in the workdir; `=<glob>` (e.g. `.planning/analysis/*.md`) requires a match.
    Use it on any "write a file" unit — especially batch/backgrounded ones you won't eyeball.
    (Shared-mode batch: prefer the glob form; `=1`'s "newer than start" is racy across co-located
    units.) Leave unset for research/verify units that legitimately write nothing.
  - `ULTRACODEX_LANG` — force a conditional language-rules block into the preamble (e.g.
    `compose`/`kotlin`). Auto-detected from the task text too, so you rarely need to set it — a
    task mentioning Compose/Kotlin/`.kt` auto-gets the **Compose scope-only-extensions rule** (the
    `Modifier.weight`/`.align` import trap that broke builds 3×: those are scope extensions, never
    a top-level import). Add more language blocks in the worker the same way as they earn their keep.
  - `ULTRACODEX_TIMEOUT` (600s), `ULTRACODEX_SANDBOX` (workspace-write),
    `CODEX_BIN` (explicit binary).
- **Standing preamble:** every worker automatically gets the ultracodex contract
  (headless, no questions, no commit, stay in workdir, use `$UCX_PYTHON`, reply ≤3
  lines) prepended — so you don't re-type it per prompt. Verified: workers obey the
  terse contract without the caller stating it. The preamble also enforces **write-first,
  verify-last**: the worker flushes all files to disk and prints `FILES WRITTEN: <paths>`
  BEFORE any build/test, and is told NOT to run full project builds (gradle/make/whole-repo
  test) unless the task asks. So if a unit times out, its files are usually already on
  disk — the worker's timeout message lists them; check the workdir before assuming loss.
- **Per-unit tuning is the point:** Luna + high effort for *short-context* mechanical units
  (effort is the lever — Luna high beats Terra; Luna is only safe when the unit's context is
  small — see the long-context warning above), Sol max for the hardest, and Terra ONLY for
  context-heavy mechanical units (its one niche) — the audit log records model/effort/profile
  per run so you can see (and prove) the mix.
- **Binary resolution:** binary is resolved by the shared `resolve-codex.sh`
  (version-sorted, skips `.obsolete` builds, validates the binary runs — no more
  mtime-picks-a-stale-build risk; the shim and worker share it so they can't drift).
  The worker **retries once** on a transient exec failure (not on timeout/success) and
  appends a JSONL line to `~/.claude/ultracodex-worker.log` per run (workdir/rc/attempts
  → provable savings). Turn those logs (+ the routing log) into a summary with
  `bash ~/.claude/skills/ultracodex/ucx-report.sh` (or `--json`): worker runs, success
  rate, deny/allow split, and a COARSE estimate of Opus tokens kept off the metered lane.
- **Deterministic verdicts:** for anything where a wrong "passed" is costly, pass
  `ULTRACODEX_SCHEMA=<schema.json>` so the worker returns structured JSON
  (`{"passed":bool,"summary":str}`) you can trust-but-verify instead of eyeballing prose.

### Worker duration — background anything non-trivial

The **Bash tool caps wall-clock at ~2 min (default) / 10 min (max)** — this is the
HARNESS limit and it kills the call with **exit 143 (SIGTERM)** regardless of the
`timeout 900` inside the command. A `codex exec` unit that reads several files, writes
code, and runs tests routinely exceeds 2 min.

Rule of thumb (from measured runs): trivial ≈ 7s, code+test ≈ 10–30s, **research /
multi-file / plan-writing / big-refactor units ≈ minutes → WILL be killed at 120s.**

So:
- **Trivial/short units:** call `codex-worker.sh` synchronously (fine under the cap).
- **Anything substantial (research, planning, multi-file build, test-heavy):** launch
  the worker with **`run_in_background: true`** on the Bash tool — it survives the cap,
  runs across turns, and **the harness AUTO-RE-INVOKES you when it finishes.** So: fire
  it, then either do other useful work or end your turn — the re-invocation brings you
  back with the result to read. **Do NOT `sleep`/poll the output file to "wait" for it** —
  that burns a turn (and can itself hit the 2min cap) for zero benefit; the notification is
  automatic. Only read the output file early if you specifically need partial progress.
  Don't rely on the inner `timeout` — it can't beat the tool cap.
- If you get **exit 143**, that is the cap, not a Codex failure — relaunch in the
  background, don't treat it as ULTRACODEX_WORKER_ERROR.

#### How a failed/timed-out worker reaches YOU (there is no separate "notifier")

The completion re-invocation is the notification — **and it fires on FAILURE and TIMEOUT,
not just success.** When a backgrounded worker exits, the harness brings you back with its
exit status and output regardless of rc. The worker makes that result unmissable: on any
failure/timeout it prints a loud **`ULTRACODEX_WORKER_ERROR:`** line to stderr and exits
non-zero (124 inner-timeout, 143/137 tool-cap kill, else a real Codex error), with a
`files written before the cut-off may be usable: …` hint so you know whether its output
survived. So you don't need a Telegram/desktop pinger to "notify Claude" — reading the
non-zero result on re-invocation IS the notification. When you see one:
- **rc 124 / 143 / 137** → the wall-clock cap or inner timeout, NOT a Codex fault. The
  files are often already on disk (the worker writes-before-verifying) — check the workdir
  / the `files written…` hint before redoing the work; then relaunch backgrounded (or
  right-size the model — see the latency rule) if anything's missing.
- **other non-zero rc** → a genuine Codex error (the worker already retried once on a
  transient blip). Read the `ULTRACODEX_WORKER_ERROR:` detail, then fall back per the
  Codex-down section (inline / spawn subagent / stop).

**The one way to LOSE this notification: never `&`-detach workers *inside a single Bash
call*** (e.g. `codex-worker.sh … & codex-worker.sh … &` in one command). That orphans them
from the harness — the Bash call returns immediately, the workers keep running unwatched,
and you get NO re-invocation when they finish/fail (you're left blind-polling, the exact
trap that cost a session). To run several at once, either issue **multiple `run_in_background`
Bash calls in one turn** (each is tracked and each re-invokes you), or use **`codex-batch.sh`
launched as ONE `run_in_background` call** — the batch process is the tracked foreground job,
so its own internal parallelism is fine and you get one re-invocation when the whole batch
ends (with `results.jsonl` recording every unit's rc).

## The two iron rules (the whole point)

1. **Artifacts flow through the filesystem, NOT your context.** The worker reads files,
   writes code, runs tests — all on disk. You never read a file's contents or the
   worker's verbose output back. You read only the terse summary the worker returns
   (make it reply in ≤3 lines: status / files touched / test result). Reading full
   diffs back into Opus defeats the entire purpose — it makes this MORE expensive than
   doing the work natively.
2. **Escalate on stakes, not on cost.** Read the real artifact yourself ONLY when the
   work is security/auth/data/money-relevant, a worker reports failure, or a summary is
   surprising / smells off. Routine → trust the terse summary.

## Routing doctrine (who does what)

| Work | Lane |
|---|---|
| Decompose the task, route units, plan | **You (Opus)** |
| Architecture / design / ambiguity calls | **You (Opus)** |
| Final synthesis + the answer to the user | **You (Opus)** |
| Verify security/correctness-critical results | **You (Opus)** — read the real artifact, try to refute |
| Write code, refactor, run tests | **Codex worker** |
| Bulk search / discovery ("find all X") | **Codex worker** |
| Routine verification (tests pass? builds?) | **Codex worker** |

Worker model = gpt-5.6-sol at xhigh (default *floor* — safe for any unit) — flagship-tier,
treat as Opus-adjacent for implementation under a clear spec. But EFFORT is the real lever,
so actively right-size per unit: most short-context implementation → **Luna high** or **Sol
medium** (matches Sol/xhigh quality far cheaper); reserve Sol max for the hardest; Terra only
for context-heavy mechanical units. Quality comes from YOUR spec clarity + effort level +
YOUR verification of the critical bits, not from always paying for the top tier.

### The hardest work — where the ceiling actually is

"Max out the model" is not one dial. The ceiling depends on WHAT is hard:

- **Hard JUDGMENT** (architecture decision, tradeoff, ambiguity, "what should we build /
  why is this broken") → **stays on YOU (Opus)**. A Codex model is weaker at judgment at
  ANY tier, so Sol+ultra on a design *decision* lowers the ceiling, not raises it. This is
  the work that used to go to Fable — it comes back to Opus, not to a bigger Codex effort.
- **Hard EXECUTION** (approach is known, the *doing* is gnarly) → **Sol**, and pick effort
  by shape:
  - One deep problem (subtle bug, tricky algorithm, single dense reasoning chain) →
    **Sol + `max`** (max = more time on a *single* task; depth over speed).
  - One large **self-decomposable** task you hand off WHOLE → **Sol + `ultra`** (ultra =
    parallel subagents) — **only if you are NOT already splitting it** with batch/pipeline,
    else it's double, nested fan-out. Ultra is a specific tool, not a general "amazing"
    button.
- **The real ceiling = the combination, not a bigger effort number:** for work that truly
  matters, **YOU direct → Sol+max executes (often 2–3 attempts from different framings via
  `codex-batch.sh`) → YOU adversarially judge/synthesize the winner.** Independent attempts
  + your judgment beat one worker thinking longer — a single max/ultra pass has one blind
  spot; diverse framings + Opus synthesis cover it. (This is the judge-panel / diverse-lens
  recipe above, aimed at the hardest unit.)

### Cheap pre-review (optional) — `codex-review.sh`

Review/judgment stays YOURS (the block hook keeps it on Claude). But you can get a free
Codex first pass over a diff to surface the obvious stuff before you judge:

```
bash ~/.claude/skills/ultracodex/codex-review.sh --uncommitted -C <repo>   # or --base <branch> / --commit <sha>
```

It wraps `codex review` (Codex 0.144+) and prints a clean findings list (P0/file:line).
Treat the output as LEADS, not conclusions — YOU re-judge each (real? severity? false
positive?) and remain the reviewer of record. It's a token-saving pre-filter, not a
replacement for your review. **Slow (~2-4 min even cheap) — always `run_in_background:true`.**
Right-size it: `ULTRACODEX_MODEL=gpt-5.6-luna ULTRACODEX_EFFORT=low`.

### What actually fits Codex (learned from real runs)

The routing table is necessary but not sufficient — the shape of the change matters more
than the category:

- **GOOD for Codex:** NEW leaf files (a new module + its tests), and big MECHANICAL
  fan-outs (a migration across many call sites, a bulk decoder/lookup table, a test
  matrix over many cases). This is where the token savings are real and Codex nails it.
- **BAD for Codex, keep on Opus:** edits to pre-existing core files (Codex's sandbox is
  often ACL-DENIED from touching them — it will fail the write and, worse, waste time
  investigating the denial), and small safety-critical edits where a wrong call is
  expensive (auth, money, data-integrity, byte-frozen formats, correctness-sensitive
  math). A 60-line safety edit is NOT a Codex job even though it's "writing code."
- **Tell the worker its limits IN THE PROMPT:** "you'll be ACL-denied on pre-existing
  files under <dir> — do not attempt them, do not investigate the denial; write only the
  new files I name and hand me a diff for any edit to an existing file." (The worker
  preamble now says this by default, but name the specific dirs.)
- **Every test spec:** "drive the real exported function; never re-assemble the
  production string/value in the test." Codex won't self-apply your project's
  test-the-delivered-behavior lessons — state it each time.

Honest note: on a queue that's mostly edits-to-existing-core or safety-critical
judgment, the Codex split barely applies and you'll (correctly) work solo. Don't force
work onto Codex to hit a token target; the savings come from the mechanical/new-file
pieces, not from pretending a safety edit is one.

**ROI is STRUCTURALLY CAPPED on some projects — say so up front.** Real-world observation
(e.g. an Android/Kotlin feature session): the dominant unit shape was *multi-point edits into
large existing files* (a ViewModel, a Scaffold, a detail screen) — which is exactly what stays
on Opus (ACL-denied on pre-existing files + safety-adjacent). So most of that session correctly
ran on Opus, and the Codex savings were small **by the nature of the work, not a tool failure.**
When you scope a task, set the honest expectation: if the queue is mostly existing-file edits,
ultracodex saves little here and that's fine — flag it rather than manufacture Codex work to
look busy. The big wins are net-new leaf files (module + tests), bulk mechanical fan-outs
(migrations, lookup tables, test matrices), and research/discovery — projects heavy in those
see the real savings; projects heavy in core-file surgery structurally won't.

### Prompt shape — the two rules that decide latency

1. **Whole NEW file → Codex; multi-point edits into a large existing file → you (Opus).**
   The one worker that timed out was 4 separate insertions into a 900-line file — Codex
   had to locate every site, hold the whole file, and reason about placement (slow +
   error-prone), on top of the ACL-denial risk. When a change would be several edits into
   one big existing file, instead hand Codex a self-contained NEW file and do the 1–2
   line wiring into the existing file yourself. New leaf files are its sweet spot; scatter
   edits into big files are its worst.
2. **Give Codex the SPEC, not near-final code.** If you've already written the code in
   the prompt, the round-trip to Codex adds latency for ~zero gain — just apply it
   yourself. Codex earns its keep on "here's the contract + the filename, produce the
   file," not "type these exact bytes." Over-specifying is a smell that the unit was
   actually an Opus job.
3. **Right-size the model to LATENCY, not just difficulty.** `gpt-5.6-sol` at `xhigh` is
   the flagship but it is SLOW — a ~300-line file with rich detail can run past the
   backgrounded worker's practical window. For large-but-MECHANICAL generation (a screen
   from a tight spec, a boilerplate module) drop to `gpt-5.6-terra` (and/or `high` effort):
   it finishes in time and the spec, not the tier, carries the quality. Reserve `sol`+`xhigh`
   for genuinely hard reasoning. Either way, background it and rely on write-first so a
   timeout still leaves usable files. If a unit repeatedly times out even backgrounded,
   split it (two smaller files) or write it yourself — that's the signal it was an Opus job.

## Skills and MCP servers — what the worker can and can't reach

The worker is a fresh Codex process; it does NOT inherit your Claude skills or your
session's MCP connections. Handle each deliberately:

- **Claude skills are doctrine, not runtime tools.** A skill tells you HOW to do
  something — that's YOUR job to read and distill into the worker's spec. The worker
  never needs the skill installed; it needs a self-contained prompt, which is exactly
  what the architect produces. So there is no "skill gap" for process/doctrine skills —
  reading the skill and embedding its method in the unit spec is the intended flow.
- **MCP servers: Codex supports them natively** (`[mcp_servers.*]` config, `codex mcp`),
  but each one spawns PER `codex exec`, so loading them all would slow every worker. The
  split, by the same logic as the code-vs-safety routing:
  - **Give the worker READ-ONLY KNOWLEDGE MCPs** — e.g. `context7` (library/API docs).
    Opt in per unit with `ULTRACODEX_MCP=context7`. Verified end-to-end: a sandboxed
    worker called `mcp__context7.resolve_library_id` and got docs back.
  - **DB/dev MCPs work in the worker too — including session-bound ones.** A DB/dev MCP
    registered GLOBALLY in `~/.codex/config.toml` is reachable from every worker with no
    flag (verified end-to-end: a sandboxed worker ran a real `SELECT` through the InterSystems
    IRIS MCP and got the result back). So DB-heavy work (SQL, class compiles) can go to the
    free lane. If such a server binds a **session-bound transport** (e.g. a named pipe whose
    name rotates per editor session, so a hardcoded address in `config.toml` goes stale on
    restart), that is the **MCP server's own problem to solve** — a well-built one self-heals
    (re-resolves a live endpoint on connect). Do NOT add a pipe-resolver to this generic
    worker; that couples a vendor-neutral tool to one MCP and duplicates, less robustly, what
    the server should already do.
  - **Keep STATEFUL / OUTWARD-FACING MCPs on the orchestrator by default** — e.g.
    `playwright` (browser) or any device/service-control MCP. Fragile under the
    restricted-token sandbox, and these are the "confirm before acting" operations that
    belong under your judgment — same reason safety edits stay on Opus. (`playwright` is
    available via `ULTRACODEX_MCP=playwright` if a unit genuinely needs headless browser
    work, but default to keeping it on the orchestrator.)
  - **Web fetch/search needs no MCP** — use `ULTRACODEX_SEARCH=1` (Codex's native
    `web_search`), which is keyless. (A "firecrawl"-style scraper MCP would just be a
    heavier, key-requiring duplicate of this.)

Net: the worker gets read-only knowledge tools AND DB/dev MCPs (with a freshly-resolved
connection); you keep the outward-facing, confirm-before-acting connections.

## Lifecycle

1. **Decompose** (reasoning only; read no big files). Produce units, each tagged with
   its lane. Write each unit's spec clearly enough that a context-free worker can do it
   without guessing (embed the full spec in the prompt — workers share no memory).
2. **Dispatch** the Codex-lane units via `codex-worker.sh`, in parallel where
   independent. Each prompt ends with: "Reply in ≤3 lines: status / files touched /
   test result."
3. **Verify by stakes.** Routine → delegate the check to another Codex worker
   ("run the tests, reply pass/fail in one line"). Critical → you read the artifact and
   adversarially judge it.
4. **Synthesize** from the summaries (never the diffs) → the answer to the user. If you
   bounded coverage (skipped a slow test, sampled), say so — no silent shortcuts.

Preserve the ultracode quality shape: fan-out → loop-until-dry → adversarial verify →
completeness critic → synthesize. Only the workers changed (Codex, not Claude subagents).

## Orchestration recipes (Workflow-grade thoroughness, Codex leaves)

The Workflow tool is blocked because it fans out a **Claude** fleet. You get the same
*shapes* by composing the Codex helpers with YOU as the loop controller. The stability
comes precisely from keeping the between-round judgment on Opus — never build a Codex loop
that self-judges whether to continue.

- **Parallel fan-out (barrier):** `codex-batch.sh <tasks>` — N independent units at once,
  collect all, then you act on the full set. Use when you need every result together
  (dedup, "0 found → skip").
- **Pipeline (no barrier):** `codex-pipeline.sh <items> <stage1> <stage2> …` — each item
  flows build→test→verify independently. Use for staged per-item work.
- **Loop-until-dry (unknown-size discovery):** loop in YOUR turns —
  `codex-batch.sh` a round of finders → you dedup fresh vs. a `seen` set you hold → repeat
  until K consecutive rounds add nothing. You own the "are we dry?" call; Codex only finds.
- **Find → verify:** `codex-batch.sh` finders → feed the hits into a `codex-pipeline.sh`
  verify stage (or verify the critical ones yourself). Cheap breadth, then judgment where
  it matters.
- **Judge-panel / diverse-lens:** `codex-batch.sh` the same question from N angles
  (different prompts/models) → YOU synthesize the winner. Codex generates; Opus judges.
- **Structured verdicts:** add `ULTRACODEX_SCHEMA=<schema.json>` so a round returns
  `{passed,summary}` JSON you can branch on deterministically instead of eyeballing prose.

Two rules that keep these stable: (1) every round's results are terse summaries / JSONL on
disk — you read those, never the diffs; (2) background any round that runs past ~2min and
let the completion notification bring you back (don't poll). The "engine" is you between
rounds — cheap, because the coordination is just reading summaries.

## Flags

- `--paranoid` — read + spot-check EVERY worker result, not just critical ones. Highest
  safety, more Opus tokens. Use for high-stakes changes.
- `--yolo` — you only decompose and give the final verdict; everything else (incl.
  verification) is Codex. Lowest Opus tokens.
- default = **Balanced**: the routing table above + hair-trigger escalation.

## Codex-down fallback (do NOT deadlock)

If `codex-worker.sh` returns `ULTRACODEX_WORKER_ERROR` / non-zero (Codex unreachable,
timed out, or app-server broken): do NOT silently proceed. **Warn the user** and offer
three choices:
- **(a) Inline** — you do the unit yourself in Opus (spends metered tokens).
- **(b) Spawn subagent** — `touch ~/.claude/.allow-subagents-<session_id>` (lifts the
  block hook for THIS session, auto-expires 10 min), run the Claude subagent, then `rm`
  that file to re-block.
- **(c) Stop.**
**If the user is AFK / does not answer: default to STOP & WAIT** — spend no tokens, run
nothing unattended. (Matches the block hook `ultracodex-block-subagents.js` and the user's
gate-manual-steps preference.)

## Known caveats

- **Running Python tests in-sandbox: use the REAL python, not the WindowsApps shim.**
  The `workspace-write` restricted-token sandbox CANNOT spawn
  `...\WindowsApps\python.exe` (a store symlink → "a specified logon session does not
  exist"). The fix (verified: sandboxed worker wrote code AND ran pytest → `1 passed`):
  the helper resolves a real CPython and exports it as **`$UCX_PYTHON`**
  (`~/AppData/Local/Python/pythoncore-*/python.exe`). When a unit must run Python tests,
  tell the worker to run them with `"$UCX_PYTHON" -m pytest ...` — NOT bare `python`.
  This keeps sandbox isolation ON, stays fully free, and needs no full-access. Only fall
  back to `ULTRACODEX_SANDBOX=danger-full-access` if a tool genuinely can't be reached
  otherwise — and that disables isolation, so auto-mode will (correctly) require the
  user's explicit approval.
- **Concurrency is safe.** 6 parallel workers ran clean, no `~/.codex` SQLite lock
  contention, DB integrity ok afterward. A few transient `codex.exe` app-servers may
  linger briefly after a burst (they exit on their own; not the zombie-pileup failure
  mode). Give each worker its OWN workdir to avoid file clobbering.
- **Failure is isolated.** One worker's error (bad binary, timeout) does NOT affect
  siblings in the same parallel batch. The helper auto-creates a missing workdir.

## Notes

- The block hook already prevents you from spawning Claude subagents/Workflows, so
  routing to Codex is enforced, not just suggested. This skill is the *smooth* way to
  do the orchestration the hook forces.
- Building/editing this skill itself is orchestrator work — do it inline, don't try to
  spawn subagents for it (the hook would block that anyway).
