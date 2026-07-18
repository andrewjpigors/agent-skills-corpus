---
name: whip-up-html-template-format
description: >-
  Reference for whip-up-html user template file format — v1 token contract and
  v2 MiniJinja contract — CSS pitfalls, JS rules, trust lifecycle, and limits.
  Use when the user asks about editing, debugging, or understanding an existing
  template — questions like "почему не работает", "как устроен шаблон",
  "что делает токен", "как добавить стили", "что такое forced-dark",
  "template contract", "contract_version", "v2 template", "MiniJinja".
  Also use when the user wants to modify an existing template's layout, CSS, or
  JS without creating a new one from scratch.
---

# Whip-Up-HTML: Template Format Reference

This skill covers the complete contract for whip-up-html user templates:
v1 token-based format, v2 MiniJinja format, CSS rules, JS rules, trust
lifecycle, and known pitfalls.

---

## Two template contracts

whip-up-html supports two template versions. The version is declared by
`contract_version` in `meta.toml`.

| | v1 (default) | v2 (MiniJinja) |
|---|---|---|
| `contract_version` | absent or `1` | `2` |
| Layout file | `layout.html` | `layout.html.j2` |
| Syntax | `{{TOKEN}}` substitution | `[[= var =]]` / `[[% block %]]` |
| Shell | engine-owned `shell.html` wraps it | template owns full HTML page |
| JavaScript | executed if present | disabled until trust-promoted |
| Input modes | `standard_document` only | `standard_document` or `template_data` |

Choose v1 for simple templates that map cleanly to the seven section types.
Choose v2 when you need arbitrary DOM structure, loops over sections, or
template-specific data schemas.

---

## File Structure

### v1 template

```
~/.config/whip-up-html/templates/<id>/
├── meta.toml        ← required
├── layout.html      ← required
├── style.css        ← optional, inlined after base CSS
└── script.js        ← optional, inlined before </body>
```

### v2 template

```
~/.config/whip-up-html/templates/<id>/
├── meta.toml              ← required
├── layout.html.j2         ← required, full standalone HTML page
├── style.css              ← optional
├── script.js              ← optional, disabled until trusted
├── content.schema.json    ← required only for template_data mode
└── partials/              ← optional MiniJinja partials
    └── card.html.j2
```

The folder name **must** match the `id` in `meta.toml` exactly.

---

## meta.toml

### v1 (5 required fields)

```toml
id = "my-template"                        # lowercase letters, digits, hyphens only
name = "My Template"                      # human-readable, shown in list_templates
purpose = "Short description"             # one line, shown in list_templates
badge_label = "DOCS"                      # hero badge text, keep short (2-6 chars)
required_section_types = ["faq"]          # [] = accept any
```

### v2 (additional fields)

```toml
id = "my-template"
name = "My Template"
purpose = "Short description"
badge_label = "DOCS"
required_section_types = []
contract_version = 2
input_mode = "standard_document"   # or "template_data"
```

`trust_status` is never written manually — the engine manages it.
New templates always start as `untrusted`.

---

## layout.html — Token Reference

Plain HTML fragment, no `<html>/<head>/<body>`. Engine wraps it in its shell.

### Mandatory (need at least one)

| Token | What gets injected |
|---|---|
| `{{HERO}}` | `<header class="hero"><span class="badge">…</span><h1>…</h1><p>…</p></header>` |
| `{{SECTIONS}}` | All section blocks |
| `{{FAQ_SECTIONS}}` | FAQ sections only |

### Optional

| Token | What gets injected |
|---|---|
| `{{TOC}}` | `<nav class="toc" aria-label="…"><strong>…</strong><ol><li><a href="#id">…</a></li></ol></nav>` |
| `{{SUPPORT_SECTIONS}}` | All sections except FAQ |
| `{{CTA}}` | Call-to-action block (empty string if document has none) |
| `{{FOOTER}}` | Footer (empty string if document has none) |

Tokens absent from layout.html are silently ignored.

### Section HTML the engine guarantees

