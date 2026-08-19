<div align="center">
  <h1>AY Skills</h1>
  <p><strong>让 AI 先弄清楚再动手，少打断，也别自作主张。</strong></p>
  <p>
    <a href="https://github.com/ALVIN-YANG/ay-skills/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/ALVIN-YANG/ay-skills/test.yml?branch=main&style=flat-square&label=tests" alt="测试"></a>
    <a href="https://github.com/ALVIN-YANG/ay-skills/releases"><img src="https://img.shields.io/github/v/release/ALVIN-YANG/ay-skills?style=flat-square" alt="版本"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="MIT 许可证"></a>
  </p>
  <p><a href="README.md">English</a></p>
</div>

AY Skills 来自我每天和 AI 一起做事时反复遇到的烦心事：产品点子还没查用户和市场就写成了需求，多轮页面设计越画越不像一套，后端还没定边界和契约就开始写代码，Bug 靠猜，流式语音有杂音却不分层排查，重构没有基线，评审时顺手改代码，发布时又把本地、提交和线上状态混为一谈。

所以我把它们做成了可以单独安装的 Skill。任务说清楚了就直接做；还有产品或技术上的关键选择，就先调查、问一次，然后在你确认的范围内完成。

<p align="center">
  <img src="assets/ay-skills-map.zh-CN.svg" alt="十三个 AY Skill 覆盖产品、UI、架构、API、数据库、实现、排错、音频、优化、写作、评审、图标和 App Store 发布。" width="100%">
</p>

## Skill

| Skill | 什么时候用 | 它会做什么 |
|---|---|---|
| [`ay-product`](skills/ay-product/SKILL.md) | 把一个简单设想变成产品方向、MVP、需求或 PRD | 调查用户问题和市场，给出聚焦的产品建议，并把假设变成可验证的问题 |
| [`ay-ui`](skills/ay-ui/SKILL.md) | 确定视觉方向、逐页设计产品界面或整理 UI 交接 | 锁定一套视觉契约，用可见页面迭代，只记录确认过的设计 |
| [`ay-architecture`](skills/ay-architecture/SKILL.md) | 写代码前设计新系统或子系统 | 定义最简单可行的边界、数据归属、部署、故障隔离和演进方式 |
| [`ay-api`](skills/ay-api/SKILL.md) | 设计 REST、GraphQL、gRPC、服务、事件或 Webhook 契约 | 从调用方任务推导稳定接口，不把数据库表直接翻译成 CRUD |
| [`ay-database`](skills/ay-database/SKILL.md) | 选择数据库，或设计表、索引、事务和迁移 | 从业务约束与访问路径出发，再应用具体数据库引擎的规则 |
| [`ay-implement`](skills/ay-implement/SKILL.md) | 落地已经确认的功能、设计或普通代码变更 | 保留已确认决策，完成最小闭环，并验证真实结果 |
| [`ay-fix`](skills/ay-fix/SKILL.md) | 排查 Bug、回归、崩溃、偶发失败或异常变慢 | 先确认根因，再做最小有效修复 |
| [`ay-audio`](skills/ay-audio/SKILL.md) | 实现或排查 Apple 平台的流式 TTS 与语音播放 | 从服务端字节一路定位到混音和设备，并以真实听感验收 |
| [`ay-improve`](skills/ay-improve/SKILL.md) | 重构，或者优化性能和可维护性 | 先建立基线，修改后再比较结果 |
| [`ay-write`](skills/ay-write/SKILL.md) | 写文章、教程、长篇改稿或图文解释 | 写出自然、清楚、没有废话的长内容 |
| [`ay-review`](skills/ay-review/SKILL.md) | 评审代码、分支、方案或发布准备度 | 默认只读，只报告重要且有证据的问题 |
| [`ay-icon`](skills/ay-icon/SKILL.md) | 设计或替换 App Store、Play 商店或启动器图标 | 先锁定隐喻和风格，再生成、检查并装进资源 |
| [`ay-app-store`](skills/ay-app-store/SKILL.md) | 准备、提交、跟踪或修复 Apple App Store 发布 | 对齐代码、元数据、付费项目、账号和实时审核状态后再操作 |

可以只装一个，也可以全部安装。它们彼此不依赖，不需要路由器，也不会把一个小改动变成一场规划会议。

完整产品通常按 `ay-product → ay-ui → ay-architecture → ay-api → ay-database → ay-implement` 交接，需要时用 `ay-review` 检查文档一致性或实现结果。这只是建议顺序，不是强制流水线。技术可行性会阻塞 UI 时，架构可以提前；每个 Skill 也都能从已有输入单独工作。

0.6.0 把 `ay-work` 改名为 `ay-implement`，让名字和“负责落地”的职责一致。

## 安装

同时安装到 Codex 和 Claude Code：

```bash
npx skills@latest add ALVIN-YANG/ay-skills -a codex claude-code -g -y
```

想挑选单个 Skill，或者安装到当前项目：

