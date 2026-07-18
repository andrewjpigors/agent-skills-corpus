---
name: visual-explainer
description: "Agent skill that generates beautiful, self-contained HTML pages for visualizing C# / .NET architecture, library internals, dependency graphs, namespace hierarchies, and project structure. Use this skill when asked to create visual HTML diagrams, architecture reports, diff reviews, NuGet dependency audits, or when complex .NET information needs to be presented as styled interactive HTML pages."
license: MIT
compatibility: Designed for C# / .NET codebases. Requires Node.js 18+ for the validation script.
---

# Visual Explainer — C# / .NET Edition

Generate self-contained HTML files for technical diagrams, visualizations, and data tables — optimized for C# applications, .NET libraries, and the broader .NET ecosystem. Always open the result in the browser. Never fall back to ASCII art when this skill is loaded.

**Proactive table rendering.** When you're about to present tabular data as an ASCII box-drawing table in the terminal (comparisons, audits, feature matrices, status reports, any structured rows/columns), generate an HTML page instead. The threshold: if the table has 4+ rows or 3+ columns, it belongs in the browser. Don't wait for the user to ask — render it as HTML automatically and tell them the file path. You can still include a brief text summary in the chat, but the table itself should be the HTML page.

## C# / .NET Domain Knowledge

This skill is optimized for visualizing C# and .NET codebases. When analyzing or diagramming .NET projects, apply this domain knowledge:

### Common Architecture Patterns to Recognize

| Pattern | What to diagram | Approach |
|---|---|---|
| Clean Architecture / Onion | Concentric layers (Domain → Application → Infrastructure → Presentation) | CSS Grid cards with colored rings or nested borders |
| CQRS + MediatR | Command/Query separation, handler pipeline, behaviors | Mermaid flowchart with parallel branches |
| Repository + Unit of Work | DbContext, repositories, service layer | Mermaid class diagram or ER diagram |
| Middleware pipeline | ASP.NET Core request pipeline, middleware chain | Horizontal CSS pipeline (step boxes + arrows) |
| Dependency Injection | Service registration, lifetime scopes (Singleton/Scoped/Transient) | Data table with lifetime badges |
| Options pattern | `IOptions<T>`, configuration binding, validation | Data table mapping config sections to classes |
| Background services | `IHostedService`, `BackgroundService`, channels, queues | Mermaid sequence diagram or flowchart |
| Minimal APIs / Controllers | Route mapping, endpoint groups, filters | Data table or flowchart |
| Vertical Slice Architecture | Feature folders, each slice self-contained (handler + model + validator) | Mermaid flowchart showing request → slice → response |
| API Versioning | URL/header/query-string versioned endpoints | Data table: version → endpoints → deprecation status |
| Health checks | `/health`, `/ready`, dependency checks | Data table with check name, status badge, dependency |
| Rate limiting | ASP.NET Core rate limiting middleware, policies | Mermaid flowchart or data table with policy definitions |

### .NET-Specific Diagram Types

**Project dependency graph.** Visualize `.csproj` → `.csproj` references and NuGet package dependencies. Use Mermaid `graph TD` with `subgraph` blocks for solution folders. Color-code: project references in one accent, NuGet packages in another, test projects dimmed.

**Namespace hierarchy.** Show the namespace tree of an assembly. Use Mermaid `mindmap` rooted at the assembly name, branching into top-level namespaces and their children. Leaf nodes can show class counts.

**Class/interface relationships.** Inheritance chains, interface implementations, decorator stacks. Use Mermaid `classDiagram` for simple cases. For complex hierarchies with many members, use CSS Grid cards grouped by namespace with interface badges.

**Entity Framework model.** DbContext, entity classes, relationships (1:1, 1:N, N:N), owned types, value objects. Use Mermaid `erDiagram` with navigation properties as relationship labels.

**NuGet dependency audit.** Package name, installed version, latest version, vulnerability status. Use the data table template with status badges (✓ up-to-date, ⚠ outdated, ✗ vulnerable).

**ASP.NET middleware pipeline.** Ordered chain of middleware components from request entry to response exit. Use the CSS horizontal pipeline pattern with step boxes. Color-code by concern: auth (purple), logging (blue), error handling (red), business logic (green).

**Configuration binding map.** Show which `appsettings.json` sections bind to which `IOptions<T>` classes and where they're registered. Use a two-column data table: JSON path → C# type.

### Service-Specific Diagram Types

