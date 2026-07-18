---
name: "tdd-coach"
description: "Test-driven development skill for engineering teams. Activates when the user wants to write tests, practice TDD, generate unit or integration tests, analyze coverage reports, review test quality, generate fixtures or mocks, or work through a red-green-refactor cycle. Also activates when the user pastes acceptance criteria, a user story, or Jira ticket text and wants executable tests derived from it — no Jira API needed. Supports Jest, Vitest, Mocha+Chai, Pytest, JUnit 4, JUnit 5, Spring Boot test slices, and Playwright component tests. Framework and language are auto-detected; no configuration required to start."
---

# TDD Coach

A plugin-based TDD skill. The root file (this one) handles detection and routing. Per-framework patterns live in `frameworks/<name>/SKILL.md` and are loaded automatically based on your project.

---

## Quick Start — What to Type

**Not sure where to begin?** Use one of these prompts to get the best experience:

| Your situation | Suggested starter prompt |
|---|---|
| **Nothing exists yet** — you want to write the tests first | `Guide me through writing TDD tests for a [function/class] that [does X]. Walk me through the red-green-refactor cycle.` |
| **Acceptance criteria or a ticket** — turn requirements into tests | `Here are my acceptance criteria: [paste them]. Generate executable tests and walk me through making each one pass.` |
| **Existing code, no tests** — add a test suite | `Here is my source file: [paste or attach]. Generate a full test suite covering all branches, edge cases, and boundaries.` |
| **Existing code + tests** — review or improve coverage | `Here is my source and test file. Review test quality and suggest improvements — coverage gaps, missing edge cases, incorrect doubles.` |
| **Refactoring risky code** — characterisation tests first | `I need to refactor [file]. Generate characterisation tests to lock down the current behaviour before I change anything.` |
| **Learning TDD** — guided red-green-refactor practice | `Guide me through a full red-green-refactor cycle for [feature]. Start by writing a failing test.` |

You don't need to pick a workflow — just describe what you're working on and the skill will route correctly. The prompts above just help you get more targeted output on the first attempt.

---

## Step 0 — Detect and Load

**Do this before generating anything.**

### 0a. Check for project config

Look for `.tdd-coach.json` in the project root (same level as `package.json`, `pom.xml`, or `pyproject.toml`).

- **Found** → read it; its `framework`, `language`, and `conventions` values are authoritative and override auto-detection.
- **Not found** → auto-detect using the signals below.
- **Ambiguous and user hasn't specified** → ask exactly once: `"Which framework? (Jest / Vitest / Mocha+Chai / Pytest / JUnit 4 / JUnit 5 / Spring Boot / Playwright)"`

### 0b. Auto-detect framework

| File / signal | Framework to use |
|---|---|
| `jest` in `package.json` devDependencies | Jest |
| `vitest` in `package.json` devDependencies | Vitest |
| `mocha` in `package.json` devDependencies | Mocha + Chai |
| `pytest` in `requirements*.txt` or `pyproject.toml` | Pytest |
| `junit-jupiter` in `pom.xml` or `build.gradle` | JUnit 5 |
| `<artifactId>junit</artifactId>` in `pom.xml` (without `junit-jupiter`) | JUnit 4 |
| `spring-boot-starter-test` in `pom.xml` | Spring Boot |
| `@playwright/test` in `package.json` | Playwright |

### 0c. Load the framework plugin

Plugins contain the test structure, mocking patterns, gotchas, and coverage config for each stack. **Read the plugin file before generating any tests.**

Resolution order — check each in sequence and use the first one found:

1. If `.tdd-coach.json` sets `"pluginDir"` → read `<pluginDir>/<framework>/SKILL.md` (project-local override, highest priority)
2. Otherwise → read `frameworks/<framework>/SKILL.md` from this skill's own directory
3. If neither exists → fall back to built-in knowledge; note that no plugin was loaded but continue

Plugin map:

| Framework key | Plugin path |
|---|---|
| `jest` | `frameworks/jest/SKILL.md` |
| `vitest` | `frameworks/vitest/SKILL.md` |
| `mocha-chai` | `frameworks/mocha-chai/SKILL.md` |
| `pytest` | `frameworks/pytest/SKILL.md` |
| `junit5` | `frameworks/junit5/SKILL.md` |
| `junit4` | `frameworks/junit4/SKILL.md` |
| `spring-boot` | `frameworks/spring-boot/SKILL.md` |
| `playwright` | `frameworks/playwright/SKILL.md` |

### 0d. Apply conventions (if configured)

If `.tdd-coach.json` sets `"conventions.extraInstructions"`, read that file (path is relative to the project root) and treat its contents as additional rules that extend or override the plugin for this session. These rules apply to everything generated — naming, comment style, mock strategy, file layout.

**Recognised shorthand flags in `.tdd-coach.json`:**

| Key | Type | Default | Effect |
|-----|------|---------|--------|
| `"doubleComments"` | boolean | `true` | When `false`, omit the inline type-and-why comments on test doubles (e.g. `// stub — ...`). Tags and traceability comments are unaffected. |
| `"verbose"` | boolean | `true` | When `false`, suppress the RED phase explanation prose (why it fails, what true RED looks like, double rationale paragraph) and the self-check narration. The tests and inline double comments are still generated normally. Set this if you know TDD and just want clean output. |

### 0e. Read language-specific config files (TypeScript only)

For TypeScript projects, before generating any tests:

1. Look for `tsconfig.json` (or `tsconfig.base.json`, `tsconfig.test.json`) in the project root.
2. Check for `"strict": true` or `"useUnknownInCatchVariables": true` in `compilerOptions`.
3. Pass this flag to the Jest / Vitest plugin — it changes the generated catch patterns and callback parameter types.

If no tsconfig is found and the project is TypeScript, ask: `"Is strict mode enabled in your tsconfig (strict: true)?"`

---

## TDD Workflows

### SOLID — Proactive Design Coaching

**This skill is a coaching tool, not just a code generator.** Writing tests is one of the best moments to find design problems — test doubles expose hidden coupling, and setUp complexity reveals classes with too many responsibilities. Whenever you read source code as part of any workflow, scan for SOLID violations and report them.

**How to report a SOLID violation:**

Add a `⚠ SOLID` comment block at the top of the generated test file, or immediately above the affected test, using the language's comment syntax:

```python
# ⚠ SOLID — Dependency Inversion (D):
# RateLimiter calls datetime.now() directly (concrete dependency).
# This required patching the module-level datetime import to control the clock.
# Recommendation: inject a Clock abstraction (callable or Protocol) so tests
# can pass a fake clock without patching globals — easier to test, clearer contract.
```

```typescript
// ⚠ SOLID — Single Responsibility (S):
// NotificationManager handles routing, rate limiting, and persistence in one class.
// This test requires mocks for UserRepository, EmailService, SmsService, and
// RateLimitStore — four separate concerns.
// Recommendation: extract ChannelRouter and RateLimiter; NotificationManager
// should orchestrate them, not own their logic.
```

```java
// ⚠ SOLID — Interface Segregation (I):
// CartService depends on InventoryService, which exposes 9 methods.
// Only checkStock() is used here; the other 8 add noise to every stub setup.
// Recommendation: introduce a narrow StockChecker interface with checkStock() only.
```

**What to scan for — the five principles:**

| Principle | Testability signal | What to flag |
|-----------|-------------------|-------------|
| **S — Single Responsibility** | Many unrelated `@Mock` fields; enormous `setUp`; tests that feel like they're testing two different things | Class does too many things — suggest splitting |
| **O — Open/Closed** | Parametrized tests that enumerate all type variants; `if/else` or `switch` on a type string | Type-switching logic that requires changing the class for every new variant — suggest a strategy or polymorphic approach |
| **L — Liskov Substitution** | Subclass tests that skip or override parent assertions; subtype throws where parent returns | Subtype violates the parent's contract — flag the broken invariant |
| **I — Interface Segregation** | Mock has many methods but test only uses a few; wide stub setup with no-op returns | Dependency interface is too wide — suggest narrowing |
| **D — Dependency Inversion** | No interface to mock; patching a concrete class or module; `new ConcreteService()` in SUT constructor; direct calls to `datetime.now()`, `System.currentTimeMillis()`, static methods | SUT depends on concretion — suggest extracting an interface or injecting an abstraction |

**When to flag vs. when to stay silent:**

- **Flag** if the violation directly complicates the test (forces a patch, forces a wide mock, forces a complex setUp). The test being hard to write is the signal that the design has a problem.
- **Flag** if there is no interface to mock — name what interface is needed and where it should live.
- **Stay silent** if the design is straightforward even without perfect SOLID compliance (e.g. a pure function with no dependencies needs no comment).

**Tone:** coaching, not scolding. One sentence on what the problem is, one sentence on why it matters for testing, one concrete recommendation. Then write the tests against the current design — do not refuse to test imperfect code.

---

### 1. Generate Tests from Source Code

1. Complete Step 0
2. Read the source file (path or pasted code)
3. Identify: public methods/functions, branches, error paths, boundary conditions
4. If the input includes a numbered spec, requirement list, or section headings — treat each numbered item as an AC. Group tests into classes or `@Nested` blocks per requirement and add traceability comments (`# AC-1: add item to cart`) above each test, exactly as Workflow 2 does. If the input is raw source code with no spec, group tests by method under test.
5. Apply the plugin's conventions — file layout, test structure, naming, mocking approach
6. Generate a complete test file: happy path, error cases, edge cases, boundaries
   **Test double rule — apply whenever a test uses any double (skip if `"doubleComments": false` in `.tdd-coach.json`):**
   For every test double in the generated file, add a comment on the same line (or immediately above the declaration) that states:
   1. The **type** of double (Dummy, Stub, Fake, Spy, or Mock)
   2. **Why** that type was chosen — what it controls or verifies
   3. **What the test expects it to do** (what value it returns, or what interaction it records)
   Use the decision flowchart in the `## Test Doubles` section to pick the right type. Examples:
   - `// stub — returns SAVE10 discount so we can verify SUT applies 10% correctly`
   - `// mock — verifies save() was called with status=CONFIRMED (the observable output)`
   - `// dummy — logger required by constructor but irrelevant to this discount test`
   - `// spy — real send() must execute; records args so we can verify recipient address`
   - `// fake — in-memory CartRepository; realistic behaviour without a database`
7. **Tag EVERY test** — no exceptions — using the framework's native mechanism:
   - `@pytest.mark.happy_path` / `@pytest.mark.negative` / `@pytest.mark.edge` / `@pytest.mark.boundary` (Pytest)
   - `[happy-path]` / `[negative]` / `[edge]` / `[boundary]` name prefixes inside `describe` groups (Jest/Vitest)
   - `@Tag("happy-path")` / `@Tag("negative")` / `@Tag("edge")` / `@Tag("boundary")` (JUnit 5)
   - `@Category(HappyPath.class)` / `@Category(Negative.class)` / `@Category(Edge.class)` / `@Category(Boundary.class)` (JUnit 4)

   **Tag assignment rules — apply these literally, no exceptions:**
   - Happy path / normal flow → `happy-path` (every test must have at least one tag)
   - Raises exception / returns error / rejects invalid input → `negative`
   - Unusual but valid input: None, null, empty string, zero, max value, unicode, non-existent key, float precision → `edge`
   - Value at the exact boundary of a stated rule (limit-1, limit, limit+1) → `boundary`
   - A test can carry multiple tags when it genuinely covers both (e.g. rejecting the 51st item is both `@pytest.mark.boundary` + `@pytest.mark.negative`)

   **Common misses — always check these before outputting:**
   - Handling a non-existent / missing key gracefully → `edge`
   - `None` or `null` input that is accepted (not just rejected) → `edge`
   - Zero-value inputs (zero price, zero quantity, empty cart total) → `edge`
   - Tests that verify no-op or silent behaviour on bad input → `edge`

8. **Self-check before outputting**: scan every `def test_` / `it(` / `@Test` in the generated file. Read the test body. Apply the tag rules above to each test. **Every test must have at least one tag — no untagged tests.** Any test missing a tag is a defect — fix it before outputting. Also verify that every test double in the file has a type comment explaining what it is and why — unless `"doubleComments": false` is set in `.tdd-coach.json`. Do not skip this check.
9. **Done when**: every public method has at least one test; all exception/error branches are explicitly exercised; **every test (happy path, negative, edge, and boundary) is tagged**; every test double is labelled with its type and purpose; test names read as specifications; if input had numbered requirements, every test has a traceability comment

