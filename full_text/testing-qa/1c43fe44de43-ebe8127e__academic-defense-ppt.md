---
name: academic-defense-ppt
description: >
  面向科研汇报/学术答辩场景的 PPT 生成工作流。当用户提到"科研答辩"、"学术答辩"、"毕业答辩"、"开题报告"、"组会汇报"、"seminar"、"制作答辩PPT"、"答辩幻灯片"时触发。整合 opendataloader PDF 解析、ppt-master SVG 生成管线、scientific-schematics 科研示意图，以五模块流水线产出高质量学术 PPTX。
license: Private
---

# 科研答辩 PPT 工作流

> 面向科研汇报/学术答辩场景的一体化 PPT 生成 Skill。
> 整合 `ppt-master`（主管线）、`pptx` skill（设计理念 & QA）、`scientific-schematics`（科研示意图），
> 以 **信息提取与约束器 → 主生成器 → 资产服务层 → 后处理器 → 检验器** 五模块流水线运行。

---

## 全局预设：科研答辩风格

| 属性 | 默认值 | 说明 |
|------|--------|------|
| **画布** | 16:9 (1280×720) | 学术答辩标准比例 |
| **基调** | 简洁大气、要点明确、逻辑严谨 | 信息密度适中，每页一个核心论点 |
| **色调** | 深蓝系 (`#003366` 主色) | 学术场景行业惯例，可在确认步骤中定制 |
| **字体** | 中文微软雅黑 / 英文 Calibri | 可在确认步骤中替换 |
| **内容来源** | 严格基于用户提供的素材 | 文本从提取信息中精炼，不凭空添加 |
| **图片** | 所有图片全部收集、登记、分类，不得遗漏 | 关键证据图进主 deck；次要支持图进 backup slides；冗余/重复图仅保留在资产库，不强制进入最终 PPT |

### 科研答辩内容要求

- **标题层**：每页一个简短断言式标题（如"所提出方法在关键指标上实现显著提升"）
- **要点层**：3-5 个关键论据/发现，使用精炼短语，不写长段落
- **证据层**：图表、公式、实验数据，占据页面主要视觉空间
- **注释层**：必要的来源标注、单位说明，字号 ≤12px，不抢视觉焦点
- **逻辑流**：引言→背景→方法→结果→讨论→结论，整体叙事连贯

---

## 统一中间表示（Spec Layer）

以下四个 YAML 文件构成整条流水线的**唯一中间协议**。Module 1 负责产出它们，Module 2-5 必须围绕它们运行，不得仅依赖自然语言接力。

### 1. `deck_config.yaml` — 全局配置

```yaml
# 最小必填字段
presentation_type: "博士答辩"        # 博士答辩 / 硕士答辩 / 组会 / seminar / proposal
target_slides: 20                    # 目标页数（含 backup）
target_duration_min: 30              # 目标时长（分钟）
audience: "答辩委员会"               # 受众
template: "academic_defense"         # 模板名（或 "free_design"）
language: "zh-CN"                    # 主语言
font_scheme:                         # 字体方案
  title_zh: "微软雅黑"
  title_en: "Calibri"
  body_zh: "微软雅黑"
  body_en: "Calibri"
palette:                             # 色板
  primary: "#003366"
  accent: "#0066CC"
  highlight: "#CC0000"
  bg: "#FFFFFF"
  text_primary: "#333333"
  text_secondary: "#666666"
allow_ai_images: true                # 是否允许 AI 补图
enable_backup_slides: true           # 是否启用 backup slides
style_source:                        # 可选：蒸馏风格来源（由 ppt-style-distiller 生成）
  mode: "distilled_style"            # "default" / "distilled_style"
  style_id: "academic_research_talk_cn"    # 学术会议报告风格
  # style_id: "phd_defense_cn"             # 博士学位答辩风格（使用此行时，注释上行）
  style_bank_path: "style_bank/academic_research_talk_cn"
  # style_bank_path: "style_bank/phd_defense_cn"
  reference_strength: "high"         # low / medium / high
  allow_layout_reuse: true
  allow_color_reuse: true
  allow_asset_reuse: false           # 永远禁止复用源素材
```

### 2. `slide_plan.yaml` — 逐页计划

```yaml
slides:
  - page: 1
    slide_type: "cover"
    action_title: "某研究方向的关键方法与结果"
    core_conclusion: null
    key_points: []
    required_images: ["cover_mark.png"]
    optional_images: []
    needs_schematic: false
    needs_formula: false
    notes_outline: "开场问候，介绍题目与汇报结构"
    estimated_duration_min: 1
  # ... 后续各页
```

### 3. `asset_manifest.yaml` — 素材总表

```yaml
assets:
  - filename: "fig3_spectrum.png"
    source: "PDF/Figure 3"
    category: "实验结果"              # 实验结果 / 方法示意 / 装饰 / 公式 / 表格
    placement: "main_deck"           # main_deck / backup / asset_only
    assigned_page: 8
    ai_generated: false
    native_width: 1200           # 原生像素宽度（由 analyze_images.py 自动填充）
    native_height: 800           # 原生像素高度（SVG 放置时不得超出此值）
  - filename: "system_diagram.png"
    source: "AI generated"
    category: "方法示意"
    placement: "main_deck"
    assigned_page: 5
    ai_generated: true
  # ...
```

### 4. `style_contract.yaml` — 样式锁定

