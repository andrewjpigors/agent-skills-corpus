---
name: wordpress-theme-patterns
description: WordPress theme development patterns for classic themes (template hierarchy, functions.php organization, child themes), block/FSE themes (theme.json, block templates, template parts), and hybrid approaches. Use when building or modifying WordPress themes.
---

# WordPress Theme Development Patterns

## Introduction

This skill provides production-ready patterns for WordPress theme development. All code is PHP 8.0+ compatible, follows WordPress Coding Standards, and uses proper escaping and sanitization. Patterns cover classic themes, block/FSE themes, child themes, hybrid approaches, and the template hierarchy system that underlies all WordPress theming.

## When to Use This Skill

- Building a new WordPress theme (classic, block, or hybrid)
- Organizing `functions.php` and theme include files
- Creating a child theme with proper parent asset enqueuing
- Configuring `theme.json` for block/FSE themes
- Working with the WordPress template hierarchy
- Registering theme supports, menus, image sizes, and sidebars
- Enqueueing theme scripts and styles correctly
- Creating custom template tags for use in theme templates
- Building block templates and template parts for FSE themes

## Core Concepts

**Template Hierarchy**: WordPress resolves templates from most-specific to least-specific. Understanding this hierarchy is essential for theme development: `single-{post_type}-{slug}.php` > `single-{post_type}.php` > `single.php` > `singular.php` > `index.php`.

**Classic vs Block Themes**: Classic themes use PHP template files and `functions.php` for configuration. Block themes use `theme.json` for design tokens and HTML-based block templates in `templates/` and `parts/` directories. Hybrid themes combine both approaches.

**Escape Late, Sanitize Early**: Sanitize all input when it enters the system. Escape all output at the point of rendering. Never trust user input, database values, or third-party API responses.

**WordPress Coding Standards**: Use tabs for indentation, `snake_case` for function and variable names, Yoda conditions for comparisons, and braces on the same line for control structures.

## Quick Start

A minimal classic theme requires only two files: `style.css` (with the theme header) and `index.php`. Here is a practical starting point with proper theme support:

```php
<?php
/**
 * Theme functions and definitions.
 *
 * @package suspended
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'THEME_VERSION', '1.0.0' );
define( 'THEME_DIR', get_template_directory() );
define( 'THEME_URI', get_template_directory_uri() );

add_action( 'after_setup_theme', function (): void {
    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'html5', [
        'search-form', 'comment-form', 'comment-list',
        'gallery', 'caption', 'style', 'script',
    ] );

    register_nav_menus( [
        'primary' => esc_html__( 'Primary Menu', 'suspended' ),
        'footer'  => esc_html__( 'Footer Menu', 'suspended' ),
    ] );
} );

add_action( 'wp_enqueue_scripts', function (): void {
    wp_enqueue_style( 'suspended-style', THEME_URI . '/css/main.css', [], THEME_VERSION );
    wp_enqueue_script( 'suspended-script', THEME_URI . '/js/main.js', [], THEME_VERSION, [ 'in_footer' => true, 'strategy' => 'defer' ] );
} );
```

---

## Template Hierarchy Reference

WordPress uses the template hierarchy to determine which theme template file to use for a given request. Templates are resolved from most-specific to most-general, always falling back to `index.php`.

### Single Posts and Pages

```text
Single Post:
  single-{post_type}-{slug}.php
  single-{post_type}.php
  single.php
  singular.php
  index.php

Page:
  {custom-template}.php    (selected in editor)
  page-{slug}.php
  page-{id}.php
  page.php
  singular.php
  index.php

Attachment:
  {mime-type}.php          (e.g., image.php, video.php)
  attachment.php
  single-attachment-{slug}.php
  single-attachment.php
  single.php
  singular.php
  index.php
```

### Archives

