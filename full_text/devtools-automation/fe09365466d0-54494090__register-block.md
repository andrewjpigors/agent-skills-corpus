---
name: register-block
description: Use this skill when the user asks to register a block without a static template. Trigger phrases include "register a block", "create a block", "add a new block", "new block called", "prepare a block", "block scaffold". Also triggers on "update the block", "extend the block", "add feature to", "update section wrapper", or any request that names an existing block and describes a change.
version: 5.0.0
---

# Register Block Skill

> If a static component already exists in `static/src/blocks/` for this block, use `/migrate-static` instead — it derives attributes and markup from the component automatically.

> **Create or Update?**
> - If the block **does not exist yet** → follow Steps 0–9 below.
> - If the block **already exists** → jump to **Step 0-U (Update Flow)** immediately below.

The user provides requirements directly. Gather everything needed before writing any files.

---

## Step 0-U — Update Flow (existing blocks only)

### 0-U.1 Read all existing files first (non-negotiable)

Before planning any change, read every file that exists for the block:

- `resources/scripts/editor/blocks/{folder}/block.json`
- `resources/scripts/editor/blocks/{folder}/edit.jsx`
- `resources/scripts/editor/blocks/{folder}/index.jsx`
- `app/Blocks/{ClassName}.php`
- `resources/views/blocks/{folder}/index.blade.php`
- `resources/styles/blocks/{folder}.css`
- `resources/styles/blocks/{folder}.editor.css`
- `static/src/blocks/custom/{folder}/{Component}.tsx` (if exists)

### 0-U.2 Check reference project (if mentioned)

If the user says "look at `../other-project`" or similar, read the **equivalent block files** from that project and treat them as the canonical implementation pattern to follow.

### 0-U.3 Clarify scope before writing anything

Ask:
> "Should I update only the **editor files** (`block.json` + `edit.jsx`), or also the **PHP class** and **Blade template**?"

Default assumption: **editor-only** unless the user explicitly says otherwise or the new attribute requires server-side rendering to work.

### 0-U.4 Plan the diff, not a rewrite

Only change what the request requires. Do not restructure, rename, or clean up code that isn't directly involved in the new feature.

---

## Step 0 — Gather Requirements

Ask the user for the following before proceeding. Do not proceed until all are confirmed.

1. **Block name** — human-readable name (e.g. "Promo Banner")
2. **Render strategy** — client-side (save.jsx) or server-side (PHP + Blade)?
3. **InnerBlocks?** — does this block contain child blocks?
4. **Attributes** — for each attribute: name, type (`string` / `boolean` / `number` / `object` / `array`), default value, and any options if it's an enum string
5. **Any other constraints** — data query (CPT/taxonomy), toolbar controls, special layout requirements

Use this mapping to decide which editor control to generate for each attribute.

**Boolean attribute naming:** Boolean attribute names must use the `is` prefix (e.g. `isEnabled`, `isOpenedByDefault`). Rename for clarity if needed.

| Attribute type | Editor control |
|----------------|---------------|
| `boolean` | `<ToggleControl>` |
| `string` free text | `<TextControl>` |
| `string` HTML content | `<RichText>` in edit, `<RichText.Content>` in save |
| `string` enum, 2–4 options | `<ToggleGroupControl>` (`__experimentalToggleGroupControl`) |
| `string` enum, 5+ options | `<RadioControl>` |
| `object {value, slug}` color | `<ColorPaletteControl>` from `@secretstache/wordpress-gutenberg` |
| `object {id, url, alt}` media | `<MediaControl>` from `@secretstache/wordpress-gutenberg` |
| `number` bounded | `<RangeControl>` with min/max/step |

---

## Step 1 — Derive Names

| Item | Convention | Example |
|------|-----------|---------|
| Folder | kebab-case | `promo-banner` |
| Block slug | `{namespace}/{folder}` | `ssm/promo-banner` |
| PHP class | PascalCase | `PromoBanner` |
| CSS root | `wp-block-{namespace}-{folder}` | `wp-block-ssm-promo-banner` |
| BEM element | `wp-block-{namespace}-{folder}__{el}` | `wp-block-ssm-promo-banner__title` |

