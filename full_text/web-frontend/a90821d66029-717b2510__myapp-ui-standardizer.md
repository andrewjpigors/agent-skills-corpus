---
name: myapp-ui-standardizer
description: Standardizes MyApp frontend windows so they are visually consistent with the rest of the project. Includes patterns for skeletons that replicate the real structure, entity loading in the controller for detail views, modern cards (uniform height, footer with pill and actions), and brand colors (papaia/nautical). Analyzes the current HTML, detects what is missing, and generates the necessary CSS and HTML patch. Use when the user says "standardize window", "standardize view", "UI standardize", "improve style of", "adjust styles", or wants to make a specific view match MyApp visual standards.
---

# MyApp UI Standardizer

Your goal is to standardize a specific window of the MyApp project so it is visually consistent with the rest of the application.

## Pre-loaded context

### Stack

- AngularJS 1.x (`myApp` module) + Angular Material + Bootstrap 3
- Global CSS in `src/main/webapp/content/css/` (NO CSS variables, NO dark mode)
- Entity-specific styles go in inline `<style>` blocks at the end of the HTML template

### Main CSS files

| File | Contents |
|------|----------|
| **`content/css/myapp-standard.css`** | **Centralized standardization file. ALWAYS check here first before creating new CSS.** |
| `content/css/original-myapp.css` | Core colors, layout, spacing utilities |
| `content/css/custom.css` | Overrides, custom components (billing, banners, animate.css) |
| `content/css/main.css` | `form-wrapper`, official buttons, base skeleton, login |
| `content/css/layout.css` | Metronic layout (sidebar, page header) |
| `content/css/components.css` | Metronic components (portlets, dashboard) |

### Visual reference windows

Consult these windows according to the type of view to standardize:

| View type | Reference | Key patterns |
|-----------|-----------|--------------|
| **List/cards** | `entities/visitant-invitation/visitants-user-invited.html` | Cards (`visitor-card-v2`), chips, search bar, skeleton cards, `md-menu`, FAB, responsive |
| **Expandable card list / sub-card grid** | `entities/accounting-full-period/accounting-full-periods.html` | Cards by period (header + expandable body), child card grid (month), card footer with pill + actions (Reopen/Delete), skeleton replicating period + month structure, papaia/nautical colors |
| **Form** | `entities/owner/owner-form.html` | `form-wrapper` + `ng-cloak` + `fade-in`, `form-title`, `form-content`, `setInvalidForm`, two-column layout (`col-lg-6` + `divFormsMDXS`), `md-progress-circular` loader, translate on labels |
| **Dashboard/detail** | `entities/house/house-administration.html` | Header with selector, skeleton with global `.skeleton`, nav tabs (`acc-sub-nav`), `<loader>`, mobile-specific sections, `<no-content>`, `ui-view` child routes |
| **Detail with controller-side load** | `entities/accounting-period/accounting-period-detail.html` | Entity loaded in controller (`loadEntity` + `vm.isReady`), skeleton replicating real structure (same blocks and classes: `bank-container`, `bank-container-title`, account tree), no `entity` in state resolve |
| **Data table** | `entities/egress/egresses.html` | `tableMaterialDesign`, `table-scrollable`, `ad-table-header`, `md-menu` for actions, status dots with `ad-status-*`, cards on mobile + table on desktop, currency with `fMoneyBank()` |
| **Table with search** | `entities/bitacora-acciones/bitacora-acciones.html` | `tableMaterialDesign`, `jh-sort` for sorting, table skeleton, infinite scroll, search bar |
| **Report/table with export** | `entities/charge/billingReport.html` | `tableMaterialDesignAccountStatus`, `excel-data`, `fMoneyExport()`, status badges, totals row, `id="tableToExport"` |

### MyApp color palette and brand

For the full color and class reference, see [css-reference.md](css-reference.md).

**MyApp brand colors (use in semantic states, badges and buttons):**
- **Papaia** (open, active, warm accent): `#deb66e` (main), `#eeddbf` (badge background), `#5c4a1a` (text on light background), icon gradient `#deb66e` → `#c9a84a`. Existing classes: `.papaia-fresh-font`, `.orange-button-oficial`.
- **Nautical** (closed, primary, actions): `#001e2f` (main), `#002a42` (hover), `#e3eef9` (badge background). Classes: `.nautical-blue-font`, `.background-nautical-blue`.
- Custom branded badges: e.g., `.afp-badge-abierto { background: #eeddbf; color: #5c4a1a; }`, `.afp-badge-cerrado { background: #e3eef9; color: #001e2f; }`.
- Header gradient icons: `.icon--open { background: linear-gradient(135deg, #deb66e 0%, #c9a84a 100%); }`, `.icon--closed { background: linear-gradient(135deg, #001e2f 0%, #002a42 100%); }`.

### Standardization preferences

