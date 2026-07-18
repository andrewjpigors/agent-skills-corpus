---
name: code-review
description: "Performs a read-only architectural and quality code review on a specified file or bounded set of files. Checks correctness, architecture conformance, maintainability, performance, testability, security/privacy risk, rule compliance, and implementation risk without modifying project state."
argument-hint: "[path-to-file-or-directory] [--review full|lean|solo] [--no-bash]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task
agent: lead-programmer
---

# Code Review Skill

## Skill Name

code-review

## Mission

Perform a repository-local, read-only code review that identifies correctness defects, architecture drift, rule violations, maintainability risks, testability gaps, performance hazards, security/privacy issues, and implementation risks.

This skill must never modify files or project state.

The core review question is:

> Does this code safely implement its intended behavior, comply with project architecture and path-scoped rules, remain testable and maintainable, and avoid unacceptable performance, security, and reliability risks?

---

## Operating Principles

1. **Read-only means read-only**
   - Do not create, edit, move, delete, rename, stage, commit, tag, deploy, publish, or update project state.
   - Do not run commands that modify files, snapshots, caches, generated reports, dependencies, build artifacts, databases, scenes, assets, or local config.

2. **Evidence first**
   - Every conclusion must cite or name a repository source, diagnostic result, or explicitly state that it is an inference.
   - Do not claim tests, builds, linters, profilers, or formatters passed unless the diagnostic actually ran and evidence is available.

3. **Review the smallest useful scope**
   - Review the requested file or bounded directory.
   - Read only neighboring files, design docs, ADRs, tests, and rules needed to understand contracts and risks.
   - If the requested directory is too broad, review a representative subset and state the limitation.

4. **Architecture and design compliance matter**
   - Compare code against governing ADRs, architecture manifests, GDDs, path-scoped rules, and relevant tests.
   - Code may compile and still fail review if it violates architecture or design contracts.

5. **Severity must reflect risk**
   - Blocking issues prevent safe implementation, review, release, or downstream workflow.
   - High issues are likely to cause defects, rework, invalid QA, security risk, or architecture drift.
   - Medium issues weaken quality or handoff.
   - Low issues are cleanup, clarity, or optional improvements.

6. **Recommendations are not patches**
   - Provide patch direction, not file edits.
   - Do not imply that files were changed.
   - If a durable patch/report is needed, recommend the appropriate write-capable skill or agent.

7. **Bash is diagnostic only**
   - Bash may run safe read-only commands only.
   - Any command with possible mutation requires refusal within this skill.

8. **Subagents are bounded reviewers**
   - Use `Task` only when domain review materially improves the result.
   - Pass bounded context and request a precise verdict.
   - Do not spawn duplicate reviewers.

9. **Partial reviews are valid only when labeled**
   - If context, files, tools, or diagnostics are unavailable, state the review is partial.
   - Do not overclaim coverage.

10. **Self-healing before final report**
    - If a file is missing, scope is too broad, diagnostics fail, sources conflict, or review confidence is low, classify the problem, narrow scope where safe, and report uncertainty.

11. **Bounded self-learning**
    - Lessons from repeated findings, user corrections, CI/test failures, architecture drift, or false positives may be proposed only as reviewable lessons.
    - This skill itself does not write lessons because it has no write tools.

---

## Scope

This skill may review:

- source files,
- test files,
- configuration files,
- data files,
- scripts,
- build files,
- tool files,
- path-scoped rule files,
- architecture documents needed for compliance,
- GDD/design files needed for traceability,
- neighboring files needed to understand interfaces.

This skill may not modify any of them.

---

## Non-Goals

This skill must not:

- edit code,
- create reports on disk,
- update tests,
- update snapshots,
- update registries,
- update stories,
- update status files,
- run mutating commands,
- install dependencies,
- run destructive cleanup,
- run deployment or publishing commands,
- approve final release readiness,
- make architecture decisions that require ADR/Technical Director approval,
- claim full validation from partial evidence,
- store persistent memory or lessons directly.

---

## Invocation Modes

Supported invocations:

```text
/code-review path/to/file
/code-review path/to/directory
/code-review path/to/file --review full
/code-review path/to/file --review lean
/code-review path/to/file --review solo
/code-review path/to/file --no-bash
```

If no path is provided:

```text
Stop and request a repository-relative path.
```

Do not guess a path.

---

## Review Modes

Resolve review mode once:

1. Explicit `--review full|lean|solo`.
2. Else read `production/review-mode.txt` if present.
3. Else default to `lean`.

If the review-mode file is missing, malformed, or empty:

```text
Default to lean and report the assumption once.
```

### Review Mode Semantics

| Mode | Behavior |
|---|---|
| `solo` | No subagents. Main reviewer only. |
| `lean` | Use at most one essential specialist if the domain clearly benefits. |
| `full` | Use relevant specialist review for high-risk or cross-domain code. |

### `--no-bash`

If `--no-bash` is present:

- Do not call Bash.
- Use `Read`, `Glob`, `Grep`, and `Task` only.
- Report diagnostics as not run.

---

## Path Safety

All user-supplied paths must be repository-relative.

Reject:

- absolute paths,
- paths containing `..`,
- paths outside expected project roots,
- paths that normalize outside the repository,
- symlink-like or shell-expanded paths if safety cannot be established.

Expected roots include, but are not limited to:

```text
src/
Assets/
tests/
design/
docs/
assets/
production/
tools/
scripts/
.claude/
```

If unsafe:

```text
Path rejected: [reason]
```

Do not read or run diagnostics on unsafe paths.

---

## Read-Only Bash Safety

### Always Prohibited

Never run:

```text
rm
mv
cp
touch
mkdir
rmdir
git add
git commit
git tag
git push
git reset
git clean
git checkout
git switch
git restore
npm install
pnpm install
yarn install
pip install
dotnet add
dotnet restore
cargo build
cargo update
scons
make install
deploy
publish
upload
build upload
snapshot update
```

Also prohibit commands that:

- write files,
- update snapshots,
- generate reports into the repository,
- mutate databases,
- mutate test fixtures,
- modify scenes/assets,
- install or update dependencies,
- contact production services,
- deploy or publish artifacts.

### Safe Diagnostic Examples

Allowed when local and obviously read-only:

```text
git status --short
git log --oneline -n 20
git diff --name-only
git diff -- path/to/file
grep / rg searches
find/list commands
cat/head/tail/sed read-only views
test discovery commands that do not execute or write
```

### Conditionally Safe

Only run if clearly non-mutating in this project:

- existing lint commands,
- existing test commands,
- type-check commands,
- static-analysis commands.

Before running, inspect or infer whether they write:

- snapshots,
- coverage files,
- cache files,
- generated artifacts,
- reports,
- temp files inside repo,
- fixture updates.

If uncertain, do not run.

### Bash Command Record

Every Bash command run must be listed:

```md
## Bash Diagnostics

| Command | Purpose | Read-only? | Result |
|---|---|---:|---|
```

---

## Review Lifecycle State Labels

Use these states internally and in the report where helpful:

```text
INVOCATION_PARSED
PATH_VALIDATED
PATH_REJECTED
SCOPE_BOUNDED
SCOPE_TOO_BROAD
PRIMARY_SOURCE_READ
PRIMARY_SOURCE_MISSING
CONTEXT_DISCOVERED
CONTEXT_PARTIAL
RULES_DISCOVERED
ARCHITECTURE_DISCOVERED
GDD_DISCOVERED
TESTS_DISCOVERED
DIAGNOSTICS_NOT_RUN
DIAGNOSTICS_RUN
DIAGNOSTICS_FAILED
SUBAGENT_NOT_USED
SUBAGENT_REQUESTED
SUBAGENT_COMPLETE
SUBAGENT_FAILED
FINDINGS_DRAFTED
EVIDENCE_CHECKED
REPORT_COMPLETE
BLOCKED
UNKNOWN
```

### State Rules

