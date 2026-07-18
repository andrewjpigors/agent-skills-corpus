---
name: official-docs-known-risk-gate
description: Use when an audit finding, scanner claim, report draft, exploit result, or severity decision must be checked against official documentation, security policy, intended behavior, scope, known issues, accepted risk, advisories, or disclosure rules before making a security claim.
---

# 官方文档已知风险门禁

## 权威边界

本 Skill 只保留审计方法，不定义 JSON schema、报告模板正文、提交资格状态、账号对象矩阵字段或完成核验规则。

- 字段、状态族、EVID 命名以对应中文 schema、template 和 validator 为准。
- 报告版式只引用 `templates/单漏洞提交报告模板.md`、`templates/赏金提交总入口模板.md`、`templates/完成核验模板.md`，本 Skill 不复制模板正文。
- 账号对象事实只引用账号对象矩阵和证据链；本 Skill 不重新定义账号对象矩阵字段、平台表单或正文写法。
- 提交资格只由 `evidence/赏金资格.json` 和报告与复核类提交门禁裁决；本 Skill 只提示需要外部门禁，不生成提交资格状态。
- Web 浏览器复现、截图、trace、network、console、storage/session 证据必须按 `skills/审计基础方法类/PlaywrightMCP运行证据归档/SKILL.md` 归档并回链 evidence。


## 定位

本 Skill 用于把候选漏洞放回官方资料、官方安全模型、目标范围和已知风险基线中裁决。

它只回答一个问题：**当前发现到底是新安全边界、官方已知问题、预期功能、受信任主体能力、范围外、accepted risk、配置加固、低价值情报、重复问题，还是仍然 unknown。**

它不替代 Source→Sink 追踪、漏洞类型专项、语言专项、动态验证、最高危害追踪、报告复核或提交门禁。它的输出应反哺这些门禁：限制能写什么、不能写什么、缺什么证据、是否需要继续动态补证。

核心原则：**官方资料决定解释边界，不决定弱验证；强验证证明能发生，官方门禁证明能否写成新漏洞。**

## 触发场景

以下情况必须使用：

- 新目标审计刚开始，还没有读官方 SECURITY、范围、安全策略、权限模型、默认配置、release notes、known issues 或 advisory。
- 候选发现准备写 `technical_confirmed`、高危、严重、默认配置受影响、最新版本受影响、未认证、低权限、跨租户、RCE、SSRF 内网、有效凭据、批量越权或数据泄露。
- 扫描器、公开 PoC、issue、其他模型/工具、历史报告或运行日志声称“已确认”，但尚未对照官方预期行为。
- finding 涉及管理员功能、插件/脚本/工作流能力、沙箱、URL fetch/webhook、AI 工作流、文件导入导出、secret、组件依赖、默认配置、移动端、客户端或第三方集成。
- 需要判断是否命中 known issue、duplicate、accepted risk、expected behavior、out of scope、hardening only、config only、low priority 或 intelligence only。
- 报告准备写“官方未公开”“官方最新版本仍受影响”“默认安装可利用”“官方缓解被绕过”。

## 输出要求

每次使用至少输出以下裁决，不需要照搬模板，但字段含义必须完整：

```text
Finding:
已读官方材料:
未读 / 不可访问 / 只部分阅读材料:
目标版本与配置边界:
官方安全模型摘要:
官方对象和标识符模型:
命中的官方已知风险 / 预期行为 / accepted risk / 范围规则:
official_known_status:
security_model_status:
新边界 / 去重判断:
target_scope_status:
allowed_claims:
forbidden_claims:
missing_evidence:
下一步补证或降级动作:
```

结构化记录必须落入 notes，而不是只写自然语言段落：

```text
notes/官方文档阅读记录.md:
- source_id:
- url 或 path:
- read_status:
- version_scope:
- checked_at:

notes/官方已知风险基线.md:
- known_risk_id:
- affected_versions:
- fixed_versions:
- submission_effect:
- new_boundary_required:
```

`official_known_status` 映射规则：

