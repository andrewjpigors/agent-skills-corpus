---
name: ohhdc
description: "OpenHarmony HDC helper in napi_generator: install/uninstall/list HAPs, deploy-test and static-deploy-test pipelines, screenshots and uitest layout dumps, Wi‑Fi utilities, hilog/faultlog, LEDs. Wraps hdc shell flows implemented in ohhdc.py; device-side ability CLI names follow upstream OpenHarmony docs."
author: "Created by user"
created: "2026-01-28"
version: "1.0.2"
---

# OpenHarmony HDC Skill

This skill provides capabilities for OpenHarmony ecosystem devices via **HDC** (the **hdc** host tool: the standard device bridge for OHOS in the OpenHarmony / DevEco SDK): **list installed HAP apps**, **uninstall HAP**, **install HAP**, **install-project** (install main + test HAP with two `hdc install` commands), **deploy-test** (部署运行 HAP 测试用例：卸载后以 `hdc install -r` 安装主包与测试包，再在设备 shell 执行应用测试流水线), **replace-install HAP**, **display screenshot** (`snapshot_display` + `hdc file recv`，默认保存到技能目录 `screenshot/`), **app-scoped screenshot** (`screenshot-app` / `snap-app`: 设备侧拉起应用别名后执行 `snapshot_display`; 预设别名见 `ohhdc.py` 中 `SCREENSHOT_APP_ALIASES`), **UI layout JSON** (`uitest dumpLayout` + `hdc file recv`，默认保存到 `layout/`), **Wi‑Fi via wificommand** (`wifi-kaihong`: enable Wi‑Fi and connect default **KaiHong** / **KaiHong@888** or custom `--wifi-ssid` / `--wifi-password`), **control LEDs** (`/sys/class/leds/{red,green,blue}/brightness`), **view device logs (hilog)**, **view error/fault logs (data/log/faultlog)**, **view foreground/running applications**, **force-stop applications**, **start applications**, and **run tests**.

## 应用示例与提示词（中文）

在 **napi_generator 仓库根** 执行；需 **`hdc`** 在 PATH、设备已连接。

| 场景 | 命令示例 | 提示词示例 |
|------|----------|------------|
| 已装应用 | `python3 src/skills/ohhdc/ohhdc.py apps` | 「列出设备上所有 HAP bundle」 |
| 安装/覆盖 | `python3 src/skills/ohhdc/ohhdc.py replace-install /path/to-signed.hap` | 「替换安装这个签好的 hap」 |
| 跑 ohosTest | `python3 src/skills/ohhdc/ohhdc.py test <bundle> -m <module> ...` | 「在设备上跑 nativeproj 的单元测试套件」 |
| 故障日志 | `python3 src/skills/ohhdc/ohhdc.py faultlog` | 「看下 faultlog 目录里最近错误」 |
| 截屏 | `python3 src/skills/ohhdc/ohhdc.py screenshot` | 「截一张全屏保存到技能 screenshot 目录」 |
| Wi‑Fi | `python3 src/skills/ohhdc/ohhdc.py wifi-kaihong` | 「连上默认 KaiHong AP」 |
| 帮助 | `python3 src/skills/ohhdc/ohhdc.py --help` | 「ohhdc 有哪些子命令」 |

## Query Installed Apps

### Feature Description

**List device-installed HAP applications.** The skill runs `hdc shell "bm dump -a"` to get all installed bundle names (HAP apps) from the connected device, then formats the output as Markdown for easy reading.

### When to Use

- User asks: "查看设备上安装的 HAP" / "查看设备安装的 app" / "设备上装了多少 hap"
- User asks: "List installed apps on device" / "Show device HAP apps" / "How many apps are installed"
- User needs to inspect or count installed applications on an OpenHarmony-compatible device

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc shell 'bm dump -a'"` (so `hdc` is in PATH from bashrc)
2. Parse output: skip `ID:` lines, strip leading tabs/spaces, extract bundle names (lines containing `.` or starting with `ohos.`)
3. Deduplicate and format as Markdown: table + bullet list

### Usage in Conversation

**Natural language examples:**

- "查看设备上安装的 HAP"
- "查看设备安装的 app"
- "设备上装了多少 hap"
- "List installed apps on the device"
- "Show me the installed HAP apps"

The assistant uses this skill to run the script and show the result in Markdown.

### Quick Start – Using the Script

```bash
# From project root; ensure hdc is available (e.g. source ~/.bashrc in your shell first)

# List installed apps, Markdown format (default)
python3 src/skills/ohhdc/ohhdc.py apps

# Same, explicit format
python3 src/skills/ohhdc/ohhdc.py list-apps --format markdown

# Plain text list
python3 src/skills/ohhdc/ohhdc.py apps --format plain
```

**Available commands:**

- `apps` / `list-apps` – List installed HAP apps (bundle names).
- `--format markdown` or `--format md` – Output as Markdown (default).
- `--format plain` or `--format list` – Output as plain text list.

---

## Uninstall HAP

### Feature Description

**Uninstall a HAP from the device** by bundle name. Uses:  
`hdc shell "bm uninstall -n <bundleName>"`.

### When to Use

- User says: "卸载设备上的 xxx 应用" / "卸载 com.example.p7zipTest" / "uninstall HAP com.xxx.xxx"
- User needs to remove a specific app by its bundle name.

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc shell \"bm uninstall -n <bundleName>\""`
2. Print success or error.

### Usage in Conversation

- "卸载 com.example.p7zipTest"
- "Uninstall the app com.example.p7zipTest from the device"

### Quick Start – Script

```bash
# Uninstall by bundle name (required)
python3 src/skills/ohhdc/ohhdc.py uninstall com.example.p7zipTest
```

**Parameter:** `target` = bundle name (e.g. `com.example.p7zipTest`).

---

## Install HAP

### Feature Description

**Install a HAP file onto the device.** Uses:  
`hdc install <hap_path>`.

### When to Use

- User says: "安装这个 HAP 到设备" / "把 xxx.hap 装到设备" / "install HAP /path/to/app.hap"
- User provides a HAP file path and wants to install it.

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc install <hap_path>"`
2. Path is quoted so spaces are safe.
3. Print success or error.

