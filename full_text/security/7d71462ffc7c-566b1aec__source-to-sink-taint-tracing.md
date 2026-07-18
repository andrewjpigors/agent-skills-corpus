---
name: source-to-sink-taint-tracing
description: Use when an audit needs to prove whether user-controlled, stored, framework-bound, message-derived, file-derived, header-derived, claim-derived, or configuration-derived data can reach a security-sensitive sink with exploitable control, and when that trace must survive identifier-acquisition, account-matrix, and official-security-model review before it can be reported.
---

# Source到Sink数据流追踪

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 如何使用这个 Skill

使用本 Skill 时，把它当成“漏洞证据链闭合器”，不是危险函数词典。它适合在以下场景启动：

- 已经看到一个可疑 source，想知道它是否真正进入 SQL、命令、文件、模板、SSRF、鉴权等 sink。
- 已经看到一个 sink，想反向追踪参数来源、可控性、防护和触发条件。
- 扫描器、规则、正则、IDE、CodeQL、Semgrep、SAST、DAST 或其他模型/工具 给出告警，需要人工复核。
- 框架项目里出现“非标准写法”：绕过框架输入封装、绕过 ORM、禁用默认中间件、raw 输出、原生查询、整体对象写入、动态表达式。
- 需要把一条发现裁决为 `technical_confirmed`、`candidate`、`blocked` 或 `rejected`。
- 需要写漏洞报告相关 evidence 中的 Source、Sink、Trace、防护缺口、强验证、负控、修复建议和声明边界。

使用前先明确本次 trace 的单一目标：

```text
入口是什么 -> 哪个 source 可控 -> 哪个变量/字段承载 taint -> 经过哪些调用/分支/transform -> 到达哪个 sink 的哪个危险参数 -> 是否有有效防护 -> 如何证明影响与负控
```

如果这条 trace 未来要进入报告，还要同步确认：官方安全模型是否支持该声明、对象/租户边界是否被突破、以及攻击者是否真的能拿到所需标识符。

### 每次判断的最小交付

每次写结论前，至少把下面几件事交代清楚，缺一项就先降级，不要抢着下 `technical_confirmed`：

- source 的控制主体、控制粒度、可信边界。
- source 到绑定变量、字段、对象、claim、文件或消息的映射。
- sink 的危险参数位置，以及参数是否被实际使用。
- transform、覆盖、分支、异常、权限和默认值如何影响 taint。
- 官方安全模型、范围、默认配置和 known risk 是否支持该 trace 的漏洞解释。
- 强正控、负控、清理/恢复。
- 当前可写的 `allowed claims` 与必须禁止的 `forbidden claims`。

如果入口、路由、handler 都没定位清楚，先做入口与调用链追踪；如果只有扫描器命中或正则命中，不得直接进入漏洞结论。

## 核心原则

### 1. 正则和扫描只负责发现候选，不负责下结论

正则匹配、grep、ripgrep、IDE 搜索、Semgrep/CodeQL 命中，都是“探照灯”，不是裁判。它们能快速定位危险函数、用户输入、raw SQL、文件操作、模板输出、危险配置，但不能证明跨行变量追踪、过滤语义、分支可达、框架绑定和运行态影响。

常见候选搜索可以这样启动，但命中后必须进入人工 trace：

```bash
# PHP 命令执行候选
rg -n "\b(system|exec|shell_exec|popen|proc_open|passthru)\s*\(" --glob '*.php' .

# PHP 用户输入候选
rg -n "\$_(GET|POST|REQUEST|COOKIE|FILES)\b" --glob '*.php' .

# SQL 拼接 / raw 查询候选
rg -n "(query\s*\(|execute\s*\(|whereRaw|orderByRaw|selectRaw|DB::raw|\$\{|\+\s*\w+\s*\+)" .

# 文件 / 包含 / 解压候选
rg -n "\b(include|require|file_get_contents|file_put_contents|fopen|fwrite|readfile|extractTo|ZipArchive|TarArchive)\b" .
```

检验：这条命中是否已经证明了 source、binding、trace、sink 参数、防护缺口、影响和负控？如果没有，只能标为 candidate 线索。

### 1.1 工具给出的 taint trace 必须人工复核

CodeQL、Semgrep、商业 SAST 或 IDE 的 data-flow/path trace 可以节省定位时间，但它们的模型和真实运行语义不等价。复核时至少检查：

- **source 是否精确**：source pattern 是否把整个表达式、子表达式、包装函数、默认值或 helper 都标成污染；source 是否真由攻击者控制。
- **propagator 是否符合项目语义**：赋值、函数调用、字段写入、集合传播、builder、serializer、ORM hydration、消息发送是否真的把同一个字段传下去。
- **sanitizer 是否过宽**：工具认为 `sanitize(x)` 安全，不等于 sink 使用了 `sanitize(x)` 的返回值；也不等于 sanitizer 覆盖当前上下文。
- **sink 是否精确**：命中函数不等于命中危险参数；必须看第几个参数、哪个字段、哪个结构片段、哪个执行分支。
- **trace 是否唯一或完整**：工具通常只展示一条代表性路径，不能证明其他路径不存在；也不能证明展示路径在当前 profile、DI 实现、feature flag、路由缓存下可达。
- **local flow 与 global flow 要区分**：函数内传播和跨函数、跨对象属性、跨异步消息、跨存储读取不是同一难度。局部 trace 完整不代表全局 trace 闭合。
- **taint 与 value flow 要区分**：`y = x + suffix` 可能不是同一个值，但仍受 x 影响；这适合 taint 传播，不代表能控制完整 sink 参数。

工具 trace 的正确用法是：把它拆成 `source candidate -> propagation candidate -> sanitizer candidate -> sink candidate` 四类线索，然后逐项用代码语义和运行态证据复核。禁止把 SARIF、dataflow 截图、规则命中或 agent 总结直接复制成报告结论。

### 2. 变量追踪看生命周期：定义、传递、使用

每个污染变量至少要回答三件事：

| 阶段 | 要看什么 | 常见误判 |
|---|---|---|
| 定义 | 变量是否来自请求、header、cookie、文件、消息、claim、数据库、缓存、客户端代码、低权限写入 | 只看到变量名像 `id`、`url` 就假设可控 |
| 传递 | 赋值、参数、返回值、对象字段、数组元素、集合、序列化、队列、缓存、ORM hydration | 参数传到函数但函数未使用；对象传入但 sink 用另一个字段 |
| 使用 | sink 的危险参数位置、执行分支、最终字符串/对象/URL/path/header/query | 只看到函数名，未确认污染值进入危险参数 |

基本追踪方向有两种：

- 从 sink 反向：看到 `system(cmd)`、`query(sql)`、`render_template_string(tpl)` 后，向上找 `cmd/sql/tpl` 的来源。
- 从 source 正向：看到 `req.body.url`、`$_GET['id']`、`@RequestBody dto`、`request.args.get()` 后，向下追它是否进入 sink。

检验：能否写出 `source -> 初始变量 -> 每一跳 -> transform/branch -> sink危险参数` 的连续链路？中间缺一跳就不能 technical_confirmed。

### 2.1 追踪时优先证明“同一后继值”

Source→Sink 的关键不是“名字相似”，而是证明 sink 使用的是 source 的同一后继值。以下都要拆开：

