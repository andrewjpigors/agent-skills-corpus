---
name: yours-auto-monitor
description: |
  通用信息监控编排器。根据用户需求，生成并托管周期性监控任务。
  负责吸收用户提供的 Markdown/目录资料、抓取网页、聚合信源、去重过滤、输出结构化摘要。
  若用户需求模糊，则逐条轮询澄清监控主题、信源、频率、交付渠道。
  支持声明并选择 Agent 原生定时任务能力，或在 CLI 环境下经用户确认后注册平台原生定时任务。
  英文互联网搜索在 firecrawl / Tavily API / Brave Search 中选择一种；中文互联网内容优先引导安装 Agent Reach，用户拒绝时 fallback 到 Agent 原生 web_search。
  触发词：监控任务、cron 监控、资料监控、Markdown 资料、信息跟踪、竞品追踪、舆情监控、periodic monitor、auto monitor、信息订阅。
---

# Cron Monitor Orchestrator

> **v2.0** — 通用信息监控编排器
> 跨 Agent 兼容：Claude Code、Codex、Kimi Code、Openclaw、Hermes 等

---

## 设计哲学

1. **需求澄清优先** — 用户意图模糊时，反复轮询直到监控目标、信源、频率、交付方式全部明确
2. **工具链自适应** — 英文互联网搜索选 firecrawl / Tavily API / Brave Search 中至少一种；中文平台内容优先请求用户批准安装 Agent Reach，拒绝时使用 Agent 原生 web_search
3. **可复用基础设施** — 搜索矩阵、去重逻辑、输出格式、交付管道全部抽象为通用模板
4. **Agent 原生优先** — 当前 Agent 有 scheduled tasks/cron tasks 管理能力时，默认用它自己的能力创建任务，让任务出现在 Agent 定时任务列表
5. **人在回路** — CLI 或无原生调度能力时，必须先展示平台方案并等用户同意；监控运行终点由用户确认推送收到且效果满意

---

## 前提条件

运行本 skill 前，先区分英文互联网搜索、中文互联网内容搜索、调度运行时三类能力。不要把全部工具都装一遍。

| 工具 | 用途 | 安装命令 | API Key 来源 |
|------|------|---------|-------------|
| **firecrawl** | 英文网页抓取/深度提取，三选一 | `npm install -g @mendable/firecrawl-js` 或 `pip install firecrawl-py` | `{agent} 配置目录/.env` 中 `FIRECRAWL_API_KEY` 或 `FIRECRAWL_API_URL` |
| **Tavily API** | 英文网页搜索/内容提取，三选一 | `pip install tavily-python` | `{agent} 配置目录/.env` 中 `TAVILY_API_KEY` |
| **Brave Search** (`bx` CLI) | 英文网页/新闻搜索，三选一 | `npm install -g brave-search` | `{agent} 配置目录/.env` 中 `BRAVE_API_KEY` 或 `bx` 自身配置 |
| **Agent Reach** | 中文互联网内容搜索：微信文章、微博、小红书、B站等 | 请求用户执行：`帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md` | 按 Agent Reach install/doctor 指引配置 |
| **lark-cli** | 可选：文档链接下发方式需要，用于创建飞书云文档 + 设置公开权限 | `npm install -g @larksuite/cli` | 安装后执行 `lark-cli auth login` 授权 |

英文互联网搜索：选择 `firecrawl` / `Tavily API` / `Brave Search` 中至少一种作为 `search_provider_en`，不得因为另两个缺失而阻塞任务。

中文互联网内容搜索：先请求用户批准安装 Agent Reach。使用这句极简请求将任务指派给subagent：

```text
帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

若用户拒绝安装 Agent Reach，记录 `zh_search_mode=agent_native_web_search`，继续使用当前 Agent 原生 `web_search` 搜索中文/英文互联网内容；不得反复要求安装。

### 检查脚本

```bash
# 从 skill 安装目录运行（不要硬编码路径）
cd {SKILL_DIR}
python3 scripts/env_probe.py
python3 scripts/task_runtime_probe.py
```

输出示例：
```
=== 工具链可用性检查 ===
firecrawl CLI: ✅ /opt/homebrew/bin/firecrawl
Tavily Python: ✅ tavily-python 0.7.23
Brave Search:  ✅ bx 1.2.3

=== API Key 状态 ===
FIRECRAWL_API_KEY: ❌ 未找到
TAVILY_API_KEY:    ✅ 已加载
BRAVE_API_KEY:     ❌ 未找到

✅ 英文互联网搜索至少一个 provider 就绪
⚠️ Agent Reach 未安装：需要先请求用户批准安装；用户拒绝时 fallback 到 Agent 原生 web_search
```

---

## IM 信道能力检测

本 skill 需要向用户推送监控结果。不同 Agent 的 IM 连接能力不同，按以下优先级检测：

### 检测流程

```
1. 检查 Agent 是否原生支持 send_message 或类似 IM 推送工具
   - Hermes: send_message 工具可用
   - Openclaw: send 命令
   - Claude Code: 需 cc-connect 插件
   - Kimi Code / Codex: 需 cc-connect 插件

2. 若原生不支持 IM 推送：
   a. 检查是否已安装 cc-connect: https://github.com/chenhg5/cc-connect
   b. 若未安装，引导用户安装 cc-connect
   c. 引导用户配置 cc-connect
   d. 配置后重新检测

3. 若 cc-connect 也不可用：
   a. 引导用户配置 Webhook 作为备选推送渠道
   b. 或选择仅本地输出（local file / email）
