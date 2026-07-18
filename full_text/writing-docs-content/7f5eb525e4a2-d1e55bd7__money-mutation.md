---
name: money-mutation
description: Use before implementing any code path that moves money - credit / debit, balance adjustment, bonus grant, settlement, payout, refund, transfer. Enforces Decimal helper + idempotency key + double-entry ledger + audit trail + reconciliation checklist before writing code.
---

# Money Mutation

Real money. Float drift is a loss; missing idempotency is a double-pay;
missing audit is a compliance gap.

Run this skill BEFORE writing any code that moves a balance, grants
credit, settles, claims, refunds, or adjusts.

## Pre-flight checklist

Answer each of these before writing the first line of code. If you cannot
answer, escalate to the user.

1. **Where does the money come from / go to?** Name the source account
   and destination account. Both must exist in the ledger.
2. **What's the idempotency contract?** What key prevents a double-pay
   on retry? Where does it persist? For how long?
3. **What's the unit of money?** Currency code + the project's Decimal
   helper. Forks should wrap their chosen library (`Decimal.js`,
   `BigNumber.js`, math.js BigNumber) in a single helper that pins
   precision and rounding mode in one location.
4. **What's the isolation level?** Postgres `SERIALIZABLE` with a
   bounded retry on `40001` for money-touching code paths.
5. **Are credits paired with debits?** Every credit row needs a paired
   debit row in the SAME DB transaction so the ledger balances.
6. **Is there a lock?** Concurrent operations on the same wallet wrap in
   a distributed lock with try/finally release and a fencing token.
7. **Is there an audit row?** Who did it, when, why, source-of-action.
   Admin actions additionally write to the admin audit log.
8. **What does the wire format look like?** Money serializes as a string
   at every wire boundary (HTTP, Kafka, Redis, logs).
9. **What's the failure path?** If the call fails halfway, what state
   is the system in? Can it be safely retried?
10. **What's the reversal path?** When this needs to be undone
    (chargeback, clawback, void), is there an explicit reversal event
    with paired ledger entries?

## After implementation - verification checklist

- Replay the mutation with the same idempotency key. Did it return the
  prior response without performing the side effect again?
- Run with a forced `40001` conflict (concurrent write). Did the retry
  loop fire? Did the result remain correct?
- Force the call to fail after the credit but before the debit. Does
  the DB transaction roll back both?
- Force the lock to be held. Does the second caller wait or fail
  cleanly? It must NOT proceed silently.
- Sum the ledger after the test. Is the balance correct? Is the audit
  row present?

## Dispatch

- For review of an existing money diff, hand to the fork's domain-safety
  reviewer (e.g. `casino-safety-reviewer`, `payments-reviewer`,
  `vault-reviewer`) AND `security-reviewer`.
- For migration of a money table, additionally invoke
  `migration-reviewer`.
- For a saga that crosses services, additionally invoke
  `distributed-systems-reviewer`.
