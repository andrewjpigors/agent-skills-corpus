---
name: interpreting-storyboard-specs
description: Use when given a VRse storyboard document — converts chapter/moment narrative format into a YAML module spec and implements it via scene setup + Story JSON generation. Triggers on "Convert and implement", "Convert only", or any prompt with a <storyboard_file> tag.
user-invocable: true
effort: high
allowed-tools: Read, Grep, Glob, Write, Bash(cat *)
---

# Interpreting VRse Storyboard Specs

## Storyboard Format Reference

Full format specification with all keywords and examples:
`{{SKILLS_HOME}}/interpreting-storyboard-specs/storyboard-format.md`

Reference storyboard — Standard format (LOTO training, 4 chapters):
`Assets/Storyboards/LOTO_MechanicalTraining.md`

Reference storyboard — LXD format (LOTO training, same module):
`{{USER_HOME}}/Downloads/LOTO_MechanicalTraining_LXD.md`

---

## Execution Sequence

### Mode A: "Implement" (default — full pipeline)
1. Read the storyboard file
2. **Detect format + Normalize** — detect Standard vs LXD, fix heading levels, strip annotations (Step 0)
3. Parse metadata frontmatter — extract `art_scene`, `dev_scene`, `story_json`, `story_json_mode`
4. Parse objects + spawn points:
   - Standard: `## Objects` + `## Spawn Points` per chapter
   - LXD: global `## Object Registry` table + global `## Spawn Points` table
5. Extract lifecycle sections → translate using correct syntax map → generate YAML spec
6. **Validate YAML** — schema check with self-correcting retry loop (Step 7)
7. **Pre-flight scene paths** — verify files exist; fuzzy-match if not found (Step 8)
8. Save spec to `Assets/Storyboards/<ModuleName>_spec.yaml`
9. Hand off to `vrse-module-pipeline` — scene paths already embedded in YAML spec

### Mode B: "Convert only" (no Unity changes)
1. Read storyboard file
2. Normalize → parse → generate YAML spec
3. Save to `Assets/Storyboards/<ModuleName>_spec.yaml`
4. Output spec to user — stop here

---

## Prompt Format (what user types)

**Standard (implement):**
```
<storyboard_file>
Assets/Storyboards/ModuleName.md
</storyboard_file>
```

**Convert only (no Unity changes):**
```
Convert only:
<storyboard_file>
Assets/Storyboards/ModuleName.md
</storyboard_file>
```

Scene paths, Story JSON path, and mode all come from the storyboard's frontmatter — no `<scene>` block needed.

---

## Step 0: Detect Format + Normalize

### Format Detection
Two storyboard formats are accepted. Detect which one before parsing:

**Standard format** — human-readable keywords, per-chapter `## Objects` sections:
```
- Trigger: User grabs ObjectName
- Spawn: ContainerName
- Haptics: 0.5, 0.5
```

**LXD format** — technical class names, global `## Object Registry` table, `*(chapterIndex: N)*` annotations:
```
- Trigger: GrabbableTrigger [ObjectName] → Grab, handOption: Any
- Objects,Spawn: [ContainerName]
- Haptics: Both | intensity: 0.5 | duration: 0.5
```

Detect by: if the file contains `## Object Registry` table OR `Trigger: GrabbableTrigger [` → **LXD format**. Otherwise → **Standard format**.

**Hybrid detection:** If BOTH signals are present (Standard per-chapter `## Objects` sections AND LXD class-name triggers like `Trigger: GrabbableTrigger [`), treat as hybrid: parse objects using Standard rules (per-chapter `## Objects`), parse triggers/actions using the LXD Syntax Map. Log a warning: "Hybrid format detected — using Standard object parsing + LXD trigger syntax." If the resulting YAML fails schema validation (Step 7), HALT and ask the user to normalize to one format.

Both formats (and hybrid) are fully supported. Parse accordingly using the correct mapping table (Steps 1–2 below, and the LXD Syntax Map section).

### Normalize (both formats)
| Issue | Fix |
|---|---|
| Heading uses `##` for chapter instead of `#` | Correct to `#` |
| Moment uses `##` instead of `###` in standard format | Correct to `###` |
| LXD format: moment uses `## Moment N` (H2) | Keep as-is — LXD uses H2 for moments |
| `**Onawake**` / `**on_right**` / mixed case lifecycle keywords | Normalize to `**OnAwake**`, `**OnRight**`, etc. |
| `**OnRight** *(InOrder)*` italic annotation | Strip italic markers → `**OnRight** (InOrder)` |
| `*(chapterIndex: N)*` / `*(momentIndex: N \| ...)*` annotations | Parse and discard the annotation text — use N as the index |
| Missing `---` frontmatter delimiters | Flag and halt — cannot proceed without metadata |
| `art_scene` / `dev_scene` / `story_json` / `story_json_mode` missing from frontmatter | Halt with exact list of missing fields |
| `> **Module:** ...` blockquote header instead of `---` frontmatter | Halt — tell user to replace with `---` frontmatter block |
| Trailing whitespace on action lines | Trim |
| Windows line endings (`\r\n`) | Normalize to `\n` |

