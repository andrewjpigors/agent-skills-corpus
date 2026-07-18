---
name: oh-my-speckit
description: MANDATORY workflow for GitHub Speckit projects. Enforces Spec-First → Clarify → Research → Evaluate → Design → Plan → TDD → Review, with optional Constitution and quality checks. Activates when working in projects with .github/speckit/ directory.

mcp: [context7]
---

# Oh-My-Speckit Workflow - Specification-Driven Development

## [BLOCKING] EXECUTION DIRECTIVES

**These directives are NOT suggestions. They are MANDATORY execution requirements.**

### IMPORTANT: How to Execute Speckit Commands

**Speckit commands are prompt template files.** To execute them:

1. **Read the command file** from project directory:
   - Primary: `.opencode/commands/speckit.{command}.md`
   - Fallback: `.claude/commands/speckit.{command}.md`
   
2. **Process special syntax** in the file:
   | Syntax | Action |
   |--------|--------|
   | `$ARGUMENTS` | Replace with user's feature description |
   | `@filepath` | Read that file and insert contents |
   | `!command` | Execute shell command, insert stdout |

3. **Execute ALL instructions** in the processed file exactly as written

### IMMEDIATE ACTION REQUIRED

Upon loading this skill, you MUST:

1. **Check project structure first** using Glob/Read tools
2. **If `.github/speckit/` missing** → Read and execute `.opencode/commands/oms-init.md`
   - If `.opencode/commands/oms-init.md` and `.claude/commands/oms-init.md` are both missing, **run global `/oms-init`** and follow its prompts.
3. **If constitution missing** → Read and execute `.opencode/commands/speckit.constitution.md`
4. **Otherwise** → Read and execute `.opencode/commands/speckit.specify.md`

**NO TEXT BEFORE TOOL CALLS** - Start with file checks immediately.

### WHAT "MUST" MEANS

| Directive | Meaning |
|-----------|---------|
| **MUST** | Non-negotiable. Failure = workflow broken. |
| **MUST NOT** | Forbidden. Doing this = workflow broken. |
| **SHOULD** | Strong recommendation. Skip only with explicit user override. |

---

## Critical Guardrails

- **NO TodoWrite in Phases 0–5**: These phases require user input and explicit approvals.
- **Approval Gate**: After Phases 0–3.6, STOP and wait for explicit user approval.
- **Do NOT auto-advance**: If approval is missing, do not continue to the next phase.
- **Research before Evaluate**: Phase 3.5 (Research) MUST complete before Phase 3.6 (Evaluate).

## Workflow Overview (Hybrid)

```
0. Initialize     → Setup Speckit structure (oms-init)
1. Constitution   → (MANDATORY for new projects, first-time only)
2. Spec-First     → Define WHAT (speckit.specify)
3. Clarify        → Resolve unknowns (speckit.clarify)
3.5 Research      → Market/competitive analysis (librarian) [NEW]
3.6 Evaluate      → Feature add/remove/modify assessment (speckit-architect) [NEW]
4. Design Session → Refine HOW (brainstorming)
5. Plan           → Create detailed plan (speckit.plan + writing-plans)
6. (Optional)     → Analyze / Checklist quality pass
7. Tasks          → speckit.tasks
8. TDD Execution  → /orchestrate → parallel workers → TDD (MANDATORY)
9. Review & Update→ Verify & update spec (requesting-code-review)
```

## When to Use This Skill

Use only when explicitly invoked by name.

**DO NOT activate when:**
- Simple bug fixes (use systematic-debugging instead)
- Documentation updates only
- Refactoring without behavior change

---

## Quick Mode (OPTIONAL - User Must Enable)

### When to Use Quick Mode

Quick Mode is for **small features, internal tools, or time-sensitive work** where full Research/Evaluate phases are overkill.

**Eligible scenarios:**
- Internal tools with no external users
- Bug fixes that require spec tracking
- Small features (< 1 day implementation)
- Prototypes or MVPs
- User explicitly requests "quick mode" or "빠른 모드"

**NOT eligible:**
- User-facing features
- Security-related changes
- Payment/financial features
- Features requiring market differentiation

### How to Enable Quick Mode

User must explicitly say one of:
- "Use quick mode"
- "빠른 모드로 해줘"
- "Skip research and evaluate"
- "Research/Evaluate 생략해줘"

### Quick Mode Workflow

