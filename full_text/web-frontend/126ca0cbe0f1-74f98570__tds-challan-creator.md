---
name: tds-challan-creator
description: >-
  Drive the Indian Income Tax e-Pay Tax portal (eportal.incometax.gov.in) with the
  npx agent-browser CLI to generate a TDS/TCS challan and capture its CRN (Challan Reference
  Number) via "Pay Later" — WITHOUT making any actual payment. Use this whenever the user
  wants to "create a TDS challan", "generate a TCS challan", "make a challan / CRN on the
  income tax portal", "pay TDS" through e-Pay Tax, or produce a challan reference number for
  a TAN. Trigger even if they only say "generate the challan for a TAN" or "get me a CRN".
  Requires the `npx agent-browser` CLI and a human available to relay the mobile OTP.
---

# TDS / TCS Challan Creator (e-Pay Tax → CRN)

Generate a TDS/TCS challan on the Income Tax Department's **e-Pay Tax** portal and stop at
the point where the portal issues a **CRN (Challan Reference Number)** through the **Pay
Later** option. The CRN can be paid later from any authorised bank within its validity
window.

## Hard safety boundary — read first

- **Never complete a payment.** The flow ends the instant the CRN is generated (via **Pay
  Later**). Do **not** click "Pay Now", do not enter card/net-banking/UPI credentials, and
  do not submit anything on a bank's own payment page. Selecting **any** payment-mode tab
  (e.g. Debit Card) and bank option is only used to *reach* the challan summary; you then
  choose **Pay Later**.
- **Never invent tax numbers.** PAN/TAN, section, and every amount come from the user. If a
  required value is missing, ask — don't guess. A wrong section or amount on a real tax
  challan is a costly error.
- **Pause for the OTP.** The OTP is sent to the user's phone. You cannot proceed past it
  alone. Stop and ask the user each run.

## Tooling

This skill drives the browser exclusively through the **npx agent-browser** CLI. Core loop:

```bash
npx agent-browser open <url>                 # navigate (SPA — always follow with a wait)
npx agent-browser wait --load networkidle    # let the Angular app settle
npx agent-browser snapshot -i --json         # interactive elements + refs (@e1, @e2, ...)
npx agent-browser click @e5                  # act on a ref from the latest snapshot
npx agent-browser fill  @e6 "value"          # clear + type
npx agent-browser find text "Continue" click # act by visible label when it's stable
```

## Hybrid execution model (speed + accuracy)

Use a hybrid workflow so the portal runs fast, but the model still makes the judgment calls that matter:

### Script the deterministic parts
- Portal launch and page-load waits
- Filling fixed identity fields and OTP boxes
- Selecting known radios: deductee type, residential status, payment mode, bank
- Entering known amounts
- Verifying DOM state: checked radios, enabled buttons, totals, and preview values
- Clicking stable navigation controls once the page state is known
- Extracting the CRN from the challan details page

### Leave the ambiguous parts to the LLM
- Mapping messy business wording to the correct section / description
- Choosing between close or partial section matches
- Deciding whether a portal failure is recoverable or should stop for human review
- Explaining failures and next steps in plain language

### Execution preference
- Use direct DOM reads / `eval` for the stable checks first; use snapshots as fallback for drift.
- Prefer one uninterrupted pass from OTP to CRN capture.
- Treat session reuse as best-effort only; if back, reload, or navigation breaks the portal state, restart clean rather than forcing a brittle reuse path.

### One-time setup: config file (do this FIRST, once per environment)

This portal needs specific launch flags and a real-browser User-Agent, or it returns
`net::ERR_EMPTY_RESPONSE` (and Chrome crashes with `No usable sandbox!` in containers).
Rather than prefixing every command with env vars — which the daemon does not persist, so a
single missed prefix breaks the run — **write these once to a config file that the CLI reads
on every invocation**, regardless of shell or working directory:

```bash
mkdir -p ~/.agent-browser
cat > ~/.agent-browser/config.json <<'JSON'
{
  "$schema": "https://agent-browser.dev/schema.json",
  "args": "--no-sandbox,--disable-blink-features=AutomationControlled,--disable-dev-shm-usage,--headless=new",
  "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
  "headed": false
}
JSON
```

