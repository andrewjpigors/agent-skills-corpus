---
name: gen-spec-code-framework
description: "Use when initializing, repairing, upgrading, or backfilling a Spec Coding .ai/ framework in a repository. Strict initializer-only workflow that creates the P0/P1 contracts, runtime skeleton, and .github/skills/spec-code/SKILL.md for later role-based execution."
---

# Spec Coding Framework Initializer

本技能用于把目标仓库初始化、补齐或升级为符合 Spec Coding 规范的框架仓库。它只生成框架资产，不代替后续角色执行需求分析、系统设计、原型设计、Coding、Reviewing、Testing、Fixing 或部署验收。

## 1. Authority

- 本技能是 Spec Coding 框架初始化的唯一权威来源；所有 canonical 规范（§5.4.1 00_index 生成骨架、§5.7.2 运行时技能体）已完整内嵌，不依赖任何外部规范文档。
- `.github/skills/spec-code/SKILL.md` 是运行时执行技能；本文件是初始化器，二者职责不可混用。
- 本版初始化器遵循 **task-card-only context**：初始化结果不得生成或要求旧版第二套上下文资产。

## 2. Hard Rules

- 框架契约、规则、模板与运行时技能只允许落在 `.ai/` 与 `.github/skills/spec-code/`；业务规格骨架只允许落在 `doc/spec/` 与 `doc/spec/tasks/`；禁止再生成 `spec_coding/` 目录变体或其他平行根目录。
- 必须直接写文件到工作区；不要把完整文件正文长篇打印在对话里代替落盘。
- 严禁伪造运行时实例。初始化阶段唯一允许预置的运行时骨架是：
  - 空目录：`.ai/checkpoints/`、`.ai/artifacts/logs/`、`.ai/artifacts/reports/`、`.ai/fix_task/`
- 严禁伪造角色运行产物：`doc/spec/prd.md`、模块设计文档、真实任务卡、Evidence Manifest、Command Receipt、Checkpoint、测试报告、Review 报告都不属于初始化阶段产物。
- `.ai/00_index.md` 必须使用真实项目元信息，不得保留示例值，不得把 `{{PROJECT_*}}` 一类占位符留在实际契约文件中。
- 初始化器必须在本技能内部携带 `.ai/00_index.md` 的完整生成骨架（见 §5.4.1）；目标运行时仓库必须完全自包含，不得依赖任何外部规范文档才能生成、理解或执行 `.ai/00_index.md`。
- 初始化器必须在本技能内部携带 `.github/skills/spec-code/SKILL.md` 的完整落盘规范体（见 §5.7.2）；生成运行时技能时不得依赖任何外部规范文档，必须从本技能内嵌规范体原样落盘。
- 若初始化阶段尚未获得人工确认的模块清单，`.ai/00_index.md` 必须写入“待登记”默认模块行，不得保留 `{{module}}` 类占位符，也不得伪造模块实例。
- `.ai/templates/` 内允许保留占位符；模板以外的契约、规则与运行时技能必须是可直接使用的真实内容。
- `.ai/harness.yaml` 必须填入推断或用户确认后的真实命令；若只能落到保底占位命令，必须在最终报告中明确标记“框架已初始化，但尚未 execution-ready”。
- 若 `.ai/` 或 `.github/skills/spec-code/` 已存在，必须先获得且只获得一次明确决策：`覆盖全部`、`仅补充缺失` 或 `取消操作`。
- 初始化器不得生成 `.ai/context/**`、`current.yaml`、`temp_context_pack.md`、`temp_context_slice.md`、`temp_delta_context.md` 这类已废弃资产。
- 在 9 项项目元信息收集完整前，不得进入覆盖决策、命令推断、合同生成、骨架创建、模板生成、规则生成或任何写盘初始化动作；缺项时必须继续追问，直到完整为止。
- 9 项项目元信息必须由人类明确输入；AI 不得根据仓库结构、依赖清单、README、代码、目录名、历史文件或任何仓库信号自行猜测、补全、代填或默认推断这些元信息。

## 3. Required Inputs

写任何框架文件前，必须先一次性收集以下 9 项项目元信息：

1. 项目名称
2. 项目代号
3. 项目背景
4. 后端技术栈
5. 前端技术栈
6. 数据库
7. 缓存
8. 部署方式
9. CI/CD 类型

### 3.1 Metadata Completion Gate

- 这 9 项是初始化硬门禁，不是建议项；缺任意 1 项都不得继续初始化。
- 这 9 项的唯一合法来源是人类明确输入；仓库扫描结果、代码线索、README 描述、依赖声明或历史文件都不能替代人类输入。
- 初始化器必须逐项校验：缺失、空值、模糊表述、无法唯一解析的回答，都视为“未完成输入”。
- 若存在缺项，必须以单批问题只追问当前缺失项；收到回复后再次逐项校验。
- 若补充后仍有缺项或表述仍不明确，必须继续追问；不得因为已经问过一次就继续初始化。
- 重复询问必须持续到 9 项全部完整、明确、可用于生成真实契约内容后，才能进入覆盖决策、命令推断与写盘阶段。
- 不得使用默认值、猜测值、示例值或 `{{PLACEHOLDER}}` 代替缺失的项目元信息。
- 若仓库扫描结果与人类输入不一致，AI 不得以扫描结果覆盖项目元信息；必须暂停并把冲突点提交给人类确认，以人类明确答复为唯一权威值。

## 4. Strict Initialization Targets

默认目标是：`Strict P0 + 与仓库相关的 P1 + 条件性 UI 资产`。

### 4.1 Minimum Bootstrap

仅当用户明确要求最小版时，才允许以这 8 项作为完成态：

1. `.ai/00_index.md`
2. `.ai/01_status.md`
3. `.ai/02_TransitionLog.md`
4. `.ai/harness.yaml`
5. `.ai/templates/temp_task_card.md`
6. `.ai/rules/review_rule.md`
7. `.ai/rules/context_rule.md`
8. `.github/skills/spec-code/SKILL.md`

> **门禁警告**：此 8 项仅支持框架启动，**不足以让任务卡进入 `Coding/Fixing`**。首张任务卡进入 `Coding` 或重发 `Fixing` 任务卡前，还必须补齐以下 5 项，否则 `pre_execution_checks` 将触发 `Blocked`：
> - `.ai/templates/temp_execution_envelope.yaml`
> - `.ai/templates/temp_command_receipt.yaml`
> - `.ai/templates/temp_evidence_manifest.yaml`
> - `.ai/templates/temp_failure_signature.md`
> - `.ai/rules/harness_rule.md`

### 4.2 Strict P0 Core Contract

严格初始化至少要创建以下 P0 资产：

- `.ai/00_index.md`
- `.ai/01_status.md`
- `.ai/02_TransitionLog.md`
- `.ai/harness.yaml`
- `.ai/templates/temp_task_card.md`
- `.ai/templates/temp_execution_envelope.yaml`
- `.ai/templates/temp_command_receipt.yaml`
- `.ai/templates/temp_evidence_manifest.yaml`
- `.ai/templates/temp_failure_signature.md`
- `.ai/rules/review_rule.md`
- `.ai/rules/harness_rule.md`
- `.ai/rules/context_rule.md`
- `.github/skills/spec-code/SKILL.md`（运行时子技能，必须按 §5.7.2 规范体原样落盘，并通过 §5.7.1 的固定形状校验；生成结果必须是角色执行技能，不得保留初始化器身份，不得改写章节顺序、章节标题、frontmatter 或门禁语义；若任一必需项缺失，初始化器不得宣告完成）

并同时创建运行时空骨架：

- `.ai/checkpoints/`
- `.ai/artifacts/logs/`
- `.ai/artifacts/reports/`
- `.ai/fix_task/`
- `doc/spec/`
- `doc/spec/design/`
- `doc/spec/tasks/`
- `doc/spec/test_case/`
- `doc/spec/prototype/`
- `doc/spec/deploy/`
- `script/`
- `src/`
- `src/common/`
- `src/3rd/`
- `test/`

### 4.3 Delivery Governance Set

若用户要求“严格初始化”或仓库目标是可交付治理，则继续生成：

- `.ai/templates/temp_prd.md`
- `.ai/templates/temp_system_design.md`
- `.ai/templates/temp_module_design.md`
- `.ai/templates/temp_map_task.md`
- `.ai/templates/temp_traceability.md`
- `.ai/templates/temp_review_summary.md`
- `.ai/templates/temp_test_case.md`
- `.ai/templates/temp_deploy.md`
- `.ai/templates/temp_spec_change_record.yaml`
- `.ai/rules/{lang}_rule.md`

