---
name: tone
version: 1.1.0
description: |
  PhD 学术语气 / 作者指纹 提取与对齐工作流 orchestrator。统一调度 4 skills（corpus-ingest / move-detector / register-translator / ai-residue-detector）+ 4 agents（fingerprint-miner / tribunal / voice-synthesizer / tone-auditor），实现「语料 → 指纹挖掘 → 风格语义库 → 写作时调用 → 草稿审计 → 迭代」闭环。

  **核心心智**：作者「有什么就先做什么」 — 缺 B / 缺 C / 缺 D 不 abort，只在 A 路（外部参考论文）为空时才 abort。系统第一优先级产出是**可被 AI 调用的风格语义参考库**，不是完整的 voice spec。

  触发方式：
  - /tone setup [--mode collaboration|terminal]   — Phase 1 冷启动（建库，partial-input 容忍）
  - /tone library [function|section|fingerprint]  — Phase L 写作时调用风格语义库（最高频）
  - /tone audit <draft-file-or-paragraph> [--mode] — Phase 2 写完每段跑 7 维度评分（缺料维度自动 N/A）
  - /tone iterate                                  — Phase 3 spec 升版（v0.X → v0.X+1）
  - /tone status                                   — 看当前 spec 版本 / 语料状态 / 待迭代信号
  - /tone explain <symbol>                         — 反查任意符号是什么意思（如 `/tone explain CORE-7` / `/tone explain RL-4`）
  - 用户说「跑语气审计 / 看 voice 偏离 / 这段够不够像我 / 这段太完美了导师没空间 / 我的指纹丢了吗 / 给我找参考 / introduction 同位置怎么写」

  **人话翻译层（v1.2.0）**：底层符号不动 — orchestrator 跑时按 `lexicon.md` 自动在 user-facing 状态附人话注。作者不用学符号体系。词典在 `~/.claude/skills/tone/lexicon.md`。指纹动态名从 fingerprint 文件 `human_name:` 字段读。

  适用：英文 PhD chapter / proposal / lit review / supervisor 邮件 / 一作论文 — 凡是要在「作者指纹 × 导师 PhD 期原型」之间对齐的英文学术写作。
  不适用：中文写作（→ load-fingerprint / lnc / bullet）；非作者建模领域。

allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
  - Skill
  - Agent
---

# /tone — 语气与指纹对齐工作流 orchestrator

## 设计原则

1. **职责分离** — orchestrator 不重写 4 skills + 4 agents 任何逻辑，只在合适节点串联
2. **有什么用什么（RL-0）** — 作者素材随时间累积，缺 B / 缺 C / 缺 D 不 abort。只在 A 路（外部参考论文）为空时才 abort（连风格库都建不出来）。spec 每维度带 confidence 标记（HIGH / LOW / N-A），audit 时 N-A 维度跳过不假装能评
3. **风格语义库优先** — 系统第一可交付产物是 `outputs/` 下的 moves + lexical-fingerprint + supervisor-prototype（哪有跑哪），通过 `/tone library` 让 LLM 写作时主动调用。voice-spec 合成是第二层叠加，缺料时降级跑
4. **四阶段闭环** — Phase 1 setup（建库 + partial spec）→ Phase L library（写作时调用，最高频）→ Phase 2 audit（写完段评分）→ Phase 3 iterate（升版），系统终极目标是作者最终不再需要它（学我者生,像我者死）
5. **mode 透传** — 每次调用必带 `mode`：`collaboration`（默认，v0.5 三原则渲染〔证据纪律 / 经济精确 / 分离〕+ supervisor 留白机制〔§9.4 豁免 + §10 zones〕）或 `terminal`（质量上限 + 留白移除）。RL-2。〔2026-06-10:旧「60:40 目标函数」已随 voice-spec-v0.5 废除,resonance 从优化目标降级为约束〕
6. **PRINT-CHECK 门禁** — 每个 Stage 结束 print 一份 `PRINT-CHECK-<STAGE>` 凭证，作者看到 ✅ 才进下一阶段（对齐 /phd-write 模式）
7. **红线零妥协** — RL-1（不动论证）/ RL-3（不平均化）/ RL-4（战略不完美 ≠ 烂稿）通过每个 Stage 前置检查显式喊出
8. **轻量优先** — Phase L library + Phase 2 audit 是最高频入口；Phase 1/3 是低频重型
9. **人话翻译层（v1.2.0 新）** — 底层符号体系（PRINT-CHECK / RL / GATE / CORE-N / W-M1 / HIGH-TRUST / etc.）不动。每次产出 user-facing 状态时按 `lexicon.md` 规则附人话注：
   - 每个符号**第一次出现**时后跟 `(= <人话>)` 或 ` ↳ <人话>`
   - **Stage 开头**必带一句人话："我现在要 X，需要你给 Y，做完后系统会有 Z"
   - **GATE 处**必带完整人话："可以进 / 卡住了 + 三件事最重要 + 你能做什么"
   - **最终报告**不允许只堆表格 — 必有 "你现在多了 X / 能用 Y / 下一步 Z" 三句
   - 指纹用 `human_name` 字段，括号附 id：「战略不完美 (CORE-1) / 保留」
   - 用户可调 `/tone explain <symbol>` 反查任何符号

