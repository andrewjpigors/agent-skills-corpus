---
name: react-perf-investigation
description: Use when a React app feels janky, drops frames, has slow form input, or shows excess re-renders. Procedure for measuring before optimizing, then applying Tao-of-React-grounded fixes (children-as-prop, context split, key fixes, effect anti-patterns, memo cargo cult).
---

# React Perf Investigation

Most perceived "slow React" is one of a small number of fixable
patterns. The right answer is almost never "add `useMemo` everywhere."

## Step 1 — measure first

- Open React DevTools Profiler. Record an interaction that feels slow.
- Identify the components with the highest "render time" and "render
  count" for that interaction.
- Sort by what re-rendered: which components rendered that didn't
  visibly change?
- If you can't reproduce in DevTools, you don't have a perf bug yet.

## Step 2 — categorize

Match the symptom to its likely cause:

| Symptom | Most likely cause |
|---|---|
| Whole tree re-renders on every keystroke | Form state lifted too high; controlled inputs |
| Tab switch janks for a moment | Synchronous expensive child needs `useTransition` |
| Long list scrolls poorly | Not virtualized; or missing keys |
| New item briefly shows wrong content | Array index used as key |
| Modal closes slowly | Children-as-prop not used; modal parent re-renders too much |
| Form submit is slow | Validation runs on every render (recreated schema) |
| Initial route is heavy | Not lazy-loaded; MUI barrel import; huge bundle |

## Step 3 — common fixes

### Children-as-prop isolation

Component that owns fast-changing state (open/closed, hover, input
value) accepts `children` and passes them through. Its state change
does NOT re-render the children.

### Context split by change frequency

A single context that mixes "current input value" and "current locale"
makes every consumer re-render on every keystroke. Split into two
contexts: high-frequency stays narrow, low-frequency stays broad.

### Memoize the context value

`<Context.Provider value={{ foo }}>` rebuilds the object every parent
render. Either `useMemo` the value, or use a Zustand/RTK store
instead of context for cross-cutting state.

### Stable keys

Array index as key for a reorderable list is the canonical "ghost
state from previous item" bug. Use a stable, unique id.

### useEffect that should not exist

- `setState` inside `useEffect` to derive state from props - derive
  during render instead.
- An effect that only runs on mount and synchronously sets state -
  that's a render-time computation.
- An effect that subscribes - its teardown must match exactly THIS
  run's subscription, not "the latest one."
- A fetch effect that doesn't cancel via `AbortController` on
  re-render - races return stale data.

### AbortController in fetch effects

```ts
useEffect(() => {
  const ctrl = new AbortController();
  fetch(url, { signal: ctrl.signal }).then(...);
  return () => ctrl.abort();
}, [url]);
```

### `useTransition` for non-urgent updates

Filter typing where the filtered list rebuild is expensive: wrap the
update in `startTransition` so the input stays responsive.

### `useDeferredValue` for expensive downstream

Pass `useDeferredValue(value)` to the expensive child so the input
updates immediately and the child catches up.

### Virtualize past ~200 visible rows

`react-window`, `react-virtuoso`. Below that, key stability + memoized
rows is usually enough.

### Bundle hygiene

- MUI: `import Button from '@mui/material/Button'`, never the barrel.
- Route-level lazy: `React.lazy` + `Suspense` around routes and
  rarely-used modals.

## Step 4 — verify

- Re-record the same interaction in Profiler.
- The fix should reduce render count or render time on the targeted
  component.
- If it didn't, undo and try the next category - don't keep stacking
  "fixes."

## Anti-patterns

- Adding `useMemo` / `useCallback` everywhere without a memoized
  consumer benefiting from referential stability.
- "Premature memoization" before measuring.
- Adding `React.memo` to a component that re-renders for the right
  reason (a real prop change).
- Replacing a render-time derivation with `useEffect` + `setState`.

## Dispatch

- For review of a perf-shaped PR, hand to `react-perf-reviewer`.
- For an SSR/hydration mismatch, hand to `frontend-reviewer` +
  trigger `runtime-boundary-review` skill.
