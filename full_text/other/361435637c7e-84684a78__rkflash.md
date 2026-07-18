---
name: rkflash
description: "Rockchip OH 镜像技能：同步须配置 rkflash_sync_config.json 或 RKFLASH_* 环境变量（无内置主机/密码）；pscp/scp/paramiko 同步；config.cfg 驱动烧录；默认版本校验与 VERIFY OK 后关灯。见 SKILL.md。"
author: "Created by user"
created: "2026-03-25"
version: "1.5.0"
---

# rkflash 技能

本文档与 **`rkflash.py`** 实现一一对应：同步多种方式、**`images/images/` 摊平**、**`config.cfg` 驱动的烧录流程**（典型 **18** 步）、**默认版本校验**、**校验通过后关灯**、**模块常量**与**退出码**。

在 **Windows**（或已配置 OpenSSH/`sshpass` 的 Linux）下，将 **`images/`** 中分区镜像按 **`images/config.cfg`** 解析出的顺序与 **`di` 参数**烧录到 **Rockchip** 开发板（**无**代码内写死的 **`REQUIRED_IMAGES`** 列表）。**同步与版本校验**所依赖的 **SSH 主机、用户、密码、远端镜像路径**等**不设仓库默认值**，须通过 **CLI / 环境变量 / `<base>/rkflash_sync_config.json`** 配置；在交互终端下可对缺项**逐条提示输入**，非 TTY 则**报错退出**并说明如何配置。**烧录日志**：**`log/rkflash_<时间>.log`**（UTF-8，步骤标题**英文**）；**expect-scp 调试日志**：**`log/rkflash_sync_expect_<时间>.log`**。**与 `rkflash.py` 顶部模块 docstring、`--help` 描述一致**（子命令、**`config.cfg`** 解析、**烧录完成判定**、**`--no-verify-version` / `--no-leds-off`**）。

## 应用示例与提示词

在 **napi_generator 仓库根** 下进入 **`src/skills/rkflash`**（或带 `--base` 指向该目录）。须先配置 **`rkflash_sync_config.json`**（从 **`rkflash_sync_config.example.json`** 复制，**勿提交真实密码**）。

| 场景 | 命令示例 | 提示词示例 |
|------|----------|------------|
| 查看布局 | `python3 src/skills/rkflash/rkflash.py analyze-config` | 「解析当前 images 下 config.cfg 的烧录顺序」 |
| PuTTY 同步 | `python3 src/skills/rkflash/rkflash.py pscp-sync` | 「用 pscp 从编译机同步镜像到本机再准备烧录」 |
| 一键烧录 | `python3 src/skills/rkflash/rkflash.py flash_all` | 「同步完成后执行 flash_all 烧录 RK 板」 |
| 跳过版本校验 | `python3 src/skills/rkflash/rkflash.py flash_all --no-verify-version` | 「先烧录不做 ohos.para 版本比对」 |
| 不关灯 | `python3 src/skills/rkflash/rkflash.py flash_all --no-leds-off` | 「烧录通过后不要 hdc 关灯」 |
| 帮助 | `python3 src/skills/rkflash/rkflash.py --help` | 「rkflash 有哪些子命令和参数」 |

---

## 功能简介（与 `rkflash.py` 对齐）

| 类别 | 行为概要 |
|------|----------|
| **同步** | **`pscp-sync`**（PuTTY **`pscp -pw -r`**）、**`raw-scp`**（**`shell=True`** 跑 **`scp`**）、**`sync-images`**（sshpass / paramiko / **pexpect scp**）→ 目标均为 **`<base>/images/`** |
| **摊平** | 仅 **`pscp-sync`**、**`raw-scp`** 在 **exit 0** 后调用 **`_flatten_nested_images_subdir`**；**`sync-images` 不摊平** |
| **布局** | **`images/config.cfg`** 必选；**`load_flash_layout_from_config`** 得 **`ul`** 与各 **`di`**；**`analyze-config`** 打印人读结果 |
| **烧录** | **`flash_all`**：**`hdc shell reboot loader`**（内置等待 **15s**）+ **`upgrade_tool.exe`** 多步 **`td`/`rcb`/`ul`/`di`/`rd`** |
| **验收** | 默认 **`verify_flashed_version_against_server`**：延时 → **`hdc shell param get`** → 拉 **`ohos.para`** 比对 **`SOFTWARE_VERSION_PARAM`** |
| **关灯** | **VERIFY OK** 且未 **`--no-leds-off`**：**`hdc shell sh -c`**（**`rkflash_sync_config.json`** 的 **`leds_off_cmd` / `leds_off_names`** 或 **`RKFLASH_LEDS_NAMES`**，否则默认 **blue,green,red**）；**失败不导致 exit 1** |
| **输出** | 终端 **`print`/`RuntimeError`**：**英文 ASCII**；**`log/*.log`**：**UTF-8** |

---

## 能力总览（与 `rkflash.py` 一致）

