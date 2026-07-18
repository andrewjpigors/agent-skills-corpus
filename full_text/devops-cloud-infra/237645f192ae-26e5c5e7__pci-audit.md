---
name: pci-audit
description: "Audit code and infrastructure for PCI DSS v4.0 compliance — CDE scoping, tokenization validation, SAQ determination, network segmentation review, encryption checks, access control audit, and logging verification. Use before accepting payments, during payment integration changes, or for annual PCI compliance reviews."
---

# PCI-DSS Audit — Securing Payment Card Data at Every Layer

Audits code, configuration, and infrastructure against all 12 PCI DSS v4.0 requirements. Covers cardholder data environment scoping, tokenization validation, encryption standards, network segmentation, access control, logging, and vulnerability management. Determines the correct SAQ type and identifies scope reduction opportunities through payment processor delegation.

---

## Your Expertise

You are a **Qualified Security Assessor (QSA)** with 20+ years in payment security — from PCI DSS v1.0 through v4.0. You have conducted 75+ PCI assessments across e-commerce, fintech, and payment processor companies handling billions in annual transaction volume. You hold QSA, CISSP, and PA-QSA certifications. You are an expert in:

- PCI DSS v4.0 — all 12 requirements, 78 base requirements, ~400 testing procedures
- Cardholder Data Environment (CDE) — scoping, segmentation, data flow mapping
- Tokenization and encryption — replacing PANs with tokens, P2PE, TLS configuration, key management lifecycle
- SAQ types — SAQ A, A-EP, D — knowing which applies and reducing scope aggressively
- Requirement groups — Build/maintain secure network (1-2), protect cardholder data (3-4), vulnerability management (5-6), access control (7-9), monitoring and testing (10-11), security policy (12)
- PCI scope reduction — using payment processors (Stripe, Adyen, Braintree) to minimize CDE footprint
- Compensating controls — documenting and validating alternatives when a requirement cannot be met directly

You have seen every way card data leaks: debug logs capturing full PANs, developers storing CVVs "temporarily" in Redis, iframes loading payment forms over HTTP, and tokenization implementations that still pass raw card numbers through the merchant server. You know where the bodies are buried.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Payment Integration
<!-- Example: Stripe Elements — PAN never touches our servers, card data entered in Stripe-hosted iframe, only token IDs (tok_xxx, pm_xxx) returned to our backend -->

### CDE Scope
<!-- Example: No CDE — fully tokenized via Stripe, only Stripe customer IDs and payment method tokens stored in our database. No PAN, CVV, expiry, or track data anywhere in our systems -->

### SAQ Type
<!-- Example: SAQ A — all payment page fields hosted by Stripe (Elements/Checkout), no card data transmitted through our servers, payment page served over TLS -->

### Encryption Standards
<!-- Example: TLS 1.3 for all payment pages, HSTS enabled with 1-year max-age, no mixed content on checkout flows. No card data stored so AES-256-at-rest not applicable -->

### Network Segmentation
<!-- Example: Payment webhook handler runs in isolated ECS service in private subnet, separate security group allowing only Stripe IP ranges on webhook port. No direct internet access from payment service -->

### Compliance Level
<!-- Example: Level 4 merchant — fewer than 20,000 e-commerce transactions per year. SAQ + quarterly ASV scan required. No on-site QSA assessment needed -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│           MANDATORY RULES FOR EVERY PCI AUDIT                │
│                                                              │
│  1. NEVER STORE WHAT YOU DON'T NEED                          │
│     → Full PAN, CVV, PIN, magnetic stripe data must NEVER    │
│       be stored after authorization. Period.                 │
│     → If Stripe/Adyen handles payment, you should never see  │
│       card data in your systems — not in logs, not in DB,    │
│       not in temp files, not in error messages               │
│     → "We only store it for a few seconds" is not a valid   │
│       excuse — it puts you in full PCI scope                 │
│     → PCI DSS Req 3                                          │
│                                                              │
│  2. TOKENIZE, DON'T ENCRYPT CARD DATA                        │
│     → If you must handle card numbers, tokenize them         │
│       immediately via your payment processor                 │
│     → Encryption of card data puts you in FULL PCI scope —   │
│       you become responsible for key management, rotation,   │
│       split knowledge, dual control                          │
│     → Tokenization keeps you at SAQ A — the processor owns   │
│       the card data, you only hold meaningless tokens        │
│     → PCI DSS Req 3.4, 3.5                                   │
│                                                              │
│  3. EVERY PAYMENT PAGE MUST BE TLS 1.2+                      │
│     → No mixed content, no HTTP fallbacks, no self-signed    │
│       certs on any page that loads payment forms             │
│     → HSTS headers mandatory on all payment-related domains  │
│     → TLS 1.0 and 1.1 are explicitly prohibited by PCI v4.0 │
│     → PCI DSS Req 4.2.1                                      │
│                                                              │
│  4. LOG EVERY ACCESS TO PAYMENT SYSTEMS                      │
│     → Every login, every query, every admin action on any    │
│       system that touches payment data or tokens             │
│     → Logs retained 12 months minimum, 3 months immediately  │
│       available for analysis                                 │
│     → Logs must be tamper-evident — write to append-only     │
│       storage or centralized SIEM                            │
│     → PCI DSS Req 10.1, 10.2, 10.3, 10.7                    │
│                                                              │
│  5. SEGMENT YOUR NETWORK                                     │
│     → Payment systems must be isolated from general-purpose  │
│       servers — separate VPC/subnet/security group           │
│     → If an attacker compromises your blog server, they must │
│       NOT be able to reach your payment service              │
│     → Flat networks with everything in one subnet are an     │
│       automatic PCI failure                                  │
│     → PCI DSS Req 1.3, 1.4                                   │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in audit reports, findings, or          │
│       compliance documentation                               │
│     → All output reads as if written by a QSA assessor       │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Before integrating a payment processor (Stripe, Adyen, Braintree, Square)
- After modifying checkout pages, payment forms, or billing flows
- When adding or changing webhook handlers for payment events
- During annual PCI compliance review (SAQ self-assessment)
- Before quarterly ASV (Approved Scanning Vendor) external scan
- When migrating payment infrastructure (new processor, new hosting, new architecture)
- After a security incident involving payment-adjacent systems
- When onboarding a new payment method (Apple Pay, Google Pay, ACH, BNPL)
- When changing network architecture that touches payment services

