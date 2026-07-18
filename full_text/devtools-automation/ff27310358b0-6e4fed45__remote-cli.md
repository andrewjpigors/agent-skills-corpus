---
name: remote-cli
description: Use when the user asks you to perform any Remote.com HR action — create or list time off, manage expenses (approve/decline/download receipts), list or create employments, change an employment's department or manager, update an employee's work email or external id, update personal details (date of birth, gender, nationality, tax id, social security number, other country-specific identity fields), inspect onboarding progress or cancel onboarding for a not-yet-signed employee, view or amend employment contracts (salary changes, title changes, etc.), download payslips, submit terminations, register or inspect webhook callbacks, replay webhook deliveries, manage custom fields (define new attributes, read or update per-employment values) — via the remotecli CLI tool in this project. Also triggers when asked to look up leave balance, employment status, company info, departments, onboarding step state, or webhook delivery history through the CLI, export any list to CSV for a spreadsheet, or discover which fields/columns a list endpoint exposes.
---

# Using the Remote CLI

## Overview

`remotecli` is the built binary for this project. Build it with `make build` if the binary is missing or stale after code changes.

> **Building on top of Remote.com?** Use the `remote-api-builder` skill instead — it teaches the methodology for using `remotecli` as an executable spec to build your own client/SDK/service. This skill (`remote-cli`) is for *driving* the CLI as an operator; `remote-api-builder` is for *learning from* the CLI as a builder.

The simplest setup is a single env var:
```bash
export REMOTE_ENVIRONMENT=production   # or: local | partners | sandbox | staging
```
This sets `REMOTE_BASE_URL`, `REMOTE_AUTH_URL`, and `REMOTE_CLIENT_ID` together. For custom endpoints, set those vars directly. `REMOTE_CLIENT_SECRET` is only needed for token-refresh / JWT-bearer paths (e.g. `employments` actions after the access token expires).

An **active company** must be selected before most commands:
```bash
remotecli companies list   # see what's saved
remotecli use              # interactively pick the active one
```

## Driving the CLI Autonomously

When acting without a human at the keyboard, every interactive prompt is friction — the TUI blocks waiting for keystrokes and your agent has no way to answer. Use this priority order; **top is always cheaper than bottom**:

### 1. Suppress the prompt with flags (preferred)

Every interactive picker has a flag equivalent. Resolve IDs via `list` filters, then pass them to the action. This requires zero special protocol and zero per-prompt round-trips.

```bash
# ❌ Picker fires — TUI blocks; the agent has no way to answer
remotecli contracts list

# ✅ Resolve the ID via a filter, then pass it
remotecli employments list --email alice@example.com --pretty
remotecli contracts list --employment-id emp_abc123
```

Same pattern for `expenses approve --expense-id`, `time-off approve --timeoff-id`, `payslips download --id`, `contract-amendments create --employment-id`, etc. See `references/commands.md` for the full flag inventory.

### 2. Use `--json-prompts` only when a prompt is unavoidable

Schema-driven flows (`employments create`, `contract-amendments create`) prompt for required fields the API doesn't expose as flags. For those, `--json-prompts` swaps the TUI for an NDJSON stdio protocol: stdout emits `{"type":"prompt", ...}` events, stdin takes one `{"answer": ...}` line per event, in order.

**Read the protocol first.** The complete spec lives in `CLAUDE.md` → "JSON prompter mode" (about 30 lines). It enumerates every event type and answer shape. Don't speculate at the format — read it once and you'll know exactly what to send.

Drive the whole flow in **one Bash call**, pre-computing every answer:

```bash
# After reading the schema (or doing a dry-run to learn the prompt order):
printf '%s\n' \
  '{"answer":"Alice Cooper"}' \
  '{"answer":"alice@example.com"}' \
  '{"answer":"2026-06-01"}' \
  | remotecli --json-prompts employments create --country GBR
```

Splitting the flow across multiple Bash tool calls multiplies permission prompts and breaks the pipe. One process, one pipeline, one permission.

**Discovering prompts: each probe should reveal many prompts, not one.** The prompter validates answers in order and emits the next prompt *before* reading its answer, so one Bash call with N valid answers reveals N+1 prompts. Pipe several plausible answers per probe call — `0` validates as a select or number, `"2026-06-01"` as a date, a sufficiently long string as `role_description` — and read every prompt the call emits before composing the next one. Two or three probe calls is usually enough to map a whole form; firing ten one-answer-at-a-time calls is the anti-pattern, because it costs permission prompts and round-trips for no information you couldn't have learned in a single pass. Stop probing the moment field names appear that match data you already have (`job_title`, `work_hours_per_week`, `annual_gross_salary` are all in `contracts list` output) and switch to a real run with the real values.

### 2.5. For multi-field create flows, plan first

`employments create` and `contract-amendments create` are schema-driven — the prompt list depends on the country, the existing contract, and earlier answers. Driving them prompt-by-prompt through `--json-prompts` is the slowest possible way to fill them in: you guess one field at a time, a bad enum value is fatal, and conditional branches surprise you halfway through.