**Request lifecycle.** Full HTTP request flow from Kestrel to response. Use Mermaid `sequenceDiagram` with participants: Client, Kestrel, Middleware, Router, Auth, Handler, Database. Show the happy path and one error path. Color-code middleware participants by concern.

**Endpoint route table.** All registered endpoints with HTTP method, path, handler reference, auth policy, and rate-limiting policy. Use the data table template with HTTP method badges (colored: GET=green, POST=accent, PUT=orange, DELETE=red). Group by controller/feature area.

**Middleware pipeline.** Ordered chain from `UseExceptionHandler()` to `MapControllers()`. Use the CSS horizontal pipeline pattern. Each step shows: order position, extension method name (e.g., `UseAuthentication()`), and the concern category. Critical ordering constraints (auth before authz, CORS before routing) should be called out with callout boxes.

**DI service registration map.** Which services are registered with which lifetime (Singleton/Scoped/Transient) and their implementation type. Use a data table with lifetime badges color-coded: Singleton=domain-1, Scoped=domain-2, Transient=domain-3.

**Configuration binding map.** Which `appsettings.json` sections bind to which `IOptions<T>` / `IOptionsSnapshot<T>` / `IOptionsMonitor<T>` classes. Use a two-column data table: JSON path → C# type, with a third column for environment variable overrides (`ASPNETCORE_*`, custom env vars).

**Health check dashboard.** Health check name, status (Healthy/Degraded/Unhealthy), dependencies checked, timeout. Use the data table template with status badges.

### C# Code in Diagrams

- **Monaco Editor default language**: Always use `data-language="csharp"` for code samples unless the code is explicitly another language (JSON, XML, YAML, SQL).
- **File extensions to expect**: `.cs`, `.csproj`, `.sln`, `.props`, `.targets`, `appsettings.json`, `Program.cs`, `Startup.cs`.
- **Namespace display**: Show fully qualified names in diagram nodes only when disambiguation is needed. Prefer short class names with namespace as a subtitle or badge.
- **Generic types**: Display `IRepository<Order>` not `IRepository<T>` when the concrete usage is known. In Monaco code samples, keep the generic form.
- **Access modifiers**: In class diagrams, use `+` public, `-` private, `#` protected, `~` internal as prefix markers on member lists.
- **NuGet packages**: When referencing packages, show the package name in `<code>` tags styled with the accent color. Link to nuget.org when useful.
- **Project files**: Reference `.csproj` files with VS Code links pointing to the project file, not the directory.
- **HTTP method badges**: In endpoint `table` sections, show HTTP methods as colored inline badges: GET (green), POST (accent), PUT (orange), DELETE (red).
- **Middleware ordering**: When showing middleware pipeline, always reflect the actual registration order from `Program.cs`. Incorrect ordering (e.g., auth after routing) is a critical visualization error.
- **Configuration paths**: Show `appsettings.json` paths in `<code>` with colon separators (e.g., `Logging:LogLevel:Default`). Show environment variable overrides with double-underscore format (e.g., `Logging__LogLevel__Default`).

## Workflow

### 0. Research (before you diagram)

Before generating any visualization, **research the .NET APIs and patterns** involved using the Microsoft Learn MCP tools. This ensures diagrams are accurate, use correct type names, and reflect current best practices.

**When to research:**
- Diagramming a library or framework you haven't fully read yet — search for its architecture overview on MS Learn
- Showing API surface (classes, interfaces, extension methods) — verify actual type names and namespaces
- Documenting configuration / options patterns — fetch the official configuration docs to get correct property names
- Comparing alternatives — search MS Learn for the recommended approach before listing trade-offs
- Explaining middleware, DI lifetimes, hosting models — fetch the authoritative docs rather than relying on memory

**How to research (MCP tools):**

1. **`microsoft_docs_search`** — Start here. Search for the .NET API, pattern, or concept. Returns up to 10 relevant content chunks with article titles and URLs. Use specific queries: `"IHttpClientFactory dependency injection"` beats `"http client"`.

2. **`microsoft_code_sample_search`** — Search for official code examples. Pass `language: "csharp"` to filter results. Use when you need realistic usage patterns for Monaco Editor code samples in your diagrams.

3. **`microsoft_docs_fetch`** — Follow up on high-value pages found by search. Fetches the complete page as markdown. Use when search results are truncated or when you need full step-by-step procedures, configuration tables, or API reference details.

