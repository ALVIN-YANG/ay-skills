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

For a full illustrated article, inspect the overview and module images separately: use the default cinematic live-action style with natural adult Chinese faces, skin texture, physical costume detail, distinct expressive actions, and readable diagrams, unless another style was requested. Comprehensively organize mechanisms, relationships, steps, and decisive limits. Each important module needs a local image that explains it beyond the overview. For the queue case, a conveyor alone fails: cover enqueueing versus completion, buffering versus sustained overload, and the send-before-acknowledgment gap that can cause duplicate mail. Useful labels and captions are encouraged; reject tiny text, missing central details, contradictory metaphors, decorative covers, or a prompt presented as an asset. Check hierarchy at thumbnail size and detail at reading size. Compare characters against the actual selected portraits from the eight-character bundle for consistent faces, hairstyles, proportions, clothing palette, and roles; adapt poses and scenes to the article without treating the fan-character names as model performance evidence. Do not require every image to include all eight characters. A textual character description alone does not verify continuity. Place images beside the corresponding explanations and verify real files and links. Genre, narrow edits, and explicit style or text-only requests take precedence. These checks require real output; text-only execution cases do not verify image production.

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


## Writing type boundaries and interview Q&A

Freeze `write-interview-qa` and the different-topic `write-interview-holdout` before editing the skill. Compare the original AY instructions, the pinned Fenng bundle, and the revised AY instructions using identical tasks, evidence, output limits, model, and sandbox. An upstream skill's reputation is not an output-quality result.

Check the actual answers, not keyword counts: the opening answers the exact question; a short answer still explains the decisive mechanism and limits; original questions and the separate follow-up survive; each card can be read alone. Reject invented personal experience, benchmark claims, service APIs, automatic deduplication, unsupported authorization, and unconditional retry or freshness promises. The RAG answer distinguishes retrieval from supported/correct generation. Schema validation must not authorize deletion of p-8. The timeout follow-up must acknowledge the absent idempotency and query capabilities. The cache answer must retain the expiry/update distinction and concurrent-check/decrement boundary. Literal JSON values must survive; typography improvements do not authorize changing them.

Record answer length against the requested budget without presenting it as measured recall or reading time. Cards should not acquire article intros, repeated conclusions, a universal four-part template, mandatory visuals, or a mock interview. Interview-report provenance supports what was reportedly asked; official technical material supports the answer. Neither report popularity nor this synthetic fixture proves interview frequency.

`write-procedure-only` checks steps, conditions, observed outcomes, and a stopping point; it must preserve the command arguments and not execute them. `write-narrative-opening` checks that clearly authorized fiction remains fiction, starts in action, and keeps the requested viewpoint and unresolved mystery. Do not impose answer-first exposition or a technical article outline on it. Existing explanation, English, source-comparison, and read-only review cases guard the common rules.

AI inspection can identify factual or structural failures. It does not establish human comprehension, memorization, or a universally best writing skill. Record close or inconclusive comparisons as such.


## Chinese social writing and video scripts

Freeze the five `write-social-*` cases before editing the skill. Run the same WeChat, Xiaohongshu, and voiceover inputs against the original and revised bundles with the same CLI/model, limits, and sandbox. Compare actual drafts; a named platform, title, or generated file is not evidence of good platform writing.

The WeChat article needs a truthful title, an opening that earns its promise, and a connected argument with a useful reading example. The Xiaohongshu note needs distinct title and first-card copy, compact useful paragraphs, and only relevant topics. Neither may turn the fictional tool into a real recommendation, claim firsthand use, invent speed gains, generalize one import check into reliability or accuracy, or conceal missing PDF/sync/verification features when recommending suitability. Both must preserve the need to read context. Reject fear, misleading clickbait, forced personas/emojis, fabricated popularity, and unexplained technical jargon. Check requested length manually.

For voiceover, inspect what will actually be spoken: it should be natural aloud, deliver the opening promise, explain the decisive limit, and fit an explicitly estimated 60-second budget with room for pauses. Do not claim a timed recording or render was performed. The simple voiceover must not grow into a storyboard, image prompt pack, or publishing kit. In the folding holdout, spoken lines, visible actions, and subtitle emphasis should agree in order; the time budget must accommodate the actual hand movements. Do not add equipment, a finished airplane, measured success, or unusable dense subtitles. Timing is an estimate until recorded.

The title-only case remains read-only and returns one grounded title and reason, without inventing results or expanding the body. Social-media requests do not automatically inherit technical-module anime illustrations, repeated summaries, mandatory CTAs, or a fixed number of title candidates. Draft approval does not authorize opening an account dashboard, publishing, creating a video, or executing described steps. Check the actual transcript and changed paths. Existing Q&A, explanation, and narrative cases guard the common rules. AI review does not establish human comprehension, engagement, conversion, or a universally best reference.


## Integration handoffs merged into writing

Freeze the existing HTTP release case and the MQTT and no-visible-change cases before changing entrypoints. Run identical cases against the original integration skill and the merged write bundle with the same CLI/model. Preserve the consumer, release baseline, real field names and requiredness, concrete request/success examples, distinct special-error examples, and complete error summary. Inspect the actual tables and payloads; term coverage alone does not prove completeness. Do not invent contract details to fill the format.

For the MQTT case, distinguish command direction, accepted receipt, applied completion, and rejection. Keep the version capability gate and field constraints. Missing QoS, deduplication, retry intervals and timeouts must remain explicitly unresolved with the missing evidence named; no assumed exactly-once delivery or arbitrary timeout policy. Exclude other clients, unchanged topics, internal classes and broker topology. The no-visible-change case should explain why no client adjustment is needed without an empty template or file changes. Existing HTTP behavior must remain equivalent after consolidation.

Check that interface-design requests still select ay-api, implemented-contract handoffs select ay-write, and general articles, interview answers, social writing and public API-reference generation keep their boundaries. Handoffs do not inherit article scaffolding or illustrations. Inspect changed paths and transcripts to confirm documentation did not authorize contract changes, code edits or publishing.

The unchanged-contract boundary has two selection cases: a request only to audit whether anything changed belongs to ay-review; a request to write a client upgrade note belongs to ay-write even when the correct note is one sentence saying nothing changed. Preserve this distinction rather than broadening the writing trigger to all contract audits.