- **Scope**: HTML and CSS always. Controller (.js) only if critical (e.g., missing `vm.isReady`, `vm.searching`, `$rootScope.mainTitle`).
- **Aggressiveness**: Fix EVERYTHING -- i18n (hardcoded text), HTML semantics, accessibility, inline styles. Not just visual.
- **Skeleton**: ALWAYS propose skeleton loaders (it's the modern pattern). Replace `<loader>` spinners with skeletons whenever possible. The skeleton must **replicate the structure** of the view (same containers, classes and hierarchy) to avoid visual jump on load.
- **CSS location**: Reusable classes go in `content/css/myapp-standard.css` (ALWAYS read this file first to avoid duplication). Only styles very specific to a single view go inline in `<style>`.
- **Mobile**: ALWAYS generate a functional mobile version of the window. It's not enough that it "doesn't break" on mobile; the view must be **usable and complete** on small screens. See "Mobile Standardization" section for required patterns by view type.
- **Output**: Apply changes directly to the file (execution mode). Show the Style Map first as a summary.

### Critical restrictions

- **NO dark mode** in MyApp. Do not generate dark mode support.
- **NO CSS custom properties** (variables). Do not create `--var` or use `:root`.
- **NO 8px grid**. Spacing uses mixed values: 5, 8, 10, 12, 15, 16, 20, 30, 40, 50px.
- **NO BEM prefix or `.ad-`** for view classes. Scoping uses the entity domain prefix (e.g., `visitor-*`, `email-activity-*`). Globally reusable classes in `myapp-standard.css` DO use the `ad-` prefix.
- **The global skeleton is called `placeHolderShimmer`** (not `skeleton-loading`). See css-reference.md for the two skeleton systems.

---

## Skeleton loaders – structure that replicates the view

**Critical rule:** The skeleton must use the **same container structure and the same classes** as the real view, not generic blocks. That way, when data loads there is no visual "jump" and the user recognizes the same screen.

1. **Replicate hierarchy and classes:** Same wrappers (`bank-container`, `bank-container-title`, `padding-5-10`, etc.) and same layout (header + body, nested blocks). Placeholders are `<span class="skeleton">` or existing skeleton classes (e.g., `ic-skeleton-line`, `ic-skeleton-card-header`) with inline `width`/`height`.
2. **View with multiple blocks:** If the view has multiple blocks (e.g., "Initial check" + "accounting accounts"), the skeleton must have the same blocks in the same order, with placeholders instead of content.
3. **View with tree or repeated list:** Replicate 2–3 example items (section header + nested rows) with the same indentation and classes (`row-bottom-gray`, `margin-left-10`, etc.).
4. **Reference:** `accounting-period-detail.html` (skeleton with Initial check block + accounting accounts block with account tree); `accounting-full-periods.html` (skeleton with period cards and grid of month cards).

---

## Detail views – entity loading in controller

For **detail** views that today receive the entity via **state resolve**, it is preferable to **move the load to the controller** and show a skeleton in the template. That way the route resolves instantly and the screen does not stay "stuck" until the server responds.

**Steps:**
1. **State:** Remove `entity` from the state's `resolve`. Keep `previousState` and `translatePartialLoader` if applicable.
2. **Controller:** Do not inject `entity`. Initialize `vm.accountingPeriod = null` (or the entity name) and `vm.isReady = false`. Create `loadEntity()` that gets the id from `$stateParams`, decrypts it if applicable, and calls the service (e.g., `Entity.get({id: id}, success, error)`). On success: assign the entity to `vm`, `vm.isReady = true`, and call any secondary load (e.g., `loadInitialCheck()`). On error: `vm.isReady = true` and error toast. Call `loadEntity()` at the end of the controller (replacing the `entity` dependency in resolve).
3. **Template:** Real content wrapped in `ng-if="vm.isReady"`. Skeleton with `ng-if="!vm.isReady"` that **replicates the structure** of the view (same blocks and classes). See "Skeleton loaders – structure that replicates the view".

**Reference:** `accounting-period.state.js` (no `entity` in resolve), `accounting-period-detail.controller.js` (`loadEntity`, `vm.isReady`), `accounting-period-detail.html` (skeleton + content with `ng-if="vm.isReady"`).

---

## Modern cards (lists and grids)

For card lists (e.g., periods with monthly sub-cards), use these patterns so they don't get misaligned and the actions don't break the layout.

### Uniform card height in grid

- Grid container: `display: flex; flex-wrap: wrap; gap: 16px; align-items: stretch;`
- Each card: `display: flex; flex-direction: column; min-height: 140px;` (or appropriate value). Main content with `flex: 1` and `min-height` if needed so the footer stays at the bottom.
- The `md-card-content` (or internal wrapper): `flex: 1; display: flex; flex-direction: column; min-height: 0;` so flex distributes correctly.

### Card footer (pill + actions)

- Structure: content area (`flex: 1`) + **footer** with `margin-top`, `padding-top`, `border-top`, `flex-shrink: 0`.
- Footer: `layout="row" layout-align="space-between center"`. Left: status pill/badge. Right: action button(s) (Reopen, Delete, etc.).
- **When there is no button:** Add a conditional class to the footer (e.g., `ng-class="{'card-footer--no-actions': !hasAction}"`). In CSS: `.card-footer--no-actions .badge-wrapper { margin-left: auto; }` so the pill aligns to the right.

### Card actions

- Main action (e.g., "Reopen"): `md-button` with icon + text, nautical style (`#001e2f`). Placed in the footer on the right.
- Destructive action (e.g., "Delete"): icon only (`md-icon`) in red (`#c62828`, hover `#b71c1c`) to save space; use `$event.stopPropagation()` if the card is clickable (going to detail).
- States (OPEN/CLOSED): pills with brand colors (papaia for open, nautical for closed) or `ad-badge-success`/`ad-badge-info` if branding is not required.

### Reference

`accounting-full-periods.html`: period cards with header (icon + title + badges), expandable body, grid of month cards with footer (pill + Reopen or Delete icon), skeleton replicating period + month.

---

## Table standardization

Tables are one of the most used and most inconsistent components of the project. This section defines the standard pattern for tables and how to migrate legacy tables.

### Anatomy of a standard MyApp table

A standard table has these layers (from outside in):

```
[scrollable wrapper]
  [table element with base classes]
    [thead with standard background]
      [tr with columns]
        [th with centered text and/or sorting]
    [tbody]
      [tr with hover, ng-repeat]
        [td with data, badges, actions]
    [tfoot optional for totals]
```

### Base table classes

**Standard pattern (preferred):**
```html
<table class="table table-hover tableMaterialDesign">
```

**Existing variants (DO NOT create new ones):**

| Class | Padding | Use |
|-------|---------|-----|
| `tableMaterialDesign` | `6px` | General table (default) |
| `tableMaterialDesignPayments` | `15px` | Payment tables (more spacing) |
| `tableMaterialDesignAccountStatus` | `7px` | Account status |
| `tableMaterialDesignResultStates` | `8px top/bottom, 5px sides` | Accounting result states |
| `tableMaterialDesignResidents` | `15px top/bottom, 5px sides` | Residents table |

**Rule:** When standardizing, use `tableMaterialDesign` as the default. Only use variants when the context requires it (e.g., a payments table needs more padding). NEVER create a new `tableMaterialDesign*` variant.

**Optional complementary classes:**
- `table-bordered` -- adds borders between cells (use only if the table has many columns and needs visual separation)
- `font-13` -- sets font-size to 13px (use in dense tables)
- `gray-font` -- gray text color (`#616161`)

### Scrollable wrapper

**For tables with many columns (>6) or that need horizontal scroll:**
```html
<div class="table-scrollable gray-font" style="border: 0 !important;">
    <table class="table table-hover tableMaterialDesign">
        ...
    </table>
</div>
```

**Note:** `table-scrollable` adds `border: 1px solid #ddd` by default. If the table is already inside a `form-content` or card, use `style="border: 0 !important;"` to remove the double border.

**For simple tables (<=6 columns):** No wrapper is needed; the table can go directly.

### Standard thead

```html
<thead class="ad-table-header">
    <tr class="text-center">
        <th>Column 1</th>
        <th>Column 2</th>
        <th class="text-center">Actions</th>
    </tr>
</thead>
```

**Class `ad-table-header`** (defined in `myapp-standard.css`): applies `background-color: #fafafa` and consistent header styles. Use this class instead of the inline `style="background-color: #fafafa;"` that exists in many legacy tables.

**If the table has sorting:**
```html
<thead class="ad-table-header">
    <tr class="text-center" jh-sort="vm.predicate" ascending="vm.reverse" callback="vm.transition()">
        <th jh-sort-by="concept">Concept</th>
        <th jh-sort-by="date" class="text-center">Date</th>
        <th>Actions</th> <!-- action columns are NOT sortable -->
    </tr>
</thead>
```

**Sorting with custom `ng-click` (alternative pattern):**
```html
<thead class="ad-table-header">
    <tr class="text-center">
        <th class="pointer" ng-click="vm.sortBy('concept')">Concept</th>
        <th class="pointer text-center" ng-click="vm.sortBy('date')">Date</th>
    </tr>
</thead>
```

### Standard tbody

```html
<tbody>
    <tr class="text-center" ng-repeat="item in vm.items track by item.id">
        <td>{{item.name}}</td>
        <td class="text-center">{{item.date | date:'dd/MM/yyyy'}}</td>
        <td class="text-center ad-table-actions-cell">
            <!-- actions -->
        </td>
    </tr>
</tbody>
```

### Actions column

**Pattern with `md-menu` (preferred for 2+ actions):**
```html
<td class="text-center ad-table-actions-cell">
    <md-menu md-position-mode="target-right target">
        <md-button aria-label="Options" class="md-icon-button no-padding"
                   ng-click="$mdMenu.open($event)">
            <md-icon style="color: #999;">more_vert</md-icon>
            <md-tooltip md-direction="left" class="font-13 bold white-color">Options</md-tooltip>
        </md-button>
        <md-menu-content width="4">
            <md-menu-item>
                <md-button ng-click="vm.view(item)">
                    <div layout="row" flex><p flex>View detail</p></div>
                </md-button>
            </md-menu-item>
            <md-menu-item>
                <md-button ng-click="vm.edit(item)">
                    <div layout="row" flex><p flex>Edit</p></div>
                </md-button>
            </md-menu-item>
            <md-menu-item>
                <md-button ng-click="vm.delete(item)">
                    <div layout="row" flex><p flex>Delete</p></div>
                </md-button>
            </md-menu-item>
        </md-menu-content>
    </md-menu>
</td>
```

**Pattern with direct icons (for 1-2 simple actions):**
```html
<td class="text-center ad-table-actions-cell">
    <md-icon class="pointer" style="color: #999; font-size: 20px;"
             ng-click="vm.view(item)" aria-label="View detail">
        <md-tooltip>View detail</md-tooltip>
        remove_red_eye
    </md-icon>
</td>
```

### Badges and status in cells

**Use `ad-badge-*` badges from `myapp-standard.css`:**
```html
<td class="text-center">
    <span class="ad-badge ad-badge-success" ng-if="item.status === 'active'">Active</span>
    <span class="ad-badge ad-badge-error" ng-if="item.status === 'cancelled'">Cancelled</span>
    <span class="ad-badge ad-badge-warning" ng-if="item.status === 'pending'">Pending</span>
</td>
```

**Status indicators with icon (colored dot):**
```html
<td class="text-center">
    <md-icon class="ad-status-icon ad-status-success" ng-if="item.state === 2">lens</md-icon>
    <md-icon class="ad-status-icon ad-status-warning" ng-if="item.state === 1">lens</md-icon>
    <md-icon class="ad-status-icon ad-status-error" ng-if="item.state === 3">lens</md-icon>
    <md-tooltip>{{item.stateLabel}}</md-tooltip>
</td>
```

### Monetary values in cells

```html
<!-- Basic format (primary currency) -->
<td class="text-right">{{fMoney(item.amount)}}</td>

<!-- Format with variable currency -->
<td class="text-right">{{fMoneyBank(item.currency, item.amount)}}</td>

<!-- Format compatible with Excel export -->
<td class="text-right">{{fMoneyExport(vm.exportingExcel, item.amount)}}</td>

<!-- Value with positive/negative color -->
<td class="text-right" ng-class="{'ad-value-positive': item.balance >= 0, 'ad-value-negative': item.balance < 0}">
    {{fMoney(item.balance)}}
</td>
```

### Totals row

```html
<tfoot>
    <tr class="ad-table-totals-row">
        <td colspan="4" class="text-right"><b>Total</b></td>
        <td class="text-right"><b>{{fMoney(vm.total)}}</b></td>
        <td></td> <!-- empty cell if there is an actions column -->
    </tr>
</tfoot>
```

### Skeleton loader for tables

**Table with data on page load:**
```html
<!-- Skeleton -->
<div class="table-skeleton margin-top-20" ng-if="!vm.isReady">
    <table class="table table-hover tableMaterialDesign">
        <thead class="ad-table-header">
            <tr class="text-center ad-skeleton-table-header">
                <th><span class="skeleton" style="width: 80px; height: 16px; display: inline-block;"></span></th>
                <th><span class="skeleton" style="width: 100px; height: 16px; display: inline-block;"></span></th>
                <th><span class="skeleton" style="width: 60px; height: 16px; display: inline-block;"></span></th>
            </tr>
        </thead>
        <tbody>
            <tr class="text-center ad-skeleton-table-row" ng-repeat="i in [1,2,3,4,5,6] track by i">
                <td><span class="skeleton" style="width: 90px; height: 14px; display: inline-block;"></span></td>
                <td><span class="skeleton" style="width: 120px; height: 14px; display: inline-block;"></span></td>
                <td><span class="skeleton" style="width: 50px; height: 14px; display: inline-block;"></span></td>
            </tr>
        </tbody>
    </table>
</div>

<!-- Real table -->
<div ng-if="vm.isReady">
    ...
</div>
```

**Table with search/filters (data on demand):**
```html
<!-- Skeleton appears ONLY when searching -->
<div class="table-skeleton margin-top-20" ng-if="!vm.isReady && vm.searching">
    <!-- same skeleton pattern -->
</div>
```

**Tip:** Adjust the `width` of each `<span class="skeleton">` to the approximate width of the real content for that column. Headers a bit wider (`16px` height), cells a bit smaller (`14px` height). In complex views (detail, nested cards), the skeleton must replicate the real structure; see "Skeleton loaders – structure that replicates the view".

### Responsive table (mobile)

There are two patterns for handling tables on mobile:

**Pattern 1: Horizontal scroll (default, for simple tables)**
Use `table-scrollable` wrapper. The table scrolls horizontally on mobile. Apply `hidden-xs` to less important columns to reduce width.

```html
<div class="table-scrollable gray-font" style="border: 0 !important;">
    <table class="table table-hover tableMaterialDesign">
        <thead class="ad-table-header">
            <tr class="text-center">
                <th>Name</th>
                <th>Amount</th>
                <th class="hidden-xs">Date</th> <!-- hidden on mobile -->
                <th class="hidden-xs">Status</th> <!-- hidden on mobile -->
                <th class="text-center">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr ng-repeat="item in vm.items">
                <td>{{item.name}}</td>
                <td>{{fMoney(item.amount)}}</td>
                <td class="hidden-xs">{{item.date | date:'dd/MM/yyyy'}}</td>
                <td class="hidden-xs">...</td>
                <td class="text-center">...</td>
            </tr>
        </tbody>
    </table>
</div>
```

**Pattern 2: Cards on mobile, table on desktop (for tables with rich data)**
Show cards on small screens and table on desktop. Use Bootstrap visibility classes.

```html
<!-- Cards for mobile (visible only on xs/sm/md) -->
<div hide-lg hide-xl ng-show="vm.items.length > 0">
    <md-card ng-repeat="item in vm.items"
             class="margin-bottom-16 residentCardContainer outline-none">
        <!-- card content with key data -->
    </md-card>
</div>

<!-- Table for desktop (visible only on lg+) -->
<div class="table-scrollable gray-font" style="border: 0 !important;" 
     hide-xs hide-sm hide-md ng-show="vm.items.length > 0">
    <table class="table table-hover tableMaterialDesign">
        ...
    </table>
</div>
```

**When to use each pattern:**
- **Pattern 1 (scroll):** Tables with <= 5 columns, simple data, reports for export
- **Pattern 2 (cards):** Tables with > 5 columns, rich data with actions, main CRUD views

### Table with pagination

```html
<!-- Table -->
<table class="table table-hover tableMaterialDesign">
    ...
</table>

<!-- Pagination (below the table) -->
<div class="text-center" ng-show="vm.items.length > 0">
    <jhi-item-count page="vm.page" total="vm.queryCount" items-per-page="vm.itemsPerPage"></jhi-item-count>
    <uib-pager ng-model="vm.page" ng-change="vm.loadPage(vm.page)"
               total-items="vm.queryCount" items-per-page="vm.itemsPerPage"
               previous-text="&lsaquo;" next-text="&rsaquo;"></uib-pager>
</div>
```

### Table with Excel export

If the table supports export, add `id="tableToExport"` and the `excel-data` class:
```html
<table id="tableToExport" class="table table-hover tableMaterialDesign excel-data">
```

And use `fMoneyExport(vm.exportingExcel, value)` so monetary values export correctly.

### Table standardization checklist

When standardizing a table, verify each item:

- [ ] Uses correct base classes: `table table-hover tableMaterialDesign` (or justified variant)
- [ ] `<thead>` uses class `ad-table-header` (not inline `style="background-color: #fafafa;"`)
- [ ] `<th>` are semantically correct (only in `<thead>`, not in `<tbody>`)
- [ ] Action columns use `md-menu` (2+ actions) or direct icons (1 action)
- [ ] Action columns have `aria-label` on buttons
- [ ] Status badges use `ad-badge-*` or `ad-status-*` (no inline colors)
- [ ] Monetary values use `fMoney()` / `fMoneyBank()` / `fMoneyExport()`
- [ ] Monetary values have `text-right` (right alignment)
- [ ] Positive/negative value colors use `ad-value-positive` / `ad-value-negative`
- [ ] Hardcoded text replaced with `| translate`
- [ ] `table-scrollable` wrapper if there are >6 columns (with `border: 0 !important` if inside card/form-content)
- [ ] `hidden-xs` on less important columns to reduce width on mobile
- [ ] Skeleton loader present with table structure (no spinner `<loader>`)
- [ ] Skeleton uses global `.skeleton` class with appropriate inline `width`/`height`
- [ ] Totals row (if applicable) uses `<tfoot>` with class `ad-table-totals-row`
- [ ] `<no-content>` for empty table
- [ ] If the table has many columns + rich data, consider cards on mobile (Pattern 2)

### Legacy table migration

**Common problems in existing tables and how to fix them:**

| Problem | Solution |
|---------|----------|
| `style="background-color: #fafafa;"` on `<thead>` | Replace with `class="ad-table-header"` |
| `<th>` inside `<tbody>` | Change to `<td>` with `<b>` if bold is needed |
| Status with inline colors (`style="color: #FF3D00;"`) | Use `ad-status-*` or `ad-badge-*` |
| `<loader>` or `md-progress-circular` for table | Replace with table skeleton |
| `jh-table table table-striped` (legacy JHipster) | Migrate to `table table-hover tableMaterialDesign` |
| `table-responsive` (Bootstrap) | Migrate to `table-scrollable` with `border: 0 !important` |
| Button group for actions (`btn-group`) | Migrate to `md-menu` with `more_vert` |
| Inline font-size on `<table>` | Add `font-13` as a class if needed |
| Totals with extra `<tbody>` | Migrate to `<tfoot>` with `ad-table-totals-row` |

---

## Mobile Standardization

**CRITICAL RULE:** Every standardized window MUST have a functional and complete mobile version. MyApp is frequently used from mobile devices, and a view that just "doesn't break" on mobile is NOT acceptable. The mobile view must allow the user to complete all the tasks available on desktop.

### Required mobile principles

1. **Full functionality**: Every action available on desktop must be accessible on mobile. Never hide critical actions with `hidden-xs`.
2. **Readability**: Text readable without zoom, minimum 13px on mobile. Labels and values must fit without excessive truncation.
3. **Touch targets**: Clickable areas >= 44px on mobile (already included in accessibility, but critical for mobile).
4. **Vertical scroll**: Prefer vertical scroll over horizontal scroll. Tables with horizontal scroll are a justified exception, not the rule.
5. **Priority information**: On mobile, show the most important information first. Secondary data can go on a second line or expand on tap.

### Mobile patterns by view type

#### Forms

Forms are naturally responsive thanks to `layout-xs="column"` and `divFormsMDXS`. Verify additionally:

```html
<!-- Columns stack on mobile automatically -->
<div layout="row" layout-xs="column">
    <div flex class="col-lg-6 col-md-6 col-sm-6 white-bg divFormsMDXS">
        <md-input-container class="md-block">
            <label>Field 1</label>
            <input ng-model="vm.entity.field1">
        </md-input-container>
    </div>
    <div flex class="col-lg-6 col-md-6 col-sm-6 white-bg divFormsMDXS">
        <md-input-container class="md-block">
            <label>Field 2</label>
            <input ng-model="vm.entity.field2">
        </md-input-container>
    </div>
</div>
```

**Mobile checklist for forms:**
- [ ] Inputs use `md-block` to occupy 100% width
- [ ] Columns stack with `layout-xs="column"` or `divFormsMDXS`
- [ ] Action buttons are full-width on mobile (`width: 100%` in `@media max-width: 767px`)
- [ ] The title toolbar is hidden on mobile (`hide-sm hide-xs`) since the title goes in the navbar
- [ ] No side-by-side inputs that become illegible on mobile

#### Card lists

Cards are the ideal format for mobile. If the view already uses cards, verify:

```html
<!-- Cards: responsive by default with Bootstrap grid -->
<div class="col-md-4 col-sm-6 col-xs-12 no-padding residentDivContainerXs"
     ng-repeat="item in vm.items track by item.id">
    <md-card class="margin-bottom-16 residentCardContainer outline-none">
        <!-- Card content -->
    </md-card>
</div>
```

**Mobile checklist for cards:**
- [ ] Cards take 100% width on `xs` (`col-xs-12`)
- [ ] Card content does not truncate or overflow
- [ ] Card actions are accessible (buttons or `md-menu`)
- [ ] Card skeleton works on mobile (same responsive structure)
- [ ] Filter/tab chips have horizontal scroll if there are many (`overflow-x: auto` on the wrapper)

#### Tables (IMPORTANT RULE)

**Tables are the most problematic component on mobile.** Apply this decision:

| Table type | Mobile strategy |
|------------|-----------------|
| Main CRUD table (rich data, actions) | **REQUIRED**: Cards on mobile + table on desktop (Pattern 2a) |
| Simple table (<=3 columns, 1 action per row) | **Compact list** on mobile + table on desktop (Pattern 2b) |
| Simple table (<=4 columns, no complex actions) | Horizontal scroll (`table-scrollable`) with `hidden-xs` on secondary columns |
| Report/export table | Horizontal scroll (the user expects tabular format for reports) |
| Table with totals/accounting summary | Horizontal scroll + ensure "Total" column and amount are visible |

> **CRITICAL RULE: Mobile/desktop data parity.** The mobile version MUST ONLY show data that was already visible in the desktop version. NEVER add extra fields (extension, status, creation date, etc.) that were not shown in the original table. Mobile changes the **layout**, not the **content**.

**Pattern 2a: Cards with `md-card` (for tables with rich data: badges, amounts, multiple actions):**

```html
<!-- ===== MOBILE VERSION: Cards (visible on xs/sm) ===== -->
<div class="[entity]-mobile-cards" hide-gt-sm ng-show="vm.items.length > 0">
    <md-card ng-repeat="item in vm.items track by item.id"
             class="[entity]-mobile-card margin-bottom-8">
        <md-card-content class="no-padding">
            <div layout="row" layout-align="space-between start" class="padding-10">
                <!-- Main info -->
                <div flex="80" layout="column">
                    <span class="[entity]-mobile-card-title">{{item.name}}</span>
                    <span class="[entity]-mobile-card-subtitle">{{item.detail}}</span>
                    <div layout="row" layout-align="start center" class="margin-top-5">
                        <!-- Status badges -->
                        <span class="ad-badge ad-badge-success" ng-if="item.active">
                            {{'myApp.entity.active' | translate}}
                        </span>
                        <!-- Monetary value -->
                        <span class="[entity]-mobile-card-amount" ng-if="item.amount">
                            {{fMoney(item.amount)}}
                        </span>
                    </div>
                </div>
                <!-- Actions menu -->
                <div flex="20" layout="row" layout-align="end start">
                    <md-menu md-position-mode="target-right target">
                        <md-button aria-label="Options" class="md-icon-button no-padding"
                                   ng-click="$mdMenu.open($event)">
                            <md-icon style="color: #999;">more_vert</md-icon>
                        </md-button>
                        <md-menu-content width="4">
                            <md-menu-item>
                                <md-button ng-click="vm.view(item)">
                                    <div layout="row" flex><p flex>View detail</p></div>
                                </md-button>
                            </md-menu-item>
                            <md-menu-item>
                                <md-button ng-click="vm.edit(item)">
                                    <div layout="row" flex><p flex>Edit</p></div>
                                </md-button>
                            </md-menu-item>
                        </md-menu-content>
                    </md-menu>
                </div>
            </div>
        </md-card-content>
    </md-card>
</div>

<!-- ===== DESKTOP VERSION: Table (visible on md+) ===== -->
<div class="table-scrollable gray-font" style="border: 0 !important;"
     hide-xs hide-sm ng-show="vm.items.length > 0">
    <table class="table table-hover tableMaterialDesign">
        <thead class="ad-table-header">...</thead>
        <tbody>...</tbody>
    </table>
</div>
```

**Base CSS for mobile cards (add to inline `<style>`):**
```css
/* ========== [Entity] – Mobile Cards ========== */
.[entity]-mobile-card {
    border-radius: 10px;
    border: 1px solid #e8e8e8;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}
.[entity]-mobile-card-title {
    font-size: 14px;
    font-weight: 600;
    color: #1f2937;
    line-height: 1.3;
}
.[entity]-mobile-card-subtitle {
    font-size: 12px;
    color: #6b7280;
    margin-top: 2px;
}
.[entity]-mobile-card-amount {
    font-size: 14px;
    font-weight: 600;
    color: #1f2937;
    margin-left: 8px;
}
```

**Mobile cards skeleton:**
```html
<!-- Skeleton mobile cards -->
<div class="[entity]-mobile-cards" hide-gt-sm ng-if="!vm.isReady">
    <md-card ng-repeat="i in [1,2,3,4,5] track by i"
             class="[entity]-mobile-card margin-bottom-8">
        <md-card-content class="no-padding">
            <div layout="row" layout-align="space-between start" class="padding-10">
                <div flex="80" layout="column">
                    <span class="skeleton" style="width: 60%; height: 14px; display: inline-block;"></span>
                    <span class="skeleton" style="width: 40%; height: 12px; display: inline-block; margin-top: 6px;"></span>
                    <span class="skeleton" style="width: 30%; height: 12px; display: inline-block; margin-top: 6px;"></span>
                </div>
                <div flex="20">
                    <span class="skeleton" style="width: 24px; height: 24px; display: inline-block; border-radius: 50%;"></span>
                </div>
            </div>
        </md-card-content>
    </md-card>
</div>
```

**Pattern 2b: Compact list (for simple tables: <=3 columns, 1 action per row):**

Use when the table is simple and `md-card` would add excessive padding/margins. Uses divs with flex in a single bordered container, without `md-card`.

> **When to choose 2b over 2a:** If the desktop table has <=3 columns (e.g., name + action, or name + status + action) and a single action per row, use compact list. If it has badges, amounts, multiple actions, or rich data, use cards (2a).

```html
<!-- ===== MOBILE VERSION: Compact list (visible on xs/sm) ===== -->
<div class="[entity]-mobile-list" hide-gt-sm ng-show="vm.items.length > 0">
    <div class="[entity]-mobile-item"
         ng-repeat="item in vm.items track by item.id">
        <div class="[entity]-mobile-item-info">
            <span class="[entity]-mobile-item-label">Column name</span>
            <span class="[entity]-mobile-item-name">{{item.name}}</span>
        </div>
        <md-button class="orange-button-oficial [entity]-mobile-action-btn"
                   ng-click="vm.action(item)"
                   aria-label="Action on {{item.name}}">
            <md-icon class="material-icons-with-text material-icons"
                     style="color: white; margin-right: 4px; font-size: 16px;">send</md-icon>
            Action
        </md-button>
    </div>
</div>

<!-- ===== DESKTOP VERSION: Table (visible on md+) ===== -->
<div hide-xs hide-sm ng-show="vm.items.length > 0">
    <div class="table-scrollable" style="border: 0 !important;">
        <table class="table table-hover tableMaterialDesign">
            <thead class="ad-table-header">...</thead>
            <tbody>...</tbody>
        </table>
    </div>
</div>
```

**Base CSS for compact list (add to inline `<style>`):**
```css
/* ========== [Entity] – Mobile List ========== */
.[entity]-mobile-list {
    border: 1px solid #e8e8e8;
    border-radius: 8px;
    overflow: hidden;
    background: #fff;
}
.[entity]-mobile-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    border-bottom: 1px solid #f1f5f9;
}
.[entity]-mobile-item:last-child {
    border-bottom: none;
}
.[entity]-mobile-item-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
    flex: 1;
}
.[entity]-mobile-item-label {
    font-size: 11px;
    color: #9e9e9e;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    line-height: 1;
    margin-bottom: 2px;
}
.[entity]-mobile-item-name {
    font-size: 15px;
    font-weight: 600;
    color: #1f2937;
    line-height: 1.3;
}
.[entity]-mobile-action-btn {
    min-width: 85px !important; /* override Angular Material */
    min-height: 32px;
    line-height: 32px;
    font-size: 13px;
    margin: 0 !important;
}
```

**Compact list skeleton:**
```html
<!-- Skeleton mobile list -->
<div class="[entity]-mobile-list" hide-gt-sm ng-if="!vm.isReady">
    <div class="[entity]-mobile-item" ng-repeat="i in [1,2,3,4,5,6,7,8] track by i">
        <div class="[entity]-mobile-item-info">
            <span class="skeleton" style="width: 35px; height: 10px; display: block; margin-bottom: 4px;"></span>
            <span class="skeleton" style="width: 90px; height: 15px; display: block;"></span>
        </div>
        <span class="skeleton" style="width: 80px; height: 32px; display: inline-block; border-radius: 4px;"></span>
    </div>
</div>
```

#### Dashboard/detail

Dashboards have multiple sections that need to be reorganized on mobile:

**Mobile patterns for dashboards:**
- [ ] Sections in columns (`layout="row"`) stack on mobile (`layout-xs="column"`)
- [ ] KPIs/metrics use a responsive grid: `col-md-3 col-sm-6 col-xs-12` (2 per row on tablet, 1 on mobile)
- [ ] Navigation tabs scroll horizontally on mobile if there are many
- [ ] Charts resize correctly (width 100%)
- [ ] Header selectors and filters are full-width on mobile

```html
<!-- Responsive KPIs -->
<div layout="row" layout-xs="column" class="margin-bottom-16">
    <div flex class="col-md-3 col-sm-6 col-xs-12">
        <md-card class="[entity]-kpi-card">
            <span class="[entity]-kpi-label">Total</span>
            <span class="[entity]-kpi-value">{{fMoney(vm.total)}}</span>
        </md-card>
    </div>
    <!-- more KPIs... -->
</div>
```

#### Filters and search bars

```html
<!-- Search bar (already responsive via Bootstrap) -->
<div class="form-group no-padding col-md-6 col-sm-8 col-xs-12">
    <div class="input-icon" style="color:#484848!important;">
        <i class="fa fa-search"></i>
        <input type="text" class="form-control search-bar"
               placeholder="{{ 'myApp.entity.search' | translate }}"
               ng-model="vm.search">
    </div>
</div>

<!-- Multiple filters: in row on desktop, column on mobile -->
<div layout="row" layout-xs="column" class="margin-bottom-16">
    <md-input-container flex class="no-margin">
        <label>Filter 1</label>
        <md-select ng-model="vm.filter1">...</md-select>
    </md-input-container>
    <md-input-container flex class="no-margin">
        <label>Filter 2</label>
        <md-select ng-model="vm.filter2">...</md-select>
    </md-input-container>
    <md-button class="md-primary md-raised" ng-click="vm.search()">
        Query
    </md-button>
</div>
```

#### Modal dialogs

Dialogs with `$mdDialog` need mobile adjustment:

```css
/* Inside @media (max-width: 767px) of inline <style> */
@media (max-width: 767px) {
    md-dialog {
        min-width: 95vw !important; /* required Angular Material override */
        max-width: 95vw !important;
        margin: 8px !important;
    }
}
```

### Breakpoints and visibility classes

**Angular Material (preferred for hide/show):**

| Class | Visible on |
|-------|------------|
| `hide-xs` | Hidden on xs (< 600px) |
| `hide-sm` | Hidden on sm (600-959px) |
| `hide-gt-sm` | Hidden on > 959px (only visible on xs/sm) |
| `hide-md` | Hidden on md (960-1279px) |
| `hide-gt-md` | Hidden on > 1279px |
| `hide-lg` | Hidden on lg (>= 1280px) |

**Pattern: mobile vs desktop:**
```html
<!-- Mobile only (xs and sm): -->
<div hide-gt-sm>Mobile content</div>

<!-- Desktop only (md+): -->
<div hide-xs hide-sm>Desktop content</div>
```

**Bootstrap (for table columns):**

| Class | Hidden on |
|-------|-----------|
| `hidden-xs` | < 768px |
| `hidden-sm` | 768-991px |
| `hidden-md` | 992-1199px |
| `visible-xs` | Only visible < 768px |

### Required responsive CSS

**Every inline `<style>` block MUST include at least these mobile breakpoints:**

```css
/* ========== Mobile (< 768px) ========== */
@media (max-width: 767px) {
    /* Mobile adjustments: font sizes, paddings, layouts */
    .[entity]-element {
        padding: 8px;
        font-size: 13px;
    }
}

/* ========== Narrow mobile (< 480px) ========== */
@media (max-width: 480px) {
    /* Adjustments for very small screens */
    .[entity]-element {
        padding: 5px;
    }
}
```

**Common responsive adjustments:**
- Reduce `padding` and `margin` on mobile (e.g., `padding: 20px` desktop → `padding: 10px` mobile)
- Reduce `font-size` where necessary (but never < 12px)
- Full-width action buttons on mobile: `width: 100%; margin-bottom: 8px;`
- Hide secondary columns of tables: `hidden-xs`
- Floating FAB: verify it does not cover content on mobile

---

## Workflow

### Phase 1: Get the target window

Ask **only**:
1. Which is the target window (HTML file path or module/feature name)
2. Optionally, if there is a screenshot of the current state

Do not ask about stack, main CSS, or reference windows (already pre-loaded above).

### Phase 2: Automatic analysis

When you receive the window, **before responding**:

1. Read `src/main/webapp/content/css/myapp-standard.css` -- verify which reusable classes already exist to avoid duplication
2. Read the full HTML file of the target window
3. Read [css-reference.md](css-reference.md) for tokens and patterns
4. Determine the type of view and read the corresponding reference:
   - List/cards → `visitants-user-invited.html`
   - Form → `owner/owner-form.html`
   - Dashboard/detail → `house/house-administration.html`
   - Data table (CRUD) → `egress/egresses.html`
   - Table with search/report → `bitacora-acciones/bitacora-acciones.html` or `charge/billingReport.html`
5. If you need to verify classes from other global CSS, consult the files listed above
6. If the view has a controller, read it to verify whether `vm.isReady`, `vm.searching`, `$rootScope.mainTitle` exist
7. Determine the **view type**:
   - **Form/detail**: data on page load → use skeleton with `ng-if="!vm.isReady"`
   - **Card list**: data on load → card skeleton with `ng-if="!vm.isReady"`
   - **Search/report**: data on demand → skeleton ONLY when searching with `ng-if="!vm.isReady && vm.searching"`, do NOT put initial loader
8. **If it is a detail view** that receives the entity via state resolve: consider moving the load to the controller (`loadEntity` + `vm.isReady`) and put a skeleton in the template so the view doesn't get stuck until the server responds (see "Detail views – entity loading in controller" section).
9. **Skeleton:** The skeleton must **replicate the real structure** (same containers and classes: `bank-container`, `bank-container-title`, nested blocks, tree or list). Do not use generic blocks (see "Skeleton loaders – structure that replicates the view" section).
10. Analyze:
   - Which standard structure elements are missing (outer wrapper, loader, ng-cloak, fade-in)
   - Which existing utility classes could replace inline or custom styles
   - Which present components need adjustment (tables, forms, cards, modals, chips, filters)
   - If it already has inline `<style>`, what can be improved/aligned
   - Opportunities to add skeleton loaders if it only uses a spinner
   - Inline styles (`style="..."`) that should be scoped CSS classes
   - Hardcoded text that should use `translate`
   - Semantic HTML problems (`<th>` vs `<td>`, etc.)
11. **Required mobile analysis** (see "Mobile Standardization" section):
   - Does it have a functional mobile version or does it just look "compressed"?
   - CRUD tables: do they have mobile cards (Pattern 2) or only horizontal scroll?
   - Forms: do columns stack correctly with `layout-xs="column"`?
   - Filters/search: are they usable on mobile (full-width, stacked)?
   - Actions: are all desktop actions accessible on mobile?
   - Touch targets: clickable buttons and icons >= 44px on mobile?
   - Skeleton: is there a mobile skeleton in addition to the desktop one?
   - CSS breakpoints: does the inline `<style>` include `@media (max-width: 767px)` and `@media (max-width: 480px)`?
   - Modal dialogs: do they fit the mobile width?
12. **If the view contains tables**, additionally analyze (see "Table standardization" section):
   - Table classes: does it use `tableMaterialDesign` or a legacy/incorrect variant?
   - Thead: does it use `ad-table-header` or inline `style="background-color:..."`?
   - Actions: does it use `md-menu` with `more_vert` or legacy buttons (`btn-group`)?
   - Status: does it use `ad-badge-*` / `ad-status-*` or inline colors?
   - Monetary values: does it use `fMoney*()` with `text-right`?
   - Responsive: does it have `table-scrollable` or `hidden-xs` on columns? Does it need cards on mobile?
   - Skeleton: does it have a table skeleton or only a spinner?
   - Totals: does it use `<tfoot>` with `ad-table-totals-row`?
   - Pagination: does it use `jhi-item-count` + `uib-pager` correctly?
   - Export: does it have `id="tableToExport"` and `fMoneyExport()` if it supports export?

### Phase 3: Style Map (bullet points)

Present a short summary of the diagnosis:
- What is missing vs. the standard
- What will be added/changed
- Which existing classes will be reused
- Which new classes will be created (with domain prefix)
- **Mobile state**: what the view currently has on mobile and what will be added/improved (e.g., "CRUD table without mobile cards → mobile cards will be added with `hide-gt-sm`"). Indicate whether Pattern 2a (cards) or 2b (compact list) will be used and why.
- **Skeleton**: if a new skeleton is designed, indicate that it will replicate the real structure (blocks and classes). If it is a detail, indicate whether the load is moved to the controller.

### Phase 4: Apply changes

**Execution mode:** Apply changes directly to the files. Present the Style Map first as a summary, then execute.

#### What to apply:

**1. HTML template** -- edit the file directly:
- Add/adjust outer wrapper (`form-wrapper`, `ng-cloak`, `fade-in`) if missing
- Add `md-toolbar.form-title` with title if missing
- Add `md-content.form-content` with `layout-padding` if missing
- Replace `<loader>` with the appropriate skeleton loader; the skeleton must **replicate the structure** of the view (same blocks and classes, not generic blocks)
- In detail views that today resolve `entity` in the state: consider removing `entity` from resolve, loading it in the controller (`loadEntity` + `vm.isReady`) and showing a skeleton until the entity arrives
- Add `<no-content>` for empty states if missing
- Fix `<th>` vs `<td>`, hardcoded text via `translate`, missing `aria-label`
- Extract inline styles into CSS classes
- Add/update `<style>` block at the end of the file
- **Mobile required**: Add a functional mobile version according to view type:
  - CRUD tables → mobile cards with `hide-gt-sm` + desktop table with `hide-xs hide-sm`
  - Forms → verify `layout-xs="column"`, full-width buttons on mobile
  - Filters → stack on mobile with `layout-xs="column"`
  - Skeleton → include mobile skeleton (cards) in addition to desktop (table)
  - Actions → all desktop actions accessible on mobile (via `md-menu` in cards)

**2. CSS** -- where to apply:
- **Reusable classes** (badges, status, spacing, generic skeletons, value indicators) → `content/css/myapp-standard.css`
  - ALWAYS read this file first. If the class already exists, use it directly. DO NOT duplicate.
  - Add new classes in the corresponding section of the file (status, badges, skeleton, etc.)
- **View-specific styles** for a single view → inline `<style>` block at the end of the HTML

**CSS rules:**
- All new classes use the domain prefix: `[entity]-*` (e.g., `complaint-card`, `payment-skeleton-row`)
- Reuse existing global classes instead of redefining
- Include responsive with breakpoints `@media (max-width: 767px)` and `@media (max-width: 480px)`
- Include states: hover, focus visible, disabled where applicable
- ALWAYS include skeleton loader if the window loads asynchronous data
- Do not use `!important` except for Angular Material overrides (document why)
- Accessibility: visible focus, reasonable contrast, clickable areas >= 44px on mobile

**3. Controller (.js)** -- only if critical:
- Add `vm.isReady` / `vm.searching` if it doesn't exist and the view needs it
- In detail views: if the load is moved to the controller, implement `loadEntity()` (get id from `$stateParams`, decrypt if applicable, call the service, on success assign entity + `vm.isReady = true` + secondary loads, on error `vm.isReady = true` + toast) and stop injecting `entity`
- Add `$rootScope.mainTitle` if it uses `{{mainTitle}}` in toolbar
- Add `$rootScope.active` if missing

## Standardization checklist

When finishing, verify internally against this list:

### Structure
- [ ] Outer wrapper present (`form-wrapper`, `ng-cloak`, `fade-in`) -- or justify why it does not apply
- [ ] Toolbar with title (`form-title`)
- [ ] Content area (`form-content`)
- [ ] Correct loader/skeleton according to view type (page-load vs search); skeleton **replicates real structure** (same containers and classes)
- [ ] In detail with entity by resolve: considered moving the load to the controller and skeleton in template
- [ ] `<no-content>` for empty lists/results

### CSS
- [ ] `myapp-standard.css` reviewed before creating new classes (no duplication)
- [ ] Reusable classes added to `myapp-standard.css` (not inline)
- [ ] Existing utility classes reused (not reinvented)
- [ ] Inline styles (`style="..."`) extracted to CSS classes
- [ ] Project palette colors (not made up)
- [ ] Responsive (767px, 480px breakpoints)
- [ ] Skeleton uses the correct system: global `.skeleton` for tables, inline keyframe for custom cards
- [ ] No dark mode, no CSS variables, no global selectors without scope
- [ ] `!important` only for Angular Material overrides, documented

### Tables (if the view contains tables)
- [ ] Base classes: `table table-hover tableMaterialDesign` (or justified variant)
- [ ] Thead uses `ad-table-header` (no inline styles)
- [ ] `<th>` only in `<thead>`, `<td>` in `<tbody>` (correct semantics)
- [ ] Actions with `md-menu` + `more_vert` (2+ actions) or direct icons (1 action)
- [ ] `aria-label` on table action buttons
- [ ] Status badges use `ad-badge-*` or `ad-status-*`
- [ ] Monetary values with `text-right` and appropriate `fMoney*()`
- [ ] Positive/negative values with `ad-value-positive` / `ad-value-negative`
- [ ] `table-scrollable` wrapper with `border: 0 !important` if >6 columns
- [ ] `hidden-xs` on secondary columns
- [ ] Table skeleton (no spinner) with `.skeleton` spans
- [ ] Totals in `<tfoot>` with `ad-table-totals-row` (if applicable)
- [ ] `<no-content>` for empty table
- [ ] Cards on mobile (Pattern 2a) or compact list (Pattern 2b) according to table complexity

### Semantic HTML
- [ ] Correct use of `<th>` (only in `<thead>`) vs `<td>` (in `<tbody>`)
- [ ] User-facing text uses `| translate` or `data-translate` (not hardcoded)
- [ ] `<no-content>` uses `text-translation` (preferred) or `text` (acceptable)

### Mobile (REQUIRED)
- [ ] Functional and complete mobile view (not just "compressed")
- [ ] Data parity: mobile shows ONLY the data visible on desktop (no extra fields added)
- [ ] Tables with rich data use mobile cards Pattern 2a (`md-card` + `hide-gt-sm`) + desktop table (`hide-xs hide-sm`)
- [ ] Simple tables (<=3 cols) use compact list Pattern 2b (flex divs, no `md-card`) + desktop table
- [ ] Forms: columns stack on mobile (`layout-xs="column"`, `divFormsMDXS`)
- [ ] Action buttons are full-width on mobile (in `@media max-width: 767px`)
- [ ] Filters/search stack on mobile (`layout-xs="column"`)
- [ ] All desktop actions are accessible on mobile (via `md-menu` in cards or visible buttons)
- [ ] Mobile skeleton present (cards skeleton if the view uses cards on mobile)
- [ ] Navigation chips/tabs with horizontal scroll if there are many
- [ ] Responsive CSS includes `@media (max-width: 767px)` and `@media (max-width: 480px)`
- [ ] Modal dialogs adapt to 95vw on mobile
- [ ] Touch targets >= 44px on interactive elements
- [ ] Priority information visible without horizontal scroll on mobile

### Accessibility
- [ ] Visible focus on interactive elements
- [ ] Clickable areas >= 44px on mobile
- [ ] Color is not the only means of conveying information (add text/icon if only color is used for status)
- [ ] `aria-label` on icon-only buttons

## Quality rules

- **Reuse before creating.** Always check whether a global class already resolves the style.
- **Do not invent tokens.** Use only colors from the palette documented in css-reference.md.
- **Maintain consistency.** Buttons, inputs, selects, tables, badges and modals must look the same as in the rest of the project.
- **Minimum impact.** Do not break other screens; never use global selectors without scope.
- **If files or references are missing**, make clear assumptions and document them in the Style Map.
- **Do not invent data on mobile.** The mobile version MUST ONLY show data that was already visible on desktop. NEVER add extra fields (e.g., extension, status, creation date) that were not shown in the original desktop table or view. If the desktop table shows "Subsidiary" and "Action", the mobile card shows exactly that. The mobile version is a layout change, not a content change.
- **Prefer compact lists over `md-card` on mobile.** For simple tables (<=3 columns, basic actions), DO NOT use `<md-card>` which adds excessive margins and padding. Use divs with flex layout inside a single bordered container. Reserve `<md-card>` only for views with rich data (badges, subtitles, amounts, multiple actions).
- **Skeleton that fits.** The skeleton must use the same container classes and hierarchy as the real view (e.g., `bank-container`, `bank-container-title`, nested blocks), not generic boxes, so that when content is swapped in there is no layout jump.

## Output format

```
1. Style Map (short bullet points of the diagnosis and what will be done)
2. Apply changes directly:
   a. Edit HTML template (structure, skeleton, semantics, i18n)
   b. Add/update inline <style> (or custom.css if reusable)
   c. Edit controller .js (only if critical)
3. Checklist (confirmation of items met)
4. Summary of modified files
```
