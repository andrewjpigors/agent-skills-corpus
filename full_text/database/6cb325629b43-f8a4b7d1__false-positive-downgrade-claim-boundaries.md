---
name: false-positive-downgrade-claim-boundaries
description: Use when deciding whether a suspected vulnerability, scanner finding, report claim, audit note, or agent assertion should be downgraded, rejected, marked blocked, marked 需要外部门禁裁决, or constrained with explicit allowed and forbidden claims.
---

# 误报降级与声明边界

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态；提交资格只属于 finding，不裁决整个 case 完成。
- 声明边界只授权报告措辞，不裁决 case 完成；case 完成必须由机器完成门禁结果裁决。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

这个 Skill 的任务是把“看起来像漏洞”的东西压回证据本身：什么能 technical_confirmed，什么只能 需要外部门禁裁决，什么只能 candidate，什么必须 blocked，什么应该 rejected，以及当前证据到底允许声明什么、禁止声明什么。它不是保守化模板，而是证据纪律模板：在自有、明确允许、可回滚的实验环境中，应当继续追踪到当前可证明的最高影响；但任何声明都不能超过 source、sink、trace、运行态、负控、清理、官方安全模型和 对外提交资格 证据的上限。

调用时先写一行目标句：

```text
我要裁决：{候选发现 / 扫描器告警 / 外部模型/工具结论 / 报告 claim} 是否应降级、拒绝、保留 candidate、标记 blocked、标记 需要外部门禁裁决，或保留 technical_confirmed 但收缩声明边界。
```

典型触发场景：

- 只有 scanner 命中、危险函数、版本号、secret 正则、HTTP 200、错误栈、callback、marker、截图或 外部模型/工具自述。
- 报告声称 technical_confirmed / high / critical / exploitable，但缺 source、sink、trace、负控、影响证明、运行态证据或清理恢复证据。
- 需要把 `pending / suspected / possible / likely / exploitable / verified / fixed / triaged / resolved / informative` 统一裁决成 `technical_confirmed / candidate / blocked / rejected`。
- 需要写 `allowed_claims / forbidden_to_claim_now / not_yet_proven_claims / proven_blocked_claims`，明确当前证据能说什么、暂不能说什么、哪些方向尚待补证、哪些方向已有排除证据。
- 需要给扫描器 finding、漏洞报告、复现记录、审计笔记、Bug Bounty 提交或其他模型/工具 输出做误报复核、降级说明或补证计划。
- 需要裁决 callback-only SSRF、marker-only RCE、error-only SQLi、reflect-only XSS、status-only IDOR、version-only SCA、regex-only secret、CSRF form-only、XXE parser-only 等夸大场景。
- 需要避免为了凑数量写低价值漏洞，或避免把未证明影响的点写成高危。

每次使用至少输出：

```text
Finding：
原始状态：
人工状态：本 Skill 只给 technical_status 方法性建议；提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决。
证据状态：route / source / trace / sink / transform / runtime / impact / negative control / cleanup / security model
外部门禁引用：提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决；本 Skill 不复制枚举、不生成状态。
标识符获取：{需要哪些 ID / handle / token / URI；攻击者如何获得；单对象/多对象/批量/不可获得}
账号矩阵：{attacker / owner / victim / control / cleanup；内部复核记录账号对象矩阵必要事实、主体 ID、租户/工作区、角色、对象归属、token/cookie 引用}
allowed_claims：
forbidden_to_claim_now：
not_yet_proven_claims：
proven_blocked_claims：
Missing Evidence：
blocks_finding_submit：
blocks_case_completion：
停止继续升级原因：
下一步补证或修复：
```

本 Skill 不代替漏洞类型专项、语言专项、Source-to-Sink、动态验证、漏洞报告复核或官方门禁；它负责把这些结果转成“能不能写、能写到多强、必须删掉什么”的裁决。报告级 technical_confirmed 必须比单点技术命中更严格；对外提交 又必须比technical_confirmed 更严格，因为它会直接影响修复优先级、提交状态、风险等级和对外声明。

## 核心原则

### 1. 降级不是保守，是证据纪律

只看到 sink 不是漏洞；必须证明 source 可控、trace 闭合、防护不足、影响真实。任何一项缺证据、为 unknown、为 not_satisfied，或被负控否定，都不得写 technical_confirmed。

### 2. 证据上限决定声明上限

`allowed_claims` 只能写证据已经证明的最小准确句子。`forbidden_to_claim_now` 必须明确列出当前报告不得写的更强句子，但不得被当作方向排除证据。

声明边界必须拆成四类：

- `allowed_claims`：当前证据已经允许报告阶段渲染的声明。
- `forbidden_to_claim_now`：当前报告不得写的强声明，只限制措辞，不代表方向已排除。
- `not_yet_proven_claims`：尚未证明但仍可能成立的方向，必须有 `missing_refs`，并按情况设置 `blocks_finding_submit` / `blocks_case_completion`。
- `proven_blocked_claims`：已有负控、官方模型、范围、配置、版本或其他排除证据证明不能成立的声明，必须有排除证据引用。

`forbidden_to_claim_now` 不能当作排除证据，不能关闭审计方向，不能替代最高影响闭环和缺失证据 backlog。当前不能声明 RCE、SSRF、文件写入、模板写入、账号接管、跨租户等高危方向时，必须判断它是 `not_yet_proven_claims` 还是 `proven_blocked_claims`；不能只写一句“当前禁止声明”就收口。

| 现有证据 | 允许声明 | 禁止声明 |
|---|---|---|
| 只触发 DNS callback | 服务端会解析并请求受控域名，需继续验证最终目标与响应 | 内网可读、metadata 泄露、任意内网扫描 |
| 只看到 marker 字符串回显 | 输入影响响应内容或模板输出，需证明执行语义 | 命令执行、shell、服务器沦陷 |
| 只看到错误栈 | 查询构造可能受输入影响，需布尔/时间/常量/测试数据证明 | 数据库可读取、整库泄露 |
| 只换 ID 返回 200 | 对象 ID 可影响响应，需 A/B 主体、对象归属、标识符获取链和账号矩阵 | 越权读取他人数据、稳定可利用、批量越权 |
| 只正则命中 | 疑似凭据暴露，需攻击者可获得性、有效性、权限和轮换 | 有效密钥泄露、已被利用 |

### 3. 工具只能发现线索，不能替代语义裁决

扫描器 severity、CodeQL/Semgrep trace、DAST callback、SCA version hit、secret regex、外部模型/工具语言结论、AI triage、截图 OCR 都只是候选来源。最终裁决必须回到：入口可达、source 可控、trace 闭合、transform 防护、sink 危险参数、运行态差异、负控、影响、安全模型。

检验句：**如果删除工具名称、规则 ID 和 外部模型/工具结论，只保留代码/请求/响应/日志/副作用，漏洞是否仍能成立？**

### 4. 技术成立仍可能不是 对外提交资格

误报降级不仅要判断“技术现象是否发生”，还要判断“这条声明是否能作为漏洞报告成立”。必须把状态拆成两层：

- 技术状态：route、source、trace、sink、transform、强正控、负控、清理是否闭合。
- 报告状态：官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决）、duplicate、提交材料质量要求是否支持当前声明。

如果技术链路成立，但官方安全模型、范围、默认配置或已知风险基线不支持对外漏洞声明，应写 `需要外部门禁裁决`，而不是为了避免“误报”二选一地写 technical_confirmed 或 rejected。

常见降级：

| 技术现象 | 正确状态 | 禁止外推 |
|---|---|---|
| 强正控证明 debug 配置泄露，但默认配置未证明 | 需要外部门禁裁决 / candidate | 默认生产受影响 |
| 管理员或插件作者可执行危险操作，官方模型认为该主体受信任 | 需要外部门禁裁决 / rejected | 未认证、低权限、越权 |
| 沙箱内可执行预期能力，但没有逃逸边界 | 需要外部门禁裁决 / rejected | 沙箱逃逸、宿主机控制 |
| 问题与官方 known issue / accepted risk 重合，无新边界 | 需要外部门禁裁决 / rejected | 新漏洞、官方未公开 |
| 范围、默认配置、版本或 duplicate 未读完 | candidate / blocked | 对外可提交、高危可提交 |

