---
name: craftengine-skill
version: 3.0.0
description: >-
  Generate CraftEngine plugin YAML configuration templates based strictly on the
  CraftEngine Wiki and CraftEngine Template content. Analyzes user needs,
  references the correct Wiki sections and Template examples, then generates one
  complete, validated configuration at a time. After generation, validates YAML
  syntax and cross-checks every field against the Wiki to prevent fabricated content.
  Asks the user for any uncertain decisions before proceeding, including whether
  to output the result in chat or save to a file.
  Triggered by: "生成CraftEngine配置", "CE模板生成", "写CraftEngine物品",
  "CraftEngine方块", "CraftEngine家具", "CraftEngine配方", "CraftEngine装备",
  "CE config", "craftengine template", "生成CE物品", "生成CE方块",
  "生成CE家具", "craftengine配置", "写CE配置", "CraftEngine自定义",
  "craftengine item", "craftengine block", "craftengine furniture",
  "CraftEngine高级配置", "CraftEngine农作物", "CraftEngine食物",
  "CraftEngine工具", "CraftEngine字体", "CraftEngine原版战利品",
  "CraftEngine世界生成", "CraftEngine配置合并", "CraftEngine翻译".
context: fork
agent: general-purpose
allowed-tools: Read Write Glob Grep Bash WebFetch
---

# CraftEngine Skill

## Purpose

根据用户需求，严格基于 Skill 内置的 **CraftEngine Wiki** 和 **CraftEngine Template** 内容，生成符合官方规范的 CraftEngine 插件 YAML 配置模板。每次只生成一个完整的配置（一个物品、一个方块、一个家具等），生成后校验 YAML 语法，并对照 Wiki 验证是否存在虚构内容。

## When to Use

- 用户需要创建 CraftEngine 插件的自定义配置（物品、方块、家具、配方、装备等）
- 用户不熟悉 CraftEngine 配置格式，需要一个模板作为起点
- 用户需要生成一个完整可用的 CraftEngine YAML 配置
- 用户需要校验已有的 CraftEngine 配置是否正确
- 用户需要了解某个 CraftEngine 功能的具体配置方式

## When NOT to Use

- 用户询问 CraftEngine 的概念性问题或插件安装 —— 引导用户阅读 Wiki 或 Template 的 README.md
- 用户需要批量生成多个配置 —— 要求每次只生成一个，多次调用本 Skill
- 用户需要修改项目中已有的配置而非生成新配置
- 需求与 CraftEngine 插件无关（其他 Minecraft 插件如 Oraxen、CustomCrops 等）

## Workflow / Steps

### Step 1: 分析用户需求

解析用户的输入，提取以下关键信息：

1. **配置类型**：用户需要生成什么类型的 CraftEngine 配置？
   - `item` — 物品（武器、工具、食物、消耗品、装饰品、方块物品、家具物品等）
   - `block` — 方块（基础方块、农作物、门、楼梯、存储方块等）
   - `furniture` — 家具（椅子、桌子、灯具、装饰家具等）
   - `recipe` — 配方（有序/无序合成、烧炼、锻造、酿造等）
   - `equipment` — 装备盔甲（组件型/纹饰型）
   - `category` — 物品分类
   - `loot_table` — 战利品表
   - `vanilla_loot` — 原版战利品覆盖（覆盖 Minecraft 原生方块/实体的战利品）
   - `jukebox_song` — 唱片机曲目
   - `painting` — 画
   - `image` — 图像
   - `emoji` — 表情
   - `sound` — 音效
   - `font` / `fonts` — 字体
   - `template` — 模板系统（含配置工厂）
   - `global_variable` — 全局变量
   - `lang` / `i18n` / `translations` — 语言/翻译
   - `config_merges` — 配置合并
   - `configured_feature` — 世界生成配置
   - `advanced` — 高级配置特性（节标识符 `#`、节分隔符 `::`、版本条件 `$$`、YAML 类型标签、子包）

2. **核心功能**：用户希望这个配置实现什么功能？
   - 例如：可放置的方块、可交互的家具、带特效的武器、可种植的作物等

3. **特殊要求**：是否有版本限制、命名空间要求、材质路径等

4. **不确定之处**：标记所有用户未明确但生成配置所需的信息

如果用户描述模糊，输出你的理解并向用户确认后再继续。

### Step 2: 查阅参考资料

根据 Step 1 判断的配置类型和核心功能，按以下规则查找对应的 Wiki 和 Template 参考文件：

#### Wiki 查阅规则

**物品 (item) 相关：**
- 基本物品配置 → `references/CraftEngine Wiki/configuration/item.md`
- 物品数据（名称/描述/组件/NBT） → `references/CraftEngine Wiki/configuration/item/data.md`
- 物品设置（燃料/标签/装备/弹射物/食物等） → `references/CraftEngine Wiki/configuration/item/settings.md`
- 物品行为（方块物品/家具物品/堆肥/范围挖掘等） → `references/CraftEngine Wiki/configuration/item/behaviors.md` + 对应子页面
- 物品模型（简化/condition/range_dispatch/composite 等 8 种） → `references/CraftEngine Wiki/configuration/item/models.md` + 对应子页面
- 物品更新器 → `references/CraftEngine Wiki/configuration/item/updater.md`

