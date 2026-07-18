---
name: blender-mcp-quality
description: >
  Blender 5.1 MCP quality assurance and best practices for 3D modeling, animation,
  rigging, lighting, and rendering via the blender-mcp MCP server. Use this skill
  whenever working with Blender through MCP tools such as execute_blender_code,
  get_scene_info, get_object_info, get_viewport_screenshot, or any Blender-related
  3D task including modeling, scene creation, material setup, rigging, armatures,
  animation, keyframes, camera paths, lighting, modifiers, or object manipulation.
  This skill enforces geometry validation, polygon budgets, spatial correctness,
  animation best practices, and correct Blender 5.1 Python API usage.
---

# Blender 5.1 MCP Quality Assurance

This skill ensures high-quality 3D output when using the blender-mcp MCP server
with **Blender 5.1**. Follow ALL sections strictly. Do not skip validation steps.

---

## 0. Pre-Modeling Planning (RECOMMENDED)

Before writing any `bpy` code, follow this checklist to avoid aimless primitive
placement and ensure the final result matches the user's intent.

### 0.1 Anatomy inventory

List the major visible parts of the asset before modeling:
- **Primary masses** — body, head, chassis, building shell
- **Connecting parts** — neck, arms, wheels, supports, beams
- **Repeated details** — windows, bolts, buttons, fence segments, stairs
- **Accessories** — antennae, belts, signs, decorative elements

### 0.2 Proportion estimation

Estimate key proportions as ratios derived from the user's description or
reference image. Document at least three ratio estimates before building:

```
Example for a cartoon robot:
- Body height : width  ≈ 1.5 : 1
- Head : body height   ≈ 1 : 2
- Arm length : body height ≈ 1 : 1
- Leg length : body height ≈ 1 : 1.2
```

### 0.3 Build order

Plan construction steps from large to small:
1. **Blockout** — primary masses with simple primitives
2. **Structure** — connecting parts, supports, joints
3. **Detail** — repeated features, accessories, surface detail
4. **Rigging** — armature, bone placement, weight assignment
5. **Animation** — keyframes, constraints, paths
6. **Polish** — materials, lighting, camera, render settings

### 0.4 Single-step discipline

Build only one logical unit per step. After each step:
1. Verify placement using `get_object_info` (bounding box, location)
2. Run the validation script from Section 1
3. Compare the result to the user's description
4. Fix issues before adding the next part

> **Do not** stack multiple unverified parts. If a step produces a warning,
> address it before moving on.

---

## 1. MANDATORY: Post-Creation Validation

After EVERY creation or modification step (adding objects, moving objects, applying
materials, importing models, generating), you MUST run validation via `execute_blender_code`:

```python
import bpy
import bmesh
import mathutils
from mathutils.bvhtree import BVHTree

report = {"errors": [], "warnings": [], "stats": {}}
depsgraph = bpy.context.evaluated_depsgraph_get()

for obj in bpy.context.scene.objects:
    if obj.type != 'MESH':
        continue

    mesh = obj.data

    # 1. Built-in mesh validation (fixes corrupt data)
    had_errors = mesh.validate(verbose=False)
    if had_errors:
        report["errors"].append(f"{obj.name}: mesh.validate() found and repaired invalid geometry")

    # 2. Polygon count check
    poly_count = len(mesh.polygons)
    vert_count = len(mesh.vertices)
    report["stats"][obj.name] = {"polygons": poly_count, "vertices": vert_count}
    if poly_count > 10000:
        report["warnings"].append(f"{obj.name}: {poly_count} polygons — consider Decimate modifier")
    if poly_count > 50000:
        report["errors"].append(f"{obj.name}: {poly_count} polygons — excessively high, must reduce")

    # 3. Non-manifold geometry check (BMVert.is_manifold in Blender 5.1)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    non_manifold_verts = [v for v in bm.verts if not v.is_manifold]
    if non_manifold_verts:
        report["warnings"].append(f"{obj.name}: {len(non_manifold_verts)} non-manifold vertices")

    # 4. Degenerate face check (zero-area faces)
    degenerate = [f for f in bm.faces if f.calc_area() < 1e-6]
    if degenerate:
        report["warnings"].append(f"{obj.name}: {len(degenerate)} zero-area/degenerate faces")

    bm.free()

    # 5. Ground-plane check
    if any(coord != -1.0 for corner in obj.bound_box for coord in corner):
        bbox_corners = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        min_z = min(c.z for c in bbox_corners)
        if min_z < -0.01:
            report["warnings"].append(f"{obj.name}: below ground plane (lowest z={min_z:.3f})")

# 6. Object intersection check (BVH overlap between mesh pairs)
# NOTE: For rigged/parented setups (e.g. wheels on a car, armature rigs),
# overlap between parent-child objects is EXPECTED and should be treated as
# false-positive noise — not real errors. Only flag overlaps between
# unrelated objects.
mesh_objects = [o for o in bpy.context.scene.objects if o.type == 'MESH']
checked = set()
for i, obj_a in enumerate(mesh_objects):
    for j, obj_b in enumerate(mesh_objects):
        if i >= j:
            continue
        # Skip parent-child pairs (overlap is intentional)
        if obj_a.parent == obj_b or obj_b.parent == obj_a:
            continue
        pair_key = (obj_a.name, obj_b.name)
        if pair_key in checked:
            continue
        checked.add(pair_key)
        try:
            bvh_a = BVHTree.FromObject(obj_a, depsgraph)
            bvh_b = BVHTree.FromObject(obj_b, depsgraph)
            overlap = bvh_a.overlap(bvh_b)
            if overlap and len(overlap) > 0:
                report["warnings"].append(
                    f"{obj_a.name} intersects {obj_b.name} ({len(overlap)} overlapping faces)"
                )
        except:
            pass

import json
print("VALIDATION_REPORT:" + json.dumps(report, indent=2))
```

