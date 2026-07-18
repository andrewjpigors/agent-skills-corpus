---
name: copiatore
description: Analyze and fix website UI/UX/a11y/performance. Quick scan, deep audit with Teams, autodebug loop, or iterative dev companion.
user_invocable: true
---

# Copiatore — Design Intelligence

## Iron Rule
```
A finding without a measured value AND visual verification in the screenshot is not a finding. No exceptions.
```
"`.hero h1` has font-size 14px — below 16px minimum" = finding. "The typography could be improved" = noise. If you can't point to a pixel value, a CSS selector, and a screenshot region, you haven't found anything — you're guessing.

## Onboarding

When invoked WITHOUT a specific command (e.g., just `/copiatore` or a generic request like "analizza questo sito"), present this intake using AskUserQuestion:

```
Question: "Cosa vuoi fare?"
Header: "Mode"

Option 1: "Analisi design (Recommended)"
  Description: "Audit completo: screenshot, design review con score, a11y, performance. Ti dico cosa non va e come fixare."

Option 2: "Clona un sito"
  Description: "Estraggo struttura, token, asset e ricostruisco il sito in HTML/CSS. Sezione per sezione, pixel-perfect."

Option 3: "Debug e fix"
  Description: "Trovo i problemi, li fixo nel codice, verifico con visual diff. Loop autonomo fino a convergenza."

Option 4: "Dev companion"
  Description: "Ti seguo mentre sviluppi. Feedback continuo su ogni cambio: visual diff, regressioni, suggerimenti."
```

**IF "Analisi design" was selected**, ask the analysis depth:
```
Question: "Che tipo di analisi?"
Header: "Profondità"

Option 1: "Rapida — technical + aesthetic sintetico (~2 min) (Recommended)"
  Description: "Score tecnico + valutazione estetica inline. Veloce, copre tutto l'essenziale."

Option 2: "Approfondita — design critic completo (~5 min)"
  Description: "Score tecnico + Design Critic agent con analisi estetica strutturata su 7 dimensioni."
```

Then ask for the URL:
```
Question: "Su quale sito lavoriamo?"
Header: "URL"
(free text — the user types the URL)
```

**Route to the appropriate mode:**
- "Analisi design" + "Rapida" → scan + design_review + Step 1.5 inline
- "Analisi design" + "Approfondita" → scan + design_review + Step 1.5 via design-qa agent
- "Clona un sito" → clone workflow
- "Debug e fix" → heal workflow with heal_step convergence
- "Dev companion" → dev mode with baseline

**If the user gives a specific command** (e.g., `/copiatore scan https://example.com`), skip onboarding and execute directly.

---

## Step 0 — Site Context Audit (MANDATORY)

Before ANY analysis mode, gather site context. This is not the analysis — it's the data you need to analyze intelligently.

After `copiatore_navigate`, immediately run:

1. **`copiatore_extract`** — raw design data (colors, typography, spacing, layout)
2. **`copiatore_screenshot`** — above-fold visual. **Read it with the Read tool.** If you skip visual inspection, the analysis is unreliable.
3. **Detect framework** via `copiatore_evaluate` expression: `JSON.stringify({ viewport: document.querySelector('meta[name=viewport]')?.content, generator: document.querySelector('meta[name=generator]')?.content, next: !!document.getElementById('__next'), nuxt: !!window.__NUXT__, react: !!document.querySelector('[data-reactroot]'), angular: !!document.querySelector('[ng-version]') })`

From the extract + screenshot + framework check, classify:

| Signal | How to detect | Impact on analysis |
|--------|--------------|-------------------|
| **Site type** | URL patterns, content density, component mix | Marketing → visual impact priority. Dashboard → information density. E-commerce → conversion flow. Blog → readability. |
| **Framework** | Meta generator, `__next`, `__NUXT__`, `data-reactroot`, `ng-version` | SPA → check hydration artifacts. SSR → check FCP. Static → check caching. |
| **Design system maturity** | CSS variable count, `off_grid_ratio`, type `scale_ratio` from extract | Level 0-1 → flag everything. Level 3-4 → flag deviations from THEIR system, not generic rules. |
| **Auth wall** | Login form visible, redirect to /login, cookie consent overlays | Behind auth → tools see login page, not app. AskUserQuestion: provide session or analyze login page only. |
| **Dark mode** | `prefers-color-scheme` in stylesheets, `.dark` / `[data-theme]` toggles | Test BOTH modes. Contrast bugs hide in dark mode. |
| **Responsive setup** | Viewport meta present, breakpoint count from stylesheets | No viewport meta = CRITICAL. Zero breakpoints = mobile-hostile. |
| **Heavy assets** | Canvas/WebGL, `<video>`, image count >20, total asset weight | WebGL → `copiatore_fps_monitor` mandatory. Heavy images → LCP focus. |

**Output Step 0 as a classification table before proceeding.** Every subsequent step references this context.

**If `copiatore_extract` fails** → see Error Recovery Protocol below.
**If auth wall detected** → AskUserQuestion before continuing.

---

## Step 1.5 — Visual Impression Assessment

After the technical design_review (Step 1), evaluate the **aesthetic quality** of the site. This catches what data extraction misses: a site can score 85/100 technically while looking like a generic template.

**Two modes** (selected during onboarding):

### Inline Mode (Rapida)

Look at the screenshots. For each of 7 aspects, score 1-10 with one line of evidence. Not the full Design Critic process — an honest judgment in 30 seconds.

**FIRST:** look at the above-fold screenshot for 2 seconds. What does it communicate? What would you remember? Write one sentence.

**THEN evaluate:**

1. **DEPTH** — Are there layers? Shadows? Gradients? Or is everything flat on one plane?
2. **RHYTHM** — Do sections vary or repeat the same pattern? Is there tension/release in the scroll?
3. **PALETTE** — Do colors have depth and temperature variation, or are they 3 flat tints?
4. **CRAFT** — Hover states? Transitions? Eased animations? Or raw default browser behavior?
5. **ORIGINALITY** — Could you mistake this for a template? What makes it visually unique?
6. **RESONANCE** — Does it communicate the right emotion for its target audience?
7. **COHERENCE** — Does every element (icons, spacing, color, type) speak the same visual language?

Average = **Aesthetic Score** (1-10).

**Divergence flag:** IF aesthetic < 6 AND technical > 75, flag the gap explicitly:
> "Technically solid but aesthetically weak — the site works but doesn't impress."

### Deep Mode (Approfondita)

Spawn the `design-qa` agent as a subagent. Pass it:
- Desktop screenshots (above-fold + full-page)
- Mobile screenshots (above-fold + full-page)
- Site context from Step 0 (type, framework, palette, type scale)
- Technical score from Step 1

The agent runs its full 4-phase methodology and returns a structured aesthetic assessment. See `.claude/agents/design-qa.md` for the complete process.

### Output Format — Dual Score

Every analysis report shows BOTH scores side by side:

```
DESIGN SCORE
───────────────────────────────
Technical    [0-100]  Grade: [A-F]
Aesthetic    [1-10]   [⚠ if < 6]
───────────────────────────────

[If divergence: "Technical score reflects correctness (grid, a11y,
type scale). Aesthetic score reflects visual quality (depth, craft,
originality). This site is correct but not beautiful."]
```

The two scores are **independent** — neither overrides the other. Both appear in the report. The user decides which to act on.

---

## Post-Report Prompt

After EVERY analysis report (scan, audit, fix, compare), the agent MUST ask the user what to do next. Never deliver a report and stop.

```
Question: "Cosa vuoi fare?"
Header: "Next"

Option 1: "Fix i problemi trovati" [Recommended if critical/major findings exist]
  Description: "Applico le fix nel codice, verifico con visual diff."

Option 2: "Migliora stile/estetica" [Recommended if aesthetic < 6]
  Description: "Ti propongo 3 interventi per alzare l'impatto visivo."

Option 3: "Approfondisci un'area specifica"
  Description: "Scegli: a11y, performance, mobile, una sezione, un componente."

Option 4: "Fatto così"
  Description: "Il report è sufficiente, non serve altro."
```

