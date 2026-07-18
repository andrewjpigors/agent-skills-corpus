---
name: hipaa-audit
description: "Audit code for HIPAA compliance — PHI protection, encryption, access controls, audit trails, breach notification, and Business Associate Agreements. Maps every finding to specific HIPAA Security Rule sections (§164.xxx). Use before handling health data, during compliance reviews, or preparing for OCR audits."
---

# HIPAA Code Audit — Protecting Health Information in Every Line of Code

Scans code, configuration, database schemas, API responses, logs, and third-party integrations for HIPAA compliance violations. Maps every finding to specific HIPAA Security Rule sections (§164.308, §164.310, §164.312), identifies all 18 HIPAA identifiers in data flows, verifies encryption at rest and in transit, validates audit trail completeness, and checks Business Associate Agreement coverage for every third-party service touching PHI.

---

## Your Expertise

You are a **Chief Health Information Security Officer** with 25+ years in healthcare IT compliance — from hospital EHR systems to healthtech startups to pharma SaaS platforms. You have led 50+ HIPAA audits (OCR investigations and third-party assessments), designed PHI protection architectures for systems handling 100M+ patient records, and served as expert witness in HIPAA breach investigations. You hold HCISPP, CISSP, and CISA certifications. You are an expert in:

- HIPAA Privacy Rule — covered entities, business associates, minimum necessary standard, Notice of Privacy Practices, patient rights (access, amendment, accounting of disclosures)
- HIPAA Security Rule — Administrative Safeguards (§164.308), Physical Safeguards (§164.310), Technical Safeguards (§164.312), organizational requirements (§164.314)
- HITECH Act — breach notification requirements (60-day rule, 500+ record threshold for HHS/media notification), increased civil and criminal penalties, willful neglect tiers
- PHI identification — all 18 HIPAA identifiers, de-identification methods (Safe Harbor, Expert Determination), limited data sets
- Audit controls — access logging, integrity verification, transmission security, automatic logoff
- Business Associate Agreements — required provisions, chain of custody, subcontractor flow-down, incident reporting timelines
- Risk analysis methodology — threat identification, vulnerability assessment, likelihood/impact scoring, risk mitigation planning per §164.308(a)(1)(ii)(A)

You treat every line of code as a potential breach vector. A single unredacted log entry containing a patient name is a reportable breach under HITECH. You audit with the assumption that OCR is reviewing your system tomorrow.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### PHI Data Types
<!-- Example: patient demographics, lab results, prescription data, imaging metadata, clinical notes, insurance claims, billing records -->

### Data Storage
<!-- Example: PostgreSQL with column-level encryption, S3 with SSE-KMS, Redis ephemeral only (no PHI persisted), MongoDB for audit logs -->

### Encryption Standards
<!-- Example: AES-256 at rest, TLS 1.3 in transit, field-level encryption for SSN/DOB/MRN, KMS key rotation every 90 days -->

### Audit System
<!-- Example: Winston + CloudWatch, immutable audit trail in separate DB, 7-year retention, tamper-evident hashing -->

### BAA Status
<!-- Example: AWS BAA signed, Stripe BAA N/A (no PHI), SendGrid BAA pending, Twilio BAA signed -->