| 能力 | 说明 |
|------|------|
| **`pscp-sync`** | PuTTY **`pscp -batch -pw -r`**，`cwd=<base>/images`，拉远端目录到 **`.`**；成功后可摊平 **`images/images/`** |
| **`raw-scp`** | **`shell=True`** 执行 **`--cmd` / `RKFLASH_RAW_SCP_CMD` / `raw_scp_cmd`**（JSON），交互密码；成功后可摊平 |
| **`sync-images`** | **sshpass+scp** / **paramiko SFTP 递归** / **`--expect-scp`（pexpect）**；**不**做 `images/images/` 摊平（远端用 **`remote/.`** 或 SFTP 扁平拉取） |
| **烧录** | **`hdc shell reboot loader`** + **`upgrade_tool`**；**`ul`/`di` 参数**由 **`images/config.cfg`** 解析（典型 18 步，见下） |
| **版本校验** | 默认开启：设备 **`hdc shell param get`** 解析 **`const.product.software.version`**，与服务器 **`ohos.para`** 同键比对；**`--no-verify-version`** 仅调试用，**不能**作为「烧录完成」依据 |
| **关灯（校验通过后）** | **`VERIFY OK`** 之后 **`hdc shell sh -c`** 执行脚本（尽力而为，失败**不**影响 **exit 0**）；优先级：**`leds_off_cmd`**（整段 sh）> **`RKFLASH_LEDS_NAMES`** / **`leds_off_names`** > 默认 **blue,green,red**；**`--no-leds-off`** 关闭此步 |
| **终端文案** | 脚本 **`print` / `--help` / `RuntimeError`** 为**英文 ASCII**；外部工具输出原样 |

---

## 脚本输出语言

- **`rkflash.py` 自身**的 `print`、**`--help`**、报错 **`RuntimeError`** 为**英文（ASCII）**，减轻 Windows 控制台 **GBK** 乱码。
- **`upgrade_tool.exe` / `hdc` / `pscp`** 等输出仍为工具原样（可能含中文）。
- **`log/*.log`** 为 **UTF-8**。

---

## 子命令与退出码

| 命令 | 作用 | 典型退出码 |
|------|------|------------|
| **`python rkflash.py`** | **烧录**（**`config.cfg`**）+ 默认**版本校验** + **VERIFY OK 后关灯**（除非 **`--no-leds-off`**） | **0** = 烧录与版本比对**均**成功（关灯失败仍可能 **0**）；**1** = 烧录或校验失败。**`--no-verify-version`** 时**跳过**校验与关灯，**不**作量产完成依据 |
| **`python rkflash.py pscp-sync`** | **PuTTY pscp** 非交互同步 | **0** 成功；**1** 失败；**124** **`--timeout` 超时** |
| **`python rkflash.py raw-scp`** | 手工同款 **`scp`** | 与 **`scp` 进程**一致 |
| **`python rkflash.py sync-images`** | **scp / SFTP / expect-scp** | **0** 成功；**1** 失败 |
| **`python rkflash.py analyze-config`** | 解析二进制 **`images/config.cfg`**：**`ul`** 用 **`.bin` 基名**，各分区 **`di <flag> <basename>`**（cfg 内标签 → **`upgrade_tool`** 参数，如 **`resource` → `-resource`**） | **0**；缺失或解析失败为 **1** |

子命令通过 **`argv[1]`** 识别：`sync-images`、`raw-scp`、`pscp-sync`、**`analyze-config`**；**无子命令**时进入烧录模式（`argparse` 解析 **`--base`**、**`--hdc-timeout` / `--step-timeout` / `--long-timeout`**、**`--no-verify-version` / `--no-leds-off`**、**`--verify-*` / `--remote-ohos-para`** 等）。**`analyze-config`** 见下文专节。

**路径**：在仓库内一般为 **`src/skills/rkflash/rkflash.py`**；工作目录可为任意，用 **`--base`** 指向技能根（含 **`bin/`**、**`images/`**）。

---

独立 **关灯技能**见同仓库 **`src/skills/ohleds/`**（**`ohleds.py`**）：仅通过 **`hdc`** 关 sysfs 灯；可与 rkflash 共用 **`RKFLASH_LEDS_NAMES`**；**`ohhdc`** 亦提供 **`led … on|off`** 细粒度控制。

---

## 必填配置（同步 / 版本校验 / `raw-scp`）

