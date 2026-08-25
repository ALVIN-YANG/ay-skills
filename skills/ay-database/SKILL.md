---
name: ay-database
description: Select and design a database-specific logical and physical data model before implementation. Use when the primary deliverable is database choice, tables or collections, keys, constraints, indexes, transactions, concurrency, migration, ERD, DDL, or database.md, including 数据库设计, 表结构, 索引设计, or schema review. Do not use for product requirements, system architecture, API contracts, query debugging, or requests primarily asking to run migrations.
---

# AY Database

Design from invariants and access paths, then apply the actual engine's behavior.

## Approval contract

<!-- ay-contract:start -->
- Read the full request and investigate discoverable facts before asking the user.
- Treat review, diagnosis, explanation, and planning as read-only unless the user also requests change.
- Treat a precise instruction as approval when target, observable result, and acceptance boundary are clear.
- A broad outcome authorizes investigation, not file or artifact changes based on choices the agent must invent.
- For a materially underspecified change, present one recommended proposal and wait for approval.
- After approval, execute autonomously inside the approved boundary; do not ask about ordinary implementation details.
- Reopen approval only when new evidence changes behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or external actions.
- Perform external actions only when the request or approved proposal includes them. Confirm the exact target before an irreversible action.
- Preserve unrelated and user-authored work. Verify the real requested outcome before claiming completion.
<!-- ay-contract:end -->

## Establish the database contract

Inspect available requirements, architecture, API, existing schema and migrations. Preserve approved domain terms and invariants. Identify the exact engine and version, deployment model, driver or ORM, migration tool, workload, access paths, consistency, retention, tenancy, scale, security, backup, and recovery constraints. Preserve an existing engine unless evidence justifies migration.

If engine choice is genuinely open, compare the smallest credible options against workload and operations; do not pick by fashion. For PostgreSQL read [PostgreSQL](references/postgresql.md), for MySQL or MariaDB read [MySQL](references/mysql.md), and for SQLite read [SQLite](references/sqlite.md). For another engine, consult its current primary documentation before using engine-specific claims.

## Model invariants, then storage

Define entities or aggregates, ownership, lifecycle, identifiers, cardinality, uniqueness, nullability, and deletion or retention semantics. Turn enforceable invariants into database constraints when the engine can express them safely.

Derive tables, collections, keys, indexes, partitions, and denormalization from actual reads, writes, ordering, volume, and contention. State the queries each index serves and the write or storage cost. Do not impose UUIDs, soft deletion, timestamps, normalization, row-level security, or NoSQL universally.

Keep the handoff focused on supplied invariants and access paths. Omit generic engine advice that does not change this design.

Define transaction boundaries, isolation or conflict handling, idempotency support, tenant separation, audit needs, and sensitive-data controls. Keep API response shape independent from physical storage.

## Plan change and proof

For an existing system, cover backfill, compatibility window, locks, online or rebuild behavior, rollback, observability, and integrity checks using the exact engine version. Separate schema design from permission to execute DDL or touch live data.

Create `database.md`, ERD, DDL, or migration design only when requested or required for an approved handoff. Validate representative queries, constraints, concurrent writes, and migration rehearsal. Stop before implementation or live migration unless separately authorized.