**After running validation:**
- **Errors**: fix immediately before proceeding.
- **Warnings**: evaluate each. Fix spatial issues (below ground, unintended intersections).
  For intentional intersections (e.g., a table leg inside a floor), note and move on.
- Always include polygon stats in your response to the user.

---

## 2. Polygon Budget Guidelines

These are maximum values — prefer lower when possible:

| Object Type | Max Polygons | Primitive Settings |
|---|---|---|
| Background/distant object | 500 | UV Sphere: segments=16, ring_count=8 |
| Standard scene object | 2,000 | UV Sphere: segments=24, ring_count=12 |
| Hero/focal object | 5,000 | UV Sphere: segments=32, ring_count=16 |
| Detailed character | 10,000 | UV Sphere: segments=48, ring_count=24 |
| Ground plane / terrain | 100–400 | Subdivided plane: cuts=10 to cuts=20 |
| Simple furniture | 500–2,000 | Use cubes + loop cuts, not high-poly |
| Tree / organic shape | 3,000–8,000 | Prefer Ico Sphere over UV Sphere for organic |

**Key rules:**
- NEVER use `segments=128` or `ring_count=64` unless user explicitly requests high-poly.
- Default UV Sphere: `segments=32, ring_count=16` (480 faces).
- Default Ico Sphere: `subdivisions=2` (80 faces). Use `subdivisions=3` (320 faces) only
  for hero/focal objects.
- Default Cylinder: `vertices=32`. Use `vertices=16` for background objects.
- Default Cone: `vertices=32`. Use `vertices=16` for background objects.

---

## 3. Correct Blender 5.1 Python API Usage

### 3.1 Always update the view layer after transforms

```python
obj.location = (1, 2, 3)
bpy.context.view_layer.update()
print(obj.matrix_world)  # Now shows correct values
```

Without `view_layer.update()`, `matrix_world` and dependent values are stale.

### 3.2 Always apply transforms before parenting or rigging

```python
bpy.ops.object.select_all(action='DESELECT')
obj.select_set(True)
bpy.context.view_layer.objects.active = obj
bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
```

Failure to apply transforms is the #1 cause of broken rigging and deformed meshes.

### 3.3 Validate mesh after from_pydata() as a safe default

```python
mesh = bpy.data.meshes.new("MyMesh")
mesh.from_pydata(vertices, edges, faces)
mesh.validate(verbose=True)  # Safe default unless the input is already known-good
mesh.update()
```

### 3.4 Use BMesh for topology operations

```python
import bmesh
bm = bmesh.new()
bm.from_mesh(obj.data)
# ... edits ...
bm.to_mesh(obj.data)
bm.free()
obj.data.update()
```

Do NOT loop over `mesh.polygons` for editing — use BMesh.

### 3.5 Mesh access is out-of-sync in Edit Mode

In Blender 5.1, object-mode mesh data can be read in Edit Mode but is out of sync with
the edit mesh. The official gotcha from `info_gotchas_meshes.html` recommends either
using `bmesh.from_edit_mesh()` for edit-mode data or switching to Object Mode to work
with synced mesh data:

```python
if bpy.context.object and bpy.context.object.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
```

When editing in Edit Mode, keep working through the edit BMesh until you explicitly
write/sync changes back. Do not mix unsynced object-mode mesh reads with edit-mesh edits.

### 3.6 Check operator context before calling operators

```python
if bpy.ops.mesh.normals_make_consistent.poll():
    bpy.ops.mesh.normals_make_consistent(inside=False)
```

### 3.7 BVHTree requires evaluated depsgraph

```python
from mathutils.bvhtree import BVHTree
depsgraph = bpy.context.evaluated_depsgraph_get()
bvh = BVHTree.FromObject(obj, depsgraph)
```

### 3.8 calc_normals() was removed

```python
# WRONG — removed in Blender 4.x+
# mesh.calc_normals()

# CORRECT — normals auto-calculated. To recalculate orientation:
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')
```

### 3.9 Prefer direct data access over operators

From Blender's official best practices: avoid `bpy.ops` whenever direct data access
via `bpy.data` is possible. Operators require context setup, are slower, and less
reliable in scripted contexts. Use operators only when no data-level alternative exists
(e.g., `bpy.ops.object.transform_apply`, `bpy.ops.mesh.normals_make_consistent`).

### 3.10 Use "Copy Data Path" to discover API paths

Right-click any property in Blender's UI and select **Copy Data Path** or
**Copy Full Data Path** to get the exact Python expression. This is the most
reliable way to find correct property names — especially for new or renamed
properties in 5.1. Blender's official best practices recommend this approach
over guessing attribute names.

### 3.11 Python threads are not supported

Blender's Python API is **not thread-safe**. All `bpy` operations must run on
the main thread. Do not use `threading` or `concurrent.futures` to parallelize
Blender operations. From the official docs: "Python threads can be used for
non-Blender operations, but accessing `bpy` from any thread other than the
main thread will crash Blender."

This is typically not a concern for MCP-based workflows (each `execute_blender_code`
call runs sequentially), but avoid spawning threads inside your scripts.

### 3.12 Every new object must be linked to a collection

When creating an object programmatically via data, it will not appear in the scene or the viewport until it is linked to a collection. Always link newly created objects explicitly:

```python
# Create mesh and object
mesh_data = bpy.data.meshes.new("MyMesh")
obj = bpy.data.objects.new("MyObject", mesh_data)

# MUST link to a collection to make it visible and renderable
bpy.context.collection.objects.link(obj)
```

---

## 4. Object Placement & Spatial Correctness

### 4.1 Ground snapping

```python
import mathutils
if any(coord != -1.0 for corner in obj.bound_box for coord in corner):
    bbox_corners = [obj.matrix_world @ mathutils.Vector(c) for c in obj.bound_box]
    min_z = min(c.z for c in bbox_corners)
    obj.location.z -= min_z
    bpy.context.view_layer.update()
```

`obj.bound_box` can be unavailable on some objects; Blender uses `-1.0` coordinates in
that case, so guard before using it.

### 4.2 Object spacing

After placing multiple objects, use `get_object_info` to check bounding boxes.
Maintain a minimum gap of 0.01 Blender units between non-touching objects.

### 4.3 Armature joint alignment

When creating armatures, always verify:
- Bone tails connect to the next bone's head (for connected chains)
- The armature root is at the mesh origin or scene origin
- All bones have non-zero length (head != tail)

```python
for bone in armature.data.bones:
    length = (bone.tail - bone.head).length
    if length < 0.001:
        print(f"WARNING: Bone '{bone.name}' has near-zero length!")
```

### 4.4 Contact/gap verification for joined parts

When parts are supposed to physically touch (e.g., a wheel on an axle, a head
on a neck, a post on a base), verify the contact numerically — do not rely on
visual closeness alone. Run this after placing joined parts:

```python
import bpy
import mathutils

def check_contact(obj_a_name, obj_b_name, max_gap=0.02):
    """Verify two objects are within contact tolerance.
    Returns the gap distance between their closest bounding box faces."""
    obj_a = bpy.data.objects.get(obj_a_name)
    obj_b = bpy.data.objects.get(obj_b_name)
    if not obj_a or not obj_b:
        print(f"ERROR: Object not found: {obj_a_name if not obj_a else obj_b_name}")
        return None

    bpy.context.view_layer.update()

    # Get world-space bounding boxes
    bbox_a = [obj_a.matrix_world @ mathutils.Vector(c) for c in obj_a.bound_box]
    bbox_b = [obj_b.matrix_world @ mathutils.Vector(c) for c in obj_b.bound_box]

    # Axis-aligned extents
    min_a = mathutils.Vector((min(c.x for c in bbox_a), min(c.y for c in bbox_a), min(c.z for c in bbox_a)))
    max_a = mathutils.Vector((max(c.x for c in bbox_a), max(c.y for c in bbox_a), max(c.z for c in bbox_a)))
    min_b = mathutils.Vector((min(c.x for c in bbox_b), min(c.y for c in bbox_b), min(c.z for c in bbox_b)))
    max_b = mathutils.Vector((max(c.x for c in bbox_b), max(c.y for c in bbox_b), max(c.z for c in bbox_b)))

    # Per-axis gap (negative = overlap, positive = gap)
    gaps = []
    for axis in range(3):
        gap = max(min_a[axis] - max_b[axis], min_b[axis] - max_a[axis])
        gaps.append(gap)

    max_axis_gap = max(gaps)
    axis_names = ['X', 'Y', 'Z']
    worst = gaps.index(max_axis_gap)

    if max_axis_gap > max_gap:
        print(f"GAP: {obj_a_name} ↔ {obj_b_name}: {max_axis_gap:.4f} gap on {axis_names[worst]} — fix placement")
    elif max_axis_gap > 0:
        print(f"OK: {obj_a_name} ↔ {obj_b_name}: within tolerance (gap={max_axis_gap:.4f})")
    else:
        print(f"OK: {obj_a_name} ↔ {obj_b_name}: overlapping (penetration={abs(max_axis_gap):.4f})")
    return max_axis_gap

# Usage:
# check_contact("Body", "Head", max_gap=0.02)
# check_contact("Wheel_L", "Axle", max_gap=0.01)
```

Use this check for any parts the user expects to be physically connected.
A gap larger than 0.02 Blender units is usually visible and should be fixed.

---

## 5. Materials & Shading

### 5.1 Always use Principled BSDF

Use `ShaderNodeBsdfPrincipled` as the base shader:

```python
mat = bpy.data.materials.new(name="MyMaterial")

# In Blender 5.1, use_nodes is deprecated (always True, setting it is a no-op).
# The material node tree is created automatically upon calling materials.new().
# Access it directly and clear default nodes to build your custom setup.
nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear default nodes and build from scratch
nodes.clear()

# Create Material Output
output = nodes.new('ShaderNodeOutputMaterial')
output.location = (300, 0)

# Create Principled BSDF
principled = nodes.new('ShaderNodeBsdfPrincipled')
principled.location = (0, 0)
principled.inputs["Base Color"].default_value = (0.8, 0.2, 0.2, 1.0)
principled.inputs["Roughness"].default_value = 0.4
principled.inputs["Metallic"].default_value = 0.0

# Link BSDF → Output
links.new(principled.outputs['BSDF'], output.inputs['Surface'])
```

> **Blender 5.1 material node tree warning:**
> `bpy.data.materials.new()` automatically creates a material **with** a default node tree since nodes are always enabled in Blender 5.x.
> The old `mat.use_nodes = True` trick is deprecated and setting it is a no-op.
> Simply access `mat.node_tree` directly, and clear any default nodes using `nodes.clear()` before building your custom node tree.

### 5.2 Color space on textures