1. **配置文件（推荐）**：将 **`rkflash_sync_config.example.json`** 复制为技能根下的 **`rkflash_sync_config.json`**（与 **`rkflash.py`** 同目录，或通过 **`--base`** 指向的根），填写 **`sync_host`**、**`sync_user`**、**`sync_remote`**；密码建议用环境变量 **`RKFLASH_SSH_PASSWORD`**，或写入 JSON 的 **`sync_password`**（**勿提交含真实密码的 JSON 到公开仓库**；仓库 **`.gitignore`** 已忽略该文件名）。
2. **环境变量**：**`RKFLASH_SYNC_HOST`**、**`RKFLASH_SYNC_USER`**、**`RKFLASH_SSH_PASSWORD`**、**`RKFLASH_SYNC_REMOTE`**（远端 **phone images** 目录的绝对路径）。可选：**`RKFLASH_REMOTE_OHOS_PARA`**（未设且 **`sync_remote`** 以 **`/images`** 结尾时，脚本会推导 **`.../system/etc/param/ohos.para`**）、**`RKFLASH_SYNC_PORT`**、**`RKFLASH_RAW_SCP_CMD`**（**`raw-scp`** 整行 shell 命令）。
3. **CLI**：各子命令的 **`--host` / `--user` / `--password` / `--remote`**（及主命令的 **`--verify-*` / `--remote-ohos-para`**）覆盖文件与环境。
4. **交互终端**：缺项时脚本可 **`input` / `getpass`** 补全；**无 TTY** 时直接 **`RuntimeError`** 并打印上述配置说明。

**`analyze-config`** 与 **`--no-verify-version`** 的纯烧录路径**不**要求 SSH 配置；**`pscp-sync` / `sync-images` / `raw-scp`** 及默认带版本校验的主命令**必须**能解析出完整连接信息。

---

## 环境变量一览

| 变量 | 用途 |
|------|------|
| **`RKFLASH_SYNC_HOST`** | SSH 主机（同步与拉取 **`ohos.para`**；可被 CLI **`--host` / `--verify-host`** 覆盖） |
| **`RKFLASH_SYNC_USER`** | SSH 用户名 |
| **`RKFLASH_SSH_PASSWORD`** | SSH 密码（同步与 **`ohos.para`**；可被 **`--password` / `--verify-password`** 或 JSON **`sync_password`** 覆盖） |
| **`RKFLASH_SYNC_REMOTE`** | 远端 **images** 目录绝对路径（**`pscp-sync` / `sync-images`**；用于推导 **`ohos.para`** 路径） |
| **`RKFLASH_SYNC_PORT`** | SSH 端口（默认 **22**） |
| **`RKFLASH_REMOTE_OHOS_PARA`** | 远端 **`ohos.para`** 绝对路径（可选；未设时按 **`sync_remote`** 推导） |
| **`RKFLASH_RAW_SCP_CMD`** | **`raw-scp`** 默认 shell 命令行（可被 **`--cmd`** 或 JSON **`raw_scp_cmd`** 覆盖） |
| **`RKFLASH_PSCP`** | **`pscp.exe`** 路径（**`pscp-sync`**、**版本校验拉单文件**优先使用） |
| **`RKFLASH_SSHPASS`** | **`sshpass`** 可执行文件路径 |
| **`RKFLASH_SCP`** | **`--expect-scp`** 时优先使用的 **`scp.exe`**（建议系统 OpenSSH） |
| **`RKFLASH_EXPECT_PHASE1_TIMEOUT`** | expect-scp **首阶段**等待秒数（默认 **300**） |
| **`leds_off_cmd`**（`rkflash_sync_config.json`） | **`VERIFY OK`** 后 **`hdc shell sh -c`** 的**整段** shell（**优先级最高**；空字符串则忽略） |
| **`RKFLASH_LEDS_NAMES`** | 逗号分隔 sysfs 名；**优先于** JSON **`leds_off_names`**（当未使用 **`leds_off_cmd`** 时） |
| **`leds_off_names`**（`rkflash_sync_config.json`） | 同 **`RKFLASH_LEDS_NAMES`**；未设环境变量时从 JSON 读 |
| （以上均无） | 默认关灯：**blue、green、red** 三个节点（与此前写死命名一致）；需全盘 sysfs 时可于 JSON 设 **`leds_off_cmd`** 为自定义循环脚本 |

---

## 外部工具与依赖

以下为 **`rkflash.py` 实际子进程调用或强依赖**的组件（**非** Python 标准库）。未列出的逻辑在脚本内用 **Python** 完成（如解析 **`param get`** 文本、摊平目录）。

### 可执行文件 / 宿主程序