### Usage in Conversation

- "安装 `src/skills/ohhap/NativeProj46R/autosign/app1-signed.hap`"（假定当前目录为 **napi_generator** 仓库根）
- "Install the HAP at .../app1-signed.hap to the device"

### Quick Start – Script

```bash
# Install HAP（在 napi_generator 仓库根下；也可用 .hap 的绝对路径）
python3 src/skills/ohhdc/ohhdc.py install src/skills/ohhap/NativeProj46R/autosign/app1-signed.hap
```

**Parameter:** `target` = absolute or relative path to the `.hap` file.

---

## Install Project (主 HAP + 测试 HAP，推荐)

### Feature Description

**按项目安装两个 HAP**：先安装主 HAP，再安装测试 HAP，均使用 `hdc install`（不用 `-r`）。  
等价于依次执行：

- `hdc install <project_dir>/entry/build/default/outputs/default/entry-default-signed.hap`
- `hdc install <project_dir>/entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap`

安装前如设备上已有同包名应用且签名不一致，需先卸载再执行本安装。

### When to Use

- User says: "安装这个项目的两个 HAP" / "按项目安装 NativeProj46R" / "install project"
- 签名、编译完成后，需要将主 HAP 与测试 HAP 部署到设备。

### Quick Start – Script

```bash
# 按项目安装（target = 项目根目录；示例为仓库内 examples/NativeProj46R）
python3 src/skills/ohhdc/ohhdc.py install-project examples/NativeProj46R
```

或手动执行两个命令：

```bash
hdc install examples/NativeProj46R/entry/build/default/outputs/default/entry-default-signed.hap
hdc install examples/NativeProj46R/entry/build/default/outputs/ohosTest/entry-ohosTest-signed.hap
```

**Parameter:** `target` = 项目根目录（含 `entry/build/...` 的上级目录）。

---

## 部署运行 HAP 测试用例（deploy-test）

### Feature Description

**部署并运行 HAP 测试用例**：依次执行「卸载同包名应用 → 使用 `hdc install -r` 安装主 HAP → 使用 `hdc install -r` 安装测试 HAP → 经 **`hdc shell`** 在设备上执行 **应用测试** 子流程（与 OpenHarmony 设备侧命令行工具一致，由本仓库 `ohhdc.py` 拼出参数）。  
等价于历史记录中的完整流程：先卸载，再两条 `hdc install -r`，最后在设备 shell 内对主/测包执行带 **`-s class`、`-s timeout`、`-m entry_test`、`-s unittest`** 等参数的应用测试命令。

- 包名（bundleName）未指定时，从项目 `AppScope/app.json5` 解析。
- 主 HAP、测试 HAP 路径约定与 install-project 相同。
- **测试套件自动发现**：未通过 `--suite` 指定时，从项目 `entry/src/ohosTest/ets/test/List.test.ets` 解析调用的测试函数（如 `abilityTest()`、`indexUitestTest()`），再在各对应 `.test.ets` 文件中读取 `describe('SuiteName', ...)` 的 `SuiteName`，按 List 中的顺序拼成 `-s class ActsAbilityTest,IndexUitestTest,IndexdtsTest` 等形式；解析失败时回退为 `ActsAbilityTest,IndexUitestTest`。

### When to Use

- User says: "部署运行 HAP 测试用例" / "卸载后安装两个 HAP 再跑测试" / "deploy and run HAP tests"
- 需要一键完成：卸载 → 安装主 HAP + 测试 HAP → 运行测试。

### Quick Start – Script

```bash
# 部署运行测试（target = 项目根目录；测试套件从 List.test.ets 自动发现，默认 -m entry_test -t 15000）
python3 src/skills/ohhdc/ohhdc.py deploy-test examples/NativeProj46R

# 指定测试套件与超时（覆盖自动发现）
python3 src/skills/ohhdc/ohhdc.py deploy-test /path/to/NativeProj46R --suite "ActsAbilityTest,IndexUitestTest" --timeout 20000
```

**Parameters:** `target` = 项目根目录；`--module` / `-m` = 测试模块名（默认 entry_test）；`--suite` / `-s` = `-s class` 的取值，多个套件逗号分隔（**不指定时从 List.test.ets 及各 .test.ets 的 describe 名自动发现**）；`--timeout` / `-t` = 超时毫秒（默认 15000）。

---

## 静态 XTS：仅主包 + unittest TestRunner（static-deploy-test）

### Feature Description

**ArkTS `use static` + Hypium 一体工程**常见形态：无独立 ohosTest HAP，测试入口为 **主模块** 内的 **`OpenHarmonyTestRunner`**。设备侧推荐与文档一致：

设备侧完整命令与上游文档一致：**`-s timeout`** 写在 **`-s unittest`**（Runner 多为类名 **`OpenHarmonyTestRunner`**）之前。

（Runner 优先用**类名**；仅在设备要求时使用 `/ets/testrunner/...` 路径形式。）

本动作依次：**卸载同包名 → `hdc install -r` 仅主包 `entry-default-signed.hap` → 执行上述形态的应用测试命令**。与 **`deploy-test`**（双 HAP + `-s class`）互斥，请按工程类型选用。

### Quick Start – Script