- `raw`、`safe`、`normalized`、`escaped` 同时存在时，sink 到底用了哪个。
- `dto`、`entity`、`model` 同时存在时，sink 用的是请求字段、数据库字段、默认字段还是服务端覆盖字段。
- `id` 进入查询后换成 `record.owner_id` 时，`id` 控制的是对象选择，不等于控制 `owner_id`。
- `url` 经过 redirect、DNS、HTTP client wrapper 后，sink 使用的是初始 URL、规范化 URL、最终 URL、解析后 IP，还是服务端配置 host。
- `filename` 经过随机文件名、扩展名替换、对象存储 key 映射后，sink 使用的是原始文件名还是服务端生成名。
- `role`、`tenant`、`userId` 同时在 request、session、JWT、数据库中出现时，必须证明信任来源是哪一个。

检验句：**如果我把 source 改成 A/B 两个不同测试值，sink 危险参数会不会同步变成 A/B？如果不会，变化发生在哪一跳？**

### 3. 框架审计要找“标准写法之外的差异”

框架不是漏洞本身。主流框架通常提供路由、中间件、ORM、模板转义、CSRF、认证授权等安全机制；漏洞常出在开发者绕过这些机制的位置。

框架项目先做三步：

1. **认框架**：依赖清单、目录结构、入口文件、路由配置、配置文件、响应头、启动代码。
2. **知机制**：请求如何绑定到 handler，参数如何进入 DTO/Model，ORM/模板/鉴权/CSRF 默认如何工作，哪些配置会改变默认行为。
3. **找差异**：原生输入、raw SQL、raw 输出、整体对象写入、禁用中间件、跳过 CSRF、绕过 Policy/Gate/Interceptor、动态表达式、危险组件可达。

检验：如果一个发现只说“Laravel/ThinkPHP/Spring/Django 默认安全/默认不安全”，没有读项目实际配置和调用方式，结论无效。

### 4. Transform 不等于 Sanitizer

`trim`、`lower`、`decode`、`json_decode`、`base64_decode`、对象映射、格式化、拼接、序列化、ORM hydration 都是 transform，默认仍保持 taint。只有在同变量、同分支、同上下文、sink 前执行，并且失败时阻断的处理，才可能是 sanitizer。

输入验证也一样：**服务器端 allowlist + 规范化/归一化 + 失败即阻断** 才能作为安全证据；客户端校验只算 UX，不算安全。安全 API 永远优先于转义；如果必须转义，也必须按 sink 上下文选择正确编码方式。

例子：

- `trim(userInput)` 对命令注入、SQL 结构注入通常不构成防护。
- `htmlspecialchars` 对 HTML body 可能有效，但对 SQL、shell、path、header、URL 不构成防护。
- `addslashes` 不能当作通用 SQL 或命令防护；要看数据库驱动、字符集、参数化情况和上下文。
- MyBatis `#{}` 通常按值绑定；`${}` 是字符串替换，动态表名/列名/排序必须额外白名单。
- Laravel / Django / ORM 的参数化只保护值位置，不自动保护 raw 片段、列名、表名、排序、表达式和拼接。
- 模板默认转义只保护默认输出语法；raw 输出、safe 标记、关闭 autoescape、服务端模板字符串仍要追踪。

### 5. 强验证默认用于授权可重置环境，结论必须有边界

在自有 Docker、CTF、靶场、本地可重置环境、隔离预发或明确授权的测试环境中，不应满足于弱 marker。trace 闭合后要尽量追到当前范围内最高可证明影响：查询语义、受控读写、对象越权、服务端请求、文件边界、命令输出、浏览器执行、组件链触发。

边界同时必须清楚：不越出授权范围，不测试第三方真实系统，不读取真实生产用户数据，不输出真实凭据，不制造不可清理副作用。没有环境、账号、对象、日志、快照、重置或清理能力时，不强行写 technical_confirmed。

### 6. 依赖对象标识符的 trace 必须补齐“标识符获取链”

Source→Sink 不是只追“字段能不能到 sink”。如果漏洞影响依赖 `user_id`、`object_id`、`tenant_id`、`workspace_id`、`project_id`、`file_id`、`document_id`、`workflow_id`、`plugin_id`、分享 token、lookup handle、物理表名、资源 URI 或其他对象标识符，trace 必须额外证明攻击者如何获得这些标识符。

- 单对象 trace：必须证明该 ID 来自攻击者自身可达路径，例如列表、详情响应、搜索、导出、日志、关系链、分享页、可预测序列或可推导路径；结论只能写到这个对象或同类可获得对象。
- 多对象 / 批量 / 广义 trace：必须证明 ID 能批量、持续、枚举、列表式、搜索式、导出式、日志泄露式、关系链式、分享页式或可推导式获得。
- 拿不到 ID：不能把“已知 ID 后可利用”写成高价值 `technical_confirmed`；通常只能写 `candidate`、`blocked` 或在排除证据充分时写 `rejected`。
- 管理员手工提供的 ID、报告作者笔记里的 ID、聊天上下文出现的 ID、历史附件里的 ID，只能作为定位样本，不能算攻击者可获得路径。

凡是 trace 依赖多账号、多对象、owner/victim、跨租户、低权限/高权限对照或清理动作，多主体或对象边界 claim 必须引用账号对象矩阵，记录主体、角色、对象归属、租户/workspace、token/cookie 隔离和清理责任；账号对象矩阵字段以 `templates/账号对象矩阵模板.md` 与对应 schema/template 为准，本 Skill 不重新定义。

检验句：**如果我不给这个 ID，攻击者能不能从自己的入口稳定拿到它？如果报告写批量或广义影响，攻击者能不能批量或持续拿到足够多 ID？**

### 7. 官方安全模型决定 trace 能否写成漏洞

source→sink 只证明“数据流到了哪里”，不自动证明“这条流就是新漏洞”。如果这条 trace 要进入报告，还必须补上官方安全模型的裁决：

- 官方是否把当前主体、对象、租户、插件、脚本、沙箱、导入、webhook、预览、URL fetch 或管理功能定义为受信任边界。
- 官方是否把当前行为定义为预期功能、已知风险、accepted risk、范围外或 hardening only。
- 官方是否明确默认配置、默认角色或默认部署不会受影响。
- 官方是否把这条路径的边界解释为对象级授权、功能级授权、租户级隔离、沙箱隔离或管理员正常能力。

如果官方安全模型 unknown、scope unknown、默认配置 unknown 或 known risk 未去重，这条 trace 只能给出技术候选，不能直接写 technical_confirmed 或对外提交。

## 审计目标

本 Skill 要证明或排除的是：污染数据是否以可利用方式进入安全敏感语义。

需要证明：

- 入口真实可达，路由/消息/任务/文件导入/CLI 已注册并启用。
- source 真实可控，控制主体、权限、租户、对象和字段粒度明确。
- 参数绑定清楚：从请求、消息、文件、claim、session、数据库或缓存进入哪个变量/字段。
- trace 连续：赋值、函数参数、返回值、对象属性、数组元素、集合、序列化、异步消息、ORM/Mapper、接口实现、父类/trait/AOP 都有证据。
- transform、防护、覆盖、分支、异常和权限判断被逐项裁决。
- sink 的危险参数位置被污染，且当前分支会执行。
- 若影响依赖对象标识符，攻击者获得 ID / handle / token / URI 的链路、规模和边界被证明。
- 若影响依赖多主体、多对象或跨租户，账号矩阵、对象归属、账号对象矩阵必要事实和清理责任可复核。
- 若这条 trace 需要写成漏洞报告，官方安全模型、范围、默认配置和 known risk 也要能支持当前声明。
- 强正控、影响证明、负控、清理/恢复和声明边界齐全。

