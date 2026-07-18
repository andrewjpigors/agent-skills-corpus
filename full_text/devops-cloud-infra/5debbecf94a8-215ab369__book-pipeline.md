---
name: book-pipeline
description: Launch deep source-code-analysis book publishing pipeline. Orchestrates Agent Teams working in parallel through full flow from clone to final draft. Same as /tech-insider:make-book command.
user-invocable: true
---

# Deep Source-Code Analysis Book — Pipeline Orchestration

You execute full book publishing pipeline. Move through phases sequentially, using **Agent Teams** for parallel work within each phase.

## Critical: You (Lead) Do NOT Do Actual Work

- **Do NOT** clone repositories, read source code, analyze codebases yourself — delegate to teammates
- **Do NOT** write chapter content, review chapters, generate any book artifacts
- **Do NOT** spawn subagents for actual work — all work done by Agent Teams within each phase

### The Lead's Operating Loop

**Your entire job is this cycle:**

```
Make decision (create tasks, spawn teammates, present to user)
  ↓
Wait for mailbox message (teammate completion, idle notification, user response)
  ↓
Make next decision (shutdown, next phase, fix, deliver)
  ↓
Wait for mailbox message
  ↓
(repeat)
```

**You should be idle most of the time.** Moment you finish decision, yield. Wait for mailbox. System notifies when teammate completes, when teammate goes idle, or when user responds. Only then make next decision. Never fill idle time with polling, monitoring, or doing teammates' work.

**CRITICAL: After sending message to any teammate (SendMessage), you MUST STOP and yield immediately.** Do NOT make any more tool calls. Do NOT "check status." Do NOT "prepare next phase." Your message send is last action of turn. Next turn triggered by mailbox notification. If you continue working after SendMessage, you block mailbox and cause DEADLOCK.

## Team Lifecycle Discipline

**Pipeline uses ONE team throughout. Create it once at Phase 3, recycle members between phases, delete at end.**

### Waiting Discipline (Applies to EVERY phase)

**Whenever lead spawns teammate or sends message to teammate, lead MUST yield immediately.** No exceptions.

- **CRITICAL: Polling DEADLOCKS mailbox.** `sleep`, `sleep && stat`, `Monitor("Wait 60s and check for file")` — any polling mechanism blocks incoming mailbox messages from teammates. Lead will never see completion message because it's busy polling. **This is deadlock, not timeout.**
- **CRITICAL: After any SendMessage to teammate, your turn is OVER.** Do NOT make more tool calls. Do NOT "check on way." Do NOT "prepare next step." Just yield. Next turn triggered by mailbox notification.
- **Lead's only action while waiting: DO NOTHING.** Do NOT poll, do NOT monitor, do NOT check output files, do NOT grep for completion strings. Just yield and wait for system to deliver teammate's completion message.
- When teammate goes idle (mailbox notification received), send ONE structured shutdown request:
  ```
  SendMessage({ to: "<name>", summary: "shutdown", message: { type: "shutdown_request", request_id: "shutdown-1", approve: true } })
  ```
  Then wait for idle confirmation before proceeding.

### Phase Transition (Shutdown Old → Create Tasks → Spawn All New)
Between every phase that uses Agent Teams:
1. **Shutdown old teammates**: For each active teammate, send structured shutdown request:
   ```
   SendMessage({
     to: "<teammate-name>",
     summary: "shutdown",
     message: { type: "shutdown_request", request_id: "shutdown-1", approve: true }
   })
   ```
   **Use structured message format above — NOT plain string.** **One request per teammate. Do NOT send multiple.**
2. **After sending ALL shutdown requests, YIELD IMMEDIATELY.** Turn over. Next turn triggered by mailbox notifications from teammates confirming shutdown. **Do NOT proceed to step 3 in same turn.**
3. **Wait for all shutdowns** — teammates confirm via mailbox. System takes moment to process. **Do NOT proceed until all old teammates confirmed gone (idle notification received).**
4. **Create tasks**: Use `TaskCreate` to create ALL tasks for this phase with clear descriptions.
5. **Spawn ALL teammates at once** — call Agent multiple times in parallel (one per teammate needed), ALL with `team_name: "book-pipeline"`. **Do NOT spawn one at a time sequentially.** Number of teammates to spawn depends on phase (see phase-specific instructions).
6. **After spawning ALL teammates, YIELD IMMEDIATELY.** Turn over.
7. **Wait** — teammates auto-claim tasks via file locking, complete them, auto-claim next. They auto-message lead via mailbox when done.
   - **CRITICAL: Polling blocks mailbox.** If lead uses `sleep`, `Monitor`, or any polling mechanism, incoming mailbox messages from teammates cannot be delivered — creating DEADLOCK. Lead will never see completion message because it's busy polling.
   - **Lead's only action while waiting: DO NOTHING.** Do NOT poll, do NOT monitor, do NOT check files. Just yield and let system deliver teammate messages to your mailbox.
