---
name: language-typescript
description: TypeScript conventions with generic guidance plus a monorepo-specific addendum.
---

# TypeScript Skill

## Purpose

This skill codifies preferred TypeScript practices based on:

- repository-enforced conventions (ESLint, tsconfig, package structure)
- recurring refactor preferences
- architecture patterns across TypeScript services and modules

Use this as the default rulebook before writing, refactoring, or reviewing TypeScript code.

## Source of Truth Hierarchy

When rules conflict, apply in this order:

1. Repository lint + compiler rules
2. Existing local pattern in the nearest module/package
3. This skill's defaults

Do not invent a new local style when an existing style is already established.

## Language and Formatting Baseline

- TypeScript strict mode is expected (`strict` family enabled).
- 2-space indentation.
- single quotes.
- no semicolons.
- trailing commas where formatter applies.
- arrow functions only; do not use `function` declarations.

## Naming Conventions

### General

- Files: kebab-case with purpose suffix where applicable.
- Classes: PascalCase with role suffix (`Service`, `Controller`, `Module`, `Repository`).
- Methods/variables: camelCase.
- Private members: camelCase, no leading underscore.

### Interfaces and Type Parameters

- Interface names start with `I` and use PascalCase.
- Generic type parameters start with `T` and are descriptive (`TItem`, `TResponse`, `TData`).

### Booleans

- Prefix booleans with intent-bearing verbs:
  - `is`, `has`, `can`, `should`, `did`, `will`, `does`, `expected`
- Prefer semantic names over ambiguous forms.

### Single-Purpose App Naming

When an app has a single domain (e.g., `lambda-image-processing`, `lambda-subscriptions`), drop the domain prefix from class names — the app scope already provides context:

- `ProcessingService` not `ImageProcessingService`
- `TransformerService` not `ImageTransformerService`
- `RepositoryService` not `ImageEntityRepository`

Keep action-descriptive words (`Processing`, `Transformer`, `Repository`) — only drop the redundant domain qualifier.

This rule does NOT apply to multi-domain apps like `apps/api/` where the domain prefix disambiguates between modules (e.g., `RoutineService` vs `ExerciseService`).

### Domain Terms

- Prefer canonical domain names over legacy/vendor names.
- Keep terms consistent across route, DTO, service, repository, entity, tests, and docs.

## File and Module Organization

- Keep folders purpose-driven and predictable within the local project conventions.
- Match the nearest existing module layout before introducing new structure.
- Prefer direct imports over unnecessary local barrels.
- Delete barrel files (`index.ts`) when all consumers already import directly from source files; a barrel with zero consumers is dead code.
- Do not create wrapper interfaces, adapter layers, or helper methods unless they reduce real complexity; each layer of indirection adds navigation cost.
- Do not create passthrough methods where a public method only packs parameters into a single-use interface to forward to a private method; merge into one method and delete the wrapper interface.
- Co-locate related types: config schema types and runtime data types consumed by the same pipeline belong in one file, not split across multiple type files with re-exports between them.
- Do not split error classes across multiple files within the same app/module when they share a common base; one `errors.ts` is sufficient.
- Do not create 1-method wrapper services around single infrastructure calls (e.g., a service that only wraps `redis.del()` or `readFile()` + YAML parse); inline into the consuming service.
- Avoid creating new files unless there is a clear structural reason.

## Types and Modeling

### interface vs type

- Use `interface` for object shapes and contracts.
- Use `type` for unions, intersections, mapped/utility aliases, and discriminators.

### Arrays

- Use `TItem[]`, not `Array<TItem>`.

### Inference

- Avoid redundant primitive annotations when inference is obvious.
- Keep explicit annotations where they improve cross-file readability.

### Return Types

- Explicit return types are preferred on public methods/functions and exported symbols.
- Keep service/controller/repository boundaries explicitly typed.

### Nullability and Optionality

- Model nullability intentionally (`T | null` when explicitly nullable).
- Use `?` for optional fields.
- In DTO Swagger metadata, reflect optional vs nullable precisely.

### `any` vs `unknown`

- Never use `any`; use `unknown` and narrow with type guards or validation (e.g., Zod `.parse()`).
- If an external API returns untyped data, receive it as `unknown` and validate before use.

### Derived Types

