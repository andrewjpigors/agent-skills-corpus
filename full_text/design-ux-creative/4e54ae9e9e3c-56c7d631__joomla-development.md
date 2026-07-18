---
name: joomla-development
description: Use when working anywhere under component/ or plugins/, on build scripts (scripts/build-*.py, install-to-staging.py), staging installs, or version bumps for AI Boost for Joomla. Covers plugin and component anatomy, manifest XML rules, Pro-gating, the numbered gotchas, and branding rules.
---

# Joomla Development Skill — AI Boost for Joomla

## When to load this skill

Load this skill any time you are working on:
- Any file inside `component/` (plugins, component, lib, package)
- Build scripts (`scripts/build-*.py`, `scripts/install-to-staging.py`)
- Staging installs or version bumps
- Any task plan that touches plugin or component PHP code

> **Source validation:** The facts in this skill were re-verified directly against the live tree
> on 2026-07-04 (order 0090): `component/Version.php`, `component/package/pkg_aiboost.xml`,
> `component/package/pkg_script.php`, `component/plugins/system/aiboost_schema/aiboost_schema.{php,xml}`,
> `component/plugins/system/aiboost_core/aiboost_core.php`, `component/lib/src/` (full listing),
> `component/lib/src/PluginRegistry.php`, `scripts/build-package-zip.py`,
> `scripts/install-to-staging.py`, plus a real staging build+install. Update this skill whenever
> source code diverges. **OPERATING.md wins on any conflict.**

> **Authoritative roster:** the full plugin→SKU map is `component/lib/src/PluginRegistry.php` (14
> plugins). `scripts/build-package-zip.py`'s `PLUGIN_NAMES` / `PRO_PLUGIN_NAMES` /
> `INTEGRATION_PLUGIN_NAMES` arrays define what ships in each build variant.
> `component/package/pkg_aiboost.xml` lists what the outer Free ZIP bundles and may lag — trust
> `PluginRegistry.php` + the build script over the package manifest.

---

## Branding (non-negotiable)

| Correct | Never use |
|---------|-----------|
| **AI Boost for Joomla** | ~~JoomlaBoost~~, ~~AI Boost Now~~ |
| **AI Boost** (brand) | — |
| Domain: `aiboostnow.com` | — |

Single source of truth: `CLAUDE.md` → "Non-negotiable rules → Branding".

---

## Package Architecture

**Authoritative plugin→SKU roster: `component/lib/src/PluginRegistry.php`.** CLAUDE.md's
"System plugins" table mirrors it. There is **no** standalone `aiboost_seo` — canonical URL +
robots meta live inside `aiboost_core`. `aiboost_aeo` is **Free** (Pro AEO is the separate
`aiboost_aeo_pro` decorator). Current tree = **14 system plugins** under
`component/plugins/system/`:

| Plugin | Tier | Role |
|---|---|---|
| `aiboost_core` | Free | Bootstraps lib; ordering = 1 (enforced by pkg_script postflight); owns canonical URL + robots meta |
| `aiboost_schema` | Free | Schema.org JSON-LD |
| `aiboost_sitemap` | Free | XML sitemap + basic hreflang |
| `aiboost_social` | Free | OpenGraph + Twitter Cards |
| `aiboost_analytics` | Free | Analytics tag injection |
| `aiboost_code` | Free | Custom code injection (head/body/footer) |
| `aiboost_aeo` | Free | llms.txt + IndexNow |
| `aiboost_schema_pro` | Pro | Schema.org Pro decorator |
| `aiboost_social_pro` | Pro | Social Pro decorator |
| `aiboost_aeo_pro` | Pro | AEO Pro decorator |
| `aiboost_code_pro` | Pro | Custom code Pro decorator |
| `aiboost_hreflang_pro` | Pro | Full hreflang Pro decorator |
| `aiboost_int_falang` | Integration | Falang hreflang bridge (Free bridge; Pro payload fenced) |
| `aiboost_int_yootheme` | Integration | YOOtheme Pro schema mapping (Free bridge; Pro payload fenced) |

The build-script arrays match this split: `PLUGIN_NAMES` (7 Free) · `PRO_PLUGIN_NAMES` (5) ·
`INTEGRATION_PLUGIN_NAMES` (`aiboost_int_falang`, `aiboost_int_yootheme`) in
`scripts/build-package-zip.py`. **The `pkg_aiboost-{version}.zip` Free package bundles the
component + the 7 Free plugins only** (confirmed: `pkg_aiboost.xml` lists exactly those 8 sub-ZIPs).
The 5 `_pro` decorator plugins ship in the separate Pro package (`pkg_aiboost_pro`), and the
integration bridges ship as their own add-on packages (`pkg_aiboost_yootheme` /
`pkg_aiboost_falang` via `scripts/build-addon-zip.py`) — see Add-on Plugins below.

**Version source of truth:** `component/Version.php`
- Build scripts inject this version into every manifest and installer script
- Never manually edit `<version>` in any XML — the build script does it

**Shared lib:** `component/lib/src/` (namespace `AiBoost\Lib`) — `PluginRegistry`,
`ConflictManager`, `ConflictPolicy`, `LicenseValidator`, `HeadBlockBuilder`, `BodyBlockBuilder`,
`HealthCheckService`, the `Page/` resolver, the `Manifest/` definitions, the `Cms/` adapters,
and the service classes.
- **Plugins no longer bundle their own copies of these classes.** Each plugin loads the shared
  lib from the installed component via `com_aiboost/lib/autoload.php` (see Entry Point). The old
  per-plugin `lib/src/` copy model **and the `ProGate.php` trait were removed in P01** — do not
  reintroduce either. Plugins therefore hard-depend on `com_aiboost` being installed (they no-op
  gracefully if it is absent).

---

## Plugin Anatomy

Every plugin follows this exact structure:

```
aiboost_{slug}/
├── aiboost_{slug}.php        ← Legacy entry point (REQUIRED — see Class Alias section)
├── aiboost_{slug}.xml        ← Manifest (REQUIRED) — <files> lists only src + language
├── src/
│   ├── Extension/
│   │   └── AiBoost{Slug}.php ← Main plugin class (extends CMSPlugin)
│   ├── Service/             ← Feature services (Pro ones stripped from Free via FREE_EXCLUDE)
│   └── Features/            ← Manifest-codegen'd Pro feature stubs (Pro plugins only)
└── language/
    └── en-GB/
        ├── plg_system_aiboost_{slug}.ini
        └── plg_system_aiboost_{slug}.sys.ini
```

There is **no `lib/` folder inside the plugin** and **no `script.php`** — the shared lib is
loaded from the installed component (see Entry Point) and install-time ordering/cleanup lives in
the package's `pkg_script.php`. Only `en-GB` ships until the product is final (the other language
packs are added later, on request).

---

## Plugin Entry Point (`aiboost_{slug}.php`)

This file does three things in this exact order (verbatim from `aiboost_schema.php`):

```php
<?php
defined('_JEXEC') or die;

// 1. Load the shared lib from the INSTALLED component (single autoloader — no
//    per-plugin copies). Bail out gracefully if com_aiboost is absent (uninstalled
//    separately, failed update, partial deploy) so a fatal never takes down the site.
$loader = JPATH_ADMINISTRATOR . '/components/com_aiboost/lib/autoload.php';
if (!file_exists($loader)) {
    return;
}
require_once $loader;

// 2. Load the real extension class
require_once __DIR__ . '/src/Extension/AiBoost{Slug}.php';

// 3. Register legacy class alias (see Class Alias section)
if (!class_exists('PlgSystemAiboost_{slug}', false)) {
    class_alias(
        \AiBoost\Plugin\System\AiBoost{Slug}\Extension\AiBoost{Slug}::class,
        'PlgSystemAiboost_{slug}'
    );
}
```

`aiboost_core` follows the **same** shape — it loads the shared autoload, its own
`src/Extension/AiBoostCore.php`, and aliases `PlgSystemAiboost_core`. (Historical note: it used
to be a lib-bootstrap-only stub; the bootstrapping now happens through the component's
`lib/autoload.php`, which every plugin shares.)

---

## Class Alias Pattern (critical — never skip)

Joomla 3/4/5/6 legacy loader constructs the class name as:
```
PlgSystem + ucfirst($element)
```

For `element = aiboost_schema`:
- `ucfirst('aiboost_schema')` = `'Aiboost_schema'`
- Expected class: `PlgSystemAiboost_schema`

The real class lives in a namespaced path. Without the alias, Joomla cannot find it.

**Rule:** Every plugin entry point MUST register `PlgSystem{ucfirst(element)}` as a class alias pointing to the namespaced class. Check the alias in `aiboost_schema.php` as the reference.

---

## Manifest XML Rules

Required fields (every plugin):
```xml
<?xml version="1.0" encoding="utf-8"?>
<extension type="plugin" group="system" method="upgrade">
  <name>PLG_SYSTEM_AIBOOST_{SLUG}</name>           <!-- language constant, NOT plain text -->
  <version>0.0.0</version>                          <!-- placeholder — the build script injects component/Version.php -->
  <description>PLG_SYSTEM_AIBOOST_{SLUG}_XML_DESCRIPTION</description>
  <php_minimum>8.1.0</php_minimum>
  <joomla_minimum>5.0.0</joomla_minimum>
  <namespace path="src">AiBoost\Plugin\System\AiBoost{Slug}</namespace>
  <files>
    <filename plugin="aiboost_{slug}">aiboost_{slug}.php</filename>
    <folder>src</folder>
    <folder>language</folder>
    <!-- no <folder>lib</folder> — the shared lib loads from the installed component -->
  </files>
  <languages>
    <language tag="en-GB">language/en-GB/plg_system_aiboost_{slug}.ini</language>
    <language tag="en-GB">language/en-GB/plg_system_aiboost_{slug}.sys.ini</language>
    <!-- ... other language tags ... -->
  </languages>
  <config>
    <fields name="params">
      <!-- fieldsets here -->
    </fields>
  </config>
</extension>
```

Critical rules:
- `method="upgrade"` is MANDATORY — without it reinstall fails
- `<name>` must use a language constant (not plain text) — Joomla uses it in the Extensions list
- `<namespace path="src">` declares the PSR-4 root; Joomla autoloads from `src/`
- `<filename plugin="aiboost_{slug}">` — the `plugin` attribute tells Joomla which file is the entry point
- Version is injected by the build script — never hardcode it manually

---

## `showon` Attribute Syntax

Used in XML `<field>` and `<fieldset>` to conditionally show/hide:

```xml
<!-- NOTE: showon="license_tier:pro" is RETIRED — Pro gating is the Vue <ProGate>
     + the perpetual pro_activated flag (see "Pro Gating" below), not XML showon. -->

<!-- Show for multiple schema_type values -->
<field name="specific_price_range"
       showon="schema_type:localbusiness[OR]schema_type:restaurant[OR]schema_type:hotel" />

<!-- Show when a toggle is off (value = 0) -->
<field name="hours_mon_opens" showon="hours_mon_closed:0" />
```

Rules:
- `[OR]` joins multiple conditions — no spaces around it
- `[AND]` also available for AND logic
- Use `showon` on `<fieldset>` to hide the entire group
- `showon` on a `<fieldset>` does NOT prevent the fields inside from saving — only hides them visually

---

## Pro Gating (CURRENT model — perpetual activation; updated order 0017)

> The old `ProGate` trait / `isProEnabled()` / `license_tier` / `showon="license_tier:pro"` model is
> **RETIRED**. The `ProGate` trait and `AbstractService::isProTier()` were **deleted**;
> `ProFeatureRegistry::stripLocked()` is a **no-op**. Do not reintroduce any of them.

