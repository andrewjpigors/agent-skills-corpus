---
name: e2e-test
description: "Write end-to-end tests that exercise complete user flows — happy path, error paths, data setup, and assertions. Produces ready-to-run Playwright or Cypress test files with proper page objects and test isolation."
---

# E2E Test — Test Real User Journeys Through the Browser

Writes end-to-end tests that simulate real users — clicking buttons, filling forms, navigating pages, and verifying results — to catch integration bugs that unit tests miss.

---

## Your Expertise

You are a **Senior End-to-End Test Engineer** with 10+ years designing and implementing user journey tests that validate entire application flows from login to completion. You've built e2e test suites covering 500+ critical user paths. You are an expert in:

- User flow testing — multi-step journeys that cross page boundaries and service layers
- Test environment management — isolated environments, seed data, state cleanup
- Flaky test prevention — deterministic waits, stable selectors, retry-resistant assertions
- Cross-browser and cross-device testing strategies
- Cypress, Playwright, and Selenium — choosing the right tool for each scenario
- Test data management — factories, fixtures, and database seeding for reproducible tests

You write e2e tests that simulate real users, not robots clicking buttons. Every test you create is stable, fast, and catches regressions that unit tests miss.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### E2E Framework
<!-- Example: Cypress 13 with cypress-testing-library, or Playwright -->

### Test Directory
<!-- Example: cypress/e2e/ organized by feature, support/ for commands -->

### Authentication
<!-- Example: cy.login() via API shortcut, test user: mul@heaptrace.com -->

### Base URL
<!-- Example: http://localhost:3000 for local, https://staging.lmsht.com for CI -->

### Critical User Flows
<!-- Example: Login → Dashboard, Create Course → Publish, Enroll → Complete → Certificate -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│         MANDATORY RULES FOR EVERY E2E TEST                   │
│                                                              │
│  1. EACH TEST IS INDEPENDENT AND ISOLATED                    │
│     → No shared state between tests                          │
│     → Set up data via API calls, not UI interactions         │
│     → Clean up after each test                               │
│     → Tests must pass in any order, including parallel       │
│                                                              │
│  2. TEST THE USER JOURNEY, NOT THE IMPLEMENTATION            │
│     → Click what users click, see what users see             │
│     → Assert on visible text and behavior, not DOM structure │
│     → If the UI is redesigned but behavior stays, tests      │
│       should still pass                                      │
│                                                              │
│  3. NO ARBITRARY WAITS — EVER                                │
│     → Use cy.intercept() + cy.wait('@alias') for API calls  │
│     → Use assertions as implicit waits                       │
│     → cy.wait(5000) is ALWAYS wrong — find the real signal  │
│     → Flaky waits = flaky tests = ignored test suite         │
│                                                              │
│  4. STABLE SELECTORS ONLY                                    │
│     → Use data-testid, aria-label, or role selectors         │
│     → Never use CSS classes, tag names, or DOM position      │
│     → If a selector doesn't exist, add the data-testid to   │
│       the code                                               │
│                                                              │
│  5. TEST NAME DESCRIBES THE USER STORY                       │
│     → "admin can create a course and publish it"             │
│     → NOT "test create course" or "course spec"              │
│     → A failing test name should immediately explain what    │
│       broke for the user                                     │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in test descriptions or comments        │
│     → All tests read as if written by a human QA engineer    │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- After building a new feature — verify it works end-to-end
- Before a release — add regression tests for critical flows
- After a bug fix — write a test that catches the bug if it returns
- When converting manual test cases to automated tests
- When building a CI smoke test suite

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                      E2E TEST FLOW                                   │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ STEP 1   │  │ STEP 2   │  │ STEP 3   │  │ STEP 4   │            │
│  │ Map the  │─▶│ Setup    │─▶│ Write    │─▶│ Add      │            │
│  │ Flow     │  │ Data     │  │ Tests    │  │ Cleanup  │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│   Identify      Create test   Actions +     Teardown                 │
│   user steps    fixtures      assertions    test data                │
│   Find selectors seed DB       error paths   reset state             │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │               TEST STRUCTURE                                 │    │
│  │                                                              │    │
│  │  describe('Feature: Course Enrollment')                      │    │
│  │  │                                                           │    │
│  │  ├── beforeAll: seed database, create test user              │    │
│  │  ├── beforeEach: log in, navigate to starting page           │    │
│  │  │                                                           │    │
│  │  ├── test: 'admin enrolls user in course' (happy path)       │    │
│  │  ├── test: 'shows error for duplicate enrollment' (error)    │    │
│  │  ├── test: 'member cannot enroll others' (auth)              │    │
│  │  ├── test: 'handles network failure gracefully' (resilience) │    │
│  │  │                                                           │    │
│  │  ├── afterEach: clean up created records                     │    │
│  │  └── afterAll: remove test user, reset DB                    │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Map the User Flow

