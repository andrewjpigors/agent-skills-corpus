---
name: btl-api
description: "操作 BlueprintTextLanguage Remote Control API。使用场景：调用 ExportToText 导出蓝图/资产内容、调用 TriggerLiveCoding 触发编译、调用 BuildAssetCache 重建资产索引、调用 AddVariable 向蓝图添加变量、调用 AddFunctionFromJson 通过 JSON 节点图生成函数（支持 entry/sequence/print/branch/call/spawn/getvar/setvar/cast/customevent/self/return/foreach/interfacecall/event）、调用 AddFunctionParam 添加函数参数签名、调用 AddEventGraphNodeFromJson 向事件图写入节点、调用 RemoveFunction/RenameFunction 删除或重命名函数、调用 RemoveVariable/SetVariableDefault 删除或修改变量默认值、调用 SetVariableMetadata/SetVariableExposeOnSpawn 修改变量元数据、调用 CreateBlueprint/AddInterface/ClearBlueprint 管理蓝图生命周期、调用 DeleteAsset/DuplicateAsset/MoveAsset 管理资产、调用 SearchClass/SearchFunction 搜索可用类和函数、调用 AddComponent/SetComponentProperty/GetComponentProperty/RemoveComponent 管理蓝图组件、调用 AddEventGraphNodeFromJson 绑定组件委托事件（VarName.DelegateName 格式）、调用 ClearEventGraphByEvent 清除指定事件连接的节点、调用 RemoveOrphanNodes 清除孤立节点、分析导出文本内容。包含调用示例和返回格式说明。"
argument-hint: "要操作的资产路径或 API 动作，例如：/Game/BP/MyBlueprint 或 compile"
---

# BTL Remote Control API 技能

## 概述

通过 HTTP Remote Control API 向运行中的 UE 编辑器发送指令，调用 `UBTLManager` 上的静态函数。

**服务地址**：`http://localhost:30010`（UE 编辑器运行时监听）  
**目标对象**：`/Script/BlueprintTextLanguage.Default__BTLManager`

---

## API 接口

### 1. ExportToText — 导出资产为文本

将指定资产导出为结构化文本，支持蓝图、数据资产、字符串表等所有主要资产类型。导出结果同时缓存到 `[ProjectSaved]/BlueprintTextLanguage/` 目录（镜像资产路径，扩展名 `.btl`）。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"ExportToText","parameters":{"BlueprintPath":"<资产路径>"},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue  # true = 成功
# $r.OutText 包含完整文本，但建议通过缓存文件读取以避免终端溢出
```

**注意**：`OutText` 返回值可能非常大，直接在终端打印会导致卡顿。建议通过缓存文件读取：
```powershell
# 导出后读取缓存文件（资产路径 /Game/BP/Foo → Game/BP/Foo.btl）
Get-Content "[ProjectSaved]/BlueprintTextLanguage/Game/BP/Foo.btl" -TotalCount 60
```

**资产路径格式**：UE 内容浏览器路径，不含扩展名，例如：
- `/Game/BP/Characters/BP_Player`
- `/Game/Config/InputMapping/UI/IMC_Main`
- `/Game/Data/DA_SomeConfig`

**支持的资产类型及输出格式**：

| 资产类型 | UE 类 | 输出节段 |
|---------|-------|---------|
| 普通蓝图 | `UBlueprint` | 头信息 → 接口 → 变量 → 组件 → CDO → 函数 → 事件图 → Lua |
| 动画蓝图 | `UAnimBlueprint` | 头信息 → 变量 → 函数 → 事件图 → 动画图 → Lua |
| 控件蓝图 | `UWidgetBlueprint` | 头信息 → 变量 → 控件树 → 动画 → 函数 → 事件图 → Lua |
| 蓝图接口 | `UBlueprint(Interface)` | 头信息 → 接口函数签名 |
| 宏库 | `UBlueprint(MacroLibrary)` | 头信息 → 宏定义 |
| 函数库 | `UBlueprint(FunctionLibrary)` | 头信息 → 变量 → 函数 → Lua |
| LevelSequence | `ULevelSequence` | 头信息 → 轨道列表 |
| UserDefinedStruct | `UUserDefinedStruct` | 头信息 → 字段列表 |
| DataTable | `UDataTable` | 头信息 → 行列表 |
| UserDefinedEnum | `UUserDefinedEnum` | 头信息 → 枚举值列表 |
| DataAsset | `UDataAsset` | 头信息 → Properties 节段 |
| StringTable | `UStringTable` | 头信息 → Entries 节段（按 Key 排序） |

**输出格式约定**：

| 符号 | 含义 |
|------|------|
| `== Section ==` | 一级节标题（Interfaces / Variables / Functions / Event Graphs 等） |
| `--- Name ---` | 二级子节（单个函数 / 单个事件 / 单行数据） |
| `[N] NodeID \| Title` | 蓝图节点，NodeID 为引擎内部名 |
| `[>] pin -> Target.pin` | 执行输出引脚 → 目标节点 |
| `[<e] pin` | 执行输入引脚 |
| `[<] pin = value` | 数据输入引脚（默认值） |
| `[<] pin -> Target.pin` | 数据输入引脚（连线） |
| `[~] pin -> Target.pin` | 数据输出引脚（连线） |
| `- Name \| Type \| Default \| Category` | 变量 / 属性条目（管道符分隔字段） |

**普通蓝图输出示例**：
```
== Blueprint ==
Name: BP_Player
Path: /Game/BP/BP_Player.BP_Player
Type: Normal Blueprint
Parent: Actor | native

== Interfaces ==
- UnLuaInterface

== Variables ==
- Health | float | 100.0 | Default
- Speed | float | 600.0 | Movement

