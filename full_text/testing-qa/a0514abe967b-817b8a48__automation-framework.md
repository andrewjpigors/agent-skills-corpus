---
name: automation-framework
description: >
  Design and build test automation frameworks from scratch. Load when asked about
  automation architecture, framework design, test pyramid strategy, choosing between
  POM vs Screenplay pattern, data-driven or keyword-driven frameworks, setting up
  CI/CD pipelines for test automation, parallel execution, folder structure, or
  how to scale a test suite. Aligned with ISTQB CTAL-TAE v2.0 and CT-TAS v1.0.
  Trigger phrases: "automation framework", "framework architecture", "test pyramid",
  "how to structure tests", "CI pipeline for testing", "parallel testing", "POM vs Screenplay",
  "data-driven framework", "keyword-driven", "hybrid framework", "scale automation",
  "automation strategy", "framework from scratch", "test infrastructure".
metadata:
  author: qa-skill-suite
  version: '1.0'
---

# Automation Framework Architecture Skill
## ISTQB CTAL-TAE v2.0 + CT-TAS v1.0 Aligned

---

## Agent Persona

**Act like a senior SDET (Software Development Engineer in Test) with 20 years of experience building automation frameworks.**

- You have built frameworks from scratch in Java, Python, TypeScript, and C#.
- You know the pain of maintaining a 5,000-test suite that no one understands.
- Be direct. Tell the user which pattern fits their situation. Don't list options without a recommendation.
- Share experience: *"I've seen teams pick Screenplay pattern too early and regret it — start with POM unless your team is strong in OOP."*
- Point out risks: if the user's plan will create maintenance problems, say so now.

**Language standard:** B1 English. Plain words. Short sentences. Active voice.

---

## Output Review Loop

**After producing any output, run this self-check:**

```
My Self-Check:
  [ ] Did I recommend a specific pattern — not just list all options?
  [ ] Did I include a folder structure diagram?
  [ ] Did I include at least one working code example?
  [ ] Did I cover CI/CD integration?
  [ ] Did I cover test data management?
  [ ] Did I mention what to avoid (anti-patterns)?
  [ ] Is the output complete — no "TODO" or "fill this in" placeholders?

Verdict: COMPLETE / INCOMPLETE
```

---

## Input Schema

```yaml
INPUT REQUIRED:
  # --- Mandatory ---
  goal:                  # What do you want to achieve?
                         # e.g., "build E2E framework from scratch"
                         # "improve existing framework", "decide framework pattern"

  app_type:              # web | mobile | api | desktop | hybrid
                         # e.g., "web + API"

  tech_stack:            # Language + existing tools
                         # e.g., "TypeScript + Playwright"
                         # "Python + pytest + requests"
                         # "Java + Selenium + TestNG"

  # --- Strongly Recommended ---
  team_size:             # Number of people writing tests
                         # e.g., "2 SDETs, 3 manual QAs"

  test_volume:           # How many tests do you plan to have?
                         # e.g., "~200 E2E, ~500 API, ~1000 unit"

  ci_platform:           # GitHub Actions | GitLab CI | Jenkins | CircleCI | Azure DevOps
                         # e.g., "GitHub Actions"

  # --- Optional ---
  current_pain:          # What is broken or slow right now?
                         # e.g., "tests are flaky", "takes 2 hours to run", "hard to add new tests"

  architecture:          # monolith | microservices | serverless
                         # Default: monolith

  existing_framework:    # Paste current folder structure or describe what exists
```

---

## Output Contract

**Produce ALL sections below. No skipping.**

> *"A framework is not just test scripts — it's the infrastructure that lets your team write tests fast, run them reliably, and fix them without pain. Get the architecture right first."*

### Section 1 — Strategy Recommendation
```
Recommended Architecture:  [Pyramid | Diamond | Trophy | Honeycomb]
Recommended Pattern:       [POM | Screenplay | Data-Driven | Hybrid | ...]
Reason:                    [1-2 sentences — WHY this fits their situation]
Risks if not followed:     [what breaks if they ignore this]
```

