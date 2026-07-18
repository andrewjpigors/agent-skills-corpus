---
name: scholar-pipeline
description: |
  学术写作全流程编排器。自动协调规划、写作、审阅的多轮迭代。
  触发词：写申报书、写论文、学术写作、开始写作、write proposal、
  write paper、nsfc、国自然
  适用：国自然申报书、AI顶会论文等学术文档的端到端生成与迭代优化。
allowed-tools: [Read, Write, Edit, Bash, Agent]
---

# Scholar Pipeline — 学术写作全流程编排器

## Section 1: 初始化

### 1.1 读取配置

Pipeline 启动时，首先加载项目配置和模板定义，构建完整的运行参数。

```
{SCRIPTS} = 脚本目录绝对路径，编排器在会话开始时按自身文件位置解析一次
           （等价于 Path(__file__).resolve().parents[2] / "scripts"——
           本 SKILL.md 位于 <仓库根>/scholar-writing/skills/pipeline/SKILL.md，
           parents[2] 上溯三级父目录正好落在 <仓库根>/scholar-writing/，再拼接 scripts/
           即得 <仓库根>/scholar-writing/scripts/；抄 init_project.py:21-23 的同款解析逻辑，
           注意不要在 parents[2] 后面重复拼接 "scholar-writing"，那会产生不存在的
           scholar-writing/scholar-writing/scripts/ 路径）。
           下文所有脚本调用均以 python3 {SCRIPTS}/<name>.py 的绝对路径形式给出，不受当前 cwd 影响。

初始化流程：

1. 读取 config.yaml
   config = Read("config.yaml")
   project_type     = config.project.type          # 例如 "nsfc", "paper"
   project_template = config.project.template       # 例如 "youth_fund", "icml"
   input_mode       = config.project.input_mode     # "from_materials" | "from_outline" | "from_draft"
   # 风格与交付相关字段（全部可选，schema 不进 required；缺省语义见第 5 步的优先级合并）
   cfg_citation_style  = config.project.citation_style    # "numbered" | "author_year"，未配置为 undefined
   cfg_style_profile   = config.project.style_profile     # 画像路径（相对 scholar-writing/ 根）或 null
   cfg_style_alignment = config.project.style_alignment   # boolean，仅 input_mode == "from_draft" 时生效
   cfg_delivery        = config.delivery                  # 顶层可选块 {sections: [模板 sections[].name…]}，
                                                          # 未配置 = 全量交付（命名刻意避开 scope，
                                                          # 防与 aggregate.py --scope 参数撞名）

2. 加载模板（支持继承）
   template_path = "templates/{project_type}/{project_template}.yaml"
   template = Read(template_path)

   # 模板继承：深度合并
   # extends 语义（权威说明见 references/CONVENTIONS_ZH.md 第四节）：
   #   extends 的取值是"相对 templates/ 根、不含 .yaml 后缀"的路径，
   #   例如 面上项目.yaml 中 extends: nsfc/base 指向 templates/nsfc/base.yaml。
   #   解析时【不要】再额外拼接 project_type 段，否则会拼成
   #   templates/nsfc/nsfc/base.yaml（重复 nsfc，double-nsfc bug）。
   if template.extends:
       parent_path = "templates/{template.extends}.yaml"   # 正确：templates/nsfc/base.yaml
       parent_template = Read(parent_path)
       # 若父模板自身也含 extends，则先递归解析到最顶层祖先，再自底向上逐层合并
       template = deep_merge(parent_template, template)     # parent 为基准，child 覆盖
       # deep_merge 规则（明确可执行；对 sections / dependency_graph /
       # review_strategy / length_management 等父模板键，均被子模板同名键覆盖）：
       #   1) 标量字段（如 name、review_strategy 字符串、length_management 下的标量）：
       #      child 有则覆盖 parent，child 无则保留 parent。
       #   2) 字典字段（如 dependency_graph、length_management）：按 key 递归 deep_merge，
       #      同名 key 下 child 覆盖 parent，parent 独有的 key 保留。
       #   3) 数组字段（如 sections）：
       #      · 元素为带 name（无 name 则用 id）的对象时，按该键对齐：
       #        - 同名元素：递归 deep_merge，child 字段覆盖 parent 同名字段，
       #          parent 未被覆盖的字段保留（如子模板只改某章 target_length，其余字段沿用父模板）；
       #        - child 独有的新元素：追加到数组末尾；
       #        - parent 独有的元素：保留。
       #      · 元素为标量、或缺少 name/id 无法对齐时：child 整个数组替换 parent（不追加）。

3. 从模板提取核心结构
   sections          = template.sections            # 章节列表，每项含 id、name、reviewer_dims，
                                                     # 以及三个"真源"字段（权威说明见 CONVENTIONS_ZH.md 第一节）：
                                                     #   file      落盘文件名真源（如 06_特色与创新.md，不含 sections/ 前缀，由消费方拼接）
                                                     #   checklist 评审 checklist 真源（如 checklists/06_创新点.yaml）
                                                     #   writer    写作 skill 真源（如 writer/nsfc/创新点）
                                                     # 编排器一律以这三个字段为准，不得按章节名反推文件/skill 路径
   dependency_graph   = template.dependency_graph    # 章节间依赖关系（DAG）
   review_strategy    = template.review_strategy     # "per_section" | "batch" | "hybrid"

4. 从 config.yaml 提取运行参数
   convergence        = config.convergence           # { max_section_rounds, max_global_rounds, section_score_threshold, global_score_threshold }
   score_weights      = config.score_weights         # 各审阅维度权重，如 { logic: 0.2, detail: 0.15, ... }
   checklist_weight_map = config.checklist_weight_map # checklist 条目到维度的映射权重
   critical_threshold = config.critical_threshold    # 关键缺陷阈值，低于此分数触发 human_needed

5. 合并为运行时上下文
   # 风格/交付字段的优先级合并：项目 config > 模板顶层 > 缺省
   #（模板顶层可声明 citation_style / style_profile 作为模板级缺省，见 schemas/template.schema.yaml；
   #  style_alignment 与 delivery 只在项目 config 声明，无模板级缺省）
   citation_style  = cfg_citation_style  存在 ? cfg_citation_style  : (template.citation_style 存在 ? template.citation_style : "numbered")
   # style_profile 三值语义（键缺失 ≠ 显式 null，勿混同——init_project 生成的 config 缺省不写该键）：
   #   键缺失        → 继承模板缺省（template.style_profile 存在 ? template.style_profile : null）
   #   显式 null     → 用户禁用画像（不回落模板缺省）
   #   显式字符串    → 覆盖模板，用该路径
   style_profile   = cfg_style_profile 键缺失 ? (template.style_profile 存在 ? template.style_profile : null)
                     : cfg_style_profile
   style_alignment = cfg_style_alignment 存在 ? cfg_style_alignment : false     # 仅 input_mode == "from_draft" 时生效
   delivery        = cfg_delivery        存在 ? cfg_delivery        : null      # null = 全量交付
   runtime_ctx = {
       project_type, project_template, input_mode,
       sections, dependency_graph, review_strategy,
       convergence, score_weights, checklist_weight_map, critical_threshold,
       citation_style, style_profile, style_alignment, delivery
   }
```

配置校验规则：
- `config.yaml` 不存在 → 报错并终止，提示用户在仓库根运行 `python scholar-writing/scripts/init_project.py <项目名> --template <类型>/<模板>`
- `template` 文件不存在 → 报错并终止，列出可用模板
- `sections` 为空 → 报错并终止
- `dependency_graph` 中引用了不存在的 section id → 报错并终止
- `convergence.max_section_rounds` 必须 >= 1 且 <= 10
- `convergence.max_global_rounds` 必须 >= 1 且 <= 5
- `convergence.section_score_threshold` 必须在 0-100 之间
- `convergence.global_score_threshold` 必须在 0-100 之间
- `project.citation_style` 若配置，必须是枚举值 `numbered` 或 `author_year`（未配置按 `numbered` 处理）
- `project.style_profile` 若配置且非 null，必须是字符串路径（相对 scholar-writing/ 根），且指向的画像文件必须存在 → 不存在则报错并终止；显式 null 表示禁用画像（不回落模板缺省），键缺失才继承模板缺省（见上方合并规则）
- `project.style_alignment` 若配置，必须是 boolean；取 true 而 `input_mode != "from_draft"` 时输出警告并按 false 处理（该开关仅 from_draft 生效）
- `delivery.sections` 若配置，必须是非空字符串数组，且每个元素都能在模板 `sections[].name` 中找到 → 有对不上的章节名则报错并终止

### 1.1b Schema 校验（V1 校验点）

Pipeline 启动后，调用 validate.py 校验配置和输入文件：

```
# V1: 校验 config.yaml
result = Bash("python3 {SCRIPTS}/validate.py config config.yaml --format json")
if result.valid == false:
    输出错误信息给用户
    终止 Pipeline

# V1: 根据 input_mode 校验输入完整性
switch(input_mode):
    case "from_materials":
        result = Bash("python3 {SCRIPTS}/validate.py manifest materials/manifest.yaml --format json")
        if result.valid == false: 终止 Pipeline，提示用户修复 manifest.yaml
    case "from_outline":
        result = Bash("python3 {SCRIPTS}/validate.py outline planning/outline.md --format json --project-type {project_type}")
        if result.valid == false: 终止 Pipeline，提示用户修复 outline.md
    case "from_draft":
        验证 sections/ 下至少有一个 .md 文件，否则终止
```

### 1.2 断点恢复

Pipeline 支持从任意中断点恢复执行，通过 `scores.yaml` 记录项目状态。

**scores.yaml 原子写约定（全流程强制）**：`scores.yaml` 是断点恢复的唯一状态源。任何对它的持久化都**必须**通过原子写脚本完成，**禁止用 Write 工具或任何方式直接整文件覆盖 scores.yaml** —— 否则一旦写到一半崩溃，状态文件会损坏成非法 YAML，丢失全部进度且无法安全恢复。为此约定写入原语 `write_scores(scores)`，其实现固定为：把 scores 序列化为 YAML 文本，通过 stdin 传给 `{SCRIPTS}/atomic_write.py`（脚本内部用 tempfile 写临时文件、fsync 落盘后再 os.replace 原子替换目标，天然防半写；且写入前会自动做一次 YAML 合法性校验，非法内容根本不触碰目标文件）：

    write_scores(scores)  ≡  Bash("python3 {SCRIPTS}/atomic_write.py scores.yaml", stdin = yaml_dump(scores))

（此处 stdin=... 是伪代码简写，实际编排器需要用 heredoc 形式把 yaml_dump(scores) 的内容传给 atomic_write.py
的标准输入，例如：Bash("python3 {SCRIPTS}/atomic_write.py scores.yaml <<'SCORES_EOF'\n{yaml_dump(scores)}\nSCORES_EOF")，
分隔符 SCORES_EOF 不得出现在 scores 内容本身中；atomic_write.py 在 stdin 为空时会拒绝写入，见其自身实现。）