```text
Category:
  category-{slug}.php
  category-{id}.php
  category.php
  archive.php
  index.php

Tag:
  tag-{slug}.php
  tag-{id}.php
  tag.php
  archive.php
  index.php

Custom Taxonomy:
  taxonomy-{taxonomy}-{term}.php
  taxonomy-{taxonomy}.php
  taxonomy.php
  archive.php
  index.php

Custom Post Type Archive:
  archive-{post_type}.php
  archive.php
  index.php

Author:
  author-{nicename}.php
  author-{id}.php
  author.php
  archive.php
  index.php
```

### Special Templates

```text
Front Page:     front-page.php > home.php > index.php
Blog/Home:      home.php > index.php
Search:         search.php > index.php
404:            404.php > index.php
```

### Block Theme Template Hierarchy

Block themes follow the same hierarchy but use HTML files in the `templates/` directory instead of PHP files. Template parts live in `parts/`:

```text
templates/
  single-project.html      (equivalent to single-project.php)
  single.html              (equivalent to single.php)
  archive-project.html     (equivalent to archive-project.php)
  page.html
  index.html               (required for block themes)

parts/
  header.html
  footer.html
  sidebar.html
```

---

## Patterns

### Pattern 1: Classic Theme functions.php Organization

Keep `functions.php` lean by delegating hook registrations to separate include files.

**functions.php**:

```php
<?php
/**
 * Theme functions and definitions.
 *
 * @package suspended
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

define( 'THEME_VERSION', '1.0.0' );
define( 'THEME_DIR', get_template_directory() );
define( 'THEME_URI', get_template_directory_uri() );

$theme_includes = [
    'inc/theme-support.php',
    'inc/enqueue.php',
    'inc/template-tags.php',
    'inc/widgets.php',
    'inc/customizer.php',
];

foreach ( $theme_includes as $file ) {
    $filepath = THEME_DIR . '/' . $file;
    if ( file_exists( $filepath ) ) {
        require_once $filepath;
    }
}
```

**inc/theme-support.php**:

```php
<?php
/**
 * Theme support features.
 *
 * @package suspended
 */

declare(strict_types=1);

add_action( 'after_setup_theme', function (): void {
    add_theme_support( 'html5', [
        'search-form', 'comment-form', 'comment-list',
        'gallery', 'caption', 'style', 'script',
    ] );

    add_theme_support( 'title-tag' );
    add_theme_support( 'post-thumbnails' );
    add_theme_support( 'automatic-feed-links' );
    add_theme_support( 'customize-selective-refresh-widgets' );
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'responsive-embeds' );

    // Custom image sizes.
    add_image_size( 'hero-banner', 1920, 800, true );
    add_image_size( 'card-thumbnail', 600, 400, true );

    // Navigation menus.
    register_nav_menus( [
        'primary' => esc_html__( 'Primary Menu', 'suspended' ),
        'footer'  => esc_html__( 'Footer Menu', 'suspended' ),
        'mobile'  => esc_html__( 'Mobile Menu', 'suspended' ),
    ] );

    $GLOBALS['content_width'] = 1200;

    load_theme_textdomain( 'suspended', THEME_DIR . '/languages' );
} );
```

**inc/enqueue.php**:

```php
<?php
/**
 * Enqueue scripts and styles.
 *
 * @package suspended
 */

declare(strict_types=1);

add_action( 'wp_enqueue_scripts', function (): void {
    wp_enqueue_style(
        'suspended-style',
        THEME_URI . '/css/main.css',
        [],
        THEME_VERSION
    );

    wp_enqueue_script(
        'suspended-script',
        THEME_URI . '/js/main.js',
        [],
        THEME_VERSION,
        [ 'in_footer' => true, 'strategy' => 'defer' ]
    );

    wp_localize_script( 'suspended-script', 'suspendedData', [
        'ajaxUrl' => admin_url( 'admin-ajax.php' ),
        'nonce'   => wp_create_nonce( 'suspended_nonce' ),
        'homeUrl' => home_url( '/' ),
    ] );

    if ( is_singular() && comments_open() && get_option( 'thread_comments' ) ) {
        wp_enqueue_script( 'comment-reply' );
    }
}, 10 );
```