### 1.1 — Identify the Journey

Before writing any code, walk through the feature manually and document every step.

```
┌──────────────────────────────────────────────────────────────┐
│  USER FLOW MAPPING                                           │
│                                                              │
│  For each flow, document:                                    │
│                                                              │
│  1. STARTING STATE                                           │
│     → What page is the user on?                              │
│     → Are they logged in? What role?                         │
│     → What data already exists?                              │
│                                                              │
│  2. ACTIONS (in order)                                       │
│     → What does the user click/type/select?                  │
│     → What API calls fire behind the scenes?                 │
│     → What loading states appear?                            │
│                                                              │
│  3. VERIFICATION POINTS                                      │
│     → What text/element should appear after each action?     │
│     → What data should change in the database?               │
│     → What side effects should fire? (email, redirect)       │
│                                                              │
│  4. END STATE                                                │
│     → What page is the user on now?                          │
│     → What has changed from the starting state?              │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 — Flow Diagram Example

```
┌──────────┐     Click "Enroll"    ┌──────────────┐     Select user     ┌──────────────┐
│  Course  │ ─────────────────────▶│  Enrollment  │ ──────────────────▶ │  Confirm     │
│  Detail  │                       │  Dialog      │                     │  Dialog      │
└──────────┘                       └──────────────┘                     └──────────────┘
                                                                              │
                                                                         Click "Confirm"
                                                                              │
                                                                              ▼
┌──────────┐     Toast "Enrolled"  ┌──────────────┐
│  Course  │ ◀─────────────────────│  API Call     │
│  Detail  │    User in list       │  POST /enroll │
└──────────┘                       └──────────────┘
```

### 1.3 — Find Selectors

```
┌──────────────────────────────────────────────────────────────┐
│  SELECTOR STRATEGY (in order of preference)                  │
│                                                              │
│  1. data-testid="enroll-button"      ← BEST: explicit, stable│
│  2. role="button" + name="Enroll"    ← GOOD: accessible      │
│  3. text="Enroll Users"             ← OK: visible to user    │
│  4. .enroll-button                   ← AVOID: class changes  │
│  5. #enroll-btn                      ← AVOID: fragile ID     │
│  6. div > button:nth-child(3)        ← NEVER: breaks easily  │
│                                                              │
│  RULES                                                       │
│  → Prefer data-testid for critical interactions              │
│  → Use getByRole + getByText for accessibility-first tests   │
│  → Never use CSS class selectors — they change with styling  │
│  → Never use index-based selectors — they break with layout  │
│  → Add data-testid to the component if none exists           │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 2: Set Up Test Data

### 2.1 — Test Data Strategy

```
┌──────────────────────────────────────────────────────────────┐
│  TEST DATA APPROACHES                                        │
│                                                              │
│  APPROACH 1: API SEEDING (recommended)                       │
│  → Call API endpoints in beforeAll to create test data       │
│  → Pros: uses real validation, closest to production         │
│  → Cons: slower, depends on API being correct                │
│                                                              │
│  APPROACH 2: DATABASE SEEDING                                │
│  → Insert records directly via Prisma/SQL in beforeAll       │
│  → Pros: fast, can create exact states needed                │
│  → Cons: bypasses validation, can drift from real behavior   │
│                                                              │
│  APPROACH 3: FIXTURE FILES                                   │
│  → Load JSON fixtures into the database                      │
│  → Pros: repeatable, version controlled                      │
│  → Cons: fixtures get stale, need maintenance                │
│                                                              │
│  BEST PRACTICE: Use API seeding for entities the user        │
│  creates (courses, users). Use DB seeding for complex        │
│  states that are hard to reach through the UI (enrollment    │
│  with specific progress, expired subscriptions).             │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 — Test Isolation

```
┌──────────────────────────────────────────────────────────────┐
│  TEST ISOLATION RULES                                        │
│                                                              │
│  □ Each test must be independent — no shared mutable state   │
│  □ Tests must pass in any order                              │
│  □ Tests must pass when run alone or in parallel             │
│  □ Use unique identifiers (timestamp, UUID) in test data     │
│  □ Clean up created data in afterEach / afterAll             │
│  □ Never depend on data from a previous test                 │
│                                                              │
│  ISOLATION PATTERN                                           │
│  → Create a unique tenant per test suite                     │
│  → Create test users with unique emails (test+ts@domain.com)│
│  → Delete all created data in afterAll                       │
│  → Use transactions that roll back if DB seeding             │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 3: Write the Tests

### 3.1 — Test File Structure (Playwright)

