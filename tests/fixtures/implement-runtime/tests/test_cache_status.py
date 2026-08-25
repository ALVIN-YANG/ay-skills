import unittest

from src.cache_status import visible_status


class CacheStatusTests(unittest.TestCase):
    def test_online_is_live(self) -> None:
        self.assertEqual(visible_status(True, None), "Live")

    def test_offline_cache_shows_timestamp(self) -> None:
        self.assertEqual(
            visible_status(False, "2026-08-24 09:30"),
            "Offline - cached 2026-08-24 09:30",
        )

    def test_offline_without_cache_has_safe_empty_state(self) -> None:
        self.assertEqual(visible_status(False, None), "Offline - no cached data")


if __name__ == "__main__":
    unittest.main()
