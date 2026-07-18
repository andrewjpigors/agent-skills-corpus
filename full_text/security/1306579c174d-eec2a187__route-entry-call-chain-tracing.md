---
name: route-entry-call-chain-tracing
description: Use when enumerating application entry points, resolving route-to-handler mappings, or tracing whether a request, message, job, stored value, object identifier, or 对外提交资格 security claim can actually reach a sensitive sink through middleware, authorization, dynamic dispatch, service layers, repositories, events, queues, cron jobs, imports, webhooks, RPC, GraphQL, WebSocket, or CLI entry points.
---

# 路由入口与调用链追踪

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

这个 Skill 只解决一件事：**某个入口是否真的能把攻击者可控输入送到敏感 sink**。

使用顺序：

1. 先认入口：HTTP、GraphQL、WebSocket、RPC、CLI、webhook、queue、event、cron、file import、plugin hook 都要纳入入口表。
2. 再认路由：method、path、host、header、content-type、params、priority、fallback、route cache、gateway rewrite 都要逐项核对。
3. 再认 handler：要落到真实 class、function、method、consumer、job、resolver、callback，而不是只停在 URL 名字。
4. 再展开链路：middleware、filter、interceptor、guard、policy、gate、AOP、DI、trait、mixin、decorator、dynamic dispatch 都要追。
5. 再追 sink：service、use case、manager、repository、DAO、mapper、model、helper、client、parser、template、filesystem、queue、HTTP client、command。
6. 若链路依赖对象标识符：先证明 `user_id/object_id/tenant_id/workspace_id/file_id/share token/lookup handle/URI` 等标识符如何由攻击者获得，不能把手工样本 ID 当成攻击者能力。
7. 若链路依赖多主体、多对象或跨租户：建立账号对象矩阵，记录 attacker、owner、victim、control、cleanup 的账号用途、账号对象矩阵必要事实、主体 ID、租户/工作区、角色、token/cookie 引用、对象归属和清理责任。
8. 若链路准备写入报告：裁决官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和外部门禁引用。
9. 最后裁决：入口、路由、handler、链路、sink、标识符获取、账号矩阵、官方安全模型、正控、负控、清理、停止原因一起看，才能写结论。

不适用场景：

- 只想写报告文案，不需要证明入口与调用链。
- 只想看某个漏洞族的 payload、绕过或修复细节；应转到漏洞专项。
- 只想做部署、恢复、监控、调度、容器维护。
- 没有代码、配置、运行态材料或授权环境，却要求直接写 technical_confirmed。

## 核心原则

### 1. route-only 不是 technical_confirmed

路由文件、OpenAPI、Swagger、WSDL、GraphQL schema、菜单、前端请求、扫描器 URL 只能说明“可能存在入口”，不能直接说明“可利用”。

要写 technical_confirmed，必须继续证明：

```text
入口已注册 -> 请求能匹配 -> handler 已解析 -> 中间件/权限路径清楚 -> 参数绑定清楚 -> 调用链闭合 -> sink 可达 -> 强正控成立 -> 负控排除误报 -> 清理完成
```

以下都不得单独升级为 technical_confirmed：

- 只有路由定义。
- 只有 API 文档。
- 只有 HTTP 200。
- 只有 handler 名称或 controller 名称。
- 只有 queue publish，没有 consumer。
- 只有 cron 定义，没有任务执行。
- 只有前端页面、菜单或动态路由。
- 只有扫描器 call graph。
- 只有 外部模型/工具自述。

### 2. 路由匹配是多条件匹配

一个请求能否命中 handler，不只看 path。必须同时判断：

- method：GET、POST、PUT、PATCH、DELETE、HEAD、OPTIONS、RPC method、GraphQL operation、WebSocket event。
- path：context path、base path、group prefix、locale、version、namespace、subdomain、router mount。
- 条件：host、header、params、content-type、accept、consumes、produces、route regex、type converter、enum。
- 顺序：priority、fallback、wildcard、resource route、auto route、terminal middleware、short-circuit。
- 运行态：route cache、compiled route、feature flag、profile、plugin registration、module provider、gateway rewrite、proxy。

### 3. handler 命中不等于 sink 可达

handler 之后仍可能被这些因素阻断：

- 认证、授权、对象级权限、tenant、policy、gate、guard、filter、interceptor。
- body parser、schema validation、DTO binding、model binding、route model binding、parser config。
- if/switch/try/catch、早退、异常吞掉、redirect、default value、硬编码覆盖。
- service 接口多实现、依赖注入 profile、AOP、decorator、dynamic proxy。
- 事件/队列/cron/file import 的异步消费端未注册、未运行或消费不同 topic/schema。
- sink 所在分支需要特殊对象状态、角色、配置或 feature flag。

### 3.1 路由可达不等于安全边界被违反

入口、路由、handler、middleware 和 sink 全部闭合，也只能证明“代码路径可达”。若要推进授权或对象边界声明，还必须填写 Actor×Action×Resource：谁(actor)在什么认证/信任级别下，对什么资源(resource)执行什么动作(action)，项目应有权限是什么，实际结果是什么，裁决是否违反边界。如果该路径准备写成漏洞报告，还必须判断它是否违反官方声明的安全边界。官方 SECURITY、安全策略、API 文档、权限模型、对象模型、默认配置、release note、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决）、safe harbor 和提交材料质量要求，都会改变最终声明。

常见降级：

| 路由链路现象 | 官方模型裁决 | 正确结论 |
|---|---|---|
| 管理员路由能执行 SQL、命令、导入脚本或危险配置 | 官方把管理员/部署者定义为受信任主体，且没有低权限绕过 | expected admin capability / hardening only |
| 插件、脚本、工作流、沙箱入口能执行代码 | 官方定义为插件作者或脚本作者能力，且没有沙箱逃逸或跨主体影响 | expected plugin/sandbox capability |
| URL preview、webhook、导入、文件预览能请求外部资源 | 官方定义为正常 URL fetch，但没有内网响应可读、metadata mock、状态改变或跨边界影响 | expected fetch 或 candidate |
| 路由只在 debug、本地、示例配置、危险开关或非默认 profile 下暴露 | 默认配置和 scope 未证明 | blocked / needs-official-baseline |
| 路由链路强正控成立 | 官方模型未读完、known issue 未去重、accepted risk 未裁决 | 需要外部门禁裁决 或 candidate |

