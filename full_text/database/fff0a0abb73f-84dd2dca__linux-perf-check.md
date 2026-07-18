---
name: linux-perf-check
description: |
  SSH远程连接Linux服务器进行全量巡检的技能。支持单机和批量巡检，覆盖系统基础信息、CPU负载、内存&Swap、磁盘空间、网络状态、进程&服务、日志、用户与安全、硬件状态、数据库/中间件、备份&业务、资源阈值告警、Java 宕机分析、MySQL深度诊断（23项）、数据库健康诊断、数据库安全审计、数据库锁分析、数据库备份调度、SQL审核执行，全面支持 MySQL/PostgreSQL/Oracle 三大数据库。

  ⚠️ 安全要求：SSH密钥认证登录，禁止密码登录；仅执行只读命令，禁止修改服务器配置；数据库仅允许SELECT查询，禁止INSERT/UPDATE/DELETE/DROP/ALTER等任何写入操作。

  🚀 性能优化（2026-06-04）：模块级多线程并发执行，默认5线程并发巡检，单机全量巡检从20+分钟压至1-2分钟；阻塞模块自动跳过不卡死。

  新增数据库模块（2026-05-30）：db_health（健康诊断）、db_security（安全审计）、db_locks（锁分析）、db_backup（备份调度）、db_sql（SQL审核执行），均支持 MySQL/PostgreSQL/Oracle 三库。

  使用场景包括但不限于：
  - "帮我巡检XX服务器"
  - "检查192.168.26.66的系统状态"
  - "批量巡检所有服务器"
  - "Linux服务器巡检报告"
  - "服务器负载过高排查"
  - "运维巡检"
  - "一键巡检所有指标"
agent_created: true
---

# Linux 服务器全量巡检技能

## 功能概述

通过SSH远程连接Linux服务器，自动收集系统指标（含数据库深度诊断），生成专业巡检报告。覆盖基础巡检 14 项 + Java 宕机诊断 + 数据库深度诊断（MySQL/PostgreSQL/Oracle 三大库，共 10 个数据库专用模块）。

**支持两种模式：**
- **单机巡检**：指定单台服务器直接巡检
- **批量巡检**：通过 `inventory.json` 服务器清单，并发巡检多台服务器，生成汇总报告

## 巡检覆盖范围（14大类）

| 模块 | 名称 | 核心指标 |
|------|------|----------|
| `system` | 系统基础信息 | 系统版本、内核、主机名、IP/网关/DNS、运行时长、时区、登录用户 |
| `cpu` | CPU负载巡检 | CPU型号/核数、使用率、1/5/15分钟负载、高占用进程 |
| `memory` | 内存&Swap | 物理/缓存/缓冲区、Swap分区、OOM日志 |
| `disk` | 磁盘空间 | 全盘使用率、inode、大文件/日志垃圾、IO繁忙度、只读挂载 |
| `network` | 网络状态 | 网卡流量、监听端口、TCP连接、防火墙、丢包延迟 |
| `process` | 进程&服务 | 业务进程存活、僵尸进程、定时任务、异常进程 |
| `log` | 日志巡检 | 系统日志、安全日志、内核报错、崩溃/OOM |
| `security` | 用户与安全 | 可疑账号、空密码、特权用户、sudo权限、暴力破解、SSH配置 |
| `hardware` | 硬件状态 | CPU温度、硬盘健康、RAID阵列、DMI信息 |
| `middleware` | 数据库/中间件 | MySQL/Redis/Nginx/Tomcat/Docker运行状态、连接数、慢查询 |
| `backup` | 备份&业务 | 备份任务、备份文件、业务端口可用性、SSL证书 |
| `alert` | 资源阈值告警 | CPU>80%、内存>85%、磁盘>85%、Swap>50%、失败登录、僵尸进程 |
| `jvm_crash` | Java 宕机分析 | Java进程检测、JVM crash log、jstack死锁检测、jmap堆对象TOP20、jstat GC统计、OOM记录、应用异常日志 |
| `mysql_deep` | MySQL深度诊断（23项） | 连接使用率、缓冲池命中率、DB/表大小、性能指标、安全审计、索引分析、主从复制、InnoDB引擎状态、慢查询配置、关键参数；**新增**：性能瓶颈诊断、慢查询执行时间分析、未使用索引检测、回表检测、冗余索引检测、缺失索引检测、MySQL参数调优建议 |
| `db_health` | 数据库健康诊断 | MySQL/PostgreSQL/Oracle 健康评分、异常检测、容量预测、瓶颈分析、TOP SQL、趋势分析 |
| `db_security` | 数据库安全审计 | SQL注入检测、敏感数据扫描、权限审计、配置安全、密码策略、登录监控（三库通用） |
| `db_locks` | 数据库锁分析 | 当前锁统计、死锁检测、阻塞链追踪、阻塞事务终止（三库通用） |
| `db_backup` | 数据库备份与调度 | 全量/增量备份(mysqldump/pg_dump/expdp)、Cron定时任务、备份验证 |
| `db_sql` | SQL 审核与执行 | SQL规范审核(5维度)、DDL影响分析、重写优化、Schema查询、数据导出导入 |

## 认证方式

### 方式1：SSH密钥认证（推荐）

```bash
# 生成密钥
ssh-keygen -t ed25519 -C "workbuddy-inspection" -f ~/.ssh/id_ed25519_workbuddy

# 上传公钥
ssh-copy-id -i ~/.ssh/id_ed25519_workbuddy.pub root@<服务器IP>

# 验证
ssh -i ~/.ssh/id_ed25519_workbuddy root@<服务器IP>
```

### 方式2：密码认证

每次巡检时提供：服务器IP、SSH端口、用户名、密码。

## 使用方法

### 单机巡检

```bash
# 全量巡检（密码认证）— 一键跑全部模块，默认5线程并发
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --host <IP> --user root --password <密码> --check all

# 全量巡检（密钥认证）
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --host <IP> --user root --key ~/.ssh/id_ed25519_workbuddy --check all

# 指定模块巡检
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --host <IP> --user root --password <密码> \
  --check cpu,memory,disk,alert

# 调优并发（加快巡检速度）
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --host <IP> --user root --password <密码> --check all \
  --module-workers 8 --module-timeout 60

# 保存报告
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --host <IP> --user root --password <密码> \
  -o /path/to/report.txt --json-output /path/to/report.json
```

### 批量巡检

#### 1. 编辑服务器清单

