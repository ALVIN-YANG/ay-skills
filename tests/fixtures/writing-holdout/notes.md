# Upload retry measurements

Readers can operate a website but do not know retry or idempotency terminology.

A controlled experiment sent 200 uploads. Twelve first attempts timed out. The server may have accepted an upload before its response was lost, so a timeout did not establish failure.

The test server accepted an operation ID and returned the existing upload when the same ID was retried. Retrying with a new ID could create a duplicate. This behavior was tested only on this server, not on every storage provider.

There is no production rollout, personal experience, or evidence that retries reduce latency. Explain the mechanism without inventing any of these claims.