**Use the plan-first loop instead:**

```bash
# 1. Build an answers file with everything you already know (e.g. unchanged fields
#    copied from `contracts list`, or fields the user explicitly asked for).
cat > /tmp/ans.json <<'EOF'
{"contract_amendment": {
  "job_title": "Senior Engineer",
  "annual_gross_salary": 8500000,
  "compensation_currency_code": "GBP"
}}
EOF

# 2. Dry-run. The CLI fetches the country-specific schema, walks it against
#    your answers, and emits one NDJSON plan event. No API write happens.
remotecli --answers /tmp/ans.json --plan contract-amendments create --employment-id emp_abc123
# → {"type":"plan","data":{"ok":false,"form":"contract_amendment",
#       "missing":[ ...required-but-unanswered fields only... ],
#       "invalid":[ ...pre-filled values that don't satisfy the schema... ],
#       "fields":[  ← the COMPLETE inventory: every field the run will prompt,
#                     required AND optional, answered AND not, each select with
#                     its option consts inline. Build your answers file FROM HERE.
#         {"field":"role_description","kind":"text","required":true,"answered":false},
#         {"field":"experience_level","kind":"select","required":true,"answered":false,
#          "options":[{"title":"Level 2 - Entry Level","const":"Level 2 - Entry Level - Employees who..."},
#                     {"title":"Level 3 - Associate","const":"Level 3 - Associate - Employees who..."}]},
#         {"field":"has_bonus","kind":"select","required":false,"answered":false,
#          "options":[{"title":"Yes","const":"yes"},{"title":"No","const":"no"}]}],
#       "answers":{"job_title":"Senior Engineer",...}}}
# exit code: 2

# 3. Fill /tmp/ans.json from `fields[]` (NOT just `missing[]`) — see the two
#    rules below — then run for real:
remotecli --answers /tmp/ans.json contract-amendments create --employment-id emp_abc123
```

**Two rules that save the most time (learned the hard way on ES Global Payroll):**

1. **Build from `fields[]`, not `missing[]`.** `missing` is only the *required-unanswered* subset. `fields` is every field the real run will prompt — required and optional alike — and you must account for the optional ones too: an optional **select** has no "empty" choice in `--json-prompts` (`{"answer":""}` is rejected, so it hard-blocks until you pick a value), and an optional **text** field still emits a prompt that blocks on stdin (an empty `{"answer":""}` is accepted, but you have to send it). A form can have dozens of optional fields invisible to `missing` but listed in `fields`. Skip them and the real run blocks on the first one. Pre-fill or pre-answer everything in `fields`, not just `missing`.
2. **`--answers` needs the `const`, not the title.** Unlike the interactive/`--json-prompts` stream (which maps a chosen label to its const), `--answers` sends select values **verbatim**. Pre-filling `work_schedule: "Full-time"` 422s; use `work_schedule: "full_time"` — i.e. copy `options[i].const` from the plan event. (`options[i].title` is display-only.) Array-typed fields like `country_of_citizenship`/`nationality` want a JSON array, e.g. `["Spain"]`.

**Why this is strictly better than prompt-by-prompt discovery:**

| Concern | `--json-prompts` discovery | Plan-first |
|---|---|---|
| Reveals fields at this branch | One per probe, often via batched-answer trick | One `plan` event: `fields[]` = every field (req+optional), every enum const |
| Bad enum value | Fatal — process exits non-zero, restart from scratch | Reported as `invalid`; tweak file, re-plan |
| Conditional branches | Surprise — show up only after you answer the controlling field | Re-plan after filling the controlling field; no fatal restarts |
| API safety | The submit confirm is the only guard | `--plan` never calls the API; zero risk during exploration |
| Final invocation | Long NDJSON pipe with one answer per line | Single non-interactive call with `--answers` |

**Iterative branch discovery.** A `plan` event only shows fields whose controlling conditions are already satisfied. When `fields[]`/`missing[]` includes a controlling field (e.g. `work_schedule`, `contract_type`), set it and re-plan — the newly-active branch's fields (e.g. `part_time_salary_confirmation` for `work_schedule=part_time`, `contract_end_date` for a fixed-term/substitution `contract_type`, `salary_decrease_reason` for a lower salary) appear in the next plan. For lean countries (GBR) one or two iterations is enough; for rich ones (ES Global Payroll) budget a few more as each controlling select unlocks the next layer.

**Server-side cross-field rules `--plan` can't see.** `--plan` validates presence, type and enum membership, but not every server constraint. Known cases where `ok:true` still 422s: `reason_for_change_description` must be empty unless `reason_for_change = "other"`; ES `contract_type:100` (permanent) forbids `cause_substitution` (the schema still prompts it — use a substitution type like `410`, or expect that field to block). Treat the first real submit as the final validation step.

**Answers-file shape (both commands use the same wrapper):**

