---

name: ppt-style-distiller
description: >
从科研会议、学术报告、答辩、组会或课程报告 PPTX/PDF 中蒸馏可复用的风格知识。
当用户要求分析、学习、蒸馏、归纳、复用 PPT 风格、排版、叙事方式、标题风格、
学术表达方式，或生成 style_bank / layout_patterns / visual_grammar /
rhetorical_grammar / style_contract_variant 时触发。
本 skill 不直接生成最终 PPT，而是作为上游风格知识层，为 academic-defense-ppt、
ppt-master 或其他 PPT 生成工作流提供结构化风格文件。
license: Private
----------------

# PPT Style Distiller — 科研 PPT 风格蒸馏 Skill

## 0. Skill 定位

本 skill 用于从一批科研 PPT 中蒸馏可复用的**视觉语法、排版模式、叙事结构和学术表达风格**。

它解决的问题不是“如何生成一份 PPT”，而是：

> 如何把参考 PPT 中稳定、可复用、可迁移的设计与表达规律，转化为后续 PPT 生成工作流可调用的结构化风格知识。

本 skill 的输出不是最终 `.pptx`，而是风格知识库文件，例如：

* `style_profile.yaml`
* `deck_narrative_profile.yaml`
* `layout_patterns.yaml`
* `visual_grammar.yaml`
* `rhetorical_grammar.yaml`
* `style_contract_variant.yaml`
* `design_spec_addendum.md`
* `style_audit_report.md`

这些文件供后续 `academic-defense-ppt`、`ppt-master` 或其他 PPT 生成 skill 调用。

---

## 1. 适用场景

当用户提出以下需求时，触发本 skill：

* “帮我学习这批 PPT 的风格”
* “蒸馏这些学术会议 PPT 的排版”
* “总结科研大佬 PPT 的叙事方式”
* “从这些 PPT 中提取可复用模板”
* “生成 layout_patterns / style_contract / visual_grammar”
* “分析这份 PPT 为什么专业”
* “把这些会议报告风格融入我的 PPT 工作流”
* “检查我生成的 PPT 是否符合某个蒸馏风格”

---

## 2. 非目标与边界

本 skill 不做以下事情：

1. 不直接生成最终 PPTX。
2. 不模仿某一位具体报告人的个人风格。
3. 不复用源 PPT 中的 logo、照片、实验图、插画、机构 VI、版权素材。
4. 不逐页复制源 PPT 的具体版式。
5. 不把“高级感、简洁、大气、专业”这类模糊评价当作最终输出。
6. 不把所有 PPT 混合成一个笼统的“大佬风格”。
7. 不用大模型直接自由总结 1GB 级别 PPT 语料。

本 skill 只抽象以下内容：

* 页面类型与叙事功能
* 图文比例
* 标题与正文表达风格
* 图表与注释组织方式
* 字体层级
* 色彩使用规则
* 页面密度
* 版式模式
* section / transition / backup 的使用方式
* 可接入生成工作流的 style contract

---

## 3. 核心原则

### 3.1 先结构化，再抽象

不要让大模型直接“看 PPT 并总结风格”。

必须先把 PPT 拆解为结构化记录：

```text
PPTX / PDF
  ↓
结构解析脚本
  ↓
raw_slide_records.yaml
  ↓
逐页分类与功能识别
  ↓
slide_records.yaml
  ↓
风格归纳与模式聚类
  ↓
style_profile / layout_patterns / visual_grammar / rhetorical_grammar
  ↓
style_contract_variant / design_spec_addendum
```

大模型的任务不是凭感觉评价，而是在固定 schema 下完成：

1. 给每页打标签；
2. 从标签中归纳模式；
3. 把模式转化为可执行规则。

### 3.2 区分形式层与内容层

蒸馏内容分为两大主层：

| 层级  | 目标                           | 输出                                                                           |
| --- | ---------------------------- | ---------------------------------------------------------------------------- |
| 形式层 | 格式、排版、图文比例、字体、配色、留白、注释方式     | `visual_grammar.yaml`, `layout_patterns.yaml`, `style_contract_variant.yaml` |
| 内容层 | 叙事结构、标题风格、正文压缩方式、图表解释方式、过渡语言 | `deck_narrative_profile.yaml`, `rhetorical_grammar.yaml`                     |

这两层必须分开输出，禁止混写。

### 3.3 抽象规律，不复制页面

允许学习：

* “结果页通常主图占 60–75%”
* “标题多采用结论式 claim-based title”
* “右侧 interpretation box 用于解释核心趋势”
* “backup 页承载公式推导和额外实验”

禁止输出：

* “复制第 12 页的布局”
* “照搬某教授的封面风格”
* “复用源 PPT 中的机构 logo 和装饰元素”
* “把某页图像作为模板背景”

### 3.4 所有结论必须有证据

任何风格判断都必须来自 `slide_records.yaml` 中的统计或示例页面。

禁止输出无证据判断：

```yaml
bad:
  style: "高级、简洁、大气"
```

应输出可执行判断：

```yaml
good:
  density:
    level: "medium-high"
    evidence:
      average_text_blocks_per_slide: 3.1
      average_main_visual_area_ratio: 0.58
      average_body_font_size: 15
  title_style:
    dominant_type: "claim-based"
    evidence:
      claim_based_title_ratio: 0.64
```

---

## 4. 输入源类型

### 4.1 首选输入

* `.pptx` 文件夹
* 单个 `.pptx`
* 从 PPT 导出的 `.pdf`

### 4.2 可接受输入

* 页面截图文件夹
* 已经解析好的 Markdown / JSON
* 其他 AI 输出的 PPT 分析文件

### 4.3 不推荐输入

* 单纯自然语言描述
* 未分类的大量混合截图
* 没有页面顺序的图片集合

---

## 5. 运行模式

本 skill 有四种固定运行模式。

---

### Mode 1: `single_deck_profile`

用于分析单个 PPT。

#### 输入

```yaml
mode: "single_deck_profile"
input:
  pptx_path: "reference_ppts/example_talk.pptx"
  corpus_label: "optional_label"
```

#### 输出

```text
outputs/example_talk/
  raw_slide_records.yaml
  slide_records.yaml
  deck_profile.yaml
  visual_grammar.yaml
  rhetorical_grammar.yaml
  layout_patterns.yaml
  extraction_report.md
```

#### 适用场景

* 分析某一份高质量会议报告
* 研究某种具体报告结构
* 作为后续语料库蒸馏的单体样本

---

### Mode 2: `corpus_distillation`

用于分析一批 PPT，生成可复用风格库。

#### 输入

```yaml
mode: "corpus_distillation"
input:
  pptx_folder: "reference_ppts/research_conference/"
  corpus_label: "research_conference_talks"
  target_style_ids:
    - "conference_clean"
    - "experimental_result_focused"
    - "theory_dense"
```

#### 输出

```text
style_bank/
  conference_clean/
    style_profile.yaml
    deck_narrative_profile.yaml
    layout_patterns.yaml
    visual_grammar.yaml
    rhetorical_grammar.yaml
    style_contract_variant.yaml
    design_spec_addendum.md
    template_requirements.yaml
    distillation_report.md

  experimental_result_focused/
    ...

  theory_dense/
    ...
```

#### 适用场景