```bash
python3 src/skills/ohhdc/ohhdc.py static-deploy-test /path/to/static_xts_project
export OHOS_A​A_TEST_TIMEOUT_MS=600000
python3 src/skills/ohhdc/ohhdc.py static-deploy-test /path/to/project --timeout 600000 -m entry --unittest-runner OpenHarmonyTestRunner
# 本机等待设备应用测试结束的墙钟（秒）：默认至少约 30 分钟；套件很大时可增大
export OHOS_A​A_TEST_WALL_SEC=7200
python3 src/skills/ohhdc/ohhdc.py static-deploy-test /path/to/project
```

**说明**：`--timeout` 传给设备的 `-s timeout`（毫秒）；子进程最长等待由 **`OHOS_A​A_TEST_WALL_SEC`** 控制（未设时默认 **≥1800s**），与设备参数不是同一含义。框架单测超时还可设 **`OHOS_A​A_TEST_TIMEOUT_MS`**（覆盖 `-s timeout` 毫秒值，整包 Hypium 建议 **≥ 300000**）。

**「测试没跑起来」常见原因（非等待时间）**：
1. **`-s unittest` 取值**：官方文档要求多为 **类名** `OpenHarmonyTestRunner`，不是路径 `/ets/testrunner/...`；脚本默认已改为类名，路径可通过 **`OHOS_A​A_TEST_UNITTEST_RUNNER`** 或 **`--unittest-runner`** 指定。
2. **参数顺序**：文档示例为 **`-s timeout <ms> -s unittest <runner>`**，顺序与部分环境解析有关，脚本已按此排列。
3. **Release 签名**：部分设备上 **release 签名的 HAP 无法执行应用测试子命令**（错误码 **10106002**），需使用 **debug 包** 或符合设备策略的签名。

**日志为何常「看不到」**：Hypium 大量输出在设备 **hilog**，应用测试子进程回传到本机终端的 stdout 可能很少；超时场景下旧实现还曾**丢弃**子进程已有片段。现支持：**合并 stderr**、超时**保留已捕获片段**、**`OHOS_A​A_TEST_LOG_FILE`** 用 `tee` 落盘。

**应用测试执行过程中轮询 hilog**：自应用测试子进程启动起，后台线程按间隔（**`OHOS_A​A_TEST_HILOG_POLL_SEC`**，默认 3s）短采 **hilog**（单次时长 **`OHOS_A​A_TEST_HILOG_SLICE_SEC`**，默认 5s），拼在 **标准输出之前**，便于看「跑的过程中」哪一步出错。**`OHOS_A​A_TEST_SKIP_HILOG_DURING=1`** 可关；**`OHOS_A​A_TEST_SKIP_HILOG=1`** 会同时关闭「过程中」与「结束后」两段自动 hilog。

**应用测试结束后自动抓 hilog**：返回前再调用 **`capture_hilog_after_app_test`**（约 **20s** 一段）。可调 **`OHOS_A​A_TEST_HILOG_SEC`**、**`OHOS_A​A_TEST_HILOG_GREP`**（与过程中共用同一 grep 变量）。

---

## Replace Install HAP

### Feature Description

**Replace-install a HAP** (overwrite existing app with same bundle name). Uses:  
`hdc -r install <hap_path>`.

### When to Use

- User says: "替换安装这个 HAP" / "覆盖安装 xxx.hap" / "replace install /path/to/app.hap"
- User wants to update an already installed app by reinstalling the HAP.

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc -r install <hap_path>"`
2. Path is quoted so spaces are safe.
3. Print success or error.

### Usage in Conversation

- "替换安装 `src/skills/ohhap/NativeProj46R/autosign/app1-signed.hap`"（假定当前目录为 **napi_generator** 仓库根）
- "Replace-install the HAP at .../app1-signed.hap"

### Quick Start – Script

```bash
# Replace-install HAP（在 napi_generator 仓库根下；也可用 .hap 的绝对路径）
python3 src/skills/ohhdc/ohhdc.py replace-install src/skills/ohhap/NativeProj46R/autosign/app1-signed.hap
```

**Parameter:** `target` = absolute or relative path to the `.hap` file.

---

## View Device Logs (hilog)

### Feature Description

**View device hilog output** from the connected device. The skill runs `hdc shell hilog` to stream log output. Optional behavior:

- **Debug level**: `hdc shell hilog -b D` – show debug-level logs.
- **Show private info**: `hdc shell hilog -p off` – turn off filtering of private information.
- **Disable flow control**: `hdc shell param set hilog.flowctrl.proc.on false` – run once before hilog to reduce dropped logs.
- **Filter by keyword or PID**: `hdc shell hilog | grep <pattern>` – filter on the host (e.g. `grep BMS` for keyword "BMS", or grep by process tag/pid). The filter can be a keyword or a PID.

Because hilog streams continuously, the skill captures output for a configurable number of seconds (default 15), then stops.

### When to Use

- User asks: "查看设备日志" / "抓一下设备 hilog" / "看下 debug 级别日志" / "用 grep 过滤 BMS 相关日志"
- User asks: "View device logs" / "Show hilog from device" / "Capture debug-level hilog" / "Filter hilog by keyword"
- User needs to debug or inspect runtime logs on the device

### How It Works

1. Optionally run: `hdc shell "param set hilog.flowctrl.proc.on false"` when `--flowctrl-off` is set.
2. Build hilog command: `hdc shell "hilog [-b D] [-p off]"` according to `--level` and `--private-off`.
3. Run with `timeout <N>` so capture ends after N seconds; if `--grep` or positional filter is given, pipe output through `grep --line-buffered <pattern>` on the host.
4. Print captured stdout (and stderr when relevant).

### Usage in Conversation

