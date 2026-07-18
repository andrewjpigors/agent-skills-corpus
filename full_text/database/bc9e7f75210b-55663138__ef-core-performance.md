---
name: ef-core-performance
description: >
  Best practices for high-performance Entity Framework Core (EF Core 8/9): fast read
  queries AND fast writes/inserts, plus high-throughput, data-intensive apps
  (concurrency, parallel/background jobs, streaming large datasets, resiliency,
  optimistic concurrency, bulk insert). ALWAYS-ON for EF Core projects: if the codebase
  references any EF Core package (Microsoft.EntityFrameworkCore*,
  Npgsql.EntityFrameworkCore.PostgreSQL, Pomelo.EntityFrameworkCore.MySql, Oracle/MySql
  EF providers) or contains a DbContext, DbSet properties, OnModelCreating, or a
  Migrations folder, consult and apply this skill before writing, generating, reviewing,
  refactoring, or fixing ANY data-access code in that project — even when performance,
  N+1, slow SaveChanges, or bulk insert are not explicitly mentioned. All fixes must
  preserve original behavior (same output). Also use for "review my EF Core query",
  "why is this insert slow", and "scale my EF Core app".
license: MIT
---

# High-Performance EF Core (Queries + Inserts)

This skill optimizes Entity Framework Core data access for throughput and low
latency, covering the **read path** (queries), the **write path** (inserts,
updates, bulk operations), and the demands of **high-throughput, data-intensive
applications** (concurrency, parallel processing, resiliency, streaming). It
targets EF Core 8 and 9; notes call out where a feature needs a specific version.

The golden rule of EF Core performance: **EF generates SQL, and the database does
the work.** Most "EF is slow" problems are really "EF was told to do the wrong
thing." So the first move is always to *see the SQL EF actually runs*, then fix
the cause — not to reach for a bulk library or raw SQL prematurely.

## Offline & multi-agent use

This skill is fully self-contained: all guidance lives in this file and in
`references/`, so it works **with no internet access and no external tools** — read the
local files and apply them directly. For a fast lookup table and source attribution see
`references/offline-reference.md`. Operational and correctness depth (migrations,
inheritance mapping, testing, async bugs, observability, pagination, EF-version shifts,
read replicas, non-relational providers) is in `references/correctness-and-ops.md`. To
install the skill in other LLM coding agents
(Claude Code, Cursor, GitHub Copilot, Cline, Windsurf, Codex, OpenCode, Gemini CLI,
and others) and to force it on for an EF Core repo, see `references/INSTALL.md`.

## Context & token management (apply the skill cheaply)

Applying this skill should not blow up the context window or token cost. Work narrowly.

Context management:

- **Progressive disclosure.** This `SKILL.md` body is enough for almost every fix. Open
  `references/offline-reference.md` only for a fast lookup, and `references/INSTALL.md`
  only when installing — do not load all references up front.
- **Read narrowly, not the whole solution.** Detect EF Core from a single `*.csproj` /
  `Directory.Packages.props`, then open only the files in scope: the specific
  `DbContext`, the query/repository/method under review, and its entity config. Skip
  unrelated projects, generated migrations, and `*ModelSnapshot.cs` unless the task
  needs them.
- **Sample, don't dump.** When inspecting SQL or query logs, read a representative slice
  (the N+1 pattern, the one slow statement) rather than pasting the entire log.
- **Reference by path/line; don't echo large files back** into the conversation.

LLM / token management:

- **Scope to what was asked.** Fix the hot path the user named; don't silently refactor
  the whole data layer. Unsolicited rewrites cost tokens and risk behavior changes.
- **Emit targeted edits, not full-file rewrites.** Prefer minimal diffs to the lines
  that change.
- **Reuse the decision tables here** instead of re-deriving the reasoning each turn, and
  reuse facts already established this session (detected provider, tracking default)
  rather than re-checking.
- **Batch related fixes into one pass** so files aren't re-read repeatedly.
- **Report concisely:** name the practice applied, the before/after, and the
  behavior-equivalence note — skip restating unchanged code.

## Activation — apply automatically on any EF Core project

This skill is not opt-in. Before writing or changing data-access code, check whether
the project uses EF Core, and if it does, apply this skill's practices by default.

Detect EF Core by scanning for any of:

