---
name: ikenga-artifact-builder
description: |
  Author a self-contained interactive HTML artifact (dashboard, view,
  comparison, mockup) that renders standalone in any browser AND lights up
  with live data when opened inside the Ikenga shell. Replaces .md for
  visual/interactive/data-bearing outputs.

  TRIGGER when: the user asks for a dashboard, view, summary-as-page,
  comparison, mockup, prototype, "make me an HTML…", or any output where
  interactivity or live data adds value over static text. Also trigger when
  CLAUDE.md / memory has a rule preferring artifacts over .md for visual
  outputs.

  Has two invocation paths: a **wizard fast-path** (kicked off by the
  Ikenga shell's artifact-creation wizard with archetype + folder already
  chosen — build immediately) and a **discover path** (direct invocation
  from terminal / chat — runs a five-question discovery before building,
  scoping memory queries to the active Claude project).

  DO NOT TRIGGER for: prose, technical writeups, decision docs, READMEs,
  long-form explanations, code reviews — those stay as .md.
license: Apache-2.0
---

# Ikenga Artifact Builder

You produce **single-file HTML artifacts** that:

- Render standalone in any browser (claude.ai's artifact viewer included).
- Light up with live data when opened inside the Ikenga shell.
- Are easy to share, review, paste into chat, and iterate on.

## Two invocation paths

This skill is invoked two ways. Take a different first turn for each.

### A. Wizard fast-path (kicked off by the Ikenga shell)

The Ikenga artifact-creation wizard spawned this session with a kickoff
prompt that already names project + archetype + suggested path. The
prompt has a recognisable shape:

> Build a **one-pager** for project **royalti-io-website**
> (`/home/.../royalti-io-website`).
>
> Suggested path: `one-pagers/q3-recap.html` (under the project root).
> Use that, or ask me where it should live.
>
> Read `.claude/skills/` in this project to know which sub-skills are
> available, then ask 2-3 clarifying questions about audience, tone,
> and structure before writing anything. Use the `ikenga-artifact-builder`
> skill for the build phase.

**Detect the fast-path** by all three of these in the first user message:

1. The phrase `Build a <archetype-label>` where `<archetype-label>` is one
   of: `dashboard`, `one-pager`, `slide deck`, `social card`, `site`,
   `scrollytelling experience`, `artifact`.
2. A `Suggested path:` line with a backtick-quoted `.html` path.
3. A backtick-quoted absolute project root path on the same line as
   "for project".

When all three are present, **skip the discover phase entirely**. Treat
the project root in backticks as the project identifier (the wizard does
not include a separate `project_id` — it identifies the project by
root_path). Pull the archetype label and the suggested path verbatim
from the prompt. Then jump to workflow step 2 ("Sketch data sources"),
ask at most one short clarifying question about content, and build.

### B. Discover path (direct invocation)

User invoked you directly from a terminal `claude`, an existing chat
thread, or a skill chain — none of the wizard markers above are present.
Run the five-question discovery below before building.

## Discover phase (direct path only)

Ask five short questions in order, one at a time. Don't batch. Capture
the answers — at the end they form the same internal state the wizard's
kickoff would have produced (project root, archetype slug, target
folder, suggested path).

### 1. What are you building?

Free text. Listen for words mapping to one of the seven archetypes
(`dashboard`, `one-pager`, `slides`, `social`, `site`, `scrollytelling`)
or the explicit "just plain HTML" out. Don't propose anything yet.

### 2. Archetype confirm

Echo back the closest match and let the user redirect. The seven
canonical archetypes (kept in sync with
`shell/src/shell/artifact-wizard/archetypes.ts` — that file is the
source of truth):

| Slug | When |
|------|------|
| `dashboard` | KPIs, charts, live data, scan-and-scroll. Default 1440×900. |
| `one-pager` | Proposal, summary, landing-page-as-doc. Default 1440×900. |
| `slides` | Sequential reveal, presenter mode. 16:9 (1920×1080). |
| `social` | Square 1080×1080 social card. Single dense composition. |
| `site` | Multi-section landing-style site in a single HTML file. |
| `scrollytelling` | Scroll-driven narrative, pinned sections, progressive reveals. |
| `blank` | None of these — just plain HTML, bespoke structure. |

Phrase it as: "Sounds like a `one-pager`. Yes / no / something else?"
Accept "none of these — just plain HTML" as the explicit out (→ `blank`).

### 3. Where does it live?

Default to `<project-root>/<archetype-default-subdir>/<slug>.html` where
`<project-root>` is the active project's root (from `pwd` in a terminal
session, or asked of the user in a chat without shell access) and
`<archetype-default-subdir>` is the archetype's `defaultSubdir` from
the table:

| Slug | `defaultSubdir` |
|------|----------------|
| `dashboard` | `dashboards` |
| `one-pager` | `one-pagers` |
| `slides` | `slides` |
| `social` | `social` |
| `site` | `sites` |
| `scrollytelling` | `scrollytelling` |
| `blank` | `artifacts` |

Show the proposed full path; let the user override either the folder
or the slug. Validate that the parent dir exists (or will be created
by the agent on first write) before continuing.

### 4. Project context check + memory hits

Before recommending sub-skills, walk **both** of these directories and
parse frontmatter (`name`, `description`) from every `*.md`:

- `<project-root>/.claude/skills/*.md` — project-scoped skills.
- `~/.claude/skills/*.md` — user-global skills (tag these `(global)`
  in any listing so the user knows the source).

Recommend only skills you actually saw on disk. Don't suggest
`huashu-design` if it isn't installed in this project.

Then query mempalace for similar past artifacts in **this** Claude
project. Pass the project root path as the `project_id` filter (see
"Memory queries" below — this is the same identity the wizard threads
into its own pre-fetch). Surface up to three hits with one-line
summaries each; ask whether to riff on any of them.

### 5. Confirm + hand off

Echo the assembled state back:

> Building a **<archetype-label>** at `<full-path>`.
> Project: `<project-root>`.
> Sub-skills available here: <comma-separated list>.
> Memory hits: <three one-liners, or "none">.
>
> Ready?

On confirmation, hand off to the build workflow below (the same workflow
the fast-path enters). The internal state at this point matches what
`scaffold.ts::startArtifact` would have produced from the wizard.

## Memory queries (both paths)

Mempalace identifies projects by **the absolute project root path**.
That's the same key the wizard threads (its kickoff prompt names
`display_name` and `root_path` — root_path is the load-bearing
identifier; `display_name` is for humans). There's no separate
shell-internal `project_id` to thread; the path *is* the id.

How to derive it:

- **Wizard fast-path**: extract the backtick-quoted absolute path from
  the kickoff prompt's "for project … (`<root>`)" line.
- **Discover path**: ask the user for `pwd` (terminal) or have them
  paste the project root (chat). The path captured in question 3 above
  is also a valid source if it already lies under a project root.

The mempalace MCP surface doesn't have a `project_id` filter parameter
— scoping happens through the entity name itself. Concrete patterns:

- **Knowledge-graph queries** — call
  `mempalace_kg_query({ entity: <project-root-path> })` and walk the
  returned triples for facts attached to the project. Triples written
  this way look like `(<project-root-path>, has_artifact, <slug>)` or
  `(<project-root-path>, last_archetype, dashboard)`.
- **Semantic search** — include the project root path (or the project's
  display name, if known) in the `query` string when calling
  `mempalace_search`. The room/wing filters are about
  agent identity, not project identity, so pass them only if you
  already know which agent diary you want.
- **Diary writes** — pass `topic: 'project:<project-root-path>'` when
  calling `mempalace_diary_write`. Future skill runs can find
  project-scoped diaries by prefix-matching the topic.
- **Adding facts** — when recording "we built X here today" via
  `mempalace_kg_add`, use the project root path as `subject`. This is
  what makes the `kg_query({entity: <path>})` reads above return
  anything in future sessions.

If you didn't pin down a project root (rare — only happens if the user
is working outside any project), skip the project scoping rather than
guess. A global memory hit is better than a wrong-project hit.

## When to produce an artifact vs a .md file

| Situation | Output |
|-----------|--------|
| Dashboard, KPIs, charts | Artifact |
| Comparison table the user will scan/sort | Artifact |
| UI mockup, prototype, design exploration | Artifact |
| Anything with live data (SQL, Supabase, API, MCP) | Artifact |
| Status page the user wants to refresh | Artifact |
| Prose, writeups, decision docs, READMEs | `.md` |
| Step-by-step instructions, runbooks | `.md` |
| Code reviews, technical analysis | `.md` |

If unsure, ask: *"will the user **interact** with this, or just **read** it?"* Interact → artifact. Read → markdown.

## The hard rules

