---
name: cold-outreach-builder
description: >-
  Interactive, beginner-friendly builder for a personal cold-email / outreach
  automation tool. Use when someone wants to build (or reverse-engineer) an
  outreach app from scratch. It interviews them in plain English about how they
  want to send (SMTP/API), where their contacts come from, who they're targeting,
  and what their emails say, then scaffolds a complete paced-sending tool with a
  dashboard, a database log, automatic dedupe, daily caps, and a send-time window.
  Triggers: "build an outreach tool", "cold email app", "email campaign tool",
  "outreach automation", "reverse engineer this outreach project".
---

# Cold Outreach Builder

> **What this skill is.** It's a recipe + interviewer. When someone activates it,
> you (the AI) interview them about how they want to do outreach, then build them
> their *own* complete tool — their email account, their keys, their message
> scripts. They don't need to know how to code. You do the building; you explain
> as you go.

---

## ⚠️ READ THIS FIRST — how you (the AI) must behave

You are helping a person who **may not know how to code at all**. Treat them like a
smart friend who can copy-paste and follow click-by-click steps, but who cannot read
code and should never be made to feel dumb. Follow this exactly:

1. **Do not write any code yet.** First, say hello and explain in one or two plain
   sentences what you're about to build together.

2. **Offer two paths:**
   - **Express path** — "I'll pick safe, sensible defaults for everything. I only
     need two things from you: which email address you'll send from, and a one-time
     app password. ~10 minutes." (Recommend this for beginners.)
   - **Guided path** — "I'll ask you about 7 short questions so it's exactly how you
     want it. ~20 minutes."

3. **Run the interview** (see *Section 3*). Ask in small batches, plain English.
   **Always offer a recommended default.** If they say "I don't know," use the
   default and move on. Never make them make a technical decision they don't
   understand.

4. **Before building, confirm.** Show their choices as a short bullet list and ask
   "Look good?" Fix anything, then proceed.

5. **Build in the order in *Section 7*.** As you create each file, say in **one
   sentence** what it's for. Do **not** paste walls of unexplained code at them.
   Code blocks in this skill are your reference — the person doesn't need to read
   them.

6. **Walk them through setup and the smoke test** (*Section 9* and *Section 7*).
   Send one test email to their own address together, and confirm it logged.

7. **If something errors, explain the fix in plain words.** No jargon dumps.

**Tone:** friendly, encouraging, concrete. Celebrate the moment it sends the first
email — that's the payoff.

---

## 0. Before you start (plain-English primer)

**What you're building, in one sentence:** a little app on your own computer that
sends personalized emails for you — slowly and safely so they don't look like spam —
and keeps a list of everyone you've contacted so nobody gets the same email twice.

**What you need:**
- An email account you can send from (a normal Gmail works great).
- About 20 minutes.
- Willingness to copy-paste a few things. That's it.

**A 6-word glossary** (you'll see these terms once or twice — here's what they mean):

| Term | Plain meaning |
|------|---------------|
| **SMTP** | The "send mail" doorway every email provider has. We just point the app at it. |
| **App password** | A special one-time password you generate so the app can log into your email *without* using your real password. Safer. |
| **API key** | A secret code that lets the app talk to an outside service (like a contact-finder). Optional — only if you want one. |
| **Terminal** | The black text window where you type a command to start the app. We'll show you exactly what to type. |
| **Environment variable** | A setting kept in a hidden file called `.env` (your passwords/keys) so they're never mixed into the code. |
| **Database** | A single file (`outreach.db`) that quietly remembers who you've emailed. You never open it by hand. |

You will **not** need to understand any code. The AI writes it; you run it.

---

## 1. What you're building

```
Find contacts          Pick a template         Send slowly & safely        Remember forever
(CSV / API / paste) --> (per contact)     -->  (1 email every 7-9 min,  -->  (database: never
                                               only 9am-5pm, daily cap)      email anyone twice)
```

**The one important idea (a "two-part" design):**

- The **Dashboard** (`app.py`) is the screen you click around in — pick contacts,
  preview the email, hit **Start**.
- When you hit Start, it launches a **separate background sender**
  (`run_campaign.py`) that keeps going **even if you close the browser**.
