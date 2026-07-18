---
name: leptos-islands
description: Apply Leptos 0.8+ Islands architecture to enterprise SSR applications — admin panels, CRUD systems, PBX/callcenter dashboards, table-heavy management UIs. Auto-triggers when adding `#[island]`/`#[component]`, designing hydration boundaries, building modals/sheets/dialogs/forms, debugging dead buttons or dead inputs, configuring `leptos/islands`, or sizing WASM. Enforces SSR-first, static-by-default, hydrate-only-the-interactive-ownership-boundary discipline.
---

# Leptos Islands — Enterprise SSR Architecture

This skill is written for SSR-first enterprise applications: admin consoles, CRUD systems, PBX/callcenter dashboards, supervisor panels, reporting UIs, settings pages. Islands are the **correct default** for these apps. The job is not to "decide whether to use islands" — it is to **decide where the hydration boundary goes**.

## Core Mental Model — read this before anything else

In Islands mode (`leptos/islands` enabled — formerly `experimental-islands` in 0.7), the two attributes mean fundamentally different things:

| Attribute | Where it runs | Reactivity | Event handlers | WASM cost | When to use |
|---|---|---|---|---|---|
| `#[component]` | **Server only.** Renders HTML, then nothing. | None on client. Signals do not update. | `on:click` / `on:input` **do NOT attach.** | Zero. Not shipped. | Layouts, shells, wrappers, cards, typography, static tables, server-rendered detail panes, page chrome. |
| `#[island]` | Server-renders, then **hydrates on the client.** | Full client reactivity. | Attach and fire. | Ships WASM for this subtree. | Forms, modals, sheets, dropdowns, filters, tabs, accordions, toggles, pagination, row actions, toolbars, search inputs — anything with local interactivity. |

**The single most common bug in this codebase is putting interactive markup (`on:click`, signals, `RwSignal`, dropdowns) inside `#[component]` and expecting it to work.** It will not. Event handlers silently fail to attach. Inputs look fine but never fire `on:input`. Buttons render but do nothing.

**The single correct rule:**

```text
Hydration boundaries follow ownership boundaries,
not file/component/code-organization boundaries.
```

Corollaries:

```text
Do NOT hydrate entire pages.
Hydrate only the interactive ownership boundaries.
Do NOT split one ownership tree across multiple islands.
A reusable interactive UI helper does NOT automatically need its own #[island].
```

The whole page is `#[component]`. The roots of independent interactive ownership trees inside it are `#[island]`. Reusable interactive helpers called from inside those islands are usually plain `fn ... -> impl IntoView`.

## Four Different Boundaries — keep them straight

The most common architectural error in this codebase is collapsing these four concepts into one:

| Boundary kind | What it is | Marker in code | Question it answers |
|---|---|---|---|
| **Hydration boundary** | Where SSR HTML hands off to client WASM | `#[island]` attribute | "What subtree ships WASM and runs handlers/signals?" |
| **Component boundary** | Where a Rust function is called via `view! { <Foo … /> }` | `#[component]` or `#[island]` attribute | "What is the reusable view function?" |
| **Ownership boundary** | What nodes share signals/state/handlers | Shared `RwSignal`, modal open state, form fields | "Who reacts to whom?" |
| **Code-organization boundary** | Where source code is split for readability/reuse | `fn`, `pub fn`, separate file/module | "How is this code arranged?" |