**inc/template-tags.php**:

```php
<?php
/**
 * Custom template tags for use in theme templates.
 *
 * @package suspended
 */

declare(strict_types=1);

/**
 * Display the posted-on date with proper escaping.
 */
function suspended_posted_on(): void {
    $time_string = sprintf(
        '<time class="entry-date published" datetime="%1$s">%2$s</time>',
        esc_attr( get_the_date( DATE_W3C ) ),
        esc_html( get_the_date() )
    );

    printf(
        '<span class="posted-on">%s %s</span>',
        esc_html__( 'Published', 'suspended' ),
        $time_string // Already escaped above.
    );
}

/**
 * Display the post author with a link to their archive.
 */
function suspended_posted_by(): void {
    printf(
        '<span class="byline"><span class="author vcard"><a class="url fn n" href="%s">%s</a></span></span>',
        esc_url( get_author_posts_url( (int) get_the_author_meta( 'ID' ) ) ),
        esc_html( get_the_author() )
    );
}

/**
 * Display a post thumbnail with fallback.
 *
 * @param string $size Image size name.
 */
function suspended_post_thumbnail( string $size = 'card-thumbnail' ): void {
    if ( post_password_required() || is_attachment() ) {
        return;
    }

    if ( has_post_thumbnail() ) {
        the_post_thumbnail( $size, [
            'class'   => 'entry-thumbnail',
            'loading' => 'lazy',
        ] );
    } else {
        printf(
            '<img src="%s" alt="%s" class="entry-thumbnail placeholder" loading="lazy" />',
            esc_url( THEME_URI . '/images/placeholder.jpg' ),
            esc_attr__( 'Placeholder image', 'suspended' )
        );
    }
}
```

---

### Pattern 2: Child Theme Setup with Proper Parent Enqueue

**style.css** (child theme header -- required):

```css
/*
 Theme Name:   Suspended Child
 Theme URI:    https://example.com/suspended-child
 Description:  Child theme for Suspended
 Author:       Your Name
 Author URI:   https://example.com
 Template:     suspended
 Version:      1.0.0
 Text Domain:  suspended-child
*/
```

**functions.php** (child theme):

```php
<?php
/**
 * Suspended Child theme functions.
 *
 * @package suspended-child
 */

declare(strict_types=1);

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_action( 'wp_enqueue_scripts', function (): void {
    $parent_theme   = wp_get_theme( 'suspended' );
    $parent_version = $parent_theme->get( 'Version' );

    // Enqueue parent style.
    wp_enqueue_style(
        'suspended-parent-style',
        get_template_directory_uri() . '/css/main.css',
        [],
        $parent_version
    );

    // Enqueue child style with parent as dependency.
    wp_enqueue_style(
        'suspended-child-style',
        get_stylesheet_directory_uri() . '/css/child.css',
        [ 'suspended-parent-style' ],
        wp_get_theme()->get( 'Version' )
    );

    // Child theme scripts.
    wp_enqueue_script(
        'suspended-child-script',
        get_stylesheet_directory_uri() . '/js/child.js',
        [ 'suspended-script' ],
        wp_get_theme()->get( 'Version' ),
        [ 'in_footer' => true, 'strategy' => 'defer' ]
    );
}, 20 ); // Priority 20 to load after parent at 10.

/**
 * Override parent theme features or add new ones.
 */
add_action( 'after_setup_theme', function (): void {
    // Override a parent image size.
    add_image_size( 'card-thumbnail', 800, 500, true );

    // Register additional child theme menu.
    register_nav_menus( [
        'topbar' => esc_html__( 'Top Bar Menu', 'suspended-child' ),
    ] );
}, 11 ); // Priority 11 to run after parent's after_setup_theme at 10.
```

**Key child theme rules:**

