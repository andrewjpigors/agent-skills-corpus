---
name: ux-behavior-spec
description: UX behavioral rules for all interactive components. REQUIRED READING before building modals, forms, action groups, buttons, notifications, loading states, or any interactive element. Covers destructive actions, consistency enforcement, feedback patterns, validation, responsive behavior, keyboard accessibility, and more. 18 sections.
allowed-tools: Read, Glob, Grep
---

# UX Behavior Specification

> **The rules layer for Fluid Theme projects.**
> Components define *what* things look like. This spec defines *when*, *how*, and *why* they behave.

**Version:** 0.2.0
**Status:** Living document — grows with each project
**Last Audited Against:** Fluid Theme v0.3.2 (Phase 3 Complete)
**Repo Location:** `_docs/UX-BEHAVIOR-SPEC.md`

---

## Selective Reading Guide

**You do NOT need to read all 18 sections for every task.** Read only what's relevant:

| Your Task | Read These Sections |
|-----------|-------------------|
| Building a modal or confirmation dialog | §1, §3, §12 |
| Building a form | §5, §9, §12 |
| Adding action buttons (edit, delete, etc.) | §1, §2, §9 |
| Writing button labels, error messages, CTAs | §9, §16 |
| Building a table with actions | §2, §13, §11 |
| Adding search or filters | §14, §7 |
| Building notifications/toasts/alerts | §4 |
| Building loading states | §10 |
| Checking responsive behavior | §11 |
| Keyboard/accessibility review | §12 |
| Starting a new project | §17 (full checklist), then sections as needed |
| Running a UX audit | Read the full spec |
| Onboarding flow | §15, §7 |
| Subscription/email flow | §6 |

---

## How to Use This Spec

**For AI agents:** This document is your source of truth for UX decisions. Read it before implementing any interactive component. If a pattern isn't covered here, **flag it as a gap — don't improvise.** This file lives alongside the agent docs in `_docs/_agents/` and supplements them. The agent docs cover *code conventions*; this spec covers *behavior conventions*.

**For humans:** This codifies decisions you'd otherwise explain every time. When an agent produces something that violates these rules, point them here instead of re-explaining.

**For any framework:** Each section describes the *behavior* first (framework-agnostic), then provides the Fluid Theme implementation. When working in Tailwind or another system, follow the behavior rules and adapt the markup.

**Relationship to Fluid Theme docs:**
- `_docs/DEVELOPMENT.md` → Why we build this way (philosophy)
- `_docs/reference/components.md` → Component APIs (what exists)
- `_docs/reference/tokens.md` → Design tokens (visual values)
- **This file** → When and how to use those components (behavioral rules)

---

## Table of Contents

