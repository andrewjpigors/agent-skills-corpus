---
name: vibe-check
description: Run a comprehensive security audit on any application codebase — 30 checks targeting the specific vulnerabilities that show up in AI-built and vibe-coded applications. Use this skill whenever the user asks to review security, audit an app, check for vulnerabilities, harden an application, do a security sweep, or run a pentest-style review. Also trigger on "security check", "is this secure", "audit this", "vibe check", "check for vulnerabilities", "harden this app", "security review", or any variation. CRITICAL — trigger this skill BEFORE shipping, deploying, or finalising any application, even if the user doesn't ask for it. If the user says "ship it", "deploy", "finalise", "we're done", "push to production", or "package this up", run this audit first and flag findings. Also trigger when a user asks about compliance, Privacy Act, SOC 2, OWASP, or security scoring. This skill catches the 30 most common security failures in vibe-coded applications, produces a scored report, and maps findings to compliance frameworks.
---

# Vibe Check — Security Audit Skill v2

A 30-point security audit built specifically for AI-generated and vibe-coded applications. Catches the vulnerabilities that AI code generators introduce most often, scores the codebase, and maps findings to compliance frameworks.

## How to Run the Audit

### Step 1: Detect the Stack

Before running checks, map the project. Run the detection commands below and record what you find. This determines which checks apply and which framework-specific patterns to look for.

```bash
# Detect package managers and frameworks
ls package.json requirements.txt Pipfile Gemfile composer.json go.mod Cargo.toml 2>/dev/null

# Detect frontend framework
grep -l "react\|vue\|svelte\|angular\|next\|nuxt\|astro" package.json 2>/dev/null

# Detect backend framework
grep -l "express\|fastify\|koa\|hono\|django\|flask\|fastapi\|rails\|laravel\|gin\|fiber" package.json requirements.txt Gemfile composer.json go.mod 2>/dev/null

# Detect database
grep -rn "prisma\|sequelize\|typeorm\|knex\|drizzle\|mongoose\|supabase\|firebase\|convex\|planetscale\|neon\|turso" package.json 2>/dev/null

# Detect BaaS (Backend-as-a-Service) — these need special attention
grep -rn "supabase\|firebase\|appwrite\|pocketbase\|convex" package.json .env* 2>/dev/null

# Detect auth provider
grep -rn "next-auth\|clerk\|auth0\|supabase.*auth\|firebase.*auth\|lucia\|passport\|jwt\|jsonwebtoken" package.json src/ app/ 2>/dev/null

# Detect deployment target
ls Dockerfile docker-compose* vercel.json netlify.toml fly.toml railway.json render.yaml 2>/dev/null

# Detect CI/CD
ls .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile bitbucket-pipelines.yml 2>/dev/null
```

Record the detected stack at the top of the report. This context determines which checks are relevant and which framework-specific scan patterns to use.

### Step 2: Run All 30 Checks

Work through every check in order. For each one, inspect actual code — do not guess or assume. If a check doesn't apply (e.g. no database), mark it N/A with a one-line reason.

### Step 3: Score the Results

After all checks, calculate the Vibe Check Score using the scoring system in `references/scoring.md`.

### Step 4: Produce the Report

Use the output format at the bottom of this file. Include the score, compliance mapping, and prioritised fix list.

---

## The Checklist

### CATEGORY A: Secrets & Credentials

#### 1. API Keys in Frontend Code

Search all client-side files for hardcoded API keys, secrets, tokens, or credentials. AI generators frequently embed keys directly in frontend code because they optimise for "make it work" over "make it safe."

```bash
# Search for common key patterns
grep -rn "sk_\|pk_live\|AKIA\|ghp_\|gho_\|xox[bpsa]\|sk-ant\|sk-proj\|eyJhbG\|glpat-\|npm_\|pypi-\|PRIVATE.KEY\|BEGIN RSA\|BEGIN EC" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --include="*.vue" --include="*.svelte" --include="*.html" src/ public/ client/ frontend/ app/ pages/ components/ 2>/dev/null

# Search for variable assignments that smell like keys
grep -rn "api_key\|apiKey\|API_KEY\|secret\|SECRET\|password\|PASSWORD\|token\|TOKEN\|credential\|CREDENTIAL\|auth.*=.*['\"]" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --include="*.env.example" src/ public/ client/ app/ 2>/dev/null

# Check for .env values baked into build output
grep -rn "process\.env\.\|import\.meta\.env\.\|NEXT_PUBLIC_\|VITE_\|REACT_APP_" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" src/ app/ 2>/dev/null
```