---

## 5 红线（每 Stage 强制喊出）

- **RL-0** 有什么用什么 — 缺 B/C/D 不 abort，spec 维度带 confidence；只在 A 路（外部参考论文）为空时才 abort
- **RL-1** auditor / detector 永远不碰实质论证，只动语气
- **RL-2** 每次调用声明 mode（默认 collaboration）
- **RL-3** 不做平均化 — 每个 move / 指纹实例必带完整上下文
- **RL-4** 战略不完美 = 共振载体 / 协作空间 / 作者个体性，**绝不**等于 unprofessionalism / AI 味 / 事实错误

---

## 数据布局（`{TONE_ROOT}` 默认 = `<repo-root>/ (本仓库根目录)`）

```
{TONE_ROOT}/
├── _config.json              ← 路径配置 + 当前 spec 版本号
├── intuition-list.md         ← 作者凭直觉列的语言习惯（人工提供，corpus-ingest 前必备）
├── corpus/
│   ├── A_external-theses/    ← Type A 源文件 + ingest 后 paragraph 单元 JSON
│   ├── B_pure-private/       ← Type B（作者私密 meta-thinking）
│   ├── C_cross-register/     ← Type C（邮件 / 硕士论文 / X / 中文）
│   └── D_supervisor-pre/     ← Type D（导师 PhD 期 thesis + 早期一作论文）
├── outputs/
│   ├── moves.md              ← move-detector 输出（Type A 实例库）
│   ├── author-fingerprint.md ← fingerprint-miner 输出：三档（core / register-marker / self-perception-bias）
│   ├── supervisor-prototype.md ← fingerprint-miner 输出：含 characteristic flaws 显式标注
│   ├── register-table.md     ← register-translator 输出：source × function × academic-eq 转换表
│   ├── tribunal/<date>.md    ← 每次 tribunal 6 persona 审查记录
│   └── voice-spec-v{X.Y}.md  ← voice-synthesizer 输出（spec 主文档，每次 iterate 升版）
├── audit-log.md              ← Phase 2 每次 audit 的 accept/reject 流水（Phase 3 燃料）
└── SCRIPTING-LOG.md          ← 哪一步后来被 Python 化（参考 SCRIPTING-POLICY.md）
```

---

# Phase 1 · setup（冷启动，一次性）

## Stage S-1：语料可用性检查（soft 降级，只 A 路空时 abort）

**RL-0 心智**：作者素材按节奏累积，缺啥标啥，唯一 hard requirement 是 A 路（外部参考论文）— 没 A 路连风格库都建不出来。

| 语料 | 检查路径 | 缺失行为 | 后续维度受影响 |
|---|---|---|---|
| **A 外部参考论文**（必需） | `{TONE_ROOT}/corpus/A_external-theses/*.{md,pdf,txt}` ≥ 3 文件 | **ABORT** + 提示作者先收集 3 篇导师带过或同领域参考论文 | — |
| B 作者纯私密 | `{TONE_ROOT}/corpus/B_pure-private/*.md` ≥ 1 文件 ≥ 1000 字 | 标记 `B=MISSING`，继续 | 作者 core fingerprint 维度 confidence=LOW；audit 时该维度 N/A |
| C 作者跨 register | `{TONE_ROOT}/corpus/C_cross-register/` | 标记 `C=MISSING`，继续 | register-translator 维度 N/A，跨 register 稳定性判断不可用 |
| D 导师 PhD 期 | `{TONE_ROOT}/corpus/D_supervisor-pre/*.{md,pdf,txt}` ≥ 2 文件 | 标记 `D=MISSING`，继续 | supervisor-prototype 维度 N/A；mode=collaboration 的 supervisor-resonance 约束降级为「纯 A 路语义参考库」 |
| intuition-list | `{TONE_ROOT}/intuition-list.md` ≥ 5 条 | 标记 `INTUITION=MISSING`，继续 | fingerprint-miner 跳过 self-perception-bias 对比维度 |

冷启动语料规模目标（README §Phase 1，但**不要等齐**）：A 5-8（优先导师带过的学生论文）/ B 越多越好 / C 每 register 3-5 / D 导师早期 thesis + 早期一作论文。**先把 A 路跑通建库 → 后续 B/C/D 来一波就 /tone iterate 升一次。**

### PRINT-CHECK-PREREQ