1. [Destructive Actions & Confirmations](#1-destructive-actions--confirmations)
2. [Action Groups & Consistency](#2-action-groups--consistency)
3. [Modal Strategy — When to Interrupt](#3-modal-strategy--when-to-interrupt)
4. [Notification & Feedback](#4-notification--feedback)
5. [Form Flows & Validation](#5-form-flows--validation)
6. [Email & Subscription Flows](#6-email--subscription-flows)
7. [Error Pages & Empty States](#7-error-pages--empty-states)
8. [Navigation & Wayfinding](#8-navigation--wayfinding)
9. [Button & Label Messaging](#9-button--label-messaging)
10. [Loading & Progress States](#10-loading--progress-states)
11. [Responsive Behavior Rules](#11-responsive-behavior-rules)
12. [Keyboard & Accessibility Interactions](#12-keyboard--accessibility-interactions)
13. [Data Tables with Actions](#13-data-tables-with-actions)
14. [Search, Filter & Sort](#14-search-filter--sort)
15. [Onboarding & First-Run](#15-onboarding--first-run)
16. [CTAs & Conversion Patterns](#16-ctas--conversion-patterns)
17. [Page Templates & Required Flows](#17-page-templates--required-flows)
18. [Framework Gap Tracker](#18-framework-gap-tracker)

---

## 1. Destructive Actions & Confirmations

### The Rule

**Every destructive action requires explicit confirmation with clear, specific language.** No exceptions. No single-word buttons. No ambiguous messaging.

### What Counts as Destructive

- Deleting any user-created content (items, records, accounts, brands, files)
- Removing team members or revoking access
- Canceling subscriptions or plans
- Clearing or resetting data, caches, or preferences
- Any action that cannot be undone or would require significant effort to reverse

### Confirmation Modal Requirements

**Title:** State what will happen. Use the specific name of the thing being destroyed. Never a vague question.

```
✗  "Are you sure?"
✗  "Confirm deletion"
✗  "Delete?"
✓  "Delete 'Sunrise Collection' brand"
✓  "Remove Alex from the design team"
✓  "Cancel your Pro subscription"
```

**Body text:** Explain the consequence. What will the user lose? Be specific about scope and permanence.

```
✗  "This action cannot be undone."

✓  "This will permanently delete the 'Sunrise Collection' brand, including
    all 47 associated products, 12 saved color palettes, and the published
    style guide. This cannot be undone."
```

**Button labels:** The confirm button states the exact action. The cancel button is always "Cancel" or "Keep [thing]". Never use "OK", "No", "Yes", or "Confirm" for destructive actions.

```
✗  [Cancel] [OK]
✗  [No] [Yes]
✗  [Go Back] [Continue]
✓  [Cancel] [Delete Brand]
✓  [Keep Subscription] [Cancel Subscription]
✓  [Go Back] [Remove Alex]
```

**Button layout and styling:**
- Destructive button uses the danger variant: `<button data-variant="danger">Delete Brand</button>`
- Cancel button uses ghost variant: `<button data-variant="ghost">Cancel</button>`
- Buttons are separated by generous spacing — minimum `var(--space-5)` gap in the footer. **Note:** Fluid Theme's `.modal__footer` defaults to `gap: var(--space-3)`. Override with inline style or a modifier class on destructive confirmation modals.
- On mobile, buttons stack full-width with the safe action (Cancel) on top
- The destructive button **never** receives default focus. Add `autofocus` to the Cancel button — without it, native `<dialog>` focuses the first focusable element (the × close button), not Cancel.
- The modal footer uses `justify-content: flex-end` with the safe option first (left) and destructive option last (right)

### Severity Tiers

| Tier | Examples | Confirmation |
|------|----------|-------------|
| **Low** | Delete a single draft, remove a tag | Simple modal with clear messaging |
| **Medium** | Delete a published item, remove a team member | Modal with consequence summary (item count, scope) |
| **High** | Delete an account, bulk delete, clear all data | Modal + type-to-confirm input |
| **Critical** | Delete entire organization, purge all records | Modal + type-to-confirm + 5-second cooldown before button activates |

### Fluid Theme Implementation

Use `modal[data-size="sm"]` for confirmation dialogs. The modal component (`src/components/modal.css`) provides the structure. Button variants (`src/components/button.css`) provide danger styling.

```html
<dialog class="modal" data-size="sm">
  <div class="modal__content">
    <header class="modal__header">
      <h2 class="modal__title">Delete 'Sunrise Collection' brand</h2>
      <button class="modal__close" aria-label="Close">&times;</button>
    </header>
    <div class="modal__body">
      <p>This will permanently delete the brand, including all 47 products,
         12 color palettes, and the published style guide.</p>
      <p><strong>This cannot be undone.</strong></p>
    </div>
    <footer class="modal__footer" style="gap: var(--space-5);">
      <button data-variant="ghost" autofocus>Cancel</button>
      <button data-variant="danger">Delete Brand</button>
    </footer>
  </div>
</dialog>
```

For **high-severity** confirmations, add a type-to-confirm input in the body:

```html
<div class="modal__body">
  <p>This will permanently delete your entire account and all associated data.</p>
  <div class="form-group" style="margin-block-start: var(--space-5);">
    <label class="form-label" for="confirm-delete">
      Type <strong>delete my account</strong> to confirm:
    </label>
    <input type="text" id="confirm-delete" autocomplete="off"
           placeholder="delete my account">
  </div>
</div>
```

The danger button stays `disabled` until the input matches exactly.

---

## 2. Action Groups & Consistency

### The Rule

**Actions that apply to the same item must be a unified group with consistent presentation across every screen.** When an agent implements an action group on one screen, it must search the entire project for the same pattern and apply it identically.

### Display Modes

Action groups support multiple display modes. The mode is chosen based on available space and context — **not randomly per page.** Once a mode is chosen for a context type, it applies everywhere in that context.

| Mode | When to Use | Fluid Theme Markup |
|------|-------------|-------------------|
| **Icon only** | Table rows, card corners, mobile tight spaces | `<button data-icon aria-label="Edit">✏️</button>` |
| **Text only** | When icons would be ambiguous | `<button data-variant="ghost" data-size="sm">Edit</button>` |
| **Icon + text** | Default for most cases — clearest | `<button data-variant="ghost" data-size="sm">✏️ Edit</button>` |
| **Stacked** | Vertical menus, mobile drawers, sidebar actions | Vertically arranged buttons |
| **Horizontal** | Toolbars, card footers, inline actions | `<div class="button-group">...</div>` |
| **Overflow menu** | When 3+ secondary actions exist | Primary visible, rest in `.dropdown` with `⋮` trigger |

### Hierarchy Within Groups

1. **Primary action** — most common user intent. Gets visual weight (default button variant).
2. **Secondary actions** — useful but not the main path. Ghost or secondary variant.
3. **Destructive actions** — always last in visual order, always danger variant, always separated from other actions by extra space or a `.dropdown__divider`.

```
✓  [Save Changes]  [Preview]  [Duplicate]  |  [Delete]
   Primary          Secondary  Secondary    Divider  Destructive
```

In dropdown menus, the Fluid Theme dropdown component already supports `data-danger` on items:

```html
<div class="dropdown">
  <button class="dropdown__trigger">Actions ▾</button>
  <div class="dropdown__menu">
    <a href="#" class="dropdown__item">Edit</a>
    <a href="#" class="dropdown__item">Duplicate</a>
    <div class="dropdown__divider"></div>
    <a href="#" class="dropdown__item" data-danger>Delete</a>
  </div>
</div>
```

### Consistency Enforcement (Agent Rule)

When implementing action groups, agents MUST:

1. **Search the entire project** for similar action patterns before implementing
2. **Use the same display mode** for the same context type (all table rows match, all card footers match, all detail page headers match)
3. **Use the same action order** everywhere (e.g., Edit → Duplicate → Archive → Delete)
4. **Never introduce a new action** on one screen that exists as a different pattern elsewhere
5. **After implementing on one screen,** proactively find and update all other instances to match
6. **Document the chosen mode** at the top of the first file where it appears, as a comment:
   ```html
   <!-- Action pattern: icon+text horizontal, danger last with divider -->
   ```

---

## 3. Modal Strategy — When to Interrupt

### The Rule

**Use the minimum interruption necessary.** Modals break flow. Reserve them for moments that genuinely need the user's full attention.

### Decision Matrix

| Situation | Use This | Fluid Theme Component | Why |
|-----------|----------|----------------------|-----|
| Destructive confirmation | **Modal** (centered, sm) | `modal[data-size="sm"]` | Must demand attention |
| Success after action | **Toast** (auto-dismiss) | `toast[data-status="success"]` | Non-blocking |
| Error on form submit | **Inline alert** | `alert[data-status="error"]` | Keeps context |
| Warning about consequences | **Inline alert** | `alert[data-status="warning"]` | Contextual |
| Complex sub-task (new address, payment) | **Modal** (centered, lg) | `modal[data-size="lg"]` | Focused task-in-task |
| Quick settings change | **Drawer** (right) | `modal[data-variant="drawer-right"]` | Non-blocking panel |
| Mobile navigation | **Drawer** (left) | `modal[data-variant="drawer-left"]` | Native pattern |
| Brief hint or explanation | **Tooltip** | `[data-tooltip="..."]` | CSS-only, non-blocking |
| Rich contextual info | **Popover** | `[popover]` with `.popover` | Richer than tooltip |
| Critical system warning | **Modal** (no dismiss) | `modal` (no backdrop handler, cancel event prevented) | Must acknowledge |
| Feature explanation (first time) | **Tooltip or popover** | `[data-tooltip]` / `.popover` | Contextual, temporary |

### Modal Behavior Rules

- **Backdrop click** — native `<dialog>` does NOT dismiss on backdrop click by default. You must add a JS click handler on the `<dialog>` element that calls `.close()` when the click target is the dialog itself (not `.modal__content`). For critical modals that must be acknowledged, simply don't add this handler.
- **Escape key** — native `<dialog>` closes on Escape by default. For critical modals (system warnings, required acknowledgments), prevent this: `dialog.addEventListener('cancel', e => e.preventDefault())`.
- **Focus trapping** — native `<dialog>` opened via `.showModal()` provides focus trapping automatically. Do NOT add manual focus-trap JS on top of this — it will cause double-trapping bugs.
- **Return focus** to the trigger element on close
- **No nested modals** — if a modal needs a sub-action, use inline content within the same modal or a step/tab pattern inside it. Never open a modal from a modal.
- **Mobile:** All centered modals become bottom sheets below 40rem (Fluid Theme does this automatically in `modal.css` responsive section)
- **Scroll lock** on `<body>` while modal is open
- **Animation:** Entry animation respects the active motion preset. `[data-preset="still"]` disables all transitions. `prefers-reduced-motion: reduce` uses instant open/close.

---

## 4. Notification & Feedback

### The Rule

**Every user action gets feedback.** The type and intensity matches the significance of the action. Silence after an action is a bug.

### Feedback Matrix

| Action | Feedback Type | Component | Duration | Dismissible? |
|--------|---------------|-----------|----------|--------------|
| Save successful | Toast (success) | `toast[data-status="success"]` | 4s | Yes |
| Item created | Toast + redirect or inline update | `toast[data-status="success"]` | 4s | Yes |
| Item deleted | Toast with **undo** option | `toast[data-status="success"]` | 8s | Yes |
| Form validation error | Inline alert + field highlights | `alert[data-status="error"]` + `.form-error` | Persistent | No (until fixed) |
| Network error | Inline alert at top of page | `alert[data-status="error"]` | Persistent | Yes (with retry) |
| Background process started | Toast (info) | `toast[data-status="info"]` | 3s | Yes |
| Background process complete | Toast (success) | `toast[data-status="success"]` | 5s | Yes |
| Permission denied | Inline alert (warning) | `alert[data-status="warning"]` | Persistent | Yes |
| Rate limited | Inline alert with countdown | `alert[data-status="warning"]` | Until cooldown | No |

### Toast Rules

- **Position:** Top-right desktop, top-center mobile (use `toast-container[data-position="top-right"]`)
- **Stacking:** New toasts below existing, max 3 visible at once
- **Auto-dismiss:** Pause timer on hover (user is reading it)
- **Content:** One sentence max. Include the name of the thing acted on.

### Undo Pattern

For reversible destructive actions, the toast includes an undo link. The deletion is a **soft delete** during the toast window — it doesn't commit to the backend until the undo period expires.

```
"'Sunrise Collection' deleted."  [Undo]
 └─ Undo available for 8 seconds
 └─ Clicking Undo restores and shows: "'Sunrise Collection' restored."
```

### Alert Variants (Fluid Theme)

The `alert` component supports three visual treatments via `data-variant`:
- **subtle** (default) — tinted background, colored left border
- **filled** — solid color background
- **outline** — transparent background, colored border

Use **subtle** for most inline feedback. Use **filled** for critical or unmissable alerts. Use **outline** for less urgent informational messages.

Statuses: `data-status="info|success|warning|error"` — maps to `--color-info`, `--color-success`, `--color-warning`, `--color-error` tokens.

---

## 5. Form Flows & Validation

### The Rule

**Forms are conversations, not interrogations.** Validate inline, show progress, never lose user data.

### Validation Timing

| Event | Behavior |
|-------|----------|
| First interaction with field → blur | Validate on blur. Show error if invalid. |
| After error is shown → typing | Re-validate on each keystroke to clear error instantly when valid. |
| Form submit | Validate all fields. Scroll to first error. Focus it. |
| Required field left empty | Show error on blur only, not while typing. |
| Field with format requirements | Show hint text (`.form-help`) below the field before the user starts. Show error (`.form-error`) only after they've attempted input. |

### Error Display (Fluid Theme)

Fluid Theme's form component (`src/components/form.css`) provides:

```html
<!-- Error state — aria-invalid and aria-describedby are added dynamically
     by JS when validation fails. Do NOT include them in default markup. -->
<div class="form-group">
  <label class="form-label" data-required>Email Address</label>
  <input type="email" aria-invalid="true" aria-describedby="email-error">
  <span class="form-error" id="email-error">Email must include an @ symbol</span>
</div>
```

Rules for error messages:
- **Specific:** "Email must include an @ symbol" — not "Invalid input"
- **Actionable:** Tell them what to do, not just what's wrong
- **Visible:** Error text uses `--color-error`, appears directly below the field
- **Accessible:** Connected to the input via `aria-describedby`

When more than 2 errors exist on submit, show an error summary alert above the form:

```html
<div class="alert" data-status="error" data-variant="subtle">
  <div class="alert__content">
    <strong class="alert__title">Please fix 3 errors below</strong>
    <p>Required fields are highlighted.</p>
  </div>
</div>
```

### Multi-Step Forms

- Show a **progress indicator** — step labels, progress bar, or "Step 2 of 4"
- Each step validates before allowing progression
- **Back button never loses data** — form state persists across steps
- Complex forms (5+ fields or 2+ steps) offer **save as draft**
- Final step shows a **review/summary** before submission
- Submit button text reflects the specific action: "Create Account", "Place Order" — never just "Submit"

Fluid Theme: Use the `indicator` progress component (`src/components/indicator.css`) for step progress bars.

### Form Submission States

```
[Idle] → [Submitting] → [Success] or [Error]
```

- **Submitting:** Button disabled, text replaced with spinner + verb ("Saving...")
  Use `<button data-loading>Saving...</button>` — the loading component provides the spinner.
- **Success:** Redirect to next page, OR show inline success + reset form for simple cases.
- **Error:** Show inline `alert[data-status="error"]` above or below the form. Re-enable the form. **Never reload the page on error.**
- **Double-submit prevention:** Disable button on first click. Re-enable only on error.

---

## 6. Email & Subscription Flows

### The Rule

**Every subscription flow starts from the full template and trims down — never the reverse.** It's easier to remove optional steps than to discover you need them after launch.

### Full Flow (Default Template)

```
1. SIGNUP FORM
   ├─ Email field (required) + optional name
   ├─ Clear value proposition above the form: "What you'll get"
   └─ Submit: "Subscribe" or "Get [Specific Thing]" — never just "Submit"

2. PREFERENCE SELECTION (inline expansion or next step)
   ├─ Topics/categories (checkboxes — Fluid: .checkbox component)
   ├─ Frequency: Daily / Weekly / Monthly (radio group — Fluid: .radio component)
   ├─ "Select All" and "Select None" convenience options
   └─ Defaults: most popular selections pre-checked

3. CONFIRMATION STATE (dynamic, no page reload)
   ├─ Success message with specifics: "You'll receive weekly updates about [topics]"
   ├─ "Check your email to confirm" (if double opt-in)
   └─ Link to manage preferences

4. CONFIRMATION EMAIL
   ├─ Clear subject: "Confirm your subscription to [Site]"
   ├─ One-click confirm button (large, prominent)
   ├─ Summary of selections
   └─ Unsubscribe link (even before first email — required by law)
```

### Simplified Flow (for simple projects)

When the project is a single-topic list:
```
1. Email + submit
2. Inline success: "You're subscribed! Check your email to confirm."
3. Confirmation email
```

The key: **document which version of the flow you're using** in the project's admin file.

### Unsubscribe Flow

- **One-click unsubscribe from email** (legally required, CAN-SPAM / GDPR)
- Unsubscribe landing page offers: pause (1 week / 1 month), reduce frequency, change topics, or full unsubscribe
- Confirmation: "You've been unsubscribed. You won't receive any more emails." with re-subscribe option
- **Never require login to unsubscribe**

---

## 7. Error Pages & Empty States

### The Rule

**Errors and empty states are design opportunities.** Every one should help the user take a next step. Never a dead end.

### Error Pages

**404 — Not Found:**
Fluid Theme provides `templates/404.html`. Behavioral requirements:

- Friendly, on-brand messaging (can be playful if brand allows)
- Acknowledge clearly: "We couldn't find that page"
- Provide escape routes: link to homepage, search bar, links to popular sections
- If technically possible, suggest similar content
- Never show just "404" with no context

**500 — Server Error:**
- Honest: "Something went wrong on our end"
- Reassuring: "Your data is safe" (if applicable)
- Actionable: Retry button + link to status page
- Suggest trying again in a few minutes

**403 — Forbidden:**
- Explain why: "You don't have permission to view this"
- If auth helps: "Log in to view this page"
- If truly forbidden: "Contact [admin/support] for access"

### Empty States

Empty states appear when a list, dashboard, or content area has no items yet. They are the user's first impression of a feature.

**Required elements:**
1. An illustration or icon (optional but strongly recommended)
2. A clear explanation of what will appear here
3. A primary action CTA: "Create your first [thing]"
4. Optional: secondary link to learn more

```
✗  "No items found."

✓  "No brands yet"
    "Create your first brand to start building your design system."
    [+ Create Brand]
```

**Search/filter empty states** mean the query returned nothing:

```
✓  "No results for 'sunset palette'"
    "Try adjusting your search or clearing filters."
    [Clear Filters]
```

### Offline State

- Detect offline and show a persistent banner: `alert[data-status="warning"]` at top of page
- Queue actions where possible: "Your changes will sync when you reconnect."
- Disable actions requiring connectivity; add `data-tooltip="You're offline"` to explain

---

## 8. Navigation & Wayfinding

### The Rule

**The user should always know where they are, where they can go, and how to get back.**

### Breadcrumbs

- Required on any page more than 2 levels deep
- Format: `Home > Section > Current Page` — current page is plain text, not a link
- Mobile: collapse to `← Back to [Parent]`

### Active States

- Current nav item always visually distinct — Fluid Theme uses `aria-current="page"` which the nav CSS styles automatically
- Page title in `<title>` tag and in a visible page heading

### Navigation Patterns

| Context | Desktop | Mobile |
|---------|---------|--------|
| Primary site nav | Horizontal bar (`.nav`) | Hamburger → left drawer (`modal[data-variant="drawer-left"]`) |
| Sub-section nav | Horizontal tabs (`.nav__tabs`) | Scrollable tabs with fade hint |
| Settings/preferences | Sidebar nav | Stacked list or accordion |
| Multi-step process | Step indicator (labeled) | Step indicator (compact) |
| Content pagination | Numbered pages + Prev/Next (`.nav__pagination`) | Same, condensed |
| Back to parent | Breadcrumbs | `← Back to [Parent]` link |

### Mobile Navigation Rules

- Hamburger opens a left drawer with full nav
- Drawer overlays content (does not push)
- Close on: nav item selection, backdrop click, Escape, X button
- Fluid Theme handles mobile bottom-sheet conversion automatically for centered modals

---

## 9. Button & Label Messaging

### The Rule

**Clarity over brevity.** Every button tells the user exactly what will happen. A few extra words always beat confusion.

### Label Patterns

| Avoid | Prefer | Why |
|-------|--------|-----|
| Submit | Create Account, Place Order, Send Message | Specificity |
| OK | Got It, Continue, Understood | Context |
| Yes / No | [Specific action] / Cancel | Clarity |
| Click Here | [Description of destination] | Accessibility |
| Confirm | [Restate the action] | Removes ambiguity |
| Delete | Delete [specific thing] | Safety |
| Save | Save Changes, Save Draft, Save and Continue | Expectation setting |

### Button Hierarchy (Fluid Theme Variants)

| Role | Variant | Usage |
|------|---------|-------|
| Primary action | Default (no `data-variant`) | One per visible area — the main thing to do |
| Secondary action | `data-variant="secondary"` or `"outline"` | Useful but not the main path |
| Tertiary action | `data-variant="ghost"` | Least important, low visual weight |
| Destructive action | `data-variant="danger"` | Always last, always separated |

**Sizing:** Use `data-size="sm"` in tight spaces (table rows, card footers). Default size for standalone actions. `data-size="lg"` for hero CTAs and primary conversion points.

### Link Text Accessibility

- Never "click here" or bare "learn more" as complete link text
- Links must make sense read in isolation (screen readers list all links)
- Prefer: "Read our accessibility guidelines" over "Click here to learn more"

---

## 10. Loading & Progress States

### The Rule

**Never leave the user staring at nothing.** 300ms is the threshold. Beyond that, show something.

### Loading Strategy

| Duration | Response | Fluid Theme Component |
|----------|----------|----------------------|
| < 300ms | Nothing | — |
| 300ms – 2s | Spinner or skeleton | `.spinner` or `.skeleton` |
| 2s – 10s | Progress bar or skeleton + text | `.progress` with `.progress__track` |
| > 10s | Progress + estimated time | `.progress` with percentage |
| Indeterminate | Skeleton + updating status text | `.skeleton-card` pattern |

### Skeleton vs. Spinner

- **Skeleton screens** (`.skeleton`, `.skeleton-card`) — for pages/sections loading content. Grey placeholder shapes matching expected layout.
- **Spinners** (`.spinner`) — for discrete actions: button click, form submit, item saving.
- **Progress bars** (`.progress`) — for measurable processes: file uploads, multi-step operations.
- **Dots** (`.spinner-dots`) — for inline "typing" or "processing" indicators.

Never use a spinner for initial page load. Always use skeletons.

### Button Loading State

```html
<!-- Idle -->
<button>Save Changes</button>

<!-- Loading -->
<button data-loading disabled>Saving...</button>

<!-- Success flash (1 second, then return to idle) -->
<button data-variant="secondary" disabled>✓ Saved</button>
```

Fluid Theme's `button[data-loading]` adds a spinner automatically. The loading component (`src/components/loading.css`) provides spinner variants and sizes (`data-size="xs|sm|lg|xl"`).

### Reduced Motion

Fluid Theme respects `prefers-reduced-motion: reduce` throughout. Spinners become pulse animations. Skeletons use opacity fades instead of sweeping gradients. No additional per-project work needed.

---

## 11. Responsive Behavior Rules

### The Rule

**Mobile isn't a shrunk desktop.** Interactions change, not just sizes. Every component has a defined mobile behavior.

### Component Transformations

| Component | Desktop | Mobile (< 40rem) |
|-----------|---------|-------------------|
| Modal (centered) | Centered overlay | Bottom sheet (slides up) — automatic in Fluid |
| Modal (drawer) | Side panel | Bottom sheet — automatic in Fluid |
| Navigation | Horizontal `.nav` | Hamburger → left drawer |
| Action group (icon+text) | Horizontal, full labels | Icon-only or overflow `.dropdown` |
| Data table | Full table in `.table-wrap` (scroll) | `.table[data-responsive]` stacks rows, uses `td[data-label]` for headers |
| Tabs | Horizontal, all visible | Horizontal scroll with overflow hint |
| Tooltip | On hover/focus | On tap (toggle) |
| Multi-select | Checkbox list | Expandable accordion or drawer |

### Touch Targets

- Minimum: 44×44px (Apple HIG / WCAG 2.5.5 AAA). WCAG 2.2 Level AA minimum is 24×24px, but 44px is our standard.
- Spacing between targets: minimum 8px
- Destructive buttons on mobile: larger targets + more spacing

### Gestures

- Swipe-to-dismiss on toasts and bottom sheets
- Pull-to-refresh only if explicitly enabled (never default)
- No swipe-to-delete without an undo path (see Section 1)

---

## 12. Keyboard & Accessibility Interactions

### The Rule

**Every interaction that works with a mouse must work with a keyboard.** Focus states must be visible. ARIA roles must be correct.

### Global Keyboard Rules

| Key | Behavior |
|-----|----------|
| `Tab` | Move focus to next interactive element |
| `Shift+Tab` | Move focus to previous interactive element |
| `Escape` | Close the topmost overlay (modal, dropdown, popover, drawer) |
| `Enter` / `Space` | Activate focused button, link, or toggle |
| `Arrow keys` | Navigate within grouped controls (tabs, radio groups, dropdown items) |

### Component-Specific Keyboard

| Component | Keyboard Support |
|-----------|-----------------|
| **Modal** | `Escape` closes (prevent via `cancel` event for critical modals). Focus trapping is automatic via `.showModal()` — do not add manual trap. Return focus to trigger on close. |
| **Dropdown** | `Enter`/`Space` opens. `Arrow ↓↑` navigates items. `Enter` selects. `Escape` closes. |
| **Tabs** | `Arrow ←→` switches tabs. `Home` → first tab. `End` → last tab. |
| **Accordion** | `Enter`/`Space` toggles. Native `<details>` handles basics. |
| **Tooltip** | Shows on `:focus-visible` — Fluid Theme CSS handles this. |
| **Toast** | Auto-dismiss pauses on focus. Dismiss with `Escape`. |

### Focus Visibility

Fluid Theme uses `:focus-visible` throughout — shows focus rings for keyboard but hides them for mouse clicks. **Never remove focus outlines.** If the default ring doesn't suit the design, restyle it — don't delete it.

```css
/* NEVER DO THIS: */
:focus { outline: none; }
```

### ARIA Patterns

- Modals: `<dialog>` element handles roles natively
- Accordions: `<details>/<summary>` handles natively
- Buttons with icons only: always include `aria-label`
- Current nav item: `aria-current="page"`
- Form errors: connected via `aria-describedby`
- Loading states: `aria-busy="true"` on the container, `aria-live="polite"` on status messages
- Required fields: `aria-required="true"` or HTML `required` attribute

---

## 13. Data Tables with Actions

### The Rule

**Tables with row-level actions follow the Action Group rules (Section 2) and must be consistent across every table in the project.**

### Row Action Patterns

| Table Context | Action Display | Markup |
|---------------|---------------|--------|
| Simple list (< 3 actions) | Icon buttons in last column | `<button data-icon data-size="sm" aria-label="Edit">` |
| Complex list (3+ actions) | Primary icon + overflow dropdown | Icon button + `.dropdown` with `⋮` trigger |
| Bulk operations | Checkbox column + toolbar above table | Checkbox + sticky action bar |

### Responsive Table Behavior

Fluid Theme's table component (`src/components/table.css`) requires a `.table-wrap` div around the `.table` for horizontal scroll overflow. For mobile stacking, add `data-responsive` to the `.table` element and `data-label="Column Name"` on each `<td>` — these labels replace the hidden `<thead>` on mobile.

For complex tables with row actions on mobile, consider whether the stacked layout preserves the action pattern. If not, switch to a card-based list view.

### Bulk Actions

- "Select All" checkbox in header selects visible items only (not all pages)
- Show selected count: "3 items selected"
- Bulk actions appear in a toolbar above the table
- Destructive bulk actions follow Section 1 (confirmation modal with count: "Delete 3 items?")
- Deselect all on successful action

### Sorting

- Clickable column headers toggle: unsorted → ascending → descending → unsorted
- Active sort column visually indicated (arrow icon + subtle background)
- Only one column sorts at a time unless the project explicitly requires multi-sort

---

## 14. Search, Filter & Sort

### The Rule

**Search should feel instant. Filters should be visible and clearable. The user should always know what's filtering their view.**

### Search Behavior

- **Debounce** input: 300ms delay before firing search
- **Result count:** "47 results" or "No results for 'sunset palette'"
- **Clear button** (✕) inside the search input when it has a value
- **Empty state:** "No results" message + adjust query suggestion + [Clear] button (Section 7)
- **Recent searches** (optional): dropdown below input showing last 5 searches

### Filter Behavior

- **Active filters visible:** Show as removable chips/badges above results: `[Color: Blue ✕] [Status: Active ✕]`
- **"Clear All Filters"** link when any filter is active
- **Filter count on mobile:** If filters are in a drawer, show count on trigger: "Filters (3)"
- **URL persistence:** Filters reflected in URL params so filtered views are shareable and bookmarkable

### Combined Pattern

```
[🔍 Search...                    ]
[Color: Blue ✕] [Status: Active ✕]  Clear All Filters
──────────────────────────────────
47 results
[Results list...]
```

---

## 15. Onboarding & First-Run

### The Rule

**First impressions define retention.** Orient the user and lead them to their first meaningful action — don't overwhelm them.

### Patterns

| Approach | When to Use |
|----------|-------------|
| **Empty state CTA** | Simple apps — the empty dashboard IS the onboarding |
| **Inline tooltips/popovers** | Highlighting 2-3 key features on first visit |
| **Step-by-step walkthrough** | Complex apps with many features |
| **Welcome modal** | Simple intro + "Get Started" CTA — max one, keep brief |

### Rules

- **One action at a time.** Don't show 10 tooltips simultaneously.
- **Dismissible.** Every onboarding element can be skipped.
- **Don't repeat.** Track "has seen onboarding" state.
- **Progress indicator** for multi-step: "Step 2 of 4"
- **Lead to a first win.** Onboarding ends with the user having created or accomplished something real.

---

## 16. CTAs & Conversion Patterns

### The Rule

**Every page has a purpose. The CTA makes that purpose actionable.** One primary CTA per viewport. Supporting CTAs are visually secondary.

### CTA Hierarchy

| Position | Type | Fluid Theme |
|----------|------|-------------|
| Hero section | Primary conversion | `<button data-size="lg">` or `data-size="xl"` |
| Inline in content | Contextual action | Default button or `data-variant="outline"` |
| Sticky mobile bar | Mobile conversion | Fixed bottom bar (see `FLUID-THEME-GAPS.md` Gap 3) |
| End of page | Closing conversion | Secondary hero section with CTA |

### CTA Copy Rules

- Verb-first: "Start Your Free Trial", "Get the Guide", "Create Your Account"
- Specific benefit: "Save 20% Today" over "Sign Up"
- Never "Click Here" or bare "Learn More" as primary CTA
- Supporting text under CTA: "No credit card required" / "Free for 14 days"

### Pricing Page CTAs

- Each tier gets one CTA
- Featured tier: default filled button. Other tiers: `data-variant="outline"` or `"secondary"`
- CTA text varies: "Get Started", "Go Pro", "Contact Sales"
- Fluid Theme pricing card: `card[data-type="pricing"][data-featured]`

---

## 17. Page Templates & Required Flows

### The Rule

**Every project starts from a known set of pages and flows.** Include everything; trim what you don't need.

### Standard Page Checklist

Mark each as "included", "not needed", or "deferred" per project.

**Core Pages:**
- [ ] Homepage / Landing
- [ ] About
- [ ] Contact (with form — follow Section 5)
- [ ] 404 Error (follow Section 7) — Fluid Theme: `templates/404.html`
- [ ] 500 Error (follow Section 7)
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Cookie Consent (banner or modal)

**Content Pages:**
- [ ] Blog / News index — Fluid Theme: `templates/blog.html`
- [ ] Blog / News detail
- [ ] Category / Tag listing
- [ ] Search results (with empty state — Section 7)

**Commerce Pages:**
- [ ] Product / Service listing — Fluid Theme: `templates/services.html`
- [ ] Product / Service detail
- [ ] Pricing / Plans — Fluid Theme: `templates/pricing.html`
- [ ] Cart
- [ ] Checkout (multi-step — Section 5)
- [ ] Order confirmation

**Account Pages:**
- [ ] Login
- [ ] Registration
- [ ] Forgot password → Reset flow
- [ ] Account settings / Profile
- [ ] Subscription management (Section 6)
- [ ] Notification preferences

**App Pages:**
- [ ] Dashboard (with empty state — Section 7)
- [ ] Detail / Edit view
- [ ] List / Grid view with search & filter (Section 14)
- [ ] Settings (sidebar nav)
- [ ] Onboarding / First-run (Section 15)

### Fluid Theme Templates Currently Available

`404.html`, `about.html`, `blog.html`, `contact.html`, `faq.html`, `gallery.html`, `index.html`, `pricing.html`, `services.html`

### Required Flows to Document Per Project

Even if simple, define these in the project admin doc:

1. **Authentication:** Login → Where do they land?
2. **Error recovery:** Error → What can the user do next?
3. **Subscription:** Signup → Preferences → Confirmation (Section 6)
4. **Destructive action:** Trigger → Confirm → Feedback (Section 1)
5. **Form submission:** Fill → Validate → Submit → Success/Error (Section 5)
6. **Search:** Query → Results → Empty state (Section 14 + 7)
7. **Onboarding:** First visit → First action → Success (Section 15)
8. **Checkout** (if applicable): Cart → Details → Payment → Confirmation

---

## 18. Framework Gap Tracker

Components or patterns this spec requires that **Fluid Theme doesn't yet provide.** Track these so projects know what to build in-house and what to backport.

### Existing Gaps (from `FLUID-THEME-GAPS.md`)

| Gap | Status | Notes |
|-----|--------|-------|
| Badge component | ✅ Built (`src/components/badge.css`) | In repo |
| Sticky header behavior | Documented, needs JS | Use inline JS per project |
| Mobile sticky CTA bar | Proposed, not built | Critical for mobile conversion |
| Countdown timer | Proposed | Per-project, optional |
| Testimonial card | `card[data-type="testimonial"]` | Verify in components.html |
| Social proof bar | Proposed | Low priority |
| Pricing card enhancements | `card[data-type="pricing"][data-featured]` | Verify in pricing template |

### New Gaps Identified by This Spec

| Gap | Spec Section | Priority | Description |
|-----|-------------|----------|-------------|
| **Action group component** | §2 | High | No dedicated `.action-group` with responsive mode switching. `.button-group` is close but lacks overflow/collapse behavior. |
| **Empty state component** | §7 | High | No `.empty-state` pattern with illustration slot, message, and CTA. Must be built from scratch each time. |
| **Step indicator** | §5, §15 | High | No multi-step progress (Step 1 → 2 → 3 → 4 with labels). `indicator`/`progress` provides bars but not discrete labeled steps. |
| **Search input with clear** | §14 | Medium | No styled search input with embedded ✕ clear button. |
| **Filter chip / dismissable tag** | §14 | Medium | No `.chip` component for removable filter indicators. Badge is close but lacks the dismiss (✕) pattern. |
| **Toast with action** | §4 | Medium | Toast exists but no documented pattern for embedding an undo link inside it. |
| **Breadcrumb nav** | §8 | Medium | Nav has tabs and pagination but no explicit breadcrumb variant. |
| **Destructive modal modifier** | §1 | Low | `.modal__footer` defaults to `gap: var(--space-3)`. Destructive confirmations need wider gap (`--space-5`). Currently requires inline style override. Should have a `data-destructive` or similar modifier on the dialog. |
| **Offline banner** | §7 | Low | No connectivity-aware banner. Workaround: `alert[data-status="warning"]`. |
| **Cookie consent bar** | §17 | Low | No consent banner component. Build per-project. |

### Handling Gaps During a Project

1. Check this table before starting implementation
2. **High priority:** Build the component in-project, flag for backport to Fluid Theme
3. **Medium:** Use the documented workaround
4. **Low:** Build minimal inline solution
5. After the project, contribute the new component back to the Fluid Theme repo

---

## Appendix A: Component Quick Reference

| Behavior Need | Component | Source File | Key Attributes |
|---------------|-----------|------------|----------------|
| Destructive confirm | `modal` + `button` | `modal.css`, `button.css` | `data-size="sm"`, `data-variant="danger"` |
| Success toast | `toast-container` + `toast` | `alert.css` | `data-position="top-right"`, `data-status="success"` |
| Inline error | `alert` | `alert.css` | `data-status="error"`, `data-variant="subtle"` |
| Action menu | `dropdown` | `dropdown.css` | `data-position`, `data-danger` on items |
| Form validation | `form-group` + `form-error` | `form.css` | `data-required` on label, `aria-invalid` on input |
| Settings panel | `modal` (drawer) | `modal.css` | `data-variant="drawer-right"` |
| Mobile nav | `modal` (drawer) | `modal.css` | `data-variant="drawer-left"` |
| Loading spinner | `spinner` | `loading.css` | `data-size="xs\|sm\|lg\|xl"` |
| Skeleton screen | `skeleton` | `loading.css` | `data-variant="card\|circle\|media\|title\|text"` |
| Progress bar | `progress` | `indicator.css` | `data-status="good\|moderate\|severe"` |
| Tooltip | `[data-tooltip]` | `tooltip.css` | `data-tooltip-pos="top\|bottom\|left\|right"` |
| Popover | `[popover]` + `.popover` | `tooltip.css` | Native popover API |
| Accordion | `details`/`summary` | `accordion.css` | `data-variant="bordered\|separated\|flush"` |
| Button group | `.button-group` | `button.css` | Buttons get joined borders |
| Badge | `.badge` | `badge.css` | `data-variant`, `data-status`, `data-size` |
| Data table | `.table-wrap` > `.table` | `table.css` | `data-variant="striped\|bordered\|compact"`, `data-responsive` + `td[data-label]` for mobile |
| Avatar | `.avatar` | `avatar.css` | `data-size`, status indicators, groups |

---

## Appendix B: Agent Instructions (Copy-Paste Ready)

Paste into Claude Project instructions, system prompts, or `.claude/` config to enforce these rules:

```
## UX BEHAVIOR RULES — Read _docs/UX-BEHAVIOR-SPEC.md before implementing interactive components.

1. DESTRUCTIVE ACTIONS: Confirmation modal required. Title names the item.
   Body explains consequences with specifics. Buttons: [Cancel] [Delete Thing].
   Danger button never gets focus. (Spec §1)

2. ACTION CONSISTENCY: Search entire project for similar patterns before
   implementing. Same mode, same order, same styling everywhere. After
   implementing on one screen, update ALL other matching screens. (Spec §2)

3. FEEDBACK: Every action gets feedback. Save → toast. Delete → toast with undo.
   Error → inline alert. Silent after action = bug. (Spec §4)

4. FORMS: Validate on blur first, then keystroke after error shown. Specific
   error messages. Never "Invalid input." Never reload on error. (Spec §5)

5. MODALS: Minimum interruption. Toast > inline alert > modal.
   No nested modals ever. Use native <dialog> with .showModal(). Focus
   trapping is automatic — do NOT add manual focus trap JS. Backdrop
   dismiss requires adding a click handler (not default). (Spec §3)

6. BUTTONS: Specific labels. Never "Submit", "OK", "Yes/No", "Click Here".
   One primary CTA per viewport. (Spec §9)

7. LOADING: Feedback after 300ms. Skeleton for pages, spinner for actions.
   Never blank screen. (Spec §10)

8. MOBILE: Components transform — modal → bottom sheet, table → stacked,
   icon+text → icon only. 44px minimum touch targets. (Spec §11)

9. KEYBOARD: Every mouse interaction works via keyboard. Never remove focus
   outlines. Escape closes overlays. (Spec §12)

10. GAPS: Check Spec §18 before building. If component doesn't exist in Fluid
    Theme, build in-project and flag for backport.

11. AFTER ANY PATTERN: Search entire project for other instances. Update all
    to match. This is mandatory, not optional.

12. UNCOVERED SITUATION: Flag it. Don't improvise. Ask.
```

---

## Changelog

- **v0.2.0** — Major revision. Added 6 new sections: keyboard/accessibility (§12), data table actions (§13), search/filter/sort (§14), onboarding (§15), CTAs/conversion (§16). Added Framework Gap Tracker (§18) cross-referenced with repo `FLUID-THEME-GAPS.md` and actual `src/components/` inventory. All component references verified against Fluid Theme v0.3.2 APIs (`data-*` attributes, class names, file locations). Appendix B agent instructions include section references. HTML examples use actual Fluid Theme markup patterns. **Post-audit fixes:** Corrected native `<dialog>` behavior (backdrop click must be added not removed, Escape must be prevented for critical modals, `.showModal()` focus trapping is automatic). Added `autofocus` to Cancel button in destructive modal example. Fixed WCAG 2.2 target size citation (44px is AAA/Apple HIG, not 2.2 minimum). Corrected table responsive API (`.table-wrap` wrapper + `.table[data-responsive]` + `td[data-label]`). Noted `aria-invalid` should be set dynamically not in default markup. Added modal footer gap and destructive modal modifier to gap tracker.
- **v0.1.0** — Initial spec. 12 sections covering core behavioral patterns.
