---
name: bug-bounty-hunting
description: Bug bounty hunting workflows — target selection, recon, code audit, vulnerability identification, and report submission on platforms like HackerOne, Bugcrowd, Intigriti.
tags: [security, bug-bounty, hacking, vulnerability, hackerone]
triggers:
  - bug bounty
  - vulnerability hunting
  - security research
  - HackerOne
  - Bugcrowd
  - finding bugs
  - responsible disclosure
---

# Bug Bounty Hunting

Assist the user with bug bounty hunting: target selection, reconnaissance, source code analysis, vulnerability identification, and report guidance.

## Audited Projects (Reference)

Detailed audit findings for specific projects are saved in `references/`:
- `references/shopware-audit-findings.md` — Shopware 6 SSRF (2 reports submitted)
- `references/matomo-audit-findings.md` — Matomo deep audit (SSRF confirmed, VIEW access trigger)
- `references/matomo-annotations-xss.md` — Matomo Stored XSS via `|raw` Twig filter (submitted)
- `references/jetpack-audit-findings.md` — Jetpack/WordPress SSRF + auth bypass (3 reports submitted)
- `references/woocommerce-audit-findings.md` — WooCommerce Agentic Checkout + Store API (1 report submitted)
- `references/magento-audit-findings.md` — Magento 2 attack surface analysis (unauthenticated API, SSRF vectors, deserialization, GraphQL)
- `references/hackerone-graphql-api.md` — Query bounty tables via GraphQL API (bypasses Cloudflare)
- `references/yeswehack-programs.md` — YesWeHack program list with bounty ranges (Indonesian programs: GOJEK, GoTo Financial)
- `references/matomo-policy-scope.md` — Matomo's full HackerOne policy, scope, out-of-scope list, and lessons learned (SSRF rejection)

Load these before re-auditing the same project to avoid repeating work.

## Submission Templates (Reference)

- `templates/hackerone-submission-template.md` — File structure + CVSS quick reference for HackerOne submissions

## User Hunting Philosophy

**Kanjeng wants SUBMITTABLE findings, not just Critical.** Any vulnerability that can be submitted and earn money is valuable — $777 is better than $0. Don't spend days chasing Critical when there's a confirmed High sitting right there. The workflow is:

1. Scan for ALL severity levels in parallel
2. Confirm the easiest exploitable finding first
3. Write report and submit
4. THEN go back for harder findings

"Diamond in the hand is worth more than gold in the ground."

**User's exact words:** "Kalo yg kecil² ketemu, asal bisa di submit dan jadi uang gpp, jgn fokus ke yg critical aja, tapi yg jelas bisa di submit ya" — Don't focus only on Critical. Find anything submittable that earns money. The key is "jelas bisa di submit" (clearly submittable) — the finding must be provable, not speculative.

**Severity Prioritization (User Preference):** When listing findings, always analyze in order: CRITICAL → HIGH → MEDIUM → LOW. User explicitly asked "kenapa tidak yang high dulu?" when agent suggested starting from MEDIUM. The logic: higher severity = higher bounty = better ROI on analysis time. Only fall back to lower severity when higher ones are confirmed not exploitable or have disqualifying caveats.

**Honesty About "Critical" Findings:** When critical findings have caveats (duplicate risk, high privilege requirement, design limitation), be UPFRONT about them before suggesting deep dive. User asked "kenapa tidak deep dive dulu dengan 2 temuan critical nya?" and agent correctly explained:
- SSRF blocklist weakness = likely duplicate of already-submitted report
- Plugin upload RCE = requires Super User (who already has full control)

This honesty saved time and built trust. Never oversell findings — user values directness over perfectionism.

## PHP Open-Source Bounty Landscape (Reality Check — 2026-05)

**Key finding from scanning 80+ HackerOne handles:** PHP open-source projects with actual monetary bounties are extremely rare. Most are VDP-only (credit/Hall of Fame, no money).

**Verified PHP programs with ACTUAL bounties:**
- **Matomo** — Critical $13,000 ✅ (best PHP target)
- **Automattic/Jetpack** — Bounty active, no public table ✅
- **Adobe/Magento** — Critical $5K-$15K (tiered) ✅
- **Shopware** — EUR, own submission form ✅

**Verified PHP programs that are VDP-ONLY (no money):**
- Drupal, MediaWiki/Wikimedia, Joomla, TYPO3, Laravel, Symfony, phpBB, PrestaShop, Nextcloud, ownCloud (unclear), phpMyAdmin, CakePHP, CodeIgniter, SilverStripe, CraftCMS, Concrete5, OctoberCMS, Statamic, Pimcore, OpenCart

**Why this matters:** Don't waste time cloning repos of Drupal, Joomla, etc. expecting bounty payouts. The user's priority is "jelas bisa di submit dan jadi uang" — VDP programs are time sinks if the goal is paid bounties.

**Strategy:** Focus on the 3-4 confirmed PHP bounty programs. Matomo is the best bet (small codebase, high bounty, low competition). Adobe/Magento is the backup (huge surface but complex). Jetpack/WooCommerce is already partially explored.

## CRITICAL RULE: Mandatory Local Testing Before Submit

**NEVER submit a report based on code reading alone. ALWAYS test the PoC locally first.**

### Required Workflow (NO EXCEPTIONS)
1. **Read code** — trace FULL data flow (input → processing → output)
2. **Setup local instance** — install target app locally (Docker/Composer/NPM)
3. **Execute PoC** — prove the bug ACTUALLY works in real browser/request
4. **Record evidence** — screenshot/video from YOUR local instance
5. **Only then submit** to HackerOne

### What NOT to do
- ❌ Submit based on code reading alone ("I think this is vulnerable")
- ❌ Submit because input is unsanitized without checking output sanitization
- ❌ Assume `|raw` in templates = XSS without checking if data is pre-escaped
- ❌ Skip testing because "it looks obvious"
- ❌ Trust partial analysis — always trace the COMPLETE chain

### Lesson Learned (May 2026 — Matomo XSS)
Submitted invalid Matomo XSS to HackerOne. Only traced `filterNote()` (no sanitize) + `|raw` in template. MISSED `decorateAnnotation()` → `Common::sanitizeInputValue()` → `htmlspecialchars()` which properly escapes at output. Report rejected. Reputation damage. Root cause: did NOT test on real instance, only read code.

## Ethical Boundaries

**CRITICAL — never violate these:**

