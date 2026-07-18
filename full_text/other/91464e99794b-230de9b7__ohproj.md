---
name: ohproj
description: "创建、编译、签名、编译测试、执行测试 OpenHarmony 原生应用项目（基于 NativeProj46R 模板），含 NAPI 对接规范与测试报告说明。可选关联 ohservices 技能与 ohsa.py：在同仓库做系统镜像/SystemAbility 开发或需设备侧 hilog/hidumper 诊断时使用。"
author: "Created by user"
created: "2026-01-20"
version: "1.6.1"
---

# ohproj 技能说明

本技能提供 **创建**、**编译**、**签名**、**编译测试用例**、**执行测试用例** 与 **清除签名** 六类能力，面向基于模板 NativeProj46R 的原生应用项目（含 NAPI + ArkTS）。配套设计文档与代码规范见 **DESIGN.md**，测试报告格式见 **八、测试报告格式**。**常见问题与避免**（编译失败、测试依赖缺失、mock 未关、用例不足等）见 **KNOWN_ISSUES_AND_AVOIDANCE.md**。

**系统镜像侧 `snapshot_record` 屏幕录制 MP4**（非 HAP）：开发与烧录流程、修改文件清单、SELinux、调试命令见 **第十节**；可执行脚本 **`src/skills/ohrecord/ohrecord.py`** 与 **`src/skills/ohrecord/SKILL.md`**。

---

## 一、能力总览

| 能力 | 说明 | 调用方式 |
|------|------|----------|
| **创建项目** | 从模板拷贝并重命名目录与 bundleName，可选接入用户 C/C++ 代码目录；可选 `--setup-cjson` 一键完成 cJSON 接入（CMake、NAPI、测试、mock、oh_modules） | `ohproj.py create <项目名> [--code-dir <路径>] [--setup-cjson]` 或按 SKILL 步骤 4.x 手工执行 |
| **编译** | 检查环境并构建主 HAP（委托 ohhap/hapbuild.py） | `ohproj.py build <项目目录>` |
| **签名** | 对未签名主 HAP 与测试 HAP 进行 release/debug 签名 | `ohproj.py sign <项目目录> [release\|debug]` |
| **编译测试用例** | 构建 ohosTest 模块的单元测试 HAP（委托 hapbuild.py build-test） | `ohproj.py build-test <项目目录>` |
| **执行测试用例** | 卸载→安装主 HAP→安装测试 HAP→执行 aa test（委托 ohhdc deploy-test），输出测试报告 | `ohproj.py test <项目目录> [--timeout 毫秒]` |
| **清除签名** | 删除项目下的 autosign 目录 | `ohproj.py clean-sign <项目目录>` |

**环境依赖**：编译与签名需 HarmonyOS Command Line Tools、OpenHarmony SDK（见 ohhap 技能）；签名还需 Java 及证书目录。执行测试需设备已连接且 hdc 可用（见 ohhdc 技能）。

**可选关联（系统 SA / 镜像侧）**：若在同一源码树中开发**系统镜像**、调试 **SystemAbility（如 sampletest）**、或需在设备上批量查 **落盘 hilog / dmesg / hidumper**，可使用 **ohservices** 技能中的 **`ohsa.py`**（与纯 ArkTS 应用流程独立，见下文 **九、关联技能：ohservices / ohsa.py**）。

**编译时 Node 与工作目录**：`ohproj.py build` / `build-test` 委托 ohhap 的 hapbuild.py 执行；hapbuild 优先使用 **${HOS_CLT_PATH}/tool/node/bin/node** 运行 hvigor，若不存在则回退到 /usr/bin/node 或 PATH 中的 node；且子进程以 **cwd=项目目录** 执行，确保 hvigor 读取项目内 hvigor-config 等配置，避免“配置文件不存在”类错误。

---

## 二、使用方法

### 2.1 命令行（推荐使用绝对路径）

在仓库根目录（或任意目录）下执行，**项目目录建议使用绝对路径**，避免工作目录歧义。

```bash
# 创建项目（在 ohproj 目录下生成 <项目名>NativeProj46R）
python3 src/skills/ohproj/ohproj.py create <项目名> [--code-dir <用户代码目录>]

# 编译主 HAP
python3 src/skills/ohproj/ohproj.py build <项目目录绝对路径>

# 签名（默认 release）
python3 src/skills/ohproj/ohproj.py sign <项目目录绝对路径> [release|debug]

# 编译单元测试 HAP
python3 src/skills/ohproj/ohproj.py build-test <项目目录绝对路径>

# 执行单元测试（部署到设备并运行）
python3 src/skills/ohproj/ohproj.py test <项目目录绝对路径> [--timeout 毫秒]

# 清除签名
python3 src/skills/ohproj/ohproj.py clean-sign <项目目录绝对路径>
```

**直接调用 ohhap / ohhdc（与 ohproj 等价）：**

```bash
python3 src/skills/ohhap/hapbuild.py build <项目目录绝对路径>
python3 src/skills/ohhap/hapbuild.py sign <项目目录绝对路径> [release|debug]
python3 src/skills/ohhap/hapbuild.py build-test <项目目录绝对路径>
python3 src/skills/ohhap/hapbuild.py clean-sign <项目目录绝对路径>
python3 src/skills/ohhdc/ohhdc.py deploy-test <项目目录绝对路径> [--timeout 毫秒]
```

### 2.2 对话/提示词（供 AI 与用户使用）

**创建与接入**