* 从 10–100 份科研 PPT 中抽象风格知识
* 建立个人科研 PPT 风格库
* 为后续自动生成 PPT 提供稳定 style source

---

### Mode 3: `style_contract_generation`

用于把已有蒸馏结果转换成主 PPT 生成工作流可调用的样式协议。

#### 输入

```yaml
mode: "style_contract_generation"
input:
  style_profile: "style_bank/conference_clean/style_profile.yaml"
  layout_patterns: "style_bank/conference_clean/layout_patterns.yaml"
  visual_grammar: "style_bank/conference_clean/visual_grammar.yaml"
  rhetorical_grammar: "style_bank/conference_clean/rhetorical_grammar.yaml"
  target_use: "academic_defense"
```

#### 输出

```text
style_bank/conference_clean/
  style_contract_variant.yaml
  design_spec_addendum.md
  template_requirements.yaml
```

#### 适用场景

* 把风格库接入 `academic-defense-ppt`
* 为 `ppt-master` 创建模板约束
* 将抽象风格转化为可执行设计规则

---

### Mode 4: `generated_ppt_audit`

用于检查已生成 PPT 是否符合某个蒸馏风格。

#### 输入

```yaml
mode: "generated_ppt_audit"
input:
  generated_pptx: "exports/my_defense.pptx"
  reference_style: "style_bank/conference_clean/"
```

#### 输出

```text
audit/
  style_audit_report.md
  slide_level_revision_plan.yaml
  style_score.yaml
```

#### 适用场景

* 检查自动生成 PPT 是否符合目标风格
* 作为 `academic-defense-ppt` Validator 的风格一致性补充
* 生成逐页修改建议

---

## 6. 推荐语料组织方式

不要把所有 PPT 混成一个风格。建议按报告类型、领域和信息密度拆分。

### 6.1 推荐风格簇

| style_id                      | 适用场景                   | 特征                |
| ----------------------------- | ---------------------- | ----------------- |
| `conference_clean`            | 大部分学术会议报告、邀请报告、seminar | 白底、大图、文字少、故事线强    |
| `experimental_result_focused` | 实验结果型报告、论文进展汇报         | 图表密集、对比清楚、结果标题明确  |
| `theory_dense`                | 理论机制报告、公式推导较多报告        | 信息密度高、公式和示意图多     |
| `defense_formal`              | 学位答辩、开题、中期、考核          | 结构规整、章节清楚、贡献链稳定   |
| `keynote_storytelling`        | 大会报告、概览性报告             | 场景化开头、叙事强、视觉冲击更明显 |

### 6.2 最小可行语料

第一次不要处理全部 1GB。建议最小版本：

```yaml
pilot_corpus:
  decks: 10
  representative_slides_per_deck: 10-20
  manually_check_slide_types: true
  output_styles:
    - conference_clean
    - experimental_result_focused
```

完成最小版本并验证有效后，再扩大到完整语料库。

---

## 7. 文件夹结构建议

```text
96_Skills/
  ppt-style-distiller/
    SKILL.md
    README.md
    prompts/
      classify_slide_type.md
      extract_layout_patterns.md
      extract_visual_grammar.md
      extract_rhetorical_grammar.md
      build_deck_narrative_profile.md
      build_style_contract_variant.md
      audit_generated_ppt.md
    schemas/
      slide_record.schema.yaml
      layout_pattern.schema.yaml
      visual_grammar.schema.yaml
      rhetorical_grammar.schema.yaml
      deck_narrative_profile.schema.yaml
      style_contract_variant.schema.yaml
      style_audit.schema.yaml

97_Tools/
  ppt_style_profiler/
    extract_pptx_structure.py
    render_slides.py
    extract_slide_images.py
    cluster_layouts.py
    build_style_bank.py
    audit_generated_ppt.py

90_Templates/
  ppt_styles/
    conference_clean/
      style_profile.yaml
      deck_narrative_profile.yaml
      layout_patterns.yaml
      visual_grammar.yaml
      rhetorical_grammar.yaml
      style_contract_variant.yaml
      design_spec_addendum.md
      template_requirements.yaml
    experimental_result_focused/
      ...
    theory_dense/
      ...
```

---

## 8. 标准输出文件定义

---

### 8.1 `raw_slide_records.yaml`

由程序解析 PPT 后生成。只记录事实，不做解释。

```yaml
source_deck:
  deck_id: "talk_001"
  filename: "example_talk.pptx"
  slide_count: 42
  page_size:
    width: 13.333
    height: 7.5
    unit: "inch"

slides:
  - deck_id: "talk_001"
    page: 1
    text:
      title_candidates:
        - "Metasurfaces for Computational Imaging"
      all_text_blocks:
        - text: "Metasurfaces for Computational Imaging"
          bbox: [1.2, 0.8, 11.8, 1.5]
          font_size: 34
        - text: "Conference Name, 2024"
          bbox: [1.2, 6.6, 6.0, 7.0]
          font_size: 12
    shapes:
      total_count: 8
      text_box_count: 4
      image_count: 1
      chart_like_count: 0
      equation_like_count: 0
    layout_metrics:
      main_visual_area_ratio: 0.30
      text_area_ratio: 0.22
      whitespace_ratio_estimate: 0.48
    colors:
      dominant_colors:
        - "#FFFFFF"
        - "#1F3A5F"
        - "#333333"
    assets:
      images:
        - asset_id: "talk_001_p1_img1"
          bbox: [8.2, 1.2, 12.0, 5.6]
          area_ratio: 0.24
```

---

### 8.2 `slide_records.yaml`

由大模型基于 `raw_slide_records.yaml` 和页面截图进行分类与解释。

每一页必须有固定记录。

```yaml
slide_records:
  - deck_id: "talk_001"
    page: 12
    slide_type: "result-main"
    title_text: "Metasurface enables compact spectral reconstruction"
    title_type: "claim-based"
    title_function: "states_result"

    content_function:
      primary: "show_core_experimental_result"
      secondary:
        - "explain_metric"
        - "connect_result_to_claim"

    text_blocks:
      count: 3
      total_words: 42
      max_block_words: 18
      bullet_count: 3
      body_style: "compressed_phrases"

    visual_blocks:
      main_visual_type: "experimental_figure"
      image_count: 2
      chart_count: 1
      equation_count: 0
      main_visual_area_ratio: 0.62

    layout:
      dominant_pattern: "large_figure_with_right_interpretation"
      title_position: "top_full_width"
      main_visual_position: "left_center"
      text_position: "right"
      footer_present: true

    style:
      background: "white"
      density_level: "medium-high"
      primary_colors:
        - "#1F3A5F"
        - "#333333"
      accent_colors:
        - "#C0392B"
      font_size_estimate:
        title: 34
        body: 16
        caption: 10

    rhetorical_features:
      result_explanation_pattern:
        - "what_is_shown"
        - "key_trend"
        - "why_it_supports_claim"
      evidence_relation: "figure_supports_title_claim"

    reusable:
      score: 8
      reason: "Clear result-first structure with high figure dominance and concise interpretation."

    evidence:
      screenshot: "slides_png/talk_001_page_012.png"
      raw_record_ref: "raw_slide_records.yaml#talk_001_p12"
```

---

### 8.3 `style_profile.yaml`