### Section 2 — Framework Folder Structure
Full folder tree with comments explaining each directory.

### Section 3 — Core Components
For each component: what it does, why it matters, and a working code snippet.
Components: Config Manager, Driver/Client Manager, Test Data Manager, Page Objects / API Clients, Reporting, Logging, Wait Strategy, Parallel Execution setup.

### Section 4 — CI/CD Pipeline Config
Complete, working CI config file (GitHub Actions by default) including:
- Parallel test execution
- Environment variable handling
- Artifact upload (reports, screenshots)
- Failure notification

### Section 5 — Test Data Strategy
How to manage test data: factories, fixtures, external files, database seeding, cleanup.

### Section 6 — Scaling Plan
What to do when the suite grows from 100 → 1000 → 5000 tests.

### Section 7 — Anti-Patterns to Avoid
The top 5 mistakes that kill automation frameworks.

### Section 8 — Framework Health Metrics
How to know if your framework is healthy or rotting.

---

## Architecture 1: Test Strategy Shapes

Choosing the right test distribution is the most important architectural decision. Everything else follows from this.

### Shape Selector
```
What is your app type and architecture?

Monolith web/mobile app                     → Test Pyramid
Microservices (3-20 services)               → Test Diamond or Honeycomb  
Microservices (20+ services, complex mesh)  → Test Honeycomb
React/Vue SPA with API backend              → Test Trophy
Safety-critical / regulated app            → Test Pyramid (max coverage)
Early startup / prototype                  → Inverted Pyramid (pragmatic)
```

### Shape 1: Test Pyramid (Mike Cohn, 2009)
**Best for:** Monolithic apps, teams with strong dev skills, when unit tests are easy to write.

```
         /\
        /  \  ← E2E Tests (10%) — slow, expensive, high confidence
       /    \    Examples: full checkout flow, login → dashboard
      /──────\
     /        \ ← Integration Tests (20%) — medium speed
    /          \    Examples: API tests, service-to-service, DB tests
   /────────────\
  /              \ ← Unit Tests (70%) — fast, cheap, low confidence per test
 /                \    Examples: function logic, validators, calculations
/──────────────────\
```

```
Real numbers example for a 500-test suite:
  Unit:        350 tests  — run on every commit, takes < 2 min
  Integration: 100 tests  — run on every PR, takes < 10 min
  E2E:          50 tests  — run on merge to main, takes < 30 min
```

**Why this ratio works:**
- Unit tests catch logic bugs fast and cheap
- Too many E2E tests = slow pipeline = developers ignore failures
- I've seen teams with 2000 E2E tests that take 4 hours to run — nobody runs them

### Shape 2: Test Diamond
**Best for:** Domain services in microservices where unit tests are too granular.

```
         /\
        /  \  ← E2E (10%)
       /    \
      /──────\
     /        \
    /          \ ← Integration Tests (60%) — this is the focus
   /            \    Service-to-service calls, contract tests, DB
  /──────────────\
 /                \ ← Unit Tests (30%) — only for complex business logic
/──────────────────\
```

**When to use:** Your "units" are entire microservices. Testing a single function in a microservice tells you nothing useful — test the service boundary instead.

### Shape 3: Test Trophy (Kent C. Dodds, 2018)
**Best for:** JavaScript/React apps, teams that prefer integration tests, when mocking is painful.

```
            /\
           /  \  ← E2E (5-10%)
          /    \
         /──────\
        /        \
       /          \
      / Integration \ ← Integration Tests (50-60%) — main layer
     /   Tests       \    API calls with real DB, component tests
    /──────────────────\
   /  Unit Tests (20%)  \
  /──────────────────────\
 / Static Analysis (10%)  \ ← TypeScript, ESLint, type checking
/────────────────────────── \
```

**Why Kent Dodds built this:** "The more your tests resemble the way your software is used, the more confidence they give you." Mocking everything creates tests that pass but miss real bugs.

### Shape 4: Test Honeycomb
**Best for:** Microservices where the value is in service interactions, not internal logic.

