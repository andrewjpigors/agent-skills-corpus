---
name: story-reviewer
description: >-
  Reviews E2E user stories for INVEST compliance, Gherkin correctness, EARS
  constraint coverage, and test derivation quality. Produces a structured verdict
  with per-dimension scores, specific issues, and actionable feedback. Use when
  validating a story before sprint planning, reviewing stories created by
  story-creator or an AI generator, auditing story quality in a PR, or when
  rewrite-in-rust phase 1 produces behavioral specs that need formal validation.
  Triggers: review story, validate story, story quality, BDD review, acceptance
  criteria review, story audit, story feedback, INVEST check.
license: MIT
metadata:
  version: 1.0.0
  author: skills-repo
allowed-tools: Read Write Glob Grep AskUserQuestion Bash(find *) Bash(ls *)
hooks:
  Stop:
    - hooks:
        - type: command
          command: python3 "$HOME/.claude/skills/story-reviewer/scripts/check-completion.py"
          timeout: 120
compatibility: >-
  Hook paths assume global install at $HOME/.claude/skills/story-reviewer/.
  Adjust the hook command path if you install skills elsewhere.
---

# Story Reviewer

Runs a story through a seven-dimension quality gate and produces a structured verdict: PASS, NEEDS_REVISION, or REJECT. Each dimension has a score and specific issues with locations. The feedback's designed so that running `story-creator` with it will actually improve the score — not just produce generic advice. If you've ever gotten review feedback that doesn't tell you what to change, that's what this skill's trying to fix.

## Quick Start

Point this skill at a story file or paste a story. It'll parse the structure, score each quality dimension, identify specific issues with quoted text, derive test cases from each acceptance criterion, and output a structured verdict with actionable feedback. Feed the feedback back to `story-creator` for revision. Repeat until PASS.

Feed the feedback back to `story-creator` for revision. Repeat until PASS.

**Running in opencode:** the `hooks:` frontmatter is ignored, so the review loop isn't automatic. Either re-run the skill until it reports PASS, or opt into the `.opencode/plugins/completion-loop.ts` plugin by setting `OPENCODE_REVIEW_LOOP=story-reviewer` while it runs. Tool-name mapping is in [docs/OPENCODE-COMPATIBILITY.md](../../../docs/OPENCODE-COMPATIBILITY.md).

## When to Use This Skill

- After `story-creator` produces a draft (always review before sprint planning)
- When reviewing stories in a pull request or merge request
- During `all-aboard` documentation audit — check existing stories for quality
- When `rewrite-in-rust` phase 1 produces behavioral specs to validate
- After significant refactoring that may have broken story-to-code traceability
- When AI-generated stories need human-quality validation before use

## Review Dimensions

Score each dimension 1-4:
- **4** — Fully satisfies the criterion
- **3** — Minor gaps, does not block use
- **2** — Significant gaps, needs revision before use
- **1** — Missing or broken, must fix

### Dimension 1: INVEST Compliance

Check each criterion:

| Criterion | What to look for | Common failure |
|---|---|---|
| Independent | No dependency on incomplete stories | "Depends on STORY-NNN (Draft)" |
| Negotiable | Solution not over-specified | Prescribes implementation ("use Redis") |
| Valuable | "so that" describes real outcome | "so that the system works" |
| Estimable | Enough detail to scope | Vague acceptance criteria |
| Small | Fits a single iteration | More than 4 acceptance criteria |
| Testable | Each criterion has clear pass/fail | "system should feel fast" |

Flag each failure with the specific text that fails and why.

### Dimension 2: Gherkin Correctness

Check each acceptance criterion:

**Structural rules:**
- Given establishes preconditions (state, not actions)
- When describes a single triggering action
- Then describes a measurable outcome (observable, not internal)
- And/But used only for compound conditions of the same step type
- No implementation details in steps ("calls the API" is OK; "calls `POST /v2/scan`" is too specific)

