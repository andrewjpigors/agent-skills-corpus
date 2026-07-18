---
name: dm-powerappscodeapp
description: Build an enterprise-grade Power Apps Code App backed by a Dataverse solution. Covers solution/publisher setup, schema creation via DataverseMCP, Model-Driven App, seed data, and Code App scaffold/deploy via PAC CLI. Use for prompts like "build a Power Apps Code App", "create Dataverse solution + immersive app".
---

## Purpose
Create a complete enterprise-grade application using:
- Dataverse Solution, including publisher and versioning discipline (Major.Minor.Date.BuildCount)
- Dataverse schema with multiple tables, columns, views, relationships and choice sets, only via Dataverse MCP
- A Model-Driven App to access the created Dataverse tables, with at least 3 views and 1 dashboard
- Power Apps Code App for immersive experiences (https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview)

Use the following Tools to achieve the goal:
- Use DataverseMCP to create tables, columns, views, relationships, and choice sets in the correct dependency order. Do not use Python SDK or any external tools for Dataverse schema management.
- Use PAC CLI to add data sources to the Code App, generating typed models and services.
- Use DataverseMCP to create immersive demo data
- Use PAC CLI for general app management (init, build, push)
- Use `pac model create --name <APP_NAME> --solution <SOLUTION_UNIQUE_NAME> --publish` to create and publish the model-driven app from CLI (no Maker portal required for creation).

**Verified PAC CLI version baseline:** 2.7.x. Command surface below assumes this version. Run `pac --version` at Step 0 and adjust if behavior differs.

This skill ensures:
- Clean ALM (Solution-first)
- No schema hallucination
- Full component lifecycle (tables → solution → app → deployment)
- Efficient auth (browser-native, no device code flow)
- Production-ready code with typed services

---

## Core Principles

1. **Solution-First ALM:** All components must live in a Power Platform Solution - use the existing preferred Solution 
2. **DataverseMCP + PAC CLI Only:** Never use Python SDK or external tools; use native PAC ecosystem
3. **Browser Auth:** Use PAC CLI for authentication
4. **Publisher:** Use the publisher prefix consistently across all schema and code artifacts; verify solution publisher before creating tables
5. **Version Discipline:** Major.Minor.Date.BuildCount (e.g., 1.0.20250412.8)
6. **Validate at Each Step:** Describe schema, query data, test integration
7. **One Canonical Naming Convention Per Run:** Pick `<prefix>_<entity>` (e.g., `dm_booking`) at Step 0 and use it everywhere — solution name, publisher prefix, table logical names, and `pac code add-data-source` arguments must agree. Do not mix prefixes mid-run.

---

## Step 0 — Environment & Context

Inputs:
- Environment URL: https://<org>.crm.dynamics.com
- Org ID: <org-id>
- Solution name (e.g., FluxTravelSolution, BackToDynamicsMinds)
- Publisher prefix (e.g., flux_)

Preconditions:
- A Developer Environment exists with Dataverse and is selected using PAC CLI
- A preferred Solution exists
- PAC CLI installed and configured, check on latest version
- PAC CLI v2.6+ authenticated (`pac auth who` must succeed)
- No device code flow triggers (reuse cached PAC auth session)

Steps: 
- Ask the User if the current environment using 'pac auth who' is correct
- If not, proceed to create a new Developer Environment and authenticate with PAC CLI
- Each new Environment needs to be assigned to an Environment Group. Ask for the Environment Group if multiple are available. 
- To use the DataverseMCP, the environment must be manually enabled. Ask the user to enable the environment for DataverseMCP and confirm before proceeding.
- If the environment is already enabled for DataverseMCP update the DataverseMCP configuration with the environment details (URL) and confirm connectivity by describing the environment.

