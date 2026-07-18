---
name: data-table
description: Canonical Leptos data-table page — layout/design, four-owner state model, hydration boundary, island contract (TableData + Selection + refetch_action + sort/filter pushState), mutation reconciliation (MutationBinder + ReconcileStrategy + SelectionPolicy), label bundle, server-fn + DTO shape, and the inviolable pushState+refetch pairing. Trigger keywords: data table, list page, table page, controller bar, filter panel, pagination, ListQueryParams, TableData, Selection, TableQueryState, facet counts, sortable header, refetch_action, SheetController, MutationBinder, ReconcileStrategy, ReplaceById, ReplaceOrAppend, BulkPatch, RemoveById, ClearAll, RemoveMissing, FacetCounts, ToastQueue, LabelBundle, status_switch, bulk action, sheet, drawer, toast host, empty state, BadgeVariant. Auto-triggers on any new or modified list page, any table island, any mutation response shape, any label bundle, or any review of visual/behavioral consistency across list pages.
---

# Canonical Data-Table Page

Single source of truth for every Leptos data-table page in this project. Project-agnostic. Sections cover layout, behavior, mutations, labels, server fns, and verification hooks. Long-form companions live under [`references/`](references/).

> **Architecture in one paragraph.** SSR page shell parses the URL query map into typed `ListQueryParams`, drives a `Resource` against a `#[server]` list fn, and renders inside a `<Transition>` a hydrated `<XTableIsland>` that owns all client interactivity. The island carries `TableData<XRow>`, `Selection<Id>`, reactive count signals seeded from SSR props, four `MutationBinder` installs (bulk-set-active, single-toggle, save, delete), a `SheetController`, and a client-side `refetch_action` driven by sort/filter clicks. Mutations dispatch through Leptos `Action`s, return canonical DTOs, and the binders reconcile the row store + selection + toast queue from those DTOs alone — never from a router refresh, never from optimistic UI.

## When to use

Auto-triggers when:

- A new page renders a list of rows with pagination, filtering, or sorting.
- A new island whose name contains `table_island` (or equivalent project convention) is added or modified.
- Code touches `TableQueryState`, `TableData`, `Selection`, `MutationBinder`, `SheetController`, `FacetCounts`, `sortable_header_link`, `filter_toggle_button`, `bulk_action_bar`, `refetch_action`, or any `*LabelBundle`.
- A server fn matching `get_<entity>_list`, `update_<entity>`, `delete_<entity>`, `set_<entity>_active` is added or called.
- A review/audit of a list page is requested.

Do NOT use for tiny static lists (no pagination, no filter, no mutation) — use a plain `<For>` component instead.

---

## 1. The four owners (do not blur)

| Owner | Owns | Lifetime | Where |
|---|---|---|---|
| **URL** | filters, search, sort, pagination, facet selections | survives navigation/refresh/deep-link | `window.location.search` ↔ `use_query_map()` |
| **Server** | entity rows + facet counts | authoritative across requests | DB via service layer |
| **`TableData<XRow>`** | rendered rows for current page | island lifetime; preserved across filter/sort | island context |
| **`Selection<Id>`** | user-selected ids (intent) | island lifetime; survives filter/sort/pagination | island context |

No piece of state has two owners. Counts live ONLY on the server (and on the snapshot in the URL response); selection lives ONLY in `Selection<Id>`; URL params live ONLY in the URL. When state seems to want two owners, that is the bug — find the single owner and read from it.

## 2. Reactive-ownership rule

> **The island owns all client-side reactive state. The SSR page owns request-scoped Resources only.**

- `RwSignal`, `Action`, `Effect`, `Memo`, `Callback` — island-owned.
- `Resource` — page-owned. The island does NOT subscribe to a Resource via context.
- The island MAY create a local `Action` that wraps the same server fn the page Resource called (this is `refetch_action`) but does NOT consume the page Resource.

## 3. Concurrency contract

- **Last successful mutation response wins.** No optimistic merge.
- **Mutations are independent across rows.** Per-row `pending_toggle_id`.
- **Refetch supersedes in-flight mutations for the row store only.** Counts are server-authoritative on every response.
- **Bulk actions are atomic on the server.** Response carries `updated` + `skipped_ids`.

## 4. URL contract

Reserved params: `page` (i64, default 1), `per_page` (i64, default 25), `search` (String), `sort_by` (String), `sort_dir` (`asc`/`desc`; malformed → None). Per-entity: `is_active`/`is_enabled` (bool) plus entity-specific filters.

**Canonical ordering** when building base URLs via `TableQueryState::build_base_url()`: `per_page`, `search`, `sort_by`, `sort_dir`, then entity filters in declared order. `page` is excluded so the pagination component appends `&page=N` cleanly.

**Update semantics:**

- Sort / filter / pagination clicks update the URL via `History.pushState` AND dispatch the island's local `refetch_action`. They do NOT trigger a router navigation or document reload.
- Search is debounced inside `SearchInput` and writes on commit.
- Mutations DO NOT touch the URL.

> **The pushState + refetch pairing is mandatory.** `History.pushState` alone updates the URL but does NOT invalidate the page's SSR-owned `Resource` in islands mode. Removing the refetch callback to "simplify" the click handler will silently leave the table body stale until a real navigation.