== Components ==
- DefaultSceneRoot | SceneComponent | root
- Mesh | StaticMeshComponent | DefaultSceneRoot

== CDO Overrides ==

== Functions ==
--- MyFunc ---
[N] K2Node_FunctionEntry_0 | MyFunc
  [>] then -> K2Node_CallFunction_0.execute
[N] K2Node_CallFunction_0 | 打印字符串
  [<e] execute -> K2Node_FunctionEntry_0.then
  [>] then
  [<] InString = Hello

== Event Graphs ==
--- 事件开始运行 ---
[N] K2Node_Event_0 | 事件开始运行
  [>] then
```

---

### 2. TriggerLiveCoding — 触发 Live Coding 编译

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"TriggerLiveCoding","parameters":{},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue  # true = 编译成功（必须读取，不可跳过）
$r.OutResult    # "Success" / "NoChanges" / "Failure" 等
```

> **核心规则：编译结果一律以 `$r.ReturnValue` 返回值为准。**
> - `ReturnValue: true` → **编译成功**，无论 `OutResult` 是 `Success` 还是 `NoChanges`，均表示代码已生效，**不得再次触发编译**，直接进入后续验证。
> - `ReturnValue: false` → **编译失败**，必须读取 UBT 日志定位错误后修复。
> - **禁止跳过返回值检查**：每次调用 `TriggerLiveCoding` 后必须读取并判断 `$r.ReturnValue`，不可仅凭 HTTP 状态码或 `OutResult` 文本判断。

**编译结果枚举**（`OutResult` — 仅供参考，以 `ReturnValue` 为准）：
- `Success` — 本次触发了编译且成功
- `NoChanges` — 编译已在后台完成，无新增改动（ReturnValue 仍为 true）
- `Failure` — 编译失败
- `InProgress` — 编译仍在进行
- `ModuleNotLoaded` — Live Coding 模块未加载

> **`NoChanges` 的含义**：UHT 检测到 `.h` 文件中新增了 `UFUNCTION` / `UPROPERTY` 等宏声明时，
> 会在后台**自动触发一次 Live Coding 编译**生成新的 patch 文件。
> 此后手动调用 `TriggerLiveCoding` 时，LiveCoding 认为已无待编译改动，返回 `NoChanges`（`ReturnValue: true`）。
> 这是**正常且正确**的结果——说明代码已生效，**不需要重复编译**，直接进行后续验证即可。

**编译失败时的处理规范**：

`ReturnValue: false` 时，**必须先读取 UBT 日志定位实际错误，禁止凭猜测修改代码**。

```powershell
# 读取最后 40 行，通常包含全部 error 信息
Get-Content "<EngineRoot>\Engine\Programs\UnrealBuildTool\Log.txt" | Select-Object -Last 40
```

日志中查找 `error` 关键字：
```powershell
Get-Content "<EngineRoot>\Engine\Programs\UnrealBuildTool\Log.txt" | Select-String "error" | Select-Object -Last 20
```

**错误定位规则**：
- 日志中的 `error CXXXX:` 行包含出错的文件路径和行号 → 直接定位问题代码
- 看 `note:` 行理解类型不匹配的具体原因
- 将完整错误文本作为上下文，再决定修复方案
- 确认有明确修复思路后，方可改动代码并再次编译

**Live Coding 限制 — 需要全量重编译的场景**：

> Live Coding 仅能 patch **UCLASS 标注类**的成员函数体变更。以下场景 **Live Coding 无法生效**，
> 必须提醒用户**关闭 UE 编辑器**后通过 IDE 全量编译（或用 `UnrealBuildTool` 命令行构建）：
>
> | 改动类型 | 示例 |
> |---------|------|
> | 非 UCLASS 纯 C++ 类的方法改动 | `FBTLExporterBase::TraverseFromNode()`、`FBTLNode::PrintToLog()` |
> | struct / class 字段增删 | 向 `FBTLNode` 添加 `TArray<FString> ImportMeta` |
> | 新增全局 / 静态函数 | 新增 `static void Foo()` 并在已有函数中调用 |
> | `.h` 中类布局变更 | 改变继承关系、虚函数表结构 |
>
> **判断方法**：若 `TriggerLiveCoding` 返回 `ReturnValue: true`（`Success` 或 `NoChanges`）但新逻辑未生效，
> 说明改动的类不在 Live Coding patch 范围内，**必须全量重编译**。

---

### 3. BuildAssetCache — 重建资产索引缓存

遍历项目 Content、Source、Plugins 目录，生成两个缓存文件。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"BuildAssetCache","parameters":{},"generateTransaction":false}'
Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
```

**输出文件**（位于 `[ProjectSaved]/BlueprintTextLanguage/`）：
- `cache_uasset.json` — 所有 `.uasset` / `.umap` 路径列表
- `cache_source.json` — 所有 `.h` / `.cpp` 路径列表
- `Game/<Path>/<AssetName>.btl` — ExportToText 导出缓存（自动创建）

---

### 4. AddVariable — 向蓝图添加成员变量

向指定蓝图添加一个新的成员变量，添加后自动重编译并持久化保存。

```powershell
# 基础类型（TypeExtra 可省略）
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddVariable","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"MyCount","VarType":"int","DefaultValue":"0","TypeExtra":"","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因

# objectref（TypeExtra = 目标类路径）
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddVariable","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"EnemyRef","VarType":"objectref","DefaultValue":"","TypeExtra":"/Game/BP/BP_Enemy","OutError":""},"generateTransaction":false}'

# array<int>（TypeExtra = 内层类型）
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddVariable","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"Scores","VarType":"array","DefaultValue":"","TypeExtra":"int","OutError":""},"generateTransaction":false}'

