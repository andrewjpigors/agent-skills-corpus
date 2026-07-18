---
name: watch-face-conventions
description: Wear OS Watch Face Format (WFF) のウォッチフェイス実装で得た規約・落とし穴・実機検証手順。watchface.xml・watch_face_info.xml・AndroidManifest.xml を編集する、ComplicationSlotを設計する、データ式を使う、レイアウト調整をする、AMBIENTモード対応する、実機にデプロイするときは必ずこのスキルを参照すること。Sora/JetBrains Mono などのカスタムフォントを使う場合の幅変動対処や、PowerShellでのADB操作の落とし穴も含む。
---

# Watch Face Conventions

Pixel Watch 3 向け Watch Face Format (WFF) 実装の規約・知見集約。  
forestdigital プロジェクト (Phase 01〜06) で得た学びをまとめている。

---

## 1. プロジェクト基盤

### WFF バージョン

`AndroidManifest.xml` の `com.google.wear.watchface.format.version` で指定。**v4 が最新**で `<RadialGradient>` 等の機能を全サポート。Pixel Watch 3 (Wear OS 5) で完全動作する。

```xml
<application android:hasCode="false" ...>
  <meta-data android:name="com.google.android.wearable.standalone" android:value="true" />
  <property
      android:name="com.google.wear.watchface.format.version"
      android:value="4" />
</application>
```

- `android:hasCode="false"` は WFF の前提条件。Kotlin/Java コードを一切持たない宣言的XMLで実装する
- `com.google.android.wearable.standalone` を `true` にしてスタンドアロン動作

| WFF version | Wear OS | API level | 主な追加機能 |
|-------------|---------|-----------|------------|
| 1 | 4 | 33 | 基本構文 |
| 2 | 5 | 34 | Weather データソース、Gradient |
| 3 | 5.1 | 35 | 追加式・関数 |
| 4 | 6 | 36 | 最新機能全部 |

### watch_face_info.xml の必須要素

**`<Editable value="true" />` を必ず入れること。** これがないとウォッチフェイスのカスタマイズUI（鉛筆/編集ボタン）が表示されず、ユーザーが Complication を設定できない。

```xml
<WatchFaceInfo>
    <Preview value="@drawable/preview" />
    <Editable value="true" />
</WatchFaceInfo>
```