```
0. Initialize     → (same)
1. Constitution   → (same, first-time only)
2. Spec-First     → (same)
3. Clarify        → (same)
3.5 Research      → ⏭️ SKIPPED (Quick Mode)
3.6 Evaluate      → ⏭️ SKIPPED (Quick Mode)
4. Design Session → (same)
5. Plan           → (same)
6-10              → (same)
```

### Quick Mode Spec Frontmatter

When Quick Mode is enabled, add to spec frontmatter:

```yaml
---
status: clarified
mode: quick
quick_mode_reason: [user's reason for enabling quick mode]
skipped_phases: [research, evaluate]
---
```

### Quick Mode Guardrails

Even in Quick Mode:
- ✅ Spec is STILL required
- ✅ Clarify phase is STILL required
- ✅ TDD is STILL required
- ✅ Tests are STILL required
- ❌ Cannot skip spec creation
- ❌ Cannot skip clarify (edge cases matter!)

### Reverting from Quick Mode

If during implementation you discover:
- Competitors exist that should be analyzed
- Feature scope expanded beyond "small"
- Security implications found

Then: **STOP and revert to full workflow**
1. Notify user: "This feature needs full Research/Evaluate. Reverting from Quick Mode."
2. Execute Phase 3.5 and 3.6
3. Continue from there


## Phase 0: Initialize (MANDATORY, FIRST-TIME ONLY)

### 👉 EXECUTE NOW (if structure missing)

**Read and execute the speckit init command file:**
```
Read: .opencode/commands/oms-init.md (or .claude/commands/oms-init.md)
Then: Follow ALL instructions in that file
```

**If both files are missing:**
- Run global `/oms-init` and follow its prompts

---

**REQUIRED for all new projects.** Setup Speckit directory structure.

1. **Check if Speckit structure exists:**
   - `.github/speckit/` directory
   - `.opencode/designs/` and `.opencode/plans/` directories

2. **If structure missing:**
   - **Read** `.opencode/commands/oms-init.md` (or `.claude/commands/oms-init.md`)
   - **Execute** all instructions in that file
   - If both files are missing, **run global `/oms-init`** and follow its prompts
   - Get approval before proceeding to Phase 1

3. **If structure exists:**
   - Verify structure is complete
   - Skip to Phase 1

## Phase 1: Constitution (MANDATORY, FIRST-TIME ONLY)

### 👉 EXECUTE NOW (if constitution missing)

**Read and execute the constitution command file:**
```
Read: .opencode/commands/speckit.constitution.md
Then: Follow ALL instructions in that file
```

---

**REQUIRED for all new projects.** Set guiding principles before any feature work.

1. **Check if constitution exists:**
   - `.github/speckit/constitution.md`
   - `.specify/memory/constitution.md`

2. **If constitution missing:**
   - **Read** `.opencode/commands/speckit.constitution.md`
   - **Execute** all instructions in that file
   - Interview user for project principles
   - Get approval before proceeding to Phase 2

3. **If constitution exists:**
   - Read and apply it to all feature work
   - Skip to Phase 2

## Phase 2: Spec-First (MANDATORY)

### [BLOCKING] EXECUTION REQUIRED

**MUST**: Read and execute `.opencode/commands/speckit.specify.md`
**MUST NOT**: Skip reading the command file and make up your own spec format.

---

### Phase 2A: Initial Draft

**Before ANY code or design work:**

1. **Delegate to Spec Writer Agent:**
   ```
   task(
     subagent_type="speckit-spec-writer",
     description="Create initial spec",
     prompt="Read .opencode/commands/speckit.specify.md and execute it for: [user's feature request]"
   )
   ```

2. **Read and Execute the Speckit command file:**
   - **Read** `.opencode/commands/speckit.specify.md`
   - **Process** any `@filepath` references (read those files too)
   - **Execute** all instructions exactly as written

3. **Create comprehensive initial draft:**
   - Analyze user requirements
   - Review existing codebase context
   - Create structured spec document following the template
   - Emphasize deep reasoning and completeness

4. **Show draft to user:**
   - Present the initial spec
   - Collect direct feedback for refinement

### Phase 2B: Iterative Refinement

1. **Continue with Spec Writer Agent:**
   ```
   task(
     subagent_type="speckit-spec-writer",
     description="Refine spec",
     prompt="Refine spec based on user feedback: [feedback]"
   )
   ```

2. **Rapid feedback cycles (5-10+ rounds expected):**
   - Quickly incorporate user feedback
   - Make focused edits and clarifications
   - Favor speed and iteration over perfection

