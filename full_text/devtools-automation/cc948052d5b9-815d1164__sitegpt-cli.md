---
name: sitegpt-cli
description: Use when an AI agent needs to manage SiteGPT through the SiteGPT CLI, including authentication, profiles, chatbots, knowledge sources, custom responses, settings, personas, instructions, conversations, messages, leads, members, billing, tokens, or troubleshooting CLI command usage.
license: MIT
metadata:
  author: sitegpt
  organization: SiteGPT
  version: "0.2.1"
---

# SiteGPT CLI

Use the SiteGPT CLI to manage SiteGPT accounts and chatbots from a terminal or agent environment. Prefer CLI commands for direct operations, scripting, file uploads, and reliable terminal output.

The installed command is `sitegpt`.

SiteGPT also publishes an agent auth discovery file at
`https://sitegpt.ai/auth.md`. Use it when an agent environment wants a
standard, machine-readable description of the anonymous onboarding registration
flow. The CLI commands below remain the preferred implementation path when a
terminal is available.

## Prerequisite

Check whether the CLI is installed before starting:

```bash
sitegpt --version
```

If `sitegpt` is missing, ask the user before installing it:

```bash
npm install -g @sitegpt/cli
```

## Agent Operating Mode

You own the outcome: a working, branded, accurate chatbot the human is glad to claim — not a list of commands run. Act like a SiteGPT implementation engineer.

- Understand the business from its website, docs, audience, and support needs.
- Resolve the canonical website URL first and reuse it everywhere (see "Resolve The Canonical Website URL First").
- Build a discovery brief and **ask it before you create or train the chatbot** — use case, industry, audience, persona, primary goal, escalation (see "Build A Discovery Brief First"). Creating the chatbot and ingesting knowledge before you ask reads as never having asked, even if you ask afterward.
- Create or update the right SiteGPT resources through the CLI; prefer `--json` for IDs and status; parallelize independent work after required IDs exist.
- Treat the website as messy: handle bare/non-canonical domains, JS-rendered pages, anti-bot blocks, and missing sitemaps without giving up (see "Robustness And Recovery").
- The value moment is a correct answer to a question the human did not script. Do not hand over a preview until you have verified that (see "The Aha Test").
- Stay visible on anything longer than a few seconds, and finish with a crisp handoff: what you built, test questions to try, and the claim/dashboard link.
- Never invent company facts, pricing, policies, or capabilities; never echo tokens; confirm before anything destructive.

If web/browser/fetch tools are available, inspect the website before creating the chatbot — the SiteGPT CLI manages SiteGPT, it does not understand websites. With no web tools, create a conservative chatbot, ingest the sitemap/website, and tell the user that deeper brand-specific customization needs website inspection.

## Quick Start — The Happy Path

For the most common request — "create / try a SiteGPT chatbot for `<url>`" with no account or token provided — do exactly this, in order. Do not improvise command names, and do not explore by trial and error.

1. Confirm the CLI: `sitegpt --version` (install only if missing).
2. **Pick the flow — ask, don't assume.** If a human is present and gave no token, your **first** question to them is: **"Do you already have a SiteGPT account?"** Not being logged in is ambiguous — the human might have no account, one account, or several. Don't guess which, and don't choose the flow for them based on anything you think you know about who they are; ask, and let them decide. Being logged out / having no saved profile is exactly why you ask, not a reason to skip to the preview (see "Choose The Right CLI Flow First").
   - **Yes** → run `sitegpt login` (a one-time browser approve) and build **in their account** (**Account Chatbot Setup**). Do **not** hand an account-holder a throwaway preview to claim later just to skip logging in.
   - **No / just trying** → the no-login preview path, steps 3–7 below.
   - No human to ask (headless) → default to the preview path.
3. Resolve the canonical website URL and inspect the site **just enough to pre-fill the brief** (the two sections below) — homepage content, brand, and whether a sitemap exists. Save deep work (logo extraction, sizing every sitemap) for after the human answers.
4. **Ask the human the discovery brief** as multiple-choice questions and **wait for the answers — before you create or train anything.** This is the human's first interaction; do not build first and ask at the end.
5. Create the preview **once**: `sitegpt onboarding start <canonical-url> --json`. It is public — no login. Capture the workspace id, chatbot id, temporary token, and onboarding URL. **Never re-run this on a retry** — reuse the ids you already got, or you will create duplicate workspaces.
6. Configure from the answers — knowledge (sitemap), persona, instructions, starters/followups, appearance/icon. Discover exact flags with `sitegpt <command> --help`.
7. Run the aha test, then share the onboarding URL and offer to claim.

**Command rule.** The **CLI is the source of truth for command syntax**; this skill is the source of truth for *workflow*. Discover commands with `sitegpt agent-guide` (workflow + command map) and exact flags with `sitegpt <command> --help` / `sitegpt <command> <subcommand> --help`. Never guess a name like `chatbot create` or `source add-website`; if a command or flag is rejected, read its `--help` instead. Errors are structured — in `--json` they carry an `error.code` and often an `error.hint`; read the hint and do exactly what it says before retrying (it usually names the command that fixes it, e.g. how to get a missing id or which auth step to run).

**Token rule.** Keep the temporary token out of command lines and logs — write it to an env file and `source` it (`export SITEGPT_API_TOKEN=…` in a file), so it is never echoed inline.

## Choose The Right CLI Flow First

Decide the flow before doing the work:

- **The human gave a token/profile, said they already use SiteGPT, or asked to
  update an existing chatbot/account** → **Account Chatbot Setup**: check auth and
  manage resources directly in that account.