```yaml
theme_colors:
  primary: "#003366"
  accent: "#0066CC"
  highlight: "#CC0000"
font_family:
  title: "'微软雅黑', 'Calibri', sans-serif"
  body: "'微软雅黑', 'Calibri', sans-serif"
font_size_hierarchy:
  slide_title: 36          # px
  section_header: 24
  body: 16
  caption: 12
margins:
  left: 40
  right: 40
  top: 0
  bottom: 35
chart_spec:
  axis_label_size: 12
  legend_position: "bottom-right"
  colorblind_safe: true
citation_format: "APA"      # APA / IEEE / Nature / 自定义
forbidden_elements:
  - "accent lines under titles"
  - "decorative clip-art"
  - "word clouds"
  - "3D chart effects"
```

> 后续所有模块不得仅依赖自然语言接力，必须以 `deck_config.yaml + slide_plan.yaml + asset_manifest.yaml + style_contract.yaml` 为统一输入输出协议。

---

## 流水线总览

```
┌─────────────────────────────────────────────────────────────┐
│  Module 1: 信息提取与约束器 (Extractor & Constrainer)         │
│    PDF解析 [主] opendataloader → Markdown素材                 │
│           [备] PyMuPDF（ODL失败时自动切换）                    │
│    图片收集 → 分析归类 → asset_manifest.yaml                  │
│    内容精炼 → source_digest.md + slide_plan.yaml              │
│    ⛔ BLOCKING A: 内容冻结                                    │
│                          ↓                                    │
│  Module 2: 主生成器 (Main Generator)                          │
│    输入: deck_config / slide_plan / asset_manifest / style    │
│    ⛔ BLOCKING B: 样式冻结                                    │
│    design_spec.md 输出（设计落地文件）                          │
│    SVG 逐页生成（按 slide_plan + 页型约束）+ 演讲备注          │
│    ↕ Module 3 资产服务层按页按需调用                           │
│                          ↓                                    │
│  Module 4: 后处理器 (Post-processor)                          │
│    total_md_split → finalize_svg → svg_to_pptx                │
│                          ↓                                    │
│  Module 5: 检验器 (Validator)                                 │
│    SVG质量检查 + 内容可追溯核查 + 子代理视觉QA                  │
│    不通过 → 回退修正 → 重新检验                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 会话初始化：加载历史记忆

> 每次执行本 skill 前，先读取本地记忆文件，将历史经验纳入约束：

**Step 1：加载通用经验**
```
read_file skills/academic-defense-ppt/memory/lessons.md
```
将 `lessons.md` 中的规则融入后续所有模块的决策。若文件不存在，跳过。

**Step 2：加载风格纠正记录（style_bank 联动）**

若 `deck_config.yaml` 中已指定 `style_source.style_id`，额外加载：
```
read_file skills/academic-defense-ppt/memory/style_feedback.yaml
```
从 `style_feedback.yaml` 中提取对应 `style_id` 下的 `corrections` 列表，将其作为**高优先级覆盖规则**，合并进 Module 2.2a 检索到的 `style_contract_variant.yaml`：
- `corrections[].override_field` 中的字段值**替换**原 style_contract 中的对应字段
- `corrections[].note` 记录原因，供生成时参考

若文件不存在或对应 style_id 无记录，跳过。

---

## Module 1: 信息提取与约束器

### 1.1 PDF 素材解析

🚧 **GATE**: 用户已提供 PDF 文件路径或素材描述。

#### 主路径：opendataloader（ODL）

使用 opendataloader 解析 PDF 为 AI 可读格式：

```powershell
conda run -p "<ODL_ENV_PATH>" python -c "import opendataloader_pdf; opendataloader_pdf.convert(input_path=[r'<PDF路径>'], output_dir=r'<EXPORT_DIR>/opendataloader', format='json,markdown', use_struct_tree=True)"
```

**输出位置**: `<EXPORT_DIR>/opendataloader/<文件名>/`
- `parsed_md/` — Markdown 全文（主要 AI 输入源）
- `parsed_json/` — JSON 结构化数据（表格/页码定位时使用）

> ⚠️ ODL 已知局限：部分 PDF 会触发 Java `Comparison method violates its general contract` 异常（exit code 1）。可先尝试 `pages='1-5'` 缩小范围绕过；若整份 PDF 均无法解析，则进入备选路径。

#### 备选路径：PyMuPDF（ODL 失败时使用）

当 ODL 返回非零退出码或输出为空时，自动切换到 PyMuPDF 进行解析：

```python
import fitz, os

pdf_path = r"<PDF路径>"
out_dir  = r"<项目路径>/extracted"
img_dir  = os.path.join(out_dir, "images")
os.makedirs(img_dir, exist_ok=True)

doc = fitz.open(pdf_path)

# 提取全文
full_text = ""
for i, page in enumerate(doc):
    full_text += f"\n\n--- Page {i+1} ---\n\n" + page.get_text()

with open(os.path.join(out_dir, "full_text.md"), "w", encoding="utf-8") as f:
    f.write(full_text)

# 提取嵌入图片
img_count = 0
for i, page in enumerate(doc):
    for j, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:   # CMYK → RGB
            pix = fitz.Pixmap(fitz.csRGB, pix)
        pix.save(os.path.join(img_dir, f"page{i+1}_img{j+1}.png"))
        img_count += 1
        pix = None