**方块 (block) 相关：**
- 方块基本配置 → `references/CraftEngine Wiki/configuration/block.md`
- 方块状态（单状态/多状态/属性/外观/变体） → `references/CraftEngine Wiki/configuration/block/states.md`
- 方块状态属性类型 → `references/CraftEngine Wiki/configuration/block/states/properties.md`
- 方块实体渲染器 → `references/CraftEngine Wiki/configuration/block/states/entity_renderer.md`
- 方块设置（硬度/音效/光照/工具等） → `references/CraftEngine Wiki/configuration/block/settings.md`
- 方块行为（生长/下落/门/存储/蔓延等） → `references/CraftEngine Wiki/configuration/block/behaviors.md` + 对应子页面
- 方块标签 → `references/CraftEngine Wiki/reference/block_tags.md`

**家具 (furniture) 相关：**
- 家具基本配置 → `references/CraftEngine Wiki/configuration/furniture.md`
- 家具设置（物品/击打次数/音效/挖掘工具） → `references/CraftEngine Wiki/configuration/furniture/settings.md`
- 家具变体（元素/判定箱/座椅/实体剔除） → `references/CraftEngine Wiki/configuration/furniture/variants.md`
- 家具行为（物品展示/发光/存储） → `references/CraftEngine Wiki/configuration/furniture/behaviors.md`

**配方 (recipe) 相关：**
- 配方全部类型（11 种） + 标签/分组/后处理器 → `references/CraftEngine Wiki/configuration/recipe.md`
- 外部物品来源兼容 → `references/CraftEngine Wiki/compatibility/external_item_sources.md`

**其他配置：**
- 装备盔甲 → `references/CraftEngine Wiki/configuration/equipment.md`
- 分类 → `references/CraftEngine Wiki/configuration/category.md`
- 战利品表 → `references/CraftEngine Wiki/reference/loot_table.md`
- 原版战利品覆盖 → `references/CraftEngine Wiki/configuration/vanilla_loot.md`
- 模板系统 → `references/CraftEngine Wiki/reference/template.md`
- 事件系统（46 种函数） → `references/CraftEngine Wiki/reference/events.md`
- 条件系统（28 种条件） → `references/CraftEngine Wiki/reference/conditions.md`
- 文本格式（MiniMessage + 附加标签） → `references/CraftEngine Wiki/reference/text_format.md`
- 数字格式（11 种） → `references/CraftEngine Wiki/reference/number_format.md`
- 链式参数 → `references/CraftEngine Wiki/reference/text_format/chain_arguments.md`
- 全局变量 → `references/CraftEngine Wiki/configuration/global_variable.md`
- 语言/翻译 → `references/CraftEngine Wiki/configuration/lang.md` + `references/CraftEngine Wiki/configuration/i18n.md` + `references/CraftEngine Wiki/configuration/translations.md`（如存在）
- 图像/表情 → `references/CraftEngine Wiki/configuration/image.md` + `references/CraftEngine Wiki/configuration/emoji.md`
- 唱片/音效 → `references/CraftEngine Wiki/configuration/jukebox_song.md` + `references/CraftEngine Wiki/configuration/sound.md`
- 画 → `references/CraftEngine Wiki/configuration/painting.md`
- 字体 → `references/CraftEngine Wiki/configuration/font.md`
- 文件冲突 → `references/CraftEngine Wiki/reference/file_conflict.md`
- 世界生成配置 → `references/CraftEngine Wiki/configuration/configured_feature.md`（如存在）
- 命令参考 → `references/CraftEngine Wiki/reference/commands.md`
- 高级配置特性（节标识符/节分隔符/版本条件/YAML类型标签） → `references/CraftEngine Wiki/configuration.md`（configuration.md 顶层文档）
- 兼容性（反Xray/ASP/Axiom/BlueMap/数据包/外部物品来源/MM/PAPI/QuickShop/Skript/Leveler/WorldPainter） → `references/CraftEngine Wiki/compatibility/` 对应子页面

#### Template 查阅规则

根据配置类型查找对应的 Template 参考：

**General 目录（完整模板参考，优先使用）：**
- 物品类：
  - `基础物品.yml` — 装饰物品/工具/燃料/方块物品
  - `物品设置.yml` — 全部 settings 选项
  - `物品行为.yml` — 全部 behavior 类型
  - `物品模型类型.yml` — 全部 8 种模型
  - `物品数据组件.yml` — 全部 data 组件
  - `武器.yml` — 剑/弓/弩/三叉戟
  - `工具.yml` — 范围挖掘/弹射物
  - `食物.yml` — 食物/消耗品
  - `消耗品与药水.yml` — 药水/消耗品
  - `音乐唱片.yml` — 唱片机物品
- 方块类：
  - `基础方块.yml` — 14 种方块示例
  - `方块设置.yml` — settings 完整
  - `方块标签.yml` — 标签配置
  - `方块实体渲染器.yml` — entity_renderer
  - `变化与蔓延.yml` — 氧化/扩散/衰变
  - `农作物与植物.yml` — 作物/茎/灌木/树苗
  - `物理机制方块.yml` — 下落/混凝土粉末/弹跳
  - `特殊机制方块.yml` — 可剥离/稳固基底/母岩
  - `展示与粒子效果.yml` — 展示/粒子
  - `朝向与液体交互.yml` — 定向/悬挂/液体
  - `门与红石方块.yml` — 门/活板门/栅栏/按钮
  - `楼梯台阶与多层方块.yml` — 楼梯/台阶/多层
  - `存储与座椅.yml` — 存储/抽屉/座椅
  - `灯与钟.yml` — 灯/可切换灯/震响