With this in place, run commands plainly — `npx agent-browser <command>` — with **no env
prefix and no `--headless` flag**; the config supplies all of it. Config precedence is
config file < `AGENT_BROWSER_*` env < CLI flags, so you can still override any single value
on one command if needed.

Notes:
- `~/.agent-browser/config.json` is user-level and cwd-independent (best for agents whose
  bash calls may start in a fresh shell). If you'd rather scope it to one project instead of
  globally, put the same JSON in `./agent-browser.json` in a fixed working directory.
- Keep the `userAgent` reasonably current; a long-stale Chrome version may eventually be
  flagged. `Chrome/137` is the tested baseline.
- **Optional hardening:** add `"allowedDomains": ["incometax.gov.in", "*.incometax.gov.in"]`
  to prevent stray navigation to a real bank page. Only do this if the portal still loads —
  if it starts failing to render, a required CDN is being blocked; add that CDN's domain or
  remove the key.

### Rules that keep this reliable on this portal

- It is a single-page app with hash routing. **After every navigation or button click that
  changes the page, run `wait --load networkidle` (and/or `wait --text "<something on the
  next page>"`) and then a fresh `snapshot -i`.** Refs from an old snapshot are stale. Prefer
  condition waits (`wait --text "..."`, `wait --fn "..."`) for page/section loads; the few
  short fixed `wait 500`/`wait 1000` calls below are only settle pauses after client-side
  filtering or Angular event dispatch, where no clean condition exists.
- **NEVER `reload` the page.** The SPA session dies on reload and shows "Unauthorized! The
  page is not available." If you need to retry a page, use `back` or restart from Step 1.
- Prefer `find text/role/label ... click` for labelled buttons ("Continue", "Proceed",
  "Add", "Pay Later"). Use `@eN` refs from a snapshot for inputs, radios, and the OTP boxes.
- Default to **headless** (set by the config file above) — the user prefers unattended runs.
  Only switch to headed for visual debugging: override on a single command with `--headed`.
  In shared or multi-user environments, do **not** use `close --all`; prefer starting a fresh,
  isolated browser session so you don't terminate anyone else's work.
- Use the `npx` wrapper (`npx agent-browser ...`) consistently. When you change launch
  behaviour (headed/headless, args), restart only the browser context you are actively using;
  avoid global browser teardown commands in shared sessions.
- For a second CRN, try in-page Edit Payment / New Payment only while the live portal state
  remains intact; if back/reload/navigation breaks the flow, restart clean and obtain a fresh
  OTP instead of forcing session reuse.
- If a visible footer button is below the fold, prefer `scrollintoview` or a direct JS click
  on the visible button after re-snapshotting.
- **Browser launch on Linux/sandboxed environments (critical).** On Ubuntu 23.10+ or
  containers, Chrome crashes with `No usable sandbox!` without `--no-sandbox`, and this portal
  rejects vanilla headless with `net::ERR_EMPTY_RESPONSE`. The config file above fixes both
  (via `args` `--no-sandbox` + `--headless=new`, and the custom `userAgent`). Because the CLI
  re-reads that config on every call, you never have to remember a per-command prefix. Still
  run `npx agent-browser close --all` before the first `open` so any pre-existing daemon
  adopts the config. If launch still stalls, use the xvfb + CDP fallback in
  `references/browser-launch-and-blockers.md`.
- **Use `fill` (not `keyboard type`) for standard form inputs on this portal.** `keyboard type` appends to existing value instead of replacing it, which causes "Invalid Mobile number" errors when the field already has text. Always use `npx agent-browser fill @<ref> "value"` — it clears first, then types.
- **Angular Material OTP fields are special — `fill` does NOT trigger change detection.** See Step 4.
- **Angular Material `mat-select` dropdowns are special — `fill`/`keyboard type` don't work.** See Step 8.
- **Viewport is only 1280×577 in headless mode.** Buttons (especially Continue) are often
  below the fold. Always `scrollintoview @ref` or `scroll down 200` before clicking.
- If a click seems to do nothing, `snapshot -i` again and check whether a validation error
  or a different label appeared before retrying.
- **If a JavaScript modal/prompt blocks the page**, dismiss it before anything else, then
  re-snapshot (refs shift once it closes): `npx agent-browser dialog dismiss`.
- **When the page visually advances but the snapshot looks stale**, confirm the real state
  with `npx agent-browser get text body` before firing the next action, rather than acting
  on lagging refs.
