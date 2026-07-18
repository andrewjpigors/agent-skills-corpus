---
name: agent-observability-pattern
description: "Conventions for observing a multi-step AI SDK agent in a Next.js app — how to model every agent boundary as a closed TypeScript discriminated union, emit it from a single recorder that isolates volatile experimental_ callback names, stream it as custom data-trace-event parts over the same UI message stream, reduce it in a store, and derive the view through pure selectors with cost computed in one pricing module. Use whenever creating, updating, or porting the src/lib/trace module — trace event union, recorder, pricing, run store, selectors, or the agent run route. Triggers include: 'observe the agent', 'trace events', 'agent timeline', 'token usage', 'tool call timeline', 'stream agent steps', 'cost per run', 'add a trace event', 'instrument the agent'."
---

# The agent observability layer

## Goal

Every interesting boundary in an agent run — the run starting, a step starting, a tool call beginning and ending, a step finishing with token usage, the run finishing with a total cost — is modelled as **one self-contained event in a closed TypeScript discriminated union** (`TraceEvent`). A single `recorder` module is the only place that touches the AI SDK's volatile `experimental_*` callback names; it translates each callback into a stable union member. Those events stream to the client as custom `data-trace-event` parts over the **same** `createUIMessageStream` connection that carries the assistant's text — there is no second channel. A store reduces the flat event log; **pure selectors** (`deriveSteps`, `deriveBounds`) are the only bridge from that log to the view. Cost is computed in exactly one `pricing` module. Adding a new observable boundary is a fixed **5-step ritual**, and TypeScript exhaustiveness checking is what forces every step to be completed.

## Files

- **`src/lib/trace/types.ts`** — The single source of truth: the `TraceEvent` discriminated union. One variant per boundary, discriminated by a string `type` literal. Every variant carries a monotonic `ts: number` (epoch millis). This file imports nothing app-specific and is the contract every other file in the layer agrees on.
- **`src/lib/trace/recorder.ts`** — `createRecorder({ runId, modelId, task, onEvent })` returns `{ callbacks, finish() }`. `callbacks` is the object spread into `streamText(...)`; it is the **only** place the volatile `experimental_onStepStart` / `experimental_onToolCallStart` / `experimental_onToolCallFinish` / `onStepFinish` names appear. Each callback maps its SDK argument to a `TraceEvent` and pushes it through `onEvent`, passing tool `input` / `output` / `error` through `sanitize()` first so the emitted event is safe-by-construction. The recorder owns all per-run accumulation (token totals, step start times) and emits `run-start` on construction and `run-finish` from `finish()`.
- **`src/lib/trace/sanitize.ts`** — `sanitize(value)` (and `sanitizeText(str)`): the single source of truth for what is safe to keep in a `TraceEvent`. Masks object keys that look like credentials, scrubs token-shaped substrings out of strings (provider keys, `Bearer …`, JWTs, PEM blocks), and truncates runaway strings. Pure and **idempotent**, so it can run again at render time as a safety net for legacy data. Applied at the emission boundary in `recorder.ts`, never only at render.
- **`src/lib/trace/pricing.ts`** — `costFor(modelId, { inputTokens, outputTokens })`. The **only** place token-to-dollar rates live. Keyed by the stable `provider:alias` model ID, never by raw model strings. Returns `0` for unknown IDs rather than throwing.
- **`src/lib/store/run-store.ts`** — The reducer. Holds `events: TraceEvent[]` plus run status, and exposes `append(event)` (live path) alongside replay/load actions. It also exports the **pure selectors** `deriveSteps` and `deriveBounds` — no React, no side effects — which fold the flat log into the shape the timeline renders.
- **`src/app/api/agent/run/route.ts`** — The server boundary. Wraps `streamText` in `createUIMessageStream`, wires the recorder's `onEvent` to `writer.write({ type: "data-trace-event", data: event })`, merges the model's own UI stream, then calls `recorder.finish()`. Returns `createUIMessageStreamResponse`.
- **`src/lib/trace/recorder.test.ts`** — The recorder contract test (layer 1 of 4). Drives each callback with a fake SDK argument and asserts the exact `TraceEvent` emitted.
- **`src/lib/trace/sanitize.test.ts`** — The sanitizer table-test (layer 3 of 4). Asserts credential keys are masked, token-shaped values scrubbed, nesting/truncation handled, and that `sanitize()` is idempotent. Build any token-shaped fixtures at runtime (string concatenation) so no literal secret pattern is committed — a secret-guard hook will reject the file otherwise.