检验句：**我证明的是未受信任主体跨越了官方保护边界，还是只证明了一个官方预期功能的路由能被调用？**

### 3.2 入口命中也不等于对象可攻击

越权、IDOR、对象级授权、批量导出、跨租户访问、文件访问、工作区资源访问等链路，入口命中和 handler 命中只能说明“请求能到代码”，不能说明“攻击者能拿到目标对象”。必须额外证明：

1. **必需标识符**：这条入口链路需要哪些 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、资源 URI 或物理表名。
2. **攻击者获取路径**：这些标识符来自攻击者可达的列表、详情、搜索、导出、日志、关系链、分享页、客户端状态、可预测序列、分页接口、批量接口，还是仅来自管理员手工提供、报告作者笔记、聊天上下文或旧附件。
3. **规模边界**：只能获得单个对象、同类多个对象、分页批量、持续同步、可枚举、可推导，还是不可获得。
多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

只有“已知 ID 后请求成功”时，不能写高价值 `technical_confirmed`。如果删掉手工样本 ID 后攻击者无法自己获得目标 ID，只能写窄化 `candidate`、`blocked`，或在有排除证据时写 `rejected`。如果要声明批量、全量、全用户、全租户、全工作区或广义影响，必须证明标识符能批量、持续、列表、搜索、导出、关系链、枚举或可推导获得。

### 4. 多方法入口必须拆开

很多框架会把多个业务方法藏在一个入口下：resource route、自动路由、通配符路由、GraphQL resolver、RPC service、WebSocket event、`/dispatch`、WordPress hook、Struts 通配符、Laravel/Rails resource route。

必须逐方法记录：触发字段、参数、handler、权限、防护、sink 和状态；不能把一个方法的证据复制给另一个方法。

### 5. 默认在授权可重置环境里做强验证

在自有 Docker、CTF、靶场、本地、隔离预发或其他明确授权、可重置、可观察环境中，允许用强正控证明真实影响；但必须只用测试账号、测试对象、测试文件、测试表、受控回连和可清理副作用。

边界是：不越出授权范围，不测试第三方真实系统，不读取真实用户数据，不复用真实生产凭据，不制造不可清理影响。

## 审计目标

本 Skill 的目标不是列 URL，而是产出一条可复核的入口与调用链证据。

一次合格追踪应回答：

1. 入口在哪里定义，是否被当前运行配置加载。
2. 请求或任务如何匹配入口，哪些条件会导致不匹配。
3. 入口对应哪个 handler、controller、action、resolver、command、consumer、job。
4. 哪些 middleware、filter、interceptor、guard、policy、dependency 在 handler 前后执行。
5. 参数如何从 source 绑定到 handler 变量。
6. 参数如何穿过 service、use case、manager、repository、mapper、model、helper、client 或异步边界。
7. 哪个分支、权限或配置决定 sink 是否执行。
8. sink 的危险参数位置是什么，是否被目标 source 污染。
9. 运行态如何证明 route match、handler hit、auth decision、sink execution 和副作用。
10. 如果入口链路依赖对象标识符，攻击者如何获得该 ID、handle、token 或 URI；结论能写到单对象、多对象、批量、持续、可枚举还是不可获得。
11. 如果入口链路依赖多账号、多对象、owner/victim、跨租户或清理动作，账号矩阵是否可复核，内部材料是否有账号对象矩阵必要事实。
12. 哪些声明允许写，哪些必须禁止或降级。
13. 如果入口链路要写入漏洞报告、复核结论或对外提交，官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和 外部门禁是否支持该声明。

## 输入材料

### 入口与路由材料

- HTTP 路由：route 文件、注解、attribute、decorator、resource route、auto route、fallback、route cache、compiled route、API gateway、reverse proxy、rewrite。
- GraphQL：schema、resolver、operation、mutation、query、subscription、directive、context、auth middleware。
- WebSocket：gateway、channel、room、event name、message schema、connect auth、broadcast scope。
- RPC/SOAP/gRPC：service definition、WSDL、proto、method list、endpoint address、transport binding、auth metadata。
- CLI/cron/job：command registry、argv、stdin、schedule、worker registration、job handler、profile、env。
- webhook/event/queue：route、topic、routing key、event class、producer、consumer、listener、retry、dead-letter。
- file import：watcher、upload/import endpoint、parser、row/object mapping、import job、post-processing。
- plugin/hook：hook name、callback registration、priority、activation condition、autoload、include。

### 中间件与安全边界材料

- Authentication、Authorization、RBAC、ABAC、object permission、tenant resolver。
- CSRF、CORS、rate limit、signature/HMAC、nonce、timestamp、method override。
- body parser、upload parser、content negotiation、schema validation、form request、serializer。
- framework security chain、filter chain、interceptor order、before/after action、decorator、AOP。
- skip、except、only、permitAll、anonymous、public route、withoutMiddleware、AllowAnonymous 等排除配置。

### 调用链与资源层材料

- Controller、Action、Handler、Resolver、Endpoint。
- Service、Use case、Manager、Domain service、Command handler。
- Repository、DAO、Mapper、Model、Entity、Query builder、ORM scope。
- Helper、trait、mixin、concern、base class、abstract class、interface implementation。
- HTTP client、filesystem、object storage、cache、queue、template、parser、deserializer、auth decision。
- 构建与运行配置：lockfile、module provider、DI/container binding、profile、feature flag、实际打包版本、镜像。

### 运行态材料

- 正常请求、强正控请求、负控请求。
- Burp、DevTools、curl、browser steps。
- route list、debug route、endpoint list、framework introspection 输出。
- handler 日志、auth 日志、SQL/HTTP/file/cache/queue 日志、异常栈。
- 数据库、文件、缓存、队列、对象存储、回连服务、业务状态副作用。
- 测试账号、测试对象、测试租户、测试 token、测试文件、快照、回滚、清理方式。
- 多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。
- 标识符获取材料：对象 ID、用户 ID、租户 ID、工作区 ID、文件 ID、分享 token、lookup handle、资源 URI、物理表名来自列表、详情、搜索、导出、日志、关系链、分享页、客户端状态、可预测序列还是批量接口；必须区分手工样本、单对象可得、多对象可得、批量可得、持续可得、可推导和不可得。

