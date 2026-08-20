# Store screenshot workflow

Use this reference for App Store upload candidates, not ordinary product UI design. Checked against Apple sources on 2026-08-20; refresh them before each release because device slots and accepted sizes change.

## Establish the target

Confirm the app, release build, platforms, device classes, orientations, locales, screenshot slots, and current Apple dimensions. Apple currently accepts one to ten JPEG or PNG screenshots per slot and rejects alpha or transparency. Mac screenshots use an accepted 16:10 size, including 2880×1800. Treat the current App Store Connect form and [Apple screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications) as authoritative.

Define the ordered story from approved product claims. Lead with the strongest user outcome, give each slide one job, and keep copy factual and readable at storefront-thumbnail size. Disclose paid requirements when the depicted capability needs an in-app purchase. If visual direction is unsettled, present one deck direction and one representative slide for approval.

## Capture the shipped product

Run the current release candidate and capture the real app on the target simulator, device, or Mac at native scale. Prefer deterministic fictional demo data or fixtures; never expose a real person's account, network, hardware, or location data. Remove cursors, selection handles, debug overlays, failure alerts, and unrelated system UI before capture.

The visible app surface in an upload candidate must remain an exact captured layer. Crop or mask private fields and scale proportionally, but do not stretch, repaint, regenerate, or silently improve controls, text, content, or product states. Recapture after material UI changes. Image generation may explore art direction or create truthful background decoration; it must not fabricate the app itself.

Apple requires screenshots to show the app in use and accurately reflect its core experience. Review [App Review Guidelines 2.3](https://developer.apple.com/app-store/review/guidelines/#accurate-metadata) before finalizing claims, content, or overlays.

## Compose reproducibly

Render directly at each final target resolution with local fonts. Preserve the capture's aspect ratio with deliberate fit, fill, or crop behavior. Keep headings, decoration, and device framing outside the exact app layer unless the overlay truthfully explains interaction.

Prefer an existing project renderer or deck format. Otherwise create the smallest project-local reproducible renderer using the repository's current stack; adding a dependency, paid service, or hosted editor needs approval. Preserve source paths, slide order, copy, locales, target sizes, crop coordinates, and export command in code or data. Keep private raw captures out of Git while retaining enough instructions to recapture them.

## Validate the exported files

Inspect the final exported pixels, not only the editor preview. Verify:

- accepted dimensions, orientation, JPEG/PNG encoding, no alpha, and no unintended upscaling;
- proportional UI geometry, complete text, safe margins, consistent visual system, and useful variation across the set;
- OCR or an independent copy check for every locale, including punctuation, glyphs, truncation, and right-to-left layout where applicable;
- readable thumbnails, truthful claims, current shipped features, paid-feature disclosure, fictional data, content rights, and no private or debug material;
- a clean re-export from the saved renderer or deck state produces the same upload candidates.

Keep experiments separate from upload candidates. Report generation, visual inspection, App Store upload acceptance, and submission as separate evidence layers.

## Implementation influences

This original workflow uses ideas, not copied code or text, from:

- [iamngoni/store-screenshot-mockups](https://github.com/iamngoni/store-screenshot-mockups): exact real-UI layers and separation of exploratory generated art from upload candidates.
- [ParthJadhav/app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots) (MIT): ordered marketing stories, thumbnail-readable copy, reproducible deck state, and exact exports.
- [gyugyu86/app-store-screenshot-studio](https://github.com/gyugyu86/app-store-screenshot-studio) (MIT; bundled fonts under OFL-1.1): local rendering, proportional fit/fill, localization, and opaque exports.