- Do NOT claim credit for vulnerabilities the user didn't find themselves. The submitter must be the actual researcher.
- Do NOT run destructive tests (DoS, data deletion) against targets.
- Do NOT exfiltrate real user data during testing.
- Do NOT disclose vulnerabilities publicly before patches are released.
- Do NOT bypass authentication on production systems without explicit authorization.

**What the agent CAN do legitimately:**
- Analyze publicly available source code (open source repos on GitHub)
- Perform passive reconnaissance (DNS, subdomains, headers, OSINT)
- Identify vulnerability patterns in code and provide PoC templates
- Guide the user through exploitation steps they execute themselves
- Help write and format bug reports

## Collaborative Workflow

The most effective approach is a **pair-hunting model**:

1. **Agent**: clone repo, analyze source code, identify potential vulns, provide PoC
2. **User**: verify in local/test environment, capture screenshots, submit report

This is ethical because:
- Agent analyzes public code (same as any security researcher)
- User reproduces and validates independently
- User is the actual submitter and researcher of record

## Target Selection

### Bug Bounty Target Management

Target lists are maintained in `/tmp/bugbounty/TARGETS.md`. Before adding a new target, verify bounty status using the HackerOne GraphQL API (see `references/hackerone-graphql-api.md`). Key check: `offers_bounties: true` = paid program, `offers_bounties: null` = VDP only (no money).

### Best targets for code audit (agent can help directly):
- Open source projects with HackerOne/Bugcrowd programs
- Smaller codebase (< 50K LOC) = less competition
- Projects in languages the user knows (PHP/Laravel for Kanjeng)
- Recently launched programs or recently added features

**Pitfall — VDP-only programs**: Drupal and MediaWiki/Wikimedia are HackerOne programs but offer **NO monetary bounties** (credit/Hall of Fame only). Always verify `offers_bounties: true` via HackerOne GraphQL API before investing audit time. Check `references/program-status.md` for the latest verified status. The user's priority is "jelas bisa di submit dan jadi uang" — VDP programs waste time if the goal is paid bounties.

### Direct-to-Maintainer Programs

Many open source projects accept reports via email without HackerOne:
- Check `SECURITY.md` in repo root for email addresses
- Look for `security@project.com` contact
- Some have their own submission forms (e.g., Shopware)
- **Verify payment before investing time** — many say "report to us" but only give credit, not money

### Confirmed PAID programs (as of 2026-05)
- **Matomo** — HackerOne (`hackerone.com/matomo`), PHP, up to **$13K Critical** (RCE/SQLi), $1,777 High (XSS/CSRF/auth bypass), $777 other. Best PHP target — active repo, accepting submissions.
- **Shopware** — own submission form, pays EUR, PHP/Symfony codebase
- **GitLab** — HackerOne, $1K-$30K (very competitive)
- **Automattic/WordPress/Jetpack/WooCommerce** — HackerOne (`hackerone.com/automattic`), $250-$10K, PHP, wide scope. Jetpack (5M+ sites) + WooCommerce (4M+ sites) in same program. Blog token = shared secret across both.
- **Adobe/Magento** — HackerOne (`hackerone.com/adobe`), PHP, e-commerce. **3 Tier Bounty (verified via GraphQL API 2026-05):**
  - Tier 1 (Magento, ColdFusion, Firefly, Acrobat Web): Critical $5K-$10K, High $1K-$5K, Medium $200-$1K, Low $100-$200
  - Tier 2 (Commerce Web, Behance, Express, IMS): Critical $2.5K-$5K, High $500-$2.5K, Medium $100-$500, Low $0-$100
  - Tier 3 AI Bonus (Firefly AI, Acrobat AI, Express AI): Critical $7.5K-$15K, High $1.5K-$7.5K, Medium $300-$1.5K, Low $150-$300
  - Note: Adobe Commerce vulns requiring admin panel = max $5K. Hall of Fame + quarterly Top 10 rewards.
- **Discourse** — HackerOne, Ruby
- **Drupal** — HackerOne (`hackerone.com/drupal`), PHP, **VDP ONLY (no monetary bounties)** — credit/Hall of Fame only
- **MediaWiki/Wikimedia** — HackerOne (`hackerone.com/mediawiki`), PHP, **VDP ONLY (no monetary bounties)** — credit/Hall of Fame only

### Confirmed NOT paying / PAUSED / DISCONTINUED (avoid)
- **ownCloud** — DISCONTINUED on HackerOne (moved to YesWeHack, but 404 — likely private/paused). Do NOT target.
- **Nextcloud** — suspended monetary bounties (2026, due to AI spam flood)
- **PrestaShop** — PAUSED on YesWeHack (`prestashop-project.org/security/bug-bounty/` says "currently paused")
- **Saleor** — explicitly "no monetary rewards"
- **Strapi** — "no bounties, no swag"
- **Rocket.Chat** — "no monetary rewards"

### Platforms (all free to join):
- **HackerOne** (hackerone.com) — largest, most programs
- **Bugcrowd** (bugcrowd.com) — second largest
- **Intigriti** (intigriti.com) — strong in Europe
- **YesWeHack** (yeswehack.com) — 66+ paid programs, strong in Europe/Asia. API: `api.yeswehack.com/programs` returns JSON with bounty ranges. Top programs: Swiss Post E-Voting (€230K), Doctolib (€50K), OVHcloud (€12.5K), TeamViewer (€10K). Has Indonesian programs: GoTo Financial ($7K), GOJEK ($5K), DANA ($3K).
- **Open Bug Bounty** (openbugbounty.org) — no monetary reward but good for portfolio

### Finding programs:
- Filter by "recently launched" = less competition
- Check SECURITY.md in repo root for bounty info
- Look for programs with large scope = more attack surface
- Avoid mega-popular programs early (GitLab, Shopify) — too much competition
- **YesWeHack low-competition strategy**: Use API to find programs with <300 reports. Fewer reports = fewer hunters = higher chance of finding unreported bugs. Sort by `reports_count` ascending.

## Reconnaissance

### Passive recon (safe, no direct target contact):
```
# DNS records
dig target.com +short
dig ANY target.com +short

# Subdomain enumeration
for sub in api admin dev staging app mail ftp cdn static; do
  dig +short "$sub.target.com"
done

# SSL cert info (reveals infrastructure)
echo | openssl s_client -connect target.com:443 -servername target.com 2>/dev/null | openssl x509 -noout -subject -issuer -dates

# Headers analysis
curl -sI "https://target.com" -H "User-Agent: Mozilla/5.0" | head -30

# Wayback Machine for historical URLs
curl -s "https://web.archive.org/cdx/search/cdx?url=target.com/*&output=text&fl=original&limit=50"

# IP info
curl -s "https://ipinfo.io/<IP>"
```