- Prefer `Pick`, `Omit`, `Partial`, and other utility types over manually redeclaring fields.
- When a subset of an existing type is needed, derive it: `type UserSummary = Pick<User, 'id' | 'name'>`.

### Non-null Assertions

- Acceptable for framework/ORM initialized fields (`id!`, entity fields).
- Acceptable in tests where fixture guarantees existence.
- Do not use `!` to bypass real uncertainty in application logic.

### Type Safety

- Do not widen existing domain enums or named type aliases to anonymous `string`/`number` types; use the exact existing type (e.g., `Gender`, `MeasurementSystem`, `DailyTimeCommitment`).
- Enforce interface alignment with the canonical source type (e.g., align response interface fields with `IProfile` enum-typed fields).

## API Layer Conventions (NestJS)

### Controllers

- Keep controllers thin: parse/validate/route only.
- Delegate business logic to services.
- Keep explicit return types.
- Use route semantics intentionally (GET read-only, POST mutations, etc.).
- Private controller methods that implement non-trivial business logic are a hard review failure; extract that logic into a service.

### Authentication and Authorization

Controllers must use the established guard and decorator patterns:

**Public endpoints (authenticated user):**

```typescript
@ApiTags('feature')
@Controller('feature')
@UseGuards(FirebaseAuthGuard)
@ApiBearerAuth()
export class FeatureController {
  @Get()
  public async list(@GetUser() user: IUserPayload): Promise<FeatureListResponse> {
    return this.featureService.list(user.userId)
  }
}
```

**Admin-only endpoints:**

```typescript
@ApiTags('admin')
@Controller('admin/feature')
@UseGuards(FirebaseAuthGuard, RolesGuard)
@Roles(UserRole.ADMIN)
@ApiBearerAuth()
export class FeatureAdminController { ... }
```

Key patterns:

| Decorator/Guard                 | Source            | Purpose                                                            |
| ------------------------------- | ----------------- | ------------------------------------------------------------------ |
| `@UseGuards(FirebaseAuthGuard)` | `@workspace/auth` | Validates Firebase Bearer token                                    |
| `@UseGuards(RolesGuard)`        | `@workspace/auth` | Enforces role-based access (used with `@Roles`)                    |
| `@Roles(UserRole.ADMIN)`        | `@workspace/auth` | Declares required role                                             |
| `@GetUser()`                    | `@workspace/auth` | Extracts `IUserPayload` from request (has `userId`, `uid`, `role`) |
| `@ApiBearerAuth()`              | `@nestjs/swagger` | Swagger auth metadata                                              |

### Admin/Public Controller Split

When a module needs both user-facing and admin endpoints, create two controllers in the same module:

- `<feature>.controller.ts` — public, `@Controller('feature')`, `@UseGuards(FirebaseAuthGuard)` only
- `<feature>-admin.controller.ts` — admin, `@Controller('admin/feature')`, `@UseGuards(FirebaseAuthGuard, RolesGuard)` + `@Roles(UserRole.ADMIN)`

Both registered in the module's `controllers: [FeatureController, FeatureAdminController]`.

### DTOs

- Names should describe transport role: `*QueryDto`, `*Request`, `*Response`.
- Use class-validator for request validation.
- Use class-transformer where conversion is needed.
- Swagger decorators must match runtime shape (`ApiPropertyOptional`, `nullable: true`, `isArray`, `enumName`, `type`).

### Module-Scoped Config

Do not use raw `ConfigService.get<T>('ENV_VAR')` in feature module services. The correct pattern is a validated config class registered via `ConfigModule.forFeature()` and injected with `@Inject(config.KEY)`.

Bad — raw access, no validation, duplicated across services:

```typescript
constructor(private readonly configService: ConfigService) {
  this.arn = this.configService.get<string>('LAMBDA_ARN', '')
}
```

Good — validated, typed, single source of truth:

```typescript
// config/feature.config.ts
export class FeatureConfig {
  @IsString()
  @IsOptional()
  public LAMBDA_ARN?: string
}
export const featureConfig = registerAs('featureConfig', () => load(FeatureConfig))

// feature.service.ts
constructor(@Inject(featureConfig.KEY) private readonly config: FeatureConfig) {}
```