**Research workflow:**
```
Search MS Learn for the topic
  → Identify 1-2 authoritative pages
  → Fetch full content of the best page
  → Extract: correct type names, namespaces, patterns, configuration keys
  → Use these in your diagram nodes, code samples, and descriptions
```

**What to extract for diagrams:**
- **Correct fully-qualified type names** (e.g., `Microsoft.Extensions.DependencyInjection.IServiceCollection` not a guess)
- **Extension method signatures** for DI registration code samples
- **Configuration section paths** (e.g., `"Logging:LogLevel:Default"`)
- **Recommended patterns** and anti-patterns noted in the docs
- **Version-specific behavior** — note which .NET version introduced an API if relevant

Do NOT skip research and generate diagrams from memory alone. A beautiful diagram with wrong type names or outdated patterns is worse than an ugly accurate one.

### 1. Think (5 seconds, not 5 minutes)

Before writing HTML, commit to a direction. Don't default to "dark theme with blue accents" every time.

**Who is looking?** A developer understanding a system? A PM seeing the big picture? A team reviewing a proposal? This shapes information density and visual complexity.

**What type of diagram?** Architecture, flowchart, sequence, data flow, schema/ER, state machine, mind map, data table, timeline, or dashboard. Each has distinct layout needs and rendering approaches (see Diagram Types below).

**Service or library?** If the codebase is a service (has HTTP endpoints, middleware pipeline, `Program.cs` with `WebApplication.CreateBuilder` or `Host.CreateBuilder`), use the service-report flow. If it's a library (exposes a public API surface, is consumed as a NuGet package, has no host builder), use the library-report flow. Mixed projects (e.g., a library that also ships a host) — pick the dominant concern or generate both reports.

**Visual is always default.** Even essays, blog posts, and articles get visual treatment — extract structure into cards, diagrams, grids, tables.

Prose patterns (lead paragraphs, pull quotes, callout boxes) are **accent elements** within visual pages, not a separate mode. Use them to highlight key points or provide breathing room, but the page structure remains visual.

For prose accents, use `callout` and `markdown` section types. For everything else, use the standard template workflow with aesthetic directions below.

**What aesthetic?** Pick one and commit. The constrained aesthetics (Blueprint, Editorial, Paper/ink) are safer — they have specific requirements that prevent generic output. The flexible ones (IDE-inspired) require more discipline.

**Constrained aesthetics (prefer these):**
- Blueprint (technical drawing feel, subtle grid background, deep slate/blue palette, monospace labels, precise borders)
- Editorial (serif headlines like Instrument Serif or Crimson Pro, generous whitespace, muted earth tones or deep navy + gold)
- Paper/ink (warm cream `#faf7f5` background, terracotta/sage accents, informal feel)
- Monochrome terminal (green/amber on near-black, monospace everything, CRT glow optional)

**Flexible aesthetics (use with caution):**
- IDE-inspired (borrow a real, named color scheme: Dracula, Nord, Catppuccin Mocha/Latte, Solarized Dark/Light, Gruvbox, One Dark, Rosé Pine) — commit to the actual palette, don't approximate
- Data-dense (small type, tight spacing, maximum information, muted colors)

**Explicitly forbidden:**
- Neon dashboard (cyan + magenta + purple on dark) — always produces AI slop
- Gradient mesh (pink/purple/cyan blobs) — too generic
- Any combination of Inter font + violet/indigo accents + gradient text

Vary the choice each time. If the last diagram was dark and technical, make the next one light and editorial. The swap test: if you replaced your styling with a generic dark theme and nobody would notice the difference, you haven't designed anything.

### 2. Structure — Template-Based Workflow

**Use the template.** All diagrams are generated using the HTML template at `./assets/template.html`. Your job is to produce a **JSON data object** — the template handles all CSS, JS, rendering, and interactivity.

**Read the section types reference** at `./references/section-types.md` before composing your JSON. It documents every supported section type with its schema, examples, and composition guidelines.

**How to generate:**
1. Copy `./assets/template.html` to the output location (e.g., `diagrams/my-report.html`)
2. Replace the `const DATA = {...};` line with your JSON payload
3. The HTML file is self-contained — opens in any browser with no build step

**Choosing a palette:** Set `"palette"` in the JSON to one of the 6 named palettes. See `./references/palette-registry.md` for visual reference.