8. **Shutdown when idle** — when all tasks done and teammates go idle, send ONE structured shutdown request per teammate (see step 1 format). **After sending, YIELD IMMEDIATELY.** Wait for confirmations in next turn.

**Lead's only jobs: create tasks, spawn ALL new teammates in parallel, then yield and wait for mailbox. Never poll.**

**IMPORTANT: Order is critical — shutdown old FIRST, then create tasks, then spawn ALL new teammates in one parallel batch. Never create new team — always use team_name "book-pipeline".**

### Initial Team Creation (Phase 3 only)
`TeamCreate({ team_name: "book-pipeline", description: "Book publishing pipeline" })` — create ONCE.

### Shutdown Pattern (used by every phase)
Every phase ends with: **Wait for teammate idle notification → send ONE `shutdown_request` → wait for confirmation → proceed to next phase.** Refer to "Waiting Discipline" section above for full rules.

### Final Cleanup (Phase 11 only)
`TeamDelete({})` — delete ONCE at very end. **No parameters needed** — tool automatically targets current team. If it fails with "active members" error, some teammates still running; wait for their idle notifications, send shutdown_request to each, then retry `TeamDelete({})`.

### Prohibited Operations
- **NEVER** create second team — ONE team throughout pipeline
- **NEVER** manually edit or delete `~/.claude/teams/` or `~/.claude/tasks/` files
- **NEVER** fall back to subagents (`Agent` without `team_name`)
- **NEVER** use `sleep`, `sleep` loops, or `Monitor` to check teammate progress — teammates auto-message lead via mailbox on completion. Lead does NOT need to poll, wait on files, or monitor output. **Just wait for mailbox message.**
- **NEVER** poll for output files — if teammate has work to do, they will message you. Just wait.
- **NEVER** continue working after SendMessage to teammate — SendMessage is ALWAYS last action of turn. Yield immediately.
- **NEVER** rush shutdown — send ONE shutdown_request per teammate, then WAIT. System takes time to process after approval. Do NOT send repeated shutdowns. Do NOT do teammate's work yourself while waiting.

## Agent Teams Rules

**This pipeline uses Agent Teams, NOT subagents.** Each parallel batch spawns independent teammates that share task list and communicate directly.

### Core Constraints

1. **Team size MUST NOT exceed 6** — at any point, no more than 6 teammates active simultaneously. This is hard limit.
2. **Auto-shutdown on completion** — teammates that finish assigned tasks MUST shut down and exit immediately. Do not leave idle teammates running.
3. **Reviewer pattern: fixed 4, serial processing** — review phases (6a/6b/6c/7) use exactly 4 teammates maximum regardless of chapter count. Each teammate processes multiple chapters serially via shared task list: pick up next task → complete → pick up next → shut down when queue empty.
4. **Queue-based onboarding via config file** — when non-review phase requires more than 6 workers, do NOT split into batches manually. Pipeline (lead) responsible for queue management:
   - Write all pending teammate assignments to `.work/team-queue.md` with status (queued / onboarded / completed)
   - Spawn up to 6 teammates initially, mark them as "onboarded"
   - Monitor active teammates: when one completes and shuts down, mark it "completed" in queue, then spawn next "queued" teammate and mark it "onboarded"
   - Repeat until queue empty
   - Queue file format:
     ```markdown
     # Team Queue
     | # | Agent Type | Task | Status |
     |---|-----------|------|--------|
     | 1 | book-chapter-reviewer | Review ch01 | completed |
     | 2 | book-chapter-reviewer | Review ch02 | completed |
     | 7 | book-chapter-reviewer | Review ch07 | queued |
     ```
