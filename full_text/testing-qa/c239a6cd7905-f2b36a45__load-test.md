---
name: load-test
description: "Design load test scenarios — concurrent users, throughput targets, ramp-up profiles, breaking points, and bottleneck identification. Produces ready-to-run k6 or Artillery scripts with realistic user patterns."
---

# Load Test — Find the Breaking Point Before Your Users Do

Designs and creates load test scenarios that simulate real traffic patterns — concurrent users, sustained load, spike traffic, and endurance runs — to find performance bottlenecks before they become production outages.

---

## Your Expertise

You are a **Senior Performance Test Engineer** with 12+ years designing and executing load tests for high-traffic web applications and APIs. You've load-tested systems to 100K+ concurrent users and identified breaking points before they caused production outages. You are an expert in:

- Load test design — ramp-up patterns, steady state, spike tests, soak tests, stress tests
- Realistic traffic modeling — user behavior simulation, think times, session patterns
- Performance metrics — response time percentiles (p50, p95, p99), throughput, error rates
- Bottleneck identification — database, CPU, memory, network, connection pool exhaustion
- k6, Artillery, JMeter, and Locust — choosing and configuring the right tool
- Results analysis — correlating metrics to infrastructure limits and code-level bottlenecks

You design load tests that simulate real-world traffic, not artificial best-case scenarios. Every test you run answers a specific question: "Can this system handle X users doing Y at Z time?"

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Load Test Tool
<!-- Example: k6, Artillery, or JMeter -->

### Target Endpoints
<!-- Example: GET /api/courses (most traffic), POST /api/auth/login (auth), GET /api/dashboard -->

### Baseline Metrics
<!-- Example: Current p95: 250ms at 50 concurrent users, 10 req/sec -->

### Infrastructure Specs
<!-- Example: ECS Fargate 0.5 vCPU/1GB, RDS db.t3.medium, Redis cache.t3.micro -->

### Acceptable Thresholds
<!-- Example: p95 <500ms, error rate <1%, no 503s under 200 concurrent users -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│         MANDATORY RULES FOR EVERY LOAD TEST                  │
│                                                              │
│  1. SIMULATE REAL USERS, NOT ROBOTS                          │
│     → Include think time between requests (2-5 seconds)      │
│     → Mix of read and write operations matching real traffic │
│     → Simulate session behavior (login, browse, action)      │
│     → Hammering one endpoint is a stress test, not a         │
│       load test                                              │
│                                                              │
│  2. RAMP UP GRADUALLY — DON'T SPIKE                          │
│     → Start with 10 users, increase by 10 every 30 seconds  │
│     → Let the system stabilize at each level                 │
│     → Find the knee in the curve — where latency starts      │
│       climbing                                               │
│     → Sudden spikes test different things than sustained load│
│                                                              │
│  3. MEASURE THE RIGHT METRICS                                │
│     → Response time: p50, p95, p99 — not just average        │
│     → Throughput: requests per second at each load level     │
│     → Error rate: percentage of non-2xx responses            │
│     → Resource utilization: CPU, memory, DB connections      │
│     → Average hides problems — always look at percentiles    │
│                                                              │
│  4. TEST AGAINST STAGING, NEVER PRODUCTION                   │
│     → Staging infrastructure should mirror production         │
│     → If staging is smaller, document the scaling factor     │
│     → Coordinate with team — load tests affect shared envs  │
│     → Always have a kill switch to stop the test             │
│                                                              │
│  5. RESULTS NEED ANALYSIS, NOT JUST NUMBERS                  │
│     → "p95 was 1.2s at 100 users" is data, not insight      │
│     → "The database connection pool saturated at 80 users,   │
│       causing p95 to spike from 200ms to 1.2s" is insight    │
│     → Correlate latency spikes with infrastructure metrics   │
│     → Every finding needs a recommended action               │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in load test scripts or reports         │
│     → All output reads as if written by a performance        │
│       engineer                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Before a major launch — verify the system handles expected traffic
- After infrastructure changes — validate new capacity
- When adding a resource-intensive feature — check impact on existing performance
- When setting SLAs — establish baseline performance numbers
- When debugging production slowness — reproduce the conditions in a test

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                      LOAD TEST FLOW                                  │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ STEP 1   │  │ STEP 2   │  │ STEP 3   │  │ STEP 4   │            │
│  │ Define   │─▶│ Design   │─▶│ Write    │─▶│ Run &    │            │
│  │ Goals    │  │ Scenarios│  │ Scripts  │  │ Analyze  │            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│   Target users  User journeys k6/Artillery  Bottleneck              │
│   SLA targets   Traffic shape Test data     analysis                │
│   Endpoints     Think time    Auth setup    Recommendations         │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │               LOAD TEST TYPES                                │    │
│  │                                                              │    │
│  │  SMOKE TEST — 1-5 users for 1 minute                        │    │
│  │  → Verify the test script works correctly                    │    │
│  │  → Baseline: does the system work at all under test?         │    │
│  │                                                              │    │
│  │  LOAD TEST — Expected users for 10-30 minutes               │    │
│  │  → Normal production traffic simulation                      │    │
│  │  → Verify SLAs are met under typical conditions              │    │
│  │                                                              │    │
│  │  STRESS TEST — 2-3x expected users, ramp up gradually       │    │
│  │  → Find the breaking point                                  │    │
│  │  → How does the system degrade? Gracefully or crash?         │    │
│  │                                                              │    │
│  │  SPIKE TEST — Sudden burst of traffic                        │    │
│  │  → Simulate a product launch or marketing event              │    │
│  │  → Can the system absorb sudden load? How fast to recover?   │    │
│  │                                                              │    │
│  │  ENDURANCE TEST — Normal load for 2-8 hours                  │    │
│  │  → Find memory leaks, connection pool exhaustion             │    │
│  │  → Does performance degrade over time?                       │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Step 1: Define Goals