- **No token/profile, and a human is present** → do not assume. Ask one quick
  multiple-choice question and branch on the answer:

  > Do you already have a SiteGPT account?
  > • **Yes — build it in my account** → I'll log you in and create it there.
  > • **No / just trying — build a free preview I can claim** → I'll build a
  >   working chatbot with no login, and you claim it afterward (an existing
  >   account can claim it too).

  - **Yes** → run `sitegpt login`, then **Account Chatbot Setup**.
  - **No / just trying** → **Agent-First Onboarding** (`sitegpt onboarding start`,
    no login, then preview and claim).
- **No token/profile and no human to ask** (autonomous/headless run) → default to
  **Agent-First Onboarding**, since it creates value before signup.

`PROFILE_NOT_CONFIGURED` (or any logged-out / no-token state) is not an error and
never a reason to stop — it only means no saved profile exists. **It does not mean
the human has no SiteGPT account**: they may have one and simply need to
`sitegpt login`. So a logged-out CLI is never a reason to skip the account
question and jump to the preview — when there is no token and a human is present,
you must ask first. Do not run `whoami` and treat its failure as "no account".

## Resolve The Canonical Website URL First

A human often gives a bare or non-canonical domain — `example.com`,
`www.example.com`, `http://example.com`, or a deep link. Normalize it once,
before inspection, before `onboarding start`, and before knowledge ingestion,
then reuse the same canonical URL everywhere so pages are not missed or
duplicated.

- If no scheme is given, try `https://` first; fall back to `http://` only if
  HTTPS fails.
- Check for a redirect to find the host the site actually serves from:

```bash
curl -sIL "https://example.com" | grep -iE '^HTTP/|^location:'
```

- **If the site redirects** (`example.com` 301s to `www.example.com`, or the
  reverse), use the final redirect target as canonical.
- **If there is no redirect and both hosts respond** — a common setup where
  `example.com` and `www.example.com` each serve the site independently — figure
  out the canonical host; do not guess. In order:
  1. Declared canonical on the homepage: `<link rel="canonical">`, `og:url`, or
     JSON-LD `url`/`@id`:
     ```bash
     curl -sL "https://example.com" | grep -iE 'rel="canonical"|og:url|"@id"|"url"'
     ```
  2. If none is declared, infer it: the host used in the sitemap's `<loc>` URLs
     and in the homepage's own internal absolute links reveals the site's
     preferred host.
  3. If still unknown, fetch both hosts and compare. If they serve the **same**
     site, either works — keep the host the human gave and use it consistently.
     If they serve **different** content (one is parked, blank, or a different
     site), use the host with the real site.
  4. State the chosen host and any assumption in your report.
  Pick one host and use it **consistently** for onboarding and every knowledge
  source, so the crawl is never split across www and non-www.
- Use that one canonical origin for the robots.txt and sitemap checks below, for
  `sitegpt onboarding start`, and for the website/sitemap knowledge sources.
- If neither scheme is reachable, or the domain redirects off to a parked /
  for-sale / unrelated page, stop and tell the human instead of building a
  chatbot for the wrong site.

## Build A Discovery Brief First

**Gather a short discovery brief — and ask it before you create the chatbot or
start ingestion, not after.** The brief drives persona, instructions, starter
prompts, lead capture, escalation, tone, and which pages matter most. Inspect the
site only enough to pre-fill the answers; creating the chatbot, ingesting
knowledge, and configuring everything else all come **after** the human replies.
Creating the bot and kicking off ingestion first — then asking at the end — reads
as "it never asked me" even though you did, and it is the most common way this
skill disappoints a human. A tailored result the human helped shape is what makes
them claim it; a generic one built without them undersells.

**You must ask, not assume.** When a human is in the loop and you can put a
question to them — any interactive session, including Claude Code, Cursor, or a
chat UI — **ask the discovery brief as multiple-choice questions and wait for the
answers before you configure the chatbot**. Silently inferring the brief and
building anyway is a failure of this skill: the human chose to be involved, and
the brief is the one place their choice matters most. Only skip the questions
when there is genuinely no human to answer (a headless, CI, or batch run) or the
human explicitly said "just build it" / "use your best guesses".

Make it effortless, not an interrogation. Inspect the website first so you can
**pre-fill the most likely answer** to every question; the human mostly taps to
accept. Selecting an option is not friction — only typing is.

- **Use your environment's question tool** (for example Claude's AskUserQuestion)
  to present the brief as multiple-choice questions with the inferred answer
  pre-selected and an "Other" option for typing. Do not just print the questions
  and answer them yourself — put them to the human and wait for a reply.
- **If you only have plain text** (no question tool), present the inferred brief
  as one compact confirm-or-edit message and wait for the reply.
- **Only if there is no human at all** (autonomous/headless run): proceed with the
  inferred brief and clearly state every assumption in your final report.

Ask about six things, ordered by impact. Each is multiple-choice with the
inferred default pre-selected; include an "Other" choice so the human can type
when the options do not fit:

1. **Primary use case** — Customer support · Sales / lead-gen · Onboarding /
   product guide · Docs / technical · Marketing guide · A mix.
2. **Industry** — SaaS · Ecommerce · Healthcare · Legal · Finance · Education ·
   Agency · Local services · Other. Drives tone and safety guardrails.
3. **Audience** — Prospects · Existing customers · Developers · Patients ·
   Students · Mixed.
4. **Primary goal** — Deflect support tickets · Book a demo · Capture leads ·
   Start a trial · Help find docs/answers.
5. **Tone** — Friendly · Formal · Technical · Playful · Enterprise ·
   Caring / cautious.
6. **Escalation and contact** — Support email · Sales email · Human handoff ·
   None found. Use a text field for the actual address, pre-filled if the site
   published one.

Optional, skippable follow-ups: bot/persona name (pre-fill `<Brand> Assistant`),
languages, priority pages to weight in knowledge, and anything the bot must not
say.