If any **halt** condition is hit, stop and tell the user exactly what to fix — do not guess.

---

## Step 0.5: Initialize `<ModuleName>_review.md`

After format detection and normalization succeed (Step 0 complete) and BEFORE Step 1 metadata extraction begins, create the build review file. This file accumulates Class 2 (🟡) and Class 3 (🔵) entries from every downstream pipeline stage; the build is not "complete" until this file is finalized at the end of `vrse-module-pipeline` Step 9.

**Where:** same directory as the source storyboard, named `<ModuleName>_review.md` (extracted from frontmatter `module:` field — strip whitespace, no extension change). Example: storyboard `BGS Training.md` → review `BGS Training_review.md`.

**Initial content:**

```markdown
# Build Review — <ModuleName>

**Source storyboard:** `<full path to storyboard>`
**Build started:** <ISO 8601 timestamp>
**Build finished:** _(pending — finalized in vrse-module-pipeline Step 9)_
**Status:** _(pending)_

## Summary
- 🔴 0 hard failures (build halted) — _(pending)_
- 🟡 0 review items
- 🔵 0 informational notes

---

## 🟡 Review items

_(none yet — appended by downstream stages as Class 2 events occur)_

---

## 🔵 Informational notes

_(none yet — appended by downstream stages as Class 3 events occur)_
```

**Append API for downstream stages:** every Class 2 / Class 3 event during the build appends a structured entry under the appropriate section, incrementing the summary counts. The full schema is defined in `vrse-module-pipeline/SKILL.md` → "Review File Contract".

