---
name: oraxen-skill
version: 1.1.0
description: >-
  Generate Oraxen plugin YAML configuration templates based strictly on the
  Oraxen Wiki (Oraxen Docs Origin) and Oraxen Template content. Analyzes user needs,
  references the correct Wiki sections and Template examples, then generates one
  complete, validated configuration at a time. After generation, validates YAML
  syntax and cross-checks every field against the Wiki to prevent fabricated content.
  Asks the user for any uncertain decisions before proceeding, including whether
  to output the result in chat or save to a file.
  Triggered by: "生成Oraxen配置", "Oraxen模板生成", "写Oraxen物品",
  "Oraxen方块", "Oraxen家具", "Oraxen配方", "Oraxen装备",
  "oraxen config", "oraxen template", "生成Oraxen物品", "生成Oraxen方块",
  "生成Oraxen家具", "生成Oraxen盔甲", "oraxen配置", "写Oraxen配置",
  "Oraxen自定义", "oraxen item", "oraxen block", "oraxen furniture",
  "oraxen armor", "Oraxen盔甲", "Oraxen食物", "Oraxen武器", "Oraxen工具",
  "Oraxen合成", "Oraxen唱片", "Oraxen作物", "Oraxen机制", "Oraxen机械",
  "oraxen food", "oraxen weapon", "oraxen tool", "oraxen recipe",
  "oraxen mechanic", "oraxen farming", "oraxen combat".
context: fork
agent: general-purpose
allowed-tools: Read Write Glob Grep Bash WebFetch
---

# Oraxen Configuration Skill

## Purpose

根据用户需求，严格基于项目中已有的 **Oraxen Docs Origin（Wiki）** 和 **Oraxen Template（预制配置）** 内容，生成符合官方规范的 Oraxen 插件 YAML 配置模板。每次只生成一个完整的配置（一个物品、一个方块、一个家具等），生成后校验 YAML 语法，并对照 Wiki 验证是否存在虚构内容。

## When to Use

- 用户需要创建 Oraxen 插件的自定义配置（物品、方块、家具、盔甲、配方、机制等）
- 用户不熟悉 Oraxen 配置格式，需要一个模板作为起点
- 用户需要生成一个完整可用的 Oraxen YAML 配置
- 用户需要校验已有的 Oraxen 配置是否正确
- 用户需要了解某个 Oraxen 功能的具体配置方式
- 用户需要为 Oraxen 物品添加特殊能力（Mechanics）

## When NOT to Use

- 用户询问 Oraxen 的概念性问题或插件安装 —— 引导用户阅读 Oraxen 官方 Wiki
- 用户需要批量生成多个配置 —— 要求每次只生成一个，多次调用本 Skill
- 用户需要修改项目中已有的配置而非生成新配置
- 需求与其他插件相关（CraftEngine、CustomCrops、MythicMobs 等）—— 除非是 Oraxen 兼容性配置
- 用户需要配置 Oraxen 全局设置（settings.yml、mechanics.yml）—— 这些不通过 item 配置生成

## Workflow / Steps

### Step 1: 分析用户需求

解析用户的输入，提取以下关键信息：

#### 1a. 配置类型判断

根据用户描述判断需要生成什么类型的 Oraxen 配置：

| 类型 | Oraxen 配置方式 | 用户可能说的关键词 |
|------|----------------|-------------------|
| **基础物品 (Basic Item)** | 简单的物品（显示名称+材质+纹理） | 材料、宝石、组件、装饰品 |
| **武器 (Weapon)** | 基础物品 + AttributeModifiers + 可选 Mechanics | 剑、弓、弩、武器、三叉戟 |
| **工具 (Tool)** | 基础物品 + Components.tool + 可选 Mechanics | 镐、斧、锹、锄、锤子、工具 |
| **食物 (Food)** | Components.food + Components.consumable | 食物、食品、消耗品、饮料 |
| **方块 (Block)** | Mechanics.noteblock / stringblock / chorusblock / shapedblock | 矿石、装饰方块、植物、楼梯 |
| **家具 (Furniture)** | Mechanics.furniture (DISPLAY_ENTITY / ITEM_FRAME) | 椅子、桌子、灯具、装饰 |
| **盔甲 (Armor)** | Components.equippable + AttributeModifiers | 头盔、胸甲、护腿、靴子、盔甲套 |
| **唱片 (Music Disc)** | Components.jukebox_playable | 唱片、音乐碟片 |
| **背包 (Backpack)** | Mechanics.backpack | 背包、存储 |
| **作物/植物 (Crop/Plant)** | Mechanics.furniture + evolution/stages | 作物、植物、种子、生长 |
| **FarmBlock** | Mechanics.noteblock + farmblock | 耕地、农场方块 |

#### 1b. 核心功能提取

- 用户希望这个配置实现什么具体功能？
- 是否需要特殊 Mechanics（机制）？如：thor（雷击）、bigmining（范围挖掘）、harvesting（收割）等
- 是否需要 Components？如：food（食物）、tool（工具）、equippable（可装备）等
- Pack 配置：generate_model（自动生成模型）还是使用自定义模型？

#### 1c. 不确定项记录

标记所有用户未明确但生成配置所需的信息，供 Step 3 询问。

#### 1d. 需求确认

如果用户描述模糊，输出你对需求的理解并向用户确认后再继续。

---

### Step 2: 查阅参考资料

根据 Step 1 判断的配置类型和核心功能，查找对应的 Oraxen Docs Origin（Wiki）和 Oraxen Template（预制配置）参考文件。

#### 2a. Wiki 查阅规则

所有 Wiki 参考文件位于项目目录的 `references/Oraxen Docs Origin/` 下。

**通用参考（所有配置）：**
- 配置总览和结构 → `references/Oraxen Docs Origin/Creating Content/Overview.md`
- 物品基本结构（displayname、material、Pack、Mechanics） → `references/Oraxen Docs Origin/Creating Content/Items/Getting Started.md`

**基础物品 (Basic Item)：**
- 物品外观与模型（Pack 配置） → `references/Oraxen Docs Origin/Creating Content/Items/Appearance & Models.md`
- 物品组件（Components，1.20.5+） → `references/Oraxen Docs Origin/Creating Content/Items/Components.md`
- 物品染色（Dyeable Items） → `references/Oraxen Docs Origin/Creating Content/Items/Dyeable Items.md`

**武器 (Weapon)：**
- 基础物品结构 + AttributeModifiers → `Items/Components.md`（AttributeModifiers 章节）
- 战斗 Mechanics（thor、lifeleech、bleeding 等） → `Items/Item Abilities/Combat.md`
- 弩/弓的特有 Pack 配置（pulling_models、charged_model） → `Items/Appearance & Models.md`

**工具 (Tool)：**
- Components.tool（挖掘规则） → `Items/Components.md`（Tool Component 章节）
- 工具 Mechanics（bigmining、smelting、efficiency、harvesting） → `Items/Item Abilities/Farming.md`
- 工具外观模型 → `Items/Appearance & Models.md`

**食物 (Food)：**
- Components.food + Components.consumable（1.21.2+） → `Items/Components.md`（Food & Consumable Components 章节）
- 食物 Mechanics（旧版本 1.20.5 以下） → `Items/Item Abilities/Miscellaneous.md`（Custom Food 章节）
- 参考实际食物配置示例 → `references/Oraxen_food_template.md`

**方块 (Block)：**
- 方块机制总览 → `Blocks/Overview.md`
- NoteBlock 机制（矿石、固体方块） → `Blocks/NoteBlock.md`
- StringBlock 机制（植物、装饰） → `Blocks/StringBlock.md`
- ChorusBlock 机制（透明方块） → `Blocks/ChorusBlock.md`
- ShapedBlock 机制（楼梯、门） → `Blocks/ShapedBlock.md`
- FarmBlock 机制（自定义耕地） → `Blocks/FarmBlock.md`

**家具 (Furniture)：**
- 家具机制总览 → `Furniture/Overview.md`
- Display Entity 家具 → `Furniture/Display Entities.md`
- 家具位置与旋转 → `Furniture/Position & Rotation.md`
- 作物进化与种植 → `Furniture/Farming & Evolution.md`