# map<string, int>（TypeExtra = 'keyType|valueType'）
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddVariable","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"NameToScore","VarType":"map","DefaultValue":"","TypeExtra":"string|int","OutError":""},"generateTransaction":false}'
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径，格式同 ExportToText |
| `VarName` | string | 新变量名，与已有变量重名时返回 false |
| `VarType` | string | 变量类型（见下表） |
| `DefaultValue` | string | 默认值字符串，空字符串表示使用类型零值（objectref/enum/struct/array/set/map 通常留空） |
| `TypeExtra` | string | 扩展类型信息（见下表说明），基础类型留空即可 |
| `OutError` | string | 输出：失败时包含错误描述 |

**支持的变量类型**：

| 类型字符串 | 蓝图类型 | TypeExtra |
|-----------|---------|-----------|
| `int` | int32 | — |
| `int64` | int64 | — |
| `bool` | bool | — |
| `float` | float | — |
| `string` | FString | — |
| `name` | FName | — |
| `text` | FText | — |
| `objectref` | 对象引用（UObject*） | 目标类路径（`AActor`、`/Game/BP/BP_Enemy`、`/Script/Engine.Actor`） |
| `enum` | 枚举引用 | 枚举路径（如 `/Script/Engine.ENetRole`） |
| `struct` | 结构体引用 | 结构体路径（如 `/Script/CoreUObject.Vector`） |
| `array` | TArray | 内层基础类型（`int`/`bool`/`float`/`string`/`name`/`text`/`int64`） |
| `set` | TSet | 内层基础类型（同 array） |
| `map` | TMap | `'keyType\|valueType'`，例如 `'string\|int'` |

**添加后自动执行顺序**：
1. `FBlueprintEditorUtils::AddMemberVariable` 添加变量定义
2. `FKismetEditorUtilities::CompileBlueprint` 重编译蓝图
3. `UPackage::SavePackage` 持久化保存

**验证方式**：调用 `ExportToText` 后在 `== Variables ==` 节段确认新变量，输出格式举例：
- `- MyCount | int32 |  | Default`
- `- EnemyRef | ZeroSecondTestActor_C* |  | Default`
- `- Scores | TArray<int32> |  | Default`
- `- NameToScore | TMap<FString, int32> |  | Default`

---

### 5. AddFunctionFromJson — 通过 JSON 描述向蓝图添加函数

通过 JSON 描述的节点图，向指定蓝图添加新函数。支持节点类型：`sequence` / `print` / `branch` / `call`。节点坐标由 BFS 自动布局分配（x 步长 350，y 步长 200）。

