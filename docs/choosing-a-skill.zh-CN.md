# 如何选择 Skill

按当前要交付的东西选择主 Skill。命中具体领域或产物时，由专用 Skill 主导；AY Skills 只在需要时补充批准和证据边界。

## 常见产品交接

一条常用顺序是：

```text
ay-product → ay-ui → ay-architecture → ay-api → ay-database → ay-implement → ay-integration-docs
```

这不是强制流水线。技术可行性会阻塞 UI 时，可以提前做架构。没有其他客户端消费接口变化时，不需要 `ay-integration-docs`。需要只读检查时再用 `ay-review`。每个 Skill 也能从已有输入单独工作。

## 容易混淆的情况

| 请求 | 主 Skill |
|---|---|
| 用真实专家的公开方法分析开放问题 | `ay-expert-lens`；具体产物和执行仍由领域 Skill 负责 |
| 第一人称模拟专家或名人 | 专用人格 Skill；`ay-expert-lens` 不冒充本人 |
| 设计新的 API、事件或消息契约 | `ay-api` |
| 给某个客户端写本期已确认或已实现的契约变化 | `ay-integration-docs` |
| 根据 OpenAPI 生成完整公共参考 | 专用 API 文档生成器 |
| 上传、提交 App Store、检查审核状态或处理拒审 | 专用 App Store 发布 Skill |
| 用发布构建生成真实上架宣传图 | `ay-store-screenshots` |
| 生成并安装 Apple AppIcon 或 `.icns` | 有专用 Apple 图标 Skill 时由它主导；开放的隐喻和方向由 `ay-icon` 主导 |
| 只诊断故障，不要求修复 | 专用诊断流程；需要一并修复时用 `ay-fix` |
| 选择或深化模块接口与边界 | 专用代码库设计 Skill；边界确认后再用 `ay-improve` |
| 从某个 commit、分支或 merge base 评审代码 | 专用 diff 评审 Skill；跨产品和交付物时用 `ay-review` |
| 写自然中文长文 | 专用中文写作 Skill；调研、英文或图解型内容用 `ay-write` |

仍然难以区分时，只安装拥有当前交付物的那个 Skill，或者在请求中直接点名。