本文件后续所有 `write_scores(scores)`，以及散文中"更新 scores.yaml: …""写入 scores.yaml""在 scores.yaml 中标注 …"等一切对 scores.yaml 的持久化表述，**一律指经由此脚本的原子写入**，不再逐处展开。

```
断点恢复流程：

1. 检查 scores.yaml 是否存在
   scores_path = "scores.yaml"
   scores_exists = file_exists(scores_path)

2. 如果不存在 → 新项目初始化
   if not scores_exists:
       scores = {
           phase: "init",
           global_round: 1,          # 外环轮次真源，1-based（与 §4.1 的 round 计数口径一致，见该字段的读写约定）；
                                      # 初值取 1 而非 0：§4.1 外环主循环 `FOR round = scores.global_round TO
                                      # convergence.max_global_rounds` 直接以此字段作为起始边界，若初值为 0 会
                                      # 在全新项目首次进入外环时多跑出一个不存在的 "round 0" 迭代，
                                      # 与全文其余 round 计数（reviews/round_{round}/…、round == max_..._rounds
                                      # 等比较）的 1-based 语义冲突；初值直接设为 1 无需在循环处做额外的
                                      # max(…, 1) 特判，语义最自洽。
           global_scores: [],        # 顶层数组真源（schemas/scores.schema.yaml），外环每轮由§4.1「评分聚合」
                                      # 向此数组 append 一条 {round, consistency, narrative, feasibility, format,
                                      # weighted, flagged}；此处先初始化为空数组，避免外环第一次 append 前该字段
                                      # undefined
           sections: {}
       }
       for section in runtime_ctx.sections:
           scores.sections[section.id] = {
               status: "pending",       # pending | writing | reviewing | revising | approved | human_needed
               current_round: 0,        # 章节内环真源，本轮读到的最新轮次（0 = 尚未进入审阅-修改循环）
               rounds_used: 0,          # 该章节实际耗费的内环轮次（approved / revising 收尾时回写）
               inner_scores: [],        # 每轮内环评分记录
               reviewer_feedback: null,
               last_updated: now()
           }
       write_scores(scores)      # 原子写，见本节开头「scores.yaml 原子写约定」
       # V4: 校验 scores.yaml 状态机合法性
       result = Bash("python3 {SCRIPTS}/validate.py scores scores.yaml --format json")
       if result.valid == false:
           尝试自修复（修正非法状态值）后 write_scores(scores)
           if 仍失败: scores.phase = "human_needed"; write_scores(scores)
       # 后续所有 scores.yaml 写入均经 write_scores（原子写），并在写入后执行 V4 校验

3. 如果存在 → 先校验，再按 per-section 状态精确定位断点
   else:
       # 【恢复先校验】分两层：先确认 YAML 本身可解析，再确认语义合法。绝不拿一个可能损坏/
       # 非法的状态直接路由——否则会把坏状态越走越坏、甚至覆写掉可挽救的进度。
       TRY:
           scores = Read(scores_path)   # YAML 解析；失败在此层被捕获
       CATCH 解析异常:
           # 层1：YAML 语法本身损坏，scores 对象不可用，无从读取任何既有字段，只能重建骨架
           备份原文件（不覆盖，另存为 scores.yaml.corrupt）
           写入最小合法骨架 {phase: "human_needed", global_round: 0, global_scores: [], sections: {}}（write_scores 原子写；
                           这是本次故障后唯一一次合法写入——旧内容已不可读，无从修改；global_scores 一并初始化为
                           空数组，避免后续外环第一次 append 时该字段 undefined）
           输出诊断："scores.yaml 不是合法 YAML（解析失败），已备份到 scores.yaml.corrupt"
           提示用户："请参考备份文件人工恢复各章节状态后重新运行 Pipeline。"
           STOP

       # 层2：YAML 语法合法，进一步做语义校验（phase/status 枚举、必填字段等）
       result = Bash("python3 {SCRIPTS}/validate.py scores scores.yaml --format json")
       if result.valid == false:
           输出诊断：打印 validate.py 报告的具体非法点（phase/status 枚举越界、
                     缺失必填字段、section 状态机非法跳转等）
           scores.phase = "human_needed"
           write_scores(scores)          # 原子写；scores 对象本身可读，只是语义不合法，安全回写
           提示用户："scores.yaml 状态文件语义非法（YAML 本身可解析），无法安全恢复。
                    请根据以上诊断修复后重新运行 Pipeline。"
           STOP

       phase = scores.phase

       # 路由原则：
       #   顶层 phase 只负责【粗粒度阶段】（init / global_review / expert_review / human_needed /
       #   gate_blocked / export_failed / stalled / completed）；
       #   而章节内环（写作—审阅—修改）的【精确断点】一律以 per-section status 为准来定位——
       #   遍历 sections，按拓扑序找到断点章节及其所处子阶段，而非仅凭顶层 phase 粗粒度路由。
       #   这样可避免"某章 reviewing/revising 中途崩溃后，被当成未写而从 Writer 重跑、
       #   丢弃已完成的审阅/修订"。per-section status 与顶层 phase 的映射：
       #     pending  → 首次写作     writing → 重写（上次写作未完成）
       #     reviewing→ 重审本轮     revising→ 重跑本轮修改后再审
       #     approved → 跳过         human_needed → 需人工介入

       switch(phase):

           case "init":
               # 上次在初始化阶段中断，重新开始
               # 【style_align pass 的重入语义】from_draft 项目若启用了风格对齐
               # （runtime_ctx.style_profile 存在且 style_alignment == true），§1.3 的风格对齐
               # pass 在【全部章节对齐完成后】才把 phase 置为 section_review——因此对齐 pass
               # 未完成即中断时，phase 仍停留在 init，重入本分支后会经 §1.3 重跑整个对齐 pass。
               # 该 pass 设计为幂等重跑：Revision(mode=style_align) 以画像为目标语体做整章重写，
               # 对已对齐章节再次执行不改变事实内容、只收敛到同一语体，不会越改越偏；
               # 对齐完成后统一置 status=reviewing、current_round=1，与首次执行产生同一状态。
               → 继续执行 Section 1.3 入口路由

           case "section_writing", "section_review", "revision":
               # 内环任一子阶段中断（三个 phase 统一按 per-section status 精确恢复；
               # 无论 from_materials / from_outline / from_draft 入口进入内环，均可达本分支，
               # section_review 与 revision 子阶段在此都可被正确恢复）。
               # 按拓扑序（Section 3 的章节执行顺序）找到第一个仍处于内环未完成子阶段的章节：
               target = 按拓扑序 first(s for s in scores.sections where s.status in {"pending", "writing", "reviewing", "revising"})
               if target is null:
                   remaining_human_needed = [s for s in scores.sections where s.status == "human_needed"]
                   if remaining_human_needed 为空:
                       # 所有章节已 approved，推进到外环
                       scores.phase = "global_review"
                       write_scores(scores)
                       → 跳转 Section 4
                   else:
                       # 余下未完成的章节全部卡在 human_needed，转诊断处理
                       → 转顶层 case "human_needed" 的处理
               else:
                   switch(target.status):
                       case "pending":
                           → 跳转 Section 3，从 target 章节的【写作阶段】开始（首次写作）
                       case "writing":
                           # 上次写作中途崩溃，本节尚未完成，重写
                           → 跳转 Section 3，从 target 章节的【写作阶段】开始（重写）
                       case "reviewing":
                           # 已写完、审阅中崩溃，续跑本轮审阅，不回退到 Writer
                           → 跳转 Section 3，从 target 章节【审阅-修改循环】的第 target.current_round 轮继续（重审第 target.current_round 轮，不从第1轮重新开始）
                       case "revising":
                           # 本轮 Revision 中途崩溃，重跑本轮修改后再审，不回退到 Writer
                           → 跳转 Section 3，从 target 章节【修改】步骤开始（重修第 target.current_round 轮）
                       # human_needed 已被排除在选择范围外，target 不会取到该状态，无需在此处理
                   # 说明：approved 与 human_needed 的章节都不会被选为 target；human_needed 章节需等其余章节全部完成后统一转诊断处理

           case "global_review":
               # 进入外环全文验证
               → 跳转 Section 4

           case "expert_review":
               # 外环已收敛且两道前置门已过，在阶段4 专家评审中断——重跑阶段4（幂等）
               → 跳转 Section 4.3

           case "human_needed":
               # 输出诊断信息，等待用户介入
               blocked_sections = [s for s in scores.sections where s.status == "human_needed"]
               for s in blocked_sections:
                   输出：
                     - 章节文件: s.file
                     - 当前轮次: s.current_round
                     - 最近评分: s.inner_scores[-1] if exists
                     - 审阅反馈: s.reviewer_feedback
                     - 卡点原因: 评分低于 critical_threshold 或达到 max_section_rounds 仍未收敛
               提示用户：
                 "以上章节需要人工介入。请修改后将 status 改为 'pending' 并重新运行 Pipeline。"

           case "gate_blocked":
               IF scores.blocker.type == "completeness":
                   输出：以下章节未通过完备性门，请人工补齐后重新运行：
                   FOR item IN scores.blocker.problem_sections:
                       输出 "- {item.file}（{item.name}）：{item.reason}"
                   提示："修复上述章节内容后无需改动 phase，直接重新运行 Pipeline 即可——会自动重新执行前置门1，不会重跑外环审阅轮次。"
               ELIF scores.blocker.type == "render_backfill":
                   输出：以下插图缺失或题注与嵌图数不符，请人工补图后重新运行：
                   FOR item IN scores.blocker.missing:
                       输出 "- {item}"
                   输出："当前题注数 {scores.blocker.caption_lines} / 已嵌入图片数 {scores.blocker.embedded}"
                   提示："补齐插图后直接重新运行 Pipeline 即可——会自动重新执行前置门2，不会重跑外环审阅轮次。"
               → 跳转 Section 4.1『两道前置门』代码块（FOR round 循环体内 `IF agg.approved == true:` 分支下方
                 的前置门1起始处），从前置门1开始重新执行；不重新进入 FOR round 循环头部、不重新调用
                 R4-R7 Reviewer、不重新计算 agg —— 直接复用 scores.yaml 中已持久化的上一次收敛结果，
                 只重跑前置门1和前置门2这两步及其后续判断（专家评审分支 / 置 completed）。
                 前置门通过则按 Section 4.1 原逻辑继续；仍不通过则再次置 phase="gate_blocked" 并更新 blocker 诊断。

           case "export_failed":
               输出："最终导出失败，原因：{scores.blocker.reason}"
               输出："详情：{scores.blocker.export_result}"
               提示："请人工排查导出环境（如 pandoc 是否可用、磁盘空间、输出目录权限等）后重新运行 Pipeline；
                     两道前置门已通过，重新运行会直接原地重跑 Section 4.2 的导出步骤，不会重跑外环审阅轮次。"
               → 跳转 Section 4.2『最终导出』代码块重新执行（该代码块的判断条件同时接受
                 phase == "completed" 或 "export_failed"，见 Section 4.2）。

           case "stalled":
               输出："外环已跑满 {convergence.max_global_rounds} 轮仍未收敛"
               输出："各维度分数趋势：{scores.blocker.weighted_trend}"
               输出："反复不过的 checklist 项：{scores.blocker.failing_checklist}"
               提示：可选两种处理方式——
                   "(a) 人工修改 config.yaml 提高 convergence.max_global_rounds 后，将 phase 改回 'global_review' 重新运行；
                        外环主循环已支持从 scores.global_round 记录的轮次续跑，不会浪费已完成轮次。"
                   "(b) 若认为当前质量已可接受，可人工将 phase 直接改为 'completed' 触发导出（导出前仍会执行 V5 最终完整性校验兜底，
                        不会因为跳过外环收敛判定就放过真正的产物缺陷）。"

           case "completed":
               # 交付物文件名：未配置 delivery 时为 output/{项目名}.docx；
               # 配置了 delivery（部分交付）时为 output/{项目名}_部分交付.docx（见 Section 4.2），下同
               交付物路径 = runtime_ctx.delivery 存在 ? f"output/{项目名}_部分交付.docx" : f"output/{项目名}.docx"
               IF NOT file_exists(交付物路径):
                   # 幂等重试：completed 状态下 docx 缺失，说明上次可能在导出前就崩溃了（phase 先被置 completed，导出还没跑完）
                   → 跳转 Section 4.2『最终导出』代码块重新执行（同 case "export_failed" 的重入方式）
               ELSE:
                   提示："项目已完成，最终交付物 {交付物路径} 已存在。"
                   输出交付摘要：最终分数、总轮次、各维度分数趋势、token 消耗