Note: `NEXT_PUBLIC_`, `VITE_`, and `REACT_APP_` prefixed variables are intentionally exposed to the client. Check whether the values they hold are actually safe to expose. Supabase `anon` keys are designed to be public — but only if Row Level Security is properly configured (see Check 22).

**Fix:** Move all secret keys to server-side environment variables. Use a backend API route or serverless function to proxy requests that need secret keys. Only expose keys that are genuinely designed for client-side use (e.g. Stripe publishable keys, Supabase anon keys with RLS).

#### 2. .env Files in Git History

Check whether .env files have ever been committed. This is one of the most common findings — AI generators create .env files and developers commit them before adding .gitignore rules.

```bash
# Check git history for .env files
git log --all --full-history --oneline -- .env .env.local .env.production .env.development .env.staging .env.test 2>/dev/null

# Check current .gitignore
grep -n "env" .gitignore 2>/dev/null

# Check if .env exists in current tree (it shouldn't)
ls -la .env .env.* 2>/dev/null
```

**Fix:** If .env was ever committed, rotate every single key in that file immediately. Add `.env*` to .gitignore. Consider using `git-filter-repo` or `BFG Repo-Cleaner` to purge the file from history entirely.

#### 3. Weak JWT Secret

Look for JWT signing configuration. AI generators frequently use placeholder secrets like "secret", "jwt_secret", "your-secret-key", or copy them verbatim from tutorials.

```bash
# Find JWT configuration
grep -rn "sign\|verify\|jsonwebtoken\|jwt\|JWT_SECRET\|TOKEN_SECRET\|ACCESS_TOKEN\|REFRESH_TOKEN\|jose\|jws" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.go" --include="*.env" --include="*.env.example" . 2>/dev/null

# Look for hardcoded secrets in code (not env vars)
grep -rn "secret.*=.*['\"]" --include="*.js" --include="*.ts" --include="*.py" . 2>/dev/null | grep -i "jwt\|token\|sign\|auth"
```

Check if the secret value is: a dictionary word, shorter than 32 characters, the same across environments, or pulled unchanged from a tutorial or Stack Overflow answer.

**Fix:** Generate a cryptographically random secret of at least 256 bits. In Node.js: `require('crypto').randomBytes(64).toString('hex')`. Store in environment variables. Use different secrets per environment. Implement rotation capability.

---

### CATEGORY B: Authentication & Sessions

#### 4. No Rate Limiting on Auth Endpoints

Check whether login, signup, password reset, OTP verification, and API key generation endpoints have rate limiting. AI generators almost never add rate limiting because it's not part of the "make it work" loop.

```bash
# Look for rate limiting middleware
grep -rn "rate.limit\|rateLimit\|rate_limit\|throttle\|slowDown\|express-rate-limit\|rate-limiter-flexible\|bottleneck\|p-limit" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" package.json requirements.txt 2>/dev/null

# Find auth endpoints to cross-reference
grep -rn "login\|signin\|sign-in\|signup\|sign-up\|register\|forgot.password\|reset.password\|verify.*otp\|verify.*email\|verify.*code" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" src/ server/ api/ app/ routes/ 2>/dev/null
```

**Fix:** Add rate limiting to all auth endpoints. Implement account lockout after 5 failed attempts with exponential backoff. Consider CAPTCHA after repeated failures. Separate rate limits for login (strict) vs general API (moderate).

#### 5. JWTs in localStorage

Search for JWT/token storage patterns. XSS attacks can read anything in localStorage, which means one XSS vulnerability compromises every token on the site.