检验句：**我是在降级误报，还是在把一个真实技术现象错误地包装成可提交漏洞？如果官方边界不支持，只能写 需要外部门禁裁决 或继续补证。**

`technical_confirmed`、`validated`、`bounty_submit_ready`、`finding_submit_ready` 也都不能推出 `case_audit_complete`。本 Skill 只能收缩 finding 的技术声明和报告声明；全案完成必须检查高危面覆盖、最高影响闭环、缺失证据阻断、报告占位符和机器完成门禁。

### 5. 强验证默认用于授权可重置环境

在自有、明确授权、隔离、可重置、可清理环境中，不应满足于弱 marker。应按漏洞语义追踪当前范围内最高可证明影响：受控测试数据读取、测试对象写入、跨测试账号/租户访问、受控服务端请求、受控命令结果、受控回连、可清理文件、可回滚状态变更、最小资源曲线或组件可达触发。

边界同时必须清楚：不越出授权范围，不测试第三方真实系统，不读取真实生产用户数据，不输出真实凭据，不制造不可清理副作用。没有账号、对象、日志、快照、清理能力时，降级为 `blocked`，不要强行 technical_confirmed。

### 6. 负控是提交材料质量的一部分

负控不是额外可选项。报告要从“这个输入会触发”升级到“这个输入因为漏洞条件触发”，必须有负控排除正常功能、缓存、随机、权限本来允许、错误页、WAF、限流、测试数据污染、环境差异。

报告没有负控时：

- 可以是 `candidate`。
- 可以是 `blocked`。
- 不能是高置信 `technical_confirmed`。
- 不能写 High/Critical 的强影响声明，除非解释为什么负控不适用且有等价证据。

### 7. 风险等级必须解释，不照抄 severity

风险等级不是扫描器 severity、CVSS 数字或平台优先级的复述。评级必须说明：

- 攻击者需要什么权限。
- 入口是否默认暴露。
- source 是否完全可控。
- 影响是否真实证明。
- 是否跨用户、跨租户、跨沙箱、跨网络、跨文件或跨权限。
- 是否需要用户交互、特定配置、特定版本、特定 feature flag。
- 是否有官方已知、accepted risk、expected behavior、范围或官方已知拒绝（外部裁决） 或 duplicate 风险。
- 哪些因素让风险降级。

### 8. ID 类 claim 先降到可获得规模

只要 claim 依赖 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、资源 URI、对象 key、物理表名或其他对象标识符，就必须先裁决“攻击者能否获得该标识符”。

降级规则：

- 只有“已知 ID 后可利用”“替换 ID 返回 200”“拿另一个用户对象 ID 后成功”：不得写高价值 `technical_confirmed`，只能写 `candidate` 或 `blocked`，除非证明攻击者可获得路径。
- 只有管理员手工给出的 ID、报告作者笔记 ID、聊天上下文 ID、历史附件 ID、截图 ID：只能作为定位样本，不能算攻击者能力。
- 只证明一个样本 ID：`allowed_claims` 只能写该样本或同一获取路径下的对象；`forbidden_to_claim_now` 必须禁止“任意对象、全量、批量、所有用户、所有租户、所有工作区”，且若这些方向仍可能成立，必须进入 `not_yet_proven_claims` 并回链缺失证据。
- 证明列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口能稳定提供 ID：才可以按单对象、多对象、批量、持续或可推导规模写声明。
- 代码、接口和运行态都证明攻击者拿不到必要 ID：可写 `rejected`，但必须说明排除过哪些获取路径。

检验句：**如果删掉复核人手工提供的 ID，攻击者还能不能自己拿到目标 ID？如果报告写批量或全量，攻击者能不能稳定拿到足够多 ID？**

### 9. 多主体 claim 必须有账号对象矩阵

跨用户、跨租户、越权读写、未授权、CSRF 受害者上下文、存储型触发、批量对象、清理回滚这类 claim，必须能复核“谁操作了谁的对象”。内部材料至少记录 attacker、owner、victim、control、cleanup 的账号用途、用户名或邮箱、账号对象矩阵必要事实、主体 ID、tenant/workspace、role/scope、token/cookie 引用、对象归属、适用步骤和清理责任。

缺账号对象矩阵时：

- 不得写多主体 `technical_confirmed`。
- 不得把 owner/victim 普通账号写成管理员账号。
- 不得把中间件、容器、数据库、对象存储管理账号写成 Web 登录账号。
- 不得在内部复核材料缺账号对象矩阵必要事实时声称可重放。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

### 10. 敏感信息边界必须可复核

多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

## 审计目标

复核报告时必须回答十五个问题：

1. 报告中的每个 claim 是什么？是否被拆开？
2. 入口是否真实可达？route、handler、认证、中间件、feature flag 是否明确？
3. source 是否由攻击者控制？控制主体、权限、对象、租户、字段粒度是什么？
4. source 到 sink 的 trace 是否闭合？每一跳 file:line、变量、分支、权限是否可解释？
5. sink 的危险参数是否被污染？是否真的进入安全敏感语义？
6. transform、防护、鉴权、对象级授权、框架默认安全是否有效？
7. 运行态强正控是否证明了 CIA 影响或安全边界破坏？
8. 负控是否排除了误报、正常功能和环境噪声？
9. 最高危害是否已经追到当前授权范围上限？停止原因是否具体？
10. 报告阶段可渲染声明、禁止声明和缺失证据分别是什么？
11. 如果 claim 依赖 ID、URI、token、object key、物理表名或其他标识符，攻击者如何获得这些标识符？证据只支撑单对象、多对象、批量、持续、可枚举、可搜索、可导出、可推导还是不可获得？
12. 如果 claim 依赖多账号、多对象、跨租户、受害者上下文、清理动作或回归复测，账号对象矩阵是否足以让复核人区分 attacker、owner、victim、control、cleanup，并重放关键步骤？
13. 如果技术现象真实发生，官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决）、duplicate 和提交材料质量要求是否支持 对外提交资格？
14. 不能声明的更高影响属于 `not_yet_proven_claims` 还是 `proven_blocked_claims`？是否分别有缺失证据或排除证据？
15. 当前声明边界是否没有被用来关闭高危面覆盖、最高影响闭环或 case 完成阻断？

必须排除：

- scanner-only、external-tool-only、sink-only、source-only、trace-only。
- callback-only SSRF、marker-only RCE、error-only SQLi、reflect-only XSS、status-only IDOR、version-only SCA、regex-only secret。
- pending 写 technical_confirmed、fixed 无复测、resolved 无修复证据、duplicate 未去重、informative 写高危。
- 管理员正常能力、插件作者正常能力、沙箱内预期能力、配置 hardening、范围外、accepted risk 被写成新漏洞。
- technical_confirmed 被直接写成对外可提交；官方模型 unknown 被写成可提交漏洞。
- 报告只描述现象，没有攻击者条件、服务端条件、安全影响和安全模型。

## 输入材料

### 报告材料

- 标题、漏洞类型、风险等级、摘要、影响范围、前置条件。
- 复现步骤、Web 操作、curl、Burp 请求、截图、视频、payload、请求响应、日志片段。
- 影响证明：数据、状态、权限、文件、命令、浏览器、服务端请求、secret、组件触发、资源消耗。
- 标识符获取证明：对象 ID、用户 ID、租户/空间/项目 ID、文件 URI、分享 token、lookup handle、对象 key、物理表名、资源路径的来源、可获得规模和攻击者可达路径。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 修复建议、修复状态、复测结果、回归测试。
- `allowed_claims`、`forbidden_to_claim_now`、`not_yet_proven_claims`、`proven_blocked_claims`、Missing Evidence、停止继续升级原因。
- 外部门禁引用、官方安全模型裁决、对外提交阻塞项。

### 代码与配置材料