描述一个风格簇的全局特征。

```yaml
style_id: "conference_clean"
style_name: "Conference Clean Academic Style"
source_scope:
  corpus_label: "research_conference_talks"
  deck_count: 10
  slide_count: 168
  included_slide_types:
    - motivation
    - field_context
    - method_overview
    - result-main
    - result_comparison
    - conclusion

best_for:
  - invited_talk
  - academic_conference
  - seminar
  - thesis_defense_with_storytelling

not_suitable_for:
  - extremely_dense_theory_derivation
  - business_pitch
  - poster_style_presentation

visual_tone:
  background_preference: "mostly_white"
  density: "medium"
  figure_weight: "high"
  text_weight: "low-to-medium"
  accent_usage: "minimal_but_functional"

layout_bias:
  dominant_patterns:
    - "large_figure_with_right_interpretation"
    - "three_block_method_pipeline"
    - "problem_gap_solution_chain"
    - "two_panel_comparison_with_takeaway"

rhetorical_bias:
  title_style: "claim-based"
  body_style: "compressed academic phrases"
  result_slide_logic: "claim → evidence → interpretation"
  motivation_logic: "field context → bottleneck → research gap"

evidence_summary:
  average_main_visual_area_ratio: 0.58
  average_body_words_per_slide: 47
  claim_based_title_ratio: 0.64
  median_bullet_count: 3

avoid:
  - "decorative gradients"
  - "large unrelated icons"
  - "paragraph-heavy slides"
  - "raw paper captions copied directly"
  - "more than two accent colors per slide"
```

---

### 8.4 `deck_narrative_profile.yaml`

描述整份报告的叙事结构。

```yaml
deck_narrative_profile:
  style_id: "conference_clean"
  talk_type: "academic_conference"
  narrative_mode: "problem-driven"

  opening_style:
    preferred_sequence:
      - "field_context"
      - "motivation"
      - "research_gap"
      - "proposed_idea"
    common_opening_patterns:
      - "start from a broad application scenario"
      - "show one bottleneck before presenting method"
      - "use a simple conceptual figure before technical details"

  common_sequence:
    - cover
    - field_context
    - motivation
    - research_gap
    - method_overview
    - method_detail
    - result-main
    - result_comparison
    - mechanism_explanation
    - discussion
    - conclusion
    - acknowledgement
    - backup

  sectioning:
    uses_section_dividers: true
    average_slides_per_section: 5
    divider_style: "minimal_title_plus_progress_marker"

  evidence_flow:
    preferred_chain:
      - "problem"
      - "gap"
      - "method"
      - "main_result"
      - "comparison"
      - "mechanism"
      - "summary"

  backup_strategy:
    enabled: true
    common_backup_content:
      - "extra equations"
      - "additional experimental results"
      - "fabrication details"
      - "parameter sweeps"
      - "supplementary comparisons"
```

---

### 8.5 `layout_patterns.yaml`

记录可复用单页排版模式。

```yaml
patterns:
  - pattern_id: "problem_gap_solution_chain"
    slide_type: "motivation"
    purpose: "Move audience from broad field problem to the need for the proposed approach."

    structure:
      title_area: "top full-width claim or question"
      left_region: "field context figure or application scenario"
      right_region: "3 pain points or bottlenecks"
      bottom_region: "one-line transition to proposed method"

    visual_ratio:
      figure_area: "0.40-0.55"
      text_area: "0.25-0.35"
      whitespace: "0.15-0.25"

    text_budget:
      title_words: "8-14"
      max_bullets: 3
      max_words_per_bullet: 12

    best_for:
      - "research motivation"
      - "field bottleneck"
      - "introduction to new method"

    avoid:
      - "long literature review"
      - "more than four disconnected pain points"
      - "technical equations before problem is established"

  - pattern_id: "three_block_method_pipeline"
    slide_type: "method_overview"
    purpose: "Explain the method as a sequence of three conceptual modules."

    structure:
      title_area: "top full-width"
      center_region: "three horizontally connected modules"
      bottom_region: "input-output relation or physical intuition"
      optional_side_note: "one concise explanation box"

    visual_ratio:
      diagram_area: "0.55-0.70"
      text_area: "0.15-0.25"
      whitespace: "0.15-0.25"

    text_budget:
      module_label_words: "2-5"
      max_explanatory_lines: 3

    best_for:
      - "optical system pipeline"
      - "neural network architecture"
      - "reconstruction workflow"
      - "experimental procedure"

    avoid:
      - "too many internal details"
      - "small unreadable labels"
      - "mixing algorithm and experiment without hierarchy"

  - pattern_id: "large_figure_with_right_interpretation"
    slide_type: "result-main"
    purpose: "Show one central result and interpret why it supports the claim."

    structure:
      title_area: "top full-width claim"
      main_visual: "left or center 60-75%"
      interpretation_box: "right 20-30%"
      condition_or_caption: "bottom-left small text"

    visual_ratio:
      figure_area: "0.60-0.75"
      text_area: "0.15-0.25"
      whitespace: "0.10-0.20"

    text_budget:
      max_bullets: 3
      max_words_per_bullet: 12
      caption_words: "8-20"

    required_annotations:
      - "metric"
      - "experimental condition"
      - "key trend marker"

    best_for:
      - "spectral reconstruction"
      - "imaging result"
      - "quantitative performance figure"

    avoid:
      - "multiple unrelated plots"
      - "paper-style long captions"
      - "title that only says Results"

  - pattern_id: "two_panel_comparison_with_takeaway"
    slide_type: "result_comparison"
    purpose: "Compare proposed method with baseline or alternative condition."

    structure:
      title_area: "top full-width claim"
      left_panel: "baseline / previous method"
      right_panel: "proposed / improved method"
      bottom_takeaway: "one sentence conclusion or metric delta"

    visual_ratio:
      figure_area: "0.55-0.70"
      text_area: "0.15-0.25"
      whitespace: "0.10-0.20"

    text_budget:
      max_bullets: 2
      takeaway_words: "8-16"

    required_annotations:
      - "comparison condition"
      - "same metric scale"
      - "key improvement marker"

    avoid:
      - "unfair visual scaling"
      - "too many baselines on one slide"
      - "missing experimental condition"
```

---

### 8.6 `visual_grammar.yaml`

记录视觉层规则。

```yaml
visual_grammar:
  style_id: "conference_clean"

  canvas:
    aspect_ratio: "16:9"
    background_preference: "white"
    dark_background_usage: "rare; only for section divider or high-level concept"

  typography:
    title_size_range: [30, 38]
    body_size_range: [14, 18]
    caption_size_range: [9, 12]
    title_weight: "semi-bold"
    body_weight: "regular"
    preferred_alignment: "left"
    avoid:
      - "center-aligned paragraphs"
      - "body text below 12 px"
      - "too many font families"

  color_usage:
    primary_palette_type: "low-saturation academic"
    max_accent_colors_per_slide: 2
    highlight_usage: "only for key result, contrast, or current section"
    avoid:
      - "decorative gradient backgrounds"
      - "rainbow palettes without data meaning"
      - "low contrast gray text"

  layout_density:
    default: "medium"
    result_slides: "medium-high"
    theory_slides: "high but structured"
    section_slides: "low"

  figure_rules:
    result_slide_main_figure_area: "0.60-0.75"
    method_slide_diagram_area: "0.55-0.70"
    minimum_chart_label_size: 9
    captions:
      position: "below or near figure"
      style: "short condition or reading instruction"

  annotation_style:
    arrows: "minimal and functional"
    callout_boxes: "used for interpretation or key takeaway"
    numbered_labels: "common for multi-step methods"
    avoid:
      - "decorative arrows"
      - "callouts that repeat the title"
      - "more than three annotation styles on one slide"

  footer_rules:
    page_number: "optional but consistent"
    section_marker: "recommended for long decks"
    institution_logo: "small, not dominant"
```