```powershell
$graphJson = '{"nodes":[{"id":"seq","type":"sequence"},{"id":"p0","type":"print","message":"Line 0"},{"id":"p1","type":"print","message":"Line 1"}],"links":[{"from":"entry","fromPin":"then","to":"seq","toPin":"execute"},{"from":"seq","fromPin":"then_0","to":"p0","toPin":"execute"},{"from":"seq","fromPin":"then_1","to":"p1","toPin":"execute"}]}'
$esc = $graphJson -replace '\\', '\\\\' -replace '"', '\"'
$body = "{`"objectPath`":`"/Script/BlueprintTextLanguage.Default__BTLManager`",`"functionName`":`"AddFunctionFromJson`",`"parameters`":{`"BlueprintPath`":`"/Game/Foo/BP_Bar`",`"FuncName`":`"MyFunc`",`"GraphJson`":`"$esc`"},`"generateTransaction`":false}"
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `FuncName` | string | 函数名，与已有函数重名时返回 false |
| `GraphJson` | string | 节点图 JSON，含 `nodes` 和 `links` 数组 |
| `OutError` | string | 输出：失败时包含错误描述 |

**节点类型速查**：

| type | 对应 K2 节点 | 专属字段 |
|------|------------|----------|
| `entry` | `UK2Node_FunctionEntry`（固定 id `"entry"`，自动注册） | — |
| `sequence` | `UK2Node_ExecutionSequence` | — |
| `print` | `KismetSystemLibrary::PrintString` | `message`（写入 InString） |
| `branch` | `UK2Node_IfThenElse` | — |
| `call` | `UK2Node_CallFunction` | `class`、`func`、`pins` |
| `spawn` | `UK2Node_SpawnActorFromClass` | `class`（目标 Actor 类路径） |
| `getvar` | `UK2Node_VariableGet` | `var`（变量名，须预先存在于蓝图） |
| `setvar` | `UK2Node_VariableSet` | `var`（变量名，须预先存在于蓝图） |
| `cast` | `UK2Node_DynamicCast` | `class`（目标类：C++ 类名带或不带前缀均可，如 `AActor`/`Actor`/`ACharacter`，或蓝图路径如 `/Game/BP/BP_Player`） |
| `customevent` | `UK2Node_CustomEvent` | `name`（事件显示名） |
| `self` | `UK2Node_Self` | — （输出蓝图自身引用，输出引脚名为 `self`，可连接到 `cast` 的 `Object` 引脚） |
| `return` | `UK2Node_FunctionResult` | `pins`（返回值引脚默认值） |
| `foreach` | `UK2Node_MacroInstance`（ForEachLoop） | — （从 StandardMacros 宏库加载 ForEachLoop 宏图） |
| `interfacecall` | `UK2Node_CallFunction`（接口消息调用） | `class`（接口路径或类名）、`func`（函数名） |
| `event` | `UK2Node_Event`（内置事件 override 入口） | `name`（事件函数名，如 `ReceiveBeginPlay`）、`class`（可选，事件所属类，默认蓝图父类） |

**注意事项**：
- `entry` 节点无需在 `nodes` 中声明，直接在 `links` 中用 `"from":"entry"` 引用即可
- `sequence` 的 then 引脚数量由 `links` 中该节点的输出连线数自动决定，无需手动指定
- `print` 的 `message` 字段会直接覆盖 `InString` 默认值（`"Hello"`）
- `cast` 的执行出口引脚名为 `then`（成功）和 `CastFailed`（失败）
- `cast` 的 `Object` 输入引脚**必须连接**具体对象，否则蓝图编译报"类型尚未确定"错误；可通过 `self` 节点（`{"id":"s","type":"self"}`）输出蓝图自身引用并连接到 `Object` 引脚；**注意**：cast 目标类不应是 self 所属类的父类或同类（如蓝图继承自 Actor，不能 cast to Actor），应使用子类或无继承关系的类（如 `ACharacter`）
- `cast` 的数据输出引脚名（转换结果）**依赖 UE 编辑器本地化语言**（如中文环境下为 `"As静态网格体组件"` 而非 `"AsStatic Mesh Component"`）。在 JSON links 中使用**任意以 `"As"` 开头的名称**即可，系统会自动通过 `GetCastResultPin()` 回退匹配，无需关心本地化名称

  ```powershell
  # 示例：self → Cast To Character（向下转型，目标类为 self 的子类或无关类）
  $graphJson = '{"nodes":[{"id":"s","type":"self"},{"id":"c","type":"cast","class":"ACharacter"}],"links":[{"from":"entry","fromPin":"then","to":"c","toPin":"execute"},{"from":"s","fromPin":"self","to":"c","toPin":"Object"}]}'
  ```
- `call` 的 `class` 支持省略 `U` 前缀（`KismetSystemLibrary` 等效于 `UKismetSystemLibrary`）
- **纯函数（BlueprintPure / const 方法）无执行引脚**：`GetComponentByClass`、`GetActorLocation`、`MakeTransform` 等 `const` 方法或标记为 `BlueprintPure` 的函数**没有 `execute`/`then` 执行引脚**，仅有数据输入/输出引脚。在 JSON links 中**不要**将执行链连接到纯函数节点，否则连线会静默失败。可通过 `SearchFunction` 返回的 `pure` 字段判断函数是否为纯函数
- `spawn` 的 `ReturnValue` 引脚在连线时可直接引用，类型在 `ReconstructNode` 后更新为目标 Actor 类；`SpawnTransform` 是 by-ref 必填引脚，**不连接会产生蓝图编译错误**，需提供（例如通过 `MakeTransform` 节点或变量）
- `getvar` / `setvar` 的 `var` 值须与蓝图中已存在变量名完全一致（区分大小写）；输出引脚名即为变量名
- **对象引用引脚默认值**：`pins` 中若引脚类型为对象引用（如 `UStaticMesh*`、`UClass*`），直接传入资产路径字符串即可（如 `"/Engine/BasicShapes/Sphere.Sphere"`），系统会自动通过 `StaticLoadObject` 加载对象并设置 `Pin->DefaultObject`
- **接口实现图复用**：若 `FuncName` 与已有接口实现占位图同名，`AddFunctionFromJson` 会自动复用该图（清空非入口节点）并填充新逻辑，无需手动删除占位图
- `event` 节点用于在事件图中创建内置事件 override 入口（如 `ReceiveBeginPlay`、`ReceiveTick`）。如果图中已存在同名 override 事件，**自动复用现有节点**而非创建重复项。`name` 字段为事件函数名，`class` 字段可选（默认使用蓝图父类）

  ```powershell
  # 示例：在事件图中添加一个 ReceiveEndPlay 事件入口并连接 PrintString
  $graphJson = '{"nodes":[{"id":"ep","type":"event","name":"ReceiveEndPlay"},{"id":"p0","type":"print","message":"Game Over"}],"links":[{"from":"ep","fromPin":"then","to":"p0","toPin":"execute"}]}'
  ```

**验证方式** — ExportToText 输出示例（2 条消息）：
```
--- MyFunc ---
[N] K2Node_FunctionEntry_0 | MyFunc
  [>] then -> K2Node_ExecutionSequence_0.execute
[N] K2Node_ExecutionSequence_0 | 序列
  [>] then_0 -> K2Node_CallFunction_0.execute
  [>] then_1 -> K2Node_CallFunction_1.execute
[N] K2Node_CallFunction_0 | 打印字符串
  [<] InString = Line 0
[N] K2Node_CallFunction_1 | 打印字符串
  [<] InString = Line 1
```

---

### 6. AddFunctionParam — 向蓝图函数添加参数引脚

向指定函数添加输入参数（bIsOutput=false）或返回值引脚（bIsOutput=true）。参数类型与 `AddVariable` 保持相同的字符串约定。

```powershell
# 添加输入参数 Health (float)
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddFunctionParam","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","FuncName":"MyFunc","ParamName":"Health","ParamType":"float","bIsOutput":false,"OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因

# 添加返回值引脚 Result (bool)
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddFunctionParam","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","FuncName":"MyFunc","ParamName":"Result","ParamType":"bool","bIsOutput":true,"OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `FuncName` | string | 目标函数名（FunctionGraphs 或接口实现图均支持） |
| `ParamName` | string | 参数名，不可重复 |
| `ParamType` | string | 类型字符串：int / int64 / bool / float / double / string / name / text |
| `bIsOutput` | bool | false = 输入参数，true = 返回值引脚 |

**注意事项**：
- 函数必须已由 `AddFunctionFromJson` 创建再调用本接口
- 返回值引脚会自动创建缺失的 FunctionResult 节点
- 引脚名与参数名相同（区分大小写）

---

### 7. AddEventGraphNodeFromJson — 向事件图写入节点

向蓝图事件图表（EventGraph）插入节点。`EventName` 支持内置事件（如 BeginPlay）或自定义事件名，找不到时自动创建自定义事件节点。