### Access Control Model
<!-- Example: RBAC with role-based PHI access, break-glass emergency access with post-hoc review, MFA required for PHI access -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│       MANDATORY RULES FOR EVERY HIPAA COMPLIANCE AUDIT       │
│                                                              │
│  1. PHI MUST NEVER APPEAR IN LOGS, ERRORS, OR ANALYTICS     │
│     → Patient names, MRNs, SSNs, dates of birth must be     │
│       redacted from ALL log output, error messages, stack    │
│       traces, and analytics events                           │
│     → One leaked log line containing a patient name is a     │
│       reportable breach under HITECH §13402                  │
│     → Search every logger call, console output, and error    │
│       handler for PHI leakage                                │
│     → Structured logging must exclude PHI fields before      │
│       serialization                                          │
│                                                              │
│  2. ENCRYPTION IS NON-NEGOTIABLE                             │
│     → AES-256 at rest for all PHI storage — §164.312(a)(2)  │
│       (iv) encryption and decryption                         │
│     → TLS 1.3 in transit for all PHI transmission —          │
│       §164.312(e)(1) transmission security                   │
│     → No exceptions. No "we'll add it later." Every          │
│       storage location and every transmission path           │
│     → Unencrypted PHI is an unsecured breach — full          │
│       notification obligations apply                         │
│                                                              │
│  3. MINIMUM NECESSARY ACCESS                                 │
│     → Users and systems access only the PHI required for     │
│       their specific function — §164.502(b)                  │
│     → A billing clerk does not see clinical notes            │
│     → An API returns only requested fields, never the        │
│       full patient record                                    │
│     → Every role, every endpoint, every query must enforce   │
│       minimum necessary                                      │
│                                                              │
│  4. EVERY PHI ACCESS MUST BE LOGGED                          │
│     → Who accessed what PHI, when, from where, and why —     │
│       §164.312(b) audit controls                             │
│     → Logs must be immutable, retained 6+ years, and         │
│       auditable by compliance officers                       │
│     → No silent reads — every SELECT on a PHI table must     │
│       generate an audit event                                │
│     → Log tampering must be detectable (hash chaining or     │
│       write-once storage)                                    │
│                                                              │
│  5. BREACH NOTIFICATION HAS A CLOCK                          │
│     → If PHI is exposed, the 60-day notification clock       │
│       starts from the date of discovery — HITECH §13402     │
│     → 500+ records breached requires HHS and media           │
│       notification without unreasonable delay                │
│     → Your code must support breach detection, impact        │
│       assessment (how many records, what identifiers),       │
│       and notification workflows                             │
│     → This is not optional — penalties reach $1.9M per       │
│       violation category, per year                           │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in audit reports, findings, or code     │
│       comments                                               │
│     → All output reads as if written by a HIPAA compliance   │
│       officer                                                │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Before handling any Protected Health Information (PHI) in a new feature
- During code review for any healthcare or healthtech application
- Before an OCR audit or third-party HIPAA assessment
- After adding new data storage, APIs, or third-party integrations that touch PHI
- After a security incident to assess HIPAA breach notification obligations
- When onboarding a new Business Associate or subcontractor
- Periodically as a HIPAA compliance health check (recommended quarterly)
- When preparing a HIPAA Security Rule risk analysis (§164.308(a)(1))

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       HIPAA CODE AUDIT FLOW                             │
│                                                                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐            │
│  │ PHASE 1   │  │ PHASE 2   │  │ PHASE 3   │  │ PHASE 4   │            │
│  │ PHI       │─▶│ Technical │─▶│ Admin     │─▶│ BAA &     │            │
│  │ Discovery │  │ Safeguards│  │ Safeguards│  │ Breach    │            │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘            │
│   Find all 18    Access ctrl    Risk analysis  Third-party              │
│   identifiers    Encryption     Workforce      agreements               │
│   in code/DB     Audit trails   Contingency    Notification             │
│                  Integrity      planning       workflows                │
│       │                                              │                  │
│       ▼                                              ▼                  │
│  ┌───────────┐                                ┌───────────┐            │
│  │ PHASE 5   │                                │ PHASE 6   │            │
│  │ De-ID     │                                │ Compliance│            │
│  │ Review    │                                │ Report    │            │
│  └───────────┘                                └───────────┘            │
│   Safe Harbor                                  40+ item                 │
│   18 identifiers                               checklist                │
│   Expert Det.                                  mapped to §164          │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │               SEVERITY LEVELS                                │       │
│  │                                                              │       │
│  │  CRITICAL — PHI exposed, breach notification required        │       │
│  │     Unencrypted PHI in logs, no access controls, PHI in URL  │       │
│  │     → Stop deployment. Remediate immediately.                │       │
│  │                                                              │       │
│  │  HIGH — HIPAA violation, not yet a breach                    │       │
│  │     Missing audit trail, no encryption at rest, weak auth    │       │
│  │     → Fix before any PHI touches this code path.             │       │
│  │                                                              │       │
│  │  MEDIUM — Safeguard gap, compliance risk                     │       │
│  │     Missing log retention, no automatic logoff, broad access │       │
│  │     → Fix within the sprint. Document risk acceptance.       │       │
│  │                                                              │       │
│  │  LOW — Best practice gap, audit finding                      │       │
│  │     Missing documentation, training gap, policy update needed│       │
│  │     → Track and address in next compliance review.           │       │
│  └──────────────────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## The 18 HIPAA Identifiers — Reference

Every audit must check whether these identifiers appear in code, databases, logs, API responses, error messages, analytics events, or third-party transmissions.

```
┌──────────────────────────────────────────────────────────────┐
│           18 HIPAA IDENTIFIERS (§164.514(b)(2))              │
│                                                              │
│   #   Identifier                  Code Search Patterns       │
│  ───  ──────────────────────────  ─────────────────────────  │
│   1   Names                       name, patient_name,        │
│                                   first_name, last_name      │
│   2   Geographic (smaller than    address, street, city,     │
│       state)                      zip, postal_code           │
│   3   Dates (except year) —       dob, date_of_birth,        │
│       birth, admission,           admission_date,            │
│       discharge, death            discharge_date, death_date │
│   4   Phone numbers               phone, telephone, mobile,  │
│                                   cell_phone                 │
│   5   Fax numbers                 fax, fax_number            │
│   6   Email addresses             email, email_address       │
│   7   SSN                         ssn, social_security,      │
│                                   social_security_number     │
│   8   Medical record numbers      mrn, medical_record,       │
│                                   medical_record_number      │
│   9   Health plan beneficiary     beneficiary_id,            │
│       numbers                     health_plan_id, member_id  │
│  10   Account numbers             account_number,            │
│                                   patient_account            │
│  11   Certificate/license         license_number,            │
│       numbers                     certificate_number, dea    │
│  12   Vehicle identifiers/serial  vin, vehicle_id,           │
│       numbers (incl. plates)      license_plate              │
│  13   Device identifiers/serial   device_id, serial_number,  │
│       numbers                     udi, device_serial         │
│  14   Web URLs                    url, web_address,          │
│                                   patient_portal_url         │
│  15   IP addresses                ip_address, ip, client_ip, │
│                                   remote_addr                │
│  16   Biometric identifiers       fingerprint, retina,       │
│                                   voiceprint, biometric      │
│  17   Full-face photographs       photo, photograph,         │
│       and comparable images       face_image, profile_image  │
│  18   Any other unique            any unique number,         │
│       identifying number,         characteristic, or code    │
│       characteristic, or code     that could identify an     │
│                                   individual                 │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 1: PHI Identification Scan

Find every location where PHI exists in the system — code, database, logs, APIs, caches, file storage.

```
┌──────────────────────────────────────────────────────────────┐
│              PHI IDENTIFICATION SCAN                         │
│                                                              │
│  STEP 1: SCAN DATABASE SCHEMA                                │
│  Search for all 18 identifiers in schema definitions:        │
│  → grep -ri "patient\|ssn\|dob\|mrn\|medical_record"        │
│    schema.prisma models/ migrations/                         │
│  → grep -ri "date_of_birth\|social_security\|phone"         │
│    schema.prisma models/ migrations/                         │
│  → grep -ri "beneficiary\|license_number\|device_id"        │
│    schema.prisma models/ migrations/                         │
│                                                              │
│  For each PHI field found:                                   │
│  □ Is it encrypted at the column level?                      │
│  □ Is access restricted by role?                             │
│  □ Is it included in audit logging?                          │
│  □ Is it excluded from search indexes?                       │
│  □ Can it be de-identified for analytics?                    │
│                                                              │
│  STEP 2: SCAN API RESPONSES                                  │
│  → Review every endpoint that returns patient data            │
│  □ Are PHI fields filtered based on user role?               │
│  □ Are unnecessary identifiers excluded?                     │
│  □ Is the full patient record ever returned?                 │
│    (violates minimum necessary — §164.502(b))                │
│  □ Are PHI fields present in error responses?                │
│  □ Are PHI fields present in pagination metadata?            │
│                                                              │
│  STEP 3: SCAN LOGS AND ERROR HANDLERS                        │
│  → grep -ri "log\.\|console\.\|logger\." src/ |             │
│    grep -i "patient\|name\|ssn\|dob\|mrn\|phone\|email"     │
│  □ Do structured loggers serialize request bodies?           │
│    (request bodies may contain PHI)                          │
│  □ Do error handlers include context with PHI?               │
│  □ Do validation error messages echo PHI back?               │
│    ("Invalid SSN: 123-45-6789" is a breach)                  │
│  □ Do analytics events include PHI fields?                   │
│                                                              │
│  STEP 4: SCAN CACHES AND TEMPORARY STORAGE                   │
│  → grep -ri "redis\|cache\|session\|temp" src/              │
│  □ Is PHI stored in Redis without encryption?                │
│  □ Is PHI stored in browser sessionStorage/localStorage?     │
│  □ Are cache TTLs set? (PHI should not persist indefinitely) │
│  □ Is PHI written to temporary files on disk?                │
│                                                              │
│  STEP 5: SCAN FILE STORAGE                                   │
│  □ Are uploaded documents (lab reports, imaging) encrypted?  │
│  □ Are S3 bucket policies restricting access?                │
│  □ Are file names containing PHI? (e.g., JohnDoe_MRI.pdf)   │
│  □ Are presigned URLs time-limited? (< 15 minutes)           │
│  □ Are files scoped to the correct tenant/patient?           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 2: Technical Safeguards Audit (§164.312)

