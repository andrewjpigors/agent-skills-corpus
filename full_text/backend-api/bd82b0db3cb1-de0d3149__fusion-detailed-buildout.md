---
name: fusion-detailed-buildout
description: "Procedural high-fidelity CAD buildout of rooms / equipment / props in Autodesk Fusion, driven from WSL via the Fusion MCP. Load when you are about to script geometry into a Fusion Design — modeling a room, an instrument, a vessel/tank/kiln, casework, glassware, a fixture, or any real-world object — and the bar is COMPREHENSIVE detail (recessed door/drawer panels, knobs/displays/status-lights, spouts/necks/caps, 5-star bases, fume-hood sashes) rather than a single blocky primitive. Codifies the runtime model (def run(_context), cm-internal units, file read-back over the never-surfaced return value, no ui.messageBox), the into-component local-coord build pattern + Z##_Room_Element_NN naming + idempotency, the shape-decomposition vocabulary (primitives + the small features that make an object READ), the plan-spec-then-staged-build workflow, paste-ready API helpers (offset-start extrude, cyl, ring/annulus, loft cone, rotated-polygon leg, placement transforms), the verification loop (bbox read-back + containment audit + isolate/explicit-camera framing), the matte/glass/metal appearance pass, and the failure-mode catalog (read-back-never-written false hang, loft-heavy slowness, cm/mm unit slips, screenshot auto-reframe, concurrent-writer corruption). Skip for non-Fusion CAD, for single-block L1 massing where one primitive suffices, or for pure appearance/audit passes with no new geometry. Pairs with [[skill-agent-orchestration]] for multi-room scale-out."
allowed-tools: Bash, Read, Write, Edit, Agent, ToolSearch, Monitor
user-invocable: true
version: 1.1.0
---

# fusion-detailed-buildout

How to build a richly detailed Fusion 3D model — one room, instrument, vessel, or prop at a time — by scripting the Fusion API through the WSL→Fusion MCP bridge, at the level of fidelity where every object **reads** as the real thing (recessed cabinet doors with reveal gaps and bar handles, instruments with displays/knobs/status-lights/vents, glassware with spouts/necks/lips/caps, 5-star stool bases, a partly-lowered fume-hood sash). Distilled from the real buildout of an example multi-room industrial facility: a detailed showcase lab (68 sub-components / 403 bodies) plus the surrounding 11-room facility (93 components / 262 bodies) in a project referred to below as `/path/to/project`.

This is the canonical reference for **detailed procedural Fusion buildout**. It is layer-agnostic: it applies whether you are the root agent driving Fusion directly, or a subordinate handed one room/element to detail. For driving *many* rooms in parallel with serialized writers, pair this with the `agent-orchestration` skill (`[[skill-agent-orchestration]]`); §11 below is the bridge.

---

## 1. When to load this skill

Load when ALL of these hold:

- You are scripting **new geometry** into an Autodesk Fusion Design (not another CAD tool — this skill is Fusion-API-specific).
- The object is a real-world thing that should be **recognizable**, not a stand-in box: a lab room, a vessel/tank/reactor, a rotary kiln, a cyclone/hopper, casework (cabinets/benches), an instrument (balance, microscope, centrifuge, furnace, XRD), glassware, a fume hood, a stool/chair/cart, safety fixtures.
- The detail bar is **L2 or L3** (recognizable shape language → fine identifying features), i.e. "comprehensive detail," not L1 single-primitive massing.

Load also when:

- You are writing a per-room **spec doc** that a builder will execute (§5), or
- You are running the **appearance pass** (§9) or **verification loop** (§8) over a detailed build, or
- You are orchestrating a detailed buildout across multiple rooms (§11).

Skip when:

- The CAD tool is not Fusion (SolidWorks/Onshape/FreeCAD/blender — different API, none of the helpers transfer).
- The task is genuine **L1 blocky massing** where one primitive block per item is the agreed tier (then you don't need the shape vocabulary; just `box_z` each item).
- It's a pure non-geometry pass with no new bodies (e.g. only renaming, only re-coloring an existing build — though the appearance methodology in §9 is still worth reading).
- A conversational answer with no Fusion write.

---

## 2. Runtime model — driving Fusion from WSL

Fusion is the Windows desktop app; it exposes an official local MCP server at `127.0.0.1:27182`. A WSL instance reaches it through a Windows **portproxy** `0.0.0.0:27183 → 127.0.0.1:27182`. The client is `/path/to/project/tools/fusion_mcp.py`.

**Preconditions (verify before anything):**
- Fusion must be **open with an active parametric Design**. Scripts no-op silently against no Design — every script guards with `if not isinstance(des, adsk.fusion.Design): _write({"ok": False, "reason": "no active Design"})`.
- The portproxy + firewall rule must be live. `fusion_mcp.py` resolves the WSL gateway IP dynamically (it changes on `wsl --shutdown`); the registered `claude mcp` URL is hardcoded — re-point if it disconnects.

**The three driver verbs (run from the project root):**

```bash
python3 tools/fusion_mcp.py exec  scripts/rooms/Z08_stage1_casework.py        # run a Fusion API script
python3 tools/fusion_mcp.py shot  iso-top-right artifacts/screenshots/x.png    # screenshot the viewport
python3 tools/fusion_mcp.py read  '{"queryType":"screenshot","direction":"front"}'   # raw read query
python3 tools/fusion_mcp.py tools                                              # list MCP tool names
```

**The script shape — every build/util script is one `def run(_context)`:**

```python
import adsk.core, adsk.fusion, traceback, json

OUT = r"\\wsl.localhost\<Distro>\path\to\project\artifacts\readback\<name>.json"

def run(_context):
    try:
        app = adsk.core.Application.get()
        des = app.activeProduct
        if not isinstance(des, adsk.fusion.Design):
            _write({"ok": False, "reason": "no active Design"}); return
        root = des.rootComponent
        # ... build geometry ...
        _write({"ok": True, ...})          # structured read-back
    except:
        _write({"ok": False, "trace": traceback.format_exc()})

def _write(data):
    try:
        with open(OUT, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass
```

**Read-back: the return value is NOT surfaced.** The MCP `execute` tool reports only success/error — a script's `run()` return value never comes back. So every script writes structured JSON **into the WSL filesystem** via the UNC path `\\wsl.localhost\<Distro>\...` (keeps everything WSL-local — no C: writes). The orchestrator then `Read`s the WSL-local file `artifacts/readback/<name>.json` in the project. **Wrap `_write` in try/except** so a read-back failure never throws out of `run` — but see Failure Mode (a): a missing read-back can make a waiting agent hang even though Fusion finished.

**Screenshots** come back as base64 image content from `fusion_mcp_read queryType:screenshot`; `shot` decodes and saves the PNG. Screenshot camera labels are **nonstandard** (`front` = top-down plan view). Trust the geometric bbox read-back as authoritative over the screenshot camera; use explicit camera framing (§8) when you need a reliable view of one part.

**Units — the #1 footgun.** The Fusion API internal length unit is **cm**, even though the document is set to mm.
- `ValueInput.createByReal(v)` interprets `v` as **cm**.
- `ValueInput.createByString("%g mm" % v)` interprets the string with explicit units — **always prefer this** for sketch extents and plane offsets when your design numbers are in mm.
- Point3D coordinates are raw cm: the build scripts define `MM = 0.1` and multiply every mm coordinate by `MM` before passing to `Point3D.create`. A forgotten `MM` makes a part **10× too big or small** (see Failure Mode (c) — the stool seat).

**NEVER call `ui.messageBox`** (or any modal dialog). A modal blocks the headless MCP run forever (Failure Mode (d)).

---

## 3. Build pattern — into-component, local coordinates

**One top-level component per room; equipment nested as sub-components.** The room component (e.g. `Z08_QCLab`) is created empty at Phase 1, already translated to its world origin by its occurrence transform. Builders add geometry **into** that component in **room-local coordinates** (0,0 = a chosen room corner). This keeps writers non-overlapping (no shared-wall ownership disputes) and makes per-room specs portable.

```python
ROOM_OCC = "Z08_QCLab:1"
occ = root.occurrences.itemByName(ROOM_OCC)
if occ is None:
    _write({"ok": False, "reason": "occurrence %s not found" % ROOM_OCC}); return
roomComp = occ.component

def new_sub(name):
    s = roomComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())  # identity transform
    s.component.name = name
    return s.component
```

- **Sub-component per element.** Each real object (a cabinet, an instrument, a beaker) is its own named sub-component, holding one-or-many bodies. This is what makes selection, isolation (§8), and keyword-driven appearances (§9) work.
- **Naming: `Z##_Room_Element[_NN]`** for the sub-component; bodies inside get descriptive suffixes (`..._Carcass`, `..._Door`, `..._DoorHandle`, `..._GlassSash`, `..._Display`). The descriptive body names are load-bearing — the appearance pass keywords off them (`sash`/`shield`/`glass`→glass, `screen`/`display`→dark). Resolve `_NN` per the room spec.
- **Local vs world bbox.** A nested body's `boundingBox` is **component-local** (relative to the room origin), because the occurrence carries the world transform. Read-back in build scripts reports local mm (`min/max * 10`). To get a WORLD bbox (for containment against the building, or to frame a camera), read the **occurrence's** `boundingBox` (already world) — that's what `focus_sub.py` and `isolate.py` use. Mixing the two is Failure Mode (h).
- **Idempotency — delete this stage's subs before rebuild.** A stage owns a fixed list of sub-component names and deletes exactly those before rebuilding, so re-running a stage is safe and doesn't double-build:

```python
STAGE2_SUBS = ["Z08_QCLab_FumeHood_01", "Z08_QCLab_Balance_01", ...]
want = set(STAGE2_SUBS)
for sub in list(roomComp.occurrences):     # list() — snapshot, you're mutating
    if sub.component.name in want:
        sub.deleteMe()
```

  Stage 1 (the casework foundation) instead wipes the WHOLE room (it replaces the prior simple equipment): `for sub in list(roomComp.occurrences): sub.deleteMe()` plus `for b in list(roomComp.bRepBodies): b.deleteMe()`.
- **Parametric shared params, no magic numbers — with a caveat.** The plant convention (`AGENTS.md`) is: dimensions driven from lowerCamelCase shared user parameters (`workHeight=900`, `ceilingHeight=6000`), no magic numbers, no new params without orchestrator approval. In the *detailed showcase* scripts the team pragmatically used Python constants for the dense per-element dims (and said so in the read-back notes — "All dims Python constants; no params") while still **referencing** the pinned shared values (`WORK_HEIGHT = 900.0   # references param workHeight`). The rule that always holds: **the cross-stage reference dims are pinned and shared** so stages compose; only the within-element detail dims are local constants. The param-unit gotcha: a user parameter's value is in the document unit, but when you read it back into a script for `createByReal` you still owe the cm conversion.

---

## 4. Detail methodology — the shape vocabulary (THE CORE)

**Guiding principle:** *a detailed object = the correct primitives at the correct relative positions, PLUS the small identifying features that signal what it is.* A box at the right footprint is L1. The same box with a recessed front panel set in by a ~3-4 mm reveal, a thin bar handle proud of that panel, a recessed toe-kick at the base, and a worktop slab on top — that READS as a cabinet. The fidelity lives in the small features, and they are cheap (a few extra `box_z`/`cyl_z` calls). Push fidelity where it's cheap.

**Decompose any real object into primitives + fine features.** Catalog drawn from the real lab + plant builds:

**Vessels / tanks / reactors** — vertical cylinder body + dished top (a low `cone_z` cap or a short wide cylinder) + support legs (4 boxes) or a skirt + a platform where specified. (`scene_detail_spec.md` L2.)

**Rotary kiln** — long slightly-inclined cylinder + drive housing block + support rollers + feed/discharge hoods at the ends.

**Cyclone / hopper** — a cone (via loft between two circles, §7) OR a stacked-cylinder taper if you want to avoid loft cost; collection hopper cone underneath. (Loft is the honest cone but is slow at scale — see Failure Mode (b).)

**Casework (cabinet / bench)** — this is the canonical detailing pattern:
- **Carcass** box from toe-kick top to cabinet top.
- **Toe-kick**: a narrower box set BACK from the front face (recessed plinth) at the base.
- **Worktop slab** on top, with a small **backsplash** box along the wall.
- **Door** mode: one recessed panel inset by `DOOR_GAP ≈ 4 mm` all around, sitting `PANEL_PROUD ≈ 18 mm` proud of the carcass face, + a vertical **bar handle** box near the opening edge.
- **Drawers** mode: two stacked recessed fronts, each with a horizontal bar handle.
- The reveal gap is what makes panels read as separate doors/drawers. See the `base_cabinet()` helper in `Z08_stage1_casework.py` (and `base_cabinet_west()` for the rotated-orientation variant where the front faces +x instead of +y).

**Instruments** (balance, microscope, centrifuge, furnace, XRD, pH meter, analyzer) — **housing** box + **recessed display panel** (a thin box, ~8 mm deep, sitting just proud of the front) + **knob/button cylinders** (small `cyl_z`) + **status lights** (small cylinder on top) + **vents** (thin slot boxes or shallow cuts on a side) + **feet**. Add the device-specific signature: microscope = base + vertical arm + stage + objective turret disc + 3 tiny objective cylinders + angled head + 2 eyepiece tubes + side focus knob; centrifuge = body + domed lid (shallow wide cylinder) + back hinge + front panel + 3 buttons; furnace = body + recessed insulated door + door handle + control panel + display + knob + a small flue chimney; XRD = tall cabinet + leaded-glass sample door + sloped console (approx as a stacked box) + display + X-ray-on status light + side vent slots.

**Glassware** (the showcase set) — all built from tapered cylinders, cones (loft), and stacked cones for bulbs:
- **Beaker** = slightly tapered cylinder (`cone_z` with top dia > bottom dia, ~0.92 ratio) + a thin rim ring + a small pour-spout box at the rim.
- **Erlenmeyer flask** = cone (wide base → narrow top) + short cylindrical neck + a lip ring.
- **Volumetric flask** = bulb (approximated as two cones: a widening lower half + a narrowing upper half ≈ sphere) + long thin neck + graduation ring + stopper.
- **Graduated cylinder** = wide short foot cylinder + tall thin body cylinder + small spout.
- **Reagent bottle** = cylinder body + shoulder (cone narrowing) + short neck + cap cylinder.
- **Wash bottle** = body cylinder + shoulder cone + cap + an angled spout tube (approx as a thin box).
- See `reagent_bottle()`, `gas_cyl()`, the beaker/flask/vol loops in `Z08_stage3_accessories.py`.

**5-star stool / task-chair base** — central **hub** cylinder + 5 **radial legs** (rotated thin profiles, one per 72°, via the `leg()` rotated-polygon helper §7) + a **caster** cylinder at each leg end + a gas-lift **post** cylinder + a **foot-ring** (annulus via the 2-loop `ring()` helper) + a round **seat** (dished disc) — and for a chair, a backrest box. See `stool()` in stage 3 and the clean `rebuild_stools.py` rebuild.

**Fume hood** — base cabinet (floor→worktop) + back panel + 2 side walls + top housing slab + a fascia header above the opening + an **airfoil** sill at the front edge + a movable **glass sash** (a thin box positioned partly-lowered, left transparent for the appearance pass) + a sash pull handle + an interior **baffle** panel + a round **exhaust collar** + a riser cylinder to the ceiling + a few service-valve knob cylinders. See the FumeHood block in `Z08_stage2_instruments.py`.

**Detail tiers (what "comprehensive detail" means) — `docs/scene_detail_spec.md`:**
- **L1 Blocky** — one primitive block per item at correct footprint/height/position. Goal: correct spatial layout + material-flow legibility.
- **L2 Recognizable** — the shape language above: tanks get cylinders+legs+dished tops, kilns get tubes+drives+hoods, casework gets cabinets+worktops, instruments get housings+displays+knobs. Goal: the object is identifiable.
- **L3 Connective + fine** — pipe/duct runs, conveyors, instrumentation stubs, corridor carts; and at the prop level, the small features (spouts, vents, status lights, recessed reveals, handles) that make it photo-real. The showcase lab is L3-level prop detail.
- Tiers are **additive** — build L1 plant-wide first for a coherent skeleton, enrich to L2, then L3. Each tier is a separate serialized write pass.

**Approximation is allowed — and should be declared.** Swept arcs (gooseneck faucet, wash-bottle spout) are approximated as straight riser + horizontal arm + downturn tip. Spheres are approximated as two cones. Pipes are approximated as long thin boxes. Sloped consoles/fascias are approximated as stacked boxes. The discipline: **state the approximation in the read-back `notes`** ("Faucet gooseneck APPROX as straight riser+horizontal spout arm+downturn tip (no swept arc)") so the auditor/PI knows what's literal vs suggestive.

---

## 5. Plan before build — the spec-doc approach

For anything denser than a couple of items, write a **per-room (or per-element) spec doc FIRST**, then a builder executes it. The showcase used `docs/rooms/Z08_showcase.md`. A good spec has:

1. **Goal + theme** — one line (e.g. "richly detailed analytical QC lab, powder/battery-cathode QC theme so instruments are thematically right").
2. **Interior envelope + origin convention** — `5000(x) × 4000(y) × 6000(z)`, `0,0 = SW corner of interior`, "build into the `Z08_QCLab` component (already translated to world origin)."
3. **Pinned reference dims** — the cross-stage shared values so stages compose: worktop surface `z=900` (`workHeight`), base cabinets `z∈[100,860]` on a toe-kick `z∈[0,100]`, reagent shelves at `z=1300/1650`, door on the south wall centered, **keep the entry walkway clear**. These are the contract between stages.
4. **Zone layout (local coords)** — each functional zone with footprint (`x∈[300,4700], y∈[3300,4000]`), depth, and what lives there.
5. **Curated element list** — every element with its resolved `_NN`, descriptive name (`Z08_QCLab_<Element>_NN` for appearance keywording), footprint/height/position, and which stage owns it.
6. **Detailing guidance** — the per-element fidelity targets ("cabinet doors as recessed panels with a ~3 mm gap + bar handles; beaker = tapered cylinder + spout; instruments get displays/knobs/status-lights/vents; sash + draft shield are TRANSPARENT, left for the appearance pass").
7. **Build order** — the stage sequence (§6) and the note that **appearances are a separate later pass** (builder leaves default gray, uses descriptive names for keywording).

There is a template at `docs/room_spec_template.md` in the project. Spec authoring is non-write work and can run in parallel with a writer in another room (different file lanes).

**Spec skeleton (paste-ready):**

```markdown
# Z## <Room> — detail spec
Goal: <one line, with theme>. Interior = LxWxH; 0,0 = <corner>. Build into `Z##_<Room>` (at world origin).

## Pinned reference dims (so stages compose)
- <surfaceHeight z=...> ; <cabinet bands> ; <shelf heights> ; <door wall + clear walkway>

## Zone layout (local)
- <Zone A>: footprint x∈[..], y∈[..], depth ..; holds <...>.
- <Zone B>: ...

## Element list (resolve _NN; descriptive names `Z##_<Room>_<Element>_NN`)
**Stage 1 casework:** <...>
**Stage 2 instruments:** <...>
**Stage 3 accessories/safety:** <...>

## Detailing guidance
- <per-element fidelity targets; what's transparent/left for appearance pass>

## Build order
Stage 1 → Stage 2 → Stage 3. Appearances in a SEPARATE later pass (default gray; descriptive names).
```

---

## 6. Staged building — decompose a dense buildout

A dense room is too much for one script (both for reliability and for the loft-slowness in Failure Mode (b)). Decompose into **stages by element class**, run serially, each idempotent over its own subs:

- **Stage 1 — casework** (the foundation): benches/worktops, base + wall cabinets, sink, faucet, shelves. Pins the worktops at `z=900` that later stages sit on. Stage 1 wipes the whole room.
- **Stage 2 — instruments**: everything that sits on the pinned worktops or the floor (balance, microscope, centrifuge, analyzer, hot-plate, pH meter, furnace + oven on a stand, XRD, computer, chair, fume hood). Idempotent over its own sub list.
- **Stage 3 — accessories / glassware / safety**: beakers/flasks/bottles, racks, stools, cart, gas cylinders, emergency shower, eyewash, extinguisher, waste bins, whiteboard, clock, service spine.

Rules:
- **One Fusion writer at a time.** The Fusion API is single-threaded; concurrent writers corrupt state (Failure Mode (g)). Serialize. Non-write work (spec docs, layout math, draft scripts) may run in parallel.
- **Idempotent per stage** — each stage deletes exactly its own named subs first (§3), so a re-run is clean.
- **AVOID loft-heavy mega-scripts.** Stage 3 in the real build had ~250 loft bodies and was slow enough that the waiting agent hung on a read-back that arrived late (Failure Modes (a)+(b)). Mitigations: prefer extrude/`cyl_z` over loft where a stacked-cylinder taper reads well enough; keep cone/loft count bounded per script; split a very dense stage into sub-batches; and make the orchestrator check Fusion state directly rather than trusting the wait.
- **Batch by item-count**, not by zone, when scaling — a script with 40 simple boxes is fine; a script with 250 lofts is not.

---

## 7. Fusion API toolkit (paste-ready, extracted from the real scripts)

These are the actual working helpers from the build. Two idioms appear:
- **Plane-offset extrude** (`box_z`/`cyl_z`/`cone_z`): create a construction plane at `z0`, sketch on it, extrude up by `h`. Uses `createByString('… mm')` so it's mm-correct. This is what the room builders use.
- **Offset-start extrude** (`extrude(z0,z1)`): one sketch on XY, extrude from `z0` to `z1` via `OffsetStartDefinition`. Cleaner for stacked coaxial parts (stools). Uses `createByReal` so coordinates are **cm** here (note `cyl(... 19.0 ...)` = 190 mm radius).

```python
MM = 0.1  # mm -> cm (API internal). Multiply every mm COORDINATE by MM before Point3D.create.
VI = adsk.core.ValueInput
P  = adsk.core.Point3D.create
FO = adsk.fusion.FeatureOperations

# --- box: footprint (x,y,w,d) at height z0, extruded up h. All args in mm. ---
def box_z(comp, x, y, w, d, h, z0, bname):
    if w <= 0 or d <= 0 or h == 0:
        return None
    planes = comp.constructionPlanes
    pin = planes.createInput()
    pin.setByOffset(comp.xYConstructionPlane, VI.createByString("%g mm" % z0))
    plane = planes.add(pin)
    sk = comp.sketches.add(plane)
    sk.sketchCurves.sketchLines.addTwoPointRectangle(
        P(x * MM, y * MM, 0), P((x + w) * MM, (y + d) * MM, 0))
    ein = comp.features.extrudeFeatures.createInput(
        sk.profiles.item(0), FO.NewBodyFeatureOperation)
    ein.setDistanceExtent(False, VI.createByString("%g mm" % h))   # negative h cuts downward
    b = comp.features.extrudeFeatures.add(ein).bodies.item(0)
    b.name = bname
    return b

# --- cylinder: center (cx,cy), diameter dia, height h from z0. mm. (h<0 extrudes down) ---
def cyl_z(comp, cx, cy, dia, h, z0, bname):
    planes = comp.constructionPlanes
    pin = planes.createInput()
    pin.setByOffset(comp.xYConstructionPlane, VI.createByString("%g mm" % z0))
    plane = planes.add(pin)
    sk = comp.sketches.add(plane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(P(cx * MM, cy * MM, 0), (dia / 2.0) * MM)
    ein = comp.features.extrudeFeatures.createInput(
        sk.profiles.item(0), FO.NewBodyFeatureOperation)
    ein.setDistanceExtent(False, VI.createByString("%g mm" % h))
    b = comp.features.extrudeFeatures.add(ein).bodies.item(0)
    b.name = bname
    return b

# --- truncated cone via loft between two circles (flasks, shoulders, beakers, funnels) ---
#     dia_bot != dia_top. SLOW at scale — see Failure Mode (b); prefer a stacked-cyl taper if you can.
def cone_z(comp, cx, cy, dia_bot, dia_top, h, z0, bname):
    planes = comp.constructionPlanes
    pin0 = planes.createInput()
    pin0.setByOffset(comp.xYConstructionPlane, VI.createByString("%g mm" % z0))
    sk0 = comp.sketches.add(planes.add(pin0))
    sk0.sketchCurves.sketchCircles.addByCenterRadius(P(cx * MM, cy * MM, 0), (dia_bot / 2.0) * MM)
    pin1 = planes.createInput()
    pin1.setByOffset(comp.xYConstructionPlane, VI.createByString("%g mm" % (z0 + h)))
    sk1 = comp.sketches.add(planes.add(pin1))
    sk1.sketchCurves.sketchCircles.addByCenterRadius(P(cx * MM, cy * MM, 0), (dia_top / 2.0) * MM)
    lofts = comp.features.loftFeatures
    li = lofts.createInput(FO.NewBodyFeatureOperation)
    li.loftSections.add(sk0.profiles.item(0))
    li.loftSections.add(sk1.profiles.item(0))
    b = lofts.add(li).bodies.item(0)
    b.name = bname
    return b
```

**Offset-start extrude + ring/annulus + rotated-polygon leg** (from `rebuild_stools.py` — cm units, coordinates already cm):

```python
VR = adsk.core.ValueInput.createByReal   # interprets value as CM

def extrude(comp, prof, z0, z1, name):           # extrude a profile from z0 to z1 (cm)
    exts = comp.features.extrudeFeatures
    ei = exts.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ei.startExtent = adsk.fusion.OffsetStartDefinition.create(VR(z0))   # start the extrude AT z0
    ei.setDistanceExtent(False, VR(z1 - z0))
    b = exts.add(ei).bodies.item(0); b.name = name
    return b

def cyl(comp, cx, cy, r, z0, z1, name):          # coaxial cylinder, cm
    sk = comp.sketches.add(comp.xYConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(P(cx, cy, 0), r)
    extrude(comp, sk.profiles.item(0), z0, z1, name)

def ring(comp, cx, cy, r_out, r_in, z0, z1, name):   # ANNULUS: pick the 2-loop profile (outer+inner)
    sk = comp.sketches.add(comp.xYConstructionPlane)
    cc = sk.sketchCurves.sketchCircles
    cc.addByCenterRadius(P(cx, cy, 0), r_out)
    cc.addByCenterRadius(P(cx, cy, 0), r_in)
    prof = None
    for i in range(sk.profiles.count):
        if sk.profiles.item(i).profileLoops.count == 2:   # the ring profile has 2 loops
            prof = sk.profiles.item(i); break
    extrude(comp, prof or sk.profiles.item(0), z0, z1, name)

def leg(comp, cx, cy, ang_deg, name):            # a radial leg: rotated trapezoid swept out from center
    th = math.radians(ang_deg)
    ux, uy = math.cos(th), math.sin(th)          # radial unit vector
    tx, ty = -math.sin(th), math.cos(th)         # tangential unit vector
    r_in, r_out, w_in, w_out = 2.5, 21.5, 2.75, 1.9   # cm: inner/outer radius, inner/outer half-width
    pts = [(cx + r_in*ux + w_in*tx, cy + r_in*uy + w_in*ty),
           (cx + r_out*ux + w_out*tx, cy + r_out*uy + w_out*ty),
           (cx + r_out*ux - w_out*tx, cy + r_out*uy - w_out*ty),
           (cx + r_in*ux - w_in*tx, cy + r_in*uy - w_in*ty)]
    sk = comp.sketches.add(comp.xYConstructionPlane)
    lines = sk.sketchCurves.sketchLines
    pc = [P(x, y, 0) for x, y in pts]
    for i in range(4):
        lines.addByTwoPoints(pc[i], pc[(i + 1) % 4])
    extrude(comp, sk.profiles.item(0), 1.8, 5.0, name)
```

**Radial placement** (legs, casters, valves, pipettes — anything arrayed around a center):

```python
import math
for k in range(5):                                  # 5-star: one every 72°
    ang = k * (2.0 * math.pi / 5.0)
    ex = cx + R * math.cos(ang)
    ey = cy + R * math.sin(ang)
    cyl_z(comp, ex, ey, dia, h, z0, "%s_Caster_%02d" % (nm, k + 1))
```

**Placement transforms / rotation** — `new_sub` uses `Matrix3D.create()` (identity) and builds the body at its local coords; to place a whole sub-component, set a translation/rotation on the occurrence's `Matrix3D` instead of moving every body. For axis-rotated parts within a component, the cleanest path the build used is to **compute rotated sketch points** (the `leg()` helper) rather than rotating features — fewer moving parts, deterministic bbox.

**Notes on the helpers:**
- `box_z`/`cyl_z` guard against degenerate inputs (`w<=0` / `h==0`) so a zero-size part silently no-ops instead of throwing.
- Negative `h` extrudes downward (used for a faucet spout tip hanging below the arm, and basin recesses below the worktop).
- Fillets/chamfers: the spec calls for rounded worktop/instrument edges; in practice the build kept edges square and relied on shape + appearance for read. If you add fillets, do them as a final feature on the specific edges and re-audit the bbox (fillets shrink the bbox slightly).
- Booleans/cuts: extrude with `CutFeatureOperation` against a target body, or use `combineFeatures`. The lab build mostly used additive bodies (a recessed panel is a separate proud box, not a cut) — cheaper and the read-back stays one-body-per-feature.

---

## 8. Verification loop

Every write pass is verified three ways; **trust the geometric bbox over the screenshot camera.**

1. **Structured read-back JSON (per-body bbox + containment flag).** Each build script's `_emit()` walks the room's sub-components, reads each body's local bbox (`min/max * 10` → mm), flags `inside` against the interior envelope with a small tolerance, and writes `{ok, bodyCount, allInside, bodies:[{name, sub, local_min_mm, local_max_mm, inside}], notes}`. The orchestrator `Read`s this and confirms `allInside` + the expected `bodyCount` + reads the `notes` (which declare approximations). This is authoritative — it's exact geometry, not a camera guess.

2. **Audit scripts** (`scripts/rooms/audit_rooms.py`, `scripts/final_audit.py`) — run after a commit, over the whole design:
   - **Containment**: for a frozen room table (`name → (Lx,Wy,H)`), every direct + nested body must be inside the envelope (TOL ≈ 5 mm). Reports `violations`.
   - **Naming compliance**: `final_audit.py` lists every component + sub-name; the orchestrator checks the `Z##_Room_Element_NN` convention (the real Phase 4 reported **0 naming violations**).
   - **Param check**: reports `userParamCount` + the param list, so an unexpected new param (a writer that violated "create none without approval") shows up.
   - **Census**: `componentCount`, `totalBodies`, per-top-level sub counts — confirms the expected growth (e.g. components 60→… as rooms populate) and that other rooms were untouched.

3. **Isolate / focus + explicit-camera framing** to inspect ONE part un-occluded:
   - `set_shell_visible.py` toggles the `Z00_BuildingShell` occurrence's `isLightBulbOn` so equipment is visible un-occluded (reads desired state from a flag file written by WSL before exec).
   - `isolate.py` turns on exactly one top-level component and frames an **explicit orthographic camera** on its world bbox (computes center + diagonal, sets `cam.eye = center + (diag, -diag, 0.8·diag)`, `cam.viewExtents = 0.72·diag`). Reads the target name from a flag file.
   - `focus_sub.py` does the same for a **nested** sub-component (turns on its room, turns off sibling subs, frames the sub's world bbox) AND dumps the focused sub's bodies (world mm) into the read-back — so you get geometry + a reliable view of one instrument at once.
   - The **flag-file pattern**: WSL writes a tiny flag (`isolate.flag` = component name) before `exec`, the script reads it. This is how you parameterize a util script without editing it each run.

**Screenshot caveats (don't be fooled by the camera):**
- The MCP screenshot camera labels are nonstandard (`front` = top-down plan). `app.activeViewport.fit()` (called at the end of every build) and a bare `shot` **auto-reframe to the whole design** — so a screenshot after a build shows the entire plant, not the part you just built (Failure Mode (e)). To inspect one part, run `isolate.py`/`focus_sub.py` first (which sets an explicit camera), THEN `shot current` (or screenshot without re-fitting). When in doubt, **believe the bbox numbers, not the picture.**

---

## 9. Materials & appearances — a separate pass AFTER geometry

Appearances are applied in their own serialized pass, after all geometry exists. The builder leaves bodies default gray and gives them **descriptive names**; the appearance pass keywords off those names. Two real scripts: `apply_appearances.py` (plant-wide, by equipment function) and `lab_appearances.py` (the Z08 lab, finer). Methodology:

**Find a base appearance, then recolor a copy (matte).** Search the material libraries for a matte base by a priority list of names, copy it into the design (`des.appearances.addByCopy(base, "LAB_paint_236_237_239")`), then set its color by finding the `ColorProperty`:

```python
def set_color(appr, rgb):
    for pi in range(appr.appearanceProperties.count):
        p = appr.appearanceProperties.item(pi)
        if p.objectType == adsk.core.ColorProperty.classType():
            p.value = adsk.core.Color.create(rgb[0], rgb[1], rgb[2], 255); break
```

- **Matte, not glossy.** The first appearance attempt was glossy + glass and came out **too dark** (dark reflections). The lesson (logged in the session log): use a **matte** base (`Plastic - Matte (White)` / `Paint - Matte`) + a **bright palette**. Recolor from matte; avoid glossy/metallic bases for general recolor.

**Glass — Transparent Distance, NOT an opacity fraction.** Fusion glass clarity is controlled by a FloatProperty whose name contains "distance" ("Transparent Distance", in cm): **larger = clearer**, smaller = more tinted/absorbing. Frosting is a separate Roughness FloatProperty. There is no "opacity 0.3" slider — set the distance.

```python
def set_dist(appr, dist):
    for pi in range(appr.appearanceProperties.count):
        p = appr.appearanceProperties.item(pi)
        if p.objectType == adsk.core.FloatProperty.classType() and "distance" in p.name.lower():
            p.value = dist; break          # e.g. 50 = clear glassware; 4 = tinted amber reagent bottle
# frosted: find the "rough" FloatProperty and raise it (wall_transparency.py sets roughness 0.5)
```

  `wall_transparency.py` makes the building walls frosted see-through this way (tinted v1 transDist large, clearer v2 transDist=8) — driven by a tunable flag file so the orchestrator can iterate the value across passes without editing the script.

**Satin metal** — find a satin/stainless base (`Steel - Satin` / `Stainless Steel` / `Aluminum - Satin`) and apply it directly (no recolor) for sink/faucet/cart/furnace-stand.

**Keyword → material categorization.** Map a sub-component name (lowercased) to a category via an ordered keyword list — **first matching substring wins**, so order matters (put `mufflefurnace` before a generic `furnace`, `jetmill` before `mill`). `apply_appearances.py` maps to function categories (thermal/air/vessel/handling/electrical/lab/machinery/structure) with a palette; `lab_appearances.py` maps each lab element to (kind, rgb, transDist): white casework, dark epoxy worktops, black instruments, colored safety items, amber reagent bottles, glass glassware.

**Body-level overrides within an instrument.** A sub-component gets a base material, but specific bodies override by their descriptive name — `sash`/`shield`/`glass`/`window` → glass; `screen`/`monitor`/`display` → dark near-black. This is why descriptive body names (§3) are load-bearing:

```python
for b in sc.bRepBodies:
    bl = b.name.lower()
    if any(s in bl for s in ("sash", "shield", "glass", "window")):
        a = appr_for("glass", (215, 228, 232), 60.0)
    elif any(s in bl for s in ("screen", "monitor", "display")):
        a = appr_for("paint", (22, 26, 40), None)
    else:
        a = appr_for(kind, rgb, dist)
    b.appearance = a
```

- **Cache appearances** by (kind, rgb, dist) and reuse existing-by-name (`des.appearances.itemByName(nm) or addByCopy(...)`) so you don't create 400 duplicate appearances.
- **Per-instance overrides** (e.g. the 3 waste bins distinct by number) via a small dict keyed on the `_NN`.
- The appearance pass reports `{colored, byKind/byCat, errors, bases}` so you confirm coverage (real Z08 pass: 403 bodies, 0 errors).

---

## 10. Failure-mode catalog (each: symptom + prevention, from THIS build)

**(a) Read-back never written → agent hangs waiting on already-finished work.** *Symptom:* a dense Stage-3 script finishes building all geometry in Fusion, but the waiting agent never sees a read-back JSON (it arrived late / wasn't written) and hangs as if the build is still running. *Prevention:* write the read-back **robustly** (the `_write` try/except, written as the last act of `run`); for very long scripts, consider an early "started" marker. Critically, **the orchestrator must check Fusion state directly** (run `final_audit.py` / `audit_rooms.py`, count bodies) rather than trusting the wait — in the real incident the orchestrator stopped the dead agent, confirmed Fusion was responsive, and verified all 68 subs / 403 bodies had in fact built.

**(b) Loft-heavy scripts hang / are very slow.** *Symptom:* a stage with ~250 loft (`cone_z`) bodies runs slowly enough to look hung. *Prevention:* prefer extrude/stacked-cylinder tapers over loft where they read well enough; bound the loft count per script; split a dense stage into sub-batches; budget time for loft-heavy passes and don't interpret slowness as failure without checking body count.

**(c) cm/mm unit slips.** *Symptom:* a part comes out 10× too small/large (the real case: a stool seat built at cm-as-mm was 10× too small, fixed by `rebuild_stools.py`). *Prevention:* be explicit about which idiom a script uses — `createByString('… mm')` + `MM=0.1` coordinate scaling (the room builders) OR `createByReal` with **cm** numbers (the stool rebuild) — never mix them in one body. **Verify dimensions via the read-back bbox** (it reports mm); a 10× error is glaring there.

**(d) `ui.messageBox` hangs headless.** *Symptom:* any modal dialog blocks the MCP run forever. *Prevention:* never call `ui.messageBox` or any modal; all output goes to the read-back JSON.

**(e) Screenshot auto-reframes to the whole design.** *Symptom:* you screenshot to inspect the cabinet you just built and get a picture of the entire plant, because `viewport.fit()` / a bare `shot` reframes to everything. *Prevention:* isolate/focus first (explicit camera), then screenshot without re-fitting; and trust the bbox over the picture.

**(f) Containment "pokes" — wall-mounted / ceiling items.** *Symptom:* a clock, first-aid box, or exhaust riser is flagged out-of-bounds because it's mounted on/through a wall or rises to the ceiling. *Prevention:* the audit uses a small tolerance; genuinely wall-mounted items must sit just inside the envelope (the real Clock_01 was floating off the south wall at y=14030 and got repositioned onto the north wall inside the envelope). Treat a single cosmetic containment flag as a fix-it, not a build failure — but DO fix it.

**(g) Concurrent Fusion writers corrupt.** *Symptom:* two scripts writing geometry at once leave the design in a bad state (the API is single-threaded). *Prevention:* **serialize** — exactly one writer at a time; the orchestrator grants the write lock by spawning one writer, waiting + auditing, then the next. Spec/layout/draft work runs in parallel; only geometry writes are locked.

**(h) Nested-body bbox is component-local.** *Symptom:* a containment or camera-framing calc using a nested body's `boundingBox` is off by the room origin, because that bbox is in the room-local frame while you expected world. *Prevention:* for WORLD coordinates read the **occurrence's** `boundingBox` (carries the transform); for local geometry checks read the **body's** bbox and compare against the local envelope. `audit_rooms.py` compares local body bbox against the local room envelope (correct); `focus_sub.py`/`isolate.py` use the occurrence world bbox for camera framing (correct).

---

## 11. Orchestration for scale — many rooms

To replicate this fidelity across many rooms, pair with `[[skill-agent-orchestration]]`. The shape that worked for the 11-room example facility:

- **Per-room spec FIRST** (§5), drafted in parallel (non-write lane) while a writer works elsewhere.
- **Serialized writers (the write lock).** One geometry writer at a time; the orchestrator spawns a writer, waits for its read-back, **audits it** (§8), then releases the lock to the next. Build the FIRST room as a pattern-validation (the real build validated the into-component local-coord pattern on Z01 before batching the rest).
- **Batch by item-count.** Group rooms into small serialized batches (the example facility ran Batch A = Z02–Z04, B = Z05–Z07, C = Z08–Z11), one builder building sequentially per batch. Keep dense/loft-heavy rooms in their own batch.
- **Audit after every commit.** Containment + naming + param-count + "other rooms untouched," before the next writer. The orchestrator owns the audit (don't trust the writer's self-report).
- **Appearance pass AFTER all geometry** (§9), as its own serialized pass over the finished tree.
- **Principal/subordinate pattern** ([[skill-agent-orchestration]]): the brief grants the subordinate authority to build ONLY within its assigned room/zone, relative to the room origin, using only shared params, holding the write lock no longer than its task, reporting via the read-back JSON, and handing the lock back. Default-deny on everything else (never touch other rooms, never create params without approval, never run an appearance pass unless granted).

**Subordinate operating rules (paste into every room-builder brief):**

```
- Build ONLY within your assigned room/zone, into the Z##_<Room> component, in LOCAL coords
  relative to its origin. Stay inside the room envelope; no spill.
- Use ONLY the shared user parameters (pinned reference dims); create none without approval.
- One Fusion writer at a time — you hold the write lock; release it the moment your task is done.
- Each element is a named sub-component (Z##_<Room>_<Element>_NN) with descriptive body names
  (..._Door, ..._GlassSash, ..._Display) for the later appearance pass.
- Detail to the agreed tier: correct primitives at correct relative positions + the small
  identifying features. Declare any approximations (swept arcs, spheres, pipes) in the read-back notes.
- Report via the read-back JSON: subs created, bodies, allInside flag, params used, notes.
  Do NOT call ui.messageBox. Do NOT touch other rooms or run the appearance pass.
```

---

## 12. Scaling parallelism — parallel-generate, serial-commit

**The hard ceiling:** one Fusion app = one single-threaded API = **one geometry commit at a time**. Concurrent
`exec` calls corrupt state (Failure Mode (g)). You cannot parallelize the *commit*. But the commit is *seconds*;
the slow part is agent reasoning/authoring (*minutes*). So parallelize everything around the commit and shrink the
serial part to just the write. Built + tested 2026-06-05 (DECISIONS D-10); assets live under the project's `tools/`.

```
   N BUILDER AGENTS (parallel, NO Fusion) ──► queue/<AREA>.plan.py  ──► EXECUTOR (the ONE Fusion writer)
   each writes ONLY a pure-Python plan()        (a plan = AREA,          per plan: offline-validate ► assemble
   returning a geometry-op list; offline-        ROOM_OCC, INTERIOR,      plan()+canonical runtime ► exec ► audit
   validates its own plan before queueing        plan()->[ops])           read-back ► pass ✔ / bounce ✘
```

**The geometry-op IR (`tools/geom_ops.py`).** A plan is a list of plain-dict ops; each fully describes one body so it
can be (a) bbox-checked offline and (b) built by the canonical runtime. Ops (all LOCAL mm; 0,0 = room SW corner):
`box{sub,body,x,y,w,d,h,z0}` · `cyl{…cx,cy,dia,h,z0}` · `cone{…cx,cy,dia_bot,dia_top,h,z0}` ·
`ring{…cx,cy,r_out,r_in,z0,z1}` · `hcyl{…axis('x'|'y'),cx,cy,cz,dia,length}` · `leg{…cx,cy,ang,r_in,r_out,w_in,w_out,z0,z1}`.
Every `sub` starts with `AREA_`; every `body` starts with its `sub`.

**The plan-file contract** (a builder writes ONLY this — see `docs/plan_template.py`): module-level `AREA` (str),
`ROOM_OCC` (str, the existing room occurrence), `INTERIOR` (Lx,Wy,Lz mm), and `plan()` → `[ops]`. No `adsk`, no
Fusion knowledge — just geometry intent. This is what makes builders parallelizable and trivially validatable.

**Offline validation (`tools/validate_plan.py` → `validate_ops`).** Runs with no Fusion. Imports the plan, runs
`plan()`, and FAILS on: bad/unknown op, missing keys, containment violation (bbox outside `[0,Lx]×[0,Wy]×[0,Lz]`),
duplicate body name, `sub` not under `AREA`. WARNS on: body not prefixed by sub, a largest-dim < 3 mm or global
extent < 5 % of the room (**the cm/mm slip — caught here, before Fusion**), significant cross-sub overlap.

**The executor gateway (`tools/executor.py`).** The ONLY thing that touches Fusion. `executor.py <plan…>` or
`executor.py --queue` (drains `queue/*.plan.py` sorted). Per plan, **serially**: offline-validate → assemble
`plan_source + tools/buildlib_runtime.py` into `artifacts/scratch/` → `fusion_mcp.py exec` → audit the read-back
(`ok && allInside && bodies==expected`) → record pass/fail (bounce failures back to the builder with the trace).

**The canonical runtime (`tools/buildlib_runtime.py`).** Maintained + tested ONCE. Appended after a plan file at
exec time; reads the module globals + `plan()`, deletes this plan's sub-components (idempotent), builds each op
into its named sub-component via the op→builder dispatch, and writes a per-body LOCAL-bbox read-back with an
`allInside` flag. Builders never write this — the Fusion-API surface lives in exactly one tested place.

**Workflow for N rooms:** partition by **disjoint room component** (already conflict-free — see §3/§D-6). Spawn N
builder agents in parallel, each: load this skill + the room's spec → write `queue/<AREA>.plan.py` → run
`validate_plan.py` until clean → done (no Fusion). Then the orchestrator runs `executor.py --queue` once; it commits
every room serially and audits each. Net wall-clock ≈ max(builder time) + Σ(commit time), vs Σ(builder+commit) when
coupled — roughly an Nx speedup, capped by total commit time.

**ALWAYS e2e-test a new op type.** `tools/test_validate.py` covers the validator offline; `tools/_pipeline_test.plan.py`
exercises every op live and asserts each body's bbox matches its offline model to the mm. When this was first run it
caught two `hcyl` plane-axis SIGN bugs (yZ-plane sketch-X → **−**worldZ; xZ-plane sketch-Y → **−**worldZ) that no
offline check could find — the offline bbox model and the Fusion builder must agree, and only a live build proves it.

**Escalation tiers (not built — for beyond ~Nx):** Tier 2 — N Windows Fusion instances/VMs, each its own MCP port,
each builds a subset truly in parallel into its own doc; a final merge inserts the per-instance STEP/F3D exports
(true horizontal scaling, heavy setup). Tier 3 — generate per-room geometry with a headless parallel CAD kernel
(CadQuery/build123d/pythonOCC) → per-room STEP → one serial import+assemble into Fusion (massive parallelism, but
imported solids lose the parametric feature tree).

---

## 13. Quality-bar checklist + reusable assets + changelog

**"Done to comprehensive detail" checklist:**
- [ ] Every element is its own named sub-component (`Z##_Room_Element_NN`) with descriptive body names.
- [ ] Each object READS: correct primitives at correct relative positions + the identifying fine features (recessed panels w/ reveal gaps + handles + toe-kicks on casework; displays/knobs/status-lights/vents/feet on instruments; spouts/necks/lips/caps on glassware; 5-star base + foot-ring on stools; sash/airfoil/baffle/collar on the fume hood).
- [ ] Read-back JSON shows `ok:true`, expected `bodyCount`, `allInside:true` — and `notes` declare every approximation.
- [ ] Audit passes: containment (all inside envelope), naming (0 violations), param count unchanged (no rogue params), other rooms untouched.
- [ ] Transparent/screen elements left default in the build, then handled in the appearance pass (matte recolor + glass-by-transparent-distance + satin metal + body-level glass/screen overrides), 0 appearance errors.
- [ ] Inspected at least the tricky parts via isolate/focus + explicit camera (not just the auto-fit whole-plant screenshot).
- [ ] Stages idempotent (re-runnable); only one writer wrote at a time.

**Reusable assets (paths relative to the project root):**
- `tools/fusion_mcp.py` — the MCP client (`exec` / `read` / `shot` / `tools`).
- `scripts/util/rebuild_stools.py` — cleanest examples of offset-start extrude, `cyl`, `ring` (2-loop annulus), rotated-polygon `leg`.
- `scripts/rooms/Z08_stage{1,2,3}_*.py` — the canonical detailed build: casework helpers (`base_cabinet`, `base_cabinet_west`), instruments, glassware (`cone_z`, `reagent_bottle`, `gas_cyl`, `stool`).
- `scripts/util/apply_appearances.py`, `lab_appearances.py`, `wall_transparency.py` — the appearance methodology (matte recolor, glass transparent-distance, satin metal, keyword categorization, body-level overrides, flag-file tuning).
- `scripts/util/isolate.py`, `focus_sub.py`, `set_shell_visible.py` — visibility isolation + explicit-camera framing + the flag-file pattern.
- `scripts/rooms/audit_rooms.py`, `scripts/final_audit.py` — containment / naming / param / census verification.
- **Parallel pipeline (§12):** `tools/geom_ops.py` (op IR + bbox + `validate_ops`), `tools/validate_plan.py` (offline plan check), `tools/buildlib_runtime.py` (canonical op→Fusion runtime), `tools/executor.py` (serial commit gateway), `tools/test_validate.py` + `tools/_pipeline_test.plan.py` (the offline + live test suite), `docs/plan_template.py` (the plan a builder writes), `queue/` (drop `<AREA>.plan.py` here).
- `docs/rooms/Z08_showcase.md` — a model detailed-room spec; `docs/room_spec_template.md` — the spec template; `docs/scene_detail_spec.md` — the L1/L2/L3 tier definitions.
- `AGENTS.md` / `PLAN.md` / `DECISIONS.md` — the conventions, write-lock model, and decision history.

**Versioning + amendments.** Keep the front-matter `description` tightly aligned to "when to load" — that's the load gate. As new shape patterns, helpers, or failure modes appear, add them (shape vocabulary in §4, helpers in §7, failure modes in §10) with a date. Refactors welcome; don't let the description drift vague.

## Changelog

### 1.1.0 (2026-06-05)
- Added §12 "Scaling parallelism — parallel-generate, serial-commit": the geometry-op IR (box/cyl/cone/ring/hcyl/leg), the pure-Python `plan()` contract, offline `validate_ops` (catches the cm/mm slip + containment before Fusion), the `executor.py` serial-commit gateway + canonical `buildlib_runtime.py`, the N-room workflow, the e2e-test-every-op rule (two `hcyl` plane-axis sign bugs were caught this way), and the multi-instance / offline-kernel escalation tiers. Built + tested 2026-06-05 (DECISIONS D-10). (Old §12 → §13.)

### 1.0.0 (2026-06-05)
- Initial skill, synthesized from a showcase detailed-lab buildout (68 subs / 403 bodies) and the surrounding 11-room example industrial facility.
- Captures: the WSL→Fusion MCP runtime model (`def run(_context)`, cm-internal units, file read-back over the never-surfaced return value, no `ui.messageBox`); the into-component local-coord build pattern + `Z##_Room_Element_NN` naming + per-stage idempotency; the shape-decomposition vocabulary (casework / instruments / glassware / stools / fume hood / vessels / kiln / cyclone) with the L1/L2/L3 tiers; the plan-spec-then-staged-build workflow + spec template; paste-ready API helpers (plane-offset + offset-start extrude, `cyl`, `ring` annulus, `cone_z` loft, rotated-polygon `leg`, radial placement); the verification loop (bbox read-back + containment/naming/param audits + isolate/focus explicit-camera framing + screenshot caveats); the matte/glass/metal appearance pass (transparent-distance not opacity, keyword categorization, body-level overrides); and the 8-entry failure-mode catalog (read-back-never-written false hang, loft slowness, cm/mm slips, modal hang, screenshot auto-reframe, wall-mount containment pokes, concurrent-writer corruption, local-vs-world bbox).
- Cross-links `[[skill-agent-orchestration]]` for multi-room scale-out and `[[reference-fusion-mcp-wsl]]` for the connection method.
```