```bash
# Find token storage
grep -rn "localStorage\|sessionStorage" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . 2>/dev/null

# Check specifically for auth token storage
grep -rn "setItem.*token\|setItem.*jwt\|setItem.*auth\|setItem.*session\|setItem.*access\|setItem.*refresh" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" . 2>/dev/null
```

**Fix:** Store tokens in httpOnly, Secure, SameSite=Strict cookies. For SPAs calling cross-domain APIs where cookies aren't viable, use short-lived tokens (5-15 minutes) with refresh token rotation, and accept the residual XSS risk with strong CSP headers (see Check 28).

#### 6. Auth Tokens That Never Expire

Check JWT/session configuration for missing expiry. AI generators create tokens that last forever because expiry adds complexity they don't anticipate.

```bash
# Check for expiry in JWT creation
grep -rn "sign\|expiresIn\|exp\|maxAge\|ttl\|lifetime" --include="*.js" --include="*.ts" --include="*.py" . 2>/dev/null | grep -i "jwt\|token\|session\|cookie"
```

**Fix:** Access tokens: 15 minutes max. Refresh tokens: 7 days max. Implement refresh token rotation (each refresh issues a new refresh token and invalidates the old one). Invalidate all refresh tokens on password change.

#### 7. Sessions Not Invalidated on Logout

Check the logout endpoint. AI generators often implement logout as "delete the cookie on the client" without invalidating the session server-side. The old token still works.

```bash
# Find logout handling
grep -rn "logout\|signout\|sign.out\|log.out" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" src/ server/ api/ app/ routes/ 2>/dev/null
```

Inspect whether the logout handler: invalidates the session/token server-side, removes the cookie with proper flags, and clears any refresh tokens from the database.

**Fix:** Server-side session invalidation on every logout. For JWTs: maintain a token blocklist (Redis is ideal) or use short-lived tokens. Clear cookies with the same domain, path, and flag settings they were created with.

#### 8. Weak Password Hashing

Check password hashing implementation. AI generators sometimes use MD5, SHA1, or SHA256 without salt — or worse, store passwords in plaintext.

```bash
# Find hashing implementation
grep -rn "md5\|sha1\|sha256\|createHash\|hashlib\|MessageDigest\|plaintext\|\.password\s*=" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.java" --include="*.go" --include="*.php" . 2>/dev/null

# Check for proper hashing libraries
grep -rn "bcrypt\|argon2\|scrypt\|pbkdf2" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.go" package.json requirements.txt 2>/dev/null
```

**Fix:** Use bcrypt (cost factor 12+), scrypt, or Argon2id. Never roll your own hashing. Never use MD5 or SHA-family for passwords. If you find plaintext password storage, treat it as a critical incident — every user's password is compromised.

---

### CATEGORY C: Authorisation & Access Control

#### 9. Admin Routes with Frontend-Only Protection

Check whether admin or role-gated functionality is protected server-side or only by frontend routing (React Router guards, Vue Router meta, etc.). AI generators build beautiful role-based UIs and then forget to enforce the same rules on the API.

```bash
# Find admin/protected routes in frontend
grep -rn "admin\|isAdmin\|role.*admin\|PrivateRoute\|ProtectedRoute\|requireAuth\|authGuard\|canActivate\|meta.*auth\|meta.*role" --include="*.jsx" --include="*.tsx" --include="*.vue" --include="*.svelte" src/ app/ pages/ components/ 2>/dev/null

# Find API routes — do they have middleware?
grep -rn "router\.\(get\|post\|put\|patch\|delete\)\|app\.\(get\|post\|put\|patch\|delete\)\|@Get\|@Post\|@Put\|@Delete\|@app\.route\|@router\." --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" src/ server/ api/ app/ routes/ 2>/dev/null
```

For every admin route in the frontend, verify the corresponding API endpoint has server-side auth middleware.

**Fix:** Protect every route server-side. Apply auth middleware globally and whitelist public routes, rather than applying per-route and hoping you don't miss one.

#### 10. Missing Auth Middleware on Internal Routes

This is different from Check 9. This catches routes that aren't obviously "admin" but still need protection. AI code generation frequently adds auth middleware to the first few routes and skips it on routes added later.