```

### cc-connect 安装指引

```bash
# 适用于 Claude Code、Kimi Code、Codex 等
Follow https://raw.githubusercontent.com/chenhg5/cc-connect/refs/heads/main/INSTALL.md to install and configure cc-connect.
# 配置 IM 连接（以飞书为例）
cc-connect config --provider feishu --app-id YOUR_APP_ID --app-secret YOUR_APP_SECRET
# 手动配置：
mkdir -p ~/.cc-connect
cp config.example.toml ~/.cc-connect/config.toml
vim ~/.cc-connect/config.toml
# 参考：
https://github.com/chenhg5/cc-connect
```

### 检测脚本

```bash
cd {SKILL_DIR}
python3 scripts/channel_probe.py
```

---

## 去重后端选择

本 skill 支持多种去重记录存储方式。Agent 须引导用户选择其中一种：

| 后端 | 类型 | 安装方式 | 适用场景 |
|------|------|---------|---------|
| **hindsight** | Agent 内置记忆 | 随 Agent 自带 | 同一会话内短期去重 |
| **mem0** | 开源记忆层 | `pip install mem0ai` | 跨会话长期记忆 |
| **agentmemory** | 开源记忆层 | `pip install agentmemory` | 跨会话长期记忆，SQLite 存储 |
| **lark-cli** | 飞书文档 | `npm install -g @larksuite/cli` | 团队协作，文档化记录 |
| **local** | 本地文件 | 无需安装 | 单机使用，简单可靠 |

### 选择流程

```
1. 向用户展示上表，询问偏好
2. 若用户选择 hindsight/mem0/agentmemory：
   a. 检查是否已安装
   b. 若未安装，引导安装并配置
   c. 测试读写是否正常

3. 若用户选择 lark-cli：
   a. 检查 lark-cli 是否已安装并登录
   b. 引导用户创建或指定一个飞书文档作为去重记录存储
   c. 记录文档 URL 或 token 到配置

4. 若用户选择 local（默认）：
   a. 确认本地存储路径（默认: {agent}/cron/output/{task_name}/processed_urls.txt）
   b. 确保目录可写
```

### 配置格式

去重后端配置写入 `{agent}/.env`：

```bash
# 选择一种后端
DEDUP_BACKEND=local          # 可选: hindsight, mem0, agentmemory, lark, local

# local 后端路径（可选，默认见上）
DEDUP_LOCAL_PATH={agent}/cron/output/{task_name}/processed_urls.txt

# mem0 / agentmemory 配置
MEM0_API_KEY=your_key        # 若使用 mem0 云服务
AGENTMEMORY_DB_PATH={agent}/data/agentmemory.db

# lark 后端配置
LARK_DEDUP_DOC_TOKEN=doc_token_here
LARK_DEDUP_TABLE_ID=table_id_here
```

---

## 工作流程

### Phase 0A: 用户资料吸收（用户给出文件或目录时先执行）

输入：用户引用的 `.md` / `.txt` / `.csv` / `.json` 文件，或包含这些文件的目录。

输出：一份归一化的监控需求摘要，必须使用固定字段：`task_name`、`topic`、`entities`、`columns`、`direct_urls`、`wechat_sources`、`platform_sources`、`cross_queries`、`known_frequency`、`known_delivery`、`known_delivery_method`、`known_output_format`、`search_provider_en`、`zh_search_mode`、`scheduler_capability`、`dedup_backend`、`missing_fields`、`conflicts`。

```
1. 列出用户给出的所有文件；目录输入按文件名排序读取，忽略隐藏文件和备份文件。
2. 从资料中提取并合并四类信息：
   a. 实体清单：公司、产品、公众号、关键词；保留中英文别名和优先级。
   b. 栏目/维度：临床进展、交易动态、监管审批、学术突破、早筛/诊断等。
   c. 信源清单：URL、数据库、监管机构、交易所、会议、公众号、行业媒体。
   d. 运行约束：频率、交付渠道、下发方式、输出格式、排除规则、语言。
3. 将文件名作为语义线索：
   - `栏目说明.md` → `columns` 和输出栏目模板
   - `信源清单.md` → `direct_urls` / `wechat_sources` / `platform_sources`，按下方分类表拆分
   - `重点关注*名单.md` / `药企名单*.md` → `entities` 和 priority
   - 单文件中出现的“网页抓取关键词” → `cross_queries`
   - 单文件中出现的“公众号名称” → `wechat_sources`，不得伪造 URL
4. 检测并处理特殊资料问题：
   - **重复文件**：文件名含 `copy` / `副本` / `备份` / `backup` 或内容 MD5 相同 → 标记 `duplicate_source`，优先使用原始文件，跳过重复提取
   - **近重复实体**：简称与全称并存（如"诺辉" vs "诺辉健康"）或中英文别名指向同一实体 → 合并为单一实体，保留最长正式名称，别名记入 `aliases`
   - **无实体清单**：资料中只有行业/领域描述，无具体公司/产品/关键词 → 标记 `entity_scope=generic`，进入 Phase 0 追问用户补充至少 3-5 个重点实体，或确认按泛行业模式运行
5. 对照 Phase 0 十项清单，只追问 `missing_fields`；资料中已经明确的信息不得重复询问。
6. 若资料冲突，列出冲突字段、冲突来源文件和候选值，让用户选择；不得自行吞掉冲突。
7. 若用户明确要求"搜索矩阵设计/预览"，在 Phase 0A 输出 `matrix_preview`，只包含 query 模板、信源分组和示例条目；不得写文件、不得运行工具、不得创建任务。
8. 若用户允许落盘且当前环境可写，将确认后的摘要保存为 `{agent}/scripts/{task_name}_brief.md`；用户要求只预览或不改文件时，不写任何文件。
```

信源分类规则：

| 输入形态 | 归一化字段 | 处理规则 |
|---|---|---|
| `http://` / `https://` URL | `direct_urls` | 保留 URL、名称、类型、更新频率；后续用 `firecrawl` / `curl` / 数据库页面监控 |
| `微信公众号搜索：X`、`公众号名称`、无 URL 的公众号 | `wechat_sources` | 只保留账号名和栏目角色；生成“账号名 + 关键词 + 时间限定词”query；不得写入 `direct_urls` |
| 微博号、交易平台内账号、数据库入口但无具体 URL | `platform_sources` | 保留平台名、账号/入口名、检索方式；后续用平台搜索或用户提供的 URL 补全 |
| “网页抓取关键词”、疾病/技术/产品关键词 | `cross_queries` | 按主题分组，不作为实体；用于全局 query 和实体 query 模板 |
| 公司/产品/药物/靶点名单 | `entities` | 保留原名、英文别名、类别、priority、来源文件 |

