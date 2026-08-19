# SQLite design checks

Confirm the SQLite library version bundled by the application, compile options, connection setup, journal mode, and migration framework. The system SQLite version may differ from a development CLI.

- Treat SQLite as an embedded database file with local operational constraints, not as a smaller client-server database. Check file ownership, backup, encryption, and whether multiple processes or hosts can access it safely.
- WAL can let readers and a writer overlap, but ordinary WAL still has one writer at a time and depends on checkpoint behavior. Test write bursts, busy handling, long readers, app suspension, and crash recovery.
- Enable and verify foreign-key enforcement on every relevant connection instead of assuming the default. Exercise `foreign_key_check` after migrations when appropriate.
- Use declared types and constraints deliberately while accounting for SQLite type affinity and application binding behavior.
- Plan migrations against the exact version's `ALTER TABLE` support. Rebuild-table migrations need transaction, trigger, view, index, data-copy, integrity, disk-space, and rollback checks.

Primary references: [WAL](https://www.sqlite.org/wal.html), [foreign keys](https://www.sqlite.org/foreignkeys.html), [ALTER TABLE](https://www.sqlite.org/lang_altertable.html), and [isolation](https://www.sqlite.org/isolation.html).
