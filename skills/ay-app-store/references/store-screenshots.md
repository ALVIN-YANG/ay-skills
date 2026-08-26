# Store screenshot workflow

Use this reference for Apple App Store screenshot upload candidates, not product UI design or release operations. Apple sources were refreshed on 2026-08-26; check them again for every release.

## Establish the target and story

Confirm the app and release build, platforms, device classes, orientations, locales, screenshot slots, and current dimensions. Treat the live App Store Connect form and [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) as authoritative. Apple currently accepts one to ten JPEG or PNG files per slot and rejects alpha or transparency.

Order the deck around approved product claims. Lead with the strongest user outcome, give each slide one job, and make its headline readable at storefront-thumbnail size. Disclose paid requirements when a depicted capability needs an in-app purchase. If the story or visual direction is unsettled, present one recommended deck direction and one representative slide for approval.

## Capture the shipped product

Run the current release candidate and capture it on the target simulator, device, or Mac at native scale. Use an existing demo account or deterministic fictional data. Never expose a real person's account, network, hardware, health, financial, or location data. Remove cursors, debug overlays, failure alerts, and unrelated system UI before capture.

The app surface in an upload candidate must remain an exact captured layer. Scale proportionally and crop only with intent; never stretch, repaint, regenerate, or silently improve controls, text, content, or product states. Recapture after material UI changes. Image generation may explore art direction or create truthful background decoration, but it must not fabricate the app itself.

Apple requires metadata and screenshots to match the current core experience. Review [App Review Guidelines 2.3](https://developer.apple.com/app-store/review/guidelines/#accurate-metadata) before finalizing claims, overlays, or paid-feature disclosure.

## Compose reproducibly

Separate capture, composition, and export. Prefer the project's existing renderer. Otherwise create the smallest local renderer in the current stack; do not scaffold a large editor when a data file plus a short render command is enough.

Keep one canonical deck state in code or structured data. Record source paths or recapture instructions, release build, slide order, copy by locale, target sizes, fit/fill/crop behavior, fonts, colors, and export command. Keep private raw captures out of Git. Use stable output folders such as `store-screenshots/<device>/<locale>/` so one directory maps to one App Store Connect slot.

Render directly at each final size with local fonts. Connected multi-slide art is acceptable only when every exported crop also works alone and no required copy or critical UI is split. Recheck line breaks for every locale; translation alone does not prove layout. Treat right-to-left decks as distinct compositions.

## Validate the exported files

Run the bundled validator once per slot directory with dimensions taken from current Apple documentation:

```bash
python3 scripts/validate_store_screenshots.py store-screenshots/mac/en-US --size 2880x1800
```

Then inspect the final pixels and thumbnails. Verify proportional UI geometry, complete copy and glyphs, readable hierarchy, safe margins, useful variation, truthful claims, fictional data, rights, and no private or debug material. Re-export from saved state and compare the outputs. Keep experiments outside upload-candidate folders.

Report rendering, script validation, visual inspection, upload acceptance, and submission as separate evidence. This skill stops before upload.

## Open-source influences

AY uses original instructions and validator code. The workflow borrows patterns, not text or runtime code, from these reviewed projects:

- [ParthJadhav/app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) (MIT): canonical JSON deck state, locale/device export bundles, thumbnail-first copy, and resumable editing.
- [gyugyu86/app-store-screenshot-studio](https://github.com/gyugyu86/app-store-screenshot-studio) (MIT; bundled fonts OFL-1.1): local-only rendering, proportional fit/fill, saved deck state, and opaque exports.
- [thiagoperes/ai-appshots](https://github.com/thiagoperes/ai-appshots) (MIT): configuration-driven capture/composition/export and validation before staging.
- [fastlane/fastlane](https://github.com/fastlane/fastlane) (MIT): reproducible capture and locale-oriented screenshot organization in existing release automation.
