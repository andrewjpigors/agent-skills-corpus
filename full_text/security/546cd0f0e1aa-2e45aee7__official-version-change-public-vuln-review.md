---
name: official-version-change-public-vuln-review
description: Use when auditing official releases, changelogs, compare diffs, security advisories, CVEs, GHSAs, OSV records, issues, patches, image tags, image digests, dependency updates, version drift, latest-version claims, or whether runtime code is affected by a publicly fixed vulnerability.
---

# 官方版本变更与公开漏洞复核

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 定位

本 Skill 用于把“官方现在最新是什么、官方最近改了什么、公开漏洞是否影响当前运行态、历史修复是否真的修完整”变成可复核的审计线索。

它专门防止以下错误：

1. 把搜索摘要、旧会话、README 示例、安装日志、镜像 tag 或模型记忆当成官方 latest。
2. 把 CVE / GHSA / OSV / NVD / advisory / issue / release note / patch diff 命中当成漏洞已经确认。
3. 只看安全提交标题或一小段代码，就说历史漏洞已修完、当前版本无回归。
4. 启动环境后不核对 runtime version、image digest、运行配置和插件/worker 状态。
5. 忽略官方最近几个版本刚改过的鉴权、反序列化、模板、RCE、SSRF、文件、依赖、默认配置或沙箱边界。

核心原则：**官方变更只决定优先看哪里；公开漏洞只决定优先复核什么。只有当前运行版本、当前代码/产物、可控 source、可达 sink、强验证、负控、清理和声明边界闭合，才允许进入 confirmed。**

本 Skill 不替代官方安全模型、目标范围隔离、Source→Sink 追踪、动态验证、最高影响证明、Allowed Claims、提交门禁或报告复核。skill 不是漏洞证据；它的作用是给这些门禁提供版本、补丁、公开漏洞和漂移事实。

## 触发场景

以下任一情况必须使用：

- 需要安装、拉取镜像、启动环境、声明 latest / 最新版本 / fixed version。
- 用户或其他 AI 询问“你确定是官方最新版本吗”。
- 目标运行的是旧版本、旧 commit、旧镜像 tag、旧 digest、旧 lockfile、旧插件或旧依赖。
- 需要判断当前目标是否受 CVE、GHSA、OSV、NVD、vendor advisory、官方 security advisory、公开 PoC、历史 issue 影响。
- 需要复核官方最近几个 release、changelog、compare diff、PR、commit、测试、迁移文档。
- 官方改动触及鉴权、权限、对象边界、反序列化、模板、命令执行、SSRF、文件、上传、解压、SQL/NoSQL、secret、默认配置、插件、runner、worker、沙箱、依赖或构建链。
- 扫描器或其他模型/工具 只给了 version-only、CVE-only、diff-only、issue-only、PoC-only 结论。
- 容器、依赖、镜像、插件、advisory 或官方 release 可能更新，需要防止版本事实漂移。
- 需要判断补丁是否只修了一个入口、一个分支、一个源码文件，而当前运行产物仍可达。

## 与项目字段的关系

本 Skill 使用项目中已经存在的字段，不创造旧字段或兼容字段。

### 覆盖矩阵.version_identity_gate

版本身份三点核验写入：

```text
version_identity_gate.status
version_identity_gate.official_latest_version
version_identity_gate.image_tag_or_digest
version_identity_gate.runtime_version
version_identity_gate.decision_if_mismatch
version_identity_gate.corrections
version_identity_gate.forbidden_until_verified
```

`version_identity_gate.status` 只使用项目已有状态：

```text
version_identity_verified
version_identity_mismatch
version_identity_unknown
correction_required
not_applicable
```

含义：

| 状态 | 使用条件 | 禁止外推 |
|---|---|---|
| `version_identity_verified` | 官方最新、计划产物或镜像、当前运行版本均已核对，且查询时间明确 | 仍不能替代 Source→Sink、强验证和负控 |
| `version_identity_mismatch` | 当前运行版本与官方最新、fixed、源码或镜像 digest 不一致 | 必须决定切换到官方最新，或保留旧版本做补丁前后复核 |
| `version_identity_unknown` | 任一关键版本事实缺失 | 不得声明 latest、fixed、current affected、rejected、not_official_known、对外可提交或完成 |
| `correction_required` | 已发现先前版本说法错误 | 必须追加 correction 并更新受影响结论 |
| `not_applicable` | 当前动作完全不涉及版本、安装、运行态、公开漏洞或提交判断 | 不能为了绕过版本门禁而使用 |

