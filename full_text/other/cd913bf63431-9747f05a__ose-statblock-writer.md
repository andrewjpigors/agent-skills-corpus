---
name: ose-statblock-writer
description: Write OSE B/X statblocks for Foundry VTT import (v14.3+). Use Nx stacks (10x Potion of Healing) and {worn}/{stowed} for equipped weapons and armor.
applyTo: "statblock+ose+bx+dnd+foundry"
allowed-tools: []
---

# OSE Statblock Writer Skill

## Overview

This skill teaches you to write statblocks in the exact format consumed by the **OSE Statblock Importer for Foundry VTT v14** (module **v14.3.0+**). The format is a semi-colon-delimited key-value text representation of a B/X D&D (Old School Essentials, Basic D&D, Moldvay B/X) creature or character. It also supports **extended modern-OSR conventions**: ascending AC, explicit attack bonuses, named equipment, **item stack quantities** (`10x Potion of Healing` → 10/10 on the sheet), **worn/equipped markers** (`Sword +2 {worn}`, `Plate Mail {worn}` → `system.equipped`), multi-attack damage lists, spells, languages, multi-line bestiary paste, level-up/partial reimport, class-feature auto-import, and multi-block batch import.

Actors can also be **exported** back to this format via **Copy Statblock** (sheet header / actor directory). Prefer writing import-safe text that round-trips cleanly — including `Nx` stacks and `{worn}` on equipped weapons/armor.

### Agent checklist when writing equipment

Whenever you emit `Weapon:`, `Armor:`, `Equipment:`, or `Gear:` for a character or classed NPC:

1. **Stacks** — multiples use `Nx Name` (e.g. `10x Potion of Healing`), never the name repeated N times.
2. **Worn** — put ready weapons and worn armor with a trailing **`{worn}`** (e.g. `Weapon: Sword {worn}`; `Armor: Plate Mail {worn}, Shield {worn}`).
3. **Stowed** — off-hand / pack weapons use **`{stowed}`** when you want them unequipped (e.g. `Dagger {stowed}`).
4. **Pack gear** — potions, rations, rope stay unequipped unless you intentionally mark something `{worn}` (cloaks, etc.).

## Deterministic Generation Workflow

When you are asked to **generate** NPC or character statblocks rather than only
explain the format, prefer the bundled script:

`scripts/OSE_GENERATE_STATBLOCKS.py`

Use it whenever the request can be expressed as:

- AI-imagined NPCs with class, level, role, armor, weapon, or morale hints
- Book or module text that can be converted into structured NPC inputs
- User suggestions such as "make me three 2nd-level guards and a paladin
captain"

Recommended workflow:

1. Extract or infer structured inputs such as `name`, `class`, `level`,
   `armor`, `weapon`, `location`, `alignment`, `traits`, `goals`, and
   optional `equipment`.
2. Run `scripts/OSE_GENERATE_STATBLOCKS.py` for deterministic generation rather
   than hand-authoring the whole block from scratch.
3. Use the script's default `line` output as the base statblock.
4. Add or revise `Feature:` blocks manually only for details the script does
   not synthesize yet.
5. Keep the final output import-safe: no stray semicolons inside field values,
   and no explanatory prose outside the statblock unless the user asked for it.

The script already emits importer-safe fields such as `AAC`/`AC`, separate
`HD` and `SV`, explicit `Weapon:` / `Armor:` fields, `Traits:`, `Role:`, and
`Feature:` blocks for extra metadata.

Example single-NPC command:

```bash
python scripts/OSE_GENERATE_STATBLOCKS.py \
  --name "Brother Oren" \
  --class Cleric \
  --level 2 \
  --armor "chain mail" \
  --weapon "mace" \
  --location "Chapel" \
  --alignment L \
  --traits "devout, steady" \
  --equipment "holy symbol, rations" \
  --feature "Blessing|Allies within 10 ft. gain +1 morale."
```

Example batch workflow:

1. Turn the source text into a JSON array of NPC records.
2. Run `python scripts/OSE_GENERATE_STATBLOCKS.py --data-file my_npcs.json`.
3. Return the generated `line` statblocks, adjusting only edge-case flavor or
   special abilities as needed.

Useful script controls:

- `--weapon-mode auto|melee|missile` for daggers, spears, and other dual-use weapons
- `--qualities "poison, fear"` for extra `Qual` tags beyond melee/missile
- repeatable `--feature "Name|Text"` for bespoke abilities
- `--emit-class-abilities` when you want generic `Feature:` blocks even before
  compendium auto-import happens
- repeatable `--item-json '{"name":"Whetstone","type":"item","quantity":2}'`
  for deterministic rich inventory items
- `--mode inventory --apply-to "Actor Name"` for loadout-only statblocks
- `--gp`, `--sp`, `--cp`, `--ep`, `--pp` for coin object creation

If the request is for a **monster** with unusual bespoke abilities, you may
still write the statblock by hand using the field rules below, but prefer the
script first for classed NPCs, henchmen, guards, retainers, and other humanoid
characters.

## Import Modes (Mode: field)

| Mode value | Meaning |
|------------|---------|
| *(omit)* / `full` | Full import: stats + equipment + features + spells |
| `Inventory` | Gear/coins only — does not change combat stats |
| `Level-up` / `Levelup` | Updates HD, SV/saves, class features, homebrew, spells; keeps inventory and ability scores; updates HP only if `HP:` is present |
| `Partial` | Only fields listed in `Fields:` (e.g. `Fields: hd, spells`) |

```text
Mladen: Mode: Level-up; HD F2; SV F2
Mladen: Mode: Partial; Fields: hd, spells; HD F3; Spells: sleep, magic missile
Human Warrior: Mode: Inventory; Apply To: Human Warrior; Weapon: Sword; Coins: 5 gp
```

**Level-up / partial / inventory** always target an **existing** actor (open sheet, or `Apply To: Name`). They do not create new actors.

---

## Rich Inventory and Loadout Mode

When the user needs **custom items**, **metadata-aware inventory**, or a
**template that adds gear to an existing actor**, prefer these two formats.

### Item stack quantities (multiples of one item)

When an NPC or loadout has **more than one** of the same item, **do not** list the name repeatedly. Prefix (preferred) or suffix the count so Foundry gets one item with `quantity.value` / `quantity.max` (sheet shows **10/10**).

**Preferred form (always use this when writing new statblocks):**

```text
Equipment: 10x Potion of Healing, 2x Rations (standard, 7 days), 20x Torches (6)
```

| Write this | Not this |
|------------|----------|
| `10x Potion of Healing` | `Potion of Healing, Potion of Healing, …` (×10) |
| `2x Rations (standard, 7 days)` | two separate ration entries |
| `20x Arrows (quiver of 20)` only if you truly want 20 separate quivers — prefer catalog sense |

**All accepted quantity forms:**

| Syntax | Example | Result |
|--------|---------|--------|
| **`Nx Name`** (preferred) | `10x Potion of Healing` | qty 10, name `Potion of Healing` |
| `N x Name` | `10 x Potion of Healing` | same |
| `Name xN` | `Potion of Healing x10` | same |
| `Name x N` | `Potion of Healing x 10` | same |
| `N Name` | `10 Arrows` | bare count before name |
| Rich JSON | `[Potion of Healing::{"type":"item","quantity":10}]` | same via metadata |

**Rules for agents:**

1. Prefer **`Nx ItemName`** (no space required between number and `x`).
2. Put the quantity on **each list segment** that needs a stack: `10x A, 3x B, C` → A×10, B×3, C×1.
3. Parenthetical catalog names with commas are fine: `2x Rations (standard, 7 days)`.
4. Do **not** put `x` on magic bonuses: write `Sword +1`, never treat `+1` as a quantity.
5. Coins use **`Coins: 5 gp, 8 sp`**, not `5x GP` (coins have their own parser).
6. Works on `Equipment:`, `Gear:`, `Weapon:`, `Armor:`, and equipment directives inside `Notes:`.

**Full character example with stacks:**

```text
Quartermaster: AAC 12; HD F1; HP 8; MV 40; #AT 1; Dmg 1d6; ML 8; SV F1; AL N; Weapon: Sword {worn}; Armor: Leather Armour {worn}; Equipment: 10x Potion of Healing, 2x Rations (standard, 7 days), 6x Torches (6), Rope (50'), Backpack; Coins: 15 gp
```

**Inventory-only restock example:**

```text
Mladen: Mode: Inventory; Apply To: Mladen; Equipment: 5x Potion of Healing, 2x Holy Water (vial); Coins: 10 gp
```

### Worn / equipped (`{worn}` and `{stowed}`)

Trailing curly markers set OSE **`system.equipped`** so weapons are ready in hand and armor is worn (counts for AC).

**Always do this for ready combat loadouts when writing character/NPC statblocks:**

```text
Weapon: Sword +2 {worn}, Dagger {stowed}
Armor: Plate Mail {worn}, Shield {worn}
Equipment: Holy Symbol, 10x Potion of Healing, Rope (50')
```

| Marker | Meaning | Use for |
|--------|---------|---------|
| **`{worn}`** | Equip now (`equipped: true`) | Primary weapon, armor, shield; optional worn cloak |
| `{equipped}` `{held}` `{wielded}` `{ready}` | Same as `{worn}` | Aliases |
| **`{stowed}`** | Force unequipped | Backup dagger, spare weapons in pack |
| `{carried}` `{packed}` `{unequipped}` | Same as `{stowed}` | Aliases |

**Defaults (when no marker):**

| Field | Default equipped? |
|-------|-------------------|
| `Weapon: …` | **Yes** (ready) — still write `{worn}` for clarity and export round-trip |
| `Armor: …` | **Yes** (worn) — still write `{worn}` on plate/shield |
| `Equipment:` / `Gear:` | **No** — bag items; add `{worn}` only when something should be worn (e.g. cloak) |

**Combine with stacks and magic names:**