- Do not mark `CONTEXT_DISCOVERED` when only the requested file was read but dependencies are unknown.
- Do not mark `DIAGNOSTICS_RUN` unless at least one safe diagnostic ran.
- Do not mark `SUBAGENT_COMPLETE` if Task failed or returned no usable verdict.
- Do not mark `REPORT_COMPLETE` until evidence and no-write validation are checked.

---

## Evidence and Confidence Taxonomy

### Evidence Types

```text
DIRECT_CODE_EVIDENCE — exact file/line or source excerpt.
DIRECT_TEST_EVIDENCE — test file or diagnostic result.
ARCHITECTURE_EVIDENCE — ADR, registry, manifest, architecture doc.
DESIGN_EVIDENCE — GDD or design doc.
RULE_EVIDENCE — path-scoped rule or governance file.
DIAGNOSTIC_EVIDENCE — safe Bash output.
SUBAGENT_EVIDENCE — Task verdict.
INFERENCE — reasoned conclusion from available evidence.
UNKNOWN — insufficient evidence.
```

### Confidence Levels

```text
HIGH — direct source or diagnostic evidence.
MEDIUM — strong inference from multiple sources.
LOW — limited evidence or partial context.
UNKNOWN — cannot determine.
```

Every finding should include an evidence type and confidence.

---

## Discovery Strategy

### Primary Sources

Read the requested path first.

Then discover only what is necessary:

```text
neighboring files needed to understand imports/contracts
docs/architecture/control-manifest.md
docs/architecture/adr-*.md
docs/registry/architecture.yaml
design/gdd/**
tests/**
path-scoped rules relevant to the requested file
```

### Discovery Rules

1. Prefer canonical source-of-truth files over generated reports.
2. Use `Glob` and `Grep` before reading large documents.
3. Keep a source list for the final report.
4. When many files match, read the most relevant 5–10 first.
5. Summarize unread candidates as potential additional context.
6. Treat missing or draft-status dependencies as gaps or blockers.
7. Do not invent missing contracts, design intent, or architecture decisions.

---

## Directory Review Scope

When reviewing a directory:

1. Count files by type.
2. Identify high-risk files first:
   - entry points,
   - public APIs,
   - stateful systems,
   - files with recent changes if `git diff` is available,
   - files matching path-scoped rules,
   - files with tests,
   - files without tests,
   - files with network/save/security/player-input behavior.
3. Read up to a bounded subset first.
4. State if the review is sampling-based.

### Directory Scope Record

```md
## Directory Scope

- Requested directory:
- Files found:
- Files reviewed:
- Files not reviewed:
- Selection rationale:
- Coverage:
  - Complete
  - Representative
  - Partial
```

If the directory is too broad for a meaningful review, use the smallest evidence-backed subset and report the limitation.

---

## Working Model

Before producing findings, build a concise working model:

```md
## Working Model

- Reviewed target:
- System/domain:
- Intended behavior:
- Key dependencies:
- Governing rules:
- Governing ADRs:
- Governing GDDs:
- Tests found:
- Diagnostics run:
- Review confidence:
```

Do not expose this section unless useful for transparency in the final report.

---

## Domain Classification

Classify the reviewed code by domain when possible:

```text
Gameplay
Engine/Core
AI
LLM Dialogue
Network
Netcode Security
Save/Persistence
UI
Data/Config
Tests
Tools
DevOps/Build
Audio
Analytics/Telemetry
Prototype
Architecture/Docs
Unknown
```

Apply relevant path-scoped rules when a domain is identified.

### Domain Review Triggers

| Domain | Extra Review Focus |
|---|---|
| Gameplay | data-driven values, delta time, UI decoupling, interfaces, tests |
| Engine/Core | hot-path allocations, dependency direction, public API stability, cleanup |
| AI | 2ms budget, data-driven params, debug hooks, telegraphing |
| Network | authority, message versioning, rollback, bandwidth, validation |
| Netcode Security | client trust, rate limits, anti-cheat, audit logs |
| Save/Persistence | HMAC, version-first load, migrations, fixture saves |
| UI | localization, focus, input parity, accessibility, non-blocking |
| Data/Config | JSON validity, schema, naming, references, defaults |
| Tests | naming, AAA, isolation, cleanup, regression, thresholds |
| Prototype | isolation, README, findings, no production import |
| Analytics | privacy, event purpose, opt-out, PII avoidance |
| Tools | undoability, atomic operations, clear errors, non-corruption |

