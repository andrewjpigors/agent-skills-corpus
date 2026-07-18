---
name: hono-cf-clean-arch
description: Prescriptive clean architecture conventions for full-stack monorepo apps with a Hono backend on Cloudflare Workers and a React SPA frontend. Use when creating, refactoring, reviewing, or adding features to such a project — it dictates the server directory layout, dependency rules, port/adapter conventions, the shared DTO contract, and the lightweight frontend rules. Also use when asked to "apply clean architecture" to a Hono/Workers project.
---

# Clean Architecture for Hono + Cloudflare Workers + React SPA

This skill makes every project with this stack share one structure. It is a pragmatic
adaptation of Robert C. Martin's Clean Architecture: the dependency rule is enforced
strictly; the ceremonial patterns (Interactor classes, Output Ports, Presenters) are
deliberately dropped. When in doubt, the test is "can business logic be tested without
Workers, D1, or fetch?" — not "does it look like the book".

The circles govern `server/` only. The React SPA is the outermost delivery mechanism
of the system; it follows the lightweight frontend rules below, never the circles.

> **Held to the law.** This skill implements the Agent Laws [Architecture Law](../../laws/20-architecture.md) (`AR-001`–`AR-008`) — the Dependency Rule, ports at boundaries, isolation-testability, and automated enforcement — for the Hono + Cloudflare Workers + React stack. The Law is the binding standard; this skill is one stack's way to satisfy it. A reviewer judges an implementation *and* this skill against the Law.

## Canonical layout

```
server/
  domain/          # Pure business rules. Plain TS, zero outward imports.
  usecases/        # Application operations. Imports domain + ports only.
    ports.ts       # Interfaces + port-level error classes for everything beyond the process boundary.
    deps.ts        # The Deps interface aggregating all ports.
  adapters/        # Implementations of ports.
    repos/         # Drizzle repositories. The ONLY place drizzle/schema is imported.
    providers/     # External HTTP API clients (metadata sources, etc.) + DTO mapping.
    gateways/      # Other external services (downloaders, indexers, webhooks...).
  http/            # Hono routes as chained `*Routes` consts (→ AppType), zod schemas, error mapping, auth middleware.
    context.ts     # AppBindings (plain env interface) + AppVariables + AppEnv. Keeps AppType browser-safe.
  auth.ts          # better-auth integration (when used) — see the auth note below.
  composition.ts   # createDeps(env): wires adapters into usecases. The only place adapters are constructed.
  worker.ts        # Worker entry (fetch/scheduled): secure headers, per-request deps wiring, app + ASSETS.
  db/              # drizzle schema + client factory (consumed by adapters/repos only).
shared/            # API contract: DTO types + pure helpers usable by both sides.
src/               # React SPA. Its own enforced layering (see Frontend structure), not the circles.
migrations/        # D1 migrations.
```

The number of subdirectories under `adapters/` may vary per project; the four layers
and their names (`domain`, `usecases`, `adapters`, `http`) do not.

## Path aliases

Three aliases, defined identically in `tsconfig.json` paths, `vite.config.ts`, and
`vitest.config.ts` (all three must agree or resolution silently differs per tool):

- `@/*` → `src/*` — the SPA's home; frontend files import their siblings absolutely.
- `@server/*` → `server/*` — the server's home; server files use it for any
  cross-directory (upward) import. Same-directory siblings stay `./x` (more readable,
  shows cohesion). This keeps the two halves symmetric — each has a clean self-alias
  instead of `../../../` chains.
- `@shared/*` → `shared/*` — the contract, imported by both halves.

The aliases are globally defined, so they do NOT enforce boundaries — the SPA
*could* type-resolve `@server/...` and the server `@/...`. Both directions are
forbidden by dependency-cruiser (`frontend-not-into-server`, `server-not-into-frontend`);
the only legal cross-half import is `@shared/*`. dependency-cruiser resolves the
aliases via the tsconfig, so the rules catch aliased violations too.

## Dependency rules (enforced, not advisory)

Direction: `http → usecases → domain`, `adapters → usecases(ports) + domain`,
`composition → everything`. Never the reverse.

1. `domain/` imports nothing except other `domain/` files and `shared/` pure helpers.
   No hono, no drizzle, no zod, no fetch, no env access.
