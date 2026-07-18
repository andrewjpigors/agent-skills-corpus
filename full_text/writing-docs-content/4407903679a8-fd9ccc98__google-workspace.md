---
name: google-workspace
description: "Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python."
version: 1.0.1
author: Nous Research
license: MIT
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials (downloaded from Google Cloud Console)
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, Email, OAuth]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace

Gmail, Calendar, Drive, Contacts, Sheets, and Docs — through Hermes-managed OAuth and a thin CLI wrapper. When `gws` is installed, the skill uses it as the execution backend for broader Google Workspace coverage; otherwise it falls back to the bundled Python client implementation.

## References

- `references/gmail-search-syntax.md` — Gmail search operators (is:unread, from:, newer_than:, etc.)
- `references/pickle-oauth-alternative.md` — Alternative pickle-based OAuth flow for when the user pastes raw credentials JSON (Desktop app type) and runs auth locally
- `references/selva-accounts.md` — Selva Partners token map (audited May 2026), account→pickle mapping, OAuth consolidation plan, diagnostic snippets for inspecting pickle token state, signature state, org logo notes, scope requirements per task
- `references/substack-login-setup-pitfalls.md` — Substack sign-in/setup pitfalls: remote browser vs iPhone sessions, magic-link/code handling, and fallback to guided manual setup.
- `references/selva-sheets-pricing-engine.md` — Selva/Cosecha Google Sheets pricing engine pattern: Growers Price List → SKU matrix → tiered client price lists, direct OAuth-pickle Sheets API usage, formula pitfalls, and concise business update style
- `references/tiller-family-budget-workflow.md` — Tiller/Google Sheets workflow for building household budget OS, normalized P&L, cash-flow tabs, cut plan, and categorization rules while avoiding transfer/credit-card double-counting

## Templates

- `templates/selva_signature_lorenzo.html` — Selva Partners branded HTML email signature template. Replace `{{NAME}}`, `{{TITLE}}`, `{{PHONE}}`, `{{EMAIL}}` to create signatures for other accounts. Includes embedded base64 logo (80x80px), gold border, dark green/gold color scheme.
- `references/selva-gmail-accounts.md` — Selva Partners account/token map, re-auth recipe for Chloe, signature substitution table, org logo specs

## Scripts

- `scripts/setup.py` — OAuth2 setup (run once to authorize)
- `scripts/google_api.py` — compatibility wrapper CLI. It prefers `gws` for operations when available, while preserving Hermes' existing JSON output contract.

## First-Time Setup

The setup is fully non-interactive — you drive it step by step so it works
on CLI, Telegram, Discord, or any platform.

