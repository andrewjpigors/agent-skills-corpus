---
name: ric-admin-console
description: "Use for Chinese enterprise admin panels, SaaS back offices, CRUD/RBAC consoles, data tables, branded login and workbench screens, public portals attached to management systems, multilingual or themeable admin UI, shadcn-first React admin builds, optional Ant Design or Vue UI stacks, ImageGen-backed brand assets, GSAP/3D-enhanced entry surfaces, browser screenshot validation, and cross-agent implementation environments."
---
# RIC Admin Console Skill

Use this skill for Chinese enterprise management systems: admin panels, back offices, operations consoles, CRUD systems, permission systems, workflow approval systems, internal tools, data-heavy dashboards, branded login pages, visual workbenches, and SaaS control panels.

Do not blindly apply marketing-page taste rules to every admin page. Admin consoles are product surfaces for repeated work, but selected first-screen surfaces still need strong brand expression, visual assets, layout rhythm, CTA quality, and anti-template design judgment. Use high visual impact on login pages, workbench first screens, welcome/onboarding pages, empty states, announcement banners, dashboard first screens, big-screen command centers, module homepages, and productized SaaS console homepages. Keep ordinary CRUD, permission config, audit logs, settings, and detail pages optimized for clarity, scan speed, predictable navigation, permission-aware actions, state coverage, and dense but orderly information.

## 1. Operating Protocol

1. Perform skill retrieval before work.
2. Inspect the existing project before choosing libraries: `package.json`, router, UI library, layout components, table/form stack, state management, auth/permission model, request client, mock/data layer, and styling system.
3. Before locking the implementation scope, run the planning check in section 2A. Ask only for decisions that cannot be inferred and materially affect implementation; otherwise record explicit defaults.
4. After detecting the UI framework, perform framework skill retrieval and read the relevant installed skill when available. For React admin systems without an established UI system, retrieve and use `shadcn` before component selection or code. For React + Ant Design/ProComponents/antd imports, retrieve and use `ant-design` and/or `antd`; follow their CLI/API lookup rules when writing antd component code.
5. Prefer the existing stack. Do not replace shadcn/ui, Ant Design, Element Plus, Naive UI, Arco, or another established UI system unless the user asks.
6. Prefer PowerShell commands on Windows. Use pnpm over npm for Node projects.
7. Do not change global Node/FNM configuration. Use temporary `fnm use` or `fnm exec` only when needed.
8. Treat permissions as a first-class design input. Buttons, menus, routes, API calls, and bulk actions must have a shared permission source.
9. Treat locale, theme, layout mode, product title, and brand assets as product architecture inputs, not final decoration.
10. Render the shell and skeleton-first placeholders before data arrives. Provide loading, empty, error, disabled, success, and unauthenticated states for every interactive area.
11. Use Codex-native tools when running in Codex, but keep the workflow portable to Claude Code, Cursor, Windsurf, Cline, Aider, Antigravity, and other agent environments through capability detection and explicit fallbacks.
12. When a task needs image generation, browser screenshots, framework docs, GSAP, Three.js/WebGL, shadcn, AntD, or i18n APIs, retrieve the matching local skill when present or consult the relevant official documentation before implementation.
13. Never create destructive database/cache/message/object-storage operations. Follow `ric-infra-safety` for infrastructure and namespace rules.
14. Finish with repository validation: lint/test/build when available, framework-specific checks when available, and browser or screenshot checks for layout work.

Read these references when the task needs detail:

- `references/layout-patterns.md` for shell layouts, menus, top bars, breadcrumbs, auth states.
- `references/page-patterns.md` for workbench, list, detail, profile, settings, permissions, approval, logs, messages, import/export, tasks.
- `references/component-contracts.md` for query cards, tables, pagination, modals, drawers, forms, actions, status UI.
- `references/china-enterprise-visual-style.md` for Chinese enterprise visual taste, density, Chinese typography, color, spacing, and anti-template rules.
- `references/admin-visual-impact.md` for admin-adapted brand expression, hero/first-screen composition, CTA quality, visual assets, layout rhythm, motion restraint, and anti-template rules.
- `references/framework-adapters.md` for shadcn-first React defaults, framework skill retrieval, and React/Vue/UI-library decision rules.
- `references/i18n-patterns.md` when multilingual UI, locale switching, translated menus/breadcrumbs/tables/forms, date/number/currency formatting, or framework-specific i18n choices are in scope.
- `references/acceptance-checklist.md` before declaring work complete.
- `references/validation-loop.md` for browser screenshot verification after runnable UI work.
- `../../references/ric-imagegen-fallback.md` when admin-specific bitmap assets are needed and agent-native/built-in/MCP/IDE image generation is unavailable.