Keep it to one short pass and pre-select everything, so a human who agrees just
confirms. **Translate the brief into the persona, instructions, and settings — do
not paste the raw brief into the instruction set.** The instruction set is the
bot's runtime prompt; a `Discovery brief (set by the owner): use case = …, lead
form = off` header there is redundant with the behavior you already wrote from it,
is noise the model re-reads on every answer, and leaks operational details if a
user asks the bot about itself. Instead, put a clean human-readable summary of the
bot's purpose in the **chatbot description** (metadata, not the prompt), and
**recap the choices you made to the human in your handoff** so they can see and
adjust them. The answers are also useful signal — in an account context they can feed
analytics on which use cases and industries convert best. Then translate the
brief into configuration using the use-case presets and industry guardrails
below.

## Use-Case Presets

Map the brief's primary use case to a configuration bundle. Treat these as
strong defaults, then adjust to the specific website.

- **Support**
  - Persona: brand support specialist; friendly, concise.
  - Starters: "How do I …", "Troubleshoot …", "Pricing and plans", "Contact support".
  - Lead form: off unless the goal also includes leads.
  - Escalation/CTA: escalate to the support email; offer human handoff when stuck.
  - Instruction emphasis: accuracy, grounded answers, uncertainty handling, escalation.
- **Sales / lead-gen**
  - Persona: sales-aware advisor; helpful, confident.
  - Starters: "What does <Brand> do?", "Plans and pricing", "Book a demo", "Is it right for me?".
  - Lead form: on, with one or two qualification fields.
  - Escalation/CTA: book-a-demo or contact-sales link.
  - Instruction emphasis: qualify, capture contact, route to sales, never invent pricing.
- **Onboarding / product guide**
  - Persona: onboarding guide; encouraging, step-by-step.
  - Starters: "Getting started", "Set it up", "Key features", "Best practices".
  - Lead form: optional.
  - Escalation/CTA: link to setup docs or support.
  - Instruction emphasis: step-by-step guidance, link to docs, reduce time-to-value.
- **Docs / technical**
  - Persona: docs assistant; precise, technical.
  - Starters: "How to …", "API / reference", "Examples", "Limits and quotas".
  - Lead form: off.
  - Escalation/CTA: link to the most relevant docs.
  - Instruction emphasis: cite sources, careful unknowns, no invented behavior.
- **Marketing guide**
  - Persona: friendly product guide.
  - Starters: "What is <Brand>?", "Who is it for?", "Pricing", "How does it compare?".
  - Lead form: optional.
  - Escalation/CTA: CTA to start a trial or book a demo.
  - Instruction emphasis: clear value proposition, help visitors navigate, honest comparisons.

For a mix, lead with the primary use case and fold in the secondary one's
starters and escalation without overcomplicating the persona. Let the **primary
goal** drive lead capture: if the goal is leads, enable the lead form and
qualification even when you must ask the human for the sales email — do not wait
for the website to volunteer it.

## Industry Guardrails

Bake industry-appropriate tone and safety into the instruction set:

- **Healthcare** — caring, cautious. No medical advice or diagnosis; urge
  contacting a qualified professional; be privacy-aware.
- **Legal** — formal, cautious. No legal advice; general information only;
  suggest consulting a lawyer.
- **Finance** — precise, cautious. No financial or investment advice; no
  guarantees of returns.
- **Ecommerce** — friendly. Handle orders, returns, and shipping only from
  published policy; never invent stock, prices, or delivery dates.
- **SaaS / tech** — technical, concise. Ground answers in docs; cite; be careful
  with API behavior and limits.
- **Education** — encouraging. Keep it age-appropriate; cite sources.
- **Local services** — warm, simple. Give hours, location, and booking from the
  site; collect contact details for quotes.

When the industry is sensitive (healthcare, legal, finance), make the "do not
invent / not professional advice" rules explicit in the instructions and prefer
escalation to a human over guessing.

## Robustness And Recovery

Real websites and networks are messy. A world-class run degrades gracefully and never strands the human.

- **Idempotency.** Do not create duplicates on a re-run. Reuse the workspace and chatbot ID you already have this session; run `onboarding start` once per site per session; list existing knowledge/personas/instructions before adding to an account chatbot.
- **Transient errors.** On HTTP 429 or 5xx, back off and retry a few times before surfacing the failure. Ingestion is asynchronous — block until it settles with `sitegpt knowledge wait --chatbot <id> --json` (or pass `--wait` to an add command); it exits non-zero on timeout and reports trained/failed counts. Don't assume training finished, and don't hand-roll a poll loop.
- **Partial failures.** If some documents fail, report which and the `knowledge documents resync` command; do not claim the bot is fully trained.
- **Plan limits.** Sync/scan frequencies and source counts may be downgraded with an API warning — surface these instead of silently dropping them.
- **Hard websites.** JS-rendered (SPA) pages, anti-bot/403 blocks, and missing sitemaps are common — the inspection step shows how to detect and work around each. Always still produce a working bot, and note where appearance or knowledge was set conservatively.
- **Subdomains and walled content.** Knowledge often lives on `docs.`, `help.`, `app.`, or `blog.` subdomains — include the ones that match the use case. Login-walled docs cannot be crawled; suggest a connector (Notion, Drive, GitHub, Confluence) instead.
- **Stay visible.** Anything longer than a few seconds (crawl, indexing) gets a short progress note. Never go silent through a multi-minute build.
- **Degrade by capability.** No question tool → one confirm message for the brief. No web tools → conservative bot + sitemap ingest. No human → infer and proceed, stating assumptions.
- **Freshness needs a re-syncable source.** Recurring auto-sync/scan attaches to **WEBSITE or SITEMAP** sources, not to individual `links add` (URLS_LIST) docs. If the knowledge must stay current (pricing, features), ingest the main source as a sitemap/website so it can auto-sync; for facts that must never drift (pricing, contact), also seed a custom response.
- **Expected ingestion failures.** Some JS-rendered pages fail to ingest. If a failed page is redundant — its content already covered by another source you ingested — remove it and move on; do not treat it as a blocker or retry it endlessly.
- **No busywork, and trust your output.** Command output is reliable: never run empty "sync"/"checkpoint"/"noop" commands to flush it. Before retrying a command, check status (`status` / `documents stats`) — do not re-run something that already succeeded just because a count or message looked off, and never re-run `onboarding start` (it creates a duplicate).

## First Moves

For agent-first onboarding, start with the website URL, not an account login.
It is fine to check `sitegpt --version` and inspect the website first, but do
not run `sitegpt whoami` as a required step. If a human is present, **ask the
discovery brief and wait for the answers before this step** (see "Build A
Discovery Brief First") — do not create the workspace and build first:

```bash
sitegpt onboarding start https://example.com --json
```

This does not require login. It returns a temporary one-chatbot token, chatbot ID, and onboarding URL. Use the temporary token to finish setup, then check readiness:

```bash
SITEGPT_API_TOKEN="<temporary-token>" sitegpt onboarding status <workspace-id> --json
```

After capturing the temporary token, keep using it through `SITEGPT_API_TOKEN`
instead of logging in. Do not echo the token, do not include the full token in
final output, and do not ask the human to create a token unless the onboarding
start command fails.

The status response includes `data.setupChecklist`; fix pending, warning, or unknown checklist items when possible before sharing the onboarding URL. Give the human the onboarding URL only after you have configured and tested the chatbot. Do not ask the human to sign in before a chatbot preview exists unless the user explicitly wants to manage an existing SiteGPT account.

After the human claims the chatbot, the same temporary token is transferred to the claimed SiteGPT user. It stays scoped only to that chatbot and keeps its original expiry. Continue using it for final checks or small post-claim edits unless the user asks you to stop.

After the human reviews the preview, ask whether they want to claim it, then run
the claim — the full flow (email/plan/interval, checkout, and the
existing-subscriber case) is in **Playbook: Agent-First Onboarding Chatbot**.

For existing accounts or direct account management, use the **Account Chatbot
Setup** playbook (it starts with `whoami` / `login` / `profiles`). Use `--json`
whenever you need IDs, pagination cursors, full nested data, or reliable parsing,
and discover exact syntax with `sitegpt <command> --help`.

### Avoid Cancelled Setup Work

Some agent runtimes cancel parallel tool calls when one command returns a
non-zero exit code. Do not put optional auth checks in the same shell command or
parallel batch as required website inspection.

Good:

```bash
sitegpt --version
sitegpt whoami --json || true
```

Then independently inspect the website and continue with onboarding if auth is
not configured.

Bad:

```bash
sitegpt whoami --json && curl -sL https://example.com -o /tmp/page.html
```

For agent-first onboarding, missing auth is expected. Website inspection and
`sitegpt onboarding start` should still continue.

## Playbook: Agent-First Onboarding Chatbot

Use this workflow when the user asks something like "Try SiteGPT for https://example.com" and they have not provided an existing SiteGPT token/profile. The goal is to create a working preview before signup.

If the user already has a SiteGPT token/profile and wants the chatbot created directly inside their account, use the **Account Chatbot Setup** playbook below instead.

### Configuration Mindset

Configure the temporary chatbot as a polished first preview. The human has not
created a SiteGPT account yet, so the preview must demonstrate value before
signup:

- **Knowledge**: add the best source first, usually sitemap. Wait for training
  when practical and use `onboarding status` to inspect `setupChecklist`.
- **Brand settings**: upload a real brand icon/chat bubble and apply extracted
  colors before sharing the preview. The user should immediately recognize the
  website's brand in the preview page and launcher.
- **Persona**: create one clear persona matching the chatbot purpose. Avoid
  overcomplicated persona variants; the user needs one strong default.
- **Instructions**: create one active instruction set with grounding,
  uncertainty, escalation/contact behavior, and purpose-specific rules.
- **Starters/followups**: add broad visitor questions that make the preview easy
  to test without the user thinking of prompts.
- **Lead/support settings**: enable only when the website or user provides the
  needed contact/sales details.
- **Handoff**: final output should focus on the onboarding URL, setup checklist
  status, what was configured, and what the human can claim.

### 1. Inspect The Website

Use raw HTML (`curl` + search) for structured signals like colors, icons, manifests, and sitemap links. Use WebFetch/browser tools for prose-heavy understanding like value proposition, navigation, audience, and tone.

Gather:

- Brand or product name.
- Homepage title, meta description, and core value proposition.
- Main navigation labels and important URLs.
- Docs, pricing, contact, support, FAQ, blog, terms, privacy, and login URLs when visible.
- Support email, sales email, phone number, or contact form URL if published.
- Logo, favicon, or simple brand mark that can be saved as an image file.
- Brand colors from the required raw HTML extraction procedure below.
- Open Graph/Twitter images, app icons, and product screenshots that can inform the chatbot's visual setup.
- Sitemap URLs from `robots.txt`, `<link rel="sitemap">`, `/sitemap.xml`, `/sitemap_index.xml`, or obvious CMS sitemap paths.
- Tone: formal, friendly, technical, playful, enterprise, healthcare/legal cautious, etc.

Do not invent company facts, pricing, policies, emails, or guarantees. If something is not visible, configure the chatbot to say it does not know and offer escalation/contact.

### 1A. Extract Structural Signals From Raw HTML (Required)

Summarizing tools are useful for understanding prose, but they often strip or blur exact metadata such as hex colors, icon links, manifests, and sitemap links. Do not trust qualitative output like "appears to be blue-based" for appearance setup. Always inspect raw HTML before choosing brand colors or icons.

Use a raw-HTML pass:

```bash
SITE_URL="https://example.com"
# Use a real browser User-Agent — default curl is blocked by many sites and CDNs.
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
curl -sL -A "$UA" "$SITE_URL" -o /tmp/sitegpt-page.html

