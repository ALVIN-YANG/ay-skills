---
name: ay-write
description: Draft, research, or revise authored Chinese and English prose with clear meaning and a natural voice. Use when writing articles, technical explainers, posts, stories, or speeches; 写文章、中文写作、改稿、说人话、去 AI 味 in supplied prose. Own prose-only Chinese writing as well as illustrated work. Do not use for ordinary conversational answers, shortening the assistant's last reply, UI strings, or API handoff documents.
---

# AY Write

Write so the intended reader understands without supplying missing explanations.

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

## Establish the reading task

Infer the reader's existing knowledge, the question or experience the piece should deliver, genre, language, and destination. Use supplied writing as the voice baseline. Ask only about consequential gaps.

Draft or revise directly when the request and material establish the outcome. Do not require outline approval by default. Preserve requested structure; propose changes only when they alter intent or an approval boundary.

For explainers or unclear prose, read [references/clear-prose.md](references/clear-prose.md). Use relevant examples as comparisons, not a mandatory template.

## Preserve meaning while writing plainly

Verify factual claims with suitable primary sources. Do not invent the author's experiences, attributed beliefs, quotes, measurements, or results. Label hypothetical examples. Fiction may invent within the requested premise.

In explanatory writing, answer the reader's question early, then explain through a concrete example. Put implementation details and secondary exceptions after the main explanation. Preserve conditions, uncertainty, and safety limits; simplification must not strengthen a claim.

Name the actor, action, and consequence. Keep useful technical terms and explain unfamiliar ones when needed. Remove repetitive conclusions, empty abstractions, and transitions that add nothing. Naturalness does not require slang, simulated mistakes, banned punctuation, or sentence-length quotas. Narrative and fiction need not begin with a conclusion.

## Use visuals selectively

Read [references/visuals.md](references/visuals.md) when a visual explains something better than prose or is requested. Respect the project's formats and existing capabilities.

Approval for writing does not authorize publishing, paid tools, new dependencies, or unrelated edits.

## Check understanding and deliver

Check whether the reader can recover the intended answer and next action from the text alone. Identify unsupported jumps, unclear referents, and unexplained terms; fix the passages, not just the score. Automated prose checks and AI review are aids, not proof of human comprehension.

Verify claims, links, examples, assets, and rendered layout in proportion to the task. Deliver only the requested work and material limitations. When asked to improve this skill, turn concrete feedback into a regression case; do not silently rewrite skill or user settings during ordinary writing.