```json
// contract-amendments create
{"contract_amendment": {"job_title": "...", "annual_gross_salary": 8500000, ...}}

// employments create
{
  "employment_basic_information": {"name": "Alice Cooper", "email": "alice@example.com", ...},
  "address_details":              {"city": "London", ...},
  "personal_details":             {...},
  "contract_details":             {"job_title": "...", "annual_gross_salary": 7200000, ...},
  "pricing_plan_details":         {"frequency": "monthly"}
}
```

Top-level keys must be objects. A flat `{field: value}` file is rejected — the wrapper is mandatory so the same loader works for single-form (amendments) and multi-form (employments) commands.

### 3. Never write a Python wrapper

If `printf | remotecli` can't express the flow, the answer is to read the schema and pre-compute the answers — **not** to wrap the CLI in `subprocess.Popen`. A wrapper script costs:

- File-write permission to create the script
- Python execution permission to run it
- A near-guaranteed stdin-buffering bug (forgetting `flush=True`, line-buffering on pipes)
- More permission prompts every time you iterate on the script

The CLI was designed for Unix pipes. If you're reaching for Python, you've misread the protocol — go back to step 2 and re-read the `JSON prompter mode` section.

### Red flags — stop and reconsider

| You're about to... | Instead, do this |
|---|---|
| Open an interactive picker via `--json-prompts` and try to answer it | Run the matching `list` command with a filter flag, pass the resulting ID via `--<resource>-id` |
| `cat answers.txt \| remotecli --json-prompts ...` after writing the file in a separate step | Inline the answers with `printf` in a single Bash call — no temp file, no extra permission prompt |
| `python wrapper.py` that calls `subprocess.Popen(["remotecli", ...])` | Stop. Read `CLAUDE.md` → "JSON prompter mode". Use `printf \| remotecli` instead |
| Run multiple Bash tool calls to drive one CLI invocation | One Bash call, one pipeline — the CLI process should not span tool invocations |

## Quick Command Reference

| Command | What it does | Key flags |
|---------|-------------|-----------|
| `login` | Authenticate via browser (PKCE) | — |
| `use` | Pick active company (interactive) | — |
| `me` | Show current identity | `--company-token` |
| `companies list` | List saved companies | `--pretty` |
| `companies create` | Create a company | `--integration-token` |
| `employments list` | List employments | `--status`, `--email`, `--employment-model`, `--all` |
| `employments create` | Onboard a new employee | `--country`, `--answers`, `--plan` |
| `employments show <id>` | Get a single employment | — |
| `employments update [id]` | Update flat employment fields (department, manager, work email, external id) | `--department`, `--department-id`, `--manager-id`, `--work-email`, `--external-id` |
| `employments update-personal-details [id]` | Update country-specific personal details (DOB, gender, nationality, tax id, etc.) via JSON Schema | `--country`, `--answers`, `--plan` |
| `onboarding steps [id]` | Show the onboarding-step checklist (status, substep count) for an employment | `--columns`, `--company-token` |
| `onboarding cancel [id]` | Cancel onboarding before the employee signs the contract | `--async`, `--yes` / `-y` |
| `departments list` | List company departments | `--company-id`, `--columns`, `--all` |
| `departments create` | Create a new company department | `--name`, `--company-id` |
| `contracts list` | List contracts for an employment for historical contracts set the only-active to false | `--employment-id`, `--only-active=false` |
| `contract-amendments list` | List submitted contract amendments | `--employment-id`, `--status`, `--all` |
| `contract-amendments show <id>` | Show a single amendment | — |
| `contract-amendments create` | Submit a contract amendment | `--employment-id`, `--contract-id`, `--country`, `--answers`, `--plan` |
| `expenses list` | List expenses | `--status`, `--all`, `--pretty` |
| `expenses create` | Submit an expense | `--employment-id`, `--amount`, `--currency`, `--expense-date`, `--title`, `--category`, `--tax-amount`, `--notes` |
| `expenses categories` | List valid `--category` codes for an employment | `--employment-id`, `--include-parents` |
| `expenses approve` | Approve a pending expense | `--expense-id` |
| `expenses decline` | Decline a pending expense | `--expense-id`, `--reason` |
| `expenses download-receipt` | Download a receipt file | `--expense-id`, `--receipt-id`, `--out-file` |
| `payslips list` | List payslips | `--employment-id`, `--start-date`, `--end-date` |
| `payslips download` | Download a payslip PDF | `--id`, `--out-file` |
| `time-off policies` | List leave policies details | `--employment-id` |
| `time-off balance` | Show leave balance summary | `--employment-id` |
| `time-off create` | Create time off (approved if manager, requested if employee) | `--employment-id`, `--timeoff-type`, `--start-date`, `--end-date` |
| `time-off list` | List time off records | `--employment-id`, `--status`, `--timeoff-type` |
| `time-off approve` | Approve a requested time off | `--timeoff-id` |
| `time-off cancel` | Cancel an approved time off | `--timeoff-id`, `--reason` |
| `time-off decline` | Decline a requested time off | `--timeoff-id`, `--reason` |
| `terminations list` | List terminations | `--employment-id`, `--type` |
| `terminations create` | Submit a termination request | `--employment-id` |
| `webhooks list` | List webhook callbacks for the active company | `--columns` |
| `webhooks create` | Register a webhook callback | `--url`, `--events` |
| `webhooks update [id]` | Update callback URL and/or subscribed events | `--url`, `--events`, `--add-events`, `--remove-events` |
| `webhooks delete [id]` | Delete a webhook callback (confirms on TTY) | `--yes` / `-y` |
| `webhooks event-history` | List webhook delivery events | `--event-type`, `--successfully-delivered`, `--before`, `--after`, `--all` |
| `webhooks event-replay [ids...]` | Replay events by id or filter | `--event-ids`, `--event-type`, `--before`, `--after`, `--yes` |
| `custom-fields list` | List custom field definitions for the company | `--all`, `--page`, `--page-size`, `--columns` |
| `custom-fields create` | Define a new custom field | `--name`, `--type`, `--required`, `--visibility`, `--data-entry-access` |
| `custom-fields values` | List all custom field values on one employment | `--employment-id` |
| `custom-fields show` | Show a single custom field's value for an employment | `--field-id`, `--employment-id` |
| `custom-fields update` | Update a custom field's value for an employment | `--field-id`, `--employment-id`, `--value` |
| `cache list` | List every cached entry (scope, key, size, time-to-expiry) | `--columns` |
| `cache info` | One-line summary: path, total entries, total size, oldest/newest expiry | — |
| `cache clear` | Flush cached responses (all or by prefix) | `--prefix` |
| `cache path` | Print the cache file path | — |
| `<resource> list-columns` | List columns available for `--columns` on that resource's `list`. Registered on every list-bearing resource. | — |

