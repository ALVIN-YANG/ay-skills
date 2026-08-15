from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import plistlib
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "scan_apple_release",
    ROOT / "skills" / "ay-app-store" / "scripts" / "scan_apple_release.py",
)
assert SPEC and SPEC.loader
scanner = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scanner
SPEC.loader.exec_module(scanner)


class AppleReleaseScanTests(unittest.TestCase):
    def test_report_collects_release_evidence_without_claiming_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            project = root / "Demo.xcodeproj"
            project.mkdir()
            project.joinpath("project.pbxproj").write_text(
                "PRODUCT_BUNDLE_IDENTIFIER = com.example.demo;\n"
                "MARKETING_VERSION = 1.2;\n"
                "CURRENT_PROJECT_VERSION = 7;\n"
                "DEVELOPMENT_TEAM = TEAM123;\n",
                encoding="utf-8",
            )
            with root.joinpath("Info.plist").open("wb") as handle:
                plistlib.dump(
                    {"NSCameraUsageDescription": "Capture a document selected by the user."},
                    handle,
                )
            root.joinpath("PrivacyInfo.xcprivacy").write_text("{}\n", encoding="utf-8")
            root.joinpath("Products.storekit").write_text(
                json.dumps({"products": [{"productID": "com.example.demo.full", "type": "NonConsumable"}]}),
                encoding="utf-8",
            )
            root.joinpath("App.swift").write_text(
                "import StoreKit\nlet privacy = \"https://example.com/privacy\"\n",
                encoding="utf-8",
            )

            report = scanner.make_report(root)

            self.assertEqual(report["project_settings"]["PRODUCT_BUNDLE_IDENTIFIER"], ["com.example.demo"])
            self.assertEqual(report["purpose_strings"]["NSCameraUsageDescription"], ["Capture a document selected by the user."])
            self.assertEqual(report["storekit_products"][0]["productID"], "com.example.demo.full")
            self.assertEqual(report["privacy_manifests"], ["PrivacyInfo.xcprivacy"])
            self.assertNotIn("ready", report)


if __name__ == "__main__":
    unittest.main()
