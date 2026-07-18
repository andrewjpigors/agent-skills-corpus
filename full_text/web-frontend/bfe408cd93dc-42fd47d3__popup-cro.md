---
name: popup-cro
preamble-tier: 4
version: 1.0.0
description: |
  Optimize popups, modals, overlays, slide-ins, and banners for conversion without annoying
  users. Visits the live page in a real browser, triggers popups via scroll, exit-intent,
  time delay, and click, then audits content, form, CTA, mobile rendering, accessibility,
  and compliance. Fixes issues in source code with atomic commits and before/after
  verification. Use when asked to "optimize popup", "popup CRO", "exit intent not working",
  "modal conversions", "lead capture popup", "email popup", "popup audit", "overlay optimization",
  "scroll trigger popup", "sticky bar", or "notification bar". Proactively suggest when
  reviewing a page that has popups or modals. For forms outside of popups, see form-cro.
  For general page conversion optimization, see page-cro.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - WebSearch
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

## Preamble (run first)

```bash
_UPD=$(~/.claude/skills/vstack/bin/vstack-update-check 2>/dev/null || .claude/skills/vstack/bin/vstack-update-check 2>/dev/null || true)
[ -n "$_UPD" ] && echo "$_UPD" || true
mkdir -p ~/.vstack/sessions
touch ~/.vstack/sessions/"$PPID"
_SESSIONS=$(find ~/.vstack/sessions -mmin -120 -type f 2>/dev/null | wc -l | tr -d ' ')
find ~/.vstack/sessions -mmin +120 -type f -delete 2>/dev/null || true
_CONTRIB=$(~/.claude/skills/vstack/bin/vstack-config get vstack_contributor 2>/dev/null || true)
_PROACTIVE=$(~/.claude/skills/vstack/bin/vstack-config get proactive 2>/dev/null || echo "true")
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
echo "PROACTIVE: $_PROACTIVE"
source <(~/.claude/skills/vstack/bin/vstack-repo-mode 2>/dev/null) || true
REPO_MODE=${REPO_MODE:-unknown}
echo "REPO_MODE: $REPO_MODE"
```

If `PROACTIVE` is `"false"`, do not proactively suggest vstack skills — only invoke
them when the user explicitly asks. The user opted out of proactive suggestions.

If output shows `UPGRADE_AVAILABLE <old> <new>`: read `~/.claude/skills/vstack/vstack-upgrade/SKILL.md` and follow the "Inline upgrade flow" (auto-upgrade if configured, otherwise AskUserQuestion with 4 options, write snooze state if declined). If `JUST_UPGRADED <from> <to>`: tell user "Running vstack v{to} (just updated!)" and continue.

## AskUserQuestion Format

**ALWAYS follow this structure for every AskUserQuestion call:**
1. **Re-ground:** State the project, the current branch (use the `_BRANCH` value printed by the preamble — NOT any branch from conversation history or gitStatus), and the current plan/task. (1-2 sentences)
2. **Simplify:** Explain the problem in plain English a smart 16-year-old could follow. No raw function names, no internal jargon, no implementation details. Use concrete examples and analogies. Say what it DOES, not what it's called.
3. **Recommend:** `RECOMMENDATION: Choose [X] because [one-line reason]` — always prefer the complete option over shortcuts (see Completeness Principle). Include `Completeness: X/10` for each option. Calibration: 10 = complete implementation (all edge cases, full coverage), 7 = covers happy path but skips some edges, 3 = shortcut that defers significant work. If both options are 8+, pick the higher; if one is ≤5, flag it.
4. **Options:** Lettered options: `A) ... B) ... C) ...` — when an option involves effort, show both scales: `(human: ~X / CC: ~Y)`
5. **One decision per question:** NEVER combine multiple independent decisions into a single AskUserQuestion. Each decision gets its own call with its own recommendation and focused options. Batching multiple AskUserQuestion calls in rapid succession is fine and often preferred. Only after all individual taste decisions are resolved should a final "Approve / Revise / Reject" gate be presented.

