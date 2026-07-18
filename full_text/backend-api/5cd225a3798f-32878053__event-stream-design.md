---
name: event-stream-design
description: Use when designing a new Kafka topic, consumer, producer, transactional outbox, saga, or change-data-capture path. DDIA-grounded patterns - commands vs events, point-in-time joins, idempotency, exactly-once via dedup.
---

# Event Stream Design

The Kafka log is the source of truth between services. Treat the design
of a new topic / consumer as a higher-stakes act than designing an HTTP
endpoint - schemas are forever and replay is mandatory.

## Step 1 - command or event?

- **Command** = "do X." Synchronous. Validated. Can be rejected.
  Lives in HTTP / gRPC.
- **Event** = "X happened." Asynchronous. Immutable. Cannot be unsent.
  Lives in Kafka.

Validate BEFORE publication. Once an event is on the log it is a fact.
If a downstream consumer might need to reject the event, you have a
command pretending to be an event.

## Step 2 - what's the event-time?

- Tag every event with a logical event-time (`occurredAt`), not just
  the ingestion time. Aggregations and joins use event-time.
- Producers can lie. Treat producer event-time as a hint, not a
  source-of-truth, for cross-service ordering.

## Step 3 - partition key

- Pick a key that aligns with locality so causally-related events
  land on the same partition: `user_id`, `account_id`, `entity_id`,
  `wallet_id`, `campaign_id`.
- Cross-partition ordering does NOT exist. If two events need a
  happens-before relationship, put them on the same partition or
  carry an explicit causal id.

## Step 4 - schema and evolution

- Forward-compatible: new producers, old consumers. Unknown fields
  ignored.
- Backward-compatible: old producers, new consumers. Missing fields
  default sensibly.
- Add fields with defaults. Never remove a field in one step; mark as
  deprecated, then remove in a later release.
- Protobuf / Avro tag numbers are forever.

## Step 5 - producer defaults

- `acks=all` for any event the platform cannot afford to lose.
- `enable.idempotence=true`.
- `max.in.flight.requests.per.connection <= 5`.
- Outbox pattern for "DB write + Kafka publish":
  - Write the domain row + an `outbox` row in ONE local Postgres
    transaction.
  - A relay reads outbox and publishes to Kafka with the outbox PK
    as the dedup key.
  - Never call `kafka.send` directly inside a DB transaction - it is
    not transactional and rollback leaves an orphan event.

## Step 6 - consumer defaults

- Every consumer dedups BEFORE mutating state. Use a unique
  `(topic, partition, offset)` or a business event id.
- Write the dedup row in the SAME DB transaction as the side effect.
  Kafka offset commit alone is NOT enough - the consumer can crash
  between commit and side effect.
- Commit offsets only after the dedup row is durable.
- Use a 60-second buffer for "missed terminal events" that arrive
  before the entity id is known.
- Dead-letter topic for any poison message that could block a
  partition.

## Step 7 - stream-table joins must be point-in-time

- Carry the relevant snapshot at the moment of the event (price at
  placement time, rule version at claim time, exchange rate at
  settlement time).
- Current-state joins are nondeterministic and break reprocessing.

## Step 8 - replay test

- A consumer is correct iff replaying the log from offset 0 produces
  the same output. If you cannot replay, the design is broken.
- Aggregates: composite primary key, dedup before mutation, consumer
  is a pure function of the input stream.

## Step 9 - cross-service workflows are sagas

- Each step has a forward action and an explicit, idempotent
  compensating action.
- Compensations must be safe to run on entities that were never
  created or charged (no-op when nothing to undo).
- Saga state lives in the orchestrator's local DB; recover by replay.

## Step 10 - review

- Hand to `distributed-systems-reviewer`.
- If the event carries money, additionally hand to the fork's
  domain-safety reviewer.
- If the producer schema changes, additionally hand to
  `migration-reviewer` for the migration that adds the outbox table
  or alters the column.

## Anti-patterns

- LWW timestamp ordering on money.
- Wall-clock comparison across services.
- Kafka offset commit before the side effect is durable.
- Direct `kafka.send` inside a DB transaction.
- Cross-partition ordering assumptions.
- Stream-table join on current state.
- Consumer that cannot be replayed from offset 0.
- Cross-service workflow as 2PC/XA.