```

### 1.3 入口路由

根据 `input_mode` 决定 Pipeline 从哪个阶段开始执行。

```
入口路由逻辑：

switch(runtime_ctx.input_mode):

    case "from_materials":
        # 用户提供了原始素材（文献、笔记、数据等），需要从零开始
        # → 执行阶段 1：架构规划
        scores.phase = "init"
        write_scores(scores)
        # 说明：本入口经 Section 2 用户确认后置 phase=section_writing 进入 Section 3；
        #       内环子阶段（section_review / revision）由 Section 3.1 在推进过程中写入 scores.phase，
        #       因此崩溃后 1.2 的恢复 switch 对本入口同样可精确定位到审阅/修订子阶段。
        → 跳转 Section 2（Architect Agent 进行架构规划）

    case "from_outline":
        # 用户已提供 planning/outline.md（大纲）
        # 系统需要补全以下结构化文件：
        validate_file_exists("planning/outline.md")

        # 补全步骤：
        # a) 从 outline.md 解析章节结构，生成 dependency_graph.yaml
        #    - 分析各章节间的引用关系和逻辑依赖
        #    - 构建 DAG 并验证无环
        Agent("architect", task="从 outline.md 生成 dependency_graph.yaml")

        # b) 从 outline.md 提取核心论点，生成 claim_registry.md
        #    - 每个 claim 包含：id, statement, evidence_refs, section_refs
        Agent("architect", task="从 outline.md 提取 claim_registry.md")

        # c) 如果存在 references/ 目录，生成 material_mapping.md
        #    - 将素材映射到各章节
        if dir_exists("references/"):
            Agent("architect", task="生成 material_mapping.md")

        scores.phase = "section_writing"
        write_scores(scores)
        → 跳转 Section 3（开始章节写作-审阅循环）

    case "from_draft":
        # 用户已提供各章节草稿 sections/*.md
        # 系统补全 claim_registry.md，然后进入审阅模式
        validate_dir_exists("sections/")
        draft_files = glob("sections/*.md")
        if len(draft_files) == 0:
            报错："sections/ 目录为空，请提供至少一个章节草稿文件。"

        # 补全 claim_registry.md
        Agent("architect", task="从 sections/*.md 提取 claim_registry.md")

        # 标记所有章节为 writing 完成，直接进入审阅
        # 注意：存在性判断以模板 sections[].file（落盘真源）为准，不用 section.id 反推文件名
        for section in runtime_ctx.sections:
            if file_exists(f"sections/{section.file}"):
                scores.sections[section.id].status = "reviewing"
                scores.sections[section.id].current_round = 1

        # ── 风格对齐 pass（与 §2.5 末尾的增补一致，两处描述同一子流程）──
        IF runtime_ctx.style_profile 存在 AND runtime_ctx.style_alignment == true:
            # 风格对齐 pass：入环前先把草稿重写到画像语体，再走正常审阅
            FOR section IN 已存在章节（delivery 范围内；未配置 delivery 则全量，按 section.name 对齐）:
                按 §8.3 模板调用 Revision(mode=style_align, 注入画像路径)
                # Revision 在 change_log 标注「全维度复审必需: 是」
            对齐后所有章节 status=reviewing、current_round=1（write_scores 原子写）
            # 注意：此 pass 的产出必须完整走内环 R1-R3 与外环 R4-R7，不得沿用对齐前评分
        # 重入语义见 §1.2「style_align pass 的重入语义」：pass 完成前 phase 仍是 init，
        # 中断后重入会从本分支头部整体重跑该 pass（幂等）

        scores.phase = "section_review"
        write_scores(scores)
        → 跳转 Section 3（审阅模式，跳过 Writer 首轮）
```

### 1.4 Dry Run 模式

在正式执行前，可通过 `config.dry_run` 预览完整执行计划。

```
Dry Run 流程：

if config.dry_run == true:

    # 1. 计算章节执行顺序（拓扑排序）
    exec_order = topological_sort(runtime_ctx.dependency_graph)

    # 2. 估算每章节调用次数
    estimated_calls = {}
    for section in exec_order:
        writer_calls = 1                                    # 首轮写作
        reviewer_calls = 1                                  # 首轮审阅
        revision_calls = convergence.max_section_rounds - 1   # 最大修改轮次（最坏情况）
        estimated_calls[section.id] = {
            writer: writer_calls,
            reviewer: reviewer_calls * len(section.reviewer_dims),
            revision: revision_calls
        }

    # 3. 估算外环调用
    outer_calls = convergence.max_global_rounds * len(runtime_ctx.sections)

    # 4. 汇总
    total_agent_calls = sum(
        e.writer + e.reviewer + e.revision
        for e in estimated_calls.values()
    ) + outer_calls

    # 5. 输出执行计划
    输出：
      "=== Dry Run 执行计划 ==="
      "项目类型: {project_type} / {project_template}"
      "输入模式: {input_mode}"
      ""
      "章节执行顺序:"
      for i, section in enumerate(exec_order):
          e = estimated_calls[section.id]
          "  {i+1}. {section.name}"
          "     Writer 调用: {e.writer} 次"
          "     Reviewer 调用: {e.reviewer} 次 ({len(section.reviewer_dims)} 个维度)"
          "     最大修改轮次: {e.revision} 次"
      ""
      "外环全文验证: 最多 {convergence.max_global_rounds} 轮"
      "Agent 调用总估算: {total_agent_calls} 次（最坏情况）"
      ""
      "收敛参数:"
      "  内环最大轮次: {convergence.max_section_rounds}"
      "  外环最大轮次: {convergence.max_global_rounds}"
      "  章节通过分: {convergence.section_score_threshold}, 全文通过分: {convergence.global_score_threshold}"
      "  关键缺陷阈值: {critical_threshold}"

    # 6. 不执行任何 Agent 调用，直接结束
    return
```

---

## 2. 阶段 1：架构规划

本阶段调用 Architect Agent 分析用户材料并构建文档骨架。

### 2.1 调用 Architect Agent

1. 通过 Bash 工具列出 `materials/` 目录下的所有文件
2. 读取每个文件内容（PDF 文件提取文本摘要，Markdown/文本文件直接读取）
3. 读取 `config.yaml` 中的项目类型和模板信息
4. 构造 Architect Agent 的 prompt：

```
你的任务是分析以下研究材料，构建国自然申报书的文档骨架。

## 项目配置
{config.yaml 中的 project 节}

## 材料清单
{materials/ 下每个文件的路径和内容}

## 输出要求
请生成以下 4 个文件：

1. planning/outline.md — 全文大纲
   格式：每个章节包含标题、核心论点（1-2句）、预期篇幅、要点列表

2. planning/dependency_graph.yaml — 章节依赖关系
   格式：与模板中的 dependency_graph 相同的 YAML 结构
   基于模板默认值，根据具体项目微调

3. planning/claim_registry.md — 核心论点注册表
   格式：Markdown 表格
   | 论点ID | 核心论点 | 摘要中表述 | 立项依据中表述 | 研究内容中表述 | 创新点中表述 |

4. planning/material_mapping.md — 材料到章节的映射
   格式：每个章节列出对应的材料文件及其中的关键段落
```

5. 通过 Agent 工具调用 Architect Agent（subagent_type="general-purpose"）

### 2.2 产出物验证

调用后检查：
- planning/outline.md 存在且非空
- planning/dependency_graph.yaml 存在且可被 YAML 解析
- planning/claim_registry.md 存在且非空
- planning/material_mapping.md 存在且非空

任一缺失 → 重试（最多 2 次）→ 仍失败则更新 scores.yaml phase → human_needed

#### V2 Schema 校验

Architect 生成文件后，校验格式正确性：
```
for file_type, path in [("outline", "planning/outline.md"),
                         ("dependency_graph", "planning/dependency_graph.yaml"),
                         ("claim_registry", "planning/claim_registry.md")]:
    result = Bash(f"python3 {SCRIPTS}/validate.py {file_type} {path} --format json --project-type {project_type}")
    if result.valid == false:
        if retry_count < 2: 重新调用 Architect
        else: 更新 scores.yaml phase → human_needed
```

### 2.3 用户确认

输出 outline.md 的内容摘要，请求用户确认或微调：
- 用户确认 → 更新 scores.yaml phase → section_writing，进入阶段 2
- 用户修改 → 等待用户编辑 outline.md 后再次确认

### 2.4 from_outline 模式补全

如果 input_mode == from_outline：
- 跳过 Architect 调用
- 读取用户提供的 planning/outline.md
- 自动生成 dependency_graph.yaml（从模板默认值）
- 自动生成 claim_registry.md（从 outline 中提取核心论点）
- 自动生成 material_mapping.md（如果 materials/ 存在则映射，否则标记为空）

### 2.5 from_draft 模式补全

如果 input_mode == from_draft：
- 跳过 Architect 和 Writer
- 读取 sections/ 下已有章节
- 自动生成 claim_registry.md（从各章节文本中提取核心论点）
- 使用模板默认 dependency_graph

补全完成后，若项目启用了风格对齐，先执行风格对齐 pass 再进入审阅
（与 §1.3 from_draft 分支的增补一致，两处描述同一子流程）：

```
IF runtime_ctx.style_profile 存在 AND runtime_ctx.style_alignment == true:
    # 风格对齐 pass：入环前先把草稿重写到画像语体，再走正常审阅
    FOR section IN 已存在章节（delivery 范围内；未配置 delivery 则全量，按 section.name 对齐）:
        按 §8.3 模板调用 Revision(mode=style_align, 注入画像路径)
        # Revision 在 change_log 标注「全维度复审必需: 是」
    对齐后所有章节 status=reviewing、current_round=1（write_scores 原子写）
    # 注意：此 pass 的产出必须完整走内环 R1-R3 与外环 R4-R7，不得沿用对齐前评分
