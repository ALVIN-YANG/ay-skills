# 工具选择与安全边界

## 选择顺序

1. **本地只读工具**：`rg`、`plutil`、`xcodebuild -showBuildSettings`、本 Skill 扫描脚本。用于建立代码和配置事实。
2. **Apple 官方工具/API**：Xcode Organizer、Transporter、`xcodebuild`、App Store Connect API。用于构建、上传和受支持的后台操作。
3. **已登录网页**：用于 App Review 详情、Resolution Center、协议、税务、银行、角色限制和 API 未覆盖字段。
4. **项目已有发布工具**：Fastlane 或 CI。先读现有配置，避免重新搭建或覆盖签名。
5. **第三方 CLI**：只有在用户同意安装/使用且已核对来源、版本和认证方式后采用。

## 可参考的开源项目

- `tddworks/asc-cli`：https://github.com/tddworks/asc-cli
  - 提供公开 App Store Connect API 的较完整命令面、JSON 输出和 readiness/status 查询。
  - 部分首次 IAP 和 Resolution Center 功能依赖其 `iris` 私有 API/cookie 路径；默认不要使用这些路径。
- `fastlane/fastlane`：https://github.com/fastlane/fastlane
  - 适合已有 Fastlane 的项目继续复用上传、元数据和 TestFlight 流程。
- `sosteam65/app-store-connect-skill`：https://github.com/sosteam65/app-store-connect-skill
  - MIT Skill，覆盖很多 REST 操作，可作为命令面索引；不要直接采用其明文 credentials 文件模式，也不要假设列出的操作都能由公开 API 完成。
- `tinh2/skills-hub-registry` 的 `store-compliance` / `app-store-publish`
  - 适合作为静态检查项参考；其自动生成 Fastlane、签名和“发现问题就修复”的默认行为不适合已有脏工作树或只读审计。

本 Skill 原创整合流程，不复制无明确许可证仓库的文本或代码。

## 凭据

- `.p8` 私钥只存安全目录；仓库仅记录路径或密码管理器条目名。
- 不把 Key ID、Issuer ID、Apple ID 密码、2FA、cookie、App 专用密码写入聊天、Markdown、脚本或 Git。
- 允许工具从 Keychain、安全凭据文件或临时环境变量读取；输出前检查日志是否泄露。
- 使用第三方工具前查看它如何保存凭据。cookie 抽取、私有 API 和浏览器会话复用需要单独风险判断。

## 浏览器操作

- 每次页面跳转或刷新后重新获取可见元素，不复用旧索引。
- 输入前核对 App 名、平台、版本和 submission。
- 点击 Submit、Cancel、Delete、Agree、Publish、价格/地区保存前满足动作级授权。
- 动作完成后读取确认页、toast、Submission ID 和项目状态；只看到按钮消失不算成功。

## API/CLI 操作

- 优先运行 list/get/check-readiness，再运行 update/submit。
- 保存原始 JSON 回包或脱敏摘要，记录资源 ID。
- 遇到 200/0 exit code 仍要检查业务状态和错误数组。
- 重试前确认操作是否幂等；创建 submission、商品、版本和回复消息不能盲重试。