- The `Template` header in `style.css` must match the parent theme's directory name exactly.
- Use `get_template_directory_uri()` for parent theme assets.
- Use `get_stylesheet_directory_uri()` for child theme assets.
- Enqueue child styles with the parent style handle as a dependency.
- Use a higher priority number (e.g., 20) on `wp_enqueue_scripts` to ensure the parent has loaded first.
- Use a higher priority number (e.g., 11) on `after_setup_theme` to override parent settings.
- To remove a parent hook, use `remove_action()` or `remove_filter()` at the `init` hook.

---

### Pattern 3: Block/FSE theme.json Configuration

A complete `theme.json` for a block theme with settings, styles, custom templates, and template parts.

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "settings": {
        "appearanceTools": true,
        "useRootPaddingAwareAlignments": true,
        "layout": {
            "contentSize": "800px",
            "wideSize": "1200px"
        },
        "color": {
            "defaultPalette": false,
            "defaultGradients": false,
            "palette": [
                { "slug": "primary", "color": "#1e40af", "name": "Primary" },
                { "slug": "secondary", "color": "#9333ea", "name": "Secondary" },
                { "slug": "foreground", "color": "#1f2937", "name": "Foreground" },
                { "slug": "background", "color": "#ffffff", "name": "Background" },
                { "slug": "muted", "color": "#6b7280", "name": "Muted" }
            ]
        },
        "typography": {
            "fluid": true,
            "fontFamilies": [
                {
                    "fontFamily": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
                    "slug": "system",
                    "name": "System"
                },
                {
                    "fontFamily": "'Georgia', 'Times New Roman', serif",
                    "slug": "serif",
                    "name": "Serif"
                }
            ],
            "fontSizes": [
                { "slug": "small", "size": "0.875rem", "name": "Small", "fluid": { "min": "0.8rem", "max": "0.875rem" } },
                { "slug": "medium", "size": "1.125rem", "name": "Medium", "fluid": { "min": "1rem", "max": "1.125rem" } },
                { "slug": "large", "size": "1.75rem", "name": "Large", "fluid": { "min": "1.375rem", "max": "1.75rem" } },
                { "slug": "x-large", "size": "2.5rem", "name": "Extra Large", "fluid": { "min": "1.75rem", "max": "2.5rem" } }
            ]
        },
        "spacing": {
            "units": [ "px", "em", "rem", "vh", "vw", "%" ],
            "spacingScale": { "steps": 0 },
            "spacingSizes": [
                { "slug": "10", "size": "0.5rem", "name": "XS" },
                { "slug": "20", "size": "1rem", "name": "Small" },
                { "slug": "30", "size": "1.5rem", "name": "Medium" },
                { "slug": "40", "size": "2rem", "name": "Large" },
                { "slug": "50", "size": "3rem", "name": "XL" },
                { "slug": "60", "size": "5rem", "name": "XXL" }
            ]
        },
        "blocks": {
            "core/button": { "border": { "radius": true } },
            "core/paragraph": { "color": { "link": true } }
        }
    },
    "styles": {
        "color": {
            "background": "var(--wp--preset--color--background)",
            "text": "var(--wp--preset--color--foreground)"
        },
        "typography": {
            "fontFamily": "var(--wp--preset--font-family--system)",
            "fontSize": "var(--wp--preset--font-size--medium)",
            "lineHeight": "1.6"
        },
        "spacing": {
            "padding": {
                "top": "0",
                "right": "var(--wp--preset--spacing--20)",
                "bottom": "0",
                "left": "var(--wp--preset--spacing--20)"
            }
        },
        "elements": {
            "link": {
                "color": { "text": "var(--wp--preset--color--primary)" },
                ":hover": { "color": { "text": "var(--wp--preset--color--secondary)" } }
            },
            "heading": {
                "typography": { "fontWeight": "700", "lineHeight": "1.2" },
                "color": { "text": "var(--wp--preset--color--foreground)" }
            },
            "h1": { "typography": { "fontSize": "var(--wp--preset--font-size--x-large)" } },
            "h2": { "typography": { "fontSize": "var(--wp--preset--font-size--large)" } },
            "button": {
                "border": { "radius": "4px" },
                "color": {
                    "background": "var(--wp--preset--color--primary)",
                    "text": "var(--wp--preset--color--background)"
                },
                ":hover": { "color": { "background": "var(--wp--preset--color--secondary)" } }
            }
        },
        "blocks": {
            "core/site-title": {
                "typography": { "fontSize": "var(--wp--preset--font-size--large)", "fontWeight": "700" }
            },
            "core/navigation": {
                "typography": { "fontSize": "var(--wp--preset--font-size--small)" }
            }
        }
    },
    "customTemplates": [
        { "name": "page-no-title", "title": "Page (No Title)", "postTypes": [ "page" ] },
        { "name": "page-full-width", "title": "Full Width", "postTypes": [ "page", "post" ] }
    ],
    "templateParts": [
        { "name": "header", "title": "Header", "area": "header" },
        { "name": "footer", "title": "Footer", "area": "footer" },
        { "name": "sidebar", "title": "Sidebar", "area": "uncategorized" }
    ]
}
```

**Key theme.json concepts:**

- **version 3**: Current schema version (WordPress 6.6+). Use version 2 for WordPress 6.0-6.5 compatibility.
- **appearanceTools**: Shorthand that enables border, color, spacing, typography, and dimensions controls in the editor.
- **useRootPaddingAwareAlignments**: Ensures full-width blocks break out of the content padding correctly.
- **fluid typography**: Automatically scales font sizes between `min` and `max` based on viewport width.
- **defaultPalette/defaultGradients**: Set to `false` to remove WordPress default colors and show only your custom palette.
- **customTemplates**: Defines templates available in the editor's template selector.
- **templateParts**: Declares reusable template parts. The `area` property determines where the part appears in the Site Editor.

---

### Pattern 4: Block Theme Template Files

Block themes use HTML files with block markup instead of PHP templates.

**templates/index.html** (required):

```html
<!-- wp:template-part {"slug":"header","area":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:query {"queryId":1,"query":{"perPage":10,"pages":0,"offset":0,"postType":"post","order":"desc","orderBy":"date","inherit":true}} -->
    <div class="wp-block-query">
        <!-- wp:post-template -->
            <!-- wp:post-featured-image {"isLink":true} /-->
            <!-- wp:post-title {"isLink":true} /-->
            <!-- wp:post-excerpt /-->
            <!-- wp:post-date /-->
        <!-- /wp:post-template -->

        <!-- wp:query-pagination -->
            <!-- wp:query-pagination-previous /-->
            <!-- wp:query-pagination-numbers /-->
            <!-- wp:query-pagination-next /-->
        <!-- /wp:query-pagination -->

        <!-- wp:query-no-results -->
            <!-- wp:paragraph -->
            <p>No posts found.</p>
            <!-- /wp:paragraph -->
        <!-- /wp:query-no-results -->
    </div>
    <!-- /wp:query -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","area":"footer"} /-->
```

**templates/single.html**:

```html
<!-- wp:template-part {"slug":"header","area":"header"} /-->

<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} -->
<main class="wp-block-group">
    <!-- wp:post-featured-image /-->
    <!-- wp:post-title {"level":1} /-->

    <!-- wp:group {"layout":{"type":"flex","justifyContent":"left","flexWrap":"wrap"}} -->
    <div class="wp-block-group">
        <!-- wp:post-date /-->
        <!-- wp:post-author-name {"isLink":true} /-->
        <!-- wp:post-terms {"term":"category"} /-->
    </div>
    <!-- /wp:group -->

    <!-- wp:post-content {"layout":{"type":"constrained"}} /-->

    <!-- wp:post-terms {"term":"post_tag","prefix":"Tags: "} /-->

    <!-- wp:comments -->
        <!-- wp:comments-title /-->
        <!-- wp:comment-template -->
            <!-- wp:comment-author-name /-->
            <!-- wp:comment-date /-->
            <!-- wp:comment-content /-->
            <!-- wp:comment-reply-link /-->
            <!-- wp:comment-edit-link /-->
        <!-- /wp:comment-template -->
        <!-- wp:comments-pagination -->
            <!-- wp:comments-pagination-previous /-->
            <!-- wp:comments-pagination-numbers /-->
            <!-- wp:comments-pagination-next /-->
        <!-- /wp:comments-pagination -->
        <!-- wp:post-comments-form /-->
    <!-- /wp:comments -->
