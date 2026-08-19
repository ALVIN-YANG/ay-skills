---
name: ay-ui
description: Design and approve product interfaces before frontend implementation. Use when the primary deliverable is visual direction, application screens, screen-by-screen mockups, interaction states, a design system, or a design.md handoff, including 定设计风格, 生成设计图, UI方案, or 一张张确认页面. Do not use for product strategy, store icons, a single decorative image, UI compliance review, or requests primarily asking to write frontend code.
---

# AY UI

Turn approved product behavior into a coherent interface, then preserve the approved decisions for implementation.

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

## Establish the visual contract

Inspect the approved requirements, product or repository, existing brand and design system, target platform, real content, and supplied references. Extract the primary journey, screen inventory, reusable states, and platform constraints. Do not silently change approved product behavior.

If the visual direction is open, recommend one distinctive direction with its rationale, typography, color, spacing, surface treatment, and one signature idea. Show only alternatives that expose a material tradeoff, then wait. Use already available design or image capabilities; adding a paid tool or dependency needs approval.

## Design through visible checkpoints

Start with the screen that best tests hierarchy, content density, navigation, and the chosen visual idea. Inspect the rendered result before presenting it. Collect feedback that changes a decision, update the visual contract, then continue screen by screen unless the user explicitly asks for a batch.

Keep tokens, components, icon language, content model, device frame, and approved assets consistent. Treat feedback as local unless it changes the shared contract. Cover loading, empty, error, permission, cancellation, recovery, disabled, and accessibility states when relevant. Account for responsive or platform-specific behavior instead of stretching one screenshot everywhere.

## Hand off the approved design

When the user has approved the design set and requested a durable handoff, create `design.md` or the repository's established equivalent. Record only approved decisions: visual thesis, tokens, components, screens, flows, states, responsive rules, accessibility, asset paths, non-goals, and unresolved implementation constraints. Reference final assets rather than rejected drafts.

Verify that the document and image set describe the same product. Stop before frontend code unless implementation is separately authorized.