编辑 `~/.workbuddy/skills/linux-perf-check/inventory.json`，添加需要巡检的服务器：

```json
{
  "servers": [
    {
      "alias": "生产服务器-MySQL",
      "host": "192.168.26.66",
      "port": 22,
      "user": "root",
      "auth": { "type": "password", "value": "redhat" },
      "enabled": true,
      "tags": ["生产", "MySQL"]
    },
    {
      "alias": "测试服务器",
      "host": "192.168.26.100",
      "port": 22,
      "user": "root",
      "auth": { "type": "key", "value": "~/.ssh/id_ed25519_workbuddy" },
      "enabled": true,
      "tags": ["测试"]
    }
  ],
  "settings": {
    "check_modules": "all",
    "timeout": 120,
    "workers": 3,
    "module_workers": 5,
    "module_timeout": null,
    "output_dir": "./reports",
    "generate_html": true
  }
}
```

#### 2. 执行批量巡检

```bash
# 基本批量巡检
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --inventory ~/.workbuddy/skills/linux-perf-check/inventory.json

# 指定并发数 + 生成HTML报告
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --inventory ~/.workbuddy/skills/linux-perf-check/inventory.json \
  --workers 5 --html

# 只巡检关键指标（快速）
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --inventory ~/.workbuddy/skills/linux-perf-check/inventory.json \
  --check cpu,memory,disk,alert

# 指定输出目录
python ~/.workbuddy/skills/linux-perf-check/scripts/linux_inspection.py \
  --inventory ~/.workbuddy/skills/linux-perf-check/inventory.json \
  --output-dir /path/to/reports --html
```

#### inventory.json 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `alias` | 否 | 服务器别名，用于报告中显示 |
| `host` | 是 | IP地址 |
| `port` | 否 | SSH端口，默认22 |
| `user` | 是 | SSH用户名 |
| `auth.type` | 是 | `password` 或 `key` |
| `auth.value` | 是 | 密码字符串 或 密钥文件路径 |
| `enabled` | 否 | 是否启用，默认true |
| `tags` | 否 | 标签数组，用于分类 |

#### settings 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `check_modules` | 否 | 巡检模块，`"all"` 或逗号分隔字符串（如 `"cpu,memory"`） |
| `timeout` | 否 | SSH 命令超时秒数，默认 120 |
| `workers` | 否 | 服务器并发线程数，默认 3 |
| `module_workers` | 否 | **单服务器模块并发线程数**，默认 5（设为 1 回退串行） |
| `module_timeout` | 否 | 单模块超时秒数，默认继承 `timeout` |
| `output_dir` | 否 | 报告输出目录，默认 `./reports` |
| `generate_html` | 否 | 是否生成 HTML 汇总报告，默认 `false` |

#### 批量巡检输出

批量巡检会在输出目录生成以下文件：

```
reports/
├── 192_168_26_66_20260521_134500.txt       # 单台文本报告
├── 192_168_26_66_20260521_134500.json      # 单台JSON报告
├── 192_168_26_100_20260521_134500.txt
├── 192_168_26_100_20260521_134500.json
├── batch_summary_20260521_134500.txt       # 汇总文本报告
└── batch_report_20260521_134500.html       # 汇总HTML报告
```

### --check 模块速查

| 参数值 | 巡检内容 | 需要凭证 |
|--------|----------|:---:|
| **`all`** | **一键全量巡检（展开为下面全部 19 个模块）** | — |
| `system` | 系统基础信息 | SSH |
| `cpu` | CPU负载 | SSH |
| `memory` | 内存&Swap | SSH |
| `disk` | 磁盘空间 | SSH |
| `network` | 网络状态 | SSH |
| `process` | 进程&服务 | SSH |
| `log` | 日志 | SSH |
| `security` | 安全 | SSH |
| `hardware` | 硬件 | SSH |
| `middleware` | 数据库/中间件 | SSH |
| `backup` | 备份&业务 | SSH |
| `alert` | 阈值告警汇总 | SSH |
| `jvm_crash` | Java 宕机分析（jstack/jmap/jstat/crash log） | SSH |
| `mysql_deep` | MySQL/MariaDB深度诊断（23项） | ⚡ DB凭证 |
| `db_health` | 数据库健康诊断（MySQL/PG/Oracle） | ⚡ DB凭证 |
| `db_security` | 数据库安全审计（三库通用） | ⚡ DB凭证 |
| `db_locks` | 数据库锁分析（三库通用） | ⚡ DB凭证 |
| `db_backup` | 数据库备份调度（三库通用） | ⚡ DB凭证 |
| `db_sql` | SQL审核与执行（三库通用） | ⚡ DB凭证 |

- **SSH**：仅需 SSH 凭证即可运行
- **⚡ DB凭证**：需要额外提供数据库连接凭证（`--mysql-user`/`--mysql-password` 或 `inventory.json` 中的 `databases[]`）

多个模块用逗号分隔：`--check cpu,memory,disk,alert,jvm_crash,mysql_deep,db_health,db_security`

### --check all 一键全量巡检 ⭐

**当用户说"巡检"、"全量巡检"、"一键巡检"时，AI 自动使用 `--check all`。**

`all` 自动展开为以下 19 个模块：

```
system,cpu,memory,disk,network,process,log,security,hardware,
middleware,backup,alert,jvm_crash,
mysql_deep,db_health,db_security,db_locks,db_backup,db_sql
```

**凭证处理逻辑：**

| 模块组 | 有 DB 凭证时 | 无 DB 凭证时 |
|--------|:----------:|:----------:|
| 系统巡检 14 项（system~jvm_crash） | ✅ 正常执行 | ✅ 正常执行 |
| 数据库 6 项（mysql_deep~db_sql） | ✅ 正常执行 | ⚠️ 跳过 + 提示"缺少数据库凭证" |

**实际行为：**
- 只要有 SSH 凭证就能跑，「数据库模块没凭证就跳过，不报错」
- 报告末尾会列出跳过的模块及原因，方便后续补齐

**使用示例：**

```bash
# 最简方式：一键全量
python linux_inspection.py --host 192.168.26.66 --user root --password xxx --check all

# 有 DB 凭证时能跑全部 20 个模块
python linux_inspection.py --host 192.168.26.66 --user root --password xxx \
  --check all --mysql-user root --mysql-password dbpwd

# 批量模式：inventory.json 中配置 check_modules: "all"
# 配合 databases[] 字段，自动对列表中的每类数据库执行对应模块
python linux_inspection.py --inventory inventory.json
```

