# Apple 官方发布流程参考

核对日期：2026-08-16。政策与后台字段可能变化；每次正式发布时重新打开相关官方页面。

## 必查官方来源

- App Review Guidelines：https://developer.apple.com/app-store/review/guidelines/
- 提交审核概览：https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/overview-of-submitting-for-review/
- 提交 App 版本：https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-app/
- 提交 IAP/订阅：https://developer.apple.com/help/app-store-connect/manage-submissions-to-app-review/submit-an-in-app-purchase/
- App 信息必填/可编辑属性：https://developer.apple.com/help/app-store-connect/reference/app-information/required-localizable-and-editable-properties
- App Privacy：https://developer.apple.com/help/app-store-connect/manage-app-information/manage-app-privacy/
- 隐私标签说明：https://developer.apple.com/app-store/app-privacy-details/
- 配置 IAP 概览：https://developer.apple.com/help/app-store-connect/configure-in-app-purchase-settings/overview-for-configuring-in-app-purchases/
- 自动续订订阅：https://developer.apple.com/help/app-store-connect/manage-subscriptions/offer-auto-renewable-subscriptions/
- 自定义/标准 EULA：https://developer.apple.com/help/app-store-connect/manage-app-information/provide-a-custom-license-agreement
- 协议：https://developer.apple.com/help/app-store-connect/manage-agreements/sign-and-update-agreements/
- 银行：https://developer.apple.com/help/app-store-connect/manage-banking-information/enter-banking-information/
- 税务：https://developer.apple.com/help/app-store-connect/manage-tax-information/provide-tax-information

## 提交前事实清单

### App 和构建

- App Store Connect 中存在匹配 Bundle ID 的 App 记录。
- 版本、Build、平台、签名 Team、SKU 和 Apple App ID 已核对。
- 上传包已完成 Apple processing，不只停留在本地上传成功。
- 正确 Build 已关联到正确 App Store 版本。
- 出口合规和加密问题已按实际代码回答。

### 元数据

- 每个目标语言的名称、副标题、描述、关键词、支持 URL 和截图完整。
- 描述和截图与当前 Build 一致，并明确 IAP 才能获得的能力。
- 隐私政策 URL 可公开访问；App 内也有易于找到的入口。
- 年龄分级、内容权利、类别、版权、Review Contact 和 Review Notes 完整。
- 使用标准 EULA 或正确配置自定义 EULA；订阅页面和元数据提供适用的 Terms/EULA 信息。

### 隐私和权限

- App Privacy 回答覆盖 App 和第三方 SDK 实际收集的数据。
- 权限用途文案清楚、完整并对应真实触发点。
- PrivacyInfo.xcprivacy 和被 Apple 点名的第三方 SDK 隐私清单/签名要求已核对。
- 账号创建、删除和免登录规则按 App 实际能力处理。

### IAP/订阅

- Product ID、类型、权益、周期、价格和可用地区在代码、本地 StoreKit 和后台一致。
- IAP 有本地化、价格、可用性、审核截图和审核说明。
- 可恢复购买有恢复入口；退款、撤销、Family Sharing 和订阅过期按产品规则处理。
- 首次提交某种 IAP/订阅时与新 App 版本一起提交；新订阅组至少带一个订阅。
- 提交单中实际包含 App 版本、需要审核的 IAP、订阅和订阅组。

### 账号与收款

- Account Holder 已接受当前 Paid Apps Agreement。
- 税务和银行状态完整、有效；法律主体和银行持有人信息逐字一致。
- DSA/商家身份等适用声明无待办。

## 规则解释边界

- Apple 的 App Review 邮件可能只通知“Changes needed”；具体原因以 App Review 详情页为准。
- 每个平台同一时间通常只有一个含 App 版本的 submission 在审；其他项目的并行限制以当前后台为准。
- API、网页和第三方 CLI 覆盖范围不同。能写字段不等于能完成账号协议、税务、银行或所有首次 IAP 流程。
- 标准 EULA 默认适用不代表订阅审核页面一定能从元数据看到 Terms 链接；按实际审核反馈和当前后台要求补齐可见入口。