---

## Step 2 — `block.json`

`resources/scripts/editor/blocks/{folder}/block.json`

```json
{
  "$schema": "https://schemas.wp.org/trunk/block.json",
  "apiVersion": 3,
  "name": "ssm/block-slug",
  "title": "Block Title",
  "description": "",
  "keywords": ["keyword1", "keyword2", "ab"],
  "category": "ssm-components",
  "icon": "columns",
  "supports": {
    "anchor": true,
    "className": true,
    "spacing": { "margin": true, "padding": true }
  },
  "attributes": {}
}
```

Add `"render": "index"` for server-rendered blocks only.

**`"anchor"` and `"className"`** are included in every block by default — they enable the WordPress ID/anchor attribute and custom CSS class fields.

**Icon:** use `"columns"` as the default. Use `"list-view"` for list/accordion/timeline-style blocks. Use `"grid-view"` for cloud/gallery-style blocks.

Category: `"ssm-components"` for standalone blocks, `"ssm-templates"` for data-query/full-section blocks, `"ssm-design"` for root layout containers (section-wrapper).

---

## Step 3 — `index.jsx`

`resources/scripts/editor/blocks/{folder}/index.jsx`

**Client-side block:**
```js
import { registerBlockType } from '@wordpress/blocks';

import { edit } from './edit.jsx';
import { save } from './save.jsx';
import blockMetadata from './block.json';

registerBlockType(blockMetadata, { edit, save });
```

**Server-rendered block (no InnerBlocks, no data source):**
```js
import { registerBlockType } from '@wordpress/blocks';

import { edit } from './edit.jsx';
import blockMetadata from './block.json';

registerBlockType(blockMetadata, { edit, save: () => null });
```

**InnerBlocks block (plain container — section wrapper, accordion, etc.):**
```js
import { registerBlockType } from '@wordpress/blocks';
import { InnerBlocks } from '@wordpress/block-editor';

import { edit } from './edit.jsx';
import blockMetadata from './block.json';

registerBlockType(blockMetadata, {
  edit,
  save: () => <InnerBlocks.Content />,
});
```

**InnerBlocks block with PHP wrapper** (e.g. a carousel needing server-side markup around child items): add `"render": "index"` to block.json AND keep `save: () => <InnerBlocks.Content />`. PHP receives serialized inner blocks as `$content`.

**Data-source block** — has `queryType` / posts / feed. No `save`, no `InnerBlocks`, no `InnerBlocksCleanupFilter`. Constants are typically defined locally in `edit.jsx`:
```js
import { registerBlockType } from '@wordpress/blocks';

import { edit } from './edit.jsx';
import blockMetadata from './block.json';

registerBlockType(blockMetadata, { edit });
```

**Child block** — uses `__experimentalLabel` to show a meaningful name in the List View:
```js
import { registerBlockType } from '@wordpress/blocks';
import { InnerBlocks } from '@wordpress/block-editor';

import { edit } from './edit.jsx';
import blockMetadata from './block.json';

registerBlockType(blockMetadata, {
  edit,
  save: () => <InnerBlocks.Content />,
  __experimentalLabel: (attributes, { context }) => {
    const customName = attributes?.metadata?.name;
    if (context === 'list-view' && (customName || attributes.title)) {
      return customName || attributes.title;
    }
  },
});
```

---

## Step 3a — Parent / Child Block Structure

Use this pattern when a block owns a dedicated child block (e.g. Timeline → Timeline Item, Accordion → Accordion Item).

### Folder layout

Child blocks live **inside** the parent folder, not as siblings:

```
blocks/
  timeline/
    block.json
    index.jsx         ← imports child
    edit.jsx
    timeline-item/
      block.json
      index.jsx
      edit.jsx
```

### Child `block.json`

Use `"parent"` to restrict the child to only appear inside the parent:

```json
{
  "name": "ssm/timeline-item",
  "title": "Timeline Item",
  "parent": ["ssm/timeline"],
  "supports": { "className": false },
  "attributes": {
    "year": { "type": "number", "default": null }
  },
  "render": "index"
}
```

### Parent `index.jsx` — import the child here

The child registers itself when its `index.jsx` is imported. **Do not add the child to `editor.js`.**

```js
import { registerBlockType } from '@wordpress/blocks';
import { InnerBlocks } from '@wordpress/block-editor';

import { edit } from './edit.jsx';
import blockMetadata from './block.json';

import './timeline-item/index.jsx'; // ← child registers itself

registerBlockType(blockMetadata, {
  edit,
  save: () => <InnerBlocks.Content />,
});
```

### Parent `edit.jsx` — InnerBlocks setup

```jsx
import {
  InnerBlocks,
  useBlockProps,
  useInnerBlocksProps,
} from '@wordpress/block-editor';
import { useSelect } from '@wordpress/data';
import { __experimentalEmptyBlockPlaceholder as EmptyBlockPlaceholder } from '@secretstache/wordpress-gutenberg';

export const edit = ({ clientId }) => {
  const hasInnerBlocks = useSelect(
    (select) => select('core/block-editor').getBlockOrder(clientId).length > 0,
    [],
  );

  const blockProps = useBlockProps();

  const innerBlocksProps = useInnerBlocksProps(
    { className: 'wp-block-ssm-timeline__slides' },
    { allowedBlocks: ['ssm/timeline-item'], renderAppender: false },
  );

  return (
    <div {...blockProps}>
      <div {...innerBlocksProps}>
        {innerBlocksProps.children}
        {hasInnerBlocks
          ? <InnerBlocks.DefaultBlockAppender />
          : <EmptyBlockPlaceholder title="No items yet" clientId={clientId} />
        }
      </div>
    </div>
  );
};
```

**Child blocks with URL + open-in-new-tab:** use `__experimentalLinkControl` from `@wordpress/block-editor` (not `TextControl` + `ToggleControl`):
```jsx
import { __experimentalLinkControl as LinkControl } from '@wordpress/block-editor';
import { useMemo, useCallback } from '@wordpress/element';

// Attributes: url (string), linkIsOpenInNewTab (boolean)
const linkValue = useMemo(() => ({ url, opensInNewTab: linkIsOpenInNewTab }), [url, linkIsOpenInNewTab]);
<LinkControl
  value={linkValue}
  onChange={(link) => setAttributes({ url: link?.url || '', linkIsOpenInNewTab: link?.opensInNewTab || false })}
  onRemove={() => setAttributes({ url: '', linkIsOpenInNewTab: false })}
  settings={[{ id: 'opensInNewTab', title: 'Open in new tab', isToggle: true }]}
  showInitialSuggestions={true}
/>
```
In save.jsx: `<a href={url || '#'} {...(linkIsOpenInNewTab && { target: '_blank', rel: 'noreferrer noopener' })}>`

### Child `edit.jsx` — template + InnerBlocks

```jsx
import {
  useBlockProps,
  useInnerBlocksProps,
  InspectorControls,
} from '@wordpress/block-editor';
import { PanelBody, __experimentalNumberControl as NumberControl } from '@wordpress/components';
import { useCallback } from '@wordpress/element';

const ALLOWED_BLOCKS = ['core/image', 'core/heading', 'core/paragraph'];
const TEMPLATE = [
  ['core/image', {}],
  ['core/heading', { level: 3, placeholder: 'Headline' }],
  ['core/paragraph', { placeholder: 'Description...' }],
];

export const edit = ({ attributes, setAttributes }) => {
  const { year } = attributes;

  const onYearChange = useCallback(
    (value) => setAttributes({ year: value !== '' ? parseInt(value, 10) : null }),
    [],
  );

  const blockProps = useBlockProps();
  const innerBlocksProps = useInnerBlocksProps(
    { className: 'wp-block-ssm-timeline-item__content' },
    { allowedBlocks: ALLOWED_BLOCKS, template: TEMPLATE },
  );

  return (
    <>
      <InspectorControls>
        <PanelBody title="Settings">
          <NumberControl label="Year" value={year ?? ''} onChange={onYearChange} />
        </PanelBody>
      </InspectorControls>

      <div {...blockProps}>
        {year && <div className="wp-block-ssm-timeline-item__year">{year}</div>}
        <div {...innerBlocksProps} />
      </div>
    </>
  );
};
```

