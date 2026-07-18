---
name: design-saas-app
description: Design UI/UX for SaaS software products — from wireframes to polished interactive prototypes. Use this skill whenever the user wants to design, prototype, or mock up a SaaS application interface, including dashboards, onboarding flows, settings pages, pricing pages, admin panels, or any multi-page web app. Trigger this skill for requests involving "SaaS design", "app UI", "dashboard layout", "design a web app", "wireframe", "prototype", "user flow", "landing page for my SaaS", "design system", or any request to visually design or prototype a software product interface — even if they just say "design my app" or "what should my app look like". Also trigger when users share a product idea and want to see what the UI could look like, or when they want to improve an existing SaaS interface. Do NOT trigger for marketing-only landing pages with no product UI, static graphic design (logos, icons), or native mobile app design.
---

# SaaS UI/UX Design Skill

Create professional, production-quality SaaS interfaces — from low-fidelity wireframes to fully polished interactive React prototypes. This skill handles complete multi-page app flows and adapts its design thinking to the specific SaaS domain.

## Workflow

When the user requests a SaaS UI/UX design, follow this process:

### 1. Understand the People (The Human Rule)

Design starts with people, not screens. Before thinking about layouts or components, deeply understand the humans who will use this product. Every design decision — what to build, how it works, how it looks — should trace back to a real need or lived experience.

**Gather user context.** If the user hasn't provided enough, ask about:

- **What does the product do?** (e.g., "project management for freelancers", "analytics dashboard for e-commerce")
- **Who are the primary users?** Not just "developers" — get specific: "Senior backend engineers at mid-size companies who need to document existing systems they didn't build." Specificity leads to better design decisions.
- **What's their core job-to-be-done?** Frame it as: "When [situation], I want to [action], so I can [outcome]." Example: "When I onboard onto a new codebase, I want to auto-generate an architecture overview, so I can understand the system in hours instead of weeks."
- **What frustrates them today?** What's the pain with existing tools or workflows? This reveals what your design must fix. Example: "Manually drawing architecture diagrams that are outdated within a week."
- **Any brand direction?** (colors, mood, existing brand assets, competitors to reference)

**Build a quick user persona.** Before coding, write a 3-line persona that anchors your design decisions:

> **Jane, Staff Architect at a 200-person startup.** Manages 12 microservices. Needs to keep architecture docs current for her team. Frustrated by manual diagramming that goes stale. Values speed and accuracy over aesthetics. Uses dark mode, keyboard-driven workflows, and has 3 monitors.

Every design choice should pass the "Would Jane want this?" test. If you're designing a settings page, ask: does Jane need this setting, or are you adding it because it seems complete?

**Consider the user's emotional journey.** SaaS products are used daily — they become part of someone's work life. Map the emotional arc:
- **First visit:** Uncertain, evaluating. Design must build trust and show value fast.
- **Onboarding:** Motivated but impatient. Reduce friction, celebrate small wins ("First document generated!").
- **Daily use:** Focused, efficient. Don't get in the way. Speed and keyboard shortcuts matter here.
- **Frustration moments:** Something broke, an action failed, data is missing. Error handling and reversal patterns determine whether they stay or churn.

Use domain knowledge to fill gaps intelligently. An analytics SaaS needs data-dense layouts with excellent scannability. A creative tool needs spacious canvases with minimal chrome. A B2B enterprise tool needs clear hierarchy and power-user affordances. Adapt your suggestions to the domain — don't make the user spell out every detail.

### 2. Ask Which Stage and Output Format

Present the user with two choices before generating anything:

**Design Stage:**
- **Wireframe** — Low-fidelity structural layout. Grayscale, focused on information architecture, content hierarchy, and user flow. No visual polish — just boxes, labels, and flow. This is for validating structure before investing in aesthetics.
- **Polished Design** — High-fidelity interactive prototype. Full color, typography, spacing, micro-interactions, and responsive behavior. Production-grade code the user could adapt into a real product.
- **Both (sequential)** — Start with wireframe for approval, then build the polished version.