| Palette | Vibe | Use for |
|---|---|---|
| `cool-slate` | Technical, blue-gray | Architecture reports, system overviews |
| `warm-terracotta` | Earthy, editorial | Library walkthroughs, documentation |
| `forest` | Natural, green | Environment/infrastructure diagrams |
| `ocean` | Calm, teal | API reports, service documentation |
| `dusk` | Dramatic, purple | Feature specs, design proposals |
| `sand` | Desert minimalism | Configuration guides, data tables |

**Choosing section types:** Read `./references/section-types.md` for the full catalog. Common patterns:

| Diagram need | Section types to use |
|---|---|
| Architecture overview | `hero` → `callout` → `mermaid` → `card` × N → `file-inventory` |
| Data flow / pipeline | `hero` → `pipeline` → `mermaid` → `card` × N |
| Type inventory | `hero` → `kpi-row` → `table` → `file-inventory` |
| Feature comparison | `hero` → `table` → `callout` |
| Service report | `hero` → `mermaid` (request flow) → `table` (endpoints) → `pipeline` (middleware) → `file-inventory` |

**For slide deck presentations** (when `--slides` flag is present or `/generate-slides` is invoked): the template system does not apply to slides — read `./assets/slide-deck.html` and `./references/slide-patterns.md` instead. (Note: the template also supports a lightweight `?slides` query-string mode that presents sections as slides — see `./references/section-types.md` for details.)

**Navigation** is automatic — the template generates a sidebar TOC from any section with a `heading` field. On narrow screens it collapses to a horizontal bar.

**Choosing a rendering approach — all rendered via JSON section types:**

| Diagram type | Section type | Why |
|---|---|---|
| Architecture (text-heavy) | `hero` + `card` + `grid` | Rich card content (descriptions, code, tool lists) |
| Architecture (topology-focused) | `mermaid` | Visible connections need automatic edge routing |
| Flowchart / pipeline | `mermaid` or `pipeline` | `pipeline` for simple linear flows, `mermaid` for branching |
| Sequence diagram | `mermaid` | Lifelines, messages, activation boxes |
| Data flow | `mermaid` with edge labels | Connections and data descriptions |
| ER / schema diagram | `mermaid` | Relationship lines between entities |
| State machine | `mermaid` | State transitions with labeled edges |
| Data table | `table` | Semantic markup, accessibility, copy-paste |
| KPI / metrics | `kpi-row` | Quick-glance numeric summary |
| File listings | `file-inventory` | Collapsible file lists with VS Code links |

**Mermaid theming:** Always use `theme: 'base'` with custom `themeVariables` so colors match your page palette. Use `layout: 'elk'` for complex graphs (requires the `@mermaid-js/layout-elk` package — see `./references/libraries.md` for the CDN import). Override Mermaid's SVG classes with CSS for pixel-perfect control. See `./references/libraries.md` for full theming guide.

**Mermaid zoom controls:** The template automatically adds zoom controls (+/−/reset/focus buttons), Ctrl/Cmd+scroll zoom, and a `.mermaid-inner` wrapper to every `mermaid` section. The **focus button** (⛶) opens a fullscreen overlay that auto-fits the SVG to maximum viewport size — essential for complex .NET dependency graphs and architecture diagrams. No manual setup needed.

**Mermaid CSS class collision constraint:** Never define `.node` as a page-level CSS class. Mermaid.js uses `.node` internally on SVG `<g>` elements with `transform: translate(x, y)` for positioning. Page-level `.node` styles (hover transforms, box-shadows) leak into diagrams and break layout. Use the namespaced `.ve-card` class for card components instead. The only safe way to style Mermaid's `.node` is scoped under `.mermaid` (e.g., `.mermaid .node rect`).

**AI-generated illustrations (optional).** If image generation tools are available (e.g., via MCP servers or built-in capabilities), optionally generate illustrations and embed as base64 data URIs in `markdown` section content.

**When to use:** Hero banners that establish the page's visual tone. Conceptual illustrations for abstract systems that Mermaid can't express (physical infrastructure, user journeys, mental models). Educational diagrams that benefit from artistic or photorealistic rendering. Decorative accents that reinforce the aesthetic.

**When to skip:** Anything Mermaid or CSS handles well. Generic decoration that doesn't convey meaning. Data-heavy pages where images would distract. Always degrade gracefully — if image generation isn't available, skip images without erroring. The page should stand on its own with CSS and typography alone.