- 「用 ohproj 创建原生项目，项目名 xxx，要接入的代码目录是 yyy」
- 「执行创建原生项目技能，项目名称 ohson，需要引入目录是 cJSON-master，需要导出的接口是 cJSON.h 里 CJSON_PUBLIC 声明的接口，并完成应用代码调用和测试用例编写，最后编译、签名并检查结果」
- 「对导出的接口完善对应单元测试，并编译和执行测试用例」
- 「学习 tests 目录里测试用例的设计和实现，对比 Cjsondts.test.ets 整理单元测试设计规范，补齐 ohproj 对设计、实现测试用例的能力并补全测试用例」→ 见 DESIGN.md 第六节、SKILL 步骤 4.6

**编译与签名**

- 「使用 ohproj/ohhap 技能编译 @arkcJsonNativeProj46R」
- 「使用技能签名这个项目 @arkcJsonNativeProj46R」
- 「对项目 /path/to/arkcJsonNativeProj46R 执行编译并签名」
- 「使用技能编译这个项目的单元测试并执行」→ 先 `build-test` 再 `sign` 再 `test`

**测试**

- 「@ohsonNativeProj46R 使用技能编译单元测试并执行」
- 「编译、执行这个项目的单元测试」
- 「执行测试用例后生成的测试报告里，每个测试 suite 和内部所有测试用例的执行情况怎么看？」→ 见 **八、测试报告格式**

**问题排查**

- 「为啥 Index.d.ts 没有暴露接口？」→ 检查 `entry/src/main/cpp/types/libentry/Index.d.ts` 与 `entry/oh_modules/libentry.so/Index.d.ts` 是否同步、是否导出全部 NAPI 接口。
- 「CjsondtsTest 报 undefined is not callable」→ 按步骤 4.5 将 `entry/src/mock/mock-config.json5` 清空为 `{}`。
- 「某条用例失败了，修改下」→ 根据测试报告中 `OHOS_REPORT_STATUS_CODE: -2` 与 `test=CaseName`、`stream=` 定位用例，结合 DESIGN.md 代码规范修复。
- **编译报 uv_cwd、@ohos/hypium 解析失败、测试用例数量不足等** → 见 **KNOWN_ISSUES_AND_AVOIDANCE.md** 的成因与避免/修复步骤。
- **build 或 build-test 报 `ENOENT: uv_cwd`** → 到**项目根目录**下手动执行 KNOWN_ISSUES 1.1 节「手动修复步骤」中的两条 hvigor 命令（均带 `--no-daemon`），完成主 HAP 与测试 HAP 构建后再执行 `ohproj.py sign`、`ohproj.py test`。

---

## 三、调用命令汇总

| 意图 | 命令 |
|------|------|
| 创建项目（仅拷贝+重命名+bundleName） | `python3 src/skills/ohproj/ohproj.py create arkcJson` |
| 创建并接入代码目录 | `python3 src/skills/ohproj/ohproj.py create arkcJson --code-dir src/skills/ohproj/cJSON-master` |
| 创建并一键完成 cJSON 接入（标准化可编译可测） | `python3 src/skills/ohproj/ohproj.py create <项目名> --code-dir src/skills/ohproj/cJSON-master --setup-cjson` |
| 编译主 HAP | `python3 src/skills/ohproj/ohproj.py build <napi_generator 仓库根>/src/skills/ohproj/arkcJsonNativeProj46R` |
| 签名（release） | `python3 src/skills/ohproj/ohproj.py sign <napi_generator 仓库根>/src/skills/ohproj/arkcJsonNativeProj46R` |
| 签名（debug） | `python3 src/skills/ohproj/ohproj.py sign /path/to/project debug` |
| 编译单元测试 HAP | `python3 src/skills/ohproj/ohproj.py build-test /path/to/ohsonNativeProj46R` |
| 执行单元测试（部署并运行） | `python3 src/skills/ohproj/ohproj.py test /path/to/ohsonNativeProj46R` |
| 执行测试（指定超时毫秒） | `python3 src/skills/ohproj/ohproj.py test /path/to/project --timeout 120000` |
| 清除签名 | `python3 src/skills/ohproj/ohproj.py clean-sign /path/to/project` |
| **snapshot_record / MP4（系统镜像）** | 见 **第十节**；`python3 src/skills/ohrecord/ohrecord.py <子命令>` |

---

## 四、创建原生应用项目（详细步骤）

当用户需要「完整创建并接入 NAPI + 测试」时，按下列步骤执行（或由 AI 按步骤生成代码）。

### 4.1 步骤一：拷贝模板并修改命名与 bundleName

- **模板路径**：`src/skills/ohhap/NativeProj46R`
- **目标路径**：`src/skills/ohproj/<命名>NativeProj46R`
- **bundleName**：`ohos.<命名小写>.nativeproj46r`（如 `arkcJson` → `ohos.arkcjson.nativeproj46r`）
- **修改文件**：`AppScope/app.json5`、`autosign/UnsgnedReleasedProfileTemplate.json` 中的 `bundleName` / `bundle-name`

### 4.2 步骤二：拷贝用户代码目录并加入 CMake

- 将用户指定目录（如 `cJSON-master`）拷贝到项目的 `entry/src/main/cpp/` 下。
- 在 `entry/src/main/cpp/CMakeLists.txt` 中增加 `include_directories` 与 `add_library` 中的源文件。

### 4.3 步骤三：NAPI 与 Index.d.ts、ArkTS 调用