**AI 交互规范：**
- 用户说「巡检」→ 直接 `--check all`
- 用户说「巡检一下数据库」→ `--check mysql_deep,db_health,db_security`
- 用户说「快速巡检」→ `--check cpu,memory,disk,alert`

## Java 宕机分析工作流 ⭐

### 概述

`jvm_crash` 模块是专门针对 Java 应用宕机/异常场景的诊断模块。它通过 SSH 远程在服务器上自动采集 JDK 诊断数据，然后将文本化结果交给 AI 进行深度分析。

### 采集内容

| 诊断维度 | 使用工具 | 采集内容 |
|----------|----------|----------|
| 进程检测 | jps / ps | Java 进程 PID、启动参数、运行时长 |
| Crash 历史 | find | 近 30 天内 hs_err_pid*.log 摘要 |
| 内存分析 | jmap -histo:live | 堆内存对象 TOP 20（按实例数） |
| GC 分析 | jstat -gcutil | 最近 3 次 GC 采样统计 |
| 线程分析 | jstack | 线程状态分布、BLOCKED 线程、死锁检测 |
| 系统 OOM | dmesg / journalctl | 系统级 OOM Killer 记录 |
| 应用日志 | grep | 应用日志中的异常/错误关键词 |

### AI 分析能力（巡检后 AI 自动进行）

AI 在拿到巡检数据后，会自动进行以下分析：

1. **死锁诊断** — 识别 `Found deadlock` 关键字，绘制死锁环路
2. **OOM 根因** — 结合 jmap TOP 对象 + 系统 OOM 记录，定位内存泄漏嫌疑类
3. **线程阻塞** — 统计 BLOCKED 线程数，识别持锁线程和等待链
4. **JVM Crash** — 解析 hs_err_pid*.log 中的信号量(SIGSEGV/SIGBUS)、native 帧、问题帧
5. **GC 异常** — 判断 Full GC 频率是否异常，建议 GC 策略调优
6. **建议输出** — 生成结构化诊断报告 + JVM 参数调优建议 + 代码排查方向

### 使用示例

```bash
# 仅巡检 Java 宕机分析
python linux_inspection.py --host 192.168.26.66 --user root --password xxx --check jvm_crash

# 全量巡检（含 Java 分析）
python linux_inspection.py --host 192.168.26.66 --user root --password xxx --check all

# 关注 CPU/内存 + Java 分析（典型场景：运维报"服务器卡"）
python linux_inspection.py --host 192.168.26.66 --user root --password xxx --check cpu,memory,jvm_crash,alert
```

### Heap Dump 深度分析（额外步骤）

对于需要深入分析内存泄漏的场景，`jvm_crash` 模块提供的是轻量快照（jmap -histo）。如果发现内存异常，可进一步操作：

```bash
# 在服务器上生成 heap dump
jcmd <pid> GC.heap_dump /tmp/heap_$(date +%Y%m%d).hprof

# 转文本摘要后交给 AI 分析
jmap -histo:live <pid> > /tmp/heap_histo.txt
# 或使用 MAT 导出 leak suspects report
```

### 注意事项

- `jmap -histo:live` 会触发 Full GC，生产环境谨慎使用；如需无侵入版本可改用 `jmap -histo`（不含 `:live`）
- `jstack` / `jmap` 需要与目标 JVM 相同版本的 JDK，或目标进程用户权限
- 应用日志扫描默认搜索 `/opt /app /home /data /usr/local /var/log` 下 `*/logs/*.log` 路径

## 告警阈值

| 指标 | 正常 | 告警 | 危险 |
|------|------|------|------|
| CPU使用率 | < 70% | 70%-80% | > 80% |
| 内存使用率 | < 70% | 70%-85% | > 85% |
| 磁盘使用率 | < 70% | 70%-85% | > 85% |
| Swap使用率 | < 30% | 30%-50% | > 50% |
| CPU负载 | < 核数×0.7 | - | > 核数×1.0 |
| 僵尸进程 | 0 | - | > 0 |
| 失败登录 | 0 | > 5次 | > 20次 |
| 数据库连接使用率 | < 60% | 60%-80% | > 80% |
| 缓冲池命中率 | > 95% | 90%-95% | < 90% |
| 主从延迟 | < 10s | 10s-60s | > 60s |
| 慢查询数(日) | < 50 | 50-200 | > 200 |
| 数据库磁盘碎片率 | < 20% | 20%-50% | > 50% |

## 报告格式

巡检完成后生成以下输出：

### 单机模式
1. **终端输出**：结构化的巡检结果
2. **文本报告**（可选 `-o`）：结构化巡检结果
3. **JSON报告**（可选 `--json-output`）：机器可读的结构化数据
4. **告警摘要**：自动提取超阈值项

### 批量模式
1. **单台报告**：每台服务器独立的 txt + json 报告
2. **汇总报告**：`batch_summary_*.txt` 包含所有服务器概览和告警
3. **HTML报告**（`--html`）：暗色主题可视化报告，含跨服务器对比表格

## 报告生成要求

AI执行巡检后，需根据原始数据生成**结构化巡检报告**：

```
# Linux服务器巡检报告

## 基本信息
- 巡检时间: YYYY-MM-DD HH:mm:ss
- 目标主机: IP:PORT
- 操作用户: xxx

## 一、系统基础信息
| 项目 | 值 |
|------|-----|
| 操作系统 | xxx |
| 内核版本 | xxx |
| 主机名 | xxx |
| IP地址 | xxx |
| 运行时长 | xxx |

## 二、CPU负载
[状态: 正常/告警/危险]
| 项目 | 值 | 状态 |
|------|-----|------|
| CPU型号 | xxx | - |
| 物理核心 | xx核 | - |
| CPU使用率 | xx% | 正常/告警 |
| 负载(1/5/15) | x.xx/x.xx/x.xx | 正常/告警 |

## 告警汇总
| 级别 | 模块 | 问题描述 | 建议 |
|------|------|----------|------|
| 告警 | 磁盘 | /data 使用率92% | 清理日志或扩容 |
```

## 前置条件

```bash
pip install paramiko
```

## 巡检流程（AI执行）

### 单机巡检
1. 确认用户提供的：服务器IP、端口、用户名、密码/密钥
2. 先用`--check system`快速验证连通性
3. 连通后执行 `--check all` 全量巡检（或用户指定模块）
4. 数据库模块缺凭证时自动跳过，报告末尾标注跳过原因
5. 解析原始输出，生成结构化巡检报告
6. 高亮告警项，给出处理建议
7. 保存报告文件，交付给用户

