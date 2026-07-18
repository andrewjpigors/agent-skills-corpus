---
name: mobile-test
description: "Design and implement a complete mobile testing strategy — unit tests, component/widget tests, E2E flows, API mocking, snapshot testing, CI integration, and flaky test management across React Native, Flutter, and iOS. Use when building test infrastructure, writing test suites, or fixing unreliable tests."
---

# Mobile Testing — Confidence Across Every Device

Designs and implements a full mobile testing strategy — from fast unit tests to real-device E2E suites — so bugs die in CI, not in production. Covers React Native, Flutter, and native iOS with platform-specific tooling, test pyramid enforcement, and flaky test elimination.

---

## Your Expertise

You are a **Principal Mobile QA Architect** with 17+ years building test infrastructure for mobile applications — from unit tests to device farms running 500+ devices. You've built testing pipelines that catch 95% of bugs before they reach users, reduced regression cycles from 2 weeks to 2 hours, and designed flake-free E2E suites. You are an expert in:

- React Native testing — Jest + React Native Testing Library, Detox E2E, Maestro, MSW for API mocking
- Flutter testing — widget tests, integration tests (patrol, integration_test), golden tests, mockito
- iOS testing — XCTest, XCUITest, snapshot testing (SnapshotTesting lib), performance tests
- Test architecture — test pyramid for mobile (heavy unit, medium widget/component, light E2E)
- Device testing — real device clouds (BrowserStack, AWS Device Farm), device matrix selection
- Flaky test elimination — deterministic waits, isolated test state, retry strategies, test quarantine
- API mocking — MSW for React Native, mockito + dio adapter for Flutter, URLProtocol for iOS
- CI integration — running mobile tests in GitHub Actions, Codemagic, Xcode Cloud with parallelization
- Coverage analysis — meaningful coverage targets that correlate with defect reduction, not vanity metrics

You build test suites that developers actually trust. When the suite is green, the team ships with confidence. When it is red, the failure points to a real bug — never a timing issue.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Unit Test Framework
<!-- Example: Jest + React Native Testing Library -->
<!-- Example: flutter_test + mockito -->
<!-- Example: XCTest + Quick/Nimble -->

### E2E Test Framework
<!-- Example: Detox / Maestro -->
<!-- Example: patrol / integration_test -->
<!-- Example: XCUITest -->

### API Mocking
<!-- Example: MSW (Mock Service Worker) -->
<!-- Example: mockito + dio adapter -->
<!-- Example: URLProtocol mock -->

### CI Test Runner
<!-- Example: GitHub Actions + EAS Build -->
<!-- Example: Codemagic -->
<!-- Example: Xcode Cloud -->

### Device Matrix
<!-- Example: iPhone SE, iPhone 15, Pixel 6a, Samsung Galaxy S23, iPad -->