### 覆盖矩阵.version_change_public_vuln_review

官方变更和公开漏洞复核写入：

```text
version_change_public_vuln_review.status
version_change_public_vuln_review.current_runtime_facts
version_change_public_vuln_review.official_version_window
version_change_public_vuln_review.public_vulnerability_sources
version_change_public_vuln_review.version_drift_recheck_required_before_claim
version_change_public_vuln_review.blocking_rule
```

它记录的是候选来源和版本事实，不是漏洞成立证据。

### 覆盖矩阵.historical_public_vuln_fix_review

历史漏洞和安全修复完整性写入：

```text
historical_public_vuln_fix_review.status
historical_public_vuln_fix_review.items
historical_public_vuln_fix_review.blocking_rule
historical_public_vuln_fix_review.forbidden_until_complete
```

`historical_public_vuln_fix_review.status` 只使用项目已有状态：

```text
not_started
historical_fix_review_partial
complete
needs_runtime
blocked
not_applicable
```

不要新造版本状态、旧字段或不存在字段。

## 版本身份三点核验

涉及 latest、安装、启动、版本影响、修复状态、公开漏洞复核或提交结论前，必须核验三点。

| 核验点 | 合格证据 | 不合格证据 |
|---|---|---|
| `official_latest_version` | 官方 release、tag、advisory、vendor 页面、官方 registry、官方包仓库或官方 API；包含版本、发布时间、链接、查询时间 | 搜索摘要、搜索引擎片段、第三方博客、README 示例、旧会话、模型记忆 |
| `image_tag_or_digest` | 镜像 tag 对应 manifest digest、release asset hash、包版本、lockfile、SBOM、签名、provenance；记录查询时间 | 只写 `latest`、安装日志、compose 示例、模糊 tag、镜像名 |
| `runtime_version` | 运行中应用接口、版本文件、包元数据、进程加载路径、镜像 label、binary metadata、容器 digest、日志 banner | 源码 tag、镜像名、安装命令、未运行容器、推测 |

执行规则：

- 安装或拉取前，至少确认官方最新版本和计划使用的 tag/digest；不能把搜索结果当 latest。
- 启动后，必须立即确认 runtime_version；未确认前不得说“当前运行的是最新版”。
- latest 是可变标签，不是固定版本；必须解析到 digest、release asset 或运行态版本。
- `runtime_version != official_latest_version` 时，必须先选择：切到官方最新版本审计，或保留旧版本做补丁前后差异 / 回归验证。
- 任一点缺失时，只能写 `version_identity_unknown`、`version_drift_unknown`、`blocked` 或 `blocked`。
- 一旦发现版本说错，必须追加 correction：错误说法、错误依据、正确事实、正确来源、影响哪些结论、后续动作。

## 历史环境、当前环境、真实目标环境分层

不要把不同环境的结论合并：

| 层级 | 可声明 | 不可声明 |
|---|---|---|
| 历史旧版本 / 旧配置 | 只能声明该旧环境在记录时间和配置下 confirmed | 不得外推当前版本、真实站、latest 或所有部署受影响 |
| 当前本地/实验运行态 | 只能声明当前运行版本、digest、配置、账号对象和触发链的结果 | 不得在版本身份 unknown 时写 fixed、affected、not_official_known 或 submit-ready |
| 官方 fixed / patched 版本 | 只能声明官方已修复点、补丁语义和当前代码是否加载修复 | 不得仅因 fixed 就说所有部署安全；必须有运行态负控 |
| 真实目标版本 unknown | 只能写 unknown / blocked / 需要版本核验 | 不得把 lab confirmed 写成真实目标 affected |

官方已知、advisory-covered、duplicate、known-limitation、accepted risk 或官方明确修复，是提交资格硬门禁。只有证明新主体、新入口、新对象、新默认配置、新版本、更高影响或官方缓解绕过时，才允许继续进入外部门禁复核。

## 版本事实分层

不得把不同层级混为一谈。

