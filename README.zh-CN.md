<div align="center">
  <h1>AY Skills</h1>
  <p><strong>为高级 AI 编程 Agent 设计的轻量、人类批准工作流。</strong></p>
  <p>
    <a href="https://github.com/ALVIN-YANG/ay-skills/actions/workflows/test.yml"><img src="https://img.shields.io/github/actions/workflow/status/ALVIN-YANG/ay-skills/test.yml?branch=main&style=flat-square&label=tests" alt="测试"></a>
    <a href="https://github.com/ALVIN-YANG/ay-skills/releases"><img src="https://img.shields.io/github/v/release/ALVIN-YANG/ay-skills?style=flat-square" alt="版本"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="MIT 许可证"></a>
  </p>
  <p><a href="README.md">English</a></p>
</div>

高级模型通常已经会写代码，真正难的是协作：它可能没弄清背景就开始猜，把模糊需求擅自变成产品决策，或者方向已经明确还在重复请示。

AY Skills 只给模型一份协作契约：

> **先理解背景，只获取一次方向批准，在批准边界内完成工作，并证明真实结果。**

<p align="center">
  <img src="assets/ay-skills-map.zh-CN.svg" alt="按任务选择 AY Skill：新工作使用 ay-work，故障修复使用 ay-fix，基于证据的优化使用 ay-improve，图文写作使用 ay-write，评审使用 ay-review。" width="100%">
</p>

## 五个独立 Skill

| Skill | 适用场景 | 核心作用 |
|---|---|---|
| [`ay-work`](skills/ay-work/SKILL.md) | 产品需求、用户场景、新功能、架构和普通变更 | 对齐模糊方向，然后实现并验证批准的结果 |
| [`ay-fix`](skills/ay-fix/SKILL.md) | Bug、回归、崩溃、偶发测试、异常变慢 | 先证明根因，再做最小授权修复 |
| [`ay-improve`](skills/ay-improve/SKILL.md) | 重构、架构、性能、可维护性 | 有真实基线才允许改结构 |
| [`ay-write`](skills/ay-write/SKILL.md) | 自然技术写作和图文文章 | 先对齐观点、大纲、来源和有效配图，再成稿 |
| [`ay-review`](skills/ay-review/SKILL.md) | Diff、分支、方案和发布准备度 | 默认只读，只报告有影响且有证据的问题 |

可以安装一个，也可以全部安装。每个 Skill 都能独立工作，不依赖路由器或其他 AY Skill。

## 安装

用可移植 Agent Skills 方式同时安装到 Codex 和 Claude Code：

```bash
npx skills@latest add ALVIN-YANG/ay-skills -a codex claude-code -g -y
```

去掉 `-y` 可以选择单个 Skill 或安装到当前项目：

```bash
npx skills@latest add ALVIN-YANG/ay-skills
```

Claude Code 也支持原生插件安装：

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

这些 Skill 默认由模型按任务自动触发，也可以显式调用：

```text
使用 $ay-work 给应用增加导出流程。
使用 $ay-fix 诊断并修复这个偶发测试。
使用 $ay-improve 基于真实基线简化这个模块。
使用 $ay-write 写一篇实用的图文技术文章。
使用 $ay-review 只读评审当前分支。
```

## 一次批准，不是无限检查点

| 用户请求 | AY 的行为 |
|---|---|
| “把 Retry 改成 Try again，并运行 UI 检查。” | 指令本身已经批准，直接调查、修改、验证 |
| “优化一下首页。” | 先调查，提出一个推荐方向，修改前等待批准 |
| “修复这个 Bug。” | 先诊断；只有根因修复唯一、局部、可逆且不改变预期行为时才直接修 |
| “评审这个分支。” | 只读检查和报告，不自动修复 |
| “实施批准的方案，检查通过就推送。” | 按方案实施并推送，除非批准边界发生变化，否则不重复请示 |

只有新证据会改变产品行为、架构、数据契约、依赖、范围、风险、费用、回滚或外部操作时，才重新申请批准。普通实现细节由 Agent 自主决定。

## 图文写作，不盘问绘图工具

`ay-write` 会把核心观点、大纲和配图计划一起提交批准。批准后，根据表达目的和当前已有能力自动选择：

| 表达需要 | 默认形式 |
|---|---|
| 精确的小型图解 | SVG |
| 复杂、可编辑的架构 | draw.io 源文件和导出图 |
| 概念或手绘风解释 | Excalidraw 源文件和导出图 |
| 数据结论 | 有可追溯数据的图表 |
| 封面、场景或隐喻 | 生图 |

只有风格或可编辑性会改变交付结果时，才询问绘图工具。安装插件、依赖、付费能力或项目运行时仍然需要批准。

## 刻意保持轻量

- 只有五个 Skill，没有路由器和模式标签。
- 每个 `SKILL.md` 不超过 150 行和 500 个正文英文单词。
- 没有 hooks、遥测、状态栏、bootstrap、全局规则、自动提交或强制规划文档。
- 所有宿主共用同一份可移植 `SKILL.md` 源码。
- 源码测试、插件校验、隔离安装、宿主行为、CI、Release 内容和远程安装分别报告，不混为一种证明。

## 兼容性

Codex 行为和两种宿主的可移植安装已经验证。Claude Code 的原生 manifest、隔离 marketplace 安装和五个 Skill 发现已经验证；仓库包含其实时行为测试，但运行时需要 Claude API 可连接。其他实现 [Agent Skills 规范](https://agentskills.io/specification) 的工具可以读取相同目录，但没有真实测试前不会宣称完整支持。

## 开发与验证

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/run_behavior_evals.py --host codex
python3 scripts/run_behavior_evals.py --host claude
```

行为集覆盖明确小改、模糊功能、Bug 批准边界、基于证据的优化、图文写作、只读评审、外部操作和单 Skill 自动触发。

## 灵感来源

AY Skills 是原创项目，受到以下项目启发：

- [mattpocock/skills](https://github.com/mattpocock/skills)：事实与决策分离的 grilling，以及克制、可组合的 Skill 设计。
- [obra/superpowers](https://github.com/obra/superpowers)：根因优先、方向性变更先批准、完成前必须有证据。
- [tw93/Waza](https://github.com/tw93/Waza)：结果与证据契约、范围克制、项目上下文调查和自然写作。

三个项目均使用 MIT 许可证。AY Skills 没有复制其 Skill 文本或运行时代码。

## 许可证

[MIT](LICENSE) © 2026 Alvin Yang
