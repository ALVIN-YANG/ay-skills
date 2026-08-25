---
name: ay-expert-lens
description: Select and apply publicly documented thinking frameworks from real experts to open-ended decisions, ideation, critique, or explanation. Use when the user asks who understands a problem best, requests a named expert's perspective, invokes best minds, 顶级专家, or 谁最懂这个, or wants competing expert lenses. Do not use for ordinary facts, implementation, diagnosis, individualized medical, legal, or financial advice, style imitation, or unsupported claims about what a person would say.
---

# AY Expert Lens

Apply a real expert's documented method to the problem without turning reputation into evidence.

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

## Use a lens only when it changes the reasoning

Use this skill when selecting or applying an expert framework is the primary request and the question allows more than one defensible approach. A general brainstorm, style imitation, fact lookup, implementation, diagnosis, or task with objective proof does not need an expert lens. When another workflow owns the concrete deliverable, let it lead and use this lens only when the user explicitly asks for it.

Choose one primary expert by default. Add another only when documented disagreement exposes a material tradeoff. Do not optimize for fame. Prefer the person whose published work best matches the precise problem, context, and decision.

## Ground the lens

Inspect the user's evidence and constraints. Verify public sources before attributing a framework when the material is not supplied. Prefer original books, papers, talks, interviews, and official records. Refresh current or high-stakes facts from authoritative sources.

Extract the framework's problem, decision rules, assumptions, and limits. Keep three layers distinct: the expert's documented position, a reasoned inference from it, and the recommendation for the user's situation.

Never invent a quotation. Quote only text that was verified and cite its direct source. Do not claim to be the person, imitate their voice, or state what they would believe today. Attribute the method plainly, such as "Applying X's documented framework." If the public basis is weak or the lens adds no useful distinction, say so and answer without a persona.

## Apply it to the decision

Name the selected lens and why it fits. Translate it into concrete questions or decision rules, apply those to the user's constraints, and explain what the lens changes. For multiple experts, show the actual disagreement before synthesizing a recommendation.

Preserve the user's goal and approved scope. An expert lens cannot replace current facts, executed evidence, qualified medical, legal, or financial advice, or the accountable human decision-maker.
