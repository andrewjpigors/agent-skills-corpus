---
name: umaterial-agent
description: UE material agent skill. Uses UE capability profiles plus a small overlay to write JSON Material IR, validate it offline and through UE, then iterate on rendered previews. UE4.23 is the supported profile; other profiles require live bootstrap and smoke verification.
---

# UMaterialAgent Skill

You convert user material requests into a confirmed material contract and then
into a UE material graph described by a tiny JSON IR. The workflow uses
UE-probed capability data where possible, runs offline validation, uses a live
UE shader gate through a headless commandlet or editor session, previews the
material visually, and imports the final persistent asset.

Every material request starts with a confirmed material contract. This applies
to simple materials too. Before writing IR, running validators, importing into
UE, or rendering previews, translate the user's prompt into a concrete contract
and ask the user to confirm it. Do not proceed to generation until the user
confirms or edits that contract.

The contract must include:

- Material mode: domain, blend mode, shading model, preview renderer, geometry,
  and whether animation/time samples are needed.
- Visible goals: color palette, shape language, surface finish, transparency,
  glow, masks, motion, and any reference style implied by the prompt.
- Detailed acceptance criteria: specific observable checks the preview must
  satisfy.
- Rejection criteria: failure modes that are easy for LLMs to miss, such as
  triangle patterns when the user asked for hexagons, a broad glow band when the
  user asked for a narrow scan band, UV seams, wrong opacity, or missing
  sparkles.
- User confirmation question: ask whether this contract is the target before
  producing IR.

For ongoing revisions after a preview, update the contract whenever the user
changes the visual target, then confirm the changed contract before another IR
revision. Parameter-only tuning may reuse the existing confirmed contract.

All tool execution happens through the agent's shell tool: each domain operation is a standalone Python script in this skill's `scripts/` directory. The scripts print a single JSON result object to stdout:

```json
{"ok": true, "title": "UE validation passed", "output": "...", "metadata": {"path": "/Game/Materials/M_Foo", "compile_gate": {"waited_for_async_shaders": true}}}
```

Read this JSON after every shell call; `ok=false` is the signal to iterate.

## 1. The IR at a glance

```json
{
  "settings": {"domain": "Surface", "blend": "Opaque", "shading": "DefaultLit"},
  "nodes": [
    {"id": "tint",   "type": "Color", "rgba": [0.15, 0.05, 0.25, 1.0]},
    {"id": "noise",  "type": "Noise"},
    {"id": "mix",    "type": "Add"},
    {"id": "rimExp", "type": "ScalarParameter", "name": "RimExp", "default": 3.0},
    {"id": "rim",    "type": "Fresnel"}
  ],
  "edges": [
    {"from": "tint",   "to": "mix.A"},
    {"from": "noise",  "to": "mix.B"},
    {"from": "rimExp", "to": "rim.ExponentIn"}
  ],
  "output": {
    "BaseColor": {"from": "mix"},
    "EmissiveColor": {"from": "rim"},
    "Roughness": {"const": 0.5},
    "Metallic":  {"const": 0.0},
    "Normal":    {"const": [0, 0, 1]}
  }
}
```

**Three hard rules.** Memorize them — every failure mode is a violation of one of these.

### Rule 1 · One canonical shape per node type

Each node type uses the single value shape shown below.

| Type | Required shape |
|---|---|
| `Scalar` | `{"id": "...", "type": "Scalar", "value": 0.5}` |
| `Vec2` | `{"id": "...", "type": "Vec2", "value": [0.1, 0.2]}` |
| `Color` | `{"id": "...", "type": "Color", "rgba": [r, g, b, a]}` — **exactly 4 numbers**, alpha usually 1.0 |
| `Vec4` | `{"id": "...", "type": "Vec4", "value": [x, y, z, w]}` |
| `ScalarParameter` | `{"id": "...", "type": "ScalarParameter", "name": "Foo", "default": 3.0}` |
| `VectorParameter` | `{"id": "...", "type": "VectorParameter", "name": "Foo", "default": [r, g, b, a]}` |
| `StaticBoolParameter` | `{"id": "...", "type": "StaticBoolParameter", "name": "Foo", "default": false}` |

Any other node (Noise, Add, Fresnel, Panner, etc.) takes `id` + `type` plus its own property fields (e.g. `Panner.SpeedX`). Put graph wiring in `edges`.