Define a shorthand first:

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
```

### Step 0: Check if already set up

```bash
$GSETUP --check
```

If it prints `AUTHENTICATED`, skip to Usage — setup is already done.

### Step 1: Triage — ask the user what they need

Before starting OAuth setup, ask the user TWO questions:

**Question 1: "What Google services do you need? Just email, or also
Calendar/Drive/Sheets/Docs?"**

- **Email only** → They don't need this skill at all. Use the `himalaya` skill
  instead — it works with a Gmail App Password (Settings → Security → App
  Passwords) and takes 2 minutes to set up. No Google Cloud project needed.
  Load the himalaya skill and follow its setup instructions.

- **Email + Calendar** → Continue with this skill, but use
  `--services email,calendar` during auth so the consent screen only asks for
  the scopes they actually need.

- **Calendar/Drive/Sheets/Docs only** → Continue with this skill and use a
  narrower `--services` set like `calendar,drive,sheets,docs`.

- **Full Workspace access** → Continue with this skill and use the default
  `all` service set.

**Question 2: "Does your Google account use Advanced Protection (hardware
security keys required to sign in)? If you're not sure, you probably don't
— it's something you would have explicitly enrolled in."**

- **No / Not sure** → Normal setup. Continue below.
- **Yes** → Their Workspace admin must add the OAuth client ID to the org's
  allowed apps list before Step 4 will work. Let them know upfront.

### Step 2: Create OAuth credentials (one-time, ~5 minutes)

Tell the user:

> You need a Google Cloud OAuth client. This is a one-time setup:
>
> 1. Create or select a project:
>    https://console.cloud.google.com/projectselector2/home/dashboard
> 2. Enable the required APIs from the API Library:
>    https://console.cloud.google.com/apis/library
>    Enable: Gmail API, Google Calendar API, Google Drive API,
>    Google Sheets API, Google Docs API, People API
> 3. Create the OAuth client here:
>    https://console.cloud.google.com/apis/credentials
>    Credentials → Create Credentials → OAuth 2.0 Client ID
> 4. Application type: "Desktop app" → Create
> 5. If the app is still in Testing, add the user's Google account as a test user here:
>    https://console.cloud.google.com/auth/audience
>    Audience → Test users → Add users
> 6. Download the JSON file and tell me the file path
>
> Important Hermes CLI note: if the file path starts with `/`, do NOT send only the bare path as its own message in the CLI, because it can be mistaken for a slash command. Send it in a sentence instead, like:
> `The JSON file path is: /home/user/Downloads/client_secret_....json`

Once they provide the path:

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

If they paste the raw client ID / client secret values instead of a file path,
write a valid Desktop OAuth JSON file for them yourself, save it somewhere
explicit (for example `~/Downloads/hermes-google-client-secret.json`), then run
`--client-secret` against that file.

### Step 3: Get authorization URL

Use the service set chosen in Step 1. Examples:

```bash
$GSETUP --auth-url --services email,calendar --format json
$GSETUP --auth-url --services calendar,drive,sheets,docs --format json
$GSETUP --auth-url --services all --format json
```

This returns JSON with an `auth_url` field and also saves the exact URL to
`~/.hermes/google_oauth_last_url.txt`.

Agent rules for this step:
- Extract the `auth_url` field and send that exact URL to the user as a single line.
- Tell the user that the browser will likely fail on `http://localhost:1` after approval, and that this is expected.
- Tell them to copy the ENTIRE redirected URL from the browser address bar.
- If the user gets `Error 403: access_denied`, send them directly to `https://console.cloud.google.com/auth/audience` to add themselves as a test user.

### Step 4: Exchange the code

The user will paste back either a URL like `http://localhost:1/?code=4/0A...&scope=...`
or just the code string. Either works. The `--auth-url` step stores a temporary
pending OAuth session locally so `--auth-code` can complete the PKCE exchange
later, even on headless systems:

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED" --format json
```

If `--auth-code` fails because the code expired, was already used, or came from
an older browser tab, it now returns a fresh `fresh_auth_url`. In that case,
immediately send the new URL to the user and have them retry with the newest
browser redirect only.

### Step 5: Verify

```bash
$GSETUP --check
```

Should print `AUTHENTICATED`. Setup is complete — token refreshes automatically from now on.

### Notes

- Token is stored at `~/.hermes/google_token.json` and auto-refreshes.
- Pending OAuth session state/verifier are stored temporarily at `~/.hermes/google_oauth_pending.json` until exchange completes.
- If `gws` is installed, `google_api.py` points it at the same `~/.hermes/google_token.json` credentials file. Users do not need to run a separate `gws auth login` flow.
- To revoke: `$GSETUP --revoke`

## Usage

All commands go through the API script. Set `GAPI` as a shorthand:

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

### Gmail

```bash
# Search (returns JSON array with id, from, subject, date, snippet)
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"

# Read full message (returns JSON with body text)
$GAPI gmail get MESSAGE_ID

# Send
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1><p>Details...</p>" --html
$GAPI gmail send --to user@example.com --subject "Hello" --from '"Research Agent" <user@example.com>' --body "Message text"

# Reply (automatically threads and sets In-Reply-To)
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail reply MESSAGE_ID --from '"Support Bot" <user@example.com>' --body "Thanks"

# Labels
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

### Calendar

```bash
# List events (defaults to next 7 days)
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# Create event (ISO 8601 with timezone required)
$GAPI calendar create --summary "Team Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar create --summary "Lunch" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Cafe"
$GAPI calendar create --summary "Review" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"

# Delete event
$GAPI calendar delete EVENT_ID
```

### Drive

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
```

### Contacts

```bash
$GAPI contacts list --max 20
```

### Sheets

```bash
# Read
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

# Write
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# Append rows
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

#### Selva/Cosecha pricing workbooks