### Coverage Targets
<!-- Example: 80% unit, 60% widget/component, critical paths E2E -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│          MANDATORY RULES FOR EVERY MOBILE TEST TASK          │
│                                                              │
│  1. TEST PYRAMID APPLIES TO MOBILE                           │
│     → Many fast unit tests (business logic, utils, state)    │
│     → Some component/widget tests (render, interact, state)  │
│     → Few E2E tests (critical user journeys only)            │
│     → Inverting the pyramid gives you slow, flaky CI that    │
│       nobody trusts — 40-minute suites kill velocity         │
│                                                              │
│  2. MOCK THE BOUNDARY, NOT THE IMPLEMENTATION                │
│     → Mock API responses and native modules, not internal    │
│       functions                                              │
│     → Tests that mock implementation details break on every  │
│       refactor and prove nothing about real behavior         │
│     → Mock at the network layer (MSW, dio adapter,           │
│       URLProtocol), not at the service layer                 │
│                                                              │
│  3. REAL DEVICES FOR E2E                                     │
│     → Simulators miss touch latency, keyboard behavior,      │
│       camera, biometrics, push notifications                 │
│     → Run E2E on real devices or device clouds               │
│     → Simulators are acceptable for unit and component tests │
│     → Never ship a release tested only on simulator          │
│                                                              │
│  4. FLAKY TESTS ARE WORSE THAN NO TESTS                      │
│     → A test that fails randomly teaches the team to ignore  │
│       failures — then real bugs slip through                 │
│     → Fix or quarantine flaky tests immediately              │
│     → Never retry-and-ignore — that masks real failures      │
│     → Track flake rate per test and per test file             │
│                                                              │
│  5. TEST WHAT USERS DO, NOT WHAT CODE DOES                   │
│     → E2E tests mirror user journeys: "log in, create item,  │
│       verify it appears in list"                             │
│     → Not "verify function returns correct object shape"     │
│     → Query by accessibility labels, not by test IDs that    │
│       have no user-facing meaning                            │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in test code, comments, or docs         │
│     → All output reads as if written by a principal engineer  │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Setting up test infrastructure for a new mobile project from scratch
- Writing unit tests for business logic, state management, or utility functions
- Building component/widget tests for UI elements with user interactions
- Creating E2E test suites for critical user journeys
- Fixing flaky tests that erode team confidence in CI
- Configuring CI pipelines to run mobile tests efficiently
- Selecting a device matrix for real-device testing
- Adding API mocking to decouple tests from live backends
- Setting up snapshot/golden testing for visual regression
- Auditing test coverage and identifying gaps in the test pyramid

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                    MOBILE TESTING FLOW                                │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ PHASE 1  │  │ PHASE 2  │  │ PHASE 3  │  │ PHASE 4  │            │
│  │ Strategy │─▶│ Unit &   │─▶│ E2E &    │─▶│ CI &     │            │
│  │ Design   │  │ Component│  │ Device   │  │ Pipeline │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│   Test pyramid   Pure logic    Full flows    Parallel runs           │
│   Coverage plan  UI render     Device cloud  Flake tracking          │
│   Tooling pick   API mocking   Snapshots     Coverage gates          │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                  MOBILE TEST PYRAMID                          │    │
│  │                                                              │    │
│  │                       /\                                      │    │
│  │                      /  \          E2E Tests                  │    │
│  │                     / E2E\         5-10 critical flows        │    │
│  │                    /──────\        Real devices, slow, few    │    │
│  │                   /        \                                  │    │
│  │                  / Componen \       Component / Widget Tests  │    │
│  │                 /  / Widget  \      Render + interact + state │    │
│  │                /──────────────\     Fast, many, high value    │    │
│  │               /                \                              │    │
│  │              /   Unit Tests     \   Unit Tests                │    │
│  │             /  Business Logic    \  Pure functions, utils     │    │
│  │            /  State Management    \ Milliseconds per test     │    │
│  │           /────────────────────────\                          │    │
│  │                                                              │    │
│  │  Speed:    ████████████  Fast  ──────────────  Slow          │    │
│  │  Count:    ████████████  Many  ──────────────  Few           │    │
│  │  Cost:     ████████████  Cheap ──────────────  Expensive     │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Test Strategy Design

### 1.1 — Platform Tooling Comparison

| Concern | React Native | Flutter | iOS Native |
|---------|-------------|---------|------------|
| **Unit framework** | Jest | flutter_test | XCTest |
| **Component test** | React Native Testing Library | flutter_test (widget tests) | XCTest + ViewInspector |
| **E2E framework** | Detox / Maestro | patrol / integration_test | XCUITest |
| **API mocking** | MSW (Mock Service Worker) | mockito + dio adapter | URLProtocol mock |
| **Snapshot testing** | jest-image-snapshot | golden tests (matchesGoldenFile) | SnapshotTesting (pointfree) |
| **State test** | Test store directly (Zustand/Redux) | bloc_test / riverpod test | Test ObservableObject directly |
| **Coverage tool** | jest --coverage (Istanbul) | flutter test --coverage (lcov) | xcodebuild + xcresultparser |
| **CI recommendation** | GitHub Actions + EAS Build | Codemagic / GitHub Actions | Xcode Cloud / GitHub Actions |
| **Device cloud** | BrowserStack, AWS Device Farm | BrowserStack, Firebase Test Lab | BrowserStack, AWS Device Farm |

### 1.2 — Coverage Targets by Layer

```
┌──────────────────────────────────────────────────────────────┐
│  COVERAGE TARGETS — WHAT TO AIM FOR                          │
│                                                              │
│  Layer              Target     What Counts                   │
│  ─────────────────────────────────────────────────────────   │
│  Unit tests         80%+       Business logic, utils,        │
│                                state management, formatters  │
│                                                              │
│  Component/Widget   60%+       Screen components, forms,     │
│                                interactive elements, lists   │
│                                                              │
│  E2E tests          Critical   Login, onboarding, core CRUD, │
│                     paths      payment, data-critical flows  │
│                     only                                     │
│                                                              │
│  WHAT NOT TO MEASURE                                         │
│  ─────────────────────────────────────────────────────────   │
│  → Don't count navigation boilerplate in coverage            │
│  → Don't chase 100% — diminishing returns past 85%           │
│  → Don't count generated code (GraphQL types, Prisma, etc)   │
│  → Coverage without assertions is theater, not testing       │
└──────────────────────────────────────────────────────────────┘
```

### 1.3 — What to Test at Each Level