```text
Weapon: 2x Dagger {stowed}, Sword +1 {worn}
Armor: Chainmail {worn}, Shield (Steel) {worn}
Equipment: 10x Potion of Healing, Cloak of Defence {worn}
```

**Do not** put the marker inside catalog parentheses: write `Shield (Steel) {worn}`, not `Shield (Steel worn)`.

Rich JSON alternative: `[Sword::{"type":"weapon","equipped":true}]`.

### Rich item blocks

Use square-bracket item envelopes inside `Equipment:` when you need description or extra metadata beyond a plain stack:

```text
Equipment: [Oil Flask::{"type":"item","quantity":3,"weight":1}::Enough for three night watches.]
```

For plain stacks, **`10x Oil Flask` is enough** — rich blocks are optional.

Rules:

- segment 1 is the item name
- segment 2 is compact JSON metadata (`"quantity": N` sets the stack)
- segment 3 is description text
- use `||` between multiple rich items in one field
- avoid semicolons inside item descriptions

### Inventory-only mode

Use this when stats should stay untouched and only inventory should change:

```text
Human Warrior: Mode: Inventory; Apply To: Human Warrior; Weapon: Sword {worn}; Armor: Chainmail {worn}, Shield {worn}; Equipment: 2x Whetstone, 10x Potion of Healing, [Backpack::{"type":"item"}]; Coins: 5 gp, 8 sp
```

Use inventory-only mode for workflows like:

- create a naked base actor, then apply `swordsman` (mark main weapon/armor `{worn}`)
- convert one guard into an axeman or spearman with `Weapon: Battle Axe {worn}`
- add module loot and utility gear after the main import
- restock potions/rations with `Nx` quantities

---

## General Format

```
Name: KEY VALUE; KEY VALUE; KEY: VALUE; ...
```

- Fields are separated by **semi-colons** (`;`).
- Each field is either `Key: Value` (colon-separated) or `Key Value` (space-separated).
- The **name** is everything before the first colon (`:`) on a single-line block.
- For multi-block import, separate statblocks with **blank lines**.
- The parser is case-insensitive for field keys.
- Trailing punctuation (`.` `;`) on values is stripped.
- Import dialog accepts **drag-and-drop** of plain text, `.txt`/`.md` files, or journal content.

### Multi-line bestiary / book paste (v14.3+)

Name on the first line; fields on following lines (no requirement for a single `Name: …` line):

```text
Kobold
AC 7
HD 1/2
HP 3
MV 40
#AT 1
Dmg 1-4
ML 6
AL C
TT Nil
NA 4d4
```

Equivalent single-line form still works. First line may also be classic `Name: AC 7; HD …` with extra field lines below.

### Minimal valid statblock

```
Goblin: AC 6; HD 1-1; HP 4; MV 20; #AT 1; Dmg 1-6; ML 7; SV NM; AL C
```

---

## Supported Fields — Complete Reference

### 1. Name (Required)

Everything before the first colon. For monsters this is the creature name. For characters this is the character name. If missing, a warning is raised but parsing continues.

```
Mladen: AC 15; HD F1; ...
```

### 2. AC / AAC — Armor Class

Accepts both **descending** (classic B/X, lower = better) and **ascending** (modern, higher = better) AC.

| Syntax | Meaning |
|--------|---------|
| `AC 6` | Descending AC 6 (→ ascending 13) |
| `AC 15` | Ascending AC 15 (→ descending 4) |
| `AAC 15` | Explicit ascending AC 15 |
| `AC 10` | Ascending if ≥ 10, else descending (key-based heuristic) |

**Heuristic**: Plain `AC` values ≤ 10 are treated as descending B/X AC. Values > 10 are treated as ascending. Use `AAC` or `AC` + `ascending`/`descending` keyword to be explicit.

```
AC 6          — classic descending
AAC 13        — explicit ascending
AC 15         — auto-detected as ascending (> 10)
```

The parser computes both values internally. The tool will set both `system.ac.value` (descending) and `system.aac.value` (ascending) on the actor.

### 3. HD — Hit Dice

The most flexible field. Supports multiple formats:

| Format | Example | Meaning |
|--------|---------|---------|
| Monster shorthand | `2D+1` | 2d8+2 (d8 implicit, per-die +1) |
| Monster shorthand no mod | `4D` | 4d8 |
| Monster shorthand negative | `2D-2` | 2d8-4 |
| Explicit dice | `2d6` | 2d6 (no per-die bonus) |
| Explicit dice with total bonus | `2d6+1` | 2d6+1 (flat bonus, not per-die) |
| Class+Level (letter) | `F3` | Fighter 3 (d8 HD) |
| Class+Level (letter) | `MU2` | Magic-User 2 (d6 HD) |
| Class+Level (letter) | `T1` | Thief 1 (d4 HD) |
| Class+Level (letter) | `C4` | Cleric 4 (d8 HD) |
| Class+Level (letter) | `D5` | Dwarf 5 (d8 HD) |
| Class+Level (letter) | `E3` | Elf 3 (d6 HD) |
| Class+Level (letter) | `H2` | Halfling 2 (d4 HD) |
| Fractional | `1/2` | 1d4 (½ HD creature) |
| Fractional | `1/4` | 1d4 (¼ HD creature) |
| Fractional | `3/2` | 2d8 (1½ HD creature) |
| Plain number | `3` | 3d8 (monster default) |
| Normal Man | `Normal Man` | 1d4 (NH) |

**Class letter to die mapping**:

| Letter | Class | Die |
|--------|-------|-----|
| `F` | Fighter | d8 |
| `M` / `MU` | Magic-User | d6 |
| `T` | Thief | d4 |
| `C` | Cleric | d8 |
| `R` | Ranger | d6 |
| `D` | Dwarf | d8 |
| `E` | Elf | d6 |
| `H` | Halfling | d4 |
| `N` | Normal Man | d4 |

**Per-die bonus vs total bonus**:

- `2D+1` → 2d8, each die gets +1 → total bonus +2 (per-die bonus)
- `2d6+1` → 2d6, flat +1 bonus (total bonus, because die size is explicit)
- The attack value for monster THAC0 is derived from `count + (bonus * 0.5)`.

### 4. HP — Hit Points

| Format | Example | Meaning |
|--------|---------|---------|
| Parenthetical | `(12 hp)` | HP is 12 |
| Equals | `=12` | HP is 12 |
| Last number | `HD 1 (12 hp)` | Picks 12 from context |
| Monster fallback | (omitted) | Auto-computed from average HD if HP field is selected |

```
HP 12
HP (12 hp)
HP = 12
```

If HP is omitted but `selectedFields.hp` is enabled, monster actors get HP auto-computed from `ceil(count × avg(die) + bonus)`.

### 5. MV / Move / Movement — Movement Rate

Integer value. Feet per round in classic B/X terms.

```
MV 40        — 40' movement
Move 30      — 30' movement
Movement 120 — 120' (flying/swimming)
```

Only the first integer token is extracted.

### 6. ML / Morale — Morale

Integer, typically 2–12 in OSE. Warnings are raised for values outside 1–12 range.

```
ML 10
Morale 7
ML 12
```

### 7. AL / Alignment — Alignment

Free-text alignment. Trailing punctuation is stripped. **Aliases normalize to short form** `L` / `N` / `C` when recognized.

| Input | Stored |
|-------|--------|
| `L`, `Law`, `Lawful` | `L` |
| `N`, `Neutral`, `Any` | `N` |
| `C`, `Chaos`, `Chaotic` | `C` |
| Other text | Kept as trimmed free text |

```
AL L
AL Lawful
AL Chaotic
Alignment: Neutral
```

When world setting **Apply Token Defaults** is enabled, disposition is derived from alignment (Lawful friendly, Neutral neutral, Chaotic hostile).

### 8. #AT / AT / Attacks — Number of Attacks

Integer count of attacks per round. Used with multi-part `Dmg` to create **multiple Attack weapons** (v14.3+).

```
#AT 1        — 1 attack
AT 2         — 2 attacks
Attacks 3    — 3 attacks
```

The `#` prefix is optional. Weapon count = `max(#AT, number of Dmg segments)`.

### 9. Dmg / Damage — Damage Expression

The most expressive field. Supports:

| Format | Example | Parsed As |
|--------|---------|-----------|
| Range | `1-8` | `1d8` |
| Range with offset | `2-7` | `1d6+1` |
| Dice formula | `1d8` | `1d8` |
| Multi-dice | `2d6` | `2d6` |
| Dice with mod | `2d6+1` | `2d6+1` |
| Named parenthetical | `1-8 (axe)` | `1d8`, name ignored |
| **Multi-attack slash/list** | `1d6/1d8` | Two formulas → Attack + Attack 2 |
| **Multi-attack comma** | `1d6, 1d4` | Two formulas |
| Shared atk bonus | `1d6/1d8 +2 atk` | Both segments get +2 |
| **With attack bonus** | `+2 atk 1d8` | formula=`1d8`, bonus=`+2` |
| **With attack bonus** | `1d8+2 atk` | formula=`1d8`, bonus=`+2` |
| Plain number | `6` | `1d6` |

**Attack bonus notation**: Append `+N atk` or `-N atk` on a segment (or trailing on the whole list) to set attack bonus on generated Attack items.

```
Dmg 1d8+2 atk       — 1d8 damage, +2 attack bonus
Dmg +3 atk 2d6      — 2d6 damage, +3 attack bonus
Dmg 1d6/1d8         — two Attack weapons (with #AT 2 or more)
Dmg 1-8             — parsed as 1d8
```

If named `Weapon:` equipment is present, auto Attack items from Dmg are skipped (equipment wins).

**Monster attack bonus fallback**: If no explicit `+N atk` is provided, the tool derives attack bonus from HD using the B/X monster attack matrix (≤1HD → 0, 2HD → +1, 3HD → +2, etc.).