Infrastructure-level configs from `@workspace/*` packages (e.g., `databaseConfig`, `storageConfig`, `redisConfig`) use the same `registerAs` + `load` pattern but are registered globally in the root module's `ConfigModule.forRoot({ load: [...] })`.

## Service and Repository Boundaries

### Services

- Own business rules, orchestration, and response shaping.
- Use guard clauses to reduce nesting.
- Keep method names action-oriented.

### Redis Caching Pattern

Services that cache data follow a read-through pattern:

```typescript
public async getData(id: string): Promise<TData> {
  const cacheKey = CACHE_KEYS.RESOURCE(id)
  const cached = await this.redisService.get<TData>(cacheKey)

  if (cached !== null) {
    return cached
  }

  const data = await this.repository.findById(id)
  await this.redisService.set(cacheKey, data, CACHE_TTL_SECONDS)
  return data
}
```

Cache keys are defined in `apps/api/src/shared/cache.constants.ts`. Workers and webhooks invalidate these keys after writes.

### Repositories

- Keep persistence-focused and predictable.
- Prefer typed return shapes.
- Keep API response mapping in services unless repository contract is intentionally API-oriented.
- For paginated database-backed reads, apply filtering and pagination in the database query, never in memory.
- Ensure deterministic ordering at query level before pagination (`ORDER BY` + `LIMIT/OFFSET` or cursor predicate).

## Async and Concurrency

- No floating promises.
- Use `void` for intentional fire-and-forget.
- Do not mark function `async` when it does not await.
- Use `Promise.all` for independent operations.
- Keep sequential `await` when order matters.

## Error Handling

- Prefer typed/domain-specific errors over generic `Error`.
- Convert low-level errors to stable application-facing errors at boundaries.
- Keep messages actionable and specific.

## Commenting and Documentation

- Keep code mostly self-documenting.
- Add comments only for non-obvious constraints and side-effect ordering.
- Comments explain "why", not "what". Avoid comments that restate code.
- Complex logic has explanatory comments or is broken into named steps.
- No `@ts-ignore` or `@ts-expect-error`; fix the underlying type issue instead.
- No `eslint-disable` unless there is a documented, unavoidable reason inline.

## Testing Alignment

- Use the project's shared setup helpers and factories when they exist.
- Keep assertions strict and aligned with contract.
- Keep tests deterministic and isolated.

## Architecture Principles

- Appropriate separation of concerns — no god functions, no mixed layers.
- No unnecessary coupling between modules.
- No premature abstraction — abstraction must be earned by real duplication.
- Keep service/repository/controller boundaries clean.
- No over-modularization in single-purpose apps — lambdas/workers with one pipeline should use flat module structure, not `core/` + `feature/` hierarchies.
- No 3-layer service chains where the intermediate adds no branching logic — collapse to 2 layers (orchestrator + specialized).
- No standalone helper files with functions used in exactly one place — inline as private methods.

## Code Quality Principles

1. Behavior-preserving by default.
2. Apply YAGNI: do not add features that are not needed now.
3. Prefer WET over unnecessary abstraction (Rule of Three: write it once — just write it; write it twice — notice but resist abstracting; write it a third time — now evaluate whether the cases share the same reason to change; if yes abstract, if no keep separate).
4. Keep implementations smaller: reduce real logic surface, not cosmetic one-liners/comment removal.
5. Do not extract code into one-off helpers/methods by default; only extract when it clearly reduces real complexity (including linter-driven complexity/size limits), materially improves readability with a well-defined responsibility, and has a strong likelihood of reuse.
6. Treat functions/methods with many seemingly unrelated parameters as a code smell; investigate whether responsibilities should be clarified or split by concern (without splitting for the sake of splitting).
7. Eliminate unnecessary indirection: every layer of wrapping (trivial methods, single-use wrapper interfaces, barrel files, parameter objects used at one call site) adds navigation cost; remove wrappers that do not reduce real complexity.
8. Avoid verbose data transformations: when a source structure already matches the target type, assign directly instead of copying field-by-field; field-by-field mapping is only justified when transformation, validation, or field subsetting occurs.
9. Avoid redundant work: when an expensive operation (IO, parsing, computation) has already been performed and its result is available, pass the result down instead of re-executing the operation.
10. No magic strings or numbers; extract into named constants.
11. Wrap multi-write operations in transactions.
12. No `any`; use `unknown` and narrow with type guards or validation.
13. Derive types from existing ones (`Pick`, `Omit`, `Partial`) instead of copy-pasting fields.
14. Remove dead code aggressively — unused methods/types/exports/tests/config keys/dependencies.
15. Do not keep compatibility shims unless explicitly requested.
16. Do not add backwards compatibility layers unless explicitly requested by the user. If there is strong reasoning to add backwards compatibility, pause and ask user clarification before implementing.

