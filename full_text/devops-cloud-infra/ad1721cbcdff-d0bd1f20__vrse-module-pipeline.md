---
name: vrse-module-pipeline
description: "Use when implementing a full VRse module — triggered by <spec>, <storyboard_file>, 'Implement this VRse module', or 'build module' prompts. This is the primary execution skill for all module builds. Do NOT read other VRse skills during full builds — everything needed is here."
user-invocable: true
effort: high
---

# VRse Module Pipeline

## First Decision: New Build or Resume?

Check if the dev scene already has converted objects under `QueryObjects` (e.g., you're appending a chapter or fixing Story JSON in an existing session).

- **Resume** → skip to "Resuming an Existing Build" below
- **New build** → proceed to Rules, then Step 0

### Resuming an Existing Build (new session, scene already set up)
If the dev scene is already built and you just need to append a chapter or fix the Story JSON, skip Steps 0–4 and start here:
1. **Check `LastGOQIds.json` is for THIS module** — the file is shared across all modules. If `generatedAt` is empty or the IDs look wrong (e.g., LOTO objects), run `execute_menu_item("VRseTemp/Data/Clear LastGOQIds.json")` first.
2. Read `Assets/Editor/LastGOQIds.json` → restore ID_MAP instantly (no log parse needed)
3. If the file is empty or stale → run `VRseTemp/Log Module GOQ IDs` to regenerate it, then read
4. Proceed directly to Step 5 (ID verification) or Step 6 (Story JSON) as needed

This avoids full pre-flight + object rebuild for append-only or JSON-fix sessions.

### Append Mode Reference

When appending chapters to an existing module (not starting from scratch):
1. Read existing Story JSON file, count `chapters[]`, confirm spec's `chapterIndex` = `chapters.length`
2. Check for stale IDs — if the scene has been modified since `LastGOQIds.json` was written, re-run `VRseTemp/Log Module GOQ IDs`
3. In Step 6 (Story JSON generation), use `mode: append` — merge new chapters into the existing JSON, don't overwrite

---

## Rules

- **CRITICAL: Your very first action — before ANY tool call including Read or find_gameobjects — MUST be TodoWrite with ALL of the following tasks listed as pending:**
  - Step 0: Pre-flight check
  - Step 1: Parse spec / storyboard
  - Step 2: Scene setup (open dev + art scenes)
  - Step 3: Object conversion (pivots / grabbables / touchables)
  - Step 4: Placement & hierarchy
  - Step 5: ID harvest (save twice → Log GOQ IDs → read LastGOQIds.json)
  - Step 6: Story JSON generation (write _TrainingStory.json)
  - Step 7: Validation
  - Step 8: Save & wrap-up

  **Object conversion is NOT the end of the pipeline — you MUST reach Step 6 (Story JSON) for the build to be considered complete.**
- **CRITICAL: Story JSON is generated ONLY via `Assets/Editor/build_story.py`.** The script reads `Assets/Editor/BuildContext.json` (skeleton + paths, written by pre-build), `Assets/Editor/LastGOQIds.json` (ID_MAP), and `Assets/Editor/build_moments.json` (the per-build moment table you write in Step 6). Reading prior-build Story JSON files under `_Backups/` for shape lookup is **BANNED** — the framework's `skeleton-guide.md` and the script's emitter tables are the only canonical source. If the script halts because a storyboard introduced an unknown action/trigger keyword, follow the **HALT-or-extend protocol**: add the new keyword to BOTH `.claude/skills/vrse-module-pipeline/templates/skeleton-guide.md` and `Assets/Editor/build_story.py`'s `ACTION_EMITTERS` / `TRIGGER_EMITTERS`, then re-run. Never inline action shapes ad-hoc.
- **NEVER batch dependent operations** — if step N needs step N-1's result, run sequentially. For partial batch failure handling, see `batching-vrse-mcp-operations` skill.
- `refresh_asset_db` → any script usage must be sequential (domain reload + reconnect wait)
- `set_transform` position/rotation/scale = strings `"x,y,z"` not arrays
- Use `execute_menu_item` — never `execute_editor_script` (Windows path-too-long)
- `add_gameobject` with `type: primitive` has NO mesh — use `execute_menu_item("GameObject/3D Object/Cube")` for geometry
- Append per-object `[MenuItem]` entries to `Assets/Editor/TempVRseConverter.cs` below the `// === GENERATED MENU ITEMS BELOW ===` marker — never rewrite the helpers above it
- **Two scenes:** Art scene (loaded additively, contains meshes) + Dev scene (VRse framework objects). Duplication flows art→dev.
- **`pivot` type ALWAYS uses `DuplicateAndSetupGrabbable` — NEVER `DuplicateFromArtScene`**. `DuplicateFromArtScene` produces a raw mesh+GOQ only (no Rigidbody, no grabbable stack). Pivot = full grabbable conversion + `MetaXRPivotRotateLimiter`. This is the most common mistake — double-check every pivot C# menu item.
- **Verify system object names exactly before writing Story JSON** — system objects like the timer and SFX player live under `#h2 Vrse System`. Always run `find_gameobjects` to confirm the exact name. In this project: timer = `CountDownTimer` (capital D), SFX = `SFXPlayer`. Never assume lowercase.
- **SFXPlayer `_audioSource` must be wired** — after scene build, run `get_components` on the SFXPlayer GameObject and confirm `_audioSource` is not null. If null, add a `[MenuItem]` fix using reflection or SerializedObject to wire it.
- **All converted interactables start disabled** — `DuplicateAndSetupGrabbable` / `DuplicateAndSetupTouchable` (and `*FromArt` variants) automatically set `enableOnStart = false` on the `MetaXRBaseItem` component. Objects must be spawned via Story JSON `Objects.Spawn` — do NOT manually set `enableOnStart = true`.
- **Logical name = vrse_name = dev-scene name = JSON Query value** (the **naming axis**). The pipeline enforces this single axis throughout: the dev-scene wrapper is always renamed to the logical name (= the spec's `vrse_name`, which is auto-set to the logical name written in the storyboard's `## Objects` line). Only the art prefab (`source_object`) is allowed to differ — the converter bridges that gap by renaming the duplicate. All children derive from the wrapper name via the suffix convention below.

  **Naming Convention Table (art scene → dev scene):**

  | Component | Name Pattern | Example | Notes |
  |---|---|---|---|
  | **Wrapper** | `VrseName` (= logical name from spec) | `BananaCover` | Top-level interactable; renamed during conversion if source ≠ logical |
  | **Mesh child** | `VrseName_Mesh` | `BananaCover_Mesh` | Converter adds `_Mesh` suffix to the logical name |
  | **Tooltip** | `VrseName_ToolTip` | `BananaCover_ToolTip` | Strip underscores from VrseName |
  | **Ghost highlight** | `Open/CloseVrseName_GhostHighlight` | `OpenBananaCover_GhostHighlight` | Strip underscores |
  | **PlacePoint** | `VrseName_PlacePoint` or `VrseName_PP` | `BananaCover_PP` | `_PP` for art markers, `_PlacePoint` for dev objects |
  | **Spawn Point** | `SP_Name` or `Name_SP` | `Detector_SP` | Teleport destination |

  **Common prefixes from art scenes:**
  - `GRB_*` = Grabbable object (mesh + interactive wrapper)
  - `*_PP` = PlacePoint art marker (empty GO at target position)
  - `*_SP` or `SP_*` = Spawn/teleport point
  - `*_U_SP` = Unit/SharedPlatform variant suffix (preserve as-is from art)

  **When `source_object` ≠ logical name:** The first param to `DuplicateAndSetupGrabbable` is the art scene name (source), the second is the logical name (= vrse_name). The mesh child will be `LogicalName_Mesh`, NOT `SourceName_Mesh`. Step 4's naming-axis verification HALTs if the wrapper does not end up with the logical name after conversion.

  **Mesh child naming fallback:** If `{name}_Mesh` is not found in `LastGOQIds.json`, search for any object whose path contains `{name}/Mesh/` — the first child under that path is the mesh child regardless of its actual name. Log the actual name for use in Story JSON ID resolution.

## Execution Sequence

### Step 0: Pre-flight Check

**Step 0a — Read `Assets/Editor/BuildContext.json` FIRST (before any other tool call).**

Pre-build writes this file at session start with:
- `scenePaths.{artScene, devScene, storyJson}` — canonical paths for this build
- `containerPaths.{grabbable, touchable, placepoint, props, spawnPointsRoot}` — dev-scene hierarchy
- `templates.fullModuleSkeleton` — generic chapter/moment skeleton (~2 KB)
- `templates.skeletonGuide` — storyboard-action → JSON-action translation tables + 9 reusable patterns (~24 KB)
- `catalogs.{actions, triggers, moments}` — paths to the catalog files

**These are the framework's canonical source of truth for Story JSON.** You will NOT read prior-build Story JSON backups for shape lookup at any point in this build (banned by the rule above). If `BuildContext.json` is missing → **HALT (Class 1)**: pre-build did not run; ask the user to re-launch the build through the orchestrator.

**Read scene paths from the YAML spec `module:` block:**
```yaml
module:
  art_scene: "Assets/Scenes/Art/Module_Art.unity"
  dev_scene: "Assets/Scenes/Dev/Module_Dev.unity"
  story_json: "Assets/StreamingAssets/Story Files/Project/Module.json"
  story_json_mode: new
```
These are written by `interpreting-storyboard-specs` from the storyboard frontmatter. Use them directly — no `<scene>` block needed.

If a `<scene>` block is present in the prompt it takes precedence (backwards compatibility).

**Open scenes:**
1. Write `Assets/Editor/BuildConfig.json` with the scene paths from the storyboard frontmatter:
   ```json
   { "artScene": "Assets/Training/Art/.../Scene.unity", "devScene": "Assets/StudioProjects/.../Dev.unity" }
   ```
   Use `create_script` or write the file directly — this tells the generic scene loaders which scenes to use.
2. `open_scene` the dev scene (Single mode — correct)
3. Load art scene **additively** via: `execute_menu_item("VRseTemp/Scene/Load Art Scene Additive")`
   - **⚠️ NEVER use `open_scene` for the art scene — MCP has no additive mode, it REPLACES the dev scene**
   - The menu item reads the path from `BuildConfig.json` and loads additively
   - To unload later: `execute_menu_item("VRseTemp/Scene/Unload Art Scene")`
4. `get_editor_screenshot` — **📸 Screenshot 1 of 3: Scene Load** — captures both scenes loaded

> **Screenshot budget: exactly 3 per full build.** Screenshots are cheap (~1,500 tokens each via vision, not raw base64), but still keep to these 3 fixed milestones only — never add extra per-object screenshots.

Run BEFORE any object creation:
```json
{ "method": "batch_execute", "params": { "commands": [
  { "method": "get_hierarchy" },
  { "method": "save_scene" }
]}}
```

**Verify from hierarchy:**
- `QueryObjects` exists → if not, **HALT**: "QueryObjects root not found in dev scene. Ensure the correct dev scene is open."
- **Append mode:** Read existing Story JSON file, count `chapters[]`, confirm spec's `chapterIndex` = `chapters.length`

**Read the scene's actual structure** — do NOT assume any template hierarchy. Note what parent nodes exist under `QueryObjects`. The scene may use:
- **TYPE-based (production):** `#h2 Interactables/#h3 Grabbable`, `#h3 Placepoint`, `#h3 Touchable`, `#h3 UI` + `#h2 Non Interactables/#h3 Objects`, `#h3 Colliders`
- **Chapter-based (simple):** objects placed directly under `QueryObjects` and inside named chapter containers
- Mixed or custom

For new modules with `hierarchy: type_based` in YAML spec, create the type-based container structure. Otherwise, use whatever structure already exists. Record the actual parent paths for each object type before proceeding.

**Art scene object discovery (CRITICAL — do this BEFORE writing any converter code):**

> **⚠️ `find_gameobjects` only searches the active (dev) scene — it CANNOT find objects in additively loaded scenes.** You MUST use a C# helper to scan across all loaded scenes.

Write a temporary `[MenuItem]` in `TempVRseConverter.cs` that lists all GameObjects in the art scene:
```csharp
[MenuItem("VRseTemp/00 List Art Scene Objects")]
public static void ListArtSceneObjects()
{
    var json = System.IO.File.ReadAllText("Assets/Editor/BuildConfig.json");
    var artSceneName = System.IO.Path.GetFileNameWithoutExtension(
        System.Text.RegularExpressions.Regex.Match(json, "\"artScene\"\\s*:\\s*\"([^\"]+)\"").Groups[1].Value);
    var all = Resources.FindObjectsOfTypeAll<GameObject>();
    foreach (var go in all)
    {
        if (go.scene.name == artSceneName && go.hideFlags == HideFlags.None)
            Debug.Log($"[ART] {GetHierarchyPath(go)}");
    }
}
```
Run this ONCE after loading scenes. From the output, build an **Art Object Registry** — the complete list of objects available in the art scene with their full paths.

**Art scene scan troubleshooting:**

| Scan result | Diagnosis | Fix |
|---|---|---|
| Zero `[ART]` lines in console | Art scene not loaded or wrong scene name in BuildConfig.json | Verify `BuildConfig.json` `artScene` path matches the actual file, then re-run `VRseTemp/Scene/Load Art Scene Additive` |
| Objects found but none match spec `source_object` names | Art scene variant mismatch (e.g., wrong LOD version or region variant) | List the actual object names from the scan output and ask the user which art scene to use |
| Compilation error on scan helper | Syntax issue in the `ListArtSceneObjects` method | Check console for the exact error, fix the C# method, run `refresh_asset_db`, then retry |

**Source object verification (CRITICAL — using Art Object Registry, NOT find_gameobjects):**
For each `source_object` in the spec, check the Art Object Registry:
- If source found → ✅ proceed
- If source NOT found → **HALT** with error: `"Source object 'X' not found in art scene '{artSceneName}'. Check exact name in the Art Object Registry output above."`
- **NEVER silently substitute a placeholder cube** for a missing source_object

**Duplicate name detection (Plan H — Class 2 WARN, NOT HALT):** After the registry scan, for every spec object that has a `source_object` set, count how many art objects match that name across all parents.

- **0 matches** → covered by the source-not-found HALT above (Class 1 — file-system absence is irrecoverable).
- **1 match** → proceed as normal.
- **2+ matches AND `source_parent` is NOT specified in the spec** → **WARN, do NOT halt.** Pick the lexicographically-first match by full path (e.g. `Detector/X` < `LeftWing/X`). Continue the build. Append a 🟡 entry to `<ModuleName>_review.md`:

  ```
  ### R<N> — Ambiguous source for '<X>' (Stage 0)
  - Location: storyboard '## Objects' line declaring '[source: <X>]'
  - Issue: '<X>' matched multiple art-scene objects under different parents
  - Placeholder: picked '<picked_parent>/<X>' (lexicographic first)
  - Alternatives: <list of other parents>
  - Fix: Add [source_parent: <picked_parent>] to disambiguate, OR delete the
    unused art object, OR confirm the picked one is correct.
  ```

- **2+ matches AND `source_parent` is specified** → verify the parent path resolves to exactly one match in the registry. If yes, proceed with the disambiguated converter (see "Source Name Disambiguation" below). If `source_parent` resolves to zero matches → HALT (Class 1: the storyboard's disambiguation hint is wrong, fix it). If `source_parent` still resolves to multiple matches (very rare — same parent name appears multiple times in the art hierarchy) → WARN per the rule above and pick the first.

**Rationale (Plan H):** the historical silent-failure mode (generic helper picks first match silently) is closed because the pick is now logged with attribution. The user can always inspect the review.md and fix the storyboard with `[source_parent:]`, or accept the first-match choice. Halting here would force a retry cycle for a recoverable ambiguity; better to build with a placeholder and let the user audit.

**Clean slate check (prevents stale objects from prior cancelled builds):**
Check if `QueryObjects` already has converted objects (with `MetaXRGrabbableWrapper` or `GameObjectQuery`). If stale objects exist from a prior build:
1. List them: `get_hierarchy` on `QueryObjects`
2. If they match the current spec → **inventory them for reuse** (skip re-conversion, just verify components)
3. If they don't match or are partial → **delete them** via `delete_gameobject` + `save_scene` before proceeding
This prevents the "found stale partial object → diagnose → delete → retry" cycle that wastes minutes.

**Shared object analysis:**
Build a usage map — scan every moment's triggers and actions across ALL chapters. An object is "referenced" by a moment if its name appears in ANY `trigger.Query` or `action.Query` field:
```
USAGE MAP:
  Wheel → [Ch1, Ch2]    ← shared (2+ chapters) → place directly under QueryObjects
  LockoutCover → [Ch1]  ← chapter-exclusive → place inside that chapter's container
```
Objects used in 2+ chapters go under `QueryObjects` directly (or in a `Common` group if one exists). Chapter-exclusive objects go inside their chapter container.

### Step 1: Chapter Containers
For each chapter in the spec, check if a container already exists under `QueryObjects`. If not, create it:
```json
{ "method": "add_gameobject", "params": { "type": "empty", "name": "CHAPTER 1 - CHAPTER NAME", "parent": "QueryObjects" } }
{ "method": "add_component", "params": { "path": "QueryObjects/CHAPTER 1 - CHAPTER NAME", "component": "GameObjectQuery" } }
```
Container naming convention: `"CHAPTER {N+1} - {NAME_UPPER}"` (e.g. chapterIndex 0 → `"CHAPTER 1 - INTRODUCTION AND SAFETY OVERVIEW"`).

Skip creation if the container already exists. Use `get_components` to verify GOQ is present.

**Object parent paths (adapt to actual scene structure):**
- Shared objects → `QueryObjects` (directly, or inside a `Common` node if one exists)
- Chapter-exclusive → `QueryObjects/CHAPTER N - NAME`

**✅ Checkpoint:** All chapter containers exist with `GameObjectQuery`.

### Step 2: Append ALL Menu Items to TempVRseConverter.cs (ONE pass — no edits after refresh)

> **CRITICAL: Write ALL converter menu items in a SINGLE Edit operation.** Cross-reference every `source_object` against the Art Object Registry from Step 0 BEFORE writing any code. If a source name doesn't match the registry, fix it NOW — not after domain reload. Each extra edit → extra `refresh_asset_db` → extra domain reload → extra MCP disconnect/reconnect → 30+ seconds wasted per cycle. The goal is: **write once, compile once, refresh once.**

The base file at `Assets/Editor/TempVRseConverter.cs` contains:
- `SetupGrabbable(name, parent, pos)` — for objects already in scene (no mesh copy)
- `DuplicateFromScene(source, vrse, parent, pos)` — duplicates from art scene preserving mesh, NO conversion
- `DuplicateAndSetupGrabbable(source, vrse, parent, pos)` — duplicates + converts to grabbable
- `DuplicateAndSetupTouchable(source, vrse, parent, pos)` — duplicates + converts to touchable

**Only append** per-object `[MenuItem]` entries below the `// === GENERATED MENU ITEMS BELOW ===` marker. Never rewrite the helpers above it.

**Type-to-helper mapping (strict — use correct helper for each type):**

| Spec type | Has source_object? | Has embedded_in? | Menu item pattern | Helper |
|---|---|---|---|---|
| `grabbable` | Yes | No | `DupSetup ArtName` | `DuplicateAndSetupGrabbable("ArtName", "LogicalName", parent, pos)` — source=art name, second arg=logical name (= spec's vrse_name, always equal to logical) |
| `grabbable` | No | No | `Setup X` | Create cube first, then `SetupGrabbable("X", parent, pos)` |
| `touchable` | Yes | No | `DupSetup ArtName` | `DuplicateAndSetupTouchable("ArtName", "LogicalName", parent, pos)` — source=art name, second arg=logical name |
| `touchable` | No | No | `Setup X` | Create empty, then convert via selection |
| `pivot` | Yes | No | `DupSetup ArtName` | `DuplicateAndSetupGrabbable("ArtName", "LogicalName", parent, pos)` then `add_component MetaXRPivotRotateLimiter` — **⚠️ MUST use DuplicateAndSetupGrabbable, NEVER DuplicateFromArtScene** |
| `placepoint` | — | No | (see PlacePoint recipe) | No DuplicateAndSetup variant needed |
| `simple` | — | No | (batch_execute) | Just add_gameobject + GameObjectQuery |
| any | — | Yes | `EmbedGOQ X` | `AddGOQToEmbeddedChild("ParentName", "X")` — run AFTER parent is converted |

**Source Name Disambiguation (when art scene has duplicate names):**

When the Art Object Registry (Step 0) shows TWO objects with the same name under different parents, the generic `DuplicateAndSetupGrabbable` will pick the FIRST match — which may be the wrong one or an already-converted copy. You MUST write a **scene-scoped helper** instead:

```csharp
[MenuItem("VRseTemp/DupSetup GRB_SafetyDoor_C (from Door C)")]
public static void DupSetupSafetyDoorC()
{
    const string ART_SCENE = "AZ_AFT_Ch_5";
    const string SOURCE_NAME = "GRB_SafetyDoor_D";    // actual art name
    const string VRSE_NAME = "GRB_SafetyDoor_C";      // desired dev scene name
    const string SOURCE_PARENT = "Door C";              // disambiguator

    var all = Resources.FindObjectsOfTypeAll<GameObject>();
    GameObject artSource = null;
    foreach (var go in all)
    {
        if (go.name == SOURCE_NAME
            && go.scene.name == ART_SCENE
            && go.GetComponent<IGrabbableWrapper>() == null   // raw, not converted
            && go.transform.parent?.name == SOURCE_PARENT)    // correct parent
        {
            artSource = go;
            break;
        }
    }
    if (artSource == null) { Debug.LogError($"[MT] Source '{SOURCE_NAME}' under '{SOURCE_PARENT}' not found in '{ART_SCENE}'"); return; }
    DuplicateAndSetupGrabbable_FromSource(artSource, VRSE_NAME, qo, pos);
}
```

**When to use:** Any time `source_object` differs from the logical name, or when `source_parent` is specified in the spec (which is required by Step 0 for any source with duplicate art-scene matches). The key differences from the generic helper:
1. Scopes search to art scene only (`go.scene.name == ART_SCENE`)
2. Filters out already-converted copies (`!IGrabbableWrapper`)
3. Uses parent name to disambiguate duplicates (`go.transform.parent?.name`)
4. Renames the duplicate to the logical name (= `vrse_name` per the spec) instead of keeping `SOURCE_NAME`

**`embedded_in` objects — key rules:**
- Do NOT generate a `DupSetup` or `Setup` menu item — the object already exists inside the converted parent
- Generate an `EmbedGOQ` menu item instead: `AddGOQToEmbeddedChild("ParentName", "ChildName")`
- Run the `EmbedGOQ` menu item AFTER the parent's `DupSetup` + `save_scene`
- Known post-conversion path: `ParentName/Mesh/ParentName_Mesh` for direct mesh child; deeper children at `ParentName/Mesh/ParentName_Mesh/ChildName`
- **Animators are automatically restored** by `DuplicateAndSetupGrabbable` — no manual step needed. The helper captures Animator + controller references before conversion and restores any that are missing on the post-conversion hierarchy.

**Parent parameter — use the actual parent path from the scene hierarchy (determined in Step 0):**
- Shared objects: `parent = "QueryObjects"` (or `"QueryObjects/Common"` if that node exists)
- Chapter-exclusive: `parent = "QueryObjects/CHAPTER N - NAME"`

Example entries:
```csharp
// Chapter-exclusive grabbable from art scene
[MenuItem("VRseTemp/DupSetup LockoutCover")]
public static void DupSetupLockoutCover() =>
    DuplicateAndSetupGrabbable("LockoutDevice", "LockoutDevice", "QueryObjects/CHAPTER 2 - LOCAL CONTROL SWITCH AND MECHANICAL ISOLATION", new Vector3(0,1,1.5f));

// Pivot (grabbable + MetaXRPivotRotateLimiter) — use DuplicateAndSetupGrabbable, then add_component MetaXRPivotRotateLimiter
[MenuItem("VRseTemp/DupSetup Wheel")]
public static void DupSetupWheel() =>
    DuplicateAndSetupGrabbable("GateValveWheel", "GateValveWheel", "QueryObjects", new Vector3(0,1,1.5f));
// After execute: add_component { path: "QueryObjects/Wheel", component: "MetaXRPivotRotateLimiter" }

// Embedded child — run AFTER DupSetup of parent (LockoutCover). Object lives inside the converted wrapper.
// Adds GOQ to LockoutCover_Mesh (created by converter at LockoutCover/Mesh/LockoutCover_Mesh).
// Animators on LockoutCover and its children are auto-restored by DuplicateAndSetupGrabbable.
[MenuItem("VRseTemp/EmbedGOQ LockoutCover_Mesh")]
public static void EmbedGOQLockoutCoverMesh() =>
    AddGOQToEmbeddedChild("LockoutCover", "LockoutCover_Mesh");

// Deeper embedded child (e.g., LockoutCoverA inside LockoutCover_Mesh)
[MenuItem("VRseTemp/EmbedGOQ LockoutCoverA")]
public static void EmbedGOQLockoutCoverA() =>
    AddGOQToEmbeddedChild("LockoutCover", "LockoutCoverA");

// Chapter-exclusive touchable from art scene (under chapter container)
[MenuItem("VRseTemp/DupSetup SafetySwitch")]
public static void DupSetupSafetySwitch() =>
    DuplicateAndSetupTouchable("SafetySwitch_Prop", "SafetySwitch_Prop", "QueryObjects/CHAPTER 1 - CHAPTER NAME", new Vector3(0,1,1.5f));

// Chapter-exclusive grabbable (new cube, no art source)
[MenuItem("VRseTemp/Setup TestBlock")]
public static void SetupTestBlock() =>
    SetupGrabbable("TestBlock", "QueryObjects/CHAPTER 1 - CHAPTER NAME", new Vector3(0.5f, 1.0f, 1.5f));
```

**C# self-review (BEFORE compilation gate — run this mentally for every object you just wrote):**

For each object added to TempVRseConverter.cs, confirm the helper matches the spec type:

| Spec type | Required helper | HALT if you wrote instead |
|---|---|---|
| `grabbable` | `DuplicateAndSetupGrabbable` | `DuplicateFromArtScene` ❌ |
| `pivot` | `DuplicateAndSetupGrabbable` + then `add MetaXRPivotRotateLimiter` | `DuplicateFromArtScene` ❌ |
| `touchable` | `DuplicateAndSetupTouchable` | `DuplicateFromArtScene` ❌ |
| `simple` | `DuplicateFromArtScene` | — |

`DuplicateFromArtScene` produces **raw mesh + GOQ only** — no Rigidbody, no grabbable stack. It is ONLY correct for `simple` type. If you wrote it for a pivot or grabbable, fix the C# before continuing.

Also confirm: for every `GetComponent<X>()` or `AddComponent<X>()` in new code, grep the class name first to verify the exact namespace — never guess it.

**Compilation gate (BEFORE refresh — catches TempVRseConverter.cs errors early):**
```json
{ "method": "get_compilation_errors" }
```
If any errors reference `TempVRseConverter.cs` → fix before proceeding. Do NOT call `refresh_asset_db` with a broken script — domain reload will fail silently and menu items won't exist.

### Step 3: ONE `refresh_asset_db`
Wait for domain reload + reconnect. Only ONE refresh for all objects.

### Step 4: Execute Setup Menu Items
Run each sequentially:
```json
{ "method": "execute_menu_item", "params": { "menu_path": "VRseTemp/DupSetup ObjectName" }}
```

**Save after each object (prevents ID=-1 and limits rollback scope):**
```json
{ "method": "save_scene" }
```
Run `save_scene` immediately after each successful menu item before moving to the next object. If a conversion fails, you only need to fix that one object — not redo everything.

**Post-conversion verification (CRITICAL — run after EACH menu item):**

> **Fix 1 & 4: Use targeted path-based `get_components`, NOT `get_hierarchy`.**
> `get_hierarchy` returns the full scene (2MB+) and its component list is position-dependent
> (objects with many components like grabbables show only a few). Always query by full path.

For shared objects (directly under QueryObjects):
```json
{ "method": "get_components", "params": { "path": "QueryObjects/ObjectName" }}
```
For chapter-exclusive objects:
```json
{ "method": "get_components", "params": { "path": "QueryObjects/CHAPTER N - CHAPTER NAME/ObjectName" }}
```
Use the exact chapter container name from your scene hierarchy.

**Typed component assertions — HALT immediately if any required component is missing:**

| Type | Required components | Missing any → |
|---|---|---|
| `grabbable` | `MetaXRGrabbableWrapper`, `NetworkGrabbableWrapper`, `GameObjectQuery` | **HALT (Class 1)** — runtime needs Rigidbody/grabbable stack to function; missing = no physics |
| `pivot` | `MetaXRGrabbableWrapper`, `NetworkGrabbableWrapper`, `MetaXRPivotRotateLimiter`, `GameObjectQuery` | **HALT (Class 1)** — missing grabbable = wrong helper; missing limiter = no rotation |
| `touchable` | `HandTouchDetectable`, `GameObjectQuery`, **`Collider` (isTrigger=true)** | **WARN (Class 2)** — emit 🟡 review.md entry: "Type variance on '<X>' — touchable missing components, may not respond to hand touch. Confirm prefab structure or change type." Continue build. |
| `placepoint` | `MetaXRPlacePointWrapper`, `NetworkPlacePointWrapper`, `GameObjectQuery` | **HALT (Class 1)** — missing wrapper means placement triggers can't fire |
| `simple` | `GameObjectQuery`, **`Collider` (isTrigger=true) if used as CollisionTrigger target** | **WARN (Class 2)** — emit 🟡 review.md entry: "GameObjectQuery missing on simple object '<X>' — Spawn/Despawn may fail at runtime. Add component manually." Continue build. |
| `embedded` | `GameObjectQuery` (at full child path) | **HALT (Class 1)** — EmbedGOQ must run; without it the child cannot be queried |

**Trigger-collider auto-attach (NEW — `VRseBatchSetup.cs`):** `setup_touchable` and `duplicate` tasks now call `EnsureTriggerCollider` after creating the dev-scene object. If the source mesh did not bring a `Collider` along, a `BoxCollider` sized from the mesh's local bounds is added with `isTrigger=true`. This closes the silent failure where `HandTouchTrigger` / `CollisionTrigger` / `PlacePointTrigger` would never fire on objects whose art source happened to lack a collider. Existing colliders are respected — the helper is a no-op if any `Collider` is already present in the hierarchy. If a mesh-less object reaches the helper, a warning is logged and verification will still flag it.

**Grabbable collider tightening (NEW — `VRseBatchSetup.cs`):** `setup_grabbable` now calls `TightenGrabbableCollider` after Meta XR conversion. Meta's converter adds a convex `MeshCollider` when the source has no collider — convex hulls of non-convex meshes (Allen keys, hooks, L-shapes) bulge far beyond the silhouette, which looks wrong in training scenes and can disrupt placepoint snapping. The helper replaces any auto-added `MeshCollider` with a mesh-tight `BoxCollider` sized from `mesh.bounds`. Hand-tuned `BoxCollider` / `SphereCollider` / `CapsuleCollider` from the art source are respected (left untouched). Pivots inherit this since they go through the same `setup_grabbable` task.

**Placepoint placement-mode passthrough (NEW — `VRseBatchSetup.cs`):** `create_placepoint` now accepts optional `force_place` / `held_place_only` fields (string `"true"` / `"false"`; omit to keep wrapper defaults). When emitting `batch_tasks.json` from the YAML spec, copy `properties.force_place` and `properties.held_place_only` from each placepoint object into the corresponding task. The spec interpreter sets these automatically for placepoints whose target grabbable is `GrabLock`-ed anywhere in the storyboard (see `interpreting-storyboard-specs/SKILL.md` Step 5.5 and `patterns.md` Pattern 13). Without this passthrough, grab-locked tools cannot snap to their return placepoint.

**Missing `MetaXRGrabbableWrapper` on a grabbable or pivot is NEVER intentional.** Do NOT proceed or note it as "possibly intentional" — always treat as a build error and fix before continuing.

**Naming-axis verification (NEW — runs in the same iteration as the component check):**

For every spec object, the dev-scene wrapper MUST be named exactly the logical name (= `vrse_name` per the spec). The pipeline enforces this single naming axis: logical name → vrse_name → dev-scene name → JSON Query value. Any divergence here causes silent runtime "object not found" failures downstream, so verify it now.

```json
{ "method": "find_gameobjects", "params": { "name_pattern": "<expected_name>", "search_scope": "scene" }}
```

Where `<expected_name>` = the spec's `vrse_name` for this object (= the logical name written before the type in the storyboard's `## Objects` line).

| Result | Action |
|---|---|
| Exactly one match under `QueryObjects/...` | ✅ proceed |
| Zero matches under `QueryObjects/...` | **HALT (Class 1)** with: `Step 4 verification: GameObject '<expected_name>' not found in dev scene under QueryObjects after conversion. Source: '<source_object>'. Type: '<type>'. Likely causes: (a) wrong DupSetup helper used (e.g., DuplicateFromArtScene on a pivot), (b) source picked from wrong art parent, (c) post-conversion rename did not run. Diagnose before retrying.` Stays HALT because downstream Story JSON would reference a GameObject that doesn't exist — runtime-broken. |
| Multiple matches under `QueryObjects/...` | **WARN (Class 2)** — keep the lexicographically-first instance, mark others for cleanup. Append 🟡 review.md entry: `Duplicate conversion of '<expected_name>' — N instances found (<paths>). Pipeline kept '<picked_path>'; others should be deleted before final delivery.` Continue build. |
| Match found but path is outside `QueryObjects` (e.g. under "Others") | Append a reparent fix per the recovery table — this is a known fixable mode |

**Mesh-child verification (for `grabbable`, `pivot`, `touchable`):**

The conversion auto-suffixes a `_Mesh` child under the wrapper (path: `QueryObjects/.../<expected_name>/Mesh/<expected_name>_Mesh`, or for embedded children, the deeper path documented in Step 3). The mesh child carries the renderer and is the target of `MetaLayerAction` outline highlights. Verify it exists:

```json
{ "method": "find_gameobjects", "params": { "name_pattern": "<expected_name>_Mesh", "search_scope": "scene" }}
```

| Result | Action |
|---|---|
| At least one match whose path is under the wrapper | ✅ proceed |
| Zero matches | **WARN (Class 2)** — fall back to using the wrapper itself as the highlight target (lossy: outline geometry will match the wrapper bounds rather than the mesh, which is usually still acceptable for tools/buttons but may look wrong on complex shapes). Append 🟡 review.md entry: `Mesh child '<expected_name>_Mesh' missing under wrapper. Outline highlights will use the wrapper as fallback — visual quality may be reduced. Check the art prefab has a 'Mesh' child, or accept the fallback if cosmetic-only.` Continue build. |

**Why these checks matter:** with the naming axis enforced, every Query value the Story JSON later emits is mechanically derived from a logical name. By verifying at Step 4 that each logical name resolves to exactly one wrapper (with the expected mesh child), we eliminate boundaries C, D, and E in the pipeline trust chain — Stage 5 (ID harvest) and Stage 6 (JSON emit) can trust their inputs by construction. Catching name failures here saves the "build succeeded → playtest broken" debugging session.

**Mesh check (geometry):** If `get_components` on the mesh child shows no `MeshFilter` or `SkinnedMeshRenderer` AND the object should have geometry: **HALT** — source object was not found in art scene or was a wrapper-only prefab.

**Parent check:** If `get_components` returns a result but the object is not found at the expected path, it landed under "Others". Append a reparent fix menu item and execute it.

If any check fails → diagnose the failure type and apply the targeted fix below. Do NOT continue to Story JSON with broken objects.

**Conversion Recovery (use when a conversion fails — do NOT rebuild from scratch):**

| Failure | Diagnosis | Fix |
|---|---|---|
| Object not found at expected path | Landed under "Others" | Append `[MenuItem("VRseTemp/Reparent X")]` calling `ReparentObject("X", "QueryObjects/CHAPTER N - NAME")` to TempVRseConverter.cs → refresh → execute |
| Missing `MetaXRGrabbableWrapper` | Conversion didn't run | Re-select object, re-run `DupSetup` menu item, save |
| Missing `MeshFilter` | Source object not in art scene | HALT — verify art scene is loaded additively, source name matches exactly |
| Missing `MetaXRPivotRotateLimiter` | Forgot to add after grabbable conversion | `add_component { path: "QueryObjects/.../ObjectName", component: "MetaXRPivotRotateLimiter" }` |
| Missing `GameObjectQuery` on embedded child | `EmbedGOQ` not run yet | Run the `EmbedGOQ` menu item for that child |
| `get_components` returns empty | Path is wrong | Run `find_gameobjects` to locate actual path, then re-verify |

After any recovery fix: `save_scene` → re-run `get_components` to confirm.

**✅ Checkpoint:** All objects pass component checks via full-path `get_components`.

**📸 Screenshot 2 of 3: All Interactables Set** — take this ONCE after ALL objects pass the checkpoint above:
```
select_gameobject("QueryObjects")
→ execute_menu_item("VRseTemp/FrameSelected")
→ get_editor_screenshot
```
This frames the entire QueryObjects hierarchy in the scene view, showing all converted interactables in place. Do NOT take per-object screenshots — only this one after all objects are confirmed.

**PP Transform Sync — ALWAYS run this, even if you think no placepoints exist:**
```json
{ "method": "execute_menu_item", "params": { "menu_path": "VRseTemp/Sync PP Transforms" }}
{ "method": "save_scene" }
```
Console should show `✅ 'X_PP': pos/rot/collider.size` for each placepoint. `0 synced` with no output = no placepoints found (fine if spec has none). Any `⚠️` = name mismatch between art marker and dev placepoint.

**Hard verify (mandatory — do NOT skip):**
For every placepoint in the spec, run `get_components` and confirm:
- `Transform.position` is **NOT** `(0, 1, 1.5)` — if it is, sync did not find the art marker
- `BoxCollider.size` is **NOT** `(1, 1, 1)` — if it is, the collider size was not synced from the marker's localScale
```json
{ "method": "get_components", "params": { "path": "QueryObjects/CHAPTER N - NAME/MyPlacePoint_PP" }}
```
If either check fails → **HALT**: check the `_PP` art marker name matches exactly (case-sensitive), confirm art scene is loaded additively, re-run sync and save.

### Step 4c: Configure PlaceAndAnimate Paths

> **Skip this step if:** No objects in the spec use `PlaceAndAnimate_Block` or have animate-on-place mechanics.

For each `PlaceAndAnimate_Block` instance in the scene:

1. **Detect mechanic type** from the YAML spec — look for keywords: "tighten", "screw", "insert", "slide", "lever", "drawer", "snap", "place and animate"
2. **Read the object's current world transform:**
   ```json
   { "method": "get_components", "params": { "path": "QueryObjects/.../ObjectName", "component": "Transform" }}
   ```
3. **Create a trigger collider** (child of the animated object):
   ```json
   { "method": "add_gameobject", "params": { "name": "PAATrigger", "parent": "QueryObjects/.../ObjectName", "type": "Empty" }}
   { "method": "add_collider", "params": { "game_object_path": "QueryObjects/.../ObjectName/PAATrigger", "type": "Box", "is_trigger": true, "size": "0.05,0.05,0.05" }}
   ```
4. **Compute path points** using the matching recipe from `building-blocks-catalog.md` → "PlaceAndAnimate Animation Path Recipes". Substitute the object's actual position/rotation/scale.
5. **Write a `[MenuItem]`** to `TempVRseConverter.cs` calling `PlaceAndAnimateConfigurator.ConfigurePath()`:
   ```csharp
   [MenuItem("VRseTemp/ConfigPAA_ObjectName")]
   public static void ConfigPAA_ObjectName() =>
       PlaceAndAnimateConfigurator.ConfigurePath(
           "QueryObjects/.../ObjectName",
           "PathName",
           "QueryObjects/.../ObjectName/PAATrigger",
           1.0f,
           new[] {
               new Vector3(x,y,z), new Vector3(rx,ry,rz), Vector3.one,  // start
               new Vector3(x,y,z), new Vector3(rx,ry,rz2), Vector3.one  // end
           });
   ```
6. **`refresh_asset_db`** → wait for compilation
7. **`execute_menu_item("VRseTemp/ConfigPAA_ObjectName")`**
8. **Verify:** `get_components(path: "QueryObjects/.../ObjectName", component: "MetaXRPlaceAndAnimate")` — confirm `_animationPaths` has entries with correct `PathName` and point count
9. **`save_scene`**

**Keyword → Recipe quick reference:**

| Storyboard keyword | Recipe | End transform change |
|---|---|---|
| tighten / screw CW | Screw CW | rot.z - 90 |
| loosen / unscrew / CCW | Screw CCW | rot.z + 90 |
| slide in / insert / push | Slide insert | pos + offset |
| place / snap / attach | Snap place | hover → surface |
| pull lever / flip switch | Lever pull | rot.x - 45 |
| open drawer / pull out | Drawer open | pos.z + distance |

**✅ Checkpoint:** All PlaceAndAnimate objects have configured `_animationPaths` with at least 2 path points each.

### Step 4.5: Spatial Placement (Auto-Position Interactables)

> **Purpose:** Objects created in Step 4 are at default positions `(0, 1, 1.5)`. This step uses spatial analysis tools to compute correct positions based on the environment geometry and storyboard context — no manual coordinate entry needed.

**Skip this step if:** ALL objects in the spec have explicit `position:` values that are NOT the default `[0, 1, 1.5]`.

**a. Analyze the environment:**
```json
{ "method": "spatial_analyze_scene" }
```
Returns all renderable objects with world-space bounds, 6 face centers, classification (surface/mechanism/panel/object), children, and discovered horizontal surfaces. Use this as the spatial index for all placement decisions.

**b. Probe complex objects (if storyboard references internal features like "rack", "shelf", "compartment"):**
```json
{ "method": "spatial_probe_surfaces", "params": { "target_object": "Table" }}
```
Returns all internal horizontal surfaces (shelves, racks) with heights, extents, and areas. Use when the storyboard says "place X on the rack" or "on the lower shelf" — the probe finds the exact Y height.

**c. For each interactable, determine placement using this decision tree:**

| Storyboard context | Relationship | How to compute position |
|---|---|---|
| "picks up from [surface]" / "on the table" | REST_ON_SURFACE | `discoveredSurfaces` or `probe_surfaces` → Y = surface.height + object.halfHeight |
| "turns/rotates on [mechanism]" | MECHANISM_ATTACHED | Check children of reference object for semantic match (e.g., "Axis", "Stem") → use child worldPos. Fallback: reference.surfaces.top |
| "places into/onto [target]" | TARGET_SNAP | `spatial_find_surface(target, direction)` → offset along normal |
| "presses on [panel]" | PANEL_MOUNTED | reference.surfaces.front + small offset along normal |
| "near [object]" / "beside [object]" | BESIDE | reference.worldPosition + offset along X or Z (use bounds.size to avoid overlap) |

**d. Batch-place all objects:**
```json
{ "method": "batch_execute", "params": { "commands": [
  { "method": "set_transform", "params": { "path": "QueryObjects/Wheel", "position": "2.0,1.5,3.0" }},
  { "method": "set_transform", "params": { "path": "QueryObjects/CHAPTER 1 - NAME/LockoutCover", "position": "-1.0,0.85,0.0" }}
]}}
```

**e. Validate placements:**
```json
{ "method": "spatial_check_placement", "params": { "game_object_path": "QueryObjects/Wheel" }}
```
Run on each placed object. Check the `issues` array — fix any:
- "Floating Xm above surface" → lower Y
- "Penetrates floor" → raise Y
- "Overlapping with: OtherObj" → offset X or Z

**f. Precision refinement (if check_placement reports issues):**
```json
{ "method": "spatial_find_surface", "params": { "target_object": "GateValve", "direction": "0,0,-1" }}
```
Use targeted surface finding + `spatial_raycast` for unusual angles. Max 2 refinement rounds, then proceed.

**g. PlacePoint-specific placement (CRITICAL — placepoints need position + rotation + collider size):**

PlacePoints are snap targets — they need more than just position. For each placepoint:

1. **Position** — from `spatial_find_surface` on the target object:
```json
{ "method": "spatial_find_surface", "params": { "target_object": "GateValve", "direction": "0,0,-1" }}
```
Result: `surfacePoint` = where to place, `surfaceNormal` = approach direction.
Offset the placepoint slightly along the normal (0.01-0.05m) so it sits just in front of the surface.

2. **Rotation** — compute from `surfaceNormal` so the placepoint faces the approach direction:

| Surface normal | Placepoint rotation | Meaning |
|---|---|---|
| `(0, 1, 0)` — top | `(0, 0, 0)` | Place from above (default) |
| `(0, -1, 0)` — bottom | `(180, 0, 0)` | Place from below |
| `(0, 0, 1)` — front | `(-90, 0, 0)` | Place from front |
| `(0, 0, -1)` — back | `(90, 0, 0)` | Place from back |
| `(1, 0, 0)` — right | `(0, 0, -90)` | Place from right |
| `(-1, 0, 0)` — left | `(0, 0, 90)` | Place from left |

For angled normals, compute `Quaternion.LookRotation(-normal, Vector3.up)` mentally — the placepoint's forward should point OPPOSITE to the normal (toward the surface).

3. **Collider size** — estimate from the corresponding grabbable's bounds:
```json
{ "method": "spatial_get_bounds", "params": { "game_object_path": "QueryObjects/PadLock" }}
```
Use `bounds.size` as the placepoint's BoxCollider size (with ~20% padding). If the grabbable doesn't exist yet or has no mesh, use these defaults:
```
Small (bolt, key):    collider size = (0.08, 0.08, 0.08)
Medium (lock, cover): collider size = (0.15, 0.15, 0.15)
Large (panel, tool):  collider size = (0.25, 0.25, 0.25)
```
Set via: `update_component { path: "PP_Name", component: "BoxCollider", properties: { size: "0.15,0.15,0.15" }}`

4. **After spatial placement, `Sync PP Transforms` still runs** — if art markers exist (ending in `_PP`), they OVERRIDE the spatial placement with exact artist-defined positions. This is intentional: spatial placement is the fallback, art markers are the authority.

**Size estimation (when object bounds aren't available yet — just created, no mesh):**
```
Small grabbable (bolt, key, switch):  halfHeight = 0.03m
Medium grabbable (cover, tool, lock): halfHeight = 0.08m
Large grabbable (panel, door):        halfHeight = 0.15m
Pivot (wheel, lever):                 halfHeight = 0.12m
PlacePoint:                           halfHeight = 0.0m (snap point only)
```

**Spatial tool reference:**
| Tool | When to use |
|---|---|
| `spatial_analyze_scene` | First call — full spatial index of the environment |
| `spatial_probe_surfaces` | Object has internal geometry (racks, shelves, compartments) |
| `spatial_get_bounds` | Need bounds of a specific object |
| `spatial_raycast` | Need to find what's at a specific point/direction |
| `spatial_find_surface` | Need exact surface point on a target from a direction |
| `spatial_check_placement` | Validate final position of a placed object |

**✅ Checkpoint:** All objects pass `spatial_check_placement` with `placementOk: true` (or issues are intentional, e.g., wall-mounted objects won't have a surface below).

### Step 5: Save + Build ID_MAP
```json
{ "method": "save_scene" }
{ "method": "save_scene" }
{ "method": "execute_menu_item", "params": { "menu_path": "VRseTemp/Log Module GOQ IDs" }}
```
The menu item logs IDs to console AND writes `Assets/Editor/LastGOQIds.json`. **Always read the file — never parse the console log:**
```
Read: Assets/Editor/LastGOQIds.json
```
The file contains `{ "name", "id", "path" }` entries for every object under QueryObjects. Build ID_MAP from this — it's reliable, structured, and survives session boundaries. If a broader diagnostic is needed (all scene objects), use `Log All GOQ IDs`.

**Build ID_MAP** from the result — a lookup table of every object name → ID:
```
ID_MAP:
  TestBlock → 843879           (under QueryObjects/CHAPTER 1 - NAME)
  TestPlacePoint → 843880      (under QueryObjects/CHAPTER 1 - NAME)
  CHAPTER 1 - NAME → 843881    (chapter container — use by ID for Spawn/Despawn)
  Wheel → 843884               (shared, directly under QueryObjects)
```
Chapter containers have unique names so can be referenced by name. Still prefer ID for Spawn/Despawn to be safe.

**ID verification gate (HARD HALT):**
1. Check ALL IDs > 0 (not -1)
2. If ANY ID is -1: save scene again, then immediately re-read IDs (no MCP wait tool — save triggers Unity's ID assignment synchronously)
3. If STILL -1 after 2nd save: **HALT** with list of objects with invalid IDs
4. **NEVER proceed to JSON generation with ID = -1** — this causes runtime lookup failures

**ID staleness check (append mode only — prevents writing stale IDs from a prior build):**
If `mode: append`, read the existing Story JSON and extract the IDs of any objects that also appear in the current build. Build a diff table:
```
STALE ID DIFF:
  WaterPressureGauge_Needle  old=351995  new=523355  ← CHANGED — update all refs in JSON
  LockoutCover               old=573639  new=573639  ← same ✅
```
Any object whose ID changed → update ALL occurrences in the Story JSON (trigger.ID, action.ID, grabbableName `#$`). Never overwrite with old IDs from a previous session.

**✅ Checkpoint:** All IDs verified > 0, no stale IDs from prior build.

### Step 5.5: Build Extended ID_MAP (optional)

> **Skip this step by default.** `build_story.py` consumes the flat `LastGOQIds.json` directly. The extended `IdMapEntry` form below is only needed if you've extended `build_story.py` (per the Step 6 HALT-or-extend protocol) to emit production patterns that reference mesh children, tooltips, or ghost highlights with explicit IDs (rare — most modules don't need this).

The flat `LastGOQIds.json` contains `{ name, id, path }` entries for every object under QueryObjects. If your extended emitters need richer records that link grabbables to their mesh children, tooltips, and ghost highlights:

**Build `IdMapEntry` records from the flat ID list:**

For each interactable object (grabbable/pivot/touchable) in the YAML spec `objects:` list:
1. Find the object's GOQ ID from the flat list → `entry.id` and `entry.queryId`
2. Find the mesh child by convention: look for `{name}_Mesh` in the flat list → `entry.meshId` and `entry.meshQueryId`
   - If the mesh child has a different name (e.g., `HandleWindow_A` for `BarrelZoneDoorA`), check the path — the mesh child lives under `{grabbable}/Mesh/.../{meshName}`
3. Find the tooltip: look for objects ending in `_ToolTip` whose path contains the grabbable name → `entry.tooltipId` and `entry.tooltipName`
4. Find the ghost highlight: look for objects ending in `_GhostHighlight` whose path is a sibling container of the grabbable → `entry.ghostId` and `entry.ghostName`
5. For placepoints: the main ID is also the `entry.placePointId`

**IMPORTANT: Ghost/tooltip names are NOT derivable from the grabbable name.** Example:
- Grabbable: `SafetyDoor_A` → Ghost: `OpenSafetyGlassA_GhostHighlight` (NOT `OpenSafetyDoorA`)
- Grabbable: `BarrelZoneDoorA` → Tooltip: `BarrelZoneDoorARotatable_ToolTip` (NOT `BarrelZoneDoorA_ToolTip`)

Always read actual names from `LastGOQIds.json` paths, never compute them.

**System IDs:** Query `VOPlayer` and `TriggerQueryObjectGuider` via `find_gameobjects` → record their GOQ IDs:
```json
{ "method": "find_gameobjects", "params": { "query": "VOPlayer", "include_inactive": true }}
{ "method": "find_gameobjects", "params": { "query": "TriggerQueryObjectGuider", "include_inactive": true }}
```
Then `get_components` on each → read `GameObjectQuery._ID`.

**HMI screen IDs (if applicable):** For modules with HMI button moments, query each screen object's GOQ ID and build `HMIScreenFlow` records mapping chapter transitions.

**Result:** A complete `Record<string, IdMapEntry>` + `SystemIds` + `HMIScreenFlow` map, ready for the generator.

---

### Step 6: Generate Story JSON via `build_story.py`

> **🛑 BANNED: Reading any file under `_Backups/` for shape lookup.** The framework's `templates.skeletonGuide` (already in context from Step 0a) and `Assets/Editor/build_story.py`'s emitter tables are the only canonical source for action/trigger JSON shapes. Reading prior-build Story JSON to "see how it looked last time" was the single largest waste in past builds (~9 min/build of re-reading + deliberation). Don't.

**Story JSON is generated ONLY via `Assets/Editor/build_story.py`.** The script is project-agnostic — it reads `BuildContext.json` for paths/skeleton, `LastGOQIds.json` for the ID_MAP, and `build_moments.json` (which you write below) for the per-build moment data, then emits the Story JSON to `scenePaths.storyJson`.

**How to invoke:**

1. **Author `Assets/Editor/build_moments.json`** — a declarative moment table using storyboard-action keywords. The schema mirrors `templates.skeletonGuide` exactly:

   ```json
   {
     "module": "Module Name",
     "defaults": {"firstWarningTimer": 30, "lastWarningTimer": 20},
     "chapters": [
       {
         "name": "Chapter Name",
         "chapterIndex": 0,
         "moments": [
           {
             "name": "Moment Name",
             "momentIndex": 0,
             "onAwake":  [{"action": "Spawn", "target": "X"}],
             "onStart":  [{"action": "VoiceOver", "text": "..."},
                          {"action": "Highlight", "target": "X"}],
             "onRight":  {
               "mode": "InOrder",
               "sets": [
                 {
                   "trigger": {"type": "Grab", "target": "X"},
                   "actions": [{"action": "Unhighlight", "target": "X"},
                               {"action": "VoiceOver", "text": "..."}]
                 }
               ]
             },
             "onWrong":         [],
             "onFirstWarning":  [{"action": "Haptics", "intensity": 0.3, "duration": 0.3},
                                 {"action": "VoiceOver", "text": "Hint VO"}],
             "onLastWarning":   [],
             "onEnd":           [{"action": "Despawn", "target": "X"}]
           }
         ]
       }
     ]
   }
   ```

   **Action keywords:** `VoiceOver`, `Spawn`, `Despawn`, `Highlight`, `Unhighlight`, `EnableGrab`, `DisableGrab`, `EnableGrabFor`, `GrabLock`, `GrabUnlock`, `ForceRelease`, `Teleport`, `Animation`, `Haptics`, `Timer`, `SFX`, `UnlockRotation`, `GuidanceArrow`, `LockMovement`, `UnlockMovement`, `CameraFade`, `ToastMessage`. Full per-keyword schemas are in `templates.skeletonGuide`.

   **Trigger types:** `Grab`, `Release`, `Touch`, `Place`, `Button`, `Collision`, `Pivot`, `MCQ`, `Timer`. Same — full schemas in `templates.skeletonGuide`.

2. **Run the script** via Bash:

   ```bash
   python "{{UNITY_PROJECT}}/Assets/Editor/build_story.py"
   ```

   On success: `[build_story] Wrote ... Chapters: N  Moments: M`. On any unrecognized action/trigger keyword, the script HALTs naming the missing keyword.

3. **HALT-or-extend protocol** — when the script halts on an unknown keyword:
   - Add the new shape to `.claude/skills/vrse-module-pipeline/templates/skeleton-guide.md` (the human-facing canonical reference).
   - Mirror the same shape in `Assets/Editor/build_story.py` — add an emitter function and register it in `ACTION_EMITTERS` or `TRIGGER_EMITTERS`.
   - Re-run the script. Future builds get the new keyword for free.
   - **Never inline a one-off shape** in `build_moments.json` or write a per-build Python helper — that's exactly the failure mode this script exists to prevent.

> **CRITICAL FORMAT RULES (enforced by `build_story.py`; if you ever inspect the output, verify these):**
> - `"name"` for chapters/moments (NOT `"chapterName"`)
> - `onRight`: `{"mode": "InOrder" | "Any" | "Random", "triggerActionSets": [...]}`
> - `onWrong`: bare array `[]` (NOT `{"actions": []}`)
> - `defaults`: string (JSON-encoded), e.g. `"{\"firstWarningTimer\":30}"`
> - `studio: {"id": ""}` on every chapter and moment
> - All lifecycle slots present: `onAwake`, `onStart`, `onRight`, `onWrong`, `onFirstWarning`, `onLastWarning`, `onEnd`
> - All action/trigger `ID` fields = `-1` — runtime resolves by `Query`. Only `Teleport.targetTransform`, `PlacePointTrigger.grabbableName`, `Timer.Query`, and `SFX.Query` embed numeric IDs (via `Name#$<ID>`).

**Shared object lifecycle** — `build_story.py` does NOT auto-balance Spawn/Despawn across moments (each moment is emitted independently from `build_moments.json`). You are responsible for placing:
1. The FIRST moment that uses a shared object → `Spawn` in its `onAwake`
2. The LAST moment that uses it → `Despawn` in its `onEnd`

Step 7 (Spawn/Despawn balance check) audits this and auto-fixes imbalances if found.

**Writing the Story JSON file:**
- Always `Read` the target file first (satisfies Write tool requirement)
- `mode: new` → Write full `JSON.stringify(doc, null, 2)`
- `mode: append` → Read existing → merge new chapters → Write

**✅ Checkpoint:** Before writing, validate:
- Every `Query` value matches a key in ID_MAP
- Every `grabbableName` has `#$` + correct ID
- `formatVersion: "2.0"` present
- `chapterIndex`/`momentIndex` sequential from 0
- All lifecycle slots present

### Step 6.5: Variant Generation (optional)

> **Skip this step unless `module.variants` explicitly includes `partially_guided` or `evaluation`.** Variant stripping is not currently built into `build_story.py`. If the module spec requires variants, follow the **HALT-or-extend protocol**: add a `--variant` flag to `build_story.py` that strips guidance actions per the rules below, then re-run for each variant. Mirror the spec in `templates/skeleton-guide.md` so it's discoverable.

**Strip rules (when extending `build_story.py` to support variants):**

For variants `PartiallyGuided` and `Evaluation`, strip from each moment's `onStart.actions` and every `onRight.triggerActionSets[].actions`:
- `VoiceOver` actions
- `MetaLayerAction` actions
- `TargetGuidanceArrowAction` actions
- `Objects.Spawn` / `Objects.Despawn` where `Query` contains `_ToolTip` or `_GhostHighlight`

**Preserve:** triggers, `GrabbablePropertyChangeAction`, `PivotRotateLimiterAction`, `onAwake`, `onEnd`. Interactive mechanics remain identical across all variants.

**Output:** save as `{Module}_TrainingStory_PartiallyGuided.json` and `{Module}_TrainingStory_Evaluation.json` next to the Training file.

### Step 7: Spawn/Despawn Balance Check
Scan the written JSON mechanically — enumerate every unique `Query` value that appears in any `Objects` action, then verify balance.

**Step 8a: Build the spawn ledger**
Go through ALL moments across ALL chapters. For every `Objects` action (`Option: "Spawn"` or `Option: "Despawn"`), record:
```
SPAWN LEDGER:
  Query                              | First Spawn          | Last Despawn
  -----------------------------------|----------------------|---------------------
  CHAPTER 1 - INTRO                  | Ch0 M0 onAwake       | Ch0 M2 onEnd  ✅
  CHAPTER 2 - ISOLATION              | Ch1 M0 onAwake       | Ch1 M3 onEnd  ✅
  Wheel                              | Ch0 M1 onAwake       | Ch2 M3 onEnd  ✅
  LockoutCover                       | — MISSING SPAWN —    |               ❌
```

**Step 8b: Verify every Spawned object is also Despawned**
For each row in the ledger:
- No Spawn → add `Objects.Spawn` to the first moment that references it in a trigger/action
- No Despawn → add `Objects.Despawn` to the LAST moment across all chapters that references it in `onEnd`
- If both are missing → object is neither created nor cleaned up — investigate spec

**Step 8c: Verify every trigger Query is Spawned before it fires**
For every trigger in `onRight`/`onWrong`, confirm the referenced object has a Spawn action in a moment that comes BEFORE the trigger's moment (by chapterIndex then momentIndex). If not → add Spawn to that chapter's first moment `onAwake`.

Rewrite the file if any fixes were needed.

**Plan H — log auto-fixes to review.md (Class 2):** every auto-inserted Spawn or Despawn is a soft decision the user should be able to audit. For each fix applied in Step 8b/8c, append a 🟡 entry to `<ModuleName>_review.md`:

```
### R<N> — Lifecycle auto-balanced for '<Query>' (Step 7)
- Issue: object referenced in triggers/actions but missing <Spawn|Despawn>
- Auto-fix: inserted Objects.<Spawn|Despawn> in <Chapter N, Moment M> <onAwake|onEnd>
- Verify: confirm the auto-inserted lifecycle matches your intent — sometimes
  the object should be in a different chapter container or use different timing.
```

Continue the build after auto-fixing — do NOT halt. The user reviews the auto-fixes post-build.

### Step 8: Final Validation Sweep

> **Fix 4: Do NOT use `get_hierarchy` for component validation** — it returns 2MB+ for large scenes
> and truncates component lists. Use targeted `get_components` per object instead.

**📸 Screenshot 3 of 3: Build Complete** — after Story JSON is written and saves succeed:
```
select_gameobject("QueryObjects")
→ execute_menu_item("VRseTemp/FrameSelected")
→ get_editor_screenshot
```
This is the final state screenshot — full scene with all interactables in place and Story JSON written.

**Step 9a: Save + compilation check**
```json
{ "method": "batch_execute", "params": { "commands": [
  { "method": "save_scene" },
  { "method": "get_compilation_errors" },
  { "method": "find_missing_references" }
]}}
```
Check: 0 compilation errors. Ignore pre-existing `find_missing_references` entries on non-module objects.

**Step 9b: Per-object GOQ + component verification**
For every object in the spec, run `get_components` using its full hierarchy path:
```json
{ "method": "get_components", "params": { "path": "QueryObjects/Wheel" }}
{ "method": "get_components", "params": { "path": "QueryObjects/CHAPTER 1 - CHAPTER NAME/LockoutCover" }}
{ "method": "get_components", "params": { "path": "QueryObjects/CHAPTER 2 - CHAPTER NAME/WaterPressureGauge_Needle" }}
```

**Embedded objects** — path is INSIDE the converted parent's hierarchy, NOT in the chapter container:
```json
{ "method": "get_components", "params": { "path": "LockoutCover/Mesh/LockoutCover_Mesh" }}
{ "method": "get_components", "params": { "path": "LockoutCover/Mesh/LockoutCover_Mesh/LockoutCoverA" }}
```
Confirm: embedded objects have `GameObjectQuery`. Optionally confirm `Animator` is present if the art source had one (auto-restored by converter, but worth verifying).

Batch these: all objects of the same chapter can run in parallel.
Confirm: every module object has `GameObjectQuery` and its type-specific wrapper components.

**Step 9c: Auto-patch minor issues found in 9a/9b**

If issues were found in the component or JSON checks above, apply targeted fixes and re-validate once (no more than one auto-patch pass):

| Issue found | Auto-fix |
|---|---|
| Object missing `GameObjectQuery` | `add_component { path: "...", component: "GameObjectQuery" }` → `save_scene` |
| Object missing `MetaXRPivotRotateLimiter` on pivot | `add_component` → `save_scene` |
| Story JSON has a `Query` value not matching any scene object name | Fix the name to match exactly, rewrite JSON file |
| Spawn/Despawn imbalance in JSON | Add missing Spawn/Despawn as per Step 7 rules, rewrite JSON |
| ID = -1 anywhere in JSON | **Should have been caught at Step 5.** Re-run Step 5's ID verification gate (save × 2 → Log GOQ IDs → read LastGOQIds.json → rebuild ID_MAP). If still -1 after re-verification → HALT with exact object names. |

After auto-patch: re-run `get_compilation_errors` + targeted `get_components` on patched objects to confirm fixed. If still failing after one patch pass → HALT with exact issue list.

**Step 9d: Run the module GOQ ID log to check for duplicate names**
```json
{ "method": "execute_menu_item", "params": { "menu_path": "VRseTemp/Log Module GOQ IDs" }}
```
Read console log output. This logs only objects under QueryObjects — no noise from pre-existing scene objects. The log flags duplicates with ⚠️. If any duplicates exist within the module → investigate which object has the correct ID and update Story JSON if needed. For scene-wide diagnostics, use `Log All GOQ IDs`.

**Step 9e: Finalize `<ModuleName>_review.md` (Plan H)**

Per Plan H, the review file initialized in `interpreting-storyboard-specs` Step 0.5 has been accumulated through every pipeline stage. Before declaring the build complete, finalize it:

1. Read the existing `<ModuleName>_review.md`.
2. Count the 🟡 (Class 2) review items and 🔵 (Class 3) informational notes that were appended during the build.
3. Replace the placeholder header lines with final values:
   ```
   **Build finished:** <ISO 8601 timestamp>
   **Status:** ✅ COMPLETED WITH N REVIEW ITEMS  (where N = count of 🟡 entries)
   ```
4. Replace the Summary block with final counts:
   ```
   ## Summary
   - 🔴 0 hard failures (build halted) — build completed; no Class 1 HALTs fired
   - 🟡 <count> review items (recommended fixes — open in Unity)
   - 🔵 <count> informational notes (defaults applied; audit if anything looks wrong)
   ```
5. Save the finalized review.md.
6. Output a one-line summary to the user: `Build complete. Review: <ModuleName>_review.md (🟡 <yellow_count> · 🔵 <blue_count>).` Direct the user to open the file before playtest.

If the review file was never initialized (Step 0.5 was skipped — should not happen, but defensive), create a minimal one with status `✅ COMPLETED` and zero counts. Log a note that initialization was missed.

---

## Review File Contract (Plan H)

This section defines the canonical schema and emission rules for `<ModuleName>_review.md`. Every pipeline stage that produces a Class 2 (🟡) or Class 3 (🔵) event MUST emit an entry to the review file using this format. Class 1 (🔴) events do not appear here — they HALT the pipeline.

### File location

Same directory as the source storyboard. Filename: `<ModuleName>_review.md` (where `<ModuleName>` is the frontmatter `module:` field with whitespace stripped).

### Lifecycle

| Stage | Action |
|---|---|
| `interpreting-storyboard-specs` Step 0.5 | **Initialize** — create the file with the standard header (see template below) and empty 🟡/🔵 sections. If a stale review.md exists from a prior run, rename it to `<ModuleName>_review_<timestamp>.md` first. |
| Every pipeline stage | **Append** — when a Class 2 / Class 3 event occurs, append a structured entry under the appropriate section and increment the running count. |
| `vrse-module-pipeline` Step 9e | **Finalize** — replace the placeholder header lines (`Build finished`, `Status`) and Summary block with final counts; output a one-line summary to the user. |

### Template

```markdown
# Build Review — <ModuleName>

**Source storyboard:** `<full path to storyboard>`
**Build started:** <ISO 8601 timestamp from Step 0.5>
**Build finished:** <ISO 8601 timestamp from Step 9e>
**Status:** ✅ COMPLETED WITH N REVIEW ITEMS  |  ⚠️ COMPLETED WITH WARNINGS  |  ❌ HALTED AT <stage>

## Summary
- 🔴 0 hard failures (build halted) — _(or "build halted at <stage>" if a Class 1 fired)_
- 🟡 <count> review items (recommended fixes — open in Unity)
- 🔵 <count> informational notes (defaults applied; audit if anything looks wrong)

---

## 🟡 Review items

### R1 — <short title> (<stage>)
- **Location:** <where in the source — storyboard line, moment N, etc.>
- **Issue:** <one-line description of the soft failure>
- **Placeholder:** <what the pipeline did instead — e.g. picked first match, used wrapper as highlight target>
- **Alternatives:** <list of other choices the pipeline could have made, if applicable>
- **Fix:** <what the user should do post-build — edit storyboard, fix in Unity, etc.>

### R2 — ...

---

## 🔵 Informational notes

### N1 — <short title> (<stage>)
- **Location:** <where>
- **Default applied:** <what the pipeline used as a default>
- **Action:** <what the user should do if the default is wrong>

### N2 — ...
```

### Append rules

When a stage emits a Class 2 (🟡) entry:

1. Generate the next sequential `R<N>` ID by counting existing 🟡 entries + 1.
2. Append the entry under `## 🟡 Review items` (NOT at the top — preserve chronological order).
3. The entry MUST contain all five fields: Location, Issue, Placeholder, Alternatives (or "None"), Fix.
4. Do not modify other entries — append-only.

When a stage emits a Class 3 (🔵) entry:

1. Generate the next sequential `N<N>` ID by counting existing 🔵 entries + 1.
2. Append the entry under `## 🔵 Informational notes`.
3. The entry MUST contain three fields: Location, Default applied, Action.

### Severity tier definitions (canonical)

| Tier | Icon | Definition | Pipeline behavior |
|---|---|---|---|
| **Class 1** | 🔴 | Irrecoverable: would corrupt state, lose data, or write wrong file | **HALT** — fix input and retry |
| **Class 2** | 🟡 | Recoverable in Unity: build can produce a placeholder; user fixes in editor | **WARN + placeholder** — append review.md entry, continue build |
| **Class 3** | 🔵 | Informational: a default was applied, no real failure | **NOTE** — append review.md entry, continue build |

### Worked example

For a successful build of `BGS Training` with two Class 2 events (one ambiguous source, one auto-balanced lifecycle) and two Class 3 events (animation clip placeholder + position fallback), the finalized review.md looks like:

```markdown
# Build Review — BGS Training

**Source storyboard:** `Assets/Storyboards/BGS Training.md`
**Build started:** 2026-04-26T14:32:11+05:30
**Build finished:** 2026-04-26T14:48:53+05:30
**Status:** ⚠️ COMPLETED WITH WARNINGS

## Summary
- 🔴 0 hard failures (build halted)
- 🟡 2 review items (recommended fixes — open in Unity)
- 🔵 2 informational notes (defaults applied; audit if anything looks wrong)

---

## 🟡 Review items

### R1 — Ambiguous source for `BananaCover` (Stage 0)
- **Location:** Storyboard `## Objects` line declaring `[source: BananaCover]`
- **Issue:** `BananaCover` matched 2 art-scene objects under different parents
- **Placeholder:** Picked `Detector/BananaCover` (lexicographic first)
- **Alternatives:** `LeftWing/BananaCover`
- **Fix:** Add `[source_parent: Detector]` to the storyboard, OR delete the unused art object, OR confirm the picked one is correct.

### R2 — Lifecycle auto-balanced for `Trolley` (Step 7)
- **Location:** Story JSON
- **Issue:** `Trolley` referenced in triggers but missing Spawn
- **Placeholder:** Inserted `Objects.Spawn` in Chapter 1, Moment 0 onAwake
- **Alternatives:** None — this is auto-fix; user can move the Spawn to a different moment if the chosen placement is wrong
- **Fix:** Confirm Chapter 1 Moment 0 onAwake is the correct spawn point for `Trolley`. If the trolley should appear later, move the Spawn manually.

---

## 🔵 Informational notes

### N1 — Animation clip placeholder for Moment 1 (parse-sop)
- **Location:** Storyboard line 136, Moment 1 OnRight Trigger 2
- **Default applied:** Clip name `ScrewRemove_3mm` (inferred from tool size)
- **Action:** Confirm the clip exists in the project, or rename to a real clip name in the storyboard.

### N2 — Position fallback for `ControlMonitors` (Step 4.5)
- **Location:** Stage 4.5 spatial placement
- **Default applied:** `(0, 1, 1.5)` — no `[at:]` hint or explicit `[position:]`
- **Action:** Reposition in editor if wrong.
```

### Author workflow

1. Build runs end-to-end (or HALTs at Class 1 — rare).
2. User opens `<ModuleName>_review.md` in their editor.
3. User opens Unity, plays the module, and uses the review file as a checklist:
   - 🟡 items → open the storyboard or the dev scene, fix, re-run pipeline if structural change required.
   - 🔵 items → audit; fix only if the default is wrong.
4. User signs off when both lists are resolved.

### Why this matters

This review file is the framework's primary mechanism for **converting silent failures into auditable decisions**. Every soft inference the pipeline makes is logged with attribution and an explicit fix path. The author never needs to ask "why did the pipeline do X?" — the answer is in review.md, and the fix is documented next to the issue.

---

## YAML Schema (quick reference)

Key fields: `module` (name, project, scene_template, hierarchy, variants), `objects[]` (name, type, source_object, vrse_name, source_parent, prefab, position, spatial_hint, shared, embedded_in, properties), `story.chapters[].moments[]` (on_awake, on_start, on_right, on_wrong, warnings, on_end).

Pipeline-specific fields not in the base schema:
- `embedded_in: "ParentObjectName"` — object lives inside a converted parent's hierarchy (NOT duplicated from art). Converter produces `ParentName/Mesh/ParentName_Mesh/...`; after parent conversion, `AddGOQToEmbeddedChild(parent, name)` handles this.
- `source_parent: "ParentName"` — disambiguate when art scene has multiple objects with same `source_object` name under different parents.

**Full schema with shorthands, expansion rules, and examples:** `{{SKILLS_HOME}}/writing-vrse-module-specs/SKILL.md`

## Object Recipes

Full MCP call sequences for every object type (grabbable, placepoint, touchable, simple, etc.): `{{SKILLS_HOME}}/setting-up-vrse-scenes/object-recipes.md`
BuildingBlocks prefab catalog: `{{SKILLS_HOME}}/setting-up-vrse-scenes/building-blocks-catalog.md`

Key reminders:
- PlacePoint names **must end with `_PP`** for `Sync PP Transforms` auto-matching
- Run `Sync PP Transforms` after ALL placepoints are created (mandatory)
- For shared objects: use `"QueryObjects"` as parent (not a chapter container)

## Story JSON Reference

### Generator Script

All Story JSON generation goes through `Assets/Editor/build_story.py` (run via `python <path>`). The script is project-agnostic — it reads `BuildContext.json`, `LastGOQIds.json`, and `build_moments.json`, then emits the Story JSON to `scenePaths.storyJson`.

The script's translation tables (`ACTION_EMITTERS`, `TRIGGER_EMITTERS`) mirror `templates/skeleton-guide.md`. To add a new keyword, follow the **HALT-or-extend protocol** in Step 6.

### Format rules (enforced by `build_story.py`)
- `Type: 0` = Action, `Type: 1` = Trigger
- `studio: {"id": ""}` on every chapter and moment
- All action/trigger `ID` fields = `-1`; runtime resolves by `Query`. Numeric IDs are embedded only in `Teleport.targetTransform`, `PlacePointTrigger.grabbableName`, `Timer.Query`, and `SFX.Query` (via `Name#$<ID>`).
- **Never include** `targetGameObject` — runtime-only field
- `onWrong` is a bare array `[]`, not `{"actions": []}`

### Templates
Reference templates: `{{SKILLS_HOME}}/vrse-module-pipeline/templates/` (skeleton + skeleton-guide.md). These are also embedded in `BuildContext.json` at session start.

## Deep Reference (read ONLY when needed)
- Story schema + structure skeleton: `{{SKILLS_HOME}}/creating-vrse-story-json/story-schema.md`
- Action catalog (30 types): `{{SKILLS_HOME}}/creating-vrse-story-json/action-catalog.md`
- Trigger catalog (15 types): `{{SKILLS_HOME}}/creating-vrse-story-json/trigger-catalog.md`
- Moment templates (9 types): `{{SKILLS_HOME}}/creating-vrse-story-json/moment-templates.md`
- Production patterns (15): `{{SKILLS_HOME}}/vrse-module-pipeline/patterns.md`
- YAML spec examples: `{{SKILLS_HOME}}/writing-vrse-module-specs/examples/`