- advisory-covered、官方修复覆盖、官方公告覆盖：写 `official_known`。
- duplicate：写 `duplicate`。
- known-limitation、accepted risk、expected behavior、官方安全模型内预期能力：写 `accepted_risk`；如更接近公告覆盖，可写 `official_known`。
- 资料不完整、真实目标版本 unknown、去重未完成：写 `unknown` 或 `needs_manual_dedup`。
- `unknown` / `needs_manual_dedup` 不能推出 `not_official_known`、`finding_submit_ready=true` 或 `bounty_submit_ready`。

finding 若要写 `not_official_known`，必须回链结构化 `source_id` / `known_risk_id`；“未观察到公开匹配”只能作线索。

如果官方资料未读完、版本未对齐、scope 未确认、安全模型 unknown、或去重未完成，不得输出 `not_official_known`、`latest_affected`、`default_affected`、对外提交资格、`official_unpublished` 等强结论。

## 核心原则

### 1. 未读完不等于未公开

以下情况都不能写“官方未公开”或 `not_official_known`：

- 只读 README、首页、安装片段、搜索摘要或第三方转载。
- 只搜漏洞类型关键词，没有读安全策略、范围、权限模型、配置文档、release notes、known issues、advisory 和官方 issue/discussion。
- 官方文档站、登录后 scope、历史公告或仓库安全策略不可访问，但没有记录原因。
- 目标版本、commit、镜像 digest、运行版本、插件、feature flag 或默认配置不明确。
- 只读源码，不知道运行态是否加载同一版本、同一配置、同一插件。
- 发现与已有 issue、公告、release note、accepted risk 或维护者说明相似，但未逐项去重。

正确状态应是：

```text
official_known_unknown
security_model_unknown
scope_unknown
needs_manual_dedup
candidate
blocked
```

### 2. 官方资料必须区分层级

优先使用官方来源；非官方资料只能作为线索。

| 层级 | 资料 | 用途 | 限制 |
|---|---|---|---|
| 官方安全策略 | SECURITY、安全计划、披露规则、安全公告 | 支持版本、范围、accepted risk、提交限制 | 只约束其声明的版本和资产 |
| 官方产品文档 | README、部署、配置、管理员手册、API、权限模型 | 默认配置、角色、对象、信任主体、预期功能 | 文档版本要和目标版本对齐 |
| 官方变更资料 | release notes、changelog、migration guide、compare diff、官方 advisory | 修复边界、默认值变化、历史已知风险 | 不能仅凭标题下结论 |
| 官方维护者说明 | issue、discussion、PR review、FAQ、known limitations | 设计意图、重复问题、不会修复、accepted risk | 需要确认维护者身份和适用范围 |
| 官方产物资料 | registry、镜像 digest、签名、SBOM、包元数据、示例配置 | 运行版本、默认部署、组件加载 | tag 不等于 digest，示例不等于默认 |
| 非官方线索 | CVE 库、漏洞库、博客、PoC、扫描器、社交媒体、其他模型/工具 | 提醒去核查 | 不能替代官方门禁 |

如果唯一证据来自非官方资料，只能写：

```text
official_material_status: missing_or_unread
security_model_status: security_model_unknown
新边界 / 去重判断: unknown
forbidden_claims:
- 不得声明官方未公开。
- 不得声明官方已确认。
- 不得声明 accepted risk / expected behavior，除非补到官方材料。
```

### 3. 官方已知不等于没有价值，但默认不能当新漏洞

技术现象命中官方已知、accepted risk、expected behavior、known limitation、duplicate 或范围排除时，默认不得写成新漏洞主张。

只有证明至少一个新边界，才允许继续作为候选：

- 新主体：官方只描述管理员、owner、插件作者或部署者能力，当前证明普通用户、低权限或未认证可触发。
- 新入口：官方已知覆盖一个入口，当前是另一条默认可达入口、异步入口、导入导出入口、API、worker 或插件路径。
- 新对象：官方只覆盖自有对象，当前证明他人对象、跨工作区、跨组织、跨租户、跨项目或跨隔离边界。
- 新版本：官方只覆盖旧版本，当前证明最新支持版本、当前运行 digest 或回归版本仍受影响。
- 新默认配置：官方描述非默认、debug、示例或弱配置，当前证明全新默认安装仍受影响。
- 新影响：官方只承认 callback、错误、低影响或加固建议，当前证明可读、可写、可执行、可越权、可获得有效 secret 或可跨边界。
- 新缓解绕过：官方推荐或补丁防护在同变量、同路径、同上下文被绕过。

