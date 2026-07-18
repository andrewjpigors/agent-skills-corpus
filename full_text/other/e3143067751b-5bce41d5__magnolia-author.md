---
name: magnolia-author
description: Author pages on Magnolia author instances. Use when the user asks to create, update, publish, or read pages or components on a Magnolia CMS. Backed by the magnolia-author MCP server.
metadata:
  tags: [magnolia, cms, authoring]
  category: cms
---

# magnolia-author

End-to-end skill for authoring on Magnolia CMS instances via the
magnolia-author MCP server. Generic: no assumptions about specific
component libraries, page templates, or client conventions. Discover
those at runtime via `list_templates`, `get_template`, `get_dialog`.

## When to use

- "Create a page about X on [client] [tier] author"
- "Add a [component] to /some/page"
- "Swap / update the image on a component"
- "What components can go in [area] of [template]?"
- "Show me the fields of [component]"
- "List page templates on [instance]"
- "Publish /path/to/page"

## Tool-choice nudges

- For "what pages are under `/X`?" → use `list_pages(parent_path='/X')`.
  Don't reach for `search_workspace` unless you need a fulltext match
  across unknown locations.
- For "show me the structure of `/X/Y`" → use `read_node(path='/X/Y')`.
- Use `search_workspace` only when you genuinely need fulltext matching
  across an unknown subtree. On instances exposing the JCR query endpoint
  it's an indexed sub-second search (`method: "indexed"` in the response);
  otherwise it falls back to a BFS that can take minutes — bounded by
  `max_nodes_scanned` and a 600s MCP timeout.
- Your gateway may ALLOWLIST a subset of this skill's tools — a tool named
  in this document can be absent from your tool list. If it is absent, it
  is NOT a prompt: never call `get_prompt`/`list_prompts` with a tool name.
  Fall back instead: no `get_component_definition` → `get_template` on the
  component id (areas) + `get_dialog` (fields); no `scan_components` →
  `read_node(structure_only=True)` on a live page; no `verify_render` →
  fetch the page URL and eyeball the HTML.
- Avoid `verbose=True` on `get_template`/`get_component_definition` unless
  you are debugging a definition: the raw JSON Schema for a container can
  be enormous, and the default (slim) response already carries everything
  needed for authoring.

## Hard rules