**Recommendation logic:**
- IF any critical/major findings → recommend Option 1
- ELSE IF aesthetic < 6 AND technical > 60 → recommend Option 2
- ELSE → recommend Option 4

---

## Design Criteria

All analysis MUST evaluate against the design criteria in `.claude/design-criteria.md`. This includes:
- Visual Structure Checklist (alignment, whitespace, weight, hierarchy)
- Gestalt Principles (proximity, alignment, contrast, repetition, closure, figure/ground)
- Cognitive Load Thresholds (Cowan 2001: 4±1 chunks)
- Fitts's Law (48px mobile, 32px desktop, 8px gap)
- Typography Standards (scale, measure, spacing)
- Severity Classification (critical/major/minor/suggestion)

**Every scan, audit, and fix MUST apply these criteria. No exceptions.**

Additionally, use `.claude/design-references.md` for industry-standard benchmarks:
- Apple HIG patterns (layout, typography, color, motion, components)
- Material Design 3 patterns (grid, type scale, color system, elevation)
- Awwwards/FWA patterns (hero sections, scroll interactions, typography-driven design)
- Anti-patterns checklist (layout, typography, color, interaction, performance fails)
- Design scoring rubric (0–10 per dimension, total 0–100)

---

## Design Judgment Patterns

Judgment heuristics for design analysis. Not every pattern applies to every site — scan all and apply those that illuminate blind spots in the current analysis.

### Visual Structure Judgment

1. **Intentional vs Accidental Whitespace**: Large gap near fold — deliberate (hero breathing room) or broken (missing content, collapsed container)? Check: does the gap align with the spacing grid? Does a similar pattern appear elsewhere on the page?
2. **Consistency Signal**: 80% of cards have 16px padding, one has 24px — different card type (intentional) or bug? Check: different CSS class? Different content type? If same class → bug.
3. **Extracted Data vs Visual Truth**: CSS says `gap: 16px` but screenshot shows uneven spacing → the visual is authoritative. CSS may be overridden by child margins, flex-grow, or percentage widths. Always verify extracted data against the screenshot.

### Typography Judgment

4. **System Font Detection**: `font-family: system-ui, -apple-system` as primary (not fallback) → intentional choice, not "missing custom font."
5. **Scale Ratio Tolerance**: Extracted `scale_ratio` of 1.24 when Major Third is 1.25 → this IS Major Third with rounding. Tolerance: ±0.03 from named ratios before flagging "no scale."
6. **Heading Level vs Visual Size**: h3 visually larger than h2 → bug, OR intentional de-emphasis (h2 in sidebar, different section). Check context before flagging.

### Color Judgment

7. **Brand vs UI Color**: Site brand is red, buttons are blue → blue is UI convention (action color), not brand inconsistency. Flag only when the same function (e.g., primary CTA) uses different colors in different locations.
8. **Contrast in Context**: 3.8:1 on an 80px decorative heading → acceptable (WCAG large text: 3:1). Same ratio on 14px body → critical. Font size determines the threshold.

### Layout Judgment

9. **Mobile-First vs Desktop-First**: Desktop clean + mobile broken → desktop-first. Mobile clean + desktop gaps → mobile-first. This changes the fix strategy: add mobile overrides vs add desktop overrides.
10. **Content Density by Site Type**: Marketing: 30-40% density is good (breathing room sells). Dashboard: 60-80% is expected (density = efficiency). Never apply dashboard metrics to a landing page or vice versa.

### Performance Judgment

11. **Framework Tax**: Next.js with 200KB JS → lean. Static brochure with 200KB JS → bloated. The framework context from Step 0 determines whether a metric is good or bad.
12. **FPS in Context**: 60fps target applies to animations and scroll. Static page with 45fps at idle → the GPU isn't being asked to do anything. Only flag FPS during active animations or scroll.

### The Contrarian Check