---

### 8.7 `rhetorical_grammar.yaml`

记录文字与内容表达规则。

```yaml
rhetorical_grammar:
  style_id: "conference_clean"

  title_style:
    dominant_type: "claim-based"
    alternatives:
      motivation: "question-based or bottleneck statement"
      section_divider: "descriptive"
      backup: "descriptive"
    preferred_patterns:
      - "[Method/phenomenon] enables [capability]"
      - "[Key variable] determines [observed trend]"
      - "[Proposed approach] improves [metric] under [condition]"
    avoid:
      - "single noun titles"
      - "paper section titles copied directly"
      - "generic titles such as Results or Method"

  body_style:
    bullet_count_range: [2, 4]
    preferred_sentence_form: "compressed academic phrases"
    max_words_per_bullet: 12
    avoid:
      - "long paragraphs"
      - "abstract-like prose"
      - "copying paper captions as bullet points"

  motivation_style:
    preferred_sequence:
      - "field context"
      - "technical bottleneck"
      - "unmet need"
      - "transition to proposed idea"
    avoid:
      - "starting with implementation details"
      - "literature list without synthesis"

  method_explanation:
    preferred_sequence:
      - "input"
      - "core mechanism"
      - "output"
      - "why it works"
    equation_policy:
      main_slides: "only essential equations"
      backup_slides: "detailed derivations allowed"

  result_explanation:
    preferred_pattern:
      - "what is shown"
      - "what trend matters"
      - "why it supports the claim"
    required_context:
      - "metric"
      - "condition"
      - "baseline or reference when applicable"
    avoid:
      - "showing data without interpretation"
      - "using title as a neutral figure label"

  transition_style:
    common_patterns:
      - "This raises the question..."
      - "To address this limitation..."
      - "We next examine..."
      - "This motivates the following design..."
    purpose: "make the logic between slides explicit"

  conclusion_style:
    preferred_structure:
      - "3-5 claims"
      - "each claim maps to one earlier result"
      - "future direction only after core contributions"
    avoid:
      - "new results"
      - "new terminology"
      - "overly broad claims unsupported by slides"
```

---

### 8.8 `style_contract_variant.yaml`

用于接入 PPT 生成 workflow。

```yaml
style_contract_variant:
  id: "conference_clean"
  derived_from:
    style_profile: "style_profile.yaml"
    visual_grammar: "visual_grammar.yaml"
    rhetorical_grammar: "rhetorical_grammar.yaml"
    layout_patterns: "layout_patterns.yaml"

  theme_colors:
    primary: "#1F3A5F"
    accent: "#3B82F6"
    highlight: "#C0392B"
    bg: "#FFFFFF"
    text_primary: "#202020"
    text_secondary: "#666666"

  font_family:
    title: "'Calibri', 'Arial', 'Microsoft YaHei', sans-serif"
    body: "'Calibri', 'Arial', 'Microsoft YaHei', sans-serif"
    caption: "'Calibri', 'Arial', 'Microsoft YaHei', sans-serif"

  font_size_hierarchy:
    slide_title: 34
    section_header: 24
    body: 15
    caption: 10
    footer: 9

  margins:
    left: 48
    right: 48
    top: 28
    bottom: 32

  density:
    default: "medium"
    result_main: "medium-high"
    method_detail: "high"
    section_divider: "low"

  figure_priority:
    result_main: "high"
    method_overview: "high"
    background: "medium"
    conclusion: "low"

  title_policy:
    default: "claim-based"
    motivation: "question-or-bottleneck"
    section_divider: "descriptive"
    backup: "descriptive"

  text_budget:
    max_body_bullets: 4
    max_words_per_bullet: 12
    max_body_words_per_slide: 60
    result_slide_max_bullets: 3

  layout_pattern_preferences:
    motivation:
      - "problem_gap_solution_chain"
    method_overview:
      - "three_block_method_pipeline"
    result-main:
      - "large_figure_with_right_interpretation"
    result_comparison:
      - "two_panel_comparison_with_takeaway"

  forbidden_elements:
    - "decorative clip-art"
    - "word clouds"
    - "3D chart effects"
    - "long paper-style captions"
    - "more than two accent colors per slide"
    - "paragraph-heavy result slides"
```

---

### 8.9 `design_spec_addendum.md`

供 `ppt-master` 或主 PPT 生成器读取的自然语言设计补充。

```markdown
# Design Spec Addendum: conference_clean

## Style intent

This style is optimized for academic conference talks and research seminars.
It emphasizes clear evidence-first slides, concise claim-based titles, and large central scientific figures.

## Layout behavior

- Result slides should be figure-first.
- Method slides should use structured diagrams rather than paragraph explanations.
- Motivation slides should establish field context before technical detail.
- Conclusion slides should map directly to earlier evidence slides.

## Text behavior

- Prefer claim-based titles.
- Avoid generic slide titles such as "Results" or "Method".
- Use 2–4 concise bullets per slide.
- Do not copy paper paragraphs or figure captions directly.

## Visual behavior

- Use mostly white backgrounds.
- Reserve 60–75% of result slides for the main visual.
- Use accent color only for key trend, metric, or active section marker.
- Keep annotations functional and minimal.
```

---

### 8.10 `template_requirements.yaml`

规定该风格至少需要哪些模板页型。

```yaml
template_requirements:
  style_id: "conference_clean"
  required_templates:
    - cover
    - section_divider
    - field_context
    - motivation
    - method_overview
    - method_detail
    - result_main
    - result_comparison
    - conclusion
    - acknowledgement
    - backup

  minimum_layout_variants:
    result_main: 2
    method_overview: 2
    comparison: 2
    motivation: 1

  required_placeholders:
    cover:
      - title
      - speaker
      - affiliation
      - date
      - optional_logo
    result_main:
      - claim_title
      - main_figure
      - interpretation_box
      - caption_or_condition
    method_overview:
      - pipeline_diagram
      - input_label
      - output_label
      - physical_intuition
```

---

## 9. Slide Type Taxonomy

本 skill 使用固定 slide type 分类。分类必须写入每页 `slide_record`。

```yaml
slide_types:
  - cover
  - speaker_intro
  - outline
  - field_context
  - motivation
  - research_gap
  - concept_explanation
  - background
  - literature_synthesis
  - method_overview
  - method_detail
  - experimental_setup
  - result-main
  - result_comparison
  - result_ablation
  - mechanism_explanation
  - summary_transition
  - discussion
  - limitation
  - outlook
  - conclusion
  - acknowledgement
  - backup
  - unknown
```

### 9.1 分类标准