```
═══════════════════════════════════════════════════════════
PRINT-CHECK-PREREQ (Stage S-1) — 语料可用性 + 降级标记
═══════════════════════════════════════════════════════════
mode: collaboration (default)
{TONE_ROOT}: <abs path>

[A 路硬门禁]
✅/❌ A 外部参考论文：N 篇（≥3 才能进 S0；< 3 → ABORT）

[B/C/D 软标记 — 缺啥标啥，不 abort]
B 作者纯私密：           N 文件 / XXXX 字  → 状态：READY / MISSING
C 作者跨 register：      email N / X-中文 N / 硕士 N  → 状态：READY / MISSING
D 导师 PhD 期：          N 篇  → 状态：READY / MISSING
intuition-list.md：     N 条  → 状态：READY / MISSING

[本次 run 的 confidence 矩阵预告]
core author fingerprint：  HIGH/LOW/N-A （依赖 B、C）
register-translate 规则：  HIGH/LOW/N-A （依赖 C）
supervisor resonance 约束： HIGH/LOW/N-A （依赖 D，缺 D 时降级为纯 A 路库）
self-perception-bias 对比：HIGH/LOW/N-A （依赖 intuition-list）
moves 实例库（A 路）：       HIGH （A 路只要 ≥3 就高）
lexical-fingerprint 矩阵：  HIGH （A 路只要 ≥3 就高）

[红线声明]
RL-0 有什么用什么 / RL-1 不动论证 / RL-2 mode=collaboration / RL-3 不平均化 / RL-4 战略不完美 ≠ 烂稿

GATE: ✅ A 路 ≥3 → 可进 S0  /  ❌ A < 3 → ABORT，先补 A 路
═══════════════════════════════════════════════════════════
```

## Stage S0：corpus-ingest（按 S-1 状态跑可用 type）

`Skill("corpus-ingest")` 只处理 S-1 标记为 READY 的 type。MISSING 的 type 跳过，**不报错**。

**首次警告**：A/B/C 可自动跑；**D 如果 READY**，完成后必须人工 review（fingerprint-miner 会暴露这些 flaws 作为共振载体，必须确认 ingest 没把 flaws 当噪声清掉 — README §First-run caution）。D MISSING 时跳过本警告。

### PRINT-CHECK-INGEST

```
PRINT-CHECK-INGEST (Stage S0)
段级单元总数：N（A=… B=… C=… D=…）
section_function 分布：topic-establishment N / evidence N / synthesis N / scoping N / transition N / meta N
RL-3 实例化检查：每段保留原文 + 元数据 ✅
Type D flaw 保留人工 review：⬜ 待作者抽查 / ✅ 已通过
GATE: ✅ PASS → 可进 S1
```

## Stage S1：可用线并行抽取（按 S-1 状态决定跑哪些）

**线 1（A 路，必跑）**：`Skill("move-detector")` on Type A → `outputs/moves.md` + `outputs/lexical-fingerprint-matrix.md`（每篇 A 出一份 `*_paragraphs.md` + `*_moves.md`）

**线 2（B+C 作者指纹）**：B/C 都 MISSING 时**整线跳过**，spec 里作者 core fingerprint 维度标 N/A；至少一个 READY → `Agent(subagent_type="fingerprint-miner")` 跑可用部分，prompt 显式告知缺哪个

**线 3（D 导师原型）**：D MISSING 时**整线跳过**，spec 里 supervisor-prototype 维度标 N/A；D READY → `Agent(subagent_type="fingerprint-miner")` → `outputs/supervisor-prototype.md`

跑得动的线并行调度（同一消息内多 tool calls）。**跳过的线必须在 PRINT-CHECK-EXTRACT 里显式标 SKIPPED 原因**，不能默默不跑。

### PRINT-CHECK-EXTRACT

```
PRINT-CHECK-EXTRACT (Stage S1)
[线 1 move-detector + lexical] — RAN
detected moves：N 实例 / 10 类 taxonomy 分布：…
lexical-fingerprint-matrix：N 篇 × M 词频维度
flag-for-human：N 处（unsure，需作者确认）

[线 2 fingerprint-miner author] — RAN / SKIPPED (B+C all MISSING)
若 RAN：
  core fingerprints：N 条（跨 register stable，但 C MISSING 时降级为单 register 稳定）
  register-markers：N 条
  self-perception-bias：N 条 / SKIPPED (intuition-list MISSING)
  对照 intuition-list：被语料修正的 N 处

[线 3 fingerprint-miner supervisor] — RAN / SKIPPED (D MISSING)
若 RAN：
  prototype features：N 条
  characteristic flaws：N 条（必须保留，不准 "优化掉"）
  ⚠️ Type D flaws 首跑必须人工 review：⬜ / ✅

GATE: ✅ PASS（含 RAN 的线全过，含 D RAN 时的 flaw review）→ 可进 S2
```

## Stage S2：tribunal 6 persona 审查（按 S1 可用输出降级）

`Agent(subagent_type="tribunal", prompt=...)` 对 S1 跑出来的输出做 6 persona 审查：Wittgenstein（清晰度）/ Socrates（个人 vs 领域）/ Popper（可证伪）/ Damschroder（可操作化）/ Voice Critic（藏判断）/ Supervisor's Ghost（共振 / 可改空间 / 独立性）。

降级规则：
- author fingerprint SKIPPED → Socrates / Voice Critic 跳过作者维度，只审 moves 库
- supervisor prototype SKIPPED → Supervisor's Ghost 整 persona 跳过，spec 标 "no supervisor anchor"
- mode=collaboration 时 Ghost 的 editable-space 检查 active；mode=terminal 时关掉

persona 跳过必须在 PRINT-CHECK-TRIBUNAL 显式标 SKIPPED 原因。

### PRINT-CHECK-TRIBUNAL