**Output Format:**
- **React (.jsx)** — Single-file React component using Tailwind utilities and hooks for interactivity. Best for users who want to iterate within a React ecosystem or view directly in the Claude artifact preview. Uses available libraries like lucide-react, recharts, shadcn/ui.
- **HTML/CSS/JS (.html)** — Standalone single-file HTML document with embedded CSS and vanilla JavaScript. Opens directly in any browser with no build tools or dependencies. Best for quick sharing, stakeholder review, or users not working in React.
- **Both** — Generate both formats so the user can view in-browser (HTML) and also drop the React version into their codebase.

If the user has already indicated their preferences for either choice, skip that question and proceed. Always ask about output format — don't assume React or HTML by default. The output format affects implementation decisions throughout the process, so it needs to be decided upfront.

When generating **HTML/CSS/JS**, follow these guidelines:
- All CSS in a single `<style>` block in the `<head>`
- All JavaScript in a single `<script>` block before `</body>`
- Use semantic HTML elements (`<nav>`, `<main>`, `<aside>`, `<section>`, `<button>`)
- Load Google Fonts via `@import` in the CSS
- External libraries from cdnjs.cloudflare.com if needed
- Page navigation via showing/hiding sections with a simple JS function
- Mobile responsiveness via CSS media queries
- No build tools, no npm, no frameworks — pure browser-native code

When generating **React (.jsx)**, follow these guidelines:
- Single-file React component with default export
- Use Tailwind utility classes for styling
- State management with React hooks (useState, useReducer)
- Available libraries: lucide-react, recharts, d3, shadcn/ui, three.js, lodash
- Page navigation via state-driven conditional rendering
- Components defined within the single file, composed in the main export

### 3. Explore Before Committing (The Ambiguity Rule + The Re-design Rule)

Don't jump to the first layout that comes to mind. Good design requires sitting with uncertainty, exploring alternatives, and learning from what already works.

**Study existing solutions first (Re-design Rule).** Most problems have been solved before in some form. Before designing from scratch:
- Identify 2–3 competing or adjacent products in the same domain. How do they solve the core UX challenges? What works well? What feels clunky? The domain-aware patterns table below is a starting point, but real products reveal nuances that abstractions miss.
- Ask the user: "Are there any existing tools you like or dislike? What specifically works or doesn't?" This is goldmine context — it tells you what to borrow and what to avoid.
- Recognize proven patterns and build on them rather than reinventing. If every CRM uses a pipeline view, there's a reason — users have learned that pattern. Innovate on the details, not the fundamentals.
- When a user mentions they have an existing product to redesign, start by understanding what currently works before changing anything. Preserve what users already rely on.

**Explore 2–3 directions before converging (Ambiguity Rule).** Resist the urge to commit to a single approach immediately:
- For complex flows, briefly describe 2–3 alternative structural approaches before building. Example: "For the document generator, I see two approaches: (A) a step-by-step wizard that guides users through repo → doc type → settings → generate, or (B) a single-page form with smart defaults that lets power users generate in one click. Which fits your users better?"
- Present trade-offs honestly: approach A is more guided but slower for experts; approach B is faster but may overwhelm new users.
- If the user doesn't have a strong preference, pick the approach that best serves the primary persona — but note the alternative as a future consideration.
- For visual direction, describe the aesthetic you're planning before coding: "I'm thinking dark, technical, dense — like a dev tool. Or would you prefer something lighter and more approachable?" One sentence of alignment upfront saves a full redesign later.

This exploration phase should be lightweight — a few sentences of reasoning and a quick check with the user, not a formal research report. The goal is to make informed choices rather than defaulting to the first idea.

### 4. Design Thinking (Do This Before Coding)

Spend real thought on these before writing a single line of code:

**Information Architecture**
- What are the primary, secondary, and tertiary navigation items?
- What does the user need to see first? What can be progressive-disclosed?
- How does the user move between pages? What's the mental model?
- Where does the user spend 80% of their time? That page gets 80% of your design effort.

**User Flow Mapping**
- Map the critical path: what's the #1 thing a user comes to do, and how few clicks does it take?
- Identify states: empty states, loading states, error states, success states. Design for all of them, not just the happy path.
- Consider onboarding: how does a brand-new user understand what to do?