### 官方安全模型材料

当入口链路准备支撑 `technical_confirmed`、高危、严重、未认证、低权限、跨用户、跨租户、默认配置受影响、RCE、SSRF 内网访问、文件越界、沙箱逃逸、有效凭据泄露、任意对象访问或其他 对外提交声明时，必须收集官方安全模型材料：

- SECURITY、安全策略、披露范围、测试限制、safe harbor、范围或官方已知拒绝（外部裁决）、提交材料质量要求。
- README、部署文档、默认配置、示例配置、生产建议、危险功能开关、debug/local/admin-only 条件。
- API 文档、权限模型、角色说明、scope、ACL、对象归属、多租户/组织/workspace/project/file/token/secret 隔离说明。
- 框架或产品文档中对路由、middleware、guard、policy、CSRF、CORS、object permission、tenant resolver、plugin、webhook、URL fetch、file import、sandbox 的设计说明。
- release note、changelog、migration guide、security advisory、known issue、known limitation、duplicate、accepted risk、expected behavior、won't fix。

官方材料不是停止强验证的借口；它用于解释强验证结果是否能作为新漏洞提交。没有官方门禁时，不得把“路由可达 + sink 可达”直接写成对外可提交。

## Source 识别

本 Skill 只做入口相关 Source 识别；深层 taint 细节应转到 Source→Sink 专项。

### HTTP / API Source

Source 要按“来源 + 绑定 + 主体 + 条件”记录：

- query：`id`、`ids`、`url`、`path`、`file`、`name`、`sort`、`order`、`filter`、`callback`、`returnTo`、`redirect`、`template`、`expr`、`operator`、`tenant`、`page`、`limit`。
- path：`/{id}`、slug、filename、wildcard、regex capture、extension、tenant path、locale、version、resource action。
- body：form、JSON、XML、GraphQL variables、protobuf、nested object、array、bulk list、operator object、patch document。
- header：Authorization、Host、Origin、Referer、X-Forwarded-*、Content-Type、Accept、User-Agent、自定义签名头、callback header。
- cookie：session、remember-me、tenant、locale、业务偏好。
- multipart：文件名、content-type、文件内容、普通字段、压缩包 entry name。

### 非 HTTP / 二次污染 Source

- CLI argv、stdin、环境变量、导入文件、CSV、Excel、XML、JSON、YAML、ZIP、TAR、office 文档。
- webhook payload、OAuth/OIDC/SAML claim、支付、消息、代码仓库回调。
- queue message、event bus payload、workflow form、cron 读取记录。
- 数据库、缓存、文件和对象存储中的存储型污染：必须证明攻击者能先写入，再由后续入口读取。
- 前端/客户端代码中的隐藏参数、签名参数、硬编码 key、Authorization 生成逻辑：只有后端接受并信任时才成为后端 source。

### 对象标识符 Source

入口链路里的对象标识符必须拆成“可传入、可选择、可获得、可越权/可批量”四层：

| 层级 | 入口追踪要证明什么 | 不足时的结论 |
|---|---|---|
| 可传入 | ID / handle / token / URI 能从 path、query、body、header、message、file row、GraphQL variables 或 WebSocket payload 进入 handler | 只能说明有入口 source |
| 可选择 | 该值影响对象 lookup、query condition、repository 参数、policy 判断、导出范围、文件路径或批量元素 | 只能说明对象选择受影响 |
| 可获得 | 攻击者能从自身可达入口获得目标标识符：列表、详情、搜索、导出、日志、关系链、分享页、分页、客户端状态、可预测序列或批量接口 | 缺失时不能高价值 technical_confirmed |
| 可越权 / 可批量 | A/B 主体对象负控成立；若声明批量，证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得 | 缺失时只能窄化或降级 |

管理员手工给出的 ID、报告作者笔记里的 ID、聊天上下文里的 ID、历史附件里的 ID，只能作为定位样本，不能当作攻击者可获得路径。

### 框架 Source 差异点

| 生态 | 标准机制 | 需要警惕的 source 差异 |
|---|---|---|
| ThinkPHP | Request、I 函数、路由参数、模型/验证器 | 直接读 `$_GET/$_POST/$_REQUEST`、控制器未走基类/中间件、`request()->param()` 整体写模型 |
| Laravel | Request、FormRequest、route model binding、middleware | `$request->all()` 直接 create/fill/update、raw query、路由缺 auth/can/signed、Blade raw 输出 |
| Spring | `@RequestMapping`、`@RequestParam`、`@PathVariable`、`@RequestBody`、Interceptor/Security | DTO mass assignment、MyBatis `${}`、SpEL/EL、禁用 CSRF、缺对象级授权 |
| Django | request、forms、serializers、ORM、template autoescape、CSRF middleware | `RawSQL/extra/raw`、`mark_safe`、`csrf_exempt`、`DEBUG=True`、手写 SQL、模板字符串 |
| Flask | `request.args/form/json/files`、route decorator、Jinja2 | route 未认证、`render_template_string`、手写 SQL、`send_file` 路径、轻量框架缺默认安全层 |
| Express/Node | route、middleware、body parser、router、template engine | `req.body` 整体更新对象、缺认证中间件、无约束 CORS、`eval/Function`、`child_process` |

### Source 证据模板

```markdown
| Entry ID | Source | 类型 | 进入位置 | 控制主体 | 控制粒度 | 初始变量/字段 | taint 类型 | 证据 |
|---|---|---|---|---|---|---|---|---|
| HTTP:POST:/api/users | body.name | JSON body | `{file:line}` | 低权限用户 | 完整 / 字段 / 条件 | `dto.name` | direct / stored / claim / file / message | 请求 + 代码 |
```

对象标识符类 source 额外记录：

```markdown
| Entry ID | 必需标识符 | 传入位置 | 影响对象选择的位置 | 攻击者获取路径 | 可获得规模 | 是否手工样本 | 账号对象矩阵 | 结论边界 |
|---|---|---|---|---|---|---|---|---|
| HTTP:GET:/files/{id} | file_id | path.id | `{file:line repo.find(id)}` | 列表响应 / 分享页 / 搜索 | 单对象 / 多对象 / 批量 / 不可获得 | 是/否 | A/B/T/cleanup | 只能声明到可获得规模 |
```

