import unittest

from src.data_age import display_state


class DataAgeTests(unittest.TestCase):
    def test_fresh_online_snapshot(self) -> None:
        self.assertEqual(display_state(True, 1, True, True), "Updated 1m ago")

    def test_failed_online_refresh_keeps_stale_snapshot(self) -> None:
        self.assertEqual(
            display_state(True, 8, False, True),
            "Stale - updated 8m ago - Retry",
        )

    def test_source_stale_snapshot_is_not_presented_as_fresh(self) -> None:
        self.assertEqual(
            display_state(True, 4, True, False),
            "Stale - updated 4m ago - Retry",
        )

    def test_offline_snapshot_is_stale(self) -> None:
        self.assertEqual(display_state(False, 8, False, True), "Stale - updated 8m ago - Retry")

    def test_offline_without_snapshot(self) -> None:
        self.assertEqual(display_state(False, None, False, False), "Offline - no snapshot - Retry")

    def test_online_without_snapshot_is_recoverable(self) -> None:
        self.assertEqual(display_state(True, None, False, False), "Unavailable - no snapshot - Retry")

    def test_negative_age_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            display_state(True, -1, True, True)


if __name__ == "__main__":
    unittest.main()