```powershell
# 向 BeginPlay 图写入一个 PrintString
$graphJson = '{"nodes":[{"id":"p0","type":"print","message":"Hello from BeginPlay"}],"links":[{"from":"entry","fromPin":"then","to":"p0","toPin":"execute"}]}'
$esc = $graphJson -replace '\\', '\\\\' -replace '"', '\"'
$body = "{`"objectPath`":`"/Script/BlueprintTextLanguage.Default__BTLManager`",`"functionName`":`"AddEventGraphNodeFromJson`",`"parameters`":{`"BlueprintPath`":`"/Game/Foo/BP_Bar`",`"EventName`":`"BeginPlay`",`"GraphJson`":`"$esc`"},`"generateTransaction`":false}"
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError
```

**参数说明**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `EventName` | string | 事件名：内置事件支持后缀匹配（BeginPlay 匹配 ReceiveBeginPlay）；自定义事件精确匹配名称 |
| `GraphJson` | string | 节点图 JSON，格式与 AddFunctionFromJson 相同 |

**节点类型**：支持 AddFunctionFromJson 的全部节点类型（sequence/print/branch/call/spawn/getvar/setvar/cast/customevent）。`entry` 自动指向指定的事件节点。

**常用 EventName 对应表**：

| 用户传入 | 匹配的内置函数名 |
|---|---|
| `BeginPlay` | `ReceiveBeginPlay` |
| `Tick` | `ReceiveTick` |
| `EndPlay` | `ReceiveEndPlay` |
| 自定义事件名 | 精确匹配，未找到则自动创建 |

---

### 7.5. ClearEventGraphByEvent — 清除指定事件的连接节点

清除事件图中指定事件入口连接的所有节点，**保留事件节点本身**。用于重写某个事件的逻辑前先清理旧节点，避免孤立残留。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"ClearEventGraphByEvent","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","EventName":"BeginPlay","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `EventName` | string | 事件名（同 AddEventGraphNodeFromJson 的匹配规则） |

**行为说明：**
1. 查找指定事件节点（支持后缀匹配 BeginPlay → ReceiveBeginPlay）
2. BFS 遍历事件节点连接的所有可达节点
3. 断开所有连线后逐一删除可达节点，**保留事件节点本身**
4. 重编译并保存蓝图

**典型用法** — 先清除后重建：
```powershell
# 1. 清除旧的 BeginPlay 逻辑
ClearEventGraphByEvent(BP, "BeginPlay")
# 2. 写入新的 BeginPlay 逻辑
AddEventGraphNodeFromJson(BP, "BeginPlay", $newGraphJson)
```

---

### 7.6. RemoveOrphanNodes — 删除事件图中所有孤立节点

一键清除事件图中所有不可从任何事件入口到达的孤立节点。用于批量清理历史残留。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RemoveOrphanNodes","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |

**行为说明：**
1. BFS 从所有 `UK2Node_Event` 出发，收集可达节点集合
2. 收集所有不可达且非编译器系统节点的孤立节点
3. 断开连线后逐一删除
4. 有节点被删除时才重编译并保存

**验证方式：** 调用 `ExportToText` 后检查是否还有 `--- 孤立节点 ---` 节段。

---

### 7.7. ArrangeEventGraph — 整理事件图布局

重新整理蓝图事件图的节点布局。按事件分组、BFS 深度排列、纵向堆叠，消除所有重叠。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"ArrangeEventGraph","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |

**布局规则：**
1. 收集所有事件入口（UK2Node_Event / UK2Node_CustomEvent / UK2Node_ComponentBoundEvent）
2. 按优先级排序：BeginPlay → Tick → EndPlay → Overlap → Hit → 其他内置 → 自定义事件 → 组件委托事件
3. 对每个事件 BFS 收集连通子图，按链路深度分配 X 坐标（步长 350），同深度按行分配 Y 坐标（步长 200）
4. 子图间纵向堆叠，间距 150px

**典型用法：** 在多次 `AddEventGraphNodeFromJson` 后调用，一次性整理所有事件节点布局。

---

### 8. RemoveFunction — 删除蓝图函数

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RemoveFunction","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","FuncName":"OldFunc","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `FuncName` | string | 要删除的函数名 |

---

### 9. RenameFunction — 蓝图函数重命名

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RenameFunction","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","OldFuncName":"OldName","NewFuncName":"NewName","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue
$r.OutError
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `OldFuncName` | string | 原函数名 |
| `NewFuncName` | string | 新函数名（不可与已有函数重名） |

---

### 10. RemoveVariable — 删除蓝图变量

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RemoveVariable","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"OldVar","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue
$r.OutError
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 要删除的变量名 |

---

### 11. SetVariableDefault — 修改蓝图变量默认值

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SetVariableDefault","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"MyCount","NewDefaultValue":"42","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue
$r.OutError
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 目标变量名 |
| `NewDefaultValue` | string | 新的默认值字符串 |

> **注意**：修改默认值仅更新蓝图元数据，不触发完整重编译。CDO 默认值将在蓝图下次编译时生效。

---

### 12. RenameVariable — 重命名蓝图变量

重命名成员变量，引擎内部自动同步更新所有引用该变量的 GetVar/SetVar 节点。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RenameVariable","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","OldVarName":"OldName","NewVarName":"NewName","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `OldVarName` | string | 原变量名（区分大小写） |
| `NewVarName` | string | 新变量名（不可与已有变量重名） |

---

### 13. AddInterface — 向蓝图添加接口继承