**Coverage rules:**
- At least one happy-path scenario
- At least one failure/error scenario
- Boundary or edge cases present for stories with numeric limits, size constraints, or concurrent operations

For each violation, quote the offending step and explain what's wrong.

### Dimension 3: EARS Constraint Coverage

Check that system invariants are expressed as EARS constraints (not buried in Gherkin):

**Required coverage for stories with:**
- Timeout or SLA → Event-driven: `When <timeout>, the <Actor> shall <fallback>.`
- Concurrent access → State-driven: `While <lock held>, the <Actor> shall <behavior>.`
- Security failures → Unwanted behavior: `If <auth fails>, then the <Actor> shall <halt>.`
- Performance requirements → Ubiquitous: `The <Actor> shall <complete within N ms>.`

Flag: missing EARS constraints for stories with security, timing, or concurrency concerns.

### Dimension 4: Autonomy Boundaries (agent stories only)

For stories where the actor is an AI agent:

Check that all four fields are present and specific:
- Maximum actions per cycle (a number, not "reasonable")
- Escalation threshold (a concrete condition, not "when needed")
- Prohibited actions (explicit list, not "harmful things")
- Human oversight requirement (yes/no and under what conditions)

A story that says "the agent will use its judgment" for any of these fails this dimension.

### Dimension 5: Security Coverage

For each data flow in the story, check STRIDE coverage:

| Threat | Must have |
|---|---|
| Spoofing | Authentication scenario or EARS constraint |
| Tampering | Integrity check scenario |
| Repudiation | Audit/logging scenario |
| Information Disclosure | Data protection scenario |
| Denial of Service | Rate limit or resource constraint |
| Elevation of Privilege | Authorization boundary check |

Not every story touches every category. But stories that cross trust boundaries must address all six.

### Dimension 6: Test Derivability

For each acceptance criterion, derive the test cases that would validate it:

**For each Gherkin scenario, verify you can derive:**
- A concrete unit or integration test (Given → setup, When → action, Then → assertion)
- The test type (unit, contract, integration, E2E, chaos)
- The test framework that would execute it (for Rust: `#[test]`, `proptest!`, `cucumber`)

Flag: acceptance criteria that are too vague to derive tests from, or criteria that require E2E infrastructure not described in the story's dependencies.

Build the traceability matrix:

```
| Scenario | Test Type | Framework | Derives from Criterion |
|---|---|---|---|
| Happy path - scan completes | Integration | cucumber | AC-1 |
| Error - upstream timeout | Unit | #[test] | AC-2 |
```

### Dimension 7: Traceability Links

Check that all cross-references resolve:

- Related ADR links: does ADR-NNNN exist?
- Related spec requirement: does FR-NNN exist?
- Dependency stories: do STORY-NNN entries exist and are they in appropriate states?
- Standards mappings: are SLSA levels, SCVS controls, and SSDF practices cited correctly?

Flag broken links specifically.

## Verdict Format

After scoring all dimensions, produce:

```markdown
## Story Review: [Story ID] — [Title]

**Verdict:** [PASS / NEEDS_REVISION / REJECT]
**Reviewed:** [date]

### Scores

| Dimension | Score | Status |
|---|---|---|
| INVEST Compliance | [1-4] | [Pass/Needs work/Fail] |
| Gherkin Correctness | [1-4] | [Pass/Needs work/Fail] |
| EARS Constraints | [1-4] | [Pass/Needs work/Fail] |
| Autonomy Boundaries | [1-4/N/A] | [Pass/Needs work/Fail/N/A] |
| Security Coverage | [1-4] | [Pass/Needs work/Fail] |
| Test Derivability | [1-4] | [Pass/Needs work/Fail] |
| Traceability Links | [1-4] | [Pass/Needs work/Fail] |

**Score:** [N/28 or N/24 if autonomy N/A]

### Issues

[For each issue:]
**[Severity: BLOCK / WARN]** [Dimension] — [Specific text from story]
→ [What's wrong]
→ [What to change]

### Derived Test Cases

[Traceability matrix from Dimension 6]

### Feedback for Revision

[3-6 specific, actionable items the story creator can act on directly]
If resubmitting to story-creator, paste this section as "prior feedback".
```