13. **"Is this actually bad?"**: Before flagging, ask: would a senior designer at Apple/Stripe/Linear defend this choice? If yes → it's a design decision, not a bug. Flag as `suggestion`, not `major`.
14. **"Am I measuring the right thing?"**: Beautiful typography + 4s LCP → the visual quality is real AND the perf issue is real. Don't let one dimension poison the assessment of another. Score independently.

---

## Site Type Decision Tree

After Step 0 classifies the site, route the analysis emphasis:

**Marketing / Landing Page**
- Priority: Visual impact, hero effectiveness, CTA clarity, scroll narrative
- Key metrics: Above-fold hierarchy, CTA contrast ratio, Fitts target sizes
- Common traps: Hero >100vh pushing CTA below fold, font too small for scanning distance
- Lighten: Dense a11y audit (unless requested). Heavy perf audit (unless >3s LCP).

**E-commerce / Product Page**
- Priority: Product visibility, price clarity, add-to-cart prominence, trust signals
- Key metrics: Product image quality, price font weight vs body, CTA size, review visibility
- Common traps: Competing CTAs, cluttered above-fold, slow product image loading
- Add: `copiatore_functional_test` on add-to-cart + checkout flow

**Dashboard / SaaS App**
- Priority: Information density, scan-ability, action discoverability, empty states
- Key metrics: Content-to-chrome ratio, nav depth, data table readability, loading states
- Common traps: Overloaded sidebar, no empty states, inconsistent card heights
- Add: Test at 1024px (common laptop viewport) via `copiatore_emulate`

**Blog / Content Site**
- Priority: Readability, typography quality, content hierarchy, reading flow
- Key metrics: Line length (45-75ch), line height (1.5+), heading hierarchy, image-to-text ratio
- Common traps: Line >80ch, skipped heading levels, missing article landmarks
- Add: Full a11y audit (content sites have highest accessibility obligations)

**Portfolio / Creative**
- Priority: Visual storytelling, animation quality, load performance, unique interactions
- Key metrics: FPS during scroll, LCP (usually image-heavy), interaction smoothness
- Common traps: Over-animated (user fatigue), slow initial load, inaccessible custom interactions
- Add: `copiatore_fps_monitor` + `copiatore_gesture` for scroll interactions

**Web App (forms, flows)**
- Priority: Form usability, error handling, flow completion, state management
- Key metrics: Input sizes, label clarity, error message placement, step indicators
- Common traps: Bad inline validation timing, unclear required fields, no progress indicator
- Add: `copiatore_functional_test` on all forms + `copiatore_user_journey`

### Step 0 Integration with Modes

Every mode listed in the Commands table starts with `copiatore_navigate`. Immediately after navigation, **run Step 0 before proceeding** with mode-specific steps. Exceptions:
- `tokens` — pure extraction, no analysis judgment needed
- `bench` — HTTP-level test, no design context needed
- `export-tokens` — format conversion, no analysis

---

## Commands

Parse the user's command after `/copiatore`:

| Command | Mode | Description |
|---------|------|-------------|
| `scan <url>` | Quick | Single-agent snapshot + visual analysis |
| `audit <url>` | Deep | Team of 4 specialist agents |
| `fix <url>` | Autodebug | Deep audit + apply fixes + verify loop |
| `dev <url>` | Iterative | Continuous feedback while building |
| `tokens <url>` | Extract | Design tokens only (CSS variables) |
| `compare <a> <b>` | Compare | Side-by-side design comparison |
| `test <url>` | Functional | Automated form/CTA testing |
| `heal <url> [--full]` | Autonomous | Design QA agent fix loop |
| `clone <url>` | Clone | Replicate site visual design into HTML/CSS |
| `a11y-axe <url>` | A11y | axe-core powered accessibility audit |
| `perf <url>` | Performance | Lighthouse + Web Vitals + PageSpeed audit |
| `bench <url>` | Benchmark | HTTP load test with autocannon |
| `export-tokens <url>` | Export | W3C DTCG tokens + Style Dictionary multi-platform |
| `create` | Create | Build a new site from scratch with selected style |

---