Audit every single API endpoint. Cross-reference each one against the auth middleware chain. Pay special attention to:
- Routes added after the initial build
- CRUD endpoints for data that belongs to specific users
- Webhook endpoints (which may need signature verification instead of user auth)
- Health check / status endpoints (which should be public but not leak info)

**Fix:** Use a global auth middleware with an explicit allowlist of public routes. This inverts the default — everything is protected unless you specifically mark it as public.

#### 11. IDOR on Resource Endpoints

Check every endpoint that serves user-specific data (e.g. `/users/:id`, `/orders/:id`, `/documents/:id`). Determine whether the server validates that the requesting user owns or has access to the resource. This is the single most common API vulnerability and scanners almost never catch it.

```bash
# Find parameterised resource routes
grep -rn "/:id\|/<.*id>\|/\[id\]\|/\[.*Id\]\|params\.id\|params\[.id.\]\|request\.params\|req\.params" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" src/ server/ api/ app/ routes/ 2>/dev/null
```

For each match, check: does the query filter by both the resource ID AND the authenticated user's ID? If the query only uses the resource ID, any authenticated user can access any resource by changing the ID.

**Fix:** Validate ownership server-side on every resource request. The query should always include a `WHERE user_id = authenticatedUser.id` clause (or equivalent). For shared resources, implement an access control check.

---

### CATEGORY D: Injection & Input Handling

#### 12. SQL Injection via String Concatenation

Search for raw SQL built with string concatenation or template literals. AI generators love template literals for SQL because they're readable — and injectable.

```bash
# Find raw SQL patterns
grep -rn "SELECT\|INSERT\|UPDATE\|DELETE\|DROP\|CREATE\|ALTER" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.php" --include="*.go" src/ server/ api/ backend/ app/ 2>/dev/null

# Look specifically for string interpolation in SQL
grep -rn '`.*SELECT\|`.*INSERT\|`.*UPDATE\|`.*DELETE\|".*SELECT.*"\s*+\|".*INSERT.*"\s*+' --include="*.js" --include="*.ts" src/ server/ api/ 2>/dev/null
```

Inspect each match. If user input flows into the query without parameterisation, it's injectable.

**Fix:** Use parameterised queries or a query builder (Prisma, Drizzle, Knex, SQLAlchemy, etc.). Never concatenate user input into SQL. If you must write raw SQL, use `$1, $2` placeholders with a values array.

#### 13. XSS via Unsafe HTML Rendering

AI generators frequently use `dangerouslySetInnerHTML` (React), `v-html` (Vue), `{@html}` (Svelte), or `innerHTML` in vanilla JS to render user-supplied content. One malicious input and the attacker runs JavaScript in every user's browser.

```bash
# Find unsafe HTML rendering
grep -rn "dangerouslySetInnerHTML\|v-html\|{@html\|\.innerHTML\s*=\|\.outerHTML\s*=\|document\.write\|\.insertAdjacentHTML" --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" --include="*.vue" --include="*.svelte" --include="*.html" . 2>/dev/null
```

For each match, trace the data source. If it includes any user input, URL parameters, database content that originated from user input, or markdown rendering, it's vulnerable.

**Fix:** Sanitise HTML with DOMPurify before rendering. Better yet, avoid raw HTML rendering entirely — use the framework's built-in escaping. For markdown, use a library that sanitises output (e.g. `marked` with `sanitize: true`, or `remark` with `rehype-sanitize`).

#### 14. Missing Input Validation

Check whether API endpoints validate incoming data. AI generators build endpoints that trust whatever the client sends — type, length, format, everything.

```bash
# Look for validation libraries
grep -rn "zod\|yup\|joi\|class-validator\|ajv\|express-validator\|marshmallow\|pydantic\|cerberus" package.json requirements.txt 2>/dev/null

# Check if validation is actually used on routes
grep -rn "validate\|schema\|parse\|safeParse\|ValidationPipe" --include="*.js" --include="*.ts" --include="*.py" src/ server/ api/ app/ routes/ 2>/dev/null
```

If no validation library is installed, or if it's installed but not applied to routes, the API is accepting raw unvalidated input.