1. **Single self-contained HTML file** unless the user explicitly asks for a folder/multi-page artifact.
2. **Must render with no network access** — include a `<script id="ikenga-mock-data" type="application/json">` block with realistic mock data, and the page must use it as a fallback when the bridge is absent or sources fail.
3. **No `eval`, no `Function(...)`, no `document.write`** — claude.ai's artifact viewer blocks them, and our shell's CSP does too.
4. **No external network in the static layer** unless declared in `dataSources`. CDN imports (React, Tailwind, the bridge) are fine; ad-hoc `fetch` calls are not.
5. **Manifest is mandatory** as `<script type="application/json" id="ikenga-manifest">…</script>`. The `fallback` block in it is mandatory for any artifact you intend to share.

If you can't satisfy these, write a `.md` instead and tell the user why.

## File layout

### Single-file (default)

```
output.html    ← the whole artifact, including manifest, mock data, styles, code
```

### Folder (only when user asks for assets, sub-pages, or large data)

```
my-artifact/
├── index.html
├── manifest.json
├── data/
│   └── mock.json
└── assets/
    └── logo.svg
```

## Single-file template

Start from this skeleton. Fill in the marked regions; do not restructure.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{{ARTIFACT NAME}}</title>

  <!-- Manifest. Required. Auto-derived capabilities; no explicit block needed. -->
  <script type="application/json" id="ikenga-manifest">
  {
    "format": "ikenga-artifact",
    "formatVersion": "0.1",
    "id": "{{kebab-case-id}}",
    "name": "{{Human Name}}",
    "version": "0.1.0",
    "description": "{{One-line purpose.}}",
    "license": "Apache-2.0",
    "icon": { "lucide": "{{lucide-icon-name}}" },
    "dataSources": {
      /* declare every live source here; bridge auto-fetches on init */
    },
    "fallback": {
      "mode": "mock",
      "dataTag": "ikenga-mock-data",
      "banner": "Running outside Ikenga — showing mock data."
    },
    "pin": {
      "suggested": false,
      "section": "{{suggested-section-or-omit}}",
      "label": "{{Short label}}"
    },
    "requires": { "ikenga": ">=0.4", "bridge": "^1.0" }
  }
  </script>

  <!-- Mock data. Required. Must match shape of live sources. -->
  <script type="application/json" id="ikenga-mock-data">
  {
    /* one key per dataSource; values match what live source would return */
  }
  </script>

  <!-- Styles. Tailwind via CDN OK. Inline custom styles below. -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- darkMode:'class' so `dark:` utilities track the Ikenga shell toggle
       (the host bridge mirrors a `.dark` class) instead of the OS media query. -->
  <script>tailwind.config = { darkMode: 'class' };</script>
  <!-- Standalone theming. Inside Ikenga the injected host bridge has already
       mirrored the shell's data-mode/data-theme + `.dark` onto <html> (and the
       shell pre-injects @ikenga/tokens, so var(--bg-base) etc. resolve). This
       block only runs OUTSIDE the shell, following the OS color scheme so a
       shared artifact still does dark/light. -->
  <script>
    (function () {
      if (window.__ikenga_host__) return; // in-shell: host bridge owns theme
      var root = document.documentElement, mql = window.matchMedia('(prefers-color-scheme: dark)');
      var apply = function () {
        root.setAttribute('data-mode', mql.matches ? 'dark' : 'light');
        root.setAttribute('data-theme', 'A');
        root.classList.toggle('dark', mql.matches);
      };
      apply();
      if (mql.addEventListener) mql.addEventListener('change', apply);
      else if (mql.addListener) mql.addListener(apply);
    })();
  </script>
  <style>
    /* custom styles only — keep minimal. Palette-aware surfaces should use the
       @ikenga/tokens custom properties (var(--bg-base), var(--bg-surface),
       var(--fg), var(--fg-muted), var(--border), var(--primary), …) so they
       track the shell's A/B/C theme. Tailwind utilities are fine for layout. */
  </style>

  <!-- React UMD (globals: React, ReactDOM). Pin minor — unpinned URLs occasionally serve breaking minors. -->
  <script crossorigin src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
  <script crossorigin src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>

  <!-- Babel-standalone for in-browser JSX. Loaded from cache inside Ikenga (shell pre-injects). -->
  <script src="https://cdn.jsdelivr.net/npm/@babel/standalone@7.25.6/babel.min.js"></script>
</head>