### 4.4 Conditional UI Governance

若仓库存在前端/UI 原型需求，或用户明确要求补齐 UI 治理资产，则额外生成：

- `.ai/rules/ui_rule.md`

但初始化阶段仍不得伪造 `doc/spec/prototype/*.html` 原型实例，包括 `style.html` 与 `{module}_ui.html`。

## 5. Execution Workflow

初始化器必须按以下顺序执行；任一步未满足退出条件，禁止进入下一步。

### 5.1 Discovery

必须先做只读发现：

1. 检查 `.ai/`、`.github/skills/spec-code/`、`doc/spec/` 是否已存在。
2. 扫描仓库信号，仅用于命令推断、语言规则推断与人类输入一致性校验；不得把扫描结果当作 9 项项目元信息的来源。
3. 判断当前目标是 `新建`、`补齐缺失`、`修复漂移` 或 `升级版本`。

> `5.1 Discovery` 只允许只读分析；从 `5.2` 开始，所有初始化动作都受 `3.1 Metadata Completion Gate` 约束。元信息未完整前，不得继续后续步骤。

### 5.2 Metadata Intake And Overwrite Decision

1. 先逐项校验 9 项项目元信息是否完整；缺任意 1 项时，必须停止初始化，并以单批问题追问全部缺失项。
2. 若某项项目元信息不是人类明确输入，而只是 AI 基于仓库信号、依赖、文档或代码做出的判断，该项仍视为缺失，必须继续追问。
3. 收到用户补充后，必须重新逐项校验 9 项项目元信息；若仍有缺项、空值、歧义或无法唯一解析的表述，继续追问，不得进入下一步。
4. 若仓库扫描结果与人类输入存在冲突，必须暂停并把冲突项逐条提交给人类确认；确认前不得继续初始化，也不得擅自覆盖人类输入。
5. 只有当 9 项项目元信息全部由人类明确提供、内容完整明确且冲突已消除时，才允许继续覆盖决策与后续初始化。
6. 若检测到现有框架目录，先获得 `覆盖全部`、`仅补充缺失` 或 `取消操作`。
7. 未获得覆盖决策前，不得修改任何已存在的框架合同文件。
8. 若命令推断置信度低（无法确认测试框架、构建工具或语言规则），暂停并以单批问题向用户收集缺失信息；不得用 `{{PLACEHOLDER}}` 占位而不在最终报告中标记 `execution-not-ready`。
9. 若发现 UI 相关资产（`doc/spec/prototype/` 目录、前端框架依赖）但用户未在人类输入的 9 项元信息中说明前端技术栈，暂停并询问是否生成 `.ai/rules/ui_rule.md`；得到明确答复后再继续。
10. 若扫描发现已废弃目录（`.ai/context/`）或已废弃模板（`temp_context_pack.md`、`temp_context_slice.md`、`temp_delta_context.md` 等），在处理前暂停并列出漂移详情，要求用户确认是否执行清理；确认后再执行覆盖或删除。

### 5.3 Command And Rule Inference

生成 `.ai/harness.yaml` 前，必须先推断 setup/build/test/format/lint/task-test 命令以及语言规则。

### 5.4 Contract First

优先生成或修复核心合同文件：

1. `.ai/00_index.md`
2. `.ai/01_status.md`
3. `.ai/02_TransitionLog.md`
4. `.ai/harness.yaml`

要求：

- `00_index.md` 必须按 `5.4.1 Canonical 00_index Shape` 生成，使用真实项目元数据，成为运行时自包含路由入口；生成结果不得引用任何外部规范文档或废弃上下文资产。
- `01_status.md` 必须包含 `RequirementDesign` 初始状态快照与最近状态迁移表。
- `02_TransitionLog.md` 必须是 append-only 历史归档空表头。
- `harness.yaml` 必须体现"任务卡是唯一上下文合同"的执行模型，不得要求任何外部旧版上下文资产，并且必须显式包含 `verify_test_case_doc_present`、`verify_single_focus_contract`、`verify_stage_command_window`、`explicit_confirmation_gates`、`status_writeback_fields`、`confirmation_gate_writeback_fields`、`stage_command_window` 与 `auto_run`；其中 `verify_test_case_doc_present` 必须校验对应测试用例文档存在，且其相关用例被任务卡的 `acceptance_tests` 完整覆盖；`verify_single_focus_contract` 必须校验 `focus_contract.mode=single_focus`、`primary_design_id` 命中 `design_ids`、`primary_acceptance_test` 命中 `acceptance_tests[*].test_id`、全部 `acceptance_tests[*].focus_key` 与 `focus_contract.focus_key` 一致，且 `focus_artifacts` 与 `write_scope.editable_files` 精确一致并属于 `expected_artifacts`；`status_writeback_fields` 必须限定为 `active_run_id`、`task_status`、`source_failure_signature`、`last_evidence_manifest`、`blocked_from_state`、`blocked_reason`、`resume_token`，`confirmation_gate_writeback_fields` 必须限定为 `task_status`、`blocked_from_state`、`blocked_reason`、`resume_token`、`active_run_id`、`last_evidence_manifest`。还必须包含 `workspace.allow_dependency_install: safe_setup_only`，并在 `stage_command_window` 中为 `Software Engineer` / `QA Engineer` 暴露受控的 `setup_command`、`build_command`、`task_test_command`、`project_test_command`；同时包含 `safety_policy`（含 `writable_paths`、`append_only_paths`、`forbidden_paths`、`forbidden_commands`）、`block_conditions`（`max_fix_attempts_per_task`、`repeated_failure_signature`、`flaky_test_threshold`）、`auto_run`（含 `enabled`、`require_spec_freeze`、8 项 `startup_checks`、`queue_policy`、`stop_policy.global_stop_on_env_error_tasks`）、`failure_signature` 算法节（含 `algorithm`、`components`、`trace_normalization`、`format`）、`test_output_schema` 节、`evidence_manifest` 节与 `command_receipt` 节（字段完整规格见本技能 §5.4 各项要求与 §6 验收清单 item 10）；`test` 节必须含 `retry_policy` 与 `isolation: per_test`。生成说明与相关规则还必须明确：若任务卡无法压缩为单卡单焦点、同职责域的小上下文范围，初始化器应要求发卡人拆卡，而不是通过扩大上下文预算放行。

### 5.4.1 Canonical 00_index Shape

初始化器生成 `.ai/00_index.md` 时，必须直接实体化以下 canonical 模板，并完成两类替换：

1. 将 `{{PROJECT_*}}` 字段替换为人类明确提供的 9 项项目元信息。
2. 将命令类占位符替换为推断或经用户确认后的真实命令。

除此之外，不得删改章节顺序、关键表格、`ai_constitution` 锚点、角色字段值或状态约束语义。
本节 canonical 模板正文为自包含权威版本，是生成 `.ai/00_index.md` 的唯一来源。

若初始化阶段尚未获得人工确认的模块清单，必须保留默认“待登记”模块行；不得保留 `{{module}}` 类占位符。

````markdown
# 00_index

> 本文件是整个 Spec Coding 框架的只读路由入口。
> 它提供项目元数据、角色边界、状态机、追踪链、Harness 入口与上下文加载协议。
> 它不是状态日志，不是任务卡，不是测试证据容器。
> 运行时仓库不依赖维护仓库中的额外规范文档；本文件必须自包含可执行路由所需的全局约束。

## 1. 文档定位与执行优先级

1. 路由入口：`.ai/00_index.md`
2. 唯一状态真源：`.ai/01_status.md`
3. 执行合约：`.ai/harness.yaml`
4. 规则补充：`.ai/rules/*.md`
5. `Coding/Fixing` 任务态默认唯一上下文合同：当前任务卡；程序员可声明“无任务卡”进入无卡模式
6. 运行时实例资产：`.ai/checkpoints/`、`.ai/artifacts/logs/`、`.ai/artifacts/reports/`
7. 业务规格资产：`doc/spec/**`

## 2. 项目元数据

| Item | Value |
| --- | --- |
| project_name | `{{PROJECT_NAME}}` |
| project_code | `{{PROJECT_CODE}}` |
| project_background | `{{PROJECT_BACKGROUND}}` |
| backend_stack | `{{BACKEND_STACK}}` |
| frontend_stack | `{{FRONTEND_STACK}}` |
| database | `{{DATABASE}}` |
| cache | `{{CACHE}}` |
| deployment_mode | `{{DEPLOYMENT_MODE}}` |
| cicd_type | `{{CICD_TYPE}}` |
| repository_root | `.` |
| allow_network | `false` |
| allow_dependency_install | `safe_setup_only` |
| config_mutation_policy | `restricted` |
| default_shell | `bash_or_powershell` |
| task_card_only_context | `true` |