- "查看设备日志"
- "抓 20 秒设备 hilog，用 debug 级别"
- "关闭 private 屏蔽并查看 hilog"
- "查看设备日志，只显示包含 BMS 的行"
- "View device hilog with debug level"
- "Filter device logs by keyword testTag"

### Quick Start – Script

```bash
# 查看设备日志（默认采集 15 秒）
python3 src/skills/ohhdc/ohhdc.py hilog
python3 src/skills/ohhdc/ohhdc.py logs

# Debug 级别
python3 src/skills/ohhdc/ohhdc.py hilog --level D
python3 src/skills/ohhdc/ohhdc.py hilog -b D

# 关闭对 private 信息的屏蔽
python3 src/skills/ohhdc/ohhdc.py hilog --private-off
python3 src/skills/ohhdc/ohhdc.py hilog -p

# 先关闭 hilog 流量控制再抓日志
python3 src/skills/ohhdc/ohhdc.py hilog --flowctrl-off
python3 src/skills/ohhdc/ohhdc.py hilog -f

# 按关键字或 pid 过滤（BMS 为示例，可为任意关键字或 pid）
python3 src/skills/ohhdc/ohhdc.py hilog BMS
python3 src/skills/ohhdc/ohhdc.py hilog --grep testTag
python3 src/skills/ohhdc/ohhdc.py hilog -g 12345

# 组合：debug 级别 + 关闭 private 屏蔽 + 过滤 BMS + 采集 30 秒
python3 src/skills/ohhdc/ohhdc.py hilog BMS -b D -p -f --hilog-timeout 30
```

**Parameters:**

- `hilog` / `logs` – View device hilog (stream captured for a limited time).
- `target` (positional) – Optional filter pattern for grep (e.g. `ohhdc.py hilog BMS`).
- `--level` / `-b` – Log level (e.g. `D` for debug).
- `--private-off` / `-p` – Use `hilog -p off` to show private info.
- `--flowctrl-off` / `-f` – Run `param set hilog.flowctrl.proc.on false` before hilog.
- `--grep` / `-g` – Filter lines by keyword or pid (grep on host).
- `--hilog-timeout` – Capture duration in seconds (default 15).

---

## View Error / Fault Logs (faultlog)

### Feature Description

**View device error/fault logs** under `/data/log/faultlog`. The directory contains four subdirectories for analysis:

- **faultlogger** – fault logger 相关日志
- **freeze** – 卡死/冻结类日志
- **hilog** – 持久化 hilog 错误日志
- **temp** – 临时错误日志

The skill runs `hdc shell "ls -la /data/log/faultlog"` (or a subdir) to list files, and `hdc shell "cat <path>"` (or `tail -n N`) to read file content. Use this to **analyze crash/freeze/error logs** on the device.

### When to Use

- User asks: "查看设备错误日志" / "data/log/faultlog 下有什么" / "看下 faultlogger 目录" / "读取 hilog 错误日志文件"
- User asks: "View device fault log" / "List error log directory" / "Analyze faultlog content"
- User needs to debug crashes, freezes, or errors using faultlog/faultlogger/freeze/hilog/temp

### How It Works

1. **List**: Run `hdc shell "ls -la /data/log/faultlog"` or `ls -la /data/log/faultlog/<subdir>` (subdir: faultlogger, freeze, hilog, temp).
2. **Read**: Run `hdc shell "cat /data/log/faultlog/<rel_path>"` (or `tail -n N` when `--tail` is set). `rel_path` is relative to faultlog (e.g. `hilog/xxx.log`).
3. Print output for user to analyze.

### Usage in Conversation

- "查看设备错误日志目录"
- "列出 data/log/faultlog 下的 faultlogger"
- "读取 faultlog 里 hilog 目录下的某个日志文件"
- "View faultlog directory" / "Show last 100 lines of faultlogger log file"

### Quick Start – Script

```bash
# 列出 /data/log/faultlog 根目录
python3 src/skills/ohhdc/ohhdc.py faultlog
python3 src/skills/ohhdc/ohhdc.py error-log

# 列出子目录（faultlogger / freeze / hilog / temp）
python3 src/skills/ohhdc/ohhdc.py faultlog faultlogger
python3 src/skills/ohhdc/ohhdc.py faultlog hilog
python3 src/skills/ohhdc/ohhdc.py faultlog freeze
python3 src/skills/ohhdc/ohhdc.py faultlog temp

# 读取某文件内容（相对 data/log/faultlog 的路径）
python3 src/skills/ohhdc/ohhdc.py faultlog --cat hilog/2024-01-01-12.log
python3 src/skills/ohhdc/ohhdc.py faultlog --cat faultlogger/xxx

# 只读最后 N 行
python3 src/skills/ohhdc/ohhdc.py faultlog --cat hilog/xxx.log --tail 100
```

**Parameters:**

- `faultlog` / `error-log` – List or read error/fault logs under `/data/log/faultlog`.
- `target` (positional) – Optional subdir: `faultlogger`, `freeze`, `hilog`, or `temp` (list that subdir).
- `--cat` – Read file content; path is relative to `/data/log/faultlog` (e.g. `hilog/xxx.log`).
- `--tail` – When used with `--cat`, output only the last N lines of the file.

---

## View Foreground/Running Apps

### Feature Description

**View foreground applications and running app processes** on the device. Uses:  
- `hdc shell "a​a dump -a"` - View all abilities (foreground and background)
- `hdc shell "a​a dump -r"` - View running abilities (app processes)

Extracts key information: bundle name, ability name, ability type, app state (FOREGROUND/BACKGROUND), start time, AbilityRecord ID, and running app processes (process name, PID, UID, state).

### When to Use