向指定蓝图添加接口继承，支持原生 C++ 接口（`/Script/...` 路径）和蓝图接口（`/Game/...` 路径），添加后自动重编译并持久化保存。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddInterface","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","InterfacePath":"/Script/UnLua.UnLuaInterface","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 目标蓝图路径，格式同 ExportToText |
| `InterfacePath` | string | 接口类路径（见下方说明） |
| `OutError` | string | 输出：失败时包含错误描述 |

**InterfacePath 格式：**

| 接口类型 | 路径格式 | 示例 |
|---------|---------|------|
| 原生 C++ 接口 | `/Script/<模块名>.<类名>` | `/Script/UnLua.UnLuaInterface` |
| 蓝图接口 | `/Game/...`（同 ExportToText 路径） | `/Game/Interfaces/BPI_MyInterface` |

**已知常用接口路径：**
- UnLua 接口：`/Script/UnLua.UnLuaInterface`

**行为说明：**
1. 加载接口类（原生接口直接 `LoadObject<UClass>`；蓝图接口加载 `UBlueprint` 后取 `GeneratedClass`）
2. 检查目标类是否是 `UInterface` 派生类
3. 检查是否已经实现该接口（重复添加返回 false）
4. 调用 `FBlueprintEditorUtils::ImplementNewInterface` 添加接口并生成空实现占位图
5. `FKismetEditorUtilities::CompileBlueprint` 重编译
6. `UPackage::SavePackage` 持久化保存

**验证方式：** 调用 `ExportToText` 后在 `== Interfaces ==` 节段确认接口名称出现。

```
== Interfaces ==
- UnLuaInterface
```

---

### 14. RemoveInterface — 移除蓝图已实现的接口

移除蓝图的接口实现，同步删除接口函数占位图，重编译并保存。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RemoveInterface","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","InterfacePath":"/Script/UnLua.UnLuaInterface","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `InterfacePath` | string | 接口类路径（同 AddInterface） |

---

### 15. ClearBlueprint — 清空蓝图所有用户内容

删除蓝图中所有用户创建的函数图、成员变量和接口继承，重新编译并持久化保存。常用于在重新构建蓝图内容前的清理操作。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"ClearBlueprint","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar"},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 目标蓝图路径，格式同 ExportToText |
| `OutError` | string | 输出：失败时包含错误描述 |

**行为说明：**
1. 遍历所有 `FunctionGraphs`，逐一调用 `FBlueprintEditorUtils::RemoveGraph` 删除用户函数图
2. 遍历所有 `NewVariables`，逐一调用 `FBlueprintEditorUtils::RemoveMemberVariable` 删除成员变量
3. 遍历所有 `ImplementedInterfaces`，逐一调用 `FBlueprintEditorUtils::RemoveInterface` 取消接口继承
4. `FKismetEditorUtilities::CompileBlueprint` 重编译，`UPackage::SavePackage` 持久化保存

> **注意**：系统保留图（`UserConstructionScript`、`EventGraph` 等）不属于 `FunctionGraphs`，不会被删除。

---

### 15.5. CreateBlueprint — 创建新蓝图资产

在指定路径创建新的蓝图资产。支持多种蓝图类型。

```powershell
# 创建普通 Actor 蓝图
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"CreateBlueprint","parameters":{"AssetPath":"/Game/BP/BP_NewActor","ParentClassName":"","BlueprintTypeStr":"actor","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功

# 创建 WidgetBlueprint
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"CreateBlueprint","parameters":{"AssetPath":"/Game/UI/WBP_MyWidget","ParentClassName":"","BlueprintTypeStr":"widgetblueprint","OutError":""},"generateTransaction":false}'
```

**参数说明：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `AssetPath` | string | 新蓝图的资产路径（不含扩展名） |
| `ParentClassName` | string | 自定义父类名（可选，空字符串使用类型默认父类） |
| `BlueprintTypeStr` | string | 蓝图类型（见下表） |
| `OutError` | string | 输出：失败时包含错误描述 |

**支持的蓝图类型：**

| 类型字符串 | 默认父类 | 说明 |
|-----------|---------|------|
| `actor`（默认） | `AActor` | 普通 Actor 蓝图 |
| `functionlibrary` | `UBlueprintFunctionLibrary` | 函数库 |
| `interface` | `UInterface` | 蓝图接口 |
| `macrolibrary` | `AActor` | 宏库 |
| `widgetblueprint` | `UUserWidget` | 控件蓝图（UMG Widget） |

**ParentClassName 说明：**
- 留空使用类型默认父类
- 可传入 C++ 类名（如 `Character`、`Pawn`）或蓝图路径（如 `/Game/BP/BP_Base`）

---

### 16. SetVariableMetadata — 修改变量分类和提示文本

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SetVariableMetadata","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"Health","Category":"Combat","Tooltip":"角色当前生命值","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 目标变量名 |
| `Category` | string | 分类名（空字符串则不修改分类） |
| `Tooltip` | string | 提示文本（空字符串则不修改提示） |

---

### 17. SetVariableExposeOnSpawn — 控制变量生成时暴露

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SetVariableExposeOnSpawn","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"Health","bExpose":true,"OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 目标变量名 |
| `bExpose` | bool | true = 在 SpawnActor 时暴露该变量，false = 取消暴露 |

---