资料吸收摘要模板：
```markdown
# {task_name} 监控需求摘要

- 主题：{topic}
- 重点实体：{entities_count} 个，按 priority 分组
- 栏目：{columns}
- 直接 URL：{direct_urls_count} 个
- 公众号：{wechat_sources_count} 个
- 平台内信源：{platform_sources_count} 个
- 全局关键词：{cross_queries_count} 组
- 已明确：频率={known_frequency}；交付={known_delivery}；下发方式={known_delivery_method}；输出={known_output_format}；去重={dedup_backend}
- 搜索：英文={search_provider_en}；中文={zh_search_mode}
- 调度：{scheduler_capability}
- 待确认：{missing_fields}
- 冲突：{conflicts}
```

🔴 **CHECKPOINT · 🛑 STOP**：资料吸收完成后，展示摘要和待确认项；用户确认或补齐缺口后再进入 Phase 1。

### Phase 0: 需求澄清（必须完成，不可跳过）

若用户没有提供可解析资料，或 Phase 0A 后仍存在缺口，按以下清单逐条确认。资料中已经明确的字段直接填入，不重复追问：

| # | 确认项 | 示例回答 |
|---|--------|---------|
| 1 | **监控主题**是什么？ | "全球肿瘤新药研发动态"、"AI 芯片行业融资" |
| 2 | **目标实体**清单？ | 药企名单、创业公司列表、关键词集合。若用户仅给出行业/领域（如"AI 制药"），标记 `entity_scope=generic`，追问补充 3-5 个重点实体或确认泛行业模式 |
| 3 | **监控维度**？ | 临床进展、交易动态、监管审批、财报、技术突破 |
| 4 | **信源偏好**？ | 学术期刊、监管机构、行业媒体、公司公告、社交媒体 |
| 5 | **更新频率**？ | 实时、每日、每周一/四、每月 |
| 6 | **交付渠道**？ | 飞书、企业微信、Telegram、邮件、本地文件、Webhook |
| 7 | **下发方式**？ | `direct`：cc-connect/Agent IM 直接推送；`doc_link`：lark-cli 存飞书文档后推摘要+URL |
| 8 | **输出格式**？ | 一行一条摘要、Markdown 报告、结构化表格、客观 R&D 简报 |
| 9 | **排除规则**？ | 旧闻重发、股价波动、纯广告 |
| 10 | **语言**？ | 中文为主、英文为主、双语 |

🔴 **CHECKPOINT · 🛑 STOP**：Phase 0 完成后，向用户复述完整监控方案，确认无误再进入 Phase 1。

### Phase 1: 信源映射

根据用户确认的信源偏好，将抽象需求映射到具体 URL / API / 搜索 query：

```
1. 列出所有候选信源
2. 为每个实体（公司/关键词）设计搜索矩阵：
   - 中文搜索 query（用于 Agent Reach；用户拒绝安装时用于 Agent 原生 web_search）
   - 英文搜索 query（用于已选定的 `search_provider_en`，三选一）
   - 直接监控 URL（官网新闻页、投资者关系页）
   - 公众号或无 URL 信源：生成“公众号名 + 关键词 + 时间限定词”的搜索 query，不写入 direct_urls
3. 将搜索矩阵保存到 {agent}/scripts/{task_name}_matrix.json
4. 保存执行说明 `{agent}/scripts/{task_name}_runbook.md`，写明每轮运行要用哪个 Agent 原生搜索工具或哪个单一 provider；不得引用已删除的 `search_runner.py`
```

搜索矩阵示例：
```json
{
  "task_name": "pharma-pipeline-tracker",
  "entities": [
    {
      "name": "罗氏制药",
      "name_en": "Roche",
      "queries": {
        "zh": ["罗氏制药 新药临床", "Roche 中国 获批"],
        "en": ["Roche oncology pipeline update", "Roche FDA approval"]
      },
      "direct_urls": ["https://www.roche.com/media/releases.htm"]
    }
  ],
  "cross_queries": {
    "zh": "肿瘤新药 本周 动态",
    "en": "oncology drug development this week"
  }
}
```

### Phase 2: 工具链检查与补齐

```
1. 运行 env_probe.py 扫描现有工具。
2. 英文互联网搜索只需选择一个 provider：
   - `firecrawl`：适合固定 URL、单页深抓、全文提取
   - `Tavily API`：适合英文网页搜索和摘要
   - `Brave Search`：适合英文网页/新闻快速搜索
3. 若三个英文 provider 都不可用：
   a. 向用户说明只需三选一，不要求全部安装。
   b. 让用户选择要补齐哪一个，再提供安装和 API key 配置指引。
   c. 安装或配置完成后重新运行 env_probe.py。
4. 中文互联网内容搜索：
   a. 若 Agent Reach 可用，设置 `zh_search_mode=agent_reach`。
   b. 若不可用，必须请求用户批准安装，原文请求：
      `帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md`
   c. 若用户同意，安装后运行 `agent-reach doctor`。
   d. 若用户拒绝，设置 `zh_search_mode=agent_native_web_search`，使用 Agent 原生 web_search 搜索中文/英文互联网内容。
5. 按任务类型判断是否通过：
   - 英文搜索/固定 URL：已选 `search_provider_en` 可用 → 通过
   - 中文平台内容：`agent_reach` 可用，或用户已明确拒绝并接受 `agent_native_web_search` fallback → 通过
   - 以上均不可用 → 不通过，继续补齐或缩小监控范围
```

🔴 **CHECKPOINT · 🛑 STOP**：工具链齐全后，告知用户当前可用工具清单，确认无误再进入 Phase 2.5。

### Phase 2.5: 推送渠道与下发方式配置（不可跳过）