```typescript
// tests/e2e/enrollment.spec.ts

import { test, expect } from '@playwright/test'

// --- Test Data ---
const TEST_USER = {
  email: `test-enroll-${Date.now()}@acme.com`,
  password: 'TestPass123!',
  name: 'Test User',
}

// --- Page Object (inline or imported) ---
class CoursePage {
  constructor(private page: Page) {}

  async navigateTo(courseId: string) {
    await this.page.goto(`/courses/${courseId}`)
  }

  async clickEnrollUsers() {
    await this.page.getByRole('button', { name: 'Enroll Users' }).click()
  }

  async searchUser(email: string) {
    await this.page.getByPlaceholder('Search users...').fill(email)
    await this.page.waitForResponse('**/api/users/search*')
  }

  async selectUser(name: string) {
    await this.page.getByRole('checkbox', { name }).check()
  }

  async confirmEnrollment() {
    await this.page.getByRole('button', { name: 'Enroll' }).click()
  }

  async expectUserEnrolled(name: string) {
    await expect(
      this.page.getByText(`${name} enrolled successfully`)
    ).toBeVisible()
  }
}

// --- Tests ---
test.describe('Course Enrollment', () => {
  let coursePage: CoursePage

  test.beforeEach(async ({ page }) => {
    // Log in as admin
    await page.goto('/login')
    await page.getByLabel('Email').fill('admin@acme.com')
    await page.getByLabel('Password').fill('AdminPass123!')
    await page.getByRole('button', { name: 'Sign In' }).click()
    await page.waitForURL('/dashboard')

    coursePage = new CoursePage(page)
  })

  test('admin enrolls a user in a published course', async () => {
    await coursePage.navigateTo('test-course-id')
    await coursePage.clickEnrollUsers()
    await coursePage.searchUser(TEST_USER.email)
    await coursePage.selectUser(TEST_USER.name)
    await coursePage.confirmEnrollment()
    await coursePage.expectUserEnrolled(TEST_USER.name)
  })

  test('shows error for already enrolled user', async () => {
    // ... error path test
  })

  test('member role cannot access enroll button', async () => {
    // ... authorization test
  })
})
```

### 3.2 — What to Test in Each Flow

```
┌──────────────────────────────────────────────────────────────┐
│  HAPPY PATH TEST                                             │
│                                                              │
│  MUST verify:                                                │
│  □ User can complete the full flow without errors            │
│  □ Success message/toast appears                             │
│  □ Data is persisted (reload page, verify it's still there)  │
│  □ Navigation lands on the correct page                      │
│  □ Side effects fire (check for email, notification badge)   │
│  □ Related UI updates (counts, lists, status badges)         │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  ERROR PATH TESTS                                            │
│                                                              │
│  MUST verify:                                                │
│  □ Error message is user-friendly (not a stack trace)        │
│  □ Form data is preserved after error (user doesn't retype)  │
│  □ User can retry the action after fixing the error          │
│  □ No partial data is saved on failure                       │
│  □ Loading state doesn't get stuck                           │
│  □ Concurrent actions don't cause data corruption            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  AUTHORIZATION TESTS                                         │
│                                                              │
│  MUST verify:                                                │
│  □ Unauthorized user sees access denied (not a crash)        │
│  □ UI elements are hidden for wrong roles (button not shown) │
│  □ Direct URL access is blocked (not just hidden buttons)    │
│  □ API returns 403/401 for unauthorized requests             │
│  □ Cross-tenant access is blocked                            │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 — Assertion Best Practices

```
┌──────────────────────────────────────────────────────────────┐
│  ASSERTION RULES                                             │
│                                                              │
│  ✅ DO: Assert visible text the user would see               │
│     await expect(page.getByText('Enrolled')).toBeVisible()   │
│                                                              │
│  ✅ DO: Assert URL changes after navigation                  │
│     await expect(page).toHaveURL('/dashboard')               │
│                                                              │
│  ✅ DO: Assert element count for lists                       │
│     await expect(page.getByRole('row')).toHaveCount(5)       │
│                                                              │
│  ✅ DO: Assert disabled state for invalid actions            │
│     await expect(submitBtn).toBeDisabled()                   │
│                                                              │
│  ✅ DO: Wait for network before asserting                    │
│     await page.waitForResponse('**/api/enroll')              │
│     await expect(successToast).toBeVisible()                 │
│                                                              │
│  ❌ DON'T: Use arbitrary timeouts                            │
│     await page.waitForTimeout(3000) ← FLAKY                 │
│                                                              │
│  ❌ DON'T: Assert on CSS classes or styles                   │
│     expect(el).toHaveClass('bg-green-500') ← BRITTLE        │
│                                                              │
│  ❌ DON'T: Assert on internal state or variables             │
│     expect(window.__store.user) ← IMPLEMENTATION DETAIL     │
│                                                              │
│  ❌ DON'T: Assert "no error" without checking success        │
│     Test that the RIGHT thing happened, not just that        │
│     nothing blew up                                          │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 4: Handle Flakiness

