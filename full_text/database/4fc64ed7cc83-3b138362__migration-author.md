---
name: migration-author
description: Use when authoring a new schema migration (Drizzle, TypeORM, Sequelize, Prisma, Knex). Selects the right ORM CLI, names files correctly, enforces forward-only + rolling-deploy compatibility, routes review to migration-reviewer.
---

# Migration Author

Picking the wrong CLI silently creates an unusable file that the deploy
pipeline will not see. Pick deliberately.

## Step 1 - identify the ORM

Forks document this in their per-service rules. The general matrix lives
in `90-migrations.md`:

| ORM | Generate | Apply | File shape |
|---|---|---|---|
| Drizzle | `pnpm <svc>:db:generate --name <name>` or `drizzle-kit generate` | `pnpm <svc>:db:migrate` | `<00NN>_<snake_name>.sql` |
| TypeORM | `pnpm migration:generate ./data/migrations/<Name>` | `pnpm migration:run` | `<unix-ms>-<Name>.ts` |
| Prisma | `npx prisma migrate dev --name <name>` | `npx prisma migrate deploy` | `<timestamp>_<name>/migration.sql` |
| Sequelize | hand-write or `npx sequelize migration:generate --name <name>` | `npx sequelize-cli db:migrate` | `<YYYYMMDDHHmmss>-<name>.js` |
| Knex | `npx knex migrate:make <name>` | `npx knex migrate:latest` | `<YYYYMMDDHHmmss>_<name>.{js,ts}` |

If the project owns a legacy shared DB through one service, all
migrations for that DB land in that owning service. Do not add
migrations to read-only / introspected schema directories.

## Step 2 - universal rules

- **Forward-only.** Down-migrations are documentation, not policy. The
  rollback strategy is to write another forward migration that undoes
  the change.
- **Backward-compatible for at least one rolling deploy window.** The
  previous release must still be able to read the new schema during
  the deploy. Destructive changes are two-step:
  1. Deploy code that tolerates BOTH shapes.
  2. Drop the old shape in a later migration after the rolling deploy
     completes.
- **No broad table locks on hot tables** (`ALTER TABLE ... DROP
  COLUMN`, `RENAME COLUMN`). Use `CONCURRENTLY` on indexes; phase
  destructive column changes.
- **Idempotent on partial application.** The deploy can die halfway;
  the next run must complete cleanly.

## Step 3 - write the change

- Make the schema edit in code first (Drizzle / TypeORM entity /
  Prisma schema).
- Run the generate command. Inspect the generated SQL or TS - do not
  trust the generator blindly.
- For Drizzle, confirm the numeric prefix is the next gap-free number.
- For TypeORM / Sequelize / Knex, confirm the timestamp prefix is
  monotonic.

## Step 4 - verify locally

- Drop a scratch DB. Run the migration from scratch. It must complete.
- Test on a non-empty DB (use a snapshot or test fixture).
- Run the previous release's binary against the new schema. It must
  still work.

## Step 5 - review

- Self-review against the migration-author checklist above.
- Hand to `migration-reviewer` subagent before merge.
- If the schema change touches money tables, additionally hand to the
  fork's domain-safety reviewer.

## Anti-patterns

- Writing raw SQL outside the ORM CLI (Drizzle / TypeORM / Prisma).
- Two migrations in one file ("while I'm here, also...").
- A migration that the previous release cannot tolerate, deployed in
  one shot.
- A migration whose down-version reverses business meaning (lost
  audit data).
- Migrations under a seeds / fixtures directory (seeds are not
  schema).