### `editor.js` — only the parent

```js
import './blocks/timeline/index.jsx'; // child is pulled in by the parent
```

---

## Step 4 — `edit.jsx`

`resources/scripts/editor/blocks/{folder}/edit.jsx`

The edit component has two parts: **InspectorControls** (sidebar) and the **block preview** (canvas).

```jsx
import { InspectorControls, useBlockProps } from '@wordpress/block-editor';
import {
  PanelBody,
  ToggleControl,
  TextControl,
  RangeControl,
  __experimentalToggleGroupControl as ToggleGroupControl,
  __experimentalToggleGroupControlOption as ToggleGroupControlOption,
  __experimentalDivider as Divider,
} from '@wordpress/components';
import { useCallback } from '@wordpress/element';
import { ColorPaletteControl, MediaControl } from '@secretstache/wordpress-gutenberg';

export const edit = ({ attributes, setAttributes }) => {
  const { isEnabled, label, size, accentColor } = attributes;

  const blockProps = useBlockProps({
    className: 'wp-block-ssm-block-slug',
  });

  const onSizeChange = useCallback((size) => {
    setAttributes({ size });
  }, []);

  return (
    <>
      <InspectorControls>
        <PanelBody title="Settings">

          <ToggleControl
            label="Enable feature"
            checked={isEnabled}
            onChange={(isEnabled) => setAttributes({ isEnabled })}
          />

          <Divider />

          <ToggleGroupControl
            isBlock
            label="Size"
            value={size}
            onChange={onSizeChange}
          >
            <ToggleGroupControlOption value="default" label="Default" />
            <ToggleGroupControlOption value="large" label="Large" />
          </ToggleGroupControl>

          <Divider />

          <ColorPaletteControl
            label="Accent Color"
            value={accentColor?.value}
            attributeName="accentColor"
            setAttributes={setAttributes}
          />

        </PanelBody>
      </InspectorControls>

      <div {...blockProps}>
        {/* Preview placeholder — no static template yet */}
      </div>
    </>
  );
};
```

**Key rules:**
- `useBlockProps()` always on the outermost wrapper.
- `ColorPaletteControl`: `value={color?.value}` — pass the string, not the whole object.
- `ToggleGroupControl` / `ToggleGroupControlOption` are `__experimental` — import with that prefix.
- `__experimentalDivider as Divider` — between control groups inside a PanelBody.
- Use `useCallback` for handlers passed as props; inline `onChange` is fine otherwise.
- Destructure all used attributes at the top.

**Child block text props — use `RichText` inline in the canvas, not `TextControl` in the sidebar:**

```jsx
import { RichText } from '@wordpress/block-editor';

<RichText
  tagName="span"
  value={title}
  onChange={(title) => setAttributes({ title })}
  placeholder="Enter title..."
/>
```

Use `RichText` for item-level text in child blocks (title, label, description). Use `TextControl` in the sidebar only for block-level global settings.

**InnerBlocks:**
```jsx
import { useInnerBlocksProps } from '@wordpress/block-editor';

const ALLOWED_BLOCKS = ['ssm/child-block'];
const TEMPLATE = [['ssm/child-block', {}]];

const blockProps = useBlockProps();
const innerBlocksProps = useInnerBlocksProps(blockProps, {
  allowedBlocks: ALLOWED_BLOCKS,
  template: TEMPLATE,
  renderAppender: InnerBlocks.DefaultBlockAppender,
});

return <div {...innerBlocksProps} />;
```