需要排除：

- source 只在前端存在，后端不接收。
- source 来自可信服务端状态、固定配置、不可伪造 claim、不可写数据库字段，攻击者不能影响。
- 参数被无条件覆盖、白名单限定到安全值、类型转换阻断当前漏洞语义。
- 参数传递过但未实际使用，或进入非危险参数。
- sink 只在测试代码、示例、未注册 profile、不可达路由、未消费队列中存在。
- 同变量、同分支、同上下文的防护真实阻断。
- 官方安全模型明确该行为是预期功能、范围外、accepted risk 或 hardening only。
- 弱 payload 失败但尚未证明路径不可达或防护有效；这种情况不得直接 rejected。

## 输入材料

优先读取这些材料，不要只看目录或搜索结果：

- 入口材料：路由文件、注解/attribute/decorator、controller/action/handler/resolver、RPC、GraphQL、WebSocket、webhook、queue consumer、event listener、cron、CLI、file import。
- 绑定材料：request object、body parser、serializer、DTO/VO/FormRequest/ModelBinder、path/query/body/header/cookie/file、session/JWT/OAuth/OIDC/SAML claim。
- 传播材料：service、manager、usecase、repository、DAO、mapper、model、helper、trait、mixin、decorator、AOP、接口、抽象类、父类、magic method、ORM scope、query macro。
- 防护材料：middleware、filter、interceptor、guard、policy、gate、validator、schema、escape、sanitize、canonicalize、auth decision、CSRF/CORS/security header 配置。
- sink 材料：SQL/ORM/Mapper XML、NoSQL/DSL、command/code/template/expression、file/upload/archive/XML/deserialization/HTTP client/redirect/header/auth/cache/queue/log/crypto/config。
- 运行材料：baseline 请求、强正控请求、负控请求、测试账号/对象、日志、数据库/缓存/文件/队列/对象存储副作用、DNS/HTTP 回调、浏览器 DevTools、清理记录。
- 复核材料：扫描器 trace、报告、误报说明、历史修复、官方安全文档、框架版本和运行配置。
- 标识符材料：列表、详情、搜索、导出、日志、关系链、分享页、可预测序列、可推导规则、批量接口、分页接口、对象 URI、分享 token、lookup handle；必须区分单对象可得、多对象可得、批量可得和不可得。
- 多主体或对象边界 claim 必须引用账号对象矩阵，记录主体、角色、对象归属、租户/workspace、token/cookie 隔离和清理责任；账号对象矩阵字段以 `templates/账号对象矩阵模板.md` 与对应 schema/template 为准，本 Skill 不重新定义。
- 官方安全模型材料：SECURITY、安全策略、scope、默认配置、release notes、known issues、accepted risk、范围或官方已知拒绝（外部裁决）、预期行为、对象/租户/插件/沙箱边界与 report quality 规则。

## Source 识别

Source 必须记录来源、进入点、控制主体、控制粒度和污染类型。

### Source 裁决顺序

不要先问“这个字段危险吗”，先按顺序问：

1. 这个值是否进入后端或任务系统，而不是只停留在前端、文档、Swagger、Mock、测试数据。
2. 谁能控制它：匿名、普通用户、管理员、内部服务、第三方 webhook、任务系统、攻击者可污染存储。
3. 控制粒度是什么：完整值、字段、数组元素、对象 ID、枚举选择、格式受限、条件受限、存储型、不可控。
4. 它是否跨过可信边界：签名、session、JWT、OAuth/OIDC/SAML、反向代理 header、HMAC、CSRF、租户。
5. 它是否被服务端覆盖：当前主体、tenant、owner、固定 host、随机文件名、默认配置、数据库记录。
6. 它是否能到达目标 sink 所需的同一分支和同一字段。

只有 1-6 都有答案，才开始谈漏洞类型和强验证。

### HTTP / API Source

- query：`id`、`url`、`path`、`file`、`sort`、`order`、`filter`、`callback`、`returnTo`、`redirect`、`template`。
- path：`/{id}`、slug、tenant、filename、wildcard、正则 capture、后缀。
- body：form、JSON、XML、GraphQL variables、protobuf、nested object、array、bulk list。
- header：Authorization、Host、Origin、Referer、X-Forwarded-*、Content-Type、自定义签名头。
- cookie：session、remember-me、JWT cookie、tenant、locale、业务偏好。
- multipart：文件名、Content-Type、文件内容、普通字段、压缩包 entry name。

### 非 HTTP / 二次污染 Source

- CLI argv/stdin、环境变量、导入文件、CSV/Excel/XML/JSON/YAML/ZIP/TAR/office 文档。
- webhook payload、OAuth/OIDC/SAML claim、支付/消息/代码仓库回调。
- queue message、event bus payload、workflow form、cron 读取记录。
- 数据库、缓存、文件和对象存储中的存储型污染：必须证明攻击者能先写入，再由后续入口读取。
- 前端/客户端代码中的隐藏参数、签名参数、硬编码 key、Authorization 生成逻辑：只有后端接受并信任时才成为后端 source。

### 存储型 Source 必须闭合写入端与读取端

存储型污染是最容易被误判的路径。要同时证明：

```text
攻击者可写入口 -> 存储位置/字段/key/对象 -> 读取入口/任务/consumer -> 读取后变量 -> transform/防护 -> sink危险参数
```

常见错误：

- 只看到数据库字段包含危险字符串，但没证明攻击者能写。
- 只证明攻击者能写 profile/template/rule/callback，但没证明后续任务读取并进入 sink。
- 只证明后台管理员可写，却把结论写成低权限可利用。
- 只证明读取端会渲染/执行，但写入端字段被白名单、富文本 sanitizer、模板沙箱或审核流程限制。
- 存储型 XSS 只在攻击者自己页面触发，却写成可攻击其他用户。
- 存储型 SSRF/RCE 只保存配置，没证明 job、webhook、worker 或 scheduler 会消费。

存储型链路缺写入端或读取端时，只能写 `candidate` 或 `blocked`。

### 框架 Source 差异点

| 生态 | 标准机制 | 需要警惕的 source 差异 |
|---|---|---|
| ThinkPHP | Request/I 函数、路由参数、模型/验证器 | 直接读 `$_GET/$_POST/$_REQUEST`、控制器未走基类/中间件、`request()->param()` 整体写模型 |
| Laravel | `Request`、FormRequest、route model binding、middleware | `$request->all()` 直接 `create/fill/update`、raw query、路由缺 auth/can/signed、Blade raw 输出 |
| Spring | `@RequestMapping`、`@RequestParam`、`@PathVariable`、`@RequestBody`、Interceptor/Security | DTO mass assignment、MyBatis `${}`、SpEL/EL、禁用 CSRF、缺对象级授权 |
| Django | request、forms/serializers、ORM、template autoescape、CSRF middleware | `RawSQL/extra/raw`、`mark_safe`、`csrf_exempt`、`DEBUG=True`、手写 SQL/模板字符串 |
| Flask | `request.args/form/json/files`、route decorator、Jinja2 | route 未认证、`render_template_string`、手写 SQL、`send_file` 路径、轻量框架缺默认安全层 |
| Express/Node | route/middleware、body parser、router、template engine | `req.body` 整体更新对象、缺认证中间件、无约束 CORS、`eval/Function`、`child_process` 拼接 |