| 层级 | 含义 |
|---|---|
| official latest | 官方当前最新 release / tag / advisory / registry 所指版本 |
| fixed version | 官方、漏洞库或补丁声明修复该问题的版本 |
| repo version | 仓库默认分支、tag、commit 当前状态 |
| source version | 本轮实际审计的源码 tag / commit / patch |
| dependency version | lockfile、依赖树、vendor、SBOM 中的包版本 |
| artifact version | jar、wheel、npm bundle、release asset、binary、plugin 的实际版本 |
| image version | 镜像 tag、manifest digest、平台 digest、image label、layer |
| runtime version | 进程实际加载的代码、配置、插件、worker、依赖和镜像 |
| doc version | 官方文档、release note、advisory 适用的产品版本 |

判断优先级：**runtime > artifact / image digest > lockfile / SBOM > source tag > README / release 文案。**

禁止：

- 把“源码已修”写成“运行已修”。
- 把“tag 相同”写成“digest 相同”。
- 把“fixed version 存在”写成“当前部署已修”。
- 把“官方最新”写成“当前运行最新”。
- 把“当前运行旧版”写成“官方最新受影响”。

## latest 纠错规则

只要出现以下情况，必须追加 correction，不得静默改口：

- 先前把旧版本说成 latest。
- 先前只看搜索摘要就判断官方最新。
- 先前把 Docker / OCI tag 当固定版本。
- 先前没有启动后核对 runtime_version。
- 先前把源码版本、镜像版本和运行版本混用。
- 先前把官方已修复说成当前运行已修。

Correction 至少写：

```text
wrong_statement:
wrong_basis:
correct_fact:
official_source:
runtime_or_artifact_source:
checked_at:
affected_outputs:
required_action: downgrade / rerun / switch_version / keep_old_for_diff / update_report / block_claim
```

Correction 是客观事实，不是道歉段落；不得把聊天过程、情绪评价或模型表现写入正式产物。

## 版本和公开资料会漂移

以下事实都可能变：

- 最新 release。
- Docker / OCI image tag 指向的 digest。
- advisory 的 affected range 和 fixed version。
- CVE / GHSA / OSV / NVD 记录。
- issue、PR、维护者评论。
- lockfile、base image、插件、runner、CI action。
- 运行容器是否被重建或替换。

因此必须记录 `checked_at`，并在进入 confirmed、rejected、not_official_known、对外可提交或最终报告前重新确认关键事实。重新确认失败时，不得沿用旧结论。

如果容器、镜像、依赖、插件或运行服务发生更新、重建、替换，必须重新确认：

- official latest。
- image digest 或 release artifact。
- runtime version。
- 当前配置、feature flag、plugin、worker。
- 公开漏洞 affected range 是否仍适用。
- 先前补丁 diff 和运行产物是否仍一致。

## 变更优先审计

官方最近改动最值得优先看，尤其是最新几个版本和当前版本到 fixed/latest 的差异。

优先关注：

- release note、changelog、migration guide 中的 security、permission、safe、validate、sanitize、sandbox、SSRF、RCE、XSS、path、deserialize、template、upload、secret、token、default、dependency。
- compare diff 中新增的 guard、allowlist、denylist、type filter、path normalize、URL/IP 校验、权限检查、租户过滤、CSRF/CORS、签名校验。
- 新增或修改的测试用例，尤其是恶意输入、越权主体、路径绕过、URL 绕过、危险类型、模板表达式、反序列化 payload。
- 新增入口、插件、runner、worker、tool、webhook、导入导出、预览、转换、文件解析、异步任务。
- 默认配置变化：危险功能从默认开到默认关，或从默认关变成默认开。
- 依赖、base image、构建链、CI action、registry、install script、SBOM、签名和 provenance 变化。

但变更优先不等于 diff-only。每个可疑变更都必须翻译成：

```text
旧行为是什么
新行为是什么
保护了哪个变量 / 对象 / 路径 / 权限 / 网络 / 类型 / 配置边界
当前运行代码是否仍有旧行为
攻击者如何控制 source
source 是否到达 sink
当前配置是否启用或阻断
如何用强验证和负控证明
```

## 历史漏洞修复完整性门禁

看到安全提交标题、release 摘要、issue 标题或部分补丁，不等于历史漏洞复核完成。每个历史漏洞、公开漏洞、修复提交、安全相关 issue 都必须逐条映射。