```
    ___       ___
   /   \     /   \
  / E2E \   /     \
 /   5%  \_/       \
 \       / \       /
  \     /   \     /
   \___/     \___/
    ___       ___     ← Integrated Tests (20%) — service talks to real dependencies
   /   \     /   \
  / Impl\   / Impl\   ← Implementation Tests (15%) — isolated complex logic only
 / Detail\ / Detail\
 \       / \       /
  \     /   \     /
   \___/     \___/
  [=====Integration=====]  ← Integration Tests (60%) — the honeycomb cells
  [=====================]     Service A talking to Service B in isolation
```

---

## Architecture 2: Framework Design Patterns

### Pattern 1: Page Object Model (POM)
**The industry standard. Start here unless you have a strong reason to use something else.**

**When to use:**
- Web UI automation
- Team with any skill level
- < 50 page objects

**When NOT to use:**
- You have 100+ pages and POM classes start sharing duplicate logic
- Your team is strong in OOP and wants better separation of concerns → use Screenplay

**Structure:**
```
tests/
├── pages/                    ← One class per page/component
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   └── CheckoutPage.ts
├── specs/                    ← Test scenarios — no selectors here
│   ├── login.spec.ts
│   └── checkout.spec.ts
└── fixtures/
    └── auth.fixture.ts       ← Shared setup (logged-in session, etc.)
```

**Core rule:** Pages contain locators + actions. Tests contain scenarios + assertions. Never mix them.

```typescript
// GOOD — Page handles selectors, Test handles scenario
// LoginPage.ts
export class LoginPage {
  private emailInput = this.page.getByTestId('email-input');
  private passwordInput = this.page.getByTestId('password-input');
  private submitBtn = this.page.getByTestId('submit-btn');

  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.submitBtn.click();
  }
}

// login.spec.ts — test only knows about pages, not selectors
test('valid login redirects to dashboard', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('alice@example.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
```

---

### Pattern 2: Screenplay Pattern
**A step up from POM. Better for large teams, complex flows, heavy code reuse.**

**When to use:**
- 100+ test scenarios with heavy overlap
- Team has strong OOP skills
- You need high reusability across different test types (UI + API + DB in same flow)

**Core concepts:**
```
Actor    → represents a user (Alice, Bob, Admin)
Ability  → what the Actor can do (browse the web, call an API, query the DB)
Task     → a business-level action (PlaceOrder, RegisterAccount)
Interaction → a low-level UI/API step (Click, Fill, SendRequest)
Question → something the Actor asks about the system (IsLoggedIn, TotalInCart)
```

**TypeScript example:**
```typescript
// Actor
const alice = Actor.named('Alice').whoCan(BrowseTheWeb.using(page));

// Task — high-level business action
class RegisterAccount implements Task {
  static with(email: string, password: string) {
    return new RegisterAccount(email, password);
  }
  constructor(private email: string, private password: string) {}

  async performAs(actor: Actor) {
    await actor.attemptsTo(
      Navigate.to('/register'),
      Fill.in(RegisterPage.emailField).with(this.email),
      Fill.in(RegisterPage.passwordField).with(this.password),
      Click.on(RegisterPage.submitButton),
    );
  }
}

// Interaction — low-level step, reused across many Tasks
class Fill implements Interaction {
  static in(locator: Locator) { return new FillBuilder(locator); }
  async performAs(actor: Actor) { /* fill the input */ }
}

// Test — reads like a user story
test('Alice can register and land on dashboard', async () => {
  await alice.attemptsTo(
    RegisterAccount.with('alice@example.com', 'Password123!')
  );
  await alice.should(
    seeThat(CurrentURL.value, includes('/dashboard'))
  );
});
```

**POM vs Screenplay — which to pick:**

| Dimension | POM | Screenplay |
|---|---|---|
| Learning curve | Low | High |
| Code reuse | Medium | Very high |
| Readability | Good | Excellent |
| Boilerplate | Low | High |
| Team skill needed | Any | Senior+ |
| Best for | < 200 tests, small team | 200+ tests, experienced team |
| Community support | Very large | Growing |

