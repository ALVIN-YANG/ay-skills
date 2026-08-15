#!/usr/bin/env python3
"""Collect read-only Apple release evidence from a repository.

This scanner deliberately reports facts and evidence gaps. It does not claim that
an app is compliant or ready for App Review.
"""

from __future__ import annotations

import argparse
import json
import plistlib
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


SKIP_DIRS = {
    ".git",
    ".build",
    ".deriveddata",
    ".swiftpm",
    "build",
    "deriveddata",
    "node_modules",
    "pods",
    "carthage",
    "vendor",
}

PROJECT_KEYS = (
    "PRODUCT_BUNDLE_IDENTIFIER",
    "MARKETING_VERSION",
    "CURRENT_PROJECT_VERSION",
    "DEVELOPMENT_TEAM",
    "IPHONEOS_DEPLOYMENT_TARGET",
    "MACOSX_DEPLOYMENT_TARGET",
    "TVOS_DEPLOYMENT_TARGET",
    "WATCHOS_DEPLOYMENT_TARGET",
    "XROS_DEPLOYMENT_TARGET",
    "CODE_SIGN_STYLE",
)

PURPOSE_KEYS = (
    "NSCameraUsageDescription",
    "NSPhotoLibraryUsageDescription",
    "NSPhotoLibraryAddUsageDescription",
    "NSMicrophoneUsageDescription",
    "NSLocationWhenInUseUsageDescription",
    "NSLocationAlwaysAndWhenInUseUsageDescription",
    "NSContactsUsageDescription",
    "NSCalendarsUsageDescription",
    "NSRemindersUsageDescription",
    "NSFaceIDUsageDescription",
    "NSUserTrackingUsageDescription",
    "NSSpeechRecognitionUsageDescription",
    "NSBluetoothAlwaysUsageDescription",
    "NSLocalNetworkUsageDescription",
)

PERMISSION_HINTS = {
    "camera": ("AVCaptureDevice", "UIImagePickerController", ".camera", "cameraDevice"),
    "photos": ("PHPhotoLibrary", "PhotosPicker", "PHPickerViewController"),
    "microphone": ("AVAudioRecorder", "AVAudioSession", "requestRecordPermission"),
    "location": ("CLLocationManager", "requestWhenInUseAuthorization", "requestAlwaysAuthorization"),
    "contacts": ("CNContactStore", "requestAccess(for: .contacts"),
    "tracking": ("ATTrackingManager", "advertisingIdentifier"),
    "face_id": ("LAPolicy", "deviceOwnerAuthenticationWithBiometrics", "LAContext"),
    "local_network": ("NSNetService", "NWBrowser", "MultipeerConnectivity", "MCNearbyService"),
}

SDK_PATTERNS = {
    "Firebase": r"\b(?:import\s+Firebase|Firebase[A-Z]|firebase-ios-sdk)",
    "GoogleAnalytics": r"\b(?:import\s+GoogleAnalytics|GoogleAnalytics)",
    "GoogleSignIn": r"\b(?:import\s+GoogleSignIn|GoogleSignIn-iOS)",
    "Facebook/Meta SDK": r"\b(?:import\s+FacebookCore|FBSDK|facebook-ios-sdk)",
    "Amplitude": r"\b(?:import\s+Amplitude|AmplitudeSwift|amplitude-swift)",
    "Mixpanel": r"\b(?:import\s+Mixpanel|mixpanel-swift)",
    "Sentry": r"\b(?:import\s+Sentry|sentry-cocoa)",
    "AppsFlyer": r"\b(?:import\s+AppsFlyerLib|AppsFlyerLib|appsflyerframework)",
    "Adjust": r"\b(?:import\s+Adjust|AdjustConfig|adjust/ios_sdk)",
    "RevenueCat": r"\b(?:import\s+RevenueCat|Purchases\.configure|purchases-ios)",
    "GoogleMobileAds": r"\b(?:import\s+GoogleMobileAds|GADMobileAds|googleads-mobile-ios-sdk)",
    "StoreKit": r"\b(?:import\s+StoreKit|StoreKit\.)",
    "CloudKit": r"\b(?:import\s+CloudKit|CK(?:Container|Database|Record|SyncEngine|Query|Asset))",
    "AuthenticationServices": r"\b(?:import\s+AuthenticationServices|ASAuthorization)",
}