3. **Spec approval:**
   - Continue cycles until user explicitly approves
   - Save final draft to `.github/speckit/specs/{feature-name}/spec.md`
   - **STOP here until user approves**

## Phase 3: Clarify (MANDATORY)

### [BLOCKING] EXECUTION REQUIRED

**MUST**: Read and execute `.opencode/commands/speckit.clarify.md`
**MUST**: Delegate to `speckit-architect` for validation.

---

### Architect: speckit-architect

**Validate and clarify the draft:**

1. **Delegate to Architect Agent:**
   ```
   task(
     subagent_type="speckit-architect",
     description="Validate and clarify spec",
     prompt="Read .opencode/commands/speckit.clarify.md and execute it for spec at: [spec path]"
   )
   ```

2. **Read and Execute the Speckit command file:**
   - **Read** `.opencode/commands/speckit.clarify.md`
   - **Execute** all instructions exactly as written

3. **Deep Validation:**
   - Find ALL edge cases not covered
   - Identify ALL ambiguities
   - Add missing non-functional requirements
   - Perform risk analysis
   - Generate clarifying questions

4. **Refinement (1-2 rounds expected):**
   - Present findings to user
   - Get answers to clarifying questions
   - Update spec with clarifications
   - Ensure spec is crystal clear

5. **Completion:**
   - Ensure ALL uncertainties resolved
   - Update spec status to `clarified`
   - Proceed to Phase 3.5 (Research)

## Phase 3.5: Market Research (MANDATORY)

### [BLOCKING] EXECUTION REQUIRED

**MUST**: Execute market/competitive research before evaluation.
**MUST**: Use `librarian` agent for research (runs in background).

---

### Research Agent: librarian

**Research the market landscape for the clarified spec:**

1. **Launch Research Agent (Background):**
   ```
   background_task(
     agent="librarian",
     description="Market research for [feature name]",
     prompt="Research market landscape for this feature spec:

     Feature: [feature name]
     Spec path: [spec path]

     Research and report:
     1. **Competitive Analysis**: What similar solutions exist? (3-5 competitors)
        - Their approach, strengths, weaknesses
     2. **Market Trends**: Current trends in this space (2025)
     3. **Best Practices**: Industry standards and patterns
     4. **Potential Differentiators**: How could this feature stand out?
     5. **Risks/Concerns**: Common pitfalls to avoid

     Output a structured research.md report."
   )
   ```

2. **Wait for research completion**

3. **Present research.md to user:**
   - Show competitive landscape
   - Show market trends
   - Allow user to note any irrelevant findings
   - Save to `.github/speckit/specs/{feature-name}/research.md`

4. **Proceed to Evaluate phase**

## Phase 3.6: Feature Evaluation (MANDATORY)

### [BLOCKING] EXECUTION REQUIRED

**MUST**: Evaluate spec against research findings.
**MUST**: Delegate to `speckit-architect` (Opus) for deep reasoning.

---

### Architect: speckit-architect

**Evaluate the spec with research context:**

1. **Delegate to Architect Agent:**
   ```
   task(
     subagent_type="speckit-architect",
     description="Evaluate spec against market research",
     prompt="Evaluate this feature spec against market research.

     Spec: [spec path]
     Research: [research.md path]

     Provide evaluation:
     1. **Features to ADD**: What's missing that competitors have or market expects?
     2. **Features to REMOVE**: What's over-engineered or unnecessary?
     3. **Features to MODIFY**: What needs adjustment based on best practices?
     4. **Priority Assessment**: Which features are must-have vs nice-to-have?
     5. **Differentiation Strategy**: How to stand out from competitors?

     For each suggestion, provide:
     - Rationale (why)
     - Evidence (from research)
     - Impact (high/medium/low)

     Output structured evaluation.md report."
   )
   ```

2. **Present evaluation.md to user:**
   - Show feature recommendations (add/remove/modify)
   - Show priority assessment
   - Show differentiation opportunities

3. **User Decision:**
   - For EACH suggestion: **Accept** or **Reject**
   - User may provide reasoning for rejections
   - Update spec based on accepted suggestions

4. **Finalize Spec:**
   - Apply accepted changes to spec
   - Update spec status to `evaluated`
   - Save evaluation decisions to `.github/speckit/specs/{feature-name}/evaluation.md`
   - **STOP and confirm with user before proceeding to Design**

## Phase 4: Design Session

