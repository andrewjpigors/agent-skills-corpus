---
name: parameter-controllability-analysis
description: Use when deciding whether a parameter, object field, stored value, claim, file name, URL, path, expression, selector, or object id remains attacker-controlled at a sensitive operation, especially when the result may be written into a report and must be bounded by the official security model, scope, and expected behavior.
---

# 参数可控性判断

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

这个 Skill 只解决一个问题：**到达敏感操作时，目标值是否仍然由攻击者控制，控制到什么粒度，在哪些条件下可控，哪些证据足以支撑结论**。它不是危险函数清单，也不是漏洞类型百科；它用于把“看起来有线索”的输入、变量、字段、对象 ID、URL、文件名、路径、表达式、claim 或存储值，裁决成可复核的可控性结论。

在以下场景优先使用：

- 已经看到 source 和 sink，但不确定 source 是否真正影响 sink 的危险参数位置。
- 扫描器、正则、CodeQL、Semgrep、IDE 或其他模型/工具 给出了 taint trace，需要人工复核。
- 漏洞报告声称“用户可控参数进入 SQL/命令/文件/SSRF/XSS/鉴权判断”，需要判断是否夸大。
- 参数传进对象、DTO、Map、数组、Model、Entity、Serializer、FormRequest、Pydantic、ModelBinder 或 claims 后，需要做字段级控制判断。
- 值经过默认值、白名单、类型转换、服务端查询、权限绑定、canonicalize、escape、sanitize 后，需要判断控制权是否被缩小、转移、保留或阻断。
- 弱 payload 没有效果，需要判断是参数不可控、防护有效，还是 payload 没命中上下文、观察点错误、分支条件没满足。
- IDOR、越权、SSRF、文件、上传、模板、表达式、SQL 结构片段、NoSQL operator、JWT/session/claim 等发现需要区分 `technical_confirmed / candidate / blocked / rejected`。

每次使用时，先写出目标句：

```text
我要判断：{source字段/存储值/claim} 是否以 {FULLY/FIELD/CONDITIONAL/...} 控制 {sink危险参数位置}，以及该控制能否支撑 {漏洞类型/报告声明}。
```

然后按本 Skill 的顺序推进：Source → Sink → Transform/覆盖 → Route/Call Chain → 字段级 trace → 证据点 → 动态强验证 → 负控 → 状态判定 → 报告边界。不要先写结论再找证据。

使用本 Skill 的输出至少包含一种：

- 参数可控性矩阵。
- 字段级映射表。
- 覆盖/防护/分支裁决表。
- sink 危险参数映射。
- 动态验证与负控计划。
- `technical_confirmed / candidate / blocked / rejected` 判定。
- 报告中的 Source、Trace、Sink、防护缺口、影响证明和声明边界。

## 核心原则

### 1. 参数可控性是 technical_confirmed 的硬门槛

没有可控性，就没有漏洞确认。以下证据都不能单独支撑 `technical_confirmed`：

- 只有 source，例如 `req.body.url`、`$_GET['id']`、`@RequestBody dto`。
- 只有 sink，例如 `query(sql)`、`system(cmd)`、`render(template)`。
- 只有 source 到 sink 的扫描器线索。
- 只有变量名像 `id`、`url`、`path`、`role`、`tenant`、`template`。
- 只有 HTTP 200、错误栈、marker 回显、DNS callback、版本命中。
- 只有 外部模型/工具自述“已验证可控”。

`technical_confirmed` 至少要证明：攻击者能控制 source；source 绑定到目标变量/字段；每一跳传播连续；覆盖、防护、分支和权限没有阻断；值进入 sink 的危险参数位置；强正控证明安全影响；负控排除误报；副作用可清理或无副作用。

检验句：**我能否写出 `source -> binding -> field mapping -> transform/branch -> actual sink dangerous argument -> positive proof -> negative control`？** 写不出就不能 technical_confirmed。

### 1.1 可控性裁决必须按顺序推进

不要先问“这个参数能不能打出漏洞”，先按顺序回答：

1. **是否进入服务端或任务系统**：只在前端、文档、Swagger、Mock、测试 fixture 中出现的字段，不能算后端 source。
2. **谁能控制**：匿名、普通用户、管理员、内部服务、第三方 webhook、低权限写入端、攻击者可污染存储，各自风险不同。
3. **控制到什么粒度**：完整值、对象字段、数组元素、枚举选择、对象 ID、排序字段、operator、path segment、URL host、文件内容、文件名、claim。
4. **是否跨可信边界**：session、JWT/OAuth/OIDC/SAML、签名 header、HMAC、反向代理 header、CSRF、tenant/owner 是否由可信服务端绑定。
5. **是否被服务端覆盖或派生**：当前主体、tenant、owner、随机文件名、服务端查询字段、默认配置、对象存储 key、record 字段是否替换了用户值。
6. **是否仍影响同一个危险参数**：sink 使用的是原始值、防护后值、派生值、数据库值、默认值，还是另一个字段。
7. **是否能触发当前分支**：权限、对象状态、feature flag、异常路径、批量元素、异步 consumer 是否真的让该值到达 sink。
8. **是否有强正控和负控**：参数变化能否稳定改变 sink 语义；移除字段、安全值、无权限主体、不同对象/租户是否让影响消失。

任一环证据不足时，写 `candidate` 或 `blocked`，不要用“看起来可控”补齐缺口。

### 1.2 工具 trace 和规则命中只提供可控性线索

CodeQL、Semgrep、商业 SAST、IDE data-flow、grep 和其他模型/工具 的输出必须拆成四类线索复核：

- `source candidate`：source pattern 是否过宽；字段是否真由攻击者控制；默认值、helper、包装对象是否被误标。
- `propagation candidate`：赋值、函数参数、返回值、对象字段、builder、serializer、ORM hydration、队列消息是否传播的是同一后继字段。
- `sanitizer candidate`：工具认为安全的函数是否作用在同一变量、同一字段、同一分支、同一上下文；sink 是否使用了返回值。
- `sink candidate`：命中 API 是否使用了危险参数；污染值是否进入危险参数，而不是日志、label、错误消息或普通显示字段。

SARIF、规则路径图、IDE 跳转和扫描器 confidence 不得直接写成可控性结论；它们只决定下一步读哪里、测哪里。

### 1.3 官方安全模型决定能写多强

可控性判断不是只看代码路径，还要看官方资料是否支持最终声明。若官方 SECURITY、权限模型、API 文档、默认配置、已知风险、范围说明、预期行为、受信任主体边界或对外提交限制与当前声明冲突，则不能把结果直接写成更强结论。

检验句：**如果把官方资料盖住，只看代码、请求和响应，我还能写出与官方边界一致的声明吗？如果不能，就必须降级。**

### 2. “传递过”不等于“实际使用”

参数出现在调用链里，只能说明它被传递过；漏洞判断要看它是否影响危险语义。

常见误判：

- 参数传入 service，但 service 没有使用该参数。
- 整个 DTO 进入 DAO，但 SQL 只使用 DTO 的另一个字段。
- `req.body` 被传进 `update(user)`，但 ORM 只允许 `$fillable` / permitted / allowed fields 中的字段。
- 整体对象被绑定进实体，但敏感字段在 service 层被当前主体、服务端查询或默认值覆盖。
- Mass assignment / over-posting 只允许“字段名进入对象”这一事实，不等于敏感字段进入持久化或权限判断。
- 参数传入 HTTP client wrapper，但最终 host、scheme、port 由服务端固定。
- 文件名传入 upload helper，但最终文件名被服务端随机生成。
- object id 传入查询，但查询同时绑定当前主体 owner/tenant。
- JWT claim 被读取，但 claim 来自服务端 session 映射而不是客户端 token。
- queue message 里有字段，但 consumer 不消费该字段或消费的是另一个 topic/schema。

检验句：**sink 的危险参数到底是哪个变量/字段？它和 source 是同一个后继值吗？**

### 3. 字段级可控性优先于对象级可控性

对象可控不代表对象里的每个字段可控；对象不可完全可控也不代表其中没有危险字段可控。审计时必须追字段、键、元素、属性、claim、嵌套 path，而不是只追对象名。

示例判断：

| 现象 | 不能直接说 | 必须继续判断 |
|---|---|---|
| `dto` 来自请求体 | DTO 全字段可控 | 哪些字段被 binder 接收、哪些字段被忽略、哪些字段被覆盖 |
| `Map<String,Object>` 来自 JSON | Map 安全或危险 | 哪些 key 进入 operator、SQL 片段、模板、权限条件 |
| `entity` 被 `save()` | 任意字段写入 | ORM 允许字段、默认值、hook、setter、guarded/fillable/permit/allowed fields |
| `patch/update` 接收整个对象 | 可改所有字段 | DTO 到 entity 的字段复制、敏感字段覆盖、allowlist/denylist、hook、审计字段 |
| `claims.role` 被读取 | role 可伪造 | token 签名、issuer、audience、exp、算法固定、服务端 session 绑定 |
| `record.owner_id` 进入授权判断 | owner 可控 | owner 来自请求、数据库、session，还是对象选择的派生结果 |

