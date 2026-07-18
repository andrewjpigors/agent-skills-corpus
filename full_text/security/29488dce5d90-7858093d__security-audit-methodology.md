---
name: security-audit-methodology
description: Use when planning, coordinating, or reviewing evidence-first security code audits, vulnerability hunting, scanner triage, exploitability review, or report verification across a repository before selecting language-specific or vulnerability-specific skills.
---

# 安全审计总方法论

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态；提交资格只属于 finding，不裁决整个 case 完成。
- case 完成只由 `validators/案例完成门禁校验.py` 及 `evidence/完成门禁校验结果.json` 或等价机器输出裁决；本 Skill 不手写完成通过。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

本 Skill 是通用安全代码审计的总入口。它不替代语言专项、漏洞类型专项、动态验证专项或报告复核专项，而是先建立统一的审计骨架：范围、入口、Source、Sink、Trace、Transform、运行态证据、负控、四则条件、高危面覆盖、最高影响、缺失证据 backlog、声明边界、赏金资格和机器完成门禁。

使用时按三步走：

1. **先建地图**：确认目标范围、语言/框架、入口类型、官方安全模型、权限模型、对象/租户/标识符边界、运行方式、可用测试账号、可观察日志和可重置能力。
2. **再建证据链**：每条疑似漏洞都必须从入口可达、Source 可控、Trace 闭合、Transform 判断、Sink 参数、动态正控、负控和影响证明逐项推进。
3. **最后定声明**：根据证据上限裁决 `technical_confirmed / candidate / blocked / rejected`，并写清四则条件、允许声明、禁止声明、停止继续追踪原因、缺失证据、是否阻断 finding 提交、是否阻断 case 完成和修复建议。

适用场景：

- 刚开始审计一个陌生仓库，需要统一范围、入口覆盖、证据门槛和后续专项路由。
- 扫描器、其他模型/工具、历史报告、日志片段或人工笔记给出候选，需要转成人工可复核任务。
- 一条发现准备从“可疑”升级为“已确认”，需要检查是否缺 route、source、trace、sink、强正控、负控或影响证明。
- 一份漏洞报告需要复核是否能支撑其标题、等级、影响范围、复现步骤和修复建议。
- 多个语言、多个框架或多个漏洞类型混在一起，需要一个不偏语言、不偏漏洞族的总裁决方法。

不适用场景：

- 项目部署、容器编排、监控、恢复、调度、CI 运维或漏洞平台运营。
- 只需要某个单一漏洞族的深度 payload、绕过技巧或修复细节；此时应转到对应漏洞类型 skill。
- 只需要某个语言/框架的路由、ORM、模板、权限模型细节；此时应转到对应语言专项 skill。
- 没有代码、配置、运行态材料或测试授权，却要求直接写 `technical_confirmed`。

每次使用本 Skill，至少输出一种可复核产物：

- 审计范围与入口覆盖矩阵。
- 官方安全模型、对象模型和声明边界摘要。
- Source→Sink trace 表。
- 候选发现清单与状态裁决。
- 动态验证计划与正控/负控设计。
- 最高影响追踪表。
- 高危面覆盖矩阵和缺失证据 backlog。
- 报告复核结论或应写入 evidence 的报告素材。

## 核心原则

### 1. 证据链优先

漏洞结论必须来自证据链，而不是来自单个现象。完整链路至少包含：

```text
入口可达 → Source 可控 → 参数绑定清楚 → Trace 闭合 → Transform/防护判断真实 → Sink 危险参数被污染 → 官方安全模型确认边界 → 强正控证明影响 → 负控排除误报 → 最高影响追踪 → 声明边界
```

以下内容只能作为线索，不能单独作为 `technical_confirmed`：

- 扫描器告警、SARIF、SAST/DAST/SCA severity。
- 其他模型/工具的“已验证”“可利用”“高危”自述。
- 单个危险函数名、单个 sink、单个 source。
- HTTP 200、错误页、异常栈、版本命中、回显 marker、OOB callback。
- 没有对象归属对照的 IDOR、没有最终目标差异的 SSRF、没有浏览器执行的 XSS、没有执行语义的 RCE。

四则条件是证据链进入 validated / bounty_submit_ready / finding_submit_ready 的硬门禁：攻击者条件、服务端条件、真实安全影响、项目安全模型违反必须同时落入 `evidence/证据链.json` 与 `evidence/赏金资格.json`；缺任一项时必须进入 `evidence/缺失证据.json`，并标明 `blocks_finding_submit` / `blocks_case_completion`。

### 2. 默认授权实验强验证

默认在自有 Docker、CTF、靶场、本地、隔离预发、测试租户或其他明确授权、可观察、可回滚环境中工作。在这种环境内，不要因为 payload “看起来强”就停在弱证明；应尽量证明真实安全价值。

允许在授权可重置环境内使用：

- 受控数据读取、受控写入、受控批量操作。
- 受控删除/覆盖、受控持久化、受控文件读写。
- 受控命令输出、受控回连、受控内网 canary、最小资源压力曲线。
- A/B 用户、A/B 对象、跨租户测试对象、测试 secret、测试 token、测试文件、测试表。

真正边界是：

- 不越出授权范围。
- 不测试第三方真实系统。
- 不读取、输出、传播真实用户数据。
- 不复用、泄露、深入利用真实生产凭据。
- 不执行不可清理、不可回滚、不可解释的副作用。
- 没有测试账号、对象、日志、快照、重置或清理能力时，不把结论写成 `technical_confirmed`。

### 3. 最高影响不是夸大，而是证据上限

审计目标不是停在最低触发，而是在可控范围内追到最高可证明影响：

- SQLi：从错误到布尔/时间/常量/测试数据读取/受控写入。
- SSRF：从 callback 到最终 URL、重定向后目标、内网 canary、响应可读性、状态改变。
- RCE：从 marker 到命令输出、执行身份、工作目录、受控文件、环境边界。
- XSS：从反射到浏览器执行、DOM/存储传播、目标角色触发、同源能力。
- IDOR：从换 ID / 已知 ID 到标识符获取链、账号矩阵、对象归属、跨用户/跨租户、敏感字段、越权写/删/导出；批量声明必须证明 ID 可批量获得。
- 文件类：从路径可控到 resolved path、base 逃逸、内容读取、写后可访问、覆盖/执行/二次解析。

如果不能继续升级，必须写停止原因：越出授权范围、缺环境、缺对象、缺日志、缺快照、负控阻断、防护有效、技术边界、影响已达当前测试上限。

每个未证明但可疑的更高影响必须进入 `evidence/最高影响证明.json` 的 `higher_impact_closures[]`。`maximum_impact_status=satisfied_for_current_claim` 只能表示当前声明边界足够，不表示全案完成；RCE、SSRF、文件写入、模板写入、反序列化、账号接管、权限提升、敏感数据、批量、跨站点、跨租户等方向没有闭环时，必须写缺失证据或排除证据。

### 4. 负控用于增强结论，不用于削弱验证

负控不是“保守不测”，而是让正控更可信。每个 `technical_confirmed` 至少应有一个能排除误报的对照：安全值、无权限主体、他人对象、其他租户、移除关键字段、修复后配置、合法目标与非法目标、无回连与有回连、布尔真与布尔假、时间差与无时间差。

### 5. 状态分级必须诚实