### Architect: speckit-architect

**ONLY after spec is evaluated and finalized (Phase 3.6 complete):**

1. **Delegate to Architect Agent:**
   ```
   task(
     subagent_type="speckit-architect",
     description="Design architecture",
     prompt="Design architecture for: [feature name]. Follow brainstorming skill methodology."
   )
   ```

2. **Design Session Questions:**
   - "What's the overall architecture?"
   - "Which existing components/modules can be reused?"
   - "What new files/components are needed?"
   - "What are the key technical decisions?"
   - "What could go wrong?"

3. **Create design document:**
   - Save to `.opencode/designs/{feature-name}-design.md`
   - Include:
     - Architecture diagram (text-based)
     - Component structure and responsibilities
     - Key technical decisions with rationale
     - Risk mitigation strategies
     - Data flow design

4. **Update spec with design:**
   - Add "## Design" section to spec
   - Link to design document
   - Update status to `designed`
   - Get user approval before proceeding

## Phase 5: Implementation Plan

### [BLOCKING] EXECUTION REQUIRED

**MUST**: Read and execute `.opencode/commands/speckit.plan.md`
**MUST**: Delegate to `speckit-architect` for planning.

---

### Architect: speckit-architect

**ONLY after design is approved:**

1. **Delegate to Architect Agent:**
   ```
   task(
     subagent_type="speckit-architect",
     description="Create implementation plan",
     prompt="Read .opencode/commands/speckit.plan.md and execute it for: [feature name]"
   )
   ```

2. **Read and Execute the Speckit command file:**
   - **Read** `.opencode/commands/speckit.plan.md`
   - **Execute** all instructions exactly as written

3. **Create Detailed Plan:**
   - Break design into concrete tasks
   - Map task dependencies
   - Define file structure
   - Specify API contracts
   - Plan test strategy
   - Define rollout approach

4. **Link plan to spec:**
   - Save to `.opencode/plans/{feature-name}-plan.md`
   - Update spec with "## Implementation Plan" section
   - Link to plan file
   - Update status to `planned`

5. **CRITICAL DECISION POINT:**
   - Present the plan to the user
   - Ask: "Do you approve this plan? If yes, I will proceed to implement ALL tasks autonomously."
   - **WAIT for explicit approval**
   - Once approved, **DO NOT STOP** until Phase 9 is complete

## Phase 6: (Optional) Analyze / Checklist

**Optional quality pass before task execution:**

1. **Run analysis (if needed):**
   - **Read** `.opencode/commands/speckit.analyze.md`
   - **Execute** all instructions in that file

2. **Run checklist (if needed):**
   - **Read** `.opencode/commands/speckit.checklist.md`
   - **Execute** all instructions in that file

3. **Skip to Phase 7 if not needed**

## Phase 7: Tasks (AUTO-EXECUTE)

### [BLOCKING] EXECUTION REQUIRED

**MUST**: Read and execute `.opencode/commands/speckit.tasks.md`

---

### Main Sisyphus

**Triggered IMMEDIATELY after Plan approval:**

1. **Announce autonomous execution mode:**
   - "Engaging autonomous implementation. Stand by for completion."

2. **Read and Execute the Speckit tasks command:**
   - **Read** `.opencode/commands/speckit.tasks.md`
   - **Execute** all instructions exactly as written

3. **Skill Mapping (Smart Context):**
    - Review the generated `tasks.md`
    - `/speckit.tasks` command now auto-generates skill tags (see `.opencode/command/speckit.tasks.md`)
    - Verify skill tags are present: `→ /skill-name` at end of task descriptions
    - Common skill mappings:
      | Task Type | Skill Tag |
      |-----------|-----------|
      | Browser/E2E testing | `→ /playwright` |
      | UI/UX components | `→ /frontend-ui-ux` |
      | Quality checks | `→ /speckit.checklist` |
      | Complex debugging | `→ /systematic-debugging` |
    - Optional: add dependencies with `(id: X)` and `(depends_on: A,B)`
    
    **중요:** Phase 8에서 태스크 실행 시, `→ /skill-name` 표기를 만나면:
    1. **Read** `.opencode/commands/{skill-name}.md` 또는 해당 스킬 파일
    2. **Execute** 그 파일의 지시사항을 따름

4. **Proceed to Phase 8 immediately**

## Phase 8: TDD Execution via Orchestration (AUTO-EXECUTE, MANDATORY)