### Source 证据模板

```markdown
| Source | 类型 | 进入位置 | 控制主体 | 控制粒度 | 初始变量/字段 | taint 类型 | 证据 |
|---|---|---|---|---|---|---|---|
| `{field}` | query/body/header/... | `{file:line}` | 未登录/普通用户/管理员/系统 | FULL/FIELD/CONDITIONAL/... | `{var.path}` | direct/stored/claim/file/message | `{代码/请求}` |
```

## Sink 识别

Sink 必须记录危险语义、危险参数位置、执行条件和影响，不得只写函数名。

### Sink 裁决顺序

先定位 sink 的危险语义，再定位 API 名：

1. sink 属于哪类危险语义：查询、执行、文件、网络、输出、解析、权限、状态、缓存、队列、日志、配置。
2. 危险参数在哪里：参数序号、对象字段、SQL 片段、URL 部件、path segment、header name/value、模板表达式、operator、ACL 条件。
3. source 后继值是否进入该危险位置，而不是进入日志、label、非危险配置、错误消息或普通显示字段。
4. sink 是否在当前入口分支执行：profile、feature flag、role、object state、异常路径、early return、队列消费状态。
5. 防护是否在 sink 前覆盖同一字段：参数化、白名单、编码、canonicalize、鉴权、类型限制。
6. sink 影响是否可观察：响应、日志、状态、副作用、回连、浏览器执行、命令输出、对象权限差异。

如果只完成 1-2，最多是 sink candidate；完成到 3-5 才能进入强验证；完成 6 加负控后才考虑 technical_confirmed。

### 查询与注入 Sink

- SQL：JDBC Statement、PreparedStatement 拼接前 SQL、MyBatis `${}`、Mapper XML、SQL Provider、JPA nativeQuery、Hibernate HQL/JPQL 拼接、PDO/mysqli query、Laravel raw/whereRaw/orderByRaw/selectRaw、Django RawSQL/extra/raw、动态表名/列名/排序/limit。
- NoSQL/DSL：Mongo filter/update/operator/aggregation、Elasticsearch DSL、Redis key pattern、GraphQL filter、用户对象直接构造查询。
- LDAP/XPath：filter/DN 拼接、XPath expression、XML query raw expression。

### 执行、表达式与模板 Sink

- command：PHP `system/exec/shell_exec/proc_open`，Java `Runtime.exec/ProcessBuilder`，Node `child_process`，Python `subprocess/os.system`，Go `os/exec`，.NET `ProcessStartInfo`。
- dynamic code：`eval/assert`、script engine、reflection invoke、dynamic import、SpEL/OGNL/MVEL/Groovy、EL、模板 compile/evaluate。
- template：模板名、模板内容、表达式字符串、`render_template_string`、Blade `{!! !!}`、raw/safe 标记、关闭 autoescape。

### 文件、解析与网络 Sink

- file read/write：`readfile/fopen/file_get_contents/include/require`、`Files.read/write`、`fs.readFile/writeFile`、`open/read/write`、object storage get/put。
- upload/archive：`move_uploaded_file`、`MultipartFile.transferTo`、object storage upload、preview conversion、Zip/Tar extract、自定义 entry path join。
- XML/deserialize：DOM/SAX/StAX、DocumentBuilderFactory、XMLInputFactory、SimpleXML、ObjectInputStream、Jackson default typing、Fastjson、XStream、Hessian、PHP unserialize/Phar、pickle/yaml unsafe load。
- SSRF：RestTemplate/WebClient/OkHttp/curl/requests/http.Client/fetch/URL.openConnection、`file_get_contents($url)`。

### 输出、权限与状态 Sink

- XSS：HTML body、attribute、JS、CSS、URL、JSON-in-HTML、Markdown/rich text、DOM sink、SSR hydration。
- redirect/header：Location、returnUrl、callbackUrl、Set-Cookie、CORS header、Content-Disposition filename、CRLF 控制字符。
- auth decision：hasRole、authorize、policy/gate、owner/tenant 条件、ACL query、object lookup before permission check。
- CSRF/state change：POST/PUT/PATCH/DELETE、GET state change、method override、JSON/multipart/AJAX 分支。
- cache/queue/log/crypto/config：cache key、message dispatch、日志输出、secret read/write、sign/verify、debug/error config。

### Sink 证据模板

```markdown
| Sink | 调用点 | 危险参数位置 | 输入变量 | 执行条件 | 影响语义 | 防护点 | 证据 |
|---|---|---|---|---|---|---|---|
| SQL/CMD/FILE/... | `{file:line API}` | 参数/字段/片段 | `{var}` | 分支/配置/角色 | 读/写/执行/越权/... | 参数化/白名单/... | `{代码片段}` |
```

## Transform / 防护检查

每个 transform 都要判断是保持污染、改变形态、缩小控制面，还是完全阻断。

| 类型 | 示例 | 默认判断 |
|---|---|---|
| 格式转换 | trim/lower/urlDecode/jsonDecode/xmlDecode/base64Decode | 通常仍 tainted |
| 拼接组合 | concat/StringBuilder/sprintf/template string/path join | 通常仍 tainted，且可能污染更大对象 |
| 容器传播 | array/list/map/set/object field/session/cache | taint 进入字段/元素，需要字段级追踪 |
| 序列化/映射 | JSON/XML/YAML/ORM hydration/DTO mapping | 追字段映射、默认值、忽略字段、别名 |
| 类型转换 | int/bool/enum/date/UUID parse | 可能缩小注入面，但未必阻断 IDOR/业务越权 |
| 编码转义 | HTML/SQL/shell/URL/JSON escape | 只有匹配 sink 上下文才可能有效 |
| canonicalize | realpath/normalize/URL parse/DNS resolve | 只有顺序正确且重定向/编码后仍校验才可能有效 |
| 权限判断 | hasRole/owner/tenant/policy/gate | 必须在 sink 前，绑定当前对象和主体 |
| 覆盖赋值 | default/constant/server lookup | 无条件覆盖通常切断可控性 |

防护有效必须同时满足：

1. 作用在同一个污染值或唯一后继字段上。
2. 发生在 sink 前。
3. 覆盖当前执行分支、异常分支、批量元素和异步消费端。
4. 与 sink 上下文匹配。
5. 失败时 return/throw/deny/abort，不能 fallback 到原始值或危险默认值。
6. 有代码、配置或运行态证据，不靠方法名和框架默认假设。

## 路由与调用链追踪

Source→Sink trace 必须先证明入口可达，再证明每一跳传播。

### 入口枚举

- HTTP route：路由文件、注解、attribute、decorator、controller method、REST resource。
- 框架边界：Servlet/Filter/Listener、Middleware、Interceptor、Guard、Policy、AOP。
- API 入口：GraphQL resolver、RPC service、WebSocket handler、message listener。
- 非 HTTP：CLI command、scheduled job、queue consumer、webhook、file import、CMS hook。
- 动态路由、正则路由、通配符、group prefix、反向代理 prefix、route cache 必须有解析证据。