---

## Safe Refactoring — Characterisation Tests for Legacy Code

> **This is not TDD.** TDD means writing a test before the code exists. This section is for the opposite situation: you have existing code with no tests and you need to refactor it safely. The goal is not to describe what the code *should* do — it's to pin down what it *currently does* so any refactor that breaks behaviour is caught immediately.
>
> If your team has no tests at all, start here before introducing TDD. Get a safety net first, then adopt TDD for new work.

1. Complete Step 0
2. Read the source file; note all observable outputs, return values, and side effects
3. Generate **characterisation tests** — tests that record the current behaviour, even if that behaviour seems wrong or surprising:
   - Call every public method with representative inputs
   - Assert the exact output the code produces right now (not what you'd expect it to produce)
   - Do not fix bugs during this phase — capture them as-is; the test is a snapshot, not a spec
4. Mark any tests that capture suspicious behaviour with a comment: `# characterisation — verify this is intentional`
5. Tell the user: *"These tests pin the current behaviour. Run them green first, then refactor. Any test that goes red means the refactor changed observable behaviour — intentional or not."*

**Done when**: the full test suite passes against the current (unmodified) source. The team now has a safety net to refactor against. Once it's green, new features and bug fixes can be driven by TDD (Workflow 4).

---

### 2. Generate Tests from Acceptance Criteria

Works from pasted text — user story, numbered ACs, Gherkin, Jira ticket body, numbered spec sections. No API calls needed.

1. Complete Step 0
2. Parse pasted text for acceptance criteria in any format: numbered list, Gherkin Given/When/Then, bullet ACs, numbered spec sections
3. Map each criterion to one or more test cases; when an AC implies a boundary, generate both sides (e.g. "locks after 5 failures" → test that 5th attempt is still allowed AND test that 6th triggers lock)
4. **Group tests by AC** — use a class per AC group (Pytest), `@Nested` block per AC (JUnit 5), or `describe` block per AC (Jest). Name the class/block after the AC: `class TestAddItemToCart`, `class TestCalculateTotal`, etc.
5. Add traceability comments above each test linking it to its AC number: `# AC-1: user can add item with SKU and quantity`
6. Generate tests using the loaded plugin's conventions. **For every test double in the generated file, add a comment stating its type, why it was chosen, and what the test expects it to do** — same rule as Workflow 1, step 6.
7. **Tag EVERY test** — same rules and self-check as Workflow 1 steps 7–9 (including the double-labelling check). The groupings and the tags are both required — do not produce one without the other.

**AC → test name mapping:**

| AC text | Generated test name |
|---|---|
| "User can log in with valid credentials" | `test_login_valid_credentials_returns_token` |
| "Invalid password returns 401" | `test_login_invalid_password_returns_401` |
| "Account locks after 5 failed attempts" | `test_login_locks_after_five_failures` |
| "Account locks after 5 failed attempts" | `test_login_sixth_attempt_returns_423_locked` |

**Done when**: every AC maps to at least one test; AC edge cases have boundary tests on both sides; every test has a traceability comment; **every test (happy path, negative, edge, and boundary) is tagged**; every test double is labelled with its type and purpose; groupings reflect the AC structure.

### 3. Analyze Coverage Gaps

1. Complete Step 0
2. Read the coverage report file provided by the user (LCOV, JSON, or XML/Cobertura)
3. Parse uncovered lines and branches; classify each gap:
   - **P0** — uncovered error/exception paths, security logic, payment flows
   - **P1** — uncovered branches in core business logic
   - **P2** — uncovered utility functions, low-risk helpers
4. Generate missing tests for P0 gaps using the active plugin's patterns
5. **Done when**: P0 gaps have generated tests; P1/P2 gaps are listed with priority rationale

**Coverage targets (override via `coverageThreshold` in `.tdd-coach.json`):**

| Metric | Target |
|---|---|
| Line | 80%+ |
| Branch | 70%+ |
| Function / method | 90%+ |
| Auth, payments, validation | 100% |

### 4. Red-Green-Refactor Cycle

Designed to be run iteratively, one requirement at a time.

- **RED** — Write a failing test for exactly one requirement. **STOP after writing the test. Do not write implementation code.** Wait for the user to run the test and confirm it fails. After generating the test, always explain *(skip if `"verbose": false` in `.tdd-coach.json`)*:
  1. **Why it will fail** — is it a missing module (import error), a missing class/method (runtime error), or a failing assertion? Each has a different meaning.
  2. **What the correct RED failure looks like** — the test must reach the assertion and fail there. A test that fails on a syntax error or unresolved import is not RED — it's broken.
  3. **What to create to get to true RED** — e.g. "create an empty `TransferLimitService` class and stub `canTransfer` to throw `NotImplementedError` — then the tests will load and fail on assertions, which is the real RED state."
  4. **Which test doubles are needed and why** *(skip if `"verbose": false`)* — before writing the test, identify every dependency the SUT will need. For each one:
     - Name the double type (Dummy, Stub, Fake, Spy, or Mock) and explain why that type was chosen.
     - **If the dependency touches anything external** (database, HTTP, email, file system, clock, queue) — check whether an interface already exists for it. If not, flag it: *"Consider extracting a `PaymentGateway` interface before writing this test — the SUT should depend on the abstraction, not the Stripe SDK directly. This is what makes the test double possible and the design modular."*
     - Write a short paragraph above the test summarising the doubles chosen:
       > *"This test needs two doubles: a **stub** for `DiscountService.getRate` — we need it to return a fixed 10% so we can verify the SUT applies it correctly — and a **dummy** for `AuditLogger` — the constructor requires it but discount calculation doesn't depend on logging. I am not using a mock on `DiscountService` because the test's assertion is on the calculated total (output), not on whether `getRate` was called (interaction)."*

  Then write the test with each double labelled in a comment (e.g. `// stub — returns 0.10 so we can verify 10% is applied to the total`) — unless `"doubleComments": false`.

  > **If you didn't watch the test fail, you don't know if it tests the right thing.** A test that has never been red could be passing for the wrong reason — it might be testing a mock, testing an already-implemented path, or simply not running. Confirm failure before writing any implementation.

- **GREEN** — Write the minimum code needed to make the test pass. No extra logic, no early abstraction. If in doubt, write the simplest thing that could possibly work.
- **REFACTOR** — Improve the structure of the implementation without changing its behaviour. Run the full test suite after every change.
- Commit after each GREEN phase. Then move to the next requirement and repeat.

### 5. Review Existing Test Quality

1. Complete Step 0
2. Read the test file
3. Score across four dimensions:

| Dimension | What good looks like |
|---|---|
| **Isolation** | No shared mutable state; tests pass in any order |
| **Assertion quality** | Specific values asserted — not `assert result is not None` |
| **Naming** | Test name reads as a specification without needing to read the body |
| **Determinism** | No dependency on system time, random seeds, or live network calls |

4. List detected smells with specific line references:
   - **Assertion roulette** — multiple unrelated assertions in one test body
   - **Mystery guest** — test depends on file or DB state set up outside the test
   - **Eager test** — one test method exercises multiple distinct behaviours
   - **Weak assertion** — `assert token` instead of `assert len(token) == 64`
   - **Slow unit test** — unit test taking over 100ms (usually means a real I/O call)
5. Output refactored versions with before/after examples for each detected smell

### 6. Generate Fixtures and Mocks

1. Complete Step 0
2. Identify what the user needs: typed test data, mock objects, stubs, spy wrappers
3. Generate fixtures that cover boundary values and representative equivalence classes
4. For mocks: follow the active plugin's mocking strategy (e.g. `unittest.mock` for Pytest, `jest.spyOn` for Jest, `@MockBean` for Spring Boot slices)
5. Output ready-to-use code, not just structure sketches

---

## Test Granularity — Unit vs. Integration

This skill defaults to **unit tests** because they're fast, isolated, and directly tied to the code being generated. But unit tests are not always the right tool.

### The testing trophy (practical guide)

```
        /\
       /  \   ← E2E (few, slow, high confidence in full flows)
      /----\
     /      \ ← Integration (moderate, test real behaviour across layers)
    /--------\
   /          \ ← Unit (many, fast, test logic in isolation)
  /------------\
 /              \ ← Static analysis / types (free, catches whole classes of bugs)
```

**Unit tests are best for:** pure functions, complex business logic, edge cases and boundaries, anything with many input combinations. They run fast and give precise failure messages.

**Integration tests are best for:** behaviour that spans multiple components (service + repository + domain model), anything where mocking every collaborator would make the test less trustworthy than just using the real thing, and tests that need to survive internal refactors without being rewritten.

**The warning sign that you have too many unit tests:** a refactor that doesn't change any user-facing behaviour breaks dozens of tests. Those tests are coupled to implementation details, not behaviour. They're maintenance overhead, not safety net.

### Default guidance per workflow

| Situation | Recommended granularity |
|---|---|
| Pure function, complex logic, many branches | Unit test |
| Service method that calls a repository | Unit test with mocked repo (fast) **or** integration test with real repo (more trustworthy) — ask the user |
| API endpoint / HTTP handler | Integration test (Supertest, `@WebMvcTest`, pytest HTTP client) |
| Full user flow across multiple services | E2E or integration — not a unit test |
| Legacy code characterisation (Workflow 1b) | Integration-level where possible — captures real behaviour, not mocked behaviour |

When generating tests from a spec or AC list, **ask the user** if they want unit or integration coverage if the boundary isn't clear from context. Don't default to heavy mocking without checking — a test that mocks every collaborator may give false confidence.

---

## When to Stop and Ask vs. Continue

### Determine mode first — but default to TDD, don't ask

| Signal | Mode | What to do |
|---|---|---|
| Source file has code in it | **Test existing code** | Read it. Test exactly what's there. Do not invent behaviour. |
| Source file exists but is **empty** | **TDD** | The file name names the domain. **Do NOT proceed. Ask scope, interface, contracts, framework before generating anything.** |
| User pastes code | **Test existing code** | Same as above. |
| Spec, ACs, or user story provided | **TDD** | Generate RED phase tests. No mode question needed. |
| Just a description, no file, no spec | **TDD** | Default to TDD. Do not ask mode. **Ask scope, interface, contracts, framework before generating anything.** |

**Default is always TDD.** Do not ask "do you have existing code?" — if there's no code visible, assume TDD.

**Do not invent requirements.** An empty file or a bare description is not a spec. Guessing scope, interface shape, and error contracts produces tests for code the user never asked for. **Ask first. Always.**

> **Anti-pattern to avoid:** Stating "I'll proceed with reasonable defaults" and generating tests without asking. This is wrong even when the user seems to want quick output. The questions take one round trip. Invented tests waste more time than that.

**When a source file is provided:** generate tests that cover exactly what the code does — its public methods, their branches, their error paths. Nothing more. Let the developer say if they want edge case expansion.

**When only a vague description or empty file is given:** ask the clarifying questions below first, then generate. Do not skip this step.

### What to ask when input is vague

Ask only what is genuinely unknown. Group questions; never ask one at a time over multiple turns. Cover these areas.

**Stop after asking. Output only the questions. Do not answer them yourself. Do not continue past the question block. Your next output after the questions must be silence — wait for the user's reply before generating any tests.**

> **Why this matters:** Generating questions and then answering them yourself produces tests for a function you invented. The user's `ApplyTax.py` is empty — you have zero information about what it should do. Guessing scope, interface, and error contracts and then generating tests against your own guesses is not TDD. It is fiction.

**1. Mode — source or spec?**
> "Do you have existing code to test, or are we doing TDD (write failing tests before the code exists)?"

**2. Scope — what operations/behaviours?**
> "What should it support? e.g. add, subtract, multiply, divide — or more?"
> Do not assume scope from the domain name. "Calculator" does not imply sqrt, power, expression parsing, or history unless stated.

**3. Interface shape**
> "Is this a class (`new Calculator().add(2,3)`), standalone functions (`add(2,3)`), or an expression evaluator (`evaluate('2+3')`)?"

**4. Error and boundary contracts** — ask about anything with a non-obvious answer:
> - Division by zero: throw an Error, return Infinity, return null?
> - Invalid inputs (strings, NaN): throw, coerce, or ignore?
> - Floating point: does `0.1 + 0.2` need to equal `0.3` (i.e. do you need rounding/precision handling)?

**5. Framework** (if not detected)
> "Jest, Vitest, or Mocha+Chai?"

**If the user skips, dismisses, or ignores the questions — do not proceed.** Say:
> "I need answers to generate useful tests. Without knowing the interface shape and error contracts, any tests I write would be for a function I invented. Please answer the questions above, or paste even a rough description of what `ApplyTax` should do."

Do not generate. Do not list assumptions and proceed anyway. Wait for a real answer.

Once **all answers are in**, generate:
- One happy-path test per stated operation
- One test per error/boundary contract stated above (div-by-zero, invalid input, etc.)
- `it.each` / `@ParameterizedTest` / `@pytest.mark.parametrize` for boundary values — only if the contract defines them
- Do NOT add tests for language runtime behaviour (IEEE 754 float math, JS type coercion) unless the spec calls for it
- State any remaining assumptions explicitly at the end; offer to expand

**Do not skip to this step.** "State remaining assumptions" means assumptions left over *after* asking and receiving answers — not a substitute for asking.

### Stop and ask when:

- Scope of the feature is unknown — ask what operations/behaviours to cover (all in one message)
- Framework cannot be detected and the user hasn't specified one
- Error/boundary contracts are non-obvious (div-by-zero, invalid input, float precision) — ask before inventing
- Acceptance criteria conflict or leave boundary values undefined
- Logic touches auth, payments, encryption, or PII — confirm test scenarios before writing
- An external dependency has no documented contract or spec

### Continue without asking when:

- Source file is provided — read it and test what's there
- ACs are numbered and each maps directly to a test
- Pure functions with typed inputs and typed outputs — interface is self-describing
- OpenAPI spec or typed interface is available
- The codebase has existing tests with clear patterns to follow
- Standard CRUD operations with well-defined models

> Do not stop based on test *count*. Fifty parametrised tests for a discount calculator need no human input. Three tests on undocumented payment rules do.
>
> Do not invent scope. "Calculator in TS" does not imply sqrt, power, history, or float precision tests unless the user or spec says so.
>
> Ask everything in one message. Do not drip-feed one question per turn.

---

## Framework Plugins

All framework-specific patterns — file layout, test structure, mocking, async handling, coverage config, gotchas — live in the `frameworks/` directory. The root SKILL.md (this file) routes to the right plugin; the plugin does the heavy lifting.

| Plugin | Stack | What it covers |
|---|---|---|
| `frameworks/jest/SKILL.md` | TypeScript/JS · Jest 29+ | Module mocks, `jest.spyOn`, timer mocks, snapshot tests, coverage config, `clearAllMocks` vs `restoreAllMocks` |
| `frameworks/vitest/SKILL.md` | TypeScript/JS · Vitest 0.34+ | `vi` mocking API, in-source tests, Vite integration, coverage via `@vitest/coverage-v8` |
| `frameworks/mocha-chai/SKILL.md` | TypeScript/JS · Mocha + Chai | `expect`/`assert`/`should` assertion styles, Sinon stubs and spies, `chai-http`, ESM vs CJS setup |
| `frameworks/pytest/SKILL.md` | Python 3.9+ · Pytest 7+ | `@pytest.mark.parametrize`, `conftest.py` fixtures, `unittest.mock`, `pytest-asyncio`, Hypothesis |
| `frameworks/junit5/SKILL.md` | Java 11+ · JUnit 5 + AssertJ | `@ParameterizedTest`, `@Nested`, Mockito `@ExtendWith`, AssertJ fluent assertions, lifecycle hooks |
| `frameworks/junit4/SKILL.md` | Java 8+ · JUnit 4 + AssertJ | `@RunWith`, `@Before`/`@After`, flat naming, `Parameterized` runner, `MockitoRule`, gotchas |
| `frameworks/spring-boot/SKILL.md` | Java · Spring Boot 2.7+ / 3.x | `@WebMvcTest`, `@DataJpaTest`, `@MockBean` vs `@Mock`, `@WithMockUser`, `spring-security-test` dependency |
| `frameworks/playwright/SKILL.md` | TypeScript · Playwright 1.40+ | Component mounting options, locator strategy, accessibility assertions, network interception |

---

## Test Doubles

**Test doubles** are objects that stand in for real dependencies during a test. Using the wrong type is the most common cause of tests that pass for the wrong reason, break on innocent refactors, or miss real bugs. Each type has a precise definition — use the right one for what you actually need to verify.

### Definitions (apply these exactly when generating tests)

| Type | Definition | Why you use it |
|------|-----------|----------------|
| **Dummy value** | A value that is required for the tested interface but the test case does not depend on it | The constructor or method requires the parameter, but its value is irrelevant to what this test verifies. Passing a dummy makes intent explicit: *this dependency does not matter here.* |
| **Stub** | Provides static (hardcoded) input to the SUT — no assertion on whether it was called | You need to control what a dependency *returns* so you can verify how the SUT *reacts* to it. The stub is the cause; the SUT's output is the effect. |
| **Fake** | A relatively full-function implementation that is better suited to testing than the production version (e.g., an in-memory database instead of a database server) | The real dependency is too slow, too complex, or unavailable in tests, but you need realistic behaviour — not just a hardcoded return value. Fakes are hand-written, not generated by a mocking library. |
| **Spy** | Supports setting the output of a call *before* the test runs **and** verifying the input parameters *after* the test runs — the real method still executes | You want to verify what the SUT passed to a collaborator *and* you want the real collaborator to run. Spies record calls without replacing behaviour. |
| **Mock** | Verifies output via expectations defined *before* the test runs — the real method does not execute | The interaction itself is the observable output: "was the repository saved?", "was the email queued?", "was the payment charged?". Expectations are set up first; the mock fails if they are not met. |

> **When generating tests, label each double type in a comment.** Seeing `# stub — controls return value` vs `# mock — verifies save was called` makes the test's intent immediately clear to the reader, and makes it easier to catch the wrong choice.

---

### Doubles as a design signal — the interface rule

Using a test double on an external dependency (database, email service, payment gateway, HTTP client, file system) is not just a testing technique — **it's a design signal that an interface is missing.**

The correct pattern when a dependency touches something external:

1. **Define an interface** that describes the access your code needs — not the full API of the external system, just the operations your SUT actually calls. (This is the Dependency Inversion Principle: depend on an abstraction, not a concrete implementation.)
2. **Write two implementations**: one that calls the real external system (used in production), and one that is a test double — a fake, stub, or mock.
3. **Inject the interface** into the SUT via the constructor (preferred) or a setter.

```python
# Interface (Python — use Protocol or ABC)
class PaymentGateway(Protocol):
    def charge(self, amount_cents: int, token: str) -> ChargeResult: ...

# Production implementation
class StripeGateway:
    def charge(self, amount_cents: int, token: str) -> ChargeResult:
        return stripe.charge(amount_cents, token)   # real Stripe call

# Test double — fake with controllable behaviour
class FakePaymentGateway:
    def __init__(self):
        self.charged: list[tuple] = []
        self.should_fail = False

    def charge(self, amount_cents: int, token: str) -> ChargeResult:
        if self.should_fail:
            raise PaymentDeclinedError("card declined")
        self.charged.append((amount_cents, token))
        return ChargeResult(success=True, charge_id="fake-123")

# SUT depends on the interface, not Stripe
class CheckoutService:
    def __init__(self, gateway: PaymentGateway): ...
```

**When the skill encounters a test that needs a double for an external dependency, it should:**
- Check whether an interface already exists. If not, note it: *"Consider extracting a `PaymentGateway` interface — this makes the boundary explicit and lets you swap implementations without changing `CheckoutService`."*
- Generate the double to satisfy the interface, not the concrete class.
- If a fake is appropriate, generate it as a standalone class, not inline mock setup.

> This is the pattern that makes TDD a design tool rather than just a verification tool. The pressure to write a test first forces you to define the boundary. The interface is the boundary made explicit.

---

### Decision flowchart — pick the right double

```
Does the test depend on the value of this dependency at all?
  └─ No → Dummy value

Does the test assert on what the SUT returned or computed?
  └─ Yes → Stub (configure the dependency's return value; assert on the SUT output)

Does the test assert that the SUT called the dependency?
  └─ Yes, AND the real dependency should also execute → Spy
  └─ Yes, AND the real dependency must NOT execute → Mock

Is the dependency too complex for a stub but too slow/unavailable for the real thing?
  └─ Yes → Fake (write a lightweight working implementation)
```

---

### All five patterns — Python (`unittest.mock`)

```python
from unittest.mock import MagicMock, patch
import pytest
from src.order_service import OrderService
from src.discount_service import DiscountService

# ── 1. DUMMY VALUE ────────────────────────────────────────────────────────────
# AuditLogger is required by the constructor but this test doesn't care about
# audit logging at all. Passing a MagicMock() makes intent explicit.
@pytest.mark.happy_path
def test_calculates_discount_correctly():
    dummy_logger = MagicMock()            # dummy — never asserted on
    stub_discount = MagicMock()           # stub — see below
    service = OrderService(discount_svc=stub_discount, logger=dummy_logger)

    stub_discount.get_rate.return_value = 0.10   # stub configuration

    total = service.calculate_total(subtotal=100.0)

    assert total == 90.0                  # assert on SUT output, not on the stub


# ── 2. STUB ───────────────────────────────────────────────────────────────────
# We need find_by_code to return a specific code so we can verify how the
# cart service reacts. No assertion on whether find_by_code was called.
@pytest.mark.happy_path
def test_checkout_applies_10_percent_discount(monkeypatch):
    monkeypatch.setattr(
        'src.discount_repo.find_by_code',
        lambda code: DiscountCode(code='SAVE10', pct=10)   # stub — static input
    )

    total = cart_service.checkout(cart, discount_code='SAVE10')

    assert total == 90.0                  # assert on output, not on stub


# ── 3. FAKE ───────────────────────────────────────────────────────────────────
# Using a real database in unit tests is too slow. FakeDiscountRepository is a
# lightweight in-memory implementation — realistic behaviour without the server.
class FakeDiscountRepository:
    """In-memory fake — better suited to testing than the real DB repository."""
    def __init__(self):
        self._codes: dict[str, object] = {}

    def add(self, code) -> None:
        self._codes[code.code] = code

    def find_by_code(self, code: str):
        return self._codes.get(code)

@pytest.fixture
def fake_repo():
    repo = FakeDiscountRepository()
    repo.add(DiscountCode(code='SAVE10', pct=10))
    return repo

@pytest.mark.happy_path
def test_checkout_with_fake_repository(fake_repo):
    service = CartService(discount_repo=fake_repo)   # fake — realistic behaviour
    total = service.checkout(cart, discount_code='SAVE10')
    assert total == 90.0


# ── 4. SPY ────────────────────────────────────────────────────────────────────
# We want to verify the email was sent to the right address, AND we want the
# real EmailService.send() to actually execute (e.g., to test serialisation).
@pytest.mark.happy_path
def test_confirmation_email_sent_to_correct_address():
    from src.email_service import EmailService
    real_email = EmailService()
    # wraps= keeps the real method running; calls are recorded
    with patch.object(real_email, 'send', wraps=real_email.send) as spy:
        order_service.confirm_order(user_id='u-1', cart=cart, email_svc=real_email)

        # verify input parameter AFTER the test ran — that's what makes it a spy
        spy.assert_called_once()
        assert spy.call_args.kwargs['to'] == 'u-1@example.com'


# ── 5. MOCK ───────────────────────────────────────────────────────────────────
# The observable output of confirm_order is that the order was persisted.
# We can't query a real DB, so we use a mock and verify the interaction.
# Expectation (what should be called) is known before the test runs.
@pytest.mark.happy_path
def test_confirm_order_persists_order():
    mock_repo = MagicMock()               # mock — will verify interaction
    service = OrderService(repo=mock_repo, logger=MagicMock())   # logger = dummy

    service.confirm_order(user_id='u-1', cart=cart)

    # assert interaction AFTER — was save() called with the right order?
    mock_repo.save.assert_called_once()
    saved = mock_repo.save.call_args.args[0]
    assert saved.user_id == 'u-1'
    assert saved.status == 'confirmed'
```

---

### All five patterns — Jest / TypeScript

```typescript
import { OrderService } from '../src/orderService';

// ── 1. DUMMY VALUE ────────────────────────────────────────────────────────────
// AuditLogger is required by the constructor — this test doesn't care about it.
it('[happy-path] calculates discount correctly', () => {
  const dummyLogger = { log: jest.fn() };                 // dummy — never asserted on
  const stubDiscount = { getRate: jest.fn() };            // stub — see below
  const service = new OrderService(stubDiscount, dummyLogger);

  stubDiscount.getRate.mockReturnValue(0.10);             // stub: static input

  expect(service.calculateTotal(100)).toBe(90);           // assert on SUT output
});


// ── 2. STUB ───────────────────────────────────────────────────────────────────
// findByCode needs to return a specific code. We configure the return value
// before calling the SUT, then assert on what the SUT produced.
it('[happy-path] applies 10% discount from code', async () => {
  discountRepo.findByCode.mockResolvedValue({ code: 'SAVE10', pct: 10 }); // stub

  const total = await cartService.checkout(cart, 'SAVE10');

  expect(total).toBe(90);    // assert on SUT output — no expect(discountRepo...) here
});


// ── 3. FAKE ───────────────────────────────────────────────────────────────────
// FakeDiscountRepository is a lightweight working implementation.
// It behaves like the real thing but uses a plain Map — no DB required.
class FakeDiscountRepository {
  private codes = new Map<string, { code: string; pct: number }>();

  add(code: { code: string; pct: number }) { this.codes.set(code.code, code); }
  findByCode(code: string) { return Promise.resolve(this.codes.get(code) ?? null); }
}

it('[happy-path] applies discount via fake repository', async () => {
  const fakeRepo = new FakeDiscountRepository();   // fake — realistic behaviour
  fakeRepo.add({ code: 'SAVE10', pct: 10 });

  const service = new CartService(fakeRepo);
  const total = await service.checkout(cart, 'SAVE10');

  expect(total).toBe(90);
});


// ── 4. SPY ────────────────────────────────────────────────────────────────────
// Real emailService.send() must execute. We also want to verify what it
// received. jest.spyOn WITHOUT mockReturnValue = spy (real method runs).
import * as emailService from '../src/emailService';

it('[happy-path] sends confirmation to correct address', async () => {
  const sendSpy = jest.spyOn(emailService, 'send'); // spy — real method runs

  await orderService.confirmOrder('u-1', cart);

  // verify input parameters AFTER the test ran
  expect(sendSpy).toHaveBeenCalledWith(
    expect.objectContaining({ to: 'u-1@example.com' })
  );
});
// ⚠️ Adding .mockReturnValue() or .mockResolvedValue() here turns it into a Mock —
//    the real send() would no longer run.


// ── 5. MOCK ───────────────────────────────────────────────────────────────────
// The observable output is that the order was saved.
// Expectation is configured BEFORE calling the SUT.
it('[happy-path] persists order on confirm', async () => {
  const mockRepo = { save: jest.fn().mockResolvedValue({ id: 'order-1' }) }; // mock
  const dummyLogger = { log: jest.fn() };                                     // dummy
  const service = new OrderService(mockRepo, dummyLogger);

  await service.confirmOrder('u-1', cart);

  // verify the interaction — was save called with the right shape?
  expect(mockRepo.save).toHaveBeenCalledWith(
    expect.objectContaining({ userId: 'u-1', status: 'confirmed' })
  );
});
```

---

### All five patterns — Mockito (JUnit 4 / 5)

```java
// JUnit 5 shown; for JUnit 4 substitute @RunWith(MockitoJUnitRunner.class)
// and @Category(HappyPath.class) for @Tag("happy-path").

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    // ── 1. DUMMY VALUE ──────────────────────────────────────────────────────
    // AuditLogger is required by the constructor.
    // This test verifies discount calculation — logging is irrelevant.
    @Mock
    private AuditLogger dummyLogger;        // plain Mockito @Mock — used as dummy here;
                                            // given()/then() never called on it in this test

    @Mock
    private DiscountService stubDiscount;   // plain Mockito @Mock — used as stub here

    @InjectMocks
    private OrderService orderService;

    @Test
    @Tag("happy-path")
    void shouldCalculateDiscountCorrectly() {
        // Stub: configure what the dependency returns BEFORE calling the SUT
        given(stubDiscount.getRate("SAVE10")).willReturn(0.10);

        BigDecimal total = orderService.calculateTotal(new BigDecimal("100.00"), "SAVE10");

        // Assert on SUT output — no then(stubDiscount).should() here
        assertThat(total).isEqualByComparingTo("90.00");
    }


    // ── 2. STUB ─────────────────────────────────────────────────────────────
    // We need findByCode to return a specific code.
    // Stub configures the return value; test asserts on what the SUT produced.
    @Test
    @Tag("happy-path")
    void shouldApply10PercentDiscount() {
        given(discountRepo.findByCode("SAVE10"))           // stub — static input
            .willReturn(new DiscountCode("SAVE10", 10));

        BigDecimal total = cartService.checkout(cart, "SAVE10");

        assertThat(total).isEqualByComparingTo("90.00");  // assert on output
        // No then(discountRepo).should()... — that would make it a mock
    }


    // ── 3. FAKE ─────────────────────────────────────────────────────────────
    // FakeCartRepository is a lightweight working implementation.
    // The real JPA repository requires a database; this uses a HashMap.
    static class FakeCartRepository implements CartRepository {
        private final Map<String, Cart> store = new HashMap<>();

        @Override
        public Optional<Cart> findByUserId(String userId) {
            return Optional.ofNullable(store.get(userId));   // realistic behaviour
        }

        @Override
        public Cart save(Cart cart) {
            store.put(cart.getUserId(), cart);
            return cart;
        }
    }

    @Test
    @Tag("happy-path")
    void shouldSaveAndRetrieveCart_withFakeRepository() {
        CartService service = new CartService(
            new FakeCartRepository(),   // fake — full behaviour, no DB
            mock(EmailService.class)    // dummy — not exercised in this test
        );
        service.addItem("u-1", new CartItem("sku-1", 1));
        Optional<Cart> found = service.getCart("u-1");
        assertThat(found).isPresent();
        assertThat(found.get().getItems()).hasSize(1);
    }


    // ── 4. SPY ──────────────────────────────────────────────────────────────
    // Real EmailService.send() must execute (e.g., serialisation is part of
    // the test). @Spy wraps the real object and records all calls.
    @Spy
    private EmailService emailSpy = new EmailService();   // spy — real method runs

    @Test
    @Tag("happy-path")
    void shouldSendEmailToCorrectAddress() {
        orderService.confirmOrder("u-1", cart);

        // verify what was passed AFTER the test ran — real send() also executed
        then(emailSpy).should().send(argThat(email ->
            email.getTo().equals("u-1@example.com")
        ));
    }


    // ── 5. MOCK ─────────────────────────────────────────────────────────────
    // The observable output of confirmOrder is that the order was persisted.
    // Expectation is set via then().should() AFTER the call (BDD style),
    // or via verify() in classic style. Real save() does not run.
    @Mock
    private OrderRepository mockOrderRepo;   // plain Mockito @Mock — used as mock here;
                                             // then().should() will verify the interaction

    @Test
    @Tag("happy-path")
    void shouldPersistOrderOnConfirm() {
        orderService.confirmOrder("u-1", cart);

        // verify the interaction — was save() called with the right order?
        then(mockOrderRepo).should().save(argThat(order ->
            order.getUserId().equals("u-1") &&
            order.getStatus() == OrderStatus.CONFIRMED
        ));
    }
}
```

---

### Common mistakes

| Mistake | What goes wrong | Fix |
|---------|----------------|-----|
| Using a mock when you only need a stub | Test asserts that a method was called when you only care what the SUT returned — breaks on refactors that don't change behaviour | Use a stub; assert on the SUT's return value, not on the dependency |
| Using a mock when you need a fake | 10-line `given()` chain for CRUD operations, duplicated across tests | Write a `FakeRepository` — 30 lines once, shared via a fixture |
| Setting up stubs that are never used | `MockitoJUnitRunner` / `MockitoExtension` fails with "unnecessary stubbing" | Remove unused `given()` calls, or use `lenient()` only when justified |
| Spying on the SUT itself | `@Spy CartService cartService` inside `CartServiceTest` — can't distinguish real from spied behaviour | Only spy on *collaborators*, never on the system under test |
| Not labelling which double type you're using | Reader has to reverse-engineer intent from mock setup | Add a comment: `// stub — controls return value` / `// mock — verifies save called` |

---

### Ask the skill to pick the right double and explain why

```
Generate tests for OrderService.confirmOrder().
For each dependency, identify which test double type to use (Dummy, Stub, Fake, Spy, or Mock)
and add a comment in the test explaining WHY that type was chosen.
Framework: JUnit 5
```

---

## Advanced Patterns

### Property-Based Testing

Use when the input space is large and the expected outcome can be described as an invariant rather than a concrete example.

**Python — Hypothesis:**
```python
from hypothesis import given, strategies as st
from app.serializers import serialize, deserialize

@given(st.text())
def test_roundtrip_preserves_value(data):
    """Serialize then deserialize must always return the original string."""
    assert deserialize(serialize(data)) == data
```

**TypeScript — fast-check:**
```typescript
import fc from 'fast-check';
import { encode, decode } from './codec';

test('encode/decode roundtrip', () => {
  fc.assert(fc.property(fc.string(), (s) => {
    expect(decode(encode(s))).toBe(s);
  }));
});
```

### Mutation Testing

Coverage tells you code was *executed*. Mutation testing tells you code was *verified* — it modifies production code and checks whether your tests catch the change.

| Language | Tool | Command |
|---|---|---|
| TypeScript/JS | Stryker | `npx stryker run` |
| Python | mutmut | `mutmut run --paths-to-mutate=src/` |
| Java | PIT | `mvn org.pitest:pitest-maven:mutationCoverage` |

Target **85%+ mutation score** on P0 paths: auth, payments, data validation. 100% line coverage with a 40% mutation score means your tests are watching code run, not verifying it.

---

## Scripts Reference

The `scripts/` directory contains Python CLI tools. All use stdlib only — no pip installs, no virtual environments needed. Requires Python 3.9+.

| Script | What it does | Example |
|---|---|---|
| `test_generator.py` | Generate test stubs from a source file or pasted code | `python scripts/test_generator.py --input src/auth/login.py --framework pytest` |
| `coverage_analyzer.py` | Parse LCOV / JSON / XML reports and classify gaps P0/P1/P2 | `python scripts/coverage_analyzer.py --report coverage/lcov.info --threshold 80` |
| `fixture_generator.py` | Generate typed test fixtures with boundary values | `python scripts/fixture_generator.py --entity User --count 5 --output fixtures/users.json` |
| `metrics_calculator.py` | Score a test file on isolation, assertions, naming, determinism | `python scripts/metrics_calculator.py --file tests/test_auth.py` |
| `framework_adapter.py` | Output framework-specific imports and test file structure | `python scripts/framework_adapter.py --framework jest --language typescript` |
| `format_detector.py` | Detect language and framework from source files | `python scripts/format_detector.py --input src/` |

---

## Customization

Teams can lock in their stack and enforce conventions without modifying this skill.

- **Set framework and conventions** → drop `.tdd-coach.json` in the project root. See `CUSTOMIZING.md` for the full key reference.
- **Override a built-in plugin** or add a new framework (Spock, NUnit, RSpec, etc.) → create a plugin file and optionally register it via `pluginDir`. See `WRITING_PLUGINS.md`.
- **Auto-run tests after every file write** → add a `PostToolUse` hook to `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "<your test command> 2>&1 | tail -20"
      }
    ]
  }
}
```

Replace `<your test command>` with your runner: `npx jest --no-coverage --watchAll=false`, `python -m pytest -x -q`, or `./mvnw test -q`. This gives Claude immediate RED/GREEN feedback during a TDD cycle without manual test runs.

Common `.tdd-coach.json` examples:
```json
{ "framework": "mocha-chai", "assertionLibrary": "chai-expect", "mockLibrary": "sinon" }
{ "framework": "pytest", "variant": "django" }
{ "framework": "spring-boot", "testSlices": ["webmvc"] }
```

---

## Limitations

| Area | Detail |
|---|---|
| Unit test scope | Integration and E2E tests need different approaches — see Playwright plugin for component-level UI testing |
| Static analysis only | Tests cannot be executed or validated for runtime correctness during generation |
| Spring Boot slices | `@WebMvcTest` / `@DataJpaTest` require Spring Boot 2.7+ / 3.x |
| Coverage report formats | LCOV, JSON (Istanbul/V8), and XML (Cobertura/JaCoCo) only — convert other formats before analysis |
| Business logic assertions | Generated tests provide correct structure and coverage of paths; assertions on domain rules should be reviewed before committing |