- 在 `napi_init.cpp` 中实现 C 接口的 NAPI 封装并注册到 exports。
- **G.PRE.02-CPP（用函数代替函数式宏）**：注册 `napi_property_descriptor` 时**不要**使用 `#define NAPI_METHOD_ENTRY(...)` 等**类函数宏**填充结构体；应使用 **`static` 函数**（如模板 **`templates/cjson/napi_init.cpp`** 中的 `MakeNapiMethodEntry(const char* utf8name, napi_callback method)`）返回与宏展开等价的描述符，满足规范并便于类型检查与单步调试。
- 在 `entry/src/main/cpp/types/libentry/Index.d.ts` 中声明 TypeScript 接口。
- 同步更新 `entry/oh_modules/libentry.so/Index.d.ts`（与 types 一致），避免编译使用旧声明。
- 在 `Index.ets` 中为变量添加**显式类型**（避免 arkts-no-any-unknown）。

**重要注意——须导出原有代码的全体接口**：以接入代码的头文件为准（如 cJSON.h 中所有 `CJSON_PUBLIC` 声明的接口），必须在 `napi_init.cpp` 中**全部**实现 NAPI 封装，并在 `Index.d.ts` 中**全部**声明，不得只实现或声明部分接口。若只导出部分接口，会导致应用层或测试无法调用未导出接口，且与“完整对接原有 C/C++ API”的目标不符。创建项目时请先对照头文件逐项核对，确保每个公开接口都有对应的 NAPI 与 .d.ts 声明。

**宏 / 结构体 / 枚举的导出约定**：C 头文件中的宏、结构体、枚举**不**在 .d.ts 中“原样”导出；详见本目录下 **NAPI_EXPORT_CONVENTIONS.md**。宏的取值通过 NAPI 常量 getter（如 `sqlite3Const*`）或 .d.ts 字面常量体现；结构体对应为句柄类型（如 `Sqlite3Handle = number`）；枚举取值按宏处理或使用 TS 枚举/常量。

### 4.4 步骤四：测试用例与 List.test.ets

- 新增 `*dts.test.ets`，在 `List.test.ets` 中 import 并注册测试套件。

**重要注意——单元测试须覆盖所有导出接口**：为每个通过 NAPI 导出的接口编写至少一个测试用例，测试用例需**覆盖所有**在 Index.d.ts 中声明的接口，不得遗漏。若只对部分接口写测试，未覆盖的接口在后续修改中容易引入回归且难以发现。创建项目时请根据 Index.d.ts 的导出列表逐项编写或补充测试，确保每个接口都有对应测试。

**每接口至少三类用例（强制）**：每个导出接口须具备至少 **3 种**测试用例，便于按接口统计覆盖、回归与可读性。命名与含义见 **4.6** 及本目录下 **TEST_CASE_DESIGN.md**。

### 4.6 设计/实现测试用例的规范与步骤（与 DESIGN 六、6.9–6.10 对应）

编写或补全 NAPI 单元测试时，应遵循 **entry/src/ohosTest/ets/test** 下既有用例（如 Indexdts.test.ets、Cjsondts.test.ets）与 **DESIGN.md 第六节「单元测试设计规范与方法」**及**测试数据要求（6.9）、补全清单（6.10）**，以及本技能 **「每接口至少三类用例」** 约定（详见 **TEST_CASE_DESIGN.md**）：

1. **结构**：使用 `describe('SuiteName', () => { ... })` 与 `it('caseName', TEST_FILTER, () => { ... })`；按需使用 beforeAll/beforeEach/afterEach/afterAll。
2. **命名（三类用例，必须沿用）**：每个接口至少 3 条用例，用例名须带明确后缀，便于按接口统计是否满足「至少 3 类」：
   - **正常功能**：`apiName_normal_<场景或结果>`（如 `sqlite3Open_normal_memory_returns_handle`）
   - **边界值**：`apiName_boundary_<条件>`（如 `sqlite3Open_boundary_empty_path`、`sqlite3Exec_boundary_empty_sql`）
   - **返回值**：`apiName_return_value_<类型或含义>`（如 `sqlite3Open_return_value_handle_type`、`sqlite3Close_return_value_is_number`）
   - 可选兼容旧写法：`apiName_<scenario>`、`apiName_<inputOrCondition>_<expected>`，但补全时优先使用上述三类命名。
3. **常量**：从 **constant.ets** 引入 TEST_FILTER、HILOG_DOMAIN、VAL_*、NEG_*、INVALID_HANDLE（若已定义）等，避免魔数。
4. **AAA 与清理**：Arrange（准备输入）→ Act（调用 NAPI）→ Assert（expect(...).assertEqual(...)）；对拥有的 handle 在用例末尾调用 lib.xxxDelete(h) 等做资源清理；已转移所有权的 item 勿重复 Delete。
5. **显式类型**：变量与返回值写明类型（如 `const h: number`、`const out: string | null`），满足 ArkTS 规范。
6. **覆盖类型**：每个导出接口至少一条**正向**用例；**且**至少一条**边界**（空串、空数组、下标边界、无效 handle 等）与至少一条**返回值**（类型、范围、rc 等）用例，使该接口满足「正常 / 边界 / 返回值」三类。参考 cJSON 源码 tests/misc_tests.c 的 null/非法输入设计。
7. **可追溯**：每个 it 内可用 hilog.info(HILOG_DOMAIN, 'testTag', '%{public}s', 'caseName') 打与用例名一致的日志。
8. **补全清单**：新增 NAPI 接口后，在对应 *dts.test.ets 中按上述规范增加 it（**至少 3 条**：normal、boundary、return_value），无需改 List.test.ets（套件已统一注册）；并对照 Index.d.ts 检查是否还有未覆盖的接口或未满 3 类的接口，补齐用例。