---

## How It Works

```
┌──────────────────────────────────────────────────────────────────────┐
│                     PCI-DSS AUDIT FLOW                               │
│                                                                      │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│  │  PHASE 1  │  │  PHASE 2  │  │  PHASE 3  │  │  PHASE 4  │        │
│  │  Scope &  │─▶│  Network  │─▶│  Data     │─▶│  Access   │        │
│  │  SAQ      │  │  & Config │  │  Protect  │  │  Control  │        │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │
│   CDE scope      Firewalls      Encryption     Need-to-know        │
│   Data flow      Segmentation   Tokenization   Auth strength        │
│   SAQ type       Hardening      Key mgmt       Physical (if any)   │
│       │                                                              │
│       ▼                                                              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐        │
│  │  PHASE 5  │  │  PHASE 6  │  │  PHASE 7  │  │  PHASE 8  │        │
│  │  Vuln     │─▶│  Monitor  │─▶│  Policy   │─▶│  Report   │        │
│  │  Mgmt     │  │  & Test   │  │  Review   │  │  & Attest │        │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘        │
│   Patching       Logging        Sec policy     Findings +           │
│   Malware        IDS/IPS        Risk assess    SAQ status +         │
│   Secure dev     Pen test       Awareness      Remediation          │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │          PCI DSS v4.0 — 12 REQUIREMENTS                     │    │
│  │                                                              │    │
│  │  NETWORK (1-2)  DATA (3-4)  VULN (5-6)  ACCESS (7-9)       │    │
│  │  MONITOR (10-11)  POLICY (12)                                │    │
│  │                                                              │    │
│  │  78 base requirements  ~400 testing procedures               │    │
│  │  Scope determines which apply to YOUR environment            │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: CDE Scoping and SAQ Determination

The most critical phase. Incorrect scoping means auditing the wrong things — or missing what matters entirely.

### Cardholder Data Flow Mapping

Trace every path card data could take through your systems.

```
┌──────────────────────────────────────────────────────────────────────┐
│           TOKENIZED PAYMENT FLOW (SCOPE REDUCTION)                   │
│                                                                      │
│  ┌──────────┐   Card data    ┌──────────────┐   Token    ┌────────┐ │
│  │ Customer │ ──────────────▶│   Stripe /   │ ─────────▶│  Your  │ │
│  │ Browser  │   (iframe /    │   Adyen /    │  (tok_xx)  │ Server │ │
│  │          │    hosted)     │   Processor  │            │        │ │
│  └──────────┘                └──────────────┘            └────────┘ │
│       │                           │                          │      │
│       │                           │                          │      │
│       │  Card data NEVER          │  Processor stores        │      │
│       │  touches your server      │  card data (their CDE)   │      │
│       │                           │                          │      │
│       │                           ▼                          ▼      │
│       │                    ┌──────────────┐         ┌────────────┐  │
│       │                    │  PCI Level 1 │         │ Your DB    │  │
│       │                    │  (Processor) │         │ Stores:    │  │
│       │                    │  Stores PAN  │         │ - token ID │  │
│       │                    │  in vault    │         │ - cust ID  │  │
│       │                    └──────────────┘         │ - last 4   │  │
│       │                                             │ - NO PAN   │  │
│       │     YOUR SCOPE: SAQ A                       │ - NO CVV   │  │
│       │     No CDE in your environment              └────────────┘  │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────── │
│                                                                      │
│           DIRECT CARD HANDLING FLOW (FULL SCOPE)                     │
│                                                                      │
│  ┌──────────┐   Card data    ┌──────────┐   Card data  ┌──────────┐│
│  │ Customer │ ──────────────▶│   Your   │ ────────────▶│ Payment  ││
│  │ Browser  │   (your form)  │  Server  │  (API call)  │ Gateway  ││
│  │          │                │   !!!    │              │          ││
│  └──────────┘                └──────────┘              └──────────┘│
│                                   │                                 │
│              YOUR SERVER IS NOW CDE — FULL PCI SCOPE               │
│              SAQ D: 300+ requirements, annual pen test             │
│              Key management, encryption, segmentation              │
│              Logging, monitoring, vulnerability scanning            │
└──────────────────────────────────────────────────────────────────────┘
```

### SAQ Decision Tree

Determine which Self-Assessment Questionnaire applies.

```
┌──────────────────────────────────────────────────────────────────────┐
│                   SAQ DETERMINATION DECISION TREE                    │
│                                                                      │
│  Does your server EVER receive, process, or store cardholder data?   │
│                                                                      │
│  ┌─── YES ──────────────────────────────────────────────────────┐    │
│  │                                                              │    │
│  │  Do you store card data after authorization?                 │    │
│  │  ├── YES → STOP. You are storing prohibited data.           │    │
│  │  │         CVV/PIN must NEVER be stored post-auth.          │    │
│  │  │         Full PAN storage requires SAQ D + encryption.    │    │
│  │  │                                                          │    │
│  │  └── NO → SAQ D (full assessment)                           │    │
│  │           → 300+ questions                                  │    │
│  │           → Annual penetration test required                │    │
│  │           → Quarterly internal + external vulnerability scan│    │
│  │           → Network segmentation mandatory                  │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌─── NO ───────────────────────────────────────────────────────┐    │
│  │                                                              │    │
│  │  Does your website INFLUENCE the payment page?               │    │
│  │  (Do you serve JavaScript that runs on the payment page?     │    │
│  │   Do you host the page that contains the payment iframe?)    │    │
│  │                                                              │    │
│  │  ├── YES → SAQ A-EP (e-commerce with partial outsourcing)  │    │
│  │  │         → ~140 questions                                 │    │
│  │  │         → Quarterly ASV scan required                    │    │
│  │  │         → Vulnerability management required              │    │
│  │  │         → Your web server is in scope                    │    │
│  │  │                                                          │    │
│  │  └── NO → Does the processor provide the ENTIRE payment    │    │
│  │            page? (redirect or hosted payment page)           │    │
│  │                                                              │    │
│  │           ├── YES → SAQ A (fully outsourced)                │    │
│  │           │         → ~30 questions                         │    │
│  │           │         → Minimal scope                         │    │
│  │           │         → Easiest compliance path               │    │
│  │           │                                                  │    │
│  │           └── NO  → SAQ A-EP                                │    │
│  └──────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  COMMON MAPPING:                                                     │
│  ┌──────────────────────────┬──────────┬────────────────────────┐    │
│  │ Integration Type         │ SAQ Type │ Scope                  │    │
│  ├──────────────────────────┼──────────┼────────────────────────┤    │
│  │ Stripe Checkout (hosted) │ SAQ A    │ Minimal                │    │
│  │ Stripe Elements (iframe) │ SAQ A-EP │ Web server in scope    │    │
│  │ Stripe.js + own form     │ SAQ A-EP │ Web server in scope    │    │
│  │ Direct API (card in body)│ SAQ D    │ Full CDE scope         │    │
│  │ PayPal redirect          │ SAQ A    │ Minimal                │    │
│  │ Adyen Drop-in            │ SAQ A-EP │ Web server in scope    │    │
│  │ Braintree Hosted Fields  │ SAQ A-EP │ Web server in scope    │    │
│  │ Square Web Payments SDK  │ SAQ A-EP │ Web server in scope    │    │
│  └──────────────────────────┴──────────┴────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