```

---

## 3. 阶段 2：章节写作-审阅循环（内环）

读取 planning/dependency_graph.yaml，按拓扑排序得到章节执行顺序（priority 值从小到大，同 priority 的章节可并行处理但为简化实现按顺序执行）。

### 3.1 章节迭代主循环

```
FOR 每个章节 section（按拓扑序）:
  IF scores.yaml 中 section.status == "approved": SKIP
  IF scores.yaml 中 section.status == "human_needed": SKIP

  ### 写作阶段
  IF section.manual == true OR section.writer is null:
    # 手动填写章节（如指南方向/工作条件/其他说明），或该模板暂缺自动 Writer 的章节——跳过自动写作，
    # 直接进入完备性门检查（该门本身已对 section.manual==true 的章节豁免；writer 为 null 但未标 manual
    # 的章节仍会被完备性门检查到"文件缺失"，提示人工补齐——这是有意为之，不豁免校验，只是不尝试自动生成）
    跳过本节的 Writer 调用与审阅-修改循环，直接标记 section.status → "approved"（若文件已由人工预先提供且非空）
    或保持 section.status == "pending"（若文件尚不存在，留给完备性门在外环前拦截并提示人工补齐）
    CONTINUE   # 跳到 FOR 循环下一个章节
  IF input_mode == "from_draft" AND sections/{section.file} 已存在:
    跳过 Writer，直接进入审阅
  ELSE:
    更新 scores.yaml: section.status → "writing"; scores.phase → "section_writing"（write_scores 原子写）
    # 先落 writing 状态再调用 Writer：一旦 Writer 阶段崩溃，1.2 恢复时见到 status==writing
    # 会判定"上次写作未完成"并只重写本节，不影响其他已完成章节
    执行上下文压缩（Section 6.1）：为已完成章节生成摘要
    按 Section 8.1 模板构造 Writer prompt（含编排器注入的本节落盘文件名 {section_file}）
    通过 Agent 工具调用对应 Writer Agent
    验证 sections/{section.file} 存在且非空
    IF 验证失败 → 重试（最多 2 次）→ 仍失败则标记 human_needed
  更新 scores.yaml: section.status → "reviewing"; scores.phase → "section_review"（write_scores 原子写）
  # 顶层 phase 与 section.status 同步推进：使崩溃后 1.2 能精确恢复到审阅子阶段，而非退回 Writer 重跑

  ### 审阅-修改循环
  FOR round = (section.current_round IF section.current_round >= 1 ELSE 1) TO convergence.max_section_rounds:
    # 起始值：首次进入本循环时 section.current_round 是 init 时的默认值 0，回落到从 1 开始；
    # 若是 1.2 恢复分支（case "reviewing"/"revising"）重入本循环，section.current_round 已被
    # 上一次崩溃前的本段代码持久化为具体轮次，据此续跑，不会从第 1 轮重新调用 Reviewer
    更新 scores.yaml: section.current_round → round（write_scores 原子写）
    # 循环体首行即落盘本轮轮次：即便本轮内 R1/R2/R3 或后续步骤中途崩溃，section.current_round
    # 也已经是最新值，1.2 的恢复选择器据此续跑正确的轮次，不依赖仅在其他分支收尾时才写入

    # 并行调用 3 个章节级 Reviewer
    按 Section 8.2 模板构造 R1、R2、R3 的 prompt
    通过 3 个并行 Agent 调用发出审阅请求
    等待全部返回

    # 保存审阅报告
    将 R1 输出写入 reviews/round_{round}/{section编号}_{section名}_R1.md
    将 R2 输出写入 reviews/round_{round}/{section编号}_{section名}_R2.md
    将 R3 输出写入 reviews/round_{round}/{section编号}_{section名}_R3.md

    # V3: 校验审阅报告格式
    for report_path in [R1_path, R2_path, R3_path]:
        result = Bash(f"python3 {SCRIPTS}/validate.py review_report {report_path} --format json")
        if result.valid == false:
            if retry_count < 2: 重新调用该 Reviewer
            else: 使用 critical_threshold 作为该维度分数，记录到 change_logs/errors.md

    # 解析评分（§5.4a）：从每份审阅报告提取 Checklist 评分表格，
    # 按 §5.1 聚合出 logic/de_ai/completeness 三维分，收集本轮标红条目为 flagged（dict 形态，携带 severity）：
    # critical 短路条目 → {"id": ID, "severity": "critical", "score": 分数}；
    # major 标记条目 → {"id": ID, "severity": "major", "score": 分数}。两类条目在同一个 flagged 列表里
    # 混合传给 aggregate.py（旧的纯 ID 字符串形态默认按 critical 处理，仍兼容，但本次改动后建议统一用
    # 带 severity 的 dict 形态，便于审计追溯）
    # 评分聚合（§5.2，脚本为准，禁止心算）：调用 aggregate.py 得 weighted 与 approved
    agg = Bash("python3 {SCRIPTS}/aggregate.py --scope inner "
               "--logic {logic} --de-ai {de_ai} --completeness {completeness} "
               "--flagged '{flagged_json}' --config config.yaml")   # 解析见 §5.4b
    # agg = {"weighted","approved","reason","critical_count","major_count"}

    # 判定（直接采信脚本的 approved，等价于 weighted ≥ section_score_threshold）
    IF agg.approved == true:
      更新 scores.yaml: section.status → "approved"
      更新 scores.yaml: section.current_score → agg.weighted
      更新 scores.yaml: section.rounds_used → round
      更新 scores.yaml: section.current_round → round
      记录各 reviewer 维度分到 section.last_reviewer_scores
      section.content_sha256 = Bash("shasum -a 256 sections/{section.file}").split()[0]
      # 评分时刻的正文指纹（随上述字段一并 write_scores 原子写；导出门禁 §4.2 用——
      # 导出前重算指纹与此值不一致即判定评分失效，回内环重审）
      BREAK

    IF round == convergence.max_section_rounds:
      更新 scores.yaml: section.status → "human_needed"
      更新 scores.yaml: section.current_round → round
      记录诊断信息：agg.reason + 列出所有未通过的 checklist 项（分数 < 60 的 critical 项 + 分数 < 70 的 high 项）
      BREAK

    # 修改
    更新 scores.yaml: section.status → "revising", section.current_round → round; scores.phase → "revision"（write_scores 原子写）
    # 顶层 phase 推进为 revision：这是全流程唯一给 phase 赋值 revision 之处，
    # 使 1.2 的 case revision 分支真正可达，并能精确续跑本轮 Revision 后再审
    按 Section 8.3 模板构造 Revision Agent prompt（合并 R1+R2+R3 的修改建议）
    通过 Agent 工具调用 Revision Agent
    验证修改后章节存在且 change_log 已写入

    # 篇幅代跑与压缩/扩写（P1-4）：revision 子 agent 的 allowed-tools 无 Bash，无法自查字数，
    # 故由【有 Bash 的编排器】代跑 count_words.py，对照模板 length_management.section_targets。
    # 以 section_targets 为唯一真源（模板 > writer 自估），按 section.name 对齐取 chars 区间。
    stat = Bash("python3 {SCRIPTS}/count_words.py sections/{section.file}")
    target = length_management.section_targets[section.name]   # 已深度合并的模板配置（§1.1）
    IF target 存在 AND target.chars 存在:
      metric = target.metric IF target.metric 存在 ELSE "total_chars"   # 按目标声明的统计口径比较，缺省 total_chars
      IF stat[metric] > target.chars[1]:     # 超预算 → 按 compress.priority 压缩
        FOR c = 1 TO length_management.compress.max_rounds:
          调用 Revision Agent（压缩指令：删冗余/合并/精简，保 compress.preserve 项）
          stat = Bash("python3 {SCRIPTS}/count_words.py sections/{section.file}")
          IF stat[metric] ≤ target.chars[1]: BREAK
      ELIF stat[metric] < target.chars[0]:   # 欠预算 → 按 expand.priority 扩写
        FOR c = 1 TO length_management.expand.max_rounds:
          调用 Revision Agent（扩写指令：补细节/文献/机制，避 expand.avoid 注水）
          stat = Bash("python3 {SCRIPTS}/count_words.py sections/{section.file}")
          IF stat[metric] ≥ target.chars[0]: BREAK
      # 达 max_rounds 仍超/欠：记录到 change_logs/，交由下一轮审阅/前置门（§4.1 完备性门）处置，不在此阻塞

    更新 scores.yaml: section.status → "reviewing", section.rounds_used → round, section.current_round → round; scores.phase → "section_review"（write_scores 原子写）
  END FOR