## Quick Mode (scan)

Read `skills/copiatore/methods/analysis.md` with the Read tool, then follow the ObserveProcess phases. For scan mode, skip Phase 2 mobile snapshot (desktop only) and use inline aesthetic assessment.

## Quick Functional Test (test)

1. `copiatore_navigate` to the URL
2. `copiatore_interactive_map` — discover forms, CTAs, orphan inputs
3. `copiatore_functional_test` mode:auto — smart-fill, click CTAs, capture transitions
4. `copiatore_test_report` save:true — persist results, check regressions
5. Output: pass/fail per form + CTA, network/console errors, transition frame captures

## Design QA Agent (heal)

Read `skills/copiatore/methods/heal.md` with the Read tool. `/copiatore heal <url>` uses checkpoint mode (AskUserQuestion for ambiguous choices). `/copiatore heal <url> --full` uses full-auto mode (zero interruptions, always picks lowest-risk root-cause fix).

## Deep Mode (audit)

Read `skills/copiatore/methods/analysis.md` with the Read tool, then follow all ObserveProcess phases. Include mobile snapshot in Phase 2. Use deep aesthetic assessment (spawn design-qa agent).

### Device Presets

- **Desktop**: 1440x900 (default)
- **Mobile**: `copiatore_emulate` device: "iPhone 15 Pro"
- **Tablet**: `copiatore_emulate` device: "iPad Pro"
- **Android**: `copiatore_emulate` device: "Pixel 5"

Or use `copiatore_responsive_audit` with viewport array.

## Autodebug Loop (fix)

Read `skills/copiatore/methods/heal.md` with the Read tool, then follow the ConvergeProcess phases. Before healing, run a full analysis (methods/analysis.md) to establish the finding list. Apply Fix Alternatives protocol for every critical/major finding.

## Iterative Dev Companion (dev)

Continuous feedback loop during development:
1. **Baseline:** `copiatore_navigate` → `copiatore_snapshot` → `copiatore_screenshot` "baseline" → quick analysis
2. **Dev cycle (after each change):** Rebuild → navigate → screenshot "iteration-N" → `copiatore_visual_diff` baseline vs N → targeted analysis on changed area
3. **Milestone:** Full scan against baseline, device check, performance re-check, summary
4. **Update baseline:** After user approves, new screenshot "baseline"

Principles: fast feedback (not exhaustive reports), always screenshots + visual diffs, specific values ("4px off grid" not "alignment issues"), track regressions.

## Design Tokens Only (tokens)

1. `copiatore_navigate` → `copiatore_design_tokens`
2. Output CSS variables block, ready to paste

## Site Clone (clone)

Read `skills/copiatore/methods/clone.md` with the Read tool, then follow the ReplicateProcess phases. The key principle: every CSS property must use extracted CSS variables, never hardcoded values.

## Create Mode (create)

Read `skills/copiatore/methods/create.md` with the Read tool, then follow the BuildProcess phases. Requires a style module from `.claude/design-styles/` — the onboarding intake will ask the user to select one.

## Accessibility Audit (a11y-axe)

1. `copiatore_navigate` to the URL
2. `copiatore_a11y_axe` standard:wcag21aa → zero-false-positive violations
3. For manual checks: `copiatore_a11y_extract` (headings, landmarks, form labels)
4. Output: violations sorted by impact, WCAG compliance, score, remediation

## Performance Audit (perf)

1. `copiatore_navigate` → `copiatore_lighthouse` categories: performance,accessibility,best-practices
2. `copiatore_web_vitals` interact:true wait_ms:5000 — real LCP, INP, CLS, TTFB, FCP
3. Optional: `copiatore_pagespeed` strategy: mobile — CrUX field data
4. WebGL/canvas sites: `copiatore_fps_monitor` duration:3000 for GPU load
5. Output: Core Web Vitals table with Good/Needs Work/Poor + opportunities ranked by impact

## HTTP Load Benchmark (bench)