- 家具类：
  - `基础家具.yml` — 3 个完整家具示例
  - `家具行为.yml` — display_item/glowing/storage
- 配方类：
  - `配方.yml` — 全部 11 种配方+后处理器
- 装备类：
  - `盔甲套装.yml` — 组件型/纹饰型/3D 头盔
- 其他：
  - `高级配置特性.yml` — 节标识符 `#`、节分隔符 `::`、版本条件 `$$`、扩展值类型、子包
  - `分类配置.yml` — 分类菜单
  - `战利品表.yml` — 战利品表
  - `模板系统.yml` — template/config_factory
  - `事件与条件.yml` — 事件+条件
  - `语言配置.yml` — lang/i18n
  - `图像配置.yml` — image
  - `表情配置.yml` — emoji
  - `文本格式.yml` — MiniMessage 标签
  - `数字格式.yml` — 数字格式
  - `链式参数.yml` — chain arguments
  - `全局变量.yml` — global_variable
  - `物品更新器.yml` — updater
  - `文件冲突配置.yml` — file_conflict
  - `画配置.yml` — painting
  - `字体配置.yml` — font
  - `音乐唱片.yml` — jukebox_song（sound 配置参考 Wiki `configuration/sound.md`）

**Example 目录（可直接使用的完整示例）：**
- `物品/1. 基础材料与宝石.yml` 到 `物品/10. 物品行为完整示例.yml`
- `方块/1. 基础方块.yml` 到 `方块/9. 方块实体渲染器.yml`
- `家具/1. 基础家具.yml` + `家具/2. 家具行为.yml`
- `配方/1. 全部配方类型.yml`
- `装备/1. 盔甲套装.yml`
- `事件与条件/1. 事件函数完整示例.yml` + `2. 条件完整示例.yml`
- `其他配置/1. 图像与表情.yml` 到 `7. 文件冲突与字体与更新器.yml`
- `完整产业链/` — **完整产业链示例目录**，包含 70+ 个跨配置类型的综合示例（如 `6. 红石与机械产业链.yml`、`8. 存储与物流产业链.yml`、`10. 经济与交易产业链.yml`、`11. 音乐与音效产业链.yml`、`12. 世界生成与树木产业链.yml`、`15. 模板系统高级应用.yml`、`16. 农耕扩展产业链.yml`、`18. 便携工具产业链.yml`、`19. 酿造与饮品产业链.yml`、`22. 自定义工作台产业链.yml`、`24. 诅咒物品与进化产业链.yml`、`27. 容器与背包产业链.yml`、`30. 装备进阶升阶产业链.yml`、`31. 生物战利品专业化产业链.yml`、`32. 家具套装产业链.yml`、`35. 字体与表情产业链.yml`、`36. 物品更新升级产业链.yml`、`37. 分类菜单与UI组织产业链.yml`、`42. 物品模型高级展示产业链.yml`、`44. 座椅与社交家具产业链.yml`、`45. 定向放置与悬挂产业链.yml`、`47. 可剥离方块与木材加工产业链.yml`、`50. 语言与国际化产业链.yml`、`58. 物品品质与稀有度系统产业链.yml` 等），适合需要跨配置类型的综合参考场景

使用 `Read` 工具读取对应的 Wiki 页面和 Template 文件，将关键配置结构加载到上下文中。

#### 参考来源优先级规则

生成配置时，严格按照以下优先级使用参考来源：