## 2. Design Read

Before implementation, state one concise design read:

`Reading this as: <system type> for <user role>, with <layout mode>, <visual impact mode>, <data density>, <permission complexity>, <locale strategy>, <theme mode>, <brand asset direction>, <public portal scope>, and <framework/UI library>.`

Examples:

- `Reading this as: user/role management for operations staff, with sidebar-plus-topbar layout, utility visual mode, high table density, RBAC permissions, and React + shadcn/ui + TanStack Table.`
- `Reading this as: SaaS console login plus workbench for tenant admins, with sidebar-plus-topbar layout, product/immersive visual modes, medium-high density, tenant permissions, and React + shadcn/ui.`
- `Reading this as: approval workflow console for department managers, with topnav-only layout, product visual mode, medium density, route-level permissions, and Vue 3 + Element Plus.`
- `Reading this as: CMS admin plus public portal for editors and visitors, with sidebar-plus-topbar admin layout, immersive portal/login and utility content pages, zh-CN default with en-US ready, light/dark/system theme, generated RIC brand assets, public portal in scope, and Next.js + shadcn/ui.`

Ask clarification only when layout mode, auth model, locale/theme scope, framework choice, brand/title identity, portal scope, or capability scope cannot be inferred from the repo and materially changes implementation.

## 2A. Planning Questions

When the user asks to create or substantially change an admin system and the scope is not already explicit, ask or record decisions for these capabilities before implementation:

- Website/system title, product name, LOGO source, desired LOGO style, brand color, and whether ImageGen should create the brand asset pack.
- Layout mode: `sidebar-only`, `topnav-only`, or `sidebar-with-topbar`; record the default if the user does not choose.
- Theme mode: light only, dark only, or `light/dark/system` switching; record persistence strategy when switching is in scope.
- Multilingual/i18n scope: no full i18n, i18n-ready only, or implemented language switch; record default locale, target locales, URL/cookie/user-preference strategy, and translation file ownership.
- Public portal or user-facing frontend scope: website, landing page, help center, invite page, login/register, tenant welcome page, report cover, or user console.
- RBAC roles, role assignment, permission points, and route/button permissions.
- Menu management, dynamic menus, hidden/disabled/no-permission items, and menu permission binding.
- Department/organization structure, tenant isolation, and data permission scope.
- Third-party login, SSO, OAuth/OIDC, LDAP/AD, DingTalk, Feishu, WeCom, or SMS login.
- Audit logs, login records, approval/workflow, messages/notifications, import/export, and async task center.

Defaults when the user does not answer and implementation must proceed:

- Locale: Simplified Chinese (`zh-CN`) as default, i18n-ready structure only, no full translated copy unless requested.
- Theme: `light/dark/system` support when the stack makes it reasonable; otherwise light theme plus token-ready structure.
- Layout: `sidebar-with-topbar`.
- Title/brand: use the project name or user-provided name; if no usable LOGO exists, generate a RIC-style brand mark and app icon.
- Auth/capabilities: local account login, basic RBAC, static route-derived menus with permission metadata, no third-party login, no tenant isolation, and audit/message modules only when requested by the page scope.

State the assumptions in the design read or handoff.

## 3. Asset Plan And Brand Asset Pack

After the design read and before implementation, create a concise Asset Plan:

`Asset Plan: <needed assets or none>, <source: existing brand asset | agent-native ImageGen | MCP/IDE image tool | RIC CLI fallback | not needed>, <save path>, <where used>.`

Active ImageGen is required when a `product` or `immersive` surface needs visual differentiation and no suitable existing brand/design-system asset exists. This includes login visual panels, workbench/module backgrounds, onboarding/announcement banners, empty-state illustrations, report/export covers, and dashboard/command-center backgrounds.

For a new or visually refreshed admin system, also create a Brand Asset Pack plan:

`Brand Asset Pack: <logo/mark>, <app icon>, <module icon style>, <background textures>, <default avatar>, <empty-state art>, <light/dark variants>, <save paths>, <consuming components>.`

Generate or reuse a consistent set of admin brand assets: logo/mark, app icon, sidebar/topbar brand mark, module or navigation icon style, login/workbench/module backgrounds, default avatar, empty-state art, and report/announcement visuals when relevant.

Rules:

- Do not skip needed visual assets after the requirement is clear.
- Do not substitute pure CSS gradients, blank placeholders, hand-rolled decorative SVG, or fake screenshot divs when a bitmap asset is needed.
- If agent-native image generation, built-in image generation, MCP image tooling, or IDE image tooling is available, use it first for project-bound bitmap assets.
- If image generation is needed but no agent-native/built-in/MCP/IDE image tool is available, read `../../references/ric-imagegen-fallback.md` and use the bundled CLI fallback directly.
- The CLI fallback requires `OPENAI_API_KEY`; if it is missing, stop and ask for that environment variable.
- `utility` pages do not need decorative generation unless they contain important empty, error, import/export, report, or onboarding states.
- Use one visual language for logo, generated assets, avatar placeholders, and project-specific bitmap icons. Functional operation icons may use the existing UI icon library by default, but they must match the generated brand system in weight, size, and tone. If the user asks for all small icons to be generated, create a full project icon pack with ImageGen or CLI fallback and wire it through a shared icon component.
- At final handoff, report generated asset paths or state that no image asset was needed for this page type.

## 3A. Locale And Theme Plan

When multilingual UI or theme switching is requested, or when a new admin system should be future-ready, create a short plan before implementation:

`Locale Plan: <mode: zh-CN only | i18n-ready | implemented>, <default locale>, <target locales>, <routing/persistence>, <library>, <translation coverage>.`

`Theme Plan: <mode: light | dark | light/dark/system>, <token source>, <persistence>, <asset variants>, <verification states>.`

Rules:

- Read `references/i18n-patterns.md` before implementing multilingual UI.
- Translate visible product strings through structured keys when i18n is implemented: menus, breadcrumbs, route/page titles, table columns, buttons, status labels, validation errors, empty/error/loading messages, notifications, auth errors, and profile/settings text.
- Keep dates, numbers, percentages, and currency locale-aware instead of string-concatenated.
- Theme switching must be token-driven. Do not hand-invert random colors page by page.
- LOGO, avatar, generated backgrounds, chart colors, semantic statuses, table selected/hover state, modal masks, and scrollbars must work in both light and dark themes.

## 4. Stack Selection

Use multi-stack decision-making:

1. Existing React + shadcn/ui: use shadcn source components, Tailwind semantic tokens, Radix/base primitives, local aliases, and TanStack Table when table state needs explicit control.
2. Existing Vue + Element Plus: use Element Plus layout, menu, table, form, dialog/drawer, pagination, popconfirm patterns.
3. Existing Naive UI or Arco: stay within that library and mirror its density/token system.
4. Existing custom design system: use the local primitives and only add external packages when missing capabilities are real.
5. Existing React + Ant Design: keep Ant Design, ProComponents, ProLayout, ProTable, Modal/Drawer/Form patterns already present unless the user explicitly chooses a migration.
6. New React project or React project without an established UI system: recommend React + Vite or Next + shadcn/ui + Tailwind + Radix primitives + TanStack Table.
7. New Vue project without user preference: recommend Vue 3 + Vite + Element Plus.

React default: shadcn-first. Ant Design/ProComponents is the secondary React option and should be used only when the user chooses it, the project is already deeply AntD-based, or the team/business requirement explicitly needs Ant Design Pro patterns. If a React project already uses AntD and the task suggests shadcn, ask the user to choose between the recommended shadcn direction and preserving AntD before mixing or migrating.

One UI system per app. Do not mix Ant Design and Element Plus, Ant Design and Material, or shadcn and ProComponents unless the repo already does so and migration is explicitly in scope.

Before writing framework-specific component code, read `references/framework-adapters.md` and apply its skill retrieval protocol. If a matching skill is unavailable, use the existing project version and official API documentation rather than inventing props, events, tokens, or component names.

## 5. Visual Direction

Default to enterprise-refined Chinese admin taste:

- Clear, trustworthy, compact, and stable.
- Medium-high information density.
- Productized brand expression on selected first-screen surfaces.
- Blue/neutral base with controlled semantic colors, or the product's existing brand color.
- Strong table readability, predictable action placement, consistent icons, polished empty states, and clear status tags.
- Chinese text rhythm: short labels, direct button copy, no oversized English marketing slogans.

Apply visual impact by surface:

- `utility`: tables, forms, permissions, logs, settings, and dense detail pages. Low visual drama, high efficiency.
- `product`: workbench, module homepages, SaaS console homepages, dashboard summaries, announcement centers. Stronger brand tone, richer layout rhythm, clear CTA hierarchy.
- `immersive`: login pages, welcome/onboarding pages, big-screen command centers, report covers, and hero-like console entry pages. Visual assets and first impression matter, but actions and state clarity still win.

Inherit the useful parts of `ric-design-taste-frontend`: brand read, visual asset priority, anti-default discipline, CTA contrast/wrap checks, copy self-audit, layout diversity, and restrained motion. Adapt them for admin workflows instead of copying landing-page structure.

Avoid globally:

- Marketing hero sections on ordinary CRUD pages, giant slogans in operational screens, decorative illustrations that compete with data, and large editorial typography inside dense tools.
- Excessive gradients, glassmorphism, huge round cards, animated backgrounds, and overbuilt motion.
- Default-looking blue-white-gray templates with no hierarchy, poor spacing, generic fake metrics, or meaningless charts.

## 6. Admin Visual Impact

Use high visual design only where it improves brand recognition, orientation, business understanding, or action conversion.

Required high-impact surfaces:

- Login page: branded first screen, clear authentication path, trustworthy copy, primary login CTA, secondary help/security links, and a visual asset or brand background when assets are available.
- Workbench first screen: dashboard hero, command header, or branded overview that summarizes identity, today's priorities, urgent tasks, key metrics, notices, and quick starts.
- Module homepage: visual overview that explains the module's purpose, primary actions, status, and next best actions.
- Empty states: business-specific explanation, permission-aware CTA, and generated or existing visual asset when useful.
- Announcement/onboarding: focused message, one primary CTA per intent, supporting visual, and dismiss/read state.
- Dashboard/big screen: stronger theme, chart rhythm, motion when useful, clear metric definitions, refresh/state indicators, and visible abnormal states.

Rules:

- Do not turn every content page into a hero page.
- Do not use marketing copy where operational copy is needed.
- Do not invent fake business numbers, fake brands, fake logos, QR codes, or decorative trust claims.
- Keep CTA labels direct and action-specific. Avoid duplicate CTA intent on the same surface.
- Button text must not wrap on desktop and must pass contrast checks.
- Hero/command-header copy must be short enough to scan while working.
- Use real UI components for product previews. Avoid fake screenshot divs.
- Motion must communicate navigation, loading, reveal, expansion, or data change; avoid scroll storytelling and decorative loops in normal admin work.
- Before finishing, reread visible copy and replace vague, poetic, or AI-sounding text with concise business language.

Read `references/admin-visual-impact.md` before implementing login, workbench first screen, module homepage, onboarding, empty state, dashboard hero, command-center visuals, or any generated admin bitmap asset.

## 6A. Public Portal And Advanced Motion

If the admin system includes a public portal, official website, landing page, user-facing console homepage, invite page, registration flow, help center, tenant welcome page, or report cover, treat that surface as a frontend product surface attached to the admin system.

Rules:

- Keep `ric-admin-console` as the entry skill, but actively inherit `ric-design-taste-frontend` for brand read, visual variance, visual asset priority, CTA quality, copy audit, motion discipline, and anti-template checks.
- For public portal, login/register, tenant welcome, module landing, workbench hero, command center, report cover, and onboarding surfaces, visual impact may be `product` or `immersive`.
- GSAP, Three.js/WebGL, 3D cards, canvas backgrounds, advanced scroll/motion choreography, and generated hero imagery are allowed only when they serve orientation, brand recognition, data comprehension, guided focus, or state change.
- Retrieve local `gsap-core`, motion, Three.js/WebGL, imagegen, and design-taste skills when those technologies are in scope; if a skill is missing, check the project dependency and official documentation before coding.
- Isolate heavy motion or WebGL in leaf components with cleanup and reduced-motion fallbacks. Do not mix GSAP/Three.js/Motion control of the same animated surface.
- Do not apply scroll storytelling, parallax, animated backgrounds, or cinematic transitions to ordinary CRUD, permission, audit, settings, or dense detail pages.
- Browser screenshot and interaction verification must include both the high-impact surface and at least one utility admin page, so visual ambition does not pollute operational pages.