**测试数据要求**（详见 DESIGN 6.9）：  
- 不使用文件 IO，输入用**内联字符串/常量**；数值与句柄无效值用 **constant.ets**（VAL_*、NEG_*、INVALID_HANDLE）。  
- 同一接口多种等价输入（如 Compare 对 string/number/null/array/boolean）应**分用例**覆盖；打印类补零、负数等典型值；Minify 补「去空白、保留内容」断言。  
- 与 C 侧测试的差异与补全建议见 **CJSONDTS_comparison.md**，C 侧测试设计见 **cJSON_tests_design.md**。

**创建项目与补全测试时的自检**：请对照 **KNOWN_ISSUES_AND_AVOIDANCE.md** 第三节「创建项目时的检查清单」，避免编译失败（uv_cwd、oh_modules 缺失、CMake 未配）、测试失败（mock 未关、Indexdts 类型错误、DetachItemViaPointer 逻辑）、以及用例数量与设计文档不一致。

### 4.5 步骤五：单元测试使用真实 NAPI（必做，避免 CjsondtsTest 等失败）

模板中 `entry/src/mock/mock-config.json5` 会将 `libentry.so` 映射到 mock 实现（`Libentry.mock.ets` 仅实现 `add`）。若测试用例（如 `*dts.test.ets`）中调用了 NAPI 的其他接口（如 `cjsonVersion`、`cjsonParse` 等），运行时会加载 mock 而非主 HAP 中的真实 .so，未在 mock 中实现的接口为 **undefined**，导致报错 **"undefined is not callable"**，整组用例失败。

**正确做法**：在接入 NAPI 并编写调用该 NAPI 的单元测试后，必须**关闭对 libentry.so 的 mock**，让测试运行时加载主 HAP 中的真实 native 模块：

- 修改 **`entry/src/mock/mock-config.json5`**，清空对 `libentry.so` 的映射（使用空对象 `{}`），例如：
  ```json5
  {
  }
  ```
- 不要保留类似 `"libentry.so": { "source": "src/mock/Libentry.mock.ets" }` 的配置。

这样执行 `build-test` → `sign` → `test` 时，设备会加载主 HAP 中的真实 libentry.so，所有 NAPI 测试用例即可通过。若未做此步，仅 mock 中的接口（如 `add`）能通过，其余接口会报 "undefined is not callable"。

---

## 五、输出示例

### 5.1 创建项目

```
创建项目: arkcJson
  模板: .../NativeProj46R -> .../ohproj/arkcJsonNativeProj46R
  bundleName: ohos.arkcjson.nativeproj46r
  已修改 AppScope/app.json5、autosign/UnsgnedReleasedProfileTemplate.json
✓ 项目已创建: .../arkcJsonNativeProj46R
  后续: 接入代码、NAPI、Index.d.ts、测试用例 见 SKILL 步骤 4.2–4.4
```

### 5.2 编译

```
================================================================================
检查编译环境...
================================================================================
✓ HarmonyOS Command Line Tools 路径: <你的 Command Line Tools 目录>
✓ OpenHarmony SDK 路径: <你的 ohos-sdk 目录>
...
================================================================================
开始构建 HAP...
================================================================================
工作目录: <napi_generator 仓库根>/src/skills/ohproj/arkcJsonNativeProj46R
执行清理...
执行构建...
✓ HAP 构建成功！
================================================================================
检查生成的 HAP 文件...
找到 1 个 HAP 文件:
  1. entry/build/default/outputs/default/entry-default-unsigned.hap
主要 HAP 文件: entry/build/default/outputs/default/entry-default-unsigned.hap
```

### 5.3 签名

```
================================================================================
开始 HAP 签名流程...
================================================================================
✓ 项目 bundleName: ohos.arkcjson.nativeproj46r
✓ 未签名的 HAP 文件: .../entry/build/default/outputs/default/entry-default-unsigned.hap
步骤 1: 创建 autosign 目录...
...
步骤 8: 验证应用包签名...
  ✓ 验证成功: entry-default-signed.hap
✓ HAP 签名流程完成！
  签名的 HAP 文件: .../entry/build/default/outputs/default/entry-default-signed.hap
```

### 5.4 编译测试用例

```
================================================================================
开始构建测试 HAP...
================================================================================
工作目录: <你的 HAP 工程根目录>
...
✓ 测试 HAP 构建成功！
  测试 HAP: entry/build/default/outputs/default/entry_test-default-unsigned.hap
```

### 5.5 执行测试用例

执行前需已 build、build-test、sign，且设备已连接。

```
卸载已安装应用...
安装主 HAP...
安装测试 HAP...
执行 aa test...
✓ 部署运行测试完成: /path/to/ohsonNativeProj46R
```

若部分用例（如 UI 测试）报 "App died"，可为环境或已知问题；可关注 ActsAbilityTest、自定义 *dts 测试套件等结果。

---

## 六、路径与文件参考