## Rules

1. **The union is closed and authoritative.** Every observable boundary is a member of `TraceEvent` in `types.ts`. No code anywhere may invent an ad-hoc event shape or stream a payload that is not a `TraceEvent`. Discriminate only on the `type` string literal.
2. **Every event carries a monotonic `ts`.** Timestamps are epoch milliseconds captured with `Date.now()` at emit time. Selectors and the timeline rely on `ts` ordering; an event without `ts` cannot be placed on the timeline.
3. **Volatile callback names live only in the recorder.** The `experimental_*` names (and any future renames) appear in exactly one module. The rest of the app sees only the stable union. When the SDK renames a callback, you change one line in `recorder.ts` and nothing else moves.
4. **Adding a boundary follows the 5-step ritual, enforced by exhaustiveness.** (a) Add the variant to the union in `types.ts`; (b) emit it from the recorder; (c) handle it in the store reducer / selectors; (d) render it; (e) add a recorder-contract test. A `switch (event.type)` with a `default: const _exhaustive: never = event` (or an exhaustive `if/else` chain) makes the compiler fail until every consumer handles the new variant — that is the enforcement mechanism, not discipline.
5. **One stream, not two.** Trace events ride the same `createUIMessageStream` connection as the assistant text, as custom `data-trace-event` parts. Never open a second SSE/WebSocket channel for telemetry — it desynchronises ordering and doubles the failure surface.
6. **The client consumes trace events via `useChat`'s `onData`.** Custom data parts arrive through `onData`; filter on `part.type === "data-trace-event"` and `append(part.data)` to the store. Do not parse the raw stream by hand.
7. **Selectors are pure and are the only bridge to the view.** Components never walk `events[]` directly. They call `deriveSteps(events)` / `deriveBounds(events, now)`. Selectors take the event array (plus a `now` fallback) and return plain data — no React hooks, no `Date.now()` inside, no mutation of inputs beyond locally constructed accumulators.
8. **Cost is derived in one place.** Dollar figures come only from `costFor(...)` in `pricing.ts`, computed once at `run-finish` (or per-step from `usage`). The UI never hardcodes a rate or multiplies tokens by a number inline.
9. **Tool I/O is sanitized at the emission boundary.** The recorder passes tool-call `input`, `output`, and `error` through `sanitize()` *before* `onEvent`, so the persisted `TraceEvent` is **safe-by-construction**. Redaction must never live only in the inspector/renderer: by the time a component renders, the raw payload has already been streamed to the client, reduced into the store, and written to IndexedDB. Sanitization is both key-based (mask credential-looking keys) and value-based (scrub token-shaped substrings), and is idempotent so the renderer may re-apply it as a safety net for runs persisted before this rule existed.
10. **Four test layers.** (1) Recorder contract — each callback emits the right event with fake timers for deterministic `ts`. (2) Selector logic — feed a hand-built event log, assert the derived steps/bounds. (3) Sanitizer — table-test `sanitize()` over secret keys, token-shaped values, nesting, truncation, and idempotency. (4) End-to-end — mock the SSE response and assert the store ends in the expected state. See the wire format in rule 11.
11. **The SSE wire format is fixed.** Each chunk is `data: <json>\n\n`; the stream is terminated by `data: [DONE]`; the response `Content-Type` is `text/event-stream`; and it carries the header `x-vercel-ai-ui-message-stream: v1`. Tests that mock the stream must reproduce this exactly or `useChat` will not parse it.

## Canonical example

// src/lib/trace/types.ts
```typescript
// The single, closed contract. One self-contained variant per agent boundary,
// discriminated by `type`. EVERY variant carries a monotonic `ts` (epoch ms).
// Adding a boundary starts here; exhaustiveness checks downstream then fail
// until every consumer handles the new variant.
export type TraceEvent =
  | { type: "run-start"; runId: string; modelId: string; task: string; ts: number }
  | { type: "step-start"; stepNumber: number; ts: number }
  | {
      type: "tool-call-start";
      stepNumber: number;
      toolCallId: string;
      toolName: string;
      input: unknown;
      ts: number;
    }
  | {
      type: "tool-call-finish";
      stepNumber: number;
      toolCallId: string;
      durationMs: number;
      ok: boolean;
      output?: unknown;
      error?: string;
      ts: number;
    }
  | {
      type: "step-finish";
      stepNumber: number;
      durationMs: number;
      usage: { inputTokens: number; outputTokens: number; totalTokens: number };
      finishReason: string;
      ts: number;
    }
  | {
      type: "run-finish";
      totalDurationMs: number;
      totalUsage: { inputTokens: number; outputTokens: number; totalTokens: number };
      costUsd: number;
      ts: number;
    };
```

