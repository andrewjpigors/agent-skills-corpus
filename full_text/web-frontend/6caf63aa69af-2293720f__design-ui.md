---
name: design-ui
description: Create distinctive, production-grade frontend interfaces with high design quality across web, mobile (React Native), and macOS-style layouts. Applies Apple Human Interface Guidelines (spacing, typography, touch targets, whitespace, navigation) merged with bold aesthetic direction. Use when building or styling UI, mobile-first screens, native-feeling web apps, or when the user mentions Apple HIG, iOS design, design system tokens, or platform ergonomics.
version: 3.0.0
category: design
portable: true
---

# Frontend Design

## Purpose

Build distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices. A premium app is not defined by one big feature but by the sum of many small, intentional decisions — press feedback, motion, tactile response, keyboard integration, and thoughtful empty states.

## Foundational Design Principles

These principles, distilled from platform Human Interface Guidelines, frame every design decision. Use them as a lens when designing and evaluating interfaces.

### Purpose
Design is making something with intention. Every feature asks for the user's **time, attention, and trust** — valuable things you can't afford to waste. Before sketching or coding, ask: does this have purpose? Choosing what **not** to include is often more important than what to build.

**Create value.** At every stage, ask what the product is for and whether the design serves that purpose. **Keep focused** — prioritize the most important features by aligning with how people actually want to use the product. **Find new ways to solve the problem** — investigate existing solutions without re-creating them; define what sets your product apart.

**Affordances & signifiers** — every interactive element must signal its purpose without instruction. A button looks pressable (shadow, shape, label), a link looks clickable (color, underline), a slider looks draggable (handle, track). Use active states, color, and visual cues so the user instinctively knows what to do. If an action needs explaining, the affordance is wrong.

### Agency
Put people in control. Let them do things their way instead of funneling them down a predetermined path. Offer **forgiveness** — make it easy to undo actions, confirm destructive operations. Agency gives people confidence to explore freely.

**Stay out of the way.** Get people directly to the task or content at hand — the best designs are unobtrusive and present when needed. **Give freedom to explore** — avoid locking people into specific flows or modes; make guided flows easy to skip or escape. **Help recover from mistakes** — build forgiveness in, make reversing actions effortless so people feel safe to explore.

### Responsibility
Act in people's best interest. Privacy is a human right — only request data when necessary, be transparent about its use. **Anticipate misuse**, especially with AI capabilities. Add safeguards (previews, confirmations, disclaimers). Remove features entirely if risks outweigh value. Design for longevity — use standardized patterns, make elements repairable/updatable, and respect the user's investment in your product.

**Be transparent** about what your product does and why from the very first interaction. Provide clear rationale when asking for permission. **Keep information safe** — only collect what's needed, handle it with care, and put protections in place to prevent abuse.

**Privacy patterns:** Ask for permission **in context**, not at launch — wait until the user engages a feature that needs the data. Write brief, active-voice purpose strings ("The app records at night to detect snoring" not "Microphone access needed for better experience"). Process data on-device when possible. Use passkeys over passwords; store sensitive data in keychain, never plaintext. Prefer system auth (Face ID, Touch ID, WebAuthn) over custom login forms. Clearly indicate when recording, location sharing, or data collection is active — never obscure system indicators.

### Familiarity
Build on what people already know. Use **metaphor** (trash = delete) that draws on real-world experience. Be **consistent** — things that look the same should behave the same. Consistent placement helps users predict where controls will be. **Provide clear feedback** — show when controls are available, indicate when content changes, use system patterns for alerts and choices.

**Balance with brand expression.** Standards create comfort, but rigid adherence can stifle identity. A great design system provides structure without erasing the brand's unique visual energy. Know when to intentionally deviate from platform conventions to express character — as long as the deviation serves a purpose and doesn't harm usability.

### Flexibility
People use your design in unique ways across different contexts. Support the full range of devices (touch on phone, pointer on laptop, hands-free in car). Cater to diverse abilities — age, language, expertise, accessibility needs. Let people personalize controls and layouts.

**Design for everyone** — treat accessibility as a priority from the start. **Preserve context** across platforms — keep content and controls in consistent positions, use natural animations for transitions. **Consider varied input methods** — voice, touch, keyboard, pointing devices — more input modes means more people can use your product their way. **Approach every platform with intention** — software should feel polished and at home wherever it runs.

**Accessibility is not optional.** Support multiple senses (visual, auditory, haptic) so no single mode is required. Adopt Accessibility APIs rather than reimplementing them. Test with assistive technologies. Provide customization for text size, colors, and layout density. Every accessibility improvement makes the product better for all users.

### Simplicity
Strip away the unnecessary so the core purpose shines. Simplicity is **not** minimalism — burying all features in one place is not simple. Be **concise** (plain language, fewer steps) and **clear** (strong hierarchy using order, spacing, and contrast). Every element should earn its place. **Establish hierarchy** — when form and function are readily apparent, people know how to reach a desired outcome.

**Obsessive reduction** — start by cutting non-essential elements to avoid decision paralysis. Only reveal complexity when absolutely necessary. **The three-tap rule** — the most important actions should be available within three taps or clicks. Optimize for the common, frequent use cases.

**Master visual hierarchy** — guide the eye, don't just place elements. Use **typography size** (larger = more important), **color weight** (bold/high-contrast for primary actions, muted for secondary), and **spacing** (more space around = more significance). The single biggest tell of amateur design is a flat visual hierarchy where nothing stands out — every element competes equally for attention.

### Craft
Attention to detail that tells people you care. Beautiful fonts across devices, thoughtful colors that adapt light/dark, responsive animations with natural feedback, reliable foundations.

**Quality sets the tone** — every element shows people how much you care. Be deliberate with each decision: stunning visuals, smooth animations, precise wording. **Experiment and iterate** — prototype early, try new approaches, discard what doesn't work. Test in real-world settings. **Maintain your craft** — shipping isn't the finish line. Keep the interface current with latest platform capabilities and keep the quality bar high. Design is an ongoing commitment.

### Delight
Not confetti or tacked-on flourishes. Delight is the **natural result** of getting all the other principles right.

**Identify the emotion you want to inspire** — a fitness app might energize, a meditation app might calm, a game might thrill. **Create defining moments** — every interaction is a chance to show what your design stands for. **Don't mistake delight for decoration** — people are trying to accomplish a task; don't let pursuit of delight get in the way of purpose. **Consider the whole** — delight is the culmination of everything: the freedom to act, safety to explore, comfort of familiar metaphors, flexibility across contexts. When you design with intent, focus, and care, the result is naturally delightful.

## Product Design Mindset

Designing a product is different from designing a screen. A screen is a layout; a product is a system of connected flows, states, and decisions. Adopt this mindset to move from surface-level UI to cohesive product design.

### Start with User Intent

Don't begin with icons, colors, or layouts. Begin with one question: **What is the primary action the user needs to take right now?** Every design decision should serve that intent first.

- **One action per view** — identify the single most important thing the user can do on this screen (sign up, create, search, read). Make that action dominant. Everything else — search bars, filters, secondary navigation — augments the core intent as the user's needs expand.
- **Features are secondary** — resist the urge to cram every capability onto the surface. Serve the primary intent with clarity first, then progressively disclose supporting features as the user signals deeper need.

### Leverage Existing Mental Models

Users have spent over 30 years developing expectations for how interfaces work. Navigation at the top, clickable links are blue, settings in a gear icon — these conventions exist because they work.

- **Follow before you break** — start with established patterns (top nav, left sidebar, bottom tabs on mobile). Users don't have to learn anything new to use your product. Only deviate when the convention truly conflicts with your product's unique needs.
- **Scale through convention** — designs based on standard patterns are easier to scale, hand off, and adapt across platforms. Novel layouts require more documentation, more testing, and more cognitive effort from every new user.

### Design for All States, Not Just the Happy Path

The happy path (perfect data, no errors, ideal conditions) is the easiest screen to design. Real users live in the other states:

- **Empty states** — guide the user when there's no content yet. Explain what belongs here and how to get started. An empty state is an onboarding moment, not a void.
- **Loading states** — show shimmer skeletons that mirror the final layout so the user knows what to expect and that something is happening.
- **Error states** — explain what went wrong in plain language, and offer a clear next step (retry, go back, contact support). Never leave the user stranded with a generic error code.
- **Success / confirmation states** — confirm the action completed and set up the next logical step. "Team created — now invite your members" is better than a silent success.
- **Edge cases** — zero results from a search, a network timeout mid-form, data that doesn't fit its container. Every edge case is a design decision, not a developer bug.

If you've only designed the happy path, you've designed 20% of the product.

### Build for Flow, Not Just Sections

Stop thinking in static screens. Think in user sequences — how did the user arrive here, and what do they need to do next?

- **Chained decisions**: Every action creates a next logical step. After creating a team space, prompt the user to add members. After uploading a file, offer to share it. After completing a purchase, show the order status. The product feels intelligent when it anticipates the user's next move.
- **Entry and exit**: For every screen, ask: where did the user come from? Where can they go? Are those paths obvious? A screen with no clear exit feels like a trap.
- **Connected flows**: A change in one part of the product (updating a profile, changing a setting) should reflect everywhere that data appears. Inconsistency between screens breaks the illusion of a single product.

### Design Systems as Trust-Building

A design system is not a color palette and a button library. It is the shared language that makes the product feel like one coherent thing rather than a collection of pages built by different people at different times.

