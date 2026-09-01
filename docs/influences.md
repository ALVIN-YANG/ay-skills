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

## App Store screenshots

The screenshot workflow was informed by MIT-licensed [app-store-screenshots](https://github.com/ParthJadhav/app-store-screenshots), [Shotsmith](https://github.com/gyugyu86/app-store-screenshot-studio), [ai-appshots](https://github.com/thiagoperes/ai-appshots), and [fastlane](https://github.com/fastlane/fastlane).

AY keeps one reproducible deck state, organizes exports by locale and device, preserves the shipped UI, and rejects invalid files before upload. The instructions and validator code are original.

## Expert selection

The question-relative expert selection in `ay-expert-lens` was prompted by MIT-licensed [Best Minds](https://github.com/Agentchengfeng/best-minds).

AY applies verifiable published frameworks, separates sources from inference, and does not impersonate the person or invent what they would say.

## Client integration documentation

The client-impact boundary in `ay-integration-docs` was informed by Apache-2.0 [oasdiff](https://github.com/oasdiff/oasdiff), plus the API documentation work in MIT-licensed [wshobson/agents](https://github.com/wshobson/agents) and [awesome-copilot](https://github.com/github/awesome-copilot).

AY adds a consumer-and-release filter, observable business semantics, required examples and field tables, and explicit exclusion of internal or unchanged behavior.
