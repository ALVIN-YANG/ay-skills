from __future__ import annotations

import importlib.util
import binascii
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "run_behavior_evals", ROOT / "scripts" / "run_behavior_evals.py"
)
assert SPEC and SPEC.loader
behavior = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = behavior
SPEC.loader.exec_module(behavior)


def rgb_png(width: int, height: int) -> bytes:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        checksum = binascii.crc32(kind + payload) & 0xFFFFFFFF
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    rows = b"".join(b"\x00" + b"\x00\x00\x80" * width for _ in range(height))
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b"")


class BehaviorEvalTests(unittest.TestCase):
    def test_network_disconnect_is_infrastructure_error(self) -> None:
        self.assertTrue(
            behavior.is_infrastructure_error_text(
                "failed to lookup address information; stream disconnected before completion"
            )
        )

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
            {
                "expected_created": {"article.md": 10},
                "created_all": {"article.md": ["evidence", "boundary"]},
                "final_any": ["article.md"],
            },
            {},
            {"article.md": b"Evidence makes the boundary testable."},
            "Created article.md",
        )
        self.assertEqual(errors, [])

    def test_verify_result_reports_missing_created_content(self) -> None:
        errors = behavior.verify_result(
            {"created_all": {"api.md": ["authorization", "idempotency"]}},
            {},
            {"api.md": b"Authorization is defined."},
            "Created api.md",
        )
        self.assertTrue(any("idempotency" in error for error in errors))

    def test_verify_result_rejects_forbidden_created_content(self) -> None:
        errors = behavior.verify_result(
            {"created_none": {"ios-api.md": ["ReportRepository", "/v1/admin"]}},
            {},
            {"ios-api.md": b"POST /v1/reports\nInternal: ReportRepository"},
            "Created ios-api.md",
        )
        self.assertTrue(any("ReportRepository" in error for error in errors))

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

    def test_verify_result_checks_structured_final_pattern(self) -> None:
        self.assertEqual(
            behavior.verify_result(
                {"final_regex": [r"(?m)^BLOCKER_COUNT: 0$"]},
                {},
                {},
                "Review complete\nBLOCKER_COUNT: 0\n",
            ),
            [],
        )
        errors = behavior.verify_result(
            {"final_regex": [r"(?m)^BLOCKER_COUNT: 0$"]},
            {},
            {},
            "BLOCKER_COUNT: 2",
        )
        self.assertTrue(any("required pattern" in error for error in errors))

    def test_verify_result_checks_png_dimensions_and_alpha(self) -> None:
        errors = behavior.verify_result(
            {"expected_png": {"deck.png": {"width": 12, "height": 8, "alpha": False}}},
            {},
            {"deck.png": rgb_png(12, 8)},
            "Created deck",
        )
        self.assertEqual(errors, [])

    def test_verify_result_rejects_svg_with_wrong_size(self) -> None:
        errors = behavior.verify_result(
            {"expected_svg": {"screen.svg": {"width": 390, "height": 844, "contains": ["Retry"]}}},
            {},
            {"screen.svg": b'<svg width="400" height="844"><text>Retry</text></svg>'},
            "Created screen",
        )
        self.assertTrue(any("expected 390x844" in error for error in errors))

    def test_verify_result_rejects_truncated_png(self) -> None:
        truncated = rgb_png(12, 8)[:33]
        errors = behavior.verify_result(
            {"expected_png": {"deck.png": {"width": 12, "height": 8, "alpha": False}}},
            {},
            {"deck.png": truncated},
            "Created deck",
        )
        self.assertTrue(any("IEND" in error or "image data" in error for error in errors))

    def test_svg_comments_do_not_count_as_visible_text(self) -> None:
        errors = behavior.verify_result(
            {"expected_svg": {"screen.svg": {"width": 390, "height": 844, "contains": ["Retry"]}}},
            {},
            {"screen.svg": b'<svg width="390" height="844"><!-- Retry --><rect width="10" height="10"/></svg>'},
            "Created screen",
        )
        self.assertTrue(any("missed visible terms" in error for error in errors))

    def test_verify_result_protects_fixture_tests(self) -> None:
        errors = behavior.verify_result(
            {"unchanged_files": ["tests/test_app.py"]},
            {"tests/test_app.py": b"assert old"},
            {"tests/test_app.py": b"assert True"},
            "Tests passed",
        )
        self.assertTrue(any("must remain unchanged" in error for error in errors))

    def test_fixture_catalog_installs_ay_and_competitor_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory) / "skills"
            installed.mkdir()
            behavior.install_catalog(installed, "ay-product", "fixture")
            self.assertTrue((installed / "ay-product" / "SKILL.md").is_file())
            self.assertTrue((installed / "ship-app-store" / "SKILL.md").is_file())

    def test_reproduction_rejects_output_changed_by_the_model(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            generator = workspace / "render.py"
            generator.write_text(
                "from pathlib import Path\nPath('output.txt').write_text('clean')\n",
                encoding="utf-8",
            )
            (workspace / "output.txt").write_text("invented", encoding="utf-8")
            errors = behavior.verify_reproducible_outputs(
                workspace,
                behavior.snapshot(workspace),
                [{"path": "output.txt", "command": ["python3", "render.py"]}],
                30,
            )
            self.assertTrue(any("differs from clean reproduction" in error for error in errors))

    def test_reproduction_requires_command_to_create_the_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)
            (workspace / "output.txt").write_text("preexisting", encoding="utf-8")
            errors = behavior.verify_reproducible_outputs(
                workspace,
                behavior.snapshot(workspace),
                [{"path": "output.txt", "command": ["python3", "-c", "pass"]}],
                30,
            )
            self.assertTrue(any("did not create output" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