**Lock the naming convention NOW** and reuse for the entire run:
- `PUBLISHER_PREFIX` (e.g., `dm`) — 2–8 lowercase letters, no underscore
- `PUBLISHER_NAME` (e.g., `DynamicsMinds`)
- `SOLUTION_UNIQUE_NAME` (e.g., `backtodynamicsminds`) — no spaces, lowercase
- `SOLUTION_DISPLAY_NAME` (e.g., `Back To DynamicsMinds`)
- `APP_NAME` (e.g., `BackToDMOps`)

Record these once and substitute everywhere below. **Never let placeholders like `flux_` and `dm_` co-exist in a single run.**

---

## Step 0.5 — Verify Publisher Prefix Behavior (CRITICAL)

Before any `create_table`, run a single throwaway `create_table` (or inspect an existing table the publisher owns) and `describe_table` it. Confirm:
- Logical name format is exactly `<PUBLISHER_PREFIX>_<entity>` (single underscore, single prefix).
- No double-prefix (e.g., `crcce_dm_*` indicates the DataverseMCP server is auto-injecting its own publisher; STOP and switch publishers or solutions before continuing).
- The table landed in `$SOLUTION_UNIQUE_NAME` (not the default solution).

If logical names diverge from the plan, update `schema-plan.md` with the **actual** logical names and re-derive Step 6/8 inputs from there. Never proceed with mixed prefixes.

---

## Step 1 — Design Schema (Dependency Order)

Write the schema plan to `schema-plan.md` BEFORE any create_table call. Include for each table: logical name, display name, primary column, all attribute columns (name/type/required), choice sets, lookups, views, forms. The agent re-reads this file at each step to avoid drift.

Plan table creation respecting lookups (example for time-travel booking):

1. **Root tables** (no dependencies):
   - `${PUBLISHER_PREFIX}_temporaldestination`
   - `${PUBLISHER_PREFIX}_fluxvehicle`

2. **Dependent tables** (with lookups to root):
   - `${PUBLISHER_PREFIX}_temporalaccommodation` (→ temporaldestination)
   - `${PUBLISHER_PREFIX}_travelguide` (→ temporaldestination)

3. **Junction tables** (with multiple lookups):
   - `${PUBLISHER_PREFIX}_timetravelbooking` (→ fluxvehicle, temporaldestination, temporalaccommodation)

Use lowercase, no underscores inside the entity portion of the logical name (Dataverse normalizes anyway, and consistent lowercase avoids `pac code add-data-source` mismatches).

**Why:** Creates root-first to avoid lookup resolution errors during table creation

---

## Step 2 — Create Tables + Columns + Views (DataverseMCP)

Only continue with Step 2 after fully completing Step 1 and receive approval by the user on the schema plan.
For each table (in dependency order):
- Use the DataverseMCP `create_table` tool with appropriate parameters (schema name, display name, primary column).
- **Always pass the solution unique name** so the table is added to the solution at creation time (do not rely on a later "add component" step — those are easy to forget).
- **Immediately after create_table, call `describe_table`** and assert the logical name is exactly `${PUBLISHER_PREFIX}_<entity>` with no double prefix. If it isn't, STOP and return to Step 0.5.
- Add columns with correct data types, required/optional settings, and choice sets.
- Create at least 1 main view with relevant columns and filters.
- Create at least 1 main form with key fields and sections.
- Only use DataverseMCP for all schema operations; do not use Python SDK or any external tools.

Batch where possible: group all column additions for a single table into one operation rather than one MCP call per column.

**Per-Table Requirements:**
- Primary autonumber column (logical name: flux_<entity>id)
- Required columns marked with metadata
- Choice sets pre-defined with option values
- Defaults set (e.g., IsActive = true, Status = Pending)
- Currency, datetime, email, multiline text fields where needed