- `technical_confirmed`：证据链闭合，强正控和负控成立，影响与边界清楚。
- `candidate`：静态证据或弱运行态证据支持继续追，但缺关键证明。
- `blocked`：代码链路可疑，但缺账号、对象、配置、日志、运行版本、可观察副作用或可重置环境。
- `rejected`：存在明确排除证据，例如不可达、不可控、防护有效、影响不成立或版本不适用。

不要把 `candidate`、`blocked`、`pending`、`likely`、`scanner-technical_confirmed` 写成 `technical_confirmed`。

`validated` / `bounty_submit_ready` / `finding_submit_ready` 也不得冒充 `case_audit_complete`。单个 finding 可提交只说明该 finding 在当前声明边界内可提交；全案完成必须经过主链产物、四则条件、高危面覆盖、最高影响闭环、缺失证据阻断、声明边界语义、报告占位符和机器完成门禁。

### 6. 标识符获取链和账号矩阵是多主体漏洞的硬门槛

凡是漏洞结论依赖 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、`uri`、物理表名、分享 token、lookup handle 或其他对象标识符，都必须先回答：攻击者如何获得这些标识符。

- 单对象结论：必须证明该 ID 来自攻击者自身可达路径，例如列表、详情响应、搜索、导出、日志、关系链、分享页或可推导序列；结论只能写到该对象或同类可获得对象。
- 多对象 / 批量 / 广义结论：必须证明 ID 能批量、持续、枚举、列表式、搜索式、导出式、日志泄露式、关系链式或可推导式获得。
- 拿不到 ID：不能把“已知 ID 后可利用”写成高价值 `technical_confirmed`；通常只能写 `candidate`、`blocked` 或 `rejected`。
- 管理员手工给出的 ID、聊天上下文里的 ID、旧附件里的 ID、报告作者笔记里的 ID，只能作为定位样本，不能算攻击者可获得路径。

凡是结论依赖登录态、多账号、多对象、owner/victim、低权限/高权限、跨租户或清理动作，内部复核材料必须有账号矩阵：账号用途、用户名或邮箱、账号对象矩阵必要事实、user_id、tenant/workspace、role/scope、token/cookie 引用、对象归属和清理责任。报告阶段按唯一模板渲染可复现所需账号对象矩阵事实，不写本地路径、项目私有路径或内部编号，但内部材料不能缺复现所需的授权测试账号（以账号对象矩阵模板为准）和账号对象矩阵必要事实。

### 7. 官方安全模型决定漏洞边界

代码链路能触发不等于一定是漏洞。每条候选都必须对照官方资料、目标规则或等价设计材料，回答该行为是否违反被承诺保护的安全边界：

- 官方资料包括 SECURITY、安全公告、README、配置文档、API 文档、权限模型、release notes、known issues、scope/rules、官方 issue/discussion 和默认部署材料。
- 如果官方定义管理员、owner、插件作者、脚本作者、部署者或沙箱内代码为受信任主体，必须证明当前 finding 跨越了更低权限、跨主体、跨租户、跨沙箱、跨网络、跨文件或 secret 边界。
- 如果官方只承认 URL fetch、webhook、模板渲染、插件执行、导入导出或沙箱执行是功能，必须证明额外 CIA 影响、官方缓解绕过或新边界。
- 安全模型 unknown、scope unknown、默认配置 unknown、版本边界 unknown 时，不得写 technical_confirmed 或对外提交。

检验句：**如果删掉工具名、扫描器等级、外部模型/工具结论和第三方文章，只保留官方安全模型、代码链路、运行态强证据、负控和清理记录，当前声明还能成立吗？**

### 8. 高危面覆盖与 skill 产物反证

总方法论必须驱动 `evidence/覆盖矩阵.json` 的 `high_risk_surface_matrix`。至少逐项覆盖或说明缺口/排除证据：

```text
鉴权与越权、文件读取、文件写入、文件上传、归档解压、模板渲染、SSRF、命令执行、代码执行、XXE、反序列化、配置密钥、日志泄露、任务调度、组件漏洞
```

命中 sink、入口、依赖、配置或语言特性后，应触发对应漏洞族或语言专项 skill。skill 台账写“已读/已应用”后，必须在覆盖矩阵、候选发现、证据链、缺失证据、最高影响证明、声明边界或赏金资格中留下对应结果。没有产物反证时，skill 使用记录只能 partial / missing，并阻断 case 完成。

### 9. Forbidden Claims 不是停止探索理由

Forbidden Claims 只限制当前报告能说什么，不能关闭审计方向。当前不能声明 RCE、SSRF、文件写入、账号接管、跨租户等高危影响时，必须判断它们是：

- 已排除：有排除证据，写入声明边界和最高影响闭环。
- 未证明：写入缺失证据和 `higher_impact_closures[]`。
- 被阻断：写明阻断原因、解除条件和是否 `blocks_case_completion`。

不得用一句“报告不得声明 X”替代高危面覆盖、最高影响闭环或缺失证据 backlog。

## 通用 code-audit 方法契约

本 Skill 吸收通用代码审计方法，但不吸收历史 payload、webshell、绕过细节、自动 exploit 或真实目标材料。执行时必须把方法落到正式产物：

1. **控制缺失模型**：先定义敏感操作，再列应有控制、实际控制、缺失/绕过控制。`control_gap_status` 不是 `gap_confirmed` 时，不得写 confirmed。
2. **Source→Binding→Guard→Flow→Sink→Trigger→Effect→Negative→Clean→Claim**：按顺序闭合；缺 Guard、Effect、Negative 或 Clean 时只能 blocked / partial。
3. **Actor×Action×Resource**：每个授权 claim 必须有主体、动作、资源、应有权限、实际结果和证据引用。
4. **CRUD 与敏感操作覆盖**：不能只测命中的 update/read；要记录 create/read/update/delete 和项目相关配置写入、文件写入、权限变更、执行、导入导出等动作的覆盖或排除依据。
5. **业务状态机**：对安装、初始化、发布、审批、启停、导入导出、附件、模板、配置、任务、账号等流程，记录状态、迁移、前置条件、不变量和 guard。
6. **分层验证**：static_candidate → reachable → controllable → guard_gap_or_bypass → triggerable → effect_observed → negative_control_passed → cleanup_done → claim_allowed；任何关键层 false 都必须写 `current_blocker` 和缺失证据。

落点：`evidence/证据链.json` 的 `source_guard_flow_sink`、`control_gap_analysis`、`actor_action_resource`、`validation_ladder`，以及 `evidence/覆盖矩阵.json` 的 `actor_action_resource_coverage`、`crud_coverage`、`business_state_machine_coverage`。

## 审计目标

一次高质量安全代码审计应回答以下问题：

