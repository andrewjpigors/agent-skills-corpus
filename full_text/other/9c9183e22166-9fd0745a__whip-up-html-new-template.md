---
name: whip-up-html-new-template
description: >-
  Create a new whip-up-html v2 user template from an existing HTML source.
  Use when the user provides an HTML file, URL, or code and asks to turn it
  into a reusable template. Triggered by phrases like "сделай шаблон",
  "создай шаблон", "добавь шаблон", "make a template", "new template", or
  "port this to a template". Always invoke this skill before doing any file
  work related to creating a new whip-up-html template.
---

# Whip-Up-HTML: Create New Template (Import Workflow)

Convert an existing HTML source into a v2 whip-up-html user template installed
to `~/.config/whip-up-html/templates/<id>/`. The template is created as
**untrusted** and must be explicitly promoted by the user before JavaScript
executes.

This skill follows the source-preserving import workflow. Do **not** reconstruct
a visual approximation from memory or training data — the source DOM is the
contract. Deviations must be listed in the compatibility report.

---

## Step 0 — Acquire the source

The user must provide the source HTML. Accepted forms:

- **File path** — read with the Read tool
- **URL** — fetch raw HTML with WebFetch (not a text-only summary)
- **Inline code** — use as-is from the conversation

A text description alone is insufficient for this workflow. If the user has only
a description, ask whether they want to create a template from scratch using the
v1 token approach instead (see the `whip-up-html-template-format` skill).

If no source has been provided, ask:

> "Покажи источник — путь к HTML-файлу, URL или вставь код прямо сюда.
> Текстовое описание не подходит для этого workflow — нужен настоящий HTML."

Store the raw source text as the **reference snapshot**. Do not modify it.

---

## Step 1 — Store a reference snapshot

Write the raw source to a temporary reference file so it can be compared later:

```bash
mkdir -p /tmp/wuh-import
```

Save the source as `/tmp/wuh-import/reference.html`. This is the immutable
baseline. All compatibility checks compare the rendered template output against
this file.

---

## Step 2 — Ask for template id and name

Ask in one message:

> "Как назвать шаблон?
> - **id** (папка + идентификатор): строчные буквы и цифры, только дефисы,
>   например `mac-help`, `terminal-docs`
> - **name** (человекочитаемое): например «Mac Help Center»"

Wait for the user's answer. The `id` must match `^[a-z][a-z0-9-]*$`.

---

## Step 3 — Analyse the source DOM

Read the reference snapshot and extract:

1. **Body DOM structure** — layout containers, sidebar, header, main, footer,
   overlay panels. Note the actual HTML elements and class names used.
2. **Static presentation nodes** — decorative elements, icons, chrome that do
   not vary per document (keep them verbatim in the template).
3. **Content-bearing nodes** — text, headings, lists, code blocks, tables,
   callouts that will differ per rendered document. These become MiniJinja
   variables or loops.
4. **Inline and linked CSS** — extract `<style>` blocks and same-origin `<link
   rel="stylesheet">` content.
5. **JavaScript** — identify all `<script>` blocks and their behaviors. Note
   any external dependencies or network calls.
6. **Assets** — images, fonts, icons referenced by `src`, `href`, or `url()`.
   Note whether they are inline (data URIs) or external.

Produce a **mapping report** (written to `/tmp/wuh-import/mapping.md`):

```markdown
# Mapping report: <id>

## Content nodes → template variables
| Source selector / description | Template variable / loop |
|---|---|
| `<h1 class="title">` | `[[= document.title =]]` |
| `<ul class="features"> li` | `[[% for item in section.items %]]` |
| … | … |

## Static nodes (preserved verbatim)
- Window chrome: `.titlebar`, `.traffic-lights`
- Decorative background: `.hero-bg`

## Unsupported / removed active content
| Element / behavior | Reason | Disposition |
|---|---|---|
| `<script src="https://cdn.example.com/…">` | External network | Removed |
| `onclick="eval(…)"` | Inline handler | Removed |

## Missing / external assets
| Asset | Status |
|---|---|
| `logo.png` (external URL) | Not embedded — placeholder comment added |

## Engine constraints applied
- No dynamic `href`/`src` interpolation (linter requires `urls.*` prefix)
- No `id`/`class` attribute interpolation (linter requires `ids.*`/`classes.*`)
```

Write this file, then show the user a summary of the mapping before proceeding.

---

## Step 4 — Create the template folder

```bash
mkdir -p ~/.config/whip-up-html/templates/<id>
```

---

## Step 5 — Write meta.toml

```toml
id = "<id>"
name = "<name>"
purpose = "<one-sentence description>"
badge_label = "<SHORT>"          # 2–6 chars, e.g. HELP, DOCS, GUIDE
contract_version = 2
input_mode = "standard_document" # or "template_data" for non-standard layouts
required_section_types = []      # [] = accept any section type
```

**v2 template rules:**
- `contract_version = 2` is required for MiniJinja templates
- `input_mode = "standard_document"` uses the built-in `Document` model
- `input_mode = "template_data"` requires a `content.schema.json` file
- No `trust_status` field — new templates are always `untrusted` until explicitly promoted

---

## Step 6 — Write layout.html.j2

Preserve the source DOM. Replace only the mapped content nodes with MiniJinja
expressions. Keep all structural HTML, classes, IDs and attributes verbatim.

**Template delimiters:**