Validate (gate before Step 4):
- `mcp_dataversemcp_list_tables` — confirm all tables present with the expected prefix.
- `mcp_dataversemcp_describe_table` for each — confirm columns, choices, primary column, **and capture `entitySetName` (plural) for later `@odata.bind` use**.
- Confirm solution membership via FetchXML (PAC 2.7.x does NOT have `pac solution list-components`):
  ```
  pac env fetch --xml "<fetch><entity name='solutioncomponent'><attribute name='objectid'/><attribute name='componenttype'/><filter><condition attribute='solutionid' operator='eq' value='<SOLUTION_GUID>'/></filter></entity></fetch>"
  ```
  Resolve `<SOLUTION_GUID>` first:
  ```
  pac env fetch --xml "<fetch><entity name='solution'><attribute name='solutionid'/><filter><condition attribute='uniquename' operator='eq' value='$SOLUTION_UNIQUE_NAME'/></filter></entity></fetch>"
  ```
- Persist the verified logical names AND entitySetNames to `schema-plan.md` so subsequent steps (lookups, seeding, `add-data-source`) use the *actual* names, not the planned names.

---

## Step 3 — Create the Model-Driven App 

The Purpose states the deliverable includes a Model-Driven App with ≥3 views and 1 dashboard. Create it here, before seeding, so seeded data can be visually verified in the app.

Steps (CLI-first):
```bash
pac model create \
  --name "$APP_NAME" \
  --description "<short description>" \
  --solution "$SOLUTION_UNIQUE_NAME" \
  --publish
```
Capture the returned `App ID` for later validation and Maker portal links.

The sitemap, views, dashboard, and additional pages are finished in the Maker portal app designer. Always also produce a `MODEL_DRIVEN_FINISHING.md` runbook in the project root that lists:
- Concrete sitemap groups (e.g., Operations, Catalog, Concierge) and which table pages belong to each
- ≥3 view definitions (name, filter, columns) per primary table
- 1 dashboard with ≥2 charts (group-by fields specified)
- Publish + acceptance checklist

Validate: open the app via `pac model list`, confirm sitemap, views, and dashboard render.

---

## Step 4 — Create Lookup Relationships (Solution-Aware)

Define lookup columns pointing to related tables:

```bash
# Example: Add lookup to flux_TimeTravelBooking pointing to flux_TemporalDestination
pac env fetch --xml @fetch_destinations.xml | jq '.value[].flux_destinationid'
# Then create booking with lookup OData bind: "flux_destinationid@odata.bind": "/flux_temporaldestinations(id)"
```

Ensure all relationships:
- Have correct logical names
- Are added to Solution
- Support cascading delete/update as needed

Validate relationships exist:
```bash
# Via describe_table for the lookup column
```

---

## Step 5 — Create Choice Sets (Option Sets)

Define all choice columns before tables reference them:

Example choices:
```
BookingStatus: Pending (100000000), Confirmed (100000001), Departed (100000002), Returned (100000003), Cancelled (100000004)
RiskLevel: Low (100000000), Medium (100000001), High (100000002), Extreme (100000003)
VehicleStatus: Available (100000000), InTransit (100000001), Maintenance (100000002), Retired (100000003)
```

Create via Solution XML or PAC CLI.

**Key:** Choice values must be numeric; map to TypeScript enums in service layer. the numbering must be consistent and is depending on the publisher Choice value prefix (e.g. '91968' that results on option values like 91968000000, 91968000001, etc.). 

---

## Step 6 — Seed Demo Data (DataverseMCP)

Create realistic seed data for each table using DataverseMCP `create_record`, ensuring:
- All required fields populated.
- Lookups use the correct **EntitySet (plural collection) name**, NOT the table logical name. Dataverse pluralizes irregularly (e.g., `dm_temporaldestination` → `dm_temporaldestinations`, but `dm_fluxvehicle` → `dm_fluxvehicles`, while `dm_category` → `dm_categories`). **Resolve the actual collection name via `describe_table` before binding.**
  ```
  "dm_destination@odata.bind": "/dm_temporaldestinations(<guid>)"
  ```
- Choice fields use the numeric option value (e.g., `statuscode: 100000001`).

Seed in dependency order (root → dependent → junction). After creating each parent record, capture its GUID into a local map (`seed-ids.json`) so junction records can reference them without re-querying.