5. **Single team throughout** — create team "book-pipeline" at Phase 3. Between phases: shutdown old teammates → spawn new teammates with same team_name. Delete team only at Phase 11.
6. **Lead only coordinates** — pipeline (lead) delegates work, monitors progress, reports to user. All reading, writing, reviewing, proofreading done by teammates.
7. **NEVER fall back to subagents** — if teammate encounters error or is slow, do NOT replace it with subagent. Fix issue within team model or report to user.

---

## Parameter Parsing

Extract from user input:
- First argument not starting with `--` → repo URL or local path (required)
- `--title` → book title (optional; can also be AI-generated during topic-selection phase)
- `--subtitle` → subtitle (optional)
- `--audience` → target readers (optional, e.g. "Python developers", "Go backend engineers")
- `--focus` → key focus areas (optional, comma-separated)
- `--chapters` → suggested chapter count, default 16 (passed to Phase 2 topic selection as hint)
- `--book-dir` → book output directory, defaults to `<project-name>-book/`

If repo path missing, use AskUserQuestion to prompt user.

After determining `BOOK_DIR`:
```bash
# Check for existing book directory (re-entrancy check)
if [ -d "$BOOK_DIR/.work" ]; then
  echo "WARNING: Existing book directory found at $BOOK_DIR"
  echo "Previous intermediate files may be overwritten."
  # Ask user whether to clean up or continue
fi
mkdir -p "$BOOK_DIR" "$BOOK_DIR/.work"
```

---

## Pipeline Orchestration

Execute phases in order. After each phase completes, report to user and confirm before proceeding.

**IMPORTANT: Pipeline MUST continue to next phase after user confirmation. Do NOT stop prematurely.**

### Phase 1: Clone + Analyze

```
Input: repo URL or local path
Output: codebase metrics (language distribution, file count, LOC, directory structure, test coverage)
```

**IMPORTANT: Execute all steps SEQUENTIALLY. Do NOT run multiple Bash calls in parallel.**

1. If URL:
   - Derive repo directory name from URL (e.g., `https://github.com/user/repo` → `repo/`)
   - **Re-entrancy**: if directory already exists, skip `git clone` and use existing copy
   - If not, run `git clone <url>` (wait for it to complete)
   If local path, verify it exists with `ls`
2. **Detect language distribution** (polyglot):
   ```bash
   find . -type f \( -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.rb" -o -name "*.swift" -o -name "*.kt" -o -name "*.cs" \) | \
     sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
   ```
3. Gather metrics (replace `<ext>` with detected primary language):
   ```bash
   find . -type f -name "*.<ext>" | wc -l
   find . -type f -name "*.<ext>" -exec cat {} + | wc -l
   find . -type d \( -name "test*" -o -name "spec*" -o -name "__test*" \) | wc -l
   find . -type d -maxdepth 3 | grep -v node_modules | grep -v .git | sort
   du -sh .
   ```
4. Read README.md and entry-point files to understand architecture
5. Present analysis results to user; confirm before moving to topic selection

### Phase 2: Topic Selection

```
Input: codebase analysis results, user intent
Output: topic report (TOPIC.md)
```

**This is LEAD-ONLY phase. Do NOT create team. Do NOT spawn any teammates. You write TOPIC.md yourself.**

**Re-entrancy**: If `TOPIC.md` already exists from previous run, read it first and present it to user for confirmation instead of regenerating. Only regenerate if user explicitly requests changes.

1. **Early exit check**: if codebase very small (< 1K LOC, single file, or trivial project), recommend to user that this project may not warrant full technical book. Offer to continue anyway if user confirms.
2. Based on code analysis, generate topic report `TOPIC.md` containing:
   - **Project Positioning** — what project is and what problem it solves
   - **Technical Highlights** — 3-5 most noteworthy technical decisions or architectural designs
   - **Target Audience** — who will read this book and what prerequisites they need
   - **Writing Angle** — which lens to use (architecture analysis vs. usage guide vs. source-code walkthrough)
   - **Title Suggestions** — 3-5 candidate titles + subtitles
   - **Recommended Chapter Count** — 12-18 chapters (based on codebase complexity), respecting `--chapters` hint if provided
   - **What Not to Cover** — topics unsuitable for deep analysis
3. Present topic report to user
4. After user confirmation or edits, proceed to outline

### Phase 3: Outline

```
Input: TOPIC.md + codebase
Output: BOOK_PLAN.md + STYLE_GUIDE.md + EDITORIAL_PLAN.md
```

