---
name: tanstack-start-cloudflare
description: Professional skill for building production-grade monolithic web applications with TanStack Start deployed on Cloudflare Workers. Covers project scaffolding with Wrangler, file-based routing with TanStack Router, server functions (RPC), D1 database with Drizzle ORM, Workers KV for caching and sessions, R2 object storage for file uploads, Supabase Auth integration (JWT validation offloaded to save Worker CPU), vanilla CSS Modules for styling, deployment environments, observability, and Cloudflare-specific anti-patterns. Assumes the React skill is available for component architecture, hooks, and forms. Use this skill for any full-stack TanStack Start + Cloudflare Workers project.
license: MIT
metadata:
  authors: "Fembyte"
  version: "1.0.0"
  requires: "react"
  based_on:
    - "https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/"
    - "https://tanstack.com/start/latest/docs/framework/react/overview"
    - "https://developers.cloudflare.com/workers/wrangler/"
    - "https://supabase.com/docs/guides/auth"
---

# Professional TanStack Start + Cloudflare Workers Skill — Monolithic Full-Stack

**Always consult the official docs for latest APIs:**
- [TanStack Start](https://tanstack.com/start/latest/docs/framework/react/overview)
- [Cloudflare Workers + TanStack Start Guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [D1 Docs](https://developers.cloudflare.com/d1/)
- [KV Docs](https://developers.cloudflare.com/kv/)
- [R2 Docs](https://developers.cloudflare.com/r2/)
- [Supabase Auth](https://supabase.com/docs/guides/auth)

> **Pre-requisite:** This skill assumes the **React skill** is already loaded. It does not re-cover component architecture, hooks, forms, state management, testing, or a11y patterns. Those are handled by the React skill. This skill focuses exclusively on the TanStack Start + Cloudflare Workers layer.

> **Styling decision:** This skill uses **vanilla CSS Modules** (`.module.css`) — no Tailwind, no CSS-in-JS. Rationale: zero runtime cost, minimal bundle impact, maximum Cloudflare Workers free tier efficiency. For design tokens, use CSS custom properties.

---

## 0. BEFORE YOU WRITE ANY CODE — Consistency Protocol

> **This section is mandatory. Skip it and you will break project consistency.**

Every time you are asked to create or modify anything in an existing TanStack Start + Cloudflare project, you MUST run this audit first. No exceptions.

### Step 1 — Audit existing project structure

```
Does the project use TanStack Start?
  Check for: app/ directory with route files, app.config.ts
  YES → Confirm TanStack Start conventions are followed.
  NO  → Run scaffolding first (see Section 2).

Does a similar route or server function already exist?
  YES → extend or compose it. Never create a duplicate.
  NO  → create following file-based routing conventions.

Does a similar database query or KV access pattern already exist?
  YES → reuse the same pattern (Drizzle query, KV helper).
  NO  → create it following the established patterns in server/ or lib/.
```

### Step 2 — Read the Cloudflare configuration

Before writing any server-side code, check:
- `wrangler.jsonc` (or `wrangler.toml`) for bindings: D1 databases, KV namespaces, R2 buckets
- `app.config.ts` for TanStack Start configuration (SSR, prerender)
- `vite.config.ts` for Cloudflare plugin settings
- `.dev.vars` for local secrets (never commit this file)

- **ONLY reference bindings that exist in wrangler config.**
- Never invent binding names — they must match exactly.
- Always run `npm run cf-typegen` after adding new bindings.

### Step 3 — Inherit naming conventions

Before naming a new route, server function, or module, look at 2–3 existing files and match their pattern exactly.

| Type | Convention | Example |
|------|-----------|---------|
| Route files | kebab-case in `app/routes/` | `blog-post.tsx`, `dashboard.tsx` |
| Route groups | `(group-name)` folder | `(auth)/login.tsx`, `(dashboard)/settings.tsx` |
| Root layout | `__root.tsx` (obligatorio) | `app/routes/__root.tsx` |
| Nested layouts | `__layout.tsx` (dentro de grupos) | `(admin)/__layout.tsx` |
| Server functions | camelCase in route file or `server/` | `getPost.ts`, `createUser.ts` |
| Database queries | `server/db/queries/` | `users.ts`, `posts.ts` |
| Database schema | `server/db/schema/` | `users.ts`, `posts.ts` |
| KV helpers | `server/kv/` | `sessions.ts`, `cache.ts` |
| R2 helpers | `server/r2/` | `uploads.ts`, `images.ts` |
| CSS Modules | `ComponentName.module.css` | `DashboardPage.module.css` |
| CSS custom properties | `--kebab-case` | `--color-primary`, `--spacing-md` |
| Environment variables | `env.*` in wrangler + `process.env.*` locally | `env.DB`, `env.KV_STORE` |

### Step 4 — Check rendering strategy

Before adding data fetching or server logic:
- Is this page mostly static? → Enable prerendering (SSG) in route config.
- Does it need real-time data per request? → Use loader + server functions (SSR).
- Is it a client-only interactive section? → Use client-side TanStack Query + server functions.
- TanStack Start default: **SSR with streaming** — loader runs on server, component renders on both.

### Step 5 — Consistency checklist before delivering code

Before responding with any code, verify:

- [ ] No raw CSS in JSX `style={{}}` — use CSS Modules or CSS custom properties
- [ ] No Tailwind classes, no shadcn/ui imports — this project uses vanilla CSS Modules
- [ ] All server-side code imports `env` from `cloudflare:workers` (not process.env)
- [ ] All D1 queries use Drizzle ORM (or the project's chosen query builder)
- [ ] All KV/R2 operations use the binding name from `wrangler.jsonc` exactly
- [ ] All server functions are typed end-to-end (input validator → handler → return type)
- [ ] Auth checks happen in server functions, not client-only
- [ ] No Node.js crypto APIs — use Web Crypto or Supabase for JWT
- [ ] File routes follow kebab-case convention
- [ ] `.dev.vars` is in `.gitignore`

---

## 1. Project Structure — TanStack Start + Cloudflare

```
project-root/
├── app/
│   ├── routes/                    → File-based routes (TanStack Router)
│   │   ├── __root.tsx             → Root layout (obligatorio, wrappea todo)
│   │   ├── index.tsx              → Home page (/)
│   │   ├── about.tsx              → /about
│   │   ├── blog/
│   │   │   ├── index.tsx          → /blog
│   │   │   └── $slug.tsx          → /blog/:slug (dynamic)
│   │   ├── (auth)/                → Route group (no URL prefix)
│   │   │   ├── login.tsx          → /login
│   │   │   └── register.tsx       → /register
│   │   ├── (dashboard)/           → Protected route group
│   │   │   ├── __layout.tsx       → Dashboard layout + auth guard
│   │   │   ├── index.tsx          → /dashboard
│   │   │   └── settings.tsx       → /dashboard/settings
│   │   └── api/                   → API routes (optional server routes)
│   │       └── webhook.ts         → /api/webhook
│   ├── app.config.ts              → TanStack Start config (SSR, prerender)
│   ├── router.config.ts           → TanStack Router config (if separate)
│   └── server/                    → Server-side code (only runs in Worker)
│       ├── db/
│       │   ├── schema/            → Drizzle ORM table definitions
│       │   │   ├── users.ts
│       │   │   └── posts.ts
│       │   ├── queries/           → Reusable query functions
│       │   │   ├── users.ts
│       │   │   └── posts.ts
│       │   └── index.ts           → Drizzle client + DB connection
│       ├── kv/
│       │   ├── sessions.ts        → Session storage via KV
│       │   └── cache.ts           → Generic cache helpers
│       ├── r2/
│       │   ├── uploads.ts         → File upload/download logic
│       │   └── images.ts          → Image-specific operations
│       ├── auth/
│       │   ├── supabase.ts        → Supabase client initialization
│       │   ├── middleware.ts      → Auth guard for server functions
│       │   └── types.ts           → Auth-related types
│       └── utils/
│           ├── errors.ts          → Custom error classes
│           └── validation.ts      → Shared Zod schemas
├── src/
│   ├── features/                  → Feature modules (per React skill)
│   │   └── ...
│   ├── shared/
│   │   ├── ui/                    → Reusable UI components
│   │   │   └── Button/
│   │   │       ├── Button.tsx
│   │   │       └── Button.module.css
│   │   ├── lib/
│   │   │   ├── cn.ts              → Simple className merger (no tailwind-merge)
│   │   │   └── constants.ts
│   │   └── styles/
│   │       ├── globals.css        → CSS reset, custom properties (tokens)
│   │       ├── variables.css      → Design tokens (colors, spacing, fonts)
│   │       └── utils.css          → Utility classes (.sr-only, .container)
│   └── env.d.ts                   → TypeScript env types (or use cf-typegen)
├── public/                        → Static assets
│   ├── favicon.ico
│   └── robots.txt
├── wrangler.jsonc                 → Cloudflare Workers + bindings config
├── vite.config.ts                 → Vite + Cloudflare plugin
├── tsconfig.json                  → TypeScript config with path aliases
├── package.json
├── .dev.vars                      → Local secrets (gitignored)
├── .gitignore
└── drizzle.config.ts              → Drizzle Kit configuration
```

### Decision tree — Where does a new file go?

```
Is it a page/route?
  YES → app/routes/<path>.tsx (file-based routing)
  NO  → Is it server-side logic (DB, KV, R2, auth)?
          YES → app/server/<domain>/ (only runs in Worker)
          NO  → Is it a React component?
                  YES → src/features/<name>/ or src/shared/ui/
                  NO  → Is it a shared utility/constant?
                          YES → src/shared/lib/
                          NO  → Review: does it belong in client or server?
```

### Key configuration files

| File | Purpose |
|------|---------|
| `wrangler.jsonc` | Cloudflare bindings (D1, KV, R2), compatibility date, observability |
| `app.config.ts` | TanStack Start: SSR, prerender, server entry |
| `vite.config.ts` | Vite plugins: cloudflare, tanstackStart, react |
| `tsconfig.json` | Path aliases (`@/` → `src/`), strict mode |
| `drizzle.config.ts` | Drizzle Kit: schema path, migrations output, dialect + d1-http driver |
| `.dev.vars` | Local secrets for `wrangler dev` (gitignored) |

---

## 2. Setup and Scaffolding

### 2.1 Create a new project from scratch

```bash
# Create TanStack Start app pre-configured for Cloudflare Workers
npm create cloudflare@latest -- my-app --framework=tanstack-start

# Or with pnpm
pnpm create cloudflare@latest my-app --framework=tanstack-start
```

This scaffolds:
- TanStack Start with Vite
- `@cloudflare/vite-plugin` pre-configured
- `wrangler.jsonc` with sensible defaults
- File-based routing in `app/routes/`

### 2.2 Manual setup — add Cloudflare to existing TanStack Start project

```bash
# Install dependencies
npm install -D @cloudflare/vite-plugin wrangler

# Generate wrangler.jsonc (if not present)
npx wrangler init
```

**vite.config.ts:**
```typescript
import { defineConfig } from "vite"
import { tanstackStart } from "@tanstack/react-start/plugin/vite"
import { cloudflare } from "@cloudflare/vite-plugin"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [
    cloudflare({ viteEnvironment: { name: "ssr" } }),
    tanstackStart(),
    react(),
  ],
})
```

**wrangler.jsonc (minimal):**
```jsonc
{
  "$schema": "node_modules/wrangler/config-schema.json",
  "name": "my-tanstack-app",
  "compatibility_date": "2026-06-01",
  "compatibility_flags": ["nodejs_compat_v2"],
  "main": "@tanstack/react-start/server-entry",
  "observability": {
    "enabled": true
  }
}
```

**package.json scripts:**
```json
{
  "scripts": {
    "dev": "vite dev",
    "build": "vite build",
    "preview": "vite preview",
    "deploy": "npm run build && wrangler deploy",
    "cf-typegen": "wrangler types",
    "db:generate": "drizzle-kit generate",
    "db:migrate:local": "wrangler d1 execute DB --local --file=./drizzle/migrations/0000.sql",
    "db:migrate:remote": "wrangler d1 execute DB --remote --file=./drizzle/migrations/0000.sql",
    "db:studio": "drizzle-kit studio"
  }
}
```

### 2.3 Type generation for bindings

After adding bindings to `wrangler.jsonc`, generate TypeScript types:

```bash
npm run cf-typegen
```

This creates type-safe access to `env.DB`, `env.KV_STORE`, `env.MY_BUCKET`, etc.

### 2.4 Local development

```bash
# Start dev server with local Cloudflare bindings
npm run dev
# or explicitly:
npx wrangler dev
```

Wrangler automatically:
- Runs a local D1 database (SQLite)
- Simulates KV and R2 locally
- Reads secrets from `.dev.vars`

---

## 3. Routing Architecture — TanStack Router

TanStack Start uses **file-based routing** powered by TanStack Router. Every file in `app/routes/` becomes a route automatically.

### 3.1 Basic route

```tsx
// app/routes/about.tsx
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/about")({
  component: AboutPage,
})

function AboutPage() {
  return (
    <main>
      <h1>About Us</h1>
      <p>This is the about page.</p>
    </main>
  )
}
```

### 3.2 Route with loader (server-side data)

```tsx
// app/routes/blog/index.tsx
import { createFileRoute } from "@tanstack/react-router"
import { createServerFn } from "@tanstack/react-start"
import { env } from "cloudflare:workers"
import { getDB, schema } from "@/server/db"
import { eq } from "drizzle-orm"

// Server function — runs in the Worker
const getPublishedPosts = createServerFn().handler(async () => {
  const db = getDB(env)
  const posts = await db.select()
    .from(schema.posts)
    .where(eq(schema.posts.published, true))
    .orderBy(schema.posts.createdAt)
    .all()
  return posts
})

export const Route = createFileRoute("/blog/")({
  loader: () => getPublishedPosts(),
  component: BlogListPage,
})

function BlogListPage() {
  const posts = Route.useLoaderData()
  return (
    <main>
      <h1>Blog</h1>
      {posts.map(post => (
        <article key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.excerpt}</p>
        </article>
      ))}
    </main>
  )
}
```

### 3.3 Dynamic route with params

```tsx
// app/routes/blog/$slug.tsx
import { createFileRoute } from "@tanstack/react-router"
import { createServerFn } from "@tanstack/react-start"
import { env } from "cloudflare:workers"
import { getDB, schema } from "@/server/db"
import { eq } from "drizzle-orm"
import { z } from "zod"

const getPostBySlug = createServerFn()
  .inputValidator(z.string().min(1, "Slug is required"))
  .handler(async ({ data: slug }) => {
    const db = getDB(env)
    const post = await db.select()
      .from(schema.posts)
      .where(eq(schema.posts.slug, slug))
      .get()
    if (!post) throw new Error("Post not found")
    return post
  })

export const Route = createFileRoute("/blog/$slug")({
  loader: ({ params }) => getPostBySlug(params.slug),
  component: BlogPostPage,
})

function BlogPostPage() {
  const post = Route.useLoaderData()
  return (
    <article>
      <h1>{post.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: post.content }} />
    </article>
  )
}
```

### 3.4 Nested layouts

```tsx
// app/routes/__root.tsx — Root layout (OBLIGATORIO)
import { Outlet, createRootRoute } from "@tanstack/react-router"

export const Route = createRootRoute({
  component: RootLayout,
})

function RootLayout() {
  return (
    <>
      <header>My App Header</header>
      <Outlet /> {/* Child routes render here */}
      <footer>My App Footer</footer>
    </>
  )
}
```

```tsx
// app/routes/(dashboard)/__layout.tsx — Dashboard layout with auth guard
import { Outlet, createFileRoute, redirect } from "@tanstack/react-router"
import { createServerFn } from "@tanstack/react-start"
import { getSession } from "@/server/auth/middleware"

// Server function: verifica que el usuario tenga sesión activa
const requireAuth = createServerFn().handler(async () => {
  const session = await getSession()
  if (!session) {
    throw new Error("Unauthorized")
  }
  return { session }
})

export const Route = createFileRoute("/(dashboard)/__layout")({
  beforeLoad: async () => {
    try {
      const { session } = await requireAuth()
      return { session }
    } catch {
      throw redirect({ to: "/login" })
    }
  },
  component: DashboardLayout,
})

function DashboardLayout() {
  return (
    <div className="dashboard-layout">
      <aside>Dashboard Sidebar</aside>
      <main><Outlet /></main>
    </div>
  )
}
```

### 3.5 Route groups (no URL prefix)

Route groups are folders wrapped in parentheses `(group-name)/`. They **do not** affect the URL.

```
app/routes/
  (auth)/login.tsx     → /login
  (auth)/register.tsx  → /register
  (dashboard)/index.tsx → /dashboard
```

### 3.6 Not-found route

```tsx
// app/routes/__not-found.tsx
import { createFileRoute } from "@tanstack/react-router"

export const Route = createFileRoute("/__not-found")({
  component: NotFoundPage,
})

function NotFoundPage() {
  return (
    <main>
      <h1>404 — Page Not Found</h1>
      <a href="/">Go home</a>
    </main>
  )
}
```

---

## 4. Server Functions — `createServerFn`

Server functions are type-safe RPC calls from client to server. They run **inside the Cloudflare Worker** and have access to all bindings.

### 4.1 Basic server function (GET equivalent)

```typescript
// In route file or server/ module
import { createServerFn } from "@tanstack/react-start"
import { env } from "cloudflare:workers"

export const getUsers = createServerFn().handler(async () => {
  const users = await env.DB.select().from(schema.users).all()
  return users // Fully typed return
})

// Client-side usage:
// const users = await getUsers()
```

### 4.2 Server function with input validation (Zod)

```typescript
import { createServerFn } from "@tanstack/react-start"
import { z } from "zod"
import { env } from "cloudflare:workers"

const createPostSchema = z.object({
  title: z.string().min(5).max(200),
  content: z.string().min(20),
  published: z.boolean().default(false),
})

export const createPost = createServerFn({ method: "POST" })
  .inputValidator(createPostSchema)
  .handler(async ({ data }) => {
    const post = await env.DB.insert(schema.posts)
      .values({
        title: data.title,
        content: data.content,
        published: data.published,
        createdAt: Date.now(),
      })
      .returning()
      .get()
    return post
  })

// Client usage:
// const newPost = await createPost({ title: "...", content: "..." })
```

### 4.3 Accessing Cloudflare bindings (D1, KV, R2)

```typescript
import { createServerFn } from "@tanstack/react-start"
import { env } from "cloudflare:workers"

// D1
const dbResult = await env.DB.prepare("SELECT * FROM users").all()

// KV — read
const cachedData = await env.KV_STORE.get("cache-key", "json")

// KV — write
await env.KV_STORE.put("cache-key", JSON.stringify(data), { expirationTtl: 3600 })

// R2 — upload
await env.MY_BUCKET.put("file-key.txt", fileContent)

// R2 — download
const object = await env.MY_BUCKET.get("file-key.txt")
const text = await object?.text()
```

### 4.4 Error handling in server functions

```typescript
import { createServerFn } from "@tanstack/react-start"

class AppError extends Error {
  constructor(
    message: string,
    public status: number = 500,
    public code: string = "INTERNAL_ERROR"
  ) {
    super(message)
    this.name = "AppError"
  }
}

export const deletePost = createServerFn({ method: "POST" })
  .inputValidator((id: string) => id)
  .handler(async ({ data: postId }) => {
    const post = await env.DB.select()
      .from(schema.posts)
      .where(eq(schema.posts.id, postId))
      .get()

    if (!post) {
      throw new AppError("Post not found", 404, "NOT_FOUND")
    }

    // Auth check — getSession lee el token de los headers y valida contra Supabase
    const session = await getSession()
    if (!session || session.userId !== post.authorId) {
      throw new AppError("Unauthorized", 403, "UNAUTHORIZED")
    }

    await env.DB.delete(schema.posts)
      .where(eq(schema.posts.id, postId))

    return { success: true }
  })
```

### 4.5 Server function patterns summary

| Pattern | Use case |
|---------|----------|
| `createServerFn().handler(...)` | Public read operation (GET-like) |
| `createServerFn({ method: "POST" }).handler(...)` | Mutation (POST-like) |
| `.inputValidator(schema)` | Validate and type input (Zod recommended) |
| Throw custom errors | Let TanStack Start's error boundary catch them |
| `env` from `cloudflare:workers` | Access all Cloudflare bindings |

---

## 5. Database — Cloudflare D1

D1 is Cloudflare's serverless SQLite database. It runs at the edge with read replication.

### 5.1 Create a D1 database

```bash
# Create database
npx wrangler d1 create my-app-db

# This outputs the database ID — add it to wrangler.jsonc
```

**wrangler.jsonc:**
```jsonc
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-app-db",
      "database_id": "<YOUR_DB_ID>"
    }
  ]
}
```

### 5.2 Schema design with Drizzle ORM

Drizzle ORM is the recommended approach for type-safe D1 queries:

```bash
npm install drizzle-orm
npm install -D drizzle-kit @cloudflare/d1
```

**drizzle.config.ts:**
```typescript
import "dotenv/config"
import { defineConfig } from "drizzle-kit"

export default defineConfig({
  schema: "./app/server/db/schema/*.ts",
  out: "./drizzle/migrations",
  dialect: "sqlite",
  driver: "d1-http",
  dbCredentials: {
    accountId: process.env.CLOUDFLARE_ACCOUNT_ID!,
    databaseId: process.env.CLOUDFLARE_DATABASE_ID!,
    token: process.env.CLOUDFLARE_D1_TOKEN!,
  },
})
```

**app/server/db/schema/users.ts:**
```typescript
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core"

export const users = sqliteTable("users", {
  id: text("id").primaryKey(), // UUID from Supabase Auth
  email: text("email").notNull().unique(),
  name: text("name"),
  avatarUrl: text("avatar_url"),
  role: text("role", { enum: ["user", "admin"] }).default("user").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" })
    .notNull()
    .$defaultFn(() => new Date()),
  updatedAt: integer("updated_at", { mode: "timestamp" })
    .notNull()
    .$defaultFn(() => new Date()),
})
```

**app/server/db/schema/posts.ts:**
```typescript
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core"
import { users } from "./users"

export const posts = sqliteTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  slug: text("slug").notNull().unique(),
  content: text("content").notNull(),
  excerpt: text("excerpt"),
  published: integer("published", { mode: "boolean" }).default(false).notNull(),
  authorId: text("author_id")
    .notNull()
    .references(() => users.id),
  createdAt: integer("created_at", { mode: "timestamp" })
    .notNull()
    .$defaultFn(() => new Date()),
  updatedAt: integer("updated_at", { mode: "timestamp" })
    .notNull()
    .$defaultFn(() => new Date()),
})
```

### 5.3 Initialize Drizzle client for Cloudflare Workers

> **CRÍTICO:** En Cloudflare Workers, `env` solo existe dentro del contexto de una request (handler, server function). **Nunca** inicialices el cliente Drizzle a nivel de módulo. Usa una factory function que reciba `env` como parámetro.

**app/server/db/index.ts:**
```typescript
import { drizzle } from "drizzle-orm/d1"
import type { D1Database } from "@cloudflare/workers-types"
import * as schema from "./schema"

// Factory: recibe el binding D1 desde el contexto de la request
export function getDB(env: { DB: D1Database }) {
  return drizzle(env.DB, { schema })
}

export { schema }
```

**Uso dentro de una server function:**
```typescript
import { createServerFn } from "@tanstack/react-start"
import { env } from "cloudflare:workers"
import { getDB, schema } from "@/server/db"
import { eq } from "drizzle-orm"

export const getUsers = createServerFn().handler(async () => {
  const db = getDB(env) // ← env solo disponible aquí
  return db.select().from(schema.users).all()
})
```

> **Important:** On Cloudflare Workers, Drizzle's `drizzle(d1Binding, { schema })` is the correct initialization. Do NOT use `node-postgres` or `better-sqlite3` drivers — those don't work at the edge.

### 5.4 Query patterns

> Las funciones de query reciben la instancia `db` como parámetro (no como import de módulo). Usa `getDB(env)` dentro de la server function para obtenerla.

```typescript
// app/server/db/queries/posts.ts
import type { DrizzleD1Database } from "drizzle-orm/d1"
import * as schema from "../schema"
import { eq, desc, and, or, like, sql } from "drizzle-orm"

// Todas las queries reciben db como primer parámetro
export async function getPublishedPosts(
  db: DrizzleD1Database<typeof schema>,
  limit = 20,
  offset = 0
) {
  return db.select()
    .from(schema.posts)
    .where(eq(schema.posts.published, true))
    .orderBy(desc(schema.posts.createdAt))
    .limit(limit)
    .offset(offset)
    .all()
}

// Get single post by slug (with author join)
export async function getPostBySlug(
  db: DrizzleD1Database<typeof schema>,
  slug: string
) {
  return db.select()
    .from(schema.posts)
    .innerJoin(schema.users, eq(schema.posts.authorId, schema.users.id))
    .where(eq(schema.posts.slug, slug))
    .get()
}

// Create post — returns the inserted row
export async function createPost(
  db: DrizzleD1Database<typeof schema>,
  data: { id: string; title: string; slug: string; content: string; authorId: string }
) {
  return db.insert(schema.posts)
    .values(data)
    .returning()
    .get()
}

// Usage in a server function:
// import { getDB } from "@/server/db"
// import { env } from "cloudflare:workers"
//
// export const getPosts = createServerFn().handler(async () => {
//   const db = getDB(env)
//   return getPublishedPosts(db)
// })

### 5.5 Migrations

```bash
# After editing schema files, generate migration SQL
npx drizzle-kit generate

# This creates: drizzle/migrations/0000_sparkling_iron_man.sql

# Apply to local D1 (for development)
npx wrangler d1 execute DB --local --file=./drizzle/migrations/0000_sparkling_iron_man.sql

# Apply to remote D1 (for production)
npx wrangler d1 execute DB --remote --file=./drizzle/migrations/0000_sparkling_iron_man.sql
```

**In CI/CD (GitHub Actions example):**
```yaml
- name: Apply D1 migrations
  run: npx wrangler d1 execute DB --remote --file=./drizzle/migrations/0000_sparkling_iron_man.sql
  env:
    CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
    CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CF_ACCOUNT_ID }}
```

### 5.6 D1 best practices

- **Use indexes** on frequently queried columns: `slug`, `authorId`, `createdAt`
- **Keep queries selective**: D1 has a 1MB row size limit, 100KB per column
- **Use `returning()`** to get the inserted/updated row in one roundtrip
- **Prefer `all()` over `run()`** when you need results
- **Pagination is mandatory** for list endpoints — D1 pages results internally
- **Time Travel** gives you point-in-time recovery for 30 days (no manual backups needed)

---

## 6. Key-Value Storage — Workers KV

KV is an eventually consistent, globally replicated key-value store. **Read-optimized** — ideal for configuration, sessions, and caching.

### 6.1 Create a KV namespace

```bash
npx wrangler kv:namespace create "KV_STORE"
npx wrangler kv:namespace create "KV_STORE" --preview  # For preview env
```

**wrangler.jsonc:**
```jsonc
{
  "kv_namespaces": [
    {
      "binding": "KV_STORE",
      "id": "<YOUR_KV_ID>"
    }
  ]
}
```

### 6.2 KV API patterns

```typescript
import { env } from "cloudflare:workers"

// Read
const value = await env.KV_STORE.get("key")                    // string | null
const json = await env.KV_STORE.get<MyType>("key", "json")     // typed JSON
const buffer = await env.KV_STORE.get("key", "arrayBuffer")    // binary

// Write
await env.KV_STORE.put("key", "value")                          // string
await env.KV_STORE.put("key", JSON.stringify(data))             // JSON
await env.KV_STORE.put("key", "value", { expirationTtl: 3600 }) // expires in 1hr
await env.KV_STORE.put("key", "value", { expiration: 1717200000 }) // epoch

// Delete
await env.KV_STORE.delete("key")

// List keys (max 1000 per request, use cursor for pagination)
const list = await env.KV_STORE.list({ prefix: "session:", limit: 100 })

// Write multiple (atomic batch — not available yet for all plans)
await env.KV_STORE.put("key1", "value1")
await env.KV_STORE.put("key2", "value2")
```

### 6.3 Use cases

#### Session storage with Supabase JWT

```typescript
// app/server/kv/sessions.ts
import { env } from "cloudflare:workers"

const SESSION_PREFIX = "session:"
const SESSION_TTL = 60 * 60 * 24 * 7 // 7 days in seconds

export async function storeSession(userId: string, sessionData: object) {
  const key = `${SESSION_PREFIX}${userId}`
  await env.KV_STORE.put(key, JSON.stringify(sessionData), {
    expirationTtl: SESSION_TTL,
  })
}

export async function getSessionFromKV(userId: string) {
  const key = `${SESSION_PREFIX}${userId}`
  return env.KV_STORE.get(key, "json")
}

export async function deleteSessionFromKV(userId: string) {
  const key = `${SESSION_PREFIX}${userId}`
  await env.KV_STORE.delete(key)
}
```

#### Response caching

```typescript
// app/server/kv/cache.ts
import { env } from "cloudflare:workers"

const CACHE_TTL = 60 * 5 // 5 minutes

export async function getCachedOrFetch<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = CACHE_TTL
): Promise<T> {
  const cached = await env.KV_STORE.get<T>(key, "json")
  if (cached !== null) return cached

  const fresh = await fetcher()
  await env.KV_STORE.put(key, JSON.stringify(fresh), { expirationTtl: ttl })
  return fresh
}

// Usage in a server function:
export const getPopularPosts = createServerFn().handler(async () => {
  return getCachedOrFetch("popular-posts", async () => {
    return db.select().from(schema.posts).orderBy(desc(schema.posts.views)).limit(10).all()
  })
})
```

#### Rate limiting

```typescript
// app/server/kv/rate-limit.ts
import { env } from "cloudflare:workers"

export async function checkRateLimit(
  key: string,
  limit: number,
  windowSeconds: number
): Promise<boolean> {
  const count = await env.KV_STORE.get(`rate-limit:${key}`)
  const current = count ? parseInt(count, 10) : 0

  if (current >= limit) return false

  await env.KV_STORE.put(`rate-limit:${key}`, String(current + 1), {
    expirationTtl: windowSeconds,
  })
  return true
}
```

### 6.4 KV constraints and caveats

| Characteristic | Detail |
|---------------|--------|
| **Consistency** | Eventually consistent — writes may take up to 60s to propagate globally |
| **Key size** | Max 512 bytes |
| **Value size** | Max 25 MiB |
| **Write limit** | 1 write/second/key (burst to 100 writes/key for short periods) |
| **Read throughput** | Scales automatically, extremely fast |
| **List operation** | Max 1000 keys per call; use cursor for more |

### 6.5 KV vs D1 — When to use which

| Use case | Use |
|----------|-----|
| User profiles, posts, comments | **D1** (relational, queryable) |
| Session tokens, refresh tokens | **KV** (fast reads, TTL) |
| Feature flags, config | **KV** (rarely changes, read-heavy) |
| API response cache | **KV** (fast, TTL-based expiration) |
| Rate limiting counters | **KV** (simple key-value, atomic-ish) |
| Search/filter queries | **D1** (SQL WHERE, JOIN, LIKE) |
| File storage | **R2** (see Section 7) |

---

## 7. Object Storage — Cloudflare R2

R2 is S3-compatible object storage with **zero egress fees**. Use it for file uploads, images, documents, and large binary data.

### 7.1 Create an R2 bucket

```bash
npx wrangler r2 bucket create my-app-files
```

**wrangler.jsonc:**
```jsonc
{
  "r2_buckets": [
    {
      "binding": "MY_BUCKET",
      "bucket_name": "my-app-files"
    }
  ]
}
```

### 7.2 R2 API patterns

```typescript
import { env } from "cloudflare:workers"

// Upload — small file
await env.MY_BUCKET.put("path/to/file.jpg", fileContents, {
  httpMetadata: {
    contentType: "image/jpeg",
    cacheControl: "public, max-age=31536000",
  },
  customMetadata: {
    uploadedBy: userId,
    originalName: "photo.jpg",
  },
})

// Upload — with MD5 checksum verification
const hash = await crypto.subtle.digest("MD5", fileContents)
const md5 = Array.from(new Uint8Array(hash))
  .map(b => b.toString(16).padStart(2, "0"))
  .join("")

await env.MY_BUCKET.put("file.bin", fileContents, { md5 })

// Download
const object = await env.MY_BUCKET.get("path/to/file.jpg")
if (object === null) {
  // File not found
}
const body = await object.arrayBuffer() // or .text(), .blob(), .json()
const contentType = object.httpMetadata?.contentType

// Get only metadata (no body)
const head = await env.MY_BUCKET.head("path/to/file.jpg")
console.log(head?.size, head?.httpMetadata?.contentType)

// Delete
await env.MY_BUCKET.delete("path/to/file.jpg")

// List objects (with prefix and pagination)
const listed = await env.MY_BUCKET.list({
  prefix: "uploads/2024/",
  limit: 100,
  cursor: undefined, // use truncated cursor for next page
})
```

### 7.3 Public buckets and signed URLs

For publicly accessible files, enable public access on the bucket. For private files, generate **presigned URLs**:

> R2 doesn't support presigned URLs natively. For authenticated file access, route requests through a Worker or use Cloudflare's custom domain with access controls.

Alternative: serve files through a Worker route with auth:

```typescript
// app/routes/api/files/$fileId.ts
import { createFileRoute } from "@tanstack/react-router"
import { createServerFn } from "@tanstack/react-start"
import { getSession } from "@/server/auth/middleware"

export const getFile = createServerFn()
  .inputValidator((fileId: string) => fileId)
  .handler(async ({ data: fileId }) => {
    const session = await getSession()
    if (!session) throw new Error("Unauthorized")

    const object = await env.MY_BUCKET.get(`private/${session.userId}/${fileId}`)
    if (!object) throw new Error("File not found")

    return new Response(await object.arrayBuffer(), {
      headers: {
        "Content-Type": object.httpMetadata?.contentType || "application/octet-stream",
        "Cache-Control": "private, max-age=3600",
      },
    })
  })
```

### 7.4 File upload pattern from client

```typescript
// Server function for generating upload URL
export const getUploadUrl = createServerFn()
  .inputValidator(z.object({
    fileName: z.string(),
    contentType: z.string(),
    size: z.number(),
  }))
  .handler(async ({ data }) => {
    const session = await getSession()
    if (!session) throw new Error("Unauthorized")

    const fileId = crypto.randomUUID()
    const extension = data.fileName.split(".").pop()
    const key = `uploads/${session.userId}/${fileId}.${extension}`

    return { key, fileId }
  })

// Server function to perform upload (multipart for large files)
export const uploadFile = createServerFn({ method: "POST" })
  .inputValidator(z.object({
    key: z.string(),
    content: z.instanceof(ArrayBuffer).or(z.string()),
    contentType: z.string(),
  }))
  .handler(async ({ data }) => {
    await env.MY_BUCKET.put(data.key, data.content, {
      httpMetadata: { contentType: data.contentType },
    })
    return { success: true, key: data.key }
  })
```

### 7.5 CORS configuration for R2

```bash
npx wrangler r2 bucket cors add my-app-files --allowed-origins '["https://myapp.com"]' --allowed-methods '["GET","PUT"]'
```

---

## 8. Authentication — Supabase Auth

Supabase Auth handles all cryptographic operations externally, saving Cloudflare Workers CPU. The Worker only validates JWT tokens — no password hashing, no key generation.

### 8.1 Why Supabase Auth on Cloudflare Workers

| Approach | Problem on Workers |
|----------|-------------------|
| Local bcrypt/argon2 hashing | Workers have limited CPU time (10-50ms for paid, less on free) — bcrypt exceeds this |
| Local JWT generation | Web Crypto API works for JWT, but key management is complex |
| **Supabase Auth** | All crypto happens on Supabase servers; Workers only verify JWTs (fast, cheap) |

### 8.2 Install Supabase client

```bash
npm install @supabase/supabase-js
```

### 8.3 Supabase client initialization

> **CRÍTICO:** En Cloudflare Workers, `process.env` **no existe en runtime**. Las variables de entorno se acceden a través del binding `env` desde `cloudflare:workers` o mediante `wrangler secret put`.

**app/server/auth/supabase.ts:**
```typescript
import { createClient } from "@supabase/supabase-js"

// Recibe env del contexto de la request (NO usar process.env en Workers)
export function getSupabaseAdmin(env: {
  SUPABASE_URL: string
  SUPABASE_SERVICE_ROLE_KEY: string
}) {
  return createClient(
    env.SUPABASE_URL,
    env.SUPABASE_SERVICE_ROLE_KEY,
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  )
}
```

**.dev.vars:**
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOi...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOi...
```

**Set production secrets:**
```bash
npx wrangler secret put SUPABASE_URL
npx wrangler secret put SUPABASE_SERVICE_ROLE_KEY
```

### 8.4 JWT validation middleware for server functions

```typescript
// app/server/auth/middleware.ts
import { env } from "cloudflare:workers"
import { getSupabaseAdmin } from "./supabase"

export interface Session {
  userId: string
  email: string
  role: string
}

// Verify JWT and return session or null
export async function verifyJWT(token: string): Promise<Session | null> {
  try {
    const supabase = getSupabaseAdmin(env)
    const { data: { user }, error } = await supabase.auth.getUser(token)

    if (error || !user) return null

    return {
      userId: user.id,
      email: user.email!,
      role: user.role || "user",
    }
  } catch {
    return null
  }
}

// Extract token from request headers
export function extractToken(request: Request): string | null {
  const authHeader = request.headers.get("Authorization")
  if (!authHeader?.startsWith("Bearer ")) return null
  return authHeader.slice(7)
}

// Main auth guard — use this in server functions
// Reads session from KV (set during login) and verifies with Supabase
export async function getSession(): Promise<Session | null> {
  // In production, extract sessionId from cookie via getWebRequest() or similar
  // For simplicity, this shows the pattern:
  const cookieHeader = "" // get from request context
  const sessionId = extractSessionIdFromCookie(cookieHeader)
  if (!sessionId) return null

  const key = `session:${sessionId}`
  const cached = await env.KV_STORE.get<Session>(key, "json")
  if (cached) return cached

  return null
}

// Helper — extract session cookie
function extractSessionIdFromCookie(cookieHeader: string): string | null {
  const match = cookieHeader.match(/session_id=([^;]+)/)
  return match ? match[1] : null
}
```

### 8.5 Session management — KV-backed sessions

```typescript
// app/server/auth/sessions.ts
import { env } from "cloudflare:workers"
import type { Session } from "./middleware"

const SESSION_PREFIX = "session:"
const SESSION_TTL = 60 * 60 * 24 * 7 // 7 days

// Store session in KV after successful login
export async function createAuthSession(session: Session): Promise<string> {
  const sessionId = crypto.randomUUID()
  const key = `${SESSION_PREFIX}${sessionId}`

  await env.KV_STORE.put(key, JSON.stringify({
    ...session,
    createdAt: Date.now(),
  }), { expirationTtl: SESSION_TTL })

  return sessionId
}

// Retrieve session from KV (low-level, called by getSession() in middleware)
export async function getSessionFromKV(sessionId: string): Promise<Session | null> {
  const key = `${SESSION_PREFIX}${sessionId}`
  const data = await env.KV_STORE.get<Session & { createdAt: number }>(key, "json")
  if (!data) return null
  return { userId: data.userId, email: data.email, role: data.role }
}

// Delete session on logout
export async function deleteAuthSession(sessionId: string): Promise<void> {
  const key = `${SESSION_PREFIX}${sessionId}`
  await env.KV_STORE.delete(key)
}
```

### 8.6 Auth flow — Login server function

```typescript
// app/routes/(auth)/login.tsx — or app/server/auth/login.ts
import { createServerFn } from "@tanstack/react-start"
import { z } from "zod"
import { getSupabaseAdmin } from "@/server/auth/supabase"
import { createAuthSession } from "@/server/auth/sessions"

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

export const loginUser = createServerFn({ method: "POST" })
  .inputValidator(loginSchema)
  .handler(async ({ data }) => {
    const supabase = getSupabaseAdmin(env)

    // Sign in via Supabase
    const { data: authData, error } = await supabase.auth.signInWithPassword({
      email: data.email,
      password: data.password,
    })

    if (error || !authData.user) {
      throw new Error(error?.message || "Invalid credentials")
    }

    // Create KV session
    const sessionId = await createAuthSession({
      userId: authData.user.id,
      email: authData.user.email!,
      role: authData.user.user_metadata?.role || "user",
    })

    return {
      sessionId,
      user: {
        id: authData.user.id,
        email: authData.user.email,
      },
    }
  })
```

### 8.7 Client-side: use Supabase client for browser operations

```typescript
// src/shared/lib/supabase-client.ts (CLIENT SIDE ONLY)
import { createClient } from "@supabase/supabase-js"

export const supabase = createClient(
  import.meta.env.VITE_SUPABASE_URL!,
  import.meta.env.VITE_SUPABASE_ANON_KEY!
)

// Use this for:
// - supabase.auth.signUp()
// - supabase.auth.signInWithPassword()
// - supabase.auth.signInWithOAuth()
// - supabase.auth.signOut()
// - supabase.auth.onAuthStateChange() → listener for auth state
// The ANON key is safe on the client — RLS policies protect data access
```

### 8.8 Protecting routes — `beforeLoad` with KV session

```typescript
// app/routes/(dashboard)/__layout.tsx
import { createFileRoute, redirect } from "@tanstack/react-router"
import { createServerFn } from "@tanstack/react-start"
import { getSession } from "@/server/auth/middleware"

// Server function to check auth state
const checkAuth = createServerFn().handler(async () => {
  // In a real app, extract sessionId from cookie
  // For now, show the pattern:
  return { authenticated: false }
})

export const Route = createFileRoute("/(dashboard)/__layout")({
  beforeLoad: async () => {
    const { authenticated } = await checkAuth()
    if (!authenticated) {
      throw redirect({ to: "/login" })
    }
  },
  component: DashboardLayout,
})
```

---

## 9. Styling — Vanilla CSS Modules

Use CSS Modules (`.module.css`) for scoped, zero-runtime-cost styling. No Tailwind, no CSS-in-JS.

### 9.1 Design tokens — CSS custom properties

**src/shared/styles/variables.css:**
```css
:root {
  /* Colors */
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-light: #dbeafe;
  --color-background: #ffffff;
  --color-foreground: #111827;
  --color-muted: #f3f4f6;
  --color-muted-foreground: #6b7280;
  --color-border: #e5e7eb;
  --color-danger: #dc2626;
  --color-success: #16a34a;
  --color-ring: #93c5fd;

  /* Typography */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --font-size-xs: 0.75rem;
  --font-size-sm: 0.875rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.125rem;
  --font-size-xl: 1.25rem;
  --font-size-2xl: 1.5rem;
  --font-size-3xl: 1.875rem;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  --spacing-12: 3rem;

  /* Borders and radii */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);

  /* Transitions */
  --transition-colors: background-color 0.2s, border-color 0.2s, color 0.2s;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: #3b82f6;
    --color-primary-hover: #2563eb;
    --color-primary-light: #1e3a5f;
    --color-background: #0f172a;
    --color-foreground: #f1f5f9;
    --color-muted: #1e293b;
    --color-muted-foreground: #94a3b8;
    --color-border: #334155;
    --color-ring: #1d4ed8;
    --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
    --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.4);
  }
}
```

### 9.2 CSS Modules pattern

**src/shared/ui/Button/Button.module.css:**
```css
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-2);
  padding: var(--spacing-2) var(--spacing-4);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  font-weight: 500;
  font-family: var(--font-sans);
  cursor: pointer;
  transition: var(--transition-colors);
  line-height: 1.5;
}

.btn:focus-visible {
  outline: 2px solid var(--color-ring);
  outline-offset: 2px;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.primary {
  background-color: var(--color-primary);
  color: white;
}

.primary:hover:not(:disabled) {
  background-color: var(--color-primary-hover);
}

.ghost {
  background-color: transparent;
  color: var(--color-foreground);
}

.ghost:hover:not(:disabled) {
  background-color: var(--color-muted);
}

.danger {
  background-color: var(--color-danger);
  color: white;
}

.sm {
  padding: var(--spacing-1) var(--spacing-3);
  font-size: var(--font-size-xs);
}

.lg {
  padding: var(--spacing-3) var(--spacing-6);
  font-size: var(--font-size-base);
}
```

**src/shared/ui/Button/Button.tsx:**
```tsx
import { type ButtonHTMLAttributes, type ReactNode } from "react"
import styles from "./Button.module.css"

type ButtonVariant = "primary" | "ghost" | "danger"
type ButtonSize = "sm" | "md" | "lg"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant
  size?: ButtonSize
  loading?: boolean
  children: ReactNode
}

export function Button({
  variant = "primary",
  size = "md",
  loading = false,
  disabled,
  className = "",
  children,
  ...props
}: ButtonProps) {
  const classNames = [
    styles.btn,
    styles[variant],
    size !== "md" ? styles[size] : "",
    className,
  ].filter(Boolean).join(" ")

  return (
    <button
      className={classNames}
      disabled={disabled || loading}
      {...props}
    >
      {loading && <span aria-hidden="true">⏳</span>}
      {children}
    </button>
  )
}
```

### 9.3 Simple `cn()` utility (no tailwind-merge needed)

```typescript
// src/shared/lib/cn.ts
/**
 * Simple className merger.
 * No tailwind-merge needed since we use CSS Modules.
 */
export function cn(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(" ")
}
```

### 9.4 Responsive design with container queries

```css
/* FeatureCard.module.css */
.card {
  padding: var(--spacing-4);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  container-type: inline-size;
}

/* Adapt based on container width, not viewport */
@container (min-width: 400px) {
  .card {
    display: flex;
    gap: var(--spacing-4);
  }
}
```

### 9.5 Layout patterns with CSS Grid + custom properties

```css
/* Page layout */
.pageLayout {
  display: grid;
  grid-template-columns: 1fr;
  min-height: 100dvh;
}

@media (min-width: 768px) {
  .pageLayout {
    grid-template-columns: 250px 1fr;
  }
}

/* Card grid */
.cardGrid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-6);
}

/* Centered container */
.container {
  width: 100%;
  max-width: 1200px;
  margin-inline: auto;
  padding-inline: var(--spacing-4);
}

/* Stack */
.stack {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}
```

---

## 10. Deployment and Environments

### 10.1 Local development

```bash
# Full local dev with D1, KV, R2 bindings
npx wrangler dev

# Or via npm script
npm run dev
```

Wrangler automatically:
- Uses `.dev.vars` for secrets
- Creates local D1 database (SQLite file)
- Simulates KV and R2 locally
- Hot reloads on file changes

### 10.2 Preview deployment

```bash
# Deploy to preview environment
npx wrangler deploy --env preview

# Or with custom name
npx wrangler deploy --name my-app-preview
```

**wrangler.jsonc with environments:**
```jsonc
{
  "name": "my-tanstack-app",
  "env": {
    "preview": {
      "name": "my-tanstack-app-preview",
      "d1_databases": [
        {
          "binding": "DB",
          "database_name": "my-app-db-preview",
          "database_id": "<PREVIEW_DB_ID>"
        }
      ]
    },
    "production": {
      "name": "my-tanstack-app",
      "d1_databases": [
        {
          "binding": "DB",
          "database_name": "my-app-db",
          "database_id": "<PROD_DB_ID>"
        }
      ]
    }
  }
}
```

### 10.3 Production deployment

```bash
npm run deploy
# Equivalent to: npm run build && wrangler deploy
```

### 10.4 CI/CD — GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloudflare Workers

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - run: npm ci

      - name: Apply D1 migrations
        run: |
          for file in ./drizzle/migrations/*.sql; do
            npx wrangler d1 execute DB --remote --file="$file"
          done
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CF_ACCOUNT_ID }}

      - name: Deploy
        run: npm run deploy
        env:
          CLOUDFLARE_API_TOKEN: ${{ secrets.CF_API_TOKEN }}
          CLOUDFLARE_ACCOUNT_ID: ${{ secrets.CF_ACCOUNT_ID }}
```

### 10.5 Static prerendering (SSG)

For completely static pages, enable prerendering:

```typescript
// vite.config.ts
export default defineConfig({
  plugins: [
    cloudflare({ viteEnvironment: { name: "ssr" } }),
    tanstackStart({
      prerender: {
        enabled: true,
      },
    }),
    react(),
  ],
})
```

Per-route opt-in:

```tsx
// app/routes/about.tsx
export const Route = createFileRoute("/about")({
  prerender: true, // Pre-rendered at build time
  component: AboutPage,
})
```

### 10.6 Custom entrypoints (Queues, Cron, Durable Objects)

Create `app/server.ts` to add Workers features beyond HTTP:

```typescript
// app/server.ts
import handler from "@tanstack/react-start/server-entry"

// Export Durable Objects if needed
// export { MyDurableObject } from "./my-durable-object"

export default {
  fetch: handler.fetch,

  // Handle Cron Triggers
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext) {
    switch (event.cron) {
      case "*/5 * * * *":
        // Every 5 minutes — cleanup expired sessions
        console.log("Running session cleanup...")
        break
    }
  },

  // Handle Queues
  async queue(batch: MessageBatch, env: Env, ctx: ExecutionContext) {
    for (const message of batch.messages) {
      console.log("Processing queue message:", message.body)
      message.ack()
    }
  },
}
```

Update `wrangler.jsonc`:
```jsonc
{
  "main": "app/server.ts"
}
```

---

## 11. Observability and Logging

### 11.1 Built-in Cloudflare Workers observability

Enable in `wrangler.jsonc`:
```jsonc
{
  "observability": {
    "enabled": true
  }
}
```

This provides:
- Request latency metrics
- Error rates
- CPU time per request
- D1 query performance (when D1 binding is configured)

### 11.2 Structured logging

```typescript
// app/server/utils/logger.ts
interface LogEntry {
  level: "info" | "warn" | "error"
  message: string
  timestamp: string
  requestId?: string
  userId?: string
  duration?: number
  metadata?: Record<string, unknown>
}

export function log(entry: Omit<LogEntry, "timestamp">) {
  const fullEntry: LogEntry = {
    ...entry,
    timestamp: new Date().toISOString(),
  }

  // In Workers, console.log goes to wrangler tail / Cloudflare dashboard
  const logFn = entry.level === "error" ? console.error
    : entry.level === "warn" ? console.warn
    : console.log

  logFn(JSON.stringify(fullEntry))
}

// Usage in server function:
export const getPost = createServerFn()
  .handler(async ({ data: slug }) => {
    const start = Date.now()
    log({ level: "info", message: "Fetching post", metadata: { slug } })

    const post = await db.select().from(schema.posts)
      .where(eq(schema.posts.slug, slug))
      .get()

    log({
      level: "info",
      message: "Post fetched",
      duration: Date.now() - start,
      metadata: { slug, found: !!post },
    })

    return post
  })
```

### 11.3 Real-time log streaming

```bash
# Stream production logs to your terminal
npx wrangler tail
```

---

## 12. Anti-patterns and Common Mistakes

### 12.1 CRITICAL — NEVER do these

| # | Anti-pattern | Why it's wrong | Correct approach |
|---|-------------|----------------|-----------------|
| 1 | **Using Node.js crypto/bcrypt in Workers** | Exceeds CPU time limits; Worker killed mid-hash | Use Supabase Auth (external crypto) or Web Crypto API |
| 2 | **Importing `env` in client components** | `cloudflare:workers` is server-only; breaks SSR | Access bindings ONLY in server functions (`createServerFn`) |
| 3 | **Using D1 for session storage** | D1 is SQL, not optimized for key-value reads | Use Workers KV for sessions (fast, TTL support) |
| 4 | **Using KV for relational data** | KV has no queries, no joins, eventual consistency | Use D1 for any data you need to query/filter/join |
| 5 | **Storing files in D1** | D1 has row size limits, not meant for blobs | Use R2 for file storage |
| 6 | **Hardcoding secrets in wrangler.jsonc** | Committed to git, exposed | Use `.dev.vars` (local) + `wrangler secret put` (production) |
| 7 | **Skipping input validation on server functions** | Malicious input reaches your database | Always use `.inputValidator()` with Zod schemas |
| 8 | **No error handling in server functions** | Silent failures, bad UX | Always try/catch or throw typed errors; use ErrorBoundary on client |

### 12.2 HIGH severity

| # | Anti-pattern | Correct approach |
|---|-------------|-----------------|
| 9 | **Assuming KV writes are immediately visible** | KV is eventually consistent — read your own writes from same location only |
| 10 | **Using `SELECT *` without pagination on large D1 tables** | Always paginate queries: `.limit(50).offset(...)` |
| 11 | **Not running `cf-typegen` after adding bindings** | Run `npm run cf-typegen` to get TypeScript types for `env.*` |
| 12 | **Using Supabase service role key on the client** | NEVER expose the service role key; use anon key on client |
| 13 | **Not setting `httpMetadata.contentType` on R2 uploads** | Always set content type for proper browser handling |
| 14 | **Creating new Drizzle client per request** | Drizzle's `drizzle(d1, { schema })` is stateless — reuse the instance |
| 15 | **Over-fetching from D1 in a single request** | D1 charges per row read; select only columns you need |

### 12.3 MEDIUM severity

| # | Anti-pattern | Correct approach |
|---|-------------|-----------------|
| 16 | **Not using `returning()` on INSERT/UPDATE** | One less round trip to D1 |
| 17 | **Using `Date.now()` directly in schema** | Use `. $defaultFn(() => new Date())` in Drizzle |
| 18 | **Ignoring D1 read replication for global apps** | Place replicas closer to users to reduce latency |
| 19 | **Forgetting to set `Cache-Control` on static assets** | R2 objects + Worker responses should have caching headers |
| 20 | **Not using `import type` for Drizzle schema imports** | Avoids pulling schema into client bundles |

### 12.4 Cloudflare Workers specific constraints

| Constraint | Free tier | Paid tier |
|-----------|-----------|-----------|
| CPU time per request | 10 ms | 30 s (standard) |
| Request duration (wall clock) | — | 30 s |
| Memory per request | 128 MB | 128 MB |
| D1 storage | 5 GB (total) | Per GB pricing |
| D1 rows read per query | 25,000 | 25,000 |
| KV reads/day | 100,000 | Per million pricing |
| R2 storage | 10 GB | Per GB pricing |

---

## 13. Evaluation and Failure Detection

### Anti-pattern mapping table

| # | Anti-pattern | Severity | Description | Solution |
|---|-------------|----------|-------------|----------|
| 1 | **Node.js crypto in Workers** | CRITICAL | bcrypt/argon2 in Worker exceeds CPU limits | Offload to Supabase Auth |
| 2 | **Client-side env access** | CRITICAL | `cloudflare:workers` imported in browser bundle | Server functions only |
| 3 | **Supabase service key on client** | CRITICAL | Full DB access exposed to browser | Anon key + RLS policies |
| 4 | **KV for relational data** | HIGH | Cannot query, filter, or join KV data | Use D1 for structured data |
| 5 | **Unpaginated D1 queries** | HIGH | Can hit row read limits, slow responses | Always `.limit().offset()` |
| 6 | **KV consistency assumptions** | HIGH | Writes not immediately visible globally | Design for eventual consistency |
| 7 | **Missing input validation** | HIGH | SQL injection, malformed data | Zod schemas on every server function |
| 8 | **No error boundaries** | MEDIUM | Unhandled errors crash the page | ErrorBoundary per route |
| 9 | **Missing cache headers** | MEDIUM | Unnecessary D1 reads, slower responses | Cache-Control on responses |
| 10 | **R2 without content type** | MEDIUM | Browsers mishandle file downloads | Always set httpMetadata.contentType |

### Domain levels — TanStack Start + Cloudflare

#### Básico — Scaffolding y rutas

- Create a project with `npm create cloudflare`
- Define file-based routes with `createFileRoute`
- Create simple server functions with `createServerFn`
- Read from D1 using Drizzle ORM
- Deploy with `wrangler deploy`
- Use CSS Modules for styling

#### Intermedio — Integración de servicios

- Implement auth flow with Supabase + KV sessions
- Use KV for caching and rate limiting
- Upload/manage files with R2
- Design D1 schemas with relations and indexes
- Handle errors with custom error classes
- Configure environment-specific wrangler configs
- Use Drizzle migrations

#### Avanzado — Producción y optimización

- Custom server entrypoints (Queues, Cron, Durable Objects)
- Static prerendering with SSR hybrid strategy
- Multi-region D1 read replicas
- Advanced D1 query patterns (CTEs, window functions)
- Observability dashboards and alerting
- CI/CD with automated D1 migrations
- Performance profiling of server functions

### Production bottlenecks

| # | Bottleneck | Detection | Solution |
|---|-----------|-----------|----------|
| 1 | **Slow D1 queries** | wrangler tail / observability dashboard | Add indexes, optimize JOINs, paginate |
| 2 | **CPU time exceeded** | Worker error logs ("CPU time exceeded") | Offload crypto to Supabase, reduce computation |
| 3 | **KV write throttling** | KV API errors under load | Batch writes, use different key prefixes for hot spots |
| 4 | **R2 upload latency** | Large file uploads timing out | Use multipart uploads for files > 100MB |
| 5 | **Excessive D1 reads** | High D1 bill, slow page loads | Implement KV caching layer for hot queries |
| 6 | **Session KV misses** | Users logged out unexpectedly | Increase KV TTL, handle null graciously |
| 7 | **Cold starts** | High TTFB on first request after deploy | Prerender static pages, keep Worker warm |

---

## 14. Quick Reference

### CLI commands

| Command | Purpose |
|---------|---------|
| `npm create cloudflare@latest -- --framework=tanstack-start` | Scaffold new project |
| `npm run dev` | Start dev server with local bindings |
| `npm run build` | Build for production |
| `npm run deploy` | Build + deploy to Cloudflare |
| `npm run cf-typegen` | Generate TypeScript types for bindings |
| `npx wrangler d1 create <name>` | Create D1 database |
| `npx wrangler d1 execute DB --local --file=./path.sql` | Run SQL on local D1 |
| `npx wrangler d1 execute DB --remote --file=./path.sql` | Run SQL on remote D1 |
| `npx wrangler kv:namespace create <name>` | Create KV namespace |
| `npx wrangler r2 bucket create <name>` | Create R2 bucket |
| `npx wrangler secret put <KEY>` | Set production secret |
| `npx wrangler tail` | Stream production logs |
| `npx drizzle-kit generate` | Generate D1 migration from schema |
| `npx drizzle-kit studio` | Open Drizzle Studio (DB browser) |

### Bindings reference — wrangler.jsonc

```jsonc
{
  "d1_databases": [
    { "binding": "DB", "database_name": "my-db", "database_id": "xxx" }
  ],
  "kv_namespaces": [
    { "binding": "KV_STORE", "id": "xxx" }
  ],
  "r2_buckets": [
    { "binding": "MY_BUCKET", "bucket_name": "my-files" }
  ],
  "services": [
    { "binding": "AUTH_SERVICE", "service": "auth-worker" }
  ],
  "queues": {
    "producers": [
      { "binding": "MY_QUEUE", "queue": "my-queue" }
    ]
  }
}
```

### Storage decision matrix

| Question | D1 | KV | R2 |
|----------|----|----|-----|
| Need SQL queries (WHERE, JOIN, ORDER)? | ✅ | ❌ | ❌ |
| Sub-millisecond reads? | ✅ (with replicas) | ✅ | ❌ |
| Store files/images? | ❌ | ❌ (< 25MB) | ✅ |
| TTL / auto-expiration? | ❌ (manual) | ✅ | ✅ (lifecycle rules) |
| Relational data? | ✅ | ❌ | ❌ |
| Eventually consistent reads OK? | N/A (strong consistency) | ✅ | N/A |
| Global low-latency reads? | ✅ (replicas) | ✅ | ✅ |
| Write-heavy workload? | ✅ | ⚠️ (1 write/sec/key) | ✅ |
| Highest value size | 1MB (row limit) | 25MB | 5TB |
| Egress fees? | No | No | **No** (zero) |

### Architecture principles

1. **Crypto off the edge** — Supabase Auth handles hashing; Workers only verify JWTs
2. **D1 for data, KV for cache** — relational queries in D1, ephemeral/session data in KV
3. **R2 for files** — any binary data goes to R2, not D1
4. **Server functions are the API** — no separate backend; `createServerFn` IS your API
5. **Validate at the edge** — Zod schemas on every server function input
6. **Type-safe end-to-end** — Drizzle ORM + TanStack Router loader types + server function return types
7. **CSS Modules over frameworks** — zero runtime, minimal bundle, fast Worker cold starts
8. **Bindings as the bridge** — wrangler.jsonc defines what your Worker can access; `env` is the typed gateway

### Resources

- [TanStack Start Docs](https://tanstack.com/start/latest/docs/framework/react/overview)
- [Cloudflare Workers + TanStack Start Guide](https://developers.cloudflare.com/workers/framework-guides/web-apps/tanstack-start/)
- [Wrangler CLI Docs](https://developers.cloudflare.com/workers/wrangler/)
- [D1 Documentation](https://developers.cloudflare.com/d1/)
- [D1 Client API](https://developers.cloudflare.com/d1/worker-api/)
- [KV Documentation](https://developers.cloudflare.com/kv/)
- [KV API Reference](https://developers.cloudflare.com/kv/api/)
- [R2 Documentation](https://developers.cloudflare.com/r2/)
- [Supabase Auth Docs](https://supabase.com/docs/guides/auth)
- [Supabase JS Client](https://supabase.com/docs/reference/javascript/introduction)
- [Drizzle ORM Docs](https://orm.drizzle.team/docs/overview)
- [Drizzle + D1 Guide](https://orm.drizzle.team/docs/get-started/d1-new)
- [TanStack Router Docs](https://tanstack.com/router/latest/docs/framework/react/overview)
- [CSS Modules (Vite)](https://vite.dev/guide/features.html#css-modules)
- [Cloudflare Workers Limits](https://developers.cloudflare.com/workers/platform/limits/)