### Google Dorks:
```
site:target.com
site:target.com filetype:php
site:target.com inurl:admin
site:target.com inurl:api
site:target.com inurl:login
```

### Limitation: Cloudflare-blocked sites
If the target is behind Cloudflare JS challenge, server-side tools cannot access it. Options:
- User performs browser-based testing, agent analyzes captured data
- Focus on source code analysis (GitHub repos) instead
- Check if origin IP is exposed (bypasses CF)

## Vulnerability Patterns to Look For

### High-value (P1-P2, $1K+):
- **SQL Injection**: string concatenation in queries, raw DB queries with user input
- **RCE**: `eval()`, `exec()`, `system()`, deserialization of user input
- **Auth Bypass**: missing auth middleware, JWT secret issues, IDOR
- **SSRF**: user-controlled URLs in server-side requests
- **File Upload → RCE**: unrestricted upload, path traversal in filenames

### Medium-value (P3, $250-$1K):
- **Stored XSS**: user input rendered without escaping in templates
- **IDOR**: sequential/predictable IDs in API endpoints, missing ownership checks
- **Privilege Escalation**: role checks missing on admin endpoints
- **Mass Assignment**: unprotected fillable fields in ORM models

### Low-value (P4-P5, $0-$250):
- **Information Disclosure**: verbose errors, debug mode enabled, exposed config
- **CSRF**: missing CSRF tokens on state-changing operations
- **Open Redirect**: unvalidated redirect parameters

## Environment Safety

**The user may ask "will this damage my VPS?" — reassure them:**
- Cloning repos and reading code = 100% safe (just file I/O)
- No exploits are executed against production targets
- Verification happens in local environment (localhost)
- Static analysis = reading text files, same as opening in VS Code

## Code Audit Approach

### PHP-Specific Audit Patterns (Learned from Matomo Audit)

When auditing PHP projects, look for these defense patterns and their weaknesses:

**1. WordPress SSRF Functions**
- `wp_remote_post()` / `wp_remote_get()` / `wp_remote_request()` — NO built-in SSRF protection
- `wp_safe_remote_post()` / `wp_safe_remote_get()` / `wp_safe_remote_request()` — WordPress blocks private/reserved IPs
- **Audit pattern:** `grep -rn 'wp_remote_post\\|wp_remote_get\\|wp_remote_request' --include='*.php' src/` (without "safe") — these bypass WordPress SSRF protection
- `download_url()` — Downloads URL to temp file, uses `wp_remote_get()` internally. If URL is user-controlled, potential SSRF via redirect bypass.

**2. SQL Query Construction**
- Parameterized queries (`?` bind) = safe. String concatenation with `$user_input` = vulnerable.
- Check if FIELD NAMES (not just values) are user-controllable — `INSERT INTO table ($fields) VALUES (?)` where `$fields` comes from `array_keys()` of user data is dangerous
- Check ORDER BY, GROUP BY, LIMIT — these often can't use parameterized placeholders

**3. SSRF Blocklist Analysis**
- Find the blocklist config (e.g., `http.blocklist.hosts` in Matomo)
- Check what's MISSING from the blocklist: `127.0.0.1`, `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`, `169.254.169.254` (cloud metadata), `[::1]` (IPv6 localhost), `0.0.0.0`, hex/octal IP representations
- Check if redirect following re-validates the final URL
- **"Inconsistency Pattern"** (proven in Shopware): If SSRF protection exists in ONE component but not another, report the inconsistency as a design flaw

**4. Twig `|raw` Audit (Proven Pattern — Matomo Annotations XSS)**
- `|raw` in Twig disables auto-escaping — only safe if the variable contains trusted HTML
- Trace ALL `|raw` variables back to their source — if ANY flow from user input, it's XSS
- High-risk: error messages, notification messages, user-generated content rendered with `|raw`
- Low-risk: hardcoded translation strings with `|raw`
- **Contrast technique**: If the SAME plugin has some templates using `|raw` and others using `|e('html_attr')`, the `|raw` instances are likely bugs, not design choices
- **Proven example**: Matomo Annotations — `filterNote()` only truncated length (no `htmlspecialchars()`), template used `{{ annotation.note|raw }}`, while `getEvolutionIcons.twig` properly used `counts.note|e('html_attr')`. This inconsistency was the key evidence.
- **Bounty**: Matomo Annotations XSS = $777-$1,777 (VIEW access, stored XSS affecting all users)

**5. `safe_unserialize` vs `unserialize` Check**
- Check if project uses `unserialize()` directly or a safe wrapper like `safe_unserialize($data, ['allowed_classes' => false])`
- If wrapper exists, check ALL call sites — are there any that pass `allowed_classes` with dangerous classes?
- Check if user input flows into unserialize: cookies, POST data, database values
- **Pitfall**: `safe_unserialize` with `$allowedClasses = []` (empty array) is SAFE because `empty([]) = true` → `allowed_classes = false`. Don't report as vulnerable just because `unserialize()` is called — check the actual `allowed_classes` value.
- **Proven example**: Matomo CoreUpdater — `safe_unserialize(Request::fromPost()->getStringParameter('messages', ''))` looks dangerous but `$allowedClasses = []` defaults to `allowed_classes = false`. NOT exploitable.

**6. Plugin/Extension Architecture**
- New plugins (recently added) are less audited — prioritize them
- Check plugin upload mechanisms — what validation exists on uploaded ZIPs?
- Check if plugins can override security policies (CSP, CORS, auth)

### Systematic Scan Methodology
Use `scripts/code-audit.sh <repo-dir> [src-subdir]` for automated scanning. It runs all scans below in priority order.

Run these scans in parallel for high-severity patterns:

#### Scan 1: RCE Vectors (P1)
```bash
grep -rn 'eval\s*(\|exec\s*(\|system\s*(\|passthru\s*(\|shell_exec\s*(\|proc_open\s*(\|popen\s*(' --include='*.php' src/
```

#### Scan 2: Deserialization (P1-P2)
```bash
grep -rn 'unserialize\s*(' --include='*.php' src/ | grep -v 'test\|Test\|spec\|mock'
```
Check: Is data source user-controllable? Is `allowed_classes` restricted?

#### Scan 3: SQL Injection (P1)
```bash
grep -rn 'executeQuery\|executeStatement\|->query(' --include='*.php' src/ | grep -i 'select\|insert\|update\|delete\|where'
```