doc.close()
print(f"Text saved. Images extracted: {img_count}")
```

**PyMuPDF 输出**：
- `extracted/full_text.md` — 纯文本全文（替代 ODL 的 `parsed_md/`）
- `extracted/images/page*_img*.png` — 嵌入图片（替代 ODL 的图片输出）

> **注意事项**：
> - PyMuPDF 不解析 PDF 结构树，文本顺序可能与阅读顺序有偏差（尤其双栏排版），需人工校验
> - 仅提取嵌入矢量/位图图片，页面截图（如渲染整页图像）需另行处理
> - 确认 PyMuPDF 已安装：`pip show pymupdf`；若未安装：`pip install pymupdf`

### 1.2 图片素材收集

> ⚠️ **不得遗漏用户提供的任何图片**。所有科研图表、实验结果、示意图必须全部收集并登记到 `asset_manifest.yaml`。

操作步骤：
1. 从 PDF 解析结果中提取所有图片 → 收集到项目 `images/` 目录
2. 用户额外提供的图片 → 同样移入 `images/`
3. 运行图片分析：
   ```bash
   python3 skills/ppt-master/scripts/analyze_images.py <project_path>/images
   ```
4. 输出图片清单，标注每张图的类别（实验结果 / 示意图 / 装饰 / 公式）和建议用途
5. 生成 `asset_manifest.yaml`，为每张图标注 `placement`（main_deck / backup / asset_only）

> "全部收集"指进入 `asset_manifest.yaml` 统一管理，不等于全部强制进入最终主 deck。关键证据图优先进入主 deck，次要支持图进入 backup slides，冗余或重复图可仅保留在资产库。

### 1.3 内容精炼与约束

从 Markdown 素材中提取并精炼内容，遵循以下约束：

| 约束规则 | 说明 |
|----------|------|
| **素材忠实** | 所有文本内容必须来源于提取的素材，不得凭空编造数据或结论 |
| **精炼表达** | 长段落 → 短句/关键词，每页文本不超过 60 字（中文）或 80 词（英文） |
| **术语一致** | 全文统一使用相同的学术术语，不随意替换同义词 |
| **数据精确** | 数值、单位、公式必须与原文完全一致 |
| **图文对应** | 每个引用的图表必须有对应的文字说明和标注 |
| **图片分级** | 所有图片必须纳入资产清单，但最终使用分为：主 deck / backup / 仅保留资产库 |

同时生成 `source_digest.md`（素材忠实摘要），用于后续检验器的可追溯性核查：

#### `source_digest.md` 结构

```markdown
# Source Digest

## 研究主线
[一句话概括研究目标和方法]

## 关键贡献
1. [贡献1]
2. [贡献2]
3. ...

## 核心数据
| 指标 | 数值 | 单位 | 出处页码 |
|------|------|------|----------|
| ...  | ...  | ...  | ...      |

## 图表索引
| 图表编号 | 描述 | 原文位置 | 对应 asset |
|----------|------|----------|-----------|
| Fig.1    | ...  | p.3      | fig1_xxx.png |

## 禁止误改项
- [不得修改的关键术语、数值、结论列表]
```

**输出**：
- `source_digest.md` — 素材忠实摘要（可追溯性核查依据）
- `deck_config.yaml` — 全局配置（初步填充，BLOCKING A 确认后锁定）
- `slide_plan.yaml` — 逐页计划
- `asset_manifest.yaml` — 素材总表

> 结构化内容大纲（Markdown）作为辅助产物可同步输出，但不再是唯一中间结果。

### 1.4 内容冻结（⛔ BLOCKING A）

> 在开始模板选择和样式设计之前，必须先冻结内容结构。这是第一个硬停点。

⛔ **BLOCKING**: 必须向用户展示以下内容并等待确认/修改，确认前不得进入 Module 2。

**确认清单**：

| # | 确认项 | 说明 |
|---|--------|------|
| 1 | **总页数预算** | 主 deck XX 页 + backup XX 页 |
| 2 | **章节顺序** | 封面→引言→背景→方法→结果→讨论→结论→致谢→backup |
| 3 | **必保留页面** | 哪些页面不可删减 |
| 4 | **可压缩内容** | 哪些内容可移入 backup |
| 5 | **主证据图** | 哪些图片是核心论据，必须进入主 deck |
| 6 | **附录/备份页** | 是否启用，放哪些补充材料 |
| 7 | **主结论链条** | 结论 1→证据→结论 2→证据→... 是否正确 |

**呈现格式**：

```markdown
## 🔒 内容冻结确认（BLOCKING A）

基于素材分析，内容结构如下：

- **主 deck**: XX 页（封面→引言→背景→方法×3→结果×4→讨论→结论→致谢）
- **backup**: XX 页（补充实验、推导细节、额外对比）
- **主证据图**: fig3_spectrum.png, fig5_comparison.png, ...（共 X 张）
- **主结论链条**:
  1. [贡献1] ← 由结果页 X 支撑
  2. [贡献2] ← 由结果页 Y 支撑
  3. ...