1. **范围是否清楚**：审计对象、版本、配置、部署形态、测试账号、测试对象、授权边界是什么。
2. **入口是否覆盖**：HTTP、GraphQL、WebSocket、RPC、CLI、webhook、queue、cron、event、file import、plugin hook 是否枚举。
3. **Source 是否可控**：攻击者、低权限用户、外部服务、二次污染源或存储数据是否能控制输入。
4. **Sink 是否危险**：危险语义是什么，危险参数位置在哪里，执行条件是什么。
5. **Trace 是否闭合**：参数是否从 source 经绑定、转换、分支、权限、防护到达 sink。
6. **Transform 是否有效**：参数化、白名单、escape、canonicalize、parser 配置、鉴权、CSRF、模板自动转义是否真实作用于当前变量和上下文。
7. **运行态是否证明影响**：响应、日志、副作用、回连、浏览器执行、数据库/文件/队列/缓存状态是否能证明安全影响。
8. **负控是否排误报**：正控差异是否由漏洞条件导致，而不是缓存、权限本来允许、错误页、WAF、随机值或工具误报。
9. **最高影响是否追够**：是否从低层触发继续追到当前环境可证明的最高影响。
10. **报告声明是否克制**：标题、等级、影响、范围、复现和修复建议是否小于等于证据。
11. **标识符是否可获得**：若影响依赖 ID、对象 handle 或租户标识，是否证明攻击者获得路径，是否区分单对象、多对象、批量和广义声明。
12. **账号矩阵是否可复核**：若影响依赖多主体，是否记录账号、账号对象矩阵必要事实、主体 ID、租户、角色、token/cookie 引用、对象归属和清理责任。
13. **官方模型是否支持声明**：是否读过安全策略、权限模型、范围、默认配置和 known risk；是否区分新漏洞、预期功能、accepted risk、hardening only、范围或官方已知拒绝（外部裁决） 和 对外提交资格。
14. **高危面是否覆盖**：是否逐项覆盖高危面，未覆盖项是否写入缺失证据或排除证据。
15. **完成门禁是否机器通过**：是否运行完成门禁并引用机器结果；是否没有把 finding 可提交写成 case 完成。

## 输入材料

开始审计前，尽量收集以下材料；缺失项必须写进缺口，不能脑补。

### 代码与入口材料

- 路由定义：注解、attribute、decorator、路由文件、资源路由、自动路由、通配符、fallback、GraphQL schema、RPC/SOAP、WebSocket gateway。
- Handler 层：Controller、Action、Handler、Resolver、Servlet、Endpoint、View、server action、插件 hook callback。
- 中间层：Middleware、Filter、Interceptor、Guard、Policy、Gate、CSRF、CORS、body parser、upload parser、tenant resolver、exception handler。
- 业务层：Service、UseCase、Manager、Domain service、Command handler、Job、Listener、Subscriber、Worker。
- 数据与资源层：DAO、Repository、Mapper、Model、Entity、Query builder、ORM scope、HTTP client、filesystem、object storage、cache、queue、template、parser、deserializer。

### 配置与依赖材料

- 依赖清单、lockfile、构建脚本、实际打包版本、运行镜像、feature flag。
- 安全配置：认证、授权、CSRF、CORS、安全头、session/cookie、JWT/OAuth/SAML、模板自动转义、debug/error page。
- 数据配置：数据库权限、ORM 方言、Mapper XML、multi-tenant filter、soft delete/global scope、SQL logging。
- 文件与网络配置：upload directory、static mapping、object storage policy、archive import directory、proxy、DNS resolver、outbound allowlist。
- Parser 与执行配置：XML parser、JSON polymorphic typing、反序列化 allowlist、模板 sandbox、表达式语言、shell/path environment。

### 运行态与实验材料

- 请求/响应：method、URL、headers、cookies、body、文件字段、状态码、响应头、响应体、重定向链。
- 浏览器材料：页面路径、操作步骤、DevTools Network/Console/DOM/Storage、Burp 记录。
- 日志与副作用：访问日志、应用日志、鉴权日志、SQL/ORM 日志、HTTP 出站、DNS/回调、文件变化、数据库记录、缓存键、队列消息。
- 测试主体：匿名、低权限、无权限、不同租户、管理员测试账号、service account、测试 API key。
- 测试对象：自己对象 A、他人测试对象 B、跨租户对象 T、测试表、测试文件、测试 cookie、测试 secret canary、可删除上传文件。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 标识符材料：ID / handle / token / URI / object key / physical table 来自列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、历史请求、分享页、客户端状态、可预测序列还是批量接口；是否只能单对象获得，还是能批量、持续、枚举、搜索、导出、关系链式或可推导获得。
- 可重置能力：快照、回滚、清理命令、测试命名空间、临时目录、受控回连端点、metadata mock、内网 canary。

### 既有材料

- 扫描器结果、SARIF、SAST/DAST/SCA/Secret/IaC 报告。
- 旧漏洞报告、复测记录、误报记录、修复 commit、测试用例。
- 官方文档、安全公告、release notes、security policy、scope、known issue、expected behavior。
- 官方对象模型、权限模型、默认配置、accepted risk、范围或官方已知拒绝（外部裁决）、report quality rules 和已知风险基线。
- 完成门禁材料：`evidence/完成门禁校验结果.json` 或等价机器输出、报告占位符扫描结果、阻断项和 warnings。

## Source 识别

Source 识别必须同时回答四个问题：来源是什么、谁能控制、控制粒度多大、如何进入代码。

### HTTP Source

检查：

- query：search/filter/sort/order/page/limit/id/returnUrl/callbackUrl/path/key/url/host。
- path：path variable、slug、通配符、正则捕获、文件扩展、locale/tenant segment。
- body：form、JSON、XML、GraphQL variables、protobuf、multipart 字段、数组、嵌套对象、批量列表。
- header：Authorization、Host、Origin、Referer、X-Forwarded-*、Content-Type、User-Agent、自定义业务 header、签名 header。
- cookie：session、remember-me、偏好设置、tenant、locale、JWT cookie、非 HttpOnly 业务 cookie。
- multipart：文件名、Content-Type、文件内容、magic bytes、压缩包 entry、伴随表单字段。

### 非 HTTP Source

不要漏掉：

- GraphQL operation、resolver 参数、mutation input、fragment、alias、directive、batch query。
- WebSocket message、channel、topic、room、事件 payload。
- CLI 参数、stdin、环境变量、导入文件、批处理参数。
- webhook、OAuth/OIDC/SAML claim、支付/消息/仓库回调。
- queue message、event bus payload、cron 读取的数据库记录、工作流表单。
- CSV/Excel/XML/JSON/YAML/ZIP/TAR/office 导入内容、文件名和压缩包 entry。
- 用户可编辑模板、表达式、规则、报表字段、自动化工作流配置。

### 身份与二次污染 Source

不要默认信任这些字段：

- session 中的 user_id、tenant_id、role、permission、csrf token。
- JWT/OAuth/OIDC/SAML claim：sub、aud、iss、exp、nbf、scope、groups、tenant、email、role。
- 反向代理传入的用户头；必须确认只有可信代理能设置。
- 前端传入的 owner_id、role、tenant_id、permission；默认服务端应重算。
- 数据库存储值、缓存值、对象 metadata、队列消息；必须追写入入口和读取触发主体。

Source 记录模板：

```markdown
| Source | 类型 | 进入位置 | 控制主体 | 控制粒度 | 绑定变量 | 二次污染链 | 证据 | 结论 |
|---|---|---|---|---|---|---|---|---|
| `{field}` | query/body/header/... | `{file:line}` | 匿名/低权限/... | 完全/条件/枚举/片段 | `{var}` | 写入→读取→sink | 代码/请求 | full/conditional/none |
```

## Sink 识别

Sink 不是 API 名清单，而是“危险语义 + 危险参数 + 执行条件 + 可证明影响”。记录时必须说明哪个参数危险、为什么危险、当前 source 是否污染该参数。

### 常见 Sink 家族