**FAQ sections** (`{{FAQ_SECTIONS}}`):
```html
<section class="content-section faq-section" id="…">
  <h2>Section Title</h2>
  <details class="faq-item">
    <summary>Question text</summary>
    <div class="faq-answer"><p>Answer text</p></div>
  </details>
</section>
```

**Other section types and their CSS classes:**

| Type | Classes on `<section>` |
|---|---|
| text | `content-section text-section` |
| list | `content-section list-section` |
| steps | `content-section steps-section` |
| code | `content-section code-section` |
| table | `content-section table-section` |
| callout info | `content-section callout callout-info` |
| callout success | `content-section callout callout-success` |
| callout warning | `content-section callout callout-warning` |

---

## style.css — Rules and Pitfalls

Inlined into `<head>` **after** the selected theme CSS. Your rules take precedence.
Do not reference external URLs. Max 50 KB.

### Pitfall 1 — Base page width constraint

The engine sets:
```css
.page { width: min(calc(100% - 32px), var(--content-width)); }
```

If the template needs full viewport width (e.g. a floating window), override:

```css
.page {
  width: 100% !important;
  max-width: none !important;
  margin: 0 !important;
  padding: 0 !important;
  min-height: 100vh !important;
  position: relative !important;
}
#main-content {
  display: block !important;
  position: relative !important;
  width: 100% !important;
  min-height: 100vh !important;
}
```

> ⚠ Do NOT use `display: contents` on `#main-content` — breaks `position: fixed` children in Safari.

### Pitfall 2 — forced-dark class

The base shell JS adds `forced-dark` to `<html>` at startup (default theme = dark).
Any element that must stay light-colored needs explicit override:

```css
.my-element {
  background: #ffffee !important;   /* hardcoded hex, not a variable */
  color: #222222 !important;
  color-scheme: light;
}
```

`color-scheme: light` prevents the browser's own dark-mode adjustments inside that subtree.

### Pitfall 3 — Base FAQ chevron

The base CSS adds a circular chevron button via `summary::after`:
```css
/* base CSS does this: */
.faq-item summary { justify-content: space-between; }
.faq-item summary::after { content: "›"; /* circle button */ }
```

To replace with custom styling:
```css
.my-wrapper details.faq-item > summary {
  justify-content: flex-start;
}
.my-wrapper details.faq-item > summary::after {
  display: none !important;
}
```

### Pitfall 4 — Hero spirograph

The `.hero::after` pseudo-element renders an animated spirograph via CSS variable:
```css
.hero::after { background-image: var(--hero-spiro-img); }
```

To kill it:
```css
.hero {
  --hero-spiro-img: none;
  --hero-glow: none;
  --hero-stripe: none;
}
.hero::before, .hero::after {
  width: 0 !important;
  height: 0 !important;
  opacity: 0 !important;
}
```

### Enabling drag for a window element

Set `position: absolute` on the element JS will move:
```css
.my-window {
  position: absolute;
  /* JS sets left/top at runtime */
}
```

---

## script.js — Rules

Inlined in `<script>` tag before `</body>`, after base shell scripts.

**What the base shell already provides** (do not duplicate):
- Theme toggle (light ↔ dark), `forced-dark` / `forced-light` on `<html>`
- Back-to-top button
- "Expand all" buttons on each `.faq-section`
- Search bar inserted into `.main-column`
- TOC active-link highlight on scroll

If your template replaces any of these, remove or intercept the base elements in your JS.

**Rules:**
- Wrap all code in an IIFE: `(function () { 'use strict'; /* … */ })();`
- No ES modules (`import`/`export`), no dynamic `import()`
- `DOMContentLoaded` fires normally — use it for DOM-dependent init
- Max 50 KB

---

---

## v2 layout.html.j2 — MiniJinja dialect

v2 templates produce a **complete standalone HTML page** (includes `<!doctype
html>`, `<html>`, `<head>`, `<body>`). The engine does not add a shell.

### Delimiters

| Purpose | Syntax |
|---|---|
| Output a value | `[[= expression =]]` |
| Block tag | `[[% for/if/include/… %]]` |
| Comment | `[[# … #]]` |