## Sink 识别

调用链追踪时只需定位 sink 类型、调用点、危险参数和所属入口，不要把本 Skill 写成漏洞百科。

### 常见 sink

- 查询类：SQL、HQL、JPQL、native query、MyBatis XML、NoSQL filter、LDAP、XPath、search DSL。
- 执行类：系统命令、动态代码、表达式语言、模板编译、反射调用。
- 文件类：读、写、删、复制、重命名、上传保存、下载、对象存储、归档解压。
- 网络类：HTTP client、URL fetch、SSRF、webhook forwarder、proxy、metadata client。
- 输出类：template render、raw HTML、JSONP callback、redirect、response header、cookie、CORS。
- 解析类：XML、YAML、反序列化、office/image/PDF 转换、archive entry。
- 权限类：对象查询、批量 update/delete/export、role change、tenant/owner condition、policy decision。
- 状态类：CSRF state change、cache write、queue publish、workflow dispatch。

### Sink 记录模板

```markdown
| Sink | 调用点 | 危险参数 | 所属 Entry ID | 执行条件 | 当前可达性 | 证据 |
|---|---|---|---|---|---|---|
| SQL | `{file:line mapper.query}` | `${orderBy}` | HTTP:GET:/items | sort 非空 | BRANCH_CONDITIONAL | 代码 |
```

## Transform / 防护检查

每个 transform 都要判断是保持污染、改变形态、缩小控制面，还是完全阻断。

| 类型 | 示例 | 默认判断 |
|---|---|---|
| 纯传播 | assignment、参数传递、return、getter/setter | 保持可控 |
| 格式转换 | trim、lower、decode、parse JSON/XML、base64 decode | 通常仍可控 |
| 拼接组合 | concat、StringBuilder、sprintf、template string、path join | 组合值受污染，需字段级判断 |
| 容器传播 | array/list/map/object/session/cache | taint 进入字段/元素，需要字段级追踪 |
| 序列化映射 | DTO、VO、Entity、Model、ORM hydration、serializer | 追字段映射、默认值、别名、忽略字段 |
| 类型转换 | int、bool、enum、date、UUID | 缩小控制面，不自动安全 |
| 派生 | hash、slug、lookup、normalize、canonicalize | 判断危险语义是否保留 |
| 覆盖 | hardcoded、default、server value、db value | 可能阻断可控性 |
| 防护 | allowlist、parameterization、escape、authorization | 必须判断上下文和分支 |

### 防护有效性门槛

一个防护只有同时满足以下条件，才能降低或阻断可控性：

1. 作用在同一个 source 的后继变量或同一个字段上。
2. 发生在 sink 前。
3. 覆盖当前执行分支、异常分支、批量元素和异步消费端。
4. 与 sink 上下文匹配。
5. 失败时 return、throw、deny、abort，而不是 fallback 到原始值或危险默认值。
6. sink 实际使用防护后的值，而不是仍使用原始值。
7. 有代码、配置或运行态证据，不靠方法名和框架默认假设。

### 常见防护判断

- 参数化：只保护值位置；动态表名、列名、排序、operator、limit、JSON path、模板名、文件路径、URL host 仍需白名单。
- 白名单：必须是服务端允许列表；前端下拉、Swagger enum、注释、TypeScript 类型不算服务端白名单。
- 类型转换：int、UUID、enum 可阻断结构注入，但不能自动阻断 IDOR、越权、批量滥用或对象选择。
- canonicalize：必须早于路径/URL/IP/权限判断，并覆盖编码、双重编码、Unicode、大小写、符号链接、重定向、DNS rebinding。
- escape：必须匹配上下文；HTML escape 不能保护 SQL、shell、path、header，SQL escape 不能保护 HTML、JS。
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

入口到 sink 的追踪必须先证明入口可达，再证明每一跳传播。

### 入口枚举

- HTTP route：路由文件、注解、attribute、decorator、controller method、REST resource。
- 框架边界：Servlet、Filter、Listener、Middleware、Interceptor、Guard、Policy、AOP。
- API 入口：GraphQL resolver、RPC service、WebSocket handler、message listener。
- 非 HTTP：CLI command、scheduled job、queue consumer、webhook、file import、CMS hook。
- 动态路由、正则路由、通配符、group prefix、反向代理 prefix、route cache 必须有解析证据。

### handler 到 sink

逐层追踪：

```text
handler/controller/action
  -> service、use case、manager
  -> repository、DAO、mapper、model、helper、client
  -> sink
```

复杂边界要特别处理：

- 依赖注入：构造函数、注解、容器绑定、provider、service registration。
- 接口、抽象类、父类、trait、mixin、decorator、AOP：解析真实实现；未解析写缺口。
- ORM、Mapper、XML、query macro、repository 基类：追到最终查询或操作。
- 事件、队列：同时追 producer 和 consumer；只追一端不能 technical_confirmed。
- 动态函数、反射、魔术方法、自动路由：必须给出解析规则或运行态补证。

每一跳记录格式：

```markdown
### Level N: `{classOrFile}.{method}`
- 位置：`{file:line}`
- 输入：`{var}` 来自 `{previous}`
- 关键动作：`parse/validate/auth/assign/call/query/fetch/render/execute`
- 分支：`{condition}`，攻击者是否能满足
- 防护：`{guard/sanitizer/parameterization/canonicalize}`
- 输出：`{nextVar}` → `{nextMethod}`
- 状态：COMPLETE / PARTIAL / UNRESOLVED
```

## 数据流追踪步骤

本 Skill 的数据流追踪只覆盖“入口到调用链”范围；深层 taint 传播应转到 Source→Sink 专项。

