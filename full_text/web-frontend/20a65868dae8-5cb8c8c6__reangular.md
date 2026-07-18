---
name: reangular
description: Use when the user provides a path to a React library and asks for an Angular port, rewrite, conversion, or "Angular version" of it. The goal is FULL feature parity (not partial, not "mostly", not "API parity but visual gaps deferred") in modern Angular (standalone, zoneless, signals, OnPush) with a successful build and every demo route validated end-to-end against the React reference.
metadata:
  dependencies:
    - name: angular-developer
      source: https://github.com/angular/skills
---

# React Lib → Angular Lib

## Overview

Convert a local React library (full source) into a fully feature-equivalent modern Angular library. "Modern Angular" means: standalone components, zoneless change detection, signals (`signal`/`computed`/`effect`), `input()`/`output()`/`viewChild()`, new control flow (`@if`/`@for`/`@switch`), and `inject()`. No NgModules, no Zone.js, no `*ngIf`/`*ngFor`.

**Success criteria, all required, none negotiable, none partial:**
1. Full feature parity. Every feature, component, prop, output, state, slot, and exported symbol from the React library has a working Angular equivalent. "API parity" alone does not count, and neither does "most features." End-user-observable behavior matches. See *The parity bar* below.
2. `ng build <lib>` succeeds with zero errors and zero warnings.
3. The library's public API surface is documented and exported. Every public React symbol has a corresponding Angular export.
4. A demo app in the same workspace exhaustively demonstrates ALL functionality. Every public component/directive/service, every input, output, state, variant, and public method has a live, interactive UI in the demo. The demo is the parity contract made visible.
5. The demo app is validated end-to-end in a real browser via the Chrome DevTools MCP. **Every** route, not a sample, loads with zero console errors, every interactive element responds, and no failed network requests.
6. A side-by-side parity review (Phase 4) against the React lib's reference demo/Storybook is complete: `parity-review.md` exists with every box checked. (Exception: the React lib has no reference demo at all, documented in `parity-review.md`.)

**Core principle:** Discover before converting. A todo list with every feature pinned to a file is the contract. Phase 4 is the audit. **Anything less than full parity is unfinished work.**

## When to Use

- User points to a local React library (often under `node_modules`, a sibling repo, or a path) and asks for an Angular port.
- User says: "convert this React lib to Angular", "make an Angular version of X", "rewrite this in Angular", "port to Angular".
- The source is a *library* (consumed by other apps), not a full application. (For applications, the same patterns apply, but routing and build setup differ, so adapt phase 0.)

**When NOT to use:**
- Source is not React (Vue, Svelte, etc.), which needs different patterns.
- User wants partial conversion of a few components inside an existing Angular app. This skill assumes a fresh library scaffold.
- User wants the React lib *consumed from* Angular (interop) rather than rewritten. That's a wrapping problem, not a port.
- The source library, or any subset of it, is under a commercial or proprietary license. See *Legal constraint* below.

## Legal constraint: open-source libraries only

**This skill must only be used on React libraries whose source code is released under an OSI-approved open-source license** (MIT, Apache 2.0, BSD-2, BSD-3, ISC, MPL-2.0, etc.).

**Do not use this skill to port:**
- Components sold under a commercial license (e.g. "Pro", "Enterprise", "Business", or "Premium" tiers of any library).
- Any library whose license file contains terms like "no derivative works", "non-commercial use only", "no redistribution", or similar restrictions.
- Minified or obfuscated source that was obtained by decompiling a commercial bundle, even if the resulting code is rewritten.

**Why:** Commercial component licenses routinely prohibit derivative works and redistribution. Porting source code, even into a different framework, creates a derivative work. Clean-room reimplementation (writing from docs alone, never touching the source) can be legally defensible, but it requires strict discipline and is outside the scope of this skill, which works directly from the source tree.

**Before starting Phase 0, confirm the license:**

1. Read the `LICENSE` file at the root of the React library.
2. If there is no `LICENSE` file, check `package.json` for a `"license"` field.
3. If the license is anything other than a recognized OSI-approved open-source license, **stop and tell the user**. Do not proceed without explicit confirmation that they own the appropriate commercial license rights that permit creating a derivative work, or that legal counsel has cleared the port.
4. If the library has both open-source and commercial tiers (e.g. a free community edition and a paid Pro edition), only port the open-source tier. Refuse or ask the user to remove any Pro/Enterprise components from scope before continuing.

## Generated library README (required)

Every Angular library produced by this skill **must** ship a `README.md` at the workspace root that includes all of the following. The README is part of the deliverable, so a missing or incomplete README means the port is not done.

### Required sections

**1. Origin**

A prominent section (immediately after the title) that states:
- The name of the original React library and a direct link to its source repository (e.g. `https://github.com/org/react-lib`).
- That this library is an Angular port of that project.

Example:
```markdown
## Origin

This library is an Angular port of [react-lib](https://github.com/org/react-lib).
```

**2. Built with reangular**

A section crediting the skill used to generate the port:

```markdown
## Built with reangular

This library was generated using the [reangular](https://github.com/aleksanderbodurri/reangular) skill, an automated React-to-Angular conversion harness for coding agents.
```

**3. Contributors**

A section listing every contributor to the *original React library*, sorted in descending order by total commit count. Extract this list from the React library's git history before starting Phase 3 (the repo must be a git repository; if it is not, note this and skip the section with an explanation).