1. **本地 CraftEngine Wiki**（`references/CraftEngine Wiki/`）— 最优先，默认使用
2. **本地 CraftEngine Template**（`references/CraftEngine Template/`）— 辅助参考
3. **官方在线文档**（[https://ce.gtemc.cn/zh-Hans/](https://ce.gtemc.cn/zh-Hans/)）— **仅在用户明确要求时才使用**

#### 在线文档使用规则

- **在用户明确说明要使用官方在线文档之前，绝对不要使用在线文档。** 始终优先使用本地文档。
- 如果遇到本地 Wiki 和 Template 中均未记载的功能或字段，且你觉得有必要查阅在线文档，**必须先向用户确认**是否搜索在线文档。
- 向用户确认时，必须说明：**在线文档可能因网络原因无法访问**。
- 如果用户同意使用在线文档，使用 `WebFetch` 或 `WebSearch` 工具获取在线文档内容。
- 如果在线文档无法访问（网络超时、404 等），**必须告知用户无法访问**，并询问用户是否仍要继续生成（此时告知用户缺少参考依据，配置可能有风险），或中止当前操作。

#### 验证规则

- 必须实际读取文件内容，不得仅凭文件名推断
- 同一功能同时读取 Wiki 和对应 Template 进行交叉验证
- 如果 Wiki 和 Template 对同一字段描述不一致，**以 Wiki 为准**
- 对于不确定的字段用法，查看 Wiki 中的具体示例确认
- 记录读取了哪些参考文件，供 Step 5 校验使用

### Step 3: 向用户确认不确定项

在生成配置之前，列出所有无法确定的信息并向用户提问。包括但不限于：

- **命名空间**（默认 namespace，建议用户提供）
- **物品/方块 ID**（需用户指定）
- **材质/模型路径**（需用户指定）
- **显示名称和描述文本**（需用户提供）
- **具体数值**（如耐久度、伤害值、烧炼时间等）—— 如果用户未指定，使用合理的默认值并标注
- **行为参数**（如方块行为的具体类型参数）
- **版本要求**（针对哪个 Minecraft 版本？默认使用最新）
- **付费版功能**：如果用户所需功能仅付费版支持，明确告知用户
- **在线文档查询**：如果本地 Wiki 和 Template 均无法满足需求，**向用户询问**是否尝试查阅官方在线文档（`https://ce.gtemc.cn/zh-Hans/`），同时说明在线文档可能因网络原因无法访问

#### 输出方式询问（新增）

**如果用户没有明确说明输出方式，必须向用户询问：**
- **对话中返回** — 配置以 YAML 代码块形式直接展示在对话中
- **输出到文件** — 使用 `Write` 工具将配置保存到项目目录下的指定位置

询问格式示例：
> 输出方式：你希望生成的配置以什么形式交付？
> 1. **对话中返回** — 直接展示 YAML 代码块，方便复制
> 2. **输出到文件** — 保存到项目目录，方便后续管理

如果用户选择了"输出到文件"，继续询问：
- 保存路径（默认：`plugins/CraftEngine/<对应子目录>/<id>.yml`）
- 文件名

**判断规则：**
- 用户说"保存""生成到""写到文件""输出到"等 → 视为选择"输出到文件"
- 用户说"展示""显示""看看""给我看"等 → 视为选择"对话中返回"
- 用户没有明确倾向 → 默认选择"输出到文件"并询问路径

提问格式示例：
> 我将为你生成一个 [配置类型]，需要以下信息：
> 1. 命名空间（如 `my_namespace`）：？
> 2. 物品 ID（如 `my_sword`）：？
> 3. 材质路径（如 `minecraft:item/custom/my_sword`）：？
> 4. 显示名称：？
> 5. ...其他问题

除非用户明确说"你自己决定"，否则不得跳过此步骤擅自假设。

### Step 4: 生成配置模板

根据 Wiki 和 Template 参考内容，严格按照以下规范生成配置：

#### 通用规范

1. **文件结构**：
   ```yaml
   # =============================================================================
   # CraftEngine [配置类型] 配置 — [配置名称]
   # =============================================================================
   # Wiki 参考路径:
   #   - references/CraftEngine Wiki/[对应Wiki路径]
   # Template 参考:
   #   - references/CraftEngine Template/[对应Template路径]
   # =============================================================================

   [根键]:
     [命名空间]:[ID]:
       # 配置内容
   ```

2. **命名空间格式**：使用 `小写英文:小写英文_id` 格式（如 `default:topaz_sword`）

3. **必填字段**必须标注（来源：[Wiki 页面名]）
4. **可选字段**标注默认值（来源：[Wiki 页面名]）
5. **付费版功能**标注 `# 付费版专属`
6. **版本要求**标注 `# 需要 1.21.2+` 等
7. **<< CHANGE THIS** 标记所有需要用户自行修改的值

#### 配置类型规范

**物品 (items) 生成规范：**
```yaml
items:
  namespace:item_id:
    material: paper          # 必填。基础材质
    custom_model_data: 1001  # 可选。正整数，同材质物品不同值
    item_model: "namespace:item_id"  # 可选。1.21.2+
    # data:
    #   item_name: "<!i><颜色>名称"
    #   lore: [...]
    #   components: {...}
    # settings: {...}
    # behavior:
    #   type: block_item / furniture_item / ...
    # model: {...}
    # events: [...]
    # category: namespace:category_id
```

**方块 (blocks) 生成规范：**
```yaml
blocks:
  namespace:block_id:
    state:
      auto_state: note_block
      model:
        texture: "minecraft:block/custom/..."  # 单张纹理
    settings:
      hardness: 2.0
      # ...
    # behavior:
    #   type: ...
    # loot: {...}
    # events: [...]
```

**家具 (furniture) 生成规范：**
```yaml
furniture:
  namespace:furniture_id:
    settings:
      item: namespace:furniture_item_id
      hit_times: 3
      sounds: {...}
    variants:
      ground:
        elements:
          - type: item_display
            item: namespace:furniture_item_id
            # ...
        hitboxes:
          - type: shulker / interaction / ...
            # ...
```

**配方 (recipes) 生成规范：**
```yaml
recipes:
  namespace:recipe_id:
    type: shaped / shapeless / smelting / ...
    pattern: [...]
    ingredients: {...}
    result:
      id: namespace:item_id
      count: 1
```

**原版战利品覆盖 (vanilla_loots) 生成规范：**
```yaml
vanilla_loots:
  namespace:loot_id:
    type: block / entity            # 覆盖目标类型（来源: Wiki vanilla_loot.md）
    target: "minecraft:grass"        # 或 target: [...] 方块状态列表
    override: false                  # 是否覆盖原版战利品（可选）
    loot:                            # 战利品配置（同 loot_table.md 语法）
      - ...
```

#### 高级配置特性

当用户需要高级配置特性时，使用以下特殊语法（来源: `高级配置特性.yml` / Wiki `configuration.md`）：

**1. 节标识符 (Section Identifiers) `#`**
用于在同一文件中出现多个同类型配置节：
```yaml
items#0:
  namespace:first_group:
    material: paper
items#1:
  namespace:second_group:
    material: stick
```
标识符可以是任意字符串：`items#main`、`blocks#extra`、`recipes#a` 等。

**2. 节分隔符 (Section Separators) `::`**
将深层嵌套折叠为单行，提高可读性：
```yaml
items:
  namespace:item:
    data::item_name: "<!i>示例物品"         # 等价于 data: → item_name:
    data::food::nutrition: 5                # 等价于 data: → food: → nutrition:
    data::components::minecraft:max_damage: 128
```

**3. 版本条件配置 (Version Conditions) `$$`**
根据服务器版本自动选择值或合并配置块：
```yaml
items:
  namespace:version_item:
    material: paper
    data:
      item_name:
        $$>=1.21.2: "<!i>新版名称"          # 1.21.2+ 使用
        $$1.20.1~1.21.1: "&6旧版名称"       # 1.20.1~1.21.1 使用
        $$fallback: "&7默认名称"             # 回退值
```
格式支持：
- 固定版本：`$$1.21.4`
- 版本范围：`$$1.20.1~1.21.4`
- 版本比较：`$$>=1.21.4`、`$$<1.21.8`
- 回退值：`$$fallback: <value>`

**4. 版本条件合并 (Version Merge)**
```yaml
items:
  namespace:item:
    material: paper
    data:
      item_name: "<!i>基础名称"
    $$>=1.21.2:                              # 仅在 1.21.2+ 合并以下内容
      data:
        food:
          nutrition: 4
          saturation: 2.5
```

**5. 扩展值类型 (Extended Value Types / YAML Tags)**
确保数值被正确解析（来源: `高级配置特性.yml`）：
```yaml
data:
  components:
    minecraft:custom_data: !!long 12345678901234
```
可用标签：`!!long`、`!!float`、`!!byte`、`!!short`、`!!ByteArray`、`!!IntArray`、`!!LongArray`、`!!DoubleArray`、`!!IntList`、`!!LongList`、`!!DoubleList`

**6. 子包 (Subpacks)**
在 `pack.yml` 中配置，允许根据版本条件启用/禁用资源包子包：
```yaml
# plugins/CraftEngine/pack.yml
subpacks:
  $$>=1.21.4:
    modern_pack: true          # 1.21.4+ 启用
  legacy_pack: true            # 始终启用
  experimental_pack: false     # 默认禁用
```

#### 关键约束

- **绝对不要使用 Wiki 中没有提到的字段、参数或功能。** 如果你不确定某字段是否存在，查找 Wiki 确认。Wiki 中找不到的，不使用。
- **绝对不要假设 Template 中的示例包含所有可能字段。** Template 只是示例，完整字段列表以 Wiki 为准。
- **YAML 格式必须正确。** 注意缩进（2 空格）、冒号后的空格、列表的连字符格式。
- **注释中使用参考来源。** 每个主要配置块旁标注对应的 Wiki 页面路径。
- **使用 "<!i>" 前缀** 确保物品名称在 1.20.4 及以下版本正确显示（来源：Wiki data.md item_name 节）。
- **使用 MiniMessage 格式** 进行文本格式化（来源：Wiki reference/text_format.md）。
- **可选字段注释掉** 而非删除，方便用户按需启用。
- **使用 `#<标识符>` 节标识符** 时，确保每个标识符唯一，且仅用于区分同类型的多个配置节。
- **使用 `::` 节分隔符** 时，确认嵌套路径正确，避免因路径歧义导致配置无效。
- **使用 `$$` 版本条件** 时，始终提供 `$$fallback` 回退值以兼容未覆盖的版本。
- **使用 YAML 类型标签**（`!!long`、`!!float` 等）时，确保目标字段确实需要该类型，避免过度使用。
- **高级配置特性**（节标识符、节分隔符、版本条件、YAML 标签、子包）仅在用户需求涉及时才使用，不可默认加入基础配置中。

### Step 5: 使用 Python 脚本校验

生成配置后，使用 `scripts/craftengine_validator.py` 进行自动化校验。该脚本基于 CraftEngine Wiki 构建了完备的字段 Schema，支持深层校验和精确的错误定位。

#### 5a. 准备校验环境

检查 Python 环境和 PyYAML 依赖：

```bash
python -c "import yaml; print('PyYAML OK')" 2>&1 || echo "需要安装 PyYAML"
```

如果缺少 PyYAML，安装：
```bash
pip install pyyaml
```

#### 5b. 执行校验脚本

将生成的配置文件传递给校验脚本：

```bash
python scripts/craftengine_validator.py <config.yml>
```

脚本会自动执行以下全维度校验：

| 校验维度 | 覆盖内容 |
|---------|---------|
| **YAML 语法** | 解析 YAML 文件，捕获语法错误（错误码 4） |
| **根键合法性** | 检查根键是否在 Wiki 定义的 20+ 种合法根键中 |
| **字段存在性** | 逐字段对照 Wiki Schema 检查，报告未知字段 |
| **必填字段** | 检查必填字段是否缺失（如 items 的 `material`、blocks 的 `state/states`） |
| **字段类型** | 检查值类型（string/int/boolean/list/mapping 等 14 种类型检查器） |
| **枚举值校验** | `auto_state` 组名（25 种）、`push_reaction`（5 种）、属性类型（13 种）等 |
| **物品行为** | 11 种行为类型的特有字段和必填参数 |
| **方块行为** | 50+ 种行为类型的特有字段和必需属性 |
| **家具元素** | 6 种元素类型、4 种判定箱类型的字段校验 |
| **配方类型** | 11 种配方的 type-specific 字段和 category 合法性 |
| **事件函数** | 46 种函数类型的必填参数和 conditions 嵌套 |
| **条件类型** | 28 种条件类型的必填字段（支持 `!` 前缀取反） |
| **版本感知** | 标注需要特定 MC 版本的功能（1.20.5+、1.21.2+ 等） |
| **付费版标注** | 标注付费版专属功能（client_bound_data、conditional 等） |
| **交叉引用** | 检查引用的分类 ID 是否存在 |
| **物品行为规则** | rotation（8 种）、alignment（5 种）枚举校验 |
| **高级语法校验** | 检查 `#` 节标识符唯一性、`::` 分隔符路径合法性、`$$` 版本条件格式正确性 |
| **YAML 类型标签** | 校验 `!!long`、`!!float` 等类型标签的使用是否正确 |
| **原版战利品覆盖** | 校验 `vanilla_loots` 的 type/target/override 字段 |

#### 5c. 读取校验结果

**纯文本模式**（默认），逐条显示：
```
[错误] items.my:sword.material: 字段"material"为必填但缺失
[错误] blocks.my:block.state.auto_state: auto_state 'invalid_type' 无效 (期望: {solid, note_block, ...})
[错误] recipes.my:recipe.type: 配方类型 'wrong_type' 无效 (期望: {shaped, shapeless, ...})
[错误] items.my:sword.behavior.type: 物品行为类型 'unknown' 无效 (期望: {block_item, furniture_item, ...})
[错误] furniture.my:chair.variants.ground.hitboxes[0].type: 判定箱类型 'unknown' 无效 (期望: {interaction, shulker, ...})
[警告] items.my:item.data.equippable: 字段需要 1.21.2+，当前版本 1.21.2
```

**JSON 模式**（`--json`），结构化输出：
```json
{"config.yml": [{"path": "items.my:sword.material", "type": "missing_field", "severity": "error", ...}]}
```

#### 5d. 修复与重校验

- 根据错误路径定位到配置中的对应位置
- 对照 Wiki 确认正确的字段名、类型和枚举值
- **Error 级别的错误必须全部修复**，Warning 可酌情处理
- 修正后重新执行 Step 5b，直到脚本退出码为 0

#### 退出码说明

| 退出码 | 含义 |
|--------|------|
| 0 | 校验通过，无错误 |
| 1 | 校验完成，存在错误/警告 |
| 2 | 参数错误 |
| 3 | 文件读取失败 |
| 4 | YAML 解析错误 |

### Step 6: 输出结果

根据 Step 3 确认的输出方式，按对应格式输出：

#### 6a. 对话中返回

以 Markdown 代码块形式展示完整的 YAML 配置，包含：

1. **生成的配置内容** — 以 YAML 代码块展示完整的配置
2. **参考来源** — 列出参考的 Wiki 页面和 Template 文件
3. **需修改项** — 列出所有标记了 `<< CHANGE THIS` 的项
4. **注意事项** — 版本要求、付费版限制、已知限制等
5. **保存建议** — 建议将配置保存到 `plugins/CraftEngine/` 的哪个子目录

#### 6b. 输出到文件

使用 `Write` 工具将配置保存到指定路径：

1. **确定保存路径** — 使用 Step 3 中用户确认的路径，默认为：
   - `items:` → `plugins/CraftEngine/items/<id>.yml`
   - `blocks:` → `plugins/CraftEngine/blocks/<id>.yml`
   - `furniture:` → `plugins/CraftEngine/furniture/<id>.yml`
   - `recipes:` → `plugins/CraftEngine/recipes/<id>.yml`
   - `equipments:` → `plugins/CraftEngine/equipments/<id>.yml`
   - `vanilla_loots:` → `plugins/CraftEngine/vanilla_loots/<id>.yml`
   - `fonts:` → `plugins/CraftEngine/fonts/<id>.yml`
   - 以此类推，子目录名与 YAML 根键名一致
2. **检查目录是否存在** — 如果目标目录不存在，先向用户确认是否创建
3. **写入文件** — 使用 `Write` 工具保存配置，包含完整的文件头注释（Wiki 参考路径、Template 参考路径、使用说明）
4. **输出报告** — 向用户报告文件已保存的路径、文件内容概要、需修改项列表、注意事项

#### 判断规则

- 如果 Step 3 未确定输出方式，**不得默认使用"对话中返回"**，必须回到 Step 3 询问用户
- 使用 `Write` 工具前，先确认目标目录所在的项目路径是否存在

## Constraints

- **Always** 在生成任何配置前，先读取对应的 Wiki 页面和 Template 文件，确保准确理解配置结构
- **Always** 严格遵守 Wiki 内容 — Wiki 中没有的功能/字段绝对不使用
- **Always** 以 Wiki 为准 — 如果 Template 与 Wiki 描述不一致，以 Wiki 为准
- **Always** 一次只生成一个配置（一个物品、一个方块、一个家具等），不要一次性生成多个
- **Always** 生成完成后执行 YAML 语法校验和 Wiki 对照校验
- **Always** 对任何不确定的配置项向用户提问，除非用户明确授权你自行决定
- **Always** 使用 `<< CHANGE THIS` 标记所有需要用户修改的值
- **Always** 在配置注释中标注参考来源（Wiki 页面路径）
- **Always** 在配置中标注字段的必填/可选状态和默认值
- **Always** 标注付费版专属功能和版本要求
- **Always** 如果用户没有明确说明输出方式（对话中返回 / 输出到文件），必须向用户询问后再输出
- **Never** 在用户未明确输出方式的情况下默认使用"对话中返回"进行交付
- **Always** 优先使用本地 CraftEngine Wiki 和 Template，**绝不**在用户未明确要求时擅自使用在线文档
- **Always** 如果觉得有必要查阅在线文档，必须先向用户确认，并说明在线文档可能因网络原因无法访问
- **Always** 尝试在线文档后若无法访问，必须告知用户，并询问是否继续或中止
- **Never** 在本地文档完全满足需求时向用户提出使用在线文档
- **Never** 使用推测或假设的功能 — 只使用 Wiki 中明确记载的
- **Never** 同时生成多个配置 — 用户需要多个配置时，分别调用
- **Never** 在配置中存在语法错误时交付
- **Never** 使用 `is:` 键（CraftEngine 不使用此键）
- **Never** 假设 Template 文件中的占位符 namespace（如 `my:`、`custom:`）是正确的 — 提示用户替换
- **Never** 在 YAML 中使用 Tab 缩进 — 只使用 2 空格缩进
- **Always** 使用 `#` 节标识符时，确保标识符在同一文件中唯一
- **Always** 使用 `::` 节分隔符时，验证嵌套路径的精确性，避免路径歧义
- **Always** 使用 `$$` 版本条件时，提供 `$$fallback` 回退值覆盖未匹配的版本
- **Always** 生成基础配置时保持简单（不使用高级特性），仅在用户需求涉及时才添加节标识符、版本条件、YAML 类型标签等高级语法
- **Never** 在不需要高级特性的基础配置中使用 `#`、`::` 或 `$$` 语法
- **Never** 将 `高级配置特性` 作为默认配置模板使用 — 仅在用户明确需求或配置复杂度确实需要时采用

## Examples

### ✅ Do This

**用户输入：**
```
生成一个可放置的家具椅子，双人座，带座椅功能
```

**正确做法：**

Step 1 分析：
- 配置类型：furniture（家具）
- 核心功能：双人座椅子，带座椅（两个座位）
- 参考：furniture.md + furniture/variants.md（seats 配置）

Step 2 查阅：
- Read `references/CraftEngine Wiki/configuration/furniture.md` — 了解家具整体结构
- Read `references/CraftEngine Wiki/configuration/furniture/settings.md` — 了解 settings 选项
- Read `references/CraftEngine Wiki/configuration/furniture/variants.md` — 了解 elements、hitboxes、seats 配置
- Read `references/CraftEngine Template/General/基础家具.yml` — 参考椅子示例

Step 3 向用户确认：
> 需要以下信息：
> 1. 命名空间：？
> 2. 家具 ID（如 `double_chair`）：？
> 3. 物品 ID（如 `double_chair_item`）：？
> 4. 显示名称：？
> 5. 材质路径：？
> 6. 输出方式：你希望生成的配置以什么形式交付？
>    a) **对话中返回** — 直接展示 YAML 代码块
>    b) **输出到文件** — 保存到项目目录