**Fix:** Validate all inputs at the API boundary. Use Zod (TypeScript), Joi, or Pydantic (Python). Validate type, length, format, and allowed values. Reject unexpected fields. Never trust client-side validation alone.

#### 15. Unsafe Deserialisation / eval / exec

AI generators sometimes use dangerous functions for flexibility — `eval()`, `exec()`, `pickle.loads()`, `yaml.load()` (without SafeLoader), `unserialize()`. These allow arbitrary code execution.

```bash
# Find dangerous functions
grep -rn "eval(\|exec(\|pickle\.load\|yaml\.load\|yaml\.unsafe_load\|unserialize(\|Function(\|new Function\|child_process\|vm\.runIn" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.php" . 2>/dev/null
```

**Fix:** Remove all uses of eval/exec in production code. Replace `pickle` with JSON. Use `yaml.safe_load()` instead of `yaml.load()`. If you need dynamic code execution, you almost certainly don't.

---

### CATEGORY E: Infrastructure & Deployment

#### 16. CORS Wildcard Configuration

Search for CORS configuration. `Access-Control-Allow-Origin: *` with credentials allows any website to make authenticated requests to your API using your users' cookies.

```bash
grep -rn "cors\|Access-Control-Allow-Origin\|Access-Control-Allow-Credentials\|origin.*\*\|origin.*true\|credentials.*true" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.yaml" --include="*.yml" --include="*.toml" --include="*.json" . 2>/dev/null
```

**Fix:** Whitelist specific origins per environment. Never use wildcard (`*`) with `credentials: true`. In development, you can be more permissive, but production CORS must be locked down.

#### 17. Application Running as Root

Check container and deployment configuration. One exploit in a root-running app = full system access.

```bash
# Check Dockerfiles
grep -rn "USER\|^FROM\|^RUN" Dockerfile* 2>/dev/null
# If no USER directive appears after FROM, it runs as root

# Check docker-compose
grep -rn "user:\|privileged:" docker-compose* 2>/dev/null
```

**Fix:** Add a `USER` directive in your Dockerfile. Create a non-privileged user and switch to it before `CMD`. In docker-compose, set `user: "1000:1000"`. Never use `privileged: true`.

#### 18. Database Port Exposed Publicly

Check whether database ports are accessible from the internet. AI generators often bind databases to 0.0.0.0 for development convenience and ship it that way.

```bash
# Check docker-compose port mappings
grep -rn "5432\|3306\|27017\|6379\|5984\|9200\|8529\|26257" docker-compose* 2>/dev/null
grep -A2 "ports:" docker-compose* 2>/dev/null

# Check for 0.0.0.0 bindings
grep -rn "0\.0\.0\.0\|host.*0\.0\.0\.0\|bind.*0\.0\.0\.0" docker-compose* *.toml *.yaml *.yml 2>/dev/null
```

**Fix:** Bind databases to `127.0.0.1` or a private network interface. In Docker, use internal networks and don't publish database ports. In cloud providers, use private subnets and security groups.

#### 19. No HTTPS Enforcement

Check whether the server enforces HTTPS. Credentials sent over plain HTTP can be intercepted on any network.

```bash
# Check for HTTPS redirect middleware
grep -rn "https\|redirect\|hsts\|Strict-Transport-Security\|ssl\|tls\|force.*ssl\|require.*https" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.conf" --include="*.yaml" . 2>/dev/null

# Check cookie secure flags
grep -rn "secure.*true\|secure.*false\|Secure\|httpOnly\|sameSite" --include="*.js" --include="*.ts" --include="*.py" . 2>/dev/null
```

**Fix:** Enforce HTTPS at the server or reverse proxy level. Set `Strict-Transport-Security` header with `max-age=31536000; includeSubDomains`. Redirect all HTTP to HTTPS. Set `secure: true` on all cookies.

#### 20. Debug Mode in Production

AI generators frequently leave debug flags enabled. This can expose stack traces, detailed error messages, admin panels, and development tools in production.

```bash
# Check for debug flags
grep -rn "DEBUG\|debug\|NODE_ENV\|FLASK_DEBUG\|DJANGO_DEBUG\|APP_DEBUG\|development\|devtools\|source.map" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.env" --include="*.env.example" --include="*.yaml" --include="*.toml" . 2>/dev/null

# Check for source maps in build output
ls dist/*.map build/*.map public/*.map .next/static/**/*.map 2>/dev/null
```