| 字段 | 必须回答 |
|---|---|
| `id_or_url` | CVE / GHSA / OSV / NVD / advisory / issue / PR / commit / release note 标识、链接和查询时间 |
| `original_vulnerability_condition` | 原漏洞攻击者条件、服务端条件、入口、受影响组件、配置、影响和前置条件 |
| `affected_range` / `fixed_versions` | 受影响版本范围、修复版本、生态、包名、组件名 |
| `patch_points` | 修了哪些文件、函数、测试、配置、依赖、镜像、构建链或运行策略 |
| `patch_security_semantic` | 补丁实际保护了什么安全边界，旧行为如何变成新行为 |
| `current_code_presence` | 当前代码是否还有原入口、原 sink、同类 helper、替代触发链或绕过路径 |
| `current_runtime_reachability` | 当前运行版本、digest、配置、feature flag、plugin、worker 是否加载相关代码 |
| `regression_or_bypass_validation` | 是否做过最小复现、修复版本负控、绕过变体；没做时为什么 |
| `fix_completeness_status` | fixed / incomplete_fix / bypass_possible / needs_runtime / not_applicable / unknown |

阻断规则：

- 只看 commit message、release note 摘要、issue 标题或部分代码，只能写 `historical_fix_review_partial`。
- 没有公开漏洞清单，不能写“历史漏洞已修完”或“无历史漏洞回归”。
- 没有补丁语义复核，不能写“修复完整”。
- 没有 runtime reachability，不能写“当前运行版本已修”。
- 没有 regression / bypass / fixed-version 负控，不能把历史漏洞方向 rejected。

## 公开漏洞复核

CVE、GHSA、OSV、NVD、vendor advisory、官方 security advisory、公开 PoC、issue、扫描器告警都只是线索。

公开漏洞复核至少提取：

```text
id:
source_type: CVE / GHSA / OSV / NVD / vendor advisory / issue / PR / public PoC / scanner
affected_range:
fixed_versions:
affected_ecosystem:
affected_package_or_component:
affected_functions_or_files:
prerequisites:
config_conditions:
attacker_condition:
impact_claimed_by_source:
patch_or_reference_links:
source_modified_or_published_at:
checked_at:
current_version_in_range: yes / no / unknown
current_code_present: yes / no / unknown
current_runtime_reachable: yes / no / unknown
current_config_matches: yes / no / unknown
```

判定规则：

- affected range 命中，但函数不可达、模块未加载、配置不满足、插件未启用，只能 candidate / blocked / rejected_by_evidence。
- affected range 不命中，但补丁语义显示当前新入口、fork、backport 或默认配置仍有同类缺口，可以另开新候选，不能冒充原 CVE。
- 公开 PoC 失败不能直接 rejected，必须判断是版本、配置、入口、payload、权限、日志、网络、worker、依赖还是防护导致。
- 扫描器未报不能写没有公开漏洞；扫描器报了也不能写 confirmed。
- 漏洞库记录也会更新；进入结论前必须复核 modified / updated 时间和查询时间。

## Source / Sink / Trace 复核

版本线索必须回到当前目标调用链：

```text
官方变更或公开漏洞
  -> 当前代码/产物是否存在旧行为
  -> 入口 route / handler / worker / CLI / queue / webhook / plugin 是否可达
  -> 攻击者是否能控制 source
  -> transform / guard 是否缺失或可绕过
  -> sink 是否危险且实际执行
  -> 强验证是否证明真实影响
  -> 负控是否证明差异来自补丁边界
  -> 清理与声明边界
```

常见 source：HTTP 参数、header、cookie、文件上传、导入文件、归档内容、URL、webhook、队列消息、插件配置、workflow 节点、模板、表达式、类型名、包名、registry、CI input、stored taint、对象元数据。

高优先 sink：鉴权授权、对象级权限、JWT/session、命令执行、模板引擎、脚本引擎、反序列化、URL fetch、文件读写、归档解压、SQL/NoSQL、secret/log、构建脚本、install script、CI action、runner、worker、plugin。

没有当前目标 Source→Sink，不得把版本线索写成漏洞。

## 动态验证与负控

必须动态验证的情况：

- 要把 version-only / CVE-only / diff-only 线索升级为 confirmed。
- 要声明当前运行版本受影响、最新版本仍受影响、默认配置受影响或修复不完整。
- patch diff 指向高影响边界：RCE、反序列化、模板、SSRF、文件、上传、解压、SQL/NoSQL、鉴权、secret、依赖供应链。
- 需要证明镜像、插件、worker、runner、queue consumer、CI job 或构建产物实际加载受影响代码。
- 需要比较旧版本与修复版本行为差异。

常用负控：