（用户选择"对话中返回"）

Step 4 生成配置（示例输出）：
```yaml
# =============================================================================
# CraftEngine 家具配置 — 双人座椅
# =============================================================================
# Wiki 参考:
#   - references/CraftEngine Wiki/configuration/furniture.md
#   - references/CraftEngine Wiki/configuration/furniture/settings.md
#   - references/CraftEngine Wiki/configuration/furniture/variants.md
# Template 参考:
#   - references/CraftEngine Template/General/基础家具.yml (示例 1: 基础椅子)
# =============================================================================

furniture:
  namespace:double_chair:              # << CHANGE THIS: 家具ID
    settings:
      item: namespace:double_chair     # << CHANGE THIS: 对应物品ID
      hit_times: 3                     # 击打次数 (可选, 默认值: 未定义)
      sounds:
        break: minecraft:block.bamboo_wood.break   # << CHANGE THIS
        place: minecraft:block.bamboo_wood.place   # << CHANGE THIS
        hit: minecraft:block.bamboo_wood.hit       # << CHANGE THIS
      adventure_mode_breaking: false   # 冒险模式破坏 (可选)
      correct_tools:                   # 合适挖掘工具 (可选)
        - "#minecraft:axes"
    variants:
      ground:
        loot_spawn_offset: 0.5,0.5,0   # 掉落物偏移 (可选)
        elements:
          - type: item_display         # 物品展示实体
            item: namespace:double_chair_item  # << CHANGE THIS
            display_transform: none
            billboard: fixed
            position: 0.5,0,0
            translation: 0,0.5,0
            scale: 1
        hitboxes:
          - type: shulker              # 潜影贝判定箱 (硬碰撞)
            can_use_item_on: true
            blocks_building: true
            position: 0,0,0
            scale: 1
            peek: 0
            direction: east
            interaction_entity: true
            interactive: true
            seats:                     # 双人座位
              - 0,0,-0.1 0             # 第一个座位
              - 1,0,-0.1 0             # 第二个座位 (来源: Wiki furniture/variants.md seats)
```

