---
name: radzion-method
description: Use when implementing or refactoring heavily-typed TS / React state code. The Radzion Method - Record dispatch, match helpers, ensurePresent / attempt, core.ts vs types.ts, setupValueProvider / setupStateProvider, optimistic-with-snapshot-rollback. Pairs with radzion-method rule.
---

# Radzion Method

A type-driven discipline that compresses TS/React state code by leaning
hard on the type system, const arrays, and Record-based dispatch.

Read `radzion-method` rule (`~/.cursor/rules/radzion-method.mdc`) for
the full rule list. This skill is the procedural how-to.

## When to use

- Designing a new feature module on a client app with state +
  fetches + variants.
- Refactoring a `switch/case` ladder over a typed union into Record
  dispatch.
- Building a resolver pattern for N variants sharing operations
  (chains, payment rails, bookmakers, providers).
- Replacing manual `if(isLoading)/if(error)/if(!data)` ladders with
  `<MatchQuery>`.
- Replacing a manual cache-update mutation with the optimistic +
  snapshot-rollback pattern.

## When NOT to use

- The codebase only has 2-3 variants. Resolver pattern is overkill.
- The service uses a different framework (TypeORM repositories,
  legacy Sequelize). Don't force the method on legacy code.
- The team / service convention is already settled differently.
  Stay consistent with neighbors.

## Step 1 — set the file layout

```
modules/<feature>/
  config.ts        camelCase constants
  core.ts          const arrays + derived types + mappings
  types.ts         pure type definitions (zero runtime)
  data/
    hooks.ts       useXxxQuery (raw), useXxx (resolved/asserted)
    mappers/       pure API -> domain transformers
  <sub-feature>/
    index.tsx      barrel export
    *.tsx          one component per file
```

NO `components/`, `hooks/`, `utils/` folders inside the feature.

## Step 2 — derive types from const arrays

```ts
// core.ts
export const sortableColumns = ['size', 'creationTime'] as const;
export type SortableColumn = (typeof sortableColumns)[number];

export const chainKindRecord = {
  Ethereum: 'evm',
  Arbitrum: 'evm',
  Cosmos: 'cosmos',
  Solana: 'solana',
} as const;
export type ChainKind = (typeof chainKindRecord)[keyof typeof chainKindRecord];
```

Never duplicate the union literal next to the runtime array.

## Step 3 — boundary helpers

- `ensurePresent(value, valueName)` - throw if null/undefined; use at
  the system boundary.
- `attempt(() => ...)` - returns `{ data } | { error }`. Use at
  user-facing boundaries instead of try/catch.
- `isOneOf(value, constArray)` - runtime check that narrows the type.

## Step 4 — dispatch with Record, not switch

```ts
// Bad
switch (chain) { case 'ethereum': ...; case 'solana': ...; ... }

// Good
const resolvers: Record<ChainKind, Resolver<Input, Output>> = {
  evm: evmResolver,
  cosmos: cosmosResolver,
  solana: solanaResolver,
};
export const getResult = (input: Input) => resolvers[getChainKind(input.chain)](input);
```

TypeScript enforces exhaustiveness. Adding a new variant = one Record
entry; the compiler tells you every site that needs to handle it.

## Step 5 — `<MatchQuery>` for every query UI

```tsx
<MatchQuery
  value={query}
  pending={() => <Skeleton />}
  error={(e) => <ErrorState error={e} />}
  success={(data) => <FeatureView data={data} />}
/>
```

Never write `if (isLoading) ... if (error) ... if (!data) ...`.
Pre-conditions (wallet connected, user logged in) go BEFORE
`<MatchQuery>`, never inside.

## Step 6 — providers for subtree state

- `setupValueProvider<T>(contextId)` for read-only computed values.
- `setupStateProvider<T>(contextId, initialValue?)` for mutable state.
- Compose providers innermost = fastest-changing. Re-render blast
  radius scales with provider depth.

## Step 7 — optimistic with snapshot rollback

```ts
useMutation({
  mutationFn: placeOrder,
  onMutate: async (input) => {
    await queryClient.cancelQueries({ queryKey });
    const previous = queryClient.getQueryData(queryKey);
    queryClient.setQueryData(queryKey, (curr) => applyOptimistic(curr, input));
    return { previous };
  },
  onError: (_, __, ctx) => {
    if (ctx?.previous) queryClient.setQueryData(queryKey, ctx.previous);
    showErrorToast('Reverted');
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey }),
});
```

Never re-fetch to recover from an error you already know failed.
Restore the snapshot.

## Step 8 — WebSocket sync hooks (5 rules)

1. Subscribe via a ref-counted stream (multiple consumers share one
   socket).
2. Update via a pure `applyXxxUpdate(prev, update)` function.
3. Write directly to the React Query cache via `setQueryData`.
4. Drop the update if `prev` is undefined (idempotent on empty
   cache).
5. Unsubscribe on unmount or key change.

Combine with `{ staleTime: 3_000, refetchInterval: 15_000 }` as a
deferred-REST-invalidation safety net behind the WS feed.

## Anti-patterns

See `radzion-method` rule. Most common in review:

- `switch/case` on a typed union.
- `useMemo`/`useCallback` cargo-cult when React Compiler is enabled.
- Manual `if(isLoading)` ladders.
- Asymmetric REST fallbacks across order/event sides.
- `?.` / `?? ''` on non-optional types.
- `as` type assertions.