## 3. 关键路径与约定目录

| Asset | Path | Notes |
| --- | --- | --- |
| Route entry | `.ai/00_index.md` | 全员只读 |
| Status source | `.ai/01_status.md` | 唯一状态真源 |
| Transition archive | `.ai/02_TransitionLog.md` | 仅追加 |
| Harness contract | `.ai/harness.yaml` | 执行、采证、恢复 |
| Coding cards | `doc/spec/tasks/` | 含 `map_task.md` |
| Fix cards | `.ai/fix_task/` | 仅保留活动修复卡 |
| Checkpoints | `.ai/checkpoints/` | `Execution Envelope` |
| Reports | `.ai/artifacts/reports/` | 测试报告、命令收据、证据清单 |
| Logs | `.ai/artifacts/logs/` | 原始执行日志 |
| Specs | `doc/spec/` | PRD、设计、测试用例、部署 |
| UI prototypes | `doc/spec/prototype/` | `style.html` 参考样式模板与 HTML 高保真原型 |
| Deploy specs | `doc/spec/deploy/` | 模块部署说明 |
| Source root | `src/` | 模块工程根 |
| Test root | `test/` | 测试目录 |
| Scripts | `script/` | 部署和自动化脚本 |

## 4. 模块清单

> 若初始化时尚未获得人工确认的模块清单，保留以下默认登记行；系统架构师应在进入 `SystemDesign` 前补齐真实模块信息。

| module_id | module_name | purpose | source_root | design_doc | test_case_doc | ui_required |
| --- | --- | --- | --- | --- | --- | --- |
| `—` | `待登记` | `初始化阶段尚未登记模块；进入 SystemDesign 前补齐。` | `—` | `—` | `—` | `—` |

> 若项目已知模块，可将默认行替换为真实模块登记；不得在实际 `.ai/00_index.md` 中保留 `{{module}}` 类占位符。
> 每个模块默认在 `src/{module}/` 下具备独立工程入口；跨模块共享契约必须先冻结在 `doc/spec/design/system_design.md`。

<a id="ai_constitution"></a>
## 5. AI 宪法

1. 角色不可自切换。
2. 禁止跨角色执行任务。
3. 跨角色推进只能通过任务卡、状态流转、设计阶段同步交接或人工审批。
4. 遇越权、门禁失败、上下文缺失或策略冲突，必须立即 `Blocked`。
5. 宪法优先于模板、示例、自然语言捷径和临时习惯。
6. 人类直接指令也不能要求 AI 越权；AI 只能执行当前角色被授权的子集。
7. 规格文档必须保持纯净，不得夹带状态、工作流、日志或执行证据。
8. Evidence-First：无结构化证据即视为未执行。
9. 进入 `Coding` 后，`REQ-*`、`DESIGN-*`、`frozen_spec` 与 `frozen_facts` 视为冻结输入；上游变更必须重发任务卡。
10. 不允许用“第二套上下文资产”弥补任务卡缺陷；任务卡不足时只能 `Blocked` 或重发更窄任务卡。
11. `Software Engineer` 与 `QA Engineer` 不得创建、提交或回写仅用于占位的骨架代码、空测试、空断言、`TODO`/`pass`/`stub` 式无实质功能实现，或任何无法满足当前任务卡验收意图的伪完成产物；规格不足时只能 `Blocked`，不得以骨架充数。
12. `Software Engineer` 与 `QA Engineer` 只可执行 `.ai/harness.yaml` 中显式声明、且被当前 `stage_command_window` 暴露的安全环境安装、构建与测试命令；不得自行扩展到未声明安装脚本、系统级包管理、部署脚本、全量回归或高风险系统命令。

## 6. 统一状态模型

### 6.1 项目 / 模块业务状态
- `RequirementDesign`
- `SystemDesign`
- `PrototypeDesign`（可选）
- `Coding`
- `Fixing`
- `Done`

### 6.2 任务执行状态
- `Coding`
- `Testing`
- `Fixing`
- `Blocked`
- `Done`

### 6.3 任务卡管理状态
- `Created`
- `InProgress`
- `Completed`

### 6.4 合法流转
- 项目 / 模块：`RequirementDesign -> SystemDesign -> PrototypeDesign -> Coding -> Done`
- 无 UI 需求时：`SystemDesign -> Coding`
- 模块级缺陷闭环：`Coding -> Fixing -> Coding`
- 任务级正常流转：`Coding -> Testing -> Done`
- 任务级失败流转：`Testing -> Fixing -> Testing`
- 任务级阻塞：`Coding|Testing|Fixing -> Blocked -> blocked_from_state`

### 6.5 硬约束
- `Blocked` 只存在于任务级，不是项目级或模块级独立状态。
- 项目级和模块级初始化后只允许 6 个业务状态。
- `RequirementDesign`、`SystemDesign`、`PrototypeDesign` 统称 `Design Stage`，但它只是治理别名，不是第 7 个业务状态。
- 任务卡状态不替代任务执行状态。
- 任何角色不得跳过 `Testing` 让任务从 `Fixing` 直接进入 `Done`。
- 阻塞解除后只能回到 `blocked_from_state`，不得跳转到任意下游状态。

## 7. 阶段绑定写边界

> 下表同时覆盖模块级业务阶段与任务级执行阶段；凡未列明的业务资产写入一律视为越界。

| Stage | Primary Role | Allowed Business Writes | Explicitly Forbidden |
| --- | --- | --- | --- |
| `RequirementDesign` | `Product Manager` | 需求文档与 `.ai/01_status.md` | 系统设计、原型、代码、测试、框架文件 |
| `SystemDesign` | `System Architect` | `doc/spec/design/system_design.md`、`doc/spec/design/{module}_design.md`、`doc/spec/test_case/{module}_test_case.md` 与 `.ai/01_status.md` | 需求文档、原型、代码、测试、框架文件 |
| `PrototypeDesign` | `UI/UX Designer` | `doc/spec/prototype/style.html`、`doc/spec/prototype/{module}_ui.html`、静态导出图、`.ai/01_status.md`；若 `style.html` 缺失，先生成默认草案并停机等待人为确认 | 需求、系统设计、代码、测试、框架文件 |
| `Coding` | `Software Engineer` | 当前任务卡 `write_scope` 白名单内代码 / 测试、必要 checkpoint、`.ai/01_status.md` | 需求、设计、原型、框架文件、无关代码 |
| `Testing` | `QA Engineer` | `test/`、`.ai/artifacts/reports/`、`.ai/artifacts/logs/`、`.ai/fix_task/**`（仅失败回路）、`.ai/01_status.md` | 业务实现、需求/设计/原型、框架文件 |
| `Fixing` | `Software Engineer` | 同一 `task_id + failure_signature` 关联的白名单代码 / 测试、活动修复卡执行字段、checkpoint、`.ai/01_status.md` | 顺手扩散修复、需求/设计/原型/框架文件 |
| `Done` | none | 仅归档类写入 | 任何业务资产新增或修改 |

> 注：`QA Engineer` 负责测试用例文档与测试用例代码；在 `SystemDesign` 阶段可协同编写 `doc/spec/test_case/{module}_test_case.md`；在 `Testing` 失败回路中可写 `.ai/fix_task/**` 并签发 `Fixing` 任务卡。

> `RequirementDesign`、`SystemDesign`、`PrototypeDesign` 在治理口径上统称“设计阶段”。设计阶段允许围绕同一变更请求做顺序协同，例如先修改需求文档，再同步设计文档和 UI 原型；但每次执行仍只允许 1 个激活角色，且各角色只能写本阶段白名单资产。

> 命令执行权限与文件写权限分离：`Software Engineer` 与 `QA Engineer` 可执行 `.ai/harness.yaml` 中已声明、且被当前 `stage_command_window` 暴露的安全 `setup/build/test` 命令；不得执行未声明安装脚本、系统级包管理、部署脚本或高风险清理命令。

## 8. 角色权限矩阵

### 8.1 角色字段权威值

| 中文名称 | 字段值 |
| --- | --- |
| 需求分析师 | `Product Manager` |
| 系统架构师 | `System Architect` |
| UI/UX 设计师 | `UI/UX Designer` |
| 程序员 | `Software Engineer` |
| 测试工程师 | `QA Engineer` |
| 运维工程师 | `DevOps Engineer` |
| 审阅者 | `Reviewer` |