## Query and Data Access

- No SQL/ORM N+1 query patterns; verify query efficiency on touched paths.
- Fetch only needed columns; avoid over-fetching; paginate large result sets.
- HARD FAIL: for database-backed paginated results, perform both filtering and pagination in the database query layer; never filter/slice in memory.
- Define deterministic ordering for any user-visible list, pagination, queue, or time-sequenced processing.
- Verify supporting indexes exist for new/changed query paths (including composites matching `WHERE` + `ORDER BY`); remove redundant indexes.
- No injection-prone patterns (SQL/NoSQL/command/template); use parameterization/safe APIs.
- No multi-write operations without a transaction boundary.

## Preferred Patterns

### One-off extraction policy

- default to inline code when extracted helpers would be called only once
- extract only when one of these is true: complexity/size reduction (including lint constraints), clearly better readability with a well-defined responsibility, or likely near-term reuse
- rationale: avoid deep one-time call chains that force readers to jump across multiple functions and reduce navigability

### Inline one-call wrappers

```typescript
// ❌
const getUsers = async () => fetchData('/api/users')
const users = await getUsers()

// ✅
const users = await fetchData('/api/users')
```

### Trivial wrapper methods — inline the delegation

```typescript
// ❌ wrapper that only hardcodes one argument
private async cleanupTempFile(key: string): Promise<void> {
  await this.cleanupFile(key, 'temp file')
}
await this.cleanupTempFile(tempKey)

// ✅ call the real method directly
await this.cleanupFile(tempKey, 'temp file')
```

### Single-use parameter wrapper interfaces — use direct params

```typescript
// ❌ interface used at exactly one call site for a private method
interface IProcessInput {
  buffer: Buffer
  entityId: string
  config: IConfig
}
private async process(input: IProcessInput): Promise<void> {
  const { buffer, entityId, config } = input
  // ...
}

// ✅ direct parameters (consistent with sibling methods)
private async process(
  buffer: Buffer,
  entityId: string,
  config: IConfig,
): Promise<void> {
  // ...
}
```

### Passthrough methods — merge when public only packs params for a private method

```typescript
// ❌ public method does nothing except pack params into an object and forward
interface ITranscodeOptions {
  inputPath: string
  outputDir: string
  probeResult: IProbeResult
  presets: string[]
}
public transcode(
  inputPath: string,
  outputDir: string,
  probeResult: IProbeResult,
  presets: string[],
): Promise<IResult> {
  return this.transcodeVariants({ inputPath, outputDir, probeResult, presets })
}
private async transcodeVariants(options: ITranscodeOptions): Promise<IResult> {
  const { inputPath, outputDir, probeResult, presets } = options
  // actual logic here
}

// ✅ merge into one method; delete the wrapper interface
public async transcode(
  inputPath: string,
  outputDir: string,
  probeResult: IProbeResult,
  presets: string[],
): Promise<IResult> {
  // actual logic here (no forwarding, no wrapper interface)
}
```

### Verbose field-by-field copy — assign directly when shapes match

```typescript
// ❌ manual copy when source already matches target type
this.configs = new Map(
  Object.entries(raw.entities).map(([name, cfg]) => [
    name,
    {
      tableName: cfg.tableName,
      s3Prefix: cfg.s3Prefix,
      outputFormat: cfg.outputFormat,
      sizes: Object.fromEntries(
        Object.entries(cfg.sizes).map(([k, v]) => [
          k,
          {
            maxWidth: v.maxWidth,
            maxHeight: v.maxHeight,
          },
        ])
      ),
    },
  ])
)

// ✅ direct assignment — source shape matches IEntityImageSchema
this.configs = new Map(Object.entries(raw.entities).map(([name, cfg]) => [name, cfg]))
```

### Redundant expensive calls — pass results down