Step 5 校验：
- YAML 语法校验通过
- Wiki 对照：seats 格式 `x,y,z yaw` 来自 Wiki variants.md；所有字段名均存在于 Wiki

### ❌ Not This

**错误做法 — 生成配置时包含 Wiki 未记载的功能：**
```yaml
# ❌ Wiki 中不存在 "auto_rotate" 字段
variants:
  ground:
    auto_rotate: true
    elements:
      - ...
```

**错误做法 — 不查阅 Wiki 直接凭记忆生成：**
```yaml
# ❌ 假设所有物品都需要 "display_name" 字段（Wiki 中不存在此字段）
items:
  my:item:
    display_name: "My Item"  # ❌ Wiki 中使用 data.item_name
```

**错误做法 — 一次生成多个配置：**
> 用户说要一个椅子，一次性生成了椅子+桌子+灯具+配方共 4 个配置

**错误做法 — 不向用户确认不确定项：**
> 用户说"生成个剑"，直接假设了命名空间为 `default`、伤害值为 10、材质路径等

**错误做法 — 用户未指定输出方式时自行假设：**
> 用户说"生成一个铁剑的 CraftEngine 配置"，没有说明要保存还是展示
> ❌ 直接以代码块输出到对话中，未询问用户是否需要保存到文件
> ✅ 应先询问：你希望生成的配置以什么形式交付？（对话中返回 / 输出到文件）