**盔甲 (Armor)：**
- 盔甲机制总览（选择版本对应的方法） → `Armors/Overview.md`
- Components 盔甲（1.21.2+ 推荐） → `Armors/Components(1.21.2+).md`
- Trims 盔甲（1.20-1.21.1） → `Armors/Trims (1.20-1.21.1).md`
- Shaders 盔甲（1.18-1.19.4 旧版） → `Armors/Shaders (1.18-1.19.4).md`

**Mechanics（机制）参考：**
- 所有 Mechanics 概览 → `Items/Item Abilities/Overview.md`
- 战斗类 Mechanics → `Items/Item Abilities/Combat.md`
- 农耕类 Mechanics → `Items/Item Abilities/Farming.md`
- 杂项 Mechanics → `Items/Item Abilities/Miscellaneous.md`
- 自定义 Mechanics → `Items/Item Abilities/Custom Abilities.md`
- 点击动作（Click Actions） → `Items/Item Abilities/Click Actions.md`
- 背包外观（Backpack Cosmetic） → `Items/Item Abilities/Backpack Cosmetic.md`

**配方 (Recipe)：**
- 配方系统 → `Commands & Recipes/Recipes.md`

**音效 (Sound)：**
- 音效配置参考 → `Configuration Reference/sound.yml.md`

#### 2b. Template 查阅规则

所有 Template 参考文件位于项目目录的 `references/Oraxen Template/` 下。

| 配置类型 | General 参考文件 | Example 示例文件 |
|---------|-----------------|-----------------|
| 基础物品/材料 | `General/基础物品.md` | `Example/物品/1. 基础材料与宝石.md` |
| 武器 | `General/武器.md` | `Example/物品/2. 武器.md` |
| 工具 | `General/工具.md` | `Example/物品/3. 工具.md` |
| 食物 | `General/食物.md` | `Example/物品/4. 食物.md` |
| 消耗品/药水 | — | `Example/物品/5. 消耗品与药水.md` |
| 音乐唱片 | — | `Example/物品/6. 音乐唱片.md` |
| 背包 | `General/杂项机制参考.md`（Backpack 节） | `Example/物品/7. 背包.md` |
| 皮肤系统 | — | `Example/物品/8. 皮肤系统.md` |
| 帽子 | — | `Example/物品/9. 帽子与头部装备.md` |
| 方块（音符盒） | `General/音符盒方块.md` | `Example/方块/音符盒矿石.md` |
| 方块（绊线） | `General/绊线方块.md` | `Example/方块/绊线花朵与植物.md` |
| 方块（紫颂/透明） | `General/紫颂方块.md` | `Example/方块/紫颂透明方块.md` |
| 方块（形状/楼梯） | `General/形状方块.md` | `Example/方块/形状方块.md` |
| 方块（农场） | `General/农场方块.md` | `Example/方块/农场方块与种植盆.md` |
| 家具 | `General/基础家具.md` | `Example/家具/基础家具.md` |
| 家具（座椅） | `General/展示实体.md` | `Example/家具/座椅与大型家具.md` |
| 家具（进化/作物） | `General/家具进化.md` | `Example/家具/进化植物.md` |
| 家具（唱片机） | `General/家具唱片机.md` | `Example/家具/唱片机.md` |
| 盔甲（1.21.2+） | `General/盔甲_组件_1.21.2+.md` | `Example/盔甲/完整盔甲套装_绿宝石.md` |
| 盔甲（纹饰） | `General/盔甲_纹饰_1.20-1.21.1.md` | — |
| 盔甲（着色器） | `General/盔甲_着色器_1.18-1.19.4.md` | — |
| 盔甲（鞘翅） | — | `Example/盔甲/自定义鞘翅.md` |
| 可染色物品 | `General/可染色物品.md` | — |
| 配方 | `General/配方.md` | `Example/其他配置/配方.md` |
| 战斗 Mechanics | `General/战斗机制参考.md` | `Example/其他配置/战斗机制完整参考.md` |
| 农耕 Mechanics | `General/农耕机制参考.md` | `Example/其他配置/农耕机制完整参考.md` |
| 杂项 Mechanics | `General/杂项机制参考.md` | `Example/其他配置/杂项机制完整参考.md` |
| 自定义能力/点击 | `General/自定义能力与点击动作.md` | `Example/其他配置/自定义能力_点击动作.md` |
| 综合配置 | `General/综合机制配置参考.md` | `Example/其他配置/综合配置示例.md` |
| 自定义音效 | `General/自定义音效.md` | `Example/其他配置/自定义音效.md` |
| UI/字形 | `General/字形.md` | `Example/UI与字形/界面字形.md`、`表情字形.md` |
| GUI | `General/自定义GUI.md` | `Example/UI与字形/GUI物品.md` |
| HUD | `General/自定义HUD.md` | `Example/UI与字形/自定义HUD.md` |
| 文字特效 | `General/文字特效.md` | `Example/UI与字形/文字特效.md` |
| ModelEngine 家具 | `General/ModelEngine家具.md` | — |
| 农场方块 | `General/农场方块.md` | — |

**特殊参考：**
- 食物模板速查 → `references/Oraxen_food_template.md`

#### 2c. 参考来源交叉验证

1. 用 `Read` 工具读取对应的 Wiki 页面和 Template 文件
2. **必须实际读取文件内容**，不得仅凭文件名或记忆推断
3. 同一功能同时读取 Wiki 和对应 Template 进行交叉验证
4. 如果 Wiki 和 Template 对同一字段描述不一致，**以 Wiki 为准**
5. 记录读取了哪些参考文件，供 Step 5 校验使用

#### 2d. 注意事项

- Wiki 和 Template 中引用的纹理路径（如 `default/amethyst.png`）仅为项目示例，生成时需提醒用户替换
- 注意版本差异标注：Components 部分功能仅 1.20.5+ / 1.21.2+ 可用
- Wiki 中文档适用于较新版本（1.20.5+），旧版本（1.20.5 以下）应使用 Mechanics 方式替代 Components

#### 2e. 参考来源优先级规则

生成配置时，严格按照以下优先级使用参考来源：