<!-- Token-backed surfaces track the shell's A/B/C palette + light/dark. For a
     simpler artifact you can instead use Tailwind neutrals
     (`bg-neutral-50 text-neutral-900 dark:bg-neutral-950 dark:text-neutral-100`) —
     those still flip light/dark via the `.dark` class, but won't pick up the palette. -->
<body class="antialiased" style="background: var(--bg-base); color: var(--fg);">
  <!-- Visible placeholder so a JS-init failure is distinguishable from a CSS/HTML failure. -->
  <div id="root">
    <div class="max-w-2xl mx-auto p-6 text-sm" style="color: var(--fg-muted);">Initializing…</div>
  </div>

  <!--
    Plain `text/babel` (NOT `data-type="module"`) + UMD React globals + IIFE async.
    Why: `text/babel` + ESM imports + top-level `await` is brittle in Babel-standalone
    and produces silent blank pages. The pattern below is the one validated by the
    three v0 example artifacts; do not switch to ESM imports unless you've also
    confirmed Babel-standalone has matured around module mode.
  -->
  <script type="text/babel" data-presets="env,react">
    (function () {
      const { useState, useEffect } = React;

      // Recommended hook: subscribes once, re-renders on refresh. Use one per source.
      function useSource(art, name) {
        const [value, setValue] = useState(() => art.source(name).get());
        useEffect(() => art.source(name).subscribe(setValue), [art, name]);
        return [value, () => art.source(name).refresh()];
      }

      function App({ art }) {
        // const [foo, refreshFoo] = useSource(art, 'foo');

        // Expose state the conversation should react to (selection, step, decisions).
        // Readable from a terminal via `iyke iframe-state <pane>`. See SKILL.md
        // "Surfacing state to the shell (`publishState`)" for when to use this.
        // useEffect(() => { art.publishState && art.publishState('selection', selectedIds); }, [selectedIds]);

        return (
          <div className="max-w-2xl mx-auto p-6">
            {art.host.anyFallback() && (
              <div className="mb-4 px-3 py-2 rounded border border-amber-200 dark:border-amber-900/50 bg-amber-50 dark:bg-amber-900/20 text-amber-900 dark:text-amber-200 text-sm">
                Showing mock data for one or more sources.
              </div>
            )}
            {/* render here */}
          </div>
        );
      }

      // Once `@ikenga/artifact` is on a CDN, replace the polyfill reference with:
      //   const art = await bridge.init();
      // (still inside this IIFE — do not hoist top-level await out of it).
      window.__ikenga_bridge_polyfill__.init().then(function (art) {
        ReactDOM.createRoot(document.getElementById('root')).render(<App art={art} />);
      }).catch(function (err) {
        // Visible error surface — far easier to debug than a silent blank page.
        document.getElementById('root').innerHTML =
          '<pre style="padding:2rem;color:#b91c1c;font-family:ui-monospace,monospace;white-space:pre-wrap">'
          + 'Init failed: ' + (err && err.message ? err.message : String(err))
          + '</pre>';
        console.error('[ikenga] init failed', err);
      });
    })();
  </script>
</body>
</html>
```

**Note on JSX + Babel.** `data-presets="env,react"` enables JSX. The artifact opens directly in any browser (`file://`, claude.ai, Ikenga shell) without a build step. Inside Ikenga, the shell pre-injects `@babel/standalone` into the artifact iframe, so the artifact's `<script src>` resolves from cache (~300KB paid once per shell session, not per artifact).

