---
name: sociology-review-writing
description: |
  社会学学术论文写作技能。支持撰写社会分层、社会流动、教育社会学等领域的
  中文学术论文（引言、文献综述、研究假设、数据分析与实证结果）。
  端到端工作流：Zotero 文献检索 → 三级分层阅读 → 论证链驱动写作 →
  [可选] Stata 数据分析与图表生成 → 引文终局核验 → .docx 编译输出。
  触发关键词：社会学论文写作、文献综述、社会分层、社会流动、《社会学研究》、
  学术写作、Zotero文献、Stata分析、实证研究。
author: LI Meng
---
# 社会学学术论文写作

## 概览

本技能执行端到端工作流，从 Zotero 文献检索到 .docx 输出。支持两种论文类型：

- **理论/综述型**（仅含引言 + 文献综述 + 研究假设）→ 会话 A-B-D 三会话完成
- **实证/定量型**（含数据分析、实证结果章节）→ 会话 A-B-C-D 四会话完成

核心设计原则：

1. **检查点驱动**：每阶段结束自动持久化状态，支持跨会话恢复
2. **全景驱动分层阅读**：先读全景视图（摘要+笔记精炼）→ 设计论证架构 → 定向 B/C 层深读
3. **引文白名单机制**：只允许引用白名单内文献，杜绝幽灵条目
4. **论证链驱动写作**：禁止罗列堆砌，要求每段有逻辑起承转合
5. **编排器必用**：每次新会话**必须**先运行 `orchestrator.py status --workspace "工作目录"` 获取当前进度，再运行 `orchestrator.py next` 获取具体命令，**禁止**跳过编排器直接操作

## 依赖