### 10. SV / Save / Saves — Saving Throw Class

One of the most important fields. It determines which save progression table to use.

**Format**: `SV <CLASS_ABBREVIATION>[<LEVEL>]`

```
SV F1         — Fighter 1
SV MU3        — Magic-User 3
SV T5         — Thief 5
SV C2         — Cleric 2
SV D4         — Dwarf 4
SV E1         — Elf 1
SV H2         — Halfling 2
SV NM         — Normal Man (fixed saves 18/18/18/18/18)
SV NH         — Normal Human (same as NM)
SV PAL3       — Paladin 3
SV BARB2      — Barbarian 2
SV RGR4       — Ranger 4
SV KNIGHT5    — Knight 5 (→ Fighter)
```

**Complete SV class alias table**:

| Input | Resolved Class Key | Display Name |
|-------|-------------------|--------------|
| `F`, `FTR`, `FIGHTER`, `K`, `KNT`, `KNIGHT`, `R`, `RGR`, `RANGER`, `RANG` | `fighter` | Fighter |
| `T`, `THF`, `THIEF`, `ACROBAT`, `ACRO`, `ASSASSIN`, `ASS`, `BARD` | `thief` | Thief |
| `C`, `CLR`, `CLERIC`, `DRU`, `DRUID` | `cleric_druid` | Cleric |
| `M`, `MU`, `MAGE`, `MAGIC-USER`, `MAGICUSER`, `ILLUSIONIST`, `ILL` | `magic_user` | Magic-User |
| `D`, `DWARF`, `DUERGAR` | `dwarf_halfling` | Dwarf |
| `H`, `HALFLING` | `dwarf_halfling` | Dwarf |
| `E`, `ELF` | `elf` | Elf |
| `DROW` | `drow` | Drow |
| `GNOME` | `gnome` | Gnome |
| `HALF-ELF`, `HALFELF` | `half_elf` | Half-Elf |
| `HALF-ORC`, `HALFORC` | `half_orc` | Half-Orc |
| `PAL`, `PALADIN` | `paladin` | Paladin |
| `BARB`, `BARBARIAN` | `barbarian` | Barbarian |
| `SVIRF`, `SVIRFNEBLIN` | `svirfneblin` | Svirfneblin |
| `NM`, `NH`, `NORMAL MAN`, `NORMAL-MAN`, `NORMALMAN`, `NORMAL HUMAN`, `NORMAL-HUMAN`, `NORMALHUMAN` | `normal_man` | Normal Man |

**If level is omitted**, the parser tries to extract level from parsed HD count or from the existing actor's HD.

**Save progression tables** are built into the parser for all classes (thief, barbarian, cleric_druid, drow, dwarf_halfling, elf, fighter, gnome, half_elf, half_orc, magic_user, paladin, svirfneblin).

### 11. Qual / Quality / Qualities — Monster Qualities

Comma or slash separated list of monster qualities. These get appended to the auto-generated Attack item name and influence weapon flags.

```
Qual melee           — Attack (melee)
Qualities undead, regenerating
Qual melee, poison   — Attack (melee, poison)
```

Qualities containing `melee` or `missile` set the corresponding weapon system flag. Other qualities are appended to the default weapon name as `Attack (quality1, quality2)`.

### 12. Notes — Freeform Notes

A catch-all field that triggers sub-parsing for **equipment directives** and **traits**.

```
Notes: armor leather+shield; weapon longsword; traits brave, loyal; role bodyguard
```

The parser extracts:

- **Equipment**: `weapon <items>`, `armor <items>`, `equipment <items>`, `gear <items>`
- **Traits**: `traits <text>` or `traits: <text>`
- **Role**: handled separately (see below)

### 13. Traits — Explicit Traits

```
Traits: brave, loyal, stubborn
Traits: undead, incorporeal, drains life
Traits direct, no-nonsense, blunt
```

Traits are written to `system.details.notes` as `<strong>traits:</strong> <value>`.

### Features (Feat / Feature / Features) — Bracketed Named Features

Named feature blocks with description text. Each feature has a `{Name}` prefix followed by its description paragraph. Multiple features are separated by the next `{Name}` marker. The key accepts `Feat`, `Feature`, or `Features` (case-insensitive).

```
Feature: {Darkvision} 60 ft. range, sees in total darkness. {Regeneration} Regains 5 HP per round at the start of each turn unless damaged by fire or acid.
```

**Behavior by actor type**:

| Actor Type | Where features go |
|---|---|
| **Monster** | Appended to `system.details.biography` as `<strong>Name</strong> Text`, features separated by blank lines |
| **Character** | Created as embedded `ability` items with generic icon (`systems/ose/assets/default/ability.png`), with `name = {Name}` and `system.description = {text}` |

**Duplicate handling**: If an ability item with the same name already exists, it is **updated** with the new description text rather than duplicated.

**Usage in statblock**:

```
Feat: {Cleave} When you reduce a foe to 0 HP, you may make one additional melee attack. {Shield Wall} Adjacent shielded allies gain +1 AC.
Feature: {Breath Weapon} 60 ft. cone, 8d6 fire damage, save vs breath for half.
Features: {Undead Nature} Does not need to eat, breathe, or sleep.
```

**Writing concise feature descriptions** — source books often devote a full paragraph or page to a single ability. For the statblock importer, distill each feature into a single sentence covering only what the DM needs at the table:

- **Damage**: dice, type, area (e.g. "8d6 fire, 60 ft. cone" not "a great blast of searing flame erupts...")
- **Save**: save type and outcome (e.g. "save vs breath for half" or "save vs spell or paralyzed")
- **Effect abbreviation**: the mechanical result in minimal words (e.g. "-2 AC for 1d4 rounds" not "the target's armor class is reduced by 2 points for a duration of...")
- **Duration**: only if it's a combat-relevant number (e.g. "2d4 turns", "1 round")
- **Omit**: flavor text, lore, narrative, multiple synonyms, and any detail the DM can improvise

**Good vs Bad examples**:

| ❌ Too verbose | ✅ Concise & actionable |
|---|---|
| `{Dragon Fear} When the dragon takes to the air and lets out a terrifying roar that shakes the very foundations of the earth, all creatures who can see or hear the dragon within a 120 foot radius must make a saving throw against spells or become frightened, suffering a -2 penalty to all attack rolls and being unable to approach the dragon for as long as they remain in its presence.` | `{Dragon Fear} 120 ft. radius, save vs spell or frightened (-2 attack, cannot approach).` |
| `{Vampiric Touch} The vampire reaches out with a deathly pale hand and upon a successful melee touch attack against a living target, the victim loses 2d6 hit points as their life force is drained away, which the vampire then adds to its own hit point total as it feeds upon their essence.` | `{Vampiric Touch} Melee touch, 2d6 necrotic, heals vampire equal damage.` |
| `{Spellcasting} The lich is an accomplished spellcaster of immense power, having studied the arcane arts for centuries beyond counting, and can cast the following prepared spells using its Intelligence as its spellcasting ability, with a spell save DC of 20 and a +12 bonus to hit with spell attacks.` | `{Spellcasting} INT, DC 20, +12 atk. At will: detect magic, mage hand. 3/day: fireball, counterspell. 1/day: power word kill.` |

### 14. Role — Combat Role

```
Role: bodyguard
Role: scout, trap-finder
Role straightforward escort
```

Stored in `parsed.role`. Descriptive text about the creature's combat function.

### 15. Weapon / Armor / Equipment / Gear — Equipment Directives

Explicit equipment fields that bypass notes parsing. Each accepts comma, slash, `and`, or `+` separated lists. Each segment may carry an **inline quantity** (`Nx` / `xN`).

```
Weapon: longsword, dagger
Armor: leather+shield
Equipment: 10x Potion of Healing, 2x Rations (standard, 7 days), rope
Gear: grappling hook, crowbar
```

**Split rules** for equipment lists:

- Commas: `longsword, dagger` (commas **inside parentheses** stay part of the name, e.g. `Rations (standard, 7 days)`)
- Slashes: `leather/shield`
- `and`: `rope and torches`
- ` + `: `leather + shield`
- Adjacent `+`: `leather+shield` (but NOT `axe+1` — magical notation is preserved)

**Quantities / stack sizes** (→ OSE `system.quantity.value` and `.max`, sheet shows **N/N**):

| Syntax | Example | Notes |
|--------|---------|--------|
| **`Nx Name`** | `10x Potion of Healing` | **Preferred** when writing statblocks |
| `N x Name` | `3 x Holy Water (vial)` | spaces allowed |
| `Name xN` | `Potion of Healing x10` | suffix form |
| `Name x N` | `Torch x 6` | suffix with space |
| `N Name` | `10 Arrows` | bare count; name must start with a letter |
| Rich JSON | `[Name::{"quantity":10}]` | when description/metadata also needed |

**Worn / equipped** (→ OSE `system.equipped = true` — weapon in hand, armor worn):

| Syntax | Example | Effect |
|--------|---------|--------|
| **`Name {worn}`** | `Sword +2 {worn}` | Equipped / ready (preferred marker) |
| `{equipped}` `{held}` `{wielded}` `{ready}` | `Shield {held}` | Same as `{worn}` |
| `{stowed}` `{carried}` `{unequipped}` | `Dagger {stowed}` | Force **not** equipped |
| Defaults | `Weapon: Sword` / `Armor: Chainmail` | From `Weapon:` / `Armor:` fields, equipped **by default** even without marker |
| Gear list | `Equipment: Cloak of Defence {worn}` | Must mark `{worn}` — bag items stay unequipped otherwise |

```
Weapon: Sword +2 {worn}, Dagger {stowed}
Armor: Plate Mail {worn}, Shield {worn}
Equipment: 10x Potion of Healing, 2x Rations (standard, 7 days), Rope (50'), Holy Symbol
```

→ sword ready, dagger stowed, plate + shield worn, potions/rations in pack.