When building or repairing a Selva/Cosecha pricing workbook, load `references/selva-sheets-pricing-engine.md` first. Key rules:
- Use **Growers Price List** terminology.
- Mark missing cost/pack data as `Needs Quote`; do not invent grower COGS or unit counts.
- Verify both formulas (`valueRenderOption='FORMULA'`) and rendered values.
- Guard tier case-price formulas against blank inputs so missing prices show blank, not `$0.00`.
- If `gws` credentials are missing, direct Sheets API via Lorenzo's Selva OAuth pickle is acceptable; never expose credential contents.

#### Tiller / household budget workbooks

When asked to analyze a Tiller Sheet and create a family budget, cash-flow view, or P&L, load `references/tiller-family-budget-workflow.md` before writing. Key rules:
- Read metadata and sample rows from `Transactions`, `Categories`, `Balances`, and `Accounts` first.
- Create new analysis tabs instead of altering source Tiller tabs unless explicitly requested.
- For a normalized P&L, exclude bank transfers and credit-card payment mechanics to avoid double-counting; show them separately in cash-flow analysis.
- Month headers like `2026-01` must be treated as text, not currency/date serials.

### Docs

```bash
$GAPI docs get DOC_ID
```

### Substack / magic-link login emails

For Substack and similar passwordless flows, clicking the email link in the user's local browser does **not** authenticate the remote/browser tool session. If the task requires the browser tool to be logged in, the sign-in link must be opened inside that same remote browser session.

Workflow:
1. Trigger the login email to the correct known account; check memory before asking the user to repeat an email address.
2. Search Gmail for recent `from:substack` login messages and inspect snippets/headers first.
3. If the page has no code input and only says "Check your email", ask for the temporary sign-in link to be pasted, or retrieve/open the link in the remote browser if tooling succeeds.
4. Do not expose magic-link URLs in final summaries; treat them as sensitive temporary credentials.
5. If a Gmail extraction command times out and the tool marks it blocked, do not retry the same command shape. Switch strategy or ask the user for the link.

### Gmail Signatures (sendAs API)
The `google_api.py` wrapper does not expose signatures — use the Gmail API directly via Python pickle token:

```python
import pickle, warnings
warnings.filterwarnings('ignore')
from googleapiclient.discovery import build

with open('/Users/lorenzobelpassi/.hermes/selva_outreach_token.pickle', 'rb') as f:
    creds = pickle.load(f)
service = build('gmail', 'v1', credentials=creds)

# Read all send-as aliases and their signatures
sigs = service.users().settings().sendAs().list(userId='me').execute()
for sa in sigs.get('sendAs', []):
    print(sa.get('sendAsEmail'), len(sa.get('signature', '')), 'chars')

# Update a signature
service.users().settings().sendAs().patch(
    userId='me',
    sendAsEmail='user@selva-partners.com',
    body={'signature': '<html>...signature HTML...</html>'}
).execute()
```

**Tokens for Selva accounts:**
- Lorenzo (lorenzo.belpassi@selva-partners.com): `~/.hermes/selva_outreach_token.pickle`
- Chloe (chloe.sanchez@selva-partners.com): `~/.hermes/chloe_outreach_token.pickle`
- Both use project `selva-outreach`, credentials at `~/.hermes/selva_outreach_credentials.json`
- `chloe.lorenzob1987@gmail.com` is RETIRED — consolidated into chloe.sanchez@selva-partners.com
- Old tokens (gmail_token.pickle, personal_gmail_token.pickle, selva_gmail_token.pickle) are abandoned — do not use

**Python version note:** On Lorenzo's Mac, `python3` resolves to `/usr/bin/python3` (3.9.6) — this is the one with google packages installed (via pip3 in Library/Python/3.9). `python3.9` and `python3.11` as explicit commands do NOT exist. Always use `python3`.

**Signature structure for Lorenzo (selva-partners.com):**
Rich HTML table with:
- Embedded base64 PNG logo (Selva Partners, 80x80px)
- Gold left border (rgb(184,134,11))
- Name, title, phone, email, website
- Color scheme: dark green (rgb(45,66,51)), gold, grey

When copying a signature to another account, preserve the full HTML but update name, title, email fields only.

## Output Format

All commands return JSON. Parse with `jq` or read directly. Key fields:

- **Gmail search**: `[{id, threadId, from, to, subject, date, snippet, labels}]`
- **Gmail get**: `{id, threadId, from, to, subject, date, labels, body}`
- **Gmail send/reply**: `{status: "sent", id, threadId}`
- **Calendar list**: `[{id, summary, start, end, location, description, htmlLink}]`
- **Calendar create**: `{status: "created", id, summary, htmlLink}`
- **Drive search**: `[{id, name, mimeType, modifiedTime, webViewLink}]`
- **Contacts list**: `[{name, emails: [...], phones: [...]}]`
- **Sheets get**: `[[cell, cell, ...], ...]`