| slide_type              | 判定标准                       |
| ----------------------- | -------------------------- |
| `cover`                 | 标题、作者、单位、会议/日期信息为主         |
| `speaker_intro`         | 报告人或团队介绍                   |
| `outline`               | 展示报告结构或章节目录                |
| `field_context`         | 从宏观领域、应用场景或研究背景切入          |
| `motivation`            | 说明为什么这个问题重要                |
| `research_gap`          | 指出现有方法或领域中的缺口              |
| `concept_explanation`   | 解释一个核心概念、物理图像或技术思想         |
| `background`            | 提供必要背景知识                   |
| `literature_synthesis`  | 总结已有工作，不是简单列文献             |
| `method_overview`       | 方法总览，流程图或系统图为主             |
| `method_detail`         | 方法细节、公式、参数、模块解释            |
| `experimental_setup`    | 实验装置、样品、测量系统、参数表           |
| `result-main`           | 一个核心结果，图表为主                |
| `result_comparison`     | 对比 baseline、SOTA、不同条件或不同方法 |
| `result_ablation`       | 消融实验、参数扫描、因素分析             |
| `mechanism_explanation` | 解释结果背后的机制                  |
| `summary_transition`    | 阶段性总结并转入下一部分               |
| `discussion`            | 讨论意义、边界、解释和对比              |
| `limitation`            | 局限性和不足                     |
| `outlook`               | 未来工作、应用前景                  |
| `conclusion`            | 总结主要贡献和结论                  |
| `acknowledgement`       | 致谢、联系方式、Q&A                |
| `backup`                | 补充实验、推导、额外数据、答疑材料          |
| `unknown`               | 无法可靠分类                     |

---

## 10. 工作流详解

---

## Module 1: PPT 解析器

### 10.1 目标

把 PPTX/PDF 转换成结构化中间数据和页面截图。

### 10.2 PPTX 解析优先级

优先使用程序解析 PPTX，而不是直接让大模型阅读全部文件。

应提取：

* 页面尺寸
* 每页文本
* 文本框坐标
* 字体大小
* 字体名称
* 字体颜色
* shape 数量
* 图片数量
* 图片坐标
* 图表数量
* 公式候选
* 页脚与页码
* section 标识
* 主视觉元素面积比例
* 页面截图

### 10.3 建议工具

可使用：

* `python-pptx`：解析 PPTX 结构
* LibreOffice headless：导出页面为 PDF 或 PNG
* PyMuPDF：解析 PDF 页面和渲染截图
* OpenCV / PIL：估计图片区域、颜色分布、留白比例

### 10.4 输出

```text
extracted/
  slides_png/
    deck001_page001.png
    deck001_page002.png
  raw_slide_records.yaml
  extracted_text.json
  extracted_shapes.json
  extracted_assets.json
  extraction_report.md
```

### 10.5 解析失败处理

若 PPTX 解析失败：

1. 尝试用 LibreOffice 转换为 PDF。
2. 用 PyMuPDF 渲染每页截图。
3. 从 PDF 中提取文本块和图片块。
4. 如果仍失败，只保留页面截图，进入弱解析模式。

弱解析模式必须在 `extraction_report.md` 中声明：

```yaml
extraction_quality:
  mode: "weak_visual_only"
  limitations:
    - "shape coordinates unavailable"
    - "font size estimated from screenshot"
    - "text extraction incomplete"
```

---

## Module 2: 逐页分类器

### 11.1 目标

基于 `raw_slide_records.yaml` 和页面截图，为每页生成标准 `slide_record`。

### 11.2 分类输入

每页输入应包含：

* 页面截图
* 页面文本
* shape 统计
* 主视觉区域估计
* 字体与颜色估计
* 前后页上下文

### 11.3 分类任务

每页必须完成以下判断：

```yaml
required_labels:
  - slide_type
  - title_type
  - title_function
  - content_function
  - main_visual_type
  - dominant_layout_pattern
  - density_level
  - reusable_score
```

### 11.4 `title_type` 枚举

```yaml
title_types:
  - claim-based          # 标题直接表达结论
  - question-based       # 标题提出问题
  - descriptive          # 描述页面主题
  - section-label        # 章节标题
  - metric-based         # 标题突出指标或数值
  - generic              # Results / Method 等泛标题
  - none
```

### 11.5 `main_visual_type` 枚举

```yaml
main_visual_types:
  - experimental_figure
  - simulation_result
  - data_chart
  - optical_setup
  - method_diagram
  - conceptual_schematic
  - equation
  - table
  - photo
  - literature_map
  - timeline
  - none
```

### 11.6 `density_level` 枚举

```yaml
density_levels:
  - low
  - medium
  - medium-high
  - high
```

### 11.7 可复用评分

每页需要给出 `reusable.score`，范围 0–10。

评分标准：

| 分数   | 含义                            |
| ---- | ----------------------------- |
| 0–2  | 不建议复用，可能是过渡页、版权页或过于特殊页面       |
| 3–4  | 可提供参考，但模式不稳定                  |
| 5–6  | 有一定参考价值，可作为局部样式样本             |
| 7–8  | 高价值可复用页面，适合抽象为 layout pattern |
| 9–10 | 极高价值页面，可作为模板设计核心依据            |

低分原因要写明，例如：

* 过于依赖原始图像
* 布局太特殊
* 信息过密不可迁移
* 只有机构宣传意义
* 无清晰学术表达功能

---

## Module 3: 形式蒸馏

### 12.1 目标

从 `slide_records.yaml` 中抽象视觉与排版规律。

### 12.2 输入

```text
slide_records.yaml
slides_png/
```

### 12.3 输出

```text
visual_grammar.yaml
layout_patterns.yaml
style_profile.yaml
```

### 12.4 必须统计的指标

```yaml
metrics_to_compute:
  global:
    - average_main_visual_area_ratio
    - median_text_blocks_per_slide
    - median_body_words_per_slide
    - common_background_colors
    - common_title_positions
    - common_footer_patterns

  by_slide_type:
    - average_main_visual_area_ratio
    - median_bullet_count
    - title_type_distribution
    - density_distribution
    - common_layout_patterns
    - common_main_visual_types
```

### 12.5 版式模式聚类

同类 slide type 下，按以下特征聚类：

* 主视觉区域位置
* 文本区域位置
* 标题位置
* 是否有 interpretation box
* 是否有多 panel 比较
* 是否有流程箭头
* 页面密度
* 图文比例

聚类后输出 `layout_patterns.yaml`。

### 12.6 禁止输出模糊规则

禁止：

```yaml
layout: "clean and beautiful"
```

必须改写为：

```yaml
layout:
  background: "white"
  title_position: "top_full_width"
  main_visual_area_ratio: "0.60-0.75"
  body_bullet_count: "2-3"
  interpretation_box_position: "right"
```

---

## Module 4: 内容蒸馏

### 13.1 目标

总结文字、标题、叙事、图文解释方式。

### 13.2 输入

```text
slide_records.yaml
extracted_text.json
```

### 13.3 输出

```text
rhetorical_grammar.yaml
deck_narrative_profile.yaml
```

### 13.4 必须分析的内容

