# Influences and attribution

AY Skills is original work informed by the following projects. Their ideas were adapted to AY's narrower skill boundaries; their text, templates, and runtime code were not copied.

## General skill design

- [Superpowers](https://github.com/obra/superpowers)
- [Anthropic Skills](https://github.com/anthropics/skills)
- [wshobson/agents](https://github.com/wshobson/agents)
- [PM Skills](https://github.com/phuryn/pm-skills)
- [awesome-copilot](https://github.com/github/awesome-copilot)
- [claude-skills](https://github.com/alirezarezvani/claude-skills)
- [mattpocock/skills](https://github.com/mattpocock/skills)
- [Waza](https://github.com/tw93/Waza)

The relevant ideas include approval before implementation, consistent UI direction, separate architecture/API/database responsibilities, engine-specific storage design, evidence-first discovery, and narrow skill boundaries.

## Product websites

The website workflow was informed by MIT-licensed [oil-ui](https://github.com/oil-oil/oil-ui/tree/c8f76565ec30aea721b042e58d91612b9de3ee9d), reviewed on 2026-10-13. AY adapts product-grounded visual direction, meaningful composition comparisons, and inspection of actual desktop and mobile renders.

The instructions and synthetic evaluation cases are original. No upstream text, templates, scripts, or assets were copied. AY keeps its approval contract, optional comparisons and handoffs, and existing tool choices; it adds no updater, promotion, or mandatory multi-direction process.

## Design handoffs

The handoff checks were informed by the University of Michigan's [Elephant-Goldfish skills](https://github.com/eecs498-aase/materials/tree/795b99ce2e5b39eacfda488e6db0b9b812143252/egm/skills). AY adapts three ideas: a document must carry the design without its author's conversation, reviewers must distinguish missing decisions from disagreements, and implementation must expose material conflicts with the approved design.

The reviewed repository metadata reported no license, and its tree contained no identifiable license file on 2026-10-12. Only the ideas informed this work; no upstream instructions, templates, scripts, or test data were copied. AY keeps its independent skills, existing approval contract, and optional handoff artifacts.

## App Store screenshots

The screenshot workflow was informed by MIT-licensed [app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots), [Shotsmith](https://github.com/gyugyu86/app-store-screenshot-studio), [ai-appshots](https://github.com/thiagoperes/ai-appshots), and [fastlane](https://github.com/fastlane/fastlane).

AY keeps one reproducible deck state, organizes exports by locale and device, preserves the shipped UI, and rejects invalid files before upload. The instructions and validator code are original.

## Expert selection

The question-relative expert selection in `ay-expert-lens` was prompted by MIT-licensed [Best Minds](https://github.com/Agentchengfeng/best-minds).

AY applies verifiable published frameworks, separates sources from inference, and does not impersonate the person or invent what they would say.

## Client integration documentation

The client-impact boundary in `ay-write` integration handoffs (formerly `ay-integration-docs`) was informed by Apache-2.0 [oasdiff](https://github.com/oasdiff/oasdiff), plus the API documentation work in MIT-licensed [wshobson/agents](https://github.com/wshobson/agents) and [awesome-copilot](https://github.com/github/awesome-copilot).

AY adds a consumer-and-release filter, observable business semantics, required examples and field tables, and explicit exclusion of internal or unchanged behavior.

## Clear writing

The writing revisions draw on [Google Technical Writing](https://developers.google.com/tech-writing/one/short-sentences), [NN/G content comprehension testing](https://www.nngroup.com/articles/testing-content-websites/), and [Anthropic's guidance on concise instructions and representative examples](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

AY's prose instructions and before/after examples are original. They separate preserving facts, making an explanation understandable, and evaluating it with real readers. No upstream prose, test data, or validator was copied; AI review is not presented as proof of human comprehension.

The writing-type distinctions also draw on Daniele Procida's [Diátaxis](https://diataxis.fr/start-here/): learning, doing, lookup, and understanding call for different documentation forms. AY applies that distinction to technical writing and interview study entries; narrative is outside this framework's technical-documentation scope. The branches and acceptance checks are original adaptations, not a copied template or a requirement to split every topic into four documents.

The common rules were also compared with Fenng's MIT-licensed [Tech-Doc-Style-Chinese](https://github.com/Fenng/Tech-Doc-Style-Chinese/tree/b119d01c9bb7cd132b3c62fafdff34227c4410d1), reviewed on 2026-10-15. The useful overlap is protecting facts, conditions, and machine-readable literals before optimizing style. AY's instructions and synthetic question sets are original; upstream text, templates, checkers, and task stages were not copied. Paired trials compare actual output without claiming a universally best skill or measured human recall.

## Chinese social writing

The social-writing additions were informed by three task-specific candidates, reviewed on 2026-10-15:

| Reference | Useful idea | License review at the pinned revision |
|---|---|---|
| [classfang/weixin-mp-skills: wechat-article-write](https://github.com/classfang/weixin-mp-skills/tree/6f71866de118ab06a5640364fe037cd434eec20c/wechat-article-write) | Reader purpose, useful original substance, connected arguments, and mobile reading; writing is distinct from optional HTML formatting | Repository metadata reported no license; the recursive tree contained no identifiable license file |
| [Vink567/xiaohongshu-writer](https://github.com/Vink567/xiaohongshu-writer/tree/b04cf573216e471aa992cee6e3cd136608ccda25) | Coordinate title, first-card copy, and body; change the presentation for reviews, tutorials, and stories | MIT license file inspected |
| [ShortVideo-AI/short-video-script-skill](https://github.com/ShortVideo-AI/short-video-script-skill/tree/5b42b3bfb5199483a90614070b374c23758e7807) | Write for speech, check duration, and distinguish spoken copy from shots and release packaging | Frontmatter declares MIT, but repository metadata and the recursive tree provided no independent license file |

These are references for fit, not proven quality winners. AY's wording and synthetic cases are original; no upstream instructions, templates, scripts, assets, or test data were copied. AY does not adopt mandatory title counts, staged confirmations, fixed personas, emoji quotas, algorithm promises, engagement bait, or automatic publishing. Estimated script duration remains distinct from a timed recording or a rendered video.

Also inspected: MIT-licensed [zdyya/writer-skill](https://github.com/zdyya/writer-skill/tree/dd100aaf4bb4c028bbda6b11184d232c4c0a0737) and [sangjiexun/koubo-script-skill](https://github.com/sangjiexun/koubo-script-skill/tree/68f48daa19caa4d3b8df41caeccd58eefa4aa533), whose full production workflows exceed this writing-only scope. MIT-licensed [v0id-byte/xiaohongshu-writer](https://github.com/v0id-byte/xiaohongshu-writer/tree/57e93b7579e7256c24626d39df6901b3654ce9c7) attributes rules to an official enterprise guide without a traceable source in the inspected skill; AY does not treat its fixed metrics or recommendation claims as platform facts.


## Agent evaluation

`ay-agent-eval` adapts the user's existing local skill and protocol, reviewed on 2026-10-28. It remains independently installable and requires no evaluation framework, paid service, multi-agent setup, or background controller. Its detailed source notes remain in the protocol. No upstream code, templates, or passages were imported.

The admission decision applies Percy Liang and collaborators' [HELM framework](https://arxiv.org/abs/2211.09110): explicit scenario coverage, multiple relevant metrics, standardized comparison and inspectable evidence. HELM evaluates language models; applying those principles to tool state, authorization and bounded repair is AY's adaptation. [Anthropic's agent-evaluation guidance](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) supports outcome checks, calibrated graders and trial accounting. Framework reputation is not evidence that this skill improves a given agent.