## Rules

1. **Never send email or create/delete events without confirming with the user first.** Show the draft content and ask for approval.
2. **Check auth before first use** — run `setup.py --check`. If it fails, guide the user through setup.
3. **Use the Gmail search syntax reference** for complex queries — load it with `skill_view("google-workspace", file_path="references/gmail-search-syntax.md")`.
4. **Calendar times must include timezone** — always use ISO 8601 with offset (e.g., `2026-03-01T10:00:00-06:00`) or UTC (`Z`).
5. **Respect rate limits** — avoid rapid-fire sequential API calls. Batch reads when possible.

## Alternative: Pickle-based Local OAuth (user pastes credentials JSON)

When the user pastes raw credentials JSON (Desktop app type) directly into chat and prefers to run the auth flow locally in their terminal (browser opens on their machine), use this pattern instead of the gws setup flow:

1. Save credentials to `~/.hermes/gmail_credentials.json`
2. Write and run `~/.hermes/gmail_auth.py` (see `references/pickle-oauth-alternative.md`)
3. User runs `python3 ~/.hermes/gmail_auth.py` in their terminal — browser opens, they sign in
4. Token saved to `~/.hermes/gmail_token.pickle`

**Important:** Each time you add new scopes, you must delete the old token and re-run auth:
```bash
rm ~/.hermes/gmail_token.pickle
python3 ~/.hermes/gmail_auth.py
```

**Scope expansion pattern (confirmed working):** When the user wants to add services (e.g. "add Calendar and Drive"), update the SCOPES list in the auth script, delete the pickle token, and ask the user to re-run auth locally. Do NOT try to re-run auth from within the agent — it opens a browser and will timeout.

**API enablement required:** OAuth scopes alone aren't enough. Each Google API must be explicitly enabled in the Cloud project at https://console.developers.google.com/apis/api/APINAME/overview?project=PROJECT_ID. A 403 `accessNotConfigured` error means the API is not enabled — send the user the direct enable link.

**Service account vs OAuth (important distinction):**
- OAuth (`installed` or `web` type credentials) = user login flow, requires browser, token stored in pickle/json. Use for interactive user-facing agents.
- Service account (`"type": "service_account"`) = unattended background agents, no browser needed, authenticates as a bot identity. Required for scheduled/cron jobs like the Deal Log Agent.
- When a user pastes `{"web": {...}}` credentials for an unattended workflow, flag it immediately — they need a service account key instead. Direct them to console.cloud.google.com/iam-admin/serviceaccounts.
- Service account email (e.g. `agent@project.iam.gserviceaccount.com`) must be shared on any Drive folders/Docs/Sheets it needs to access, just like sharing with a person.
- Store service account JSON as an env var (`GOOGLE_SERVICE_ACCOUNT_JSON`) by serializing with `json.dumps()` — avoid multiline values in .env files.
- **Google Workspace orgs may block service account key creation** via `iam.disableServiceAccountKeyCreation` org policy. When you see "An Organization Policy that blocks service account key creation has been enforced", fall back to OAuth pickle token if it already has the required scopes. For Lorenzo (chloe-lorenzob1987-org), this policy is enforced — always use the OAuth token at `~/.hermes/gmail_token.pickle`.

APIs that commonly need enabling beyond Gmail:
- `drive.googleapis.com`
- `calendar-json.googleapis.com`
- `docs.googleapis.com`
- `sheets.googleapis.com`
- `slides.googleapis.com`
- `people.googleapis.com` (Contacts)

## Gmail Personal Account OAuth Notes

- Workspace-internal OAuth apps (e.g. a project under `selva-partners.com` with an Internal consent screen) cannot authorize consumer Gmail accounts like `lorenzo.belpassi@gmail.com`. If the user says the Gmail is not under the Workspace domain, switch to an External/test-user OAuth app or a project created under a personal Google account.
- For Lorenzo's personal Gmail Natoora search, use token path `~/.hermes/personal_gmail_token.pickle` when available. If authorizing it, do not reuse `selva_outreach_credentials.json` if it is internal-only; use an external-capable credentials file such as `~/.hermes/gmail_credentials.json` and add `lorenzo.belpassi@gmail.com` as a test user if the app is in Testing.
- Keep personal Gmail search/read workflows separate from Selva Workspace accounts: personal Gmail may contain historic Natoora correspondence; Selva Workspace tokens are for active Selva outreach.