| 工具 | 来源 / 典型形态 | 脚本中的用途 | 说明 |
|------|-----------------|--------------|------|
| **`pscp.exe`** | [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/) 套件 | **`pscp-sync`** 整目录 **`pscp -batch -pw -r`**；**版本校验**时 **`pscp` 单文件**拉取远端 **`ohos.para`** 到临时文件 | Windows 常见路径 **`C:\PuTTY\pscp.exe`**；路径由 **`--pscp` / `RKFLASH_PSCP` / PATH** 解析；拉 **`ohos.para` 失败时**可改走 **paramiko**（见下） |
| **`scp`（及底层 `ssh`）** | **OpenSSH 客户端**（Windows「可选功能」、Linux 发行版包）或 **Git for Windows** 自带的 MSYS **`scp`** | **`raw-scp`**：整行在 **`shell=True`** 下执行（**`--cmd` / `RKFLASH_RAW_SCP_CMD` / `raw_scp_cmd`**）；**`sync-images`** 在 **sshpass+scp** 或 **`--expect-scp`** 分支中启动 **`scp`** | **`--expect-scp`** 建议 **`RKFLASH_SCP`** 指向 **`%SystemRoot%\System32\OpenSSH\scp.exe`**，避免 Git MSYS 版在无 TTY 下不出密码提示 |
| **`sshpass`** | Linux 常见包（如 `apt install sshpass`） | **`sync-images`** 走 **`sshpass -p … scp -r …`** 时作为子进程 argv[0] | **Windows 通常没有**；该路径下多用 **`pscp-sync`**、**`--expect-scp`** 或 **paramiko** |
| **`hdc`** | **OpenHarmony / HarmonyOS Device Connector**（SDK 或独立工具，需在 **PATH**） | **`hdc shell reboot loader`**；**`hdc shell param get`**（烧录后版本校验）；**`VERIFY OK`** 后 **`hdc shell sh -c`** 关灯（默认 sysfs） | 烧录、校验、关灯均依赖本机可执行 **`hdc`** |
| **`upgrade_tool.exe`** | **Rockchip** 官方烧录工具（Windows **`exe`**） | **`flash_all`** 中 **`td` / `rcb` / `ul` / `di` / `rd`** 等子命令 | 必须放在技能根 **`bin/upgrade_tool.exe`**（与 **`rkflash.py`** 中 **`_ensure_dirs`** 一致） |
| **系统 Shell** | Windows 下多为 **`cmd.exe`**（由 **`subprocess` + `shell=True`** 使用） | 仅 **`raw-scp`**：执行用户配置的 **`scp`** 命令行 | 需本机已能手工运行同一条 **`scp`** |

### Python 第三方库（`pip`）

| 包 | 用途 | 何时需要 |
|----|------|----------|
| **`paramiko`** | **SFTP** 递归下载（**`sync-images`** 无 **sshpass** 或 **`--no-prefer-scp`** 等）；**`ohos.para`** 在 **`pscp` 不可用或失败**时回退读取 | **`pip install -r src/skills/rkflash/requirements-sync.txt`** |
| **`pexpect`** | **`sync-images --expect-scp`**：驱动 **`scp`** 子进程并自动应答密码/主机指纹 | 同上；**仅**在启用 **`--expect-scp`** 时导入 |

### 与功能对照简表

| 功能 | 主要外部工具 |
|------|----------------|
| **`pscp-sync`** | **`pscp`** |
| **`raw-scp`** | **Shell + `scp`（+ `ssh`）** |
| **`sync-images`（sshpass 路径）** | **`sshpass` + `scp`** |
| **`sync-images`（paramiko）** | 无 CLI（**paramiko**） |
| **`sync-images`（expect-scp）** | **`scp`（+ `ssh`）** + **pexpect** |
| **烧录** | **`hdc`** + **`bin/upgrade_tool.exe`** |
| **版本校验** | **`hdc`**；**`pscp`** 或 **paramiko** 二选一拉 **`ohos.para`** |
| **关灯（校验后）** | **`hdc`** |

---

## 模块常量（`rkflash.py`，与代码一致）

| 名称 | 含义 |
|------|------|
| **`CONFIG_JSON_NAME`** | **`rkflash_sync_config.json`**（位于 **`--base`** 技能根；与 **`rkflash_sync_config.example.json`** 同结构） |
| **`RkflashSshConfig`** | **`_resolve_rkflash_ssh_config()`** 的解析结果：**`host` / `port` / `user` / `password` / `remote_images` / `remote_ohos_para`** |
| **`DEFAULT_PSCP_SYNC_TIMEOUT_SEC`** | **1800**（**`pscp-sync`** 整次子进程超时，超则 **124**） |
| **`DEFAULT_PSCP_EXE`** | `C:\PuTTY\pscp.exe`（**仅**在文件存在时作为 **`pscp`** 候选路径，非凭据） |
| **`SOFTWARE_VERSION_PARAM`** | **`const.product.software.version`**（设备 param 与 **`ohos.para`** 解析键） |
| **`images/config.cfg`** | **必选**：二进制 Rockchip 配置；脚本解析 **UTF-16-LE** 分区标签与镜像路径，得到 **`CfgFlashLayout`**（**`load_flash_layout_from_config`**）：**`loader_basename`**、**`partitions`**（**`di_flag` + `image_basename`**）。烧录前检查与 **`di`/`ul` 参数**均来自此文件 |
| **默认关灯** | 未配置 **`leds_off_cmd`** 且无命名列表时：对 **blue / green / red** 的 **`brightness`** 写 **0**；全盘 sysfs 循环见代码内 **`_DEFAULT_LEDS_OFF_SH`**（供 **`leds_off_cmd`** 或扩展使用） |

---

## `config.cfg` 与烧录布局（与 `rkflash.py` 一致）