**If the file already exists** (re-running pipeline on the same storyboard): rename the existing file to `<ModuleName>_review_<timestamp>.md` (preserves prior run's review for diff) and create a fresh one. Do NOT append to a stale file from a previous run.

**Do not skip this step.** Per Plan H, the review file is the framework's primary mechanism for surfacing soft failures without halting the build. Even an empty review (zero 🟡, zero 🔵) is meaningful — it means the build was unambiguous end-to-end.

---

## LXD Syntax Map

When the file is in **LXD format**, read the full translation tables from:
`{{SKILLS_HOME}}/interpreting-storyboard-specs/lxd-syntax-map.md`

This covers: Object Registry → YAML objects, Spawn Points → YAML, Action Syntax → YAML actions (25+ patterns), Trigger Syntax → YAML triggers (10+ patterns), MCQResponse field mapping, and special lines.

---

## Step 1: Metadata & Object Extraction

### 1a: Parse metadata header
Read YAML frontmatter (`---` delimited):
```yaml
---
module: "Module Name"
project: "ProjectName"
formatVersion: 2.0      # optional; defaults to 2.0 if absent. Emitted into Story JSON top-level.
defaults:
  firstWarningTimer: 30
  lastWarningTimer: 20
---
```
- `module` → YAML spec `module.name`
- `formatVersion` → YAML spec `module.formatVersion` (defaults to `2.0` if absent). Propagates into emitted Story JSON `formatVersion` top-level field. **Must be `2.0` to avoid v1 migration that restructures `onRight`.**
- `project` → YAML spec `module.project`
- `defaults` → moment-level `defaults` in Story JSON: `{"chapterFirstWarningTimer": N, "chapterLastWarningTimer": N}`

### 1b: Parse Objects section
Each chapter has `## Objects`:
```
- ObjectName (type) [source: ArtPropName] [position: x, y, z] [allows: GrabbableName]
```

| Type keyword | YAML type | Notes |
|---|---|---|
| `grabbable` | `grabbable` | GrabbableTrigger interactions |
| `placepoint` | `placepoint` | Parse `[allows: X]` → `allowed_grabbables` |
| `touchable` | `touchable` | HandTouchTrigger interactions |
| `simple` | `simple` | Spawn/Despawn only, no interaction |
| `pivot` | `pivot` | PivotRotateLimiterTrigger interactions |
| `forceps` | `forceps` | ForcepsTrigger interactions |

Parse modifiers:
- `[source: X]` → `source_object: X` (triggers Recipe 2b — duplicate from art scene)
- `[source_parent: P]` → `source_parent: P` (used by preflight to disambiguate when `source` matches multiple art objects under different parents)
- `[position: x, y, z]` → `position: [x, y, z]`
- `[at: description]` → `spatial_hint: "description"` (e.g., `[at: on Table rack]`, `[at: near GateValve]`) — used by Step 4.5 spatial placement to auto-compute position
- `[allows: X]` → `properties.allowed_grabbables: [X]`

**Naming axis (mandatory):** the YAML spec MUST set `vrse_name: <logical_name>` for every object — i.e., the dev-scene name always matches the logical name written before the type in the `## Objects` line. This eliminates the historical class of silent runtime "object not found" failures caused by logical/vrse_name divergence.

**Legacy `[vrse_name:]` modifier — HALT:** if a storyboard contains a `[vrse_name: Y]` modifier on any object, the parser MUST HALT immediately with this message:

```
'[vrse_name:]' modifier is no longer supported. The pipeline auto-sets
vrse_name = logical name (the name written before the type in the
'## Objects' line). Remove '[vrse_name: Y]' from object '<ObjectName>'.
If your art prefab has a different name, declare it via [source: ArtName]
— conversion will rename the duplicate to the logical name automatically.
```

Do not silently ignore the modifier and do not attempt a "best-effort" emit. Halt and surface the message so the author resolves the storyboard.

**Position inference:** If an object has no `[position:]` modifier, omit `position` from the YAML. The pipeline's Step 4.5 will auto-compute it from the scene geometry using spatial analysis tools. If `[at:]` is present, include `spatial_hint` to guide placement. If neither is present, the pipeline infers placement from storyboard context (e.g., "user picks up wrench from workbench" → place wrench on workbench surface).

### 1c: Cross-Chapter Object Deduplication
After parsing all chapters' `## Objects` sections, build a cross-chapter usage map:

```
USAGE MAP:
  Wheel       → [Ch0, Ch1]     ← shared (appears in 2+ chapters)
  PadLock     → [Ch0, Ch1, Ch2] ← shared
  LockoutCover→ [Ch0]          ← chapter-exclusive
```

**Rules:**
- If an object name appears in 2+ chapters → tag it as `shared: true` in the YAML spec
- Shared objects go directly under **QueryObjects root** (not under any chapter container)
- Shared objects get **individual** `Objects.Spawn` / `Objects.Despawn` in Story JSON (not group spawn/despawn via chapter container)
- Only duplicate/create the shared object **ONCE** — do NOT create copies per chapter
- In the YAML output, shared objects appear in the top-level `objects:` list with `shared: true`
- Chapter-specific `objects:` references should just reference the shared object by name (no re-declaration)

**Spawn/Despawn lifecycle for shared objects:**
1. Find the FIRST moment (across all chapters, ordered by chapterIndex then momentIndex) that references the object
2. Spawn it in that moment's `on_awake`
3. Find the LAST moment that references it
4. Despawn it in that moment's `on_end`
5. Object stays alive between first and last use — NO intermediate despawn/respawn between chapters

### 1d: Parse Spawn Points section
```
- SP_Name: Description
```
→ Add to YAML `spawn_points` list. Referenced by `Teleport: SP_Name`.

### 1e: Auto-discovery fallback
If no `## Objects` section, infer type from interactions (legacy format):

| Storyboard description | Inferred type |
|---|---|
| `Trigger: User grabs X` | `grabbable` |
| `Trigger: User touches X` | `touchable` |
| `Trigger: User places X into Y` → Y | `placepoint` |
| `Trigger: User clicks X` | `uiButton` |
| `Trigger: User rotates X` | `pivot` |
| Only Spawn/Despawn, no trigger | `simple` |

Also check scene for `VRseInteractableMarker` components via `get_hierarchy`.

---

## Step 2: Storyboard → YAML Action/Trigger Mapping

### Actions

| Storyboard keyword | YAML `action` | Option | Key data fields |
|---|---|---|---|
| `VoiceOver: "text"` | `VoiceOver` | `Play` | `text`, `waitForCompletion: true` |
| `Spawn: ContainerName` | `Objects` | `Spawn` | `waitForCompletion: true` if 2nd+ |
| `Despawn: ContainerName` | `Objects` | `Despawn` | `waitForCompletion: true` if followed by Spawn |
| `Teleport: SpawnPointName` | `Player` | `Teleport` | `targetTransform: "Name#$ID"` |
| `Timer: Ns` | `TimerAction` | `Start` | `duration: N`, `waitForCompletion: true` |
| `Highlight: ObjectName` | `MetaLayerAction` | `SetActive` | Full Data format (see MetaLayerAction note in Role/Hand section below), `Outline: true` |
| `Highlight: ObjectName [label: "text"] [color: #hex] [width: N]` | `MetaLayerAction` | `Edit` then `SetActive` | `Outline: {outlineColor, outlineWidth, setActive: true}, Label: {labelText, setActive}` |
| `Unhighlight: ObjectName` | `MetaLayerAction` | `SetActive` | Full Data format, `Outline: false` |
| `SFX: clip_name` | `SFXPlayer` | `Play` | `audioClipName: "name"` |
| `SFX: clip_name [volume: N] [range: N]` | `SFXPlayer` | `Play` | `audioClipName, setVolume, audioRange` |
| `Animation: clip_name on ObjectName` | `Animation` | `Play` | Query: `ObjectName`, `_clipName: "name"`, `waitForCompletion` |
| `Animation: clip_name` | `Animation` | `Play` | Query: `""`, `ID: -1`, `_clipName: "name"`, `waitForCompletion` (untargeted — runs on default Animator) |
| `Haptics: intensity, duration` | `HapticsAction` | `Both` | Query: `Haptics`, `hapticIntensity: I`, `hapticDuration: D` |
| `GrabUnlock: ObjectName` | `GrabLockAction` | `GrabUnlock` | `waitForCompletion: true` |
| `GrabUnlock: ObjectName [forceRelease]` | `GrabLockAction` | `GrabUnlock` | `forceRelease: true` |
| `UnlockRotation: ObjectName` | `PivotRotateLimiterAction` | `Unlock` | `waitForCompletion: true` |
| `MoveObject: ObjectName to TargetName [speed: N]` | `ObjectAnimationAction` | `PositionRotation` | `lerpDuration: N`, `targetTransform: "Target#$ID"` |
| `EnableGrab: ObjectName` | `Objects` | `SetComponentProperty` | `component: "Grabbable"`, `property: "isGrabbable"`, `propertyValue: "true"` |
| `DisableGrab: ObjectName` | `Objects` | `SetComponentProperty` | `component: "Grabbable"`, `property: "isGrabbable"`, `propertyValue: "false"` |
| `SetProperty: Object.Component.field = value` | `Objects` | `SetComponentProperty` | Query: `Object`, `component: "Component"`, `property: "field"`, `propertyValue: "value"` |
| `ForceRelease: ObjectName` | `Objects` | `SetComponentProperty` | Query: `ObjectName`, `component: "Grabbable"`, `property: "isGrabbable"`, `propertyValue: "true"`, `forceRelease: true` |
| `EnableGrabFor: ObjectName [op?]` | `GrabbablePropertyChangeAction` | `ChangeIsGrabbable` | `isGrabbable: true`, `targetRoleSetId` from modifier |
| `DisableGrabFor: ObjectName [op?]` | `GrabbablePropertyChangeAction` | `ChangeIsGrabbable` | `isGrabbable: false`, `targetRoleSetId` from modifier |
| `Highlight: [X1, X2, X3] [modifiers]` | `MetaLayerAction` × N | `SetActive` or `Edit` | Emit one MetaLayerAction per target, all with the same modifier-derived Data payload |
| `GuidanceArrow: ObjectName` | `TargetGuidanceArrowAction` | `Override` | Query: `TriggerQueryObjectGuider`, `targetGameObject: "Name#$ID"` |
| `GuidanceArrow: disable` | `TargetGuidanceArrowAction` | `Disable` | Query: `TriggerQueryObjectGuider` |
| `GrabLock: ObjectName` | `GrabLockAction` | `GrabLock` | — |
| `HMISwap: ScreenA → ScreenB` | `Objects(Despawn ScreenA)` + `Objects(Spawn ScreenB)` | `Despawn` / `Spawn` | Both `waitForCompletion: false` |
| `Highlight: ObjectName [op?]` | `MetaLayerAction` | `SetActive` | Full Data format (see MetaLayerAction note below), `targetRoleSetId` from modifier |
| `Unhighlight: ObjectName` | `MetaLayerAction` | `SetActive` | Full Data format with `Outline: false` (see MetaLayerAction note below) |
| `ChecklistUIToggle: ["items"]` | `ChecklistUIToggle` | `Configure` | `toggleInfos: [...]`, index 1-based |
| `ChecklistUIToggle.Check: N` | `ChecklistUIToggle` | `Check` | `index: N` (1-based) |
| `LockMovement` | `Player` | `LockMovement` | — |
| `UnlockMovement` | `Player` | `UnlockMovement` | — |
| `CameraFade: in/out/inout` | `Player` | `CameraFade` | `fadeType`, `fadeDuration`, `waitForCompletion` |
| `UIText: "text" on PanelName` | `UIPropertyChangeAction` | `ChangeText` | `text: "..."` |
| `ToastMessage: "text"` | `ToastMessage` | `Show` | `message: "..."` |
| `VFX: effect_name` | `ScriptableAction` | *(custom)* | ⚠️ `# CUSTOM REQUIRED` |
| `MCQ: {...}` | `MCQResponseAction` | `""` | See MCQ parsing below |

### MCQ Parsing

```markdown
- MCQ:
  question: "Question text?"
  options: ["A", "B", "C", "D"]
  correct: [1]
  showDuration: 5
  answerDescription: "text"
```

→ YAML:
```yaml
- action: MCQResponseAction
  query: "MCQ EVALUATION PANEL"
  option: ""
  data:
    questionIndex: (auto-increment)
    questionText: "Question text?"
    optionsList: ["A", "B", "C", "D"]
    correctOptionIndex: [1]
    showAnswerDuration: 5
    answerDescriptionText: "text"
```

### Triggers

| Storyboard trigger | YAML `trigger` | Option | Key data |
|---|---|---|---|
| `Trigger: User grabs X` | `GrabbableTrigger` | `Grab` | `handOption: "Any"` |
| `Trigger: User releases X` | `GrabbableTrigger` | `Release` | `handOption: "Any"` |
| `Trigger: User touches X` | `HandTouchTrigger` | `Touch` | — |
| `Trigger: User places X into Y` | `PlacePointTrigger` | `CorrectPlace` | `grabbableName: "X#$ID"` |
| `Trigger: User places X into Y [disableGrabOnPlace]` | `PlacePointTrigger` | `CorrectPlace` | `disableGrabOnPlace: true` |
| `Trigger: User places X into Y [disableGrabOnPlace] [disablePlacePointOnPlace]` | `PlacePointTrigger` | `CorrectPlace` | Both flags |
| `Trigger: User places X into Y [disableRigidbodyOnPlace]` | `PlacePointTrigger` | `CorrectPlace` | `disableRigidbodyOnPlace: true` |
| `Trigger: Any object placed into Y` | `PlacePointTrigger` | `Place` | — |
| `Trigger: User clicks X` | `UIButtonTrigger` | `OnClick` | — |
| `Trigger: User enters X` | `CollisionTrigger` | `Enter` | `isTrigger: true` |
| `Trigger: User rotates X to min` | `PivotRotateLimiterTrigger` | `Min` | — |
| `Trigger: User rotates X to min [lockOnReach]` | `PivotRotateLimiterTrigger` | `Min` | `lockOnReach: true` |
| `Trigger: User rotates X to max` | `PivotRotateLimiterTrigger` | `Max` | — |
| `Trigger: User rotates X to max [lockOnReach]` | `PivotRotateLimiterTrigger` | `Max` | `lockOnReach: true` |
| `Trigger: X reaches bounds [boundType: Y]` | `TransformBoundsTrigger` | `Single` | `boundType: Y`, `lockOnReach`, `snapToExactBounds` |
| `Trigger: User answers MCQ` | `MCQResponseTrigger` | `AnyResponse` | — |
| `Trigger: Any of [X, Y, Z] touched` | `AnyTrigger` | `Touch` | `triggerFrom: "Any"` |
| `Trigger: Custom — description` | `ScriptableTrigger` | *(custom)* | ⚠️ `# CUSTOM REQUIRED` |

### Role Modifier Expansion

Applied to any action that accepts `[op1]`, `[op2]`, or `[all]` modifiers (e.g., `EnableGrabFor`, `DisableGrabFor`, `Highlight`):

| Storyboard Modifier | JSON Data Field | Value |
|---|---|---|
| `[op1]` | `targetRoleSetId` | `1` |
| `[op2]` | `targetRoleSetId` | `2` |
| `[all]` | `targetRoleSetId` | `0` |
| *(no modifier)* | `targetRoleSetId` | `0` |

### Hand Modifier Expansion (on Grab triggers)

Applied to `Trigger: User grabs X` when a hand modifier is present:

| Storyboard Modifier | JSON Fields | Notes |
|---|---|---|
| `[right hand]` | `handOption: "Right"`, `Type: 1` | Hand-specific grab |
| `[left hand]` | `handOption: "Left"`, `Type: 1` | Hand-specific grab |
| *(no modifier)* | `handOption: "Any"`, `Type: 0` | Any hand |

### MetaLayerAction Data Format

> **ALWAYS use the full MetaLayerAction Data format** for any `Highlight:` or `Unhighlight:` keyword. Never use the simplified `{"Outline": true}` form.

```json
{"Outline": true, "Label": false, "Highlighter": false, "GhostHand": {"ghostHandsState": ""}, "targetRoleSetId": 0}
```

- For `Highlight:` → `"Outline": true`
- For `Unhighlight:` → `"Outline": false`
- `targetRoleSetId` comes from the role modifier (0 if no modifier)
- All other fields (`Label`, `Highlighter`, `GhostHand`) must be present even if false/empty

---

## Step 3: Warning Timing → YAML

**From metadata header:**
- `defaults.firstWarningTimer: 30` → `chapterFirstWarningTimer: 30`
- `defaults.lastWarningTimer: 20` → `chapterLastWarningTimer: 20`

**From storyboard lifecycle sections:**
- `**FirstWarning**` → `onFirstWarning` actions in Story JSON
- `**LastWarning**` → `onLastWarning` actions in Story JSON
- Both typically contain `Haptics` + `VoiceOver` pairs

---

## Step 4: Chapter / Moment Structure Rules

- `# Chapter N - Name` → YAML `chapters[]` entry, `chapterIndex: N` (or from last existing if appending)
- `### Moment N - Name` → `moments[]` entry, `momentIndex: N`
- Chapter container name format: `"CHAPTER {N+1} - {CHAPTER_NAME_UPPER}"`
  - Example: chapter 0 → `"CHAPTER 1 - INTRODUCTION AND SAFETY OVERVIEW"`
- If objects must survive across moments within same chapter: use ONE chapter container, do NOT Despawn between moments
- Spawn container in `OnAwake` of first moment, Despawn in `OnEnd` of last moment
- **Shared objects** (used across chapters): go under QueryObjects root, NOT inside any chapter container. Individual Spawn/Despawn, NOT group spawn/despawn.
- `**OnRight** (InOrder)` → `mode: "InOrder"` — sequential triggers
- `**OnRight** (Random)` → `mode: "Random"` — any trigger can fire

---

## Step 5: Gap Handling

| Situation | Action |
|---|---|
| Object position unknown | **Omit `position` from YAML** — Step 4.5 auto-computes from scene geometry. If storyboard context hints at location (e.g., "picks up from table"), add `spatial_hint: "on Table"`. Only use `position: [0.0, 1.0, 1.5]` as last resort if no spatial context exists |
| chapterIndex for append mode | Read existing JSON, count `chapters[]`, use `length` as next index |
| Custom trigger / action | Add `type: custom` + `# ⚠️ CUSTOM REQUIRED` |
| VFX | Map to `ScriptableAction` placeholder, flag as `# ⚠️ CUSTOM REQUIRED` |
| Duplicate object name in scene | Append `_N` suffix to deduplicate, add comment |
| Missing `## Objects` section | Fall back to inference from trigger descriptions |
| Missing `## Spawn Points` section | Extract spawn point names from `Teleport:` actions |

---

## Step 5.5: Placepoint Auto-Configuration for Grab-Locked Grabbables

Some grabbables get `GrabLock`-ed during a chapter — once locked, the user cannot release them. With the default `MetaXRPlacePointWrapper` settings (`forcePlace=false, heldPlaceOnly=true`), the placepoint requires a release gesture to snap. A grab-locked object therefore cannot be placed, and the snap silently fails. Every placepoint that accepts a grab-locked grabbable must be configured to force-snap while the object is held in trigger range.

**Rule (apply during YAML emit, before Step 6):**

1. **Collect locked names.** Walk every chapter's `**OnAwake**`, `**OnStart**`, `**OnRight**`, `**OnFirstWarning**`, `**OnLastWarning**`, `**OnEnd**`, and per-trigger response action lists. For every action that maps to `GrabLockAction` with `Option: GrabLock` (i.e., the storyboard line `GrabLock: <name>`), add `<name>` to a set `grabLockedNames`. One occurrence anywhere in the storyboard is enough — once locked in any moment, the placepoint must support it.
2. **For each placepoint object** in the parsed `objects` list:
   - Read `properties.allowed_grabbables` (parsed from `[allows: X]` per Step 1b).
   - If `allowed_grabbables` ∩ `grabLockedNames` is non-empty, emit:
     ```yaml
     properties:
       allowed_grabbables: ["<existing>"]
       force_place: true
       held_place_only: false
     ```
3. **No-match is silent.** If a grab-locked grabbable has no placepoint that allows it, emit nothing — the grabbable may be lock-only by design (e.g., a tool locked for collision use, never returned). Do NOT halt or warn.
4. **Manual override path (rare).** Storyboards do not have a syntax for overriding the auto-rule per placepoint — keeping the storyboard surface narrow. If a specific placepoint truly needs the default `forcePlace=false, heldPlaceOnly=true` behavior despite its grabbable being locked elsewhere, the author hand-edits the generated YAML to set `properties.force_place: false` (or omits the fields) before invoking the pipeline. Document this in module notes; do not invent storyboard modifiers.

**Linkage uses `[allows: X]`, NOT naming convention.** The `allowed_grabbables` field is the explicit author-declared link between placepoint and grabbable. Naming-convention matching (`PP_<grabbable>`) is unreliable across modules and is not used here.

**Why this lives at spec time, not at Story JSON time.** The pipeline creates placepoints in the scene at Steps 2-4, before Story JSON is generated at Step 6. Detecting grab-lock from the generated Story JSON would require a fragile second-pass fixup. Detecting at spec interpretation means the YAML — and downstream `batch_tasks.json` — already contains the correct fields, so the placepoint is created with the right settings on the first batch pass.

**Downstream contract.** `vrse-module-pipeline` translates `properties.force_place` / `properties.held_place_only` from the YAML object into the `force_place` / `held_place_only` string fields of the `create_placepoint` task in `batch_tasks.json` (see `VRseBatchSetup.cs` `BatchTask` definition). Values must be emitted as strings `"true"` / `"false"` per the JsonUtility-compatible schema.

---

## Step 6: YAML Output Format

```yaml
# Auto-generated from: Assets/Storyboards/ModuleName.md
# Generated: YYYY-MM-DD

module:
  name: "Module Name"
  project: "ProjectName"
  art_scene: "Assets/Scenes/Art/Module_Art.unity"
  dev_scene: "Assets/Scenes/Dev/Module_Dev.unity"
  story_json: "Assets/StreamingAssets/Story Files/Project/Module.json"
  story_json_mode: new    # new | append

defaults:
  firstWarningTimer: 30
  lastWarningTimer: 20

objects:
  # Chapter-exclusive object — position auto-computed by Step 4.5 spatial placement
  - name: "LockoutCover"
    type: grabbable
    vrse_name: "LockoutCover"         # ← AUTO-SET = name (mandatory; naming axis)
    source_object: "LockoutDevice"    # only if [source: X] present
    spatial_hint: "on Table"          # optional — guides auto-placement (from [at:] modifier)

  # Shared object (used in 2+ chapters) — goes under QueryObjects root, created ONCE
  - name: "Wheel"
    type: pivot
    vrse_name: "Wheel"                # ← AUTO-SET = name
    source_object: "GateValveWheel"
    shared: true                      # ← set when object appears in 2+ chapters
    spatial_hint: "attached to GateValve"  # inferred from storyboard context

  # Source under disambiguated parent — vrse_name still equals logical name
  - name: "GRB_SafetyDoor_C"
    type: pivot
    vrse_name: "GRB_SafetyDoor_C"     # ← AUTO-SET = name
    source_object: "GRB_SafetyDoor_D"
    source_parent: "Door C"            # disambiguates duplicate sources

  # Explicit position (only when author specifies [position: x, y, z])
  - name: "SafetySign"
    type: simple
    vrse_name: "SafetySign"           # ← AUTO-SET = name
    position: [2.0, 1.5, 0.0]        # explicit — skips spatial auto-placement

spawn_points:
  - name: "SP_Start"
    description: "Starting position"

story:
  chapters:
    - name: "Chapter Name"
      chapterIndex: 0
      moments:
        - name: "Moment Name"
          momentIndex: 0
          defaults:
            chapterFirstWarningTimer: 30
            chapterLastWarningTimer: 20
          on_awake:
            - action: Player
              option: Teleport
              data:
                targetTransform: "SP_Start"
            - action: Objects
              query: "CHAPTER 1 - NAME"
              option: Spawn
          on_start:
            - voiceover: "Instruction text."
            - action: MetaLayerAction
              query: "ObjectName"
              option: SetActive
              data:
                Outline: true
          on_right:
            mode: InOrder
            steps:
              - trigger: GrabbableTrigger
                query: "ObjectName"
                option: Grab
                then:
                  - action: GrabLockAction
                    query: "ObjectName"
                    option: GrabUnlock
                    data:
                      forceRelease: true
                  - action: HapticsAction
                    option: Both
                    data:
                      hapticIntensity: 0.5
                      hapticDuration: 0.5
                  - voiceover: "Good."
          on_first_warning:
            - action: HapticsAction
              option: Both
              data:
                hapticIntensity: 0.5
                hapticDuration: 0.5
            - voiceover: "Reminder text."
          on_last_warning:
            - action: HapticsAction
              option: Both
              data:
                hapticIntensity: 0.5
                hapticDuration: 0.5
            - voiceover: "Final warning."
          on_end:
            - action: TimerAction
              option: Start
              data:
                duration: 3
```

---

## Step 7: YAML Validation Loop

Run after generating the YAML spec. Check the spec against this schema before saving or handing to the pipeline. If errors are found, fix them inline and re-check — up to 3 passes. Do NOT hand off to the pipeline with a failing spec.

### Schema checks

**Module block:**
- `module.name` present and non-empty
- `module.art_scene`, `module.dev_scene`, `module.story_json`, `module.story_json_mode` all present (copied from frontmatter)

**Objects block:**
- Every object has `name` and `type`
- `type` is one of: `grabbable`, `touchable`, `placepoint`, `simple`, `pivot`, `forceps`
- `placepoint` objects have `properties.allowed_grabbables` list
- Shared objects have `shared: true`
- No duplicate `name` values

**Story block:**
- `chapterIndex` values are sequential starting from 0 (or from the correct append offset)
- Each chapter has at least one moment
- `momentIndex` values within each chapter are sequential starting from 0
- Every `query` value in triggers/actions that references a game object exists in the `objects` list by name (exception: `VoiceOver` query can be empty)
- Every `on_right` block has `mode` and `steps`
- No moment references an object that is neither in `objects` nor a chapter container name

### Auto-fix rules (apply silently, don't halt)

| Error | Fix |
|---|---|
| `chapterIndex` out of sequence | Renumber sequentially |
| `momentIndex` out of sequence within chapter | Renumber sequentially |
| Missing `shared: true` on object used in 2+ chapters | Add it |
| `on_right` missing `mode` | Default to `InOrder` |
| Position missing on object | Default to `[0.0, 1.0, 1.5]` + add `# ⚠️ review position` |

### Escalate to user (do not auto-fix)
- Object referenced in trigger/action that does not exist in `objects` list and cannot be inferred
- `story_json_mode: append` but existing JSON file cannot be found (can't determine next chapterIndex)
- 3 validation passes still produce errors — report exact list and stop

---

## Step 8: Pre-flight Scene Paths

Before handing off to the pipeline, verify the scene files exist. This catches stale paths before the build starts.

```
For each path in: module.art_scene, module.dev_scene, module.story_json (parent dir only):
  1. Check if file exists at exact path
  2. If not found → search Assets/ for files matching the filename (basename only)
  3. If exactly one match found → use it, log: "⚠️ Path corrected: <old> → <new>"
  4. If multiple matches → pick the lexicographically-first match by full path
     and emit a 🟡 review.md entry: "Scene path resolved by fuzzy match —
     `<old>` → `<picked>`. Alternatives: [<list>]. Confirm correct path in
     storyboard frontmatter or rename." Continue the build.
  5. If no matches → HALT: "Scene not found: <path>. Check the storyboard frontmatter."
```

**Plan H downgrade:** previously, multiple-match was a HALT. Per Plan H's tier table this is Class 2 (recoverable: lexicographic first-match is a sane placeholder; user fixes the storyboard or renames the scene file post-build). Zero-match remains HALT (Class 1 — file-system absence is irrecoverable).

Story JSON path: only verify the parent directory exists (file itself may not exist yet for `mode: new`).

---

## Critical Rules

1. **Never generate Story JSON before scene setup** — IDs aren't assigned until after save
2. **Never manually enumerate objects that are already tagged** with `VRseInteractableMarker` — read from scene
3. **Container name format is exact**: `"CHAPTER {N+1} - {NAME_UPPER}"` — case-sensitive, space before dash
4. **`source_object` bypasses primitive creation** — triggers Recipe 2b (duplicate from art scene)
5. **PlacePointTrigger `grabbableName`** always needs `#$ID` suffix — expand after reading IDs from `QueryObjectsIdManager`
6. **Append mode**: always read the existing Story JSON file first to get the correct next `chapterIndex`
7. **HapticsAction Option is `"Both"`** — not `"Vibrate"`. Data uses `hapticIntensity` and `hapticDuration`.
8. **MCQResponseAction Option is `""`** (empty string) — not any named option.
9. **Trigger keyword is `Trigger:`** — never parse bare `Action:` descriptions as triggers.
10. **Shared objects (used in 2+ chapters)** go under QueryObjects root with `shared: true`. Create/duplicate only ONCE. Individual Spawn/Despawn in Story JSON.
11. **Source objects from art scene** require the art scene to be loaded additively. If not found → HALT, never substitute a placeholder cube.
12. **Story JSON field names**: Use `"name"` for chapters and moments (NOT `"chapterName"`/`"momentName"`). `onWrong` is a bare array. `onRight.mode` at top level.

---

## Keyword → Moment Template Mapping

When generating YAML, map storyboard keywords to moment templates for production-grade output:

| Storyboard Keywords | YAML `template:` Value |
|---|---|
| "grab", "pick up", "take", "retrieve" | `guided-grab-step` |
| "place", "put", "insert", "return", "set down" | `guided-place-step` |
| "grab X and place in Y", "move X to Y" (same moment) | `guided-grab-and-place-step` |
| "open", "close", "rotate", "turn" (+ pivot/door/valve) | `guided-pivot-step` |
| "touch", "press", "push" (+ touchable/button) | `guided-touch-step` |
| "question", "quiz", "MCQ", "assessment" | `mcq-question` |
| First moment of chapter (introduction) | `chapter-intro` |
| Last moment of chapter (cleanup/transition) | `chapter-cleanup` |
| "go to", "move to area", "teleport" | `teleport-transition` |
| `[op1]`/`[op2]` modifiers + pivot trigger | `pivot-door-dual-role` (Template 11) |
| `[op1]`/`[op2]` + UIButtonTrigger + HMISwap | `hmi-button-press` (Template 10) |
| `[right hand]`/`[left hand]` modifier on grab | `hand-specific-grab` (Template 12) |

### Additional Keyword → Action Mappings

| Storyboard Keywords | YAML Action |
|---|---|
| "arrow", "guidance arrow", "point to" | `guidance_arrow: "ObjectName"` (implicit in templates) |
| "disable all grabbables", "lock everything" | `reset_all_grabbables: true` |
| "checklist", "task list", "progress" | `checklist: configure\|check\|current` |
| "operator 1", "operator 2", "role" | `role: 1\|2` on relevant actions/triggers |
| "ghost", "preview", "highlight position" | `ghost_highlight: "ObjectName"` |
| "tooltip", "hint label" | `tooltip: "ObjectName_ToolTip"` |

### Implicit Template Behaviors

When a `template:` is set on a moment, the following are **automatically included** and should NOT be manually specified:
- `reset_all_grabbables: true` in onAwake
- `guidance_arrow` in onStart
- MetaLayerAction outline in onStart
- Tooltip spawn/despawn lifecycle
- Warning VoiceOvers in onFirstWarning/onLastWarning

Only specify additional actions that go beyond the template's standard behavior.

## Supporting Files

- Storyboard format specification: `{{SKILLS_HOME}}/interpreting-storyboard-specs/storyboard-format.md`
- Moment templates (production patterns): `{{SKILLS_HOME}}/creating-vrse-story-json/moment-templates.md`
- Production patterns reference: `{{SKILLS_HOME}}/vrse-module-pipeline/patterns.md`
- Full MCP sequences: `{{SKILLS_HOME}}/setting-up-vrse-scenes/object-recipes.md`
- Action catalog (30 types): `{{SKILLS_HOME}}/creating-vrse-story-json/action-catalog.md`
- Trigger catalog (15 types): `{{SKILLS_HOME}}/creating-vrse-story-json/trigger-catalog.md`
- Story JSON schema + example: `{{SKILLS_HOME}}/creating-vrse-story-json/story-schema.md`
- YAML spec examples: `{{SKILLS_HOME}}/writing-vrse-module-specs/examples/`