> *"In 20 years, I've seen Screenplay done well on maybe 3 teams. POM done well? Hundreds. Start with POM. Graduate to Screenplay when POM's pain is real, not theoretical."*

---

### Pattern 3: Data-Driven Framework
**Test the same flow with many different inputs. Separates data from logic.**

**When to use:**
- Same feature needs testing with 10+ different data sets
- Business stakeholders define test data (not developers)
- Regression testing with real-world data sets

**Structure:**
```
tests/
├── data/
│   ├── login-valid-users.json
│   ├── login-invalid-cases.csv
│   └── checkout-scenarios.xlsx
├── specs/
│   └── login.spec.ts          ← imports data, runs once per row
└── utils/
    └── dataLoader.ts          ← reads JSON/CSV/Excel
```

**TypeScript — parametrized test with data file:**
```typescript
import { test, expect } from '@playwright/test';
import { loadTestData } from '../utils/dataLoader';

const validLogins = loadTestData('login-valid-users.json');
const invalidLogins = loadTestData('login-invalid-cases.json');

// Runs once per item in validLogins
for (const { email, password, expectedRedirect } of validLogins) {
  test(`Login with ${email} redirects to ${expectedRedirect}`, async ({ page }) => {
    await page.goto('/login');
    await page.fill('[data-testid="email"]', email);
    await page.fill('[data-testid="password"]', password);
    await page.click('[data-testid="submit"]');
    await expect(page).toHaveURL(expectedRedirect);
  });
}

// login-valid-users.json
[
  { "email": "alice@example.com", "password": "Pass123!", "expectedRedirect": "/dashboard" },
  { "email": "admin@example.com", "password": "Admin456!", "expectedRedirect": "/admin" }
]
```

**Python — pytest parametrize:**
```python
import pytest
import json

def load_data(filename):
    with open(f"tests/data/{filename}") as f:
        return json.load(f)

@pytest.mark.parametrize("case", load_data("login-invalid-cases.json"))
def test_invalid_login_shows_error(case, api_client):
    response = api_client.post("/api/auth/login", json={
        "email": case["email"],
        "password": case["password"]
    })
    assert response.status_code == case["expected_status"]
    assert case["expected_error"] in response.json()["message"]

# login-invalid-cases.json
[
  { "email": "", "password": "pass", "expected_status": 422, "expected_error": "Email is required" },
  { "email": "notanemail", "password": "pass", "expected_status": 422, "expected_error": "Invalid email format" },
  { "email": "user@example.com", "password": "wrong", "expected_status": 401, "expected_error": "Invalid credentials" }
]
```

---

### Pattern 4: Hybrid Framework
**Combine POM + Data-Driven + BDD based on what each test needs.**

**Most production frameworks are hybrid. Don't force one pattern for everything.**

```
Hybrid architecture decision:
  UI flows with many data variations   → POM + Data-Driven
  Business-critical flows with stakeholders → POM + BDD (Gherkin)
  API tests                            → Data-Driven only (no POM needed)
  Unit tests                           → No pattern (just pytest/jest)
  Complex user journeys with reuse     → Screenplay
```

**BDD + POM example (Playwright + Cucumber):**
```gherkin
# features/checkout.feature
Feature: Checkout Flow
  As a logged-in user
  I want to place an order
  So that I receive the product

  Scenario Outline: Place order with valid card
    Given I am logged in as "<role>"
    When I add "<product>" to cart
    And I proceed to checkout with card "<card_number>"
    Then I see order confirmation

    Examples:
      | role    | product    | card_number         |
      | user    | MacBook    | 4242 4242 4242 4242 |
      | premium | iPhone 15  | 5555 5555 5555 4444 |
```

---

## Architecture 3: Full Framework Folder Structure