## 5. Hydration boundary

**SSR-only (`#[component]`):** page component, content sub-component, skeleton fallback, page-level error boundary, pagination.

**Hydrates (`#[island]`):** table island, form sheet, embedded helpers (`SearchInput`, status facet, entity-specific filters), `ToastHost` at chrome layer (mounted ONCE).

**Rules:**

- Page is `#[component]`, NOT an island. It serializes initial data into island props.
- Table island receives `initial: Vec<XDto>`, facet `*_count: i64`, `query: TableQueryState`, active per-entity filter values, and the `XLabelBundle` — every prop derives `Serialize + Deserialize`.
- NO `RwSignal`/`Resource`/`Action`/`Callback` crosses the hydration boundary as a prop.

---

## 6. Page layout & design

### 6.1 Chrome regions (top → bottom)

```
┌─────────────────────────────────────────────────────────────────────┐
│ [Page title]                                                        │  (A) Header
│ [Optional subtitle / breadcrumb]                                    │
├─────────────────────────────────────────────────────────────────────┤
│ [Search] │ [Refresh] [Columns] [Filters] [Spacer] [Primary action] │  (B) Controller bar
├─────────────────────────────────────────────────────────────────────┤
│  [Filter panel — collapsible; hidden by default]                    │  (C) Filter panel
│    [Scope ▾] [Status ▾] [Bool ⏵] [Owner ▾] [Date range]  [Reset]    │
├─────────────────────────────────────────────────────────────────────┤
│ [Facet chips: Active(123) Inactive(45)]                             │  (D) Facet strip
├─────────────────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ ☐ │ Col A ⇅ │ Col B ⇅ │ Col C │ … │ Status │ Actions           │ │  (E) Table head
│ ├─────────────────────────────────────────────────────────────────┤ │
│ │ ☐ │ row data ……………………………………………………………… │ [≡] [⋮]            │ │  (F) Table body
│ └─────────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────────┐ │
│ │ N selected  [Enable] [Disable] [Delete]              [Clear]   │ │  (G) Bulk bar
│ └─────────────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│ [Page 1 of 8]    [‹ Prev] [1][2][3]…[8] [Next ›]    [25 / page ▾]   │  (H) Footer pagination
└─────────────────────────────────────────────────────────────────────┘

[Sheet / drawer — slides from right; covers the page when open]        (I) Sheet
[Toast host — fixed top-right corner of the chrome layer]              (J) Toast
```

Regions A, B, C, D, H stay SSR. Region E `<thead>` stays SSR; sort headers are `<a href>` anchors. Region F `<tbody>` stays SSR for initial paint; the island re-renders rows on hydration. Region G is rendered inside the table island. Regions I (sheet) and J (toast host at chrome) live in island and chrome contexts respectively.

### 6.2 Controller bar (B) — element order

Left → right, fixed: `Search` → `Refresh` → `Columns` → `Filters` → *(flex spacer)* → `Primary action` (rightmost).

Variants 2–4 are icon-only on narrow viewports (≤ 640 px), icon+label otherwise. The primary action stays full-width with label. Never insert a secondary primary action in this row — secondary actions live in the row kebab.

### 6.3 Filter panel (C) — order

1. Scope (categorical narrowers: Campaign, Batch, Integration, Vendor, Role, Break Reason, …)
2. Status / State (active/inactive, online/offline, …)
3. Boolean toggles (unassigned-only, connected/not-connected, …)
4. Owner / Assignment
5. Date range (always last, via `<DateRangePicker/>`)
6. Reset (centralized `onReset`, right-aligned)

Cascading scope filters stay adjacent. Date picker never precedes a categorical filter. No inline ghost-button reset on individual filters.

### 6.4 Facet strip (D)

Status facets render as chips: `Active (123)`, `Inactive (45)`. Counts come from `FacetCounts` context (server-authoritative). Clicking a chip writes `is_active=true`/`is_active=false` to the URL and dispatches `refetch_action` via `FacetRefetch::dispatch`. Selected chip uses the colored variant matching its semantics; unselected use neutral muted.

### 6.5 Table grid (E + F)

| Column | Width hint | Notes |
|---|---|---|
| Selection checkbox | 40 px fixed | Centered. |
| Primary identifier (name/label) | `min-content` → grow | Often the row link target; opens edit sheet. |
| Secondary columns | content-based | Truncate with ellipsis past `max-w-[...]`. |
| Status | 120 px fixed | `status_switch` (toggle) or `Badge` (read-only). |
| Updated/Created at | 160 px fixed | Right-aligned, `<RelativeTime>`. |
| Actions | 80 px fixed | Right-aligned. Inline icons + kebab. |

Rules:

- `<tbody>` is required (Leptos hydration mismatch otherwise).
- `<For each=... key=row.id />` — stable key on the row id.
- Empty cells render `—`, never an empty string.
- Sortable headers use the anchor-based `sortable_header_link` (URL-bound) — never `on:click` mutating a local sort signal.
- Hidden columns gate BOTH `<th>` AND `<td>` body together — a hidden header with a visible body misaligns the grid.

### 6.6 Skeleton, overlay, empty, error