**Optional `desc` field — strongly recommended.** Every node accepts an optional `desc: "..."` string. The compiler maps it to `UMaterialExpression.Desc`, which the UE Material Editor renders as a yellow comment block above the node. Adding a one-line `desc` per node makes the imported graph self-documenting. Example:

```json
{"id": "fbm_noise",  "type": "Custom", "code": "...",
 "input_names": ["UV"], "output_type": "Float1",
 "desc": "FBM noise (4 octaves, lacunarity 2, gain 0.5) for the dissolve mask"}
```

Custom nodes additionally accept `description: "..."` which sets the node's TITLE shown inside its blue header (e.g. "Stars sparkle"). `desc` and `description` are both useful — `description` is short, `desc` is the longer comment.

### Rule 2 · Every connection lives in `edges`

```json
"edges": [
  {"from": "noise", "to": "mix.A"},
  {"from": "tint.RGB", "to": "mix.B"}
]
```

- **`from`** = `"node_id"` for the node's default output, `"node_id.CHANNELS"` for a channel swizzle, or `{"node": "node_id", "output": "NamedOutput", "channels": "RGB"}` for a named UE output. The `channels` key is optional and the compiler auto-inserts a ComponentMask for swizzles.
- **`to`** = `"node_id.PinName"` — dotted target syntax naming one specific input pin.

Every node you declare **must** be on a forward path to at least one output pin via edges. "Declared but never connected" is an error.

Named-output source refs are supported anywhere a `from` value appears:

```json
{"from": {"node": "break_attrs", "output": "BaseColor", "channels": "RGB"}}
```

Use this for `BreakMaterialAttributes`, material functions, plugin expressions, and any UE expression with multiple named outputs.

### Rule 3 · `output` maps pins to either `{from}` or `{const}`

- `{"from": "node_id"}` wires a pin to a node's default output. Supports channel swizzle: `{"from": "mix.RGB"}`.
- `{"from": {"node": "break_attrs", "output": "BaseColor"}}` wires a named UE output.
- `{"const": <number | list>}` — inline literal. The compiler auto-generates a Scalar/Vec2/Color/Vec4 node and wires it.
- **Exactly one** of `from` or `const` per pin.

## 2. Settings: required blend + shading combinations

- `domain`: `Surface` (nearly always) / `PostProcess` / `DeferredDecal` / `LightFunction` / `UI`.
- `blend`: `Opaque` / `Masked` / `Translucent` / `Additive` / `Modulate` / `AlphaComposite` / `AlphaHoldout`.
- `shading`: `Unlit` / `DefaultLit` / `Subsurface` / `PreintegratedSkin` / `ClearCoat` / `SubsurfaceProfile` / `TwoSidedFoliage` / `Hair` / `Cloth` / `Eye` / `FromMaterialExpression`.

**Required output pins per blend + shading:**

| Configuration | Required outputs |
|---|---|
| DefaultLit + Opaque | `BaseColor` |
| DefaultLit + Masked | `BaseColor`, `OpacityMask` |
| DefaultLit + Translucent | `BaseColor`, `Opacity` |
| Unlit + anything | `EmissiveColor` |
| Additive (any shading) | `EmissiveColor` |
| Cloth / Subsurface | `BaseColor`, `SubsurfaceColor` |
| ClearCoat / Hair / Eye | `BaseColor` |

### 2a. Optional material-asset-level settings

Beyond `domain` / `shading` / `blend` you can also set any of these keys inside `settings`. They map to UMaterial UPROPERTYs (the Details-panel knobs the Material Editor exposes), and **leaving them out preserves UE's defaults** — so every existing IR keeps working. Set the ones you need; ir_compiler hard-rejects unknown keys (typo-safe).

**The four that flip "looks wrong" → "looks right" most often:**

| Key | Type | Default | Use it when |
|---|---|---|---|
| `translucency_lighting_mode` | enum | `VolumetricNonDirectional` | Translucent material looks foggy / flat / diffuse-only. Set to `Surface` (cheap, vertex-rate) or `SurfacePerPixelLighting` (per-pixel, more expensive) for glass / water / plastic / windows. **Almost always wrong by default.** |
| `opacity_mask_clip_value` | float ≥ 0 | `0.333` | Masked material mostly disappears or has hard ugly edges. Lower it (e.g. `0.1`) for noise-driven masks; raise it (`0.5`) for cleaner cutouts. |
| `two_sided` | bool | `false` | Foliage / leaves / glass cards / hair sheets / paper / cloth — anything visible from both sides. |
| `refraction_mode` | enum | `IndexOfRefraction` | Glass / water / crystal with a `Refraction` output pin: `IndexOfRefraction` (physical, scalar input = IOR) vs `PixelNormalOffset` (input treated as screen offset, screen-space distortion). |