**Prompt craft:** Match the image to the page's palette and aesthetic direction. Specify the style (3D render, technical illustration, watercolor, isometric, flat vector, etc.) and mention dominant colors from your CSS variables. Use landscape aspect ratios for hero banners, square for inline illustrations. Keep prompts specific — "isometric illustration of a message queue with cyan nodes on dark navy background" beats "a diagram of a queue."

### 3. Style

The template handles all styling automatically via the named palette. Focus on:

- **Choosing the right palette** for the content's tone (see palette table above)
- **Using domain slots consistently** — assign `domain-1` through `domain-5` to specific concerns in your `legend`, then use matching `domain` fields on `card` sections
- **Varying visual weight** — use `hero` for the primary overview, `card` for detailed type descriptions, `callout` for important notes, `collapsible` for supplementary content
- **Writing good Markdown content** — the template renders Markdown via marked.js, so use `**bold**`, `` `code` ``, `[links](url)`, and lists naturally in content fields

### 4. Deliver

**To generate the final HTML file:**

1. Copy the template: `Copy-Item .agents/skills/visual-explainer/assets/template.html diagrams/output-name.html`
2. Replace the DATA placeholder in the copied file with your JSON payload
3. The `const DATA = {...};` line is the only thing that changes between diagrams

**Output location:** Write to `./diagrams/`. Use a descriptive filename: `modem-architecture.html`, `pipeline-flow.html`.

**Open in browser:**
- macOS: `open ./diagrams/filename.html`
- Linux: `xdg-open ./diagrams/filename.html`
- Windows: `start ./diagrams/filename.html`

**Tell the user** the file path so they can re-open or share it.

## Diagram Types

All diagram types below are rendered via the template's JSON section types. See `./references/section-types.md` for full schemas.

### Architecture / System Diagrams
Two approaches depending on what matters more:

**Text-heavy overviews** (card content matters more than connections): Use `card` sections with inner grids. Cards support rich descriptions, code references, file links, badges, and nested items. Combine with `hero` for overview and `pipeline` for process flows.

**Topology-focused diagrams** (connections matter more than card content): Use `mermaid` sections. A `graph TD` or `graph LR` with custom `themeVariables` produces proper diagrams with automatic edge routing. Use when the point is showing how components connect.

### Flowcharts / Pipelines
Use `mermaid` sections for complex flows with branches and decision points. Use `pipeline` sections for simple linear step sequences (build pipelines, middleware chains, deployment stages).

### Sequence / Data Flow / ER / State Diagrams
Use `mermaid` sections. Mermaid supports `sequenceDiagram`, `erDiagram`, `stateDiagram-v2`, `mindmap`, and `flowchart` syntaxes — all rendered with automatic layout.

**`stateDiagram-v2` label caveat:** Transition labels have a strict parser — colons, parentheses, `<br/>`, HTML entities, and most special characters cause silent parse failures ("Syntax error in text"). If your labels need any of these (e.g., `cancel()`, `curate: true`, multi-line labels), use `flowchart LR` instead with rounded nodes and quoted edge labels (`|"label text"|`). Flowcharts handle all special characters and support `<br/>` for line breaks. Reserve `stateDiagram-v2` for simple single-word or plain-text labels.

### Data Tables / Comparisons / Audits
Use `table` sections. The template renders semantic `<table>` elements with sticky headers, alternating row backgrounds, hover highlights, and responsive overflow handling.

**Use proactively.** Any time you'd render an ASCII box-drawing table in the terminal, generate an HTML table instead. This includes: NuGet dependency audits, API endpoint inventories, DI service registration tables, configuration binding maps, test result summaries, feature comparisons — any structured rows and columns.

### Timeline / Roadmap Views
Use `pipeline` sections for linear timelines. For branching timelines, use `mermaid` with a `graph TD` or `gitGraph`.

### Dashboard / Metrics Overview
Use `kpi-row` for hero metrics, `card` sections with inner grids for detail cards. For charts (bar, line, pie), use Chart.js via CDN (see `./references/libraries.md`).

## Slide Deck Mode

Generate magazine-quality slide deck presentations as self-contained HTML files. Use **only when explicitly requested** — `/generate-slides`, `--slides` flag on an existing prompt, or natural language like "as a slide deck." Never auto-select slide format.

**Before generating**, read `./assets/slide-deck.html` (reference template demonstrating all 10 slide types) and `./references/slide-patterns.md` (engine CSS, layouts, transitions, presets).

### Slide Types

