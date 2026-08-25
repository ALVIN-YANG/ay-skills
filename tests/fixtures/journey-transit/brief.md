# Approved brief: NextStop

An iPhone commuter saves a Stop and sees Departures with a visible DataAge. The app works without an account. When offline, the last successful snapshot remains readable and is marked Stale; manual Retry remains available. Notification permission denial must not block manual refresh. A tiny regional feed adapter refreshes public data once per minute. No ticket sales, social feed, ads, location tracking, or user profiles.

The approved pure display checkpoint inputs are named `is_online`, `age_minutes`, `latest_refresh_success`, and `source_confirmed_current`. A snapshot is Stale with Retry when offline, refresh failed, or the source did not confirm current data. No snapshot must say `Offline - no snapshot - Retry` when offline or `Unavailable - no snapshot - Retry` when online; it must never claim there are no Departures. A negative DataAge is rejected. Feed, cache, notification, and app integration remain outside this checkpoint.