### handler 到 sink

逐层追踪：

```text
handler/controller/action
  -> service/usecase/manager
  -> repository/DAO/mapper/model/client/helper
  -> sink
```

复杂边界要特别处理：

- 依赖注入：构造函数、注解、容器绑定、provider、service registration。
- 接口/抽象类/父类/trait/mixin/decorator/AOP：解析真实实现；未解析写缺口。
- ORM/Mapper/XML/query macro/repository 基类：追到最终查询或操作。
- 事件/队列：同时追 producer 和 consumer；只追一端不能 technical_confirmed。
- 动态函数/反射/魔术方法/自动路由：必须给出解析规则或运行态补证。

每一跳记录格式：

```text
Level-N: {file:line} {class/function}.{method}({args})
输入: {sourceField/localVar}
传播: assignment/call/return/field/container/serialization/message
transform: decode/validate/escape/canonicalize/auth/default/overwrite
分支: {condition} -> 进入/不进入下一跳
输出: {nextArg/return/field/message}
证据: {关键代码}
缺口: {未解析实现/缺配置/缺运行态/缺消费端}
```

## 数据流追踪步骤

### 第 1 步：建立 trace 任务卡

```markdown
- trace_id: `{entry}:{source}:{sink}`
- 入口: `{METHOD PATH / CLI / queue / cron / webhook / file import}`
- 目标漏洞族: `{SQL/SSRF/CMD/FILE/XSS/AUTH/...}`
- source 假设: `{字段/claim/message/file/stored}`
- sink 假设: `{API/函数/配置}`
- 必需标识符: `{无 / user_id / object_id / tenant_id / file_id / lookup handle / ...}`
- 标识符获取假设: `{列表/搜索/详情/导出/日志/关系链/分享页/可预测/手工样本/未知}`
- 主体对象矩阵: `{attacker / owner / victim / control / cleanup}`
- 官方安全模型状态: `{已读/未读/unknown/expected behavior/accepted risk/in scope/out of scope}`
- 当前状态: `untraced`
```

### 第 2 步：候选定位，但不下结论

用正则、IDE、SAST、规则、依赖清单找候选：危险函数、source、raw 调用、框架差异、历史高危组件、配置关闭。记录命中位置和为什么值得追踪。命中本身只能写 `candidate-source` 或 `candidate-sink`。

候选定位要避免“搜索词替代语义”：

- 搜 `eval`、`exec`、`raw`、`query` 只能证明有危险 API。
- 搜 `$_GET`、`req.body`、`@RequestBody` 只能证明有输入读取。
- 搜 `${}`、`raw`、`unsafe` 只能证明需要复核。
- 扫描器 trace 只能证明规则模型认为存在路径。

下一步必须把候选拆成可复核任务卡：`source candidate`、`sink candidate`、`propagation candidate`、`sanitizer candidate`、`runtime gap`。

### 第 3 步：写入口请求或消息样例

写清 method、path、query、headers、cookies、body、multipart、认证状态、对象 ID、租户、前置数据。非 HTTP 场景写 CLI argv、queue message、webhook payload、file import 样例。准备动态验证时使用测试对象和唯一 marker。

如果请求依赖对象标识符，不要只写 `{id}` 占位符。必须同时写：

- 这个 ID 是从哪里拿到的：列表、详情响应、搜索、导出、日志、关系链、分享页、可预测序列、批量接口，还是只能由管理员手工给出。
- 这个 ID 属于谁：attacker 自己对象、victim 对象、control 对象、跨租户对象、公开对象还是未知对象。
- 这个 ID 的可获得规模：单个样本、同类多个、分页批量、持续获取、可枚举、可导出、不可获得。
- 这个 ID 是否被服务端重新绑定到当前主体；如果查询同时绑定 owner/tenant，ID 可控不等于越权成立。

如果 ID 只能从手工样本得到，trace 可以继续定位代码问题，但报告结论必须降级，不能写成高价值 technical_confirmed 或批量影响。

### 第 4 步：定位参数进入点

记录读取 API、绑定变量、类型、默认值、数组/对象/嵌套字段、claim/session 来源、文件内容或文件名。框架自动绑定必须读 binder/serializer/form/model 配置。

### 第 5 步：追踪变量传播

逐层记录：

- 直接赋值：`cmd = request['cmd']`。
- 函数处理：`cmd = trim(input)`，继续判断 transform 语义。
- 跨函数：caller arg → callee param。
- 跨文件：include/import/autoload/模块导入。
- 数组/集合：`arr['cmd']`、`map.get('url')`、bulk list 每个元素。
- 对象属性：`dto.url`、getter/setter、Lombok、property accessor、mass assignment。
- 多来源拼接：每个片段分别追 source 和限制。
- 编码/解码：base64/url/json/xml/yaml decode 后继续追。
- 动态调用：函数名、类名、方法名、模板名、表达式名可控时，额外证明最终目标。

传播过程中遇到以下情况要单独建子任务，不要口头略过：

- alias：两个变量/引用/指针/对象属性指向同一底层对象。
- mutation：helper 原地修改对象、Map、数组、builder、request attribute、context。
- merge：默认配置、用户配置、数据库配置、请求配置合并，后者是否覆盖前者。
- serializer：字段别名、忽略字段、unknown fields、extra fields、case-insensitive binding。
- collection：批量列表每个元素是否逐项校验、逐项授权、逐项进入 sink。
- async：message body、headers、routing key、consumer schema 是否与 producer 一致。
- persistence：写入字段和读取字段是否一致，中间是否经过审核、转义、清洗、模板编译或缓存刷新。

### 第 6 步：记录 transform、覆盖和分支

```markdown
| 位置 | 输入变量 | transform/覆盖/防护 | 条件 | true 分支 | false 分支 | 可控性影响 | 证据 |
|---|---|---|---|---|---|---|---|
```

必须记录 return、throw、continue、break、redirect、try/catch/fallback。安全检查失败后如果仍继续执行或换到危险默认路径，防护无效。

### 第 7 步：定位 sink 参数位置

不要只写“调用了 execute/render/exec”。要写：

- sink API/function。
- 第几个参数、哪个字段、哪个 SQL 片段、哪个 URL 部件、哪个 path、哪个 header、哪个模板表达式是危险位置。
- tainted 变量如何映射到该危险位置。
- sink 执行条件和防护点。

### 第 8 步：判断可控性和实际使用

```markdown
| Source | Sink | 路径状态 | 实际使用 | 可控性 | 防护状态 | 影响状态 | 结论 |
|---|---|---|---|---|---|---|---|
| `{source}` | `{sink}` | COMPLETE/PARTIAL/UNRESOLVED | 是/否/部分 | FULL/FIELD/CONDITIONAL/... | 有效/不足/未确认 | 已证/待证/无影响 | technical_confirmed/candidate/blocked/rejected |
```

可控性常用状态：