**Data query blocks:**
```jsx
import { select } from '@wordpress/data';
import { useMemo } from '@wordpress/element';
import {
  ResourcesWrapper,
  DataQueryControls,
  useDataQuery,
} from '@secretstache/wordpress-gutenberg';

// Define constants locally (not imported from index.jsx):
const QUERY_TYPE = { LATEST: 'latest', BY_CATEGORY: 'by_category', CURATED: 'curated' };
const POST_TYPE  = { ITEM: 'my_post_type' };
const TAXONOMY   = { CATEGORY: 'my_taxonomy' };

const { queryType, curatedTerms, curatedPosts, numberOfPosts } = attributes;

const isQueryTypeCurated    = queryType === QUERY_TYPE.CURATED;
const isQueryTypeByCategory = queryType === QUERY_TYPE.BY_CATEGORY;

const isEmptySelection =
  (isQueryTypeCurated && !curatedPosts?.length) ||
  (isQueryTypeByCategory && !curatedTerms?.length);

const queryConfig = useMemo(() => ({
  postType: POST_TYPE.ITEM,
  taxonomySlug: TAXONOMY.CATEGORY,
  curatedTermsIds: isQueryTypeByCategory && curatedTerms,
  curatedPostsIds: isQueryTypeCurated && curatedPosts?.map((post) => post.value),
  numberOfPosts: !isQueryTypeCurated ? numberOfPosts : -1,
  extraQueryArgs: {},
}), [queryType, curatedTerms, curatedPosts, numberOfPosts]);

const { postsToShow, isResolving, isEmpty } = useDataQuery(
  queryConfig,
  [queryType, curatedTerms, curatedPosts, numberOfPosts],
);
```

**Toolbar controls:**
```jsx
import { BlockControls } from '@wordpress/block-editor';
import { ToolbarButton } from '@wordpress/components';
import { replace } from '@wordpress/icons';

<BlockControls>
  <ToolbarButton icon={replace} label="Change image" onClick={openModal} />
</BlockControls>
```

---

## Step 5 — `save.jsx` (client-side blocks only)

```jsx
import { useBlockProps } from '@wordpress/block-editor';

export const save = ({ attributes }) => {
  const { title, size, accentColor } = attributes;

  if (!title) return null;

  const blockProps = useBlockProps.save({
    className: 'wp-block-ssm-block-slug',
  });

  return (
    <div {...blockProps}>
      {/* Placeholder — update when static template is ready */}
    </div>
  );
};
```

Rules:
- `useBlockProps.save()` — not `useBlockProps()`.
- Return `null` if required attributes are missing.
- `<RichText.Content tagName="p" value={quote} />` for rich text output.
- Skip for server-rendered blocks.

---

## Step 6 — Register in `editor.js`

Add to the block import list in alphabetical order:
```js
import './blocks/block-slug';
```

---

## Step 7 — PHP Class (server-rendered blocks only)

`app/Blocks/{ClassName}.php`

```php
<?php

namespace App\Blocks;

class ClassName extends Block
{
    protected function prepareData($attributes, $content): array
    {
        $label   = $attributes['label'] ?? '';
        $size    = $attributes['size'] ?? 'default';
        $color   = $attributes['accentColor'] ?? [];

        $wrapper_attributes = get_block_wrapper_attributes([
            'class' => 'flex flex-col',
        ]);

        return [
            'wrapper_attributes' => $wrapper_attributes,
            'label'              => $label,
            'size'               => $size,
            'color'              => $color,
            'content'            => $content,
        ];
    }
}
```

Rules:
- Class filename is PascalCase. Auto-loader converts `ClassName` → `class-name` as folder name — verify they match.
- `get_block_wrapper_attributes()` merges editor classes/styles — always use it.
- Pass `data-*` attributes through the wrapper array for JS hooks.
- Every `$attributes` key needs a `?? default` fallback.
- Color objects: use `$color['value']` for the hex and `$color['slug']` for the CSS var.

**Data-query block pattern** (CPT/taxonomy blocks — always use this exact structure):