// src/lib/trace/pricing.ts
```typescript
// USD per 1M tokens — the ONE place rates live. Keyed by the stable
// "provider:alias" model ID, never a raw model string. The UI never multiplies
// tokens by a rate inline; it reads costUsd off the run-finish event.
type Price = { inputPer1M: number; outputPer1M: number };

const PRICES: Record<string, Price> = {
  "openai:fast": { inputPer1M: 0.15, outputPer1M: 0.6 },
  "openai:balanced": { inputPer1M: 2.5, outputPer1M: 10.0 },
  "anthropic:fast": { inputPer1M: 0.8, outputPer1M: 4.0 },
  "anthropic:balanced": { inputPer1M: 3.0, outputPer1M: 15.0 },
};

export function costFor(
  modelId: string,
  usage: { inputTokens: number; outputTokens: number },
): number {
  const p = PRICES[modelId];
  if (!p) return 0; // unknown model → 0, never throw
  return (usage.inputTokens / 1e6) * p.inputPer1M + (usage.outputTokens / 1e6) * p.outputPer1M;
}
```

// src/lib/trace/sanitize.ts
```typescript
// The single source of truth for "what is safe to keep" in a TraceEvent. Runs at
// the emission boundary (recorder.ts) so every downstream consumer — stream, store,
// IndexedDB, replay, inspector — receives already-safe data. Two layers of defence:
// (1) key-based: mask object keys whose name looks secret; (2) value-based: scrub
// token-shaped substrings even under innocent keys or inside free text. Idempotent,
// so the renderer may re-apply it as a safety net for legacy persisted runs.
const SECRET_KEY =
  /(api[-_]?key|token|secret|password|passwd|authorization|bearer|credential|private[-_]?key|client[-_]?secret|session)/i;
const MAX_STRING = 500;
const REDACTED = "[redacted]";

// Token-shaped values, scrubbed in-place so surrounding context survives.
const SECRET_VALUE_PATTERNS: RegExp[] = [
  /sk-[A-Za-z0-9_-]{16,}/g, // OpenAI / Anthropic style keys
  /(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}/g, // GitHub tokens
  /AKIA[0-9A-Z]{16}/g, // AWS access key id
  /eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}/g, // JWT
  /Bearer\s+[A-Za-z0-9._-]{8,}/gi, // Authorization: Bearer …
  /-----BEGIN[A-Z ]*PRIVATE KEY-----[\s\S]*?-----END[A-Z ]*PRIVATE KEY-----/g, // PEM
];

function scrubString(value: string): string {
  let out = value;
  for (const re of SECRET_VALUE_PATTERNS) out = out.replace(re, REDACTED);
  return out.length > MAX_STRING ? `${out.slice(0, MAX_STRING)}… [truncated]` : out;
}

export function sanitize(value: unknown): unknown {
  if (typeof value === "string") return scrubString(value);
  if (Array.isArray(value)) return value.map(sanitize);
  if (value && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value).map(([k, v]) =>
        SECRET_KEY.test(k) ? [k, REDACTED] : [k, sanitize(v)],
      ),
    );
  }
  return value; // numbers, booleans, null, undefined pass through
}

// String-typed convenience for fields that are always strings (e.g. error text).
export function sanitizeText(value: string): string {
  return scrubString(value);
}
```