请确认或修改以上内容结构。确认后内容框架将锁定，后续仅调整视觉样式。
```

**✅ Checkpoint — 内容冻结确认完成，`deck_config.yaml` 和 `slide_plan.yaml` 锁定，进入 Module 2**

---

## Module 2: 主生成器

> Module 2 的输入是 Module 1 产出的结构化 spec 文件，而非仅仅是原始 PDF/Markdown：
> - `deck_config.yaml` — 全局配置
> - `slide_plan.yaml` — 逐页计划
> - `asset_manifest.yaml` — 素材总表
> - `style_contract.yaml` — 样式锁定（在 BLOCKING B 确认后生成）
>
> `ppt-master` 是唯一主生成器，负责把结构化 spec 转换成逐页 SVG；其他 skill 不直接接管整套 deck 的生成权。
> `design_spec.md` 是面向 ppt-master executor 的设计落地文件，从上述 YAML 协议派生，而非唯一规范来源。

### 2.1 项目初始化

```bash
python3 skills/ppt-master/scripts/project_manager.py init <project_name> --format ppt169
python3 skills/ppt-master/scripts/project_manager.py import-sources <project_path> <source_files...> --move
```

### 2.2 模板选择

科研答辩场景默认推荐 `academic_defense` 模板。也可使用用户自定义模板（见 [自定义模板扩展](#自定义模板扩展)）。

> 如用户已有自定义学术模板，优先使用自定义模板。

选定模板后复制模板文件：
```bash
cp skills/ppt-master/templates/layouts/<template_name>/*.svg <project_path>/templates/
cp skills/ppt-master/templates/layouts/<template_name>/design_spec.md <project_path>/templates/
```

### 2.2a 风格检索（Style Retrieval）

> 在样式冻结前，检索是否存在已蒸馏的参考风格，以提升生成质量。

**检索步骤**：

1. 检查 `style_bank/` 是否存在风格文件夹：
   ```
   list_dir style_bank/
   ```
2. 根据 `deck_config.yaml` 中 `style_source.style_id` 或任务类型，选择风格：
   - 学术会议报告 → `academic_research_talk_cn`
   - **博士学位答辩 → `phd_defense_cn`**（包含 TOC分隔页/本章小结/成果列表等答辩特有结构）
   - 用户未指定时：答辩任务默认 `phd_defense_cn`，学术报告默认 `academic_research_talk_cn`
   ```
   list_dir style_bank/
   # 按选定风格加载：
   read_file style_bank/<style_id>/style_contract_variant.yaml
   read_file style_bank/<style_id>/design_spec_addendum.md
   ```
3. 将 `style_contract_variant.yaml` 中的规则与默认 `style_contract.yaml` 合并：
   - 优先使用蒸馏风格的 `theme_colors`、`font_size_hierarchy`、`text_budget`、`layout_pattern_preferences`
   - 保留 `deck_config.yaml` 中用户已显式指定的字段
   - `allow_asset_reuse` 始终保持 `false`

4. 若 `deck_config.yaml` 中 `style_source.mode == "default"` 或 style_bank 为空，跳过此步，使用默认风格。

> **关键约束**：风格检索只影响视觉规则（颜色、字号、布局偏好、标题风格）；不影响内容规划（slide_plan.yaml 已在 BLOCKING A 锁定）。

---

### 2.3 样式冻结（⛔ BLOCKING B）

> 此步仅负责确认视觉和模板相关内容，内容结构已在 BLOCKING A 中冻结。确认完成后，后续所有步骤自动执行。

⛔ **BLOCKING**: 必须向用户展示推荐方案并等待确认/修改：

| # | 确认项 | 默认推荐 | 蒸馏风格推荐（若已加载） |
|---|--------|----------|--------------------------|
| 1 | **画布格式** | 16:9 (1280×720) | 16:9 |
| 2 | **风格来源** | 默认学术风 | 学术报告→`academic_research_talk_cn`（7份报告,277页）; 答辩→`phd_defense_cn`（2份答辩,97页） |
| 3 | **主题色** | 深蓝 `#003366` + 强调蓝 `#0066CC` + 强调红 `#CC0000` | `#1F3A8F` + `#2B5CAE` + `#C0392B` |
| 4 | **字体方案** | 中文：微软雅黑 / 英文：Calibri | 同默认 |
| 5 | **标题风格** | 描述式 / 断言式 | **断言式（claim-based）为主**：结果页标题直接陈述结论 |
| 6 | **结果页布局** | 图文混排 | **图主文辅**：主图占 40–65%，2–3 条简短注释 |
| 7 | **文字预算** | 正文 ≤ 5 条 | **结果页 ≤ 3 条**，每条 ≤ 16 字 |
| 8 | **禁用元素** | 标题下划线 / 3D 图表 / 词云 | 同默认 + 禁用泛标题"结果""实验""方法" |

**呈现格式（蒸馏风格已加载时）**：

```markdown
## 🎨 样式冻结确认（BLOCKING B）

基于您的素材和内容结构，并结合已蒸馏的参考风格 `academic_research_talk_cn`
（参考了已脱敏的公开风格样本），我的视觉推荐如下：

1. **画布**: 16:9 标准演示 (1280×720)
2. **风格**: 中文学术研究报告风格——图主文辅、断言式标题、简洁学术
3. **主题色**: 深蓝 #1F3A8F / 强调蓝 #2B5CAE / 强调红 #C0392B
4. **字体**: 标题 微软雅黑 34pt / 正文 18pt / 图注 10pt / 英文 Calibri
5. **结果页规则**: 主图占 40–65%，标题陈述结论，正文 ≤ 3 条
6. **图片**: XX 张主证据图进入主 deck，XX 张进入 backup
7. **禁用**: 泛标题"结果/实验/方法"、3D 图表、词云、段落式正文

请确认或修改以上视觉方案。
```

确认后，生成 `style_contract.yaml` 并锁定。

### 2.4 页面类型约束（Slide Type Rules）

SVG 生成前，必须对照 `slide_plan.yaml` 中每页的 `slide_type` 应用以下约束：

| slide_type | 约束 |
|---|---|
| **cover** | 论文标题居中或偏上，作者/导师/院校/日期信息齐全；院校 logo 必须出现；不放正文内容 |
| **outline** | 清晰的章节导航结构；当前汇报位置可高亮；不堆砌文字 |
| **motivation** | 以问题/痛点驱动；配背景图或领域概览图；标题为疑问句或挑战陈述；正文 ≤ 3 条 |
| **background** | 文献概况或技术现状综述；可使用时间线或对比表格；引用须标注来源 |
| **method-overview** | 必须有流程图或系统图作为主视觉元素；图主文辅；不堆砌公式；只保留主链路，细节移入 method-detail |
| **method-detail** | 可展示公式推导、算法伪代码、参数设置；信息密度可高于其他页型；须与 method-overview 有明确层级关系 |
| **experimental-setup** | 实验环境/设备/参数表格为主；可配实验装置照片；标注关键实验条件 |
| **result-main** | 必须以图表/结果图为主要视觉元素；标题必须是结论句（非描述句）；正文不超过 3 条；必须写清 metric、单位、实验条件 |
| **result-ablation** | 消融实验或参数分析；使用对比表格或分组柱状图；标题点明哪个因素最重要 |
| **comparison** | 与 baseline/SOTA 的定量对比；表格或柱状图为主；标题写出本方法的优势结论；标注公平对比条件 |
| **discussion** | 优势与局限并列分析；可引用其他工作进行对比讨论；不引入新实验数据 |
| **limitation** | 坦诚列出 2-3 条局限；可附未来工作方向；不要写成负面总结 |
| **conclusion** | 仅保留 3-5 条核心贡献；不引入新图；不出现新术语；各条应与前文结果页一一对应 |
| **acknowledgement** | 简洁收尾；致谢导师/合作者/基金；可放联系方式；不放正文内容 |
| **backup** | 用于补充实验、额外图表、推导过程和答疑材料；可容纳次要支持图；不纳入主叙事节奏；页面右上角标注 "Backup" |

### 2.5 设计规范输出

确认后，读取 `templates/design_spec_reference.md` 模板，生成完整的 `<project_path>/design_spec.md`，包含 I-XI 所有章节。

> 必须先 `read_file templates/design_spec_reference.md`，输出后逐节自查。
> `design_spec.md` 是面向 ppt-master executor 的设计落地文件，其内容必须与 `style_contract.yaml` 和 `slide_plan.yaml` 保持一致。
> `ppt-master` 是唯一主生成器，负责把结构化 spec 转换成逐页 SVG；其他 skill 不直接接管整套 deck 的生成权。

### 2.6 SVG 逐页生成

> SVG 逐页生成必须严格服从 `slide_plan.yaml` 中定义的 slide type 及其对应约束（见 2.4）。

读取角色定义（按需选择风格文件）：
```
Read references/executor-base.md
Read references/executor-general.md    # 学术答辩默认使用 general
```

**执行纪律**：
- 确认全局设计参数后，逐页顺序生成 SVG → `<project_path>/svg_output/`
- **禁止批量生成**（如 5 页一组）
- **禁止委托子代理生成 SVG**
- 图标使用 `<use data-icon="chunk/xxx" .../>` 占位符
- 当 `slide_plan.yaml` 中某页标记 `needs_schematic: true` 时，调用 Module 3 资产服务层生成对应示意图后再继续该页 SVG

**科研答辩特有布局要求**：
- **封面页**: 论文标题、作者、导师、院校 logo、日期
- **目录页**: 清晰的章节导航
- **背景/引言页**: 研究意义、文献概况，配背景示意图
- **方法页**: 技术路线图/流程图，图主文辅
- **结果页**: 实验数据图表为主，每页聚焦一个核心发现
- **讨论页**: 对比分析，优势与局限
- **结论页**: 3-5 条核心贡献总结
- **致谢页**: 简洁收尾

**排版要点**（整合自 pptx skill 设计理念）：
- 每页必须有视觉元素（图/表/图标/示意图），禁止纯文本页
- 布局多样化——双栏、图文对照、数据卡片、时间线交替使用
- 标题 ≥ 36px，正文 14-16px，注释 ≤ 12px
- 左对齐正文，居中仅用于标题
- 页边距 ≥ 40px，元素间距 ≥ 20px

**图片放置原则（防止强行放大 / 比例失真）**：

> PowerPoint 将 SVG 转换为可编辑形状时会忽略 `preserveAspectRatio`，直接按 `width/height` 属性强制拉伸图片。`fix_image_aspect.py` 后处理步骤会自动修正，但主动设置正确尺寸是第一道防线。

| 规则 | 说明 |
|------|------|
| **不超原生分辨率** | 从 `asset_manifest.yaml` 读取 `native_width`/`native_height`，SVG 声明的 `width` 和 `height` **均不得超过**对应原生值 |
| **保持原生比例** | `width / height` 必须等于（或接近）`native_width / native_height`，允许 ±2% 误差；不得任意指定 |
| **背景装饰图例外** | cover/ending 页使用 `preserveAspectRatio="xMidYMid slice"` 的全幅背景图，允许裁剪填充；若原图高度 < 720px（如宽幅全景图），接受轻微放大但须在 asset_manifest 中标注 `blurry_acceptable: true` |
| **实验结果图** | 科研数据图 category=实验结果 的图片，**禁止放大**，宁可留白也不拉伸 |
| **尺寸计算方法** | 确定容器高度 H（px），按 `display_w = H × (native_w / native_h)` 计算显示宽度；若超出容器宽度，则反过来按宽度推算高度 |

### 2.7 演讲备注生成

所有 SVG 生成完毕后，批量生成 `<project_path>/notes/total.md`。

格式：每页 `# <编号>_<页名>`，含 2-5 句脚本、`要点: ① ② ③`、`时长: X 分钟`，页间以 `[过渡]` 衔接。

**✅ Checkpoint — SVG + 备注全部生成，进入 Module 4**

---

## Module 3: 资产服务层（Asset Services）

> 资产服务层不是一个严格顺序执行的独立阶段，而是由 `slide_plan.yaml` 驱动，在页面生成过程中按需调用，为特定页面提供 schematic、chart、icon 等视觉资产。当 Module 2 在逐页生成 SVG 时遇到需要补充视觉素材的页面，即时调用本模块的对应服务。

### 3.1 科研示意图（scientific-schematics）

按页调用：当 `slide_plan.yaml` 中某页标记 `needs_schematic: true` 时触发，为该页生成对应的科研示意图。

用于生成：神经网络架构图、光学系统示意图、实验流程图、信号通路图等。

```bash
python scripts/generate_schematic.py "<详细描述>" -o <project_path>/images/<名称>.png --doc-type presentation
```

**提示词要求**：
- 明确图表类型（流程图/架构图/通路图等）
- 包含具体组件和标注
- 指定流向（从左到右/从上到下）
- 要求色盲友好配色
- 配色须与 `style_contract.yaml` 中的主题色协调

**质量阈值**: presentation 级别 ≥ 6.5/10，若用于论文答辩级可提高至 thesis (8.0/10)。

生成完成后须更新 `asset_manifest.yaml`，登记新生成的图片。

### 3.2 图表模板（ppt-master charts）

按页调用：当某页需要使用特定可视化类型（柱状图、时间线、流程图等）时，从 52 种模板中选取参考。

模板位于 `skills/ppt-master/templates/charts/`。

使用前必须：
```
read_file templates/charts/<chart_name>.svg
```
提取布局坐标和结构逻辑作为创作参考，但不照搬——适配本项目的配色和数据。

### 3.3 图标库（ppt-master icons）

按页调用：在 SVG 生成过程中，为各页面选取合适的图标点缀。

6700+ 矢量图标，三个风格库：

| 库 | 风格 | 学术答辩推荐 |
|----|------|-------------|
| `chunk` | 填充·直线几何 | ✅ **默认** |
| `tabler-filled` | 填充·贝塞尔曲线 | 需要圆润风格时 |
| `tabler-outline` | 描边线条 | 轻量风格时 |

> ⚠️ **同一 PPT 只用一个图标库**，不混用。

搜索图标：
```bash
ls skills/ppt-master/templates/icons/chunk/ | grep <关键词>
```

---

## Module 4: 后处理器

🚧 **GATE**: Module 2 完成，所有 SVG 在 `svg_output/`，备注在 `notes/total.md`。

> ⚠️ 以下三步**必须逐一执行**，每步确认成功后再执行下一步。
> ❌ 绝不在同一代码块中执行多步。

**Step 4.1** — 拆分演讲备注：
```bash
python3 skills/ppt-master/scripts/total_md_split.py <project_path>
```

**Step 4.2** — SVG 后处理（图标嵌入/图片裁切/文本扁平化）：
```bash
python3 skills/ppt-master/scripts/finalize_svg.py <project_path>
```

**Step 4.3** — 导出 PPTX：
```bash
python3 skills/ppt-master/scripts/svg_to_pptx.py <project_path> -s final
```

> ❌ 绝不用 `cp` 替代 `finalize_svg.py`
> ❌ 绝不从 `svg_output/` 直接导出——必须从 `svg_final/` 导出

**输出**: `exports/<project_name>_<时间戳>.pptx`

**✅ Checkpoint — PPTX 导出完成，进入 Module 5 检验**

---

## Module 5: 检验器

### 5.1 SVG 质量检查

```bash
python3 skills/ppt-master/scripts/svg_quality_checker.py <project_path>
```

检查禁用特性、兼容性问题。

### 5.2 内容核查

```bash
python -m markitdown <output.pptx>
```

核查项：
- [ ] 所有文本内容与素材一致，无编造
- [ ] 数据/数值/单位/公式准确
- [ ] 术语全文统一
- [ ] 无遗留占位符文本（`grep -iE "xxxx|lorem|ipsum|placeholder"`）
- [ ] `asset_manifest.yaml` 中标记为 `main_deck` 的图片均已出现在对应页面，无遗漏
- [ ] `asset_manifest.yaml` 中标记为 `backup` 的图片出现在 backup 页面中
- [ ] 每个关键数据、结论、公式都可以追溯到 `source_digest.md` 或原始解析内容中的具体位置

### 5.3 视觉 QA（子代理检查）

> 来源于 pptx skill 的 QA 理念：**假设存在问题，你的任务是找到它们。**

将幻灯片转换为图片后，使用子代理（fresh eyes）检查：

```
视觉检查这些幻灯片。假设存在问题——找出它们。

检查项：
- 元素重叠（文字穿过形状、线条穿过文字）
- 文本溢出或在边缘/框边界被截断
- 元素间距过近（< 20px）或间距不均
- 页边距不足（< 40px）
- 低对比度文本或图标
- 图表数据标注是否清晰可读
- 学术规范：引用格式、单位标注、坐标轴标签
- 逻辑流：页面顺序是否符合论文结构

逐页列出发现的所有问题，包括细微问题。
```

### 5.4 修正循环

1. 收集所有问题 → 分类（内容/布局/格式）
2. 修正 SVG 源文件
3. 重新执行 Module 4 后处理
4. 重新检验受影响的页面
5. 直到零关键问题通过

### 5.5 会话记忆写入

> 检验通过后，将本次会话的关键信息追加到本地记忆文件，供后续会话学习。

**操作步骤**：
1. 将以下 JSON 对象追加到 `memory/session_log.jsonl`（每行一条 JSON）
2. 若发现新的通用规律，同步更新 `memory/lessons.md` 对应分类
3. 若遇到新的已知 bug / 绕过方案，追加到 `memory/known_issues.yaml`
4. **若发现已使用的 style_bank 规则与实际生成效果存在偏差，写入 `memory/style_feedback.yaml`**

```jsonc
// 追加到 memory/session_log.jsonl
{
  "date": "<YYYY-MM-DD>",
  "template": "<使用的模板 ID>",
  "style_id": "<使用的 style_id，如 academic_research_talk_cn>",
  "slide_count": 0,
  "pdf_title": "<论文标题>",
  "model": "<使用的模型>",
  "issues": [],      // 本次遇到的问题（字符串数组）
  "fixes": [],       // 对应解决方案
  "quality_score": 0 // svg_quality_checker 通过率 0-100
}
```

**style_feedback.yaml 写入规则**（仅在发现风格规则偏差时触发）：

```yaml
# skills/academic-defense-ppt/memory/style_feedback.yaml
academic_research_talk_cn:
  corrections:
    - date: "YYYY-MM-DD"
      override_field: "font_sizes.body"
      override_value: 16
      original_value: 18
      note: "18pt正文在 ppt-master 渲染后过大，实测16pt更合适"
    - date: "YYYY-MM-DD"
      override_field: "density_by_type.result_main"
      override_value: "medium (≤3 figures + ≤2 bullets)"
      note: "3图在小尺寸SVG中拥挤，改为≤2 bullets"

phd_defense_cn:
  corrections: []
```

> **写入触发条件**（满足任一即触发）：
> - `quality_score < 80` 且能归因到某个 style_contract 规则
> - 用户在审核时明确指出某个视觉规则"不对"
> - 生成结果与 `design_spec_addendum.md` 描述严重不符

**✅ Checkpoint — 记忆写入完成，本次会话结束**

---

## 自定义模板扩展

ppt-master 支持通过 `workflows/create-template.md` 工作流创建全局模板。

### 添加自定义学术模板步骤

1. **准备参考**: 提供你的院校/课题组 PPT 模板（.pptx 文件）或风格描述
2. **启动工作流**:
   ```
   Read skills/ppt-master/workflows/create-template.md
   ```
3. **提供模板信息**:

   | 项目 | 说明 |
   |------|------|
   | 模板 ID | 如 `lab_academic_defense`，ASCII 命名 |
   | 显示名称 | 如 "通用学术答辩模板" |
   | 类别 | `scenario`（场景特定模板） |
   | 适用场景 | 学术答辩、课题组汇报、学术会议 |

4. **生成模板文件**: 工作流会产出 5 个标准 SVG 模板 + `design_spec.md`，存入 `templates/layouts/<模板ID>/`
5. **注册索引**: 自动更新 `layouts_index.json`，后续项目可直接选用

### 自定义模板设计要点

- 封面须包含院校 logo 占位、导师信息区域
- 内容页预留大面积图表区域（科研展示需要）
- 页脚统一放置页码 + 课题组/院校标识
- 色彩方案应与院校 VI 一致
- 提供至少 2 种内容布局变体（图左文右 / 图上文下）

---

## 模型能力适配

> 当前流水线以顶级模型为基准设计。若检测到模型输出质量不足（如 YAML 结构错误、SVG 布局混乱、忽略约束规则），自动降级至对应补偿模式。

### 能力分级

| 等级 | 典型模型 | 特征 | 适用模式 |
|------|---------|------|----------|
| **Tier 1（完整）** | Claude 4.5+、GPT-5.4、Gemini 3.0+ | 严格遵守规范、能自主处理边界情况 | 完整五模块流水线 |
| **Tier 2（标准）** | Claude 4、GPT-5.3、Gemini 2.0 Pro | 基本规范遵守，偶有遗漏 | 流水线 + 每步验证 |
| **Tier 3（简化）** | GPT-5.2、较弱模型 | 频繁遗漏约束、YAML 结构不稳定 | 模板填充模式（见下） |

### Tier 3 补偿机制（模板填充模式）

1. **模板优先**：不生成自由布局 SVG，仅在模板 SVG 中填充占位文本和图片路径
2. **逐步确认**：每个 YAML 文件生成后，让模型逐字段重复一遍关键值，确认无误再继续
3. **显式 schema**：提供完整 YAML 结构，模型只填写 `[VALUE]` 占位，不修改结构
4. **缩小批次**：每次生成 1 页 SVG，立即用 `svg_quality_checker.py` 验证，错误则当场修正
5. **禁止自由设计**：所有 `x/y/width/height` 坐标必须来自模板参考值，禁止自行计算新坐标

### 每模块验证检查点

每个模块完成后，执行以下验证，**验证失败则修正后再继续**：

| 模块 | 验证项 |
|------|--------|
| Module 1 完成后 | `deck_config.yaml` 和 `slide_plan.yaml` 结构完整、无缺失字段；`asset_manifest.yaml` 中每张图片有 `native_width/height` |
| Module 2 每页完成后 | 图片 `width/height` ≤ `native_width/height`；无 `<style>`/`class`/`foreignObject`；无模板占位符残留 |
| Module 4 完成后 | `svg_quality_checker.py` 错误数为 0 |
| Module 5 完成后 | 内容可追溯至 `source_digest.md`；关键数据与原文一致 |

---

## SVG 技术约束（不可违反）

继承自 ppt-master `shared-standards.md`：

**禁用特性**: `mask` | `<style>` | `class` | 外部 CSS | `<foreignObject>` | `textPath` | `@font-face` | `<animate*>` | `<script>` | `<iframe>` | `<symbol>`+`<use>`

**PPT 兼容替代方案**:

| 禁用 | 替代 |
|------|------|
| `rgba()` | `fill-opacity` / `stroke-opacity` |
| `<g opacity>` | 子元素逐一设置 opacity |
| `<image opacity>` | 覆盖遮罩层 |

---

## 快速参考卡片

```
# 完整流程一览

# Module 1: 信息提取
conda run -p ".../opendataloader/env" python -c "import opendataloader_pdf; ..."
python3 skills/ppt-master/scripts/analyze_images.py <project>/images
# 输出: source_digest.md + deck_config.yaml + slide_plan.yaml + asset_manifest.yaml
# ⛔ BLOCKING A: 内容冻结确认

# Module 2: 主生成
python3 skills/ppt-master/scripts/project_manager.py init <name> --format ppt169
python3 skills/ppt-master/scripts/project_manager.py import-sources <project> <files> --move

# Module 2.2a: 风格检索（可选，若 style_bank 已有蒸馏风格）
# list_dir style_bank/
# read_file style_bank/academic_research_talk_cn/style_contract_variant.yaml
# read_file style_bank/academic_research_talk_cn/design_spec_addendum.md
# → 合并到 style_contract.yaml

# ⛔ BLOCKING B: 样式冻结确认 → style_contract.yaml → design_spec.md → SVG 逐页生成 → 备注

# Module 3: 资产服务层（由 slide_plan 驱动，按需调用）
python scripts/generate_schematic.py "<描述>" -o <project>/images/xxx.png --doc-type presentation
ls skills/ppt-master/templates/icons/chunk/ | grep <keyword>

# Module 4: 后处理（逐步执行）
python3 skills/ppt-master/scripts/total_md_split.py <project>
python3 skills/ppt-master/scripts/finalize_svg.py <project>
python3 skills/ppt-master/scripts/svg_to_pptx.py <project> -s final

# Module 5: 检验
python3 skills/ppt-master/scripts/svg_quality_checker.py <project>
python -m markitdown <output.pptx>
# + 可追溯性核查（对照 source_digest.md）
# + 子代理视觉 QA
```

## 蒸馏风格快速参考

### 已蒸馏风格库

| style_id | 路径 | 语料规模 | 适用场景 |
|----------|------|----------|----------|
| `academic_research_talk_cn` | `style_bank/academic_research_talk_cn/` | 7份, 277页 | 学术会议报告 / 组会汇报 / seminar |
| `phd_defense_cn` | `style_bank/phd_defense_cn/` | 2份, 97页 | 博士学位答辩 |

### 风格库文件说明（两个风格库结构相同）

| 文件 | 用途 |
|------|------|
| `style_contract_variant.yaml` | 可执行风格规则（颜色/字号/文字预算/禁用项） |
| `design_spec_addendum.md` | 自然语言设计补充（layout/text/visual 行为） |
| `layout_patterns.yaml` | 可复用版式模式（含版式结构描述） |
| `visual_grammar.yaml` | 视觉层规则（字体/颜色/图表规则） |
| `rhetorical_grammar.yaml` | 文字层规则（标题风格/正文/标注/叙事） |
| `deck_narrative_profile.yaml` | 参考PPT的叙事结构与章节分析 |
| `style_profile.yaml` | 蒸馏元数据（来源/统计/总体概况） |

### 最佳实践

**academic_research_talk_cn**（来自公开脱敏的学术报告样本）：
- 结果页标题：断言式，直接陈述贡献
- 结果页布局：1张主图 + 1条引用 + 0-2条注释
- 每页最多4个文字块；结果页≤3条正文
- Section 切换：重复大纲页，高亮当前章节

**phd_defense_cn**（来自公开脱敏的答辩样本）：
- 标题格式：章节编号前缀 `N.章节名称`（贯穿全章）
- TOC分隔页：每章前插入，当前章节高亮，其余置灰
- 本章小结：每研究章末必有，动词起句，列出3-5条创新贡献
- 答辩末尾：总结展望 → 发表论文 → 致谢 → Q&A
