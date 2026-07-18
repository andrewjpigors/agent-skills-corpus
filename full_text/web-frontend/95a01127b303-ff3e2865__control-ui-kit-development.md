---
name: control-ui-kit-development
description: Build and work with Control UI Kit Blade components — form fields, inputs, tables, buttons, panels, modals, tabs, alerts, charts, maps, icons, and theming.
---

# Control UI Kit Development

## When to use this skill

Use this skill when working with the `control-ui-kit/control-ui-kit` package: building forms, rendering tables, using UI components (alerts, panels, modals, buttons, tabs), rendering Chart.js charts, adding maps, styling with the theme system, or adding/modifying components in this library.

---

## Overview

Control UI Kit is a Laravel Blade component library providing ~180 components across 18 categories. Components are registered via `config/control-ui-kit.php` and styled via `config/themes/default.php`. All component styles use Tailwind CSS class strings.

**Installation:**
```bash
composer require control-ui-kit/control-ui-kit
```

**Asset loading (in layout):**
```blade
@controlUiKitAssets
```

---

## Architecture

### Three-layer form system

Every interactive form element has three layers:

| Layer | Prefix | Example | Purpose |
|---|---|---|---|
| **Field** | `field-*` | `x-field-text` | Label + layout + validation error |
| **Input** | `input-*` | `x-input-text` | Raw HTML input element |
| **Layout** | `form-layout-*` | `form-layout-responsive` | Label/input arrangement |

Always use `x-field-*` components in views. Use `x-input-*` only when embedding a raw input without label/layout.

### Trait architecture

- `UseThemeFile` — `style()` and `setConfigStyles()` for reading `config/themes/default.php`
- `UseInputTheme` — `setInputStyles()` for input-specific theming
- `LivewireAttributes` — wires up `wire:model`, `wire:key`, etc. transparently

### Component registration

All aliases are in `config/control-ui-kit.php` under `'components'`. To override a component, publish the config and swap the class:

```bash
php artisan vendor:publish --tag=control-ui-kit-config
```

---

## Form Fields (`x-field-*`)

Field components wrap an input with a label, optional help text, and validation error display. They extend `InputField` which provides `name`, `label`, `help`, `value`, and `layout` properties.

### Layout options

Pass `layout="stacked"`, `layout="inline"`, or `layout="responsive"` (default) to any field:

```blade
<x-field-text name="title" label="Title" layout="stacked" />
<x-field-text name="title" label="Title" layout="inline" />
<x-field-text name="title" label="Title" />  {{-- responsive (default) --}}
```

Change the default globally in `config/control-ui-kit.php`:
```php
'field-layouts' => ['default' => 'stacked'],
```

### Full field reference

| Blade tag | Description | Key extra props |
|---|---|---|
| `x-field-text` | Text input | — |
| `x-field-email` | Email input | — |
| `x-field-url` | URL input | — |
| `x-field-password` | Password with reveal toggle | — |
| `x-field-textarea` | Multi-line text | — |
| `x-field-search` | Search input | `clear-url`, `clear-icon` |
| `x-field-number` | Integer input | `min`, `max`, `step` |
| `x-field-decimal` | Decimal input | `decimals` |
| `x-field-currency` | Currency input | `symbol` |
| `x-field-percent` | Percentage (0–100) | — |
| `x-field-royalty` | Royalty/rate input | — |
| `x-field-select` | Dropdown | `options`, `placeholder` |
| `x-field-radio-group` | Radio button group | `options` |
| `x-field-checkbox` | Checkbox | — |
| `x-field-tags` | Multi-tag input | — |
| `x-field-toggle` | Toggle switch | — |
| `x-field-date` | Date picker (flatpickr) | `min-date`, `max-date` |
| `x-field-datetime` | Date + time picker | — |
| `x-field-date-range` | Date range picker | — |
| `x-field-time` | Time picker | — |
| `x-field-color-picker` | Colour picker | — |
| `x-field-autocomplete` | AJAX autocomplete | `url`, `min-length` |
| `x-field-file-upload` | File upload | `accept` |
| `x-field-image-upload` | Image upload with preview | `accept` |
| `x-field-otc` | One-time code (6-digit) | `digits` |
| `x-field-range` | Range slider | `min`, `max`, `step` |
| `x-field-info` | Read-only display field | — |
| `x-field-link` | Read-only link display | `href` |
| `x-field-slot` | Custom slot-based field | — |
| `x-field-input` | Base field (rarely used directly) | — |

### Common field props

```blade
<x-field-text
    name="username"           {{-- form field name (required) --}}
    label="Username"          {{-- label text --}}
    value="john"              {{-- initial value --}}
    help="No spaces allowed"  {{-- help text below label --}}
    layout="stacked"          {{-- inline | stacked | responsive --}}
    required                  {{-- shows required indicator --}}
/>
```

### Info and Link fields (read-only)

```blade
{{-- Display plain text --}}
<x-field-info name="status" label="Status" value="Active" />
<x-field-info name="status" label="Status">Active</x-field-info>

{{-- Display a hyperlink --}}
<x-field-link name="site" label="Website" href="https://example.com" value="Visit Site" />
<x-field-link name="site" label="Website" href="https://example.com" target="_blank">Visit Site</x-field-link>
```

### Select field

```blade
<x-field-select
    name="country"
    label="Country"
    :options="$countries"      {{-- array or Collection: [id => label] or [['id' => ..., 'text' => ...]] --}}
    placeholder="Select one"
    value="{{ $record->country }}"
/>
```

### Checkbox / Toggle

```blade
<x-field-checkbox name="agree" label="I agree" value="1" :checked="$user->agreed" />
<x-field-toggle name="active" label="Active" :checked="$record->active" />
```

### Livewire integration

Field components pass through all `wire:*` attributes transparently:

```blade
<x-field-text name="search" label="Search" wire:model.live="search" />
<x-field-select name="status" label="Status" :options="$statuses" wire:model="status" />
```

---

## Standalone Inputs (`x-input-*`)

Use input components without label/layout — e.g. inside a custom slot or `x-field-slot`:

```blade
<x-field-slot name="custom" label="Custom">
    <x-input-text name="custom" value="{{ $value }}" />
</x-field-slot>

{{-- Hidden input --}}
<x-input-hidden name="user_id" :value="auth()->id()" />
```

### Input base props (all inputs)

| Prop | Type | Description |
|---|---|---|
| `name` | string | Input `name` attribute (required) |
| `id` | string | Input `id` (defaults to `name`) |
| `value` | string | Current value |
| `placeholder` | string | Placeholder text |
| `type` | string | HTML input type override |
| `min` / `max` / `step` | numeric | Numeric constraints |
| `icon-left` / `icon-right` | string | Icon component name |
| `prefix-text` / `suffix-text` | string | Wrapper text |
| `required-input` | bool | Native required attribute |

### Search input clear button (`x-input-search` / `x-field-search`)

The search input can render a clickable clear (✕) icon that links to a route. Pass `clear-url`:

```blade
{{-- Standalone --}}
<x-input-search name="search" :value="request('search')" :clear-url="route('users.index')" />

{{-- As a field --}}
<x-field-search name="search" label="Search" :value="request('search')" :clear-url="route('users.index')" />
```

Behaviour:

- The clear icon **only appears when the input has a value** (the server-rendered `value` / `old()`), so it shows once a search term is present.
- Clicking it navigates to `clear-url` — typically the index route without the query string, resetting the search.
- The clear icon renders **before** the `icon-right` block, so a search can have both a clear link and a right icon.

The clear icon has its own themeable style region — override per-instance or via the `input-search` theme section:

| Prop | Config key | Default | Description |
|---|---|---|---|
| `clear-icon` | `input-search.clear-icon` | `icon-close` | Icon component used for the clear button |
| `clear-color` | `input-search.clear-color` | `text-muted` | Icon colour |
| `clear-background` | `input-search.clear-background` | `''` | Background |
| `clear-border` | `input-search.clear-border` | `border-l border-input` | Border |
| `clear-size` | `input-search.clear-size` | `w-4 h-4` | Icon size |
| `clear-other` | `input-search.clear-other` | `flex items-center justify-center self-stretch w-10` | Layout/other classes |
| `clear-padding` | `input-search.clear-padding` | `px-2.5` | Padding |
| `clear-rounded` | `input-search.clear-rounded` | `''` | Border radius |
| `clear-shadow` | `input-search.clear-shadow` | `''` | Shadow |

```blade
{{-- Custom clear icon and colour --}}
<x-input-search name="search" :value="request('search')"
    :clear-url="route('users.index')" clear-icon="icon-trash" clear-color="text-red-500" />
```

> The clear link is a plain `<a href>` (full-page navigation). For a live client-side toggle while typing, add an Alpine binding.

---

## Theming & Styling

All styles come from `config/themes/default.php`. Every component reads its defaults from a keyed section matching its component name.

### How styles resolve

```
config('themes.default.input.background')  →  'bg-input'
config('themes.default.button.default.color')  →  'text-button-default hover:text-button-default-hover'
```

### Overriding styles per-instance

Pass any style parameter directly on the component. They override the theme default:

```blade
{{-- Override a single style --}}
<x-field-text name="code" label="Code" color="text-red-600" />
<x-button brand padding="px-6 py-3">Save</x-button>
<x-alert danger background="bg-red-50 border border-red-200">Warning!</x-alert>
```

### Common style props available on most components

`background`, `border`, `color`, `font`, `other`, `padding`, `rounded`, `shadow`, `width`

### Overriding theme globally

Publish the theme file and edit:

```bash
php artisan vendor:publish --tag=control-ui-kit-theme
```

This copies `config/themes/default.php` to your app's config directory.

---

## Button (`x-button`)

```blade
{{-- Style variants (boolean flags) --}}
<x-button default>Default</x-button>
<x-button brand>Save</x-button>
<x-button danger>Delete</x-button>
<x-button info>Info</x-button>
<x-button success>Done</x-button>
<x-button warning>Caution</x-button>
<x-button muted>Cancel</x-button>

{{-- As a link --}}
<x-button brand href="/dashboard">Go to Dashboard</x-button>

{{-- With icon --}}
<x-button brand icon="icon-save">Save Record</x-button>

{{-- Form submit with single-click prevention --}}
<x-button brand type="submit" :single-click="true">Submit</x-button>

{{-- Disabled --}}
<x-button brand disabled>Unavailable</x-button>
```

Key props: `href` (renders `<a>` instead of `<button>`), `icon`, `type` (submit/button/reset), `single-click`, `text` (alternative to slot).

---

## Button Group (`x-button-group`, `x-button-group-item`)

A connected row of buttons that share a single visual border — used for mutually exclusive option selectors (e.g. metric switchers, date range toggles).

```blade
<x-button-group>
    <x-button-group-item first active text="Years" />
    <x-button-group-item text="Months" />
    <x-button-group-item last text="Days" />
</x-button-group>
```

### Position props

| Prop | Effect |
|---|---|
| `first` | Applies left-only rounding (`rounded-l-sm rounded-r-none`) |
| `last` | Applies right-only rounding (`rounded-l-none rounded-r-sm`) |
| `first` + `last` | Standalone button — uses base `rounded` |
| neither | Middle item — `rounded-none` |

The `x-button-group` wrapper uses `isolate inline-flex` so adjacent `ring-1 ring-inset` borders collapse into a single 1 px line. Non-first items automatically receive `-ml-px` to prevent double borders.

### Style variants

Same boolean variant flags as `x-button`:

```blade
<x-button-group>
    <x-button-group-item first brand text="Brand" />
    <x-button-group-item brand text="Brand" />
    <x-button-group-item last brand text="Brand" />
</x-button-group>
```

Available variants: `default` (default), `brand`, `danger`, `info`, `success`, `warning`, `muted`, `link`.

### Active (selected) state

```blade
<x-button-group-item first active text="Streams" />
```

`active` applies variant-specific active background and ring classes (`bg-button-{variant}-active`, `ring-button-{variant}-active`) which use `!important` to persist through hover. Also adds `aria-pressed="true"` for accessibility.

### Responsive wrap

Pass `wrap` to apply a breakpoint-specific wrapping class on the container:

```blade
<x-button-group wrap="md">
    ...
</x-button-group>
```

This adds `btn-grp-{wrap}` (e.g. `btn-grp-md`) to the wrapper `<div>`, letting your CSS wrap the group at that breakpoint. Default is no wrapping.

### Additional props

| Prop | Description |
|---|---|
| `text` | Button label (alternative to slot) |
| `trans` | Laravel translation key — resolved via `trans()` and used as label text |
| `href` | Renders an `<a>` instead of `<button>` |
| `disabled` | Disables the button; strips `href` if present |
| `icon` | Icon component name (e.g. `icon-audio-stream`) |
| `rounded` | Override the position-computed rounding |
| `margin` | Override the default `-ml-px` negative margin |

### Theme config keys

`button-group` controls the wrapper (`other`, `rounded`, `shadow`, `wrap`); `button-group-item` controls each item. Per-variant sub-keys (`default`, `brand`, etc.) each have `background`, `border`, `color`, `icon`, and `active` keys.

---

## Alert (`x-alert`)

```blade
<x-alert default title="Note" text="Something happened." />
<x-alert brand title="Welcome" text="Signed in successfully." />
<x-alert danger title="Error" text="Something went wrong." />
<x-alert info title="Tip">Use keyboard shortcuts for faster navigation.</x-alert>
<x-alert success title="Saved">Your changes have been saved.</x-alert>
<x-alert warning title="Warning" text="This action cannot be undone." />
<x-alert muted title="Note" text="This feature is deprecated." />

{{-- With multiple URLs --}}
<x-alert info title="Learn more" :urls="[['url' => '/docs', 'text' => 'Documentation'], ['url' => '/help', 'text' => 'Help']]" />

{{-- Size variants --}}
<x-alert danger tiny title="Small alert" />
<x-alert danger small title="Small alert" />
<x-alert danger medium title="Medium alert" />   {{-- default --}}
<x-alert danger large title="Large alert" />
```

---

## Panel (`x-panel`)

```blade
<x-panel>
    <x-panel-header>Panel Title</x-panel-header>

    <x-panel-section>
        Content goes here
    </x-panel-section>

    <x-panel-divider />

    <x-panel-section>
        More content
    </x-panel-section>

    <x-panel-footer>
        <x-button brand>Save</x-button>
    </x-panel-footer>
</x-panel>
```

---

## Modal (`x-modal`)

```blade
{{-- Trigger button --}}
<x-button brand @click="$dispatch('open-modal', 'my-modal')">Open</x-button>

{{-- Modal --}}
<x-modal name="my-modal" title="Confirm Action">
    <p>Are you sure?</p>
    <x-slot:footer>
        <x-button brand @click="$dispatch('close-modal', 'my-modal')">Confirm</x-button>
        <x-button muted @click="$dispatch('close-modal', 'my-modal')">Cancel</x-button>
    </x-slot:footer>
</x-modal>

{{-- Confirmation dialog shorthand --}}
<x-modal-confirmation name="delete-confirm" title="Delete record?" />
```

---

## Tabs (`x-tabs`)

```blade
<x-tabs>
    <x-tabs-heading name="details" label="Details" active />
    <x-tabs-heading name="history" label="History" />

    <x-tabs-panel name="details">
        Details content here
    </x-tabs-panel>

    <x-tabs-panel name="history">
        History content here
    </x-tabs-panel>
</x-tabs>
```

### Dynamic component in a tab panel

`x-tabs-panel` can render a registered control-ui-kit component dynamically, with optional data injection:

```blade
{{-- Render a registered component in the panel (no data) --}}
<x-tabs-panel name="chart" component="line-chart" />

{{-- Render with data — component is instantiated with named args --}}
<x-tabs-panel
    name="chart"
    component="line-chart"
    :component-data="['id' => 'my_chart', 'datasets' => $datasets, 'labels' => $labels]"
/>
```

`component` must match a key in `config/control-ui-kit.php` under `'components'`. The `component-data` array is spread as named constructor arguments using PHP 8's named argument spread (`new $class(...$componentData)`).

---

## Charts

All chart components require Chart.js to be loaded. Use `@controlUiKitAssets` in your layout.

### Modern dataset API (Line, Column, Bar, Combo, Stacked)

These five charts share the same core API:

| Prop | Type | Description |
|---|---|---|
| `id` | string | Required. Canvas element id and JS `window.{id}` variable |
| `:datasets` | array | Array of dataset objects (see below) |
| `:labels` | array | X-axis labels |
| `x-axis-type` | `'category'`\|`'time'` | Default: `'category'` |
| `x-axis-min-unit` | string | e.g. `'day'`, `'month'` — only used when `x-axis-type="time"` |
| `animation` | `'true'`\|`'false'` | Default: `'true'` |
| `animation-duration` | string | Milliseconds (from theme config) |
| `animation-easing` | string | e.g. `'easeInOutQuart'` |
| `point-radius` | string | Point dot size (from theme config) |
| `hide-grid` | `'true'`\|`'false'` | Hide Y gridlines. Default: `'false'` |
| `hide-x-grid` | `'true'`\|`'false'` | Hide X gridlines. Default: `'true'` |

**Dataset object keys:**

| Key | Description |
|---|---|
| `label` | Legend label string |
| `data` | Array of values |
| `color` | CSS variable string e.g. `'--chart-500'` (falls back to theme palette) |
| `gradientStops` | Array of `['t' => 0.0..1.0, 'cssVar' => '--chart-xxx']` for per-bar/per-point gradient |
| `order` | Chart.js dataset order for layering |

### Line chart (`x-line-chart`)

```blade
<x-line-chart
    id="streams_chart"
    :datasets="[
        ['label' => 'Streams', 'data' => [100, 200, 150, 300], 'color' => '--chart-500'],
        ['label' => 'Downloads', 'data' => [40, 80, 60, 120]],
    ]"
    :labels="['Jan', 'Feb', 'Mar', 'Apr']"
/>

{{-- Time-series with min unit --}}
<x-line-chart
    id="daily_chart"
    x-axis-type="time"
    x-axis-min-unit="day"
    :datasets="[['label' => 'Plays', 'data' => $plays]]"
    :labels="$dates"
/>
```