## 7. Admin Asset Generation

Admin systems usually need fewer generated visuals than marketing pages, but they still benefit from deliberate project-specific assets. When the system needs visual assets and no suitable existing brand/design-system asset exists, invoke the relevant agent image generation ability instead of shipping generic placeholders.

Generate assets for:

- Logo/brand mark and app icon when no suitable brand asset exists.
- Sidebar/topbar brand mark variants.
- Generated small icon pack when the user asks for all small icons to be generated, or when project-specific module icons are not covered by the chosen icon library.
- Login page illustration, visual panel, or brand background.
- Empty states for workbench, list pages, import/export, messages, tasks, and permissions.
- Low-contrast dashboard texture or module background.
- Announcement or onboarding banner.
- Product/module icon concepts when no icon system exists.
- Profile/avatar placeholder sets when the system needs neutral defaults.
- Report cover or export preview artwork when the product has document/report flows.

Rules:

- Prefer existing brand assets and UI-library icon systems first for functional icons.
- Generated admin assets must be quiet, enterprise-refined, low-noise, and secondary to the data.
- Do not generate decorative hero art for normal CRUD pages.
- Do not put critical UI text inside generated images.
- Do not use fake logos, trademarks, QR codes, watermarks, fake company names, or fake business data inside generated images.
- Save project-bound generated assets into the workspace and wire them into the app; never leave referenced assets only in a tool temp folder.
- If agent-native image generation, the built-in image tool, MCP image tool, or IDE image tool is missing or unavailable, read `../../references/ric-imagegen-fallback.md` and use the bundled CLI fallback directly. The CLI path requires `OPENAI_API_KEY`; if it is missing, stop and ask for that environment variable.

## 8. Required Shell Layouts

Support these layout modes. Pick one based on the brief or existing project:

1. `sidebar-only`
   - Left sidebar menu.
   - Logo at the top of the sidebar.
   - User avatar, nickname, settings, and secondary icons at the bottom.
   - Main content area on the right.

2. `topnav-only`
   - Top menu.
   - Logo on the left.
   - Avatar, nickname, settings, and secondary icons on the right.
   - Header stays fixed while scrolling.

3. `sidebar-with-topbar`
   - Left sidebar menu plus top bar.
   - Top bar has logo on the left and avatar/nickname/settings/secondary icons on the right.
   - Top bar stays fixed while scrolling.
   - Top bar center can be empty, announcement, unread messages, global search, shortcuts, environment tag, tenant switcher, or a custom business module.

All modes require:

- Breadcrumbs at the top of the content page.
- Current route highlighted in the menu.
- Grouped menus that can expand and collapse.
- Permission-aware menu visibility and disabled states.
- Responsive collapse behavior for narrow screens.
- Main content scrolling without breaking fixed top/header regions.

## 9. Authentication And Permissions

Model these states explicitly:

- Anonymous / unauthenticated.
- Logged in but missing permission.
- Logged in with partial permissions.
- Logged in as administrator or privileged role.
- Token expired / session timeout.

Rules:

- Hide protected menus and actions when unauthenticated.
- Do not show create/edit/delete/export/import/bulk actions without permission.
- Route guards must align with menu filtering and button visibility.
- Sensitive back-end operations must still enforce permissions server-side.
- When a user lacks permission, prefer a clean disabled state or 403 page over broken invisible failures.

## 10. Navigation And Breadcrumbs

Menus:

- Provide navigation for pages and functional areas.
- Support grouped menu sections.
- Support expand/collapse per group.
- Support nested items when the system hierarchy requires it.
- Show route-active state, disabled state, external-link state, and unread/count badges when applicable.

Breadcrumbs:

- Show the current page location in the system hierarchy.
- Let users navigate upward with real links or click handlers on parent items.
- Preserve list filters, sorting, pagination, tab, and scroll state when returning from detail pages.
- If browser history is unreliable or empty, navigate to the parent route with saved query/state instead of doing nothing.
- Keep breadcrumb labels consistent with route titles and menu labels.
- Leave clear spacing between breadcrumbs and the page title/header; never make them visually stick together.