2. `usecases/` imports `domain/`, `shared/` types, and its own `ports.ts`. It must not
   import `hono`, `drizzle-orm`, `zod`, anything in `adapters/`, `http/`, or `db/`.
3. `fetch` is only called inside `adapters/`. `drizzle-orm` and the schema are only
   imported by `adapters/repos/` (and `db/` itself).
4. `http/` translates: zod-validate input → call usecase → serialize DTO. No business
   rules, no SQL, no fetch. Routes get dependencies from context
   (`c.get('deps')`), never construct adapters.
5. `composition.ts` is the only composition root. Workers are per-request: it must be
   a cheap factory returning a plain object — no DI container, no module-level
   singletons holding env-derived state. Keep `createDeps(env)` request-free so the
   `scheduled`/queue entrypoints can reuse it; request-bound capabilities are handed
   to usecases as function parameters (see below).
6. Ship the dependency-cruiser config from `templates/dependency-cruiser.cjs` and wire
   `pnpm lint:arch` into CI. Prose rules decay; CI rules don't.

## Hard-won wiring rules (from real migrations)

- **Hono registration order is load-bearing.** Middleware only guards routes
  registered after it, and static paths must register before parameter paths
  (`/indexers/search` before `/indexers/:id`). With Hono RPC (the default), routes
  are chained `*Routes` consts composed in `app.ts` via `.route()`, and order is the
  chain order: public routes, then `.use('*', requireAuth)`, then protected routes.
  Place middleware deliberately in the chain and keep static-before-param within each
  resource const. (Pre-RPC, the equivalent was `registerXxxRoutes(routes)` functions
  called in order; chaining replaces that and additionally yields `AppType`.)
- **Port-level error types.** An error class thrown by an adapter and caught by
  `http/` for status mapping must be declared in `usecases/ports.ts`
  (`BookProviderError`, `MusicProviderError`, ...). If it lives in the adapter, the
  http layer is forced to import the adapter and the boundary breaks.
- **better-auth (or any auth framework that owns its own tables and handles raw
  requests) spans layers.** Keep it as a single named module at `server/auth.ts`,
  consumed by `http/` and `composition.ts`, and give it a named exception in the
  drizzle rule. Forcing it into `adapters/` just trades one violation
  (drizzle-outside-repos) for another (http-into-adapters).
- **Request-bound capabilities** (e.g. better-auth's `createUser`, which needs the
  request origin) don't go into `Deps`. Pass them to the usecase as a plain function
  parameter built by the route — a one-function port. The business rule (when the
  call is allowed, what happens after) stays in the usecase; only the request-bound
  construction stays in http.
- **Streaming/SSE endpoints**: the usecase takes `(deps, ..., signal, emit)` — it
  emits domain events and resolves when upstream streams end. `http/` owns
  `ReadableStream`, the `Response`, and SSE wire formatting. `Response` objects never
  leave the http layer. The route must own one `AbortController` and abort it from
  BOTH teardown paths — the request signal AND `ReadableStream.cancel()` (they are
  independent in Workers); passing `c.req.raw.signal` straight into the usecase
  leaks upstream connections when only the body consumer cancels.
- **Repos return parsed records.** Stored JSON config columns (`credentialsJson`)
  are parsed inside the repo into the same config shape the gateway ports take, so
  serialization never appears in usecases.
- **Authenticate AND authorize/scope — they are different.** A `requireAuth`
  middleware that verifies a token but routes/usecases that ignore the principal is a
  data-leak waiting to happen (every user sees every row). Pass the principal
  (`c.get('user').sub`) into the usecase/repo and scope queries by owner (or org).
  The example resource must demonstrate this, not just gate the route.
- **Keyset pagination needs a unique tiebreaker.** A cursor over a non-unique column
  (`createdAt`) silently drops rows that share a value. Order by and key the cursor on
  `(createdAt, id)`; the opaque cursor encodes both, the `WHERE` is
  `createdAt < c OR (createdAt = c AND id < cid)`. Cursor encode/decode is a
  persistence detail — keep it in the repo; http passes the cursor through opaquely.

## Ports