- Use the standard Blender color-space names from the active color configuration.
- Color/Diffuse/Albedo: `sRGB`
- Normal maps, roughness, metallic, displacement: `Non-Color`

### 5.3 Assign materials to objects

```python
if obj.data.materials:
    obj.data.materials[0] = mat
else:
    obj.data.materials.append(mat)
```

### 5.4 Flat shading for low-poly / cartoon style

```python
for poly in obj.data.polygons:
    poly.use_smooth = False
# Or for smooth:
for poly in obj.data.polygons:
    poly.use_smooth = True
```

> **Note:** `MeshPolygon.use_smooth` remains functional in Blender 5.1 and is the
> correct direct-data approach for per-face shading control. However, do **not** use
> the removed `mesh.use_auto_smooth` property — it was replaced in Blender 4.1 by
> the **Smooth by Angle** geometry node modifier for angle-based auto-smoothing.
> For simple flat/smooth shading as shown above, the per-polygon approach is still
> the recommended method per Blender's "prefer direct data access" best practice.

---

## 6. Lighting & Camera Setup

### 6.1 Three-point lighting

```python
import bpy
import math

# Key light (main light, slightly above and to the side)
key_light_data = bpy.data.lights.new(name="KeyLight", type='AREA')
key_light_data.energy = 500
key_light_data.size = 3
key_light = bpy.data.objects.new(name="KeyLight", object_data=key_light_data)
bpy.context.collection.objects.link(key_light)
key_light.location = (4, -3, 5)
key_light.rotation_euler = (math.radians(60), 0, math.radians(45))

# Fill light (softer, opposite side)
fill_light_data = bpy.data.lights.new(name="FillLight", type='AREA')
fill_light_data.energy = 200
fill_light_data.size = 5
fill_light = bpy.data.objects.new(name="FillLight", object_data=fill_light_data)
bpy.context.collection.objects.link(fill_light)
fill_light.location = (-4, -2, 3)
fill_light.rotation_euler = (math.radians(50), 0, math.radians(-45))

# Rim/back light
rim_light_data = bpy.data.lights.new(name="RimLight", type='POINT')
rim_light_data.energy = 300
rim_light = bpy.data.objects.new(name="RimLight", object_data=rim_light_data)
bpy.context.collection.objects.link(rim_light)
rim_light.location = (0, 4, 4)
```

### 6.2 Light types in Blender 5.1

| Type | Use case | Key property |
|---|---|---|
| `'POINT'` | Omnidirectional, lamps, candles | `energy`, `shadow_soft_size` |
| `'SUN'` | Outdoor/directional, shadows | `energy`, `angle` |
| `'SPOT'` | Focused beam, stage lights | `energy`, `spot_size`, `spot_blend` |
| `'AREA'` | Soft studio lighting | `energy`, `size`, `shape` |

### 6.3 Camera setup

```python
cam_data = bpy.data.cameras.new(name="Camera")
cam_data.lens = 50  # 50mm focal length (standard)
cam_data.clip_start = 0.1
cam_data.clip_end = 1000

cam = bpy.data.objects.new(name="Camera", object_data=cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (7, -7, 5)

# Point camera at a target
track = cam.constraints.new(type='TRACK_TO')
target = bpy.data.objects.get("MySubject")
if target:
    track.target = target
track.track_axis = 'TRACK_NEGATIVE_Z'
track.up_axis = 'UP_Y'

bpy.context.scene.camera = cam
```

### 6.4 World/environment background

```python
world = bpy.data.worlds.new(name="World")
bpy.context.scene.world = world
bg = world.node_tree.nodes.get("Background")
if bg:
    bg.inputs["Color"].default_value = (0.05, 0.05, 0.08, 1.0)  # Dark blue-gray
    bg.inputs["Strength"].default_value = 1.0
```

In Blender 5.1, worlds already have a node tree. `use_nodes` is a deprecated
compatibility property and does not need to be set.

---

## 7. Modifiers

### 7.1 Adding modifiers via Python

```python
# Subdivision Surface
mod = obj.modifiers.new(name="Subsurf", type='SUBSURF')
mod.levels = 1          # Viewport
mod.render_levels = 2   # Render

# Mirror
mod = obj.modifiers.new(name="Mirror", type='MIRROR')
mod.use_axis = (True, False, False)  # Mirror on X

# Solidify (give thickness to flat surfaces)
mod = obj.modifiers.new(name="Solidify", type='SOLIDIFY')
mod.thickness = 0.02

# Boolean (cut/join shapes)
mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = bpy.data.objects.get("Cutter")

# Decimate (reduce polygon count)
mod = obj.modifiers.new(name="Decimate", type='DECIMATE')
mod.ratio = 0.5  # Keep 50% of faces
```

### 7.2 Applying modifiers

```python
bpy.context.view_layer.objects.active = obj
for mod in obj.modifiers:
    bpy.ops.object.modifier_apply(modifier=mod.name)
```

**Important:** Apply modifiers BEFORE rigging. After applying, always run
`mesh.validate()` to ensure the resulting geometry is clean.

### 7.3 Modifier order matters

Blender applies modifiers top-to-bottom. Common order:
1. Mirror → 2. Subdivision Surface → 3. Solidify → 4. Armature

---

## 8. Armature & Rigging

### 8.1 Creating an armature