Avatar dropdown:

- Clicking avatar or nickname opens a dropdown.
- Required items: personal information, system settings, logout.
- Optional items: account security, notification preferences, theme, tenant switch, message center.
- Logout must be explicit and safe; clear tokens/session and redirect to login.

## 11. Default Workbench

Most admin systems should open to a workbench page. Treat the top of the workbench as a product surface, not a generic card dump.

Include relevant cards:

- User summary: name, role, department, current tenant, quick status.
- Calendar: in-progress projects, tasks, deadlines, meetings, approvals.
- Todo list: pending tasks, approvals, incidents, messages.
- Activity feed: operations, workflow updates, team dynamics.
- Quick start / shortcuts: frequently used modules and create actions.
- Personalized metrics: role-relevant counts, trend deltas, SLA reminders, health indicators.
- System notices: announcements, maintenance, unread messages.

Workbench visual rules:

- Use a dashboard hero, command header, or branded overview when the workbench is a primary entry page.
- Show identity and priorities: role, department/tenant, today's focus, urgent work, key metrics, notices, and quick starts.
- Give CTAs clear operational intent, such as create order, handle approval, invite user, view risk, or configure integration.
- Use brand visuals, textures, or generated assets only when they support orientation and hierarchy.
- Keep core numbers, tasks, and actions immediately scannable.

Do not use meaningless fake data. If mock data is necessary, make it domain-specific and replaceable.

## 12. List Page Protocol

A standard list page contains a query card and a table card.

Page header:

- Render the current page title once.
- Breadcrumb labels, page header title, module hero title, and table card title must not repeat the same title as separate large headings.
- If a module hero or command header already owns the page title, the table card title should be a compact dataset label or omitted.

Query card:

- Place it at the top.
- Fields reflect real table query dimensions.
- Include search and reset actions on the right.
- Pressing Enter in inputs triggers search.
- Searching updates table data and resets pagination to page 1 unless using infinite scroll.
- Keep advanced filters collapsible when more than one row is needed.

Table card top-left:

- Primary create action only when it is not already present in a page hero or command header.
- Bulk delete appears when row selection exists and the user has delete permission.
- Other batch actions only when permission and selection semantics are clear.

Table card top-right:

- Refresh icon.
- Column settings icon.
- Density icon when the UI library supports it.
- Export/import icons only when authorized.

Table body:

- First column is selection only when multi-select is supported.
- Selection can support cross-page selection; if so, show selected count, clear selection, and cross-page semantics.
- Second column is usually the name/title column.
- Clicking name opens a detail page or detail modal/drawer depending on complexity.
- Sortable headers show visible sort state.
- Status fields use consistent semantic tags.
- The last column is actions: edit, delete, and more actions in an overflow menu.

Selection toolbar:

- Show one selected-count message.
- Show one clear action, default label `清空选择`.
- Do not render both `取消选择` and `清空选择`.
- When deletion is allowed, show `批量删除` after selection; use danger styling and require confirmation with selected count and cross-page semantics.
- Disable batch actions when the selection is empty or permission is missing.

Table footer:

- Use pagination by default.
- Infinite scroll mode removes pagination but must show loading, reached-end, and retry states.

## 13. Modal, Drawer, And Form Protocol

Modal:

- Contains title, content area, and action area.
- Content scrolls internally after reaching 90% viewport height or 70% viewport width.
- Do not show scrollbars when content does not overflow.
- Use for short create/edit/detail flows.

Drawer:

- Prefer for long forms, complex detail, side-by-side inspection, or preserving list context.
- Use clear sectioning and sticky footer actions for long content.

Forms:

- Labels use concise Chinese business language.
- Required fields, validation messages, help text, disabled fields, loading, submit failure, submit success, and dirty state must be handled.
- Long forms should be grouped by business meaning.
- Dangerous operations require confirmation and clear effect wording.

## 14. Detail And Profile Pages

Detail pages:

- Use a page for complex detail and a modal/drawer for simple detail.
- Include basic information, status, associated data, operation history/activity, attachments when applicable, and permission-aware actions.
- Preserve list filters, pagination, and sorting on return.
- Choose tabs, descriptions, timeline, child tables, and audit logs based on business complexity.