- User says: "查看前台应用" / "查看正在运行的应用" / "查看设备上的前台应用"
- User says: "Show foreground apps" / "View running applications" / "What apps are running"
- User needs to inspect which apps are currently active on the device

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc shell \"a​a dump -a\""` (or `a​a dump -r` for running only)
2. Parse output: extract AbilityRecord info (bundle name, ability type, app state, etc.) and AppRunningRecords (process info)
3. Format as Markdown: show foreground apps table and running app processes table

### Usage in Conversation

- "查看前台应用"
- "查看正在运行的应用"
- "设备上哪些应用在前台"
- "Show foreground apps on the device"
- "View running applications"

### Quick Start – Script

```bash
# View foreground apps (default: shows foreground + running processes)
python3 src/skills/ohhdc/ohhdc.py foreground

# Same, short form
python3 src/skills/ohhdc/ohhdc.py fg

# View all abilities (including background)
python3 src/skills/ohhdc/ohhdc.py dump-all

# View running abilities only
python3 src/skills/ohhdc/ohhdc.py running
python3 src/skills/ohhdc/ohhdc.py dump-running
```

**Available commands:**

- `foreground` / `fg` – View foreground apps and running processes (default view)
- `dump-all` – View all abilities including background ones
- `running` / `dump-running` – View running abilities/app processes only

**Output includes:**

- **Foreground Apps Table**: Bundle Name, Ability Name, Type, State, AbilityRecord ID, Start Time
- **Running App Processes Table**: Process Name, PID, UID, State

---

## Force Stop Application

### Feature Description

**Force-stop an application** by bundle name. Uses:  
`hdc shell "a​a force-stop <bundleName>"`.

### When to Use

- User says: "强制关闭 xxx 应用" / "关闭 com.ohos.settings" / "force stop app com.xxx.xxx"
- User needs to forcefully terminate a running application on the device.

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc shell \"a​a force-stop <bundleName>\""`
2. Print success or error.

### Usage in Conversation

- "强制关闭 com.ohos.settings"
- "关闭设置应用"
- "Force stop the app com.ohos.settings"

### Quick Start – Script

```bash
# Force-stop by bundle name (required)
python3 src/skills/ohhdc/ohhdc.py force-stop com.ohos.settings

# Same, short form
python3 src/skills/ohhdc/ohhdc.py stop com.ohos.settings
```

**Parameter:** `target` = bundle name (e.g. `com.ohos.settings`).

---

## Start Application

### Feature Description

**Start an application** by bundle name and ability name. Uses:  
`hdc shell "a​a start -a <abilityName> -b <bundleName>"`.

### When to Use

- User says: "启动 xxx 应用" / "打开 com.ohos.settings" / "start app com.xxx.xxx"
- User needs to launch an application on the device.

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc shell \"a​a start -a <abilityName> -b <bundleName>\""`
2. Print success or error.

### Usage in Conversation

- "启动 com.ohos.settings 应用"
- "打开设置应用，使用 EntryAbility"
- "Start the app com.ohos.settings with EntryAbility"

### Quick Start – Script

```bash
# Start app (requires bundleName and ability name)
python3 src/skills/ohhdc/ohhdc.py start com.ohos.settings --ability EntryAbility

# Same, using short form
python3 src/skills/ohhdc/ohhdc.py start com.ohos.settings -a EntryAbility
```

**Parameters:**
- `target` = bundle name (e.g. `com.ohos.settings`)
- `--ability` / `-a` = ability name (e.g. `EntryAbility`)

**Note:** Common ability names include:
- `EntryAbility` - Main entry ability
- `com.ohos.settings.MainAbility` - Settings main ability
- Check installed apps or use `a​a dump -a` to find ability names

---

## Run Tests

### Feature Description

**Run test cases** for an application. Uses:  
`hdc shell "a​a test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s class <suiteName>[#<caseName>] -s timeout <timeout>"`.

Supports:
- **Run specific test case**: Provide suite name and case name (e.g., `ActsAbilityTest#assertContain`)
- **Run full test suite**: Provide only suite name (e.g., `ActsAbilityTest`)

### When to Use

- User says: "运行测试" / "执行测试用例" / "运行 ohos.test.nativeproj46r 的测试"
- User says: "Run tests for app" / "Execute test case" / "Run ActsAbilityTest#assertContain"
- User needs to run unit tests or specific test cases on the device.

### How It Works

1. Execute: `bash -c "source ~/.bashrc && hdc shell \"a​a test -b <bundleName> -m <moduleName> -s unittest OpenHarmonyTestRunner -s class <suiteName>[#<caseName>] -s timeout <timeout>\""`
2. If `caseName` is provided, runs specific test case: `suiteName#caseName`
3. If `caseName` is not provided, runs full test suite: `suiteName`
4. Print test execution results.

### Usage in Conversation

- "运行 ohos.test.nativeproj46r 的测试"
- "执行 ActsAbilityTest#assertContain 测试用例"
- "运行 entry_test 模块的全量测试"
- "Run tests for ohos.test.nativeproj46r"
- "Execute test case ActsAbilityTest#assertContain"

### Quick Start – Script

```bash
# Run specific test case
python3 src/skills/ohhdc/ohhdc.py test ohos.test.nativeproj46r \
  --module entry_test \
  --suite ActsAbilityTest \
  --case assertContain \
  --timeout 15000

# Run full test suite (omit --case)
python3 src/skills/ohhdc/ohhdc.py test ohos.test.nativeproj46r \
  --module entry_test \
  --suite ActsAbilityTest \
  --timeout 15000

# Using short form
python3 src/skills/ohhdc/ohhdc.py test ohos.test.nativeproj46r \
  -m entry_test \
  -s ActsAbilityTest \
  -c assertContain \
  -t 15000
```