```
PRINT-CHECK-TRIBUNAL (Stage S2) — mode=<mode>
Wittgenstein：    MUST=N SHOULD=N
Socrates：        MUST=N SHOULD=N / SKIPPED (author fingerprint MISSING)
Popper：          MUST=N SHOULD=N
Damschroder：     MUST=N SHOULD=N
Voice Critic：    MUST=N SHOULD=N / SKIPPED (author fingerprint MISSING)
Supervisor Ghost：resonance=PASS/FAIL · editable-space=<active 时 PASS/FAIL / terminal 时 N/A> · independence=PASS/FAIL
                  或 SKIPPED (supervisor prototype MISSING)

修订要求清单：（MUST 必须先吃完才能进 S3，SKIPPED 维度的 MUST=0 不算违规）
1. ...

GATE: ✅ PASS（active persona MUST=0）→ 可进 S3
```

## Stage S3：voice-synthesizer + register-translator（partial-input + confidence 标记）

`Agent(subagent_type="voice-synthesizer", prompt=...)` 按 mode + S1/S2 可用输出跑合成（2026-06-10 起按 voice-spec-v0.5 模型,数字配比已废）：

| 可用语料组合 | mode=collaboration | mode=terminal |
|---|---|---|
| A+B+C+D 齐 | **voice = 作者裁决层**（v0.5 三原则 + 九信号 + native-human register）；**supervisor 层 = 约束**（不与导师风格硬冲突 + §9.4 豁免 + §10 zones 留白） | 质量上限 + 留白移除（supervisor 贡献仍须可见） |
| A+B+C，缺 D | 同上,supervisor-resonance 约束标 N/A | 同左 |
| A+D，缺 B+C | A 路通用学术 move + supervisor 约束 + 留白；作者 core 维度标 N/A，spec 提示「作者指纹未建模」 | A 路通用学术 move + supervisor 贡献可见 |
| 只有 A | **不合成 voice-spec**，只产出「风格语义参考库 v{X.Y}」（moves + lexical matrix），spec 全维度 N/A，作者通过 `/tone library` 调用 | 同左 |

对每条 author core fingerprint（若有）给出 3 选 1 命运：**preserve** / **register-translate** / **drop**（功能记录下来由学术替代承载）。

register-translate 部分：C READY 才调 `Skill("register-translator")` 产出 `outputs/register-table.md`；C MISSING 时该表标 `N/A — no cross-register samples`。

合成产物写入 `outputs/voice-spec-v{NEXT}.md`（每维度首行标 `confidence: HIGH/LOW/N-A` + 原因），并更新 `_config.json` 当前版本号 + `corpus_state` 字段（记录本次跑的语料状态）。

### PRINT-CHECK-SYNTH

```
PRINT-CHECK-SYNTH (Stage S3) — mode=<mode>
corpus_state: A=N / B=READY|MISSING / C=READY|MISSING / D=READY|MISSING / intuition=READY|MISSING
合成档位：<齐 / 缺D / 缺BC / 只A>
voice-spec-v{X.Y}.md 已生成（abs path） — 或者「风格语义库 v{X.Y}（无 spec）」

[voice 构成（v0.5：作者裁决层=声音，resonance=软约束，无数字配比；旧 60:40 已废除 2026-06-10）]
作者 ruling 层：证据纪律 / 经济精确 / 分离 + 九信号 已落实 ✅
supervisor resonance：✅ 不与导师风格硬冲突 / ⚠️ 硬冲突处列出   或 N/A (缺 D)
战略不完美保留：N 处（每处说明 "右的不完美"：共振载体 / 协作空间 / 作者个体性）
                  或 N/A (缺 D)

[author core 指纹命运分配] — 或 N/A (B+C MISSING)
preserve：N 条
register-translate：N 条（已生成 register-table.md，N 行规则；或 N/A 缺 C）
drop（功能由学术替代承载）：N 条

[spec 维度 confidence 矩阵]
authorial-presence    : HIGH/LOW/N-A — 原因
hedging               : HIGH/LOW/N-A — 原因
citation-integration  : HIGH/LOW/N-A — 原因
argumentative-density : HIGH/LOW/N-A — 原因
sentence-rhythm       : HIGH/LOW/N-A — 原因
lexical-register      : HIGH/LOW/N-A — 原因
meta-discourse        : HIGH/LOW/N-A — 原因
supervisor-resonance  : HIGH/LOW/N-A — 原因

[supreme maxim 检查]
□ spec 描述 "为什么这样写" 而非 "写什么"（学我者生,像我者死）
□ N-A 维度明确告知作者「补哪类语料能升 confidence」

GATE: ✅ PASS → 可进 S4
```

## Stage S4：spec 落盘 + index 更新

- 写 `outputs/voice-spec-v{X.Y}.md`（synthesizer 已写，此 Stage 只 verify）
- 更新 `_config.json`：`current_spec: voice-spec-v{X.Y}.md`，`spec_history: [v0.1, ...]`
- 在 `audit-log.md` 顶部 append 「spec 升至 v{X.Y}，{date}」分隔线

### PRINT-CHECK-COMMIT

```
PRINT-CHECK-COMMIT (Stage S4)
current_spec：voice-spec-v{X.Y}.md
_config.json updated ✅
audit-log.md 分隔线 inserted ✅

下一步：日常写作每段写完用 `/tone audit <段>` 跑审计
═══════════════════════════════════════════════════════════
```