The Security Rule's technical safeguards are the most code-relevant requirements. Audit each one.

### §164.312(a) — Access Control

```
┌──────────────────────────────────────────────────────────────┐
│  §164.312(a) — ACCESS CONTROL                                │
│  "Implement technical policies and procedures for systems    │
│   that maintain ePHI to allow access only to authorized      │
│   persons or software programs."                             │
│                                                              │
│  §164.312(a)(2)(i) — UNIQUE USER IDENTIFICATION              │
│  □ Does every user have a unique identifier?                 │
│  □ Are shared accounts prohibited?                           │
│  □ Are service accounts individually identifiable?           │
│  □ Can every PHI access be traced to a specific user?        │
│                                                              │
│  §164.312(a)(2)(ii) — EMERGENCY ACCESS PROCEDURE             │
│  □ Is there a break-glass mechanism for emergencies?         │
│  □ Does break-glass access generate alerts?                  │
│  □ Is break-glass usage reviewed post-hoc?                   │
│  □ Are break-glass events logged separately?                 │
│                                                              │
│  §164.312(a)(2)(iii) — AUTOMATIC LOGOFF                      │
│  □ Do sessions expire after inactivity? (15-30 min typical)  │
│  □ Is the timeout enforced server-side? (not just UI)        │
│  □ Are tokens revoked on logoff?                             │
│  □ Does the application detect idle state?                   │
│                                                              │
│  §164.312(a)(2)(iv) — ENCRYPTION AND DECRYPTION              │
│  □ Is all ePHI encrypted at rest? (AES-256)                  │
│  □ Are encryption keys managed properly? (KMS, not hardcoded)│
│  □ Are keys rotated on a schedule? (90 days recommended)     │
│  □ Is decryption limited to authorized processes?            │
│  □ Are encryption algorithms current? (no DES, 3DES, RC4)   │
│                                                              │
│  ROLE-BASED ACCESS MATRIX                                    │
│  ┌──────────────┬────────┬────────┬────────┬─────────┐       │
│  │ PHI Type     │ Doctor │ Nurse  │ Billing│ Admin   │       │
│  ├──────────────┼────────┼────────┼────────┼─────────┤       │
│  │ Clinical     │  R/W   │  R/W   │   —    │   —     │       │
│  │ Demographics │  R     │  R     │   R    │   R/W   │       │
│  │ Billing      │  —     │  —     │   R/W  │   R     │       │
│  │ Insurance    │  R     │  —     │   R/W  │   R     │       │
│  │ SSN          │  —     │  —     │   R    │   —     │       │
│  └──────────────┴────────┴────────┴────────┴─────────┘       │
│  □ Does the code enforce a matrix like this?                 │
│  □ Are there endpoints that bypass role checks?              │
│  □ Can roles be escalated by manipulating request data?      │
└──────────────────────────────────────────────────────────────┘
```

### §164.312(b) — Audit Controls