#### Scan 4: File Upload (P1-P2)
```bash
grep -rn 'move_uploaded_file\|tmp_name\|\$_FILES\|UploadedFile\|getClientOriginalName\|getClientMimeType' --include='*.php' src/
```

#### Scan 5: SSRF (P2-P3)
```bash
grep -rn 'curl_setopt\|CURLOPT_URL\|file_get_contents\s*(\|HttpClient\|GuzzleHttp\|->request(' --include='*.php' src/
```
Check for URL validation. Compare with any `FileUrlValidator` that exists.

#### Scan 6: Auth Bypass
```bash
grep -rn 'auth_required.*false\|auth_required.*0' --include='*.php' src/
```
Check each endpoint for proper authorization.

#### Scan 7: Path Traversal
```bash
grep -rn 'file_get_contents\|file_put_contents\|readfile\|include\s*(\|require\s*(' --include='*.php' src/
```

#### Scan 8: XSS
```bash
grep -rn '\|raw\|autoescape.*false' --include='*.twig' src/
```

### Systemic Vulnerability Discovery

After finding one vulnerability, **follow the pattern** to find systemic issues:
- Found one SSRF? Grep for ALL components making HTTP requests
- Found one deserialization? Grep for ALL `unserialize()` calls
- Found one missing auth check? Grep for ALL `auth_required: false` endpoints

```bash
# Find all HTTP request-making components in an app system
grep -rn 'guzzle.*post\|guzzle.*get\|client.*request\|client.*post' --include='*.php' src/

# Find all deserialization points
grep -rn 'unserialize\s*(' --include='*.php' src/ | grep -v 'test\|Test'

# Find all unauthenticated endpoints
grep -rn 'auth_required.*false' --include='*.php' src/
```

Systemic findings are worth more than individual bugs — they show design flaws and often earn higher bounties. Report as "Systemic [Vuln Type] in [System]" rather than individual reports.

**Proven example**: Shopware SSRF — found one SSRF in webhook system, then grepped for all HTTP request components and found 7+ additional SSRF vectors in the app system (TaxProvider, ActionButton, AppDownloader, etc.). Submitted as two reports: individual webhook SSRF + systemic app system SSRF.

### Common Vulnerability Patterns Found

#### SSRF via Webhook Systems
- Webhook URLs stored in DB without validation
- Webhook client sends requests without SSRF protection
- Compare with `FileUrlValidator` which often HAS `FILTER_FLAG_NO_PRIV_RANGE`
- Attack: malicious app registers webhook to internal IP (169.254.169.254)

**Key audit technique — "Inconsistency Pattern"**: Look for security controls that exist in ONE part of the codebase but are missing in another. In Shopware, `FileUrlValidator` had SSRF protection but the webhook/app system didn't use it. This inconsistency is itself a strong argument for the report — it shows the developers knew about the risk but failed to apply it everywhere.

#### SSRF via Redirect Bypass
- URL validation happens BEFORE request
- HTTP redirects not re-validated after following
- Attack: external URL redirects to internal service

#### Deserialization from Database
- `unserialize()` on DB-sourced data without `allowed_classes`
- If attacker can write to table (via SQL injection), can achieve RCE
- Look for flow/job/task tables that store serialized payloads

#### auth_required: false Endpoints
- ImportExport file download (usually requires access token)
- User recovery endpoints (password reset)
- SSO endpoints
- Health check endpoints
- Product export (accessKey-based, no auth)

### Jetpack/WordPress Plugin Attack Surface
Jetpack monorepo (~15K files, 20+ plugins, 80+ packages). Key SSRF vectors:
- `wp_remote_post()` / `wp_remote_get()` / `wp_remote_request()` — NO SSRF protection (vs `wp_safe_remote_*`)
- `download_url()` uses `wp_safe_remote_get()` but follows redirects WITHOUT re-validating — bypass via 302 to internal IP
- `Post_To_Url` class (legacy) has no URL validation; `Form_Webhooks` (newer) HAS protection — inconsistency pattern
- External Media endpoint accepts ANY URL (no domain allowlist for pexels/openverse/google_photos)
- `permission_callback => '__return_true'` on sensitive endpoints (remote_authorize, verify_registration, sync/spawn-sync)
- 89 `allow_jetpack_site_auth` endpoints accept blog token without user context

### WooCommerce Attack Surface
WooCommerce (~15K files, modern PSR-4 in `src/`, legacy in `includes/`). Key vectors:
- **Agentic Checkout** (`src/StoreApi/Routes/V1/Agentic/`) — NEW AI agent checkout flow, blog token auth, no CSRF, payment processing
- **Store API** (`/wc/store/v1/*`) — 46+ unauthenticated endpoints (`__return_true`), checkout/cart manipulation
- **WC-Auth** (`/wc-auth/v1/authorize`) — CSRF on key generation, callback_url exfiltration
- **Blog token chain** — same token used for Jetpack RCE + WooCommerce payment fraud

### Blog Token Exploitation Chain (Critical Pattern)
The Jetpack blog token is a site-level shared secret stored in `wp_options`. Any vulnerability that leaks this token (SSRF, SQLi, DB backup, log leak) escalates to:
- **Jetpack RCE** (Backup Helper Script — `$needed_capabilities = array()`)
- **WooCommerce payment fraud** (Agentic Checkout — process Stripe payments)
- **Full site compromise**

This creates a vulnerability chain: medium-severity DB read → critical RCE + financial fraud. When reporting blog token issues, ALWAYS mention this chain to justify higher severity.

### Legacy vs Modern Code Inconsistency (Proven Pattern)
Both Jetpack and WooCommerce have legacy code paths that bypass newer security controls:
- `Post_To_Url` (legacy) has no URL validation; `Form_Webhooks` (modern) has protection
- Store API `requires_nonce()` returns false on Agentic Checkout
- `wp_remote_post()` (legacy) vs `wp_safe_remote_post()` (modern)

**Audit technique:** When you find a secure function (e.g., `wp_safe_remote_post`), grep for the UNSAFE variant (e.g., `wp_remote_post` without "safe") — the existence of both in the same codebase is itself a finding.

### WordPress SSRF Bypass Technique
`download_url()` → `wp_safe_remote_get()` validates INITIAL URL but follows HTTP redirects without re-validating redirect target. Bypass: set up public server returning 302 to `http://169.254.169.254/`. DNS rebinding also works (TOCTOU race).