- **格式**：Rockchip 二进制 **`CFG`** 头；内嵌 **UTF-16-LE** 字符串（分区标签 + 带 **`\\`** 的 Windows 风格路径）。
- **解析入口**：**`load_flash_layout_from_config(cfg_path)`**、**`parse_rockchip_config_cfg_flash_layout(data)`**。
- **`CfgFlashLayout`**：**`loader_basename`**（文件中**首个** **`.bin`** 路径的基名，用于 **`ul`**）；**`partitions`**：每项 **`CfgFlashPartition(cfg_label, di_flag, image_basename)`**，按各 **`.img`** 在文件中**首次出现**的顺序排列（重复路径只保留首次）。
- **标签 → `di` 参数**：**`Uboot`**（大小写不敏感）→ **`-u`**；其余 → **`-` + 标签小写**（如 **`resource` → `-resource`**，**`sys-prod` → `-sys-prod`**，**`Boot_linux` → `-boot_linux`**）。
- **自检命令**：**`python rkflash.py analyze-config`**（可选 **`--config`**，默认 **`<base>/images/config.cfg`**）。
- **辅助**：**`parse_rockchip_config_cfg_burn_files(data)`** 仅返回 **`.img`** 基名列表与 **loader** **`.bin`** 基名，供只需文件名的调用方使用。

---

## 推荐流程（同步 → 烧录 → 版本校验）