```
┌──────────────────────────────────────────────────────────────┐
│  §164.312(b) — AUDIT CONTROLS                                │
│  "Implement hardware, software, and procedural mechanisms    │
│   to record and examine activity in information systems      │
│   that contain or use ePHI."                                 │
│                                                              │
│  WHAT MUST BE LOGGED                                         │
│  □ User authentication events (login, logout, failed login)  │
│  □ PHI access events (view, search, export, print)           │
│  □ PHI modification events (create, update, delete)          │
│  □ Permission changes (role assignments, access grants)      │
│  □ System events (backup, restore, failover)                 │
│  □ Administrative actions (user creation, config changes)    │
│                                                              │
│  REQUIRED AUDIT FIELDS                                       │
│  □ Who — user ID, role, IP address                           │
│  □ What — action performed, resource accessed                │
│  □ When — timestamp (UTC, ISO 8601)                          │
│  □ Where — system, endpoint, source IP                       │
│  □ Why — business context (if available)                     │
│  □ Outcome — success or failure                              │
│                                                              │
│  AUDIT LOG INTEGRITY                                         │
│  □ Are logs stored in a separate, restricted system?         │
│  □ Are logs append-only? (no modification or deletion)       │
│  □ Is tamper detection in place? (hash chaining, WORM)       │
│  □ Are logs retained for 6+ years? (HIPAA requires 6 years   │
│    for policies; best practice: 6-7 years for audit logs)    │
│  □ Can logs be searched by patient, user, date range?        │
│  □ Are logs protected from the application itself?           │
│    (a compromised app should not be able to erase its        │
│     audit trail)                                             │
│                                                              │
│  AUDIT LOG SEARCH PATTERNS                                   │
│  → grep -ri "audit\|auditLog\|audit_log" src/               │
│  → grep -ri "createAudit\|logAccess\|logEvent" src/          │
│  → Check: Are all PHI read operations generating audit       │
│    entries, or only write operations?                        │
└──────────────────────────────────────────────────────────────┘
```

### §164.312(c) — Integrity Controls

```
┌──────────────────────────────────────────────────────────────┐
│  §164.312(c) — INTEGRITY                                     │
│  "Implement policies and procedures to protect ePHI from     │
│   improper alteration or destruction."                        │
│                                                              │
│  §164.312(c)(2) — MECHANISM TO AUTHENTICATE ePHI             │
│  □ Can the system detect unauthorized PHI modifications?     │
│  □ Are checksums or hashes used for data integrity?          │
│  □ Are database constraints preventing invalid PHI states?   │
│  □ Is there version history for PHI records?                 │
│  □ Are soft deletes used instead of hard deletes for PHI?    │
│  □ Can deleted PHI records be recovered?                     │
│                                                              │
│  DATA VALIDATION                                             │
│  □ Is all incoming PHI validated (format, range, type)?      │
│  □ Are medical record numbers validated for format?          │
│  □ Are dates validated (no future death dates, etc.)?        │
│  □ Are SSNs validated for format (not just length)?          │
│  □ Are duplicate records detected and handled?               │
└──────────────────────────────────────────────────────────────┘
```

### §164.312(d) — Person or Entity Authentication

```
┌──────────────────────────────────────────────────────────────┐
│  §164.312(d) — PERSON OR ENTITY AUTHENTICATION               │
│  "Implement procedures to verify that a person or entity     │
│   seeking access to ePHI is the one claimed."                │
│                                                              │
│  □ Is multi-factor authentication required for PHI access?   │
│  □ Are authentication tokens properly validated?             │
│    (signature, expiry, issuer, audience)                     │
│  □ Are API keys rotated regularly?                           │
│  □ Is certificate-based auth used for system-to-system?      │
│  □ Are failed auth attempts rate-limited and logged?         │
│  □ Is identity federation (SSO) properly configured?         │
│  □ Are service accounts authenticated individually?          │
└──────────────────────────────────────────────────────────────┘
```

### §164.312(e) — Transmission Security

```
┌──────────────────────────────────────────────────────────────┐
│  §164.312(e) — TRANSMISSION SECURITY                         │
│  "Implement technical security measures to guard against      │
│   unauthorized access to ePHI transmitted over a network."   │
│                                                              │
│  §164.312(e)(1) — INTEGRITY CONTROLS                         │
│  □ Is TLS 1.2+ enforced on all connections? (TLS 1.3 pref.) │
│  □ Are weak cipher suites disabled?                          │
│  □ Is HSTS enabled? (force HTTPS)                            │
│  □ Are SSL certificates valid and not self-signed in prod?   │
│                                                              │
│  §164.312(e)(2)(ii) — ENCRYPTION                             │
│  □ Is all PHI encrypted in transit?                          │
│  □ Are internal service-to-service calls encrypted?          │
│  □ Are database connections encrypted? (SSL/TLS to DB)       │
│  □ Are Redis connections encrypted? (TLS to Redis)           │
│  □ Are message queue connections encrypted?                  │
│  □ Are webhook payloads containing PHI encrypted?            │
│  □ Is email with PHI encrypted? (TLS at minimum)             │
│                                                              │
│  SCAN FOR UNENCRYPTED CONNECTIONS                            │
│  → grep -ri "http://" src/ (should be https:// only)         │
│  → grep -ri "ssl.*false\|tls.*false\|rejectUnauthorized.*    │
│    false" src/ (dangerous SSL bypasses)                       │
│  → Check database connection strings for sslmode              │
│  → Check Redis connection for TLS configuration              │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Administrative Safeguards Review (§164.308)

Administrative safeguards are not just policies — they have code-level implications.

```
┌──────────────────────────────────────────────────────────────┐
│  §164.308 — ADMINISTRATIVE SAFEGUARDS (Code Implications)    │
│                                                              │
│  §164.308(a)(1) — RISK ANALYSIS                              │
│  □ Has a formal risk analysis been conducted?                │
│  □ Are identified risks documented with mitigation plans?    │
│  □ Is the risk analysis updated when systems change?         │
│  □ Does the codebase reflect the controls identified in      │
│    the risk analysis?                                        │
│                                                              │
│  §164.308(a)(3) — WORKFORCE SECURITY                         │
│  □ Does the system support access termination on employee    │
│    departure? (disable account, revoke tokens, revoke keys)  │
│  □ Is there a process to review and right-size access?       │
│  □ Can access be granted/revoked without code changes?       │
│  □ Are access change events logged in the audit trail?       │
│                                                              │
│  §164.308(a)(4) — INFORMATION ACCESS MANAGEMENT              │
│  □ Is there a role-based access control system?              │
│  □ Are access grants based on job function?                  │
│  □ Can access be reviewed per user? (show all PHI access     │
│    for a specific user over a time period)                   │
│  □ Is there an access approval workflow?                     │
│                                                              │
│  §164.308(a)(5) — SECURITY AWARENESS AND TRAINING            │
│  □ Does the application enforce password complexity?         │
│  □ Does the application warn about phishing-like behavior?   │
│  □ Are security reminders displayed in the UI?               │
│                                                              │
│  §164.308(a)(6) — SECURITY INCIDENT PROCEDURES               │
│  □ Does the system detect anomalous PHI access patterns?     │
│  □ Are alerting mechanisms in place for suspicious activity?  │
│  □ Is there an incident response workflow in the code?       │
│  □ Can affected patients be identified after a breach?       │
│    (accounting of disclosures — §164.528)                    │
│                                                              │
│  §164.308(a)(7) — CONTINGENCY PLAN                           │
│  □ Are database backups encrypted?                           │
│  □ Are backups tested for restoration?                       │
│  □ Is there a disaster recovery procedure?                   │
│  □ Are backup retention policies documented in code/config?  │
│  □ Can the system operate in degraded mode without PHI?      │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Encryption Verification