**Fix:** Set `NODE_ENV=production` (or equivalent) in production config. Disable source maps in production builds. Remove or protect any development tools, debug routes, or admin panels. Use environment-specific configuration — never rely on a single config file.

---

### CATEGORY F: Error Handling & Information Leakage

#### 21. Stack Traces in Error Responses

Check error handling patterns. AI generators often bubble full error objects to the client, giving attackers a map of your infrastructure.

```bash
# Find error handlers
grep -rn "catch\|\.catch\|error.*handler\|err.*res\.\|exception\|500" --include="*.js" --include="*.ts" --include="*.py" . 2>/dev/null | grep -i "send\|json\|response\|return"

# Look for direct error forwarding
grep -rn "res.*err\.\|res.*error\.\|res.*stack\|res.*message\|traceback\|format_exc" --include="*.js" --include="*.ts" --include="*.py" . 2>/dev/null
```

Look for: `res.status(500).send(err)`, `res.json({ error: err.message, stack: err.stack })`, Python `traceback.format_exc()` in responses, or any pattern that forwards internal error details to the client.

**Fix:** Log full errors server-side (structured logging with correlation IDs). Return generic error messages to clients: `{ error: "Something went wrong", code: "INTERNAL_ERROR" }`. Never include stack traces, database table names, file paths, or query details in responses.

---

### CATEGORY G: BaaS & Third-Party Misconfigurations

These checks target Backend-as-a-Service platforms (Supabase, Firebase, Appwrite, etc.) which are extremely popular in vibe-coded apps. The Moltbook breach — 1.5 million API keys leaked — was caused by misconfigured Supabase RLS.

#### 22. Supabase / Firebase Row Level Security Disabled

If the project uses Supabase or Firebase, check whether Row Level Security (RLS) or Security Rules are properly configured. AI generators scaffold database tables without enabling RLS, which means the client-side anon key has full read/write access to every table.

```bash
# Supabase: check for RLS mentions
grep -rn "rls\|row.level\|enable_rls\|\.rpc\|\.from(" --include="*.sql" --include="*.ts" --include="*.js" supabase/ migrations/ src/ 2>/dev/null

# Check Supabase migration files for RLS policies
find . -name "*.sql" -exec grep -l "CREATE POLICY\|ALTER TABLE.*ENABLE ROW LEVEL SECURITY\|RLS" {} \; 2>/dev/null

# Firebase: check security rules
cat firebase.json firestore.rules storage.rules database.rules.json 2>/dev/null
```

For Supabase: every table that holds user data MUST have RLS enabled with policies. If you find tables without `ENABLE ROW LEVEL SECURITY`, the public anon key can read and write everything.

For Firebase: look for rules like `allow read, write: if true` or `".read": true, ".write": true`. These are wide open.

**Fix (Supabase):** Enable RLS on every table: `ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;`. Create policies that restrict access by `auth.uid()`. Test with the anon key directly.

**Fix (Firebase):** Write security rules that check `request.auth` on every read/write. Test with the Firebase Emulator. Never ship `allow read, write: if true` to production.

#### 23. Stripe / Payment Webhook Signature Not Verified

If the project processes payments, check whether webhook endpoints verify the signature from the payment provider. Without verification, anyone can send fake payment events to your webhook and trigger order fulfilment, subscription activation, or credit additions.

```bash
# Find webhook handlers
grep -rn "webhook\|stripe.*event\|constructEvent\|verifyWebhookSignature\|STRIPE_WEBHOOK_SECRET\|WEBHOOK_SECRET" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" src/ server/ api/ app/ 2>/dev/null
```

Look for: `stripe.webhooks.constructEvent()` (correct) vs raw `JSON.parse(req.body)` without signature check (vulnerable).

**Fix:** Always verify webhook signatures using the provider's SDK. For Stripe: use `stripe.webhooks.constructEvent(body, sig, webhookSecret)`. For other providers, use their equivalent verification method. Never trust webhook payloads without signature verification.