| State | Shown when | What renders |
|---|---|---|
| **Skeleton** | initial SSR load only (`<Transition>` fallback) | Shimmer rectangles in same grid. |
| **Loading overlay** | `any_pending == true` for whole-set mutations | Translucent layer over `<tbody>` only. |
| **Per-row pending** | single toggle / delete in flight | That row's `status_switch` disabled via `pending_toggle_id`. |
| **Empty** | `items.is_empty()` | Icon + headline + sub-line + optional CTA. If filters active, headline is "No results match your filters" + Reset. |
| **Error** | page Resource errors | `<ErrorBoundary>` fallback (`FriendlyError`); controller bar stays interactive. |

### 6.7 Bulk action bar (G)

- Position: inside the table island, between `<tbody>` and the footer.
- Visibility: `selection.selected_count() > 0`.
- Width: matches the table grid; optional sticky-bottom on long pages.
- Left: `N selected` count. Center/right: `BulkAction` buttons in declared order, each colored by `BulkActionVariant` (§6.10). Far right: `Clear selection` ghost button.
- The bulk bar is the only place where destructive bulk operations are exposed. Single-row destructive ops live in the row kebab.

### 6.8 Sheet / drawer (I)

- Slides from the right; ~480 px wide desktop, full-width mobile (< 640 px).
- Owned by `SheetController` in island context.
- Modes: `Closed`, `Create`, `Edit(id)`.
- Body is its own `#[island]` (`XFormSheet`).
- Z-index above the loading overlay.
- Backdrop click confirms via `client_confirm_dialog` only if `is_dirty`; otherwise closes silently.
- Sheet footer: leftmost destructive `Delete` (edit mode only) → `Cancel` → rightmost primary `Save`.

### 6.9 Toast host (J)

- Mounted ONCE at the chrome layer (NOT inside any table island — filter changes would tear it down).
- Fixed top-right (24 px from top + right).
- Stack newest on top. Auto-dismiss: Success 4 s, Warning 6 s, Error 8 s. Hover pauses dismissal.
- Toasts emitted by `MutationBinder` go through `ToastQueue` context.

### 6.10 Reserved status palette

| Semantic | Color | Used for |
|---|---|---|
| `Success` / `Active` | green | `BadgeVariant::Active`, success toasts, online indicators, healthy state |
| `Warning` / `Pending` | yellow | `BadgeVariant::Pending`, partial-success toasts, in-progress |
| `Error` / `Inactive` / `Destructive` | red | `BadgeVariant::Inactive`, error toasts, destructive bulk actions, offline |
| Neutral / Muted | gray | non-semantic chips, secondary text, disabled controls |

`BulkActionVariant::Destructive` MUST render in red. Never use red for a non-destructive action. Color is never the only indicator of status — pair every colored dot/badge with text.

### 6.11 Spacing & sizing

- Page outer padding: `px-6 py-4` desktop, `px-3 py-3` mobile.
- Vertical gap between regions: `gap-4` (16 px). Filter panel collapse animates 150 ms.
- Row height: 56 px (48 px compact). Header / controller / bulk bar: 56 px.

### 6.12 Responsive

| Breakpoint | Behavior |
|---|---|
| ≥ 1024 px | Full chrome. |
| 640–1023 px | Controller buttons icon-only. Date picker stacks below scope. Secondary columns may auto-hide. |
| < 640 px | Filter panel becomes a full-width sheet. Pagination collapses to `‹ N / M ›`. Rows stack into `MobileRowCard` if the primitive exists. |

### 6.13 Accessibility minimums

- Sortable headers expose `aria-sort` matching URL state.
- Selection checkbox column has accessible name ("Select row").
- Filter panel toggle button has `aria-expanded`.
- Sheet uses `role="dialog"` + focus trap + restore-focus-on-close.
- Toasts use `role="status"` (success/warning) or `role="alert"` (error).

Deep dive: [`references/wireframe.md`](references/wireframe.md).

---

## 7. Page-shell shape

### 7.1 Query → params memo → Resource

```rust
let query_map = use_query_map();
let query: Signal<TableQueryState> = TableQueryState::from_query_map(&query_map, "/<area>/<entity>");
let params: Memo<ListQueryParams> = Memo::new(move |_| {
    ListQueryParams::from_query_map(&query_map.get())
});
let resource = Resource::new(
    move || params.get(),
    |p| async move { get_x_list(p).await },
);
```

**Critical:** subscribe via `.get()`, never `.read()`. `.read()` returns an untracked guard so filter changes never invalidate the Resource — facet counters stay stale forever.

### 7.2 `<Transition>` not `<Suspense>`

Paginated tables use `<Transition>` with `XTableSkeleton` as fallback. `<Suspense>` would unmount the table on every interaction.

### 7.3 `<ErrorBoundary>`

Wrap the `<Transition>` in `<ErrorBoundary>` whose fallback is `FriendlyError`. Title/description come from the language layer.

### 7.4 Pagination component

Mounted OUTSIDE the table island (stays SSR). `base_url` = `query.build_base_url()` + each active per-entity filter appended in declared order. The pagination component appends `&page=N`.

---

## 8. Table island contract

### 8.1 Context provision (order matters)

Inside the island body, BEFORE the `view!`, install in this order:

```rust
let table_data = TableData::<XRow>::new(initial.into_iter().map(XRow).collect());
provide_context(table_data);

let selection = Selection::<i32>::new();
provide_context(selection);

let active_count_sig    = RwSignal::new(active_count);
let inactive_count_sig  = RwSignal::new(inactive_count);
provide_context(XCounts { active: active_count_sig, inactive: inactive_count_sig });
provide_context(FacetCounts {
    active:   Signal::derive(move || active_count_sig.get()),
    inactive: Signal::derive(move || inactive_count_sig.get()),
});

let refetch_action = Action::new(|_| async move { /* see §8.3 */ });
let refetch_cb     = Callback::new(move |_| { refetch_action.dispatch(()); });
provide_context(FacetRefetch { dispatch: refetch_cb });

let sheet          = SheetController::new();
let saved_response = RwSignal::<Option<XMutationResponse>>::new(None);
provide_context(XSheetController { sheet, saved_response });
```

Reordering breaks consumers that read context during their own setup.

### 8.2 The `XRow` newtype

```rust
#[derive(Clone, Serialize, Deserialize)]
pub struct XRow(pub XDto);

impl Row for XRow {
    type Id = i32;
    fn id(&self) -> i32 { self.0.id }
}
```

Orphan rule prevents `impl Row for XDto`. Use the newtype.

### 8.3 Refetch action

```rust
let refetch_action: Action<(), Result<XListResponse, ServerFnError>> = Action::new(|_: &()| async move {
    #[cfg(target_arch = "wasm32")]
    {
        let search = web_sys::window().unwrap().location().search().unwrap_or_default();
        let params = ListQueryParams::from_search_string(&search);
        get_x_list(params).await
    }
    #[cfg(not(target_arch = "wasm32"))]
    { Err(ServerFnError::ServerError("refetch is wasm-only".into())) }
});

Effect::new(move |_| {
    if let Some(Ok(resp)) = refetch_action.value().get() {
        table_data.set_all(resp.items.into_iter().map(XRow).collect());
        active_count_sig.set(resp.active_count);
        inactive_count_sig.set(resp.inactive_count);
    }
});
```

The Effect MUST NOT touch `selection` — selection survives filter/sort by design.

### 8.4 Sort link + pushState pairing (MANDATORY)

```rust
sortable_header_link(
    /* href     = */ href_for_sort_col("name", &query),
    /* label    = */ labels.table.col_name.clone(),
    /* refetch  = */ refetch_cb,
)
```

Helper sequence: `event.preventDefault()` → `History.pushState(null, "", target)` → `refetch_cb`. Removing the refetch callback silently leaves the body stale until a real navigation.

### 8.5 Filter panel mechanics

`filters_visible: RwSignal<bool>` is island-local. All filter changes write to the URL via the facet/filter primitive and trigger the same `History.pushState + refetch_cb` flow as sort.

### 8.6 Column toggle (island-local, NOT URL-bound)

```rust
let hidden_columns: RwSignal<Vec<String>> = RwSignal::new(Vec::new());
// Gate cells on: !hidden_columns.with(|h| h.iter().any(|x| x == col_id))
```

Per-user preference, not part of the query.

### 8.7 Selection survives filter / sort / pagination (by design)

`Selection<Id>` represents **intent**, not **visibility**.

Selection IS modified, deliberately:

| Trigger | Policy |
|---|---|
| Successful bulk action | `SelectionPolicy::ClearAll` |
| Successful delete | `SelectionPolicy::RemoveMissing` |
| Filter / sort / pagination / search | never |

`visible_ids` is captured into a `StoredValue<Vec<Id>>` via `table_data.rows.with_untracked(...)`. Using `.with(...)` would re-render the selection cell on every row mutation.

### 8.8 Pending state

| Source | Affects |
|---|---|
| `refetch_action.pending()` | full overlay |
| Bulk install pending | full overlay |
| Sheet save install pending | full overlay |
| Delete install pending | full overlay |
| Single-row toggle | only that row's switch (per-row `pending_toggle_id`) |

```rust
let any_pending = Memo::new(move |_| {
    refetch_action.pending().get()
        || bulk_install.pending.get()
        || save_install.pending.get()
        || delete_install.pending.get()
});
table_loading_overlay(any_pending.into())
```

Deep dive: [`references/island.md`](references/island.md).

---

## 9. Mutation reconciliation

> **Cardinal rule.** Mutations reconcile from the **mutation response payload alone**. NEVER refetch on toggle/edit/delete. NEVER apply optimistic UI.

### 9.1 The four binder installs

| Install | Source | Strategy | Selection | Overlay |
|---|---|---|---|---|
| Bulk set-active | `Action<(Vec<Id>, bool), BulkSetActiveResponse>` | `BulkPatch` | `ClearAll` | yes |
| Single toggle | `Action<(Id, bool), MutationResponse>` | `ReplaceById` | `Preserve` | NO (per-row pending) |
| Sheet save | `SavedSignalSource<RwSignal<Option<Dto>>>` | `ReplaceOrAppend` | `Preserve` | yes |
| Delete | `Action<Id, Id>` (id-only after FacetCounts side-effect) | `RemoveById` | `RemoveMissing` | yes |