- 注入类：SQL/HQL/JPQL/NoSQL/LDAP/XPath/Cypher/Gremlin/Redis key/query/filter/update/raw expression。
- 执行类：系统命令、动态代码、表达式语言、模板编译、反射调用、脚本引擎、workflow expression。
- 文件类：读取、写入、重命名、复制、删除、上传保存、下载、预览转换、对象存储 get/put、归档解压。
- 解析类：XML、YAML、JSON polymorphic、反序列化、office/image/PDF 转换、压缩包 entry 处理。
- Web 输出类：HTML body、attribute、JavaScript、CSS、URL、JSON-in-HTML、Markdown/rich text、DOM sink、SSR hydration。
- 网络类：SSRF、HTTP client、URL fetch、proxy、metadata client、image/PDF previewer、webhook forwarder。
- 权限类：对象查询、批量更新/删除、导出、审批、角色变更、tenant filter、policy/gate/ACL。
- 状态类：CSRF 状态改变、cache key、queue publish、topic/routing key、workflow dispatch。
- 配置/密钥/日志类：secret 读取/写入、签名校验、加密解密、日志输出、debug error、依赖加载。

Sink 记录模板：

```markdown
| Sink | 调用点 | 危险参数 | 参数来源 | 执行条件 | 防护点 | 最高可证明影响 | 证据 |
|---|---|---|---|---|---|---|---|
| SQL/CMD/FILE/... | `{file:line API}` | 参数/字段/索引 | `{var}` | 分支/配置/角色 | 参数化/白名单/... | 读/写/执行/... | 代码/日志 |
```

## Transform / 防护检查

Transform 检查的核心问题是：防护是否作用在**同一个变量、同一个分支、同一个上下文、同一个 sink 参数**，并且早于危险动作生效。

### 参数化与查询防护

- 参数化必须覆盖用户值进入查询的位置；动态表名、列名、排序字段、排序方向、函数名、SQL 关键字不能靠值绑定保护。
- `prepare()` 不是自动安全；必须确认 SQL 模板中使用占位符，用户值通过 bind/execute 参数进入。
- ORM/Query Builder 一旦使用 raw/native/string interpolation/orderByRaw/whereRaw，就按 raw query 审计。
- NoSQL 必须防止用户对象整体进入 filter/update；拒绝 `$` 操作符注入，固定查询结构，schema 校验字段类型。

### 白名单、规范化与类型校验

- 白名单必须是允许列表，不是黑名单、不完整正则、`contains`、`startsWith`、`endsWith` 或字符串前缀错判。
- URL/path/file 判断必须先 decode/canonicalize/normalize/realpath，再做 base、scheme、host、port、IP、redirect 判断。
- 类型转换失败必须拒绝；如果失败后回退原字符串或默认危险分支，不能算防护。
- schema validation 要覆盖嵌套字段、数组元素、额外字段、批量接口、反序列化后的对象。

### Escape / Encode / Template

- escape 必须匹配上下文：HTML body、attribute、JavaScript string、URL、CSS、JSON、HTTP header、SQL、LDAP、shell 不能混用。
- 模板自动转义必须确认未使用 raw/unsafe 输出、未关闭 autoescape、未进入 script/style/URL 特殊上下文。
- shell escape 不能替代结构化参数；命令名、参数、路径、工作目录、环境变量要分别固定或白名单。

### 权限、CSRF、会话、日志

- 鉴权要区分认证、角色授权、对象级授权、租户边界、数据权限、业务状态权限。
- 权限检查必须在读取/写入/执行前生效；controller 层检查不能替代批量对象逐项授权。
- CSRF token 必须与 session 和状态改变绑定，覆盖 JSON、multipart、AJAX、method override 和早退分支。
- 日志风险必须证明敏感数据真实进入日志，且低权限主体能够读取或间接获得日志。

## 路由与调用链追踪

总方法论只要求建立可复核调用链；复杂框架细节应转到入口与调用链专项。

追踪步骤：

1. 枚举入口：HTTP、GraphQL、WebSocket、RPC、CLI、webhook、queue、event、cron、file import、plugin hook。
2. 匹配 handler：method/path/host/header/content-type/prefix/namespace/fallback/middleware/auth/handler。
3. 解析参数绑定：path/query/body/header/cookie/file/session/claim/DTO/VO/Model/FormRequest/Serializer。
4. 记录中间层：auth、role、tenant、CSRF、CORS、body parser、upload parser、schema validation、rate limit、exception handler。
5. 追业务层：handler → service/usecase/manager → repository/DAO/mapper/model/helper/client。
6. 处理动态调用：接口实现、依赖注入、反射、容器绑定、trait/mixin、decorator/AOP、magic method、插件注册表。
7. 处理异步链：producer → topic/queue/event name → consumer/listener → 参数对象 → sink。
8. 标注缺口：未解析实现、运行配置缺失、feature flag 不明、路由未注册、middleware 顺序未知。

每一跳记录格式：

```text
Level-N: {file:line} {class/function}.{method}({args})
输入变量: {sourceField} -> {localVar}
处理动作: decode/parse/validate/escape/canonicalize/auth/assign/call
分支条件: {condition}，进入/不进入下一跳依据
输出变量: {localVar} -> {nextArg}
下一跳: {file:line method}
证据: 关键代码片段或配置片段
缺口: 未解析实现/缺运行配置/缺测试数据
```

## 数据流追踪步骤

对每条候选路径按以下顺序执行，不得跳步：

1. 写入口请求样例：method、path、query、headers、cookies、body、文件字段、认证状态、唯一审计 marker。
2. 定位参数进入点：字段在哪个 `file:line` 被读取、绑定、反序列化或映射。
3. 记录绑定方式：request object、DTO、VO、Entity、Model、FormRequest、Serializer、数组、claim、session、queue message、file row。
4. 记录变量重命名：如 `request.query.name -> dto.name -> filter.keyword -> queryParam`。
5. 记录对象转换：字段复制、默认值、类型转换、getter/setter、model binder、ORM hydration。
6. 记录分支条件：if/switch/try/catch/return/throw、feature flag、角色判断、环境判断、空值保护、异常路径。
7. 记录 Transform：trim、decode、escape、schema validation、allowlist、regex、canonicalize、sanitize 是否作用同一变量。
8. 记录权限检查：认证、角色、对象级授权、tenant/owner 条件、policy/gate、middleware 是否覆盖当前分支。
9. 记录调用链：handler → service → repository/helper/client/model/mapper → sink。
10. 标出 sink 参数位置：危险调用点、参数名/索引、最终字符串/对象结构、执行条件。
11. 判断参数仍然可控：完全可控、条件可控、白名单内可控、被覆盖、不可控、未解析。
12. 判断防护是否足够：结合 sink 上下文，不写泛泛“已过滤”。
13. 设计强正控：选择能证明漏洞语义的 payload，不停留在无意义 marker。
14. 设计负控：只改变一个关键条件，排除正常行为和环境噪声。
15. 追最高影响：继续追读取、写入、越权、执行、服务端请求、文件越界、浏览器执行或组合链。
16. 裁决状态：technical_confirmed/candidate/blocked/rejected，并列依据、缺口、停止原因或排除证据。

参数可控性矩阵：

```markdown
| 参数/字段 | Source | 绑定变量 | 传播路径 | 覆盖类型 | 防护 | Sink | 可控性 | 可利用条件 | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| `{field}` | body/json/... | `{var}` | L1→L2→L3 | 无覆盖/条件覆盖/硬编码覆盖 | allowlist/... | SQL/CMD/... | 完全/条件/不可控 | 条件 | 审计/降级/排除 |
```

## 必检证据点

### 静态证据