Line datasets also support:
- `radius` — per-dataset point radius override
- `hoverRadius` — per-dataset hover radius override
- `dashed` — `true` to render a dashed line

### Column chart (`x-column-chart`)

Vertical bar chart. Supports all modern API props including `x-axis-type` time/category and per-bar `gradientStops`.

```blade
<x-column-chart
    id="monthly_sales"
    :datasets="[
        ['label' => 'Revenue', 'data' => [5000, 7200, 6100], 'color' => '--chart-400'],
    ]"
    :labels="['Jan', 'Feb', 'Mar']"
/>

{{-- With per-bar gradient --}}
<x-column-chart
    id="gradient_col"
    :datasets="[
        [
            'label' => 'Streams',
            'data' => [100, 200, 150],
            'gradientStops' => [
                ['t' => 0.0, 'cssVar' => '--chart-100'],
                ['t' => 1.0, 'cssVar' => '--chart-600'],
            ],
        ],
    ]"
    :labels="['Jan', 'Feb', 'Mar']"
/>
```

### Bar chart (`x-bar-chart`)

Horizontal bar chart (`indexAxis: y`). Same API as column chart but no time-axis support. The X axis is always `type: linear`.

```blade
<x-bar-chart
    id="top_tracks"
    :datasets="[
        ['label' => 'Streams', 'data' => [500, 320, 210], 'color' => '--chart-500'],
    ]"
    :labels="['Track A', 'Track B', 'Track C']"
/>
```

### Combo chart (`x-combo-chart`)

Mixed bar + line chart. Each dataset can independently be `'bar'` (default) or `'line'` type. Supports an optional second Y axis for the line series.

```blade
<x-combo-chart
    id="combo"
    :datasets="[
        ['label' => 'Revenue', 'data' => [500, 700, 600], 'type' => 'bar', 'yAxisID' => 'y'],
        ['label' => 'Growth %', 'data' => [10, 40, 20], 'type' => 'line', 'yAxisID' => 'y1'],
    ]"
    :labels="['Jan', 'Feb', 'Mar']"
    show-second-axis="true"
    y1-axis-label="Growth %"
/>
```

**Combo-specific props:**

| Prop | Description |
|---|---|
| `show-second-axis` | `'true'` to render a right-hand Y axis (`y1`) |
| `y1-axis-label` | Label text for the right axis |

**Per-dataset keys specific to combo:**

| Key | Description |
|---|---|
| `type` | `'bar'` (default) or `'line'` |
| `yAxisID` | `'y'` or `'y1'` to assign dataset to an axis |

### Stacked chart (`x-stacked-chart`)

Stacked bar chart. Sets `stacked: true` on both x and y axes. Supports a `stack` key per dataset to group datasets into independent stacks.

```blade
<x-stacked-chart
    id="stacked"
    :datasets="[
        ['label' => 'Physical', 'data' => [100, 120, 90], 'stack' => 'sales'],
        ['label' => 'Digital', 'data' => [200, 180, 220], 'stack' => 'sales'],
        ['label' => 'Returns', 'data' => [10, 15, 8], 'stack' => 'returns'],
    ]"
    :labels="['Jan', 'Feb', 'Mar']"
/>
```

Orientation defaults to vertical (stacked columns). Pass `index-axis="y"` for a **horizontal** stacked bar chart (bars stack left-to-right); any other value falls back to `"x"`.

```blade
<x-stacked-chart id="stacked" index-axis="y" :datasets="$datasets" :labels="$labels" />
```

### Donut chart (`x-donut-chart`)

Pass data as a label-keyed array of numeric values:

```blade
<x-donut-chart
    id="format_split"
    :data="['Streaming' => 65, 'Download' => 25, 'Physical' => 10]"
    :colors="['--chart-500', '--chart-300', '--chart-100']"
/>
```

Alternatively use separate `:values` and `:labels` arrays:

```blade
<x-donut-chart
    id="format_split"
    :values="[65, 25, 10]"
    :labels="['Streaming', 'Download', 'Physical']"
/>
```

Key props: `id`, `:data` (label-keyed value array), `:values` + `:labels` (alternative to `:data`), `:colors`, `cutout` (percentage string, default from config).

**Responsive cutout.** The `cutout` value can be varied per breakpoint using Tailwind-style prefixed attributes (`sm:`, `md:`, `lg:`, `xl:`, `2xl:`). It is mobile-first: `cutout` is the base value and each `{breakpoint}:cutout` overrides it at that screen width and up. The chart picks the largest matching breakpoint on load and re-evaluates on window resize.

```blade
<x-donut-chart
    id="format_split"
    :data="['Streaming' => 65, 'Download' => 25, 'Physical' => 10]"
    cutout="80%"
    sm:cutout="78%"
    md:cutout="75%"
    lg:cutout="72%"
    xl:cutout="70%"
    2xl:cutout="68%"
/>
```

Breakpoint widths follow Tailwind defaults: `sm` 640px, `md` 768px, `lg` 1024px, `xl` 1280px, `2xl` 1536px. This is donut-only (pie has no cutout). Implementation note: these colon-prefixed attributes are not constructor params — `Donut::withAttributes()` reads them from the attribute bag and pushes the resolved map onto the chart, which the shared `charts/chart.blade.php` template applies client-side.

### Legend segment toggling (pie & donut)

Clicking a legend entry hides/shows that segment — this is Chart.js's built-in behaviour and works out of the box (the components don't override `legend.onClick`). External custom legends carrying `data-chart="{id}"` + `data-index` are also wired for click-to-toggle (dim + line-through on the hidden row) and hover highlighting via the shared template.

### Pie chart (`x-pie-chart`)

Same API as donut chart without the `cutout` prop (and no responsive cutout):

```blade
<x-pie-chart
    id="genre_split"
    :data="['Pop' => 40, 'Rock' => 35, 'Electronic' => 25]"
    :colors="['--chart-500', '--chart-400', '--chart-200']"
/>
```

### Gauge chart (`x-gauge-chart`)

Single-metric gauge: a full-circle doughnut ring where the filled arc is `value` out of `max`,
the remainder is a muted track, and the value is drawn in the centre. Styled identically to the
donut (fonts, tooltip, animation, segment border) — it reuses the same `chart.blade.php` pipeline.