| 用途 | 路径或文件 |
|------|------------|
| 模板工程 | `src/skills/ohhap/NativeProj46R` |
| 生成项目目录 | `src/skills/ohproj/<命名>NativeProj46R` |
| 编译/签名/编译测试脚本 | `src/skills/ohhap/hapbuild.py` |
| 执行测试脚本 | `src/skills/ohhdc/ohhdc.py`（deploy-test） |
| 系统 SA / 镜像产物与设备诊断（可选） | `src/skills/ohservices/ohsa.py`；说明见 **ohservices/SKILL.md** |
| 未签名主 HAP | `entry/build/default/outputs/default/entry-default-unsigned.hap` |
| 已签名主 HAP | `entry/build/default/outputs/default/entry-default-signed.hap` |
| 测试 HAP（未签名/已签名） | `entry/build/default/outputs/ohosTest/entry-ohosTest-unsigned.hap` / `entry-ohosTest-signed.hap` |
| NAPI 与 TS 声明 | `entry/src/main/cpp/napi_init.cpp`、`entry/src/main/cpp/types/libentry/Index.d.ts`、`entry/oh_modules/libentry.so/Index.d.ts` |
| 单元测试 mock 配置 | `entry/src/mock/mock-config.json5`（NAPI 测试须取消对 libentry.so 的 mock，见 4.5） |
| 设计文档与代码规范 | `src/skills/ohproj/DESIGN.md` |
| 测试用例三类命名与设计约定 | `src/skills/ohproj/TEST_CASE_DESIGN.md` |
| NAPI 宏/结构体/枚举导出约定 | `src/skills/ohproj/NAPI_EXPORT_CONVENTIONS.md` |
| 常见问题与避免指南 | `src/skills/ohproj/KNOWN_ISSUES_AND_AVOIDANCE.md` |

---

## 七、提示词与输出约定

- **提示词**：用户可说「用 ohproj 创建/编译/签名」「使用技能编译/签名 @项目名」「编译单元测试并执行」「使用技能编译这个项目的单元测试并执行」。
- **输出**：执行命令后给出简要结论（成功/失败）及产物路径；若失败，摘录关键报错便于排查。
- **执行测试流程**：通常顺序为 `build` → `build-test` → `sign`（对主 HAP 与测试 HAP 均签名）→ `test`；`test` 会先卸载再安装主 HAP 与测试 HAP，然后执行 `aa test`。
- **NAPI 单元测试失败**：若 CjsondtsTest 等报 "undefined is not callable"，检查 `entry/src/mock/mock-config.json5` 是否仍对 `libentry.so` 做了 mock；按步骤 4.5 清空该配置后重新 build-test、sign、test。
- **导出与测试范围**：用户要求“导出某头文件的 CJSON_PUBLIC/全部公开接口”时，须导出**所有**该头文件中的公开接口（napi_init.cpp + Index.d.ts 全量对应），且单元测试须**覆盖所有**已导出接口，**每个接口至少 3 类用例**（正常/边界/返回值），命名沿用 **TEST_CASE_DESIGN.md**（见步骤 4.3、4.4、4.6）。
- **设计文档与代码规范**：详见本目录下 **DESIGN.md**（NAPI 封装约定、ArkTS/测试代码规范、已知问题与修复）。
- **常见问题与避免**：创建/编译/测试前可参考 **KNOWN_ISSUES_AND_AVOIDANCE.md**，避免编译 uv_cwd、@ohos/hypium 缺失、mock 未关、用例不足、DetachItemViaPointer 等逻辑错误再次发生。

---

## 八、测试报告格式

执行 `ohproj.py test <项目目录>` 后，设备通过 Hypium 输出测试报告，主要包含以下内容。解析时可按 **测试套件（class）** 与 **用例（test）** 两级查看执行情况。

### 8.1 报告结构概览

- **OHOS_REPORT_SUM: N** — 当前输出的测试套件包含的用例数量（或套件数，依 Hypium 版本）。
- **OHOS_REPORT_STATUS: class=SuiteName** — 测试套件名称（如 `ActsAbilityTest`、`CjsondtsTest`）。
- **OHOS_REPORT_STATUS: current=M** — 当前执行到的用例序号（从 1 开始）。
- **OHOS_REPORT_STATUS: numtests=K** — 当前运行计划中的总用例数。
- **OHOS_REPORT_STATUS: test=CaseName** — 当前执行的测试用例名称（如 `assertContain`、`cjsonParse_valid_json_returns_handle`）。
- **OHOS_REPORT_STATUS_CODE: 0** — 该用例**通过**。
- **OHOS_REPORT_STATUS_CODE: -2** — 该用例**失败**；通常伴随 **OHOS_REPORT_STATUS: stream=** 错误信息及 **stack=** 堆栈。
- **OHOS_REPORT_STATUS: consuming=T** — 该用例耗时（毫秒）。
- **OHOS_REPORT_RESULT: stream=Tests run: R, Failure: F, Error: E, Pass: P, Ignore: I** — 汇总：总运行 R，失败 F，错误 E，通过 P，忽略 I。
- **OHOS_REPORT_CODE: -1** — 表示存在失败或错误（F 或 E > 0 时）。
- **TestFinished-ResultCode: 0** / **TestFinished-ResultMsg: ...** — 测试跑完的退出信息。

### 8.2 按套件与用例解读

