# AY Skills

[![测试](https://img.shields.io/github/actions/workflow/status/ALVIN-YANG/ay-skills/test.yml?branch=main&style=flat-square&label=tests)](https://github.com/ALVIN-YANG/ay-skills/actions/workflows/test.yml)
[![版本](https://img.shields.io/github/v/release/ALVIN-YANG/ay-skills?style=flat-square)](https://github.com/ALVIN-YANG/ay-skills/releases)
[![MIT 许可证](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)

[English](README.md)

AY Skills 是十五个可以单独安装的 coding-agent Skill。每个 Skill 都写清楚三件事：什么时候可以直接做，什么决定需要你确认，做到哪一步才算有证据。

## 快速开始

先看列表，再选择要安装的 Skill：

```bash
npx skills@latest add ALVIN-YANG/ay-skills -l
npx skills@latest add ALVIN-YANG/ay-skills
```

平时直接描述任务即可。只有想强制指定时，才需要写 `$ay-implement` 之类的名字。

```text
给这个应用增加 CSV 导出，并验证真实结果。
```

## 它怎么工作

- 目标和结果明确，直接完成。
- 如果要替你决定产品行为、架构、数据契约、依赖、范围、风险、费用、回滚或外部操作，先停下来确认。
- 方向确认后，在约定范围内继续做到验证完成，并说明真正验到了哪一层。
- 评审默认只读，除非你明确要求修复。

这些 Skill 彼此独立，不需要路由器、共享运行时、模式标签、hooks、遥测、自动提交或强制规划文件。

## Skill

### 产品与设计

| Skill | 适合处理 |
|---|---|
| [`ay-expert-lens`](skills/ay-expert-lens/SKILL.md) | 用真实专家公开的方法分析开放问题 |
| [`ay-product`](skills/ay-product/SKILL.md) | 调查产品设想，给出聚焦且可验证的方向 |
| [`ay-ui`](skills/ay-ui/SKILL.md) | 确定视觉方向、设计页面并整理 UI 交接 |
| [`ay-architecture`](skills/ay-architecture/SKILL.md) | 确定系统边界、归属、部署与故障行为 |
| [`ay-api`](skills/ay-api/SKILL.md) | 设计面向调用方的接口、事件、Webhook 与服务契约 |
| [`ay-database`](skills/ay-database/SKILL.md) | 按具体数据库设计表、索引、事务与迁移 |

### 开发与交接

| Skill | 适合处理 |
|---|---|
| [`ay-implement`](skills/ay-implement/SKILL.md) | 落地确认过的变更并验证结果 |
| [`ay-integration-docs`](skills/ay-integration-docs/SKILL.md) | 只写指定客户端需要的接口和消息变化 |
| [`ay-fix`](skills/ay-fix/SKILL.md) | 确认 Bug 根因，再做最小有效修复 |
| [`ay-improve`](skills/ay-improve/SKILL.md) | 从真实基线出发重构或优化 |
| [`ay-review`](skills/ay-review/SKILL.md) | 只读检查产品、设计、代码和交付结果 |

### 专项工作

| Skill | 适合处理 |
|---|---|
| [`ay-audio`](skills/ay-audio/SKILL.md) | 实现或排查 Apple 平台的流式 TTS 与语音播放 |
| [`ay-write`](skills/ay-write/SKILL.md) | 写作或大幅修改文章、教程与图文说明 |
| [`ay-icon`](skills/ay-icon/SKILL.md) | 设计并安装商店或启动器图标 |
| [`ay-store-screenshots`](skills/ay-store-screenshots/SKILL.md) | 用发布版本的真实 UI 制作可复现的 App Store 宣传图 |

常见职责冲突和产品交接顺序见 [如何选择 Skill](docs/choosing-a-skill.zh-CN.md)。

## 一个例子

```text
你：增加离线模式。

AY：当前应用默认一直联网。我建议首版只允许离线查看缓存数据，明确显示
数据更新时间，不做离线写入和自动排队。验收覆盖冷启动、断网查看和恢复联网。
按这个边界做吗？

你：可以。

AY：已按确认范围完成并通过相关测试。离线写入仍不在本次范围；真机恢复联网
是目前唯一没有验证的环节。
```

## 仓库里的验证

测试会检查 Skill 路由、实际行为、受保护文件、生成物复现、独立安装、发布包和连续交接。FieldLog、PairDown、NextStop 三条完整旅程都是合成测试，不冒充用户研究或线上成绩。输入和断言见 [`tests/journey-scenarios.json`](tests/journey-scenarios.json)。

开发命令和各验证层级的边界见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 其他安装方式

给 Codex 和 Claude Code 安装全部十五个 Skill：

```bash
npx skills@latest add ALVIN-YANG/ay-skills -s '*' -a codex claude-code -g -y
```

<details>
<summary>Claude Code 插件和维护命令</summary>

```text
/plugin marketplace add ALVIN-YANG/ay-skills
/plugin install ay-skills@ay-skills
```

```bash
npx skills@latest list -g
npx skills@latest update -g
npx skills@latest remove ay-audio -g
```

</details>

AY Skills 遵循 [Agent Skills 规范](https://agentskills.io/specification)。Codex 清单只用于本地市场测试和以后可能的公共目录提交，本项目没有声称已经公开上架 Codex 插件。

## 来源与许可证

项目代码和说明均为原创，开发时参考过一些 agent-skill 与应用交付项目。具体来源、许可证和借鉴边界记录在 [docs/influences.md](docs/influences.md)。

[MIT](LICENSE) © 2026 Alvin Yang