- route、controller/handler、service、repository/DAO/mapper、model、serializer、template、middleware/filter/interceptor、policy/guard。
- 配置、默认值、feature flag、profile、插件、路由缓存、依赖注入、AOP、队列、cron、事件监听。
- 依赖清单、lockfile、SBOM、镜像、运行包、构建产物、版本输出。
- 单元测试、集成测试、权限矩阵测试、安全 wrapper、修复 PR。

### 运行态材料

- 授权范围、环境类型、版本、配置、账号、角色、租户、测试对象、前置快照、清理能力。
- baseline、weak positive、strong positive、impact escalation、negative control、retest 请求。
- 响应、日志、审计日志、数据库、缓存、队列、文件、对象存储、OOB、浏览器、命令输出。
- 标识符获取运行态：列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列、批量接口、受害者主动分享或不可获得证据。
- 多主体运行态：不同账号、不同租户、自己对象、他人对象、无权限主体、过期/无效 token、清理账号的请求、响应和状态差异。
- 清理命令、恢复快照、复测后状态。

### 范围与安全模型材料

- 官方安全策略、scope、范围或官方已知拒绝（外部裁决）、known issues、accepted risk、默认配置、权限模型、release notes。
- 报告目标的资产、版本、模块、部署方式、第三方依赖和披露要求。
- 去重材料：历史报告、公告、issue、修复记录、重复工单。
- 官方对象模型、标识符暴露模型、角色模型、沙箱模型、网络模型、默认配置说明、提交材料质量要求。

## Source 识别

报告复核中的 Source 识别不是重新枚举所有输入，而是验证报告声称的攻击者可控点是否真实、具体、可复现。

### Source 复核问题

- source 是 query、path、body、header、cookie、JSON、XML、multipart、GraphQL、WebSocket、RPC、CLI、queue、webhook、file import、stored taint 还是 claim？
- 攻击者是谁：匿名、普通用户、低权限成员、租户管理员、owner、管理员、插件作者、部署者、内部服务、供应链输入？
- 控制粒度是什么：完整字符串、字段、数字、枚举、URL host、path 片段、模板片段、operator、对象 ID、排序字段、文件内容？
- source 是否被服务端重写、默认值覆盖、schema 限制、类型转换、白名单替换、对象绑定或权限过滤？
- source 是否需要不可获得对象 ID、secret、token、受害者交互、管理员配置或特定 feature flag？
- source 如果是对象标识符，报告是否证明“可传入”之外的“可获得”：攻击者从哪里看到、推导、枚举、搜索、导出、关系链、成员/收件人/组织选择器、历史请求或分享页获得它？
- source 如果支撑批量、全量、任意对象或广义影响，报告是否证明标识符能批量、持续、列表式、搜索式、导出式、日志式、关系链式或可推导式获得？
- source 如果来自另一个账号、租户、受害者对象或历史测试材料，是否有账号对象矩阵证明对象归属、登录态隔离、角色差异、token/cookie 未混用和清理责任？
- 如果 source 来自存储值，谁能写入，谁会触发读取，是否跨越权限或租户？

### Source 状态

```text
controlled：攻击者能稳定控制漏洞所需字段和值。
partially-controlled：只能控制部分结构或枚举，需限定 claim。
stored-taint：写入端和触发端需要一起证明。
not-controlled：服务端覆盖、可信来源或不可获得前置条件。
unresolved：报告未提供足够材料。
```

## Sink 识别

报告中出现危险函数、组件版本或响应差异，不代表 sink 成立。必须确认危险参数和执行语义。

### Sink 复核问题

- sink 是 SQL/NoSQL/LDAP/XPath、shell/process、eval/template、SSRF HTTP client、文件读写、上传/解压、XML parser、反序列化、HTML/JS 输出、auth decision、secret 使用、依赖组件还是 IaC/container 配置？
- 报告是否定位了危险 API、参数位置和执行条件？
- source 是否进入危险参数，而不是进入日志、错误消息、label、注释、安全上下文或非危险参数？
- sink 所在分支是否在当前 route、权限、配置、feature flag、插件下执行？
- sink 行为是否是官方预期功能、管理员能力、插件能力、沙箱内能力、debug 功能或范围外能力？

### Sink 状态

```text
dangerous：危险参数被可控数据污染，且执行条件明确。
wrong-parameter：命中了函数名，但污染值不在危险参数。
non-dangerous：当前上下文无安全敏感语义。
unreachable：sink 不可达或未启用。
unresolved：报告缺少代码或运行态证据。
```

## Transform / 防护检查

证据复核必须说明防护为什么不足，或为什么有效；不能只写“未过滤”“已过滤”。

### 防护复核标准

| 防护 | 有效条件 | 常见报告缺陷 |
|---|---|---|
| 参数化 | 同一 SQL/查询值位置使用绑定变量 | 动态列名、表名、排序、operator、raw 片段仍拼接 |
| allowlist | 服务端固定集合，失败阻断 | 黑名单、前缀判断、用户可写列表、只校验长度 |
| escape/encode | 与 HTML/JS/CSS/URL/header/shell/SQL 上下文匹配 | HTML escape 被拿来证明所有上下文安全 |
| normalize/canonicalize | 在权限和路径判断前执行 | realpath 后没重新校验 base，符号链接/双编码遗漏 |
| schema/type | 服务端执行且覆盖实际字段 | 客户端校验、只校验另一个字段、默认值覆盖不清楚 |
| authz/policy | sink 前执行，绑定当前主体、对象和租户 | 只在 UI、列表页或单项接口检查，批量/导出/异步遗漏 |
| framework default | 当前配置启用且调用方式未绕过 | raw API、关闭 autoescape、禁用 CSRF、跳过 middleware |
| rate limit/WAF | 稳定阻断漏洞语义 | 只挡当前 payload，换编码/结构/路径仍可达 |

### 防护裁决

```text
effective：同变量、同路径、同上下文、sink 前执行，负控证明阻断。
partial：只覆盖部分字段、分支、上下文或配置。
bypassed：强正控证明绕过。
unknown：报告没有足够证据。
not-applicable：该漏洞语义不依赖该防护。
```

`unknown` 不能支撑 technical_confirmed；`effective` 必须导致 rejected 或降级；`partial/bypassed` 需要继续补强证据。

## 路由与调用链追踪

证据复核必须把复现入口接到代码路径，或把代码路径接到可触发入口；缺一端时只能给出 candidate 或 blocked 方法性建议。

### 必查入口

- HTTP route、REST、GraphQL、WebSocket、SSE、gRPC、RPC。
- CLI command、cron、queue consumer、event listener、webhook、file import、batch job。
- CMS/plugin hook、admin ajax、template render、mobile API、serverless function。
- DAST 请求对应的真实浏览器流程。

### 调用链记录格式

```text
entry -> handler -> binder/DTO -> service -> helper -> repository/client/parser/template -> sink
file:line -> function/method -> variable/field -> branch/auth -> next hop
```

必须处理：

- 父类、接口、trait、decorator、middleware、filter、interceptor、AOP。
- 依赖注入、服务容器、注解、attribute、反射、动态路由。
- 异步生产端和消费端；存储型漏洞的写入端和读取端。
- 修复前后版本差异。

## 数据流追踪步骤

### 第 1 步：冻结复核对象

记录报告标题、报告来源、目标资产、版本、commit、运行环境、测试账号、测试对象、复核时间、原始状态和原始风险等级。不要把不同版本、不同部署、不同配置的证据混在一起。

### 第 2 步：拆分 claims

把报告拆成最小可裁决单元：

```text
Claim A：漏洞类型成立。
Claim B：攻击者条件成立。
Claim C：服务端条件成立。
Claim D：安全影响成立。
Claim E：安全模型被违反。
Claim F：风险等级成立。
Claim G：finding 是否可提交。
Claim G2：case 是否完成；只能引用机器完成门禁结果，不能由声明边界自证。
Claim H：修复已完成。
```

### 第 3 步：建立证据矩阵