| Level | Test These | Skip These |
|-------|-----------|------------|
| **Unit** | Pure functions, formatters, validators, state reducers, API transformers, date/currency utils | UI rendering, navigation, native module calls |
| **Component** | Render output, user interactions (tap, swipe, type), loading/error/empty states, conditional rendering, accessibility labels | Network calls (mock them), navigation transitions, animations |
| **E2E** | Login flow, onboarding, core CRUD, payment, data export, push notification tap-through | Every permutation of form validation, admin-only screens, settings toggles |

---

## Phase 2: Unit Testing

### 2.1 — React Native Unit Tests (Jest)

Test pure business logic with zero UI dependencies.

```typescript
// src/utils/formatCurrency.ts
export function formatCurrency(cents: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(cents / 100);
}

// __tests__/utils/formatCurrency.test.ts
import { formatCurrency } from '../src/utils/formatCurrency';

describe('formatCurrency', () => {
  it('formats cents to dollar string', () => {
    expect(formatCurrency(1999)).toBe('$19.99');
  });

  it('handles zero', () => {
    expect(formatCurrency(0)).toBe('$0.00');
  });

  it('handles large amounts', () => {
    expect(formatCurrency(1_000_000)).toBe('$10,000.00');
  });

  it('respects currency parameter', () => {
    expect(formatCurrency(1999, 'EUR')).toContain('19.99');
  });
});
```

### 2.2 — Flutter Unit Tests

```dart
// lib/utils/password_validator.dart
class PasswordValidator {
  static const int minLength = 8;

  static ValidationResult validate(String password) {
    if (password.length < minLength) {
      return ValidationResult(false, 'Must be at least $minLength characters');
    }
    if (!password.contains(RegExp(r'[A-Z]'))) {
      return ValidationResult(false, 'Must contain an uppercase letter');
    }
    if (!password.contains(RegExp(r'[0-9]'))) {
      return ValidationResult(false, 'Must contain a number');
    }
    return ValidationResult(true, null);
  }
}

// test/utils/password_validator_test.dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('PasswordValidator', () {
    test('rejects short passwords', () {
      final result = PasswordValidator.validate('Ab1');
      expect(result.isValid, false);
      expect(result.error, contains('8 characters'));
    });

    test('rejects passwords without uppercase', () {
      final result = PasswordValidator.validate('abcdefg1');
      expect(result.isValid, false);
    });

    test('accepts valid passwords', () {
      final result = PasswordValidator.validate('StrongPass1');
      expect(result.isValid, true);
    });
  });
}
```

### 2.3 — iOS Unit Tests (XCTest)

```swift
// Tests/UtilsTests/DateFormatterTests.swift
import XCTest
@testable import MyApp

final class DateFormatterTests: XCTestCase {

    func testRelativeDate_today() {
        let now = Date()
        XCTAssertEqual(RelativeDateFormatter.format(now), "Today")
    }

    func testRelativeDate_yesterday() {
        let yesterday = Calendar.current.date(byAdding: .day, value: -1, to: Date())!
        XCTAssertEqual(RelativeDateFormatter.format(yesterday), "Yesterday")
    }

    func testRelativeDate_daysAgo() {
        let fiveDaysAgo = Calendar.current.date(byAdding: .day, value: -5, to: Date())!
        XCTAssertEqual(RelativeDateFormatter.format(fiveDaysAgo), "5 days ago")
    }
}
```

### 2.4 — State Management Testing

```
┌──────────────────────────────────────────────────────────────┐
│  STATE TESTING CHECKLIST                                     │
│                                                              │
│  □ Initial state is correct                                  │
│  □ Each action/event produces the expected state change      │
│  □ Derived/computed values update correctly                  │
│  □ Async operations set loading → success/error states       │
│  □ Error state is recoverable (retry clears error)           │
│  □ State resets properly on logout/navigation                │
│  □ Optimistic updates roll back on API failure               │
│  □ Concurrent state changes don't cause race conditions      │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Component / Widget Testing

### 3.1 — React Native Component Tests (RNTL)

```typescript
// __tests__/components/CourseCard.test.tsx
import { render, fireEvent } from '@testing-library/react-native';
import { CourseCard } from '../src/components/CourseCard';

const mockCourse = {
  id: '1',
  title: 'React Native Testing',
  progress: 65,
  thumbnail: 'https://example.com/thumb.jpg',
};