```
┌──────────────────────────────────────────────────────────────┐
│  FLAKY TEST PREVENTION                                       │
│                                                              │
│  TIMING                                                      │
│  □ Wait for network responses, not fixed timeouts            │
│  □ Wait for elements to be visible before interacting        │
│  □ Use auto-waiting assertions (Playwright's expect)         │
│  □ Add waitForLoadState('networkidle') after navigation      │
│                                                              │
│  DATA                                                        │
│  □ Use unique data per test run (timestamps, UUIDs)          │
│  □ Never depend on data ordering unless explicitly sorted    │
│  □ Reset state in beforeEach, not just beforeAll             │
│  □ Handle race conditions with retry logic                   │
│                                                              │
│  SELECTORS                                                   │
│  □ Use stable selectors (data-testid, role, text)            │
│  □ Avoid selectors that depend on DOM structure              │
│  □ Use getByRole over getByTestId when possible              │
│                                                              │
│  ENVIRONMENT                                                 │
│  □ Tests must work in CI (no desktop dependencies)           │
│  □ Mock external services (email, payment, file upload)      │
│  □ Use consistent timezone in test config                    │
│  □ Set viewport size explicitly (don't depend on default)    │
│                                                              │
│  DEBUGGING FLAKY TESTS                                       │
│  → Run the test 10 times in a loop:                          │
│    npx playwright test enrollment --repeat-each=10           │
│  → Enable trace on failure:                                  │
│    npx playwright test --trace on-first-retry                │
│  → Record video on failure:                                  │
│    use: { video: 'on-first-retry' }                          │
└──────────────────────────────────────────────────────────────┘
```

---

## Page Object Pattern

```
┌──────────────────────────────────────────────────────────────┐
│  PAGE OBJECT DECISION TREE                                   │
│                                                              │
│  Is the page used in more than 2 test files?                 │
│  │                                                           │
│  ├── YES → Extract to page-objects/ directory                │
│  │   File: tests/page-objects/course-page.ts                 │
│  │   Export: class CoursePage { ... }                         │
│  │                                                           │
│  └── NO → Inline the page object in the test file            │
│      Keep it simple, refactor later if reuse grows           │
│                                                              │
│  PAGE OBJECT RULES                                           │
│  → Encapsulate selectors (never use selectors in test body)  │
│  → Methods = user actions (clickEnroll, fillName, submitForm)│
│  → Assertion helpers = what user sees (expectSuccess, ...)   │
│  → No test logic in page objects (no if/else, no assertions  │
│    about test-specific conditions)                           │
│  → Constructor takes Page instance                           │
│  → One page object per page or major dialog                  │
└──────────────────────────────────────────────────────────────┘
```

---

## Anti-Patterns — What NOT to Do

```
┌──────────────────────────────────────────────────────────────┐
│  E2E TEST ANTI-PATTERNS                                      │
│                                                              │
│  ❌ Tests that depend on execution order                     │
│     → Each test must set up its own state                    │
│                                                              │
│  ❌ Using sleep() or waitForTimeout()                        │
│     → Wait for specific events: network, element, URL       │
│                                                              │
│  ❌ Testing backend logic through the UI                     │
│     → Use API tests for validation rules, business logic     │
│     → E2E tests verify the integration, not the logic        │
│                                                              │
│  ❌ Asserting on snapshot of entire page                     │
│     → Too brittle, breaks on any copy change                 │
│                                                              │
│  ❌ Sharing state between tests via global variables         │
│     → Use test fixtures or beforeEach setup                  │
│                                                              │
│  ❌ Not cleaning up test data                                │
│     → Accumulated data causes false failures                 │
│                                                              │
│  ❌ Testing too many things in one test                      │
│     → One test = one flow = one assertion group              │
│     → Long tests are hard to debug when they fail            │
│                                                              │
│  ❌ Ignoring CI environment differences                      │
│     → Test must work headless, on Linux, with no GPU         │
└──────────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Test the user, not the code** — Write tests as if you are describing what a user does, not what the code executes. "User clicks Enroll" not "POST /api/enroll is called."
2. **Keep tests short** — A good E2E test is 10-20 lines of action + assertion. If it's longer, split into multiple tests.
3. **Name tests like scenarios** — `'admin enrolls user in published course'` not `'test enrollment feature'`.
4. **Always verify after reload** — The strongest assertion is: perform action, reload page, verify the change persisted.
5. **Run locally first** — Always run the test locally before pushing. Fix flakiness before it enters CI.
6. **One flow per test file** — Group related tests in one describe block, but don't mix unrelated flows.
7. **Add data-testid proactively** — When building a feature, add data-testid to interactive elements. It makes E2E testing dramatically easier.

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