END FOR
```

### 3.2 内环完成后

所有章节处理完毕后：
- 检查是否有 status == "human_needed" 的章节
  - 有 → 暂停，提示用户哪些章节需要人工介入，等待用户处理后继续
  - 无 → 更新 scores.yaml: phase → "global_review", global_round → 1，进入阶段 3

---

## 4. 阶段 3：全文验证-修改循环（外环）

### 4.1 外环主循环

```
FOR round = scores.global_round TO convergence.max_global_rounds:
  # 起始边界读自持久化的 scores.global_round（1-based，见 §1.2 初始化块），
  # 使崩溃重启后外环从已完成的轮次续跑，而非每次都从第 1 轮重新开始

  ### 上下文压缩
  执行 Section 6.2 的全文压缩策略：
  为每个章节生成 500 字压缩版

  ### 全文级审阅
  确定本轮需要运行的 Reviewer（审阅对象为 delivery 范围内章节；未配置 delivery 则全量，按 section.name 对齐）：
  - 必跑：R4（一致性）、R5（叙事）、R7（格式）
  - 条件触发 R6（可行性）：检查 change_logs/ 中最近一轮是否涉及「研究方案」或「可行性分析」

  定期全文一致性检查：
  IF round % convergence.full_consistency_check_interval == 0:
    R4 使用全文原文而非压缩版（强制全面检查）

  # R7 脚本代跑注入（P1-4）：R7 的 allowed-tools 无 Bash，无法自跑脚本，
  # 由【有 Bash 的编排器】在调用 R7 前统一代跑四个检查脚本，把 JSON 结果注入 R7 prompt（§8.2）。
  IF 本轮需运行 R7:
    fmt_words = Bash("python3 {SCRIPTS}/count_words.py sections/")      # {chinese_chars,...,total_chars,estimated_pages}
    fmt_head  = Bash("python3 {SCRIPTS}/check_format.py sections/")     # {heading_structure,issues,page_estimate,checked_files}
    fmt_ref   = Bash("python3 {SCRIPTS}/check_references.py sections/ --citation-style {runtime_ctx.citation_style}")
              # {citation_count,citations,year_distribution,citation_style,foreign_style_count,foreign_style_samples}
              # --citation-style 取 runtime_ctx（config > 模板 > 缺省 numbered）；
              # foreign_style_count > 0 表示疑似混入对方制式引文（保守过滤后的漂移信号，
              # 样例见 foreign_style_samples；导出门禁 §4.2 亦会核查拦截）
    fmt_xref  = Bash("python3 {SCRIPTS}/check_cross_refs.py sections/") # {文件: [被引文件…]} 交叉引用图
    fmt_pages = 模板深度合并（extends）后的 {total_pages_warning, total_pages_hard_limit}
              # 页数红线注入（与四份脚本 JSON 并列）：R7 无 Bash 也不自行读模板做继承合并，
              # 红线数值由编排器从模板 length_management 取出后随 prompt 注入；null=无硬限
    # 任一脚本退出码≠0 → 按 Section 7.3 记录并继续（该项由 R7 的 LLM 部分兜底），不阻塞

  并行调用需要运行的 Reviewer（按 Section 8.2 的全文级模板；R7 prompt 注入上面四份脚本 JSON）
  保存审阅报告到 reviews/round_{round}/global_R{N}.md

  ### 评分聚合（§5.3，脚本为准，禁止心算）
  从各全文级报告解析 consistency/narrative/feasibility/format 四维分，并按 §5.4a 收集本轮标红条目为
  flagged（dict 形态，携带 severity）：critical 短路条目 → {"id": ID, "severity": "critical", "score": 分数}；
  major 标记条目 → {"id": ID, "severity": "major", "score": 分数}。两类条目在同一个 flagged 列表里混合传给
  aggregate.py（旧的纯 ID 字符串形态默认按 critical 处理，仍兼容，但本次改动后建议统一用带 severity 的 dict
  形态，便于审计追溯）
  R6 未运行时按 §5.3 规则准备 feasibility 入参（用历史分，或首轮未触发则用重归一化 --config）
  agg = Bash("python3 {SCRIPTS}/aggregate.py --scope global "
             "--consistency {c} --narrative {n} --feasibility {f} --format {fmt} "
             "--flagged '{flagged_json}' --config config.yaml")   # 解析见 §5.4b
  prev_global = scores.global_scores[-1] IF scores.global_scores 非空 ELSE null
             # 必须在下面 append 本轮记录之前读取，否则「上一轮」会被本轮自己覆盖，
             # 导致下方§分数回退检测把本轮与自己比较（见该处说明）
  向 scores.yaml 顶层 global_scores 数组 append 一条 {round: round, consistency: {c}, narrative: {n},
             feasibility: {f}, format: {fmt}, weighted: agg.weighted, flagged: flagged}（write_scores 原子写）
  更新 change_history: 记录 agg.critical_count / agg.major_count / 本轮 minor 数量

  ### 收敛判定（直接采信 aggregate.py 的 approved）
  # 脚本的 approved 已内建 A∧B：weighted ≥ global_threshold 且 critical_count==0 且 major_count ≤ max_major
  条件 A: agg.weighted ≥ convergence.global_score_threshold          # 文档口径，实际由脚本判
  条件 B: agg.critical_count == 0 AND agg.major_count ≤ convergence.max_major_issues

  IF agg.approved == true:            # ≡ A AND B
    # ── 置 completed 前的两道前置门（P1-1 章节完备性 / P1-2 渲染回填）──
    # 任一不过一律拒绝 completed、改判 human_needed，杜绝"半成品宣告通过"
    # （如 6/12 章仍是空壳、或正文题注对不上嵌图却静默导出无图 docx）

    ### 前置门 1：章节完备性门（P1-1）
    # 遍历模板 sections 里所有【非 manual】且在 delivery 范围内（未配置 delivery 则全量）的章节，
    # 逐一核验：落盘文件已存在、非空、并达到字数下限
    problem_sections = []
    length_management = 已深度合并模板的 length_management（见 Section 1.1）
    FOR section IN runtime_ctx.sections:
      IF section.manual == true:                       # 手动填写章节（如指南方向/工作条件/其他说明）不纳入完备性门
        CONTINUE
      IF runtime_ctx.delivery 存在 AND section.name NOT IN runtime_ctx.delivery.sections:
        CONTINUE                                       # 部分交付：delivery 范围外章节不纳入完备性门
      path = f"sections/{section.file}"                # 以模板 section.file 为落盘真源，不按章节名反推
      IF NOT file_exists(path):
        problem_sections.append({file: section.file, name: section.name, reason: "文件缺失"})
        CONTINUE
      stat = Bash(f"python3 {SCRIPTS}/count_words.py {path}")   # 输出 {chinese_chars,english_words,total_chars,estimated_pages}
      IF stat.error OR stat.total_chars == 0:          # 文件存在但无正文（空壳/仅空白）
        problem_sections.append({file: section.file, name: section.name, reason: "空壳（无正文内容）"})
        CONTINUE
      # 字数下限：仅当 length_management.section_targets 为本节配置了 chars 时才校验
      target = length_management.section_targets[section.name]   # 按 section.name 对齐；无配置则跳过下限校验
      IF target 存在 AND target.chars 存在:
        metric = target.metric IF target.metric 存在 ELSE "total_chars"
        min_chars = target.chars[0]                    # chars 区间下界即字数下限
        IF stat[metric] < min_chars:
          problem_sections.append({file: section.file, name: section.name,
                                   reason: f"字数不足（{stat[metric]} < 下限 {min_chars}）"})

    IF problem_sections 非空:
      更新 scores.yaml: phase → "gate_blocked"，blocker → {type: "completeness", problem_sections: problem_sections}（write_scores 原子写）
      输出：拒绝置 completed；逐条列出缺失/空壳/字数不足的问题章节，提示人工补齐后再续跑
      STOP

    ### 前置门 2：渲染回填（P1-2）
    # 完备性达标后、导出之前，先渲染 Mermaid 源图并回填正文占位锚点，再校验"题注数 > 嵌图数即拦截"
    result = Bash("python3 {SCRIPTS}/backfill_figures.py .")    # 项目目录即当前工作目录；成功 ok:true 退出码 0
    # 部分交付口径（与前置门 1 一致）：backfill 仍全项目执行（图源共享），但阻断判定
    # 只看 delivery 范围内章节——范围外草稿章节的缺图/题注不匹配仅输出 warning，不 gate_blocked
    IF runtime_ctx.delivery 存在:
      将 result.missing 与题注核对限定在 delivery 范围内章节文件；范围外缺图 → warning 逐条列出，不阻断
    IF result.ok != true OR result.caption_lines > result.embedded:  # 前者：存在未生成/未嵌入的图（锚点/markdown引用缺图）；
                                                               # 后者：ok=true 但仍有纯文本「图N…」题注未配图（backfill_figures.py 的 ok 不统计此类）
                                                               # （部分交付时两个条件均按上一步限定后的范围内数据判定）
      更新 scores.yaml: phase → "gate_blocked"，blocker → {type: "render_backfill", missing: result.missing, caption_lines: result.caption_lines, embedded: result.embedded}（write_scores 原子写）
      输出：题注与嵌图不匹配，逐条列出缺图；【不静默导出无图 docx】，提示人工补图后再续跑
      STOP

    # ── 两道前置门均通过 → 先进专家评审（P1-5），再置 completed ──
    # 收敛达标后、最终导出前，插入阶段4 专家评审模拟（把关性质，不再迭代改稿）。
    # expert_simulation 开关取自 pipeline 配置 settings.expert_simulation.enabled
    # （skills/pipeline/config.yaml，缺省 true）；下记为 config.expert_simulation.enabled。
    IF config.expert_simulation.enabled == true
       AND agg.weighted ≥ 85 AND agg.critical_count == 0
       AND agg.major_count ≤ convergence.max_major_issues:     # 达 R8 门槛（global≥85 且 critical=0、major≤2）
      更新 scores.yaml: phase → "expert_review"（write_scores 原子写）
      输出：外环已收敛且两道前置门通过，进入阶段4 专家评审模拟
      STOP    # 结束外环 → 进入 Section 4.3（阶段4 专家评审），4.3 完成后经 expert_review → completed
    ELSE:
      # 未启用专家评审 或 未达门槛 → 直接置完成
      更新 scores.yaml: phase → "completed"（write_scores 原子写）
      输出完成摘要：最终分数、总轮次、各维度分数趋势、token 消耗
      STOP    # 结束外环 → 进入 Section 4.2 输出阶段（导出 output/<项目名>.docx + V5 最终校验）

  IF round == convergence.max_global_rounds AND agg.approved != true:   # 即 NOT (A AND B)
    更新 scores.yaml: phase → "stalled"，blocker → {type: "convergence_exhausted", round: round,
                    weighted_trend: <各维度分数趋势数据>, failing_checklist: <反复不过的checklist项列表>}（write_scores 原子写）
    输出诊断报告：
      - 各维度分数趋势（每轮的分数变化）
      - 反复不过的 checklist 项列表
      - 卡住的原因分析
    STOP

  ### 分数回退检测
  IF round > 1:
    IF agg.weighted < prev_global.weighted:   # prev_global 即 scores.global_scores[-1]（append 本轮记录之前取到的上一轮值，见§评分聚合）
      下一轮强制全文重审：所有章节重新进入内环，不使用影响分析
      在 scores.yaml 中标注 force_full_recheck: true
      CONTINUE（跳过下面的增量重审，直接进入下一轮）

  ### 修改与影响分析
  合并 R4-R7 的审阅意见
  按 Section 8.3 模板调用 Revision Agent

  # 篇幅代跑与压缩/扩写（P1-4，外环）：每轮 revision 完成后，由编排器（有 Bash）代跑 count_words，
  # 对照模板 length_management.section_targets（以 section_targets 为唯一真源，模板 > writer）。
  # 对被本轮 Revision 改动的章节逐一核对 chars 区间：超上界→按 compress.priority 压缩、
  # 欠下界→按 expand.priority 扩写，各 ≤ 对应 max_rounds（与 §3.1 修改步骤同一策略）；
  # 达 max_rounds 仍不达标则记 change_logs/，交由本轮 R7 篇幅诊断与收敛前的完备性门（前置门1）处置。
  FOR section IN Revision 改动的章节:
    stat = Bash("python3 {SCRIPTS}/count_words.py sections/{section.file}")
    target = length_management.section_targets[section.name]
    IF target 存在 AND target.chars 存在:
      metric = target.metric IF target.metric 存在 ELSE "total_chars"   # 按目标声明的统计口径比较，缺省 total_chars
      IF stat[metric] > target.chars[1]: 触发压缩循环（≤ compress.max_rounds）
      ELIF stat[metric] < target.chars[0]: 触发扩写循环（≤ expand.max_rounds）

  # 脚本辅助交叉引用检测
  运行 {SCRIPTS}/check_cross_refs.py sections/ → 获取章节间引用关系图
  读取 Revision Agent 输出的 change_log

  确定受影响章节：
  1. change_log 中 Revision Agent 标注的受影响章节
  2. check_cross_refs 检测到的：如果被修改章节被其他章节引用，引用方自动标记为受影响
  3. 取两者的并集

  ### 增量重审
  只对受影响章节重新触发阶段 2 内环（Section 3）
  这些章节的 scores.yaml status 重置为 "reviewing"
  # 重置 reviewing 的同时清空该章 content_sha256（旧指纹对应对齐前/修改前的正文，
  # 保留会让导出门禁 §4.2 误判；重审通过后由 §3.1 评分落盘处重新写入新指纹）
  更新 scores.yaml: global_round → round + 1