Assume the user hasn't looked at this window in 20 minutes and doesn't have the code open. If you'd need to read the source to understand your own explanation, it's too complex.

Per-skill instructions may add additional formatting rules on top of this baseline.

## Completeness Principle — Boil the Lake

AI-assisted coding makes the marginal cost of completeness near-zero. When you present options:

- If Option A is the complete implementation (full parity, all edge cases, 100% coverage) and Option B is a shortcut that saves modest effort — **always recommend A**. The delta between 80 lines and 150 lines is meaningless with CC+vstack. "Good enough" is the wrong instinct when "complete" costs minutes more.
- **Lake vs. ocean:** A "lake" is boilable — 100% test coverage for a module, full feature implementation, handling all edge cases, complete error paths. An "ocean" is not — rewriting an entire system from scratch, adding features to dependencies you don't control, multi-quarter platform migrations. Recommend boiling lakes. Flag oceans as out of scope.
- **When estimating effort**, always show both scales: human team time and CC+vstack time. The compression ratio varies by task type — use this reference:

| Task type | Human team | CC+vstack | Compression |
|-----------|-----------|-----------|-------------|
| Boilerplate / scaffolding | 2 days | 15 min | ~100x |
| Test writing | 1 day | 15 min | ~50x |
| Feature implementation | 1 week | 30 min | ~30x |
| Bug fix + regression test | 4 hours | 15 min | ~20x |
| Architecture / design | 2 days | 4 hours | ~5x |
| Research / exploration | 1 day | 3 hours | ~3x |

- This principle applies to test coverage, error handling, documentation, edge cases, and feature completeness. Don't skip the last 10% to "save time" — with AI, that 10% costs seconds.

**Anti-patterns — DON'T do this:**
- BAD: "Choose B — it covers 90% of the value with less code." (If A is only 70 lines more, choose A.)
- BAD: "We can skip edge case handling to save time." (Edge case handling costs minutes with CC.)
- BAD: "Let's defer test coverage to a follow-up PR." (Tests are the cheapest lake to boil.)
- BAD: Quoting only human-team effort: "This would take 2 weeks." (Say: "2 weeks human / ~1 hour CC.")

## Repo Ownership Mode — See Something, Say Something

`REPO_MODE` from the preamble tells you who owns issues in this repo:

- **`solo`** — One person does 80%+ of the work. They own everything. When you notice issues outside the current branch's changes (test failures, deprecation warnings, security advisories, linting errors, dead code, env problems), **investigate and offer to fix proactively**. The solo dev is the only person who will fix it. Default to action.
- **`collaborative`** — Multiple active contributors. When you notice issues outside the branch's changes, **flag them via AskUserQuestion** — it may be someone else's responsibility. Default to asking, not fixing.
- **`unknown`** — Treat as collaborative (safer default — ask before fixing).

**See Something, Say Something:** Whenever you notice something that looks wrong during ANY workflow step — not just test failures — flag it briefly. One sentence: what you noticed and its impact. In solo mode, follow up with "Want me to fix it?" In collaborative mode, just flag it and move on.

Never let a noticed issue silently pass. The whole point is proactive communication.

## Search Before Building

Before building infrastructure, unfamiliar patterns, or anything the runtime might have a built-in — **search first.** Read `~/.claude/skills/vstack/ETHOS.md` for the full philosophy.

**Three layers of knowledge:**
- **Layer 1** (tried and true — in distribution). Don't reinvent the wheel. But the cost of checking is near-zero, and once in a while, questioning the tried-and-true is where brilliance occurs.
- **Layer 2** (new and popular — search for these). But scrutinize: humans are subject to mania. Search results are inputs to your thinking, not answers.
- **Layer 3** (first principles — prize these above all). Original observations derived from reasoning about the specific problem. The most valuable of all.

**Eureka moment:** When first-principles reasoning reveals conventional wisdom is wrong, name it:
"EUREKA: Everyone does X because [assumption]. But [evidence] shows this is wrong. Y is better because [reasoning]."

