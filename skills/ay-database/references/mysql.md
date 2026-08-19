# MySQL and MariaDB design checks

Confirm the product, storage engine, exact version, SQL mode, charset, and collation. Do not transfer MySQL behavior to MariaDB, or one version's DDL guarantees to another.

- For InnoDB, the primary key is the clustered index and is carried by secondary-index entries. Evaluate primary-key width, stability, insertion pattern, and the cost it adds to every secondary index.
- Derive composite index order from equality, range, join, and sort patterns. Account for collation, prefix length, generated or functional columns, and covering needs using the deployed version.
- State transaction isolation and locking assumptions. Test contention, deadlocks, gap or next-key locking, and retry behavior for the real statements rather than assuming generic MVCC behavior.
- Check each schema change against the version's `ALGORITHM`, `LOCK`, metadata-lock, rebuild, space, and replication behavior. “Online DDL” does not mean zero blocking or zero operational risk.
- Keep constraints explicit and verify that the selected version enforces them as expected. Avoid relying on silent coercion or environment-specific SQL modes.

Primary references: [InnoDB indexes](https://dev.mysql.com/doc/refman/8.4/en/innodb-index-types.html), [isolation](https://dev.mysql.com/doc/refman/8.4/en/innodb-transaction-isolation-levels.html), and [online DDL](https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl.html). For MariaDB, use its matching version documentation instead.