END FOR
```

### 4.2 外环完成后的输出

#### 导出门禁清单（前置门 0）

任何一次最终导出（含 export_failed / completed 重入的原地重跑）都必须先过本清单，
再进入下方「最终导出」代码块。目的：拦截"评分之后正文又被改动（人工改稿、风格对齐、
任何来源）却沿用旧评分导出"的复审失效，以及引文制式漂移。

```
FOR section IN delivery 范围内非 manual 章节:     # 未配置 delivery 则全量，按 section.name 对齐
    actual = Bash("shasum -a 256 sections/{section.file}").split()[0]
    IF scores.sections[section.id].content_sha256 不存在:
        # 存量项目：评分产生于指纹机制引入之前，字段缺失 ≠ 正文被改——
        # 首次补录指纹并沿用既有评分，不得把老项目无差别打回内环重审
        scores.sections[section.id].content_sha256 = actual（write_scores 原子写）
        输出 warning："{section.file} 首次补录内容指纹，沿用既有评分"
    ELIF actual != scores.sections[section.id].content_sha256:
        # 记录指纹存在且不相等：正文在评分后被改动（人工/风格对齐/任何来源）——旧评分失效
        该章 status=reviewing，回内环重审；本次导出中止
IF 存在被重置为 reviewing 的章节:
    清空这些章节的 content_sha256；更新 scores.yaml: phase → "section_review"（write_scores 原子写）
    输出：逐条列出指纹不一致的章节（file + 记录指纹 + 实测指纹），提示重新运行 Pipeline 走内环重审
    STOP
IF runtime_ctx.citation_style 已配置:
    refs = Bash("python3 {SCRIPTS}/check_references.py sections/ --citation-style {runtime_ctx.citation_style}")
    IF refs.foreign_style_count > 0:
        # 命中 ≠ 必然漂移：脚本已做保守过滤，但政策文件、产品名等括注仍可能残余误报。
        # 编排器逐条核查 refs.foreign_style_samples（回到正文上下文判断是否真是引文）：
        IF 样例中存在真实的对方制式引文:
            记 Major 并中止导出（引文制式漂移，转 Revision 统一制式后重走门禁）
        ELSE:
            输出 warning：逐条列出误报样例及判定理由，放行导出
# R2/R5/R7 三个维度的最新评分必须产生于当前 content_sha256 之后——
# 由上面的指纹校验间接保证；任何维度「未复评」都不允许出现在导出前状态
```

#### 最终导出（P1-1，仅 phase == "completed" 时执行）

外环收敛（两道前置门均通过）后 phase 变为 completed —— 未启用专家评审时由 Section 4.1 直接置，
启用时经 Section 4.3 阶段4 专家评审后置 —— 在此统一完成 .docx 导出。
导出与 V5 校验绑定：只有 output/<项目名>.docx 成功生成，completed 才算真正交付；否则回退 export_failed。

```
IF scores.phase == "completed" OR scores.phase == "export_failed":
    # 后者是 case "export_failed" 重入时的原地重跑；两种 phase 走同一段导出逻辑
    # 缺省即继承默认样式模板 assets/nsfc_reference.docx（脚本按自身位置解析，不受 cwd 影响），
    # 输出到 <项目>/output/<项目名>.docx；如需覆盖样式可显式传 --reference-doc <path>
    IF runtime_ctx.delivery 存在:
        # 部分交付：只合并交付范围内章节——sections/ 下范围外的 .md（from_draft 项目
        # 的典型情形：其余章节以未审草稿形态存在）不得混入交付物
        delivery_files = delivery 范围内章节的 section.file 列表（按模板 sections 顺序，逗号拼接）
        result = Bash("python3 {SCRIPTS}/export_docx.py . --sections {delivery_files}")
        IF sections/ 下存在范围外 .md 文件:
            输出 warning：列出被排除的范围外文件（未审草稿，不入交付物）
    ELSE:
        result = Bash("python3 {SCRIPTS}/export_docx.py .")
    # 成功：{"ok": true, "output": ".../output/<项目名>.docx", "sections": N, "has_reference": true, "skipped": []}
    IF result.ok != true OR result.has_reference != true OR NOT file_exists(result.output):
        更新 scores.yaml: phase → "export_failed"，blocker → {type: "export_failed", reason: <具体失败原因>, export_result: result}（write_scores 原子写）
        输出：最终导出失败（未生成 output/*.docx 或未继承样式），需人工介入
    ELSE:
        IF runtime_ctx.delivery 存在:
            # 部分交付：导出物文件名加后缀，避免与全量交付物混淆
            将 result.output 重命名为 output/<项目名>_部分交付.docx（Bash mv）
            导出日志中列出本次交付章节清单（runtime_ctx.delivery.sections 逐项）
            记录重命名后的路径为最终交付 .docx 路径（含 sections=result.sections）
        ELSE:
            记录 result.output 为最终交付 .docx 路径（含 sections=result.sections）
```

#### V5 最终完整性校验

```
results = Bash("python3 {SCRIPTS}/validate.py all . --format json")
输出完整性报告（validate.py 各项仅作参考，不阻塞已完成的项目）

# 新增验收项（completed 项目必须满足；不满足则应按上面的最终导出逻辑回退 export_failed）：
- output/<项目名>.docx 已生成且非空（即最终导出 ok:true、has_reference:true、output 文件存在；
  配置了 delivery 的部分交付项目为 output/<项目名>_部分交付.docx）
```

无论以何种方式结束（completed / human_needed），都输出以下信息：
- 总运行轮次（内环总轮次 + 外环轮次）
- 各章节最终分数
- 全文各维度分数
- 累计 token 消耗（从 scores.yaml 的 token_usage 读取）
- 如果是 completed：导出的 .docx 文件路径（output/<项目名>.docx）；如运行过阶段4，附专家评审综合分与过会判断
- 如果是 human_needed：需要人工关注的具体问题列表（含空壳/字数不足章节、缺图清单、导出失败等前置门未过项）

### 4.3 阶段4：专家评审模拟（R8，P1-5）

**触发时机**：外环两道前置门均通过后（Section 4.1 已置 `phase="expert_review"` 并跳转至此），
在最终导出（Section 4.2）**之前**。这是收敛后的最终质量把关，**不再迭代改稿**。
断点恢复：Section 1.2 的 `case "expert_review"` 分支会重新进入本节（重跑幂等）。

**门槛**（Section 4.1 已判定，此处复用其结果，未达则不会进入本节而是直接置 completed）：
- `config.expert_simulation.enabled == true`
- `agg.weighted ≥ 85` 且 `agg.critical_count == 0` 且 `agg.major_count ≤ max_major_issues(≤2)`

```
### 阶段4 专家评审流程

1. 读取 R8 配置
   r8_cfg = Read("scholar-writing/skills/reviewer/R8_expert_sim/config.yaml")
   panel_count = clamp(config.expert_simulation.panel_count 或 r8_cfg.default_panel_count(3),
                       1, r8_cfg.max_panel_count(5))
   panel = 前 panel_count 个 enabled==true 的 r8_cfg.expert_profiles
   consensus_threshold = r8_cfg.aggregation.consensus_threshold   # 默认 0.60

2. 上下文准备（复用 Section 6.2 全文压缩）
   为每章生成 500 字压缩版 + 提供 sections/ 全文；project_type（面上/青年/重点）取自 config/template

3. 并行调用 R8（每位专家一个 Agent 调用，独立评审、互不影响）
   FOR expert IN panel:
     按 Section 8.5 模板构造 R8 prompt（注入 expert_profile=expert.id）
     通过 Agent 工具并行调用（subagent_type="general-purpose"，读取 R8 SKILL.md）
   等待全部返回
   各专家输出写入 reviews/expert_simulation/panel_{N}_{expert_id}_R8.md
   （六维打分 + critical/major/minor + 函评/会评过会判断；frontmatter: reviewer: R8 / dimension: expert_sim）

4. 聚合（以 expert_profile=aggregator 再次调用 R8）
   按 consensus_threshold 聚合跨专家共识与独立观点、综合六维分、综合过会判断
   写入 reviews/expert_simulation/aggregated_report.md（frontmatter 同上）

5. 校验 R8 报告 schema（复用 V3 的 review_report 校验）
   reports = glob("reviews/expert_simulation/panel_*_R8.md") + ["reviews/expert_simulation/aggregated_report.md"]
   FOR report IN reports:                          # panel_*_R8.md 亦被 V5 的 reviews/**/*_R*.md 命中
     res = Bash(f"python3 {SCRIPTS}/validate.py review_report {report} --format json")
     # frontmatter(reviewer: R8, dimension: expert_sim) 命中 review_report.schema 全局分支（reviewer ^R[4-8]$），
     # 且 REVIEWER_DIMENSION_MAP[R8]=expert_sim 语义校验通过
     IF res.valid == false: 记录到 change_logs/errors.md（把关性质，不回退改稿、不阻塞导出）

6. 收尾：phase 经 expert_review → completed（write_scores 原子写）
   在 scores.yaml 记录 expert_simulation: { 综合六维分, 函评综合判断, 会评综合判断, critical/major 计数 }
   更新 scores.yaml: phase → "completed"
   输出专家评审摘要（综合分、函评/会评判断、critical 清单）
   → 进入 Section 4.2 输出阶段（最终导出 output/<项目名>.docx + V5）
```

说明：R8 为把关而非改稿环节——即便专家给出 critical/major，也不再自动触发内环修改；这些问题作为
交付附带的人工修订建议随 aggregated_report.md 一并呈现，由用户决定是否再手动开一轮。

---

## 5. 评分聚合逻辑

### 5.1 Checklist 条目 → Reviewer 维度分

每个 Reviewer 对其 checklist 中的每条 criterion 打分（0-100）。按 weight 加权聚合为该 Reviewer 的维度分：

- critical 权重 = 3
- high 权重 = 2
- medium 权重 = 1
- 维度分 = Σ(条目分 × 条目权重) / Σ(条目权重)

**Critical 短路规则**：任一 critical 条目分数 < critical_threshold（默认 60）时，该维度直接标红（flagged）。标红维度的处理：
1. 在审阅报告中显著标注
2. 章节/全文总分在加权聚合后额外扣减 10 分 —— 该扣减不由编排器心算，而是把标红条目 ID
   收入 flagged 列表传给 §5.2/§5.3 的 aggregate.py，由脚本统一施加 −10 并 clamp≥0
3. 修改建议中该 critical 条目标为最高优先级

**Major 标记规则**：任一 high 权重条目分数 < 70（阈值与 §3.1 内环 max_section_rounds 用尽时诊断"分数 < 70 的
high 项"一致）时，该条目标记为 major。标记为 major 的条目不触发 −10 惩罚（惩罚只对 critical 短路生效），但计入
major_count，用于外环收敛判据 B（`major_count ≤ max_major_issues`）与 R8 门槛判断。

### 5.2 章节级评分（内环，R1-R3）

**加权公式（作文档，计算以脚本为准）**：
```
section_score = logic_score × 0.40 + de_ai_score × 0.25 + completeness_score × 0.35