### [BLOCKING] PARALLEL EXECUTION REQUIRED

**MUST use `/orchestrate` for ALL task execution.** No sequential fallback.

### ⛔ FORBIDDEN ACTIONS
- ❌ Implementing tasks directly without /orchestrate
- ❌ Calling task(subagent_type="speckit-developer") directly for implementation
- ❌ Writing code yourself in this phase
- ❌ Skipping orchestration "because it's simpler"

### ✅ REQUIRED ACTION
**IMMEDIATELY execute this command:**
```
/orchestrate execute .opencode/plans/<feature-name>-plan.md
```

If /orchestrate skill is not loaded, first load it:
```
Read: ~/.claude/skills/orchestrate/SKILL.md
Then execute the orchestration command above
```

---

### Orchestration Flow

1. **Spawn parallel workers via `/orchestrate`:**
   ```
   /orchestrate execute .opencode/plans/<feature-name>-plan.md
   ```
   
   - LLM analyzes tasks and groups them dynamically
   - Each worker group spawns as tmux session
   - Workers execute in parallel

2. **Each Worker calls appropriate subagent:**
   ```
   Worker → task() → speckit-developer (or other agent based on domain)
   ```

3. **speckit-developer handles task (with sub-delegation):**
   
   Developer가 태스크를 받으면 도메인에 따라:
   - **UI/Frontend** → `task()` → `frontend-ui-ux-engineer`
   - **Documentation** → `task()` → `document-writer`
   - **Complex Analysis** → `task()` → `oracle`
   - **Backend/API/Testing** → 직접 TDD 구현
   
   **하나의 태스크에서 여러 서브에이전트 호출 가능.**
   예: "로그인 기능" = UI(위임) + API(직접) + 문서(위임)

4. **TDD Cycle (for direct implementation):**
   1. **Load Skill:** 태스크에 `→ /skill-name`이 있으면:
      - **Read** 해당 스킬의 command 파일 또는 SKILL.md
      - **Follow** 그 파일의 지시사항
   2. **RED:** Write failing test
   3. **GREEN:** Write minimal code to pass
   4. **REFACTOR:** Clean up while keeping tests green
   5. **Mark Complete:** Check `[x]` in `tasks.md`

5. **Result Collection:**
   - Orchestrator collects results from all workers
   - Synthesizes and detects conflicts
   - Reports completion

### Why Mandatory Orchestration?

- **일관된 실행 모델**: 항상 같은 방식으로 동작
- **병렬 처리**: 태스크가 1개여도 worker 1개로 실행
- **서브에이전트 체인 활용**: Worker → Developer → 전문 에이전트
- **토큰 폴백 지원**: 각 에이전트별 모델 폴백 설정 적용

## Phase 8.5: Global Refactoring (AUTO-EXECUTE)

### Optimizer: speckit-optimizer

**Project-Wide Cleanup:**

1. **Delegate to Optimizer Agent:**
   ```
   task(
     subagent_type="speckit-optimizer",
     description="Global refactoring",
     prompt="Perform global refactoring after implementation. DRY, cleanup, optimize."
   )
   ```

2. **Execute Cleanup (leveraging 400k context):**
   - **DRY:** Extract duplicated logic from multiple files into shared helpers
   - **Structure:** Verify file organization and move files if needed
   - **Clean:** Remove unused imports, console logs, and dead code
   - **Style:** Ensure consistent naming conventions across modules
   - **Performance:** Optimize algorithms and queries where beneficial

3. **Verify Integrity:**
   - Run full test suite (`npm test`)
   - **Must pass 100%** before proceeding
   - Verify no regressions introduced

## Phase 9: Review & Update (AUTO-EXECUTE)

### Developer: speckit-developer

**Triggered IMMEDIATELY after refactoring complete:**

1. **Delegate to Developer Agent:**
   ```
   task(
     subagent_type="speckit-developer",
     description="Review and update spec",
     prompt="Review implementation against spec and update status to 'implemented'"
   )
   ```

2. **Self-review checklist:**
   - [ ] All acceptance criteria met (from spec)
   - [ ] All tests pass
   - [ ] Code follows project conventions
   - [ ] No unrelated changes
   - [ ] Plan tasks all completed

3. **Update spec status:**
   - Change status to `implemented`
   - Add implementation date
   - Link to PR (if created)
   - Add actual implementation notes

## Phase 10: Systematic Verification & Quality Score (AUTO-EXECUTE)