**One gate, one flag.** `PluginRegistry::isProActive(array $settings): bool` is the single source of
truth — it returns true iff `pro_activated === '1'`. That flag is set **once** by
`PluginRegistry::markPerpetualActivation()` the first time a real key verifies active against our licence
server, and is **never cleared** (licence expiry only pauses updates/support, never relocks features).
**Never gate on `license_tier`, `license_state`, or the heartbeat** — they drift on expiry and caused the
historical relock bugs. `license_tier` is written only as a Health *diagnostic*, never read as a gate.

**Runtime emission** — every Pro front-end feature lives **inside the corresponding FREE plugin**, behind:

```php
use AiBoost\Lib\PluginRegistry;

public function onBeforeCompileHead(): void
{
    $settings = /* the request-cached settings blob */;
    if (class_exists(SchemaProBuilder::class) && PluginRegistry::isProActive($settings)) {
        // Pro-only code. The Pro class is FREE_EXCLUDE-stripped from the Free
        // build, so class_exists() is already false there (belt + braces).
    }
}
```

Per-language overlays additionally require the integration SKU, e.g.
`PluginRegistry::isProActive($settings) && PluginRegistry::hasPro('int_falang')`.
**Integrations are perpetual too (order 0143):** `hasPro('int_*')` gates on the
per-integration flag (`int_falang_activated` / `int_yootheme_activated`) — set once by
`saveLicenseState()` on the first verified-active key for that integration, never
cleared. It never reads the live `license_state` status (which drifts on expiry — the
old integration relock bug). The flags live on `SYSTEM_PRESERVED_KEYS` like
`pro_activated`, and `pkg_script::migrateActivateIntegrationPerpetual()` backfills
them for pre-0143 integration customers on upgrade.

**Three things keep Pro out of the Free edition** (defence in depth):
1. **Physical build** — `scripts/build-package-zip.py` strips every Pro Service/Feature class
   (`FREE_EXCLUDE`) and every `// @pro:start … // @pro:end` block; `verify-no-pro-leakage.py` runs STRICT
   and fails the build on any leaked token (`ProGate::`, `isProEnabled(`, `@pro`, …).
2. **Save fence** — `SettingsSaveDefinition::SYSTEM_PRESERVED_KEYS` + `mergeSystemPreservedKeys()` (fail-closed
   both ways) means a client cannot POST/import `pro_activated=1` to self-promote.
3. **Server** — `LicenseValidator::verify()` fails closed on store/product-pin mismatch or any transport error.

**Admin UI** — the Vue bootstrap `isPro` flag (from `HtmlView::buildBootstrap`, itself `isProActive()`)
drives every `<ProGate>`. Wrap a Pro card/field with `<ProGate mode="card">` / `<ProGate mode="field">`
— but **never** with a `gate-key="…"` feature/route lock (the `ProFeatureRegistryParityTest` fails the
build if one reappears). There is no per-plugin `license` fieldset / `showon="license_tier:pro"` anymore;
the SPA owns Pro presentation.

**Manifest tier** — a Pro setting declares `'tier' => 'pro'` in `component/lib/src/Manifest/*.php`; codegen
derives its `.ini`/partial/Health stubs. Functional gating still comes from the runtime guard + physical
build above, not from the tier metadata. Authoritative deep-dive: `docs/analysis/licensing-and-pro-gating.md`.

---

## Conflict handling (ConflictManager + ConflictPolicy + DocumentInspector)

AI Boost avoids double-emitting output that a competitor (4SEO, Yoast-style plugins) or a sibling
AI Boost plugin already produces. Three current pieces (loaded from the shared component lib — the
old `ensureConflictManager()` / `ProGate` lazy-loader is **gone**):

- **`ConflictManager`** — a static registry of output *slots*: `claim(string $slot, string
  $pluginName, string $reason = '')`. Slot constants (`ConflictManager::SLOT_*`) include
  `SLOT_SCHEMA_ORG`, `SLOT_SCHEMA_FAQ`, `SLOT_OG_TAGS`, `SLOT_CANONICAL`, `SLOT_HREFLANG`,
  `SLOT_ROBOTS_TXT`, `SLOT_META_ROBOTS`, `SLOT_SITEMAP`, `SLOT_SITEMAP_XML`, `SLOT_LLMS_TXT`,
  `SLOT_INDEX_NOW`. Integration bridges declare the slots they own via `claimsSlots: [...]` in
  their `IntegrationDescriptor` (see `aiboost_int_yootheme` / `aiboost_int_falang`).
- **`ConflictPolicy`** — the user-facing takeover/defer decision from the Conflict Manager feature
  (the `/conflicts` Vue page + first-run wizard). Per feature, the site owner chooses whether AI
  Boost takes over or defers to the competitor; the policy is persisted read-modify-write into the
  settings blob (never a full-replace).
- **`DocumentInspector::shouldSkip()`** — the runtime check a Free plugin calls before emitting: if
  another extension already produced this output (or policy says defer), the plugin cooperatively
  skips and calls `HeadBlockBuilder::noteSkip($section, 'reason')` so the consolidated block shows a
  `<!-- Skipped: … -->` line instead of silent absence (gotcha L020/L021).

**Do not reintroduce the old `onAfterInitialise` + `ConflictManager::claim(SLOT_*)` + `ProGate`
pattern in a Free plugin** — that shape survives only in the integration descriptors. New skip
logic goes through `DocumentInspector` / `ConflictPolicy`.

---

## Language Files

Two files per language per plugin:

| File | Purpose |
|------|---------|
| `plg_system_aiboost_{slug}.ini` | Labels/descriptions shown in plugin config form |
| `plg_system_aiboost_{slug}.sys.ini` | Plugin name/description shown in Extensions list |

Naming convention for constants:
```ini
; .sys.ini
PLG_SYSTEM_AIBOOST_SCHEMA="AI Boost — Schema.org"
PLG_SYSTEM_AIBOOST_SCHEMA_XML_DESCRIPTION="Generates Schema.org JSON-LD..."

; .ini
PLG_SYSTEM_AIBOOST_SCHEMA_FIELDSET_LICENSE="License"
PLG_SYSTEM_AIBOOST_SCHEMA_LICENSE_KEY_LABEL="License Key"
PLG_SYSTEM_AIBOOST_SCHEMA_ORG_NAME_LABEL="Organization Name"
```

Rules:
- **Only `en-GB` until the final version** — do NOT touch `de-DE`, `fr-FR`, etc.
- All string values must be in double quotes
- No trailing spaces
- Constants are ALL_CAPS with underscores
- String values may contain HTML but must be on one line

---

## Shared Lib (loaded from the component, not bundled)

`component/lib/src/` (namespace `AiBoost\Lib`) holds the shared classes used by all plugins. **The
plugins do NOT carry their own copies.** Each plugin's entry point requires
`JPATH_ADMINISTRATOR . '/components/com_aiboost/lib/autoload.php'`, which resolves every
`AiBoost\Lib\*` class from the installed component at runtime. The build script confirms this in a
comment: *"Plugins no longer bundle lib/ classes — ProGate/ConflictManager removed in P01."*

Consequences to remember:
- A plugin **hard-depends on `com_aiboost` being installed**. If the loader file is missing the
  plugin `return`s early (no-op) rather than fataling — see Entry Point.
- The build no longer copies `ProGate` / `ConflictManager` / `LicenseValidator` into plugin ZIPs.
  `ProGate.php` no longer exists at all; `ConflictManager` and `LicenseValidator` live only in the
  component lib.
- Because there is one physical copy per site, the old double-load `class_exists` / `trait_exists`
  guards are no longer needed at the plugin boundary (the component autoloader owns loading).

---

## aiboost_core Plugin (Special Rules)

- **Joomla ordering = 1** so it runs before the feature plugins. Ordering is enforced by the
  **package's `component/package/pkg_script.php` `postflight()`** — `aiboost_core` itself has **no
  `script.php`**.
- It is a normal plugin (`src/Extension/AiBoostCore.php`), not an empty bootstrap stub. Besides
  ensuring the shared lib is available first, it **owns the canonical URL + robots meta** output
  and takes part in the ConflictPolicy/DocumentInspector cooperative-skip flow like the others.
- The package installs it ahead of the feature plugins; when installing loose plugin ZIPs, install
  `aiboost_core` first.

---

## Build Workflow

### Build the one-product package (the ONE build path)
```bash
python3 scripts/build-package-zip.py
```
Output: `deliverables/plugin/pkg_aiboost-{version}.zip`.

This is the ONLY supported build path. It rebuilds the Vue admin bundle, runs the
manifest codegen `--check`, strips every `// @pro:start/@pro:end` block + every
FREE_EXCLUDE Pro class from the Free build, and STRICT-verifies no Pro leakage. The
old per-plugin `build-component-plugins.py` was removed in order 0057 · P0-4 — it
copied plugin dirs verbatim with NO stripping, so it could ship a whole Pro class in
a "free" plugin ZIP.

**The single package ZIP installs cleanly on Joomla 5 and 6.** (Re-proven order 0090:
`pkg_aiboost-0.90.3.zip` installed successfully on the Joomla 6.1 staging site via
`install-to-staging.py`.) The old belief that "the outer package ZIP fails on Joomla 6.1, use
individual ZIPs" is **false** — the package ZIP is the routine path `install-to-staging.py`
auto-detects and installs.

### Build add-on ZIPs
```bash
python3 scripts/build-addon-zip.py
```

---

## Staging Deploy & Definition of Done

**The Definition of Done lives in `OPERATING.md` ("Build, verify & close") — that is the
authority; OPERATING.md wins on any conflict. This section is a pointer, not a second copy.**
Never finish a plugin/component task from a build alone — verify on staging first.

The DoD requires (see OPERATING.md for the full ordered list):

1. **Bump the version** (`component/Version.php`) before building — patch = fix/tweak, minor =
   new feature/field/tab. (Order 0090 is docs-only, so it does NOT bump.)
2. **Build:** `python scripts/build-package-zip.py`.
3. **Install on a Pro AND a Free test site** — Free and Pro share one codebase, so every change is
   Free-affecting; never verify Pro only. Routine:
   `python _creds_run.py scripts/install-matrix.py --sites j6pro,j6free` (add `j5pro,j5free` when
   an install/schema path changed). `staging.offroadserbia.com` (Pro) and `offroadbalkans.com`
   (Free) are the live sites — touched only at release.
4. **Schema / `install.sql` / `pkg_script.php` changes only** — run the clean-uninstall verifier
   on **both** targets: `python scripts/verify-clean-uninstall.py --target pro` and `--target free`.
5. **Verify the artifact** — open each admin Dashboard, confirm the feature works, the relevant
   **Health** item passes, the front-end artifact (meta tag / JSON-LD / script) actually appears,
   and that Pro-gated surfaces render **locked** on Free.

**Before judging staging output, check the environment first (or you WILL misread it):**
- **Conflict Manager mode** — staging often runs a competitor (4SEO); if AI Boost is in `defer` it
  cooperatively **skips** overlapping output, so "no output" can mean "correctly deferred". Read
  AI Boost's own consolidated `<!-- AI Boost for Joomla -->` block, or set takeover then restore.
- **Pro licence active** — Pro output only emits when `pro_activated='1'` (a Pro *install* does not
  auto-activate). Confirm a real key is active or DB-seed `pro_activated='1'` before judging Pro
  output as missing.

**Credentials:** run the scripts through `_creds_run.py` from the wrapper root (it loads
`CREDENTIALS.local.md` into env — `STAGING_*`, matrix sites — and sets cwd to `aiboost-joomla/`):
`python _creds_run.py scripts/install-to-staging.py`. On this Windows machine plain `python`
works and every Python script should be prefixed with `PYTHONIOENCODING=utf-8` (several print a
Unicode arrow and crash under cp1252 *after* writing the file). If the installer hits an IP block:
`https://staging.offroadserbia.com/administrator/index.php?admintools_rescue=EMAIL`.

---

## Visual verification (subagent)