```text
route: present / missing / unresolved
source: controlled / partial / not-controlled / unresolved
binding: clear / partial / missing
trace: complete / partial / broken / tool-only
sink: dangerous / wrong-parameter / non-dangerous / unresolved
transform: bypassed / partial / effective / unknown
runtime: strong / weak / missing
impact: proven / weak / missing
identifier_acquisition: proven-single / proven-bulk / manual-sample-only / missing / not-needed
account_object_matrix: complete / partial / missing / not-needed
negative_control: present / missing / not-applicable-with-reason
cleanup: done / not-needed / missing
security_model: violates / expected / unknown / 范围或官方已知拒绝（外部裁决）
four_conditions_gate: complete / partial / missing
claim_boundary_shape: allowed_claims / forbidden_to_claim_now / not_yet_proven_claims / proven_blocked_claims
higher_impact_closure: complete / partial / missing
case_completion_blockers: [] 
security_model_status: 记录官方安全模型是否已复核、是否支持当前声明、是否属于预期行为/accepted risk/范围拒绝/known issue 等；具体状态值以对应中文 schema、template 和 validator 为准。
target_scope_status: in-scope / 范围或官方已知拒绝（外部裁决） / unknown
默认配置边界说明: default-affected / non-default-only / debug-local-only / admin-config-only / unknown
official_known_status: not-known / duplicate / known-limitation / advisory-covered / unknown
预期行为说明: violates-boundary / expected / unknown
accepted risk 说明: not-accepted / accepted / unknown
外部门禁引用：提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决；本 Skill 不复制枚举、不生成状态。
forbidden_submit_reasons: []
```

### 第 4 步：找最弱证据点

结论由最弱关键证据决定：

- route 缺失：不能 technical_confirmed。
- source 不可控：rejected 或降级。
- trace partial：candidate 或 blocked。
- sink 参数错误：rejected。
- 防护 effective：rejected。
- strong positive 缺失：不能强影响 technical_confirmed。
- impact weak：只能写弱声明。
- identifier_acquisition missing：依赖标识符的越权、未授权、对象读取、对象写入、跨租户、批量或全量 claim 不能 technical_confirmed。
- identifier_acquisition manual-sample-only：只能写手工样本下可疑，或写 `candidate` / `blocked`；不得写攻击者稳定可利用。
- account_object_matrix missing：多主体、多对象、跨租户、受害者上下文、清理或回归复测相关 claim 不能 technical_confirmed。
- 负控缺失：不得高置信。
- cleanup 缺失：不得声称验证闭环完整。
- security model unknown：不能对外提交。
- security_model_status unknown：不能写可提交、默认影响、官方未公开、高危 对外提交资格。
- 外部门禁未裁决为可提交：不得把 technical_confirmed 包装成对外可提交漏洞；应写 `需要外部门禁裁决`、`candidate` 或 `blocked`。
- 四则条件缺失：不得写 `validated`、`bounty_submit_ready`、`finding_submit_ready` 或漏洞成立。
- `not_yet_proven_claims` 没有 `missing_refs`：声明边界无效，不能完成。
- `proven_blocked_claims` 没有排除证据：不能当作排除，只能转为 not_yet_proven 或 missing。
- `case_completion_blockers` 非空：不得写 case 完成。
- 默认配置边界为 non-default-only / debug-local-only / admin-config-only 时：不得写默认生产受影响。
- official_known_status 为 duplicate / known-limitation 时：除非证明新主体、新入口、新对象、新版本、新默认配置、新影响层级或官方缓解绕过，否则不得写新漏洞。
- 预期行为或 accepted risk 已成立时：只能写内部加固、文档改进、规则降噪或 `需要外部门禁裁决`；没有新边界时不得对外提交。

### 第 5 步：复核运行态证据

逐项检查 baseline、strong positive、impact escalation、negative control、cleanup。确认每个请求或操作的账号、对象、租户、marker、时间、请求 ID、响应、日志和副作用。若 claim 依赖 ID、URI、token、object key 或物理表名，还要复核攻击者获取标识符的请求链；若 claim 依赖多主体，还要复核账号对象矩阵与 token/cookie 隔离。

### 第 6 步：复核最高危害

判断报告是否停在弱证明。如果能在授权环境内安全推进，应要求补证；如果不能推进，必须写清停止原因。

### 第 7 步：写状态裁决

```text
Status：本 Skill 只给 technical_status 方法性建议；提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决。
Reason:
Evidence strongest point:
Evidence weakest point:
Official Security Model:
对外提交资格 Status:
对外提交资格 Blockers:
allowed_claims:
forbidden_to_claim_now:
not_yet_proven_claims:
proven_blocked_claims:
Missing Evidence:
blocks_finding_submit:
blocks_case_completion:
Next action:
```

## 必检证据点

### 报告结构证据

- 标题是否说明漏洞类型、位置和影响。
- 目标资产、位置、角色、版本、配置是否明确。
- 复现步骤是否可按顺序执行。
- 预期结果和实际结果是否区分。
- 影响说明是否绑定证据，而不是泛泛描述。
- 修复建议是否指向根因。

### 入口证据

- method/path/handler 或 message/topic/command。
- route 注册、profile/feature flag、插件启用状态。
- middleware/filter/interceptor/guard/policy 顺序。
- 浏览器流程或 API 调用如何到达该入口。

### Source 证据

- 字段名、来源、绑定位置。
- 可控主体、权限、租户、对象。
- 控制粒度和前置条件。
- 存储型污染的写入端和触发端。

### 标识符获取证据

- `EVID_IDENTIFIER_ACQUISITION`：列出漏洞成立所需的每个 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、资源 URI、对象 key、物理表名或其他标识符。
- 对每个标识符写清来源：列表响应、详情响应、搜索、导出、日志泄露、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列、批量接口、受害者交互、管理员手工提供、历史附件、截图、报告笔记或未知。
- 对每个标识符写清攻击者可达性：攻击者自己能否在同权限下获得，是否需要 victim 主动分享，是否需要管理员视角，是否只能在测试过程中手工拿到。
- 对每个标识符写清可获得规模：单对象、同类多对象、批量、持续、可枚举、可搜索、可导出、可推导、不可获得。
- 报告写“批量”“全量”“所有用户”“所有租户”“任意对象”“任意文件”时，必须有能支撑该规模的标识符获取证据；只有一个样本 ID 时，只能支撑该样本或同一获取路径下的对象。

### 账号对象矩阵证据

- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 每个账号至少记录用途、用户名或邮箱、账号对象矩阵必要事实、主体 ID、tenant/workspace、role/scope、token/cookie 引用、对象归属、适用步骤和清理责任。
- 多主体 claim 必须证明 token/cookie 没有混用，attacker 不是 owner，victim 对象确实属于 victim，control 对象用于证明正常权限路径。
- 账号矩阵缺账号对象矩阵必要事实时，内部复核不能重放；报告阶段按唯一模板渲染可复现所需账号对象矩阵事实，第三方或生产完整密码、token、cookie、session 或可复用真实凭据不在不受控渠道扩散。

### Trace 证据

- 每一跳 file:line、变量名、函数、分支、异常、早退、权限判断。
- DTO/Model/Serializer/Mapper/ORM/队列/缓存/事件/AOP/DI 的字段映射。
- 工具 trace 与人工 trace 的差异。

### Sink 证据

- 危险 API/函数/组件/配置。
- 危险参数位置。
- 执行条件。
- sink 所在分支可达性。

### 防护证据

- sanitizer/validator/escape/allowlist/parameterization/authz 是否同变量、同路径、同上下文。
- 框架默认防护是否启用，是否被 raw API 绕过。
- 官方缓解是否生效或被绕过。

### 官方安全模型与对外提交资格 证据