1. 写出最小入口样例：HTTP 请求、GraphQL operation、WS event、queue message、CLI argv、cron input、file import 样例。
2. 定位 source 字段进入点：`file:line`、handler 参数、request object、DTO、model、message object。
3. 记录绑定与重命名：`source.field -> handlerVar -> dto.field -> serviceArg -> repoArg -> sinkArg`。
4. 记录中间件处理：auth、tenant、CSRF、schema、parser、signature、rate limit 是否改写或阻断。
5. 记录分支：if/switch/early return/exception/profile/feature flag/role/object state。
6. 逐跳追业务层：handler、service、manager、repository、mapper、model、helper、client。
7. 标出 sink：API、危险参数位置、执行条件和所属 Entry ID。
8. 若入口依赖对象 ID、租户 ID、文件 ID、分享 token、lookup handle 或 URI，先写标识符获取链：攻击者从哪个入口拿到、响应字段是什么、能拿多少、是否可持续、是否只是手工样本。
9. 若入口依赖 A/B 主体、owner/victim、跨租户或清理动作，先写账号对象矩阵：账号、账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 引用、适用步骤和清理责任。
10. 若入口链路要进报告，写官方门禁状态：`security_model_status`、`target_scope_status`、`official_known_status`、`version_identity_status`、`预期行为 / accepted risk 说明`、`范围外裁决`、外部门禁引用。
11. 设计正控和负控：证明目标 route、handler、auth 决策、ID 获取链、官方边界、sink 执行和副作用。
12. 输出状态和缺口：未解析实现、缺运行态、缺对象、缺 ID 获取链、缺账号矩阵、缺官方安全模型、缺日志、缺负控时不得 technical_confirmed/对外提交。

## 必检证据点

### 入口证据

- route 定义：`file:line`、注解、attribute、decorator、route file、compiled route、route cache。
- 注册证据：module、provider、plugin、router、blueprint、engine、autoload、container 是否加载。
- 匹配证据：method、path、host、header、content-type、params、accept、prefix、priority、fallback。
- 非 HTTP 证据：topic、consumer、command、schedule、event listener、file watcher、hook callback。

### handler 与中间链证据

- handler 解析：真实 class、function、method、closure、resolver、consumer、job。
- middleware、filter、interceptor、guard、policy、dependency 顺序。
- 鉴权与授权：登录态、角色、对象级权限、tenant、owner、public、anonymous、skip。
- 参数绑定：path、query、body、header、cookie、session、claim、message、file 到本地变量。
- 分支执行：feature flag、profile、对象状态、early return、异常处理。

### 调用链证据

- 每一跳 `file:line`、函数签名、输入变量、输出变量、调用语句。
- 接口实现、依赖注入、AOP、decorator、trait、mixin、magic method 解析依据。
- 异步 producer、transport、consumer、message schema、消费日志。
- sink 调用点、危险参数位置、执行条件。

### 运行态证据

- baseline 请求或任务：证明正常业务路径。
- 强正控：证明目标分支、sink 执行、可观察影响。
- 负控：错误 method、path、content-type、token、对象、租户、移除字段、安全值、修复后配置。
- 日志：route match、handler hit、auth decision、branch execution、sink execution。
- 副作用：数据库、文件、对象存储、缓存、队列、HTTP/DNS 回连、业务状态。
- 清理：测试对象、测试文件、测试记录、缓存、队列、配置恢复。

### 证据点 ID 建议

```markdown
| 证据点 | 含义 |
|---|---|
| EVID_ENTRY_REGISTERED | 入口被注册 |
| EVID_ROUTE_MATCH_RULE | 路由匹配规则 |
| EVID_ROUTE_PRIORITY | 优先级、fallback、shadowing |
| EVID_HANDLER_RESOLUTION | handler 解析 |
| EVID_MIDDLEWARE_CHAIN | 中间件/过滤器链 |
| EVID_AUTH_BOUNDARY | 鉴权/授权边界 |
| EVID_PARAM_BINDING | 参数绑定 |
| EVID_BRANCH_EXECUTION | 分支执行 |
| EVID_IDENTIFIER_ACQUISITION | 对象标识符获取路径、获取主体、获取规模、单对象/批量边界 |
| EVID_ACCOUNT_OBJECT_MATRIX | 多主体、多对象、跨租户验证中的账号、账号对象矩阵必要事实、角色、对象归属和清理责任 |
| EVID_OFFICIAL_SECURITY_MODEL | 官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 与对外提交裁决 |
| EVID_CALL_CHAIN_HOP_N | 第 N 跳调用链 |
| EVID_DYNAMIC_DISPATCH | 动态分发解析 |
| EVID_ASYNC_PRODUCER | 异步生产端 |
| EVID_ASYNC_CONSUMER | 异步消费端 |
| EVID_SINK_REACHABILITY | sink 可达 |
| EVID_STRONG_POSITIVE | 强正控 |
| EVID_NEGATIVE_CONTROL | 负控 |
| EVID_IMPACT_PROOF | 影响证明 |
| EVID_CLEANUP | 清理/恢复 |
```

## 动态验证触发条件

必须动态验证的场景：

- route cache、compiled route、反向代理、gateway prefix、runtime profile 或 feature flag 可能改变入口。
- middleware、filter、interceptor、guard、policy 执行顺序需要日志确认。
- 自动路由、fallback、wildcard、dynamic dispatch、reflection、magic method、DI 多实现无法静态确认。
- 队列、事件、cron、webhook、file import 需要 producer、consumer 同环境证据。
- 鉴权、越权、IDOR、CSRF、SSRF、文件访问、上传、命令执行、组件可达性依赖运行态。
- 对象级授权、IDOR、跨租户、批量导出、文件访问、分享访问依赖对象标识符时，必须运行态确认标识符能否由攻击者列表、详情、搜索、导出、日志、关系链、分享页、客户端状态、可预测序列或批量接口获得。
- 多主体、多对象或跨租户链路必须运行态确认账号对象矩阵、对象归属、token/cookie 隔离和清理动作。
- 路由链路准备写成对外对外可提交、高危、严重、未认证、默认配置受影响、跨租户、沙箱逃逸、RCE、SSRF 内网访问或有效凭据泄露时，必须裁决官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 和 范围或官方已知拒绝（外部裁决）。
- 扫描器、报告或 外部模型/工具输出要升级 technical_confirmed。
- 弱 payload 失败但代码仍显示路径可疑，需要排查是否命中错误 route、错误分支或错误观察点。

可以保持 candidate 的场景：