1. Create team `book-pipeline` with `TeamCreate({ team_name: "book-pipeline", description: "Book publishing pipeline" })`
2. Create task: "Analyze codebase, generate BOOK_PLAN.md (chapter outline with Theme field per chapter), STYLE_GUIDE.md (writing guide), and EDITORIAL_PLAN.md (pipeline plan)."
3. Spawn 1 **planner** teammate with `book-outline` mode, passing codebase path, TOPIC.md, `BOOK_DIR`, and `--chapters` hint.
4. Follow Shutdown Pattern (wait for idle → shutdown → confirm).
5. Present outline summary to user; confirm before moving to coordination.

### Phase 4: Pre-Writing Coordination (Critical — Prevents Style Fragmentation)

```
Input: BOOK_PLAN.md + STYLE_GUIDE.md
Output: DEPENDENCIES.md (chapter dependency graph + cross-reference conventions)
```

**Before Writers start in parallel, make sure they all know where their boundaries are.**

1. Create task: "Read BOOK_PLAN.md and STYLE_GUIDE.md, generate DEPENDENCIES.md with home chapter, cross-reference conventions, content boundaries, transition suggestions."
2. Spawn 1 **planner** teammate with `dependencies` mode.
3. Follow Shutdown Pattern (wait for idle → shutdown → confirm).

### Phase 4.5: Code Index (Token Budget Reduction)

```
Input: codebase + BOOK_PLAN.md
Output: CODE_INDEX.md (pre-computed code summary + call graph + architecture map)
```

**Writers and reviewers query this index instead of reading raw source — cuts token cost by 50%+.**

1. Create task: "Scan codebase, produce CODE_INDEX.md with module summary, call graph, data flow map, key constants, test inventory, architecture summary."
2. Spawn 1 **planner** teammate with `code-index` mode.
3. Follow Shutdown Pattern (wait for idle → shutdown → confirm).
4. Writers and reviewers query this index instead of reading raw source — cuts token cost by 50%+.

### Phase 5: First Draft Writing (Staged — Prevents Writer Drift)

```
Input: BOOK_PLAN.md + STYLE_GUIDE.md + DEPENDENCIES.md + CODE_INDEX.md
Output: chapter files `.work/chapters/chXX-*.md`
```

1. Create `.work/chapters/` directory for draft chapters
2. **Batch 1 (Foundation chapters)**:
   - Create task for foundation chapters with details from `BOOK_PLAN.md` (titles, descriptions, key files, chapter theme/lens), `DEPENDENCIES.md` (boundaries), `STYLE_GUIDE.md` (conventions), `CODE_INDEX.md` (code summaries)
   - Task description must include: "These are foundation chapters — focus on narrative clarity, project motivation, architectural overview, and why this codebase matters. Lower code density, higher readability. Set tone for entire book."
   - Spawn 1 **book-writer** teammate with prompt: "Write foundation chapters (first 2-3). These set book's tone — exemplary structure compliance required. Pick up task from shared task list. When done, shut down."
   - Follow Shutdown Pattern.
3. **Checkpoint**: Lead (YOU) manually reviews Batch 1 output for style/depth/tone alignment with STYLE_GUIDE.md. **Do NOT spawn reviewer for this.** This is quick visual check by lead — confirm chapter structure, Mermaid usage, decision box format, terminology, writing tone.
   - **After reviewing, present findings to user and ask for confirmation before proceeding to Batch 2.** If user approves, proceed. If issues found, list them and ask whether to fix before Batch 2 or proceed anyway.
4. **Batch 2 (All remaining chapters)**:
   - Create tasks — one per remaining chapter. Each task must include:
     - Chapter title, description, key files from `BOOK_PLAN.md`
     - Chapter theme/lens (from BOOK_PLAN.md or inferred): e.g., "core architecture deep dive", "subsystem internals", "engineering practices/production concerns"
     - Style guidance per chapter type:
       - Core architecture chapters: high code density, deep technical analysis, design decisions emphasized
       - Subsystem/tools chapters: practical focus, how components interact, extensibility patterns
       - Integration/deployment chapters: production concerns, operational realities, trade-offs
     - `DEPENDENCIES.md` boundaries, `STYLE_GUIDE.md` conventions, `CODE_INDEX.md` summaries
     - Path to Batch 1 output as style reference
   - **Spawn 3 book-writer teammates IN PARALLEL** (one parallel Agent call per teammate, all with same team_name). Each prompt: "Pick up available writing tasks. Write chapters according to STYLE_GUIDE.md conventions, adapting tone and code density to chapter's theme/lens as specified in task. Use Batch 1 output as style reference. When no tasks remain, shut down."
   - Each writer auto-claims, writes, auto-claims next — repeat until done
   - Follow Shutdown Pattern.