- A `*.csproj`, `Directory.Packages.props`, or `packages.config` referencing an EF
  Core package: `Microsoft.EntityFrameworkCore`, `...SqlServer`, `...Sqlite`,
  `...InMemory`, `...Cosmos`, `...Design`, `Npgsql.EntityFrameworkCore.PostgreSQL`,
  `Pomelo.EntityFrameworkCore.MySql`, `Oracle.EntityFrameworkCore`, `MySql.EntityFrameworkCore`.
- A class deriving from `DbContext`, any `DbSet<T>` property, or `using Microsoft.EntityFrameworkCore;`.
- A `Migrations/` folder, `*ModelSnapshot.cs`, or `OnModelCreating` / `IEntityTypeConfiguration<T>`.

If any of these are present, follow this skill whenever you author, generate, review,
refactor, or fix data-access code in the project — even if the user only asked for a
feature, a bug fix, or "just add this query" and never mentioned performance. When you
apply a practice from here, briefly say which one and why, so the change is reviewable.

(Triggering is ultimately a runtime heuristic, not a hard lock — this section maximizes
the chance the skill is consulted, and once consulted it governs the work.)

## Non-negotiable: fixes must preserve behavior (same output)

Every change this skill motivates is a **performance/clarity refactor, never a
behavior change.** The optimized code must produce the *same observable result* as the
original: the same rows, the same values, the same ordering, the same null/empty
handling, the same number and type of side effects (rows inserted/updated/deleted), and
the same thrown-exception contract. Speed is the only thing allowed to change.

Before proposing a fix, verify equivalence against this list:

- **Result set:** same entities/columns, same filtering, same `null` vs empty results.
- **Ordering:** preserve any `OrderBy`; if the original relied on incidental ordering,
  add an explicit `OrderBy` rather than silently changing it.
- **Duplicates/identity:** if switching to `AsNoTracking()`, use
  `AsNoTrackingWithIdentityResolution()` where the original tracking collapsed
  duplicate references, so object graphs stay identical.
- **Write effects:** an insert/update/delete refactor must affect exactly the same
  rows. `ExecuteUpdate`/`ExecuteDelete` and bulk-copy paths bypass the change tracker,
  so they skip interceptors, `SavingChanges` events, computed/generated values, and
  in-context cache updates — only use them where those were not relied upon.
- **Transactions:** keep the same atomicity. Don't split one transactional
  `SaveChanges` into several statements that could partially apply.
- **Concurrency:** preserve concurrency-token checks; don't drop optimistic-concurrency
  behavior in the name of speed.

If a faster approach *would* change any of the above, do NOT apply it silently. Either
keep behavior identical, or call out the exact difference and let the user opt in. When
practical, confirm equivalence by comparing the generated SQL and/or running the
existing tests before and after.

## When to use

- Queries are slow, return too much data, or emit far more SQL statements than expected.
- N+1 query patterns appear in logs (one query, then one more per row).
- `SaveChanges` / `SaveChangesAsync` is slow when inserting or updating many rows.
- The user needs to import / seed / bulk-insert thousands+ of rows.
- Database CPU/IO or app memory is high and EF Core is in the path.
- The app runs under high concurrency / load: parallel or background data jobs,
  connection-pool exhaustion, transient/deadlock failures, or concurrency conflicts.
- The user asks to review or refactor EF Core repository / query / persistence code.

## When NOT to use

- The code uses Dapper, raw ADO.NET, or another ORM (not EF Core).
- The bottleneck is purely database-side schema (missing indexes, bad data types,
  lock contention) with no EF-side fix — diagnose, then hand off to DBA work.
- The user wants help *designing the schema/model* from scratch with no perf angle.

## Step 0 — Always measure first: see the real SQL

Never optimize blind. Turn on query logging and read what EF emits.

```csharp
optionsBuilder
    .UseSqlServer(connectionString)              // or .UseNpgsql(...)
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging()                // shows parameter values — DEV ONLY
    .EnableDetailedErrors();                      // DEV ONLY
```

Or via `appsettings.json`:

```json
{ "Logging": { "LogLevel": {
    "Microsoft.EntityFrameworkCore.Database.Command": "Information"
} } }
```

What to look for: a loop of nearly identical `SELECT`s (N+1), one giant
cartesian `JOIN` returning duplicated rows, `SELECT *` when only two columns are
needed, or a "client evaluation" warning meaning EF pulled data into memory to
filter it in C#. For production diagnosis prefer EF interceptors, `dotnet-trace`,
or the database's own query store rather than `EnableSensitiveDataLogging`.