```blade
<x-gauge-chart id="uptime" value="72" suffix="%" label="Uptime" />

{{-- value out of a custom max, custom colours --}}
<x-gauge-chart id="storage" value="18" max="32" display="18 GB" value-color="--chart-300" track-color="--chart-grid" />
```

Key props: `id`, `value` (number), `max` (default `100`), `suffix` (appended to the centre value,
e.g. `%`), `label` (small caption drawn beneath the value), `display` (override the centre text
entirely), `value-color` / `track-color` (CSS vars, default `--chart-100` / `--chart-grid`),
`cutout` (default `75%`). It is a **complete circle**, not a semicircle gauge. Legend and tooltip
The built-in legend is hidden by default (`legend-display` to show it). Tooltips behave exactly
like the donut/pie charts — enabled and themed identically, and driven by external legends
(`data-chart="{id}"` + `data-index`) for hover-highlight and click-to-toggle; set
`tooltip-enabled="false"` to turn them off. All other donut legend/title/tooltip/animation props are also accepted. The centre text is drawn by a small inline
Chart.js plugin; centre styling is themeable via `charts.gauge.center`. The value and label font
sizes are **Tailwind text-size classes** (`size` default `text-3xl`, `label-size` default `text-sm`) —
overridable per instance with `center-size` / `center-label-size` — resolved to pixels at draw time.
Other centre keys: `color`, `family`, `weight`.

### Matrix chart (`x-matrix-chart`)

Heatmap / calendar-style intensity grid. Each data point has `x`, `y`, and `count` values. Cell color intensity scales from the maximum count.

```blade
<x-matrix-chart
    id="activity_grid"
    :data="$activityData"   {{-- array of ['x' => ..., 'y' => ..., 'count' => ...] --}}
    color="--chart-500"
    label="Activity"
/>
```

Key props: `id`, `:data`, `color` (CSS variable), `label`, `x-margin`, `y-margin`, `y-reverse`, `x-label-visible`, `y-label-visible`.

### Change / KPI chart (`x-change-chart`)

Displays a metric tile with current value, comparison to previous value, and an up/down indicator. The wrapper uses `flex flex-col` by default so the `link` is pinned to the bottom of the card — useful when cards of different heights appear in a grid row.

```blade
{{-- Basic usage --}}
<x-change-chart
    title="Monthly Streams"
    :current="125400"
    :previous="98200"
    :decimals="0"
    link="/reports/streams"
    link-text="View report"
    icon="icon-music-note"
/>

{{-- With image instead of icon --}}
<x-change-chart
    title="Top Artist"
    :current="980"
    :previous="850"
    image="/images/artist.jpg"
    image-alt="Artist photo"
    link="/reports/artist"
    link-text="View"
/>

{{-- Show absolute difference instead of percentage --}}
<x-change-chart
    title="New Signups"
    :current="340"
    :previous="290"
    percent-difference="false"
    hide-difference-icon="true"
/>

{{-- Reverse the direction: down is good (uses increase-color), up is bad (uses decrease-color) --}}
<x-change-chart
    title="Churn Rate"
    :current="4.2"
    :previous="5.8"
    reverse="true"
/>
```

| Prop | Type | Description |
|---|---|---|
| `title` | string | Card heading (required) |
| `current` | float | Current value |
| `previous` | float | Previous value for comparison |
| `decimals` | int | Decimal places for the difference display |
| `link` | string | URL for the bottom link |
| `link-text` | string | Text for the bottom link |
| `icon` | string | Icon component name (e.g. `icon-music-note`) |
| `image` | string | Image URL (replaces icon; fills left third of card) |
| `image-alt` | string | Alt text for the image |
| `image-style` | string | Custom CSS class string that overrides all image style props |
| `percent-difference` | `'true'`\|`'false'` | Show percentage diff (default: `'true'`); set `'false'` for absolute |
| `hide-difference-icon` | `'true'`\|`'false'` | Hide the up/down trend icon next to the diff value |
| `reverse` | `'true'`\|`'false'` | Reverse which direction is positive: a down number uses `increase-color`, an up number uses `decrease-color` (default: `'false'`). Sign and trend icon still follow actual movement |
| `increase-icon` | string | Icon for positive change (overrides theme default) |
| `decrease-icon` | string | Icon for negative change (overrides theme default) |

### Common chart props (axis & legend fine-tuning)

All modern API charts (Line, Column, Bar, Combo, Stacked) support these additional fine-tuning props:

```blade
<x-line-chart
    id="my_chart"
    :datasets="$datasets"
    :labels="$labels"

    {{-- Legend --}}
    legend-display="true"
    legend-position="top"     {{-- top | bottom | left | right --}}
    legend-align="center"     {{-- start | center | end --}}

    {{-- Title --}}
    title="Chart Title"
    title-display="true"

    {{-- X axis ticks --}}
    x-axis-label="Month"
    x-tick-color="--color-muted"

    {{-- Y axis ticks --}}
    y-axis-label="Count"
    y-tick-color="--color-muted"

    {{-- Grid --}}
    grid-color="--color-border"
    hide-grid="false"
    hide-x-grid="true"
/>
```

### Chart color palette

The default color palette is defined in `config/themes/default.php` under `charts.defaults.colors` as an array of CSS variable names (`'--chart-100'`, `'--chart-200'`, etc.). Datasets cycle through this palette if no `color` is specified.

### Tooltip intersect (per chart type)

Chart.js's `tooltip.intersect` option controls whether the tooltip requires the cursor to be visually inside a chart element before it shows. The default is **split per chart type** so each chart can ship with the right behaviour out of the box:

| Chart | Config key | Default |
|---|---|---|
| Pie | `charts.pie.tooltip-intersect` | `true` |
| Donut | `charts.donut.tooltip-intersect` | `true` |
| Gauge | `charts.gauge.tooltip-intersect` | `true` |
| Bar | `charts.bar.tooltip-intersect` | `false` |
| Line | `charts.line.tooltip-intersect` | `false` |
| Column | `charts.column.tooltip-intersect` | `false` |
| Stacked | `charts.stacked.tooltip-intersect` | `false` |
| Combo | `charts.combo.tooltip-intersect` | `false` |