## Notes

- **项目中 Skill 内置的 Wiki 和 Template 路径**：所有 Wiki 文件位于 `references/CraftEngine Wiki/`，Template 文件位于 `references/CraftEngine Template/`。
- **官方在线文档地址**：[https://ce.gtemc.cn/zh-Hans/](https://ce.gtemc.cn/zh-Hans/) — 仅当用户明确要求时使用，不可擅自访问。由于网络环境差异，在线文档可能无法访问，尝试后如不可用应向用户报告。
- **命名空间规范**：CraftEngine 使用 `命名空间:路径` 格式（如 `default:topaz_sword`），命名空间建议使用小写英文。
- **版本差异**：CraftEngine 的部分功能依赖 Minecraft 版本。1.20.5+ 使用组件系统，旧版本使用 NBT。生成配置时注意版本标注。
- **付费版功能**：`client_bound_data`、`client_bound_material`、`visual_result`、`functions`、`conditions`（配方级）、`conditional`（条件数据）等为付费版专属，生成时需要标注。
- **auto_state 组**：方块状态使用 `auto_state` 时，组名必须来自 Wiki states.md 列的表格（如 `solid`、`note_block`、`leaves` 等）。
- **YAML 格式**：CraftEngine 支持 `.yml` 和 `.yaml` 扩展名，配置文件应使用 UTF-8 编码。
- **区块标识符**：当单个 YAML 文件中出现多个同一根键的配置块时，使用 `items#0:`、`items#1:` 格式（来源：Wiki configuration.md / `高级配置特性.yml`）。
- **节分隔符 `::`**：将深层嵌套折叠为单行，如 `data::item_name:` 等价于 `data: → item_name:`（来源：`高级配置特性.yml` / Wiki configuration.md）。
- **版本条件 `$$`**：使用 `$$>=1.21.2` 等前缀实现版本感知配置，需提供 `$$fallback` 回退值（来源：`高级配置特性.yml` / Wiki configuration.md）。
- **YAML 类型标签**：`!!long`、`!!float`、`!!byte` 等确保数值被精确解析，适用于 NBT 组件等需要精确类型的场景（来源：`高级配置特性.yml`）。
- **子包 (Subpacks)**：在 `pack.yml` 中配置，结合版本条件启用/禁用资源包子包（来源：`高级配置特性.yml`）。
- **Template 优势**：CraftEngine 的模板系统（`templates` + `arguments`）可以大幅减少重复配置，适合批量生成类似物品。同时 `高级配置特性.yml` 提供的节分隔符、版本条件等可进一步优化配置结构。
- **完整产业链示例**：`references/CraftEngine Template/Example/完整产业链/` 目录包含 70+ 个跨配置类型的综合示例，适合用户需要了解多个配置如何协作时参考。
- **文件存放位置**：生成的配置文件应根据根键放入 CraftEngine 的对应子目录（如 `items:` → `items/` 目录，`blocks:` → `blocks/` 目录，`recipes:` → `recipes/` 目录等）。
- **输出方式选择**：两种输出方式各有适用场景。"对话中返回"适合快速查看和复制配置片段；"输出到文件"适合生成完整配置后直接使用。如果用户不确定选择哪个，推荐"输出到文件"以便后续管理。