TEXT_SUFFIXES = {
    ".swift",
    ".m",
    ".mm",
    ".h",
    ".plist",
    ".xcstrings",
    ".json",
    ".md",
    ".txt",
    ".rb",
    ".yml",
    ".yaml",
}


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        lowered_parts = {part.lower() for part in path.relative_to(root).parts[:-1]}
        if lowered_parts & SKIP_DIRS:
            continue
        yield path


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def read_text(path: Path, limit: int = 5_000_000) -> str:
    try:
        if path.stat().st_size > limit:
            return ""
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def unique(values: Iterable[str]) -> list[str]:
    return sorted({value.strip().strip('"') for value in values if value and value.strip()})


def extract_project_settings(paths: list[Path], root: Path) -> tuple[dict[str, list[str]], list[str]]:
    settings: dict[str, list[str]] = defaultdict(list)
    sources: list[str] = []
    for path in paths:
        if path.name != "project.pbxproj":
            continue
        text = read_text(path)
        if not text:
            continue
        sources.append(rel(path, root))
        for key in PROJECT_KEYS:
            pattern = rf"\b{re.escape(key)}\s*=\s*([^;\n]+);"
            settings[key].extend(match.group(1).strip() for match in re.finditer(pattern, text))
    cleaned = {key: unique(values) for key, values in settings.items()}
    return {key: values for key, values in cleaned.items() if values}, sources


def flatten_xcstrings(node: Any, prefix: str = "") -> list[str]:
    values: list[str] = []
    if isinstance(node, dict):
        if isinstance(node.get("value"), str):
            values.append(node["value"])
        for key, value in node.items():
            if key != "value":
                values.extend(flatten_xcstrings(value, f"{prefix}.{key}" if prefix else key))
    elif isinstance(node, list):
        for value in node:
            values.extend(flatten_xcstrings(value, prefix))
    return values


def extract_purpose_strings(paths: list[Path], root: Path) -> tuple[dict[str, list[str]], list[str]]:
    found: dict[str, list[str]] = defaultdict(list)
    sources: list[str] = []
    for path in paths:
        if path.suffix.lower() not in {".plist", ".xcstrings"} and path.name != "project.pbxproj":
            continue
        if not (
            path.name in {"Info.plist", "project.pbxproj"}
            or "InfoPlist" in path.name
            or path.suffix.lower() == ".xcstrings"
        ):
            continue
        recorded = False
        if path.suffix.lower() == ".plist":
            try:
                with path.open("rb") as handle:
                    data = plistlib.load(handle)
                if isinstance(data, dict):
                    for key in PURPOSE_KEYS:
                        value = data.get(key)
                        if isinstance(value, str) and value.strip():
                            found[key].append(value.strip())
                            recorded = True
            except (OSError, plistlib.InvalidFileException):
                pass
        text = read_text(path)
        if not text:
            continue
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = None
        if isinstance(data, dict):
            strings = data.get("strings")
            if isinstance(strings, dict):
                for key in PURPOSE_KEYS:
                    entry = strings.get(key)
                    if entry is not None:
                        values = flatten_xcstrings(entry)
                        found[key].extend(values)
                        recorded = recorded or bool(values)
        for key in PURPOSE_KEYS:
            if key not in text:
                continue
            for pattern in (
                rf"{re.escape(key)}\s*[=:]\s*[\"']([^\"'\n]+)",
                rf"<key>{re.escape(key)}</key>\s*<string>([^<]+)</string>",
                rf"INFOPLIST_KEY_{re.escape(key)}\s*=\s*([^;\n]+);",
            ):
                found[key].extend(match.group(1).strip() for match in re.finditer(pattern, text))
        if recorded or any(key in text for key in PURPOSE_KEYS):
            sources.append(rel(path, root))
    return {key: unique(values) for key, values in found.items()}, unique(sources)