- 路由证据：route/method/path/handler/middleware/auth/source 参数。
- Source 证据：字段来源、读取 API、绑定变量、控制主体、控制粒度。
- 参数绑定证据：DTO/Model/数组/对象属性/claim/session/queue/file row 映射。
- Trace 证据：每一跳 `file:line`、函数、变量名、分支、调用关系。
- Sink 证据：危险 API、危险参数位置、执行条件、影响语义。
- 防护缺口证据：参数化缺口、白名单缺口、escape 上下文错误、canonicalize 顺序错误、parser 配置缺失、上传策略缺失、签名/鉴权缺失。
- 鉴权缺失证据：无认证、仅认证、角色缺失、对象归属缺失、tenant 条件缺失、批量未逐项授权。
- 标识符获取证据：对象 ID、用户 ID、租户 ID、文件 ID、分享 token 或 lookup handle 的攻击者获取路径；单对象、多对象、批量和广义影响分别对应的证据。
- 账号矩阵证据：多主体、多对象、多租户发现中，attacker / owner / victim / control / cleanup 的账号对象矩阵必要事实、主体 ID、角色、租户、token/cookie 引用、对象归属和清理责任。
- 官方安全模型证据：官方资料阅读状态、角色模型、对象模型、标识符暴露位置、对象级授权要求、默认配置、scope、known risk 和对外提交限制。
- 版本/依赖证据：manifest、lockfile、实际打包、运行版本、组件启用配置、调用可达性。

### 运行态证据

- 动态请求证据：baseline、强正控、强化请求、负控请求、账号角色、前置数据、payload、环境说明。
- 响应证据：状态码、响应体关键片段、header、跳转、错误信息、时间差，并解释安全含义。
- 副作用证据：数据库变更、文件变化、服务端请求、DNS/HTTP 回调、缓存键、队列消息、对象存储对象、业务状态。
- 负控证据：安全值、无权限主体、其他对象/租户、无效对象、移除关键字段、允许/禁止目标对照、修复后对照。
- 日志证据：handler 命中、auth 决策、sink 执行、异常栈、SQL/ORM 日志、HTTP client 日志、审计日志。
- 影响证明：测试敏感字段、越权对象、真实写入、执行语义、文件边界、内网 canary、浏览器执行、持久化污染、资源边界。
- 清理证据：测试对象、测试文件、测试表、缓存、队列、上传/解压产物的清理动作和清理结果。

### 证据点 ID 建议

```markdown
| 类型 | 建议 ID | 必须映射到 |
|---|---|---|
| 路由 | EVID_ROUTE_MATCH | method/path/handler/middleware |
| Source | EVID_SOURCE_ENTRY | 输入字段、控制主体、进入位置 |
| 绑定 | EVID_PARAM_BINDING | request/DTO/Model/数组/属性映射 |
| Trace | EVID_TRACE_HOP_N | 第 N 跳 file:line、变量变化 |
| 分支 | EVID_BRANCH_EXECUTION | 分支条件与执行证据 |
| Sink | EVID_SINK_EXEC_POINT | 危险调用点与参数位置 |
| 防护 | EVID_GUARD_OR_SANITIZER | 参数化、白名单、escape、auth、parser 配置 |
| 标识符 | EVID_IDENTIFIER_ACQUISITION | ID 来源、获取主体、获取规模、单对象/批量边界 |
| 账号矩阵 | EVID_ACCOUNT_OBJECT_MATRIX | 主体、账号对象矩阵必要事实、角色、租户、对象归属、清理责任 |
| 官方模型 | EVID_OFFICIAL_SECURITY_MODEL | 官方资料、范围、预期行为、对象模型、known risk、声明边界 |
| 影响 | EVID_IMPACT_PROOF | 响应、日志、副作用、执行、越权、回连 |
| 负控 | EVID_NEGATIVE_CONTROL | 对照请求/用户/对象/参数/配置 |
| 清理 | EVID_CLEANUP_RESULT | 清理动作与清理后状态 |
| 版本 | EVID_VERSION_REACHABILITY | 版本、打包、启用、可达性 |
```

## 动态验证触发条件

以下情况若要升级为 `technical_confirmed`，通常必须动态验证：

- 影响依赖运行配置、feature flag、数据库方言、路由注册、middleware 顺序、组件启用状态。
- 漏洞类型需要观察副作用：越权、SQL/NoSQL 语义、SSRF、文件读写、上传可访问性、命令/代码执行、XSS 浏览器执行、CSRF、状态改变、缓存/队列污染、组件可达性。
- 防护是否生效取决于 runtime：template autoescape、parser factory、反向代理、session/cookie、CORS、安全头、object storage policy。
- 需要证明双主体、双对象、双租户差异。
- 需要证明攻击者如何从自身可达入口获得对象标识符，或证明批量/全量声明所需的标识符规模。
- 需要证明账号矩阵、对象归属、token/cookie 隔离、owner/victim/control/cleanup 边界。
- 需要证明官方安全模型是否承诺保护该边界，或当前 finding 是否只是 expected behavior / accepted risk / 范围或官方已知拒绝（外部裁决）。
- 扫描器、报告或外部模型/工具结论要升级 technical_confirmed。
- 已有低层触发，但需要继续确认最高影响。

可以先保持 `candidate` 的情况：

- 已有 source、binding、trace、sink，但缺运行环境、账号、对象 ID、日志、强正控或负控。
- 只有 known-ID-only、tool-ID-only、admin-sample-only、screenshot-ID-only、single-ID-only，尚未证明攻击者获取路径或可获得规模。
- 已证明危险构造存在，但执行分支、配置开关或防护覆盖未确认。
- 组件版本命中且代码引用存在，但缺打包/启用/触发路径。
- 存储型污染链写入端或读取端缺一段运行态证据。

必须降级为 `blocked` 或停止当前目标验证的情况：

- 目标不在授权范围，或会访问第三方真实资源、真实内网资产、真实云 metadata credential。
- 会读取、输出、复用真实 secret、token、cookie、密码、个人敏感信息。
- 没有测试账号、测试对象、测试租户、日志观察、快照/重置/清理方案。
- 验证链路已经越出当前测试边界。

## 授权实验模式下的强验证方法

强验证必须按“基线 → 正控 → 升级 → 负控 → 清理”组织。

### 通用请求框架

```text
1. baseline：使用正常参数确认业务路径、handler、auth、对象和日志。
2. positive：使用能证明漏洞语义的 payload，不只放无意义 marker。
3. escalation：正控成立后继续追最高影响，如测试数据读取、越权写、命令输出、内网 canary、浏览器执行。
4. negative：只改变一个关键条件，证明差异来自漏洞条件。
5. cleanup：删除测试数据、恢复测试对象、清空缓存/队列、移除测试文件，并记录结果。
```

### 代表性强验证方向

这些是方向，不是直接复制到第三方目标的命令；必须按授权范围、框架语义、数据库方言、字段上下文和清理能力调整。