Volume targets:
- 5 Destination records (minimum)
- 3+ Vehicle records
- 3+ Accommodation records (one per destination type)
- 5+ Travel Guide records (one per destination)
- 5+ Booking records (covering all statuses)

**Performance:** One MCP `create_record` call per record is acceptable at this scale (≤30 records). For larger seed sets, defer to a post-deploy script inside the Code App or a Power Automate flow rather than dozens of MCP calls.

Validate seeding via `mcp_dataversemcp_read_query` (FetchXML or OData) — confirm row counts and that lookup columns resolve to non-null related records.

---

## Step 7 — Scaffold Code App 

Initialize app from official Microsoft template:

```bash
npx degit github:microsoft/PowerAppsCodeApps/templates/vite <app-name>
cd <app-name>
npm install
npm install react-router-dom
npm install -D tailwindcss @tailwindcss/vite
```

Initialize PAC code app:
```bash
pac code init --displayname "FluxTravel"
```

Update vite.config.ts (note the correct plugin path — `@microsoft/power-apps-vite/plugin`, NOT `@microsoft/power-apps/vite`):
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { powerApps } from '@microsoft/power-apps-vite/plugin'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    powerApps(),
  ],
})
```

`pac code init` produces `power.config.json` in the project root (not `app.power.json`). Do not edit it manually unless changing display name.

---

## Step 8 — Add Dataverse Data Sources (Generated Models)

**The `-t` argument in PAC 2.7.x is the table LOGICAL NAME (singular)** — e.g., `seb_temporaldestination`, not `seb_temporaldestinations`. Passing the EntitySet (plural) name fails with `Failed to get entity definition for table '...'`. This is the opposite of `@odata.bind`, which uses plural.

Also pass `-env <env URL>` explicitly — without it, PAC sometimes resolves a stale environment and reports phantom "table not found" errors.

**Before running add-data-source, always publish customizations** so the metadata lookup endpoint sees the latest tables:
```bash
pac solution publish
```

Add each table as a data source to generate typed services:
```bash
ENV_URL="https://<org>.crm.dynamics.com"
pac code add-data-source -a dataverse -t dm_temporaldestination -env $ENV_URL
pac code add-data-source -a dataverse -t dm_fluxvehicle -env $ENV_URL
pac code add-data-source -a dataverse -t dm_temporalaccommodation -env $ENV_URL
pac code add-data-source -a dataverse -t dm_timetravelbooking -env $ENV_URL
pac code add-data-source -a dataverse -t dm_travelguide -env $ENV_URL
```

If one table errors transiently (intermittent metadata service failure), retry once with `-l verbose` after `pac solution publish`. Do not switch to plural — singular is correct.

Result:
- `src/generated/models/*.ts` — Typed entity definitions
- `src/generated/services/*.ts` — Typed CRUD services with static methods `create`, `update`, `delete`, `get`, `getAll`, `getMetadata`
- `src/generated/index.ts` — Barrel exports

**Key Rules:**
- Never manually edit generated files; regenerate if schema changes.
- `getAll()` / `get()` return `IOperationResult<T>` which wraps the payload — unwrap via `result.data` (or `result.value` for arrays in some shapes) in your service layer.

---

## Step 9 — Build Typed Service Layer

Create `src/services/dataverseService.ts` wrapping generated services. Two patterns are non-obvious and must be followed:

1. **Unwrap `IOperationResult`** — generated `getAll`/`get` return `{ data?: T, value?: T }`:
```typescript
function unwrapData<T>(result: unknown): T {
  const payload = result as { data?: T; value?: T };
  if (payload?.data !== undefined) return payload.data;
  if (payload?.value !== undefined) return payload.value;
  throw new Error('Dataverse response missing data payload.');
}
```

2. **OData lookup binds use EntitySet (plural) names** — opposite of `add-data-source`:
```typescript
const DESTINATION_SET = 'dm_temporaldestinations'; // entitySetName from describe_table
function toBind(entitySet: string, id: string): string { return `/${entitySet}(${id})`; }
```

3. **Type-safe casts at OData boundary** (the template's ESLint forbids `as any`):
```typescript
const payload = record as unknown as Omit<Dm_timetravelbookingsBase, 'dm_timetravelbookingid'>;
```

Full skeleton:
```typescript
import { Dm_temporaldestinationsService /* ... */ } from "../generated";
import type { Dm_timetravelbookingsBase } from '../generated/models/Dm_timetravelbookingsModel';

