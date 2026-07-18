---
name: scanner-result-triage
description: Use when reviewing SAST, DAST, SCA, secret, IaC, container, SARIF, CodeQL, Semgrep, or commercial scanner findings before accepting, downgrading, rejecting, deduplicating, converting them into manual audit tasks, or deciding whether a scanner-derived claim is 对外提交资格.
---

# 扫描器结果复核

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

这个 Skill 用来把扫描器输出转成可复核的人工审计结论。扫描器可以帮助定位代码、请求、依赖、secret、配置、路径、数据流、规则解释和重复告警，但它不能替代人工完成：入口可达性、source 可控性、trace 闭合、防护有效性、真实影响、强正控、负控、清理恢复、官方安全模型、外部门禁引用和声明边界裁决。

调用时先写一行目标句：

```text
我要复核：{扫描器 finding / SARIF result / DAST 请求 / SCA 版本命中 / secret 命中 / IaC 配置告警} 是否能转成 technical_confirmed、candidate、blocked 或 rejected，并给出 evidence gate、官方安全模型、外部门禁引用、强验证、负控、去重、报告声明边界和修复建议。
```

典型触发场景：

- 收到 SAST、DAST、IAST、SCA、secret scanning、IaC、container、license、dependency、CodeQL、Semgrep、SARIF、Nuclei、ZAP、Burp Scanner 或商业扫描平台结果。
- 工具标注了 high、critical、reachable、validated、technical_confirmed、fixed、ignored、removed、suppressed、false positive，但需要人工确认语义。
- 扫描器只给出 sink、source、dataflow path、dependency path、secret 字符串、HTTP 200、callback、错误栈、版本号或配置项。
- 多个工具对同一漏洞重复命中，需要按真实攻击路径去重、合并证据和统一修复建议。
- 报告或其他模型/工具 根据扫描器输出声称“已确认漏洞”，需要排除 scanner-only、external-tool-only、sink-only、version-only、regex-only、callback-only 等弱结论。
- 在自有 Docker、CTF、靶场、本地、隔离预发或其他明确授权、可重置、可清理环境中，需要把扫描器弱线索推进到强正控、最高危害、负控和清理闭环。

每次使用至少输出：

```text
Finding ID：
扫描器原始状态：
人工复核状态：本 Skill 只给 technical_status 方法性建议；提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决。
工具可信部分：
工具误报或过度声明部分：
Route / Source / Trace / Sink / Transform：
标识符获取：{需要哪些 ID / handle / token / URI / object key；工具是否只是手工样本；攻击者如何获得；单对象/批量/不可获得}
账号矩阵：{attacker / owner / victim / control / cleanup；内部复核记录账号对象矩阵必要事实、主体 ID、租户/工作区、角色、对象归属、token/cookie 引用}
官方安全模型：{SECURITY / scope / 默认配置 / 权限模型 / 对象模型 / known issue / expected behavior / accepted risk / 范围或官方已知拒绝（外部裁决）}
外部门禁引用：提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决；本 Skill 不复制枚举、不生成状态。
强正控：
负控：
影响证明：
清理/恢复：
Allowed Claims：
Forbidden Claims：
下一步：补运行态 / 写报告 / 合并重复 / 调整规则 / 修复代码 / 拒绝
```

本 Skill 不处理扫描器平台部署、CI 调度、报表运营、漏洞工单流转、监控告警或工具采购。它只处理“扫描器结果是否能成为安全审计证据”。

## 核心原则

### 1. 扫描器结果是线索，不是漏洞结论

扫描器能告诉你“这里值得看”，不能自动证明“这里成立”。以下都不得直接写 technical_confirmed：

- 工具 severity 是 high/critical。
- 工具 confidence 是 high。
- 工具状态是 reachable、validated、technical_confirmed valid。
- SARIF 有 codeFlows/threadFlows。
- CodeQL 或 Semgrep 给出 source-to-sink path。
- DAST 得到 200、500、反射、延迟、callback 或错误栈。
- SCA 命中受影响版本。
- Secret 扫描命中格式或校验器说 valid。
- AI triage、Autofix、assistant 或平台模型 或平台模型建议“可忽略/可修复/已验证”。

检验句：**如果删除工具名称、severity、confidence 和自动结论，只保留代码、请求、响应、日志、副作用、负控和清理记录，漏洞是否仍成立？**

### 2. 工具状态和人工状态必须分离

扫描器状态只描述工具视角；人工状态描述审计结论。不要混用。

| 扫描器状态 | 只能说明 | 人工还必须确认 |
|---|---|---|
| open | 规则仍命中 | 是否可达、可控、有影响 |
| reviewing | 等待处理 | 缺口是什么 |
| fixed / removed | 新扫描不再出现 | 代码/配置是否真正修复，是否因规则变化、文件删除、忽略导致消失 |
| ignored / suppressed | 工具不再提示或被忽略 | 忽略理由是否有效，是否有风险接受证据 |
| reachable | 工具认为路径可达 | route、运行配置、攻击者条件、真实调用是否成立 |
| validated / technical_confirmed valid | 工具有某种验证 | 验证强度是否足以支撑安全影响 |
| provisionally ignored | AI 或平台初筛认为低风险 | 人工是否同意，以及是否有证据 |

人工复核状态必须和报告提交状态分开。人工复核状态描述“技术证据是否证明问题发生”；报告提交状态描述“官方安全模型、范围、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和披露规则是否允许把它作为新漏洞提交”。

人工复核状态只能是：

```text
technical_confirmed / candidate / blocked / rejected
```

`fixed` 不是漏洞状态；它是修复状态，必须经过复测才能写“已修复”。

`需要外部门禁裁决` 的含义是：route/source/trace/sink/强正控/负控可以证明技术现象真实发生，但官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 还没裁决，或已经裁决为不能作为新漏洞提交。它不能被包装成“可提交高危漏洞”。

提交资格仅作为外部门禁引用；具体状态和值由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决。


### 3. 证据链高于数量和规则名

多个工具重复报同一位置，不等于多个漏洞；一个规则命中多个 helper，也不一定是多个漏洞。必须按真实攻击路径聚合：同一入口、同一 source、同一 sink、同一安全边界、同一修复点，通常合并为一个 finding。

反过来，一个扫描器 finding 也可能拆成多个人工 finding：同一规则命中多个入口、不同攻击者权限、不同租户边界、不同 sink 或不同修复责任时，应拆开裁决。

### 4. 数据流工具的 path 必须人工复核

CodeQL、Semgrep、商业 SAST、SARIF codeFlows 可以节省定位时间，但工具模型不等于运行语义：

- source pattern 可能过宽，把包装函数、默认值、子表达式或服务端常量标成 taint。
- propagator 可能漏掉框架绑定、ORM hydration、DTO 映射、队列、缓存、对象属性、异步消费或动态调用。
- sanitizer 可能过宽，认为某函数安全，但 sink 实际使用未净化变量，或上下文不匹配。
- sink 可能过粗，只命中函数名，没有定位危险参数。
- 工具通常只展示一条代表路径，不证明其他路径不存在，也不证明该路径在当前 profile、feature flag、DI 实现、路由缓存下可达。
- local flow、global flow、taint tracking、value flow 的含义不同；taint 表示“受影响”，不等于完全控制 sink 参数。

检验句：**我能否手写一条 route -> source -> binding -> trace hops -> sink 参数 -> transform gap -> strong positive -> impact -> negative control 的链？不能就不能 technical_confirmed。**

### 5. 默认授权实验模式下要追最高可证明影响

在自有、明确授权、隔离、可重置、可清理环境中，不要停在扫描器弱证明：