// src/lib/trace/recorder.ts
```typescript
import type { TraceEvent } from "./types";
import { costFor } from "./pricing";
import { sanitize, sanitizeText } from "./sanitize";

// Narrow structural interfaces — only the fields the recorder reads. Using these
// (instead of the SDK's full generics) avoids the variance mismatch when the
// callbacks are spread into streamText(...), which is parameterised on the tool set.
type StepStartArg = { stepNumber: number };
type ToolCallStartArg = {
  stepNumber: number | undefined;
  toolCall: { toolCallId: string; toolName: string; input: unknown };
};
type ToolCallFinishArg = {
  stepNumber: number | undefined;
  toolCall: { toolCallId: string };
  durationMs: number;
} & ({ success: true; output: unknown } | { success: false; error: unknown });
type StepFinishArg = {
  stepNumber: number;
  usage: { inputTokens?: number; outputTokens?: number; totalTokens?: number };
  finishReason: string;
};

type RecorderOptions = {
  runId: string;
  modelId: string;
  task: string;
  onEvent: (event: TraceEvent) => void;
};

export function createRecorder({ runId, modelId, task, onEvent }: RecorderOptions) {
  const runStartTs = Date.now();
  let totalInputTokens = 0;
  let totalOutputTokens = 0;
  // The SDK does not give step durationMs, so we measure wall-clock here.
  const stepStartTimes = new Map<number, number>();

  onEvent({ type: "run-start", runId, modelId, task, ts: runStartTs });

  // ⇩ The ONLY place the volatile experimental_ names live. Each callback maps
  // its SDK argument to a stable TraceEvent. A rename upstream is a one-line fix.
  const callbacks = {
    experimental_onStepStart: (e: StepStartArg) => {
      const ts = Date.now();
      stepStartTimes.set(e.stepNumber, ts);
      onEvent({ type: "step-start", stepNumber: e.stepNumber, ts });
    },

    experimental_onToolCallStart: (e: ToolCallStartArg) => {
      onEvent({
        type: "tool-call-start",
        stepNumber: e.stepNumber ?? 0,
        toolCallId: e.toolCall.toolCallId,
        toolName: e.toolCall.toolName,
        // Sanitize at the emission boundary — raw input never reaches the
        // stream, store, or IndexedDB. The persisted event is safe-by-construction.
        input: sanitize(e.toolCall.input),
        ts: Date.now(),
      });
    },

    experimental_onToolCallFinish: (e: ToolCallFinishArg) => {
      onEvent({
        type: "tool-call-finish",
        stepNumber: e.stepNumber ?? 0,
        toolCallId: e.toolCall.toolCallId,
        durationMs: e.durationMs,
        ok: e.success,
        output: e.success ? sanitize(e.output) : undefined,
        error: !e.success ? sanitizeText(String(e.error)) : undefined,
        ts: Date.now(),
      });
    },

    onStepFinish: (e: StepFinishArg) => {
      const ts = Date.now();
      const durationMs = ts - (stepStartTimes.get(e.stepNumber) ?? ts);
      stepStartTimes.delete(e.stepNumber);

      const inputTokens = e.usage.inputTokens ?? 0;
      const outputTokens = e.usage.outputTokens ?? 0;
      const totalTokens = e.usage.totalTokens ?? inputTokens + outputTokens;
      totalInputTokens += inputTokens;
      totalOutputTokens += outputTokens;

      onEvent({
        type: "step-finish",
        stepNumber: e.stepNumber,
        durationMs,
        usage: { inputTokens, outputTokens, totalTokens },
        finishReason: e.finishReason,
        ts,
      });
    },
  };

  function finish() {
    const ts = Date.now();
    onEvent({
      type: "run-finish",
      totalDurationMs: ts - runStartTs,
      totalUsage: {
        inputTokens: totalInputTokens,
        outputTokens: totalOutputTokens,
        totalTokens: totalInputTokens + totalOutputTokens,
      },
      // Cost computed once, from the one pricing module.
      costUsd: costFor(modelId, { inputTokens: totalInputTokens, outputTokens: totalOutputTokens }),
      ts,
    });
  }

  return { callbacks, finish };
}
```

// src/app/api/agent/run/route.ts
```typescript
import { streamText, createUIMessageStream, createUIMessageStreamResponse, stepCountIs } from "ai";
import { randomUUID } from "node:crypto";
import { getModel } from "@/lib/ai/get-model";
import { createRecorder } from "@/lib/trace/recorder";
import { serverTools } from "@/lib/tools/registry.server";

export const maxDuration = 60;

export async function POST(req: Request) {
  const { task, modelId } = (await req.json()) as { task: string; modelId: string };

  const stream = createUIMessageStream({
    execute: async ({ writer }) => {
      const runId = randomUUID();
      const recorder = createRecorder({
        runId,
        modelId,
        task,
        // ⇩ One stream, not two: trace events ride the SAME connection as the
        // model text, as custom "data-trace-event" parts.
        onEvent: (event) => writer.write({ type: "data-trace-event", data: event }),
      });

      const result = streamText({
        model: getModel(modelId),
        tools: serverTools,
        stopWhen: stepCountIs(10),
        prompt: task,
        ...recorder.callbacks, // recorder is the only consumer of experimental_ names
      });

      writer.merge(result.toUIMessageStream());
      await result.finishReason;
      recorder.finish(); // emits run-finish (with costUsd) last
    },
  });

  // Response is text/event-stream with header x-vercel-ai-ui-message-stream: v1.
  return createUIMessageStreamResponse({ stream });
}
```