1. `copiatore_navigate` to the URL (to resolve the final URL)
2. `copiatore_http_benchmark` url: finalUrl, duration: 10, connections: 10
3. Returns: requests/sec, latency p50/p90/p99, throughput MB/s, errors
4. Compare against baseline or run with increasing connections to find saturation point

## Export Design Tokens (export-tokens)

1. `copiatore_navigate` → `copiatore_export_tokens` format: "all"
2. Outputs: DTCG JSON (W3C standard), CSS Variables, iOS Swift, Android XML
3. Use format: "dtcg", "css", "ios", or "android" for platform-specific.

## Quick Comparison (compare)

1. Navigate to URL A → `copiatore_extract` → data_a
2. Navigate to URL B → `copiatore_extract` → data_b
3. Structured comparison: palette, typography, spacing, layout

---

## Error Recovery Protocol

When a Copiatore tool fails, follow this protocol. Do NOT silently skip the step — either recover or report the gap.

| Failure | Likely Cause | Recovery |
|---------|-------------|----------|
| `copiatore_navigate` timeout | Slow site, SSR delay, infinite redirect | Retry with `wait_until: "domcontentloaded"`. Still fails → verify URL, ask user. |
| `copiatore_screenshot` blank/white | SPA hydration pending, canvas-only, overlay blocking | Wait 2s, retry. Still blank → `copiatore_evaluate` to check `document.readyState` and visible element count. |
| `copiatore_extract` empty data | Canvas-only site, iframe-embedded, heavy JS rendering | Try `copiatore_evaluate` with custom query. Report: "Extraction limited — site uses [canvas/iframe]. Manual inspection from screenshots only." |
| CDP session error | Navigation during CDP call, page crash, cross-origin frame | Retry once. Persistent → skip CDP-dependent metrics (FPS, GPU layers). Note gap in output. |
| `copiatore_visual_diff` fails | Different viewport sizes, page changed between screenshots | Ensure both screenshots use identical viewport. Re-navigate if page changed. |
| `copiatore_a11y_axe` timeout | Very large DOM, heavy JS | Use `copiatore_a11y_extract` instead (lighter). Note: "axe unavailable, structural analysis only." |
| Any tool returns partial data | Resource constraints, incomplete page load | Use what you have. Mark affected metrics as `[partial]` in output. |

### Cascading Failure Rule

If Step 0 (Site Context Audit) fails completely → you cannot trust subsequent analysis. Stop:
```
STATUS: BLOCKED
Cause: Site context audit failed — [what failed]
Action needed: [what the user should check]
```

If a non-critical tool fails mid-analysis → continue with remaining tools, mark the gap:
```
⚠ [tool_name] unavailable: [reason]. Analysis excludes [what's missing].
```

Never silently drop a tool failure. Every gap must appear in the final output.

---

## Self-Check (MANDATORY before completing ANY mode)

Before outputting final results, verify every item. If ANY check fails, go back and fix before outputting.

- [ ] **Did I READ the screenshots?** Used the Read tool on the .png files. If I only analyzed extracted data without visual inspection, the analysis is incomplete. Go back.
- [ ] **Did I reference specific elements?** Every finding must cite a CSS selector, pixel value, or screenshot region. "Improve spacing" is banned. "`.hero-cta` has 8px padding — Fitts minimum is 48px target" is correct.
- [ ] **Did I check above-fold?** The first screenful is 80% of first impression. If I skipped it, I missed the most important part.
- [ ] **Did I check mobile?** If the mode includes responsive analysis and I only checked desktop, the analysis is incomplete. Run `copiatore_emulate` iPhone 15 Pro.
- [ ] **Did I apply the design criteria?** Cross-check: my findings must map to at least 3 of the 7 criteria sections in `design-criteria.md`. If fewer → I'm not looking hard enough.
- [ ] **Did I account for site type?** A finding critical for marketing may be fine for a dashboard (and vice versa). Did I use the Step 0 classification?
- [ ] **Am I reporting what I found, or what I expected?** If every site gets the same 5 findings, I'm templating, not analyzing. Each site is different.
- [ ] **Did I catch conflicting signals?** Typography excellent but spacing broken → note BOTH. Don't let one dimension color the other.
- [ ] **Did I evaluate aesthetics?** If analysis mode, I MUST have an aesthetic score alongside the technical score. If I only ran design_review without Step 1.5, the analysis is incomplete.
- [ ] **Did I ask "Cosa vuoi fare?"** Every report ends with the post-report prompt. If I delivered a report and stopped, I failed.