### 批量巡检
1. 用户说"批量巡检"或提供多台服务器信息时，引导用户提供服务器清单
2. 编辑 `inventory.json` 写入服务器信息
3. 执行 `--inventory` + `--html` 批量巡检
4. 生成汇总HTML报告，展示跨服务器对比
5. 高亮有告警的服务器，给出处理建议
6. 交付HTML报告文件

## MySQL深度诊断模块 🔍

`mysql_deep` 模块通过 SSH 连接到服务器后，再通过 TCP 连接 MySQL/MariaDB 数据库进行深度诊断。密码使用 `MYSQL_PWD` 环境变量传递，不会出现在进程列表中。

### 检测维度（14小节）

| 小节 | 内容 | 说明 |
|------|------|------|
| 14.1 | 基础状态 | 版本、运行时间、当前连接数、max_connections |
| 14.2 | 连接使用率 | Threads_connected / max_connections 百分比 |
| 14.3 | 内存配置 | innodb_buffer_pool_size、key_buffer_size 等关键内存参数 |
| 14.4 | 缓冲池命中率 | InnoDB Buffer Pool 读命中率（应 > 95%） |
| 14.5 | 数据库大小 TOP10 | 按 data_length + index_length 排序，单位 GB |
| 14.6 | 大表 TOP10 | 单表排行（GB），优先 information_schema，超时回退 innodb_table_stats（InnoDB） |
| 14.7 | 性能指标 | Slow_queries、QPS相关、InnoDB锁等待、临时表 |

### 大表查询实测示例（vms66 / 2026-05-29）

> 当 `information_schema.tables` 超时（>30s）时，14.6 自动回退到 `mysql.innodb_table_stats`，秒级返回结果。

**14.6 大表 TOP10（innodb_table_stats 回退结果）：**

| 库 | 表 | 大小_GB | 估算行数 | 引擎 |
|------|------|---------|----------|------|
| ekp | sys_xform_template_history | 0.077 | 241 | InnoDB |
| ekp_gelan | sys_xform_template_history | 0.024 | 71 | InnoDB |
| ekp_gelan | sys_xform_template | 0.024 | 109 | InnoDB |
| ekp | sys_xform_template | 0.024 | 65 | InnoDB |
| ekpv13 | sys_xform_template | 0.022 | 165 | InnoDB |
| ekpv13 | sys_xform_template_history | 0.018 | 110 | InnoDB |
| ekp | sys_read_log | 0.014 | 22166 | InnoDB |
| ekp | sys_print_template_history | 0.009 | 31 | InnoDB |
| mkpaas | design_element | 0.008 | 1881 | InnoDB |
| ekp | lbpm_node_definition | 0.006 | 4020 | InnoDB |

> 说明：该服务器 MySQL 的 `information_schema` 查询极慢（历史慢查询 TOP1 耗时 15603 秒），14.5 和 14.6 均触发超时回退。回退仅覆盖 InnoDB 表，MyISAM/其他引擎表未包含。
| 14.8 | 慢查询配置 | slow_query_log 状态、long_query_time 阈值 |
| 14.9 | 安全审计 | 匿名用户、空密码、远程 root、test 数据库 |
| 14.10 | 索引分析 | 无主键表检测 |
| 14.11 | 主从复制 | SHOW SLAVE STATUS 关键字段 |
| 14.12 | 关键配置参数 | max_allowed_packet、binlog、事务隔离级别等 |
| 14.13 | InnoDB引擎状态 | BUFFER POOL、死锁、ROW OPERATIONS 摘要 |
| 14.14 | 当前连接详情 | PROCESSLIST，按运行时间倒序 TOP20 |

### 自动告警规则

| 告警 | 触发条件 | 级别 |
|------|----------|------|
| 连接使用率过高 | usage_pct > 80% | 🔴 mid |
| 缓冲池命中率偏低 | hit_ratio < 95% | 🟡 low |
| 存在大量慢查询 | slow_query_count > 100 | 🟡 low |
| 匿名用户存在 | mysql.user 有空 User | 🔴 mid |
| 空密码用户 | authentication_string 为空 | 🔴 mid |
| root 远程登录 | User='root' AND Host='%' | 🟡 low |
| 无主键表 | 业务库中有表缺主键 | 🟡 low |
| 主从延迟严重 | Seconds_Behind_Master > 60 | 🔴 mid |
| 连接失败 | ERROR 1045/2003 | 🔴 mid |

### 使用方式

**单机模式：**
```bash
# 检查本地 MySQL
python linux_inspection.py --host 192.168.26.66 --user root --password redhat \
  --check mysql_deep --mysql-user app --mysql-password dbpwd

# 检查远程 MySQL
python linux_inspection.py --host 192.168.26.66 --user root --password redhat \
  --check mysql_deep --mysql-host 192.168.1.100 --mysql-port 3307 \
  --mysql-user dba --mysql-password secret
```

**批量模式（inventory.json）：**
```json
{
  "servers": [{
    "host": "192.168.26.66",
    "alias": "DB服务器",
    "auth": {"type": "password", "value": "redhat"},
    "db_auth": {
      "_comment": "数据库连接凭证：IP、端口、账号、密码",
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "password": "mysql_root_pwd"
    }
  }],
  "settings": {
    "check_modules": ["mysql_deep", "system", "cpu", "memory", "disk"],
    "generate_html": true
  }
}
```

**`db_auth` 字段说明（必填项）：**

| 字段 | 必填 | 说明 |
|------|------|------|
| `type` | 否 | 数据库类型：`mysql`(默认) / `postgresql` / `oracle` |
| `host` | 是 | 数据库 IP 地址（本机填 `127.0.0.1`） |
| `port` | 否 | 数据库端口（MySQL默认3306、PG默认5432、Oracle默认1521） |
| `user` | 是 | 数据库账号 |
| `password` | 是 | 数据库密码 |
| `database` | 否 | 默认数据库名（PG/Oracle 建议填写） |

**多数据库配置示例（inventory.json）：**
```json
{
  "servers": [{
    "host": "192.168.26.66",
    "alias": "混合数据库服务器",
    "auth": {"type": "password", "value": "redhat"},
    "databases": [
      {"type": "mysql", "host": "127.0.0.1", "port": 3306, "user": "root", "password": "mysql_pwd"},
      {"type": "postgresql", "host": "127.0.0.1", "port": 5432, "user": "postgres", "password": "pg_pwd", "database": "ekp"},
      {"type": "oracle", "host": "192.168.1.50", "port": 1521, "user": "scott", "password": "oracle_pwd", "database": "ORCL"}
    ]
  }],
  "settings": {
    "check_modules": ["mysql_deep", "db_health", "db_security", "system", "cpu", "memory"],
    "generate_html": true
  }
}
```