没有新边界时，应写成：

```text
官方已知排除（外部裁决）
expected_behavior
accepted_risk
out_of_scope
hardening_only
config_only_risk
needs_new_boundary
```

### 4. 官方安全模型是漏洞四则条件的一部分

官方门禁必须回答 Security Model / Intended Behavior：目标承诺保护什么，信任谁，哪些危险能力是正常功能，哪些边界不承诺保护。

至少提取：

- 角色模型：匿名、访客、普通用户、成员、owner、管理员、租户管理员、服务账号、插件作者、脚本作者、部署者、系统任务。
- 对象模型：用户、组织、租户、workspace、项目、文件、知识库、任务、workflow、插件、secret、token、webhook、分享链接、object key、物理表。
- 权限模型：role、scope、action、ACL、RBAC、ABAC、API token scope、服务端对象级授权要求。
- 执行模型：管理员工具、插件执行、脚本执行、沙箱内命令、模板渲染、工作流工具、导入导出、调试能力是否为预期功能。
- 网络模型：URL fetch、webhook、callback、代理、重定向、内网、metadata、egress、防 SSRF 边界。
- 数据模型：哪些数据公开、私有、租户隔离、仅 owner 可见、日志可见、secret 脱敏、测试数据与真实数据边界。
- 默认配置：危险功能是否默认开启，示例配置与生产配置是否不同，安全开关默认值是什么。
- 不承诺边界：内容安全、prompt-only、管理员自害、插件作者自害、弱配置、第三方系统、低影响 header、无影响 DoS、合规线索。

安全模型 unknown 时，最多写 candidate / blocked / security_model_unknown，不得写强漏洞声明。

### 5. 官方门禁约束 source / sink / trace / transform 的解释

官方门禁不替代技术证据，但会改变证据解释：

- Source：官方模型说明哪些入口、角色、token、插件、webhook、CLI、管理后台、测试接口属于不可信主体或范围内主体。若攻击者条件与官方信任模型冲突，不能写未认证或低权限。
- Sink：官方模型说明哪些敏感操作是管理员正常能力、插件作者能力、沙箱内功能、调试功能或部署者责任。若 sink 是预期功能，必须降级为 expected behavior 或 hardening only，除非证明新边界。
- Trace：官方文档说明 route 是否默认注册、是否需要 feature flag、license、enterprise/cloud、debug/local、插件启用或管理员预配置。trace 闭合但不在默认边界内时，必须写 server condition。
- Transform：官方文档说明默认参数化、escape、allowlist、sandbox、RBAC、egress、CSRF、secret rotation 是否启用。文档说有防护不等于运行态有效，源码有防护也不等于同上下文有效。

检验句：**如果官方把当前主体视为受信任主体，或把当前 sink 视为正常功能，我是否证明了低权限、跨主体、跨对象、跨租户、跨沙箱、跨网络、跨默认配置或防护绕过？**

## 官方资料阅读状态

每份资料必须标注阅读状态和结论限制。

| 状态 | 含义 | 允许结论 | 禁止结论 |
|---|---|---|---|
| `full` | 与 finding 相关的范围、版本、安全模型、限制和 known risk 已完整读完 | 可用于门禁裁决 | 不能超出该资料版本和范围 |
| `partial` | 只读了部分章节或资料过大未读完 | 只能限定引用已读部分 | 不得写官方未公开、官方未说明 |
| `unavailable` | 登录受限、网络失败、页面失效或权限不足 | 记录阻塞和替代线索 | 不得当作不存在 |
| `not_found` | 在明确官方位置未找到该类资料 | 可写“未找到该资料” | 不得写“目标没有该安全模型” |
| `conflicting` | 官方资料之间冲突 | 进入人工去重 | 不得任选有利一条 |