Combine with stacks: `2x Dagger {stowed}`, `Sword {worn}`.

See **Item stack quantities** under Rich Inventory for agent writing rules.

Each directive feeds into the equipment container with structured requests (`name` + `quantity`):

```
parsed.equipment = {
  weapons: [{ name, quantity, … }],
  armors: […],
  gear: [{ name: "Potion of Healing", quantity: 10 }, …],
  coins: […]
}
```

### 16. Literacy — Literacy Status

```
Literacy: literate
Literacy: illiterate
```

Appended to notes as `Literacy: <value>`.

### 17. Spells / Spell / Spell List — Spell import (v14.3+)

Named spells are matched against loaded Item packs (`type: spell`) and created on the actor.

```
Spells: sleep, magic missile, shield
Spell: Charm Person
```

Slot-only shorthand is accepted but **does not** create spell items:

```
Spells: 2/1
```

Produces a warning; prefer named spells for Foundry. Optionally recorded as notes.

### 18. Languages / Lang — Spoken languages (v14.3+)

Comma-separated list written into actor notes as `Languages: …`.

```
Languages: Common, Elvish, Alignment tongue
Lang: Common, Dwarvish
```

### 19. TT / Treasure Type, NA / Number Appearing, SA / Special Attacks (v14.3+)

Bestiary book fields:

| Key | Example | Effect |
|-----|---------|--------|
| `TT` / `Treasure Type` | `TT: E` | Notes: Treasure Type |
| `NA` / `Number Appearing` | `NA: 4d4` | Notes: Number Appearing |
| `SA` / `Special Attacks` | `SA: breath weapon 30 ft` | Feature `{Special Attacks}` text |

```
Kobold: AC 7; HD 1/2; ML 6; AL C; TT Nil; NA 4d4; SA pack tactics
```

### 20. Fields — Partial mode field list (v14.3+)

Used with `Mode: Partial`. Comma-separated field keys to apply:

```
Mode: Partial; Fields: hd, sv, spells, features
```

Recognized names include: `name`, `ac`, `hd`, `hp`, `mv`, `ml`, `al`, `at`, `dmg`, `abilities`, `notes`, `qualities`, `equipment`, `features`, `spells`, `languages` (and aliases like `damage`, `gear`, `saves`).

### 21. Mode / Apply To / Coins — Import control fields

| Key | Example | Effect |
|-----|---------|--------|
| `Mode` | `Mode: Level-up` | `full` (default), `Inventory`, `Level-up` / `Levelup`, `Partial` |
| `Apply To` | `Apply To: Mladen` | Target existing actor by name (required when no sheet is open for inventory/level-up/partial) |
| `Coins` | `Coins: 5 gp, 8 sp` | Creates coin item objects (`gp`/`sp`/`cp`/`ep`/`pp`) |

Also accepted as equipment-style keys: `coins`, `loadout`, `inventory`, `treasure` (feed the equipment/coins container). See **Import Modes** above.

### 22. Abilities — Ability Scores

Six standard B/X abilities. Can be parsed inline from any token that starts with an ability name, or extracted from the full body text.

**Supported ability names**:

- `Str` / `Strength`
- `Dex` / `Dexterity`
- `Con` / `Constitution`
- `Int` / `Intelligence`
- `Wis` / `Wisdom`
- `Cha` / `Charisma`

**Format variants**:

```
; Str 10 Dex 8 Con 6 Int 16 Wis 8 Cha 13
; Strength: 10 Dexterity: 8 Constitution: 6
; Str=10 Dex=8 Con=6 Int=16 Wis=8 Cha=13
```

The regex extracts `ability_name [:=]? number` patterns from anywhere in the body. Values can be negative.

---

## Character vs Monster Statblocks

### Monster Statblock (Minimal)

```
Kobold: AC 7; HD 1/2; MV 40; #AT 1; Dmg 1-4; ML 6; SV NM; AL C
```

### Monster Statblock (Full Extended)

```
Great Wyrm: AC 18; HD 8D+4; HP 52; MV 30 fly 60; #AT 3; Dmg 2d8+3 atk / 1d6 / 1d6; ML 11; SV F8; AL C; Qual melee, fear; Notes: armor scale; Traits: breath weapon (60ft cone, 8d6 fire), fear aura (60ft, save vs spell); Role solo dragon
```

### Character Statblock

```
Mladen: AAC 15; HD F1; HP 11; MV 20; #AT 1; Dmg +2 atk 1d8; ML 10; SV F1; AL N; Str 10 Dex 6 Con 6 Int 16 Wis 8 Cha 13; Weapon: Sword {worn}; Armor: Leather Armour {worn}, Shield {worn}; Traits: direct, no-nonsense, blunt; Role: bodyguard
```

### Henchman / Classed NPC

```
Aelric: AAC 14; HD C3; HP 18; MV 30; #AT 1; Dmg 1d6; ML 8; SV C3; AL L; Str 12 Dex 9 Con 10 Int 13 Wis 16 Cha 11; Weapon: Mace {worn}; Armor: Chainmail {worn}; Traits: devout, healer; Role: support caster
```

### Maximum Valid Monster Statblock (all monster-applicable fields)

```
Elder Lich: AC 20; HD 18D+4; HP 90; MV 30; #AT 2; Dmg 1d10+8 atk; ML 12; SV MU18; AL C; Qual undead, melee, magic; Notes: armor Bracers of Armour; weapon Wand of Paralysation, Dagger +1; equipment Cloak of Defence, Crystal Ball with ESP, Spell Scroll; traits paralyzing touch (save vs paralysis or paralyzed 2d4 turns), spellcasting (MU18), phylactery (cannot be destroyed until phylactery is found), immune to non-magical weapons, immune to cold and lightning, immune to charm and sleep; Feature: {Paralyzing Touch} Target must save vs paralysis or be paralyzed for 2d4 turns. {Spellcasting} Casts spells as an 18th-level Magic-User (5/5/5/5/4/4/3/3/2). {Phylactery} Cannot be permanently destroyed until its phylactery is located and destroyed. {Turn Resistance} +4 bonus to all saves against turning attempts; Role solo spellcaster
```

### Maximum Valid Character Statblock (all character-applicable fields)

```
Ser Vex: AC 19; HD PAL6; HP 48; MV 20; #AT 2; Dmg 1d8+4 atk; ML 11; SV PAL6; AL L; Str 17 Dex 12 Con 15 Int 13 Wis 16 Cha 18; Notes: armor Plate Mail +2+Shield +1; weapon Sword +2; equipment Potion of Healing, Holy Symbol, Rations (standard 7 days), Rope (50'); traits devout, inspiring, fearless, tactical; Feature: {Cleave} When you reduce a foe to 0 HP, you may make one additional melee attack against another target within reach. {Shield Wall} While adjacent to an ally who also wields a shield, both of you gain +1 AC. {Battle Cry} Once per combat, all allies within 30 ft. gain +1 to attack rolls for 1 round; role front-line commander; Literacy literate
```

---

## Multi-Block Import

Separate statblocks with one or more **blank lines**. Each block is parsed independently.

```
Mladen: AC 15; HD F1; HP 11; MV 20; #AT 1; Dmg 1d8+2 atk; ML 10; SV F1; AL N; Notes: armor leather+shield; weapon longsword

Kobold: AC 7; HD 1/2; MV 40; #AT 1; Dmg 1-4; ML 6; SV NM; AL C; Notes: small dog-faced humanoids, often with spears or slings

Aelric: AC 14; HD C3; HP 18; MV 30; #AT 1; Dmg 1d6; ML 8; SV C3; AL L; Str 12 Dex 9 Con 10 Int 13 Wis 16 Cha 11; Notes: armor chain; weapon mace
```

**Targeting rules (v14.2+)**:

- **Single block** with an open actor sheet → applies to that actor.
- **Multi-block** → open actor is updated only when the parsed **name matches** the open actor; other blocks create new actors.
- **Inventory / Level-up / Partial** → always need an existing actor (`Apply To:` or open sheet).

Optional world settings for **new** actors only:

- Import folder path (e.g. `Imported/Monsters`)
- Name prefix / suffix

---

## Export (Copy Statblock)

Use sheet header **Copy Statblock** or the actor directory context menu. Output is import-safe text for characters and monsters (core combat fields, equipment for PCs, multi-weapon Dmg for monsters when present).

**Item stacks**: gear/weapons/armor with `quantity.value` (or max) greater than 1 export as `Nx Name` (e.g. 10 potions → `10x Potion of Healing`). Qty 1 stays a bare name.

**Worn**: equipped weapons/armor export with a trailing `{worn}` (e.g. `Sword +2 {worn}`, `Plate Mail {worn}`).

Round-trips cleanly with import.

---

## Equipment Matching Logic

When equipment directives are present, the tool:

1. **Canonicalizes** the name against `data/ose-equipment-stubs.json` (a catalog of ~500+ OSE equipment items with normalized names across weapons, armor, shields, and gear)
2. **Searches all Item compendiums** for the best match using a scoring algorithm
3. **Creates embedded items** from compendium documents or as placeholder items depending on the `characterWeaponArmorImportMode` setting

**Matching algorithm**:

- Exact normalized match: +300 score
- Starts-with / prefix match: +220
- Contains / substring match: +180
- Token overlap: +40 per matching word
- Magic bonus alignment penalties: non-magical requests penalize magical matches unless explicitly requested
- Minimum score threshold for acceptance: 80 for compendium items, 120 for name canonicalization

### Explicit Magic Item Matching

To request a magical weapon, use `+N` notation:

```
Weapon: sword+2      — explicitly requests a +2 sword
Weapon: axe+1        — explicitly requests a +1 axe
Weapon: longsword    — prefers non-magical longsword
```

---

## Class Feature Auto-Import

For **character** actors (type=`"character"`), the tool auto-imports class abilities from the `ose-advancedfantasytome.abilities` compendium when an SV class with a valid feature mapping is parsed.