`true` is the right default for pie/donut — `mode: 'nearest'` + `intersect: false` on a circular chart can highlight a segment whose anchor is nearest the cursor rather than the one the cursor is actually over, producing wrong-segment tooltips. `false` is friendlier for bar/line where users expect the nearest data point to highlight without needing pixel-perfect hover.

Override per instance with the `:tooltip-intersect` prop (note the leading colon — `strict_types=1` rejects bare string attributes against the `?bool` parameter):

```blade
<x-donut-chart id="d1" :data="$data" :tooltip-intersect="false" />
<x-line-chart id="l1" :datasets="$ds" :labels="$lb" :tooltip-intersect="true" />
```

---

## Maps

### World map choropleth (`x-world-map-chart`)

Renders an SVG choropleth (heat map) of the world. Countries are coloured by value intensity using CSS variable colour interpolation — fully integrated with the theming system.

**Library stack:** D3-geo (ISC) + TopoJSON client (ISC) + Natural Earth 110m data (public domain). No Highcharts dependency.

| Prop | Type | Default | Description |
|---|---|---|---|
| `id` | string | required | SVG element ID |
| `data` | array | `[]` | ISO-A2 → value map. Each value is either a number, or `['value' => 1200, 'id' => 42]` to also attach an `id` for use in links. e.g. `['GB' => ['value' => 1200, 'id' => 42], 'US' => 5000]` |
| `projection` | string | `'natural-earth'` | `natural-earth` \| `mercator` \| `equal-earth` |
| `show-tooltip` | string | `'true'` | Show country name + value on hover |
| `number-format` | string | `''` | Max decimal places for tooltip value |
| `url` | string | `''` | When set, every country becomes clickable and navigates to this URL. Supports `{id}`, `{iso}`, `{name}` and `{value}` placeholders (each URL-encoded from the clicked country) |
| `url-target` | string | `'_self'` | Where the clicked URL opens, like an `<a target>` — `_self`, `_blank`, etc. Default set in the `world-map-chart` theme section |

**Style props** (all override the `world-map-chart` theme section):

| Prop | Default CSS var | Description |
|---|---|---|
| `min-color` | `--chart-100` | Country fill at minimum/zero value |
| `max-color` | `--chart-500` | Country fill at maximum value |
| `no-data-color` | `--color-border` | Fill for countries absent from data |
| `border-color` | `--color-panel` | Country border stroke colour |
| `border-width` | `0.5` | Stroke width in SVG user units |
| `background-color` | `--color-panel` | SVG background (ocean) colour |
| `tooltip-background` | `--color-panel` | Tooltip background CSS var |
| `tooltip-color` | `--color-panel-text` | Tooltip text CSS var |
| `tooltip-font` | `text-xs` | Tailwind font classes for tooltip |
| `tooltip-padding` | `px-2 py-1` | Tailwind padding classes for tooltip |
| `tooltip-rounded` | `rounded` | Tailwind border-radius for tooltip |
| `url-target` | `_self` | Default link target for clickable countries (overridable per-instance via the `url-target` prop) |
| `width` | `w-full` | Tailwind width of wrapper div |
| `height` | `h-auto` | Tailwind height of wrapper div |

**Basic usage:**

```blade
<x-world-map-chart
    id="sales_map"
    :data="['GB' => 12400, 'US' => 98000, 'DE' => 8300, 'FR' => 7100, 'AU' => 5400]"
/>
```

**Custom colours and projection:**

```blade
<x-world-map-chart
    id="plays_map"
    :data="$countryPlays"
    projection="mercator"
    min-color="--chart-100"
    max-color="--chart-700"
    no-data-color="--color-muted"
/>
```

**Clickable countries:**