建议记录：

```text
[DOC-READ-STATE]
source_id:
title:
official_or_not: official / official-mirror / third-party / unknown
source_type: SECURITY / docs / api / config / release / advisory / issue / scope / artifact / other
version_scope:
read_status: full / partial / unavailable / not_found / conflicting
security_topics:
usable_for_claims:
claim_limit:
```

## 版本、配置和运行态对齐

官方门禁必须防止把不同层级混为一谈。

必须分清：

- 官方最新版本。
- 官方支持版本。
- 修复版本。
- 源码 tag / commit。
- 依赖 lock / SBOM / package 版本。
- 镜像 tag 与 manifest digest。
- 运行态版本、加载路径、插件、worker、feature flag、配置。
- 文档版本和产品版本。

禁止：

- 把 `latest` tag 当固定版本。
- 把搜索摘要当官方最新版本。
- 把源码已修当运行已修。
- 把 release note 的 security 字样当漏洞证据。
- 把当前实验环境配置当默认配置。
- 把旧文档直接约束新版本，或把新文档直接洗掉旧版本风险。

进入强声明前必须能回答：

```text
official_latest_version:
current_source_version:
artifact_tag_or_digest:
runtime_version:
doc_version_scope:
default_config_basis:
version_checked_at:
version_drift_risk:
```

版本或配置 unknown 时，使用 `version_identity_unknown`、`default_config_unknown`、`blocked`，不得写 latest/default 影响。

## 已知风险基线

不要只复制文档标题。要把官方资料转成可对照的 known risk 条目。

```yaml
known_risk:
  id: OKR-001
  source_id: DOC-001
  type: known_vuln | known_limitation | expected_behavior | accepted_risk | out_of_scope | config_risk | hardening_only | auth_model | sandbox_model | plugin_model | network_model | report_rule
  affected_versions: ""
  affected_config: default | non-default | debug | sample | admin-enabled | unknown
  attacker_condition: ""
  server_condition: ""
  protected_boundary: ""
  expected_behavior_statement: ""
  official_mitigation: ""
  submission_effect: exclude | downgrade | needs_new_boundary | no_effect | unknown
  new_boundary_required:
    - new_subject
    - new_entry
    - new_object
    - new_version
    - new_default_config
    - higher_impact
    - mitigation_bypass
  forbidden_claims:
    - "不得声明官方未公开，除非证明当前边界不在 OKR-001 覆盖范围内。"
  summary: "用自己的话摘要，不长段复制。"
```

## 与当前 finding 对照

不要只按漏洞类型去重。相似风险必须逐项比较：

| 维度 | 必问问题 | 裁决示例 |
|---|---|---|
| 入口 | 是否同一 API、页面、任务、插件、导入路径、webhook、URL fetch、worker | same_entry / new_entry / unknown |
| 主体 | 是否同一权限和信任前提 | trusted_admin / low_priv_new_boundary |
| 对象 | 是否同一对象归属、同租户、跨租户、跨组织、跨项目 | same_object / new_object_boundary |
| 标识符 | 所需 ID 是否攻击者可获得，是否支持批量或持续获得 | attacker_obtainable / known_id_only / unknown |
| 配置 | 默认、示例、debug、弱配置、管理员启用 | default_affected / non_default_only |
| 版本 | 是否旧版本、修复版本、当前运行版本、最新支持版本 | fixed / regression / runtime_unknown |
| 防护 | 官方缓解是否同上下文有效 | effective / bypassed / unknown |
| 影响 | 是否同一 CIA 层级 | same_impact / higher_impact |
| 范围 | 是否 in scope、out of scope、accepted risk、duplicate | in_scope / excluded / dedup_needed |

去重不确定时写 `needs_manual_dedup`，不得写 `likely_new`。

## 标识符获取和账号对象矩阵

官方对象模型必须落到可复核的 ID 获取链。尤其是 IDOR、BOLA、BFLA、未授权、分享资源越权、对象存储越权、批量导出、跨租户或“已知对象即可利用”。

