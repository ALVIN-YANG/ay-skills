---
name: ay-app-store
description: Audit, prepare, submit, monitor, and recover Apple App Store releases from verified project and live App Store Connect state. Use when the user asks to 上架, 发布, 提交审核, 重新提交, 检查审核状态, 处理 App Review 拒绝, prepare TestFlight or App Store builds, reconcile StoreKit subscriptions, privacy, EULA, screenshots, metadata, or review information for an Apple-platform app. Do not use for Google Play-only publishing, store-icon creation, ASO-only research, or ordinary feature implementation.
---

# AY App Store

Move an Apple release through verified states. Never equate a green local build with a processed build, a submitted version, an approved version, or a downloadable storefront listing.

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

Inspect the repository, git state, build settings, entitlements, packaged purpose strings, privacy manifests, StoreKit, legal links, screenshots, and release automation. `python3 scripts/scan_apple_release.py <repo>` produces a read-only inventory, never a compliance verdict.

Refresh Apple documentation before policy conclusions. Use [Apple workflow](references/apple-workflow.md) for official checks and [tooling](references/tooling.md) for credential boundaries.

Reconcile:

- Identity: app record, Bundle ID, platform, version, build, team, SKU.
- Privacy: data flow, SDKs, labels, policy, in-app entry, permissions.
- Commerce: product IDs, types, periods, prices, entitlements, restore, review items.
- Review: localizations, screenshots, URLs, rating, contact, notes, attachments.
- Account: agreements, tax, banking, trader status, roles.

Prefer live App Store Connect state over code or email inference. “Changes needed” is only a pointer; inspect every rejected item and Resolution Center message.

## Resolve and prove

Classify gaps as code/build, metadata, commerce, explanation, or account work. Use [rejection playbook](references/rejection-playbook.md) for privacy, subscription/EULA, missing-item, and summary-email cases.

Prove states independently:

1. Source or metadata changed.
2. Tests and archive passed.
3. Upload finished Apple processing.
4. Build and IAP items joined the intended submission.
5. Submission ID and review state are confirmed.
6. Review passed.
7. Version is Ready for Distribution.
8. Storefront download works.

Report the highest proven layer and all unverified layers.

## Operate live surfaces

Prefer supported APIs or existing automation; use signed-in web UI for review messages and account fields. Installing tools, reusing cookies, or calling private APIs needs approval.

A precise request to submit or resubmit the named app/version is approval; do not ask twice. Unrequested cancellation, deletion, pricing, territories, agreements, banking/tax, credentials, members, or reviewer replies need their own boundary.

Before mutation, recheck app, platform, version, build, products, and submission. Afterwards, reread state and capture stable IDs. Never store secrets or full banking/identity data in files, chat, or Git.

`assets/release-dossier-template.md` is optional.