```typescript
// ❌ metadata fetched in outer method, then re-fetched on same buffer in inner
const metadata = await this.getMetadata(buffer) // outer
// ... later:
private async processOriginal(buffer: Buffer): Promise<void> {
  const metadata = await this.getMetadata(buffer) // duplicate call
}

// ✅ pass the already-computed metadata
private async processOriginal(buffer: Buffer, metadata: IMetadata): Promise<void> {
  // uses metadata directly — no duplicate IO
}
```

### No `any` — use `unknown` + narrowing

```typescript
// ❌
const data: any = await response.json()
data.name.toUpperCase()

// ✅
const data: unknown = await response.json()
const parsed = UserSchema.parse(data)
parsed.name.toUpperCase()
```

### Derive types instead of copy-pasting fields

```typescript
// ❌
interface UserSummary {
  id: string
  name: string
}

// ✅
type UserSummary = Pick<User, 'id' | 'name'>
```

### No barrel exports (except package entry files)

```typescript
// ❌ services/index.ts re-exporting siblings
export { UserService } from './user.service'
export { OrderService } from './order.service'

// ✅ import directly from source
import { UserService } from './services/user.service'
```

### Magic values → named constants

```typescript
// ❌
if (retries > 3) { ... }
const key = `cache:user:${id}`

// ✅
const MAX_RETRIES = 3
const CACHE_PREFIX_USER = 'cache:user'

if (retries > MAX_RETRIES) { ... }
const key = `${CACHE_PREFIX_USER}:${id}`
```

### Guard clause bracing (hard fail)

```typescript
// ❌ single-line return is not allowed
if (!user) return null

// ✅ always use braces + multiline
if (!user) {
  return null
}

if (!user.isActive) {
  return null
}

if (!hasPermission(user)) {
  return null
}
```

### No escape hatches

```typescript
// ❌
// @ts-ignore
// @ts-expect-error
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const data: any = value

// ✅ fix the actual problem
const data: unknown = value
if (isUser(data)) { ... }
```

## Refactor-Oriented Rules

1. Rename completely across DTOs/imports/tests/docs.
2. Preserve contracts unless behavior change is explicit.
3. Remove dead types instead of keeping compatibility stubs.
4. Do not add backwards compatibility layers unless explicitly requested by the user.
5. If there is strong reasoning to add backwards compatibility, pause and ask user clarification before implementing.
6. Keep schema/entity alignment.
7. Keep required vs optional semantics truthful across layers.
8. Remove unnecessary indirection: inline trivial wrappers, replace single-use parameter objects with direct parameters, delete unused barrels.
9. Simplify data transformations: when source and target types match structurally, assign directly instead of field-by-field copying.
10. Eliminate redundant work: pass already-computed results (metadata, validation outcomes, parsed data) to callees instead of re-computing.

## Refactor Playbooks

### Indirection reduction

- identify trivial wrapper methods that only delegate to another method with a hardcoded argument; inline the call at all call sites and remove the wrapper
- identify single-use parameter wrapper interfaces/types (an interface created only to bundle arguments for one private method call); replace with direct parameters, especially when parallel methods in the same class already use direct parameters (consistency matters)
- identify barrel files (`index.ts`) that merely re-export siblings without adding value; if all consumers already import directly from the source files, delete the barrel
- identify wrapper objects or adapter layers that pass data through without transformation; remove the layer and let consumers use the source directly
- identify passthrough methods where a public method's only job is to pack its parameters into a single-use interface and forward to a private method; merge into one method (the private method becomes the public one) and delete the wrapper interface

### Verbose transformation reduction

- when loading config, deserializing data, or mapping between layers, check whether the source shape already matches the target type
- if it does, assign directly instead of copying field-by-field; field-by-field mapping is only warranted when fields are renamed, transformed, validated, or subsetted
- watch for mapping code that expands as new fields are added but never actually transforms anything — this is a maintenance surface with no value

### Redundant work elimination

- when a method calls an expensive operation (IO, parsing, metadata extraction) and then passes the raw input to a sub-method that repeats the same operation, pass the result down instead
- common pattern: metadata/validation fetched in an outer method, then re-fetched in an inner method on the same input — add a parameter for the already-computed result

### Module flattening (single-purpose apps)

When a lambda or worker app has multiple NestJS modules (`core/`, `feature/`) but only one pipeline:

1. Identify whether the `core/` module contains any service with more than one consumer across modules.
2. If every `core/` service is consumed only by the feature module, merge all files into a single flat `module/` directory.
3. Inline standalone helper files (functions used in exactly one place) as private methods.
4. Merge thin wrapper services (1-method services around infrastructure calls like `redis.del()`, `readFile()`) into the consuming service.
5. Consolidate multiple type files into a single schema file when all types serve the same pipeline.
6. Merge multiple error files into a single `errors.ts`.
7. Drop redundant domain prefix from class names when the app scope already implies it (e.g., `ProcessingService` not `ImageProcessingService` inside `lambda-image-processing`).
8. Update the root module to a flat providers list — no sub-module imports.

### Service chain collapse

When a service chain has 3+ layers (orchestrator → intermediate → specialized) and the intermediate service adds no branching logic or independent state:

1. Identify what the intermediate service actually contributes — if it only forwards calls and aggregates results, it's a passthrough layer.
2. Move the intermediate service's logic into the orchestrator.
3. Let the orchestrator call the specialized service directly.
4. Delete the intermediate service and update module providers.

Example: `ImageProcessingService` → `ImageProcessorService` → `ImageTransformerService` collapsed to `ProcessingService` → `TransformerService` — the orchestrator now owns the full pipeline (download, validate, blurhash, resize, upload).

### Re-export and type alias cleanup

- Identify `export type { X }` re-exports where the consuming files could import directly from the source.
- Identify type files that exist solely to hold 1-2 interfaces consumed by one other file — merge into the consumer's schema file.
- When config types (e.g., `IEntityConfig`) and runtime data types (e.g., `IMediaItemData`) are consumed by the same pipeline, co-locate them in one schema file.

### Dead code removal

- remove unused methods/types/exports/tests/config keys/dependencies
- do not keep compatibility shims unless explicitly requested

### Post-change dead code verification

After removing a dependency, import, or injection from a service/module, run `codebase_find_unused_symbols` scoped to the affected module to detect methods or symbols that became dead as a side effect. Either clean them up in the same PR or log a follow-up ticket. Do not leave newly-dead code unacknowledged.

### Refactor-session unused symbol sweep

At least once during every refactor session, run `codebase_find_unused_symbols` on the touched scope (module/package or whole project, depending on blast radius). For each candidate, determine whether it is truly dead code or an exported symbol potentially used externally. If the list is large or ambiguous, dispatch task sub-agents to investigate and classify candidates before removal.

## Validation Matrix

- module-local: targeted tests + typecheck + lint
- route/contract change: endpoint integration tests + status/payload verification
- quality gate: zero ESLint errors and zero TypeScript errors

## Anti-Patterns

- compatibility shims for removed APIs
- backwards compatibility added without explicit user request
- partial domain renames
- broad lint-disable blocks with no reason
- unnecessary local barrels
- stale TODOs after refactor completion
- putting admin endpoints on the public controller
- omitting `@UseGuards(FirebaseAuthGuard)` on controller classes
- omitting `@GetUser()` when the service needs the authenticated user's ID
- magic strings or numbers; extract into named constants
- using `any` instead of `unknown` + narrowing
- `function` declarations instead of arrow functions
- `@ts-ignore` or `@ts-expect-error` instead of fixing the type issue
- copy-pasting type fields instead of deriving with `Pick`/`Omit`/`Partial`
- in-memory filtering/slicing for paginated results backed by database queries
- unnecessary indirection: trivial wrapper methods that only delegate with a hardcoded argument, single-use parameter wrapper interfaces for private methods, barrel files with no consumers, adapter layers that pass through without transforming
- verbose field-by-field data mapping when source structure already matches target type (assign directly instead)
- inconsistent parameter style across sibling methods in the same class (e.g., one method uses direct params, another uses a wrapper object for the same pattern)
- redundant expensive operations: calling the same IO/parsing/metadata operation twice on the same input when the result could be passed down
- passthrough methods: a public method whose only job is to pack its parameters into a single-use interface and forward to a private method (merge into one method)
- exported symbols with zero consumers anywhere in the project (dead exports)
- speculative properties/parameters: fields declared on error classes, config objects, or DTOs that nothing in the codebase reads (YAGNI — remove unless there is evidence of external consumption)
- multi-module hierarchies (`core/` + `feature/`) in single-purpose apps (lambdas, workers) that have only one pipeline; use a flat module structure instead
- redundant domain prefix in class names when the app scope already implies the domain (e.g., `ImageProcessingService` inside `lambda-image-processing`)
- 1-method wrapper services around infrastructure calls (`CacheInvalidationService` wrapping `redis.del()`, `ConfigLoaderService` wrapping `readFile` + YAML parse)
- standalone helper files with functions used in exactly one place; inline as private methods
- re-export type aliases that add no transformation (e.g., `export type { IBlurhashSchema }` from a file that imports it from another type file)
- 3-layer service chains (orchestrator → intermediate → specialized) where the intermediate adds no branching logic; collapse to 2 layers
- split type files for one pipeline: config types, data types, and error types for the same domain scattered across 3+ files when they could be 1-2 files
- widening existing domain enums or named type aliases to anonymous `string`/`number` types
- no single-line `if` statements (including `return`, `throw`, `continue`, `break`); always use braces and multiline blocks
- no escape hatches: no `@ts-ignore`, no `@ts-expect-error`, no `eslint-disable`, no `any`
- no SQL/ORM N+1 query patterns
- no multi-write operations without a transaction boundary
- no injection-prone patterns (SQL/NoSQL/command/template)
- no orphan imports
- no stale test names/routes/docs
- no API doc drift
- no hidden behavior changes
- no unnecessary file splits
- no unsorted user-visible lists or paginated endpoints
- no newly-dead symbols left behind after dependency removal (verify with `codebase_find_unused_symbols`)