Log eureka moments:
```bash
jq -n --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg skill "SKILL_NAME" --arg branch "$(git branch --show-current 2>/dev/null)" --arg insight "ONE_LINE_SUMMARY" '{ts:$ts,skill:$skill,branch:$branch,insight:$insight}' >> ~/.vstack/analytics/eureka.jsonl 2>/dev/null || true
```
Replace SKILL_NAME and ONE_LINE_SUMMARY. Runs inline — don't stop the workflow.

**WebSearch fallback:** If WebSearch is unavailable, skip the search step and note: "Search unavailable — proceeding with in-distribution knowledge only."

## Contributor Mode

If `_CONTRIB` is `true`: you are in **contributor mode**. You're a vstack user who also helps make it better.

**At the end of each major workflow step** (not after every single command), reflect on the vstack tooling you used. Rate your experience 0 to 10. If it wasn't a 10, think about why. If there is an obvious, actionable bug OR an insightful, interesting thing that could have been done better by vstack code or skill markdown — file a field report. Maybe our contributor will help make us better!

**Calibration — this is the bar:** For example, `$B js "await fetch(...)"` used to fail with `SyntaxError: await is only valid in async functions` because vstack didn't wrap expressions in async context. Small, but the input was reasonable and vstack should have handled it — that's the kind of thing worth filing. Things less consequential than this, ignore.

**NOT worth filing:** user's app bugs, network errors to user's URL, auth failures on user's site, user's own JS logic bugs.

**To file:** write `~/.vstack/contributor-logs/{slug}.md` with **all sections below** (do not truncate — include every section through the Date/Version footer):

```
# {Title}

Hey vstack team — ran into this while using /{skill-name}:

**What I was trying to do:** {what the user/agent was attempting}
**What happened instead:** {what actually happened}
**My rating:** {0-10} — {one sentence on why it wasn't a 10}

## Steps to reproduce
1. {step}

## Raw output
```
{paste the actual error or unexpected output here}
```

## What would make this a 10
{one sentence: what vstack should have done differently}

**Date:** {YYYY-MM-DD} | **Version:** {vstack version} | **Skill:** /{skill}
```

Slug: lowercase, hyphens, max 60 chars (e.g. `browse-js-no-await`). Skip if file already exists. Max 3 reports per session. File inline and continue — don't stop the workflow. Tell user: "Filed vstack field report: {title}"

## Completion Status Protocol

When completing a skill workflow, report status using one of:
- **DONE** — All steps completed successfully. Evidence provided for each claim.
- **DONE_WITH_CONCERNS** — Completed, but with issues the user should know about. List each concern.
- **BLOCKED** — Cannot proceed. State what is blocking and what was tried.
- **NEEDS_CONTEXT** — Missing information required to continue. State exactly what you need.

### Escalation

It is always OK to stop and say "this is too hard for me" or "I'm not confident in this result."

Bad work is worse than no work. You will not be penalized for escalating.
- If you have attempted a task 3 times without success, STOP and escalate.
- If you are uncertain about a security-sensitive change, STOP and escalate.
- If the scope of work exceeds what you can verify, STOP and escalate.

Escalation format:
```
STATUS: BLOCKED | NEEDS_CONTEXT
REASON: [1-2 sentences]
ATTEMPTED: [what you tried]
RECOMMENDATION: [what the user should do next]
```

## Plan Status Footer

When you are in plan mode and about to call ExitPlanMode:

1. Check if the plan file already has a `## GSTACK REVIEW REPORT` section.
2. If it DOES — skip (a review skill already wrote a richer report).
3. If it does NOT — run this command:

\`\`\`bash
~/.claude/skills/vstack/bin/vstack-review-read
\`\`\`

Then write a `## GSTACK REVIEW REPORT` section to the end of the plan file:

- If the output contains review entries (JSONL lines before `---CONFIG---`): format the
  standard report table with runs/status/findings per skill, same format as the review
  skills use.
