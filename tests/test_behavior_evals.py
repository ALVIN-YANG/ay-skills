from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_behavior_evals", ROOT / "scripts" / "run_behavior_evals.py"
)
assert SPEC and SPEC.loader
behavior = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = behavior
SPEC.loader.exec_module(behavior)


class BehaviorEvalTests(unittest.TestCase):
    def test_changed_paths_detects_create_edit_and_delete(self) -> None:
        before = {"edit.txt": b"old", "delete.txt": b"gone", "same.txt": b"same"}
        after = {"edit.txt": b"new", "create.txt": b"new", "same.txt": b"same"}
        self.assertEqual(
            behavior.changed_paths(before, after),
            {"edit.txt", "delete.txt", "create.txt"},
        )

    def test_verify_result_rejects_unapproved_changes(self) -> None:
        errors = behavior.verify_result(
            {"expect_no_changes": True, "final_any": ["cause"]},
            {"app.py": b"old"},
            {"app.py": b"new"},
            "Confirmed cause",
        )
        self.assertTrue(any("unexpected changes" in error for error in errors))

    def test_verify_result_checks_created_artifact(self) -> None:
        errors = behavior.verify_result(
            {"expected_created": {"article.md": 10}, "final_any": ["article.md"]},
            {},
            {"article.md": b"long enough article"},
            "Created article.md",
        )
        self.assertEqual(errors, [])

    def test_verify_result_checks_required_and_forbidden_terms(self) -> None:
        errors = behavior.verify_result(
            {
                "final_all": ["target user", "non-goal"],
                "final_none": ["guaranteed demand"],
            },
            {},
            {},
            "Target user: technicians. Non-goal: automated diagnosis.",
        )
        self.assertEqual(errors, [])

    def test_verify_result_reports_term_failures(self) -> None:
        errors = behavior.verify_result(
            {
                "final_all": ["target user", "acceptance"],
                "final_none": ["guaranteed demand"],
            },
            {},
            {},
            "Target user: technicians. This has guaranteed demand.",
        )
        self.assertTrue(any("acceptance" in error for error in errors))
        self.assertTrue(any("guaranteed demand" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