- fixed version / backport / 补丁分支同 payload 不触发。
- safe config / 关闭危险功能 / 开启 allowlist、sandbox、safe loader 后不触发。
- 权限负控：匿名、普通用户、owner、admin 区分管理员正常能力。
- 对象负控：自己对象、他人对象、不同租户对象、公开对象。
- payload 负控：安全值、错误类型、错误协议、合法文件名、无危险字段。
- 入口负控：禁用插件、停止 worker、无 consumer、未注册 route。
- 产物负控：重建后 artifact hash、进程加载路径或 digest 改变。
- 漂移负控：结论前确认版本、digest、advisory 没变。

负控缺失时不得高置信 confirmed。正控失败时不得直接 rejected；先确认 payload 是否到达 sink。

## 授权实验模式下的强验证

默认验证发生在自有、授权、隔离、可重置、可清理环境。

强验证应把“版本命中”升级为“当前运行态影响”：

- 版本行为对照：旧版本触发，fixed version 或安全配置不触发。
- 补丁导向 payload：从补丁新增测试、错误处理、allowlist、parser 参数、path check、权限检查反推最小输入。
- 运行产物确认：镜像 digest、包版本、bundle、classpath、binary metadata、进程加载路径与当前服务一致。
- 最小安全复现：只使用测试对象、测试文件、测试 registry、授权 mock/canary，不读取真实用户数据或真实凭据。
- 清理：删除 canary、测试文件、测试对象、queue message、cache key、测试 registry 包，恢复配置。

范围边界：验证当前目标，不把同宿主机其他服务、其他任务、未知端口、第三方资源当跳板、回连端、补证对象或第二阶段。

## 最高影响追踪

版本变更线索不能停在“官方修过”或“版本命中”。继续追：

| 低层线索 | 继续追踪 | 可能影响 |
|---|---|---|
| release note 写 security | 找 commit / PR / test / changed sink | 新安全边界候选 |
| CVE affected range 命中 | runtime version + affected function + source | 当前版本可利用 |
| patch 新增鉴权 | 旧入口 + 低权限 source + 对象矩阵 | 越权 / 提权 |
| patch 新增 path check | 文件入口 + canary | 路径穿越 / 文件读写 |
| patch 禁危险类型 | parser/deserializer + type control | 对象注入 / RCE 链 |
| patch 限制 URL | URL source + mock/canary | SSRF / 内网边界绕过 |
| patch 升级依赖 | 运行包 + vulnerable API + source | 组件漏洞可达 |
| image digest 更新 | 旧运行容器 + 入口触发 | 镜像漏洞实际影响 |
| issue 提到默认配置 | 默认安装证据 + 负控 | 默认配置受影响或已修 |

停止继续升级必须写具体原因：缺 worker、缺双账号、缺 fixed version、缺运行产物、safe config 已阻断、继续会触碰范围外服务或真实数据、当前授权范围已达到可证明最高影响。

## 对结论的阻断规则

以下任一情况不得写 `technical_confirmed`、`rejected`、`not_official_known`、对外提交资格 或完成结论：

- `version_identity_gate.status = version_identity_unknown`。
- `version_identity_gate.status = correction_required` 但 correction 未写入相关产物。
- `runtime_version` 未确认，却声明当前运行 latest / fixed / affected / not affected。
- `historical_public_vuln_fix_review.status = not_started` 或 `historical_fix_review_partial`，却声明历史漏洞已修完、无回归或不是公开已知。
- `version_change_public_vuln_review` 只记录了标题、摘要、搜索片段、issue 编号或 CVE 编号，没有补丁语义、当前代码存在性、当前运行态可达性。
- 继续补证会触碰范围外对象或第三方资源。
- 报告需要依赖本地路径、私有脚本、旧会话、JSON 索引或未解释 artifact 才能复现版本影响。

## 方法性状态边界

### technical_confirmed

必须同时满足：

- 当前运行版本、产物、digest、配置、插件 / worker 状态已确认。
- 官方变更或公开漏洞的 affected range、fixed version、前置条件和安全语义已提取。
- 当前代码或产物仍包含受影响旧行为，且没有有效 backport / fork patch / safe config 阻断。
- Source→Sink trace 在当前目标中闭合。
- 攻击者条件、服务端条件、配置条件与公开漏洞或补丁语义一致。
- 强正控证明实际影响，不只是版本、diff、issue、advisory、scanner、HTTP 200、错误栈或 callback。
- 至少一个与 claim 对齐的负控成立，最好包含 fixed version、backport 或 safe config 对照。
- 版本漂移已在结论前重新确认。
- 测试副作用已清理。
- Allowed Claims / Forbidden Claims / Missing Evidence 完整。