> **`ReplaceOrAppend` on sheet save is non-negotiable.** `ReplaceById` makes edits work but creates silently no-op.

### 9.2 `ReconcileStrategy` decision matrix

| Scenario | Strategy | Why |
|---|---|---|
| Toggle one row | `ReplaceById` | Server returns full DTO; patch in place. |
| Edit one row | `ReplaceOrAppend` | Same path as create. |
| Create one row | `ReplaceOrAppend` | Reconcile per server ordering. Never fake-prepend. |
| Bulk enable/disable | `BulkPatch` | Response carries `updated` + `skipped_ids`. |
| Delete | `RemoveById` | Drop the row. |
| Order can't be reconciled locally | `Refetch` | Last resort. |

### 9.3 `SelectionPolicy` decision matrix

| Scenario | Policy |
|---|---|
| Single-row toggle/edit/save | `Preserve` |
| Bulk action | `ClearAll` |
| Delete | `RemoveMissing` |

### 9.4 Toast semantics

| Level | Color | Used for |
|---|---|---|
| `Success` | green | Saved, N rows updated |
| `Warning` | yellow | Partial success (skipped system rows) |
| `Error` | red | Validation, conflict, transport |

Error-toast titles use stable string keys (label-independent so toasts render if the bundle is missing): `"Validation failed"`, `"Unauthorized"`, `"Not found"`, `"Conflict"`, `"Request failed"`, `"An error occurred"`.

`ToastHost` is mounted ONCE at chrome and consumed via `ToastQueue` context.

### 9.5 Toggle confirmation flow

1. User clicks the row's `status_switch`.
2. `toggle_switch_cell`'s `on_click`: early-return if `pending_toggle_id == Some(row_id)`; set `pending_row_id` (StoredValue), `pending_new_val`, `confirm_open=true`.
3. `client_confirm_dialog` opens — title/message from `pick_toggle_copy(&labels, new_val)`.
4. Confirm: `pending_toggle_id.set(Some(row_id))`; `action_update_active.dispatch((row_id, new_val))`; `confirm_open.set(false)`.
5. Action body calls `update_x(id, UpdateRequest { is_active: Some(new_val), .. })`; writes facet counts.
6. `MutationBinder` (`ReplaceById` + `Preserve`) reconciles.
7. Effect on `action_update_active.value()` clears `pending_toggle_id` on BOTH Ok and Err.

### 9.6 Sheet save flow

```rust
Effect::new(move |_| {
    if let Some(resp) = saved_response.get() {
        active_count_sig.set(resp.active_count);
        inactive_count_sig.set(resp.inactive_count);
        sheet_saved_dto.set(Some(resp.item));
    }
});
```

A `MutationBinder` watches `sheet_saved_dto` via `SavedSignalSource` with `ReplaceOrAppend` + `Preserve`. The sheet's own pending state stays internal.

### 9.7 Delete flow

```rust
let action_delete: Action<i32, Result<i32, ServerFnError>> = Action::new(move |id: &i32| {
    let id = *id;
    async move {
        let resp = delete_x(id).await?;
        active_count_sig.set(resp.active_count);
        inactive_count_sig.set(resp.inactive_count);
        Ok(resp.id)
    }
});
```

`RemoveById` + `RemoveMissing` drops the row and removes its id from `Selection`.

Deep dive: [`references/mutations.md`](references/mutations.md).

---

## 10. Label bundle

> **Cardinal rule.** Resolve every label on the SSR page from the language/translation context. Pack the resolved strings into ONE composite serializable struct. Pass it to the island as a single prop. NEVER call the translation context inside an `#[island]` body.

### 10.1 Composition

```rust
#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct XLabelBundle {
    pub table:       TableLabels,
    pub controller:  TableControllerLabels,
    pub crud:        CrudLabels,
    pub sheet:       SheetLabels,
    pub bulk:        BulkActionLabels,
    pub toggle:      ToggleConfirmLabels,
    pub domain:      XDomainLabels,
    pub form:        XFormLabels,
}
```

### 10.2 Constructors

```rust
impl XLabelBundle {
    pub fn from_translator(t: &impl Translator) -> Self { /* ... */ }
    #[cfg(feature = "ssr")]
    pub fn from_lang(ctx: &LanguageContext) -> Self { Self::from_translator(ctx) }
}
```

`from_lang` is SSR-gated. `from_translator` takes any `Translator` so unit tests construct bundles from a fake key→value map.

### 10.3 `Label` newtype

```rust
pub type Label = std::sync::Arc<str>;
```

Workspace `serde` `rc` feature MUST be enabled:

```toml
serde = { version = "1", features = ["derive", "rc"] }
```

### 10.4 Tests (per bundle)

- Non-empty after construction.
- `serde_json` round-trip equality.
- Per-sub-bundle field population.

Deep dive: [`references/labels.md`](references/labels.md).

---

## 11. Server fns + DTO shape