- SQL/NoSQL 不停在 error-only；继续验证布尔、时间、常量、测试表、测试集合、受控 count 或受控写入。
- RCE/命令执行不停在 marker；继续验证 stdout/stderr、退出码、执行用户、工作目录、受控文件、受控回连。
- SSRF 不停在 callback；继续验证最终 URL、重定向后目标、解析后 IP、授权内网 canary、metadata mock、防护边界或响应可读性。
- XSS 不停在 reflect；继续验证浏览器执行、上下文突破、存储触发、CSP 影响和目标角色触发。
- IDOR/越权不停在替换 ID 返回 200；继续验证 A/B 主体、对象归属、跨租户、敏感字段或状态改变。
- SCA 不停在 version-only；继续验证运行包加载、调用点可达、漏洞条件满足和触发输入。
- Secret 不停在 regex-only；继续验证暴露面、有效性、权限范围和轮换状态，并全程保持非账号类敏感材料展示边界清楚。

强验证边界是授权、数据和可恢复性：不越权，不打第三方真实系统，不读取真实生产用户数据，不泄露真实凭据，不制造不可清理副作用。没有账号、对象、日志、快照、清理能力时，降级为 `blocked`，不要强行 technical_confirmed。

### 6. 弱 payload 阴性不是 rejected

扫描器 payload 失败、PoC 无回显、callback 未触发、时间差不稳定，不自动代表漏洞不存在。先判断：

- payload 是否到达同一个 sink。
- payload 是否适配当前数据库、shell、模板、解析器、编码、Content-Type、序列化格式。
- 入口是否需要认证、对象、租户、feature flag、队列消费或异步触发。
- 防护是否真的同变量、同路径、同上下文生效。
- 观察点是否正确：响应、日志、数据库、文件、队列、浏览器、OOB。

只有有明确否定证据，才能 rejected。

### 7. 工具可定位 ID，不能替攻击者获得 ID

扫描器、SARIF、CodeQL、Semgrep、DAST、Burp、Nuclei 或其他模型/工具 经常会把对象 ID、资源 URI、file key、tenant/workspace、physical table、share token、lookup handle 标出来，但“工具看到”不等于“攻击者能获得”。凡是 finding 的利用链依赖对象标识符，都必须额外裁决：

- 工具给出的 ID 是来自扫描上下文、管理员样本、历史报告、截图、fixture、日志、测试脚本，还是攻击者自身可达入口。
- 攻击者能否从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口获得它。
- 单个样本是否只能支撑单对象 claim；批量、全量、任意对象、全用户、全租户、全工作区是否有可获得规模证据。

检验句：**如果删除扫描器提供的样本 ID，攻击者还能不能自己拿到目标 ID？如果不能，finding 不能因为工具命中就升级为高价值 technical_confirmed。**

### 8. 多主体扫描结论必须有账号对象矩阵

扫描器或 DAST 工具可能用多个 token、cookie、会话、HAR、浏览器 profile、PAT 或测试账号重放请求。只要结论依赖跨用户、跨租户、owner/victim、无权限主体、清理账号或修复复测，就必须记录账号对象矩阵，避免把同一 token 误当双主体、把 owner 当 attacker、把中间件账号当 Web 管理员。

多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

### 9. 扫描器 technical_confirmed 不等于 对外提交资格

扫描器的 `technical_confirmed`、`validated`、`reachable`、`exploit available`、`active`、`verified`、`fixed`、`reopened`、`dismissed` 或 AI triage 状态，只能说明工具或平台做过某种判断；不能说明这条 finding 已经满足官方披露边界。即使人工强正控和负控都成立，也还要问：

- 官方 SECURITY、安全策略或报告规则是否把该行为列入范围？
- 默认配置是否真实受影响，还是只在 debug、本地、示例、危险开关、管理员配置或非默认 profile 下出现？
- 官方权限模型、对象模型、租户模型、插件模型、沙箱模型、URL fetch 模型、日志模型或 API 文档是否把该行为定义为预期能力？
- release note、changelog、known issue、advisory、FAQ、issue、文档警告或 accepted risk 是否已经覆盖这条风险？
- 当前证据是否只是 hardening only、best practice、低价值信息泄露、管理员正常能力、受信任主体能力或 范围或官方已知拒绝（外部裁决）？
- 如果要写未认证、低权限、跨用户、跨租户、默认配置受影响、高危、严重、RCE、SSRF 内网访问、沙箱逃逸、有效凭据泄露、批量越权，官方模型是否支持这些强声明？

检验句：**我证明的是扫描器命中的技术现象，还是证明了未受信任主体违反官方承诺的保护边界？如果后者没有证据，只能写 需要外部门禁裁决、candidate 或 blocked。**

## 审计目标

本 Skill 的目标不是“清空扫描器列表”，而是把扫描器结果转成可行动的安全审计结论。

必须证明：

- 工具命中的文件、行号、依赖、请求或配置属于当前审计版本、构建产物或运行环境。
- 工具规则适配当前语言、框架、库版本、调用方式和配置。
- finding 对应的入口真实可达，且 route、handler、middleware、feature flag、profile、插件启用状态明确。
- 攻击者可控 source 存在，控制主体、权限、对象、租户和控制粒度明确。
- source 到 sink 的 trace 人工闭合；每一跳变量、函数、分支、防护和权限都可解释。
- sink 的危险参数位置确实被污染，而不是只命中函数名、日志参数、label、测试路径或安全上下文。
- transform、防护、sanitizer、validator、parameterization、escape、allowlist、authz、framework default 是否有效已被裁决。
- 强正控能证明真实 CIA 影响或安全边界破坏。
- 负控能排除缓存、随机、正常权限、错误页、限流、WAF、工具误报和环境偶然性。
- 若 finding 依赖对象 ID、资源 URI、token、object key、physical table 或 lookup handle，必须证明攻击者获取路径和可获得规模。
- 若 finding 依赖多账号、多对象、跨租户、owner/victim 或清理动作，必须有账号对象矩阵和 token/cookie 隔离证据。
- 若 finding 准备进入报告、对外提交、风险评级、修复优先级裁决或“官方未公开/默认配置受影响”声明，必须有 `EVID_OFFICIAL_SECURITY_MODEL`，证明 scope、默认配置、权限模型、对象模型、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 与当前 claim 不冲突。
- technical_confirmed 和对外提交资格必须分层；动态强正控成立但官方模型未知时，只能写 `需要外部门禁裁决`、`candidate` 或 `blocked`。
- 清理/恢复完成，或明确无副作用。
- Allowed Claims 与 Forbidden Claims 限制报告阶段渲染不超过证据。

必须排除：

- 测试、示例、fixture、mock、demo、文档、生成代码、未部署目录。
- 死代码、未注册路由、未启用 profile、未加载插件、关闭的 feature flag。
- 不可控参数、服务端常量、可信配置、不可伪造 claim、被服务端覆盖的字段。
- sink 不可达、危险参数未污染、只进入日志/注释/展示标签/安全上下文。
- 框架默认防护被工具漏建模，或 sanitizer 被工具误判。
- SCA 版本命中但组件未打包、未加载、漏洞功能未调用、修复版本已在运行包中。
- Secret 是占位符、测试值、假 key、已吊销、权限不足或攻击者不可获得。
- DAST 响应差异来自缓存、随机 token、限流、错误页、统一异常处理或 WAF。
- 工具提供的对象 ID、URI、token、object key、physical table、截图 ID 或历史报告 ID 不可由攻击者获得。
- 多主体扫描其实使用了同一 token/cookie、对象公开、权限本来允许或账号角色混淆。

## 输入材料

### 扫描器原始材料

至少读取原始结果，而不是只看截图或摘要：

- SARIF/JSON/XML/HTML/CSV/Markdown/控制台输出/平台导出。
- 工具名称、工具版本、规则集版本、扫描时间、扫描范围、分支、commit、构建 ID。
- 规则 ID、query id、CWE、category、message、severity、confidence、precision、tags。
- finding id、fingerprint、partial fingerprint、location、related locations、codeFlows、threadFlows、dependency path、request/response。
- baseline、ignore、suppression、removed、fixed、triage status、AI triage、autofix、reachability、validation 状态。

### 源码与构建材料

- 路由、controller/handler、service、repository/DAO/mapper、model、serializer/deserializer、template、middleware/filter/interceptor、policy/guard。
- 配置、默认配置、环境变量、feature flag、profile、插件注册、路由缓存、依赖注入、AOP、队列、cron、事件监听。
- manifest、lockfile、dependency tree、SBOM、构建产物、镜像、运行包、版本输出。
- 单元测试、集成测试、既有安全 wrapper、扫描器 ignore 注释和误报说明。