必须回答：

- 必需标识符是什么：user_id、tenant_id、workspace_id、project_id、file_id、document_id、workflow_id、plugin_id、share token、lookup handle、URI、object key、physical table 等。
- 官方入口是否暴露这些标识符：列表、详情、搜索、导出、日志、关系链、成员/收件人/组织选择器、分享页、客户端状态、历史请求、分页、批量接口。
- 攻击者能否在最低权限下获得：yes / no / unknown。
- 可获得规模是什么：single、multiple、bulk、continuous、enumerable、searchable、exportable、inferable、not-obtainable、unknown。
- 官方是否要求每次对象访问做服务端对象级授权，还是只依赖 UI 隐藏、不可预测 ID、列表过滤或前端路由。

记录格式：

```text
[OFFICIAL-IDENTIFIER-MODEL]
required_identifiers:
official_exposure_paths:
attacker_obtainable: yes / no / unknown
obtainable_scale: single / multiple / bulk / continuous / enumerable / searchable / exportable / inferable / not-obtainable / unknown
official_authorization_requirement: per-object server auth / list-only filtering / ui-hidden / unpredictable-id / unknown
claim_limit:
```

多主体或对象边界 claim 必须引用账号对象矩阵，记录主体、角色、对象归属、租户/workspace、token/cookie 隔离和清理责任；账号对象矩阵字段以 `templates/账号对象矩阵模板.md` 与对应 schema/template 为准，本 Skill 不重新定义。

```text
[OFFICIAL-ACCOUNT-OBJECT-MATRIX]
attacker_role:
owner_role:
victim_role:
control_role:
cleanup_role:
tenant_workspace_boundary:
object_ownership_rule:
token_cookie_isolation_required: yes / no / unknown
public_report_sensitive_boundary:
internal_replay_fields:
```

门禁规则：

- 只有 known-ID-only、tool-sample-only、admin-sample-only、screenshot-sample-only，不得写高价值 confirmed、批量、任意对象、所有用户或所有租户。
- 官方只通过 owner 列表暴露对象时，claim 只能限于 owner 可见对象，除非动态验证证明跨主体可获得。
- 官方入口支持批量、分页、搜索、导出、关系链或分享页暴露大量标识符时，可以继续补运行态规模证明，但仍不能跳过对象级授权验证。
- 缺账号对象矩阵时，不得写跨主体、跨租户、owner/victim 或清理闭环 confirmed。

检验句：**删掉复核人手工提供的 ID 后，攻击者还能从官方可达入口拿到该 ID 吗？如果报告写批量，攻击者能稳定获得足够多 ID 吗？**

## 官方缓解和文档运行态不一致

官方资料说“已修复”“默认安全”“有 allowlist”“启用沙箱”“阻断内网”“服务端授权”时，必须回到运行态验证同变量、同路径、同上下文是否有效。

| 裁决 | 含义 | 后续动作 |
|---|---|---|
| `official_mitigation_effective` | 官方防护在当前版本、当前配置、同变量、同路径、同上下文经负控证明有效 | rejected 或降级 |
| `official_mitigation_unknown` | 文档有防护说明，但运行态未验证 | blocked |
| `official_mitigation_bypassed` | 强验证证明绕过官方防护 | 可作为新边界候选 |
| `doc_claim_runtime_mismatch` | 文档声称安全，但默认运行态不安全 | 记录默认配置或文档修复建议 |
| `config_dependent` | 安全依赖配置 | 限定 server condition，不外推默认影响 |

检验句：**官方说有防护时，我是否证明了当前版本、当前配置、当前入口、当前变量真的使用了它？官方说风险已知时，我是否证明当前 finding 多了新边界？**

## 动态验证触发条件

官方门禁本身是文档和安全模型裁决，但以下情况必须回到运行态补证，不能只靠文档推断：