- **If the portal renders a bare blocker page** (an error/"not available" message instead of
  the form), do not force the flow forward — `screenshot` it, `get text body`, and report the
  blocker to the user. See `references/browser-launch-and-blockers.md`.

### Angular Material interaction patterns (critical)

These patterns were battle-tested and MUST be followed — generic `fill`/`click` approaches
silently fail on this portal's Angular Material components.

#### OTP input boxes (6-digit)

`fill` and `keyboard type` set the DOM value but Angular's reactive forms don't detect the
change — the Continue button stays disabled even though the values look correct in the DOM.
The reliable approach uses **real keyboard events** via `click` + `press` per box:

```bash
# Snapshot to get fresh OTP refs each time (they change after Resend OTP)
npx agent-browser snapshot -i --json
# Click each box, then press the digit key (real keystroke triggers Angular)
npx agent-browser click @otp_1 && npx agent-browser press <digit-1>
npx agent-browser click @otp_2 && npx agent-browser press <digit-2>
npx agent-browser click @otp_3 && npx agent-browser press <digit-3>
# ... repeat for all 6 digits (substitute the actual digits the user provides)
```

After filling, **verify Continue is enabled** before clicking:
```bash
npx agent-browser eval "(() => { const b = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === 'Continue' && x.offsetParent !== null); return b?.disabled ?? 'not found'; })()"
```

If still `true`, dispatch Angular events manually as a fallback:
```bash
npx agent-browser eval "(() => { document.querySelectorAll('input[type=\"password\"]').forEach(inp => { inp.dispatchEvent(new Event('input', {bubbles: true})); inp.dispatchEvent(new Event('change', {bubbles: true})); }); return 'dispatched'; })()"
```

#### `mat-select` searchable dropdown (Description/Section selector)

`fill` and `keyboard type` do nothing on `mat-select` — the overlay search box is inside a
CDK overlay, not accessible via regular fill. The reliable approach uses `eval`:

```bash
# 1. Open the mat-select by its label ("Description") — do NOT rely on a generated id like
#    mat-select-2; those numbers shift between portal releases. Find it by nearby label text:
npx agent-browser eval "(() => {
  const field = [...document.querySelectorAll('mat-form-field, .mat-mdc-form-field')]
    .find(f => /Description/i.test(f.textContent));
  const sel = (field && field.querySelector('mat-select')) || document.querySelector('mat-select');
  if (!sel) return 'no mat-select found';
  sel.click();
  return 'opened ' + (sel.id || '(unnamed mat-select)');
})()"
npx agent-browser wait --fn "!!document.querySelector('.cdk-overlay-pane')"

# 2. Type in the CDK overlay search box via JS
npx agent-browser eval "(() => {
  const overlay = document.querySelector('.cdk-overlay-pane');
  const search = overlay.querySelector('input[placeholder=\"Search...\"]');
  search.focus();
  search.value = '<KEYWORD>';
  search.dispatchEvent(new Event('input', {bubbles: true}));
  return 'typed';
})()"
npx agent-browser wait 500

# 3. Read filtered options
npx agent-browser eval "(() => {
  const overlay = document.querySelector('.cdk-overlay-pane');
  return [...overlay.querySelectorAll('mat-option')]
    .filter(o => o.getBoundingClientRect().width > 0)
    .map(o => o.textContent.trim().substring(0, 100));
})()"

# 4. Click the matching option
npx agent-browser eval "(() => {
  const overlay = document.querySelector('.cdk-overlay-pane');
  for (const opt of overlay.querySelectorAll('mat-option')) {
    if (opt.getBoundingClientRect().width > 0 && opt.textContent.includes('<KEYWORD>')) {
      opt.click();
      return 'clicked: ' + opt.textContent.trim().substring(0, 80);
    }
  }
  return 'not found';
})()"
```

#### Material radio buttons

`click` on the ref works but may fail silently if the radio is below the viewport. Always
verify with eval after clicking:
```bash
npx agent-browser eval "(() => {
  const radios = document.querySelectorAll('input[type=\"radio\"]');
  return [...radios].filter(r => r.checked).map(r => ({name: r.name, value: r.value}));
})()"
```

### `eval` command rules

- **Always wrap in an IIFE:** `(() => { ... })()`. The eval shares a persistent JS context
  across calls — bare `const`/`let` declarations throw `SyntaxError: Identifier 'x' has
  already been declared` on the second call.