</main>
<!-- /wp:group -->

<!-- wp:template-part {"slug":"footer","area":"footer"} /-->
```

**parts/header.html**:

```html
<!-- wp:group {"tagName":"header","layout":{"type":"constrained"}} -->
<header class="wp-block-group">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:site-title /-->
        <!-- wp:navigation /-->
    </div>
    <!-- /wp:group -->
</header>
<!-- /wp:group -->
```

**parts/footer.html**:

```html
<!-- wp:group {"tagName":"footer","layout":{"type":"constrained"}} -->
<footer class="wp-block-group">
    <!-- wp:group {"layout":{"type":"flex","justifyContent":"space-between"}} -->
    <div class="wp-block-group">
        <!-- wp:paragraph -->
        <p>&copy; 2026 Site Name. All rights reserved.</p>
        <!-- /wp:paragraph -->
        <!-- wp:navigation /-->
    </div>
    <!-- /wp:group -->
</footer>
<!-- /wp:group -->
```

---

### Pattern 5: Hybrid Theme (Classic Theme with Block Support)

A hybrid approach lets a classic theme adopt block editor features progressively.

**functions.php additions for block support:**

```php
<?php
declare(strict_types=1);

add_action( 'after_setup_theme', function (): void {
    // Enable block editor features in a classic theme.
    add_theme_support( 'wp-block-styles' );
    add_theme_support( 'responsive-embeds' );
    add_theme_support( 'align-wide' );
    add_theme_support( 'editor-styles' );

    // Load editor-specific styles so the editor matches the front end.
    add_editor_style( 'css/editor-style.css' );

    // Define a color palette for the block editor.
    add_theme_support( 'editor-color-palette', [
        [ 'name' => esc_html__( 'Primary', 'suspended' ), 'slug' => 'primary', 'color' => '#1e40af' ],
        [ 'name' => esc_html__( 'Secondary', 'suspended' ), 'slug' => 'secondary', 'color' => '#9333ea' ],
        [ 'name' => esc_html__( 'Foreground', 'suspended' ), 'slug' => 'foreground', 'color' => '#1f2937' ],
        [ 'name' => esc_html__( 'Background', 'suspended' ), 'slug' => 'background', 'color' => '#ffffff' ],
    ] );

    // Define font sizes for the block editor.
    add_theme_support( 'editor-font-sizes', [
        [ 'name' => esc_html__( 'Small', 'suspended' ), 'slug' => 'small', 'size' => 14 ],
        [ 'name' => esc_html__( 'Medium', 'suspended' ), 'slug' => 'medium', 'size' => 18 ],
        [ 'name' => esc_html__( 'Large', 'suspended' ), 'slug' => 'large', 'size' => 28 ],
    ] );

    // Disable custom colors to enforce the palette.
    add_theme_support( 'disable-custom-colors' );
} );
```

**Optional theme.json for a hybrid theme:**

A classic theme can include a `theme.json` to configure block editor settings without becoming a full block theme. Simply omit the `templates/` and `parts/` directories:

```json
{
    "$schema": "https://schemas.wp.org/trunk/theme.json",
    "version": 3,
    "settings": {
        "layout": {
            "contentSize": "800px",
            "wideSize": "1200px"
        },
        "color": {
            "defaultPalette": false,
            "palette": [
                { "slug": "primary", "color": "#1e40af", "name": "Primary" },
                { "slug": "secondary", "color": "#9333ea", "name": "Secondary" }
            ]
        }
    }
}
```

---

### Pattern 6: Widget and Sidebar Registration

```php
<?php
/**
 * Register widget areas (sidebars).
 *
 * @package suspended
 */

