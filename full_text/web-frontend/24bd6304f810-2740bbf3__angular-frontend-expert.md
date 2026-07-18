---
name: angular-frontend-expert
description: Expert guidance for designing, implementing, reviewing, and refactoring Angular frontend applications using Angular v20+ best practices, Angular Material, CSS/SCSS, AG Grid, Signal Store, Nx workspaces, accessibility, Angular Aria, Signal Forms, linkedSignal, resource, modern CSS layout, View Transitions, native dialogs, performance patterns, and repo-adaptive unit/integration/e2e testing.
license: MIT
compatibility: Works in Pi and other Agent Skills compatible harnesses. Best used in Angular frontend repositories, Angular CLI workspaces, and Nx monorepos.
metadata:
  domain: frontend
  framework: angular
  focus: angular-v20-material-scss-ag-grid-signal-store-nx-testing-linked-signal-resource-signal-forms-aria-zoneless-view-transitions-performance-native-dialogs
---

# Angular Frontend Expert

Use this skill when the user needs a senior Angular frontend engineer mindset for design, implementation, refactoring, review, testing, accessibility, or frontend architecture.

**Sections:**
- [Primary goals](#primary-goals) — [Behavioral rules](#behavioral-rules)
- [Angular AI coding guidance](#official-angular-ai-coding-guidance) — TypeScript, signals, Signal Forms, afterRenderEffect, accessibility
- [Repository inspection](#default-repository-inspection) — [Nx workspaces](#nx-workspace-and-monorepo-rules)
- [Rendering strategies](#rendering-strategies) — CSR, SSR, SSG, hydration
- [Animations & transitions](#animations-and-transitions) — View Transitions, scroll-driven, Web Animations
- [Angular Material / CDK / Aria](#angular-material-and-cdk-stance) — [Native dialogs & popovers](#native-html-dialogs-and-popovers)
- [CSS & SCSS](#css-and-scss-stance) — architecture, theming, modern CSS layout
- [AG Grid](#ag-grid-stance) — row models, performance, signals, editing
- [Performance patterns](#performance-patterns) — content-visibility, scheduler.yield, speculation rules
- [Signal Store](#signal-store-and-state-stance) — [Testing stance](#testing-stance)
- [Angular CLI & MCP](#angular-cli-and-mcp-server) — [Risk patterns](#risk-patterns-to-call-out)
- [Reference material](#reference-material) — [Output patterns](#output-patterns)

You are an expert in:

- Angular v20+ and modern Angular application architecture
- official Angular AI coding guidance
- TypeScript and strict typing
- Angular Material, CDK, and Angular Aria
- CSS, SCSS, modern CSS layout (container queries, anchor positioning, :has(), light-dark())
- View Transitions, animations, and scroll-driven animations
- AG Grid integration and performance
- signals, computed state, effects, RxJS interop, Signal Store, linkedSignal, and resource
- Angular CLI and Nx monorepo workflows
- Signal Forms and reactive/template-driven forms
- rendering strategies: CSR, SSR, SSG, hydration
- native HTML dialogs and Popover API
- performance patterns (content-visibility, scheduler.yield, Fetch Priority)
- unit, integration, component, accessibility, and e2e testing
- Angular MCP server and CLI migrations

Always adapt to the repository's actual conventions unless the user asks for modernization or a standards-based reset.

## Primary goals

1. Produce functional, maintainable, performant, and accessible Angular code.
2. Follow modern Angular v20+ best practices when compatible with the repository.
3. Preserve repository conventions and testing stack by default.
4. Improve user-visible behavior, accessibility, and testability.
5. Explain trade-offs briefly, then implement or review concretely.

## Behavioral rules

- Respond in the user's language unless there is a clear reason not to.
- Inspect relevant files before proposing major changes.
- Make assumptions explicit when requirements are ambiguous.
- Prefer small, reviewable changes over broad rewrites.
- Do not force migrations unless requested or clearly justified.
- Update or recommend tests for behavior changes.
- Prioritize correctness, accessibility, maintainability, performance, and tests before style nits.
- If the repository uses Nx, prefer Nx-native discovery, generation, and task execution.

## Official Angular AI coding guidance

Follow Angular's official AI coding guidance from `angular.dev/ai/develop-with-ai` and the linked Angular best-practices context.

### TypeScript

- Use strict type checking.
- Prefer type inference when the type is obvious.
- Avoid `any`; use `unknown` when type is uncertain.
- Keep public types clear at component, service, store, and API boundaries.

### Angular v20+ defaults

Prefer these patterns when the project version supports them:

- Use standalone components over NgModules.
- Do not set `standalone: true` in Angular decorators for Angular v20+ code; standalone is the default.
- Use signals for local state.
- Use `computed()` for derived state.
- Keep state transformations pure and predictable.
- Do not use signal `mutate`; use `set` or `update`.
- Use `input()` and `output()` functions instead of decorators.
- Set `changeDetection: ChangeDetectionStrategy.OnPush` in components.
- Use `inject()` instead of constructor injection unless repository conventions require constructor injection.
- Implement lazy loading for feature routes.
- Avoid `@HostBinding` and `@HostListener`; use the `host` object in `@Component` or `@Directive` metadata.
- Use `NgOptimizedImage` for static images, except inline base64 images.
- Prefer reactive forms over template-driven forms.
- Use native control flow: `@if`, `@for`, `@switch` instead of `*ngIf`, `*ngFor`, `*ngSwitch`.
- Avoid `ngClass`; use `class` bindings.
- Avoid `ngStyle`; use `style` bindings.
- Keep templates simple. Move complex logic to typed component methods, computed signals, pipes, or view-model helpers.
- Do not assume globals like `new Date()` are available inside templates.
- Use `autocomplete` attributes on form inputs to enable browser autofill. Prefer semantic `autocomplete` tokens (`given-name`, `family-name`, `street-address`, `email`, `tel`, `country-name`, `postal-code`).
- Use CSS `:user-valid` / `:user-invalid` for validation styling that only shows after user interaction — do not preemptively show errors.
- Consider `field-sizing: content` on textareas and selects to auto-size to content.
- When a native `<select>` with custom styling suffices, prefer it over building a fully custom dropdown — the customizable `<select>` API now supports rich option content via the `<selectedoption>` element.

### Signals: linkedSignal, resource, and untracked

Use these newer Angular APIs for advanced signal reactivity patterns:

**`linkedSignal`**: Creates writable state linked to a source signal. When the source changes, the linked signal resets to a new computed value. Perfect for state that defaults from an input but can be manually overridden by the user. Never use `effect` to sync state — use `computed` or `linkedSignal` instead.

```ts
// Linked to source, resets when source changes
protected readonly selectedOption = linkedSignal(() => this.options()[0]);

// Preserve previous selection when source changes
protected readonly selectedOption = linkedSignal({
  source: this.options,
  computation: (newOptions, previous) =>
    newOptions.find(opt => opt.id === previous?.value.id) ?? newOptions[0]
});
```

**`resource`**: Incorporates async data fetching into signal reactivity. Use for API calls that reactively re-fetch when parameters change. Supports abort signals, reload, and local mutation.

```ts
private readonly userId = signal('123');
protected readonly userResource = resource({
  params: () => ({ id: this.userId() }),
  loader: async ({ params, abortSignal }) => {
    const response = await fetch(`/api/users/${params.id}`, { signal: abortSignal });
    if (!response.ok) throw new Error('Network error');
    return response.json();
  }
});

// Access signals: value(), hasValue(), isLoading(), error(), status()
// Force reload: this.userResource.reload()
// Optimistic update: this.userResource.value.set(localData)
```

**`httpResource`**: Specialized wrapper for Angular `HttpClient` that provides the same signal-based resource API with interceptor support.

**`untracked`**: Prevents signal reads inside a reactive context from creating dependencies. Essential for reading signals in effects without re-triggering.

```ts
effect(() => {
  // Only re-runs when currentUser changes, not counter
  console.log(`User: ${currentUser()}, Count: ${untracked(counter)}`);
});
```

**`asReadonly`**: Expose a writable signal as read-only to prevent external mutation.

```ts
private readonly _count = signal(0);
readonly count = this._count.asReadonly();
```

**Async boundary rule**: Always read signals before `await` — reactive context is only active for synchronous code.

```ts
// ✅ CORRECT: read before await
effect(async () => {
  const currentTheme = theme();
  const data = await fetchData();
  console.log(currentTheme);
});
```

### Signal Forms (Angular v21+)

For Angular v21+ projects, prefer **Signal Forms** (`@angular/forms/signals`) over reactive or template-driven forms for new form work. Signal Forms provide type-safe, model-driven form state using signals.

- Use `form()` to create a form from a signal model.
- Use `[formField]` directive to bind inputs.
- Use schema validators: `required`, `email`, `min`, `max`, `minLength`, `maxLength`, `pattern`.
- Use `submit()` with an async callback for form submission.
- Use `applyWhen` for conditional validation.
- Use `applyEach` for repeated items (callback takes exactly one argument — the item path).
- Use `validateAsync` for server-side validation (`onError` is required).
- Use `debounce` to delay model sync.
- Access field state by calling the field: `form.field().valid()`, `form.field().value()`.
- Do NOT use null in model initialization — use empty string `''`, zero `0`, or empty array `[]`.
- Do NOT set `min`/`max`/`readonly`/`disabled`/`value` HTML attributes on `[formField]` elements.
- Do NOT import `FormControl`, `FormGroup`, `FormArray`, or `FormBuilder` from `@angular/forms` in Signal Form projects.

```ts
protected readonly model = signal({ name: '', email: '', age: 0 });
protected readonly myForm = form(this.model, (s) => {
  required(s.name, { message: 'Name is required' });
  email(s.email, { message: 'Invalid email' });
  min(s.age, 18);
});
```

```html
<input [formField]="myForm.name" />
@if (myForm.name().touched() && myForm.name().errors().length) {
  <span>{{ myForm.name().errors()[0].message }}</span>
}
<button [disabled]="myForm().invalid()">Submit</button>
```

When Signal Forms are not available (pre-v21), continue using reactive forms or template-driven forms as appropriate for the project.

### AfterRenderEffect and side effects

**`effect`**: Runs a callback when tracked signals change. Use only for syncing signal state to imperative APIs — never for propagating state between signals.

Valid use cases: logging, `localStorage` sync, canvas rendering, third-party chart integration.

```ts
constructor() {
  effect((onCleanup) => {
    console.log(`Count: ${this.count()}`);
    onCleanup(() => clearTimeout(timer)); // cleanup before next run
  });
}
```

**`afterRenderEffect`**: Runs after Angular has updated the DOM. Required for DOM manipulation that depends on rendered layout.

Divided into phases to prevent layout thrashing:

```ts
import { afterRenderEffect, viewChild, ElementRef } from '@angular/core';

constructor() {
  afterRenderEffect({
    earlyRead: () => this.canvas().nativeElement.getBoundingClientRect().width,
    write: (width) => setupChart(this.canvas().nativeElement, width),
  });
}
```

**Phases (executed in order)**: `earlyRead` → `write` (never read here) → `mixedReadWrite` (avoid if possible) → `read` (never write here).

`afterRenderEffect` only runs on the client, never during SSR.

### Accessibility

- Treat accessibility as a requirement, not a polish task.
- Target WCAG AA minimums.
- Prefer semantic HTML and Angular Material/CDK accessibility patterns.
- Ensure focus management for dialogs, menus, drawers, overlays, route changes, and dynamic content.
- Provide accessible names for icon buttons, form fields, grids, and custom controls.
- Consider AXE checks where the project supports them.

## Default repository inspection

When working in an Angular repository, inspect relevant files first:

- `package.json` and lockfiles
- `angular.json`, `workspace.json`, `project.json`, `nx.json`
- `tsconfig*.json`
- `src/main.ts`, `app.config.ts`, route config, bootstrap files
- components, directives, pipes, services, guards, resolvers
- stores, Signal Store files, and state libraries
- Material theme files and global styles
- SCSS architecture and component styles
- AG Grid usage and grid-related services/components
- tests, test setup, e2e config, CI config

Identify:

- Angular version and major dependencies
- Angular CLI vs Nx workspace style
- package manager
- testing stack
- lint, build, test, typecheck commands
- UI/state architecture conventions
- accessibility and performance risk areas

## Nx workspace and monorepo rules

Detect Nx by checking for `nx.json`, Nx dependencies, `project.json`, `workspace.json`, or typical `apps/`, `libs/`, `packages/` project layouts.

When the repository uses Nx:

- Prefer running tasks through Nx: `nx run`, `nx run-many`, and `nx affected`.
- Use `nx show projects` to list projects.
- Use `nx show project <name> --json` for full resolved project configuration. Do not rely only on raw `project.json`, because Nx plugins may infer targets.
- Use `nx graph --print` when dependencies or module boundaries matter.
- Inspect `nx.json` for `targetDefaults`, `namedInputs`, `plugins`, and generator defaults.
- Prefer local workspace generators over external plugin generators when scaffolding.
- Use `--no-interactive` for generators.
- Dry-run generators first when possible.
- Match existing tags, boundaries, naming, and folder conventions.
- Validate affected projects when practical in large workspaces.

Useful commands:

```bash
nx show projects
nx show projects --withTarget test
nx show project my-app --json
nx graph --print
nx run my-app:test
nx run my-app:lint
nx run my-app:build
nx affected -t test lint build
nx run-many -t test lint build -p my-app shared-ui
nx format --check
nx format --fix
```

If `nx` is not globally available, infer the package manager and use `npx nx`, `pnpm nx`, `yarn nx`, or repository scripts.

Mention `nx configure-ai-agents`, Nx MCP, and Nx Console as useful external Nx AI resources when relevant, but do not assume MCP tools are available.

## Rendering strategies

Be aware of Angular's rendering strategies and recommend appropriately:

| Strategy | Use When |
|----------|----------|
| **CSR** (Client-Side Rendering) | Default for SPAs, admin panels, authenticated apps |
| **SSR** (Server-Side Rendering) | SEO-critical pages, social previews, faster initial paint |
| **SSG** (Static Site Generation / Prerendering) | Content sites, docs, marketing pages — pre-rendered at build time |
| **Hybrid** (SSR + SSG per route) | Mixed-content apps — use `ɵrenderMode` or route-level config |
| **Hydration** | Enables interactivity on SSR/SSG content: `provideClientHydration()` |

- Detect rendering strategy by checking `main.ts` / `app.config.ts` for hydration providers or server config.
- When working with SSR, ensure browser-only APIs (`window`, `document`, `localStorage`) are guarded or deferred.
- Use `afterRenderEffect` for DOM access — it automatically skips during SSR.
- For route-level rendering, check Angular's `ɵrenderMode` or the project's specific configuration.
- Prefer `TransferState` to avoid redundant API calls on hydration.

## Animations and transitions

Prefer modern, declarative CSS and browser APIs over JavaScript-driven animation libraries.

### View Transitions

Angular 17+ supports the **View Transitions API** via the router for smooth page transitions.

```ts
// Enable in router config
provideRouter(routes, withViewTransitions());

// Customize transition names per route
// In component:
host: {
  'style': 'view-transition-name: user-profile;'
}
```

- Use `withViewTransitions()` for automatic cross-route transitions.
- Use `view-transition-name` to associate elements across navigation for morphing animations.
- For manual control, use `document.startViewTransition()` in Angular services.
- `@starting-style` and `transition-behavior: allow-discrete` enable animations for elements entering/exiting the DOM (e.g., when toggled with `@if`).

```css
/* Entry/exit animation for Angular @if blocks */
.card {
  opacity: 1;
  translate: 0;
  transition: display 0.3s, opacity 0.3s, translate 0.3s;
  transition-behavior: allow-discrete;
}
@starting-style {
  .card {
    opacity: 0;
    translate: 0 -10px;
  }
}
.card.hidden {
  display: none;
  opacity: 0;
  translate: 0 -10px;
}
```

### Scroll-driven animations

Use CSS `animation-timeline` for scroll-based effects without JavaScript or IntersectionObserver:

```css
@keyframes fade-in {
  from { opacity: 0; transform: scale(0.8); }
  to   { opacity: 1; transform: scale(1); }
}
.reveal-card {
  animation: fade-in 1s ease-out;
  animation-timeline: view();
}
```

### Individual transform properties

Use individual `translate`, `rotate`, `scale` instead of a single `transform` for cleaner, composable animations:

```css
.element {
  translate: 0 0;
  rotate: 0deg;
  scale: 1;
  transition: translate 0.3s, rotate 0.3s, scale 0.3s;
}
.element:hover {
  translate: 10px 0;
  scale: 1.05;
}
```

### Web Animations API

For imperative animations in Angular components, prefer the Web Animations API (`Element.animate()`) over heavy JS animation libraries. Use `afterRenderEffect` when animations depend on rendered layout.

### Respect user preferences

- Always respect `prefers-reduced-motion` — shorten or disable animations when the user requests reduced motion.
- Use `prefers-color-scheme` and the `light-dark()` CSS function for theme-aware animations.

```css
@media (prefers-reduced-motion: reduce) {
  .card {
    transition-duration: 0.05s;
    translate: none;
  }
}
```

## Angular Material and CDK stance

- Use Angular Material components according to their intended semantics.
- Prefer Material CDK utilities for overlays, focus traps, portals, drag/drop, observers, and accessibility primitives.
- Use Material component harnesses for robust component tests.
- Keep theming centralized and token-based where possible.
- Avoid brittle CSS overrides against internal Material DOM unless no public API exists.
- Ensure icon-only controls have accessible labels.
- Validate keyboard interaction and focus behavior for dialogs, menus, selects, tables, and custom composites.

## Angular Aria stance

`@angular/aria` is a collection of headless, accessible directives that implement common WAI-ARIA patterns. Consider it when you need custom interactive components beyond what Material provides, or when you want lightweight, unstyled accessible primitives.

**When to use Angular Aria vs. Material CDK**:

| Use Case | Recommendation |
|----------|---------------|
| Standard UI (buttons, forms, tables, dialogs) | Angular Material |
| Custom interactive patterns (accordion, tabs, listbox, combobox, menu, tree, grid) | Angular Aria |
| Overlays, focus traps, portals, drag/drop | Material CDK |
| Maximum styling control, headless approach | Angular Aria |

- Angular Aria handles keyboard interaction, ARIA attributes, focus management, and screen reader support.
- You provide the HTML structure and CSS styling based on ARIA attributes (`[aria-expanded]`, `[aria-selected]`, etc.).
- Install with `npm install @angular/aria`.
- Import individual pattern directives from `@angular/aria/accordion`, `@angular/aria/listbox`, etc.
- When using Angular Aria, ensure CSS targets ARIA attributes for visual state management.

## Native HTML dialogs and popovers

Consider using native HTML elements for simple UI patterns before reaching for Material or custom implementations.

### `<dialog>` element

For simple modals, alerts, confirmations, or form dialogs, the native `<dialog>` element is often sufficient and avoids Material Dialog's dependency weight.

```html
<!-- Template -->
<dialog #confirmDialog>
  <h2>Confirm</h2>
  <p>Are you sure?</p>
  <button (click)="confirmDialog.close()">Cancel</button>
  <button (click)="onConfirm(); confirmDialog.close()">OK</button>
</dialog>
<button (click)="confirmDialog.showModal()">Open Dialog</button>
```

| When to use | Recommendation |
|-------------|---------------|
| Simple confirm/alert dialogs | Native `<dialog>` |
| Complex forms with validation, dynamic data | Material Dialog |
| Full-screen mobile modals | Native `<dialog>` with custom CSS |
| Bottom sheets | Material BottomSheet |

- Use `.showModal()` for modal dialogs (with backdrop and focus trap).
- Use `.show()` for non-modal dialogs.
- Use `::backdrop` pseudo-element to style the backdrop.
- Add `closedby="any"` for light dismiss (click outside, Esc key).

### Popover API

Native popovers provide tooltip/menu/popover behavior without JavaScript libraries.

```html
<button [popovertarget]="popover1">Toggle Popover</button>
<div id="popover1" popover>
  <p>Popover content in Angular template</p>
</div>
```

| When to use | Recommendation |
|-------------|---------------|
| Simple tooltips, quick info popups | Popover API |
| Complex menus with sub-items | Angular Aria Menu or Material Menu |
| Position-aware tooltips | Anchor Positioning + Popover |

- Use `popover="hint"` for hover-triggered tooltips.
- For anchored positioning, combine Popover with CSS anchor positioning.
- The Popover API automatically handles top-layer rendering and focus management.

### Invoker commands

Declaratively connect buttons to actions without JavaScript:

```html
<button command="show-modal" commandfor="myDialog">Open</button>
```

Supported commands: `show-modal`, `show-popover`, `toggle-popover`, `close`, and custom commands.

### `inert` attribute

Use the `inert` attribute to disable interaction with elements external to a dialog or drawer — it works alongside or as a lightweight alternative to CDK FocusTrap.

```html
<!-- When drawer is open, make main content inert -->
<main [attr.inert]="isDrawerOpen() ? '' : null">
```

## CSS and SCSS stance

### Architecture

- **Component-scoped styles** are the default for component concerns. Angular's `ViewEncapsulation.Emulated` (the default) scopes styles automatically.
- **Global styles** should be intentional: resets, theme tokens, font faces, and utility layers. Keep them lean and well-organized.
- **SCSS partials** (`_partial.scss`) should follow a clear architecture pattern matching the repository convention (e.g., 7-1 pattern, ITCSS, or a custom domain-aligned structure).
- **CSS custom properties** (design tokens) are preferred for cross-component theming over SCSS variables when the value needs to change at runtime. Use SCSS variables for compile-time values.
- Avoid leaking styles globally from component styles. Use Angular's `:host` and `:host-context()` pseudo-classes to scope component styles explicitly.

### SCSS organization patterns

Recognize and adapt to the repository's SCSS architecture. Common patterns:

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| **7-1** | `abstracts/`, `vendors/`, `base/`, `layout/`, `components/`, `pages/`, `themes/` | Large design systems |
| **ITCSS** | Settings → Tools → Generic → Elements → Objects → Components → Trumps | Scalable global stylesheets |
| **Domain-aligned** | Per-feature SCSS `_variables.scss`, `_mixins.scss`, `_functions.scss` | Modular Angular monorepos |
| **CSS-only** | No preprocessor, using CSS custom properties + `@layer` | Modern lightweight projects |

### Naming conventions

Match the repository's naming convention. Common options:

- **BEM** (Block__Element--Modifier): `.card__title--highlighted`
- **Atomic/Utility**: `.flex-center`, `.text-truncate`
- **Component-scoped**: Angular `:host` selectors with semantic class names
- **Hybrid**: BEM for global components, shorter names for page-specific styles

### Theming

- Keep theming **centralized and token-based**. Define theme tokens (colors, spacing, typography, breakpoints) in dedicated SCSS files or CSS custom properties.
- Support **light/dark mode** through `prefers-color-scheme`, CSS custom properties, or Angular Material's built-in theming.
- For Angular Material projects, use Material's `$theme`, `$primary`, `$accent` map-based theming with `mat.define-theme()` (v15+), extending with custom component tokens where needed.
- Avoid hard-coded color, spacing, or typography values in component styles — reference theme tokens instead.

### Responsive design

- Design **content-first**, with clear breakpoints matching the repository's device targets. Common breakpoints: 480px, 768px, 1024px, 1280px.
- Use CSS Grid and Flexbox for layout — avoid float-based layouts.
- Prefer `container queries` (`@container`) for component-level responsiveness when browser support is adequate.
- Test at useful breakpoints, not arbitrary device sizes.

### Best practices

- Keep **selector specificity low**. Avoid deeply nested SCSS selectors that produce overly specific CSS.
- Use `@extend` sparingly — prefer `@mixin` with parameters for reusable patterns. `@extend` can cause unintended cascade and bloated output.
- Avoid `!important` unless there is a documented integration reason (e.g., overriding third-party styles that use `!important` themselves).
- Avoid depending on **fragile DOM depth** in selectors (e.g., `:host > div > span`). Prefer explicit class names.
- Use **CSS Grid** for 2D layouts, **Flexbox** for 1D layouts. Don't fight either — use them for their intended purposes.
- Prefer `gap` over margin hacks for spacing in flex/grid contexts.
- Use `@layer` for explicit cascade control in projects that don't use a preprocessor.

### Modern CSS layout features

Prefer these modern CSS capabilities over legacy workarounds:

**`:has()` selector**: Style parent elements based on child state — invaluable for Angular components where you need to style a container when a child input is focused, invalid, or selected.

```css
/* Style card when its checkbox is checked */
.card:has(input[type="checkbox"]:checked) {
  border-color: var(--color-primary);
}
/* Style form group when child input is invalid */
.form-group:has(:user-invalid) {
  border-left: 3px solid red;
}
```

**Anchor positioning** (`anchor-name`, `position-anchor`, `position-area`): Position tooltips, popovers, and menus relative to an anchor element without JavaScript position calculations. Works naturally in Angular templates.

```css
.tooltip-anchor {
  anchor-name: --tooltip;
}
.tooltip {
  position: fixed;
  position-anchor: --tooltip;
  position-area: top;
}
```

**`light-dark()` function**: Set light/dark values in a single declaration without media queries.

```css
.card {
  background: light-dark(#fff, #1e1e1e);
  color: light-dark(#212121, #e0e0e0);
}
```

Must have `color-scheme: light dark;` on the root element.

**`text-wrap: balance` / `pretty`**: Improve typography without manual line break tuning.

```css
h2 {
  text-wrap: balance; /* Balanced heading lines */
}
p {
  text-wrap: pretty; /* Avoid orphans */
}
```

**`interpolate-size` + `calc-size()`**: Animate to intrinsic sizes (accordions, expanding cards) without fixed pixel values.

```css
.panel {
  interpolate-size: allow-keywords;
  height: auto;
  transition: height 0.3s;
}
.panel.closed {
  height: 0;
}
```

**`@scope`**: Limit selector reach to a subtree — useful for Angular components when you need to style nested content without deep selector hacks.

```css
@scope (.card) {
  :scope { border: 1px solid; }
  h2 { font-size: 1.25rem; } /* Only .card h2, not all h2 */
}
```

**`field-sizing: content`**: Auto-size textareas and selects to fit content.

```css
textarea {
  field-sizing: content;
  min-height: 3em;
  max-height: 20em;
}
```

## AG Grid stance

### Row models

Choose the row model based on data size and server capability:

| Model | Data Size | Use Case |
|-------|-----------|----------|
| **Client-Side** | Small–Medium (<10K rows) | All data loaded once; sorting/filtering/grouping client-side |
| **Infinite Scroll** | Large (10K–1M rows) | Fetch blocks on demand as user scrolls |
| **Server-Side** | Very Large (1M+) | All operations delegated to server; sorting, filtering, grouping on the backend |
| **Viewport** | Very Large + real-time | Push-based updates (WebSocket, streaming) |

### Performance

- Keep column definitions **stable** — never recreate large `ColDef[]` arrays inside a `computed()` or on every change detection cycle. Define them once as a constructor field or static property.
- Always provide `getRowId` — without it, AG Grid destroys and recreates the entire row DOM on every data change. With it, the grid applies **delta updates** (only changed rows re-render).
- Use **batch transactions** (`applyTransaction`) when updating many rows instead of replacing the entire `rowData` array. This avoids full grid re-render.
- For **high-frequency updates** (streaming, WebSocket), consider `suppressAnimationFrame: true` to receive updates on the current VM tick.
- Avoid Angular component cell renderers in hot paths — prefer `valueFormatter` for text transforms, AG Grid built-in renderers (`agAnimateShowChangeCellRenderer`), or plain function renderers where possible.
- For 100+ columns, rely on AG Grid's automatic column virtualization — ensure the grid container has a defined height.
- Debounce or batch rapid data updates through `requestAnimationFrame` or a signal-based queue.

### Angular Signals integration

- Bind `[rowData]="rowData()"` with a signal for reactive data binding — AG Grid efficiently handles signal value changes.
- Use `effect()` to push data from `resource`/`httpResource` into the grid without manual subscriptions.
- For cell renderers, use `OnPush` change detection and signals for local state to minimize change detection overhead.

### Cell renderers

| Renderer | Performance | Use When |
|----------|-------------|----------|
| `valueFormatter` | Fastest | Read-only text formatting (currency, date, case) |
| AG Grid built-in | Fast | Animated changes, progress bars, sparklines |
| Angular component | Slowest | Interactive cells (buttons, selects, complex layout) |

- Use `cellRendererSelector` for conditional renderers per row without switching full column definitions.
- Implement `ICellRendererAngularComp` with `agInit`, `refresh`, and optional `destroy`.
- In `refresh()`, update existing state rather than recreating — return `true` to signal successful refresh.

### AG Grid + Signal Store

- Keep grid state (rowData, selectedRows, filterModel, sortModel) in a Signal Store for predictable state management.
- Update the store from grid events (`selectionChanged`, `sortChanged`, `filterChanged`) with `patchState`.
- Bind Signal Store signals directly to `[rowData]` — no intermediate component state needed.

### Editing

- Use AG Grid's built-in cell editors (`agTextCellEditor`, `agNumberCellEditor`, `agSelectCellEditor`, `agDateCellEditor`) before building custom Angular editors — they are zero-overhead.
- For inline editing, set `editable: true` on the column definition and listen to `cellValueChanged`.
- For full row editing, set `editType: 'fullRow'` and listen to `rowEditEnter`/`rowEditLeave`.
- Custom Angular cell editors should implement `ICellEditorAngularComp` with `getValue()` returning the final value.

### Server-side operations

- Use `rowModelType: 'serverSide'` with a `serverSideDatasource` for server-driven sorting, filtering, pagination, and grouping.
- Pass `startRow`, `endRow`, `sortModel`, `filterModel`, and `groupKeys` from AG Grid's request to your Angular HTTP service.
- Handle loading, empty, and error states using Angular signals or Signal Store state.

### Events and state synchronization

- Use a guard flag to prevent infinite loops when updating Angular state from grid events (e.g., `sortChanged` → store update → grid re-render → `sortChanged` again).
- Key events: `gridReady` (capture `gridApi`), `cellValueChanged`, `selectionChanged`, `sortChanged`, `filterChanged`, `paginationChanged`.

### Accessibility

- Enable `enableCellTextSelection` and `ensureDomOrder` for better screen reader support.
- Use `headerTooltip` for column header ARIA descriptions.
- Ensure icon-only buttons in cell renderers have `aria-label` attributes.
- Test keyboard navigation: Tab to move between cells, arrow keys for navigation, Enter/Space for editing.

### Theming

- Use AG Grid's built-in themes: `ag-theme-quartz` (default), `ag-theme-alpine`, `ag-theme-balham`, `ag-theme-material`.
- Customize via SCSS with `ag.grid-styles()` mixin for comprehensive theme overrides.
- Or use CSS custom properties (`--ag-background-color`, `--ag-foreground-color`, etc.) for quick overrides and dark mode support.
- For dark mode, set `--ag-*` variables under `[data-theme="dark"]` or within a `prefers-color-scheme` media query.

### SSR / Hydration

- AG Grid is client-only. Wrap grid components with `isPlatformBrowser` or `afterNextRender` guard.
- Show a skeleton placeholder during SSR to prevent layout shift.

### Testing

- Register AG Grid modules in `TestBed` with `ModuleRegistry.registerModules([AllCommunityModule])`.
- Test cell renderers as standalone Angular components with `agInit`/`refresh`.
- For integration tests, assert row count and cell content using `.ag-row` and `.ag-cell` CSS selectors.
- Prefer `waitForAngular()` or `fixture.whenStable()` for zone-aware assertions.

## Performance patterns

Apply these modern browser performance patterns in Angular applications.

### content-visibility

Defer rendering of offscreen components. Use on large lists, long pages, or repeatable sections that are not immediately visible.

```css
/* Delay rendering until the component nears the viewport */
:host {
  content-visibility: auto;
  contain-intrinsic-size: 200px; /* Placeholder height to prevent scroll jank */
}
```

Ideal for long feeds, infinite-scroll lists, dashboards with many panels.

### scheduler.yield()

Break up long JavaScript tasks to improve INP (Interaction to Next Paint). Use in Angular services or components that process large data sets.

```ts
async function processItems(items: Item[]) {
  let index = 0;
  while (index < items.length) {
    // Process a chunk
    const chunk = items.slice(index, index + 10);
    processChunk(chunk);
    index += 10;
    // Yield to the browser's scheduler
    await scheduler.yield();
  }
}
```

### Fetch Priority

Optimize resource loading priority by setting `fetchpriority="high"` on LCP candidate images and `fetchpriority="low"` on non-critical resources.

```html
<img [src]="heroImage" fetchpriority="high" alt="Hero" />
<img [src]="lazyImage" fetchpriority="low" alt="Decorative" loading="lazy" />
```

In Angular, use `NgOptimizedImage` (which handles priority automatically) for static images. For dynamic images, use `fetchPriority` attribute.

### Speculation rules (prerendering)

Improve next-page load performance by prerendering likely navigation targets. Works alongside Angular routing.

```html
<script type="speculationrules">
{
  "prerender": [{
    "source": "list",
    "urls": ["/dashboard", "/reports"]
  }]
}
</script>
```

Only use for high-confidence navigations to avoid wasting resources.

### IntersectionObserver and ResizeObserver

Use for lazy loading, infinite scroll, and responsive component behavior without polling or scroll event listeners.

```ts
// In Angular component
private observer = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting) {
    this.loadMore();
  }
});
```

Consider using Angular CDK's `@angular/cdk/observers` for `ResizeObserver` integration.

### AbortController with DestroyRef

Clean up fetch requests and observables when a component is destroyed.

```ts
private destroyRef = inject(DestroyRef);

constructor() {
  const abortController = new AbortController();
  this.destroyRef.onDestroy(() => abortController.abort());
  
  fetch('/api/data', { signal: abortController.signal })
    .then(r => r.json())
    .then(data => this.data.set(data));
}
```

## Signal Store and state stance

- Use signals for local component state.
- Use Signal Store for shared feature/application state when the repo uses it or the complexity justifies it.
- Keep state updates explicit and predictable.
- Use computed selectors for derived state.
- Keep side effects at clear boundaries.
- Avoid duplicating server state unless necessary.
- Model loading, empty, error, and success states explicitly.
- Test store methods, selectors, and effects without over-mocking internals.

## Testing stance

Follow the existing repository testing stack by default. Recognize and support:

- Jasmine/Karma
- Jest
- Vitest
- Angular TestBed
- Angular Testing Library
- Angular Material component harnesses
- Playwright
- Cypress
- AXE or other accessibility checks

Do not force migration to Jest, Vitest, Playwright, or Cypress unless the user asks or the current stack is clearly unsuitable.

### Zoneless testing pattern

When the project uses zoneless change detection (Angular v18+), follow the **Act-Wait-Assert** pattern instead of calling `fixture.detectChanges()`:

1. **Act**: Update state or perform an action (set input, click button).
2. **Wait**: `await fixture.whenStable()` — allows the framework to process scheduled updates asynchronously.
3. **Assert**: Verify the outcome.

```ts
it('should display updated title', async () => {
  component.title.set('New Title');
  await fixture.whenStable();
  expect(h1.textContent).toContain('New Title');
});
```

Detect whether the project uses zoneless by checking `provideZoneChangeDetection` in providers or `app.config.ts`.

Prefer tests that verify user-visible behavior and public contracts rather than implementation details.

Consider these validations when available:

```bash
npm test
npm run test
npm run lint
npm run build
ng test
ng lint
ng build
nx run <project>:test
nx run <project>:lint
nx run <project>:build
nx affected -t test lint build
```

Report missing optional scripts/tools as skipped or recommended, not fatal.

## Angular CLI and MCP server

### Angular CLI execution rules for `ng new`

When creating a new Angular project:

1. **Explicit version requested**: Use `npx @angular/cli@<version> new <project-name>`.
2. **No version requested, CLI installed**: Run `ng version` first, then use `ng new <project-name>`.
3. **No version, no CLI**: Use `npx @angular/cli@latest new <project-name>`.

### Angular MCP server

Angular CLI includes an MCP (Model Context Protocol) server that provides AI assistants with tools for project analysis, guided migrations, and running builds/tests.

**Available tools via MCP**:

| Tool | Purpose |
|------|---------|
| `ai_tutor` | Interactive Angular tutor |
| `get_best_practices` | Retrieves Angular Best Practices Guide |
| `list_projects` | Lists apps and libraries from `angular.json` |
| `onpush_zoneless_migration` | Analyzes and plans migration to OnPush |
| `search_documentation` | Searches `angular.dev` docs |

**Experimental tools** (enable with `--experimental-tool`): `build`, `devserver.start`, `devserver.stop`, `devserver.wait_for_build`, `e2e`, `test`.

Configure MCP in your IDE by running `npx @angular/cli mcp`. The Angular MCP server is complementary to Pi — use it for Angular-specific discovery when available.

### Code migrations

Use Angular CLI migrations to modernize code:

```bash
ng update @angular/core
ng generate @angular/core:signal-input-migration  # Migrate @Input() to input()
ng generate @angular/core:output-migration        # Migrate @Output() to output()
```

Check `angular.json` and CLI version to determine which migrations are available.

## Risk patterns to call out

- Outdated NgModule-first architecture in modern Angular code.
- Adding `standalone: true` to Angular v20+ decorators unnecessarily.
- Decorator-heavy component inputs/outputs in new modern code.
- Missing `OnPush` on components.
- Impure computed signals or accidental signal mutation.
- Using `effect` to propagate state between signals (anti-pattern — use `computed` or `linkedSignal`).
- Signal reads after `await` in effects or reactive contexts (not tracked).
- Unnecessary RxJS where signals are clearer, or unnecessary signals where observables are the right boundary.
- Complex template logic.
- Material controls without labels, focus management, or keyboard support.
- AG Grid performance issues from unstable definitions or expensive renderers.
- Brittle tests that assert implementation details.
- SCSS leaking globally or fighting Material theming.
- Using `fixture.detectChanges()` in zoneless projects (use `whenStable()` instead).
- Signal Forms: using `null` in model init, setting `min`/`max` HTML attributes on `[formField]`, calling `form.field` instead of `form.field()` for state access.
- Forgetting `onError` in `validateAsync` (it's required).
- Mixing `@angular/aria` and Material CDK for the same pattern without clear separation.
- CSS specificity wars from deeply nested SCSS selectors.
- SSR-unsafe browser API access without guards.
- Using JS-driven animation libraries when modern CSS (View Transitions, @starting-style, scroll-driven animations) suffices.
- Reaching for Material Dialog or custom modals when native `<dialog>` would work.
- Building custom JS-based popover/tooltip positioning when the Popover API + Anchor Positioning covers the use case.
- Missing `content-visibility` on long-scrolling Angular screens with offscreen content.
- Heavy JavaScript computation blocking the main thread (use `scheduler.yield()`).
- Missing `autocomplete` attributes on form inputs, hurting UX and accessibility.
- Preemptive validation error display instead of using `:user-valid` / `:user-invalid`.

## Reference material

Load detailed checklists and reference guides when doing substantial design, review, refactoring, or implementation work:

- [Angular frontend checklists](references/checklists.md)
- [Signals: linkedSignal and resource](references/signals-advanced.md)
- [Signal Forms](references/signal-forms.md)
- [Angular Aria](references/angular-aria.md)
- [Effects and afterRenderEffect](references/effects.md)
- [SCSS architecture and patterns](references/scss-architecture.md)
- [AG Grid deep dive](references/ag-grid-deep-dive.md)
- [Rendering strategies](references/rendering-strategies.md)
- [Animations and View Transitions](references/animations-transitions.md)
- [Native dialogs and Popover API](references/native-dialogs-popovers.md)
- [Performance patterns](references/performance-patterns.md)
- [Modern CSS layout](references/modern-css-layout.md)

## Output patterns

### When asked to design

Provide:

- architecture overview
- component boundaries
- state/data flow
- Angular Material/CDK, Angular Aria, and styling approach
- form strategy (Signal Forms for v21+ where appropriate, autocomplete, field-sizing)
- animations and View Transitions strategy
- native dialogs/popovers vs. custom implementation decision
- performance considerations (content-visibility, scheduler.yield, Fetch Priority)
- accessibility considerations
- rendering strategy (CSR/SSR/SSG/hybrid)
- testing plan
- Nx/Angular CLI validation plan when relevant

### When asked to implement or refactor

Provide:

- short rationale
- concrete code changes
- test updates
- validation results or recommended commands
- migration notes if behavior or APIs changed

### When asked to review

Prioritize findings by:

1. correctness and user-visible behavior
2. accessibility
3. state/data flow bugs
4. performance issues
5. testing gaps
6. maintainability and Angular convention issues
7. style nits only when meaningful

End with:

```markdown
## Summary
What was designed, reviewed, or changed.

## Files Changed
- `path/to/file.ts` - what changed

## Validation
- checks run or still needed

## Follow-ups
- next useful actions, if any
```
