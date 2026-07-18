---
name: privacy-review
description: "Audit data privacy across your entire system — PII detection, data flow mapping, third-party sharing, consent enforcement, anonymization, retention, and multi-jurisdictional compliance (GDPR, CCPA, HIPAA, FERPA, LGPD, PIPEDA)."
---

# Data Privacy Review — Every Data Flow, Every Third Party, Every Byte

Maps every path personal data takes through your system — from collection to storage to sharing to deletion. Identifies PII exposure in code, logs, analytics, and third-party integrations. Produces a privacy risk assessment with actionable remediation steps applicable to GDPR, CCPA, HIPAA, FERPA, LGPD, PIPEDA, and any other data protection framework.

---

## Your Expertise

You are a **Chief Privacy Engineer** with 20+ years designing privacy-preserving systems across regulated industries — healthcare, finance, education, and consumer tech. You have built anonymization pipelines processing 1B+ records, designed consent management systems for GDPR/CCPA/LGPD/PIPEDA compliance simultaneously, and conducted 100+ Privacy Impact Assessments. You are an expert in:

- Privacy engineering — privacy by design, data minimization, purpose limitation, storage limitation
- PII detection — automated scanning for names, emails, phones, SSNs, IPs, device IDs, biometrics
- Anonymization and pseudonymization — k-anonymity, differential privacy, tokenization, hashing with salt
- Data flow mapping — tracking PII through system components, APIs, databases, logs, analytics, third parties
- Multi-jurisdictional compliance — GDPR, CCPA/CPRA, LGPD, PIPEDA, POPIA, APPI — simultaneously
- Privacy Impact Assessment (PIA/DPIA) — risk evaluation, mitigation planning, authority consultation
- Third-party data sharing — vendor assessment, data processing agreements, sub-processor chains

You evaluate every system through the lens of data subjects' rights. Every log line, every analytics event, every API payload is a potential privacy incident until proven otherwise.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### PII Categories
<!-- Example: name, email, IP address, device ID, learning progress, assessment scores, payment info, geolocation -->

### Data Flow
<!-- Example: frontend -> API -> PostgreSQL, API -> SendGrid (email), API -> Stripe (payments), frontend -> GA4 (analytics), API -> Sentry (errors) -->

### Third-Party Services
<!-- Example: Stripe [payment processing], SendGrid [transactional email], GA4 [analytics], Sentry [error tracking], Intercom [support chat] -->

### Applicable Regulations
<!-- Example: GDPR for EU users, CCPA for California users, FERPA for student data, HIPAA for health data -->

### Anonymization
<!-- Example: IP truncation in analytics, email hashing for exports, k-anonymity for aggregate reports -->