## Common Workflows

### Updating an employment — which command updates which field?

Three commands mutate an employment. The split is by *where the field lives in the data model*, not by intent — pick the one that matches the resource the field belongs to, not the verb the user used.

| Field category | Command | Lives on |
|---|---|---|
| `job_title`, `role_description`, `annual_gross_salary`, `work_hours_per_week`, `work_schedule`, `contract_duration_type`, `experience_level`, anything else compensation- or scope-of-work-related | `contract-amendments create` | The active contract |
| `department_id`, `manager_id`, `work_email`, `external_id` | `employments update` | Flat fields on the employment record (`PATCH /v2/employments/{id}`) |
| `date_of_birth`, `gender`, `place_of_birth`, `marital_status`, `nationality`, `tax_id`, `social_security_number`, dependent details, other country-specific identity/HR fields | `employments update-personal-details` | The employment's `personal_details` nested object (`PUT /v1/employments/{id}/personal_details`) |
| `address_details`, `emergency_contact_details`, `bank_account_details`, other country-specific forms | Not yet wrapped — use the web UI or call the per-section v2 endpoints directly | — |

**How to find where a field lives — three probes, top to bottom:**

```bash
# 1. Anything you see HERE goes through `contract-amendments create`:
remotecli contracts list --employment-id emp_abc123
#   → data.employment_contracts[0]: job_title, annual_gross_salary, work_hours_per_week,
#     work_schedule, contract_duration_type, compensation_currency_code, experience_level, ...

# 2. FLAT fields you see HERE go through `employments update`;
#    the nested `personal_details` object goes through `employments update-personal-details`:
remotecli employments show emp_abc123
#   → data.employment: department, manager, work_email, external_id (flat → `employments update`)
#                      personal_details: { date_of_birth, gender, ... } (nested → `update-personal-details`)

# 3. To see EVERY field the personal_details form accepts for this country
#    (including required-but-currently-empty ones), do a plan dry-run with an empty seed:
echo '{"personal_details":{}}' > /tmp/pd.json
remotecli --answers /tmp/pd.json --plan employments update-personal-details emp_abc123
#   → one NDJSON plan event listing every missing field + its kind/options/required flag,
#     resolved against the employment's country. No write happens.
```