- route、handler、source、sink 静态证据较完整，但缺运行环境、账号、对象、日志、强正控或负控。
- 非 HTTP 入口静态可见，但缺 producer、consumer 连接证据。
- 组件版本和调用点可达，但缺实际触发输入。
- 动态分发可疑但无法解析全部分支。
- 入口能替换对象 ID，但只有手工样本、管理员视角 ID、历史报告 ID 或单个不可泛化 ID，尚未证明攻击者可获得路径。
- 入口链路可达且强正控成立，但官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 尚未裁决。

必须停止当前目标动态验证的场景：

- 会越出授权范围。
- 会访问第三方真实系统或真实内网资产。
- 会读取、输出、复用真实用户数据或真实生产凭据。
- 会造成不可清理副作用、不可逆修改、拒绝服务或持久化后门。
- 缺测试账号、测试对象、日志观察、快照、重置或清理能力。
- 缺官方资料、范围说明、默认配置、known issue 去重、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 裁决，且当前结论要写成对外可提交。

## 授权实验模式下的强验证方法

强验证目标不是“打得更响”，而是证明 route、handler、middleware、branch 和 sink 的真实可达性。

### HTTP / API 验证框架

```text
baseline:
  使用正常 method/path/header/content-type/body/token/object，确认业务路径、handler 命中、正常响应。

positive:
  仅修改目标 source 字段为与 sink 匹配的强正控输入，记录 handler、auth、branch、sink、影响。

route-negative:
  改 method/path/content-type/host/header/params，证明不是相邻 route、fallback 或统一错误页。

auth-negative:
  改为未登录、低权限、其他角色、其他租户、其他对象，证明权限边界；IDOR/越权必须用攻击者可获得的对象 ID，而不是手工样本。

field-negative:
  移除关键字段、使用安全值、使用不满足分支条件的值，证明差异由目标 source 触发。

identifier-negative:
  使用不可获得 ID、无效 ID、自己对象 ID、他人测试对象 ID、跨租户测试对象 ID、批量 mixed IDs，对比是否逐项授权；如果攻击者无法从自身入口拿到目标 ID，只能写窄化或降级结论。

cleanup:
  清理测试记录、测试文件、缓存、队列、对象存储、业务状态。
```

### 非 HTTP 验证框架

```markdown
GraphQL:
- operation / variables / context / resolver 日志 / auth decision / sink 日志 / 负控 operation。

WebSocket:
- connect auth / channel / event / payload / handler 日志 / 广播范围 / 无权限对照。

Queue/Event:
- producer / topic / message schema / message id / consumer 日志 / sink 日志 / dead-letter / 清理。

CLI/Cron:
- command / argv / stdin / env / working directory / job log / 文件或数据库副作用 / 清理。

File Import:
- 文件格式 / 文件名 / row 字段 / parser 日志 / import job / sink / 清理导入数据。
```

### 浏览器与 Burp 要求

- 先用真实 UI 捕获 baseline，再修改请求。
- 每次只改变一个变量：method、path、content-type、token、对象、tenant、source 字段、分发字段。
- 对 route priority 和 fallback，要构造相邻 route 对照。
- 对鉴权和对象级权限，至少使用两个主体和两个对象。
- 记录 Network、Console、DOM、服务端日志、数据库/文件/队列/缓存变化。
- 弱 payload 失败时先复核 route、handler、sink、观察点，不直接 rejected。

## 最高危害追踪

入口与调用链追踪本身不负责完整漏洞利用，但必须指出当前入口能支撑的最高影响方向：

| 方向 | 需要继续追的证据 |
|---|---|
| 数据读取 | route 命中、对象权限、查询分支、测试数据响应或日志 |
| 数据写入 | 状态改变、数据库、缓存、文件副作用、清理结果 |
| 越权 | A/B 主体、A/B 对象、tenant、owner 对照、最低权限、标识符获取链、账号对象矩阵 |
| 执行 | handler 分支、命令/表达式 sink、输出、文件、OOB、执行身份 |
| SSRF | HTTP client sink、最终 URL、内网 canary、重定向后目标、响应可见性 |
| 文件越界 | 最终路径、realpath、base、读写内容、访问、覆盖、执行边界 |
| 存储传播 | 写入入口、存储位置、读取入口、触发主体、清理 |
| 组件可达 | 版本、打包、启用、入口、输入可控、危险配置 |

停止继续追踪时写清：`out_of_authorized_scope`、`no_test_object`、`no_runtime_observability`、`no_reset_or_cleanup`、`negative_control_blocks`、`requires_real_user_data`、`impact_already_max_for_environment`。

## 负控设计

入口与调用链负控至少覆盖以下类别：

| 负控类别 | 目的 |
|---|---|
| 错误 method | 排除 method 不敏感或统一 handler |
| 错误 path / 相邻 path | 排除 fallback、wildcard、错误 route |
| 错误 host / prefix / locale / version | 排除 gateway 或 route group 误判 |
| 错误 content-type / accept | 排除 parser 或 consumes / produces 条件误判 |
| 移除关键字段 | 证明目标 source 必需 |
| 安全值 | 证明差异不是正常业务响应 |
| 标识符获取对照 | 证明 ID 不是手工样本能力 |
| 无权限主体 | 证明认证边界 |
| 他人对象 / 跨租户对象 | 证明对象级授权边界 |
| 批量 ID 对照 | 证明是否逐项授权和能否批量声明 |
| consumer 未运行 / 错 topic | 排除只追 producer 的异步误报 |
| 修复后或安全配置 | 证明防护有效性 |

负控失败要分析原因：请求构造错、payload 不适配、观察点错、权限不足、目标分支未进入、防护真实有效、环境缺失，或候选应降级。一个弱 payload 失败不得直接 rejected。

## technical_status 方法性判定边界

### technical_confirmed

入口与调用链类结论要写 technical_confirmed，必须同时满足：