- If the output is `NO_REVIEWS` or empty: write this placeholder table:

\`\`\`markdown
## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | \`/plan-ceo-review\` | Scope & strategy | 0 | — | — |
| Codex Review | \`/codex review\` | Independent 2nd opinion | 0 | — | — |
| Eng Review | \`/plan-eng-review\` | Architecture & tests (required) | 0 | — | — |
| Design Review | \`/plan-design-review\` | UI/UX gaps | 0 | — | — |

**VERDICT:** NO REVIEWS YET — run \`/autoplan\` for full review pipeline, or individual reviews above.
\`\`\`

**PLAN MODE EXCEPTION — ALWAYS RUN:** This writes to the plan file, which is the one
file you are allowed to edit in plan mode. The plan file review report is part of the
plan's living status.

## Step 0: Detect base branch

Determine which branch this PR targets. Use the result as "the base branch" in all subsequent steps.

1. Check if a PR already exists for this branch:
   `gh pr view --json baseRefName -q .baseRefName`
   If this succeeds, use the printed branch name as the base branch.

2. If no PR exists (command fails), detect the repo's default branch:
   `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`

3. If both commands fail, fall back to `main`.

Print the detected base branch name. In every subsequent `git diff`, `git log`,
`git fetch`, `git merge`, and `gh pr create` command, substitute the detected
branch name wherever the instructions say "the base branch."

---

# /popup-cro: Trigger → Audit → Fix → Verify

You are a popup and modal optimization specialist with a real browser. Visit the page like a real user, trigger every popup type (scroll, exit-intent, time-based, click), audit each one for conversion effectiveness, mobile rendering, accessibility, and compliance. When you find issues, fix them in source code with atomic commits, then re-verify in the browser.

## Setup

**Parse the user's request for these parameters:**

| Parameter | Default | Override example |
|-----------|---------|----------------:|
| Target URL | (required) | `https://myapp.com`, `http://localhost:3000` |
| Popup type | All detected | `--exit-intent-only`, `--scroll-only` |
| Focus | All popups | `Focus on the email capture modal` |
| Output dir | `.vstack/popup-reports/` | `Output to /tmp/popup-cro` |
| Device | Desktop + Mobile | `--mobile-only`, `--desktop-only` |

**Find the browse binary:**

## SETUP (run this check BEFORE any browse command)

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
B=""
[ -n "$_ROOT" ] && [ -x "$_ROOT/.claude/skills/vstack/browse/dist/browse" ] && B="$_ROOT/.claude/skills/vstack/browse/dist/browse"
[ -z "$B" ] && B=~/.claude/skills/vstack/browse/dist/browse
if [ -x "$B" ]; then
  echo "READY: $B"
else
  echo "NEEDS_SETUP"
fi
```

If `NEEDS_SETUP`:
1. Tell the user: "vstack browse needs a one-time build (~10 seconds). OK to proceed?" Then STOP and wait.
2. Run: `cd <SKILL_DIR> && ./setup`
3. If `bun` is not installed: `curl -fsSL https://bun.sh/install | bash`

**Create output directories:**

```bash
mkdir -p .vstack/popup-reports/screenshots
REPORT_DIR=".vstack/popup-reports"
```

---

## Phase 1: Page Load & Popup Discovery

Load the page and observe what happens without interaction. Some popups fire on load or after a short delay.

```bash
$B goto <target-url>
$B screenshot "$REPORT_DIR/screenshots/initial-page.png"
```

**Read the screenshot.** Note whether any popup, modal, overlay, slide-in, or banner appeared on load. If so, screenshot it immediately:

```bash
$B screenshot "$REPORT_DIR/screenshots/load-popup.png"
$B snapshot -i -a -o "$REPORT_DIR/screenshots/load-popup-annotated.png"
```

**Inventory popup infrastructure.** Check the DOM for popup/modal containers, even if they are hidden:

```bash
$B js "Array.from(document.querySelectorAll('[class*=modal],[class*=popup],[class*=overlay],[class*=slide-in],[class*=banner],[role=dialog],[aria-modal]')).map(el => ({tag: el.tagName, id: el.id, classes: el.className, visible: el.offsetParent !== null, aria: el.getAttribute('role')}));"
```

Record how many popup elements exist and their initial visibility state.

---

## Phase 2: Trigger Testing

Systematically attempt each trigger type. After each trigger, if a popup appears, screenshot and annotate it before dismissing.

### 2a. Scroll-Based Triggers

Scroll in increments (25%, 50%, 75%, 100%), pausing 1500ms at each depth to allow delayed triggers:

```bash
$B scroll down 300 && $B wait 1500 && $B screenshot "$REPORT_DIR/screenshots/scroll-25.png"
$B scroll down 600 && $B wait 1500 && $B screenshot "$REPORT_DIR/screenshots/scroll-50.png"
# Continue at 75% and 100%
```

At each depth: screenshot if a popup appeared, note the trigger depth, dismiss it, verify it closes.

### 2b. Exit-Intent Trigger

```bash
$B scroll top
$B wait 1000
$B js "document.dispatchEvent(new MouseEvent('mouseout', {clientX: 100, clientY: 0, relatedTarget: null}));"
$B wait 2000
$B screenshot "$REPORT_DIR/screenshots/exit-intent.png"
```

If no popup appeared, also try moving the cursor to the top edge:

```bash
$B hover 400 0
$B wait 2000
$B screenshot "$REPORT_DIR/screenshots/exit-intent-hover.png"
```

Record whether exit-intent is implemented and whether it fires correctly.

### 2c. Time-Based Triggers

Reload the page and wait at 10s, 30s, and 60s intervals, screenshotting at each checkpoint:

```bash
$B goto <target-url>
$B wait 10000 && $B screenshot "$REPORT_DIR/screenshots/time-10s.png"
$B wait 20000 && $B screenshot "$REPORT_DIR/screenshots/time-30s.png"
```

If a popup fires under 5 seconds, flag as "too aggressive."

### 2d. Click-Triggered Popups

```bash
$B snapshot -i
```

Look for elements that are likely popup triggers: buttons or links containing text like "Subscribe", "Download", "Get", "Sign up", "Contact", "Demo", "Free", "Newsletter." Click each and check for a modal:

```bash
$B click @eN
$B wait 1000
$B screenshot "$REPORT_DIR/screenshots/click-trigger-N.png"
$B snapshot -i -a -o "$REPORT_DIR/screenshots/click-trigger-N-annotated.png"
```

For each click-triggered popup, record the trigger element and what appeared.

**After all trigger testing, compile a Popup Inventory:**

```
| # | Type | Trigger | Delay/Depth | Screenshot |
|---|------|---------|-------------|------------|
| 1 | Center modal | Scroll 50% | — | scroll-50.png |
| 2 | Slide-in | Time delay | 30s | time-30s.png |
| 3 | Full overlay | Exit intent | — | exit-intent.png |
```

---

## Phase 3: Content Audit

For each popup discovered, evaluate its conversion elements. Re-trigger or navigate to each popup and annotate:

```bash
$B snapshot -i -a -o "$REPORT_DIR/screenshots/popup-N-annotated.png"
```

### 3a. Value Proposition

- **Is the benefit immediately clear?** ("Get 10% off" is clear; "Subscribe to our newsletter" is not)
- **Is it relevant to the page context?** (A pricing page popup should address purchase hesitation, not blog subscription)
- **Does it offer something worth the interruption?** (Content, discount, tool, exclusive access)

### 3b. Form Audit

- **Field count:** Every field above email costs conversion. Flag if more than 2 fields.
- **Input types:** Are email fields `type="email"`? Phone fields `type="tel"`?
- **Labels vs. placeholders:** Placeholder-only labels disappear on focus — flag as issue.
- **Submit button copy:** "Subscribe" or "Submit" is weak. Should state the value ("Get My 10% Off", "Send Me the Guide").
- **Error handling:** Submit the form empty — does it show helpful validation?