- `EVID_OFFICIAL_SECURITY_MODEL`：准备写 technical_confirmed、对外提交资格、对外提交、高危/严重、默认配置受影响、未认证、低权限、跨用户、跨租户、沙箱逃逸、有效凭据泄露、内网访问或批量越权时，必须证明官方 SECURITY、安全策略、scope、API 文档、权限模型、对象模型、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决）、duplicate 和提交材料质量规则已经裁决。
- `security_model_status`：reviewed / unknown / 预期行为拒绝（外部裁决） / accepted-risk / 范围或官方已知拒绝（外部裁决） / hardening-only / known-issue / reviewed_supports_current_claim。
- `target_scope_status`：in-scope / 范围或官方已知拒绝（外部裁决） / unknown；范围 unknown 时只能 candidate 或 blocked，不得对外提交。
- `默认配置边界说明`：default-affected / non-default-only / debug-local-only / admin-config-only / unknown；非默认、debug、本地或管理员配置不能外推成默认生产影响。
- `official_known_status`：not-known / duplicate / known-limitation / advisory-covered / unknown；重复或已知限制没有新边界时应降级或拒绝。
- `预期行为 / accepted risk 说明`：确认当前行为是否官方预期、受信任主体正常能力、accepted risk 或 hardening only。
- 提交资格由外部门禁单独裁决是否可提交；不能用 technical_confirmed 替代。
- `forbidden_submit_reasons`：列出缺官方资料、范围不明、默认配置不明、已知风险、预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、重复、非账号类敏感材料展示边界不足、账号矩阵不足或 ID 获取链不足。

### 动态证据

- baseline、strong positive、impact escalation、negative control、retest。
- 请求、响应、日志、审计日志、数据库/缓存/队列/文件/OOB/浏览器/命令输出。
- 清理/恢复或无副作用证明。

### 声明边界证据

- `allowed_claims`：可以写的最强事实。
- forbidden_to_claim_now：当前不能写的更强事实；不代表已排除。
- not_yet_proven_claims：未证明但仍可能成立，必须回链 Missing Evidence。
- proven_blocked_claims：已被证据排除或阻断，必须回链排除证据。
- Missing Evidence：升级所需证据。
- Stop Reason：停止追踪最高危害的具体原因。

## 动态验证触发条件

### 必须动态验证才能 technical_confirmed

- 越权、IDOR、权限绕过、跨租户、对象级授权缺失。
- SSRF、开放重定向、webhook、URL preview、服务端请求。
- SQL/NoSQL/LDAP/XPath 注入。
- 文件读取、文件写入、上传、解压、路径穿越、对象存储 key 越界。
- 命令执行、代码执行、模板表达式、反序列化、XXE。
- XSS、DOM XSS、存储型 XSS、响应头注入。
- CSRF 和任何状态改变类漏洞。
- SCA 可达漏洞和供应链组件触发。
- Secret 有效性、权限范围和暴露面。
- 资源消耗和可用性影响。

对依赖标识符的报告，动态验证至少包含三组动作：

1. attacker 用自身可达入口获得目标标识符，或证明无法从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口获得。
2. attacker 使用该标识符触发越权读、写、删、导出、绑定、复制、签名、状态改变或其他影响。
3. control 账号、自己对象、他人对象、无权限主体、过期/无效 token 或不同租户负控证明差异来自授权缺失，而不是对象公开、正常共享、缓存、登录态混用或测试数据污染。

### 可以先 candidate

- 静态证据较完整但缺强正控、负控、运行态或安全模型。
- 报告只证明低层现象，但值得继续补证。
- 代码 trace 有缺口，但 source/sink 方向合理。
- 修复建议可能正确，但根因未完全证明。
- 影响需要双账号、双对象、日志或 OOB 才能确认。
- 只有“已知 ID 后可利用”、手工样本 ID、截图 ID、历史附件 ID、报告笔记 ID 或管理员视角 ID，但尚未证明攻击者如何获得。
- 单对象样本成立，但批量、全量、任意对象、所有用户、所有租户或广义声明缺可获得规模证据。
- 多账号步骤存在，但账号矩阵缺账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 隔离或清理责任。

### 必须 blocked

- 必须运行环境、账号、对象、租户、日志、浏览器、队列、构建产物、feature flag、license、插件或清理能力才能判断。
- 必须运行态确认标识符是否能从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口获得。
- 必须运行态确认账号矩阵、对象归属、tenant/workspace、role/scope、token/cookie 隔离和清理能力。
- 必须复测才能确认 fixed/resolved。
- 必须官方 scope、安全模型或 known issue 去重才能对外提交。

### rejected

只有明确否定证据才 rejected：

- 入口不可达或未启用。
- source 不可控。
- trace 断裂且已证伪。
- sink 参数错误或无安全语义。
- 防护 effective。
- 影响不存在或仅普通 bug。
- 版本未加载、组件不可达、secret 无效且不可获得。
- 代码、接口和运行态均证明攻击者无法获得必要对象标识符，且不存在列表、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、可预测或可推导路径。
- 多主体报告经复核证明其实使用同一账号、同一 token、同一对象、对象公开或 owner/victim 边界不成立。
- 完全重复已知问题且没有新边界。
- 范围外且只讨论提交状态。

rejected 必须写证据，不得只写“误报”。

## 授权实验模式下的强验证方法

强验证的目的不是“打得更猛”，而是把弱现象升级为可复核的安全影响。只要环境属于自有、明确授权、隔离、可回滚、可清理范围，就应优先设计能证明漏洞语义的验证，而不是停在无害 marker、单个 callback、单次错误栈或工具命中。

### 强验证前置门槛

执行强验证前必须同时满足：

- 授权范围清楚：资产、账号、角色、租户、对象、网络、时间窗口和允许动作明确。
- 环境可控：本地、靶场、CTF、隔离预发、测试租户、测试数据库或可重置容器。
- 观察点存在：响应、日志、审计日志、数据库、缓存、文件、队列、OOB、浏览器、命令输出至少有一个可复核观察点。
- 清理能力存在：能删除测试数据、回滚快照、重置容器、撤销测试凭据或证明无持久副作用。
- 数据边界清楚：只使用测试账号、测试对象、测试文件、测试 secret、测试网络端点，不读取真实用户数据或真实第三方凭据。

任一前置门槛缺失时，不要把强影响写成 technical_confirmed；应标记 `blocked` 或 `candidate`，并写清缺失项。

### 不同漏洞语义的强验证目标

| 漏洞语义 | 弱证据 | 授权实验中应追的强证据 | 不能越过的边界 |
|---|---|---|---|
| SSRF | DNS/HTTP callback | 证明服务端请求可控协议、host、端口、路径；在受控内网模拟服务上证明响应差异或受限资源访问 | 不扫真实内网，不打云 metadata 真实凭据 |
| SQL/NoSQL 注入 | 错误栈或时间抖动 | 布尔差异、时间差异、受控测试表/集合读取、测试行写入、权限范围证明 | 不读取生产数据，不破坏真实表 |
| 命令执行 | marker 回显 | 受控命令输出、当前用户/目录/环境差异、受控回连、可清理文件写入 | 不持久化后门，不访问真实敏感文件 |
| 文件读取 | 路径拼接命中 | 读取测试文件、容器内无敏感标记文件、路径规范化绕过证明 | 不读真实凭据、真实用户文件 |
| 文件写入/上传/解压 | 上传成功 | 写入受控目录、访问/执行边界、覆盖/穿越/链接场景、清理记录 | 不覆盖真实文件，不放不可清理可执行物 |
| XSS/DOM XSS | 字符串反射 | 浏览器执行上下文、同源能力、可读写测试 DOM/测试 cookie 限制、存储触发链 | 不窃取真实 cookie，不钓鱼真实用户 |
| IDOR/越权 | 换 ID 返回 200、已知 ID 后成功 | 标识符获取链、账号对象矩阵、双账号、双对象、双租户 A/B 对照，证明越过对象级授权并读/写测试对象；批量 claim 还要证明标识符可批量获得 | 不访问真实用户对象，不把手工样本 ID 当攻击者能力 |
| CSRF | 表单可提交 | 受害测试账号在无交互或弱交互下发生状态变化，验证 token/Origin/SameSite 旁路 | 不影响真实账号状态 |
| Secret | 正则命中 | 暴露面、可获得性、有效性、权限范围、轮换状态、最小无害 API 调用 | 不输出完整真实 secret，不滥用第三方服务 |
| SCA | 版本命中 | 组件实际加载、漏洞功能可达、受控 PoC 触发、缓解配置无效或缺失 | 不对第三方服务做真实利用 |
| 资源消耗 | 单次慢响应 | 受控并发/大小/深度曲线、阈值、恢复时间、限流效果 | 不压垮共享环境 |