### CDE Scoping Checklist

```
SCOPING — WHAT IS IN YOUR CDE?

□ List every system that stores, processes, or transmits cardholder data
□ List every system that is connected to the CDE (even if it doesn't touch card data)
□ List every person with access to CDE systems
□ Map every network segment that can reach CDE systems

CARDHOLDER DATA ELEMENTS:
  IN SCOPE if stored:        NEVER STORE after auth:
  ├── Primary Account Number  ├── CVV / CVC / CID
  ├── Cardholder Name         ├── PIN / PIN block
  ├── Expiration Date         └── Full magnetic stripe
  └── Service Code

SCOPE REDUCTION AUDIT:
□ Is payment processing fully outsourced to a PCI-compliant processor?
□ Does your server ever receive raw card numbers? (check API routes)
□ Do payment form fields exist in YOUR HTML? (or in processor iframe?)
□ Does your JavaScript touch card input fields? (check event listeners)
□ Do server logs ever contain card numbers? (even partial)
□ Do error tracking services (Sentry, etc.) capture card data in payloads?
□ Do database columns exist for PAN, CVV, or track data?
□ Do Redis/cache keys ever hold card data, even temporarily?
```

---

## Phase 2: Network Security (Requirements 1-2)

Install and maintain network security controls. Remove vendor defaults.