- The two parts talk to each other through a few small text files (JSON) and the
  database. That's why your campaign doesn't stop just because you walked away.

This separation is the single best design decision in the whole tool. Keep it.

---

## 2. The pieces (file map)

| File | Plain-English job |
|------|-------------------|
| `app.py` | The dashboard you click. Streamlit turns Python into a web page automatically. |
| `mailer.py` | The careful mail-sender: pacing, the 9-5 window, the daily cap, the "don't email twice" check. **The heart of the tool.** |
| `run_campaign.py` | The background worker the dashboard launches so sending survives the browser closing. |
| `db.py` | The memory. Creates the database and answers "have we emailed this person?" and "how many did we send today?" |
| `templates.py` | Your email scripts, with blanks like `{{first_name}}` that get filled in per person. |
| `sources/` (e.g. `csv_source.py`) | Where contacts come from. CSV is simplest; APIs/scrapers are optional. |
| `.env` | Your secrets (email login, keys). **Never shared, never committed.** |
| `requirements.txt` | The list of free add-ons the app needs. One command installs them all. |

---

## 3. The interview (ask these BEFORE building)

Ask in plain English. Each question has a **Recommended** answer for anyone unsure.
In **Express mode**, silently use every Recommended answer and only ask Q1's email +
app password.

**Q1 — How will you send email?**
- *Gmail* — **Recommended.** Free, easy, works for low volume. (Needs a one-time app
  password — you'll walk them through it in Section 9.)
- *Outlook / Office 365* — good if that's their work/school email.
- *A sending service (SendGrid, Mailgun, Amazon SES)* — better for higher volume;
  uses an API key instead of a password.
- *Other SMTP* — they paste host/port from their provider.
> Capture: provider, the from-address, and either an app password or API key.
> Why it matters: this is literally how mail leaves the building.

**Q2 — How careful should the pacing be?**
- **Recommended defaults:** max **20 emails/day**, one every **7–9 minutes**, only
  between **9am and 5pm** on weekdays, in their timezone.
- Tell them: slower + smaller is safer for staying out of spam folders. They can
  raise it later.
> Capture: daily cap, delay range, send-window hours, timezone.

**Q3 — Where do your contacts come from?** (pick any)
- *Upload a CSV* — **Recommended / simplest.** A spreadsheet with columns like
  first name, last name, email, company.
- *Paste a few by hand* — fine for tiny lists.
- *A contact-finding API* (e.g. Hunter.io to find emails from a website, Apollo to
  find people at a company) — optional, needs a free API key.
- *A directory scraper* (like pulling startups from a public list) — advanced,
  optional.
> Capture: which sources to enable.

**Q4 — Who are you trying to reach?**
- Ask: what kinds of companies or roles? (e.g. "banks," "startups," "recruiters,"
  "marketing managers"). This is just so you can label things sensibly and set up
  optional auto-routing (e.g. a bank gets the "bank" script).
> Capture: segments, and any "if company looks like X, use script Y" rules.

**Q5 — Your email scripts.**
- *Write my own* — they paste their wording; you wire in the `{{blanks}}`.
- *Give me a starting template I can edit* — **Recommended.** You provide a clean
  generic script and they tweak it.
- *Draft one for me* — they describe the goal ("I'm a student asking for a 15-min
  call") and you write it.
- Explain the available blanks: `{{first_name}}`, `{{company_name}}`,
  `{{sender_name}}`.
> Capture: one or more templates, each with a subject + body.

**Q6 — Where will it run?**
- *Just on my computer* — **Recommended** to start. Nothing to deploy.
- *Online, always on (Railway/Render/Fly)* — optional; you'll add a deploy file.

**Q7 — Password-protect the dashboard?**
- *No* — **Recommended** for local-only use.
- *Yes* — set one password; good if they deploy it online.

After Q7: **summarize their picks and confirm before writing anything.**

---

## 4. The contact schema (the one rule that makes everything fit)

Every contact — no matter where it came from (CSV, API, hand-typed) — must end up as
a simple record with these fields. This single shared shape is *why* you can swap
contact sources freely: the database, the sender, and the templates all expect the
same thing.

```python
# A contact is just a dictionary with these keys.
# Required:
#   first_name, last_name, email, title, organization_name
# Optional extras some sources add:
#   is_alum, batch, email_confidence, _template_key (which script to use for them)
contact = {
    "first_name": "Jordan",
    "last_name": "Lee",
    "email": "jordan@acme.com",
    "title": "Recruiter",
    "organization_name": "Acme Inc.",
}
```

**Rule for you (the AI):** every contact source you build must output exactly this
shape (extra keys are fine; the five required ones are not optional). If a CSV calls
the column `company_name`, map it to `organization_name` on import.

---

## 5. The components (reference code — explain, don't dump)

> Everything below is your blueprint. Embed/adapt the **hard parts** verbatim (they
> encode lessons that are easy to get wrong). For each file you create, tell the
> person *one sentence* about what it does — they do not need to see or understand
> the code.

### 5a. `db.py` — the memory (dedupe + daily count)

*Say to the user:* "This file creates a small database that remembers everyone you
email, so no one ever gets the same message twice, and it counts how many you've
sent today."

```python
import os, sqlite3
from datetime import datetime
import pytz

# Keep data next to the app (works on Windows, Mac, and servers alike).
DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(DATA_DIR, "outreach.db")
TZ = pytz.timezone(os.getenv("TIMEZONE", "America/Toronto"))

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS outreach_log (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                email         TEXT UNIQUE NOT NULL,   -- UNIQUE = the dedupe guarantee
                first_name    TEXT,
                last_name     TEXT,
                company       TEXT,
                title         TEXT,
                template_key  TEXT,
                sent_at       TEXT,
                status        TEXT DEFAULT 'sent'
            )
        """)
        conn.commit()

def is_already_contacted(email):
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            "SELECT 1 FROM outreach_log WHERE email = ?", (email,)
        ).fetchone() is not None

def log_contact(contact, template_key):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """INSERT OR IGNORE INTO outreach_log
               (email, first_name, last_name, company, title, template_key, sent_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (contact.get("email"), contact.get("first_name"), contact.get("last_name"),
             contact.get("organization_name"), contact.get("title"), template_key,
             datetime.now(TZ).isoformat()),
        )
        conn.commit()

def count_sent_today():
    today = datetime.now(TZ).strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT COUNT(*) FROM outreach_log WHERE sent_at LIKE ?", (f"{today}%",)
        ).fetchone()
    return row[0] if row else 0

def get_all_logs():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM outreach_log ORDER BY sent_at DESC").fetchall()
    return [dict(r) for r in rows]
```

### 5b. `mailer.py` — the careful sender (the heart)

*Say to the user:* "This is the part that actually sends the emails — but politely:
it waits a few minutes between each one, stops outside your chosen hours, never goes
over your daily limit, and skips anyone you've already contacted."

The **order of the safety checks matters** — keep it: stop-request → send-window →
daily-cap → already-contacted → send → wait.

```python
import os, smtplib, time, json, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
import db, templates

DATA_DIR    = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
STATUS_FILE = os.path.join(DATA_DIR, "campaign_status.json")
STOP_FILE   = os.path.join(DATA_DIR, "campaign_stop.flag")
TZ          = pytz.timezone(os.getenv("TIMEZONE", "America/Toronto"))

# --- All sending settings come from .env, so nothing is hard-coded ---
SMTP_HOST   = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT   = int(os.getenv("SMTP_PORT", "587"))
SMTP_SSL    = os.getenv("SMTP_USE_SSL", "false").lower() == "true"  # True for port 465
DAILY_CAP   = int(os.getenv("DAILY_CAP", "20"))
HOUR_START  = int(os.getenv("SEND_HOUR_START", "9"))
HOUR_END    = int(os.getenv("SEND_HOUR_END", "17"))
DELAY_MIN   = int(os.getenv("SEND_DELAY_MIN_SECONDS", str(7 * 60)))
DELAY_MAX   = int(os.getenv("SEND_DELAY_MAX_SECONDS", str(9 * 60)))

def _write_status(s):
    try:
        with open(STATUS_FILE, "w") as f: json.dump(s, f)
    except OSError: pass

def read_status():
    try:
        with open(STATUS_FILE) as f: return json.load(f)
    except (OSError, json.JSONDecodeError): return {}

def request_stop():
    with open(STOP_FILE, "w") as f: f.write("stop")

def clear_stop_request():
    try: os.remove(STOP_FILE)
    except OSError: pass

def stop_requested():
    return os.path.exists(STOP_FILE)

def is_within_send_window():
    return HOUR_START <= datetime.now(TZ).hour < HOUR_END

def send_email(to_email, subject, body):
    """Send one plain-text email. Returns True if it went out."""
    user = os.getenv("SMTP_USER"); password = os.getenv("SMTP_PASSWORD")
    msg = MIMEMultipart("alternative")
    msg["Subject"], msg["From"], msg["To"] = subject, user, to_email
    msg.attach(MIMEText(body, "plain"))
    try:
        if SMTP_SSL:
            server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30)
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
            server.ehlo(); server.starttls()
        with server:
            server.login(user, password)
            server.sendmail(user, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[mailer] could not send to {to_email}: {e}")
        return False

def paced_send(contacts, template_key=None):
    """Send to each contact slowly, with all the safety checks."""
    db.init_db(); clear_stop_request()
    sender_name = os.getenv("SENDER_NAME", "")

    for idx, contact in enumerate(contacts):
        email     = contact.get("email", "")
        remaining = contacts[idx + 1:]
        tmpl      = contact.get("_template_key") or template_key

        if stop_requested():                                   # 1. user hit "End"
            _write_status({"state": "idle", "stop_reason": "manual_stop",
                           "remaining_count": len(contacts[idx:])}); return
        if not tmpl:                                            #    no script -> skip
            continue
        if not is_within_send_window():                        # 2. outside 9-5
            _write_status({"state": "idle", "stop_reason": "outside_window",
                           "remaining_count": len(contacts[idx:])}); break
        if db.count_sent_today() >= DAILY_CAP:                 # 3. hit daily cap
            _write_status({"state": "idle", "stop_reason": "daily_cap",
                           "remaining_count": len(contacts[idx:])}); break
        if db.is_already_contacted(email):                    # 4. already emailed
            continue

        _write_status({"state": "sending", "to": email,        # 5. render + send
                       "remaining_count": len(remaining)})
        subject, body = templates.render(tmpl, contact, sender_name)
        if send_email(email, subject, body):
            db.log_contact(contact, tmpl)
            print(f"[mailer] sent to {email}")

        delay = random.randint(DELAY_MIN, DELAY_MAX)           # 6. wait 7-9 min
        _write_status({"state": "waiting", "last_sent_to": email,
                       "next_send_at": datetime.now(TZ).timestamp() + delay,
                       "remaining_count": len(remaining)})
        end = time.time() + delay
        while time.time() < end:                               #    but stay stoppable
            if stop_requested():
                _write_status({"state": "idle", "stop_reason": "manual_stop",
                               "remaining_count": len(remaining)}); return
            time.sleep(1)

    _write_status({"state": "idle", "remaining_count": 0})
```

### 5c. `run_campaign.py` — the background worker

*Say to the user:* "This is the helper the dashboard launches in the background so
your campaign keeps sending even after you close the browser."

```python
# -*- coding: utf-8 -*-
import sys, io
# Windows fix: make sure printing names with accents/emoji never crashes.
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import json, os
import db, mailer

db.init_db()

# The dashboard passes "email:templatekey" pairs and drops the full contact
# details into contacts_cache.json. We match them back up here.
DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
pairs = [a for a in sys.argv[1:] if ":" in a]

try:
    with open(os.path.join(DATA_DIR, "contacts_cache.json")) as f:
        contact_map = {c["email"]: c for c in json.load(f)}
except (OSError, json.JSONDecodeError):
    contact_map = {}

contacts = []
for pair in pairs:
    email, tmpl = pair.rsplit(":", 1)
    c = contact_map.get(email, {"email": email, "first_name": "", "last_name": "",
                                "organization_name": "", "title": ""})
    c["_template_key"] = tmpl
    contacts.append(c)

mailer.paced_send(contacts)
print("[run_campaign] done.")
```

### 5d. `templates.py` — the email scripts

*Say to the user:* "These are your email scripts. The `{{blanks}}` get filled in
automatically for each person — their first name, their company, your name."

```python
# Each template = a subject + body. Blanks: {{first_name}} {{company_name}} {{sender_name}}
TEMPLATES = {
    "intro": {
        "subject": "Quick question, {{first_name}}",
        "body": (
            "Hi {{first_name}},\n\n"
            "[One or two sentences on who you are and why you're reaching out to "
            "{{company_name}} specifically.]\n\n"
            "[Your small ask — e.g. a 15-minute call this week.]\n\n"
            "Thanks for reading,\n"
            "{{sender_name}}"
        ),
    },
    # Add more named scripts as needed, e.g. "bank", "tech", "recruiter".
}

def render(template_key, contact, sender_name):
    """Fill the blanks in a template for one contact. Returns (subject, body)."""
    if template_key not in TEMPLATES:
        raise KeyError(f"Unknown template: {template_key!r}. Have: {list(TEMPLATES)}")
    tmpl = TEMPLATES[template_key]
    fills = {
        "{{first_name}}":   contact.get("first_name", ""),
        "{{company_name}}": contact.get("organization_name", ""),
        "{{sender_name}}":  sender_name,
    }
    subject, body = tmpl["subject"], tmpl["body"]
    for blank, value in fills.items():
        subject = subject.replace(blank, value)
        body    = body.replace(blank, value)
    return subject, body

def auto_template(company):
    """Optional: auto-pick a script from the company name. Tweak to taste."""
    c = (company or "").lower()
    if any(k in c for k in ["bank", "capital", "financial", "finance"]): return "bank"
    if any(k in c for k in ["tech", "software", "labs", "ai"]):          return "tech"
    return "intro"
```

### 5e. Contact sources (pick what Q3 asked for)

**The contract:** every source returns a `list` of contacts in the *Section 4* shape.

**CSV import — build this one by default.** *Say:* "This lets you upload a spreadsheet
of contacts."

```python
import pandas as pd

def load_csv(path_or_file):
    df = pd.read_csv(path_or_file)
    df.columns = [c.strip().lower() for c in df.columns]   # tidy headers
    if "company_name" in df.columns:                       # normalize to our schema
        df["organization_name"] = df["company_name"]
    return [row for row in df.to_dict(orient="records") if row.get("email")]
```

**Optional — find emails via an API (reference pattern).** Only build if Q3 asked for
it. *Say:* "This finds work emails for you from a company website, using a free
Hunter.io key." Keep network calls defensive (timeouts, handle non-200, return `[]`
on failure). The same pattern adapts to Apollo, Clearbit, etc.

```python
import os, requests

def find_emails_hunter(domain, min_confidence=50):
    key = os.getenv("HUNTER_API_KEY", "")
    if not key: return []
    try:
        r = requests.get("https://api.hunter.io/v2/domain-search",
                         params={"domain": domain, "api_key": key, "limit": 10}, timeout=10)
    except requests.RequestException:
        return []
    if r.status_code != 200: return []
    out = []
    for e in r.json().get("data", {}).get("emails", []):
        if (e.get("confidence") or 0) >= min_confidence and e.get("value"):
            out.append({
                "first_name": e.get("first_name", ""), "last_name": e.get("last_name", ""),
                "email": e["value"], "title": e.get("position", ""),
                "organization_name": domain, "email_confidence": e.get("confidence"),
            })
    return out
```

**Optional — directory scraper.** Same idea: hit a public listing, then run each
company domain through the email finder. Advanced; only if asked.

### 5f. `app.py` — the dashboard (describe structure, embed the 2 tricky bits)

*Say to the user:* "This is the screen you'll actually use. It has tabs to load
contacts, start a campaign, and see your history."

Lay it out with `st.tabs(["Run Campaign", "Log", "Settings"])`. In *Run Campaign*:
let them load contacts (Q3 source), show a checkbox list, pick a template per person,
preview the first email, then a **Start** button. The two load-bearing pieces:

**(1) The live status bar** — refreshes itself by reading the status file the mailer
writes:

```python
import streamlit as st
from datetime import datetime
import pytz, mailer
TZ = pytz.timezone("America/Toronto")

@st.fragment(run_every=10)   # re-runs every 10 seconds on its own
def campaign_status_bar():
    s = mailer.read_status()
    state = s.get("state")
    if state == "waiting":
        secs = max(0, int(s.get("next_send_at", 0) - datetime.now(TZ).timestamp()))
        st.info(f"Running — next email in {secs // 60}m {secs % 60}s · "
                f"{s.get('remaining_count', 0)} left")
    elif state == "sending":
        st.warning(f"Sending to {s.get('to', '')}…")
    elif state == "idle":
        st.success("Campaign finished (or paused). Nothing sending right now.")

campaign_status_bar()
```

**(2) The Start button → launches the background sender:**

```python
import os, sys, json, subprocess

# Save the full contact details so the background worker can look them up,
# then launch it and immediately return control to the dashboard.
DATA_DIR = os.getenv("DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(DATA_DIR, "contacts_cache.json"), "w") as f:
    json.dump(contacts, f)

pairs = [f"{c['email']}:{chosen_template_for(c)}" for c in to_send]  # email:template
subprocess.Popen([sys.executable, "run_campaign.py"] + pairs,
                 cwd=os.path.dirname(os.path.abspath(__file__)))
st.success(f"Started for {len(to_send)} contact(s) — runs in the background. "
           f"You can close this tab.")
```

Add a **Log** tab (`db.get_all_logs()` in a table) and a **Settings** tab (show the
send window, daily cap, and let them set their display name).

### 5g. Config files

**`.env.example`** (they copy it to `.env` and fill in their real values):

```bash
# --- How you send ---
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_SSL=false          # set true (and PORT 465) if your provider needs SSL
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your_app_password_here
SENDER_NAME=Your Name

# --- Pacing & safety ---
TIMEZONE=America/Toronto
DAILY_CAP=20
SEND_HOUR_START=9
SEND_HOUR_END=17

# --- Optional contact-source keys (leave blank if unused) ---
HUNTER_API_KEY=
APOLLO_API_KEY=

# --- Optional dashboard password (leave blank for none) ---
DASHBOARD_PASSWORD=
```

**`requirements.txt`:**

```
streamlit
pandas
python-dotenv
pytz
requests
```

**`.gitignore`** (so secrets and personal data never get shared):

```
.env
outreach.db
campaign_status.json
campaign_stop.flag
contacts_cache.json
campaign_queue.json
*.csv
__pycache__/
.venv/
```

---

## 6. Swap points (so anyone can do it their own way)

| You want to change… | Default | How to swap |
|---|---|---|
| **Email provider** | Gmail (SMTP, port 587) | Change `SMTP_*` in `.env`. For SendGrid/Mailgun/SES, use their SMTP host + an API key as the password, or their HTTP API in `send_email`. |
| **Where contacts come from** | CSV upload | Add a file in `sources/` that returns the *Section 4* shape. Nothing else changes. |
| **Email scripts** | One generic `intro` template | Add entries to `TEMPLATES`; optionally route with `auto_template`. |
| **Storage** | SQLite file (`outreach.db`) | Swap the three `db.py` functions to Postgres/MySQL; keep the function names. |
| **Where it runs** | Your computer | Add `railway.toml` (or Render/Fly config) and a mounted data folder; set `DATA_DIR` to it. |
| **Pacing** | 20/day, 7-9 min, 9-5 | All in `.env` — no code changes. |

*Railway deploy file (only if Q6 = online):*

```toml
[build]
builder = "nixpacks"
[deploy]
startCommand = "streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"
[[volumes]]
mountPath = "/data"     # then set DATA_DIR=/data in the host's env vars
```

---

## 7. Build order + smoke test

Build in this order (each step is small; explain each in one sentence as you go):

1. `requirements.txt`, `.env.example`, `.gitignore` — the setup files.
2. `db.py` — the memory.
3. `templates.py` — the scripts (use Q5 answers).
4. `mailer.py` — the sender.
5. `run_campaign.py` — the background worker.
6. One contact source (CSV by default) in `sources/`.
7. `app.py` — the dashboard.

**Smoke test (do this WITH them):**
1. Finish setup (*Section 9*): make `.env`, install requirements.
2. Start the app: `streamlit run app.py`.
3. Load **one** contact whose email is **their own address**.
4. Temporarily set the send window to the current hour (or note YC-style "anytime"
   exceptions) so it sends now.
5. Hit Start. Within a minute they get the email. 🎉
6. Hit Start again with the same contact — confirm it **skips** (dedupe works).
7. Check the **Log** tab — the send is recorded.

If the email arrives and the second run skips it, the whole machine works.

---

## 8. Guardrails & hard-won gotchas (bake these in)

These come from a real, working version of this tool — they save hours of debugging:

- **Windows printing crash:** put the UTF-8 `sys.stdout` wrapper (see `run_campaign.py`)
  at the top of any script that prints contact names, or accented names crash it.
- **"Database not found" on different machines:** always build paths from
  `os.path.abspath(__file__)` / `DATA_DIR` — never assume the current folder.
- **SSL vs TLS:** port **587** uses `starttls()`; port **465** uses `SMTP_SSL`. The
  `SMTP_USE_SSL` flag covers both. Wrong combo = silent login failures.
- **Deliverability (staying out of spam):** keep it plain-text, keep volume low, keep
  the random delay, avoid raw tracking links, and warm up slowly. Conservative caps
  protect your email account's reputation.
- **Compliance — this matters, say it plainly to the user:** use a real, honest
  identity, make it easy to opt out (a simple "reply STOP / let me know and I won't
  follow up" line is a good minimum), and know the rules where you and your
  recipients are (e.g. **CAN-SPAM** in the US, **CASL** in Canada, **GDPR** in the
  EU). This tool sends real email from a real account — use it respectfully or it can
  get the account suspended.
- **Secrets hygiene:** real credentials live only in `.env`; use an **app password**,
  never your real email password; `.env` is git-ignored and never shared.

---

## 9. Getting set up (beginner appendix — spell it all out)

Walk the user through these. Don't assume any of it is obvious.

**A. Install Python (if they don't have it)**
- Go to <https://www.python.org/downloads/> and install the latest version.
- **Windows:** on the first install screen, tick **"Add Python to PATH"** before
  clicking Install. (This is the #1 thing beginners miss.)

**B. Get a Gmail app password (the easy send method)**
- Turn on 2-Step Verification: <https://myaccount.google.com/security>.
- Then open <https://myaccount.google.com/apppasswords>, name it "Outreach app," and
  copy the 16-character code it gives you.
- That code goes in `.env` as `SMTP_PASSWORD`. (Outlook/365 and SendGrid have their
  own equivalent — guide them to the right one based on Q1.)

**C. Put their secrets in place**
- Copy `.env.example` to a new file named exactly `.env`.
- Fill in `SMTP_USER` (their email), `SMTP_PASSWORD` (the app password), and
  `SENDER_NAME` (their name).

**D. Open a terminal in the project folder**
- **Windows:** open the folder in File Explorer, type `cmd` in the address bar, Enter.
- **Mac:** right-click the folder → "New Terminal at Folder."

**E. Install the add-ons (one time)**
```
pip install -r requirements.txt
```

**F. Start the app**
```
streamlit run app.py
```
- A browser tab opens automatically. That's the dashboard. To stop it later, go back
  to the terminal and press `Ctrl + C`.

That's the whole journey: install Python → app password → fill `.env` → install →
run. Everything after that is clicking around the dashboard.

---

## Appendix: quick reference card for you (the AI)

- **Never** start by writing code. Start with the interview (or Express path).
- **Always** give a recommended default; accept "I don't know."
- **One sentence** of plain explanation per file you create.
- The **five required contact fields** are non-negotiable: `first_name, last_name,
  email, title, organization_name`.
- The **safety-check order** in `paced_send` is load-bearing — don't reorder it.
- End by **sending one real test email** to the user's own inbox and confirming the
  dedupe + log.
