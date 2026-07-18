---
name: create-implementation
description: Write a TypeScript implementation for a Clef concept — the handler that implements each action defined in the concept spec. Covers storage patterns, variant returns, input extraction, and testing.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
argument-hint: "<concept-name>"
---

# Create a Clef Concept Implementation

Write a TypeScript handler for the concept **$ARGUMENTS** that implements every action from its `.concept` spec.

## What is a Concept Implementation?

A concept implementation is a **handler object** that provides one function per action declared in the concept spec. Each function receives untyped `input` and returns a **variant completion** (a discriminated union like `{ variant: 'ok', ... }` or `{ variant: 'error', ... }`).

**The default and preferred style is functional** — handlers return a `StorageProgram<A>` (a free monad) describing storage operations as pure data, rather than executing them directly. This enables static effect analysis, purity validation, caching, and applicative parallelism.

```typescript
import type { FunctionalConceptHandler } from '../runtime/functional-handler';
import {
  createProgram, get, put, putFrom, find, branch, complete, completeFrom,
  mapBindings, type StorageProgram,
} from '../runtime/storage-program';
import { autoInterpret } from '../runtime/functional-compat';

const _handler: FunctionalConceptHandler = {
  // Simple action — value known at construction (use put/complete)
  create(input: Record<string, unknown>) {
    const name = input.name as string;
    let p = createProgram();
    p = put(p, 'items', name, { name, status: 'active' });
    return complete(p, 'ok', { item: name });
  },

  // Action using storage reads — use putFrom/completeFrom
  update(input: Record<string, unknown>) {
    const id = input.id as string;
    const newName = input.name as string;
    let p = createProgram();
    p = get(p, 'items', id, 'existing');
    return branch(p,
      (bindings) => !bindings.existing,
      (b) => complete(b, 'not_found', {}),
      (b) => {
        let b2 = putFrom(b, 'items', id, (bindings) => {
          const existing = bindings.existing as Record<string, unknown>;
          return { ...existing, name: newName };
        });
        return complete(b2, 'ok', { item: id });
      },
    );
  },
};
export const myHandler = autoInterpret(_handler);
```

For cases where functional style cannot be supported (language limitations, legacy concepts, direct FFI/system calls), use the **imperative fallback**:

```typescript
import type { ConceptHandler } from '@clef/kernel';

export const myHandler: ConceptHandler = {
  async actionName(input, storage) {
    const field = input.field as string;
    // ... business logic using storage ...
    return { variant: 'ok', field };
  },
};
```

Implementations are **pure business logic** — they never reference other concepts. All cross-concept coordination happens through syncs.

## Step-by-Step Process

### Step 1: Read the Concept Spec

Every implementation must match its `.concept` spec exactly. The spec defines:
- **Type parameters** — the generic types (e.g., `[U]` for user, `[A]` for article)
- **State** — the relations (storage tables) the concept manages
- **Actions** — the functions to implement, with their parameters and return variants
- **Invariants** — behavioral contracts the implementation must satisfy

Find and read the spec from `specs/app/<name>.concept` or `specs/framework/<name>.concept`.

Example spec structure:
```
concept Article [A] {
  purpose { Manage articles with title, description, body, and author. }

  state {
    articles: set A
    slug: A -> String
    title: A -> String
    ...
  }

  actions {
    action create(article: A, title: String, ...) {
      -> ok(article: A) { Add article to set. Store all fields. }
    }
    action update(article: A, title: String, ...) {
      -> ok(article: A) { Update fields. }
      -> notfound(message: String) { If article does not exist. }
    }
  }

  invariant {
    after create(article: a, title: "Test", ...) -> ok(article: a)
    then get(article: a) -> ok(article: a, title: "Test", ...)
  }
}
```

### Step 2: Create the Handler File

Place the file at:
```
handlers/ts/app/<name>.handler.ts        # App concepts
handlers/ts/framework/<name>.handler.ts   # Framework concepts
```

Start with the imports and handler skeleton. **Default to functional style:**

```typescript
import type { FunctionalConceptHandler } from '../runtime/functional-handler';
import { createProgram, get, find, put, merge, del, branch, complete, pure, traverse,
         relation, at, field, getLens, putLens, modifyLens } from '../runtime/storage-program';

export const <name>Handler: FunctionalConceptHandler = {
  // One method per action from the spec (no async — program construction is synchronous)
};
```

Only use the imperative skeleton when functional style cannot be supported:

```typescript
import type { ConceptHandler } from '@clef/kernel';

export const <name>Handler: ConceptHandler = {
  // One async method per action from the spec
};
```

### Step 3: Implement Each Action