```
1. 运行 channel_probe.py 扫描已连接的 IM 频道
2. 向用户展示可用渠道清单，让其选择（可多选）：
   - 飞书 / 企业微信 / 个人微信 / Telegram / QQ Bot
   - Webhook（自定义 HTTP POST）
   - 本地文件 / Email
3. 对未配置的渠道：
   a. 展示配置指引（环境变量名、获取方式）
   b. 引导用户写入 {agent}/.env
   c. 重新探测确认
4. 若用户选择 Webhook：
   a. 收集 webhook URL
   b. 写入 {agent}/.env 作为 WEBHOOK_URL
   c. 询问推送格式（JSON / form-data / 纯文本）
5. 若 Agent 无原生 IM 能力且未安装 cc-connect：
   a. 引导用户安装 cc-connect: https://github.com/chenhg5/cc-connect
   b. 或选择 Webhook / 本地输出作为备选
6. 询问下发方式（delivery_method），二选一：
   - `direct`（默认）— 使用 Agent 原生 IM / cc-connect / Webhook 直接推送消息
   - `doc_link` — 使用 lark-cli 将完整报告存入飞书云文档，再向用户指定信道推送摘要+URL

   **判断依据**：预估报告长度 > 4KB 或输出格式为「客观 R&D 简报」时，主动推荐 `doc_link`；短摘要或一行式输出用 `direct`。
7. 若用户选择 `doc_link`：
   a. 检查 `lark-cli` 是否已安装（`which lark-cli`）
   b. 若未安装，询问用户是否安装：
      - 安装命令：`npm install -g @larksuite/cli`
      - 用户同意 → 执行安装，继续步骤 c
      - 用户拒绝 → 回退到 `direct` 下发方式，或让用户重新选择
   c. 检查 `lark-cli` 是否已登录授权：
      ```bash
      lark-cli auth status 2>&1
      ```
   d. 若未授权，引导用户执行：
      ```bash
      lark-cli auth login
      ```
      完成后重新检查授权状态。
   e. 验证 lark-cli 可创建文档：
      ```bash
      lark-cli docs +create --api-version v2 --doc-format markdown --content "# test" --as user 2>&1
      ```
      确认返回 JSON 中含 `document_id` 和 `url`。
8. 生成交付配置：
   - deliver（去哪）："wecom:channel_name" / "telegram" / "feishu" / "webhook" / "local" 等
   - delivery_method（怎么发）："direct" 或 "doc_link"
```

🔴 **CHECKPOINT · 🛑 STOP**：渠道与下发方式配置完成后，展示用户选择的交付方案，确认无误再进入 Phase 3（或 Phase 2.6）。

### Phase 2.6: 文档链接下发方式配置（仅 delivery_method=doc_link 时执行）

当用户选择 `delivery_method=doc_link` 时，必须完成本阶段。该方式与 `direct`（Agent IM / cc-connect / Webhook 直推）并列可选，不是交付渠道。它用于将完整报告以飞书云文档承载，向用户指定信道只推摘要+URL，避免长文本撑爆 IM 消息限制。

```
前提：Phase 2.5 步骤 7 已确认 lark-cli 安装且授权通过。

1. 配置文档标题模板
   a. 询问用户文档标题格式，默认模板："{task_name} 监控周报（{date}）"
   b. {date} 使用执行日期，格式 %y.%m.%d（如 26.07.06）
   c. 将标题模板写入 {agent}/scripts/{task_name}_runbook.md

2. 配置文档公开权限
   a. 告知用户：每轮运行将自动创建飞书云文档并设置为"任何人凭链接可读"
   b. 对应 lark-cli 命令：lark-cli drive permission.public patch --token {doc_id} --type docx --data '{"link_share_entity":"anyone_readable"}' --as user --yes
   c. 用户确认此权限设置可接受后继续

3. 配置摘要提取规则
   a. 从报告内容提取以下字段作为 IM/Webhook 推送摘要：
      - 监测周期（📅 或"监测周期"行）
      - 重点关注条目（🔥 标记行或重点关注章节）
      - 最多 3-5 行
   b. 将摘要规则写入 runbook

4. 配置推送链路
   a. doc_link 链路：创建飞书文档 → 提取摘要 → 将"摘要 + 飞书文档链接"推送到 Phase 2.5 选定的交付渠道
   b. 若 deliver=wecom:channel_name 且 delivery_method=doc_link，推送格式：
      "📊 {task_name} 监控周报\n\n{summary}\n\n完整报告见飞书文档：\n{doc_url}"
   c. 若未选择可接收摘要+URL的交付渠道，提示用户：还需要至少一个 IM/Webhook 渠道，或选择 local 自行查看

5. Dry run 文档创建验证
   a. 创建一个测试飞书文档，确认 lark-cli + 授权 + 权限设置全链路通
   b. 向用户展示创建的测试文档 URL，确认可以免登录访问
   c. 删除测试文档（lark-cli drive file delete --token {doc_id} --as user --yes）
```

🔴 **CHECKPOINT · 🛑 STOP**：链路配置完成且测试文档可访问后，展示配置摘要，用户确认再进入 Phase 3。

### Phase 3: 预跑验证（Dry Run）

在创建监控任务前，先手动执行一轮完整搜索，**并实际测试推送渠道**：

```
1. 使用已确认的 `search_provider_en` 执行搜索矩阵的前 3 个英文 query。
2. 使用 `zh_search_mode` 执行前 3 个中文 query：
   - `agent_reach`：优先用微信文章、微博、小红书、B站等对应 channel。
   - `agent_native_web_search`：使用当前 Agent 原生 web_search，不再要求安装 Agent Reach。
3. 对 `direct_urls` 用当前 provider 的 URL 抽取能力、Agent 原生网页读取能力，或轻量 `curl`/reader 读取；不得调用 `search_runner.py`。
4. 检查输出质量：
   - 结果是否相关？
   - 时间戳是否在预期范围内？
   - 是否有大量死链或重复？
5. 对每个选定的推送渠道发送测试消息：
   - IM 频道：用 Agent 原生推送工具或 cc-connect 发送测试消息
   - Webhook：用 test_push.py --channel webhook 发送测试 POST
   - 本地：检查文件是否正确写入
6. 待用户回复是否收到测试消息：
   - 收到 → 继续
   - 未收到 → 排查渠道配置，重发测试，或更换渠道
7. 若质量不达标：
   - 调整 query 关键词
   - 更换英文 provider（三选一中的另一个）
   - 将中文搜索从 Agent 原生 web_search 升级为 Agent Reach（仍需用户批准）
   - 补充直接 URL 监控
8. 将调整后矩阵写回 JSON，并同步更新 `{task_name}_runbook.md`
```