| 含义 | 报告行示例 |
|------|------------|
| 套件开始 | `OHOS_REPORT_STATUS: class=CjsondtsTest` |
| 用例名称 | `OHOS_REPORT_STATUS: test=cjsonVersion_returns_string` |
| 用例通过 | 该 test 后出现 `OHOS_REPORT_STATUS_CODE: 0` |
| 用例失败 | 该 test 后出现 `OHOS_REPORT_STATUS_CODE: -2`，且常有 `stream=...`、`stack=...` |
| 套件耗时 | `OHOS_REPORT_STATUS: suiteconsuming=T` |
| 全局汇总 | `OHOS_REPORT_RESULT: stream=Tests run: 63, Failure: 0, Error: 0, Pass: 63, Ignore: 0` |

### 8.3 典型输出片段

```
OHOS_REPORT_SUM: 1
OHOS_REPORT_STATUS: class=ActsAbilityTest
OHOS_REPORT_STATUS: current=1
OHOS_REPORT_STATUS: numtests=63
OHOS_REPORT_STATUS: test=assertContain
OHOS_REPORT_STATUS_CODE: 1
OHOS_REPORT_STATUS_CODE: 0
OHOS_REPORT_STATUS: consuming=14

OHOS_REPORT_SUM: 62
OHOS_REPORT_STATUS: class=CjsondtsTest
OHOS_REPORT_STATUS: test=cjsonVersion_returns_string
OHOS_REPORT_STATUS_CODE: 0
...
OHOS_REPORT_RESULT: stream=Tests run: 63, Failure: 0, Error: 0, Pass: 63, Ignore: 0
OHOS_REPORT_CODE: -1
TestFinished-ResultCode: 0
TestFinished-ResultMsg: your test finished!!!
```

**说明**：若某用例失败，在报告中搜索 `OHOS_REPORT_STATUS_CODE: -2`，其前的 `test=CaseName` 即为失败用例名，`stream=` 为断言或错误信息；可根据 DESIGN.md 中的代码规范与已知问题排查（如 mock 配置、AddItemToObjectCS 键生命周期、assertContain 替代写法等）。

---

## 九、关联技能：ohservices / ohsa.py（系统 SystemAbility 与设备诊断）

本技能（**ohproj**）面向 **ArkTS + NAPI 应用工程**（HAP 编译、签名、`aa test`）。**ohservices** 技能与脚本 **`ohsa.py`** 面向**同仓库内**的 **sampletest 等 SystemAbility 样例**与**系统镜像产物/设备侧**排查，二者职责不同，可按需组合使用。

### 9.1 何时使用 ohsa.py

| 场景 | 说明 |
|------|------|
| 已烧录 **rk3568 等**系统镜像，需确认 **sampletest** 进程 / profile / init | `ohsa.py device`、`device-files`、`diag` |
| 需查 **落盘 hilog** 中 Publish、SELinux、hidumper 关键字 | `ohsa.py hilog-disk` |
| 需查 **dmesg** 中 init/execv/secon | `ohsa.py dmesg` |
| 验证 **hidumper -s 9009** | `ohsa.py hidumper`（或 `--hidumper-name Sampletest`） |
| 仅验证 **out 目录下**是否已编出 sampletest 的 so/profile/cfg | `ohsa.py build`（默认 `out/rk3568`，可用 `--product` / `--out`） |

### 9.2 命令示例（在**源码根**或任意目录执行，建议绝对路径）

```bash
# 综合诊断：设备上 /system 文件 + 进程 + 落盘 hilog 摘要 + dmesg（需 hdc 已连接）
python3 <napi_generator 仓库根>/src/skills/ohservices/ohsa.py diag

# 多设备指定序列号（等价 hdc -t）
python3 <napi_generator 仓库根>/src/skills/ohservices/ohsa.py -t 192.168.x.x:8710 diag

# 仅检查本机编译产物是否包含 sampletest（不连设备）
python3 <napi_generator 仓库根>/src/skills/ohservices/ohsa.py build --product rk3568

# 与 ohproj 测试衔接：应用测完后在同一设备上查系统侧日志
python3 <napi_generator 仓库根>/src/skills/ohproj/ohproj.py test /path/to/xxxNativeProj46R
python3 <napi_generator 仓库根>/src/skills/ohservices/ohsa.py hilog-disk
```

### 9.3 文档与完整子命令

- **完整说明与参数**：`src/skills/ohservices/SKILL.md`（「本技能脚本 ohsa.py」小节）。
- **全流程指南**：`src/skills/ohservices/saguide.md`。

---

## 十、snapshot_record 屏幕录制 MP4（系统侧改动与 ohrecord）

本节记录 **`snapshot_record`** 通过 **AVScreenCapture / CAPTURE_FILE** 在设备上输出 **MP4** 的完整工程说明：实现思路、涉及路径、编译与烧录、设备准备、验证与调试、已遇问题与解决方案。**固化的命令行操作**请优先使用 **`src/skills/ohrecord/ohrecord.py`**（见 **10.8**）；本节为权威说明文档。

### 10.1 背景与目标

- **目标**：在 **开发者模式** 下，使用系统命令 **`snapshot_record`** 将默认显示内容录制为 **MP4**，文件由 **媒体服务进程** 创建与写入，路径需满足 **SELinux** 与 **策略类型** 要求。
- **关键点**：客户端仅传 **绝对路径**；**服务端 `InitRecorder`** 在 **无 IPC 传入 fd** 时对路径执行 **`open(O_RDWR|O_CREAT|O_TRUNC)`**；避免 **`fd://` + Binder `WriteFileDescriptor`** 在部分 native 调用链上失败导致 **`Init` 提前失败、`Release` 表现为 IPC 错误**。