- A port is a plain TypeScript interface in `usecases/ports.ts`, named for the
  capability (`LibraryRepo`, `MediaProvider`, `DownloaderGateway`), not the vendor.
- Port granularity = process boundary. DB access, external HTTP, queues get ports.
  Internal pure helpers do not — call them directly.
- Multi-implementation concepts (e.g. several downloader kinds) get one port and one
  adapter file per kind, dispatched by a lookup table in composition or the adapter
  index — never `if (kind === ...)` chains inside usecases.
- Usecases are plain functions (or small modules of functions) taking `deps` as the
  first argument: `submitDownload(deps, userId, input)`. No classes unless state
  genuinely requires one.

## Data crossing boundaries

- `shared/types.ts` (or `shared/*.ts`) is the API contract between server and SPA.
  DTOs there are plain, framework-free data — usecases may accept and return them
  directly. Do not add a second mapping layer when the DTO already fits.
- Drizzle rows never leave `adapters/repos/`. Repos map rows to domain/DTO shapes.
- Framework objects (Hono `Context`, `Request`, `Response`) never enter `usecases/`.
- Domain types that have no business on the wire stay in `server/domain/`; don't dump
  them into `shared/` "for convenience".

## Explicitly NOT done (anti-ceremony list)

An agent applying the book literally will produce these. Reject them in this stack:

- No DI frameworks or containers. `createDeps(env)` returning a plain object is the
  whole mechanism.
- No Interactor classes, no Input/Output Port interface pairs per operation.
- No Presenters for JSON APIs — the DTO is the presentation.
- No Request/Response Model classes duplicating a zod-inferred type or shared DTO.
- No repository interface methods speculatively added "for later". Ports contain only
  what usecases call today.
- No pass-through usecases. When a route is a pure forward to a single port call
  (e.g. book search → `deps.bookProvider.search(...)`), call the port from the route
  via `deps` directly. A usecase exists when there is orchestration (resolve config +
  call, multi-port flows, state rules) — an empty wrapper is ceremony.
- No clean-architecture layering inside `src/` (the React app).

A 10/10 architecture here = dependency-cruiser passes + business rules testable with
fake ports + layer sizes proportional to the project. Pattern count is not a score.

## Frontend structure (enforced, like the server)

The SPA is not governed by the server circles, but it gets its own deliberate
layering — also checked by `pnpm lint:arch` (cruise `src/` too). This is what keeps
derived projects from rotting into one `components/` + one `lib/api/` god-pile.

```
src/
  app/         providers, router, shell — composition; MAY import anything in src.
  routes/      thin page components, mounted only by app/router (leaves).
  features/    one dir per feature (notes, auth): api.ts (RPC calls) + hooks.ts
               (react-query) + feature-local components. Features are ISOLATED —
               a feature never imports another feature; share via lib/ or shared/.
  components/  reusable presentational: ui/ primitives (shadcn) + shared widgets.
               NEVER imports features/routes.
  lib/         cross-cutting infra: rpc, config, token, theme, query-client, utils.
               A LEAF — imports nothing from features/routes/app/components.
  i18n/        setup + locales/ (one file per locale; zh satisfies `typeof enUS`).
  styles/, test/
```

The dependency-cruiser rules that encode this (in `templates/dependency-cruiser.cjs`):
`frontend-features-are-isolated`, `frontend-lib-is-a-leaf`,
`frontend-components-no-features`, `frontend-routes-are-leaves`. The app shell
(nav + auth + theme) is composition, so it lives in `app/`, not `components/` —
putting it in `components/` would break `components-no-features`.

The rules (the whole list):

1. All HTTP goes through the typed RPC client `src/lib/rpc.ts` (see below).
   Components and hooks never call `fetch` directly; features call `rpc`, pages call
   feature hooks.
2. Server data shapes come from `shared/` — never re-declared in `src/`.
3. Server state lives in react-query (per-feature `hooks.ts`); UI state lives in
   components/context. Don't mix.
4. If genuine client-side domain logic appears (offline-first, editors, local state
   machines), extract it into dependency-free pure TS modules with their own tests.

## Hono RPC (the typed client — frontend default)

The SPA calls the API through Hono's RPC client, not hand-written fetch wrappers —
one source of truth for routes, params, and response types.