```python
import bpy

# Create armature data and object
arm_data = bpy.data.armatures.new("Armature")
arm_obj = bpy.data.objects.new("Armature", arm_data)
bpy.context.collection.objects.link(arm_obj)
bpy.context.view_layer.objects.active = arm_obj

# Enter Edit Mode to add bones
bpy.ops.object.mode_set(mode='EDIT')
edit_bones = arm_data.edit_bones

# Root bone (spine/hips)
root = edit_bones.new("Root")
root.head = (0, 0, 0.8)
root.tail = (0, 0, 1.2)

# Child bone (spine)
spine = edit_bones.new("Spine")
spine.head = root.tail
spine.tail = (0, 0, 1.6)
spine.parent = root
spine.use_connect = True

bpy.ops.object.mode_set(mode='OBJECT')
```

### 8.2 Bone types in Blender 5.1

From `info_gotchas_armatures_and_bones.html`: Blender has three bone types that share
similar names but have different access contexts:

| Type | Access context | Data path |
|---|---|---|
| `EditBone` | Armature in Edit Mode | `armature.data.edit_bones` |
| `Bone` | Armature in Object/Pose Mode | `armature.data.bones` |
| `PoseBone` | Armature in Pose Mode | `armature.pose.bones` |

**Critical:** You can only create/modify bones via `EditBone` in Edit Mode.
`Bone` and `PoseBone` are read-only for structure.
Do not keep `EditBone` references after leaving Edit Mode; they become invalid.

### 8.3 Bone placement rules (CRITICAL)

> **Bones MUST be positioned inside the geometry they control.** If a bone is
> outside or at the edge of a mesh part, automatic weights will assign near-zero
> weight and that part will "float" during animation.

For multi-part characters (body + arms + legs + head + eyes):

```python
# CORRECT: Position arm bone INSIDE the arm cylinder
upper_arm_L = edit_bones.new("left_upper_arm")
upper_arm_L.head = (-0.6, 0, 1.3)   # At shoulder, inside arm mesh
upper_arm_L.tail = (-0.6, 0, 0.9)   # At elbow, inside arm mesh

# WRONG: Bone outside the arm mesh — auto-weights will fail
# upper_arm_L.head = (-1.5, 0, 1.3)  # Too far from body, outside arm mesh
```

**Rule:** After creating all bones, visually verify (or calculate) that each bone's
head and tail positions fall within the bounding box of the mesh part they should control.

### 8.4 Parenting mesh to armature

```python
# Select mesh first, then armature
bpy.ops.object.select_all(action='DESELECT')
mesh_obj.select_set(True)
arm_obj.select_set(True)
bpy.context.view_layer.objects.active = arm_obj

# Automatic weights
bpy.ops.object.parent_set(type='ARMATURE_AUTO')
```

### 8.5 Post-auto-weight cleanup (MANDATORY for rigged characters)

Automatic weights are unreliable for **small detail parts** (eyes, pupils, buttons,
antennae) and **extremities** (hands, feet, fingers). This applies to ALL character
types — humanoids, animals, robots, creatures, vehicles with moving parts.

After `ARMATURE_AUTO`, you MUST manually fix the weights for these parts:

```python
import bpy

def assign_vertices_to_bone(mesh_obj, bone_name, vertex_indices, weight=1.0):
    """Assign vertices exclusively to one bone, removing from all others.
    Works for any rigged mesh — characters, animals, robots, etc."""
    # Remove these vertices from ALL existing vertex groups
    for vg in mesh_obj.vertex_groups:
        try:
            vg.remove(vertex_indices)
        except:
            pass

    # Create or get the target vertex group
    vg = mesh_obj.vertex_groups.get(bone_name)
    if not vg:
        vg = mesh_obj.vertex_groups.new(name=bone_name)

    # Assign with full weight
    vg.add(vertex_indices, weight, 'REPLACE')


def find_vertices_near_bone(mesh_obj, armature_obj, bone_name, radius=0.3):
    """Find all mesh vertices within a radius of a bone's position.
    Useful for identifying which vertices belong to a specific body part."""
    bone = armature_obj.data.bones.get(bone_name)
    if not bone:
        return []
    # Bone center in world space
    bone_center = armature_obj.matrix_world @ ((bone.head_local + bone.tail_local) / 2)
    verts = []
    for v in mesh_obj.data.vertices:
        world_pos = mesh_obj.matrix_world @ v.co
        if (world_pos - bone_center).length < radius:
            verts.append(v.index)
    return verts


# === Usage Examples (adapt to your specific character) ===

# Get your mesh and armature by name:
# mesh_obj = bpy.data.objects.get("CharacterMesh")
# arm_obj  = bpy.data.objects.get("CharacterArmature")

# Example 1: Lock eyes to head bone (any character with eyes)
# eye_verts = find_vertices_near_bone(mesh_obj, arm_obj, "head", radius=0.15)
# assign_vertices_to_bone(mesh_obj, "head", eye_verts)

# Example 2: Lock a belt/accessory to spine bone
# belt_verts = find_vertices_near_bone(mesh_obj, arm_obj, "spine", radius=0.2)
# assign_vertices_to_bone(mesh_obj, "spine", belt_verts)

# Example 3: For robots — lock entire arm rigidly to upper_arm bone
# arm_verts = find_vertices_near_bone(mesh_obj, arm_obj, "left_upper_arm", radius=0.4)
# assign_vertices_to_bone(mesh_obj, "left_upper_arm", arm_verts)
```

> **When to use manual weights instead of auto-weights:**
>
> - Characters with **separate body parts joined into one mesh** (arms glued to body)
> - Any mesh with **small detail geometry** (eyes, pupils, buttons, bolts)
> - **Mechanical/robot characters** where parts should move rigidly (no smooth deformation)
>
> For robots/mechanical characters, consider using **rigid weights** (1.0 for the
> controlling bone, 0.0 for everything else) instead of smooth auto-weights.

