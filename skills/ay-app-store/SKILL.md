---
name: ay-app-store
description: Create reproducible real-UI store screenshots, or act as the chosen workflow for auditing, submitting, monitoring, and recovering Apple App Store releases. Use when the request is 生成 App Store 宣传图, 上架, 提交审核, App Review 拒绝, StoreKit, privacy, metadata, or live review state. When another dedicated App Store release skill is installed, let it lead generic release work and use ay-app-store for screenshot generation. Do not use for store icons, UI mockups, or ordinary implementation.
---

# AY App Store

Move an Apple release through verified states. Never equate a local build, processed upload, submission, approval, and downloadable storefront listing.

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

## Establish facts

Inspect source, build/signing, entitlements, packaged purpose strings, privacy, StoreKit, legal links, screenshots, and automation. `python3 scripts/scan_apple_release.py <repo>` is an inventory, not a verdict.

Refresh Apple documentation before policy conclusions. Use [Apple workflow](references/apple-workflow.md) for official checks and [tooling](references/tooling.md) for credential boundaries.

For general release work, reconcile identity, privacy, commerce, metadata, and account readiness against live App Store Connect. Prefer live state. Let another dedicated release workflow lead unless the user chose this one.

## Prepare store screenshots

For screenshot creation or refresh, read [store screenshot workflow](references/store-screenshots.md). Start from the current release build, keep the captured app layer exact, and use generated art only around it.

A precise generation request authorizes artifacts, not upload. If direction is open, propose one direction and representative slide. The deliverable is incomplete until final images exist and are inspected; Markdown alone is not a deck. Report sources, targets, locales, exports, checks, and unverified state.

## Resolve and prove

Classify gaps as code/build, metadata, commerce, explanation, or account work. Use [rejection playbook](references/rejection-playbook.md) for recovery and the [Apple workflow evidence ladder](references/apple-workflow.md#证据阶梯) to separate change, archive, processing, submission, review, distribution, and storefront proof. Report the highest proven layer and every unverified layer.

## Operate live surfaces

Prefer supported APIs or existing automation. Installing tools, reusing cookies, or calling private APIs needs approval.

A precise request to submit or resubmit the named app/version is approval. Unrequested cancellation, deletion, pricing, territories, agreements, banking/tax, credentials, members, or reviewer replies need separate approval.

Before mutation recheck app, platform, version, build, products, and submission; afterwards reread state and stable IDs. Never store secrets or full identity data. Use `assets/release-dossier-template.md` only for a requested durable handoff.