### 运行态材料

- 授权范围、环境类型、版本、配置、账号、角色、租户、测试对象、快照、日志和清理能力。
- baseline 请求、弱正控、强正控、升级验证、负控请求。
- 响应、日志、审计日志、数据库/缓存/队列/文件/对象存储状态、OOB/callback、浏览器执行、命令输出。
- 标识符获取运行态：攻击者从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列、分页或批量接口获得对象 ID、用户 ID、租户/工作区 ID、文件 URI、object key、lookup handle 或分享 token 的请求链；若不可获得，也要记录排查过的入口。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 修复后复测、负控、清理/恢复结果。

### 安全模型与报告材料

- 官方安全策略、scope、范围或官方已知拒绝（外部裁决）、默认配置、权限模型、known issues、accepted risk、release notes。
- SECURITY、安全策略、API 文档、权限/对象/租户/插件/沙箱模型、默认配置、危险开关、debug/local/admin-only 条件、safe harbor、提交材料质量要求、release note、changelog、security advisory、known limitation、duplicate、won't fix、hardening only 说明。
- 原漏洞报告、复核意见、修复 PR、忽略原因、风险接受说明。
- Allowed Claims、Forbidden Claims、Missing Evidence、对外提交阻塞项、停止继续升级原因。

## Source 识别

扫描器常把 source 简化成“用户输入”或“外部数据”。人工复核必须还原攻击者条件。

### SAST / dataflow source

检查：

- source pattern 是否真对应攻击者输入：HTTP query/body/header/cookie/path、GraphQL variables、WebSocket message、RPC 参数、CLI 参数、queue message、webhook payload、上传文件、导入数据、数据库二次污染、日志再解析、OAuth/SAML/JWT claim。
- source 是否由低权限或外部主体控制；如果只来自管理员配置、部署者环境变量、服务端常量、系统任务或可信内部服务，必须限定攻击者条件。
- source 控制粒度：完整字符串、结构字段、枚举值、数字范围、路径片段、URL host、header 名称、operator、排序字段、模板片段、对象 ID。
- source 若是对象 ID、资源 URI、object key、lookup handle、tenant/workspace、physical table 或 share token，必须额外确认攻击者如何获得该标识符；“工具 path 中出现了 ID”只说明工具有样本，不说明攻击者可获得。
- source 是否被框架绑定到 DTO、Model、Request、Serializer、Form、Command、Message、Entity 或 Map。
- source 是否被默认值、服务端覆盖、schema、枚举、类型转换、权限过滤或后端查询结果替代。

### DAST source

DAST source 是请求差异，不等于字段可控性成立。检查：

- 请求是否来自真实业务流程，还是扫描器手造无效请求。
- 参数是否被服务端接收，还是被网关、WAF、schema、Content-Type、CSRF、认证失败拦截。
- 响应差异是否由该字段导致；每次只改变一个变量。
- 重放是否稳定；是否受缓存、随机 token、限流、时间、会话状态影响。
- DAST 请求中的对象 ID、路径、URI、token、workspace、object key 是攻击者业务流程自然拿到的，还是扫描器录制、管理员样本、历史 HAR、报告附件或手工替换得到的。
- 如果是存储型，写入端和触发端是否都可控并跨越安全边界。

### SCA source

SCA source 是“漏洞组件可被攻击输入触达”。检查：

- 漏洞组件是否在运行包、镜像或部署环境中实际存在。
- 漏洞函数、类、endpoint、parser、协议、反序列化器、压缩/解压、模板、日志、HTTP client 是否被调用。
- 攻击者输入是否能进入漏洞条件；不是所有依赖版本命中都可利用。
- 是否有上层限制、配置关闭、补丁 backport、wrapper、防火墙、协议限制或不可达调用点。

### Secret source

Secret finding 必须回答“攻击者能否获得”：

- secret 位于公开仓库、发布包、镜像层、前端 bundle、日志、错误页、移动端包、文档、备份、artifact、CI 输出还是私有本地文件。
- secret 是真实值、测试值、占位符、示例值、假阳性格式还是已吊销。
- secret 权限、scope、有效期、轮换状态和最小验证方式。
- 对第三方或生产真实敏感值，报告中只允许使用 hash、尾号、权限元数据或目标官方接收流程；不得在不受控渠道输出完整可复用凭据。该限制不能替代账号对象矩阵事实：复现所需授权测试账号和账号对象矩阵必要事实应由报告阶段按唯一模板渲染。

## Sink 识别

扫描器命中函数名不够，必须定位危险参数和安全语义。

### 常见 sink 类别

| 类别 | 例子 | 必须确认 |
|---|---|---|
| 查询 | SQL/NoSQL/LDAP/XPath/HQL/JPQL/Elasticsearch/GraphQL resolver | 动态值、动态结构、operator、列名、排序、表名、raw fragment |
| 执行 | shell、process、eval、template expression、script engine、反序列化、插件 hook | 参数进入执行语义，不是日志或预览 |
| 网络 | HTTP client、webhook、URL preview、redirect follow、DNS、SMTP、FTP、Redis | 最终 URL、host/IP、协议、重定向后目标、内网/metadata 边界 |
| 文件 | read/write/delete/copy/move、include、upload、extract、object key | resolved target、base 约束、软链接、覆盖模式、可访问性、清理 |
| Web 输出 | HTML/JS/CSS/URL/attribute、response header、Location、Set-Cookie | 输出上下文、转义、浏览器执行、目标角色 |
| 权限业务 | auth decision、ACL、policy、tenant filter、export、delete、invite、billing | 主体、对象、租户、状态改变 |
| 依赖组件 | parser、converter、logger、serializer、image/PDF/XML/archive 库 | 运行加载、调用路径、漏洞条件 |
| Secret/IaC | key 使用点、IAM policy、container capability、hostPath、public bucket | 实际部署、权限、暴露面、补偿控制 |

### sink 复核问题

- 扫描器命中的位置是否是危险参数，还是函数其他参数、日志上下文、注释、错误消息或测试 helper。
- source 是否能控制完整 sink 参数，还是只能控制不可危险的片段。
- sink 是否在当前入口、分支、权限、profile、feature flag 下执行。
- sink 前是否有同变量、同路径、同上下文的防护。
- sink 影响是否被官方安全模型视为预期功能、管理员正常能力、沙箱内能力或范围外。

## Transform / 防护检查

扫描器最容易误判 sanitizer、framework default 和权限检查。复核必须用“同变量、同路径、同上下文”原则。

### 防护分类

| 防护 | 有效条件 | 常见误判 |
|---|---|---|
| 参数化 | sink 的值位置使用绑定变量 | 动态列名、表名、排序、operator、raw fragment 未保护 |
| allowlist | 服务端固定集合，失败阻断 | 黑名单、前缀判断、用户可写 allowlist、只做长度限制 |
| escape/encode | 与输出上下文匹配 | HTML escape 用到 JS/URL/CSS/header/shell/SQL |
| normalize/canonicalize | 在权限和路径判断前执行 | 检查前后变量不一致，符号链接/双编码未处理 |
| schema/type validation | 服务端执行，覆盖实际字段 | 客户端校验、只校验另一字段、默认值覆盖不清楚 |
| authz/policy | sink 前执行，绑定当前主体和对象 | 只在 UI 层、列表页、单对象检查，批量/导出/异步遗漏 |
| framework default | 当前配置真实启用，调用方式未绕过 | raw API、关闭 autoescape、禁用 CSRF、绕过 middleware |
| WAF/rate limit | 能稳定阻断漏洞语义 | 只挡当前 payload，换编码/结构/路径仍可达 |

### 扫描器 sanitizer 裁决

对每个 sanitizer 写成四类之一：