- **Consistency builds trust**: When every button, spacing unit, and type style follows the same rules, users stop noticing the UI and focus on the task. Inconsistency forces them to re-learn how to interact on every screen.
- **Patterns beat novelty**: Reusing the same pattern for similar tasks (always use a modal for create flows, always use a sidebar for navigation) makes the product predictable. Predictable products feel safe and intuitive.
- **Familiarity across contexts**: A button in the dashboard should look and behave the same as a button in settings. A confirmation dialog should use the same structure everywhere. Users internalize these patterns and navigate faster over time.
- **Reflect your team's values**: A lean startup needs a flexible, minimal system that doesn't slow experimentation. A large organization needs deep, strict definitions that ensure consistency across dozens of teams. The system serves the team, not the other way around.
- **Know when to break the rules**: Mastery of a design system means knowing exactly when to follow convention and when to break it with intention. A deliberate deviation (a modal that expands into a full page, a button that animates into a progress bar) is powerful because it's rare. Random inconsistency erodes trust; intentional rule-breaking creates memorable moments.

**The shift**: Stop designing pages. Start designing systems of connected flows, states, and consistent patterns. That is the difference between a UI designer and a product designer.

### Friction as a Design Choice

Not all friction is bad. Intentional friction can prevent errors, encourage better habits, or slow down a high-stakes decision. The key is intent — friction designed to help the user is good; friction designed to trap them is a dark pattern.