IF 任一维度被标红（§5.1 的 critical 短路）:
  section_score = max(section_score - 10, 0)

判定: section_score ≥ section_score_threshold → 通过
```

**计算以脚本为准（P2-1，必须）**：上面的公式仅作文档说明。**加权总分 `weighted` 与
通过判定 `approved` 一律调用确定性脚本 `python3 {SCRIPTS}/aggregate.py`
计算，禁止由 LLM 心算加权**——心算极易漏扣 critical 的 −10 惩罚、记错 0.40/0.25/0.35
权重或写错阈值（下方计算示例即为一例：心算得 77.0，脚本精确为 76.8）。脚本吃三项维度分
（由 §5.1 按 checklist 权重聚合得到）与 flagged 标红条目列表，一次性算出
`weighted / approved / critical_count / major_count / reason`。§5.1 定义的"标红后总分 −10"
即由脚本按 flagged 施加（clamp≥0），编排器不再另行扣分。

`flagged` 取 scores.yaml 中本轮记录的标红 checklist ID 列表（纯 ID 字符串默认按 critical
处理，如 `["C4"]`）；当某 critical 条目分数已知时也可传对象 `[{"id":"C4","severity":"critical","score":58}]`。
传 `--config config.yaml` 使脚本采用项目配置的权重/阈值（score_weights.section、
convergence.section_score_threshold、critical_threshold），而非内置默认值。

内环调用示例（scope=inner）：
```
result = Bash("python3 {SCRIPTS}/aggregate.py --scope inner "
              "--logic 76.4 --de-ai 81.3 --completeness 73.9 "
              "--flagged '[]' --config config.yaml")
# → {"weighted": 76.8, "approved": false,
#    "reason": "内环加权分 76.8 < 章节阈值 80，需进入修改",
#    "critical_count": 0, "major_count": 0}
# 若 C4 为 critical 且分数 < critical_threshold（标红），--flagged '["C4"]' → weighted 自动 −10、clamp≥0
```

**维度分来源示例（§5.1 → 脚本入参）**：
```
章节"立项依据"第 1 轮审阅：
  R1(Logic):       L1=85(high/2), L2=70(critical/3), L3=80(high/2)
                   → (85×2 + 70×3 + 80×2) / (2+3+2) = 76.4
                   → L2=70 ≥ 60 → 不触发短路
  R2(De-AI):       D1=90(medium/1), D2=75(high/2), D3=85(medium/1)
                   → (90×1 + 75×2 + 85×1) / (1+2+1) = 81.3
  R3(Completeness): C1=80(high/2), C2=65(critical/3), C3=90(medium/1), C4=70(critical/3)
                   → (80×2 + 65×3 + 90×1 + 70×3) / (2+3+1+3) = 73.9
                   → C2=65 ≥ 60, C4=70 ≥ 60 → 不触发短路，flagged=[]

  以 --logic 76.4 --de-ai 81.3 --completeness 73.9 --flagged '[]' 调用 aggregate.py（如上）
  → weighted=76.8 < section_score_threshold(80) → approved=false → 进入修改
```

### 5.3 全文级评分（外环，R4-R7）

**加权公式（作文档，计算以脚本为准）**：

**R6 运行时（正常情况）**：
```
global_score = consistency × 0.30 + narrative × 0.35 + feasibility × 0.20 + format × 0.15
```

**R6 未运行但有历史分数时**：
```
feasibility_score = 上一轮的 feasibility 分数
global_score = consistency × 0.30 + narrative × 0.35 + feasibility_score × 0.20 + format × 0.15
```

**R6 从未运行过（首轮即未触发）**：
```
重新归一化权重（排除 feasibility 的 0.20）：
  consistency: 0.30 / 0.80 = 0.375
  narrative:   0.35 / 0.80 = 0.4375
  format:      0.15 / 0.80 = 0.1875
global_score = consistency × 0.375 + narrative × 0.4375 + format × 0.1875
```

如果任一维度被标红：global_score = max(global_score - 10, 0)

**计算以脚本为准（P2-1，必须）**：同 §5.2，外环的 `weighted` 与 `approved` 也一律调用
`python3 {SCRIPTS}/aggregate.py --scope global`，**不得 LLM 心算**。外环脚本除加权外
还内建了收敛判据——`approved` 当且仅当 `weighted ≥ global_threshold 且 critical_count==0
且 major_count ≤ max_major`，正好等价于 §4.1 的收敛条件 A∧B，编排器直接采信脚本的 `approved`
与 `critical_count/major_count`，无需再手工判 A/B（详见 §4.1 评分聚合/收敛判定）。

外环调用示例（scope=global，正常/有历史两种情形均直接传四维分）：
```
result = Bash("python3 {SCRIPTS}/aggregate.py --scope global "
              "--consistency 97 --narrative 82 --feasibility 85.2 --format 71.0 "
              "--flagged '[]' --config config.yaml")
# → {"weighted": 85.5, "approved": true,
#    "reason": "外环加权分 85.5 ≥ 全文阈值 85，且 critical=0、major=0≤2，通过",
#    "critical_count": 0, "major_count": 0}
# R6 未运行但有历史：feasibility 传"上一轮的 feasibility 分数"，其余同上。
```

**R6 从未运行过（首轮即未触发）用脚本表达重归一化**：脚本要求四维齐全且权重和=1.0，
故编排器写一份临时权重 config（feasibility 权重置 0，其余按上式归一化），feasibility 分数随意
传（乘 0 无影响）：
```
# renorm.yaml:
#   score_weights:
#     global: { consistency: 0.375, narrative: 0.4375, feasibility: 0.0, format: 0.1875 }
#   convergence: { global_score_threshold: 85, max_major_issues: 2 }
#   critical_threshold: 60
result = Bash("python3 {SCRIPTS}/aggregate.py --scope global "
              "--consistency 90 --narrative 80 --feasibility 0 --format 70 "
              "--flagged '[]' --config renorm.yaml")
# → weighted = 90×0.375 + 80×0.4375 + 0 + 70×0.1875 = 81.9（feasibility 因权重 0 不计）
```
标红惩罚（§5.1 的 −10、clamp≥0）同样由脚本按 `--flagged` 施加，编排器不再另扣。

### 5.4 评分解析

分两层：**（a）从审阅报告解析维度分与标红条目 →（b）交 aggregate.py 得 weighted/approved**。

**（a）从 Reviewer 的审阅报告中提取评分表格**。预期格式：
```
| ID | Criterion | Score | Justification |
```
解析每行的 ID 和 Score 字段，按 §5.1 聚合为各 Reviewer 的维度分；并收集本轮标红条目为
flagged 列表（dict 形态，携带 severity）：critical 短路条目（分数 < critical_threshold）→
{"id": ID, "severity": "critical", "score": 分数}；major 标记条目（high 权重且分数 < 70，见 §5.1
「Major 标记规则」）→ {"id": ID, "severity": "major", "score": 分数}。两类条目在同一个 flagged 列表
里混合传给 aggregate.py（旧的纯 ID 字符串形态默认按 critical 处理，仍兼容，但本次改动后建议统一用
带 severity 的 dict 形态，便于审计追溯）。如果表格解析失败 → 触发 Section 7 的错误处理流程。

**（b）解析 aggregate.py 的输出**。§5.2/§5.3 的脚本调用成功时（退出码 0）打印一行 JSON：
```
{"weighted": float, "approved": bool, "reason": str, "critical_count": int, "major_count": int}
```
编排器直接读取：`weighted` 作为本轮加权总分、`approved` 作为通过/收敛判定、
`critical_count/major_count` 用于外环 critical=0 且 major≤上限的记录与诊断，`reason` 写入日志。
若脚本失败（退出码 1，打印 `{"error": ...}`）→ 记录到 change_logs/errors.md 并按 Section 7.3
脚本失败流程处理（不静默把 error 当成分数）。

---

## 6. 上下文预算管理

为防止后期 agent 上下文溢出，对每类 agent 的输入实施压缩策略。

### 6.1 Section Writer 的输入压缩

为每个已完成章节生成 200-300 字摘要，作为后续 Writer 的参考上下文：
- 在主会话中直接执行摘要生成（不需要独立 agent）
- 读取 sections/章节名.md → 提取核心论点和关键数据 → 生成摘要
- 存入 sections/summaries/章节名_summary.md
- Writer Agent 接收的前序章节上下文只包含这些摘要，不包含全文

**预算估算**：
- 章节大纲 ≈ 1K token
- Checklist ≈ 2K token
- 前序章节摘要（最多 6 章 × 300字）≈ 3K token
- 素材片段 ≈ 3-5K token
- claim_registry ≈ 2K token
- **总计 ≈ 11-13K token**，在 sub-agent 上下文窗口内可控

### 6.2 Global Reviewer 的输入压缩

在调用全文级 Reviewer（R4-R7）之前，主会话执行以下压缩步骤：
- 对每个章节生成 500 字压缩版，存入 sections/summaries/章节名_compressed.md
- 被影响分析标记为"重点关注"的章节传递原文，其余传递压缩版
- R4（一致性）额外接收完整的 claim_registry.md
- R7（格式）主要依赖脚本输出，LLM 只处理脚本无法覆盖的部分

**预算估算**：
- 全文压缩版（7 章 × 500字）≈ 6K token
- 重点章节原文（1-2 章）≈ 5K token
- Checklist ≈ 2K token
- claim_registry ≈ 2K token
- **总计 ≈ 15-17K token**，在 sub-agent 上下文窗口内可控

### 6.3 溢出降级策略

如果实际输入超出预算（Agent 调用返回截断或异常）：
1. 前序章节摘要缩减到 100 字/章
2. 全文压缩版缩减到 300 字/章
3. 素材片段只保留 material_mapping 中标注为"关键"的部分

---

## 7. 错误处理

### 7.1 Writer 产出异常

**检测**：调用 Writer Agent 后，检查 sections/{章节}.md 是否存在且非空
**恢复**：
1. 重新调用 Writer Agent（最多重试 2 次）
2. 仍失败 → 更新 scores.yaml 该章节 status → "human_needed"
3. 记录错误到 change_logs/errors.md：时间、章节名、错误描述

### 7.2 Reviewer 评分解析失败

**检测**：审阅报告中未找到预期的评分表格格式（| ID | Criterion | Score | Justification |）
**恢复**：
1. 重新调用 Reviewer（新鲜上下文，最多重试 2 次）
2. 仍失败 → 该维度使用上一轮分数
3. 首轮即解析失败 → 该维度使用 critical_threshold（默认 60）作为默认分
4. 记录到 change_logs/errors.md

### 7.3 脚本执行失败

**检测**：Python 脚本（count_words.py、check_format.py 等）退出码 ≠ 0
**恢复**：
1. 记录错误到 change_logs/errors.md
2. 跳过该检查项，在 scores.yaml 中标注 script_error: true
3. 不阻塞整体流程

### 7.4 外环分数震荡

**检测**：连续 2 轮全文总分变化 < 2 分且未达 global_score_threshold
**恢复**：
1. 更新 scores.yaml: phase → "human_needed"
2. 输出诊断报告：
   - 每个维度的分数趋势（过去各轮的分数列表）
   - 反复不过的 checklist 项（连续 2 轮分数 < 60 的条目）
   - 可能的卡点原因分析

### 7.5 上下文窗口溢出

**检测**：Agent 调用返回截断信号或异常错误
**恢复**：
1. 启用更激进的摘要策略：
   - 前序章节摘要缩减到 100 字/章
   - 全文压缩版缩减到 300 字/章
   - 素材片段只保留 material_mapping 中标注为"关键"的部分
2. 以降级模式重试 Agent 调用
3. 仍失败 → 标记 human_needed

### 7.6 Token 使用追踪

每次 Agent 调用后，更新 scores.yaml 中的 token_usage 字段：

```yaml
token_usage:
  total_input: 0
  total_output: 0
  by_agent:
    architect: { input: 0, output: 0, calls: 0 }
    writer: { input: 0, output: 0, calls: 0 }
    reviewer: { input: 0, output: 0, calls: 0 }
    revision: { input: 0, output: 0, calls: 0 }