**Domain-Aware Design Patterns**
Adapt your design instincts to the SaaS category:

| Domain | Key Design Considerations |
|--------|--------------------------|
| Analytics / BI | Data density, chart readability, filter systems, date range pickers, export flows |
| Project Management | Kanban/list/timeline views, drag-and-drop, status indicators, assignment UX |
| CRM / Sales | Contact cards, pipeline views, activity timelines, bulk actions |
| Developer Tools | Code blocks, API references, terminal-like UIs, dark mode preference |
| Communication | Message threading, presence indicators, notification hierarchies |
| Finance / Billing | Tables with sorting, transaction history, invoicing flows, number formatting |
| Creative Tools | Canvas-based layouts, toolbars, property panels, asset libraries |
| HR / People | Org charts, profile cards, approval workflows, form-heavy interfaces |
| E-commerce Admin | Order management, inventory tables, revenue charts, product editors |
| Healthcare / Life Science | Data compliance indicators, patient/sample flows, careful status coloring |

If the domain isn't listed, reason about what makes it unique and design accordingly.

## Design System Specifications

Every SaaS design you create should be built on a consistent, well-defined design system. Think of these as the engineering specs behind the visual design — they ensure consistency, scalability, and professionalism across every page and component.

### 1. Layer Names & Hierarchy

Establish a clear naming and nesting structure for every element in the design. This matters because it makes the prototype code readable, maintainable, and translatable into a real codebase.

**Naming convention:** Use descriptive, hierarchical names that communicate purpose and scope.
- **Page level:** `SignupPage`, `DashboardPage`, `SettingsPage`
- **Section level:** `DashboardHeader`, `DashboardMetrics`, `DashboardRecentDocs`
- **Component level:** `MetricCard`, `DocListItem`, `NavSidebarItem`
- **Element level:** `MetricCard-value`, `MetricCard-label`, `MetricCard-trend`

**Hierarchy rules:**
- Organize from outside-in: Page → Layout Region → Section → Component → Element
- Shared chrome (sidebar, top bar) lives at the app-shell level, not duplicated per page
- Modal and overlay layers sit above the page layer with appropriate z-index stacking: base content (0), sticky headers (10), dropdowns (20), modals (30), toasts (40)
- Every component should be self-contained — it should work correctly regardless of where it's placed

### 2. Layout Structure Choices

Define the structural bones of the application before any visual styling.

**Common SaaS layout patterns** (choose based on product complexity):
- **Sidebar + Content:** Best for feature-rich apps with 5+ nav items. Fixed sidebar (220–280px), fluid content area. The workhorse of SaaS.
- **Top Nav + Content:** Best for simpler apps with 3–5 nav items. Full-width content area, horizontal nav. Feels more open.
- **Sidebar + Top Bar + Content:** The most common for complex SaaS. Sidebar for primary navigation, top bar for search/user/breadcrumbs, content area for everything else.
- **Canvas + Panels:** For creative/builder tools. Central canvas with collapsible left (tools) and right (properties) panels.

**Layout implementation rules:**
- Use CSS Grid for page-level layout (sidebar + content). Use Flexbox for component-level layout (rows, alignment).
- Sidebar should be position-fixed or sticky so content scrolls independently.
- Content areas should have a max-width container (1200–1440px) centered within the available space for readability on ultra-wide monitors.
- Define explicit grid areas: `sidebar | main`, `sidebar | topbar + content`, etc.

### 3. Visual Style

Commit to a deliberate aesthetic direction for every design. The visual style should feel tailored to the product's domain and audience.