declare(strict_types=1);

add_action( 'widgets_init', function (): void {
    register_sidebar( [
        'name'          => esc_html__( 'Main Sidebar', 'suspended' ),
        'id'            => 'sidebar-main',
        'description'   => esc_html__( 'Widgets displayed on blog and archive pages.', 'suspended' ),
        'before_widget' => '<section id="%1$s" class="widget %2$s">',
        'after_widget'  => '</section>',
        'before_title'  => '<h3 class="widget-title">',
        'after_title'   => '</h3>',
    ] );

    register_sidebar( [
        'name'          => esc_html__( 'Footer Column 1', 'suspended' ),
        'id'            => 'footer-1',
        'description'   => esc_html__( 'First footer widget area.', 'suspended' ),
        'before_widget' => '<div id="%1$s" class="widget %2$s">',
        'after_widget'  => '</div>',
        'before_title'  => '<h4 class="widget-title">',
        'after_title'   => '</h4>',
    ] );
} );
```

**Using a sidebar in a template:**

```php
<?php if ( is_active_sidebar( 'sidebar-main' ) ) : ?>
    <aside class="sidebar" role="complementary">
        <?php dynamic_sidebar( 'sidebar-main' ); ?>
    </aside>
<?php endif; ?>
```

---

### Pattern 7: Theme Customizer Integration

```php
<?php
/**
 * Theme Customizer settings.
 *
 * @package suspended
 */