### 8.2 权限矩阵

| Role | Read Baseline | Write Baseline | Explicitly Forbidden |
| --- | --- | --- | --- |
| `Product Manager` | `.ai/templates/`、需求文档、`.ai/00_index.md`、`.ai/01_status.md` | 需求文档、`.ai/01_status.md` | 系统设计、原型、`src/`、`test/`、`script/`、`.ai/00_index.md` |
| `System Architect` | 需求文档、设计文档、测试用例设计、任务模板、规则文件、`.ai/00_index.md`、`.ai/01_status.md` | 设计文档、`doc/spec/test_case/{module}_test_case.md`、`.ai/01_status.md`；仅在合法发卡窗口写 `doc/spec/tasks/**` 或 `.ai/fix_task/**` | 需求文档、原型、`src/`、`test/`、`.ai/00_index.md` |
| `UI/UX Designer` | 需求文档、相关设计文档、`doc/spec/prototype/`、`.ai/rules/ui_rule.md`、`.ai/00_index.md`、`.ai/01_status.md` | `doc/spec/prototype/`、`.ai/01_status.md` | 需求主文档、系统设计、`src/`、`test/`、`.ai/00_index.md` |
| `Software Engineer` | 当前任务卡、`read_scope.visible_files`、`allowed_files` 内直接相关代码 / 测试、`rule_refs` 规则文件、`.ai/00_index.md` 权限边界章节、`.ai/01_status.md` 当前任务条目 | `write_scope.editable_files`、当前任务 checkpoint、`.ai/01_status.md`；`issued_in=Fixing` 时可写当前修复卡执行字段；**仅在系统架构师授权发卡窗口**，可额外写 `doc/spec/tasks/**`（后续 Coding 任务卡） | 需求、设计、原型、框架文件、其他任务卡、`read_scope` 未声明文件 |
| `QA Engineer` | 当前任务卡、`doc/spec/test_case/{module}_test_case.md`、相关接口声明、测试文件、`.ai/00_index.md`、`.ai/01_status.md` | `doc/spec/test_case/{module}_test_case.md`（仅测试用例设计阶段）、`test/`、`.ai/artifacts/reports/`、`.ai/artifacts/logs/`、`.ai/fix_task/**`（仅 Testing 失败回路）、`.ai/01_status.md` | 修改业务实现、需求/设计主文档、`.ai/00_index.md` |
| `DevOps Engineer` | `doc/spec/prd.md`、`doc/spec/design/system_design.md`、`doc/spec/design/{module}_design.md`、`doc/spec/deploy/deploy.md`、`script/`、`.ai/00_index.md`、`.ai/01_status.md` | `doc/spec/deploy/deploy.md`、`script/`、`.ai/01_status.md` | 需求、设计、测试和业务代码、`.ai/00_index.md` |
| `Reviewer` | 全目录只读、`.ai/00_index.md`、`.ai/01_status.md`、当前任务卡、最新 Evidence Manifest、相关 diff | 仅 `.ai/01_status.md` 中的评分、结论与状态回写 | 修改任何业务产物、`.ai/00_index.md`、绕过审查链路 |

> 测试工程师在 `Testing` 阶段的允许输出还包括测试用例代码与 `Fixing` 任务卡；测试用例设计文档仍由 `SystemDesign` 阶段协同产出。

> 程序员可在声明“无任务卡”后进入无任务卡模式开展任务；该模式不改变其余读写边界。

## 9. 任务卡与执行合约

### 9.1 任务卡适用范围
- 任务卡只服务于 `Coding` 和 `Fixing`；在新建 `Coding` 任务卡前，必须先确认对应测试用例文档存在，且其相关用例已被 `acceptance_tests` 完整覆盖。
- `Coding` 任务卡必须压缩为同一主验收路径下的单一功能切片，默认只覆盖 1 个主 `DESIGN-*` 决策、1 组主 `acceptance_tests` 与直接配套的实现 / 测试文件。
- 第二个接口、第二个页面、跨模块顺手修复、无关重构，或需要明显扩大 `read_scope` / `write_scope` 的内容，必须拆成新卡，不得打包进同一张卡。
- 编码卡必须存放于 `doc/spec/tasks/`，并登记到 `doc/spec/tasks/map_task.md`。
- 修复卡必须存放于 `.ai/fix_task/`，并引用来源编码卡。
- 修复卡完成并完成证据回写后必须自动删除。

### 9.2 任务卡强制字段
- `task_id`
- `module_id`
- `issued_by`
- `issued_in`
- `owner_role`
- `card_type`
- `card_status`
- `req_ids`
- `design_ids`
- `frozen_spec`
- `frozen_facts`
- `decision_sources`
- `input_artifacts`
- `permission_scope`
- `read_scope`
- `write_scope`
- `acceptance_checks`
- `acceptance_tests`
- `focus_contract`
- `test_command`
- `expected_artifacts`
- `blocked_if`
- `context_budget`

### 9.3 范围合同
- `permission_scope` 是审计摘要层。
- `read_scope.visible_files` 是精确可见层。
- `write_scope.editable_files` 是精确编辑层。
- `allowed_files` 是 Harness 粗粒度沙箱层。
- `focus_contract` 是 Harness 机检层；必须把唯一 `focus_key`、主设计 ID、主测试 ID 与焦点产物写成结构化字段。
- `read_scope.visible_files`、`write_scope.editable_files`、`acceptance_tests` 与 `expected_artifacts` 必须共同收敛到同一主验收焦点；若出现第二个独立功能点，任务卡无效。
- 任何写入必须同时满足阶段写边界、`allowed_files` 和 `write_scope.editable_files`。
- 任何读取必须命中当前任务卡允许的输入；缺失则 `Blocked`。

### 9.4 确定性执行规则
- 第一条业务命令前必须创建或更新 `.ai/checkpoints/{task_id}-current.yaml`
- 每条实际执行命令都必须生成 `Command Receipt`
- 每轮执行后必须生成 `Evidence Manifest`
- 恢复执行必须依赖 `resume_token` 与 fingerprint 校验
- 自然语言“继续上次”无效

## 10. Traceability 规则

### 10.1 ID 命名规范
- 需求：`REQ-{module}-{nnn}`
- 设计：`DESIGN-{module}-{nnn}`
- 任务：`TASK-{module}-{nnn}`
- 测试：`TEST-{module}-{nnn}`
- 部署：`DEPLOY-{module}-{nnn}`
- 规格变更：`SCR-{module}-{nnn}`

### 10.2 下游强制回指

| Artifact | Must Reference |
| --- | --- |
| `prd.md` | `REQ-*` |
| `doc/spec/design/{module}_design.md` | `REQ-*` |
| `doc/spec/test_case/{module}_test_case.md` | `REQ-*`, `DESIGN-*` |
| `TASK-*.md` | `REQ-*`, `DESIGN-*` |
| 测试用例与测试报告 | `TASK-*`, `REQ-*`, `TEST-*` |
| 部署文档 | `DEPLOY-*`, `TASK-*` |
| 规格变更记录 | 被替换的 `TASK-*` 或 `DESIGN-*` |

### 10.3 最小闭环
- `TEST -> TASK -> DESIGN -> REQ`
- 若存在部署阶段：`DEPLOY -> TASK -> DESIGN -> REQ`
- 无法映射到至少一个 `REQ-*` 和一个 `DESIGN-*` 的任务不得进入 `Coding`

## 11. Harness 入口

| Item | Value |
| --- | --- |
| harness_contract | `.ai/harness.yaml` |
| setup_command | `{{PROJECT_SETUP_CMD}}` |
| build_command | `{{PROJECT_BUILD_CMD}}` |
| project_test_command | `{{PROJECT_TEST_CMD}}` |
| task_test_command | `{{PROJECT_TASK_TEST_CMD}}` |
| logs_dir | `.ai/artifacts/logs/` |
| reports_dir | `.ai/artifacts/reports/` |
| checkpoint_path | `.ai/checkpoints/{task_id}-current.yaml` |
| coding_map | `doc/spec/tasks/map_task.md` |
| fix_card_dir | `.ai/fix_task/` |

