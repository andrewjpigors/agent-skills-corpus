---
name: dragble-custom-tools
description: Build custom drag-and-drop tools and property editor widgets for the Dragble editor. Covers tool registration, declarative templates, JS renderers, property definitions, widgets, property states, transformers, validators, canvas scripts, and email-safe HTML patterns.
license: MIT
metadata:
  author: dragble
  version: "1.0"
---

# Dragble Custom Tools

## Overview

Custom tools are drag-and-drop content blocks that users can place on the editor canvas. They are registered via `dragble.registerTool()` through the SDK or `window.dragble.registerTool()` inside custom JS scripts loaded by the editor.

**Two rendering modes** (auto-detected — no flag needed):

| Mode | Trigger | Best for |
|---|---|---|
| **Declarative (Template)** | Config has `template` (string) | ~60% of tools — HTML + mustache-like syntax |
| **JS Renderer** | Config has `renderer` (function) | Dynamic tools — QR codes, charts, runtime JS |

Having both `template` AND `renderer` is an error.
Having neither defaults to declarative with an empty template.

**Rules:**
- Tool IDs (`name`) **must be camelCase**: `coupon`, `productCard`, `qrCode`
- No `custom#` prefix in config — the editor adds `custom#` internally
- Properties use `editor` (widget type) and `default` (not `defaultValue`)
- Flat properties auto-group under "Settings"; grouped properties use explicit `{ title, position, properties }`
- Functions (`renderer`, `script`, `validator`) are serialized as `__DRAGBLE_FN__`-prefixed strings when crossing the postMessage boundary — closures don't survive

---

## Complete Example: Declarative Template Mode

A coupon code tool with template, emailTemplate, and flat properties:

```typescript
dragble.registerTool({
  name: 'couponCode',
  label: 'Coupon Code',
  icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><line x1="2" y1="12" x2="22" y2="12"/></svg>',
  category: 'interactive',
  description: 'Displays a styled coupon code with a copy button',

  // Declarative template — uses {{value}} syntax
  template: `
    <div style="text-align:center; padding:{{padding}}; background:{{bgColor}}; border:2px dashed {{borderColor}}; border-radius:8px;">
      {{#if showLabel}}
        <div style="font-size:14px; color:{{textColor}}; margin-bottom:8px;">
          {{label || 'Your Coupon Code'}}
        </div>
      {{/if}}
      <div style="font-size:{{fontSize}}; font-weight:bold; color:{{codeColor}}; letter-spacing:2px;">
        {{code}}
      </div>
      {{#if showExpiry}}
        <div style="font-size:12px; color:#999; margin-top:8px;">
          Expires: {{expiryDate}}
        </div>
      {{/if}}
    </div>
  `,

  // Email-specific template (table-based for Outlook compatibility)
  emailTemplate: `
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:2px dashed {{borderColor}}; border-radius:8px; background:{{bgColor}};">
      <tr>
        <td align="center" style="padding:{{padding}};">
          {{#if showLabel}}
            <div style="font-size:14px; color:{{textColor}}; margin-bottom:8px;">
              {{label || 'Your Coupon Code'}}
            </div>
          {{/if}}
          <div style="font-size:{{fontSize}}; font-weight:bold; color:{{codeColor}}; letter-spacing:2px;">
            {{code}}
          </div>
          {{#if showExpiry}}
            <div style="font-size:12px; color:#999999; margin-top:8px;">
              Expires: {{expiryDate}}
            </div>
          {{/if}}
        </td>
      </tr>
    </table>
  `,

  // Flat properties — auto-grouped under "Settings"
  properties: {
    code:        { editor: 'text',         default: 'SAVE20',    label: 'Coupon Code' },
    bgColor:     { editor: 'color_picker', default: '#fff8e1' },
    borderColor: { editor: 'color_picker', default: '#f59e0b' },
    textColor:   { editor: 'color_picker', default: '#333333' },
    codeColor:   { editor: 'color_picker', default: '#d97706' },
    fontSize:    { editor: 'font_size',    default: '28px' },
    padding:     { editor: 'text',         default: '24px' },
    showLabel:   { editor: 'toggle',       default: true },
    label:       { editor: 'text',         default: 'Your Coupon Code' },
    showExpiry:  { editor: 'toggle',       default: false },
    expiryDate:  { editor: 'text',         default: '2025-12-31' },
  },

  // Hide expiry fields when showExpiry is off
  propertyStates: {
    expiryDate: { show: { property: 'showExpiry', equals: true } },
    label:      { show: { property: 'showLabel',  equals: true } },
  },
});
```

---

## Complete Example: JS Renderer Mode

A product card with `renderer`, `emailRenderer`, and grouped properties:

```typescript
dragble.registerTool({
  name: 'productCard',
  label: 'Product Card',
  icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/></svg>',
  category: 'interactive',

  // JS renderer — receives values, returns HTML string
  renderer: (values) => {
    const price = Number(values.price) || 0;
    const salePrice = values.onSale ? Number(values.salePrice) || 0 : null;
    return `
      <div style="border:1px solid ${values.borderColor}; border-radius:8px; overflow:hidden; font-family:sans-serif;">
        <img src="${values.imageUrl}" alt="${values.title}" style="width:100%; height:200px; object-fit:cover;" />
        <div style="padding:16px;">
          <h3 style="margin:0 0 8px; color:${values.titleColor};">${values.title}</h3>
          <p style="margin:0 0 12px; color:#666; font-size:14px;">${values.description}</p>
          <div style="font-size:18px; font-weight:bold; color:${values.priceColor};">
            ${salePrice !== null ? `<span style="text-decoration:line-through; color:#999; margin-right:8px;">$${price.toFixed(2)}</span>` : ''}
            $${(salePrice ?? price).toFixed(2)}
          </div>
        </div>
      </div>
    `;
  },

  // Email renderer — table-based layout for email clients
  emailRenderer: (values) => {
    const price = Number(values.price) || 0;
    const salePrice = values.onSale ? Number(values.salePrice) || 0 : null;
    return `
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid ${values.borderColor}; border-radius:8px;">
        <tr>
          <td>
            <img src="${values.imageUrl}" alt="${values.title}" width="600" style="width:100%; display:block;" />
          </td>
        </tr>
        <tr>
          <td style="padding:16px;">
            <h3 style="margin:0 0 8px; color:${values.titleColor};">${values.title}</h3>
            <p style="margin:0 0 12px; color:#666666; font-size:14px;">${values.description}</p>
            <div style="font-size:18px; font-weight:bold; color:${values.priceColor};">
              ${salePrice !== null ? `<span style="text-decoration:line-through; color:#999999; margin-right:8px;">$${price.toFixed(2)}</span>` : ''}
              $${(salePrice ?? price).toFixed(2)}
            </div>
          </td>
        </tr>
      </table>
    `;
  },

  // Grouped properties — explicit sections with titles and ordering
  properties: {
    content: {
      title: 'Content',
      position: 1,
      properties: {
        title:       { editor: 'text',     default: 'Product Name' },
        description: { editor: 'textarea', default: 'A short description of the product.' },
        imageUrl:    { editor: 'image',    default: 'https://placehold.co/600x400' },
      },
    },
    pricing: {
      title: 'Pricing',
      position: 2,
      properties: {
        price:     { editor: 'text',   default: '49.99', label: 'Regular Price' },
        onSale:    { editor: 'toggle', default: false },
        salePrice: { editor: 'text',   default: '29.99' },
      },
    },
    style: {
      title: 'Style',
      position: 3,
      properties: {
        titleColor:  { editor: 'color_picker', default: '#1a1a1a' },
        priceColor:  { editor: 'color_picker', default: '#16a34a' },
        borderColor: { editor: 'color_picker', default: '#e5e7eb' },
      },
    },
  },

  propertyStates: {
    salePrice: { show: { property: 'onSale', equals: true } },
  },

  transformer: {
    onSale: {
      false: { salePrice: '' },
    },
  },
});
```

---

## DragbleToolConfig Reference

All fields on the tool configuration object:

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | `string` | Yes | — | camelCase tool ID: `coupon`, `productCard` |
| `label` | `string` | Yes | — | Display label in the side panel |
| `icon` | `string` | No | default icon | SVG string for the tool icon |
| `category` | `'text'\|'media'\|'interactive'\|'advanced'\|'layout'` | No | `'advanced'` | Panel category |
| `description` | `string` | No | — | Tooltip text |
| `order` | `number` | No | — | Sort order in panel (lower = higher) |
| `template` | `string` | No* | — | HTML template (declarative mode) |
| `emailTemplate` | `string` | No | — | Email-specific template override |
| `renderer` | `(values) => string` | No* | — | HTML renderer function (JS mode) |
| `emailRenderer` | `(values) => string` | No | — | Email-specific renderer function |
| `properties` | `DragbleProperties` | No | — | Property definitions (flat or grouped) |
| `baseToolType` | `string` | No | `'html'` | Base tool: `paragraph\|heading\|button\|image\|divider\|menu\|html\|social\|video\|table` |
| `includeBaseProperties` | `boolean` | No | `false` | Include base tool's existing properties |
| `supportedDisplayModes` | `('email'\|'web'\|'popup')[]` | No | all modes | Which editor modes show this tool |
| `usageLimit` | `number` | No | `0` (unlimited) | Max instances in a design |
| `head` | `{ css?: string, js?: string }` | No | — | CSS/JS injected into `<head>` when tool is present |
| `propertyStates` | `PropertyStatesConfig` | No | — | Dynamic property show/hide rules |
| `transformer` | `TransformerConfig` | No | — | Cross-property auto-updates |
| `validator` | `function \| string` | No | — | Content audit rules |
| `openOnDrop` | `boolean` | No | `false` | Auto-open content dialog on drop |
| `data` | `Record<string, unknown>` | No | — | Arbitrary data from SDK config |
| `script` | `(container, values) => cleanup?` | No | — | Canvas lifecycle script |
| `url` | `string` | No | — | URL to a JS file exporting `{ tool, widgets? }` |

*One of `template` or `renderer` is expected (but neither is technically required — empty template is valid).

---

## Property Definitions

### Flat Properties

All properties at the top level, auto-grouped under a "Settings" section:

```typescript
properties: {
  bgColor:  { editor: 'color_picker', default: '#ffffff' },
  title:    { editor: 'text',         default: 'Hello' },
  fontSize: { editor: 'font_size',    default: '16px' },
}
```

### Grouped Properties

Explicit sections with `title`, `position`, and nested `properties`:

```typescript
properties: {
  content: {
    title: 'Content',
    position: 1,
    properties: {
      title:       { editor: 'text',     default: 'Heading' },
      description: { editor: 'textarea', default: '' },
    },
  },
  style: {
    title: 'Style',
    position: 2,
    properties: {
      bgColor: { editor: 'color_picker', default: '#ffffff' },
    },
  },
}
```

Mixing flat and grouped is **not allowed** — the normalizer rejects it.

### DragblePropertyDef

Each property definition:

| Field | Type | Required | Description |
|---|---|---|---|
| `editor` | `string` | Yes | Widget type name (see Widget Types below) |
| `label` | `string` | No | Display label. Auto-generated from key if omitted (`bgColor` -> "Bg Color") |
| `default` | `unknown` | No | Default value. Extracted into tool defaults automatically |
| `hideOnMobile` | `boolean` | No | Hide this property on mobile view |
| `message` | `string` | No | Help text shown below the property |
| `data` | `Record<string, unknown>` | No | Editor-specific config (dropdown options, slider range, etc.) |

---

## Widget Types

### Built-In Generic Widgets

30+ widget types available for property editors. Use the **generic name** (left column) in property definitions:

| Generic Name | Default Value Type | What It Renders | Access Pattern |
|---|---|---|---|
| `text` | `string` | Single-line text input | `values.propName` (string) |
| `textarea` | `string` | Multi-line text input / code editor | `values.propName` (string) |
| `rich_text` | `string` | Rich text editor (falls back to code editor) | `values.propName` (HTML string) |
| `color_picker` | `string` | Color picker with label | `values.propName` (`'#rrggbb'`) |
| `alignment` | `string` | Text alignment (left/center/right/justify) | `values.propName` (`'left'\|'center'\|'right'\|'justify'`) |
| `text_alignment` | `string` | Text alignment (4-way) | Same as `alignment` |
| `vertical_alignment` | `string` | Vertical alignment (start/center/end) | `values.propName` (`'flex-start'\|'center'\|'flex-end'`) |
| `font_family` | `string` | Font family dropdown | `values.propName` (font name string) |
| `font_weight` | `string\|number` | Font weight picker | `values.propName` (`'400'\|'700'` etc.) |
| `font_size` | `string` | Font size counter (px) | `values.propName` (`'16px'`) |
| `border` | `object` | Border editor (width + color + style) | `values.propName` (border object) |
| `single_border` | `object` | Single-side border | `values.propName` (border object) |
| `counter` | `string\|number` | Numeric increment/decrement | `values.propName` (number or string) |
| `image` | `string` | Image URL input with dimensions | `values.propName` (URL string) |
| `image_upload` | `string` | Image upload with file manager + preview | `values.propName` (URL string) |
| `toggle` | `boolean` | On/off switch | `values.propName` (`true\|false`) |
| `link` | `object` | Link/action URL editor | `values.propName` (link object) |
| `dropdown` | `string` | Dropdown select | `values.propName` (selected value) |
| `datetime` | `string` | Date/time input (falls back to numeric) | `values.propName` (string) |
| `slider` | `number\|string` | Range slider | `values.propName` (number) |
| `spacing` | `string` | 4-side padding/margin editor | `values.propName` (CSS shorthand) |
| `border_radius` | `string` | 4-corner border radius editor | `values.propName` (CSS shorthand) |
| `line_height` | `string` | Line height (%) | `values.propName` (`'140%'`) |
| `letter_spacing` | `string` | Letter spacing (px) | `values.propName` (`'0.5px'`) |
| `html` | `string` | HTML code editor | `values.propName` (HTML string) |
| `code_editor` | `string` | Code editor with syntax highlighting | `values.propName` (code string) |
| `heading_type` | `string` | Heading level selector (h1-h4) | `values.propName` (`'h1'\|'h2'\|'h3'\|'h4'`) |
| `visibility` | `object` | Desktop/mobile show/hide toggles | `values.propName` (visibility object) |
| `auto_width` | `boolean\|string` | Auto-width toggle + percentage | `values.propName` |
| `video_url` | `string` | Video URL input with auto-detection | `values.propName` (URL string) |

### Aliases

These aliases resolve to the same widget. Use whichever reads best:

| Alias | Resolves To |
|---|---|
| `color` | `color_picker` |
| `input`, `text_input` | `text` |
| `number`, `numeric` | `counter` |
| `padding`, `margin` | `spacing` |
| `radius`, `borderradius` | `border_radius` |
| `code`, `html_code`, `raw_html` | `code_editor` |
| `text_align`, `textalign` | `text_alignment` |
| `vertical_align`, `verticalalign`, `valign` | `vertical_alignment` |
| `heading`, `heading_level` | `heading_type` |
| `hide_show`, `display` | `visibility` |
| `width_auto`, `autowidth` | `auto_width` |
| `border_top`, `border_side` | `single_border` |
| `file`, `upload` | `image_upload` |
| `video` | `video_url` |

### Dropdown Configuration

Pass options via the `data` field:

```typescript
layout: {
  editor: 'dropdown',
  default: 'horizontal',
  data: {
    options: [
      { label: 'Horizontal', value: 'horizontal' },
      { label: 'Vertical',   value: 'vertical' },
      { label: 'Grid',       value: 'grid' },
    ],
  },
}
```

### Slider Configuration

Pass min/max/step via the `data` field:

```typescript
opacity: {
  editor: 'slider',
  default: 100,
  data: {
    min: 0,
    max: 100,
    step: 1,
  },
}
```

### Resolution Order

When the editor encounters a property type string, it resolves in this order:

1. **Custom renderer** — registered via `dragble.registerPropertyEditor()` or `createWidget()`
2. **Generic widget** — resolved from the table above (e.g., `color_picker` -> internal `TEXT_COLOR`)
3. **Internal renderer** — direct SCREAMING_CASE lookup (e.g., `FONT_SIZE`, `ALIGNMENT`)
4. **Fallback** — dev warning in development, null in production

SCREAMING_CASE types (e.g., `IMAGE_UPLOAD`, `FONT_SIZE`) always bypass generic widget resolution and go directly to the internal renderer.

---

## Template Engine Syntax

Used in `template` and `emailTemplate` fields. Processing order: `#each` -> `#if` -> `#unless` -> `{{{raw}}}` -> `{{escaped}}`.

### Value Interpolation

```handlebars
{{value}}                    HTML-escaped output
{{{rawHtml}}}                Unescaped HTML (triple braces)
{{nested.key.path}}          Dot-notation access into nested objects
{{value || 'fallback'}}      Fallback when value is empty/undefined/null
```

### Conditional Blocks

```handlebars
{{#if showImage}}
  <img src="{{imageUrl}}" />
{{/if}}

{{#if hasTitle}}
  <h2>{{title}}</h2>
{{else}}
  <h2>Untitled</h2>
{{/if}}

{{#unless hideFooter}}
  <footer>{{footerText}}</footer>
{{/unless}}

{{#unless hideFooter}}
  <footer>{{footerText}}</footer>
{{else}}
  <!-- footer hidden -->
{{/unless}}
```

Truthiness rules: `null`, `undefined`, `false`, empty string, `0`, empty array -> **falsy**. Everything else -> **truthy**.

### Iteration

```handlebars
{{#each items}}
  <div>
    {{name}} - ${{price}}
    {{#if @first}}<span class="badge">First!</span>{{/if}}
    {{#if @last}}<span class="badge">Last!</span>{{/if}}
    <small>Item #{{@index}}</small>
  </div>
{{/each}}
```

Inside `{{#each}}`:
- `{{this}}` — current item (for primitive arrays like strings/numbers)
- `{{@index}}` — 0-based index
- `{{@first}}` — `true` if first item
- `{{@last}}` — `true` if last item
- Object properties are merged into scope: if item is `{ name: 'Widget' }`, use `{{name}}` directly

### Safety

- `{{value}}` escapes HTML (`<` -> `&lt;`). Use `{{{raw}}}` only when you trust the content.
- Template errors are **logged but never thrown**. Bad expressions return the raw placeholder in dev, empty string in production.
- No `eval()` or `new Function()`. Only property access and simple truthiness.
- Nesting limit: 10 levels of recursion per block type (safety counter).

---

## Property States

Control which properties are visible based on other property values.

### Simple Declarative

```typescript
propertyStates: {
  borderColor: {
    show: { property: 'style', equals: 'outlined' }
  },
  borderWidth: {
    show: { property: 'style', in: ['outlined', 'bordered'] }
  },
  subtitle: {
    show: { property: 'showSubtitle', truthy: true }
  },
}
```

Available operators on a single condition (AND-ed if multiple):
- `equals` — strict equality
- `notEquals` — strict inequality
- `in` — value is in array
- `notIn` — value is not in array
- `truthy` — value is truthy (set to `true`)
- `falsy` — value is falsy (set to `true`)

### Functional

```typescript
propertyStates: {
  gradient: {
    show: (values) => values.bgType === 'gradient' && values.enableBg === true
  },
}
```

Functions cannot cross postMessage (not serializable). Use declarative for SDK-registered tools.

### Compound Conditions (all / any / not)

```typescript
propertyStates: {
  borderRadius: {
    show: {
      all: [
        { property: 'style', equals: 'outlined' },
        { property: 'enableRoundedCorners', equals: true },
      ]
    }
  },
  altLayout: {
    show: {
      any: [
        { property: 'mode', equals: 'advanced' },
        { property: 'forceAlt', equals: true },
      ]
    }
  },
  simpleBorder: {
    show: {
      not: { property: 'style', equals: 'none' }
    }
  },
}
```

On evaluation errors, the property **defaults to visible** (never silently hidden).

---

## Transformers

Auto-update properties when another property changes. Runs **once per change** (no cascading, prevents loops). The changed property itself is never overwritten by the transformer (user's explicit change always wins).

### Declarative Transformer

```typescript
transformer: {
  // When 'style' changes to 'minimal', set these values
  style: {
    minimal:  { borderColor: 'transparent', borderWidth: '0' },
    outlined: { borderColor: '#000000', borderWidth: '1px' },
  },
  // When 'enableBg' changes to 'false', clear bg properties
  enableBg: {
    false: { bgColor: 'transparent', bgImage: '' },
  },
}
```

Format: `{ [changedProperty]: { [matchValue]: { [targetProp]: newValue } } }`

Match values are compared via `String(value)` — booleans become `'true'`/`'false'`, numbers become their string representation.

### Functional Transformer

```typescript
transformer: (values, changedProperty) => {
  if (changedProperty === 'imageSize') {
    const size = Number(values.imageSize) || 200;
    return { imageWidth: `${size}px`, imageHeight: `${size}px` };
  }
  if (changedProperty === 'style' && values.style === 'minimal') {
    return { borderColor: 'transparent', borderWidth: '0', shadow: 'none' };
  }
  return {};
}
```

Functions cannot cross postMessage. Use declarative for SDK-registered tools.

---

## Canvas Scripts

The `script` field attaches interactive behavior to the tool's rendered HTML on the canvas. Receives the container DOM element and current property values. Can return a cleanup function.

```typescript
dragble.registerTool({
  name: 'countdownTimer',
  label: 'Countdown Timer',
  template: `
    <div style="text-align:center; padding:20px; background:{{bgColor}}; font-family:monospace;">
      <div style="font-size:12px; color:{{labelColor}}; margin-bottom:8px;">{{label}}</div>
      <div class="countdown-display" style="font-size:{{fontSize}}; color:{{digitColor}}; font-weight:bold;">
        00:00:00:00
      </div>
    </div>
  `,
  properties: {
    targetDate:  { editor: 'text',         default: '2025-12-31T00:00:00', label: 'Target Date (ISO)' },
    label:       { editor: 'text',         default: 'Time Remaining' },
    bgColor:     { editor: 'color_picker', default: '#1a1a2e' },
    labelColor:  { editor: 'color_picker', default: '#aaaaaa' },
    digitColor:  { editor: 'color_picker', default: '#ffffff' },
    fontSize:    { editor: 'font_size',    default: '36px' },
  },

  // Canvas script — runs inside the editor workspace
  script: (container, values) => {
    const display = container.querySelector('.countdown-display');
    if (!display) return;

    const target = new Date(values.targetDate).getTime();

    function tick() {
      const now = Date.now();
      const diff = Math.max(0, target - now);
      const days = Math.floor(diff / 86400000);
      const hrs  = Math.floor((diff % 86400000) / 3600000);
      const mins = Math.floor((diff % 3600000) / 60000);
      const secs = Math.floor((diff % 60000) / 1000);
      display.textContent =
        `${String(days).padStart(2,'0')}:${String(hrs).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
    }

    tick();
    const interval = setInterval(tick, 1000);

    // Return cleanup function — called before re-render or tool removal
    return () => clearInterval(interval);
  },
});
```

**Rules:**
- The script runs after the tool's HTML is inserted into the canvas DOM
- The cleanup function is called before re-render (property change) or when the tool is removed
- Scripts are serialized as `__DRAGBLE_FN__`-prefixed strings when crossing postMessage — closures over external variables will NOT work
- For email export, scripts are ignored (email HTML is static)

---

## Content Dialog

Auto-open a host-app dialog when a tool is dropped. The dialog runs in the **host app context** (outside the editor iframe), giving full access to the host app's UI framework.

```typescript
// Tool config
dragble.registerTool({
  name: 'productPicker',
  label: 'Product',
  template: '<div style="padding:16px;"><h3>{{productName}}</h3><p>{{productDescription}}</p></div>',
  openOnDrop: true,   // <-- triggers dialog on drop
  properties: {
    productName:        { editor: 'text', default: '' },
    productDescription: { editor: 'text', default: '' },
    productImage:       { editor: 'text', default: '' },
  },
});

// SDK init — register the dialog callback
dragble.init({
  // ... other config ...
  callbacks: {
    onContentDialog: (info) => {
      // info.toolType   = "custom#productPicker"
      // info.action     = "insert" | "edit"
      // info.currentValues = { ... } (for edit action)
      return new Promise((resolve) => {
        showProductPickerModal({
          onSelect: (product) => resolve({
            productName: product.name,
            productDescription: product.description,
            productImage: product.imageUrl,
          }),
          onCancel: () => resolve({ cancelled: true }),
        });
      });
    },
  },
});
```

**Flow:**
1. User drops tool -> editor sends `DRAGBLE_CONTENT_DIALOG_REQUEST` to SDK
2. SDK calls `onContentDialog(info)` -> host app shows modal
3. Host app resolves with values or `{ cancelled: true }`
4. Editor merges values into tool content; sidebar properties remain available for fine-tuning
5. If cancelled on insert: tool is removed. If cancelled on edit: no change.

Dialog timeout: 60 seconds.

---

## Custom Widgets (createWidget)

When none of the 30+ built-in widgets fit, create a custom property editor widget.

### Mode A: Render/Mount/Update/Unmount

Lightweight, reactive lifecycle:

```typescript
dragble.createWidget({
  name: 'star_rating',

  // render() returns HTML string — called on initial render
  render(value, updateValue, context) {
    const stars = Number(value) || 0;
    return `<div class="star-rating">${
      [1,2,3,4,5].map(i =>
        `<span data-star="${i}" style="cursor:pointer; font-size:24px; color:${i <= stars ? '#f59e0b' : '#ddd'};">&#9733;</span>`
      ).join('')
    }</div>`;
  },

  // mount() — called after render HTML is inserted into DOM
  mount(node, value, updateValue, context) {
    node.addEventListener('click', (e) => {
      const star = (e.target as HTMLElement).dataset.star;
      if (star) updateValue(Number(star));
    });
  },

  // update() — called when value changes externally (undo, transformer, load)
  // If omitted, the widget is fully re-rendered (render + mount) on change
  update(node, value, context) {
    const stars = Number(value) || 0;
    node.querySelectorAll('[data-star]').forEach((el) => {
      const i = Number((el as HTMLElement).dataset.star);
      (el as HTMLElement).style.color = i <= stars ? '#f59e0b' : '#ddd';
    });
  },

  // unmount() — cleanup when widget is removed from DOM
  unmount(node) {
    // Remove event listeners if needed
  },
});

// Use in tool properties:
dragble.registerTool({
  name: 'reviewBlock',
  label: 'Review',
  template: '<div>Rating: {{rating}}/5</div>',
  properties: {
    rating: { editor: 'star_rating', default: 3 },
  },
});
```

### Mode B: URL/Iframe

For widgets built with any framework. The iframe communicates via postMessage:

```typescript
dragble.createWidget({
  name: 'map_picker',
  url: 'https://my-app.com/widgets/map-picker.html',
  height: 300,  // iframe height in pixels (default: 200)
});
```

The iframe page receives messages:
- `{ type: "init", value, data, theme }` — on load
- `{ type: "update", value }` — when value changes externally (undo, transformer, load)

The iframe sends:
- `{ type: "setValue", value }` — to update the property value

### WidgetContext

All Mode A lifecycle functions receive a `WidgetContext`:

```typescript
interface WidgetContext {
  values: Record<string, unknown>;  // ALL tool property values
  data: Record<string, unknown>;    // Application data from init config
  theme: { accentColor: string; mode: 'light' | 'dark' };
  toolName: string;                 // Tool name this widget belongs to
}
```

Widgets receive ALL tool values (not just their own), enabling cross-property logic without a transformer.

### Widget Registration Order

Widgets **flush before tools**. When the editor initializes:
1. Pending widgets are sent via `CREATE_WIDGET` messages
2. Then pending tools are sent via `ADD_TOOL` messages

This ensures widget types are registered in the `PropertyEditorRegistry` before tools reference them via `editor: "widget_name"`.

### Serialization

Functions in widget configs (`render`, `mount`, `update`, `unmount`) are serialized as `__DRAGBLE_FN__`-prefixed strings when crossing postMessage:

```
"__DRAGBLE_FN__function render(value, updateValue, context) { ... }"
```

**Closures don't survive serialization.** The function body is serialized via `.toString()` and reconstructed on the other side. Variables captured from outer scope will be `undefined`. Keep widget functions self-contained.

### Layout

Widgets can specify layout positioning:

```typescript
dragble.createWidget({
  name: 'my_widget',
  render: (value, updateValue) => `<div>...</div>`,
  layout: 'bottom',  // 'inline' (default) | 'bottom' | 'full-width'
});
```

---

## Validators

Custom content audit rules. Called during `audit()` to check tool content for issues. Returns `AuditRule[]`.

### Function Validator

```typescript
dragble.registerTool({
  name: 'imageBlock',
  label: 'Image Block',
  template: '<img src="{{imageUrl}}" alt="{{altText}}" />',
  properties: {
    imageUrl: { editor: 'image', default: '' },
    altText:  { editor: 'text',  default: '' },
  },

  validator: (info) => {
    const errors = [];
    const { design, defaultErrors } = info;
    // info.design = full design data
    // info.defaultErrors = built-in audit errors
    // info.tool = "custom#imageBlock"

    // Check all instances of this tool in the design
    // Return AuditRule[] array:
    if (!info.design) return errors;

    errors.push({
      id: 'imageBlock-missing-alt',
      severity: 'WARNING',    // 'ERROR' | 'WARNING' | 'INFO'
      title: 'Missing Alt Text',
      description: 'Image blocks should have alt text for accessibility.',
    });

    return errors;
  },
});
```

### String Validator (postMessage-safe)

For SDK-registered tools, provide the validator as a function body string:

```typescript
validator: `
  var errors = [];
  // 'info' is the argument name
  if (!info.design) return errors;
  errors.push({
    id: 'my-check',
    severity: 'WARNING',
    title: 'Check Failed',
    description: 'Something needs attention.',
  });
  return errors;
`
```

String validators are auto-registered with the Redux validator system. Function validators are executed directly from metadata (10-second timeout).

### AuditRule Shape

```typescript
interface AuditRule {
  id: string;              // Unique rule ID
  severity: 'ERROR' | 'WARNING' | 'INFO';
  title: string;           // Short description
  description: string;     // Detailed explanation
  tool?: { type: string }; // Auto-tagged with tool type
}
```

---

## Email-Safe HTML Patterns

Email clients (especially Outlook) have severe CSS limitations. Use these patterns in `emailTemplate` and `emailRenderer`.

### Table-Based Button

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td align="center" bgcolor="{{buttonColor}}" style="border-radius:4px;">
      <a href="{{buttonUrl}}" target="_blank"
         style="display:inline-block; padding:12px 24px; color:{{buttonTextColor}};
                text-decoration:none; font-family:Arial,sans-serif; font-size:16px;
                font-weight:bold; border-radius:4px;">
        {{buttonText}}
      </a>
    </td>
  </tr>
</table>
```

### Two-Column Layout

```html
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td width="50%" valign="top" style="padding-right:10px;">
      <!-- Left column content -->
    </td>
    <td width="50%" valign="top" style="padding-left:10px;">
      <!-- Right column content -->
    </td>
  </tr>
</table>
```

### Safe CSS Properties

These work across all major email clients:

| Safe | Notes |
|---|---|
| `color` | Use hex codes, not `rgb()` |
| `background-color`, `bgcolor` | Use `bgcolor` on `<td>` for Outlook |
| `font-family` | Stick to web-safe stacks with `Arial,sans-serif` fallback |
| `font-size`, `font-weight`, `font-style` | Use `px` units |
| `text-align`, `vertical-align` | Use on `<td>` elements |
| `padding` | On `<td>` elements. Avoid padding on `<div>` |
| `border` | Simple borders work. Use `border-collapse: collapse` on tables |
| `width`, `height` | Use HTML attributes on `<table>`, `<td>`, `<img>` |
| `line-height` | Use `px` values |
| `text-decoration` | `none`, `underline` |
| `display: block/inline` | On `<img>` to prevent gaps |
| `margin` | Unreliable — use padding on `<td>` or spacer rows instead |
| `border-radius` | Works in modern clients, ignored in Outlook |

### Unsafe CSS (Avoid in Email Templates)

| Unsafe | Why |
|---|---|
| `flexbox`, `grid` | No support in Outlook |
| `position`, `float` | Inconsistent across clients |
| `box-shadow`, `text-shadow` | No Outlook support |
| `opacity` | Ignored in many clients |
| `max-width`, `min-width` | Unreliable — use fixed `width` |
| `background-image` | Requires VML fallback for Outlook |
| `calc()` | Not supported in email |
| `@media` queries | Limited — only some clients support |
| `CSS custom properties (--var)` | No support |
| `transform`, `animation`, `transition` | Not supported |

---

## Common Mistakes

### 1. Tool name not camelCase

```typescript
// WRONG — will be rejected
{ name: 'my-tool',     ... }  // kebab-case
{ name: 'MyTool',      ... }  // PascalCase
{ name: 'my_tool',     ... }  // snake_case
{ name: 'TOOL',        ... }  // uppercase

// CORRECT
{ name: 'myTool',      ... }
{ name: 'coupon',      ... }
{ name: 'productCard', ... }
```

Name must match `/^[a-z][a-zA-Z0-9]*$/`.

### 2. Both template and renderer

```typescript
// WRONG — error: cannot have both
{
  name: 'myTool',
  template: '<div>{{value}}</div>',
  renderer: (v) => `<div>${v.value}</div>`,
}

// CORRECT — pick one
{ name: 'myTool', template: '<div>{{value}}</div>', ... }
// OR
{ name: 'myTool', renderer: (v) => `<div>${v.value}</div>`, ... }
```

### 3. Missing emailTemplate for email tools

If your tool is used in email mode and the web template uses non-email-safe CSS (flexbox, grid), provide a table-based `emailTemplate`. Without it, the web template is used for email export too, which may break in Outlook.

### 4. Mixing flat and grouped properties

```typescript
// WRONG — cannot mix flat and grouped
properties: {
  bgColor: { editor: 'color_picker', default: '#fff' },  // flat
  content: {                                               // grouped
    title: 'Content',
    properties: { title: { editor: 'text', default: '' } },
  },
}

// CORRECT — pick one style
// All flat:
properties: {
  bgColor: { editor: 'color_picker', default: '#fff' },
  title:   { editor: 'text',         default: '' },
}

// All grouped:
properties: {
  style:   { title: 'Style',   position: 1, properties: { bgColor: { editor: 'color_picker', default: '#fff' } } },
  content: { title: 'Content', position: 2, properties: { title: { editor: 'text', default: '' } } },
}
```

### 5. Closures in serialized functions

```typescript
// WRONG — `API_BASE` is captured from outer scope, will be undefined after serialization
const API_BASE = 'https://api.example.com';
dragble.registerTool({
  name: 'myTool',
  renderer: (values) => `<img src="${API_BASE}/images/${values.id}" />`,  // API_BASE is gone!
});

// CORRECT — inline all values
dragble.registerTool({
  name: 'myTool',
  renderer: (values) => `<img src="https://api.example.com/images/${values.id}" />`,
});
```

### 6. Using `default` instead of `defaultValue`

```typescript
// WRONG — this is the old Unlayer convention
properties: {
  color: { editor: 'color_picker', defaultValue: '#fff' },
}

// CORRECT — Dragble uses 'default'
properties: {
  color: { editor: 'color_picker', default: '#fff' },
}
```

### 7. Property state references unknown property

```typescript
// WRONG — 'theme' doesn't exist in properties
propertyStates: {
  borderColor: { show: { property: 'theme', equals: 'dark' } },
}

// CORRECT — reference a property that exists in the tool's properties
properties: {
  style: { editor: 'dropdown', default: 'solid', data: { options: [...] } },
  borderColor: { editor: 'color_picker', default: '#000' },
},
propertyStates: {
  borderColor: { show: { property: 'style', equals: 'outlined' } },
}
```

### 8. Expecting transformer cascading

Transformers run **once** per property change. If transformer A sets property B, and property B has a transformer rule, that rule does **not** fire. This prevents infinite loops.

### 9. Using `custom#` prefix in tool name

```typescript
// WRONG — the editor adds custom# internally
{ name: 'custom#coupon', ... }

// CORRECT — just the camelCase name
{ name: 'coupon', ... }
```

### 10. createWidget before init

```typescript
// WRONG — throws "Editor not initialized"
dragble.createWidget({ name: 'myWidget', render: ... });
dragble.init({ ... });

// CORRECT — init first, then create widget (it queues automatically)
dragble.init({ ... });
dragble.createWidget({ name: 'myWidget', render: ... });
// Widget is queued and flushed after INIT handshake completes
```