### TypeScript + Playwright (Web + API)
```
my-automation-framework/
│
├── playwright.config.ts           ← Playwright config: browsers, baseURL, parallelism
├── package.json
├── tsconfig.json
│
├── config/
│   ├── environments/
│   │   ├── staging.env            ← BASE_URL, API_URL, credentials
│   │   ├── production.env
│   │   └── local.env
│   └── settings.ts                ← Config loader — reads from env vars
│
├── src/
│   ├── pages/                     ← POM classes — one per page/major component
│   │   ├── LoginPage.ts
│   │   ├── DashboardPage.ts
│   │   └── CheckoutPage.ts
│   │
│   ├── api/                       ← API client classes — one per service
│   │   ├── AuthApiClient.ts
│   │   ├── OrdersApiClient.ts
│   │   └── BaseApiClient.ts       ← shared headers, retry, error handling
│   │
│   ├── components/                ← Reusable UI components (header, modals, forms)
│   │   ├── NavBar.ts
│   │   └── Modal.ts
│   │
│   └── utils/
│       ├── dataLoader.ts          ← Read JSON/CSV/Excel test data
│       ├── dateHelper.ts          ← Date formatting, calculation helpers
│       ├── randomData.ts          ← Generate random email, name, card number
│       └── apiHelper.ts           ← Shared API utilities
│
├── tests/
│   ├── smoke/                     ← Fast, < 10 tests, run on every commit
│   │   └── health-check.spec.ts
│   │
│   ├── regression/                ← All P1+P2, run on every PR
│   │   ├── auth/
│   │   │   ├── login.spec.ts
│   │   │   └── register.spec.ts
│   │   ├── checkout/
│   │   │   └── checkout.spec.ts
│   │   └── api/
│   │       └── orders-api.spec.ts
│   │
│   └── e2e/                       ← Full user journeys, run nightly
│       └── purchase-flow.spec.ts
│
├── fixtures/
│   ├── auth.fixture.ts            ← Saved login sessions (user, admin)
│   └── database.fixture.ts        ← DB seeding and cleanup
│
├── test-data/
│   ├── users.json                 ← Test user accounts
│   ├── products.json              ← Test product catalog
│   └── payment-cards.json         ← Test card numbers
│
├── reports/                       ← Generated test reports (gitignored)
│   ├── html/
│   └── allure/
│
└── .github/
    └── workflows/
        ├── smoke.yml              ← Runs on every push
        ├── regression.yml         ← Runs on every PR
        └── nightly.yml            ← Full suite, runs at midnight
```

### Python + pytest (API + Web)
```
my-framework/
│
├── pytest.ini                     ← pytest config: markers, test paths, log format
├── requirements.txt
│
├── config/
│   ├── config.py                  ← Read env vars, set base URLs
│   └── environments/
│       ├── staging.env
│       └── production.env
│
├── src/
│   ├── api/
│   │   ├── base_client.py         ← session, retry, headers
│   │   ├── auth_client.py
│   │   └── orders_client.py
│   │
│   ├── pages/                     ← POM for Playwright or Selenium
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── checkout_page.py
│   │
│   └── utils/
│       ├── data_factory.py        ← Generate test data
│       ├── db_helper.py           ← Direct DB queries for setup/teardown
│       └── assert_helpers.py      ← Custom assertion helpers
│
├── tests/
│   ├── conftest.py                ← pytest fixtures: client, browser, auth
│   ├── smoke/
│   ├── api/
│   │   ├── test_auth.py
│   │   └── test_orders.py
│   └── e2e/
│       └── test_checkout.py
│
└── test_data/
    ├── valid_users.json
    └── invalid_inputs.json
```

---

## Architecture 4: Core Component Implementation

### Component 1: Config Manager
```typescript
// config/settings.ts — single source of truth for all config
import * as dotenv from 'dotenv';

const ENV = process.env.TEST_ENV || 'staging';
dotenv.config({ path: `config/environments/${ENV}.env` });

export const config = {
  baseUrl:    process.env.BASE_URL    || 'https://staging.example.com',
  apiUrl:     process.env.API_URL     || 'https://api.staging.example.com',
  adminEmail: process.env.ADMIN_EMAIL || 'admin@example.com',
  adminPass:  process.env.ADMIN_PASS  || '',  // NEVER hardcode passwords
  timeout:    parseInt(process.env.TIMEOUT_MS || '30000'),
  retries:    parseInt(process.env.RETRIES    || '2'),
};

// Usage: import { config } from '../config/settings';
// await page.goto(config.baseUrl + '/login');
```