🔴 **CHECKPOINT · 🛑 STOP**：Dry run 结果和测试推送展示给用户，确认搜索质量满意**且**推送测试通过后再创建监控任务。

### Phase 4: 定时任务运行时声明与创建

创建任务前，先声明当前 Agent 的调度能力。运行：

```bash
cd {SKILL_DIR}
python3 scripts/task_runtime_probe.py
```

按结果进入 A 或 B。

#### A. Agent 有原生 scheduled tasks / cron tasks 管理能力（默认）

适用：Openclaw、Hermes、Claude Code Desktop、Codex App、Kimi Work。

```
1. 优先使用 Agent 自身创建和管理定时任务的能力。
2. 任务必须出现在 Agent 自己的定时任务/自动化/cron 管理列表中，方便用户查看、暂停、删除。
3. 任务体使用 `{task_name}_runbook.md` 和 `{task_name}_matrix.json`，由 Agent 在每轮运行时调用已确认的搜索 provider、去重后端和推送渠道。
4. 创建后展示：
   - Agent 原生任务名称 / ID
   - schedule / cron 表达式
   - 下次执行时间
   - 管理入口或查看命令
```

示例映射：

| Agent | 默认调度能力 |
|---|---|
| Openclaw | Openclaw scheduled tasks / cron tasks；任务应在 Openclaw 列表可见 |
| Hermes | Hermes cronjob；任务应在 Hermes cron 管理列表可见 |
| Claude Code Desktop | Routines / Scheduled Tasks |
| Codex App | Scheduled Automations |
| Kimi Work | Kimi Work scheduled tasks |

#### B. Agent 无原生本地持久化调度能力

适用：Claude Code CLI、Kimi Code CLI、Codex CLI，以及无法检测到原生调度列表的运行时。

先检测用户系统，再展示平台原生方案。**必须等待用户同意方案后才开始创建任务。**

| 平台 | 首选方案 | 关键能力 | 何时用 |
|---|---|---|---|
| macOS | `launchd` User Agent (`~/Library/LaunchAgents/*.plist`) | 登录自启、`StartCalendarInterval`、系统唤醒后补跑错过任务、日志路径 | 本地 Mac 长期运行 |
| Windows | Task Scheduler (`Register-ScheduledTask`) | `WakeToRun`、`StartWhenAvailable`、`RestartCount`、任务计划程序可见 | Windows 桌面/工作站 |
| Linux | `systemd --user` service + timer | `Persistent=true` 补跑、`journalctl` 日志、`enable --user` | Linux 桌面/服务器 |
| 其他 | POSIX cron fallback | 基础定时 | 仅在前三者不可用时使用；需说明休眠补跑风险 |

CLI 环境检查点模板：

```markdown
## 定时任务创建方案确认

- 当前 Agent：{agent_name}（未检测到原生 scheduled tasks/cron tasks 管理能力）
- 当前系统：{platform}
- 推荐方案：{launchd | Windows Task Scheduler | systemd user timer | cron fallback}
- 任务名称：{task_name}
- 频率：{cron_expr_or_calendar}
- 下发方式：{delivery_method}
- 执行命令：{runtime_command}
- 日志位置：{stdout_log} / {stderr_log}
- 管理/删除方式：{management_command}
- 风险：{missed_run_or_wake_notes}

请确认是否按此方案创建。你回复同意后我再注册任务。
```

🔴 **CHECKPOINT · 🛑 STOP**：展示上述方案确认模板，用户回复"同意"或"确认"后才注册任务。未获明确同意前不得写入 `launchd` plist、Windows Task Scheduler 或 systemd timer。

生成 `runtime_command` 时，优先调用当前 Agent 的非交互 CLI 让它执行 `{task_name}_runbook.md`；若没有可靠非交互 CLI，则生成当前任务专用的轻量脚本，脚本只使用已选 `search_provider_en`、`zh_search_mode`、去重后端、推送渠道和 `delivery_method`。不得复活或引用 `search_runner.py`。

**`deliver` 字段规范**：
- `"wecom:channel_name"` — 单一企业微信频道
- `"telegram"` — Telegram 频道
- `"feishu"` — 飞书频道
- `"weixin"` — 个人微信频道
- `"qqbot"` — QQ Bot 频道
- `"wecom:channel_name,telegram,feishu"` — 多渠道同时推送
- `"webhook"` — POST 到配置的 WEBHOOK_URL
- `"local"` — 仅保存本地文件
- `"email"` — 发送邮件（需配置 SMTP）

**`delivery_method` 字段规范**：
- `"direct"` — 默认。使用 Agent 原生 IM / cc-connect / webhook 直接推送消息
- `"doc_link"` — 使用 lark-cli 将完整报告存入飞书云文档，再向 `deliver` 指定信道推送摘要+URL

创建后展示给用户：
- 任务名称 / ID
- 下次执行时间
- **交付渠道清单**（刚创建时选定的所有渠道）
- **下发方式**（direct 或 doc_link）
- 测试运行命令

### Phase 5: 运行终点与满意度确认

skill 的运行终点不是“任务已注册”，而是以下全部成立：

```
1. 定时任务试跑成功：手动触发或立即运行一次，完成搜索、去重、摘要生成、推送。
2. 用户确认 IM 平台已收到推送：飞书/企业微信/Telegram/个人微信/QQ Bot/Webhook 接收端均按用户选择验证。
3. 若 `delivery_method=doc_link`：确认飞书文档已创建、公开链接免登录可访问、摘要+URL 已推送到指定信道。
4. 用户确认 IM 端消息效果满意：标题、摘要粒度、链接、栏目、格式、噪声控制符合预期。
```