数据库凭证优先级：**服务器级 `databases[]` > 服务器级 `db_auth` > 全局 `settings.db_auth` > CLI 默认值**

### 注意事项

- 需要服务器上有 `mysql` CLI 客户端（通常 `yum install -y mysql`）
- 兼容 MySQL 5.7/8.0 和 MariaDB 10.x
- `performance_schema` 不可用时自动降级，显示提示信息
- `slow_log` 表不存在时自动跳过
- 密码通过 `MYSQL_PWD` 环境变量传递，不暴露在进程列表中
- 连接失败时模块会标记为异常，但不影响其他巡检模块

---

## 数据库健康诊断 (db_health) 🩺

### 概述

`db_health` 模块是数据库维度的"体检中心"，支持 **MySQL / PostgreSQL / Oracle** 三种数据库。通过 SSH 连接到服务器后，使用对应的 CLI 客户端（mysql / psql / sqlplus）直连数据库执行只读诊断 SQL。复用 `inventory.json` 中的 `db_auth` 字段配置数据库连接凭证。

### 核心诊断维度

| 维度 | 检查内容 | 适用数据库 |
|------|---------|-----------|
| 健康评分 | 版本、运行时间、总大小、QPS/TPS | 三库通用 |
| 连接状态 | 总连接数、活跃连接、空闲连接、最大查询时长 | 三库通用 |
| 缓冲池/缓存 | InnoDB Buffer Pool 命中率 / PostgreSQL shared_buffers / Oracle Buffer Cache | 三库通用 |
| 异常检测 | 锁等待数、慢查询数、长时间运行查询(>30s) | 三库通用 |
| 容量预测 | 各库大小、TOP 20 大表、磁盘碎片、自增ID使用率 | 三库通用 |
| 瓶颈分析 | 自动识别 CPU/IO/锁/连接/慢查询 五大瓶颈方向 | 三库通用 |

### 关键诊断 SQL

**PostgreSQL - 健康评分：**
```sql
SELECT version(), EXTRACT(EPOCH FROM NOW() - pg_postmaster_start_time()) AS uptime_sec,
  pg_database_size(current_database()) / 1073741824.0 AS size_gb;
SELECT COUNT(*) AS total, COUNT(*) FILTER (WHERE state='active') AS active,
  COUNT(*) FILTER (WHERE state='idle') AS idle FROM pg_stat_activity;
SELECT ROUND(100.0 * SUM(blks_hit) / GREATEST(SUM(blks_hit + blks_read), 1), 2) AS cache_hit_pct
  FROM pg_stat_database WHERE datname = current_database();
```

**Oracle - 健康评分：**
```sql
SELECT banner AS version, (SYSDATE - STARTUP_TIME) * 86400 AS uptime_sec FROM v$version, v$instance WHERE banner LIKE 'Oracle%';
SELECT COUNT(*) AS total, COUNT(CASE WHEN status='ACTIVE' THEN 1 END) AS active FROM v$session;
SELECT ROUND(100 * (1 - SUM(value) / (SELECT SUM(value) FROM v$sysstat WHERE name='consistent gets')), 2) AS buffer_hit_pct
  FROM v$sysstat WHERE name = 'physical reads';
```

**MySQL - 瓶颈分析（五大方向一键检测）：**
```sql
-- CPU: 活跃连接 vs 总连接
SELECT VARIABLE_VALUE FROM performance_schema.global_status WHERE VARIABLE_NAME='Threads_running';
-- IO: 缓冲池命中率
SELECT ROUND((1 - Innodb_buffer_pool_reads / Innodb_buffer_pool_read_requests) * 100, 2) 
  FROM (SELECT SUM(VARIABLE_VALUE) FROM performance_schema.global_status WHERE VARIABLE_NAME IN ('Innodb_buffer_pool_reads','Innodb_buffer_pool_read_requests')) t;
-- 锁: 当前行锁等待
SELECT SUM(VARIABLE_VALUE) FROM performance_schema.global_status WHERE VARIABLE_NAME='Innodb_row_lock_current_waits';
-- 连接: 连接使用率
SELECT ROUND(SUM(CASE WHEN VARIABLE_NAME='Threads_connected' THEN VARIABLE_VALUE END) * 100.0 / 
  (SELECT VARIABLE_VALUE FROM performance_schema.global_variables WHERE VARIABLE_NAME='max_connections'), 2) AS conn_pct
  FROM performance_schema.global_status WHERE VARIABLE_NAME IN ('Threads_connected');
-- 慢查询: 最近1小时慢查询
SELECT COUNT(*) FROM mysql.slow_log WHERE start_time > DATE_SUB(NOW(), INTERVAL 1 HOUR);
```

### AI 决策流程

```
场景1：用户说"数据库健康检查"
  → 依次执行健康评分、连接状态、缓冲池命中率 SQL
  → 汇总输出：版本、运行时间、连接数、命中率、QPS、总大小
  → 给出健康评分（0-100）和评级（优秀/良好/需关注）

场景2：用户说"数据库容量够吗"
  → 执行各库大小 SQL + TOP 20 大表
  → 检查磁盘碎片和自增ID使用率
  → 基于当前增长趋势估算剩余天数
  → 输出：当前总容量 / 预测剩余天数 / TOP N 大表 / 扩容建议

场景3：用户说"数据库瓶颈在哪"
  → 执行五大方向瓶颈检测 SQL
  → CPU高 → 追 TOP SQL；IO高 → 查缓冲池；锁多 → 追踪阻塞链
  → 输出：瓶颈方向 + 根因 + 解决建议
```

### 使用方式

```bash
# 巡检 PostgreSQL
python linux_inspection.py --host 192.168.26.66 --user root --password xxx \
  --check db_health --pg-user app --pg-password dbpwd --pg-db mydb

# 巡检 Oracle（使用 inventory.json 中的 db_auth）
python linux_inspection.py --inventory inventory.json --check db_health

# 组合巡检：系统 + 数据库健康
python linux_inspection.py --host 192.168.26.66 --user root --password xxx \
  --check system,cpu,memory,disk,db_health --mysql-user root --mysql-password xxx
```