```rust
#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct ListQueryParams { /* page, per_page, search, sort_by, sort_dir, per-entity filters */ }

#[server] pub async fn get_x_list(p: ListQueryParams) -> Result<XListResponse, ServerFnError>;
#[server] pub async fn create_x(req: XCreateRequest) -> Result<XMutationResponse, ServerFnError>;
#[server] pub async fn update_x(id: i32, req: XUpdateRequest) -> Result<XMutationResponse, ServerFnError>;
#[server] pub async fn delete_x(id: i32) -> Result<XDeleteResponse, ServerFnError>;
#[server] pub async fn set_x_active(ids: Vec<i32>, active: bool) -> Result<XBulkSetActiveResponse, ServerFnError>;
```

Each fn:

1. Pulls `AppState` / `PgPool` from context.
2. Opens its own `Transaction`.
3. Calls ONE service method. Service owns validation, permissions, ordering. Repository owns SQL.
4. Commits.
5. Maps row(s) → DTO(s) and returns.
6. NEVER holds AppState across `.await` boundaries that span an I/O suspend.

REST handlers (when present) for external clients call the SAME service methods — no duplicated business logic.

### 11.1 DTO contract

```rust
#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct XDto {
    pub id: i32,
    pub is_active: bool,
    pub is_system: bool,     // optional — only if entity has system-row gating
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
    // entity fields …
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct XListResponse {
    pub items: Vec<XDto>,
    pub total: i64, pub page: i64, pub per_page: i64,
    pub active_count: i64, pub inactive_count: i64,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq)]
#[serde(rename_all = "camelCase")]
pub struct XMutationResponse { pub item: XDto, pub active_count: i64, pub inactive_count: i64 }

// Same shape for XBulkSetActiveResponse { updated, skipped_ids, active_count, inactive_count }
// and XDeleteResponse { id, active_count, inactive_count }.

impl FacetCounts for XMutationResponse        { /* … */ }
impl FacetCounts for XBulkSetActiveResponse   { /* … */ }
impl FacetCounts for XDeleteResponse          { /* … */ }
```

**Rules:**

- `#[serde(rename_all = "camelCase")]` on every wire struct.
- `PartialEq` on every mutation response — `MutationBinder`'s edge-triggered Effect requires it.
- Facet counts on every mutation response — count signals reconcile without a separate refetch.
- Skipped ids on bulk responses — drives the partial-success warning toast.

Deep dive: [`references/server-fns.md`](references/server-fns.md).

---

## 12. Anti-patterns

- `router.refresh()` after a mutation — diverges from the mutation-response-wins contract.
- Optimistic UI: writing to `table_data` before the server responds.
- Hand-rolled `fetch()` from an island.
- Updating local row state from form values instead of the mutation response payload.
- POST/PATCH/PUT followed by an explicit GET to refetch the row.
- `.read()` in a `Memo` / `Resource` source — dependency never registers.
- Client-side row reordering.
- Translation context call inside an island body — use `XLabelBundle`.
- `#[allow(...)]` to silence unused-fn warnings.
- `unwrap()`/`expect()` in handlers/services/workers/islands.
- `<Suspense>` for paginated tables — use `<Transition>`.
- `ToastHost` mounted inside the table island.
- Forgetting `ReconcileStrategy::ReplaceOrAppend` on sheet save — creates silently no-op.
- Multiple `Resource` calls for the same data.
- `impl Row for XDto` — orphan-rule violation; newtype.
- Sort `<th on:click>` in a `#[component]` — handler dead; use anchor.
- Bulk bar in a `#[component]` table footer — click handler dead; place inside the table island.

---

## 13. Verification hooks (run from repo root)

Adjust glob roots if the project uses a non-`src/` layout (e.g. `crates/`, `apps/`).

### 13.1 Behavior / anti-pattern hooks

```bash
# H1 — no router.refresh() in islands
git grep -nE 'router\.refresh|use_navigate.*refresh|location\.reload' -- '*.rs' \
  | grep -E '(islands|widgets)/'

# H2 — no <Suspense> on paginated tables
git grep -lnE '<Suspense' -- '*.rs' \
  | xargs -I{} grep -lE 'TableData|use_query_map|PageNavigation' {} 2>/dev/null

# H3 — Resource source uses .get() not .read()
git grep -nE 'Resource::new\([^)]*\.read\(\)' -- '*.rs'

# H4 — no fetch() / reqwest / gloo_net from islands
git grep -nE 'web_sys::window\(\)\.fetch_|reqwest::|gloo_net::http::Request' -- '*.rs' \
  | grep -E '(islands|widgets)/'

# H5 — every <table> has <tbody>
git grep -n '<table' -- '*.rs' | grep -v '<tbody'

# H6 — no LocalResource for paginated table data
git grep -nE 'LocalResource::new|create_local_resource' -- '*.rs' \
  | grep -iE 'table|list|page'

# H7 — no unwrap()/expect() in production paths
git grep -nE '\.unwrap\(\)|\.expect\(' -- '*.rs' \
  | grep -vE '_test|tests/|#\[cfg\(test\)' \
  | grep -E '(islands|pages|server_fns|handlers)/'

# H8 — never impl Row for *Dto
git grep -nE '^impl\s+Row\s+for\s+\w+Dto' -- '*.rs'

# H9 — no location.href = / set_href in islands
git grep -nE 'set_href|location\.href\s*=' -- '*.rs' | grep -E '(islands|widgets)/'

# H10 — sort headers never use on:click (use anchor instead)
git grep -lnE '<th[^>]*on:click' -- '*.rs' \
  | xargs -I{} grep -l 'sort\|Sort' {} 2>/dev/null

# H11 — bulk bar lives in an #[island], not #[component]
for f in $(git grep -l 'bulk_action_bar\|BulkActionBar' -- '*.rs'); do
  head -40 "$f" | grep -qE '#\[island\]' \
    || echo "Possibly placed in #[component]: $f"
done

# H12 — ToastHost mounted once and not inside any table island
git grep -l 'ToastHost' -- '*.rs' | wc -l   # should be exactly 1
git grep -l 'ToastHost' -- '*.rs' | xargs -I{} grep -l 'TableData\|table_island' {} 2>/dev/null

# H13 — pagination mounted outside the table island
git grep -l 'PageNavigation\|PageNav' -- '*.rs' | xargs -I{} grep -l '#\[island\]' {} 2>/dev/null
```