---

# Phase L · library（写作时调用风格语义参考库，最高频）

**入口语义**：作者写作时主动调用 — "我现在要写 X 段，从已建库里给我同类参考"。**不是审稿**，是 pre-hoc 辅助。

## 使用方式

```
/tone library <function>           # 按 section_function 查（topic-establishment / evidence / synthesis / scoping / transition / meta）
/tone library section <name>       # 按 section 查（introduction / methods / discussion / conclusion / lit-review）
/tone library fingerprint <name>   # 按指纹名查（如果 spec 存在）
/tone library move <type>          # 按 move taxonomy 查（10 类之一）
/tone library lexical <word>       # 在 lexical fingerprint matrix 里查某词在 A 路出现模式
```

## Stage L-1：库可用性

读 `_config.json`，盘点 `outputs/` 里实际存在的资产：
- `*_moves.md`（A 路每篇）
- `*_paragraphs.md`（A 路每篇）
- `lexical-fingerprint-matrix.md`
- `supervisor-prototype.md`（D READY 时）
- `supervisor-imprint-conclusions-v*.md`（已有的导师 imprint 提取）
- `author-fingerprint.md`（B/C 至少一个 READY 时）
- `voice-spec-v{X.Y}.md`（S3 跑出来才有）
- **`constitutional-fingerprint.md`** — 人工硬规则（MUST / MUST NOT / 阈值 / §15 六项 AI leak / 导师真实批注衍生），**真文件住在本 outputs/，作者自己更新**（2026-06-12 起；此前曾 symlink 借引 phd-write，已归位）；每次 library 调用必带，规则书与样本并立

库为空 → 提示先跑 `/tone setup`（A 路 ≥3 即可建库，不要等 B/C/D）。

## Stage L0：检索 + 喂给上游 LLM

按子命令参数 grep / 读取相关 outputs 文件，**返回给调用方 LLM 的内容是「规则书 + 实例本」双份**，不是分析：

```
═══════════════════════════════════════════════════════════
[CONSTITUTIONAL RULES — 人工硬规则，每次必带，最高优先级]
═══════════════════════════════════════════════════════════
↪ 完整读出 outputs/constitutional-fingerprint.md：
  §2 MUST（强制规则）
  §3 MUST NOT（禁止）
  §4 SHOULD（推荐）
  §5 阈值表（句长 SD / 形容词密度 / 抛问不答等）
  §6 自审清单
  §7 few-shot 风格转换示例
  §15 六项 AI leak（抛问不答 / 三段并列 / 元叙述 / 抽象修辞代事实 / 比较级无锚点 / case-for-X）

任何后续 reference block 的「学」都不得违反 constitutional rules。
冲突时 constitutional > derived > sample。

═══════════════════════════════════════════════════════════
[REFERENCE BLOCK — function=<X>, source=A 路]
═══════════════════════════════════════════════════════════
来自 <thesis name>, paragraph #<N>, section=<…>, section_function=<X>:
"<原段落>"
move 标签：<move_type> · 长度：<n words> · 句长 SD：<…>

来自 <thesis name>, paragraph #<M>, …
"<原段落>"
...

[LEXICAL FINGERPRINT — function=<X> 在 A 路出现的高频词/句法]
- 高频名词短语：…
- 高频动词：…
- 句长分布：mean=… SD=…
- 高频 hedge 词：…

[SUPERVISOR IMPRINT — 若 D READY 且 section_function 相关]
来自 supervisor-prototype.md §<…>：
"<原句>"
characteristic flaw note：<…>

[AUTHOR FINGERPRINT — 若 author-fingerprint READY 且相关]
…

═══════════════════════════════════════════════════════════
[INSTRUCTION TO CALLER]
═══════════════════════════════════════════════════════════
你（上游 LLM）写这段时：
1. **CONSTITUTIONAL RULES 是底线** — 违反任何一条都不能输出
2. **REFERENCE BLOCK 是范例** — 参考 move 结构 + 句法节奏 + 词汇范围
3. **不要直接复制原句**，要把你自己的 idea 套到同样的 move 形状里
4. RL-1：不动你正在写的论证骨架，只让语义/语气向参考靠拢
```

## Stage L1：调用方接管

L0 输出后，**orchestrator 不再干预** — 让调用方（/phd-write 或作者直接调）拿着 reference block 去写。写完想审 → 跑 `/tone audit`。

### PRINT-CHECK-LIBRARY

```
PRINT-CHECK-LIBRARY (Phase L)
query: <子命令 + 参数>
matched: N 个 reference paragraphs / M 行 lexical / K 条 imprint
output: 已喂给上游 LLM（不落盘，每次调用 fresh）
GATE: ✅ 直接进作者写作 / 上游 LLM 继续生成
═══════════════════════════════════════════════════════════
```

---

# Phase 2 · audit（日常每段调用，最高频）

## Stage A-1：spec / 库可用性 + mode + confidence 矩阵读取

