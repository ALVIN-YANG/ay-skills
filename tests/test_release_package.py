from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "package_release", ROOT / "scripts" / "package_release.py"
)
assert SPEC and SPEC.loader
package_release = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = package_release
SPEC.loader.exec_module(package_release)


class ReleasePackageTests(unittest.TestCase):
    def test_archive_matches_checkout_and_contains_every_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "ay-skills.tar.gz"
            package_release.build_archive(archive, ROOT)
            self.assertEqual(package_release.verify_archive(archive, ROOT), [])
            packaged = package_release.manifest(ROOT)["files"]
            self.assertIn("CONTRIBUTING.md", packaged)
            self.assertIn("docs/choosing-a-skill.md", packaged)
            self.assertIn("docs/choosing-a-skill.zh-CN.md", packaged)
            self.assertIn("docs/influences.md", packaged)

    def test_verifier_rejects_unreadable_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "broken.tar.gz"
            archive.write_text("not an archive", encoding="utf-8")
            errors = package_release.verify_archive(archive, ROOT)
            self.assertTrue(any("could not be read" in error for error in errors))

    def test_verifier_rejects_tampered_member_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "tampered.tar.gz"
            package_release.build_archive(
                archive,
                ROOT,
                {"skills/ay-product/SKILL.md": b"tampered\n"},
            )
            errors = package_release.verify_archive(archive, ROOT)
            self.assertTrue(any("hash mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