```yaml
content_features:
  title:
    - title_type_distribution
    - claim_based_title_examples
    - generic_title_ratio
    - title_word_count_range

  body:
    - bullet_count_distribution
    - average_words_per_bullet
    - phrase_vs_sentence_ratio
    - paragraph_like_slide_ratio

  result_explanation:
    - whether_title_states_result
    - whether_metric_is_explicit
    - whether_condition_is_explicit
    - whether_interpretation_is_present

  narrative:
    - opening_sequence
    - method_to_result_transition
    - result_to_discussion_transition
    - use_of_summary_transition
    - backup_strategy
```

### 13.5 标题风格规则

将标题归入以下类别：

```yaml
title_style_categories:
  claim-based:
    description: "标题表达本页结论或发现"
    example: "Metasurface enables compact spectral reconstruction"
  question-based:
    description: "标题提出研究问题或挑战"
    example: "Can we resolve spectrum and polarization simultaneously?"
  descriptive:
    description: "标题描述页面主题"
    example: "Experimental setup"
  metric-based:
    description: "标题突出定量指标或提升"
    example: "3.2× improvement in reconstruction accuracy"
  generic:
    description: "泛标题，信息量低"
    example: "Results"
```

### 13.6 图表解释规则

结果页必须检查：

```yaml
result_slide_checks:
  - title_contains_claim
  - metric_visible
  - experimental_condition_visible
  - baseline_or_reference_visible
  - key_trend_annotated
  - interpretation_present
```

---

## Module 5: 风格压缩与规范化

### 14.1 目标

把蒸馏出的观察结果压缩成可执行风格规则。

### 14.2 输入

```text
style_profile.yaml
layout_patterns.yaml
visual_grammar.yaml
rhetorical_grammar.yaml
deck_narrative_profile.yaml
```

### 14.3 输出

```text
style_contract_variant.yaml
design_spec_addendum.md
template_requirements.yaml
```

### 14.4 压缩规则

任何观察性描述必须转换为以下形式之一：

1. 数值范围
2. 枚举选项
3. slide type 规则
4. 布局约束
5. 文本预算
6. 禁用项
7. 优先级规则

示例：

观察性描述：

```text
这类 PPT 结果页通常比较重视图，右边会写少量解释。
```

压缩为：

```yaml
result-main:
  layout_preference:
    - "large_figure_with_right_interpretation"
  main_figure_area_ratio: "0.60-0.75"
  interpretation_box_position: "right"
  max_bullets: 3
  max_words_per_bullet: 12
```

---

## Module 6: 风格 QA

### 15.1 目标

检查蒸馏结果是否可执行、可复用、可接入主工作流。

### 15.2 QA 输出

```yaml
qa:
  has_style_profile: true
  has_deck_narrative_profile: true
  has_layout_patterns: true
  has_visual_grammar: true
  has_rhetorical_grammar: true
  has_style_contract_variant: true
  has_design_spec_addendum: true
  no_raw_asset_reuse: true
  no_specific_author_imitation: true
  no_vague_rules: true
  compatible_with_academic_defense_ppt: true
  evidence_linked_to_slide_records: true
```

### 15.3 模糊规则检查

如果出现以下词汇，必须要求重写为可执行规则：

```yaml
vague_terms:
  - "高级"
  - "大气"
  - "美观"
  - "专业"
  - "简洁"
  - "清晰"
  - "有设计感"
  - "现代"
  - "优雅"
```

这些词可以出现在解释中，但不能作为最终规则。

例如：

```yaml
bad:
  style: "简洁专业"
```

应改为：

```yaml
good:
  background: "white"
  max_accent_colors_per_slide: 2
  max_body_bullets: 4
  minimum_margin_px: 40
  result_slide_main_visual_ratio: "0.60-0.75"
```

---

## 16. 与 `academic-defense-ppt` 的集成方式

本 skill 是上游风格知识层，推荐集成路径：

```text
ppt-style-distiller
  ↓
style_bank / layout_patterns / style_contract_variant
  ↓
academic-defense-ppt
  ↓
style_contract.yaml / design_spec.md
  ↓
ppt-master SVG generation
  ↓
PPTX
```

### 16.1 在 `deck_config.yaml` 中增加字段

```yaml
style_source:
  mode: "distilled_style"
  style_id: "conference_clean"
  reference_strength: "medium"   # low / medium / high
  allow_layout_reuse: true
  allow_color_reuse: false
  allow_asset_reuse: false
  style_bank_path: "90_Templates/ppt_styles/conference_clean"
```

字段解释：

| 字段                   | 含义                    |
| -------------------- | --------------------- |
| `mode`               | 是否使用蒸馏风格              |
| `style_id`           | 调用哪个风格簇               |
| `reference_strength` | 风格约束强度                |
| `allow_layout_reuse` | 是否允许复用抽象布局模式          |
| `allow_color_reuse`  | 是否允许复用色彩方案            |
| `allow_asset_reuse`  | 是否允许复用源素材；默认必须为 false |
| `style_bank_path`    | 风格文件路径                |

### 16.2 在样式冻结前增加风格检索

主 PPT 生成 workflow 可增加：

```text
Module 2.2a: Style Retrieval
输入: presentation_type + audience + slide_plan
检索: style_bank
输出: 推荐 style_contract_variant + layout_patterns
然后进入 BLOCKING B 样式冻结
```

### 16.3 样式冻结时展示

```markdown
## 样式冻结确认：蒸馏风格方案

推荐风格: conference_clean

选择理由:
- 目标场景为学术会议/博士答辩
- slide_plan 中 result-main 和 method-overview 占比较高
- 该风格强调大图、结论式标题和右侧解释框

将应用的规则:
1. 结果页主图面积 60–75%
2. 标题默认使用 claim-based title
3. 正文每页不超过 4 条 bullet
4. 方法页优先使用三段式流程图
5. 禁止复制源 PPT 的图片、logo 和专属装饰

请确认或修改风格方案。
```

---

## 17. Generated PPT Audit

当用户要求检查生成 PPT 是否符合蒸馏风格时，使用 `generated_ppt_audit` 模式。

### 17.1 输入

```yaml
mode: "generated_ppt_audit"
input:
  generated_pptx: "exports/my_talk.pptx"
  reference_style: "90_Templates/ppt_styles/conference_clean"
```

### 17.2 输出 `style_score.yaml`

```yaml
style_score:
  overall: 7.8
  dimensions:
    layout_consistency: 8.0
    figure_dominance: 8.5
    text_compression: 7.0
    academic_formality: 8.0
    narrative_flow: 7.5
    visual_noise_control: 8.0
    slide_type_fit: 7.0
    source_traceability: 9.0

  major_issues:
    - "Several result slides use descriptive rather than claim-based titles."
    - "Two method slides contain too many small labels."
    - "Slide 8 has insufficient figure dominance for result-main type."
```

### 17.3 输出 `slide_level_revision_plan.yaml`

```yaml
revision_plan:
  - page: 8
    issue_type: "layout_mismatch"
    current_slide_type: "result-main"
    expected_pattern: "large_figure_with_right_interpretation"
    problems:
      - "main figure area ratio is about 0.42, below expected 0.60-0.75"
      - "body has 6 bullets, exceeding recommended maximum of 3"
    actions:
      - "increase main figure size"
      - "move secondary bullets to speaker notes or backup"
      - "rewrite title as a result claim"

  - page: 12
    issue_type: "rhetorical_mismatch"
    current_title: "Experimental Results"
    suggested_title: "Reconstruction remains stable under broadband illumination"
    actions:
      - "replace generic title with claim-based title"
      - "add condition label near figure"
```