These are **independent axes**. A single ownership tree can be:
- One hydration boundary (one `#[island]`).
- Composed of many component boundaries (functions called from the island's `view!`).
- Spread across many code-organization boundaries (helpers in separate modules/files).

What is **NOT** legal:
- Splitting one ownership tree across multiple **hydration boundaries**. A shared `RwSignal` cannot serialize across two sibling `#[island]` instances; the topology breaks.
- Putting interactive markup under a `#[component]` boundary inside or outside an island (a `#[component]` is server-only — interactivity dies).

### The recurring mistake

When developers feel a piece of UI is "reusable" or "self-contained" they instinctively reach for `#[island]` (mirroring React's habit of making every reusable interactive piece a top-level component). Under Leptos islands this *fragments* the ownership tree: each `#[island]` is an **independent hydration root** that gets its own hydration handoff. A `RwSignal<bool>` passed as a prop from one island to a sibling island is not "shared state" — it is two separate islands instantiated with independent reactive runtimes.

The correct move when extracting a reusable interactive helper is almost always a **plain function**, not a `#[island]`.

## When to Use Islands — corrected guidance

Islands are **ideal** for enterprise SSR apps when:

- Layouts are mostly static (sidebars, headers, page chrome).
- Tables render from server data with server-side sort/filter/pagination.
- Interactivity is localized to specific regions (filters, row actions, sheets).
- Modals/sheets/forms are self-contained ownership trees.
- Hydration boundaries are designed intentionally rather than accidentally.

Examples that **should** use islands:

- ✅ Admin panels
- ✅ CRUD systems (Business Units, Agents, Campaigns, Leads, DNC, …)
- ✅ PBX/callcenter dashboards
- ✅ Supervisor real-time consoles
- ✅ Reporting systems
- ✅ Settings pages
- ✅ Table-heavy enterprise UIs with sheet-based CRUD

The earlier rule of thumb "if most of the page is interactive, skip islands" is **wrong for this codebase**. In a CRUD admin page the *page shell* is static; the interactivity is concentrated in a filter panel, the row action menu, and the create/edit sheet. Each of those is one island. The table body, headers, layout, page title, and surrounding content remain `#[component]` (zero WASM). Total hydrated surface is small even though the page "feels" highly interactive.

Skip islands only when every region of the page is reactive against the same global state and there is no static surface to keep server-only — which is rare in admin tooling.

## Hydration Ownership Boundaries — the load-bearing concept

An **interactive ownership tree** is the set of nodes that share *any* of:

- a signal (`RwSignal`, `Signal`, `Memo`, `Resource`)
- modal/dialog/sheet open-state
- an event handler that mutates shared state
- an input that another node reads
- a derived value that another node uses
- a reactive effect (`Effect::new`)

**Every node in a single ownership tree MUST live inside the same island subtree.**

If you split an ownership tree across an island boundary, the island half hydrates and the `#[component]` half does not — handlers never attach, signals never propagate, and you get the symptoms in the Debugging section below.

### Concrete consequence

Given this interactive flow:

```text
[trigger button] → opens [modal/sheet] → contains [form] → contains [inputs]
                                       → contains [save button] → calls [server action]
                                       → contains [cancel button] → closes modal
```

This is **one ownership tree**. The trigger button shares `open: RwSignal<bool>` with the modal; the form inputs share field signals with the save button; the save button reads form state to call the server action. **All of it lives inside one `#[island]`.**

Do NOT:

- Make the trigger button an `#[island]` and the modal content a `#[component]`.
- Render the modal portal outside the island's ownership using a top-level `<Portal>` that escapes the island subtree.
- Hoist the form into a sibling island and the buttons into the parent.
- Split a tabbed sheet so each tab is a separate island that owns one signal each — the tabs need to coordinate.

## Modals, Sheets, Dialogs, Drawers, Popovers

These are the most common place ownership gets accidentally split. The rule:

> **The trigger, the open-state, the modal/sheet content, the form, the inputs, and the action buttons belong to the SAME island subtree.**

### Broken pattern — DO NOT do this

```rust
// BROKEN — trigger is hydrated, modal content is not
#[island]
pub fn OpenSheetButton(open: RwSignal<bool>) -> impl IntoView {
    view! { <button on:click=move |_| open.set(true)>"New Business Unit"</button> }
}

#[component] // ← STATIC. Inputs and buttons inside will NOT work.
pub fn BusinessUnitSheetContent(open: RwSignal<bool>) -> impl IntoView {
    let name = RwSignal::new(String::new()); // never reactive
    view! {
        <Sheet open=open>
            <input on:input=move |ev| name.set(event_target_value(&ev)) /> // dead
            <button on:click=move |_| { /* save */ }>"Save"</button>      // dead
        </Sheet>
    }
}
```

Symptoms: sheet opens, inputs render, typing does nothing, Save does nothing, console may show no error at all.

### Correct pattern — one island owns the whole flow

```rust
#[island]
pub fn BusinessUnitSheetIsland(initial: Option<BusinessUnit>) -> impl IntoView {
    let open = RwSignal::new(false);
    let name = RwSignal::new(initial.as_ref().map(|b| b.name.clone()).unwrap_or_default());
    let save = ServerAction::<UpsertBusinessUnit>::new();

    view! {
        <button on:click=move |_| open.set(true)>"New Business Unit"</button>
        <Sheet open=open on_close=move || open.set(false)>
            <ActionForm action=save>
                <input
                    name="name"
                    prop:value=move || name.get()
                    on:input=move |ev| name.set(event_target_value(&ev))
                />
                <button type="button" on:click=move |_| open.set(false)>"Cancel"</button>
                <button type="submit" disabled=move || save.pending().get()>"Save"</button>
            </ActionForm>
        </Sheet>
    }
}
```

The island encapsulates: trigger, open-state, form state, both action buttons, the submit pathway. The page calls `<BusinessUnitSheetIsland />` from its `#[component]` shell and that is the entire hydration boundary for this flow.

### Portals

If a modal renders into a portal root (`document.body`), Leptos still tracks ownership through the reactive system — but **only if the portal is created from inside an island's render tree**. Calling `<Portal>` from a `#[component]` will render the portal contents server-side as static HTML and lose interactivity. Keep portals inside the island.

## Interactive Helper Functions — the right way to decompose an island

When an island grows large you decompose it. The decomposition is a **code-organization boundary**, not a hydration boundary. The correct tool is a **plain Rust function** that returns `impl IntoView` and accepts the parent island's signals as parameters.

This is distinct from the `Children` / `ChildrenFn` mechanism described in "Children passed into islands are server-rendered" below. Children are static HTML serialized once at SSR; helper functions are inlined into the island's reactive view tree and carry parent signals through. Use helper functions for interactive subtrees that need reactive props from the parent island; use `Children` for static content that an island consumes.

```rust
// Reusable interactive helper. NOT #[island], NOT #[component]. A plain function.
// It is a code-organization boundary only — its reactivity flows through the calling island.
pub fn business_unit_form_sheet(
    open:        RwSignal<bool>,
    edit_target: RwSignal<Option<BusinessUnitDto>>,
    save:        ServerAction<UpsertBusinessUnit>,
) -> impl IntoView {
    view! {
        <Sheet open=open on_close=move || open.set(false)>
            <ActionForm action=save>
                <input
                    name="name"
                    prop:value=move || edit_target.get().map(|b| b.name).unwrap_or_default()
                    on:input=move |ev| {
                        let v = event_target_value(&ev);
                        edit_target.update(|t| {
                            if let Some(bu) = t.as_mut() { bu.name = v; }
                        });
                    }
                />
                <button type="button" on:click=move |_| open.set(false)>"Cancel"</button>
                <button type="submit" disabled=move || save.pending().get()>"Save"</button>
            </ActionForm>
        </Sheet>
    }
}

// One ownership tree, one island, helper called inline.
#[island]
pub fn BusinessUnitsTableIsland(rows: Vec<BusinessUnitDto>) -> impl IntoView {
    let open        = RwSignal::new(false);
    let edit_target = RwSignal::new(None::<BusinessUnitDto>);
    let save        = ServerAction::<UpsertBusinessUnit>::new();

    view! {
        <button on:click=move |_| { edit_target.set(None); open.set(true); }>
            "New Business Unit"
        </button>

        // For each row, a row-edit button that loads into the same form sheet.
        <For each=move || rows.clone() key=|r| r.id let:row>
            <tr>
                <td>{row.name.clone()}</td>
                <td>
                    <button on:click=move |_| { edit_target.set(Some(row.clone())); open.set(true); }>
                        "Edit"
                    </button>
                </td>
            </tr>
        </For>

        // Plain-function helper — composes into THIS island's view tree.
        // The Sheet, form, inputs, and buttons all hydrate as part of BusinessUnitsTableIsland.
        {business_unit_form_sheet(open, edit_target, save)}
    }
}
```

Notice the call site: `{business_unit_form_sheet(open, edit_target, save)}` — a Rust **function call** inside `view!`, not an element invocation like `<BusinessUnitFormSheet … />`. The helper is splatted into the parent island's view tree. The `RwSignal`s are the parent island's own signals; the helper just reads/writes them.

### Why this works (and `#[island]` for the helper would not)

- A plain function returning `impl IntoView` is **not a hydration boundary**. Its view nodes belong to the caller's island. Signals flow naturally.
- A `#[island]` is an **independent hydration root**. Each instance gets its own reactive runtime. A `RwSignal` passed as a prop is *re-instantiated* per-island on hydration — it is not the same signal as the parent's.
- A `#[component]` is **server-only**. If you reach for `#[component]` to "make this reusable", you ship the markup as static HTML and every handler inside it dies.

### Naming

- A reusable helper that depends on parent-island state and does NOT own its own hydration → name it `business_unit_form_sheet`, `agent_filter_panel`, `row_action_menu`. **Do NOT** suffix `_island` and **do NOT** annotate `#[island]`.
- An independent hydration root (lives at a stable place in the page and owns its own state from scratch) → name it `BusinessUnitsTableIsland`, `BulkActionBarIsland`. Use the `Island` suffix and `#[island]` attribute.

The naming convention is a load-bearing signal: if a file is named `*_island.rs` or a function `Foo*Island`, readers will assume an independent hydration root and may try to pass signals into it — which fails silently. Reserve the `Island` suffix for actual islands.

## RwSignal Cannot Cross Independent Island Boundaries

`RwSignal<T>` is not `Serialize`/`Deserialize`. It cannot be transmitted across the SSR→client hydration handoff for an island prop. Even if you somehow forced it through (e.g. via context), the two islands hydrate from independent reactive runtimes — the signals would be different instances pointing at different storage.

**This is not a limitation to work around — it is the system telling you the ownership boundary is in the wrong place.**

If a child function/component needs:

- `RwSignal<T>` / `WriteSignal<T>` / `ReadSignal<T>` from a parent
- `Memo<T>` from a parent
- A `ServerAction<…>` from a parent
- A `Resource<…>` from a parent
- Modal/sheet/dialog open-state from a parent
- Form field state from a parent

then that child is **part of the parent's ownership tree** and must be:

- a plain function (`pub fn helper(open: RwSignal<bool>) -> impl IntoView`), OR
- a `#[component]` *only* if the child receives no reactive props and renders only static HTML (no `on:`, no signal reads — just inert markup composing into the parent island).

It must **not** be a `#[island]`. The moment you make the child `#[island]`, the parent's signal becomes inaccessible from the child's reactive runtime and the UI breaks.

### Coordination across independent islands

If two distinct ownership trees genuinely need to coordinate (different parts of the page that hydrate independently), the coordination channel is:

- **URL state** via `use_query_map()` (the data-table pattern; survives reload, deep-linkable).
- **Server fns + `action.version()`** (one island dispatches, another reads `version()` as a `Resource` source).
- **Server-sent events / WebSocket** for real-time fan-out.

Raw `RwSignal` props across `#[island]` boundaries are not a valid coordination channel.

## Interactive Ownership Tree — first-class architectural rule

Before writing the first line of a feature, sketch the ownership tree on paper. One `#[island]` per **independent** ownership tree, no more, no fewer. Sub-divide that island internally with plain functions or static `#[component]` children, never with sibling `#[island]`s that need to share state.

Common ownership trees in this codebase:

| Tree | Belongs to one island |
|---|---|
| Filter panel (search + selects + reset) | `FilterPanelIsland` |
| Create/edit sheet (trigger + form + buttons) | `<Entity>SheetIsland` |
| Row action menu (button + menu + per-item handler) | `RowActionsIsland` (or per-row island) |
| Bulk action bar (selection state + actions) | `BulkActionBarIsland` |
| Pagination control (page state + buttons + size selector) | `PaginationIsland` (often combined with filters) |
| Live presence/status pill that subscribes to SSE | `<Feature>StatusIsland` |
| Tabs that swap server-rendered panes | `TabsIsland` (panes can be children passed in) |

**One subtle case: per-row islands.** If each row has a small toggle or menu and rows are server-rendered from a paginated table, the row interactivity goes inside a row-level island (`<RowActionsIsland row=...>`) and the surrounding `<tbody>` / `<tr>` chrome stays in `#[component]`. The table is not one big island.

## Children passed into islands are server-rendered

Children passed into an `#[island]` via `Children` / `ChildrenFn` are serialized as static HTML on the server and inserted into the island shell. **They do not hydrate.** Use this deliberately:

```rust
#[island]
pub fn Tabs(labels: Vec<String>, children: Children) -> impl IntoView {
    let active = RwSignal::new(0usize);
    view! {
        <nav>
            {labels.into_iter().enumerate().map(|(i, label)| view! {
                <button class:active=move || active.get() == i
                        on:click=move |_| active.set(i)>{label}</button>
            }).collect_view()}
        </nav>
        <div class="tab-panels">{children()}</div>
    }
}

// Usage from a #[component]:
view! {
    <Tabs labels=vec!["Overview".into(), "Members".into()]>
        <OverviewPane data=overview />     // #[component], static, fine
        <MembersPane  data=members />      // #[component], static, fine
    </Tabs>
}
```

If a child needs to be interactive, it must itself be an `#[island]`:

```rust
view! {
    <Tabs labels=vec!["Settings".into()]>
        <SettingsFormIsland initial=settings />   // ← #[island], hydrates independently
    </Tabs>
}
```

## SSR-First Guidance — what goes where

Use `#[component]` (server-only, zero WASM) for:

- Page handlers and page shells
- Layouts (`AppLayout`, `AdminLayout`, sidebars, headers, breadcrumbs)
- Cards, wrappers, containers, panels
- Typography: headings, labels, descriptions, helper text
- Static tables (server-side paginated; rows are rendered HTML)
- Static detail panes / read-only views
- Empty states, loading skeletons rendered server-side
- Read-only badges, status pills whose value is fixed for the request
- Navigation menus (anchor tags, no client routing)

Use `#[island]` for:

- Forms (every form is at least one island)
- Modals, sheets, drawers, dialogs, popovers
- Dropdowns and select menus
- Filter panels and search inputs
- Tabs, accordions, collapsibles (when they swap client-side)
- Toggle switches, checkboxes that drive client state
- Pagination controls
- Row actions and bulk action bars
- Live-updating status indicators (SSE-subscribed)
- Toolbars containing any of the above
- Any tree containing a signal or `on:` handler

## Cargo / Features

**Feature flag name in Leptos 0.8 is `islands`** (renamed from `experimental-islands` in 0.7). Apply it via `leptos`'s feature alone — `leptos_router` does not need a separate islands feature in 0.8; it picks up islands mode through the `leptos` dependency.

```toml
[dependencies]
leptos        = { version = "0.8", default-features = false }
leptos_router = { version = "0.8" }

[features]
ssr     = ["leptos/ssr",     "leptos/islands"]
hydrate = ["leptos/hydrate", "leptos/islands"]
```

`leptos/islands` MUST be in **both** `ssr` and `hydrate` feature sets — otherwise the server and client disagree on what is an island and hydration mismatches silently.

If you are on Leptos 0.7, the flag is `experimental-islands` instead. Pick the name that matches the leptos version in `Cargo.toml`.

## Islands-Router (0.8+)

Leptos 0.8 ships an islands-aware router. With it, in-app navigation does not full-reload the page; instead it re-fetches the new server-rendered HTML and re-hydrates the new island instances. Without it, every link is a full page load. Enabling `leptos/islands` is sufficient on 0.8.

The router component name and surface area are still stabilizing — consult the current 0.8 examples in `leptos-rs/leptos/examples/` for the exact import. Pattern is: standard `<Router>` / `<Routes>` JSX with the feature flag flipping internals to islands-mode navigation.

## WASM Bundle Discipline

Each `#[island]` adds to the hydrated surface. Goals:

- Keep islands **small and leaf-shaped**. An island that itself contains other islands is fine, but an island that renders a giant component tree pulls all that into WASM.
- Push static content into `Children` passed into islands rather than rendering it inside the island body.
- Prefer **per-feature islands** (`BusinessUnitSheetIsland`, `AgentFilterPanelIsland`) over **per-page mega-islands** (`BusinessUnitPageIsland` would be an anti-pattern — see below).
- Measure with `ls -lh target/site/pkg/*.wasm` after `cargo leptos build --release`. Islands work; the question is which ones, not whether.

## Anti-Patterns — block on sight

### Anti-pattern 1 — entire page as one island

```rust
// BAD
#[island]
pub fn BusinessUnitsPageIsland() -> impl IntoView { /* table + filters + sheet + ... */ }
```

This recreates the React full-hydration model: every byte of the page is in WASM, SSR is wasted, and you lose every benefit of islands. **Pages are `#[component]`.** Interactive subtrees are `#[island]`.

### Anti-pattern 2 — split modal / sheet ownership

```rust
// BAD
#[island]    fn OpenButton() { ... }       // hydrates
#[component] fn ModalContent() { ... }     // does NOT hydrate; inputs and buttons are dead
```

See the Modal/Sheet section. Trigger + content + form + buttons live in one island.

### Anti-pattern 3 — interactive component declared as `#[component]`

```rust
// BAD — looks fine, does nothing
#[component]
pub fn SearchInput(value: RwSignal<String>) -> impl IntoView {
    view! { <input on:input=move |ev| value.set(event_target_value(&ev)) /> }
}
```

`on:input` does not attach. `value` updates from the parent will render server-side but client-side typing does nothing. If the component has any `on:`, any signal mutation, or owns any reactive state — it must be `#[island]`.

### Anti-pattern 4 — portal/modal escaping island ownership

```rust
// BAD — portal rendered from a #[component] context
#[component]
pub fn PageShell(children: Children) -> impl IntoView {
    view! {
        <main>{children()}</main>
        <Portal>{/* modal root */}</Portal>   // ← static, no hydration
    }
}
```

If the portal needs interactive content, mount it from inside the island that owns the modal state, not from the page shell.

### Anti-pattern 5 — sibling islands that share signals through props

```rust
// BAD
#[island] fn FilterIsland(query: RwSignal<String>) { ... }
#[island] fn ResultsIsland(query: RwSignal<String>) { ... }
// Each island hydrates separately. Sharing a RwSignal across island boundaries
// is not the same as sharing it within a single ownership tree — the two
// hydrate from independent island instances and the signal is not the bridge
// you think it is.
```

If two pieces of UI must react to the same source-of-truth signal, they belong in the same island. Use URL query state (the data-table pattern in CLAUDE.md) for cross-island coordination, not raw shared signals.

### Anti-pattern 6 — marking purely static UI as `#[island]`

```rust
// BAD — wastes WASM bytes on something that has no interactivity
#[island]
pub fn StaticInfoCard(title: String, body: String) -> impl IntoView { /* ... */ }
```

Use `#[component]`. The cost of an island is paid even if the island never calls a signal.

### Anti-pattern 7 — fragmenting one ownership tree into multiple `#[island]`s

```rust
// BAD — looks "clean and modular" but breaks reactivity
#[island] fn ParentIsland() -> impl IntoView {
    let open = RwSignal::new(false);
    view! { <ChildIsland open=open /> }
}

#[island] fn ChildIsland(open: RwSignal<bool>) -> impl IntoView {
    view! { <button on:click=move |_| open.set(true)>"Open"</button> }
}
```

Symptoms: the button renders, `open.set(true)` runs in `ChildIsland`'s reactive runtime, but `ParentIsland` never observes the change because `open` in `ChildIsland` is a different instance after hydration. Modals never open. Sheets never close. Forms never submit.

This is the **single most common over-componentization mistake** when moving from React. The instinct "child is interactive → child needs `#[island]`" is wrong under Leptos islands.

**Fix:** extract the child as a plain function, not an island.

```rust
// CORRECT
#[island]
fn ParentIsland() -> impl IntoView {
    let open = RwSignal::new(false);
    view! { {child_helper(open)} }
}

// Plain function. NOT #[island]. NOT #[component]. Composes into the calling island.
fn child_helper(open: RwSignal<bool>) -> impl IntoView {
    view! { <button on:click=move |_| open.set(true)>"Open"</button> }
}
```

The diagnostic question is always: **"does this child need a signal/handler/state from its parent?"** If yes, it belongs in the parent's island — usually as a plain function. Promoting it to `#[island]` is what *causes* the dead-button bugs the team has been seeing.

### Anti-pattern 8 — `Island`-suffixed helper that is not actually a hydration root

```rust
// BAD — name lies about the architecture
pub fn BusinessUnitFormSheetIsland(...) -> impl IntoView { ... }  // plain fn, no attribute
```

Readers (and tools) will read the `Island` suffix as "this is an independent hydration root" and try to use it as one (passing it signals via props, expecting it to hydrate alone). Reserve the `Island` suffix and the `Island` PascalCase for functions actually annotated `#[island]` that own their own ownership tree from scratch. Reusable helpers get plain `snake_case` names: `business_unit_form_sheet`, `row_actions_menu`, `filter_select`.

## Debugging Hydration Failures

When something is "dead" — buttons that render but don't click, inputs that type but don't update, modals that open but whose internals don't work, interactions that only start working after a random unrelated click — the cause is almost always an ownership-boundary mistake.

### Diagnostic checklist

1. **Is the dead element inside a `#[component]` that contains an `on:`, a signal, or a reactive read?** → That component must be `#[island]`. This is ~70% of cases.
2. **Is the dead element inside `Children` passed to an `#[island]`?** → Children are server-rendered and static. Either pull the interactivity into the parent island, or make the child its own `#[island]`.
3. **Is the dead element inside a portal mounted from a `#[component]`?** → Move the portal inside an island.
4. **Are two interactive nodes in sibling islands trying to share a signal?** → They are not actually sharing — move them into the same island, or coordinate via URL state / server fns.
5. **Does the browser console show a hydration mismatch warning?** → SSR and client rendered different HTML. Common cause: `leptos/islands` (or `experimental-islands` on 0.7) missing from one of the `ssr` / `hydrate` feature sets, or random/time-based content rendered without `Suspense`.
6. **Does interaction "wake up" after clicking somewhere else first?** → Classic sign that a different island's hydration was deferred and your click triggered a routing/hydration event that re-evaluated the page. The actually-broken element is still in a `#[component]` ownership context.

### Temporary instrumentation

Drop these into the suspect island to confirm hydration is happening (or not):

```rust
#[island]
pub fn SuspectIsland(/* ... */) -> impl IntoView {
    Effect::new(move |_| {
        leptos::logging::log!("SuspectIsland hydrated");
    });

    let count = RwSignal::new(0);
    Effect::new(move |_| {
        leptos::logging::log!("count is now {}", count.get());
    });

    view! {
        <button on:click=move |_| {
            leptos::logging::log!("clicked");
            count.update(|n| *n += 1);
        }>
            "Click ("{count}")"
        </button>
    }
}
```

If "hydrated" never logs → the island never hydrated; check that it's actually `#[island]` and that `leptos/islands` (0.8) / `experimental-islands` (0.7) is on both feature sets.

If "hydrated" logs but "clicked" never does → the button is rendering server-side HTML inside a non-hydrating parent. Walk up the tree until you find the offending `#[component]`-with-interactivity boundary.

If "clicked" logs but `count.get()` never changes downstream → the consumer of `count` is across an island boundary; pull it inside.

Remove the logging before committing.

## Review Checklist

Before opening a PR that adds or modifies a page:

- [ ] The page handler / page function is `#[component]` (not `#[island]`).
- [ ] Each interactive ownership tree is exactly one `#[island]`.
- [ ] Triggers, modal/sheet content, forms, inputs, and action buttons that belong to one flow live in the same island.
- [ ] No `#[component]` in the diff contains `on:click`, `on:input`, `RwSignal::new`, `Effect::new`, or `ServerAction::<…>::new()`.
- [ ] No `#[island]` exists purely to render static content.
- [ ] Portals are mounted from inside islands, not from page shells.
- [ ] Children of islands are static or themselves islands — never silently expected to hydrate.
- [ ] `leptos/islands` (or `experimental-islands` on 0.7) is in both `ssr` and `hydrate` feature sets.
- [ ] No two sibling `#[island]`s share a `RwSignal`/`Memo`/`ServerAction`/`Resource` through props. If they need to, they are one ownership tree and must be ONE island.
- [ ] Reusable interactive helpers extracted for readability are plain `fn` returning `impl IntoView`, called as `{helper(signals…)}` from inside the parent island. They are NOT `#[island]` and (if they contain interactivity) NOT `#[component]`.
- [ ] Functions named `*Island` / files named `*_island.rs` are actually `#[island]` and own their state from scratch — they do not take parent-island signals as props.

## Verification Hooks

```bash
# leptos/islands (or experimental-islands on 0.7) must be in both ssr and hydrate feature sets
grep -nE 'leptos/islands|experimental-islands' Cargo.toml src/crates/web-app/Cargo.toml

# Find #[component]s that smell interactive — top source of dead-button bugs
grep -rnE '#\[component\]' src/crates/web-app/src \
  | cut -d: -f1 \
  | xargs -I{} sh -c 'grep -lE "on:click|on:input|RwSignal::new|Effect::new|ServerAction::" "{}" && echo "  ↑ possibly should be #[island]: {}"'

# Island vs component ratio (sanity, not a hard target)
echo "Islands:";    grep -rnE '#\[island\]'    src/crates/web-app/src | wc -l
echo "Components:"; grep -rnE '#\[component\]' src/crates/web-app/src | wc -l

# WASM size after release build
ls -lh target/site/pkg/*.wasm 2>/dev/null || echo "build first: cargo leptos build --release"
```

## References

- https://book.leptos.dev/islands/ — official Islands chapter
- https://github.com/leptos-rs/leptos/tree/main/examples/islands — minimal working example
- https://github.com/leptos-rs/leptos/tree/main/examples/islands_router — 0.8 islands-router example
- https://docs.rs/leptos/latest/leptos/attr.island.html — `#[island]` attribute reference
- https://leptos.dev/blog/islands-in-leptos-08/ — 0.8 islands-router announcement