export async function getDestinations(activeOnly: boolean) {
  const result = await Dm_temporaldestinationsService.getAll({
    select: [...],
    filter: activeOnly ? 'dm_isactive eq true' : undefined,
  });
  return unwrapData<Destination[]>(result);
}
```

**Key Lesson:** Service layer provides centralized unwrapping, OData binding, type safety, and a single place to satisfy ESLint cast rules.

---

## Step 10 — Build App Architecture

Structure:

```
src/
├── App.tsx                           [Router root + outlet]
├── main.tsx                          [Entry point]
├── index.css                         [Global theme]
├── types/domain.ts                   [Domain type aliases]
├── providers/PowerProvider.tsx       [Auth context via Power Apps SDK]
├── services/dataverseService.ts      [Typed CRUD + OData binding]
├── components/
│   ├── AppShell.tsx                  [Nav + Outlet]
│   └── StatusPill.tsx                [Reusable badge/tag component]
└── pages/
    ├── Dashboard.tsx
    ├── DestinationExplorer.tsx
    ├── BookingForm.tsx               [Multi-step form if needed]
    ├── MyTravels.tsx
    ├── TemporalGuide.tsx
    └── AdminPanel.tsx
```

**Key Lesson:** Router setup first (enables app to be runnable at each phase)

```typescript
// App.tsx
<BrowserRouter>
  <Routes>
    <Route element={<AppShell />}>
      <Route path="/" element={<Dashboard />} />
      <Route path="/destinations" element={<DestinationExplorer />} />
      ...
    </Route>
  </Routes>
</BrowserRouter>
```

---

## Step 11 — Implement Pages with Data Binding

Each page pattern:

1. **Load data** on mount (useEffect + service layer)
2. **Handle loading state** (skeleton or spinner)
3. **Render list or detail** (use data)
4. **Handle CRUD actions** (create/update/delete via service)
5. **Error handling** (show user-friendly messages)

Example (Dashboard):
```typescript
const [destinations, setDestinations] = useState([])
const [loading, setLoading] = useState(true)
const [error, setError] = useState(null)

useEffect(() => {
  getDestinations(true)
    .then(setDestinations)
    .catch(err => setError(err.message))
    .finally(() => setLoading(false))
}, [])

return loading ? <Spinner /> : destinations.map(d => <Card>{d.flux_eraname}</Card>)
```

---

## Step 12 — Apply the Design System 

**Goal:** Every app delivered by this skill must look like it was built by a senior product designer, not like a default Vite template. The principles below are non-negotiable defaults; deviate only with explicit user direction.

### 12.1 Stack (install once at scaffold time)
```bash
# In the Code App project root
npm install lucide-react class-variance-authority clsx tailwind-merge framer-motion sonner
npx shadcn@latest init -d                     # accepts defaults: neutral base, CSS vars, src/components/ui
npx shadcn@latest add button card input label select textarea badge dialog \
                       dropdown-menu sheet skeleton table tabs tooltip sonner separator avatar
```
- shadcn components are **copied into `src/components/ui/`** — no runtime dependency, fully themeable, accessible (Radix under the hood).
- Use `lucide-react` as the single icon family. Never mix icon sets.
- Use `cn()` helper (from `src/lib/utils.ts` created by shadcn init) for all conditional class merges.

### 12.2 Design tokens (CSS variables, not hex literals)
All colors, radii, and shadows live in `src/index.css` as CSS variables. Components reference them via Tailwind utilities (`bg-background`, `text-foreground`, `border-border`, etc.) — **never** hardcode `bg-slate-950`/`#0a0a0f` in a component.

