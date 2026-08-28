from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_skills", ROOT / "scripts" / "verify_skills.py"
)
assert SPEC and SPEC.loader
verify_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verify_skills)


class VerifySkillsTests(unittest.TestCase):
    def test_repository_passes(self) -> None:
        self.assertEqual(verify_skills.validate(ROOT), [])

    def test_contract_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "checkout"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            skill = checkout / "skills" / "ay-fix" / "SKILL.md"
            text = skill.read_text(encoding="utf-8")
            skill.write_text(
                text.replace("Verify the real requested outcome", "Assume the requested outcome"),
                encoding="utf-8",
            )
            errors = verify_skills.validate(checkout)
            self.assertTrue(any("approval contract drifted" in error for error in errors))

    def test_extra_frontmatter_field_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill_file = Path(directory) / "SKILL.md"
            skill_file.write_text(
                "---\nname: demo\ndescription: Use when testing.\nextra: no\n---\nBody\n",
                encoding="utf-8",
            )
            fields, _ = verify_skills.parse_frontmatter(skill_file)
            self.assertEqual(set(fields), {"name", "description", "extra"})

    def test_manifest_version_drift_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "checkout"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            manifest = checkout / ".codex-plugin" / "plugin.json"
            version = checkout.joinpath("VERSION").read_text(encoding="utf-8").strip()
            text = manifest.read_text(encoding="utf-8")
            manifest.write_text(
                text.replace(f'"version": "{version}"', '"version": "9.9.9"', 1),
                encoding="utf-8",
            )
            errors = verify_skills.validate(checkout)
            self.assertTrue(any("version must match VERSION" in error for error in errors))

    def test_release_tag_must_match_version(self) -> None:
        with patch.dict(
            "os.environ",
            {"GITHUB_REF_TYPE": "tag", "GITHUB_REF_NAME": "v9.9.9"},
            clear=False,
        ):
            errors = verify_skills.validate(ROOT)
        self.assertTrue(any("release tag must match VERSION" in error for error in errors))

    def test_execution_case_needs_observable_assertion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "checkout"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            scenarios = checkout / "tests" / "execution-scenarios.json"
            data = json.loads(scenarios.read_text(encoding="utf-8"))
            for key in (
                "expect_no_changes",
                "expected_files",
                "expected_created",
                "created_all",
                "final_any",
                "final_all",
                "final_none",
            ):
                data[0].pop(key, None)
            scenarios.write_text(json.dumps(data), encoding="utf-8")
            errors = verify_skills.validate(checkout)
            self.assertTrue(any("missing observable assertion" in error for error in errors))

    def test_execution_case_rejects_non_boolean_extra_change_flag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            checkout = Path(directory) / "checkout"
            shutil.copytree(ROOT, checkout, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            scenarios = checkout / "tests" / "execution-scenarios.json"
            data = json.loads(scenarios.read_text(encoding="utf-8"))
            data[0]["allow_extra_changes"] = "false"
            scenarios.write_text(json.dumps(data), encoding="utf-8")
            errors = verify_skills.validate(checkout)
            self.assertTrue(any("allow_extra_changes must be a boolean" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