---

## 数据库安全审计 (db_security) 🔒

### 概述

`db_security` 模块对数据库进行全方位安全审计，支持 **MySQL / PostgreSQL / Oracle**，覆盖 7 个检查维度，输出安全评分（A/B/C/D/F）。

### 审计维度与评分权重

| 维度 | 权重 | 检查项 |
|------|:---:|--------|
| 权限审计 | 25% | 超级用户、GRANT 权限、任意主机访问、数据库级权限 |
| 配置安全 | 20% | 关键安全参数、日志启用、加密配置 |
| 密码策略 | 15% | 密码复杂度策略、过期策略、弱密码 |
| 敏感数据 | 15% | 密码/身份证/手机号/邮箱/银行卡等敏感列扫描 |
| 登录安全 | 10% | 匿名用户、空密码、失败登录记录 |
| SQL注入 | 10% | 参数化查询检查、动态SQL风险 |
| 高危操作 | 5% | DROP/TRUNCATE/DELETE无WHERE/GRANT ALL 审计 |

### 关键诊断 SQL

**MySQL - 综合安全审计：**
```sql
-- 匿名用户/空密码/任意主机
SELECT user, host FROM mysql.user WHERE user = '' OR authentication_string = '';
SELECT user, host FROM mysql.user WHERE host = '%';

-- 用户权限列表
SELECT user, host, Select_priv, Insert_priv, Update_priv, Delete_priv,
  Create_priv, Drop_priv, Grant_priv, Super_priv FROM mysql.user;

-- 关键安全配置
SHOW VARIABLES WHERE Variable_name IN (
  'local_infile', 'secure_file_priv', 'log_bin', 'general_log',
  'sql_mode', 'default_authentication_plugin', 'validate_password.policy');
```

**PostgreSQL - 权限审计：**
```sql
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin, rolvaliduntil FROM pg_roles;
SELECT grantee, table_schema, table_name, privilege_type 
  FROM information_schema.table_privileges WHERE table_schema NOT IN ('pg_catalog','information_schema');
-- pg_hba.conf 检查（需读文件）: grep -v '^#' /var/lib/pgsql/*/data/pg_hba.conf | grep -E 'trust|0.0.0.0'
```

**敏感数据扫描（三库通用逻辑）：**
```sql
-- MySQL 示例：扫描包含敏感信息的列
SELECT table_schema, table_name, column_name,
  CASE WHEN column_name LIKE '%pass%' OR column_name LIKE '%pwd%' THEN '密码'
       WHEN column_name LIKE '%phone%' OR column_name LIKE '%mobile%' THEN '手机号'
       WHEN column_name LIKE '%email%' OR column_name LIKE '%mail%' THEN '邮箱'
       WHEN column_name LIKE '%id_card%' THEN '身份证'
  END AS sensitive_type
FROM information_schema.COLUMNS
WHERE table_schema NOT IN ('mysql','sys','performance_schema','information_schema')
  AND (column_name REGEXP 'pass|pwd|phone|mobile|email|mail|id_card|bank|card_no|salary')
ORDER BY table_schema, table_name;
```

### 安全评分标准

| 评分 | 评级 | 状态 | 处理建议 |
|------|:---:|------|---------|
| 90-100 | A | 安全配置完善 | 保持 |
| 80-89 | B | 少量中低风险项 | 择期修复 |
| 70-79 | C | 存在中风险项 | 尽快修复 |
| 60-69 | D | 存在高风险项 | 优先修复 |
| <60 | F | 严重安全隐患 | **立即修复** |

---

## 数据库锁分析 (db_locks) 🔍

### 概述

`db_locks` 模块专门处理数据库锁相关故障，支持 **MySQL / PostgreSQL / Oracle** 的锁分析、死锁检测、阻塞链追踪。

### 核心诊断 SQL

**MySQL - 锁统计概览：**
```sql
SELECT COUNT(*) AS total_trx,
  SUM(CASE WHEN trx_state='LOCK WAIT' THEN 1 ELSE 0 END) AS lock_waiting,
  MAX(TIMESTAMPDIFF(SECOND, trx_started, NOW())) AS max_trx_age_sec
FROM information_schema.INNODB_TRX;
```

**MySQL - 阻塞链追踪（完整版）：**
```sql
-- MySQL 8.0+ 使用 sys.innodb_lock_waits
SELECT waiting_pid, waiting_query, blocking_pid, blocking_query,
  wait_age_secs, locked_table, locked_index, locked_type
FROM sys.innodb_lock_waits;

-- MySQL 5.7 兼容版
SELECT r.trx_mysql_thread_id AS waiting_thread,
  TIMESTAMPDIFF(SECOND, r.trx_started, NOW()) AS wait_sec,
  LEFT(r.trx_query, 100) AS waiting_query,
  b.trx_mysql_thread_id AS blocking_thread,
  LEFT(b.trx_query, 100) AS blocking_query
FROM information_schema.INNODB_LOCK_WAITS w
JOIN information_schema.INNODB_TRX r ON w.requesting_trx_id = r.trx_id
JOIN information_schema.INNODB_TRX b ON w.blocking_trx_id = b.trx_id;
```

**PostgreSQL - 锁等待：**
```sql
SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query,
  blocking.pid AS blocking_pid, blocking.query AS blocking_query,
  blocked.wait_event_type, blocked.wait_event
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking ON blocked.wait_event_type='Lock' AND blocking.pid != blocked.pid;
```

**Oracle - 锁等待：**
```sql
SELECT blocking_session, sid, serial#, wait_class, seconds_in_wait, sql_id
FROM v$session WHERE blocking_session IS NOT NULL;
```

### AI 决策流程

```
场景1：用户说"看看数据库锁情况"
  → 执行锁统计 SQL → 如果有waiting事务 → 追踪阻塞链
  → 输出：总锁数 / 等待数 / 最老事务 / 阻塞源

场景2：用户说"有死锁吗"
  → 执行 SHOW ENGINE INNODB STATUS（MySQL）/ 查 PG 日志
  → 解析死锁信息：时间、涉及SQL、循环等待关系
  → 给出避免死锁建议（统一加锁顺序 / 缩短事务）

场景3：用户说"有阻塞，帮我看看"
  → 构建阻塞链图：A→B→C
  → 找到阻塞源 + 分析阻塞SQL + 事务时长
  → 建议：终止阻塞源 / 等待 / 优化SQL
```

### 锁类型速查