### HackerOne CVSS Auto-Adjustment
HackerOne's automated pre-check may adjust CVSS score — this is NOT the final triage decision. The actual triage team determines final severity and bounty. Don't be discouraged by auto-adjustment. Example: Jetpack Forms SSRF was submitted as CVSS 8.6, auto-adjusted to 5.7, but final decision is by triage team.

### HackerOne Submission Field Mapping
When user asks "bantu isian sesuai ini" (help fill in the form), map files to fields:
- **Title** → clear, specific, one-line description
- **Asset** → product name (e.g., "Jetpack", "Matomo")
- **Weakness** → CWE ID (e.g., "CWE-918: Server-Side Request Forgery")
- **Severity** → CVSS score + vector
- **Description** → copy from `description.md`
- **Impact** → copy from `impact.md`
- **Attachments** → `poc-script.*`, evidence HTML files

User preference: provide description and impact as SEPARATE .md files, not one big report.

#### Magento-Specific Audit Patterns (from 2026-05-13 analysis)

Magento 2 is a modular monolith with ~222 modules, 23K+ PHP files, heavy XML config. Key attack patterns:

**Unauthenticated REST API** — 41 anonymous endpoints including admin token generation (`/V1/integration/admin/token` — no rate limit default), customer creation, password reset, guest checkout payment.

**GraphQL** — Full schema exposed via introspection, all mutations unauthenticated by default. `generateCustomerToken`, `createCustomer`, `placeOrder` accessible without auth.

**SSRF vectors** — ProductVideo `RetrieveImage.php` fetches user-supplied URLs. Dashboard `Tunnel.php` proxies requests with base64-decoded params.

**Deserialization** — 15+ files use `unserialize()` including `RedirectDataCacheSerializer`, `OperationProcessor`.

**File upload** — Multiple admin upload controllers with extension allowlists (bypass-worthy).

**Best hunting areas**: GraphQL mutations, guest checkout flow (price tampering), admin token brute force, ImportExport XML parsing (XXE), catalog search filter injection (SQLi via `like` operator).

Full analysis: `references/magento-audit-findings.md`

### Repo Comparison Technique (for target selection)

When comparing targets, use GitHub API to get:
1. **File counts by extension** — `git/trees/BRANCH?recursive=1` then count by extension
2. **Module/plugin counts** — count unique directories under key paths (e.g., `app/code/Magento/`, `plugins/`)
3. **Top-level structure** — `contents/` API for directory layout
4. **Stars, forks, size, open issues** — `/repos/OWNER/REPO` endpoint

Key metric: **PHP file count** = proxy for audit complexity. Magento (23,549) vs Matomo (3,396) = 7x difference.

## Laravel-specific patterns:
```php
// VULN: SQL injection via raw query
DB::raw("SELECT * FROM users WHERE id = $request->id")

// VULN: Mass assignment
User::create($request->all()); // without $fillable guard

// VULN: Unsafe deserialization
unserialize($request->data);

// VULN: Command injection
exec("convert " . $request->filename);
```

## PoC Creation

See `references/poc-creation.md` for detailed PoC templates including:
- SSRF PoC with listener and standalone test
- XSS PoC template
- IDOR PoC template
- Report template for submission

## Deliverable Packaging (User Preference)

**User wants everything ready to submit — not just analysis.**

### Submission Package Structure
For each report, prepare these files:
```
report-name/
├── REPORT_SUBMIT.md          # Full report (reference/copy-paste source)
├── vulnerability-description.md  # Description ONLY (copy to HackerOne "Description" field)
├── impact-description.md         # Impact ONLY (copy to HackerOne "Impact" field)
├── poc-script.sh/.php/.py       # Runnable PoC script
├── 01-evidence-name.html        # Code evidence (attach directly to HackerOne)
├── 02-evidence-name.html        # More evidence files...
└── supporting-files...          # Logs, manifests, etc.
```

### Key Workflow: Separate Description & Impact Files
**User preference:** Create separate .md files for description and impact instead of one big REPORT_SUBMIT.md. This maps directly to HackerOne's form fields:
- `vulnerability-description.md` → copy-paste to "Description" field
- `impact-description.md` → copy-paste to "Impact" field
- `poc-script.*` → attach as file
- `*.html` → attach as code evidence files

### Packaging
Bundle everything into a zip for easy download:
```bash
# Prefer zip (user preference), fall back to tar.gz if zip not installed
cd /tmp/bugbounty && python3 -c "
import zipfile, os
with zipfile.ZipFile('report-name.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, fnames in os.walk('report-name'):
        for fname in fnames:
            fp = os.path.join(root, fname)
            zf.write(fp, os.path.relpath(fp, '.'))
"
```

### Delivery Order
When sending via Telegram:
1. Brief summary message
2. `vulnerability-description.md` (copy to Description field)
3. `impact-description.md` (copy to Impact field)
4. PoC script (attach to report)
5. HTML evidence files (attach to report)
6. Zip package (everything bundled)

### User's Exact Preference
"langsung dalam bentuk zip complete file aja" — User wants everything zipped into one package. Always provide the zip.

## HackerOne Submission Workflow

When the user is ready to submit a report to HackerOne, follow this workflow:

### 1. Check Signal Requirements First
Before submitting, check the program's Signal requirement level:
- **Strict (≥ 1.0)**: Most restrictive. New hackers get 4 trial reports per program, 6 total per 30 days.
- **Standard (≥ 0.0)**: Recommended for most programs.
- **Lenient (≥ -1.0)**: Most permissive.

**Signal impact:**
- Accepted/confirmed report → Signal goes UP ✅
- Informational → Signal stays NEUTRAL ⚪
- Duplicate → Signal stays NEUTRAL ⚪
- N/A/rejected → Signal goes DOWN ❌
- Spam/invalid → Signal goes DOWN significantly ❌

**Implication for new hackers:** Only submit reports you're confident are valid. Save trial reports for confirmed vulnerabilities. Warn the user about Signal BEFORE they submit.

### 2. Prepare Submission Package
Each report needs:
- **Title**: Clear, specific (e.g., "SSRF via SiteContentDetector — Incomplete Host Blocklist")
- **Weakness**: CWE ID (e.g., CWE-918 for SSRF)
- **CVSS Score**: Use the CVSS calculator. For SSRF with VIEW access: `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` = 7.1 (High)
- **Description**: Vulnerability details with code evidence
- **Impact**: What an attacker could achieve
- **Attachments**: PoC script, code evidence, screenshots