读 `_config.json`：
- 当前 spec 存在 → 走完整 audit 流程，读 spec 的 confidence 矩阵决定哪些维度跑、哪些 N/A
- 只有「风格语义库」无 spec → 跳过 A1 tone-auditor 的指纹比对部分，只跑 A0 ai-residue 快筛 + 库参考对比
- 啥都没有 → 提示先跑 `/tone setup`

接受 `--mode collaboration|terminal`（默认 collaboration）。接受输入：草稿文件路径，**或**直接粘贴的段落文本。

### PRINT-CHECK-AUDIT-INIT

```
PRINT-CHECK-AUDIT-INIT (Stage A-1)
current_spec：voice-spec-v{X.Y}.md ✅ / 仅风格库 v{X.Y} ⚠️ / 空 ❌
corpus_state（从 _config.json）：A=N / B=… / C=… / D=…
本次 audit 将跑维度：<列出 confidence ≠ N-A 的维度>
本次 audit 将 N/A 维度：<列出 + 原因 + 缺啥能解锁>
mode：collaboration / terminal
input：<file path or "inline paragraph">
GATE: ✅ → 可进 A0
```

## Stage A0：ai-residue-detector 快筛

`Skill("ai-residue-detector")` 对草稿快扫：句法过均匀 / AI buzzword 密度 / 判断密度 / 作者在场度 / 过完美度，给 AI-flavor score + 触发位置 + 每位置「此处本应出现什么作者指纹」。

**并行跑 constitutional §15 六项 AI leak 逐项扫**（导师实证清单，离散句型红线，不在 ai-residue 5 信号内）：①抛问不答（`?` 后无 evidence-answer）②三段并列（The first/second/third 机械三联）③元叙述（描述自己结构，如 organised as a funnel）④抽象修辞代事实（the geography of the burden is shifting 类比喻替数字）⑤比较级无锚点（higher/high 没说比谁高）⑥case-for-X 套话。逐句定位，任一命中 = 红线 FAIL。

**同一道也扫 constitutional §3.6 抽象模板红线**（`it is important to note that` / `the results indicate that` / `collectively, these results suggest` / `taken together, these … establish/suggest/show` / `in light of these findings` 等 summative connector + 抽象模板）：命中即红线 FAIL，改法 = 直接陈述综合结论 + 引用，删掉 summative connector。〔2026-06-12 补：此前 A0 只扫 §15，漏了 §3.6，导致 `Taken together, these trials establish` 这类 AI-tell 溜过审计；§3.6 与 §15 同属离散模板红线，一并扫〕

ai-residue 5 信号 + §15 六项 + §3.6 模板全 PASS → 跳到 A1（深审）；任一 FAIL → 列出位置（§15 命中给改法：删元叙述/抽象修辞、比较级补锚点、抛问改陈述、三联拆开；§3.6 命中 → 删 summative connector 直陈），作者要么先改要么标记接受后继续。

### PRINT-CHECK-RESIDUE

```
PRINT-CHECK-RESIDUE (Stage A0)
AI-flavor score：X / 100（越低越好）
信号子分：
  syntactic-uniformity：PASS/FAIL（句长 SD = ?）
  AI-buzzword 密度：PASS/FAIL（命中 buzzwords：…）
  judgment-density：PASS/FAIL（"so what" 句 N/段）
  authorial-presence：PASS/FAIL（判断动词 / 元判断句 N）
  over-completeness：PASS/FAIL（每 claim 都引用 / 双面给齐 → 触发）

[constitutional §15 六项 AI leak 逐项扫]
  ①抛问不答          ：PASS / FAIL <句>
  ②三段并列          ：PASS / FAIL <句>
  ③元叙述结构        ：PASS / FAIL <句>
  ④抽象修辞代事实    ：PASS / FAIL <句>
  ⑤比较级无锚点      ：PASS / FAIL <句>
  ⑥case-for-X 套话   ：PASS / FAIL <句>

[constitutional §3.6 抽象模板红线扫]
  summative connector / 抽象模板（taken together…establish / collectively / it is important to note 等）：PASS / FAIL <句>

触发位置 + 指纹缺口（cross-ref spec）：
位置 1：<原句>
        缺口：spec §X 「<指纹名>」此处本应出现，建议：<建议>
...

GATE: ai-residue 5 信号 + §15 六项全 PASS → 直接 A1  /  有 FAIL → 作者裁决后进 A1
```

## Stage A1：tone-auditor 深审（按 spec confidence 跳 N-A 维度）

`Agent(subagent_type="tone-auditor", prompt=...)`，传入 mode + 草稿 + spec + **本次跑的维度白名单**（confidence ≠ N-A 的维度）。

7 维度 profile：authorial-presence / hedging / citation-integration / argumentative-density / sentence-rhythm / lexical-register / meta-discourse。**N-A 维度直接输出 "N/A — <原因>"，不假装能评。**

对照 spec 找偏离 + 指纹丢失 + "陈述事实而藏判断" 位置（限于 confidence ≥ LOW 的维度）。

mode=collaboration + supervisor-resonance 维度 ≥ LOW 时跑 over-perfection warning（够不够给导师留笔的空间 / 不完美是否是 "右的不完美"）；supervisor-resonance=N/A 时整段 warning 跳过。mode=terminal 时关掉，作者指纹比例阈值提高。