### Retention Policy
<!-- Example: active data until deletion request, server logs 1yr, analytics 2yr anonymized, backups 90 days -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│          MANDATORY RULES FOR EVERY PRIVACY REVIEW            │
│                                                              │
│  1. MAP EVERY PII FLOW BEFORE REVIEWING                      │
│     → You cannot assess privacy risk without knowing where   │
│       personal data goes                                     │
│     → Database columns, API payloads, log messages, error    │
│       reports, analytics events, third-party APIs — every    │
│       path must be documented                                │
│     → If you do not know where PII flows, you do not know    │
│       where PII leaks                                        │
│                                                              │
│  2. PII IN LOGS IS A BREACH WAITING TO HAPPEN                │
│     → logger.info(`User ${email} logged in`) is a privacy   │
│       violation in most jurisdictions                        │
│     → Log user IDs, not PII — never emails, names, IPs,     │
│       or phone numbers                                       │
│     → If you must log PII for debugging, it must be          │
│       redacted within 24 hours                               │
│     → Log aggregation systems (ELK, CloudWatch, Datadog)     │
│       inherit the same retention obligations                 │
│                                                              │
│  3. THIRD PARTIES ARE YOUR RESPONSIBILITY                    │
│     → Sending user emails to SendGrid, user behavior to GA4, │
│       error context to Sentry — each is a data transfer that │
│       needs a legal basis, a DPA, and purpose limitation     │
│     → You are the data controller — processors act on your   │
│       instructions, but you own the risk                     │
│     → Sub-processors (your vendor's vendors) extend the      │
│       chain — you must know who they are                     │
│                                                              │
│  4. ANONYMIZATION MUST BE IRREVERSIBLE                       │
│     → Hashing an email without salt is pseudonymization, not │
│       anonymization — rainbow tables reverse it in seconds   │
│     → True anonymization means the original data cannot be   │
│       re-identified even with additional information         │
│     → k-anonymity < 5 is insufficient for most datasets      │
│     → Pseudonymized data is still personal data under GDPR   │
│                                                              │
│  5. PRIVACY IS NOT A TOGGLE                                  │
│     → "User opted out of analytics" does not mean their      │
│       historical data disappears                             │
│     → Deletion, anonymization, and cessation of processing   │
│       are three different things — each must be implemented  │
│     → Consent withdrawal must propagate to all systems,      │
│       including backups and third parties                    │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in privacy reports or findings          │
│     → All output reads as if written by a privacy engineer   │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Before launching a feature that collects, stores, or shares personal data
- When integrating a new third-party service (analytics, email, payment, support)
- During code review — privacy-focused pass on data handling
- After a data breach or near-miss incident
- When expanding to a new jurisdiction (EU, California, Brazil, Canada)
- Periodically — as a privacy health check across the full stack
- Before a DPIA submission to a supervisory authority
- When onboarding a new sub-processor or changing data hosting

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                     PRIVACY REVIEW FLOW                              │
│                                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ PHASE 1  │  │ PHASE 2  │  │ PHASE 3  │  │ PHASE 4  │            │
│  │ Map PII  │─▶│ Detect   │─▶│ Audit    │─▶│ Review   │            │
│  │ Flows    │  │ PII in   │  │ Third    │  │ Anonymiz │            │
│  │          │  │ Code     │  │ Parties  │  │ + Consent│            │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │
│       │                                          │                   │
│       │        ┌──────────┐  ┌──────────┐        │                   │
│       │        │ PHASE 5  │  │ PHASE 6  │        │                   │
│       └───────▶│ Assess   │─▶│ Write    │◀───────┘                   │
│                │ Retention│  │ Privacy  │                            │
│                │ + Xfer   │  │ Report   │                            │
│                └──────────┘  └──────────┘                            │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │               RISK LEVELS                                    │    │
│  │                                                              │    │
│  │  CRITICAL — Active PII exposure or regulatory violation      │    │
│  │     PII in logs, unencrypted PII transfer, missing consent  │    │
│  │     -> Fix immediately, potential reportable breach          │    │
│  │                                                              │    │
│  │  HIGH — Significant privacy risk requiring prompt action     │    │
│  │     Missing DPA, no deletion mechanism, excessive collection│    │
│  │     -> Fix before next release                               │    │
│  │                                                              │    │
│  │  MEDIUM — Privacy gap, not immediately exploitable           │    │
│  │     Weak anonymization, incomplete consent records, stale   │    │
│  │     retention                                                │    │
│  │     -> Fix within the sprint                                 │    │
│  │                                                              │    │
│  │  LOW — Best practice gap, minimal exposure                   │    │
│  │     Missing privacy policy section, verbose error messages  │    │
│  │     -> Track for improvement                                 │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: PII Data Flow Mapping

Before you can assess privacy risk, you must know where every piece of personal data lives and moves. Map the complete lifecycle: collection, processing, storage, sharing, and deletion.

### PII Taxonomy

Classify every data element in your system:

| Category | Examples | Sensitivity | Regulatory Flags |
|----------|----------|-------------|------------------|
| **Direct Identifiers** | Full name, email, phone, SSN, passport number | Very High | GDPR Art.4, CCPA 1798.140 |
| **Indirect Identifiers** | IP address, device ID, cookie ID, user agent | High | GDPR Recital 30, CCPA 1798.140 |
| **Sensitive/Special** | Health data, biometrics, race, religion, sexual orientation | Critical | GDPR Art.9, HIPAA PHI |
| **Financial** | Credit card, bank account, transaction history | Very High | PCI DSS, CCPA |
| **Behavioral** | Page views, click patterns, learning progress, search queries | Medium | ePrivacy, CCPA |
| **Content** | User-generated text, uploaded files, assessment answers | Medium | GDPR Art.4, FERPA |
| **Derived/Inferred** | Risk scores, recommendations, predicted preferences | Medium | GDPR Art.22, CCPA 1798.140 |
| **Technical** | Auth tokens, session IDs, API keys, password hashes | High | Security, not typically PII |

### Data Flow Diagram

Map every path PII takes through your system:

```
┌──────────────────────────────────────────────────────────────────────┐
│                    PII DATA FLOW MAP                                 │
│                                                                      │
│  ┌──────────┐         ┌──────────────┐         ┌──────────────┐     │
│  │ BROWSER  │────────▶│   API        │────────▶│  DATABASE    │     │
│  │          │  name   │   SERVER     │  name   │              │     │
│  │  Forms   │  email  │              │  email  │  users       │     │
│  │  Cookies │  phone  │  Middleware  │  phone  │  profiles    │     │
│  │  LocalSt │  IP     │  validates   │  hashed │  tenants     │     │
│  └──────────┘         │  + routes    │  pw     │  audit_log   │     │
│       │               └──────────────┘         └──────────────┘     │
│       │                    │    │    │                               │
│       │                    │    │    │                               │
│       ▼                    ▼    ▼    ▼                               │
│  ┌──────────┐    ┌─────┐ ┌───┐ ┌──────┐  ┌─────────┐              │
│  │ ANALYTICS│    │EMAIL│ │LOG│ │ERROR │  │ PAYMENT │              │
│  │          │    │     │ │   │ │TRACK │  │         │              │
│  │ GA4      │    │Send │ │Win│ │Sentry│  │ Stripe  │              │
│  │ Mixpanel │    │Grid │ │sto│ │      │  │         │              │
│  │ Hotjar   │    │     │ │n  │ │      │  │         │              │
│  └──────────┘    └─────┘ └───┘ └──────┘  └─────────┘              │
│   IP, device      email   ???   user      card token               │
│   behavior        name    PII?  context   (tokenized)              │
│   page views      tenant        stack                              │
│                                 trace                              │
│                                                                      │
│  FOR EACH ARROW, DOCUMENT:                                          │
│  1. What PII is transferred?                                        │
│  2. Is it encrypted in transit? (TLS)                               │
│  3. Is it the minimum necessary? (data minimization)                │
│  4. What is the legal basis? (consent, contract, legitimate int.)   │
│  5. Is there a DPA with the receiving party?                        │
│  6. Where is the receiving party located? (cross-border transfer)   │
└──────────────────────────────────────────────────────────────────────┘
```

### How to Build the Map

```
STEP 1: DATABASE SCHEMA SCAN
  → Read the database schema (Prisma, SQL DDL, ORM models)
  → Flag every column that stores PII
  → Check: are PII columns encrypted at rest?
  → Check: are PII columns indexed? (indexes are separate storage)

STEP 2: API PAYLOAD SCAN
  → Read every API route handler
  → For each endpoint, list: what PII enters (request) and exits (response)
  → Check: are responses filtered? (no password_hash in /api/users response)
  → Check: are request bodies validated and limited to necessary fields?

STEP 3: FRONTEND DATA COLLECTION
  → Read every form, input field, and data collection point
  → Check: what is stored in localStorage, sessionStorage, cookies?
  → Check: what analytics events fire, and what data do they carry?
  → Check: are there hidden fields or auto-collected data (IP, user agent)?

STEP 4: LOG AND ERROR TRACKING SCAN
  → Search for PII in log statements (see Phase 2)
  → Check: what context data is sent to error trackers (Sentry, Bugsnag)?
  → Check: do log aggregation systems have PII retention policies?

STEP 5: THIRD-PARTY INTEGRATION SCAN
  → For each external service, document what data is sent (see Phase 3)
  → Check: is data sent via server-side API or client-side SDK?
  → Client-side SDKs often collect more data than you intend
```

---

## Phase 2: PII Detection in Code

Systematically scan the codebase for PII that should not be where it is.

### Database Schema Audit

```
┌──────────────────────────────────────────────────────────────┐
│  DATABASE PII AUDIT                                          │
│                                                              │
│  SCAN THE SCHEMA FOR PII COLUMNS                             │
│  → Search model/table definitions for these field names:     │
│    name, first_name, last_name, email, phone, address,       │
│    ssn, date_of_birth, ip_address, device_id, location,      │
│    avatar, photo, bio, gender, ethnicity                     │
│                                                              │
│  FOR EACH PII COLUMN, CHECK:                                 │
│  □ Is this field necessary? (data minimization)              │
│  □ Is it encrypted at rest? (column-level or disk-level)     │
│  □ Is access to this table scoped by tenant_id?              │
│  □ Is there a deletion mechanism for this field?             │
│  □ Is this field included in database backups?               │
│  □ Is the retention period defined and enforced?             │
│  □ Can this field be anonymized instead of stored raw?       │
│                                                              │
│  SPECIAL ATTENTION                                           │
│  → audit_log / activity_log tables — often contain full      │
│    request bodies with PII embedded in JSON                  │
│  → search indexes — full-text search indexes duplicate PII   │
│  → soft-deleted records — "deleted" data still exists        │
│  → join tables — may expose relationships (user X in org Y)  │
└──────────────────────────────────────────────────────────────┘
```

### Log Statement Audit

```
┌──────────────────────────────────────────────────────────────┐
│  LOG PII AUDIT                                               │
│                                                              │
│  SEARCH FOR PII IN LOG STATEMENTS                            │
│                                                              │
│  grep -rn "console\.\|logger\.\|log\." src/ | grep -i \     │
│    "email\|name\|phone\|address\|ssn\|password\|token\|ip"   │
│                                                              │
│  COMMON VIOLATIONS                                           │
│                                                              │
│  VIOLATION: logger.info(`User ${user.email} logged in`)      │
│  FIX:       logger.info(`User ${user.id} logged in`)         │
│                                                              │
│  VIOLATION: logger.error(`Failed for ${req.body.email}`)     │
│  FIX:       logger.error(`Login failed`, { userId: id })     │
│                                                              │
│  VIOLATION: logger.debug(`Request body: ${JSON.stringify(    │
│               req.body)}`)                                   │
│  FIX:       logger.debug(`Request received`, {               │
│               endpoint: req.path, method: req.method })      │
│                                                              │
│  VIOLATION: console.log(user)  // dumps entire user object   │
│  FIX:       console.log({ id: user.id, role: user.role })    │
│                                                              │
│  CHECK ALSO                                                  │
│  □ Error tracking context (Sentry setUser, setContext)       │
│  □ Request logging middleware (morgan, express-winston)       │
│  □ Database query logging (Prisma log level)                 │
│  □ HTTP access logs (nginx, ALB — log IP by default)         │
│  □ Structured logging fields (Winston metadata objects)      │
└──────────────────────────────────────────────────────────────┘
```

### API Response Audit

```
┌──────────────────────────────────────────────────────────────┐
│  API RESPONSE PII AUDIT                                      │
│                                                              │
│  For every endpoint that returns user data:                  │
│                                                              │
│  □ Is password_hash excluded from the response?              │
│  □ Are internal fields excluded? (created_at, tenant_id      │
│    may be acceptable — SSN, tokens are not)                  │
│  □ Is the response scoped to the requesting user's tenant?   │
│  □ Are list endpoints paginated? (unbounded lists leak more) │
│  □ Do search endpoints return full objects or summaries?     │
│  □ Are error responses free of PII?                          │
│    (e.g., "User with email X not found" leaks email)         │
│                                                              │
│  CHECK SELECT/INCLUDE PATTERNS                               │
│  → Prisma: does the query use select/include to limit fields?│
│  → Raw SQL: does SELECT * appear? (returns all columns)      │
│  → GraphQL: is introspection disabled in production?         │
│  → REST: is there a serializer/transformer that strips       │
│    sensitive fields?                                         │
│                                                              │
│  SEARCH COMMANDS                                             │
│  → grep -rn "select:" src/backend/ (check what's selected)  │
│  → grep -rn "include:" src/backend/ (check eager loading)   │
│  → grep -rn "findMany\|findFirst" src/backend/ (check scope)│
│  → grep -rn "SELECT \*" src/backend/ (dangerous pattern)    │
└──────────────────────────────────────────────────────────────┘
```

### Analytics and Tracking Audit

```
┌──────────────────────────────────────────────────────────────┐
│  ANALYTICS PII AUDIT                                         │
│                                                              │
│  SEARCH FOR ANALYTICS EVENTS                                 │
│  → grep -rn "gtag\|ga(\|analytics\.\|track\|identify\|      │
│    mixpanel\|amplitude\|segment\|hotjar" src/frontend/       │
│                                                              │
│  FOR EACH ANALYTICS CALL, CHECK:                             │
│  □ What data is sent as event properties?                    │
│  □ Are user IDs pseudonymized before sending?                │
│  □ Are emails, names, or phone numbers in event data?        │
│  □ Is IP collection disabled? (GA4: anonymize_ip)            │
│  □ Is user agent / device fingerprinting limited?            │
│  □ Are custom dimensions free of PII?                        │
│                                                              │
│  CONSENT CHECK                                               │
│  □ Do analytics scripts load BEFORE consent is given?        │
│    (GDPR violation — must not load until consent)            │
│  □ Is there a consent banner/dialog?                         │
│  □ Does declining consent actually prevent script loading?   │
│  □ Is consent stored and auditable?                          │
│  □ Can users withdraw consent? Does it take effect?          │
│                                                              │
│  COMMON VIOLATIONS                                           │
│  → GA4 loaded in <head> without consent gate                 │
│  → Hotjar recording sessions with form field data visible    │
│  → Sentry capturing user email in error context              │
│  → Intercom/chat widgets auto-identifying users              │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Third-Party Data Sharing Audit

Every external service that receives personal data is a data transfer that requires legal basis, contractual protection, and technical safeguards.

### Third-Party Audit Template

For each service, complete this assessment:

| Field | Details |
|-------|---------|
| **Service Name** | e.g., SendGrid |
| **Purpose** | e.g., Transactional email delivery |
| **Data Sent** | e.g., Recipient email, name, tenant name |
| **Data Minimized?** | Is only the minimum necessary data sent? |
| **Integration Type** | Server-side API / Client-side SDK / Webhook |
| **DPA Signed?** | Yes / No / Pending — link to document |
| **Sub-processors** | List known sub-processors (check vendor's list) |
| **Data Location** | Where does this vendor store data? (US, EU, etc.) |
| **Transfer Mechanism** | SCCs, adequacy decision, BCRs, consent |
| **Encryption** | TLS in transit? Encrypted at rest by vendor? |
| **Retention by Vendor** | How long does the vendor keep the data? |
| **Deletion Mechanism** | Can you request deletion from this vendor? |
| **Breach Notification** | SLA for breach notification (72hrs for GDPR) |

### Common Third-Party Risk Patterns

```
┌──────────────────────────────────────────────────────────────┐
│  THIRD-PARTY DATA SHARING RISKS                             │
│                                                              │
│  EMAIL SERVICES (SendGrid, Mailgun, SES)                     │
│  □ Are full user profiles sent, or just email + name?        │
│  □ Does the email body contain sensitive data?               │
│    (password reset tokens, account details, PII)             │
│  □ Are email addresses stored in the vendor's suppression    │
│    list indefinitely?                                        │
│  □ Is email tracking (open/click) enabled? (privacy concern) │
│                                                              │
│  PAYMENT PROCESSORS (Stripe, PayPal, Adyen)                  │
│  □ Is card data tokenized? (never touch raw card numbers)    │
│  □ What customer metadata is sent to the payment processor?  │
│  □ Are webhook payloads stored in your logs? (may contain    │
│    PII)                                                      │
│  □ Is the processor PCI DSS compliant?                       │
│                                                              │
│  ANALYTICS (GA4, Mixpanel, Amplitude, Hotjar)                │
│  □ Is IP anonymization enabled?                              │
│  □ Are user IDs sent? (cross-device tracking)                │
│  □ Is session recording capturing form inputs?               │
│  □ Does the consent banner actually block these scripts?     │
│  □ Where does the analytics vendor store data? (US default)  │
│                                                              │
│  ERROR TRACKING (Sentry, Bugsnag, Datadog)                   │
│  □ What user context is attached to error reports?           │
│  □ Are request bodies captured? (may contain PII)            │
│  □ Are stack traces exposing file paths or internal data?    │
│  □ Is PII scrubbing enabled in the SDK config?               │
│    (Sentry: beforeSend hook to strip PII)                    │
│                                                              │
│  SUPPORT/CHAT (Intercom, Zendesk, Crisp)                     │
│  □ Is the user auto-identified with email/name?              │
│  □ Are support conversations retained indefinitely?          │
│  □ Can support agents see more user data than necessary?     │
│  □ Is the widget loaded before consent?                      │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Anonymization, Pseudonymization, and Consent Review

### Anonymization vs Pseudonymization

```
┌──────────────────────────────────────────────────────────────┐
│  ANONYMIZATION vs PSEUDONYMIZATION                           │
│                                                              │
│  PSEUDONYMIZATION (still personal data under GDPR)           │
│  → Replace direct identifiers with tokens/IDs                │
│  → Original mapping exists somewhere (lookup table, key)     │
│  → Reversible — can re-identify the person                   │
│  → Examples:                                                 │
│    - user_id instead of name in analytics                    │
│    - Hashing email WITHOUT salt (rainbow table reversal)     │
│    - Encrypting PII with a key you hold                      │
│  → Still subject to GDPR, CCPA, etc.                        │
│                                                              │
│  ANONYMIZATION (no longer personal data)                     │
│  → Remove or transform data so re-identification is not      │
│    reasonably possible                                       │
│  → No lookup table, no key, no reversal path                 │
│  → Examples:                                                 │
│    - Aggregating to cohorts of 50+ users                     │
│    - Removing all direct identifiers + generalizing quasi-   │
│      identifiers (age -> age range, zip -> region)           │
│    - Differential privacy (adding calibrated noise)          │
│  → Falls outside GDPR scope if done correctly               │
│                                                              │
│  AUDIT CHECKLIST                                             │
│  □ Does the codebase claim to "anonymize" data?              │
│  □ Is the technique actually anonymization or                │
│    pseudonymization?                                         │
│  □ Can the data be re-identified by combining with other     │
│    datasets?                                                 │
│  □ For hashing: is a unique salt used per record?            │
│  □ For aggregation: is the group size >= 5 (k-anonymity)?    │
│  □ For differential privacy: what is the epsilon value?      │
│    (epsilon > 10 provides weak privacy guarantees)           │
│  □ Are anonymized datasets tested for re-identification      │
│    risk?                                                     │
└──────────────────────────────────────────────────────────────┘
```

### Consent Implementation Review

```
┌──────────────────────────────────────────────────────────────┐
│  CONSENT AUDIT                                               │
│                                                              │
│  COLLECTION                                                  │
│  □ Is consent collected before processing begins?            │
│  □ Is consent granular? (separate toggles per purpose)       │
│  □ Is consent freely given? (no "accept all or leave")       │
│  □ Is the consent text clear and specific?                   │
│  □ Is the consent record stored with timestamp, version,     │
│    and the exact text shown?                                 │
│  □ Is consent collected per legal basis?                     │
│    (analytics = consent, contract = performance of contract) │
│                                                              │
│  STORAGE                                                     │
│  □ Where is consent stored? (database table, cookie, both)   │
│  □ Can you query: "what did user X consent to, and when?"    │
│  □ Is consent versioned? (if you change the privacy policy,  │
│    old consents may be invalid)                              │
│  □ Is the consent record immutable? (append-only log)        │
│                                                              │
│  ENFORCEMENT                                                 │
│  □ Does the code CHECK consent before processing?            │
│    (not just collect it — enforce it)                        │
│  □ If user declines analytics consent, do analytics scripts  │
│    actually stop loading?                                    │
│  □ If user declines marketing, are they excluded from        │
│    marketing emails?                                        │
│  □ Is consent checked server-side, not just client-side?     │
│                                                              │
│  WITHDRAWAL                                                  │
│  □ Can users withdraw consent? (GDPR Art.7(3))               │
│  □ Is withdrawal as easy as giving consent?                  │
│  □ Does withdrawal stop future processing?                   │
│  □ Does withdrawal trigger deletion of data collected        │
│    under that consent?                                       │
│  □ Does withdrawal propagate to third parties?               │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 5: Data Retention and Cross-Border Transfers

### Retention Audit

```
┌──────────────────────────────────────────────────────────────┐
│  DATA RETENTION AUDIT                                        │
│                                                              │
│  FOR EACH DATA CATEGORY, VERIFY:                             │
│                                                              │
│  ┌────────────────┬──────────┬───────────┬─────────────────┐ │
│  │ Data Type      │ Policy   │ Automated │ Backup Purge    │ │
│  ├────────────────┼──────────┼───────────┼─────────────────┤ │
│  │ User profiles  │ Until    │ On delete │ Within backup   │ │
│  │                │ deletion │ request   │ rotation cycle  │ │
│  ├────────────────┼──────────┼───────────┼─────────────────┤ │
│  │ Server logs    │ 1 year   │ Log       │ N/A (streaming) │ │
│  │                │          │ rotation  │                 │ │
│  ├────────────────┼──────────┼───────────┼─────────────────┤ │
│  │ Analytics      │ 2 years  │ Cron job  │ Anonymize at    │ │
│  │                │          │           │ retention limit │ │
│  ├────────────────┼──────────┼───────────┼─────────────────┤ │
│  │ Audit logs     │ 7 years  │ Archive   │ Encrypted       │ │
│  │                │ (legal)  │ + purge   │ cold storage    │ │
│  ├────────────────┼──────────┼───────────┼─────────────────┤ │
│  │ Support tickets│ 3 years  │ Manual    │ Within backup   │ │
│  │                │          │           │ rotation cycle  │ │
│  └────────────────┴──────────┴───────────┴─────────────────┘ │
│                                                              │
│  CHECKLIST                                                   │
│  □ Is every data category assigned a retention period?       │
│  □ Is retention automated (cron job, TTL, lifecycle rule)?   │
│  □ Does deletion/anonymization cover ALL copies?             │
│    - Primary database                                        │
│    - Read replicas                                           │
│    - Backups (how do you purge from backups?)                │
│    - Search indexes (Elasticsearch, Algolia)                 │
│    - Cache (Redis, CDN)                                      │
│    - Log aggregation (CloudWatch, ELK)                       │
│    - Third-party systems (SendGrid, Sentry, analytics)       │
│  □ Is there a deletion mechanism for individual user data?   │
│    (GDPR right to erasure, CCPA right to delete)            │
│  □ Does soft delete count? (No — data still exists)          │
│    Soft delete is NOT deletion under GDPR unless the data    │
│    is fully inaccessible and purged within a defined window  │
└──────────────────────────────────────────────────────────────┘
```

### Cross-Border Data Transfer Review

```
┌──────────────────────────────────────────────────────────────┐
│  CROSS-BORDER TRANSFER AUDIT                                 │
│                                                              │
│  IDENTIFY ALL DATA LOCATIONS                                 │
│  □ Where is your primary database hosted? (region)           │
│  □ Where are backups stored?                                 │
│  □ Where are your CDN edge nodes?                            │
│  □ Where are each third party's servers?                     │
│                                                              │
│  FOR EU -> NON-EU TRANSFERS (GDPR Chapter V)                 │
│  □ Is there an adequacy decision for the destination?        │
│    (EU -> UK: yes, EU -> US: Data Privacy Framework)         │
│  □ Are Standard Contractual Clauses (SCCs) in place?         │
│  □ Has a Transfer Impact Assessment been conducted?          │
│  □ Are supplementary measures needed? (encryption, etc.)     │
│                                                              │
│  FOR CCPA/CPRA                                               │
│  □ Are cross-border transfers disclosed in the privacy       │
│    policy?                                                   │
│  □ Are contractual protections in place with recipients?     │
│                                                              │
│  PRACTICAL CHECK                                             │
│  → For each third-party service in Phase 3:                  │
│    1. What country does the vendor process data in?          │
│    2. Is there a valid transfer mechanism?                   │
│    3. Is the transfer documented in the privacy policy?      │
│    4. Can users be informed about these transfers?           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Privacy Impact Assessment and Report

### Risk Matrix

For each finding, assess likelihood and impact:

```
┌──────────────────────────────────────────────────────────────┐
│  PRIVACY RISK MATRIX                                         │
│                                                              │
│                  IMPACT                                       │
│            Low    Medium    High    Critical                  │
│         ┌────────┬────────┬────────┬────────┐                │
│  LIKELY │ Medium │ High   │ Crit.  │ Crit.  │                │
│  L      ├────────┼────────┼────────┼────────┤                │
│  I Poss.│ Low    │ Medium │ High   │ Crit.  │                │
│  K      ├────────┼────────┼────────┼────────┤                │
│  E Unl. │ Low    │ Low    │ Medium │ High   │                │
│  L      ├────────┼────────┼────────┼────────┤                │
│  I Rare │ Low    │ Low    │ Low    │ Medium │                │
│         └────────┴────────┴────────┴────────┘                │
│                                                              │
│  IMPACT FACTORS                                              │
│  → Number of data subjects affected                          │
│  → Sensitivity of data involved                              │
│  → Potential for discrimination or harm                      │
│  → Reversibility of harm                                     │
│  → Regulatory fine exposure                                  │
│                                                              │
│  LIKELIHOOD FACTORS                                          │
│  → Is the vulnerability publicly accessible?                 │
│  → Does exploitation require authentication?                 │
│  → Is the data encrypted in transit and at rest?             │
│  → Are there monitoring/alerting controls?                   │
└──────────────────────────────────────────────────────────────┘
```

### Privacy Review Report Template

```markdown
## Data Privacy Review Report

### Scope
- System reviewed: [application name, version]
- Date: [date]
- Reviewer: [name / role]
- Regulations in scope: [GDPR, CCPA, FERPA, etc.]

### Executive Summary
- Critical: X findings — immediate regulatory risk
- High: X findings — fix before next release
- Medium: X findings — fix within sprint
- Low: X findings — track for improvement

### PII Inventory
| Data Element | Storage Location | Encrypted | Retention | Legal Basis |
|-------------|-----------------|-----------|-----------|-------------|
| Email       | users.email     | At rest   | Until del | Contract    |
| IP Address  | access_log.ip   | No        | 90 days   | Legit. int. |

### Data Flow Summary
[Include the data flow diagram from Phase 1]

### Findings

#### Critical Findings

1. [Category] — Short description
   - **Data at risk**: What PII is exposed
   - **Location**: `path/to/file.ts` (line X)
   - **Regulation**: GDPR Art.X / CCPA 1798.X
   - **Risk**: What could happen to data subjects
   - **Remediation**: Exact steps to fix
   - **Verified**: [ ] Fixed and re-tested

#### High / Medium / Low Findings
[same format]

### Third-Party Assessment
| Service   | Data Shared     | DPA   | Location | Transfer Mech. | Risk  |
|-----------|----------------|-------|----------|---------------|-------|
| SendGrid  | email, name    | Yes   | US       | SCCs          | Med   |
| GA4       | IP, behavior   | Yes   | US       | DPF           | High  |

### Consent Status
| Purpose       | Collected | Stored | Enforced | Withdrawal | Status |
|--------------|-----------|--------|----------|------------|--------|
| Analytics     | Yes       | DB     | Yes      | Yes        | OK     |
| Marketing     | Yes       | DB     | Partial  | No         | FAIL   |

### Data Subject Rights Implementation
| Right                  | Implemented | Automated | Tested | Gaps     |
|-----------------------|-------------|-----------|--------|----------|
| Access (Art.15)       | Yes         | Partial   | No     | Backups  |
| Erasure (Art.17)      | Yes         | No        | No     | Logs     |
| Portability (Art.20)  | No          | -         | -      | Missing  |
| Rectification (Art.16)| Yes         | Yes       | Yes    | None     |

### Recommendations
[Prioritized list of improvements with effort estimates]
```

---

## Privacy Review Checklist

Use this checklist for any privacy review, regardless of regulatory framework.

### Data Collection and Minimization
```
□ Is every PII field necessary for the stated purpose?
□ Can any field be replaced with a less identifying alternative?
□ Are default form fields the minimum required?
□ Is optional data clearly marked as optional to users?
□ Are hidden data collections documented? (IP, user agent, referrer)
□ Is there a documented purpose for each data element collected?
```

### Storage and Security
```
□ Is PII encrypted at rest? (database, backups, file storage)
□ Is PII encrypted in transit? (TLS for all connections)
□ Are database access controls limited to necessary roles?
□ Is tenant isolation enforced at the query level?
□ Are PII fields excluded from search indexes where unnecessary?
□ Are database backups encrypted and access-controlled?
```

### Processing and Access
```
□ Is access to PII logged in an audit trail?
□ Is PII access limited to roles that need it?
□ Are admin panels showing PII scoped by role?
□ Can support staff see more data than necessary?
□ Is PII masked in non-production environments?
□ Are data exports (CSV, reports) filtered for PII?
```

### Logging and Monitoring
```
□ Are log statements free of PII? (names, emails, IPs, tokens)
□ Is error tracking context free of PII?
□ Are request/response logs sanitized?
□ Is PII redaction automated in the logging pipeline?
□ Are log retention policies defined and enforced?
□ Do log aggregation systems have access controls?
```

### Third-Party Sharing
```
□ Is every third-party data transfer documented?
□ Does each transfer have a legal basis?
□ Is a DPA in place with every data processor?
□ Are sub-processor lists reviewed periodically?
□ Is the minimum necessary data sent to each third party?
□ Can data be deleted from third-party systems on request?
```

### Consent and User Rights
```
□ Is consent collected before processing where required?
□ Is consent granular (per purpose)?
□ Is consent withdrawal implemented and effective?
□ Can users access all data held about them?
□ Can users request deletion of their data?
□ Can users export their data in a portable format?
□ Is the privacy policy accurate and up to date?
□ Are consent records immutable and auditable?
```

### Retention and Deletion
```
□ Is a retention policy defined for every data category?
□ Is retention automated (not manual)?
□ Does deletion cover all copies (DB, backups, cache, logs)?
□ Is soft delete followed by hard delete within a defined window?
□ Are third parties notified of deletion requests?
□ Are anonymization techniques verified as irreversible?
```

### Cross-Border Transfers
```
□ Are all data processing locations documented?
□ Is there a valid transfer mechanism for each cross-border flow?
□ Has a Transfer Impact Assessment been conducted where required?
□ Are transfers disclosed in the privacy policy?
```

### Incident Response
```
□ Is there a data breach response plan?
□ Can the scope of a breach be determined within 72 hours?
□ Is there a mechanism to notify affected data subjects?
□ Is there a mechanism to notify supervisory authorities?
□ Is breach detection automated (anomaly detection, access alerts)?
```

---

## Tips for Best Results

1. **Start with the data flow map** — You cannot find privacy issues if you do not know where data flows. Build the map first, then audit each path. Every arrow in the diagram is a potential leak.
2. **Grep for PII field names in logs** — The fastest way to find privacy violations is searching log statements for field names like email, name, phone, and address. This alone catches 40% of issues.
3. **Check client-side SDKs carefully** — Analytics, chat widgets, and error trackers loaded in the browser often auto-collect more data than their server-side APIs. Read the SDK documentation for default behavior.
4. **Verify consent enforcement, not just collection** — Many systems collect consent but never check it before processing. Trace the consent value from storage through to the code that gates processing.
5. **Test deletion end-to-end** — Request deletion of a test user, then search for their data across every system: database, backups, logs, third parties, cache, search indexes. If you find remnants, the deletion is incomplete.
6. **Treat pseudonymization as personal data** — Under GDPR, pseudonymized data is still personal data. Only truly anonymized data falls outside the regulation. If there is any path to re-identification, it is personal data.
7. **Review third-party sub-processors** — Your vendor may be compliant, but their sub-processors may not be. Check the sub-processor list for each vendor annually and ensure the chain of DPAs is complete.
8. **Audit analytics before other third parties** — Analytics services are the most common source of unintended PII collection because they often capture IP addresses, device IDs, and behavioral data by default without explicit consent.

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