### 3. CVSS Scoring Guide
Common CVSS vectors for bug bounty:
- **SSRF (VIEW access)**: `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:N/A:N` = 7.1 High
- **SSRF (Admin access)**: `CVSS:3.0/AV:N/AC:L/PR:H/UI:N/S:C/C:H/I:N/A:N` = 6.5 Medium
- **SSRF (Author+, no domain allowlist)**: `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N` = 5.4 Medium
- **RCE via shared secret (blog token)**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` = 9.8 Critical
- **Payment fraud via shared secret**: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` = 8.2 High
- **Stored XSS**: `CVSS:3.0/AV:N/AC:L/PR:L/UI:R/S:C/C:L/I:L/A:N` = 5.4 Medium
- **IDOR**: `CVSS:3.0/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` = 6.5 Medium
- **Info Disclosure**: `CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` = 5.3 Medium

### 4. Asset Matching
HackerOne requires matching the report to a specific asset in the program's scope. Check the program's "Scope" tab. If unsure, select "All assets" or the main asset.

### 5. Evidence Requirements
HackerOne reviewers prefer **concrete evidence** over theoretical capability:
- Screenshots of vulnerable code (with highlighting)
- Screenshots of PoC execution (terminal output, HTTP responses)
- curl commands that demonstrate the vulnerability
- PoC scripts (`.sh`, `.py`, `.php`)

### 6. Creating Code Evidence Files (PREFER DIRECT HTML ATTACHMENT)

**Key learning: Attach HTML files DIRECTLY to HackerOne — no need for screenshots.** Reviewers can open HTML in their browser with syntax highlighting. This is cleaner, more professional, and easier than screenshots.

**Workflow:**
1. Create styled HTML files with dark-theme code highlighting
2. Each HTML file = one code evidence piece (e.g., "weak blocklist", "no URL validation")
3. Send HTML files to user via Telegram
4. User attaches `.html` files directly to HackerOne report

**User preference:** "apa file html itu aja saya attach?" → Yes, attach HTML files directly. Better than screenshots.

**Template for HTML evidence files:**
```html
<!DOCTYPE html>
<html><head><title>FILENAME - ISSUE</title>
<style>body{background:#1e1e1e;color:#d4d4d4;font-family:'Consolas',monospace;padding:20px;font-size:14px;line-height:1.6}
.code{background:#2d2d2d;padding:15px;border-radius:8px;border-left:4px solid #569cd6}
.highlight{background:#4a2020;border-left:4px solid #f44747}
.comment{color:#6a9955}.string{color:#ce9178}.key{color:#9cdcfe}
.label{color:#569cd6;font-weight:bold;font-size:16px;margin-bottom:10px}
.filename{color:#808080;font-size:12px;margin-bottom:5px}</style></head>
<body>
<div class="filename">📄 FILEPATH (line N)</div>
<div class="label">🔴 VULNERABILITY TITLE</div>
<div class="code highlight">
<!-- vulnerable code here -->
</div>
</body></html>
```

## CRITICAL FAILURES — Lessons Learned (2026-05-13)

**Two reports were rejected due to sloppy analysis. This MUST NOT happen again.**

### Failure 1: SSRF Report Rejected (Out of Scope)
- **Mistake**: Submitted "SSRF via SiteContentDetector — Incomplete Host Blocklist"
- **Why rejected**: Blind SSRF is explicitly OUT OF SCOPE in Matomo's policy
- **Root cause**: Did NOT read the program's out-of-scope list before hunting
- **Impact**: Signal score damaged, 1 of 4 trial reports wasted

### Failure 2: Annotations XSS Report Rejected (Not Reproducible)
- **Mistake**: Claimed Stored XSS via `|raw` in template
- **Why rejected**: "XSS is never executed, annotation remains escaped in the UI"
- **Root cause**: Only checked INPUT path (`filterNote()`) without checking OUTPUT path (`decorateAnnotation()` → `Common::sanitizeInputValue()` → `htmlspecialchars()`)
- **Impact**: Signal score damaged further, another report wasted

### Root Causes (Why This Happened)
1. **Did not read policy first** — Out-of-scope list was ignored
2. **Incomplete data flow analysis** — Checked input + template, MISSED output encoding
3. **Overconfidence** — Listed "potential vulns" without verification
4. **No real instance testing** — Matomo policy REQUIRES validation on running instance
5. **Code analysis only** — Theorized exploitability without PoC

### MANDATORY Rules Going Forward (Non-Negotiable)
1. **READ POLICY FIRST** — Before ANY analysis, read the full program policy including out-of-scope list via HackerOne GraphQL: `team(handle: "X") { policy_setting { policy } }`
2. **TRACE COMPLETE DATA FLOW** — For XSS: input → storage → OUTPUT ENCODING → template. Never claim XSS without verifying the output encoding layer.
3. **VALIDATE ON REAL INSTANCE** — Never submit based on code analysis alone. Matomo policy: "Findings must be validated in a real, running Matomo instance"
4. **VERIFY BEFORE CLAIMING** — Do not list "potential vulnerabilities" without confirming exploitability
5. **CHECK OUTPUT ENCODING** — Always check if there's sanitization/encoding at the output layer (e.g., `decorateAnnotation()`, `sanitizeInputValue()`, `htmlspecialchars()`)
6. **ASSUME NOTHING** — Just because `|raw` exists doesn't mean XSS. The data might be pre-escaped.

### New Audit Checklist (For Every Finding)
- [ ] Read program policy (out-of-scope list)
- [ ] Trace input path (how data enters)
- [ ] Trace storage path (how data is stored)
- [ ] **Trace output path (how data is rendered — THE CRITICAL LAYER)**
- [ ] Check for output encoding (`htmlspecialchars()`, `sanitizeInputValue()`, etc.)
- [ ] Verify on real instance if possible
- [ ] Only THEN write report

## Critical Lesson: Matomo SSRF Rejection (2026-05-13)

**SSRF report #3729822 was rejected as "out of scope" by Matomo staff.** The report was "SSRF via SiteContentDetector — Incomplete Host Blocklist."

**Why it was rejected:**
1. **Blind SSRF** — explicitly out of scope in Matomo's policy: *"Blind Server-Side Request Forgery (SSRF)"*
2. **Code analysis only** — no working PoC validated on real instance
3. **Policy violation**: *"Reports based solely on code analysis, automated tools, or AI-generated output without demonstrated exploitability will not be accepted"*

**ALWAYS read the full program policy BEFORE hunting.** Matomo's out-of-scope list includes: Blind SSRF, path disclosure, clickjacking, info disclosure (non-sensitive), version disclosure, theoretical issues without PoC.