```

注意：实际 token 数可能无法精确获取（取决于 Claude Code API 的返回信息）。如果无法获取，记录调用次数作为替代指标。

### 7.7 所有错误的统一日志

所有错误和异常记录到 change_logs/errors.md，格式：
```
## [时间戳] [错误类型]
- 章节/阶段：{位置}
- 错误描述：{描述}
- 恢复策略：{采取的措施}
- 结果：{成功/仍失败}
```

---

## 8. Agent 调用模板

以下是编排器调用各类 agent 时的 prompt 构造模板。

### 8.1 调用 Writer Agent

对于每个章节，按以下模板构造 Writer 的 prompt：

```
你的任务是撰写国自然申报书的「{section.name}」部分。

## 本节落盘文件名（必须严格写入此文件，勿自行编造编号或文件名）
{section_file}
（由编排器注入 = 当前所用模板 sections[].file 的值，如 06_特色与创新.md，不含 sections/ 前缀）

## 章节大纲
{从 planning/outline.md 中提取该章节的大纲部分}

## 评审标准（写作时请对照，你将被这些标准审阅）
{读取 section.checklist 字段所指向的 checklist 文件全文；section.checklist 是模板声明的
 该章节 checklist 真源路径，如 checklists/06_创新点.yaml，联合基金专属章节可能是
 checklists/联合基金/07_年度计划.yaml。不要按章节名硬编码 checklists/{章节名}.yaml}

## 前序章节摘要（保持上下文连贯）
{从 sections/summaries/ 读取已完成章节的摘要，按依赖顺序排列}

## 相关素材
{从 planning/material_mapping.md 中提取该章节对应的素材内容}

## 论点注册表（保持核心论点表述一致）
{planning/claim_registry.md 全文}

{若 runtime_ctx.style_profile 非空，编排器在此注入一行：`风格画像: {style_profile 绝对路径}，写作前必须 Read`}

请将完成的章节写入 `sections/{section_file}`（{section_file} 为不含路径的裸文件名）
```

通过 Agent 工具调用：
- subagent_type: "general-purpose"
- Writer skill 按当前 section.writer 字段确定（模板声明的该章节写作 skill 真源，如
  writer/nsfc/创新点），读取该 skill 的 SKILL.md 内容与上述 prompt 合并为完整指令；
  不要按章节名硬编码 writer 路径。
- 编排器负责把 section.file 的值作为 {section_file} 注入 prompt（writer skill 自身已改为
  占位、outputs.path 依赖注入，不含硬编码落盘文件名，见 CONVENTIONS_ZH.md 第一节）

### 8.2 调用 Reviewer Agent（两步法）

章节级审阅时，并行调用 R1 + R2 + R3。每个 Reviewer 的 prompt 模板：

```
请对以下章节进行{审阅维度}审阅。

## 待审阅章节
{sections/章节名.md 的完整文本}

## 评审标准
{从 checklist 中提取该 Reviewer 对应维度的条目}

## 审阅流程（严格遵循两步法）

### 第一步：自由分析
通读全文，从{维度}角度自由分析。不看 checklist，不限格式，充分推理。

### 第二步：对照 Checklist 评分
对照上述评审标准，逐条打分（0-100）。输出格式：

| ID | Criterion | Score | Justification |
|----|-----------|-------|---------------|

### 第三步：修改建议
按严重级别排序输出：
- [Critical] ...
- [Major] ...
- [Minor] ...
```

全文级审阅（R4-R7）的 prompt 类似，但输入替换为全文压缩版 + 重点章节原文。

**风格画像注入（R2/R5）**：若 runtime_ctx.style_profile 非空，编排器在 R2（章节级去 AI 味）与
R5（全文级叙事）的 prompt 中注入一行：`风格画像: {style_profile 绝对路径}，审阅前必须 Read`——
两者审阅时以画像为风格真值（如画像 §4 程式句式白名单不计入 AI 痕迹），画像规则优先级高于
STYLE_GUIDE_ZH.md / DEAI_PATTERNS_ZH.md 的一般性规定。

**R7（格式）的脚本代跑注入（P1-4）**：R7 的 allowed-tools 无 Bash，无法自行运行脚本，故其 prompt
由编排器在 §4.1「R7 脚本代跑注入」处代跑后追加以下四份 JSON 结果（R7 SKILL 已声明"你将收到脚本
的检查结果（JSON 格式）"，与此对接）：
```
## 脚本检查结果（由编排器代跑注入，勿自行调用脚本）
### count_words.py sections/
{fmt_words JSON}          # {chinese_chars, english_words, total_chars, estimated_pages}
### check_format.py sections/
{fmt_head JSON}           # {heading_structure, issues, page_estimate, checked_files}
### check_references.py sections/ --citation-style {runtime_ctx.citation_style}
{fmt_ref JSON}            # {citation_count, citations, year_distribution, citation_style, foreign_style_count, foreign_style_samples}
### check_cross_refs.py sections/
{fmt_xref JSON}           # {文件: [被引文件…]} 交叉引用图
### 页数红线（模板 length_management，extends 深度合并后）
{fmt_pages JSON}          # {total_pages_warning, total_pages_hard_limit}；null=无硬限，仅建议性提示
```
其中 count_words 结果供 R7 对照模板 length_management.section_targets 做篇幅诊断
（以 section_targets 为准，模板 > writer）。若某节 section_targets 配置了 metric 字段，
应按该字段对应的统计量（如 chinese_chars）判断是否超/欠预算，而非默认用 total_chars；
缺省未配置 metric 时才用 total_chars。

调用方式：3 个章节级 Reviewer 通过 3 个并行 Agent 调用。

### 8.3 调用 Revision Agent

```
请修改「{章节名}」章节。

## 原文
{sections/章节名.md 的完整文本}

## 审阅意见（按严重级别排序：critical → major → minor）
{合并该章节所有 Reviewer 的审阅报告}

## 论点注册表
{planning/claim_registry.md}

请完成以下任务：
1. 按审阅意见逐条修改章节，将修改后内容写入 sections/{章节名}.md
2. 将修改记录写入 change_logs/round_{N}_changes.md，每条包含：
   - 修改位置（章节名 + 段落位置）
   - 修改内容摘要
   - 对应的审阅意见 ID
   - 受影响的其他章节列表及原因
3. 如果修改涉及 claim_registry 中的核心论点，同时更新 planning/claim_registry.md
```

**mode 与画像路径参数（风格对齐 pass 专用）**：常规修订不传 mode，保持 revision SKILL 的
"保守修改"契约。仅 §2.5/§1.3 的风格对齐 pass 调用本模板时，编排器额外传入两项：
- `mode: style_align` —— 触发 revision SKILL 的「风格对齐模式(style_align)」（唯一允许突破
  保守修改契约的修订形态；审阅意见段替换为画像对照要求）；
- 注入一行 `风格画像: {style_profile 绝对路径}，修改前必须 Read`。

该模式下 Revision 的 change_log 以 `SA-画像§<节名>` 标注意见来源，并在末尾写明
「全维度复审必需: 是」——编排器据此让该章完整重走内环 R1-R3 与外环 R4-R7（见 §2.5）。

### 8.4 审阅报告存储

每轮审阅的报告存储路径：
- 章节级：reviews/round_{N}/{章节编号}_{章节名}_R{1,2,3}.md
- 全文级：reviews/round_{N}/global_R{4,5,6,7}.md
- 专家评审（阶段4，round 结构之外）：
  - 单专家：reviews/expert_simulation/panel_{N}_{expert_id}_R8.md
  - 聚合报告：reviews/expert_simulation/aggregated_report.md
  （两者 frontmatter 均为 reviewer: R8 / dimension: expert_sim，可过 review_report.schema 全局分支）

### 8.5 调用 R8 专家评审 Agent（阶段4，P1-5）

由 Section 4.3 在外环收敛后调用。每位专家一次 Agent 调用（并行、独立），聚合再单独调用一次。

```
你现在扮演国自然申报书评审专家，profile = {expert_profile}
（取自 R8 config.expert_profiles 的某一项 id，如 innovation_expert / methodology_expert /
 critical_reviewer；聚合阶段传 expert_profile = aggregator）。

## 项目类型
{project_type 与预算画像：面上 50-60万 / 青年 30-40万 / 重点 200-300万，用于资助额度约束识别}

## 全文（压缩版 + 重点章节原文）
{Section 6.2 生成的每章 500 字压缩版；必要章节附原文}

## 你的任务（遵循 R8 SKILL.md 两步法）
- 单专家：六维打分（创新性/科学假说/方案可行性/研究基础/团队/预期成果）+ critical/major/minor 问题清单
  + 函评与会评二值过会判断；写入 reviews/expert_simulation/panel_{N}_{expert_id}_R8.md
- 聚合（aggregator）：按 consensus_threshold(0.60) 汇总共识/独立观点、综合六维分与过会判断；
  写入 reviews/expert_simulation/aggregated_report.md

## 输出必须以 YAML frontmatter 开头（供 review_report.schema 校验）
---
reviewer: R8
dimension: expert_sim
---
```

调用方式：subagent_type="general-purpose"，读取 R8 SKILL.md（skills/reviewer/R8_expert_sim/）
与上述 prompt 合并；panel_count 位专家并行发出，全部返回后再发聚合调用。