**`job_title` gotcha.** It appears in *both* the create-time `employment_basic_information` form and the `contract_amendment` form. After hire, the displayed job title comes from the active contract — to change it, use `contract-amendments create`, not `employments update` (which doesn't accept `job_title` anyway and would 422 you).

**Create time off for an employee:**
```bash
remotecli time-off create \
  --employment-id emp_abc123 \
  --timeoff-type time_off \
  --start-date 2026-05-09 \
  --end-date 2026-05-09
```
Common types: `time_off`, `sick_leave`, `paid_time_off`, `public_holiday`, `unpaid_leave`, `maternity_leave`, `paternity_leave`, `bereavement`. Full list in `references/commands.md`.

**List active employments:**
```bash
remotecli employments list --status active --pretty
```

**Approve a pending expense:**
```bash
remotecli expenses approve --expense-id exp_xyz789
```

**Download the latest payslip for an employment:**
```bash
remotecli payslips list --employment-id emp_abc123 --pretty
remotecli payslips download --id <id> --out-file ./payslip.pdf
```

**Check an employee's leave balance:**
```bash
remotecli time-off balance --employment-id emp_abc123 --pretty
```

**Amend an employee's contract (salary, title, hours, etc.):**

A contract amendment is a *delta* over the current contract — unchanged fields must be copied verbatim from the active contract, or the API records each one as an additional proposed change. The fastest autonomous recipe is **resolve → read → plan → submit**:

```bash
# 1. Resolve the employment (skip the picker; filters are unambiguous).
remotecli employments list --email alice@example.com --pretty
# → emp_abc123 in GBR

# 2. Read the active contract. Don't pass --pretty — we want the JSON form.
remotecli contracts list --employment-id emp_abc123
# → data.employment_contracts[0] has job_title, role_description,
#   annual_gross_salary (integer minor units, e.g. 7200000 = £72,000),
#   work_hours_per_week, contract_duration_type, work_schedule,
#   compensation_currency_code, experience_level, ...

# 3. Build the answers file by copying the active contract verbatim and
#    overwriting only the fields the change actually affects.
#    For a 10% raise on a £72,000 → £79,200 contract:
cat > /tmp/amend.json <<'EOF'
{"contract_amendment": {
  "job_title": "Senior Engineer",
  "role_description": "<copy verbatim from contracts list>",
  "annual_gross_salary": 7920000,
  "work_hours_per_week": 40,
  "contract_duration_type": "indefinite",
  "work_schedule": "full_time",
  "compensation_currency_code": "GBP",
  "experience_level": "Level 3 - Associate - <full const value from schema>",
  "effective_date": "2026-06-01",
  "reason_for_change": "annual_pay_adjustment",
  "reason_for_change_description": "Annual performance-based raise"
}}
EOF

# 4. Dry-run to catch anything missing (conditional branches, country-specific
#    extras, or fields you mistyped). The CLI does not POST.
remotecli --answers /tmp/amend.json --plan contract-amendments create --employment-id emp_abc123

# 5. If the plan reports !ok, edit /tmp/amend.json with the missing/invalid
#    fields (the plan event includes oneOf options verbatim for select fields)
#    and re-plan. Repeat until ok.

# 6. Submit for real.
remotecli --answers /tmp/amend.json contract-amendments create --employment-id emp_abc123
# → {"amendment_id":"am_...","status":"submitted","employment_id":"emp_abc123"}
```

**Critical reminders:**
- `annual_gross_salary` is in **minor units (pence/cents)** in both `contracts list` and the amendment form. `7200000` = £72,000. Don't divide by 100. Don't pass `72000.00`.
- For `experience_level`, the `const` value in the schema is the **entire descriptive sentence** (e.g. `"Level 3 - Associate - Employees who perform independently tasks ..."`), not just `"Level 3"`. Copy `options[i].const` from the plan event verbatim — it's the full descriptive sentence, not the short title.
- A salary *decrease* (new gross < current gross) unlocks two more required fields: `salary_decrease_reason` and `was_employee_informed`. The plan event will surface these only after `annual_gross_salary` and `compensation_currency_code` are both set.
- Track the amendment afterwards with `remotecli contract-amendments list --employment-id emp_abc123` or `remotecli contract-amendments show <amendment_id>`.

**Manage webhook callbacks:**

Webhook callbacks are scoped to the active company. All six commands resolve the company from the active token; no separate `--employment-id` is needed. The full reference is in `references/commands.md` → `webhooks`.

```bash
# Register a callback. --events is comma-separated; the server validates
# against its enum, so unknown event names return 422.
remotecli webhooks create \
  --url "https://hooks.example.com/remote" \
  --events "company.eor_hiring.verification_completed"
# → returns id, url, subscribed_events, signing_key (HMAC secret).
#   The signing_key is shown ONCE — capture it from --json output before
#   moving on. The CLI emits a TTY-only stderr warning when a secret-shaped
#   field is detected.

# List callbacks for the active company.
remotecli webhooks list --json

# Update — three modes (mutually exclusive):
#   --events foo,bar    full replace
#   --add-events foo    add to current
#   --remove-events bar drop from current
# PATCH always sends subscribed_events, so the URL-only flag still works.
remotecli webhooks update <id> --url "https://new.example.com/hook"
remotecli webhooks update <id> --add-events "employment.invited" --remove-events "contract.activated"

# Delete. Pass --yes for non-interactive.
remotecli webhooks delete <id> --yes

# Inspect delivery history. Tri-state --successfully-delivered (omit | true | false).
remotecli webhooks event-history \
  --event-type "company.eor_hiring.verification_completed" \
  --successfully-delivered false \
  --after "2026-05-01T00:00:00Z" \
  --all --json

# Replay events. EITHER positional ids OR filters (at least one of either).
remotecli webhooks event-replay ev_1 ev_2 --yes                 # explicit ids
remotecli webhooks event-replay --event-type X --after 2026-05-01 --yes
# Calling with neither ids nor filters is a hard error — the CLI refuses to
# replay everything.
```

**Event-type catalog notes:**
- The bundled catalog used by the interactive multiselect is intentionally small (currently one entry: `company.eor_hiring.verification_completed`) — it's a UX aid, not authoritative.
- For unknown event types, just pass them on `--events` / `--add-events` — the CLI accepts any string. The server's enum is the source of truth.
- When the server rejects an unknown event name, the error is `Invalid value for enum` (HTTP 422). Update the bundled catalog in `internal/webhooks/events.go` once you've confirmed a new event name works.

**Change an employment's department, manager, or contact fields (`employments update`):**

Updates the four flat employment-level fields exposed by `PATCH /v2/employments/{id}`: `department_id`, `manager_id`, `work_email`, `external_id`. For salary, job-title, hours, or role changes use `contract-amendments create` instead — those live on the contract, not the employment.

```bash
# 1. Resolve the employment (skip the picker).
remotecli employments list --email alice@example.com --pretty   # → emp_abc123

# 2. If changing department by name, list the company's departments first.
#    --department <name> resolves the slug for you (prompting if multiple match);
#    --department-id <slug> takes the slug directly.
remotecli departments list --pretty
# Need a department that doesn't exist yet? Create it first:
remotecli departments create --name "Product"
remotecli employments update emp_abc123 --department Product

# 3. Detach a department:
remotecli employments update emp_abc123 --department-id null

# 4. Change manager / work email / external id:
remotecli employments update emp_abc123 --manager-id usr_admin42
remotecli employments update emp_abc123 --work-email alice@newcorp.example
remotecli employments update emp_abc123 --external-id HR-1042

# 5. Multiple fields in one call:
remotecli employments update emp_abc123 \
  --department Product --manager-id usr_admin42 --external-id HR-1042
```

**Picker fallback (avoid by passing IDs).** Calling `employments update` with no positional arg, no `--employment-id`, and no mutation flags opens the standard employment picker, then a "which field to change?" select (mirrors `webhooks update`). Under `--json-prompts` the same flow emits `select` + typed prompts. For autonomous use, always pass `--employment-id` (or the positional arg) and at least one mutation flag.

**Department names are not unique.** When `--department <name>` matches more than one department, the CLI prompts to disambiguate. Pass `--department-id <slug>` to skip resolution entirely.

**Role.** Requires a manager / admin / owner token. Employee tokens get a 403 (server-side guard).

**Change an employment's personal details (`employments update-personal-details`):**

Replaces the employment's `personal_details` via `PUT /v1/employments/{id}/personal_details`. The accepted fields are country-specific (driven by the JSON Schema at `/v1/countries/{country}/personal_details`), so the discovery loop is the same plan-first pattern used by `contract-amendments create`: dry-run to learn the schema, then submit. The country is resolved from the employment automatically — pass `--country` only to override.

```bash
# 1. Resolve the employment (skip the picker).
remotecli employments list --email alice@example.com --pretty   # → emp_abc123

# 2. (Optional) See what's currently set — `personal_details` is a nested object on
#    `employments show`. Treat its keys as the starting point for your answers file
#    (unchanged keys must be re-sent on PUT, since this endpoint REPLACES the
#    personal_details object — it's not a sparse PATCH).
remotecli employments show emp_abc123 --json | jq '.data.employment.personal_details'

# 3. Build an answers file. The wrapper key is the form name: "personal_details".
cat > /tmp/pd.json <<'EOF'
{"personal_details": {
  "date_of_birth": "1990-04-12",
  "gender": "female",
  "place_of_birth": "London",
  "nationality": "British"
}}
EOF

# 4. Dry-run. The plan event lists every required-but-missing field for this
#    country, with options[] for select-typed fields. No write happens.
remotecli --answers /tmp/pd.json --plan employments update-personal-details emp_abc123
# → {"type":"plan","data":{"ok":false,"form":"personal_details",
#                          "missing":[{"field":"tax_id","kind":"text",...}],
#                          "invalid":[], "answers":{...}}}
# exit code: 2

# 5. Patch /tmp/pd.json with the missing fields and re-plan until ok.

# 6. Submit for real.
remotecli --answers /tmp/pd.json employments update-personal-details emp_abc123
# → renders the updated employment record on stdout.
```

**Replacement semantics.** This endpoint **replaces** the `personal_details` object — it is not a sparse PATCH. Always seed the answers file from the current `employments show` output, then overwrite only the keys that should change. Omitting a previously-set field will clear it.

**`--country` override.** By default the country is read from the employment record. Pass `--country GBR` to force a specific schema (rare — only useful if the employment record's country is missing or you're testing schema variations).

**Discovery tip.** To see *every* field the schema accepts for a country without committing to values, plan against an empty seed: `echo '{"personal_details":{}}' > /tmp/pd.json && remotecli --answers /tmp/pd.json --plan employments update-personal-details emp_abc123`. The resulting `missing[]` is the full required-field list for that country.

**Role.** Requires a manager / admin / owner token (employees update their own profile through the web UI / employee-scoped endpoints).

**Inspect or cancel onboarding (`onboarding steps` / `onboarding cancel`):**

After `employments create`, the employee progresses through an onboarding checklist (basic info → contract → verification → reserve payment → contract signature). `onboarding steps` shows that checklist; `onboarding cancel` aborts it while the employee hasn't signed yet. Aliased as `onboardings` for convenience.

```bash
# 1. Resolve the employment.
remotecli employments list --email alice@example.com --pretty   # → emp_abc123

# 2. Show the onboarding step checklist. Output is one row per top-level step.
remotecli onboarding steps emp_abc123 --pretty
# → Title, Status, Substeps (count). Available columns also include
#   `started`, `completed`, and `description` — see
#   `remotecli onboarding list-columns`.
remotecli onboarding steps emp_abc123 --columns title,status,started,completed,description

# Need the full nested structure (substeps with their own status / titles)?
# JSON mode returns the raw envelope so you can drill in with jq:
remotecli onboarding steps emp_abc123 --json | jq '.data.steps[] | {label, status, sub_steps: [.sub_steps[] | {label, status}]}'

# 3. Cancel onboarding (only valid while status ∈
#    {invited, created, created_awaiting_reserve, created_reserve_paid, pre_hire}
#    and the employee has not signed the contract).
remotecli onboarding cancel emp_abc123 --yes
#   --yes  skips the confirmation prompt — required in non-interactive shells.
#   --async  processes the cancellation server-side asynchronously (the response
#            returns immediately; poll `employments show` to see the final state).
```

**Picker fallback (avoid by passing IDs).** Calling `onboarding cancel` with no employment id opens a picker pre-filtered to the five cancellable statuses; calling it in a non-interactive shell without an id and without `--yes` is a hard error (the CLI refuses to mass-cancel by accident).

**Status guard.** The server only accepts cancellation for employments in one of: `invited`, `created`, `created_awaiting_reserve`, `created_reserve_paid`, `pre_hire`. After the employee signs the contract, cancellation must go through the termination flow (`terminations create`) instead.

**Role.** Manager / admin / owner token. Employee tokens get a 403 — employees can't cancel their own onboarding.

**Read or update a custom field value for an employee:**

Custom fields are company-defined attributes attached to employments (e.g. "Shirt Size", "Office Location Code", "Monthly Travel Days"). Definitions live company-wide; values live per-employment.

```bash
# 1. List the company's definitions to find the field-id and its type.
remotecli custom-fields list --pretty
# → cf_b26b...  Has Company Laptop?   boolean  …  visibility_scope: everyone
# → cf_2576...  Languages             string   …
# → cf_b24f...  Monthly Travel Days   integer  …

# 2. (Read all values on one employment.)
remotecli employments list --email alice@example.com --pretty   # → emp_4d13...
remotecli custom-fields values --employment-id emp_4d13... --pretty

# 3. (Read or update a single value.)
remotecli custom-fields show \
  --field-id cf_b24f... --employment-id emp_4d13...
remotecli custom-fields update \
  --field-id cf_b24f... --employment-id emp_4d13... --value 12
```

**Picker fallbacks (avoid by passing IDs).** `show` and `update` open an interactive `pickCustomField` picker when `--field-id` is omitted, and the standard employment picker when `--employment-id` is omitted. Resolve both via filters first (`custom-fields list` and `employments list --email`) when driving autonomously.

**Typed-prompt fallback on `update`.** When `--value` is omitted, the CLI looks up the field's `type` from the cached definitions list and presents a type-matched prompt (text / number / date / boolean / etc.). Under `--json-prompts` you get the same typed `prompt` event — so the simple `printf '{"answer":"12"}\n' | remotecli --json-prompts custom-fields update --field-id ... --employment-id ...` pattern works fine. Send strings for text/number/date prompts and `true`/`false` for boolean prompts.

**Define a new custom field (`custom-fields create`):**

Hybrid flags + interactive prompts. Pass what you know; the prompter only asks for what's missing.

```bash
# Fully non-interactive:
remotecli custom-fields create \
  --name "Hire Cohort" \
  --type string \
  --required=false \
  --visibility everyone \
  --data-entry-access company_admin_only
```

| Field | Enum |
|---|---|
| `--type` | `string`, `integer`, `float`, `boolean`, `date` |
| `--visibility` (the company-wide visibility scope) | `everyone`, `company_admin_only` |
| `--data-entry-access` (who can write the value) | `everyone`, `company_admin_only` |

Returns the new definition's `id`. Custom field values for existing employments start unset until written via `custom-fields update`.

**Onboard a new employee (`employments create`):**

`employments create` walks five forms in sequence: basic info → address → personal details → contract details → pricing plan. The country selects which fields appear in each. Drive it the same way as amendments — answers file + plan-first.

```bash
# 1. Build an answers file with everything you know. Top-level keys are the
#    five form names; values are {field: value} objects per form.
cat > /tmp/hire.json <<'EOF'
{
  "employment_basic_information": {
    "name": "Alice Cooper",
    "email": "alice@example.com",
    "job_title": "Senior Engineer",
    "provisional_start_date": "2026-07-01"
  },
  "address_details": {
    "address_line_1": "1 King's Cross",
    "city": "London",
    "postal_code": "N1 9AG"
  },
  "personal_details": {
    "date_of_birth": "1990-04-12"
  },
  "contract_details": {
    "annual_gross_salary": 8500000,
    "work_hours_per_week": 40,
    "contract_duration_type": "indefinite",
    "work_schedule": "full_time"
  },
  "pricing_plan_details": {
    "frequency": "monthly"
  }
}
EOF

# 2. Dry-run. Returns ONE aggregated plan event spanning all five forms;
#    each missing/invalid entry carries a "form" field so you know which
#    section of the answers file to patch.
remotecli --answers /tmp/hire.json --plan employments create --country GBR

# 3. Patch missing fields per form, re-plan until ok.

# 4. Real run. Pricing plan defaults to `{"frequency":"monthly"}` if you
#    omit it; everything else must be supplied via --answers or come from
#    interactive prompts.
remotecli --answers /tmp/hire.json employments create --country GBR
# → {"employment_id":"emp_...","status":"invited"}
```

The country code (3-letter ISO, e.g. `GBR`, `USA`, `BEL`, `PRT`) must be passed on the command line; it is not a form field. After creation the employee receives an invite email.

## Output Control

```bash
remotecli <cmd>             # auto: table on TTY, json on pipes (default)
remotecli <cmd> --json      # force JSON (alias for --output=json)
remotecli <cmd> --pretty    # force table (alias for --output=table; compact column subset)
remotecli <cmd> -o csv      # CSV for spreadsheet export (list commands only)
remotecli <cmd> --all       # fetch all pages (list commands; default page-size: 20)
remotecli <cmd> --columns id,name,email   # pick exact columns (any mode)
```

For autonomous use, **always pass `--json` (or pipe to a non-TTY)** — the default switches to table when stdout is a terminal, and table output is not machine-parseable.

**`--pretty` vs `--output=csv` show different column sets by default.** `--pretty` returns a compact set tuned for terminal width (e.g. employments: ID, Name, Email, Country, Status, Model). `-o csv` and `-o json` return every column the registry exposes (employments: 16, contracts: 15, expenses: 18, time-off: 18, terminations: 12, contract-amendments: 8). Agents reading JSON already see everything. To pull the full set into table mode, pass `--columns` explicitly — it accepts any registered key regardless of the default set.

### Discovering available columns

Every list command has a sibling `list-columns` subcommand that prints the key/header pairs for `--columns`:

```bash
remotecli employments list-columns          # JSON: data.columns = [{key, header}, ...]
remotecli employments list-columns --pretty  # table
remotecli employments list-columns -o csv    # csv
```

Use this before assuming a field exists. The list reflects the *current* registry (no API call), so it's the source of truth for what `--columns` will accept and what a CSV export will contain. `list-columns` is registered on all list-bearing resources: `companies`, `employments`, `contracts`, `contract-amendments`, `expenses`, `payslips`, `terminations`, `time-off`, `departments`, and the two webhook lists. The webhooks variants attach to the leaf, not the parent — invoke them as `webhooks list list-columns` and `webhooks event-history list-columns`.

### CSV export

`-o csv` is list-only — non-list commands (`me`, `* show`, schema-driven `create`) fail non-zero with `csv output is only supported for list commands`. CSV writes to stdout; redirect to capture:

```bash
remotecli employments list --all -o csv > /tmp/employments.csv
remotecli expenses list --all -o csv --columns id,amount,currency,employee > /tmp/expense-totals.csv
```

Headers come from each column's display name (e.g. `Net (source)`, `Compensation`). Tax / amount / currency cells use the same formatters table mode uses (ISO 4217-aware decimal places), so the numbers are spreadsheet-ready without further processing.

## Role Restrictions

These operations require a **company manager token** and fail with employee tokens:
- `expenses create / approve / decline`
- `time-off create / approve / decline`
- `terminations create`

Employee tokens use different endpoints (`/v1/employee/...`) and expose a read-only subset.

## Constraints to Know

- `expenses create --expense-date` must be **today or in the past** — future dates are rejected by the API.
- File uploads (receipts, termination docs): PDF/DOC/DOCX only, max 10 MB each, max 5 files.
- `expenses create` self-submission guard: when the OAuth identity equals the target employment's user, a `confirm` prompt (`__self_submit_confirm`) fires before submission. Agents driving via `--json-prompts` must answer `{"answer":true}` to proceed; the server would otherwise auto-approve the expense and skip reviewer policy.

## Full Reference

See `references/commands.md` for every flag, valid enum values, and pagination options for each command.