字段级可控性必须写清：`source.field -> binding.field -> local.field -> transform -> sink.argument`。

### 4. 覆盖语义按代码意图判断，不按方法名猜

同一个方法名在不同上下文里可能只是 transform，也可能是 sanitizer；同一个 `if` 可能是默认值保护，也可能是安全拦截。必须读语义。

| 覆盖/限制 | 典型语义 | 可控性判断 |
|---|---|---|
| 无覆盖 | 输入一路传播到 sink | `FULLY_CONTROLLABLE` 或 `FIELD_CONTROLLABLE` |
| 无条件覆盖 | sink 前总是赋固定值/服务端值 | `OVERWRITTEN` 或 `SERVER_CONTROLLED` |
| 空值默认 | 只有 null/empty 时使用默认值 | 非空输入仍 `CONDITIONALLY_CONTROLLABLE` |
| 条件覆盖 | 某分支覆盖，某分支保留 | 输出分支矩阵，判断攻击者能否选分支 |
| 白名单 | 只允许服务端定义值 | `ALLOWLIST_CONTROLLABLE`，继续判断允许值是否仍危险 |
| 类型/范围 | int、UUID、enum、date、range | `TYPE_LIMITED_CONTROLLABLE`，可能阻断注入但不自动阻断 IDOR |
| 服务端查询 | 输入 id 换成 DB record 字段 | 直接字段不可控，但对象选择可能可控 |
| 权限绑定 | owner/tenant 来自当前主体 | 通常阻断越权，但要证明绑定在 sink 前且覆盖批量元素 |
| sanitizer | 输出安全值进入 sink | 只有同变量、同字段、同分支、同上下文且失败阻断才有效 |

检验句：**如果攻击者提供不同输入，sink 危险参数会不会随之改变？改变范围是什么？**

### 5. 可控性状态要分级，不要二元化

使用以下状态表达控制粒度：

| 状态 | 含义 | 常见结论 |
|---|---|---|
| `FULLY_CONTROLLABLE` | 完整值可由攻击者控制 | 高优先追 sink 影响 |
| `FIELD_CONTROLLABLE` | 对象/数组/JSON/DTO/Map 中部分字段可控 | 必须字段级映射 |
| `CONDITIONALLY_CONTROLLABLE` | 满足分支、格式、角色、配置或对象状态时可控 | 需要分支与运行态证明 |
| `ALLOWLIST_CONTROLLABLE` | 只能选择服务端允许值 | 判断允许值是否仍有危险语义 |
| `TYPE_LIMITED_CONTROLLABLE` | 类型/范围缩小 | 注入可能降级，越权/业务滥用仍可能成立 |
| `DERIVED_CONTROLLABLE` | 值由输入派生，如 slug/hash/lookup/normalize | 判断危险语义是否保留 |
| `STORED_CONTROLLABLE` | 攻击者可先写入，后续读取进入 sink | 必须写入端和读取端闭合 |
| `SERVER_CONTROLLED` | 值来自可信服务端状态 | 通常不能作为攻击者可控参数 |
| `OVERWRITTEN` | sink 前被无条件覆盖 | 通常 rejected |
| `UNRESOLVED` | 证据不足 | candidate 或 blocked |

### 6. 低层可控不等于高层影响

可控性只是漏洞成立链条的一环。低层现象不能自动升级为高层结论：

- `int id` 可控：不能证明 SQL 结构注入，但可能证明 IDOR 或批量越权。
- URL 字符串可控：不能证明 SSRF 高危，必须看最终 URL/IP、重定向、DNS/IP 校验、响应可读性或受控内网 canary。
- 命令参数片段可控：不能证明命令执行，必须证明命令语义、stdout/stderr、退出码、执行身份或受控文件/回连。
- HTML 反射可控：不能证明 XSS，必须看浏览器执行上下文、转义、CSP、DOM/存储触发。
- SQL 错误可控：不能证明数据泄露，必须看布尔/时间/常量/测试表/受控写入等影响。
- 版本可疑：不能证明组件漏洞可达，必须看组件加载、配置启用、调用点和输入可控。

### 6.1 对象标识符可控必须同时证明“能传入”和“能获得”