若任一项不成立，不得宣布完成。根据用户新输入意见调整 query、信源、摘要格式、推送模板、调度命令或渠道配置，然后重新试跑并再次请求确认。

---

## 搜索执行规范

### 工具选择优先级

| 场景 | 首选规则 | 备选规则 |
|------|---------|---------|
| 英文互联网搜索 | 在 `firecrawl` / `Tavily API` / `Brave Search` 中选择一种作为 `search_provider_en` | 用户同意后切换到另一个 provider |
| 中文互联网内容搜索 | Agent Reach（微信文章、微博、小红书、B站等 channel） | 用户拒绝安装时，用 Agent 原生 `web_search` 查询中文/英文内容 |
| 固定 URL 更新 | 已选 provider 的 URL 抽取能力或 Agent 原生网页读取 | `curl`/reader + diff |
| 平台内账号/公众号 | Agent Reach 对应平台 channel | Agent 原生 `web_search` 的“账号名 + 关键词 + 时间限定词”query |

### 搜索矩阵执行顺序

```
for each entity in matrix:
  1. 用 zh_search_mode 执行中文 query
  2. 用 search_provider_en 执行英文 query
  3. 对 direct_urls 抽取标题、正文、发布时间
  4. 汇总结果并按去重后端过滤
  5. 生成摘要并推送
```

### 去重机制

```
1. 规范化 URL（去除查询参数、锚点，统一小写）
2. 检查已处理记录（根据用户选择的 DEDUP_BACKEND）：
   - hindsight: 调用 hindsight_recall "{task_name} dedup"
   - mem0: 查询 mem0 API
   - agentmemory: 查询 agentmemory
   - lark: 读取飞书文档/表格
   - local: 读取 {agent}/cron/output/{job_id}/processed_urls.txt
3. 仅处理未出现过的条目
4. 新条目写入去重记录
```

---

## 输出格式模板

### 单条摘要（默认）
```
【实体名】|【类型：研发/财报/战略/监管/学术】|【一句话总结】|【信源URL】|【发布时间】
```

### Markdown 报告（可选）
```markdown
# {task_name} 监控周报（截至 {date}）

## {实体A}
- 【类型】| {摘要} | [来源](URL) | {日期}

## {实体B}
- 本周暂无新动态。

## 备注
- 去重：已排除 X 条重复/旧闻
- 数据落库：{成功/失败说明}
```

### 客观 R&D 简报（推荐格式）
纯客观、学术中立。零感性评述，零宏大叙事。每条固定结构：

```markdown
# {task_name} 监控周报（{date}）

📅 **监测周期**：{start_date} — {end_date}
📊 **动态分类**：产品发布 / 临床数据 / 融资合作 / 监管获批 / 学术发表

## 一、{分组A}（如：国内竞品动态）

1. **{实体名}** — [{分类}]
   - **{日期}**，{客观事实描述，不带主观判断}
   - 🔍 来源：{provider} | [{标题}]({url})
   - 💡 简评：{一行中立技术/商业评价，不抒情}

2. **{实体名}** — [无新动态]
   - 🔍 来源：{provider}

## 二、{分组B}（如：国外竞品动态）

（同上格式）

## 三、重点关注

| 动态 | 关联度 | 核心影响 |
|---|---|---|
| {事件} | ⭐⭐⭐ | {一句客观影响描述} |
```

**简报格式约束**：
- 分类法固定：产品发布 / 临床数据 / 融资合作 / 监管获批 / 学术发表 / 无新动态
- 每条必须带直接新闻链接，不只工具引用名
- 💡 简评限一行，中立、专业，不抒情不叙事
- 无动态实体也列出，标注 `[无新动态]`，不省略

---

## 异常与边界条件