- 官方文档声称有防护，但代码、diff、配置或运行态疑似绕过。
- 官方说明默认安全，但当前环境疑似全新默认安装不安全。
- 官方说明某漏洞已修复，但当前版本、digest、入口或配置疑似仍可触发。
- 官方把某能力定义为管理员、插件作者、脚本作者、部署者或沙箱内能力，但 finding 声称普通用户、低权限、未认证或跨主体可触发。
- 官方只承认 callback、URL fetch、预览、导入导出或调试能力，但 finding 声称内部响应可读、metadata、状态改变、文件越界、secret 或执行边界破坏。
- finding 依赖对象 ID、分享 token、resource URI、object key 或 physical table，但官方模型对 ID 暴露和对象级授权不清楚。
- finding 准备写批量、全量、所有用户、所有租户、任意对象、RCE、SSRF 内网、有效凭据、默认配置或最新版本受影响。

无法动态验证时不得脑补，应写：

```text
停止原因:
- 缺测试账号 / 测试对象 / 双租户 / 日志 / OOB / 快照 / 清理能力。
- 继续会触碰真实用户数据、真实凭据、第三方系统或范围外资产。
- 官方资料不可访问，无法确认 scope 或安全模型。
当前状态: candidate / blocked / scope_unknown / security_model_unknown
```

## 授权实验模式下的强验证解释

官方门禁不得削弱授权实验环境中的强验证。在自有、授权、隔离、可重置、可清理环境内，应该追当前范围内最高可证明影响；官方门禁只限制最终声明不超过安全模型和证据。

强验证前要记录：

```text
环境类型:
版本 / digest / 配置:
测试主体:
测试对象:
观察点:
快照与清理:
要证明或推翻的官方安全模型声明:
```

强验证解释时必须问：

- 当前主体是否官方受信任主体？如果是，是否证明了跨主体或低权限边界。
- 当前 sink 是否官方预期功能？如果是，是否证明了逃逸、越权、跨租户、敏感数据、防护绕过或默认配置风险。
- 当前环境是否官方默认配置？如果不是，声明必须限定配置。
- 当前影响是否属于官方排除项？如果是，只能降级或内部记录，除非证明新边界。
- 当前验证是否触碰范围外服务、真实用户数据、真实凭据或第三方系统？如果是，停止并裁剪证据。

## 范围隔离与无关服务边界

官方门禁必须服务于当前目标，不允许把无关系统当跳板、证据或二阶段目标。

规则：

- 只解释当前授权目标、当前授权任务、当前服务、当前容器、当前账号和当前对象。
- 不因为追 RCE、SSRF、文件读写、管理面或内网影响，就主动碰无关服务。
- 若宿主机文件、宿主机 canary、测试内网 canary 或受控 mock 明确属于当前授权验证范围，可以作为证据；但不得访问、登录、重启、探测、利用其他无关服务来补证。
- 发现无关服务时，只记录“范围外对象，未触碰，未作为证据”，不得把它写入漏洞链路。
- 报告结论只基于当前目标内的证据，不把旁路环境、旧会话、其他项目或宿主机无关服务混入。

## 方法性状态边界

### `technical_confirmed`

同时满足以下条件，官方门禁才不阻止技术确认：

- 官方资料阅读状态足以支撑当前声明，未读资料不会改变核心结论或已明确进入声明限制。
- scope、版本、运行态、默认配置、插件/feature flag 与声明一致。
- 官方安全模型明确当前行为违反受保护边界，而不是预期功能、受信任主体能力、范围外、accepted risk、hardening only 或 duplicate。
- 已知风险基线没有覆盖当前边界，或已证明新主体、新入口、新对象、新版本、新默认配置、更高影响或缓解绕过。
- Source→Sink、强正控、负控、清理和 Allowed Claims 已由相邻门禁闭合。
- 依赖对象标识符或多主体时，官方对象模型、标识符获取链、账号对象矩阵和可获得规模不阻塞声明。

### `candidate`

适用于：

- 静态链路可疑，但官方安全模型、scope、known issue、默认配置或去重未完成。
- 官方未找到明确说明，但资料阅读不完整或版本对齐不足。
- 已知风险相似，可能有新边界但还未证明。
- 只有 known-ID-only、单对象样本、弱正控、callback-only、marker-only、error-only、version-only 或 scanner-only。