declare(strict_types=1);

add_action( 'customize_register', function ( WP_Customize_Manager $wp_customize ): void {
    // Add a section.
    $wp_customize->add_section( 'suspended_hero', [
        'title'    => esc_html__( 'Hero Section', 'suspended' ),
        'priority' => 30,
    ] );

    // Add a setting with sanitization.
    $wp_customize->add_setting( 'suspended_hero_heading', [
        'default'           => esc_html__( 'Welcome to our site', 'suspended' ),
        'sanitize_callback' => 'sanitize_text_field',
        'transport'         => 'postMessage',
    ] );

    // Add the control.
    $wp_customize->add_control( 'suspended_hero_heading', [
        'label'   => esc_html__( 'Hero Heading', 'suspended' ),
        'section' => 'suspended_hero',
        'type'    => 'text',
    ] );

    // Image control.
    $wp_customize->add_setting( 'suspended_hero_image', [
        'default'           => '',
        'sanitize_callback' => 'esc_url_raw',
    ] );

    $wp_customize->add_control( new WP_Customize_Image_Control( $wp_customize, 'suspended_hero_image', [
        'label'   => esc_html__( 'Hero Background Image', 'suspended' ),
        'section' => 'suspended_hero',
    ] ) );

    // Selective refresh for the heading.
    $wp_customize->selective_refresh->add_partial( 'suspended_hero_heading', [
        'selector'        => '.hero-heading',
        'render_callback' => function (): void {
            echo esc_html( get_theme_mod( 'suspended_hero_heading', 'Welcome to our site' ) );
        },
    ] );
} );
```

**Using the customizer value in a template:**

```php
<h1 class="hero-heading">
    <?php echo esc_html( get_theme_mod( 'suspended_hero_heading', 'Welcome to our site' ) ); ?>
</h1>

<?php
$hero_image = get_theme_mod( 'suspended_hero_image', '' );
if ( $hero_image ) :
?>
    <div class="hero-image" style="background-image: url(<?php echo esc_url( $hero_image ); ?>);">
    </div>
