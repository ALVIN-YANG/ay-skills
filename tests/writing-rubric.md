# Writing checks beyond file creation

The execution cases check whether the requested file was produced and protected inputs stayed unchanged. They do not score readability. Use the raw notes and intended reader below for a separate review of the actual output; do not show this rubric to the drafting agent as its user brief.

## Chinese explanation

Case `write-chinese-clarity` uses `fixtures/writing-clarity/notes.md`.

A reader should be able to explain, from the article alone:

- What must survive a process exit, and what step follows the uploaded CSV?
- Why does a timed-out email request leave an unknown result?
- Given this mail service's actual limitations, why is automatic retry unsafe?

Reject invented result-query APIs, invented idempotency support, claims of database-failover validation, author experience, or measured improvements absent from the notes. Check that unfamiliar names follow or accompany an explanation, and that the opening answers the recovery question before cataloguing frameworks.

## Reading effort and information density

Case `write-reading-density` uses `fixtures/writing-density/`. The verbose draft is a synthetic candidate, not a user-approved example. Compare the actual before/after skill outputs on the same request; record article length without treating it as measured human reading time.

The first sentence should identify what a message queue is and what it does. The opening should recover the article's core answer and decisive limits. The article must be substantially shorter than the supplied draft without losing the order-email example, the distinction between enqueueing and completion, temporary buffering versus sustained backlog, or the duplicate-mail risk between sending and acknowledgment.

Reject background padding, repeated summaries, unrelated taxonomy or deployment advice, jargon piles, omitted causal steps, invented transaction guarantees, automatic deduplication, and author experience. Every paragraph should supply necessary new information. A one-sentence abstract that loses the mechanism also fails. The explicit text-only request must prevent image generation or an unsolicited visual plan.

Full articles should have distinct knowledge modules with meaningful headings and a coherent progression. Each module answers a main question and builds on prior explanations; reject isolated fact cards, unexplained jumps, or mechanical transitions that add no reasoning. Module count follows the reading task, and narrow paragraph or fiction requests keep their scope.

For a full illustrated article, inspect the overview and module images separately: use the chosen Japanese cel-shaded anime style and comprehensively organize mechanisms, relationships, steps, and decisive limits. Each important module needs a local image that explains it beyond the overview. For the queue case, a conveyor alone fails: cover enqueueing versus completion, buffering versus sustained overload, and the send-before-acknowledgment gap that can cause duplicate mail. Useful labels and captions are encouraged; reject tiny text, missing central details, contradictory metaphors, decorative covers, or a prompt presented as an asset. Check hierarchy at thumbnail size and detail at reading size. Compare every image against the bundled user-selected reference for consistent faces, hairstyles, proportions, clothing palette, and roles; adapt poses and scenes without copying its Langfuse topic or claims. A textual character description alone does not verify continuity. Place images beside the corresponding explanations and verify real files and links. Genre, narrow edits, and explicit style or text-only requests take precedence. These checks require real output; text-only execution cases do not verify image production.

## English transfer case

Case `write-english-holdout` uses a different subject and language, outside the skill's Chinese rewrite examples.

The output must preserve 200 attempts and twelve initial timeouts, distinguish timeout from confirmed failure, explain reusing the operation ID, and restrict the tested guarantee to the stated server. Check whether a non-specialist could understand the duplicate-upload risk without already knowing idempotency.

## Technical selection

Case `write-technical-selection` uses `fixtures/writing-selection/notes.md`.

A reader should be able to identify the recommended deployment and explain why the public cloud SaaS and per-user desktop app are rejected or deprioritized. The article should define the sandbox or restricted-container idea before relying on it, separate deployment location from isolation, and reach the recommendation through the stated privacy, multi-user, hostile-file, and recovery constraints.

Reject invented benchmarks, costs, production results, vendor features, or a flat catalog that never chooses. Also reject an opening recommendation repeated under comparison, minimum-boundary, and final-recommendation headings without new reasoning. Reject unexplained abstractions such as calling the Web service a "control plane" when its actual actions can be stated directly. Do not expand this selection request into database fields, permission configuration, a deployment guide, or an implementation handoff. The recommendation should keep files inside the company network, isolate LibreOffice from the business server, and persist task progress and results outside the conversion process.

## Source-grounded technical comparison

Case `write-source-comparison` uses `fixtures/writing-source/` and synthetic source excerpts.

The reader should be able to identify who exchanges messages and who decides what happens next in all five configurations. Check whether the opening answers the selection question without treating Hybrid's 42% as better than the SAS baseline of 60%. The article must distinguish 18 percentage points from a 30% relative decline if it calculates the difference, preserve that Independent lacks cross-validation in this configuration, and not turn three workers into a universal definition.

Reject generic framework shopping that replaces the requested source comparison, claims of having read a complete paper, invented production results or caching/cost findings, and code or deployment instructions that displace the explanation. The five-name assertion only checks coverage; inspect the actual prose to assess understanding and source fidelity.

## Genre and scope checks

Use a short fiction request to confirm that invented events are allowed and an explanatory conclusion is not imposed. Use `write-review-only` to confirm that a critique does not mutate the draft. A precise paragraph rewrite should retain requested structure and must not grow into an article, visual plan, or publishing task.

## Record and iterate

For each run record the CLI/model when known, skill revision, raw input, actual output, and specific passages that helped or blocked understanding. Report factual preservation, task scope, and explanation quality separately. AI review is a preliminary judgment, not representative human testing.

When a reader objects, preserve the original passage and the proposed correction as a candidate case. Only mark wording as user-approved after actual confirmation. Recheck another subject before turning feedback into a general instruction; do not reward uniform punctuation, arbitrary sentence lengths, or the presence of a preferred heading.