```text
effective：同变量、同路径、同上下文、sink 前执行，负控证明阻断。
partial：只覆盖部分字段、分支、上下文、配置或 payload。
bypassed：强正控证明绕过。
unknown：文档或代码显示可能存在，但运行态/路径/上下文未确认。
```

只有 `effective` 可作为 rejected 或降级依据；`unknown` 只能导致 `candidate` 或 `blocked`。

## 路由与调用链追踪

扫描器经常只给文件行号，不给真实入口。复核时必须把 finding 接回可触发路径。

### 入口类型

- HTTP route、REST、GraphQL resolver、WebSocket、SSE、gRPC、RPC。
- CLI command、cron、queue consumer、event listener、webhook、文件导入、批处理任务。
- CMS/plugin hook、admin ajax、template render、mobile/API endpoint、serverless function。
- DAST 请求对应的真实浏览器流程。

### 追踪要求

每一跳记录：

```text
entry -> handler -> binder/DTO -> service -> helper -> repository/client/parser/template -> sink
file:line -> function/method -> variable/field -> branch/auth -> next hop
```

特别处理：

- 父类、接口、trait、mixin、decorator、middleware、filter、interceptor、AOP。
- 依赖注入、服务容器、反射、注解/attribute、动态路由、路由缓存。
- 异步生产端和消费端；存储型漏洞的写入端和读取端。
- 生成代码和框架约定目录；确认是否进入构建产物或部署目录。

### 降级条件

- 只有 scanner file:line，没有入口。
- 只有 handler，没有 source 绑定。
- 只有 source，没有 sink。
- 只有 sink，没有调用链。
- trace 中断且无法解释 DI/接口/异步/存储两端。
- middleware、policy、guard 顺序未确认。
- DAST 请求无法重放或无法关联到 handler。

## 数据流追踪步骤

### 第 1 步：冻结扫描上下文

记录：工具、版本、规则集、扫描范围、commit、分支、构建产物、运行版本、扫描时间、配置、baseline、ignore、AI triage、导出格式。

禁止把不同 commit、不同分支、不同运行包、不同配置的扫描结果混成一个结论。

### 第 2 步：保留原始 finding

保留工具原始文本，不要马上改写：

```yaml
scanner_finding:
  tool: ""
  tool_version: ""
  rule_id: ""
  query_id: ""
  cwe: ""
  severity: ""
  confidence: ""
  scanner_status: open | reviewing | fixed | removed | ignored | validated | reachable | unknown
  finding_id: ""
  fingerprint: ""
  locations:
    - file: ""
      line: ""
  codeflows: []
  request_response: ""
  dependency_path: ""
  secret_validation: ""
  identifier_samples:
    - value_type: user_id | object_id | tenant_id | workspace_id | file_uri | object_key | lookup_handle | token | physical_table | other
      source: attacker-flow | scanner-sample | admin-sample | historical-report | screenshot | log | unknown
      obtainable_by_attacker: yes | no | unknown
      obtainable_scale: single | multiple | bulk | continuous | enumerable | inferable | not-obtainable | unknown
  account_object_matrix_refs: []
  original_claim: ""
```

### 第 3 步：拆分 claim

把扫描器描述拆成可裁决 claim：

```text
Claim A：这里有某类漏洞。
Claim B：攻击者能控制 source。
Claim C：source 能到达 sink。
Claim D：防护不存在或无效。
Claim E：能造成某种影响。
Claim F：风险等级为 High/Critical。
Claim G：已经修复/误报/可忽略。
Claim H：攻击者能获得利用所需的对象标识符。
Claim I：多主体、多对象、跨租户或清理步骤的账号对象矩阵成立。
```

逐个 claim 裁决，不要整体接受或整体拒绝。

### 第 4 步：按真实漏洞实例去重

去重维度：

- 同一入口和攻击路径。
- 同一 source、同一 sink、同一防护缺口。
- 同一攻击者条件和对象/租户边界。
- 同一修复点。
- 同一依赖组件和同一可达调用点。

不要只按文件行号、规则 ID 或 fingerprint 去重；这些是辅助。

### 第 5 步：复核 source

从扫描器 source 或 DAST 参数开始，确认攻击者最低权限、控制字段、控制粒度、绑定变量、默认值、覆盖逻辑和可信边界。

输出：

```text
source_status: controlled / partially-controlled / stored-taint / not-controlled / unresolved
attacker_condition:
control_granularity:
binding_evidence:
identifier_acquisition:
  required_identifiers:
  attacker_obtainable_path:
  obtainable_scale:
  known_id_only: yes/no/unknown
blocking_evidence:
```

### 第 6 步：裁决标识符获取与账号对象矩阵

只要 finding 依赖 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、资源 URI、object key、physical table 或其他标识符，就先裁决标识符获取链。

输出：

```text
identifier_acquisition_status: attacker-obtainable / single-sample-only / tool-sample-only / admin-sample-only / not-obtainable / unresolved
identifier_path:
  entry:
  request_or_page:
  response_field_or_location:
  actor:
  scale: single / multiple / bulk / continuous / enumerable / searchable / exportable / inferable / not-obtainable / unknown
known_id_boundary:
```

只要 finding 依赖跨用户、跨租户、owner/victim、无权限主体、清理账号、批量对象、修复复测或多 token 重放，就裁决账号对象矩阵。

```text
account_object_matrix_status: complete / partial / missing / contradicted
attacker:
owner:
victim:
control:
cleanup:
token_cookie_isolation: proven / mixed / unknown
object_ownership_evidence:
```

只有工具样本 ID、管理员视角 ID、截图 ID、历史报告 ID、手工粘贴 ID 时，不得继续按高价值 technical_confirmed 写；只能降级为 `candidate` 或 `blocked`，除非补出攻击者可达获取路径。

### 第 7 步：复核 sink

从扫描器 sink 开始，确认危险 API、危险参数位置、执行分支、上下文和影响语义。

输出：

```text
sink_status: dangerous / non-dangerous / wrong-parameter / test-only / unreachable / unresolved
sink_parameter:
execution_condition:
impact_semantics:
```

### 第 8 步：重建人工 trace

不要只复制工具 path。手写人工 trace：

```text
Route/Message/Command:
  -> Source binding: file:line variable
  -> Transform / DTO / Model: file:line variable
  -> Branch / Auth decision: file:line condition
  -> Service / Repository / Client: file:line variable
  -> Sink argument: file:line parameter
Trace status: complete / partial / broken / tool-only
```

### 第 9 步：裁决防护

对 scanner 标出的 sanitizer、没标出的框架防护、权限检查和配置防护逐项裁决：

```text
protection:
  type:
  location:
  same_variable: yes/no/unknown
  same_path: yes/no/unknown
  same_context: yes/no/unknown
  failure_blocks: yes/no/unknown
  runtime_enabled: yes/no/unknown
  verdict: effective / partial / bypassed / unknown
```

### 第 10 步：决定动态验证策略

根据漏洞族选择强正控、观察点、负控和清理方式。若没有运行态条件，写 `blocked` 缺口，不得假装 technical_confirmed。

对 IDOR、未授权、对象级授权、跨租户、批量导出、任意文件/对象访问类 finding，动态验证策略必须先包含：攻击者如何获得必要标识符、A/B 主体和对象归属如何证明、token/cookie 如何隔离、批量声明的 ID 规模如何证明。

### 第 11 步：追最高影响

从扫描器弱证明推进：

```text
scanner hit -> route/source/sink -> weak positive -> strong positive -> impact -> highest authorized impact -> negative control -> cleanup -> claim boundary
```

停止必须写原因。

### 第 12 步：裁决官方安全模型与对外提交资格

扫描器复核不能只在“技术是否发生”处停止。任何准备进入报告、对外提交、定级、写修复优先级或写强漏洞声明的 finding，都必须补上官方安全模型裁决。

输出：

