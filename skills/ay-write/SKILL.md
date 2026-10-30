---
name: ay-write
description: Write or revise Chinese and English prose. Use when authoring articles, Q&A, guides, stories, speeches, social content, or consumer handoffs for approved/implemented APIs and messages; 中文写作、面试题库、公众号、小红书、视频文案、口播、改稿、去 AI 味、联调文档、客户端升级说明. Exclude contract design, conversations, mock interviews, interview sourcing, UI copy, layout-only work, and assistant-reply shortening.
---

# AY Write

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

## Common rules

Identify audience, purpose, form, voice, and budget. Draft directly when clear; preserve narrow edit and read-only review boundaries.

Preserve facts, conditions, uncertainty, causality, and machine-readable literals. Verify factual claims with primary sources; distinguish evidence from inference. Never invent experience, quotes, measurements, or results. Label hypothetical examples; requested fiction may invent.

Keep actors, actions, and referents clear. Explain unfamiliar terms. Cut redundancy without losing mechanisms or limits. Respect requested conventions and structure.

## Match the writing task

- **Interview Q&A and FAQ:** Answer each exact question first; add necessary explanation, examples, and limits. Preserve follow-ups and version conditions. Keep entries independently readable; avoid article scaffolding and interview simulation.
- **Explanations and selection articles:** Open with the answer and decisive conditions; define the subject immediately. Connect modules in understanding order, using a complete example and material tradeoffs.
- **Tutorials and how-to guides:** Give prerequisites, actions, observable checks, and relevant failure or stopping conditions. Writing instructions does not authorize running commands.
- **Reference:** Organize for lookup with consistent terms and stable structure.
- **Integration handoffs:** Read [integration-docs.md](references/integration-docs.md) for consumer and release scope, contract evidence, field tables, examples, and error handling. Document existing decisions; do not invent contracts.
- **Narrative and speeches:** Preserve requested viewpoint, pacing, and voice; do not force an explanatory opening or technical outline.
- **WeChat, Xiaohongshu, and video:** Read [social-writing.md](references/social-writing.md) for platform packaging, speech, and timing. Deliver requested parts only.

For factual explanations, read [clear-prose.md](references/clear-prose.md); for other technical writing, read [technical-articles.md](references/technical-articles.md).

## Visuals and delivery

Full explanatory articles include opening and module images, defaulting to cinematic photorealism and the bundled cast; honor requested styles and text-only scope. Read [visuals.md](references/visuals.md) for illustrations. Q&A, reference entries, integration handoffs, narrow edits, fiction, and social content do not inherit this requirement.

Revise; verify coverage, facts, links, assets, and layout. AI review cannot prove human comprehension or recall. A prompt is not an image; report unavailable production.

Writing approval excludes publishing, paid tools, new dependencies, and unrelated edits. Ordinary writing does not authorize skill edits.