### Available context for `standard_document` mode

```
document.title, .description, .badge, .lang, .footer
document.hero.title, .hero.subtitle
document.cta.title, .cta.text, .cta.button_label
document.sections  →  list
  section.type     "text"|"list"|"steps"|"faq"|"code"|"table"|"callout"
  section.id, .title
  section.paragraphs      (text)
  section.items, .ordered (list / steps / faq)
  section.code, .language, .caption  (code)
  section.columns, .rows  (table)
  section.text, .kind     (callout)
```

### Linter rules — attribute interpolation

The engine rejects interpolation in attributes unless typed correctly:

| Attribute | Required form |
|---|---|
| `href`, `src` | must use `urls.*` variable |
| `id`, `for` | must use `ids.*` variable |
| `class` | must use `classes.*` variable |
| `title`, `alt` | must use `text.*` variable |
| Any other attribute | interpolation forbidden |

Consequence: you cannot write `class="section-[[= section.type =]]"`. Use
`[[% if section.type == "callout" %]]…[[% endif %]]` branches instead.

### Partials

```
[[% include 'partials/card.html.j2' %]]
```

Only static include names are allowed. Dynamic `include` (variable path) is
rejected at compile time.

---

## v2 Trust lifecycle

| State | Meaning |
|---|---|
| `untrusted` | Installed but JS disabled; active HTML/CSS rejected |
| `quarantined` | Failed compilation or policy check; not renderable |
| `trusted` | Explicitly promoted; JS allowed with enforced CSP |

Every new template starts as `untrusted`. JavaScript in `script.js` is silently
disabled until the user promotes it.

### Promote to trusted

```bash
whip-up-html trust inspect <id>   # shows SHA-256 digest
whip-up-html trust promote <id> <digest> 2
```

After promotion the server must reconnect (see MCP Caching below) to pick up
the new trust state.

### Inspect and list

```bash
whip-up-html trust list            # all user templates and their trust state
whip-up-html trust inspect <id>    # digest and details for one template
```

### Revoke

```bash
whip-up-html trust revoke <id> <digest> 2
```

Revoke returns the template to `untrusted`. A reconnect is required.

---

## v2 Limits

| Resource | Limit |
|---|---|
| Entry layout (`layout.html.j2`) | 512 KiB |
| One partial | 256 KiB |
| `style.css` | 2 MiB |
| `script.js` | 1 MiB |
| `content.schema.json` | 256 KiB |
| Total package | 8 MiB |
| Package files | 128 |
| Include depth | 32 |
| Saved HTML output | 16 MiB |
| `render_html_page` response | 1 MiB |

---

## MCP Caching — Important

The MCP server loads template files **once at startup**.

Any change to template files requires a server reload before it takes effect.
The correct reload sequence — do NOT restart all of Claude Code:

```bash
whip-up-html stop
# Then click Reconnect (⟳) next to whip-up-html in Claude Code's MCP panel
```

Claude Code restarts only the whip-up-html process; the rest of the session is
unaffected.

Workaround for rapid CSS/JS iteration: patch the generated HTML file directly
with Python or sed, then reload in browser. Merge changes back to template files
when satisfied.

---

## Template Install Location

User templates: `~/.config/whip-up-html/templates/<id>/`

Project source (canonical, version-controlled):
`/Users/eugene/ProjectWork/whip-up-html/whip-up-html/`

The install scripts (`install.sh`, `install.ps1`) copy the bundled `templates/`
folder from the release archive to the user config directory.

---

## Deleting / Resetting a Template

```bash
rm -rf ~/.config/whip-up-html/templates/<id>
```

Engine falls back to built-in templates automatically on next restart.

---

## Working Reference — mac-help

`~/.config/whip-up-html/templates/mac-help/` is a complete working example.
Implements: drag window, maximize/restore, terminal overlay, notepad overlay,
sidebar TOC, search, forced-dark protection, hero spirograph removed, FAQ left-aligned.