`id`、`ids`、`user_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、资源 URI、物理表名这类对象标识符，不能只判断“参数值能不能被攻击者填写”。对象级漏洞还要判断攻击者是否能从自己的权限范围内获得目标标识符。

对象标识符可控性拆成四层：

| 层级 | 必须证明 | 不足时的结论 |
|---|---|---|
| 可传入 | 攻击者能把 ID 放进 query/path/body/header/message/file 中，且后端接收 | 只能说明有 source |
| 可选择 | 该 ID 影响对象选择、查询、更新、删除、导出或权限判断 | 只能说明对象选择可控 |
| 可获得 | 攻击者能通过列表、详情、搜索、导出、日志、关系链、分享页、可预测序列、批量接口等获得目标 ID | 缺失时不能高价值 technical_confirmed |
| 可越权 / 可批量 | A/B 主体对象负控成立；若声明批量，证明 ID 能批量、持续、枚举、列表、搜索、导出或可推导获得 | 缺失时只能窄化或降级 |

管理员手工提供的 ID、报告作者笔记里的 ID、聊天上下文里的 ID、历史附件里的 ID，只能作为定位样本，不能算攻击者可获得路径。“已知 ID 后可利用”不是完整的可控性证明；如果拿不到 ID 获取链，通常写 `candidate` 或 `blocked`，有明确不可获得证据时才写 `rejected`。

多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

检验句：**这个 ID 是攻击者自己可获得的，还是我在审计材料里手工拿到的？如果我写“批量/全量/广义影响”，攻击者能不能稳定获得足够多 ID？**

### 7. 授权实验模式下默认追最高可证明影响

在自有 Docker、CTF、靶场、本地、隔离预发、测试租户或其他明确授权、可重置、可观察、可清理环境中，不要停在弱 marker。应在边界内使用足够强的正控证明真实安全语义，包括受控数据读取、受控写入、受控对象越权、受控文件边界、受控回连、受控命令结果、受控批量、受控持久化验证或最小资源压力验证。

真正边界是：不越出授权范围；不测试第三方真实系统；不读取、输出或传播真实生产用户数据；不复用或泄露真实凭据；不制造不可清理、不可回滚、不可解释的副作用；没有账号、对象、日志、快照、重置或清理能力时不写 technical_confirmed。

## 审计目标

一次合格的参数可控性判断应回答：

1. source 是什么，谁能控制，控制粒度多大。
2. source 如何绑定到变量、字段、对象、claim、文件或消息。
3. 目标 sink 是什么，危险参数位置在哪里。
4. 每一跳传播是否连续，是否跨函数、跨文件、跨类、跨异步边界。
5. 值是否被默认值、硬编码、服务端查询、类型转换、白名单、权限绑定或 sanitizer 覆盖。
6. sink 所在分支是否执行，分支条件攻击者能否影响。
7. 参数是否被实际使用，还是只传递、记录、展示或进入非危险参数。
8. 当前可控性状态是什么：完全、字段级、条件、白名单内、类型受限、派生、存储型、服务端控制、覆盖、未知。
9. 如果静态可控，动态上能证明什么最高影响。
10. 如果不能 technical_confirmed，缺什么证据，为什么降级。
11. 如果参数是对象标识符，攻击者如何获得该 ID / handle / token / URI，能支持单对象、多对象、批量还是不可获得结论。
12. 如果依赖多主体、多对象或跨租户，账号矩阵、对象归属、账号对象矩阵必要事实、token/cookie 隔离和清理责任是否可复核。
13. 如果可控性结论要写入漏洞报告、复核结论或 对外提交声明，官方安全模型、范围、默认配置、已知风险、预期行为和禁止声明边界是否支持该结论。

需要排除：

- source 不可控、只在前端、只来自可信配置、只来自不可伪造 session/claim。
- source 没有绑定到目标变量。
- 参数被无条件覆盖或服务端重新生成。
- 参数只进入非危险参数位置。
- 参数进入对象但 sink 使用另一个字段。
- 白名单/类型/权限/参数化/上下文转义真实阻断当前风险。
- 弱 payload 失败但尚未证明路径不可达或防护有效。

## 输入材料

### 代码材料

- 入口：route、controller、handler、resolver、RPC method、WebSocket event、CLI command、webhook、queue consumer、cron job、file import、plugin hook。
- 绑定：request object、body parser、multipart parser、DTO/VO/Entity/Model、Serializer、FormRequest、Pydantic、ModelBinder、strong parameters、route model binding、GraphQL args、message schema。
- 调用链：service、usecase、manager、repository、DAO、mapper、model、helper、trait、mixin、decorator、AOP、interface、abstract class、base class、event producer/consumer。
- 覆盖：default、fallback、merge、copy、clone、builder、setter、hydration、mass assignment、server-side lookup、session/claim rewrite、object mapping。
- 防护：validate、sanitize、escape、canonicalize、normalize、allowlist、denylist、schema validation、auth check、policy/gate/voter、tenant/owner condition、CSRF/signature/JWT verification。
- sink：SQL/ORM/NoSQL/LDAP/XPath、命令/代码/表达式/模板、文件读写/上传/归档、SSRF、XSS、XXE、反序列化、redirect/header、auth decision、cache/queue/log/config/secret。

### 配置材料

- 路由加载、route cache、自动路由、fallback、resource route、API gateway/rewrite/proxy。
- body parser、serializer、validation、strict mode、mass assignment、unknown fields、extra fields。
- ORM/query builder/raw API、Mapper XML、SQL dialect、NoSQL operator 解析。
- security chain、middleware/filter/interceptor 顺序、CSRF、CORS、trusted proxy、session/cookie、JWT/OAuth/OIDC/SAML。
- template autoescape、raw/safe 标记、XML parser、反序列化类型限制、HTTP client redirect/DNS/IP 配置。
- upload/storage/static serving、object storage policy、web root、symlink、path alias、feature flag、profile。

### 运行材料

- baseline 请求、强正控请求、负控请求、Burp/DevTools/curl/browser 操作记录。
- 测试账号、测试对象、测试租户、测试 token、测试文件、测试表、受控 canary、受控回连服务。
- 应用日志、访问日志、auth 决策日志、SQL/ORM 日志、HTTP 出站日志、文件/队列/缓存日志。
- 数据库记录、对象归属、租户边界、文件变化、对象存储对象、队列消息、回调记录。
- 标识符获取材料：对象 ID、用户 ID、租户 ID、文件 ID、分享 token、lookup handle、资源 URI 来自列表、详情、搜索、导出、日志、关系链、分享页、可预测序列还是批量接口；必须区分手工样本、单对象可得、多对象可得、批量可得和不可得。
- 多主体或对象边界 claim 必须引用账号对象矩阵，记录主体、角色、对象归属、租户/workspace、token/cookie 隔离和清理责任；账号对象矩阵字段以 `templates/账号对象矩阵模板.md` 与对应 schema/template 为准，本 Skill 不重新定义。
- 清理/恢复记录：测试记录删除、测试文件删除、缓存/队列清理、临时服务关闭、快照恢复。

### 复核材料

- 扫描器 trace、SARIF、规则命中、漏洞报告、复现报告、误报说明、修复说明、单元/集成测试。
- 官方文档、安全公告、release notes、框架安全配置说明、SECURITY、权限模型、API 文档、默认配置、已知风险、范围说明、预期行为、accepted risk、范围或官方已知拒绝（外部裁决）、对外提交限制。
- 其他 外部模型/工具结论只能当线索，必须重新做 source、field mapping、trace、sink、强正控和负控。

### 安全模型材料

- 官方声明的保护边界：用户/租户/对象/项目/工作区/插件/脚本/管理员/服务账号各自的信任边界。
- 默认配置与安全配置：功能默认是否启用、危险能力是否需要显式开启、示例配置是否只用于开发或测试。
- 范围与例外：scope、范围或官方已知拒绝（外部裁决）、known issue、duplicate、accepted risk、expected behavior、hardening only、管理员正常能力。
- 报告边界：官方或目标规则是否要求特定复现质量、非账号类敏感材料展示边界、影响证明、禁止 payload、禁止声明或提交前置条件。
- 缺失处理：找不到这些材料时记录 `security_model_status=unknown`，不得把 unknown 当作违反安全边界。

## Source 识别

Source 识别必须同时记录：来源、进入点、控制主体、控制粒度、可控条件和可信边界。

### HTTP / API Source

- query：`id`、`ids`、`url`、`path`、`file`、`name`、`sort`、`order`、`filter`、`callback`、`returnTo`、`redirect`、`template`、`expr`、`operator`、`tenant`、`page`、`limit`。
- path：`/{id}`、slug、filename、wildcard、regex capture、extension、tenant path、locale、version、resource action。
- body：form、JSON、XML、GraphQL variables、protobuf、nested object、array、bulk list、operator object、patch document。
- header：Authorization、Host、Origin、Referer、X-Forwarded-*、Content-Type、User-Agent、自定义签名 header、callback header。
- cookie：session、remember-me、JWT cookie、tenant、locale、偏好设置、业务 cookie。
- multipart：文件名、content-type、文件内容、普通字段、压缩包 entry name。

### 对象标识符 Source

对象标识符既可能是普通 source，也可能是权限边界本身。判断时不要只写“ID 可控”，必须拆开：

- **字段来源**：ID 来自 path、query、body、header、cookie、message、file row、GraphQL variable，还是服务端 session / claim / 数据库查询。
- **攻击者获得路径**：列表、详情、搜索、导出、日志、关系链、分享页、可预测序列、批量接口、分页接口、客户端缓存、前端状态。
- **对象归属**：攻击者自己对象、受害者对象、control 对象、跨租户对象、公开对象、系统对象、未知对象。
- **规模边界**：单个样本、同类多个、分页批量、持续获取、可枚举、可推导、不可获得。
- **服务端重绑定**：后端是否把传入 ID 换成当前主体、tenant、owner、server lookup、route model binding 后的对象。
- **批量语义**：`ids[]`、bulk update/delete/export/import 中是否逐项校验、逐项授权、逐项记录失败。

如果 ID 只能由审计者手工提供，或只能从管理员视角看到，参数本身可以继续追踪，但高价值越权结论必须降级；如果报告声称批量影响，必须证明攻击者能批量获得 ID，而不是只证明一个样本 ID 可替换。

### 框架绑定 Source

| 生态 | 常见入口 | 可控性重点 |
|---|---|---|
| Java/Spring | `@RequestParam`、`@PathVariable`、`@RequestBody`、Servlet request、JAX-RS、Struts Action、MultipartFile | DTO mass assignment、Bean Validation 是否只校验格式、MyBatis `${}`、对象级授权、SpEL/EL |
| PHP/Laravel/Symfony/ThinkPHP | `$_GET/$_POST`、Request、route param、FormRequest、Symfony attributes、WordPress REST/admin-ajax | `$request->all()` 整体写模型、`$fillable/$guarded`、raw query、Blade raw、直接读超全局绕过封装 |
| Python/Django/Flask/FastAPI | request、forms、serializers、Pydantic、Celery args | `RawSQL/extra/raw`、`mark_safe`、`csrf_exempt`、`render_template_string`、route 未认证 |
| Node/Express/Nest/Koa | `req.query/params/body/headers/cookies`、DTO/Pipe、GraphQL args、WebSocket payload | `req.body` 整体更新对象、缺 auth middleware、无约束 CORS、`eval/Function`、`child_process` |
| Go | `r.URL.Query()`、route vars、Gin/Echo/Fiber bind、struct tags、form file | binding 后默认值、validator 是否阻断、path join、模板与 `os/exec` |
| DotNet | model binding、`[FromRoute]`、`[FromQuery]`、`[FromBody]`、claims、HttpContext | over-posting、DataAnnotations 边界、AuthorizationHandler、EF raw SQL、claims 可信性 |
| Rails | `params`、strong parameters、cookies、session、headers | permitted fields、before_action、Pundit/CanCan、ActiveRecord raw/scope |

### 非 HTTP 与二次污染 Source

- GraphQL：operation、variables、input object、alias、directive、resolver args、context claim。
- WebSocket：event name、payload、room/channel、connection token、headers、message metadata。
- CLI：argv、stdin、env、config path、import file path。
- webhook：payload、signature header、event type、replay id、source IP/proxy header。
- queue/event：topic、routing key、headers、message body、metadata、producer identity。
- cron/job：任务读取的数据库记录、缓存 key、文件内容、配置项、上次任务状态。
- file import：CSV/Excel/XML/JSON/YAML/ZIP/TAR/office 文档内容、sheet 名、entry name、文件名。
- stored taint：用户可编辑昵称、模板、规则、回调 URL、报表字段、对象 metadata、缓存值、队列消息、上传文件内容。

存储型 source 必须闭合两端：

```text
写入入口 -> 存储位置/字段/key -> 读取入口/任务/consumer -> sink危险参数位置
```

只看到数据库里有 tainted-looking 字符串，不等于攻击者可写；只看到写入端，不等于读取端会进 sink。

### 身份、session、JWT、claim Source

身份字段必须按信任边界判断：

- 服务端 session 中的 `user_id/tenant_id/role/scope` 通常是服务端控制；但要检查 session fixation、反序列化、存储污染、弱签名、客户端可写 session store。
- JWT/OAuth/OIDC/SAML claim 只有在签名验证、算法固定、issuer、audience、exp/nbf、key selection、scope/tenant 绑定都成立时才可信。
- 反向代理身份 header 只有在外部无法直连应用、应用只信任可信代理、代理会覆盖客户端同名 header 时才可信。
- API key/HMAC 主体映射要检查签名验证、时间戳/nonce、重放保护和权限绑定。
- 前端隐藏字段、客户端生成 Authorization、移动端硬编码 key，只有后端接受并信任时才成为后端 source。

### Source 证据模板

```markdown
| Source | 类型 | 进入位置 | 初始变量/字段 | 控制主体 | 控制粒度 | 可控条件 | 是否存储型 | 证据 |
|---|---|---|---|---|---|---|---|---|
| `{field}` | query/body/claim/message/... | `{file:line}` | `{var.path}` | 匿名/普通用户/... | 完全/字段/枚举/条件 | `{auth/config/object}` | 是/否 | `{代码/请求/日志}` |
```

## Sink 识别

Sink 识别必须记录危险语义和危险参数位置。函数名只是入口，真正要证明的是 source 是否进入“能改变安全语义的那一个参数、字段、片段或对象”。

### 值型 Sink 与结构性 Sink

| 类型 | 示例 | 可控性要求 |
|---|---|---|
| 值型 sink | SQL `WHERE name = ?` 的绑定值、日志字段、普通 JSON 响应 | 参数化/编码可能有效，但仍需看授权、敏感输出和业务影响 |
| 结构性 sink | SQL 表名/列名/orderBy/groupBy/limit、NoSQL operator、LDAP filter、XPath、shell 结构、模板名/表达式、path segment、URL host/scheme/port、header name/value | 必须服务端白名单或严格上下文防护；普通值绑定不够 |
| 权限型 sink | object id、tenant id、owner id、role/scope、policy decision、ACL query | 关键是对象级授权和主体绑定 |
| 解析型 sink | XML、YAML、反序列化、模板编译、表达式求值、归档解压 | 关键是 parser 配置、类型限制、输入位置和触发链 |

### 查询与注入 Sink

- SQL：JDBC Statement、PreparedStatement 拼接前 SQL、MyBatis `${}`、Mapper XML、SQL Provider、JPA nativeQuery、Hibernate HQL/JPQL、PDO/mysqli query、Laravel raw/whereRaw/orderByRaw/selectRaw、Django RawSQL/extra/raw、ActiveRecord raw SQL。
- NoSQL/DSL：Mongo filter/update/delete、operator injection、aggregation pipeline、Elasticsearch DSL、Redis key/eval、GraphQL filter。
- LDAP/XPath：LDAP filter/DN 拼接、XPath expression、XML query。

### 执行、模板与表达式 Sink

- 命令执行：Runtime.exec、ProcessBuilder、system/exec/shell_exec/proc_open、child_process、subprocess、os/exec、PowerShell、ProcessStartInfo。
- 动态代码：eval、assert、Function、vm、script engine、reflection invoke、dynamic import。
- 表达式/模板：SpEL、OGNL、MVEL、Freemarker、Velocity、Thymeleaf、Jinja2、Twig、Blade raw、Smarty、ERB、Razor、Handlebars/EJS/Pug。

### 文件、网络、响应与权限 Sink

- 文件读写：include/require、file_get_contents、fopen、readfile、Files.read/write、fs.readFile/writeFile、open/read/write、object storage get/put。
- 上传/归档：move_uploaded_file、MultipartFile.transferTo、object storage upload、Zip/Tar extract、entry path join、static serving、web root mapping。
- SSRF/HTTP：RestTemplate、WebClient、OkHttp、HttpClient、URL.openConnection、Guzzle/cURL、axios/fetch/request、requests/httpx、net/http。
- XSS/响应：response writer、template render、JSONP callback、Markdown/HTML sanitizer、富文本、header、Location、Set-Cookie、Content-Disposition。
- auth decision：hasRole/hasAuthority、authorize、policy/gate/voter、owner/tenant condition、ACL query、role mapping、JWT/OAuth claim 使用。
- cache/queue/log/config：cache key/value、queue publish/consume、日志输出、配置写入、feature flag、secret/key material。

### Sink 证据模板

```markdown
| Sink类型 | API/语句 | 调用点 | 危险参数位置 | 输入变量/字段 | 是否实际使用 | 执行条件 | 防护点 | 证据 |
|---|---|---|---|---|---|---|---|---|
| SQL/SSRF/CMD/... | `{api}` | `{file:line}` | `{arg/field/fragment}` | `{var.path}` | 是/否/部分 | `{branch/auth/config}` | `{param/allowlist/...}` | `{代码/日志}` |
```

## Transform / 防护检查

Transform 是值的变化；sanitizer 是能阻断当前危险语义的防护。二者不能混用。

### Transform 分类

| 类型 | 示例 | 默认判断 |
|---|---|---|
| 纯传播 | assignment、参数传递、return、getter/setter | 保持可控 |
| 格式转换 | trim、lower、decode、parse JSON/XML、base64 decode | 通常仍可控 |
| 拼接组合 | concat、StringBuilder、sprintf、template string、path join | 组合值受污染，需字段级判断 |
| 容器传播 | array/list/map/object/session/cache | 字段/键/元素级可控 |
| 序列化映射 | DTO/VO/Entity/Model、ORM hydration、serializer | 追字段映射、默认值、别名、忽略字段 |
| 类型转换 | int/bool/enum/date/UUID | 缩小控制面，不自动安全 |
| 派生 | hash、slug、lookup、normalize、canonicalize | 判断危险语义是否保留 |
| 覆盖 | hardcoded/default/server value/db value | 可能阻断可控性 |
| 防护 | allowlist、parameterization、escape、authorization | 必须判断上下文和分支 |

### 防护有效性门槛

一个防护只有同时满足以下条件，才能降低或阻断可控性：

1. 作用在同一个 source 的后继变量或同一个字段上。
2. 发生在 sink 前。
3. 覆盖当前执行分支、异常分支、批量元素和异步消费端。
4. 与 sink 上下文匹配。
5. 失败时 return/throw/deny/abort，而不是 fallback 到原始值或危险默认值。
6. sink 实际使用防护后的值，而不是仍使用原始值。
7. 有代码、配置或运行态证据，不靠方法名和框架默认假设。

### 常见防护判断

- 参数化：只保护值位置；动态表名、列名、排序、operator、limit、JSON path、模板名、文件路径、URL host 仍需白名单。
- 白名单：必须是服务端允许列表；前端下拉、Swagger enum、注释、TypeScript 类型不算服务端白名单。
- 类型转换：int/UUID/enum 可阻断结构注入，但不能自动阻断 IDOR、越权、批量滥用或对象选择。
- canonicalize：必须早于路径/URL/IP/权限判断，并覆盖编码、双重编码、Unicode、大小写、符号链接、重定向、DNS rebinding。
- escape：必须匹配上下文；HTML escape 不能保护 SQL/shell/path/header，SQL escape 不能保护 HTML/JS。
- authorization：必须绑定当前主体与目标对象，不只是登录态、role 或前端按钮隐藏。
- schema validation：必须失败即阻断；只校验字段存在、非空、长度，不等于白名单安全。
- sanitizer：必须确认 sink 使用 sanitizer 返回值，而不是仍使用原始变量。

### 防护无效的典型情况

- `safe = sanitize(raw)`，sink 使用 `raw`。
- validator 检查非空/长度，但 sink 需要结构白名单。
- SQL `orderBy`、`groupBy`、表名、列名使用用户输入，却只做值参数化。
- `realpath` 在文件不存在时返回 false，代码回退到原始 path。
- `startsWith(base)` 在 decode/canonicalize 前执行。
- URL allowlist 只校验初始 URL，不校验重定向后地址、解析后 IP 和 DNS 重绑定。
- 授权检查在读取、写入、发送请求或状态改变后执行。
- 只对单个元素校验，批量列表其他元素未校验。
- `request->validated()` 只校验字段存在，未限制字段值集合。
- strong parameters 只允许字段名，不证明对象归属。
- JWT claim 被读取但未校验签名、issuer、audience、过期时间或算法固定。

## 路由与调用链追踪

参数可控性必须建立在可达调用链上。路由、handler、middleware、auth、service、repository、sink 的任一环缺失，都要降级。

### 入口到绑定

1. 枚举入口：HTTP、GraphQL、WebSocket、RPC、CLI、webhook、queue、event、cron、file import、plugin hook。
2. 解析 handler：method/path/operation/event/topic 到真实类、函数、方法、consumer 或 job。
3. 记录中间链：middleware、filter、interceptor、guard、policy、gate、decorator、AOP、before/after hook。
4. 记录 source：字段名、来源、控制主体、请求样例或消息样例。
5. 记录绑定：handler 参数、request object、DTO/Model 字段、默认值、类型转换、schema validation。
6. 对 `action/type/op/method/interfaceId/event` 这类二次分发字段，逐方法建立独立参数任务卡。

### handler 到 sink

逐层追踪：

```text
handler/controller/resolver/consumer
  -> service、use case、manager
  -> repository/DAO/mapper/model/helper/client
  -> sink
