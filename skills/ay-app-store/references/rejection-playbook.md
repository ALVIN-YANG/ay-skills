# App Review 驳回处理手册

只把模式用于定位，不预判 Apple 一定接受。最终以当前 App Review 消息、当前构建和官方规则为准。

## 先分流

| 类型 | 常见证据 | 通常动作 |
| --- | --- | --- |
| 代码/二进制 | 崩溃、功能失效、权限用途文案打包在 Info.plist | 修代码或配置，递增 Build，重新上传 |
| 元数据 | 描述、截图、URL、审核说明、EULA 缺失 | 在可编辑状态下修后台字段；确认是否需要新 Build |
| IAP/订阅 | 商品缺字段、没进 submission、付费页披露不足 | 修商品/付费页/审核截图，核对 submission 组合 |
| 需要解释 | 审核人员找不到入口、需要硬件或账号 | 在 Resolution Center 回复精确路径和证据 |
| 账号/商业 | 协议、税务、银行、主体或地区问题 | Account Holder/财务处理；不要用代码修复 |

## 5.1.1 权限与隐私

症状：用途文案只写“需要相机权限”“用于 App 功能”，或隐私政策/标签与真实数据流不一致。

处理：

1. 从代码确认权限在哪个用户动作触发、读取什么数据、数据用于什么结果、是否离开设备。
2. 用途文案同时说明用户动作、数据类型和用途。例如“仅在你选择拍照时使用相机，把证件、合同或票据照片加入当前私人资料”。
3. 核对拒绝权限后的路径，不在启动时抢先请求。
4. 同步核对 App 内隐私入口、App Store Connect 隐私 URL、隐私政策和 App Privacy。
5. 用实际打包后的 Info.plist 验证，不只看源码字符串目录。

## 3.1.2 订阅和 Terms/EULA

症状：付费页缺自动续订、周期、价格、权益、隐私政策或 Terms/EULA；商店描述无法看到 EULA；商品和 App 没一起提交。

处理：

1. 付费页展示方案名称、周期、当前 StoreKit 价格、权益、自动续订和管理/取消说明。
2. 在购买入口附近提供可用的 Privacy Policy 与 Terms/EULA 链接；App 内打开可以，必须让用户看得到。
3. 采用 Apple 标准 EULA 时，按当前后台/审核要求在元数据中提供可见链接；自定义 EULA 则在 App Information 正确配置。
4. 对比代码、本地 `.storekit` 与 App Store Connect 的 Product ID、类型、周期、价格、Family Sharing 和权益。
5. 首次自动续订订阅、首次非消耗型等按 Apple 当前规则与新 App 版本一起提交；新订阅组也加入同一 submission。

## 提交单无法添加商品

症状：商品已创建但 Add for Review 不可用，或旧 submission 无法加入新增 IAP。

处理：

1. 读取每个商品、订阅组、App 版本和 submission 的当前状态。
2. 判断是缺少本地化/价格/审核截图/可用性，还是项目已绑定其他 submission。
3. 不盲目取消旧 submission。先列出取消会移除的项目和重新提交影响，再取得授权。
4. 创建新 submission 后逐项重新读取，确认 App 版本、Build、组和商品都在其中。

## 审核邮件只有摘要

症状：邮件写“Changes needed”但没有具体问题。

处理：

1. 打开邮件中的 App Review 详情链接。
2. 读取所有被拒项目、Guideline、审核备注、截图/附件和 Resolution Center 消息。
3. 一个 submission 可能有多个原因；全部建档后再修复。

## 修复后是否需要发邮件

- Apple 明确要求信息时，在原 Resolution Center 线程回复。
- 仅需改代码/元数据且已经重新提交时，通常等待审核，不重复发通用邮件。
- 状态长时间异常时再走 App Review Status 支持渠道，并记录 case ID；不把支持邮件当作 submission。

## 验证完成条件

- 新 Build 或元数据已在 App Store Connect 可见。
- 正确项目进入正确 submission。
- 提交后取得 Submission ID，重新读取状态和项目列表。
- 通过后再验证 Ready for Distribution/销售状态和实际 storefront；审核通过不自动证明已可下载。