- Server: routes are **chained `*Routes` consts** (`new Hono<AppEnv>().get(...).post(...)`),
  composed in `app.ts` via `.route()`, and `app.ts` does `export type AppType = typeof app`.
  Register-functions returning `void` lose the types — RPC needs the chain.
- Client: `export const rpc = hc<AppType>('/', { fetch: authFetch }).api`. `authFetch`
  injects the bearer token and, on 401, clears it and redirects to `/login`.
- **Keep `AppType` browser-safe, or the type-import drags Workers types into the web
  tsc program.** Type the http layer with a plain `AppBindings` interface (the env
  vars routes read, as strings) in `http/context.ts` — NOT `Cloudflare.Env`. The full
  `Env` (D1/ASSETS) and the `createDeps` deps-middleware live in `server/worker.ts`,
  which the SPA never imports. `getAuthConfig` takes a plain `AuthEnv` interface for
  the same reason. Then `import type { AppType }` pulls only hono + shared + browser-safe
  TS into the web build.
- This is the ONE compile-time link from `src/` to `server/`. The
  `frontend-not-into-server` rule allows it via `dependencyTypesNot: ['type-only']`
  (runtime is still pure HTTP). depcruise needs `tsConfig` pointed at a config that
  resolves both halves' aliases + parses `.tsx` (use `server/tsconfig.json`, which
  inherits `paths` + `jsx` from the base — give the base `jsx: react-jsx`); the root
  base has `files: []` and can't be loaded directly.

## Auth (OIDC at the edge — the template default)

Stateless OIDC, no custom login backend, no session table:

- SPA logs in with the provider (`oidc-client-ts`, Authorization Code + PKCE), stores
  the token (id_token, aud = client id) in localStorage (`lib/token.ts`), sends it as
  `Authorization: Bearer`.