5. Collect results on completion; show progress to user

### Phase 6: Three Reviews

#### 6a. Initial Review (Per-Chapter Structure Check)

```
Input: all chapter files `.work/chapters/ch*.md` + STYLE_GUIDE.md
Output: `.work/review-chXX.md` (one per chapter)
```

1. Create tasks in shared task list — one task per chapter, with details: "Review chapter chXX for structural compliance per STYLE_GUIDE.md. Write report to `.work/review-chXX.md`."
2. Spawn 4 **book-chapter-reviewer** teammates (max 4 regardless of chapter count) with prompt: "Pick up available review tasks from shared task list. Review each chapter, write report to `.work/review-chXX.md`. When no tasks remain, shut down."
3. Each reviewer auto-claims, reviews, writes report, then auto-claims next one — repeat until all tasks done
4. Follow Shutdown Pattern.

#### 6b. Technical Review (Fact-Checking — Critical!)

```
Input: all chapter files `.work/chapters/ch*.md` + source repo + CODE_INDEX.md
Output: `.work/tech-review-chXX.md` (one per chapter)
```

**This is not format check — it is fact check. Verify whether code logic described in each chapter actually matches source code.**

1. Create tasks in shared task list — one task per chapter: "Fact-check chapter chXX against source code. Verify code citations, architecture descriptions, data accuracy. Write report to `.work/tech-review-chXX.md`."
2. Spawn 4 **book-technical-reviewer** teammates (max 4 regardless of chapter count) with prompt: "Pick up available technical review tasks. Verify claims against source code, run tests if available. Write report to `.work/tech-review-chXX.md`. When no tasks remain, shut down."
3. Each reviewer auto-claims, verifies, writes report, then auto-claims next one — repeat until all tasks done
4. Follow Shutdown Pattern.
5. Each reviewer checks:
   - **Code Logic** — does claimed behavior match actual code
   - **Architecture Description** — does described architecture match actual code structure
   - **Code Reference Context** — does code at `file:line` actually implement what chapter claims
   - **Data Accuracy** — are performance figures and numbers backed by evidence
   - **Design Decision Authenticity** — do described "alternatives" and "trade-offs" actually exist
6. **Automated test verification** (if tests exist):
   - Detect test framework from `CODE_INDEX.md` test inventory
   - Run relevant tests to verify behavioral claims using appropriate command for detected framework:
     | Framework | Command |
     |-----------|---------|
     | pytest | `pytest -v tests/ --tb=short 2>&1 \| head -50` |
     | unittest (Python) | `python -m unittest discover -v 2>&1 \| head -50` |
     | jest | `npx jest --verbose 2>&1 \| head -50` |
     | vitest | `npx vitest run 2>&1 \| head -50` |
     | go test | `go test ./... -v 2>&1 \| head -50` |
     | cargo test | `cargo test 2>&1 \| head -50` |
     | JUnit/Maven | `mvn test -q 2>&1 \| head -50` |
     | Gradle | `./gradlew test 2>&1 \| head -50` |
     | Other | Fall back to manual source verification |
   - If chapter claims "function X handles Y case correctly", verify test exists that covers it
   - If codebase has no tests, fall back to manual source verification

#### 6c. Cross-Chapter Review (Consistency)

```
Input: all `.work/chapters/ch*.md` + all `.work/review-chXX.md` + all `.work/tech-review-chXX.md` + STYLE_GUIDE.md
Output: `.work/review-consistency.md`
```

**To avoid context window explosion (18 chapters + all review reports = 100K+ tokens), split consistency review by Book Part:**