- **Return JSON-serializable values** (strings, numbers, arrays, objects). `eval` output is
  parsed by the CLI.

## Inputs to collect

Gather these before starting. Defaults reflect the common case shown in the reference flow;
confirm anything you defaulted.

| Field | Notes | Default |
|---|---|---|
| **PAN or TAN** | 10 characters. TAN for TDS/TCS deposits. | *required* |
| **Mobile number** | Receives the OTP. India (+91) by default. | *required* |
| **Tax Year** | e.g. `2026-27`. | latest available in dropdown |
| **Deductee type** (Major Head) | `Company` → *Corporation Tax (0020)*; `Non-Company / Other than Company` → *Income Tax (Other than Companies) (0021)*. ("Domestic company" ⇒ Company/0020.) | Company (0020) |
| **Residential status** | `Resident` or `Non-Resident` deductee(s). | Resident |
| **Minor Head** | If the portal asks: `TDS/TCS Payable by Taxpayer (200)` vs `(400)`. | 200 |
| **Section** | The nature-of-payment line. Give a code **or** a clear description/keyword (e.g. "professional fees", "rent", "contractor"). See section handling below. | *required* |
| **Amounts** | Any of: Tax, Surcharge, Education Cess, Interest, Late Fee, Penalty, Others. Only what applies; the rest stay ₹0. | Tax required; others 0 |
| **Payment mode + bank (preview only)** | The portal requires you to pick *some* tab + bank to reach the challan summary. Any payment mode (Debit Card / Net Banking / etc.) and any bank will do — no card/account details are entered. | whichever tab the user prefers; pick the first enabled bank option inside it |