1. **本地 Oraxen Docs Origin（Wiki）**（`references/Oraxen Docs Origin/`）— 最优先，默认使用
2. **本地 Oraxen Template（预制配置）**（`references/Oraxen Template/`）— 辅助参考
3. **官方在线文档**（[https://docs.oraxen.com/](https://docs.oraxen.com/)）— **仅在用户明确要求时才使用**

##### 在线文档使用规则

- **在用户明确说明要使用官方在线文档之前，绝对不要使用在线文档。** 始终优先使用本地文档。
- 如果遇到本地 Wiki 和 Template 中均未记载的功能或字段，且你觉得有必要查阅在线文档，**必须先向用户确认**是否搜索在线文档。
- 向用户确认时，必须说明：**在线文档可能因网络原因无法访问**。
- 如果用户同意使用在线文档，使用 `WebFetch` 工具获取在线文档内容。
- 如果在线文档无法访问（网络超时、404 等），**必须告知用户无法访问**，并询问用户是否仍要继续生成（此时告知用户缺少参考依据，配置可能有风险），或中止当前操作。

---

### Step 3: 向用户确认不确定项

在生成配置之前，列出所有无法确定的信息并向用户提问。包括但不限于：

#### 必须确认的信息

| 信息项 | 说明 | 示例 |
|--------|------|------|
| **配置类型** | 如果用户未明确，先确认 | `item` / `block` / `furniture` / `armor` 等 |
| **物品 ID** | YAML 中的键名 | `my_sword`、`ruby_ore` |
| **显示名称** | 支持 MiniMessage 颜色格式 | `<gradient:#4B36B1:#6699FF>My Item` |
| **基础材质 (material)** | Minecraft 材质，参考 [Spigot Material](https://hub.spigotmc.org/javadocs/spigot/org/bukkit/Material.html) | `DIAMOND_SWORD`、`PAPER` |
| **纹理/模型路径** | Pack 中的纹理路径 | `default/my_texture.png` |
| **Minecraft 版本** | 影响 Components 和 Mechanics 的选择 | `1.21.4`、`1.20.5` |

#### 根据配置类型额外确认

**基础物品/武器/工具：**
- 是否添加 AttributeModifiers（攻击力、攻速等）
- 是否添加 Lore（描述文本）
- 是否添加 Mechanics（特殊能力）
- 是否添加 Components（耐久度、fire_resistant 等）

**食物：**
- 营养值 (nutrition) 和饱和度 (saturation)
- 食用时间 (consume_seconds)
- 食用后效果 (on_consume_effects)
- 是否使用旧版 Mechanics.food（1.20.5 以下）

**方块：**
- 方块机制类型（NoteBlock / StringBlock / ChorusBlock / ShapedBlock）
- custom_variation 值（确保未被其他方块占用）
- 是否设置硬度、亮度、掉落物等

**家具：**
- 家具类型（DISPLAY_ENTITY / ITEM_FRAME / GLOW_ITEM_FRAME）
- 是否设置屏障 (barrier) 或碰撞箱 (hitbox)
- 是否设置座椅 (seat)
- 是否设置存储 (storage)
- 是否可旋转 (rotatable)

**盔甲：**
- 适用的 Minecraft 版本方法
- 盔甲部位（HEAD / CHEST / LEGS / FEET）
- 护甲值和韧性值

**配方：**
- 配方形状和材料
- 是否设置权限

#### 输出方式询问

**如果用户没有明确说明输出方式，必须向用户询问：**
1. **对话中返回** — 配置以 YAML 代码块形式直接展示在对话中
2. **输出到文件** — 使用 `Write` 工具将配置保存到项目目录下的指定位置

**判断规则：**
- 用户说"保存""生成到""写到文件""输出到"等 → 视为选择"输出到文件"
- 用户说"展示""显示""看看""给我看"等 → 视为选择"对话中返回"
- 用户没有明确倾向 → 默认选择"输出到文件"并询问路径

**如果选择"输出到文件"，继续询问：**
- 保存到哪个 `.yml` 文件？
- 建议默认路径：`Oraxen/items/<类型>/<id>.yml` 或 `plugins/Oraxen/items/<id>.yml`

#### 不可跳过的原则

除非用户明确说"你自己决定"或"你看着办"，否则不得跳过此步骤擅自假设任何未明确的信息。

---

### Step 4: 生成配置模板

根据 Wiki 和 Template 参考内容，严格按照以下规范生成配置。

#### 4a. 通用 YAML 结构

Oraxen 配置的基本结构：

```yaml
# =============================================================================
# Oraxen [配置类型] 配置 — [配置名称]
# =============================================================================
# Wiki 参考路径:
#   - references/Oraxen Docs Origin/[对应Wiki路径]
# Template 参考:
#   - references/Oraxen Template/General/[对应分类名].md
# =============================================================================

<item_id>:
  displayname: "<颜色格式>显示名称"     # 物品显示名称，支持 MiniMessage
  material: <MATERIAL>               # Minecraft 基础材质
  # ========== 可选基本字段 ==========
  # lore:                             # 物品描述（多行）
  #   - "<颜色>描述文本1"
  #   - "<颜色>描述文本2"
  # unstackable: true                 # 是否不可堆叠（背包等特殊物品需要）
  # excludeFromInventory: true        # 是否从 /o inv 隐藏
  # color: 255, 255, 255             # 染色物品的 RGB 颜色
  # ========== Pack：外观与模型 ==========
  Pack:
    generate_model: true/false       # 是否自动生成模型
    parent_model: "item/generated"   # 仅 generate_model=true 时需要
    textures:                        # 仅 generate_model=true 时需要
      - <纹理路径>                     # 如: default/my_item.png
    # model: <模型路径>               # 仅 generate_model=false 时需要
    # ========== Components（1.20.5+） ==========
  Components:
    # 根据类型添加对应组件...
  # ========== AttributeModifiers（属性修饰） ==========
  # AttributeModifiers:
  #   - attribute: ATTACK_DAMAGE
  #     amount: 10
  #     operation: 0                  # 0=ADD_NUMBER, 1=ADD_SCALAR, 2=MULTIPLY_SCALAR_1
  #     slot: HAND                    # HAND, OFFHAND, HEAD, CHEST, LEGS, FEET
  # ========== Enchantments（附魔） ==========
  # Enchantments:
  #   sharpness: 5
  # ========== Mechanics（机制/特殊能力） ==========
  # Mechanics:
  #   <mechanic_type>:
  #     <配置参数>
```

#### 4b. 各配置类型生成规范

##### 基础物品 (Basic Item)

适用场景：材料、宝石、装饰品、合成组件等无特殊功能的物品。

```yaml
<item_id>:
  displayname: "<颜色>显示名称"
  material: PAPER                     # 基础材质，推荐 PAPER 用于自定义物品
  Pack:
    generate_model: true
    parent_model: "item/generated"    # 普通物品用 generated，工具武器用 handheld
    textures:
      - default/<id>.png             # << CHANGE THIS: 纹理路径
```

**参考来源：**
- Wiki: `Items/Getting Started.md` — 基本结构和 Pack 配置
- Wiki: `Items/Appearance & Models.md` — 纹理和模型详解
- Template: `references/Oraxen Template/Example/物品/1. 基础材料与宝石.md` - amethyst、ruby 等示例

##### 武器 (Weapon)

适用场景：剑、斧、弓、弩、三叉戟。

```yaml
<item_id>:
  displayname: "<颜色>武器名称"
  material: DIAMOND_SWORD             # 按武器类型选择基础材质
  lore:
    - "<颜色>描述文本"
  AttributeModifiers:
    - attribute: ATTACK_DAMAGE
      amount: 10                      # << CHANGE THIS: 基础攻击力
      operation: 0
      slot: HAND
    - attribute: ATTACK_SPEED
      amount: 1.6                     # << CHANGE THIS: 攻击速度
      operation: 0
      slot: HAND
  Pack:
    generate_model: true/false
    parent_model: "item/handheld"     # 武器/工具用 handheld
    # model: default/<模型路径>       # 自定义 3D 模型
    textures:
      - default/<id>.png
  Components:
    durability: <数值>                # 耐久度
  # Mechanics:                        # 可选战斗机制
  #   <combat_mechanic>: ...
```

**特殊武器 Pack 配置（参考 `Items/Appearance & Models.md`）：**

**弓 (Bow)** — 需要 pulling_models：
```yaml
Pack:
  generate_model: false
  model: default/combat_bow
  pulling_models:
    - default/combat_bow_pulling_0
    - default/combat_bow_pulling_1
    - default/combat_bow_pulling_2
```

**弩 (Crossbow)** — 需要 charged_model：
```yaml
Pack:
  generate_model: false
  model: default/custom_bow
  pulling_models:
    - default/custom_bow_pulling_0
    - default/custom_bow_pulling_1
    - default/custom_bow_pulling_2
  charged_model: default/custom_bow_pulling_2
  firework_model: default/custom_bow_charged
```

**盾牌 (Shield)** — 需要 blocking_model：
```yaml
Pack:
  generate_model: false
  model: example_shield.json
  blocking_model: example_shield_blocking.json
```

**钓鱼竿 (Fishing Rod)** — 需要 cast_model：
```yaml
Pack:
  generate_model: false
  model: default/fishing_rod
  cast_model: default/fishing_rod_cast
```

**耐久度分层模型 (不同耐久度时显示不同模型)：**
```yaml
Pack:
  generate_model: false
  model: default/diamond_sword
  damaged_models:
    - default/diamond_sword_damaged1
    - default/diamond_sword_damaged2
    - default/diamond_sword_damaged3
```

**参考来源：**
- Wiki: `Items/Getting Started.md` — 基础结构
- Wiki: `Items/Components.md` — durability、AttributeModifiers
- Wiki: `Items/Appearance & Models.md` — 特殊武器模型
- Wiki: `Items/Item Abilities/Combat.md` — 战斗 Mechanics
- Template: `references/Oraxen Template/Example/物品/2. 武器.md` - glass_sword、storm_sword 等
- Template: `references/Oraxen Template/General/工具.md` — 锤子系列

##### 工具 (Tool)

适用场景：镐、斧、锹、锄、锤子、收割工具等。

```yaml
<item_id>:
  displayname: "<颜色>工具名称"
  material: DIAMOND_PICKAXE           # 按工具类型选择
  lore:
    - "<颜色>描述"
  Components:
    durability: <数值>                 # 耐久度
    tool:                              # 1.20.5+ 工具组件
      damage_per_block: 1
      default_mining_speed: 1.0
      rules:
        - speed: 10.0
          correct_for_drops: true
          tags:
            - minecraft:mineable/pickaxe
  Pack:
    generate_model: true/false
    parent_model: "item/handheld"
    # model: default/<模型路径>
    textures:
      - default/<id>.png
  # Mechanics:
  #   bigmining:                       # 范围挖掘
  #     radius: 1
  #     depth: 1
  #   smelting:                        # 自动熔炼
  #     enabled: true
  #   harvesting:                      # 自动收割
  #     cooldown: 10000
  #     radius: 5
  #     height: 3
```

**参考来源：**
- Wiki: `Items/Components.md` — Tool Component
- Wiki: `Items/Item Abilities/Farming.md` — bigmining、smelting、harvesting
- Template: `references/Oraxen Template/Example/物品/3. 工具.md` - emerald_hammer、iron_serpe 等

##### 食物 (Food) — 1.21.2+ 版本

适用场景：可食用的自定义物品，带效果或不带效果。

```yaml
<item_id>:
  displayname: "<颜色>食物名称"
  material: PAPER                     # 推荐 PAPER 或 BREAD 等
  Pack:
    generate_model: true
    parent_model: "item/generated"
    textures:
      - default/<id>.png
  Components:
    food:
      nutrition: <数值>               # 恢复的饱食度（半鸡腿数），如 8
      saturation: <数值>              # 附加饱和度，如 12.8
      can_always_eat: true/false      # 满饱时能否食用
    consumable:
      consume_seconds: <秒数>         # 食用耗时，如 1.6
      animation: EAT/DRINK            # EAT = 固体, DRINK = 液体
      sound: entity.generic.eat       # 食用音效
      has_consume_particles: true
      on_consume_effects:             # 可选：食用后效果
        - type: apply_effects
          effects:
            minecraft:haste:
              duration: <秒数>         # 效果持续时间（秒）
              amplifier: 0             # 效果等级（0 = I级）
              ambient: true
              show_particles: true
              show_icon: true
          probability: 1.0             # 触发概率 0.0-1.0
    # use_remainder:                   # 可选：食用后留下物品
    #   oraxen_item: empty_bottle
    #   amount: 1
    # use_cooldown:                    # 可选：使用冷却
    #   seconds: 2.5
```

**效果类型（on_consume_effects）：**
| 类型 | 描述 | 参数 |
|------|------|------|
| `apply_effects` | 应用状态效果 | `effects` (map), `probability` |
| `remove_effects` | 移除指定效果 | `effects` (list) |
| `clear_all_effects` | 清除所有效果 | 无 |
| `teleport_randomly` | 随机传送 | `diameter` (默认 16) |
| `play_sound` | 播放音效 | `sound` |

**旧版本食物（1.20.5-1.21）：**
```yaml
Components:
  food:
    nutrition: 4
    saturation: 2.5
    can_always_eat: false
    eat_seconds: 1.6
    effects:
      haste:
        duration: 200              # 单位：刻（20刻=1秒）
        amplifier: 0
        ambient: false
        show_particles: true
        show_icon: true
        probability: 1.0
```

**旧版 Mechanics 食物（1.20.5 以下）：**
```yaml
Mechanics:
  food:
    hunger: 10
    saturation: 10
    effects:
      haste:
        amplifier: 0
        duration: 30               # 单位：秒
```

**参考来源：**
- Wiki: `Items/Components.md` — Food & Consumable Components（1.21.2+/1.20.5-1.21）
- Wiki: `Items/Item Abilities/Miscellaneous.md` — Custom Food（旧版）
- Template: `references/Oraxen Template/Example/物品/4. 食物.md` - 食物完整示例
- Template: `references/Oraxen Template/General/食物.md` - 食物模板结构
- 速查: `references/Oraxen_food_template.md`

##### 方块 (Block) — NoteBlock 机制

适用场景：矿石、石材、固体装饰方块等。

```yaml
<block_id>:
  displayname: "<颜色>方块名称"
  material: PAPER                     # 或其他基础材质
  Pack:
    generate_model: true/false
    parent_model: "block/cube_all"    # 单纹理方块
    textures:
      - default/<纹理路径>            # 如 amethyst_ore
    # model: default/<模型路径>       # 自定义模型
  Mechanics:
    noteblock:
      custom_variation: <数字>        # 必须唯一，0~799
      model: <模型路径>              # 模型路径（通常与物品名一致）
      # ========== 可选方块属性 ==========
      hardness: <数值>               # 硬度（挖掘时间），默认 1
      light: <0-15>                  # 光照等级
      # blast_resistant: true         # 抗爆炸
      # immovable: true               # 不可被活塞推动
      # is_falling: true              # 受重力影响（如沙砾）
      # can_ignite: true              # 可被点燃
      # block_sounds:                 # 自定义音效
      #   place_sound: block.stone.place
      #   break_sound: block.stone.break
      # ========== 掉落物配置 ==========
      drop:
        silktouch: true/false        # 精准采集是否掉落自身
        fortune: true/false          # 是否受时运影响
        minimal_type: IRON           # 最低有效工具等级
        best_tools:                  # 最佳挖掘工具
          - PICKAXE
        loots:
          - oraxen_item: <掉落物品ID>
            probability: 1.0
```

**父模型选择（参考 `Blocks/NoteBlock.md`）：**
| 模型 | 纹理数 | 适用场景 |
|------|--------|---------|
| `block/cube_all` | 1 | 六面同纹理 |
| `block/cube_column` | 2 | 原木、柱子（顶底+侧面） |
| `block/cross` | 1 | 植物、花 |
| `block/orientable` | 3 | 熔炉、观察者 |
| `block/orientable_vertical` | 2 | 纵向朝向 |

**NoteBlock 支持的附加功能（参考 Wiki）：**
- `storage` — 存储容器（STORAGE/PERSONAL/ENDERCHEST/DISPOSAL）
- `limited_placing` — 限制放置位置
- `directional` — 定向方块（LOG/FURNACE/DROPPER）
- `logStrip` — 可剥皮原木
- `farmblock` — 自定义耕地系统
- `clickActions` — 点击动作

**StringBlock 方块（植物、花草类）：**
```yaml
Mechanics:
  stringblock:
    custom_variation: <数字>
    model: <模型路径>
    # plant: true                     # 是否为植物
    # tall: true                      # 是否为2格高植物（需要 tall_plant: 另一个半段）
    # waterloggable: true             # 可含水
    drop:
      silktouch: false
      loots:
        - oraxen_item: <ID>
          probability: 1.0
```

**参考来源：**
- Wiki: `Blocks/Overview.md` — 方块机制对比
- Wiki: `Blocks/NoteBlock.md` — NoteBlock 完整配置
- Wiki: `Blocks/StringBlock.md` — StringBlock 配置
- Wiki: `Blocks/FarmBlock.md` — FarmBlock 配置
- Template: `references/Oraxen Template/Example/方块/音符盒矿石.md` — amethyst_ore、caveblock 等

##### 家具 (Furniture)

适用场景：椅子、桌子、灯具、复杂 3D 装饰品、可交互对象。

```yaml
<furniture_id>:
  displayname: "<颜色>家具名称"
  material: PAPER
  Mechanics:
    furniture:
      type: DISPLAY_ENTITY            # DISPLAY_ENTITY（推荐）或 ITEM_FRAME、GLOW_ITEM_FRAME
      # ========== 基本配置 ==========
      barrier: true/false            # 是否生成屏障（碰撞箱）
      # hitbox:                       # DISPLAY_ENTITY 的简化碰撞箱（替代 barriers）
      #   width: 1.0
      #   height: 1.0
      # display_entity_properties:    # 显示实体属性
      #   display_transform: FIXED
      #   scale:
      #     x: 1.0
      #     y: 1.0
      #     z: 1.0
      #   translation:
      #     x: 0.0
      #     y: 0.0
      #     z: 0.0
      # ========== 可选功能 ==========
      # light: <0-15>                 # 光照等级
      # rotatable: true               # 可否旋转
      # seat:                          # 座椅（需要 barrier: true）
      #   height: 0.5
      # hardness: <数值>              # 硬度（破坏时间）
      # restricted_rotation:          # 限制旋转方向
      #   VERY_STRICT                 # VERY_STRICT=4向, STRICT=8向
      # ========== 放置限制 ==========
      # limited_placing:
      #   roof: false                 # 可否放在天花板
      #   floor: true                # 可否放在地板
      #   wall: false                 # 可否挂在墙上
      # ========== 音效 ==========
      # block_sounds:
      #   place_sound: block.stone.place
      #   break_sound: block.stone.break
      # ========== 掉落物 ==========
      drop:
        silktouch: false
        loots:
          - oraxen_item: <家具ID>
            probability: 1.0
  Pack:
    generate_model: false
    model: default/<模型路径>          # 自定义 3D 模型路径
    # models:                          # 多个模型变体（用于 jukebox 等）
    #   opened: default/model_opened
```

**家具类型说明：**
- **DISPLAY_ENTITY**（推荐，1.19.4+）：支持 hitbox、display_entity_properties、动画等现代功能
- **ITEM_FRAME / GLOW_ITEM_FRAME**（旧版）：功能较少，不推荐新项目使用

**家具附加功能：**
| 功能 | 配置位置 | 需要条件 |
|------|---------|---------|
| 存储容器 | `furniture.storage` | barrier: true |
| 唱片机 | `furniture.jukebox` | 无 |
| 进化/生长 | `furniture.evolution` / `furniture.stages` | 无 |
| 文字显示 | `furniture.text_entity` / `furniture.text_entities` | DISPLAY_ENTITY |
| 点击动作 | `furniture.clickActions` | 需要碰撞箱 |
| BlockLocker | `furniture.blocklocker` | 无 |
| 放置限制 | `furniture.limited_placing` | 无 |

**存储容器配置：**
```yaml
furniture:
  barrier: true                      # 存储需要 barriers
  storage:
    type: STORAGE                    # STORAGE / PERSONAL / ENDERCHEST / DISPOSAL
    rows: 5                          # 行数，默认 6
    title: "<red>存储容器名称"       # 默认 "Storage"
    open_sound: entity.shulker.open
    close_sound: entity.shulker.close
```

**进化/生长配置（作物）：**
```yaml
# 推荐方式：Inline Stages（单物品多阶段）
<plant_id>:
  displayname: "<颜色>植物名称"
  material: PAPER
  Pack:
    generate_model: true
    parent_model: "item/generated"
    textures:
      - custom/plants/seed
    models:
      stage0: custom/plants/stage_0
      stage1: custom/plants/stage_1
      stage2: custom/plants/stage_2
      stage3: custom/plants/stage_3
  Mechanics:
    furniture:
      barrier: false
      farmblock_required: true       # 需要 Oraxen 耕地
      # farmland_required: true      # 需要原版耕地
      initial_stage: 0
      stages:
        - model: stage0
          evolution:
            delay: 10000
            probability: 0.5
            light_boost: true
          drop:
            silktouch: true
            loots:
              - { oraxen_item: <plant_id>, probability: 1.0 }
        - model: stage1
          evolution:
            delay: 10000
            probability: 0.5
          drop:
            loots:
              - { oraxen_item: <plant_id>, probability: 1.0 }
        - model: stage2
          evolution:
            delay: 10000
            probability: 0.5
          drop:
            loots:
              - { oraxen_item: <plant_id>, probability: 1.0 }
        - model: stage3               # 最终阶段 — 无 evolution
          drop:
            loots:
              - { oraxen_item: <plant_id>, max_amount: 2, probability: 0.75 }
              - { oraxen_item: <harvest_item>, max_amount: 5, probability: 0.55 }
```

**注意：** `stage` 配置中的 `model` 值引用的是 `Pack.models` 中定义的键，**不是**直接写模型路径。

**参考来源：**
- Wiki: `Furniture/Overview.md` — 家具总览和所有功能
- Wiki: `Furniture/Farming & Evolution.md` — 植物进化完整配置
- Wiki: `Furniture/Display Entities.md` — DISPLAY_ENTITY 特性
- Wiki: `Furniture/Position & Rotation.md` — 位置和旋转设置
- Wiki: `Items/Item Abilities/Click Actions.md` — 点击动作
- Template: `references/Oraxen Template/Example/家具/基础家具.md` - table、chair、cart、shelf 等
- Template: `references/Oraxen Template/Example/家具/进化植物.md` - 作物/植物进化示例

##### 盔甲 (Armor) — Components 方法（1.21.2+）

适用场景：全套自定义盔甲（头盔、胸甲、护腿、靴子）。

```yaml
<armor_id>:
  displayname: "<颜色>盔甲名称"
  material: PAPER                     # 推荐 PAPER（Components 方法任何材质都可以）
  lore:
    - "<颜色>描述"
  Components:
    max_stack_size: 1                 # 盔甲不可堆叠
    durability:
      value: <数值>                   # 耐久度
      damage_entity_hit: true         # 受击时消耗耐久
    equippable:
      slot: HEAD                      # HEAD / CHEST / LEGS / FEET
      model: oraxen:<模型标识>        # 盔甲模型标识
      # equip_sound: item.armor.equip_chain  # Paper 服务端可用
      # dispensable: true
      # swappable: true
  AttributeModifiers:
    - attribute: ARMOR
      amount: <数值>                  # 护甲值
      operation: 0
      slot: HEAD                      # 与 equippable.slot 一致
    - attribute: ARMOR_TOUGHNESS
      amount: <数值>                  # 韧性值
      operation: 0
      slot: HEAD
    - attribute: MAX_HEALTH           # 可选：额外生命
      amount: <数值>
      operation: 0
      slot: HEAD
  Pack:
    generate_model: true
    parent_model: "item/generated"
    textures:
      - default/armors/<纹理路径>
```

**完整盔甲套装示例（参考 `General/盔甲_组件_1.21.2+.md`）：**
生成单件时，确保以下字段正确：
- `slot`：头盔=HEAD, 胸甲=CHEST, 护腿=LEGS, 靴子=FEET
- `model`：同套装所有件使用同一标识（如 `oraxen:emerald`）
- `durability.value`：头盔<胸甲<护腿<靴子（约 437<635<595<516）
- 胸甲的 `ARMOR` 值最高（8），腿甲次之（6），头/靴最低（3）

**参考来源：**
- Wiki: `Armors/Overview.md` — 盔甲方法选择
- Wiki: `Armors/Components(1.21.2+).md` — Components 方法
- Wiki: `Items/Components.md` — equippable、durability、AttributeModifiers
- Template: `references/Oraxen Template/Example/盔甲/` - emerald/obsidian/ruby 全套装示例

##### 唱片 (Music Disc) — 1.21+

适用场景：自定义音乐唱片。

```yaml
<disc_id>:
  displayname: "<颜色>唱片名称"
  material: PAPER
  Components:
    max_stack_size: 1
    jukebox_playable:
      show_in_tooltip: true
      song_key: oraxen:<曲目ID>       # 需要先在 sound.yml 中定义
  Pack:
    generate_model: true
    parent_model: "item/handheld"     # 或 item/generated
    textures:
      - default/<纹理>.png
```

**注意：**
- `song_key` 需要先在 `Oraxen/sound.yml` 中定义自定义音效
- 自定义歌曲需要数据包（datapack）注册歌曲，Oraxen 的声音系统可自动生成数据包

**参考来源：**
- Wiki: `Items/Components.md` — jukebox_playable
- Wiki: `Configuration Reference/sound.yml.md` — 自定义音效配置
- Template: `references/Oraxen Template/Example/物品/6. 音乐唱片.md` - welcome_disk 示例

##### 背包 (Backpack)

适用场景：便携式存储物品。

```yaml
<backpack_id>:
  displayname: "<颜色>背包名称"
  material: PAPER
  unstackable: true                  # 背包必须不可堆叠（防止复制漏洞）
  Mechanics:
    backpack:
      rows: 4                        # 存储行数
      title: "<颜色>背包标题"         # GUI 标题
      open_sound: entity.shulker.open       # 可选，默认值如上
      close_sound: entity.shulker.close     # 可选，默认值如上
  # ⚠️ backpack_cosmetic（背部装饰）不可与 backpack 共存于同一物品
  #    （mechanics.yml 标注为不兼容组合）。如需背部显示，请配置在独立物品上：
  #  leather_backpack_visual:
  #    displayname: "<颜色>背包（装饰版）"
  #    material: PAPER
  #    Mechanics:
  #      backpack_cosmetic:
  #        slot: INVENTORY
  #        offset: { x: 0.0, y: 0.0, z: 0.0 }
  #        scale: 1.0
  Pack:
    generate_model: false
    model: default/<模型路径>
```

**参考来源：**
- Wiki: `Items/Item Abilities/Miscellaneous.md` — Backpack mechanic
- Wiki: `Items/Item Abilities/Backpack Cosmetic.md` — 背包外观
- Template: `references/Oraxen Template/Example/物品/7. 背包.md` - leather_backpack 示例

##### 战斗 Mechanics 配置

适用场景：为武器添加特殊战斗能力（参考 `Items/Item Abilities/Combat.md`）。

**Thor（雷击）：**
```yaml
Mechanics:
  thor:
    lightning_bolts_amount: 5        # 闪电数量
    random_location_variation: 1.5   # 随机偏移范围
    delay: 20000                     # 冷却（毫秒）
    charges: -1                      # 使用次数（-1=无限）
```

**Lifeleech（生命偷取）：**
```yaml
Mechanics:
  lifeleech:
    amount: 2                        # 偷取的心数（1/2心单位）
```

**Bleeding（流血）：**
```yaml
Mechanics:
  bleeding:
    chance: 0.3                      # 30%概率触发
    duration: 100                    # 持续刻数（100刻=5秒）
    damage_per_interval: 0.5         # 每次伤害量
    interval: 20                     # 伤害间隔刻数（20刻=1秒）
```

**EnergyBlast（能量爆破）：**
```yaml
Mechanics:
  energyblast:
    delay: 20000
    length: 5
    damage: 10.0
    particle:
      type: REDSTONE
      size: 1
      color:
        red: 0
        green: 255
        blue: 255
```

**Fireball（火球） / WitherSkull（凋零头颅）：**
```yaml
Mechanics:
  fireball:
    delay: 3000
    yield: 2.0                       # 爆炸威力
    speed: 1.0                       # 弹射物速度
    charges: 5
# 或
  witherskull:
    charged: false                   # 是否可破坏方块
    delay: 3000
    charges: -1
```

**Knockback Strike（连击击退）：**
```yaml
Mechanics:
  knockback_strike:
    required_hits: 15               # 触发需要的连击数
    knockback_horizontal: 2.0        # 水平击退力
    knockback_vertical: 1.2          # 垂直击退力
    reset_time: 80                   # 连击超时重置（刻）
```

**参考来源：**
- Wiki: `Items/Item Abilities/Combat.md` — 全部战斗 Mechanics
- Template: `references/Oraxen Template/Example/物品/2. 武器.md` - storm_sword、blood_sword 等

##### 农耕 Mechanics 配置

适用场景：为工具添加农耕能力（参考 `Items/Item Abilities/Farming.md`）。

**范围挖掘 (BigMining)：**
```yaml
Mechanics:
  bigmining:
    radius: 1                        # 半径（1=3x3）
    depth: 1                         # 深度
```

**自动熔炼 (Smelting)：**
```yaml
Mechanics:
  smelting:
    enabled: true
    play_sound: true
```

**自动收割 (Harvesting)：**
```yaml
Mechanics:
  harvesting:
    cooldown: 10000                  # 使用间隔（毫秒）
    radius: 5                        # 范围
    height: 3                        # 高度
    lower_item_durability: true      # 是否消耗耐久
```

**浇水系统 (Watering)：**
```yaml
# 需要两个物品配对：空壶和满壶
# 空壶：
Mechanics:
  watering:
    filledCanItem: filled_watering_can

# 满壶：
Mechanics:
  watering:
    emptyCanItem: empty_watering_can
```

**修复用品 (Repair)：**
```yaml
Mechanics:
  repair:
    ratio: 0.10                      # 修复百分比（10%）
    # 或使用固定值:
    # fixed_amount: 10
```

**参考来源：**
- Wiki: `Items/Item Abilities/Farming.md` — 全部农耕 Mechanics
- Wiki: `Items/Item Abilities/Miscellaneous.md` — repair、efficiency、durability
- Template: `references/Oraxen Template/Example/物品/3. 工具.md` - iron_cog、gold_cog、diamond_cog（repair 示例）

##### 杂项 Mechanics 配置

**效率/急迫 (Efficiency)：**
```yaml
Mechanics:
  efficiency:
    amount: 2                        # 急迫等级（负数=挖掘疲劳）
```

**盔甲效果 (Armor Effects)：**
```yaml
Mechanics:
  armor_effects:
    night_vision:
      duration: 10                   # 持续时间（Tick？Wiki 中未明确单位）
      amplifier: 0
      ambient: true
      particles: true
      icon: true
```

**光环效果 (Aura)：**
```yaml
Mechanics:
  aura:
    type: simple                     # simple / ring / helix
    particle: PORTAL
```

**帽子 (Hat)：**
```yaml
Mechanics:
  hat:
    enabled: true
```

**灵魂绑定 (Soulbound)：**
```yaml
Mechanics:
  soulbound:
    lose_chance: 0                   # 0=死亡永不丢失, 1=必定丢失
```

**切换光照 (Toggle Light)：**
```yaml
Mechanics:
  toggle_light:
    light: 5                         # 基础光照等级（始终激活）
    toggle_light: 15                 # 切换后的光照等级
```

**Skin（皮肤） / Skinnable（可换肤）：**
```yaml
# 皮肤物品（用于改变其他物品外观）：
Mechanics:
  skin:
    consume: true                    # 使用后是否消耗

# 可换肤物品（可被皮肤改变外观）：
Mechanics:
  skinnable: {}
```

**参考来源：**
- Wiki: `Items/Item Abilities/Miscellaneous.md` — 全部杂项 Mechanics
- Template: `references/Oraxen Template/General/工具.md` - efficiency 工具示例
- Template: `references/Oraxen Template/Example/物品/8. 皮肤系统.md` — 皮肤相关

##### 点击动作 (Click Actions)

适用场景：方块/家具被点击时执行命令、播放音效或发送消息。

```yaml
Mechanics:
  noteblock/furniture/stringblock:    # 替换为对应的机制类型
    clickActions:
      - conditions:
          - '#player.hasPermission("permission.node")'
        actions:
          - '[console] say <player> hello!'
          - '[message] <blue>Hello!'
          - '[actionbar] <gray>Hello from actionbar!'
```

**动作类型：**
| 前缀 | 用途 |
|------|------|
| `[console]` | 以控制台身份执行命令 |
| `[player]` | 以玩家身份执行命令 |
| `[message]` | 发送聊天消息 |
| `[actionbar]` | 发送动作栏消息 |
| `{source=AMBIENT volume=1 pitch=1} [sound]` | 播放音效 |

**参考来源：**
- Wiki: `Items/Item Abilities/Click Actions.md` — 完整 clickActions 文档

#### 4c. 关键生成约束

1. **绝对不要使用 Wiki 中没有提到的字段、参数或功能。** 如果你不确定某字段是否存在，查找 Wiki 确认。Wiki 中找不到的，不使用。
2. **绝对不要假设 Template 中的示例包含所有可能字段。** Template 只是示例，完整字段列表以 Wiki 为准。
3. **YAML 格式必须正确。** 注意缩进（2 空格）、冒号后的空格、列表的连字符格式。
4. **注释中使用参考来源。** 每个主要配置块旁标注对应的 Wiki 页面路径。
5. **版本标注。** 区分 1.20.5+（Components 系统）和旧版本（Mechanics 方式）的配置。
6. **使用 MiniMessage 格式** 进行文本格式化。
7. **可选字段注释掉** 而非删除，方便用户按需启用。
8. **使用 `<< CHANGE THIS` 标记** 所有需要用户自行修改的值。

---

### Step 5: 校验生成的配置

生成配置后，执行以下校验步骤：

#### 5a. YAML 语法校验

逐行检查 YAML 语法：
- 缩进是否一致（统一 2 空格）
- 冒号后是否有空格
- 列表项 `- ` 格式是否正确
- 字符串引号是否匹配（单引号/双引号/无引号）
- 多行字符串格式是否正确
- 特殊字符是否正确处理

#### 5b. Wiki 对照校验

逐字段检查生成的配置，确保：

1. **所有字段名都存在于 Wiki 中** — 对照 Step 2 中读取的 Wiki 页面
2. **所有字段类型正确** — 字符串、整数、布尔值、列表、映射的类型匹配
3. **所有字段值范围正确** — boolean 只用 `true`/`false`，光照范围 0-15，概率范围 0.0-1.0
4. **没有虚构功能** — 不要假设 Oraxen 支持某个 Wiki 未记载的功能
5. **Components 版本兼容性** — 检查配置字段是否与用户指定的 MC 版本匹配
6. **custom_variation 唯一性** — 提醒用户确保该值未被其他方块占用

#### 5c. 修复并重校验

如果发现问题，立即修正配置，然后重新执行 Step 5a-5b 直到全部通过。

#### 5d. 自动化校验脚本

使用 `scripts/oraxen_validator.py` 进行自动化校验。该脚本严格基于 Oraxen Docs Origin 构建字段 Schema，支持深层校验与精确错误定位。

**环境准备**（需 Python + PyYAML）：
```bash
python -c "import yaml; print('PyYAML OK')" 2>&1 || pip install pyyaml
```

**执行校验**：
```bash
# 校验单个配置文件（.yml/.yaml 直接解析；.md 自动提取 ```yaml 代码块）
python scripts/oraxen_validator.py <config.yml>
python scripts/oraxen_validator.py <template.md>

# JSON 输出（便于程序化处理）
python scripts/oraxen_validator.py <config.yml> --json

# 配方文件专用模式（检查 recipe type 是否为 docs 支持的 shaped）
python scripts/oraxen_validator.py recipes/shaped.yml --recipe
```

**校验维度**：

| 维度 | 覆盖内容 |
|------|---------|
| YAML 语法 | 解析错误捕获（错误码 4） |
| 废弃字段 | `itemname` -> `displayname` 等（error） |
| 物品根字段 | 对照 Getting Started.md / Components.md 检查未知字段 |
| Pack 字段 | generate_model/parent_model/textures 等（Appearance & Models.md） |
| Components | durability/food/consumable/tool/equippable/jukebox_playable 等 |
| Mechanics | 44 个机制合法性 + 各机制子字段（Item Abilities docs） |
| 不兼容组合 | backpack+backpack_cosmetic、多方块机制共存（mechanics.yml.md） |
| 方块机制 | noteblock/stringblock/chorusblock/shaped_block 枚举与 custom_variation(>=1) |
| 家具 | type/storage type 枚举、light(1-15) 范围 |
| 配方类型 | Recipes.md 仅 shaped 受支持（--recipe 模式） |
| 可染色材质 | Dyeable Items.md 仅 POTION/LEATHER_HORSE_ARMOR |
| 枚举值 | furniture type(4种)/storage type(5种)/slot(7种)/tool_types/aura type 等 |

**结果解读**：
- `error` 级别：明确违规（废弃字段、不兼容组合、无效枚举、越界值），退出码 1
- `warning` 级别：可疑但可能是 docs 未详述的特性（未知字段、非 shaped 配方），退出码 0

校验通过（退出码 0）后再进入 Step 6 输出。

---

### Step 6: 输出结果

根据 Step 3 确认的输出方式，按对应格式输出：

#### 6a. 对话中返回

以 Markdown 代码块形式展示完整的 YAML 配置，包含：

1. **生成的配置内容** — 以 YAML 代码块展示完整的配置
2. **参考来源** — 列出参考的 Wiki 页面和 Template 文件
3. **需修改项** — 列出所有标记了 `<< CHANGE THIS` 的项
4. **注意事项** — 版本要求、付费版限制、已知限制等
5. **保存建议** — 建议将配置保存到 `references/Oraxen Template/` 的哪个子目录

#### 6b. 输出到文件

使用 `Write` 工具将配置保存到指定路径：

1. **确定保存路径** — 使用 Step 3 中用户确认的路径，建议：
   - 物品类：`Oraxen/items/<分类>/<id>.yml`（如 `Oraxen/items/weapons/my_sword.yml`）
   - 方块类：`Oraxen/items/blocks/<id>.yml`
   - 家具类：`Oraxen/items/furniture/<id>.yml`
   - 食物类：`Oraxen/items/food/<id>.yml`
   - 盔甲类：`Oraxen/items/armors/<id>.yml`
2. **检查目录是否存在** — 如果目标目录不存在，先向用户确认是否创建
3. **写入文件** — 使用 `Write` 工具保存配置，包含完整的文件头注释
4. **输出报告** — 向用户报告文件已保存的路径、文件内容概要、需修改项列表、注意事项

---

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
- **Always** 标注版本要求（如"需要 1.20.5+"、"需要 1.21.2+")
- **Always** 如果用户没有明确说明输出方式（对话中返回 / 输出到文件），必须向用户询问后再输出
- **Always** 优先使用本地 Oraxen Docs Origin（Wiki）和 Oraxen Template
- **Always** 在用户未明确要求使用在线文档之前，**绝不**使用在线文档（`https://docs.oraxen.com/`）
- **Always** 如果需要查阅在线文档，必须先向用户确认，并说明在线文档可能因网络原因无法访问
- **Always** 尝试在线文档后若无法访问（超时、404 等），必须告知用户并询问是否继续或中止
- **Always** 对于 Minecraft 版本相关的差异，必须在生成前确认用户的服务器版本
- **Never** 使用推测或假设的功能 — 只使用 Wiki 中明确记载的
- **Never** 同时生成多个配置 — 用户需要多个配置时，分别调用
- **Never** 在配置中存在语法错误时交付
- **Never** 在 YAML 中使用 Tab 缩进 — 只使用 2 空格缩进
- **Never** 假设纹理/模型文件存在于项目中 — 提醒用户需要自行准备
- **Never** 假设 `custom_variation` 值未被占用 — 提醒用户检查现有配置

## Examples

### ✅ Do This — 生成一个食物配置

**用户输入：**
```
生成一个吃了之后获得急迫效果的矿工三明治
```

**Step 1 分析：**
- 配置类型：食物（Food）
- 核心功能：可食用，食用后获得急迫效果
- 不确定项：nutrition、saturation、consume_seconds、效果持续时间、输出方式

**Step 2 查阅参考：**
- Read `references/Oraxen Docs Origin/Creating Content/Items/Components.md` — Food & Consumable Components 章节
- Read `references/Oraxen_food_template.md` — 食物模板速查

**Step 3 向用户确认：**
> 我将为你生成一个"矿工三明治"食物配置，需要确认以下信息：
> 1. 物品 ID（如 `miner_sandwich`）：？
> 2. 显示名称：？
> 3. 材质（material）：PAPER 或其他？
> 4. 纹理路径（如 `default/sandwich.png`）：？
> 5. 营养值（nutrition，参考：牛排=8，面包=5）：？
> 6. 饱和度（saturation，通常 = nutrition × 0.6~1.6）：？
> 7. 急迫效果等级（0=I级，1=II级）：？
> 8. 急迫效果持续时间（秒）：？
> 9. 你的服务器 Minecraft 版本（影响 Components 格式）：？
> 10. 输出方式：对话中返回 / 输出到文件？

（用户回答了所有问题）

**Step 4 生成配置：**
```yaml
# =============================================================================
# Oraxen 食物配置 — 矿工三明治
# =============================================================================
# Wiki 参考:
#   - references/Oraxen Docs Origin/Creating Content/Items/Components.md
# Template 参考:
#   - references/Oraxen_food_template.md
#   - references/Oraxen Template/General/食物.md
# =============================================================================

miner_sandwich:
  displayname: "<gradient:#F69D84:#FAD98D>矿工三明治"
  material: PAPER
  Pack:
    generate_model: true
    parent_model: item/generated
    textures:
      - default/sandwich.png         # << CHANGE THIS: 纹理路径
  Components:
    food:
      nutrition: 8                   # 营养值，同牛排（参考 Wiki Components.md food 节）
      saturation: 12.8               # 饱和度，nutrition × 1.6
      can_always_eat: true           # 满饱时也可食用以获取效果
    consumable:
      consume_seconds: 5             # 食用耗时 5 秒（参考 Wiki Components.md consumable 节）
      animation: EAT                 # 固体食物用 EAT
      sound: entity.generic.eat
      has_consume_particles: true
      on_consume_effects:
        - type: apply_effects        # 应用状态效果（参考 Wiki consumable on_consume_effects 表）
          effects:
            minecraft:haste:
              duration: 3600          # 3600 秒 = 60 分钟
              amplifier: 0            # I 级
              ambient: true
              show_particles: true
              show_icon: true
          probability: 1.0            # 100% 触发
```

**Step 5 校验：**
- YAML 语法：缩进正确（2 空格），冒号后有空格，列表项格式正确 ✅
- Wiki 对照：
  - `Components.food` — Wiki 中有定义 ✅
  - `Components.consumable` — Wiki 1.21.2+ 中有定义 ✅
  - `on_consume_effects` — 类型 `apply_effects` 在 Wiki 效果类型表中 ✅
  - `minecraft:haste` — 有效的 Minecraft 状态效果 ✅
  - 所有字段类型正确 ✅

### ✅ Do This — 生成一个方块配置

**用户输入：**
```
生成一个紫水晶矿石方块
```

**Step 1 分析：**
- 配置类型：方块（Block），NoteBlock 机制
- 需要：custom_variation、模型、纹理、掉落物

**Step 3 向用户确认：**
> 需要确认以下信息：
> 1. 物品 ID（如 `amethyst_ore`）：？
> 2. custom_variation 值（确保唯一）：？
> 3. 硬度（影响挖掘时间）：？
> 4. 掉落物：掉落自身还是掉落其他物品？
> 5. 纹理路径：？
> 6. 是否需要光照、工具等级限制等？
> 7. 输出方式：对话中返回 / 输出到文件？

**Step 4 生成（示例输出，基于 `Example/方块/音符盒矿石.md` 中的 amethyst_ore 模板）：**

```yaml
# =============================================================================
# Oraxen 方块配置 — 紫水晶矿石
# =============================================================================
# Wiki 参考:
#   - references/Oraxen Docs Origin/Creating Content/Blocks/Overview.md
#   - references/Oraxen Docs Origin/Creating Content/Blocks/NoteBlock.md
# Template 参考:
#   - references/Oraxen Template/Example/方块/音符盒矿石.md
# =============================================================================

amethyst_ore:
  displayname: "<light_purple>紫水晶矿石"
  material: PAPER
  Pack:
    generate_model: true
    parent_model: block/cube_all
    textures:
      - default/amethyst_ore          # << CHANGE THIS: 纹理路径
  Mechanics:
    noteblock:
      custom_variation: 1             # << CHANGE THIS: 确保唯一
      model: amethyst_ore
      hardness: 6                     # 硬度（参考 Wiki NoteBlock.md hardness 节）
      block_sounds:
        break_sound: block.stone.break
        place_sound: block.stone.place
        hit_sound: block.stone.hit
        step_sound: block.stone.step
        fall_sound: block.stone.fall
      drop:
        silktouch: true              # 精准采集时掉落自身
        fortune: true                # 受时运影响
        minimal_type: IRON           # 需要铁镐以上
        best_tools:
          - PICKAXE
        loots:
          - oraxen_item: amethyst    # << CHANGE THIS: 掉落物品 ID
            probability: 1.0
```

**Step 5 校验通过 ✅**

### ❌ Not This

**错误做法 — 包含 Wiki 未记载的功能：**
```yaml
# ❌ Wiki 中不存在 "infinite_durability" 字段
Components:
  infinite_durability: true
```

**错误做法 — 不查阅 Wiki 直接凭记忆生成：**
```yaml
# ❌ 编造了不存在的 Mechanics 类型
Mechanics:
  teleport:
    range: 100
```

**错误做法 — 混淆 Components 和 Mechanics：**
```yaml
# ❌ 在 1.21.2+ 版本中使用了旧版 Mechanics.food（除非用户确认使用旧版本）
Mechanics:
  food:  # 应使用 Components.food + Components.consumable
    hunger: 10
```

**错误做法 — 一次生成多个配置：**
> 用户说要一个椅子，一次性生成了椅子+桌子+灯具+配方共 4 个配置

**错误做法 — 不向用户确认不确定项：**
> 用户说"生成个镐子"，直接假设了材质为 DIAMOND_PICKAXE、耐久为 15000、使用 bigmining 等

**错误做法 — 用户未指定输出方式时自行假设：**
> 用户说"生成一个紫水晶矿石的 Oraxen 配置"，没有说明要保存还是展示
> ❌ 直接以代码块输出到对话中，未询问用户是否需要保存到文件
> ✅ 应先询问：你希望生成的配置以什么形式交付？（对话中返回 / 输出到文件）

**错误做法 — 纹理路径假设：**
> ❌ 假设纹理文件 `default/amethyst_ore.png` 已经存在于项目中
> ✅ 提醒用户需要自行准备纹理文件到 `Oraxen/pack/textures/` 目录

**错误做法 — 擅自使用在线文档：**
> ❌ 遇到本地 Wiki 没有的字段时，不询问用户就直接访问 `https://docs.oraxen.com/` 搜索
> ✅ 应先询问用户："本地文档未记载此功能，是否尝试访问 Oraxen 官方在线文档（https://docs.oraxen.com/）？注意在线文档可能因网络原因无法访问。"

**正确做法 — 在线文档无法访问时的处理：**
> ❌ 尝试访问在线文档失败后，默不作声地继续"编造"配置
> ✅ 告知用户："在线文档无法访问，缺少参考依据，此配置可能有风险。是否仍要继续生成，或中止当前操作？"

## Notes

- **Oraxen Docs Origin（Wiki）路径**：所有 Wiki 文件位于项目 `references/Oraxen Docs Origin/` 目录
- **Oraxen Template（预制配置）路径**：所有示例配置位于项目 `references/Oraxen Template/` 目录
- **Oraxen 食物模板速查**：项目 `references/Oraxen_food_template.md`
- **版本差异重要提醒**：Oraxen 的配置格式在不同 Minecraft 版本间有显著差异。1.20.5+ 引入 Components 系统替代了大部分 Mechanics 功能。生成配置前必须先确认用户的服务器版本。
- **材质/模型文件**：生成的配置引用纹理路径时，需要确保对应的 `.png` 文件存在于 `Oraxen/pack/textures/` 目录。模型文件（.json）需要存在于 `Oraxen/pack/models/` 目录。
- **custom_variation 冲突**：NoteBlock 和 StringBlock 使用 `custom_variation` 作为唯一标识。生成配置时提醒用户检查 `references/Oraxen Template/` 下所有文件中已使用的值。
- **纹理路径规则**：路径相对于 `Oraxen/pack/textures/`，不包含扩展名 `.png`。例如 `default/amethyst_ore` 对应 `pack/textures/default/amethyst_ore.png`。
- **MiniMessage 格式**：Oraxen 使用 Adventure API 的 MiniMessage 格式进行文本格式化。支持颜色标签（`<red>`、`<#FF0000>`）、渐变（`<gradient:#color1:#color2>`）、装饰（`<bold>`）等。
- **YAML 格式**：配置文件使用 UTF-8 编码，2 空格缩进，不使用 Tab。
- **物品 ID 规则**：Oraxen 物品 ID 使用小写英文字母和下划线，如 `my_custom_item`。
- **Pack 配置两种方式**：
  1. `generate_model: true` + `parent_model` + `textures` — 自动生成模型（推荐）
  2. `generate_model: false` + `model` — 使用自定义 JSON 模型
- **Oraxen 官方在线文档**：[https://docs.oraxen.com/](https://docs.oraxen.com/) — **仅在用户明确要求时才能使用**。不可擅自访问。由于网络环境差异，在线文档可能无法访问。尝试后如不可用应向用户报告。
- **Discord 官方社区**：如有疑问可参考 [Oraxen Discord](https://discord.gg/oraxen)
- **Oraxen 全局配置**：`Oraxen/settings.yml` 控制资源包生成方式（item_properties、model_data_ids 等），单个物品通常不需要修改这些配置。
