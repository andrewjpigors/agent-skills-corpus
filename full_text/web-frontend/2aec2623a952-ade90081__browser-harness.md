---
name: browser-harness
description: Drive a real Chrome browser via the DevStation harness — search the open web, read pages, fill forms, and hand control back to the user for logins (X/Twitter, LinkedIn, OAuth, CAPTCHAs)
version: 1.0.0
metadata:
  myai:
    tags: [web, browser, automation, social-media]
    requires_toolsets: [browser_harness]
---

# Browser Harness

Use this skill when the user asks you to do anything that requires actually
loading a webpage as a logged-in human would — searching X for posts,
reading a LinkedIn profile, filling a form behind a sign-in wall, scraping
a page that blocks fetch-style clients. The harness drives a real Chrome
session inside DevStation that the user can take over for any step that
needs human auth.

## When this skill applies

- "Search X / Twitter for …" → browser, with a takeover if not signed in
- "Find this person on LinkedIn" → browser, takeover for first run
- "Go to <site> and tell me …" / "Submit this form …" → browser
- Open-web research where a `fetch` would be blocked or paywalled

## When this skill does NOT apply

- Static-content URLs you can `curl` / fetch (news headlines, RSS, raw JSON
  APIs). Use a lighter tool first.
- The user wants you to *automate* a login. **Never enter credentials.**
  Always hand off to the user via `browser_request_user_takeover`.

## Core workflow

Every browser task follows the same five-step rhythm:

1. **status** — `browser_status` to confirm the harness is connected and
   report the starting URL.
2. **navigate** — `browser_navigate(url=…)` to the entry point.
3. **snapshot** — read the returned snapshot: a numbered list of
   interactive elements (`ref`, `tag`, `role`, `name`) plus visible page
   text. **Never click a `ref` that didn't come from a recent snapshot** —
   refs are regenerated on each call.
4. **act** — `browser_click(ref=…)` or `browser_type(ref=…, text=…,
   submit=true)` using refs from the latest snapshot. Use
   `browser_wait_for_text` after async actions if the result loads after
   the click returns.
5. **verify** — re-snapshot (or use `browser_screenshot` only when the
   user explicitly asks for visual evidence) and confirm the page shows
   what you expected before reporting to the user.

If the agent ever feels lost ("which ref was the search box again?"), the
right move is always **snapshot again**, not guess.

## Auth-handoff protocol (the rule that overrides everything else)

If at any point you see:
- A login form, a sign-in button on a logged-out shell, or a
  "Continue with Google / Apple / …" screen
- A CAPTCHA or "verify you're human"
- A two-factor prompt
- An OAuth consent screen
- A bot-detection wall

**STOP. Do not type credentials. Do not click "Sign in with Google".**
Call `browser_request_user_takeover` with a one-sentence `reason` and the
`target_url` the user should expect to land on. The tool blocks until the
user finishes and clicks "Done" in the workspace modal. When it returns,
call `browser_snapshot` to verify the logged-in state (e.g. a logged-in
header showed up), then continue the task.

After a takeover, **never** ask the user to "do it again" — the Chrome
profile is persistent, so the next time they ask you to use that site you
should already be signed in. If you are not signed in on a follow-up task,
call takeover again (something may have expired) but acknowledge that to
the user.

## Worked example 1 — Search X for a topic

User: *"Search X for recent posts about Claude Code."*

```
browser_status()
  → connected, url=about:blank

browser_navigate(url="https://x.com/search?q=Claude%20Code&f=live")
  → snapshot shows a "Log in" button + sign-up wall, no results visible

browser_request_user_takeover(
  reason="X requires login to show search results",
  target_url="https://x.com/search?q=Claude%20Code&f=live"
)
  → blocks; user logs in in the modal, clicks Done

browser_snapshot()
  → snapshot now shows the timeline; capture top 5 post texts from snap.text

# Report to user — quote 5 posts with timestamps.
```

## Worked example 2 — Read a LinkedIn profile

User: *"Find Daisy Klein on LinkedIn and tell me her current role."*

```
browser_navigate(url="https://www.linkedin.com/search/results/people/?keywords=Daisy%20Klein")
  → snapshot shows a sign-in wall

browser_request_user_takeover(reason="LinkedIn requires login to search profiles")
  → user signs in, Done

browser_snapshot()
  → snapshot shows search results; identify the right profile by name+context

browser_click(ref=<the profile result>)
  → snapshot shows the profile page; read the "Experience" section from snap.text

# Report current role + company.
```

## Session etiquette

- **Don't navigate during a takeover.** The user is driving — leave the
  page alone until the takeover tool returns.
- **Don't close tabs you didn't open.** Chrome may have multiple tabs the
  user opened manually; stick to the active one.
- **Don't accept consent / cookie banners on the user's behalf for things
  with legal weight** (e.g. T&C updates). Surface those via takeover.
- **Don't post or send.** If the user asks you to draft a post but not
  submit, draft it via `browser_type` *without* `submit=true`, then ask
  for confirmation before submitting.

## Failure modes

- `browser_status` errors with "not connected": the connector is off or
  the lease expired. Tell the user to re-enable the Browser connector in
  the workspace; do not try to recover silently.
- `browser_click` says "ref not found": the page changed (DOM mutation or
  navigation). Call `browser_snapshot` and retry with the fresh ref.
- A snapshot returns very little text or no interactive elements: the
  page is probably still loading or showing a bot wall. Try
  `browser_wait_for_text` with a phrase you expect; if that times out,
  escalate via takeover.
- Repeated failures on the same step: stop, summarize what you tried for
  the user, and ask how to proceed. Do not loop.

## Output to the user

When you finish (or get stuck), summarize:
- What page(s) you visited
- What you found (quote text directly from the snapshot when relevant)
- Whether a takeover was needed and what the user did
- Anything you couldn't complete and why

Keep it tight — the user can scroll back through your tool calls if they
want the play-by-play.