```

必须处理：

- 父类、接口、trait、mixin、helper、decorator、依赖注入、注解/attribute、AOP、反射、dynamic dispatch。
- ORM/Mapper/XML/query macro/repository 基类。
- 事件、队列、定时任务：producer 和 consumer 两端都要追。
- 对象字段：getter/setter、property accessor、magic method、array access、map key。
- 批量：list/array 每个元素是否逐项校验、逐项授权、逐项绑定。

### 每一跳记录格式

```text
Level-N: {file:line} {class/function}.{method}({args})
输入: {sourceField/localVar/object.field/container[key]}
传播: assignment/call/return/field/container/serialization/message
覆盖/防护: default/hardcode/type/allowlist/sanitize/auth/canonicalize/none
分支: {condition} -> 保留/覆盖/拒绝/进入 sink
输出: {nextArg/return/field/message}
可控性: FULLY/FIELD/CONDITIONAL/ALLOWLIST/TYPE_LIMITED/DERIVED/STORED/SERVER/OVERWRITTEN/UNRESOLVED
证据: {关键代码片段}
缺口: {未解析实现/缺配置/缺运行态/缺负控}
```

## 数据流追踪步骤

### 第 1 步：建立参数任务卡

```markdown
- parameter_id: `{entry}:{source_field}:{sink}`
- entry: `{METHOD PATH / GraphQL op / queue topic / CLI / cron / file import}`
- source: `{query/path/body/header/cookie/claim/message/file/stored}`
- initial_binding: `{file:line var.field}`
- target_sink: `{file:line API dangerous_arg}`
- hypothesis: `{完全可控/字段可控/条件可控/不可控/未知}`
- required_identifier: `{无 / user_id / object_id / tenant_id / file_id / lookup handle / share token / URI / ...}`
- identifier_acquisition: `{列表/详情/搜索/导出/日志/关系链/分享页/可预测/批量接口/手工样本/未知/不可获得}`
- subject_object_matrix: `{attacker / owner / victim / control / cleanup}`
- security_model_status: 记录官方安全模型是否已复核、是否支持当前声明、是否属于预期行为/accepted risk/范围拒绝/known issue 等；具体状态值以对应中文 schema、template 和 validator 为准。
- current_status: `untraced`
```

### 第 2 步：写入口样例

写清 method、path、query、headers、cookies、body、multipart、认证状态、对象 ID、租户、前置数据。非 HTTP 场景写 CLI argv、queue message、webhook payload、file import 样例。后续强正控必须使用测试账号、测试对象、唯一 marker、日志观察点和清理步骤。

如果入口样例包含对象标识符，必须同时写清：

- ID 从哪里来：攻击者列表、详情、搜索、导出、日志、关系链、分享页、可预测序列、批量接口，还是审计材料手工给出。
- ID 属于谁：attacker 自己对象、victim 对象、control 对象、跨租户对象、公开对象还是未知对象。
- ID 获取规模：单对象、同类多个、批量/持续、可枚举、可推导、不可获得。
- ID 在后端是否被 owner/tenant/current user 重新绑定。

没有 ID 获取链时，入口样例只能用于定位和 candidate 复核，不能支撑高价值 technical_confirmed。

### 第 3 步：定位 source 进入点

记录读取 API、绑定变量、类型、默认值、嵌套字段、数组元素、claim/session 来源、文件名、文件内容或消息字段。框架自动绑定必须读 binder/serializer/form/model 配置；不能只看 controller 参数名。

### 第 4 步：追字段级传播

不要只追对象名，按字段追：

- `request.body.user.name -> dto.name -> entity.displayName -> template output`。
- `page.orderBy -> queryOptions.orderBy -> mapper XML ORDER BY`。
- `params.id -> repository.find(id) -> record.owner_id`：`id` 控制对象选择，`owner_id` 是否可控另判。
- `file.originalname -> sanitizedName -> storageKey`：判断 sanitizer 是否真实限制。
- `jwt.claim.role -> authContext.role -> policy decision`：判断 claim 是否可信、是否经过签名和 issuer/audience 校验。
- `message.payload.url -> job.url -> httpClient.get(finalUrl)`：producer 与 consumer 都要闭合。

### 第 5 步：识别覆盖和分支

输出覆盖表：

```markdown
| 位置 | 输入变量 | 覆盖/防护 | 条件 | true 分支 | false 分支 | 可控性影响 | 证据 |
|---|---|---|---|---|---|---|---|
```

必须记录 `return/throw/continue/break/redirect/exception/fallback`。如果敏感操作只在某个分支执行，要判断攻击者能否选择该分支；如果条件来自配置、环境、feature flag 或对象状态，通常需要运行态证据。

### 第 6 步：判断实际使用

```markdown
| 参数 | 到达 sink | 危险参数位置 | 实际使用 | 未使用/覆盖原因 | 证据 |
|---|---|---|---|---|---|
```

如果参数只是传递但未使用，或 sink 使用硬编码/服务端生成值，必须降级或 rejected。

### 第 7 步：判断控制粒度

```markdown
| 参数 | 控制范围 | 限制来源 | 可选值/格式/范围 | 是否仍危险 | 可控性状态 | 证据 |
|---|---|---|---|---|---|---|
```

判断示例：

- `int id`：不能支撑 SQL 结构注入，但可能支撑 IDOR。
- `enum sort`：如果只允许安全字段，SQL 注入风险降低；但不代表对象级授权安全。
- `allowlisted host`：白名单内可控，不等于 SSRF technical_confirmed；继续看允许目标、重定向、DNS/IP、响应可读性。
- `filename extension allowlist`：扩展白名单不证明内容安全、路径安全、写后不可执行。
- `server lookup by id`：字段值可能服务端控制，但攻击者是否能选择他人对象仍需验证。

### 第 8 步：强正控推进

如果静态可控性成立，在授权可重置环境中继续证明真实语义：

```markdown
| 漏洞族 | 强正控目标 | 观察点 | 必要负控 |
|---|---|---|---|
| SQL/NoSQL | 查询语义差异、测试数据读取/写入 | SQL/ORM 日志、响应差异、测试表 | true/false、安全值、移除字段、无权限账号 |
| SSRF | 最终 URL/IP、受控 canary、重定向后校验 | 出站日志、canary 请求、目标响应 | 允许/禁止 host、重定向对照 |
| CMD/RCE | 命令输出、执行用户、工作目录、受控文件/回连 | stdout/stderr、日志、文件、回连 | 普通值、移除字段、禁止命令 |
| IDOR/Auth | 双账号双对象、跨租户、状态改变 | 响应数据、审计日志、对象状态 | 自己对象、他人对象、无权限、跨租户 |
| FILE | resolved target、base 内外边界、受控读写 | 文件内容、日志、清理结果 | base 内/外、安全文件、不存在文件 |
| XSS/TPL | 浏览器执行、模板上下文、CSP | DevTools、DOM、Console、页面状态 | 编码后值、不同上下文、安全模板 |
```

### 第 9 步：输出可控性矩阵

```markdown
| Source | Sink | 路径状态 | 覆盖类型 | 可控性 | 可控条件 | 防护状态 | 强正控/影响 | 负控 | 结论 |
|---|---|---|---|---|---|---|---|---|---|
| `{source}` | `{sink}` | COMPLETE/PARTIAL/UNRESOLVED | none/default/allowlist/... | FULLY/CONDITIONAL/... | `{condition}` | 有效/不足/未确认 | 已证/待证/无影响 | 成立/缺失 | technical_confirmed/candidate/blocked/rejected |
```

### 第 10 步：写可控性声明

```markdown
## 参数可控性声明
- controllability_status: FULLY_CONTROLLABLE / FIELD_CONTROLLABLE / CONDITIONALLY_CONTROLLABLE / ALLOWLIST_CONTROLLABLE / TYPE_LIMITED_CONTROLLABLE / DERIVED_CONTROLLABLE / STORED_CONTROLLABLE / SERVER_CONTROLLED / OVERWRITTEN / UNRESOLVED
- trace_status: COMPLETE / PARTIAL / UNRESOLVED
- security_model_status: 记录官方安全模型是否已复核、是否支持当前声明、是否属于预期行为/accepted risk/范围拒绝/known issue 等；具体状态值以对应中文 schema、template 和 validator 为准。
- 已证明:
  - {source、binding、传播、覆盖、防护、sink 参数位置、强正控、负控、官方安全模型}