- `FULLY_CONTROLLABLE`：完整值可控。
- `FIELD_CONTROLLABLE`：对象/JSON/DTO/数组中部分字段可控。
- `CONDITIONALLY_CONTROLLABLE`：满足分支、格式、角色、配置时可控。
- `ALLOWLIST_CONTROLLABLE`：只能选允许值；仍要判断允许值是否危险。
- `TYPE_LIMITED_CONTROLLABLE`：类型/范围缩小；可能阻断注入但不一定阻断越权。
- `STORED_CONTROLLABLE`：攻击者可先写入，后续读取进入 sink。
- `SERVER_CONTROLLED` / `OVERWRITTEN`：通常降级或 rejected。
- `UNRESOLVED`：证据不足，只能 candidate/blocked。

### 第 9 步：推进强正控、最高影响和负控

当 trace 显示可利用潜力时，不要停在弱 marker：

```text
trace complete -> sink 参数可控 -> 防护不足 -> 弱正控 -> 强正控 -> 最高影响 -> 负控 -> 清理/恢复
```

SQL 从错误栈推进到布尔/时间/常量/测试表；RCE 从 marker 推进到命令输出、执行身份、受控文件；SSRF 从 callback 推进到最终 URL/IP、受控内网 canary、metadata mock；IDOR 从对象 ID 替换推进到双账号双对象；文件类从路径拼接推进到 resolved target 和受控读写；XSS 从反射推进到浏览器执行。

IDOR、未授权、对象级授权、批量越权类 trace 还要继续推进两件事：

1. **标识符获取**：证明 attacker 能从自己的入口获得 victim/control 对象 ID，或证明只能获得单对象、不能批量、完全不可得。
多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

只完成 “A 账号替换 B 对象 ID 返回 200” 还不够。若 ID 获取链缺失，最多写“手工样本下可疑 / blocked / candidate”；若要写批量或广义影响，必须证明攻击者能批量、持续、枚举、列表、搜索、导出或可推导获得大量 ID。

### 第 10 步：写完整性声明

```markdown
## Trace 完整性声明
- trace_status: COMPLETE / PARTIAL / UNRESOLVED
- 已证明:
  - {入口/source/binding/某几跳/sink/防护缺口/运行态/官方安全模型/...}
- 未证明:
  - {缺实现类/缺消费端/缺运行配置/缺负控/缺官方门禁/...}
- Allowed Claims:
  - {当前证据允许声明的具体边界}
- Forbidden Claims:
  - {不得声明 technical_confirmed/无需认证/任意/RCE/全局影响/对外提交资格/...}
- 下一步:
  - {补证或修复验证动作}
```

## 必检证据点

| 证据点 | 必须回答 |
|---|---|
| `EVID_ROUTE_MATCH` | 入口是否注册、启用、可命中；middleware/guard 顺序是什么 |
| `EVID_SOURCE_ENTRY` | source 字段、来源、控制主体、控制粒度、请求样例是什么 |
| `EVID_PARAM_BINDING` | source 如何进入变量/DTO/Model/claim/message/file row |
| `EVID_TRACE_HOP_N` | 每一跳 file:line、变量名、输入/输出、调用关系是什么 |
| `EVID_TRANSFORM_N` | transform、防护、覆盖、分支如何影响 taint |
| `EVID_BRANCH_EXECUTION` | sink 所在分支是否会执行，提前退出是否阻断 |
| `EVID_SINK_PARAM_MAPPING` | 污染值是否进入 sink 危险参数位置 |
| `EVID_SANITIZER_EFFECT` | 防护是否同变量、同分支、同上下文且失败阻断 |
| `EVID_AUTH_DECISION` | 主体、角色、对象、tenant/owner 条件是否在 sink 前执行 |
| `EVID_IDENTIFIER_ACQUISITION` | 漏洞依赖的 ID / handle / token / URI 是否由攻击者可得；获取路径、获取主体、单对象/批量边界是什么 |
| `EVID_ACCOUNT_OBJECT_MATRIX` | 多主体、多对象或跨租户 trace 中，账号、账号对象矩阵必要事实、主体 ID、角色、租户、对象归属、token/cookie 引用和清理责任是什么 |
| `EVID_OFFICIAL_SECURITY_MODEL` | 官方资料、范围、默认配置、已知风险、预期行为、对象/租户/插件/沙箱边界和对外提交限制是什么 |
| `EVID_STRONG_POSITIVE` | 强正控是否证明真实漏洞语义 |
| `EVID_NEGATIVE_CONTROL` | 负控是否排除缓存、正常功能、权限本该允许、工具误报 |
| `EVID_IMPACT_PROOF` | 影响是否是受控测试数据/状态/文件/请求/命令/浏览器执行 |
| `EVID_CLEANUP_RESTORE` | 副作用是否清理、恢复或证明无副作用 |

漏洞族细化证据：

- SQL：执行点、字符串构造、用户参数到 SQL 片段、参数化/白名单、查询语义差异。
- CMD/RCE：执行点、命令字符串/参数构造、用户片段映射、命令输出/执行身份/受控文件。
- SSRF：URL 归一化、最终 URL/host/port、重定向后校验、DNS/IP 内网拦截、出站日志。
- FILE/UPLOAD/ARCHIVE：resolved target、base 约束、entry name、内容来源、覆盖模式、写后可达、清理。
- XSS/TPL：输出上下文、raw/safe/escape、浏览器执行、CSP、存储触发。
- XXE/DESER/EXPR：解析/反序列化/求值入口、输入来源、危险配置、触发链、沙箱/类型限制。
- AUTH/IDOR/CSRF：路径保护、token/claim、权限函数、owner/tenant 条件、状态变更、双主体对照。

## 动态验证触发条件

必须动态验证的场景：

- 静态 trace 闭合，但影响依赖运行态：越权、SSRF、文件读写、命令执行、上传可访问性、CSRF、缓存/队列、组件可达性。
- 防护是否生效依赖配置、middleware 顺序、运行版本、feature flag、数据库方言、代理路径、object storage policy。
- 需要证明对象级授权、租户隔离、角色差异、双主体/双对象。
- 扫描器结果要升级 technical_confirmed。
- source 是存储型污染，需要证明写入端与读取端在同一运行环境相连。
- 需要证明最高影响、执行语义、服务端请求、文件边界或状态改变。
- trace 将进入报告，需要证明官方安全模型是否承认该边界，或当前行为是否只是预期功能、accepted risk、范围外或 hardening only。

静态证据足够进入 candidate 的场景：

- source→sink 静态链路较完整，但缺账号、对象、日志或负控。
- sink 参数可控，但防护是否覆盖当前 runtime 未确认。
- 动态调用、依赖注入或异步消费端部分未解析。
- 组件版本命中并有调用点，但缺实际触发输入。
- 官方安全模型、范围、默认配置或 known risk 未读完。

不能继续动态验证的场景：

- 目标不在授权范围。
- 会访问第三方真实系统或真实用户数据。
- 会暴露、复用、转储真实 secret、token、cookie、密码或云凭据。
- 无测试账号、测试对象、日志观察、快照、回滚或清理能力。
- 只能通过不可控、不可回滚、无法隔离的方式观察影响。

## 授权实验模式下的强验证方法

以下方法只用于自有、授权、隔离、可重置环境；payload 必须按实际上下文调整，并绑定测试对象、唯一 marker、日志观察点和清理步骤。