**Why UMD + IIFE, not ESM + top-level await.** `<script type="text/babel" data-type="module">` with ESM imports and top-level `await` produces silent blank pages with current Babel-standalone — validated empirically while building the v0 examples. The UMD-globals + plain-`text/babel` + IIFE-async pattern above survives in every host we tested (`file://`, claude.ai's artifact viewer, the Launch preview panel). Revisit when Babel-standalone's module mode hardens.

**Why pinned CDN versions.** Unpinned URLs (`react@18`, `@babel/standalone@7`) occasionally serve a breaking minor that bricks all artifacts referencing them. Always pin to a tested patch (`react@18.3.1`, `@babel/standalone@7.25.6`).

## Data source types

Every entry in `dataSources` has a `type`, type-specific config, and a `refresh` block.

### `supabase`

```json
{
  "type": "supabase",
  "table": "v_cash_position",
  "select": "id, amount, currency, as_of",
  "filter": [["currency", "eq", "USD"]],
  "refresh": { "mode": "interval", "every": "15m", "onFocus": true }
}
```

Outside Ikenga: returns mock data from the `dataTag` block. Inside Ikenga: bridge resolves Supabase project from manifest's host context, RLS applies as the current user.

### `sql` (local SQLite)

```json
{
  "type": "sql",
  "db": "ikenga.local",
  "query": "select * from ar_aging_view",
  "params": [],
  "refresh": { "mode": "manual" }
}
```

Read-only. Bind parameters via `params`. Outside Ikenga: mock.

### `fetch` (HTTP)

```json
{
  "type": "fetch",
  "url": "https://api.royalti.io/fx/today",
  "method": "GET",
  "headers": {},
  "refresh": { "mode": "interval", "every": "1h" }
}
```

Network host added to the artifact's CSP allowlist automatically. Outside Ikenga: bridge attempts the fetch directly (subject to browser CORS); falls back to mock on failure.

### `mcp`

```json
{
  "type": "mcp",
  "server": "royalti-cms",
  "tool": "findPosts",
  "args": { "limit": 10 },
  "refresh": { "mode": "manual" }
}
```

Inside Ikenga only — bridge routes through the shell's MCP registry. Outside: mock.

### `file` (local watched file)

```json
{
  "type": "file",
  "path": "./data/last_run.json",
  "refresh": { "mode": "watch" }
}
```

Folder-mode only. Bridge watches via shell's fs_watch. Outside: reads once if reachable, else mock.

## `refresh` modes

- `{ "mode": "manual" }` — only when `art.source(name).refresh()` is called.
- `{ "mode": "interval", "every": "15m" }` — `1s`, `30s`, `5m`, `1h`, `1d` etc.
- `{ "mode": "interval", "every": "15m", "onFocus": true }` — also refresh when pane regains focus.
- `{ "mode": "watch" }` — file/realtime sources only.

## Compatibility constraints

- **No `eval`, `Function`, `document.write`.**
- **No inline event handlers** (`onclick="…"`, `onload="…"`). React `onClick={fn}` JSX is fine — it's a property, not an HTML attribute. Inline `style="…"` is also fine.
- **CSP-friendly.** Prefer Tailwind classes or `<style>` blocks over inline `style=` attributes when practical.
- **CDN imports only from**: `esm.sh`, `cdn.skypack.dev`, `cdn.tailwindcss.com`, `cdn.jsdelivr.net`. Anything else needs to be declared in `dataSources` (and thus in the network allowlist). Drop `unpkg.com` — `esm.sh`/`jsdelivr` are strictly better.
- **Pin CDN versions.** Use `react@18.3.1`, `@babel/standalone@7.25.6`, etc. Unpinned URLs occasionally serve breaking minors and silently brick artifacts.
- **Entry HTML ≤ 500KB** (warn) / 2MB (error). Folder-mode `assets/` and `data/` are uncapped.
- **No service workers, no `localStorage` for sensitive data.** Use `art.state.set/get` (host-mediated, SQLite-backed inside Ikenga, `localStorage` fallback in plain browser).
- **Visible "Initializing…" placeholder + visible init-error panel.** A blank page during dev means you can't tell whether HTML failed, CSS failed, or JS failed. Use the patterns in the template; don't omit them.

## Notes-back loop (auto-wired)

The bridge auto-injects a floating **"💬 comment" button in the bottom-right** of every artifact. Click → comment mode (cursor crosshair, click any element to attach a note → text input → send). Modal toggle, off by default — your own click handlers are untouched when comment mode is off.

In `ikenga` and `preview-cli` hosts, notes route back to the originating chat session with a marker linking to the artifact + selector. In plain `browser` host, the button is hidden (no chat to route to).

To opt out (printable reports, embedded widgets, anywhere the chrome would be wrong):

```json
"notes": { "enabled": false }
```

Explicit API still available when an artifact has its own feedback UI:

```js
art.notes.send("This chart needs a 90-day toggle", { selector: "#cash-chart" });
```

## Style guidance

- **Default to system fonts** + Tailwind — looks clean, ships nothing extra.
- **React to the shell theme.** Inside Ikenga the host bridge mirrors the shell's
  `data-mode` (light/dark) + `data-theme` (A/B/C palette) + a `.dark` class onto the
  artifact's `<html>`, live on every toggle, and the shell pre-injects `@ikenga/tokens`.
  So: use the token custom properties (`var(--bg-base)`, `var(--bg-surface)`, `var(--fg)`,
  `var(--fg-muted)`, `var(--border)`, `var(--primary)`, …) for surfaces/text/borders and
  they track the active palette automatically. Tailwind `dark:` utilities also work
  (template sets `darkMode:'class'`). Standalone (claude.ai / browser) the template's
  inline script follows the OS `prefers-color-scheme`; palette defaults to A.
- **Density**: dashboards skew dense (people scan). Mockups skew spacious. Pick one and commit.
- **Don't reinvent chart libraries** — for any non-trivial chart, import `recharts` or `apache-echarts` via esm.sh. For sparklines or single-metric tiles, hand-rolled SVG is fine and lighter. For chart colors that should match the theme, read `art.theme` (see cheat sheet) or pull `getComputedStyle(document.documentElement).getPropertyValue('--primary')`.
- **Keep total visual elements ≤ 7 per screen.** If you have more, split into tabs or sub-pages (folder mode).
- **Tokens vs. raw Tailwind.** Token-backed surfaces (above) are the default for anything
  meant to feel native in the shell. Raw Tailwind neutrals are the lightweight fallback —
  they still flip light/dark via `.dark`, but won't pick up the A/B/C palette.

## Workflow

1. **Clarify scope.** If the user's ask is ambiguous (e.g., "make me a dashboard"), ask one clarifying question: what data, what timeframe, what's the primary decision they're making with it. Don't ask more than one — unblock and iterate.
2. **Sketch data sources.** List every piece of data the artifact needs. For each, decide source type and refresh mode. Write the `dataSources` block first, then `mock-data` to match.
3. **Build the React tree.** Use the `useSource(art, name)` hook (in the template) — it returns `[value, refresh]` and handles subscribe/unsubscribe. One call per source. Avoid hand-rolling `useEffect` subscriptions unless you have a reason to.
4. **Write the fallback path.** Confirm the artifact renders correctly with mock data alone (close the live data subscriptions, reload — does it still work?).
5. **Self-check the compatibility rules.** No eval, no inline handlers, file size, CSP. Run the checklist before delivering.
6. **Deliver.** Tell the user where the file is, how to open it (just open in a browser, or open in Ikenga for live data), and what to do next (review, leave notes, ask for changes).

## Self-check before delivering

- [ ] Manifest tag present and valid JSON
- [ ] Manifest `license` is `Apache-2.0` (per ADR-009 every pkg/artifact ships Apache-2.0 — the BUSL tier was retired; don't copy a stale `BUSL-1.1` from older examples)
- [ ] Mock data tag present, shape matches every dataSource
- [ ] Renders with no network (mock-only)
- [ ] No `eval`, `Function`, `document.write`, inline event handlers
- [ ] All CDN imports from approved hosts
- [ ] Single file under 500KB (or in folder mode)
- [ ] Reacts to shell theme: light + dark legible, palette-aware surfaces use tokens; OS fallback works standalone
- [ ] `pin.section` is a sensible suggestion or omitted

If any box is unchecked, fix before delivering.

## Bridge surface (cheat sheet)

> **Stable bridge contract.** The four surfaces named below — `art.publishState`, `art.notes`, `art.pin`, and `art.host` — are the **public bridge contract** pinned by the manifest's `requires.bridge ^1.0`. We won't break their shape inside the `1.x` line; additions are minor-version, removals are major. Composing skills (`groundwork`, downstream artifacts that ride the bridge for `iyke iframe-state` reads, the activity-bar pin handshake) depend on these names + signatures — they're as much a versioned API as `art.source(name).get/subscribe/refresh`.
>
> The `art.source`, `art.state`, and `art.theme` surfaces are equally stable (documented above). Anything not in this section or the source/state/theme surfaces is **internal** — don't rely on it from outside the bridge polyfill.

Inside the IIFE, after `init()`:

```js
// Sources
art.source(name).get();                  // current cached value (sync)
art.source(name).subscribe(fn);          // returns unsubscribe; fires on refresh
art.source(name).refresh();              // manual refetch; returns Promise

// Host introspection
art.host.kind;                           // 'ikenga' | 'browser' | 'preview-cli'
art.host.user;                           // identity, null in plain browser
art.host.usedFallback(name);             // true if this source fell back to mock
art.host.anyFallback();                  // true if any source did

// Persisted UI state — sort, filter, tab, date range
art.state.get(key);
art.state.set(key, value);
art.state.subscribe(key, fn);

// Theme — live view of the host theme. CSS already tracks it via mirrored
// `data-mode`/`data-theme` + `.dark` and the injected tokens; use this only
// when you need theme in JS (e.g. canvas/chart colors).
art.theme.mode;                          // 'light' | 'dark'
art.theme.theme;                         // 'A' | 'B' | 'C' (palette variant)
art.theme.density;                       // 'compact' | 'comfortable' | 'spacious'
art.theme.subscribe(fn);                 // returns unsubscribe; fires on every toggle

// Notes-back loop (host-mode only; no-op + clipboard fallback elsewhere)
art.notes.send(text, { selector });

// Pin request — UI handshake to add to activity bar
art.pin();

// Surface state to the shell so the agent can read it without polling the user.
// Stored per-pane in the shell's iframe registry; readable from a terminal via
// `iyke iframe-state <pane>`. Cheap, fire-and-forget — call freely.
art.publishState(key, value);
```

## Surfacing state to the shell (`publishState`)

`art.state.set` persists *inside the iframe* (host-mediated SQLite in Ikenga,
`localStorage` in plain browsers). It is **not** visible from outside the iframe
— neither the agent in chat nor `iyke iframe-state <pane>` can see what's
there. That's correct for sensitive or UI-only state (sort order, selected tab,
draft note text) but **wrong** for anything you want the conversation to react
to: decisions, selection, scrub position, multi-select sets, "user marked this
panel done."

`art.publishState(key, value)` solves this. It sends a fire-and-forget
`postMessage` to the parent in the shape the shell's iframe registry expects
(`{ __iyke: true, kind: 'state', payload: { key, value } }`). The shell stores
the latest value per `(pane, key)` pair; a terminal call to
`iyke iframe-state <pane>` returns the full state object as JSON, which the
agent can read on the next turn.

**When to publish**:

- Decision artifacts (this artifact is for the agent + user to converge on
  something): publish the full decision map whenever it changes.
- Multi-step artifacts: publish the current step + a per-step status bag.
- Selection-driven artifacts (tables, kanban, grid): publish the current
  selection ids so the agent knows what the user is looking at.
- Anything you'd otherwise re-ask the user about ("which row did you pick?").

**When *not* to publish**:

- Free-text drafts mid-edit (publish on blur or debounce, not on keystroke).
- Anything sensitive that shouldn't be in the host log surface (PII, secrets).
- Volatile values that change >10× per second (scroll position, animation
  frames) — publishState isn't rate-limited, but you'll spam the registry.

**Pattern** (place inside the React component that owns the state):

```jsx
useEffect(() => {
  art.publishState && art.publishState('decisions', {
    decisions: state,
    resolved: Object.values(state).filter(s => s.resolved).length,
    updated_at: new Date().toISOString(),
  });
}, [state, art]);
```

**Optional-chain the call** (`art.publishState && art.publishState(...)`) so
the artifact still runs against older bridge polyfills that don't expose it.

**Verifying from a terminal** (inside Ikenga):

```bash
iyke state --json | jq '.shell.panes.leaves[].id'    # find the pane id
iyke iframe-state <pane> --json | jq                  # read published state
```

Outside Ikenga the call is a no-op (parent === self → no parent to postMessage
to), so artifacts that use publishState still render fine in plain browsers
and claude.ai. No environment guard needed.

## Worked examples

Three references, in order of complexity. Open the source of each before writing your own.

- **`references/hello-world.html`** — minimal, single fetch source, ~150 lines. Smallest valid artifact. Read first.
- **`references/cfo-daily.html`** — financial dashboard, four data sources (supabase + sql + fetch + file), three refresh modes (interval / manual / watch), ~330 lines. Tests numerical/tabular data, KPI tiles, AR aging table with overdue highlighting, FX rates, cash-by-account bar chart.
- **`references/ceo-overview.html`** — exec digest, six sources spanning all four types (kpis supabase, agent_runs + calendar mcp, notifications sql, recent_docs file, team_signals fetch), ~470 lines. Tests narrative + structured signals + **cross-artifact links** (the cfo-bot agent run links to `cfo-daily.html`). The shape of most real-world artifacts beyond charts.

Use these as the canonical reference for **shape**, not styling. Copy structure, not visual choices. The polyfill block in each is identical — when `@ikenga/artifact` ships, all three will swap their inline polyfill for one CDN import without touching the App code.