**Verdict thresholds:**
- PASS: All dimensions ≥ 3, no BLOCK issues
- NEEDS_REVISION: Any dimension = 2, or any BLOCK issue present
- REJECT: Any dimension = 1, or more than 2 BLOCK issues

## Generator-Critic Loop

This skill is designed to work with `story-creator` in a feedback loop:

1. `story-creator` produces draft → `story-reviewer` reviews
2. Verdict = NEEDS_REVISION → feed "Feedback for Revision" back to `story-creator`
3. `story-creator` revises → `story-reviewer` reviews again
4. Repeat up to 3 cycles. If still not PASS after 3, escalate to human review.

Track iteration count in the story's Status field. See the global `artifact-status-tracking` rule for how these statuses integrate with the iterate skill's completion checking.

**Valid story status values (MUST use these exact values):**

| Status | Set when | Iterate blocks? |
|---|---|---|
| `Draft` | Story first created by story-creator | Yes (P1) |
| `Revision 1` / `Revision 2` / `Revision 3` | After each story-reviewer feedback cycle | Yes (P1) |
| `Implemented` | All acceptance criteria coded with passing tests | No |
| `Complete` / `Done` / `Accepted` / `Shipped` | Fully verified | No |

The review cycle: `Draft` → `Revision 1` → `Revision 2` → `Revision 3 (escalate)`

When reviewing, verify the status field uses one of the values above. Flag non-standard statuses (like "In Progress" or "WIP") as they won't be recognized by the iterate completion checker.

If you reach iteration 3 without PASS, use `AskUserQuestion` to ask the user what tradeoff to make rather than continuing to iterate autonomously.

## Reviewing Multiple Stories

When reviewing a batch (e.g., during `all-aboard` audit):

1. Score all stories first to triage
2. Fix REJECT stories before NEEDS_REVISION stories
3. Report summary: `N stories reviewed. X PASS, Y NEEDS_REVISION, Z REJECT.`
4. Prioritize by: security coverage gaps > traceability breaks > INVEST failures > Gherkin issues

## Integration Points

**`all-aboard`:** The onboarding skill should invoke story-reviewer when it finds existing story files in `docs/stories/`. Any story scoring below 3 on any dimension is a documentation gap that should appear in the all-aboard report.

**`rewrite-in-rust`:** Phase 1 produces a behavioral spec. After converting that spec into stories with `story-creator`, run story-reviewer on each story before proceeding to Phase 2. Stories that fail test derivability mean the behavioral spec was too vague and needs more characterization work first.

**`code-review`:** When reviewing PRs that touch feature code, check if existing stories for that feature still pass review. Code changes that break story traceability should be flagged.

**`feature-development`:** After `story-creator` produces the story at Phase 3, run story-reviewer before the spec-writing step. Don't write specs from stories that fail INVEST or Gherkin correctness.

## Writing Style

Apply `natural-writing-style` to all review output. Review feedback should sound like a knowledgeable colleague, not a linter. The goal is revision, not blame.

Don't:
- "The acceptance criteria is insufficient and does not meet the testability requirement."

Do:
- "The 'system should respond quickly' criterion can't be tested — add a concrete latency target (e.g., 'within 500ms under normal load')."

## References

- [Review rubric](references/review-rubric.md) — Detailed scoring criteria with examples
- [Test derivation guide](references/test-derivation.md) — How to build the traceability matrix
- [Security coverage guide](references/security-coverage.md) — STRIDE mapping and supply chain standard references
- [Common failures](references/common-failures.md) — Patterns that reliably fail review, with fixes