### 8.6 Vertex groups for manual weight painting

```python
# Create vertex group matching bone name
vg = mesh_obj.vertex_groups.new(name="Root")
# Add vertices with weight (0.0 to 1.0)
vg.add([0, 1, 2, 3], 1.0, 'REPLACE')
```

### 8.7 Rigging validation — check for floating parts

After rigging ANY character (humanoid, animal, robot, creature), run this check:

```python
import bpy

# Check ALL rigged meshes in the scene, not just one specific object
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH' or not obj.parent or obj.parent.type != 'ARMATURE':
        continue

    unweighted = []
    weakly_weighted = []
    for v in obj.data.vertices:
        total_weight = sum(g.weight for g in v.groups)
        if total_weight < 0.001:
            unweighted.append(v.index)
        elif total_weight < 0.1:
            weakly_weighted.append(v.index)

    if unweighted:
        print(f"ERROR: {obj.name} has {len(unweighted)} unweighted vertices — they WILL float!")
    if weakly_weighted:
        print(f"WARNING: {obj.name} has {len(weakly_weighted)} weakly-weighted vertices — may drift.")
    if not unweighted and not weakly_weighted:
        print(f"OK: {obj.name} — all {len(obj.data.vertices)} vertices properly weighted.")
```

---

## 9. Animation

> **Blender 5.1 uses the layered/slotted Action API.** For robust scripting, access
> F-Curves through:
> `AnimData.action` → `Action.layers[...]` → `ActionKeyframeStrip.channelbag(slot)` → `ActionChannelbag.fcurves`.
> Treat direct `Action.fcurves` access as legacy behavior and do not rely on it for new code.

### 9.0 Helper: Get FCurves from any animated object (Blender 5.1)

Use this utility in **every** script that needs to read or modify FCurves:

```python
def get_fcurves_5_1(obj):
    """Return the FCurves collection for an animated object using the 5.1 slotted action API.
    Returns None if the object has no animation data."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return None
    action = ad.action
    slot = ad.action_slot
    if not slot:
        return None
    if not action.layers:
        return None
    layer = action.layers[0]
    if not layer.strips:
        return None
    strip = layer.strips[0]
    if strip.type != 'KEYFRAME':
        return None
    channelbag = strip.channelbag(slot)
    if not channelbag:
        return None
    return channelbag.fcurves


# Usage:
# fcurves = get_fcurves_5_1(obj)
# if fcurves:
#     for fc in fcurves:
#         for kp in fc.keyframe_points:
#             kp.interpolation = 'LINEAR'
```

### 9.1 Keyframe insertion — use object method, not operators

Always use `obj.keyframe_insert()` instead of `bpy.ops.anim.keyframe_insert()`.
The operator is slower and requires context setup.

```python
import bpy

obj = bpy.context.active_object
scene = bpy.context.scene

# Set frame range
scene.frame_start = 1
scene.frame_end = 120

# Keyframe at frame 1
scene.frame_set(1)
obj.location = (0, 0, 0)
obj.rotation_euler = (0, 0, 0)
obj.keyframe_insert(data_path="location", frame=1)
obj.keyframe_insert(data_path="rotation_euler", frame=1)

# Keyframe at frame 60
scene.frame_set(60)
obj.location = (5, 0, 0)
obj.rotation_euler = (0, 0, 3.14159)
obj.keyframe_insert(data_path="location", frame=60)
obj.keyframe_insert(data_path="rotation_euler", frame=60)

# Keyframe at frame 120 (loop back)
scene.frame_set(120)
obj.location = (0, 0, 0)
obj.rotation_euler = (0, 0, 6.28318)
obj.keyframe_insert(data_path="location", frame=120)
obj.keyframe_insert(data_path="rotation_euler", frame=120)
```

### 9.2 Always set frame range before animating

```python
scene = bpy.context.scene
scene.frame_start = 1
scene.frame_end = 250  # ~10 seconds at 24fps
scene.frame_current = 1
```

### 9.3 Duration guidelines

| Duration | Frames at 24fps | Use case |
|---|---|---|
| 2 seconds | 48 | Quick turntable / spin |
| 5 seconds | 120 | Short animation loop |
| 10 seconds | 240 | Scene flythrough |

Always set `scene.render.fps = 24` unless the user requests otherwise.

### 9.4 Camera turntable animation

```python
import bpy
import math

pivot = bpy.data.objects.new("CameraPivot", None)
bpy.context.collection.objects.link(pivot)
pivot.location = (0, 0, 0)

cam = bpy.data.objects.get("Camera")
if cam:
    cam.location = (6, 0, 3)
    cam.parent = pivot

    track = cam.constraints.new(type='TRACK_TO')
    track.target = pivot
    track.track_axis = 'TRACK_NEGATIVE_Z'
    track.up_axis = 'UP_Y'

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 120

    pivot.rotation_euler = (0, 0, 0)
    pivot.keyframe_insert(data_path="rotation_euler", frame=1)

    pivot.rotation_euler = (0, 0, math.radians(360))
    pivot.keyframe_insert(data_path="rotation_euler", frame=120)

    # Linear interpolation (no ease in/out)
    # Blender 5.1 layered/slotted path: Action → Layer → KeyframeStrip → Channelbag → FCurves
    # Prefer channelbag.fcurves; do not rely on direct Action.fcurves in new code.
    if pivot.animation_data and pivot.animation_data.action:
        action = pivot.animation_data.action
        slot = pivot.animation_data.action_slot
        if action.layers:
            layer = action.layers[0]
            if layer.strips:
                strip = layer.strips[0]
                if strip.type == 'KEYFRAME':
                    channelbag = strip.channelbag(slot)
                    if channelbag:
                        for fc in channelbag.fcurves:
                            for kp in fc.keyframe_points:
                                kp.interpolation = 'LINEAR'
```