**RL-1 显式喊出**：只动语气，不动论证骨架。auditor 给修订建议时如果发现自己在改论证 → STOP 并 flag。

### PRINT-CHECK-TONE

```
PRINT-CHECK-TONE (Stage A1) — mode=<mode>
[7 维度 tone profile —— N-A 维度直接标 N/A 不评]
authorial-presence    : <evaluation> / spec target   或   N/A — 缺 B+C, 补 1 篇私密 meta 笔记可升 LOW
hedging               : ...                                或   N/A — …
citation-integration  : ...
argumentative-density : ...
sentence-rhythm       : ...
lexical-register      : ...
meta-discourse        : ...

[指纹丢失（应出现但没出现）] — 限 LOW+ 维度
1. spec §X.Y 「<指纹>」于 <位置>：…

[陈述事实而藏判断（Voice Critic 标准）] — 限 author fingerprint READY 时跑
1. <原句> → 是 "the evidence shows" 在躲 "I read the evidence as showing"
   或 SKIPPED — 缺 author fingerprint

[over-perfection warning] (collaboration + supervisor-resonance ≥ LOW)
resonance 约束：✅ 不与导师风格硬冲突 / ⚠️ 硬冲突处列出（无数字配比目标,2026-06-10 起）
editable-space：⬜ 留 / ⬛ 太完美
imperfection 类型审查：右的不完美 N / 烂稿/AI 味 N（后者需作者修）
   或 SKIPPED — 缺 D, 无 supervisor anchor

[修订建议]（按位置给，每条只动语气 RL-1）
1. ...

GATE: ✅ 给出建议 → 等作者 accept/reject 决策
```

## Stage A2：作者裁决 + audit-log 记录

作者对每条建议给 accept / reject / modify。**rejections 是新数据**（spec 在此处与真实作者不符 — Phase 3 燃料）。

append 到 `audit-log.md`：

```
## <YYYY-MM-DD HH:MM> · mode=<mode> · spec=v{X.Y}
input: <file:line-range or "inline">
[A0 ai-residue triggers]
- <signal>: <accepted/rejected/modified> — <note>
[A1 tone-auditor suggestions]
- 建议 1: <accepted/rejected/modified> — <note>
- ...
[Phase 3 信号]
- rejection pattern: <如果 rejection 集中在某指纹 → 提示 spec 该指纹定义需修正>
- new ground truth: <如果作者标某段为 "这就是我想要的"，append 路径到 B>
---
```

### PRINT-CHECK-AUDIT-CLOSE

```
PRINT-CHECK-AUDIT-CLOSE (Stage A2)
accept / reject / modify 分布：A=N R=N M=N
audit-log.md 追加 ✅（line range：…）
Phase 3 信号汇总：N（≥ 阈值 / 暂不需迭代）
═══════════════════════════════════════════════════════════
```

---

# Phase 3 · iterate（spec 升版，低频重型）

## Stage I-1：iteration 触发条件

读 `audit-log.md`，统计自 last spec 以来：
- rejections 总数 ≥ 20 **或**
- 某指纹 rejection 集中（≥ 5 次同一指纹）**或**
- 新加 ≥ 3 篇 Type B ground truth **或**
- 作者收到导师反馈批注新数据 → 手动触发

任一满足 → 建议升版。

### PRINT-CHECK-ITER-TRIGGER

```
PRINT-CHECK-ITER-TRIGGER (Stage I-1)
since last spec (v{X.Y}, <date>):
  rejections 总数：N（阈值 20）
  集中 rejection 指纹：<指纹名 N 次 / 阈值 5>
  新 Type B：N（阈值 3）
  导师反馈数据：⬜ 无 / ✅ 有

→ iterate 推荐：YES / NO（NO 时退出，让作者继续 Phase 2）
GATE: ✅ → 可进 I0
```

## Stage I0..I3：复用 setup S0..S3（增量 mode）

- I0：`Skill("corpus-ingest")` 只处理新增语料（B/C 增量 + 可能新导师材料）
- I1：`Agent(fingerprint-miner)` 拿 audit-log rejection pattern 当 "新假设" 输入，重跑 + 验证
- I2：`Agent(tribunal)` 6 persona 重审，重点扫 rejection-pattern 指纹的定义是否被修正
- I3：`Agent(voice-synthesizer)` 跑出 `voice-spec-v{X.Y+1}.md`，并对照旧版做 diff

新 spec 落盘 + `_config.json` 升版 + `audit-log.md` 新分隔线。

### PRINT-CHECK-ITER-COMMIT

```
PRINT-CHECK-ITER-COMMIT (Stage I3)
old → new: voice-spec-v{X.Y}.md → voice-spec-v{X.Y+1}.md

[diff 摘要]
新增指纹：N · 修正指纹：N · 移除指纹：N
register-table 变动：N 行
战略不完美清单变动：N 条

[supreme maxim 自检]
□ spec 是否更靠近 "学我者生,像我者死" — 作者能否凭这版 spec 内化判断、用得更少？

═══════════════════════════════════════════════════════════
```

---

# /tone status

读 `_config.json` + 扫 `audit-log.md` 输出当前状态报告：