---

## Fix Alternatives (fix/heal modes)

For every CRITICAL or MAJOR finding in fix/heal mode, present alternatives before applying. Never auto-commit to the first solution.

```
CRITICAL TYPOGRAPHY — Body text 13px, below 16px minimum
  Element: `.content p`
  Current: font-size: 13px
  Target: ≥16px

  Alternatives:
    A) Local fix — `.content p { font-size: 16px }`. Effort: 1min. Risk: none. Fixes symptom only.
    B) Systemic fix — Update CSS variable `--body-size` from 13px to 16px. Effort: 2min. Risk: cascading to other elements using the variable. Fixes root cause.
    C) Scale fix — Set base to 16px, recalculate heading scale at 1.25 ratio. Effort: 10min. Risk: medium (many elements change). Prevents recurrence.
  Recommend B: fixes root cause with minimal blast radius — all elements using --body-size get corrected together.
```

**AskUserQuestion format:** Start with "Recommend [LETTER]: [one-line reason]" then list all options as `A) ... B) ... C) ...`. One finding per question. Never batch.

For MINOR/SUGGESTION findings: apply the obvious fix directly, no alternatives needed.

**heal mode (--full):** In full-auto mode, always pick the option with lowest risk + fixes root cause. Log the choice in output so the user can review.

---

## Interactive Question Protocol

When a finding is ambiguous — you're not sure if something is intentional or a bug — present structured options via AskUserQuestion. Do NOT assume.

```
Question format:
  "Recommend [LETTER]: [one-line reason]. [description of what you found]"
  A) [interpretation 1 + action]
  B) [interpretation 2 + action]
  C) [investigate further before deciding]
```