- 入口注册证据完整。
- 路由匹配规则清楚，真实请求或任务可命中。
- handler 解析到真实代码。
- source 进入与参数绑定清楚。
- middleware、auth、CSRF、schema 等覆盖或缺失已证明。
- handler 到 sink 的调用链闭合。
- sink 危险参数位置被污染，或安全边界被绕过。
- 若入口链路依赖对象 ID、租户 ID、文件 ID、分享 token、lookup handle、资源 URI 或物理表名，攻击者获得路径已证明，且声明范围不超过可获得规模。
- 若入口链路依赖多主体、多对象、owner/victim、跨租户或清理动作，账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离和清理责任已证明。
- 强正控证明目标分支、sink 执行和安全影响。
- 至少一个负控成立。
- 副作用已清理，或证明无不可清理副作用。
- 若要进入报告或对外提交，`EVID_OFFICIAL_SECURITY_MODEL` 已证明当前入口、主体、对象、配置和影响不属于官方预期功能、accepted risk、范围或官方已知拒绝（外部裁决）、known issue、hardening only 或受信任主体正常能力，且声明不超过官方安全边界。
- `Allowed Claims`、`Forbidden Claims` 与 `Missing Evidence` 清楚，且报告声明不超过入口链路、标识符获取、账号矩阵、强正控和负控能支撑的范围。

### candidate

以下情况只能写 candidate：

- 路由和 handler 静态可见，但缺运行态命中。
- 调用链有若干跳，但接口实现、AOP、动态调用或异步消费端未解析。
- 参数绑定可疑，但 DTO、schema、model binding 未完整确认。
- middleware、auth 覆盖范围未确认。
- sink 存在，但执行分支、可控性、防护或影响缺证据。
- 扫描器 route/call graph 有线索但未人工核对。
- 弱正控失败但尚未证明路径不可达或防护有效。
- 对象 ID 可传入并影响对象选择，但只有手工样本、管理员视角 ID、历史报告 ID 或单个不可泛化 ID，尚未证明攻击者可获得路径。
- 多对象、批量、全量或跨租户声明缺少 ID 获取规模、账号矩阵或对象归属负控。
- 路由、handler、sink 和强正控都成立，但官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 范围或官方已知拒绝（外部裁决） 未裁决，不能写对外可提交。

### blocked

写 blocked 时列具体缺口：

- route cache、compiled route、profile、feature flag、gateway prefix。
- 测试账号、对象、租户、CSRF、session、JWT、OAuth claim。
- 对象标识符能否由攻击者列表、详情、搜索、导出、日志、关系链、分享页、客户端状态、可预测序列或批量接口获得。
- 账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离或清理能力。
- handler 命中日志、auth 决策日志、sink 执行日志。
- queue、cron、event 消费端运行证据。
- 文件、数据库、缓存、对象存储、网络回调副作用。
- 清理、恢复证据。
- 官方资料、scope、默认配置、known issue 去重、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和对外提交限制。

### rejected

只有具备排除证据时才写：

- 入口不可达或未注册。
- source 不可控或只在前端存在。
- source 未绑定到目标变量，或未进入 sink。
- sink 参数不是危险参数，或 sink 使用服务端固定值。
- 参数被无条件覆盖，或白名单、类型、授权防护真实阻断当前风险。
- 依赖对象标识符的结论，经代码、接口和运行态证据证明攻击者无法获得必要 ID，且不存在列表、搜索、导出、日志、关系链、分享页、可预测或可推导路径。
- 官方资料明确该入口、主体或 sink 是 expected behavior、trusted admin normal use、accepted risk、范围或官方已知拒绝（外部裁决）、known limitation、hardening only 或已知重复问题，且当前证据没有证明新主体、新对象、新入口、新默认配置、新影响层级或官方缓解绕过。
- 强正控和负控证明参数变化不影响 sink 或影响不成立。
- 运行态负控证明影响不成立。

### 必须降级的场景

- scanner-only、external-tool-only、sink-only、source-only、route-only、regex-only。
- trace_status 为 PARTIAL / UNRESOLVED。
- controllability_status 为 UNRESOLVED。
- 无负控。
- 只有 200 响应。
- 只有 marker 回显但无 sink 参数证据。
- callback-only SSRF。
- marker-only RCE。
- error-only SQLi。
- reflect-only XSS。
- 拿不到对象归属差异的 IDOR。
- 只有“已知 ID 后可利用”，没有证明攻击者如何获得 ID。
- 只有单个手工样本 ID，却声明批量、全量、全租户、全用户、全工作区或广义影响。
- 多主体结论缺账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离或清理责任。
- 官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior 未裁决、accepted risk 未裁决或 范围或官方已知拒绝（外部裁决） 未裁决，却准备写对外可提交。
- version-only 组件漏洞。
- 只有错误信息或日志片段，无安全影响。
- 弱 payload 失败但未完成路径、sink、观察点、防护语义复核。

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

修复建议必须具体到框架、调用点、配置和测试，不得只写“过滤输入”。

- 注入类：使用参数化绑定；动态表名、列名、排序字段、排序方向使用枚举映射；移除 raw 拼接；增加 DAO、Mapper 单元测试和集成测试。
- NoSQL：固定查询结构；拒绝操作符注入；对 filter、update 对象做 schema validation；不要把用户 JSON 原样传入查询。
- 命令执行：避免 shell；使用参数数组；固定命令名；参数白名单；固定工作目录和环境变量；最小权限运行。
- 模板、XSS：保持自动转义；禁止 raw；模板名和模板路径白名单；富文本使用可信 sanitizer；按 HTML、JS、CSS、URL、attribute 上下文编码。
- 文件路径：先 decode、canonicalize，再 normalize、realpath，再 base 约束；拒绝符号链接逃逸；不要用字符串前缀代替真实路径约束。
- 上传：服务端生成文件名；扩展名、MIME、magic bytes 多重校验；存储到 web 根外；禁执行；下载鉴权；限制大小；二次处理继续校验。
- 归档：逐 entry 归一化；拒绝绝对路径、`..`、链接和特殊文件；限制解压大小和文件数；解压后权限最小化。
- SSRF：scheme allowlist；DNS 解析后拒绝本地、内网、metadata、保留地址；重定向后重校验；限制端口；记录出站审计。
- 鉴权、IDOR：默认拒绝；路由级、方法级、对象级授权同时覆盖；查询条件绑定当前主体和 tenant；批量接口逐项校验。
- 标识符暴露：不要把敏感对象 ID、tenant/workspace/file ID 无约束暴露给无关主体；列表、搜索、导出和分享接口也要绑定对象级权限；使用不可预测 ID 只能降低枚举风险，不能替代授权检查。
- CSRF：状态变更统一 token 校验；token 与 session 绑定；覆盖 JSON、multipart、AJAX、method override；SameSite 只作补充。
- XML、反序列化：禁外部实体、外部 DTD、Schema、XInclude 和网络访问；不要反序列化不可信数据；限制类型；关闭危险多态；签名并绑定上下文。
- Secret、日志：密钥移出仓库；最小权限；轮换泄露凭据；日志脱敏 token、cookie、password、secret、PII；限制日志访问。
- 依赖：升级到安全版本；确认实际打包版本；关闭危险默认配置；为可达调用点增加回归测试。

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
- 禁止把单个手工样本 ID 外推成批量、全量、全租户、全用户、全工作区或广义影响。
- 禁止把管理员手工给出的 ID、聊天上下文里的 ID、历史附件里的 ID、报告作者笔记里的 ID 当作攻击者可获得路径。
- 禁止账号矩阵缺账号对象矩阵必要事实、主体 ID、租户/工作区、对象归属、token/cookie 引用和清理责任时声称多主体 technical_confirmed 可复核。
- 禁止官方安全模型 unknown、scope unknown、默认配置 unknown、known issue 未去重、expected behavior 未裁决、accepted risk 未裁决或 范围或官方已知拒绝（外部裁决） 未裁决时写对外可提交。
- 禁止官方资料已明确为 expected behavior、trusted admin normal use、accepted risk、范围或官方已知拒绝（外部裁决）、known limitation 或 hardening only 时，仍按新漏洞 technical_confirmed/对外提交 提交；除非证明新主体、新入口、新对象、新默认配置、新影响层级或官方缓解绕过。
- 禁止只有路由可达、handler 命中或 sink 可达，而没有官方门禁支撑时，写“官方未公开”“默认配置受影响”“范围内高危”“严重漏洞”“沙箱逃逸”“跨租户突破”等强声明。
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