**How it works**:

1. The parser resolves `parsed.sv.class` to a `featureClass` via `FEATURE_CLASS_MAP`
2. Looks up that class key in `data/ose-advanced-tome-ability-class-map.json`
3. For each mapped ability, checks if the actor already has it (by compendium source UUID)
4. If not present, imports the ability from the compendium

**Feature class alias table** (extended, used for class ability lookup):

| Input | Feature Class | Display |
|-------|-------------|---------|
| `FIGHTER`, `FTR`, `F` | `fighter` | Fighter |
| `KNIGHT`, `KNT`, `K` | `knight` | Knight |
| `RANGER`, `RGR`, `RANG` | `ranger` | Ranger |
| `PALADIN`, `PAL` | `paladin` | Paladin |
| `THIEF`, `THF`, `T` | `thief` | Thief |
| `ACROBAT`, `ACRO` | `acrobat` | Acrobat |
| `ASSASSIN`, `ASS` | `assassin` | Assassin |
| `BARD` | `bard` | Bard |
| `CLERIC`, `CLR`, `C` | `cleric` | Cleric |
| `DRUID`, `DRU` | `druid` | Druid |
| `MAGIC-USER`, `MAGICUSER`, `MU`, `M`, `MAGE` | `magic-user` | Magic-User |
| `ILLUSIONIST`, `ILL` | `illusionist` | Illusionist |
| `DWARF`, `DWF`, `D` | `dwarf` | Dwarf |
| `DUERGAR` | `duergar` | Duergar |
| `ELF`, `E` | `elf` | Elf |
| `DROW`, `DRW` | `drow` | Drow |
| `GNOME`, `G` | `gnome` | Gnome |
| `HALF-ELF`, `HALFELF`, `HE` | `half-elf` | Half-Elf |
| `HALF-ORC`, `HALFORC`, `HO` | `half-orc` | Half-Orc |
| `HALFLING`, `HLF`, `H` | `halfling` | Halfling |
| `SVIRFNEBLIN`, `SVIRFNEBLLIN`, `SVIRF` | `svirfneblin` | Svirfneblin |
| `BARBARIAN`, `BARB` | `barbarian` | Barbarian |

Note that the **feature class** resolution is more granular than **SV class** — for example, Knight and Ranger resolve to `fighter` for saves but to `knight` and `ranger` for feature import.

### Avoiding Duplicate Class Feature Imports

The tool uses **compendium source UUID tracking**: each imported item gets a `flags.core.sourceId` set to `Compendium.<compendiumId>.Item.<itemId>`. Before importing, the tool checks if any existing item has that sourceId — if so, it skips.

---

## Damage → Attack Item Generation

For **monsters** and **placeholder-mode characters**, when no `Weapon:` equipment is listed, the tool auto-generates Attack weapon item(s) from the damage field:

- **Count**: `max(#AT, number of slash/comma Dmg segments)`
- **Names**: `Attack`, `Attack 2`, … (plus quality suffix when present)
- **Damage formula**: each segment of the Dmg list
- **Attack bonus**: per-segment or shared `+N atk`, else HD-derived for monsters
- **Qualities**: `melee`/`missile` set corresponding weapon flags
- **Updating**: matching Attack names are **updated** rather than duplicated

```
Beast: AC 5; HD 4; #AT 2; Dmg 1d6/1d8; ML 8; AL N
```

Creates `Attack` (1d6) and `Attack 2` (1d8).

---

## HD → Attack Bonus (Monster THAC0)

When no explicit `+N atk` is provided, monster attack bonus is derived:

| HD Value | Attack Bonus |
|----------|-------------|
| ≤ ½ | -1 |
| 1 | 0 |
| 2 | +1 |
| 3 | +2 |
| 4 | +3 |
| 5 | +4 |
| 6 | +5 |
| 7 | +6 |
| 8–9 | +7 |
| 10–11 | +8 |
| 12–13 | +9 |
| 14–15 | +10 |
| 16–17 | +11 |
| 18–19 | +12 |
| 20–21 | +13 |
| 22+ | +14 |

---

## Token HP Reroll on Placement

Monsters with explicit HD but without a separate HP field get HP auto-computed. Additionally, when an unlinked monster token is placed on the canvas, the module can **reroll HP from hit dice** for that individual token (configurable via `rerollMonsterHpOnPlacement` setting).

---

## Strict vs Lenient Mode

| Mode | Behavior |
|------|----------|
| **Strict** | Unknown tokens become errors. AC and HP are required. All unknown field segments cause parse failure. |
| **Lenient** | Unknown tokens are reported as warnings. Missing AC/HP produce warnings only. Parsing continues with available data. |

---

## Parse Confidence Scoring

The parser computes confidence scores internally, and the dialog surfaces live
warnings/errors while you type:

- **≥75% + zero errors** → 🟢 Good
- **45–74%** → 🟡 Warn
- **<45% or any errors** → 🔴 Error

Score is calculated as `(parsed_fields / total_fields) × 100 - errors×20 - warnings×5 - unknown×4`.

---

## Complete Field Key Reference

Confidence / selection keys in `FIELD_KEYS` (v14.3+):

1. `name` — Actor name
2. `ac` — Armor Class
3. `hd` — Hit Dice
4. `hp` — Hit Points
5. `mv` — Movement
6. `ml` — Morale
7. `al` — Alignment
8. `at` — Number of Attacks
9. `dmg` — Damage (incl. multi-segment lists)
10. `abilities` — Ability Scores
11. `notes` — Notes (traits, TT/NA/languages extras)
12. `qualities` — Monster Qualities
13. `equipment` — Equipment container
14. `features` — Bracketed `Feature:` blocks
15. `spells` — Named spell list
16. `languages` — Language list

Additional parse-only / mode fields (not all scored the same way):

- `Mode`, `Apply To`, `Fields`, `TT`, `NA`, `SA`, `Literacy`, `Role`, `Weapon`/`Armor`/`Gear`/`Coins`

---

## Best Practices for Writing Statblocks

### Do

1. **Always include a name** (single-line before first colon, or multi-line first line)
2. **Use consistent separators** — semi-colons between fields (or one field per line in multi-line form)
3. **Include SV class with level** — `SV F3` not just `SV F`
4. **Use ascending AC for characters**, descending for classic monsters
5. **Multi-attack**: use `#AT n` with `Dmg a/b/c` rather than one formula only
6. **Named spells** for casters (`Spells: sleep, …`) not only slot shorthand
7. **Level-up** with `Mode: Level-up` so gear is not wiped
8. **Include all six abilities** for characters
9. **Keep traits comma-separated** for clean notes output
10. **Use multi-block with blank lines** for batch imports; match names when updating open actors
11. **Stack multiples with `Nx`** — write `10x Potion of Healing`, never repeat the name ten times
12. **Use exact catalog item names** with quantities: `2x Rations (standard, 7 days)`, `3x Holy Water (vial)`
13. **Mark ready gear with `{worn}`** — `Weapon: Sword {worn}`; `Armor: Plate Mail {worn}, Shield {worn}` so weapons are in hand and armor applies

### Don't

1. Don't use `:` in field values unless it's `key: value` format — it will split incorrectly
2. Don't use `;` inside field values — it's the field delimiter
3. Don't put abilities in a separate block from the main statblock
4. Don't rely on auto-detected AC without understanding the ≤10 heuristic
5. Avoid `axe+1` next to `shield` in equipment — the `+` between letters triggers a split (`leather+shield` → `["leather", "shield"]`) while `axe+1` is preserved
6. Don't invent stack syntax like `Potion of Healing (10)` or `Potion of Healing ×10` without `x` — use `10x Potion of Healing`
7. Don't list the same consumable ten times as ten comma segments
8. Don't put `{worn}` inside parentheses of catalog names — use a trailing marker: `Shield (Steel) {worn}` not `Shield (Steel worn)`

---

## Advanced Examples

### High-Level Character with Class Features

```
Seraphina: AC 18; HD PAL5; HP 45; MV 20; #AT 1; Dmg 1d8+3 atk; ML 10; SV PAL5; AL L; Str 16 Dex 10 Con 14 Int 12 Wis 15 Cha 17; Weapon: Sword +2 {worn}; Armor: Plate Mail {worn}, Shield {worn}; Traits: devout, inspiring, fearless; Role: front-line healer
```

### Dragon (Full Monster)

```
Elder Red Dragon: AC 24; HD 11D; HP 66; MV 30 fly 90; #AT 3; Dmg 2d8+5 atk / 2d8+5 atk / 2d10+5 atk; ML 11; SV F11; AL C; Qual melee, fire, fear; Notes: traits breath weapon (90ft cone, 11d6 fire, save vs breath for half), fear aura (90ft, save vs spell), magic resistance 40%; Role solo dragon
```

### Undead with Special Qualities

```
Wraith: AC 15; HD 4D; HP 20; MV 40 fly 60; #AT 1; Dmg 1d6+4 atk; ML 12; SV F4; AL C; Qual undead, incorporeal, energy drain; Notes: traits energy drain (1 level per hit, save vs death), immune to non-magical weapons, silver or magic to hit; Role ambush predator
```

### Batch: NPC Party

```
Captain Varro: AC 16; HD F4; HP 28; MV 30; #AT 1; Dmg 1d8+1 atk; ML 9; SV F4; AL L; Str 15 Dex 12 Con 13 Int 10 Wis 11 Cha 14; Notes: armor chain+shield; weapon longsword+1; traits disciplined, tactical; role party leader

Scribe Tessa: AC 12; HD MU2; HP 8; MV 40; #AT 1; Dmg 1d4-1 atk; ML 6; SV MU2; AL N; Str 8 Dex 14 Con 9 Int 17 Wis 12 Cha 10; Notes: equipment spellbook, component pouch, ink and quill; traits curious, bookish; role knowledge expert

Brother Oren: AC 13; HD C3; HP 18; MV 30; #AT 1; Dmg 1d6; ML 8; SV C3; AL L; Str 11 Dex 8 Con 12 Int 13 Wis 16 Cha 12; Notes: armor leather; weapon mace; traits devout, healer, pacifist; role support healer
```

