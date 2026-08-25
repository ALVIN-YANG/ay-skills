# Approved brief: PairDown

A macOS user selects one folder and finds visually similar CandidatePairs fully on device. A ScanSession can be scanning, ready, cancelled, or failed. The user chooses a CandidatePair and may move one selected file to system Trash; the app never deletes automatically. The review decision survives relaunch in SQLite. No account, cloud upload, sharing, subscription, or background folder monitoring.

The approved pure review-decision checkpoint receives a ScanSession state and a tuple of selected file IDs. In ready, zero IDs returns `keep-reviewing`, exactly one returns `confirm-trash`, and more than one is rejected. scanning returns `wait-for-scan`, cancelled returns `restart-scan`, failed returns `retry-scan`, and an unknown state is rejected. SQLite, scanning, and Trash integration remain outside this checkpoint.