| 锁类型 | 说明 | 常见场景 |
|--------|------|---------|
| TABLE | 锁定整张表 | ALTER TABLE / MyISAM 写操作 |
| ROW | 锁定特定行 | InnoDB UPDATE/DELETE/SELECT...FOR UPDATE |
| METADATA | 锁定表结构 | DDL 操作 / 长事务持有 |
| GAP | 锁定索引间隙 | REPEATABLE READ 范围查询 |
| NEXT-KEY | 行锁+间隙锁 | InnoDB 默认行级锁 |

⚠️ **终止阻塞事务（KILL）需用户明确确认后执行。**

---

## 数据库备份与调度 (db_backup) 💾

### 概述

`db_backup` 模块提供数据库备份、定时任务管理、备份验证能力，支持 **MySQL(mysqldump) / PostgreSQL(pg_dump) / Oracle(expdp)**。

### 备份命令速查

**MySQL - mysqldump：**
```bash
# 全量备份（InnoDB 不锁表）
mysqldump -h<host> -P<port> -u<user> -p<pass> \
  --single-transaction --routines --triggers --events \
  --databases <db> | gzip > backup_<db>_$(date +%Y%m%d_%H%M%S).sql.gz

# 仅结构
mysqldump -h<host> -P<port> -u<user> -p<pass> --no-data <db> | gzip > schema.sql.gz

# 指定表
mysqldump -h<host> -P<port> -u<user> -p<pass> --single-transaction <db> t1 t2 | gzip > tables.sql.gz
```

**PostgreSQL - pg_dump：**
```bash
PGPASSWORD=<pass> pg_dump -h <host> -p <port> -U <user> -Fc \
  -f backup_<db>_$(date +%Y%m%d_%H%M%S).dump <db>
PGPASSWORD=<pass> pg_dump -h <host> -p <port> -U <user> --schema-only -f schema.sql <db>
```

**Oracle - expdp：**
```bash
expdp <user>/<pass>@<service> DIRECTORY=DATA_PUMP_DIR \
  DUMPFILE=backup_$(date +%Y%m%d).dmp FULL=Y
expdp <user>/<pass>@<service> DIRECTORY=DATA_PUMP_DIR \
  DUMPFILE=schema_$(date +%Y%m%d).dmp SCHEMAS=<schema>
```

### 定时备份 Cron 管理

```bash
# 每天凌晨2点全量备份
0 2 * * * /opt/scripts/db_backup.sh >> /var/log/db_backup.log 2>&1

# 每6小时增量备份
0 */6 * * * /opt/scripts/db_backup.sh --incremental

# 每周日全量 + 每月1号归档
0 0 * * 0 /opt/scripts/db_backup.sh --full
0 3 1 * * /opt/scripts/db_archive.sh
```

### 备份验证

```bash
# MySQL: 检查备份文件大小和 SQL 行数
gzip -l backup_*.sql.gz && zcat backup_*.sql.gz | wc -l

# PostgreSQL: 验证 dump 文件
pg_restore -l backup_*.dump | head -20

# 最近24小时是否有新备份
find /backup/ -name "*.sql.gz" -mmin -1440 | wc -l
```

### 最佳实践提醒
1. 备份前检查磁盘空间（剩余 > 预估大小 × 2）
2. MySQL InnoDB 务必使用 `--single-transaction`
3. 备份后验证文件完整性
4. 异地备份（上传远程存储）
5. 保留策略：7天日备 + 4周周备 + 12月月备

---

## SQL 审核与执行 (db_sql) 📋

### 概述

`db_sql` 模块整合 SQL 审核与执行两大能力，支持 **MySQL / PostgreSQL / Oracle**。

### 功能矩阵

| 功能 | 说明 | 典型用法 |
|------|------|---------|
| **SQL 规范审核** | 5维度(语法/性能/安全/风格/DDL)审核，输出评分和问题清单 | 「审核这个SQL」 |
| **DDL 影响分析** | 分析表大小、锁表风险、预估执行时间、回滚方案 | 「这个ALTER有什么影响」 |
| **SQL 重写优化** | 展开 SELECT *、优化条件、子查询转JOIN、游标分页 | 「优化这个SQL」 |
| **索引推荐** | 基于 EXPLAIN 分析，推荐单列/联合/覆盖索引 | 「加什么索引」 |
| **Schema 查询** | 表结构、字段详情、索引、建表语句 | 「查看表结构」 |
| **数据导出** | CSV/JSON/SQL 多格式导出 | 「导出users表为CSV」 |
| **数据导入** | CSV/SQL 文件导入 | 「导入这个CSV」 |

### SQL 审核维度与关键规则

**性能规范（高风险项）：**
| 规则 | 严重度 | 说明 |
|------|:---:|------|
| WHERE 条件字段无索引 | 🔴 高 | type=ALL 全表扫描 |
| 隐式类型转换 | 🔴 高 | WHERE varchar_col = 123 |
| `%` 开头的 LIKE | 🔴 高 | LIKE '%xxx' 不走索引 |
| 函数作用于索引列 | 🔴 高 | WHERE DATE(col) = '2024-01-01' |
| JOIN 字段类型不一致 | 🔴 高 | 跨类型 JOIN 性能灾难 |
| SELECT ... FOR UPDATE 范围过大 | 🔴 高 | 大量锁等待 |

**安全规范（严重项）：**
| 规则 | 严重度 | 说明 |
|------|:---:|------|
| 字符串拼接 SQL | 🔴 严重 | 必须参数化查询 |
| DELETE/UPDATE 无 WHERE | 🔴 严重 | 全表误删风险 |
| DROP TABLE/DATABASE | 🔴 严重 | 必须走变更流程 |

### SQL 重写优化示例

```
优化前：SELECT * FROM orders WHERE DATE(created_at) = '2024-01-01'
优化后：SELECT id, user_id, amount FROM orders
        WHERE created_at >= '2024-01-01 00:00:00' AND created_at < '2024-01-02'

优化前：SELECT * FROM t WHERE id NOT IN (SELECT uid FROM blacklist)
优化后：SELECT t.* FROM t LEFT JOIN blacklist b ON t.id = b.uid WHERE b.uid IS NULL

优化前：SELECT * FROM t ORDER BY id LIMIT 100000, 20
优化后：SELECT * FROM t WHERE id > 12345 ORDER BY id LIMIT 20
```

### 使用方式