# Detect a JS-rendered (SPA) shell: tiny body + a root mount node and little real text.
# If so, raw HTML has no content/colors/links — render with a browser/WebFetch tool,
# or rely on the sitemap for URLs.
wc -c /tmp/sitegpt-page.html
grep -ciE 'id="root"|id="__next"|__NEXT_DATA__|<app-root|ng-version' /tmp/sitegpt-page.html

# Brand color: raw hex frequency is dominated by #000/#fff/greys — ignore those and
# prefer declared signals (theme-color, CSS brand variables, CTA/button colors).
grep -iE 'theme-color|--primary|--brand|--accent|--color-primary|--color-brand' /tmp/sitegpt-page.html | head
grep -oE '#[0-9a-fA-F]{6}\b' /tmp/sitegpt-page.html \
  | grep -viE '#(000000|ffffff|fafafa|f5f5f5|eeeeee|dddddd|cccccc|bbbbbb|aaaaaa|999999|333333|222222|111111)' \
  | sort | uniq -c | sort -rn | head -20

# Declared theme color, icons, manifest, social image, and sitemap hints.
grep -iE 'theme-color|apple-touch-icon|rel="icon|manifest|og:image|twitter:image|sitemap' /tmp/sitegpt-page.html
```

If the response is a bot challenge or 403 — Cloudflare "checking your browser", "Access denied", a captcha page, or a near-empty body with a JS redirect — treat raw HTML as unavailable: use a browser/render tool for inspection, fall back to the sitemap for the URL set, and still proceed with onboarding. Tell the user when a site blocks automated inspection so they know appearance was set conservatively.

Discover the sitemap robustly. Prefer the `Sitemap:` directive in robots.txt (the site's own declared sitemap), and handle gzipped and index sitemaps:

```bash
curl -sL -A "$UA" "$SITE_URL/robots.txt" | grep -i '^sitemap:'
for u in sitemap.xml sitemap_index.xml sitemap.xml.gz sitemap-index.xml; do
  curl -sIL -A "$UA" "$SITE_URL/$u" | grep -iE '^HTTP/|content-type'