## Multiple Google Accounts (e.g. personal + work email)

**OAuth app scope restrictions:** Internal OAuth apps (consent screen set to "Internal") only work for accounts within that Google Workspace org. If the user tries to auth a personal Gmail against an org-internal OAuth app, it will fail with access denied.

**Solution:** Use credentials from a project with "External" user type:
- `~/.hermes/gmail_credentials.json` (from project selva-495405, chloe.lorenzob1987@gmail.com) allows external accounts
- `~/.hermes/selva_outreach_credentials.json` (from selva-partners.com org) is Internal-only

**Lorenzo's personal Gmail token:**
- Account: `lorenzo.belpassi@gmail.com`
- Token: `~/.hermes/personal_gmail_token.pickle`
- Auth script: `~/.hermes/personal_gmail_auth.py`
- Uses gmail_credentials.json (External app)

When the user needs to authorize a second Google account (e.g. a work email like `lorenzo.belpassi@selva-partners.com` in addition to a personal Gmail):

1. Save a separate token file per account — e.g. `~/.hermes/selva_gmail_token.pickle`
2. Use the same credentials JSON (`~/.hermes/gmail_credentials.json`) but a different auth script that writes to the new token path
3. The OAuth app must list the second email as a test user (or be published) — go to https://console.cloud.google.com/auth/audience?project=PROJECT_ID → Test users → Add
4. Error `Error 403: access_denied` with "app is currently being tested" = the email is not in the test users list

**Internal consent screen for Google Workspace orgs:**
If the user owns a Google Workspace org (e.g. selva-partners.com), set the OAuth consent screen to "Internal" instead of "External". Internal apps:
- Skip the verification process entirely
- Are immediately available to all users in the org
- Don't need test users added manually
Go to: APIs & Services → OAuth consent screen → User type → Internal

**GCP project creation under a Workspace org may require folder permissions:**
When the user tries to create a GCP project under their org and sees `resourcemanager.folders.create`, they need the `resourcemanager.projects.create` permission at the org level, NOT folder creation. Tell them to:
1. Go to console.cloud.google.com → New Project
2. Under "Location", select the org name (e.g. `selva-partners.com`) directly — NOT a subfolder
3. If still blocked, an org super admin needs to grant `roles/resourcemanager.projectCreator` at the org level

**Lorenzo's selva-outreach project (May 2026):**
- Project ID: `selva-outreach`
- Created under `selva-partners.com` org
- Credentials JSON: `~/.hermes/selva_outreach_credentials.json`
- Token: `~/.hermes/selva_outreach_token.pickle`
- Auth script: `~/.hermes/selva_outreach_auth.py`
- Sends from: `lorenzo.belpassi@selva-partners.com`
- APIs enabled: Gmail, Drive, Docs, Sheets, Calendar, Contacts, Slides
- Full scopes: gmail.send, gmail.readonly, gmail.modify, gmail.settings.basic, calendar, drive, documents, spreadsheets, contacts

**Re-auth preference (Lorenzo):** When tokens expire or scopes need expanding, keep the same pickle filename — do NOT change token paths or agent wiring. Minimal disruption means only the token content changes, nothing downstream needs updating.

**Chloe's selva-partners.com account (May 2026):**
- Token: `~/.hermes/chloe_outreach_token.pickle`
- Sends from: `chloe.sanchez@selva-partners.com`
- Uses same credentials JSON: `~/.hermes/selva_outreach_credentials.json`
- Scopes: gmail.send, gmail.readonly, gmail.modify, gmail.settings.basic — all correct, token is valid

**Python version for Google API scripts:**
- Use `python3` (resolves to /usr/bin/python3, version 3.9.6) — NOT python3.9 or python3.11
- Google packages installed at /Users/lorenzobelpassi/Library/Python/3.9/lib/python/site-packages
- FutureWarning spam about Python 3.9 EOL is normal — suppress with warnings.filterwarnings('ignore')

**Gmail API must be enabled separately per project.** Even if Drive is enabled, Gmail needs its own enablement at:
  https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=PROJECT_ID