// src/lib/store/run-store.ts — reducer + pure selectors
```typescript
import { create } from "zustand";
import type { TraceEvent } from "@/lib/trace/types";

export type RunStatus = "idle" | "running" | "finished" | "error";

interface RunState {
  runId: string | null;
  status: RunStatus;
  events: TraceEvent[];
  startRun: (input: { task: string; modelId: string }) => void;
  append: (event: TraceEvent) => void; // live path
  reset: () => void;
}

export const useRunStore = create<RunState>((set) => ({
  runId: null,
  status: "idle",
  events: [],
  startRun: () => set({ runId: null, status: "running", events: [] }),
  append: (event) =>
    set((state) => ({
      // Fresh array reference so memoized selectors recompute.
      events: [...state.events, event],
      runId: event.type === "run-start" ? event.runId : state.runId,
      status: event.type === "run-finish" ? "finished" : state.status,
    })),
  reset: () => set({ runId: null, status: "idle", events: [] }),
}));

// --- Pure selectors: the ONLY bridge from the flat log to the view. ---
// No React, no side effects, no Date.now() inside — trivially unit-testable.
export type StepDerivation = {
  stepNumber: number;
  llmStart: number;
  llmEnd: number | null; // null while in flight
  usage: { inputTokens: number; outputTokens: number; totalTokens: number } | null;
  toolCalls: { toolCallId: string; toolName: string; start: number; end: number | null; ok: boolean | null }[];
};

export function deriveSteps(events: TraceEvent[]): StepDerivation[] {
  const byStep = new Map<number, StepDerivation>();
  for (const e of events) {
    if (e.type === "step-start") {
      byStep.set(e.stepNumber, { stepNumber: e.stepNumber, llmStart: e.ts, llmEnd: null, usage: null, toolCalls: [] });
    } else if (e.type === "step-finish") {
      const s = byStep.get(e.stepNumber);
      if (s) { s.llmEnd = e.ts; s.usage = e.usage; }
    } else if (e.type === "tool-call-start") {
      byStep.get(e.stepNumber)?.toolCalls.push({
        toolCallId: e.toolCallId, toolName: e.toolName, start: e.ts, end: null, ok: null,
      });
    } else if (e.type === "tool-call-finish") {
      const tc = byStep.get(e.stepNumber)?.toolCalls.find((t) => t.toolCallId === e.toolCallId);
      if (tc) { tc.end = e.ts; tc.ok = e.ok; }
    }
  }
  return [...byStep.values()].sort((a, b) => a.stepNumber - b.stepNumber);
}

// The x-scale bounds. While running, maxTs is "now" so the timeline grows live.
export function deriveBounds(events: TraceEvent[], nowFallback: number): { minTs: number; maxTs: number } {
  if (events.length === 0) return { minTs: nowFallback, maxTs: nowFallback + 1000 };
  const last = events[events.length - 1];
  const runFinish = events.find((e) => e.type === "run-finish");
  return { minTs: events[0].ts, maxTs: runFinish ? runFinish.ts : Math.max(last.ts, nowFallback) };
}
```

// Client consumption via useChat onData (the only client entry point for events)
```typescript
import { useChat } from "@ai-sdk/react";
import { useRunStore } from "@/lib/store/run-store";

function useAgentRun() {
  const append = useRunStore((s) => s.append);
  return useChat({
    api: "/api/agent/run",
    // Custom data parts arrive here — filter for our trace channel and append.
    onData: (part) => {
      if (part.type === "data-trace-event") append(part.data as never);
    },
  });
}
```