```
┌──────────────────────────────────────────────────────────────────────┐
│  REQ 1: INSTALL AND MAINTAIN NETWORK SECURITY CONTROLS              │
│                                                                      │
│  FIREWALL / SECURITY GROUP REVIEW                                    │
│  □ Are inbound rules limited to required ports only?                │
│  □ Are default "allow all" rules removed?                           │
│  □ Is there a deny-all default policy?                              │
│  □ Are payment service ports restricted to known IP ranges?         │
│    (e.g., only Stripe webhook IPs can reach webhook endpoint)       │
│  □ Is outbound traffic restricted? (no unrestricted egress)         │
│  □ Are firewall rules documented and reviewed quarterly?            │
│                                                                      │
│  NETWORK SEGMENTATION                                                │
│  □ Is the payment service in an isolated subnet/VPC?                │
│  □ Can non-payment services reach the payment service directly?     │
│  □ Is there a DMZ between internet-facing and internal systems?     │
│  □ Are database servers in private subnets (no public IP)?          │
│  □ Is segmentation validated by penetration testing?                │
│                                                                      │
│  WIRELESS (if applicable)                                            │
│  □ Are wireless networks segmented from the CDE?                    │
│  □ Is WPA2/WPA3 with AES encryption used?                          │
│  □ Are default wireless passwords changed?                          │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  REQ 2: APPLY SECURE CONFIGURATIONS                                  │
│                                                                      │
│  DEFAULT CREDENTIALS                                                 │
│  □ Are all vendor default passwords changed?                        │
│    → Database admin, Redis, message queues, dashboards              │
│  □ Are default accounts disabled or removed?                        │
│  □ Are SNMP community strings changed from "public"/"private"?      │
│                                                                      │
│  SYSTEM HARDENING                                                    │
│  □ Are unnecessary services disabled on all servers?                │
│  □ Are unnecessary ports closed?                                    │
│  □ Are system packages up to date?                                  │
│  □ Is SSH key-based only? (no password auth for servers)            │
│  □ Are Docker images using minimal base images? (alpine/distroless) │
│  □ Are container privileges restricted? (no --privileged flag)      │
│                                                                      │
│  TLS CONFIGURATION                                                   │
│  □ TLS 1.2 minimum? (TLS 1.0 and 1.1 are prohibited in PCI v4.0)  │
│  □ Strong cipher suites only? (no RC4, DES, 3DES, NULL ciphers)    │
│  □ HSTS enabled with min 1-year max-age?                            │
│  □ Certificate valid and not self-signed in production?             │
│  □ Certificate chain complete?                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 3: Cardholder Data Protection (Requirements 3-4)

Protect stored data. Encrypt data in transit.

```
┌──────────────────────────────────────────────────────────────────────┐
│  REQ 3: PROTECT STORED ACCOUNT DATA                                  │
│                                                                      │
│  PROHIBITED DATA — MUST NOT EXIST ANYWHERE POST-AUTH                 │
│  □ Search entire codebase for CVV/CVC storage:                      │
│    grep -ri "cvv\|cvc\|cvv2\|cid\|security.code" src/              │
│  □ Search for PIN storage:                                          │
│    grep -ri "pin.block\|pin.value\|card.pin" src/                   │
│  □ Search for track data storage:                                   │
│    grep -ri "track1\|track2\|magnetic.stripe" src/                  │
│  □ Check database schema for prohibited columns:                    │
│    grep -i "cvv\|cvc\|pin\|track\|stripe_data" schema.prisma       │
│                                                                      │
│  PAN HANDLING                                                        │
│  □ If PAN is stored, is it rendered unreadable?                     │
│    → Tokenization (preferred — removes PAN from your scope)         │
│    → Strong one-way hash (SHA-256 with salt, keyed HMAC)            │
│    → Truncation (first 6 + last 4 digits max)                      │
│    → AES-256 encryption with proper key management                  │
│  □ If PAN is displayed, is it masked? (show only last 4)            │
│  □ Is PAN display limited to need-to-know roles?                    │
│                                                                      │
│  KEY MANAGEMENT (if encrypting card data)                            │
│  □ Are encryption keys stored separately from encrypted data?       │
│  □ Is there a documented key rotation procedure?                    │
│  □ Are keys protected by split knowledge / dual control?            │
│  □ Is there a key custodian list with signed agreements?            │
│  □ Is key retirement/replacement documented?                        │
│                                                                      │
│  DATA RETENTION                                                      │
│  □ Is there a documented data retention policy?                     │
│  □ Is cardholder data purged when no longer needed?                 │
│  □ Is there an automated process to delete expired data?            │
│  □ Are quarterly reviews conducted to verify no unnecessary data?   │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  REQ 4: PROTECT DATA IN TRANSIT                                      │
│                                                                      │
│  ENCRYPTION IN TRANSIT                                               │
│  □ All payment pages served over HTTPS?                             │
│  □ No mixed content on pages with payment forms?                    │
│    (check for http:// resources loaded on https:// pages)           │
│  □ TLS 1.2+ enforced? (check server config, not just availability) │
│  □ Strong cipher suites only?                                       │
│  □ PAN never sent over SMS, email, or chat?                        │
│  □ Webhook endpoints use HTTPS?                                     │
│  □ Internal service-to-service communication encrypted?             │
│    (mTLS or TLS for services in the CDE)                            │
│                                                                      │
│  CERTIFICATE MANAGEMENT                                              │
│  □ Certificates from trusted CA? (not self-signed in production)    │
│  □ Certificates not expired?                                        │
│  □ Auto-renewal configured? (Let's Encrypt / ACM)                   │
│  □ Certificate pinning considered for mobile apps?                  │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 4: Vulnerability Management (Requirements 5-6)

Protect systems against malware. Develop and maintain secure systems.

```
┌──────────────────────────────────────────────────────────────────────┐
│  REQ 5: PROTECT AGAINST MALWARE                                      │
│                                                                      │
│  □ Anti-malware deployed on all systems in CDE?                     │
│  □ Anti-malware signatures current and auto-updating?               │
│  □ Periodic scans configured? (not just real-time)                  │
│  □ Anti-malware logs retained and monitored?                        │
│  □ Users cannot disable anti-malware? (admin-only control)          │
│  □ Container images scanned for malware/vulnerabilities?            │
│                                                                      │
│  NOTE: For containerized environments, image scanning               │
│  (Trivy, Snyk Container) satisfies much of Req 5.                  │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  REQ 6: DEVELOP AND MAINTAIN SECURE SYSTEMS                          │
│                                                                      │
│  PATCH MANAGEMENT                                                    │
│  □ Critical security patches applied within 30 days?                │
│  □ Non-critical patches applied within defined timeline?            │
│  □ OS, application, and library patches all tracked?                │
│  □ Automated dependency scanning in CI pipeline?                    │
│    npm audit / Dependabot / Snyk                                    │
│  □ Container base images updated regularly?                         │
│                                                                      │
│  SECURE DEVELOPMENT                                                  │
│  □ Developers trained on secure coding practices?                   │
│  □ Code review required before merge? (focus on security)           │
│  □ Input validation on all user-controlled data?                    │
│  □ Output encoding to prevent injection?                            │
│  □ Parameterized queries for all database access?                   │
│  □ No use of known-vulnerable functions/libraries?                  │
│  □ Secrets management — no hardcoded credentials?                   │
│                                                                      │
│  CHANGE MANAGEMENT                                                   │
│  □ All changes to CDE systems go through change control?            │
│  □ Changes tested in non-production before deployment?              │
│  □ Rollback procedures documented?                                  │
│  □ Impact assessment performed for CDE changes?                     │
│                                                                      │
│  WEB APPLICATION SECURITY (v4.0 — Req 6.4.2, 6.4.3)                │
│  □ Payment page scripts inventoried and authorized?                 │
│  □ Content Security Policy (CSP) headers configured?                │
│  □ Subresource Integrity (SRI) on external scripts?                 │
│  □ Script changes monitored and alerted?                            │
│  □ WAF or equivalent protecting public-facing web apps?             │
│                                                                      │
│  PCI v4.0 NEW — Req 6.4.3 (mandatory March 2025):                  │
│  All payment page scripts must be:                                   │
│  1. Authorized via documented inventory                              │
│  2. Integrity-verified (CSP + SRI or equivalent)                     │
│  3. Justified with business/technical reason                         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 5: Access Control (Requirements 7-9)

Restrict access by business need. Identify and authenticate users. Restrict physical access.

```
┌──────────────────────────────────────────────────────────────────────┐
│  REQ 7: RESTRICT ACCESS BY BUSINESS NEED-TO-KNOW                    │
│                                                                      │
│  □ Access to CDE limited to personnel with documented business need?│
│  □ Role-based access control (RBAC) implemented?                    │
│  □ Default deny — users start with no access?                       │
│  □ Access rights reviewed at least every 6 months?                  │
│  □ Terminated employees removed within 24 hours?                    │
│  □ Service accounts have minimal required privileges?               │
│  □ Database access restricted to application service accounts?      │
│    (no shared admin credentials)                                    │
│                                                                      │
│  CODE REVIEW — ACCESS CHECKS                                        │
│  □ Every payment-related API endpoint has auth middleware?           │
│  □ Every endpoint checks user role/permission?                      │
│  □ Admin endpoints restricted to admin roles?                       │
│  □ Tenant isolation enforced on every query?                        │
│  □ API keys / service tokens scoped to minimum permissions?         │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  REQ 8: IDENTIFY USERS AND AUTHENTICATE ACCESS                       │
│                                                                      │
│  UNIQUE IDENTIFICATION                                               │
│  □ Every user has a unique ID? (no shared accounts)                 │
│  □ Group/shared accounts documented and approved?                   │
│  □ Service accounts traceable to responsible individual?            │
│                                                                      │
│  AUTHENTICATION STRENGTH                                             │
│  □ Passwords minimum 12 characters? (v4.0 requirement)             │
│  □ Passwords contain numeric AND alphabetic characters?             │
│  □ Password history — cannot reuse last 4 passwords?               │
│  □ Account lockout after max 10 failed attempts?                    │
│  □ Lockout duration minimum 30 minutes or until admin unlock?       │
│  □ Session timeout after 15 minutes of inactivity?                  │
│                                                                      │
│  MULTI-FACTOR AUTHENTICATION                                         │
│  □ MFA required for all administrative access to CDE?              │
│  □ MFA required for all remote access to CDE?                      │
│  □ MFA uses two DIFFERENT factor types?                             │
│    (something you know + something you have/are)                    │
│                                                                      │
│  PCI v4.0 NEW — Req 8.3.6 (mandatory March 2025):                  │
│  Minimum password length increases to 12 characters.                 │
│  MFA required for ALL access to CDE, not just remote/admin.         │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  REQ 9: RESTRICT PHYSICAL ACCESS (if applicable)                     │
│                                                                      │
│  For cloud-hosted environments:                                      │
│  □ Cloud provider is PCI DSS compliant? (AWS, GCP, Azure — yes)    │
│  □ Physical security inherited from provider?                       │
│  □ Documented in your compliance artifacts?                         │
│                                                                      │
│  For on-premise or colo:                                             │
│  □ Data center access controlled by badge/biometric?                │
│  □ Visitor logs maintained?                                         │
│  □ Media destruction procedures documented?                         │
│  □ POS devices (if any) inspected for tampering?                    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 6: Monitoring and Testing (Requirements 10-11)

Log and monitor all access. Regularly test security.

```
┌──────────────────────────────────────────────────────────────────────┐
│  REQ 10: LOG AND MONITOR ALL ACCESS TO SYSTEM COMPONENTS             │
│                                                                      │
│  WHAT MUST BE LOGGED                                                 │
│  □ All individual user access to cardholder data                    │
│  □ All actions taken by anyone with root/admin privileges           │
│  □ Access to all audit trails                                       │
│  □ Invalid logical access attempts                                  │
│  □ Use of identification and authentication mechanisms              │
│  □ Initialization, stopping, or pausing of audit logs               │
│  □ Creation and deletion of system-level objects                    │
│                                                                      │
│  LOG CONTENT — EACH ENTRY MUST INCLUDE                               │
│  □ User identification (who)                                        │
│  □ Type of event (what)                                             │
│  □ Date and time (when)                                             │
│  □ Success or failure indication (outcome)                          │
│  □ Origination of event (where — IP, system)                       │
│  □ Identity or name of affected data/resource (target)              │
│                                                                      │
│  LOG PROTECTION                                                      │
│  □ Audit trails cannot be altered? (append-only, centralized)       │
│  □ Logs stored in a separate, restricted system?                    │
│  □ Log integrity verified? (checksums, WORM storage, SIEM)         │
│  □ Logs reviewed daily for suspicious activity?                     │
│                                                                      │
│  LOG RETENTION                                                       │
│  □ Minimum 12 months of audit trail history?                        │
│  □ At least 3 months immediately available for analysis?            │
│  □ Remaining 9 months restorable from backup within reasonable time?│
│                                                                      │
│  CODE REVIEW — LOGGING                                               │
│  □ Payment webhook handlers log all events?                         │
│  □ Authentication events logged? (login, logout, failure)           │
│  □ Authorization failures logged? (forbidden access attempts)       │
│  □ Logs do NOT contain card data?                                   │
│    grep -ri "card.number\|pan\|full.card" src/ | grep -i "log"     │
│  □ Logs do NOT contain CVV, PIN, or passwords?                      │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  REQ 11: TEST SECURITY OF SYSTEMS AND NETWORKS REGULARLY             │
│                                                                      │
│  VULNERABILITY SCANNING                                              │
│  □ Quarterly internal vulnerability scans?                          │
│  □ Quarterly external ASV (Approved Scanning Vendor) scans?         │
│  □ Scans after significant infrastructure changes?                  │
│  □ All high-severity findings remediated and re-scanned?            │
│                                                                      │
│  PENETRATION TESTING                                                 │
│  □ Annual penetration test of CDE? (SAQ D, some SAQ A-EP)          │
│  □ Both network-layer and application-layer testing?                │
│  □ Testing from inside and outside the CDE network?                 │
│  □ Segmentation controls tested by pen test?                        │
│  □ Findings remediated and re-tested?                               │
│                                                                      │
│  CHANGE DETECTION                                                    │
│  □ File integrity monitoring (FIM) on critical system files?        │
│  □ FIM alerts reviewed and investigated?                            │
│  □ Payment page script monitoring in place? (Req 11.6.1)           │
│                                                                      │
│  WIRELESS SCANNING (if applicable)                                   │
│  □ Quarterly wireless access point scans?                           │
│  □ Unauthorized wireless APs investigated and removed?              │
│                                                                      │
│  PCI v4.0 NEW — Req 11.6.1 (mandatory March 2025):                 │
│  Deploy a change-and-tamper detection mechanism for payment pages.   │
│  Monitor HTTP headers and script content for unauthorized changes.   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Phase 7: Security Policy (Requirement 12)

Maintain a policy that addresses information security.

```
┌──────────────────────────────────────────────────────────────────────┐
│  REQ 12: SUPPORT INFORMATION SECURITY WITH POLICIES AND PROGRAMS     │
│                                                                      │
│  SECURITY POLICY                                                     │
│  □ Written information security policy exists?                      │
│  □ Policy reviewed annually and updated when environment changes?   │
│  □ Policy disseminated to all relevant personnel?                   │
│  □ Policy addresses all 12 PCI DSS requirements?                    │
│                                                                      │
│  RISK ASSESSMENT                                                     │
│  □ Annual formal risk assessment performed?                         │
│  □ Risk assessment identifies critical assets and threats?          │
│  □ Risk assessment results used to update security controls?        │
│                                                                      │
│  SECURITY AWARENESS                                                  │
│  □ Security awareness training for all personnel upon hire?         │
│  □ Annual refresher training?                                       │
│  □ Training covers cardholder data handling procedures?             │
│  □ Personnel acknowledge the security policy? (signed)              │
│                                                                      │
│  INCIDENT RESPONSE                                                   │
│  □ Documented incident response plan exists?                        │
│  □ Plan tested at least annually? (tabletop or simulation)          │
│  □ Specific roles and responsibilities defined?                     │
│  □ Contact information for payment brands (Visa, MC) documented?   │
│  □ Plan covers: detection, containment, eradication, recovery,     │
│    notification, lessons learned                                    │
│  □ Plan addresses data breach notification requirements?            │
│                                                                      │
│  THIRD-PARTY MANAGEMENT                                              │
│  □ All third-party service providers with CDE access identified?    │
│  □ Providers acknowledge their PCI DSS responsibilities?            │
│  □ Provider PCI compliance status verified? (AOC or SAQ)            │
│  □ Process to monitor provider compliance annually?                 │
│                                                                      │
│  PCI v4.0 NEW — Req 12.3.1:                                         │
│  Targeted risk analysis required for each PCI requirement where     │
│  the entity has flexibility in how frequently it performs an         │
│  activity (e.g., log reviews, password changes).                    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Common PCI Failures

Issues found in the majority of PCI assessments. Check these first.

```
┌──────────────────────────────────────────────────────────────────────┐
│  TOP PCI FAILURES FOUND IN REAL ASSESSMENTS                          │
│                                                                      │
│  #  │ Finding                      │ Req │ Why It Happens            │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  1  │ Card data in application     │  3  │ Debug logging enabled in │
│     │ or server logs               │     │ production captures full │
│     │                              │     │ request bodies with PAN  │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  2  │ TLS 1.0/1.1 still enabled   │  4  │ Legacy compatibility     │
│     │ on payment endpoints         │     │ settings never removed   │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  3  │ No network segmentation —   │  1  │ "Flat network" — single  │
│     │ payment service reachable    │     │ VPC/subnet for all       │
│     │ from all internal systems    │     │ services                 │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  4  │ Default database passwords  │  2  │ PostgreSQL/Redis shipped │
│     │ unchanged                    │     │ with no password or      │
│     │                              │     │ default credentials      │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  5  │ CVV stored in database      │  3  │ Developer stored "temp"  │
│     │ column after authorization   │     │ for debugging, never     │
│     │                              │     │ removed the column       │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  6  │ Shared admin accounts for   │  8  │ Team shares one SSH key  │
│     │ server/database access       │     │ or DB password           │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  7  │ Audit logs not retained     │ 10  │ Logs rotated after 30    │
│     │ for 12 months               │     │ days, no archive to S3   │
│     │                              │     │ or log aggregator        │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  8  │ No quarterly vulnerability  │ 11  │ Company never scheduled  │
│     │ scans                        │     │ ASV scans or internal    │
│     │                              │     │ scanning                 │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  9  │ Missing MFA on admin access │  8  │ SSH/console access to    │
│     │ to CDE systems              │     │ payment servers without  │
│     │                              │     │ second factor            │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  10 │ No incident response plan   │ 12  │ Company never wrote one  │
│     │ or plan never tested         │     │ or wrote it 3 years ago │
│     │                              │     │ and never tested it      │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  11 │ Payment page scripts not    │  6  │ Third-party analytics,   │
│     │ inventoried (v4.0 new)      │     │ chat widgets, A/B test   │
│     │                              │     │ scripts not documented   │
│  ───┼──────────────────────────────┼─────┼──────────────────────────│
│  12 │ Passwords under 12 chars    │  8  │ Policy says 8 chars but  │
│     │ (v4.0 new requirement)      │     │ v4.0 requires 12 as of  │
│     │                              │     │ March 2025               │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Scope Reduction Strategies

How to minimize your PCI burden using payment processors.

```
┌──────────────────────────────────────────────────────────────────────┐
│             SCOPE REDUCTION — PRACTICAL GUIDE                        │
│                                                                      │
│  STRATEGY 1: HOSTED PAYMENT PAGE (SAQ A)                             │
│                                                                      │
│  Use Stripe Checkout, PayPal redirect, or equivalent:                │
│  → Customer redirected to processor's domain for payment             │
│  → Card data never touches your servers or pages                     │
│  → Minimal PCI scope — ~30 questions                                 │
│  → No quarterly ASV scan required (depends on brand)                 │
│                                                                      │
│  VERIFICATION STEPS:                                                 │
│  □ Payment form URL is on processor's domain?                       │
│  □ No JavaScript on your site interacts with card fields?           │
│  □ Return/callback URL only receives token/session ID?              │
│  □ No card data in URL parameters on redirect back?                 │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  STRATEGY 2: IFRAME / HOSTED FIELDS (SAQ A-EP)                       │
│                                                                      │
│  Use Stripe Elements, Braintree Hosted Fields, Adyen Drop-in:        │
│  → Card fields rendered in processor's iframe                        │
│  → Your page hosts the iframe but never touches card data            │
│  → Web server is in scope (serves the page containing iframe)        │
│  → ~140 questions, quarterly ASV scan required                       │
│                                                                      │
│  VERIFICATION STEPS:                                                 │
│  □ Card input fields are inside processor's iframe?                 │
│    (inspect DOM — input should be in cross-origin iframe)           │
│  □ No JavaScript on your page reads card field values?              │
│  □ No custom event listeners on card input fields?                  │
│  □ CSP headers restrict script sources?                             │
│  □ SRI attributes on external scripts?                              │
│  □ Page served over TLS with no mixed content?                      │
│                                                                      │
│  ──────────────────────────────────────────────────────────────────  │
│                                                                      │
│  STRATEGY 3: TOKENIZATION AT THE EDGE                                │
│                                                                      │
│  If you must collect card data (rare for SaaS):                      │
│  → Tokenize at the browser/POS before data reaches your server      │
│  → Use payment processor's client-side SDK                           │
│  → Token is useless without processor's decryption key               │
│  → Only the token traverses your network                             │
│                                                                      │
│  CODE AUDIT:                                                         │
│  □ Client-side SDK creates token before form submission?            │
│  □ Server receives only token ID, never raw card number?            │
│  □ Server-side code never constructs card number objects?           │
│    grep -ri "card.number\|cardNumber\|card_number" src/backend/     │
│  □ API routes never accept card number as a field?                  │
│    grep -ri "pan\|card.num\|account.number" src/backend/routes/     │
│  □ Database schema has no column for raw card numbers?              │
│    grep -i "card_number\|pan\|account_number" schema.prisma         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## PCI Compliance Checklist

Full checklist mapped to requirements. Use this for SAQ completion and audit preparation.

```
REQUIREMENT 1 — NETWORK SECURITY CONTROLS
□ 1.1  Documented network security control policies and procedures
□ 1.2  Network security controls configured and maintained
□ 1.3  Network access to and from CDE is restricted
□ 1.4  Network connections between trusted and untrusted networks controlled
□ 1.5  Risks to CDE from other connected networks mitigated

REQUIREMENT 2 — SECURE CONFIGURATIONS
□ 2.1  Secure configuration policies documented
□ 2.2  System components configured securely (vendor defaults removed)
□ 2.3  Wireless environments (if any) configured securely

REQUIREMENT 3 — PROTECT STORED ACCOUNT DATA
□ 3.1  Account data storage policies documented, minimized
□ 3.2  Sensitive authentication data NOT stored after authorization
□ 3.3  PAN access limited to business need-to-know, masked when displayed
□ 3.4  PAN rendered unreadable (tokenization, hashing, encryption)
□ 3.5  Encryption keys for PAN protection managed securely
□ 3.6  Cryptographic key management procedures documented
□ 3.7  Policies for PAN storage duration and secure deletion

REQUIREMENT 4 — ENCRYPT DATA IN TRANSIT
□ 4.1  Strong cryptography policies documented
□ 4.2  PAN protected with strong cryptography during transmission
       → TLS 1.2+ on all payment pages and API endpoints

REQUIREMENT 5 — MALWARE PROTECTION
□ 5.1  Anti-malware policies documented
□ 5.2  Malware detected and addressed (anti-malware deployed)
□ 5.3  Anti-malware mechanisms active, maintained, monitored
□ 5.4  Anti-phishing mechanisms protect against phishing attacks

REQUIREMENT 6 — SECURE DEVELOPMENT
□ 6.1  Secure development policies documented
□ 6.2  Custom software developed securely
□ 6.3  Security vulnerabilities identified and addressed (patching)
□ 6.4  Public-facing web apps protected (WAF/CSP/SRI)
□ 6.5  Changes managed securely (change control procedures)

REQUIREMENT 7 — ACCESS RESTRICTION
□ 7.1  Need-to-know access policies documented
□ 7.2  Access to system components restricted by role
□ 7.3  Access control system in place and enforced

REQUIREMENT 8 — USER IDENTIFICATION
□ 8.1  User identification and authentication policies documented
□ 8.2  Unique IDs assigned to all users (no shared accounts)
□ 8.3  Strong authentication enforced (12+ char passwords in v4.0)
□ 8.4  MFA implemented for all CDE access
□ 8.5  MFA systems configured to prevent misuse
□ 8.6  Application and system accounts managed securely

REQUIREMENT 9 — PHYSICAL ACCESS RESTRICTION
□ 9.1  Physical access policies documented
□ 9.2  Physical access controls manage entry to CDE facilities
□ 9.3  Physical access for personnel and visitors authorized/managed
□ 9.4  Media with cardholder data securely stored/accessible/destroyed
□ 9.5  POS devices protected from tampering and unauthorized substitution

REQUIREMENT 10 — LOGGING AND MONITORING
□ 10.1 Logging policies documented
□ 10.2 Audit logs record all required events (see Phase 6)
□ 10.3 Audit logs protected from destruction and modification
□ 10.4 Audit logs reviewed to identify anomalies or suspicious activity
□ 10.5 Audit log history retained (12 months, 3 months available)
□ 10.6 Time-synchronization technology in use (NTP on all systems)
□ 10.7 Failures of critical security control systems detected and reported

REQUIREMENT 11 — SECURITY TESTING
□ 11.1 Security testing policies documented
□ 11.2 Wireless access points detected and identified (if applicable)
□ 11.3 Vulnerabilities identified, prioritized, and addressed
       → Quarterly internal scans, quarterly external ASV scans
□ 11.4 Penetration testing performed (annually for SAQ D)
□ 11.5 Network intrusions and file changes detected and responded to (FIM)
□ 11.6 Payment page changes detected and responded to (v4.0 new)

REQUIREMENT 12 — SECURITY POLICY
□ 12.1 Information security policy established and maintained
□ 12.2 Acceptable use policies for end-user technologies defined
□ 12.3 Risks to CDE formally identified, evaluated, managed
□ 12.4 PCI DSS compliance managed (assigned responsibility)
□ 12.5 PCI DSS scope documented and validated annually
□ 12.6 Security awareness program in place
□ 12.7 Personnel screened to reduce insider threat risk
□ 12.8 Third-party service provider relationships managed
□ 12.9 Third-party providers acknowledge PCI responsibility
□ 12.10 Incident response plan exists, tested, and maintained
```

---

## Phase 8: Write the PCI Audit Report

### Report Template

```markdown
## PCI DSS v4.0 Compliance Audit Report

### Scope
- Systems audited: [list payment-related systems, services, endpoints]
- SAQ type: [A / A-EP / D]
- Compliance level: [1 / 2 / 3 / 4]
- Payment processor: [Stripe / Adyen / etc.]
- Date: [date]
- Assessor: [name]

### CDE Determination
- CDE systems: [list or "None — fully tokenized via processor"]
- Connected-to systems: [systems that connect to CDE]
- In-scope network segments: [subnets, VPCs]

### SAQ Determination
- Type: [A / A-EP / D]
- Justification: [why this SAQ type applies]
- Scope reduction: [what strategies are used to reduce scope]

### Summary
| Category                | Status | Findings |
|------------------------|--------|----------|
| Req 1-2: Network       | Pass/Fail | X findings |
| Req 3-4: Data protect  | Pass/Fail | X findings |
| Req 5-6: Vuln mgmt     | Pass/Fail | X findings |
| Req 7-9: Access control | Pass/Fail | X findings |
| Req 10-11: Monitoring   | Pass/Fail | X findings |
| Req 12: Policy          | Pass/Fail | X findings |

### Findings

#### Critical — Must Fix Before Accepting Payments
1. [Req X.Y] — Short description
   - **Evidence**: What was found and where
   - **Risk**: What an attacker could do
   - **Remediation**: Exact steps to fix
   - **Verified**: [ ] Fixed and re-tested

#### High — Fix Before Next SAQ Submission
[same format]

#### Medium — Fix Within 90 Days
[same format]

#### Low — Address in Next Review Cycle
[same format]

### Compensating Controls
[document any compensating controls with justification]

### What Passes
[list requirements that are correctly implemented]

### Recommendations
[broader suggestions — scope reduction, architecture improvements]

### Next Steps
- [ ] Remediate critical/high findings
- [ ] Schedule quarterly ASV scan (if required)
- [ ] Complete SAQ submission
- [ ] File AOC (Attestation of Compliance)
```

---

## Tips for Best Results

1. **Start with scoping** — Get the CDE scope right before auditing anything else. If your scope is wrong, you are auditing the wrong systems and missing the ones that matter.
2. **Verify tokenization end-to-end** — Do not trust documentation alone. Inspect the DOM to confirm card fields are in processor iframes. Check network traffic to confirm no PAN passes through your server. Grep logs for card number patterns.
3. **Check what is NOT there** — Missing controls (no MFA, no logging, no segmentation) are harder to spot than broken controls. Use the checklists in each phase and verify every checkbox.
4. **Search for card data patterns** — Run `grep -rn "[0-9]\{13,16\}" src/` to find potential PANs in code, config, or test fixtures. Check for Luhn-valid numbers in logs, databases, and error tracking.
5. **Read your processor's integration guide** — Stripe, Adyen, and Braintree each have specific PCI guidance documents. Know which integration type you use and its exact SAQ implications.
6. **Log review is non-negotiable** — PCI requires daily log review. If nobody is reviewing logs, it is an automatic finding. Verify that alerting exists for suspicious payment events.
7. **Track PCI v4.0 deadlines** — Requirements marked "best practice until March 31, 2025" are now mandatory. Key new requirements: 12-character passwords (8.3.6), payment page script controls (6.4.3, 11.6.1), targeted risk analysis (12.3.1).
8. **Document everything** — PCI is as much about documentation as controls. Every policy, procedure, risk assessment, and change must be written down, dated, and attributed. "We do it but did not write it down" is a finding.

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
