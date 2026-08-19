# PostgreSQL design checks

Confirm the deployed major version and current PostgreSQL documentation before making version-sensitive recommendations.

- Design for PostgreSQL's heap storage and MVCC. Consider update churn, tuple width, vacuum, long transactions, and bloat for write-heavy tables.
- PostgreSQL creates indexes for primary and unique constraints, but not automatically for referencing foreign-key columns. Add an FK index only when joins, parent updates or deletes, or access paths justify it.
- Choose index access methods from operators and queries. Consider partial, expression, covering, GIN, GiST, or BRIN indexes only when the workload fits; every index adds write and maintenance cost.
- Treat `CREATE INDEX CONCURRENTLY` and other online changes as operational plans with version-specific caveats. They may take longer, wait on transactions, or leave invalid artifacts after failure; rehearse and verify.
- Use native constraints and transaction isolation for real invariants. Apply row-level security only when the trust and connection model makes database-enforced tenant policy useful.

Primary references: [MVCC](https://www.postgresql.org/docs/current/mvcc-intro.html), [indexes](https://www.postgresql.org/docs/current/indexes.html), [constraints](https://www.postgresql.org/docs/current/ddl-constraints.html), and [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html).