Personal center:

- Enter from avatar dropdown.
- Include profile, password change, account security, login records, notification preferences.
- Password change includes old password, new password, confirmation, strength hint, and submit feedback.
- Separate editable profile fields from read-only organization/role fields.

## 15. Additional Page Patterns

Implement the right pattern for the business domain:

- Permission management: users, roles, departments, permission points, menu permissions, data permissions.
- Approval/workflow: pending, processed, initiated, detail, timeline, current node, operation buttons.
- Dashboard: metrics, trend charts, distributions, ranking, alerts, and explicit metric definitions.
- Settings: system, notification, integration, parameter config, save/reset, dangerous zone.
- Audit logs: operation logs, login logs, API logs, filters for time, actor, module, result.
- Message center: unread messages, announcements, task reminders, batch read, filters, detail.
- Error pages: 403, 404, 500, network error, login expired, no permission, empty state.
- Import/export: template download, upload, parse preview, error-row download, import progress.
- Task center: async task list, progress, success/failure, retry, result download.

## 16. Scrollbar And Overflow Discipline

- Avoid double scrollbars between `body`, shell, main content, cards, tables, modals, and drawers.
- Long sidebar menus, table regions, modal bodies, and drawer bodies may scroll; normal cards should not create unnecessary internal scroll areas.
- Do not show scrollbars when content does not overflow.
- Use a shared scrollbar style such as `ric-scroll-region`: transparent track, semi-transparent rounded thumb on hover/scroll/focus, thin width, and no arrow buttons.
- For WebKit, hide scrollbar buttons with `::-webkit-scrollbar-button { display: none; }`.
- For Firefox, use `scrollbar-width: thin` and `scrollbar-color: rgba(...) transparent`.

Read `references/component-contracts.md` for the full scrollbar and overflow contract before implementing complex list/table/modal pages.

## 17. Implementation Discipline

- Use structured data for routes, menus, permissions, table columns, form schemas, and status dictionaries.
- Keep layout shell separate from page content.
- Keep list state in URL query, router state, or a predictable store so back navigation works.
- Centralize request/loading/error handling.
- Do not duplicate column definitions across table, detail, export, and column settings when a shared model can be used.
- Use stable keys for menu items, table rows, form fields, and permissions.
- Keep Chinese copy concise and business-specific.

## 18. Final Check

Before finishing, read `references/acceptance-checklist.md` and verify:

- Layout mode matches the brief.
- Auth and permission states are handled.
- Menus, breadcrumbs, active route, and profile dropdown work.
- Workbench/list/detail/profile patterns match the request.
- Tables handle loading, empty, error, sorting, pagination/infinite scroll, column settings, selection, and actions.
- Main content pages avoid duplicated titles, duplicated create buttons, duplicated selection-clear actions, and missing batch delete when deletion is allowed.
- Modals/drawers/forms handle overflow, validation, submission, and dangerous confirmations.
- Scrollbars are hidden when unnecessary and polished when visible; no double-scrollbar layout.
- Visual style is enterprise-refined Chinese admin UI with admin-adapted brand impact where the page type needs it.
- Login, workbench, module homepage, onboarding, announcement, dashboard hero, and empty states use visual assets, CTA hierarchy, copy self-audit, and anti-template judgment when relevant.
- Asset Plan was followed; generated asset paths are reported, or no generated asset was needed for the page type.
- Framework-specific skills and checks were used when a matching UI framework skill exists.
- Ordinary CRUD, permission, audit, settings, and detail pages remain efficient and are not polluted by marketing-page hero patterns.
- Repository lint/test/build or available validation commands pass.

For runnable UI work, also read and execute `references/validation-loop.md`:

- Use Browser or available browser automation to open the real app and capture screenshots. Do not rely only on terminal checks or mental review for UI quality.
- Compare screenshots against the triggered skill points and acceptance checklist.
- If screenshots reveal a mismatch, fix it and repeat run -> screenshot -> compare until all required checks pass.
- Final handoff must list checked pages/states, viewport sizes, issues found, fixes made, verification loop count, and residual risks.
- If screenshots cannot be completed because the project cannot run, dependencies/env/backend are missing, or browser tooling is unavailable, state the exact blocker and run the strongest available substitute. Do not claim screenshot verification passed without real screenshots.