```css
/* src/index.css */
@import "tailwindcss";

@theme {
  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
  --font-display: "Space Grotesk", ui-sans-serif, system-ui, sans-serif;
  --radius: 0.75rem;
}

:root {
  --background: 0 0% 100%;
  --foreground: 222 47% 11%;
  --card: 0 0% 100%;
  --card-foreground: 222 47% 11%;
  --primary: 24 95% 53%;            /* one bold accent, themed per project */
  --primary-foreground: 0 0% 100%;
  --muted: 210 40% 96%;
  --muted-foreground: 215 16% 47%;
  --border: 214 32% 91%;
  --ring: 24 95% 53%;
}

.dark {
  --background: 222 47% 5%;
  --foreground: 210 40% 98%;
  --card: 222 47% 7%;
  --card-foreground: 210 40% 98%;
  --primary: 24 95% 60%;
  --primary-foreground: 222 47% 5%;
  --muted: 217 33% 12%;
  --muted-foreground: 215 20% 65%;
  --border: 217 33% 15%;
  --ring: 24 95% 60%;
}

body { @apply bg-background text-foreground font-sans antialiased; }
h1, h2, h3 { @apply font-display tracking-tight; }
```

Pick a project-appropriate **single accent hue** (set `--primary`). Examples: amber for travel/luxury, emerald for finance/ops, violet for AI/creative, sky for productivity. Never use more than one accent.

### 12.3 The 10 design principles (apply to every page)
1. **Token-first theming** — never hardcode colors. If you reach for `slate-950`, you are wrong; use `bg-background`.
2. **One accent, two neutrals** — primary + background + foreground. That's it.
3. **Fixed type scale** — `text-xs / sm / base / lg / 2xl / 4xl`. Headings always `font-display tracking-tight`.
4. **8px spacing grid** — only Tailwind's default scale; no arbitrary `mt-[13px]`.
5. **Card-first layout** — content sits inside `<Card>` with `rounded-2xl border bg-card p-6`, never naked on the page.
6. **Generous whitespace** — `p-6`/`p-8` inside cards, `gap-6`/`gap-8` between sections, `max-w-7xl mx-auto` page container.
7. **Real states** — every data view ships with: `<Skeleton>` while loading, an illustrated/iconic empty state with a CTA, and an inline error card with retry. No raw spinners, no blank screens.
8. **Micro-interactions** — `transition-colors`, `hover:` background lift on interactive cards, focus rings (`focus-visible:ring-2 ring-ring`), Framer Motion `layout` on list re-orders, Sonner toasts on mutations.
9. **Accessibility by default** — only shadcn/Radix primitives for menus, dialogs, tooltips, selects. Never roll a custom dropdown. All interactive elements keyboard-reachable with visible focus.
10. **App shell: top bar + left rail + content** — predictable: 56px top bar (brand left, search center, user menu right), 240px collapsible left rail (lucide icons + labels), main area with `<PageHeader>` (title + description + actions) above content.

### 12.4 Required component contracts
Every page implements this pattern (encode in `src/components/PageHeader.tsx`, `EmptyState.tsx`, `ErrorState.tsx`, `LoadingState.tsx`):

```tsx
export default function MyTravels() {
  const { data, loading, error, refetch } = useBookings();

  if (loading) return <LoadingState rows={5} />;
  if (error)   return <ErrorState message={error} onRetry={refetch} />;
  if (!data?.length) return <EmptyState icon={Compass} title="No travels yet" description="..." action={{ label: "Plan a journey", to: "/bookings/new" }} />;

  return (
    <div className="space-y-6">
      <PageHeader title="My Travels" description="Your itineraries across time." actions={<Button>...</Button>} />
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {data.map(b => <BookingCard key={b.id} booking={b} />)}
      </div>
    </div>
  );
}
```