### 10.2 架构与数据流（简述）

1. **`snapshot_record`**（window_manager 部件）构造 **`AVScreenCaptureConfig`**，`recorderInfo.url` 为 **`/data/test/media/xxx.mp4`**，申请 **NativeToken**（含 **`ohos.permission.CAPTURE_SCREEN`** 等）后 **`ScreenCapture::Init` → `StartScreenRecording`**。
2. **`ScreenCaptureImpl`**（player_framework 客户端）：若 url 为 **`fd://`**，走 **`SetOutputFile` + SetRecorderInfo**；若为 **绝对路径**，仅 **SetRecorderInfo**，由服务端打开文件。
3. **`ScreenCaptureServer::InitRecorder`**（player_framework 服务端）：当 **`outputFd_ < 0`** 且 url **非 `fd://` 前缀** 时，在 **media_service** 进程内 **`open` 路径** 再交给 **Recorder**。
4. **SELinux**：`media_service` **不得** 对通用 **`data_file:file`** 随意 **`create/write`**（易触发 **`domain.te` neverallow**）。**`/data/test/media(/.*)?`** 在 **`file_contexts`** 中标记为 **`data_test_media_file`**；**`media_service.te`** 授予对该类型 **dir/file** 的 **`create/write/...`** 及 **`data_test_file:dir`** 的 **`search`**（进入测试目录树）。

### 10.3 修改文件清单（路径与原因）

| 路径 | 修改原因 |
|------|----------|
| `foundation/multimedia/player_framework/frameworks/native/screen_capture/screen_capture_impl.cpp` | **`InitCaptureFile`**：区分 **`fd://` 与绝对路径**；路径模式不再依赖客户端 **`SetOutputFile` 传 fd**，避免 Binder 传 fd/dup 失败。 |
| `foundation/multimedia/player_framework/services/services/screen_capture/server/screen_capture_server.cpp` | **`InitRecorder`**：无有效 fd 且非 **`fd://`** 时 **服务端 `open` 输出路径**；失败打 **`errno`** 日志（如 **EACCES=13**）。 |
| `foundation/multimedia/player_framework/services/services/screen_capture/ipc/screen_capture_service_proxy.cpp` | **`WriteFileDescriptor`** 返回值校验，与 recorder 等代理一致，避免静默失败。 |
| `foundation/window/window_manager/snapshot/src/snapshot_record.cpp` | 使用 **绝对路径** 填配置；注释说明由 **媒体服务** 打开文件。 |
| `foundation/window/window_manager/snapshot/src/snapshot_record_utils.cpp` | **`VALID_RECORD_PATH=/data/test/media`**；**`FillCaptureFileConfig`** 等与 **服务端 open + SELinux 类型** 对齐；路径 **`realpath`** 校验。 |
| `foundation/window/window_manager/snapshot/include/snapshot_record_utils.h` | 配置填充接口注释与路径约定一致。 |
| `foundation/window/window_manager/snapshot/BUILD.gn` | **`snapshot_record`** 可执行文件依赖 **media_client** 等（既有）；确认 **`install_enable`** 使二进制进系统镜像。 |
| `base/security/selinux_adapter/sepolicy/ohos_policy/multimedia/player/system/media_service.te` | 增加 **`data_test_file:dir`** 与 **`data_test_media_file`** 的 **allow**；**不** 放宽 **`data_file:file` 随意写**（避免 neverallow）。 |
| `base/security/selinux_adapter/sepolicy/ohos_policy/multimedia/player/system/file_contexts` | **`/data/test/media(/.*)?` → `data_test_media_file`**（若已存在则保持；与本方案一致即可）。 |

### 10.4 编译与输出物确认（开发步骤）

1. **环境**：OpenHarmony 标准编译环境；源码根目录含 **`build.sh`**。
2. **全量编译（示例 rk3568）**：
   ```bash
   cd <源码根>
   ./build.sh --product-name rk3568
   ```
   或使用：`python3 src/skills/ohrecord/ohrecord.py build --product rk3568`
3. **本机确认媒体库含路径 open 逻辑**（编译完成后）：
   ```bash
   python3 src/skills/ohrecord/ohrecord.py verify-host-so --product rk3568
   ```
   在 **`out/<product>/.../libmedia_service.z.so`** 的 **`strings`** 中应出现：**`InitRecorder open output by file path (no IPC fd)`**。
4. **镜像产物**：烧写对应产品的 **system** 等分区后，设备上应存在 **`/system/bin/snapshot_record`**；**`libmedia_service.z.so`** 常见路径为 **`/system/lib/`**（或 **`lib64`**，视产品架构）。

### 10.5 部署步骤（烧录与设备准备）

1. **烧录** 包含上述改动的镜像（与日常版本流程相同）。
2. **开发者模式**：`param get const.security.developermode.state` 为 **true**（否则 **`snapshot_record`** 会直接退出）。
3. **录制目录与 SELinux 标签**（测试步骤 **必做**）：
   ```bash
   mkdir -p /data/test/media
   chmod 777 /data/test/media
   chcon u:object_r:data_test_media_file:s0 /data/test/media
   ```
   或使用：`python3 src/skills/ohrecord/ohrecord.py prep-device`