> **0. NEVER dump the page structure to the user.** Tool results — the
> component tree, per-component lists, `structure`, `components_results`,
> theme/area breakdowns, "Layer / Component / Properties" tables, the
> verification read — are FOR YOU, not the user. The final message to the
> user is the **preview URL + one short sentence**, nothing else (see
> "Reply tone"). Do NOT narrate the build ("All 26 components created… let
> me verify the full structure:" followed by a tree). The user can open the
> page; a wall of node names is noise. Expand ONLY if they explicitly ask
> "show me the structure / what did you do step by step". This rule
> overrides any instinct to show your work.

1. **Discover before writing.** A target instance's component library,
   page templates, allowed components per area, and field schemas are
   unknown until queried. Run `list_templates` / `get_template` /
   `get_dialog` for any component you haven't authored in this session
   before calling `add_component` or `set_properties`. The renderer
   silently ignores unknown property names — bugs only show on the
   rendered page. **Batch discovery**: when you know all the components
   you'll use, call `get_dialogs(dialog_ids=[...])` once instead of N
   sequential `get_dialog` calls, OR place several `get_dialog` calls in
   parallel in a single turn (most MCP clients support parallel tool calls).
   For a one-shot map of an unfamiliar instance's whole component
   library — every component actually used, its field count, and which
   carry switchableFields — run `scan_components(instance)` once and work
   from its cached profile.

1b. **Put content in the right place — don't default to the site root.**
   Before `create_page` (or creating a workspace item), work out where this
   TYPE of content belongs on this instance. Different types have a home:
   news, events, projects, etc. each live in a specific section — and some
   aren't pages at all but entries in a dedicated workspace (e.g. events).
   Discover it with the tools: `list_pages(parent_path=<site root>)` +
   `list_workspaces` / `browse_workspace` to see where similar content
   already sits, then `read_node` an existing example to copy its parent
   path + shape. (The per-instance guide `references/<instance-key>.md` has
   the placement map too, but it's a SKILL file — load it with `skill_view`
   if your harness supports it; it is NOT an MCP resource, so don't try to
   read it via the server's `read_resource`/`list_resources`.) State the
   resolved target path back to the user before creating.

2. **Never guess DAM paths.** Always `list_dam_folder(folder_path="")`
   or `search_dam(query, root_path="")` to find an asset's path / uuid.
   Inventing paths produces 404s.

2a. **"Page header" = the site's hero/banner component, NOT the `header`
   JCR area.** When the user says "add X to the page header", they mean
   the visual hero/banner at the top of the page — which on most sites
   is a dedicated component (banner / page-banner / hero / pageHeader),
   often sitting in a dedicated top area (`intro`, `banner`, `main`),
   NOT the `header` JCR area (that's usually reserved for site-wide
   header inheritance with `allowed_components: []`). The component id
   and area name are **client-specific — discover them, don't assume**:
   run `scan_components(instance)` or read a live page
   (`read_node(<existing page>, depth=3, structure_only=True)`) to see
   what the hero component is called and where it lives, then record it in
   that instance's guide (`references/<instance-key>.md`). Real-world
   example: a site may have no `pageHeader` at all — its hero is a
   `page-banner` component sitting in an `intro` area.

2b. **Vision needs local files, not author URLs.** Magnolia `/.imaging/`
   thumbnails and any author-instance URL require authentication a vision
   tool usually doesn't have, and will 401 silently. Always
   `download_dam_asset(dam_path=...)` first and pass the returned local cache
   path to your agent's vision/multimodal tool. This applies whether the URL
   came from `search_dam`, a DAM browse, or a `read_node` result — never feed
   auth-protected Magnolia URLs to a vision tool directly.

3. **Image fields go through `set_component_image`.** Many Magnolia
   `damLinkField` implementations expect a bare `jcr:<UUID>` string plus
   a sibling `image_alt` textField. `set_component_image` writes both
   atomically and handles both shapes correctly.

4. **Prod is gated.** When `is_prod: true` in `list_instances`, confirm
   with the user before any write call, even when the default policy is
   "write directly".

5. **Delete is dry-run by default.** `delete_node` with `confirm=False`
   shows what would be removed. Pass `confirm=True` only after the user
   acknowledges.

6. **Never auto-publish.** `publish_page` runs only on explicit ask.

7. **Read shallow first.** Use `read_node(properties_only=True)` to
   inspect a single node's fields. Use `read_node(depth=2)` to map a
   page. Deep grids and nested containers may require reading specific
   sub-paths directly rather than raising the depth.

8. **Heed validation warnings.** `add_component` and `set_properties`
   return a `warnings` array when supplied property names aren't
   declared on the component's dialog. The write still succeeds but the
   renderer will likely ignore those properties. Re-author with the
   correct field names from `get_dialog`.

8a. **When a page area's `allowed_components` is narrow, the real
    content usually nests inside a layout/container component.** Many
    sites restrict the top page area to a single layout wrapper
    (container / section / grid / columns) and allow the rich component
    set only *inside* that wrapper's child areas. Don't conclude "the
    component isn't allowed here" from the page area alone — drill in:
    `get_template(<wrapper_id>)` (or read a live page) to find the
    wrapper's child area and what it allows, then author
    `add_component(parent_path=<wrapper_path>, area_name=<child area>, ...)`.
    The wrapper id and child-area names are client-specific — discover
    them and record them in `references/<instance-key>.md`. Real-world
    example: a site whose top page area allows only a single `container`
    component, with all content nested inside it.

9. **Container components store items as child nodes/components, not as
   array properties.** Heuristic: a component whose dialog has few or
   zero fields. You CANNOT pass `items: [{...}, ...]` as a property —
   Magnolia silently rejects structured values (the MCP now raises
   `StructuredValueError`).

   **Discovery path — try in this order:**

   1. **`get_component_definition(container_template_id)` FIRST.** Most
      container components declare a child area in their template
      definition. For example, `get_component_definition(accordion)`
      returns `areas: [{name: "items", max_components: 20,
      allowed_components: [{id: accordionItem}]}]` plus the container's
      own dialog fields. That tells you exactly what to author:
      `add_component(parent_path=<accordion_path>, area_name="items",
      component_template_id=<allowed_id>, ...)` per item. Then
      `get_dialog(<allowed_id>)` for the item's fields.
   2. **Only if `get_component_definition` returns empty areas** (rare —
      e.g. linkList) fall back to `read_node(path, depth=3,
      structure_only=True)` on a live instance to learn the child shape,
      then use `add_child_node` (for non-templated content nodes).

10a. **Honour explicit user hints.** When the user names a workspace,
    path, template, instance, or component in their request (e.g.
    "workspace: nav", "use the events workspace", "under /about-us"),
    USE that hint directly. Do not search elsewhere first, do not
    second-guess. The `_KNOWN_WORKSPACES` probe list is just a
    discovery shortcut — `browse_workspace` and `search_workspace`
    accept ANY workspace name, including ones not surfaced by
    `list_workspaces`. Same for site roots: a path the user gives is
    the path you use. If the user's hint turns out to be wrong, ASK
    them rather than silently switching strategies.

10b. **Never delete a user's content as a "recovery" without explicit
    permission.** If a discovery path fails (workspace 404, path not
    found, dialog missing), STOP and report the failure. Do not
    `delete_node` + `create_page` to "move" content as a workaround.
    Movement / restructuring is destructive and irreversible — confirm
    with the user before any delete that re-creates content.

11. **switchableField / compositeField ARE auto-serialised — pass a dict
    value.** When a dialog field is a `switchableField` or
    `compositeField` whose definition declares a child-node itemProvider
    (`jcrChildNodeProvider` — the Magnolia 6 default, and what
    `get_dialog` reports per field), pass the value as a dict and the MCP
    stores it as the child node Magnolia expects (verified against live
    rendering):

    ```
    add_component(..., properties={
        "theme": "default",
        "animation": {"field": "enabled", "animationStyle": "fade-up",
                      "animationTiming": "stagger"},
    })
    ```

    For switchableField the dict MUST include `"field": "<option>"` (the
    selected option; `get_dialog` lists valid `options` and `sub_fields`
    per structured field). Re-authoring replaces the child node cleanly.
    `set_properties` supports the same dict shape.

    **Remaining hazards:** `multiField`, and any structured field whose
    itemProvider is NOT child-node based, are still not auto-serialised.
    `scan_components(instance)` classifies every in-use component:
    `structured_authorable_components` (dict-authorable),
    `hazard_components` (still avoid / author in the UI), and
    `safe_components` (flat-only). When in doubt, run
    `learn_component_shape(instance, template_id)` — it reads live usages
    of the component and returns its REAL on-disk shape (flat props +
    child nodes with sample values). Ground truth beats guessing.

    If the user asks for a component in `hazard_components`, warn that
    its on-disk shape isn't supported and propose a substitute (record
    proven substitutes in `references/<instance-key>.md`).

## Tool reference (one-liner per tool)

Discovery:
- `list_instances()` -> instances + aliases (run first if instance is ambiguous)
- `test_connection(instance)` -> REST / Nodes / Definitions API status
- `list_templates(instance, category?, verbose?)` -> page templates (slim — just ids). verbose=True adds names.
- `get_template(instance, template_id)` -> areas + allowed components per area
- `get_component_definition(instance, template_id)` -> COMPONENT template definition: dialog id, templateScript, areas with `max_components` + allowed child components, AND the shaped dialog fields inlined — one call gives authoring-ready info for container components (accordion, grid, tabs, ...)
- `get_dialog(instance, dialog_id)` -> field schema for ONE component (cached per-process); select-style fields include `options` (allowed values)
- `get_dialogs(instance, dialog_ids=[...])` -> batched: N dialogs in ONE call (parallelised, cached). Prefer this over N sequential `get_dialog` calls.
- `list_components_for_area(instance, template_id, area_name)` -> allowed components for one area
- `scan_components(instance, refresh?)` -> crawls the instance page-by-page (bounded fetches), returns the real component inventory (id, usage count, field count, example_paths) classified into `structured_authorable_components` / `hazard_components` / `safe_components`. Cached per instance; the generated, never-stale replacement for hand-kept component cheat-sheets.
- `learn_component_shape(instance, template_id)` -> merges live usages of a component into its REAL on-disk shape (flat props + child nodes with sample values + the dialog). Use before authoring anything structurally unfamiliar.

Read:
- `read_node(instance, path, depth?, properties_only?, structure_only?)` -> JCR node. `properties_only` = single node's fields. `structure_only` = tree of names/types/templates only, no values (~80% smaller — ideal for "learn the layout pattern" reads of a live example).
- `list_pages(instance, parent_path?, verbose?)` -> child page names (slim). verbose=True adds path + identifier + publication state (published/modified/unpublished).
- `get_publication_status(instance, path)` -> published / modified-since-publish / unpublished + timestamps
- `query_jcr(instance, sql2_statement, ...)` -> JCR-SQL2 query. Not every install exposes the endpoint (structured error if absent). Prefer CONTAINS() (indexed) over LIKE (flaky).
- `verify_render(instance, page_path)` -> fetch the rendered .html with auth: status, title, h1s, empty `<img src>` count, broken /dam/ refs. THE way to confirm a build actually renders — a clean JCR read does not guarantee a clean render.

Workspaces (content-app backings - events, contacts, products, etc.):
- `list_workspaces(instance)` -> which JCR workspaces are accessible + child counts
- `browse_workspace(instance, workspace, path?, limit?, node_types?)` -> children in any workspace (filter by node type)
- `search_workspace(instance, workspace, query, root_path?, node_types?, limit?)` -> fulltext search across any workspace: indexed JCR query when available (fast), BFS fallback otherwise (`method` in the response says which ran)

Safety / recovery:
- Every confirmed delete / move / splice snapshots the subtree to `snapshots/` and returns `snapshot_file`; `restore_snapshot(instance, snapshot_file, confirm=True)` recreates it.
- Every mutating call is appended to `audit.jsonl` (instance, tool, path, timestamp) — answer "what changed yesterday?" from there.

DAM:
- `list_dam_folder(instance, folder_path?, limit?, offset?)` -> subfolders + paged assets
- `search_dam(instance, query, root_path?, limit?)` -> recursive name match
- `get_asset(instance, dam_path)` -> single asset metadata (uuid, preview_url, ...)
- `upload_asset(instance, parent_folder, filename, content_b64, ...)` -> base64 upload
- `upload_asset_from_url(instance, parent_folder, filename, url, ...)` -> fetch URL + upload

Write:
- `create_page(instance, parent_path, page_name, template_id, ...)` -> new mgnl:page
- `add_component(instance, parent_path, area_name, component_template_id, ...)` -> new component, APPENDED last (parent_path can be a page OR a parent component for nested grids/containers). Validates property names against the dialog; returns `warnings` for unknown names. Dict values for child-node structured fields (switchableField etc.) are serialised automatically (rule 11).
- `insert_component(instance, parent_path, area_name, component_template_id, before=?|after=?|index=?, ...)` -> insert a component at a SPECIFIC position among an area's components without rebuilding the whole area. The Nodes API can only append, so this splices: it leaves the components BEFORE the insert point untouched and recreates only the tail (area snapshotted to disk first). Use this instead of delete-everything-and-rebuild when you need a component partway up an existing page.
- `reorder_components(instance, parent_path, area_name, order=[names])` -> reorder an area's components to the given complete order (longest-correct-head kept, tail spliced; snapshot taken first).
- `copy_node(instance, source_path, dest_parent_path, new_name?)` -> deep-copy a page/component. THE fast path for "make a page like X": clone, then retouch with set_properties / set_component_image. New uuids.
- `move_node(instance, source_path, dest_parent_path, new_name?, confirm?)` -> move/rename via copy+delete. Dry-run by default; snapshots the source to disk before deleting. New uuids — unpublish first if the page is live.
- `add_child_node(instance, parent_path, name, properties?, node_type?)` -> add a generic content child (use for container items where the child isn't a templated component)
- `set_properties(instance, path, properties)` -> update node fields (POST). Validates property names against the target node's `mgnl:template` dialog; dict values for structured fields serialise as child nodes (rule 11).
- `set_component_image(instance, component_path, asset_uuid, alt)` -> set image + image_alt in one call (prefer over set_properties for images)
- `make_dam_image_ref(asset_uuid, alt)` -> returns `{image_value, image_alt}` if you want the primitive
- `delete_node(instance, path, confirm?)` -> dry-run unless confirm=True (dry-run shows child count). Confirmed deletes snapshot the subtree to disk first; `restore_snapshot(instance, snapshot_file, confirm?)` undoes them. **Not available on all instances** — if missing, rebuild elsewhere and ask the user to remove the old page from the admin UI.
- `publish_page(instance, path, recursive?)` -> activate. Auto-discovers the command route from the instance's REST whitelist config, then falls back through common catalog/command pairs; response reports the route used.
- `unpublish_page(instance, path, recursive?)` -> deactivate on public. Same explicit-ask-only policy as publish.

## Decision tree for common asks

| User says | Tool sequence |
|---|---|
| "Make a page about X on [instance]" | list_instances -> list_templates -> get_template -> get_dialog (per component) -> create_page |
| "Add a component to /some/page" | get_template (find allowed components) -> get_dialog (component fields) -> add_component |
| "Update a property on /some/path" | set_properties(path, {field: value}) — heed warnings |
| "Swap the image on a component" | search_dam OR list_dam_folder -> set_component_image |
| "Upload this image and use it" | upload_asset_from_url -> set_component_image |
| "What's currently on /some/path?" | read_node(path, properties_only=True) |
| "Make a page like /existing/page" | copy_node(src, parent, new_name) -> set_properties to retouch |
| "Move/rename /some/page" | move_node (dry-run first, confirm after user ack) |
| "Put X above/below Y on the page" | insert_component(before=/after=) or reorder_components |
| "What workspaces are there?" | list_workspaces |
| "Browse the [name] workspace" | browse_workspace(workspace=name, path="/") |
| "Find anything mentioning X in [workspace]" | search_workspace(workspace=name, query=X) |
| "Publish /some/page" | publish_page (only after explicit ask) |
| "Take /some/page down" | unpublish_page (only after explicit ask) |
| "Is /some/page live?" | get_publication_status |
| "Did the page render correctly?" | verify_render(page_path) |

## Instance resolution

1. Exact key in `list_instances` -> use it.
2. Client name only -> resolve via `aliases`.
3. "[client] [tier]" -> build key `<client>-<tier>`.
4. Don't fabricate instance names. If unresolved, ask which instance.

State the resolved instance back before any writes.

## Loading details on demand

For deeper context, load a reference file via:
`skill_view("magnolia-author", "references/<name>.md")`

- `references/moving-pages.md` - workflow for moving pages between categories when delete_node is unavailable
- `references/imagery.md` - generic damLinkField pattern + DAM upload patterns
- `references/components.md` - dialog field type cheat sheet + container-component identification
- `references/project-document-layout.md` - proven row/card layout pattern for converting PCRs, proposals, reports into Magnolia pages (card variants, HTML tables, pitfalls)
- `references/troubleshooting.md` - common failures (406 on delete, 500 on JCR LIKE, empty image src, etc.)
- `references/instances.md` - registry format + adding a new instance + cred resolution

### Per-environment guides

The files above are generic. Each configured instance ALSO gets its own
guide at `references/<instance-key>.md` (the key from `instances.json`,
e.g. `references/example-prod.md`). Load it whenever you work that
instance — it records what the generic skill deliberately doesn't know.
If the conventional name 404s, don't guess again: the `skill_view` error
lists `available_files` — pick the guide from that list (older installs
used descriptive names like `acme-site-structure.md`), and ignore
`._*` entries (macOS metadata, not content). The guide records:

- the real component inventory + the theme/library in use,
- the page-template ids and the area/nesting model (e.g. container/intro),
- the hero/banner component + where it lives,
- the verified `switchableField` hazard list + proven substitutes,
- site hierarchy, naming conventions, tone.

Start one from `references/_instance-guide-template.md`. Populate it from
`scan_components(instance)` + a couple of live `read_node` reads on first
contact, and keep it current as you learn — that's where client knowledge
lives, NOT in this SKILL.md.

The skill itself ships only generic Magnolia knowledge. Client-specific
component catalogues, page-template anatomies, and authoring conventions
belong in the per-instance guide (and/or the agent's memory), not here.

## Working with user-attached content

When the user attaches a file in chat, many MCP clients cache it to a local
path and surface that path in your context (e.g. a `media_urls` field or an
`[attachment: ... -> /path]` marker). `set_page_image` and
`upload_asset_from_url` accept such a local path directly: the bare-path form
must resolve under `MAGNOLIA_AUTHOR_CACHE_DIR`; otherwise pass it as a
`file://` URL.

### Common case: attach an image to a page header

If the user gives you a page path (e.g. `/example/about-us`) and an
image, the whole flow is **one tool call**:

```
set_page_image(
    instance="example-prod",
    page_path="/example/about-us",
    image_source="file:///path/to/attached-image.jpg",
    alt="<one-line description of the image>",
)
```

`set_page_image` auto-discovers the page's hero/banner component using
the instance's configured `header_areas` + `header_component_prefixes`
(in `instances.json`; defaults cover `intro`/`main`/`header` areas and
`page-banner`/`banner-image`/`hero`/`pageHeader` prefixes), uploads the
image to the DAM, and wires it on. The local cache path works directly —
don't base64-encode it yourself. If a client's hero lives somewhere
non-default, set those two keys on the instance rather than hardcoding.

If `set_page_image` returns `error.stage = "find_component"`, the page
exists but doesn't have a header yet. Either pass `component_name`
explicitly or use `add_component` to create one first.

### When you DO need to discover

If the user doesn't name the page, or the page may not exist, do the
lightest discovery that gets you confident:

- One `list_pages(instance, parent_path=<site root>)` to enumerate.
- One `read_node(path, depth=3, structure_only=True)` to confirm shape
  before mutations.

Reach for `search_workspace` only when you're hunting by name/property,
not when you already have a known path — it's a slow BFS (~60-120s on
busy instances). When the user told you the path, trust it; verify with
`read_node` if you're unsure.

### Documents → new page (docx, pptx, pdf, etc.)

When the user attaches a document and asks for a page based on it:

1. `mcp_file_attachments_read_attachment(path)` — get the extracted text.
2. `list_templates` once if you don't already know the right page template
   for this site (cached after first call — calling twice is free).
3. Plan the full page structure from the doc content. Aim to commit to it
   in one shot rather than discovering iteratively.
4. **Call `build_page` once** with the full component list. It creates
   the page AND populates every component server-side, then verifies and
   returns the preview URL ready for your reply.

```
build_page(
    instance="example-prod",
    parent_path="/example",
    page_name="<slug>",
    template_id="<from list_templates>",
    title="<page title>",
    components=[
        # Use the REAL component ids + area names for this instance —
        # get them from scan_components / get_template / a live page read,
        # NOT from this placeholder shape. The pattern below shows nesting:
        # a top-level layout wrapper, then children pointing at its child area.
        {"parent_path": "/<root>/<slug>", "area_name": "<top area>",
         "component_template_id": "<wrapper component id>", "name": "wrap-1",
         "properties": {...}},
        {"parent_path": "/<root>/<slug>/<top area>/wrap-1", "area_name": "<child area>",
         "component_template_id": "<content component id>",
         "properties": {...}},
        # ... more children ...
    ],
)
```

The real wrapper/content component ids and area names are per-instance —
take them from the instance's guide (`references/<instance-key>.md`) or
discover them with `scan_components` + a live `read_node`, not from this
placeholder shape.

`build_page` returns `{preview_url, components_summary, components_results,
structure}`. Per-component errors don't roll back the page — patch
afterwards with `add_components_bulk` or `set_properties_bulk`.

If you're modifying an existing page rather than creating one, use
`add_components_bulk` directly (same `components` shape) — one call instead
of N. Same for batch property updates: `set_properties_bulk`.

**Tool-call budget:** doc-to-page should now land in ~3-6 calls total
(read_attachment, optional list_templates, build_page, optional patches).
If you're over 10 calls, you're probably falling back to per-component
add_component when build_page or add_components_bulk would do it in one.

### Token-efficient defaults

- `read_node(path, depth=3, structure_only=True)` — cheapest way to "see
  what's on a page" (~400 chars vs ~8KB for a full read).
- `list_pages(verbose=False)` — slim names-only list (default).
- `get_dialogs([id1, id2, ...])` — batched, one call beats N sequential
  `get_dialog` calls.
- `list_instances` — cached after the first call; cheap to call once
  but no need to repeat.

## Always finish with a clickable URL

Every final reply that creates, modifies, or fetches a page MUST include
the rendered preview URL on its own line so the user can click straight
through to it. Construct it from the instance's `base_url` (from
`list_instances`) plus the page path with `.html`:

```
https://<base_url host>/<page_path>.html
```

Examples:
- `https://author.example.com/example/about-us.html`
- `https://author.example.com/example/services/overview.html`

Use lowercase in the URL even if the JCR path uses capitals (the
renderer is case-insensitive on URLs but always emits lowercase). The
.html is required.

If you only read or listed something (no mutation), still drop the URL
when the user is clearly going to want to look at it next.

## Authoring tone

Match the client voice (taken from registries / project memory). Don't
fabricate client metadata. No em-dashes in user-visible artefacts unless
the client style explicitly uses them.

## Reply tone

Final reply to the user is BRIEF — two lines, hard cap. Required shape for
any page op:

- **First line: the clickable preview URL.**
- One short sentence describing what changed (e.g. "Built the page — 6
  sections, draft only, ready for your review.").

A summary count is fine ("26 components, 0 errors") but it goes in that ONE
sentence — never expanded into a list or tree.

**Forbidden in the user-facing reply** (this is what's been going wrong):
- the component tree / node names (`text-1`, `section-2`, …)
- per-component or per-theme breakdowns, area/column tables
- "Layer / Component / Properties" tables, recap of every property set
- narrating the process ("All N created, let me verify the full
  structure:" + a dump of the verification read)
- instance-setup asides, generic "verified and complete" filler

The verification read (rule 0 / Verification section) is for YOU to confirm
the write worked — its output must NOT be relayed. Think: the user opens the
preview URL to SEE the page; your job is the link plus a one-line "what",
then stop.

If the user EXPLICITLY asks ("show me the structure", "what did you do step
by step?"), then expand. Otherwise stay terse — when unsure, shorter.

## Verification

After any write, ONE read_node call is enough:

- **Single component change:** `read_node(path, properties_only=True)`
- **Whole page after a build:** `read_node(page_path, depth=4,
  structure_only=True)` — one call shows every component + nesting in
  ~80% less data than a full read.

**Do not** verify N child items with N separate read calls. If you added
5 accordion items, one `read_node(accordion_path, depth=3, structure_only=True)`
shows all 5. Per-item verification adds 5 tool calls and meaningful cost
for no extra signal — the `add_component` responses already returned
`created: true` for each.

For image-bearing pages, call `verify_render(instance, page_path)` — it
fetches the rendered HTML with auth and flags empty `<img src>` tags and
broken `/dam/` refs directly (no manual curl needed). `build_page` with
`verify=True` already includes a `render_check` in its response; only call
`verify_render` separately for pages modified by other means.

Pay particular attention to components flagged by validation warnings:
those properties were stored but will likely render as empty. Re-author
with the correct field names from `get_dialog`.

**Known Magnolia render quirk:** standalone generic `image` components on
freshly authored pages sometimes render an empty `<figure class="image">`
wrapper even when properties are correct and the DAM asset exists.
Touching the node post-write (`set_component_image` again) does NOT fix
it. If the user wants a hero image, prefer the site's dedicated
hero/banner component (e.g. a `page-banner` / `banner-image` component) —
banner components render images more reliably on fresh pages than the
generic `image` component. Discover the right id per instance (and record
it in the instance guide) rather than assuming.