| 漏洞族 | 强验证目标 | 观察点 | 负控 |
|---|---|---|---|
| SQL/NoSQL | 布尔/时间稳定差异、常量回显、测试表读写、测试对象越权 | SQL/ORM 日志、响应差异、测试表、count/schema 元信息 | false 条件、合法值、参数化修复、无权限账号 |
| CMD/RCE | stdout/stderr、执行用户、工作目录、受控文件、受控回连 | 进程日志、命令结果、受控文件、DNS/HTTP canary | 普通值、移除字段、禁止命令、修复后 |
| SSRF | 最终 URL/IP、重定向后目标、内网 canary、metadata mock、响应可读性 | 出站日志、canary 请求、目标响应、DNS 解析 | 允许/禁止 host、重定向对照、本地/外网对照 |
| XSS/TPL | 浏览器执行、DOM 变化、存储触发、目标角色触发、CSP 影响 | DevTools、Console、测试 endpoint、页面 DOM | 编码后值、不同上下文、安全模板、CSP 对照 |
| FILE/UPLOAD/ARCHIVE | base 外 canary、受控写入、写后可达、执行/非执行边界 | resolved path、文件内容、HTTP 访问、清理结果 | base 内/外、安全文件、禁止扩展、修复后 |
| XXE/DESER/EXPR | 外部实体/OOB、受控 gadget/测试类、表达式执行、沙箱边界 | parser 日志、OOB、受控文件/命令/函数返回 | 禁用外部实体、类型白名单、沙箱开启 |
| AUTH/IDOR/CSRF | 双账号双对象、跨租户、状态改变、token 缺失/错误 | 响应数据、对象状态、审计日志、业务副作用 | 自己对象、他人对象、无权限、缺 token、错误 token |

弱 payload 失败时，先确认：payload 是否到达 sink、上下文是否匹配、编码是否正确、权限是否满足、观察点是否正确、防护是否真实生效。不能因为一次弱 payload 阴性直接 rejected。

## 最高危害追踪

对每条 candidate 按以下阶梯推进，直到达到当前授权环境可证明上限或明确停止原因：

```text
可触发 -> 可控 -> sink 执行 -> 强正控 -> 可读/可写/可越权/可执行/可横向 -> 负控 -> 清理 -> 声明边界
```

停止继续追踪必须写具体原因：

- 已达到当前测试范围内最高可证明影响。
- 防护经同变量、同分支、同上下文证据证明有效。
- 缺测试账号、对象、日志、回连、快照或清理能力。
- 继续验证会越出授权范围、触碰真实生产数据、真实凭据或第三方系统。
- 当前环境不支持触发该 sink，需要运行态补证。

禁止把低层现象夸大：

- callback-only SSRF 不能写内网敏感访问。
- marker-only RCE 不能写命令执行。
- error-only SQLi 不能写数据读取。
- reflect-only XSS 不能写浏览器执行。
- version-only SCA 不能写组件漏洞可达。
- secret-regex-only 不能写有效凭据泄露。

## 负控设计

负控用于证明正控结果由漏洞条件导致，不是正常功能、缓存、随机、权限本该允许、错误页、WAF、限流或工具误报。

| 发现类型 | 必要负控 |
|---|---|
| SQL/NoSQL | true/false、time/no-time、安全值、参数化修复、不同租户/权限 |
| RCE/CMD | 普通值、无分隔符、移除字段、禁止命令、命令输出差异 |
| SSRF | 允许 host、禁止 host、重定向后禁止目标、本地 canary 与外网 canary |
| XSS | 编码后值、不同输出上下文、CSP/模板安全模式、浏览器不执行对照 |
| FILE | base 内合法文件、base 外 canary、不存在文件、编码/双编码对照 |
| UPLOAD/ARCHIVE | 安全扩展、禁止扩展、base 内/外 entry、执行禁用策略 |
| IDOR/AUTH | 账号 A 对象 A、账号 A 对象 B、账号 B 对象 B、跨租户、无登录 |
| CSRF | 正确 token、缺 token、错误 token、Origin/Referer/SameSite 对照 |
| SCA/组件 | 组件未加载、版本修复后、不可达调用点、触发条件缺失 |

technical_confirmed 至少要有一个与 claim 对齐的负控；高危/严重结论通常需要多组负控。

## technical_status 方法性判定边界

### technical_confirmed

必须同时满足：

- 入口可达。
- source 控制主体与控制粒度已证明。
- 参数绑定清楚。
- trace_status 为 COMPLETE，或静态 trace 与运行态证据等价闭合。
- 污染值到达 sink 危险参数位置，并且该参数被实际使用。
- 防护不足或被绕过，缺口具体。
- 若漏洞依赖 ID、对象 handle、分享 token、资源 URI 或租户标识，`EVID_IDENTIFIER_ACQUISITION` 已证明攻击者可获得路径，并且声明范围不超过可获得规模。
- 若漏洞依赖多主体、多对象或跨租户，`EVID_ACCOUNT_OBJECT_MATRIX` 已证明账号对象矩阵、对象归属、token/cookie 隔离和清理责任；没有混用账号或对象。
- 若这条 trace 将进入报告，`EVID_OFFICIAL_SECURITY_MODEL` 已证明官方资料、范围、默认配置、已知风险和预期行为支持当前声明。
- 强正控证明真实影响或最高可证明影响。
- 负控成立。
- 清理/恢复完成，或验证无副作用。
- Allowed Claims 与证据一致，Forbidden Claims 写清。

### candidate

用于这些情况：

- source/sink 有线索，但中间层、字段级映射、实现类、动态调用、异步消费端缺失。
- 参数可能可控，但覆盖、白名单、类型转换、防护语义未判定。
- 静态 trace 较完整但缺强正控、影响证明或负控。
- 扫描器 taint trace 未人工核对 binding、field mapping、sanitizer、actual use。
- 弱 payload 失败但尚未证明路径不可达或防护有效。
- trace 依赖对象 ID，但目前只有手工样本、管理员提供 ID、旧报告 ID 或单个不可泛化 ID，尚未证明攻击者可获得路径。
- 多对象、批量或跨租户声明缺少足够 ID 获取规模或账号矩阵。
- 官方安全模型、范围、默认配置或 known risk 还没读完，不能写对外可提交。

### blocked

用于必须依赖运行态才能裁决的情况：

- 需要测试账号、对象、租户、CSRF、session、JWT/OAuth claim。
- 需要 route cache、middleware 顺序、feature flag、运行版本、构建产物。
- 需要日志、数据库、缓存、队列、文件、对象存储、DNS/HTTP 回调、浏览器环境。
- 需要双主体/双对象/双租户负控。
- 需要证明对象 ID、用户 ID、租户 ID、文件 ID、分享 token、lookup handle 或资源 URI 能否由攻击者获得。
- 需要补齐账号矩阵、账号对象矩阵必要事实、对象归属、token/cookie 隔离或清理能力。
- 需要补齐官方安全模型、范围、默认配置、known risk、accepted risk 或预期行为裁决。
- 需要快照、重置或清理能力才能做强验证。

### rejected

只有具备排除证据时才写：