**Other transparency knobs (all only effective when `blend` is translucent):**

| Key | Type | Default | Notes |
|---|---|---|---|
| `refraction_depth_bias` | float | `0.0` | Push refraction sampling deeper to reduce edge bleed. |
| `screen_space_reflections` | bool | `false` | Enable SSR on translucents (glass with reflective surroundings). |
| `disable_depth_test` | bool | `false` | UI / overlay style — always render on top. |
| `enable_responsive_aa` | bool | `false` | Suppress TAA history on this pass (kills ghosting at the cost of edge noise). |
| `use_translucency_vertex_fog` | bool | `true` | Disable for emissive particles that should ignore fog. |
| `translucency_directional_lighting_intensity` | float ≥ 0 | `1.0` | Strength of directional light contribution in `Surface*` translucency modes. |
| `dithered_lod_transition` | bool | `false` | Dither across LOD swaps instead of alpha-blend. |
| `write_only_alpha_channel` | bool | `false` | **Required** for `AlphaHoldout` to actually do anything. |
| `enable_separate_translucency` | bool | `true` | UE "Render After DOF". ir_compiler auto-sets this to `false` for `blend=Modulate` because UE4.23 rejects Modulate after-DOF translucency. |
| `cast_dynamic_shadow_as_masked` | bool | `false` | Translucent/Masked shadow casting. |

**Non-transparency settings the IR now also exposes:**

| Key | Type | Default | Notes |
|---|---|---|---|
| `num_customized_uvs` | int 0..8 | `0` | Auto-derived from the highest `CustomizedUV<N>` pin you wire. Override only if you want to expose more than you wire. |
| `use_material_attributes` | bool | `false` | Switch the master input to a single `MaterialAttributes` struct pin (for `MakeMaterialAttributes` / `SetMaterialAttributes` chains). |
| `subsurface_profile_path` | asset path | `""` | Required with `shading=SubsurfaceProfile`; must reference an existing `/Game/...` or `/Engine/...` `USubsurfaceProfile` asset. |
| `fully_rough` | bool | `false` | Mobile perf — skip specular BRDF. |
| `allow_negative_emissive_color` | bool | `false` | Permit `EmissiveColor < 0` (darkening effects). UE4.23 only allows this on `shading=Unlit`; ir_compiler rejects lit combinations offline. |
| `tessellation_mode` | enum | `NoTessellation` | Surface domain only. `NoTessellation` / `FlatTessellation` / `PNTriangles`. `WorldDisplacement` / `TessellationMultiplier` take effect with `FlatTessellation` or `PNTriangles`. |
| `enable_crack_free_displacement` | bool | `false` | Tessellation: smooth UV-seam cracks. |
| `enable_adaptive_tessellation` | bool | `true` | Tessellation: scale density by screen size. |
| `max_displacement` | float ≥ 0 | `0.0` | Tessellation: clamp displacement magnitude. `0` = unclamped. |

Enum values are case-insensitive and the `TLM_` / `RM_` / `MTM_` prefix is optional — `"Surface"` and `"TLM_Surface"` both resolve to `unreal.TranslucencyLightingMode.TLM_SURFACE`.

**Glass material example (the four critical settings + the rest as defaults):**

```json
"settings": {
  "domain": "Surface",
  "blend": "Translucent",
  "shading": "DefaultLit",
  "translucency_lighting_mode": "SurfacePerPixelLighting",
  "two_sided": false,
  "refraction_mode": "IndexOfRefraction",
  "screen_space_reflections": true
}
```

**Foliage / leaf example:**

```json
"settings": {
  "domain": "Surface",
  "blend": "Masked",
  "shading": "TwoSidedFoliage",
  "two_sided": true,
  "opacity_mask_clip_value": 0.4
}
```

## 3. Node-type catalog

The supported UE4.23 capability manifest lives at
**`lib/generated/ue_4_23_capabilities.json`**. Other engine profiles use the
same naming pattern, such as `lib/generated/ue_5_3_capabilities.json`, and can
be selected with `UMA_ENGINE_PROFILE`, `UMA_CAPABILITY_MANIFEST`, or the
scripts' `--profile` / `--manifest` options. A manifest combines live UE
reflection/probe facts with the small human overlay for IR aliases, convenience
properties, and offline diagnostics. The generated docs in
**`references/node-reference.md`**, **`references/material-system-overview.md`**,
and **`references/toolchain-smoke-matrix.md`** are derived from that manifest.