### 11.1 执行前门禁
进入 `Coding / Testing / Fixing` 前必须至少验证：
1. 当前任务卡存在且路径合法；若 `Software Engineer` 已明确声明「无任务卡」，可豁免本项与第 2 项检查，其余读写边界不变
2. 编码卡已登记 `map_task.md`；修复卡位于 `.ai/fix_task/`
3. `frozen_facts`、`decision_sources`、`input_artifacts` 完整
4. `doc/spec/test_case/{module}_test_case.md` 存在且含主路径用例
5. `focus_contract` 合法：`mode=single_focus`、`primary_design_id` 命中 `design_ids`、`primary_acceptance_test` 命中 `acceptance_tests[*].test_id`、全部 `acceptance_tests[*].focus_key` 与 `focus_contract.focus_key` 一致、`focus_artifacts` 与 `write_scope.editable_files` 精确一致且属于 `expected_artifacts`
6. `depends_on` 全部 `Done`
7. `test_command` 可解析
8. 非首次恢复时 `resume_token` 完整
9. 未触发未解决的确认门禁
10. 当前阶段命令窗口合法
11. 单次只允许一个活动执行目标

### 11.2 显式确认门禁
- `scope_expansion`
- `command_ambiguity`
- `task_card_drift`
- `policy_exception`
- `evidence_insufficiency`

> 命中任一门禁：立即 `Blocked`，只允许回写确认门禁字段，等待单批确认结果后恢复。

## 12. 上下文加载协议

### 12.1 全局规则
- 默认先读摘要：`.ai/01_status.md` 只读 `Current State Snapshot` 与当前任务 / 模块条目；历史归档不作为默认读取对象。
- 默认读取阶梯固定为：当前任务卡 -> `frozen_facts` -> `decision_sources` 锚点 -> `input_artifacts` -> `read_scope.visible_files`
- 禁止回读 PRD 全文、系统设计全文、模块设计全文、完整终端历史或无关任务卡。
- 超出 `context_budget` 不是自动许可；必须先触发确认门禁或重发更窄任务卡，默认优先拆成单卡单焦点、同职责域的小任务卡。
- `rule_refs` 只读，不计入业务文件可见配额。
- 缺失关键事实时不允许猜测，只能 `Blocked`。

### 12.2 角色启动顺序

| Role | Step 1 | Step 2 | Step 3 | Step 4 | Explicitly Forbidden |
| --- | --- | --- | --- | --- | --- |
| `Product Manager` | `.ai/00_index.md` | `.ai/01_status.md` Snapshot | `.ai/templates/temp_prd.md` | 用户输入需求 | `src/`, `test/`, 任务卡 |
| `System Architect` | `.ai/00_index.md` | `.ai/01_status.md` Snapshot | `doc/spec/prd.md` 相关模块条目 | 先 `doc/spec/design/system_design.md`，再 `doc/spec/design/{module}_design.md` 与 `.ai/templates/temp_*_design.md` | `src/`, `test/` |
| `UI/UX Designer` | `.ai/00_index.md` | `.ai/01_status.md` Snapshot | `doc/spec/prd.md` 相关模块条目、`doc/spec/design/system_design.md` / `doc/spec/design/{module}_design.md` 的 UI 相关章节 | `doc/spec/prototype/style.html`、现有 `doc/spec/prototype/{module}_ui.html`（如存在）、`.ai/rules/ui_rule.md` | `src/`, `test/`, 设计全文 |
| `Software Engineer` | `.ai/00_index.md` 权限边界章节 | `.ai/01_status.md` 当前任务行 | 当前任务卡 | `input_artifacts` 声明的最小文件集（必须含 `system_design.md`、`{module}_design.md`，有 UI 时还必须含 `{module}_ui.html`） | 其他任务卡、设计全文、未声明文件 |
| `QA Engineer` | `.ai/00_index.md` 权限边界章节 | `.ai/01_status.md` 当前任务行 | `doc/spec/test_case/{module}_test_case.md` 与当前任务卡 | 相关接口声明、测试文件；测试实现必须逐项对应测试用例文档 | 需求全文、设计模板全文、未关联代码 |
| `Reviewer` | `.ai/00_index.md` | `.ai/01_status.md` | 当前任务卡、最新 Evidence Manifest、相关 diff | `.ai/rules/review_rule.md` | 其他模块代码、全量测试套件 |
| `DevOps Engineer` | `.ai/00_index.md` | `.ai/01_status.md` | `doc/spec/prd.md` 相关模块条目、`doc/spec/design/system_design.md`、`doc/spec/design/{module}_design.md` | `doc/spec/deploy/deploy.md`、`.ai/rules/harness_rule.md`；编写脚本前必须先读已冻结部署说明 | 需求全文、详细设计正文 |

## 13. Blocked 与恢复协议

### 13.1 强制停止条件
- 需求歧义
- 设计缺失
- 依赖未就绪
- `input_artifacts` 文件或锚点不存在
- `test_command` 无效
- 环境异常
- 相同 `failure_signature` 连续重复
- flaky 测试
- 任务卡漂移
- 未解决确认门禁

### 13.2 状态回写要求
任务进入 `Blocked` 时，必须写回 `.ai/01_status.md`：
- `task_status: Blocked`
- `blocked_from_state`
- `blocked_reason.type`
- `blocked_reason.description`
- `blocked_reason.source_ref`
- `active_run_id`
- `resume_token`
- `last_evidence_manifest`（若已有）

### 13.3 恢复规则
- 只能使用 `resume_token` 恢复
- 恢复前必须校验 `task_card_fingerprint` 与 `input_fingerprint`
- 任一不匹配：新建 `run_id`
- 不允许凭自然语言或聊天历史续跑

## 14. 运行纪律

1. 除 `.ai/01_status.md`、checkpoint 和证据资产外，任何角色只能写当前阶段允许的业务资产。
2. `Coding` 和 `Fixing` 的写入必须同时满足任务卡白名单与阶段边界。
3. 任何测试通过声明都必须对应结构化测试结果文件。
4. Reviewer 只能审阅与回写结论，不能直接改业务产物。
5. 修复循环最多自动尝试 3 次；超限或重复失败必须升级。
6. 长日志、堆栈和诊断必须外置到 `.ai/artifacts/`，不得塞入规格文档或状态摘要。
7. 若本文件被更新，必须由系统架构师或初始化器在框架治理窗口内修订，其他角色不得改写。
````

### 5.5 Runtime Skeleton

在不伪造实例的前提下创建运行时骨架：

- 创建 `.ai/checkpoints/`
- 创建 `.ai/artifacts/logs/`
- 创建 `.ai/artifacts/reports/`
- 创建 `.ai/fix_task/`
- 创建 `doc/spec/`
- 创建 `doc/spec/design/`
- 创建 `doc/spec/tasks/`
- 创建 `doc/spec/test_case/`
- 创建 `doc/spec/prototype/`
- 创建 `doc/spec/deploy/`
- 创建 `script/`
- 创建 `src/`
- 创建 `src/common/`
- 创建 `src/3rd/`
- 创建 `test/`

### 5.6 Templates And Rules

必须生成（P0 核心合同；§4.1 Minimum Bootstrap 模式除外，该模式仅生成 8 项核心文件并在最终报告中明确标注未达 Coding-ready 状态）：

