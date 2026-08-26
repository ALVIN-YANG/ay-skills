from __future__ import annotations

import importlib.util
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_store_screenshots",
    ROOT / "skills" / "ay-app-store" / "scripts" / "validate_store_screenshots.py",
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    checksum = zlib.crc32(kind)
    checksum = zlib.crc32(payload, checksum)
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", checksum)


def write_png(path: Path, width: int, height: int, alpha: bool = False) -> None:
    color_type = 6 if alpha else 2
    pixel = b"\x10\x20\x30\xff" if alpha else b"\x10\x20\x30"
    rows = b"".join(b"\x00" + pixel * width for _ in range(height))
    path.write_bytes(
        validator.PNG_SIGNATURE
        + png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, color_type, 0, 0, 0))
        + png_chunk(b"IDAT", zlib.compress(rows))
        + png_chunk(b"IEND", b"")
    )


class StoreScreenshotValidationTests(unittest.TestCase):
    def test_accepts_opaque_png_at_an_allowed_size(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            slot = Path(directory)
            write_png(slot / "01.png", 40, 25)

            report = validator.validate_slot(slot, [(40, 25)])

            self.assertTrue(report["valid"])
            self.assertEqual(report["count"], 1)

    def test_rejects_alpha_and_wrong_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            slot = Path(directory)
            write_png(slot / "01.png", 20, 20, alpha=True)

            report = validator.validate_slot(slot, [(40, 25)])

            self.assertFalse(report["valid"])
            self.assertTrue(any("expected 40x25" in issue for issue in report["issues"]))
            self.assertTrue(any("alpha or transparency" in issue for issue in report["issues"]))

    def test_rejects_missing_or_oversized_slots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = validator.validate_slot(root / "missing", [(40, 25)])
            self.assertFalse(missing["valid"])
            self.assertTrue(any("does not exist" in issue for issue in missing["issues"]))

            for index in range(3):
                write_png(root / f"{index}.png", 40, 25)
            oversized = validator.validate_slot(root, [(40, 25)], max_count=2)
            self.assertFalse(oversized["valid"])
            self.assertTrue(any("expected 1-2 images" in issue for issue in oversized["issues"]))


if __name__ == "__main__":
    unittest.main()