**Parameters:**
- `target` = bundle name (e.g. `ohos.test.nativeproj46r`) - **required**
- `--module` / `-m` = module name (e.g. `entry_test`) - **required**
- `--suite` / `-s` = test suite name (e.g. `ActsAbilityTest`) - **required**
- `--case` / `-c` = test case name (e.g. `assertContain`) - **optional**, if provided runs specific case, otherwise runs full suite
- `--timeout` / `-t` = timeout in milliseconds (default: 15000) - **optional**

**Examples:**

```bash
# Run specific test case
python3 src/skills/ohhdc/ohhdc.py test ohos.test.nativeproj46r \
  -m entry_test -s ActsAbilityTest -c assertContain

# Run full test suite
python3 src/skills/ohhdc/ohhdc.py test ohos.test.nativeproj46r \
  -m entry_test -s ActsAbilityTest

# With custom timeout (30 seconds)
python3 src/skills/ohhdc/ohhdc.py test ohos.test.nativeproj46r \
  -m entry_test -s ActsAbilityTest -t 30000
```

---

## 屏幕截图（snapshot_display + file recv）

### Feature Description

1. 在设备上执行 **`snapshot_display`**，通过 **`-f`** 将图片写到固定路径（默认 **`/data/local/tmp/ohhdc_screenshot.jpeg`**，须在 `/data/local/tmp` 下且扩展名为 `.jpeg` / `.png`，与系统工具校验一致）。
2. 使用 **`hdc file recv <设备路径> <本机路径>`** 将文件拉到本地。
3. **本机默认目录**：`src/skills/ohhdc/screenshot/`（仅文件名或省略路径时自动写入该目录；写绝对路径则按指定位置保存）。

**注意**：`snapshot_display` 在源码中要求设备处于**开发者模式**，否则会提示 `not developer mode` 并退出。

**实现与 windowId 说明**：`-i` / `--display-id` 为 **DisplayId**（整屏/某块屏），**不是** windowId；按窗口截图需见设计文档  
[docs/snapshot_display_design.md](docs/snapshot_display_design.md)（含 layout bounds + 裁剪等可行路径）。

### Quick Start – Script

```bash
# 默认：src/skills/ohhdc/screenshot/ohhdc_screenshot_YYYYMMDD_HHMMSS.jpeg
python3 src/skills/ohhdc/ohhdc.py screenshot

# 与 screenshot 等价
python3 src/skills/ohhdc/ohhdc.py snapshot

# 仅指定文件名 → 仍保存在 screenshot/ 下
python3 src/skills/ohhdc/ohhdc.py screenshot my.jpeg

# 任意本机绝对路径
python3 src/skills/ohhdc/ohhdc.py screenshot /tmp/screen.jpeg

# 指定显示 ID（多屏）
python3 src/skills/ohhdc/ohhdc.py screenshot --display-id 0

# 指定设备端路径（需仍满足 snapshot 路径/后缀规则）
python3 src/skills/ohhdc/ohhdc.py snapshot --device-file /data/local/tmp/my.jpeg
```

### Usage in Conversation

- “截个图保存到桌面” → `ohhdc.py screenshot ~/Desktop/screen.jpeg`
- “用 hdc 抓屏” → `ohhdc.py snapshot`

---

## 指定应用截图（screenshot-app / snap-app）

### Feature Description

1. 根据 **别名**（`ohhdc.py` 中 `SCREENSHOT_APP_ALIASES`）或 **完整包名 + `--ability`**，在设备上执行 **`a​a start`**，等待界面就绪后执行 **`snapshot_display`**，再 **`hdc file recv`** 拉到本机。
2. 与 **整屏截图** 一致：仍是 **Display 位图**，不是按 windowId 单独出图；多窗同屏时其它窗口可能入镜。仅裁某一窗口需 **layout bounds + 本机裁剪**（见 [docs/snapshot_display_design.md](docs/snapshot_display_design.md)）。
3. **预设别名**（可在 `ohhdc.py` 中扩展）：

| 别名 | bundleName | 默认 Ability |
|------|------------|--------------|
| `etsclock` | `ohos.samples.etsclock` | `MainAbility` |

非别名：`ohhdc.py screenshot-app <bundleName> --ability <AbilityName>`。

### Quick Start – Script

```bash
# 预设别名：先启动 etsclock，约 2s 后整屏截图 → ohhdc/screenshot/screenshot_app_etsclock_*.jpeg
python3 src/skills/ohhdc/ohhdc.py screenshot-app etsclock

# 等价
python3 src/skills/ohhdc/ohhdc.py snap-app etsclock

# 指定本机保存路径（第二参数仅 screenshot-app 使用）
python3 src/skills/ohhdc/ohhdc.py screenshot-app etsclock ./clock.jpeg

# 完整包名 + Ability
python3 src/skills/ohhdc/ohhdc.py screenshot-app ohos.samples.etsclock -a MainAbility

# 多屏、启动后等待更久再截
python3 src/skills/ohhdc/ohhdc.py screenshot-app etsclock --display-id 0 --app-delay 3.5
```

### Usage in Conversation

- “截一张 etsclock 的图” → `ohhdc.py screenshot-app etsclock`
- “先打开应用再截图” → `ohhdc.py snap-app <别名>` 或包名 + `-a`

### 扩展预设别名

编辑 `src/skills/ohhdc/ohhdc.py` 中 `SCREENSHOT_APP_ALIASES`，增加  
`"短名": ("完整包名", "默认主Ability")`。

---

## 当前页面 layout（uitest dumpLayout + file recv）

### Feature Description

1. 在设备上执行 **`hdc shell uitest dumpLayout -p <设备端路径>`**（与 arkxtest `uitest` 命令行一致），将当前界面控件树导出为 **JSON**。
2. 使用 **`hdc file recv`** 将 JSON 拉到本机；若内容为合法 JSON，脚本会**缩进格式化**后写回。
3. **本机默认目录**：`src/skills/ohhdc/layout/`（默认文件名 `uitest_layout_YYYYMMDD_HHMMSS.json`）。