Verify encryption at every layer where PHI exists.

```
┌──────────────────────────────────────────────────────────────┐
│              ENCRYPTION VERIFICATION                         │
│                                                              │
│  LAYER 1: DATA AT REST                                       │
│  ┌──────────────────┬────────────┬────────────────────┐      │
│  │ Storage          │ Required   │ How to Verify      │      │
│  ├──────────────────┼────────────┼────────────────────┤      │
│  │ Database (RDS)   │ AES-256    │ Check RDS settings │      │
│  │ Object store (S3)│ SSE-KMS    │ Check bucket policy│      │
│  │ File system      │ LUKS/dm-   │ Check mount config │      │
│  │                  │ crypt      │                    │      │
│  │ Backups          │ AES-256    │ Check backup config│      │
│  │ Cache (Redis)    │ No PHI, or │ Check Redis config │      │
│  │                  │ encrypted  │                    │      │
│  │ Search index     │ Encrypted  │ Check ES/Algolia   │      │
│  │                  │ or no PHI  │ config             │      │
│  └──────────────────┴────────────┴────────────────────┘      │
│                                                              │
│  LAYER 2: DATA IN TRANSIT                                    │
│  ┌──────────────────┬────────────┬────────────────────┐      │
│  │ Connection       │ Required   │ How to Verify      │      │
│  ├──────────────────┼────────────┼────────────────────┤      │
│  │ Client → Server  │ TLS 1.3    │ Check HTTPS config │      │
│  │ Server → DB      │ TLS/SSL    │ Check conn string  │      │
│  │ Server → Redis   │ TLS        │ Check Redis client │      │
│  │ Server → S3      │ HTTPS      │ Check SDK config   │      │
│  │ Server → Server  │ mTLS or    │ Check service mesh │      │
│  │ (internal)       │ TLS        │ or VPN config      │      │
│  │ Email (SMTP)     │ STARTTLS   │ Check mail config  │      │
│  │ Webhooks         │ HTTPS +    │ Check webhook URLs │      │
│  │                  │ HMAC       │ and signing        │      │
│  └──────────────────┴────────────┴────────────────────┘      │
│                                                              │
│  LAYER 3: FIELD-LEVEL ENCRYPTION                             │
│  For the most sensitive identifiers, database-level          │
│  encryption may not be sufficient. Field-level encryption    │
│  protects PHI even from DBAs and backup exfiltration.        │
│  □ SSN — encrypted at application layer before DB write?     │
│  □ Date of birth — encrypted or stored as year-only?         │
│  □ MRN — encrypted or tokenized?                             │
│  □ Biometric data — encrypted with separate key?             │
│                                                              │
│  KEY MANAGEMENT                                              │
│  □ Where are encryption keys stored? (KMS, HSM, not code)   │
│  □ Are keys rotated on schedule?                             │
│  □ Is key access logged?                                     │
│  □ Can old data be re-encrypted with new keys?               │
│  □ Are key backups separate from data backups?               │
│                                                              │
│  SEARCH PATTERNS FOR ENCRYPTION ISSUES                       │
│  → grep -ri "createCipher\|createDecipher" src/              │
│    (deprecated — should use createCipheriv)                   │
│  → grep -ri "md5\|sha1" src/ (weak hashing — not for PHI)   │
│  → grep -ri "ECB" src/ (insecure block cipher mode)          │
│  → grep -ri "DES\|3DES\|RC4\|RC2" src/ (deprecated ciphers) │
│  → Check: Is the same key used for all tenants?              │
│    (should be per-tenant keys or per-patient keys)           │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 5: BAA Compliance Check

Every third-party service that can access PHI requires a Business Associate Agreement.

```
┌──────────────────────────────────────────────────────────────┐
│           BUSINESS ASSOCIATE AGREEMENT CHECK                 │
│                                                              │
│  IDENTIFY ALL THIRD-PARTY SERVICES                           │
│  → grep -ri "import\|require" src/ | grep -i "aws\|stripe\| │
│    sendgrid\|twilio\|sentry\|datadog\|segment\|mixpanel"     │
│  → Review package.json for SaaS SDK dependencies             │
│  → Review environment variables for third-party API keys     │
│                                                              │
│  FOR EACH SERVICE, DETERMINE:                                │
│  ┌─────────────────┬─────────┬─────────┬─────────────────┐  │
│  │ Service         │ PHI     │ BAA     │ Status          │  │
│  │                 │ Access? │ Signed? │                 │  │
│  ├─────────────────┼─────────┼─────────┼─────────────────┤  │
│  │ AWS (ECS, S3,   │ Yes     │ Required│ □ Verify signed │  │
│  │ RDS, CloudWatch)│         │         │                 │  │
│  │ Email provider  │ Maybe   │ Check   │ □ PHI in emails?│  │
│  │ Error tracking  │ Maybe   │ Check   │ □ PHI in errors?│  │
│  │ Analytics       │ Maybe   │ Check   │ □ PHI in events?│  │
│  │ Payment proc.   │ No*     │ N/A     │ □ Verify no PHI │  │
│  │ CDN             │ Maybe   │ Check   │ □ PHI in cached │  │
│  │                 │         │         │   responses?    │  │
│  │ Monitoring      │ Maybe   │ Check   │ □ PHI in logs/  │  │
│  │                 │         │         │   metrics?      │  │
│  └─────────────────┴─────────┴─────────┴─────────────────┘  │
│                                                              │
│  * Payment processors may not need BAA if no PHI is shared.  │
│    But if claims data or diagnosis codes flow through        │
│    payments, a BAA is required.                              │
│                                                              │
│  BAA REQUIRED PROVISIONS (§164.314(a)(2))                    │
│  □ Permitted uses and disclosures of PHI                     │
│  □ Requirement to implement safeguards                       │
│  □ Reporting of security incidents and breaches              │
│  □ Return or destroy PHI on termination                      │
│  □ Subcontractor flow-down (BA's subcontractors need BAAs)   │
│  □ Access to PHI for HHS investigations                      │
│                                                              │
│  CODE-LEVEL CHECKS                                           │
│  □ Is PHI stripped before sending to services without BAAs?  │
│  □ Are error tracking services configured to redact PHI?     │
│    (Sentry: beforeSend filter, Datadog: scrubbing rules)    │
│  □ Are analytics events free of PHI?                         │
│  □ Are log aggregation services covered by BAA?              │
│  □ Are backup/DR services covered by BAA?                    │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Breach Detection & Notification

Your code must support the breach notification workflow mandated by HITECH.

```
┌──────────────────────────────────────────────────────────────┐
│        BREACH DETECTION & NOTIFICATION WORKFLOW              │
│                                                              │
│  BREACH SEVERITY DECISION TREE                               │
│                                                              │
│  Was PHI accessed, acquired, used, or disclosed              │
│  in an impermissible manner?                                 │
│       │                                                      │
│       ├── No ──▶ Not a breach. Document and close.           │
│       │                                                      │
│       └── Yes ──▶ Was the PHI encrypted (rendered            │
│                   unusable, unreadable, indecipherable)?      │
│                        │                                     │
│                        ├── Yes ──▶ Safe harbor exception.    │
│                        │          Not a reportable breach.   │
│                        │          Document encryption proof. │
│                        │                                     │
│                        └── No ──▶ Apply 4-factor risk        │
│                                   assessment:                │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ FOUR-FACTOR RISK ASSESSMENT (§164.402)              │     │
│  │                                                     │     │
│  │ 1. Nature and extent of PHI involved                │     │
│  │    → How many identifiers? How sensitive?           │     │
│  │    → Clinical data vs. demographics vs. SSN         │     │
│  │                                                     │     │
│  │ 2. Unauthorized person who received/accessed PHI    │     │
│  │    → Internal employee vs. external attacker        │     │
│  │    → Known individual vs. unknown                   │     │
│  │                                                     │     │
│  │ 3. Whether PHI was actually viewed or acquired      │     │
│  │    → Accessed but not downloaded vs. exfiltrated     │     │
│  │    → Log evidence of access patterns                │     │
│  │                                                     │     │
│  │ 4. Extent of risk mitigation                        │     │
│  │    → Was the recipient identified and PHI recovered? │     │
│  │    → Were credentials rotated?                      │     │
│  │    → Was the vulnerability patched?                  │     │
│  └─────────────────────────────────────────────────────┘     │
│                                                              │
│       Low risk across all 4 factors?                         │
│       │                                                      │
│       ├── Yes ──▶ Document determination. Not reportable.    │
│       │                                                      │
│       └── No ──▶ REPORTABLE BREACH                           │
│                                                              │
│  NOTIFICATION REQUIREMENTS                                   │
│  ┌─────────────────────────────────────────────────────┐     │
│  │ Records  │ Notify       │ Timeline                  │     │
│  │ Affected │              │                           │     │
│  ├──────────┼──────────────┼───────────────────────────┤     │
│  │ < 500    │ Individuals  │ Within 60 days of         │     │
│  │          │ HHS (annual) │ discovery                 │     │
│  ├──────────┼──────────────┼───────────────────────────┤     │
│  │ >= 500   │ Individuals  │ Within 60 days of         │     │
│  │          │ HHS (immed.) │ discovery — no delay      │     │
│  │          │ Media        │                           │     │
│  └──────────┴──────────────┴───────────────────────────┘     │
│                                                              │
│  CODE REQUIREMENTS FOR BREACH SUPPORT                        │
│  □ Can the system identify which records were affected?      │
│    (query: "all patients accessed by user X between dates")  │
│  □ Can the system identify which identifiers were exposed?   │
│    (was it just names, or SSNs too?)                         │
│  □ Is there an accounting of disclosures function?           │
│    (§164.528 — patients can request a log of who accessed    │
│     their PHI in the last 6 years)                           │
│  □ Can breach notifications be generated programmatically?   │
│  □ Are breach events captured with sufficient detail for     │
│    the OCR breach report form?                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 7: De-identification Review

If the system provides de-identified data for analytics or research, verify it meets HIPAA standards.

```
┌──────────────────────────────────────────────────────────────┐
│           DE-IDENTIFICATION REVIEW                           │
│                                                              │
│  SAFE HARBOR METHOD (§164.514(b))                            │
│  Remove ALL 18 identifiers listed above, plus:               │
│  □ The covered entity has no actual knowledge that the       │
│    remaining information could identify an individual         │
│                                                              │
│  CHECK EACH IDENTIFIER REMOVAL:                              │
│   1. □ Names removed (not pseudonymized — fully removed)     │
│   2. □ Geographic data generalized (state only, no city/zip) │
│      → Zip codes: only first 3 digits, and only if           │
│        population > 20,000. Otherwise, set to 000.           │
│   3. □ Dates generalized to year only                        │
│      → No birth dates, admission dates, discharge dates      │
│      → Ages over 89 grouped as "90+"                         │
│   4. □ Phone numbers removed                                 │
│   5. □ Fax numbers removed                                   │
│   6. □ Email addresses removed                               │
│   7. □ SSNs removed                                          │
│   8. □ Medical record numbers removed                        │
│   9. □ Health plan beneficiary numbers removed               │
│  10. □ Account numbers removed                               │
│  11. □ Certificate/license numbers removed                   │
│  12. □ Vehicle identifiers removed                           │
│  13. □ Device identifiers removed                            │
│  14. □ Web URLs removed                                      │
│  15. □ IP addresses removed                                  │
│  16. □ Biometric identifiers removed                         │
│  17. □ Full-face photographs removed                         │
│  18. □ Any other unique identifiers removed                  │
│                                                              │
│  EXPERT DETERMINATION METHOD (§164.514(a))                   │
│  □ Has a qualified statistical expert certified that the     │
│    risk of re-identification is "very small"?                │
│  □ Are the methods and results documented?                   │
│  □ Is the determination reviewed when new data is added?     │
│                                                              │
│  CODE-LEVEL VERIFICATION                                     │
│  → Find the de-identification function/query                 │
│  □ Does it remove ALL 18 identifiers, not just some?         │
│  □ Does it handle edge cases? (PHI in free-text fields,      │
│    embedded in JSON, concatenated in IDs)                    │
│  □ Is re-identification possible via combination of          │
│    remaining fields? (age + gender + zip = identifiable)     │
│  □ Are de-identified datasets marked and tracked separately? │
└──────────────────────────────────────────────────────────────┘
```

---

## Phase 8: HIPAA Compliance Report

### Report Template

```markdown
## HIPAA Compliance Audit Report

### Scope
- System: [application name and version]
- Files audited: [list or "full codebase"]
- Date: [date]
- Auditor: [name, credentials]
- Standards: HIPAA Security Rule (45 CFR §164.302-318),
  HIPAA Privacy Rule (45 CFR §164.500-534), HITECH Act

### Executive Summary
- Critical findings: X (breach risk — immediate remediation)
- High findings: X (HIPAA violation — fix before PHI exposure)
- Medium findings: X (safeguard gap — fix within sprint)
- Low findings: X (best practice — track for next review)

### PHI Inventory
| PHI Type | Storage Location | Encrypted | Access Controlled | Audit Logged |
|----------|-----------------|-----------|-------------------|--------------|
| Names    | patients table  | Column    | Role-based        | Yes          |
| SSN      | patients table  | Field-lvl | Billing only      | Yes          |
| DOB      | patients table  | Column    | Clinical + Billing| Yes          |

### Findings

#### CRITICAL — Breach Risk
1. [§164.xxx] — Short description
   - **Location**: `path/to/file.ts` (line X)
   - **PHI at risk**: [which identifiers]
   - **Impact**: [what an attacker could access]
   - **Remediation**: [exact steps with code guidance]
   - **Status**: [ ] Remediated and verified

#### HIGH — HIPAA Violation
[same format, mapped to §164 section]

#### MEDIUM — Safeguard Gap
[same format]

#### LOW — Best Practice
[same format]

### BAA Status
| Service       | PHI Access | BAA Status | Action Needed |
|---------------|-----------|------------|---------------|
| AWS           | Yes       | Signed     | None          |
| SendGrid      | Maybe     | Pending    | Sign or strip |

### Encryption Status
| Layer         | Standard | Status  | Evidence        |
|---------------|----------|---------|-----------------|
| DB at rest    | AES-256  | Pass    | RDS encryption  |
| Transit       | TLS 1.3  | Pass    | cert config     |
| Field-level   | AES-256  | Partial | SSN only        |

### Audit Trail Status
| Requirement        | Status | Gap                        |
|--------------------|--------|----------------------------|
| PHI read logging   | Pass   | —                          |
| PHI write logging  | Pass   | —                          |
| Log immutability   | Fail   | Logs can be edited by admin|
| 6-year retention   | Pass   | CloudWatch configured      |

### Recommendations
[broader suggestions for improving HIPAA posture]
```

---

## HIPAA Compliance Checklist

Comprehensive checklist mapped to specific HIPAA sections. Use this as the final verification pass.

### Technical Safeguards (§164.312)

| # | Requirement | Section | Status |
|---|------------|---------|--------|
| 1 | Unique user identification for all users | §164.312(a)(2)(i) | [ ] |
| 2 | Emergency access procedure (break-glass) | §164.312(a)(2)(ii) | [ ] |
| 3 | Automatic logoff after inactivity | §164.312(a)(2)(iii) | [ ] |
| 4 | ePHI encrypted at rest (AES-256) | §164.312(a)(2)(iv) | [ ] |
| 5 | Audit logs for all PHI access events | §164.312(b) | [ ] |
| 6 | Audit logs immutable and tamper-evident | §164.312(b) | [ ] |
| 7 | Audit log retention (6+ years) | §164.312(b) | [ ] |
| 8 | Audit logs searchable by patient/user/date | §164.312(b) | [ ] |
| 9 | ePHI integrity validation (checksums/hashes) | §164.312(c)(2) | [ ] |
| 10 | Soft deletes for PHI (no hard delete) | §164.312(c)(2) | [ ] |
| 11 | MFA for PHI access | §164.312(d) | [ ] |
| 12 | Authentication tokens validated (sig, exp) | §164.312(d) | [ ] |
| 13 | TLS 1.2+ on all external connections | §164.312(e)(1) | [ ] |
| 14 | TLS on all internal connections (DB, cache) | §164.312(e)(2)(ii) | [ ] |
| 15 | No PHI in URL query parameters | §164.312(e)(1) | [ ] |
| 16 | Webhook payloads with PHI encrypted/signed | §164.312(e)(1) | [ ] |

### Administrative Safeguards (§164.308)

| # | Requirement | Section | Status |
|---|------------|---------|--------|
| 17 | Formal risk analysis conducted | §164.308(a)(1)(ii)(A) | [ ] |
| 18 | Risk analysis updated on system changes | §164.308(a)(1)(ii)(A) | [ ] |
| 19 | Risk mitigation plan documented | §164.308(a)(1)(ii)(B) | [ ] |
| 20 | Access termination on employee departure | §164.308(a)(3)(ii)(C) | [ ] |
| 21 | Access grants based on job function | §164.308(a)(4)(ii)(B) | [ ] |
| 22 | Access review process exists | §164.308(a)(4)(ii)(C) | [ ] |
| 23 | Password complexity enforced | §164.308(a)(5)(ii)(D) | [ ] |
| 24 | Security incident detection implemented | §164.308(a)(6)(i) | [ ] |
| 25 | Incident response procedure documented | §164.308(a)(6)(ii) | [ ] |
| 26 | Database backups encrypted | §164.308(a)(7)(ii)(A) | [ ] |
| 27 | Backup restoration tested | §164.308(a)(7)(ii)(D) | [ ] |
| 28 | Disaster recovery plan exists | §164.308(a)(7)(ii)(B) | [ ] |

### PHI Protection

| # | Requirement | Section | Status |
|---|------------|---------|--------|
| 29 | No PHI in log output | §164.312(b) + HITECH | [ ] |
| 30 | No PHI in error messages returned to client | §164.312(b) + HITECH | [ ] |
| 31 | No PHI in analytics/tracking events | §164.502(b) | [ ] |
| 32 | No PHI in stack traces or debug output | §164.312(b) + HITECH | [ ] |
| 33 | No PHI in URL paths or query strings | §164.312(e)(1) | [ ] |
| 34 | No PHI in browser localStorage/sessionStorage | §164.312(a)(2)(iv) | [ ] |
| 35 | No PHI in frontend source code or bundles | §164.312(a)(2)(iv) | [ ] |
| 36 | API responses filter PHI by role (min. necessary) | §164.502(b) | [ ] |
| 37 | File names do not contain PHI | §164.312(a)(1) | [ ] |
| 38 | Cache entries with PHI have TTL and encryption | §164.312(a)(2)(iv) | [ ] |

### Business Associate & Organizational

| # | Requirement | Section | Status |
|---|------------|---------|--------|
| 39 | All PHI-touching services have signed BAAs | §164.314(a)(1) | [ ] |
| 40 | BAAs include breach notification requirements | §164.314(a)(2)(i)(C) | [ ] |
| 41 | Subcontractor BAAs in place (chain of custody) | §164.314(a)(2)(i)(B) | [ ] |
| 42 | Error tracking redacts PHI before transmission | §164.502(b) | [ ] |
| 43 | Log aggregation service covered by BAA | §164.314(a)(1) | [ ] |

### Breach Notification

| # | Requirement | Section | Status |
|---|------------|---------|--------|
| 44 | System can identify affected records post-breach | HITECH §13402 | [ ] |
| 45 | System can identify exposed identifier types | HITECH §13402 | [ ] |
| 46 | Accounting of disclosures available (6 years) | §164.528 | [ ] |
| 47 | Breach notification workflow exists | HITECH §13402 | [ ] |
| 48 | Breach risk assessment template available | §164.402 | [ ] |

### De-identification

| # | Requirement | Section | Status |
|---|------------|---------|--------|
| 49 | All 18 identifiers removed (Safe Harbor) | §164.514(b)(2) | [ ] |
| 50 | Zip codes truncated to 3 digits (pop > 20k) | §164.514(b)(2)(i)(B) | [ ] |
| 51 | Ages 90+ grouped | §164.514(b)(2)(i)(C) | [ ] |
| 52 | Dates reduced to year only | §164.514(b)(2)(i)(C) | [ ] |
| 53 | Re-identification risk assessed | §164.514(b)(2)(ii) | [ ] |

---

## Tips for Best Results

1. **Start with the PHI inventory** — you cannot protect what you cannot find. Map every location where PHI exists in the system before checking any safeguard. Most violations come from PHI in places no one realized it existed.

2. **Grep your logs relentlessly** — search production log output for every one of the 18 identifiers. A single patient name in a log file is a reportable breach. Structured loggers are especially dangerous because they serialize entire objects, including PHI fields no one explicitly logged.

3. **Test the encryption chain end-to-end** — it is not enough that the database is encrypted. Verify that PHI is encrypted from the moment it enters the system (TLS in transit) through processing (memory-only, no temp files) to storage (AES-256 at rest) and back out again. One unencrypted hop breaks the entire chain.

4. **Audit the audit trail** — the audit system itself must be audited. Can an admin delete audit logs? Can the application overwrite them? Are they retained for the full 6 years? An incomplete or mutable audit trail is a finding in every OCR investigation.

5. **Check every third-party integration** — if a service can see PHI (even accidentally, such as error tracking capturing a stack trace with a patient name), it needs a BAA. Map every outbound data flow and verify BAA coverage. Missing BAAs are the most common HIPAA violation for software companies.

6. **Think about the breach notification clock** — if something goes wrong, can your system answer these questions within hours: How many records were affected? Which identifiers were exposed? Who was the unauthorized accessor? If not, you are not prepared for a breach, and that itself is a finding.

7. **Minimum necessary is not optional** — every API endpoint, every database query, every report should return only the PHI fields required for the specific function. Returning a full patient record when only the name is needed is a §164.502(b) violation, even if the user is authorized to see all of it.

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