### `blocked`

适用于：

- 需要运行态确认版本、digest、feature flag、插件、worker、默认配置或构建产物。
- 需要双账号、双对象、双租户、日志、OOB、浏览器、数据库、文件、队列或清理能力。
- 需要验证官方缓解是否有效或被绕过。
- 需要证明攻击者能否从官方入口获得必要标识符和可获得规模。

### `rejected`

只有明确否定证据才写 rejected：

- 官方明确排除该资产、版本、模块、漏洞类型或测试方式，且没有新边界。
- 官方安全模型明确这是受信任主体正常能力、expected behavior、accepted risk、hardening only、known limitation 或 duplicate，且没有新主体、新入口、新对象、新版本、新默认配置、更高影响或缓解绕过。
- 官方对象模型和运行态证明攻击者无法获得必要标识符，且没有其他可达触发路径。
- 运行态负控证明官方缓解在同变量、同路径、同上下文有效。
- 当前版本未加载、入口不可达、source 不可控、sink 不执行或 trace 被证伪。

rejected 必须保留证据和 forbidden claims，不能只写“误报”。

## Allowed / Forbidden / Missing

每次官方门禁必须输出声明边界。

### 方法性 Allowed Claims 边界

只允许写证据已经支持的最窄声明，例如：

- 在某版本、某配置、某角色、某入口、某对象范围内，当前行为违反官方承诺的某安全边界。
- 当前 finding 相比官方已知风险新增了某主体、入口、对象、版本、默认配置、影响层级或缓解绕过。
- 官方文档未覆盖当前已证明边界，但仅限已读资料和已验证版本。
- 当前只能作为 candidate / blocked / hardening / intelligence only。

### 方法性 Forbidden Claims 边界

缺少对应证据时必须禁止：

- 官方未公开。
- 官方最新版本受影响。
- 默认配置受影响。
- 未认证或低权限可利用。
- 所有部署、所有用户、所有租户、任意对象、批量影响。
- RCE、宿主机接管、沙箱逃逸、内网敏感读取、真实数据泄露、有效凭据泄露。
- 已修复、无回归、不是 duplicate、对外可提交、高危或严重。
- 受信任主体正常能力被写成越权漏洞。

### 方法性 Missing Evidence 边界

常见缺口：

- 官方 SECURITY、scope、权限模型、默认配置、known issues、release notes、advisory、官方 issue/discussion 未读或不可访问。
- 版本、digest、运行态、插件、feature flag、默认配置未确认。
- known risk baseline 未建立或未逐项去重。
- 官方对象模型、标识符获取链、账号对象矩阵缺失。
- 官方缓解未做同上下文运行态验证。
- 强正控、负控、清理或最高危害追踪缺失。

## 报告阶段引用边界

本 Skill 不内嵌报告模板，也不生成提交资格状态。官方资料复核结果只写入 evidence、声明边界和外部门禁引用：

- 官方资料、版本、scope、默认配置、known issue、expected behavior、accepted risk、范围或官方已知拒绝（外部裁决）必须有证据引用。
- Allowed Claims / Forbidden Claims / Missing Evidence 只表达声明边界，不复制报告章节正文。
- 报告阶段只能按唯一模板渲染已被 evidence 授权的官方资料结论，不能在报告阶段补造官方门禁证据。
- 提交资格由 `evidence/赏金资格.json` 与报告与复核类提交门禁裁决，本 Skill 只提示需要外部门禁。

## 修复建议边界

官方门禁会改变修复建议类型：

- 违反官方安全模型且技术 confirmed：写代码级、配置级、默认值、权限、对象级授权、防护绕过、回归测试修复。
- 官方缓解被绕过：修复建议直指绕过点，不泛泛写“加强校验”。
- expected behavior / trusted admin / sandbox expected：不要要求删除正常功能；建议补文档、警告、审计日志、最小权限、二次确认、默认关闭或显式 opt-in。
- accepted risk / out of scope / hardening only：写加固、文档、规则降噪或内部风险登记，不写新漏洞修复结论。
- security_model_unknown / scope_unknown / blocked：优先补官方资料、运行态、去重、账号对象矩阵和默认配置证据，避免基于 unknown 做大规模修复。