| Type | Use for | Layout |
|------|---------|--------|
| Title | Opening slide | Centered display text + subtitle |
| Section Divider | New topic transitions | Large section number + heading |
| Content | Text + bullet points | Heading + body, optional aside |
| Split | Two-column comparisons | 50/50 or 60/40 grid |
| Diagram | Mermaid charts | Full-width diagram with caption |
| Dashboard | KPI metrics | Card grid with hero numbers |
| Table | Structured data | Scrollable table with header |
| Code | Code snippets | Mono code block with file header |
| Quote | Key insights | Large serif italic with attribution |
| Full-Bleed | Visual impact | Background image or gradient fills viewport |

### Slide Routing

When `--slides` is detected or `/generate-slides` is invoked:
1. Read `./assets/slide-deck.html` and `./references/slide-patterns.md`
2. Plan the deck (inventory → map → layout → images) per the planning workflow in slide-patterns.md
3. Pick a preset: Midnight Editorial, Warm Signal, Terminal Mono, or Swiss Clean
4. Typography is 2–3× larger than scrollable pages (80–120px display, 28–48px headings, 16–24px body)
5. Include the SlideEngine JS for keyboard/touch/wheel navigation, progress bar, and nav dots
6. Use cinematic transitions (fade + translateY + scale on entrance)
7. Vary composition across slides — don't repeat the same layout three times in a row

### Visual Richness

- **Per-slide background variation**: Shift gradient direction or glow position on each slide
- **Decorative SVG accents**: Corner marks, divider lines, quote marks — lightweight visual interest
- **Proactive imagery**: If `surf` CLI is available, generate images for title and full-bleed slides
- **Mermaid at presentation scale**: Use fontSize 18px, 2px edges, max 8 nodes per diagram
- **autoFit()**: Post-render function auto-scales Mermaid SVGs, KPI values, and long quotes

## File Path Links

The template automatically generates **clickable VS Code links** (`vscode://file/`) from the `path` field on file entries in `card.fileLinks`, `table` file links, and `file-inventory` groups. Just provide absolute paths in your JSON — the template handles URI construction, backslash normalization, and link styling.

- Resolve all paths to **absolute** using the repository root before generating the JSON.
- With line number: add `:{line}` to the path string (e.g., `"D:/repo/src/Auth.cs:42"`).

## Prose Accent Elements

Use `callout` and `markdown` section types for prose elements — lead paragraphs, pull quotes, callout boxes. They provide breathing room between diagram-heavy sections.

**When to use:**
- **Lead paragraph**: Opening of a major section — use `markdown` with emphasized text
- **Pull quote**: Highlight a key insight — use `callout` with `accent` style
- **Callout boxes**: Warnings, tips, notes — use `callout` with `icon` and `variant` fields
- **Section dividers**: Between major topic shifts — add a `markdown` section with `---`

**When NOT to use**: Don't turn a technical diagram page into a blog post. If the page is primarily about architecture or data, keep prose minimal and use cards/tables instead.

## Documentation

When generating pages that document C#/.NET features, APIs, or architecture, map content types to visual treatments:

| Content type | Visual treatment |
|---|---|
| Feature descriptions | Cards with accent borders, grouped by category |
| Step-by-step workflows | Mermaid flowchart or CSS pipeline with numbered steps |
| API reference | Data table with method signatures, parameters, return types |
| Configuration options | Two-column table: setting → description + default value |
| Comparison (before/after) | Side-by-side panels with colored headers |
| Migration guides | Timeline or numbered step cards with code snippets |
| Decision logs | Cards with decision, rationale, and alternatives |

## Implementation Plans

When generating pages that show implementation plans for C#/.NET features:

- **Don't dump full files** — show structure with function/method signatures and brief inline comments
- **Key snippets only** — 10-20 line C# code blocks that demonstrate the pattern, not the full implementation
- **Use pseudocode for complex logic** — real code for API surface (interfaces, DTOs, service contracts)
- **State machines for behavior** — if the feature has multiple modes or states, use a Mermaid stateDiagram or flowchart
- **Edge case tables** — tabular format with scenario, expected behavior, and handling approach
- **Code blocks must preserve whitespace** — the template handles `white-space: pre-wrap` automatically in `markdown` sections

## File Structure

Every diagram is a single self-contained `.html` file based on the template at `./assets/template.html`. The template contains all CSS, JS, palettes, and rendering logic. The only thing that varies between diagrams is the `DATA` JSON object.