### 强验证记录格式

```text
Strong validation:
  scope:
  environment_snapshot:
  accounts_and_objects:
  identifier_acquisition:
  account_object_matrix:
  baseline:
  strong_positive:
  impact_observation:
  negative_control:
  logs_or_side_effects:
  cleanup_or_reset:
  remaining_limits:
```

如果强验证没有成功，不要直接 rejected。先判断失败原因：路径不对、payload 不匹配、防护有效、权限不足、观察点缺失、环境不一致、触发条件不完整，还是漏洞语义被证伪。只有最后一种才能 rejected。

## 最高危害追踪

最高危害追踪用于防止报告停在低价值现象。它要求复核者在授权范围内继续问：当前证据能不能从“可疑现象”推进到更明确的 CIA 影响、安全边界破坏或可修复根因？

### 升级顺序

按下面顺序推进，直到触达授权边界、环境边界或证据边界：

1. **可达性**：入口是否真实可达，是否默认暴露，是否需要特殊配置。
2. **可控性**：攻击者能否控制关键字段、对象、URL、模板、查询、文件名、命令参数。
3. **语义命中**：污染值是否进入真正危险参数，而不是日志、错误页、无害 label。
4. **防护绕过**：是否绕过框架默认、参数化、编码、白名单、对象级授权、CSRF、出网策略。
5. **弱影响**：错误差异、callback、反射、状态码差异、时间差异。
6. **强影响**：测试数据读取、测试对象写入、跨测试账号/租户访问、受控文件读写、受控命令结果、受控浏览器执行、受控组件触发。
7. **影响范围**：匿名/登录用户/低权限成员/管理员；单对象/批量对象；单租户/跨租户；单服务/跨网络；默认配置/特定配置。
8. **修复优先级**：根据最高已证明影响和限制因素给出风险等级，不照抄工具 severity。

### 必须降级的低层证明

- callback-only SSRF：只能说服务端请求了受控端点，不能说内网敏感信息泄露。
- marker-only RCE：只能说输入影响响应或执行链可疑，不能说命令执行，除非证明执行语义。
- error-only SQLi：只能说查询构造可疑，不能说数据读取。
- reflect-only XSS：只能说反射，不能说浏览器执行。
- status-only IDOR：只能说 ID 影响响应，不能说越权。
- known-ID-only IDOR：只能说“在手工样本 ID 下存在可疑对象访问/状态改变”，不能说攻击者稳定越权、批量越权或高价值 technical_confirmed。
- single-ID extrapolation：只能支撑单对象或同一获取路径下的对象，不能外推到任意用户、任意租户、全量对象或批量导出。
- version-only SCA：只能说版本命中，不能说可利用。
- regex-only secret：只能说疑似凭据，不能说有效凭据泄露。

### 允许停止的原因

停止追踪必须具体，不能写“风险较低”“payload 太强”“暂不验证”。可接受原因包括：

- 越出授权资产、账号、租户、网络、时间窗口或漏洞类型范围。
- 缺少测试账号、测试对象、测试数据、日志、OOB、浏览器或队列消费者。
- 环境不可重置、不可清理，继续验证可能造成不可逆副作用。
- 需要读取真实用户数据、真实第三方凭据或真实生产秘密。
- 官方安全模型说明该能力是预期功能，且没有越界证据。
- 防护已被负控证明有效，继续升级没有技术依据。
- 当前版本、配置或组件不可达，无法触发漏洞功能。
- 依赖标识符的 claim 已穷尽列表、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、可预测和可推导路径，仍证明攻击者不可获得必要标识符。

### 不合格停止原因

以下说法不能作为停止理由：

- “已经有 marker，所以 technical_confirmed。”
- “工具报 High，所以不用继续证明。”
- “callback 到了，所以一定能读内网。”
- “payload 太激进，所以不做。”
- “弱 payload 失败，所以不存在漏洞。”
- “agent 认为可利用，所以写 technical_confirmed。”
- “已知 ID 后可以用，所以就是高危 technical_confirmed。”
- “只测了一个样本 ID，但可以类推所有用户或所有租户。”

## 负控设计

负控用于回答“为什么这个现象是漏洞导致的，而不是正常功能、随机噪声、缓存、权限本来允许或测试污染”。每个 technical_confirmed claim 至少需要一个与其语义匹配的负控；高危 claim 应尽量有多个互补负控。

### 负控类型

| 负控类型 | 目的 | 示例 |
|---|---|---|
| 输入负控 | 证明只有恶意结构触发 | 合法值、转义值、不可解析值、白名单外值 |
| 身份负控 | 证明权限边界被越过 | 同请求分别用 owner、non-owner、匿名、低权限账号 |
| 对象负控 | 证明不是对象公开 | A 账号对象、B 账号对象、不可存在对象、同租户/跨租户对象 |
| 标识符获取负控 | 证明 ID 不是复核人手工样本或管理员视角样本 | attacker 只用自身入口获取 ID；手工样本移除后验证是否仍可获得 |
| 批量标识符负控 | 证明批量/全量/任意对象声明是否有可获得规模 | 单个样本、短列表、搜索、导出、关系链、可预测序列分别裁决 |
| token/cookie 隔离负控 | 排除多账号登录态混用 | A/B token 分离、过期 token、无效 token、匿名、不同租户 cookie 对照 |
| 路径负控 | 证明不是缓存或默认响应 | 改 path、method、content-type、route、feature flag |
| 防护负控 | 证明防护有效或被绕过 | 参数化版本失败、raw 版本成功；token 正确/缺失对照 |
| 环境负控 | 证明不是版本/配置差异 | 修复前后、组件启用/禁用、测试配置/默认配置 |
| 副作用负控 | 证明状态变化来自漏洞 | 操作前快照、操作后差异、清理后复查 |
| OOB 负控 | 证明请求来自目标服务端 | 随机子域、请求 ID、时间戳、源 IP、错误 host 对照 |

### 负控失败时如何裁决

- 负控证明所有用户都能访问：不要写越权，应改写为公开数据或正常功能。
- 负控证明 attacker 无法获得必要 ID：不要写稳定越权；若代码、接口和运行态都排除获取路径，可 rejected，否则降级为 candidate / blocked。
- 负控证明只有一个手工样本 ID：只允许样本级或同获取路径下的窄 claim，不允许批量、全量、任意对象或所有租户外推。
- 负控证明 token/cookie 混用：多主体 claim 无效，必须重做账号矩阵或 rejected。
- 负控证明防护稳定阻断：rejected 或降级为“防护存在，未证明绕过”。
- 负控结果不稳定：blocked，要求更多样本、日志或隔离环境。
- 负控缺失但强正控存在：可以 candidate；若要 technical_confirmed，必须解释等价证据为何足够。
- 负控设计错误：不能用错误负控削弱漏洞，也不能用错误负控支撑漏洞。

### 负控记录格式

```text
Negative control:
  hypothesis_to_exclude:
  control_input_or_account:
  expected_result:
  actual_result:
  evidence:
  interpretation:
```

## technical_status 方法性判定边界

### technical_confirmed

只有同时满足以下条件，才能写 technical_confirmed：