```text
security_model_status: 记录官方安全模型是否已复核、是否支持当前声明、是否属于预期行为/accepted risk/范围拒绝/known issue 等；具体状态值以对应中文 schema、template 和 validator 为准。
target_scope_status: in-scope / 范围或官方已知拒绝（外部裁决） / unknown
默认配置边界说明: default-affected / non-default-only / debug-local-only / admin-config-only / unknown
official_known_status: not-known / duplicate / known-limitation / advisory-covered / unknown
预期行为说明: violates-boundary / expected / unknown
accepted risk 说明: not-accepted / accepted / unknown
外部门禁引用：提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决；本 Skill 不复制枚举、不生成状态。
forbidden_submit_reasons:
```

判断规则：

- 对外提交资格由外部门禁裁决：官方资料、scope、默认配置、known issue 去重、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 都已裁决，且当前证据证明未受信任主体违反官方保护边界。
- `官方已知排除（外部裁决）`：技术强证据可能成立，但官方模型、scope、默认配置或 known issue 未读完；不得写可提交高危/严重/默认影响。
- `需要外部门禁裁决`：官方资料明确这是预期功能、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、duplicate 或 known limitation，且当前没有证明新主体、新对象、新默认配置、新边界或官方缓解绕过。
- `需要外部门禁裁决`：技术链路可确认，但 外部门禁未裁决为可提交。

### 第 13 步：给出人工裁决

输出：

```text
manual_status: technical_confirmed / candidate / blocked / rejected
confidence: high / medium / low
scanner_delta:
  accurate:
  overstated:
  missed:
security_model_status:
外部门禁引用:
forbidden_submit_reasons:
allowed_claims:
forbidden_claims:
missing_evidence:
next_action:
```

## 必检证据点

### 扫描器元数据

- 工具名称、版本、规则集版本。
- 规则 ID、query ID、CWE、category、severity、confidence、precision。
- 扫描范围、commit、分支、构建产物、运行版本。
- SARIF result、locations、related locations、codeFlows/threadFlows、partial fingerprints。
- DAST 请求响应、callback、payload、重放条件。
- SCA dependency path、package、version、fixed version、runtime package。
- Secret 类型、位置、validation、暴露面、非账号类敏感材料展示边界。
- IaC/container 配置位置、实际部署证据、补偿控制。

### 代码证据

- route/message/command 是否注册并启用。
- source 字段、绑定位置、可控主体、控制粒度。
- `EVID_IDENTIFIER_ACQUISITION`：依赖对象 ID、用户 ID、租户/工作区 ID、文件 URI、object key、lookup handle、physical table 或 token 的 finding，必须证明攻击者获取路径、入口、响应字段和可获得规模。
- `EVID_ACCOUNT_OBJECT_MATRIX`：依赖多主体、多对象、跨租户、owner/victim、无权限主体、清理或复测的 finding，必须证明账号用途、账号对象矩阵必要事实、主体 ID、角色、对象归属、token/cookie 隔离和清理责任。
- `EVID_OFFICIAL_SECURITY_MODEL`：准备写报告、定级、对外提交或写强漏洞声明的 finding，必须证明官方 SECURITY/scope/API 文档/权限模型/对象模型/默认配置/known issue/expected behavior/accepted risk/范围或官方已知拒绝（外部裁决）/report quality 规则已经裁决。
- trace 每一跳 file:line、变量名、函数、分支和权限。
- sink 危险 API、危险参数、执行条件。
- transform、防护、sanitizer、authz 是否同变量、同路径、同上下文。
- 框架默认防护是否真实启用，是否被 raw API 绕过。

### 运行态证据

- baseline 请求。
- 强正控请求或操作。
- 响应差异、日志、审计日志、数据库/缓存/队列/文件/对象状态。
- OOB/callback、最终目标、浏览器执行、命令输出、组件触发。
- 负控请求或操作。
- 清理/恢复证据。

### 不可声明边界

每条 finding 都必须写不能声明什么：

- scanner-only 不能声明 technical_confirmed。
- sink-only 不能声明可利用。
- callback-only 不能声明内网敏感 SSRF。
- marker-only 不能声明命令执行。
- error-only 不能声明数据读取。
- reflect-only 不能声明浏览器执行。
- version-only 不能声明组件漏洞可达。
- regex-only 不能声明有效凭据泄露。
- fixed/removed 不能声明已修复，除非复测证明。
- known-ID-only 不能声明攻击者稳定可利用、批量越权、任意对象、所有用户、所有租户或高价值 technical_confirmed。
- tool-ID-only 不能声明攻击者可获得；工具样本、管理员样本、截图样本、历史报告样本只用于定位。
- single-ID-only 不能外推为批量、全量、持续、枚举或跨租户影响。
- 缺账号对象矩阵不能声明跨用户、跨租户、owner/victim、受害者上下文、清理可重放或多主体 technical_confirmed。
- 官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior 未裁决、accepted risk 未裁决、范围或官方已知拒绝（外部裁决） 未裁决时，不能声明 对外提交资格、默认配置受影响、官方未公开、高危/严重、跨租户边界破坏、未认证可利用、沙箱逃逸或有效凭据泄露。
- technical_confirmed 但官方模型阻塞时，不能把 `需要外部门禁裁决` 包装成新漏洞提交结论。

## 动态验证触发条件

### 必须动态验证才能 technical_confirmed

- DAST findings：请求可重放、差异归因、强正控、负控。
- 越权/IDOR/鉴权绕过：标识符获取链、双主体、双对象、租户/组织/owner 对照、账号对象矩阵、token/cookie 隔离和对象归属。
- SSRF：服务端请求、最终目标、重定向后目标、DNS/IP、内网 canary 或 metadata mock。
- 文件读写上传解压：resolved target、读写结果、可访问面、覆盖/追加语义、清理。
- 命令/代码/模板/表达式执行：执行语义、结果、权限边界。
- SQL/NoSQL/LDAP/XPath：查询语义差异、测试数据、受控写入或稳定时间/布尔证明。
- XSS：浏览器执行上下文、存储触发、目标角色、CSP 影响。
- CSRF：无 token 或跨站条件下状态变更，配 token 负控。
- SCA reachability：运行加载、调用点、漏洞条件、触发输入。
- Secret：有效性、权限、可获得性、轮换状态，且不输出原值。
- IaC/container：实际部署、身份权限、网络暴露和补偿控制。
- 对外可提交强声明：官方 SECURITY/scope/默认配置/权限模型/对象模型/known issue/expected behavior/accepted risk/范围或官方已知拒绝（外部裁决） 必须裁决；缺官方模型时只能写技术复核状态，不得对外提交强漏洞声明。

### 可先进入 candidate

- 静态 route/source/trace/sink 基本完整，但缺运行环境。
- 工具 path 与人工 trace 大体一致，但缺强正控或负控。
- 对象 ID 可影响响应，但 ID 只来自工具样本、手工样本、截图、历史报告或管理员视角，尚未证明攻击者获取路径。
- 单对象样本可疑，但批量、持续、全量、任意对象、所有用户或跨租户声明缺可获得规模证据。
- SCA 版本和调用点存在，但缺触发条件。
- Secret 暴露面可疑，但未验证有效性或权限。
- DAST 有差异，但缺日志或归因负控。

### 必须 blocked

- 需要账号、对象、租户、日志、OOB、浏览器、队列消费、构建产物、feature flag、license 或清理能力才能判断。
- 需要复现运行配置才能验证 scanner trace。
- 需要运行态确认攻击者能否从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口获得必要标识符。
- 需要运行态确认账号对象矩阵、对象归属、role/scope、tenant/workspace、token/cookie 隔离或清理责任。
- 需要修复后版本才能确认 fixed。

### 不能动态验证的边界

- 目标不在授权范围。
- 会访问第三方真实系统或范围外目标。
- 会读取、导出、泄露真实生产用户数据。
- 会输出、复用、转储真实 secret、token、cookie、密码或云凭据。
- 无测试账号、测试对象、日志、快照、重置或清理能力。
- 副作用不可控、不可回滚或不可隔离。

## 授权实验模式下的强验证方法

强验证只用于明确授权、隔离、可重置、可清理环境。每次记录：环境、版本、配置、测试账号、测试对象、观察点、快照、清理方式和停止原因。

### 强验证矩阵

