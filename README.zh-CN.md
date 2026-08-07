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

AY Skills 来自我每天和 AI 一起做事时反复遇到的五件烦心事：需求没听明白就开工，Bug 靠猜，重构没有基线，文章像说明书，评审时顺手把代码也改了。

所以我把它们做成了五个可以单独安装的 Skill。任务说清楚了就直接做；还有产品或技术上的关键选择，就先调查、问一次，然后在你确认的范围内完成。

<p align="center">
  <img src="assets/ay-skills-map.zh-CN.svg" alt="按任务选择 AY Skill：新工作使用 ay-work，故障修复使用 ay-fix，基于证据的优化使用 ay-improve，图文写作使用 ay-write，评审使用 ay-review。" width="100%">
</p>

## 五个 Skill

| Skill | 什么时候用 | 它会做什么 |
|---|---|---|
| [`ay-work`](skills/ay-work/SKILL.md) | 做新功能，或者需求还没说清楚 | 弄清关键选择，再实现并验证结果 |
| [`ay-fix`](skills/ay-fix/SKILL.md) | 排查 Bug、回归、崩溃、偶发失败或异常变慢 | 先确认根因，再做最小有效修复 |
| [`ay-improve`](skills/ay-improve/SKILL.md) | 重构，或者优化性能和可维护性 | 先建立基线，修改后再比较结果 |
| [`ay-write`](skills/ay-write/SKILL.md) | 写文章、教程、长篇改稿或图文解释 | 写出自然、清楚、没有废话的长内容 |
| [`ay-review`](skills/ay-review/SKILL.md) | 评审代码、分支、方案或发布准备度 | 默认只读，只报告重要且有证据的问题 |

可以只装一个，也可以全部安装。它们彼此不依赖，不需要路由器，也不会把一个小改动变成一场规划会议。

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

平时直接描述任务即可，匹配时会自动使用。想明确指定也可以：

```text
使用 $ay-work 给应用增加导出流程。
使用 $ay-fix 诊断并修复这个偶发测试。
使用 $ay-improve 从真实基线出发简化这个模块。
使用 $ay-write 把这些笔记写成清楚好读的图文文章。
使用 $ay-review 评审这个分支，不要修改文件。
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

评审是个例外：除非你明确要求修复，`ay-review` 始终只读。

## 写文章时怎么配图

`ay-write` 会先想清楚文章要讲什么、怎么组织、每张图解决什么问题，再选工具。小而精确的图解用 SVG，需要编辑的架构图用 draw.io 或 Excalidraw，数据结论用来源可追溯的图表，封面和场景才考虑生图。

只有风格或可编辑性会改变结果，或者需要安装新工具、依赖、付费服务和项目运行环境时，它才会问你。

## 就这五个

没有路由器、模式标签、hooks、遥测、状态栏、自动提交或强制规划文件。每个 Skill 只做一件事，也能单独安装。

AY Skills 遵循 [Agent Skills 规范](https://agentskills.io/specification)。Codex 和 Claude Code 的便携安装已经测试，Claude Code 原生插件单独测试。Codex 插件清单已经按本地市场测试和以后提交公共目录的要求校验，但目前不声称已公开上架。其他宿主没有实测前，不写“完整支持”。

<details>
<summary>开发与验证</summary>

```bash
python3 scripts/verify_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/run_routing_evals.py --host codex
python3 scripts/run_routing_evals.py --host claude
python3 scripts/run_behavior_evals.py
```

CI 运行结构和单元测试。路由测试覆盖五个 AY Skill、不该触发 AY 的请求，以及专用 Skill 共存场景。Codex 黑盒测试会真的执行隔离任务，检查文件是否该改、是否在批准点停下、只诊断不修改、文章是否生成，以及评审是否保持只读。实时测试需要本机 CLI 和可用账号；黑盒执行目前只覆盖 Codex。

</details>

## 灵感来源

AY Skills 是原创项目，受到 [mattpocock/skills](https://github.com/mattpocock/skills)、[Superpowers](https://github.com/obra/superpowers) 和 [Waza](https://github.com/tw93/Waza) 启发：有用的追问、根因优先，以及边界清楚的小 Skill。没有复制它们的 Skill 文本或运行时代码。

## 许可证

[MIT](LICENSE) © 2026 Alvin Yang