### Classic B/X Monster (Minimal)

```
Orc: AC 6; HD 1; HP 5; MV 40; #AT 1; Dmg 1-8; ML 8; SV F1; AL C
Gelatinous Cube: AC 8; HD 4; HP 18; MV 20; #AT 1; Dmg 2-8; ML 12; SV F2; AL N; Qual undead, ooze, paralysis; Notes: traits transparent (surprise on 1-4), paralysis (2d4 turns, save vs paralysis), immune to cold and lightning; Role dungeon hazard
```

### Extended Format with All Fields

```
Shadow Knight: AC 19; HD 6D+3; HP 33; MV 30; #AT 2; Dmg 1d10+4 atk; ML 11; SV F6; AL C; Str 17 Dex 14 Con 15 Int 13 Wis 12 Cha 16; Qual melee, necrotic; Notes: armor plate; weapon greatsword+2; equipment black cloak, unholy symbol; traits incorporeal step (phase through walls), death strike (crit on 19-20), immune to fear; role elite commander; Literacy literate
```

### Multi-attack monster (slash Dmg)

```
Owlbear: AC 5; HD 5; HP 30; MV 40; #AT 3; Dmg 1d8/1d8/1d8; ML 9; SV F3; AL N; Qual melee
```

### Caster with named spells (v14.3+)

```
Apprentice Voss: AAC 11; HD MU1; HP 4; MV 40; #AT 1; Dmg 1d4; ML 7; SV MU1; AL N; Str 8 Dex 12 Con 9 Int 16 Wis 11 Cha 10; Weapon: Dagger {worn}; Spells: sleep, charm person, read magic; Languages: Common, Alignment tongue; Traits: nervous, bookish; Role: apprentice
```

### Multi-line bestiary paste (v14.3+)

```
Kobold
AC 7
HD 1/2
HP 3
MV 40
#AT 1
Dmg 1-4
ML 6
AL C
TT Nil
NA 4d4
SA pack tactics
```

### Level-up existing PC (v14.3+)

```
Mladen: Mode: Level-up; HD F2; SV F2
```

(with the character sheet open, or `Apply To: Mladen`). Inventory and ability scores are kept; HP updates only if `HP:` is present; class features/homebrew re-apply from the new SV. Casters can add `Spells: …` on the same line.

### Partial field reimport (v14.3+)

```
Mladen: Mode: Partial; Fields: hd, spells; HD F3; Spells: sleep, magic missile
```

### Character with stacked consumables (`Nx` quantities)

```
Alchemist Mira: AAC 11; HD MU2; HP 6; MV 40; #AT 1; Dmg 1d4; ML 7; SV MU2; AL N; Str 8 Dex 13 Con 9 Int 16 Wis 12 Cha 11; Weapon: Dagger {worn}; Equipment: 10x Potion of Healing, 3x Potion of Fire Resistance, 2x Rations (standard, 7 days), 6x Torches (6), Rope (50'), Backpack; Coins: 12 gp, 5 sp; Spells: sleep, detect magic; Traits: careful, thrifty; Role: party alchemist
```

### Inventory restock with stacks

```
Alchemist Mira: Mode: Inventory; Apply To: Alchemist Mira; Equipment: 5x Potion of Healing, 2x Holy Water (vial); Coins: 3 gp
```

### Ready weapons and worn armor (`{worn}`)

```
Ser Aldric: AAC 18; HD PAL5; HP 40; MV 20; #AT 1; Dmg 1d8+2 atk; ML 10; SV PAL5; AL L; Str 16 Dex 10 Con 14 Int 11 Wis 15 Cha 17; Weapon: Sword +2 {worn}, Dagger {stowed}; Armor: Plate Mail +1 {worn}, Shield {worn}; Equipment: Holy Symbol, 10x Potion of Healing, 2x Rations (standard, 7 days), Rope (50'); Traits: devout, inspiring; Role: front-line commander
```

---

## Quick Reference Card

### Single-line (core)

```
NAME: AC <n|AAC n>; HD <class+level|monsterHD>; HP <n>; MV <n>; #AT <n>; Dmg <dice|range|a/b/c>[+n atk]; ML <n>; SV <CLASS><LEVEL>; AL <L|N|C|Lawful|…>; [Str n Dex n …]; [Weapon: Name {worn}|Name {stowed}]; [Armor: Name {worn}]; [Equipment: Nx Name, …]; [Notes: …]; [Qual <q1, q2>]; [Feature: {Name} text.]; [Spells: name, name]; [Languages: …]; [TT/NA/SA …]; [Literacy <status>]; [Mode: …]; [Apply To: …]; [Fields: …]; [Coins: n gp]
```

### Item stacks (multiples)

```
Equipment: 10x Potion of Healing, 2x Rations (standard, 7 days), Rope (50')
Weapon: 2x Dagger
Gear: 3x Holy Water (vial)

# also valid:
Equipment: Potion of Healing x10
Equipment: [Potion of Healing::{"type":"item","quantity":10}]
```

### Worn / equipped

```
Weapon: Sword +2 {worn}, Dagger {stowed}
Armor: Plate Mail {worn}, Shield {worn}
Equipment: Holy Symbol, Cloak of Defence {worn}
```

### Multi-line bestiary

```
NAME
AC n
HD …
…
TT …
NA …
```

### Import modes

```
NAME: Mode: Inventory; Apply To: NAME; Weapon: …; Coins: …
NAME: Mode: Level-up; HD F2; SV F2
NAME: Mode: Partial; Fields: hd, spells; HD F3; Spells: sleep
```

### Multi-attack / multi-block

```
NAME: #AT 2; Dmg 1d6/1d8; …

Block A: …

Block B: …
```

(blank line between blocks)

---

## Parser Pipeline Summary

```
Input Text
  → splitBlocks()      — blank-line separated multi-block paste
  → _prepare()         — name + body:
                         • classic "Name: fields…" at first ":"
                         • multi-line bestiary: first line = name,
                           following lines joined with "; "
  → _tokenize()        — split body by ";" → {key, value, raw} tokens
  → _consumeToken()    — match each token (AC, HD, Dmg list, Mode,
                         Spells, TT/NA/SA, Languages, Fields, …)
  → _extractAbilities()— scan body for ability score pattern
  → _normalizeAndValidate() — import mode, alignment L/N/C, completeness
  → _computeConfidence()    — score parse quality (FIELD_KEYS v14.3+)
  → applyToActor()     — full / inventory / level-up / partial
```

Unknown tokens are collected and surfaced as live warnings in the dialog. In
strict mode, unknown tokens cause errors. In lenient mode, they generate
warnings. Multi-segment `Dmg` and `#AT` drive multi-weapon Attack creation
when no named `Weapon:` equipment is present.

---

# OSE Equipment & Item Catalogs

> **CRITICAL**: When writing statblocks with equipment directives (`weapon:`, `armor:`, `equipment:`, `gear:`), you MUST use exact names from these catalogs. The importer's matching algorithm scores against these canonical names. Using exact names guarantees perfect recognition. The normalized matching is forgiving, but exact matches score highest (300 points vs 120-220 for fuzzy).

## How Equipment Matching Works

The importer performs a two-stage equipment resolution:

1. **Name Canonicalization**: The requested name is normalized and matched against the `ose-equipment-stubs.json` catalog below. The best-scoring canonical name replaces the input. Score >= 120 needed.
2. **Compendium Lookup**: The canonicalized name is then searched across ALL loaded Item compendiums. Score >= 80 needed.

**Scoring factors**: exact match (300), prefix match (220), substring (180), word overlap (+40/word), magic bonus alignment (±80-140). Non-magical requests penalize magical matches unless `+N` is explicitly used.

---

## WEAPON CATALOG (use exact names for `weapon:` directive)

### Non-Magical Weapons

```
Arrows (quiver of 20), Battle Axe, Club, Crossbow, Crossbow bolts (case of 30),
Dagger, Halberd, Hammer (small), Hand axe, Javelin, Lance, Long bow, Mace,
Oil flask (burning), Polearm, Short bow, Short sword, Silver dagger,
Silver tipped arrow (1), Sling, Sling Stones, Spear, Staff, Sword,
Swords (generic), Torch, Two-handed sword, War hammer
```

### Magical Weapons (append `+N` or use full name)

```
Arrows +1, Arrows +2, Arrow +1 Slaying, Arrow of Location,
Axe +1, Axe +2, Bow +1,
Crossbow +1 Distance, Crossbow +1 Speed, Crossbow +2 Accuracy,
Crossbow Bolts +1, Crossbow Bolts +2,
Dagger +1, Dagger +1 Buckle, Dagger +1 Throwing, Dagger +1 Venomous,
Dagger +2 +3 vs orcs goblins and kobolds, Dagger +2 Biter,
Mace +1, Mace +1 Disrupting, Mace +2, Mace +3,
Short Sword +2 Quickness,
Sling +1, Sling Bullet +1 Impact,
Spear +1, Spear +2, Spear +3, Spear -1 Backbiter (Cursed),
Sword +1, Sword +2, Sword +3,
Sword +1 +2 vs Lycanthropes, Sword +1 +2 vs Spell Users,
Sword +1 +3 vs Dragons, Sword +1 +3 vs Enchanted Creatures,
Sword +1 +3 vs Regenerating Creatures, Sword +1 +3 vs Reptiles,
Sword +1 +3 vs Shape Changers, Sword +1 +3 vs Undead,
Sword +1 Dragon Slayer, Sword +1 Energy Drain, Sword +1 Flaming,
Sword +1 Frost Brand, Sword +1 Giant Slayer, Sword +1 Light,
Sword +1 Locate Objects, Sword +1 Luck Blade, Sword +1 Sharpness,
Sword +1 Sun Blade, Sword +1 Wishes, Sword +1 Wounding,
Sword +2 Charm Person, Sword +2 Dancing, Sword +2 Nine Lives Stealer,
Sword +2 Venger, Sword +2 Vorpal, Sword +3 Defender, Sword +3 Holy Avenger,
Sword -1 Berserker (Cursed), Sword -1 Cursed, Sword -2 Cursed,
Trident +1 Fish Command, Trident +1 Submission, Trident +2 Warning,
Trident -2 Yearning (Cursed),
War Hammer +1, War Hammer +2, War Hammer +3 Dwarven Thrower,
War Hammer +3 Thunderbolts
```

