---
name: ay-write
description: Research, draft, rewrite, and illustrate substantial Chinese or English articles and long-form technical content. Use when creating articles, blog posts, tutorials, long-form rewrites, or visual explainers, including 写文章, 写教程, or 改稿. Do not use for ordinary chat answers, short explanations, UI copy, narrow documentation edits, or artifact types handled by a dedicated skill.
---

# AY Write

Create writing that earns attention through insight, clarity, voice, and useful visuals.

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

## Shape the article

Infer the audience, reader prerequisites, core claim, voice baseline, factual stakes, destination, and available source material. Ask only for decisions that remain consequential.

For a new article, submit one recommended thesis, outline, and visual plan together. Explain what each visual teaches. Wait for approval unless the user explicitly asks to draft directly or skip the outline.

For an existing draft, preserve meaning and voice. A precise rewrite request is already approved; propose structural changes before silently reordering or deleting sections.

## Research and write

Prefer primary, current sources for factual claims. Never invent the author's experience, quotes, opinions, usage history, measurements, or results. When writing in the author's voice, use supplied material or published pieces as the baseline.

Ground concepts before later sections rely on them. Lead with a concrete tension, observation, or useful promise. Use examples that carry the argument. Cut repeated conclusions, generic transitions, inflated claims, filler headings, and explanations the audience already owns.

Natural prose is not decorative informality. Keep the author's stance, choose familiar words, vary rhythm only when it serves meaning, and let strong details replace promotional adjectives.

## Make visuals earn their place

Read [references/visuals.md](references/visuals.md) when the article benefits from figures or the user requests them. Choose the medium yourself from the explanatory job and available capabilities. Ask about tools only when style or editability changes the deliverable.

An approved visual plan authorizes using available drawing or image-generation capabilities. Request approval before installing a plugin or dependency, using a paid capability, or introducing a new project runtime.

## Verify and deliver

Check claims, citations, links, code, image filenames, alt text, editable sources, exports, and the rendered article when possible. Remove decorative figures that teach nothing.

Deliver the article and assets in the requested location. State factual or rendering gaps without adding an unsolicited essay about the editing process.