**Generation process:**
1. Copy `./assets/template.html` to the output location
2. Find the line `const DATA = {...};` and replace it with your JSON payload
3. The file is ready — opens in any browser

**Template structure:**
```
template.html
├── <style>        — All CSS (themes, components, responsive, mermaid)
├── <body>         — Focus overlay + app container (populated by JS)
├── <script>       — DATA placeholder (replaced per diagram)
├── <script>       — PALETTES object (6 named palettes)
├── <script src>   — marked.js CDN (Markdown parser)
├── <script>       — Render engine (section renderers, scroll spy, zoom)
└── <script module> — Mermaid CDN import + initialization
```

See `./references/section-types.md` for the complete JSON schema and section type catalog.

## Quality Checks

Before delivering, verify:
- **JSON structure valid**: The DATA object must be valid JSON. Validate section types match the types in `./references/section-types.md`.
- **Template copied correctly**: The output file must be an exact copy of `./assets/template.html` with only the `const DATA = {...};` line replaced.
- **Both themes**: Toggle your OS between light and dark mode. Both should look intentional, not broken.
- **Information completeness**: Does the diagram actually convey what the user asked for? Pretty but incomplete is a failure.
- **Mermaid syntax**: If using `mermaid` sections, verify the mermaid code is syntactically correct. Zoom controls, focus overlay, and panning are handled by the template automatically.
- **Domain colors consistent**: If you define legend entries in `hero`, use the same `domain-*` slots on related `card` sections throughout.
- **VS Code file links**: File references in `fileLinks` arrays must use absolute paths. The template generates `vscode://file/` links automatically.
- **Markdown content**: Content fields support full Markdown via marked.js. Use `**bold**`, `` `code` ``, lists, and links naturally.
- **File opens cleanly**: No console errors, no broken font loads, no layout shifts.

### Automated Validation

Run the validator script after generating any diagram:

```bash
node .agents/skills/visual-explainer/scripts/validate-diagram.mjs diagrams/your-output.html
```

The validator extracts the `const DATA = {...}` JSON from the HTML file and validates: top-level schema (title, palette, sections array), per-section-type field requirements (e.g., mermaid must have `code`, table must have `headers` and `rows`), and common mistakes (CSS `var()` in mermaid code, missing file paths). Fix any reported errors before delivering.

## Anti-Patterns (AI Slop)

These patterns are explicitly forbidden. They signal "AI-generated template" and undermine the skill's purpose of producing distinctive, high-quality diagrams. Review every generated page against this list.

### Typography

**Forbidden fonts as primary `--font-body`:**
- Inter — the single most overused AI default
- Roboto, Arial, Helvetica — generic system fallbacks promoted to primary
- system-ui, sans-serif alone — no character, no intent

**Required:** The template ships with 6 named palettes — use `./references/palette-registry.md` to pick. Font pairings are built into each palette.

### Color Palette

**Forbidden accent colors:**
- Indigo-500/violet-500 (`#8b5cf6`, `#7c3aed`, `#a78bfa`) — Tailwind's default purple range
- The cyan + magenta + pink neon gradient combination (`#06b6d4` → `#d946ef` → `#f472b6`)
- Any palette that could be described as "Tailwind defaults with purple/pink/cyan accents"

**Forbidden color effects:**
- Gradient text on headings (`background: linear-gradient(...); background-clip: text;`) — this screams AI-generated
- Animated glowing box-shadows on cards (`box-shadow: 0 0 20px var(--glow); animation: glow 2s...`)
- Multiple overlapping radial glows in accent colors creating a "neon haze"

**Required:** Use the 6 named palettes in `./references/palette-registry.md` (cool-slate, warm-terracotta, forest, ocean, dusk, sand) or derive from real IDE themes (Dracula, Nord, Solarized, Gruvbox, Catppuccin). Accents should feel intentional, not default.

### Section Headers

**Forbidden:**
- Emoji icons in section headers (🏗️, ⚙️, 📁, 💻, 📅, 🔗, ⚡, 🔧, 📦, 🚀, etc.)
- Section headers that all use the same icon-in-rounded-box pattern

**Required:** The template uses `ve-card__label` with colored dot indicators and numbered section headings. If an icon is genuinely needed, use an inline SVG that matches the palette — not emoji.

### Layout & Hierarchy

**Forbidden:**
- Perfectly centered everything with uniform padding
- All cards styled identically with the same border-radius, shadow, and spacing
- Every section getting equal visual treatment — no hero/primary vs. secondary distinction
- Symmetric layouts where left and right halves mirror each other