- `temp_task_card.md`，其中至少显式包含：`frozen_spec`、`frozen_facts`、`decision_sources`、`input_artifacts`、`permission_scope`、`read_scope`、`write_scope`、`acceptance_checks`、`acceptance_tests`、`focus_contract`、`test_command`、`context_budget`；并在正文中显式声明对应 `doc/spec/test_case/{module}_test_case.md` 必须已存在，缺失时不得创建任务卡。模板还必须明确：单卡只允许 1 个主验收焦点与同一职责域内的相关改动，默认保持 `max_visible_files <= 3`、`max_edit_files <= 2`；若需要第二功能点或明显扩大上下文，必须拆卡；同时每个 `acceptance_tests` 条目都要声明与 `focus_contract.focus_key` 一致的 `focus_key`。
- `temp_execution_envelope.yaml`，必须显式包含 `run_id`、`task_id`、`task_status`、`actor_role`、`task_card_ref`、`task_card_fingerprint`、`input_fingerprint`、`planned_commands`、`command_budget`、`expected_outputs`、`resume_from`、`created_at`；其中 `input_fingerprint` 至少拆分为 `task_card` 与 `code_snapshot`；不得出现旧版包标识字段。
- `temp_command_receipt.yaml`，必须包含 `run_id`、`seq`、`stage`、`command`、`cwd`、`input_refs`、`output_refs`、`exit_code`、`duration_ms`、`stdout_summary`、`stderr_summary`、`generated_at` 字段，摘要字段限 200 字符。
- `temp_evidence_manifest.yaml`，必须显式包含 `task_id`、`run_id`、`status`、`failure_signature`、`fix_attempt`、`task_card_snapshot`、`evidence`、`review_input`、`fix_input`、`generated_at`，并声明 `command_receipt` 为必备证据类型；不得出现旧版关联字段。
- `temp_failure_signature.md`，必须包含 Failure Signature 计算方式（`sha256_short`、`components`、`trace_normalization`）、使用规则与 `FS-{task_id}-{hash8}` 格式说明。
- `review_rule.md`、`harness_rule.md`、`context_rule.md`，其正文都必须把任务卡定义为唯一上下文压缩层；其中 `harness_rule.md` 还必须覆盖任务卡位置校验、测试用例文档门禁、建卡中断与先补齐测试用例文档的前置流程、单卡单焦点 / 同职责域的粒度检查、确认门禁阻断与 `blocked_reason.type` 回写约束。
- `.github/skills/spec-code/SKILL.md`，必须作为运行时子技能落盘，且正文必须按 §5.7.2 规范体原样落盘（形状要求见 §5.7.1）；生成结果必须通过 frontmatter、章节标题、状态映射、禁词与确认门禁五项检查，禁止仅写"相似内容"或"语义接近"的变体；生成时不以外部规范文档作为参考，不得保留初始化器身份、不得引用已废弃上下文资产、不得缺失启动协议、低上下文纪律、执行合约协同、confirmation gate 与恢复协议。

若触发 §4.3 Delivery Governance Set（用户要求"严格初始化"或"可交付治理"），还必须额外生成以下 P1 模板：

- `temp_prd.md`
- `temp_system_design.md`
- `temp_module_design.md`
- `temp_map_task.md`，其中必须显式声明：写入任何 TASK 行前先核验对应 `doc/spec/test_case/{module}_test_case.md` 已存在且至少含 1 条主路径用例；若缺失，必须中断建卡并先生成测试用例文档。
- `temp_traceability.md`
- `temp_review_summary.md`
- `temp_test_case.md`
- `temp_deploy.md`
- `temp_spec_change_record.yaml`
- `.ai/rules/{lang}_rule.md`（按推断或确认后的语言规则生成）

### 5.7 Runtime Skill

`.github/skills/spec-code/SKILL.md` 必须体现：

- 启动时在任务态读取当前任务卡，在非任务态读取当前阶段唯一被授权的规格产物，而不是旧版上下文资产
- 低上下文读取阶梯固定为：任务卡 -> `frozen_facts` -> `decision_sources` -> `input_artifacts`
- 任务态正常状态回写只允许命中 `status_writeback_fields`；确认门禁触发时只允许命中 `confirmation_gate_writeback_fields`
- 恢复必须基于 checkpoint 与 `resume_token`，并在恢复前校验 `task_card_fingerprint` 与 `input_fingerprint`
- 若触发 confirmation gate，必须立即 `Blocked`，且只允许回写 `confirmation_gate_writeback_fields` 允许的字段，等待单批确认后再恢复
- `blocked_reason.type` 必须写为触发的 `gate_type`，确认未返回前不得继续运行新命令
- Auto-Run 只有在 `.ai/harness.yaml#auto_run.enabled=true` 且 `startup_checks` 全部通过时才允许启动；其全局停止阈值由 `stop_policy` 决定
- 超出任务卡范围即 `Blocked`

### 5.7.1 Canonical Runtime Skill Shape

`.github/skills/spec-code/SKILL.md` 的落盘结果必须满足下列固定形状；任何一项不满足，初始化器必须重写该文件，不得仅在报告中声明“已生成”：

- Frontmatter 必须只保留 `name: spec-code` 与 `description: "Role-based execution skill for repos with a complete .ai/ Spec Coding framework. Not an initializer."`
- 顶部一级标题必须是 `# Spec Coding Execution Skill`
- 章节顺序必须严格为：
  1. `## 1. 启动协议（每次进入都执行）`
  2. `## 2. 低上下文执行纪律`
  3. `## 3. 执行合约协同`
  4. `## 4. Confirmation Gate 与恢复协议`
  5. `## 5. Auto-Run 模式（Spec 冻结后全自动推进）`
- 第 1 章必须按状态精确限定读取对象：`RequirementDesign` 读 `doc/spec/prd.md` 相关条目；`SystemDesign` 读 `doc/spec/design/system_design.md`、`doc/spec/design/{module}_design.md` 与 `doc/spec/test_case/{module}_test_case.md`；`PrototypeDesign` 先读 `doc/spec/prototype/style.html`，再读现有 `doc/spec/prototype/{module}_ui.html`（如存在）；若 `style.html` 缺失，先按项目背景生成默认草案并暂停原型任务；`Coding/Testing/Fixing` 读当前任务卡、最新 checkpoint，必要时读取最新 Evidence Manifest；不得用"当前阶段唯一产物"之类模糊措辞替代状态映射。
- 第 4 章必须明确写出 `blocked_reason.type = gate_type`、恢复前校验 `task_card_fingerprint` 与 `input_fingerprint`、以及确认未返回前不得继续运行新命令。
- 第 5 章必须包含：仅在 `.ai/harness.yaml#auto_run.enabled=true` 时可触发的前提声明、触发条件校验（8 项启动门禁）、执行循环（含 Coding → Testing → Fixing 闭环与角色调度）、暂停与升级条件表（含 `blocked_reason.type`）、终止协议（成功终止报告 + 循环终止后自检）；Auto-Run 模式下每次迭代仍受 §3 执行合约协同与 §4 门禁约束，不得绕过。
- 生成文件的 Markdown 正文（frontmatter 以下内容）中不得出现以下词汇或等价表述：`initializer`（frontmatter `description` 字段中的 `Not an initializer.` 声明不属于此限制）、`TaskReady`、`Context Pack`、`Context Slice`、`Delta Context`、`.ai/context/`、`temp_context_`、`Spec_Code_Framework.md`、`Spec_Coding_Key_Documents.md`

### 5.7.2 Canonical Runtime Skill Body

初始化器必须将以下规范体**原样**落盘到 `.github/skills/spec-code/SKILL.md`；禁止仅依赖 §5.7.1 的形状要求临时生成，也不得引用任何外部规范文档生成运行时技能。

````markdown
---
name: spec-code
description: "Role-based execution skill for repos with a complete .ai/ Spec Coding framework. Not an initializer."
---

# Spec Coding Execution Skill

## 1. 启动协议（每次进入都执行）

每次进入必须按以下顺序执行：

1. 读取 `.ai/00_index.md`（仅权限边界与状态机章节）。
2. 读取 `.ai/01_status.md` 的 `Current State Snapshot` 与当前模块/任务条目。
3. 根据当前阶段读取精确输入（见下表）；禁止读取表格外文件。

| 当前阶段 | 必须读取 | 禁止读取 |
| --- | --- | --- |
| `RequirementDesign` | `doc/spec/prd.md` 相关模块条目 | `src/`、`test/`、任务卡 |
| `SystemDesign` | `doc/spec/design/system_design.md`、`doc/spec/design/{module}_design.md`、`doc/spec/test_case/{module}_test_case.md` | `src/`、`test/`、任务卡 |
| `PrototypeDesign` | `doc/spec/prototype/style.html`、现有 `doc/spec/prototype/{module}_ui.html`（如存在）；若 `style.html` 缺失，先按项目背景生成默认草案并暂停原型任务 | 需求全文、系统设计全文、`src/`、`test/` |
| `Coding` | 当前任务卡、最新 checkpoint（`.ai/checkpoints/{task_id}-current.yaml`）；必要时读最新 Evidence Manifest | 设计全文、其他任务卡、`read_scope` 未声明文件 |
| `Testing` | 当前任务卡、最新 checkpoint（`.ai/checkpoints/{task_id}-current.yaml`）、`doc/spec/test_case/{module}_test_case.md`、相关接口声明 | 业务实现（除测试目标外）、需求/设计全文 |
| `Fixing` | 当前修复任务卡（`.ai/fix_task/`）、最新 checkpoint；必要时读最新 Evidence Manifest | 无关代码、设计全文、其他任务卡 |

在任何 `PrototypeDesign` 工作开始前，必须先确认当前模块对应的 `doc/spec/prd.md`、`doc/spec/design/system_design.md` 与 `doc/spec/design/{module}_design.md` 三类文档全部存在；缺少任一类文档时，必须立即中断并返回 `Blocked`，不得进入原型设计。