- route 可达，版本/配置/feature flag 与目标一致。
- source 由攻击者在所需权限和对象范围内控制。
- trace 从 source 到 sink 闭合，关键分支、绑定、转换和权限判断可解释。
- sink 危险参数被污染，且执行语义与漏洞类型匹配。
- transform、防护或安全机制被证明缺失、不足或可绕过。
- 运行态强正控证明真实安全影响，而不只是弱现象。
- 至少一个语义匹配的负控排除误报。
- 如果 claim 依赖对象标识符，`EVID_IDENTIFIER_ACQUISITION` 证明攻击者获得路径，且声明范围不超过可获得规模。
- 如果 claim 依赖多主体、多对象、跨租户、跨角色、受害者对象或清理动作，`EVID_ACCOUNT_OBJECT_MATRIX` 完整证明账号用途、账号对象矩阵必要事实、主体 ID、租户/工作区、角色、对象归属、token/cookie 隔离和清理责任。
- `EVID_OFFICIAL_SECURITY_MODEL` 已裁决，官方安全模型不把该行为定义为预期功能、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate。
- 如果结论要进入提交总入口报告、提交、评级或修复优先级，本 Skill 只提示需要外部门禁裁决；是否可主提交由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决。
- 最高危害已追到授权范围内合理上限，停止原因具体。
- 未证明更高影响已进入 `not_yet_proven_claims` 与 `higher_impact_closures[]`，或已在 `proven_blocked_claims` 中提供排除证据。
- 清理/恢复完成，或证明验证无持久副作用。
- `allowed_claims` 与证据一致；更强但未证明的说法已进入 `forbidden_to_claim_now` 与 `not_yet_proven_claims`，或在 `proven_blocked_claims` 中具备排除证据。

### candidate

适用于方向合理但证据不够写 technical_confirmed 的情况：

- source/sink/trace 中有部分证据，但运行态、负控、官方安全模型或 对外提交裁决不足。
- 静态路径合理，但缺账号、对象、日志、OOB、浏览器或双主体对照。
- 强正控只证明弱影响，尚未证明数据、权限、状态、执行或跨边界影响。
- 防护判断为 unknown 或 partial，仍需补证。
- 只有“已知 ID 后可利用”、手工样本 ID、截图 ID、历史附件 ID、报告笔记 ID 或管理员视角 ID，但尚未证明攻击者如何获得。
- 单对象样本成立，但批量、全量、任意对象、所有用户、所有租户或广义声明缺可获得规模证据。
- 多账号步骤存在，但账号矩阵缺账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 隔离或清理责任。
- 官方资料、scope、默认配置、known issue、expected behavior、accepted risk 或 duplicate 尚未读完，不能判断是否 对外提交资格。
- 报告可进入继续审计或补证队列，但不能提交为 technical_confirmed。

candidate 必须附 `Missing Evidence`，否则会退化成空泛怀疑。

### blocked

适用于必须依赖运行态材料才能裁决的情况：

- 需要真实路由、构建产物、profile、feature flag、插件、队列消费者或部署配置。
- 需要双账号、双租户、测试对象、测试数据、OOB、浏览器、日志或清理能力。
- 需要运行态确认标识符是否能从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口获得。
- 需要运行态确认账号矩阵、对象归属、tenant/workspace、role/scope、token/cookie 隔离和清理能力。
- 需要复测修复是否生效。
- 需要官方 scope、安全模型、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 或重复报告材料。

blocked 不是失败结论；它是“当前静态/文本材料不足以裁决”的诚实边界。

### rejected

rejected 必须有明确反证：

- 入口不可达，或目标版本/配置未启用。
- source 不受攻击者控制，或需要不可获得的前置条件。
- trace 被证伪，污染值未到达 sink。
- 命中的是错误参数、非危险上下文或官方预期功能。
- 防护在同变量、同路径、同上下文、sink 前有效。
- 动态强正控和负控共同证明影响不存在。
- 组件未加载、漏洞功能不可达、secret 无效且不可获得。
- 代码、接口和运行态均证明攻击者无法获得必要对象标识符，且不存在列表、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、可预测或可推导路径。
- 多主体报告经复核证明其实使用同一账号、同一 token、同一对象、对象公开或 owner/victim 边界不成立。
- 范围外、重复、accepted risk 或 expected behavior 已被材料证明。
- 官方安全模型明确这是 expected behavior、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate，且当前证据没有新主体、新入口、新对象、新版本、新默认配置、新边界或官方缓解绕过。
- 官方默认配置、版本或部署方式证明当前强 claim 不成立，例如只在 debug/local/危险开关/管理员配置下出现，却被报告写成默认生产影响。

rejected 报告仍需写清“为什么无效”，不要只写“误报”。

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证；完成通过必须引用机器完成门禁结果。
- 声明边界必须写入 `evidence/声明边界.json` 的 `allowed_claims`、`forbidden_to_claim_now`、`not_yet_proven_claims`、`proven_blocked_claims`，不得把四类混成一个旧式禁止声明列表。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

修复建议必须对准根因，不要只写口号。

- SQL/NoSQL/LDAP/XPath：参数化、结构化 builder、动态字段 allowlist、禁止 raw fragment。
- RCE/CMD：不用 shell 拼接，固定命令，参数数组，最小权限，隔离执行环境。
- SSRF：协议/域名/端口 allowlist，解析后 IP 校验，重定向后重校验，metadata 阻断，出网隔离。
- XSS/SSTI：上下文编码，避免 raw/safe，模板自动转义，CSP 补充，浏览器回归。
- 文件/上传/归档：canonicalize 后 base 约束，拒绝链接和特殊文件，随机文件名，不可执行目录。
- Auth/IDOR：服务端对象级授权，tenant 绑定，批量逐项校验，不信任前端 owner/role。
- CSRF：状态变更 token，Origin/Referer 辅助，覆盖 JSON/multipart/method override。
- Secret：轮换、吊销、清理历史、降低权限、迁移密钥管理、日志脱敏。
- SCA：升级安全版本；无法升级时关闭漏洞功能、加配置缓解、限制入口，并确认运行包实际更新。
- IaC/container：最小权限、去特权容器、限制 hostPath/capability、网络隔离、认证/TLS。
- 标识符暴露：列表、搜索、导出、分享页、日志、客户端状态和批量接口同样要做对象级授权；不可预测 ID 只能降低枚举概率，不能替代服务端授权。
- `需要外部门禁裁决`：不要写对外漏洞修复结论；先补官方材料、补 scope/default config/known issue 去重、收缩声明、转内部加固、补文档/警告/审计日志、优化扫描规则或登记 accepted risk。只有证明新主体、新入口、新对象、新默认配置、新版本、更高影响或官方缓解绕过后，才允许重新交由外部门禁评估对外提交资格。
- expected behavior / accepted risk / 范围或官方已知拒绝（外部裁决）：修复建议应写成加固、文档、默认安全配置、审计日志、二次确认、最小权限、检测规则优化或内部风险登记；不得要求删除正常功能，也不得把范围外问题包装成漏洞修复。

修复后必须重放 strong positive 和 negative control；扫描器不再报只能作为辅助，不能替代复测。

## 禁止事项