**Before coding, define:**
- **Mood:** Clinical/precise (fintech), warm/approachable (HR), dark/technical (dev tools), clean/airy (creative)
- **Shape language:** Sharp corners (serious, enterprise) vs. rounded corners (friendly, consumer-like). Pick a default border-radius and stick to it.
- **Density:** Compact (data-heavy tools, power users) vs. spacious (onboarding, consumer-facing)
- **Surface style:** Flat (minimal, modern), elevated (cards with shadows), layered (overlapping elements, depth)
- **Border style:** Subtle borders (#eee–#e0e0e0) for structure, or borderless with shadows for a floating feel

**Build custom.** Never rely on a preset design system aesthetic. Every design should feel like it was crafted specifically for this product — unique color palettes, distinctive typography pairings, custom component shapes.

### 4. Typography Styles

Define a complete type scale before coding. Typography alone carries 80% of a UI's personality.

**Required type scale (define all of these):**

| Token Name | Typical Use | Size Range | Weight | Line Height |
|---|---|---|---|---|
| `display` | Hero headings, landing pages | 36–48px | 700–800 | 1.1–1.2 |
| `h1` | Page titles | 24–30px | 600–700 | 1.2–1.3 |
| `h2` | Section headings | 18–22px | 600 | 1.3 |
| `h3` | Card titles, subsections | 15–18px | 600 | 1.4 |
| `body` | Paragraph text, descriptions | 14–16px | 400 | 1.5–1.7 |
| `body-sm` | Secondary text, metadata | 12–13px | 400 | 1.5 |
| `caption` | Labels, timestamps, helper text | 11–12px | 400–500 | 1.4 |
| `overline` | Section labels, categories | 10–11px | 500–600 | 1.4 |
| `mono` | Code, IDs, technical values | 12–13px | 400 | 1.5 |

**Font pairing rules:**
- Choose a distinctive display/heading font and a highly readable body font from Google Fonts.
- The font pairing should hint at the product's personality — a fintech app (e.g., DM Sans + JetBrains Mono) feels different from a creative tool (e.g., Outfit + Inter).
- Monospace font for code blocks, IDs, timestamps, and technical data.
- Never use more than 3 font families in a single design.
- Apply `letter-spacing` intentionally: tighter for large headings (-0.02em), wider for overlines and labels (0.05–0.1em).

### 5. Colors (Fills, Strokes, Backgrounds)

Build a complete color system from scratch, not just a primary color.

**Required color tokens:**

| Category | Tokens | Purpose |
|---|---|---|
| **Brand** | `primary`, `primary-hover`, `primary-active`, `primary-subtle` | Main action color + states |
| **Accent** | `accent`, `accent-subtle` | Secondary highlights, badges |
| **Semantic** | `success`, `warning`, `error`, `info` + `-subtle` variants | Status indicators, alerts |
| **Neutrals** | `gray-50` through `gray-900` (at least 7 steps) | Text, borders, backgrounds |
| **Backgrounds** | `bg-primary`, `bg-secondary`, `bg-tertiary`, `bg-elevated` | Surface hierarchy |
| **Borders** | `border-default`, `border-subtle`, `border-strong` | Container edges, dividers |
| **Text** | `text-primary`, `text-secondary`, `text-tertiary`, `text-disabled` | Content hierarchy |

**Color application rules:**
- **Fills:** Use background tokens for surfaces. Cards use `bg-elevated` over `bg-primary`. Nested elements step up one level.
- **Strokes/borders:** Default borders are `border-subtle` (1px). Interactive element borders are `border-default`. Focused elements use `border-strong` or the `primary` color.
- **Opacity:** Use opacity for overlays (modal backdrop: 0.5 black), disabled states (0.4), and hover backgrounds (0.05–0.08 of the primary color).
- Implement all colors as CSS custom properties (`--color-primary`, `--color-bg-secondary`, etc.) so themes can be swapped by redefining variables.

### 6. Component Variants

Every interactive component must be designed in multiple states. Don't just design the happy path — design every state the user might encounter.

**Required states for interactive components:**

| State | Visual Treatment |
|---|---|
| **Default** | Base appearance — how it looks at rest |
| **Hover** | Subtle background shift, cursor change, slight elevation. Should feel responsive without being distracting. |
| **Active/Pressed** | Slightly darker/compressed feel. Brief transition. |
| **Focused** | Visible focus ring (2px outline, offset 2px, high contrast). Essential for keyboard navigation. |
| **Disabled** | Reduced opacity (0.4–0.5), `cursor: not-allowed`, muted colors. |
| **Loading** | Spinner or skeleton, disabled interaction, preserved layout dimensions. |
| **Error** | Red border/outline, error message below, icon indicator. |
| **Success** | Green checkmark, confirmation message, brief highlight animation. |
| **Empty** | Illustrated placeholder with CTA. Never leave a blank void. |

**Component variant guidance:**
- Buttons: primary, secondary, ghost, destructive — each with all states above.
- Inputs: default, focused, filled, error, disabled — with labels, helper text, and validation messages.
- Cards: default, hover (slight lift), selected (border highlight), loading (skeleton).
- Navigation items: default, hover, active/current, disabled, with-badge.
- Tables: row hover, row selected, sortable column headers, empty state.

### 7. Spacing & Padding

Use a consistent spacing scale throughout the entire design. Inconsistent spacing is the fastest way to make a UI feel amateur.

**Spacing scale (base-4 system):**
- `4px` — Tight: between icon and label, inline elements
- `8px` — Compact: between related form fields, list items
- `12px` — Default inner: padding inside compact components (tags, chips, small buttons)
- `16px` — Standard: padding inside cards, between form groups, component internal padding
- `20px` — Comfortable: section padding, generous card padding
- `24px` — Spacious: between major sections on a page
- `32px` — Section gap: between distinct content blocks
- `48px` — Region gap: between page-level regions (header → content → footer)
- `64px` — Page margin: outer page padding on desktop

**Spacing rules:**
- Related elements are closer together; unrelated elements are farther apart (Gestalt proximity principle).
- Component internal padding should be consistent: if a card has 16px padding, all cards have 16px padding.
- Vertical rhythm matters — keep vertical spacing between elements consistent within a section.
- Page-level padding decreases on mobile: 64px → 24px on desktop → mobile.
- Inside tables and lists, use tighter spacing (8–12px vertical, 16–20px horizontal).

### 8. Constraints & Responsive Rules

Define explicit size constraints so the layout holds together at every viewport size.

**Container constraints:**
- **Max content width:** 1200–1440px, centered. Prevents line lengths from becoming unreadable on wide screens.
- **Sidebar width:** Fixed 220–280px on desktop. Collapsible to icon-only (64px) or fully hidden on tablet/mobile.
- **Min content width:** 320px. Nothing should break below this.
- **Modal widths:** Small (400px), Medium (560px), Large (720px), Full (90vw). Max-height: 85vh with internal scroll.
- **Card min-width:** 240px in grid layouts. Use `minmax(240px, 1fr)` in CSS Grid.
- **Table min-width:** If table exceeds viewport, use horizontal scroll on the table container (not the page).

**Breakpoint system:**
| Breakpoint | Width | Layout Changes |
|---|---|---|
| Mobile | < 640px | Single column, no sidebar, stacked cards, hamburger nav, bottom navigation |
| Tablet | 640–1024px | Collapsed sidebar (icons only), 2-column grids, simplified tables |
| Desktop | 1024–1440px | Full sidebar, multi-column layouts, full tables |
| Wide | > 1440px | Centered content container, prevent over-stretching |

**Constraint rules:**
- Sidebar: `position: fixed` or `position: sticky; top: 0; height: 100vh`
- Content area: `flex: 1; overflow-y: auto; min-width: 0` (the `min-width: 0` prevents flex overflow bugs)
- Images and charts: `max-width: 100%; height: auto`
- Text containers: `max-width: 65ch` for readable paragraph line lengths

### 9. Design Tokens / Variables

Centralize all design values into reusable tokens. This is what makes a design feel systematic rather than ad-hoc.

**Implement all tokens as CSS custom properties** at the `:root` level:

```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f8fafc;
  --color-bg-elevated: #ffffff;
  --color-text-primary: #0f172a;
  --color-text-secondary: #64748b;
  --color-border-default: #e2e8f0;
  --color-border-subtle: #f1f5f9;

  /* Typography */
  --font-display: 'Your Display Font', sans-serif;
  --font-body: 'Your Body Font', sans-serif;
  --font-mono: 'Your Mono Font', monospace;
  --text-xs: 11px;
  --text-sm: 13px;
  --text-base: 14px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 22px;
  --text-3xl: 28px;

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Borders */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.10), 0 8px 10px rgba(0,0,0,0.04);

  /* Transitions */
  --transition-fast: 100ms ease;
  --transition-base: 150ms ease;
  --transition-slow: 300ms ease;

  /* Z-Index */
  --z-base: 0;
  --z-sticky: 10;
  --z-dropdown: 20;
  --z-modal: 30;
  --z-toast: 40;
  --z-tooltip: 50;
}
```

**Token usage rules:**
- Never use raw values in component styles — always reference tokens. Write `var(--color-primary)` not `#2563eb`.
- When using Tailwind in React, map these tokens to Tailwind's theme or use inline `style` with the variables.
- For HTML output, reference variables directly in CSS: `background: var(--color-bg-secondary)`.
- Token names should be semantic (purpose-based) not descriptive (appearance-based): `--color-text-secondary` not `--color-gray-500`.

### 10. Effects (Shadows, Blur, Overlays)

Effects create depth, focus, and atmosphere. Use them intentionally — every effect should serve a spatial or interactive purpose.

**Shadow scale** (from subtle to dramatic):
| Token | Use | Value |
|---|---|---|
| `shadow-xs` | Subtle card lift, input borders | `0 1px 2px rgba(0,0,0,0.04)` |
| `shadow-sm` | Cards at rest, dropdown triggers | `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)` |
| `shadow-md` | Hovered cards, popovers | `0 4px 6px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04)` |
| `shadow-lg` | Dropdown menus, floating panels | `0 10px 15px rgba(0,0,0,0.08), 0 4px 6px rgba(0,0,0,0.04)` |
| `shadow-xl` | Modals, command palettes | `0 20px 25px rgba(0,0,0,0.10), 0 8px 10px rgba(0,0,0,0.04)` |

**Blur effects:**
- **Backdrop blur:** Use `backdrop-filter: blur(8px–12px)` on modal overlays, floating headers, and glass-morphism elements. Pair with a semi-transparent background.
- **Background blur on sticky headers:** `backdrop-filter: blur(10px); background: rgba(255,255,255,0.85)` creates a frosted glass effect when content scrolls beneath.
- **Focus blur:** Dim and blur background content when a modal is open: `filter: blur(2px–4px)` on the content behind the overlay.

**Overlay specs:**
- **Modal backdrop:** `background: rgba(0,0,0,0.4–0.6)` depending on desired darkness. Use `backdrop-filter: blur(4px)` for modern polish.
- **Dropdown shadow + border:** Combine `shadow-lg` with a `1px solid var(--color-border-subtle)` for crisp edges.
- **Toast/notification:** `shadow-lg` with a colored left border (4px) indicating severity.

**Transition effects:**
- Hover state transitions: `transition: all var(--transition-fast)` — keep hover responses snappy.
- Page transitions: `transition: opacity var(--transition-slow)` for fade-in between pages.
- Card hover lift: `transform: translateY(-2px); box-shadow: var(--shadow-md)` on hover.
- Expandable sections: `transition: max-height var(--transition-slow)` for smooth accordion behavior.
- Loading skeletons: Animated shimmer effect using CSS `@keyframes` with a gradient sweep.

## Design Principles

These higher-level principles guide how you apply the design system above:

### UX Best Practices — HCI Interaction Principles

Every SaaS design must address all 8 principles of human-computer interaction. **Read `references/hci-principles.md` before coding** — it contains detailed implementation guidance, patterns, and examples for each principle.

| # | Principle | Core Requirement | Key Patterns to Implement |
|---|---|---|---|
| 1 | **Consistency** | Standardize all interaction patterns across pages | Unified filter/sort/search behavior, consistent icon meanings, action placement rules (primary top-right, destructive separated) |
| 2 | **Shortcuts** | Accelerate power users | Command palette (⌘K), keyboard shortcuts with hint labels, bulk select + actions, deep linking URLs |
| 3 | **Feedback** | User always knows system status | Immediate (< 100ms) press states, short-wait spinners, long-wait progress bars, completion toasts, inline validation on blur, optimistic UI |
| 4 | **Dialogue** | Clear communication at decision points | Specific task completion messages ("Doc generated for payment-service"), named confirmation dialogs, guided empty states with CTAs, severity-coded toasts |
| 5 | **Error handling** | Prevent first, recover fast | Input constraints (pickers > free text), inline field validation, actionable error messages (what + why + fix), custom 404/500 pages, graceful component degradation, auto-save drafts |
| 6 | **Reversal** | Every action feels safe to try | Undo toasts (6–8s) instead of confirm dialogs, edit/cancel with unsaved-changes warning, version history, soft delete with trash |
| 7 | **Control** | Users decide how to interact | View switching (list/grid/table), resizable panels, user preferences (theme/density/notifications), saved filter views, bulk operations |
| 8 | **Memory load** | Recognize, don't recall | Global search across entity types, breadcrumbs on every page, recent items + favorites, faceted filters for lists > 20 items, contextual tooltips, smart defaults from context |

When designing, mentally walk through each principle and verify the design addresses it. If a principle is weak for a particular page, add the missing pattern.

### Responsive Design
- Design mobile-first in thinking, desktop-first in implementation (SaaS is primarily desktop).
- Sidebars collapse to hamburger on mobile. Tables become card layouts. Charts resize gracefully.
- Touch targets on mobile: minimum 44px × 44px. Follow breakpoints in Section 8.

### Accessibility
- Semantic HTML (`<nav>`, `<main>`, `<aside>`, `<button>` — not `<div>` for everything).
- WCAG AA contrast: 4.5:1 normal text, 3:1 large text. Don't rely on color alone.
- Keyboard navigable with visible focus rings (see Section 6). ARIA labels on all interactive elements.

## Implementation Guide (The Tangibility Rule)

Ideas get better when they're visible. The whole point of this skill is to make concepts tangible — turning vague product ideas into clickable, viewable prototypes that teams can react to, critique, and refine. Every fidelity level serves a purpose:

- **Wireframes** make structure debatable. You can't argue about information architecture in the abstract — but put boxes on a screen and suddenly everyone has opinions. That's the point.
- **Polished prototypes** make the product feel real. Stakeholders, investors, and users can interact with something that looks and feels like the final product, which surfaces feedback that wireframes never could.

Always encourage iteration: "Here's the wireframe. What feels right? What feels off? I'll refine based on your feedback before we move to the polished version." The prototype isn't the deliverable — the conversation it starts is.

### Wireframe Stage

Output in the user's chosen format (React `.jsx` or HTML `.html`) with:
- Grayscale only: `#ffffff`, `#f5f5f5`, `#e0e0e0`, `#999999`, `#333333`, `#000000`
- No decorative elements — pure structure with dashed borders showing component boundaries
- Realistic placeholder text (domain-appropriate: "Monthly Revenue: $24,500", not "Lorem ipsum")
- Section labels as subtle annotations: "Top Nav", "Sidebar", "Filter Bar"
- Multi-page flows use tab-based navigation so the user can click through the entire flow

### Polished Design Stage

Output in the user's chosen format with:
- Full custom color palette and typography via CSS variables and Google Fonts
- Responsive layout with real breakpoints per Section 8
- Micro-interactions: hover states, transitions, subtle load animations
- Realistic sample data throughout — never placeholder text
- Working interactive elements: page navigation, dropdowns, modals, toggles
- Clean component structure with state management for interactivity

### Multi-Page Flow Implementation

Implement page navigation within a single file. **React:** use `useState` to track current page and conditionally render page components. **HTML:** use show/hide with a `showPage(id)` JS function toggling a `.hidden` class.

Each page should feel complete — not a cut-down demo:
- Consistent navigation chrome across pages (sidebar, top bar) with active state indicators
- Realistic, domain-appropriate content on every page
- Subtle page transitions (fade or slide)
- At least 3–5 pages for a meaningful flow

### Code Quality

Even though this is a prototype, write clean code:
- **React:** Use Tailwind utility classes for styling. Name components descriptively (`DashboardMetricsGrid`, not `Section1`). Use hooks for state. Keep the component tree shallow.
- **HTML:** Use well-structured CSS with clear class naming conventions. Group styles by component/section. Use CSS custom properties (variables) for repeated values. Keep JavaScript minimal and readable.
- **Both:** Add brief comments for complex layout decisions. Use semantic HTML elements. Ensure consistent spacing and indentation.