1. Read `BOOK_PLAN.md` to identify Parts (typically 4-5 Parts)
2. Create tasks in shared task list — one task per Part: "Review consistency of all chapters within Part N. Check terminology, content deduplication, data consistency, design decision contradictions, cross-reference accuracy. Write report to `.work/review-consistency-partN.md`."
3. Spawn up to 4 **book-consistency-reviewer** teammates (if fewer Parts than 4, spawn one per Part). **Spawn ALL in parallel.**
4. Each reviewer auto-claims Part, writes report, then auto-claims next Part if available — repeat until all Parts done
5. Follow Shutdown Pattern.
6. **Merge strategy**: Pipeline lead consolidates all `.work/review-consistency-partN.md` files into `.work/review-consistency.md`:
   - If same issue appears in multiple Parts → list once with "affects all Parts"
   - If Part-specific → list under that Part section
   - If contradictions between Parts → flag as P0
   - Include summary table: total issues by severity

#### 6d. Final Review (Overall Quality — Done by Pipeline Agent)

```
Input: all review reports (`.work/`) + all tech-review reports (`.work/`) + all chapters (`.work/chapters/`) + `.work/review-consistency.md`
Output: final review verdict written to `.work/final-review-verdict.md`
```

Pipeline agent synthesizes all review results and makes go/no-go decision:

1. Collect all initial review verdicts (`review-chXX.md`)
2. Collect all technical review verdicts (`tech-review-chXX.md`)
3. Read cross-chapter consistency report (`review-consistency.md`)
4. Tally PASS/FAIL counts and identify critical issues
5. Write verdict to `.work/final-review-verdict.md`
6. Judge:
   - Any technical review FAIL → requires rework
   - Any initial review FAIL → requires rework
   - Consistency report FAIL → requires rework
   - All PASS → ready for publication → proceed to Phase 8 (Verification)

### Phase 7: Rework

```
Input: review reports (`.work/`) + tech-review reports (`.work/`) + original chapter files (`.work/chapters/`)
Output: revised `.work/chapters/ch*.md` files
```

1. Read `BOOK_PLAN.md` to determine which chapters have FAIL verdicts
2. Create tasks in shared task list — one task per FAIL chapter with details: chapter title/description/key files from `BOOK_PLAN.md`, FAIL items from `review-chXX.md` (structural issues), FAIL items from `tech-review-chXX.md` (factual errors), STYLE_GUIDE.md for formatting. Note: fix factual errors first.
3. Spawn up to 4 **book-writer** teammates with prompt: "Pick up available rework tasks. Fix assigned chapters against actual source code. Write revised chapter to `.work/chapters/chXX-*.md`. When no tasks remain, shut down."
4. Each writer auto-claims, fixes, writes, then auto-claims next FAIL chapter — repeat until done
5. Follow Shutdown Pattern, then **re-run Phase 6a + Phase 6b** with new tasks and teammates.
6. Maximum 2 rework rounds; beyond that, report to user for decision

### Phase 8: Verification

```
Input: all chapter files `.work/chapters/ch*.md`
Output: `.work/verification-status.md`
```

1. **Check mmdc availability** (fail if not installed):
   ```bash
   which mmdc >/dev/null 2>&1 || echo "ERROR: mmdc not installed. Run: npm install -g @mermaid-js/mermaid-cli"
   ```
   - **If mmdc NOT available**: Report error to user. Pipeline cannot proceed without mmdc — Mermaid validation mandatory. Wait for user to install or confirm override.
   - **If mmdc IS available**: Proceed to spawn verifier.

2. Create task: "Run automated structure checks on all chapters. Validate Mermaid syntax using mmdc (authoritative). Write `.work/verification-status.md`."

3. Spawn 1 **book-verifier** teammate. Follow Shutdown Pattern.

4. Display verification results table. If any FAILs, list issues, get user confirmation, then proceed to proofreading.

### Phase 9: Three Proofreads + Preface (Parallel)

```
Input: all chapter files `.work/chapters/ch*.md` + STYLE_GUIDE.md + TOPIC.md + BOOK_PLAN.md
Output: `.work/proofread-1.md` + `.work/proofread-2.md` + `.work/proofread-3.md` + `preface.md`
```

**4 different teammates, 4 different tasks — spawn each explicitly with mode, do NOT use auto-claim for this phase.**

1. Spawn 4 teammates **IN PARALLEL** with explicit mode instructions:
   - **proofreader**: prompt = "Execute `book-first` mode only: text proofreading (typos, punctuation, terminology, Mermaid syntax). Write `.work/proofread-1.md`."
   - **proofreader**: prompt = "Execute `book-second` mode only: cross-reference validation (cross-references, content overlap, design decision consistency). Write `.work/proofread-2.md`."
   - **proofreader**: prompt = "Execute `book-readability` mode only: read-through (transitions, narrative coherence, pacing, tone). Write `.work/proofread-3.md`."
   - **book-preface-writer**: prompt = "Write `preface.md` based on TOPIC.md, BOOK_PLAN.md, STYLE_GUIDE.md. 1-2 pages, no Mermaid, no code citations."