describe('CourseCard', () => {
  it('renders course title', () => {
    const { getByText } = render(
      <CourseCard course={mockCourse} onPress={jest.fn()} />
    );
    expect(getByText('React Native Testing')).toBeTruthy();
  });

  it('displays progress percentage', () => {
    const { getByText } = render(
      <CourseCard course={mockCourse} onPress={jest.fn()} />
    );
    expect(getByText('65%')).toBeTruthy();
  });

  it('calls onPress when tapped', () => {
    const onPress = jest.fn();
    const { getByRole } = render(
      <CourseCard course={mockCourse} onPress={onPress} />
    );
    fireEvent.press(getByRole('button'));
    expect(onPress).toHaveBeenCalledWith('1');
  });

  it('shows completed badge at 100%', () => {
    const completed = { ...mockCourse, progress: 100 };
    const { getByLabelText } = render(
      <CourseCard course={completed} onPress={jest.fn()} />
    );
    expect(getByLabelText('Course completed')).toBeTruthy();
  });
});
```

### 3.2 — Flutter Widget Tests

```dart
// test/widgets/login_form_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('LoginForm', () {
    testWidgets('shows validation error for empty email', (tester) async {
      await tester.pumpWidget(MaterialApp(home: LoginForm()));

      await tester.tap(find.text('Sign In'));
      await tester.pump();

      expect(find.text('Email is required'), findsOneWidget);
    });

    testWidgets('enables button when both fields filled', (tester) async {
      await tester.pumpWidget(MaterialApp(home: LoginForm()));

      await tester.enterText(find.byKey(Key('email')), 'user@test.com');
      await tester.enterText(find.byKey(Key('password')), 'Pass1234');
      await tester.pump();

      final button = tester.widget<ElevatedButton>(find.byType(ElevatedButton));
      expect(button.onPressed, isNotNull);
    });
  });
}
```

### 3.3 — Component Test Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  COMPONENT TEST COVERAGE CHECKLIST                           │
│                                                              │
│  Rendering                                                   │
│  □ Renders with required props / default state               │
│  □ Renders loading state (skeleton, spinner)                 │
│  □ Renders error state (error message, retry button)         │
│  □ Renders empty state (no data message)                     │
│  □ Renders with maximum data (long text, many items)         │
│                                                              │
│  Interaction                                                 │
│  □ Tap / press triggers correct callback                     │
│  □ Text input updates value and calls onChange               │
│  □ Swipe / scroll triggers correct behavior                  │
│  □ Long press shows context menu or tooltip                  │
│  □ Pull to refresh triggers reload                           │
│                                                              │
│  Accessibility                                               │
│  □ Screen reader labels present on interactive elements      │
│  □ Buttons have accessible names                             │
│  □ Images have alt text                                      │
│  □ Focus order is logical                                    │
│                                                              │
│  Edge Cases                                                  │
│  □ Component unmounts cleanly (no memory leaks)              │
│  □ Handles undefined/null props gracefully                   │
│  □ Handles rapid re-renders without crashing                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 4: E2E Testing

### 4.1 — E2E Test Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  E2E TEST STRUCTURE                                          │
│                                                              │
│  ┌──────────┐     ┌──────────────┐     ┌───────────────┐   │
│  │  Test     │────▶│  App under   │────▶│  Mock API     │   │
│  │  Runner   │     │  test        │     │  (or staging) │   │
│  │ (Detox/   │     │  (real build │     │               │   │
│  │  patrol/  │     │   on device) │     │  Deterministic│   │
│  │  XCUI)    │     │              │     │  responses    │   │
│  └──────────┘     └──────────────┘     └───────────────┘   │
│       │                  │                                   │
│       │                  ▼                                   │
│       │           ┌──────────────┐                           │
│       └──────────▶│  Device /    │                           │
│                   │  Simulator   │                           │
│                   │  (real or    │                           │
│                   │   cloud)     │                           │
│                   └──────────────┘                           │
│                                                              │
│  KEY PRINCIPLE: Each test owns its data.                     │
│  → Set up state in beforeEach                                │
│  → Clean up in afterEach                                     │
│  → Never depend on test execution order                      │
│  → Never depend on data from a previous test                 │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 — React Native E2E (Detox)

```typescript
// e2e/flows/login.e2e.ts
describe('Login Flow', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('logs in with valid credentials', async () => {
    await element(by.id('email-input')).typeText('test@example.com');
    await element(by.id('password-input')).typeText('ValidPass1!');
    await element(by.id('login-button')).tap();

    await waitFor(element(by.id('home-screen')))
      .toBeVisible()
      .withTimeout(5000);
  });

  it('shows error for invalid credentials', async () => {
    await element(by.id('email-input')).typeText('wrong@example.com');
    await element(by.id('password-input')).typeText('bad');
    await element(by.id('login-button')).tap();

    await waitFor(element(by.text('Invalid email or password')))
      .toBeVisible()
      .withTimeout(3000);
  });
});
```

### 4.3 — Flutter Integration Tests (patrol)

```dart
// integration_test/login_test.dart
import 'package:patrol/patrol.dart';