If the user gave a natural-language request (e.g. "₹100 TDS on professional fees plus ₹100
interest"), map it onto these fields and read the mapping back before you start. Do **not**
hard-code a specific bank — the available banks can differ by payment mode, and the user
may have a preference. The choice of payment mode/bank in this skill is purely a vehicle to
reach the challan summary screen; it must never be assumed to be a payment instruction.

## Step-by-step workflow

### 1. Launch and open the portal
The config file from "One-time setup" supplies the sandbox/headless args and User-Agent, so
these commands need no env prefix. In shared or multi-user environments, do **not** use a
global browser teardown; start a fresh isolated browser session for this flow instead:
```bash
npx agent-browser open "https://eportal.incometax.gov.in/iec/foservices/#/e-pay-tax-prelogin/user-details"
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```
If the page doesn't render the form (blank/blocker/`ERR_EMPTY_RESPONSE`), confirm the config
file exists, then fall back to `references/browser-launch-and-blockers.md`.

### 2. Select the applicable Income Tax Act
On the user-details page, there is an "Applicable Income Tax Act" radio selector. Choose the
option referring to **Income Tax Act, 2025** (for Tax Year 2026-27 onwards). Locate it by its
label text from the snapshot rather than a fixed ref (generated refs like `e71` drift):
```bash
npx agent-browser snapshot -i --json
npx agent-browser find text "Income Tax Act, 2025" click   # or click its @ref from the snapshot
npx agent-browser find text "Continue" click
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```
If no such selector is present (older layout), skip this step and continue.

### 3. Enter PAN/TAN and mobile
Snapshot, then fill the three inputs by their refs. The page has:
- `PAN / TAN *` (the main input, masked with dots)
- `pan number input` (the confirm field)
- `Enter Mobile Number`

```bash
npx agent-browser snapshot -i --json
npx agent-browser fill @<pan_tan_ref>         "<PAN_OR_TAN>"
npx agent-browser fill @<confirm_pan_tan_ref> "<PAN_OR_TAN>"
npx agent-browser fill @<mobile_ref>          "<MOBILE>"
```

**IMPORTANT: Continue button is below the viewport fold** (headless viewport is 1280×577,
the button is at ~634px). There are also typically **3 "Continue" buttons** in the DOM.
After filling, scroll down and click by ref:
```bash
npx agent-browser scroll down 200
npx agent-browser snapshot -i --json          # get fresh refs after scroll
npx agent-browser click @<continue_ref>       # click by ref, not by text
npx agent-browser wait --text "OTP"
```

If Continue is disabled, re-snapshot and check for validation errors. If still stuck, try
the eval approach to find and click the visible Continue:
```bash
npx agent-browser eval "(() => {
  const btns = [...document.querySelectorAll('button')]
    .filter(b => b.textContent.trim() === 'Continue' && b.offsetParent !== null && !b.disabled);
  if (btns.length > 0) { btns[btns.length - 1].scrollIntoView({block:'center'}); btns[btns.length - 1].click(); return 'clicked'; }
  return 'none enabled';
})()"
```

### 4. OTP — STOP and ask the user
Do **not** attempt to bypass, guess, or auto-read the OTP. Pause here:

> "An OTP was just sent to the mobile ending in **…<last 2 digits>**. Please paste the
> 6-digit code so I can continue."

Wait for the reply.

**CRITICAL: `fill` and `keyboard type` do NOT work for OTP fields.** Angular's reactive
forms only respond to real keypress events. Use this exact pattern:

```bash
# Snapshot to get the OTP box refs
npx agent-browser snapshot -i --json
# Click first box, then press each digit as a real keystroke.
# Substitute the six digits the user just pasted in — do NOT hard-code them.
npx agent-browser click @otp_box_1 && npx agent-browser press <digit-1>
npx agent-browser click @otp_box_2 && npx agent-browser press <digit-2>
npx agent-browser click @otp_box_3 && npx agent-browser press <digit-3>
npx agent-browser click @otp_box_4 && npx agent-browser press <digit-4>
npx agent-browser click @otp_box_5 && npx agent-browser press <digit-5>
npx agent-browser click @otp_box_6 && npx agent-browser press <digit-6>
```

**Verify Continue is enabled** before clicking:
```bash
npx agent-browser eval "(() => { const b = [...document.querySelectorAll('button')].find(x => x.textContent.trim() === 'Continue' && x.offsetParent !== null); return b?.disabled ?? 'not found'; })()"
```

If `true` (disabled), dispatch Angular events as fallback:
```bash
npx agent-browser eval "(() => { document.querySelectorAll('input[type=\"password\"]').forEach(inp => { inp.dispatchEvent(new Event('input', {bubbles: true})); inp.dispatchEvent(new Event('change', {bubbles: true})); }); return 'dispatched'; })()"
npx agent-browser wait 1000
```

Then scroll and click Continue:
```bash
npx agent-browser scroll down 100
npx agent-browser snapshot -i --json          # get fresh refs
npx agent-browser scrollintoview @<continue_ref>
npx agent-browser click @<continue_ref>
npx agent-browser wait --load networkidle
```

The OTP is valid ~15 minutes with 3 attempts.

**Resend OTP flow:** If the user didn't receive the OTP, click **Resend OTP** (link, not
button). A confirmation toast appears with an **OK** button. **Dismiss the OK toast first**
before entering the new OTP. Re-snapshot after dismissing to get fresh refs (they change
after resend). Do not echo the mobile number from the toast in chat/logs.

### 5. Confirm identity and continue
A success banner appears ("successfully verified through mobile OTP") with the PAN/TAN and a
masked name. Sanity-check the PAN/TAN matches what the user gave you, then:
```bash
npx agent-browser snapshot -i --json
npx agent-browser scroll down 200              # Continue is below fold
npx agent-browser scrollintoview @<continue_ref>
npx agent-browser click @<continue_ref>
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```

### 6. Tax Year → Pay TDS/TCS
Select the tax year from the dropdown (it's a standard `mat-select` but NOT searchable —
just click and pick), then click **Proceed** on the **Pay TDS/TCS** card (the first of the
three Proceed buttons).
```bash
npx agent-browser click @<tax_year_dropdown>
npx agent-browser wait 500
npx agent-browser click @<tax_year_option>     # e.g. "2026-27"
# Click the FIRST Proceed button (for Pay TDS/TCS, not Pay Fee or Miscellaneous)
npx agent-browser click @<first_proceed_ref>
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```
If a **Minor Head** choice appears, pick **TDS/TCS Payable by Taxpayer (200)** unless the
user specified otherwise.

### 7. Deductee type (Major Head) + residential status
Two radio groups on the "Select Deductee Type" step. The radio refs change between pages.
```bash
npx agent-browser snapshot -i --json
# Major Head: Company → 0020, else Other than Company → 0021
npx agent-browser click @<company_radio_ref>       # for Company/0020
# Residential status:
npx agent-browser click @<resident_radio_ref>      # for Resident
```