| 类型 | 从扫描器弱证据 | 推进到强证据 | 负控 | 清理 |
|---|---|---|---|---|
| SQL/NoSQL | error/规则命中 | boolean/time/常量/测试表或测试集合/受控写入 | false 条件、安全值、参数化修复、无权限主体 | 删除测试记录、回滚快照 |
| RCE/CMD | marker/危险函数 | stdout/stderr、执行用户、工作目录、受控文件、受控回连 | 普通值、移除字段、禁止命令、修复后 | 删除文件、关闭 listener、恢复快照 |
| SSRF | callback/DNS | 最终 URL/IP、重定向后目标、内网 canary、metadata mock、响应可读性 | 允许/禁止 host、重定向对照、协议/IP 变体 | 销毁 canary、保存日志 |
| XSS/SSTI | reflect/template sink | 浏览器执行、上下文突破、存储触发、模板执行语义 | 编码值、不同上下文、安全模板、CSP 对照 | 删除测试内容 |
| 文件/上传/归档 | path sink | resolved target、受控读写、写后可达、覆盖/追加、软链接/entry | base 内外、安全扩展、禁止链接、修复后 | 删除测试文件、恢复目录 |
| IDOR/Auth | 200/缺检查/已知 ID 后成功 | 标识符获取链、账号对象矩阵、A/B 主体、对象归属、跨租户、敏感字段、状态改变；批量声明还要证明 ID 可批量、持续、枚举、列表、搜索、导出、关系链或可推导获得 | 自己对象、他人对象、无权限、不同租户、不可获得 ID、token/cookie 隔离 | 恢复对象状态 |
| SCA | version hit | 运行加载、调用路径、漏洞条件触发 | 修复版本、组件未加载、配置关闭 | 恢复依赖/镜像 |
| Secret | regex/validator | 可获得性、最小有效性、权限范围、轮换状态 | 占位符、吊销、权限不足、不可获得 | 轮换/吊销并记录非账号类敏感材料展示边界 |
| IaC/Container | config hit | 实际部署、权限、网络、身份、补偿控制 | 未部署、策略覆盖、只读权限、网络隔离 | 回滚配置 |
| 对外提交资格 | 工具 high/critical 或人工强正控 | 官方模型支持该安全边界、scope 内、默认配置/受影响配置清楚、known issue 去重、expected/accepted/范围或官方已知拒绝（外部裁决） 已排除 | 官方模型 unknown、预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、duplicate、hardening only | 不写入提交总入口报告或收缩为内部修复建议 |

### 验证请求框架

```bash
# baseline：正常路径
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {TEST_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_SCANNER_BASELINE_{ID}' \
  --data '{BASELINE_JSON}'

# strong positive：证明漏洞语义，不只证明 marker
# 如果请求依赖对象 ID / URI / object key，不要直接使用扫描器样本；先记录攻击者获取该标识符的请求链。
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {LOW_PRIV_TEST_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_SCANNER_STRONG_POSITIVE_{ID}' \
  --data '{STRONG_POSITIVE_JSON}'

# negative control：安全值 / 移除关键字段 / 无权限主体 / 自己对象
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{CONTROL_PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {CONTROL_TEST_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_SCANNER_NEGATIVE_{ID}' \
  --data '{NEGATIVE_CONTROL_JSON}'
```

### Burp / 浏览器操作

1. 保留原始请求，不覆盖证据。
2. 复制为 baseline、弱正控、强正控、安全负控、权限/对象负控、修复后复测。
3. 每次只改变一个关键变量。
4. 添加唯一 marker，便于日志关联。
5. 对比响应、日志、副作用、浏览器 Console/DOM、存储、Cookie、审计日志。
6. 若差异不稳定，记录干扰因素，不得直接 technical_confirmed。
7. 完成清理或恢复快照。

## 最高危害追踪

扫描器默认给的是下限，不是上限。对每条 candidate 按阶梯推进：

```text
工具命中 -> 可达入口 -> 可控 source -> sink 危险参数 -> 防护缺口 -> 弱正控 -> 强正控 -> CIA 影响 -> 跨主体/对象/租户/沙箱/网络边界 -> 负控 -> 清理 -> 声明边界
```

### 成熟价值过滤

以下弱证据不得主提交，除非追到额外边界：

- prompt-only、内容输出、模型幻觉：需证明越权数据访问、工具滥用、跨租户上下文、状态改变或凭据泄露。
- 沙箱内 `whoami/id/pwd`：若沙箱执行是功能，需证明逃逸、越界文件、内部网络、跨用户或 secret。
- SSRF callback-only：需最终目标、内部响应、metadata mock、内网 canary 或状态改变。
- SQL error-only：需布尔、时间、常量、受控测试数据或写入。
- IDOR 200-only：需对象归属、A/B 主体、跨租户、敏感字段或状态改变。
- known-ID-only IDOR：需攻击者可达的标识符获取链；否则只能写手工样本下可疑访问，不能写稳定可利用、批量越权或高价值 technical_confirmed。
- single-ID extrapolation：一个样本只支撑该样本或同获取路径对象，不能外推任意对象、全量、所有用户、所有租户或所有工作区。
- Secret regex-only：需可获得性、有效性、权限和轮换。
- SCA version-only：需运行加载、调用点、漏洞条件和触发输入。
- DoS single-slow：需自有环境资源曲线、恢复、限流负控和业务影响。

### 停止继续升级原因

合格停止原因：

- 已达到当前授权范围可证明的最高影响。
- 继续需要真实用户数据、真实凭据或第三方系统。
- 缺测试账号、对象、租户、日志、OOB、快照或清理能力。
- 已穷尽当前授权入口，仍无法证明攻击者可获得必要标识符。
- 批量/全量声明缺可获得规模证据，已收缩为单对象或 candidate。
- 防护经同变量、同路径、同上下文证明有效。
- 官方安全模型说明这是预期功能，且没有新边界。
- 当前证据足以支撑准确等级，继续只会增加不可清理副作用。

不合格停止原因：

- “工具已经 high”。
- “payload 太强所以不验证但仍 technical_confirmed”。
- “callback 已经够了”。
- “AI 说可利用”。
- “弱 payload 没打通所以 rejected”。
- “工具给了 ID，所以攻击者一定能拿到”。
- “一个样本 ID 成功，所以所有用户/租户/对象都受影响”。

## 负控设计

负控用于证明正控差异来自漏洞条件，而不是正常功能、缓存、随机、权限本来允许、错误页、WAF、限流、扫描器规则缺陷或环境噪声。

### 负控类型

| 负控 | 设计方式 | 用于排除 |
|---|---|---|
| 参数负控 | 安全值、非法值、移除字段、只改一个变量 | payload 偶然性、错误归因 |
| 权限负控 | 无登录、低权限、普通用户、owner、管理员 | 管理员正常能力误报 |
| 对象负控 | 自己对象、他人对象、不同租户、不可见对象 | IDOR/BOLA 误判 |
| 标识符获取负控 | 不给手工样本 ID，只让 attacker 从自身入口获取；移除管理员/历史报告/截图样本后重试 | tool-ID-only、known-ID-only、管理员视角样本 |
| 批量标识符负控 | 验证列表/搜索/导出/分页/关系链能否稳定拿到多个目标 ID；无法获得时收缩声明 | 单样本外推批量/全量 |
| token/cookie 隔离负控 | A/B 浏览器 profile、cookie jar、token 文件、请求头互换和失效验证 | 同一 token 被误当双主体、owner 被当 attacker |
| 配置负控 | 默认配置、弱配置、防护开启/关闭、feature flag | 默认影响夸大 |
| 版本负控 | 修复版本、相邻版本、运行包版本 | version-only SCA 误报 |
| 网络负控 | 允许 host、禁止 host、重定向、metadata mock、内外网 canary | callback-only SSRF 夸大 |
| 防护负控 | 参数化、allowlist、安全模板、官方缓解 | sanitizer 是否有效 |
| 规则负控 | 改 rule、关 rule、ignore 文件、删除代码 | fixed/removed 是否只是工具状态变化 |
| 清理负控 | 清理前后状态、快照恢复 | 副作用是否可控 |

