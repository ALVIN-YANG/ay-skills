---
name: ay-icon
description: Design and ship store-ready app icons for iOS, iPadOS, macOS, and Android. Use when creating, replacing, or restyling an App Store, Play Store, or launcher icon, AppIcon, .icns, adaptive icon, or 1024 marketing icon, or when the user says the icon is ugly, wants a new icon, 换图标, 重做图标, 上架图标, or 图标太丑. Do not use for in-app UI glyphs, favicons-only work, article figures, or brand systems without a store-icon deliverable.
---

# AY Icon

Turn a product into a store-readable icon. Lock the mark once, then generate, inspect, and install.

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

## Decide the mark

Read the product, current icon, platform, and destination catalog. Infer the job the mark must communicate at 16–32px.

Do not default to a mouse, cursor, letter, or the most literal object. Choose one archetype: object, abstract form, hybrid, or character. Use a character only when the product is clearly character-led.

A request that names metaphor, style, and destination is approval. If those are open, present one recommended direction, two rejected alternatives, and wait.

## Generate

Use already available image generation. Do not add a paid API, CLI, or dependency without approval.

- Square full-bleed artwork. No baked rounded-square plate, device frame, or extra margin.
- No letters, numbers, watermarks, or real brand marks.
- One dominant subject filling most of the canvas. Readable when blurred to about 64px.
- Default to a matte illustration unless the user asked for glass, clay, sketch, or similar.
- Keep metaphor and palette stable across sizes and appearances.

Generate three or four candidates. Inspect each against these rules before showing a pick. Reject oily default 3D, blob-like animals, and marks that vanish on white.

## Ship

Write into the project's existing icon set and required sizes. Do not invent a second catalog. Apply a system mask only when the platform needs it and the project does not already bake one.

If asked to install or open the app, do that after the assets compile. Report destinations, skipped appearances, and any unverified store listing surface.
