#!/usr/bin/env python3
"""Validate one App Store Connect screenshot slot without external packages."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import struct
import sys
from typing import Iterable


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}
IMAGE_SUFFIXES = {".jpeg", ".jpg", ".png"}


@dataclass(frozen=True)
class ImageInfo:
    path: str
    format: str
    width: int
    height: int
    alpha: bool


def inspect_png(path: Path, data: bytes) -> ImageInfo:
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("extension is PNG but signature is not")

    offset = len(PNG_SIGNATURE)
    width = height = color_type = None
    transparency = False
    reached_end = False

    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        chunk_type = data[offset + 4 : offset + 8]
        chunk_end = offset + 12 + length
        if chunk_end > len(data):
            raise ValueError("truncated PNG chunk")

        if chunk_type == b"IHDR":
            if length != 13:
                raise ValueError("invalid PNG IHDR")
            width, height = struct.unpack_from(">II", data, offset + 8)
            color_type = data[offset + 17]
        elif chunk_type == b"tRNS":
            transparency = True
        elif chunk_type == b"IEND":
            reached_end = True
            break
        offset = chunk_end

    if width is None or height is None or color_type is None or not reached_end:
        raise ValueError("incomplete PNG")
    alpha = color_type in {4, 6} or transparency
    return ImageInfo(str(path), "PNG", width, height, alpha)


def inspect_jpeg(path: Path, data: bytes) -> ImageInfo:
    if not data.startswith(b"\xff\xd8"):
        raise ValueError("extension is JPEG but signature is not")

    offset = 2
    while offset < len(data):
        while offset < len(data) and data[offset] != 0xFF:
            offset += 1
        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            break

        marker = data[offset]
        offset += 1
        if marker in {0x01, 0xD8, 0xD9} or 0xD0 <= marker <= 0xD7:
            continue
        if offset + 2 > len(data):
            break

        length = struct.unpack_from(">H", data, offset)[0]
        if length < 2 or offset + length > len(data):
            raise ValueError("truncated JPEG segment")
        if marker in JPEG_SOF_MARKERS:
            if length < 7:
                raise ValueError("invalid JPEG frame")
            height, width = struct.unpack_from(">HH", data, offset + 3)
            return ImageInfo(str(path), "JPEG", width, height, False)
        offset += length

    raise ValueError("JPEG dimensions not found")


def inspect_image(path: Path) -> ImageInfo:
    data = path.read_bytes()
    if path.suffix.lower() == ".png":
        return inspect_png(path, data)
    return inspect_jpeg(path, data)


def validate_slot(
    directory: Path,
    allowed_sizes: Iterable[tuple[int, int]],
    min_count: int = 1,
    max_count: int = 10,
) -> dict[str, object]:
    allowed = set(allowed_sizes)
    files = sorted(
        path for path in directory.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    ) if directory.is_dir() else []
    issues: list[str] = []
    inspected: list[ImageInfo] = []

    if not directory.is_dir():
        issues.append(f"slot directory does not exist: {directory}")
    if not min_count <= len(files) <= max_count:
        issues.append(f"expected {min_count}-{max_count} images, found {len(files)}")

    for path in files:
        try:
            info = inspect_image(path)
        except (OSError, ValueError) as error:
            issues.append(f"{path.name}: {error}")
            continue
        inspected.append(info)
        if (info.width, info.height) not in allowed:
            expected = ", ".join(f"{width}x{height}" for width, height in sorted(allowed))
            issues.append(f"{path.name}: {info.width}x{info.height}, expected {expected}")
        if info.alpha:
            issues.append(f"{path.name}: PNG contains alpha or transparency")

    return {
        "slot": str(directory),
        "allowed_sizes": [f"{width}x{height}" for width, height in sorted(allowed)],
        "count": len(files),
        "files": [asdict(info) for info in inspected],
        "issues": issues,
        "valid": not issues,
    }


def parse_size(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"([1-9][0-9]*)[xX×]([1-9][0-9]*)", value.strip())
    if not match:
        raise argparse.ArgumentTypeError("size must look like WIDTHxHEIGHT")
    return int(match.group(1)), int(match.group(2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="one locale and device-slot directory")
    parser.add_argument(
        "--size",
        action="append",
        required=True,
        type=parse_size,
        dest="sizes",
        help="accepted WIDTHxHEIGHT; repeat for alternate accepted sizes",
    )
    parser.add_argument("--min-count", type=int, default=1)
    parser.add_argument("--max-count", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="emit a machine-readable report")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.min_count < 0 or args.max_count < args.min_count:
        raise SystemExit("invalid count range")

    report = validate_slot(args.directory, args.sizes, args.min_count, args.max_count)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        status = "PASS" if report["valid"] else "FAIL"
        print(f"{status}: {report['slot']} ({report['count']} images)")
        for file_report in report["files"]:
            alpha = "alpha" if file_report["alpha"] else "opaque"
            print(
                f"- {Path(file_report['path']).name}: {file_report['width']}x{file_report['height']} "
                f"{file_report['format']} {alpha}"
            )
        for issue in report["issues"]:
            print(f"- ERROR: {issue}", file=sys.stderr)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