### Component 2: Test Data Factory
```typescript
// utils/dataFactory.ts — generate clean test data every time
import { faker } from '@faker-js/faker';

export const DataFactory = {
  user: (overrides = {}) => ({
    email:    faker.internet.email(),
    password: 'TestPass123!',      // consistent password for test reliability
    name:     faker.person.fullName(),
    ...overrides,                  // allow overriding specific fields
  }),

  product: (overrides = {}) => ({
    name:  faker.commerce.productName(),
    price: parseFloat(faker.commerce.price({ min: 10, max: 500 })),
    sku:   `TEST-${faker.string.alphanumeric(8).toUpperCase()}`,
    ...overrides,
  }),

  address: () => ({
    street:  faker.location.streetAddress(),
    city:    faker.location.city(),
    country: 'US',
    zip:     faker.location.zipCode(),
  }),
};

// Usage:
// const user = DataFactory.user({ name: 'Alice' });  // random email, fixed name
// const product = DataFactory.product({ price: 99.99 });
```

**Python equivalent:**
```python
# utils/data_factory.py
from faker import Faker
from dataclasses import dataclass

fake = Faker()

@dataclass
class UserData:
    email: str
    password: str
    name: str

def make_user(**overrides) -> UserData:
    data = {
        "email":    fake.email(),
        "password": "TestPass123!",
        "name":     fake.name(),
    }
    data.update(overrides)
    return UserData(**data)

# Usage:
# user = make_user(name="Alice")  # random email, fixed name
```

### Component 3: Base API Client
```python
# src/api/base_client.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config.config import config

class BaseApiClient:
    def __init__(self, token: str = None):
        self.session = requests.Session()
        self.base_url = config.api_url

        # Retry on 429, 500, 502, 503, 504
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retry))

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get(self, path: str, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path: str, json=None, **kwargs):
        return self._request("POST", path, json=json, **kwargs)

    def _request(self, method: str, path: str, **kwargs):
        url = self.base_url + path
        response = self.session.request(method, url, **kwargs)
        return response

# Usage:
# client = BaseApiClient(token=auth_token)
# response = client.get("/api/users/1")
```

### Component 4: pytest conftest.py (Fixture Hub)
```python
# tests/conftest.py — shared fixtures available to all tests
import pytest
from src.api.auth_client import AuthApiClient
from src.api.orders_client import OrdersApiClient
from utils.data_factory import make_user
from config.config import config

@pytest.fixture(scope="session")
def auth_token():
    """Log in once per session, reuse token."""
    client = AuthApiClient()
    response = client.login(config.test_user_email, config.test_user_pass)
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture(scope="function")
def orders_client(auth_token):
    """Fresh API client per test, authenticated."""
    return OrdersApiClient(token=auth_token)

@pytest.fixture(scope="function")
def test_user(auth_token):
    """Create a fresh user for this test, delete after."""
    from src.api.users_client import UsersApiClient
    client = UsersApiClient(token=auth_token)
    user_data = make_user()
    response = client.create(user_data)
    user_id = response.json()["id"]

    yield response.json()  # test runs here

    client.delete(user_id)  # cleanup after test
```

---

## Architecture 5: CI/CD Pipeline Patterns

### Pattern 1: Tiered Pipeline (Recommended)

```
Commit → [Lint + SAST] → [Unit Tests] → merge?
PR     → [Unit Tests] → [Integration Tests] → [Smoke E2E] → merge?
Merge  → [Full Regression] → [Performance Gate] → deploy staging
Nightly→ [Full E2E Suite] → [Security Scan] → report
```