### 12.5 App shell template
```tsx
// components/AppShell.tsx
export function AppShell() {
  return (
    <div className="min-h-screen bg-background">
      <TopBar />
      <div className="flex">
        <SideNav />
        <main className="flex-1 px-6 py-8 lg:px-10">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>
      <Toaster richColors position="top-right" />
    </div>
  );
}
```

### 12.6 Acceptance checklist (gate before `pac code push`)
- [ ] No hex literals or raw `slate-*`/`amber-*` in any page component (only `bg-background`, `text-primary`, etc.).
- [ ] Every page renders a real Skeleton, EmptyState, and ErrorState.
- [ ] Every mutation triggers a `toast.success` / `toast.error`.
- [ ] All menus/dialogs/selects use shadcn (Radix) primitives.
- [ ] Lighthouse a11y score ≥ 95 on the main pages.
- [ ] Dark mode toggle works (class on `<html>`) and both themes are visually polished.
- [ ] `npm run build` is clean; no `as any`, no ESLint warnings.

---

## Step 13 — Build & Test Locally

**Build:**
```bash
npm run build
# Expect: ✓ X modules transformed, ✓ built in Yms
```

**Test locally (optional):**
```bash
npm run dev
# Opens http://localhost:5173
# Verify: Router works, pages load, data binds
```

**Key Lesson:** Always test before deploy to catch TypeScript errors early

---

## Step 14 — Deploy to Power Platform

Deploy code app:
```bash
pac code push
# Output: App pushed successfully. You can play your app at https://apps.powerapps.com/play/...
```

Deploy solution (if schema updated):
```bash
pac solution pack --zipfile flux.zip
pac solution import --path flux.zip --publish-changes
```

Update solution version before import:
```xml
<Version>1.0.0.8</Version>  <!-- e.g., 5 dest + 3 veh = 8 seed records -->
```

---

## Step 15 — Validate End-to-End

Verify:
- ✅ Solution contains all tables, relationships, components
- ✅ Seed data exists and lookups resolve
- ✅ App loads in Power Apps portal
- ✅ CRUD operations work (list → detail → create → update)
- ✅ Navigation between pages works
- ✅ Error handling displays user messages

---

## Auth Strategy (Critical)

**DO:**
- Use Power Apps SDK (`@microsoft/power-apps/data`) in React context
- Auth happens automatically in browser
- No user interaction needed after initial login