### 负控判读

- 正控成功、负控失败：继续确认差异能否归因到安全边界。
- 正控和负控都成功：可能是正常功能、权限本来允许或测试设计错误，不能 technical_confirmed。
- 正控和负控都失败：可能路径不通、payload 不适配、防护有效或观察点错误。
- 缺负控：不得高置信 technical_confirmed。
- 标识符获取负控证明 attacker 拿不到必要 ID：不得写稳定越权；若代码、接口和运行态均排除获取路径，可 rejected，否则降级为 `candidate` 或 `blocked`。
- token/cookie 隔离负控失败：多主体 claim 无效，必须重建账号对象矩阵。

## technical_status 方法性判定边界

### technical_confirmed

必须同时满足：

- 原始扫描器结果已保存并与当前代码/运行版本对齐。
- 入口可达，route/handler/message/command 注册并启用。
- source 可控，攻击者条件和控制粒度明确。
- trace 人工闭合，非仅工具 path。
- sink 危险参数被污染，执行条件明确。
- transform/防护不足或被强正控绕过。
- 强正控证明真实安全影响。
- 负控成立。
- 若 claim 依赖对象标识符，`EVID_IDENTIFIER_ACQUISITION` 证明攻击者获取路径，且声明范围不超过可获得规模。
- 若 claim 依赖多主体、多对象、跨租户、跨角色、owner/victim 或清理动作，`EVID_ACCOUNT_OBJECT_MATRIX` 完整证明账号用途、账号对象矩阵必要事实、主体 ID、tenant/workspace、role/scope、对象归属、token/cookie 隔离和清理责任。
- 清理/恢复完成或无副作用。
- `EVID_OFFICIAL_SECURITY_MODEL` 已裁决，官方安全模型不把该行为定义为预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation、受信任主体正常能力或 duplicate。
- 如果该结论要进入报告或对外提交，本 Skill 只提示需要外部门禁裁决；是否可主提交由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决。
- Allowed Claims 与证据一致，Forbidden Claims 已列出。

### candidate

适用：

- 静态证据较完整，但缺运行态、强正控、负控、日志或影响证明。
- scanner path 有价值，但人工 trace 仍缺中间跳。
- source/sink 明确，但防护是否有效未知。
- 只有已知 ID、工具样本 ID、手工样本 ID、管理员视角 ID、截图 ID 或历史报告 ID 后可利用，尚未证明攻击者如何获得。
- 单个样本 ID 可疑，但批量、全量、任意对象、所有用户、所有租户或跨工作区声明缺规模证据。
- 多账号步骤存在，但账号对象矩阵缺账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 隔离或清理责任。
- 技术证据较强，但官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 未读完，尚不能决定是否具备对外提交资格。
- SCA 调用点可疑，但漏洞条件未触发。
- secret 可能暴露，但有效性、权限或轮换未知。
- DAST 差异存在，但未排除缓存、随机、限流或错误页。

candidate 必须写补证路线，不得写成漏洞成立。

### blocked

适用：

- 必须运行配置、账号、对象、租户、日志、OOB、浏览器、队列、构建产物或清理能力才能判断。
- scanner 的 reachable/validated 依赖运行态，但原材料不足。
- 必须运行态确认标识符是否能由攻击者从列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列或批量接口获得。
- 必须运行态确认账号对象矩阵、对象归属、token/cookie 隔离、role/scope、tenant/workspace 或清理责任。
- fixed/removed 需要复测才能确认修复。
- 动态调用、DI、AOP、feature flag、插件启用状态无法静态确认。
- 必须读取官方 SECURITY、scope、默认配置、权限/对象/租户模型、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 或 report quality 资料后，才能判断对外提交资格。

blocked 不是 rejected；必须写缺什么。

### rejected / false positive

只有有明确证据才 rejected：

- 文件为测试/示例/未部署，或 route 未注册。
- source 不可控、被服务端覆盖或只来自可信配置。
- sink 不危险、参数位置错误或不可达。
- 同变量、同路径、同上下文防护有效。
- 版本未加载、组件不可达、漏洞条件不满足。
- secret 是占位符、测试值、已吊销、权限不足或攻击者不可获得。
- 攻击者无法获得漏洞成立所需对象标识符，且已排除列表、详情、搜索、导出、日志、关系链、历史请求、分享页、客户端状态、可预测序列和批量接口等获取路径。
- 多主体边界被证伪：实际同一 token/cookie、对象公开、权限本来允许、attacker 就是 owner，或账号角色混淆。
- 官方安全模型明确这是预期功能、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate，且当前证据没有证明新主体、新对象、新默认配置、新影响层级或官方缓解绕过；若技术现象仍真实存在，应写 `需要外部门禁裁决` 或内部加固建议，而不是新漏洞 technical_confirmed。
- DAST 差异来自缓存、随机、限流、错误页、WAF。
- finding 完全重复且没有新入口、新主体、新对象、新版本、新影响。

rejected 模板：

```text
Status: rejected
Reason: not-reachable / not-controllable / protected / no-impact / test-only / duplicate / version-not-used / invalid-secret / fixed-with-retest
Evidence:
Allowed Claims:
Forbidden Claims:
Scanner delta:
```

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

### 不要只让扫描器安静

修复目标是消除安全根因，不是让规则不再命中。只有在明确误报时，才调整规则、ignore 或 suppression；且必须写清证据。

### 按结果状态写建议

- `technical_confirmed`：写代码修复、配置修复、默认值修复、回归测试和扫描器复测。
- `需要外部门禁裁决`：写内部修复、加固、规则优化、补官方材料或收缩声明；不得写对外提交结论。
- `candidate`：写补证路线和临时加固，不要求大规模重构。
- `blocked`：写需要的账号、对象、日志、环境、构建产物、清理能力。
- `rejected`：写误报依据，可建议规则调优、ignore 理由或注释说明。

### 按漏洞族写建议

- SQL/NoSQL/LDAP/XPath：参数化、结构化 builder、动态字段 allowlist、禁止 raw fragment、回归注入负控。
- 命令执行：不用 shell，固定命令和参数数组，allowlist 子命令，最小权限，命令输出负控。
- SSRF：协议/域名/端口 allowlist，解析后 IP 校验，重定向后重校验，metadata 阻断，出网隔离。
- XSS/SSTI：上下文编码，避免 raw/safe，模板自动转义，CSP 补充，浏览器执行回归。
- 文件/上传/归档：canonicalize 后 base 约束，拒绝链接和特殊文件，随机文件名，不可执行目录，解压大小和数量限制。
- 鉴权/IDOR：服务端对象级授权、tenant 绑定、批量逐项校验、不要信任前端 owner/role。
- 标识符暴露链：列表、搜索、导出、分享页、日志、客户端状态、关系链、批量接口、对象签名和历史请求都要执行对象级授权；不可预测 ID 只能降低猜测概率，不能替代授权。
- 多主体/多租户：在 policy 层统一绑定 subject、tenant/workspace、role/scope 和 object owner；为 A/B 主体、A/B 对象、跨租户、批量数组、导出任务和异步消费添加回归测试。
- CSRF：所有状态变更 token，校验 Origin/Referer，覆盖 JSON/multipart/method override。
- Secret：轮换、吊销、清理历史、降低权限、迁移密钥管理、添加 push protection。
- SCA：升级安全版本；不能升级时关闭漏洞功能、加配置缓解、限制入口、确认运行包实际更新。
- IaC/container：最小权限、去特权容器、限制 hostPath/capability、网络隔离、认证/TLS、验证实际部署。

### 修复后复核

- 重放强正控和负控，而不是只看扫描器不再报。
- 确认正常功能未破坏。
- 确认依赖树、运行包、镜像、部署配置实际更新。
- 确认 secret 已轮换且旧值失效。
- 确认 ignore/suppression 有理由、范围和到期复查条件。

### 扫描器规则回归

当复核结论需要调整规则、ignore、suppression、query、pattern、sanitizer 或 severity 时，必须同时保留正例和反例：