```bash
npx skills@latest add ALVIN-YANG/ay-skills
```

Claude Code 也可以用原生插件：

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

平时直接说要做什么，对应 Skill 会自己跟上。不必写 `$ay-implement`；只有想强制指定时才点名。

```text
给应用增加导出流程。
调查这个设想，并定义一个聚焦、可验证的 MVP。
把确认过的产品逐页做成设计图，再整理 design.md。
写代码前先完成系统架构、接口和数据库设计。
诊断并修复这个偶发测试。
排查这个 macOS 流式 TTS 为什么噼啪响，并修复已确认的音频边界。
从真实基线出发简化这个模块。
把这些笔记写成清楚好读的图文文章。
评审这个分支，不要修改文件。
重做这个应用的上架图标并装进资源。
检查这个 iOS App 的审核准备情况，并提交确认无误的版本。
```

## 一个实际例子

```text
你：增加离线模式。

AY：当前应用默认一直联网。我建议首版只支持离线查看缓存数据，明确显示
“数据可能过期”；离线写入和自动排队不在本次范围。验收覆盖冷启动、断网查看、
恢复联网三条路径。按这个边界做吗？

你：可以。

AY：已按确认范围完成并通过相关测试。离线写入仍未实现；真机恢复联网是目前
唯一没有验证的环节。
```

## 和其他 Skill 一起使用

AY Skills 可以和前端设计、PDF、表格、无障碍检查等专用 Skill 共存。任务命中专用 Skill 时，由专用 Skill 主导；需要时再沿用 AY 的批准和证据边界。

不要同时全局安装两套职责相同的通用工作流，再指望每次都能自动选对。例如排错和代码评审各选一套主工作流，其他方案放到具体项目，或者在提示中明确指定。

## 什么时候会停下来问你

任务足够明确，指令本身就是批准：调查、修改、验证，直接做完。

只有需要替你决定产品行为、架构、数据契约、依赖、范围、风险、费用、回滚方式或外部操作时，才会停下来问。方向确认后，只要边界没变，就继续做到验证完成。

`ay-product` 会自己调查能查到的产品和市场事实，只询问会实质改变方向的选择，并在 UI、架构和实现开始前停下。几个设计 Skill 也遵守同一条边界，只产出确认过的契约，代码由 `ay-implement` 负责。

评审是个例外：除非你明确要求修复，`ay-review` 始终只读。

## 写文章时怎么配图

`ay-write` 会先想清楚文章要讲什么、怎么组织、每张图解决什么问题，再选工具。小而精确的图解用 SVG，需要编辑的架构图用 draw.io 或 Excalidraw，数据结论用来源可追溯的图表，封面和场景才考虑生图。

只有风格或可编辑性会改变结果，或者需要安装新工具、依赖、付费服务和项目运行环境时，它才会问你。

## 保持小而清楚

十三个 Skill。没有路由器、模式标签、hooks、遥测、状态栏、自动提交或强制规划文件。每个 Skill 各做一件事，也能单独安装。

AY Skills 遵循 [Agent Skills 规范](https://agentskills.io/specification)。便携安装、Codex 与 Claude 的实时路由、Claude Code 原生插件、CI、发布包和远程安装是彼此独立的验证层；每次发布只声明实际检查过的层级。Codex 插件清单面向本地市场测试和以后提交公共目录，目前不声称已公开上架。

<details>
<summary>开发与验证</summary>

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/run_routing_evals.py --host codex
python3 scripts/run_routing_evals.py --host claude
python3 scripts/run_behavior_evals.py
python3 scripts/run_product_evals.py
python3 scripts/run_product_evals.py --research-mode live
```

CI 运行结构和单元测试。路由测试覆盖全部 AY Skill、不该触发 AY 的请求，以及专用 Skill 共存场景。Codex 黑盒测试会真的执行隔离任务，检查可观察结果和批准边界。产品评测用固定案例和同一套评分标准，对比 `ay-product` 与未安装 Skill 的基线；实时市场调研单独运行。实时测试需要本机 CLI 和可用账号；黑盒执行目前只覆盖 Codex。

</details>

## 灵感来源

AY Skills 是原创项目，参考了 [Superpowers](https://github.com/obra/superpowers)、[Anthropic Skills](https://github.com/anthropics/skills)、[wshobson/agents](https://github.com/wshobson/agents)、[PM Skills](https://github.com/phuryn/pm-skills)、[awesome-copilot](https://github.com/github/awesome-copilot)、[claude-skills](https://github.com/alirezarezvani/claude-skills)、[mattpocock/skills](https://github.com/mattpocock/skills) 和 [Waza](https://github.com/tw93/Waza)。借鉴的是实现前确认、UI 风格一致、架构/API/数据库分工、按数据库引擎设计、证据优先和小职责边界。没有复制它们的 Skill 文本或运行时代码，也没有引入强制模式、强制文档、自动提交和默认架构套路。

## 许可证

[MIT](LICENSE) © 2026 Alvin Yang