> **Blender 5.1 layered/slotted Action API (CRITICAL)**
>
> Prefer channelbag access in layered actions. For robust F-Curve access, use:
>
> `AnimData.action` → `Action.layers[0]` → `ActionLayer.strips[0]` →
> `ActionKeyframeStrip.channelbag(slot)` → `ActionChannelbag.fcurves`
>
> The `slot` is obtained from `AnimData.action_slot`. When creating channels,
> use `ensure=True`: `strip.channelbag(slot, ensure=True)`.

### 9.5 Follow Path for vehicle/object animations

```python
import bpy

bpy.ops.curve.primitive_bezier_curve_add()
path = bpy.context.active_object
path.name = "AnimPath"

# IMPORTANT: For vehicles/ground objects, lock curve to 2D to prevent
# banking/tilt on curves. 3D curves cause the FollowPath to bank,
# which makes wheels dip below the ground plane.
path.data.dimensions = '2D'

obj = bpy.data.objects.get("MyCar")
if obj:
    constraint = obj.constraints.new(type='FOLLOW_PATH')
    constraint.target = path
    constraint.use_curve_follow = True
    constraint.forward_axis = 'FORWARD_Y'
    constraint.up_axis = 'UP_Z'

    # Animate the offset
    constraint.offset = 0
    constraint.keyframe_insert(data_path="offset", frame=1)
    constraint.offset = -100
    constraint.keyframe_insert(data_path="offset", frame=120)
```

> **Tip:** If the vehicle tilts/banks on curves, ensure `path.data.dimensions = '2D'`.
> For camera flythrough paths where banking is desired, use `'3D'` instead.

### 9.6 Material animation

```python
import bpy

obj = bpy.context.active_object
if obj and obj.data.materials:
    mat = obj.data.materials[0]
    # In Blender 5.1, use_nodes is a deprecated compatibility property.
    # Check node_tree directly instead.
    if mat.node_tree:
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            scene = bpy.context.scene

            scene.frame_set(1)
            bsdf.inputs['Base Color'].default_value = (1.0, 0.0, 0.0, 1.0)
            bsdf.inputs['Base Color'].keyframe_insert("default_value", frame=1)

            scene.frame_set(60)
            bsdf.inputs['Base Color'].default_value = (0.0, 0.0, 1.0, 1.0)
            bsdf.inputs['Base Color'].keyframe_insert("default_value", frame=60)
```

---

## 10. Render Settings

```python
scene = bpy.context.scene
scene.render.fps = 24
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.image_settings.file_format = 'FFMPEG'
scene.render.ffmpeg.format = 'MPEG4'
scene.render.ffmpeg.codec = 'H264'
scene.render.filepath = "//render_output"

# For EEVEE (fast preview renders, Blender 5.x enum):
scene.render.engine = 'BLENDER_EEVEE'
# For Cycles, switch engine first, then configure Cycles settings:
scene.render.engine = 'CYCLES'
# For Cycles, configure samples after switching the scene to Cycles:
scene.cycles.samples = 128
```

---

## 11. Post-Completion Workflow

After completing all modeling/scene work:

### 11.1 Automated validation

1. **Run the full validation script** from Section 1.
2. **Get scene info** using `get_scene_info` to confirm object count and names.
3. **For each key object**, use `get_object_info` to verify:
   - Location is correct
   - Scale is (1, 1, 1) — transforms should be applied
   - Polygon count is within budget
   - Bounding box makes sense

### 11.2 Structured visual inspection (MANDATORY)

Do **not** rely on a single 3/4 view. Inspect the model from multiple angles
to catch hidden defects (floating parts, gaps, misalignment, clipping).

**Six-side inspection checklist:**

| View | What to check |
|---|---|
| Front | Symmetry, facial features, facade alignment |
| Back | No missing faces, back of head/body complete |
| Left side | Arm/leg alignment, profile proportions |
| Right side | Mirror of left, no asymmetric defects |
| Top | Roof/top of head, no z-fighting, no gaps |
| Bottom | Ground contact, no geometry below ground plane |

After the six-side check, perform **close-up inspections** for:
- **Joints/connections** — where limbs meet body, wheels meet axle, posts meet base
- **Small parts** — eyes, buttons, bolts, antennae
- **Repeated elements** — verify spacing is consistent

Use `get_viewport_screenshot` after each angle to capture evidence.

### 11.3 Contact verification

For any parts that should physically touch, run the `check_contact()` utility
from Section 4.4 to verify numerically. Visual closeness is not proof of contact.

### 11.4 Report to the user

- Total polygon count across the scene
- Any warnings or issues found during validation
- Results of six-side inspection (note any defects found and fixed)
- Screenshot from the most representative angle for visual confirmation

---

## 12. Common Mistakes to Avoid