---

## Subagent Delegation

Use `Task` only when it materially improves the review.

### Suggested Routing

| Domain | Possible Specialist |
|---|---|
| Unity-specific code | `unity-specialist` |
| Godot-specific code | `godot-specialist` |
| Unreal-specific code | `unreal-specialist` |
| Networking | `network-programmer` or security specialist |
| Save/security/privacy | `security-engineer` |
| Performance hotspot | `performance-analyst` |
| UI | `ui-programmer`, `ux-designer`, or accessibility specialist |
| AI | `ai-programmer` |
| Tests/QA | `qa-lead` or `qa-tester` |
| Build/CI | `devops-engineer` |

### Subagent Request Format

Pass:

```md
- User request:
- Review target:
- Files read:
- Relevant excerpts or summary:
- Governing rules:
- Specific verdict needed:
- Do not modify files.
```

### Subagent Verdict Handling

Accepted verdict tokens:

```text
PASS
PASS_WITH_NOTES
CONCERNS
BLOCKED
UNKNOWN
```

If subagent output is malformed:

- summarize useful observations,
- mark verdict `UNKNOWN`,
- do not claim approval.

---

## Review Checklist

### Correctness

Check:

- off-by-one errors,
- null/missing state handling,
- invalid input handling,
- error paths,
- state transitions,
- resource cleanup,
- exception/failure behavior,
- idempotency where repeated calls are possible,
- ordering assumptions,
- concurrency/race risks,
- initialization/lifecycle behavior.

### Architecture

Check:

- dependency direction,
- interface boundaries,
- ADR compliance,
- registry compliance,
- path-scoped rules,
- single responsibility,
- hidden coupling,
- global/static state,
- direct cross-layer references,
- public API stability,
- separation of logic and presentation.

### Maintainability

Check:

- method size and complexity,
- naming clarity,
- duplicated logic,
- comments/doc comments,
- data/control flow clarity,
- extensibility,
- code locality,
- unnecessary abstractions,
- missing invariants.

### Testability

Check:

- unit-testable logic,
- dependency injection,
- deterministic behavior,
- clock/RNG control,
- filesystem/network/database isolation,
- test coverage for edge cases,
- regression tests for bug fixes,
- integration tests where needed.

### Performance

Check:

- hot-path allocations,
- per-frame work,
- blocking calls,
- unnecessary queries,
- repeated expensive operations,
- caching/pooling,
- algorithmic complexity,
- bandwidth/memory/frame-time budgets,
- profiling evidence.

### Security and Privacy

Check:

- untrusted input validation,
- client trust,
- file deserialization,
- save tampering,
- secrets in code/logs,
- raw private data in logs,
- PII collection,
- rate limits,
- audit/log redaction,
- injection risks,
- LLM prompt/output safety when relevant.

### Accessibility and UX

For UI/player-facing code, check:

- localization,
- keyboard/mouse and gamepad support,
- focus handling,
- scalable text,
- colorblind safety,
- reduced motion,
- non-blocking UI behavior.

---

## Finding Schema

Every finding should use:

```md
### [Severity] [Short Finding Title]

- **Evidence**: [file/path, function, command result, doc, or inference]
- **Evidence Type**: [DIRECT_CODE_EVIDENCE | DIRECT_TEST_EVIDENCE | ...]
- **Confidence**: [HIGH | MEDIUM | LOW | UNKNOWN]
- **Impact**: [what can break or degrade]
- **Recommendation**: [specific patch direction]
- **Owner**: [likely owner/domain]
```

### Severity Definitions