### 13.2 Mutation hooks

```bash
# M1 — sheet save uses ReplaceOrAppend
for f in $(git grep -l 'sheet_saved_dto\|SavedSignalSource' -- '*.rs'); do
  grep -qE 'ReconcileStrategy::ReplaceOrAppend|reconcile.*ReplaceOrAppend' "$f" \
    || echo "MISSING ReplaceOrAppend on sheet-save: $f"
done

# M2 — bulk uses ClearAll, delete uses RemoveMissing, single uses Preserve
for f in $(git grep -l 'MutationBinder' -- '*.rs'); do
  echo "== $f =="; grep -nE 'SelectionPolicy::(ClearAll|RemoveMissing|Preserve)' "$f"
done

# M3 — every mutation/bulk/delete response impls FacetCounts
for f in $(git ls-files '*.rs'); do
  for name in $(grep -oE 'pub struct \w+(Mutation|BulkSetActive|Delete)Response' "$f" 2>/dev/null | awk '{print $3}'); do
    git grep -qE "impl FacetCounts for $name" -- '*.rs' \
      || echo "MISSING-FACETCOUNTS: $name (declared in $f)"
  done
done

# M4 — wire structs derive Clone+PartialEq and use camelCase
for f in $(git ls-files '*.rs' | xargs -I{} grep -l 'pub struct \w\+\(Dto\|Request\|Response\)' {} 2>/dev/null); do
  awk -v F="$f" '
    /#\[derive/ { d=$0 }
    /pub struct/ {
      if (d !~ /Clone/)     print F":"NR": MISSING Clone on "$0;
      if (d !~ /PartialEq/) print F":"NR": MISSING PartialEq on "$0;
    }
  ' "$f"
done

# M5 — toggle pending clears on both Ok and Err
for f in $(git grep -l 'pending_toggle_id' -- '*.rs'); do
  awk '
    /pending_toggle_id/ { found=1 }
    /Effect::new/ && found {
      lines=""; for (i=0; i<25; i++) { getline next_line; lines = lines "\n" next_line }
      if (lines !~ /set\(None\)/) print FILENAME": pending_toggle_id Effect does not clear to None"
      found=0
    }
  ' "$f"
done

# M6 — no optimistic write to table_data before Action resolves
git grep -nB2 'table_data\.set_all\|table_data\.upsert\|table_data\.remove\|table_data\.replace' -- '*.rs' \
  | grep -vE 'MutationBinder|on_response|value\(\)\.get|Effect::new|refetch_action'
```

### 13.3 Island context hooks

```bash
# I1 — every table island provides canonical contexts
for f in $(git ls-files '*table_island*.rs' '*table_island*/mod.rs' 2>/dev/null); do
  echo "== $f =="
  grep -nE 'provide_context\((TableData|Selection|FacetCounts|FacetRefetch|.*SheetController)' "$f" \
    || echo "MISSING-CONTEXT"
done

# I2 — sortable_header_link always receives a refetch callback
git grep -nE 'sortable_header_link\(' -- '*.rs' | grep -vE 'refetch_cb|FacetRefetch|Callback'

# I3 — selection cell uses with_untracked (not with)
git grep -lnE 'visible_ids|selection_header_checkbox|selection_checkbox' -- '*.rs' \
  | xargs -I{} grep -HnE 'table_data\.rows\.with\(' {} 2>/dev/null

# I4 — column-toggle state is NOT in the URL
git grep -lnE 'hidden_columns|hidden_cols' -- '*.rs' \
  | xargs -I{} grep -HnE 'use_query_map|navigate|pushState' {} 2>/dev/null
```

### 13.4 Label-bundle hooks

```bash
# L1 — translation context never called inside an #[island]
for f in $(git grep -l '#\[island\]' -- '*.rs'); do
  grep -nE '\.t\(\s*"|LanguageContext|expect_context.*LanguageContext' "$f" \
    && echo "  ^^ translation called inside #[island]: $f"
done

# L2 — Label is Arc<str> and serde has `rc` feature
git grep -nE 'pub type Label = |type Label =' -- '*.rs'
grep -E '^serde\b.*features\s*=' Cargo.toml */Cargo.toml */*/Cargo.toml 2>/dev/null \
  | grep -v '"rc"' \
  && echo "MISSING serde \"rc\" feature in one of the manifests above"

# L3 — every bundle has a serde_json round-trip test
for f in $(git grep -l 'LabelBundle' -- '*.rs'); do
  grep -qE 'serde_json::(to_string|from_str).*LabelBundle|round_trip' "$f" \
    || echo "MISSING round-trip test: $f"
done

# L4 — from_lang is #[cfg(feature = "ssr")]
for f in $(git grep -l 'fn from_lang' -- '*.rs'); do
  grep -B1 'fn from_lang' "$f" | grep -q 'cfg.*feature.*ssr' \
    || echo "MISSING #[cfg(feature = \"ssr\")] on from_lang: $f"
done
```