**When to trigger:**
- Element looks intentionally different from the pattern (hero with asymmetric layout, oversized heading, unusual color)
- Spacing that could be either "breathing room" or "missing content"
- Component that might be under construction vs broken
- Any finding where the Contrarian Check (Pattern #13) gives a plausible "this is fine" answer

**When NOT to trigger** (just report directly):
- Clear violations with no defensible interpretation (13px body text, 2:1 contrast on readable text, no viewport meta)
- Numbers that are below documented thresholds (Fitts, WCAG, Core Web Vitals)
- Broken functionality (dead links, form errors, missing images)

**In scan mode:** No AskUserQuestion — speed matters. Report findings, flag ambiguous ones as `[AMBIGUOUS]` so the user knows.
**In audit/fix/heal mode:** Use AskUserQuestion for ambiguous findings.

---

## Completion Status Protocol

Every analysis output — not just clone — ends with this block:

```
STATUS: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
```

| Status | Condition |
|--------|-----------|
| `DONE` | Analysis complete, all tools ran, all criteria evaluated |
| `DONE_WITH_CONCERNS` | Analysis complete but some tools failed or data was partial — concerns listed |
| `BLOCKED` | Cannot produce reliable analysis — critical tool failure or auth wall |
| `NEEDS_CONTEXT` | Missing information from user (e.g., which page to analyze, target audience, brand guidelines) |

### Required Output Footer (all modes)

```
───────────────────────────────
STATUS: [DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT]
VERDICT: [SHIP | FIX FIRST | REDESIGN]
Site type: [classification from Step 0]
Findings: [N] critical, [N] major, [N] minor, [N] suggestions
Coverage: [which criteria sections were evaluated]
NOT analyzed: [what was intentionally excluded and why]
Gaps: [tools that failed or data that's missing]
Self-check: PASS
───────────────────────────────

Open questions (if any):
- [assumption made without user confirmation + what changes if wrong]
- [ambiguous finding left unresolved + which interpretation was chosen]
```

**Analysis Boundary ("NOT analyzed")**: This is NOT tool failures (that's "Gaps"). This is intentional exclusions based on mode and scope. Examples:
- "NOT analyzed: form functionality (scan mode — use `/copiatore test` for forms)"
- "NOT analyzed: mobile layout (tokens mode — pure extraction)"
- "NOT analyzed: performance (a11y-axe mode — use `/copiatore perf` for performance)"

Making exclusions explicit prevents the user from assuming everything was checked.

**Open Questions**: Track every assumption you made without user confirmation. If the user didn't answer an AskUserQuestion, or you had to assume an interpretation of an ambiguous finding, list it here. Never silently default to an interpretation — declare it.

If Self-Check did not pass, do not output. Fix first.

---

## Design Verdict

Every analysis ends with a clear, non-ambiguous verdict. STATUS tells you what happened. VERDICT tells you what to do.

| Verdict | Condition | Meaning |
|---------|-----------|---------|
| **SHIP** | Zero critical, ≤2 major, design is solid | Safe to go live. Minor issues can be fixed post-launch. |
| **FIX FIRST** | ≥1 critical OR >2 major, but all are fixable | Do not launch until critical/major findings are resolved. |
| **REDESIGN** | Fundamental structural problems — broken hierarchy, no responsive, layout collapse, a11y wall | Individual fixes won't save this. Needs architectural design work. |

**Verdict goes in the output footer, after STATUS.** The verdict is based on findings, not opinion. If findings say SHIP but your gut says something is off → add it as a concern in DONE_WITH_CONCERNS, don't inflate the verdict.

---

## Structured Output Format

Consistency across modes makes results comparable and actionable.

### Finding Format (all modes)

Every individual finding follows this structure:

```
[SEVERITY] [CATEGORY] — [one-line problem statement]
  Element: [CSS selector or screenshot region description]
  Current: [what it is now, with measured values]
  Target: [what it should be, with specific values]
  Fix: [concrete CSS/HTML change]
  Criteria: [which design-criteria.md section this violates]
```

Severity: `CRITICAL` / `MAJOR` / `MINOR` / `SUGGESTION`
Category: `typography` / `color` / `spacing` / `layout` / `a11y` / `performance` / `interaction` / `hierarchy`

### Score Table (scan, audit, fix, compare modes)

```
DESIGN SCORE
───────────────────────────────
Technical (8 dimensions, weighted)
  Visual Structure    [0-10]
  Typography          [0-10]   ×1.5
  Color & Contrast    [0-10]   ×1.2
  Spacing & Grid      [0-10]
  Hierarchy           [0-10]
  Accessibility       [0-10]   ×2.0
  Performance         [0-10]   ×0.8
───────────────────────────────
  Technical Total     [0-100]  Grade: [A-F]

Aesthetic (7 dimensions, from Step 1.5)
  Depth · Rhythm · Palette · Craft
  Originality · Resonance · Coherence
───────────────────────────────
  Aesthetic Total     [1-10]   [⚠ if < 6]
───────────────────────────────

Grade Cap: ANY critical finding → maximum grade C regardless of score
Divergence: Technical > 75 AND Aesthetic < 6 → flag explicitly
```

The grade cap prevents a site from scoring 88/100 (A) when it has a critical accessibility failure. One critical = max C.

### Mode-Specific Additions

- **scan**: Score table + top 5 findings sorted by severity
- **audit**: Score table + ALL findings grouped by category + per-agent breakdown
- **fix**: Score table BEFORE + AFTER + visual diff summary + iteration count
- **clone**: `clone_report` status + visual diff score + section-by-section completeness
- **heal**: Per-iteration score progression + convergence report (did issues decrease each cycle?)
- **dev**: Delta from baseline only (no full score — speed matters in dev mode)
- **compare**: Side-by-side score table for both sites + dimension-by-dimension winner
- **perf**: Web Vitals table with Good/Needs Work/Poor ratings + opportunities ranked by impact
- **a11y-axe**: Violations by impact + WCAG success criteria + remediation priority