2. All 4 work in parallel. Follow Shutdown Pattern for each.
3. Report to user when all complete

### Phase 9.5: Preface Review

```
Input: preface.md + TOPIC.md + BOOK_PLAN.md + STYLE_GUIDE.md
Output: `.work/preface-review.md`
```

Preface is first thing readers see — review it before incorporation:

1. Create task: "Review `preface.md` against TOPIC.md, BOOK_PLAN.md, and STYLE_GUIDE.md. Check: accuracy (matches TOPIC.md?), tone (analytical, 'we', not tutorial?), scope (intro without technical detail?), structure (motivation, audience, usage?), length (1-2 pages, no Mermaid, no code citations), factual claims. Write `.work/preface-review.md`."
2. Spawn 1 **book-chapter-reviewer** teammate. Follow Shutdown Pattern.
3. **Verdict handling**:
   - **PASS**: Proceed to Phase 10
   - **FAIL**:
     1. List issues to user.
     2. **Spawn 1 book-preface-writer teammate** with task: "Rewrite `preface.md` fixing: [list issues from preface-review report]." Follow Shutdown Pattern.
     3. Re-run Phase 9.5 (preface review) on rewritten preface.
     4. **Maximum 1 rewrite** — if Phase 9.5 still FAILs, present issues to user for manual intervention.

### Phase 10: Synthesis (Chunked Processing)

```
Input: all `.work/chapters/ch*.md` + preface.md + `.work/final-review-verdict.md` + three review reports (`.work/`) + proofread reports (`.work/`) + `.work/preface-review.md` + STYLE_GUIDE.md + CODE_INDEX.md
Output: fixed chapters + fixed preface + 4 appendices + book-final.md
```

**To avoid context-window saturation, process in sequential passes. Shutdown old teammates, spawn new ones for each pass.**

1. **Pass 1: P0 Fixes** — create task: "Fix P0 issues: decision-box formatting, ASCII art replacement, missing structure completion." Spawn 1 **book-editor-in-chief** teammate with `p0-fix` mode. Follow Shutdown Pattern.
2. **Pass 2: P1 Fixes** — create task: "Fix P1 issues: content deduplication, cross-reference correction, data consistency." Spawn 1 **book-editor-in-chief** with `p1-fix` mode. Follow Shutdown Pattern.
3. **Pass 3: P2 Fixes** — create task: "Fix P2 issues: terminology unification, difficulty buffering, transitions." Spawn 1 **book-editor-in-chief** with `p2-fixes` mode. Follow Shutdown Pattern.
4. **Pass 4: Appendix Writing** — create task: "Write 4 appendix files: appendix-A (file index), appendix-B (tool reference), appendix-C (design decisions), appendix-D (glossary)." Spawn 1 **book-editor-in-chief** with `write-appendices` mode. Follow Shutdown Pattern.
5. **Pass 5: Final Compilation** — create task: "Read all fixed chapters + 4 appendices + preface, compile `book-final.md`." Spawn 1 **book-editor-in-chief** with `compile-final` mode. Follow Shutdown Pattern.
6. Present synthesis results to user (fix counts, final word count)

### Phase 10.5: Final Review (Quality Gate — Before Delivery)

```
Input: book-final.md
Output: `.work/final-review.md` (final verdict: PASS/FAIL)
```

**Last human-readable quality gate. Catches ASCII art residue, missing sections, broken cross-references, Mermaid errors in compiled manuscript.**