先完成 **[必填配置](#必填配置同步--版本校验--raw-scp)**（**`rkflash_sync_config.json`** 或环境变量）。**`sync_remote`** 应指向编译产物树下的 **phone `images`** 目录（绝对路径）；若未单独设置 **`remote_ohos_para`** 且路径以 **`/images`** 结尾，脚本会将 **`ohos.para`** 推导为同级 **`system/etc/param/ohos.para`**。若 **`sync_remote`** 不以 **`/images`** 结尾或布局不同，请显式设置 **`RKFLASH_REMOTE_OHOS_PARA`**（或 JSON **`remote_ohos_para`** / **`--remote-ohos-para`**）。

### 烧录完成判定（与脚本退出码一致）

**只有**同时满足下面两点，才视为本次烧录流程**完成**且结果可信：

1. **`upgrade_tool` 全流程**（含末尾 **`rd`**）执行成功，日志 **`log/rkflash_*.log`** 中步骤正常结束。
2. **版本校验通过**（默认开启）：设备 **`const.product.software.version`** 与服务器 **`ohos.para`** 同键一致。

**`python rkflash.py` 进程 exit 0** 表示上述默认路径（含校验）**全部成功**；**exit 1** 表示烧录或校验任一失败。运行烧录时须**等待进程结束**并查看退出码与日志，不能视为「命令发出即完成」。**`--no-verify-version`** 仅用于调试（例如无网、无 `hdc`），**不**用于确认量产/发布烧录完成。

**校验通过后的关灯**：在 **VERIFY OK** 之后，脚本会**尽力**通过 **`hdc`** 执行关灯（配置见 **`rkflash_sync_config.json`** 的 **`leds_off_cmd` / `leds_off_names`**，否则默认 **blue,green,red**）。关灯失败或板子无对应节点时**仍**可为 **exit 0**；不需要关灯时用 **`--no-leds-off`**，特殊板型在 JSON 中设置 **`leds_off_cmd`** 为整段 **`sh`**。

```bash
# 仓库根目录；Windows 可将 python3 换成 python
# 须已配置 SSH（见 rkflash_sync_config.json 或环境变量），例如：
#   set RKFLASH_SYNC_HOST=...
#   set RKFLASH_SYNC_USER=root
#   set RKFLASH_SSH_PASSWORD=...
#   set RKFLASH_SYNC_REMOTE=/path/to/.../packages/phone/images
python3 src/skills/rkflash/rkflash.py pscp-sync
# 标准烧录 + 默认版本校验 + VERIFY OK 后关灯；须等到进程 exit 0（同样需要 SSH 配置以拉 ohos.para）
python3 src/skills/rkflash/rkflash.py
# 仅调试：跳过校验与关灯，不表示烧录结果已确认
# python3 src/skills/rkflash/rkflash.py --no-verify-version
# 校验通过但不执行关灯
# python3 src/skills/rkflash/rkflash.py --no-leds-off
# 指定技能根（当 cwd 不是 rkflash 目录时）
# python3 src/skills/rkflash/rkflash.py --base D:/path/to/rkflash
```

---

## 同步方式怎么选

| 方式 | 适用场景 |
|------|----------|
| **`pscp-sync`** | **Windows**，**PuTTY**，**`-pw` 非交互**，适合脚本 |
| **`raw-scp`** | 与终端手工 **`scp`** 完全一致，需交互密码 |
| **`sync-images`** | **Linux sshpass**、**paramiko**、**`--expect-scp`**；默认远端镜像目录需用 **`--remote`** 指定（按你的编译机实际路径填写） |

---

## `pscp-sync`（PuTTY）

- **解析顺序**：**`--pscp`** > **`RKFLASH_PSCP`** > Windows 下 **`C:\PuTTY\pscp.exe`** > **`PATH`** 中 **`pscp`**。
- **等价命令**（在 **`<base>/images`**）：  
  **`pscp -batch -pw <pwd> -r -P <port> <user>@<host>:<remote> .`**
- **超时**：**`subprocess` 整次超时**；默认 **1800 s**；超时 **退出码 124**。
- **成功且退出码 0**：调用 **`_flatten_nested_images_subdir`**，可能打印 **`[pscp-sync] flattened nested images/images/ into images/ (if present)`**。

| 参数 | 默认 |
|------|------|
| `--base` | `rkflash.py` 所在目录 |
| `--pscp` | 见上 |
| `--host` / `--user` / `--password` / `--remote` | **无**；来自 **[必填配置](#必填配置同步--版本校验--raw-scp)** 或 CLI |
| `-P` / `--port` | **22**（或由 **`RKFLASH_SYNC_PORT` / `sync_port`**） |
| `--timeout` | **1800**（秒） |

**`images/images/`**：远端目录名为 **`images`** 且 **`cwd`** 为本地 **`images/`** 时易出现内层 **`images/`**；**仅在同步成功（0）后摊平**。

---

## `raw-scp`

- **`cwd=<base>/images`**，命令行来自 **`--cmd` / `RKFLASH_RAW_SCP_CMD` / JSON `raw_scp_cmd`**；缺省且非 TTY 则报错。
- **成功（0）后摊平**内层 **`images/images/`**，英文提示 **`[raw-scp] flattened ...`**。
- 启动时打印 **`[raw-scp] cwd=...`**、**`[raw-scp] cmd=...`**。

| 参数 | 默认 |
|------|------|
| `--base` | 脚本目录 |
| `--cmd` | **无**；须配置 **`RKFLASH_RAW_SCP_CMD`** 或 **`raw_scp_cmd`**（或交互输入） |

---

## `sync-images`

### 完整参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `--base` | 脚本目录 | 技能根；同步目标 **`<base>/images`** |
| `--host` / `--user` / `--password` / `--remote` | **无** | **[必填配置](#必填配置同步--版本校验--raw-scp)** 或 CLI |
| `-P` / `--port` | **22** 或 **`RKFLASH_SYNC_PORT`** | |
| `--no-prefer-scp` | 关 | 打开则**不**用 sshpass+scp，**强制 paramiko** |
| `--sshpass` | 无 | 或 **`RKFLASH_SSHPASS`** |
| `--scp-only` | 关 | **仅** sshpass+scp；无 sshpass 则报错 |
| `--expect-scp` | 关 | **pexpect** 驱动态 **`scp`**；与 **`--scp-only`** 同时设时 **expect 优先** |
| `--transfer-timeout` | **86400** | expect-scp **传输阶段**超时（秒） |

### 传输策略优先级（与 `sync_images_from_server` 一致）

1. **`--expect-scp`** → **`_sync_images_pexpect_scp`**（不依赖 sshpass）。
2. 否则若 **`--scp-only`** → 必须有 **sshpass**，**`_sync_images_scp_cli`**；否则报错。
3. 否则若 **默认 prefer scp** 且找到 **sshpass** → **`_sync_images_scp_cli`**。
4. 否则 → **`_sync_images_paramiko`**（**paramiko** SFTP 递归）。

**expect-scp**：首阶段**不**匹配 **`Permission denied`**，避免误匹配；建议 **`RKFLASH_SCP`** 指向 **OpenSSH `scp.exe`**。

**依赖**：**`pip install -r src/skills/rkflash/requirements-sync.txt`**（**paramiko**、**pexpect**）。

**成功**：**`Synced <user>@<host>:<remote> -> <base>/images`**（英文）。

---

## `analyze-config`

解析 **`config.cfg`**（须为 Rockchip 二进制，文件头 **`CFG`** + **`\\0`**），输出 **Loader（`ul`）** 与各分区 **cfg 标签 → `di` 标志 → 镜像基名**。用于自检烧录前 **`images/`** 应与配置一致。

| 参数 | 默认 | 说明 |
|------|------|------|
| `--base` | **`rkflash.py` 所在目录** | 技能根 |
| `--config` | **`<base>/images/config.cfg`** | 任意路径的 **`config.cfg`** |

- **退出码**：**0** 解析并打印成功；**1** 文件不存在、非 **`CFG`** 头或解析 **`RuntimeError`**（ stderr 英文）。
- **不**检查 **`images/`** 下文件是否真实存在（仅 **`flash_all`** 前 **`_check_images_layout`** 检查）。

---

## 烧录与版本校验（主命令，无子命令）

### 版本校验（默认开启）

- **`Flash finished, log: ...`** 之后：等待 **`--verify-delay`（默认 60s）**，再 **`hdc shell param get`**，脚本内正则取 **`SOFTWARE_VERSION_PARAM`**（**不依赖本机 `grep`**）。
- 拉 **`--remote-ohos-para`**：**先 `pscp` 单文件到系统临时文件**（可能向终端打进度行），失败则用 **paramiko SFTP** 读远端文件。
- 结果追加到**同一烧录日志**：**`Post-flash version check`**、**`VERIFY OK`** / **`VERIFY FAIL`**；成功时 **`Version verify OK: ...`**。
- **`VERIFY OK`** 后（除非 **`--no-leds-off`**）：日志 **`Turn off all LEDs`**，执行 **`hdc shell sh -c`**（见 **`leds_off_cmd` / 命名列表 / 默认 blue,green,red**）；成功时终端 **`All LEDs off (best-effort).`**，失败仅警告**不**改退出码。

| 参数 | 默认 | 说明 |
|------|------|------|
| `--no-verify-version` | 关 | 指定则跳过校验（**仅调试**） |
| `--no-leds-off` | 关 | 指定则校验通过后**不**关灯 |
| `--verify-host` / `--verify-user` / `--verify-password` | **无** | 与同步相同配置源；CLI 可单独覆盖 |
| `--verify-port` | **22** | 或 **`RKFLASH_SYNC_PORT` / `sync_port`** |
| `--remote-ohos-para` | **无** | **`RKFLASH_REMOTE_OHOS_PARA`**、JSON、或由 **`sync_remote`** 推导 |
| `--verify-delay` | **60** | 秒 |
| `--verify-hdc-timeout` | **120** | 秒 |
| `--verify-pscp-timeout` | **120** | 秒 |
| `--base` | 脚本目录 | 技能根 |
| `--hdc-timeout` | **120** | **`hdc shell reboot loader`** |
| `--step-timeout` | **600** | **`td` / `rcb` / `rd`** 等 |
| `--long-timeout` | **7200** | **`ul`、各 `di` 下载** |

**说明**：**`--verify-hdc-timeout`** 同时用于 **`hdc shell param get`** 与 **VERIFY OK** 后关灯脚本的 **`hdc shell sh -c`**（同一秒数，与 **`rkflash.py --help`** 一致）。

---

## 目录约定（技能根 `rkflash/`）

| 路径 | 说明 |
|------|------|
| **`bin/upgrade_tool.exe`** | 必须存在 |
| **`images/`** | 镜像目录；必备文件见下 |
| **`log/`** | 自动创建 |

### `images/` 烧录必备（由 **`config.cfg`** 决定）

除 **`config.cfg`** 本体外，必备 **`ul`/`di` 涉及的文件**以该配置为准。执行 **`python rkflash.py analyze-config`** 可列出当前解析结果（**Loader** 与各 **`di` 行**）。

典型 phone 包与当前默认 **`config.cfg`** 一致时，仍为 **`MiniLoaderAll.bin`** 与 **`uboot.img`** … **`userdata.img`** 等 12 个 **`.img`**；更换 **`config.cfg`** 后列表与 **`di` 子命令参数**会随之变化。

---

## 烧录流程（日志英文标题；**`ul`/`di` 来自 `config.cfg`**）

1. **`hdc shell reboot loader`** → 等待 **15s**（**`Waiting for device in loader (15s)...`**）
2. **`td`** — `2. Test device (td)`
3. **`rcb`** — `3. Get flashinfo (rcb)`（**仅退出码 0**，不要求输出 **`ok`**）
4. **`ul <loader.bin> -noreset`** — 基名由 **`config.cfg`** 中首个 **`.bin`** 路径决定（常见 **`MiniLoaderAll.bin`**）
5. **`td`** — `5. Test device (td)`
6–7. **`di -u <uboot.img>`**（两次；**`-u`** 与 **`uboot.img`** 均由 **`config.cfg`** 解析）
8… **`di <flag> <basename>`** — 每个非 **uboot** 分区一行，**`<flag>`**（如 **`-resource`**）与 **`<basename>`**（如 **`resource.img`**）均来自 **`config.cfg`**
最后一步 **`rd`** — **`reset device (rd)`**（步号随分区数量递增）

典型 **`config.cfg`** 下仍为 **18 个 `upgrade_tool` 相关步骤**（含两次 **`di -u`**）。

除 **rcb** 外，**退出码 0** 且输出含 **`ok`**（不区分大小写）。结束：**`All steps finished: <ISO>`**。

---

## 可编程 API（Python 同模块内调用）

| 符号 | 作用 |
|------|------|
| **`CfgFlashLayout`** / **`CfgFlashPartition`** | **`config.cfg`** 解析结果（**`loader_basename`**、分区 **`di_flag`** 与 **`image_basename`**） |
| **`sync_images_from_server(base, host=..., password=..., remote_dir=..., ...)`** | 同步到 **`base/images`**（**`host`/`user`/`password`/`remote_dir`** 须由调用方提供，无模块级默认） |
| **`_resolve_rkflash_ssh_config(...)`** | 从 CLI/环境/JSON/TTY 解析 **`RkflashSshConfig`** |
| **`flash_all(base, hdc_timeout, step_timeout, long_timeout)`** | 烧录，返回 **`log` 文件 `Path`**（读 **`images/config.cfg`**） |
| **`load_flash_layout_from_config(cfg_path)`** / **`parse_rockchip_config_cfg_flash_layout(data)`** | 解析烧录布局：**`ul`** 与各 **`di`** 参数 |
| **`parse_rockchip_config_cfg_burn_files(data)`** | **`(img_basenames, [loader_bin])`**，无 **`di_flag`** |
| **`verify_flashed_version_against_server(..., leds_off=True)`** | 追加写日志；一致则 return（**`leds_off`** 时接着 **`hdc`** 关灯），否则 **`RuntimeError`**；**`hdc_timeout`** 同时作用于 **`param get`** 与关灯 |
| **`_hdc_turn_off_all_leds_after_verify(log_path, hdc_timeout)`** | **VERIFY OK** 后关灯（**不**抛异常）；通常由 **`verify_flashed_version_against_server`** 调用 |
| **`_skill_base(explicit)`** | 解析技能根目录 |
| **`_flatten_nested_images_subdir(images_dir)`** | 摊平 **`images/images/`** |

---

## 脚本入口（CLI 映射）

| CLI | 函数 |
|-----|------|
| 烧录（无子命令） | **`main()`** → **`flash_all`** + 默认 **`verify_flashed_version_against_server`** |
| **`sync-images`** | **`cmd_sync_images`** → **`sync_images_from_server`** |
| **`raw-scp`** | **`cmd_raw_scp`** |
| **`pscp-sync`** | **`cmd_pscp_sync`** |
| **`analyze-config`** | **`cmd_analyze_config`** → **`load_flash_layout_from_config`**，打印布局 |

---

## 提示词与执行要点（给 Cursor / AI 助手）

以下示例可直接复制为对话提示；执行烧录类任务时**必须**遵守「等进程结束 + 默认校验」约定。

### 推荐提示词（中文）

1. **只做同步（Windows + PuTTY）**  
   「在仓库里用 **`rkflash` 技能**：先让用户配置 **`rkflash_sync_config.json`**（或 **`RKFLASH_SYNC_*` / `RKFLASH_SSH_PASSWORD`**），再进入 **`src/skills/rkflash`** 执行 **`python rkflash.py pscp-sync`**，**等待命令跑完**，确认 **exit 0** 且如有 **`flattened nested images/images/`** 提示。不要中途把长时间同步当失败。」

2. **同步 + 完整烧录验收**  
   「用 **`src/skills/rkflash/rkflash.py`**：确保 **SSH 同步配置**已就绪；先 **`python rkflash.py pscp-sync`** 等 **exit 0**；再 **`python rkflash.py`**（**不要**加 **`--no-verify-version`**），**必须等待整个进程结束**。成功标准：**exit 0**，终端出现 **`Version verify OK`**，日志 **`log/rkflash_*.log`** 含 **`VERIFY OK`**；若出现 **`All LEDs off (best-effort).`** 表示关灯已尝试。」

3. **检查 config 与镜像列表**  
   「在技能根执行 **`python rkflash.py analyze-config`**，把输出的 **Loader** 和 **`di` 行**列出来，确认与 **`images/`** 下文件一致。」

4. **调试烧录但不做版本验收**  
   「仅调试：**`python rkflash.py --no-verify-version`**。说明：这**不能**作为量产烧录完成依据。」

5. **验收但不想关灯**  
   「烧录后要做版本校验但**不要** sysfs 关灯：**`python rkflash.py --no-leds-off`**。」

6. **板子关灯命令特殊**  
   「烧录验收通过后关灯要用自定义脚本：在 **`rkflash_sync_config.json`** 里设置 **`leds_off_cmd`** 为整段 **`sh`**，再跑 **`python rkflash.py`**。」

### 助手必须遵守

- **同步 / 默认版本校验**前须具备 **`rkflash_sync_config.json`** 或等价环境变量；**禁止**假设仓库内写死服务器地址或密码。
- **禁止**在 **`python rkflash.py`**（默认参数）未结束时就报告「烧录完成」。
- **量产 / 发布**结论仅当 **exit 0** 且**未**使用 **`--no-verify-version`**。
- 关灯失败、**`hdc`** 超时于关灯步骤：**不**推翻「版本已校验一致」的结论（仍为 **exit 0**）。

---

## 注意事项

- 烧录会改写分区，确认镜像与板型匹配。
- **密码**勿进公开仓库；生产用密钥或环境变量。
- 无 TTY 时不要用交互 **`raw-scp`**；用 **`pscp-sync`** 或 **`sync-images`**。
- 大同步：**`pscp-sync --timeout`**；长烧录：**`--long-timeout`**。
- **`pscp` 写 `system.img` 失败**（磁盘、杀毒、路径）时先清坏文件、查空间再重试。
- 版本校验需 **`rd` 后 hdc 可用** 且 **SSH 可读 `ohos.para`**；无 **pscp** 时需 **paramiko**。
- **烧录完成**：须**等待** **`python rkflash.py`** **进程结束**，**exit 0** 且**未**使用 **`--no-verify-version`**，才算 **`upgrade_tool` 成功 + 版本一致**（见上文 **「烧录完成判定」**）。自动化或助手代跑时**禁止**「命令下发即视为完成」；**`--no-verify-version`** 仅调试，**不**作为发布/验收依据。
