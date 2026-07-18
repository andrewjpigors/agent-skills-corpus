---
name: orbit-products
description: Set up, edit, or audit an Orbit Product (a versioned, code-driven logistics offering composed of ProductBricks) end-to-end via the Orbit public REST API — author the four bricks (context, feasibility, pricing, scheduling), emit Product Metrics, wire DataPools, gate it through a TransportShape, write EN+DE marketing copy, and self-verify with the product testing framework and the /products/calculate and /products/{id}/execute endpoints. Use whenever a user wants to create or configure a logistics product or transport offering, edit pricing, add a feasibility or scheduling rule, add distance/duration metrics to an offer, or write product test cases — or mentions ProductBricks, DataPools, or Product Metrics. Also use proactively when someone describes an offering to model in Orbit (e.g. "a same-day Berlin courier for 49€"). Always confirm whether the customer is on the staging or the production environment before any mutating call.
---

# Orbit Product Setup

You are a logistics product architect for Orbit. A user wants to set up, edit, or audit an **Orbit Product** for a tenant. Your job is to take a fuzzy idea ("we want a same-day Berlin courier") and ship a fully working, tested, marketing-ready product on a real tenant — **end-to-end with only an API key, zero Mission UI handoffs**.

This skill carries the deep domain knowledge. The reference files in `references/` are loaded on demand — this top-level file is the workflow and the decision tree.

## The whole workflow runs on the REST API

The entire FULL workflow runs on the public REST API with one `X-API-KEY` header — create the product, create the bricks, soft-save / hard-save, evaluate against drafts, gate the shape, read execution logs. No manual Orbit MissionControl steps are required. The routing table at the top of `references/rest-endpoints.md` lists every endpoint.

Three properties of the workflow are worth internalising up front:

1. **Drafts-first feedback loop using `/products/{id}/execute`.** Build a TransportDraft (`POST /v5/drafts`), then `POST /v5/products/{id}/execute` against it for the full calculator output. The win over `/calculate` is a synchronous full-output response with structured 412 (bad draft) / 422 (`BRICK_RUNTIME_ERROR`) codes, AND every invocation persists logs to the test-run log group (`GET /v5/products/{id}/execution-logs?onlyTestRuns=true`). **Important caveat:** like `/calculate`, `/execute` reads the **last-hard-saved** product version — it does NOT see soft-save state. So on a fresh product you must hard-save the bricks-linked product once before `/execute` produces useful output. See § "FRESH products" in the ordering rules.
2. **`validFrom` is now optional on soft-save.** The server auto-bumps to `max(now, latest.validFrom + 1)`. Omit it. The phantom-future-validFrom race is gone for steady-state edits.
3. **Brick TypeScript is validated server-side at soft-save / create.** Foot-guns (trailing `;`, top-level `const`, missing `satisfies <FnType>`) return HTTP 400 with a one-line plain-English hint. You don't need to soft-save → calculate → read server logs → guess to find a TS error.

## Three log scopes you must keep straight

This is the single highest-value rule in this skill. Get it wrong and you'll waste a debug cycle hitting an empty endpoint.

| Where the log lives | What populates it | How to read it |
| --- | --- | --- |
| **Inline in the response** of `POST /v5/products/{id}/test-cases/run` | Every ProductTestCase run. **Frozen-time** (`simulatedAt`) execution. | `testCaseResults[].logs[]`, `errorMessage`, `errorDetails[]`. **Not anywhere else.** |
| **Test-run log group** (`/test/products/{id}` or `/test/productBricks/{brickId}`) | `POST /v5/products/{id}/execute` and `POST /v5/product-bricks/{brickId}/execute` (operator-UI "Test product" / "Test brick" wrappers) | `GET /v5/products/{id}/execution-logs?onlyTestRuns=true` |
| **Production log group** (`/products/{id}`) | Real wall-clock shipment pricing — every offer evaluated against a real customer transport | `GET /v5/products/{id}/execution-logs?onlyTestRuns=false` (default) |

**The rule that matters:** when a `POST /test-cases/run` returns `status: "error"` or unexpected diffs, **never** reach for `/execution-logs` to debug it. Test-case-run logs are NOT there. They live ONLY in the inline response — `testCaseResults[].logs[]` for the brick's `console.*`, `testCaseResults[].errorMessage` for the unwrapped throw, and `testCaseResults[].errorDetails: { path: string[], message: string }[]` for per-field structured issues (e.g. when the stored `draftSnapshot.transport` doesn't validate against `TransportForProductsSchema`). Prefer `errorDetails[]` over substring-searching `errorMessage` / `logs[].message` whenever it's populated — it tells you which field of the snapshot to patch.

The reason the platform doesn't write test-case-run logs to the persistent log groups: frozen-time logs (where `Date.now()` returns `simulatedAt`) cannot be safely interleaved into wall-clock log streams. The trade-off is that all test-case-run diagnostics must come back in the response.

## What an Orbit Product actually is

A Product is a **versioned, code-driven logistics offering** that answers four questions about a transport request:

1. **Can we do it?** (feasibility)
2. **When?** (scheduling)
3. **For how much?** (pricing)
4. **What does the customer/operator see?** (metadata, messages, marketing copy)

A Product is a metadata wrapper. The actual answers are computed by **ProductBricks** — small TypeScript modules executed inside an isolated server-side sandbox for every transport request. Four brick types exist:

| Brick type    | Cardinality | Returns                                                                      | Purpose                                                                       |
| ------------- | ----------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `context`     | exactly 1   | `ContextFunctionResult` (route, computed values, messages)                   | Runs first. Builds shared context (route, vehicle class) for the other three. |
| `feasibility` | 1..N        | `FeasibilityFunctionResult` (`isFeasible`, optional errors, `isRequestable`) | AND-combined. Decides whether the product is bookable.                        |
| `pricing`     | 0..N        | `LineItem[]`                                                                 | Concatenated. Quotes the price.                                               |
| `scheduling`  | exactly 1   | `Schedule` (stops, options, recommendations)                                 | Builds the SchedulingWizard.                                                  |

**Versioning.** Every edit creates a new version with a `validFrom` epoch second. When a transport is calculated, Orbit fetches the version valid at the transport's start time. Old orders never re-price. **Soft-save now auto-bumps `validFrom` server-side** to `max(now, latest.validFrom + 1)` whenever you omit it (recommended) or pass a stale value. You should omit `validFrom` by default; pass it explicitly only when scheduling a future-effective version.

**TransportShape gating.** Products are not globally bookable. Each `TransportShape` lists which Product IDs operators see in its TransportComposer. The real entity stores this at **`shape.configuration.products.sales.ids`** and **`shape.configuration.products.purchasing.ids`**. You mutate that list with one REST call: `PATCH /v5/transportshapes/{transportShapeId}/products` with body `{add?: string[], remove?: string[], target: "sales" | "purchasing"}`. See `references/rest-endpoints.md` § Gating.

**ProductMessages = BrickMessage.** Context and feasibility bricks can emit `{ level: "info"|"warning"|"error", text: { en, de } }` messages. They surface as alerts in MissionControl and Hub. They do **not** gate booking — only `isFeasible` does.

**Three availability states the frontend renders very differently.** The combination of `isFeasible`, `lineItems`, and `isRequestable` collapses into one of:

- **offer** (`isFeasible: true` + non-empty `lineItems`) — directly bookable. Customer sees the price and "Book now".
- **request** (`isFeasible: false` OR no pricing, with `isRequestable: true`) — "price on request" mode. Customer sees `requestCTAConfig` and can submit a request manually.
- **unavailable** (`isRequestable: false`) — hidden in Hub; greyed-out in TransportComposer with whatever BrickMessages explain why.

Most-restrictive `isRequestable` wins across feasibility bricks. `Product.isRequestable` is the default; bricks override it per-request. **Always emit a BrickMessage when you flip `isFeasible: false`** — without one, operators see a greyed product with no explanation. See `references/product-anatomy.md` § Availability states for the full matrix and the implications for the `mustBeFeasible` filter on TransportShape.

**Product Metrics = display badges.** Any brick can emit `metrics: [{ title: { en, de }, value: string }]` — display-only annotations (canonically **Distance** and **Duration**) that surface on the Offer, on the Order, and on the product card in the TransportComposer. They don't affect feasibility or pricing, carry no icon, and are merged last-wins by `title` across the four bricks. Pricing and scheduling bricks switch from their bare return (`LineItem[]` / `Schedule`) to the object form (`{ lineItems, metrics }` / `{ schedule, metrics }`) to emit them; context/feasibility just add an optional `metrics` field. They're readable only inside `Offer.metrics` (no dedicated endpoint) and are **not** asserted by ProductTestCases. See `references/product-anatomy.md` § Product Metrics.