### candidate

适用于：官方改动可疑但运行态未证；affected range 命中但函数可达性未证；patch diff 可疑但未转成 payload；当前代码有旧行为但缺账号、对象、日志、worker、负控或运行产物。

### blocked

适用于：缺运行版本、image digest、artifact、lockfile、部署配置、worker、queue、plugin、fixed version 环境、双账号、测试对象、canary、日志、OOB、测试 registry 或清理能力。

### rejected

只有明确反证才能 rejected：当前运行版本不在 affected range 且无同类新入口；受影响代码不在产物中；函数未加载不可达；已有 backport/fork/vendor patch 且负控有效；source 不可控；route 不可达；sink 不执行；安全配置在同路径阻断；漏洞只影响其他生态、模块、平台、插件、部署方式或受信任主体正常能力。

不得只因 PoC 失败、扫描器未报、issue 关闭、fixed version 存在，就写 rejected。

## 与证据产物和报告的映射

### 覆盖矩阵

记录当前版本、official latest、fixed version、digest、runtime、配置、版本漂移风险、官方文档/安全公告覆盖、公开漏洞复核窗口和未覆盖项。

### 候选发现

版本变更、公开漏洞、issue、advisory、PoC、scanner、diff 都先作为候选来源，记录 observed fact、inference、missing evidence，不得候选阶段写 confirmed。

### 证据链

只吸收已经回到当前目标的入口、source、transform、sink、runtime trigger、正控、负控、清理和版本边界。

### 最高影响证明

记录从 version-only / diff-only / CVE-only 到真实影响的升级过程，未证明影响和停止原因。

### 声明边界与外部门禁引用

只允许声明已验证版本、配置、主体、入口、对象和影响。版本未知、范围未知、官方已知差异未知、负控缺失、漂移未复核时，必须阻止主提交。

### 报告阶段引用边界

报告阶段应按唯一模板自包含渲染当前运行版本、官方最新 / 修复版本、查询时间、版本窗口、补丁语义、当前触发步骤、正控、负控、清理和 forbidden claims；本 Skill 只要求这些事实先进入 EVID，不复制报告阶段正文。

多主体、对象边界或登录态相关结论必须引用账号对象矩阵、对象归属、主体边界、token/cookie 引用和清理责任；报告阶段按唯一模板渲染必要复现事实，本 Skill 不重新定义账号凭据字段或正文写法。

## 方法性 Allowed Claims 边界

证据满足时才允许写：

- 当前运行版本、digest、配置和插件 / worker 状态已由运行态确认。
- 某个官方变更触及某个明确安全边界，并已映射到当前代码或产物。
- 某个公开漏洞 affected range 命中当前运行版本，且受影响函数在当前目标可达。
- 当前旧行为可由攻击者控制 source 触发，并到达 sink。
- fixed version、safe config 或 backport 负控证明同 payload 不再触发。
- 当前最高影响只覆盖已验证版本、配置、主体、入口、对象和测试数据。
- 版本、advisory、image digest 和 runtime 在结论前已重新确认未漂移。

## 方法性 Forbidden Claims 边界

缺少证据时必须禁止：

- version-only / advisory-only / CVE-only / GHSA-only / OSV-only / NVD-only / issue-only / scanner-only / diff-only confirmed。
- 把 release note 的 security 字样写成漏洞成立。
- 把搜索结果、README 示例、Docker tag、模型记忆写成 latest 事实。
- 把镜像 tag 等同于 digest，把 `latest` 当固定安全版本。
- 把源码已修等同于运行已修。
- 把 fixed version 存在等同于当前部署已修。
- 把旧版本命中扩大成所有部署、所有配置、所有入口、所有用户受影响。
- 把公开 PoC 失败直接写成漏洞不存在。
- 把历史漏洞复核不完整写成已修完、无回归、not_official_known。
- 用范围外服务、真实用户数据、真实凭据或第三方资源证明版本漏洞影响。

## 方法性 Missing Evidence 边界

缺以下任一项时，不得 confirmed：