```php
<?php

namespace App\Blocks;

use App\View\Composers\SSM;   // always import SSM for data-query blocks

class BlogFeed extends Block
{
    public const QUERY_LATEST      = 'latest';
    public const QUERY_CURATED     = 'curated';
    public const QUERY_BY_CATEGORY = 'category';

    protected function prepareData($attributes, $content): array
    {
        $query         = $attributes['queryType']     ?? self::QUERY_LATEST;
        $number_posts  = $attributes['numberOfPosts'] ?? 3;
        $curated_posts = array_column($attributes['curatedPosts'] ?? [], 'value');
        $curated_terms = array_column($attributes['curatedTerms'] ?? [], 'value');

        $is_empty_selection = ($query === self::QUERY_CURATED && empty($curated_posts))
                           || ($query === self::QUERY_BY_CATEGORY && empty($curated_terms));

        $args = [
            'data_source'    => 'posts',             // CPT slug (not WP post_type key)
            'query'          => $query,
            'taxonomy_slug'  => 'category',
            'curated_terms'  => $curated_terms,
            'number_posts'   => $query === self::QUERY_CURATED ? -1 : $number_posts,
            'curated_posts'  => $curated_posts,
            'excluded_posts' => [get_the_ID()],      // always exclude current page
        ];
        $post_ids = $is_empty_selection ? [] : SSM::getPosts($args);

        $posts = array_map(function ($post_id) {
            $image = null;
            if (has_post_thumbnail($post_id)) {
                $thumbnail_id = get_post_thumbnail_id($post_id);
                $image = [
                    'url' => get_the_post_thumbnail_url($post_id, 'large'),
                    'id'  => $thumbnail_id,
                    'alt' => get_post_meta($thumbnail_id, '_wp_attachment_image_alt', true)
                             ?: get_the_title($post_id),
                ];
            }

            return [
                'id'         => $post_id,
                'title'      => get_the_title($post_id),
                'excerpt'    => SSM::getPostExcerpt($post_id),
                'image'      => $image,
                'link'       => get_permalink($post_id),
                'link_label' => 'Read Article',
            ];
        }, $post_ids);

        $wrapper_attributes = get_block_wrapper_attributes();

        return [
            'wrapper_attributes' => $wrapper_attributes,
            'posts'              => $posts,
        ];
    }
}
```

Key points:
- Always `use App\View\Composers\SSM;` — never use bare `get_posts()`.
- Define `QUERY_*` constants on the class (matches exported constants in `index.jsx`).
- `'data_source'` must be the CPT slug (e.g. `'posts'`, `'frh_team'`).
- Always include `'excluded_posts' => [get_the_ID()]`.
- Thumbnail: always guard with `has_post_thumbnail()`, fetch alt from post meta with title fallback.
- Use `SSM::getPostExcerpt($post_id)` — not native `get_the_excerpt()`.

**`SSM::getPosts()` patterns (additional notes):

- `data_source` must match the actual CPT slug registered in WordPress (e.g. `frh_team`). Wrong slug → zero posts returned silently.
- Taxonomy queries: the `tax_query` branch fires only when `$query === $taxonomy_slug`. For UI query types like `by_department`, map to the taxonomy slug before passing:
  ```php
  'query'         => $is_by_dept ? self::TAXONOMY_DEPT : $query,
  'taxonomy_slug' => self::TAXONOMY_DEPT,
  ```
- Custom taxonomies need `"show_in_rest" => true` in `register_extended_taxonomy()` for `DataQueryControls.TaxonomySelect` to populate. Without it the select renders empty with no error.

---

## Step 8 — Blade Template (server-rendered blocks only)

`resources/views/blocks/{folder}/index.blade.php`

```blade
@php
    /**
     * @var $wrapper_attributes  string
     * @var $label               string
     * @var $size                string
     * @var $color               array
     * @var $content             string
     */
@endphp

<div {!! $wrapper_attributes !!}>

    @if ($label)
        <p class="text-charcoal">{{ $label }}</p>
    @endif

    @if ($size === 'large')
        {{-- large variant markup --}}
    @endif

    {!! $content !!}

</div>
```

