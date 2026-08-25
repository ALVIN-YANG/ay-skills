from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SPEC = importlib.util.spec_from_file_location(
    "run_journey_evals", ROOT / "scripts" / "run_journey_evals.py"
)
assert SPEC and SPEC.loader
journey = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = journey
SPEC.loader.exec_module(journey)


class JourneyEvalTests(unittest.TestCase):
    def test_cross_artifact_terms_are_required_per_file(self) -> None:
        errors = journey.verify_cross_artifact(
            {"cross_artifact": {"required_terms": {"PRD.md": ["Draft", "Conflict"]}}},
            {"PRD.md": b"Draft only"},
        )
        self.assertTrue(any("Conflict" in error for error in errors))

    def test_cross_artifact_verifier_accepts_consistent_handoff(self) -> None:
        errors = journey.verify_cross_artifact(
            {"cross_artifact": {"required_terms": {"PRD.md": ["Draft", "Conflict"]}}},
            {"PRD.md": b"Draft and Conflict"},
        )
        self.assertEqual(errors, [])

    def test_cross_artifact_patterns_reject_explicit_contradiction(self) -> None:
        errors = journey.verify_cross_artifact(
            {
                "cross_artifact": {
                    "required_terms": {"api.md": ["closed", "conflict"]},
                    "forbidden_patterns": {
                        "api.md": [r"closed.{0,80}never.{0,40}(returns|produces).{0,40}conflict"]
                    },
                }
            },
            {"api.md": b"A closed order never returns conflict; it overwrites data."},
        )
        self.assertTrue(any("journey contradictions" in error for error in errors))

    def test_preserved_failure_can_be_rechecked_without_a_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "case"
            workspace = artifact / "workspace"
            messages = artifact / "final-messages"
            workspace.mkdir(parents=True)
            messages.mkdir()
            (workspace / "contract.md").write_text("Stable Conflict contract", encoding="utf-8")
            (messages / "02-review.txt").write_text(
                "BLOCKER_COUNT: 0\nCRITICAL_COUNT: 0\n", encoding="utf-8"
            )
            journey.write_artifact_manifest(artifact)
            result = journey.recheck_journey(
                {
                    "id": "case",
                    "steps": [
                        {"id": "build", "assert": {"expected_created": {"contract.md": 1}}},
                        {
                            "id": "review",
                            "assert": {
                                "expect_no_changes": True,
                                "final_regex": [
                                    r"(?m)^BLOCKER_COUNT: 0\s*$",
                                    r"(?m)^CRITICAL_COUNT: 0\s*$",
                                ],
                            },
                        },
                    ],
                    "cross_artifact": {
                        "required_terms": {"contract.md": ["Conflict"]}
                    },
                    "verify_commands": [["python3", "-c", "print('ok')"]],
                },
                artifact,
                30,
            )
            self.assertTrue(result.passed, result.error)

    def test_recheck_rejects_changed_preserved_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / "case"
            workspace = artifact / "workspace"
            messages = artifact / "final-messages"
            workspace.mkdir(parents=True)
            messages.mkdir()
            (workspace / "contract.md").write_text("original", encoding="utf-8")
            (messages / "01-review.txt").write_text("review", encoding="utf-8")
            journey.write_artifact_manifest(artifact)
            (workspace / "contract.md").write_text("changed", encoding="utf-8")
            self.assertTrue(journey.verify_artifact_manifest(artifact))


if __name__ == "__main__":
    unittest.main()
