import unittest

from src.job_report import submit_report


class JobReportTests(unittest.TestCase):
    def test_open_work_order_accepts_once(self) -> None:
        result = submit_report("Assigned", "pump replaced", "idem-1")
        self.assertEqual(
            result,
            {"decision": "Submitted", "idempotencyKey": "idem-1"},
        )

    def test_closed_work_order_preserves_draft(self) -> None:
        result = submit_report("Closed", "pump replaced", "idem-2")
        self.assertEqual(
            result,
            {
                "decision": "Conflict",
                "conflictReason": "WorkOrderClosed",
                "draftPreserved": True,
                "idempotencyKey": "idem-2",
            },
        )

    def test_unknown_work_order_state_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            submit_report("unknown", "pump replaced", "idem-3")

    def test_required_inputs_are_not_silently_accepted(self) -> None:
        with self.assertRaises(ValueError):
            submit_report("Assigned", "", "idem-4")
        with self.assertRaises(ValueError):
            submit_report("Assigned", "pump replaced", "")
        with self.assertRaises(ValueError):
            submit_report("Assigned", "   ", "idem-5")
        with self.assertRaises(ValueError):
            submit_report("Assigned", "pump replaced", "   ")


if __name__ == "__main__":
    unittest.main()