| 场景 | 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|---|
| 英文 provider 缺失 | firecrawl / Tavily API / Brave Search 均不可用 | 告诉用户三选一，让用户选定后引导安装配置 | 缩小监控范围至纯中文信源，或改用 Agent 原生 web_search 搜索英文内容 |
| Agent Reach 缺失 | 中文互联网内容搜索需要微信文章、微博、小红书等平台 | 请求用户批准安装 Agent Reach | 用户拒绝 → `zh_search_mode=agent_native_web_search`，不再追问 |
| API key 缺失 | `.env` 中对应 key 为空 | 提示用户获取 key 并写入 `.env` | 切换到不需要 key 的 provider（如 Brave CLI 自带配置） |
| 安装命令失败 | npm/pip 返回非零退出码 | 切换备选：npm → npx；pip → pip3 / python3 -m pip | 展示手动安装步骤，或跳过该工具改用其他 provider |
| 搜索返回空 | 所有 query 均无结果 | 扩大关键词范围，降低过滤严格度 | 切换 search_provider_en 或补充 direct_urls 直接监控 |
| 结果全为旧闻 | 发布时间均超阈值 | 检查 query 是否含时间限定词 | 切换信源或扩大时间窗口 |
| 用户资料路径不存在 | Phase 0A 中任一文件或目录无法读取 | 列出不可读路径，继续处理其余可读资料 | 全部不可读 → 要求用户重新提供路径 |
| 资料字段冲突 | 多个文件给出不同频率、栏目或重点名单 | 展示冲突表，要求用户选择一个版本 | 用户不选 → 暂停任务创建，标记 `conflicts` 待定 |
| 资料过大 | 实体超过 80 个或信源超过 120 个 | 按优先级分组，先生成 priority=high 的矩阵 | 询问是否分批监控，低优先级实体延后 |
| 公众号无 URL | 信源为微信公众号、微博账号或平台内账号 | 归入 `wechat_sources` / `platform_sources`，用搜索 query 监控 | 不得伪造网页 URL |
| 单文件混合多种角色 | 同一 Markdown 同时包含公司、公众号、关键词、栏目 | 按标题层级拆成实体、信源、关键词、栏目四类 | 无法分类的条目放入待确认列表 |
| 去重记录损坏 | processed_urls.txt 无法读取 | 重建空文件，下一周期自然恢复 | 切换 DEDUP_BACKEND 到 hindsight 或 local 其他路径 |
| 无原生调度能力 | task_runtime_probe.py 显示 `has_native_scheduler=false` | 检测 OS，展示 launchd / Task Scheduler / systemd 方案 | 等用户同意后才创建；用户拒绝 → 仅生成 runbook 供手动执行 |
| 任务创建失败 | Agent 原生调度或平台调度注册报错 | 检查 schedule 格式、运行命令、prompt 文件路径、脚本权限 | 降级为生成 runbook + 手动执行指引 |
| 交付失败 | 推送返回错误 | 重试一次 | 仍失败 → 写本地文件并告警 |
| 推送渠道未配置 | channel_probe.py 检测到 0 个可用渠道 | 强制进入 Phase 2.5，引导配置至少一个渠道 | 用户拒绝配置 → 仅 local 输出 |
| 测试推送失败 | 用户回复未收到测试消息 | 排查渠道配置、重发测试 | 更换备选渠道或降级为 local |
| 多渠道部分失败 | 多选渠道中某个失败 | 记录失败渠道，其余渠道继续推送 | 任务不中断；失败渠道下次运行重试 |
| webhook 返回非 2xx | POST 后 HTTP 状态码 ≥ 400 | 记录状态码和响应体，告诉用户检查接收端 | 任务继续；持续失败则自动降级为 local 输出 |
| 用户拒绝测试推送 | 用户表示"不想测试"或"直接创建吧" | 显示风险警告：未验证推送可用性 | 允许创建但标注 `unverified_push` 风险标记 |
| 推送频道空 | 任务未设置 deliver 字段 | 拒绝创建，要求至少指定一个推送渠道 | 用户不选 → 默认 `local` |
| Agent 无 IM 能力 | channel_probe.py 检测到无原生 IM 且未安装 cc-connect | 引导安装 cc-connect | 用户拒绝 → webhook / local |
| 去重后端未配置 | `.env` 中 DEDUP_BACKEND 未设置 | 默认使用 local | 提示用户可选 hindsight / mem0 / agentmemory / lark |
| 用户不满意 IM 消息效果 | 用户确认收到但觉得格式/摘要/噪声不满意 | 按反馈调整模板、query 或过滤规则 | 重新试跑并请求确认；反复不满意 → 切换 delivery_method |
| 重复资料文件 | Phase 0A 中发现文件名含 copy/副本/备份 或内容 MD5 相同 | 标记 duplicate_source，优先使用原始文件 | 无法区分原始与副本 → 展示文件列表让用户指定 |
| 近重复实体名 | entities 中出现简称与全称并存 | 合并为单一实体，保留最长正式名称 | 无法判断同一实体 → 放入 conflicts 让用户确认 |
| 泛行业无实体 | Phase 0/0A 后 entities 为空，仅有行业描述 | 追问用户补充 3-5 个重点实体 | 用户拒绝 → `entity_scope=generic`，cross_queries 主导 |
| lark-cli 未安装 | 用户选择 `delivery_method=doc_link` 但 `which lark-cli` 无结果 | 询问用户是否安装 | 拒绝 → 回退到 `direct` |
| lark-cli 未授权 | `lark-cli auth status` 返回未登录 | 引导用户执行 `lark-cli auth login` | 授权失败 → 回退到 `direct` |
| lark-cli 创建文档失败 | `lark-cli docs +create` 返回非零或无 document_id | 检查授权状态、网络、API 版本，重试一次 | 仍失败 → 回退到 `direct` 或 local 输出 |
| 飞书文档权限设置失败 | `permission.public patch` 返回非零 | 文档已创建，告知用户手动设置 | 接受需登录阅读，或回退到 `direct` 推送全文 |
| doc_link 无配对 IM/Webhook | 用户选择 `delivery_method=doc_link`，但未选交付渠道 | 提示需要至少一个 IM/Webhook 渠道 | 用户不选 → `local` 自行查看文档 |

---

## 约束规则

1. **不改变用户监控目标** — 只优化"怎么抓"和"怎么输出"，不改"监控什么"
2. **不引入用户未要求的交付渠道** — 默认用用户指定的渠道，不私自添加
3. **每轮只改一个维度** — 避免多个变更导致无法归因
4. **保持文件大小合理** — 生成的 prompt/script 不超过原始需求的 150%
5. **可回滚** — 所有任务通过 Agent 原生调度或平台原生机制管理，可查看、暂停、删除
6. **评分独立性** — dry run 结果须展示给用户确认，不能在同一上下文里「改完直接评」
7. **Runtime 中立性** — 本 skill 生成的脚本和 prompt 须能在任何兼容 Agent 运行
8. **路径中立性** — 所有路径使用 `{agent}` 占位符，不在脚本中硬编码任何 Agent 特定路径

---

## 反例与黑名单

本 skill 自身的反模式（不要做的事）：