- **When to add friction**: Destructive actions (delete, irreversible settings), financial confirmations (purchase, subscription change), or actions that lock the user into a workflow. A confirm dialog, a swipe-to-confirm gesture, or a required deliberate pause serves the user's long-term interest.
- **When to remove friction**: Login, data entry, navigation, discovery. Every unnecessary click, field, or loading state between the user and their goal is friction that should be eliminated.
- **Dark patterns to avoid** — forced actions (must disable something to proceed), confirm-shaming ("Are you sure? You'll miss out on..."), hidden costs revealed at checkout, trick dismiss (close button that doesn't close). These erode trust and violate the Agency principle.
- **Enforce standards with escape hatches**: If your system enforces best practices (naming conventions, required fields, format rules), provide a simple way to toggle the enforcement off. Power users should be able to bypass guardrails after demonstrating understanding.
- **AI personalization must feel intentional**: Unsolicited automation (randomized suggestions, unexpected changes) erodes trust. Every AI-driven action must be traceable to user behavior or explicitly confirmed. If the user can't explain why the AI did something, the design has failed.

## Apple Human Interface Guidelines

Full platform guidance from [Apple HIG](https://developer.apple.com/design/human-interface-guidelines). **Do not web-search for HIG** — use this section as the source of truth for spacing, patterns, presentation, and platform ergonomics.

**Brand vs platform:** Project design tokens carry color, typeface, and visual signature. HIG carries structural rules — grid, targets, safe areas, hierarchy, patterns, accessibility.

**Relationship to Foundational Design Principles above:** Apple's classic triad (Clarity, Deference, Depth) maps to Purpose, Agency, Simplicity, and Craft. Apply both lenses — HIG for platform-native ergonomics, Foundational Principles for product intent and brand.

---

### Getting started

Design a great experience for any Apple platform — or Apple-aligned web — by starting with:

1. **People first** — what task are they completing? What context (one hand, desk, glance)?
2. **Platform conventions** — use patterns users already know before inventing new ones.
3. **Content over chrome** — strip UI to what the task requires; reveal complexity progressively.
4. **System integration** — respect safe areas, Dynamic Type, dark mode, reduced motion, assistive tech.
5. **One primary action per screen** — everything else is secondary or tertiary.
6. **Hicks' Law** — decision time increases with the number and complexity of choices. Make the primary action large, easy to reach, and require minimal movement. Every additional option reduces the likelihood the user will choose any of them.

---

### Design fundamentals — core principles

Apple's three design principles that guide every platform:

| Principle | Meaning | Apply as |
|-----------|---------|----------|
| **Clarity** | Text legible at every size; icons precise; adornment subtle | Strong type hierarchy; readable 17px body; meaningful icons |
| **Deference** | UI helps people understand content — never competes with it | Content-first layout; minimal chrome; translucent floating nav |
| **Depth** | Visual layers and realistic motion convey hierarchy and vitality | Elevation via materials; spatial transitions; purposeful motion |

---

### Designing for iOS

- **Ergonomics:** One- or two-handed use at ~1ft. Primary actions in thumb-reachable zones (bottom half). Key interactive elements on the right side of the screen by default to accommodate the right-handed majority — the thumb naturally rests on the right edge.
- **Navigation:** Tab bar (3–5 destinations) · navigation stack with visible back · large titles that collapse on scroll.
- **Gestures:** Swipe-back to pop stack · swipe actions on list rows · pull-to-refresh where appropriate.
- **Layout:** Single column default · full-bleed backgrounds · floating blurred chrome over content.
- **Safe areas:** Always inset from notch, Dynamic Island, home indicator — `env(safe-area-inset-*)`.
- **Modality:** Sheets and full-screen covers for focused tasks — always dismissible (swipe, ×, Escape on iPad).
- **Adaptivity:** Support rotation, Split View, Stage Manager; don't assume fixed phone width on iPad.

---

### Designing for macOS

- **Menu bar:** Expose all commands; mirror important actions in toolbar and menus.
- **Keyboard:** Every major action has a shortcut; Return triggers primary; Escape dismisses.
- **Pointer:** Hover states expected; smaller targets OK (28pt floor); precise click areas.
- **Windows:** Resizable, minimizable, full-screen; remember window size/position when reasonable.
- **Sidebars:** Persistent hierarchy with selection highlight; resizable dividers.
- **Drag and drop:** First-class for reordering, file attach, cross-app transfer; always offer non-drag fallback.

---

### Foundations

#### Accessibility

- **VoiceOver / screen readers:** Every control has a label; decorative icons `aria-hidden`.
- **Dynamic Type:** Text scales with user settings — use `rem`, `clamp()`, test at 200% zoom.
- **Contrast:** WCAG AA — 4.5:1 body, 3:1 large text; provide Increased Contrast variant if needed.
- **Multiple senses:** Never color-only state; pair with icon, text, or shape.
- **Motor:** 44×44pt touch minimum; generous spacing between targets; support Switch Control paths.
- **Cognitive:** Plain language; predictable navigation; undo for destructive actions.
- **Respect system settings:** Bold text, Reduce Motion, Increase Contrast — never override.

#### App icons

- **Simple, recognizable silhouette** — reads at every size from 16px to 1024px.
- **No text in icons** unless essential and localized.
- **Consistent corner treatment** — squircle on iOS; rounded rect on macOS.
- **Light and dark variants** where platform requires; avoid fine detail that disappears small.
- **Brand mark ≠ UI chrome** — icon personality stays in the icon, not duplicated across every screen.

#### Color — Four-Layer System

Move beyond 60-30-10. Complex product interfaces need a structured four-layer color architecture:

**Layer 1: Neutral Foundation**
- Use **multiple subtle background layers** to create depth — distinguish sidebar, main content surface, and elevated cards through lightness, not borders. Aim for 2–4% lightness steps between layers in light mode.
- **Borders**: Avoid thin black lines (`#000` at low opacity). Use soft, high-lightness neutrals (~85–95% white) to define edges without visual noise. A border should be felt, not seen.
- **Lose the lines**: Many borders and dividers can be eliminated entirely — spacing alone creates separation. When items are tightly packed and need distinction, use subtle alternating background tints instead of lines between rows. **Line dividers done well**: If you do use lines, make them intentional — rounded caps, low-opacity (~10–20%), and placed only between major content groups (not between every row). A single thin line with rounded ends between sections is a deliberate design choice; a network of hairline borders is noise.
- **Hierarchy through shade**: Darker neutrals for prominent elements (buttons, headings), lighter neutrals for subtext and disabled states. Typography needs at least 3 neutral steps (primary text, secondary text, disabled/placeholder).

**Layer 2: Functional Accents**
- **Scale, not a single color**: Treat brand colors as a scale (100–900) rather than one hex value. Use specific steps for specific roles: 500 for primary actions, 600 for hover, 700 for active/pressed, 200 for soft backgrounds.
- **Double the steps in dark mode**: Dark mode needs more contrast between adjacent shades. If light mode uses 2% lightness differences between steps, use 4–6% in dark mode. Surfaces should **lighten** as they elevate in dark mode (card is lighter than the page background) — the opposite of light mode.

**Layer 3: Semantic Communication**
- **Break the brand for meaning**: When a button deletes data, it is red — never your brand color. Define dedicated semantic tokens for success, warning, error/info regardless of brand palette. These override all other color rules.
- **OKLCH for data viz**: For charts and data visualization, use the **OKLCH color system** instead of HSL or RGB. OKLCH produces consistent perceived brightness across hues — bright green won't appear significantly more neon than blue at the same lightness value. This is critical for accessible data visualization where multiple hues sit side-by-side.

**Layer 4: Automated Theming**
- **Derive themed palettes from neutrals**: Using OKLCH, systematically shift hue while holding lightness and chroma steady. A typical theme derivation: drop lightness by ~0.03 and increase chroma by ~0.02 from the neutral base, then rotate the hue to the target brand color. This produces a thematically consistent set of neutrals without manual tuning.
- **Test every pair in light and dark** — a passing contrast ratio in light may fail in dark.

**Key principle**: Start with neutrals, not brand colors. A well-structured neutral foundation carries 80% of the visual weight. Brand accents are the seasoning, not the meal.

#### Layout

- **8pt grid** — 4 · 8 · 12 · 16 · 20 · 24 · 32 · 44 · 56pt increments.
- **Screen insets:** 16–20pt phone · 20–24pt tablet · scale on desktop.
- **Readable width:** 45–75 characters (~600–720px prose max).
- **Whitespace hierarchy:** micro 4–8pt · intra-group 12–16pt · inter-group 24–32pt · inter-section 40–80pt.
- **Safe areas:** Content never under home indicator or notch.
- **Full-bleed content:** Backgrounds extend to edges; chrome floats above with blur/material.

#### Materials

- **Layering:** Content → controls → modal chrome. Each layer has distinct material.
- **Translucency + blur:** Nav bars, tab bars, sidebars, sticky headers — `backdrop-filter: blur(20px)` at ~80% opacity.
- **Vibrancy:** Text and icons on materials adapt contrast automatically (light-on-dark-blur, dark-on-light-blur).
- **Avoid flat sterile chrome** — subtle depth signals what's tappable vs readable.
- **Web mapping:** `bg-background/80 backdrop-blur-xl` for sticky bars; solid surfaces for cards.
- **Light mode shadows**: Use soft, subtle shadows — if the shadow is the first thing you notice, it is too strong. A card should appear to float naturally, not cast a harsh drop shadow. Prefer `box-shadow` with low opacity (8–15%) and generous blur (12–24px) over dense dark shadows.
- **Dark mode depth**: In dark mode, use **light levels** rather than heavy shadows to create depth. A card sits above a surface by being slightly lighter (lighter gray fill), not by casting a visible shadow. Heavy shadows in dark mode look muddy and artificial.

#### Typography

| Style | Size | Weight | Use |
|-------|------|--------|-----|
| Large Title | 34pt | Bold | Hero, large nav titles |
| Title 1 | 28pt | Bold | Screen titles |
| Title 2 | 22pt | Bold | Section headers |
| Title 3 | 20pt | Semibold | Subsections |
| Headline | 17pt | Semibold | Row titles |
| Body | 17pt | Regular | Reading content |
| Callout | 16pt | Regular | Secondary body |
| Subhead | 15pt | Regular | Supporting labels |
| Footnote | 13pt | Regular | Metadata |
| Caption | 11–12pt | Regular | Legal, badges |

- **17pt body** for content meant to be read.
- **Avoid Ultralight/Thin** — Regular, Medium, Semibold, Bold only.
- **Negative tracking** on large display; neutral on body.
- **One display + one body family**; mono for code only.
- **Kerning large text**: For text above 70–80px, tighten letter spacing to -2% to -4%. At large sizes, default spacing looks disjointed — the visual gaps between letters become more noticeable and need to be reduced.

---

### Patterns

#### Menus

- **Organization:** Frequent items first · 2–3 logical groups · separators between groups.
- **Labels:** Title case · verb-first · no articles ("Add to Cart" not "Add to the Cart").
- **Ellipsis (…)** when action needs more input before completing.
- **Context menus:** Short, relevant list only; mirror items available elsewhere — never exclusive commands.
- **Submenus:** Max one level · ~5 items · avoid deep nesting.
- **Toggled items:** Single label that changes ("Show Map" / "Hide Map").

#### Scroll views

- **Content is the hero** — scrolling is the primary navigation mode on phone.
- **Scroll edge effects:** Subtle blur/fade as content passes under chrome.
- **Pull-to-refresh:** Branded indicator; don't block content during refresh.
- **Pagination vs infinite scroll:** Infinite for feeds; pagination when position matters (settings, legal).
- **Scroll-linked chrome:** Large titles collapse; toolbars hide on scroll down, reveal on scroll up.
- **Horizontal scroll:** Use for carousels and peekable cards — indicate more content off-screen.

#### Search fields

- **Prominent but integrated** — search bar in nav, command palette (⌘K), or inline filter.
- **Placeholder:** Describes scope ("Search journeys") not generic "Search".
- **Instant results** as user types; debounce 200–300ms for network queries.
- **Recent searches** and suggestions when field is focused and empty.
- **Scope tokens** when searching subsets (Inbox, All, Archived).
- **Cancel/dismiss** always visible when search is active on mobile.
- **Keyboard:** `type="search"`, appropriate `inputMode`; Return submits or selects first result.

#### Sidebars

- **Persistent hierarchy** on iPad/macOS — selection highlighted, badges for counts.
- **Group by relevance** — primary navigation at top, rarely used items (settings, help, admin) at bottom. This creates a natural scannable structure.
- **Active state indicator** — a visible marker (colored rectangle, dot, or background fill) on the currently selected item so the user always knows where they are. Essential for collapsible sidebars where labels disappear.
- **Icons are essential** — if the sidebar collapses to icons-only, every icon must be immediately recognizable. Pair with tooltips for the collapsed state.
- **Collapsible** on compact width — hamburger or split-view toggle restores it.
- **Resizable** divider on macOS/iPadOS where appropriate.
- **Width:** Comfortable label truncation; icons + labels at full width, icons-only when collapsed.
- **Drag-and-drop** between sidebar and detail for organization tasks.

#### Presentation (modality)

- **Sheets (iOS):** Partial-height for quick tasks; full-screen for immersive focus. Swipe down to dismiss.
- **Popovers:** Contextual panels anchored to triggering element — desktop and iPad primary pattern.
- **Alerts:** Critical info or destructive confirmation only — max 2–3 buttons, destructive never primary style.
- **Full-screen covers:** Media, onboarding, focused multistep flows.
- **Never stack modals.** Warn before discarding user-entered content on dismiss.
- **Name the task** in title — user always knows where they are.

---

### Components

Apply HIG component roles alongside project design tokens:

| Component | Rules |
|-----------|-------|
| **Buttons** | One primary (filled accent) per view · verb labels · loading state inside · scale(0.97) press |
| **Toggles / switches** | Immediate effect · label describes ON state · never require Save for toggle |
| **Segmented controls** | 2–5 mutually exclusive options · equal width segments · short labels |
| **Sliders** | Live preview of value · numeric label optional · haptic/step feedback on mobile |
| **Progress indicators** | Determinate when duration known · indeterminate only when unknown · never block entire UI |
| **Activity indicators** | Inline with content being loaded · branded color OK · pair with skeleton layout |
| **Labels / badges** | Don't truncate critical info · badges for counts, not decoration |
| **Lists / tables** | Short row text · sortable columns · alternating rows in wide tables · swipe actions on mobile |
| **Cards** | Group related content · one primary action · entire card should be clickable if it represents a link or destination · subtle hover effect (fading arrow, scale bump) signals interactivity · hairline border or subtle elevation — not both heavy |
| **Tab bars** | 3–5 tabs · icon + label · persist selection state · never use for actions (only navigation) |
| **Toolbars** | Contextual actions for current view · most important trailing on iOS, leading on macOS |

---

### Inputs

- **Single column** on phone — full-width fields, labels above.
- **Placeholder ≠ label** — always visible or floating label; placeholder shows example format.
- **Inline validation** — blame-free, actionable ("Use at least 8 characters").
- **Keyboard type** matches content — `email`, `numeric`, `tel`, `url`.
- **Return key:** "Next" between fields · "Done"/"Go" on last field.
- **Secure fields:** Show/hide toggle · never disable paste on password fields.
- **Pickers / date:** Use native or native-like wheels/menus; avoid free-text for bounded choices.
- **Text areas:** Auto-grow with content; pin primary CTA above keyboard on mobile.
- **Disabled state:** Reduced opacity + `pointer-events: none` — never look identical to enabled.
- **Focus order** follows visual order; visible focus ring for keyboard users.
- **Chip padding ratio**: For chip components (tags, filters, categories), set vertical padding to half or a quarter of horizontal padding. A chip with 16px horizontal padding should have 4–8px vertical padding. This creates the compact, non-button appearance that distinguishes chips from buttons.

---

### Technologies (web & cross-platform mapping)

| Apple concept | Web / React implementation |
|---------------|---------------------------|
| Safe areas | `env(safe-area-inset-*)`, `100dvh` |
| Dynamic Type | `rem`, `clamp()`, `@media (prefers-contrast)` |
| Materials / blur | `backdrop-filter: blur(20px)`, `bg-*/80` |
| Haptics | `navigator.vibrate()` (limited) · RN haptic modules |
| Dark mode | `prefers-color-scheme`, `.dark` class, semantic CSS vars |
| Reduce motion | `prefers-reduced-motion: reduce` — fade not slide |
| VoiceOver | `aria-label`, `role`, live regions |
| Tab bar | Bottom nav, 44px min height, icon + label |
| Navigation stack | Route transitions, back button, breadcrumbs |
| Sidebar | CSS grid / flex split view, collapsible panel |
| Command palette | ⌘K modal search, keyboard-navigable results |
| Sheets | Bottom drawer / dialog with swipe dismiss |
| SF Pro | `-apple-system`, Inter, system-ui substitutes |

---

### Presentation & experience

**Experience principles** — how the product *feels* over time:

| Dimension | Guidance |
|-----------|----------|
| **First launch** | Communicate value in first 3 seconds; delay permissions and ratings |
| **Onboarding** | Teach by doing, not reading; progressive hints at moment of first use |
| **Loading** | Skeleton mirrors final layout; optimistic UI for reversible actions |
| **Empty states** | Explain what belongs here + one CTA — onboarding moment, not void |
| **Errors** | Inline, specific, recoverable; never blame the user |
| **Success** | Brief confirmation — toast or inline check; don't block flow |
| **Transitions** | Spatial continuity — user knows where they came from and where they are |
| **Personalization** | Defaults are sensible; ask preferences in context, not at launch |
| **Trust** | Transparent data use; destructive actions require confirmation |
| **Delight** | Earned through craft — not confetti; motion serves feedback, not decoration |

**Three questions every screen must answer instantly:**
1. **Where am I?** — title, nav highlight, breadcrumb
2. **What can I do?** — primary action obvious, secondary discoverable
3. **Where can I go next?** — clear exit, back, or forward path

---

### HIG non-negotiables

| Rule | Value |
|------|-------|
| Touch target minimum | 44×44pt (44px web) |
| Body reading size | 17pt / 17px |
| Layout grid | 8pt base unit |
| Screen edge inset | 16–20pt phone, 20–24pt tablet |
| Primary buttons per view | 1 filled accent maximum |
| Dark mode | Semantic tokens — not color inversion |
| Motion | Respect `prefers-reduced-motion` |
| Safe areas | `env(safe-area-inset-*)` on full-screen mobile views |

### Whitespace quick reference

```
4px   — icon ↔ label
8px   — related inline items
12px  — form field stack gap
16px  — card padding (mobile), screen margin
24px  — section gap within screen
32px  — major group separation
44px  — minimum control height
```

### Pre-ship HIG checklist

- [ ] 44pt touch targets on all actions
- [ ] Safe area insets applied
- [ ] Body text ≥ 17px for reading content
- [ ] One primary button per view
- [ ] Semantic colors adapt to dark mode
- [ ] Empty, loading, error states designed
- [ ] `prefers-reduced-motion` respected
- [ ] Focus rings visible for keyboard users
- [ ] User can answer: where am I / what can I do / where next
- [ ] Modals dismissible; destructive never primary
- [ ] Search, menus, and sidebars follow pattern rules above

## When to Use

Use this skill when:
- Building websites, landing pages, or dashboards
- Creating React components, HTML/CSS/JS interfaces
- Building React Native mobile app screens and components
- Styling or beautifying existing web or mobile UI
- Designing web artifacts, posters, or interactive pages
- The user wants creative, non-generic frontend work
- Designing mobile-first layouts, login/onboarding, or native-feeling web/macOS UI
- User mentions Apple HIG, SF Pro rhythm, safe areas, or 44pt targets

Do not use this skill when:
- The task is purely backend logic without UI
- The user explicitly requests generic/standard bootstrap-style designs
- The task is only about functionality with zero design consideration
- Building native mobile apps using Swift/Kotlin (use when React Native instead)

## Inputs

- User requirements: component, page, application, or interface to build
- Optional context: purpose, audience, technical constraints
- Target platform: web (React, Vue, vanilla), mobile (React Native), or both
- Framework preference: React, Vue, vanilla HTML/CSS/JS, React Native, Expo, etc.
- Performance budget: any speed/weight constraints

## Workflow

0. **Platform ergonomics** — For mobile, auth, onboarding, or macOS-style UI: apply the **Apple Human Interface Guidelines** section above. Merge HIG spacing/targets with project tokens (e.g. `docs/design/DESIGN.md`) if present.

1. **Design Thinking Phase** — Before coding, understand context and commit to a BOLD aesthetic direction. Run each decision through the Foundational Design Principles above:
   - **Brand colors**: Ask the user for their brand colors (or have them pick from 2-3 suggestions). If they have none, propose a direction: pull from the product's subject matter (medical = clean blues, gaming = saturated neons), industry convention, or an adjacent successful product's palette. Then build a **four-layer color system**: neutrals (backgrounds, borders, text hierarchy) → functional accent scale (100–900 for interactive states) → semantic tokens (success/warning/error) → themable outputs. Neutrals first, brand accents second.
   - **Purpose**: What problem does this solve? Who uses it? Does every feature earn its place, or does it waste the user's time/attention/trust?
   - **Agency & Forgiveness**: Where does the user have control? Can they undo mistakes? What happens if they go off the intended path?
   - **Safety & Responsibility**: Could any feature be misused or cause harm? How does the UI protect privacy and prevent errors?
   - **Familiarity & Consistency**: What metaphors or conventions can you borrow? Do elements that look the same behave the same?
   - **Flexibility & Accessibility**: What contexts will people use this in? How does it adapt across devices and abilities?
   - **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian
   - **Constraints**: Technical requirements (framework, performance, accessibility)
   - **Narrative & Storytelling**: What story does this interface tell? How does every visual choice — imagery, motion, layout — contribute to a cohesive narrative that communicates value?
   - **Brand Expression vs Convention**: Where does the design follow platform conventions for comfort, and where does it intentionally break away to express brand identity? Is the design a unique "place" people want to inhabit, not just a logical tool?
   - **Strategic Rule-Breaking**: Has the design language become predictable or boring? Is there an opportunity for a calculated, bold shift that revitalizes user perception — or is the current aesthetic still fresh enough to keep?
   - **Brand Ethos & Values**: What does this product stand for beyond its features? What feeling or lifestyle does it enable? Connect with users through a shared philosophy, not just utility.
   - **Differentiation**: What makes this UNFORGETTABLE? Define a simple, bold visual signature that makes the app instantly recognizable.
   - **Three Core Navigation Questions**: Can a user immediately answer "Where am I?", "What can I do?", and "Where can I go from here?" — if not, simplify the navigation structure until they can.
   - **Form Follows Function**: Start with constraints, ergonomics, and user goals — don't begin with styling. Define the functional requirements deeply enough and the form emerges naturally.
   - **Sketch user flows on paper first**: Before opening Figma or writing code, sketch the user journey across screens. Identify gaps — missing navigation, absent skip buttons, empty states not designed, search bars forgotten. Paper sketches are cheap to change and reveal structural problems before pixels are involved.
   - **Skip buttons** — every interstitial, onboarding step, or tutorial must have an obvious skip/dismiss option. Forcing users through content they don't need violates agency.
   - **Muscle Memory**: Can key actions become intuitive through repetition? Design for gradual learning — major UX changes should be introduced progressively so users build muscle memory over time.

2. **Implementation Phase** — Build working code that is:
   - Production-grade and functional
   - Visually striking and memorable
   - Cohesive with a clear aesthetic point-of-view
   - Meticulously refined in every detail
   - Polished with micro-interactions (press states, motion, haptics where applicable)

3. **Polish & Refinement Phase** — Layer on the premium details that separate a good app from a great one:
   - Add press-state feedback (scale, opacity, or spring animations on every tappable element)
   - Introduce subtle motion (cross-fades, staggered reveals, native transitions)
   - Integrate haptic feedback for key interactions (platform-permitting)
   - Handle keyboard behavior gracefully (dismissal, avoidance, animated follow)
   - Craft loading and empty states as intentional design moments
   - Review against all 8 Foundational Design Principles — does every decision serve a purpose, give agency, feel familiar, etc.?

4. **Verification Phase** — Verify against the Quality Bar below and the **Pre-ship HIG checklist** in the Apple HIG section.

## Output Format

Functional, production-ready frontend code (HTML/CSS/JS, React, Vue, React Native, etc.) that:
- Is complete and runnable
- Has a distinctive, non-generic aesthetic
- Includes all necessary styling and interactive elements
- Implements the premium polish elements appropriate to the platform

## AI-Assisted Mockups & Presentation

Use AI image generation to produce high-fidelity context-rich mockups that present your UI in realistic environments — a complement to, not replacement for, the coded interface.

### Mockup Prompt Technique
- **Describe device + environment + lighting**: "A MacBook Pro on a walnut desk with a ceramic coffee mug, soft window light, shallow depth of field." Specific environments (orange faux leather chair, concrete floor, moody natural light) produce more credible results than generic "on a desk."
- **Include aesthetic modifiers**: "Soft shadows, blurred background, warm tone, 85mm lens" — these tell the AI to produce the photographic quality that sells the mockup.
- **Generate the base scene first**, then composite your UI screenshot onto the screen area. AI-generated screens are rarely pixel-accurate; overlaying your real UI guarantees fidelity.

### AI for Atmospheric Details
- Use AI to generate environmental texture that's tedious to create manually — fabric wrinkles, surface scratches, water stains, concrete cracks, wood grain. These small imperfections are what make a mockup feel like a photograph rather than a render.

### Combine Mockups with Prototyping
- Use the AI-generated environment as the hero image for client presentations, portfolio case studies, or marketing landing pages.
- Pair it with a **functional prototype** (Figma, Framer, or coded interactive demo) that demonstrates real interactions — swipe gestures, modal transitions, hover states, animations. The mockup sells the context; the prototype sells the experience.
- The gold standard: a hero section showing the UI in a lived-in environment, linked to a clickable prototype or video walkthrough. Clients believe what they can see in context.

### E-Commerce Specific
- For product pages, generate mockups showing items in realistic use settings (a shirt on a person in natural light, a gadget on a desk with accessories). The difference between a white-background product shot and a contextual lifestyle image is often the difference between browsing and buying.

### AI Code-to-Design Workflow
Generate real UI code with AI, then bring it into design tools for refinement.

- **Reference selection**: Provide the AI with a clean, professional reference (Linear, Notion, Superhuman) to guide the aesthetic. Avoid overly complex Dribbble shots — too many conflicting details confuse AI output.
- **Component libraries**: Use platforms like 21st.dev for pre-made AI-ready components. Copy the code or the prompt directly to maintain high design standards.
- **Prompt structure**: Ask the AI for HTML+CSS (not vague "design"), clearly state the purpose ("project management dashboard with sidebar, navbar, Gantt chart"), and specify the icon library ("use Lucide icons, not emojis").
- **Figma conversion**: Download the AI output as an HTML file, then use the Figma plugin "html.to.design" to import it. Toggle "components" and "hover effects" in the import settings to preserve interactivity.
- **Post-AI polish**: AI output needs manual refinement — fix line heights and spacing, adjust colors for cohesion (e.g., shift purples toward your brand blue), ensure background contrast is balanced, and replace placeholder data with real values.

### 3D & Immersive Design

3D elements elevate perceived value — users often find 3D visuals so engaging that they overlook minor UI imperfections.

- **No-code 3D tools**: Spline (Figma-like interface, lowest barrier to entry) and Blender (full-featured, steeper learning curve) are the primary tools. Dedicate a few hours to learning the basics — the skillset differentiates you from designers who only work in 2D.
- **Standard pipeline**: Start with vector assets (SVGs) in Figma → import into 3D tool for extrusion, texturing, and animation → export as optimized web formats (glTF, USDZ) or Lottie. This keeps the design workflow clean and the assets portable.
- **Use 3D to reduce UI chrome**: A hero section with a compelling 3D scene needs less traditional UI decoration — the 3D asset carries the visual weight. Let the 3D element replace decorative backgrounds, illustrations, or hero imagery rather than adding it on top of an already busy layout.
- **Performance is non-negotiable**: Complex 3D must be mobile-optimized. Reduce polygon counts, use compressed textures, and test on mid-range devices. If the 3D element drops frame rate below 60fps, simplify or replace it.
- **Progressive enhancement**: Load a static fallback (image or low-poly preview) first, then upgrade to the full 3D experience on capable devices. Never block content behind a 3D loading state.

## Frontend Aesthetics Guidelines

Apply these guidelines through the lens of the Foundational Design Principles — every aesthetic choice should serve the purpose, feel familiar yet fresh, and simplify rather than complicate.

- **Typography**: Choose beautiful, unique fonts from Google Fonts. Avoid Arial, Inter, Roboto. Pair distinctive display fonts with refined body fonts. Make unexpected, characterful choices. Always include the Google Fonts import link in HTML/CSS. Prefer system text styles (title, body, caption, headline) that form a clear hierarchy and scale proportionately when users adjust their reading size. Avoid Ultralight/Thin weights; prefer Regular, Medium, Semibold, or Bold. Minimize number of typefaces per interface.

  **Typographic Scale**: Define a modular type scale using a ratio — 1.25 (perfect fourth) or 1.333 (perfect fifth). 6-step example: Display (2.027rem), H1 (1.802rem), H2 (1.602rem), H3 (1.424rem), Body (1rem), Small (0.889rem), Caption (0.79rem). Assign line-height per tier — headings 1.0–1.2, body 1.5–1.7, caption 1.3–1.4. Set letter-spacing tighter for larger text, looser for smaller. Store as design tokens / CSS custom properties. On web, use `clamp()` for fluid type: `font-size: clamp(1rem, 0.5rem + 2vw, 2rem)`. Test every size at 200% zoom for no truncation.

  **Font Loading & Performance**: Preload critical fonts via `<link rel="preload">` with `crossorigin`. Use `font-display: swap` in `@font-face` so fallback text renders immediately then swaps. Subset fonts to needed glyph ranges. Prefer variable fonts (single file, multiple weights). For Google Fonts, append `&display=swap` and limit to 2–3 families. Use `size-adjust` in `@font-face` to normalize fallback metrics and prevent layout shift (CLS).
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables. Dominant colors with sharp accents outperform timid palettes. Prefer **semantic colors** named after their purpose (label, background, separator) rather than their appearance — they auto-adapt to light/dark mode, contrast settings, and accessibility. Avoid hard-coding color values. For Dark Mode, do **not** simply invert colors — adjust hues and saturation so the palette feels refined in both modes, avoiding harsh high-contrast opposites. Test every color in both light and dark environments. A restrained monochrome palette can reinforce a cohesive "monolith" feel — consistent material integrity keeps focus on form over decoration.
  - **Use OKLCH for color systems**: Where possible, author color scales in OKLCH (OKLAB Lightness, Chroma, Hue) instead of HSL or RGB. OKLCH produces consistent perceived brightness across hues — a blue and a green at the same L value appear equally luminous. This is essential for data viz, theming, and dark mode derivation. Tools: `culori` (JS), `colorjs.io`, OKLCH color picker at oklch.com.

  **Accessibility: Color Contrast & Control Sizes**
  Color contrast is measurable. Every text element must meet minimum contrast ratios for legibility.
  - **WCAG AA minimums**: Body text (<18px): **4.5:1**. Large text (≥18px): **3:1**. Bold text ≥18px: **3:1**.
  - If your palette doesn't meet these, provide an **Increased Contrast** variant that does.
  - Thin/ultralight font weights need larger sizes to pass contrast ratios. Prefer Regular/Medium for body, Semibold/Bold for headings.
  - Test every text+background pair in both light and dark modes. A passing ratio in light may fail in dark.
  - Use a contrast calculator (WebAIM, APCA) to verify during design.

  **Minimum tap target sizes**:
  | Context | Default | Absolute minimum |
  |---------|---------|------------------|
  | Touch (mobile) | 44×44px | 28×28px |
  | Pointer (desktop) | 28×28px | 20×20px |
  - Spacing between controls is as important as size. Add ~12px padding around bordered elements, ~24px around borderless ones.
  - Never rely on color alone to convey state — pair with shapes, icons, or text labels (green circle + checkmark, red octagon + X).
  - For data viz: allow users to customize chart colors so they can adapt to their needs.
  - Test with color blindness simulators (devtools, extensions) — red-green and blue-orange pairs are most problematic.
- **Motion**: Mirror real-world physics — weight, momentum, friction, scroll bounce make interfaces feel alive and intuitive. Use animated transitions to create **spatial continuity**, helping users map where they are within the app (the interface should feel like a coherent space, not disconnected screens). Prioritize CSS-only for performance. One well-orchestrated page load with staggered reveals creates more delight than scattered micro-interactions. Use purposeful video or movement to re-engage users after long text sections and guide them naturally down the page — never animate just for the sake of it.

  **Motion Principles** (apply across GSAP, Framer Motion, CSS animations):
  - **Purposeful** — every animation must serve a function: convey status, provide feedback, guide attention, or enrich the experience. If removing it doesn't change understanding, cut it. Gratuitous motion distracts and can cause physical discomfort.
  - **Gesture-aligned** — motion should follow user expectations and gestures. If someone reveals a panel by sliding it down, they expect to dismiss it by sliding it down, not sideways. Realistic feedback motion helps people understand how things work.
  - **Brief & Precise** — micro-interactions: 100–200ms. Element transitions: 200–300ms. Page transitions: 300–400ms. Nothing over 500ms absent a deliberate reason. Short, precise animations feel lightweight and unobtrusive.
  - **Cancellable** — never force people to wait for an animation to complete before they can act, especially if they see it repeatedly. Let them interrupt or skip.
  - **Optional** — never use motion as the only way to convey information. Respect `prefers-reduced-motion`. When Reduce Motion is active: tighten animation springs to reduce bounce, track animations to gestures directly, avoid z-axis depth changes, replace movement transitions with fades, and avoid animating into/out of blurs.
  - **Physics-based** — use spring curves (high stiffness, low damping), not linear transitions or ease-in-out. Real-world momentum and friction make interfaces feel alive, not mechanical.

  **Implementation**:
  | Pattern | GSAP | Framer Motion | CSS |
  |---------|------|---------------|-----|
  | Staggered reveals | `gsap.fromTo(els, {opacity:0,y:20}, {stagger:0.05})` | `staggerChildren: 0.05` | `transition-delay` per child |
  | Shared-element / layout | `Flip` plugin | `layoutId` prop | `view-transition-api` |
  | Scroll-triggered | `ScrollTrigger` plugin | `useInView` + `whileInView` | `IntersectionObserver` |
  | Morph / path animation | `MorphSVGPlugin` | `motion.path` | SMIL / SVG animations |
  | Spring physics | `gsap.to(el, { ease: "back.out(1.7)" })` | `type: "spring", stiffness: 300, damping: 20` | `cubic-bezier(0.34, 1.56, 0.64, 1)` |
  | Timeline sequencing | `gsap.timeline()` | `useAnimation()` + sequence | `@keyframes` + animation-delay |
  | Scroll-driven (native) | ScrollTrigger + matchMedia | `useInView` + thresholds | `animation-timeline: view()` |
  | Text reveal | `SplitText` plugin | `motion.span` stagger | CSS `@keyframes` per word via `--i` |

  **Advanced CSS patterns:**
  - **View Transitions API** — cross-page shared-element morphs for MPAs: `@view-transition { navigation: auto; }` + `view-transition-name` on elements. Eliminates hard page cuts in traditional multi-page sites.
  - **CSS Scroll-Driven Animations** — off-main-thread scroll reveals: `animation-timeline: view(); animation-range: entry 0% entry 35%`. No JS needed for scroll-linked entrance effects.
  - **CSS `linear()` easing** — native spring curves without JS: use `linear()` function for realistic overshoot on press states, card hover, toggles. Generate via linear-easing-generator.netlify.app.
  - **IntersectionObserver + stagger** — universal scroll-triggered reveals at 97%+ browser support. Use `threshold: 0.15, rootMargin: '0px 0px -50px'` + `setTimeout` stagger per element index.
  - **FLIP technique** — animate layout changes CSS transitions can't handle: measure First/Last bounds, Invert with transform, Play with WAAPI `element.animate()`. The engine behind Framer Motion `layout` and GSAP `Flip`.
- **Spatial Composition**: Confident use of white space to let content breathe. Layouts grounded in a grid system but with experimental, staggered, or masonry arrangements — structured yet exploratory. Use mathematical ratios like the golden ratio for spacing and proportions to create subconscious visual harmony. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density. When stuck on layout, return to Swiss Design fundamentals: clarity, objectivity, grid-based organization.
- **Backgrounds & Visual Details**: Humans evolved to read the world through shading, reflections, and light variations — interfaces that incorporate these natural cues (gradients, shadows, translucency) feel more comfortable than completely flat, sterile designs. Use multi-color gradients strategically (like Instagram's light-reflection technique) to create a distinct, vibrant visual language rather than simple single-color shading. Gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, grain overlays.
- **Marketing Moments & Narrative Storytelling**: Incorporate large, impactful visual moments (hero sections, 3D renders, full-bleed imagery) with smooth transitions to tell a story and emphasize your brand or product. Don't rush users to content — use immersive narrative sequences to build understanding and desire. Every visual asset should contribute to the story.
- **Squircle & Continuous Curvature**: Use true superellipse ("squircle") geometry instead of basic rounded rectangles for icons, cards, and containers. Standard `border-radius` has a hard breakpoint where the straight edge meets the circular corner; a squircle has G2 continuity — a constantly changing radius that produces a seamless, organic curve. Humans inherently prefer curved forms (perceived as safer, less threatening). Curves also guide the eye toward content center rather than pulling focus to corners. Mirror the physical curvature of the device hardware in your UI for systemic cohesion. Use corner smoothing tools (Figma's corner smoothing, `squircle-js`, CSS `mask-border`) to apply consistent curvature across all components. The effect is most noticeable with larger radii (>12px for icons).
- **Monolith Unity**: The interface should read as one cohesive, solid object — not a collection of disjointed panels, cards, and sections. Use continuous surfaces (smooth transitions between sections), harmonized details (align and group related controls into single clean elements), and consistent material treatment throughout. A unified visual mass communicates stability and premium quality.
- **Strategic Sharp Cuts**: Squircle curves signal approachability; sharp edges and straight notches signal precision and performance. Use intentional hard lines to indicate actionable areas (where to tap, swipe, or open) and to add a sense of technical refinement. The contrast between continuous curves and deliberate sharp cuts creates visual tension that guides behavior.
- **Iconography**: Use platform icon libraries or an icon set (e.g., Lucide, Phosphor, Material) for consistency — icons should auto-align with text across all weights and sizes. Prefer platform-standard glyphs for common actions (share, search, bookmark) over custom icons. Maintain visual consistency across all icons in the same interface: same stroke weight, scale, and perspective.

  **Icon Design Principles** (for custom icons):
  - **Simplicity** — a recognizable, simplified design beats detail. Use familiar visual metaphors directly related to the action. Prefer filled, overlapping shapes with transparency for depth. Avoid thin line weights (<1.5px) and sharp corners — they lose detail at small sizes.
  - **Visual consistency** — all icons must share the same stroke thickness, scale, perspective, and level of detail. Match icon weight to adjacent text weight. Adjust individual icon dimensions for optical balance (a visually light icon needs to be slightly larger).
  - **Optical centering** — geometric centering often looks off. Asymmetric icons (download arrow, share) require 1–4px positional adjustments. Add invisible padding to the lighter side so content appears centered.
  - **Text in icons** — avoid unless essential. Text doesn't localize, is unreadable at small sizes, and adds clutter. If including a character, provide localized and RTL-flipped variants.
  - **Inclusive iconography** — prefer gender-neutral figures. Avoid culture-specific imagery. Use SVG/PDF for scalability. Provide alternative text labels (aria-label/accessibilityLabel) for every custom icon.

## Platform-Native Patterns

Beyond visual polish, a truly native-feeling app follows platform-level UX patterns that make it feel like a seamless part of the user's system rather than a standalone window. Separate UI chrome from content structurally — the UI layer should use standard components people recognize, while the content layer is where brand identity and visual personality live.

### App as a System, Not a Destination
Don't build a self-contained, full-screen window that the user navigates to. Design your app to appear **exactly where and when the user needs it**, then disappear. Use:
- **Popovers** and panels that attach to relevant UI elements
- **Notifications** for timely, actionable information
- **Keyboard-triggered widgets** or command palettes (Ctrl+K / Cmd+K, spotlight-style search) that overlay the current context
- **Menu bar / toolbar** integration for quick access without launching the full app

The goal: the app feels like an extension of the OS, not a detour.

### Content-First Design & Progressive Disclosure
Ask: what is the **minimum UI** needed for the content to shine? Strip toolbars, sidebars, and chrome to essentials. Use **progressive disclosure** to hide complex controls until the user signals they need them — reveal filter bars on a click, expand advanced settings behind a chevron, show formatting tools on text selection. This keeps the default state clean while power remains accessible.

### Keyboard-First (Desktop)
On desktop, every major action should have a keyboard shortcut. Provide clear visual feedback on shortcut activation (micro-animations or state changes so the user knows input registered). Document shortcuts in menus and expose them during onboarding. This is the hallmark of power-user-friendly applications.

### Search & Navigation
Make search prominent but keep it **integrated** — a floating search bar, a slide-out preview panel, or a command palette. For simple apps, skip the sidebar entirely to save space for content. Use inline search that reveals results in context rather than navigating to a separate search page.

### Onboarding
Even desktop and web apps benefit from a brief onboarding flow. Your first screen should immediately communicate care, quality, and trust — not just a logo splash. Don't just show a welcome screen — teach users about powerful, **hidden features** they'd otherwise miss (keyboard shortcuts, drag-and-drop, gestures).

- **Teach through interactivity** — let people learn by doing, not reading. An interactive demo where they perform the actual action beats a tutorial every time.
- **Use progressive onboarding** — context-sensitive hints revealed at the moment of first use, not everything upfront.
- **Postpone nonessential setup.** Use reasonable defaults. Ask for preferences when they become relevant, not at launch.
- **Design for the user, not the pro.** Never assume users know your industry's conventions. Design flows that feel intuitive to an everyday person.
- **Delay ratings and purchase prompts** until people have had a real experience with the product.

### Guided Behavior
Train users through visual hints and design patterns rather than tutorials. Simple, unobtrusive cues — subtle animation on first-use, contextual tooltips, faded secondary actions that reveal on hover — teach navigation over time without interrupting flow. Users learn best by doing, not reading.

### Content Organization
Organize content to guide people to what matters most. Three strategies for grouping complex data:
- **Time**: Recent, seasonal, or chronological groupings feel natural (e.g., "This Week", "Last Month")
- **Progress**: Group by completion state, continuing where the user left off
- **Patterns**: Related items, categories, or themes reduce choice overload

**Lists vs Collections**: Use **lists** for structured information that needs quick scanning (text-heavy, sortable data). Use **collections** (grids) for visual-heavy content (images, products, media). Don't mix both content types in the same section without clear separation.

**List & Table best practices**:
- **Keep text succinct** — short items minimize truncation and oversized rows. Prefer title + detail on tap over bloated rows.
- **Use descriptive column headings** — nouns or short noun phrases, no ending punctuation.
- **Make columns sortable and resizable** — click a heading to sort, drag to resize. Re-sort in opposite direction on second click.
- **Alternating row colors** in wide multi-column tables help track values across columns.
- **Support editing** — reordering alone adds value. Animate insert, delete, and reorder so changes are clear.
- **Row feedback differs by purpose** — persistent highlight for navigating a hierarchy, checkmark for toggling states.

## Modal Patterns

Modality presents content in a dedicated mode that prevents interaction with the parent view. It interrupts context, so use it deliberately.

### When to use modals
- **Critical information** requiring immediate attention
- **Confirmation** before destructive or irreversible actions
- **Narrow, bounded tasks** — editing a single item, composing a message, setting a filter
- **Immersive focus** — viewing media, marking up content, a focused multistep flow

### When NOT to use modals
- For navigation hierarchies — if a task requires browsing multiple levels, it's not a modal
- For content reference — don't cover up the context people need to do their task

### Modal best practices
- **Keep modal tasks simple and short.** If it feels like an app within your app, it's too complex.
- **Always provide obvious dismissal** — a close button, swipe-down gesture, or Escape key. Never trap people in a modal.
- **Name the task clearly** with a title or descriptive text so people know where they are.
- **Never stack modals** — dismiss one before presenting another. Multiple overlapping modals create cognitive chaos.
- **Warn before data loss** — if closing discards user-generated content, confirm before dismissing.

## Button Design

Buttons combine style, content, and role to communicate their function clearly.

### Hierarchy & Roles
- **Use style, not size, to differentiate importance** in a group — same-size buttons signal coherent choices. Use filled/colored for the primary action, outline or text for secondary.
- **Limit prominent buttons to 1–2 per view** — too many competing primaries increase cognitive load.
- **Button roles**: normal, primary (most likely choice), cancel, destructive. **Primary must never be destructive** — people tap prominent buttons without reading.
- **Always include a press state** for custom buttons — without one the button feels dead.

### Sizing & Layout
- **Minimum hit target**: 44×44px for touch, 60×60px for gaze/hover-based interfaces.
- **Provide enough spacing** around buttons to distinguish them from surrounding elements.

### Labels & Feedback
- **Button labels start with a verb** — "Add to Cart" not "Cart". Use title-style capitalization.
- **Show an activity indicator inside the button** for async actions. Update the label to reflect loading state ("Saving...").
- **The primary button should respond to Return/Enter** by default, making confirmation fast.

## Menu Patterns

Menus present commands and options efficiently. Consistency is key — most people already know how to use them.

### Context Menus
- **Prioritize relevancy** — include only commands users are most likely to need right now. Keep the list short.
- **Be consistent** — support context menus everywhere or nowhere. Inconsistency confuses.
- **Always mirror items in the main interface** — never offer commands exclusively in a context menu.

### Menu Organization
- **Frequently used first** — people scan from the top. Put priority items there.
- **Group logically with separators** — aim for 2–3 groups max per menu. More impedes scanning.
- **Keep menus short** — if too long, split into separate menus or use submenus.

### Menu Labels
- **Use title-style caps** — capitalize every word except articles, conjunctions, short prepositions.
- **Start with a verb** — short verb phrase that describes the action.
- **Skip articles** — remove "a", "an", "the". They add length without clarity.
- **Append ellipsis (…)** when the action needs more information before completing.

### Submenus & Toggled Items
- **Use submenus sparingly** — max one level deep, ~5 items max. Each level adds complexity.
- **Toggled items**: use a changeable label ("Show Map" / "Hide Map") instead of two separate items. Add a verb if the label alone is unclear.
- **Icons**: all-or-nothing within a group. Use purposefully to speed recognition — skip icons that don't clearly represent the action.

## UX Writing & Microcopy

The words inside the interface are as important as the visuals. Every string is a design decision that affects clarity, trust, and usability.

### Voice & Tone
- **Define your app's voice upfront.** Write a brief voice charter (3–5 adjectives: authoritative, playful, warm, technical) and reference it for every string.
- **Match tone to context.** Vary within your voice: errors are direct and blame-free, celebrations are warm, onboarding is encouraging. A fitness app energizes; a banking app conveys stability.
- **Be clear above all.** Choose plain, simple words. Read every string aloud — if awkward spoken, rewrite. Cut unnecessary words ruthlessly.

### Action-Oriented Labels
- **Use verbs for buttons and links.** "Send" beats "Let's do it!" "Learn more about X" beats "Click here." Verb-first labels help screen reader users.
- **Label for the next step.** In multi-step flows, use "Get Started", "Continue", "Next" consistently. Signal completion with "Done". Never switch terminology mid-flow.
- **Avoid possessive pronouns by default.** "Favorites" is shorter than "Your Favorites" and means the same. Avoid "we" in error messages ("Unable to load content" not "We're having trouble").

### Writing Error Messages
- **Prevent errors first.** If an error is common, fix the interaction rather than write a better message.
- **Be clear, blame-free, and actionable.** "Choose a password with at least 8 characters" beats "That password is too short" — both beat "Invalid password."
- **Show errors inline** next to the field, not in a distant banner. Avoid "Oops!" or "Uh-oh" — they sound insincere in frustrating moments.
- **Use hint text in fields.** Give examples ("name@example.com") or format descriptions. Errors explain how to fix: "Use only letters for your name" not "Don't use numbers."

### Empty States
- **Guide the next action.** Never show bare "No items." Explain what belongs here and give a clear CTA: "Your saved articles will appear here. Start exploring."
- **Treat empty states as onboarding moments.** Use them to showcase voice and teach value, not just state absence.
- **Empty states are temporary** — don't place critical info there that disappears when content arrives.

### Localization Readiness
- **Write for translation from day one.** Use full sentences with subject-verb-object order. Avoid idioms, puns, culture-specific metaphors.
- **Allow 30–50% text expansion.** German, Russian, Finnish can be 30–50% longer than English. Don't hardcode widths or truncate dynamically.
- **Externalize all strings.** Use i18n libraries (react-i18next, vue-i18n, gettext). Never embed raw text in components.
- **Support RTL layouts.** Use logical CSS properties (`inset-inline-start`, `margin-inline-end`) that flip automatically.
- **Format dates, numbers, currencies per locale.** Use `Intl.DateTimeFormat`, `Intl.NumberFormat` (web) or platform locale APIs (mobile).

## Data Visualization

Charts communicate complex information at a glance while adding visual interest. Every chart decision affects clarity, accessibility, and engagement.

### Choosing Chart Types
- **Bar marks** for comparing values across categories or showing parts of a whole. **Line marks** for revealing trends over time. **Point marks** for inspecting individual values and identifying outliers.
- **Combine mark types** when it adds clarity — overlay points on a line to highlight individual values alongside the trend.
- **Prefer common chart types** — people already know how to read bar, line, and area charts. Novel chart types require teaching through animation or annotation.
- **Match chart size to purpose** — small snapshots for glanceable previews, larger views for detailed analysis with interactive controls.

### Axes & Scale
- **Bar charts: always use zero as Y-axis lower bound** so relative heights are comparable. **Line/point charts**: zero can obscure meaningful differences — choose a range that makes variation visible.
- **Use fixed axis ranges** when specific min/max values are meaningful (e.g., 0–100%). Use **dynamic ranges** when values vary widely and you want marks to fill the plot area.
- **Use familiar tick sequences** (0, 5, 10…) — unfamiliar ones (1, 6, 11…) cost extra mental effort.
- **Tailor grid line density** to context — too many overwhelm, too few make estimation hard. Interactive charts with touch/pointer input can use lighter grids.

### Data Integrity
- **Never rely on color alone** to differentiate data or communicate essential information. Supplement with distinct shapes, patterns, or textures for each series.
- **In stacked bars or contiguous color regions**, add narrow visual separators between areas to help people distinguish segments.
- **Keep charts simple by default**; let users progressively reveal more detail (subsets, perspectives) through controls.

### Descriptions & Accessibility
- **Add descriptive text** — titles, subtitles, annotations, summary headlines. A chart with "Chance of rain in the next hour" is more useful than a bare line chart.
- **Make every chart accessible**: Provide labels describing chart values and components. Offer audio alternatives that audibly represent data trends.
- **Write accessibility labels that match purpose** — summary labels for overview charts (elevation trend over a route), granular labels per mark when exact values matter (daily step counts).
- **Include context in labels** (date, location). Avoid subjective words ("rapidly", "gradually"). Spell out units ("60 minutes" not "60m"). Describe what data represents, not what it looks like.
- **Make charts keyboard-navigable** — let users traverse along the logical axis. For large datasets, allow focus on value subsets.
- **Be consistent across related charts** — same type, colors, annotations, layout. Consistent visual language transfers understanding from one chart to another.

### Interactivity
- **Support touch-to-scrub** — expand hit targets to the full plot area when individual marks are too small to target precisely.
- **Let people interact to explore details**, but never require interaction to reveal critical information — display the main message by default.
- **Provide multiple perspectives** — overview (totals/averages), mid-level (subset comparison), detail (individual data points).
- **Animate data transitions** to help people track changes between states. Also announce changes non-visually for assistive technology.

## Layout Components

### Boxes (Grouping)
- Use bordered or background containers to visually group related content. Keep boxes small relative to their parent — a box that fills the screen defeats its purpose.
- Add a succinct title if it clarifies what's inside. Use padding and alignment for internal subgroups instead of nested boxes.

### Split Views (Multi-Pane Layout)
- Use for navigating a hierarchy: primary pane for top-level items, secondary/tertiary for details. Persistently highlight the current selection in each pane.
- Support drag-and-drop between panes for moving content across hierarchy levels.
- Make columns resizable with dividers. Let users hide panes in editing contexts and provide multiple ways to restore them.

### Labels
- Use a semantic hierarchy (primary, secondary, tertiary) to communicate relative importance through color and weight.
- Make useful text selectable — error messages, locations, IP addresses, serial numbers — so users can copy it elsewhere.

## Inclusive Design

Inclusive design means content and functionality everyone can access and understand, regardless of age, gender, race, ability, language, or culture.

### Welcoming Language
- Address people directly (**you**/**your**), not impersonally (**the user**/**the player**). Reserve **we**/**our** for your company, not to imply a personal relationship.
- Define specialized terms before using them. Replace colloquial expressions ("peanut gallery", "grandfathered in") — they carry exclusionary histories and don't translate.
- Use gender-neutral constructions ("Subscribers can post recipes" not "A subscriber can post his or her recipes"). Prefer nongendered human figures in avatars and icons.
- Avoid humor in UI copy — it's subjective, doesn't localize, and can alienate.

### Representation
- Depict a range of racial backgrounds, body types, ages, and physical capabilities in imagery. Avoid stereotypical occupations (male doctors, female nurses) and hero/villain dynamics that map to real-world power structures.
- Security questions referencing college, car ownership, or specific cultural experiences exclude people. Use universal alternatives ("What's your favorite activity?").
- "Family" depictions should reflect diverse structures, not only a woman + man + biological children.

### Cultural Color Awareness
- Colors carry different meanings across cultures: Red = danger in the West, luck in East Asia, mourning in South Africa. White = purity in the West, death in parts of Asia. Green = nature broadly, but can have political/religious associations.
- If your brand color is culturally sensitive, consider localized color themes or a neutral default with accent color customization.

## Premium Polish Elements

A premium-feeling application is built by stacking small, intentional details. These six elements — inspired by principles from high-quality app development — apply across web and mobile platforms. Adapt the library recommendations to the target stack.

### 1. Press States & Spring Physics

Every tappable element should give immediate tactile feedback. A button that does nothing on press feels dead.

- **Scale feedback**: On press down, scale the element to ~0.94–0.97 with a spring animation. On release, spring back to 1.0.
- **Opacity feedback**: Combine with a slight opacity drop (0.7–0.85) for layered depth.
- **Ripple / highlight**: For native-like feel, use a ripple effect (web: CSS `:active` with transform, RN: Pressable with ripple).
- **Spring physics**: Use natural spring curves — high stiffness, low damping — not linear transitions. Avoid hard instant snaps.

| Platform | Approach |
|----------|----------|
| CSS/Web | `transform: scale()` on `:active` with `transition: transform 0.15s cubic-bezier(0.32, 0.72, 0, 1)` |
| React | Framer Motion's `whileTap={{ scale: 0.95 }}` with spring transition |
| React Native | `Pressable` with `Animated.spring` or the `Presto` package for cross-platform press interactions |

Presto (React Native) handles scale, opacity, and haptic-aware press gestures out of the box. For web, a CSS approach is simpler and more performant.

### 2. Subtle Animations

Do not over-animate. Restraint is the hallmark of premium motion. Use gentle, purposeful motion to guide attention and communicate state.

- **Cross-fade icons**: When toggling icons (play/pause, bookmark, dark mode), cross-fade rather than instantly swapping. A 200–300ms opacity transition is enough.
- **Fade-in sequences**: Images, cards, and screens should fade in gently on mount. Stagger children with 50–100ms delays for a cascading reveal.
- **Native transitions**: On mobile, prefer platform-native transition patterns (zoom-in for modal presentation, slide for push navigation). On web, use shared-element or morphing transitions for element-level navigation.
- **Layout animations**: When items enter/leave a list or grid, animate with `Animated.List` (RN) or `layout` prop (Framer Motion).
- **Duration guidance**: Micro-interactions: 100–200ms. Element transitions: 200–300ms. Page transitions: 300–400ms. Anything over 500ms feels slow.

| Platform | Approach |
|----------|----------|
| CSS/Web | `transition`, `@keyframes`, `view-transition-api` |
| React | Framer Motion `AnimatePresence`, `motion.div` with `initial`/`animate`/`exit` |
| React Native | `ReactNativeEase` package or `LayoutAnimation` for native-grade 60fps transitions |

ReactNativeEase provides drop-in layout animations, cross-fade wrappers, and shared-element transitions tuned to native platform curves.

### 3. Haptics

Tactile feedback builds trust and reinforces that an action was registered. It tells the user "something happened" without requiring visual confirmation.

- **Build clear cause-effect relationships** — each haptic must correspond to a specific action so people learn the association. The same pattern always means the same thing.
- **Complement, don't replace** — haptics enhance visual and auditory feedback, never substitute for it. Match haptic intensity to the animation it accompanies.
- **Submit / confirm**: Light haptic on form submission, setting a toggle, or completing an action.
- **Interactive controls**: Sliders, switches, drag-to-adjust controls — haptic on each discrete step.
- **Error / rejection**: Error haptic pattern on failed actions or invalid inputs.
- **Success / celebration**: Success haptic pattern on achievements, completions, or positive outcomes.
- **Make haptics optional** — let people turn them off. The experience must be complete without them.
- **Avoid overuse** — haptics feel right occasionally but become tiresome when frequent. Test to find the balance.

| Platform | Approach |
|----------|----------|
| Web | `navigator.vibrate(pattern)` (limited, mobile-only in many browsers) |
| React Native | `Pulsar` package for custom and native haptic patterns (supports `impact`, `notification`, `selection` types, with intensity control) |

Use haptics sparingly. Over-use feels gimmicky. Reserve for interactions where the user would benefit from confirmation. Haptic + visual animation together create the strongest feedback loop.

### 4. Keyboard Behavior (Mobile & Form-Heavy Web)

A premium app makes the keyboard feel integrated, not like an obstacle. This applies to any interface with text input.

- **Keyboard-aware layout**: UI elements (especially primary action buttons) should move with or sit above the keyboard — never be hidden behind it.
- **Gesture dismissal**: Support swipe-down or tap-to-dismiss on the keyboard. Blurring the background during keyboard presentation adds depth.
- **Smooth animation**: Keyboard show/hide should animate input fields and surrounding UI synchronously with the keyboard's own animation curve.
- **Focus management**: Auto-focus the first input when a form screen appears. Move focus to the next field on submit (unless it is the final field).
- **Return key label**: Set the return key to "Next" for multi-field forms and "Done" / "Go" for the final field.

| Platform | Approach |
|----------|----------|
| Web | `input` events, `scrollIntoView`, CSS `:focus-within` |
| React | `react-avoiding-keyboard` or manual `scrollIntoView` on focus |
| React Native | `KeyboardAvoidingView` or `ReactNativeKeyboardController` package for animated, gesture-aware keyboard management |

ReactNativeKeyboardController offers gesture-based dismissal (swipe down to blur), keyboard-aware `KeyboardAvoidingView` with matching animation curves, and per-input return-key configuration. For web forms, a simple sticky CTA that scrolls into view on focus is usually sufficient.

### 5. Loading & Empty States

Empty states are not voids — they are opportunities. Loading states set expectations. Together they define the app's personality when there is nothing to show.

- **Empty states as onboarding**: Instead of "No items yet", explain the value: "Your saved articles will appear here. Start exploring to fill this space." Include a clear CTA.
- **Shimmer / skeleton loading**: Use shimmer placeholders that mirror the final content layout. This sets visual expectations and signals "something is coming."
- **Pull-to-refresh**: On mobile, include pull-to-refresh with a branded animation (not the default spinner).
- **Progressive loading**: Fade in content as it loads rather than a hard swap from skeleton to full page.
- **Optimistic UI**: On actions (delete, toggle, submit), update the UI immediately and reconcile with the server in the background.

| Platform | Approach |
|----------|----------|
| CSS/Web | `@keyframes shimmer` with gradient sweep on skeleton placeholders |
| React | Custom skeleton components or `react-loading-skeleton` |
| React Native | `react-native-shimmer` or built-in `ActivityIndicator` wrapped in skeleton layouts |

Treat the empty state as a designed screen, not a default. Consider illustration, branded copy, and a compelling action. The loading state should match the final layout as closely as possible so the user's eyes know where to look when data arrives.

### 6. Drag & Drop

Drag and drop is an intuitive, direct-manipulation pattern for reordering, organizing, or moving content. Support it as a power-user enhancement while always providing non-drag alternatives.

- **Every draggable item announces itself** — cursor change on hover, subtle lift on drag start (scale + shadow). The user should know an item is draggable before attempting to drag it.
- **Visual feedback during drag** — the dragged item follows the cursor/finger with a slight elevation (shadow + scale ~1.02). The drop target highlights with a clear indicator (insertion line, highlighted zone, or outline).
- **Haptic feedback on mobile** — light haptic on pick-up, confirmation haptic on successful drop, error haptic if the drop is rejected.
- **Smooth drop animation** — the item animates to its new position with a spring curve (not instant snap). Surrounding items animate out of the way with layout animation.
- **Always offer non-drag fallback** — context menu "Move to...", keyboard reorder (up/down arrows + Cmd+Shift+arrow), or explicit "Edit order" mode with drag handles.

| Platform | Approach |
|----------|----------|
| CSS/Web | `dragstart`/`dragover`/`drop` events, `@dnd-kit/core` for accessible React DnD |
| React | `@dnd-kit` (modern, accessible, keyboard-support), `react-beautiful-dnd` (legacy) |
| React Native | `react-native-draggable-flatlist` with haptic feedback on pick-up/drop |

## Verification & Quality Bar

Before considering the implementation complete, run through this checklist. Every item must be addressed — even if the answer is "not applicable given scope."

### Core Functionality
- [ ] Does the implementation fulfill the core user requirement?
- [ ] Are all interactive elements functional (buttons, links, forms, toggles)?
- [ ] Does it handle the primary user flow end-to-end without errors?
- [ ] Are there no console errors or warnings in the target environment?

### Responsiveness & Adaptivity
- [ ] Does the layout work at the target breakpoints (mobile, tablet, desktop)?
- [ ] Is content readable without horizontal scrolling on the smallest target device?
- [ ] Are touch targets at least 44×44pt on mobile?
- [ ] Does the layout adapt gracefully between portrait and landscape on mobile?

### Accessibility
- [ ] Are all interactive elements keyboard-accessible (Tab, Enter, Escape)?
- [ ] Do visible focus rings appear when navigating by keyboard?
- [ ] Are all images, icons, and controls labeled (`aria-label`, `alt` text)?
- [ ] Is color contrast WCAG AA compliant for all text (4.5:1 body, 3:1 large)?
- [ ] Is `prefers-reduced-motion` respected — no motion-only information?
- [ ] Has the color-only state check been done? (no green-only success, red-only error)

### Motion & Interactions
- [ ] Do all tappable elements have press-state feedback (scale, opacity, or ripple)?
- [ ] Are transitions purposeful and under 400ms?
- [ ] Is there no gratuitous animation that distracts from functionality?

### States Coverage
- [ ] **Loading state**: Skeleton or spinner shown while content loads.
- [ ] **Empty state**: Meaningful message + CTA when no content exists.
- [ ] **Error state**: Inline, blame-free error message with recovery action.
- [ ] **Edge cases**: Long text, missing data, rapid interactions handled gracefully.

### Polish & Detail
- [ ] Is the typography hierarchy clear and intentional?
- [ ] Are colors harmonious in both light and dark mode (where applicable)?
- [ ] Do shadows, borders, and spacing follow consistent rules?
- [ ] Is the icon set consistent in stroke, weight, and style?
- [ ] Are there hard-coded strings that should be externalized?

### Platform Integration (Apple-aligned / mobile)
- [ ] Safe areas respected (notch, Dynamic Island, home indicator).
- [ ] Keyboard-aware layout (CTA buttons not hidden behind keyboard).
- [ ] Gesture dismissal for modals (swipe down, tap backdrop).
- [ ] Dark mode tested with semantic tokens (not color inversion).
- [ ] Search, menus, sidebars follow HIG pattern rules above.

### Performance
- [ ] Fonts loaded with `font-display: swap` and preloaded.
- [ ] Images lazy-loaded or appropriately sized.
- [ ] No layout shift (CLS) from late-loading fonts or images.
- [ ] 3D / heavy assets have progressive fallback (static image first).

## Appendices

### AI Usage Notes

1. This skill includes content from Apple Human Interface Guidelines. Do not web-search for HIG — the relevant sections are embedded above.
2. When the user mentions specific brands or color palettes, import them as the four-layer color system, not as isolated hex values.
3. The AI-Assisted Mockups section is for presentation/deck work only — the primary deliverable is always working code.
4. Product Design Mindset section should be referenced when the user asks about product strategy, flow, or architecture — not just surface UI.