- API verifies the JWT in a `requireAuth` middleware via an `AuthVerifier` port +
  `jose` adapter (against the issuer's JWKS). The user comes from token claims. The
  verifier is a normal adapter/port — auth fits the circles cleanly (unlike a
  table-owning framework; that's the better-auth case below).
- **Dev/E2E bypass:** an `OIDC_DEV_USER` env accepts any bearer as a fixed user, so
  e2e injects a token instead of driving a real IdP. Gated by env, `console.warn`s,
  documented "never in production". Real verification is covered by the integration
  suite (a test keypair signs a token; the worker verifies against a local JWKS).

## Runtime config: one env set, on the backend

Do NOT keep a parallel `VITE_*`/`.env` for the frontend. The worker env is the single
source of truth; the SPA fetches its PUBLIC config (issuer, client id, feature flags…)
from `GET /api/configz` at startup (`lib/config.ts`, awaited before render). The same
built bundle then runs in every environment. `configz` exposes only public values —
never secrets.

## Product specs (BDD-lite, no Cucumber)

A `spec/` directory is the product source of truth — what the app does, described
behaviour-first, independent of implementation. Use Gherkin `.feature` files (formal
grammar, standard, and the zero-migration input for the escalation path) but with NO
Cucumber runner — they are documentation; the step-definition tax buys nothing when
the author and the only reader are the same engineer.

- One `.feature` file per capability. Each scenario carries two tags: the stable id
  `@<capability>/<slug>` and the layer that proves it (`@domain`/`@usecase`/`@web`/
  `@api`/`@e2e`). Ids never change once written. Tags are trivially greppable — a
  cleaner id mechanism than embedding ids in prose.
- **Traceability instead of generation:** each scenario's home test carries
  `[spec: <id>]` in its name. Tests reference the spec; the spec does not generate
  tests. Keep `spec/` pure (`.feature` + README) — no test code in it.
- **Verify at the cheapest layer, not all at E2E.** A scenario maps to whatever
  layer can prove it — most land in usecase/web/api; reserve e2e for genuinely
  cross-stack, hermetic journeys. This is the pyramid discipline; BDD-lite must not
  become "everything is a slow E2E".
- **Don't over-build the enforcement.** A spec↔test coverage check is a *governance
  lint* (sibling to `lint:arch`), not a behavioural test — if you add one, package it
  as a lint script, never as a `.test.ts` dropped into `spec/` or a one-file `test/`
  dir. Often the `[spec: id]` breadcrumbs alone are enough; add automation only if
  drift actually bites.
- **Escalation path:** if a non-technical audience ever needs to *run* the Gherkin,
  use `playwright-bdd` (compiles `.feature` → Playwright, keeps the native runner),
  not raw `@cucumber/cucumber`. The prose already uses Gherkin wording, so it's a
  mechanical migration. Don't reach for it preemptively.

## Infra conventions

- **Worker entry** lives at `server/worker.ts` (fetch + scheduled), not its own
  top-level dir. It's the entry/composition consumer — it may import `http`,
  `composition`, usecases freely (like `main()`); it sits at `server/` root and is
  arch-checked.
- **Env type is generated, not hand-written.** `pnpm cf-typegen` runs
  `wrangler types server/worker-configuration.d.ts --include-runtime=false --env-file .dev.vars.example`
  → a small gitignored `server/worker-configuration.d.ts` declaring `Cloudflare.Env`;
  `server/env.ts` is just `export type Env = Cloudflare.Env`. Put the path arg
  FIRST — `--env-file` is an array flag and would swallow a trailing positional.
  `--env-file .dev.vars.example` (a committed key list) keeps it CI-safe — secrets'
  *names* come from the example, not `.dev.vars` (which CI lacks). Regenerate on
  `postinstall`. Edit bindings in wrangler.toml, never the type. (For a 1–2 binding
  worker this is borderline; adopt it once there's a real binding surface.)
- **tsconfig layout:** a root `tsconfig.json` base (compilerOptions + `paths`,
  `files: []`) plus a leaf per runtime — `server/tsconfig.json`
  (`@cloudflare/workers-types`) and `src/tsconfig.json`. Both set `jsx: react-jsx`
  (put it in the base so depcruise, which loads `server/tsconfig.json`, can parse
  `.tsx`; harmless for the server, which has none). Keep the leaves IN their dirs so
  the editor routes each file to the right type environment. Do NOT merge them —
  workerd and DOM/React globals conflict (which is why `AppType` must be browser-safe;
  see Hono RPC). Don't leave decorative `references` in the base if `typecheck` runs
  explicit `tsc -p` passes (they only matter under `tsc -b`).
- **DB: schema.ts is the single source; migrations are generated.** Use
  `drizzle-kit generate` (`pnpm db:generate`), never hand-written SQL. CI guard:
  run `db:generate` and fail if `git status --porcelain migrations` is non-empty
  (schema.ts changed without a committed migration).
  - **Retrofitting onto existing hand-written migrations with prod data**
    (non-destructive baseline): keep the legacy `NNNN_*.sql` as applied history;
    add `drizzle.config.ts` with `migrations: { prefix: 'timestamp' }` (so generated
    files sort AFTER the legacy `0001..` and never collide). Baseline drizzle's
    snapshot to the current schema: `drizzle-kit generate --name baseline` (emits a
    full snapshot + a create-all SQL), then **delete the baseline SQL file** and keep
    only `migrations/meta/`. drizzle reads only the snapshot to diff, so there is
    nothing to apply (the legacy migrations already create the schema) and no empty
    migration to choke D1's "must contain a statement". Verify with `drizzle-kit
    generate` → "No schema changes". From then on, schema edits emit timestamped diff
    migrations. Do NOT squash when prod has applied the old ones — wrangler tracks
    migrations by filename and would re-run create-all.
  - Keep the integration-suite drift guard too (introspect each migrated table via
    `PRAGMA table_info`, compare to `getTableConfig(table).columns`): it proves the
    legacy history + generated migrations still equal schema.ts on a real D1, and
    catches hand-edits to any migration SQL.
- **Frontend api client is the Hono RPC client** (`src/lib/rpc.ts`, `hc<AppType>`),
  not hand-written fetch wrappers — see the Hono RPC section. Per-feature `api.ts`
  modules call `rpc`; `lib/rpc.ts` owns the bearer header + 401 redirect.
- **Commit + editor hygiene (template defaults):** Conventional Commits enforced by a
  husky `commit-msg` hook (commitlint); Biome on staged files via a `pre-commit` hook
  (lint-staged); `.editorconfig`, `.nvmrc`, `.vscode/` (Biome as formatter). A `LICENSE`,
  dependabot (npm + actions), and a PR template round out repo hygiene.
- **Security headers:** `hono/secure-headers` on the worker for `/api/*`; a
  `public/_headers` file for the SPA's static responses (Cloudflare assets honors it).
- **CD:** a `deploy.yml` ships `main` to Cloudflare (build → `db:migrate:remote` →
  `wrangler deploy`), gated behind a repo variable (`ENABLE_DEPLOY`) so it's skipped —
  not failed — until secrets + a real `database_id` are configured. `pnpm run deploy`
  (not `pnpm deploy`, which collides with pnpm's builtin) for manual.
- **Consistent API errors:** one `onError` in `app.ts` maps `HTTPException` → its
  JSON shape and anything else → 500. Routes throw; they don't hand-format errors.

## Testing strategy

The layers ARE the test taxonomy — don't invent a separate one. There is one
suite per layer; they collapse into a few **runtimes**, not naming tiers. Wired as
vitest `projects` plus a Playwright suite (see `templates/vitest.config.ts`,
`templates/playwright.config.ts`):

- `unit` (node) — server domain/usecases/adapters + shared.
- `web` (jsdom) — frontend pure logic, api client, component/hook tests (MSW).
- `integration` (workerd + real D1) — full `app.fetch` flows; the server integration crown.
- `e2e` (Playwright, real stack) — the cross-stack crown; separate CI job.

`pnpm test` runs unit+web+integration; e2e is `pnpm e2e`.

**Coverage thresholds (enforced in CI).** `pnpm test:coverage` runs `unit` + `web`
with the v8 provider and fails below per-file thresholds. The key constraint: **the
workerd `integration` pool can't be v8-instrumented**, so coverage only gates the
layers the fast suites own. Scheme:
- `coverage.include` = `server/domain`, `server/usecases`, `shared`, plus testable
  frontend (`src/features`, `src/lib`) and any `adapters/providers|gateways` (stub-fetch
  tested). `thresholds.perFile: true`.
- **Business logic (`server/domain`, `server/usecases`): 95%** via per-glob override.
  Everything else gated: **90%**.
- **Exclude the integration/e2e-only edge layers** (`adapters/repos`, `composition`,
  `worker`, http full-flow, the real JWKS verify path) — they're proven by the
  integration suite + `lint:arch`, not a %. Counting them under unit coverage would be
  a false 0%. Also exclude presentational/config glue (`lib/theme`, `lib/query-client`,
  `lib/utils`, `ui/` primitives) and barrels (`index.ts`).
- Gotcha: the v8 **text** reporter hides fully-covered (100%) files — a fully-covered
  business layer looks "missing". Verify with `--coverage.reporter=json-summary`; the
  thresholds use the real data regardless.
- Authenticate-vs-scope and keyset-tiebreaker (above) are exactly the kind of branches
  the 95% business-logic gate forces you to test.

**Per-layer (the fast suite — node, milliseconds, every commit):**
- `domain/`: pure unit tests, no mocks. Each pure module gets direct tests.
- `usecases/`: hand-written fake ports (plain objects). **This is where business
  branches are exhausted** — every conditional in an orchestration is cheapest to
  cover here (one fake object), so drive completeness from this layer. Never mock
  global `fetch` or drizzle here; if you need to, a port is missing.
- `adapters/`: stub `fetch` to assert request construction + response mapping
  (HTTP gateways/providers). Protocol detail (auth handshakes, 409 retries, RPC
  envelopes) lives here and is invisible to every other layer, so it MUST be
  tested here. A shared `stubFetch` helper that records requests keeps these terse.
- `http/`: a few request-level tests for validation, routing, and the auth wall —
  with a throwing DB so a leak past the wall fails loudly.

**The crown (the integration suite — workerd + real D1, what many call "API
tests"):** the dir is `server/integration/`, not `api-tests` — these are
cross-cutting integration tests of the assembled server, not module units. full flows through `app.fetch` inside the Workers runtime, real D1
binding, production migrations applied. This is the ONE place nothing is faked —
it's where repos (real SQL) and the auth/session integration finally get exercised,
so you do not write a separate repo-unit layer. **Pyramid discipline:** per resource
test happy path + auth/permission (401 + 403) + one validation failure. Do NOT
replay the usecase branch matrix here — that's already covered cheaply upstream;
duplicating it makes the slow suite slow for nothing.

**Invariant that keeps the suites from overlapping or rotting:** a fake may only
stand in for a *boundary*. usecase tests fake ports; adapter tests stub `fetch`;
the `web` suite mocks the API at the network edge (MSW); the api + e2e suites fake
nothing. If a test needs to mock across a boundary that isn't one of these, the
boundary is drawn wrong — fix the architecture, not the test.

**Frontend `web` suite (jsdom + MSW):** the frontend's bugs are integration bugs,
so weight it toward integration, not isolated unit. Test the real client logic
(the library/auth context cache reconciliation, forms, hooks) through the real api
client with MSW at the network boundary — never mock `@/lib/api`. For flows that
invalidate+refetch, back MSW with a small in-memory store so the refetch converges
(a fixed response gets overwritten by the post-mutation GET and the assertion
flaps). The project needs the React JSX plugin (`@vitejs/plugin-react-swc`) and a
setup file (jest-dom, MSW lifecycle, RTL cleanup, a `matchMedia` shim). Do NOT test
the shadcn `ui/` primitives. Use `renderHook` for context/hook logic; reserve full
component render tests for components with real branching.

**E2E (Playwright, real stack) — scope it to hermetic seams:** drive the real SPA +
Worker + local D1 + auth, but only the journeys with NO external dependency
(onboarding, auth/session/cookies, routing, admin config CRUD that only writes D1).
Flows that need TMDB/Prowlarr/etc. would make the PR gate depend on a third party —
leave those to manual/visual checking. Isolate the DB from `pnpm dev` via the vite
plugin's `persistState: { path }` behind an env flag, reset+migrate it on each server
boot, and run serially (the suite owns its DB). Onboarding seeds state, so no fixture
loading. Keep it to a handful of journeys; flaky e2e nobody trusts is worse than none.

**pool-workers gotchas (cost real time here — the package's config API churns
across versions, so verify against the installed version's exports before trusting
any snippet):**
- Recent majors export a `cloudflareTest(opts)` Vite *plugin* from the package root;
  older ones exported `defineWorkersProject` from `.../config`. `grep` the installed
  `dist/**/*.d.mts` for the actual export name.
- D1 migrations: read them at config time with `readD1Migrations(dir)`, pass the
  array in as a binding, and `applyD1Migrations(env.DB, env.TEST_MIGRATIONS)` from a
  setup file.
- Isolation between tests: newer versions dropped the `isolatedStorage` option —
  call `reset()` then re-apply migrations in `beforeEach` for a clean DB per test.
- Typing `env.DB`/custom bindings inside tests needs a `declare namespace Cloudflare
  { interface Env { ... } }` augmentation in a `.d.ts` next to the integration tests.

**Migrating existing tests:** an orchestration test that stubbed global `fetch` over
a fake DB becomes fake repo + REAL gateway objects + the same `fetch` stub — coverage
is preserved and the fake shrinks from a drizzle call-chain mock to a one-method
object. Don't replace the gateway with a fake in those tests, or the adapter's
request-building/mapping silently loses coverage.

## Workflow

- New project: **start from the `saas-web-starter` template repo**
  (github.com/saltbo/saas-web-starter) — it IS this skill materialized: the four
  layers, all configs (dependency-cruiser, per-dir tsconfig, wrangler types,
  drizzle-kit), the unit/web/api vitest split + Playwright e2e, the `spec/`
  convention, CI running every gate, and a `notes` slice as the copy-me example.
  Clone/`gh repo create --template`, rename, then copy the `notes` slice per
  capability. (The `templates/` files here are the same artifacts, for reference or
  retrofitting an existing repo.) Note: Cloudflare's Workers Builds only builds — the
  CI workflow is what runs the gates; without it they're local-only and decay.
- Existing project: follow `references/migration.md` — behavior-preserving steps, one
  commit each, `typecheck && test` green after every step.
- Code review: check the dependency rules above first; for deeper principle-level
  review, the generic `clean-architecture` skill's Quick Diagnostic table applies, but
  its 10/10 scoring is overridden by the anti-ceremony list here.