---

## 18. Prompt Templates

以下 prompt 文件建议放入：

```text
96_Skills/ppt-style-distiller/prompts/
```

---

### 18.1 `classify_slide_type.md`

````markdown
# Task: Classify Slide Type and Function

You are analyzing one slide from an academic presentation.
Use the provided screenshot, extracted text, and structural metadata.

Do not judge whether the slide is beautiful.
Classify the slide according to the fixed schema.

## Inputs

- screenshot: {{screenshot_path}}
- extracted_text: {{extracted_text}}
- shape_metrics: {{shape_metrics}}
- previous_slide_summary: {{previous_slide_summary}}
- next_slide_summary: {{next_slide_summary}}

## Required output

Return YAML only.

```yaml
page: {{page_number}}
slide_type: "one of the allowed slide types"
title_text: "..."
title_type: "claim-based | question-based | descriptive | section-label | metric-based | generic | none"
title_function: "..."
content_function:
  primary: "..."
  secondary: []
main_visual_type: "..."
dominant_layout_pattern: "..."
density_level: "low | medium | medium-high | high"
reusable:
  score: 0
  reason: "..."
evidence:
  screenshot: "..."
  raw_record_ref: "..."
````

## Rules

* Use `unknown` only when classification is genuinely unreliable.
* Do not infer scientific claims that are not present on the slide.
* Distinguish result slides from method slides by function, not by whether they contain figures.
* A slide with data but no interpretation may still be `result-main`, but mark weak rhetorical quality.

````

---

### 18.2 `extract_layout_patterns.md`

```markdown
# Task: Extract Reusable Layout Patterns

You are given many slide_records from academic PPTs.
Extract reusable slide-level layout patterns.

Do not describe individual slides.
Do not copy source slide layouts exactly.
Abstract recurring patterns by slide_type.

## Inputs

- slide_records: {{slide_records}}
- target_style_id: {{style_id}}

## Required output

Return YAML only.

```yaml
patterns:
  - pattern_id: "short_snake_case_id"
    slide_type: "..."
    purpose: "..."
    structure:
      title_area: "..."
      main_visual: "..."
      text_region: "..."
      optional_regions: []
    visual_ratio:
      figure_area: "range"
      text_area: "range"
      whitespace: "range"
    text_budget:
      max_bullets: 3
      max_words_per_bullet: 12
    best_for: []
    avoid: []
    evidence:
      support_slide_count: 0
      example_pages: []
````

## Rules

* Each pattern must be supported by multiple slides unless explicitly marked as rare.
* Convert vague descriptions into measurable constraints.
* Prefer patterns that can be reused in new PPT generation.

````

---

### 18.3 `extract_visual_grammar.md`

```markdown
# Task: Extract Visual Grammar

Analyze the visual design rules of an academic PPT corpus.
Use slide_records and computed metrics.

## Required output

Return YAML only.

```yaml
visual_grammar:
  style_id: "{{style_id}}"
  canvas:
    aspect_ratio: "..."
    background_preference: "..."
  typography:
    title_size_range: []
    body_size_range: []
    caption_size_range: []
    title_weight: "..."
    preferred_alignment: "..."
    avoid: []
  color_usage:
    primary_palette_type: "..."
    max_accent_colors_per_slide: 0
    highlight_usage: "..."
    avoid: []
  layout_density:
    default: "..."
    by_slide_type: {}
  figure_rules:
    result_slide_main_figure_area: "..."
    method_slide_diagram_area: "..."
    minimum_chart_label_size: 0
  annotation_style:
    arrows: "..."
    callout_boxes: "..."
    numbered_labels: "..."
    avoid: []
  evidence:
    metrics_used: []
    example_pages: []
````

## Rules

* Do not use vague terms as final rules.
* Every qualitative judgment must be accompanied by concrete visual constraints.

````

---

### 18.4 `extract_rhetorical_grammar.md`

```markdown
# Task: Extract Rhetorical Grammar

Analyze title style, body text style, result explanation, transitions, and conclusion style.

## Required output

Return YAML only.

```yaml
rhetorical_grammar:
  style_id: "{{style_id}}"
  title_style:
    dominant_type: "..."
    alternatives: {}
    preferred_patterns: []
    avoid: []
  body_style:
    bullet_count_range: []
    preferred_sentence_form: "..."
    max_words_per_bullet: 0
    avoid: []
  motivation_style:
    preferred_sequence: []
    avoid: []
  method_explanation:
    preferred_sequence: []
    equation_policy: {}
  result_explanation:
    preferred_pattern: []
    required_context: []
    avoid: []
  transition_style:
    common_patterns: []
    purpose: "..."
  conclusion_style:
    preferred_structure: []
    avoid: []
  evidence:
    title_type_distribution: {}
    example_pages: []
````

## Rules

* Distinguish paper-writing style from presentation-speaking style.
* Identify whether titles make claims, ask questions, or merely label topics.
* Result slides should be evaluated by whether they explain the evidence.

````

---

### 18.5 `build_style_contract_variant.md`

```markdown
# Task: Build Style Contract Variant

Convert distilled style files into a style_contract_variant.yaml that can be used by a PPT generation workflow.

## Inputs

- style_profile.yaml
- layout_patterns.yaml
- visual_grammar.yaml
- rhetorical_grammar.yaml
- deck_narrative_profile.yaml

## Required output

Return YAML only.

```yaml
style_contract_variant:
  id: "{{style_id}}"
  derived_from: {}
  theme_colors: {}
  font_family: {}
  font_size_hierarchy: {}
  margins: {}
  density: {}
  figure_priority: {}
  title_policy: {}
  text_budget: {}
  layout_pattern_preferences: {}
  forbidden_elements: []
````

## Rules

* Use executable constraints only.
* Resolve conflicts between visual_grammar and rhetorical_grammar explicitly.
* Do not include raw source slide images or speaker-specific identity.

````

---

### 18.6 `audit_generated_ppt.md`

```markdown
# Task: Audit Generated PPT Against Distilled Style

Compare a generated PPT with a reference distilled style.

## Inputs

- generated_slide_records.yaml
- reference_style_contract_variant.yaml
- reference_layout_patterns.yaml
- reference_rhetorical_grammar.yaml

## Required output

Return YAML only.