## Monorepo-Only Addendum (Turbo/workspaces + `apps/`/`packages/`)

Apply this section only when all are true:

- the target repository is a Turbo/workspace monorepo
- the repository has an `apps/` and/or `packages/` folder at root
- TypeScript work targets code inside that monorepo repository

### Apps (Feature Modules)

Use predictable module layout:

- `dto/`
- `entities/`
- `repositories/`
- `services/`
- `<feature>.controller.ts`
- `<feature>-admin.controller.ts` (when admin endpoints exist)
- `<feature>.module.ts`
- `<feature>.enums.ts` (or shared types)
- `_tests/`

### Feature Module Wiring

```typescript
@Module({
  imports: [
    TypeOrmModule.forFeature([Entity1, Entity2]), // Entity registration
    ConfigModule.forFeature(featureConfig), // Module-scoped config (optional)
    StorageModule.forRootAsync(), // Infrastructure (when needed)
    QueueModule.forRootAsync({ queues: [QUEUES.NAME] }), // Queue (when enqueuing jobs)
    MediaModule, // Shared utility modules
    PeerModule, // Cross-module imports are normal
  ],
  controllers: [FeatureController, FeatureAdminController],
  providers: [FeatureService, FeatureRepository, AdminFeatureService],
  exports: [FeatureService, FeatureRepository], // Only what others need
})
export class FeatureModule {}
```

### Shared Types Across Apps

Some types are manually duplicated between apps (API + worker, API + webhook) with a comment:

```typescript
// This file must be identical in:
// - apps/api/src/shared/image-job.types.ts
// - apps/worker-image/src/shared/image-job.types.ts
```

When modifying shared types, update **all copies**. These live in `apps/<app>/src/shared/`.

Known duplicated type files:

- `apps/api/src/shared/image-job.types.ts` ↔ `apps/worker-image/src/shared/image-job.types.ts`
- `apps/api/src/shared/subscription-event.types.ts` ↔ `apps/webhook-revenue-cat/src/shared/subscription-event.types.ts`

### Cache Key Contracts

Cache keys defined in `apps/api/src/shared/cache.constants.ts` are referenced by:

- Worker apps (YAML config `cacheKey` values must match)
- Webhook apps (Redis key patterns in cache invalidation code must match)

When renaming cache keys, verify all three surfaces: API constants, worker YAML config, webhook invalidation code.

### Packages Exports and Imports

- Keep package public surface in `src/index.ts`.
- Barrel exports are banned everywhere else.
- Allowed exception: package entry file barrels (`packages/<name>/src/index.ts`) only.
- Prefer direct imports inside apps/modules over local barrels.

### Additional Validation

- shared package touched: package tests + workspace typecheck/lint + key downstream tests