```text
SQLi:
  从错误探测升级到布尔真/假、时间差、UNION 常量、测试表读取、可回滚测试写入。
  不读取真实用户表、真实密码、真实 token；使用测试表、canary、count、非敏感元信息。

NoSQL:
  验证操作符注入、对象整体进入 filter、update 条件绕过、聚合管道污染。
  负控包括固定 schema、拒绝 $ 操作符、合法 filter 与非法 filter 差异。

命令/代码执行:
  从 marker 升级到命令输出、执行身份、工作目录、受控文件、受控回连。
  不做不可清理持久化，不读取真实密钥；输出限制在测试文件和系统只读指纹。

SSRF:
  从公网 callback 升级到最终 URL、重定向后目标、内网 canary、metadata mock、响应可读性。
  不访问真实云 metadata credential，不扫真实内网；使用自建 canary 服务。

XSS:
  从反射升级到浏览器执行、DOM sink、存储传播、目标角色触发、同源能力边界。
  不窃取真实 cookie；使用测试 cookie、canary endpoint 和受控页面。

文件/路径/上传/归档:
  验证 normalize/realpath 后最终路径、base 逃逸、测试文件读取、受控写入、上传后访问/执行/二次解析。
  解压验证要逐 entry 检查最终路径，并记录清理结果。

IDOR/鉴权:
  先证明用户 A 如何从自身入口获得对象 B 的 ID / handle / URI / token；若只能靠手工样本，先降级。
  用户 A 操作对象 A 应成功；用户 A 操作对象 B 应失败；用户 B 操作对象 B 应成功。
  若用户 A 能读/写/删/导出对象 B，继续追账号矩阵、token/cookie 隔离、敏感字段、批量接口、租户边界和 owner 视角。
  批量/全量/任意对象声明必须证明 ID 可批量、持续、枚举、列表、搜索、导出或关系链式获得。
```

### Burp 与浏览器复现要求

- 用真实业务操作捕获 baseline，不手造未知协议细节。
- 在 Repeater 中复制 baseline、positive、escalation、negative 四组。
- 每次只改变一个关键变量；链式验证记录每一步依赖。
- 添加唯一审计 marker，便于日志、数据库、文件和回连检索。
- 同步观察服务端日志、数据库/缓存/队列/文件、OOB、浏览器 DOM/Console/Network。
- 保存原始请求响应和负控对照；不要只截图结果页。

## 最高危害追踪

对每条发现建立最高影响表：

```markdown
| 层级 | 问题 | 已证明证据 | 未证明内容 | 下一步 | 停止原因 |
|---|---|---|---|---|---|
| 可触发 | payload 是否改变行为 |  |  |  |  |
| 可控 | 是否控制关键语义 |  |  |  |  |
| 可读 | 是否读取测试数据/文件/对象 |  |  |  |  |
| 可写 | 是否写入测试记录/状态 |  |  |  |  |
| 可越权 | 是否跨主体/对象/租户 |  |  |  |  |
| 可执行 | 是否证明执行语义 |  |  |  |  |
| 可横向 | 是否越过网络/组件/隔离边界 |  |  |  |  |
| 可组合 | 是否能与其他缺陷组合 |  |  |  |  |
```

同时必须在结构化产物中建立 `higher_impact_closures[]`，逐项记录未证明高危方向、升级尝试、缺失证据、阻断原因、不能串联原因和 `blocks_case_completion`。自然语言最高影响表不能替代机器可校验字段。

常见停止原因写法：

- `out_of_authorized_scope`：继续会越出授权范围。
- `no_reset_or_cleanup`：缺快照、回滚或清理能力。
- `no_test_object`：缺可用测试对象或测试租户。
- `no_runtime_observability`：缺日志、副作用或回连观察点。
- `negative_control_blocks`：负控证明防护有效或权限阻断。
- `impact_already_max_for_environment`：已达到当前实验环境能证明的最高影响。
- `requires_real_user_data`：继续需要真实用户数据，必须停止。

## 负控设计

负控要与漏洞条件一一对应：

| 漏洞族 | 推荐负控 |
|---|---|
| SQL/NoSQL/LDAP/XPath | 正常参数、布尔真/假、时间/无时间、合法枚举、被拒绝操作符、参数化分支 |
| SSRF | 允许目标/禁止目标、外网/内网 canary、重定向前/后、DNS/IP 编码变体、安全配置对照 |
| XSS/模板 | 转义上下文、非执行 marker、raw/escaped 分支、目标角色触发、不同浏览器上下文 |
| 文件/路径/上传/归档 | base 内/base 外、合法/非法扩展、可访问/不可访问、符号链接、压缩包安全 entry |
| IDOR/鉴权 | 未登录、低权限、自己对象、他人对象、跨租户对象、标识符获取对照、账号矩阵/token 隔离、批量逐项授权、高权限对照 |
| CSRF | 带 token/不带 token、同源/跨站、JSON/multipart/AJAX、method override、安全 SameSite 对照 |
| 组件/SCA | 启用/未启用、可达/不可达、危险配置/安全配置、版本修复前/后 |
| Secret | 占位符/真实测试凭据、已吊销/未吊销、无权限/最小权限、hash 摘要/权限 metadata |

负控失败不等于漏洞不存在；要判断是 payload 错、条件错、环境错、防护生效，还是候选应降级。一个弱 payload 失败不得直接 `rejected`。

## technical_status 方法性判定边界

### technical_confirmed

同时满足以下条件才可写 `technical_confirmed`：

- 入口可达：route/handler/middleware/auth 证据明确。
- Source 可控：控制主体、控制粒度、绑定变量明确。
- Trace 闭合：source → binding → transform → branch/auth → service/repository/helper/model → sink。
- Sink 危险参数被污染：参数位置、执行条件、最终值/结构明确。
- 防护不足：现有防护为何不能阻断当前路径。
- 强正控证明真实影响：响应、日志、副作用、对象边界、文件边界、服务端请求、命令输出、浏览器执行、状态改变或组件可达。
- 若 claim 依赖对象标识符：有 `EVID_IDENTIFIER_ACQUISITION`，证明攻击者获取路径和可获得规模，声明范围不超过该规模。
- 若 claim 依赖多主体、多对象、跨租户、owner/victim 或清理复测：有 `EVID_ACCOUNT_OBJECT_MATRIX`，证明账号对象矩阵必要事实、主体 ID、对象归属、role/scope、tenant/workspace、token/cookie 隔离和清理责任。
- 若 claim 依赖安全边界解释：有 `EVID_OFFICIAL_SECURITY_MODEL` 或等价设计/范围证据，证明不是预期功能、accepted risk、hardening only 或 范围或官方已知拒绝（外部裁决）。
- 已追踪当前授权环境内的最高可证明影响，或写清停止原因。
- 未证明更高影响已进入 `higher_impact_closures[]`，且 missing / blocked 项已进入缺失证据。
- 负控成立：至少一个能排除正常行为或误报的对照；高风险结论通常需要多个负控。
- 清理完成或无副作用：写清测试数据恢复、文件删除、环境重置或无需清理。
- 声明边界清楚：不夸大影响，不省略前置条件。

### candidate

以下情况只能写 `candidate`：

- 有 source 和 sink，但中间调用链缺失。
- 有 trace，但参数可控性未证明。
- 有危险构造，但防护是否覆盖同一变量未判断。
- 有扫描器结果，但未定位 route/source/sink。
- 有组件版本命中，但未证明实际打包、启用、调用可达或输入可控。
- 有弱正控，但缺强正控、最高影响追踪或负控。
- 只有已知 ID、工具样本 ID、管理员样本 ID、截图 ID、历史报告 ID 后可利用，尚未证明攻击者如何获得。
- 单对象样本可疑，但批量、全量、任意对象、所有用户、所有租户或跨工作区声明缺可获得规模证据。
- 官方安全模型、范围、默认配置、known risk 或 对外提交资格 规则未读完。

### blocked

写 `blocked` 时必须列具体缺口：