void main() {
  patrolTest('user can log in and see dashboard', ($) async {
    await $.pumpWidgetAndSettle(const MyApp());

    await $(#emailField).enterText('test@example.com');
    await $(#passwordField).enterText('ValidPass1!');
    await $('Sign In').tap();

    expect($('Dashboard'), findsOneWidget);
    expect($('Welcome back'), findsOneWidget);
  });
}
```

### 4.4 — iOS E2E (XCUITest)

```swift
// UITests/LoginUITests.swift
final class LoginUITests: XCTestCase {

    let app = XCUIApplication()

    override func setUp() {
        continueAfterFailure = false
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func testSuccessfulLogin() {
        let emailField = app.textFields["Email"]
        emailField.tap()
        emailField.typeText("test@example.com")

        let passwordField = app.secureTextFields["Password"]
        passwordField.tap()
        passwordField.typeText("ValidPass1!")

        app.buttons["Sign In"].tap()

        let dashboard = app.staticTexts["Dashboard"]
        XCTAssertTrue(dashboard.waitForExistence(timeout: 5))
    }
}
```

### 4.5 — Which Flows to Cover with E2E

```
┌──────────────────────────────────────────────────────────────┐
│  E2E FLOW SELECTION — KEEP IT LEAN                           │
│                                                              │
│  ALWAYS cover (P0):                                          │
│  □ Login / logout                                            │
│  □ Onboarding / first-run experience                         │
│  □ Core CRUD for primary entity (create, view, edit, delete) │
│  □ Payment / checkout flow (if applicable)                   │
│  □ Push notification tap → deep link → correct screen        │
│                                                              │
│  COVER if time allows (P1):                                  │
│  □ Search and filter on main list screen                     │
│  □ Offline mode → reconnect → sync                           │
│  □ Pull-to-refresh updates data                              │
│  □ Navigation deep links open correct screens                │
│                                                              │
│  SKIP in E2E (test at lower levels instead):                 │
│  ✗ Every form validation variant (unit test validators)      │
│  ✗ Every permission role variant (integration test API)      │
│  ✗ Settings toggles (component test the settings screen)     │
│  ✗ Rare error states (unit test error handling logic)        │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 5: API Mocking

### 5.1 — React Native (MSW)

```typescript
// test/mocks/handlers.ts
import { http, HttpResponse } from 'msw';

export const handlers = [
  http.post('*/api/auth/login', async ({ request }) => {
    const body = await request.json();
    if (body.email === 'test@example.com') {
      return HttpResponse.json({
        token: 'mock-jwt-token',
        user: { id: '1', name: 'Test User', email: body.email },
      });
    }
    return HttpResponse.json(
      { message: 'Invalid credentials' },
      { status: 401 }
    );
  }),

  http.get('*/api/courses', () => {
    return HttpResponse.json({
      items: [
        { id: '1', title: 'Course A', progress: 45 },
        { id: '2', title: 'Course B', progress: 100 },
      ],
    });
  }),
];

// test/mocks/server.ts
import { setupServer } from 'msw/node';
import { handlers } from './handlers';
export const server = setupServer(...handlers);

// jest.setup.ts
import { server } from './test/mocks/server';
beforeAll(() => server.listen({ onUnhandledRequest: 'error' }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

### 5.2 — Flutter (mockito + dio adapter)

```dart
// test/mocks/api_mock.dart
import 'package:dio/dio.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';

DioAdapter setupMockApi(Dio dio) {
  final adapter = DioAdapter(dio: dio);

  adapter.onPost('/api/auth/login', (server) {
    server.reply(200, {
      'token': 'mock-jwt-token',
      'user': {'id': '1', 'name': 'Test User'},
    });
  }, data: {'email': 'test@example.com', 'password': Matchers.any});

  adapter.onGet('/api/courses', (server) {
    server.reply(200, {
      'items': [
        {'id': '1', 'title': 'Course A', 'progress': 45},
      ],
    });
  });

  return adapter;
}
```

### 5.3 — iOS (URLProtocol)

```swift
// Tests/Mocks/MockURLProtocol.swift
class MockURLProtocol: URLProtocol {
    static var requestHandler: ((URLRequest) throws -> (HTTPURLResponse, Data?))?

    override class func canInit(with request: URLRequest) -> Bool { true }
    override class func canonicalRequest(for request: URLRequest) -> URLRequest { request }

    override func startLoading() {
        guard let handler = MockURLProtocol.requestHandler else {
            fatalError("No request handler set")
        }
        do {
            let (response, data) = try handler(request)
            client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
            if let data { client?.urlProtocol(self, didLoad: data) }
            client?.urlProtocolDidFinishLoading(self)
        } catch {
            client?.urlProtocol(self, didFailWithError: error)
        }
    }

    override func stopLoading() {}
}
```

### 5.4 — Mocking Strategy

```
┌──────────────────────────────────────────────────────────────┐
│  API MOCK DECISION TREE                                      │
│                                                              │
│  Is this a unit test?                                        │
│  ├── YES → Mock at the service/repository layer              │
│  │         (inject mock dependencies)                        │
│  └── NO                                                      │
│      │                                                       │
│      ├── Is this a component/widget test?                     │
│      │   ├── YES → Mock at the network layer                 │
│      │   │         (MSW, dio adapter, URLProtocol)            │
│      │   └── NO                                              │
│      │                                                       │
│      └── Is this an E2E test?                                │
│          ├── Mock API → Faster, deterministic, isolated       │
│          │               Use for CI runs                     │
│          └── Real API → Catches integration bugs              │
│                          Use for pre-release smoke tests     │
│                                                              │
│  RULE: Never mock what you don't own unless you also have    │
│  contract tests validating the mock matches production.      │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Snapshot / Golden Testing

### 6.1 — When to Use Snapshots

| Use Case | Snapshot Type | Platform |
|----------|-------------|----------|
| Catch unintended UI changes | Image snapshot | All |
| Lock down complex layout | Golden file | Flutter |
| Prevent text/label regressions | Inline snapshot | React Native (Jest) |
| Verify design system compliance | Image diff | All |

### 6.2 — Snapshot Test Rules

```
┌──────────────────────────────────────────────────────────────┐
│  SNAPSHOT TESTING RULES                                      │
│                                                              │
│  DO:                                                         │
│  □ Snapshot stable, well-defined components (buttons, cards) │
│  □ Use deterministic data (fixed dates, known IDs)           │
│  □ Review snapshot diffs in PRs — don't blindly update       │
│  □ Snapshot both light and dark mode variants                │
│  □ Keep snapshot count manageable (<50 per test suite)        │
│                                                              │
│  DON'T:                                                      │
│  □ Snapshot entire screens (too brittle)                     │
│  □ Snapshot animated components (non-deterministic)          │
│  □ Snapshot components with timestamps or random IDs         │
│  □ Use snapshots as a substitute for behavioral tests        │
│  □ Auto-update snapshots without reviewing the diff          │
└──────────────────────────────────────────────────────────────┘
```

### 6.3 — Flutter Golden Tests

```dart
// test/golden/course_card_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';

void main() {
  testGoldens('CourseCard renders correctly', (tester) async {
    final builder = GoldenBuilder.column()
      ..addScenario('In progress', CourseCard(progress: 45, title: 'Test'))
      ..addScenario('Completed', CourseCard(progress: 100, title: 'Test'))
      ..addScenario('Not started', CourseCard(progress: 0, title: 'Test'));

    await tester.pumpWidgetBuilder(builder.build());
    await screenMatchesGolden(tester, 'course_card_states');
  });
}
```

---

## Phase 7: CI Integration

### 7.1 — CI Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  CI PIPELINE — PARALLEL EXECUTION                            │
│                                                              │
│  PR opened / push to branch                                  │
│       │                                                      │
│       ├──▶ Job 1: Lint + Type Check          (~1 min)        │
│       │                                                      │
│       ├──▶ Job 2: Unit Tests                 (~2 min)        │
│       │    └── jest --ci --coverage                           │
│       │    └── flutter test --coverage                        │
│       │    └── xcodebuild test (unit scheme)                  │
│       │                                                      │
│       ├──▶ Job 3: Component/Widget Tests     (~3 min)        │
│       │    └── jest --ci --testPathPattern=components         │
│       │    └── flutter test test/widgets/                     │
│       │                                                      │
│       ├──▶ Job 4: Build (verify compilable)  (~5 min)        │
│       │    └── eas build --profile preview --non-interactive  │
│       │    └── flutter build apk --debug                      │
│       │    └── xcodebuild build                               │
│       │                                                      │
│       └──▶ Job 5: E2E Tests (on merge only)  (~10 min)       │
│            └── Detox / patrol / XCUITest                      │
│            └── Runs on device cloud (BrowserStack)            │
│            └── Only critical flows (5-10 tests)               │
│                                                              │
│  TOTAL PR WALL TIME: ~5 min (parallel)                       │
│  TOTAL MERGE TIME:   ~12 min (with E2E)                      │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 — Coverage Enforcement

```yaml
# Example GitHub Actions coverage check
- name: Check coverage threshold
  run: |
    COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
    if (( $(echo "$COVERAGE < 80" | bc -l) )); then
      echo "Coverage $COVERAGE% is below 80% threshold"
      exit 1
    fi
```

### 7.3 — Test Artifacts to Collect

| Artifact | Why | Format |
|----------|-----|--------|
| Coverage report | Track trends, enforce thresholds | HTML + lcov |
| Test results | Debug failures in CI | JUnit XML |
| Screenshots on failure | Visual context for E2E failures | PNG per test |
| Video on failure | Replay what happened before crash | MP4 (Detox/XCUI) |
| Performance traces | Catch regressions in startup time | JSON / trace files |

---

## Phase 8: Flaky Test Management

### 8.1 — Flaky Test Decision Tree

```
┌──────────────────────────────────────────────────────────────┐
│  FLAKY TEST DIAGNOSIS FLOW                                   │
│                                                              │
│  Test fails intermittently                                   │
│       │                                                      │
│       ├── Does it depend on timing / animations?             │
│       │   ├── YES → Replace sleep() with waitFor()           │
│       │   │         Use deterministic animation control       │
│       │   │         Disable animations in test config         │
│       │   └── NO ──▼                                         │
│       │                                                      │
│       ├── Does it depend on network / API response?          │
│       │   ├── YES → Mock the API (MSW, mockito, URLProtocol) │
│       │   │         Never hit real APIs in CI                 │
│       │   └── NO ──▼                                         │
│       │                                                      │
│       ├── Does it depend on data from another test?          │
│       │   ├── YES → Isolate test data in beforeEach          │
│       │   │         Each test creates its own state           │
│       │   │         Never rely on test execution order        │
│       │   └── NO ──▼                                         │
│       │                                                      │
│       ├── Does it depend on device state?                    │
│       │   │  (locale, timezone, permissions, disk space)      │
│       │   ├── YES → Pin device config in test setup           │
│       │   │         Reset permissions before each test        │
│       │   └── NO ──▼                                         │
│       │                                                      │
│       ├── Does it involve async state updates?               │
│       │   ├── YES → Use act() wrappers, flush microtasks     │
│       │   │         Await all pending promises                │
│       │   └── NO ──▼                                         │
│       │                                                      │
│       └── Is the root cause unclear?                         │
│           → QUARANTINE the test immediately                  │
│           → Move to __tests__/quarantine/                    │
│           → File a bug ticket with failure logs              │
│           → Fix within 1 sprint or delete                    │
└──────────────────────────────────────────────────────────────┘
```

### 8.2 — Flake Prevention Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  FLAKE PREVENTION — APPLY TO EVERY TEST                      │
│                                                              │
│  □ No sleep() or hardcoded delays — use waitFor with timeout │
│  □ No shared mutable state between tests                     │
│  □ No dependency on test execution order                     │
│  □ No real network calls — mock at the boundary              │
│  □ No real Date.now() — inject a clock or freeze time        │
│  □ No animation timing — disable animations in test mode     │
│  □ No random data — use deterministic factories              │
│  □ No file system side effects — use in-memory or temp dirs  │
│  □ Assertions wait for condition, not for time               │
│  □ Teardown runs even if test fails (afterEach, addTeardown) │
└──────────────────────────────────────────────────────────────┘
```

### 8.3 — Quarantine Process

| Step | Action | Timeline |
|------|--------|----------|
| 1 | Test fails intermittently in CI | Day 0 |
| 2 | Move to `quarantine/` directory, exclude from CI | Day 0 |
| 3 | File ticket with failure logs and screenshots | Day 0 |
| 4 | Investigate root cause (timing, state, data) | Days 1-3 |
| 5 | Fix and verify with 10x repeated runs | Days 3-5 |
| 6 | Move back to main suite, monitor for 1 week | Day 5 |
| 7 | If still flaky after 1 sprint, delete and rewrite | Day 10 |

---

## Phase 9: Device Matrix Selection

### 9.1 — Recommended Device Matrix

```
┌──────────────────────────────────────────────────────────────┐
│  DEVICE MATRIX — MINIMUM VIABLE COVERAGE                     │
│                                                              │
│  iOS (3 devices minimum):                                    │
│  ┌──────────────┬──────────┬──────────────────────────┐      │
│  │ Device       │ OS       │ Why                      │      │
│  ├──────────────┼──────────┼──────────────────────────┤      │
│  │ iPhone SE 3  │ iOS 16   │ Smallest screen, oldest  │      │
│  │              │          │ supported OS             │      │
│  │ iPhone 15    │ iOS 17   │ Most common device class │      │
│  │ iPhone 16 PM │ iOS 18   │ Largest screen, latest   │      │
│  │              │          │ OS, Dynamic Island       │      │
│  └──────────────┴──────────┴──────────────────────────┘      │
│                                                              │
│  Android (3 devices minimum):                                │
│  ┌──────────────┬──────────┬──────────────────────────┐      │
│  │ Device       │ OS       │ Why                      │      │
│  ├──────────────┼──────────┼──────────────────────────┤      │
│  │ Pixel 6a     │ Android  │ Stock Android, mid-range │      │
│  │              │ 13       │ performance baseline     │      │
│  │ Samsung S23  │ Android  │ Most popular OEM, custom │      │
│  │              │ 14       │ Samsung UI layer         │      │
│  │ Samsung A14  │ Android  │ Low-end device, tests    │      │
│  │              │ 13       │ performance under stress │      │
│  └──────────────┴──────────┴──────────────────────────┘      │
│                                                              │
│  Optional (add if user base requires):                       │
│  □ iPad (10th gen) — tablet layout                           │
│  □ Pixel Tablet — Android tablet                             │
│  □ Foldables (Samsung Fold) — if supporting fold/unfold      │
└──────────────────────────────────────────────────────────────┘
```

### 9.2 — Device Selection Criteria

```
Is the app targeting a specific market?
│
├── Global consumer app
│   → Cover: smallest, most popular, largest per platform
│   → Cover: 2 latest OS versions + oldest supported OS
│   → Cover: at least 1 non-Google Android OEM (Samsung, Xiaomi)
│
├── Enterprise / B2B
│   → Cover: whatever IT departments issue (often iPhone + Samsung)
│   → Cover: latest OS only (enterprises update faster)
│   → Add: tablet if used in meetings or field work
│
└── Regional app
    → Check regional device popularity data (StatCounter, AppAnnie)
    → Prioritize devices popular in your target market
    → Low-end devices matter more in emerging markets
```

---

## Anti-Patterns — What NOT to Do

```
┌──────────────────────────────────────────────────────────────┐
│  MOBILE TESTING ANTI-PATTERNS                                │
│                                                              │
│  ✗ Testing only on simulator, shipping without real device   │
│    → Simulators miss touch latency, memory pressure, camera  │
│                                                              │
│  ✗ E2E tests for every edge case                             │
│    → E2E is slow and expensive — use unit tests for edges    │
│                                                              │
│  ✗ Mocking internal functions instead of boundaries          │
│    → Tests break on every refactor, prove nothing about      │
│      actual API integration                                  │
│                                                              │
│  ✗ sleep(3000) instead of waitFor(condition)                 │
│    → Flaky on slow devices, wastes time on fast devices      │
│                                                              │
│  ✗ Sharing test state between test cases                     │
│    → Test A creates data, test B reads it — breaks if A      │
│      runs after B, or A fails, or tests run in parallel      │
│                                                              │
│  ✗ Ignoring flaky tests ("it passes if you retry")           │
│    → Team learns to ignore red CI, then real bugs ship       │
│                                                              │
│  ✗ No test IDs / accessibility labels on UI elements         │
│    → E2E tests query by text or position — brittle and       │
│      breaks on every copy change or layout shift             │
│                                                              │
│  ✗ Running full E2E suite on every PR                        │
│    → 30-minute CI blocks developer flow — run E2E on merge   │
│                                                              │
│  ✗ Chasing 100% coverage                                     │
│    → Coverage without assertions is theater — a test that    │
│      exercises code but asserts nothing catches nothing       │
└──────────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Start with the test pyramid** — Before writing any test, classify it: unit, component, or E2E. If your E2E count exceeds your component count, you are building a slow, fragile suite.
2. **Mock at the network boundary** — MSW for React Native, dio adapter for Flutter, URLProtocol for iOS. Tests stay fast and deterministic without coupling to backend availability.
3. **Use test IDs for E2E, accessibility labels for everything** — `testID="login-button"` for Detox/patrol, `accessibilityLabel` for the accessibility tree. Never query by internal component names.
4. **Run flaky test detection before merging new tests** — Run the new test 10 times locally. If it fails even once, fix the timing issue before it enters the suite.
5. **Collect screenshots on failure** — Every E2E framework supports failure screenshots. Configure them in CI. A screenshot of the failure state saves hours of debugging.
6. **Keep E2E tests under 10 minutes total** — If your E2E suite exceeds 10 minutes, split it into a fast smoke suite (merge gate) and a full suite (nightly). Developers will not wait 30 minutes for CI.
7. **Test on the smallest screen first** — If your layout works on iPhone SE, it works everywhere. Test the constrained case first, then verify on larger screens.
8. **Review snapshot diffs like code diffs** — Never run `--update-snapshots` blindly. Every snapshot change should be intentional and reviewed in the PR.

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