// src/lib/trace/recorder.test.ts — layer 1: the recorder contract
```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { createRecorder } from "./recorder";
import type { TraceEvent } from "./types";

describe("createRecorder", () => {
  let events: TraceEvent[];
  let recorder: ReturnType<typeof createRecorder>;

  beforeEach(() => {
    vi.useFakeTimers();        // deterministic ts
    vi.setSystemTime(1000);
    events = [];
    recorder = createRecorder({ runId: "run-1", modelId: "openai:fast", task: "t", onEvent: (e) => events.push(e) });
  });

  it("emits run-start on construction", () => {
    expect(events[0]).toMatchObject({ type: "run-start", runId: "run-1", ts: 1000 });
  });

  it("maps onStepFinish → step-finish with duration measured from step-start", () => {
    vi.setSystemTime(2000);
    recorder.callbacks.experimental_onStepStart({ stepNumber: 0 });
    vi.setSystemTime(2500);
    recorder.callbacks.onStepFinish({
      stepNumber: 0,
      usage: { inputTokens: 100, outputTokens: 50, totalTokens: 150 },
      finishReason: "tool-calls",
    });
    expect(events.find((e) => e.type === "step-finish")).toMatchObject({ durationMs: 500, finishReason: "tool-calls" });
  });

  it("defaults undefined token counts to 0", () => {
    recorder.callbacks.onStepFinish({ stepNumber: 0, usage: {}, finishReason: "stop" });
    expect(events.find((e) => e.type === "step-finish")).toMatchObject({
      usage: { inputTokens: 0, outputTokens: 0, totalTokens: 0 },
    });
  });
});
```

// Layer 3 sketch: e2e with a mocked SSE stream (exact wire format)
```typescript
// Build a fake text/event-stream response so useChat parses it for real.
function mockTraceStream(events: TraceEvent[]): Response {
  const body = new ReadableStream<Uint8Array>({
    start(controller) {
      const enc = new TextEncoder();
      for (const event of events) {
        const part = { type: "data-trace-event", data: event };
        controller.enqueue(enc.encode(`data: ${JSON.stringify(part)}\n\n`)); // data: <json>\n\n
      }
      controller.enqueue(enc.encode("data: [DONE]\n\n")); // terminator
      controller.close();
    },
  });
  return new Response(body, {
    headers: {
      "Content-Type": "text/event-stream",
      "x-vercel-ai-ui-message-stream": "v1", // required, or useChat won't parse
    },
  });
}
```

## Common mistakes

- **Inventing an ad-hoc event shape outside the union** — emitting `{ kind: "toolDone", ... }` or a bare payload instead of a `TraceEvent` variant breaks the contract and silently bypasses exhaustiveness checks. Every event is a member of `types.ts`.
- **Redacting only at render time** — calling `sanitize()`/`redact()` in the inspector but emitting raw `input`/`output` from the recorder. The redaction boundary is then too late: the raw payload (API keys, bearer tokens, PII) has already been streamed to the client, reduced into the store, and persisted to IndexedDB, where it can be replayed later. Sanitize in the recorder, before `onEvent`, so the persisted `TraceEvent` is safe-by-construction.
- **Letting `experimental_*` names leak past the recorder** — referencing `experimental_onToolCallStart` in the route, store, or a component re-couples the whole app to a name the SDK will rename. It belongs in exactly one module.
- **Opening a second channel for telemetry** — a separate SSE/WebSocket for trace events desyncs ordering against the model text and doubles failure modes. Trace events ride the same `createUIMessageStream` as `data-trace-event` parts.
- **Walking `events[]` directly in a component** — components must go through `deriveSteps` / `deriveBounds`. Inline reduction in the view duplicates logic, can't be unit-tested, and drifts from the store.
- **Putting `Date.now()` or React hooks inside a selector** — selectors must be pure functions of their arguments. Live "now" is passed in as the `nowFallback` parameter to `deriveBounds`, never read inside.
- **Hardcoding a cost or token rate in the UI** — any dollar figure not produced by `costFor(...)` will drift from real pricing. Compute cost once (at `run-finish`) and read `costUsd` off the event.
- **Skipping a step of the 5-step ritual** — adding a union variant but not handling it in the store/selectors, or vice-versa. Keep an exhaustive `switch`/`if-else` with a `never` fallback so the compiler refuses to build until every consumer is updated.
- **Mocking the stream without the exact wire format** — omitting the `\n\n` chunk separator, the `data: [DONE]` terminator, the `text/event-stream` content type, or the `x-vercel-ai-ui-message-stream: v1` header makes `useChat` silently drop events, producing confusing green e2e tests that prove nothing.
- **Measuring step duration from the SDK where it isn't provided** — `onStepFinish` has no duration; the recorder measures wall-clock from the matching `step-start`. (Tool-call finish *does* carry `durationMs` from the SDK — use it directly there.)
- **Forgetting a monotonic `ts` on a new variant** — an event with no `ts` can't be placed on the timeline and breaks `deriveBounds`. Capture `Date.now()` at emit time for every variant.