**Matomo Signal requirement: Strict (≥ 1.0)** — 4 trial reports per program. Rejected reports LOWER Signal. If Signal drops below threshold, researcher is BLOCKED from submitting.

**MANDATORY before submitting ANY report to Matomo:**
1. Read `policy_setting.policy` via HackerOne GraphQL API
2. Check the out-of-scope list
3. Validate on a real running Matomo instance
4. Have working PoC with screenshots
5. Never submit based on code analysis alone

## YesWeHack Programs (Alternative to HackerOne)

**Indonesian Programs (relevant for Kanjeng):**
- **GOJEK** — $5-$5,000, 590 reports, slug: gojek-bug-bounty-program
- **GoTo Financial** — $5-$7,000, 494 reports, slug: goto-financial-public-bounty-program

**High-Value Programs:**
- **Swiss Post E-Voting** — up to €230,000, 1159 reports
- **Doctolib** — up to €50,000, 1513 reports
- **TeamViewer** — $100-$10,000, 721 reports
- **Swiss Post** — $50-$10,000, 2213 reports

**YesWeHack API:** `https://api.yeswehack.com/programs?page=1&results_per_page=100`

## Pitfalls
- **Cloudflare/bot protection**: Most production targets have CF. Don't waste time trying to bypass from server — use browser-based testing or code audit instead.
- **Matomo out-of-scope**: Blind SSRF, path disclosure, clickjacking, info disclosure (non-sensitive), version disclosure, theoretical issues without PoC. ALWAYS check policy before hunting.
- **HackerOne Signal damage**: 6 rejected reports can severely damage Signal score. Wait for acceptance before submitting more.
- **Suspended bounty programs**: Always verify the program is still ACTIVE and PAID before investing time. Check the program page directly. Known suspended/paused as of 2026-05: ownCloud (discontinued on H1, 404 on YWH), Nextcloud (suspended monetary bounties due to AI spam), PrestaShop (paused on YesWeHack). Always check `references/program-status.md` for the latest known status.
- **HackerOne Signal Requirement**: Some programs (e.g., Matomo) enforce a "Signal" metric. Signal measures report quality on a rolling 365-day window. **Strict (≥ 1.0)** programs limit new hackers to 4 trial reports per program and 6 total per 30 days. Accepted reports raise Signal, N/A/duplicate are neutral, spam/rejected lower it. **Critical pitfall**: If Signal drops below the threshold, the researcher is blocked from submitting. Only submit reports you're confident are valid. Warn the user BEFORE they submit. Reference: https://docs.hackerone.com/en/articles/8505319-signal-requirements
- **HackerOne "concrete evidence" requirement**: Reviewers explicitly ask for "concrete evidence of successful exploitation (e.g., screenshots showing actual cloud metadata retrieval, internal service responses, or port scanning results) rather than just the theoretical capability." Always provide screenshots of PoC execution, not just code analysis.
- **Duplicate reports**: First reporter gets credit. Speed matters — if you find something, verify and submit quickly.
- **Excluded findings**: Every program has exclusions (headers, clickjacking, CSRF on anon forms, etc.). READ the exclusions before hunting.
- **Auto-generated reports**: Programs explicitly reject AI-generated reports without manual verification. Always reproduce findings manually.
- **Scanning tools**: Most programs prohibit automated scanners against production. Use code review instead.
- **Background processes for PoC**: When starting a listener server, use `terminal(background=true)` — do NOT use `&`, `nohup`, or `disown` in foreground commands. The shell wrapper will reject them.
- **tar.gz over zip**: Servers often don't have `zip` installed. Use `python3 zipfile` module as fallback: `python3 -c "import zipfile; zf=zipfile.ZipFile('out.zip','w',zipfile.ZIP_DEFLATED); zf.write('file'); zf.close()"`. User prefers zip over tar.gz.
- **YesWeHack API**: Use `api.yeswehack.com/programs?page=N` to discover programs with bounties programmatically. Response includes `bounty`, `bounty_reward_min`, `bounty_reward_max`, and `currency` fields.
- **HackerOne GraphQL API**: HackerOne's main pages are behind Cloudflare, BUT the GraphQL endpoint at `https://hackerone.com/graphql` is accessible via curl. Use introspection queries to discover schema, then query bounty tables, team info, and program details programmatically. See `references/hackerone-graphql-api.md` for working queries and schema details.
- **RCE bounty with prerequisites**: RCE vulnerabilities that require a prerequisite (like blog token compromise) may receive lower bounty than CVSS suggests. Triage team factors in "how hard is it to get the prerequisite." Frame the report as defense-in-depth failure and list multiple ways the prerequisite could be obtained (SSRF, SQLi, DB leak, log exposure).
- **Payment fraud bounty with prerequisites**: Similar to RCE, payment fraud vulns requiring blog token may get lower bounty. Emphasize the vulnerability CHAIN: any medium-severity DB read becomes critical financial fraud. List blog token compromise vectors exhaustively.
- **HackerOne auto-adjustment**: HackerOne's automated pre-check may adjust CVSS (e.g., 8.6 → 5.7). This is NOT final — triage team decides. Don't be discouraged. Submit anyway.
- **MUST TEST BEFORE SUBMIT (CRITICAL)**: NEVER submit a report based on code analysis alone. ALWAYS set up a local instance and execute the PoC to prove it works. The Matomo XSS lesson (May 2026): partial code analysis (missing output sanitization) led to invalid submission and reputation damage. Test every claim with real execution before submitting. Matomo's web installer creates config files that conflict with manual setup. If installing for PoC, use the web installer flow (system check → DB setup → create super user → tracking setup) rather than trying to create config.ini.php manually. The installer writes a 243-byte config on first access that blocks manual config creation.
- **Matomo out-of-scope (CRITICAL LESSON — SSRF rejected 2026-05-13)**: Matomo's HackerOne policy explicitly excludes: "Blind Server-Side Request Forgery (SSRF)", "Theoretical issues or issues based only on code patterns without a working exploit", "Reports based solely on code analysis, automated tools, or AI-generated output without demonstrated exploitability". The SSRF via SiteContentDetector (#3729822) was rejected as "Not Applicable" with "As mentioned in the pre-submission hook, this is out of scope." **LESSON: Always read the FULL program policy BEFORE investing audit time.** Use HackerOne GraphQL API: `team(handle: "matomo") { policy_setting { policy } }` to get the full policy text. Key in-scope: XSS, CSRF, Auth bypass, SQL Injection (demonstrated), RCE. Key out-of-scope: Blind SSRF, path disclosure, clickjacking, info disclosure (non-sensitive), code-analysis-only reports.
- **HackerOne severity button selection**: When user asks for severity, provide the CVSS broken down into individual button selections (Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope, Confidentiality, Integrity, Availability) — not just the CVSS string. User fills HackerOne form with buttons/dropdowns, not text fields.
- **HackerOne form fields as copy-paste**: When user asks "title, asset, weakness, severity, description, impact" — create a single markdown file with each field as a separate section, ready to copy-paste. User preference: `hackerone-submission-fields.md` with clear headers for each field.