- 官方 latest / fixed 来源和查询时间。
- 当前运行版本、digest、artifact、依赖、配置或插件状态。
- 对比窗口和补丁语义。
- 公开漏洞 affected range、fixed version、前置条件、受影响函数。
- 当前代码或产物是否存在受影响旧行为。
- 当前入口、source、sink、trace、guard 状态。
- 强正控、负控、清理。
- 版本漂移复核。
- 历史漏洞逐条映射和修复完整性状态。
- 官方安全模型或官方已知风险去重。

## 常见错误

| 错误 | 正确处理 |
|---|---|
| “搜索结果显示 latest 是 X” | 打开官方 release / registry / advisory 原始来源，记录 checked_at |
| “我拉了 latest，所以就是最新版” | 解析 tag 到 digest，启动后核对 runtime version |
| “官方 fixed 了，所以当前部署安全” | 核对当前运行版本、digest、加载路径和负控 |
| “CVE affected range 命中，所以 confirmed” | 回到当前 Source→Sink、强正控、负控和清理 |
| “PoC 没打通，所以 rejected” | 写 not_reproduced / blocked，分析版本、配置、入口、payload、worker、日志 |
| “只看安全提交标题就说已修完” | 逐条映射原漏洞条件、补丁点、当前代码存在性、运行态可达性和回归验证 |
| “issue 关闭所以没问题” | 判断关闭原因、维护者说明、版本范围、补丁语义和当前运行态 |
| “旧容器没重建也沿用新源码结论” | runtime 优先，确认进程实际加载产物 |
| “版本方向继续补证要用无关服务” | 停止并写 out_of_scope_would_be_touched，不碰范围外对象 |

## 自检清单

### 版本事实

- [ ] 是否确认 official latest / fixed / checked_at？
- [ ] 是否确认 image tag 对应 digest 或 release asset hash？
- [ ] 是否确认 runtime_version，而不是只看源码、安装命令或 tag？
- [ ] 是否区分 source、artifact、image、runtime、dependency、plugin、worker？
- [ ] 结论前是否重新确认 release、advisory、digest、lockfile、runtime 没有漂移？
- [ ] 如果之前版本说错，是否追加 correction 并阻断旧结论？

### 官方变更

- [ ] 是否查看最新几个版本、当前版本到 fixed/latest 的 compare diff？
- [ ] 是否把 commit / PR / test / changelog 翻译成旧行为、新行为和安全边界？
- [ ] 是否识别鉴权、parser、RCE、SSRF、文件、模板、反序列化、依赖、默认配置等高优先改动？
- [ ] 是否避免只凭 security 字样下结论？

### 公开漏洞

- [ ] 是否提取 affected range、fixed version、受影响组件、受影响函数、前置条件、配置条件和影响？
- [ ] 是否确认当前目标真的包含并加载受影响代码？
- [ ] 是否核对 backport、fork patch、vendor patch、safe config 或 feature flag？
- [ ] 是否避免 CVE-only / scanner-only / PoC-only confirmed？

### Source / Sink / Trace

- [ ] 是否证明攻击者能控制公开漏洞要求的输入？
- [ ] 是否证明入口、worker、queue、plugin、CI job 或运行路径可达？
- [ ] 是否证明受影响 sink 真实执行？
- [ ] 是否把补丁新增校验映射到同一变量、同一路径、同一上下文？

### 动态验证与负控

- [ ] 是否在授权可重置环境做强正控？
- [ ] 是否至少做 fixed version、safe config、权限、对象、payload、产物或漂移负控之一？
- [ ] 是否记录清理结果？
- [ ] PoC 失败时是否写成 not_reproduced / blocked，而不是直接 rejected？

### 声明边界

- [ ] Allowed Claims 是否限定版本、配置、主体、入口、对象和影响？
- [ ] Forbidden Claims 是否排除未验证的 latest、默认配置、所有部署、未认证、RCE、跨租户、批量、真实数据泄露？
- [ ] 缺证据时是否使用 candidate / blocked / blocked，而不是 confirmed？
- [ ] 报告是否自包含写清版本、查询时间、触发步骤、正控、负控、清理、测试账号对象矩阵字段和 Web / curl 复现，而不是依赖本地路径、JSON 索引、私有字段或已有登录态？

检验句：**如果删掉 CVE 编号、扫描器等级、release note 标题、搜索摘要和 外部模型/工具结论，只保留当前运行版本、官方补丁语义、Source→Sink、强正控、负控和清理，当前声明还能成立吗？如果不能，必须降级或补证。**