---

# Part A — Fast queries (the read path)

### A1. Kill N+1 — the single biggest EF Core query killer

N+1 happens when related data is loaded one parent at a time inside a loop
(classic with lazy loading enabled).

```csharp
// BAD: 1 query for orders + N queries (one per order) for items
var orders = await db.Orders.ToListAsync();
foreach (var o in orders)
    total += o.Items.Count;          // each access hits the DB
```

Fix it by telling EF what you need up front:

```csharp
// Option 1 — Include (one JOIN). Good for a single, small related set.
var orders = await db.Orders.Include(o => o.Items).ToListAsync();

// Option 2 — Split query. Avoids cartesian explosion across multiple/large Includes.
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Payments)
    .AsSplitQuery()
    .ToListAsync();

// Option 3 — Projection (BEST when you don't need full entities). Fetches only
// the columns you use, no tracking, no extra rows.
var summaries = await db.Orders
    .Select(o => new OrderSummary {
        OrderId   = o.Id,
        Total     = o.Items.Sum(i => i.Price),
        ItemCount = o.Items.Count
    })
    .ToListAsync();
```

**Single vs split query — pick by data shape:**

| Scenario | Use |
| --- | --- |
| One `Include`, small child set | Single query (default) |
| Multiple `Include`s (cartesian risk) | `AsSplitQuery()` |
| `Include` of a large child collection | `AsSplitQuery()` |
| Need a consistent snapshot in one transaction | Single query |

Split queries run several round-trips, so without an explicit transaction the
child rows can drift if the data changes between them — choose single query when
consistency matters more than the cartesian cost.

### A2. Use `AsNoTracking()` for read-only queries

Change tracking exists so EF can detect edits for `SaveChanges`. If you are only
displaying data, that bookkeeping is pure overhead (memory + CPU).

```csharp
var products = await db.Products
    .AsNoTracking()
    .Where(p => p.IsActive)
    .ToListAsync();
```

For read-heavy apps, make it the default and opt back in only where you write:

```csharp
services.AddDbContext<AppDbContext>(o => o
    .UseSqlServer(cs)
    .UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking));
```

Use `AsNoTrackingWithIdentityResolution()` when a no-tracking query can return the
same entity multiple times (e.g. many parents sharing one child) and you want a
single in-memory instance instead of duplicates.

Note: projecting to a DTO with `Select` is already effectively untracked for the
projected shape, so `AsNoTracking()` adds little on top of a pure projection.

### A3. Project to exactly what you need

Pulling whole entities to use two fields wastes I/O, memory, and tracking. Shape
the query to the DTO/view model. This also sidesteps over-fetching wide tables
and large columns (e.g. `varchar(max)`, blobs) you never display.

### A4. Compile queries on hot paths

For queries executed very frequently with the same shape, cache the compiled
plan to skip EF's per-call expression compilation.

```csharp
private static readonly Func<AppDbContext, int, Task<Order?>> GetOrderById =
    EF.CompileAsyncQuery((AppDbContext db, int id) =>
        db.Orders.Include(o => o.Items).FirstOrDefault(o => o.Id == id));

var order = await GetOrderById(db, orderId);
```

### A5. Common query traps

| Trap | Problem | Fix |
| --- | --- | --- |
| `ToList()` then `Where()` in memory | Loads the whole table | Filter first: `.Where(...).ToListAsync()` |
| `Count() > 0` to test existence | Counts every row | `await q.AnyAsync()` |
| `.Select(...)` after `.Include(...)` | Include is ignored once you project | Drop the Include; project the related data directly |
| `.ToList()` inside a `Select` | Triggers nested per-row queries | Keep projecting with `Select` all the way down |
| Non-translatable method in `Where` | Falls back to client evaluation | Use `EF.Functions.Like(...)`, or rework the predicate |
| Unbounded result set | Memory blowup, slow first byte | Page with `.Skip()/.Take()`, or stream with `AsAsyncEnumerable()` |
| `OFFSET` paging deep into a table | Slow on large offsets | Prefer keyset/seek paging on an indexed sort key |

### A6. Drop to raw SQL when LINQ can't express it well