- 缺测试账号、角色、token、CSRF 上下文、对象 ID、租户数据。
- 缺攻击者标识符获取链、账号对象矩阵、对象归属、token/cookie 隔离或 owner/victim 视角。
- 缺官方安全模型、scope、默认配置、known risk、accepted risk 或 report quality 资料。
- 缺真实配置、运行版本、feature flag、middleware 顺序、组件启用状态。
- 缺日志观察权限、数据库/缓存/文件/队列副作用观察权限。
- 缺受控外部回调域、DNS 记录、对象存储访问日志。
- 缺浏览器操作上下文、同源环境、真实表单或用户交互。
- 缺快照、重置或清理能力，无法安全执行高强度验证。

### rejected

只有具备排除证据时才写 `rejected`：

- route 不存在、未注册、不可触发。
- Source 不可控，或攻击者无法写入二次污染源。
- Trace 中断且有证据显示不会进入 sink。
- Sink 参数来自常量、白名单映射或服务端可信值。
- 防护对当前上下文有效，负控证明被阻断。
- 影响不成立：无测试敏感数据、无越权、无写入、无执行、无服务端请求、无跨边界。
- 攻击者无法获得必要对象标识符，且已排除列表、详情、搜索、导出、日志、关系链、历史请求、分享页、客户端状态、可预测序列和批量接口等获取路径。
- 多主体 claim 被证伪：同一 token/cookie、attacker 就是 owner、对象公开、权限本来允许或角色混淆。
- 官方安全模型明确该行为是预期功能、受信任主体正常能力、accepted risk、hardening only 或 范围或官方已知拒绝（外部裁决），且没有新边界。
- 漏洞前提错误：版本不符、组件未启用、部署配置不符、报告对象不属于当前代码。
- 多组强正控与负控无差异，且排除环境干扰、缓存、限流、WAF 和请求构造错误。

### 必须降级的场景

- scanner-only、external-tool-only、sink-only、source-only。
- 无 trace、无负控、只有 200、只有错误页、只有版本命中。
- callback-only SSRF、marker-only RCE、reflect-only XSS、error-only SQLi。
- 拿不到对象归属或攻击者标识符获取链的 IDOR、known-ID-only、tool-ID-only、single-ID-only、secret-regex-only、version-only SCA。
- 已证明低层触发但未追最高影响且没有停止原因。
- 未证明更高影响没有 `higher_impact_closures[]`。
- 四则条件缺失或未落入证据链/赏金资格。
- 高危面未覆盖且没有缺失证据或排除证据。
- 安全模型 unknown、scope unknown、默认配置 unknown、official known risk 未去重，却写对外可提交。

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 四则条件必须登记到 `evidence/证据链.json` 与 `evidence/赏金资格.json`。
- 高危面覆盖必须登记到 `evidence/覆盖矩阵.json`；未覆盖或未闭合项登记到 `evidence/缺失证据.json`。
- 最高影响闭环必须登记到 `evidence/最高影响证明.json` 的 `higher_impact_closures[]`。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证；完成通过必须引用机器完成门禁结果。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

修复建议必须具体到框架、调用点、配置和测试，不得只写“过滤输入”。

- 注入类：使用参数化绑定；动态表名、列名、排序字段、排序方向使用枚举映射；移除 raw 拼接；增加 DAO/Mapper 单元测试和集成测试。
- NoSQL：固定查询结构；拒绝操作符注入；对 filter/update 对象做 schema validation；不要把用户 JSON 原样传入查询。
- 命令执行：避免 shell；使用参数数组；固定命令名；参数白名单；固定工作目录和环境变量；最小权限运行。
- 模板/XSS：保持自动转义；禁止 raw；模板名和模板路径白名单；富文本使用可信 sanitizer；按 HTML/JS/CSS/URL/attribute 上下文编码。
- 文件路径：先 decode/canonicalize，再 normalize/realpath，再 base 约束；拒绝符号链接逃逸；不要用字符串前缀代替真实路径约束。
- 上传：服务端生成文件名；扩展名、MIME、magic bytes 多重校验；存储到 web 根外；禁执行；下载鉴权；限制大小；二次处理继续校验。
- 归档：逐 entry 归一化；拒绝绝对路径、`..`、链接和特殊文件；限制解压大小和文件数；解压后权限最小化。
- SSRF：scheme allowlist；DNS 解析后拒绝本地、内网、metadata、保留地址；重定向后重新校验；限制端口；记录出站审计。
- 鉴权/IDOR：默认拒绝；路由级、方法级、对象级授权同时覆盖；查询条件绑定当前主体和 tenant；批量接口逐项校验。
- CSRF：状态变更统一 token 校验；token 与 session 绑定；覆盖 JSON、multipart、AJAX、method override；SameSite 只作补充。
- XML/反序列化：禁外部实体、外部 DTD/Schema、XInclude 和网络访问；不要反序列化不可信数据；限制类型；关闭危险多态；签名并绑定上下文。
- Secret/日志：密钥移出仓库；最小权限；轮换泄露凭据；日志脱敏 token、cookie、password、secret、PII；限制日志访问。
- 依赖：升级到安全版本；确认实际打包版本；关闭危险默认配置；为可达调用点增加回归测试。

测试要求：

- 单元测试覆盖 sanitizer、白名单、权限判断、parser 配置、路径 canonicalize。
- 集成测试覆盖真实路由、middleware 顺序、对象级授权、CSRF、上传/下载、SQL/ORM 参数化。
- 权限矩阵覆盖未登录、低权限、对象拥有者、非拥有者、跨租户、高权限。
- 回归测试包含强正控和负控；修复后漏洞请求被阻断，正常请求仍可用。


## 全仓库耗尽式完成边界

当用户目标要求“字面意义全仓库完整审计”或“要么证明前台/宿主机 RCE，要么全仓库完整”时，本 Skill 的主审计骨架必须额外维护 `evidence/全仓库耗尽证明.json`。

硬规则：

```text
finding_submit_ready / bounty_submit_ready / phase_report_ready
≠ target_goal_complete
≠ case_audit_complete
```

case 级目标完成只能来自两条路径之一：

1. `top_impact_goal_satisfied=true`：已用证据证明本轮最高目标影响，例如前台/宿主机 RCE，并且范围、正控、负控、清理和声明边界可复核。
2. `whole_repo_exhausted=true`：全源码文件、全路由入口、全攻击面队列、全候选、继续深挖队列和 RCE/宿主机影响强制闭环均进入终态。

因此，审计开始后必须先建立全仓库队列，而不是先找一个漏洞就收口。每个候选必须被推进到 `validated_finding`、`excluded_with_evidence`、`merged_duplicate` 或 `not_applicable`；只要 `can_continue_validation=true`、入口停在 static_traced/enumerated、源码未读未审、RCE/宿主机方向 missing/blocked/unknown，完成门禁就必须失败。Forbidden Claims 只能限制报告措辞，不能关闭探索方向。

覆盖队列只能由当前主审计执行者归并到 `evidence/全仓库耗尽证明.json`；未归并、未回链、未闭合的材料不能支撑 case 完成。

## 禁止事项