4. **原因**：手工 **`mkdir`** 的目录常被标为 **`data_file`**，`media_service` **`open(O_CREAT)`** 会 **拒绝（errno 13, EACCES）**，客户端表现为 **`StartScreenRecording` 失败 ret=331350054**，hilog 见 **`InitRecorder open path failed, errno:13`**。**`chcon`** 为 **`data_test_media_file`** 后与 **`file_contexts`** 一致，录制可成功。

### 10.6 运行命令与运行产物确认（测试步骤）

**多设备**时指定：`hdc -t <序列号>` 或 **`OHRECORD_HDC_TARGET`**。

| 步骤 | 命令 |
|------|------|
| 列出设备 | `hdc list targets` 或 `python3 src/skills/ohrecord/ohrecord.py targets` |
| 设备状态 | `python3 src/skills/ohrecord/ohrecord.py device-status` |
| 验证设备 so | `python3 src/skills/ohrecord/ohrecord.py verify-device-so` |
| 录制 60 秒 | `python3 src/skills/ohrecord/ohrecord.py record -s 60 -f /data/test/media/rk_demo_60s.mp4` |
| 设备上校验文件 | `python3 src/skills/ohrecord/ohrecord.py verify-remote-mp4 -r /data/test/media/rk_demo_60s.mp4` |
| 拉取到 PC | `python3 src/skills/ohrecord/ohrecord.py pull -r /data/test/media/rk_demo_60s.mp4` |

**产物属性**：成功时文件属主多为 **`media:media_rw`**；文件头含 **`ftyp`**（如 **`ftypmp42`**）；体积随码率与时长变化。

**等价手工命令示例**：

```bash
snapshot_record -s 60 -f /data/test/media/rk_demo_60s.mp4
hdc file recv /data/test/media/rk_demo_60s.mp4 ./
```

### 10.7 调试与验证命令（问题排查）

| 现象 / 目的 | 命令 |
|-------------|------|
| ScreenCapture / InitRecorder 详情 | `hilog -x \| grep -iE 'ScreenCaptureServer\|InitRecorder\|StartScreenCaptureFile\|open path failed'` |
| 一键拉尾部（脚本） | `python3 src/skills/ohrecord/ohrecord.py hilog-capture` |
| 目录 **SELinux** 上下文 | `ls -ldZ /data/test/media`（应为 **`data_test_media_file`**） |
| **AVC**（内核拒绝） | `dmesg \| grep avc`（关注 **`media_service`** 与 **`/data/test`**） |
| 关闭 hilog 流控（可选） | `param set hilog.flowctrl.proc.on false` |
| 临时确认是否 SELinux 导致 | **`setenforce 0` 仅用于定位**；量产应修 **策略/标签**，勿依赖 Permissive。 |

**典型错误码**：**331350054** 在本流程中曾与 **`InitRecorder` 失败** 同时出现；结合 hilog 中 **`errno`** 判断是 **权限/SELinux** 还是其他 I/O。

### 10.8 ohrecord.py 子命令汇总（固化操作）

在源码根或任意目录执行（自动推断 **`OHOS_SRC`** 或通过 **`--src`** 指定）：

| 子命令 | 作用 |
|--------|------|
| `paths` | 打印关键源文件路径与 **§10.3** 对应关系 |
| `build --product <名>` | **`./build.sh --product-name`** |
| `prep-device` | 设备 **`mkdir/chmod/chcon`** |
| `device-status` | 开发者模式、**SELinux**、目录 **ls -Z** |
| `verify-host-so` | 本机 **out** 下 **libmedia_service.z.so** 特征串 |
| `verify-device-so` | 设备 **.so** 特征串 |
| `record -s N -f <设备绝对路径>` | 执行 **snapshot_record** |
| `pull -r <远程路径> [-l 本地路径]` | **hdc file recv**，默认 **`ohrecord/recv/`** |
| `verify-remote-mp4 -r <路径>` | 设备上 **ls/wc/xxxd** |
| `hilog-capture [--tail N]` | 过滤 **ScreenCapture** 相关 hilog |
| `targets` | **hdc list targets** |

### 10.9 已遇问题与解决方案（小结）

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **`StartScreenRecording` ret=331350054**，无 MP4 | **`InitRecorder open` 失败，errno=13（EACCES）** | 将 **`/data/test/media`** 标为 **`data_test_media_file`**（**`chcon`/`restorecon`**），避免仅为 **`data_file`** |
| 策略编译 **neverallow** | 对 **`data_file:file`** 放开 **create/write** | **仅** 使用 **`data_test_media_file` + 固定路径**，不改 **`domain.te`** 禁止项 |
| **Binder / IPC** 异常、Init 很早失败 | **`fd://` 传 fd** 在部分 native 路径不稳定 | **路径模式**：客户端不传 fd，**服务端 open**（见 **§10.2**） |
| **`hdc` 多设备** | 未指定 target | **`hdc -t`** 或 **`OHRECORD_HDC_TARGET`** |

### 10.10 代码与策略规范（延续 ohproj 原则）

- 修改保持与周边一致的 **日志宏、错误码检查、注释风格**；不扩大无关重构。
- **SELinux**：新增 **allow** 须有 **file_contexts** 与 **type** 支撑；避免 **neverallow** 冲突。
- **测试**：以 **真机 + Enforcing** 下 **`/data/test/media`** 成功生成 **MP4** 为准；**`strings` 特征串**作为镜像是否包含新逻辑的辅助证据。

**相关技能**：**ohhdc**（通用 HDC）、**ohservices/ohsa.py**（**dmesg**、落盘 **hilog**、系统部件诊断）。