```csharp
var rows = await db.Orders
    .FromSqlInterpolated($@"
        SELECT o.* FROM Orders o
        JOIN (SELECT OrderId, SUM(Price) Total FROM OrderItems
              GROUP BY OrderId HAVING SUM(Price) > {minTotal}) t
          ON o.Id = t.OrderId")
    .AsNoTracking()
    .ToListAsync();
```

Use `FromSqlInterpolated` / `FromSql` (parameterized) — **never** build SQL by
string-concatenating user input into `FromSqlRaw`; that is a SQL-injection hole.

### A7. Project on the way *in* too — DTOs as a security boundary

Projection isn't only a read optimization; for writes it's a safety boundary. Binding
an HTTP request body straight onto an EF entity (`TryUpdateModel`/auto-mapping the whole
entity) is **over-posting / mass assignment**: a caller can set fields they shouldn't,
e.g. `IsAdmin`, `Balance`, `OwnerId`, or a foreign key. Accept a request DTO with only
the fields a client may set, then copy those explicitly onto the entity. This also keeps
sensitive/PII columns out of read payloads — project entities to response DTOs rather
than serializing entities directly. Treat "what the client can read/write" as a
deliberate, narrow mapping in both directions.

---

# Part B — Fast inserts and bulk writes (the write path)

EF Core's tracker is built for *correctness of small unit-of-work changes*, not
for shoveling 100k rows. Insert performance falls off a cliff when people fight
that design. Escalate through these tiers — only go further when a tier is too slow.

### B1. Tier 1 — Batch with one `SaveChanges`, not one per row

The most common insert mistake is saving inside the loop.

```csharp
// BAD: N round-trips, tracker churns on every save
foreach (var dto in dtos) {
    db.Customers.Add(new Customer { Name = dto.Name });
    await db.SaveChangesAsync();      // <-- inside the loop
}

// GOOD: stage everything, save once. EF batches the INSERTs automatically.
db.Customers.AddRange(dtos.Select(d => new Customer { Name = d.Name }));
await db.SaveChangesAsync();          // one call, batched statements
```

`AddRange` + a single `SaveChanges` lets EF group inserts into batched commands
(SQL Server defaults to batching many rows per round-trip; the batch size is
provider-tunable via `MaxBatchSize`). This alone fixes most "insert is slow" cases
up to a few thousand rows.

### B2. Tier 2 — Turn off the tracker's per-add cost for large batches

When adding many entities in one context, `DetectChanges` can run repeatedly and
dominate CPU. For a bounded bulk operation, disable auto-detect, add everything,
then save:

```csharp
db.ChangeTracker.AutoDetectChangesEnabled = false;
try {
    db.Customers.AddRange(bigList);   // no per-add change scan
    await db.SaveChangesAsync();
}
finally {
    db.ChangeTracker.AutoDetectChangesEnabled = true;
}
```

Also: **use a fresh, short-lived DbContext for a big import** and don't let one
context accumulate hundreds of thousands of tracked entities — tracking state grows
and slows down. For very large jobs, chunk the input (e.g. 5k–10k rows), and
either clear the context (`db.ChangeTracker.Clear()`) or new up a context per chunk.

### B3. Tier 3 — Set-based updates/deletes without loading rows (EF Core 7+)

To change or remove many rows, do **not** load them into memory just to modify and
save. Use `ExecuteUpdate` / `ExecuteDelete`, which emit a single set-based SQL
`UPDATE`/`DELETE` and bypass the tracker entirely.

```csharp
// One UPDATE statement, no entities loaded
await db.Orders
    .Where(o => o.Status == OrderStatus.Pending && o.CreatedUtc < cutoff)
    .ExecuteUpdateAsync(s => s
        .SetProperty(o => o.Status,      OrderStatus.Expired)
        .SetProperty(o => o.UpdatedUtc,  DateTime.UtcNow));

// One DELETE statement
await db.AuditLogs
    .Where(a => a.CreatedUtc < retentionCutoff)
    .ExecuteDeleteAsync();
```

Caveat: these run immediately and outside `SaveChanges`, so they don't fire
`SaveChanges` interceptors/`SavingChanges` events and won't update entities already
tracked in the current context. Wrap in an explicit transaction if you combine them
with other writes.

### B4. Tier 4 — True bulk insert for very large volumes

EF's batched INSERTs are fine into the low thousands, but for tens of thousands to
millions of rows, use a bulk-copy path. EF Core has **no built-in `BulkInsert`**;
choose one of:

- **A maintained bulk-extensions library** (e.g. community `EFCore.BulkExtensions`
  for SQL Server/PostgreSQL/SQLite, or a provider-specific bulk package). These add
  `BulkInsert`/`BulkUpdate`/`BulkMerge` that use the database's fast path. Vet the
  library's license and maintenance before adding it to a project.
- **The provider's native bulk API directly**, which is the fastest and
  dependency-light option:
  - SQL Server: `SqlBulkCopy` (stream a `DataTable`/`IDataReader`).
  - PostgreSQL: Npgsql binary `COPY` (`BeginBinaryImport`).

```csharp
// SQL Server native bulk copy — fastest path for huge inserts
using var bulk = new SqlBulkCopy(connectionString) {
    DestinationTableName = "Customers",
    BatchSize = 10_000
};
bulk.ColumnMappings.Add(nameof(Customer.Name), "Name");
await bulk.WriteToServerAsync(dataReader);
```

These bypass EF's tracking, validation, and value generation, so generated keys,
shadow properties, and concurrency tokens are your responsibility. Use them for
ingestion/seeding/ETL, not for ordinary domain writes.

### B5. Insert decision guide

| Volume / situation | Recommended approach |
| --- | --- |
| A handful of rows | `Add`/`AddRange` + one `SaveChangesAsync` |
| Hundreds–low thousands | `AddRange` + one `SaveChanges` (let EF batch) |
| Thousands, tracker is the cost | Disable `AutoDetectChangesEnabled`, chunk, fresh context |
| Bulk modify/remove existing rows | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| Tens of thousands → millions | `SqlBulkCopy` / Npgsql `COPY` / bulk-extensions library |

---

# Part C — Context & connection hygiene (helps reads and writes)

- **DbContext lifetime is short and scoped.** Register with `AddDbContext`
  (per-request/scoped). Never share one context across threads or cache it for the
  app lifetime — `DbContext` is not thread-safe and accumulates tracked state.
- **Pool contexts on hot paths.** `AddDbContextPool<T>(...)` reuses context
  instances to cut per-request allocation/setup. Don't store request state in the
  context if you pool it.
- **Always use the async APIs** (`ToListAsync`, `SaveChangesAsync`, etc.) in
  server apps so threads aren't blocked on I/O.
- **Index for the query, not the table.** EF won't add the index your `Where`/
  `OrderBy`/join needs — confirm covering indexes exist on the columns you filter
  and sort by. Configure with `HasIndex(...)` and verify in migrations.
- **Use the right key/value-generation strategy** for high-insert tables. Default
  identity columns serialize on insert hotspots less than some alternatives; for
  distributed inserts consider sequential GUIDs or HiLo to reduce index
  fragmentation and contention.

---

# Part D — High-throughput, data-intensive applications

When an EF Core app serves heavy concurrent load or churns through large datasets,
the bottleneck shifts from "one slow query" to *resiliency, concurrency, and
keeping the connection pool healthy*. Apply these on top of Parts A–C.

### D1. Connection resiliency — survive transient faults under load

Cloud/managed databases drop connections, throttle, and time out far more often
under load. Enable the retrying execution strategy so transient failures auto-retry
with backoff instead of bubbling up as errors.

```csharp
services.AddDbContext<AppDbContext>(o => o
    .UseSqlServer(cs, sql => sql.EnableRetryOnFailure(
        maxRetryCount: 5,
        maxRetryDelay: TimeSpan.FromSeconds(10),
        errorNumbersToAdd: null)));   // Npgsql: o.UseNpgsql(cs, n => n.EnableRetryOnFailure())
```

Gotcha: a retrying strategy **cannot** wrap a user-initiated transaction implicitly,
because a retry must re-run the *entire* unit. When you open an explicit transaction,
run it inside the strategy so the whole block is retried atomically:

```csharp
var strategy = db.Database.CreateExecutionStrategy();
await strategy.ExecuteAsync(async () =>
{
    await using var tx = await db.Database.BeginTransactionAsync();
    // ... multiple SaveChanges / ExecuteUpdate calls ...
    await tx.CommitAsync();
});
```

### D2. DbContext is not thread-safe — use a pooled factory for parallel work