def extract_entitlements(paths: list[Path], root: Path) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for path in paths:
        if path.suffix.lower() != ".entitlements":
            continue
        entry: dict[str, Any] = {"path": rel(path, root), "keys": []}
        try:
            with path.open("rb") as handle:
                data = plistlib.load(handle)
            if isinstance(data, dict):
                entry["keys"] = sorted(data.keys())
                for key in (
                    "aps-environment",
                    "com.apple.developer.icloud-container-identifiers",
                    "com.apple.developer.icloud-services",
                    "com.apple.security.application-groups",
                    "com.apple.developer.associated-domains",
                ):
                    if key in data:
                        entry[key] = data[key]
        except (OSError, plistlib.InvalidFileException) as error:
            entry["error"] = str(error)
        results.append(entry)
    return results


def walk_json(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_json(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_json(value)


def extract_storekit(paths: list[Path], root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    products: dict[str, dict[str, Any]] = {}
    groups: dict[str, dict[str, Any]] = {}
    sources: list[str] = []
    for path in paths:
        if path.suffix.lower() != ".storekit":
            continue
        text = read_text(path)
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            continue
        sources.append(rel(path, root))
        for node in walk_json(data):
            product_id = node.get("productID")
            if isinstance(product_id, str) and product_id:
                products[product_id] = {
                    "productID": product_id,
                    "type": node.get("type"),
                    "displayPrice": node.get("displayPrice"),
                    "familyShareable": node.get("familyShareable"),
                    "period": node.get("recurringSubscriptionPeriod"),
                }
            subscriptions = node.get("subscriptions")
            if isinstance(subscriptions, list) and (node.get("id") or node.get("name")):
                group_key = str(node.get("id") or node.get("name"))
                groups[group_key] = {
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "productIDs": unique(
                        str(item.get("productID"))
                        for item in subscriptions
                        if isinstance(item, dict) and item.get("productID")
                    ),
                }
    return sorted(products.values(), key=lambda item: item["productID"]), sorted(groups.values(), key=lambda item: str(item.get("id"))), unique(sources)


def extract_legal_urls(paths: list[Path]) -> list[str]:
    urls: set[str] = set()
    url_pattern = re.compile(r"https?://[^\s<>\]\[\)\(\"']+")
    legal_terms = ("privacy", "terms", "eula", "legal", "agreement", "policy")
    for path in paths:
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path, limit=2_000_000)
        if not text:
            continue
        for match in url_pattern.findall(text):
            cleaned = match.rstrip(".,;:")
            lowered = cleaned.lower()
            if any(term in lowered for term in legal_terms):
                urls.add(cleaned)
    return sorted(urls)


def scan_code_hints(paths: list[Path], root: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    permission_hits: dict[str, set[str]] = defaultdict(set)
    sdk_hits: dict[str, set[str]] = defaultdict(set)
    for path in paths:
        is_source = path.suffix.lower() in {".swift", ".m", ".mm", ".h"}
        is_dependency_file = path.name in {"Package.resolved", "Podfile", "Cartfile", "project.pbxproj"}
        if not is_source and not is_dependency_file:
            continue
        text = read_text(path, limit=2_000_000)
        if not text:
            continue
        relative = rel(path, root)
        if is_source:
            for category, hints in PERMISSION_HINTS.items():
                if any(hint in text for hint in hints):
                    permission_hits[category].add(relative)
        for sdk, pattern in SDK_PATTERNS.items():
            if re.search(pattern, text):
                sdk_hits[sdk].add(relative)
    return (
        {key: sorted(values)[:20] for key, values in sorted(permission_hits.items())},
        {key: sorted(values)[:20] for key, values in sorted(sdk_hits.items())},
    )


def find_assets(paths: list[Path], root: Path) -> dict[str, Any]:
    image_suffixes = {".png", ".jpg", ".jpeg", ".webp"}
    screenshots: list[str] = []
    icons: list[str] = []
    for path in paths:
        if path.suffix.lower() not in image_suffixes:
            continue
        relative = rel(path, root)
        lowered = relative.lower()
        if any(term in lowered for term in ("screenshot", "app-review", "appstore", "app-store", "marketing")):
            screenshots.append(relative)
        if "appicon" in lowered or "icon" in path.stem.lower():
            icons.append(relative)
    return {
        "screenshot_count": len(screenshots),
        "screenshots": sorted(screenshots)[:50],
        "icon_count": len(icons),
        "icons": sorted(icons)[:30],
    }


def build_gaps(report: dict[str, Any]) -> list[str]:
    gaps: list[str] = []
    project = report["project_settings"]
    if not report["project_files"]:
        gaps.append("No Xcode project.pbxproj was found; project identity could not be extracted.")
    for key in ("PRODUCT_BUNDLE_IDENTIFIER", "MARKETING_VERSION", "CURRENT_PROJECT_VERSION", "DEVELOPMENT_TEAM"):
        if not project.get(key):
            gaps.append(f"No {key} value was found in project files.")
    required_purpose_keys = {
        "camera": ("NSCameraUsageDescription",),
        "microphone": ("NSMicrophoneUsageDescription",),
        "location": ("NSLocationWhenInUseUsageDescription", "NSLocationAlwaysAndWhenInUseUsageDescription"),
        "contacts": ("NSContactsUsageDescription",),
        "tracking": ("NSUserTrackingUsageDescription",),
        "face_id": ("NSFaceIDUsageDescription",),
        "local_network": ("NSLocalNetworkUsageDescription",),
    }
    for category, keys in required_purpose_keys.items():
        if category in report["permission_code_hints"] and not any(key in report["purpose_strings"] for key in keys):
            gaps.append(
                f"{category} code hints were found, but none of {', '.join(keys)} was extracted; inspect the built Info.plist."
            )
    if not report["legal_urls"]:
        gaps.append("No privacy/terms/EULA URL was found in scanned text files.")
    if report["storekit_products"] and not any("StoreKit" in key for key in report["sdk_hints"]):
        gaps.append("StoreKit products were found, but no StoreKit code hint was detected; verify the purchase implementation manually.")
    if not report["privacy_manifests"]:
        gaps.append("No PrivacyInfo.xcprivacy was found; determine from current Apple rules and included SDKs whether one is required.")
    if report["assets"]["screenshot_count"] == 0:
        gaps.append("No likely App Store/review screenshots were found in the repository.")
    return gaps


def make_report(root: Path) -> dict[str, Any]:
    paths = list(iter_files(root))
    project_settings, project_files = extract_project_settings(paths, root)
    purpose_strings, purpose_sources = extract_purpose_strings(paths, root)
    products, groups, storekit_sources = extract_storekit(paths, root)
    permission_hints, sdk_hints = scan_code_hints(paths, root)
    report: dict[str, Any] = {
        "scanner": "ay-app-store/scan_apple_release.py",
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "files_scanned": len(paths),
        "project_files": project_files,
        "project_settings": project_settings,
        "purpose_string_sources": purpose_sources,
        "purpose_strings": purpose_strings,
        "entitlements": extract_entitlements(paths, root),
        "privacy_manifests": sorted(rel(path, root) for path in paths if path.name == "PrivacyInfo.xcprivacy"),
        "storekit_sources": storekit_sources,
        "storekit_products": products,
        "storekit_subscription_groups": groups,
        "legal_urls": extract_legal_urls(paths),
        "permission_code_hints": permission_hints,
        "sdk_hints": sdk_hints,
        "assets": find_assets(paths, root),
    }
    report["evidence_gaps"] = build_gaps(report)
    return report


def markdown_list(values: Iterable[str], empty: str = "None found") -> list[str]:
    items = list(values)
    return [f"- {value}" for value in items] if items else [f"- {empty}"]


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Apple Release Evidence Scan",
        "",
        f"- Root: `{report['root']}`",
        f"- Scanned at: `{report['scanned_at']}`",
        f"- Files scanned: `{report['files_scanned']}`",
        "- Meaning: read-only evidence inventory; not a compliance or submission verdict.",
        "",
        "## Project identity",
        "",
    ]
    if report["project_settings"]:
        for key, values in report["project_settings"].items():
            lines.append(f"- {key}: {', '.join(f'`{value}`' for value in values)}")
    else:
        lines.append("- No build settings extracted")
    lines.extend(["", "Project files:", ""])
    lines.extend(markdown_list((f"`{value}`" for value in report["project_files"])))

    lines.extend(["", "## Permission purpose strings", ""])
    if report["purpose_strings"]:
        for key, values in report["purpose_strings"].items():
            lines.append(f"- {key}: {' | '.join(values)}")
    else:
        lines.append("- None extracted")
    lines.extend(["", "Permission-related code hints:", ""])
    if report["permission_code_hints"]:
        for key, paths in report["permission_code_hints"].items():
            lines.append(f"- {key}: {', '.join(f'`{path}`' for path in paths)}")
    else:
        lines.append("- None found")

    lines.extend(["", "## Entitlements and privacy", ""])
    if report["entitlements"]:
        for entry in report["entitlements"]:
            lines.append(f"- `{entry['path']}`: {', '.join(entry.get('keys', [])) or 'no keys extracted'}")
    else:
        lines.append("- No .entitlements files found")
    lines.append(f"- Privacy manifests: {', '.join(f'`{path}`' for path in report['privacy_manifests']) or 'None found'}")
    lines.extend(["", "SDK/framework hints:", ""])
    if report["sdk_hints"]:
        for key, paths in report["sdk_hints"].items():
            lines.append(f"- {key}: {', '.join(f'`{path}`' for path in paths)}")
    else:
        lines.append("- None found")

    lines.extend(["", "## StoreKit configuration", ""])
    if report["storekit_products"]:
        lines.append("| Product ID | Type | Price | Period | Family Sharing |")
        lines.append("| --- | --- | --- | --- | --- |")
        for product in report["storekit_products"]:
            lines.append(
                "| `{}` | {} | {} | {} | {} |".format(
                    product.get("productID", ""),
                    product.get("type") or "",
                    product.get("displayPrice") or "",
                    product.get("period") or "",
                    product.get("familyShareable") if product.get("familyShareable") is not None else "",
                )
            )
    else:
        lines.append("- No .storekit products extracted")
    if report["storekit_subscription_groups"]:
        lines.extend(["", "Subscription groups:", ""])
        for group in report["storekit_subscription_groups"]:
            lines.append(f"- {group.get('name') or group.get('id')}: {', '.join(group.get('productIDs', []))}")

    lines.extend(["", "## Legal URLs", ""])
    lines.extend(markdown_list(report["legal_urls"]))
    lines.extend(["", "## Assets", ""])
    lines.append(f"- Likely screenshots: {report['assets']['screenshot_count']}")
    lines.extend(markdown_list((f"`{path}`" for path in report["assets"]["screenshots"]), empty="No screenshot paths listed"))
    lines.append(f"- Likely icons: {report['assets']['icon_count']}")
    lines.extend(markdown_list((f"`{path}`" for path in report["assets"]["icons"]), empty="No icon paths listed"))

    lines.extend(["", "## Evidence gaps to inspect", ""])
    lines.extend(markdown_list(report["evidence_gaps"], empty="No scanner-level gaps found; live App Store Connect checks are still required."))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root to scan")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2
    report = make_report(root)
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