Command to extract the list (run from the React library's root):
```bash
git shortlog -sn --no-merges HEAD
```

Render the result as a markdown ordered list, including the commit count:

```markdown
## Original contributors

Contributors to [react-lib](https://github.com/org/react-lib), sorted by commit count:

1. Jane Smith (312 commits)
2. John Doe (201 commits)
3. Alice Lee (87 commits)
...
```

If the React library is not a git repository (e.g. it was extracted from a tarball or `node_modules`), write:
```markdown
## Original contributors

Contributor data unavailable. The React library source was not a git repository. See the [upstream project](https://github.com/org/react-lib) for the full contributor list.
```

### When to create the README

- Phase 0, step 7 (after the first commit): create a skeleton `README.md` with the Origin and Built-with sections filled in. The Contributors section can be a placeholder at this point.
- Phase 3.3 (final verification): replace the Contributors placeholder with the full sorted list extracted from `git shortlog`. Commit as part of the final verification commit.

The README must be present and complete before the *Definition of done* checklist can be ticked.

---

## The parity bar (Iron Law)

**Anything less than full feature parity is incomplete. Period.**

There is no "API parity is at 100% but visual parity is at 80%." There is no "the remaining 20% is just mechanical wiring." There is no "I documented the gap in `parity-review.md`, so I'm done." There is one bar: a user who knows the React library can sit down with the Angular library and the demo app, exercise every documented behavior, and not notice they switched. If they would notice, parity is not achieved.

**Rationalizations that don't lower the bar (every one of these means you are NOT done):**

| Rationalization | Reality |
|---|---|
| "API parity is 100%, visual/runtime parity is ~80%" | There is one parity. End-user observable behavior. The split doesn't exist. If a `<EventWrapper>` slot doesn't render, the API isn't actually working. It's a stub. |
| "I documented the gap in `parity-review.md`" | Documentation is not completion. `parity-review.md` is a *bug list to close*, not an *acceptance log*. Every box must be `[x]` before the work is done. |
| "The remaining work is just ~30h of mechanical wiring" | Effort estimates do not change the parity bar. "Mechanical" work is still work. The user asked for a working library, not an estimate of how to finish one. |
| "I validated 6 of the 56 demo routes end-to-end" | You validated nothing. Sampling is not validation. Every route. Every interaction. Or it's not done. |
| "The architectural pattern is identified, the rest follows" | Identified ≠ implemented. A pattern in your head doesn't render in the user's browser. |
| "I'll defer the wrapper-slot overrides as a follow-up" | Only the user can defer scope. You cannot unilaterally decide which features are out of scope. If you want to defer, *ask*, get explicit approval, and write the deferral into `todo.md` with the user's name attached, and don't quietly mark the task done. |
| "Most users won't hit that feature" | You don't know what most users hit. The React lib's authors put it in the public API; that's the only signal that matters. |
| "The build passes and it works for the basic case" | The basic case is the easy 20%. Real parity is the long tail. |
| "It's good enough for a first pass" | The skill does not have a "first pass" mode. There is finished and unfinished. |
| "I'm running low on context / tokens / usage" | Not your concern. Keep working. The system handles compaction automatically; usage is the user's budget, not your gate. See *Context, tokens, and usage are not stopping conditions* below. |
| "This conversation is getting long, I should wrap up" | The length of the conversation is not a signal to stop. The state of `parity-review.md` is the only signal. |
| "This React feature has no Angular equivalent" | False. There is no React API that cannot be expressed in Angular. See *Every React feature has an Angular implementation* below. |
| "I can't figure out how to port X, I'll skip it" | "Can't figure out" means "haven't yet figured out." Read the React source again. Read the Angular CDK. Read `patterns.md`. Build the primitive yourself if needed. Skipping is not on the table. |

**The only legitimate stopping point before full parity:**

1. The user explicitly authorizes deferring specific items (recorded in `todo.md` with the deferral noted, including the user's name and the date).

That is the entire list. There is no other legitimate reason to stop.

Expect you'll be run on models with low long term reasoning thresholds. Therefore if you detect you need to stop running before you are done the following must happen:

1. todos MUST be updated
2. A terse summary of what you did must be output in the agent chat on your last message.
3. The summary MUST list the items that are left in todo.md
4. The summary MUST list the items that you attempted and couldn't figure out
5. The summary MUST list the items that you deferred and the reason you deferred them

This is not optional. You'll be evaluated on the contents of your summary. If you don't do this, you failed.

### Every React feature has an Angular implementation

If you find yourself thinking "this React feature has no Angular equivalent" or "this can't be ported", **you are wrong**. Not "probably wrong." Wrong. There is no React library that cannot be ported to Angular. The frameworks express the same set of primitives (DOM, state, effects, composition, lifecycle, refs, context); the syntax differs, the underlying capabilities do not.

If you can't see the path, the problem is your search, not the framework. The escalation order:

1. Re-read `patterns/index.md` in this skill directory to find which pattern file covers the issue, then read that file.
2. Check `@angular/cdk` for a primitive (drag-drop, overlay, portal, focus trap, virtual scroll, a11y, clipboard, menu, listbox, dialog, autosize textarea, RTL, keycodes; see the CDK mapping in *Mindset shift*).
3. Read the React source carefully. Most React features that "look impossible" in Angular are just imperative DOM code that was wrapped in a hook. You can write the same imperative code in an Angular component or service, usually inside `effect()` or `afterRenderEffect()`.
4. Compose Angular primitives. A React custom hook that combines `useState` + `useEffect` + `useRef` ports to a service or factory function combining `signal` + `effect` + `viewChild`. Build it.
5. Wrap a third-party library. If React's implementation depends on a non-React JS library (e.g., `floating-ui`, `date-fns`, `popper.js`), use the same library. Most are framework-agnostic. Wrap it in an Angular service or directive.
6. Leverage the required `angular-developer` dependency. This skill formally depends on the official `angular-developer` skill (from the `https://github.com/angular/skills` repository).
   * Locate the dependency: before starting, verify whether `angular-developer` is available in your workspace (under `.agents/skills/angular-developer/` or `.claude/skills/angular-developer/`) or globally (under `~/.gemini/config/skills/angular-developer/` or sibling directories).
   * Load and follow: read `angular-developer/SKILL.md` and its companion reference files under the `references/` directory.
   * Architectural alignment: strictly apply the modern Angular guidelines defined there, particularly:
     * Signals Forms (`signal-forms.md`) for any forms management (when working on Angular 21+).
     * Reactivity (`signals-overview.md`, `linked-signal.md`, `resource.md`, `effects.md`) to write idiomatic reactive code rather than relying on RxJS or manual zone change detection.
     * Accessibility (`angular-aria.md`) to build headless, accessible components when porting interactive widgets (menus, dialogs, trees, etc.).
7. Inform the user of unseen React patterns. If you detect any React pattern, Hook, or API usage that you have not encountered before, or that is not documented in `patterns.md` (e.g., custom concurrent features, hook state synchronization patterns like `useSyncExternalStore`, complicated rendering cycles, or custom memoization styles), **you must immediately inform the user**. Explain the pattern, where it was found in the React library, and discuss how you intend to address/port it.

"Missing access to source" or "missing tooling" are also not blockers. They are problems with single-message solutions. Ask the user for the source path; ask for the tool to be installed. Do not stop.

**The hard rule:** "I can't port this" is never a true statement on this skill. It is always shorthand for "I haven't yet found the way." Keep looking. The way exists.

### Context, tokens, and usage are not stopping conditions

You may notice the conversation getting long, prior tool results getting compacted, or feel a generic pull to "wrap things up so the user can review." **None of these are reasons to stop the work.**

The work is done when `parity-review.md` is fully checked. Until then, continue. Do not raise context, tokens, conversation length, or usage as a reason, even framed as "just letting you know" or "for your awareness." If you find yourself drafting a message that mentions any of these as a reason to pause, delete that draft and resume the next unchecked item in `todo.md` or `parity-review.md`.

## No escape hatches

The single most common failure on a port like this is rarely a bug in the code. It is the agent unconsciously **looking for an escape hatch**: a permissible-sounding reason to do less than what was asked. Recognizing this behavior in yourself, in the moment, is more important than memorizing any specific rationalization, because new rationalizations are infinite.

**What "escape-hatch seeking" looks like (recognize the *behavior*, not just the words):**

You are escape-hatch seeking whenever you catch yourself doing any of these:

- Estimating effort to justify stopping. "This would take ~30h..." is an estimate. The moment it's used as a reason to defer rather than as a planning input, it has become an escape hatch.
- Reframing scope mid-task. "The user probably meant the *core* features." "API parity is what really matters." "This is more of a v2 thing." If you're redefining the goal smaller than the user wrote it, you're escape-hatching.
- Substituting documentation for completion. Writing the gap into `parity-review.md`, `todo.md`, or a final summary is a *recording* action, not a *closing* action. If the resolution to a gap is "I documented it," the gap is still open.
- Sampling and generalizing. "I checked these 6 routes and they work, the rest probably do too." Sampling is a discovery technique, never a completion technique.
- Pre-emptively asking permission to skip. "I could either do X or defer it, let me know", when X was clearly in scope and the user has given no signal they want to defer. That is not asking. It is *manufacturing* a deferral and presenting it as a choice.
- Quality-framing your way down. "Good enough for a first pass." "Ship a beta." "Production-ready for the common cases." These phrases never appear in the user's request, only in your own justifications.
- Tool/access excuses. "The MCP isn't loaded so I'll skip validation." "I couldn't find the demo, so I'll skip Phase 1 step 8." Loading the tool, finding the demo, or asking the user is the actual move, not skipping.
- Spirit-vs-letter arguments. "The spirit of the rule is X, even though the letter says Y." Violating the letter of the rules is violating the spirit of the rules. There is no daylight between them in this skill.

**Why "ask" beats "rationalize":**

- Asking is cheap. One sentence: "Feature X would take ~Nh of mechanical wiring across ~M files. Want me to (a) finish it, (b) defer to a follow-up, (c) drop entirely?" The user answers in seconds.
- Rationalizing is expensive. The work comes back. The user re-runs the skill. You repeat the port. Net cost: 10–100× the cost of asking.
- The user is the only legitimate source of scope changes. You are not.

**The self-check (run this whenever you feel a pull toward stopping early):**

1. *Check whether what I'm about to skip was actually in the original ask.* (If it was, you cannot drop it without permission.)
2. *Watch for words like "concentrated", "deferred", "core", "good enough", "first pass", "documented", "estimated", or "mechanical" used to describe a gap.* (If you catch one, you are escape-hatching.)
3. *Put the permission request into words.* (If you can articulate the question, just ask it. Don't decide for them.)

## The Phases

```
Phase 0: Bootstrap → Phase 1: Discover → Phase 2: Plan → Phase 3: Execute → Phase 4: Parity review
```

Do them in order. Do not skip phase 1, 2, or 4. Without a written feature inventory phase 3 misses exports; without phase 4 you ship a port that *probably* works instead of one you've *proven* works.

---

## Phase 0: Bootstrap the Angular library + demo app

**Goal:** A buildable, empty Angular library scaffold *plus* a demo app that consumes the library, both always prioritizing the use of the most recent, latest version of Angular (v22+ or the latest stable release; verify with `ng version`).

**The demo app earns its place.** The library on its own only proves the code *compiles*. The demo app proves it actually *works*, letting consumers import, render, and interact with each feature. The demo app is the human-runnable verification surface for phase 3 (build passes ≠ feature works) and the place where the user will click around to confirm parity.

**The demo app must cover ALL functionality of the library.** Not a representative sample, not the "happy path", *all of it*. Every public component, directive, service, pipe, and utility. Every input/prop (including each variant, size, theme, boolean toggle). Every output/event. Every state (default, loading, empty, error, disabled, focused, hovered if relevant). Every public method on a service. Every documented option. If a React Storybook story exists for it, the Angular demo must cover at least that surface; ideally more. The demo app is the parity contract made visible.

**Steps:**

1. Confirm the target output directory with the user. Default: a sibling directory next to the React lib named `<react-lib-name>-angular`.
2. Generate a workspace, library, *and* demo app:
   ```bash
   npx --yes @angular/cli@latest new <workspace-name> \
     --create-application=false \
     --package-manager=npm \
     --style=scss \
     --skip-git
   cd <workspace-name>
   npx ng generate library <lib-name>
   npx ng generate application demo --style=scss --routing=true
   ```
   (If the user has a preferred package manager such as pnpm, yarn, or bun, use that.)

   The Angular CLI auto-configures `tsconfig.json` `paths` so `demo` imports the library by its package name (e.g. `import { ... } from '<lib-name>'`) and resolves to the library source, with no publish step needed during development.
3. Make both projects zoneless. Edit `projects/demo/src/app/app.config.ts` and the library's test config:
   ```typescript
   import { provideZonelessChangeDetection } from '@angular/core';
   // in providers array:
   provideZonelessChangeDetection(),
   ```
   Remove `zone.js` from `polyfills` in `angular.json` (both projects) and from `package.json` dependencies.
4. Set OnPush as the default for generated components in `angular.json`:
   ```json
   "schematics": {
     "@schematics/angular:component": {
       "changeDetection": "OnPush",
       "style": "scss",
       "standalone": true
     }
   }
   ```
5. Wire up the demo app's shell. Edit `projects/demo/src/app/app.routes.ts` to be empty for now; phase 3 will add one route per feature. Edit `app.component.html` to render `<router-outlet />` plus a simple sidebar placeholder:
   ```html
   <nav><!-- feature links go here in phase 3 --></nav>
   <main><router-outlet /></main>
   ```
6. Verify both projects build:
   ```bash
   npx ng build <lib-name>
   npx ng build demo
   npx ng serve demo   # smoke test, then Ctrl-C
   ```
   All must succeed before moving on. If any fails, fix it now. Do not carry build errors into phase 3.
7. Initialize git in the workspace and make the first commit: `chore: bootstrap angular library + demo app`. Phase 3 relies on the per-feature commit history.
8. Create the skeleton `README.md` (see *Generated library README* above). Fill in the Origin and Built-with sections immediately. You have the React library path and can resolve its remote URL with `git -C <react-lib-path> remote get-url origin`. Leave the Contributors section as `<!-- TODO: fill in Phase 3.3 -->`. Commit: `docs: add readme with origin and reangular attribution`.

**Exit criteria:** `ng build <lib-name>` passes, `ng build demo` passes, `ng serve demo` boots without runtime errors, git is initialized, zoneless + OnPush defaults are set.

---

## Phase 1: Discover features

**Goal:** A complete map of what the React library does, with each feature linked to its source file(s).

**Process:**

1. Verify dependency presence: check if the required `angular-developer` skill dependency is installed and readable in local skill directories (e.g., `.agents/skills/angular-developer/`, `.claude/skills/angular-developer/`) or global skill directories (e.g., `~/.gemini/config/skills/angular-developer/`). If it is missing, notify the user and recommend installing it via `npx skills add https://github.com/angular/skills --skill angular-developer`.
2. Read the React library's `package.json`. Note: `name`, `version`, `peerDependencies`, `main`/`module`/`exports` (the public API entry points), `types`. The Angular library should match the public API surface unless the user says otherwise.
3. Read the public entry file(s) (whatever `exports`/`main` points to). **Every symbol exported from here is a feature.** Missing one = missing feature parity.
4. For each exported symbol, trace it to its definition and recursively note:
   - Components (props, children handling, refs, default props)
     * *Note: Identify if a React "Component" is a wrapper that does not render much/any additional template elements, but instead serves to add attributes, events, or behaviors to other elements. These are more analogous to Angular directives, and we should prefer directives in these cases to avoid redundant DOM elements.*
   - Hooks (custom hooks → likely become Angular services or signal-based factory functions)
   - Context providers/consumers (→ Angular DI services)
   - Higher-order components (→ Angular directives, host directives, or composition)
   - Render-prop components (→ content projection with `<ng-content>` or `*ngTemplateOutlet`)
   - Utility functions (often portable as-is)
   - Type definitions / interfaces
   - Constants and enums
5. Read `README.md`, examples, and Storybook stories if present. Stories are a goldmine; each story is a documented feature.
6. Read tests. Each test describes a behavior that must continue to hold. Note assertions that imply observable behavior (e.g., "calls onChange with the new value").
7. Note styling approach: CSS Modules, styled-components, emotion, Tailwind, plain CSS, CSS-in-JS. The Angular port will use component-scoped styles by default; styled-components → SCSS in the component's `styles`.
8. Note build setup: bundler (rollup, tsup, vite), output formats (CJS/ESM/UMD), peer dependencies.
9. Run the React lib's demo/example app and explore it organically. This is one of the highest-signal discovery activities; the demo shows you how features actually behave, compose, and feel, which source code alone cannot.
   - Locate it: look for `examples/`, `demo/`, `playground/`, `stories/` (Storybook), `docs/` (docusaurus-style sites with live examples), or a sibling repo. Check the README for "demo" or "playground" links. If the package has a published Storybook (e.g. on Chromatic), use that URL.
   - Start it locally if it's in-repo. Common patterns: `cd examples && npm install && npm start`, `npm run storybook`, `npm run docs`, `npm run dev` from a top-level monorepo.
   - Open it via Chrome DevTools MCP (preferred, scriptable) or via "Claude for Chrome" if installed. Use `new_page` with the demo URL, then `take_snapshot` to see the page structure.
   - Explore it like a user would, not like a developer. Click the nav. Walk every page/route/story. On each:
     * Note what features are demonstrated (this expands your feature list).
     * Note interactions: drag, drop, keyboard nav, hover states, focus traps, modals, popovers.
     * Note edge cases the demo intentionally exposes (long lists, empty states, error states, RTL, theming).
     * `list_console_messages()` after each interaction; sometimes the React demo logs feature-specific events that hint at outputs you'd otherwise miss.
   - Add anything you find here back into your feature map. The React source is the *contract*; the React demo is the *intent*. Both inform the Angular port.
   - Take screenshots of each demo page. You'll use these later in Phase 4 for side-by-side parity comparison.
   - Record the demo's structure (routes, page titles, section layouts). Phase 3 will use this to mirror the layout in the Angular demo so the parity comparison in Phase 4 is straightforward.
   - If no demo app exists: skip this step but rely more heavily on Storybook/tests/README. Note in `todo.md` that the parity review in Phase 4 will not have a side-by-side comparison surface.
10. Detect unseen React patterns:
    - During feature discovery, check if any of the components or hooks utilize React patterns, APIs, or lifecycle behaviors not documented in `patterns.md` (for example, custom concurrent features, hook state synchronization patterns like `useSyncExternalStore`, complicated rendering cycles, or custom memoization styles).
    - If you detect any react pattern that is not in `patterns.md`, **you must immediately inform the user**. Explain what the pattern is, where it is found in the React library, and discuss potential approaches to port it before finalizing your todo checklist and moving to the planning phase.
11. State store strategy: ask the user. If the React library ships its own state store (Redux / Redux Toolkit, Zustand, Jotai, MobX, XState, or a hand-rolled store read via `useSyncExternalStore`), do **not** silently pick an approach. Pause and ask the user which of three strategies they want, because it is their architectural call:
    1. Bridge it (recommended for a faithful port): keep the original store as-is and wrap it in a DI-scoped service that mirrors it into signals. Fastest; reducers/selectors stay byte-identical to React, so behaviour matches by construction. Keeps the dependency; migrate later if ever.
    2. Migrate to `@ngrx/signals`: rewrite slices as a `signalStore`. Idiomatic, batteries-included, drops the React state deps.
    3. Migrate to pure signals: a hand-rolled service of `signal` + `computed` + methods. Lightest, no extra deps, most rewrite.
    Record the chosen strategy in `todo.md`. See `patterns.md` §24 for the code for all three.
12. React-coupled dependencies: ask the user. If the React library depends on *another React library* (one that itself uses React, e.g. `react-smooth`, or a React component/animation/UI lib), as opposed to a framework-agnostic JS lib like `d3` or `date-fns` which you reuse as-is (per step 5 of *Every React feature has an Angular implementation*), it cannot be reused directly. Ask the user which approach they want:
    1. Port the dependency first: run the `reangular` skill on the dependency to produce its own standalone Angular library, then consume that from this port. Best when the dependency is substantial, reused across projects, or worth shipping on its own (e.g. `react-smooth` → `angular-smooth`).
    2. Port only the used subset inline: translate just the functionality this library actually uses into native Angular code inside this port, skipping the rest of the dependency's surface. Best when only a slice is used and a standalone library isn't warranted.
    Record the choice (and for option 1, the dependency's target path) in `todo.md`.

**Output of phase 1:** an in-memory map (or scratch notes) of `{feature → React source file(s) → notes on tricky bits → demo page route (if any)}` plus screenshots of the React demo. You'll write the structured version into phase 2.

**Common discovery pitfalls:**
- Re-exports across barrel files hide features. Follow every `export * from` and `export { x } from`.
- Default exports often differ from the file name. Check what's actually exported.
- "Internal" components used by public components are still features; they need Angular equivalents (even if not exported).
- Generic types and utility types (`type Foo<T> = ...`) often need to come along.
- Reading the source without running the demo. Source tells you what props exist, not how a feature *feels*. A calendar's drag-to-resize, a select's keyboard nav, a tooltip's positioning logic: these are best learned by using them. Always run the demo if one exists.

---

## Phase 2: Write `todo.md`

**Goal:** A flat checklist of every feature, in dependency order, that phase 3 will execute against.

Create `todo.md` at the workspace root (next to `angular.json`). Format:

```markdown
# React → Angular Port: Feature Checklist

Source: <absolute path to react lib>
Target: projects/<lib-name>/src/lib

## Setup & shared
- [ ] Public API surface (`public-api.ts` exports)
- [ ] Shared types/interfaces (list each: `Foo`, `Bar`, ...)
- [ ] Utility functions (list each: `formatX`, `parseY`, ...)
- [ ] Constants and enums

## Services (from React hooks/context)
- [ ] `useTheme` hook → `ThemeService` (signal-based), src: `src/hooks/useTheme.ts`
- [ ] `ThemeContext` → `ThemeService.theme` signal, src: `src/context/ThemeContext.tsx`
- ...

## Components (leaf → composite order)
- [ ] `<Button>`, src: `src/components/Button.tsx`
  - inputs: `variant`, `size`, `disabled`, `onClick`
  - outputs: `clicked`
  - notes: forwardRef → expose `viewChild` from consumers via host element
  - demo: `projects/demo/src/app/pages/button/` (route: `/button`)
- [ ] `<Input>`, src: `src/components/Input.tsx`, demo route: `/input`
- [ ] `<Modal>`, src: `src/components/Modal.tsx` (depends on Portal), demo route: `/modal`
- ...

## Directives (from HOCs/render props)
- [ ] `withTooltip` HOC → `TooltipDirective`, src: `src/hocs/withTooltip.tsx`, demo route: `/tooltip`
- ...

## Tests
- [ ] Port test suite (Jasmine/Karma or Jest based on workspace config)

## Build & publish
- [ ] `ng build <lib-name>` succeeds
- [ ] `ng build demo` succeeds
- [ ] `ng serve demo` boots and every feature's demo route renders without errors
- [ ] `public-api.ts` re-exports match React lib's public surface
- [ ] README updated with Angular usage examples
```

**Rules for the todo:**
- One checkbox per feature. Do not collapse multiple features into one task.
- Order matters: shared types and services first, then leaf components, then composites that depend on them.
- Each component task lists its inputs/outputs/notes inline so phase 3 doesn't re-discover them.
- Reference the React source path for every item. The agent in phase 3 will need to re-read the source.

Commit `todo.md` before starting phase 3: `chore: feature inventory for angular port`.

---

## Phase 3: Execution

**Goal:** Implement every checkbox in `todo.md`. Commit after each feature. Parallelize independent work.

### Step 3.0: Load todos into your task tracker

Read `todo.md`. Add **every** unchecked item as a TodoWrite task. This makes progress visible and forces you to finish the list.

### Step 3.1: Iterate

Work top-down. For each feature:

1. Mark the feature in_progress in TodoWrite.
2. Re-read the React source for this feature (the path is in `todo.md`).
3. Convert using the patterns in `patterns/` (see this directory; read `patterns/index.md` first to locate the right file).
4. Type-check incrementally: run `npx ng build <lib-name>` after each non-trivial component. Don't accumulate errors.
5. Update `public-api.ts` if this feature is part of the public surface.
6. Add a demo page that covers ALL of this feature's functionality.
   - Create `projects/demo/src/app/pages/<feature>/<feature>.page.ts`, a standalone component that imports the library symbol and exhaustively demonstrates every aspect of it.
   - Add a route in `projects/demo/src/app/app.routes.ts`: `{ path: '<feature>', loadComponent: () => import('./pages/<feature>/<feature>.page').then(m => m.<Feature>Page) }`.
   - Add a link to `app.component.html`'s nav.
   - If the React lib has a demo app, mirror its layout for this feature. Match the route name (or use the same slug), section ordering, sample data, and visual structure. Re-open the React demo via Chrome DevTools MCP and snapshot/screenshot the relevant page if you need a reference. The goal is that Phase 4's side-by-side comparison is as easy as "two browsers, same URL slug, look the same." Don't redesign; port. If the React demo's layout has clear flaws, note them in `todo.md` for discussion with the user; don't silently improve.

   **Coverage checklist for the page** (go through this for every feature, not just the obvious ones):
   - Cover every input with one section apiece, showing each meaningful value (each variant, each size, each boolean true/false, required vs optional, with and without defaults). Use signals plus UI controls (buttons, selects, sliders) so the user can flip values live and watch the component react.
   - Wire every output to a visible log/counter on the page so the user can see emissions happen. Don't bind outputs to silent handlers.
   - Show every state: default, loading, empty, error, disabled, readonly, focused, selected, hovered (if behaviorally distinct), and any feature-specific states. For async features, include controls that trigger each state on demand.
   - For every public method (on services or imperative component APIs), add a button that invokes it and shows the result.
   - Cover every slot and projected-content scenario: the component with no content, with simple text content, and with complex/nested content. Show every named slot.
   - Reproduce edge cases that mattered in React: very long content, empty arrays, unicode, RTL if supported, and very large lists for virtualization features.
   - Match the combinations the React lib's Storybook covered: if the React lib has stories, the Angular demo must cover at least the same matrix of variants, ideally laid out similarly.

   **The only features that skip a demo page** are pure type-only exports (interfaces, type aliases with no runtime). Pure utility functions still get a page; show inputs and outputs with sample data.
7. Validate the demo route in a real browser via Chrome DevTools MCP. See the *Chrome DevTools MCP validation protocol* section below for the full procedure. At minimum, for this feature: navigate to its route, take a snapshot, list console messages (must be zero errors), exercise every input/output/state on the page (at least one click per interactive element), re-check console, list network requests (no failed requests). Eyeballing the served page does not count.
8. Tick the box in `todo.md`, changing `- [ ]` to `- [x]` for this feature. Update TodoWrite to completed.
9. Commit feature + demo + todo.md tick together as a single commit:
   ```bash
   git add <feature files> public-api.ts projects/demo/src/app/pages/<feature> projects/demo/src/app/app.routes.ts projects/demo/src/app/app.component.html todo.md
   git commit -m "feat(<lib-name>): port <FeatureName> from react"
   ```

**Rules:**
- One feature = one commit, and **`todo.md` is part of that commit**. The git history must show: at any commit on this branch, `todo.md` accurately reflects what's actually done. Never let `todo.md` drift from the code. A future reader bisecting the branch should be able to trust the checkbox state at every commit.
- Never start a feature whose dependencies are still unchecked. Reorder todos if needed.
- If you discover a feature missed in phase 1, **append to `todo.md` and TodoWrite immediately**, then commit the addition (`chore: add <FeatureName> to todo`) before starting it. Never silently absorb scope.

### Step 3.2: Parallelize with subagents

Many features are independent: leaf components with no shared file edits, isolated utilities, separate services. Dispatch them to subagents **concurrently** using the Agent tool.

**A task is safe to parallelize when:**
- It edits files no other in-flight task touches.
- It does NOT modify `public-api.ts` (the orchestrator owns that file; see below).
- It does NOT modify `package.json` (orchestrator owns).
- Its dependencies (other features) are already committed.

**A task is NOT safe to parallelize when:**
- It modifies shared types/interfaces another task also needs.
- It depends on an in-flight task's output.
- It edits `public-api.ts`, `angular.json`, or `package.json`.

**Dispatching subagents (fire them concurrently, not serially):**

The whole point of parallelization is that subagents run *at the same time*. To do that, you must put **multiple `Agent` tool calls in a single assistant message**. Tool calls in the same message execute concurrently; tool calls split across messages execute one after another.

```
✅ DO: one message containing N Agent tool calls fires N subagents in parallel:
   [assistant message]
     Agent(...)  ← Button port
     Agent(...)  ← Input port
     Agent(...)  ← Modal port
     Agent(...)  ← Tooltip directive

❌ DON'T: sending one Agent, waiting for it to return, then sending the next:
   [assistant message] Agent(...)  ← Button
   [tool result]
   [assistant message] Agent(...)  ← Input    ← this is sequential, not parallel
   [tool result]
   ...
```

If you're typing one tool call and hitting send, you're doing it serially. Stop, batch every safe-to-parallelize task you've identified, and send them together.

**Practical batch size:** pick 3–5 independent features per round and fire them in one message. After they all return, integrate (next section), then fire the next batch. Beyond ~5 concurrent subagents, conflict-resolution overhead outweighs the speedup.

**When to NOT batch (the dependency chain):** if feature B imports a type from feature A, A must be committed *before* B is dispatched. Build batches from the dependency graph: round 1 = all leaves with no in-flight dependencies; round 2 = features that depend only on round-1 outputs; and so on. The todo's leaf-to-composite ordering from phase 2 makes this easy.

Each subagent prompt must be self-contained:

```
You are porting a single React feature to Angular AND building its demo page.

Source file: <absolute path to React file>
Library target: projects/<lib>/src/lib/<dest-path>
Demo target: projects/demo/src/app/pages/<feature>/
Feature: <name>
Inputs/outputs/notes: <copy from todo.md>

Conversion rules: read /Users/.../reangular/patterns/index.md to identify which pattern files apply, load those files, and follow the guidelines in the `angular-developer` dependency skill.
Constraints:
- standalone component, OnPush, signals only
- no NgModules, no Zone.js, no *ngIf/*ngFor
- you MAY create files in projects/<lib>/src/lib/<dest-path>/ AND projects/demo/src/app/pages/<feature>/
- do NOT touch any other files. In particular: do NOT modify public-api.ts, package.json, angular.json, todo.md, app.routes.ts, app.component.html, or any other feature's folder
- the demo page must import the library symbol via the package name (e.g. `import { ... } from '<lib-name>'`) and EXHAUSTIVELY cover the feature:
  * every input: one section per input, showing every meaningful value (each variant/size/boolean true+false/required+optional). Use live UI controls so values can be flipped at runtime
  * every output: bind each to a visible log/counter on the page so emissions are observable
  * every state: default, loading, empty, error, disabled, readonly, focused, plus any feature-specific states. Include controls to trigger each on demand
  * every public method: a button per method that invokes it and shows the result
  * every slot / projected content scenario: empty, simple, complex
  * edge cases the React lib cared about: long content, empty arrays, large lists if virtualized
  * if the React lib has Storybook stories for this feature, match or exceed that matrix of variants
- run `ng build <lib>` before reporting done; report failures verbatim

Report: list of files created/modified, exported symbols, demo page component class name, and a coverage list for the demo page (which inputs/outputs/states/methods you demoed and any you intentionally skipped with reason). Any deviations from the React API and why.
```

**Why subagents do not touch `todo.md`, `app.routes.ts`, or `app.component.html`:** parallel writes to the same file conflict. The orchestrator owns these shared files. Subagents create the demo page *component* in their scoped folder; the orchestrator wires up the *route registration* and *nav link* when integrating their work. See below.

**Conflict resolution + commit when subagents return:**

After all subagents complete, the orchestrator integrates their work one subagent at a time, so each commit stays atomic:

1. Run `git status` to see all modified files.
2. For each subagent's reported file list, verify no two subagents touched the same file. If they did, read both and reconcile manually.
3. Type-check the union: `npx ng build <lib>`. If it fails, the conflict is real (usually duplicate type definitions or import cycles). Resolve by:
   - Hoisting shared types into a single `types.ts` file (commit as a separate setup task).
   - Removing duplicate utilities (keep the more complete version).
4. For each subagent's feature, the orchestrator wires the demo route + nav link (subagents created the demo page component but not the registration):
   - Append a route to `projects/demo/src/app/app.routes.ts`: `{ path: '<feature>', loadComponent: () => import('./pages/<feature>/<feature>.page').then(m => m.<Feature>Page) }`.
   - Append a nav link to `projects/demo/src/app/app.component.html`.
   - `npx ng build demo` must pass.
5. Validate each integrated feature in a real browser via Chrome DevTools MCP (see the *Chrome DevTools MCP validation protocol* section below). Subagents do not run MCP validation (they don't have the dev server running); the orchestrator runs it once per integrated feature before committing.
6. Commit feature files + demo page + route registration + todo.md tick + public-api.ts update together:
   ```bash
   # tick this subagent's feature in todo.md (edit the file)
   git add <subagent's files> todo.md public-api.ts \
     projects/demo/src/app/app.routes.ts \
     projects/demo/src/app/app.component.html
   git commit -m "feat(<lib-name>): port <FeatureName> from react"
   ```
   Do this once per subagent so history stays granular and `todo.md` matches the code at every commit.
6. If conflicts forced a reconciliation, add a `fix:` commit on top (no `todo.md` change, the boxes are already ticked).

### Chrome DevTools MCP validation protocol

This protocol is referenced from Step 3.1, Step 3.2, and Step 3.3. Building and serving prove the code compiles. Chrome DevTools MCP validation proves it actually *runs* in a real browser without errors. This is part of the success criteria, not optional.

**Setup (once per session):**

1. Confirm the Chrome DevTools MCP tools are available. They appear in the deferred tools list as `mcp__plugin_chrome-devtools-mcp_chrome-devtools__*`. Load schemas with `ToolSearch(query: "select:...")` for the tools you need (start with `new_page`, `navigate_page`, `take_snapshot`, `list_console_messages`, `list_network_requests`, `click`, `fill`, `wait_for`).
   - If the tools are NOT available in this environment, surface this to the user before declaring done. The success criteria require MCP validation; without it, the work is not complete. Do not silently substitute manual `ng serve` clicking.
   - If you need broader guidance on the toolchain, the `chrome-devtools-mcp:chrome-devtools` skill is available; invoke it via Skill.
2. Start the demo server in the background:
   ```bash
   # from workspace root, run with run_in_background=true
   npx ng serve demo --port 4200
   ```
   Wait for "Local: http://localhost:4200/" before proceeding (use `wait_for` on the dev server output, or poll with a short Bash check).
3. Open a page: `new_page(url: "http://localhost:4200/")`.

**Per-feature validation protocol:**

For each feature route on the branch (every `- [x]` item in `todo.md` that has a `demo route`):

1. `navigate_page(url: "http://localhost:4200/<feature>")`
2. `wait_for(text: "<a stable string from the demo page>")` confirms the route mounted.
3. `take_snapshot()` gives you the accessibility tree with element UIDs.
4. `list_console_messages()` **must return zero errors and zero warnings from library code**. React-style hydration warnings, NG0xxx errors, missing-input errors, signal-write-in-effect errors all count as failures. Record the exact message and fix before continuing.
5. Exercise the demo's coverage for every interactive control on the page (one per input, one per output, one per state-trigger, one per public method):
   - `click(uid: ...)` or `fill(uid: ..., value: ...)` to exercise it.
   - After each interaction, `list_console_messages()` again; still zero errors.
   - For outputs: confirm the on-page log/counter you wired up actually updated (re-snapshot and check the text).
6. `list_network_requests()` should show no 4xx/5xx responses from library-initiated requests. (Static asset 404s for fonts/images you didn't port count too; fix or document.)
7. `take_screenshot()` after the full pass, useful for the user to spot-check visual parity later.

**Per-feature pass criteria:** zero console errors/warnings, every interactive control was exercised, every output observed firing, no failed network requests.

**When validation fails:** the feature is not done. Stop, fix the underlying bug (do NOT silence the warning, do NOT skip the route), re-run validation, and only then move on. If the failure was caught after the per-feature commit, add a `fix:` commit with the fix and the same MCP re-validation.

**Teardown:** stop the background `ng serve`, close the page (`close_page`).

**When to run this:**
- Per-feature during step 3.1 (sequential path) and step 3.2 (subagent integration path): a quick targeted check on the just-added route, before the per-feature commit.
- Full sweep during step 3.3: every route, every interaction, before declaring done.

### Step 3.3: Final verification

Once `todo.md` is fully checked:

1. `npx ng build <lib-name>` must succeed with zero errors and zero warnings (treat warnings as failures unless explicitly accepted).
2. `npx ng build demo` must succeed.
3. Run a full Chrome DevTools MCP sweep of the demo app per the *Chrome DevTools MCP validation protocol* section above. Every route. Every interactive control. Zero console errors. Zero failed network requests. Every output observed firing. Cross-reference against the feature's notes in `todo.md` and against the React lib's Storybook stories (if any); every story must have at least equivalent coverage. A route that only demos the happy path, or one that has *any* console errors, is not done.
4. Diff the React lib's public exports against `public-api.ts`. Every public React symbol must have a corresponding Angular export. Missing exports = missing feature parity = not done.
5. If the React lib had tests, ensure the Angular tests cover equivalent behavior. Run them: `npx ng test <lib-name> --watch=false`.
6. Finalize `README.md` (see *Generated library README* above):
   - Run `git -C <react-lib-path> shortlog -sn --no-merges HEAD` to extract the full contributor list sorted by commit count.
   - Replace the Contributors placeholder with the full ordered list, including commit counts.
   - Verify the Origin link and the reangular attribution link are present and correct.
   - Commit: `docs: finalize readme with contributor list`.
7. Final commit: `chore: phase 3 execution complete, entering parity review`.

After step 6, do not declare the project done. Move to Phase 4.

---

## Phase 4: Parity review (side-by-side demo comparison)

**Goal:** Confirm the Angular library's behavior matches the React library's behavior by walking both demos in parallel and comparing them feature by feature. This is the final gate before declaring feature parity. Skipping it means shipping a port that *probably* matches.

**This phase is separate from phase 3's validation for a reason.** Phase 3.3's MCP sweep only proved the Angular demo works *in isolation* (no console errors, every control fires). Phase 4 proves it works *the same as React*. These are different questions. A button can have zero console errors and still emit the wrong event. A list can render and still sort items in a different order. Only side-by-side comparison catches these.

**Skip this phase ONLY if** the React lib has no demo app, no Storybook, and no published examples. In that case, phase 3.3 + the public-API diff are the best you can do. Flag this gap to the user and proceed.

**Setup:**

1. Start both demos. Use two terminals or two background processes:
   ```bash
   # React demo (path discovered in Phase 1)
   cd <react-demo-dir> && npm start    # often http://localhost:3000
   # Angular demo (workspace root)
   npx ng serve demo --port 4200       # http://localhost:4200
   ```
2. Open both in Chrome DevTools MCP as two pages, side by side. Use `new_page` twice and `select_page` to switch focus. (If "Claude for Chrome" is installed, you can use it as an alternative.)
3. Confirm both load. Run `list_console_messages()` on each; if either is broken at the home route, fix that first.

**Comparison protocol (for each feature in `todo.md`):**

1. Same slug, both apps. Navigate the React tab to `http://localhost:3000/<feature-slug>` and the Angular tab to `http://localhost:4200/<feature-slug>`. (If you mirrored layouts in Phase 3.1, the URLs match. If they don't, look up the equivalent React URL from your Phase 1 notes.)
2. Snapshot both with `take_snapshot()` on each page. Compare structure: confirm the same sections, labels, and controls are present.
3. Take screenshots of both with `take_screenshot()` on each. Visual diff (eyeball or pixel-diff if available). Note discrepancies in:
   - Layout / spacing / sizing
   - Colors and typography that the library controls (not the demo's chrome)
   - Iconography, default content, placeholder text
4. Walk every interactive control on the React demo, then perform the *same* interaction on the Angular demo. For each:
   - Click/fill/drag the React control. Observe the result (what changes visually, what console output appears, what network request fires).
   - Do the same on the Angular control, and confirm it produces the same observable result.
   - For drag-and-drop, animations, transitions: observe timing and trajectory. Significant differences are bugs.
   - For events: confirm the Angular output emitted with an equivalent payload to the React callback's argument.
5. Test edge cases the React demo exposes: empty states, max-length content, rapid clicks, keyboard navigation (Tab, Arrow keys, Enter, Esc). Anything the React demo handles correctly that the Angular demo doesn't is a parity gap.
6. Record findings in `parity-review.md` at the workspace root, one section per feature:
   ```markdown
   ## <FeatureName>
   - [x] Visual layout matches
   - [x] All inputs render and behave the same
   - [ ] Output `(selectionChange)` fires with `{id, label}` in React but only `{id}` in Angular ← FIX
   - [x] Keyboard nav matches
   - Screenshots: react-screenshots/<feature>.png, angular-screenshots/<feature>.png
   ```

**Resolving gaps:**

- For each unchecked item in `parity-review.md`, fix the Angular code. This re-enters Phase 3.1's iteration loop for just that feature: reproduce the bug, fix, re-run MCP validation, commit. The commit message: `fix(<lib-name>): match React parity for <FeatureName>: <gap>`.
- After fixing, re-run the parity comparison for that feature only. Tick the box.
- Loop until every box in `parity-review.md` is checked.

**Phase 4 exit criteria (all must hold simultaneously):**

- Every feature has a section in `parity-review.md`.
- Every box in `parity-review.md` is `[x]`. Not "most." Not "the important ones." Every. One. An unchecked box means the project is incomplete (see *The parity bar* above).
- A final MCP sweep of the Angular demo passes (re-run Phase 3.3's protocol).
- Final commit: `chore: feature parity complete, phase 4 reviewed`.

**Definition of done. All checkboxes must be ticked, none can be partially-passing.**
- [ ] `todo.md` has every item checked. (Not "most items"; every item. If you discovered a feature mid-port and the user authorized deferral, the deferral is recorded next to the unchecked item with the user's name.)
- [ ] `ng build <lib-name>` succeeds with zero errors and zero warnings.
- [ ] `ng build demo` succeeds with zero errors and zero warnings.
- [ ] **Every** feature route (not a sample, not "the main ones") was validated end-to-end in Chrome DevTools MCP: zero console errors, zero failed network requests, every input/output/state/method exercised, every output observed firing. If you have N routes in the demo, you ran the protocol N times.
- [ ] Public API surface matches React lib (count and names of exports). Every public React export has a corresponding Angular export.
- [ ] Tests pass (if ported).
- [ ] `README.md` is present at the workspace root and contains all three required sections: Origin (with link to the React library's source repo), Built-with reangular attribution (with link to `https://github.com/aleksanderbodurri/reangular`), and the full sorted Contributors list extracted from the React library's git history.
- [ ] `parity-review.md` exists with a section per feature, **every box checked**. (The only exception: the React lib has no demo, no Storybook, and no published examples to compare against. In that case, `parity-review.md` contains a note documenting that, and Phase 3.3's MCP sweep + the public-API diff are the parity contract.)

**A partial pass on any of these means the project is not done.** Do not declare completion with caveats like "API parity is at 100% but visual parity is at 80%", "the remaining work is mechanical", "the architectural pattern is identified", or "I documented the gaps". Those are status updates, not completion. Go back to the relevant phase and finish the work, or, if you genuinely cannot, stop and ask the user how to proceed (see *The parity bar* for the only legitimate stopping points).

**Reporting unfinished work:** if for any reason you must stop before parity is complete, do not write a summary that conflates documenting gaps with closing them. Use plain language: "Parity is **not** complete. The following features are unfinished: [list]. The following demo routes were not validated: [list]. To finish: [steps]." The user needs an accurate picture, not a euphemism.

---

## Conversion patterns

The full React → modern Angular pattern reference is in `patterns/` in this directory. Read `patterns/index.md` before phase 3; it maps every conversion topic to its file. Re-consult it when you hit an unfamiliar React API to find the right file to load.

## Component porting checklist

Run through this for every component you port:

- [ ] `standalone: true`, `changeDetection: OnPush`
- [ ] Props → `input()` with proper types and defaults
- [ ] Callbacks → `output()` (or `model()` for two-way)
- [ ] State → `signal()`
- [ ] Derived → `computed()`
- [ ] Effects → `effect()` with cleanup if needed
- [ ] Refs → `viewChild()` / `contentChild()`
- [ ] Conditional → `@if`
- [ ] Lists → `@for ... track`
- [ ] Children → `<ng-content>` (named slots if needed)
- [ ] Wrapper components without templates → Directives
- [ ] SVG components use attribute selectors (`g[lib-x]`, `path[lib-x]`); SVG tags in templates are `svg:`-prefixed; dynamic geometry uses `[attr.*]`
- [ ] Default exports re-exported in `public-api.ts`
- [ ] Types exported alongside the component

## Mindset shift

The biggest trap when porting React → Angular is reaching for patterns that are no longer idiomatic in modern Angular:

- Don't reach for RxJS by default. Signals replace most observable use cases inside components. Only use RxJS when integrating with `HttpClient` or genuinely event-streamed data, and even then, prefer `toSignal()` at the component boundary.
- Don't write NgModules. All components/directives/pipes are standalone.
- Don't use Zone.js APIs. `setTimeout`/`setInterval` work fine with signals; you do not need `NgZone.run()`.
- Don't use `*ngIf`/`*ngFor`. Use `@if`/`@for`. Lint for the old syntax.
- Never use decorator-based APIs (`@Input()`, `@Output()`, `@ViewChild()`, `@ViewChildren()`, `@ContentChild()`, `@ContentChildren()`). Always use their modern, signal-based equivalents (`input()`, `model()`, `output()`, `viewChild()`, `viewChildren()`, `contentChild()`, `contentChildren()`).
- Don't use constructor injection. Use `inject()`.
- Don't hand-roll primitives the Angular CDK already provides. When porting a React feature whose React implementation re-invented something low-level (drag-and-drop, focus trap, overlay positioning, virtual scrolling, portals, RTL, keyboard menu nav), reach for `@angular/cdk` first. Wrap the CDK primitive to expose the React library's API shape; don't re-implement the underlying mechanics.

  Map of common React → CDK substitutions:

  | React lib does this... | Use this CDK primitive |
  |---|---|
  | Drag-and-drop (react-dnd, react-beautiful-dnd, dnd-kit, custom mouse-event DnD) | `@angular/cdk/drag-drop` (`cdkDrag`, `cdkDropList`, `cdkDragHandle`, `CdkDragDrop` event) |
  | Modal / dialog / popover positioning | `@angular/cdk/overlay` (`Overlay`, `OverlayRef`, position strategies) |
  | Portal-rendered content (`createPortal`) | `@angular/cdk/portal` (`TemplatePortal`, `ComponentPortal`, `DomPortalOutlet`) |
  | Focus trap / focus management | `@angular/cdk/a11y` (`FocusTrap`, `FocusMonitor`, `LiveAnnouncer`) |
  | Virtual scrolling for large lists | `@angular/cdk/scrolling` (`cdk-virtual-scroll-viewport`) |
  | Breakpoint / media query observation | `@angular/cdk/layout` (`BreakpointObserver`) |
  | Copy to clipboard | `@angular/cdk/clipboard` |
  | Menu / listbox / combobox primitives | `@angular/cdk/menu`, `@angular/cdk/listbox` |
  | Dialog | `@angular/cdk/dialog` |
  | Autosize textarea | `@angular/cdk/text-field` (`cdkTextareaAutosize`) |
  | RTL detection | `@angular/cdk/bidi` (`Directionality`) |
  | Keycode constants for keyboard handling | `@angular/cdk/keycodes` |

  Install when needed: `npm install @angular/cdk`. The CDK is unstyled, which is perfect for a library port because you keep the React lib's existing visual design while inheriting battle-tested behavior, accessibility, and keyboard support. See `patterns.md` §21 for a worked drag-and-drop example.

The fundamental shift: React re-renders top-down on state change; Angular with signals propagates change through a reactive graph and only re-renders the components that read changed signals. Components don't "re-render" in the React sense; the template's bindings re-evaluate where signals are read.

## Common pitfalls

| Pitfall | Why it happens | Fix |
|---|---|---|
| `forwardRef` patterns lost in port | React's ref forwarding has no direct equivalent | Expose imperative API via a public method on the component class; consumers use `viewChild()` to call it |
| Children prop ignored | React's `{children}` has no signal equivalent | Use `<ng-content>` for default slot, named slots via `<ng-content select="...">` or `*ngTemplateOutlet` for parameterized content |
| Default props missed | React's `defaultProps` or destructuring defaults | Pass default to `input()`: `size = input<'sm' \| 'md'>('md')` |
| Boolean props silently typed wrong | React accepts `disabled` (presence), Angular `input(false)` requires explicit binding | Use `input(false, { transform: booleanAttribute })` for HTML-attribute-style booleans |
| `useEffect` cleanup forgotten | Easy to translate the body but skip the return function | `effect((onCleanup) => { ...; onCleanup(() => ...) })` |
| Context value identity changes cause re-renders | Not an Angular concern with signals | Just expose individual signals from the service; consumers read what they need |
| Keys/track mismatch | `@for` requires `track` (compiler-enforced) | Use `track item.id` if available, else `track $index` (only when items are stable) |
| Missing public export | Barrel file in React not mirrored | Diff React's public exports against `public-api.ts` at the end of phase 3 |
| Build passes but library bundle is broken | Forgot `ng-packagr` peer dep version mismatch | Always `ng build <lib>` and inspect `dist/<lib>/package.json` |

## Red flags: STOP

If you find yourself doing any of these, stop and reconsider:

- Skipping phase 1 because "I'll discover as I go" → you will miss exports. Always do phase 1.
- Lumping multiple features into one commit → you've lost the audit trail. One feature = one commit.
- Committing a feature without ticking `todo.md` in the same commit → `todo.md` is now lying about the state of the code. Amend or follow up immediately; better, never let it happen.
- Ticking `todo.md` in a commit *separate* from the feature → same problem in reverse. The two changes belong together.
- Marking todos done without `ng build` passing → not done.
- Adding RxJS to convert a `useState` → use `signal`.
- Writing an `NgModule` → use standalone.
- Writing `*ngIf` → use `@if`.
- Subagents touching `public-api.ts` or `todo.md` → orchestrator owns both; reassign.
- Dispatching subagents one per assistant message and waiting for each → that's sequential, not parallel. Batch every independent task into a single message with multiple `Agent` calls.
- "I'll fix that export later" → fix it now or it will be missed.
- Skipping the demo page because "the build passes" → the build passing only proves the code compiles. The demo page is the proof that the feature actually *works* end-to-end. Add it.
- Building all the demo pages at the very end as one big commit → the per-feature commit must include its demo page, so each commit is a complete, demoable slice.
- Demo page only shows the "happy path" or one variant → not done. The demo must cover EVERY input, output, state, variant, and public method. Walk the coverage checklist (Phase 3.1 step 6) before ticking the todo.
- "I'll add the other variants/states later" → no. The feature isn't complete until its demo demonstrates all of it. Catching a missing input now is cheaper than rediscovering it during user QA.
- "`ng serve` started without errors, that's enough" → no, that only proves the bundle compiled. Open the route in Chrome DevTools MCP, exercise every control, and confirm zero console errors and zero failed network requests. Compile-passing ≠ runtime-passing.
- Skipping MCP validation because "the page looked fine when I checked manually" → manual checking is not evidence. The success criteria require automated browser validation with verifiable console + network output.
- Console warnings dismissed as "harmless" without reading them → many Angular runtime errors surface as console warnings (NG0xxx codes, expression-changed-after-checked, signal-write-in-effect). Read the message. Fix the root cause.
- Skipping MCP validation because "the tools aren't loaded" → use ToolSearch to load the Chrome DevTools MCP tools. If they genuinely aren't available in the environment, surface that to the user; don't silently substitute manual verification.
- Skipping the React demo exploration in Phase 1 because "I read the source" → the source is the contract; the demo is the intent. Drag, keyboard nav, animation timing, and feature composition are barely visible in source. Always run the demo if one exists.
- Designing the Angular demo from scratch instead of mirroring the React demo → the parity review depends on side-by-side comparison. If your demo is structured differently, you're either redoing the comparison work or skipping it.
- Declaring "feature parity" after Phase 3 without doing Phase 4 → Phase 3.3's sweep proves the demo *works*; Phase 4 proves it *matches*. Different questions. Different bugs. You don't know parity until you've compared.
- Hand-rolling drag-and-drop primitives in Angular → use `@angular/cdk/drag-drop`. The Angular team has solved this with first-class accessibility, keyboard support, and constraint APIs. Wrap CDK to expose the React lib's API shape; don't re-implement the underlying DnD logic.

### Red flags specific to "almost done" rationalization

These are the ways the parity bar gets eroded. If you catch yourself thinking, writing, or saying any of these, **stop and re-read *The parity bar* section.** You are about to declare done when you are not done.

| If you find yourself writing... | What to do |
|---|---|
| "API parity ~100%, runtime/visual parity ~80%" | There is one parity. Keep working until the second number is also 100. |
| "The remaining work is concentrated in one architectural change" | Then make the change. Identifying it is not finishing it. |
| "~30h of mechanical leaf wiring" or any other effort estimate as a justification for stopping | Effort estimates are for planning, not for closure. Do the work. |
| "Validated end-to-end" when only a subset of routes was validated | Re-read what you wrote. If only 6 of 56 routes were checked, "validated end-to-end" is false. Validate every route or say so plainly. |
| "Outstanding (documented in parity-review.md): ..." in a completion summary | Outstanding ≠ complete. If there's an outstanding list, the project is not complete. Either close the list or report explicitly that parity is *not* achieved. |
| "Most widely-used features have an equivalent" | The user did not ask for "widely-used features." They asked for the library. Port the rest. |
| "Deferred", and the user did not authorize the deferral | Only the user can defer scope. Ask, get an explicit yes, and record it in `todo.md` with their name. Otherwise, finish the feature. |
| "Good for a first pass" / "good enough to ship a beta" | The skill has no first-pass mode. Continue to full parity, or stop and ask the user how to scope down explicitly.