```bash
# SQL 审核 + 优化建议（AI 直接分析，无需额外参数）
python linux_inspection.py --host 192.168.26.66 --user root --password xxx \
  --check db_sql --sql "SELECT * FROM users WHERE name LIKE '%test%'"

# Schema 查询
python linux_inspection.py --host 192.168.26.66 --user root --password xxx \
  --check db_sql --schema-table users --mysql-user root --mysql-password xxx
```

### AI 决策流程

```
场景1：用户说"审核这个SQL"
  → 5维度审核：语法→性能→安全→风格→DDL
  → 执行 EXPLAIN 分析执行计划
  → 输出评分 + 问题清单 + 修复建议

场景2：用户说"这个DDL有什么风险"
  → 查询表大小和行数
  → 判断数据库版本（INSTANT DDL支持）
  → 评估：锁表风险 / 执行时间 / 复制延迟 / 回滚方案

场景3：用户说"优化这个SQL"
  → EXPLAIN 分析 → 应用优化规则
  → 输出优化后SQL + 对照说明 + 性能预估改善
```

### 安全控制

| 操作等级 | 示例 | 处理方式 |
|:---:|------|---------|
| 🔴 严重 | DROP DATABASE/TABLE | **默认禁止**，必须用户明确确认 |
| 🟠 高 | DELETE/UPDATE 无 WHERE, TRUNCATE | 警告 + 确认，建议加 LIMIT |
| 🟡 中 | DELETE/UPDATE 带 WHERE, ALTER DROP | 提醒影响范围 |
| 🟢 安全 | SELECT, SHOW, DESCRIBE, EXPLAIN | 正常执行，默认 LIMIT 100 |

---

## 注意事项

- 硬件巡检（`hardware`）部分命令需要root权限，非root用户会部分失败
- 中间件巡检（`middleware`）仅检查已安装的服务，未安装的服务会自动跳过
- 密码等敏感信息不要记录在报告中
- 大文件查找（`disk`模块）可能耗时较长，可单独执行
- 外网连通性测试受网络环境影响，结果仅供参考
- 批量巡检时单台失败不影响其他服务器，最终汇总报告会标注失败原因
- `inventory.json` 包含密码等敏感信息，不要提交到版本控制系统

---

## 性能优化记录

### 2026-06-03 性能优化

**问题**：全量巡检（`--check all`）耗时 20+ 分钟，主要瓶颈：

1. **`find /` 全盘扫描** — `disk` 模块的 `find / -xdev -type f -size +100M` 和 `jvm_crash` 模块的 `find / -name "hs_err_pid*.log"` 扫描整个根文件系统，在有大量文件的服务器上可能耗时数分钟
2. **`ssh_db` 逐条查询** — 5 个数据库模块（db_health/db_security/db_locks/db_backup/db_sql）共 ~23 条 SQL 通过独立 SSH 通道逐条执行，每次都要建立 SSH 通道对应网络往返
3. **`jstat` 过度采样** — 每个 Java 进程执行 3 次 `jstat`（间隔 1s），多进程累计等待时间长
4. **日志扫描无超时** — `jvm_crash` 的日志扫描没有 `maxdepth` 和 `timeout` 限制

**优化措施**：

| 优化项 | 修改前 | 修改后 | 预估节省 |
|--------|--------|--------|:---:|
| disk 大文件查找 | `find / -xdev`（全盘） | 限定 `/var /opt /data /home /tmp` + `maxdepth 6` + `timeout 20s` | ~3-5min |
| jvm_crash 崩溃日志 | 两次 `find / -prune /proc /sys`（全盘） | 单次 `timeout 30 find` + 限定常驻目录 `maxdepth 5` | ~2-3min |
| jstat GC 采样 | 每进程 3 次采样（3s） | 每进程 1 次快照（1s） | ~2s/进程 |
| 应用日志扫描 | 无 maxdepth 无 timeout | `maxdepth 5` + `timeout 30s` + `timeout 10s` grep | ~1-2min |
| iostat | `iostat -x 1 2`（2s 等待） | `iostat -x 1 1`（1s） | 1s |
| ssh_db 查询 | 逐条 SSH exec_command（~23 次通道） | 合并为单个 shell 脚本单次调用 | ~1-3min |
| mysql 连接 | 无 connect-timeout | `--connect-timeout=10` | 快速失败 |
| **总计** | **20+ 分钟** | **预计 3-6 分钟** | **70-85%** |

**备份**：修改前已备份至 `linux-perf-check-backup-20260603-195000`

### 2026-06-04 模块并发优化

**问题**：单机巡检 19 个模块串行执行，每个模块依次等待前一个完成，即使模块之间互不依赖也在排队，总耗时 = 各模块耗时之和。

**优化措施**：

| 优化项 | 修改前 | 修改后 | 预估节省 |
|--------|--------|--------|:---:|
| 模块执行方式 | `for` 循环串行逐一执行 | `ThreadPoolExecutor` 多线程并发（默认5线程） | **60-75%** |
| SSH 连接 | 所有模块复用 1 个 SSH 客户端 | 每线程独立 SSH 连接（线程安全） | 避免竞争 |
| 模块超时 | 全局统一超时 | 每个模块独立 `future.result(timeout)` | 单模块卡死不拖累全局 |
| 阻塞模块处理 | 阻塞导致整个巡检挂起 | 超时后自动跳过，标记 `[跳过]` | 不卡死 |
| 串行回退 | — | `--module-workers 1` 回退到串行模式 | 向后兼容 |

**核心架构变化**：

```python
# 新增 _exec_single_module() 函数：每个模块在独立线程中执行，创建独立SSH连接
# run_inspection() 重构：
#   1. 先做一次 SSH 连通性验证
#   2. 将 19 个模块提交到 ThreadPoolExecutor（默认5线程）
#   3. as_completed 收集结果，每个 future 独立超时
#   4. 按原始顺序排列报告段落
```

**新增 CLI 参数**：
- `--module-workers N`：单服务器模块并发线程数，默认 5，设为 1 回退串行
- `--module-timeout N`：单模块超时秒数，默认继承 `--timeout`

**新增 inventory.json 配置项**：
```json
"settings": {
    "module_workers": 5,
    "module_timeout": null
}
```

**合并效果（两次优化叠加）**：
| 阶段 | 预估耗时 |
|------|:---:|
| 原始版本 | 20+ min |
| 6/3 优化后 | 3-6 min |
| 6/4 模块并发后 | **1-2 min** |
| **累计提升** | **90%+** |

**备份**：修改前已备份至 `linux_inspection.py.bak.20260604_*`