## SSRF Hunter Techniques (from Bug-Bounty-Agents)

### SSRF Bypass Techniques
- **Hex IP**: `http://0x7f000001` = `http://127.0.0.1`
- **Octal IP**: `http://0177.0.0.1` = `http://127.0.0.1`
- **Decimal IP**: `http://2130706433` = `http://127.0.0.1`
- **IPv6**: `http://[::1]` or `http://[::ffff:127.0.0.1]`
- **DNS Rebinding**: First resolve to safe IP (passes validation), then re-resolve to internal IP
- **Redirect bypass**: `http://attacker.com/ssrf` → 302 to `http://169.254.169.254`
- **URL parsing confusion**: `http://attacker.com@internal-host`
- **Protocol smuggling**: `gopher://`, `file://`, `dict://`
- **Cloud metadata endpoints**:
  - AWS: `http://169.254.169.254/latest/meta-data/`
  - GCP: `http://metadata.google.internal/computeMetadata/v1/`
  - Azure: `http://169.254.169.254/metadata/instance`

### SSRF Detection in Code
Look for components that make HTTP requests:
```bash
# Find all HTTP request-making code
grep -rn 'guzzle.*post\|guzzle.*get\|client.*request\|client.*post' --include='*.php' src/
grep -rn 'HttpClient\|fetch\|axios\|request(' --include='*.ts' --include='*.js' src/
grep -rn 'urllib\|requests\|httpx\|aiohttp' --include='*.py' src/
```

Check if URLs are validated:
```bash
# Look for URL validation
grep -rn 'FILTER_VALIDATE_IP\|FILTER_FLAG_NO_PRIV_RANGE\|isPrivate\|isReserved' --include='*.php' src/
```

### The "Inconsistency Pattern" (Proven in Shopware)
If you find SSRF protection in ONE component but not another, report it as a design flaw:
- "Component A validates URLs against SSRF"
- "Component B does NOT validate URLs"
- "This inconsistency shows the risk was known but not properly mitigated"

### The "Multi-Trigger Pattern" (Proven in Matomo)
When you find SSRF via component X, DON'T stop. Grep for ALL places that call the same HTTP client:
```bash
grep -rn 'detectContent\|sendHttpRequest\|sendHttpRequestBy' --include='*.php' .
```
In Matomo, the SSRF was triggerable from 4 different endpoints:
- `SitesManager.detectConsentManager` API (VIEW access only!)
- `SitesManager.getTrackingMethodsForSite` Controller (VIEW access)
- `BotTracking.getTrackingMethodsForSite` Controller (VIEW access)
- `PrivacyManager.consent` Controller (Admin access)

The LOWEST privilege trigger is the most valuable — report that one. VIEW access SSRF is much more impactful than Admin access SSRF.

### The "Blocklist Weakness Pattern"
When a project has a host blocklist for outgoing requests:
1. Read the FULL blocklist config
2. Check what's MISSING: `127.0.0.1`, `10.x.x.x`, `172.16-31.x.x`, `192.168.x.x`, `169.254.x.x`, `[::1]`, `0.0.0.0`
3. Check if `checkHostIsAllowed` parameter defaults to `false` anywhere
4. Check if redirect following re-validates the final URL
5. Find ALL trigger points that use the HTTP client

### The "Twig `rawSafeDecoded` Pattern"
Matomo's `rawSafeDecoded` Twig filter uses `htmlspecialchars()` internally but marks output as `'is_safe' => ['all']`. This is safe for HTML context but could be dangerous if used in JavaScript/CSS context. Always check where the filtered value is rendered.

## GraphQL Attack Techniques

### Introspection Query
```graphql
{__schema{types{name,fields{name,type{name}}}}}
```

### Common GraphQL Vulnerabilities
1. **Introspection enabled** — exposes full schema
2. **No query depth limit** — DoS via nested queries
3. **No rate limiting** — brute force via queries
4. **IDOR via GraphQL** — access other users' data via ID
5. **Batch queries** — bypass rate limits

## Business Logic Flaws

### Common Patterns
1. **Race conditions** — concurrent requests bypass checks
2. **Price manipulation** — negative quantities, decimal overflow
3. **Workflow bypass** — skip steps in multi-step processes
4. **State manipulation** — change order status directly
5. **Privilege escalation** — access admin functions as regular user

### Testing Approach
1. Map the normal workflow (register → verify → purchase)
2. Try to skip steps or repeat steps
3. Manipulate parameters at each step
4. Test with negative/extreme values
5. Test concurrent requests

## JWT Attack Techniques

### Common JWT Vulnerabilities
1. **Algorithm confusion** — `alg: none` or RS256→HS256
2. **Weak secret** — brute force HMAC secret
3. **Kid injection** — path traversal in `kid` header
4. **JWKS injection** — point to attacker-controlled JWKS

### JWT Testing
```bash
# Decode JWT
echo "eyJhbGciOiJIUzI1NiJ9" | base64 -d

# Test alg:none
# Modify header: {"alg":"none","typ":"JWT"}
# Remove signature
```

## Exploit Chaining

### Chain Strategy
1. **Start with low-severity findings** — info disclosure, verbose errors
2. **Combine with auth issues** — weak session, missing auth
3. **Escalate to high impact** — RCE, data access, payment bypass

### Example Chains
- **Info Disclosure → IDOR → Account Takeover**
- **SSRF → Internal API Access → Admin Access**
- **XSS → Session Hijacking → Account Takeover**
- **Weak JWT → Auth Bypass → Data Exfiltration**

## Report Format

Good reports include:
1. **Title**: Clear, specific (e.g., "Stored XSS in user profile bio field")
2. **Severity**: Self-assessed P1-P5 with justification
3. **Description**: What the vulnerability is and why it matters
4. **Steps to Reproduce**: Numbered, exact, reproducible
5. **PoC**: Code/curl commands/screenshots
6. **Impact**: What an attacker could achieve
7. **Remediation**: Suggested fix (optional but impressive)