**Required:** Vary visual weight. Hero sections should dominate (larger type, more padding, accent-tinted background). Reference sections should feel compact. Use the depth tiers (hero → elevated → default → recessed). Asymmetric layouts create interest.

### Template Patterns

**Forbidden:**
- Three-dot window chrome (red/yellow/green dots) on code blocks — this is a cliché
- KPI cards where every metric has identical gradient text treatment
- "Neon Dashboard" as an aesthetic choice — it always produces generic results
- Gradient meshes with pink/purple/cyan blobs in the background

**Required:** Code blocks use a simple header with filename or language label. KPI cards vary by importance — hero numbers for the primary metric, subdued treatment for supporting metrics. Pick aesthetics with natural constraints: Blueprint (must feel technical/precise), Editorial (must have generous whitespace and serif typography), Paper/ink (must feel warm and informal).

### The Slop Test

Before delivering, apply this test: **Would a developer looking at this page immediately think "AI generated this"?** The telltale signs:

1. Inter or Roboto font with purple/violet gradient accents
2. Every heading has `background-clip: text` gradient
3. Emoji icons leading every section
4. Glowing cards with animated shadows
5. Cyan-magenta-pink color scheme on dark background
6. Perfectly uniform card grid with no visual hierarchy
7. Three-dot code block chrome

If two or more of these are present, the page is slop. Regenerate with a different aesthetic direction — Editorial, Blueprint, Paper/ink, or a specific IDE theme. These constrained aesthetics are harder to mess up because they have specific visual requirements that prevent defaulting to generic patterns.

## Library Reports

For .NET library analysis, NuGet package walkthroughs, and class library architecture:

1. **Research**: Use `microsoft_docs_search` and `microsoft_docs_fetch` to pull official documentation for the library. Verify type names, API surface, and recommended patterns.
2. **Template**: Use `./assets/template.html` with the standard JSON workflow. Pick a palette from `./references/palette-registry.md`.
3. **Validation**: Run `node .agents/skills/visual-explainer/scripts/validate-diagram.mjs diagrams/output.html`

### Library Report Section Pattern

Compose the JSON with these section types in order:

| Section | Type | Content |
|---|---|---|
| Overview | `hero` | Package name, framework, purpose, key dependencies as badges, KPIs (files, types, namespaces) |
| Architecture | `mermaid` | Topology diagram for 5+ interacting components |
| Components | `card` × N | One card per major class/interface with namespace, public members, file links |
| Design Principles | `callout` or `markdown` | .NET-idiomatic patterns (DI, options, decorators, `CancellationToken`) |
| Alternatives | `table` | Competing packages with status badges: current (green), alternative (accent), deprecated (red) |
| Code Sample | `markdown` | C# usage example in fenced code block. Use `microsoft_code_sample_search` for official examples first |
| File Inventory | `file-inventory` | All `.cs` files with absolute paths (auto-generates VS Code links). Group by namespace |

## Service Reports

For ASP.NET Core APIs, gRPC services, background workers, and hosted services:

1. **Research**: Use `microsoft_docs_search` and `microsoft_docs_fetch` to pull official ASP.NET Core documentation. Verify middleware ordering, auth configuration, and endpoint routing.
2. **Template**: Use `./assets/template.html` with the standard JSON workflow. Pick a palette from `./references/palette-registry.md`.
3. **Validation**: Run `node .agents/skills/visual-explainer/scripts/validate-diagram.mjs diagrams/output.html`

### Service Report Section Pattern

| Section | Type | Content |
|---|---|---|
| Overview | `hero` | Service name, hosting model, framework, ports, entry point. KPIs (endpoints, middleware, services) |
| Request Flow | `mermaid` | Sequence or flowchart: request → middleware → routing → auth → handler → response. Color by concern |
| Endpoints | `table` | HTTP Method (badge), Route, Handler, Auth Required, Description. Group by controller |
| Middleware | `pipeline` | Ordered chain with step number, name, description. Color by concern: auth, logging, CORS, routing |
| Configuration | `table` | `appsettings.json` paths → `IOptions<T>` classes, with defaults and env var overrides |
| Code Sample | `markdown` | `Program.cs` with DI registration, middleware ordering, endpoint definition |
| File Inventory | `file-inventory` | All `.cs` files with absolute paths. Group by area (Controllers/, Services/, Middleware/) |