```
TONE STATUS
current spec: voice-spec-v{X.Y}.md (<date>)
spec history: v0.1 → v0.2 → ... → v{X.Y} （N 次迭代）

corpus 规模：
  A=N · B=N · C=N · D=N

since last spec：
  audits 跑了 N 次
  accept/reject/modify：A=N R=N M=N
  iterate 触发信号：<列出哪些阈值已碰 / 未碰>

next move 建议：
  - 继续 /tone audit（信号未到）
  - 或 /tone iterate（阈值已碰）
```

---

# /phd-write 集成点

- **Stage 1（draft 前）**：写每段前可调 `Skill("tone","library <function>")` 把对应 section_function 的 A 路参考 + supervisor imprint 喂给主 LLM 当 pre-hoc 引导
- **Stage 2（critique）**：调 aw-critic 之后自动追跑 `Skill("tone","audit --mode collaboration")`，把语气审计与 aw-critic 论证批判**并列**给作者裁决
- **Stage 3（humanize）**：跑完 humanizer_academic 后再跑一次 `Skill("tone","audit")` 做指纹保留回归检查（若作者指纹维度 N/A 则跳过该回归）

`/tone` 仍可独立用 — 写邮件 / 会议发言 / 非 thesis 内容时直接调 `/tone library` 或 `/tone audit`，不必经 `/phd-write`。

---

# 子命令独立调用

| 子命令 | 跳到 | prereq | 备注 |
|---|---|---|---|
| `/tone setup` | Phase 1 S-1 → S4 | A 路 ≥ 3 篇 | B/C/D 缺则相应维度 N/A |
| `/tone library <…>` | Phase L L-1 → L1 | outputs/ 非空（即跑过 S1） | 最高频入口，写作时主动调 |
| `/tone audit <input>` | Phase 2 A-1 → A2 | 至少风格库存在 | 缺 spec 时只跑 A0 + 库参考对比 |
| `/tone iterate` | Phase 3 I-1 → I3 | spec 存在 + audit-log 有数据 | |
| `/tone status` | 单次报告 | 至少 _config.json 存在 | 显示 corpus_state + N-A 维度提示 |

---

# Scripting 决策（参考 SCRIPTING-POLICY.md）

跑过一轮真实数据后，按 4 问自评（是否 deterministic / computational / 高频 / 节省 token），强候选：
- `ai-residue-detector` 的句长 SD / buzzword 频率 / citation 比例 → 最强候选，建脚本喂 LLM
- `corpus-ingest` 的段落分割 / metadata 校验 / 中文句法特征抽取
- `fingerprint-miner` 的跨 register 出现/缺席 grep + 频率表
- `tone-auditor` 复用 ai-residue-detector 的 scorer

**绝不脚本化**：section_function 判断 / move 识别 / 指纹假设生成 / tribunal 6 persona 判断 / voice-synthesizer 命运分配 / "此处本应出现什么指纹"。

script 写完 → 记到 `{TONE_ROOT}/SCRIPTING-LOG.md`。

---

# 核心纪律

1. 每个 Stage 必须 print 一份 `PRINT-CHECK-<STAGE>` 凭证
2. mode 每个对外 tool call 都要带（默认 collaboration）
3. **RL-0：有什么用什么** — 缺 B/C/D 不 abort，spec 维度带 confidence，audit 时 N-A 维度不假装能评
4. RL-1：永远不动论证 — 发现自己在动 → STOP + flag
5. RL-3：永远不平均化 — 每个 move / 指纹必带具体上下文
6. RL-4：战略不完美 = 共振 / 协作空间 / 个体性 — 不等于 unprofessionalism / AI 味 / 事实错误
7. Phase 1 首跑 Type D flaws 必须人工抽查（D READY 时；MISSING 时跳过）
8. Phase 2 rejection 是 Phase 3 燃料 — 不要丢
9. **风格语义库优先于 voice-spec** — A 路 ≥ 3 篇就能建库走 Phase L，B/C/D 来一波就升一次 spec
10. 系统终极成功 = 作者用得越来越少（学我者生,像我者死）

---

# 版本历史

| 版本 | 日期 | 变更 |
|---|---|---|
| 1.0.0 | 2026-05-30 | 初版。3 phase 闭环，4 skills + 4 agents 编排，对齐 /phd-write 的 PRINT-CHECK 门禁模式，RL-1..4 红线显式化，与 /phd-write Stage 2/3 集成 |
| 1.1.0 | 2026-05-30 | 按作者预期重构：(1) 加 RL-0「有什么用什么」+ Stage S-1 改 soft 降级（只 A 路空时 abort）；(2) S1/S2/S3 全段加 partial-input 容忍 + spec 维度 confidence 矩阵（HIGH/LOW/N-A）；(3) Phase 2 audit 读 confidence 跳 N-A 维度，不假装能评；(4) 新增 Phase L `/tone library` 子命令 — 写作时主动调用风格语义参考库当 pre-hoc 辅助；(5) /phd-write 集成加 Stage 1 库调用钩子；(6) TONE_ROOT 默认路径修正为 `03-科研/Tone-Workflow/`（对齐 memory 实际位置） |