Run UI verification in a Task subagent so screenshots never enter the main context.
The main task receives only the subagent's text verdict.

- One screen, one theme (preferred — targeted):
  `python _creds_run.py scripts/_visual_admin_walk.py --target free --outdir artifacts/single-screen --only <screen>`
  (use `--target pro` for the Pro edition)

- One screen, BOTH themes (no targeted tool yet — fallback):
  subagent runs the full `scripts/ui-audit-screenshots.js`, then inspects and judges ONLY the
  two relevant PNGs in `artifacts/ui-audit/{light,dark}/`. Context cost stays low (only the
  verdict returns); disk/time cost is not yet optimised — see BACKLOG note.

- Theme coverage follows the CLAUDE.md rule: both light+dark only when the change touches shared
  CSS/tokens, layout, or adds/changes a component; one theme for isolated text/content edits.

- Subagent brief (form): general-purpose Task — "run <command>, open the PNG(s), return 2–4
  sentences on layout / overflow / contrast. Do NOT return the image. If anything is off or
  uncertain, say so explicitly."

---

## Release & verification techniques

The **Definition of Done is OPERATING.md's** — this is a toolbox of proven checks, not a second DoD.
Reach for these when a plain staging install is not enough to be sure a change is correct:

- **Golden-diff the consolidated block.** For output changes (schema / OG / AEO / analytics /
  canonical), `curl -s {site}/` and byte-compare the `<!-- AI Boost for Joomla - Start … End -->`
  block before vs after. A clean diff shows exactly what moved and proves nothing else did.
- **Same-version stash/compare (defeats the stale-Free-site version lag).** When a Free site still
  runs an older build, a naive before/after shows false deltas that are just the version bump. Build
  the *before* and *after* at the **same** version (stash the change, build, capture; unstash, build,
  capture) so the only difference is your edit.
- **OFF → ON → OFF live round-trip.** Toggle a feature off, capture; on, capture; off again — the
  first and third captures must match. Proves the toggle is reversible and leaves no residue.
- **Clean no-4SEO Pro sites for schema/canonical.** `j5pro` / `j6pro` (testmyweb) run without a
  competitor, so AI Boost's own schema/canonical output is unambiguous there — no Conflict-Manager
  defer to reason about. (A clean no-4SEO Free site exists too.)
- **`publish-release-to-updates.py` end-to-end proof.** After a real release, verify the update feed
  advertises the new version + correct sha256 AND that a real Joomla "Update" actually installs it —
  not just that the ZIP built. (Release runbook + the update-server flow live in OPERATING.md /
  `docs/`.)

## Version Management

**Single source of truth: `component/Version.php`**

```php
final class Version {
    public const VERSION = '0.90.3';   // illustrative — read the file for the live value
    // ...
}
```

Version is injected by build scripts into:
- All plugin XML manifests (`<version>` tag)
- `com_aiboost.xml`
- `pkg_aiboost.xml`
- Installer script `VERSION` constants

**Bumping versions:**

For the component package, bump the single source of truth `component/Version.php` (the build injects it into every manifest):
```bash
python3 scripts/bump-version.py patch   # patch = fix, minor = new field/feature
python3 scripts/build-package-zip.py
```

For the legacy plugin (archived, `plugin/src/`):
```bash
python3 scripts/bump-version.py patch
```

**Rule:** Always bump version before building a ZIP that will be installed anywhere.
- Patch (+0.0.1): bug fixes, small tweaks
- Minor (+0.1.0): new features, new tabs/fields
- Major: breaking changes (rare)

---

## com_aiboost Component

Admin URL: `/administrator/index.php?option=com_aiboost`

Structure:
```
com_aiboost/
├── com_aiboost.xml               ← Component manifest
├── vue-admin/                    ← SPA SOURCE OF TRUTH (Vite + Vue 3 + vue-router 4)
│   └── src/                        (App.vue, AppShell.vue, Sidebar.vue, router.js, main.js,
│                                    navigation.js, *Page.vue, tabs/, components/, composables/)
├── media/                        ← BUILD OUTPUT (admin-vue.js + ab-tokens.css/ab-components.css
│                                    copies + legacy dashboard/health/import/settings.js) — never hand-edit
└── admin/
    ├── com_aiboost.php           ← Entry point (MVC bootstrap)
    ├── script.php                ← Component installer script
    ├── access.xml                ← ACL
    ├── css/                      ← ab-tokens.css, ab-components.css, admin.css (authoring copies)
    ├── js/                       ← legacy per-view JS (settings.js, import.js, dashboard.js, …)
    ├── language/en-GB/
    ├── lib/autoload.php          ← PSR-4 loader for AiBoost\Lib (what plugins require)
    ├── services/provider.php     ← Joomla DI container
    ├── sql/install.sql           ← Creates #__aiboost_settings + #__aiboost_translations
    └── src/Administrator/        ← MVC: Controller, Extension, View, tmpl/ (incl. tmpl/app/default.php)
```

DB tables:
| Table | Purpose |
|-------|---------|
| `#__aiboost_settings` | Single-row JSON blob (key=`main`) |
| `#__aiboost_translations` | Per-field, per-language text values |

**Admin UI tech stack: a Vue 3 SPA — NOT vanilla PHP/JS.** `view=app` is the real single-page app
(hash router, boots from the inline `window.aiBoostBootstrap`), authored in
`component/com_aiboost/vue-admin/src/` and built into `media/` by `pnpm build` (which
`build-package-zip.py` runs automatically). `admin/tmpl/app/default.php` renders only
`<div id="ab-app">` + the bootstrap `<script>` + the token/component CSS + the SPA bundle. The route
table (`/dashboard`, `/settings`, `/health`, `/integrations`, `/analyzers`, `/licenses`,
`/conflicts`, `/redirects`, `/urlchecker`, `/import`, `/help`, `/changelog`, hidden `/_styleguide`)
lives in `vue-admin/src/router.js`; CLAUDE.md's "Vue SPA routes" table mirrors it.

**Dual-mount + load-bearing legacy views (order 0051 map).** `main.js` mounts the full SPA when
`#ab-app` exists, otherwise falls back to per-ID mounts on the thin legacy `view=X` shells. Of the 9
legacy `view=X` pages, **5 are load-bearing data endpoints the SPA fetches — do NOT delete them:**
`dashboard`, `settings`, `health`, `integrations`, `analyzer`. The other 4 (`redirects`,
`urlchecker`, `import`, `help`) are dead shells. Any unregistered `view=` already falls back to the
SPA. See gotchas **L015** (SPA shell + hash router), **L016** (`--ab-*` token system, no fighting
Bootstrap), **L017** (migrating a legacy view to a Vue page) for the working patterns.

---

## Integration bridges / Add-on Plugins (Separate Distribution)

The integration bridges are NOT bundled in `pkg_aiboost`. Each is a plugin element under
`component/plugins/system/` that requires paid third-party software, packaged as its own add-on ZIP:

| Plugin element | Add-on package | Requires |
|---|---|---|
| `aiboost_int_yootheme` | `pkg_aiboost_yootheme-{version}.zip` | YOOtheme Pro |
| `aiboost_int_falang` | `pkg_aiboost_falang-{version}.zip` | Falang Pro |

Each bridge builds a **Free** variant (Pro blocks stripped; installable in the base distribution)
and a **Pro** variant (`plg_system_aiboost_int_*_pro`, the licence-gated payload).

Build: `python scripts/build-addon-zip.py` (`--addon yootheme|falang`), or via
`build-package-zip.py --integration=<name>` / `--target=all`.
Install: manually via Joomla Extension Manager after `pkg_aiboost`.

---

## Joomla Event System

Plugins subscribe to events by implementing methods with the `on` prefix, or explicitly via `getSubscribedEvents()`:

```php
// Auto-subscription (CMSPlugin scans for on* methods)
public function onBeforeCompileHead(): void { ... }
public function onAfterInitialise(): void { ... }
public function onAfterRender(): void { ... }

// Explicit subscription (preferred, modern Joomla style)
public static function getSubscribedEvents(): array
{
    return [
        'onBeforeCompileHead' => 'handleHead',
        'onAfterInitialise'   => 'handleInit',
    ];
}
```

Key events used by AI Boost plugins:
| Event | When | Used by |
|-------|------|---------|
| `onAfterInitialise` | Early request — before routing | ConflictManager slot claiming |
| `onBeforeCompileHead` | Just before `<head>` output | Schema, Social, SEO, AEO |
| `onBeforeRender` | Just before full page output (buffered body available) | Code injection, body-level modifications |
| `onAfterRender` | After full page render (response body in `$app->getBody()`) | Sitemap response, post-render body rewrites |
| `onExtensionAfterSave` | After settings/config save | Sitemap search-engine ping (`aiboost_sitemap`) |

---

## Lessons Learned / Gotchas

