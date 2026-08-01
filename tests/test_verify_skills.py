from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest


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


if __name__ == "__main__":
    unittest.main()