- 禁止 sink-only technical_confirmed。
- 禁止 scanner-only technical_confirmed。
- 禁止 external-tool-only technical_confirmed。
- 禁止 source-only technical_confirmed。
- 禁止没有 trace 就 technical_confirmed。
- 禁止没有负控就写高置信。
- 禁止只看 200 响应。
- 禁止把框架默认安全假设当证据。
- 禁止把不可控参数当漏洞。
- 禁止把无法证明影响的点写成高危。
- 禁止把“已知 ID 后可利用”写成高价值 technical_confirmed，却不证明攻击者如何获得该 ID。
- 禁止把单对象 ID 样本外推成批量、全租户、全用户、全工作区或广义影响。
- 禁止账号矩阵缺账号对象矩阵必要事实、主体 ID、租户、对象归属、token/cookie 引用和清理责任时声称多主体 technical_confirmed 可复核。
- 禁止把 pending、candidate、blocked 写成 technical_confirmed。
- 禁止为了凑数量写低价值漏洞。
- 禁止把项目私有路径、项目名、编号、内部平台术语写进通用 skill。
- 禁止把项目运行、部署、恢复、调度、监控、任务编排、容器维护内容混进漏洞审计 skill。
- 禁止只读标题、函数名、目录或 grep 命中后就下结论。
- 禁止把扫描器 payload、异常栈、回显 marker、callback、版本命中单独当作漏洞证明。
- 禁止一个弱 payload 失败就 rejected。
- 禁止未追踪最高影响且不写停止原因。
- 禁止在未授权、第三方真实系统、生产真实用户数据、真实凭据、真实云 metadata credential 或越出目标测试范围的目标上执行动态验证。
- 禁止在报告中输出完整真实 secret、token、cookie、密码、个人敏感信息或可复用凭据。
- 禁止扩大报告声明：未证明“无需认证”就不得写无需认证；未证明“任意”就不得写任意；未证明“全局”就不得写全局。
- 禁止在安全模型 unknown、scope unknown、默认配置 unknown、known risk 未去重时写对外可提交。
- 禁止四则条件缺失时写 validated、bounty_submit_ready、finding_submit_ready 或漏洞成立。
- 禁止把 finding_submit_ready、bounty_submit_ready、phase_report_ready、候选清单或赏金资格写成 case_audit_complete。
- 禁止高危面未覆盖、最高影响未闭环、缺失证据仍阻断时写 case 完成。
- 禁止用 Forbidden Claims 关闭未验证方向。
- 禁止 skill 台账写已应用但没有覆盖矩阵、候选发现、证据链、缺失证据、最高影响或声明边界产物。
- 禁止报告占位符残留时写 ready。
- 禁止机器完成门禁未运行或失败时写完成通过。
- 禁止全仓库耗尽证明缺失、`target_goal_complete=false`、open 候选仍可继续验证或 RCE/宿主机影响未闭环时写 case 完成。

## 自检清单

输出审计结论或报告前逐项检查；关键项为“否”时不得 technical_confirmed。

### 范围与入口

- [ ] 是否写清授权范围、目标版本、配置、测试账号、测试对象、可重置能力？
- [ ] 是否读取机器完成门禁结果；若未运行或失败，是否没有写完成通过？
- [ ] 是否枚举 HTTP、GraphQL、WebSocket、RPC、CLI、webhook、queue、cron、event、file import 入口？
- [ ] 是否记录 route/method/path/handler/middleware/auth/source 参数？
- [ ] 是否处理动态路由、group prefix、自动路由、hook、反射、插件入口？

### Source 与可控性

- [ ] 是否证明 source 可由攻击者、低权限用户、外部服务或可污染存储控制？
- [ ] 是否记录控制主体、控制粒度、绑定变量和进入位置？
- [ ] 是否处理 query/path/body/header/cookie/JSON/XML/multipart/GraphQL/WebSocket/CLI/webhook/queue/file import/session/claim？
- [ ] 是否判断参数是否被硬编码覆盖、默认值替换、白名单映射、类型转换阻断或条件可控？
- [ ] 如果漏洞依赖 ID、对象 handle、租户标识或分享 token，是否证明攻击者获得路径？
- [ ] 如果报告写多对象、批量、全量或广义影响，是否证明 ID 可批量、持续、枚举、列表、搜索、导出或可推导获得？
- [ ] 多主体、多对象或跨租户结论是否有账号矩阵、账号对象矩阵必要事实、主体 ID、租户、对象归属和清理责任？

### Trace 与 Sink

- [ ] 是否逐跳追踪 route → handler/controller → service → repository/mapper/model/helper/client → sink？
- [ ] 是否记录每一跳的 `file:line`、变量名变化、分支条件、权限检查？
- [ ] 是否定位 sink 的危险参数位置，而不是只列 API 名？
- [ ] 是否证明 source 污染的变量仍进入 sink？

### Transform / 防护

- [ ] 是否确认参数化真实覆盖全部动态片段？
- [ ] 是否确认白名单是允许列表，并在规范化之后执行？
- [ ] 是否确认 escape/encode 匹配当前上下文？
- [ ] 是否确认 canonicalize/realpath/normalize 早于路径判断，并处理符号链接、编码和平台差异？
- [ ] 是否确认防护作用在同一变量、同一分支、同一上下文且早于 sink？

### 动态验证与负控

- [ ] 是否明确自有 Docker/CTF/靶场/可重置实验环境、测试账号、测试对象、快照/重置/清理能力？
- [ ] 是否写出 baseline、强正控、强化请求、负控请求？
- [ ] 是否使用足够证明漏洞语义的 payload，而不是只用无意义 marker？
- [ ] 是否记录响应、日志、副作用、清理/回滚？
- [ ] 是否为 technical_confirmed 至少提供一个负控？
- [ ] 如果不能动态验证，是否降级为 candidate/blocked 并说明原因？

### 最高影响追踪

- [ ] 是否从低层触发继续追数据读取、写入、越权、执行、内网 canary、浏览器执行或组合链？
- [ ] 是否写明最高已证明影响？
- [ ] 未证明更高影响是否进入 `higher_impact_closures[]`？
- [ ] 若未继续升级，是否写明停止原因？
- [ ] 是否没有读取真实用户数据、泄露真实凭据或越出授权范围？

### 高危面、缺失证据与完成门禁

- [ ] `high_risk_surface_matrix` 是否覆盖所有必需高危面？
- [ ] 未覆盖高危面是否进入缺失证据并标明 `blocks_case_completion`？
- [ ] 已触发 skill 是否有对应产物结果或排除记录？
- [ ] 缺失证据中是否无阻断 case 完成的 open / blocked / unknown / missing 项？
- [ ] Forbidden Claims 是否没有被当作排除证据或停止探索理由？
- [ ] 报告占位符是否清空？

### 判定与报告

- [ ] 是否为每项发现标注 technical_confirmed/candidate/blocked/rejected？
- [ ] 是否说明 candidate 升级还缺什么证据？
- [ ] 是否说明 rejected 的排除证据？
- [ ] 是否没有把扫描器结果、外部模型/工具自述、pending 状态、200 响应当 technical_confirmed？
- [ ] 是否查阅或尝试查阅官方安全策略、权限模型、scope、默认配置、release notes、known issues，并写明安全模型 unknown 时的降级？
- [ ] 是否区分 technical_confirmed 与对外提交资格，避免把预期功能、accepted risk、hardening only、范围或官方已知拒绝（外部裁决） 或未去重问题写成新漏洞？
- [ ] 是否区分 finding_submit_ready、phase_report_ready、target_goal_complete 与 case_audit_complete？
- [ ] 是否已把入口、Source、Sink、Trace、防护、复现、强正控、负控、最高影响、清理、修复建议和声明边界写入对应 EVID，并由报告阶段引用唯一模板渲染？
- [ ] 是否删除项目私有路径、项目名、编号、内部平台术语和运维流程？