## 2. 低上下文执行纪律

### 2.1 上下文读取阶梯（任务态固定顺序）

任务态（`Coding` / `Testing` / `Fixing`）上下文读取阶梯固定为：

```
当前任务卡 → frozen_facts → decision_sources 锚点 → input_artifacts → read_scope.visible_files
```

- 每轮只读取完成当前阶段所需的最小文件集。
- 禁止回读 PRD 全文、系统设计全文、模块设计全文、完整终端历史或无关任务卡。
- `rule_refs` 只读，不计入业务文件可见配额。
- 超出 `context_budget` 不是自动许可；必须先触发确认门禁或等待重发更窄任务卡。
- 缺失关键事实时不允许猜测，只能 `Blocked`。
- 任务卡是唯一上下文合同；禁止用任何第二套资产弥补任务卡缺陷。

### 2.2 写入纪律

- 任何写入必须同时满足：当前阶段写边界 + `allowed_files` + `write_scope.editable_files`。
- 除 `.ai/01_status.md`、checkpoint 与证据资产外，任何角色只能写当前阶段业务白名单内的文件。
- 任何测试通过声明都必须对应结构化测试结果文件。
- 修复循环最多自动尝试 3 次；超限或重复 `failure_signature` 必须升级至人工处置。

## 3. 执行合约协同

### 3.1 执行前门禁

进入 `Coding` / `Testing` / `Fixing` 前必须全部通过：

1. 当前任务卡存在且路径合法（编码卡在 `doc/spec/tasks/`，修复卡在 `.ai/fix_task/`）。若 `Software Engineer` 已明确声明"无任务卡"，可豁免 item 1 与 item 2 检查，其余读写边界不变。
2. 编码卡已登记 `doc/spec/tasks/map_task.md`。
3. `frozen_facts`、`decision_sources`、`input_artifacts` 完整。
4. `doc/spec/test_case/{module}_test_case.md` 存在且含主路径用例。
5. `focus_contract` 合法：`mode=single_focus`、`primary_design_id` 命中 `design_ids`、`primary_acceptance_test` 命中 `acceptance_tests[*].test_id`、全部 `acceptance_tests[*].focus_key` 与 `focus_contract.focus_key` 一致、`focus_artifacts` 与 `write_scope.editable_files` 精确一致且属于 `expected_artifacts`。
6. `depends_on` 全部 `Done`。
7. `test_command` 可解析。
8. 非首次恢复时 `resume_token` 完整。
9. 未触发未解决的确认门禁。
10. 当前阶段命令窗口合法（`stage_command_window` 校验通过）。
11. 单次只允许一个活动执行目标。

任一检查失败：立即 `Blocked`，回写 `blocked_reason`，等待人工处置。

### 3.2 执行规则

- 第一条业务命令前必须创建或更新 `.ai/checkpoints/{task_id}-current.yaml`（字段含 `run_id`、`task_id`、`actor_role`、`task_card_ref`、`task_card_fingerprint`、`input_fingerprint`、`planned_commands`、`command_budget`）。
- 每条实际执行命令都必须生成 Command Receipt（字段含 `run_id`、`seq`、`stage`、`command`、`exit_code`、`duration_ms`、`stdout_summary`、`stderr_summary`）。
- 每轮执行后必须生成 Evidence Manifest（字段含 `task_id`、`run_id`、`status`、`failure_signature`、`fix_attempt`、`evidence`、`command_receipt`）。

### 3.3 状态回写限制

正常执行时，`.ai/01_status.md` 只允许回写以下字段：`active_run_id`、`task_status`、`source_failure_signature`、`last_evidence_manifest`、`blocked_from_state`、`blocked_reason`、`resume_token`。

禁止在状态回写中夹带设计内容、需求变更、测试用例或任何其他业务资产。

## 4. Confirmation Gate 与恢复协议

### 4.1 显式确认门禁

命中以下任意条件时，立即 `Blocked`：

| gate_type | 触发条件 |
| --- | --- |
| `scope_expansion` | 请求写入超出 `write_scope.editable_files` 或 `allowed_files` |
| `command_ambiguity` | 命令含义不唯一或结果不可预测 |
| `task_card_drift` | 实际需求与任务卡 `frozen_spec` 不一致（checksum drift） |
| `policy_exception` | 请求违反角色权限矩阵或阶段写边界 |
| `evidence_insufficiency` | 执行结论缺乏结构化证据支撑 |

触发门禁时：

1. 立即停止运行新命令。
2. 将 `blocked_reason.type` 写为对应 `gate_type`。
3. 只允许回写 `confirmation_gate_writeback_fields`：`task_status`、`blocked_from_state`、`blocked_reason`、`resume_token`、`active_run_id`、`last_evidence_manifest`。
4. 等待单批确认结果后再恢复；确认未返回前不得继续运行任何新命令。

### 4.2 恢复协议

1. 恢复只能依赖 `resume_token` 触发。
2. 恢复前必须校验 `task_card_fingerprint` 与 `input_fingerprint` 均匹配。
3. 若任一不匹配：新建 `run_id`，不复用旧执行会话。
4. 阻塞解除后只能回到 `blocked_from_state` 记录的原状态，不得跳转到任意下游状态。
5. 不允许凭自然语言描述或聊天历史续跑。

## 5. Auto-Run 模式（Spec 冻结后全自动推进）

Auto-Run 只有在 `.ai/harness.yaml#auto_run.enabled=true` 且 `startup_checks` 全部通过时才可触发；否则必须保持逐卡手动执行。

### 5.1 触发条件（8 项启动门禁）

仅当以下 8 项全部满足时，才允许进入 Auto-Run 模式驱动全任务队列自动执行；任意一项不满足，停止并列出不通过项，不得强行进入循环：

| # | 检查项 |
|---|--------|
| 1 | 每个待执行模块都存在 `doc/spec/test_case/{module}_test_case.md`，且至少含 1 条主路径用例与完整错误码映射 |
| 2 | `doc/spec/tasks/map_task.md` 存在且至少有 1 条 `card_status: Created` 的任务卡 |
| 3 | 所有 `Created` 任务卡的 `acceptance_tests` 已完整覆盖对应模块 `test_case.md` 中与该任务相关的用例矩阵、边界场景与回归关注点 |
| 4 | 所有 `Created` 任务卡的 `write_scope.editable_files` 已精确白名单化（无 `"*"`、无模糊通配、无跨模块路径）|
| 5 | `.ai/harness.yaml` 的 `stage_command_window` 中 `build`/`test`/`lint` 命令均可解析（无 `{{PLACEHOLDER}}` 残留）|
| 6 | 所有任务卡的 `depends_on` 链已解析为无环图，且首个可执行任务的所有依赖均为 `task_status: Done` 或为空 |
| 7 | `01_status.md` 的 `project_status` 为 `Coding`，且当前无 `task_status: Blocked` 且未解除的任务 |
| 8 | P0 框架文件集完整（见 §3.1 执行前门禁所列 11 项）|

### 5.2 执行循环

触发条件全部通过后，按以下循环驱动任务队列；**每次迭代仍受 §3 执行合约协同与 §4 门禁约束，不得绕过**：

```
READ QUEUE: 从 map_task.md 取第一张 card_status=Created
            且 depends_on 全部 Done 的任务卡
  │
  ├─ 无可取任务 ──► §5.4 成功终止
  │
  ▼
ITERATE（Coding）: 激活 Software Engineer
  card_status: Created → InProgress
  task_status: Coding（回写 01_status.md）
  创建/更新 checkpoint；执行 write_scope.editable_files 内代码实现
  产出 Command Receipt + Evidence Manifest
  task_status: Coding → Testing
  │
  ▼
ITERATE（Testing）: 激活 QA Engineer
  实现/更新 test/ 下测试用例代码；执行 test_command
  产出测试报告 + Evidence Manifest
  │
  ├─[PASS] task_status: Testing → Done
  │         card_status: InProgress → Completed
  │         → 回到 READ QUEUE
  │
  └─[FAIL] 生成 failure_signature；检查 fix_attempt
      ├─ fix_attempt < 3 && 未连续重复相同 fs && 无 flaky
      │   ITERATE（Fixing）: 激活 Software Engineer
      │   发 Fixing 卡到 .ai/fix_task/
      │   task_status: Testing → Fixing
      │   定向修复；修复卡 Completed 后删除
      │   task_status: Fixing → Testing → 回到 ITERATE（Testing）
      └─ fix_attempt ≥ 3 || 重复 fs || flaky → §5.3 Blocked 升级
```