- 正例：真实漏洞模式、危险参数、未防护路径、可达入口或已确认的测试样本仍应命中。
- 反例：参数化、allowlist、正确授权、不可达测试代码、占位符 secret、不可获得 ID、正常管理员能力不应误报。
- 规则修改后要记录 scanner delta：哪些原命中被保留、删除、合并、降级或新增；不得用宽泛 ignore 掩盖未修复风险。
- AI 生成的规则或修复建议只能作为草稿，必须由人工用代码语义、正反例和运行态证据复核。

## 禁止事项

- 禁止 scanner-only technical_confirmed。
- 禁止 external-tool-only technical_confirmed。
- 禁止 sink-only technical_confirmed。
- 禁止 source-only technical_confirmed。
- 禁止 trace-only technical_confirmed。
- 禁止没有负控就写高置信 technical_confirmed。
- 禁止把扫描器 severity 当业务风险等级。
- 禁止把 reachable、validated、technical_confirmed valid、fixed、removed、ignored 直接当人工结论。
- 禁止把 AI triage、Autofix、assistant 建议当运行态证据。
- 禁止只看 200、500、callback、marker、error、reflect、version、regex。
- 禁止把框架默认防护当作无需复核的证据。
- 禁止把弱 payload 失败直接 rejected。
- 禁止把 callback-only SSRF 写成内网敏感访问。
- 禁止把 marker-only RCE 写成命令执行。
- 禁止把 error-only SQLi 写成数据读取。
- 禁止把 reflect-only XSS 写成浏览器执行。
- 禁止把拿不到对象归属的 IDOR 写成 technical_confirmed。
- 禁止把工具样本 ID、管理员样本 ID、截图 ID、历史报告 ID 或手工粘贴 ID 当作攻击者可获得路径。
- 禁止把 known-ID-only、single-ID-only 或 tool-ID-only 写成高价值 technical_confirmed。
- 禁止把一个对象样本外推为批量、全量、任意对象、所有用户、所有租户或所有工作区。
- 禁止账号对象矩阵缺账号对象矩阵必要事实、主体 ID、角色、对象归属、token/cookie 隔离和清理责任时写多主体 technical_confirmed。
- 禁止官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior 未裁决、accepted risk 未裁决或 范围或官方已知拒绝（外部裁决） 未裁决时写对外可提交。
- 禁止把 需要外部门禁裁决 写成“已确认可提交漏洞”。
- 禁止把官方预期功能、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate 当成新漏洞提交，除非证明新主体、新对象、新默认配置、新影响层级或官方缓解绕过。
- 禁止把 version-only SCA 写成组件漏洞可达。
- 禁止把 secret regex-only 写成有效凭据泄露。
- 禁止在报告中输出完整真实 secret、token、cookie、密码或可复用凭据。
- 禁止为了数量把低价值、无影响、范围外、hardening only 写成漏洞。
- 禁止把项目运行、部署、恢复、监控、调度、容器维护内容混入本 Skill。
- 禁止把个人机器环境信息、不可公开编号、临时对话过程或专用平台词写进通用 Skill 正文。
- 禁止越出授权范围、测试第三方真实系统、读取真实生产用户数据、泄露真实凭据或执行不可清理验证。

## 自检清单

### 扫描器材料

- [ ] 是否读取原始 SARIF/JSON/HTML/CSV/平台导出，而不是只看截图或摘要？
- [ ] 是否记录工具、版本、规则 ID、CWE、severity、confidence、扫描范围、commit、配置？
- [ ] 是否区分扫描器原始状态和人工复核状态？
- [ ] 是否记录 locations、related locations、codeFlows/threadFlows、fingerprint 或请求响应？
- [ ] 是否说明 fixed/removed/ignored 的真实含义，而不是直接当修复？

### 入口与可达性

- [ ] 是否定位 route/handler/message/command/webhook/queue/cron？
- [ ] 是否确认入口在当前 profile、feature flag、插件、路由缓存和部署配置下启用？
- [ ] 是否排除测试、示例、fixture、mock、生成代码和未部署目录？

### Source / Trace / Sink

- [ ] 是否确认 source 字段、绑定位置、控制主体、控制粒度？
- [ ] 是否判断攻击者最低权限和对象/租户条件？
- [ ] 如果 source 或利用链依赖对象 ID、URI、object key、token、lookup handle 或 physical table，是否证明攻击者获取路径和可获得规模？
- [ ] 是否区分了攻击者自然获得、工具样本、手工样本、管理员视角、截图、历史报告和未知来源？
- [ ] 是否手写人工 trace，而不是只复制工具 path？
- [ ] 是否记录每一跳 file:line、变量、函数、分支和权限？
- [ ] 是否确认 sink 危险参数位置，而不是只看函数名？

### 防护与误报排除

- [ ] sanitizer/validator/escape/allowlist/parameterization 是否同变量、同路径、同上下文？
- [ ] 框架默认防护是否真实启用，是否被 raw API 绕过？
- [ ] 是否记录 scanner 准确点、漏判点、过度声明点？
- [ ] 是否排除不可达、不可控、防护有效、版本未使用、secret 无效？

### 动态验证与最高危害

- [ ] 是否设计 baseline、强正控和负控？
- [ ] 是否避免停在 callback-only、error-only、marker-only、reflect-only、version-only、regex-only？
- [ ] 越权/未授权/IDOR 是否证明标识符获取链，而不是只改一个已知 ID 看响应？
- [ ] 批量、全量、任意对象或跨租户声明是否证明 ID 可批量、持续、枚举、列表、搜索、导出、关系链或可推导获得？
- [ ] 多主体、多对象或 owner/victim 验证是否有账号对象矩阵、账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 隔离和清理责任？
- [ ] 是否在授权可重置环境中追到当前可证明最高影响？
- [ ] 是否写清停止继续升级原因？
- [ ] 是否记录请求、响应、日志、副作用、清理或恢复？
- [ ] 缺运行态时是否降级为 candidate 或 blocked？

### 结论与报告

- [ ] technical_confirmed 是否同时满足 route、source、trace、sink、transform、强正控、负控、清理和安全模型？
- [ ] technical_confirmed 是否已经和 对外提交资格 分层，避免把技术强验证自动等同于可提交漏洞？
- [ ] 如果要写对外可提交，是否具备 `EVID_OFFICIAL_SECURITY_MODEL` 并裁决 scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决）？
- [ ] 如果官方模型 unknown 或阻塞，是否写成 需要外部门禁裁决、candidate 或 blocked，而不是强漏洞声明？
- [ ] 依赖 ID 的 technical_confirmed 是否同时满足 `EVID_IDENTIFIER_ACQUISITION`？
- [ ] 多主体 technical_confirmed 是否同时满足 `EVID_ACCOUNT_OBJECT_MATRIX`？
- [ ] candidate 是否写清补证路线？
- [ ] blocked 是否写清缺账号、对象、日志、环境、构建或清理能力？
- [ ] rejected 是否有明确否定证据？
- [ ] 是否写 Allowed Claims 与 Forbidden Claims？
- [ ] 是否提供具体修复建议和回归验证？
- [ ] 是否按非账号类敏感材料展示边界处理所有 secret、token、cookie、密码和个人敏感信息，且没有删除复现所需凭据链？
- [ ] 是否把 known-ID-only、tool-ID-only、single-ID-only、截图 ID、历史报告 ID 或管理员样本 ID 降级？
- [ ] 是否禁止单对象样本外推批量/全量/任意对象？
- [ ] 是否禁止官方预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、hardening only、known limitation 或 duplicate 被包装成新漏洞？
- [ ] 是否去除个人机器环境信息、不可公开编号、临时对话过程和专用平台词？

检验句：**扫描器让我先看哪里；人工证据决定我能说什么；官方安全模型决定能不能对外提交。只要缺 route、source、trace、sink、impact、negative control、cleanup 或 security model 中任一关键项，就不能把工具结果写成 technical_confirmed；只要官方模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 未裁决，就不能写对外可提交。**
