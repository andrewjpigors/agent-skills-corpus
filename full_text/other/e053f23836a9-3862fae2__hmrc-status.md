---
name: hmrc-status
description: Check HMRC tax account (UK) — balances owed, upcoming payments, and outstanding submissions. Activates on questions about HMRC tax status, Self Assessment, VAT, Corporation Tax, PAYE, owed amounts, next tax payment due dates, return deadlines, or "what do I owe HMRC".
---

# hmrc-status

Answer questions about a user's UK tax position by calling the HMRC Developer
Hub APIs directly with `Bash` + `curl`. Read-only: balances owed, payments
allocated, returns due. No submissions, no writes.

> **Tool choice:** use `Bash` with `curl`, not `WebFetch`. Claude Code's
> `WebFetch` tool does not accept custom request headers, so it cannot
> send the `Authorization`, `Accept: application/vnd.hmrc.<v>+json`, or
> fraud-prevention headers HMRC requires.

## When this skill activates

Use this skill when the user asks any of:

- "Do I owe anything to HMRC?" / "What's my HMRC balance?"
- "What's my next Self Assessment payment / deadline?"
- "When is my VAT return due?" / "Is my VAT up to date?"
- "What do I still need to file?" / "Outstanding submissions / returns?"
- "Check my HMRC account" / "Give me a status report on my tax account"
- Anything about Corporation Tax balance, PAYE liabilities, or UK tax
  account health.

Also use this skill for the setup and management commands:

- `/hmrc-status:setup` or "set up HMRC skill" or "configure HMRC" or
  "set up HMRC credentials"
- `/hmrc-status:add-account` or "add HMRC account" or "link HMRC account"
  or "add a tax account"
- `/hmrc-status:reset` or "reset HMRC skill" or "wipe HMRC config" or
  "delete HMRC credentials"

If the user asks to *submit* a return or *pay* anything, refuse — this
skill is read-only.

## Configuration file

The skill stores credentials and account tokens in:

```
~/.config/hmrc-status/config.json
```

This file is created by `/hmrc-status:setup` and `/hmrc-status:add-account`.
Its permissions are set to `600` (owner read/write only). Format:

```json
{
  "client_id": "...",
  "client_secret": "...",
  "environment": "sandbox",
  "device_id": "...",
  "accounts": {
    "PERSONAL": {
      "nickname": "PERSONAL",
      "account_type": "personal",
      "access_token": "...",
      "refresh_token": "...",
      "nino": "QQ123456C",
      "vrn": null
    },
    "LTD": {
      "nickname": "LTD",
      "account_type": "company",
      "access_token": "...",
      "refresh_token": "...",
      "nino": null,
      "vrn": "987654321"
    }
  }
}
```

When reading credentials in Bash, always use Python subprocess to parse the
JSON and assign values to shell variables without printing them — never use
`cat` or `jq` pipelines that echo secret values back to the terminal or
conversation transcript.

## Prerequisites (check before any API call)

The skill reads credentials from either the config file or environment variables.

### Reading order

1. **Config file first**: check `~/.config/hmrc-status/config.json`. If it
   exists and the needed account is in `accounts[SUFFIX]`, use its
   `access_token`, `nino`, `vrn`, and `refresh_token`.
   Read `environment` from `config.environment` (fallback: `production`).
   Read `device_id` from `config.device_id` (fallback: `HMRC_DEVICE_ID` env var).

2. **Env vars as fallback**: if no config file, use the existing env var scheme:
   `HMRC_ACCESS_TOKEN[_SUFFIX]`, `HMRC_NINO[_SUFFIX]`, `HMRC_VRN[_SUFFIX]`,
   `HMRC_ENV`, `HMRC_DEVICE_ID`.

3. **Neither found**: if the config file does not exist AND the env vars are not
   set, stop with:
   > No HMRC credentials configured. Run `/hmrc-status:setup` to get started.

### Env vars table (fallback / advanced use)

| Variable | Required for | Notes |
|----------|--------------|-------|
| `HMRC_ACCESS_TOKEN` | every call | Bearer token, user-delegated. Rotates ~every 4 hours |
| `HMRC_NINO` | Self Assessment / Income Tax | National Insurance Number |
| `HMRC_VRN` | VAT | VAT Registration Number |
| `HMRC_UTR` | reserved | Not currently read by any endpoint here. Document only — do not require it. |
| `HMRC_ENV` | environment selection | `sandbox` or `production` (default `production`) |

`HMRC_REFRESH_TOKEN[_SUFFIX]` may also be present. See the 401 handler below
for how refresh tokens are used.

### Multi-account resolution

When reading accounts from the config file, the `accounts` object keys are
the suffixes (e.g. `PERSONAL`, `LTD`). The multi-account resolution logic is
the same as with env vars — match the user's account name against the keys,
fall back to the single account if only one exists.

For multi-account users (e.g. personal + LTD), the suffixed form
`HMRC_ACCESS_TOKEN_<ACCOUNT>`, `HMRC_NINO_<ACCOUNT>`,
`HMRC_VRN_<ACCOUNT>` is supported for env vars. Resolve the account as follows:

1. If the user uses one of the reserved default-account aliases —
   `personal`, `default`, `main`, `my own` — prefer the **unsuffixed**
   default (config `accounts` key matching the alias, or `HMRC_ACCESS_TOKEN`
   env var). Run the appropriate lookup and:
   - If the unsuffixed / unaliased entry is found, use it. Do **not** also
     try `_PERSONAL`/`_DEFAULT`/etc. — when both forms exist, the unsuffixed
     entry wins.
   - If the unsuffixed entry is **not** set, fall back to the matching suffix
     derived from the alias by step 2's sanitisation rule (`personal` →
     `_PERSONAL`, `default` → `_DEFAULT`, `main` → `_MAIN`, `my own` →
     `_MY_OWN`). If that suffixed entry is set, use it.
   - If neither the unsuffixed default nor the matching suffix is set,
     **stop and ask** — list the account keys/suffixes that *are* set and
     let the user pick one. Do **not** fall through to step 3's
     "single-suffix-is-default" rule.
   Bare pronouns like "me" / "my" / "for me" are **not** account
   selectors — treat them as the no-account-named case (step 3 below).
   If the user asks to check **both/all/every** account, iterate over every
   account in the config `accounts` block (or every `HMRC_ACCESS_TOKEN_*`
   env var found). Produce one report block per account labelled with the
   nickname/suffix; call the accounts' endpoints in parallel where possible.
   Otherwise:
2. If the user names a specific non-default account (e.g. "my LTD account",
   "the trader account"), sanitise the label: uppercase it, collapse each
   run of whitespace into a single `_`, and strip every character not in
   `[A-Z0-9_]`. Look up the result in the config `accounts` block first,
   then in env vars as `HMRC_ACCESS_TOKEN_<SUFFIX>`. **Then verify** the
   token is actually present. If not, list the accounts/suffixes that *are*
   set and ask the user to pick one.
3. If the user names no account, list available accounts:
   - From config: read the `accounts` keys.
   - From env vars (if no config): run
     `env | grep -oE '^HMRC_ACCESS_TOKEN(_[A-Z0-9_]+)?=' | sed 's/=$//' | sort -u`
     via `Bash`. Then:
   - If only one account is found, use it as the default.
   - If more than one is found, stop and ask the user which account to query.
4. Read the matching NINO / VRN for that account (from config or env vars);
   do not mix identifiers across accounts.
5. **Use the resolved suffix everywhere downstream.** Set `SUFFIX` to the
   underscore-prefixed suffix (e.g. `SUFFIX="_LTD"`) or to the empty string
   for the unsuffixed default account, then look up tokens and identifiers
   via bash indirect expansion (`TOKEN_VAR="HMRC_ACCESS_TOKEN${SUFFIX}"` →
   `${!TOKEN_VAR}`). Do **not** write nested expansions like
   `${HMRC_ACCESS_TOKEN${SUFFIX}}` — bash rejects them with `bad substitution`.

Only require the credentials actually needed for the question. If the user
asks about VAT only, missing NINO is fine — skip Self Assessment in the report.

If a *required* credential is missing, stop and tell the user which
variables to set for the specific tax they asked about, or to run
`/hmrc-status:setup` if nothing is configured at all.

## Base URL

- Production: `https://api.service.hmrc.gov.uk`
- Sandbox:    `https://test-api.service.hmrc.gov.uk`

Pick by reading `environment` from config (fallback: `HMRC_ENV` env var,
default: `production`).

## Required request headers

Every HMRC API call MUST include (substitute the value of the env var
into the header when building the request — don't send the literal
`$HMRC_ACCESS_TOKEN`):

- `Authorization: Bearer <value of access_token>`
- `Accept: application/vnd.hmrc.<version>+json` — version depends on
  the endpoint (see table below)
- Fraud-prevention `Gov-Client-*` / `Gov-Vendor-*` headers. HMRC requires
  the full set documented in `references/HMRC_ACCOUNT_APIS.md`
  (Common Headers). Send all of `Gov-Client-Connection-Method`,
  `Gov-Client-Device-ID`, `Gov-Client-User-IDs`, `Gov-Client-Timezone`,
  `Gov-Client-Local-IPs`, `Gov-Client-User-Agent`, `Gov-Vendor-Version`.
  Calls with fewer headers are typically rejected with `403`.

### Sourcing the fraud-prevention header values

HMRC checks these values for plausibility — fabricated or rotating
values are a compliance breach. Populate them from the running host
once, and reuse the values for the whole conversation:

| Header | Where to get the value (run in `Bash` once, cache in a shell var) |
|--------|-------------------------------------------------------------------|
| `Gov-Client-Connection-Method` | Literal string `OTHER_DIRECT` (CLI tool on the user's machine) |
| `Gov-Client-Device-ID` | Read from `config.device_id` (preferred), then `${HMRC_DEVICE_ID}` env var. If neither is set, stop and ask the user to run `/hmrc-status:setup` (which generates and stores a stable UUID). Do **not** silently generate a UUID per session — HMRC expects the same device ID across sessions, and a rotating value risks `403`. |
| `Gov-Client-User-IDs` | `os=$(id -un)` (e.g. `os=alice`) |
| `Gov-Client-Timezone` | `UTC$(date +%z \| sed 's/\([+-][0-9][0-9]\)\([0-9][0-9]\)/\1:\2/')` (e.g. `UTC+00:00`) |
| `Gov-Client-Local-IPs` | macOS: `ifconfig \| awk '/inet /{print $2}' \| grep -v '^127' \| paste -sd, -`. Linux: `hostname -I \| awk '{$1=$1; gsub(" ", ","); print}'` |
| `Gov-Client-User-Agent` | `os-family=$(uname -s)&os-version=$(uname -r)&device-manufacturer=unknown&device-model=unknown` |
| `Gov-Vendor-Version` | `hmrc-status-skill=1.0` (this skill's identifier) |

Use `Bash` with `curl -sS -H ...` to send these headers; `WebFetch`
cannot.

## How to pick the right endpoint

Match the user's question to one of these query types, then call the
corresponding endpoint. Full payload schemas live in
`references/HMRC_ACCOUNT_APIS.md`.

### Query type 1 — Balance owed (how much do I owe?)

| Tax | API version | Endpoint |
|-----|-------------|----------|
| Self Assessment / Income Tax | `4.0` | `GET /accounts/self-assessment/{NINO}/balance-and-transactions?onlyOpenItems=true` |
| VAT | `1.0` | `GET /organisations/vat/{VRN}/liabilities?from=<today − 365 days>&to=<today>` — compute `from = max(today − 365 days, 2017-12-01)` and `to = today` to satisfy HMRC's three window constraints (`from` not earlier than `2017-12-01`, `to` not in the future, range ≤ 365 days). **Page backwards** in further 365-day windows (`to = previous from − 1 day`, `from = max(previous from − 366 days, 2017-12-01)`). **Termination:** process the window whose `from == 2017-12-01`, then stop — do **not** attempt another iteration below that floor. Do **not** stop on the first empty window before reaching the floor. **During this backward scan, treat a `404` with `code: NO_DATA_FOUND` as an empty window and continue paging to the next older window.** Filter results across all windows to items with `outstandingAmount > 0` to find what's actually owed. |
| Corporation Tax / PAYE | n/a (not yet on MTD-style APIs) | Tell the user: "HMRC has not released a read API for Corporation Tax/PAYE balances yet. You can check via the Business Tax Account web UI at https://www.tax.service.gov.uk/business-account." |

### Query type 2 — Next payment due (when / how much?)

Reuse the balance-owed endpoints; the response includes due dates:

- Self Assessment `balanceDetails` fields to consult, in order:
  `payableAmount` (currently payable) + `payableDueDate` (when it's due);
  `pendingChargeDueAmount` + `pendingChargeDueDate` (next pending
  charge); `firstPendingAmountRequested` / `secondPendingAmountRequested`
  for payments-on-account. `overdueAmount` /
  `earliestPaymentDateOverdue` flag a **payment** overdue (a charge past
  its due date, not yet cleared) — render this on the `Balance owed`
  line per the output template, distinct from the **return** OVERDUE
  marker on the `Outstanding` line which uses the obligations API.
- VAT: each liability item has a `due` field — pick the earliest unpaid
  one (`outstandingAmount > 0`).

### Query type 3 — Next submission / outstanding return

| Tax | API version | Endpoint |
|-----|-------------|----------|
| Self Assessment crystallisation (annual return) | `3.0` | `GET /obligations/details/{NINO}/crystallisation?status=open` |
| Self Assessment quarterly updates | `3.0` | `GET /obligations/details/{NINO}/income-and-expenditure?status=open` |
| VAT return | `1.0` | `GET /organisations/vat/{VRN}/obligations?status=O` |
| Corporation Tax / PAYE | n/a (not yet on MTD-style APIs) | Tell the user: "HMRC has not released a read API for Corporation Tax/PAYE filing obligations yet. Check upcoming returns via the Business Tax Account web UI at https://www.tax.service.gov.uk/business-account." |

> The Income Tax Obligations API uses lowercase `status=open`/`status=fulfilled`
> and returns `periodStartDate`/`periodEndDate`/`dueDate`/`receivedDate` per
> obligation. The VAT obligations API uses single-letter `status=O`/`F` and
> returns `start`/`end`/`due`/`periodKey` — do not mix the two shapes.

## Implementation patterns for command steps

> **Host-tool mapping (for non-Claude agents, including Codex):**
> - `AskUserQuestion` means "use the host's interactive user-input tool". In
>   Codex, prefer `request_user_input`; if that is unavailable, ask a normal
>   chat follow-up and wait for the reply before continuing.
> - `Bash` means "use the host shell/terminal tool".
> - `/hmrc-status:*` command names are logical procedure names. Hosts without
>   slash commands should invoke the matching `Command:` section in this file
>   when the user asks to set up, add an account, or reset the skill.
> - `WebFetch` means any fetch-only web tool that cannot set arbitrary HMRC
>   headers; do not use it for authenticated HMRC calls.

> **AskUserQuestion — collecting free-text values (credentials, codes,
> identifiers):** The tool always appends an automatic "Other" text field for
> custom input. When the user must *type* a value, present exactly 2 options
> that describe actions or fallbacks — never use an option label as a
> placeholder for the value itself. Instruct the user explicitly to type in
> "Other". Good option labels: `"I have it ready — type in 'Other' below"` /
> `"I don't have it yet — show instructions"`. Bad: `"Paste Client ID in
> 'Other'"` (the user reads the label and selects it instead of typing).

> **Shell variables do NOT persist between Bash tool calls.** Every `Bash`
> invocation is a new process; variables set in one call are gone in the next.
> Consequence: collect ALL user inputs via `AskUserQuestion` *before* the
> first Bash call that needs them, then pass them as positional arguments to
> Python heredoc scripts (`python3 - arg1 arg2 << 'PYEOF'`). Never split a
> multi-step flow (open browser → capture code → exchange → save) across
> separate Bash calls if the steps share variables.

> **Never print raw auth URLs.** Long URLs wrap across terminal lines,
> inserting a space that corrupts parameter names (e.g. `redirect_uri` →
> `redirect _uri`). Use `open "$AUTH_URL"` (macOS) or
> `xdg-open "$AUTH_URL"` (Linux) to open the browser directly from Bash.

> **Never use `python3 -c "..." -- args`.** The `--` becomes `sys.argv[1]`
> and shifts every subsequent argument by one. Always use the heredoc form:
> `python3 - arg1 arg2 << 'PYEOF' ... PYEOF`.

## Command: /hmrc-status:setup

Interactive wizard that collects application credentials and writes
`~/.config/hmrc-status/config.json`. Run this once before adding accounts.

**Steps:**

1. Check if `~/.config/hmrc-status/config.json` exists. If it does and has a
   `client_id`, warn the user:
   > Config already exists with a client_id. Running setup will overwrite your
   > application credentials (linked accounts are preserved).
   Use `AskUserQuestion` to ask: `Overwrite existing credentials? (y/N):`.
   If the response is not `y` or `yes` (case-insensitive), stop:
   > Setup cancelled. Your existing config is unchanged.

2. Load the existing config JSON if present (to preserve `accounts` and
   `device_id`). If absent, start with an empty object.

3. Use `AskUserQuestion` to collect **client_id** with this exact prompt:

   ```
   HMRC Developer Hub — Client ID

   Enter your application's Client ID.

   How to find it:
     1. Sign in at https://developer.service.hmrc.gov.uk/developer/applications
     2. Open your application → Details tab
     3. Client ID appears under "Credentials"

   Haven't created an application yet?
     • Sign in or register at developer.service.hmrc.gov.uk
     • Click "Add an application to the sandbox" (or production once ready)
     • On the API subscriptions page, add:
         – Self Assessment Accounts (MTD) v4.0
         – Obligations (MTD) v3.0
         – VAT (MTD) v1.0
     • On the redirect URIs page, add one of:
         – urn:ietf:wg:oauth:2.0:oob    ← simplest, no local server needed
         – http://localhost:8080/callback ← lets the skill capture the code automatically
     • After saving, go to Credentials — your Client ID is listed there
     • Click "Generate a client secret" — copy it immediately (shown only once)

   Client ID:
   ```

4. Use `AskUserQuestion` to collect **client_secret** with this exact prompt:

   ```
   HMRC Developer Hub — Client Secret

   Enter your application's Client Secret.

     • Found under Credentials on your application's details page
     • If you haven't generated one yet: click "Generate a client secret"
       (it is only shown once — copy it before closing the page)
     • If you lost it: generate a new one (the old one will stop working)

   ⚠  This value is sensitive — treat it like a password.

   Client Secret:
   ```

5. Use `AskUserQuestion` to collect **environment** with this exact prompt:

   ```
   Environment

   Which HMRC environment does your application target?

     1  Sandbox     – safe for testing; uses synthetic test users
                      (register at developer.service.hmrc.gov.uk/sandbox)
     2  Production  – real HMRC data; requires HMRC production credentials approval

   Enter 1 or 2:
   ```
   Map `1` → `sandbox`, `2` → `production`. If the input is not `1` or `2`,
   use `AskUserQuestion` to re-ask. Repeat until valid.

6. **Device ID:** Check if `HMRC_DEVICE_ID` env var is set OR if the existing
   config has a `device_id`. If either exists, reuse it (prefer config value).
   Otherwise generate a new one via `Bash`:
   ```bash
   DEVICE_ID=$(uuidgen)
   ```
   Store as `device_id` in the config.

7. Write the config using Python — never print the secrets:
   ```bash
   python3 - "$CLIENT_ID" "$CLIENT_SECRET" "$ENV" "$DEVICE_ID" << 'PYEOF'
   import json, os, sys
   path = os.path.expanduser('~/.config/hmrc-status/config.json')
   os.makedirs(os.path.dirname(path), exist_ok=True)
   try:
       with open(path) as f:
           existing = json.load(f)
   except Exception:
       existing = {}
   config = {
       'client_id': sys.argv[1],
       'client_secret': sys.argv[2],
       'environment': sys.argv[3],
       'device_id': sys.argv[4],
       'accounts': existing.get('accounts', {})
   }
   with open(path, 'w') as f:
       json.dump(config, f, indent=2)
   os.chmod(path, 0o600)
   print('saved')
   PYEOF
   ```
   Use the heredoc form (`python3 - args << 'PYEOF'`) so positional args start
   at `sys.argv[1]` — **never** use `python3 -c "..." -- args` as the `--`
   becomes `sys.argv[1]` and shifts every argument by one.
   Verify the output is `saved`.

8. Confirm to the user:
   ```
   Setup complete. Credentials saved.

   Next step: add a tax account by running /hmrc-status:add-account
   ```

## Command: /hmrc-status:add-account

OAuth flow that authorises a Government Gateway account and saves the
resulting tokens to config. Run this once per HMRC account (personal,
LTD, etc.).

**Step ordering rationale:** Collect ALL user inputs first, then do the
browser/token work in as few Bash calls as possible. This avoids the
failure mode where a single-use auth code is consumed in a failed exchange
because account details weren't ready yet.

**Steps:**

1. Check config. If `~/.config/hmrc-status/config.json` does not exist or has
   no `client_id`, stop:
   ```
   No application credentials found.
   Please run /hmrc-status:setup first.
   ```

2. Use `AskUserQuestion` to collect **nickname**:

   ```
   Account nickname

   Choose a short label for this account. It will be used to reference it in queries
   (e.g. "check my LTD account", "what does TRADER owe?").

   Suggestions: personal, ltd, trader, company, spouse
   Type your chosen nickname in the 'Other' field below.
   ```
   Options: `"I have a nickname ready — typed in 'Other'"` /
   `"Show me the suggestions again"` (list personal, ltd, trader, company,
   spouse as a second prompt). Sanitise the answer: uppercase, spaces →
   underscores, keep only `[A-Z0-9_]`. Store as `NICKNAME`.

3. Use `AskUserQuestion` for **account type**:

   ```
   Account type

   What kind of HMRC account is this?

     1  Personal     — Self Assessment / Income Tax (needs NINO)
     2  Company      — VAT and/or Corporation Tax (needs VRN)
     3  Both         — you have personal SA and company VAT under the same login
   ```
   Options: `"1 — Personal"` / `"2 — Company"` / `"3 — Both"`.
   Map: `1` → `personal`, `2` → `company`, `3` → `both`.

4. If account type is `personal` or `both`, use `AskUserQuestion`:

   ```
   National Insurance Number (NINO)

   Format: 2 letters, 6 digits, 1 letter — e.g. QQ 12 34 56 C
   (spaces are fine, they will be stripped)
   Type your NINO in the 'Other' field below.
   ```
   Options: `"I have my NINO — typed in 'Other'"` /
   `"I need help finding my NINO"`. Strip spaces, uppercase. Store as `NINO`.

   If account type is `company` or `both`, use `AskUserQuestion`:

   ```
   VAT Registration Number (VRN)

   9-digit number — e.g. 123456789
   (usually shown on your VAT registration certificate)
   Type your VRN in the 'Other' field below.
   ```
   Options: `"I have my VRN — typed in 'Other'"` /
   `"I need help finding my VRN"`. Strip spaces. Store as `VRN`.
   For types where a value is not needed, set to empty string `""`.

5. Use `AskUserQuestion` to collect **redirect method**:

   ```
   Redirect method

   How should the skill receive the authorization code after you log in?

     1  Out-of-band (OOB) — HMRC shows the code on the page; you copy and paste it here
                             Redirect URI: urn:ietf:wg:oauth:2.0:oob
                             Works with any redirect URI configuration. Recommended.

     2  Local listener    — the skill starts an HTTP server on localhost:8080 for ~90 seconds;
                             the code is captured automatically when your browser is redirected.
                             Redirect URI: http://localhost:8080/callback
                             ⚠ Requires http://localhost:8080/callback registered in your app.
   ```
   Options: `"1 — OOB (recommended)"` / `"2 — Local listener"`.
   Default to OOB if unclear.

6. **In ONE Bash call:** read config, build the auth URL, and open the
   browser. If local listener was chosen, also run the listener, exchange
   the token, and save the account — all in this same call.

   **OOB path** (open browser, then exit the Bash call):
   ```bash
   python3 - << 'PYEOF'
   import json, os, secrets, subprocess
   path = os.path.expanduser('~/.config/hmrc-status/config.json')
   with open(path) as f:
       cfg = json.load(f)
   env = cfg['environment']
   host = 'test-api.service.hmrc.gov.uk' if env == 'sandbox' else 'api.service.hmrc.gov.uk'
   state = secrets.token_hex(16)
   url = (f'https://{host}/oauth/authorize?response_type=code'
          f'&client_id={cfg["client_id"]}'
          f'&scope=read:self-assessment+read:vat'
          f'&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob'
          f'&state={state}')
   subprocess.run(['open', url])          # macOS
   # subprocess.run(['xdg-open', url])    # Linux fallback
   print('browser_opened')
   PYEOF
   ```
   Tell the user: `Your browser has been opened. Sign in with your Government
   Gateway credentials, then copy the authorisation code shown and paste it
   below.`

   **Local listener path** (open browser + capture code + exchange + save,
   all in one call — pass all collected values as positional args):
   ```bash
   python3 - "NICKNAME" "ACCOUNT_TYPE" "NINO" "VRN" << 'PYEOF'
   import http.server, json, os, secrets, subprocess, sys, threading, urllib.parse

   path = os.path.expanduser('~/.config/hmrc-status/config.json')
   with open(path) as f:
       cfg = json.load(f)

   env = cfg['environment']
   host = 'test-api.service.hmrc.gov.uk' if env == 'sandbox' else 'api.service.hmrc.gov.uk'
   state = secrets.token_hex(16)
   redirect_uri = 'http://localhost:8080/callback'
   url = (f'https://{host}/oauth/authorize?response_type=code'
          f'&client_id={cfg["client_id"]}'
          f'&scope=read:self-assessment+read:vat'
          f'&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback'
          f'&state={state}')
   subprocess.run(['open', url])   # macOS; use xdg-open on Linux

   code = [None]
   class Handler(http.server.BaseHTTPRequestHandler):
       def do_GET(self):
           p = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
           code[0] = p.get('code', [None])[0]
           self.send_response(200); self.end_headers()
           self.wfile.write(b'<html><body style="font-family:sans-serif;padding:40px">'
                            b'<h2>Authorisation complete</h2>'
                            b'<p>You may close this tab.</p></body></html>')
           threading.Thread(target=self.server.shutdown, daemon=True).start()
       def log_message(self, *a): pass

   with http.server.HTTPServer(('localhost', 8080), Handler) as s:
       s.timeout = 90
       s.handle_request()

   if not code[0]:
       print('TIMED_OUT')
       raise SystemExit(1)

   result = subprocess.run([
       'curl', '-sS', '-X', 'POST', f'https://{host}/oauth/token',
       '-H', 'Content-Type: application/x-www-form-urlencoded',
       '--data-urlencode', 'grant_type=authorization_code',
       '--data-urlencode', f'client_id={cfg["client_id"]}',
       '--data-urlencode', f'client_secret={cfg["client_secret"]}',
       '--data-urlencode', f'redirect_uri={redirect_uri}',
       '--data-urlencode', f'code={code[0]}',
       '-w', '\n---HTTP:%{http_code}---\n'
   ], capture_output=True, text=True)

   lines = result.stdout.rsplit('\n---HTTP:', 1)
   body = lines[0].strip()
   http_code = lines[1].rstrip('-\n') if len(lines) > 1 else '0'
   if http_code != '200':
       print(f'TOKEN_ERROR: HTTP {http_code} — {body}')
       raise SystemExit(1)

   data = json.loads(body)
   access_token  = data.get('access_token', '')
   refresh_token = data.get('refresh_token', '')
   if not access_token:
       print('TOKEN_ERROR: no access_token in response')
       raise SystemExit(1)

   nickname = sys.argv[1]
   nino = sys.argv[3].replace(' ', '').upper() if sys.argv[3] else None
   vrn  = sys.argv[4].replace(' ', '') or None
   cfg['accounts'][nickname] = {
       'nickname': nickname, 'account_type': sys.argv[2],
       'access_token': access_token, 'refresh_token': refresh_token,
       'nino': nino, 'vrn': vrn,
   }
   with open(path, 'w') as f:
       json.dump(cfg, f, indent=2)
   os.chmod(path, 0o600)
   print('SAVED')
   PYEOF
   ```
   If output is `TIMED_OUT`, tell the user the listener timed out and offer
   to retry or switch to OOB. If `TOKEN_ERROR:`, show the message and stop.
   If `SAVED`, skip steps 7–8 and go to step 9.

7. **OOB only — collect auth code:** Use `AskUserQuestion`:

   ```
   Authorization code

   HMRC showed a code after you signed in. Type it in the 'Other' field below.
   ```
   Options: `"I have the code — typed in 'Other'"` /
   `"I got an error instead — describe it in 'Other'"`. Store as `AUTH_CODE`.
   If the user reports an error, diagnose and offer to retry.

8. **OOB only — exchange code and save** in ONE Bash call. Substitute the
   literal collected values directly into the positional arguments:

   ```bash
   python3 - "NICKNAME" "ACCOUNT_TYPE" "NINO_OR_EMPTY" "VRN_OR_EMPTY" "AUTH_CODE" << 'PYEOF'
   import json, os, subprocess, sys

   path = os.path.expanduser('~/.config/hmrc-status/config.json')
   with open(path) as f:
       cfg = json.load(f)

   env = cfg['environment']
   host = 'test-api.service.hmrc.gov.uk' if env == 'sandbox' else 'api.service.hmrc.gov.uk'

   result = subprocess.run([
       'curl', '-sS', '-X', 'POST', f'https://{host}/oauth/token',
       '-H', 'Content-Type: application/x-www-form-urlencoded',
       '--data-urlencode', 'grant_type=authorization_code',
       '--data-urlencode', f'client_id={cfg["client_id"]}',
       '--data-urlencode', f'client_secret={cfg["client_secret"]}',
       '--data-urlencode', 'redirect_uri=urn:ietf:wg:oauth:2.0:oob',
       '--data-urlencode', f'code={sys.argv[5]}',
       '-w', '\n---HTTP:%{http_code}---\n'
   ], capture_output=True, text=True)

   lines = result.stdout.rsplit('\n---HTTP:', 1)
   body = lines[0].strip()
   http_code = lines[1].rstrip('-\n') if len(lines) > 1 else '0'
   if http_code != '200':
       print(f'TOKEN_ERROR: HTTP {http_code} — {body}')
       raise SystemExit(1)

   data = json.loads(body)
   access_token  = data.get('access_token', '')
   refresh_token = data.get('refresh_token', '')
   if not access_token:
       print('TOKEN_ERROR: no access_token in response')
       raise SystemExit(1)

   nickname = sys.argv[1]
   nino = sys.argv[3].replace(' ', '').upper() if sys.argv[3] else None
   vrn  = sys.argv[4].replace(' ', '') or None
   cfg['accounts'][nickname] = {
       'nickname': nickname, 'account_type': sys.argv[2],
       'access_token': access_token, 'refresh_token': refresh_token,
       'nino': nino, 'vrn': vrn,
   }
   with open(path, 'w') as f:
       json.dump(cfg, f, indent=2)
   os.chmod(path, 0o600)
   print('SAVED')
   PYEOF
   ```
   If `TOKEN_ERROR:` is in the output, show it and stop. If `SAVED`, continue.

9. Confirm to the user:
   ```
   Account "{NICKNAME}" added successfully.

   You can now ask:
     "Check my HMRC status"
     "What does my {NICKNAME} account owe HMRC?"
     "When is my {NICKNAME} VAT return due?"
   ```
   If the config already has other accounts: also print
   `Run /hmrc-status:add-account again to link additional accounts.`

## Command: /hmrc-status:reset

Wipes the config file after explicit confirmation.

**Steps:**

1. Check if `~/.config/hmrc-status/config.json` exists:
   ```bash
   test -f ~/.config/hmrc-status/config.json
   ```
   If it does not exist, stop:
   > Nothing to reset — no config file found.

2. Use `AskUserQuestion` with this exact prompt:

   ```
   Reset HMRC skill — are you sure?

   This will permanently delete your config file:
     ~/.config/hmrc-status/config.json

   Everything stored there will be lost:
     • Application credentials (client_id, client_secret)
     • All linked account tokens (access + refresh tokens)
     • Account identifiers (NINO, VRN)

   Type "yes" to confirm, or anything else to cancel:
   ```

3. If the response is exactly `yes` (case-insensitive):
   ```bash
   rm -f ~/.config/hmrc-status/config.json
   ```
   Confirm: `Config removed. Run /hmrc-status:setup to start fresh.`

4. Otherwise:
   > Reset cancelled. Your config is unchanged.

## Workflow

1. **Resolve which account(s) first.** If the user named an account
   (e.g. "my LTD account") or more than one account is found in config or
   env vars, run the *Multi-account resolution* steps under Prerequisites.
   The result is a **list** of resolved suffixes to query — usually one entry
   (empty string for the unsuffixed default account, or a single suffix like
   `_LTD`), but more when the user asked to check `both/all/every` account.
   Every credential read and every URL path built in the remaining steps must
   use the suffix for the account currently being processed.
2. **For each resolved account in the list, repeat steps 3–7.** Run
   per-account steps in parallel where possible (no shared state) and
   produce one labelled report block per account in the final answer
   (use `Default` as the label for the unsuffixed account).
3. Read the credentials the user's question needs (using this account's
   suffix). If anything required is missing for this account, surface
   the message in Prerequisites and skip the rest of this account's
   steps — continue with the next resolved account; do not abort the
   whole run.
4. Pick the endpoint(s) from the table that matches the question. If
   the user asked for a full report, call all relevant endpoints in
   parallel.
5. For each endpoint, use `Bash` to run a curl invocation referring
   to shell variables (so the literal token never appears in
   conversation transcripts or `Bash` command logs). Append
   `-w '\n---HTTP:%{http_code}---\n'` so the HTTP status code is
   appended on its own line. The example below uses `${SUFFIX}` to make
   the multi-account substitution explicit. Bash does not allow nested
   brace expansion, so compose the variable *name* into a holder and
   dereference it with bash indirect expansion `${!holder}`.
   Example shape (add the remaining `Gov-Client-*` / `Gov-Vendor-*`
   headers from the table above to this `curl` invocation):
   ```bash
   SUFFIX=""   # or e.g. "_LTD" for the account resolved in step 1
   TOKEN_VAR="HMRC_ACCESS_TOKEN${SUFFIX}"
   NINO_VAR="HMRC_NINO${SUFFIX}"
   curl -sS -w '\n---HTTP:%{http_code}---\n' \
     -H "Authorization: Bearer ${!TOKEN_VAR}" \
     -H "Accept: application/vnd.hmrc.<v>+json" \
     -H "Gov-Client-Connection-Method: OTHER_DIRECT" \
     "https://api.service.hmrc.gov.uk/accounts/self-assessment/${!NINO_VAR}/balance-and-transactions?onlyOpenItems=true"
   ```
   When credentials come from the config file, load them into shell
   variables via Python before calling curl (never `cat` the config
   file directly). The same indirect-expansion pattern applies to
   VRN — build `VRN_VAR="HMRC_VRN${SUFFIX}"` and reference it as
   `${!VRN_VAR}` in the URL path. Then split the output: everything
   before the `---HTTP:NNN---` sentinel is the JSON body; the
   three-digit code routes the "Handling errors" table.
   Do NOT use `WebFetch`. Never print the expanded token back to the user.
6. Parse the JSON response (e.g. with `jq`, falling back to a Python
   one-liner if `jq` is missing). Map fields to the output format
   below. The exact field names differ between APIs — see the Query
   Type 2 notes and `references/HMRC_ACCOUNT_APIS.md`.
7. If any HTTP error occurs, route the response through the
   "Handling errors" table before continuing. When iterating multiple
   accounts, treat 401/403/4xx as a **per-account** failure: render
   the error message inside that account's report block and continue
   with the remaining resolved accounts.
8. Render a single concise report (do not dump raw JSON). When more
   than one account was resolved in step 1, render one report block
   per account labelled with the suffix (`Default` for the unsuffixed
   account).

## Handling errors

| HTTP | Action |
|------|--------|
| `401` `INVALID_BEARER_TOKEN` | First check if the account's `refresh_token` is available (either in `~/.config/hmrc-status/config.json` under the resolved account, or as `HMRC_REFRESH_TOKEN[_SUFFIX]` env var). If available, automatically attempt a token refresh using the refresh endpoint (see `references/AUTH.md` §2.4): use the `client_id` and `client_secret` from config (or env vars `HMRC_CLIENT_ID`/`HMRC_CLIENT_SECRET`), call `POST https://{host}/oauth/token` with `grant_type=refresh_token`, then update `access_token` (and `refresh_token` if rotated) in the config file using Python, and **retry the original request once**. If the refresh also returns `401` or `400`, or no refresh token is available, stop and tell the user: "Your `HMRC_ACCESS_TOKEN` is expired and the refresh attempt failed (or no refresh token is stored). Re-authorise by running `/hmrc-status:add-account` again." |
| `403` | Inspect the JSON body's `code` / `message`. If it mentions `INSUFFICIENT_SCOPE` or names a scope, the token is missing a scope — tell the user which (`read:self-assessment` or `read:vat`) and to re-authorise via `/hmrc-status:add-account`. If it mentions `Gov-Client-*` headers or `MISSING_HEADER` / `INVALID_HEADER`, the fraud-prevention headers were rejected — surface the offending header name and instruct the user to re-check the sourcing recipes above. Do not blindly recommend re-authorisation for header errors. |
| `404` | Inspect the JSON body's `code`. If it is `NO_DATA_FOUND` (or a generic "no data" message), treat as "no records for this period" and report that — **except during the VAT liabilities backward scan, where a per-window `NO_DATA_FOUND` is an empty window and the scan continues.** If it is `MATCHING_RESOURCE_NOT_FOUND` (or the `message` indicates the NINO/VRN itself was not found), stop and tell the user the configured NINO/VRN does not match an HMRC account — likely a typo or wrong-environment token. |
| `406` | Wrong `Accept` version — fix the call. |
| `429` | Wait 5 seconds (`sleep 5`) and retry the same call once. If it still returns 429, stop and tell the user HMRC is rate-limiting the app — try again in a few minutes. |
| `5xx` | Tell the user HMRC is having a platform issue and to retry later. |

## Output format

When the user asks for a full status report, format exactly like this
(omit sections the user has no identifiers for):

```
HMRC Account Status (as of YYYY-MM-DD)
──────────────────────────────────────

Self Assessment                                              ← balance + payment lines come from balance-and-transactions; Outstanding comes from the obligations API
  Balance owed:  £<payableAmount>            ← currently payable [⚠️ OVERDUE when balanceDetails.overdueAmount > 0 — append " (£<overdueAmount> overdue since <earliestPaymentDateOverdue>)"]
  Next payment:  £<payableAmount> due <payableDueDate> (<description>)
                 ← `<description>` source: take `documentDetails[]` entries
                   where `documentDueDate == payableDueDate`. If multiple match,
                   prefer the one with `outstandingAmount > 0`; if still multiple,
                   join their `documentText` values with `, `. If none match,
                   omit the parenthetical entirely — do **not** fabricate a label.
  Outstanding:   <taxYear> return — due <dueDate> [⚠️ OVERDUE when the obligation's dueDate < today and status == "open"]
                 ← repeat the `Outstanding:` line once per open obligation across crystallisation + income-and-expenditure, sorted by dueDate ascending

VAT                                                          ← Balance owed + Next payment come from /liabilities (across all 365-day windows); Next return comes from /obligations
  Balance owed:  £<sum of outstandingAmount across all windows>
  Next payment:  £<earliest unpaid liability's outstandingAmount> due <that item's due>
  Next return:   Period <start> – <end>, due <due>
                 ← repeat the `Next return:` line once per open VAT obligation, sorted by `due` ascending
```

Empty / zero-state rules:

- **No outstanding charges** for Self Assessment means `balanceDetails.payableAmount == 0`. Render `Balance owed: £0.00`. **Before omitting `Next payment:`, also check the upcoming-charge fields**: `pendingChargeDueAmount` / `pendingChargeDueDate`, then `firstPendingAmountRequested` / `secondPendingAmountRequested`. Pair each amount with the API-provided date only. For `secondPendingAmountRequested`, only render the line if the response carries a corresponding API date field; do **not** invent a date. If the date is missing, render `Next payment: £<amount> — second payment on account (date not returned by the API; check the HMRC web account)`. If multiple upcoming-charge fields are > 0, render one `Next payment:` line per non-zero field, sorted by date ascending. Only when all upcoming-charge fields are 0 may you omit `Next payment:` entirely.
- **No outstanding VAT charges** means every VAT liability across all 365-day windows has `outstandingAmount == 0`. Render `Balance owed: £0.00` and omit `Next payment:` for VAT.
- **No outstanding obligations** (`obligations: []` or every entry has `status` ≠ `open`/`O`): render `Outstanding: none — all returns filed` for Self Assessment, or `Next return: none — all VAT returns filed` for VAT.
- **Multiple open obligations**: render one `Outstanding:` / `Next return:` line per obligation, sorted by `dueDate` (Self Assessment) or `due` (VAT) ascending. Do not collapse them.
- **Tax year string for Self Assessment** is derived from the obligation's `periodStartDate` — `periodStartDate` of `2025-04-06` becomes `2025-26`. (HMRC tax years run 6 April → 5 April.)

For a single-question answer (e.g. "what's my VAT balance?"), respond
with a one-line summary plus the supporting figure; don't print the
whole template.

Currency: always show GBP with `£` prefix, comma thousands separators,
and two decimal places (e.g. `£1,250.00`).
Dates: render every date the user sees as `DD MMM YYYY` (e.g. `31 Jan 2026`).
The only place ISO `YYYY-MM-DD` is used is the `(as of …)` report header timestamp.

## Privacy

NEVER store tokens, NINOs, VRNs, client secrets, or response bodies on disk
during the conversation (the config file is written only by the setup commands,
not during normal query runs). Don't echo the full access token back to the
user. When reading credentials in Bash, always use Python to parse the config
JSON and assign to shell vars without printing values. This skill is intended
to be open-source and must not capture personal tax data in logs, commits, or
example files.

## References

- `references/HMRC_ACCOUNT_APIS.md` — endpoint schemas, sample responses,
  full header list, error codes
- `references/AUTH.md` — how to register an app and obtain an access
  token (manual instructions and background)