## Gmail Signature Management

Signatures are set per send-as alias via the Gmail Settings API.

```python
import pickle, warnings
warnings.filterwarnings('ignore')
from googleapiclient.discovery import build

with open('/path/to/token.pickle', 'rb') as f:
    creds = pickle.load(f)
service = build('gmail', 'v1', credentials=creds)

# Read current signature
sigs = service.users().settings().sendAs().list(userId='me').execute()
sig = sigs['sendAs'][0]['signature']  # HTML string

# Set/update signature
service.users().settings().sendAs().patch(
    userId='me',
    sendAsEmail='user@selva-partners.com',
    body={'signature': new_sig_html}
).execute()
```

**Required scope:** `gmail.settings.basic` — without it you get 403 "Insufficient Permission". Check token scopes with:
```python
with open('token.pickle', 'rb') as f: creds = pickle.load(f)
print(creds.scopes)
```

**Selva Partners signature template:** Lorenzo's signature is a rich HTML table with:
- Base64-encoded logo PNG (80x80px), left column
- Gold left border divider (rgb(184,134,11))
- Right column: name (bold, dark green), title (italic gray), SELVA PARTNERS (bold), tagline, phone, email, website
- To create Chloe's version: copy Lorenzo's sig HTML and replace name/title/email fields only
- Same logo, same styling, just different personal details

## Google Workspace Org Logo

Location: admin.google.com/ac/accountsettings > Personalization section > Logo row

**Requirements:**
- Size: 320x132 pixels
- Format: PNG or GIF
- Max file size: 30KB
- Aspect ratio must match — wrong ratio causes the logo to appear smushed/squished in the Google app header bar

To update: click the logo row in Personalization, upload the correctly-sized file.

## Gmail Signature Management

Use the Gmail API `sendAs` resource to read and write signatures programmatically.

```python
import pickle, warnings
warnings.filterwarnings('ignore')
from googleapiclient.discovery import build

with open('/Users/lorenzobelpassi/.hermes/selva_outreach_token.pickle', 'rb') as f:
    creds = pickle.load(f)
service = build('gmail', 'v1', credentials=creds)

# Read signatures
sigs = service.users().settings().sendAs().list(userId='me').execute()
for sa in sigs.get('sendAs', []):
    print(sa.get('sendAsEmail'), len(sa.get('signature', '')), 'chars')

# Write/update signature
service.users().settings().sendAs().patch(
    userId='me',
    sendAsEmail='user@selva-partners.com',
    body={'signature': '<html>...</html>'}
).execute()
```

**Required scope:** `https://www.googleapis.com/auth/gmail.settings.basic`
If you get `HttpError 403: Insufficient Permission` on sendAs, the token is missing this scope — re-auth with it added (see PKCE pitfall below).

**Copying a signature between accounts:** Extract from source account, do string replacements for name/title/email, patch to destination account. The Selva Partners signature embeds the logo as a base64 PNG inline — no external hosting needed.

**Selva Partners signature fields to swap when copying Lorenzo → Chloe:**
- `>Lorenzo Belpassi<` → `>Chloe Sanchez<`
- `>Founder &amp; Managing Partner<` → `>Executive Assistant<`
- `mailto:lorenzo@selva-partners.com` → `mailto:chloe.sanchez@selva-partners.com`
- `>lorenzo@selva-partners.com<` → `>chloe.sanchez@selva-partners.com<`

## Google Workspace Org Logo

The org logo (shown in Gmail/Admin header) is set at:
admin.google.com → Account settings → Personalization → Logo

**Required dimensions:** 320x132px, PNG or GIF, max 30KB. The logo must be landscape-ratio or it will appear squished/smushed.

**To prepare the logo from the base64 in Lorenzo's signature:**
```python
from PIL import Image
import base64, re

# Extract from signature HTML
match = re.search(r'data:image/png;base64,([^\"]+)', sig)
img_data = base64.b64decode(match.group(1))
with open('/tmp/selva_logo_original.png', 'wb') as f:
    f.write(img_data)

# Resize to 320x132 with transparent padding
img = Image.open('/tmp/selva_logo_original.png').convert('RGBA')
target_w, target_h = 320, 132
scale = min(target_w / img.width, target_h / img.height)
resized = img.resize((int(img.width * scale), int(img.height * scale)), Image.LANCZOS)
canvas = Image.new('RGBA', (target_w, target_h), (0, 0, 0, 0))
canvas.paste(resized, ((target_w - resized.width) // 2, (target_h - resized.height) // 2), resized)
canvas.save('/tmp/selva_logo_320x132.png')
```
Upload the result manually at admin.google.com — there is no API for org logo upload.

