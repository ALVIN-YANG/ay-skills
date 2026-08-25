import unittest

from src.review_decision import next_action


class ReviewDecisionTests(unittest.TestCase):
    def test_ready_selected_pair_can_request_trash(self) -> None:
        self.assertEqual(next_action("ready", ("right.jpg",)), "confirm-trash")

    def test_nothing_is_deleted_automatically(self) -> None:
        self.assertEqual(next_action("ready", ()), "keep-reviewing")
        self.assertEqual(next_action("failed", ("right.jpg",)), "retry-scan")

    def test_multiple_selected_files_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            next_action("ready", ("left.jpg", "right.jpg"))

    def test_non_review_states_do_not_enter_the_review_queue(self) -> None:
        self.assertEqual(next_action("scanning", ()), "wait-for-scan")
        self.assertEqual(next_action("cancelled", ()), "restart-scan")
        with self.assertRaises(ValueError):
            next_action("unknown", ())


if __name__ == "__main__":
    unittest.main()