每次迭代必须执行：读取状态（只读）→ §3.1 执行前门禁 → 角色执行 → 采集证据（checkpoint + Command Receipt + Evidence Manifest）→ 回写 §3.3 允许的 7 个字段；**单次迭代内只允许一个角色处于激活态**。

`issued_by` 规则：Coding 卡由 `System Architect` 或 `Software Engineer` 发出；Fixing 卡由 `System Architect`、`Software Engineer` 或 `QA Engineer` 发出。

### 5.3 暂停与升级（Blocked）

以下任一条件触发时立即暂停循环，按 §4.1 执行确认门禁写入，并输出 Blocked 升级报告：

| 触发条件 | `blocked_reason.type` |
|---------|----------------------|
| 触发 §4.1 任意 `explicit_confirmation_gate` | 对应 `gate_type` |
| `fix_attempt ≥ 3`（单任务修复超限）| `repeated_failure` |
| 同一 `failure_signature` 连续出现 ≥ 2 次 | `repeated_failure` |
| Testing 同一用例 3 次内 pass/fail 交替（flaky）| `flaky_test` |
| 运行中发现 `depends_on` 未 `Done` | `dep_not_ready` |
| `env_error`（exit 127、构建失败、网络不通）| `env_error` |

若连续 `.ai/harness.yaml#auto_run.stop_policy.global_stop_on_env_error_tasks` 个不同任务均因 `env_error` 进入 `Blocked` 且未解除，立即停止全部执行，等待 DevOps 介入后重新触发 §5.1 触发条件校验。

Blocked 升级报告必须包含：`task_id`、`blocked_from_state`、`blocked_reason.type`、`blocked_reason.description`、`blocked_reason.source_ref`、`resolution_needed`，以及恢复指令提示（`resume {task_id}`）。

### 5.4 终止协议

**成功终止**：`map_task.md` 中所有任务卡均为 `card_status: Completed`，且 `01_status.md` 中所有 `task_status: Done`。

- 不自动推进 `project_status` 到 `Done`；部署验收由 `DevOps Engineer` 独立执行后再确认。
- 输出完成报告：完成任务列表（含证据路径）、修复统计（总次数、涉及 `failure_signature`）、下一步人工确认项（DevOps 部署验收 + `project_status → Done`）。

**循环终止后自检**（无论成功还是 Blocked）：

| # | 检查项 |
|---|--------|
| 1 | `map_task.md` 所有行 `card_status` 均为 `Completed`，或存在 `task_status: Blocked` 的 `InProgress` 卡等待人工处置（无悬空未标注的 `InProgress`）|
| 2 | 每个 `task_status: Done` 的任务均存在 Evidence Manifest，且 `status: pass` |
| 3 | 超出 `01_status.md` 3 条窗口的迁移记录已写入 `.ai/02_TransitionLog.md` |
| 4 | 所有 Fixing 修复卡在 `Completed` 且证据回写后已删除（`.ai/fix_task/` 无活动文件残留）|
| 5 | `active_run_id` 已置空于已 Done/Completed 的任务条目 |
| 6 | 循环中无 `write_scope.editable_files` 白名单外的业务文件写入 |
````

## 6. Validation

本节是初始化最后的验收检查，必须在所有目录与文件写盘完成后执行；任一项不通过都不得宣告完成。

初始化完成前，至少自检以下内容：

1. 不存在 `.ai/context/` 目录或任何 `temp_context_*` 模板。
2. `.ai/00_index.md` 已按 §5.4.1 的 canonical 模板生成，标题、章节顺序与 `ai_constitution` 锚点完整存在。
3. `.ai/00_index.md` 的项目元数据区已写入 9 项人类输入，不包含 `{{PROJECT_*}}`、`{{module}}` 或其他未替换占位符。
4. 若未提供模块清单，`.ai/00_index.md` 使用默认“待登记”模块行，而不是伪造模块实例或保留模块占位符。
5. `.ai/00_index.md` 不包含任何外部规范文档引用、`.ai/context/`、`temp_context_` 等运行时不应依赖的引用。
6. `temp_task_card.md` 已包含 `frozen_facts`、`focus_contract`，不包含旧版前置字段，并显式声明单卡单焦点 / 小上下文规则。
7. `harness.yaml` 的 `pre_execution_checks` 不包含任何旧版上下文校验项。
8. `temp_execution_envelope.yaml` 与 `resume_token` 示例使用 `task_card_ref` / `task_card_fingerprint`。
9. `temp_execution_envelope.yaml` 已显式包含 `actor_role` 与 `input_fingerprint`。
10. `harness.yaml` 已包含 `verify_test_case_doc_present`、`verify_single_focus_contract`、`verify_stage_command_window`、`status_writeback_fields`、`explicit_confirmation_gates`、`confirmation_gate_writeback_fields`、`stage_command_window` 与 `auto_run`，且 `verify_test_case_doc_present` 要求相关用例被 `acceptance_tests` 完整覆盖，`verify_single_focus_contract` 要求任务卡提供可机检的单焦点合同，`auto_run` 包含 8 项启动门禁与全局 `env_error` 停止阈值。
11. 运行时技能不会在任务态回退到模糊的“当前阶段唯一产物”，且非任务态读取对象已按状态精确限定，确认门禁会直接 `Blocked`。
12. 运行时技能 `.github/skills/spec-code/SKILL.md` 已要求恢复前校验 `task_card_fingerprint` / `input_fingerprint`，且不再引用旧版上下文资产或禁词。
13. 初始化开始前，9 项项目元信息已完成逐项校验；若曾缺项，初始化器已重复追问直到全部补齐。
14. 9 项项目元信息全部来自人类明确输入，而不是 AI 对仓库信号、依赖、README 或代码的猜测、补全或默认推断；若曾出现冲突，已由人类最终确认。
15. 推荐目录结构已初始化完成：`.ai/`、`doc/spec/`、`doc/spec/design/`、`doc/spec/tasks/`、`doc/spec/test_case/`、`doc/spec/prototype/`、`doc/spec/deploy/`、`script/`、`src/`、`src/common/`、`src/3rd/`、`test/` 均存在。
16. `.github/skills/spec-code/SKILL.md` 已按 §5.7.2 规范体原样落盘，且通过 §5.7.1 的标题、frontmatter、章节顺序与状态映射一致性校验。
17. `.github/skills/spec-code/SKILL.md` 不包含被禁止的词汇、外部规范文件名或废弃上下文资产引用。
18. `temp_evidence_manifest.yaml` 的 `review_input` 与 `fix_input` 字段已定义为结构化数据对象：`review_input` 须包含 `required`（bool）与 `files`（list，每项含 `path` 和 `kind`）；`fix_input` 须包含 `required`（bool）、`failure_signature`、`failed_tests`（list）与 `fix_attempt`（integer）；不得使用 `required: [list_of_field_names]` 形式的 schema 元数据片段。
19. 若触发 §4.3 Delivery Governance Set，`.ai/rules/{lang}_rule.md` 已按项目主语言生成（如 `python_rule.md`、`typescript_rule.md`）；内容至少覆盖：代码规范、安全约束（OWASP Top 10 基准）、测试规范与错误处理禁令；若语言尚未覆盖骨架，须结合项目主语言特性自行生成。


## 7. Done Criteria

只有同时满足以下条件，才可宣告初始化完成：

- P0 合同文件已落盘
- `.ai/00_index.md` 已按 §5.4.1 自包含生成，且不依赖维护仓库规范文件
- 运行时空骨架已创建（含 `doc/spec/` 与 `doc/spec/tasks/` 目录）
- 推荐目录结构已初始化完成（含 `doc/spec/design/`、`doc/spec/test_case/`、`doc/spec/prototype/`、`doc/spec/deploy/`、`script/`、`src/`、`src/common/`、`src/3rd/`、`test/`）
- 运行时子技能 `.github/skills/spec-code/SKILL.md` 已按 §5.7.2 规范体原样落盘，且通过 §5.7.1 的标题、frontmatter、章节顺序、禁词与状态映射一致性检查
- 不存在已废弃的 context 资产模板与目录
- 9 项项目元信息已由人类完整输入并通过逐项校验；缺项场景已在进入初始化前被重复追问直至补齐，任何与仓库信号的冲突都已由人类最终确认
- 若仓库存在前端/UI 原型需求，则 `.ai/rules/ui_rule.md` 已按确认结果生成或明确豁免
- 已在最终报告中说明命令推断结果、覆盖策略与 execution-ready 状态