| 工具                   | 用途                                                                                                                             |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| zotero-mcp             | `search_collections`、`get_collection_items`、`search_library`、`semantic_search`、`get_item_details`、`get_content` |
| zotero-cli / [cli-anything-zotero](https://github.com/HKUDS/CLI-Anything/tree/main/zotero/agent-harness) | Zotero 本地库读取、检索、附件定位；MCP 不可用时优先使用可发现的 CLI-Anything 入口 |
| zotero_extractor.py    | **默认全文方案**：直读 `.zotero-ft-cache` 本地缓存（覆盖率 98.2%）                                                       |
| note_preprocessor.py   | **笔记预处理+全景视图**：从 SQLite 提取 LLM 笔记，与摘要融合生成 `panoramic_view.json`（0 token）    |
| similarity_check.py    | 段落与知识卡片相似度检查（Jaccard 4-gram + 最长公共子串）                                                                        |
| citation_verifier.py   | **引文三向交叉核验**（正文↔参考文献↔Zotero 元数据，程序化，0 token）                                                     |
| aggregation_checker.py | **论证质量指标检测**（聚合率、叙述型密度、P1-P5 违规，程序化）                                                             |
| humanizer              | 去除 AI 写作痕迹（参见阶段5）                                                                                                    |
| compile_docx.py        | Word 文档编译（支持 Markdown 图片嵌入、三线表渲染、图题/表题/注释自动识别）                                   |
| shxyj_plot_style.py    | **《社会学研究》标准画图模块**（黑白灰配色、L型坐标轴、宋体/TNR字体、柱状图/折线图模板）                     |
| normalize_draft.py     | **Markdown 格式归一化**（编译前自动修正提要/关键词/标题/参考文献等格式变体）                                                     |
| checkpoint_manager.py  | 检查点状态管理                                                                                                                   |
| orchestrator.py        | **统一编排器**（status/next/validate CLI，快速获取当前阶段和下一步命令，无需重读 SKILL.md）                                      |
| stata_parser.py        | **Stata 日志结构化解析**（.log → JSON，提取回归系数/描述统计/VIF 检验，零人工解析）                                               |
| figure_checker.py      | **图表质量自检**（DPI/尺寸/灰度/格式检查，程序化，0 token）                                                                      |
| card_coverage_checker.py | **论点卡片素材消化率检测**（对比卡片中支撑文献与正文实际引用的覆盖率，程序化，0 token）                                   |
| results_verifier.py    | **数据→文本一致性核验**（正文数值↔parsed_results.json 自动比对，程序化，0 token）                                        |
| search_web             | **引言政策搜索**：搜索政策文件、统计数据、政府报告（参见阶段3引言专项）                                                   |
| read_url_content       | 读取搜索结果页面，提取具体数据和原文 URL                                                                                 |

**写作规范外部文件**（写作时需 `view_file` 重读）：

| 文件                                                                                                                       | 内容                                                                   |
| -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [quick_reference.md](references/quick_reference.md) | 金规则、P1-P5、段落结构、引文融合、标点规则                            |
| [writing_style.md](references/writing_style.md)     | 完整写作风格规范（句式、论证节奏、用词偏好、标点控制、AI痕迹检查清单） |
| [exemplar_sentences.md](references/exemplar_sentences.md) | **范句知识库**（开篇钩子、缺口声明、贡献声明、过渡句、假设收束句、数据描述、讨论结论句式） |
| [theoretical_frameworks.md](references/theoretical_frameworks.md) | **理论框架索引**（6领域30+框架 + Coleman Boat机制链模板 + 假设类型速查） |
| [review_simulation.md](references/review_simulation.md) | **模拟审稿模板**（R1方法论+R2理论审稿人角色、严重度分级、修订矩阵） |
| [journal_format.md](references/journal_format.md)   | 《社会学研究》排版体例（字体、标题、脚注、参考文献格式）               |

---

## 检查点协议（跨会话恢复）

### 恢复逻辑（每次对话开始时强制执行）

1. 询问用户工作目录路径（或使用默认 `scratch/paper_workspace`）
2. **首选：运行编排器获取状态和下一步指令**：
   ```bash
   python "scripts/orchestrator.py" status --workspace "工作目录"
   python "scripts/orchestrator.py" next --workspace "工作目录"
   ```
3. **存在 checkpoint.json** → 从中断点继续（编排器会显示具体执行命令）
4. **不存在** → 初始化后从阶段1开始：
   ```bash
   python "scripts/checkpoint_manager.py" init --workspace "工作目录" --topic "论文主题" --outline "引言,2.1,2.2,2.3" --journal "社会学研究"
   ```

> [!IMPORTANT]
> **体例范围**：当前版本仅保留《社会学研究》体例。初始化、引注、参考文献排序和 `.docx` 编译均以《社会学研究》为唯一格式基准：
>
> | 目标期刊 | 引注系统 | 体例文件 | 摘要标签 | 关键词分隔符 |
> | ---------- | ---------- | ---------- | ---------- | ------------ |
> | 《社会学研究》 | 括注式（作者,年份） | `journal_format.md` | "提要：" | 全角空格 |

### 保存逻辑（每阶段结束时强制执行）

1. 将本阶段所有中间产出写入工作目录
2. 运行 `checkpoint_manager.py complete --stage N`
3. 向用户报告本阶段成果摘要

### 阶段3 节级恢复

每完成一节并通过自检后运行：

```bash
python "scripts/checkpoint_manager.py" complete-section --workspace "工作目录" --section "2.1" --draft-file "drafts/sec1_xxx.md" --report-file "reports/check_xxx.md"
```

### 强制分会话规则

> [!CAUTION]
> **文献总量 ≥80 篇时，必须分会话执行，不得在单个会话中跑完全部阶段。** 违反此规则将导致后半段上下文压力增大、写作质量下滑。

| 会话 | 覆盖阶段 | 预计 Token | 入口产出物 | 入口检查 | 是否必须 |
| ---- | -------- | ---------- | ---------- | -------- | -------- |
| A | 1-2 | ~50K | whitelist + knowledge_cards | 无（首次启动） | ✅ 必须 |
| B | 3-5 | ~40K | drafts/ + 评分报告 | `knowledge_cards/` 非空 + checkpoint ≥2 | ✅ 必须 |
| **C** | **3b** | **~30K** | **stata/ + figures/ + drafts/sec_三.md + drafts/sec_四.md** | **checkpoint ≥5 + 用户提供 Stata .do/.log** | **⚡ 条件性** |
| D | 6-8 | ~15K | final_draft + output.docx | `final_draft.md` 存在 + checkpoint ≥5(无C) 或 ≥6(有C) | ✅ 必须 |

> [!IMPORTANT]
> **会话 C（数据分析）为条件性会话**，仅当论文包含"三、数据、变量与策略"和"四、实证分析与结果"章节时执行。
> 判断规则：
> 1. 用户提供的写作大纲中包含数据/变量/方法/实证分析相关章节 → 需要会话 C
> 2. 用户提供了 Stata .do 文件或 .log 日志 → 需要会话 C
> 3. 论文为纯理论/文献综述性质 → 跳过会话 C，直接从 B 进入 D
>
> **在阶段5结束时，agent 必须主动询问用户**："论文是否包含数据分析与实证结果部分？如需要，请提供 Stata .do 文件或运行日志。"

> [!CAUTION]
> 当 agent 感知到 token 消耗接近上限，**必须在当前阶段/节结束后立即保存检查点并告知用户开启新会话**。
> 文献 <80 篇时允许单会话执行，但 agent 应在阶段2结束后主动评估剩余 token 预算。

### 工作目录标准结构

```
paper_workspace/
├── checkpoint.json              ← 检查点状态
├── citation_whitelist.json      ← 阶段1
├── metadata.json                ← 阶段1（含 has_fulltext/has_annotations/reading_level）
├── references_formatted.md      ← 阶段1
├── annotations.json             ← 阶段1（用户注释导出，如有）
├── panoramic_view.json          ← 阶段1（全景视图：每篇文献的摘要/笔记精炼）
├── metadata_gaps.log            ← 阶段1
├── argument_scaffold.md         ← 阶段2（论证架构，用户可审核修改后再写卡片）
├── knowledge_cards/             ← 阶段2（文献卡片 + 论点卡片）
├── drafts/                      ← 阶段3 + 阶段3b
│   ├── sec_引言.md
│   ├── sec_2.1.md ~ sec_2.3.md
│   ├── sec_三.md              ← 阶段3b（数据分析，可选）
│   └── sec_四.md              ← 阶段3b（实证结果，可选）
├── reports/                     ← 阶段3/5
├── stata/                       ← 阶段3b（可选）
│   ├── *.do                   ← 用户提供的 Stata 脚本
│   ├── *.log                  ← Stata 运行日志
│   └── *.dta                  ← 数据文件
├── figures/                     ← 阶段3b（可选）
│   ├── figure1_*.png
│   ├── figure2_*.png
│   └── generate_figures.py    ← 画图脚本
├── final_draft.md               ← 阶段4
├── output.docx                  ← 阶段7
└── archive/                     ← 阶段8
```

---

## 阶段1：文献检索与白名单构建

**目标**：从 Zotero 获取全部候选文献元数据，构建引文白名单。

### 步骤1：Zotero 文献提取（MCP 或 CLI）

> [!IMPORTANT]
> **首选可用后端**：优先使用当前环境中可发现的 Zotero 后端。可选顺序为 `zotero-mcp` → `zotero-cli` → `cli-anything-zotero` → SQLite 直读。MCP/CLI 用于获取集合与条目，本地脚本继续读取全文缓存（0 token）。

向用户确认 Zotero 集合名称后，执行以下步骤：

**1a. 获取集合 Key（MCP 模式）**：

```
mcp_zotero-mcp_search_collections(q="集合名")
```

记录返回的 `collectionKey`（如 `SFXCNRCF`）。如有子集合，用 `get_subcollections` 获取子集合 Key。

**1b. 导出条目列表**：

对每个集合/子集合调用（建议 `limit=200` 确保获取全部）：

```
mcp_zotero-mcp_get_collection_items(collectionKey="KEY", limit=200)
```

将返回的 `data` 数组合并后保存为 JSON 文件：

```python
# Agent 将 MCP 返回的 data 合并写入文件
write_to_file("工作目录/mcp_items.json", json.dumps(combined_data))
```

**1c. 本地脚本处理**（0 token，~2秒）：

```bash
python "scripts/zotero_extractor.py" --from-mcp-json "工作目录/mcp_items.json" --output-dir "工作目录" --coverage-report
```

脚本自动完成：解析 MCP 元数据 → 从附件路径读取本地 `.zotero-ft-cache` 全文 → 从 SQLite 补充用户注释 → 生成全部产出。

**CLI 备选模式**：

当 MCP 不可用但本机存在 `zotero-cli` 或 `cli-anything-zotero` 时，先运行 `--help` 或 `--json app status` 做最小确认，再用集合/条目查询命令导出元数据。优先使用真实 Zotero 后端，不手工伪造文献列表。

### 步骤1（备用）：SQLite 直读

当 MCP 不可用时，使用原有 SQLite 模式：

```bash
python "scripts/zotero_extractor.py" --collections "集合名" "子集合名" --output-dir "工作目录" --coverage-report
```

> [!WARNING]
> SQLite 模式读取的是数据库快照，若 Zotero 运行中刚修改了集合成员，可能不同步。

**自动产出**（两种模式输出一致）：

- `metadata.json`：完整元数据，含 `has_fulltext`、`has_annotations`、`reading_level` 字段
- `citation_whitelist.json`：引文白名单（含阅读层级标注）
- `references_formatted.md`：《社会学研究》体例参考文献
- `annotations.json`：用户高亮/注释导出（如有）
- 控制台输出覆盖率诊断报告

### 步骤2：覆盖率诊断（0 token）

阅读控制台输出的覆盖率报告，呈现给用户：

- 全文覆盖率、注释覆盖率、摘要完整率
- 推荐的 A/B/C 层级分配
- 缺失全文的文献清单

### 步骤3：笔记提取与全景视图生成（0 token）

> [!IMPORTANT]
> 此步骤提取用户在 Zotero 中为文献撰写的 LLM 总结笔记，与摘要融合后生成全景视图。全景视图是阶段2论证架构设计的核心输入。

```bash
python "scripts/note_preprocessor.py" --metadata "工作目录/metadata.json" --output-dir "工作目录"
```

脚本自动完成：
- 从 Zotero SQLite（`immutable=1` 模式，不干扰 Zotero 运行）读取用户笔记
- 去除 HTML 标签和元数据模板区块（作者/期刊/标签/日期等）
- **有 LLM 笔记的文献** → 提取核心结论句（压缩至 150 字）
- **仅有摘要的文献** → 首尾保留法（保留首句+末句，截至 250 字，避免丢失结论）
- **仅有标题的文献** → 使用标题

**产出**：`panoramic_view.json`（全景视图，每篇文献一条记录）

### 步骤4：MCP 关键词补充（可选，仅此步消耗 token）

对每章关键词调用 `mcp_zotero-mcp_search_library(q="章节关键词", limit=10)` 发现**集合外**的关联文献。

- 将发现的候选文献呈现给用户确认
- 用户确认后追加到 `citation_whitelist.json`
- 如无预整理集合，可扩大此步范围

> [!NOTE]
> 不推荐使用 `semantic_search`（语义搜索），其响应速度慢且不稳定。优先使用 `search_library`（关键词搜索，~1秒响应）。

### 步骤4a：综述文献盲区检查（可选，推荐执行）

> [!TIP]
> 此步骤用于系统性发现用户 Zotero 集合中可能遗漏的重要文献，减少审稿人指出"遗漏关键文献"的风险。

1. **综述文献检索**：对研究主题调用 `search_web(query="主题 综述 review site:cssn.cn OR site:cnki.net 近3年")` 搜索该领域最新的综述或述评文章
2. **提取被引清单**：对搜索到的综述文章，调用 `read_url_content` 提取其参考文献列表中的高频被引文献
3. **与白名单对比**：将综述中的高频被引文献与当前 `citation_whitelist.json` 交叉比对，标记遗漏项
4. **呈现给用户确认**：将遗漏的经典文献呈现给用户，确认后追加到白名单

### 步骤4b：核心文献引文链检查（可选）

对全景视图中标记为核心（C 层候选）的文献，调用 `mcp_zotero-mcp_search_library` 搜索其关键被引文献（forward citation）。

- 聚焦于近3年的后续研究（可能是用户整理集合时尚未发表的新文献）
- 发现的重要后续研究呈现给用户确认后追加到白名单

### 步骤5：元数据清洗与检查点

- 检查 `metadata.json` 中 `publicationTitle`、`volume`、`issue` 完整性
- 缺失严重的字段通过 `get_item_details` 补全，仍缺的记录到 `metadata_gaps.log`
- 标记摘要缺失或过短（<50字）的文献为 `needs_upgrade`

### 退出条件

- 白名单覆盖综述架构所有章节，用户确认无遗漏
- 覆盖率报告已呈现、`metadata_gaps.log` 已生成
- **`panoramic_view.json` 已生成**
- **检查点保存**

---

## 阶段2：全景驱动的分层阅读

**目标**：先全景后深入——基于全景视图设计论证架构，再定向阅读构建写作素材（论点卡片）。

### 步骤 2a：全景→论证架构设计（📋 用户审核检查点）

> [!IMPORTANT]
> **先看全景（所有文献的核心观点），再设计论证结构，最后定向阅读。** 这一步决定了 80% 的写作质量。

1. 读取 `panoramic_view.json`（阶段1产出），一次性获取全部文献的核心观点全景图
2. **理论框架辅助（可选）**：若用户写作大纲中未明确指定理论框架，`view_file` 读取 [theoretical_frameworks.md](references/theoretical_frameworks.md)，根据研究问题和全景视图中的文献分布，向用户推荐2-3个候选理论框架。用户确认后再继续。
3. 结合用户提供的写作架构，为每个子节设计**论证架构**：
   - 每段的**命题句**（该段要论证什么）
   - 该段需要引用的**文献列表**（从全景视图中选取）
   - **证据层级结构**（定义层→共识层→张力/转折层→收束）
   - 预标记的**聚合引文组**（可聚合引用的文献组合）
   - 标记需要 **C 层深读**的候选文献（有 LLM 笔记或核心理论文献）
4. 将论证架构写入 `argument_scaffold.md`
5. **📋 呈现给用户审核**：用户可在此检查点修改段落顺序、增删引文、调整 C 层候选等

> [!TIP]
> 论证架构是结构化的 markdown 文件，用户可直接编辑后告知 agent "按修改后的架构写卡片"。

### 步骤 2b：定向分层阅读与卡片生成

论证架构确认后，按架构中每段涉及的文献定向阅读。**每篇文献的数据源调用优先级**：

| 优先级 | 数据源 | 说明 |
| ------ | ------ | ---- |
| 1️⃣ 最高 | **PDF 注释**（`annotations.json`） | 用户标记的原文语句，可直接引用 |
| 2️⃣ 次高 | **LLM 笔记**（`panoramic_view.json` 中 `has_note=true` 的完整笔记） | 结构化分析，补充数据、机制解释 |
| 3️⃣ 兜底 | **全文搜索**（`.zotero-ft-cache` / `get_content`） | 前两项未覆盖时使用 |
| 4️⃣ 最低 | **摘要**（`abstractNote`） | 全文也不可用时回退 |

**阅读层级由架构中的角色自动分配**：

| 层级 | 分配规则 | Token 预算 |
| ---- | -------- | ---------- |
| **N 笔记层** | 有 LLM 笔记但架构未标为 C 层 | ~0 tok（笔记在全景中已缓存） |
| **B 注释层** | 有 PDF 注释 / 架构中分配到段落 | ≤500 tok/篇 |
| **C 全文层** | 架构标记的核心文献，每章节 ≤4 篇 | ≤5,000 tok/篇 |

### Token 预算

| 步骤 | 预算 | 说明 |
| ---- | ---- | ---- |
| 全景视图读取 | ~20-25K | 一次性读入全部文献的摘要/笔记精炼 |
| 架构设计 | ~3K | 产出 argument_scaffold.md |
| B 层注释阅读 | ~8K | 有注释的文献定向读取 |
| C 层全文深读 | ~20K | 每章 ≤4 篇 |
| 卡片组装 | ~5K | 基于架构填充 |
| **总预算** | **≤65,000** | — |

### 步骤 2c：论点卡片组装

基于论证架构和定向阅读结果，产出**论点卡片**（每节一份，必须）：
- 每段的论点句 + 支撑文献及其核心贡献/局限
- 预组装的聚合引文括注（已按正确格式写好）
- 标注每条素材的**数据源**标记：📌（PDF 注释原文）、📝（LLM 笔记）、📄（全文搜索）

产出**核心文献卡片**（C 层文献，可选）：模板见 [knowledge_card_template.md](references/knowledge_card_template.md)。

### 退出条件（必须全部满足，缺一不可）

> [!CAUTION]
> 阶段2的退出条件包含**文件产出验证**，agent 不得仅在上下文中"记住"阅读结果而跳过文件写入。

- `argument_scaffold.md` 已生成并**经用户审核**
- **`knowledge_cards/` 目录中存在 ≥N 份论点卡片文件**（N = 综述章节数，如3节则至少3份）
- 论点卡片文件命名规范：`knowledge_cards/arg_引言.md`、`knowledge_cards/arg_2.1.md`、`knowledge_cards/arg_2.2.md`、`knowledge_cards/arg_2.3.md`
- **论点卡片最低内容要求**：每份卡片 ≥500字，必须包含该节各段的：(a) 论点句 (b) 支撑文献及其核心贡献/局限的一句话概括 (c) 预组装的聚合引文括注（已按正确格式写好）
- 总 token 未超 65K
- **检查点保存**

---

## 阶段3：逐节撰写

**目标**：按综述架构逐节撰写草稿，严格遵循写作规范。

> [!IMPORTANT]
> **写作优先级（严格按此顺序，不得颠倒）：**
>
> 1. ⭐ **字数达标**：每节字数达到写作架构规定的目标（使用 `--expected-chars` 检查）
> 2. ⭐ **论证深度**：每个理论观点充分展开（定义→代表性发现→辨析评价），而非压缩为“一句论点+括注群”
> 3. ⭐ **卡片素材消化**：论点卡片中的“支撑文献及核心贡献”必须逐条在正文中展开，不得跳过
> 4. 聚合率达标：在保证前三项的基础上，尽量达到聚合率 ≥60%
>
> **当论证深度与聚合率冲突时，选择充分展开论证。**

### ⛔ 阶段3入口门禁（强制，不可跳过）

> [!CAUTION]
> **进入阶段3前必须通过以下检查，任一不满足则拒绝进入写作，返回阶段2补全：**
>
> 1. `knowledge_cards/` 目录**非空**，且包含 ≥ 综述章节数的论点卡片文件
> 2. `checkpoint.json` 中当前阶段 ≥ 2（即阶段2已标记完成）
> 3. 验证命令：`ls knowledge_cards/arg_*.md | Measure-Object`（PowerShell）或 `ls knowledge_cards/arg_*.md | wc -l`（Bash），结果必须 ≥ 章节数
>
> **如果论点卡片不存在，agent 必须先回到阶段2生成论点卡片，而不是"直接开始写作"。**

### 写作前强制步骤（每次进入阶段3必须执行，不可跳过）

> [!CAUTION]
> 包括跨会话恢复时也必须执行以下四步，再开始写作：

1. `view_file` 读取用户提供的写作架构文件（如 `写作架构.txt`），确认每节的论证目标和**哪些节需要在末尾导出研究假设**
2. `view_file` 读取 [quick_reference.md](references/quick_reference.md)，记忆段落结构、P1-P5、引文融合规则
3. `view_file` 读取 [exemplar_sentences.md](references/exemplar_sentences.md)，参照范句模板的**句式结构**（开篇钩子、缺口声明、贡献声明、过渡句模板），写作时模仿已发表论文的修辞风格
4. **《社会学研究》体例确认**：`view_file` 读取 [journal_format.md](references/journal_format.md) 第三节“文中引注”和第五节“参考文献”，写作、核验和编译均固定采用括注式 `（作者,年份）`。

### 假设嵌入规则

> [!CAUTION]
> **研究假设的位置严格依据用户提供的写作大纲。** agent 不得自行决定在哪个子节导出假设或增删假设。

- 文献回顾与研究假设**融为一体**：每个子节先做文献综述，若写作大纲指定该节需导出假设，则在**该节末尾段**从前文综述中自然推导出假设
- 假设段结构：前文综述的逻辑收束 → "由此，本研究提出假设LX：……" → 假设表述（可验证的命题）
- 不存在独立的"研究假设"章节，假设分散在各子节中

### 聚合引文写法模板（每段写作前必读）

> [!CAUTION]
> 首次写作即须达到 60% 聚合率。以下模板为每段的标准结构，减少返工：

```
段落 = 论点句 + 证据层1（句末聚合括注）+ 证据层2（句末聚合括注）+ 收束句
                                ↑                        ↑
                        (A,年;B,年;C,年)            (D,年;E,年)

❌ 禁止：Day和Fiske（2017）发现……陈云松和范晓光（2016）揭示……
✅ 正确：流动感知的评价功能已获广泛验证（Day & Fiske,2017;陈云松、范晓光,2016）。
```

### 引文格式速查表（每节写作前必看）

| 情形 | 格式 | 示例 |
|------|------|------|
| 中文单作者 | （姓,年） | （李培林,2023） |
| 中文二人 | （姓A、姓B,年） | （陈云松、范晓光,2016） |
| 中文三人及以上 | （第一作者等,年） | （吴愈晓等,2025） |
| 英文单作者 | (Surname,year) | (Breen,2010) |
| 英文二人 | (A & B,year) | (Day & Fiske,2017) |
| 英文三人及以上 | (A et al.,year) | (Brown et al.,2021) |
| 多条聚合 | 中英混合时分号分隔 | （李春玲,2003;Breen,2010） |
| 同作者多年 | 逗号分隔年份 | （Spence,1973,2002） |

### 脚注标记规则

正文使用 `[^N]` 语法，`compile_docx.py` 自动转为 ①②③ 上角标。脚注定义放在文件末尾。

**学术文献 → 正文括注 `（作者,年份）`，不用脚注。脚注仅用于政策/数据/网站/作者说明。**

脚注格式示例：
```
[^1]: 数据来源：教育部《2024年全国教育事业发展基本情况》，http://www.moe.gov.cn/xxx，2025年3月1日。
[^2]: 参见《国家中长期教育改革和发展规划纲要（2010—2020年）》，第二章第三条。
[^3]: 参见「2025年政府工作报告」，http://www.gov.cn/xxx，2025年3月5日。
```

### 引言/问题提出：政策与数据搜索（强制）

> [!CAUTION]
> 写作架构中标注了"搜索网络"/"政策"/"最新数据"的节，agent **必须在写该节前**执行搜索，不得跳过或凭记忆编造数据。

1. 从写作架构提取关键词，调用 `search_web(query="关键词 site:gov.cn 年份")` 搜索 3-5 次（政策文件、统计数据、政府报告）
2. 对有价值的结果调用 `read_url_content` 提取具体数据和原文 URL
3. 将搜索结果记入 `drafts/policy_notes.md`（数据 + 来源 + URL）
4. 写作时嵌入数据，同步在文件末尾添加 `[^N]` 脚注定义
5. **无法验证来源的数据禁止使用**

### 写作流程（逐节循环）— 硬阻断机制

> [!CAUTION]
> **严禁在同一个 write_to_file / tool call 中写入多节内容。** 每节必须写入独立文件，运行自检通过后方可写下一节。一次性全写是本 Skill 最严重的违规行为。

每一节按以下流程执行：

0. **重读核心写作规则**（每节写作前必做，不要依赖上下文中的已读记忆）：
   - `view_file` 读取 [quick_reference.md](references/quick_reference.md) 全文（~50行）
   - `view_file` 读取 [writing_style.md](references/writing_style.md) 第1-30行（核心检查清单段）
   - 查看上方「引文格式速查表」确认中英文括注格式
1. **读取该节论点卡片**：`view_file` 读取 `knowledge_cards/arg_当前节.md`，确认各段的论证素材和预组装引文。
2. **撰写该节**：将该节全部段落写入**独立文件** `drafts/sec_当前节.md`（如 `drafts/sec_引言.md`、`drafts/sec_2.1.md`）。参照聚合引文模板组织每段引文。若写作大纲指定该节含假设，则在末尾段导出假设。
3. **白名单追增**（如需要）：
   - 调用 `search_library` 确认文献存在于 Zotero
   - 存在 → 追加到白名单 → 引用
   - 不存在 → **禁止引用**，改用白名单内文献替代
4. **强制暂停自检**（程序化 + 人工，不得跳过）：
   - **程序化检测**（每节写完后必须运行）：
     ```bash
     python "scripts/aggregation_checker.py" --draft drafts/sec_当前节.md --stage 3 --expected-chars 本节目标字数
     ```
   - **卡片消化率检查**（每节写完后必须运行）：
     ```bash
     python "scripts/card_coverage_checker.py" --draft drafts/sec_当前节.md --cards knowledge_cards/
     ```
     覆盖率 < 70% 时，必须回到论点卡片，逐条展开未覆盖的支撑文献。
   - **人工检查**（agent 逐段确认）：段首是否为论点句、段尾是否有综合收束、每段是否含 ≥1 处理论评价
   - 若本节含假设，检查假设是否从前文综述中逻辑推导而来
5. **不通过 → 立即重写该节**，重写后再次运行 aggregation_checker 直到通过。
6. **节级回顾**（保存检查点前必做）：
   - 重读写作架构中该节的具体要求，检查是否满足“展开要求”（如“把逻辑链条展开”“将经典机制解释融入其中”等）
   - 请核对：关键理论概念是否有定义、辨析和评价，而不只是“提一句”
7. **通过后保存节级检查点**：
   ```bash
   python "scripts/checkpoint_manager.py" complete-section --workspace "工作目录" --section "当前节" --draft-file "drafts/sec_当前节.md" --report-file "reports/check_当前节.md"
   ```
8. **方可进入下一节。**

> [!CAUTION]
> **退出条件**：各节字数达标 + 引文仅用白名单 + **每节均有独立 drafts/sec_*.md 文件** + 每节自检通过（aggregation_checker --stage 3 通过） + 假设位置与写作大纲一致 + **检查点保存**

---

## 阶段4：段落合并与逻辑衔接

**目标**：合并各节草稿，处理段间逻辑衔接。**仅关注跨段衔接**。

1. 按"引言 → 文献回顾与研究假设(一)(二)(三) → [可选] 数据与方法 → [可选] 实证结果"顺序拼接。
2. 检查段间逻辑：上段末句与下段首句是否形成"结论→前提"关系。
3. 补充过渡句和逻辑连接词。
4. 跨段 P1-P5 扫描（仅交界处）。
5. 全文通读确认论证链完整。

### ❗ `final_draft.md` 严格模板（必须遵循）

> [!CAUTION]
> 组装 `final_draft.md` 时必须严格遵循以下格式。任何偏离都可能导致 `compile_docx.py` 编译错误。

```markdown
# 论文标题

作者姓名

提要：内容文本……

关键词：词1　词2　词3

## 一、引言

正文段落……（作者,年份）……[^1]

## 二、文献回顾与研究假设

### （一）子节标题

正文……**假设内容用粗体**

## 三、数据、变量与分析策略（实证型论文，可选）

### （一）数据来源

正文……

### （二）变量测量

表1　核心变量描述统计(N=XXXX)

| 变量 | 均值 | 标准差 | 最小值 | 最大值 |
|------|------|--------|--------|--------|
| ... | ... | ... | ... | ... |

注：数据来源于……

### （三）分析策略

正文……

## 四、实证分析与结果（实证型论文，可选）

### （一）基本回归结果

表2　OLS回归结果

| 变量 | 模型1 | 模型2 | 模型3 |
|------|-------|-------|-------|
| ... | ... | ... | ... |

注：括号内为标准误。***P<0.01, **P<0.05, *P<0.1。

![图1　教育程度与工资差异](figures/figure1.png)

图1　不同教育程度的平均小时工资

注：误差线表示标准差。

参考文献

中文条目1
中文条目2
English entry 1
English entry 2

作者单位：xxx

[^1]: 脚注内容
[^2]: 脚注内容
```

**关键约束：**

| 要素 | 格式要求 |
|------|----------|
| 论文标题 | `# 标题`（单井号，不加粗体标记） |
| 提要 | `提要：内容`（无粗体、无井号、全角冒号） |
| 关键词 | `关键词：词1　词2`（无粗体、全角冒号、全角空格分隔） |
| 一级标题 | `## 一、标题`（双井号） |
| 二级标题 | `### （一）标题`（三井号） |
| 三级标题 | `#### 1. 标题`（四井号） |
| 参考文献 | `参考文献`（纯文本，无井号、无粗体） |
| 作者单位 | `作者单位：xxx`（无粗体、全角冒号） |
| 脚注定义 | `[^N]: 内容`（放在文件末尾） |
| 正文粗体 | `**粗体内容**`（仅用于假设表述） |

### 退出条件

- 全文逻辑连贯、各节字数均衡、交界处无 P1-P5 违规
- **程序化检测**（合并后必须运行）：
  ```bash
  python "scripts/aggregation_checker.py" --draft final_draft.md --stage 3
  ```
- **检查点保存**：将 `final_draft.md` 写入工作目录

---

## 阶段5：语言润色、论证终检与审阅

**目标**：消除 AI 痕迹，论证质量终检。阶段3自检是初筛（≥60%），本阶段是终检（≥70%）。

### 步骤

1. **应用 humanizer 技能**：先读取 `skills/academicforge-humanizer/SKILL.md`，按 checklist 检查修正。
2. 执行 [writing_style.md](references/writing_style.md) 检查清单。
3. **论证质量终检**（程序化 + 人工，全部达标方可通过）：

   **3a. 程序化检测**（必须运行）：

   ```bash
   python "scripts/aggregation_checker.py" --draft final_draft.md --stage 5
   ```

   自动检测：聚合率≥70%、叙述型密度≤2次/千字、P1-P5 违规、**AI痕迹**（破折号密度≤2/千字、引号密度≤4对/千字、"不仅…而且"≤1次/千字、禁用英文词=0）

   **3b. 人工检查**（agent 逐段判断）：

   | 指标         | 达标线   |
   | ------------ | -------- |
   | 段首论点率   | 100%     |
   | 段尾收束率   | 100%     |
   | 理论评价密度 | ≥1次/段 |
4. **相似度检查**（程序化）：

   ```bash
   python "scripts/similarity_check.py" --draft final_draft.md --bank knowledge_cards/ --threshold 0.30 --lcs-threshold 10
   ```

   - Jaccard 4-gram ≥30% → 🟡 警告，≥45% → 🔴 重写
   - 最长公共子串 ≥10 字 → 🟡 警告，≥20 字 → 🔴 重写
5. **去引文测试**（抽查 3 段）：删除括注后段落是否仍有完整论证逻辑？
6. **整体审阅**：逐节检查各假设是否从该节综述中自然推导而出且位置与写作大纲一致、引文密度抽查、**等待用户反馈**。

### 退出条件

- AI 痕迹消除 + 终检 5 项达标 + 去引文测试通过 + 用户确认
- **检查点保存**

---

## 阶段3b：数据分析与实证结果撰写（条件性，会话 C）

> [!IMPORTANT]
> **本阶段仅当论文包含数据分析章节时执行。** 若为纯理论/综述型论文，直接跳至阶段6。
> 进入本阶段前，agent 必须在阶段5结束时已确认用户需要数据分析，并获取了 Stata .do 文件或运行日志。

**目标**：基于 Stata 分析结果，撰写"三、数据、变量与分析策略"和"四、实证分析与结果"章节，同步生成符合期刊规范的图表。

### 入口门禁

1. checkpoint ≥ 5（即阶段5已完成）
2. 用户已提供以下材料之一：
   - Stata `.do` 脚本 + `.dta` 数据文件
   - Stata `.log` 运行日志
   - 已有的回归结果截图/文本
3. 将用户提供的 Stata 文件复制到 `stata/` 目录

### 步骤1：Stata 日志结构化解析

**首先运行 `stata_parser.py` 自动提取结构化数据**（0 token，~1秒）：

```bash
python "scripts/stata_parser.py" --log stata/*.log --output stata/parsed_results.json
```

脚本自动提取并输出到 `stata/parsed_results.json`：

| 提取内容 | JSON 字段 | 用途 |
|----------|-----------|------|
| 样本量、变量描述统计 | `descriptives[].variables` | 表1 描述统计表 |
| 回归系数、标准误、P值、R² | `regressions[].coefficients` | 表2/表3 回归结果表 |
| VIF 多重共线性 | `vif_tests[].variables` | 正文稳健性讨论 |
| 原始命令列表 | `raw_commands` | 方法论溯源 |

读取 `stata/parsed_results.json` 后直接用于撰写，无需手动解析日志文本。

> [!CAUTION]
> **所有数值必须严格来自解析结果（溯源到 Stata 日志），不得自行编造或凭记忆填写。**

### 步骤2：生成图表（使用 shxyj_plot_style.py）

编写 `figures/generate_figures.py` 画图脚本：

```python
import sys, os
# 将 skill 的 scripts/ 目录加入 Python 路径（请替换为实际安装路径）
SKILL_DIR = os.environ.get("SOCIOLOGY_SKILL_DIR", ".")
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
from shxyj_plot_style import apply_style, save_figure, LINE_STYLES, BAR_FILLS
import matplotlib.pyplot as plt
import numpy as np

apply_style()  # 全局应用《社会学研究》风格

# === 图1：描述统计可视化 ===
fig, ax = plt.subplots(figsize=(6, 4.5))
# ... 柱状图/折线图代码 ...
save_figure(fig, 'figures/figure1_xxx.png',
            title='图1　标题', note='注：...')

# === 图2：回归系数比较 ===
# ... 更多图表 ...
```

运行画图脚本：

```bash
python figures/generate_figures.py
```

**画图完成后，运行图表质量自检**（程序化，0 token）：

```bash
python "scripts/figure_checker.py" --dir figures/
```

自动检查 DPI ≥300、宽度 ≥1200px、灰度配色、文件格式和大小。不通过的图表需修改 `generate_figures.py` 后重新生成。

**常用图表类型与 API：**

| 图表类型 | 适用场景 | 核心 API |
|----------|----------|----------|
| 柱状图（带误差线） | 分组均值比较 | `ax.bar()` + `ax.errorbar()` + `BAR_FILLS` |
| 折线图（多模型对比） | 递进回归系数变化 | `ax.plot()` + `LINE_STYLES` |
| 分组柱状图 | 交互效应可视化 | 双 `ax.bar()` 并列 |
| 水平条形图 | 分解贡献排序 | `ax.barh()` |
| 系数森林图 | 多变量系数展示 | `ax.errorbar(fmt='o')` |

### 步骤3：撰写"三、数据、变量与分析策略"

写入 `drafts/sec_三.md`，包含以下子节：

1. **（一）数据来源**：数据集介绍、调查设计、样本筛选过程、最终分析样本量
2. **（二）变量测量**：
   - 因变量、自变量、控制变量的操作化定义
   - 嵌入「表1　核心变量描述统计」（Markdown 三线表）
3. **（三）分析策略**：模型选择依据、递进模型设计逻辑、潜在内生性处理

### 步骤4：撰写"四、实证分析与结果"

写入 `drafts/sec_四.md`，包含以下子节：

1. **（一）基本回归结果**：嵌入「表2 回归结果表」+ 系数解读
2. **（二）进一步分析**：交互效应、分样本分析、中介/调节效应等
3. **（三）稳健性检验**：替换变量、替换模型、子样本检验
4. 穿插引用 `figures/` 中的图表（使用 `![alt](figures/xxx.png)` 语法）

**结果报告规范：**

| 要素 | 规范 |
|------|------|
| 回归系数 | 报告至小数点后3-4位 |
| 标准误 | 括号内，与系数对齐 |
| 显著性 | ***P<0.01, **P<0.05, *P<0.1 |
| R²/Pseudo R² | 表底报告 |
| 样本量 | 表底报告 |
| 解读文字 | 先说方向和大小，再说显著性水平 |

### 步骤5：自检

- 所有表格数值与 `stata/parsed_results.json` 一致（可追溯到原始日志）
- 图表均已生成且 `figure_checker.py` 检查通过
- Markdown 图片引用路径正确
- 结果解读与系数方向一致（不存在正系数说"负相关"的情况）

### 退出条件

- `drafts/sec_三.md` 和 `drafts/sec_四.md` 已产出
- `stata/parsed_results.json` 已生成
- `figures/` 目录中所有引用图片已生成且质量检查通过
- 所有表格数值可追溯
- **检查点保存**（标记阶段3b完成）

---

## 阶段5b：模拟审稿（可选，推荐投稿前执行）

**目标**：在投稿前预判审稿意见热点，针对性加强论证。**可选执行，不强制。**

> [!TIP]
> 用户可通过在检查点中添加注释“需要审稿模拟”或直接说“帮我模拟审稿”来触发此阶段。跳过此阶段不影响后续流程。

### 步骤1：审稿人角色准备

`view_file` 读取 [review_simulation.md](references/review_simulation.md)，加载两位审稿人角色定义和评审模板。

### 步骤2：R1 方法论审稿

以 R1（方法论审稿人）角色审阅 `final_draft.md`，聚焦：

- 因果识别策略是否充分讨论
- 数据质量、样本选择偏误
- 稳健性检验是否充分
- 效应量是否讨论（实质显著性 vs 统计显著性）

按 [review_simulation.md](references/review_simulation.md) 第四节的结构化模板输出意见，每条意见标注 **严重度**（CRITICAL/MAJOR/MINOR）和 **可寻址性**（FEASIBLE/HARD/INFEASIBLE）。

### 步骤3：R2 理论审稿

以 R2（理论审稿人）角色审阅 `final_draft.md`，聚焦：

- 理论贡献是否清晰
- 文献定位是否准确、是否遗漏关键文献
- 假设推导是否从理论自然导出
- 讨论是否回扣理论框架、是否有“数据说话”的问题
- 论证结构是否存在堆砌（关联 P1-P5 检测结果）

按相同模板输出结构化意见。

### 步骤4：汇总与修订优先级矩阵

将两位审稿人意见汇总，按 [review_simulation.md](references/review_simulation.md) 第五节生成修订优先级矩阵：

- **P0**：CRITICAL + FEASIBLE → 必须立即修正
- **P1**：MAJOR + FEASIBLE → 建议修正
- **P2**：MINOR 或 HARD → 酌情处理
- **P3**：INFEASIBLE → 记录但不修改，预备 rebuttal 回应

产出 `reports/simulated_review.md`。

### 步骤5：📋 用户审核与修订

将修订优先级矩阵呈现给用户。用户确认后：

1. 按 P0 意见修订 `final_draft.md`
2. 按 P1 意见修订 `final_draft.md`
3. 修订完成后重跑 `aggregation_checker.py` 确认未破坏论证质量

### 退出条件

- `reports/simulated_review.md` 已产出
- P0 意见已全部修订
- 用户确认修订完成

---

## 阶段6：引文终局核验（程序化）

**目标**：杜绝幽灵条目。**强制执行，不得跳过。**

### 步骤1：运行三向交叉核验脚本

```bash
python "scripts/citation_verifier.py" --draft final_draft.md --metadata metadata.json --output reports/citation_report.txt
```

脚本自动完成（0 token 消耗）：

- 提取正文所有 `（作者,年份）` 括注
- 解析参考文献列表每条条目
- 三向比对：正文↔参考文献↔`metadata.json`

### 步骤2：根据报告处理

| 报告标记                  | 含义                            | 处理                                                           |
| ------------------------- | ------------------------------- | -------------------------------------------------------------- |
| ✅ 成功匹配               | 正文→参考文献→Zotero 三方一致 | 无需操作                                                       |
| 🔴 正文引了但参考文献没有 | 报告已附自动补生成的条目        | **直接追加到参考文献列表**                               |
| 🔴🔴 幽灵引文             | 正文引了但 Zotero 无记录        | 调用 `search_library` 确认；仍无 → **删除引注并改写** |
| ⚠️ 参考文献有但正文没引 | 多余条目                        | **从参考文献列表删除**                                   |
| ⚠️ 元数据不一致         | 标题/作者与 Zotero 不符         | 按 `metadata.json` 修正                                      |

### 步骤2.5：括注时间排序检查

`normalize_draft.py` 会自动修正同一作者多年引文的年份顺序（如 `（Spence,2002,1973）` → `（Spence,1973,2002）`）。运行归一化后应检查报告中是否有 `括注年份重排` 条目，确认修正无误。

同时，归一化脚本会自动清除参考文献中残留的 HTML 标签（如从 Zotero metadata `title` 字段带入的 `<i>` 标签）。

### 步骤3：修正后重跑

修正完毕后**必须再次运行脚本**，直到报告显示 `🎉 核验通过: 0 个问题`。

### 步骤4：数据→文本一致性核验（实证型论文，条件性执行）

> [!IMPORTANT]
> **仅当论文经过阶段3b（含数据分析章节）且 `stata/parsed_results.json` 存在时执行。**

```bash
python "scripts/results_verifier.py" --draft final_draft.md --parsed stata/parsed_results.json --output reports/results_verification.md
```

脚本自动完成（0 token 消耗）：

- 从 `final_draft.md` 提取所有统计数值（回归系数、标准误、P值、样本量、R²等）
- 从 `stata/parsed_results.json` 加载参考数值
- 自动比对，容差范围内（四舍五入精度差异 ≤0.0015）视为一致
- 不一致的标记为 🔴，产出 `reports/results_verification.md`

修正所有不一致后重跑，直到报告显示 `🎉 核验通过`。

- **检查点保存**

---

## 阶段7：编译 .docx 输出

**目标**：编译为符合《社会学研究》体例的 Word 文档。

> [!IMPORTANT]
> 格式规范以 [journal_format.md](references/journal_format.md) 为唯一权威。

### 步骤1：组装 final_draft.md

> [!CAUTION]
> **进入阶段7前必须 `view_file` 重新读取本文件的阶段7部分（参考文献排序算法 + 编译后验证）**，不得依赖上下文中的早期记忆。

首行一级标题（论文标题）→ 下行作者 → 提要 → 关键词 → 正文（从 `drafts/sec_*.md` 按顺序拼接）→ 参考文献 → 作者单位 → 脚注定义。

### 步骤2：参考文献排序（强制算法）

> [!CAUTION]
> **参考文献排序必须严格执行以下算法，不得凭感觉手动排列：**
>
> 1. **优先使用 `references_formatted.md`**（由 `zotero_extractor.py` 按正确排序自动生成），直接复制其中正文引用的条目即可
> 2. 若需手动排序，规则为：**中文文献（按作者姓氏拼音首字母 A→Z）→ 英文文献（按作者姓氏字母 A→Z）**
> 3. 同一作者多篇：按年份**升序**排列，第二篇起用"——"代替作者姓名
> 4. **中英文文献之间不混排**，中文全部在前，英文全部在后
> 5. 排序完成后，人工扫描确认无中英文混排

### 步骤2.5：归一化预处理（强制，编译前必须运行）

```bash
python "scripts/normalize_draft.py" final_draft.md
```

自动修正提要/关键词/标题/参考文献/作者单位的格式变体，确保编译脚本能正确解析。

### 步骤3：编译

```bash
python "scripts/compile_docx.py" final_draft.md output.docx
```

`compile_docx.py` 支持以下 Markdown 元素的自动识别与转换：

| Markdown 元素 | 转换结果 |
|---------------|----------|
| `![alt](path.png)` | 居中嵌入图片（宽度14cm） |
| `\| col1 \| col2 \|` 表格 | 《社会学研究》三线表（粗顶线/底线 + 细表头线，无竖线） |
| `图X　标题` | 图题（黑体9pt加粗居中） |
| `表X　标题` | 表题（正文段落） |
| `注：内容` | 表注/图注（宋体7.5pt六号） |

### 步骤3.5：图表嵌入验证（有数据分析时执行）

如论文经过阶段3b（数据分析），验证：

1. `figures/` 中的 PNG 文件均存在且可读
2. Markdown 中的 `![...](figures/...)` 路径与实际文件对应
3. 表格数据与 Stata 日志一致

### 步骤4：编译后验证（强制，不得跳过）

> [!CAUTION]
> **编译后必须运行以下验证，确认 Word 文件可正常打开：**

```bash
python -c "from docx import Document; d=Document('output.docx'); print(f'验证通过: {len(d.paragraphs)} 段落')"
```

- 若验证失败（抛出异常），说明编译产出了损坏的文件，**必须排查 compile_docx.py 的脚注 XML 注入逻辑**，或改用 python-docx 直接生成
- 统计字数、参考文献条数，确认与 `final_draft.md` 一致

- **检查点保存**

---

## 阶段8：清理与归档

**保留**：`final_draft.md`、`output.docx`
**归档**（移入 `archive/`）：`citation_whitelist.json`、`metadata.json`、`knowledge_cards/`
**删除**：`checkpoint.json`、`metadata_gaps.log`、`references_formatted.md`、`drafts/`、`reports/`

---

## 纯离线方案（MCP 不可用时）

阶段1的步骤1-2已完全离线运行（本地脚本），仅跳过步骤3的 MCP 语义补充。

- **阶段6替代**：用 `metadata.json` 直接比对，未命中的标记 `[待确认]`
- **阶段7替代**：用 `references_formatted.md` 作为参考文献列表

---

## 附录：Token 成本估算

| 文献规模 | 阶段1-2 (A) | 阶段3-5 (B) | 阶段3b (C, 可选) | 阶段6-8 (D) | 总计（无C） | 总计（有C） |
| -------- | ----------- | ----------- | ----------------- | ----------- | ----------- | ----------- |
| 30篇 | ~17K | ~20K | ~25K | ~5K | ~42K | ~67K |
| 80篇 | ~42K | ~40K | ~30K | ~10K | ~92K | ~122K |
| 150篇 | ~73K | ~60K | ~30K | ~15K | ~148K | ~178K |