Pass a `url` to make every country a clickable link. Use placeholders to build a per-country
destination — `{id}` (from the dataset entry's `id`), `{iso}` (ISO-A2 code), `{name}` (country
name) and `{value}` (its value). Each is URL-encoded at click time. Use `url-target="_blank"` to
open in a new window. Clicks behave like a real `<a>`: the click is dispatched onto a native
anchor carrying the event's keyboard modifiers, so Cmd/Ctrl+Click opens a new tab and Shift+Click
a new window (honouring the browser's own behaviour) regardless of `url-target`.

```blade
<x-world-map-chart
    id="reports_map"
    :data="['GB' => ['value' => 12400, 'id' => 42], 'US' => ['value' => 98000, 'id' => 17]]"
    url="/reports/country/{id}/{iso}"
    url-target="_blank"
/>
```

**Data format:** ISO 3166-1 alpha-2 country codes as keys. Each value is either a number, or an
array `['value' => 1200, 'id' => 42]` where `value` drives the choropleth shading and `id` is
available to the `url` via the `{id}` placeholder (the array form is only needed when you want an
`id` in links; a plain number still works everywhere). Countries not present in the array are shown
in `no-data-color`. The maximum value in the data set maps to `max-color`; zero/minimum maps to
`min-color`.

---

## Markdown (`x-markdown`, `x-toc`)

Renders Markdown content as HTML:

```blade
<x-markdown>
# Hello World

This is **rendered** markdown content.
</x-markdown>

{{-- From a variable --}}
<x-markdown>{{ $article->body }}</x-markdown>
```

Table of contents from a markdown string:

```blade
<x-toc>{{ $article->body }}</x-toc>
```

---

## Table (`x-table`)

```blade
<x-table
    :search="$search"
    :order-by="$orderBy"
    :sort="$sort"
    :active-filters="$activeFilters"
>
    <x-slot:filters>
        <x-table-filter name="status" label="Status" :options="$statuses" :value="$filterStatus" />
    </x-slot:filters>

    <x-slot:headings>
        <x-table-heading name="name" label="Name" sortable :order-by="$orderBy" :sort="$sort" />
        <x-table-heading name="email" label="Email" />
        <x-table-heading name="actions" label="" />
    </x-slot:headings>

    @foreach ($users as $user)
        <x-table-row>
            <x-table-cell>{{ $user->name }}</x-table-cell>
            <x-table-cell>{{ $user->email }}</x-table-cell>
            <x-table-cell>
                <x-table-action href="{{ route('users.edit', $user) }}" icon="icon-edit" label="Edit" />
            </x-table-cell>
        </x-table-row>
    @endforeach

    <x-table-empty :colspan="3" message="No users found." />

    <x-slot:pagination>
        <x-table-pagination :links="$users" />
    </x-slot:pagination>
</x-table>
```

### Table with Livewire search and sort

```php
// Livewire component
public string $search = '';
public string $orderBy = 'name';
public string $sort = 'asc';

public function updatedSearch(): void { $this->resetPage(); }
```

```blade
<x-table wire:model.live="search" :search="$search" :order-by="$orderBy" :sort="$sort">
    <x-table-heading name="name" label="Name" sortable
        wire:click="$set('orderBy', 'name')" :order-by="$orderBy" :sort="$sort" />
    ...
</x-table>
```

---

## Text & Link (`x-text`, `x-link`)

Styled inline text and anchor elements with colour variants:

```blade
<x-text default>Default text</x-text>
<x-text brand>Brand coloured text</x-text>
<x-text danger>Error text</x-text>
<x-text muted>Muted/secondary text</x-text>

<x-link href="/dashboard" brand>Go to Dashboard</x-link>
<x-link href="/help" muted>Help</x-link>
<x-link href="https://example.com" default target="_blank">External Link</x-link>
```

Variants: `default`, `brand`, `danger`, `info`, `success`, `muted`, `warning`.

---

## Icons (`x-icon-*`)

Over 300 icons available. All accept `size` and `color` props (Tailwind classes):

```blade
<x-icon-edit size="h-5 w-5" color="text-gray-500" />
<x-icon-trash size="h-4 w-4" color="text-red-500" />
<x-icon-check-circle size="h-6 w-6" color="text-green-500" />
<x-icon-spinner size="h-5 w-5" />

{{-- File type icons --}}
<x-file-pdf size="h-8 w-8" />
<x-file-csv size="h-8 w-8" />

{{-- Brand/logo icons --}}
<x-logo-spotify size="h-6 w-6" />
<x-logo-stripe size="h-6 w-6" />
```

Dynamic icon via variable:
```blade
<x-dynamic-component :component="'icon-' . $iconName" size="h-5 w-5" />
```

### Media & download icons

Four domain-specific icons for music/streaming dashboards:

| Component | Description |
|---|---|
| `x-icon-audio-stream` | Equaliser waveform — 5 symmetric vertical bars |
| `x-icon-video-stream` | Screen outline with a play triangle inside |
| `x-icon-track-download` | Single bold bar (one track) + block down-arrow + tray |
| `x-icon-release-download` | Three stacked bars (multiple tracks) + block down-arrow + tray |

```blade
<x-button-group>
    <x-button-group-item first active icon="icon-audio-stream" text="Audio Streams" />
    <x-button-group-item icon="icon-video-stream" text="Video Streams" />
    <x-button-group-item icon="icon-track-download" text="Track Downloads" />
    <x-button-group-item last icon="icon-release-download" text="Release Downloads" />
</x-button-group>
```

---

## Layout Components

```blade
<x-layout-body>
    <x-layout-header>
        {{-- Top navigation --}}
    </x-layout-header>

    <x-layout-content>
        <x-layout-toolbar>
            {{-- Page toolbar --}}
        </x-layout-toolbar>

        {{-- Page content --}}
    </x-layout-content>

    <x-layout-footer>
        {{-- Footer content --}}
    </x-layout-footer>
</x-layout-body>
```

---

## Dropdown Menu

```blade
<x-dropdown-menu label="Options">
    <x-dropdown-option href="/edit" label="Edit" icon="icon-edit" />
    <x-dropdown-option href="/duplicate" label="Duplicate" icon="icon-copy" />
    <x-dropdown-divider />
    <x-dropdown-option href="/delete" label="Delete" icon="icon-trash" danger />
</x-dropdown-menu>
```

---

## Pill / Badge

```blade
<x-pill default label="Draft" />
<x-pill brand label="Active" />
<x-pill success label="Approved" />
<x-pill danger label="Rejected" />
<x-pill warning label="Pending" />
<x-pill muted label="Archived" />
```

---

## Progress Bar

```blade
<x-progress-bar :value="65" />
<x-progress-bar :value="30" brand />
<x-progress-bar :value="90" success />
<x-progress-bar :value="20" danger small />
```

---

## Adding or Modifying Components

### File locations

| File type | Location |
|---|---|
| PHP class | `src/Components/{Category}/{Name}.php` |
| Blade view | `resources/views/control-ui-kit/{category}/{name}.blade.php` |
| Registration | `config/control-ui-kit.php` under `'components'` |
| Theme defaults | `config/themes/default.php` |
| Tests | `tests/Components/{Category}/{Name}Test.php` |

### Creating a new Field component (example pattern)

```php
// src/Components/Forms/Fields/MyField.php
class MyField extends InputField
{
    public string $myProp;

    public function __construct(
        string $name = null,
        string $label = null,
        string $help = null,
        string $value = null,
        string $layout = null,
        string $myProp = null,
    ) {
        parent::__construct($name, $label, $help, $value, $layout);
        $this->myProp = $myProp ?? '';
    }

    public function render(): View
    {
        return view('control-ui-kit::control-ui-kit.forms.fields.my');
    }
}
```

```blade
{{-- resources/views/control-ui-kit/forms/fields/my.blade.php --}}
<x-form-field :layout="$layout" input="my-input-type" :name="$name" :help="$help" :label="$label" :my-prop="$myProp" {{ $attributes }} :value="$slot->isNotEmpty() ? $slot : $value" />
```

```php
// Register in config/control-ui-kit.php
'field-my' => \ControlUIKit\Components\Forms\Fields\MyField::class,
```

### Creating a new modern chart component

Modern chart components (Line, Column, Bar, Combo, Stacked) follow this pattern:

1. **PHP class** extends `Component`, uses `UseThemeFile` trait, reads theme from `'charts.defaults'`
2. **Constructor** accepts `string $id`, `array $datasets = []`, `array $labels = []` plus optional axis/animation/grid/legend props
3. **`render()`** returns `view('control-ui-kit::control-ui-kit.charts.{name}-chart', ['chartOptions' => $this->chartOptions()])`
4. **`chartOptions()`** returns the full Chart.js options array including scales, animation, plugins
5. **Blade template** uses `@json($datasets)`, `@json($labels)`, `@json($chartOptions)`, `@json($colors)` and the `_ro()` CSS variable resolver and `gradientColor()` helper
6. **Registration** in `config/control-ui-kit.php` as `'{name}-chart' => \ControlUIKit\Components\Charts\{Name}::class`

**Blade template gradient pattern** (for per-bar gradient support):
```javascript
const stops = ds.gradientStops || null;
const rawColor = ds.color || defaultColors[i % defaultColors.length];

var backgroundColor, borderColor;
if (stops) {
    backgroundColor = Array.from({ length: ds.data.length }, function(_, barIndex) {
        return gradientColor(barIndex / Math.max(1, ds.data.length - 1), stops);
    });
    borderColor = backgroundColor;
} else {
    backgroundColor = _ro(rawColor);
    borderColor = _ro(rawColor);
}
```

### Read-only display fields (info/link pattern)

For fields that display data without an actual input, pass `input="blank"` (plain text) or `input="link"` (anchor) and set `name=""`:

```blade
{{-- Renders: <div>{{ value }}</div> --}}
<x-form-field :layout="$layout" input="blank" name="" :label="$label" {{ $attributes }} :value="$slot->isNotEmpty() ? $slot : $value" />

{{-- Renders: <x-link href="...">{{ value }}</x-link> --}}
<x-form-field :layout="$layout" input="link" name="" :label="$label" :href="$href" {{ $attributes }} :value="$slot->isNotEmpty() ? $slot : $value" />
```

---

## Testing Components

Tests use `ComponentTestCase` (extends Testbench) with the `assertComponentRenders($expected, $template)` helper.

### Modern chart test pattern

Chart tests use `$this->blade($template)` for render assertions and `new ComponentClass(...)` for constructor assertions. No `assertComponentRenders` needed — just `assertStringContainsString`.

```php
class LineTest extends ComponentTestCase
{
    private array $datasets = [
        ['label' => 'Streams', 'data' => [100, 200, 150]],
    ];
    private array $labels = ['Jan', 'Feb', 'Mar'];

    #[Test]
    public function line_chart_renders_canvas_with_correct_id(): void
    {
        $template = <<<'HTML'
            <x-line-chart id="my_chart"
                :datasets="[['label' => 'Streams', 'data' => [1, 2, 3]]]"
                :labels="['Jan', 'Feb', 'Mar']"
            />
            HTML;

        $rendered = (string) $this->blade($template);

        $this->assertStringContainsString('<canvas id="my_chart"', $rendered);
        $this->assertStringContainsString('"label":"Streams"', $rendered);
        $this->assertStringContainsString('window.my_chart = new Chart(', $rendered);
    }

    #[Test]
    public function line_chart_constructor_assigns_id(): void
    {
        $component = new Line(id: 'my_chart', datasets: $this->datasets, labels: $this->labels);

        $this->assertSame('my_chart', $component->id);
    }
}
```

### Field test structure

```php
class MyFieldTest extends ComponentTestCase
{
    public function setUp(): void
    {
        parent::setUp();

        // Set theme config used by the component
        Config::set('themes.default.label.background', 'label-background');
        // ... other label.* and error.* configs ...
        Config::set('themes.default.form-layout-responsive.wrapper', 'wrapper');
        Config::set('themes.default.form-layout-responsive.content', 'content-style');
        Config::set('themes.default.form-layout-responsive.slot', 'slot-style');
        // ...
    }

    #[Test]
    public function the_field_can_be_rendered(): void
    {
        $this->withViewErrors([]);

        $template = <<<'HTML'
            <x-field-my name="field" label="Field" value="Hello" />
            HTML;

        $expected = <<<'HTML'
            <div class="wrapper">
                <label class="...">
                    <p class="text-style"> <span>Field</span> </p>
                </label>
                <div class="content-style">
                    <div class="slot-style">
                        ...rendered input...
                    </div>
                </div>
            </div>
            HTML;

        $this->assertComponentRenders($expected, $template);
    }
}
```

### Standard Config::set calls for field tests

Any test for a `field-*` component needs these configs set in `setUp()`:

```php
// Label styles
Config::set('themes.default.label.background', 'label-background');
Config::set('themes.default.label.border', 'label-border');
Config::set('themes.default.label.color', 'label-color');
Config::set('themes.default.label.font', 'label-font');
Config::set('themes.default.label.other', 'label-other');
Config::set('themes.default.label.padding', 'label-padding');
Config::set('themes.default.label.rounded', 'label-rounded');
Config::set('themes.default.label.shadow', 'label-shadow');

// Error styles
Config::set('themes.default.error.color', 'color');
Config::set('themes.default.error.font', 'font');
Config::set('themes.default.error.other', 'other');
Config::set('themes.default.error.padding', 'padding');

// Responsive layout styles
Config::set('themes.default.form-layout-responsive.content', 'content-style');
Config::set('themes.default.form-layout-responsive.help', 'help-style');
Config::set('themes.default.form-layout-responsive.help-mobile', 'help-mobile');
Config::set('themes.default.form-layout-responsive.text', 'text-style');
Config::set('themes.default.form-layout-responsive.label', 'label-style');
Config::set('themes.default.form-layout-responsive.required-size', 'required-size');
Config::set('themes.default.form-layout-responsive.required-color', 'required-color');
Config::set('themes.default.form-layout-responsive.slot', 'slot-style');
Config::set('themes.default.form-layout-responsive.wrapper', 'wrapper');
```

### Running tests

```bash
./vendor/bin/phpunit tests/Components/Charts/LineTest.php --no-progress
./vendor/bin/phpunit --no-progress   # full suite
```

### Important: HTML indentation in tests

The `assertComponentRenders` helper runs output through the Dindent indenter. Write expected HTML with 4-space indentation matching the nesting depth. The `<a>` tag is treated as a block element by the indenter. Use `str_replace` tricks if exact whitespace matters.