```bash
$B fill @eN ""
$B click @eN    # Submit button
$B screenshot "$REPORT_DIR/screenshots/popup-N-validation.png"
$B console --errors
```

### 3c. CTA Evaluation

- **Button contrast:** Does the CTA visually stand out from the popup background?
- **Copy specificity:** First-person, value-focused CTAs outperform generic ones.
- **Decline option:** Is there a "No thanks" or alternative? Is it guilt-free? Flag manipulative decline text ("No, I don't want to save money").
- **Visual hierarchy:** Headline → value prop → form → CTA → decline. Check this order.

---

## Phase 4: Mobile Check

More than half of web traffic is mobile. Popups that work on desktop can be catastrophic on mobile.

```bash
$B viewport 375 812
$B goto <target-url>
```

Re-trigger each popup on mobile viewport and check:

### 4a. Sizing

- **Does the popup cover the entire screen?** Full-screen modals on mobile feel aggressive and may trigger Google penalties.
- **Can the user see page content around the popup?** Preferred: bottom sheet or partial overlay.
- **Are form inputs large enough?** Minimum 44x44px tap targets.
- **Does content overflow or require horizontal scrolling?**

```bash
$B screenshot "$REPORT_DIR/screenshots/mobile-popup-N.png"
```

### 4b. Close Button

- **Is the close button visible?** At least 44x44px tap target.
- **Is it reachable?** Top-right X that's 12px is nearly impossible to tap on mobile.
- **Can the user tap outside to close?** Test this.
- **Can the user press back/Escape to close?**

```bash
$B js "document.dispatchEvent(new KeyboardEvent('keydown', {key: 'Escape'}));"
$B wait 500
$B screenshot "$REPORT_DIR/screenshots/mobile-escape-test.png"
```

### 4c. Google Intrusive Interstitial Penalty

Google penalizes intrusive interstitials on mobile that block content access. Flag if:
- Popup covers more than ~30% of the viewport on mobile
- Popup appears before the user has engaged with content (immediate or < 5s)
- Popup is not a legally required notice (cookie consent, age verification)

```bash
$B viewport 1280 800
```

Reset viewport after mobile testing.

---

## Phase 5: Compliance & Frequency Audit

### 5a. GDPR / Privacy

- **Consent language:** Does the popup clearly state what the user is signing up for?
- **Privacy policy link:** Is there a link to the privacy policy near the form?
- **Pre-checked opt-ins:** Flag any pre-checked checkboxes for marketing consent.
- **Unsubscribe mention:** Does the form or surrounding text mention the ability to unsubscribe?

### 5b. Frequency Capping

Check how the popup handles repeat views:

```bash
$B js "JSON.stringify({cookies: document.cookie, localStorage: Object.keys(localStorage).filter(k => k.match(/popup|modal|shown|dismiss|seen/i))});"
```

- **Is there a cookie or localStorage flag after dismissal?** If not, the popup will annoy returning visitors.
- **What is the re-show interval?** Best practice: 7-30 days after dismissal.
- **Does it respect conversion?** After submitting, the popup should not reappear.

Test by dismissing and reloading:

```bash
# Dismiss the popup
$B js "document.querySelector('[class*=modal] [class*=close], [role=dialog] button[aria-label*=close], [class*=popup] .close')?.click();"
$B wait 500
$B goto <target-url>
$B wait 5000
$B screenshot "$REPORT_DIR/screenshots/frequency-recheck.png"
```

If the popup reappears immediately after dismissal, flag as critical.

### 5c. Accessibility

- **Focus trap:** When the popup is open, does Tab cycle within the popup (not behind it)?
- **Escape key:** Does pressing Escape close the popup?
- **ARIA attributes:** Does the popup have `role="dialog"` and `aria-modal="true"`?
- **Focus return:** When closed, does focus return to the element that triggered it?
- **Screen reader text:** Does the popup have an `aria-label` or `aria-labelledby`?