One `DbContext` instance must never be touched by two operations concurrently
(you'll get corruption or `InvalidOperationException`). For parallel/background
processing, give each unit its own context from a **pooled factory**:

```csharp
services.AddPooledDbContextFactory<AppDbContext>(o => o.UseSqlServer(cs));

// In a parallel worker / channel consumer:
await Parallel.ForEachAsync(batches, async (batch, ct) =>
{
    await using var db = await factory.CreateDbContextAsync(ct);
    db.Items.AddRange(batch);
    await db.SaveChangesAsync(ct);
});
```

Pooling reuses context instances to cut per-operation allocation and setup —
valuable on hot request paths. Don't stash per-request mutable state on a pooled
context, and bound your parallelism: too many concurrent contexts will exhaust the
ADO.NET connection pool (default Max Pool Size is 100 on SQL Server). Tune
`Max Pool Size` in the connection string and watch for pool-timeout errors.

### D3. Stream large result sets — don't buffer millions of rows

`ToListAsync()` materializes everything into memory at once. For large reads
(reports, ETL, exports), stream row-by-row so memory stays flat:

```csharp
await foreach (var row in db.Orders.AsNoTracking()
                              .Where(o => o.CreatedUtc >= from)
                              .AsAsyncEnumerable()
                              .WithCancellation(ct))
{
    await ProcessAsync(row);   // one row in flight, not the whole table
}
```

Combine with `AsNoTracking()` (or projection) so the tracker doesn't accumulate
state across the stream. For chunked writes during a stream, flush every N rows
and `ChangeTracker.Clear()` (or use a fresh context per chunk).

### D4. Compiled models — cut cold-start cost for large schemas

Apps with hundreds of entity types pay a noticeable model-building cost on first
use (slow cold starts, painful in serverless/autoscaled tiers). Pre-compile the
model so startup skips that work:

```bash
dotnet ef dbcontext optimize --output-dir Compiled --namespace MyApp.Compiled
```

```csharp
optionsBuilder.UseModel(MyApp.Compiled.AppDbContextModel.Instance);
```

Regenerate the compiled model whenever the entity model changes (wire it into the
build). Small models barely benefit — this pays off at scale.

### D5. Handle optimistic concurrency under contention

When many writers hit the same rows, use a concurrency token (`rowversion` /
`xmin` on PostgreSQL) so last-write-wins corruption is caught instead of silently
overwriting. Configure the token, then handle the conflict with a retry/merge loop:

```csharp
// Model: builder.Property(o => o.RowVersion).IsRowVersion();
for (var attempt = 0; attempt < 3; attempt++)
{
    try { await db.SaveChangesAsync(); break; }
    catch (DbUpdateConcurrencyException ex)
    {
        foreach (var entry in ex.Entries)
        {
            var current = await entry.GetDatabaseValuesAsync();
            if (current is null) { /* row deleted — decide policy */ }
            else entry.OriginalValues.SetValues(current);   // reload + reapply, then loop
        }
    }
}
```

For write-heavy hotspots, also consider set-based `ExecuteUpdate` (Part B3) which
sidesteps load-then-save races entirely.

### D6. Timeouts, cancellation, and isolation

- **Pass a `CancellationToken` to every async EF call** so overloaded requests can
  be shed instead of piling up and exhausting the pool.
- **Set a command timeout** for legitimately long operations:
  `db.Database.SetCommandTimeout(TimeSpan.FromMinutes(2));` — but prefer fixing the
  query over raising timeouts.
- **Pick an isolation level deliberately** for hot tables. Lower isolation (e.g.
  SQL Server read-committed snapshot / `READ COMMITTED SNAPSHOT`) reduces reader↔
  writer blocking under load; specify it on explicit transactions when needed.
- **Tune batch size** for large writes via `o.UseSqlServer(cs, s => s.MaxBatchSize(...))`
  when the default round-trip batching isn't optimal for your row width.

### D7. Caching — EF Core has no second-level cache

EF Core caches *compiled query plans*, not *results*. Repeatedly hitting the
database for the same rarely-changing data is a common scale bottleneck. Options:
distributed cache (`IDistributedCache`/Redis) in front of read queries you control,
or a maintained second-level-cache library. Cache only safely-stale data, and have
an explicit invalidation story — a stale cache under load is worse than a slow query.

---

# Part E — Correctness & operations (load the reference when relevant)

Fast but wrong is still wrong, and a fast query path can be undone by a bad migration
or a test that can't catch regressions. When the task touches any of the following, read
`references/correctness-and-ops.md` and apply it:

- **Migrations in production** — no startup auto-migrate races; expand/contract for
  zero-downtime; idempotent deploy scripts.
- **Inheritance mapping** — TPH (fast, default) vs TPT (join-heavy, often slow) vs TPC.
- **Testing that can catch regressions** — avoid the InMemory provider's false
  confidence; use the real provider (Testcontainers) or SQLite in-memory.
- **Async/threading bugs** — no sync-over-async (`.Result`/`.Wait()`); one operation per
  DbContext; flow `CancellationToken`.
- **Observability** — `.TagWith(...)` to correlate LINQ↔SQL; OpenTelemetry/metrics.
- **Pagination correctness** — stable `OrderBy`; keyset paging for deep pages.
- **EF version shifts** — `Contains`/collection translation changed across EF7→8→9→10;
  re-profile list-filter queries after a major upgrade.
- **Read replicas / CQRS routing**, and **non-relational providers** (Cosmos is governed
  by request units + partition key, not relational query plans).

---

# Validation checklist

Before declaring an EF Core path optimized, confirm:

- [ ] The optimized code is behavior-equivalent to the original: same rows, values,
      ordering, null handling, write effects, and transaction atomicity (speed only).
- [ ] Query logging was inspected; the SQL count matches expectations (no N+1).
- [ ] Read-only queries use `AsNoTracking()` or project to a DTO.
- [ ] `Include` vs `AsSplitQuery` matches the data shape (no cartesian blowup).
- [ ] No client-side evaluation warnings remain in the logs.
- [ ] Inserts/updates of many rows do **one** `SaveChanges`, not one per row.
- [ ] Bulk modify/delete uses `ExecuteUpdate`/`ExecuteDelete`, not load-then-save.
- [ ] Very large imports use a real bulk path (SqlBulkCopy / COPY / bulk lib).
- [ ] DbContext is scoped/short-lived; not shared across threads.
- [ ] Parallel/background work uses a context-per-unit from a pooled factory.
- [ ] Transient faults are handled (`EnableRetryOnFailure`); explicit transactions
      run inside the execution strategy.
- [ ] Large reads stream (`AsAsyncEnumerable`) instead of buffering whole tables.
- [ ] Write hotspots use a concurrency token and handle `DbUpdateConcurrencyException`.
- [ ] `CancellationToken` flows through async calls; connection pool size is sized for load.
- [ ] Filter/sort/join columns are actually indexed.
- [ ] Raw SQL is parameterized (`FromSqlInterpolated`, never concatenated input).
- [ ] Request bodies aren't bound straight onto entities (no over-posting); DTOs used.
- [ ] Pagination has a stable `OrderBy`; production migrations don't auto-run on startup.
- [ ] Tests run against a provider that can catch regressions (not the InMemory provider).

# Common pitfalls

| Pitfall | Fix |
| --- | --- |
| Lazy loading silently causing N+1 | Disable lazy-loading proxies; load explicitly with `Include`/projection |
| Forgotten global query filters skewing analysis | Check `HasQueryFilter`; use `IgnoreQueryFilters()` when intended |
| One DbContext kept alive / tracking 100k entities | Scope it; chunk imports; `ChangeTracker.Clear()` or new context per chunk |
| Bulk update by load → edit → SaveChanges | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| `SaveChanges` inside the insert loop | Stage with `AddRange`, save once |
| SQL injection via `FromSqlRaw` + string interpolation | Use `FromSqlInterpolated` (parameterized) |
| Expecting EF to add indexes for you | Define indexes in the model; verify in migrations |
| Bulk-copy path expected to set generated keys / fire interceptors | It won't — handle keys/validation yourself, reserve it for ETL |
| Sharing one DbContext across parallel tasks | Context-per-unit via `AddPooledDbContextFactory` |
| Explicit transaction silently not retried | Run it inside `CreateExecutionStrategy().ExecuteAsync(...)` |
| Connection-pool timeout errors under load | Bound parallelism; raise `Max Pool Size`; shed load with cancellation |
| Buffering huge result sets with `ToList` | Stream with `AsAsyncEnumerable`, page, or project |
| Expecting EF to cache query *results* | It caches plans only — add an explicit distributed/second-level cache |
| Lost updates on contended rows | Add a `rowversion` token; handle `DbUpdateConcurrencyException` |