### Staves, Rods, and Wands (magical weapons)

```
Staff +1 Growing, Staff of Commanding, Staff of Dispelling, Staff of Healing,
Staff of Power, Staff of Snakes, Staff of Striking, Staff of Swarming Insects,
Staff of Withering, Staff of Wizardry, Staff of the Healer, Staff of the Woodlands,
Immovable Rod, Rod of Cancellation, Rod of Lordly Might, Rod of Parrying,
Rod of Striking,
Wand of Cold, Wand of Enemy Detection, Wand of Fear, Wand of Fire Balls,
Wand of Illusion, Wand of Lightning Bolts, Wand of Magic Detection,
Wand of Magic Missiles, Wand of Metal Detection, Wand of Negation,
Wand of Paralysation, Wand of Polymorph, Wand of Radiance,
Wand of Secret Door Detection, Wand of Summoning, Wand of Trap Detection
```

---

## ARMOR CATALOG (use exact names for `armor:` directive)

### Non-Magical Armor

```
Armour (generic), Chainmail, Dog armour, Horse barding, Leather Armour, Plate Mail
```

### Magical Armor

```
Chainmail +1, Chainmail +2, Chainmail +3,
Leather Armour +1, Leather Armour +2, Leather Armour +3,
Plate Mail +1, Plate Mail +2, Plate Mail +3,
Bracers of Armour
```

### Cursed Armor

```
Cursed Chainmail -1, Cursed Chainmail -2,
Cursed Leather Armour -1, Cursed Leather Armour -2,
Cursed Plate Mail -1, Cursed Plate Mail -2
```

### Helms

```
Helm of Alignment Changing, Helm of Reading Languages and Magic,
Helm of Telepathy, Helm of Teleportation
```

---

## SHIELD CATALOG (use exact names for `armor:` directive with shield)

```
Shield, Shield (Steel), Shield (Wood), Shield +1, Shield +2, Shield +3,
Cursed Shield -1, Cursed Shield -2, Brooch of Shielding
```

> **Note**: When using `armor leather+shield`, the `+` splits into `["leather", "shield"]`. The importer matches "shield" against the shield catalog. Use exact shield names like `Shield (Steel)` or `Shield +1` for precise matching.

---

## GEAR & ADVENTURING EQUIPMENT CATALOG (use for `equipment:` or `gear:` directives)

### Standard Adventuring Gear

```
Backpack, Crowbar, Garlic, Grappling Hook, Holy Symbol, Holy Water (vial),
Iron Spikes (12), Lantern, Mirror (hand-sized steel), Oil (1 flask),
Pole (10' long wooden), Rations (iron, 7 days), Rations (standard, 7 days),
Rope (50'), Sack (large), Sack (small), Saddle and bridle, Saddle bags,
Stakes (3) and Mallet, Thieves' Tools, Tinder Box (flint & steel),
Torches (6), Waterskin, Wine (2 pints), Wolfsbane (1 bunch), GP
```

### Poisons

```
Bloodstream Poison: I, Bloodstream Poison: II, Bloodstream Poison: III, Bloodstream Poison: IV,
Ingested Poison: I, Ingested Poison: II, Ingested Poison: III,
Ingested Poison: IV, Ingested Poison: V
```

### Potions (use full names)

```
Potion of Clairaudience, Potion of Clairvoyance, Potion of Control,
Potion of Control Animal, Potion of Control Dragon, Potion of Control Giant,
Potion of Control Human, Potion of Control Plant, Potion of Control Undead,
Potion of Delusion, Potion of Diminution, Potion of ESP, Potion of Fire Resistance,
Potion of Flying, Potion of Gaseous Form, Potion of Giant Strength,
Potion of Growth, Potion of Healing, Potion of Heroism, Potion of Invisibility,
Potion of Invulnerability, Potion of Levitation, Potion of Longevity,
Potion of Poison, Potion of Polymorph Self, Potion of Speed,
Potion of Treasure Finding
```

### Rings

```
Ring of Controlling Animals, Ring of Controlling Humans, Ring of Controlling Plants,
Ring of Delusion, Ring of Djinni Summoning, Ring of Fire Resistance,
Ring of Invisibility, Ring of Protection, Ring of Protection 5' Radius,
Ring of Regeneration, Ring of Spell Storing, Ring of Spell Turning,
Ring of Telekinesis, Ring of Water Walking, Ring of Weakness,
Ring of Wishes, Ring of X-Ray Vision
```

### Scrolls

```
Cursed Scroll, Protection from Elementals Scroll, Protection from Lycanthropes Scroll,
Protection from Magic Scroll, Protection from Undead Scroll, Protection Scroll,
Spell Scroll, Treasure Map
```

### Wondrous Items & Misc Magic

```
Alchemist's Beaker, Amulet of Protection Against Possession, Amulet of Protection Against Scrying,
Apparatus of the Crab, Bag of Devouring, Bag of Holding, Bag of Transformation,
Book of Foul Corruption, Book of Infinite Spells, Book of Sublime Holiness,
Boots of Dancing, Boots of Levitation, Boots of Speed, Boots of Travelling and Leaping,
Bracers of Defencelessness, Broom of Flying, Candle of Invocation,
Chime of Opening, Chime of Ravening,
Cloak of Defence, Cloak of Flight, Cloak of Poison, Cloak of the Manta Ray,
Crystal Ball, Crystal Ball with Clairaudience, Crystal Ball with ESP, Crystal Hypnosis Ball,
Cube of Force, Cube of Frost Resistance,
Decanter of Endless Water, Deck of Many Things, Displacer Cloak,
Drums of Panic, Drums of Thunder,
Dust of Appearance, Dust of Disappearance, Dust of Sneezing and Choking,
Efreeti Bottle,
Elemental Summoning Device (Air/Earth/Fire/Water),
Elven Cloak and Boots,
Eyes of Charming, Eyes of Minuscule Sight, Eyes of Petrification, Eyes of the Eagle,
Feather Token, Figurine of Wondrous Power, Flying Carpet, Folding Boat,
Gauntlets of Ogre Power,
Gem of Brightness, Gem of Monster Attraction, Gem of Pristine Faceting, Gem of Seeing,
Girdle of Giant Strength, Gloves of Dexterity, Gloves of Swimming and Climbing,
Horn of Blasting, Horn of Cave-Ins, Horn of Frothing, Horn of Valhalla, Horn of the Tritons,
Horseshoes of Speed, Horseshoes of a Zephyr,
Incense of Meditation, Incense of Obsession, Instant Fortress, Ioun Stones, Iron Flask,
Jug of Endless Liquids,
Libram of Arcane Power, Loadstone, Luckstone, Lyre of Building,
Marvellous Pigments,
Medallion of ESP 30', Medallion of ESP 90', Medallion of Thought Projection,
Mirror of Life Trapping, Mirror of Mental Prowess, Mirror of Opposition,
Necklace of Adaptation, Necklace of Fireballs, Necklace of Strangulation,
Net of Aquatic Snaring, Net of Snaring,
Oil of Insubstantiality, Oil of Slipperiness,
Pearl of Power, Pearl of Wisdom,
Periapt of Foul Rotting, Periapt of Health, Periapt of Proof Against Poison,
Periapt of Wound Closure,
Phylactery of Betrayal, Phylactery of Faithfulness, Phylactery of Longevity,
Pipes of the Sewers, Portable Hole, Purse of Plentiful Coin,
Restorative Ointment,
Robe of Blending, Robe of Eyes, Robe of Powerlessness,
Robe of Scintillating Colours, Robe of Useful Items, Robe of the Archmagi,
Rod of Absorption, Rod of Captivation, Rod of Resurrection,
Rope of Climbing, Rope of Entanglement, Rope of Strangulation, Rug of Suffocation,
Saw of Felling,
Scarab of Chaos, Scarab of Death, Scarab of Protection, Scarab of Rage,
Spade of Mighty Digging, Sphere of Annihilation, Sweet Water,
Talisman of the Sphere, Vacuous Grimoire
```

---

## CLASS ABILITY CATALOG (auto-imported for characters via SV class)

When you write a character statblock with an SV class that maps to a feature class, the importer auto-imports ALL abilities listed for that class from the `ose-advancedfantasytome.abilities` compendium. Here are the available abilities per resolved feature class:

### Acrobat (10 abilities)

```
After Reaching 9th Level, Climb sheer surfaces (CS), Combat, Evasion,
Falling (FA), Hide in shadows (HS), Jumping, Move Silently (MS),
Tightrope Walking (TW), Tumbling Attack
```

### Assassin (10 abilities)

```
After Reaching 12th Level, Assassination (AS), Climb sheer surfaces (CS),
Combat, Disguise, Hear noise (HN), Hide in shadows (HS), Hirelings,
Move Silently (MS), Poison
```

### Barbarian (12 abilities)

```
After Reaching 8th Level, Agile Fighting, Climb Sheer Surfaces (CS), Combat,
Cure Poison, Fear of Magic, Foraging, Foraging and Hunting,
Hide In Undergrowth (HD), Hunting, Move Silently (MS), Strike Invulnerable Monsters
```