done
```

A `<sitemapindex>` lists child sitemaps — follow them to reach the actual page URLs. Pass a working sitemap URL to `sitegpt knowledge sitemap add`; if it does not expand a nested index, add the child sitemaps or fall back to the website crawl.

If a manifest is linked, fetch it and inspect colors/icons:

```bash
curl -sL "$SITE_URL/manifest.json"
```

Download the chosen icon or image to a local file and confirm format/dimensions before upload:

```bash
curl -sL "https://example.com/logo-icon.png" -o /tmp/sitegpt-brand-icon.png
file /tmp/sitegpt-brand-icon.png
```

Prefer assets in this order:

1. `apple-touch-icon` or large app icon.
2. Manifest icon with square dimensions.
3. Clean logo mark or favicon PNG/SVG converted to PNG.
4. Open Graph/Twitter image only if it contains a clear brand mark and can be cropped.

Only fall back to visual guesses or WebFetch's qualitative color description when raw HTML, CSS-visible variables, manifest, theme-color, and icon links provide no usable signal. If you pick a generic default such as `#2563EB`, treat that as a warning and re-check raw HTML before proceeding.

### 1B. Decide Brand Assets

Create an asset plan before creating the chatbot so the finished bot feels branded immediately:

- Primary color: choose the strongest brand/action color, usually from `theme-color`, primary buttons, CSS variables such as `--primary`, or the logo.
- Text-on-brand color: choose `#ffffff` for dark/saturated colors and `#111827` or similar for light colors.
- Link color: usually the primary brand color unless the site uses a separate link color.
- Icon background color: usually the primary brand color.
- Icon shape/position/size: use normal product defaults unless the site clearly uses rounded/square visual language.
- Bot/chat-bubble image: prefer favicon, app icon, simple logo mark, or a clean cropped logo. Avoid wide wordmarks as tiny icons.
- Watermark/person/agent images: only set when you have high-quality assets and the user expects them.

If image tooling is available, crop/convert the best logo or favicon into a square PNG with transparent or clean background before upload. If only a remote image URL is available, download it to a local file first, then upload the file. Do not pass remote URLs to `sitegpt icons upload`.

### 2. Ask The Discovery Brief, Then Draft The Blueprint

You have now inspected enough to pre-fill the brief, so **ask the human the
discovery brief and wait for the answers before you start the workspace or
configure anything** (see "Build A Discovery Brief First"). Do not run
`onboarding start` and build the whole bot first, then ask at the end — that
reads as never having asked. The only exception is a headless run with no human.

Then, driven by the confirmed brief (apply the matching use-case preset and
industry guardrails), decide before mutating SiteGPT:

- Primary use case and the rest of the brief: industry, audience, persona/voice,
  primary goal, and escalation. Secondary use cases can layer on starters/CTAs.
- Chatbot title that fits the brief's role — `<Brand> Assistant`, `<Brand> Guide`, or `<Brand> Support`; do not default to "Support" for a sales/marketing/docs bot.
- Chatbot description, one sentence about what it helps with.
- Best knowledge source: sitemap first, website crawl second, selected links third.
- Persona: the bot's role and voice.
- Instructions: grounding, uncertainty, escalation, privacy, lead capture, and forbidden behavior.
- Starter prompts: 3-5 first-click questions a visitor would naturally ask.
- Followup prompts: 3-5 useful next actions, including contact/support when appropriate.
- Settings: chat mode, support email, lead form/human support if appropriate, and any appearance/icon updates.
- Brand assets: primary color, readable brand text color, link color, icon background, and local icon file paths.

### 3. Start The Temporary Workspace

Start onboarding:

```bash
sitegpt onboarding start https://example.com --agent-name "<agent-name>" --json
```

Capture:

- `data.workspace.id` as `<workspace-id>`.
- `data.workspace.chatbotId` as `<chatbot-id>`.
- `data.apiToken` as the temporary setup token.
- `data.onboardingUrl` for the human. This single page lets the human test
  the chatbot and claim it.

Run setup commands with the temporary token:

```bash
SITEGPT_API_TOKEN="<temporary-token>" sitegpt chatbots get <chatbot-id> --json
```

Check the workspace readiness after major setup steps:

```bash
SITEGPT_API_TOKEN="<temporary-token>" sitegpt onboarding status <workspace-id> --json
```

Inspect `data.setupChecklist`. The checklist reports whether knowledge,
persona, instructions, conversation starters, follow-up prompts, and brand
styling are done, pending, unknown, or need review. Fix pending or warning
items before sharing the onboarding URL unless the user explicitly asks for a
rough draft.

After setup, test the chatbot with a few realistic visitor messages. If it answers from the added knowledge and the setup checklist is acceptable, tell the user the chatbot is ready and share `data.onboardingUrl` for manual testing. Ask whether they want to claim it now.

If the user wants to claim it, **first ask whether they are claiming into an existing SiteGPT account or as a new customer — do not assume new and jump to plan/interval.**

- **Existing account** (e.g. they already use SiteGPT) → they claim from the onboarding page **while signed in**; SiteGPT attaches the chatbot directly to their account with **no checkout and no plan/interval**. The CLI's temporary token cannot prove ownership of an existing account, so don't ask for plan/interval — just point them to the page.
- **New customer** → ask for email, plan, and interval, then start the claim:

```bash
SITEGPT_API_TOKEN="<temporary-token>" sitegpt onboarding claim <workspace-id> --email user@example.com --plan GROWTH --interval MONTH --json
```

If `data.checkoutUrl` is present, return it and explain that checkout happens on SiteGPT's pricing page. Once the free trial starts, SiteGPT transfers the temporary chatbot into that email's dashboard account. If checkout is already pending, reuse the returned checkout URL and do not ask for a different email or plan. If the response says the email already has an active subscription, ask the human to open the onboarding URL while signed in and claim from the page.

If the setup is wrong or the human does not want the workspace, delete it:

```bash
SITEGPT_API_TOKEN="<temporary-token>" sitegpt onboarding delete <workspace-id> --yes
```

This deletes the temporary chatbot and onboarding workspace. The workspace is no
longer available after deletion.

## Playbook: Account Chatbot Setup

Use this workflow when the user gives you a SiteGPT token/profile or asks to manage an existing SiteGPT account. This also works for a new SiteGPT customer who already wants to authenticate first and create their first chatbot directly in their account.

### Configuration Mindset

Configure inside a real SiteGPT account. Be more careful with existing state
than in onboarding because the account may already have chatbots, knowledge,
settings, tokens, or team workflows:

- **Knowledge**: list existing documents when updating an existing chatbot. Add
  new sitemap/links/files without deleting or resyncing existing sources unless
  the user asked.
- **Brand settings**: read current appearance before changing it. Preserve
  existing brand choices unless the user wants a full refresh or the chatbot is
  newly created.
- **Persona**: list current personas before replacing behavior on an existing
  chatbot. For a new chatbot, create one strong default and activate it.
- **Instructions**: list current instructions before changing active behavior.
  For a new chatbot, create one active instruction set.
- **Starters/followups**: add or update prompts to match the website purpose,
  but do not remove existing prompts without approval.
- **Lead/support settings**: respect existing routing, notification emails, and
  form requirements. Ask before changing lead capture or human handoff on an
  established chatbot.
- **Handoff**: final output should focus on the dashboard link, install snippet
  when useful, what changed, and any warnings from plan limits or ingestion.

### 1. Check Authentication

```bash
sitegpt whoami --json
```

If not authenticated, run:

```bash
sitegpt login
```

Then inspect profiles if the user mentions a specific account or environment:

```bash
sitegpt profiles list
sitegpt profiles use <profile>
```

### 2. Inspect The Website, Then Ask The Discovery Brief

Use the same inspection, raw HTML extraction, brand asset, and blueprint steps from the **Agent-First Onboarding Chatbot** playbook — but only enough to pre-fill the brief. Then **ask the human the discovery brief (see "Build A Discovery Brief First") and wait for the answers before you create the chatbot or add knowledge.** Do not run `chatbots create` and start ingestion first and ask afterward — even in the owner's own account, that reads as never having asked. The only exception is a headless run with no human to answer.

### 3. Create The Chatbot

Only after the discovery brief is answered (or there is genuinely no human to ask) create the chatbot — let the answers shape its title and description. Always request JSON so you can capture the ID:

```bash
sitegpt chatbots create "<Brand> Assistant" --description "<short description that fits the brief's role>" --json
```

Extract `chatbot.id` from the JSON response and use it for all following commands.

### 4. Add Knowledge

Prefer sitemap ingestion when a sitemap is available:

```bash
sitegpt knowledge sitemap add --chatbot <chatbot-id> https://example.com/sitemap.xml --only-main-content true --json
```

If no sitemap is available, crawl the website:

```bash
sitegpt knowledge website add --chatbot <chatbot-id> https://example.com --depth 3 --max-links 100 --only-main-content true --json
```

If only a few relevant pages are discovered, add explicit links:

```bash
sitegpt knowledge links add --chatbot <chatbot-id> https://example.com/pricing https://example.com/docs --only-main-content true --json
```

Plan-gated sync/scan frequencies may be downgraded by the API. Surface warnings to the user.

After queuing, **wait for training before you test or hand off** — add `--wait` to the ingest command, or run `sitegpt knowledge wait --chatbot <chatbot-id> --json` (it blocks until settled, exits non-zero on timeout, and reports trained/failed counts). Don't hand-roll a poll loop.

### 5. Configure Persona And Instructions

Create temporary markdown files for persona and instructions, then add and activate them:

```bash
sitegpt personas add --chatbot <chatbot-id> --title "<Brand> assistant (role from the brief)" --file ./persona.md --json
sitegpt personas use --chatbot <chatbot-id> <persona-id>
sitegpt instructions add --chatbot <chatbot-id> --file ./instructions.md --temperature 0.3 --json
sitegpt instructions use --chatbot <chatbot-id> <instruction-id>
```

Persona should be short and identity-focused. Instructions should be operational and safety-focused, and the **role must match the brief's use case** — guide, sales advisor, docs assistant, or support specialist (see Use-Case Presets) — not default to "support". A strong default instruction set:

- Answer as the brand's assistant in the role the brief selected (guide / sales / docs / support), in the chosen tone.
- Use only the chatbot's knowledge and the visible website facts gathered during setup.
- Do not invent pricing, policies, legal terms, medical claims, availability, or integrations.
- If unsure, say what is known and point to the right page or contact.
- Ask concise clarifying questions when the user's request is ambiguous.
- Keep answers practical and skimmable.
- Drive the brief's primary goal (e.g. start a trial, book a demo, find docs) with one clear, non-pushy CTA; escalate or collect contact details when the user needs human help.

### 6. Add Starters And Followups

Create prompts that match the site's actual product and common visitor intent:

```bash
sitegpt starters add --chatbot <chatbot-id> --title "What does <Brand> do?" --message "Explain what <Brand> does and who it is for." --json
sitegpt starters add --chatbot <chatbot-id> --title "Pricing" --message "Tell me about pricing, plans, and what is included." --json
sitegpt starters add --chatbot <chatbot-id> --title "Getting started" --message "How do I get started with <Brand>?" --json
sitegpt followups add --chatbot <chatbot-id> --title "Contact support" --message "How can I contact support or sales?" --json
sitegpt followups add --chatbot <chatbot-id> --title "Show docs" --message "Point me to the most relevant documentation." --json
```

Use link-type followups when a high-confidence URL exists:

```bash
sitegpt followups add --chatbot <chatbot-id> --title "Open docs" --link https://example.com/docs --type LINK --json
```

### 7. Apply Settings And Icons

Use precise section commands where possible:

```bash
sitegpt settings chat-mode set --chatbot <chatbot-id> AI
sitegpt settings general update --chatbot <chatbot-id> --support-email support@example.com
sitegpt settings appearance update --chatbot <chatbot-id> --brand-color "#0F766E" --brand-text-color "#FFFFFF" --icon-background-color "#0F766E" --link-color "#0F766E" --icon-shape CIRCLE --icon-position RIGHT
sitegpt settings lead-form update --chatbot <chatbot-id> --enabled true --collect-name true
```

Only set support email or lead/human-support settings when the site or user provides the right details. Read section help before using unfamiliar flags:

```bash
sitegpt settings general --help
sitegpt settings appearance --help
sitegpt settings lead-form --help
sitegpt settings human-support --help
```

If you have saved a logo/favicon/bot image locally, upload it:

```bash
sitegpt icons upload --chatbot <chatbot-id> bot ./brand-icon.png
sitegpt icons upload --chatbot <chatbot-id> chat-bubble ./brand-icon.png
```

Use clean raster image files. Do not hotlink remote image URLs directly to icon commands. If icon upload fails because the asset is too large or the format is unsupported, convert it to a small PNG and retry.

### 8. Parallelize Safely

After the chatbot ID is known, independent tasks can run in parallel:

- Knowledge ingestion.
- Persona creation.
- Instruction creation.
- Starter creation.
- Followup creation.
- Icon upload.
- Appearance settings.
- Independent settings section updates.

Do not parallelize tasks that depend on returned IDs, such as `personas use` before `personas add` returns, or `instructions use` before `instructions add` returns. Avoid running multiple updates against the same settings section at the same time if they might overwrite each other.

### 9. Verify The Setup

Check the final state:

```bash
sitegpt chatbots get <chatbot-id> --json
sitegpt knowledge documents list --chatbot <chatbot-id> --json
sitegpt knowledge documents stats --chatbot <chatbot-id> --json
sitegpt personas list --chatbot <chatbot-id> --json
sitegpt instructions list --chatbot <chatbot-id> --json
sitegpt starters list --chatbot <chatbot-id> --json
sitegpt followups list --chatbot <chatbot-id> --json
sitegpt dashboard --chatbot <chatbot-id>
```

If documents are still pending or failed, do not claim the chatbot is fully trained. Tell the user ingestion is queued or report the failed documents and next retry/resync command.

If conversation testing is useful, ask a few site-specific questions:

```bash
sitegpt messages send --chatbot <chatbot-id> "What does this company do?" --json
sitegpt messages send --chatbot <chatbot-id> "How much does it cost?" --json
sitegpt messages send --chatbot <chatbot-id> "How can I contact support?" --json
```

In the final response, summarize:

- Chatbot name and ID.
- Dashboard link.
- Onboarding link when this was an agent-first onboarding workspace.
- Knowledge source used and ingestion status.
- Persona/instructions created.
- Starters/followups added.
- Settings/icons applied.
- Any warnings, missing website facts, or follow-up recommendations.

## Website Setup Quality Bar

A good end-to-end setup should feel specific to the website, not generic:

- Use the brand's actual name and product language.
- Apply discovered brand colors and a real brand icon whenever reliable assets are available.
- If the brand color or bot icon ends up generic, such as default blue `#2563EB` or no uploaded logo, treat the setup as incomplete and rerun raw HTML extraction.
- Make the widget feel visibly related to the source website on first load.
- Prefer sitemap ingestion over broad crawling when possible.
- Include docs/pricing/contact/support pages when they exist.
- Make starters reflect the product's real buyer/user questions.
- Make followups useful next actions, not filler.
- Keep instructions grounded and explicit about uncertainty.
- Avoid claiming the bot can do tasks SiteGPT cannot perform.
- Verify ingestion and configuration before telling the user it is done.