```yaml
style_score:
  overall: 0
  dimensions:
    layout_consistency: 0
    figure_dominance: 0
    text_compression: 0
    academic_formality: 0
    narrative_flow: 0
    visual_noise_control: 0
    slide_type_fit: 0
    source_traceability: 0
  major_issues: []

revision_plan:
  - page: 0
    issue_type: "..."
    current_slide_type: "..."
    expected_pattern: "..."
    problems: []
    actions: []
````

## Rules

* Be critical.
* Assume problems exist and find them.
* Give page-specific revision actions.
* Do not merely say the slide is good or bad.

````

---

## 19. 建议脚本职责

本 skill 可配合 `97_Tools/ppt_style_profiler/` 下的脚本运行。

### 19.1 `extract_pptx_structure.py`

职责：

- 读取 PPTX
- 提取每页 shape、文本、图片、颜色、坐标
- 输出 `raw_slide_records.yaml`

### 19.2 `render_slides.py`

职责：

- 将 PPTX/PDF 渲染为每页 PNG
- 输出到 `slides_png/`

### 19.3 `extract_slide_images.py`

职责：

- 从 PPTX 中提取嵌入图片
- 仅用于结构分析，不用于复用源素材

### 19.4 `cluster_layouts.py`

职责：

- 基于 slide_records 中的布局特征聚类
- 生成候选 layout patterns

### 19.5 `build_style_bank.py`

职责：

- 汇总多个 deck 的输出
- 生成 style_bank 目录

### 19.6 `audit_generated_ppt.py`

职责：

- 解析生成 PPT
- 与 style_contract_variant 对比
- 输出风格评分和逐页修改计划

---

## 20. 推荐执行顺序

### 20.1 单份 PPT 分析

```text
1. render_slides.py example.pptx
2. extract_pptx_structure.py example.pptx
3. LLM: classify_slide_type.md → slide_records.yaml
4. LLM: extract_visual_grammar.md
5. LLM: extract_rhetorical_grammar.md
6. LLM: extract_layout_patterns.md
7. QA: 检查输出是否可执行
````

### 20.2 批量语料蒸馏

```text
1. 对每个 PPT 运行 Module 1–2
2. 合并所有 slide_records.yaml
3. 按 style_id 或聚类结果拆分语料
4. 对每个 style_id 运行 Module 3–5
5. 输出 style_bank
6. 运行 Module 6 QA
```

### 20.3 接入 PPT 生成工作流

```text
1. 用户选择或系统推荐 style_id
2. 读取 style_contract_variant.yaml
3. 读取 layout_patterns.yaml
4. 在样式冻结前展示风格选择
5. 用户确认后生成最终 style_contract.yaml
6. 后续由 academic-defense-ppt / ppt-master 生成 PPT
```

---

## 21. 质量标准

### 21.1 一份合格的蒸馏结果必须满足

```yaml
quality_requirements:
  structure:
    - "has separate visual and rhetorical files"
    - "has slide-type-specific layout patterns"
    - "has executable style contract"
    - "has evidence from slide_records"

  usability:
    - "can be used by PPT generation workflow"
    - "can be audited against generated PPT"
    - "does not require source PPT to be present during generation"

  safety_and_integrity:
    - "does not copy raw assets"
    - "does not imitate a specific speaker"
    - "does not include copyrighted slide images as reusable templates"
```

### 21.2 不合格输出示例

```markdown
这批 PPT 风格总体非常简洁大气，学术感强，排版清楚，适合科研汇报。建议后续 PPT 也采用类似风格，突出重点，减少文字，增加图片。
```

问题：

* 没有 slide type 规则；
* 没有数值约束；
* 没有 layout pattern；
* 没有 style contract；
* 无法被自动化 workflow 调用。

### 21.3 合格输出示例

```yaml
result-main:
  title_policy: "claim-based"
  main_visual_area_ratio: "0.60-0.75"
  text_budget:
    max_bullets: 3
    max_words_per_bullet: 12
  required_context:
    - metric
    - condition
    - baseline_or_reference
  preferred_layouts:
    - large_figure_with_right_interpretation
    - two_panel_comparison_with_takeaway
  forbidden:
    - generic_title
    - long_caption_as_body_text
    - more_than_two_unrelated_figures
```

---

## 22. 人工校验节点

虽然本 skill 尽量自动化，但建议设置两个人工校验点。

### 22.1 Checkpoint A: 语料分类确认

在批量蒸馏前，展示语料分组：

```markdown
## Checkpoint A: 语料分类确认

检测到以下风格簇：

1. conference_clean: 8 decks, 126 slides
2. experimental_result_focused: 5 decks, 91 slides
3. theory_dense: 4 decks, 77 slides

请确认是否按以上分组蒸馏，或手动调整某些 PPT 的归属。
```

### 22.2 Checkpoint B: 风格合同确认

在生成 `style_contract_variant.yaml` 后，展示摘要：

```markdown
## Checkpoint B: 风格合同确认

风格 ID: conference_clean

核心规则：
1. 结果页主图面积 60–75%
2. 标题默认为 claim-based
3. 正文最多 4 条 bullet
4. 方法页优先使用三段式流程图
5. 禁止复用源 PPT 图片、logo 和专属装饰

请确认是否加入 style_bank。
```

---

## 23. 与版权和伦理相关的规则

1. 源 PPT 只作为风格分析语料，不作为可复用素材库。
2. 不提取、保存或复用源 PPT 中的专属图片、logo、未公开数据、照片和版权图形。
3. 不输出“模仿某某教授风格”的指令。
4. 不生成会让新 PPT 与某一份源 PPT 高度相似的模板。
5. 输出必须是抽象规则，而不是可追溯到单一源页面的复制版式。
6. 如源 PPT 包含未公开研究内容，蒸馏结果不得暴露具体研究数据、结论或图像。

---

## 24. 最小可行版本计划

### Phase 1: Pilot

```yaml
phase: 1
input:
  decks: 10
  slides_per_deck: 10-20
manual_work:
  - check slide type classification
  - remove private or unusable decks
output:
  - conference_clean
  - experimental_result_focused
success_criteria:
  - produces valid style_contract_variant.yaml
  - can improve one generated PPT compared with default style
```

### Phase 2: Corpus Expansion

```yaml
phase: 2
input:
  decks: 30-50
output:
  - conference_clean
  - experimental_result_focused
  - theory_dense
  - defense_formal
success_criteria:
  - stable layout_patterns across corpora
  - generated PPT audit score improves
```

### Phase 3: Workflow Integration

```yaml
phase: 3
integration:
  - add style_source to deck_config.yaml
  - add Style Retrieval before style freezing
  - add style audit to Validator
success_criteria:
  - style selection becomes part of PPT generation workflow
  - audit produces page-level revision plan
```

---

## 25. 快速参考卡片

```text
# PPT Style Distiller 快速流程

# 1. 单份 PPT 解析
render_slides.py <deck.pptx>
extract_pptx_structure.py <deck.pptx>
# 输出 raw_slide_records.yaml + slides_png/

# 2. 逐页分类
LLM prompt: classify_slide_type.md
# 输出 slide_records.yaml

# 3. 形式蒸馏
LLM prompt: extract_visual_grammar.md
LLM prompt: extract_layout_patterns.md
# 输出 visual_grammar.yaml + layout_patterns.yaml + style_profile.yaml

# 4. 内容蒸馏
LLM prompt: extract_rhetorical_grammar.md
LLM prompt: build_deck_narrative_profile.md
# 输出 rhetorical_grammar.yaml + deck_narrative_profile.yaml

# 5. 风格合同生成
LLM prompt: build_style_contract_variant.md
# 输出 style_contract_variant.yaml + design_spec_addendum.md + template_requirements.yaml

# 6. 接入主 PPT workflow
style_source.mode = distilled_style
style_source.style_id = conference_clean

# 7. 生成后风格审计
LLM prompt: audit_generated_ppt.md
# 输出 style_score.yaml + slide_level_revision_plan.yaml
```

---

# End of Skill