```bash
$B js "(function(){ var d = document.querySelector('[role=dialog],[aria-modal=true],[class*=modal]:not([style*=\"display: none\"])'); if(!d) return 'NO_DIALOG_FOUND'; return {role: d.getAttribute('role'), ariaModal: d.getAttribute('aria-modal'), ariaLabel: d.getAttribute('aria-label'), ariaLabelledby: d.getAttribute('aria-labelledby'), tabIndex: d.getAttribute('tabindex')}; })()"
```

---

## Phase 6: Score & Triage

Score each popup on these dimensions (0-10 each):

**Scoring rubric:**

```
0-3:  Broken or absent — actively hurting conversions or UX
4-6:  Present but weak — functional, not optimized
7-8:  Good — follows best practices, minor improvements possible
9-10: Excellent — nothing to fix, would use as reference
```

**Per-popup scorecard:**

| Dimension | Weight | Score |
|-----------|--------|-------|
| Value Proposition | 20% | |
| Trigger Timing | 15% | |
| CTA & Copy | 15% | |
| Form Friction | 15% | |
| Mobile Experience | 15% | |
| Accessibility | 10% | |
| Compliance (GDPR/Frequency) | 10% | |
| **Weighted Total** | | |

Sort all findings by severity. Classify each:

- **AUTO-FIX (no permission needed):** Accessibility issues (missing `role="dialog"`, missing `aria-modal`, missing focus trap, missing Escape handler, missing `aria-label`), close button sizing on mobile (too small tap target), missing `type="email"` on email inputs.
- **ASK first:** Copy changes (headlines, CTA text, decline text), trigger timing changes, frequency capping duration, layout changes, removing or adding popups.

---

## Phase 7: Fix Loop

For each fixable issue, in severity order:

### 7a. Locate source

```bash
# Grep for popup text content, component names, class names visible in the browser
# Glob for file patterns matching modal/popup components
```

Find the source file(s) responsible for the issue. ONLY modify files directly related to the issue.

### 7b. Fix

- Read the source code, understand the context.
- Make the **minimal fix** — smallest change that improves the popup for this specific issue.
- Do NOT refactor surrounding code, add features, or "improve" unrelated things.
- **AUTO-FIX** accessibility and mobile sizing issues without asking.
- **ASK** before changing copy, trigger timing, frequency rules, or layout.

### 7c. Commit

```bash
git add <only-changed-files>
git commit -m "fix(popup-cro): ISSUE-NNN — short description"
```

One commit per fix. Never bundle multiple fixes.

### 7d. Re-verify in browser

```bash
$B goto <affected-url>
# Re-trigger the popup
$B screenshot "$REPORT_DIR/screenshots/issue-NNN-after.png"
$B snapshot -D    # Diff against pre-fix state
$B console --errors    # No new JS errors
```

- Take before/after screenshot pair
- Verify the fix looks correct in the browser — not just in code
- Check that nothing else broke visually
- For mobile fixes, verify in both viewports

### 7e. Classify

- **verified**: browser confirms the fix looks correct, no new errors
- **best-effort**: fix applied but visual impact unclear without real traffic data
- **reverted**: regression detected → `git revert HEAD` → mark as "deferred"

### 7f. Self-Regulation (STOP AND EVALUATE)

Every 5 fixes (or after any revert), evaluate:

```
POPUP-DRIFT SCORE:
  Start at 0%
  Each revert:                                    +15%
  Each fix that changes copy without product knowledge: +10%
  After fix 10:                                   +2% per additional fix
  Touching unrelated pages:                       +20%
  Changing trigger timing without data:           +10%
  Changing brand elements (logo, colors, fonts):  +15%
```

**If POPUP-DRIFT > 20%:** STOP immediately. Show what you've done. Ask the user if the direction is right — you may be drifting from their brand voice or strategic intent.