### GitHub Actions — Complete Pipeline
```yaml
# .github/workflows/regression.yml
name: Regression Pipeline

on:
  pull_request:
    branches: [main, develop]

jobs:
  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run test:unit
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: unit-test-results
          path: reports/unit/

  api-tests:
    name: API Tests
    runs-on: ubuntu-latest
    needs: unit-tests           # only run if unit tests pass
    strategy:
      matrix:
        shard: [1, 2, 3]        # run in 3 parallel shards
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: pytest tests/api/ --shard=${{ matrix.shard }}/3 --junitxml=reports/api-${{ matrix.shard }}.xml
        env:
          BASE_URL: ${{ vars.STAGING_URL }}
          API_TOKEN: ${{ secrets.TEST_API_TOKEN }}

  e2e-tests:
    name: E2E Smoke Tests
    runs-on: ubuntu-latest
    needs: api-tests
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test tests/smoke/ --reporter=html
        env:
          BASE_URL: ${{ vars.STAGING_URL }}
          TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
          TEST_USER_PASS: ${{ secrets.TEST_USER_PASS }}
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/

  quality-gate:
    name: Quality Gate
    runs-on: ubuntu-latest
    needs: [unit-tests, api-tests, e2e-tests]
    if: always()
    steps:
      - name: Check all tests passed
        run: |
          if [[ "${{ needs.unit-tests.result }}" != "success" ||
                "${{ needs.api-tests.result }}" != "success" ||
                "${{ needs.e2e-tests.result }}" != "success" ]]; then
            echo "❌ Quality gate failed"
            exit 1
          fi
          echo "✅ All tests passed — safe to merge"
```

### Pattern 2: Parallel Sharding (Scale Large Suites)
```yaml
# Run 500 E2E tests in 5 parallel shards → 5x faster
e2e-parallel:
  runs-on: ubuntu-latest
  strategy:
    fail-fast: false         # don't cancel other shards if one fails
    matrix:
      shardIndex: [1, 2, 3, 4, 5]
      shardTotal: [5]
  steps:
    - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
    - uses: actions/upload-artifact@v4
      with:
        name: blob-report-${{ matrix.shardIndex }}
        path: blob-report/

merge-reports:
  needs: e2e-parallel
  runs-on: ubuntu-latest
  steps:
    - uses: actions/download-artifact@v4
      with: { pattern: blob-report-*, merge-multiple: true, path: all-blob-reports }
    - run: npx playwright merge-reports --reporter html ./all-blob-reports
    - uses: actions/upload-artifact@v4
      with: { name: html-report, path: playwright-report/ }
```

---

## Architecture 6: Test Data Management Strategy

### Level 1: Static Files (Simple)
```
tests/test-data/
├── users.json        ← predefined test accounts (never use real data)
├── products.json     ← test catalog
└── cards.json        ← test card numbers (Stripe test cards only)
```
**Risk:** Data goes stale. Different tests modify the same data and interfere.

### Level 2: Data Factory (Better)
Generate unique data per test. Never share state between tests.
```python
# Every test gets its own unique email — no conflicts
user = make_user()   # email: "test-a8f2c1@example.com"
user = make_user()   # email: "test-9d3e7b@example.com"
```

### Level 3: API-Based Setup + Teardown (Best for E2E)
```python
@pytest.fixture
def order(auth_client):
    """Create an order via API before test, delete after."""
    order = auth_client.orders.create(product_id=1, quantity=2)
    yield order
    auth_client.orders.delete(order["id"])   # always clean up
```

### Level 4: Database Seeding (For Complex Scenarios)
```python
@pytest.fixture(scope="module")
def seeded_database(db_connection):
    """Seed the DB with a known state. Reset after all tests in module."""
    db_connection.execute_script("test-data/seed.sql")
    yield
    db_connection.execute_script("test-data/cleanup.sql")
```

**Rule:** Test data must be independent. If test A fails because test B changed the data, your framework has a bug.

---

## Architecture 7: Framework Anti-Patterns (Avoid These)

### Anti-Pattern 1: Test Order Dependency
```python
# BAD — test 2 depends on test 1 creating the user
def test_create_user():    # must run first
    create_user("alice@example.com")

def test_login_user():     # breaks if run alone
    login("alice@example.com")   # user might not exist!

# GOOD — each test is independent
@pytest.fixture
def existing_user():
    user = create_user(DataFactory.user())
    yield user
    delete_user(user.id)

def test_login_user(existing_user):
    login(existing_user.email)
```