> **背景（Phase 06）**: 当初 `<Editable>` を入れ忘れ、実機で「他のウォッチフェイスには鉛筆ボタンあるのに自分のだけ出ない」とハマった。Complications サンプル ([android/wear-os-samples](https://github.com/android/wear-os-samples)) で `<Editable value="true" />` の存在を発見して解決。

---

## 2. ファイル配置・命名規則

### ディレクトリ構成

```
watchface/src/main/
├── AndroidManifest.xml
└── res/
    ├── drawable/          # 全アイコン・プレビュー画像
    ├── font/              # カスタムフォントTTF
    ├── raw/
    │   └── watchface.xml  # ウォッチフェイス本体定義
    ├── values/
    │   └── strings.xml
    └── xml/
        └── watch_face_info.xml
```

### リソースファイル名

Android リソース名は **小文字 + 下線のみ**。ハイフン不可。

```
NG: clock-ring-ticks.png
OK: clock_ring_ticks.png
```

> **背景**: ハイフン入りのまま `@drawable/clock-ring-ticks` を参照しようとして AAPT2 で詰まる。最初に確認し、必要なら `git mv` でリネームしておく。

### フォント

- TTF を `res/font/` に配置。ファイル名は `sora_bold.ttf` `jetbrains_mono_medium.ttf` の形式
- 参照は `@font/sora_bold` のように拡張子なし
- **静的TTFを使うこと**。変数フォント (`Sora[wght].ttf` 等) は WFF互換性が不確実 & 角括弧でリソース名規則を満たさない
- 入手元: 
  - Google Fonts repo: `google/fonts/ofl/<name>/` 
  - 個別プロジェクトの公式リポ (例: [sora-xor/sora-font](https://github.com/sora-xor/sora-font), [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono))

### ライセンス

OFL フォントを同梱する場合は **OFL.txt と NOTICE.md を `LICENSES/` に配置必須**。

```
LICENSES/
├── OFL-Sora.txt
├── OFL-JetBrainsMono.txt
└── NOTICE.md   # 同梱ファイル一覧と出典
```

---

## 3. データソース (source-type)

### 直接式で利用可能なもの

`<Parameter expression="[NAME]" />` の形で式埋め込み。

**時刻・日付**: `HOUR_0_23` `HOUR_1_12` `MINUTE_Z` `SECOND_Z` `DAY_Z` `MONTH_S` `DAY_OF_WEEK_S` etc.

**ヘルス系（5種のみ）**:

| 式 | 型 | 内容 |
|----|----|-----|
| `STEP_COUNT` | Integer | 歩数 |
| `STEP_GOAL` | Integer | 目標歩数 |
| `STEP_PERCENT` | Integer | 目標達成率 (0-100) |
| `HEART_RATE` | Float/String | 心拍数 |
| `HEART_RATE_Z` | String | ゼロ埋め心拍 |

**システム系**: `BATTERY_PERCENT` `BATTERY_CHARGING_STATUS` `BATTERY_IS_LOW` `UNREAD_NOTIFICATION_COUNT`

**天気 (WFF v2+)**: `WEATHER.IS_AVAILABLE` `WEATHER.CONDITION` `WEATHER.TEMPERATURE` `WEATHER.IS_DAY` 等。詳細は §4 参照。

### 直接式で利用 **不可** なもの → ComplicationSlot

| データ | 対処 |
|--------|------|
| 歩行距離 (DISTANCE 系) | ComplicationSlot で Google Fit / Health Connect から取得 |
| 消費カロリー | 同上 |
| スマホバッテリー | 標準プロバイダなし。表示を諦めるか、サードパーティ Complication アプリを案内 |

> **背景（Phase 03）**: ドキュメントの source-type 一覧を Web検索で確認し、`DISTANCE` `WALKING_DISTANCE` `PHONE_BATTERY` がいずれも存在しないことを発見。design では「歩数 + 距離」「ウォッチ+スマホバッテリー」の表示が指定されていたが、現実は Complication 経由か省略の二択になる。

### 式の主な演算子

- 算術: `+ - * / %`
- 比較: `== != < <= > >=`
- 論理: `&& || !`
- 三項演算子: `cond ? a : b`
- 関数: `Round(x)` `Floor(x)` `Ceil(x)` `abs(x)`

XML中で `&&` `<` を書くときはエスケープ (`&amp;&amp;` `&lt;`) するか CDATA で囲む。

```xml
<Expression name="cur_clear">
  <![CDATA[[WEATHER.CONDITION] == 1 || [WEATHER.CONDITION] == 8]]>
</Expression>
```

---

## 4. WEATHER.CONDITION マッピング

`WEATHER.CONDITION` の integer 値 (0-15) と意味。Compare で分岐する際の対応表。

| 値 | 定数名 | 推奨 drawable |
|----|--------|--------------|
| 0 | UNKNOWN_VALUE | (フォールバック) |
| 1 | CLEAR | clear_day / clear_night (IS_DAY で分岐) |
| 2 | CLOUDY | cloudy |
| 3 | FOG | foggy |
| 4 | HEAVY_RAIN | heavy_rain |
| 5 | HEAVY_SNOW | snowy |
| 6 | RAIN | rainy |
| 7 | SNOW | snowy |
| 8 | SUNNY | clear_day |
| 9 | THUNDERSTORM | thunderstorm |
| 10 | SLEET | rainy |
| 11 | LIGHT_SNOW | snowy |
| 12 | LIGHT_RAIN | rainy |
| 13 | MIST | foggy |
| 14 | PARTLY_CLOUDY | partly_cloudy_day / _night |
| 15 | WINDY | cloudy (フォールバック) |

> エミュレータでは天気プロバイダが標準で接続されていない (`WEATHER.IS_AVAILABLE == false`)。フォールバック表示を必ず実装し、`<Condition>` の `<Default>` 分岐で対応する。実機での実データ表示は天気プロバイダ次第。

---

## 5. テキストレンダリング

### `align` 属性の配置場所

WFF スキーマでは **`align` の許容位置が要素によって違う**。

| 要素 | align 属性の位置 |
|------|-----------------|
| `<TimeText>` | 直接 OK (`<TimeText align="CENTER" ...>`) |
| `<PartText>` | NG — 内側の `<Text>` に配置 (`<PartText><Text align="CENTER">...</Text></PartText>`) |

lint で `Attribute align is not allowed here` が出たら PartText に align が直接ついていないか確認。

### `align="CENTER"` の lint 警告問題

`<Text align="CENTER">` は schema 既定値だが、実際の描画では明示しないと **START (左寄せ) 扱いになる**。lint は "Redundant default attribute value assignment" 警告を出すが、**削除すると見た目が壊れる**。警告は許容する。

> **背景（Phase 05 警告整理）**: 警告全消しを目指して全 `align="CENTER"` を一括削除 → 時刻が左寄りになり秒数と重なる事故発生。schema spec とランタイム挙動が不一致なため lint 警告は無視する方針に変更。

### `hourFormat` の値

- 正: `hourFormat="24"` `hourFormat="12"` `hourFormat="SYNC_TO_DEVICE"`
- 誤: `hourFormat="HOUR_24"` （ビルドは通るが lint で "Wrong attribute value"）

### `<Localization>` の冗長性

```xml
<!-- 両方とも既定値なので不要 -->
<Localization calendar="GREGORIAN" timeZone="SYNC_TO_DEVICE" />
```

これは丸ごと削除可能。lint で "Redundant default" 警告が出る。

### フォント幅の変動 (重要)

**Sora Bold (proportional font) は数字幅が大きく変動**する:

| 表示 | 96pxでの幅 |
|------|-----------|
| `11:11` | 191 px |
| `10:42` | 266 px |
| `22:48` | 276 px |
| `08:00` | 310 px |

`align="CENTER"` で時刻と隣の要素（秒数など）を配置すると、時刻の幅変動でギャップが不安定になる。
- 細い時刻 (`11:11`) のとき → ギャップ広すぎ
- 太い時刻 (`08:00`) のとき → 重なる

**解決策: 右寄せ方式**

```xml
<!-- HH:MM を右端 x=340 で固定 -->
<TimeText align="END" format="hh:mm" hourFormat="24"
    x="0" y="0" width="340" height="100">
  <Font color="#FFF2F6F3" family="@font/sora_bold" size="96" />
</TimeText>

<!-- 秒数を gap=6 で隣接 -->
<PartText x="346" y="..." width="80" height="40">
  <Text align="START">
    <Font color="#FF9FE6C8" family="@font/jetbrains_mono_medium" size="22">
      <Template><![CDATA[:%s]]>
        <Parameter expression="[SECOND_Z]" />
      </Template>
    </Font>
  </Text>
</PartText>
```

CSS の flex `gap:6` の挙動を WFF 絶対座標系で再現するパターン。

### 実装中のフォント幅計測

レイアウト調整時、ウォッチでビルドして見るより先に **PIL で実測** すると速い:

```python
from PIL import ImageFont
font = ImageFont.truetype('watchface/src/main/res/font/sora_bold.ttf', size=96)
for s in ['11:11', '10:42', '22:48', '08:00']:
    bbox = font.getbbox(s)
    print(f'{s}: w={bbox[2]-bbox[0]}px')
```

> **背景（Phase 06）**: 「時刻と秒数の間が空きすぎ」と「重なる」が時刻によって交互発生。原因が proportional font の幅変動だと気づいたのは PIL 実測してから。最初からこれをやれば早かった。

### Template と Parameter

```xml
<Template><![CDATA[%s · %s %s]]>
  <Parameter expression="[DAY_OF_WEEK_S]" />
  <Parameter expression="[MONTH_S]" />
  <Parameter expression="[DAY_Z]" />
</Template>
```

- `%s` は順番に Parameter で置換される
- **リテラル `%` を出すには `%%` でエスケープ必須** (printf 系と同じ)。エスケープせず `<Template>%</Template>` のように書くと**実機で "Error" 表示**になる (ビルドは通る)
- 空白・記号 (`·` `(` `)` `日` 等) はそのまま埋め込み可能
- CDATA 推奨 (special characters対応のため)

```xml
<!-- NG: 実機で "Error" 表示 -->
<Template>%</Template>

<!-- OK: バッテリーの "%" サブラベル等で必要 -->
<Template>%%</Template>

<!-- OK: 値に "%" を付けて表示 -->
<Template><![CDATA[%s%%]]>
  <Parameter expression="[BATTERY_PERCENT]" />
</Template>
```

> **背景**: バッテリータイルの数字下に "%" サブラベルを追加したとき発見。エミュレータでは特定の表示にならず、実機 Pixel Watch 3 でのみ "Error" と出た。ビルド時もlint時も警告なし。WFF の Template parser が `%` を format specifier の開始と認識して失敗する。

### null 安全な式

```xml
<Parameter expression="[HEART_RATE] != null ? [HEART_RATE] : &quot;--&quot;" />
```

センサーが値を返さないとき null になる式に必須。

---

## 6. ComplicationSlot

### Scene 直下に置く (重要)

ComplicationSlot は **Scene の直接の子** として配置する。`<Group>` の中に入れると lint で `Element ComplicationSlot is not allowed here` 警告。

```xml
<!-- NG: Group の中 -->
<Group name="tile_battery" ...>
  <ComplicationSlot ... />   <!-- 警告 -->
</Group>

<!-- OK: Scene 直下に絶対座標で配置 -->
<Scene>
  ...
  <Group name="tile_battery" x="229" y="318" ...>
    <PartImage ... />
    <PartText ... /> <!-- 静的部分は Group の中 -->
  </Group>
  
  <!-- 動的に切り替わる ComplicationSlot は Scene 直下 -->
  <ComplicationSlot slotId="3" x="263" y="358" ...>
    ...
  </ComplicationSlot>
</Scene>
```

座標は**絶対値**になるので、視覚的に Group の中に重ねたい場合は Group の x/y を加算した値を計算して配置する。

### 標準的な構造

```xml
<ComplicationSlot
    slotId="2"
    name="distance_slot"
    displayName="distance_label"
    supportedTypes="SHORT_TEXT EMPTY"
    x="91" y="368" width="60" height="16">
    <Variant mode="AMBIENT" target="alpha" value="180" />
    <DefaultProviderPolicy
        defaultSystemProvider="STEP_COUNT"
        defaultSystemProviderType="SHORT_TEXT" />
    <BoundingOval x="0" y="0" width="60" height="16" />
    <Complication type="SHORT_TEXT">
        <PartText x="0" y="0" width="60" height="16">
            <Text align="CENTER">
                <Font color="#8CF2F6F3" family="@font/jetbrains_mono_medium" size="14">
                    <Template><![CDATA[%s]]>
                        <Parameter expression="[COMPLICATION.TEXT]" />
                    </Template>
                </Font>
            </Text>
        </PartText>
    </Complication>
</ComplicationSlot>
```

ポイント:
- `slotId` はユニークな整数。文字盤内で重複不可
- `supportedTypes`: `SHORT_TEXT EMPTY` を最低限。空白区切り
- `<BoundingOval>` または `<BoundingRect>`: タップ判定範囲。複雑な形状なら `<BoundingArc>`
- `<DefaultProviderPolicy>`: 初期値を設定。ユーザーが変更可能
- `<Complication type="...">` の中に表示要素を置く
- スロット内では `[COMPLICATION.TEXT]` `[COMPLICATION.TITLE]` 等の特殊式が使える

### 利用可能な標準 systemProvider

```
STEP_COUNT
WATCH_BATTERY
DATE
DAY_OF_WEEK
DAY_AND_DATE
TIME_AND_DATE
WORLD_CLOCK
UNREAD_NOTIFICATION_COUNT
NEXT_EVENT
APP_SHORTCUT
SUNRISE_SUNSET
```

DISTANCE / PHONE_BATTERY 等の標準プロバイダは無いので、デフォルトを `EMPTY` にしてユーザーに第三者プロバイダ選択を委ねる。

### 通知件数の取扱い

直接式 `[UNREAD_NOTIFICATION_COUNT]` は環境によって null や 0 のままになることがある。**ComplicationSlot + `defaultSystemProvider="UNREAD_NOTIFICATION_COUNT"` の方が確実に動く**。

> **背景（Phase 06）**: 実機で `[UNREAD_NOTIFICATION_COUNT]` 直接式が常に 0 を返す事象。原因は不明だが、ComplicationSlot 経由に変えて即解決。Complication 経由はパーミッション周りも framework が面倒見てくれる。

### タップでアプリ起動 (タップ判定パターン)

ComplicationSlot は **デフォルトでタップ可能**。タップ時の挙動は設定された Complication プロバイダの `tapAction` インテント実装に依存する。

**起動するもの (例)**:
| systemProvider | タップで起動 |
|----------------|-------------|
| `STEP_COUNT` | Fit / Health Services |
| `WATCH_BATTERY` | バッテリー設定 |
| `UNREAD_NOTIFICATION_COUNT` | 通知シェード |
| サードパーティ Complication | プロバイダ実装次第 (持たないものもある) |

**起動しないもの**: 一部のサードパーティ（特に天気系で多い）はデータのみ提供、`tapAction` 無し → タップ無反応。**ウォッチフェイス側ではどうにもできない** (Complication 仕様)。

### タップ対応タイルの実装パターン: 「Group + Slot ペア」

タイル全体をタップ可能にするには、**Group (静的) + ComplicationSlot (動的+タップ判定) のペア**で組む。

```xml
<!-- 静的部分: アイコン・ラベル等、常に表示 -->
<Group name="tile_steps" x="91" y="308" width="60" height="60">
    <Variant mode="AMBIENT" target="alpha" value="180" />
    <PartImage x="12" y="0" width="36" height="36">
        <Image resource="@drawable/steps" />
    </PartImage>
</Group>

<!-- 動的+タップ判定: Scene 直下に同じ位置・サイズで重ねる -->
<ComplicationSlot slotId="1" name="steps_slot"
    supportedTypes="SHORT_TEXT EMPTY"
    x="91" y="308" width="60" height="60">
    <Variant mode="AMBIENT" target="alpha" value="180" />
    <DefaultProviderPolicy
        defaultSystemProvider="STEP_COUNT"
        defaultSystemProviderType="SHORT_TEXT" />
    <BoundingOval x="0" y="0" width="60" height="60" />
    <Complication type="SHORT_TEXT">
        <!-- 値テキストのみ。アイコンは Group 側で常時表示済み -->
        <PartText x="0" y="40" width="60" height="18">
            <Text align="CENTER">
                <Font color="#FFF2F6F3" family="@font/sora_semibold" size="16">
                    <Template><![CDATA[%s]]>
                        <Parameter expression="[COMPLICATION.TEXT]" />
                    </Template>
                </Font>
            </Text>
        </PartText>
    </Complication>
</ComplicationSlot>
```

ポイント:
- **Group と Slot は同じ x/y/width/height で配置** → 視覚的に重なる
- Slot の `BoundingOval` は**タイル全体**にする (icon エリアも tap 判定対象に含める)
- 値テキストの座標は Slot 内座標 (`y=40`) で書く
- 同じ AMBIENT alpha を両方に付けてバリアントを揃える

### 透明オーバーレイによる「既存表示にタップだけ追加」パターン

`WEATHER.*` のような直接式で組んだ複雑な領域に**タップだけ追加したい**ときに使う。表示はそのまま、Slot は不可視で BoundingOval だけ機能させる。

```xml
<ComplicationSlot slotId="6" name="weather_slot"
    supportedTypes="SHORT_TEXT EMPTY"
    x="60" y="0" width="330" height="140">
    <BoundingOval x="0" y="0" width="330" height="140" />
    <Complication type="SHORT_TEXT">
        <!-- 不可視プレースホルダー。タップ判定だけが目的。 -->
        <PartText alpha="0" x="0" y="0" width="1" height="1">
            <Text align="START">
                <Font color="#00000000" family="@font/sora_bold" size="1">
                    <Template><![CDATA[%s]]>
                        <Parameter expression="[COMPLICATION.TEXT]" />
                    </Template>
                </Font>
            </Text>
        </PartText>
    </Complication>
</ComplicationSlot>
```

ポイント:
- `<Complication>` 要素は中身が必須なので、**alpha=0 + 1×1 サイズ + 透明色 + 1pxフォント**で実質不可視にする
- ユーザーが Complication プロバイダを設定すると、表示は既存式のまま、タップは設定したプロバイダの `tapAction` で起動
- ⚠️ **二つのデータソースのズレ**: 表示は直接式 (例: OS の天気)、タップで開くアプリは別プロバイダ → 気温などの値が違うことあり。許容する旨をユーザーに説明する

> **背景（Issue #17）**: メトリクスタイルと天気エリアをタップ起動対応にする際の設計。歩数・心拍・バッテリーは Group+Slot ペア化、天気は透明オーバーレイで既存の凝った WEATHER.* 表示を維持したままタップだけ後付けした。

---

## 7. 条件分岐 (Condition)

### 基本パターン

```xml
<Condition>
    <Expressions>
        <Expression name="is_clear">[WEATHER.CONDITION] == 1</Expression>
        <Expression name="is_cloudy">[WEATHER.CONDITION] == 2</Expression>
    </Expressions>
    <Compare expression="is_clear">
        <!-- clear のときレンダリングする要素 -->
    </Compare>
    <Compare expression="is_cloudy">
        <!-- cloudy のときレンダリングする要素 -->
    </Compare>
    <Default>
        <!-- どれにも該当しないとき -->
    </Default>
</Condition>
```

- `<Compare expression="...">` は **boolean を評価する名前付き式** を取る。生の式を直接書くと動かない
- 評価順は記述順。**最初にマッチしたものだけ**レンダリングされる (switch-case と同じ)
- `<Default>` で必ずフォールバックを用意する

### 多値の集約

複数の値を1つのbool式にまとめると Compare が増えすぎず管理しやすい:

```xml
<Expression name="is_rain">
  <![CDATA[[WEATHER.CONDITION] == 6 || [WEATHER.CONDITION] == 10 || [WEATHER.CONDITION] == 12]]>
</Expression>
```

WEATHER.CONDITION 16値 → drawable 10種にマッピングするのに有用。

### ネスト

`<Compare>` の中にさらに `<Condition>` を入れられる:

```xml
<Compare expression="is_clear">
    <Condition>  <!-- 昼夜分岐 -->
        <Expressions>
            <Expression name="d">[WEATHER.IS_DAY]</Expression>
        </Expressions>
        <Compare expression="d">
            <PartImage ...><Image resource="@drawable/clear_day" /></PartImage>
        </Compare>
        <Default>
            <PartImage ...><Image resource="@drawable/clear_night" /></PartImage>
        </Default>
    </Condition>
</Compare>
```

天気 (CONDITION) × 昼夜 (IS_DAY) の組み合わせを表現するのに必要。XML は冗長になるが避けられない（WFF にマクロ・関数定義はない）。

---

## 8. 背景・グラデーション

### 単色背景

`<Scene backgroundColor="#FF0D1F1A">` で済むが、グラデーションは別途必要。

### RadialGradient

WFF v2+ で利用可能。`<PartDraw>` + `<Rectangle>` (または `<Ellipse>`) + `<Fill>` の中に置く。

```xml
<PartDraw x="0" y="0" width="450" height="450">
    <Rectangle x="0" y="0" width="450" height="450">
        <Fill>
            <RadialGradient
                centerX="225"
                centerY="157"
                radius="370"
                colors="#FF1F4838 #FF0D1F1A #FF050907"
                positions="0.0 0.55 1.0" />
        </Fill>
    </Rectangle>
</PartDraw>
```

- `colors` `positions` は空白区切りの文字列。**ColorStop 要素は使わない** (WFF 仕様)
- `positions` の値は 0.0〜1.0 の浮動小数点
- `radius` は **対角線の半分くらい** が目安 (450x450 で radius=300 だと半分以上が単色化する)

> **背景（Phase 06）**: 最初 radius=300 で実装したが「グラデーションが見えない」と指摘。原因は radius が小さすぎて画面の半分以上が末端カラーで埋まっていたこと。radius=370 に拡大 + 中心色を明るく (`#102822 → #1F4838`) + 端を暗く (`#07120E → #050907`) で視認可能になった。

### 色相のメリハリ

デザイン HTML の値をそのまま CSS の `radial-gradient(...)` で見ると映えても、WFF で同じ色を使うと薄く見える。**端と中心の輝度差を CSS より広く取る** のが目安。

---

## 9. AMBIENT モード

### 基本: `<Variant>` 要素

要素の属性を AMBIENT モードで上書きできる。`alpha` `color` などをターゲット可能:

```xml
<PartImage x="0" y="0" width="450" height="450">
    <Variant mode="AMBIENT" target="alpha" value="80" />
    <Image resource="@drawable/clock_ring_ticks" />
</PartImage>
```

通常時 alpha=255 → AMBIENT時 alpha=80 (減光)。

### グループ全体の減光

`<Group>` 直下に `<Variant>` を置くと、Group内の全要素に乗算される:

```xml
<Group name="tile_steps" x="91" y="308" width="60" height="72">
    <Variant mode="AMBIENT" target="alpha" value="180" />
    <PartImage ... />
    <PartText ... />
</Group>
```

タイルや上ゾーンなど、まとめて減光したい単位に有効。

### 時刻フォントの焼き付き対策 (デュアル要素パターン)

WFF には `Variant target="weight"` がない。**Bold→Thin の切替には2要素必要**:

```xml
<DigitalClock x="0" y="160" width="340" height="100">
    <!-- Interactive: Sora Bold (太字) -->
    <TimeText align="END" format="hh:mm" hourFormat="24"
        x="0" y="0" width="340" height="100">
        <Variant mode="AMBIENT" target="alpha" value="0" />  <!-- AMBIENT時は隠す -->
        <Font color="#FFF2F6F3" family="@font/sora_bold" size="96" />
    </TimeText>
    
    <!-- AMBIENT: Sora Thin (細字、焼き付き軽減) -->
    <TimeText alpha="0" align="END" format="hh:mm" hourFormat="24"
        x="0" y="0" width="340" height="100">
        <Variant mode="AMBIENT" target="alpha" value="255" />  <!-- AMBIENT時のみ表示 -->
        <Font color="#FFF2F6F3" family="@font/sora_thin" size="96" />
    </TimeText>
</DigitalClock>
```

- 通常時は1番目だけ可視、2番目は alpha=0 で隠れる
- AMBIENT 時は Variant で逆転 → 2番目だけ可視
- AOD の焼き付き対策では「点灯ピクセルを減らす」が原則のため、Thin 細字や非表示 (秒数) が有効

### 秒数の AMBIENT 非表示

```xml
<Group name="seconds_group" ...>
    <Variant mode="AMBIENT" target="alpha" value="0" />
    <PartText ...>...</PartText>
</Group>
```

秒数は AOD で更新頻度が下がる (1分ごと程度) ため、表示し続けるとカクついて見える。完全に非表示にするのが標準。

### tick ring の減光

ティック (時刻目盛) のような装飾要素は **alpha=80 前後で控えめに**。AMBIENT で消すと方向感が無くなるが、明るすぎると消費電力増。

---

## 10. 実機検証ワークフロー (Pixel Watch 3)

### ワイヤレス ADB セットアップ

Pixel Watch 3 は USB-C を持たないので Wi-Fi 経由必須。**PC とウォッチを同じ Wi-Fi ネットワークに**。

```powershell
# 1. ウォッチで開発者オプション有効化 (端末情報 → ビルド番号7回タップ)
# 2. 開発者向けオプション → ADB デバッグ ON、Wi-Fi 経由でデバッグ ON
# 3. 表示される IP アドレスとペアリング情報をメモ

# 4. PC からペアリング (初回のみ)
adb pair 192.168.0.7:XXXXX   # XXXXX はペアリング用ポート（5555ではない）
# プロンプトでペアリングコード入力

# 5. 接続 (毎回)
adb connect 192.168.0.7:5555
adb devices   # 'device' 表示で接続成功

# 6. インストール (-s でデバイス指定)
adb -s 192.168.0.7:5555 install -r watchface\build\outputs\apk\debug\watchface-debug.apk
```

エミュレータと実機を同時接続していると `more than one device` で怒られる。**`-s <serial>`** で必ず指定。

### カスタマイズUI へのアクセス

実機 (またはエミュレータ) で:

1. 文字盤を**長押し** → ウォッチフェイスカルーセル
2. 文字盤下に**鉛筆 (Edit) ボタン** → カスタマイズ画面
3. **Complications** タブで空のスロットをタップ → プロバイダ選択

> 鉛筆ボタンが出ない場合は `watch_face_info.xml` の `<Editable value="true" />` を確認 (§1)

### スクリーンショット

#### 一番きれいに撮れる: Pixel Watch companion app

スマホの **Pixel Watch アプリ** に「最近のメディア」「ウォッチのスクリーンショット」機能があり、これが**最もクリーン** (カルーセル・ホームピル等のオーバーレイ無し)。

実機検証で preview.png を更新する用途には companion app 経由がベスト。

#### コマンド経由 (ADB screencap)

```powershell
# ウォッチを起こす (AOD のとき重要)
adb -s 192.168.0.7:5555 shell input keyevent KEYCODE_WAKEUP
Start-Sleep -Seconds 1

# 撮影 → ローカルに pull → 元ファイル削除
adb -s 192.168.0.7:5555 shell screencap -p /sdcard/screen.png
adb -s 192.168.0.7:5555 pull /sdcard/screen.png .
adb -s 192.168.0.7:5555 shell rm /sdcard/screen.png
```

#### ⚠️ PowerShell の落とし穴

**PowerShell の `>` リダイレクトは PNG バイナリを壊す** (改行コード変換が入って画像が壊れる):

```powershell
# NG: PowerShell では破損する
adb exec-out screencap -p > screen.png

# OK: shell + pull で取得する
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png .
```

(cmd.exe や bash では `>` でも問題ない。WSL 環境なら exec-out で大丈夫)

#### 撮影時の注意

- **画面オフ / AOD だと黒画像になる** → KEYCODE_WAKEUP で起こす
- **長押し直後はカルーセル状態** → カルーセルの両サイドに他のフェイスが映る。クラウンで通常画面に戻ってから撮る
- **画面下端のホームピル** (Android のジェスチャーナビ pip) はオーバーレイでスクショに含まれる。preview.png に使う場合は PIL で塗りつぶすか、companion app 経由で取得 (これだとピルなし)

### 実機画面サイズ

Pixel Watch 3 のスクショは **456×456 で出る** (450×450 ではない)。中心トリムして 450×450 に揃える:

```python
from PIL import Image
src = Image.open('screen.png')
left = (src.width - 450) // 2
top = (src.height - 450) // 2
src.crop((left, top, left + 450, top + 450)).save('preview.png')
```

---

## 11. デザイン視点の落とし穴

### ベゼル現実

**Pixel Watch 3 (実機) はベゼルがそれなりに太い**。デザインモック (HTML) の見た目から想像するより枠の存在感がある。

実装上の影響:
- 画面**最外周**に細線や装飾を入れるとベゼルとの境界が際立って汚く見える
- **黒系・ダーク系の背景**だとベゼル境界がぼかせる (ライト系より相性良い)
- ティックリングは**ある程度内側**に寄せる方が無難 (450x450 のうち外側 10-15px はリスクゾーン)

> **背景（Phase 06）**: 実機で見て初めて分かった。エミュレータでは綺麗に見えていた外周装飾が、実機ではベゼルとの段差で違和感を出すケースあり。

### 円形デザイン

文字盤の有効領域は**円**だが、座標系は450×450の正方形。**角は実際には見えない**ので、コーナーに重要な情報を置かない。

```
中心 (225, 225) からの距離 = 225 で円周
四隅 (0,0) (450,0) (0,450) (450,450) は距離 ≈ 318 で円外
```

中心の対角 ±0.5 倍 (225±113) 範囲 ≒ x,y = 112〜338 が**安全に視認**できるエリア。

### フォント選び

- **時刻表示はモノスペース系またはタブラー数字** が無難。Sora Bold のような proportional は数字幅変動でレイアウトが乱れる
- どうしても proportional を使うなら、§5 の右寄せ方式で逃げる
- アイコンは PNG (drawable) で素朴にした方が WFF 制約と相性良い (SVG 風はサポート薄い)

---

## 12. 開発時に常用するコマンド

```powershell
# ビルド (デバッグAPK)
.\gradlew :watchface:assembleDebug

# Lint (warnings 確認)
.\gradlew :watchface:lint

# 実機接続確認
adb devices

# インストール
adb -s <SERIAL> install -r watchface\build\outputs\apk\debug\watchface-debug.apk

# ログ監視 (WFF 関連)
adb -s <SERIAL> logcat | Select-String -Pattern "WatchFace|WFF"
```

### PIL でフォント・画像を確認 (Python)

```python
# フォント幅実測
from PIL import ImageFont
font = ImageFont.truetype('watchface/src/main/res/font/sora_bold.ttf', size=96)
print(font.getbbox('22:48'))  # → (0, 21, 276, 96)

# PNG のサイズ・透明度確認
from PIL import Image
im = Image.open('watchface/src/main/res/drawable/clock_ring_ticks.png')
print(f'size: {im.size}, mode: {im.mode}')
alphas = [p[3] for p in im.getdata() if p[3] > 0]
print(f'visible pixels: {len(alphas)}, max alpha: {max(alphas)}')
```

レイアウト調整時に何度もビルド → install → 確認するより、PIL で先に数値で当たりをつける方が圧倒的に早い。

---

## 13. リファレンス・参考実装

- **WFF 公式**: [Watch Face Format ガイド](https://developer.android.com/training/wearables/wff)
- **データソース一覧**: [source-type リファレンス](https://developer.android.com/training/wearables/wff/common/attributes/source-type)
- **公式サンプル集**: [android/wear-os-samples](https://github.com/android/wear-os-samples) の `WatchFaceFormat/` 配下
  - `Complications` — ComplicationSlot の基本
  - `Weather` — `WEATHER.*` データソース使用例
  - `Flavors` — UserConfiguration / ListConfiguration / Flavors の使い方
  - `PhotosMask` — 画像マスク
- **OFL フォント取得元**:
  - Google Fonts: [`google/fonts/ofl/<name>/`](https://github.com/google/fonts/tree/main/ofl)
  - 個別: [sora-xor/sora-font](https://github.com/sora-xor/sora-font), [JetBrains/JetBrainsMono](https://github.com/JetBrains/JetBrainsMono)

---

## まとめ: 新規ウォッチフェイス作成のチェックリスト

新しい WFF プロジェクトを始めるときの確認順序:

1. **WFF version** を 4 に設定 (AndroidManifest)
2. **`<Editable value="true"/>`** を watch_face_info.xml に入れる
3. **静的TTF**を `res/font/` に配置、ファイル名は小文字_underscore
4. **PNG 素材** のファイル名にハイフンを使わない
5. **OFL.txt + NOTICE.md** を `LICENSES/` に同梱
6. **`<PartText>` の align は内側 `<Text>` に**、`hourFormat="24"` を使う
7. **時刻フォントが proportional** なら右寄せ方式 (`align=END`) で組む
8. **ComplicationSlot は Scene 直下**、絶対座標で配置
9. **タイル/エリアをタップ可能にする** なら最初から「Group (静的) + ComplicationSlot (動的+タップ)」のペアで設計。直接式オンリーで組むとタップ後付けが面倒
10. **AMBIENT** は早めに対応 — 時刻のデュアル要素、Group alpha 減光、秒数非表示
11. **背景グラデ** は radius=370 程度、色のメリハリを CSS より強めに
12. **実機検証** はワイヤレスADB、スクショは companion app かshell+pull (PowerShell の `>` 禁物)
13. **PIL でフォント幅実測** してからレイアウト調整するのが時短