## OAuth Re-auth Pitfall: PKCE Code Verifier

When adding new scopes to an existing token, generate the auth URL **without PKCE** to avoid `invalid_grant: Missing code verifier` errors during exchange. The `InstalledAppFlow` library may generate a code_challenge but not preserve the verifier across the exchange call.

**Safe approach — build the URL manually without PKCE:**
```python
import urllib.parse

params = {
    'response_type': 'code',
    'client_id': CLIENT_ID,
    'redirect_uri': 'http://localhost:1',
    'scope': ' '.join(SCOPES),
    'access_type': 'offline',
    'prompt': 'consent',
}
url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode(params)
print(url)
```

Then exchange with curl immediately after getting the code (codes expire in ~60 seconds):
```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "code=CODE_HERE" \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:1" \
  -d "grant_type=authorization_code"
```

Then save the returned token as a pickle. The redirect to localhost:1 will show ERR_UNSAFE_PORT — that's expected, just copy the full URL from the address bar.

## python3 Version Note

On Lorenzo's machine, `python3` = Python 3.9.6 at `/usr/bin/python3`. Google packages are installed via pip3 (python3.9) at `/Users/lorenzobelpassi/Library/Python/3.9/`. Use `python3` not `python3.9` or `python3.11` — only 3.9 has the google packages. Suppress FutureWarning noise with `warnings.filterwarnings('ignore')`.

## Gmail Signatures via API

**10,000 character limit:** Gmail API enforces a 10K char limit on signatures set via `sendAs.patch()`. Signatures with base64-embedded images will exceed this. Fix: replace the `data:image/...;base64,...` src with an external public URL (hosted on the website, Drive public link, etc.).

**To extract and rebuild a signature for a second user:**
1. Fetch the source account's signature via `sendAs().list()`
2. String-replace name, title, email href and link text
3. If base64 image present, swap for external URL before pushing
4. Push via `sendAs().patch(userId='me', sendAsEmail='...', body={'signature': html})`

**Required scope for signature writes:** `gmail.settings.basic` — this is NOT included in standard gmail send/read/modify scopes. If you get `403 Insufficient Permission` on sendAs, the token needs re-auth with this scope added.

**Re-auth without PKCE (simpler, avoids "Missing code verifier" errors):**
Build the auth URL manually with `urllib.parse.urlencode` instead of using `InstalledAppFlow.authorization_url()` — the flow library adds PKCE by default and the verifier doesn't survive across calls. Then exchange the code directly with curl:
```bash
curl -s -X POST https://oauth2.googleapis.com/token \
  -d "code=CODE" \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "redirect_uri=http://localhost:1" \
  -d "grant_type=authorization_code"
```
Then build a `google.oauth2.credentials.Credentials` object from the response and pickle it.

**Delivering signatures when API push fails:** If the signature exceeds 10K and no external image URL is available yet, save the HTML to `~/Desktop/name_signature.html` and tell the user to open it in a browser, Cmd+A, Cmd+C, then paste into Gmail Settings -> Signature. The embedded base64 image renders correctly when pasted this way.

**Lorenzo preference:** When a programmatic path hits repeated friction (auth loops, API limits), skip debugging and deliver the output directly — file on Desktop, copy-paste instructions. Don't persist through a third attempt.

**Outbound Gmail API signature behavior:** Gmail API `messages.send` does **not** automatically append the user's Gmail UI signature. For Lorenzo's Selva outbound campaigns, fetch the current HTML signature via `users.settings.sendAs.list()` and append it manually to the message body, or use a plain-text fallback if sending text-only. Verify website links before using them in signatures: `selva-partners.com` failed DNS in May 2026, while `selvapartners.co` resolved successfully (`Selva Partners | Hospitality Advisory & Consulting`).

## Google Workspace Org Logo

