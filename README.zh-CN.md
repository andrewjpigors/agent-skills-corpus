# Agent Skills 语料库（Agent Skills Corpus）

**一个可复现、边界明确的公开 *Agent Skills*（`SKILL.md` 文件）数据集。**

*[English → README.md](README.md)*

> **55,698 个唯一 Skill** · **14,784 个仓库** · GitHub + GitLab + Gitee · 快照日 **2026-07-18**（UTC）
> 每个 Skill 均按内容去重、进行双轴分类，并标注许可证。
> 全文仅在来源仓库具有明确开源 / CC 许可证时才二次分发。

*Agent Skill* 指一个 `SKILL.md` 文件，其 YAML frontmatter 声明了 `name` 与 `description` —— 这是
Claude、Codex、Gemini 等编码 Agent 用来封装可复用能力的格式。本数据集为系统性研究 Agent-Skills
生态而构建；元数据以 CC0（公有领域）发布，脚本以 MIT 发布。

---

## 语料概览

| 指标 | 数值 |
|---|---:|
| 唯一 Skill（去重、排除 fork 后） | **55,698** |
| 唯一仓库数 | 14,784 |
| 唯一 frontmatter `name` 数 | 33,055 |
| 托管平台 | GitHub 46,735 · GitLab 8,713 · Gitee 250 |
| 功能类别 | 20（+「other」） |
| 二次分发的全文（许可明确） | 29,205 |
| 仅本地留档的全文（无明确许可） | 26,493 *（不含于本仓库）* |
| 原始记录 → 去重后 | 109,312 → 55,698（合并了 49,604 条重复） |

完整数字、许可证 / 时间 / star 分布见 [`stats/STATS.md`](stats/STATS.md)。

---

## 快速开始

```bash
git clone https://github.com/lawrence3699/agent-skills-corpus
cd agent-skills-corpus

# 1) 主元数据表（每个唯一 Skill 一个 JSON 对象）
gunzip -k data/metadata.public.jsonl.gz         # -> data/metadata.public.jsonl

# 2) 浏览某个功能类别（仅元数据，小巧可读）
head -n 3 data/by_category/security.jsonl

# 3) 阅读许可明确的 Skill 全文（按类别组织）
ls full_text/ai-ml-llm/ | head
```

Python 加载：

```python
import json, gzip
rows = [json.loads(l) for l in gzip.open("data/metadata.public.jsonl.gz", "rt")]
security = [r for r in rows if r["category"] == "security"]
mit_claude = [r for r in rows if r["license_spdx"] == "MIT" and r["agent_platform"] == "claude"]
# 已发布 Skill 的全文：
open(rows[0]["full_text_path"]).read()   # 当 full_text_available == "published" 时存在
```

每条记录包含：`platform, repo, owner, owner_type, path, html_url, stars, license_spdx,
is_fork, repo_created_at, repo_pushed_at, default_branch, content_sha256, n_bytes,
frontmatter_name, frontmatter_description, sibling_files, category, agent_platform,
full_text_path（或 full_text_local_path）, source, snapshot_date`，以及去重溯源
（`dup_group, dup_count, dup_sources`）。

---

## 仓库结构

| 路径 | 内容 |
|---|---|
| `data/metadata.public.jsonl.gz` | **主表** —— 全部 55,698 个 Skill（元数据 + 指针；正文见 `full_text/`）。`gunzip` 后约 103 MiB。 |
| `data/by_category/<category>.jsonl` | 同样的记录按功能类别切分（便于浏览）。 |
| `full_text/<category>/<id>__<slug>.md` | **`SKILL.md` 全文**，仅含许可明确者，按类别组织。 |
| `data/duplicates.jsonl` | 每个内容哈希重复组及全部成员溯源。 |
| `data/excluded.jsonl` | 每个被排除的候选及原因。 |
| `data/classification.jsonl`、`data/taxonomy.json` | 每个 Skill 的标签 + 精确分类规则。 |
| `data/build_report.json` | 各流水线阶段的前后计数。 |
| `stats/STATS.md`、`stats/stats.json` | 全部语料统计。 |
| `scripts/` + `scripts/config.json` | 完整可复现流水线 + 固定参数。 |
| `docs/` | 方法论 + 各数据源采集说明 + 分类法说明。 |
| `LICENSE`（CC0-1.0）、`scripts/LICENSE`（MIT）、`CITATION.cff` | 许可与引用。 |