### Step 10.1: E2E Testing (Conditional)

**If project has E2E tests or UI components:**

1. **Delegate to E2E Runner Agent:**
   ```
   task(
     subagent_type="e2e-runner",
     description="Run E2E tests",
     prompt="Run E2E tests for implemented features using Playwright"
   )
   ```

2. **E2E Runner Responsibilities:**
   - Run Playwright tests for critical user flows
   - Validate UI interactions work correctly
   - Check for visual regressions
   - Report flaky tests

3. **Skip if:** No E2E tests exist or feature is backend-only

---

### Step 10.2: Security Review (Conditional - SaaS/Auth)

**If feature involves: auth, payments, user data, API endpoints:**

1. **Delegate to Security Reviewer Agent:**
   ```
   task(
     subagent_type="security-reviewer",
     description="Security audit",
     prompt="Security audit for: [feature name]. Check OWASP Top 10."
   )
   ```

2. **Security Review Checklist (OWASP Top 10):**
   - [ ] No SQL/NoSQL injection vulnerabilities
   - [ ] Input sanitization on all user inputs
   - [ ] No hardcoded secrets/credentials
   - [ ] Proper authentication checks
   - [ ] Authorization on all endpoints
   - [ ] XSS prevention (output encoding)
   - [ ] CSRF protection
   - [ ] Secure session management

3. **Critical Vulnerability Protocol:**
   - 🔴 **CRITICAL found** → STOP, fix immediately, re-review
   - 🟠 **HIGH found** → Fix before completion
   - 🟡 **MEDIUM found** → Document, fix in follow-up
   - 🟢 **LOW/None** → Proceed

4. **Skip if:** Feature has no security implications (pure UI, docs, etc.)

---

### Step 10.3: Quality Scoring

**Optimizer: speckit-optimizer**

**Final Quality Gate with Scoring:**

1. **Delegate to Optimizer Agent:**
   ```
   task(
     subagent_type="speckit-optimizer",
     description="Quality verification",
     prompt="Final verification, quality scoring, and debugging if needed"
   )
   ```

2. **Run Full Test Suite:**
   - Ensure no regressions
   - Verify all tests pass

3. **Calculate Quality Score (0-100):**

   | Category | Max Points | Criteria |
   |----------|------------|----------|
   | **Unit Tests** | 25 | Pass rate: (passed/total) * 25 |
   | **Code Coverage** | 25 | Coverage %: (coverage/100) * 25 |
   | **Integration Tests** | 15 | Pass rate: (passed/total) * 15 |
   | **E2E/Browser Tests** | 15 | Pass rate: (passed/total) * 15 |
   | **Spec Compliance** | 10 | All acceptance criteria met: 10, partial: 5 |
   | **Code Quality** | 10 | No lint errors: 5, No type errors: 5 |

   **Minimum Passing Score: 80/100**

4. **Quality Score Calculation Script:**
   ```bash
   # Run tests and capture results
   TEST_RESULT=$(npm test 2>&1)
   PASSED=$(echo "$TEST_RESULT" | grep -oP '\d+(?= passed)' | head -1 || echo 0)
   FAILED=$(echo "$TEST_RESULT" | grep -oP '\d+(?= failed)' | head -1 || echo 0)
   TOTAL=$((PASSED + FAILED))
   
   # Calculate unit test score
   if [ $TOTAL -gt 0 ]; then
     UNIT_SCORE=$((PASSED * 25 / TOTAL))
   else
     UNIT_SCORE=0
   fi
   
   # Get coverage (if available)
   COVERAGE=$(npm run coverage 2>&1 | grep -oP 'All files[^\d]*\K\d+' || echo 0)
   COVERAGE_SCORE=$((COVERAGE * 25 / 100))
   
   # Calculate total
   TOTAL_SCORE=$((UNIT_SCORE + COVERAGE_SCORE))
   echo "Quality Score: $TOTAL_SCORE/100"
   ```

5. **Score Actions:**
   - **Score >= 80**: Proceed to completion
   - **Score 60-79**: Warning, ask user if acceptable
   - **Score < 60**: BLOCK completion, require fixes

6. **If bugs found:**
   - Use systematic debugging (scientific method)
   - Fix root causes, not symptoms
   - Add tests to prevent recurrence
   - Re-calculate quality score