- 入口不可达、未注册或当前配置不启用。
- source 不可控或只在前端存在。
- source 未绑定到目标变量，或未进入 sink。
- sink 参数不是危险参数，或 sink 使用服务端固定值。
- 参数被无条件覆盖，或白名单/类型/授权真实阻断当前风险。
- 强正控和负控证明参数变化不影响 sink 或影响不成立。
- 组件未打包、未加载、版本不受影响或漏洞路径不可达。
- 依赖对象标识符的漏洞，经代码、接口和运行态证据证明攻击者无法获得必要 ID，且不存在可列表、搜索、导出、关系链、分享页、可预测或可推导路径。
- 多主体结论所需账号/对象关系经负控证明为正常授权、公开对象、自己对象或权限本该允许。
- 官方安全模型明确该行为是预期功能、受信任主体正常能力、accepted risk、范围外或 hardening only。

rejected 必须写 `file:line`、配置、请求/响应、日志、负控或依赖/运行版本证据，不得只写“看起来安全”。

## 报告与产物边界

本 Skill 不内嵌报告正文或模板章节。需要输出报告时，只把本 Skill 产生的方法性事实写入对应 evidence，并由报告阶段引用唯一模板渲染：

- 入口、Source、Binding、Guard、Flow、Sink、Trigger、Effect、Negative、Clean、Claim 统一登记为 `EVID_*` 证据。
- 单漏洞 Markdown 只使用 `templates/单漏洞提交报告模板.md`。
- 提交总入口只使用 `templates/赏金提交总入口模板.md`。
- 完成核验只使用 `templates/完成核验模板.md`，只能检查，不能补证。
- 本 Skill 可以说明应写入哪些事实，但不得复制报告章节正文、平台表单、账号对象矩阵字段或外部门禁裁决规则。

## 修复建议写法

修复建议必须匹配根因和框架机制：

- SQL/NoSQL/LDAP/XPath：值位置使用参数化；动态表名、列名、排序、operator、DSL 结构用服务端白名单。
- 命令执行：避免 shell 拼接；使用参数数组、固定命令、允许列表、隔离执行用户和最小权限。
- SSRF：scheme/host/port allowlist，DNS/IP 解析后校验，重定向后重新校验，拒绝 metadata/内网，统一 HTTP client wrapper。
- 文件/上传/归档：decode/canonicalize/realpath 后做 base 约束；随机文件名；web 根外存储；禁执行；entry 路径归一化；清理临时文件。
- XSS/模板：使用上下文转义；禁 raw/safe；模板名白名单；关闭用户可控模板编译；补浏览器回归测试。
- XXE/反序列化/表达式：禁外部实体和网络；类型白名单；关闭危险 default typing；模板/表达式沙箱；禁止用户可控对象图。
- Auth/IDOR/CSRF：服务端对象级授权、tenant/owner 条件、逐项批量授权、CSRF token 全分支覆盖、Origin/SameSite 辅助防护。
- Secret/配置：移出客户端和仓库；服务端签名；最小权限；轮换；日志脱敏；debug 关闭。
- 测试：为 source→sink、负控、权限矩阵、修复后阻断写单元/集成/回归测试。

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
- 禁止 callback-only SSRF 写成内网高危 technical_confirmed。
- 禁止 marker-only RCE 写成命令执行 technical_confirmed。
- 禁止 error-only SQLi 写成数据读取 technical_confirmed。
- 禁止 reflect-only XSS 写成浏览器执行 technical_confirmed。
- 禁止 version-only SCA 写成组件漏洞可达 technical_confirmed。
- 禁止弱 payload 失败直接 rejected。
- 禁止把“已知 ID 后可利用”写成高价值 technical_confirmed，却不证明攻击者如何获得该 ID。
- 禁止把单对象 ID 样本外推成批量、全租户、全用户、全工作区或广义影响。
- 禁止管理员手工给出的 ID、聊天上下文里的 ID、历史附件里的 ID、报告作者笔记里的 ID 当作攻击者可获得路径。
- 禁止账号矩阵缺账号对象矩阵必要事实、主体 ID、租户、对象归属、token/cookie 引用和清理责任时声称多主体 technical_confirmed 可复核。
- 禁止在官方安全模型 unknown、scope unknown、默认配置 unknown 或 known risk 未去重时写对外可提交。
- 禁止为了凑数量写低价值漏洞。
- 禁止把项目运行、部署、恢复、调度、监控内容混进漏洞审计 skill。
- 禁止把当前工作记录、来源叙事、不可公开的环境细节、内部命名或临时任务过程写进通用 skill。
- 禁止越出授权范围、测试第三方真实目标、导出真实凭据、泄露真实生产用户敏感数据或执行不可清理验证。

## 自检清单

每项回答 `是 / 否 / 不适用`：

### Source

- [ ] 是否识别 query/path/body/header/cookie/JSON/XML/multipart？
- [ ] 是否识别 GraphQL/WebSocket/CLI/webhook/queue/cron/file import？
- [ ] 是否识别 session/JWT/OAuth claim 和 framework request object？
- [ ] 是否识别 stored taint：数据库、缓存、文件、对象存储？
- [ ] 是否证明 source 的控制主体、权限边界和控制粒度？
- [ ] 客户端隐藏参数、签名头、硬编码 key 是否证明后端实际信任？
- [ ] 若 trace 依赖对象 ID、租户 ID、文件 ID、分享 token、lookup handle 或资源 URI，是否证明攻击者如何获得？
- [ ] 若报告写多对象、批量、持续、全量或广义影响，是否证明 ID 能批量、持续、枚举、列表、搜索、导出、关系链或可推导获得？
- [ ] 是否把手工样本 ID、管理员提供 ID、旧报告 ID 和攻击者可获得 ID 区分开？

### Trace

- [ ] 是否从入口追到 handler/controller？
- [ ] 是否从 handler 追到 service/repository/mapper/model/helper/client？
- [ ] 是否处理父类、接口、trait、helper、middleware、decorator、依赖注入、注解/attribute、AOP、反射？
- [ ] 是否处理事件、队列、定时任务、异步消费端？
- [ ] 是否记录每一跳 `file:line`、变量名、输入/输出、分支？
- [ ] 是否给出 trace_status：COMPLETE/PARTIAL/UNRESOLVED？
- [ ] 若是 AUTH/IDOR/对象级授权 trace，是否有 A/B 主体、A/B 对象、跨租户或 control 对象的账号矩阵？
- [ ] 账号对象矩阵是否记录主体 ID、租户/工作区、角色、对象归属、token/cookie 隔离和清理责任；具体凭据字段以账号对象矩阵模板为准？
- [ ] 若 trace 要写成报告，是否查阅并裁决官方安全模型、scope、默认配置、known issues 和 accepted risk，而不是只看代码链路？

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

### 判定与报告

- [ ] 是否给出 finding 状态：technical_confirmed/candidate/blocked/rejected？
- [ ] 是否说明 candidate/blocked 缺哪些证据？
- [ ] 是否说明 rejected 的排除证据？
- [ ] 是否避免“已知 ID 后可利用”直接写高价值 technical_confirmed？
- [ ] 是否避免单对象结果外推成批量、全局或广义影响？
- [ ] 是否避免 scanner-only、external-tool-only、sink-only、regex-only、无负控 technical_confirmed？
- [ ] 是否写清 Source、Sink、Trace、防护缺口、复现、Web 操作、负控、影响证明、最高危害、修复建议、Allowed Claims、Forbidden Claims？
- [ ] 是否没有混入不可公开的环境细节、来源叙事、临时任务记录或运维内容？