**Verify both radios are selected** before continuing (clicks can silently fail):
```bash
npx agent-browser eval "(() => {
  const radios = document.querySelectorAll('input[type=\"radio\"]');
  return [...radios].filter(r => r.checked).map(r => ({name: r.name, value: r.value}));
})()"
```
Expected for Company + Resident: `[{"name":"mat-radio-group-1","value":"0020"},{"name":"mat-radio-group-2","value":"resident"}]`

If any radio is not checked, scroll down and re-click. Then continue:
```bash
npx agent-browser scroll down 200
npx agent-browser snapshot -i --json
npx agent-browser scrollintoview @<continue_ref>
npx agent-browser click @<continue_ref>
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```

Match the exact labels from the snapshot — the visible text includes the head code (0020 /
0021) which helps you confirm you picked the right one.

### 8. Section (nature of payment) + amounts
This is the highest-risk step — getting the section right matters.

**CRITICAL: The "Description" dropdown is an Angular Material `mat-select`.** In some portal
builds it exposes a CDK overlay **with** a search box; in others it is a plain option list with
**no search input at all**. `fill` and `keyboard type` do NOT work on either variant — use
`eval` to open the select, then either type into the search box if present or enumerate the
visible `mat-option` text and click the matching section. See the "Angular Material interaction
patterns" section above for the full eval approach. Summary:

```bash
# 1. Open the mat-select overlay by its "Description" label (not a generated id)
npx agent-browser eval "(() => {
  const field = [...document.querySelectorAll('mat-form-field, .mat-mdc-form-field')]
    .find(f => /Description/i.test(f.textContent));
  const sel = (field && field.querySelector('mat-select')) || document.querySelector('mat-select');
  sel.click();
  return sel ? 'opened' : 'no mat-select found';
})()"
npx agent-browser wait --fn "!!document.querySelector('.cdk-overlay-pane')"

# 2. Search in the CDK overlay
npx agent-browser eval "(() => {
  const overlay = document.querySelector('.cdk-overlay-pane');
  const search = overlay.querySelector('input[placeholder=\"Search...\"]');
  search.focus();
  search.value = '<KEYWORD>';
  search.dispatchEvent(new Event('input', {bubbles: true}));
  return 'typed';
})()"
npx agent-browser wait 500

# 3. Read filtered options and pick the right one
npx agent-browser eval "(() => {
  const overlay = document.querySelector('.cdk-overlay-pane');
  for (const opt of overlay.querySelectorAll('mat-option')) {
    if (opt.getBoundingClientRect().width > 0 && opt.textContent.includes('<KEYWORD>')) {
      opt.click();
      return 'clicked: ' + opt.textContent.trim().substring(0, 80);
    }
  }
  return 'not found';
})()"
```

The portal shows the resolved **Section** text and a numeric **Code** after selection — read
them back to the user and **confirm before entering amounts** if there's any ambiguity or
more than one plausible match. (Note: under the Income Tax Act 2025 the section numbering is
new, e.g. professional fees appears under §393(1); don't assume old §194x numbers — search by
description and confirm.)

**Enter the section amounts** using standard `fill` (these are regular text inputs, not
mat-select):
```bash
npx agent-browser fill @<tax_ref>       "<TAX>"        # (a) Tax
npx agent-browser fill @<surcharge_ref> "<SURCHARGE>"  # (b) Surcharge  (0 if n/a)
npx agent-browser fill @<cess_ref>      "<CESS>"       # (c) Education Cess (0 if n/a)
npx agent-browser scroll down 300        # Add button may be below fold
npx agent-browser find text "Add" click  # commits the section line
npx agent-browser snapshot -i --json     # verify the line was added / total updated
```
The **Add** button stays disabled until at least one amount is entered. Identify the three
amount inputs by their labels — (a) Tax, (b) Surcharge, (c) Education Cess — from the
snapshot; do **not** rely on generated ids like `mat-input-6/7/8`, which shift between portal
releases.