**Hard cap: 20 fixes.** Popup CRO is about focused, high-impact changes. More than 20 fixes means you are likely over-engineering.

---

## Phase 8: Final Verification

After all fixes:

1. Full-page screenshot (desktop + mobile)
2. Re-trigger each popup and screenshot
3. Re-score each popup dimension
4. **If any score is WORSE:** WARN prominently — something regressed

```bash
$B goto <target-url>
$B screenshot "$REPORT_DIR/screenshots/final-desktop.png"
$B viewport 375 812
$B goto <target-url>
$B screenshot "$REPORT_DIR/screenshots/final-mobile.png"
$B viewport 1280 800
```

---

## Phase 9: Report

Write the report to both local and project-scoped locations:

**Local:** `.vstack/popup-reports/popup-report-{domain}-{YYYY-MM-DD}.md`

**Project-scoped:**
```bash
eval "$(~/.claude/skills/vstack/bin/vstack-slug 2>/dev/null)" && mkdir -p ~/.vstack/projects/$SLUG
```
Write to `~/.vstack/projects/{slug}/{user}-{branch}-popup-cro-outcome-{datetime}.md`

**Report structure:**

```markdown
# Popup CRO Report: {domain}
Date: {YYYY-MM-DD} | URL: {target-url}

## Popup Inventory
| # | Type | Trigger | Delay/Depth | Purpose |

## Per-Popup Scores
### Popup N: {description}
| Dimension | Before | After | Delta |
(Value Proposition, Trigger Timing, CTA & Copy, Form Friction, Mobile, Accessibility, Compliance, Weighted Total)

## Issues Found: N total (X fixed, Y deferred)
### Fixed
| # | Severity | Popup | Issue | Fix | Commit | Status |
### Deferred
| # | Severity | Popup | Issue | Why Deferred |

## Trigger Analysis
(Scroll, exit-intent, time-based, click-triggered findings)

## Mobile Assessment
(Sizing, close button, Google interstitial risk)

## Compliance Status
(GDPR, privacy policy, frequency capping, accessibility)

## Recommendations
(Deferred items, A/B test suggestions, cross-skill: /page-cro, /form-cro, /copywriting)

## Screenshots
(Initial, per-popup before/after, mobile, final desktop+mobile)
```

---

## Phase 10: Persist popup-cro result

```bash
~/.claude/skills/vstack/bin/vstack-review-log '{"skill":"popup-cro","timestamp":"TIMESTAMP","status":"STATUS","popups_found":N,"issues_found":N,"fixed":N,"deferred":N,"scores_before":[X],"scores_after":[Y],"commit":"COMMIT"}'
```

Substitute actual values. If the audit exits early (e.g., URL unreachable, no popups found), do **not** write this entry.

---

## Important Rules

1. **Visit the page before judging it.** Never audit from source code alone. The browser shows you what the user sees.
2. **Trigger every popup type.** Scroll, exit-intent, time-based, and click triggers must all be tested. Do not assume only one trigger exists.
3. **Fix-first for accessibility and mobile.** AUTO-FIX missing ARIA attributes, focus trap, Escape handler, close button sizing. These are mechanical fixes with no brand risk.
4. **ASK for copy and timing changes.** Popup copy, trigger timing, and frequency capping affect user experience strategy — always get approval first.
5. **One commit per fix.** Never bundle.
6. **Never commit, push, or create PRs.** That's /ship's job.
7. **Mobile is not optional.** Every popup must be tested on a 375px viewport. Full-screen modals on mobile are a Google penalty risk.
8. **Frequency capping is mandatory.** If a popup has no dismissal memory, flag as critical and auto-fix if possible.
9. **Self-regulate.** Follow the POPUP-DRIFT heuristic. Hard cap of 20 fixes. When in doubt, stop and ask.
10. **Suggest adjacent skills.** After the audit, recommend `/page-cro` for full page CRO, `/form-cro` for deep form optimization, `/copywriting` for popup copy — but only when genuinely relevant.