- 未证明:
  - {分支条件/运行态/对象归属/consumer/最高影响/官方范围或预期行为/...}
- 允许声明:
  - {当前证据能支撑的 candidate/blocked/technical_confirmed/rejected 边界}
- 禁止声明:
  - {不得写完全可控/任意/无需认证/RCE/数据泄露/全局影响/...}
- 停止继续追踪原因:
  - {已达测试上限/防护有效/缺账号对象/缺日志/会越界/缺清理能力/...}
```

## 必检证据点

### Source 与绑定证据

| 证据点 | 必须回答 |
|---|---|
| `EVID_SOURCE_CONTROL` | source 由谁控制，控制粒度是什么 |
| `EVID_PARAM_BINDING` | source 如何绑定到变量、字段、DTO、Model、claim、message、file |
| `EVID_FIELD_MAPPING` | 对象/数组/Map/DTO 内哪个字段继续传播 |
| `EVID_STORED_TAINT_WRITE` | 存储型污染的写入入口、字段、主体 |
| `EVID_STORED_TAINT_READ` | 存储型污染的读取入口、触发条件、后继变量 |
| `EVID_CLAIM_TRUST_BOUNDARY` | session/JWT/OAuth/proxy claim 是否可信 |
| `EVID_IDENTIFIER_ACQUISITION` | 对象 ID、用户 ID、租户 ID、文件 ID、分享 token、lookup handle 或 URI 是否由攻击者可获得；获取路径、主体、规模和边界是什么 |
| `EVID_ACCOUNT_OBJECT_MATRIX` | 多主体、多对象或跨租户场景中，账号、账号对象矩阵必要事实、主体 ID、角色、租户、对象归属、token/cookie 引用和清理责任是什么 |
| `EVID_OFFICIAL_SECURITY_MODEL` | 官方 SECURITY、权限模型、API 文档、默认配置、范围、已知风险、预期行为、accepted risk、范围或官方已知拒绝（外部裁决） 和对外提交限制是否支持当前声明 |

### 传播、覆盖与分支证据

| 证据点 | 必须回答 |
|---|---|
| `EVID_TRACE_HOP_N` | 第 N 跳 file:line、输入、输出、调用关系 |
| `EVID_OVERRIDE_N` | 默认值、硬编码、服务端查询、session 替换是否覆盖 |
| `EVID_BRANCH_CONTROLLABILITY` | sink 分支是否执行，攻击者能否满足条件 |
| `EVID_ACTUAL_USE` | 参数是否真正进入危险语义，而不是只传递 |
| `EVID_TYPE_RANGE_LIMIT` | 类型/范围限制如何缩小控制面 |
| `EVID_ALLOWLIST_VALUES` | 服务端白名单允许哪些值，允许值是否仍危险 |

### 防护与 sink 证据

| 证据点 | 必须回答 |
|---|---|
| `EVID_SINK_PARAM_MAPPING` | source 后继值是否进入 sink 危险参数位置 |
| `EVID_SANITIZER_EFFECT` | sanitizer 是否同变量、同字段、同分支、同上下文且失败阻断 |
| `EVID_AUTH_OBJECT_SCOPE` | 对象级 owner/tenant/ACL 是否在 sink 前绑定 |
| `EVID_FRAMEWORK_SECURITY_CONFIG` | 框架默认防护是否真实启用且覆盖当前入口 |
| `EVID_RUNTIME_CONFIG` | route cache、feature flag、profile、版本、DI 实现是否匹配 |

### 动态、影响与清理证据

| 证据点 | 必须回答 |
|---|---|
| `EVID_STRONG_POSITIVE` | 强正控是否证明真实安全语义 |
| `EVID_NEGATIVE_CONTROL` | 负控是否排除正常功能、缓存、随机、权限本该允许、工具误报 |
| `EVID_IMPACT_PROOF` | 影响是否是受控测试数据、对象、文件、请求、命令、浏览器执行或状态改变 |
| `EVID_CLEANUP` | 副作用是否清理、恢复或证明无副作用 |

## 动态验证触发条件

### 必须动态验证的场景

- 可控性依赖运行态配置、route cache、DI 实现、feature flag、middleware 顺序。
- 可控性依赖账号、对象、租户、session、JWT/OAuth claim、CSRF、签名验证。
- 可控性依赖数据库记录、缓存、队列、文件、对象存储、异步 consumer。
- 条件可控需要证明攻击者能满足分支条件。
- IDOR/越权需要双主体、双对象、双租户对照。
- 对象标识符、分享 token、lookup handle、资源 URI 的可控性依赖攻击者是否能从自身入口获得。
- 多对象、批量、全量、全租户或广义影响依赖 ID 是否能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得。
- SSRF、文件访问、上传、命令执行、状态改变、组件可达性需要运行态影响证明。
- 扫描器结果要升级 technical_confirmed。
- 可控性结论要进入漏洞报告、复核结论或 对外提交声明，需要确认官方安全模型、范围、默认配置、已知风险和预期行为是否支持当前声明。
- 弱 payload 失败但代码 trace 仍可疑，需要确认 payload 是否到达 sink、观察点是否正确、防护是否真实阻断。

### 静态证据只能进入 candidate 的场景

- source、binding、trace、sink 静态证据完整，但缺运行环境、账号、对象、强正控、负控或影响证明。
- 可控性为 `UNRESOLVED`，但有明确字段级传播和 sink 线索。
- 白名单、类型转换、授权逻辑、parser 配置、框架默认防护需要运行态确认。
- 存储型 taint 有写入端和读取端线索，但缺同环境闭合验证。
- 官方安全模型、scope、默认配置、known issue、accepted risk、expected behavior、范围或官方已知拒绝（外部裁决） 或对外提交限制未读完时，不能把可控性结论写成对外可提交。

### 不能继续动态验证的场景

- 会越出授权范围、访问第三方真实系统、触碰真实生产用户数据或真实凭据。
- 会造成不可控拒绝服务、批量破坏、不可逆修改、不可清理文件写入、持久化后门或难以回滚的配置变更。
- 没有自有或明确允许的测试环境、测试账号、对象数据、前置快照、日志访问或回滚能力。
- 只能通过危险且不可控的 payload 观察，无法隔离、无法清理、无法限制影响范围。

此时必须降级为 `candidate` 或 `blocked`，并写清缺口；不得为了升级 `technical_confirmed` 扩大测试范围。

## 授权实验模式下的强验证方法

以下方法只用于自有、授权、隔离、可重置环境。payload 必须按代码 sink、测试账号、测试对象、可清理副作用和日志观察点选择；不要复制通用 payload 代替上下文判断。

### 请求组织

至少准备四类请求或操作：

1. **baseline**：正常值，证明入口、handler 和正常业务路径可达。
2. **strong positive**：足以证明当前 sink 危险语义的受控输入。
3. **negative control**：移除字段、安全值、非法值、无权限主体、其他对象/租户、修复后配置。
4. **cleanup/restore**：删除测试记录、文件、缓存、队列，关闭临时服务或恢复快照。

请求记录模板：

```markdown
| 请求 | 改动变量 | 账号/对象 | 预期观察点 | 实际结果 | 结论 |
|---|---|---|---|---|---|
| baseline | 正常值 | A/A对象 | 正常响应 | `{status/log}` | 入口可达 |
| strong_positive | `{field}` | A/B测试对象 | sink 差异/副作用 | `{evidence}` | 参数影响危险语义 |
| negative_control | 移除/安全/非法/不同主体 | A/B/T | 差异消失或被阻断 | `{evidence}` | 排除误报 |
| cleanup | 删除测试副作用 | 测试资源 | 状态恢复 | `{evidence}` | 可清理 |
```

### 漏洞族强验证目标

| 漏洞族 | 不够的弱证明 | 授权环境内应追的强证明 |
|---|---|---|
| SQL/NoSQL | error-only、单个异常栈 | 布尔/时间稳定差异、常量回显、测试表读取/写入、count/schema 元信息、对象越权查询 |
| SSRF | DNS callback-only、URL 可控 | 最终 URL/IP、重定向后目标、DNS/IP 校验绕过、受控内网 canary、metadata mock、响应可读性 |
| CMD/RCE | marker-only、函数名命中 | stdout/stderr、退出码、执行用户、工作目录、受控文件、受控回连 |
| FILE | path 拼接、错误信息 | resolved target、base 内外边界、受控读写、写后可达、覆盖模式、清理恢复 |
| Upload/Archive | 文件名可控、上传成功 | 存储落点、扩展/MIME/magic、web 可达性、二次解析、entry traversal、执行/非执行边界 |
| XSS/TPL | reflect-only、HTML 回显 | 浏览器执行、DOM 改变、存储触发、目标角色触发、CSP/autoescape 影响 |
| Auth/IDOR | id 可替换、已知 ID 后可访问 | A/B 账号、A/B 对象、跨租户、owner/victim 视角、ID 获取链、敏感字段或状态改变 |
| Secret/Config | regex 命中 | 攻击者可获得、非占位符、权限范围、轮换状态、最小权限只读 metadata |
| SCA/组件 | version-only | 实际打包加载、配置启用、调用点可达、输入可控、触发条件成立 |

### 弱 payload 失败后的复核顺序

弱正控失败时，不要直接 rejected。按顺序检查：

1. route 是否命中。
2. handler 是否执行。
3. source 是否绑定到目标字段。
4. payload 是否被 body parser、schema、类型转换或编码改变。
5. 分支条件是否满足。
6. sink 是否执行。
7. sink 上下文是否匹配 payload。
8. 日志/响应/副作用观察点是否正确。
9. 防护是否真实同变量、同字段、同分支、同上下文阻断。
10. 是否需要换同类强 payload、编码变体、二次触发或运行态配置。

只有完成这些复核并有排除证据，才能写 `rejected`。

## 最高危害追踪

对每条可控性成立的候选，按以下阶梯推进，直到达到授权环境内最高可证明影响或明确停止原因：

```text
可触发 -> 可控 -> sink 执行 -> 强正控 -> 可读/可写/可越权/可执行/可横向 -> 负控 -> 清理 -> 声明边界
```

停止继续追踪必须写具体原因：

- 已达到当前测试范围内最高可证明影响。
- 防护经同变量、同字段、同分支、同上下文证据证明有效。
- 缺测试账号、对象、日志、回连、快照或清理能力。
- 继续验证会越出授权范围、触碰真实生产数据、真实凭据或第三方系统。
- 当前环境不支持触发该 sink，需要运行态补证。
- 当前 claim 已经足够，继续升级只会增加不可清理副作用。

禁止把低层现象夸大：callback-only SSRF 不能写内网敏感访问；marker-only RCE 不能写命令执行；error-only SQLi 不能写数据读取；reflect-only XSS 不能写浏览器执行；version-only SCA 不能写组件可达；secret-regex-only 不能写有效凭据泄露。

## 负控设计

负控用于增强证据，不是削弱验证。负控要和 claim 对齐，每次只改变一个关键变量。

| 发现类型 | 必要负控 |
|---|---|
| SQL/NoSQL | true/false、time/no-time、安全值、非法 operator、参数化修复、不同权限/租户 |
| RCE/CMD | 普通值、移除字段、禁止命令、命令输出差异、修复后阻断 |
| SSRF | 允许 host、禁止 host、重定向后禁止目标、本地 canary 与外网 canary、DNS/IP 对照 |
| XSS/TPL | 编码后值、不同输出上下文、raw/safe 关闭、CSP/模板安全模式、不同角色触发 |
| FILE | base 内合法文件、base 外 canary、不存在文件、编码/双编码、symlink 对照 |
| UPLOAD/ARCHIVE | 安全扩展、禁止扩展、base 内/外 entry、magic/MIME 不匹配、执行禁用策略 |
| IDOR/AUTH | 账号 A 对象 A、账号 A 对象 B、账号 B 对象 B、跨租户、无登录、低权限/高权限 |
| CSRF | 正确 token、缺 token、错误 token、Origin/Referer/SameSite、不同 content-type |
| SCA/组件 | 组件未加载、修复版本、不可达调用点、缺触发输入、默认安全配置 |
| Secret | 占位符、吊销、权限不足、不可由攻击者获得、最小权限 metadata 对照 |

`technical_confirmed` 至少要有一个与 claim 对齐的负控；高危/严重结论通常需要多组负控。

## technical_status 方法性判定边界

### technical_confirmed

必须同时满足：

- 入口可达。
- source 控制主体与控制粒度已证明。
- 参数绑定清楚。
- trace_status 为 `COMPLETE`，或静态 trace 与运行态证据等价闭合。
- 参数到达 sink 危险参数位置。
- 参数被实际使用，而不是只传递、只记录或只展示。
- 覆盖/防护不足，缺口具体。
- 可控条件能被攻击者满足。
- 若参数是对象 ID、租户 ID、文件 ID、分享 token、lookup handle 或资源 URI，攻击者获得路径已证明，且声明范围不超过可获得规模。
- 若结论依赖多主体、多对象、owner/victim 或跨租户，账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离和清理责任已证明。
- 若结论将写入漏洞报告、复核结论或 对外提交声明，`EVID_OFFICIAL_SECURITY_MODEL` 已证明官方资料、scope、默认配置、known issue、accepted risk、expected behavior、范围或官方已知拒绝（外部裁决） 与当前声明不冲突。
- 强正控证明真实影响或最高可证明影响。
- 至少一个负控成立。
- 有清理/恢复证据，或验证无不可清理副作用。
- 声明边界清楚。

### candidate

用于这些情况：

- source/sink 有线索，但中间层或字段级映射缺失。
- 参数可能可控，但覆盖条件、白名单、类型转换或授权逻辑未判定。
- 条件可控，但缺证明条件可由攻击者满足。
- 存储型可控，但缺写入端或读取端闭合。
- 有扫描器 taint trace，但未人工核对 binding、field mapping、sanitizer、actual use。
- 有 sink-only、source-only、route-only 或 regex-only 静态命中，只能进入待补证风险池。
- 弱正控失败但尚未证明路径不可达、防护有效或观察点正确。
- 对象 ID 可传入且影响对象选择，但目前只有手工样本 ID、管理员视角 ID、历史报告 ID 或单个不可泛化 ID，尚未证明攻击者可获得路径。
- 多对象、批量、全量或跨租户声明缺少 ID 获取规模、账号矩阵或对象归属负控。
- 官方安全模型、范围、默认配置、known issue、accepted risk、expected behavior 或 范围或官方已知拒绝（外部裁决） 未裁决；可控性可继续追踪，但不能写对外可提交。

### blocked

用于必须依赖运行态才能裁决的情况：

- 需要测试账号、对象、租户、CSRF、session、JWT/OAuth claim。
- 需要 route cache、middleware 顺序、feature flag、运行版本、构建产物。
- 需要数据库、缓存、队列、文件、对象存储、DNS/HTTP 回调、浏览器环境。
- 需要双主体、双对象、双租户负控。
- 需要运行态确认对象标识符是否能由攻击者列表、搜索、导出、日志、关系链、分享页、可预测序列或批量接口获得。
- 需要补齐账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离或清理能力。
- 需要运行态或官方资料确认该行为是否违反安全边界、是否默认配置受影响、是否属于预期行为、accepted risk、范围或官方已知拒绝（外部裁决） 或 hardening only。
- 需要快照、重置或清理能力才能做强验证。

### rejected

只有具备排除证据时才写：

- 入口不可达或未注册。
- source 不可控或只在前端存在。
- source 未绑定到目标变量。
- 参数未进入 sink 或未进入危险参数位置。
- 参数被无条件覆盖。
- 类型、白名单、参数化、canonicalize、授权防护完全阻断当前风险。
- 强正控与负控证明参数变化不影响 sink 或影响不成立。
- 依赖对象标识符的结论，经代码、接口和运行态证据证明攻击者无法获得必要 ID，且不存在可列表、搜索、导出、关系链、分享页、可预测或可推导路径。
- 多主体/多对象结论经 A/B 主体对象负控证明为正常授权、公开对象、自己对象或权限本该允许。
- 官方安全模型明确该行为是预期行为、受信任主体正常能力、accepted risk、范围或官方已知拒绝（外部裁决） 或 hardening only，且没有更低权限主体越界证据。
- 弱 payload 失败后经过路径、sink、观察点、防护语义复核，确认不可控或防护有效。

### 必须降级的场景

- scanner-only、external-tool-only、sink-only、source-only、route-only、regex-only。
- trace_status 为 `PARTIAL/UNRESOLVED`。
- controllability_status 为 `UNRESOLVED`。
- 无负控。
- 只有 200 响应。
- 只有 marker 回显但无 sink 参数证据。
- callback-only SSRF。
- marker-only RCE。
- error-only SQLi。
- reflect-only XSS。
- 拿不到对象归属差异的 IDOR。
- version-only 组件漏洞。
- 只有错误信息或日志片段，无安全影响。
- 弱 payload 失败但未完成路径、sink、观察点、防护语义复核。
- 只有“已知 ID 后可利用”，没有证明攻击者如何获得 ID。
- 只有单个手工样本 ID，却声明批量、全量、全租户、全用户、全工作区或广义影响。
- 多主体结论缺账号矩阵、账号对象矩阵必要事实、对象归属或 token/cookie 隔离。
- 官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、accepted risk / expected behavior / 范围或官方已知拒绝（外部裁决） 未裁决，却写对外可提交或强漏洞声明。

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

修复建议必须对应可控性根因，不要写泛泛“过滤输入”。

- 参数化：值位置使用绑定参数；动态表名、列名、排序、operator、模板名、路径段、URL host 使用服务端白名单。
- 白名单：允许值由服务端维护；失败必须阻断；允许值本身也要无危险语义。
- 类型与范围：对 int/UUID/date/enum 做严格转换，转换失败阻断；不要静默回退到危险默认值。
- 对象级授权：在 service/repository/model 层把当前主体、tenant、owner 绑定到查询和写入条件；批量接口逐项校验。
- Mass assignment：只允许显式字段；敏感字段如 role、tenant、owner、price、status、permission、isAdmin 由服务端计算。
- Over-posting：输入模型与持久化模型分离；更新接口只接收当前操作允许修改的字段；拒绝未知字段并为敏感字段写回归测试。
- Claim/session：固定 JWT 算法，校验 exp/nbf/iss/aud，禁止信任可伪造 header；session 登录后更新 ID。
- Parser 安全：XML 禁外部实体和网络；反序列化限制类型；模板沙箱和自动转义。
- 上传安全：随机文件名、magic/MIME/扩展校验、web 根外存储、禁执行、下载鉴权、二次处理复核。
- 路径归一化：decode/canonicalize/realpath 后做 base 约束，拒绝符号链接逃逸和不存在路径回退。
- SSRF：scheme/host/port allowlist，DNS/IP 后校验，重定向后重新校验，拒绝 metadata/内网。
- 输出编码：按 HTML、attribute、JS、CSS、URL、JSON、header 上下文分别编码。
- 日志脱敏：token、cookie、password、secret、PII 不进入低权限可读日志。
- 密钥管理：密钥移出仓库，最小权限、轮换、签名上下文和过期时间。
- 依赖升级：升级后仍需确认危险调用点配置安全和可控性被阻断。
- 测试：为 source→sink、字段级映射、负控、权限矩阵、修复后阻断写单元/集成/回归测试。

## 禁止事项

- 禁止 sink-only technical_confirmed。
- 禁止 scanner-only technical_confirmed。
- 禁止 external-tool-only technical_confirmed。
- 禁止 regex-only technical_confirmed。
- 禁止 source-only technical_confirmed。
- 禁止 route-only technical_confirmed。
- 禁止没有 trace 就 technical_confirmed。
- 禁止 trace_status=PARTIAL/UNRESOLVED 仍写 technical_confirmed。
- 禁止 controllability_status=UNRESOLVED 仍写 technical_confirmed。
- 禁止没有负控就写高置信。
- 禁止只看 200 响应。
- 禁止只看 marker 回显就写可控性 technical_confirmed。
- 禁止把框架默认安全假设当证据。
- 禁止把客户端限制、前端下拉、Swagger enum、TypeScript 类型当服务端白名单。
- 禁止把 sanitizer 名称当防护结论，必须看语义和上下文。
- 禁止把不可解析的动态调用、接口实现、异步消费端强行补全为证据。
- 禁止把“不可控”与“无风险”混为一谈；只能说当前参数链路不成立。
- 禁止弱 payload 失败后跳过 route、handler、sink、观察点复核就 rejected。
- 禁止把 callback-only SSRF 写成内网敏感访问 technical_confirmed。
- 禁止把 marker-only RCE 写成命令执行 technical_confirmed。
- 禁止把 error-only SQLi 写成数据读取 technical_confirmed。
- 禁止把 reflect-only XSS 写成浏览器执行 technical_confirmed。
- 禁止把 version-only SCA 写成组件可达 technical_confirmed。
- 禁止把 secret-regex-only 写成有效凭据泄露 technical_confirmed。
- 禁止把“已知 ID 后可利用”写成高价值 technical_confirmed，却不证明攻击者如何获得该 ID。
- 禁止把单对象 ID 样本外推成批量、全租户、全用户、全工作区或广义影响。
- 禁止把管理员手工给出的 ID、聊天上下文里的 ID、历史附件里的 ID、报告作者笔记里的 ID 当作攻击者可获得路径。
- 禁止账号矩阵缺账号对象矩阵必要事实、主体 ID、租户、对象归属、token/cookie 引用和清理责任时声称多主体 technical_confirmed 可复核。
- 禁止官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior / accepted risk / 范围或官方已知拒绝（外部裁决） 未裁决时写对外可提交。
- 禁止官方资料已经说明是预期行为、受信任主体正常能力、范围外或 hardening only 时，仍把可控性结论升级成漏洞 technical_confirmed。
- 禁止为了凑数量写低价值漏洞。
- 禁止把项目运行、部署、恢复、调度、监控内容混进漏洞审计 skill。
- 禁止把当前工作记录、来源叙事、不可公开的环境细节、内部命名或临时任务过程写进通用 skill。
- 禁止越出授权范围、测试第三方真实目标、导出真实凭据、泄露真实生产用户敏感数据或执行不可清理验证。

## 自检清单

每项回答 `是 / 否 / 不适用`。

### Source 与绑定

- [ ] 是否识别 query/path/body/header/cookie/JSON/XML/multipart/file/session/claim/message？
- [ ] 是否识别 GraphQL/WebSocket/CLI/webhook/queue/cron/file import？
- [ ] 是否证明 source 的控制主体和控制粒度？
- [ ] 是否记录 handler 参数、DTO/Model/Serializer/FormRequest/Pydantic/ModelBinder/strong parameters？
- [ ] 是否区分直接输入、stored taint、claim/session、服务端配置和数据库查询结果？
- [ ] 对 JWT/session/proxy header 是否判断签名、issuer、audience、exp、算法、代理边界？
- [ ] 若 source 是对象 ID、租户 ID、文件 ID、分享 token、lookup handle 或资源 URI，是否证明攻击者如何获得？
- [ ] 是否区分手工样本 ID、管理员视角 ID、公开/可获得 ID 和攻击者可批量获得 ID？

### Trace 与字段映射

- [ ] 是否从入口追到 handler/controller/resolver/consumer？
- [ ] 是否从 handler 追到 service、repository、mapper、model、helper、client？
- [ ] 是否处理父类、接口、trait、helper、middleware、decorator、依赖注入、注解/attribute、AOP、反射？
- [ ] 是否处理事件、队列、定时任务、异步消费端？
- [ ] 是否记录字段级映射，而不是只记录对象名？
- [ ] 是否记录每一跳 `file:line`、变量名、输入/输出、分支？
- [ ] 如果 trace 涉及对象选择，是否证明 ID 选择的是目标对象而不是被服务端重绑定到当前主体？
- [ ] 如果 trace 涉及多主体、多对象或跨租户，是否有账号矩阵和对象归属证明？

### 覆盖与防护

- [ ] 是否识别无覆盖、无条件覆盖、空值默认、条件覆盖、白名单、类型转换、服务端查询覆盖、权限覆盖？
- [ ] 是否判断覆盖条件语义，而不是只匹配方法名？
- [ ] 是否区分 transform 与 sanitizer？
- [ ] 是否确认防护作用在同一变量、同一字段、同一分支、同一上下文？
- [ ] 是否确认参数化覆盖全部动态片段？
- [ ] 是否确认白名单是服务端允许列表，且允许值本身安全？
- [ ] 是否确认类型转换/范围限制是否仍允许当前漏洞类型？
- [ ] 是否确认对象级授权和 tenant/owner 条件在 sink 前执行？

### Sink 与实际使用

- [ ] 是否定位 sink API、危险参数位置和执行条件？
- [ ] 是否区分值型 sink、结构性 sink、权限型 sink、解析型 sink？
- [ ] 是否证明参数进入危险参数，而不是非危险参数？
- [ ] 是否判断参数是否被实际使用，而不是只传递？
- [ ] 是否判断 sink 所在分支可执行？

### 动态验证与负控

- [ ] 是否写出 baseline、强正控、移除字段、非法值、安全值、不同主体/对象/租户负控？
- [ ] 是否使用唯一 marker、测试账号、测试对象和可清理副作用？
- [ ] 是否记录日志观察点和副作用观察点？
- [ ] 是否为 technical_confirmed 提供至少一个负控？
- [ ] IDOR/Auth 是否包含 A/B 主体、A/B 对象、跨租户或 control 对象负控？
- [ ] 批量/广义影响是否证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得？
- [ ] 不能动态验证时是否降级并说明原因？
- [ ] 弱 payload 失败时是否先复核路径、payload、权限、对象、sink 和观察点，而不是直接 rejected？

### 判定与报告

- [ ] 是否给出 trace_status：COMPLETE/PARTIAL/UNRESOLVED？
- [ ] 是否给出 controllability_status：FULLY/FIELD/CONDITIONAL/ALLOWLIST/TYPE_LIMITED/DERIVED/STORED/SERVER/OVERWRITTEN/UNRESOLVED？
- [ ] 如果要进入漏洞报告或 对外提交资格，是否给出 security_model_status 并裁决 SECURITY、权限模型、API 文档、默认配置、scope、known issue、accepted risk、expected behavior、范围或官方已知拒绝（外部裁决）？
- [ ] 是否给出 finding 状态：technical_confirmed/candidate/blocked/rejected？
- [ ] 是否说明 candidate/blocked 缺哪些证据？
- [ ] 是否说明 rejected 的排除证据？
- [ ] 是否避免“已知 ID 后可利用”直接写高价值 technical_confirmed？
- [ ] 是否避免单对象结果外推成批量、全量或广义影响？
- [ ] 是否避免 scanner-only、external-tool-only、sink-only、source-only、route-only、regex-only、无负控 technical_confirmed？
- [ ] 是否避免官方安全模型 unknown 或与声明冲突时写对外可提交或 technical_confirmed？
- [ ] 是否写清 Source、参数可控性矩阵、Sink、Trace、防护缺口、复现、Web 操作、强正控、负控、影响证明、修复建议、Allowed Claims、Forbidden Claims、声明边界？
- [ ] 是否去除了不可公开的环境细节、内部命名、来源叙事、当前工作记录和运行维护术语？