### Bard (7 abilities)

```
After Reaching 11th Level, Anti-Charm, Combat, Divine Magic, Enchantment,
Languages, Lore
```

### Cleric (4 abilities)

```
After Reaching 9th Level, Combat, Divine Magic, Turn Undead
```

### Drow (8 abilities)

```
After Reaching 9th Level, Combat, Detect Secret Doors, Divine Magic,
Immunity to Ghoul Paralysis, Light Sensitivity, Listening at Doors, Spider Affinity
```

### Druid (10 abilities)

```
Charm Immunity, Combat, Divine Magic, Energy Resistance, Identification,
Pass Without Trace, Path-Finding, Reaching 12th Level and Above,
Shape Change, Sylvan Languages
```

### Duergar (9 abilities)

```
After Reaching 9th Level, Combat, Detect Construction Tricks, Detect Room Traps,
Infravision, Light Sensitivity, Listening at Doors, Mental Powers, Stealth
```

### Dwarf (6 abilities)

```
After Reaching 9th Level, Combat, Detect Construction Tricks, Detect Room Traps,
Infravision, Listening at Doors
```

### Elf (7 abilities)

```
After Reaching 9th Level, Arcane Magic, Combat, Detect Secret Doors,
Immunity to Ghoul Paralysis, Infravision, Listening at Doors
```

### Fighter (9 abilities)

```
After Reaching 9th Level, Chivalric Code, Combat, Flying Mounts, Horsemanship,
Hospitality, Mounted Combat, Strength Of Will, Stronghold
```

### Gnome (11 abilities)

```
After Reaching 8th Level, Arcane Magic, Combat, Defensive Bonus,
Detect Construction Tricks, Hiding, Hiding In Dungeons,
Hiding in Woods/Undergrowth, Infravision, Listening at Doors,
Speak with Burrowing Mammals
```

### Half-Elf (5 abilities)

```
After Reaching 9th Level, Arcane Magic, Combat, Detect Secret Doors, Infravision
```

### Half-Orc (8 abilities)

```
After Reaching 8th Level, Back-stab, Combat, Hide in shadows (HS), Infravision,
Move Silently (MS), Pick pockets (PP), Retainers
```

### Halfling (9 abilities)

```
Combat, Defensive Bonus, Hiding, Hiding In Dungeons, Hiding in Woods/Undergrowth,
Initiative Bonus (Optional Rule), Listening at Doors, Missile Attack Bonus, Stronghold
```

### Illusionist (3 abilities)

```
After Reaching 11th Level, Arcane Magic, Combat
```

### Knight (resolves to fighter for SV, separate feature class)

*Knight uses Fighter abilities listed above.*

### Magic-User (3 abilities)

```
After Reaching 11th Level, Arcane Magic, Combat
```

### Paladin (8 abilities)

```
After Reaching 9th Level, Combat, Divine Magic, Holy Resistance,
Laying On Hands, Turning Undead, Vow Of Humility, Warhorse
```

### Ranger (11 abilities)

```
After Reaching 10th Level, Awareness, Combat, Divine Magic, Foraging,
Foraging and Hunting, Hunting, Limited Possessions, Pursuit, Stealth, Tracking
```

### Svirfneblin (13 abilities)

```
After Reaching 8th Level, Blend into Stone, Blend into Stone (Gloomy),
Blend into Stone (Well-Lit), Combat, Defensive Bonus, Detect Construction Tricks,
Illusion Resistance, Infravision, Light Sensitivity, Speak with Earth Elementals,
Stone Murmurs, Using Magic Items
```

### Thief (12 abilities)

```
After Reaching 9th Level, Back-stab, Climb sheer surfaces (CS), Combat,
Find/remove treasure traps (TR), Hear noise (HN), Hide In Shadows (HS),
Move silently (MS), Open Locks (OL), Pick Pockets (PP), Read Languages, Scroll Use
```

---

## RACE ABILITY CATALOG (auto-imported for characters via race)

The importer can also match race-specific abilities using the race ability map. These are the race abilities available per race:

### Drow (7 abilities)

```
Available Classes and Max Level, Detect Secret Doors, Immunity to Ghoul Paralysis,
Infravision, Innate Magic, Light Sensitivity, Listening at Doors
```

### Duergar (9 abilities)

```
Available Classes and Max Level, Combat, Detect Construction Tricks, Detect Room Traps,
Infravision, Light Sensitivity, Listening at Doors, Resilience, Stealth
```

### Dwarf (7 abilities)

```
Available Classes and Max Level, Combat, Detect Construction Tricks, Detect Room Traps,
Infravision, Listening at Doors, Resilience
```

### Elf (5 abilities)

```
Available Classes and Max Level, Detect Secret Doors, Immunity to Ghoul Paralysis,
Infravision, Listening at Doors
```

### Gnome (8 abilities)

```
Available Classes and Max Level, Combat, Defensive Bonus, Detect Construction Tricks,
Infravision, Listening at Doors, Magic Resistance, Speak with Burrowing Mammals
```

### Half-Elf (3 abilities)

```
Available Classes and Max Level, Detect Secret Doors, Infravision
```

### Half-Orc (2 abilities)

```
Available Classes and Max Level, Infravision
```

### Halfling (7 abilities)

```
Available Classes and Max Level, Combat, Defensive Bonus,
Initiative Bonus (Optional Rule), Listening at Doors, Missile Attack Bonus, Resilience
```

### Human (2 abilities)

```
Available Classes and Max Level, Racial Abilities (Optional Rule)
```

### Svirfneblin (12 abilities)

```
Available Classes at Max Level, Blend into Stone, Blend into Stone (Gloomy),
Blend into Stone (Well-Lit), Combat, Defensive Bonus, Detect Construction Tricks,
Illusion Resistance, Infravision, Light Sensitivity, Listening at Doors,
Speak with Earth Elementals
```

---

## COMPENDIUM OVERVIEW

The importer searches these compendium packs for item matching:

| Compendium | Type | Item Count |
|-----------|------|------------|
| `ose-advancedfantasytome.abilities` | Class Abilities | 93 |
| `ose-advancedfantasytome.race-abilities` | Race Abilities | ~50 |
| `ose-advancedfantasytome.ose-equipment` | Equipment | 71 |
| `ose-advancedfantasytome.ose-magic-items` | Magic Items | 311 |
| `ose-advancedfantasytome.ose-monsters` | Monsters | 428 |
| `ose-advancedfantasytome.ose-animals` | Animals | 8 |
| `ose-advancedfantasytome.ose-macros` | Macros | 5 |
| `ose-advancedfantasytome.ose-players-tome` | Journal Entries | 14 |

---

## STATBLOCK WRITING RULES WITH CATALOG KNOWLEDGE

When writing equipment in statblocks:

1. **Use exact canonical names** from the catalogs above for perfect matching
2. **Weapons**: use names from the WEAPON CATALOG. Prefer `Sword` over `longsword` (the OSE catalog uses `Sword`). Use `Battle Axe` not `battleaxe`. Use `Hand axe` not `handaxe`.
3. **Armor**: use `Leather Armour`, `Chainmail`, `Plate Mail` (British spelling "Armour" is canonical). Use `Shield` for basic shield, `Shield (Steel)` or `Shield (Wood)` for specific.
4. **Magical items**: append `+N` for simple bonus, or use full magical name. Example: `Sword +1`, `Leather Armour +1`, `Shield +1`.
5. **Gear**: use exact names like `Rope (50')`, `Torches (6)`, `Rations (standard, 7 days)`, `Tinder Box (flint & steel)`.
6. **Poisons**: use the numbered format: `Bloodstream Poison: III`, `Ingested Poison: I`.
7. **Multiples**: prefix **`Nx`** before the catalog name — `10x Potion of Healing`, `2x Rations (standard, 7 days)`, `3x Holy Water (vial)`. Foundry shows stacks as value/max (10/10). Never repeat the same item name N times in a comma list.
8. **Worn**: append **`{worn}`** on ready weapons and worn armor/shields — `Sword +1 {worn}`, `Plate Mail {worn}`, `Shield (Steel) {worn}`. Use **`{stowed}`** for pack/backup weapons. Without this, armor may not count as worn and weapons may not show ready.

### Equipment Examples Using Exact Names

```
; weapon Sword +1 {worn}, Dagger {stowed}; armor Chainmail {worn}, Shield (Steel) {worn}
; weapon Mace {worn}; armor Leather Armour {worn}, Shield (Wood) {worn}
; weapon Battle Axe {worn}; armor Plate Mail {worn}
; equipment Rope (50'), 6x Torches (6), 2x Rations (standard, 7 days), Tinder Box (flint & steel)
; equipment Thieves' Tools, Grappling Hook, Crowbar, Iron Spikes (12)
; equipment 10x Potion of Healing, 2x Potion of Fire Resistance, 3x Holy Water (vial)
; Equipment: 10x Potion of Healing, 2x Rations (standard, 7 days), Rope (50'), Backpack
; Weapon: Sword +2 {worn}; Armor: Plate Mail +1 {worn}, Shield {worn}; Equipment: Holy Symbol, 10x Potion of Healing
```

### Class Feature Import Behavior

When you write `SV F3`, the importer:

- Sets save progression from the Fighter table for level 3
- Auto-imports ALL 9 fighter abilities from the compendium
- Sets `system.details.class` to "Fighter"

When you write `SV BARB2`, the importer:

- Sets save progression from the Barbarian table for level 2
- Auto-imports ALL 12 barbarian abilities from the compendium
- Sets class display to "Barbarian"

When you write `SV PAL5`, the importer:

- Sets save progression from the Paladin table for level 5
- Auto-imports ALL 8 paladin abilities from the compendium
- Sets class display to "Paladin"

**Duplicate prevention**: If an ability already exists on the actor (tracked by compendium source UUID), it is never re-imported. You can safely re-import the same statblock without duplication.