**Source attribution.** Products and ProductBricks created via REST (API key) are stamped with `source: { type: "api-key", apiKeyName }`, so audit trails name the key, not a phantom user.

For the full anatomy (entities, fields, indexes, lifecycle), read `references/product-anatomy.md`.

## End-to-end recipe — copy-paste reference

This is the new shape of FULL workflow on REST. Read it once. Each step has a one-line "what" and a curl shape; the deeper notes are in `references/rest-endpoints.md`.

```bash
KEY="…"; STAGE="staging"; BASE="https://api.${STAGE}.orbit.do/v5"
H='-H "X-API-KEY: $KEY" -H "Content-Type: application/json"'

# 1. CREATE product (API-key auth) → returns { id, validFrom }
curl -X POST "$BASE/products" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d @product-create.json
# product-create.json minimal body — required: name, description, type, status, productBricks, bulletPoints, isRequestable
# (see references/rest-endpoints.md § "POST /products" for the example payload that's also published in the OpenAPI spec)

# 2. CREATE bricks — one POST per brick slot you need (context + 1..N feasibility + 0..N pricing + scheduling)
curl -X POST "$BASE/product-bricks" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"type":"context","name":"Berlin courier context","description":"Vehicle + route","payload":"","dataPools":[]}'
# `dataPools: []` is REQUIRED even when the brick uses no DataPools — Zod rejects the
# request with HTTP 400 if the key is missing.

# 3. SOFT-SAVE each brick with its real TS payload (omit validFrom — server auto-bumps)
jq -Rs --arg id "$BRICK_ID" '{productBrickId: $id, request: {name: "...", description: "...", status: "active", payload: ., dataPools: []}}' \
  brick-context.ts | curl -X POST "$BASE/soft-save/product-bricks" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d @-
# Response: { sessionToken, summary: { totalTests, passed, failed, errored }, products: [...], hasExecutionErrors }

# 4. SOFT-SAVE the product, linking the bricks via productBricks[]
curl -X POST "$BASE/soft-save/products" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"productId":"'"$PROD"'","request":{"productBricks":["'"$CTX"'","'"$FEAS"'","'"$PRC"'","'"$SCH"'"], …}}'

# 5. HARD-SAVE bricks + product so the brick links go live (required before /execute will see them).
#    /execute reads the LAST-HARD-SAVED product, not the soft-save's pending state.
#    keepTestCaseIds=[] is correct here — there are no test cases yet.
curl -X POST "$BASE/hard-save/product-bricks" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"sessionToken":"'"$BRICK_TKN"'","keepTestCaseIds":[]}'
curl -X POST "$BASE/hard-save/products" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"sessionToken":"'"$PROD_TKN"'","keepTestCaseIds":[]}'
# Each response carries entity.validFrom — the server-resolved one. Note it; you'll need it for
# /products/{id}/{validFrom} reads and for picking simulatedAt later.

# 6. CREATE a TransportDraft to feed /execute. Required body fields: type, status, shapeId, transport.
curl -X POST "$BASE/drafts" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"type":"manual","status":"draft","shapeId":"'"$SHAPE"'","transport":'"$TRANSPORT_JSON"'}'
# Reuse calculate-helpers.mjs' buildTransport() output as the `transport` field — byte-identical to TransportForProductsSchema.

# 7. EXECUTE the product against the draft → full calculator output (context/feasibility/pricing/scheduling)
curl -X POST "$BASE/products/$PROD/execute" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"transportDraftId":"'"$DRAFT"'"}'
# 412 = patch the draft (message starts "TransportForProductsSchema parse failed:")
# 422 with internalCode "BRICK_RUNTIME_ERROR" = fix the brick payload, soft-save AND hard-save again
# 200 = read the offer; iterate brick TS (soft-save → hard-save → /execute) until shape is right
# Logs persisted in test-run log group, fetch via GET /products/$PROD/execution-logs?onlyTestRuns=true

# 8. CAPTURE 2-4 ProductTestCases (after /execute output looks right). simulatedAt MUST be ≥ product.validFrom.
curl -X POST "$BASE/products/$PROD/test-cases" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d @testcase.json
# Response includes a non-blocking validationWarnings: DraftSnapshotValidationWarning[]. Empty = clean. Non-empty = patch the snapshot before /run.

# 9. RUN the cohort. All diagnostics are inline; do NOT reach for /execution-logs to debug failures.
curl -X POST "$BASE/products/$PROD/test-cases/run" -H "X-API-KEY: $KEY"

# 10. (If you iterated brick TS in step 7) HARD-SAVE the new versions, passing every current cohort id in keepTestCaseIds.
#     Response gives you newTestCaseIds — your previous IDs are now archived.
curl -X POST "$BASE/hard-save/product-bricks" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"sessionToken":"'"$TKN"'","keepTestCaseIds":["'"$TC1"'","'"$TC2"'","'"$TC3"'"]}'
# Response: { saved, entityType, testCasesCreated, testCasesDeleted, newTestCaseIds, entity }
# IMPORTANT: the IDs you sent in keepTestCaseIds are now archived — the FRESH ids are in newTestCaseIds.

# 11. GATE the product on a TransportShape (no Mission UI; pure REST)
curl -X PATCH "$BASE/transportshapes/$SHAPE/products" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"add":["'"$PROD"'"],"target":"sales"}'
```

That's the full happy path. The numbered workflow below carries the *judgment* you need to apply between the curls — when to interview, when to inspect, when to ask the user, when to retry, when to surface as OPEN.

## The default workflow

Run this loop end-to-end. **Test cases are not a quality net — they are the deliverable.** A product without 3+ green ProductTestCases is incomplete; the test cases are the customer's acceptance contract and the regression net every future operator (and every soft-save) leans on. Treat them as central from the spec interview onwards, not as the last step.

```text
1. CLARIFY      → spec the product (interview if fuzzy) — INCL. drafting 3-6 acceptance test
                  scenario NAMES + outcomes during the interview (Block 7). They go into the
                  spec doc as § 6 BEFORE any brick code is written.
2. STRUCTURE    → decide bricks, DataPools, TransportShape gating
3. CREATE       → POST /v5/products → {id, validFrom}; one POST /v5/product-bricks per brick slot
                  needed → {id, validFrom}. The agent manifests every shell over REST. (No Mission UI.)
4. AUTHOR       → draft brick TypeScript locally + metadata + EN/DE copy
5. SOFT-SAVE    → soft-save bricks (omit validFrom, server auto-bumps) → soft-save product
                  (this runs all existing tests; for a fresh product the test summary will
                  be empty until step 7)
6. HARD-SAVE 1  → **For FRESH products only.** Hard-save bricks + product so the brick links
                  go live. `/execute` and `/test-cases/run` both read last-hard-saved state.
                  Pass `keepTestCaseIds: []` (no cases yet). For EDITS to an existing product,
                  skip this step — proceed straight to step 7 with the soft-save token open.
7. EXECUTE      → POST /v5/drafts (body: {type, status, shapeId, transport}) →
                  POST /v5/products/{id}/execute against the draft. Full calculator output,
                  412/422 on bad input. Iterate brick TS by re-soft-saving AND re-hard-saving
                  (because /execute reads last-hard-saved). For EDITS, /execute will show the
                  current LIVE behaviour — to preview the pending edit, read the soft-save
                  response's summary + testCaseResults instead.
8. CAPTURE      → transcribe the agreed acceptance scenarios from spec § 6 into ProductTestCases
                  (POST /v5/products/{id}/test-cases). simulatedAt MUST be ≥ product.validFrom
                  (use the server-resolved value from the hard-save response, plus a buffer).
                  Inspect validationWarnings[] in each create response — empty means the
                  snapshot will validate at /run time.
9. RUN          → /test-cases/run; iterate to green using inline logs[] / errorDetails[]
                  (NOT /execution-logs).
10. HARD-SAVE 2 → For EDIT mode, or any further iteration in FRESH-product mode, hard-save the
                  current soft-save with keepTestCaseIds populated. **The keepTestCaseIds you
                  send are archived; use the newTestCaseIds in the response for any follow-up
                  call.** (Hard-save does NOT re-run tests — soft-save was the gate.)
11. GATE        → PATCH /v5/transportshapes/{id}/products with {add: [productId], target: "sales"|"purchasing"}.
                  For Hub: also add to Shop.offeredProducts (still tRPC-only — see step note).
12. SUMMARIZE   → report what was built. **HARD GATE: do not declare done unless ≥ 3 green
                  ProductTestCases exist (1 happy + 1 boundary + 1 infeasibility minimum).**
                  If the user wants to ship anyway, surface it as an explicit OPEN item with
                  a one-line "Ship-anyway override accepted by user on [date]" note.
```