<?php endif; ?>
```

---

### Pattern 8: Custom Page Templates (Classic Theme)

**templates/page-landing.php:**

```php
<?php
/**
 * Template Name: Landing Page
 * Template Post Type: page
 *
 * A full-width landing page template with no sidebar.
 *
 * @package suspended
 */

declare(strict_types=1);

get_header();
?>

<main class="landing-page">
    <?php
    while ( have_posts() ) :
        the_post();
    ?>
        <article <?php post_class( 'landing-content' ); ?>>
            <?php if ( has_post_thumbnail() ) : ?>
                <div class="landing-hero">
                    <?php the_post_thumbnail( 'hero-banner', [ 'class' => 'landing-hero__image' ] ); ?>
                </div>
            <?php endif; ?>

            <div class="landing-body">
                <?php the_content(); ?>
            </div>
        </article>
    <?php endwhile; ?>
</main>

<?php
get_footer();
```

**Key points:**

- The `Template Name:` comment in the file header registers the template in the page editor.
- `Template Post Type:` limits which post types can use this template (defaults to `page` only).
- Place custom templates in a `templates/` subdirectory or in the theme root.

---

## Best Practices Summary

### Theme File Organization

- Keep `functions.php` as a routing file that includes focused files from `inc/`.
- Group related functionality: `inc/theme-support.php`, `inc/enqueue.php`, `inc/template-tags.php`, `inc/customizer.php`.
- Place custom page templates in `templates/` or the theme root with a `Template Name:` header comment.
- For block themes, use `templates/` for full page templates and `parts/` for reusable template parts.

### Asset Enqueuing

- Always use `wp_enqueue_style()` and `wp_enqueue_script()` -- never hardcode `<link>` or `<script>` tags in templates.
- Use `get_template_directory_uri()` for parent theme assets and `get_stylesheet_directory_uri()` for child theme assets.
- Version assets with the theme version constant for cache busting.
- Use the array syntax for `wp_enqueue_script()` with `'in_footer' => true` and `'strategy' => 'defer'` for non-critical scripts.

### Child Theme Development

- The `Template` header in `style.css` must match the parent theme's directory name exactly.
- Enqueue child styles with the parent style handle as a dependency.
- Use a higher priority number (e.g., 20) on `wp_enqueue_scripts` so the parent loads first.
- Override parent `after_setup_theme` at priority 11 or higher.
- Use `remove_action()` / `remove_filter()` at `init` to remove parent hooks (requires matching function name, priority, and argument count).

### Block Theme (FSE) Development

- Define all design tokens (colors, spacing, typography) in `theme.json`, not in CSS files.
- Set `defaultPalette` and `defaultGradients` to `false` to enforce your custom palette.
- Use `useRootPaddingAwareAlignments` for correct full-width block behavior.
- Use fluid typography with `min`/`max` values for responsive font scaling without media queries.
- Register custom templates in the `customTemplates` array and template parts in `templateParts`.

### Escaping and Sanitization in Templates

- `esc_html()` for text content inside HTML tags.
- `esc_attr()` for values inside HTML attributes.
- `esc_url()` for URLs in `href`, `src`, and `action` attributes.
- `wp_kses_post()` for rich HTML that should allow post-safe tags.
- Always sanitize Customizer settings with an appropriate `sanitize_callback`.

### Performance

- Register only the theme supports you actually need.
- Conditionally load scripts (e.g., `comment-reply` only when comments are open).
- Use lazy loading (`loading="lazy"`) on images below the fold.
- Use the `'strategy' => 'defer'` parameter for non-critical JavaScript.
- Define a `content_width` global to prevent oversized embeds.

### Accessibility

- Use semantic HTML elements (`<main>`, `<nav>`, `<article>`, `<aside>`, `<header>`, `<footer>`).
- Include skip-to-content links as the first focusable element.
- Use proper heading hierarchy (h1 > h2 > h3, never skip levels) and meaningful `alt` attributes on all images.