设备端默认路径：`/data/local/tmp/ohhdc_uitest_layout.json`（可用 `--device-file` 修改）。

可选参数与 `uitest dumpLayout` 对应：`--display-id`（`-d`）、`--bundle`（`-b`）、`--window-id`（`-w`）、`--layout-merge true|false`（`-m`）、`--layout-font`（`-a`）、`--layout-independent`（`-i`）、`--layout-extend`（`-e`）。

### Quick Start – Script

```bash
# 默认写入 src/skills/ohhdc/layout/uitest_layout_*.json
python3 src/skills/ohhdc/ohhdc.py layout

# 等价
python3 src/skills/ohhdc/ohhdc.py dump-layout

# 指定本机文件名（仍在 layout/ 目录）
python3 src/skills/ohhdc/ohhdc.py layout ui.json

# 指定包名窗口、显示 ID 等
python3 src/skills/ohhdc/ohhdc.py layout --bundle com.example.app --display-id 0
```

### Usage in Conversation

- “导出当前页面布局 json” → `ohhdc.py layout`
- “把 uitest layout 存到项目里” → `ohhdc.py layout /path/to/out.json`

---

## Wi‑Fi：wificommand 开网并连 KaiHong（wifi-kaihong）

### Feature Description

使用 **wificlitools** 可执行文件 **`wificommand`**（源码 `foundation/communication/wifi/wifi/test/wificlitools`，GN 目标 `wificommand`）。通过 HDC 依次执行：

1. **`wifienable`** — 打开 Wi‑Fi  
2. **`wificonnect ssid=<SSID> password=<密码>`** — 连接热点（默认 **SSID `KaiHong`**、密码 **`KaiHong@888`**）  
3. **`wifigetstatus`** — 打印状态（可用 `--no-wifi-status` 跳过）

设备侧整条命令经 **`shlex.quote`** 传给 `hdc shell`，避免主机对 `@` 等字符误解析。

**镜像里是否自带 `wificommand`？**  
`wificlitools/BUILD.gn` 中 **`ohos_executable("wificommand")` 未设置 `install_enable`**，且目标挂在 **`test/BUILD.gn`** 的 **`unittest`** 组，**默认不会打进 system 分区**。因此多数产品镜像 **没有** `/system/bin/wificommand`。

**处理方式**：

1. **检查**：`ohhdc.py wifi-check-wificommand`（设备 PATH、`/system/bin`、临时路径 + 本机 `out/<product>` 是否已有产物）。  
2. **单独编译**（在源码根）：`./build.sh --product-name <产品> --build-target wificommand`  
   产物常见路径：`out/<产品>/communication/wifi/wificommand` 或 `out/<产品>/exe.unstripped/communication/wifi/wificommand`。  
3. **推送到设备**：`ohhdc.py wifi-push-wificommand`（按 `out` 自动查找，或第一个参数传本机二进制绝对路径），默认推到 **`/data/local/tmp/wificommand`** 并 **`chmod 755`**。  
4. **一键推送并连 KaiHong**：`ohhdc.py wifi-kaihong --push-wificommand --ohos-src <源码根>`（或设置 **`OHOS_SRC`**）。  
5. 已手动推送时可用 **`--wifi-device-bin /data/local/tmp/wificommand`** 指定设备侧路径。

### Quick Start – Script

```bash
# 先看设备上有没有、本机 out 里有没有编过
python3 src/skills/ohhdc/ohhdc.py wifi-check-wificommand --ohos-src /path/to/openharmony/src

# 仅推送 wificommand（从 out/<wifi-product> 自动查找）
python3 src/skills/ohhdc/ohhdc.py wifi-push-wificommand --ohos-src /path/to/src --wifi-product rk3568

# 指定本机二进制路径推送（第二个参数为可选 positional target）
python3 src/skills/ohhdc/ohhdc.py wifi-push-wificommand /path/to/out/rk3568/communication/wifi/wificommand

# 镜像无 wificommand 时：先推送再连 KaiHong / KaiHong@888
export OHOS_SRC=/path/to/src
python3 src/skills/ohhdc/ohhdc.py wifi-kaihong --push-wificommand

# 已推到默认路径时，也可显式指定设备侧二进制
python3 src/skills/ohhdc/ohhdc.py wifi-kaihong --wifi-device-bin /data/local/tmp/wificommand

# 覆盖 SSID / 密码
python3 src/skills/ohhdc/ohhdc.py wifi-kaihong --wifi-ssid MyAP --wifi-password 'secret123'

python3 src/skills/ohhdc/ohhdc.py wifi-kaihong --no-wifi-status
```

### Usage in Conversation

- “用 wificlitools 打开 WiFi 并连 KaiHong” → 先 **`wifi-check-wificommand`**；若无则 **`wifi-push-wificommand`** 或 **`wifi-kaihong --push-wificommand`**  
- “连公司热点 MySSID 密码 xxx” → `ohhdc.py wifi-kaihong --wifi-ssid MySSID --wifi-password xxx`

### 与 wificlitools 文档

命令语义与 **`wificlitools/DESIGN.md`**、`clitools.cpp` 中 **`wifienable` / `wificonnect`** 一致；开放热点可不传密码（`--wifi-password ''`），对应框架 **`KEY_MGMT_NONE`**。

---

## 控制 LED（sysfs brightness）

### Feature Description

通过 `hdc shell` 向设备写入 `/sys/class/leds/<节点名>/brightness`，**0 为关、1 为开**（与常见 GPIO LED 驱动一致）：