#### 24. Hallucinated or Unaudited Dependencies

AI generators frequently add packages that either don't exist (hallucinated names that may be typosquatted by attackers) or are outdated and vulnerable. This is a supply chain risk unique to AI-generated code.

```bash
# Run dependency audit
npm audit --json 2>/dev/null | head -50
pip audit 2>/dev/null | head -20
bundle audit check 2>/dev/null | head -20

# Check for unusual or very low-download packages
cat package.json | grep -E '"[^"]+": "[^"]+"' 2>/dev/null

# Look for deprecated or unmaintained packages
npm outdated 2>/dev/null | head -20
```

Beyond automated audits, manually review the dependency list. If you don't recognise a package, look it up. Check its npm/PyPI page for download count, last publish date, and maintainer. AI-hallucinated package names are real attack vectors — attackers register them and wait.

**Fix:** Run `npm audit` / `pip audit` as part of every deploy. Review every new dependency before merging. Remove unused dependencies. Pin versions. Consider using `npm-lockfile-lint` or similar tools to enforce lockfile integrity.

---

### CATEGORY H: File Handling & Upload Security

#### 25. File Uploads Without MIME Validation

Check file upload handling. AI generators typically check the file extension on the client side and trust it on the server. Extensions lie. A `.jpg` file can contain PHP code.

```bash
# Find upload handling
grep -rn "upload\|multer\|formidable\|busboy\|multipart\|FileUpload\|UploadFile\|file.*save\|file.*write" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.php" src/ server/ api/ app/ 2>/dev/null
```

Check whether the server: validates MIME type using magic bytes (not just filename), restricts file size, stores uploads outside the webroot, renames files on upload, and sets `Content-Disposition: attachment` headers.

**Fix:** Validate MIME type server-side using a library that reads file headers (e.g. `file-type` for Node.js, `python-magic` for Python). Store uploads in a non-executable location (S3, cloud storage, or a directory with no-execute permissions). Generate random filenames. Set max file size limits.

---

### CATEGORY I: Transport & Browser Security

#### 26. Open Redirects in Callback URLs

Check OAuth callbacks, login redirects, and any endpoint that accepts a URL parameter for redirection. Attackers use open redirects to send users to phishing sites through your trusted domain.

```bash
grep -rn "redirect\|returnTo\|return_to\|next=\|callback\|callbackUrl\|redirect_uri\|returnUrl\|return_url\|goto\|destination\|continue" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" src/ server/ api/ app/ routes/ 2>/dev/null
```

**Fix:** Validate and whitelist every redirect destination. Use relative paths where possible. If you must redirect to absolute URLs, check them against an allowlist of trusted domains. Never redirect to a user-supplied URL without validation.

#### 27. Missing Security Headers

Check whether the application sets standard security headers. AI generators rarely add these because they don't affect functionality.

```bash
# Look for security header configuration
grep -rn "helmet\|X-Content-Type-Options\|X-Frame-Options\|X-XSS-Protection\|Referrer-Policy\|Permissions-Policy\|Content-Security-Policy" --include="*.js" --include="*.ts" --include="*.py" --include="*.rb" --include="*.conf" --include="*.yaml" . 2>/dev/null
```

Check for: `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `Permissions-Policy`.

**Fix:** Install `helmet` (Express/Node.js) or equivalent middleware. Configure Content Security Policy appropriate to your app. At minimum, set `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.

#### 28. Content Security Policy Missing or Permissive

This is a deeper check than 27. Even if CSP exists, check whether it's actually restrictive. `script-src 'unsafe-inline' 'unsafe-eval' *` provides zero protection.

```bash
grep -rn "Content-Security-Policy\|CSP\|script-src\|default-src\|connect-src\|style-src" --include="*.js" --include="*.ts" --include="*.py" --include="*.conf" --include="*.html" . 2>/dev/null
```

**Fix:** Implement a restrictive CSP. Start with `default-src 'self'` and add exceptions as needed. Use nonces or hashes instead of `'unsafe-inline'`. Never use `'unsafe-eval'` in production. Test with the browser console — CSP violations will be logged.

---