**Enter other payments** (all optional, default ₹0) in "Details of Other payments":
```bash
npx agent-browser fill @<interest_ref> "<INTEREST>"    # (d) Interest
npx agent-browser fill @<late_fee_ref> "<LATE_FEE>"    # (e) Late Fee under section 427
npx agent-browser fill @<penalty_ref>  "<PENALTY>"     # (f) Penalty
npx agent-browser fill @<others_ref>   "<OTHERS>"      # (g) Others
```
Then continue:
```bash
npx agent-browser snapshot -i --json          # fresh refs
npx agent-browser scroll down 300
npx agent-browser scrollintoview @<continue_ref>
npx agent-browser click @<continue_ref>
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```

### 9. Verify tax break-up → continue again
A review / "Verify Tax Break Up Details" step summarises the challan. Confirm the totals look
right, then:
```bash
npx agent-browser snapshot -i --json
npx agent-browser scroll down 300
npx agent-browser scrollintoview @<continue_ref>
npx agent-browser click @<continue_ref>
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```

### 10. Payment mode (any) → reach the challan summary
The portal's "Add Payment Details" step requires you to choose **some** payment-mode tab and
**some** bank option before the challan summary/preview page is shown. **No payment is
made**, no card or account details are ever entered — the choice is purely a vehicle to
unlock the summary screen so you can pick **Pay Later** and capture the CRN.

**Do not hard-code a specific bank or a specific tab.** The list of enabled banks differs
per payment mode and per user (some are gated, some are region-locked), and the user may
have a stated preference. Pick the first available bank option in the chosen tab. The same
default works for almost everyone; if a particular tab is empty for the user, switch tabs
and pick the first available bank there.

```bash
npx agent-browser wait --text "Debit Card"   # or any other payment-mode label the snapshot shows
npx agent-browser snapshot -i --json

# If the payment-mode tabs are not all visible, find them by label rather than relying on
# a generated ref (refs like @e12 drift between portal releases). The exact labels vary by
# build — use the live snapshot to enumerate them, then pick one (Debit Card is shown below
# as an illustrative example; substitute whatever the user prefers, or any enabled tab).
npx agent-browser eval "(() => {
  const tabs = document.querySelectorAll('.mat-mdc-tab-labels > *');
  for (const t of tabs) {
    if (t.textContent.includes('Debit Card')) { t.click(); return 'clicked Debit Card tab'; }
  }
  return 'not found: ' + [...tabs].map(t => t.textContent.trim()).join(', ');
})()"
npx agent-browser wait 1000
npx agent-browser snapshot -i --json

# Pick the FIRST enabled bank option in the active tab — do not hard-code a bank name.
npx agent-browser eval "(() => {
  const inputs = [...document.querySelectorAll('input[type=\"radio\"]')];
  const visible = inputs.filter(r => r.offsetParent !== null && !r.disabled);
  if (visible.length === 0) return 'no enabled bank radios';
  visible[0].click();
  return 'picked: ' + (visible[0].value || visible[0].id || '(unnamed)');
})()"
npx agent-browser snapshot -i --json

npx agent-browser find text "Continue" click
npx agent-browser wait --load networkidle
npx agent-browser snapshot -i --json
```

If the tab content is empty, repeat the eval on the next tab label until one renders. If
every tab is empty, capture a screenshot, get the body text, and stop — the portal has
changed and the skill needs a fresh look at the live DOM.