| # | 反模式 | 为什么不要做 | 正确做法 |
|---|---|---|---|
| 1 | **模糊需求直接创建** | 监控主题/实体/频率未明确时创建任务，运行时输出无关内容、浪费 API 调用 | 必须完成 Phase 0 十项确认，用户确认后才进 Phase 1 |
| 2 | **缺少工具时默认绕过** | 不检查就开始搜索，结果命令报错、空返回、用户体验破坏 | 必须先运行 env_probe.py，缺失工具时主动引导安装 |
| 3 | **跳过 dry run 直接创建** | 搜索矩阵质量未验证，创建后运行结果不达预期，用户失望 | Phase 3 必须手动执行搜索并展示结果，用户确认 OK 才创建 |
| 4 | **在 skill 上下文里自评自改** | 改完 SKILL.md 后直接自己打分，会有「我刚改的肯定更好」乐观偏差 | 评分须由独立子 agent 或用户来做 |
| 5 | **改变用户监控目标** | 将"监控药企管线"改成"监控企业微信公众号"，越界行为 | 只优化"怎么抓"和"怎么输出"，不改"监控什么" |
| 6 | **向用户隐瞒任务执行详情** | 创建后不告诉用户任务名称、schedule、交付渠道，用户无法管理或停用 | 创建后必须展示任务名称、下次执行时间、交付渠道、测试命令 |
| 7 | **未配置推送渠道就创建** | 任务运行后用户收不到结果，以为任务没跑或出了问题 | 必须完成 Phase 2.5 推送渠道配置 + Phase 3 测试推送，用户确认收到才创建 |
| 8 | **测试推送失败后继续创建** | 用户明确表示未收到测试消息，仍然创建，后续每次运行都无效推送 | 测试失败必须排查原因、重发测试或更换渠道，直到通过 |
| 9 | **私自添加用户未选择的渠道** | 用户只选了企业微信，但私自加上 Telegram，干扰用户其他频道 | 严格使用用户确认的渠道清单，不增不减 |
| 10 | **忽视 webhook 格式配置** | 未询问接收端期望的 POST 格式（JSON / form-data / 纯文本），发送后对方解析失败 | 创建前必须确认 webhook 接收端的格式要求和验证方式 |
| 11 | **硬编码 Agent 特定路径** | 脚本中出现 `~/.hermes/skills` 或 `~/.claude` 等路径 | 使用 `{agent}` 占位符或运行时检测 |
| 12 | **假设 Agent 有 Hermes 工具** | 在无 Hermes CLI 的运行时调用 `hermes cronjob create` | 检测 Agent 类型，使用对应的原生机制或 cc-connect |
| 13 | **无视用户资料重新追问** | 用户已给出栏目、信源、名单时仍逐条问十项，浪费上下文并可能覆盖原需求 | 先执行 Phase 0A，只询问 `missing_fields` |
| 14 | **把平台内账号当网页 URL** | 公众号、微博号没有稳定公开 URL，写入 `direct_urls` 后搜索脚本会失败 | 归入 `wechat_sources` / `platform_sources` 并生成平台名 + 关键词 query |
| 15 | **有 Agent 原生调度却写系统 cron** | 用户在 Openclaw/Hermes/Desktop/App 里看不到任务，无法统一管理 | 先用 Agent 原生 scheduled tasks/cron tasks，让任务在管理列表可见 |
| 16 | **CLI 环境未确认方案就注册任务** | launchd/Task Scheduler/systemd 会写入用户系统，属于持久化变更 | 先展示平台方案和命令，等用户同意后再创建 |
| 17 | **注册成功就宣布完成** | 任务可能没跑通，或用户没收到/不喜欢 IM 消息 | 以“试跑成功 + 用户确认收到 + 用户确认满意”为终点 |
| 18 | **强制安装 Agent Reach** | 用户可能只需要英文搜索或不愿安装中文平台工具 | 中文搜索先请求批准；拒绝时使用 Agent 原生 web_search fallback |
| 19 | **doc_link 不验文档权限** | 创建飞书文档后不设公开读，推送链接后接收方需登录飞书才能看，用户体验断裂 | Phase 2.6 步骤 2 必须配置 `permission.public patch` 设 `anyone_readable`，并在 dry run 中验证免登录可访问 |
| 20 | **长报告硬走 direct** | 报告超 IM 消息长度限制被截断，或格式丢失 | 询问用户是否改用 `delivery_method=doc_link`；报告存飞书文档，IM 只推摘要+链接 |

---

## 资源文件速查

| 路径 | 用途 |
|---|---|
| `scripts/env_probe.py` | 工具链 + API key 可用性探测 |
| `scripts/task_runtime_probe.py` | 探测 Agent 原生调度能力并给出平台方案 |
| `scripts/dedup_check.py` | URL 去重检查（多后端支持） |
| `scripts/channel_probe.py` | 检测可用推送渠道（IM + webhook + cc-connect）并引导配置 |
| `scripts/test_push.py` | 测试推送渠道是否可用 |
| `templates/result-card.html` | 任务创建成功后的可视化成果卡片 |
| `references/path-pitfalls.md` | 路径中立性陷阱速查（硬编码路径反例） |

---

## 典型场景模板

### 场景 A：药企管线监控
- 实体：多家药企
- 维度：临床进展、交易动态、监管审批、财报
- 频率：每周一/四 9:00
- 交付：企业微信 / 飞书
- 信源：Brave/Tavily/firecrawl 三选一 + 公司官网 + Agent Reach（若有中文平台）

### 场景 B：技术领域舆情监控
- 实体：技术关键词（如 "LLM reasoning", "agent framework"）
- 维度：论文发表、开源项目更新、融资新闻
- 频率：每日
- 交付：Telegram
- 信源：arXiv + GitHub Trending + Hacker News + Brave/Tavily/firecrawl 三选一

### 场景 C：竞品价格/产品监控
- 实体：竞品官网特定页面
- 维度：页面内容变化（定价、功能列表、发布日志）
- 频率：每小时
- 交付：本地文件 + 邮件
- 信源：firecrawl + diff

### 场景 D：竞品动态周报（文档链接下发方式）
- 实体：国内外竞品公司
- 维度：产品发布 / 临床数据 / 融资合作 / 监管获批 / 学术发表
- 频率：每周一
- 交付渠道：wecom:channel_name
- 下发方式：delivery_method=doc_link
- 输出格式：客观 R&D 简报
- 信源：Brave/Tavily/firecrawl 三选一 + Agent Reach（若有中文平台）
- 链路：搜索 → 去重 → 生成简报 → lark-cli 创建飞书文档（公开读） → 提取摘要 → 指定信道推送「摘要 + 文档链接」

---

## 成果卡片生成

任务创建成功后，可选生成可视化成果卡片：

```bash
open templates/result-card.html  # 方法A：浏览器打开
# 方法B：playwright 截图
python3 -c "from playwright.sync_api import sync_playwright; ...
  page.goto('file://{SKILL_DIR}/templates/result-card.html'); page.screenshot(path='/tmp/{task_name}-card.png')"
```

卡片展示：任务名称、监控实体数、搜索矩阵规模、频率、交付渠道、下发方式、下次执行时间。