**DON'T:**
- Trigger device code flow (requires 3+ browser logins)
- Use external SDKs (Python, Node.js clients)
- Assume server-side auth works (doesn't; Power Apps SDK is client-only)

```typescript
// PowerProvider.tsx
import { getContext } from "@microsoft/power-apps/app"

const context = await getContext()
const user = {
  fullName: context.user.fullName,
  userPrincipalName: context.user.userPrincipalName,
}
```

---

## Version Scheme (Solution Versioning)

Adopt: **Major.Minor.Date.BuildCount**

- **Major:** Breaking schema changes (deletions, structural changes)
- **Minor:** Additive schema (new columns, tables)
- **Date:** YYYYMMDD format for the date of the build
- **BuildCount:** Incremental builds (auto-increment on solution import)

Examples:
- `1.0.20240101.0` — Initial schema, no seed data
- `1.0.20240101.8` — Schema + 8 seed records
- `1.1.20240101.8` — New feature (minor bump) + same seed records
- `2.0.20240101.21` — Major refactor (major bump) + 21 seed records

Update in `Solution.xml`:
```xml
<Version>1.0.20240101.8</Version>
```

---

## Common Pitfalls & Solutions

| Pitfall | Solution |
|---------|----------|
| **`pac code add-data-source` fails with "Failed to get entity definition"** | (1) Use the table **logical name (singular)** for `-t`, not EntitySet plural. (2) Run `pac solution publish` first to refresh metadata. (3) Pass `-env <url>` explicitly. (4) Retry once with `-l verbose` if intermittent. |
| **Components not in solution** | Pass `solutionUniqueName` to every MCP `create_table` / column / view call. Verify via FetchXML against `solutioncomponent` (PAC 2.7.x has no `solution list-components`). |
| **Lookup `@odata.bind` 400 errors** | Use the EntitySet name (plural), not the table logical name, in the bind URL: `"dm_destination@odata.bind": "/dm_temporaldestinations(<guid>)"`. Capture `entitySetName` from `describe_table` once and centralize. |
| **Vite plugin import error** | Correct path is `@microsoft/power-apps-vite/plugin` — NOT `@microsoft/power-apps/vite`. |
| **TS error: `'FormEvent' is a type and must be imported using a type-only import`** | Vite React template enables `verbatimModuleSyntax`. Split `import { useState, FormEvent } from 'react'` into `import { useState } from 'react'; import type { FormEvent } from 'react';`. |
| **ESLint `@typescript-eslint/no-explicit-any` on OData binds** | Replace `as any` with `as unknown as Partial<Omit<X, 'id'>>`. Centralize the cast in `dataverseService.ts`. |
| **`getAll()` results appear empty** | Generated services return `IOperationResult<T>`; unwrap via `result.data` (or `.value` array form) before consumption. |
| **FetchXML `top can't be specified with paging attribute page`** | Do not use `<fetch top='1'>`. Either drop `top` and use server-side paging, or pass `--xml` without the `top` attribute. |
| **Double-prefix table names (e.g., `crcce_dm_*`)** | DataverseMCP is honoring its own publisher, not yours. STOP at Step 0.5, switch the MCP-bound publisher or solution context, do not patch around it. |
| **`pac model list-tables` requires `--connectionId`** | Use `pac model list-tables` only with a connection ID; for table discovery prefer `mcp_dataversemcp_list_tables` or `pac env fetch` against `entity`/`metadata`. |
| Device code auth friction | Use browser Power Apps SDK; reuse cached PAC session. Never ask for Device Code in any scenario |
| Incomplete data seeding | Seed roots first, capture GUIDs in `seed-ids.json`, then dependents/junctions |
| Router not wired | Wire Router early (AppShell with Outlet); test at each phase |
| Build fails on import statement | Check named vs. default exports; audit all page exports |
| Power Apps SDK only in browser | Avoid Node.js backend calls; keep all ops client-side |
---

## Output Requirements

Agent must deliver:

1. **Solution validation steps** with screenshots of validation
2. **DataverseMCP/PAC CLI actions** used (commands logged)
3. **Full source code** for all pages, services, components
4. **File listing** with directory structure
5. **Deployment URL** (live Power Apps link)
6. **Validation results** (CRUD tests, navigation tests)

---

## Lessons Learned

### Anti-Patterns (do not do)
- Do NOT call `pac code add-data-source` with a plural EntitySet name — PAC 2.7.x expects the **singular logical name**. EntitySet plural is only for `@odata.bind`.
- Do NOT seed data before the Model-Driven App exists (you lose visual validation).
- Do NOT skip `pac solution publish` before `pac code add-data-source` — stale metadata causes spurious failures.
- Do NOT use `as any` for OData binds — the template's ESLint blocks merge/lint; use `as unknown as Partial<...>`.
- Do NOT import `@microsoft/power-apps/vite` — the published package is `@microsoft/power-apps-vite/plugin`.
- Do NOT mix singular/plural prefixes (e.g., `dm_booking` plan but `crcce_dm_booking` actual) — halt at Step 0.5 and reconcile.

---

## Conclusion

This skill provides a **proven blueprint** for enterprise Power Apps Code App development:
- Solution-first ALM ensures clean deployments
- PAC CLI + DataverseMCP is faster and more reliable than external tools
- Browser auth eliminates friction
- Typed service layer enables scalability
- Version discipline enables predictable releases