> **Read-only actions are pure projections, not getters** (`docs/prd/read-layer-unification-prd.md`).
> Don't hand-write `get*`/`list*`/`find*` logic that re-implements client-shaped filtering — that
> coupling belongs in a QueryProgram/view the caller composes. If a read-only action must exist for
> API compatibility, implement it as a thin projection over the read contract (a
> `find(p, relation, criteria, 'rows')` + `completeFrom`) holding no client-specific query logic.
> Pure-computation actions (`resolve`/`parse`/`evaluate`/`compute`) are fine. New getter-style
> actions are rejected by `npm run audit:no-new-getters`.
>
> **A getter-verb read needs a classification annotation — and the audit re-checks it.** The only
> way a `get*`/`list*` action passes `no-new-getters` is one annotation, each verified against the
> handler's real StorageProgram shape (`audit:classification-integrity` + `audit:read-projection-integrity`):
> - `@read(intrinsic)` — a keyed single-entity roundtrip: `get(p, relation, id)` returning that one
>   entity's own fields (the `create`→`get` contract). Projecting one keyed record's own list field
>   (e.g. `getRelated`/`listBySource` filtering a relation's link set) is still intrinsic.
> - `@read(projection)` — **STRICTER**: a pure single-field read with NO `find()` collection scan and
>   NO iteration/aggregation. `audit:read-projection-integrity` fails if a `@read(projection)` does a
>   collection scan.
> - `@read(enumeration)` — the bare own-set `list()` (`find` EMPTY criteria, `paramCount==0`, non-pool).
> - `@compute` — pure, reads NO state (inputs only).
>
> **Antipattern — do NOT do this:** giving a collection-aggregating action a getter name + `@read(projection)`
> to slip past the ratchet. `getSummary(subject)` (aggregate runs), `getCoverage(schema)` (compute a ratio),
> `trend(...)` (time-series) are **computations**, not projections. Fix with (a) a derived **data-return
> read-route** (`-> read Concept where field: value`, consumer aggregates), (b) a **computation-verb rename**
> (`summarize`, `coverageFor` — a non-getter verb needs no annotation), or (c) a **QueryProgram**. Never
> relabel a collection scan as a projection — the projection audit will reject it.

For each action in the spec, write a method on the handler object. **Functional style (default):**

```typescript
actionName(input) {
  // 1. Extract input fields with type assertions
  const id = input.id as string;
  const name = input.name as string;

  // 2. Build the storage program
  let p = createProgram();
  p = get(p, 'item', id, 'existing');

  // 3. Use branch for conditionals, complete for terminal values
  return branch(p,
    (b) => b.existing != null,
    complete(createProgram(), 'error', { message: 'already exists' }),
    complete(put(createProgram(), 'item', id, { name }), 'ok', { item: id }),
  );
},
```

**Imperative fallback** (only when functional is not feasible):

```typescript
async actionName(input, storage) {
  // 1. Extract input fields with type assertions
  const field1 = input.field1 as string;
  const field2 = input.field2 as number;

  // 2. Business logic (validation, lookup, computation)

  // 3. Storage operations (read/write)

  // 4. Return a variant completion
  return { variant: 'ok', outputField: value };
},
```

#### Input Extraction

All inputs arrive as `Record<string, unknown>`. Cast each field to its TypeScript type:

| Spec Type | TypeScript Cast | Example |
|-----------|----------------|---------|
| `String` | `as string` | `input.name as string` |
| `Int` | `as number` | `input.count as number` |
| `Float` | `as number` | `input.rate as number` |
| `Bool` | `as boolean` | `input.active as boolean` |
| `Bytes` | `as string` (base64) | `input.data as string` |
| `DateTime` | `as string` (ISO 8601) | `input.created as string` |
| `ID`, type param | `as string` | `input.user as string` |

#### Variant Returns

Return exactly the variants declared in the spec. The `variant` field is the discriminant.

**Convention: success is always `ok`.** Use `'ok'` for the happy-path variant
in every action. Domain context belongs in the output fields, not the variant
name. Do NOT use domain-specific success names like `'created'`, `'configured'`,
`'registered'`, `'updated'` — these must all be `'ok'`.

**Exception — multiple distinct success branches.** When an action genuinely
has two or more success outcomes that syncs need to distinguish, use
domain-specific variant names (e.g., `'ok'`/`'miss'` for cache lookup,
`'clean'`/`'conflicts'` for merge). This should be rare.

```typescript
// Spec: -> ok(user: U) { ... }
return { variant: 'ok', user };

// Spec: -> error(message: String) { ... }
return { variant: 'error', message: 'name already taken' };

// Spec: -> notfound(message: String) { ... }
return { variant: 'notfound', message: 'Article not found' };

// Spec: -> ok(valid: Bool) { ... }
return { variant: 'ok', valid: true };
```

### Step 4: Wire Up Storage

Read [references/storage-interface.md](references/storage-interface.md) for the complete API.

Each concept gets its own isolated `ConceptStorage`. Storage is document-oriented — each **relation** from the spec maps to a storage collection.

**Relation naming convention**: The spec's state section defines relations. In implementations, use the entity name as the relation:

```
state { articles: set A; title: A -> String; ... }
→ storage relation: 'article'

state { hash: U -> Bytes; salt: U -> Bytes }
→ storage relation: 'password'
```

The key for each record is the type parameter value (the entity ID).

#### CRITICAL: Decide which `storageType` your concept uses

When the concept is registered in `generated/kernel-registry.ts`, it gets one of four `storageType` values. **Picking the wrong one is one of the deepest violations of the cleffy architecture** — see [the audit guide V1 + V7](../../../docs/architecture/clef-base-content-native-audit.md#part-iii--the-violation-patterns-and-how-to-fix-each).

| storageType | When to use | What you get |
|-------------|-------------|--------------|
| `'pool'` | **Entity-shaped** concepts — anything user-creatable, displayable, listable. Task, Project, Cycle, Event, KeyResult, Comment, Note, etc. | Writes route through `ContentStorage/save` + `ContentNode/create`. Schema overlay, PageAsRecord promotion, default block tree, child schema, compilation provider, search index, provenance, version, references, alias, undo all auto-apply via existing generic syncs. `ContentNode/listBySchema(schema:'<Name>')` returns every entity. `EntityDetailView` renders them via `DisplayMode(<Name>:detail)`. |
| `'standard'` | **Pool machinery + infrastructure**: RuntimeRegistry, FileCatalog, EntityReflector, Cache, SearchIndex, ContentNode, Property, Outline. These ARE the pool, not entities in it. | Plain SQLite namespace, no pool routing. |
| `'identity'` | Authentication / Session / ApiToken / AccessControl. Identity-scoped storage with separate persistence. | Identity DB. |
| `'none'` | Pure providers (SlotSource, BlockEmbedSource, EntityFieldSource, …) and computation-only concepts. | No storage handle. |

**The `'pool'` decision matrix** — if the answer is "yes" to any of these, you want `'pool'`:
- "Will users create instances of this concept through a UI?"
- "Should this entity show up in search?"
- "Does this entity have a detail page at `/admin/<x>/:id`?"
- "Should Cmd+Z undo a mutation on this entity?"
- "Should other concepts be able to Reference this entity?"
- "Does this entity have schema fields someone might want to filter or display?"

If yes, do **all four** of the following or your handler ends up in a parallel storage path that bypasses the entire content-native subsystem:

1. **Author a `.schema.yaml`** under `clef-base/schemas/<suite>.schema.yaml` (or its repertoire suite folder):
   ```yaml
   schemas:
     <ConceptName>:
       concept: <ConceptName>
       primary_set: items                    # the spec's main set
       manifest: content                     # 'content' = entity-shaped, 'config' = system records
       fields:
         title:        { from: title }       # mapped → ContentNode Property
         description:  { from: description }
         status:       { from: status }
         # one entry per field that should be visible / searchable / filterable
       content_native:
         displayWidget: <Name>-detail        # widget on the detail page
         defaultTemplate: <Name>-default     # block-tree scaffold for the body
         childSchema: <ChildName>            # schema applied to outline children (e.g. TaskComment)
         compilationProvider: none           # or a registered ContentCompiler
   ```
   Use `ContentTypeScaffoldGen/generate` rather than hand-authoring.

2. **Register with `storageType: 'pool'`** in `generated/kernel-registry.ts` — NOT `'standard'`.

3. **Don't add an `action list(filters)`** to your concept. `ContentNode/listBySchema(schema: '<Name>')` is the canonical query path; it uses the schema-membership index. Cross-cutting filters (assignee=current-user, status=Todo) flow through DataSourceSpec params, not custom list-action filter args.

4. **Don't write a `<X>DetailView.tsx`** React component. The destination row gets `componentId: EntityDetailView` + `hrefTemplate: /admin/<x>/:id`. Detail rendering comes from seeded `DisplayMode(<Name>:detail)` + `FieldPlacement` rows + `DisplayMode/set_flat_fields`. Inline panels (incoming dependencies, child tasks, backlinks) are SEPARATE ViewShells composed via Layout `children`, not `footer={...}` props.

**The handler code itself doesn't change.** Your handler still calls `storage.put('myconcept', id, record)` and `storage.get('myconcept', id)`. The pool storage adapter (`runtime/adapters/content-pool-storage.ts`) intercepts those calls and routes mapped fields → `ContentStorage/save` + `ContentNode/create`, unmapped fields → concept-local SQLite, set membership → Schema membership. The schema.yaml mapping is the contract.

**Escape hatches.** If your concept truly is internal compute that doesn't represent a user entity (CriticalPath compute results, BlockedByGraph transitive closures), use `manifest: config` in the schema.yaml so they don't promote to PageAsRecord, OR keep `storageType: 'standard'`. Don't use these escape hatches by default — most user-facing concepts want `'pool'`.

#### Storage Operations

```typescript
// Create / Update
await storage.put('article', articleId, {
  article: articleId, slug, title, description, body, author,
  createdAt: now, updatedAt: now,
});

// Read one
const record = await storage.get('article', articleId);
if (!record) return { variant: 'notfound', message: 'Article not found' };

// Query by criteria
const matches = await storage.find('user', { email });
if (matches.length > 0) return { variant: 'error', message: 'email taken' };

// Delete one
await storage.del('article', articleId);

// Delete many by criteria
const count = await storage.delMany('comment', { target: articleId });
```

### Step 5: Handle State Patterns

Read [references/handler-anatomy.md](references/handler-anatomy.md) for all patterns.

Common patterns that appear across implementations:

| Pattern | When to use | Example |
|---------|-------------|---------|
| **Uniqueness check** | Before creating entities | `find('user', { name })` before `put()` |
| **Existence check** | Before update/delete/get | `get('article', id)`, return `notfound` if null |
| **Read-modify-write** | Updating partial fields | `get()`, spread `{...existing, ...updates}`, `put()` |
| **Array mutation** | Set-valued relations | `get()`, push/filter array, `put()` ⚠ see RMW concurrency below |
| **Derived fields** | Computed from inputs | Slug from title, hash from password |
| **Timestamps** | Created/updated tracking | `new Date().toISOString()` |

#### ⚠ RMW + concurrent transactions

The "Array mutation" / "Read-modify-write" patterns above are safe **within a single Transactor pipeline** (the Transactor loops over Ops sequentially with awaited persistence between them — Op_{N+1}'s `storage.get` sees Op_N's persisted write) but they **race across concurrent transactions**. Two clients both calling `addToList(item)` at the same moment will both read the same prior list, each append in-memory, each write — last-write-wins, one client's append is silently dropped.

For state that may be mutated concurrently by other clients, prefer one of:

1. **Atomic-replace action.** Author the handler to take the full new value, not a delta:
   ```
   action setItems(entity: E, items: list String) { -> ok(entity: E) }
   ```
   One `storage.put`, no read-modify-write, no race. This is the recommended shape for any list/set-state field that more than one client writes. Pair with seed authors who pass the full roster up front (see the `create-seed` skill).

2. **Optimistic-concurrency precondition.** When the caller's pattern is structurally RMW (`get` → mutate → `put`), expose a version field and have the caller pair the write with a `kind:ensure { predicate: 'expectedVersion', expectedVersion: <read-time-version> }` Op in their transaction. The check runs atomically at commit; a concurrent writer's commit fails with `conflict_at` and the caller retries with the new version. See the `transactql` skill.

3. **`kind:add` / `kind:retract` primitive Ops.** Stage attribute-level writes that compose under the Transactor's STM commit, instead of an opaque `kind:call` to a RMW handler. These get intra-tx staged-db reads (the Jepsen-2024 D2 fix) and commit atomically with the transaction's other primitive writes. Trade-off: the handler-author surface is gone; the caller composes primitives directly.

The handler-side check that catches most accidental RMW races on review: "does this action read a list field, modify it in JS, and put it back?" If yes, ask "could two clients reasonably call this at the same time?" If yes, file a follow-up for an atomic-replace alternative and document the race in the handler header until it lands.

**Hard cases.** When the action looks too gnarly for pure StorageProgram — dynamic storage keys derived from find results, cross-concept calls, time/wait/timeout, conditionals, JS transformations over reads — read [references/functional-patterns.md](references/functional-patterns.md) before reaching for an imperative `async (input, storage)` override. The five patterns there cover ~every "but this case is too complex" scenario:

| Hard case | Pattern |
|-----------|---------|
| Dynamic storage keys derived from find | `traverse(p, source, item, body, bindAs, declaredEffects?)` |
| Cross-concept reads / writes | `perform(p, 'concept', '<X>/<action>', payload, bindAs)` + boot-time bridge |
| Time / wait / timeout / poll-until | `kind: wait` Op in transactQL via `Transaction/transactQL` |
| Conditional execution | `branch(p, predicate, ifFn, elseFn)` |
| Pure JS transform over reads | `mapBindings(p, fn, bindAs)` |

Functional style is the default and what enables purity-gated where-clause invocation, atomic dry-run, deterministic replay, and engine-level safety guarantees. **If you're about to write `async (input, storage)`, you almost certainly should read functional-patterns.md first** — most "imperative because…" reasons in the codebase turn out to be wrong / out of date.

### Step 6: Declare Capabilities

If the concept spec declares `capabilities { requires crypto }`, import from Node.js:

```typescript
import { createHash, createHmac, randomBytes } from 'crypto';
```

Other capability patterns:
- `requires crypto` → `import { createHash, randomBytes } from 'crypto'`
- `requires fs` → `import { readFileSync } from 'fs'`
- No capabilities → No special imports needed

### Step 7: Write Tests

Read [references/action-dispatch.md](references/action-dispatch.md) for the testing framework.

Write tests in `tests/<name>.test.ts` or `tests/<name>-flow.test.ts`. Three test levels:

#### Unit test (handler in isolation)

```typescript
import { describe, it, expect } from 'vitest';
import { createKernel } from '../handlers/ts/framework/kernel-factory';
import { myHandler } from '../handlers/ts/app/my.impl';

describe('My Concept', () => {
  it('performs action correctly', async () => {
    const kernel = createKernel();
    kernel.registerConcept('urn:clef/My', myHandler);

    const result = await kernel.invokeConcept('urn:clef/My', 'action', {
      field: 'value',
    });

    expect(result.variant).toBe('ok');
    expect(result.field).toBe('value');
  });
});
```

#### Invariant test (from spec)

The spec's `invariant` section defines behavioral contracts. Implement them as sequential action calls:

```typescript
it('satisfies invariant: after set, check returns true', async () => {
  const kernel = createKernel();
  kernel.registerConcept('urn:clef/Password', passwordHandler);

  // AFTER clause
  const step1 = await kernel.invokeConcept('urn:clef/Password', 'set', {
    user: 'test-user', password: 'secret123',
  });
  expect(step1.variant).toBe('ok');

  // THEN clause
  const step2 = await kernel.invokeConcept('urn:clef/Password', 'check', {
    user: 'test-user', password: 'secret123',
  });
  expect(step2.variant).toBe('ok');
  expect(step2.valid).toBe(true);
});
```

For framework concepts with record/list literal invariants, the inputs arrive as nested objects. Ensure your handler correctly destructures them:

```typescript
it('satisfies invariant: generates from manifest', async () => {
  const storage = createInMemoryStorage();
  // Record literal from the spec becomes a nested object input
  const result = await handler.generate({
    spec: 's1',
    manifest: {
      name: 'Ping', uri: 'urn:clef/Ping', typeParams: [], relations: [],
      actions: [{ name: 'ping', params: [],
        variants: [{ tag: 'ok', fields: [], prose: 'Pong.' }] }],
      invariants: [], graphqlSchema: '',
      jsonSchemas: { invocations: {}, completions: {} },
      capabilities: [], purpose: 'A test.',
    },
  }, storage);
  expect(result.variant).toBe('ok');
});
```

#### Flow test (with syncs)

```typescript
it('processes full flow', async () => {
  const kernel = createKernel();
  kernel.registerConcept('urn:clef/My', myHandler);
  await kernel.loadSyncs(resolve(SYNCS_DIR, 'my.sync'));

  const response = await kernel.handleRequest({ method: 'my_action', ... });
  expect(response.body).toBeDefined();

  const flow = kernel.getFlowLog(response.flowId);
  expect(flow.length).toBeGreaterThanOrEqual(4);
});
```

### Step 8: Register the Concept

In the application bootstrap, register with the kernel:

```typescript
import { createKernel } from './kernel-factory';
import { myHandler } from './my.impl';

const kernel = createKernel();
kernel.registerConcept('urn:clef/My', myHandler);
```

For versioned concepts (with schema migration support):

```typescript
await kernel.registerVersionedConcept('urn:clef/My', myHandler, 2);
```

## Projection Sync Pattern — How Implementations Shape API Responses

When a concept action returns raw data (e.g., a user ID string for `author`), the **response sync** is responsible for enriching it before building the `Web/respond` body. This is called a **projection sync** — a response sync that uses `where`-clauses to resolve raw concept output into a richer shape.

**Why this matters for implementations:** If your action returns a foreign key (like `author: userId`), don't try to resolve it inside the handler — that would couple concepts. Instead, return the raw ID. The sync layer handles the enrichment.

**Bad — coupling concepts in the implementation:**
```typescript
async list(_input, storage) {
  const articles = await storage.find('article');
  // DON'T: resolve author profile inside the article handler
  for (const a of articles) { a.author = await getProfile(a.author); }
  return { variant: 'ok', articles: JSON.stringify(articles) };
}
```

**Good — return raw data, let syncs enrich it:**
```typescript
async list(_input, storage) {
  const articles = await storage.find('article');
  return { variant: 'ok', articles: JSON.stringify(articles) };
}
```

The projection sync then enriches the response using `where`-clause queries:

```
sync LoginResponse [eager]
when {
  Web/request: [ method: "login"; email: ?email ]
    => [ request: ?request ]
  JWT/generate: [ user: ?user ]
    => [ token: ?token ]
}
where {
  User: { ?u email: ?email; name: ?username }
}
then {
  Web/respond: [
    request: ?request;
    body: [
      user: [
        username: ?username;
        email: ?email;
        token: ?token ] ] ]
}
```

This `LoginResponse` sync is a projection — it combines JWT output (`?token`) with User state queries (`?username`) into a shaped response body. The concept handlers stay independent; the sync layer composes them.

**The sync compiler validates field names** (Section 7.2): if a sync references `Article/list: [] => [ tagList: ?tags ]` but `Article/list` only outputs `articles`, the compiler warns at compile time. This catches mismatches between what your implementation returns and what syncs expect.

See the `/create-sync` skill for the full projection sync pattern and examples.

## Functional Handler Style (StorageProgram Monad) — The Default

Functional handlers are the **default and preferred style**. They return a `StorageProgram<A>` — a pure data description of storage operations. The interpreter executes the program later. This enables static analysis, purity checking, caching, and applicative parallelism.

### When to Use Imperative Handlers Instead

Imperative handlers are a **fallback** for cases where functional style cannot be supported:

| Always use functional (default) | Fall back to imperative only when... |
|---|----|
| All new concepts | Language target lacks higher-kinded types or monadic composition |
| Concepts needing static effect analysis | Concept requires direct FFI or system calls incompatible with the monad |
| Concepts needing purity validation | Legacy concepts not yet migrated (temporary) |
| Concepts needing applicative parallelism | |
| Concepts needing lens-based state access | |

### FunctionalConceptHandler Interface

```typescript
import type { FunctionalConceptHandler } from '../runtime/functional-handler';
import { createProgram, get, find, put, merge, del, branch, complete, pure, traverse,
         relation, at, field, getLens, putLens, modifyLens } from '../runtime/storage-program';

export const myHandler: FunctionalConceptHandler = {
  actionName(input) {
    // Note: NO storage parameter — build a program instead
    const id = input.id as string;
    let p = createProgram();
    p = get(p, 'item', id, 'existing');
    return branch(p,
      (b) => b.existing != null,
      complete(createProgram(), 'error', { message: 'already exists' }),
      complete(put(createProgram(), 'item', id, { name: input.name }), 'ok', { item: id }),
    );
  },
};
```

### Key Differences from Imperative Style

1. **No `storage` parameter** — handlers never see storage; they build programs
2. **No `async/await`** — program construction is synchronous
3. **Return `StorageProgram<{variant, ...}>` instead of `Promise<{variant, ...}>`**
4. **Use `complete()` instead of plain object returns** — tracks variant in the effect set
5. **Use `branch()` instead of `if/else`** — both arms' effects are merged conservatively

### StorageProgram DSL Quick Reference

| Operation | DSL Function | Effect |
|-----------|-------------|--------|
| Read one | `get(p, relation, key, bindAs)` | reads += relation |
| Query | `find(p, relation, criteria, bindAs)` | reads += relation |
| Write (static) | `put(p, relation, key, value)` | writes += relation |
| Write (from bindings) | `putFrom(p, relation, key, (bindings) => value)` | writes += relation |
| Partial update (static) | `merge(p, relation, key, fields)` | reads+writes += relation |
| Partial update (from bindings) | `mergeFrom(p, relation, key, (bindings) => fields)` | reads+writes += relation |
| Delete | `del(p, relation, key)` | writes += relation |
| Conditional | `branch(p, condition, thenProg, elseProg)` | union of both arms |
| Terminate (static) | `complete(p, variant, output)` | completionVariants += variant |
| Terminate (from bindings) | `completeFrom(p, variant, (bindings) => output)` | completionVariants += variant |
| Derive value | `mapBindings(p, (bindings) => value, bindAs)` | (no effect) |
| Iterate collection | `traverse(p, sourceBinding, itemBinding, (item, bindings) => subProgram, bindAs)` | union with body effects |
| Monadic bind | `compose(first, bindAs, second)` | union of both programs |

### CRITICAL: Binding Semantics — `bindAs` Names Are NOT JavaScript Variables

The `bindAs` parameter in `get()`, `find()`, `mapBindings()`, and `perform()` declares a **runtime binding name** — a key that the interpreter will populate in a `bindings: Record<string, unknown>` object when the program is executed. **These names do NOT become JavaScript variables in the handler function scope.**

You can ONLY access bound values through:
1. **`branch()` conditions**: `(bindings) => bindings.myVar != null`
2. **`putFrom()` / `mergeFrom()` value functions**: `(bindings) => ({ ...bindings.existing as Record<string, unknown>, name: newName })`
3. **`completeFrom()` output functions**: `(bindings) => ({ items: bindings.all as unknown[] })`
4. **`mapBindings()` derivation functions**: `(bindings) => (bindings.items as any[]).length`

#### WRONG — referencing `bindAs` name as a JS variable:

```typescript
// BAD — this will throw ReferenceError at runtime!
actionName(input) {
  let p = createProgram();
  p = get(p, 'items', id, 'existing');       // binds result as 'existing'
  if (existing) {                              // ← ReferenceError! 'existing' is not a JS variable
    p = put(p, 'items', id, { ...existing, name: newName });
  }
  return complete(p, 'ok', {});
}
```

#### CORRECT — accessing bound values through bindings lambdas:

```typescript
// GOOD — access bound values through branch/putFrom/completeFrom lambdas
actionName(input) {
  const id = input.id as string;
  const newName = input.name as string;
  let p = createProgram();
  p = get(p, 'items', id, 'existing');        // binds result as 'existing'
  return branch(p,
    (bindings) => !bindings.existing,           // ← access via bindings object
    complete(createProgram(), 'notFound', { message: 'Item not found' }),
    (() => {
      let b = createProgram();
      b = putFrom(b, 'items', id, (bindings) => {   // ← access via bindings
        const existing = bindings.existing as Record<string, unknown>;
        return { ...existing, name: newName };
      });
      return complete(b, 'ok', { item: id });
    })(),
  );
}
```

#### CORRECT — using mapBindings to derive values:

```typescript
actionName(input) {
  let p = createProgram();
  p = find(p, 'items', {}, 'allItems');       // binds result as 'allItems'
  p = mapBindings(p, (bindings) => {           // ← derive a count from bindings
    return (bindings.allItems as any[]).length;
  }, 'itemCount');
  return completeFrom(p, 'ok', (bindings) => ({
    count: bindings.itemCount as number,
    items: bindings.allItems as unknown[],
  }));
}
```

#### Common Patterns Requiring Bindings Access

| Pattern | Wrong (ReferenceError) | Correct |
|---------|----------------------|---------|
| Check existence after get | `if (existing) { ... }` | `branch(p, (b) => b.existing != null, ...)` |
| Use fetched data in put | `put(p, rel, key, { ...existing })` | `putFrom(p, rel, key, (b) => ({ ...b.existing as any }))` |
| Return fetched data | `complete(p, 'ok', { items: all })` | `completeFrom(p, 'ok', (b) => ({ items: b.all }))` |
| Compute from fetched data | `const count = items.length` | `mapBindings(p, (b) => (b.items as any[]).length, 'count')` |
| Filter fetched results | `const filtered = items.filter(...)` | `mapBindings(p, (b) => (b.items as any[]).filter(...), 'filtered')` |
| Iterate and modify | `for (const item of items) { storage.put(...) }` | `traverse(p, 'items', '_item', (item) => { let s = createProgram(); s = put(s, ...); return complete(s, 'ok', {}); }, '_results')` |

### CRITICAL: Variant and Storage Anti-Patterns

#### _variant convention (DOES NOT WORK)
Returning `{ _variant: 'notfound' }` from a `completeFrom` callback does NOT change the variant. The variant is always the second argument to `completeFrom`. The `_variant` field is just ignored data.

**Bad:**
```typescript
return completeFrom(p, 'ok', (bindings) => {
  if (!entry) return { _variant: 'notfound' };  // BROKEN: variant is still 'ok'
  return { handler: entry.id };
});
```

**Good:** Use `mapBindings` + `branch` to select the correct variant:
```typescript
p = mapBindings(p, (b) => (b.all as any[]).find(...) || null, '_found');
return branch(p,
  (b) => !!b._found,
  (b) => completeFrom(b, 'ok', (b) => ({ handler: (b._found as any).id })),
  (b) => complete(b, 'notfound', {}),
);
```

#### _puts convention (DOES NOT WORK)
Returning `{ _puts: [...] }` from `completeFrom` does NOT write to storage. The interpreter treats `completeFrom` results as terminal pure values.

**Good:** Use `putFrom` before `completeFrom`:
```typescript
let p2 = putFrom(p, 'items', key, (b) => record);
return completeFrom(p2, 'ok', (b) => ({ item: id }));
```

#### Iterating over collections — use `traverse`
When you need to find N records and perform an operation on each (e.g., mark all matching entries as stale), use `traverse` — the monadic `mapM`/`traverse` pattern:

```typescript
invalidateByKind(input: Record<string, unknown>) {
  const kind = input.kind as string;
  let p = createProgram();
  p = find(p, 'entries', {}, 'allEntries');

  // traverse: for each entry, conditionally mark stale
  p = traverse(p, 'allEntries', '_entry', (item) => {
    const entry = item as Record<string, unknown>;
    const matches = (entry.kind as string) === kind;
    let sub = createProgram();
    if (matches) {
      sub = put(sub, 'entries', entry.stepKey as string, { ...entry, stale: true });
      return complete(sub, 'invalidated', { stepKey: entry.stepKey });
    }
    return complete(sub, 'skipped', {});
  }, '_results', {
    writes: ['entries'],
    completionVariants: ['invalidated', 'skipped'],
  });

  return completeFrom(p, 'ok', (bindings) => {
    const results = (bindings._results || []) as Array<Record<string, unknown>>;
    const invalidated = results.filter(r => r.variant === 'invalidated').map(r => r.stepKey as string);
    return { invalidated };
  });
}
```

`traverse(p, sourceBinding, itemBinding, bodyFn, bindAs, declaredEffects?)`:
- **sourceBinding**: name of a bound array (from a prior `find`)
- **itemBinding**: name to bind each item during iteration
- **bodyFn**: `(item, bindings) => StorageProgram` — sub-program for each element
- **bindAs**: name to bind the collected results array
- **declaredEffects** (optional): `{ reads?, writes?, completionVariants?, performs? }` — structural effect declaration for static analysis

The interpreter executes each sub-program sequentially, collects their outputs, and binds the results array.

**Always pass `declaredEffects`** when the body accesses item properties (which is almost always). Without it, the DSL runs the body with empty sentinel data `({}, {})` to extract effects — which throws if the body does `item.key`, `entry.stepKey`, etc. Declared effects make static analysis (completion coverage, read/write sets, purity classification) work correctly without running the body.

**Never use imperative overrides for collection iteration** — `traverse` is the standard functional solution.

#### Dynamic storage keys — use `mapBindings`
`putFrom(p, rel, key, fn)` requires `key` to be a static string. If the key is computed at runtime (e.g., a generated UUID), compute it via `mapBindings` then use `putFrom`:
```typescript
p = mapBindings(p, () => randomUUID(), '_id');
p = putFrom(p, 'items', '_placeholder', (bindings) => {
  // Note: the actual key resolution happens via the id field
  return { id: bindings._id as string, name };
});
```

#### Actions requiring stateful engine calls
If an action needs to call methods on a stateful class instance, it cannot be expressed as a pure StorageProgram. Use imperative style for those specific actions.

### Lens-Based State Access

Use typed, composable lenses instead of raw string keys:

```typescript
const userLens = at(relation('user'), userId);       // user[userId]
const emailLens = field(userLens, 'email');           // user[userId].email

let p = createProgram();
p = getLens(p, userLens, 'record');                   // read through lens
p = modifyLens(p, emailLens, () => ({ email: newEmail })); // modify through lens
return complete(p, 'ok', { user: userId });
```

Lenses enable: impact analysis, automatic migration scripts, schema diff detection, and composable state references.

### Registering Functional Handlers

```typescript
import type { FunctionalHandlerRegistration } from '../runtime/functional-handler';

const registration: FunctionalHandlerRegistration = {
  id: 'user-create',
  concept: 'User',
  action: 'create',
  purity: 'read-write',               // Must match actual effects
  declaredVariants: ['ok', 'error'],   // For algebraic effect coverage
  factory: myHandler.create,
};
```

The `purity` field is validated against the program's structural effects at build time — declaring `read-only` for a handler that writes will produce an error.

### Testing Functional Handlers

```typescript
import { classifyPurity, extractCompletionVariants, validatePurity } from '../runtime/storage-program';

it('has correct purity', () => {
  const program = myHandler.create({ id: '1', name: 'Test' });
  expect(classifyPurity(program)).toBe('read-write');
  expect(validatePurity(program, 'read-write')).toBeNull();
});

it('covers all declared variants', () => {
  const program = myHandler.create({ id: '1', name: 'Test' });
  const variants = extractCompletionVariants(program);
  expect(variants).toContain('ok');
  expect(variants).toContain('error');
});
```

## Checklist

Before considering the implementation complete:

**For functional handlers (FunctionalConceptHandler) — the default:**
- [ ] **Every action in the spec has a corresponding method** — missing actions are conformance failures
- [ ] **Every function used in the handler body is imported** — `find`, `traverse`, `mergeFrom`, `merge`, `del`, `mapBindings`, `completeFrom`, `pureFrom` etc. must all appear in the import statement. A `ReferenceError: X is not defined` at runtime means a missing import
- [ ] All input fields extracted with correct type casts
- [ ] Every variant from the spec is returned on the appropriate code path
- [ ] Storage relation names match the spec's state section
- [ ] Handler returns `StorageProgram`, never calls storage directly
- [ ] Uses `complete()` or `completeFrom()` for all terminal values (not plain `pure()` or `pureFrom()`) — `complete`/`completeFrom` track the variant in the structural effect set; `pure`/`pureFrom` do not
- [ ] Uses `branch()` for conditionals (not if/else)
- [ ] Declared purity matches actual structural effects
- [ ] Lens-based access used where possible (not raw string keys)
- [ ] Independent reads identified for applicative parallelism
- [ ] All completion variants reachable in the program tree
- [ ] No references to other concepts (all coordination via syncs)
- [ ] Handler exported as `const <name>Handler: FunctionalConceptHandler`
- [ ] Capabilities imported if spec declares them
- [ ] **Existence checks before reads/updates/deletes** — use `get(p, relation, key, 'existing')` then `branch(p, 'existing', thenBranch, elseBranch)` to return `error`/`notfound` when the entity doesn't exist. **NEVER** use `completeFrom(p, 'ok', ...)` with an inline null-check that silently returns empty data — that still completes with variant `ok` and will fail conformance tests for error-case fixtures
- [ ] **Uniqueness checks before creates** — use `get` + `branch` to check if a record already exists and return `duplicate`/`already_exists` variant
- [ ] **Input validation guards for error fixtures** — for every error-case fixture in the concept spec (fixtures with `-> error`, `-> invalid`, etc.), the handler MUST have a guard clause that validates the input and returns the error variant BEFORE any storage operations. Pattern: `if (!input.name || (input.name as string).trim() === '') return complete(createProgram(), 'error', { message: 'name is required' })`
- [ ] **JSON.parse safety** — when parsing input fields that may not be valid JSON, wrap in try/catch and return an error variant on parse failure. Never assume `input.field` is valid JSON
- [ ] **register() concept name** — the `register()` action must return the exact PascalCase concept name matching the spec (e.g., `'MyersDiff'` not `'myers'`)

**For imperative handlers (ConceptHandler) — fallback only:**
- [ ] One async method per action in the spec
- [ ] All input fields extracted with correct type casts
- [ ] Every variant from the spec is returned on the appropriate code path
- [ ] Storage relation names match the spec's state section
- [ ] Uniqueness checks before creates (if spec mentions uniqueness)
- [ ] Existence checks before updates/deletes/gets
- [ ] Invariants from the spec pass as tests
- [ ] No references to other concepts (all coordination via syncs)
- [ ] Handler exported as `const <name>Handler: ConceptHandler`
- [ ] Capabilities imported if spec declares them

## Quick Reference

See [references/handler-anatomy.md](references/handler-anatomy.md) for the handler interface and all action patterns.
See [references/storage-interface.md](references/storage-interface.md) for the full storage API.
See [references/action-dispatch.md](references/action-dispatch.md) for dispatch, testing, and registration.
See [examples/realworld-implementations.md](examples/realworld-implementations.md) for all RealWorld app implementations.
See [templates/implementation-scaffold.md](templates/implementation-scaffold.md) for copy-paste templates.

## Related Skills

| Skill | When to Use |
|-------|------------|
| `/create-concept` | Design the concept spec that this implementation fulfills |
| `/create-sync` | Write syncs that invoke actions on this implementation |
| `/create-storage-adapter` | Write the storage backend this implementation uses |
| `/create-transport-adapter` | Write the transport that delivers actions to this implementation |
| `/create-suite` | Bundle this implementation into a suite with its concept and syncs |
| `/create-view-query` | For view-layer concept implementations, use QueryProgram instructions (scan, filter, sort, group, project, join, pure) instead of ad-hoc data retrieval. Clef has three program monads: **StorageProgram** (handler layer), **RenderProgram** (surface layer), **QueryProgram** (view layer). |