## 禁止事项

- 禁止把“没搜到官方资料”写成“官方未公开”。
- 禁止用第三方博客、漏洞库、扫描器、公开 PoC、社交媒体或外部模型/工具自述替代官方资料。
- 禁止只凭 release note、issue 标题、commit message 或 advisory 摘要下结论。
- 禁止把官方已知、accepted risk、expected behavior、out of scope、hardening only、duplicate 包装成新漏洞，除非证明新边界。
- 禁止把管理员、插件作者、脚本作者、部署者、服务账号或沙箱内预期能力写成未认证或低权限漏洞。
- 禁止官方安全模型、scope、默认配置、known issue、expected behavior、accepted risk 或 duplicate 仍 unknown 时写对外可提交、高危默认影响、官方未公开。
- 禁止把 known-ID-only、tool-ID-only、admin-sample-only、screenshot-ID-only 写成批量、任意对象、所有用户或所有租户。
- 禁止把 callback-only、marker-only、error-only、reflect-only、status-only、regex-only、version-only 写成 confirmed。
- 禁止因为官方门禁而停止授权实验环境中的强验证；门禁约束声明，不替代补证。
- 禁止把无关服务、其他项目、旁路环境、真实第三方系统、真实用户数据或真实凭据作为补证对象。
- 禁止把本地绝对路径、私有脚本路径、内部编号、临时会话过程、当前聊天上下文、历史任务细节写进通用 skill 正文。

## 自检清单

### 官方资料

- [ ] 是否列出官方资料 ID、类型、版本范围和阅读状态？
- [ ] 是否区分官方、半官方、非官方线索？
- [ ] `partial`、`unavailable`、`not_found` 是否写了结论限制？
- [ ] 是否读过安全策略、范围、权限模型、默认配置、release notes、known issues、advisory 或说明其缺失？
- [ ] 是否避免把搜索不到等同于未公开？

### 安全模型

- [ ] 是否明确角色、对象、权限、默认配置、信任主体和预期危险功能？
- [ ] 是否判断当前行为违反官方承诺的安全边界，还是正常功能 / 受信任主体能力 / 范围外 / hardening？
- [ ] 安全模型 unknown 时是否降级？

### 已知风险与新边界

- [ ] 是否建立 known risk baseline，而不是只复制标题？
- [ ] 是否逐项比较入口、主体、对象、标识符、配置、版本、影响、防护和范围？
- [ ] 命中官方已知风险时，是否证明新主体、新入口、新对象、新版本、新默认配置、更高影响或缓解绕过？
- [ ] 去重不确定时是否写 `needs_manual_dedup`？

### 版本与默认配置

- [ ] 是否确认 official latest / supported / fixed 与当前 runtime 不是混用？
- [ ] 是否把 tag 解析到 digest 或运行态版本？
- [ ] 是否有官方默认配置依据或全新安装证据？
- [ ] 版本和配置事实是否记录 checked_at 并考虑漂移？

### 标识符与多主体

- [ ] 依赖 ID / token / URI / object key 时，是否证明攻击者获得路径和可获得规模？
- [ ] 是否避免 known-ID-only 外推为批量、任意对象或高价值 confirmed？
- [ ] 多主体、跨对象、跨租户或清理 claim 是否有账号对象矩阵和 token/cookie 隔离？

### 动态验证与声明边界

- [ ] 官方防护是否在同变量、同路径、同上下文运行态验证？
- [ ] 强正控和负控是否受官方模型解释约束？
- [ ] 是否没有触碰无关服务、第三方真实资源、真实用户数据或真实凭据？
- [ ] 是否输出 Allowed Claims、Forbidden Claims、Missing Evidence？

检验句：**如果删除扫描器等级、外部模型/工具结论、第三方文章、旧会话、本地路径和手工样本，只保留官方安全模型、当前版本运行态、Source→Sink、强正控、负控、清理和声明边界，当前 claim 还能成立吗？如果不能，必须降级或补证。**