- Required dimensions: **320x132px**, PNG or GIF, max 30KB
- Upload location: admin.google.com -> Account settings -> Personalization -> Logo
- To resize an existing logo: extract base64 from signature, decode, resize with Pillow to 320x132 (letterbox with transparent padding), save as PNG
- The logo in the admin console header is org-wide — one logo for all accounts

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `NOT_AUTHENTICATED` | Run setup Steps 2-5 above |
| `REFRESH_FAILED` | Token revoked or expired — redo Steps 3-5 |
| `HttpError 403: Insufficient Permission` | Missing API scope — `$GSETUP --revoke` then redo Steps 3-5 |
| `HttpError 403: Access Not Configured` | API not enabled — user needs to enable it in Google Cloud Console |
| `google_api.py` fails with `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'` | You're hitting Python 3.9 with a wrapper that uses 3.10 union syntax. For Drive/file lookup, first check whether the file is already local and use `mdfind` + local readers (`openpyxl`, docx unzip, etc.); otherwise use a small direct Python snippet against the OAuth pickle token instead of the wrapper. |
| `ModuleNotFoundError` | Run `$GSETUP --install-deps` |
| Advanced Protection blocks auth | Workspace admin must allowlist the OAuth client ID |
| `Signature exceeds maximum length of 10000 characters` | Base64 image in sig — replace with external URL or deliver as HTML file |
| `invalid_grant: Missing code verifier` | PKCE verifier lost between calls — skip InstalledAppFlow, build auth URL manually and exchange with curl |
| `invalid_grant: Missing code verifier` | PKCE mismatch — use manual URL without code_challenge (see above) |
| `invalid_grant: Bad Request` on curl exchange | Auth code expired (60s TTL) — generate a fresh URL and exchange immediately |
| Advanced Protection blocks auth | Workspace admin must allowlist the OAuth client ID |
| `Request had insufficient authentication scopes` on Gmail settings | Token is missing `gmail.settings.basic`. Re-auth with that scope added. See Gmail Signature Workflow below. |

## Gmail Signature Workflow (Selva Partners)

Accounts: `lorenzo.belpassi@selva-partners.com` (token: `selva_outreach_token.pickle`) and `chloe.sanchez@selva-partners.com` (token: `chloe_outreach_token.pickle`).

### Required scopes for signature management

```
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.settings.basic   ← REQUIRED for sendAs patch
```

If `chloe_outreach_token.pickle` only has send/read/modify scopes, re-auth is needed. Generate URL with `InstalledAppFlow` using `selva_outreach_credentials.json` and `redirect_uri='http://localhost:1'`, exchange the code, overwrite the pickle.

### Copy Lorenzo's signature to Chloe (pattern)

```python
import pickle, warnings
warnings.filterwarnings('ignore')
from googleapiclient.discovery import build

# 1. Pull Lorenzo's signature
with open('/Users/lorenzobelpassi/.hermes/selva_outreach_token.pickle', 'rb') as f:
    creds = pickle.load(f)
service = build('gmail', 'v1', credentials=creds)
sigs = service.users().settings().sendAs().list(userId='me').execute()
lorenzo_sig = sigs['sendAs'][0]['signature']

# 2. Substitute Chloe's details
chloe_sig = lorenzo_sig
chloe_sig = chloe_sig.replace('>Lorenzo Belpassi<', '>Chloe Sanchez<')
chloe_sig = chloe_sig.replace('>Founder &amp; Managing Partner<', '>Executive Assistant<')
chloe_sig = chloe_sig.replace('mailto:lorenzo@selva-partners.com', 'mailto:chloe.sanchez@selva-partners.com')
chloe_sig = chloe_sig.replace('>lorenzo@selva-partners.com<', '>chloe.sanchez@selva-partners.com<')
# Phone: keep Lorenzo's (646) 286-4344 as placeholder until Twilio number arrives

# 3. Push to Chloe
with open('/Users/lorenzobelpassi/.hermes/chloe_outreach_token.pickle', 'rb') as f:
    chloe_creds = pickle.load(f)
chloe_service = build('gmail', 'v1', credentials=chloe_creds)
chloe_service.users().settings().sendAs().patch(
    userId='me',
    sendAsEmail='chloe.sanchez@selva-partners.com',
    body={'signature': chloe_sig}
).execute()
```

### Pending items (Selva branding)
- Chloe's Twilio number: replace (646) 286-4344 in her signature once number is assigned
- Org logo in Google Workspace Admin is displaying squished — needs correct aspect-ratio logo uploaded at admin.google.com → Account → Profile

## Revoking Access

```bash
$GSETUP --revoke
```