7. **Report Completion:**
   - ONLY NOW stop and report to user
   - Include quality score breakdown
   - Provide summary of changes
   - List test results
   - Note any deviations from plan

   **Example Output:**
   ```
   ## Implementation Complete
   
   **Quality Score: 87/100**
   - Unit Tests: 23/25 (92% pass rate)
   - Coverage: 21/25 (84% coverage)
   - Integration: 15/15 (100%)
   - E2E: 13/15 (87%)
   - Spec Compliance: 10/10
   - Code Quality: 5/10 (minor lint warnings)
   
   All acceptance criteria met. Ready for review.
   ```

## [BLOCKING] Subagent Delegation Rules

**MUST delegate to specialized subagents. Direct execution is FORBIDDEN.**

### Mandatory Agent Assignments

| Phase | Agent | Invocation | MUST Use |
|-------|-------|------------|----------|
| Phase 2 (Spec) | `speckit-spec-writer` | `task(subagent_type="speckit-spec-writer", ...)` | **YES** |
| Phase 3 (Clarify) | `speckit-architect` | `task(subagent_type="speckit-architect", ...)` | **YES** |
| Phase 3.5 (Research) | `librarian` | `background_task(agent="librarian", ...)` | **YES** |
| Phase 3.6 (Evaluate) | `speckit-architect` | `task(subagent_type="speckit-architect", ...)` | **YES** |
| Phase 4-5 (Design/Plan) | `speckit-architect` | `task(subagent_type="speckit-architect", ...)` | **YES** |
| Phase 8-9 (TDD/Review) | `speckit-developer` | `task(subagent_type="speckit-developer", ...)` | **YES** |
| Phase 8.5, 10.3 (Refactor/Verify) | `speckit-optimizer` | `task(subagent_type="speckit-optimizer", ...)` | **YES** |
| Phase 10.1 (E2E) | `e2e-runner` | `task(subagent_type="e2e-runner", ...)` | **Conditional** |
| Phase 10.2 (Security) | `security-reviewer` | `task(subagent_type="security-reviewer", ...)` | **Conditional** |

### Domain-Specific Delegation (via speckit-developer)

When `speckit-developer` receives a task, it auto-delegates based on domain:

| Task Domain | Keywords | Delegate To |
|-------------|----------|-------------|
| Frontend/UI | UI, styling, component, layout, animation, CSS | `frontend-ui-ux-engineer` |
| Database/Schema | database, schema, migration, SQL, model design | `speckit-architect` |
| Documentation | docs, README, API docs, guide | `document-writer` |
| Complex Analysis | architecture, security audit, performance analysis | `oracle` |
| Backend/API/Testing | (default - developer handles) | Self |

**Note**: This delegation happens automatically within `speckit-developer`. You don't need to call these agents directly from the main workflow.

### Why Delegation is MANDATORY

1. **Token Limit Fallback**: Subagents have automatic model fallback configured
2. **Domain Optimization**: Each agent uses a model optimized for its domain
3. **Context Isolation**: Prevents context pollution between phases
4. **Parallel Execution**: Multiple subagents can run concurrently

### FORBIDDEN Actions (Main Agent)

- **MUST NOT**: Write spec content directly (delegate to spec-writer)
- **MUST NOT**: Create design documents directly (delegate to architect)
- **MUST NOT**: Write implementation code directly (delegate to developer)
- **MUST NOT**: Perform refactoring directly (delegate to optimizer)

### ALLOWED Actions (Main Agent)

- **MAY**: Read files for context
- **MAY**: Run bash commands for status checks
- **MAY**: Coordinate between subagents
- **MAY**: Verify subagent output quality
- **MAY**: Update todo lists and progress tracking

**Agent Location:** `~/.config/opencode/agents/` or `~/.claude/agents/`

### Skill Tags in Tasks

Tasks in `tasks.md` may have skill tags at the end:
```
- [ ] T007 [US1] Create login page → /playwright
```

**Execution Rule:** When encountering `→ /skill-name`:
1. Parse the skill name (e.g., `playwright`)
2. **Read** the skill's command file: `.opencode/commands/{skill-name}.md` or `~/.claude/skills/{skill-name}/SKILL.md`
3. **Execute** the task following that file's instructions

### Available Skills for Task Mapping

| Skill | Purpose | How to Execute |
|-------|---------|----------------|
| `/playwright` | Browser automation, E2E tests | Read `.opencode/commands/playwright.md` |
| `/frontend-ui-ux` | UI component design | `task(subagent_type="frontend-ui-ux-engineer", ...)` |
| `/speckit.checklist` | Quality validation | Read `.opencode/commands/speckit.checklist.md` |
| `/systematic-debugging` | Complex debugging | Read `~/.claude/skills/systematic-debugging/SKILL.md` |
| `/orchestrate` | Parallel worker execution | Read `~/.claude/skills/orchestrate/SKILL.md` |