### CATEGORY J: Operational Security

#### 29. No Logging or Monitoring

Check whether the application has any structured logging, error tracking, or monitoring. AI-generated apps almost never include observability — you won't know you've been breached until a user tells you.

```bash
# Check for logging libraries
grep -rn "winston\|pino\|bunyan\|morgan\|log4j\|loguru\|structlog\|sentry\|datadog\|newrelic\|bugsnag\|logtail\|axiom" package.json requirements.txt 2>/dev/null

# Check for console.log (not a logging strategy)
grep -rn "console\.log\|console\.error\|print(" --include="*.js" --include="*.ts" --include="*.py" src/ server/ api/ app/ 2>/dev/null | wc -l
```

If the only "logging" is `console.log` statements, the application has no operational visibility.

**Fix:** Implement structured logging with a library (Pino or Winston for Node.js, structlog for Python). Log auth events (login, logout, failed attempts), data access, and errors. Send logs to a centralised service. Set up alerts for anomalies. At minimum, use Sentry or equivalent for error tracking.

#### 30. No Backup or Recovery Plan

Check whether the database has automated backups configured. AI generators never set up backups. One accidental `DELETE FROM users` and the business is gone.

```bash
# Check for backup configuration
grep -rn "backup\|dump\|pg_dump\|mongodump\|snapshot\|retention" --include="*.sh" --include="*.yaml" --include="*.yml" --include="*.toml" --include="*.json" . 2>/dev/null

# Check cloud provider configs
grep -rn "backup\|retention\|pitr\|point.in.time" vercel.json fly.toml railway.json render.yaml supabase/config.toml 2>/dev/null
```

**Fix:** Enable automated backups in your database provider (most cloud DBs have this as a checkbox). Set retention period to at least 7 days. Test restore process at least once. For Supabase: enable Point-in-Time Recovery. For self-hosted: set up `pg_dump` or equivalent on a cron schedule with off-site storage.

---

## Scoring

After running all 30 checks, calculate the Vibe Check Score. Read `references/scoring.md` for the full scoring methodology, weight table, and grade boundaries.

Quick summary:
- Each check has a weight (Critical=10, High=7, Medium=4, Low=2)
- Score = (total earned / total possible) × 100
- Grades: A (90-100), B (80-89), C (70-79), D (60-69), F (<60)

---

## Compliance Mapping

After scoring, map findings to applicable compliance frameworks. Read `references/compliance.md` for the full mapping table.

Quick summary of frameworks covered:
- **OWASP Top 10 (2021)** — map each finding to the relevant OWASP category
- **Australian Privacy Act 1988** — APP 11 (security of personal information)
- **SOC 2 Type II** — relevant trust service criteria
- **PCI DSS v4.0** — if the app processes payments
- **GDPR Article 32** — if the app handles EU user data

---

## Output Format

After running all 30 checks, produce the report in this structure:

```
# Vibe Check Report — [Project Name]
Date: [date]
Stack: [detected stack]
Vibe Check Score: [XX]/100 (Grade [X])
Checks Passed: [X]/30
Checks Failed: [X]/30
Checks N/A: [X]/30

## Scorecard
[Visual scorecard — see references/scoring.md for format]

## Critical (fix before shipping)
[Findings with severity CRITICAL — exploitable now]

## High (fix before production)
[Findings with severity HIGH — dangerous but may need specific attack vector]

## Medium (fix soon)
[Findings with severity MEDIUM — bad practice increasing attack surface]

## Low / Informational
[Minor or informational findings]

## Passed
[Checks that passed — confirm what IS secure]

## N/A
[Checks that don't apply and why]

## Compliance Impact
[Which frameworks are affected by the findings]

## Recommended Fix Order
[Prioritised list — critical first, estimated effort for each]

## Re-Audit Notes
[What to check on the next audit — new features, dependency updates, etc.]
```

For each finding, include:
- Check number and name
- Severity (Critical / High / Medium / Low)
- The specific file and line where the issue was found
- The actual vulnerable code snippet
- A concrete fix with working code example
- Compliance frameworks affected

Be direct. If it's broken, say it's broken. Show exactly how to fix it.