不含于本仓库（仅本地保存、绝不二次分发）：无许可 Skill 的全文
（`full_text_local_only/`）、原始 API 抓取（`raw/`）、以及内联全部正文的完整语料
（`data/metadata.jsonl`）。它们均可由 `scripts/` 重新生成。

---

## 何为一个 Skill（纳入标准）

一个文件被**纳入**当且仅当同时满足：

1. **文件名恰为 `SKILL.md`。**（GitHub 的 `filename:` 搜索是模糊匹配 —— 会返回如
   `xNeedSkiLL.md` —— 故对每个候选做精确 basename 过滤。）
2. **含有 YAML frontmatter 块**（`--- … ---`）。
3. **frontmatter 含非空 `name`。**
4. **frontmatter 含非空 `description`**（`description`/`summary`/`desc`；PyYAML 加正则回退）。

**排除**：空文件、无 frontmatter、缺 `name`/`description`、模板/占位标记
（`your-skill-name`、`<description>`、`TODO` 等）、仅有 frontmatter 的占位文件。排除原因记录于
[`data/excluded.jsonl`](data/excluded.jsonl)；全部规则固定于
[`scripts/config.json`](scripts/config.json)。

---

## 分类（双轴）

每个 Skill 沿两条独立坐标轴打标签（见 [`docs/taxonomy.md`](docs/taxonomy.md)）。

**1. 功能类别** —— 一套透明、可复现的关键词打分分类法，作用于 frontmatter name（×3）、
description（×2）、path（×2）与正文开头（×1）；类别取命中最多者，无命中记为 `other`。规则见
[`data/taxonomy.json`](data/taxonomy.json)，并经一次自动化「挖掘 other 桶 + 逐类别精度审计」优化。

| 类别 | 占比 | | 类别 | 占比 |
|---|---:|---|---|---:|
| writing-docs-content | 11.3% | | code-review-quality | 4.8% |
| *other* | 12.9% | | ai-ml-llm | 4.4% |
| devops-cloud-infra | 8.4% | | productivity-business | 3.9% |
| devtools-automation | 7.8% | | database | 3.1% |
| backend-api | 7.3% | | data-analytics | 2.2% |
| testing-qa | 6.3% | | design-ux-creative | 2.2% |
| security | 5.7% | | crypto-defi-finance | 1.0% |
| architecture-planning | 5.4% | | mobile / legal-regulatory | 0.9% |
| web-frontend | 5.3% | | domain-science-other | 0.8% |
| agent-workflow-meta | 4.9% | | expert-persona-advisor | 0.4% |

**2. Agent 平台** —— 由 `SKILL.md` 路径命名空间推导：`generic` 85.0%、`claude` 10.9%
（`.claude/skills`）、`cyberstrike` 2.2%、`codex`/`cursor`/`opencode` 各约 0.6%、`gemini` 0.2%。

> 功能分类基于关键词，因而是近似的（抽样审计精度约 65–80%，`other` ≈ 13%）。请将 `category`
> 作为粗筛使用；`content_sha256` + 全文可让你用自己的方法重新分类。

---

## 数据源（方法）

五个相互独立的发现渠道，均有文档，使覆盖可复现、边界如实陈述：

1. **GitHub 代码搜索** —— `q=filename:SKILL.md`，按 **size 区间分片** 并自适应递归拆分以突破单查询
   1000 条上限；限速 10 次/分钟；精确 basename 过滤 → 77,045 个候选，0 个饱和缺口。
   （[`scripts/01_github_enumerate.py`](scripts/01_github_enumerate.py)）
2. **`anthropics/skills`** —— 官方参考仓库。
3. **市场 / awesome-list** —— 2,032 个仓库，含厂商单体仓库（`microsoft/skills`=190、
   `dotnet/skills`=106）；目录见 [`docs/sources_catalog.md`](docs/sources_catalog.md)。