**Three ordering rules that catch agents off-guard — internalize them:**

- **`/execute` and `/calculate` BOTH read last-hard-saved.** Neither sees your pending soft-save state — `executeProductTest` resolves the product version via `getCurrentEpochSeconds()` and reads the live entity, just like calculate does. Earlier drafts of this skill claimed `/execute` was the magic way to test soft-save state without hard-saving; that was wrong. The win of `/execute` over `/calculate` is the synchronous full-output response, the structured 412 / 422 envelopes, and the persistent test-run logs (`GET /v5/products/{id}/execution-logs?onlyTestRuns=true`) — NOT pending-state visibility.
- **For product EDITS: the soft-save response is the pre-commit gate.** Since `/execute` and `/calculate` read live state, the only pre-commit signal you have for an edit is the soft-save response itself: inspect `summary` + `products[].testCaseResults` and gate hard-save on those. Use `/execute` afterwards (or `/calculate`) to confirm the change landed live, but don't expect either to preview pending changes.
- **For FRESH products: hard-save the bricks-linked product BEFORE you /execute.** A new product's first `/execute` call against the empty-bricks shell returns `422 BRICK_RUNTIME_ERROR` ("Resolved scheduling brick IDs at this time: []") because soft-save state isn't visible. The fix is mechanical: hard-save once at step 6 with `keepTestCaseIds: []`, then `/execute` works against the now-live brick links. If you iterate on brick TS afterwards, you must soft-save AND hard-save again (with the current cohort in `keepTestCaseIds`) for each round.
- **Soft-save runs tests; hard-save does NOT.** Soft-save executes every existing ProductTestCase against the pending payload and returns the diffs in `summary` + `products[].testCaseResults`. Hard-save just commits the pending payload and rotates the test cohort (every kept test case archived, fresh row minted — see `newTestCaseIds`). If you skip soft-save inspection and jump to hard-save with `keepTestCaseIds`, you've shipped untested. Inspect the soft-save response. Always.

**One more sharp edge — debugging crashed bricks at /products/calculate.** Calculate returns `type: "unavailable"` with NO `feasibility`/`brickMessages`/`lineItems` fields when bricks crash inside the runner. The error is written to the execution logs but is invisible at the calculate API surface. Two faster paths: (a) `/execute` against a draft surfaces 422 with `internalCode: "BRICK_RUNTIME_ERROR"` and the unwrapped message, (b) the test-case `/run` flow returns it inline as `errorMessage` + `logs[]` ending with an `error`-level entry. Reach for /execute or /run before the raw execution logs. See `references/operations.md` § "Debugging brick crashes".

## EDIT mode — the fast path for established products

The 11-step workflow above is correct for greenfield work. For most edits to an already-shipped product (bump a fuel floater, raise a per-km rate, fix a typo in marketing copy, add one feasibility rule), it's overkill. Established tenants version the same product dozens of times — a mature product routinely accumulates 18+ versions with its pricing brick edited many times over. Forcing those flows through CLARIFY → STRUCTURE → CREATE → 3-test-gate is friction the customer doesn't want and won't tolerate.

Use this 7-step EDIT mode when **all** of the following are true:

- The product (and the brick(s) you're touching) already exist on the target stage.
- The change is scoped: a value, a rule, a copy fix — not a structural change.
- You're not adding a new brick to the product or changing its TransportShape gating.

```text
E1. READ          → fetch the current latest version (GET /v5/products/{id}/{validAt} +
                    GET /v5/product-bricks/{brickId}/{validAt}).
                    Show the user the current value of what they're changing.
E2. SHOW-DIFF     → present current → intended side-by-side. Ask the user to confirm
                    the diff before any mutation.
E3. SOFT-SAVE     → soft-save the changed entity. Omit validFrom (server auto-bumps).
                    Paste `summary` + `testCaseResults` inline. Note the sessionToken.
E4. EXECUTE       → 1-2 /execute calls (or /calculate, if the change is reflected in
                    last-hard-saved already) hitting the dimension that changed.
E5. TEST-OFFER    → if existing test cases, ask which to keep / promote / drop.
                    If the cohort is empty (the common case for established tenants),
                    you must EXPLICITLY RECOMMEND capturing one regression test for
                    this change — same posture as BrickMessages. Ask the user with
                    "capture the test" as the recommended option (label it so).
                    Skip ONLY if the user actively declines. An empty cohort is not
                    the steady state — every E5 is a chance to start it; don't shrug
                    past it. Don't silently invent tests if the user says no.
E6. HARD-SAVE     → consume the sessionToken. keepTestCaseIds = whatever survived E5.
                    **The IDs you send are archived; the response's newTestCaseIds are
                    the live cohort going forward.** For prod, see Safety below.
E7. SUMMARIZE     → product/brick id, new validFrom (returned from server), what changed
                    in one line, OPEN items if any. If you carried test cases over, list
                    the new IDs so the user can run /test-cases/run on the right cohort.
```

Skip CLARIFY, STRUCTURE, CREATE, GATE entirely. **Re-route to the FULL workflow** the moment the user wants to add a new brick, change the TransportShape, or change `productBricks[]` on the product itself — those changes ripple far enough that the full workflow earns its weight back.

The "≥ 3 green test cases" hard gate at step 11 of the FULL workflow does **not** apply in EDIT mode. The contract there is: "the test cohort that existed before the edit is still green (or the user explicitly accepted the new ground truth)." If the cohort was empty before the edit AND the user explicitly declined E5's recommendation, it's empty after — that's the tenant's choice. But don't pre-decline for them: the agent's job in E5 is to recommend the test and only skip on explicit user refusal.

## VERIFY mode — same-spec re-attestation

The third workflow path. Use it when the user wants to re-confirm that a deployed product still behaves as specified — no edit, no change, no mutation. Typical phrasings: "is product X still working?", "re-run the cohort against Y", "before the demo, double-check the spec on Z", "has the EU Standard Freight product drifted?".

Pick VERIFY when **all** of the following hold:

- The product (and its bricks) already exist on the target stage and the spec is **unchanged** from the user's perspective.
- A test cohort exists for the product, OR the user just wants the deployed bricks read back so they can confirm the spec by eye.
- No code change, payload edit, or shape gating change is on the table.

Three steps, all read-only:

```text
V1. READ          → GET /v5/products/{id}/{validAt} for the latest product version. Then
                    GET /v5/product-bricks/{brickId}/{validAt} for each id in productBricks[].
                    Print: product name, validFrom, list of (brick id, type, name, validFrom,
                    payload one-liner). Confirm the spec the user assumed matches what's
                    encoded — they'll tell you if the rule they think is there isn't.
V2. RUN           → `POST /products/{productId}/test-cases/run`. Paste the cohort result
                    inline: per-case status, any diffs, errored cases. If the cohort is
                    empty, surface that explicitly ("0 cases — only V1 readback gives
                    signal here") and offer to add a starter case via FULL Step 7 if the
                    user wants forward coverage. Don't bootstrap silently.
V3. SUMMARIZE     → one line: "spec unchanged on {stage}/{tenant}, product {id} v{validFrom}
                    re-attested at {epoch}; {n}/{total} cases passing, {failed} OPEN".
                    Plus the verbatim diffs / errored-case error messages if any. No
                    OPEN items beyond what V2 surfaced. No further mutation.
```

VERIFY is **read-only by design** — no soft-save, no calculate-and-mutate, no hard-save, no shape edits. The cohort run mutates archived `cohortTimestamp`s as a side-effect of normal cohort lifecycle (the test-case runner is read-only at the brick / product level), but never the product or brick versions themselves. If during V1 readback you spot drift the user didn't expect, **stop** and surface it — at that point the user is no longer in VERIFY mode, they're in EDIT mode, and the right next step is to re-route through the EDIT-mode E2 SHOW-DIFF gate.

**Production safety.** V2 runs the cohort against `production` (or any stage) the same way Decision-shortcuts row "Run all tests for product P" already does. The Safety rule "never run test cases against production without explicit user confirmation per session" applies — confirm once at the top of the session, then VERIFY can re-run cohorts without re-asking on every call.

## Driving this task reliably

Product setup is a 30-60 minute task with persistent state (a session token, a brick ID, an in-flight test result). If your context gets summarised/compacted mid-task, that state can be lost. Use these habits so the work survives.

**1. Keep a running checklist up front.** As soon as the user's intent is clear (after the spec interview if needed), write down the workflow steps as a checklist and mark each done as you go — mark one in progress when you start it, done the moment it's finished, never batch. The numbered list above is your template — 9 to 11 steps:

- Spec interview & sign-off
- Structure: brick split + DataPool + TransportShape decisions
- Create product + brick shells via REST
- Author brick TS payloads
- Soft-save bricks + product, inspect test summary
- Drafts-first /execute sanity (3 synthetic transports)
- Capture 2-4 ProductTestCases and run them
- Iterate to green (fix / remove-assertion / review-flow)
- Hard-save (note newTestCaseIds for follow-ups)
- Gate via PATCH /transportshapes/{id}/products (+ Shop.offeredProducts if Hub)
- Final summary report to user

Skip the spec-interview step if the user came in with a clean spec. Skip the gate step if it's an edit to an already-gated product. Other than that, the recipe is fixed.

**2. Preflight checks before the first mutation.** Ask the user to confirm — once per session, not once per request:

- **Environment** (`staging` or `production`) — never assume `production`. The base URL is `https://api.{stage}.orbit.do/v5`. A staging key against production (or the reverse) fails, and a production run mutates revenue-bearing config, so confirm this first.
- **Tenant** — ask which tenant; never assume one. The API key is bound to one tenant and one environment.
- **API key** — ask for it; it goes in the `X-API-KEY` header (a literal value, not a `Bearer` token) on every call. Treat it as a secret: never write it to a saved file, never print it back.
- **Brand-new product, or edit?** EDIT mode short-circuits steps 3-4.

Ask for these together as one focused, structured question with the concrete options when any are unknown. Don't drip-feed.

**3. Ask focused, structured questions — not free-text walls.** When you need a decision, present the concrete options, one decision at a time, so the user has a fast pick and you get a recorded answer. Use this for:

- The spec interview (one question or small group per turn).
- Branch decisions ("the user has a 'price-on-request' rule — should this product use isRequestable mode?").
- Anything where the user has 2-4 discrete options and you want a recorded answer.

Present the options rather than asking an open-ended question — it gives the user a faster choice and gives you a cleaner record.

**4. After every soft-save, paste the response summary inline.** The single highest-leverage habit. The summary is small (`{ totalTests, passed, failed, errored, sessionToken }`). Print it to the user before announcing what you'll do next. This prevents the "I hard-saved with red tests" failure mode and gives the user a chance to intervene if the diff doesn't match what they expected.

**5. After every hard-save, surface `newTestCaseIds` to the user.** Same logic as the soft-save response. Hard-save responds with `{ saved, entityType, testCasesCreated, testCasesDeleted, newTestCaseIds, entity }`. The IDs you sent in `keepTestCaseIds` are now archived against the previous version; any subsequent `/test-cases/run` or `/test-cases/{id}` call **must** use the new IDs. Print them inline so the user knows they exist and so you have them in your transcript when context compacts.

**6. Use the OpenAPI spec as a body-shape oracle.** `GET https://api.{stage}.orbit.do/v5/doc` returns the live published spec. Several endpoints (notably `POST /products`) ship a copy-pasteable `example` payload that's the canonical "minimal valid body" — fetch and read it when you're not sure what's required vs optional. The spec is generated from the same Zod schemas the runtime enforces; if your body doesn't match, the spec is the source of truth.

**7. Every read you need has a REST endpoint.** Product, brick, DataPool, test cases, drafts, and transport shapes all read over REST (`GET /v5/products/{id}/{validAt}`, `GET /v5/product-bricks/{id}/{validAt}`, `GET /v5/transportshapes`, etc.). One gap to know: the public API has **no "list all products of a tenant" endpoint** — track the product IDs you create, or discover them through the TransportShape that gates them (`shape.configuration.products.sales.ids`).

**8. Make manual handoffs easy to paste.** The only remaining hand-paste case in the new workflow is when a tenant requires Hub gating via `Shop.offeredProducts` (still tRPC-only). For that and any other rare manual paste, copy the value to the clipboard, or present it clearly, so the user can paste it into the target field — announce which field it goes into. Never make the user manually select it out of a wall of chat. For example, the value to hand off:

```text
{ "productIds": ["..."] }
```

**9. End with a final checklist sweep.** Before sending the summary, verify every checklist item is marked done. Items still in progress mean you missed a step.

## Step 1 — Clarify the spec

If the user already has a clean spec (name, who books it, feasibility rules, pricing model, scheduling, EN+DE copy) — skip to Step 2.

If the spec is fuzzy ("we want to offer same-day Berlin"), run the **product spec interview** documented in `references/interview-script.md`. The interview:

- Detects user's language (EN or DE) and uses formal `Sie/Ihr` in German (operator/shipper-facing copy is always formal; the informal `du` is only for the driver app).
- Asks 1-3 focused, structured questions per turn — never a wall of questions. Every probe is in plain language with a concrete example (no feature names).
- Walks seven blocks: **Identity → Feasibility → Scheduling → Pricing → Inclusions → Capability radar → Test ledger sign-off**.
- Maintains a **running test ledger** — every brick-affecting answer (feasibility rule, pricing component, isRequestable per-rule decision, BrickMessage spec) auto-derives a ProductTestCase row. After each block, the agent prints what it understood + the rows the block added + the manual-UAT items it added.
- Distinguishes **on-platform tests** (lineItems + feasibility — asserted by `POST /products/{id}/test-cases/run`) from **manual UAT** (audience-filter visibility, scheduling-wizard appearance, marketing copy, Hub storefront — these can't be expressed as ProductTestCases).
- Surfaces "this sounds like two products" when the user says "depends".
- Ends with three artifacts presented inline: (1) the markdown spec doc, (2) the test ledger as a markdown table, (3) the manual-UAT checklist. The customer signs off on **all three** as the v1 contract before any code is written.

Always pause for sign-off on the spec + ledger + UAT list before authoring code. The ledger rows become your work-list at Step 7 (capture ProductTestCases).

## Step 2 — Structure: bricks, DataPools, shape

Before writing TypeScript, decide:

- **Brick split.** A common shape: 1 context (route + vehicle class), 1-3 feasibility bricks (one per concern: distance/weight/region/dangerous-goods), 1-2 pricing bricks (base + surcharges), 1 scheduling. **Resist the urge to put everything in one feasibility brick** — splitting per concern lets operators reuse bricks across products and lets feasibility errors point at the actual rule.
- **DataPool needs.** Anything the operator might want to tweak without redeploying code → DataPool. Common: `pricePerKm`, fuel adjustments, zone tables, carrier rate cards, region/postcode lists. If the value is constant in code, leave it in code. If it's a table the operator should edit, it's a DataPool. DataPools have REST for both first-version create and subsequent edits (`POST /v5/soft-save/data-pools` + `POST /v5/hard-save/data-pools`) — you can author them programmatically alongside the bricks. See `references/product-anatomy.md` § DataPools and `references/rest-endpoints.md` § DataPool create / edit body shape.
- **TransportShape.** Which existing shape(s) should expose this product? Sales (Hub bookings, customer-facing) vs purchasing (Tour creation, carrier-facing) vs both. Use `GET /v5/transportshapes` to list all shapes for the tenant when picking. If unclear, ask the user with the concrete shape options.

### Brick-slot accounting — a sanity check, not a hard gate anymore

The old skill warned that the REST `/soft-save/product-bricks` flow could only edit existing brick rows, and that fresh shells had to be created via Mission UI. **That's no longer true.** `POST /v5/product-bricks` creates an empty brick of a given type with API-key auth. The agent manifests every shell it needs.

What's still worth doing before AUTHOR:

1. If you're adding bricks to an existing product, fetch the current `productBricks[]` (via `GET /v5/products/{id}/{validAt}`) and read each brick's `type` so you don't accidentally re-create shells you already have.
2. Tabulate the brick split you intend to ship: e.g. "1 context, 2 feasibility, 1 pricing, 1 scheduling — 5 shells total".
3. POST one create call per shell that doesn't already exist. Save the returned `id` and `validFrom` for step 5.

The "STOP — slot deficit" branch from the old skill is gone. The only reason to halt before AUTHOR now is if the user explicitly asked to reuse a specific existing brick whose `type` doesn't match the slot you need — and brick `type` is immutable, so that's a re-scope conversation with the user, not a Mission UI handoff.

Confirm the structure with the user before authoring code — this is where wrong assumptions cost the most.

## Step 3 — Create product + brick shells (REST)

```bash
# Product (returns { id, validFrom })
curl -X POST "$BASE/products" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d @product-create.json

# Brick shells — one POST per shell. payload can be empty at create time; it's filled in via soft-save at step 5.
curl -X POST "$BASE/product-bricks" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"type":"context","name":"… context","description":"… ≥3 chars","payload":"","dataPools":[]}'
# `dataPools: []` is REQUIRED even when the brick uses no DataPools.
```

The minimal `POST /products` body is `{ name, description, type, status, productBricks, bulletPoints, isRequestable }` (all required). `bulletPoints` accepts `[]`. `productBricks` accepts `[]` at create-time — you'll fill it in at step 5 once the brick shells exist. The OpenAPI spec ships a copy-pasteable `example` you can crib from; fetch it via `GET /v5/doc` if you're not sure of the shape.

The agent's `source` is auto-stamped as `{ type: "api-key", apiKeyName }` — audit trails attribute creates to the key.

## Step 4 — Author the bricks

Each brick is an `async (utils, input, data, context?) => …` function with a strict signature. Bricks **cannot use `import` or `require`** — every utility comes through the injected `utils` object. Time is frozen to `validAt` during execution.

Read `references/brick-authoring.md` for:

- Exact signatures and return shapes for each of the four brick types.
- The complete `utils` API (route, dataPools, loads, scheduling, dateTime, conversions, tools.z).
- The `input` shape (`ProductRequest`: tour stops, loads, shipper, carrier, properties).
- How to safely consume the `context.result` object from feasibility/pricing/scheduling.
- Worked examples for each brick type, including the LineItem shape and the Schedule + Recommendations shape.

When drafting bricks:

- **Always emit BrickMessages on infeasibility.** A `feasibility` brick that returns `{ isFeasible: false }` with no `errors` field is a bad brick — operators won't know why. Use `messages: [{ level: "warning", text: { en: "…", de: "…" } }]` for soft signals and `errors` for hard rejections.
- **Use SchedulingWizard recommendations.** The `recommendations` array on `Schedule` gives operators one-click presets ("pickup today, delivery tomorrow", "next available slot") — the single biggest UX lever in the SchedulingWizard. Like BrickMessages, this is a relatively recent feature that production tenants currently under-use, and the skill keeps nudging it. If the spec lists named presets, encode them. If the spec is silent, **propose** recommendations to the user during Step 1 (interview) rather than defaulting to none. The bar to ship without recommendations is "the user explicitly said no", not "the user didn't bring them up". See `references/brick-authoring.md` § Scheduling.
- **Default scheduling to operating hours from the spec, not hardcoded.** If the spec says 7-18, encode it. If the spec is silent, ask the user for the operating hours.
- **For multi-stop products with recommendations or `timewindow-fixed` options, READ `references/multistopp-scheduling.md` FIRST.** The kit has several non-obvious behaviours around transit anchoring, intra-day constraints, `maxRuntime` caps, and silent preset-dropping that will eat 4-5 publish→test→fail cycles if you don't internalise them upfront. The file documents 9 kit gotchas (with file paths + line numbers), 7 brick coding rules (M1–M7), a working brick template, and a pre-publish verification recipe.

### Brick TypeScript validation happens server-side at soft-save / create

`POST /v5/product-bricks` and `POST /v5/soft-save/product-bricks` run your `payload` through a real `ts.createProgram` against the runtime types bundle (`runtime-types.generated.d.ts`) before persisting. Three foot-guns are short-circuited with one-line plain-English hints:

| Foot-gun | Hint you'll get back (HTTP 400, `internalCode: "BRICK_PAYLOAD_INVALID"`) |
| --- | --- |
| Payload ends with `;` | "Brick payload must be a single TypeScript expression — the server wraps it in `const __brick: <FnType> = ( <YOUR PAYLOAD> );`. A trailing `;` becomes a parse error. Remove the final `;`." |
| Payload starts with `const`/`let`/`var` | "Brick payload must be a single TypeScript expression, not a statement. Inline the function as an arrow expression: `(async (utils, input, data) => { … }) satisfies <FnType>`." |
| TS implicit-any errors with no `satisfies <FnType>` clause | "Append `satisfies <FnType>` so the function type attaches directly: `(async (utils, input, data) => { … }) satisfies <FnType>`." |

For other compile errors you get an array of `details: [{ line, column, message }]` mapped back to your payload's coordinates. There's a 200KB byte cap (`internalCode: "BRICK_PAYLOAD_TOO_LARGE"`) and a 3s validation timeout (`internalCode: "BRICK_PAYLOAD_TIMEOUT"`).

**Caveat — `satisfies <FnType>` only fixes implicit-any on the OUTER arrow's parameters.** Nested closures inside your brick (`stops.map((stop) => …)`, `loads.filter((load) => …)`) don't inherit the contextual type. If TS flags `Parameter 'stop' implicitly has an 'any' type` on a nested closure, **annotate the closure inline**: `stops.map((stop: { address: { zipCode: string } }) => …)` or extract a typed local. The validator runs under `strict: true`, so any implicit-any in any closure is a hard error. **But don't over-annotate** — if the closure operates on a Zod-derived or branded type and you're not sure of the exact shape, leaving it un-annotated may let contextual typing recover (the outer `satisfies` propagates one level down for single-call closures). A wrong inline annotation produces a stricter error than no annotation at all. Try the bare form first; reach for the inline type only if TS still complains.

**Caveat — `context` typing in feasibility / pricing / scheduling bricks.** The injected `context` parameter is typed as `ProductFunctionContext`, which doesn't expose tenant-specific fields you may have stashed there from the context brick (`distanceMeters`, `durationSeconds`, computed route metadata). The two pragmatic options: (a) cast at the read site — `(context as any)?.distanceMeters` — and let the runtime trust the upstream brick, or (b) introduce a typed local once at the top of the brick: `const ctx = context as { distanceMeters?: number; durationSeconds?: number; }`. The skill prefers (b) because it scopes the cast to one line. Both pass server validation; both rely on you keeping the context brick's output shape in sync with what downstream bricks read.

The wrapper the validator uses is:

```ts
const __brick: <FnType> = (
  <YOUR PAYLOAD>
);
```

Where `<FnType>` is one of `ContextFunction` / `FeasibilityFunction` / `PricingFunction` / `ScheduleFunction` per the brick's `type`. Knowing the wrapper is the key to reading the error messages — most TS errors fire because your payload, when wrapped, isn't a valid expression in that position.

This validator replaces the old "soft-save succeeds, calculate runs the bad TS, you dig through the execution logs to find the line number" loop. A single REST 400 with structured details now does the job.

### Permissive-default audit — before SOFT-SAVE

Several Product fields default to maximally permissive values when left unset, and several brick types silently consume them. The combination is a trap: the Mission UI shows the field as cosmetic, the brick code reads it as load-bearing, and the operator finds out only when bookings persist with all-day windows or weekend pickups. Catch this before soft-save.

For each brick payload you've drafted, grep for references to `input.product.<field>`. For every match where `<field>` is one of the four below AND the Product currently has the field at its wide-open default, ask the user to confirm the value (present the concrete options) before continuing — pre-fill from the spec doc's Block 3 (Scheduling) answers when the spec interview ran.

| Field                          | Permissive default                | Risk if defaulted but read by a brick                                                                                       |
| ------------------------------ | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `Product.operatingHours`       | `{ from: 00:00:00, to: 23:59:59 }` | Scheduling brick that does `timewindowFixed: input.product.operatingHours` persists every Shipment with an all-day window. |
| `Product.disabledWeekdays`     | `[]` (every day enabled)          | Scheduling brick that filters by `input.product.disabledWeekdays` allows bookings on weekends/holidays the operator meant to block. |
| `Product.isRequestable`        | `true`                            | Feasibility brick that returns `isFeasible: false` falls silently to "request" mode rather than "unavailable" when the operator wanted hard rejection. |
| `Product.requestCTAConfig`     | empty                             | If the product can fall to request mode (above) and this is empty, the customer sees a blank "Anfragen" CTA. |

A representative failure: a multi-stop product created as a copy of a sibling where `operatingHours` was set, but the spinoff had it left at default. The scheduling brick silently inherited 00:00–23:59. Every multi-stop booking persisted with an all-day window; carrier-assignment emails promised "anytime that day" instead of the operator's intended 08–16. No validation anywhere along the brick → wizard → schedule-selection → submission → Shipment chain caught it.

Skip the audit only when the brick payload genuinely doesn't reference the field (no `input.product.operatingHours` anywhere → don't ask). The audit's job is to couple the prompt to actual blast radius, not to lecture the user about every wide-open default.

Marketing metadata (name, description, bulletPoints, requestCTAConfig, otherOfferSelectedText) is bilingual EN+DE. Read `references/marketing-copy.md` for tone, length, and the Title-Case-EN / sentence-case-DE convention.

## Step 5 — Soft-save (pending state, runs tests, omit validFrom)

The control plane is **REST soft-save → execute-against-draft → hard-save** with the user's API key. Ask the user for the key if you don't already have one (it goes in the `X-API-KEY` header; base URL is `https://api.{stage}.orbit.do/v5`).

Soft-save sequence:

1. `POST /soft-save/product-bricks` for each modified or freshly authored brick. Body: `{ productBrickId, request: EditProductBrickRequest }`. **Omit `validFrom`** — the server resolves it to `max(now, latest.validFrom + 1)` so you never collide with an existing version, never need to pre-query the chain, and never get bitten by clock skew. Each soft-save returns a `sessionToken`; bricks don't conflict with each other.
2. `POST /soft-save/products` for the product (with `productBricks: [...]` listing brick IDs in execution order — context first, then feasibility, then pricing, then scheduling). Same `validFrom`-optional convention.
3. **Inspect `response.summary` (`{ totalTests, passed, failed, errored }`) and `response.products[].testCaseResults`.** Note the `sessionToken` — you need it for hard-save. Don't skip ahead to step 6 until you've read this response.

If the brick TS itself was malformed, you'll get HTTP 400 with `internalCode: "BRICK_PAYLOAD_INVALID"` and either a one-line foot-gun hint or a `details: [{ line, column, message }]` array — see Step 4. Fix the payload, re-send. The validator runs before persistence so soft-save is atomic: either the new payload lands or nothing changes.

The brick `payload` is **a string**, not a function — the TypeScript source is JSON-stringified into the request. Author each brick in a local `.ts` file, then build the request body with `jq -Rs .` over the file or the equivalent in your scripting language. Hand-escaping a multi-page function inside a JSON string is how you spend an afternoon chasing parse errors. See `references/rest-endpoints.md` § "Soft-save" for the field-by-field shape.

## Step 6 — Execute against a draft (after a hard-save on fresh products)

Build a TransportDraft, then evaluate the product against it. **Important:** `/execute` reads the **last-hard-saved** product version. On a fresh product you must hard-save the bricks-linked product once first (Step 5 hard-save). On an EDIT to an existing product, `/execute` will show the LIVE behaviour — to preview a pending edit, read the soft-save response's `summary` + `testCaseResults` instead.

```bash
# 6a. Build a draft. Required body fields: type, status, shapeId, transport.
curl -X POST "$BASE/drafts" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"type":"manual","status":"draft","shapeId":"'"$SHAPE"'","transport":'"$TRANSPORT_JSON"'}'
# `status` and `shapeId` are NOT optional. For evaluation against a sales-shape product,
# `status: "draft"` is the right value. `shapeId` should match the shape you intend to gate on
# at step 11 (or at minimum a shape with the same `mode` so the transport parses).
# Use calculate-helpers.mjs' buildTransport() for the transport field — every required key
# is pre-encoded and the four 400 traps are pre-handled.
# NOTE: calculate-helpers builds multi-stop transports (`multiStopData.stops[]`). For a shape
# with `configuration.mode: "single-stop"`, the platform reads pickup/dropoff from `shipments[0]`
# instead — wrap an explicit `shipments[]` on top of the helper output.

# 6b. Execute
curl -X POST "$BASE/products/$PROD/execute" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
  '{"transportDraftId":"'"$DRAFT"'"}'
```

What you read off the response:

- **HTTP 200** — full calculator output (`context`, `feasibility`, `lineItems`, `schedule`, `brickMessages`). Assert by eye:
  - Feasibility flips correctly across the boundary.
  - Line items match the spec's pricing rules.
  - Schedule shows the right options and recommendations.
  - BrickMessages appear when expected.
- **HTTP 412** with `payload.message` starting `"TransportForProductsSchema parse failed:"` — the draft's `transport` field is missing or malformed. The serialised Zod issues tell you which field. **Patch the draft** (re-POST `/drafts` with the fix, or `POST /drafts/{id}/actions` to mutate it) and retry.
- **HTTP 422** with `internalCode: "BRICK_RUNTIME_ERROR"` — your brick threw at runtime. The `payload.message` is the unwrapped `Error.message`. **Fix the brick payload** (re-soft-save) before retrying. This is distinct from 5xx (platform error) — don't retry as-is.
- **HTTP 5xx** — platform error. Surface to user; not your bug.

For ad-hoc single-brick checks (e.g. "does my context brick produce the route fields the pricing brick expects?"), use `POST /v5/product-bricks/{brickId}/execute`. Body shape is discriminated by `type`:
- `context` → `{ type: "context", transportDraftId, productId? }`
- `feasibility` / `pricing` / `scheduling` → `{ type: "...", transportDraftId, contextBrickId, productId? }` (the contextBrickId provides the upstream context the brick depends on)

Iterate brick TS until the `/execute` output matches the spec. Logs from `/execute` (and `/product-bricks/{id}/execute`) persist to the test-run log group; fetch them via `GET /v5/products/{id}/execution-logs?onlyTestRuns=true` if you need a deeper trace than the synchronous response gives you.

`/products/calculate` still exists and is still useful: it runs against the **last-hard-saved** version of the product, so it's the right tool for "what does live currently produce?" snapshots. It is NOT the primary structural-sanity tool anymore — `/execute` reads the soft-save's pending state directly, which is what you want during authoring.

**Don't hand-roll a `TransportForProducts` from scratch.** Use the bundled `calculate-helpers.mjs` library at `scripts/calculate-helpers.mjs`. Same import pattern as before, but the output now feeds **three** consumers (calculate, draftSnapshot for test cases, AND the `transport` field of `POST /drafts`). One helper, three sites. **For single-stop shapes pass `mode: "single-stop"`** so the helper auto-wraps `shipments[0]` with `extras: []` — forgetting that wrap is the #1 412 trap on `POST /drafts`.

```js
import { stop, load, buildTransport } from
  "./scripts/calculate-helpers.mjs"; // path relative to this skill directory

const transport = buildTransport({
  pickup: stop({ companyName: "X", street: "Pariser Platz", houseNumber: "1",
                 zipCode: "10117", city: "Berlin", lat: 52.5163, lng: 13.3777,
                 day: "2026-05-11" }),
  dropoff: stop({ /* … */ }),
  loads: [load({ id: "load-1", weightKg: 5 })],
  mode: "single-stop", // omit for multi-stop; required for single-stop shapes
});

// As the transport field of POST /drafts:
const draft = await fetch(`${BASE}/drafts`, {
  method: "POST", headers: { "X-API-KEY": apiKey, "Content-Type": "application/json" },
  body: JSON.stringify({ type: "manual", transport }),
}).then(r => r.json());

// As the body for POST /products/calculate (legacy snapshot path):
const offer = await fetch(`${BASE}/products/calculate`, {
  method: "POST", headers: { "X-API-KEY": apiKey, "Content-Type": "application/json" },
  body: JSON.stringify({ transportShapeId, productIds: [productId], transport, allowUnavailable: true }),
}).then(r => r.json());
```

The four classic 400 traps still apply to the `transport` body — `address.latitude`/`longitude` not nullable, `address.zipCode` (not `postalCode`), `dangerousGood.packagingGroup: "-"` (not `""`), `pickupStopIndex` (not `pickupStop`). The helpers handle all four; only diverge from them when you have a specific reason. See `references/rest-endpoints.md` § "TransportForProducts".

## Step 7 — Capture ProductTestCases and run

**Walk the test ledger from the spec interview.** If you ran the interview at Step 1, the customer signed off on a markdown ledger (Block 7 of `references/interview-script.md`) that lists every required test case with its category, expected outcome, BrickMessages, and the interview answer it was derived from. Step 7 is mechanical: walk those ledger rows in order and create one ProductTestCase per row via `POST /products/{productId}/test-cases`.

Each test case stores a `draftSnapshot` (the synthetic transport from Step 6, wrapped as `{ shapeId, transport }`), a `simulatedAt` (frozen time), and an `expectedOutput` (`{ lineItems, feasibility }` — schedule is intentionally not asserted).

**Read `validationWarnings[]` on every create response.** `POST /v5/products/{id}/test-cases` returns a non-blocking `validationWarnings: DraftSnapshotValidationWarning[]` array. Empty means the snapshot would parse cleanly at `/test-cases/run` time; non-empty means the snapshot is structurally accepted but underspecified — patch the missing fields before running, or the run will fail with a `status: "error"` you'd have to debug after the fact. (A bare TransportForProducts without the `{ shapeId, transport }` wrapper, or `transport: null`, still hard-400s — `validationWarnings[]` is for the in-between case where the wrapper is right but a leaf field is missing.)

If the customer skipped the interview (clean spec at Step 1), construct a minimum cohort by hand. Cover:

- A happy path (typical request, mid-range).
- A boundary case (right at a feasibility limit).
- One infeasibility case **per feasibility brick** (asserts the error structure and BrickMessages).
- Optional: a surcharge / discount path if your product has those.

**Don't drift from the ledger.** If you find yourself authoring a case that isn't on the ledger, ask the user whether to add it (and append the ledger row) or skip it. The signed-off ledger is the contract; silent drift means the customer's contract and the actual tests don't match — the regression net you build won't catch what they expected it to catch.

Run them: `POST /products/{productId}/test-cases/run` → returns `{ testCaseResults: [{ status, diffs, computedOutput, expectedOutput, logs, errorMessage, errorDetails }] }`.

## Step 8 — Iterate until green

For each failed test case, decide which bucket:

- **Real bug** → fix the brick code, soft-save again (this re-runs all tests), re-inspect.
- **Over-specified assertion** → `POST /products/test-cases/{testCaseId}/remove-assertion` with the path.
- **Intentional ground truth change (brick edit, pending soft-save)** → soft-save → hard-save the brick with `keepTestCaseIds: <current cohort 0 IDs>`. Hard-save promotes the soft-save's computed output as the new ground truth for the kept tests. Do **not** use `run-for-review` + `update-ground-truth` here — that flow runs against live last-hard-saved state and won't see your pending soft-save (returns HTTP 400 or silently no-ops). The review flow is only for bootstrapping ground truth on already-hard-saved bricks whose test cases have empty `expectedOutput`.

**Read `errorDetails[]` first when present.** When `/test-cases/run` returns `status: "error"` and the failure has per-field detail (typically a stored `draftSnapshot.transport` that doesn't validate against `TransportForProducts`), the result exposes `testCaseResults[].errorDetails: { path: string[], message: string }[]` — one entry per validation issue. Prefer this over substring-searching `errorMessage` / `logs[].message` when reasoning about which field of the snapshot to patch. It mirrors the `BRICK_PAYLOAD_INVALID` envelope on `POST /product-bricks` so the same parsing logic works for both.

**Scheduling-brick crashes are not silently swallowed.** `/test-cases/run` runs scheduling bricks, and a scheduling brick that throws surfaces as `status: "error"` with the unwrapped throw — same for `POST /products/{id}/execute` and `POST /product-bricks/{brickId}/execute`. This is generally a **bug-find**, not noise — surface it clearly when reporting test results. If a scheduling brick legitimately depends on real-time-relative date math that throws under frozen-time test runs, that's a brick bug; fix it to not throw on a deterministic clock.

Iterate until **all test cases pass**. This is the green light to hard-save.

The full SOP — including how to design a good test case, what to assert, and the cohort lifecycle — is in `references/testing-sop.md`. Treat it as the gold-standard playbook; don't deviate without a reason you can explain.

## Step 9 — Hard-save (commit, no tests run; cohort rotates)

Once green: `POST /hard-save/products` (and `/hard-save/product-bricks`) with the `sessionToken` from step 5 and your `keepTestCaseIds`. Hard-save:

- Consumes the session token (single-use, 10-minute TTL — re-soft-save if expired).
- Commits the pending payload to a new version (server-resolved validFrom).
- **Rotates the test cohort.** Every id in `keepTestCaseIds` is **archived** against the previous entity version (its `cohortTimestamp` becomes non-zero). For each kept test case a **new test-case row** is created against the just-persisted entity version, with the soft-save's computed output as the new ground truth. The new IDs come back in `response.newTestCaseIds`. **The IDs you sent are no longer the current cohort.**
- Returns `{ saved, entityType, testCasesCreated, testCasesDeleted, newTestCaseIds, entity }`.
- **Does not run tests.** That's why step 5's response inspection mattered.

**Print `newTestCaseIds` to the user inline.** Any subsequent `/test-cases/run` or `/test-cases/{id}` call must use them. The IDs you sent in `keepTestCaseIds` will return 404 (they're archived). This is the single most common trap with the new cohort model — surface the new IDs so the user has them in their transcript.

If you forget what the response of soft-save said, you cannot recover it post-hard-save — re-soft-save and check again.

**Concurrency.** Hard-save returns HTTP 409 with `internalCode: "CONFLICT_RETRY"` when a concurrent writer already landed at the requested `validFrom` (or the soft-save session is otherwise stale relative to the latest persisted version). The auto-bump on soft-save means this should rarely fire; if it does, re-fetch the latest version, re-soft-save, retry the hard-save. Don't paper over it — a 409 here means another agent or operator just shipped a version of the same entity and your view of the world is stale.

## Step 10 — Gate via TransportShape (and Hub)

A product that no shape exposes is invisible. After hard-save:

- For each TransportShape that should expose this product, gate it via REST:
  ```bash
  curl -X PATCH "$BASE/transportshapes/$SHAPE/products" -H "X-API-KEY: $KEY" -H "Content-Type: application/json" -d \
    '{"add":["'"$PROD"'"],"target":"sales"}'
  ```
  Body: `{ add?: string[], remove?: string[], target: "sales" | "purchasing" }`. At least one of `add`/`remove` must be a non-empty array. Add-IDs are validated against the tenant (unknown → 400). Remove-IDs aren't (idempotent / retry-safe). Concurrency is naive read-modify-write — same semantics as Mission UI's Settings → TransportShapes → Products tab; if two agents PATCH the same shape simultaneously, the second write wins and may stomp the first's add. Prefer sequential when batching shapes.
- **Discovering the right shape ID.** Use `GET /v5/transportshapes` to list all shapes for the tenant. The conventional Hub-gating shape is `migrated-shop-shape-{tenantId}-{tenantId}` BUT this is not present on every tenant (it's only created by the migration of legacy webshop tenants). On a tenant that doesn't have it, look for any shape with `configuration.products.sales.ids` populated — that's the de facto sales/Hub shape. Confirm with the user before gating to a non-conventional shape, especially on production.
- If `shape.configuration.products.{sales|purchasing}.mustBeFeasible: true` is set, only feasible products show — make sure your feasibility brick handles the shape's typical traffic.
- For multi-stop products, the shape's `configuration.outputs` must include `"tour"` alongside `"order"` and `"shipment"`, otherwise the booking flow silently loses the tour entity. See `references/product-anatomy.md` § TransportShape → `outputs`.
- If the product is sales-typed and should appear in the customer-facing **Hub**, also add the product ID to `Shop.offeredProducts` (third gating layer). **This is the one remaining tRPC-only mutation** — there's no API-key REST equivalent for `Shop.offeredProducts` today. Use Mission UI: Settings → Shop → Offered Products. See `references/audience-and-extras.md` § "Hub activation".

## Step 11 — Summarize

End every product setup with a short report that includes:

- Product name (EN + DE), ID, status, `validFrom` (server-resolved).
- Brick IDs and types created/edited.
- DataPools touched.
- TransportShape(s) the product is now exposed on.
- The test cases written and their final pass status. **List the post-hard-save IDs** (`newTestCaseIds`) — these are the live cohort.
- Any `OPEN: …` items from the spec interview that the user still needs to resolve.

Format the report as markdown, tight, scannable. The user will paste this into a ticket or share with a teammate.

## Decision shortcuts

| User says…                                                    | Do this                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| "Re-verify product P" / "is X still working?" / "before the demo, check Y is still in spec" | **VERIFY mode.** V1 readback via `GET /v5/products/{id}/{validAt}` + `GET /v5/product-bricks/{id}/{validAt}`, V2 `POST /products/{id}/test-cases/run`, V3 one-line attestation. Read-only. Don't soft-save / hard-save / mutate. If the readback surfaces drift the user didn't expect, re-route to EDIT mode. |
| "Set up a product for X" with vague details                   | Run the interview (`references/interview-script.md`), then resume the workflow. **Default to FULL workflow on REST end-to-end** — no Mission UI. |
| "Edit the pricing on product Y"                               | EDIT mode. Soft-save brick (omit validFrom) → inspect `summary` + `testCaseResults` → hard-save brick with `keepTestCaseIds: <all current cohort 0 IDs>`. Surface `newTestCaseIds` from the response. **Do NOT use the `run-for-review` + `update-ground-truth` review flow for brick edits** — `run-for-review` always runs against LIVE state, not your pending soft-save. See `references/testing-sop.md` § "Pattern: intentional ground-truth change". |
| "Add a feasibility rule for Z"                                | Author a new feasibility brick. **Manifest the shell via `POST /v5/product-bricks`** (no Mission UI), then soft-save the brick payload + soft-save the product with the new brick added to `productBricks`. |
| "Why is product Y not showing in Orbit Hub?"                  | Diagnostic, not setup. Check `shape.configuration.products.sales.ids` (via `GET /v5/transportshapes`), then product `status`, then version validity (`validFrom` ≤ transport date), then `Shop.offeredProducts` (managed in Orbit MissionControl → Settings → Orbit Hub; there's no public read for it). |
| "What's the current price for transport T against product P?" | `POST /products/calculate` with `transportShapeId` + `productIds: [P]`. Read `offers[0].lineItems`. (Snapshot mode — runs against last-hard-saved.) |
| "Test product P against this transport — is it bookable?"    | Build a draft via `POST /v5/drafts`, then `POST /v5/products/{id}/execute` with `{transportDraftId}`. Returns full calculator output for the soft-save state. |
| "Test brick B in isolation"                                  | `POST /v5/product-bricks/{brickId}/execute` with `{ type, transportDraftId, contextBrickId? }` (contextBrickId required for feasibility/pricing/scheduling). |
| "Run all tests for product P"                                 | `POST /products/{P}/test-cases/run`. Report pass/fail and any diffs. **Check `errorDetails[]` first when results have `status: "error"`**. |
| "Show me the logs for the last /execute call on product P"   | `GET /v5/products/{P}/execution-logs?onlyTestRuns=true` (resolves the latest stream automatically). For raw production traffic: `onlyTestRuns=false`. |
| "Product metrics" / "show distance & duration on the offer"   | Product Metrics are live. They're display-only badges (`{ title, value:string }`) any brick emits via an optional `metrics[]` (pricing/scheduling switch to their object-return form). Merged last-wins by title, surfaced on `Offer.metrics` (calculate/execute) + `Order.metrics`. No icon, no dedicated endpoint, and NOT asserted by test cases. See `references/product-anatomy.md` § Product Metrics and `references/brick-authoring.md` § Emitting Product Metrics. |

## Failure modes to watch for

- **Drafting bricks before the spec is locked.** Don't. The interview pays for itself.
- **Skipping test cases because "/execute looked fine".** Don't. /execute is a one-off snapshot; only persisted ProductTestCases catch regressions on subsequent edits.
- **Putting all logic in one mega-brick.** Splits along concerns (route, weight, region, surcharge) make every future edit easier and produce better operator-facing error messages.
- **Hard-saving with `keepTestCaseIds: []` after soft-save reported failures.** Failures are real signals; investigate before committing.
- **Forgetting to use `newTestCaseIds` after a hard-save.** The `keepTestCaseIds` you sent are archived; subsequent /test-cases/run or /test-cases/{id} calls against the old IDs will 404. Always print `newTestCaseIds` to the user.
- **`/test-cases/run` returns bare `"Product not found"`.** This usually means the test case's `simulatedAt` is BEFORE the product's first hard-save `validFrom` — version resolution returns nothing and the runner can't tell the difference between "product missing" and "no version valid at this time". Read `validFrom` from your hard-save response (`entity.validFrom`) and pick a `simulatedAt` ≥ that value plus a buffer. If you compute `simulatedAt` from a date string, double-check the year — the bug usually shows up when an off-by-one-year typo lands the simulated time before the product was even created.
- **Reaching for `/execution-logs` to debug a `/test-cases/run` failure.** Won't work — test-case-run logs aren't there. They're inline in the `/test-cases/run` response (`testCaseResults[].logs[]`, `errorMessage`, `errorDetails[]`). The "Three log scopes" section at the top of this file has the rule.
- **Hardcoding rates/prices in code instead of a DataPool.** Anything the operator might want to tweak in 6 months belongs in a DataPool — and DataPools have REST too now (soft-save / hard-save).
- **Hand-rolling `validFrom` on soft-save.** Stop. Omit it; the server auto-bumps. The only legitimate reason to pass an explicit value is to schedule a future-effective version.
- **Using `import` in brick code.** It will not parse. All utilities come through `utils`. `z` is `utils.tools.z`, Luxon `DateTime` is `utils.dateTime.DateTime`.
- **Trailing `;` or top-level `const` in a brick payload.** Server-side validator catches both with a one-line hint at HTTP 400 — but you waste a roundtrip every time. The wrapper is `const __brick: <FnType> = ( <YOUR PAYLOAD> );`; author payloads as a single TS expression.
- **Making the user re-answer questions.** When you've already learned tenant + stage + API key from earlier turns, reuse them.

## Safety

- **Never run test cases against `production` without explicit user confirmation per session.** The testing framework is read-only at runtime, but the soft-save flow mutates draft entities — confirm stage on every product setup.
- **Never hard-save a product with failing tests** unless the user explicitly said "I know, ship it anyway" and you've shown them the diff.
- **Every hard-save against `production` requires a fresh confirmation from the user, no matter how trivial the change.** Show the diff (current → new value), the `validFrom` you'll commit (server-resolved), and the test cohort status. A hard-save mutates revenue-bearing config for every customer of that tenant — one prior "yes please" earlier in the session is not standing authorization. This rule applies to both FULL workflow step 9 and EDIT-mode step E6. The auto-bump and REST-end-to-end nature of the new workflow do **NOT** relax the prod-safety rule.
- **The `PATCH /v5/transportshapes/{id}/products` concurrency model is naive read-modify-write.** Two simultaneous PATCHes on the same shape can stomp each other's adds. When batching, sequential is safer.
- **Always pass server-resolved `validFrom` along to the user in your summary** — don't pretend you know what value the server picked. Read it back from the response (`POST /products` and `POST /product-bricks` both return `{ id, validFrom }`).

## What to load when

| You're doing…                                                    | Read…                                            |
| ---------------------------------------------------------------- | ------------------------------------------------ |
| Building a `TransportForProducts` payload (drafts / calculate / soft-save / test cases) | `scripts/calculate-helpers.mjs` (importable library) |
| Spec interview                                                   | `references/interview-script.md`                 |
| Designing the brick split                                        | `references/product-anatomy.md`                  |
| TransportShape configuration (gating, outputs, form, features)   | `references/product-anatomy.md` § TransportShape |
| Writing TypeScript brick code                                    | `references/brick-authoring.md`                  |
| Choosing/calling a REST endpoint                                 | `references/rest-endpoints.md`                   |
| Writing or running test cases                                    | `references/testing-sop.md`                      |
| Drafting EN/DE marketing copy                                    | `references/marketing-copy.md`                   |
| Audience filtering, vouchers, extras, Hub gating                 | `references/audience-and-extras.md`              |
| Hub activation, brick logs, cleanup                              | `references/operations.md`                       |
| 2-stop scheduling recipes (lead time, cutoffs, ferry buffers)    | `references/scheduling-2stop-patterns.md`        |
| Multi-stop scheduling (3+ stops, recommendations, fixed windows) | `references/multistopp-scheduling.md`            |

Load only what you need. Most product edits touch only `brick-authoring.md` + `rest-endpoints.md` + `testing-sop.md`. EDIT-mode work usually adds `product-anatomy.md` § TransportShape only when you're touching gating.
