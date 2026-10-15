---
name: ay-write
description: Write or revise Chinese and English prose matched to its reading task. Use when authoring articles, technical explanations, interview-bank answers, FAQ entries, guides, stories, or speeches; 中文写作、面试题库答案、技术问答、改稿、去 AI 味. Exclude conversational answers, mock interviews, interview sourcing, UI copy, API handoffs, and assistant-reply shortening.
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

Identify audience, purpose, form, voice, and budget. Draft directly when clear, without outline approval; preserve narrow edit and read-only review boundaries.

Preserve facts, conditions, uncertainty, causality, and machine-readable literals. Verify factual claims with primary sources; distinguish evidence from inference. Never invent experience, quotes, measurements, or results. Label hypothetical examples; requested fiction may invent.

Keep actors, actions, and referents clear. Explain unfamiliar terms. Cut redundancy without losing necessary mechanisms or limits. Respect project conventions and requested structure.

## Match the writing task

- **Interview Q&A and FAQ:** Answer each exact question first; add necessary explanation, examples, and limits. Preserve follow-ups and version conditions. Keep entries independently readable; avoid article scaffolding and interview simulation.
- **Explanations and selection articles:** Open with the whole answer and decisive conditions; introductions define the subject immediately. Connect knowledge modules in understanding order, using a complete example and material tradeoffs.
- **Tutorials and how-to guides:** Give prerequisites, actions, observable checks, and relevant failure or stopping conditions. Writing instructions does not authorize running commands.
- **Reference:** Organize for lookup with consistent terms and stable structure.
- **Narrative and speeches:** Preserve requested viewpoint, pacing, and voice; do not force an explanatory opening or technical outline.

For factual explanations, read [clear-prose.md](references/clear-prose.md); for technical writing, also read [technical-articles.md](references/technical-articles.md).

## Visuals and delivery

Full explanatory articles have opening and important-module images unless text only is requested. Default to Japanese cel shading and the bundled character reference; honor other styles. Read [visuals.md](references/visuals.md) for illustrations. Q&A, reference entries, narrow edits, and fiction do not inherit article illustration requirements.

Revise the draft; verify coverage, density, facts, links, assets, and layout. AI review cannot prove human comprehension or recall. A prompt is not an image; report unavailable production.

Writing approval excludes publishing, paid tools, new dependencies, and unrelated edits. Ordinary writing does not authorize skill edits.