**L001 — Tab label conflict (Task #90)**
The old monolithic plugin was adding `<script>` tags that overwrote CSS classes used by ALL Joomla plugins' tab labels. Fix: scope CSS selectors to `#com_plugins .aiboost-*` to avoid global namespace pollution. Any admin CSS must be scoped to the plugin's own form container.

**L002 — Class alias for legacy loader**
Joomla's plugin loader calls `new PlgSystem{ucfirst($element)}()`. Without the `class_alias()` in the entry point, the plugin silently fails to load — no error, just missing functionality. Always verify the alias matches exactly: `PlgSystemAiboost_schema` (note the underscore is preserved by `ucfirst`).

**L003 — ProGate trait redeclaration (fixed v0.7.0; now HISTORICAL)**
*Historical:* this applied when each plugin bundled its own `lib/src/` copies. Since P01 the plugins
load one shared copy from the component autoloader (see Shared Lib), so the per-plugin double-load
guards are no longer needed and `ProGate.php` no longer exists. The general lesson still holds if you
ever re-introduce a bundled trait: guard shared traits/classes with `if (!class_exists /
!trait_exists)` so multiple includes don't fatal.

**L004 — Version sync across files (Tasks #93, #95)**
Never manually edit `<version>` in XML manifests — the build script injects from `Version.php`. The old PowerShell build script was removed in favor of Python scripts. Use `scripts/build-package-zip.py` for the component package.

**L005 — the single `pkg_aiboost` package ZIP is the install path (old "it fails on J6.1" belief is FALSE)**
The outer package ZIP (`pkg_aiboost-*.zip`) installs **cleanly on Joomla 5 and 6**. Re-proven order
0090: `pkg_aiboost-0.90.3.zip` installed successfully on the Joomla 6.1 staging site via
`install-to-staging.py` (which auto-detects and installs the package ZIP by default). Use the single
package ZIP; `--all-plugins` (loop individual ZIPs) exists only as an alternative, not because the
package fails.

**L006 — PHP 8.5 CI (Task #103)**
PHP 8.5 was added to the test matrix in `bojancreator/ai-boost-pkg-joomla` GitHub Actions. If new PHP syntax is used, verify it passes on 8.1–8.5. Avoid deprecated dynamic properties — use explicit property declarations.

**L462 — Manifest-first codegen + build-time Pro stripping (Task #462)**
`component/lib/src/Manifest/*.php` is the single source of truth. New fields can declare `feature_class`, `health`, and `i18n` blocks; `scripts/codegen-from-manifest.py` then auto-generates the Pro feature stub at `component/plugins/system/aiboost_{sku}_pro/src/Features/{Class}.php`, appends en-GB `.ini` keys, and `HealthCheckService::registerFromManifest()` registers the Health entry at runtime.

For Pro fields, wrap the array entry between `// @pro:start` and `// @pro:end` — `build-package-zip.py` strips those blocks from the Free ZIP (admin/, lib/, every plugin/) but NOT from Pro plugin ZIPs (those keep their @pro blocks because they ARE the Pro payload). The verifier (`verify-no-pro-leakage.py`) now runs in STRICT mode and fails the build on any leaked Pro token.

Gotcha: never put the literal `@pro:start` … `@pro:end` text in a comment — the stripping regex matches across lines and will eat the surrounding code. Use prose like "opt-in opening/closing markers" instead.

**L007 — `method="upgrade"` is mandatory**
Without `method="upgrade"` in the extension XML, Joomla refuses to reinstall over an existing version. ALWAYS include it.

**L008 — `showon` does not prevent saving**
Fields hidden by `showon` are still saved when the form is submitted. If you need to block saving of hidden Pro fields on Free tier, validate server-side in the plugin's event handler before using the value.

**L009 — aiboost_core ordering**
`aiboost_core` must have Joomla ordering = 1. Its `script.php` sets this automatically via `postflight()`. If you create a new bootstrap-style plugin, copy this pattern. Joomla ordering is global across all system plugins — do not use ordering=1 for feature plugins, only the core bootstrap.

**L010 — Standalone plugin vs component plugin**
Plugins in `component/plugins/system/` are part of `pkg_aiboost` and can depend on `aiboost_core` being installed. Plugins in `plugins/` (now archived/add-ons) are truly standalone and cannot depend on any shared component. Always check which category a new plugin belongs to before writing its lib-loading code.

**L011 — Installer script class naming**
Plugin installer script class must be named `PlgSystem{Ucfirst(element)}InstallerScript`. For `aiboost_core`: `PlgSystemAiboost_coreInstallerScript`. This matches Joomla's naming convention for plugin installers.

**L012 — `defined('_JEXEC') or die` required everywhere**
Every PHP file in a plugin must start with `defined('_JEXEC') or die;` immediately after `<?php`. Without it, the file can be accessed directly via HTTP. No exceptions.

**L013 — subform field type for FAQ/repeatable data**
Use `type="subform"` with `layout="joomla.form.field.subform.repeatable-table"` for repeatable sets of fields (FAQ items, events). Set `multiple="true"` and `max="N"`. The saved value is a JSON object keyed by `item0`, `item1`, etc.

**L014 — Language tag in `<languages>` block**
The `<languages>` block in the manifest must list both `.ini` and `.sys.ini` for every language tag. Missing `.sys.ini` causes the plugin name to show as the raw constant in the Extensions list.

**L015 — Vue SPA shell in Joomla admin component (task #335)**
Trying to win the war against Joomla/YooTheme/Atum Bootstrap class overrides per-component is a losing battle. Instead, mount a single Vue 3 SPA inside one PHP shell view and let Vue Router (hash mode) own all UI routing.

Pattern:
- Add a `view=app` (default view in `DisplayController`) whose `tmpl/app/default.php` renders only `<div id="ab-app"></div>` plus a single inline `<script>window.aiBoostBootstrap = {...}</script>` with CSRF token (`Session::getFormToken()`), base URL, AJAX endpoint URLs, `legacyUrls` for every legacy view (`?option=...&view=X&tmpl=component`), `isPro`, and localized nav labels.
- `vue-router@4` in hash mode — Joomla swallows the path, so only `#/foo` survives. Routes register all Vue pages (`/dashboard`, `/health`, `/settings`, `/integrations`, `/analyzers`, `/help`).
- Component manifest `<menu link="option=com_aiboost&amp;view=app">` so the sidebar opens the SPA, not the legacy dashboard.
- Legacy fallback: `main.js` mounts the SPA only if `#ab-app` exists, otherwise falls back to per-ID mounts. This keeps `&view=dashboard` etc. working for incremental migration.
- For Vue routes that still need data from a legacy PHP view, use a `useLegacyGlobals(viewName)` composable that fetches `legacyUrls[viewName]` (which appends `tmpl=component`) and executes inline `<script>` blocks to populate `window.aiBoost*` globals.
- `api.js` reads CSRF from `window.aiBoostBootstrap.csrf.tokenName` and auto-injects it into POST bodies.
- `useColorScheme()` composable: `MutationObserver` on `<body data-bs-theme>` → reactive ref. Do NOT poll.
- Build script (`scripts/build-package-zip.py`) already runs `pnpm build` in `vue-admin/` automatically.

Gotcha: existing per-ID Vue mounts (`#ab-vue-settings`, `#ab-vue-health`, …) must be preserved during the transition — delete them only after the legacy PHP view is migrated to a Vue route.

**L016 — AI Boost Design System: do not fight Bootstrap (task #336)**
Overriding `--bs-btn-*` per-screen to fix Atum/YooTheme dark-mode regressions is a losing battle: Bootstrap 5.3 reads CSS variables (not plain `color:`), YooTheme widgetkit re-declares `--bs-*` aggressively, and every new tab opens a new override round. Solution — own the surface entirely with a parallel namespace.

Pattern:
- `admin/css/ab-tokens.css` — declare every design value as `--ab-*` (palette, typography, spacing, radius, shadow, focus ring). Scope the root declaration to `body[class*="com_aiboost"]` so tokens never leak to other Joomla admin screens. Cover both Joomla orderings for dark: `body[class*="com_aiboost"][data-bs-theme="dark"]` AND `[data-bs-theme="dark"] body[class*="com_aiboost"]`.
- `admin/css/ab-components.css` — primitives (`.ab-btn`, `.ab-card`, `.ab-input`, `.ab-badge`, `.ab-tabs`, `.ab-alert`, `.ab-tag`, `.ab-toggle`) that consume only `--ab-*` tokens. Never read `--bs-*`. Avoid `!important` unless an upstream `.btn`/`.card` rule wins the cascade; comment why.
- Load both files BEFORE `admin.css` in every `tmpl/*/default.php`, via `HTMLHelper::_('stylesheet', 'com_aiboost/ab-tokens.css', ['relative' => true, 'version' => 'auto'])`.
- Vue mount points migrate `btn btn-outline-*` → `ab-btn ab-btn--ghost`, `btn btn-primary` → `ab-btn ab-btn--primary`, `card` → `ab-card`, etc.
- Reference page: a Vue route `/_styleguide` (registered in `vue-admin/src/router.js`, hidden from the nav) renders every primitive in every variant with a dark/light toggle. Open it after any token change to verify visually.
- Once a view is migrated, delete the corresponding `.btn-outline-*` dark override from `admin.css` — it becomes dead code. Keep transitional `.text-muted`/`.form-text` overrides until every non-Vue view migrates.

Gotcha: scope every component selector with `body[class*="com_aiboost"] .ab-…`, otherwise the classes would render on Joomla front-end pages or other admin contexts if accidentally emitted.

**L017 — Migrating a legacy PHP view to a Vue page (task #337)**
To replace an inline-PHP+JS template (e.g. Redirects, URL Checker, Import) with a Vue SFC living inside the existing SPA bundle:

1. Add a JSON list endpoint to the matching `*Controller` if one does not exist (e.g. `RedirectsController::listJson`). All endpoints must enforce `core.manage` auth + `Session::checkToken()` (for write tasks) and `echo json_encode([...])` + `$this->app->close()` so Joomla never appends the admin chrome.
2. Build the Vue SFC under `vue-admin/src/<Name>Page.vue`. Fetch via `postWithCsrf(makeAdminUrl('controller.task'))` from `api.js` — never craft URLs or token names by hand.
3. Wire it into BOTH router targets in the same change:
   - `router.js` — replace the `LegacyRedirect` stub with the real component (keep `meta.legacyUrl: ''` so AppShell skips the bootstrap fetch).
   - `main.js` — add a `document.getElementById('ab-vue-<slug>')` mount in `mountLegacy()` so the per-view PHP shell still works when users hit `?option=com_aiboost&view=<slug>` directly (Joomla menu items, bookmarks).
4. Reduce the corresponding `tmpl/<view>/default.php` to a thin shell: load `ab-tokens.css`, `ab-components.css`, `admin.css`, `admin-vue.js`, render the nav `<ul class="nav ab-view-nav">`, set `window.aiBoostToken = <?= json_encode($tokenName) ?>`, render `<div id="ab-vue-<slug>"></div>`. Do not delete the `View/<Name>/HtmlView.php` PHP class — Joomla still routes to it; the View just returns the shell. Removing the View class requires also rewriting the routing to land on the SPA `app` view, which is a separate refactor.
5. `python3 scripts/build-package-zip.py` (auto-runs Vue `pnpm build`) → `python3 scripts/install-to-staging.py` → verify on staging admin.

Gotcha: `postWithCsrf` POSTs the CSRF token under its random name (`window.aiBoostBootstrap.tokenName || window.aiBoostToken`). If you forget to inject `window.aiBoostToken` in the per-view shell template, every write task fails with "Invalid security token" but reads (no `Session::checkToken()`) still work — easy to miss until the first toggle/delete.

---

**L018 — Vue ↔ Controller ↔ Service three-way alignment (task #374)**
When a single setting is touched by three layers, ALL three must agree on the key names or the option is silently dead:
1. **Vue tab** (`vue-admin/src/tabs/*.vue`) — `v-model="s[key]"` declares the canonical setting key. Add `:data-ab-field="key"` so Health → Fix-It can scroll to the exact control.
2. **SettingsController** (`admin/src/Administrator/Controller/SettingsController.php`) — every key must appear in the `$fields` whitelist (line ~120+). Missing keys are silently dropped on save. Any controller method that writes derived files (e.g. `regenerateRobotsTxt`) must read the same keys.
3. **Plugin Service** (`plugins/system/aiboost_*/src/Service/*.php`) — runtime emitter reads from the settings array passed in. Must reference the SAME keys as the Vue model.

Symptom of misalignment: toggling a setting in the admin UI appears to save but has no effect on output. The audit found `robots_block_scrapers` (aggregate, used by service) vs `scraper_*` (per-bot, used by Vue) — two parallel models that never met. Fix: pick one canonical model (per-bot wins for UX), whitelist all per-bot keys, refactor both writers, add a one-shot migration in `pkg_script.php postflight` for legacy installs (idempotent: only run if legacy key present AND no new keys saved yet).

Audit checklist when touching a setting key:
- [ ] Vue `v-model` references the key
- [ ] Vue input has `:data-ab-field="key"` for Fix-It scroll
- [ ] Key is in `SettingsController::$fields` whitelist
- [ ] Every controller method that derives files reads the key
- [ ] Every plugin service that consumes the key uses the same name
- [ ] If renaming/replacing an old key, add idempotent migration in `pkg_script.php`
- [ ] Health registry has a corresponding `info_*` / `warning_*` entry in `HealthCheckService::CATEGORIES`

---

**L019 — Detect and prune orphan settings (task #375)**
A setting is an "orphan" when it is saved to the DB but never consumed by any plugin service or controller method — toggling it has zero observable effect. Orphans accumulate when a feature gets descoped but the UI control is left behind. Symptom: user picks an option and saves successfully, but nothing changes on the front-end.

Before adding a new setting, and during periodic audits, run this 4-step check for each key:

```bash
# 1. Vue model declaration (UI exists)
rg -n "v-model[^\"]*[\"\\.]<key>" component/com_aiboost/vue-admin/src/tabs/
# 2. Controller whitelist (save path)
rg -n "'<key>'" component/com_aiboost/admin/src/Administrator/Controller/SettingsController.php
# 3. Plugin service consumers (the only proof the setting drives behaviour)
rg -n "<key>" component/plugins/system/
# 4. Health/Service consumers (cosmetic-only counts as orphan)
rg -n "<key>" component/lib/src/
```

If step 3 returns zero hits AND step 4 only reads the value to render a label, the setting is an orphan. Removal checklist:
- [ ] Delete the form control from the Vue tab
- [ ] Delete the key from `DEFAULTS` in `App.vue`
- [ ] Delete the key from `SettingsController::$fields` whitelist
- [ ] Delete any cosmetic Health check method + its call + its `CATEGORIES` entry
- [ ] Leave existing DB rows alone — the JSON blob will simply stop being updated for that key; old data is inert and harmless (no DROP COLUMN needed because settings are stored as JSON). Add a one-shot stripper in `pkg_script.php postflight` only if the key is large enough to bloat the row.
- [ ] Bump patch version; build; install on staging

Rationale: keeping dead controls in the UI erodes trust ("did my save work?") and creates support load. Removing them is a net UX win even when the underlying DB cleanup is skipped.

---

**L020 — Never emit empty wrapper comments (task #376)**
Debug wrap markers (`<!-- AI Boost: {plugin}/{block} START -->` … `END -->`) must never appear with an empty body between them. Empty pairs:
- pollute production HTML with developer-only artefacts
- mislead the DuplicateTagScanner and human inspectors into believing the feature is active when in fact it has emitted nothing
- misrepresent Cooperative-mode skips (where we deliberately stay silent)

Two structural sources of empty markers — both fixed in #376:

1. **Conditional bodies inside an unconditional wrap.** A block whose body has internal branches that may emit nothing (e.g. `ga4` when `consent === 'gtm'`; `google-verification` when both `gsc_codes` and `gsc_verification_code` are blank) was wrapped with markers before the body branch ran. Fix: build the entire body as a single `$body` string, then call `ConflictMarkerWrapper::wrap($plugin, $block, $body, $wrap)` (in `component/lib/src/`). The helper returns `''` when `trim($body) === ''`; caller short-circuits the `addCustomTag()` call.

2. **Markers around `setMetaData()` / `addHeadLink()`.** Those APIs write to the document's dedicated meta/link streams, NOT via `addCustomTag()`. Wrapping them with `addCustomTag('<!-- … START -->')` produces markers that are always adjacent with no body between them, because the actual `<meta>`/`<link>` tag renders elsewhere in the `<head>`. Two acceptable fixes:
   - **Fix A (preferred when you want a verifiable wrapper):** emit the tag as raw HTML via `addCustomTag('<meta name="…" content="…">')` so it lives in the same head stream as the wrapper comments. The whole block (markers + tags) then renders contiguously and `ConflictMarkerWrapper` can correctly suppress empty bodies. Pattern: build `$body = '<meta …>' . "\n" . '<link …>'`, then `$wrapped = ConflictMarkerWrapper::wrap('plugin', 'block', $body, $wrap); if ($wrapped !== '') $doc->addCustomTag($wrapped);`. Trade-off: you lose Joomla's automatic de-duplication of `<meta name="…">` keys, so add a Cooperative-mode `DocumentInspector::shouldSkip()` guard ahead of the emit when another extension is known to set the same name.
   - **Fix B (when you must use the meta/link stream):** do **not** call the helper at all for those blocks — simply omit the wrapper markers and add an inline comment noting why. Use this when the tag must merge with Joomla core's meta map (e.g. canonical link via `addHeadLink()` where downstream filters expect the dedicated stream).
   Task #377 (C1/C2) chose Fix A for `aiboost_aeo/ai-meta-tags` and `aiboost_aeo/markdown-discovery`; task #376 chose Fix B for `aiboost_perf/canonical` because its presence is consumed by other Joomla canonical-link consumers.

Audit checklist when adding or refactoring a wrap site:
- [ ] Does the block emit via `addCustomTag()`? If not, do not wrap.
- [ ] Is the entire block body buildable as a single string? If yes, use `ConflictMarkerWrapper::wrap()`.
- [ ] Does any internal branch produce an empty body? Trust the helper to short-circuit; never emit `addCustomTag(START)` unconditionally before the body.
- [ ] Verify on staging with `curl -s {site}/ | grep -A0 'AI Boost:'` — every START must have non-empty content before its matching END.

---

**L021 — One consolidated AI Boost head + body block, Yoast/GTM style (tasks #380, #382, #384)**
Every major modern SEO / analytics tool (Yoast, Rank Math, All in One SEO, Google Tag Manager, Meta Pixel) emits **one** clearly-labelled head block with a single outer START/END pair and short sub-section comments inside. AI Boost follows the same convention since v0.33.0; v0.34.0 (#384) inverted the default to "always verbose" (matches Yoast / GTM behaviour) and extended the pattern to `<body>` — GTM noscript, Meta Pixel noscript, custom body code, and custom footer code all consolidate into ONE AI Boost wrapper at the start of `<body>` and ONE just before `</body>`.

**Two render modes (v0.34.0+):**
- **Outer pair is ALWAYS minimal (v0.34.1+):** `<!-- AI Boost for Joomla - Start -->` / `<!-- AI Boost for Joomla - End -->`. No version, no URL — that information already lives in `<meta name="generator">` and would just bloat View Source if repeated on every wrapper. Same compact pair for head, body, and footer.
- **Default (`hide_comments` OFF — production-friendly + verbose, just like Yoast/GTM):** outer pair as above, then sub-section labels (`<!-- Schema.org -->`, `<!-- OpenGraph & Twitter -->`, `<!-- AEO -->`, `<!-- Analytics -->`, `<!-- Custom Code -->`, `<!-- Google Tag Manager (noscript) -->`, `<!-- Custom Body Code -->`, …), `<!-- Also emitted via Joomla head: … -->`, and `<!-- Skipped: … -->` lines all render inside. This is the experience site owners expect — they can see what each plugin is doing in View Source.
- **Hide comments (`hide_comments` ON — minimal source):** only the bare outer pair is emitted, with raw section bodies concatenated inside. No sub-section labels, no `Also emitted` / `Skipped` lines.

`debug_mode` and `hide_comments` are TWO INDEPENDENT toggles in the Debug tab:
- `debug_mode` → controls per-request `error_log` lines from each plugin; no front-end effect.
- `hide_comments` → controls HTML comment density (default 0 = verbose, 1 = minimal); no logging effect.

Any plugin can call `HeadBlockBuilder::setHideComments($hide)` and `BodyBlockBuilder::setHideComments($hide)` from `onBeforeCompileHead` — all read the same setting so last-write-wins is consistent. Call them BEFORE any early-return paths so skip-only contributions still respect the user's preference.

**The rules:**
1. No AI Boost plugin may call `$document->addCustomTag()` for `<head>` content directly. All head HTML flows through `AiBoost\Lib\HeadBlockBuilder::pushSection($section, $body)`.
2. No AI Boost plugin may `preg_replace` directly against `<body>` or `</body>`. All body/footer HTML flows through `AiBoost\Lib\BodyBlockBuilder::pushBody($label, $body)` / `pushFooter($label, $body)` (queued from `onBeforeCompileHead`, never from `onAfterRender` — push order matters for the consolidated wrapper, but finalize order does not).
3. Both builders splice into the rendered page via `onAfterRender` and are idempotent (static flag, first caller wins). All 6 AI Boost plugins call both `HeadBlockBuilder::finalize($app, Version::VERSION)` AND `BodyBlockBuilder::finalize($app)` in their `onAfterRender` — plugin order does not matter.
4. The orphan `ConflictMarkerWrapper` helper was deleted in #384 — body content now flows through `BodyBlockBuilder` which handles wrapper markers + hide-comments respect in one place.

**Fixed head sub-section order (do not reorder):**
1. Schema.org   (`SECTION_SCHEMA`)    — JSON-LD blocks, most important for SEO
2. OpenGraph & Twitter (`SECTION_SOCIAL`) — social-share meta tags
3. AEO          (`SECTION_AEO`)       — AI signals, markdown discovery
4. Analytics    (`SECTION_ANALYTICS`) — GSC/FB verification, GTM, GA4, Meta Pixel
5. Custom Code  (`SECTION_CODE`)      — user-supplied HTML, runs last so it can override

**Body / footer push order:** literal push order is preserved. Convention: analytics noscripts first (Google + Facebook specs want them right after `<body>`), then user-supplied Custom Body Code; footer typically only carries Custom Footer Code.

**Stays outside the block (by design):**
- `<link rel="canonical">` via `addHeadLink()` — Joomla and other extensions dedup the link stream
- `<link rel="alternate" hreflang>` via `addHeadLink()` — same reason
- Anything via `setMetaData()` — writes to dedicated meta map

Call `HeadBlockBuilder::noteNative('canonical')` (or `'hreflang (de)'`, `'title template'`, etc.) for each tag emitted through Joomla's native streams so the consolidated header comment can list it under `<!-- Also emitted via Joomla head: … -->`.

**Cooperative skips:** when `DocumentInspector::shouldSkip()` returns true, call `HeadBlockBuilder::noteSkip($section, 'reason')` so the user sees a `<!-- Skipped: OpenGraph & Twitter — already emitted by 4SEO -->` line inside the block instead of silent absence.

**Audit checklist for any new head/body-emitting plugin or refactor:**
- [ ] No `addCustomTag()` call for `<head>` content — only `HeadBlockBuilder::pushSection()`
- [ ] No direct `preg_replace` against `<body>` / `</body>` — only `BodyBlockBuilder::pushBody()` / `pushFooter()` (called from `onBeforeCompileHead`)
- [ ] Plugin's `onAfterRender()` calls BOTH `HeadBlockBuilder::finalize($app, Version::VERSION)` AND `BodyBlockBuilder::finalize($app)` (idempotent — safe to add to every plugin)
- [ ] `setHideComments($hide)` called on BOTH builders FIRST in `onBeforeCompileHead`, before any early-return path
- [ ] Cooperative-mode skip path calls `HeadBlockBuilder::noteSkip()`, never stays silent
- [ ] Any `addHeadLink()` / `setMetaData()` call is paired with `HeadBlockBuilder::noteNative('name')`
- [ ] In default mode, `curl -s {site}/` shows exactly ONE bare `<!-- AI Boost for Joomla - Start -->` in `<head>`, ONE after `<body>` (only if body content exists), and ONE before `</body>` (only if footer content exists). The outer pair must NEVER include version or URL — those go to `<meta name="generator">` only.
- [ ] In `hide_comments=1` mode, every wrapper still has the same bare outer pair but with zero inner labels (no sub-section labels, no Also-emitted, no Skipped)
- [ ] No fresh references to the removed `ConflictMarkerWrapper` class, `setDebug()` / `isDebug()` methods, or `debug_wrap_markers` setting in Vue, PHP, controllers, or docs

---

## Mandatory Step for Every Plugin/Component Task

At the end of every task that modifies plugin or component PHP code, add a final step:

> **Update Joomla skill — BOTH copies.** If any new lessons were learned (new gotcha, new pattern,
> new script), add them to the **canonical** copy
> `aiboost-joomla/.agents/skills/joomla-development/SKILL.md` under "Lessons Learned / Gotchas" with a
> task reference, **then sync the installed copy** `.claude/skills/joomla-development/SKILL.md` so the
> two stay **byte-identical**. Skipping the sync is exactly what let the two drift (order 0088 found
> the installed copy missing L024–L026). Simplest reliable sync — overwrite installed from canonical:
> ```bash
> cp aiboost-joomla/.agents/skills/joomla-development/SKILL.md .claude/skills/joomla-development/SKILL.md
> ```
> (run from the wrapper root) then confirm `diff` is empty.

See also: `OPERATING.md` (global plan: codegen recipe, Pro-gating rule, Health rule, Definition of Done).

**L022 — Plugin rename requires pkg_script `postflight` cleanup (Task #438)** — When you change a Joomla plugin's slug (e.g. `aiboost_perf` → `aiboost_core`), Joomla's package installer does NOT automatically uninstall the old plugin. It happily ships both. You must add a `postflight()` step that: (1) `SELECT extension_id FROM #__extensions WHERE element='<old_slug>' AND type='plugin' AND folder='system'`; (2) read its `enabled` column and transfer it to the new plugin row; (3) call `(new \Joomla\CMS\Installer\Installer())->uninstall('plugin', $oldId)`. Wrap in try/catch and enqueueMessage on failure so users can clean up manually. Idempotent — no-op if the old row is absent. Settings stored in `#__aiboost_settings` (not plugin params) are unaffected by the slug change and need no migration.

**L023 — Styling a checkbox as an ON/OFF switch (Task #559)** — To turn a boolean `<input type="checkbox">` into a sliding green-ON / red-OFF switch purely in CSS, set `appearance:none` on the input and draw the knob with `::before` and the "ON"/"OFF" text with `::after`; `:checked` flips colour (`--ab-success` / `--ab-danger`) and slides the knob via `left:calc(100% - knob - gap)`. Scope the rule to `[type="checkbox"]` only — `CodeTab.vue` reuses the same `.ab-toggle__input` class on radios that MUST keep their native look. Pseudo-elements DO render on `appearance:none` checkboxes in all modern browsers, but only when the input is NOT also hidden by a sibling `:has()` rule — the existing `.ab-toggle__track` hide rule targets a different markup shape, so verify your switch input is followed by a `<label>`, not a `.ab-toggle__track`. Pure-CSS approach means manifest-generated Vue partials (`tabs/generated/*.vue`) and hand-written tabs are covered without touching markup, except Bootstrap `form-check-input` toggles which must be reclassed to `ab-toggle__input`.

**L024 — Some `vue-admin/src/tabs/*.vue` are ORPHANED dead code — confirm a file is bundled before editing it (order 0043)** — Not every `.vue` under `vue-admin/src/` is wired into the SPA. `HealthTab.vue` (a client-side page-scanner with its own `runScan()` + `expected:{type:'header',regex}` checks) is imported NOWHERE: the routed `/health` is `HealthApp.vue` (backend-driven checks via `HealthCheckService`), so Vite tree-shakes `HealthTab.vue` out — editing it changes the source but NOT the shipped `media/js/admin-vue.js`, so the "fix" is inert. Before editing any tab/component and claiming a live effect, verify it's actually reachable: (1) `grep -rn "<BaseName>" vue-admin/src` — must be imported by `router.js`, `main.js`, or a parent SFC, not only self-referential; (2) after `pnpm build`, confirm a string unique to that file appears in `component/com_aiboost/media/js/admin-vue.js` (or that `git status` shows the bundle actually changed — an unchanged bundle after your edit = the file is tree-shaken/dead). Report dead-code fixes as such; don't claim a Health/UI behaviour change from a file that isn't in the bundle.

**L025 — THE canonical on/off row is `ToggleRow.vue`; never hand-write toggle markup again (order 0063)** — `vue-admin/src/components/ToggleRow.vue` (globally registered in `main.js`) is the ONE standalone on/off setting row: `<ToggleRow v-model="s.key" field="key" label="…"/>` (rich label → default slot, rich help → `#help` slot). It wraps the input in a single `<label class="ab-toggle-row">`, so the WHOLE ROW is clickable and the switch is bound to its own label; it emits `'1'`/`'0'` strings (override via `true-value`/`false-value` props). Do NOT re-inline the old `<label class="ab-toggle-row"><div>…</div><span class="ab-toggle">…<input class="ab-toggle__input"><span class="ab-toggle__track"></span></span></label>` blob. GOTCHA that broke the Crawlers switches in 0058: `.ab-toggle__input` is now `position:absolute;opacity:0;pointer-events:none` (invisible), so a toggle renders NOTHING unless it ALSO has a sibling `.ab-toggle__track` — the old `.ab-check .ab-toggle__input + .ab-check__label` pattern (still in `IntegrationOptionField.vue`, `ScopeSelector.vue`) shows label text with no visible switch. Migrate those to `ToggleRow`. Keep the compact `.ab-toggle-pair`/`.ab-toggle-cluster` grouped variant for side-by-side mini-toggles.

**L026 — Atum appends an external-link glyph via `::after` to EVERY `<a target="_blank">` that isn't already suppressed (order 0063)** — Joomla's Atum admin template globally adds a little "opens in new tab" icon through `a[target="_blank"]::after`. `admin.css` only suppressed it on `.btn` links inside the legacy `#ab-vue-*` mounts, so any OTHER external link (e.g. the ProGate `.ab-pg-field` "Translate … Pro" chip) shows a stray grey icon next to its own icon — the "2 icons" symptom. Fix: `body[class*="com_aiboost"] .<class>::after { content:none !important; display:none !important; }` (the `!important` is mandatory — it overrides Atum's own `!important`; this is the documented third-party-override exception to the no-`!important` rule). Separately, `.ab-field` is `display:grid`, so an inline-flex child (a chip/link) STRETCHES to full column width unless you add `justify-self:start; align-self:start` (same fix `.ab-btn` uses).

**L027 — Make a WHOLE feature Pro-only by extracting its logic into a FREE_EXCLUDE'd Service, and verify it on the PRO-EDITION build (order 0099)** — To convert an entire free plugin's feature into Pro-only + physically stripped from Free (e.g. Custom Code in `aiboost_code`), do NOT wrap method bodies in `// @pro:start/@pro:end` (the strip is line-based and can leave invalid PHP). Instead: (1) move ALL the feature's executable logic into a Service class in the FREE plugin dir (`aiboost_code/src/Service/CustomCodeInjector.php`) and add that path to `FREE_EXCLUDE` in `build-package-zip.py` — the whole file is omitted from the Free ZIP; (2) keep the plugin Extension in BOTH editions but gate the call as `if ($this->injectorReady() && PluginRegistry::isProActive($settings))` where `injectorReady()` is a try/catch-wrapped `class_exists(Injector::class)` (JDEBUG's loader throws on the missing file, so the guard MUST catch); (3) wrap the manifest entries in `Manifest/<tab>.php` with the Pro-strip markers so the Free lib manifest returns `[]` — but KEEP the feature's active keys in `SettingsSaveDefinition::COMPATIBILITY_KEYS` (legacyKeys) so save still accepts them in the Pro build after the component-lib always-strips the manifest. `verify-no-pro-leakage.py`'s FREE_EXCLUDE detector then guarantees the Service is present in source and absent from every Free sub-ZIP. **Verification gotcha:** `install-to-staging.py` defaults to the Free base ZIP (`pkg_aiboost-*.zip`), which has the Service FREE_EXCLUDE-stripped — installing that on the Pro staging site would make the Pro feature look broken. Install the **Pro edition** (`pkg_aiboost_pro-*.zip`) on Pro staging via `install-matrix.py --sites staging,free` (it maps `staging`→pro edition, `free`→free base). Prove both ends at runtime with a reversible `qa.settings_mutation` round-trip: set `enable_custom_code=1` + a sentinel in `custom_code_head`, fetch the homepage — the sentinel MUST appear on Pro and MUST be ABSENT on Free (that is the exact leak scenario, closed), then it auto-restores. If you also delete dead sub-options (the `custom_code_*_scope`/`*_menu_ids` keys), update ALL of: the manifest, `SettingsSaveDefinition::COMPATIBILITY_KEYS`, `ProFeatureRegistry::codeSectionFields()` (else `ManifestProRegistryParityTest` fails — every `sectionFields()` key must be a known manifest/save key), `codegen COMPLEX_COVERAGE_ALLOWLIST`, the stale `tabs/generated/<tab>/*.vue` partials, and the `SettingsSaveDefinitionTest` assertions.

**L028 — The Pro-locked TEASER: `<ProGate mode="card">` renders NO controls on Free; drive it from the registry (order 0100)** — `ProGate.vue` card mode is a registry-driven teaser: on a Pro build (`isProInstalled()`) it renders its slot (the real controls); on Free it renders ONLY a locked teaser (padlock + name + Pro badge + one "Unlock Pro" → `aiboostnow.com/pricing`), and **does NOT render the slot** — so there is no toggle and no inputs to grey out. To Pro-lock a whole section: (1) wrap it `<ProGate mode="card" reg-key="section:{tab}.{id}">` — NEVER `gate-key="…"` (the `ProFeatureRegistryParityTest` fails the build on any `gate-key`, and forbids per-field feature locks); `reg-key` is a safe new attribute it does not scan. (2) Add BOTH a `['key'=>'section:{tab}.{id}', … 'scope'=>'section', 'teaser'=>'…']` entry to `ProFeatureRegistry::all()` AND a matching row in the right `*SectionFields()` helper — the parity test enforces all()↔sectionFields() in BOTH directions, and every sectionFields key must be a known manifest or `SettingsSaveDefinition` save key. The teaser label + copy come from the registry entry (`label`/`teaser`), injected to the SPA as `window.aiBoostBootstrap.proFeatures` and read via `composables/proRegistry.js` — never hand-type an ad-hoc `label` prop. The gate is presentation only: genuine Pro-ness still needs the runtime (a `*_pro` decorator or a `PluginRegistry::isProActive($settings)` guard in the Free plugin) — a UI-only lock is forbidden. Two field-gating gotchas from 0100: (a) making a Free field Pro (e.g. `sitemap_limit`, `exclude_*` → `tier=>'pro'` in `core.php`) also needs the Free runtime to already ignore it (AiBoostSitemap already gates those on `isProActive`) AND its `SettingsSaveDefinitionTest` "free active keys" expectation moved to a pro-tier assertion; (b) `gsc_verification_code`/`gsc_codes`/`meta_pixel_*` are `SettingsSaveDefinition::saveOnlyKeys()` and MUST stay compatibility-only (a test guards it) — do NOT add them to a `Manifest/*.php`. Integration cards: paid add-ons (falang/yootheme, any `IntegrationRegistry` bridge) lock to a `addon_locked` teaser on Free via `IntegrationDetectorService::isProInstall()` — `masterToggleKeys()` returns `[]` on Free so the master switch disappears; do not reintroduce an unconditional `['falang'=>true,'yootheme'=>true]` toggle set.

**L029 — Building a hash-route deep-link by string concatenation: the FIRST appended param needs `?`, not `&` (order 0101)** — `data.urls.<page>` (from PHP bootstraps) is a bare SPA hash link, e.g. `'#/redirects'` or `appBase + '#/redirects'`. Appending a query with `+ '&tab=X'` produces `'#/redirects&tab=X'` — vue-router's hash history treats everything after `#` as the path, so `/redirects&tab=X` (no `?`) does NOT match the registered `/redirects` route and falls through to the catch-all `{ path: '/:pathMatch(.*)*', redirect: '/dashboard' }` — the button silently "does nothing" (actually navigates then immediately redirects back). Always build the FIRST appended param with `?` (`+ '?tab=log404'`), `&` only for subsequent ones on the SAME href. This exact bug hit two Dashboard buttons ("View all & manage redirects", the per-row "+ Redirect" quick-add) simultaneously — grep for `data\.urls\.\w+ \+ '&` across Vue files when auditing dashboard/quick-action links. Symmetric gotcha on the RECEIVING end: a component read via a hash route must parse its deep-link query from `window.location.hash`'s substring after `?` (or `route.query` if mounted under the router), NOT `window.location.search` — `window.location.search` is only correct when the SAME component is ALSO mounted standalone (legacy `view=X`, no router, a real navigation with a real query string). `RedirectsPage.vue`'s `onMounted` read `window.location.search` unconditionally, which is right for the standalone mount but always empty when the same component runs inside the SPA at `#/redirects?from_url=…` — check the hash first, fall back to `window.location.search`.

**L030 — Removing a dead option: delete the whole three-way-plus surface, and if it was a FREE_EXCLUDE'd Pro class ALSO drop it from `FREE_EXCLUDE` (order 0102)** — Safely retiring a settings key ripples through more places than the three-way alignment: (1) its `Manifest/*.php` entry → then re-run `codegen-from-manifest.py` (codegen NEVER deletes orphans, so ALSO hand-delete the now-stale `tabs/generated/{tab}/{key}.vue`, its idempotent `Manifest/Health/{Class}.php` stub, and any generated `.ini` keys — grep them); (2) `SettingsSaveDefinition::COMPATIBILITY_KEYS`; (3) `ProFeatureRegistry::all()` field entry AND its `*SectionFields()` row (the `ManifestProRegistryParityTest` fails if a `sectionFields` key is no longer a known manifest/save key); (4) `App.vue` `DEFAULTS` + `FIELD_TAB_ALIASES`; (5) hand-written tab markup + the hidden `StyleguidePage.vue` demo if it name-drops the feature; (6) the consuming Service (and stale doc comments); (7) `SettingsSaveDefinitionTest` expectations. If you DELETE a Pro `Service`/`Feature` file that was listed in `build-package-zip.py`'s `FREE_EXCLUDE`, you MUST remove its path from that dict too — the STRICT `verify-no-pro-leakage.py` (run inside the build and by `VerifyNoProLeakageScriptTest`) treats a `FREE_EXCLUDE` path that is missing from source as **rename/move drift** and FAILS the build ("FREE_EXCLUDE path(s) MISSING from source"). Finally: the **ImportController** did NOT filter uploaded keys through `SettingsSaveDefinition::acceptedKeys()` — it merged everything not in the denylist — so a removed key from an OLD export got persisted as inert cruft that then re-propagated through every future export. 0102 added an `acceptedKeys()` filter (mirroring `SettingsController::save`) so stale exports degrade gracefully ("Ignored N option(s)"); prove it live by importing an old-export fragment and reading the import response message (not by grepping the blob, which may already hold cruft), and re-run `verify-import-export.py` on BOTH staging+free to confirm the filter drops no real key.

**L031 — A FREE per-article field needs its OWN catalog created UNCONDITIONALLY in pkg_script (the OG fields are Pro-only) + `verify-clean-uninstall.py` leaves a Pro site on the FREE base (order 0104)** — Two gotchas from adding a Free per-article SEO-title field. (1) The 6 per-article OG custom fields are **Pro-only**: `pkg_script.php postflight` calls `ensureOgCustomFields()` only inside `if ($this->isProInstall())` and `removeOgCustomFieldsForFree()` on the else branch. So a FREE per-article field (e.g. `aiboost_seo_title`) must NOT ride that path — add a SEPARATE catalog (`SeoCustomFieldCatalog`, its own group "AI Boost — SEO") + an `ensureSeoCustomFields()` called UNCONDITIONALLY (outside the isProInstall branch), reusing the existing `upsertFieldGroup()`/`upsertField()` stock-model helpers (generalise `upsertFieldGroup` to take a description arg so the SEO group isn't labelled "OpenGraph"). Read it at runtime with a small FREE DB reader in the Free plugin (NOT the FREE_EXCLUDE'd Pro `CustomFieldReader`), and drive article detection through `AdapterRegistry::pageResolver()->resolve()->isArticle()`/`->entityId` — an inline `$view==='article'` gate would trip `test-resolver-gate-lockin.php`. (2) **`verify-clean-uninstall.py` installs the FREE base `pkg_aiboost-*.zip`** (Pass 1 install + Pass 2's "install new on top"). Run it against `--target pro` (offroadserbia) and it leaves the site on the **Free edition** — you MUST `install-matrix.py --sites staging` afterwards to restore the Pro edition. Its Pass-1 "Install failed" on a Pro site + its "translations stay empty on Free" assertion are pre-existing tooling/site-state noise (the Free base ZIP installs fine on the actual Free site; offroadbalkans carries stale Pro-era translations) — the meaningful signal is **Pass 2 "settings/translations survived the upgrade"**, which is what an additive pkg_script change (new field-create call) must keep green. Bonus: on a **multilingual** staging site the AI Boost sitemap emits the default-language loc **without** the `/sr/` prefix while the page RENDERS at `/sr/…` and canonicalises there — so a per-page noindex/canonical proof must target BOTH the loc path (→ sitemap drop) and the rendered/canonical path (→ robots-meta / URL-map), discovered from the page's own `<link rel=canonical>`.

**L032 — Any NEW file that writes the `#__aiboost_settings` blob must be registered in `SettingsWriterRmwContractTest`, and a new admin AJAX tool is auto-discovered (no registration) but must go through read-modify-write (order 0105)** — Two things bite when you add a new admin AJAX endpoint that persists a setting. (1) `component/tests/Lib/SettingsWriterRmwContractTest.php` scans ALL of `component/` for the literal pattern `quoteName('settings_json') . '` and FAILS ("A settings-blob writer was added or removed") until every such file is classified in its `WRITERS` map with a shape: `'rmw'` (loads settings_json THEN writes it in the SAME method — the test structurally enforces load-before-write), `'helper'` (a pure writer that receives the whole blob; the CALLER loads it), `'snapshot'`, `'install_rmw'`, `'import'`, or `'dead'`. The single-JSON-row model means a subset-replace silently WIPES every key you left out, so ALWAYS load the whole blob, change only your key(s), write it back — model the write on `AnalyzerController::applyFix` (rmw, self-contained) or, if your write lives in a private helper while the load lives in the calling method, classify it `'helper'` like `ConflictsController::writeSettings` (0105's `IndexingController::confirm` loads via `readSettings()` then `writeSettings()` writes it whole → registered as `'helper'`). (2) A new controller is **auto-discovered** by Joomla's `MVCFactory` from the `...\Administrator\Controller\XxxController` namespace (task `xxx.method` → `XxxController::method`) — NO provider/DI registration needed; just add the file. A NEW **SPA-only** Vue page needs wiring in EXACTLY TWO files — `vue-admin/src/router.js` (import + a `{ path, name, component, meta:{ legacyUrl:'' } }` route) and `vue-admin/src/navigation.js` (a sidebar `items[]` entry with an icon from `icons.js`) — and NOT `main.js` (that legacy-mount list is only for pages that ALSO have a `view=X` PHP shell; model an SPA-only page on `LicensesPage`/`ConflictManagerPage`). Because the route references the component, Vite bundles it (no L024 tree-shake risk); still confirm the built `admin-vue.js` inside the installed `com_aiboost-*.zip` contains a string unique to the page. Reuse existing `--ab-*` classes (`ab-section`, `ab-table`, `ab-badge--warning/--success`, `ab-btn--primary`, `ab-alert--info`) and pick an `AbIcon` name that EXISTS in `icons.js` (grep it: `check search shield robot tag map lock …`) — an unknown name renders an empty SVG.

**L033 — A Pro OUTPUT-LEVEL gate for a feature written by the shared component/lib must call a FREE_EXCLUDE'd PLUGIN class via `class_exists()`, NOT wrap the lib code in `@pro` — because `component/lib/` (and `admin/`) is `@pro`-stripped in BOTH editions (order 0106)** — `build_component_zip()` in `build-package-zip.py` runs `strip_pro_blocks()` on every admin/ and lib/ PHP file **unconditionally** (no `strip_pro` flag), and the Pro edition (`--target pro`) reuses that SAME component ZIP + adds the `*_pro` plugins (only the plugins are built FULL, `strip_pro=not pro_edition`). So a `// @pro:start/@pro:end` block inside a lib class (e.g. `RobotsTxtBuilder`) is stripped from the Pro edition too → the feature would emit NOWHERE. The physical robots.txt is written by the always-stripped lib (`SettingsController::regenerateRobotsTxt` + `pkg_script writeRobotsTxt` → `RobotsTxtBuilder`), yet a Pro feature must be present in Pro and physically absent in Free "even with a stale `pro_activated`". Solution used for Content Signals/AIPREF: put the actual output renderer in a **plugin** Service (`aiboost_aeo/src/Service/ContentSignalsRenderer.php`) listed in `FREE_EXCLUDE['aiboost_aeo']` (present only in the Pro plugin build), and have the lib writer gate on `PluginRegistry::isProActive($settings) && class_exists('AiBoost\\Plugin\\System\\AiBoostAeo\\Service\\ContentSignalsRenderer')` inside a `try/catch` (JDEBUG's loader throws on the missing class). Joomla's global namespace map registers every extension's PSR-4 prefix, so the component/lib CAN `class_exists()` a plugin class at runtime (admin save AND install postflight both resolved it live). The manifest fields stay `@pro`-wrapped in `Manifest/aeo.php` (belt+braces, stripped from the Free lib manifest) with their keys in `SettingsSaveDefinition::COMPATIBILITY_KEYS`; the Pro→Free transition self-cleans because `pkg_script` regenerates robots.txt on every install and the Free build simply has no renderer class (`class_exists`→false → clean file). **Runtime default gotcha:** a `default=1` manifest/UI toggle still reads as OFF at runtime when the key is ABSENT from the stored blob (`?? '0'`), so a brand-new Pro site wouldn't emit until first save — default the RENDERER's enable to `?? '1'` to match the manifest/#14 convention. **Verifier trap (bit me):** `verify-no-pro-leakage.py`'s token scan matches the regex `@pro\b`, so the literal string `@pro` in ANY surviving prose comment (e.g. "these entries are @pro-stripped") FAILS the STRICT Free build — write "opt-in Pro-strip markers", never the literal `@pro`, outside the actual `// @pro:start/@pro:end` fence.

**L034 — Give the CMS-neutral generators a `route()` on `AppContextInterface` for SEF URLs; adding an interface method means updating EVERY implementor incl. standalone-script test doubles (order 0106)** — The llms.txt/sitemap generators are deliberately Joomla-free (they take `AppContextInterface`), so a raw `baseUrl . '/index.php?option=com_content&view=article&id=' . $id` link is non-SEF and does not honour SEF/rewrite, the language prefix, or a subdirectory base. Fix = add `route(string $internalUrl): string` to `AppContextInterface`, implement it in `JoomlaAppContext` via `\Joomla\CMS\Router\Route::link('site', $url, false, Route::TLS_IGNORE, true)` (absolute) with a `try/catch` raw-link fallback, and a pass-through stub in `WpStub\WpAppContext`. PHPUnit `createMock(AppContextInterface::class)` auto-stubs the new method (returns ''), but **hand-written test doubles that `implements AppContextInterface` will fatal** ("contains N abstract method") until updated — there is one in `scripts/test-og-pro-decorator.php` (`FakeAppContext`); `composer test` (standalone) is what catches it, not `phpunit`. Related order-0106 llms/markdown fixes worth copying: (a) close the restricted+scheduled LEAK by passing `window:'llms'` + `accessExpr` + `publicAccessOnly:true` to `IndexabilityPolicy::itemWhereClauses` in EVERY llms enumerator (the Pro recent list had `publishedExpr` only → leaked both), over-fetch `*3` then post-filter; (b) honour noindex by skipping rows whose Joomla `metadata` JSON has `robots=noindex` and whose routed path matches `NoindexPolicy::pathIsNoindexed()` (strip the `getBaseUrl()` path first for subdir installs); (c) virtual-file routing (`llms.txt`, `*.md`) must compare a path made RELATIVE to `Uri::root(true)` or it 404s in a subdirectory install; (d) content-negotiated Markdown responses need `Vary: Accept` (merge, don't duplicate the header) or a shared cache serves the wrong variant. A clean red-green for the leak: a fluent query double whose `where()` records fragments + a mock DB with `quoteName`→identity, `quote`→`'x'`; assert the access/`publish_down` clauses are present (revert the guard → red).

**L035 — A "preview, then apply" admin action stashes its parsed-but-unapplied payload in the Joomla SESSION (fixed key, TTL-checked), never a DB draft row/table (order 0145)** — To turn a one-click destructive-looking import into preview-report-then-confirm: (1) the preview endpoint parses + classifies the upload and calls `$this->app->getSession()->set('com_aiboost.import.pending', [...payload..., 'saved_at' => time()])` — ONE fixed session key (not a per-request random token) is enough because a single admin only previews one file at a time; a fresh preview() overwrites the old one. (2) the apply endpoint reads it back via `getSession()->get()`, checks `time() - saved_at` against a TTL (900s here) so a forgotten browser tab can never silently apply a stale file, and clears the key after applying (success or failure). (3) Keep the classification logic in a `public static` PURE function (no DB/Joomla runtime) so it is unit-testable exactly like `SettingsController::buildExportPayload()` — the controller's instance methods only do I/O (read file, load DB, call the pure classifier, write DB), mirroring the project's existing static-payload-builder pattern. **Distinguishing "obsolete key" from "key this site can't use YET":** don't lump every unrecognised settings key into one "drop it" bucket — a key matching a KNOWN integration bridge's prefix (e.g. `falang_`/`yootheme_`, listed in `SettingsSaveDefinition::KNOWN_INTEGRATION_KEY_PREFIXES`) but absent from `acceptedKeys()` means "that bridge plugin isn't installed on THIS site", not "this build no longer supports it" — report it as its own category and let the admin choose to keep it dormant (stored, inert, ready for when the bridge is installed) vs discard it, matching how a genuinely-removed legacy key is still silently dropped. A live round-trip test proving this (upload → preview classifies → apply persists → re-export shows it survived) needs a key that matches the prefix but ISN'T one of the bridge's real registered fields, because installing the bridge ZIP (even Free-tier, even unlicensed) already registers its real field keys via `onAiBoostRegisterFields()` regardless of Pro activation — the QA test sites in this repo have both `aiboost_int_falang`/`aiboost_int_yootheme` installed, so real `falang_hreflang_head` etc. keys are already "known" there.

---

**L036 — `phpcbf` reformats the WHOLE file's pre-existing style debt, not just your diff — never run it on an existing file after a small targeted edit without checking `git diff --stat` first (order 0142)** — Running `vendor/bin/phpcbf --standard=phpcs.xml` on an existing source file (e.g. after a one-line semantic fix) auto-fixes EVERY PSR2 violation in the ENTIRE file, including all the pre-existing style debt nobody had touched — a 1-line intended change silently became a ~260-line diff (blank-line spacing, multi-line function-call argument wrapping, etc.) across the whole file. This buries the real change in noise and risks the reviewer missing it, or a merge conflict with concurrent work. Rule: after any `phpcbf` run on a file you did NOT create from scratch, immediately `git diff --stat` that file — if the change count is wildly larger than your intended edit, `git checkout -- <file>` and reapply ONLY your semantic fix by hand (Edit tool), leaving the file's pre-existing style debt alone (CI only cares about NEW errors in touched lines — confirm with `phpcbf`'s dry-run sibling `phpcs` scoped to the file and check the flagged line numbers fall outside your diff). `phpcbf` is safe to run un-audited only on a file you just created wholesale (nothing pre-existing to bury).

**L037 — Unit-testing a class that calls a real Joomla class not in this repo's dependency stubs: add a matching stub under `component/tests/stubs/`, don't reach for a live install (order 0142)** — Several lib/admin classes call real Joomla runtime classes directly (`Joomla\CMS\Uri\Uri::root()` in `UrlCheckerService`/`UrlcheckerController`'s SSRF guard; `Joomla\Http\Http` as a constructor type-hint in `SeoAnalyzerService`/`AiVisibilityAnalyzerService`) instead of going through the `Cms\AdapterRegistry` port (those two predate/bypass T1's adapter boundary). Since this repo has NO `joomla/*` Composer packages at all (only the project's own minimal stubs in `component/tests/stubs/`, loaded selectively — `bootstrap.php` only auto-loads Database/Registry/Factory/Plugin/Log), a test that exercises such a method needs its own tiny stub class in that same namespace (`Joomla\CMS\Uri\Uri`, `Joomla\Http\Http`) with just the 1-2 methods actually called, `require_once`'d by the test file itself (NOT added to `bootstrap.php` unless every suite needs it — follow the existing `stubs/JoomlaMvcController.php` convention: a doc-comment stating "Not loaded by bootstrap.php; tests that need it require_once it first"). A configurable canned-response stub (keyed by URL, or a settable static test value) is reusable across every test file that needs the same Joomla class — do not duplicate one per test file. `DatabaseInterface`'s stub interface (`stubs/JoomlaDatabase.php`) only declares 10 methods; a class that calls an out-of-stub method like `loadObject()` still works fine from a per-test-file Fake class (PHP has no sealed interfaces — implement the interface AND add the extra method the class under test actually calls; `createMock(DatabaseInterface::class)->method('loadObject())` would fail since PHPUnit only doubles declared interface methods).

**L038 — `phpunit.xml`'s `failOnWarning="true"` turns an E_WARNING into a hard test failure — audit every fake/stub for null-array-offset access before trusting a "logically correct" test (order 0142)** — This repo's `phpunit.xml` sets `failOnWarning="true"`, so any PHP runtime E_WARNING raised DURING a test (not just uncaught exceptions) fails it, even if every assertion would otherwise pass. The classic trap: a fake `DatabaseInterface::loadResult()` returning `''` (empty string, meant to simulate "no row") then the caller does `json_decode('', true)` → `null`, and `$decoded['some_key'] ?? 'x'` on a NULL (not merely undefined-index) triggers "Trying to access array offset on value of type null" — silently converted to a red test with a confusing failure. Fix: fakes standing in for a JSON-blob DB column must return a **valid empty-object JSON string** (`'{}'` or `json_encode([...])` with explicit keys), never `''`/`null`, so `json_decode()` always yields an array and `??` accesses stay warning-free. `@`-suppressed calls (`@gethostbynamel(...)`) are NOT affected — PHPUnit's error handler respects `error_reporting()===0` during suppression — but that only helps code you don't control; your OWN test fixtures must not manufacture the null in the first place.

---

**L039 — Changing Joomla Global Configuration over HTTP: OMIT the DB-connection fields or the save is silently rejected; the admin-toolbar site name lives HERE, not in AI Boost (order 0139)** — Two lessons from swapping the staging site name for marketing screenshots. (1) The Joomla admin top toolbar shows the Global Configuration `sitename` (configuration.php), NOT any AI Boost setting — so neutral-demo screenshots need it temporarily changed (and restored) via com_config. (2) Replaying the com_config application form over HTTP (parse all `jform[*]` fields, POST with `task=application.apply` + CSRF) FAILS with only a `<noscript>`-buried "Database connection test failed … (using password: NO)" message: the form renders `jform[password]` (the DB password) EMPTY, Joomla sees the DB settings as "changed", tests the connection with no password and rejects the WHOLE save. Fix: omit ALL DB-connection fields from the POST (`jform[dbtype]/host/user/password/db/dbprefix/dbencryption/dbssl*`) — absent keys keep their stored values server-side and the "changed?" test never fires ("Configuration saved."). This failure mode is safe in both directions (a wrong replay is rejected, never half-saved). Uploading a helper image for such shots: `POST index.php?option=com_media&task=api.files&format=json&path=local-images:/` with header `X-CSRF-Token: <token>` and JSON body `{"name":..., "content":<base64>}`; delete afterwards with the DELETE verb on `...&path=local-images:/<name>` (leave staging clean). Store `org_logo`-style media values as root-relative paths (`images/foo.png`) — `MediaPicker` normalises them for preview, and no domain text leaks into the shot.

## UI styling discipline (Vue admin)

A colour/spacing change should be ONE edit, not many. The shared system
(`ab-tokens.css` + `ab-components.css` + the 14 components in `vue-admin/src/components/`)
already carries most of this. Keep new work inside it; do not start new bespoke styling.

- **Colours through tokens.** Any status/theme/brand colour (success, danger, warning,
  accent, surface, text) must use `var(--ab-*)`. If the token does not exist, add it to
  `ab-tokens.css` and use that — do NOT hard-code a new hex for these.
  NOT in scope — leave as-is, do not churn: hex used as a `var(--x, #hex)` fallback, fills
  inside inline SVG icons, and `color:#fff` on a coloured button. These are fine; do not rip
  them out.
- **Reuse classes and components — don't hand-write new markup.** For a button/card/field use
  the existing `.ab-btn` / `.ab-card` / `.ab-field` classes and the `AbField` / `OnOffSwitch` /
  `PageHeader` components. Do not invent a new one-off button or card in a page's scoped `<style>`.
- **Spacing/size:** use existing tokens/classes for values that REPEAT. A genuinely one-off
  layout width is fine inline — do NOT manufacture a token for something used once.
- When adding a screen/tab, build from the shared parts first; add bespoke style only for what
  has no shared equivalent, and flag it so it can be folded in later.

## Cross-platform & integration boundary

The logic layer (Schema / sitemap / llms.txt / OG generators) is deliberately thin and portable;
the integration layer is a versioned SDK. Keep new work inside these boundaries so a WordPress
build and standalone+integrative plugins stay possible without rewriting the core. Full snapshot,
the gaps, and the WP/standalone plan: **`docs/ARCHITECTURE-BOUNDARIES.md`**.

- **"Which page am I on?" has ONE answer — the `PageResolver` (T1, complete).** Page-type, the primary
  entity, the single homepage truth, active + site-default content language, canonical URL and the one
  indexability verdict all come from `AdapterRegistry::pageResolver()->resolve()` → `PageContext`
  (`component/lib/src/Page/`). **Never re-derive page type inline** — no fresh
  `$option==='com_content' && $view==='article'` gate, no path/`featured` homepage guesswork, no ad-hoc
  `ComponentHelper::getParams('com_languages')->get('site')` / `getActiveLanguage()` read. A consumer reads
  `PageContext` and may keep a guarded null-fallback to its old inline logic ONLY for the absent-Page-classes
  case. The standalone/CI test `scripts/test-resolver-gate-lockin.php` enforces this: it scans `component/`
  (excluding `lib/src/Page/`) and FAILS if a NEW inline article/`featured` gate appears outside the explicit
  allowlist of known guarded fallbacks — so add new page logic to the resolver, not inline. (Design:
  `docs/analysis/T1-resolver-design.md`.)
- **New logic goes through the `Cms` adapters, not the CMS directly.** A generator takes its data
  injected (settings array, `DatabaseInterface`, `AppContextInterface`) and routes URL, filesystem,
  application, clock, http and events through `AiBoost\Lib\Cms\AdapterRegistry` (Joomla + Wp impls
  exist). Do NOT add a fresh direct `Route::_()`, `JPATH_…`, `Uri::`, `Factory::…` or `\JFactory`
  inside a generator — those are exactly what does not port to WordPress.
- **New integration code follows the SDK pattern.** A bridge is a SEPARATE plugin that extends
  `AbstractIntegrationPlugin`, returns an `IntegrationDescriptor` from `describe()`, and enriches
  output only via the SDK: the named `onAiBoostFilter*` events (`Sdk::EVENT_FILTER_*`) and/or
  `BridgeDetector::register*()`. Every cross-plugin touch is `class_exists()`-guarded so an absent
  host or absent core never fatals. The core stays generic — it fires filter events and reads back
  registered data; it never names a specific third-party extension.
- **A STANDALONE plugin does NOT extend `AbstractIntegrationPlugin`.** That base boots the shared lib
  from `com_aiboost`, so it hard-depends on AI Boost. A plugin that must run on its own carries its
  own core logic and treats AI Boost as an OPTIONAL layer — hooking the `onAiBoost*` events behind
  `class_exists()` only. (This standalone+integrative sub-pattern is a BACKLOG item, not yet built.)
- The SDK + `Cms` adapters are already WordPress-aware (`Sdk` / `BridgeDetector` guard on
  `defined('_JEXEC') or defined('ABSPATH')`; `Cms/Wp/*` adapters exist). The remaining WP work is the
  DATA layer (Joomla `#__` queries → WP equivalents) — see the boundaries doc.
