---
name: ay-app-store
description: Create and validate reproducible Apple App Store screenshot decks from exact shipped UI captures. Use when asked for App Store 宣传图, localized screenshot sets, device framing, marketing copy overlays, exact-size exports, or screenshot truth checks. Do not use for build upload, submission, review status, StoreKit or privacy setup, app icons, product UI design, or application implementation.
---

# AY App Store Screenshots

Turn current shipped UI into truthful, reproducible upload candidates. Stop before App Store Connect upload or other release work.

## Approval contract

<!-- ay-contract:start -->
- Read the full request and investigate discoverable facts before asking the user.
- Treat review, diagnosis, explanation, and planning as read-only unless the user also requests change.
- Treat a precise instruction as approval when target, observable result, and acceptance boundary are clear.
- A broad outcome authorizes investigation, not file or artifact changes based on choices the agent must invent.
- For a materially underspecified change, present one recommended proposal and wait for approval.
- After approval, execute autonomously inside the approved boundary; do not ask about ordinary implementation details.
- Reopen approval only when new evidence changes behavior, architecture, data contracts, dependencies, scope, risk, cost, rollback, or external actions.
- Perform external actions only when the request or approved proposal includes them. Confirm the exact target before an irreversible action.
- Preserve unrelated and user-authored work. Verify the real requested outcome before claiming completion.
<!-- ay-contract:end -->

## Build the deck

Read [the screenshot workflow](references/store-screenshots.md). Establish the release build, source captures, device slots, orientations, locales, ordered claims, and current Apple dimensions. If art direction is open, propose one direction and one representative slide before producing the set.

Capture the running release candidate. Keep its visible app surface as an exact proportional layer; do not repaint, regenerate, or silently improve the product UI. Do not change application code merely to create a better screenshot. Use fictional data and recapture when the shipped UI changes.

Prefer an existing project renderer. Otherwise create the smallest local, data-driven renderer that fits the repository stack. Installing a dependency, copying a third-party template, or using a hosted service needs approval. Persist source paths, slide order, copy, locales, target sizes, crop behavior, and the export command so another machine can reproduce the deck.

## Prove the exports

Inspect final pixels and storefront-size thumbnails. Check truthful claims, paid-feature disclosure, private data, copy, glyphs, truncation, safe margins, proportional geometry, and right-to-left layouts where relevant.

Run `python3 scripts/validate_store_screenshots.py <slot-directory> --size WIDTHxHEIGHT` once per locale and device slot. It checks count, encoding, exact dimensions, and PNG transparency without external packages; it does not replace visual inspection or current Apple documentation.

Finish with the source-to-output mapping, export command, validation results, and any unverified device or locale. Keep experiments outside upload-candidate directories and hand upload, submission, review, and rejection work to a release workflow.