| Purpose | Delimiter | Example |
|---|---|---|
| Variable output | `[[= … =]]` | `[[= document.title =]]` |
| Block tag | `[[% … %]]` | `[[% for section in document.sections %]]` |
| Comment | `[[# … #]]` | `[[# static nav =]]` |

**Available document variables** (for `input_mode = "standard_document"`):

```
document.title
document.description
document.badge
document.lang
document.hero.title
document.hero.subtitle
document.footer
document.cta.title / .text / .button_label
document.sections  → list of section objects
  section.type     → "text" | "list" | "steps" | "faq" | "code" | "table" | "callout"
  section.id
  section.title
  section.paragraphs (text sections)
  section.items (list/steps/faq sections)
  section.ordered (list sections)
  section.code / section.language / section.caption (code sections)
  section.columns / section.rows (table sections)
  section.text / section.kind (callout sections)
```

**Template linter rules** — violations cause compile failure:

| Attribute | Required prefix |
|---|---|
| `href`, `src` | `urls.*` — e.g. `urls.button_url` |
| `id`, `for` | `ids.*` |
| `class` | `classes.*` |
| `title`, `alt` | `text.*` |
| Any other attribute | Interpolation forbidden |

Because of these rules: do **not** interpolate dynamic section IDs into `href`
anchors — use static TOC text instead. Do not use `[[= section.type =]]` inside
`class` attributes — use `[[% if section.type == "callout" %]]` branches instead.

**The template must produce a complete standalone HTML document** (includes
`<!doctype html>`, `<html>`, `<head>`, `<body>`). v2 templates do not use the
engine's shell.html — they own the full page structure.

---

## Step 7 — Write style.css

Extract all CSS from the source (inline `<style>` blocks + linked same-origin
stylesheets). Place the combined CSS in `style.css`.

Rules:
- Do not reference external URLs in `url()` — embed assets as data URIs or omit
- Do not use `@import` with remote URLs
- Max 2 MiB

---

## Step 8 — Write script.js (if JavaScript is present)

Extract `<script>` content from the source into `script.js`.

**Important — JavaScript is disabled until trusted:**
- The template installs as `untrusted`
- The engine will not execute `script.js` until the user runs trust promotion
- This is correct behavior — inform the user in the compatibility report

Remove or note:
- External `<script src="…">` tags (network access forbidden)
- Inline event handlers (`onclick`, `onload`, etc.)
- `eval()`, `Function()`, `setTimeout`/`setInterval` with string arguments
- `import()` dynamic imports

Wrap remaining code in an IIFE:
```js
(function () {
  'use strict';
  // … your code …
})();
```

---

## Step 9 — Write compatibility report

Write `/tmp/wuh-import/compatibility-report.md`:

```markdown
# Compatibility report: <id>

## Status: UNTRUSTED — JavaScript disabled

## What was preserved
- Full page DOM structure
- All CSS styles
- (list preserved interactive features)

## What was changed
| Original | Change | Reason |
|---|---|---|
| `<script src="cdn.example.com/lib.js">` | Removed | External network forbidden |
| `onclick="…"` handlers | Removed | Inline handlers forbidden |

## What requires manual review before trust promotion
- [ ] JavaScript behavior in browser (all buttons, overlays, interactions)
- [ ] No unexpected network requests (browser DevTools → Network tab)
- [ ] No console errors

## Assets not embedded
| Asset | Original source | Status |
|---|---|---|
| logo.png | https://… | Placeholder — add as data URI manually |

## Engine constraint deviations
- (list any DOM differences required by the linter)
```

Show the user the compatibility report summary.

---

## Step 10 — Install, stop, and reload

After writing all files:

```bash
whip-up-html status    # confirm server is running
whip-up-html stop
whip-up-html status    # confirm stopped
```

Then tell the user:

> "Шаблон установлен. Нажми **Reconnect** рядом с whip-up-html в панели MCP
> (иконка ⟳). Полный перезапуск Claude Code не нужен.
> После reconnect проверю через list_templates, что `<id>` появился."

After the user confirms reconnect, call `list_templates` to verify the template
loaded. Check that it appears with the correct `id` and `name`.

---

## Step 11 — Test render (untrusted, no JS)

Call `save_html_page` with a minimal test document:

```json
{
  "template_id": "<id>",
  "output_path": "/tmp/wuh-import/test-<id>.html",
  "document": {
    "title": "Test render",
    "sections": [
      { "type": "text", "id": "test", "title": "Test", "paragraphs": ["Content."] }
    ]
  }
}
```

If the render fails, read the error, fix the template, and retry.

---

## Step 12 — Trust promotion (user action)

Inform the user:

> "Шаблон `<id>` загружен как **untrusted** — JavaScript отключён.
> Перед включением JS:
> 1. Открой `/tmp/wuh-import/test-<id>.html` в браузере
> 2. Убедись, что всё выглядит правильно без JS
> 3. Когда будешь готов включить JS, запусти:
>
> ```bash
> whip-up-html trust inspect <id>
> ```
>
> Это выведет SHA-256 digest пакета. Затем:
>
> ```bash
> whip-up-html trust promote <id> <digest> 2
> ```
>
> После promote нужен ещё раз Reconnect — сервер перечитает trust store."

Do not run `trust promote` on behalf of the user. Trust promotion requires
explicit user intent.

---

## Reference — mapping report file

After this workflow completes, `/tmp/wuh-import/` contains:
- `reference.html` — original source snapshot
- `mapping.md` — content node mapping
- `compatibility-report.md` — what changed and what to verify
- `test-<id>.html` — test render output