| Mistake | Why It's Bad | Correct Approach |
|---|---|---|
| UV Sphere with 128 segments | 16,384 faces for a sphere | Use 32 segments max (480 faces) |
| Not calling `view_layer.update()` | Stale transforms | Always call after location/rotation/scale |
| Skipping `mesh.validate()` after procedural mesh creation | Bad input can create invalid geometry | Use it as a safe default after `from_pydata()` |
| Not applying transforms before rigging | Mesh deforms incorrectly | `transform_apply()` before parenting |
| Using `mesh.calc_normals()` | Removed in Blender 5.1 | Use `normals_make_consistent()` |
| Objects floating above/below ground | Looks broken | Snap to ground using bounding box z-min |
| Assuming default node names always exist | Custom node trees may not have `Principled BSDF` or `Background` | Use `nodes.get(...)` and handle missing nodes |
| Not checking `operator.poll()` | RuntimeError crashes | Check poll() before calling operators |
| `BVHTree.FromObject(obj)` without depsgraph | Fails | Pass `depsgraph` as second argument |
| Accessing object-mode mesh data in Edit Mode | Data is out of sync with the edit mesh | Use `bmesh.from_edit_mesh()` or switch to Object Mode first |
| Creating bones outside Edit Mode | `EditBone` required | Always enter Edit Mode for bone creation |
| `bpy.ops.anim.keyframe_insert()` | Slow, context-dependent | Use `obj.keyframe_insert()` directly |
| Not setting frame range | Plays 250 frames by default | Set `frame_start` and `frame_end` |
| Not calling `scene.frame_set()` | Keyframe on wrong frame | Always call before keyframing |
| Forgetting LINEAR interpolation | Easing on rotation looks wrong | Set `kp.interpolation = 'LINEAR'` |
| Camera not pointing at subject | Camera looks at nothing | Use `TRACK_TO` constraint |
| Applying modifiers after rigging | Breaks armature linkage | Apply modifiers before rigging |
| Using `bpy.ops` when data access exists | Slow, fragile | Use `bpy.data` / direct properties |
| Using `action.fcurves` directly | Legacy path in layered actions; unreliable for new scripts | Use `ActionKeyframeStrip.channelbag(slot).fcurves` |
| FollowPath on 3D curve for vehicles | Car banks/tilts on curves, wheels clip ground | Set `path.data.dimensions = '2D'` |
| BVH overlap on rigged parent-child | False-positive warnings on intentional overlaps | Skip parent-child pairs in overlap check |
| Bones positioned outside mesh geometry | Auto-weights assign near-zero weight → parts float | Place bone head/tail **inside** the mesh part it controls |
| Trusting auto-weights for eyes/small parts | Small geometry gets conflicting weights from nearby bones | Manually assign eye/pupil vertices to `head` bone after auto-weights |
| Skipping post-rigging weight validation | Unweighted vertices float in animation but look fine in rest pose | Run Section 8.7 validation to detect zero-weight vertices |
| Using `mesh.use_auto_smooth` | Removed in Blender 4.1+ | Use the **Smooth by Angle** node modifier instead |
| Using Python threads for `bpy` calls | Crashes Blender — API is not thread-safe | Run all `bpy` operations on the main thread |
| Skipping contact verification | Parts look close but have visible gaps | Use `check_contact()` from Section 4.4 |
| Only inspecting from 3/4 view | Hidden defects on back, bottom, or sides | Run the six-side inspection from Section 11.2 |
| Assuming `use_nodes` must be set to `True` | `use_nodes` is deprecated/no-op in Blender 5.0+ | Direct access to `mat.node_tree` is safe; just clear or manage default nodes |
| Using dict-like access for built-in settings | Disabled in Blender 5.0+; throws errors (e.g., `scene['cycles']`) | Use standard attribute notation (e.g., `scene.cycles`) for registered properties |

---

## 13. Common Failure Patterns by Domain

Different asset types have different failure modes. Check the relevant section
before modeling a specific category.

### 13.1 Characters (humanoid, animal, creature)

| Failure | Prevention |
|---|---|
| Eyes/pupils float during animation | Manually assign eye vertices to `head` bone (Section 8.5) |
| Arms detach at shoulder during motion | Ensure shoulder bone head is **inside** torso mesh |
| Fingers/toes have zero weight | Auto-weights fail on thin extremities — assign manually |
| Body parts overlap after posing | Apply transforms before rigging (Section 3.2) |
| Character sinks into ground when walking | Ground-snap after every pose; validate z-min in walk cycle |

### 13.2 Vehicles (cars, trucks, aircraft)

| Failure | Prevention |
|---|---|
| Wheels clip through ground on curves | Use `path.data.dimensions = '2D'` for Follow Path (Section 9.5) |
| Wheels not touching ground at rest | Use `check_contact()` between each wheel and chassis |
| Vehicle banks/tilts unrealistically | 2D curve prevents banking; add manual tilt only if desired |
| Door/hood gaps visible | Verify contact between panel objects with Section 4.4 |
| Suspension parts float | Anchor each part to chassis using bounding-box math |

### 13.3 Buildings and architecture

| Failure | Prevention |
|---|---|
| Windows not aligned in grid | Calculate positions from wall dimensions, don't eyeball |
| Roof overhang inconsistent | Derive overhang from building width, use constants |
| Door too large/small for wall | Estimate door:wall height ratio before building (~0.4–0.5) |
| Foundation floating above ground | Ground-snap the entire building after placement |
| Repeated elements (windows, columns) have uneven spacing | Build one module, verify, then duplicate with calculated offsets |

### 13.4 Mechanical/industrial assets

| Failure | Prevention |
|---|---|
| Bolts/rivets float above surface | Use face-snapping or inset the bolt into a cut pocket |
| Pipes don't connect at joints | Build cross-section rings and bridge edge loops at bends |
| Panel seams have visible gaps | Use contact verification (Section 4.4) between panels |
| Gears/wheels have too many polygons | Use cylinder with `vertices=16` or `vertices=24`, not defaults |
| Cable endpoints don't reach sockets | Anchor curve endpoints to actual port/socket positions |
