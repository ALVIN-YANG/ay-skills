---
name: ay-write
description: Draft or revise concise, information-dense Chinese and English prose with clear openings and detailed anime information graphics. Use when writing articles, technical explainers, posts, stories, or speeches; 写文章、中文写作、改稿、说人话、去 AI 味 in supplied prose. Honor text-only requests. Do not use for ordinary conversational answers, shortening the assistant's last reply, UI strings, or API handoff documents.
---

# AY Write

Maximize useful information per unit of reading effort; preserve understanding and recall.

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

Identify the reading task; preserve the supplied voice. Draft directly when the outcome is clear. Respect requested structure and length; ask only consequential questions, without outline approval.

For explainers, read [clear-prose.md](references/clear-prose.md); for technical articles, also read [technical-articles.md](references/technical-articles.md).

## Lead with the whole answer

Explanatory openings summarize the whole answer and decisive conditions. An introduction's first sentence says what the thing is and what it does. Give the answer, not a promise to explain. Narrative and fiction follow the requested opening.

## Cut reading effort

Divide full articles into distinct knowledge modules with informative headings. Order them by the reader's understanding and connect their reasoning; avoid disconnected lists or a fixed outline.

Preserve necessary coverage while cutting repetition. After the opening, explain each point once, using a complete example with decisive limits. Remove familiar background, tangents, empty transitions, and routine recaps. Implementation and tutorials require an explicit request.

Keep actors, actions, consequences, and causal steps clear; explain unfamiliar terms. Preserve facts, conditions, uncertainty, and safety limits. Verify claims with primary sources; distinguish facts from inferences. Never invent experiences, quotes, measurements, or results. Label hypothetical examples; fiction may invent.

## Make it memorable

Full articles include an opening overview image and an explanatory image for each important knowledge module, unless the user requests text only. Default to Japanese cel shading and the bundled character reference; honor alternative styles. Show mechanisms, relationships, steps, and decisive limits with readable labels, arrows, and captions. Preserve useful detail, not decorative filler.

Read [visuals.md](references/visuals.md). Respect project formats. Report unavailable image production; a prompt is not an image.

Writing approval excludes publishing, paid tools, new dependencies, and unrelated edits.

## Check understanding and deliver

Read back the finished draft; revise it for density before delivery. Merge repeated explanations; preserve distinct facts and causal steps. Check opening coverage, visual coverage, and reading budgets. AI review cannot prove human comprehension.

Verify links, assets, and layout. Preserve skill-improvement feedback as regression cases; ordinary writing does not authorize skill edits.