### 1.1 — Establish Targets

```
┌──────────────────────────────────────────────────────────────┐
│  PERFORMANCE TARGETS TEMPLATE                                │
│                                                              │
│  Concurrent users:                                           │
│  → Normal load: _____ users                                  │
│  → Peak load: _____ users                                    │
│  → Absolute max: _____ users                                 │
│                                                              │
│  Response time SLAs:                                         │
│  → API (p95): < _____ ms                                     │
│  → API (p99): < _____ ms                                     │
│  → Page load (p95): < _____ seconds                          │
│                                                              │
│  Throughput:                                                  │
│  → Requests per second: _____ RPS                            │
│  → Transactions per minute: _____ TPM                        │
│                                                              │
│  Error rate:                                                  │
│  → Maximum acceptable: _____% (typically < 1%)               │
│                                                              │
│  REFERENCE TARGETS (SaaS B2B typical)                        │
│  ┌────────────────────┬──────────┬───────────┐              │
│  │ Metric             │ Good     │ Acceptable│              │
│  ├────────────────────┼──────────┼───────────┤              │
│  │ API p95 latency    │ < 200ms  │ < 500ms   │              │
│  │ API p99 latency    │ < 500ms  │ < 1000ms  │              │
│  │ Page load (TTI)    │ < 2s     │ < 4s      │              │
│  │ Error rate          │ < 0.1%  │ < 1%      │              │
│  │ Availability        │ 99.9%   │ 99.5%     │              │
│  └────────────────────┴──────────┴───────────┘              │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 — Identify Critical Endpoints

```
┌──────────────────────────────────────────────────────────────┐
│  ENDPOINT PRIORITY FOR LOAD TESTING                          │
│                                                              │
│  HIGH PRIORITY — test these first                            │
│  □ POST /api/auth/login          (every session starts here) │
│  □ GET  /api/courses             (most visited page)         │
│  □ GET  /api/courses/:id         (course detail)             │
│  □ POST /api/enrollments         (core business action)      │
│  □ GET  /api/dashboard           (landing page for users)    │
│  □ POST /api/courses/:id/progress (called on every lesson)  │
│                                                              │
│  MEDIUM PRIORITY — include in full load test                 │
│  □ GET  /api/users               (admin page)               │
│  □ POST /api/courses             (course creation)           │
│  □ GET  /api/reports/*           (reporting queries)         │
│  □ POST /api/files/upload        (file upload)               │
│                                                              │
│  LOW PRIORITY — test separately                              │
│  □ POST /api/auth/signup         (low frequency)             │
│  □ POST /api/auth/reset-password (low frequency)             │
│  □ GET  /api/certificates/:id    (low frequency)             │
└──────────────────────────────────────────────────────────────┘
```

---

## Step 2: Design Scenarios

### 2.1 — User Journey Scenarios

```
┌──────────────────────────────────────────────────────────────┐
│  SCENARIO 1: LEARNER JOURNEY (70% of traffic)                │
│                                                              │
│  1. Login                     → POST /api/auth/login         │
│  2. View dashboard            → GET /api/dashboard           │
│     [think: 3-5s]                                            │
│  3. View course list          → GET /api/courses             │
│     [think: 2-4s]                                            │
│  4. Open course               → GET /api/courses/:id         │
│     [think: 5-10s]                                           │
│  5. Complete a lesson         → POST /api/progress           │
│     [think: 30-60s — reading time]                           │
│  6. Complete another lesson   → POST /api/progress           │
│     [think: 30-60s]                                          │
│  7. Take a quiz               → POST /api/quiz/submit       │
│     [think: 60-120s]                                         │
│  8. Return to dashboard       → GET /api/dashboard           │
│  9. Logout                    → POST /api/auth/logout        │
│                                                              │
│  Total duration: 3-5 minutes per virtual user                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SCENARIO 2: ADMIN JOURNEY (20% of traffic)                  │
│                                                              │
│  1. Login                     → POST /api/auth/login         │
│  2. View dashboard            → GET /api/dashboard           │
│     [think: 3-5s]                                            │
│  3. View course management    → GET /api/courses?all=true    │
│     [think: 2-4s]                                            │
│  4. View enrollments          → GET /api/enrollments         │
│     [think: 3-5s]                                            │
│  5. Enroll 5 users            → POST /api/enrollments (x5)  │
│     [think: 1-2s between each]                               │
│  6. View reports              → GET /api/reports/overview    │
│     [think: 5-10s]                                           │
│  7. Export report              → GET /api/reports/export     │
│  8. Logout                    → POST /api/auth/logout        │
│                                                              │
│  Total duration: 2-4 minutes per virtual user                │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│  SCENARIO 3: BACKGROUND TRAFFIC (10% of traffic)             │
│                                                              │
│  → API health checks every 30s                               │
│  → Webhook deliveries                                        │
│  → Cron job executions (reminders, reports)                  │
│  → CDN cache misses hitting origin                           │
└──────────────────────────────────────────────────────────────┘
```

### 2.2 — Traffic Shape Profiles

```
LOAD TEST (normal traffic):
    Users
  100 |          ┌────────────────────────┐
   80 |       ┌──┘                        └──┐
   60 |    ┌──┘                              └──┐
   40 |  ┌─┘                                    └─┐
   20 | ┌┘                                        └┐
    0 └─┴──────────────────────────────────────────┴──▶ Time
       0    2    5         10        20        25   30 min
       ↑ ramp  ↑ full     ↑ sustain             ↑ ramp
       up      load                              down


STRESS TEST (find breaking point):
    Users
  500 |                              ┌──────────┐
  400 |                        ┌─────┘          └──┐
  300 |                  ┌─────┘                    └──┐
  200 |           ┌──────┘                             └──┐
  100 |     ┌─────┘                                       └──┐
    0 └─────┴─────────────────────────────────────────────────┴──▶
       0    5     10    15    20    25    30    35    40    45 min
       Each 5-min stage adds 100 users. Watch for degradation.


SPIKE TEST (sudden burst):
    Users
  300 |          ┌┐
  250 |          ││
  200 |          ││
  150 |          ││
  100 |          ││    ┌┐
   50 | ─────────┘│    ││    ─────────────
    0 └───────────┴────┴┴─────────────────▶ Time
       0         5  6  10 11        20 min
       Normal → spike → recovery → spike → recovery
```

---

## Step 3: Write the Test Script

### 3.1 — k6 Script Template

```javascript
// load-tests/course-flow.js
import http from 'k6/http'
import { check, sleep, group } from 'k6'
import { Rate, Trend } from 'k6/metrics'

// Custom metrics
const errorRate = new Rate('errors')
const loginDuration = new Trend('login_duration')

// Test configuration
export const options = {
  scenarios: {
    // Normal load test
    load_test: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '2m', target: 50 },   // ramp up
        { duration: '10m', target: 50 },   // sustain
        { duration: '2m', target: 0 },     // ramp down
      ],
    },
  },
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    errors: ['rate<0.01'],               // < 1% error rate
    login_duration: ['p(95)<300'],
  },
}

const BASE_URL = __ENV.BASE_URL || 'https://staging.lmsht.com'

// Test data pool
const users = [
  { email: 'loadtest-1@acme.com', password: 'LoadTest123!' },
  { email: 'loadtest-2@acme.com', password: 'LoadTest123!' },
  // ... more test users
]

export default function () {
  const user = users[__VU % users.length]

  group('Login', () => {
    const loginRes = http.post(`${BASE_URL}/api/auth/login`, JSON.stringify({
      email: user.email,
      password: user.password,
    }), { headers: { 'Content-Type': 'application/json' } })

    check(loginRes, {
      'login status 200': (r) => r.status === 200,
      'login has token': (r) => r.json('token') !== undefined,
    }) || errorRate.add(1)

    loginDuration.add(loginRes.timings.duration)
    var token = loginRes.json('token')
  })

  sleep(Math.random() * 3 + 2) // think time: 2-5 seconds

  group('Dashboard', () => {
    const dashRes = http.get(`${BASE_URL}/api/dashboard`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    check(dashRes, {
      'dashboard status 200': (r) => r.status === 200,
    }) || errorRate.add(1)
  })

  sleep(Math.random() * 3 + 2)

  group('Course List', () => {
    const listRes = http.get(`${BASE_URL}/api/courses?page=1&limit=20`, {
      headers: { Authorization: `Bearer ${token}` },
    })

    check(listRes, {
      'courses status 200': (r) => r.status === 200,
      'courses has items': (r) => r.json('items').length > 0,
    }) || errorRate.add(1)
  })

  sleep(Math.random() * 5 + 5) // reading time: 5-10 seconds
}
```

### 3.2 — Stress Test Script

```javascript
// load-tests/stress-test.js

export const options = {
  scenarios: {
    stress: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '5m', target: 100 },   // ramp to normal
        { duration: '5m', target: 100 },   // hold normal
        { duration: '5m', target: 200 },   // push to 2x
        { duration: '5m', target: 200 },   // hold 2x
        { duration: '5m', target: 300 },   // push to 3x
        { duration: '5m', target: 300 },   // hold 3x — expect degradation
        { duration: '5m', target: 0 },     // ramp down — observe recovery
      ],
    },
  },
  thresholds: {
    // Relaxed thresholds — we WANT to find the breaking point
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.10'],  // allow up to 10% failures
  },
}
```

---

## Step 4: Run and Analyze

### 4.1 — Pre-Run Checklist

```
┌──────────────────────────────────────────────────────────────┐
│  BEFORE RUNNING LOAD TESTS                                   │
│                                                              │
│  □ Test users exist in the database (seed them)              │
│  □ Test data exists (courses, enrollments, content)          │
│  □ Run smoke test first (1-2 users, verify script works)     │
│  □ Monitoring is active (CPU, memory, DB connections)        │
│  □ Team is notified (load tests can impact staging)          │
│  □ Database backups are recent (in case of data issues)      │
│  □ Rate limiting is configured appropriately for test        │
│  □ Load test runs AGAINST STAGING — never production         │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 — What to Monitor During Tests

```
┌──────────────────────────────────────────────────────────────┐
│  MONITORING CHECKLIST                                        │
│                                                              │
│  APPLICATION                                                 │
│  □ Response time (p50, p95, p99)                             │
│  □ Error rate (4xx, 5xx)                                     │
│  □ Throughput (requests per second)                          │
│  □ Active connections                                        │
│                                                              │
│  SERVER                                                      │
│  □ CPU utilization (per container/instance)                  │
│  □ Memory usage (watch for steady growth = leak)             │
│  □ Disk I/O                                                  │
│  □ Network I/O                                               │
│                                                              │
│  DATABASE                                                    │
│  □ Active connections (vs max pool size)                      │
│  □ Query execution time                                      │
│  □ Slow query log (queries > 100ms)                          │
│  □ Lock contention                                           │
│  □ Connection pool exhaustion                                │
│                                                              │
│  CACHE (Redis)                                               │
│  □ Hit rate (should stay > 90%)                              │
│  □ Memory usage                                              │
│  □ Eviction rate                                             │
│  □ Connection count                                          │
│                                                              │
│  INFRASTRUCTURE                                              │
│  □ Load balancer request queue                               │
│  □ ECS task count / auto-scaling events                      │
│  □ Container restarts (OOM kills)                            │
└──────────────────────────────────────────────────────────────┘
```

### 4.3 — Analysis Report Template

```markdown
## Load Test Report: [Test Name]

### Test Configuration
- **Date**: [date]
- **Environment**: staging
- **Duration**: 30 minutes
- **Peak VUs**: 200
- **Scenarios**: Learner (70%), Admin (20%), Background (10%)

### Results Summary
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| p95 latency | < 500ms | 320ms | PASS |
| p99 latency | < 1000ms | 890ms | PASS |
| Error rate | < 1% | 0.3% | PASS |
| Throughput | > 100 RPS | 145 RPS | PASS |
| Max VUs sustained | 200 | 180 | MARGINAL |

### Endpoint Breakdown
| Endpoint | p50 | p95 | p99 | Errors | Notes |
|----------|-----|-----|-----|--------|-------|
| POST /auth/login | 85ms | 210ms | 450ms | 0% | OK |
| GET /courses | 120ms | 380ms | 720ms | 0.1% | Watch at scale |
| GET /courses/:id | 95ms | 250ms | 510ms | 0% | OK |
| GET /reports | 450ms | 1200ms | 2800ms | 2.1% | BOTTLENECK |

### Bottlenecks Identified
1. **Reports endpoint** — p99 at 2800ms, 2.1% error rate.
   Root cause: Full table scan on enrollments table.
   Fix: Add index on (tenant_id, created_at).

2. **Database connections** — Pool exhausted at 180 VUs.
   Root cause: Pool size set to 20, max connections 100.
   Fix: Increase pool to 50, add connection timeout.

### Recommendations
- [ ] Add database index for reports query
- [ ] Increase connection pool from 20 to 50
- [ ] Add Redis cache for dashboard endpoint (TTL: 60s)
- [ ] Implement pagination on reports export
```

---

## Anti-Patterns — What NOT to Do

```
┌──────────────────────────────────────────────────────────────┐
│  LOAD TEST ANTI-PATTERNS                                     │
│                                                              │
│  ❌ Testing with a single endpoint                           │
│     → Real traffic hits many endpoints. Mix read/write ops.  │
│                                                              │
│  ❌ No think time between requests                           │
│     → Without delays, you test max throughput, not real load.│
│     → Real users pause between actions.                      │
│                                                              │
│  ❌ Running against production                               │
│     → Load tests can cause outages. Use staging.             │
│                                                              │
│  ❌ All virtual users doing the same thing simultaneously    │
│     → Real traffic is diverse. Use weighted scenarios.       │
│                                                              │
│  ❌ Not monitoring the server during the test                │
│     → You need to correlate response time with CPU, memory,  │
│       DB connections to find the actual bottleneck.           │
│                                                              │
│  ❌ Running once and calling it done                         │
│     → Run multiple times. Results vary. Look for trends.     │
│                                                              │
│  ❌ No baseline measurement                                  │
│     → Without a baseline, you can't tell if a change helped │
│       or hurt performance.                                   │
│                                                              │
│  ❌ Testing with fake data that doesn't match production     │
│     → Use realistic data volumes. 10 rows vs 100,000 rows   │
│       produce completely different performance profiles.      │
└──────────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Start with smoke tests** — Run 1-2 virtual users first to verify your script works. Debugging a script with 200 VUs running is painful.
2. **Use realistic think times** — Users don't fire requests every millisecond. Add 2-10 second pauses between actions to simulate real browsing.
3. **Vary the data** — Don't hit the same course ID 1000 times. Randomize course IDs, user accounts, and search queries to exercise different data paths.
4. **Ramp up gradually** — Start low and increase linearly. The point where response times start climbing is your capacity threshold.
5. **Watch the database first** — 80% of performance bottlenecks are in the database: missing indexes, N+1 queries, full table scans, connection pool exhaustion.
6. **Test after every infrastructure change** — Upgraded instance type? Changed connection pool? New cache layer? Re-run the load test to verify improvement.
7. **Keep test scripts in version control** — Load test scripts are code. Version them alongside the application.

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