```text
BLOCKING
Prevents safe implementation, review, release, or downstream skill execution. Must be resolved before acceptance.

HIGH
Likely to cause defects, rework, invalid QA, architecture drift, security/privacy risk, or serious maintainability problems.

MEDIUM
Weakens maintainability, testability, handoff quality, performance confidence, or design traceability.

LOW
Cleanup, clarity, polish, naming, documentation, or optional improvement.
```

---

## Test Evidence Policy

### Test Evidence Categories

```text
TESTS_FOUND — tests exist but were not run.
TESTS_NOT_FOUND — no relevant tests found.
TESTS_RUN_PASS — tests ran and passed.
TESTS_RUN_FAIL — tests ran and failed.
TESTS_NOT_RUN — no execution attempted.
TESTS_UNSAFE_TO_RUN — command may mutate state or environment.
TESTS_BLOCKED — test command missing or environment unavailable.
```

### Test Evidence Record

```md
## Tests Reviewed / Run

| Test / Command | Type | Status | Evidence |
|---|---|---|---|
```

Rules:

- A test file existing is not proof of passing.
- A local pass is not CI pass.
- A diagnostic failure is evidence, not noise.
- If tests were unsafe to run, say why.
- Do not recommend “ship” from unrun tests.

---

## Architecture / GDD Compliance Record

Use:

```md
## Architecture / GDD Compliance

| Source | Requirement | Observed Code Behavior | Status |
|---|---|---|---|
```

Statuses:

```text
COMPLIANT
NON_COMPLIANT
PARTIAL
UNKNOWN
NOT_APPLICABLE
```

If no governing source was found, state:

```text
No governing ADR/GDD found in reviewed scope.
```

Do not treat absence of a governing source as compliance.

---

## Diagnostic Failure Handling

If a diagnostic command fails:

1. Record the command.
2. Record the failure.
3. Determine whether the failure is:
   - review-relevant,
   - environment-related,
   - command-selection error,
   - expected because dependencies are missing.
4. Do not retry repeatedly.
5. Do not run mutating repair commands.
6. Report the diagnostic status.

---

## Read-Only Report Format

Return the report in chat.

Do not write files.

Use this structure:

```md
# Code Review: [target]

## Verdict

PASS | PASS_WITH_NOTES | NEEDS_FIX | BLOCKED | UNKNOWN

## Scope

- Requested path:
- Files reviewed:
- Files not reviewed:
- Review mode:
- Bash:
- Subagents:
- Confidence:

## Blocking Issues

[Findings or "None found in reviewed scope."]

## High-Priority Issues

[Findings or "None found in reviewed scope."]

## Medium / Low Issues

[Findings or "None found in reviewed scope."]

## Tests Reviewed / Run

| Test / Command | Type | Status | Evidence |
|---|---|---|---|

## Architecture / GDD Compliance

| Source | Requirement | Observed Code Behavior | Status |
|---|---|---|---|

## Performance / Security / Accessibility Notes

[Only include relevant domains.]

## Bash Diagnostics

| Command | Purpose | Read-only? | Result |
|---|---|---:|---|

## Subagent Verdicts

[Summaries or "No subagents used."]

## Recommended Patch Direction

[Prioritized, concrete, read-only guidance.]

## Evidence Sources

- [path or command]
```

### Verdict Rules

```text
PASS
No blocking/high issues found, tests/diagnostics adequate for requested scope, and architecture/design compliance is acceptable.

PASS_WITH_NOTES
No blocking/high issues found, but there are medium/low issues, partial context, or unrun diagnostics.

NEEDS_FIX
High or medium issues need correction before acceptance, but no blocker prevents continued work.

BLOCKED
Blocking issue, missing primary source, unsafe path, critical architecture/security violation, or insufficient evidence for safe review.

UNKNOWN
Review could not determine safety due to missing context, failed discovery, unavailable diagnostics, or overly broad scope.
```

---

## Self-Learning Protocol

Self-learning means controlled improvement from recurring code-review findings, user corrections, false positives, architecture drift, test failures, diagnostic issues, and post-review outcomes.

This skill is read-only. It may propose lessons but must not write them.

### What May Be Learned

The review process may learn:

- recurring rule violations,
- recurring architecture drift patterns,
- common false-positive patterns,
- domain-specific review heuristics,
- testability gaps,
- performance anti-patterns,
- security/privacy review triggers,
- useful diagnostics,
- unsafe diagnostics to avoid,
- better evidence requirements,
- rejected review approaches.

### What Must Not Be Learned or Stored

Do not store:

- private user data,
- private chain-of-thought,
- secrets,
- credentials,
- sensitive logs,
- raw private player data,
- one-off style preferences as universal rules,
- unapproved architecture assumptions,
- unverified diagnostic results as truth,
- temporary exceptions as permanent policy.

### Lesson Classification

Use:

```text
Confirmed Rule
Approved Review Standard
Correctness Finding
Architecture Finding
GDD Compliance Finding
Testability Finding
Performance Finding
Security Finding
Privacy Finding
Accessibility Finding
Diagnostic Finding
False Positive Finding
Subagent Review Finding
Rejected Approach
Working Assumption
Temporary Context
Superseded
```

### Lesson Proposal Format

Since this skill cannot write files, propose durable lessons like this:

```md
## Proposed Lesson

- Classification:
- Applies to:
- Lesson:
- Evidence:
- Suggested storage:
- Review trigger:
```

Recommended storage locations for a write-capable follow-up:

```text
docs/code-review/review-standards.md
docs/code-review/known-findings.md
docs/testing/test-standards.md
docs/architecture/adr-authoring-standards.md
tasks/lessons.md
production/session-state/lessons.md
```

### Lesson Validation Rules

A lesson is valid only if:

- it is specific,
- it is evidence-backed or user-approved,
- it does not include sensitive data,
- it is not overgeneralized,
- it does not conflict with active rules or accepted ADRs,
- it has a review trigger if it may expire.

### Lesson Expiry

Review or expire lessons when:

- architecture changes,
- engine version changes,
- rule files change,
- tests change,
- review process changes,
- false-positive evidence appears,
- Technical Director or Lead Programmer supersedes it,
- the lesson was temporary,
- the lesson is too broad.

---

## Self-Healing Protocol

Self-healing means detecting a review workflow failure, containing risk, repairing safely, and reporting remaining uncertainty without modifying project state.

### Failure Types

Monitor for:

- no path provided,
- unsafe path,
- primary source missing,
- scope too broad,
- missing governing docs,
- contradictory sources,
- diagnostic command unsafe,
- diagnostic command failed,
- subagent failed,
- evidence missing,
- test status overclaim risk,
- architecture compliance unknown,
- review confidence too low.

### Recovery Loop

When failure occurs:

1. **Stop**
   - Do not produce a confident verdict from unsafe or insufficient evidence.

2. **Identify**
   - State the exact workflow failure.

3. **Classify**
   - Path, source, scope, diagnostic, subagent, evidence, architecture, or test issue.

4. **Contain**
   - Mark status:
     - `BLOCKED`,
     - `UNKNOWN`,
     - `PARTIAL`,
     - `TESTS_NOT_RUN`,
     - `DIAGNOSTICS_FAILED`.

5. **Recover**
   - request a path,
   - reject unsafe path,
   - narrow scope,
   - read neighboring source,
   - skip unsafe diagnostic,
   - use read-only search instead of Bash,
   - mark subagent unavailable,
   - downgrade confidence,
   - recommend follow-up.

6. **Verify**
   - Re-check no writes occurred.
   - Re-check findings have evidence.
   - Re-check commands were read-only.

7. **Report**
   - State what was reviewed, what was not, and what remains uncertain.

8. **Learn**
   - Propose a durable lesson only if useful and evidence-backed.

---

## Error Recovery

### No Path Provided

Stop and ask:

```text
What repository-relative file or directory should I review?
```

### Unsafe Path

Reject and do not read.

```text
Path rejected: [reason]
```

### Missing Primary Source

If the requested path does not exist:

- stop unless a narrower safe scope can be inferred,
- report the missing file/folder exactly.

### Scope Too Broad

If a directory has too many files:

- review a bounded subset,
- prioritize high-risk files,
- state the review is partial,
- recommend a narrower follow-up review.

### Missing Governing Docs

If ADR/GDD/rule docs are missing:

- continue code review if primary code exists,
- mark architecture/GDD compliance as `UNKNOWN` or `NOT_APPLICABLE`,
- do not infer approval.

### Contradictory Sources

If sources disagree:

- prefer explicit source-of-truth/status docs,
- list the contradiction,
- mark compliance uncertain or blocked depending on severity.

### Unsafe Diagnostic

If a command may mutate state:

- do not run it,
- mark diagnostic `UNSAFE_TO_RUN`,
- recommend a safer command or CI check.

### Diagnostic Failure

If a diagnostic fails:

- record failure,
- do not run mutating repair,
- include failure in report,
- avoid overclaiming.

### Subagent Failure

If Task fails or returns unusable output:

- mark subagent verdict `UNKNOWN`,
- do not claim specialist review,
- continue only if main review can proceed with disclosed uncertainty.

### Evidence Missing

If a finding is plausible but unsupported:

- mark as inference,
- lower confidence,
- avoid using it as a blocker unless risk is severe.

---

## Memory Policy

### Short-Term Task Memory

Track during current review:

- requested path,
- normalized path,
- files reviewed,
- files skipped,
- domain classification,
- governing rules,
- ADR/GDD sources,
- tests found,
- diagnostics run,
- findings,
- confidence,
- unresolved gaps.

Short-term task memory expires after the review unless explicitly converted into a proposed lesson.

### Project Memory

This read-only skill may recommend storing:

- recurring review findings,
- domain review heuristics,
- diagnostic safety lessons,
- false-positive lessons,
- architecture drift lessons,
- testability lessons.

It must not write them directly.

### Never Store

Never store:

- secrets,
- credentials,
- private user/player data,
- private chain-of-thought,
- sensitive logs,
- raw private payloads,
- unsupported claims,
- one-off subjective preferences as standards.

---

## Feedback Policy

When the user, Lead Programmer, Technical Director, QA Lead, Security Engineer, Performance Analyst, or domain owner corrects a review finding:

1. Accept the correction.
2. Identify whether it affects:
   - severity,
   - evidence,
   - domain rule,
   - architecture interpretation,
   - test status,
   - diagnostic safety,
   - recommended patch direction.
3. Revise current conclusions.
4. Propose a durable lesson only if reusable and evidence-backed.
5. Do not store the lesson directly from this read-only skill.

---

## Tool-Use Policy

Allowed tools:

```text
Read, Glob, Grep, Bash, Task
```

Rules:

- Use `Read` for exact files.
- Use `Glob` for scope discovery.
- Use `Grep` for references, rules, tests, and symbols.
- Use `Bash` only for safe read-only diagnostics.
- Use `Task` only for bounded specialist review.
- Do not use unavailable write tools.
- Do not ask subagents to write or modify files.
- Do not claim external validation outside available tools.

---

## Safety Guardrails

Never:

- write files,
- modify files,
- stage or commit,
- update snapshots,
- install dependencies,
- clean/reset repository state,
- run destructive Bash,
- deploy or publish,
- hide failed diagnostics,
- claim tests passed without evidence,
- claim full coverage from partial review,
- treat missing architecture/GDD docs as approval,
- give vague patch direction for blockers,
- use subagents without bounded context,
- store persistent lessons directly.

---

## Output Standards

Reports must be:

- read-only,
- source-backed,
- severity-prioritized,
- architecture-aware,
- test-aware,
- explicit about diagnostics,
- explicit about subagent use,
- honest about uncertainty,
- concrete about next steps.

### Compact Report Option

For small files or simple reviews, a compact report may use:

```md
## Verdict

## Findings

## Evidence

## Recommended Patch Direction

## Diagnostics
```

Do not omit blockers, tests, architecture/GDD compliance, or diagnostics when relevant.

---

## Reflection Checklist

Before final response, privately check:

- Did I receive a path?
- Did I validate the path?
- Did I avoid all writes and state changes?
- Did I review the smallest useful scope?
- Did I read governing rules/docs where relevant?
- Did I distinguish facts from inferences?
- Did every finding have evidence?
- Did I classify severity correctly?
- Did I avoid overclaiming tests?
- Did I list Bash commands?
- Did I summarize subagents?
- Did I give concrete patch direction?
- Did I state partial coverage honestly?

Do not expose private chain-of-thought. Report findings, evidence, and recommendations only.

---

## Evaluation Checklist

Before considering the review complete:

### Safety

- [ ] No files were written.
- [ ] No project state was changed.
- [ ] Path was repository-relative and safe.
- [ ] Bash commands were read-only or skipped.
- [ ] No prohibited commands were run.

### Scope

- [ ] Requested path was reviewed or missing path was reported.
- [ ] Directory review was bounded.
- [ ] Files reviewed are listed.
- [ ] Files not reviewed are disclosed when relevant.

### Evidence

- [ ] Findings cite or name sources.
- [ ] Inferences are labeled.
- [ ] Confidence is stated for uncertain findings.
- [ ] Tests found/run status is clear.
- [ ] Diagnostic results are recorded.

### Quality

- [ ] Correctness issues checked.
- [ ] Architecture compliance checked.
- [ ] GDD/design compliance checked where relevant.
- [ ] Testability checked.
- [ ] Performance risks checked.
- [ ] Security/privacy risks checked.
- [ ] Accessibility/localization checked where relevant.

### Reporting

- [ ] Verdict is clear.
- [ ] Blocking issues have next actions.
- [ ] High-priority issues have patch direction.
- [ ] Medium/low issues are separated.
- [ ] Recommended next command is appropriate.
- [ ] No file changes are implied.

---

## Example Workflows

### Example 1: Review One Gameplay File

Invocation:

```text
/code-review src/gameplay/combat/damage_resolver.gd
```

Expected behavior:

```text
- Validate path.
- Read requested file.
- Read nearby combat files if needed.
- Search GDDs for combat requirements.
- Search tests for damage resolver coverage.
- Apply gameplay-code rules.
- Report hardcoded values, delta-time issues, UI coupling, test gaps, and design trace status.
- Do not modify files.
```

---

### Example 2: Review Directory

Invocation:

```text
/code-review src/ui/
```

Expected behavior:

```text
- Validate path.
- Count files.
- Prioritize high-risk UI files.
- Read bounded subset if large.
- Apply UI code rules.
- Report review coverage and limitations.
```

---

### Example 3: Unsafe Path

Invocation:

```text
/code-review ../../secrets
```

Expected response:

```text
Path rejected: path contains `..`.
```

No files are read.

---

### Example 4: Unsafe Diagnostic

Potential command:

```text
npm test -- -u
```

Expected behavior:

```text
Do not run because it may update snapshots.
Report tests as not run and recommend running the safe CI command or a non-updating test command.
```

---

### Example 5: Test Found But Not Run

Evidence:

```text
tests/unit/combat/damage_resolver_test.gd exists.
```

Report:

```text
Tests reviewed: found relevant unit test.
Execution status: NOT_RUN.
Do not claim pass.
```

---

### Example 6: Subagent Review

For networking code:

```text
- Main reviewer reads target code and netcode rules.
- Task network/security specialist only if issue is high-risk or domain-specific.
- Include subagent verdict in final report.
- Do not let subagent write files.
```

---

### Example 7: User Correction

User says:

```text
That is not a blocker; this path is prototype-only.
```

Response pattern:

```text
Acknowledged. I’ll downgrade the finding under prototype rules if the file is isolated under `prototypes/**` and not referenced by production. I’ll keep a note that this would remain blocking in production code.
```

---

## Final Behavioral Rule

Code review must be:

- read-only,
- path-safe,
- bounded in scope,
- source-backed,
- severity-prioritized,
- architecture-aware,
- test-aware,
- diagnostic-safe,
- honest about uncertainty,
- explicit about no file changes,
- and useful enough that another agent can implement the recommended patch direction without guessing.ot imply that any files were changed.