1. Create task: "Review `book-final.md`: ASCII art residue (grep for box-drawing chars), structural completeness (metaphor, Mermaid, reflection questions, principles per chapter), decision box format (blockquote only), Mermaid syntax validation, cross-reference integrity, overall quality (word count anomalies, TODOs). Write `.work/final-review.md` with PASS/FAIL verdict."
2. Spawn 1 **book-final-reviewer** teammate. Follow Shutdown Pattern.
3. **Verdict handling**:
   - **PASS**: Proceed to Phase 10.6 (External Review)
   - **FAIL**:
     1. List all blockers to user with severity ratings (P0/P1/P2).
     2. **Fixable issues** → route back to appropriate Phase 10 pass:
        - ASCII art, decision box format, missing structure → re-run Phase 10 Pass 1 (P0 fixes)
        - Content overlap, cross-refs, data consistency → re-run Phase 10 Pass 2 (P1 fixes)
        - Terminology, transitions → re-run Phase 10 Pass 3 (P2 fixes)
     3. **After fix pass completes, you MUST also re-run remaining Phase 10 passes in sequence**:
        - If you ran Pass 1: also run Pass 2 → Pass 3 → Pass 4 → Pass 5 (compile-final)
        - If you ran Pass 2: also run Pass 3 → Pass 4 → Pass 5 (compile-final)
        - If you ran Pass 3: also run Pass 4 → Pass 5 (compile-final)
     4. After Pass 5 regenerates `book-final.md`, re-run Phase 10.5 (final review).
     5. **Maximum 1 re-fix round** — if Phase 10.5 still FAILs, present issues to user for manual intervention.

### Phase 10.6: External Review (Compilation Integrity — Loop)

```
Input: book-final.md + BOOK_PLAN.md
Output: `.work/external-review.md` (compilation integrity verdict: PASS/FAIL)
```

**After Phase 10.5 quality gate passes, this phase checks compiled book as complete publication — not per-chapter quality, but whole-book integrity.**

1. Create task: "Review `book-final.md` as complete compiled manuscript against `BOOK_PLAN.md`. Check:
   - **Chapter completeness**: All chapters from BOOK_PLAN.md present, none missing
   - **Chapter order**: Chapters appear in correct sequence (ch01 → ch02 → ... → chN)
   - **No duplicates**: No chapter appears twice in manuscript
   - **No empty sections**: Every chapter has content (not just headings or placeholders)
   - **Format consistency**: Heading levels uniform across chapters, numbering sequential
   - **Layout consistency**: Spacing, separator lines (---), section breaks uniform
   - **Preface placement**: Preface appears before table of contents
   - **Appendix placement**: All 4 appendices (A-D) appear after main content
   - **Table of contents accuracy**: TOC matches actual chapter headings
   Write `.work/external-review.md` with PASS/FAIL verdict."
2. Spawn 1 **book-chapter-reviewer** teammate. Follow Shutdown Pattern.
3. **Verdict handling**:
   - **PASS**: Proceed to Phase 11 (Delivery)
   - **FAIL**:
     1. List all compilation issues to user.
     2. **Route back to Phase 10 Pass 5 (compile-final)** to regenerate `book-final.md` with corrections. Lead provides external review report as input so editor-in-chief knows what to fix.
     3. **After re-compile, re-run full review chain**: Phase 10.5 (final review) → Phase 10.6 (external review). Both must PASS before proceeding to delivery.
     4. **Maximum 1 loop** — if Phase 10.6 still FAILs after one re-compile cycle, present issues to user for manual intervention.

### Phase 11: Delivery

1. Show final draft statistics (`wc -l`, `wc -c`, chapter count)
2. Deliver final draft files to user:
   - List all deliverable file paths:
     - `book-final.md` (in `BOOK_DIR/`)
     - `preface.md` (in `BOOK_DIR/`)
     - `appendix-A.md` through `appendix-D.md` (in `BOOK_DIR/`)
   - Display summary of what was produced and where to find each file
3. Display pipeline execution summary

---

## Failure Handling Principles

- **Topic Selection** → project unsuitable for book (too small, too simple, insufficient docs); explain to user
- **Outline** → analysis insufficient; request more information
- **Review FAIL** → rework, max 2 rounds
- **Verification FAIL** → list specific issues; continue after user confirmation
- **Final Review (Phase 10.5) FAIL** → route back to appropriate Phase 10 pass; max 1 re-fix round; if still FAIL, present to user
- **External Review (Phase 10.6) FAIL** → route back to Phase 10 Pass 5 (compile-final); max 1 loop; if still FAIL, present to user
- **Synthesis** → record all P0/P1/P2 fixes; display in final report

## Progress Reporting

After each phase completes, output:
```
✅ Phase N: [Phase Name] — Complete
  - [Key Output 1]
  - [Key Output 2]
  - [Duration / File Count / Other Metrics]
```

When entire pipeline finishes, output full summary.