### 11. Pay Later → capture the CRN
On the challan summary/preview page, choose **Pay Later** (NOT "Pay Now"). The portal
generates and displays a **CRN**.
```bash
npx agent-browser find text "Pay Later" click
npx agent-browser wait --load networkidle
npx agent-browser snapshot --json                  # full snapshot to read the CRN text
npx agent-browser screenshot ./challan-crn.png     # keep visual proof of the CRN + amounts
```
Extract the CRN (a long numeric reference, often labelled "CRN" / "Challan Reference
Number"). If it's easier, read it directly:
```bash
npx agent-browser find text "CRN" text             # or get text from the CRN element's ref
```

## Output

Report back to the user, clearly:
- **CRN** (the challan reference number) — the key deliverable.
- PAN/TAN, Tax Year, Major Head (0020/0021), Residential status, Section (text + code).
- Amount breakdown (Tax / Surcharge / Cess / Interest / Late Fee / Penalty / Others) and the
  **grand total**.
- The payment mode + bank option that was selected to reach the summary (informational
  only — no payment was made).
- CRN **validity** if the page states it, and a reminder that payment is still pending — the
  CRN must be paid at an authorised bank/channel before it expires.
- Path to the saved screenshot (`./challan-crn.png`).

Then leave the browser as-is (or `npx agent-browser close` if the user is done).

## Troubleshooting

- **If the portal stalls during launch:** use the fallback browser path in `references/browser-launch-and-blockers.md` — start Chrome under `xvfb-run` with remote debugging, then `agent-browser connect` to that CDP endpoint and continue from there.
- **"Continue" won't click / is disabled:** a mandatory field is empty or invalid. Re-snapshot,
  look for red inline errors, fix, retry. Also check if the button is below the viewport fold
  — scroll down and click by ref.
- **"Continue" click succeeds but page doesn't advance:** The portal's tall layout often
  pushes the Continue button below the viewport fold (observed: `top=634` when viewport is
  only 577px tall in headless 1280×577). `find text "Continue"` reports success but the click
  lands off-screen. **Fix:** scrollintoview or scroll down, re-snapshot, click by ref.
  ```bash
  npx agent-browser scrollintoview @<continue_ref>
  npx agent-browser click @<continue_ref>
  ```
  Diagnostic:
  ```bash
  npx agent-browser eval "(() => { const b = [...document.querySelectorAll('button')].find(x => x.textContent.includes('Continue')); const r = b.getBoundingClientRect(); return 'top=' + r.top + ' viewport=' + window.innerHeight; })()"
  ```
- **Multiple "Continue" buttons on the same page:** The portal renders several Continue
  buttons (for different sections/steps). `find text "Continue" click` picks the first DOM
  match, which may be an invisible one. After scrolling, re-snapshot and click by `@eN`.
- **OTP fields filled but Continue stays disabled:** `fill` and `keyboard type` don't trigger
  Angular change detection. Use `click @ref && press <digit>` per box (see Step 4).
- **Resend OTP shows toast with OK button:** Must dismiss the OK toast before entering new
  OTP. Re-snapshot after dismissing — refs change.
- **`eval` command variable collisions:** Always wrap eval code in an IIFE:
  `(() => { ... })()`.
- **Page shows "Unauthorized" after reload:** NEVER use `reload`. The SPA session dies. Use
  `back` or restart from Step 1 with a fresh OTP.
- **Labels differ from these examples:** the portal's wording/layout can change. Always trust
  the live `snapshot -i` over the literal strings here; find the closest matching control.
- **Dropdown option not found after typing:** broaden the search term (fewer words / just the
  keyword), `wait 500`, re-snapshot. The list is long and virtualised — scroll if needed.
- **OTP page timed out:** click **Resend OTP** once the countdown allows, ask the user for the
  new code, and refill.
- **Landed on a real bank payment page:** you went too far. Do **not** enter anything —
  `npx agent-browser back` to the summary and choose **Pay Later** instead.
- **Pay Later click looks inert / CRN page not yet visible:** the preview page can take a moment
to settle. Re-read the live body text, then click the visible **Pay Later** button by JS if the
ref click is unreliable; confirm the next page says **Challan Details** and shows a CRN before
reporting success.
- **Session dropped / logged out mid-flow:** restart from Step 1; a fresh OTP will be needed.
- **Payment-mode tab is empty / no bank radios enabled:** switch to the next tab via the
  same `eval` approach and pick the first enabled bank option there. If every tab is empty,
  capture a screenshot and stop — the portal has changed.

## Notes

- This is the **Income Tax Act 2025** challan (applicable Tax Year 2026-27 onwards). For older
  years the portal routes to the legacy Challan 281 flow, where step labels differ — if you see
  that, tell the user rather than forcing this path.
- See `references/headless-2026-27-flow-notes.md` and `references/2026-07-session-notes.md` for
  the July 2026 portal observations, including the headless navigation quirk where a visible
  **Continue** may need a direct JS click and the same-session repeat-CRN pattern.
  See `references/script-map.md` for the current function-level script/LLM split.
- Up to 20 section codes can go on one challan; this skill handles one section line by default.
  If the user needs several, repeat Step 8 (select section → amounts → **Add**) for each before
  continuing.
- The choice of payment mode + bank in Step 10 is **only** a vehicle to reach the challan
  summary; it must never be treated as a payment instruction. No card/account/netbanking
  credentials are ever entered, and the skill always finishes by selecting **Pay Later**.

See `references/hybrid-script-llm-split.md` for a concise summary of the script/LLM boundary
and the current session-reuse guidance.