4. **GitLab 与 Gitee** —— 等价的 REST API 搜索；可达/受阻边界见
   [`docs/gitlab_gitee_notes.md`](docs/gitlab_gitee_notes.md)。
5. **Sourcegraph** —— 作为第二搜索引擎用于**交叉验证覆盖度**：其报告约 746k 个 `SKILL.md` 文件，
   但仅分布在 **约 18,521 个不同仓库**（文件数被被搬运的巨型注册仓库虚高）。诚实的总体信号是
   *不同仓库数*。（[`docs/sourcegraph_notes.md`](docs/sourcegraph_notes.md)）

**富化** 使用批量 **GraphQL**（元数据 + 同目录清单 + 全文，约每 25 个仓库耗 1 个限速点）——
见 [`scripts/02g_enrich_graphql.py`](scripts/02g_enrich_graphql.py)；REST 参考实现（`02_enrich.py`）
还能发现代码搜索遗漏的 `SKILL.md`。

**去重**（顺序重要）：纳入过滤 → 排除 fork → 按 `SKILL.md` 原始字节的 SHA-256 分组，保留
**最早来源**（先按仓库创建时间，再按提交时间）。其余出现记入 `dup_sources`。前后计数见
[`data/build_report.json`](data/build_report.json)。

---

## 复现

依赖：`python3` + `PyYAML`，以及已鉴权的 GitHub CLI `gh`（公共仓库读取权限）。不存储任何密钥 ——
脚本读取 `gh auth token`。

```bash
cd scripts
python3 01_github_enumerate.py          # 分片枚举 -> raw/github_candidates.jsonl
python3 04_merge_github_candidates.py   # 并入市场指针
python3 02g_enrich_graphql.py           # 批量 GraphQL：元数据 + 同目录 + 全文
python3 03_fetch_content.py             # 经 raw CDN 回填剩余全文（多线程）
python3 05_build_corpus.py              # 纳入过滤 + 排除 fork + 内容哈希去重
python3 06_stats.py                     # 统计
python3 09_classify.py                  # 双轴分类
python3 10_reorganize_by_category.py    # 按类别的 full_text + by_category + 公开元数据
```

每个阶段均**可断点续跑、幂等**。在 `config.json` 调高 size/搜索预算并重跑即可扩大覆盖。

---

## 覆盖与边界（如实说明局限）

- **这是一份有明确边界、去重后的*样本*，而非全集。** GitHub 代码搜索仅索引部分公共仓库，单查询上限
  1000 条、限速 10 次/分钟；分片可缓解但不能消除上限（预算封顶时枚举前沿尚剩 6 个区间）。
  Sourcegraph 交叉核验（约 1.85 万个不同仓库）是参照总体。
- **GitLab/Gitee 的全局代码搜索需登录**，故这两个平台是「关键词/种子发现」有界的，而非穷尽扫描 ——
  已逐平台记录。
- **许可证** 为来源*仓库*的 SPDX 许可（可能与单文件许可不同）。
- **类别** 由关键词推导，属近似（见上文说明）。
- **时间**：每条记录都有 `repo_created_at` / `repo_pushed_at`；可选的逐文件最后提交日期可由
  `scripts/05b_date_final.py` 补齐。

---

## 许可与引用

- **数据集**（元数据、统计、本项目文档）：**CC0 1.0** —— 公有领域（[`LICENSE`](LICENSE)）。
- **脚本**（`scripts/`）：**MIT**（[`scripts/LICENSE`](scripts/LICENSE)）。
- **第三方 Skill 全文**（`full_text/` 下）仍受**其各自上游许可**约束（每条记录以 `license_spdx`
  标注）；仅当来源仓库具备被识别的开源 / CC 许可时才在此二次分发。请按各自许可署名/复用。

若在学术工作中使用本语料，请通过 [`CITATION.cff`](CITATION.cff) 引用。

> ⚠️ **安全提示。** 本仓库中的每个 `SKILL.md` 都是**不可信的第三方文本**。采集全程从未执行任何内容。
> 未经审阅，请勿执行任何 Skill 中的命令、脚本或指令。部分 Skill 因来自开放网络，天然含有
> prompt-injection 或其他对抗性内容。