### 13.5 Layout hooks

```bash
# Y1 — hidden columns gate header and body together
for f in $(git grep -l 'hidden_columns' -- '*.rs'); do
  th=$(grep -c '<th' "$f"); body_gates=$(grep -c 'hidden_columns.with' "$f")
  echo "$f: <th>=$th, hidden-column gates=$body_gates"
done

# Y2 — empty-state copy exists
for f in $(git grep -l 'TableData' -- '*.rs'); do
  grep -qiE 'empty|no.results|no.records|no.items|no.data' "$f" \
    || echo "MISSING empty-state copy: $f"
done
```

---

## 14. Build / refit a page — quickstart

1. **Read** [`references/canonical-architecture.md`](references/canonical-architecture.md) end-to-end.
2. **Inventory** the page: filters, sort columns, bulk actions, row actions, facets.
3. **Extend the repo first**: expose `list_paginated_filtered`, `create`, `update`, `delete`, `bulk_set_active` returning full rows + facet counts.
4. **Build DTOs** per §11: `XDto`, `XListResponse`, `XMutationResponse`, `XBulkSetActiveResponse`, `XDeleteResponse` — each with `FacetCounts` impl where applicable. `camelCase` + `PartialEq` + `Clone` + `Debug`.
5. **Build the label bundle** per §10.
6. **Build the island** per §8: contexts in canonical order → `XRow` newtype → `refetch_action` → four `MutationBinder` installs per §9.
7. **Build the page shell** per §7: query map → params Memo → Resource → `<Transition>` → `<ErrorBoundary>` → island + pagination.
8. **Register the page** in the project's page-router and any seed/registry guards.
9. **Update API docs** with the new server-fn signatures.
10. **Validate** with §13 hooks + the project's quality-gates.

---

## 15. Validation checklist (per page, before merge)

### Functional

- [ ] Every filter is present and URL-bound.
- [ ] Every controller button is present.
- [ ] Sort columns match inventory exactly.
- [ ] Bulk actions match inventory exactly (variant, label, behavior).
- [ ] Row mutations (toggle, edit, delete) repaint from the server response payload — no manual refresh.
- [ ] Back/Forward navigates through filter/sort/pagination history correctly.
- [ ] Deep-linking `?search=foo&sort_by=name&sort_dir=desc&is_active=true&page=2` lands on that state fully SSR.

### Reactive

- [ ] Exactly one fetch per filter/sort/pagination interaction.
- [ ] Sort/filter clicks do NOT reload the document.
- [ ] Facet counters update immediately after a status-changing mutation.
- [ ] Selection survives filter/sort/pagination.
- [ ] Selection clears after a bulk action; drops the deleted id after a delete.
- [ ] Row-scoped pending disables only the affected row.

### Hydration

- [ ] Zero hydration mismatch warnings in console.
- [ ] Every island prop derives `Serialize + Deserialize`.
- [ ] No island reads a Resource via context.
- [ ] No `cfg!(feature = "ssr")` branches inside `view!{}`.

### Performance

- [ ] No unnecessary `table_data.set_all(...)` calls.
- [ ] `<For>` uses a stable `key=` on the row id.
- [ ] Memos guard expensive per-row computations.
- [ ] No N+1 queries.

### Architecture

- [ ] No duplicated reactive glue — extract reused patterns to a shared primitive.
- [ ] Business logic lives in service layer. REST and `#[server]` both call the same service method.
- [ ] No `router.refresh()`, no optimistic UI, no `fetch()` in islands, no `unwrap()` in production paths, no `#[allow(...)]`.
- [ ] API docs updated with every new server-fn signature.
- [ ] Tests: label round-trip + params-memo unit test + Playwright e2e covering the golden path.

---

## References (deep dives)

- [`references/canonical-architecture.md`](references/canonical-architecture.md) — the long-form architecture explainer.
- [`references/wireframe.md`](references/wireframe.md) — layout/design walkthrough with spacing + responsive details.
- [`references/island.md`](references/island.md) — island contract, contexts, refetch action, sort-link pairing.
- [`references/mutations.md`](references/mutations.md) — binder installs, flows, concurrency.
- [`references/labels.md`](references/labels.md) — bundle composition, tests, Label newtype.
- [`references/server-fns.md`](references/server-fns.md) — server-fn skeleton, DTO contract, repository expectations.

Related skills (do NOT skip when relevant): [[leptos-islands]], [[leptos-hydration-discipline]], [[leptos-server-fn]], [[leptos-data-loading]], [[leptos-action-form]], [[dto-domain]], [[sqlx-query]], [[quality-gates]].