- 禁止 sink-only technical_confirmed。
- 禁止 source-only technical_confirmed。
- 禁止 scanner-only technical_confirmed。
- 禁止 external-tool-only technical_confirmed。
- 禁止 regex-only technical_confirmed。
- 禁止没有 trace 就 technical_confirmed。
- 禁止 trace_status=PARTIAL/UNRESOLVED 仍写 technical_confirmed。
- 禁止没有负控就写高置信。
- 禁止只看 200 响应。
- 禁止把框架默认安全或默认不安全当证据。
- 禁止把 sanitizer 名称当防护结论；必须看语义和上下文。
- 禁止把不可解析的动态调用强行补全为证据。
- 禁止把 technical_confirmed 直接写成对外可提交。
- 禁止把 finding_submit_ready、bounty_submit_ready 或声明边界通过写成 case_audit_complete。
- 禁止用 `forbidden_to_claim_now` 关闭未验证方向、替代缺失证据、替代 `higher_impact_closures[]` 或替代高危面覆盖。
- 禁止 `not_yet_proven_claims` 没有 missing_refs。
- 禁止 `proven_blocked_claims` 没有排除证据。
- 禁止四则条件缺失时写 validated、bounty_submit_ready、finding_submit_ready 或漏洞成立。
- 禁止在官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 或 duplicate 仍为 unknown 时写对外可提交、高危默认影响或官方未公开。
- 禁止把 `需要外部门禁裁决` 写成“已确认可提交漏洞”。
- 禁止把真实技术现象因为不 对外提交资格 就简单写成 rejected；应区分内部修复、规则降噪、加固建议和对外提交状态。
- 禁止把 expected behavior、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate 包装成新漏洞，除非证明新主体、新入口、新对象、新版本、新默认配置、更高影响或官方缓解绕过。
- 禁止把非默认 debug/local/危险开关/管理员配置影响写成默认生产影响，除非有官方默认值或全新安装证据。
- 禁止 callback-only SSRF 写成内网高危 technical_confirmed。
- 禁止 marker-only RCE 写成命令执行 technical_confirmed。
- 禁止 error-only SQLi 写成数据读取 technical_confirmed。
- 禁止 reflect-only XSS 写成浏览器执行 technical_confirmed。
- 禁止 version-only SCA 写成组件漏洞可达 technical_confirmed。
- 禁止 status-only IDOR 写成越权 technical_confirmed。
- 禁止 known-ID-only IDOR 写成高价值 technical_confirmed。
- 禁止把“已知 ID 后可利用”“替换 ID 返回 200”“拿到另一个用户对象 ID 后成功”写成攻击者稳定可利用，除非证明攻击者如何获得该 ID。
- 禁止把管理员手工给出的 ID、报告作者笔记里的 ID、聊天上下文里的 ID、历史附件里的 ID、截图里的 ID 当成攻击者可获得路径。
- 禁止用单个样本 ID 外推批量、全量、任意对象、所有用户、所有租户、所有工作区或广义影响。
- 禁止账号矩阵缺账号对象矩阵必要事实、主体 ID、租户/工作区、角色、对象归属、token/cookie 引用和清理责任时写多主体 technical_confirmed。
- 禁止弱 payload 失败直接 rejected。
- 禁止为了凑数量写低价值漏洞。
- 禁止把项目运行、部署、恢复、调度、监控内容混进漏洞审计 skill。
- 禁止把个人机器环境信息、不可公开编号、临时对话过程或专用平台词写进通用 Skill 正文。
- 禁止越出授权范围、测试第三方真实系统、读取真实生产用户数据、泄露真实凭据或执行不可清理验证。

## 自检清单

每项回答 `是 / 否 / 不适用`：

### Source

- [ ] 是否识别 query/path/body/header/cookie/JSON/XML/multipart？
- [ ] 是否识别 GraphQL/WebSocket/CLI/webhook/queue/cron/file import？
- [ ] 是否识别 session/JWT/OAuth claim 和 framework request object？
- [ ] 是否识别 stored taint：数据库、缓存、文件、对象存储？
- [ ] 是否证明 source 的控制主体、权限边界和控制粒度？
- [ ] 客户端隐藏参数、签名头、硬编码 key 是否证明后端实际信任？
- [ ] 如果 source 是对象标识符，是否区分手工样本 ID、管理员视角 ID、攻击者可获得 ID 和可批量获得 ID？
- [ ] 批量、全量、任意对象、全用户、全租户或广义声明是否有批量获取标识符的证据？
- [ ] 多主体、多对象或跨租户验证是否有账号矩阵、账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 隔离和清理责任？

### Trace

- [ ] 是否从入口追到 handler/controller？
- [ ] 是否从 handler 追到 service/repository/mapper/model/helper/client？
- [ ] 是否处理父类、接口、trait、helper、middleware、decorator、依赖注入、注解/attribute、AOP、反射？
- [ ] 是否处理事件、队列、定时任务、异步消费端？
- [ ] 是否记录每一跳 `file:line`、变量名、输入/输出、分支？
- [ ] 是否给出 trace_status：COMPLETE/PARTIAL/UNRESOLVED？

### Transform / 防护

- [ ] 是否区分 transform 与 sanitizer？
- [ ] 是否确认防护作用在同一变量、同一分支、同一上下文？
- [ ] 是否确认参数化覆盖全部动态片段？
- [ ] 是否确认白名单在规范化后执行且允许值无危险语义？
- [ ] 是否确认 escape 匹配输出上下文？
- [ ] 是否确认权限检查在 sink 前执行且对象级/租户级覆盖？
- [ ] 若强正控失败，是否解释是防护有效还是 payload/路径/权限/观察点不足？

### Sink

- [ ] 是否定位 sink API、危险参数位置和执行条件？
- [ ] 是否证明 tainted 变量进入危险参数，而不是非危险参数？
- [ ] 是否覆盖 SQL/NoSQL/CMD/FILE/UPLOAD/ARCHIVE/XXE/DESER/SSRF/XSS/AUTH/CSRF/REDIR/HEADER/cache/queue 等相关 sink？
- [ ] 是否判断 sink 所在分支可执行？
- [ ] 是否引用或等价覆盖相关 EVID_* 证据点？

### 动态验证与负控

- [ ] 是否写出 baseline、强正控、负控请求？
- [ ] 是否追踪到授权测试范围内合理最高影响？
- [ ] 是否记录日志观察点和副作用观察点？
- [ ] 是否为 technical_confirmed 提供至少一个负控？
- [ ] 是否有清理/恢复证据或说明无副作用？
- [ ] 不能动态验证时是否降级并说明原因？
- [ ] 越权/未授权/IDOR 是否证明标识符获取链，而不是只改一个已知 ID 看响应？
- [ ] 依赖对象 ID、分享 token、lookup handle、URI、object key 或物理表名的验证是否有攻击者获取路径？
- [ ] 批量/广义影响是否证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得？

### 判定与报告

- [ ] 是否给出 finding 状态：technical_confirmed/需要外部门禁裁决/candidate/blocked/rejected？
- [ ] 是否区分 technical_confirmed 和对外提交资格？
- [ ] 如果要写对外可提交，是否具备 `EVID_OFFICIAL_SECURITY_MODEL`？
- [ ] 是否裁决 scope、默认配置、版本、known issue、duplicate、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和提交材料质量要求？
- [ ] security_model_status 为 unknown 时，是否降级为 candidate、blocked 或 官方已知排除（外部裁决），而不是写可提交漏洞？
- [ ] 外部门禁未裁决为可提交 时，是否写清 forbidden_submit_reasons 和 forbidden external claims？
- [ ] 是否避免把 expected behavior、受信任主体能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate 包装成新漏洞？
- [ ] 是否说明 candidate/blocked 缺哪些证据？
- [ ] 是否说明 rejected 的排除证据？
- [ ] 是否避免 scanner-only、external-tool-only、sink-only、regex-only、无负控 technical_confirmed？
- [ ] 依赖 ID 的 technical_confirmed 是否同时满足 `EVID_IDENTIFIER_ACQUISITION`？
- [ ] 多主体 technical_confirmed 是否同时满足 `EVID_ACCOUNT_OBJECT_MATRIX`？
- [ ] 是否把 known-ID-only、手工样本 ID、截图 ID、历史附件 ID 或报告笔记 ID 降级？
- [ ] 是否避免单对象样本外推成批量、全量、任意对象、全租户或全用户？
- [ ] 是否写清 `allowed_claims`、`forbidden_to_claim_now`、`not_yet_proven_claims`、`proven_blocked_claims`？
- [ ] `forbidden_to_claim_now` 是否没有被当作排除证据？
- [ ] `not_yet_proven_claims` 是否都有 `missing_refs`？
- [ ] `proven_blocked_claims` 是否都有排除证据？
- [ ] 是否没有把 finding 可提交或声明边界通过写成 case 完成？
- [ ] 是否去除个人机器环境信息、不可公开编号、临时对话过程和专用平台词？

检验句：**报告写得像 technical_confirmed，不等于证据达到 technical_confirmed；technical_confirmed，也不等于对外提交资格。只有当每个强 claim 都能被 route、source、trace、sink、impact、negative control、cleanup、security model 和 对外提交裁决支撑时，才允许写对外提交资格；否则必须降级、写 需要外部门禁裁决 或补证。**