## The Aha Test — Verify Before Handoff

The moment that earns the claim is a correct answer to a question the human did not script. Prove it before sharing the preview:

1. Generate 3–5 realistic questions from the brief and the site — a buyer question (pricing/plans), a real support how-to, a fit question ("does it do X?"), and the primary-goal action (e.g. "book a demo").
2. Ask them with `sitegpt messages send` and read the answers — the bot's reply text is at `data.message.answer.text` in `--json` (`data.message.answer` is an object), or just read the command's plain-text output, which prints the answer directly.
3. Judge honestly: are they correct, grounded in the site, and specific? A hedge, a generic answer, or a wrong fact is a failure, not a pass.
4. If the bot misses, the knowledge is incomplete — add the missing page(s) (pricing, docs, FAQ, contact), wait for ingestion with `sitegpt knowledge wait --chatbot <id>` (or `--wait` on the add), and re-test before handoff.
5. For answers that must never be wrong — pricing, contact, refund/returns, hours — seed an exact custom response:

```bash
sitegpt knowledge custom-responses add --chatbot <chatbot-id> --question "What are your prices?" --answer "<exact, from the site>"
```

Only share the onboarding/preview URL once the aha test passes, and include 2–3 of the questions you verified in the handoff so the human reproduces the value in one click.

## Agent-First Onboarding Commands

The flow (`start` → `status` → `claim`/`delete`) is covered step-by-step in
**Playbook: Agent-First Onboarding Chatbot**. Quick facts: `onboarding start` is
public (no login) and returns the temporary token every other onboarding command
needs; plans are `STARTER`/`GROWTH`/`SCALE`, intervals `MONTH`/`YEAR`; `delete`
revokes the token and removes the unclaimed workspace; `status --json` returns
`data.setupChecklist` as the progress signal before sharing the onboarding URL.

## Command Reference — Discover It Live

This skill is the source of truth for *workflow and judgment*. The **CLI is the
source of truth for command syntax** — never reproduce it here or guess it.
Discover it live:

- `sitegpt agent-guide` — the end-to-end workflow and the full command-group map.
- `sitegpt --help` — all command groups.
- `sitegpt <command> --help`, and `sitegpt <command> <subcommand> --help` — exact
  flags and arguments for anything (e.g. `sitegpt knowledge sitemap --help`,
  `sitegpt settings appearance --help`, `sitegpt onboarding claim --help`,
  `sitegpt tokens create --help`).

Command groups (what exists — run `--help` for flags):

- **Auth & profiles:** `login`, `logout`, `whoami`, `profiles`, `tokens`
- **Onboarding (no account):** `onboarding` (`start`, `status`, `claim`, `delete`)
- **Chatbots & appearance:** `chatbots`, `dashboard`, `installation`, `icons`, `settings`
- **Behaviour:** `personas`, `instructions`, `starters`, `followups`
- **Knowledge:** `knowledge` (`documents`, `links`, `website`, `sitemap`, `youtube`, `text`, `files`, `sources`, `custom-responses`)
- **Support ops:** `conversations`, `messages`, `tags`, `leads`, `members`
- **Account:** `account`, `usage`, `limits`, `billing`
- **Agents:** `mcp`, `agent-guide`

**Ownership and team membership:** `sitegpt chatbots transfer` reassigns a chatbot's ownership to another user in the same brand — provisioning the recipient if they have no account yet, and removing the previous owner unless you pass `--keep-source-as <role>`. `sitegpt members add` adds a member directly (no invite email; the account is provisioned if needed), while `sitegpt members invite` emails a magic-link invitation. Discover flags with `--help`.

Always pass `--json` when you need IDs, status, or parseable output. If a command
or flag is rejected, read its `--help` — do not guess an alternative name.

**Parse `--json` from stdout only — never merge stderr.** The CLI puts machine
output (the JSON) on **stdout** and warnings/progress/diagnostics on **stderr**.
If you pipe with `2>&1`, a stderr line (e.g. a plan-downgrade warning) lands in
your JSON and breaks the parse. Read stdout alone (e.g. `… --json 2>/dev/null | …`
or capture stdout separately), and read `error.code` / `error.hint` on failures.


## Safety Rules

- Use `--json` for machine-readable work.
- List before mutating when IDs are unknown.
- Read current settings before updating settings.
- Destructive commands require the `--yes` flag; never pass it unless the human asked to delete. **`--yes` is only the machine guard — before any irreversible delete (a whole chatbot, knowledge sources, leads, conversations), state plainly what will be permanently removed and get an explicit "yes" from the human first, even if they already asked to delete.** Deleting a chatbot wipes its knowledge, conversations, and settings and cannot be undone — confirm the specific target by name/id before running it. For bulk/selector deletes (`knowledge documents delete`, `leads bulk`, `conversations bulk`), run `--dry-run` first, show the human the blast radius, get the go-ahead, then re-run with `--yes`.
- Do not print full tokens or secrets in final answers.
- Prefer narrow scopes for specialized agents; use `--full-access` only when broad account management is needed.
- If a command fails, run the nearest `--help` level and retry with the documented syntax.

## Troubleshooting

`TOKEN_SCOPE_NOT_VALID` means the scope name is not accepted. Check `sitegpt tokens create --help`.

`TOKEN_SCOPE_NOT_ALLOWED` means the current token lacks a required scope. Log in with a broader token or ask the user to approve a token with the missing scope.

`UNKNOWN_COMMAND` usually means the command is at a different level. For example, Custom Responses live under:

```bash
sitegpt knowledge custom-responses ...
```

For local development only, include the API base during login:

```bash
sitegpt login --profile local --api-base <local-api-base-url>
```

After that, `--api-base` is stored in the profile and does not need to be repeated.