### 18. DeleteAsset — 删除资产

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"DeleteAsset","parameters":{"AssetPath":"/Game/Foo/BP_ToDelete","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `AssetPath` | string | 要删除的资产路径 |

> **注意**：如果资产被其他资产引用，删除可能失败。

---

### 19. DuplicateAsset — 复制资产

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"DuplicateAsset","parameters":{"SourcePath":"/Game/Foo/BP_Source","DestPath":"/Game/Foo/BP_Copy","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `SourcePath` | string | 源资产路径 |
| `DestPath` | string | 目标资产路径（不可已存在） |

---

### 20. MoveAsset — 移动/重命名资产

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"MoveAsset","parameters":{"SourcePath":"/Game/Foo/BP_Old","DestPath":"/Game/Bar/BP_New","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `SourcePath` | string | 源资产路径 |
| `DestPath` | string | 目标资产路径（不可已存在） |

> **注意**：引擎会自动更新所有引用该资产的重定向器。

---

### 21. SearchClass — 按关键字搜索 UClass

模糊搜索引擎中已注册的所有 UClass，返回匹配的类信息列表。用于在构建节点图前查询可用类名和路径。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SearchClass","parameters":{"Keyword":"StaticMesh","MaxResults":10,"OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue | ConvertFrom-Json | ConvertTo-Json -Depth 3
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `Keyword` | string | 搜索关键字（大小写不敏感，匹配类名或显示名） |
| `MaxResults` | int32 | 最大返回数量（默认 50） |

**返回值**（JSON 数组字符串）：
```json
[
  {
    "name": "StaticMeshComponent",
    "path": "/Script/Engine.StaticMeshComponent",
    "parent": "MeshComponent",
    "blueprintType": true,
    "abstract": false
  }
]
```

---

### 22. SearchFunction — 按关键字搜索类的 BlueprintCallable 函数

搜索指定类（含继承链）上的所有 `BlueprintCallable` 函数，返回函数签名。用于查询可用的蓝图可调用函数。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SearchFunction","parameters":{"ClassName":"StaticMeshComponent","Keyword":"SetStaticMesh","MaxResults":10,"OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue | ConvertFrom-Json | ConvertTo-Json -Depth 5
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `ClassName` | string | 目标类名（支持 C++ 类名如 `Actor`/`StaticMeshComponent`，蓝图路径如 `/Game/BP/BP_Player`） |
| `Keyword` | string | 函数名关键字（大小写不敏感，空字符串返回所有 BlueprintCallable 函数） |
| `MaxResults` | int32 | 最大返回数量（默认 50） |

**返回值**（JSON 数组字符串）：
```json
[
  {
    "name": "SetStaticMesh",
    "class": "StaticMeshComponent",
    "pure": false,
    "static": false,
    "event": false,
    "const": false,
    "params": [{"name": "NewMesh", "type": "UStaticMesh*", "out": false}],
    "returnType": "bool"
  }
]
```

**字段说明：**
- `pure`：是否为纯函数（无执行引脚，包含 `BlueprintPure` 和 `const` 方法）。**纯函数节点没有 `execute`/`then` 引脚，不能接入执行链**
- `const`：是否为 const 方法（C++ 层面的 const 标记）
- `static`：是否为静态函数
- `event`：是否为 BlueprintEvent（可重写事件）
- `params`：参数列表，每个参数含 name/type/out
- `returnType`：返回值类型（无返回值时不包含此字段）

---

### 23. AddComponent — 向蓝图添加组件

向 Actor 蓝图的 SimpleConstructionScript（SCS）添加新组件。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"AddComponent","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","ComponentClassName":"SphereComponent","VarName":"MySphere","ParentVarName":"","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `ComponentClassName` | string | 组件类名（支持带或不带 U 前缀，如 `SphereComponent` 或 `USphereComponent`） |
| `VarName` | string | 组件变量名（SCS 节点名称） |
| `ParentVarName` | string | 父组件变量名（空字符串则作为根节点添加） |

**常用组件类名：**
- `SphereComponent` — 球体碰撞
- `BoxComponent` — 盒体碰撞
- `CapsuleComponent` — 胶囊碰撞
- `StaticMeshComponent` — 静态网格
- `SceneComponent` — 空间变换
- `WidgetComponent` — UI 控件

---

### 24. SetComponentProperty — 修改组件模板属性

修改 SCS 组件模板上的属性值。支持基础类型（float/int/bool/string）和对象引用（资产路径）。

```powershell
# 设置基础属性
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SetComponentProperty","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"MySphere","PropertyName":"SphereRadius","PropertyValue":"200","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body

# 设置对象引用属性（如 StaticMesh）
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"SetComponentProperty","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"MyMesh","PropertyName":"StaticMesh","PropertyValue":"/Engine/BasicShapes/Cube.Cube","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 组件变量名 |
| `PropertyName` | string | 属性名（FProperty 名称） |
| `PropertyValue` | string | 属性值字符串（基础类型直接传值，对象引用传资产路径） |

> **对象引用属性**：若 ImportText 失败，会自动尝试通过 `StaticLoadObject` 加载对象引用（如 StaticMesh、Material 等）。

---

### 24.5. GetComponentProperty — 读取组件模板属性值

读取 SCS 组件模板上的属性，返回属性值字符串。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"GetComponentProperty","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"MySphere","PropertyName":"SphereRadius","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
$r.ReturnValue  # 属性值字符串，如 "32.000000"
$r.OutError     # 失败时说明原因
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 组件变量名 |
| `PropertyName` | string | 属性名（FProperty 名称） |

**返回值**：属性值的字符串表示（通过 `ExportTextItem_Direct` 导出）。对象引用属性返回资产路径。

---

### 25. RemoveComponent — 删除蓝图组件

删除 SCS 组件节点，子组件自动提升到父级。**同时自动清理所有关联的组件委托事件节点及其下游节点**。

```powershell
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"RemoveComponent","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","VarName":"MySphere","OutError":""},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
$r.ReturnValue  # true = 成功
```

**参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| `BlueprintPath` | string | 蓝图资产路径 |
| `VarName` | string | 要删除的组件变量名 |

---

### 组件委托事件绑定

`AddEventGraphNodeFromJson` 的 `EventName` 参数支持 `"组件变量名.委托名"` 格式，自动创建 `UK2Node_ComponentBoundEvent` 节点。

```powershell
# 绑定 SphereComponent 的 OnComponentBeginOverlap 事件
$graphJson = '{"nodes":[{"id":"p0","type":"print","message":"Overlap!"}],"links":[{"from":"entry","fromPin":"then","to":"p0","toPin":"execute"}]}'
$esc = $graphJson -replace '\\', '\\\\' -replace '"', '\"'
$body = "{`"objectPath`":`"/Script/BlueprintTextLanguage.Default__BTLManager`",`"functionName`":`"AddEventGraphNodeFromJson`",`"parameters`":{`"BlueprintPath`":`"/Game/Foo/BP_Bar`",`"EventName`":`"MySphere.OnComponentBeginOverlap`",`"GraphJson`":`"$esc`"},`"generateTransaction`":false}"
$r = Invoke-RestMethod -Method PUT -Uri 'http://localhost:30010/remote/object/call' -ContentType 'application/json' -Body $body
```

**EventName 格式：**

| 格式 | 示例 | 说明 |
|------|------|------|
| `BeginPlay` | 内置事件 | 后缀匹配 ReceiveBeginPlay |
| `MyCustomEvent` | 自定义事件 | 精确匹配或自动创建 |
| `VarName.DelegateName` | `MySphere.OnComponentBeginOverlap` | 组件委托事件（自动创建 UK2Node_ComponentBoundEvent） |

**常用组件委托：**
- `OnComponentBeginOverlap` — 重叠开始（UPrimitiveComponent）
- `OnComponentEndOverlap` — 重叠结束
- `OnComponentHit` — 碰撞命中
- `OnClicked` / `OnReleased` — 点击/释放

**ClearEventGraphByEvent 同样支持组件委托事件格式**，且会连同事件节点一起删除：
```powershell
# 清理组件委托事件及其所有下游节点
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"ClearEventGraphByEvent","parameters":{"BlueprintPath":"/Game/Foo/BP_Bar","EventName":"MySphere.OnComponentBeginOverlap","OutError":""},"generateTransaction":false}'
```

---

## 典型工作流

### 分析一个资产
```powershell
# 1. 导出资产文本
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"ExportToText","parameters":{"BlueprintPath":"/Game/BP/MyBlueprint"},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body

# 2. 查看文本
Write-Host $r.OutText
```

### 修改代码后验证编译
```powershell
# 触发编译（会等待完成）
$body = '{"objectPath":"/Script/BlueprintTextLanguage.Default__BTLManager","functionName":"TriggerLiveCoding","parameters":{},"generateTransaction":false}'
$r = Invoke-RestMethod -Method PUT -Uri "http://localhost:30010/remote/object/call" -ContentType "application/json" -Body $body
if ($r.ReturnValue) { Write-Host "编译成功: $($r.OutResult)" } else { Write-Host "编译失败: $($r.OutResult)" }
```

---

## 错误排查

| 现象 | 原因 | 解决方式 |
|------|------|---------|
| 连接拒绝 | UE 编辑器未启动或 Remote Control 未启用 | 启动 UE 编辑器，确认 `RemoteControl` 插件已启用 |
| `ReturnValue: false` | 资产路径不正确或资产未在编辑器中打开 | 检查路径格式；确保资产在编辑器中已打开 |
| `OutText` 为空 | 资产类型暂不支持 | 查看 BTLCommandlet.cpp 支持的 Cast<> 分发类型 |
| Live Coding 超时 | 编辑器未在前台 | 手动按 Ctrl+Alt+F11，或检查 UBT 日志 |

---

## 资产分析工作流

### 标准分析流程

```
1. ExportToText(主资产)
2. 识别所有引用（Lua路径、组件蓝图、父类、接口、DataAsset等）
3. 按"分析规则"决定哪些要递归导出
4. 对需要分析的依赖调用 ExportToText
5. 综合所有数据输出分析报告
```

### 依赖分析决策树

遇到引用时，按以下逻辑判断是否深入：

```
引用到某资产或路径？
├── Lua 脚本路径               → ✅ 读取文件内容，一并分析
├── 组件蓝图（*Component*）    → ✅ ExportToText，分析功能用途
├── 父类蓝图（Parent Class）   → ✅ ExportToText，理解继承链
├── 接口（Interface）          → ✅ ExportToText，列出接口契约
├── DataAsset / DataTable      → ✅ ExportToText，说明配置内容
├── StringTable                → ✅ ExportToText，列出文本条目
├── InputAction / IMC          → ✅ ExportToText，说明输入绑定
├── 子控件蓝图（WBP_*）
│   ├── 是功能核心子控件       → ✅ ExportToText
│   └── 纯布局/视觉子控件      → ⚠️ 简述用途，不导出
├── 特效（NS_* / PS_* / VFX）  → ❌ 仅说明"播放了某特效"
├── 声音（Cue / Wave）         → ❌ 仅说明"播放了某音效"
└── 材质 / 贴图                → ❌ 仅描述外观用途
```

### 递归深度控制

- **第 1 层**（主资产）：完整分析
- **第 2 层**（主资产的直接依赖）：完整分析
- **第 3 层**（依赖的依赖）：仅说明用途，**不再递归导出**

### Lua 文件读取

蓝图导出文本中若出现 Lua 模块路径：
```powershell
# Lua 文件通常位于项目 Content 目录下，后缀 .lua
$luaPath = "<ProjectRoot>\Content\Lua\<模块路径>.lua"
Get-Content $luaPath -Encoding UTF8
```

分析 Lua 时关注：
- `require` 引入的其他模块（视语境决定是否分析）
- 对 UE 方法的调用（`self:GetOwner()`、`UE4.UGameplayStatics`等）
- 与蓝图变量/函数的绑定关系