| 口语/用途（示例板） | sysfs 节点 | 关 | 开 |
|--------------------|------------|----|----|
| 红灯 | `red` | `echo 0 > .../red/brightness` | `echo 1 > .../red/brightness` |
| 蓝灯（部分板卡上对应 **green** 节点） | `green` | `echo 0 > .../green/brightness` | `echo 1 > .../green/brightness` |
| 绿灯（部分板卡上对应 **blue** 节点） | `blue` | `echo 0 > .../blue/brightness` | `echo 1 > .../blue/brightness` |

> **说明**：Linux 下 LED 的 **sysfs 目录名**（`red`/`green`/`blue`）由设备树/驱动决定，可能与外壳丝印颜色不一致；脚本使用 **节点名** `red` / `green` / `blue`，请按你的硬件实际路径选用。

### Quick Start – Script

```bash
# 红灯开 / 关（等价于 hdc shell "echo 1 > /sys/class/leds/red/brightness"）
python3 src/skills/ohhdc/ohhdc.py led red on
python3 src/skills/ohhdc/ohhdc.py led red off

# sysfs 为 green 的灯（文档中常称蓝灯）
python3 src/skills/ohhdc/ohhdc.py led green on
python3 src/skills/ohhdc/ohhdc.py led green off

# sysfs 为 blue 的灯（文档中常称绿灯）
python3 src/skills/ohhdc/ohhdc.py led blue on
python3 src/skills/ohhdc/ohhdc.py led blue off
```

**参数**：`led <red|green|blue> <on|off>`。

**底层命令示例**：`hdc shell "echo 1 > /sys/class/leds/blue/brightness"` 为打开 sysfs 名为 `blue` 的灯。

### Usage in Conversation

- “把设备红灯打开” → `ohhdc.py led red on`
- “关掉 green 节点的 LED” → `ohhdc.py led green off`

---

## 环境与通用说明

### Environment Requirements（适用于所有操作）

- **hdc**: OpenHarmony HDC 需在 PATH 中。若通过 `source ~/.bashrc` 配置，脚本会执行 `bash -c "source ~/.bashrc && hdc ..."` 以保证能找到 `hdc`。
- **Device**: 设备或模拟器需已连接并被 `hdc` 识别。

### Example Output（仅“查看已安装应用”）

```markdown
## 已安装应用

共找到 **48** 个已安装应用：

| 序号 | Bundle Name |
|------|-------------|
| 1 | `com.OpenHarmony.app.test` |
| 2 | `com.example.kikakeyboard` |
...

### 应用列表（纯文本）

- `com.OpenHarmony.app.test`
- `com.example.kikakeyboard`
...
```

### Script Location

- **Skill**: `src/skills/ohhdc/SKILL.md`
- **Script**: `src/skills/ohhdc/ohhdc.py`

### Summary

| Trigger (conversation)       | Action |
|-----------------------------|--------|
| 查看设备上的已安装应用/HAP  | Run `ohhdc.py apps`，展示 Markdown 结果 |
| 设备上装了多少 hap           | Run `ohhdc.py apps`，展示数量与列表 |
| 卸载 xxx 应用 / uninstall   | Run `ohhdc.py uninstall <bundleName>`，如 `uninstall com.example.p7zipTest` |
| 安装 HAP / install          | Run `ohhdc.py install <HAP 路径>`，如 `install /path/to/app-signed.hap` |
| 按项目安装 / install-project | Run `ohhdc.py install-project <项目根目录>`，依次执行 `hdc install` 主 HAP 与测试 HAP |
| 部署运行 HAP 测试用例 / deploy-test | Run `ohhdc.py deploy-test <项目根目录>`，卸载 → `hdc install -r` 主 HAP、测试 HAP → **设备应用测试命令** |
| 替换安装 HAP / replace-install | Run `ohhdc.py replace-install <HAP 路径>`，如 `replace-install /path/to/app-signed.hap` |
| 查看前台应用 / foreground   | Run `ohhdc.py foreground` 或 `ohhdc.py fg`，展示前台应用和运行进程 |
| 查看正在运行的应用 / running | Run `ohhdc.py running`，展示运行中的应用进程 |
| 查看所有 ability / dump-all | Run `ohhdc.py dump-all`，展示所有 ability（包括后台） |
| 强制关闭应用 / force-stop   | Run `ohhdc.py force-stop <bundleName>` 或 `ohhdc.py stop <bundleName>`，如 `force-stop com.ohos.settings` |
| 启动应用 / start            | Run `ohhdc.py start <bundleName> --ability <abilityName>`，如 `start com.ohos.settings --ability EntryAbility` |
| 运行测试 / test             | Run `ohhdc.py test <bundleName> --module <moduleName> --suite <suiteName> [--case <caseName>]`，如 `test ohos.test.nativeproj46r -m entry_test -s ActsAbilityTest -c assertContain` |
| 开关 LED（sysfs）           | Run `ohhdc.py led <red\|green\|blue> <on\|off>`，如 `led red on`、`led blue off` |
| 屏幕截图                    | `screenshot` / `snapshot`，默认 `ohhdc/screenshot/`；可选 `--display-id`、`--device-file` |
| 指定应用截图（先启动再截）   | `screenshot-app` / `snap-app <别名>` 或包名 + `--ability`；可选第二参数为本机路径、`--app-delay`、`--display-id` |
| 页面 layout JSON            | `layout` / `dump-layout`，默认 `ohhdc/layout/`；可选 `--bundle`、`--window-id`、`--display-id`、`--device-file`、`--layout-*` |
| Wi‑Fi wificommand / KaiHong | `wifi-kaihong`（可选 `--push-wificommand` + `--ohos-src` / `OHOS_SRC`）；`wifi-push-wificommand`；`wifi-check-wificommand`；默认 SSID/密码见上节 |