When you need to know which pins/properties a native UE class exposes, trust the
manifest and the live UE compiler. When you need the agent-friendly IR spelling
for common nodes, use the overlay node entries in `node-reference.md`.

High-level node families (names to search for in `references/node-reference.md`):

- **Constants / Parameters** — `Scalar`, `Vec2`, `Color`, `Vec4`, `ScalarParameter`, `VectorParameter`, `StaticBoolParameter`, `StaticSwitchParameter`
- **Source / input** — `Time`, `DeltaTime`, `TextureCoordinate`, `WorldPosition`, `VertexNormalWS`, `PixelNormalWS`, `CameraPositionWS`, `CameraVectorWS`, `ReflectionVectorWS`, `VertexColor`, `PixelDepth`, `SceneDepth`, `LightVector`, `ObjectPositionWS`, `ObjectBounds`, `ObjectRadius`, `ParticleColor`, `ParticleRadius`, `ActorPositionWS`, `AtmosphericFogColor`, `AtmosphericLightVector`, …
- **Math binary** (pins `A`, `B`) — `Add`, `Subtract`, `Multiply`, `Divide`, `Power`, `Min`, `Max`, `Fmod`, `Distance`, `DotProduct`, `CrossProduct`
- **Math unary** (pin `Input` or `VectorInput`) — `Abs`, `Floor`, `Ceil`, `Frac`, `Sqrt`, `OneMinus`, `Sign`, `Saturate`, `Round`, `Truncate`, `Normalize`, `Sine`, `Cosine`, `Tangent`, `Arcsine`, `Arccosine`, `Arctangent`, `DeriveNormalZ`
- **Interpolation / comparison** — `Lerp`, `Clamp`, `If`
- **Vector ops** — `ComponentMask`, `Append`
- **Procedural / animation** — `Noise`, `VectorNoise`, `Fresnel`, `Panner`, `Rotator`, `BumpOffset`, `DepthFade`, `SphereMask`
- **Custom HLSL** — `Custom` (see section 6)
- **Texture sampling** — `TextureSample`, `TextureSampleParameter2D`, `TextureObject`, `TextureObjectParameter` (`TexturePath` prop → `/Game/...` asset)
- **Switches** — `StaticSwitch`, `QualitySwitch`, `FeatureLevelSwitch`, `ShadingPathSwitch`, `RayTracingQualitySwitch`, `PreviousFrameSwitch`, `VirtualTextureFeatureSwitch`
- **Material attribute layers** — `MakeMaterialAttributes`, `BreakMaterialAttributes`, `BlendMaterialAttributes`, `SetMaterialAttributes`, `GetMaterialAttributes`. Pair with `output.MaterialAttributes = {"from": "..."}` to feed the master material's single attrs input (ir_compiler auto-flips `settings.use_material_attributes=true`).
- **Additional profile nodes** —
  - `ShadingModel` (per-pixel shading-model selection when `shading=FromMaterialExpression`)
  - `Transform` (vector coordinate transform — pairs with `TransformPosition`)
  - `Reroute` (visual passthrough; helps keep large graphs tidy)
  - `ChannelMaskParameter`, `CurveAtlasRowParameter`, `CollectionParameter`, `DynamicParameter` (4 more parameter types covering channel masks, gradient curves, MaterialParameterCollection globals, and particle dynamic params)
  - `EyeAdaptation`, `DepthOfFieldFunction`, `TextureProperty` (read post-process / texture metadata)
  - `TextureSampleParameterCube` / `TextureSampleParameterVolume` / `TextureSampleParameterSubUV` (cube / volume / sub-UV variants of `TextureSampleParameter2D`)
  - `FontSample` / `FontSampleParameter` (sample a UFont — for dynamic text materials)
  - `MaterialFunctionCall` (call any `UMaterialFunction` asset — pass `FunctionPath` and wire inputs by name; the IR bypasses the static pin-name check since the function's inputs are dynamic)
  - `RuntimeVirtualTextureSample` / `RuntimeVirtualTextureOutput` (read / write a `URuntimeVirtualTexture` — landscape / world materials)
  - `DecalDerivative` / `DecalLifetimeOpacity` / `DecalMipmapLevel` (DeferredDecal domain helpers — auto-rejected outside that domain)

For native nodes beyond `node-reference.md`, use `UEExpression`. UE compiler
errors identify project-specific class, asset, or context requirements.

Raw native UE nodes are supported through `UEExpression` for classes outside
the strong typed registry:

```json
{
  "id": "native_node",
  "type": "UEExpression",
  "class": "MaterialExpressionSomePluginNode",
  "properties": {"SomeProperty": 1.0},
  "output_type": "any"
}
```

Use this for plugin nodes and UE expression classes that must be preserved
directly. Wiring still belongs in `edges` and `output`, including named-output
source refs.

## 4. Available output pins

Standard PBR: `BaseColor`, `EmissiveColor`, `Metallic`, `Specular`, `Roughness`, `Normal`, `Opacity`, `OpacityMask`, `AmbientOcclusion`, `Refraction`, `SubsurfaceColor`.

Geometric / animation: `WorldPositionOffset` (vertex offsets), `WorldDisplacement` (tessellation), `TessellationMultiplier`, `PixelDepthOffset`.

Shading-model-specific: `CustomData0`, `CustomData1` (ClearCoat, Subsurface), `ShadingModel` (per-pixel selection with `FromMaterialExpression`).

Per-vertex UVs: `CustomizedUV0`..`CustomizedUV7`.

**MaterialAttributes pipeline:** `MaterialAttributes`. Wire a `MakeMaterialAttributes` / `SetMaterialAttributes` / `BlendMaterialAttributes` / `MaterialFunctionCall`-that-returns-attrs node to this pin and ir_compiler auto-flips `settings.use_material_attributes=true`. For visible Make/Set/Blend chains, the compiler checks the required attrs inside the struct: DefaultLit needs `BaseColor`, translucent blends need `Opacity`, masked blends need `OpacityMask`, and subsurface-style models need `SubsurfaceColor`. Dynamic attrs sources such as material functions and raw `UEExpression` nodes are marked for live UE validation.

## 5. Writing a material — worked example

User asks for: "a deep-purple material that pulses between dark and bright tints over time, with a pink Fresnel rim".

```json
{
  "settings": {"domain": "Surface", "blend": "Opaque", "shading": "DefaultLit"},
  "nodes": [
    {"id": "dark",      "type": "Color", "rgba": [0.15, 0.05, 0.25, 1.0]},
    {"id": "bright",    "type": "Color", "rgba": [0.55, 0.25, 0.75, 1.0]},
    {"id": "rim_color", "type": "Color", "rgba": [1.0,  0.45, 0.70, 1.0]},
    {"id": "t",         "type": "Time"},
    {"id": "pulse_raw", "type": "Sine"},
    {"id": "half",      "type": "Scalar", "value": 0.5},
    {"id": "pulse_01",  "type": "Add"},
    {"id": "body",      "type": "Lerp"},
    {"id": "rim_exp",   "type": "ScalarParameter", "name": "RimExp", "default": 3.0},
    {"id": "rim",       "type": "Fresnel"},
    {"id": "rim_out",   "type": "Multiply"},
    {"id": "final",     "type": "Add"}
  ],
  "edges": [
    {"from": "t",         "to": "pulse_raw.Input"},
    {"from": "pulse_raw", "to": "pulse_01.A"},
    {"from": "half",      "to": "pulse_01.B"},
    {"from": "dark",      "to": "body.A"},
    {"from": "bright",    "to": "body.B"},
    {"from": "pulse_01",  "to": "body.Alpha"},
    {"from": "rim_exp",   "to": "rim.ExponentIn"},
    {"from": "rim_color", "to": "rim_out.A"},
    {"from": "rim",       "to": "rim_out.B"},
    {"from": "body",      "to": "final.A"},
    {"from": "rim_out",   "to": "final.B"}
  ],
  "output": {
    "BaseColor": {"from": "final"},
    "Roughness": {"const": 0.4},
    "Metallic":  {"const": 0.0},
    "Normal":    {"const": [0, 0, 1]}
  }
}
```

Every feature the user asked for is on a forward path to an output pin. If you declare a node and forget to connect it, validation fails with the orphan list.

## 6. Custom HLSL nodes

```json
{
  "id": "stars",
  "type": "Custom",
  "code": "#define HASH(p) frac(sin(dot(p, float2(127.1, 311.7))) * 43758.5453)\nfloat2 uv = UV * 40.0;\nfloat2 id = floor(uv);\nfloat rnd = HASH(id);\nfloat2 cell = frac(uv) - 0.5;\nfloat d = length(cell);\nfloat star = smoothstep(0.1, 0.0, d) * step(0.98, rnd);\nreturn float3(star, star, star);",
  "output_type": "Float3",
  "input_names": ["UV"]
}
```

Required fields: `id`, `type: "Custom"`, `code`, `output_type` (`Float1` / `Float2` / `Float3` / `Float4`), `input_names` (list of HLSL variable names referenced — each must also appear as a `to: "stars.<name>"` target in edges).

**HLSL rules inside Custom:**
- The code runs inside an implicit function body. Use statement-level code or a single expression body; omit function declarations and `#include`.
- Statement bodies must explicitly return a value. Expression-only bodies are wrapped by the offline preflight as `return <expr>;`.
- `#define` macros are auto-prefixed per-node so two Custom nodes can share macro names.

Wire the Custom's inputs via edges: `{"from": "tc", "to": "stars.UV"}`.

## 7. How to invoke the scripts

All commands run from the skill directory or with paths adjusted from the repo root. Every script prints one JSON result object. Read it after each call; `ok=false` means revise before continuing.

### Project setup

Before import or preview, install the UMaterialAgent bridge into the UE project:

```powershell
python scripts/setup_ue_project.py --project D:\Path\Project.uproject --engine-root D:\UE_4.23 --force
python scripts/start_ue_editor.py --project D:\Path\Project.uproject --engine-root D:\UE_4.23 --close-existing --wait-for-bridge
```

The bridge provides root pins, native expression creation, reverse graph export, thumbnail preview support, and async shader-queue waiting: `CustomData0`, `CustomData1`, `CustomizedUV0..7`, `ShadingModel`, `MaterialAttributes`, `WorldDisplacement`, `TessellationMultiplier`, and `PixelDepthOffset`. `setup_ue_project.py` also creates the local auth token used by editor-backed scripts, copies the generated capability manifest into the project, and prints bootstrap/bridge/manifest hashes. Start or restart UE with `start_ue_editor.py`; it can close an old editor session, disables UE's autosave package-recovery prompt before launch, and waits for the bridge, so the modal "Restore Packages" window does not block the workflow. Host scripts check `/api/status` before posting jobs; when the editor has stale project-local files, rerun setup and start UE again with `start_ue_editor.py --close-existing`.

To bring up or refresh a whole project/profile, prefer:

```powershell
python scripts/bootstrap_engine_profile.py --project D:\Path\Project.uproject --engine-root D:\UE_4.23 --start-editor --close-existing --smoke
```

### One material per task

A finished task is one imported material named exactly what the user asked for. Keep revisions on that same asset path:

- parameter value change: use `tweak_params.py`;
- compare candidate parameter values: use `preview_sweep.py`;
- graph structure change: use `patch_material.py` or revise the IR and re-import with `--overwrite-existing`.

### Required workflow

1. Draft the material contract from the user's prompt, including detailed
   acceptance and rejection criteria. Ask the user to confirm it, even for a
   simple material.
2. After confirmation, save the confirmed contract as the `--spec` text and
   derive `intent.json` bullets from its visible goals.
3. Design the IR and write it to a temp JSON file.
4. Run `validate_material.py` until it returns `ok:true`.
5. Run `validate_material_in_ue.py` for a headless live UE shader gate. The bridge is required; this waits for the async shader compiler queue before reading material compile errors.
6. Run `import_material.py --overwrite-existing` for revisions, or `import_material.py --ue-mode headless --project <uproject> --engine-root D:\UE_4.23 --overwrite-existing` for compiler-only passes before preview.
7. Run `preview_material.py`. Capture the `PREVIEW RUN_ID` from its output. Use `--renderer capture` for a stable scene-capture preview and deterministic Time frames. Use `--renderer thumb` when you need a Content Browser style thumbnail; transparent, glass, emissive, refraction, and reflection-heavy materials can read differently across the two preview environments.
8. Run `review_material.py --run-id <RUN_ID> --intent-json @intent.json --spec @spec.txt`.
9. Dispatch the generated review prompt to a separate Codex or Claude Code reviewer agent. The reviewer must open every listed PNG path and return `VERDICT: SHIP | TUNE | REVISE | BLOCKED`.
10. Act on the verdict: `SHIP` report the asset path; `TUNE` call `tweak_params.py` and re-preview; `REVISE` update the IR and re-import; `BLOCKED` report the blocker.

### Script reference

- `bootstrap_engine_profile.py --project <uproject> --engine-root <UE_ROOT> [--profile auto|ue_5_3] [--start-editor] [--smoke]`: generate/install an engine capability profile for one project.
- `setup_ue_project.py --project <uproject> --engine-root <UE_ROOT> [--profile ue_4_23] [--manifest file.json] [--force]`: install/build the UMaterialAgent bridge and bootstrap the project.
- `start_ue_editor.py --project <uproject> --engine-root <UE_ROOT> [--close-existing] [--wait-for-bridge]`: start UE after optionally closing old editor sessions and disabling the autosave restore prompt.
- `probe_ue_material_system.py [--smoke-create] [--update-cache] [--profile ue_4_23] [--allow-stale-manifest] [--out report.json]`: enumerate live `UMaterialExpression` classes, project metadata, bridge version, and reflection schema.
- `generate_capabilities.py [--profile ue_4_23] [--out lib/generated/<profile>_capabilities.json]`: generate a capability manifest from probe cache plus overlay data.
- `generate_docs_from_capabilities.py [--manifest lib/generated/<profile>_capabilities.json]`: regenerate the capability docs under `references/`.
- `probe_toolchain_smoke.py --project <uproject> --engine-root <UE_ROOT> [--profile ue_4_23] [--out toolchain-smoke.json]`: run throwaway IR cases through offline compile plus live UE import.
- `probe_compile_behavior.py --project <uproject> --engine-root <UE_ROOT> [--out toolchain-smoke.json]`: compatibility wrapper for `probe_toolchain_smoke.py`.
- `probe_ue_oracle_behavior.py --project <uproject> --engine-root <UE_ROOT> [--out ue-oracle.json]`: create native UE nodes directly and sample raw live engine behavior.
- `validate_material.py --material-name NAME --ir-json @file.json`: offline dry run.
- `validate_material_in_ue.py --project <uproject> --engine-root <UE_ROOT> --material-name NAME --ir-json @file.json [--timeout 600]`: run the live UE shader gate through a headless UE commandlet and delete the scratch `.uasset` after success.
- `import_material.py --material-name NAME --ir-json @file.json [--overwrite-existing] [--ue-mode editor|headless --project <uproject> --engine-root <UE_ROOT>] [--timeout 600]`: compile and import `/Game/Materials/<NAME>`.
- `patch_material.py --material-path /Game/Materials/M_Foo --operations-json @ops.json [--timeout 600]`: apply small structural IR edits to the cached material IR.
- `inspect_material.py --material-path /Game/Materials/M_Foo [--timeout 120]`: dump an existing material graph.
- `export_material_ir.py --material-path /Game/Materials/M_Foo [--out out.json] [--timeout 120]`: reverse-export an existing UE material into Material IR, then run the offline compiler checks on the exported IR.
- `preview_material.py --material-path /Game/Materials/M_Foo [--geometry sphere,cube] [--frames N] [--duration SEC] [--times 0,1,2] [--size 192] [--renderer auto|thumb|capture] [--timeout 120]`: render PNG previews.
- `preview_sweep.py --material-path /Game/Materials/M_Foo --parameter-name Param --scalar-values 1,3,5 [--timeout 120]`: render parameter candidates.
- `tweak_params.py --material-path /Game/Materials/M_Foo --scalar-params '{"Param": 3}' --vector-params '{"Tint":[1,0,0,1]}' [--timeout 120]`: create/update a material instance with overrides.
- `validate_custom_hlsl.py --code-file snippet.hlsl --output-type Float3 --input-names UV,Time`: validate a Custom node body.
- `review_material.py --material-name NAME --run-id RUN_ID --intent-json @intent.json --spec @spec.txt`: emit a review prompt pinned to the exact preview run.

### Preview rules

`--renderer auto` inspects the material blend mode. Translucent, Masked, Additive, Modulate, AlphaComposite, and AlphaHoldout route to `thumb` for Content-Browser-faithful translucency. Other blends use `capture`, which supports time-driven previews through an injected preview-time parameter. If you request `thumb` with `--duration` or `--times`, the script errors; choose `capture` for time-driven frames.

`--geometry thumbnail` and `--geometry cylinder` require `thumb` or `auto`. Use `sphere` by default; add `cube` or `plane` only when the effect needs another shape.

### Temp paths on Windows

In Git Bash, prefer `mktemp` for `@file` arguments so Python receives a valid path:

```bash
IR=$(mktemp --suffix=.json)
cat > "$IR" <<'EOF'
{ "settings": {...}, "nodes": [...], "edges": [...], "output": {...} }
EOF
python scripts/validate_material.py --material-name M_Foo --ir-json "@$IR"
```
## 8. Patch operations (patch_material ops schema)

After import, `patch_material` applies small changes to the cached IR.

```
{op: "node_add",    id, type, ...props}
{op: "node_remove", id, on_orphan: "error"|"cascade"|"disconnect", expected_cascades: [...] (required when cascade)}
{op: "node_edit",   id, set: {field: value, ...}}   # id and type are immutable
{op: "edge_add",    from, to}
{op: "edge_remove", from, to}
{op: "output_set",  pin, from: "node_id"}           # or
{op: "output_set",  pin, const: <literal>}
{op: "output_unset", pin}
```

Example — bumping the rim exponent and adding a scan line:

```bash
OPS=$(mktemp --suffix=.json)
cat > "$OPS" <<'EOF'
[
  {"op": "node_edit", "id": "rim_exp", "set": {"default": 5.0}},
  {"op": "node_add", "id": "scan_time", "type": "Time"},
  {"op": "node_add", "id": "scan_wave", "type": "Sine"},
  {"op": "edge_add", "from": "scan_time", "to": "scan_wave.Input"},
  {"op": "edge_add", "from": "scan_wave", "to": "final.B"}
]
EOF
python scripts/patch_material.py --material-path /Game/Materials/M_EnergyShield --operations-json "@$OPS"
```

The patch runs the same orphan + required-output + substantive-source checks as `validate_material`. Failure leaves the cached IR unchanged.

**Cascade semantics** for `node_remove`:
- `on_orphan: "error"` (default): refuse if anything still references the node.
- `on_orphan: "cascade"`: also remove listed dependents. `expected_cascades` must match the actual dependent set exactly, or the op fails (declare-then-verify prevents silent subgraph destruction).
- `on_orphan: "disconnect"`: drop edges/outputs referencing the node but keep dependents — they may then fail the orphan check at compile time.

## 9. Reverse-export existing UE materials

Use `export_material_ir.py` when the starting point is a material already in the UE project:

```bash
python scripts/export_material_ir.py --material-path /Game/Materials/M_Source --out exported.json
python scripts/validate_material.py --material-name M_Source_Exported --ir-json @exported.json
```

The command reads `UMaterial.Expressions` and hidden root pins through the UMaterialAgent bridge, maps known UE expression classes back to overlay IR nodes, preserves unknown classes as `UEExpression`, preserves named outputs with structured source refs, drops disconnected editor-only clutter, and validates the result before reporting success. The exported IR is preservation-oriented: project/plugin-specific dynamic pins, external asset semantics, and some editor-only details still require live UE validation after re-import.

## 10. Common failure modes

- **Wrong known `type` name (case-sensitive)**, missing property, enum value, type mismatch, unknown pin, etc. The validator error echoes the valid options for overlay nodes; use `references/node-reference.md` for those. For native classes beyond the overlay, use `UEExpression` and validate in live UE.
- **Unwired node.** Every declared node needs a forward path through `edges` to an output pin. The validator reports the orphan list.
- **Unknown input name.** Pin names match UE exactly — `A` / `B` / `Alpha` for Lerp, `Input` for Abs/Sine, `ExponentIn` for Fresnel. Validator lists the valid pin names for the target type.
- **Custom node inputs.** If your HLSL references `UV`, include both `"input_names": ["UV"]` and an edge `{"from": <something>, "to": "<custom_id>.UV"}`.
- **Literal values.** Every non-local value comes via edges. Declare a `Scalar` / `Color` / `Vec2` / `Vec4` node for constants.
- **"Material already exists at /Game/..."** on `import_material`. Use `--overwrite-existing` for transactional replacement or `patch_material` for cached-IR updates.

## 11. Reference material

For deeper detail, read the files in this skill's `references/` directory (the `read` tool works on any path):

- `references/node-reference.md` — every node type's output type, input pins with required HLSL types, property defaults, enum valid values, and required-input sets (auto-regenerated from `lib/pin_registry.py` + live-probed `lib/enum_members_ue423.py`).
- `references/shader-patterns.md` — canonical HLSL recipes: hash, noise, FBM, Voronoi, dissolve, Fresnel, smoothstep, domain warping, etc. Use these as templates for complex prompts instead of deriving from scratch.
- `references/hlsl-rules.md` — what's allowed / forbidden inside a Custom node body.
- `references/material-debug.md` — symptom → cause → fix cheat sheet. Grep by keyword when a preview looks wrong (transparent material rendering opaque, gray checker, flat Normal, etc.).