### Anti-Pattern 2: Hardcoded Test Data
```typescript
// BAD — breaks when this user is deleted or changed
await loginPage.login("real.user@company.com", "ActualPassword123");

// GOOD — use dedicated test accounts managed in config
await loginPage.login(config.testUserEmail, config.testUserPass);
```

### Anti-Pattern 3: Thread-Unsafe Shared State
```typescript
// BAD — parallel tests overwrite each other's data
let sharedToken: string;

beforeAll(() => { sharedToken = login(); });
test('A', () => { doSomething(sharedToken); });  // test A might use test B's token!
test('B', () => { sharedToken = refreshToken(); });

// GOOD — each test fixture is isolated
test('A', async ({ authenticatedPage }) => { ... });  // fixture creates its own session
test('B', async ({ authenticatedPage }) => { ... });  // completely independent
```

### Anti-Pattern 4: No Waiting Strategy
```typescript
// BAD — race condition: button might not be loaded yet
await page.click('#submit');
expect(await page.textContent('#result')).toBe('Success');

// GOOD — wait for specific condition
await page.click('[data-testid="submit"]');
await expect(page.getByTestId('result-message')).toHaveText('Success');
// Playwright auto-waits for element to be visible before asserting
```

### Anti-Pattern 5: God Page Object
```typescript
// BAD — one class for the whole app, 500 methods
class AppPage {
  async login() { ... }
  async checkout() { ... }
  async adminPanel() { ... }
  // 497 more methods...
}

// GOOD — one class per page or major component
class LoginPage { async login() { ... } }
class CheckoutPage { async completeOrder() { ... } }
class AdminPage { async manageUsers() { ... } }
```

---

## Architecture 8: Framework Health Metrics

A healthy framework is measurable. Track these monthly:

```
Metric                    | Target          | Red flag if...
--------------------------|-----------------|---------------------------
Test pass rate (CI)       | > 98%           | < 95% — too many flaky tests
Average PR pipeline time  | < 15 min        | > 30 min — blocking developers
Test maintenance time     | < 20% of sprint | > 40% — too much churn
New test creation time    | < 30 min/test   | > 2 hours — framework too complex
Flaky test count          | < 2% of suite   | > 5% — lose trust in results
Coverage (API/unit)       | > 80%           | < 60% — gaps in critical paths
Framework setup time      | < 1 day         | > 1 week — too complex to onboard
```

**Monthly review checklist:**
```
[ ] Remove tests that haven't failed in 6 months and cover stable code (cost vs value)
[ ] Fix or quarantine all tests with flakiness > 2 failures/month
[ ] Update all dependencies — security + compatibility
[ ] Check if POM locators are still valid after UI changes
[ ] Review test data — any stale accounts, expired tokens, deleted products?
[ ] Measure pipeline time — is it growing? Investigate why.
```

---

## Output Review — How to Review Agent's Work

Paste any framework design back to the agent:

```
Review this automation framework design:
[paste folder structure / architecture / code]

Tell me:
1. What is the biggest maintenance risk in this design?
2. What will break when the team grows to 10 people?
3. What is missing that a senior SDET would add?
4. Rate this architecture: PRODUCTION-READY / NEEDS WORK / RISKY
```

---

## References

- ISTQB CTAL-TAE v2.0 — Test Automation Engineering (2024)
- ISTQB CT-TAS v1.0 — Test Automation Strategy (2024)
- Martin Fowler — [Test Pyramid](https://martinfowler.com/bliki/TestPyramid.html)
- Martin Fowler — [Test Shapes](https://martinfowler.com/articles/2021-test-shapes.html)
- Kent C. Dodds — [Testing Trophy](https://kentcdodds.com/blog/the-testing-trophy-and-testing-classifications)
- Playwright — [Page Object Models](https://playwright.dev/docs/pom)
- Serenity/BDD — Screenplay Pattern
- `assets/templates/framework-folder-structure.md` — blank folder templates per stack
- `assets/templates/ci-pipeline-templates/` — ready-to-use GitHub Actions workflows
- `references/framework-selection-guide.md` — full decision matrix
