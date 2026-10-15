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

The client-impact boundary in `ay-integration-docs` was informed by Apache-2.0 [oasdiff](https://github.com/oasdiff/oasdiff), plus the API documentation work in MIT-licensed [wshobson/agents](https://github.com/wshobson/agents) and [awesome-copilot](https://github.com/github/awesome-copilot).

AY adds a consumer-and-release filter, observable business semantics, required examples and field tables, and explicit exclusion of internal or unchanged behavior.

## Clear writing

The writing revisions draw on [Google Technical Writing](https://developers.google.com/tech-writing/one/short-sentences), [NN/G content comprehension testing](https://www.nngroup.com/articles/testing-content-websites/), and [Anthropic's guidance on concise instructions and representative examples](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents).

AY's prose instructions and before/after examples are original. They separate preserving facts, making an explanation understandable, and evaluating it with real readers. No upstream prose, test data, or validator was copied; AI review is not presented as proof of human comprehension.

The writing-type distinctions also draw on Daniele Procida's [Diátaxis](https://diataxis.fr/start-here/): learning, doing, lookup, and understanding call for different documentation forms. AY applies that distinction to technical writing and interview study entries; narrative is outside this framework's technical-documentation scope. The branches and acceptance checks are original adaptations, not a copied template or a requirement to split every topic into four documents.

The common rules were also compared with Fenng's MIT-licensed [Tech-Doc-Style-Chinese](https://github.com/Fenng/Tech-Doc-Style-Chinese/tree/b119d01c9bb7cd132b3c62fafdff34227c4410d1), reviewed on 2026-10-15. The useful overlap is protecting facts, conditions, and machine-readable literals before optimizing style. AY's instructions and synthetic question sets are original; upstream text, templates, checkers, and task stages were not copied. Paired trials compare actual output without claiming a universally best skill or measured human recall.