Rules:
- `@php /** @var ... */ @endphp` listing every variable at the top.
- `{!! $wrapper_attributes !!}` on the outermost element — never `{{ }}`.
- `{!! $content !!}` for InnerBlocks or inner post content.
- `{!! $html !!}` for trusted HTML from WP functions (`get_field()`, `get_the_title()`).
- `{{ $text }}` for plain escaped text.
- `@class(['class' => $condition])` for conditional CSS classes.
- Inline CSS variables:
  ```blade
  @if (!empty($color['value']))
      style="--accent: {{ $color['value'] }}"
  @endif
  ```

**Responsive images — always use `ipq_get_theme_image()` with fallback:**

```blade
@if ($post['image'])
    @if (function_exists('ipq_get_theme_image'))
        {!! ipq_get_theme_image(
            $post['image']['id'],
            [ [550, 300, true], [1100, 600, true], [2200, 1200, true] ],
            ['alt' => $post['image']['alt'], 'class' => 'w-full h-full object-cover']
        ) !!}
    @else
        <img src="{!! $post['image']['url'] !!}" alt="{!! $post['image']['alt'] !!}" class="w-full h-full object-cover" />
    @endif
@endif
```

---

## Step 9 — CSS (if needed)

`resources/styles/blocks/{folder}.css`

Only needed for things Tailwind cannot express: keyframe animations, complex selectors, CSS custom property fallbacks. Most blocks need no CSS file.

If a CSS file is created, add its `@import` to **both**:
- `resources/styles/app.css` (frontend)
- `resources/styles/editor-canvas.css` (editor) — in the `/* custom blocks */` section

Skipping `editor-canvas.css` means all block styles, including `:root` CSS variables, are absent from the editor canvas.

---

## Common Patterns

### Background type with gradient

`backgroundType` enum: `color | image | video | gradient`

**Gradient attributes in `block.json`:**
```json
"gradientFromColor":      { "type": "object", "default": { "value": "#000", "slug": "black" } },
"gradientToColor":        { "type": "object", "default": { "value": "#fff", "slug": "white" } },
"gradientFromOpacity":    { "type": "number", "default": 100 },
"gradientToOpacity":      { "type": "number", "default": 100 }
```

**Editor controls** (shown when `backgroundType === 'gradient'`):
```jsx
<ColorPaletteControl label="From Color" value={gradientFromColor?.value} attributeName="gradientFromColor" setAttributes={setAttributes} />
<RangeControl label="From Opacity" value={gradientFromOpacity} onChange={onGradientFromOpacityChange} min={0} max={100} step={5} />
<Divider />
<ColorPaletteControl label="To Color" value={gradientToColor?.value} attributeName="gradientToColor" setAttributes={setAttributes} />
<RangeControl label="To Opacity" value={gradientToOpacity} onChange={onGradientToOpacityChange} min={0} max={100} step={5} />
```

**Canvas background div** (no angle control — direction is always top-to-bottom):
```jsx
className={classNames({ 'gradient-to-b': isBackgroundTypeGradient && hasGradient })}
style={isBackgroundTypeGradient && hasGradient ? {
  '--gradient-from': `color-mix(in oklab, var(--color-${gradientFromColor?.slug}) ${gradientFromOpacity}%, transparent)`,
  '--gradient-to':   `color-mix(in oklab, var(--color-${gradientToColor?.slug}) ${gradientToOpacity}%, transparent)`,
} : {}}
```