## 自检清单

输出审计结论或报告前逐项检查；关键项为“否”时不得 technical_confirmed。

### 范围与入口

- [ ] 是否写清授权范围、目标版本、配置、测试账号、测试对象、可重置能力？
- [ ] 多主体、多对象或跨租户入口链路是否有账号矩阵、账号对象矩阵必要事实、主体 ID、对象归属、token/cookie 引用和清理责任？
- [ ] 如果链路要进入报告，是否裁决官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决） 和外部门禁引用？
- [ ] 是否枚举 HTTP、GraphQL、WebSocket、RPC、CLI、webhook、queue、cron、event、file import 入口？
- [ ] 是否记录 route、method、path、handler、middleware、auth、source 参数？
- [ ] 是否处理动态路由、group prefix、自动路由、hook、反射、插件入口？

### Source 与可控性

- [ ] 是否证明 source 可由攻击者、低权限用户、外部服务或可污染存储控制？
- [ ] 是否记录控制主体、控制粒度、绑定变量和进入位置？
- [ ] 是否处理 query、path、body、header、cookie、JSON、XML、multipart、GraphQL、WebSocket、CLI、webhook、queue、file import、session、claim？
- [ ] 是否判断参数是否被硬编码覆盖、默认值替换、白名单映射、类型转换阻断或条件可控？
- [ ] 如果 source 是对象 ID、分享 token、lookup handle、URI 或租户/工作区标识，是否证明攻击者获取路径，而不是只证明可传入？
- [ ] 如果报告写批量、全量、全用户、全租户、全工作区或广义影响，是否证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得？

### Trace 与 Sink

- [ ] 是否逐跳追踪 route -> handler/controller -> service -> repository/mapper/model/helper/client -> sink？
- [ ] 是否记录每一跳的 `file:line`、变量名变化、分支条件、权限检查？
- [ ] 是否定位 sink 的危险参数位置，而不是只列 API 名？
- [ ] 是否证明 source 污染的变量仍进入 sink？
- [ ] 如果调用链是 AUTH/IDOR/对象级授权，是否把 route -> handler -> lookup -> auth decision -> sink 和 ID 获取链同时闭合？

### Transform / 防护

- [ ] 是否确认参数化真实覆盖全部动态片段？
- [ ] 是否确认白名单是允许列表，并在规范化之后执行？
- [ ] 是否确认 escape/encode 匹配当前上下文？
- [ ] 是否确认 canonicalize/realpath/normalize 早于路径判断，并处理符号链接、编码和平台差异？
- [ ] 是否确认防护作用在同一变量、同一分支、同一上下文且早于 sink？

### 动态验证与负控

- [ ] 是否明确自有 Docker、CTF、靶场、可重置实验环境、测试账号、测试对象、快照、回滚、清理能力？
- [ ] 是否写出 baseline、强正控、负控请求？
- [ ] 是否使用足够证明漏洞语义的 payload，而不是只用无意义 marker？
- [ ] 是否记录响应、日志、副作用、清理、回滚？
- [ ] 是否为 technical_confirmed 至少提供一个负控？
- [ ] 如果不能动态验证，是否降级为 candidate 或 blocked 并说明原因？

### 最高影响追踪

- [ ] 是否从低层触发继续追数据读取、写入、越权、执行、内网 canary、浏览器执行或组合链？
- [ ] 是否写明最高已证明影响？
- [ ] 若未继续升级，是否写明停止原因？
- [ ] 是否没有读取真实用户数据、泄露真实凭据或越出授权范围？

### 判定与报告

- [ ] 是否为每项发现标注 technical_confirmed、candidate、blocked、rejected？
- [ ] 是否把 technical_confirmed 与对外提交资格 分层，而不是把 route/handler/sink 可达自动等同于可提交漏洞？
- [ ] 是否避免官方安全模型 unknown 时写对外可提交？
- [ ] 是否说明 candidate 升级还缺什么证据？
- [ ] 是否说明 rejected 的排除证据？
- [ ] 是否没有把扫描器结果、外部模型/工具自述、pending 状态、200 响应当 technical_confirmed？
- [ ] 是否避免“已知 ID 后可利用”直接写高价值 technical_confirmed？
- [ ] 是否避免单对象结果外推成批量、全量或广义影响？
- [ ] 是否已把入口、Source、Sink、Trace、防护、复现、强正控、负控、最高影响、清理、修复建议和声明边界写入对应 EVID，并由报告阶段引用唯一模板渲染？
- [ ] 是否删除项目私有路径、项目名、编号、内部平台术语和运维流程？