## Critical Rules

### NEVER:
- ❌ Skip spec creation
- ❌ Skip clarify before design
- ❌ Skip tasks before TDD
- ❌ Start coding before spec approval
- ❌ Write code before tests (except when TDD doesn't apply)
- ❌ Mark task complete without verification
- ❌ Change spec status without completing phase

### ALWAYS:
- ✅ Ask before proceeding to next phase
- ✅ Update spec at each phase
- ✅ Run tests after every change
- ✅ Commit after each task
- ✅ Show progress to user
- ✅ Prefer scripts for deterministic data extraction to reduce context cost
- ✅ Archive reusable prompts in `prompts/` (or `.opencode/prompts/`) and reference them

## Verification Before Completion

Before declaring "done", verify:

```bash
# 1. All tests pass
npm test  # or appropriate test command

# 2. Spec is updated
grep "status: implemented" .github/speckit/specs/{feature-name}/spec.md

# 3. Plan is complete
grep "\[x\]" .opencode/plans/{feature-name}-plan.md | wc -l

# 4. No uncommitted changes
git status
```

## Example Session

**User:** "Add user authentication"

**You:**
1. ✅ `/oms-init` (first-time only - setup structure)
2. ✅ `/speckit.constitution` (first-time only - project principles)
3. ✅ `/speckit.specify` → spec created/updated
4. ✅ `/speckit.clarify` → clarifications recorded
5. ✅ `/speckit.research` → market/competitive research completed
6. ✅ `/speckit.evaluate` → feature evaluation, accept/reject decisions
7. ✅ Use `superpowers:brainstorming` → Design session
8. ✅ Create `.opencode/designs/user-auth-design.md`
9. ✅ `/speckit.plan` → plan created
10. ✅ (Optional) `superpowers:writing-plans` enhancement
11. ✅ (Optional) `/speckit.analyze` / `/speckit.checklist`
12. ✅ `/speckit.tasks` → tasks approved
13. ✅ Use `superpowers:test-driven-development`
14. ✅ Execute each task: RED → GREEN → REFACTOR
15. ✅ Use `superpowers:requesting-code-review`
16. ✅ Update spec status to `implemented`
17. ✅ Done!

## File Structure

```
project/
├── .github/
│   └── speckit/
│       ├── specs/
│       │   ├── user-auth/
│       │   │   ├── spec.md           ← WHAT (requirements)
│       │   │   ├── research.md       ← Market/competitive research
│       │   │   └── evaluation.md     ← Feature evaluation decisions
│       │   └── payment/
│       │       └── spec.md
│       ├── decisions/
│       │   └── auth-strategy.md
│       └── constitution.md           ← optional, first-time only
│
├── .opencode/
│   ├── designs/
│   │   └── user-auth-design.md       ← HOW (architecture)
│   └── plans/
│       └── user-auth-plan.md         ← TASKS (implementation)
│
├── src/
│   └── ... (code)
└── tests/
    └── ... (tests)
```

## Troubleshooting

**"User wants to skip clarify"**
→ Explain: "Clarify is required before design to avoid rework."

**"Feature is too small for full workflow"**
→ Still create minimal spec. If truly trivial (1-2 line change), keep phases compact.

**"Spec already exists but is outdated"**
→ Update spec first, then re-run clarify.

**"User wants to code immediately"**
→ Firmly but politely insist: "Let me create a quick spec first. It will save time."

## Integration with Superpowers

This skill orchestrates other Superpowers skills:

```
oh-my-speckit (meta-skill)

    ├─ uses: oms-init (initialization)
    ├─ uses: brainstorming (design)
    ├─ uses: writing-plans (planning)
    ├─ uses: test-driven-development (implementation)
    ├─ uses: requesting-code-review (review)
    ├─ uses: systematic-debugging (verification)
    ├─ uses: spec-cache (optimization)
    └─ manages: Spec lifecycle
```

**Priority:** This skill takes precedence over individual skills when Speckit directory is present.

## Status Lifecycle

```
draft → clarified → researched → evaluated → designed → planned → tasked → implemented → verified
```

Track status in spec frontmatter. Never skip statuses.