**Required CSS utility** (add to block's `.css` file if not present):
```css
.gradient-to-b {
  background-image: linear-gradient(to bottom, var(--gradient-from), var(--gradient-to));
}
```

---

### Overlay with solid + gradient modes

**Attributes in `block.json`:**
```json
"isIncludeOverlay":           { "type": "boolean" },
"overlayType":                { "type": "string", "enum": ["solid","gradient"], "default": "solid" },
"overlayColor":               { "type": "object", "default": { "value": "#fff", "slug": "white" } },
"overlayOpacity":             { "type": "number", "default": 50 },
"overlayGradientFromColor":   { "type": "object", "default": { "value": "#000", "slug": "black" } },
"overlayGradientToColor":     { "type": "object", "default": { "value": "#000", "slug": "black" } },
"overlayGradientFromOpacity": { "type": "number", "default": 80 },
"overlayGradientToOpacity":   { "type": "number", "default": 20 }
```

**Editor controls** (inside the image/video branch, after a `<Divider />`):
```jsx
<ToggleControl label="Include Overlay" onChange={onIncludeOverlayChange} checked={isIncludeOverlay} />
{isIncludeOverlay && (
  <>
    <RadioControl label="Overlay Type" selected={overlayType}
                  options={[{ label: 'Solid', value: 'solid' }, { label: 'Gradient', value: 'gradient' }]}
                  onChange={onOverlayTypeChange}
    />
    {isOverlayTypeSolid && (
      <>
        <ColorPaletteControl label="Overlay Color" value={overlayColor?.value} attributeName="overlayColor" setAttributes={setAttributes} />
        <RangeControl label="Opacity" value={overlayOpacity} onChange={onOverlayOpacityChange} min={0} max={100} step={5} />
      </>
    )}
    {isOverlayTypeGradient && (
      <>
        <ColorPaletteControl label="From Color" value={overlayGradientFromColor?.value} attributeName="overlayGradientFromColor" setAttributes={setAttributes} />
        <RangeControl label="From Opacity" value={overlayGradientFromOpacity} onChange={onOverlayGradientFromOpacityChange} min={0} max={100} step={5} />
        <Divider />
        <ColorPaletteControl label="To Color" value={overlayGradientToColor?.value} attributeName="overlayGradientToColor" setAttributes={setAttributes} />
        <RangeControl label="To Opacity" value={overlayGradientToOpacity} onChange={onOverlayGradientToOpacityChange} min={0} max={100} step={5} />
      </>
    )}
  </>
)}
```

**Canvas render** (inside the background div, above the closing tag):
```jsx
{/* Solid overlay */}
{isIncludeOverlay && isOverlayTypeSolid && (
  <div className="absolute inset-0 z-10"
       style={{ backgroundColor: `color-mix(in oklab, var(--color-${overlayColor?.slug}) ${overlayOpacity}%, transparent)` }} />
)}
{/* Gradient overlay */}
{isIncludeOverlay && isOverlayTypeGradient && (
  <div className="absolute inset-0 gradient-to-b z-10" style={{
    '--gradient-from': `color-mix(in oklab, var(--color-${overlayGradientFromColor?.slug}) ${overlayGradientFromOpacity}%, transparent)`,
    '--gradient-to':   `color-mix(in oklab, var(--color-${overlayGradientToColor?.slug}) ${overlayGradientToOpacity}%, transparent)`,
  }} />
)}
```

---

### Simple boolean feature toggle

When a feature has **no sub-options** (no color, no direction, no percentage) — use exactly one attribute and one control. Do not add anything else unless explicitly asked.

```json
"isAngledBorder": { "type": "boolean", "default": false }
```
```jsx
<ToggleControl label="Include Angle" onChange={() => setAttributes({ isAngledBorder: !isAngledBorder })} checked={isAngledBorder} />
```
```jsx
// In blockProps className:
{ 'has-angled-border': isAngledBorder }
```

The CSS class drives the visual — no inline styles needed.

---

## Final Checklist

- [ ] `block.json` — all attributes from gathered requirements, `"render": "index"` only if server-rendered
- [ ] `index.js` — correct pattern; `save: () => <InnerBlocks.Content />` for InnerBlocks blocks; `__experimentalLabel` if child block
- [ ] `edit.jsx` — controls match every gathered attribute; placeholder canvas preview
- [ ] `save.jsx` — placeholder structure; `useBlockProps.save()`; `null` guard (client-side only)
- [ ] `editor.js` — import in alphabetical order
- [ ] `app/Blocks/{ClassName}.php` — every attribute extracted with `?? default`; `wrapper_attributes` always present (server-rendered only)
- [ ] `resources/views/blocks/{folder}/index.blade.php` — skeleton structure with variables (server-rendered only)
- [ ] `resources/styles/blocks/{folder}.css` — only if needed