## How to apply this skill in a new project

1. **Install dependencies** — the AI SDK core, the React binding, and a store:
   ```bash
   pnpm add ai @ai-sdk/react zustand
   pnpm add -D vitest
   ```
   This skill assumes the `src/lib/ai` model layer (registry + `getModel`) from the `ai-model-layer` skill already exists, since pricing and `modelId` are keyed on the `provider:alias` form it produces.

2. **Define the contract first — `src/lib/trace/types.ts`** — write the `TraceEvent` discriminated union with one variant per boundary you want to observe (`run-start`, `step-start`, `tool-call-start`, `tool-call-finish`, `step-finish`, `run-finish` is a solid default set). Give every variant a `type` literal and a `ts: number`. Nothing else in the layer is written until this compiles.

3. **Write `src/lib/trace/pricing.ts`** — a `PRICES` record keyed by `provider:alias`, and `costFor(modelId, usage)` returning USD. Return `0` for unknown IDs. This is the only place rates live.

4. **Write `src/lib/trace/sanitize.ts`** — `sanitize(value)` and `sanitizeText(str)`: mask credential-looking object keys, scrub token-shaped substrings out of strings, truncate runaway strings. Keep it pure and idempotent. This is the single place "what is safe to keep" is decided, and the recorder depends on it.

5. **Write `src/lib/trace/recorder.ts`** — `createRecorder({ runId, modelId, task, onEvent })` returning `{ callbacks, finish }`. Declare narrow structural arg types (not the SDK generics) to avoid the variance mismatch when spreading into `streamText`. Emit `run-start` on construction; map each `experimental_*` / `onStepFinish` callback to a `TraceEvent`, passing tool `input` / `output` / `error` through `sanitize()` / `sanitizeText()` so raw payloads never enter the event stream; accumulate token totals; emit `run-finish` (with `costFor(...)`) from `finish()`. This is the **only** file that names the volatile callbacks.

6. **Write the store — `src/lib/store/run-store.ts`** — a `zustand` store holding `events: TraceEvent[]` and `status`, with `append(event)` spreading into a fresh array (so memoized selectors recompute) and flipping status on `run-start` / `run-finish`. In the same file export the pure selectors `deriveSteps(events)` and `deriveBounds(events, now)`.

7. **Wire the server route — `src/app/api/agent/run/route.ts`** — inside `createUIMessageStream`'s `execute`, build the recorder with `onEvent: (event) => writer.write({ type: "data-trace-event", data: event })`, run `streamText({ ..., ...recorder.callbacks })`, `writer.merge(result.toUIMessageStream())`, `await result.finishReason`, then `recorder.finish()`. Return `createUIMessageStreamResponse({ stream })`.

8. **Consume on the client** — call `useChat({ api: "/api/agent/run", onData })` and in `onData` filter `part.type === "data-trace-event"` then `append(part.data)`. Render the timeline exclusively from `deriveSteps` / `deriveBounds` — never from `events[]` directly.

9. **Add the four test layers**:
   - **Recorder contract** (`recorder.test.ts`): `vi.useFakeTimers()` + `vi.setSystemTime`, drive each callback with a fake arg, assert the emitted `TraceEvent`.
   - **Selector logic**: feed a hand-built event log into `deriveSteps` / `deriveBounds`, assert the derived shape and bounds (including in-flight `null`s).
   - **Sanitizer** (`sanitize.test.ts`): table-test `sanitize()` over credential keys, token-shaped values, nested objects/arrays, truncation, and idempotency. Build token fixtures at runtime (string concatenation) so no literal secret is committed — the secret-guard hook will reject the file otherwise.
   - **End-to-end**: mock a `text/event-stream` `Response` using the exact wire format — `data: <json>\n\n` per chunk, terminated by `data: [DONE]`, with the `x-vercel-ai-ui-message-stream: v1` header — and assert the store reaches the expected final state.

10. **Lock in exhaustiveness** — wherever you switch on `event.type` (store, selectors, renderer), end with `default: { const _exhaustive: never = event; return _exhaustive; }`. Add a `CLAUDE.md` note that adding a `TraceEvent` variant means completing the full 5-step ritual; the `never` assignment is what makes the compiler enforce it.
