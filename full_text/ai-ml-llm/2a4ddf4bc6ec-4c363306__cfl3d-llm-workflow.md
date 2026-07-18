---
name: "cfl3d-llm-workflow"
description: "Project-specific CFL3D_GPT workflow skill for running airfoil CFD cases through an LLM terminal. Use when the user wants DeepSeek or another OpenAI-compatible model to collect Mach, Reynolds number, angle of attack, airfoil source, mesh options, run CFL3D, automatically diagnose and repair failures, reuse restarts for alpha sweeps, and postprocess final results."
---

# CFL3D LLM Workflow

Use this skill to operate `<repository-root>` as an LLM-guided CFL3D airfoil computation system. The goal is not code review; the goal is to turn a user's natural-language CFD request into commands, runs, diagnosis, repair, and final result files.

## First-Time Setup On This Machine

Before any CFD work, confirm the two native programs (CFL3D solver and
Construct2D) are built for this machine. This is step 0 when following this
skill on a freshly unpacked copy.

1. Run a check:

   ```bash
   python -m cfl3d_agent doctor
   ```

2. If `doctor` reports `cfl3d solver: not found` or `construct2d: not found`, or
   a solver shows `starts=False`, install/compile before continuing:

   ```bash
   ./install.sh          # macOS / Linux
   ```

   ```powershell
   .\install.ps1         # Windows  (or double-click install.bat)
   ```

   The installer detects the toolchain, compiles both programs from source via
   `tools/bootstrap.py`, and writes `configs/local_env.json` (resolved Python +
   binary paths). On Windows the package also ships prebuilt binaries under
   `dist\`, so the agent can run even before a local rebuild. See `INSTALL.md`
   and `docs/MIGRATION_CROSS_PLATFORM.md`.

3. Re-run `python -m cfl3d_agent doctor` and only proceed once both binaries are
   present and start. Drive every command with the Python that `doctor` reports
   under `recommended python`.
## Default Environment

```powershell
cd <repository-root>
# $PY is environment-specific: set it to your own Python interpreter (or
# just "python" if cfl3d_agent is importable on PATH). Run
# `& $PY -m cfl3d_agent doctor` to confirm the interpreter and solver.
$PY = "python"   # example path; change for your machine
```

Use `& $PY -m cfl3d_agent ...` for project commands.

## Windows MPI CFL3D Packaged Skill Path

Use this section when the user asks for `cfl3d_mpi.exe`, 8-core MPI CFL3D,
`<origin-case-dir>`, Windows migration, or a packaged executable workflow.
This skill now carries a validated Windows MPI payload under:

```text
.codex\skills\cfl3d-llm-workflow\assets\windows\bin\cfl3d_mpi.exe
.codex\skills\cfl3d-llm-workflow\assets\windows\bin\cfl3d_mpi_workflow.exe
.codex\skills\cfl3d-llm-workflow\assets\windows\tools\cfl3d_mpi_workflow.py
.codex\skills\cfl3d-llm-workflow\assets\windows\runtime\*.dll
.codex\skills\cfl3d-llm-workflow\references\CFL3D_MPI_WINDOWS_MIGRATION.md
```

The packaged solver is the no-redirect MPI build. It was built from
`solver\CFL3D-master\CFL3D-master\CFL3D-master` with:

```text
BUILD_MPI=ON
USE_CGNS=OFF
BUILD_CMPLX=OFF
USE_NO_REDIRECT=ON
CMAKE generator: Ninja
Fortran compiler: <msys2-root>\ucrt64\bin\gfortran.exe
MPI: <mpich2-root> using mpif.h, libfmpich2g.a, libmpi.a
```

The workflow executable is a PyInstaller package of the Python program. It can:

- confirm or rebuild `cfl3d_mpi.exe`;
- copy `<origin-case-dir>` into a run directory without modifying the source;
- detect the origin `project1.x` as little-endian Fortran unformatted Plot3D;
- preserve the 4-byte integer records and convert 8-byte double coordinate
  records to big-endian;
- rewrite only the run-directory `cfl3d.inp` to use `project1_big.x`;
- launch MPICH2 with `mpiexec -n 8 -localroot`;
- write `prepare_summary.json` and `run_summary.json` diagnostics.

Use `-localroot` with MPICH2 on this Windows machine; without it, MPICH2 may
prompt for Windows credentials or hang. `smpd` alone in the process list is
normal. Kill only stale `mpiexec` or `cfl3d_mpi` processes from failed tests.

Quick validated local smoke command:

```powershell
$Root = "<repository-root>"
$Origin = "<origin-case-dir>"
$Skill = Join-Path $Root ".codex\skills\cfl3d-llm-workflow"
$Bin = Join-Path $Skill "assets\windows\bin"
$Runtime = Join-Path $Skill "assets\windows\runtime"
$env:CFL3D_GPT_ROOT = $Root
$env:PATH = "$Runtime;$Bin;<mpich2-root>\bin;$env:PATH"
Set-Location $Root
& "$Bin\cfl3d_mpi_workflow.exe" all --origin $Origin --run-dir "$Root\runs\mpi_origin_8core_skill" --cores 8 --timeout 180
```

For a full production-style run, use `--timeout 0`. The origin case can run for
more than an hour; a 180-second smoke test is only proof that MPI, grid reading,
byte-order conversion, and solver startup work. Treat success as stronger when
`project1.out` reaches residual/flux computation, `restart.bin` is nonzero, and
`cfl3d.error` is empty.

For migration to another Windows computer, read the full command checklist in:

```text
.codex\skills\cfl3d-llm-workflow\references\CFL3D_MPI_WINDOWS_MIGRATION.md
```

The target Windows machine still needs MPICH2 installed for `mpiexec.exe` and
`smpd.exe`. The skill assets include the validated solver and required runtime
DLLs, but they do not replace MPICH2 service installation.
## Cycle Defaults

Unless the user explicitly requests a different iteration count, keep the
project defaults:

```text
Multigrid enabled:      level 2 = 1000, level 3 = 1000, level 4 = 3000
Multigrid disabled:     finest-grid single-level = 5000
```

Do not add `--ncyc 1000` by habit. Omit `--ncyc` for normal production-style
runs so the renderer writes the multigrid schedule above. Add `--ncyc N` only
when the user asks for a smoke test, a short debug run, or a specific cycle
count. When `--disable-multigrid` or `--restart-from` is used and no cycle count
is specified, the agent uses `5000` cycles.

## Operating Rule

Prefer the natural-language terminal for user-facing work, but do not make the user wait on LLM setup for basic validation. `chat --text` can parse common Chinese/English airfoil requests with local heuristic rules when `configs\llm.yaml`, the API key, or the provider call is unavailable. In that case, continue with dry-run, prompting, case preparation, diagnosis, and postprocessing where possible, and record the LLM problem as a warning instead of treating it as the whole workflow failure.

For automation, `chat --text` is non-interactive by default: if Mach, Reynolds number, alpha, airfoil source, grid, or auto-mesh intent is missing, return a structured error instead of waiting for keyboard input. Use `--interactive-fill` only when a human is at the terminal and wants the agent to ask follow-up questions.

Natural-language requests such as `我想要做naca2412的马赫数是0.5，雷诺数3e6的7-9的迎角序列` are incomplete unless they also say either `自动网格` or provide an existing `.p3d/.bin` grid. Treat `7-9的迎角序列` as `[7, 8, 9]` when no step is given, but still require a mesh source.

When `--auto-mesh` is enabled, use the bundled Windows Construct2D executable by default:

```text
.\dist\construct2d_windows\bin\construct2d.exe
```

Do not require the user to type `--construct2d` unless `doctor` cannot find the bundled executable or they want to override it.

## Mesh Topology Rules

For automatic meshing, start with O-grid unless the user explicitly asks for
C-grid. The command-line flag is:

```powershell
--grid-topology ogrid
```

or, to force C-grid from the beginning:

```powershell
--grid-topology cgrid
```

The project now has separate CFL3D input templates for the two topologies:

```text
input_template\input_template_ogrid.inp
input_template\input_template_cgrid.inp
```

Do not reuse the old single-template assumption for Construct2D meshes. The
agent selects the matching template automatically when `--template` is omitted
or points to the default template.

If a user gives an automatic-mesh point count such as `300`, treat it as a
user-facing request, not as the exact internal count. Convert `jmax`, `nsrf`,
or natural-language `mesh_points` to the next `4n+1` value before Construct2D.
Examples: `200 -> 201`, `241 -> 241`, `300 -> 301`. The normalized values are
recorded in `manifest.json` under `mesh.normalized_points`.

If CFL3D or PRECFL3D rejects an O-grid due to grid quality or input consistency,
the workflow must switch to C-grid automatically once. The trigger includes
diagnostic code `ogrid_rejected_by_cfl3d`, `precfl3d` messages such as `jend is
out of range`, grid rejection, negative Jacobian, bad grid quality, or a failed
input check after an O-grid auto mesh. The fallback disables restart for the
rerun, regenerates the mesh as C-grid, uses `input_template_cgrid.inp`, and
records the change in `auto_result.json.mesh_switches`.

Use `--no-auto-switch-cgrid` only when the user explicitly wants to debug the
O-grid itself. Otherwise leave automatic O-grid to C-grid fallback enabled.

## Intake

Collect missing case settings before running:

- Airfoil source: user `.dat`, local UIUC-like archive name, NACA 4-digit airfoil, or existing case.
- Mesh source: existing `.p3d`/`.bin`, or `--auto-mesh` with Construct2D.
- Flow settings: Mach number, Reynolds number, angle of attack, optional cycle count, timeout.
- Run mode: dry run, single real run, auto repair loop, batch, or continuous alpha sweep.
- LLM provider: `deepseek`, `openai`, `qwen`, or `local_command`.

If the user asks for continuous alpha, 连续迎角, or 迎角序列, use `sweep alpha`; from the second alpha onward, require restart reuse from the previous alpha unless the user explicitly disables it.

For automatic-mesh alpha sweeps, restart chaining may expose a CFL3D multigrid/restart
level mismatch. If CFL3D writes `stopping.inconsistent restart grid indices` while the
process exit code is still `0`, treat the case as failed, not completed. The rule-based
diagnostic code is `restart_grid_indices_inconsistent`; the safe first repair is
`disable_multigrid`, then rerun the same case while keeping restart enabled.

## Airfoil Source Rules

When the user gives an airfoil name or says "search the airfoil library", resolve
the geometry in this order:

1. User-provided coordinate file: use `--dat path\to\airfoil.dat`.
2. NACA 4-digit airfoil: use `--airfoil naca2412`, or write a reproducible file
   with `naca naca2412 --output airfoils\naca2412.dat`.
3. Project local archive: run `resolve-airfoil name --output airfoils\name.dat
   --json`. The current local archives are
   `code\coord-trans-encoding-main\mesh_generation\gen_airfoils_TEST.tar.gz`
   and `code\coord-trans-encoding-main\mesh_generation\gen_airfoils.tar.gz`.
4. Online coordinate libraries, if local search fails and network/manual download
   is available. Common sources to tell the user about are:
   `https://m-selig.ae.illinois.edu/ads/coord_database.html` for the UIUC/Selig
   coordinate database, `http://airfoiltools.com/` for search and NACA pages, and
   `https://bigfoil.com/` for a broad searchable airfoil database.
5. XFOIL processing: use the local `XFOIL\xfoil.exe` and project wrapper scripts
   to repanel or modify a known `.dat`; do not use XFOIL to invent an arbitrary
   non-NACA airfoil from only a name.

Do not invent airfoil coordinates. If `resolve-airfoil s1223` fails and no local
or user `.dat` exists, ask the user to provide a `.dat` file or download one from
a coordinate database. After a coordinate file is obtained, save it under a stable
local path such as `airfoils\s1223.dat` so batch runs are reproducible and do not
depend on a website staying available.

Useful source commands:

```powershell
New-Item -ItemType Directory -Force airfoils
& $PY -m cfl3d_agent naca naca2412 --output airfoils\naca2412.dat
& $PY -m cfl3d_agent resolve-airfoil s1223 --output airfoils\s1223.dat --json
& $PY .\XFOIL\xfoil_repanel_tool.py airfoils\s1223.dat --check-only --json
& $PY .\XFOIL\xfoil_repanel_tool.py airfoils\s1223.dat -o airfoils\s1223_repanel241.dat --target-points 241 --min-points 200 --max-points 300 --xfoil .\XFOIL\xfoil.exe --force --json
& $PY .\XFOIL\xfoil_thickness_tool.py airfoils\naca2412.dat -o airfoils\naca2412_t14.dat --target-thickness 0.14 --xfoil .\XFOIL\xfoil.exe
```

For natural-language LLM operation, translate source phrases as follows:

| User phrase | Action |
| --- | --- |
| "我有 dat 文件" | Ask for or use the path, then pass `--dat`. |
| "NACA2412" | Use `--airfoil naca2412`; optionally generate `airfoils\naca2412.dat` for auditing. |
| "S1223 / MH114 / UIUC 里面的翼型" | First run `resolve-airfoil`; if missing, ask for a `.dat` or tell the user to download it from UIUC/Selig or Airfoil Tools. |
| "本地搜索" | Search local `.dat` files and the project archive, then save the resolved coordinate file to `airfoils\`. |
| "点太少 / 网格生成失败" | Run the XFOIL repanel check and target 241 points before meshing. |

## Known Error Playbook

When a run fails, first read `report.json`, `solver_stdout.txt`, `cfl3d.error`,
`cfl3d.out`, `precfl3d.error`, `precfl3d.out`, `manifest.json`, and
`post\postprocess_report.json` if it exists. Do not judge success from the process
exit code alone; CFL3D can return `0` while writing an internal error check to logs.

Use this project-specific triage table before asking the user to debug manually:

| Symptom or diagnostic code | Likely cause | First action |
| --- | --- | --- |
| `missing_fields: grid or auto_mesh` | Request gave airfoil and flow conditions but no mesh source. | Ask for `自动网格` or an existing `.p3d/.bin` grid path. |
| `mesh_required` | Case was prepared without a CFL3D Plot3D grid. | Provide `--grid` or rerun with `--auto-mesh`. |
| Construct2D not found | Auto-mesh requested but mesher path was missing. | Use bundled `dist\construct2d_windows\bin\construct2d.exe`; do not require `--construct2d` unless overriding. |
| Airfoil point count outside 200-300 | `.dat` surface coordinates are too sparse or too dense for robust meshing. | Run `XFOIL\xfoil_repanel_tool.py` to repanel toward 241 points before Construct2D. |
| User asks for mesh point count like `300` | Construct2D/CFL3D surface counts should be `4n+1`. | Pass the user count through `mesh_points`, `--jmax`, or `--nsrf`; the agent normalizes `300 -> 301` automatically. |
| `grid data file inconsistency`, wrong `IDIM/JDIM/KDIM`, or template still says `2 129 129` | CFL3D input dimensions do not match generated `.bin` grid. | Read Plot3D `.bin` dimensions and rewrite the CFL3D dimension block. |
| `ogrid_rejected_by_cfl3d`, `jend is out of range`, negative Jacobian, or bad O-grid quality | CFL3D/PRECFL3D rejected the generated O-grid. | Keep `--auto-mesh`, switch to C-grid once, use `input_template_cgrid.inp`, and rerun without restart. |
| O-grid boundary still uses old `J=25..105` wall segment | Construct2D O-grid is being run with old C-grid-like template ranges. | Apply Construct2D O-grid boundary rewrite before running CFL3D. |
| `ogrid_one_to_one_missing` or `ogrid_periodic_boundary_missing` | Full-face O-grid wall is present, but the closing seam between `J=1` and `J=JDIM` is missing or incomplete. | Stop before CFL3D. Regenerate/rewrite O-grid input so `J0/JDIM` are `BCTYPE=0` and 1-1 blocking spans `I=1..IDIM, K=1..KDIM`. |
| `airfoil_wall_missing` | No `BCTYPE=2004` wall segment was parsed from `cfl3d.inp`. | Inspect `K0/J0/...` boundary tables; for Construct2D O-grid regenerate/rewrite boundaries. |
| `airfoil_wall_zero_range` | A parsed airfoil wall has a zero index range, usually C-grid `K0 BCTYPE=2004` with `ISTA/IEND=0/0`. | Treat the case as failed. Preserve or restore `grid_topology=cgrid`, rewrite C-grid boundaries, and rerun in a new case directory. |
| `cgrid_boundary_rewrite_skipped` | C-grid template placeholder ranges survived into `cfl3d.inp`, commonly because an existing-grid or restart path changed `grid_topology` to `unknown`. | Do not trust forces from this run. Rerun with C-grid topology preserved and verify `K0 BCTYPE=2004` is `ISTA=1, IEND=IDIM, JSTA=wall_start, JEND=wall_end`. |
| `cgrid_outer_boundary_bctype_mismatch` | C-grid `K0` wall may be present, but outer-boundary BCTYPE values are not consistent with the NASA CFL3D C-grid pattern, commonly `J0/JDIM=1003` from an old template. | Treat the case as failed. Rerender in a new C-grid case and verify `I0=1001`, `IDIM=1002`, `J0=1002`, `JDIM=1002`, `KDIM=1003`. |
| `cgrid_outer_boundary_missing` | The C-grid template is missing one of the outer boundary tables, so the renderer cannot safely rewrite that face. | Stop before CFL3D. Use `input_template_cgrid.inp` or `input_template_cgrid_lowmach.inp` and rerun preflight. |
| `cgrid_topology_metadata_unknown` | The current `cfl3d.inp` wall is valid, but `manifest.json` still says `grid_topology=unknown` while a C-grid template was used. | Treat current input as usable after `check-input`, but do not use this directory as a restart source unless you rerun/regenerate it with `grid_topology=cgrid` recorded. |
| `airfoil_wall_incomplete_coverage` | The airfoil wall exists but does not span the full expected boundary range. | For Construct2D O-grid, ensure `K0` wall covers `ISTA=1..IDIM` and `JSTA=1..JDIM`. |
| `airfoil_wall_range_out_of_bounds` | Wall segment indices exceed parsed block dimensions. | Regenerate/rewrite `cfl3d.inp`; do not run CFL3D until boundary ranges match dimensions. |
| `control_surface_not_matching_wall` | Force-integration control surface does not match the wall segment. | Rewrite `CONTROL SURFACE` so force/moment integration covers the full airfoil wall. |
| `plot3d_output_not_gridpoint` | `PLOT3D OUTPUT` uses `IPTYPE!=0`, usually `IPTYPE=1`, causing CFL3D to write cell-centered Plot3D files. | Treat as an input failure. Set `IPTYPE=0`, rerun CFL3D, then rerun rich post-processing. Editing only `cfl3d.inp` does not fix old `plot3dg.bin/plot3dq.bin`. |
| Fortran `Bad integer for item ...` | Long O-grid boundary rows were formatted too wide for CFL3D fixed-column input. | Use compact integer field widths for O-grid boundary rows. |
| `precfl3d_error` with `cannot create coarser level` or `multigrid_level_error` | Grid dimensions are incompatible with requested multigrid coarsening. | Apply policy-approved `disable_multigrid`, then rerun. |
| `stopping.inconsistent restart grid indices` or `restart_grid_indices_inconsistent` | Restart file is being read at an incompatible multigrid level during an alpha sweep. | Keep restart enabled, apply `disable_multigrid`, then rerun the same alpha. |
| User asks to continue from a finished case's `restart.bin` | The CLI now supports explicit restart continuation. | Run `auto run --restart-from runs\old_case\restart.bin --ncyc N`; use a new case directory and keep multigrid disabled. |
| `restart_without_file` | Restart was requested but no usable `restart.bin` exists. | For a single case, apply `disable_restart`; for a sweep, diagnose the previous alpha unless user explicitly asked for cold starts. |
| `grid_binary_format` or text like `grid file contains ... grids` | CFL3D misread Plot3D binary header, byte order, or record markers. | Reconvert original ASCII `.p3d` to CFL3D `.bin` with the project converter. |
| `windows_runtime_missing` / exit `3221225781` | Solver DLL/runtime cannot be loaded on Windows. | Run `doctor`; use the portable UCRT solver path or fix MSYS2 runtime PATH. |
| `solver_cpu_incompatible` | Selected solver binary was compiled for unsupported CPU instructions. | Use the locally built portable solver. |
| `missing_output` or empty `cfl3d.out` | Solver did not start or stopped before writing normal output. | Inspect `solver_stdout.txt`, `cfl3d.error`, paths, and runtime setup. |
| `residual_increased` | Solver ran but residual trend worsened. | Do not claim convergence; inspect grid quality, CFL/time step, cycle count, and turbulence settings. |
| High-subsonic/transonic request with `Mach > 0.7` | Entropy correction should be enabled for this project workflow. | Ensure the keyword-driven input section contains `epsa_r 0.3`; the case renderer adds it automatically when `mach > 0.7`. |
| Postprocess product failure | Solver files needed for force/Cp/Mach products are absent or malformed. | Open `post\postprocess_report.json`; report generated outputs exactly and do not invent missing plots. |
| LLM provider API key missing | LLM setup is incomplete, but heuristic parser can still run basic requests. | Record planner warning, continue local workflow, and ask user to set the provider API key only when LLM diagnosis is required. |

Repair actions must remain policy-gated. Current safe actions include
`disable_restart`, `disable_multigrid`, and `reconvert_grid`. Do not let an LLM
perform arbitrary solver binary changes, broad filesystem edits, or unreviewed
Fortran/source modifications.

## C-grid Boundary Preflight

For C-grid cases, `check-input` now parses all `K0` boundary segments, not just
the first row. A valid Construct2D C-grid airfoil wall should appear as the
middle `K0` segment:

```text
BCTYPE=2004, ISTA=1, IEND=IDIM, JSTA=wall_start, JEND=wall_end
```

For the common `IDIM=2, JDIM=129, NWKE=24` setup, this means:

```text
K0 segment 2: BCTYPE=2004, ISTA=1, IEND=2, JSTA=25, JEND=105
```

The outer boundary BCTYPE pattern must also match the NASA CFL3D NACA4412
C-grid standard case:

```text
I0   = 1001
IDIM = 1002
J0   = 1002
JDIM = 1002
KDIM = 1003
```

Do not accept an old C-grid input where `J0/JDIM` are `1003`, even when the
`K0` wall and control surface look aligned. The C-grid outer boundary type is
still wrong, and `check-input` correctly fails such input with
`cgrid_outer_boundary_bctype_mismatch`.

If `check-input` reports `airfoil_wall_zero_range`, especially `ISTA/IEND=0/0`,
the run is invalid even if CFL3D exited with code 0 and wrote residuals. This
usually means the C-grid boundary rewrite did not run after an existing
`grid.bin` or `--restart-from` path lost `grid_topology=cgrid`. Recreate the
case with C-grid topology preserved and verify the input before using force or
postprocessing outputs.

If `check-input` reports `cgrid_outer_boundary_bctype_mismatch`, the run is also
invalid even when residuals and `restart.bin` exist. Recreate the case in a new
directory with `--grid-topology cgrid`; do not patch the old result directory by
hand unless you are doing a controlled debug run.

In the standard LLM/agent workflow, incomplete C-grid wall or outer-boundary
inputs should no longer reach CFL3D. They can still exist in old directories,
hand-edited templates, runs launched by calling CFL3D directly, or cases where
the user bypasses `check-input`. Treat any of the following as a hard stop before
solver execution: `airfoil_wall_missing`, `airfoil_wall_zero_range`,
`airfoil_wall_incomplete_coverage`, `airfoil_wall_range_out_of_bounds`,
`control_surface_not_matching_wall`, `cgrid_outer_boundary_bctype_mismatch`, and
`cgrid_outer_boundary_missing`. A C-grid is not acceptable just because the `K0`
wall range looks right; `J0/JDIM=1002`, `KDIM=1003`, and a matching
`CONTROL SURFACE` are also required.

Current program behavior preserves explicit `--grid-topology cgrid` even for
existing `--grid` and `--restart-from` cases. If `--restart-from` points to a
source case whose `manifest.json` records `grid_topology: "cgrid"`, the
continuation inherits C-grid topology even when the user omits
`--grid-topology`. If the source manifest still says `unknown`, pass
`--grid-topology cgrid` explicitly or regenerate from a corrected source case.

If an existing case has a valid `K0` wall range (for example `I=1..2,
J=25..105`) but `J0/JDIM` are still `1003`, `check-input` fails it with
`cgrid_outer_boundary_bctype_mismatch`. Do not trust that directory's forces as
final data, and do not chain future restart cases from that metadata without
regenerating a new C-grid case with explicit `--grid-topology cgrid`.

Dry-run alpha sweeps may continue creating all requested case directories after
an input-check failure so users can inspect every prepared input. Real solver
runs must stop on failed input preflight. The current `auto run` and legacy
`run` paths block before starting CFL3D when `check-input` returns `failed`,
except that an automatic O-grid preflight failure may trigger the one-time
O-grid to C-grid fallback first.

## CFL3D Turbulence Model Handling

Use this section when the user asks for a different turbulence model. CFL3D
switches viscous/turbulence modeling through the input-file LT7 row labeled
`NCG IEM IADVANCE IFORCE IVISC(I) IVISC(J) IVISC(K)`. In this project that row
is currently inherited from
`code\coord-trans-encoding-main\BASIC_simulations\input_template.inp` and is not
exposed as a CLI flag. Do not invent commands such as `--turbulence-model sa`
unless the project later implements them. To change the model today, edit or
generate the CFL3D input template/input file and then rerun preflight.

NASA's CFL3D Version 5 manual defines `ivisc(m)` on LT7 as the
viscous/inviscid surface flag, with `m = i, j, k`. The CFL3D Version 6 New
Features page states that `ivisc` controls the turbulence-model choice and
updates the model list for V6. Use the V5 input-parameter rules together with
the V6 model table.

Core `ivisc` choices to recognize:

| `ivisc` | Model / mode |
| --- | --- |
| `0` | Inviscid |
| `1` | Laminar |
| `2` | Baldwin-Lomax, not recommended for general multi-zone work |
| `3` | Baldwin-Lomax with Degani-Schiff, not recommended for general multi-zone work |
| `4` | Baldwin-Barth, not recommended in current V6 guidance |
| `5` | Spalart-Allmaras |
| `6` | Wilcox k-omega |
| `7` | Menter SST k-omega |
| `8` | Linear version of V6 EASM k-omega model #14, not recommended as a final model |
| `9` | Linear version of V6 EASM k-epsilon model #13, not recommended as a final model |
| `10` | Abid k-epsilon |
| `11` | Nonlinear Gatski-Speziale EASM k-epsilon, not recommended |
| `12` | Nonlinear Gatski-Speziale EASM k-omega, not recommended |
| `13` | Nonlinear EASM k-epsilon |
| `14` | Nonlinear EASM k-omega |
| `15` | k-enstrophy |
| `16` | k-kL-MEAH2015 |

Practical project defaults and cautions:

- The current stock airfoil template uses `IVISC(I)=0`, `IVISC(J)=5`,
  `IVISC(K)=5`, which corresponds to inviscid i-direction and Spalart-Allmaras
  in the j/k directions for the 2-D extruded airfoil setup.
- If the user asks for SST, use `IVISC(J)=7` and `IVISC(K)=7`; if they ask for
  SA or Spalart-Allmaras, use `5`; if they ask for laminar, use `1`; if they ask
  for inviscid/Euler, use `0` and warn that viscous/turbulent drag is not a
  turbulent RANS result.
- For 2-D airfoil cases with `IDIM=2`, keep `IVISC(I)=0` unless there is a
  specific 3-D/full-Navier-Stokes reason to include i-direction viscous terms.
- Negative `ivisc` values enable wall functions in CFL3D, but NASA guidance says
  this should only be used for attached flow and is not recommended in general,
  especially for separated flows.
- For turbulence models, NASA guidance recommends near-wall spacing giving
  roughly `y+` of order 1; CFL3D prints `YPLUS STATISTICS` near the bottom of
  `cfl3d.out`. Check those statistics before trusting force coefficients.
- Some k-epsilon and k-enstrophy variants may fail to become turbulent on their
  own. If logs or `vist3d`/eddy-viscosity outputs show no sustained turbulence,
  do not claim a valid turbulent result; consider restart from a converged model
  or appropriate turbulence initialization/tripping.
- In restart sweeps, changing turbulence model between alphas is unsafe because
  restart variables may no longer be compatible. Keep the same model across the
  sweep, or cold-start a new sweep with an explicit case prefix.

Manual template edit examples, shown as input-file rows, not CLI flags:

```text
       NCG       IEM  IADVANCE    IFORCE  IVISC(I)  IVISC(J)  IVISC(K)
         3         0         0         1         0         5         5   <- current default SA in J/K
         3         0         0         1         0         7         7   <- SST in J/K
         3         0         0         1         0         1         1   <- laminar in J/K
         3         0         0         1         0         0         0   <- inviscid
```

After editing the template or prepared input, verify with:

```powershell
& $PY -m cfl3d_agent check-input runs\case_name\cfl3d.inp --json
```

Sources checked for this section: NASA CFL3D Version 5 Manual, Chapter 3
Input Parameters, LT7; NASA CFL3D Version 6.7 home page; NASA CFL3D Version 6
New Features, Turbulence Model Descriptions.

## Preflight

Before any real run:

```powershell
& $PY -m cfl3d_agent doctor
& $PY -m cfl3d_agent llm list --config configs\llm.yaml
& $PY -m cfl3d_agent llm ping --provider deepseek --config configs\llm.yaml
```

For `Mach > 0.7`, the case renderer automatically inserts the CFL3D keyword
`epsa_r 0.3` before `<-- end keyword-driven input section` if it is not already
present. Do not add duplicate `epsa_r` lines. When debugging high-Mach cases,
check the rendered `cfl3d.inp` keyword section and confirm this line is present.

## Mesh And Airfoil Point Self-Check

Before generating a new CFL3D mesh from a `.dat` airfoil, check the airfoil
surface coordinate count. Treat 200-300 coordinate points as the acceptable
range, with 241 points as the default target. This is a surface-coordinate
precheck for mesh generation; do not claim that XFOIL directly refines an
existing CFL3D Plot3D volume grid.

Use this check command for any user `.dat`, resolved UIUC/local archive airfoil,
or generated NACA `.dat` before `--auto-mesh`:

```powershell
& $PY .\XFOIL\xfoil_repanel_tool.py `
  runs\case_name\airfoil.dat `
  --check-only `
  --json
```

If `input_points` is below 200 or above 300, repanel with XFOIL before calling
Construct2D:

```powershell
& $PY .\XFOIL\xfoil_repanel_tool.py `
  runs\case_name\airfoil.dat `
  -o runs\case_name\airfoil_repanel241.dat `
  --target-points 241 `
  --min-points 200 `
  --max-points 300 `
  --xfoil .\XFOIL\xfoil.exe `
  --json
```

Then use the repaneled `.dat` as the source for meshing:

```powershell
& $PY -m cfl3d_agent auto run `
  --case case_name `
  --dat runs\case_name\airfoil_repanel241.dat `
  --mach 0.2 `
  --alpha 2.0 `
  --re 1500000 `
  --auto-mesh `
  --construct2d .\dist\construct2d_windows\bin\construct2d.exe `
  --non-interactive
```

For Construct2D grid-control counts, keep the user's intent but normalize to
`4n+1`. Example: if the user says `网格点数 300`, the natural-language plan may
contain `mesh_points=300`, but the generated `grid_options.in` must use
`jmax=301` and `nsrf=301`. Direct CLI example:

```powershell
& $PY -m cfl3d_agent auto run `
  --case naca2412_m05_re3e6_a7_points300 `
  --airfoil naca2412 `
  --mach 0.5 `
  --alpha 7 `
  --re 3e6 `
  --auto-mesh `
  --grid-topology ogrid `
  --jmax 300 `
  --nsrf 300 `
  --non-interactive `
  --json
```

After the run is prepared, verify normalization and topology:

```powershell
Get-Content runs\naca2412_m05_re3e6_a7_points300\manifest.json
Get-Content runs\naca2412_m05_re3e6_a7_points300\mesh\grid_options.in
& $PY -m cfl3d_agent check-input runs\naca2412_m05_re3e6_a7_points300\cfl3d.inp --json
```

Expected manifest fields include `grid_topology: "ogrid"` or `"cgrid"` and
`mesh.normalized_points.jmax/nsrf` equal to the internal `4n+1` values.

If the user supplied an existing `.p3d` or `.bin` grid, inspect
`manifest.json.grid_dimensions` after case preparation and report the dimensions,
but do not use XFOIL to modify that existing volume grid. If the existing grid is
too coarse or inconsistent, ask to regenerate the mesh from a checked `.dat`
source or use the auto-mesh path above.

For Construct2D-generated O-grids, verify that the prepared CFL3D input matches
the generated grid dimensions and boundary ranges. Typical automatic NACA2412
smoke dimensions are `idim=2, jdim=81, kdim=129`; the input must not keep the
old template's fixed `2 129 129` dimensions or `J=25..105` wall segment.

Always run the input self-check before a real solver run when a mesh or template
has changed. The check now verifies both multigrid dimensions and whether the
`BCTYPE=2004` airfoil wall boundary plus `CONTROL SURFACE` cover the full
expected airfoil boundary:

```powershell
& $PY -m cfl3d_agent check-input runs\case_name\cfl3d.inp --json
```

For Construct2D O-grids, a valid automatic input should have a `K0` wall segment
covering `ISTA=1..IDIM` and `JSTA=1..JDIM`, and a matching control surface on
`K=1`. If the check reports incomplete wall coverage, do not trust CL/CD/CM
because CFL3D may compute forces on only part of the airfoil.

The O-grid closing seam is also mandatory. `J0` and `JDIM` should be represented
as `BCTYPE=0` 1-1 interfaces, with `1-1 BLOCKING DATA` joining `J=1` to
`J=JDIM` over `I=1..IDIM` and `K=1..KDIM`. If `check-input` reports
`ogrid_one_to_one_missing` or `ogrid_periodic_boundary_missing`, stop before
CFL3D and regenerate or rewrite the input.

For all O-grid and C-grid templates used by this agent, `PLOT3D OUTPUT` must use
`IPTYPE=0`. CFL3D source comments define `IPTYPE=0` as q output at grid points
and `IPTYPE=1` as q output at cell centers. With `IPTYPE=1`, `plot3dg.bin` and
`plot3dq.bin` are one point smaller in each active direction, so Mach/Cp clouds
and Tecplot flowfield files can look like the wall boundary is shifted or
incomplete even when the boundary conditions are correct. `check-input` now
fails such cases with `plot3d_output_not_gridpoint`.

For automatic O-grid to C-grid fallback, inspect these files after the rerun:

```powershell
Get-Content runs\case_name\auto_result.json
Get-Content runs\case_name\manifest.json
Get-Content runs\case_name\mesh\grid_options.in
Select-String -Path runs\case_name\cfl3d.inp -Pattern "CGRID|OGRID|BCTYPE|CONTROL SURFACE|IDIM|JDIM|KDIM"
```

Expected evidence is `mesh_switches[0].from = "ogrid"`,
`mesh_switches[0].to = "cgrid"`, `manifest.json.grid_topology = "cgrid"`,
`manifest.json.mesh.topology = "cgrid"`, and a valid `check-input` result. If
the rerun still fails as C-grid, stop the automatic topology switching and use
normal diagnostics/repair policy rather than repeatedly remeshing.

For first-time DeepSeek setup:

```powershell
Copy-Item configs\llm.example.yaml configs\llm.yaml
notepad configs\llm.yaml
$env:DEEPSEEK_API_KEY = "你的 DeepSeek API Key"
```

`configs\llm.yaml` should contain:

```yaml
default_provider: deepseek

providers:
  deepseek:
    type: openai_compatible
    base_url: https://api.deepseek.com/v1
    api_key_env: DEEPSEEK_API_KEY
    model: deepseek-reasoner
    temperature: 0.1
    max_output_tokens: 2000
    timeout: 120
```

Never write a real API key into tracked files.

## Natural-Language Terminal

Start the LLM terminal:

```powershell
& $PY -m cfl3d_agent chat `
  --llm-provider deepseek `
  --llm-config configs\llm.yaml `
  --repair-policy configs\repair_policy.example.yaml `
  --rag-index knowledge\smoke_index
```

The user can then type requests such as:

```text
计算 NACA0012，Mach 0.2，Re 1500000，迎角 0 到 8 度每 2 度一个点，自动网格，失败后自动修复并输出后处理结果。
```

Example with the new mesh-topology and point-count behavior:

```text
计算 NACA2412，Mach 0.5，Re 3e6，迎角 7 到 9 度每 1 度一个点，自动网格，网格点数 300，先用 O-grid，如果 CFL3D 不接受就自动换 C-grid，并输出后处理结果。
```

If key settings are missing, ask concise follow-up questions instead of guessing physical conditions.

One-shot smoke test without relying on a working LLM key:

```powershell
& $PY -m cfl3d_agent chat `
  --text "我要算 NACA0012 Mach 0.2 攻角 2 Re 1500000 迭代 1 只准备 自动网格" `
  --dry-run `
  --auto-confirm `
  --json
```

If the command returns `missing_fields`, ask the user for only those fields, then rerun the completed request.

NACA2412 automatic-mesh smoke matching the common user phrasing:

```powershell
& $PY -m cfl3d_agent chat `
  --text "我想要做naca2412的马赫数是0.5，雷诺数3e6的7-9的迎角序列，自动网格，网格点数300，迭代1步" `
  --auto-confirm `
  --json
```

For debugging only, add `--dry-run`. A real 1-step run should complete and write
post-processing products under each case directory, but it is not a converged
CFD result.

## Single Case

Use an existing grid:

```powershell
& $PY -m cfl3d_agent auto run `
  --case naca0012_m02_a2_re15e5 `
  --airfoil naca0012 `
  --grid F:\my_meshes\naca0012.p3d `
  --mach 0.2 `
  --alpha 2.0 `
  --re 1500000 `
  --llm-provider deepseek `
  --llm-config configs\llm.yaml `
  --repair-policy configs\repair_policy.example.yaml `
  --rag-index knowledge\smoke_index `
  --max-iterations 3
```

Use automatic meshing:

```powershell
& $PY -m cfl3d_agent auto run `
  --case naca0012_auto_m02_a2_re15e5 `
  --airfoil naca0012 `
  --mach 0.2 `
  --alpha 2.0 `
  --re 1500000 `
  --auto-mesh `
  --grid-topology ogrid `
  --llm-provider deepseek `
  --llm-config configs\llm.yaml `
  --repair-policy configs\repair_policy.example.yaml `
  --rag-index knowledge\smoke_index `
  --max-iterations 3
```

This starts as O-grid and automatically falls back to C-grid once if CFL3D
rejects the O-grid. To force C-grid immediately, replace the topology flag with
`--grid-topology cgrid`. To debug O-grid without fallback, add
`--no-auto-switch-cgrid`.

## Restart Continuation

Use `--restart-from` when the user wants to continue a completed or partially
completed case from a previous `restart.bin`. Prefer `auto run`, because it
copies the restart file, writes `manifest.json`, runs diagnosis, and performs
postprocessing.

Continuation must run in a separate case directory. Do not overwrite the
original long run directory. If the user omits `--case`, the agent derives a new
case name from the restart source directory, for example
`baseline_restart_500cyc`.

Minimal continuation command when the source case already has `manifest.json`,
`airfoil.dat`, and `grid.bin`:

```powershell
& $PY -m cfl3d_agent auto run `
  --restart-from runs\baseline\restart.bin `
  --ncyc 500 `
  --non-interactive `
  --json
```

Explicit continuation command:

```powershell
& $PY -m cfl3d_agent auto run `
  --case baseline_continue_500 `
  --restart-from runs\baseline\restart.bin `
  --dat runs\baseline\airfoil.dat `
  --grid runs\baseline\grid.bin `
  --mach 0.5 `
  --alpha 7 `
  --re 3e6 `
  --ncyc 500 `
  --non-interactive `
  --json
```

When `--restart-from` is set, the agent automatically sets `restart=True` and
`disable_multigrid=True`. Record this clearly: the continuation is a
finest-grid single-level continuation run, not the same multigrid schedule as
the original multigrid run. The manifest records:

```text
restart_from
restart_file
restart_mode = finest_grid_single_level
continuation.disable_multigrid = true
continuation.ncyc
```

Never point `--restart-from` at a `restart.bin` inside the target case directory.
The program rejects that because it would risk overwriting the source restart.
Use a new `--case` name for every continuation segment.

## Continuous Alpha Sweep

For continuous angles of attack, use one sweep command instead of independent cases:

```powershell
& $PY -m cfl3d_agent sweep alpha `
  --case-prefix naca0012_m02_re15e5 `
  --airfoil naca0012 `
  --grid F:\my_meshes\naca0012.p3d `
  --mach 0.2 `
  --re 1500000 `
  --alpha-list 0,2,4,6,8 `
  --llm-provider deepseek `
  --llm-config configs\llm.yaml `
  --repair-policy configs\repair_policy.example.yaml `
  --rag-index knowledge\smoke_index `
  --json
```

For automatic-mesh alpha sweeps, omit `--grid` and let the workflow start from
O-grid with automatic C-grid fallback:

```powershell
& $PY -m cfl3d_agent sweep alpha `
  --case-prefix naca0012_m02_re15e5_auto `
  --airfoil naca0012 `
  --mach 0.2 `
  --re 1500000 `
  --auto-mesh `
  --grid-topology ogrid `
  --alpha-list 0,2,4,6,8 `
  --llm-provider deepseek `
  --llm-config configs\llm.yaml `
  --repair-policy configs\repair_policy.example.yaml `
  --rag-index knowledge\smoke_index `
  --json
```

Check that each alpha after the first records restart provenance from the previous alpha. If a restart is missing or corrupt, diagnose the previous case before continuing the sweep.

Real alpha sweeps require restart chaining by default. Use cold starts only when the user explicitly requests it:

```powershell
& $PY -m cfl3d_agent sweep alpha `
  --case-prefix naca0012_m02_re15e5_cold `
  --airfoil naca0012 `
  --grid F:\my_meshes\naca0012.p3d `
  --mach 0.2 `
  --re 1500000 `
  --alpha-list 0,2,4,6,8 `
  --allow-cold-start-after-missing-restart `
  --json
```

If an alpha after the first fails with:

```text
stopping.inconsistent restart grid indices
program termination due to a cfl3d error check
```

keep the restart workflow, but let the repair loop apply `disable_multigrid` and rerun.
This keeps the previous-alpha initial condition while avoiding CFL3D reading the restart
file at an incompatible multigrid level. Do not report such a case as completed merely
because the solver executable returned exit code `0`.

The common NACA2412 smoke workflow is:

```powershell
& $PY -m cfl3d_agent chat `
  --text "我想要做naca2412的马赫数是0.5，雷诺数3e6的7-9的迎角序列，自动网格，网格点数300，迭代1步" `
  --auto-confirm `
  --json
```

Expected smoke behavior: alpha 7 runs cold start; alpha 8 and 9 reuse the previous
`restart.bin`; if the restart/multigrid mismatch appears, the automatic repair applies
`disable_multigrid` and postprocessing still writes force curves, Cp distribution, and
Mach/Cp contours. A 1-step run is only a workflow test, not a converged CFD result.

After the sweep, summarize generated cases:

```powershell
& $PY -m cfl3d_agent post runs --runs-root runs --output runs\naca0012_m02_re15e5_post_summary.csv
```

## Batch Scale

For tens to thousands of airfoils:

1. Build an input CSV with airfoil name/path, mesh path or auto-mesh flag, Mach, Reynolds number, alpha, ncyc, and case name.
2. Submit jobs.
3. Run with bounded workers.
4. Resume after interruption.
5. Export a CSV report.

Typical commands:

The built-in batch worker currently supports only `--workers 1`; use separate batch directories or an external scheduler for concurrency. LLM/RAG flags are optional and can be omitted for the baseline workflow.

```powershell
& $PY -m cfl3d_agent batch submit --batch-dir batches\study01 --csv batches\study01\input_airfoils.csv
& $PY -m cfl3d_agent batch run --batch-dir batches\study01 --workers 1 --auto-workflow --llm-provider deepseek --llm-config configs\llm.yaml --repair-policy configs\repair_policy.example.yaml --rag-index knowledge\smoke_index
& $PY -m cfl3d_agent batch resume --batch-dir batches\study01 --workers 1 --auto-workflow --llm-provider deepseek --llm-config configs\llm.yaml --repair-policy configs\repair_policy.example.yaml --rag-index knowledge\smoke_index
& $PY -m cfl3d_agent batch report --batch-dir batches\study01 --output batches\study01\post_summary.csv
```

For 20,000 airfoils, do not launch one huge untested batch. Run 5 dry-run cases, then 20 real cases, then 200, and scale separate batch directories or external scheduler submissions according to CPU, disk, and solver license/runtime limits; do not increase the built-in `--workers` value.

## Repair Policy

Use safe repair commands first:

```powershell
& $PY -m cfl3d_agent repair plan --case-dir runs\naca0012_m02_a2_re15e5 --policy configs\repair_policy.example.yaml
& $PY -m cfl3d_agent repair apply --case-dir runs\naca0012_m02_a2_re15e5 --policy configs\repair_policy.example.yaml
& $PY -m cfl3d_agent repair run-once --case-dir runs\naca0012_m02_a2_re15e5 --policy configs\repair_policy.example.yaml
```

Allow LLM repair to adjust only policy-approved low-risk items, such as restart flags, cycle count, timeout, known input-file consistency issues, and documented mesh-generation parameters. Do not allow arbitrary solver binary changes or broad filesystem edits.

## Postprocess

`auto run`, `chat --text`, interactive `chat`, `sweep alpha`, and `batch --auto-workflow`
must treat post-processing as part of the workflow. Every case should write both
the lightweight summary and the rich product report:

```text
runs\<case>\post.json
runs\<case>\post\postprocess_report.json
```

When CFL3D output files are available, expected rich products include:

```text
runs\<case>\post\history.csv
runs\<case>\post\forces_summary.json
runs\<case>\post\force_history.png
runs\<case>\post\cl_history.png
runs\<case>\post\cd_history.png
runs\<case>\post\cmy_history.png
runs\<case>\post\surface_cp.csv
runs\<case>\post\cp_distribution.png
runs\<case>\post\flowfield.npz
runs\<case>\post\mach_contour.png
runs\<case>\post\cp_contour.png
```

If `cfl3d.res`, `cfl3d.prout`, `plot3dg.bin`, or `plot3dq.bin` is missing, do not
claim the plots exist. Open `post\postprocess_report.json` and report the
`status`, `messages`, and generated `outputs` exactly.

If `post\postprocess_report.json` says `plot3d_location` is `cell_centers`, or
the flowfield dimensions are one less than `manifest.grid_dimensions`, the
existing Mach/Cp contour files are from old cell-centered Plot3D output. Fix
`cfl3d.inp` to `IPTYPE=0`, rerun CFL3D in the same or a new case directory, and
then rerun `post case --products`. Do not tell the user the old cloud plots are
boundary-aligned.

Manual post-processing commands:

```powershell
& $PY -m cfl3d_agent post case runs\naca0012_m02_a2_re15e5 --json
& $PY -m cfl3d_agent post case runs\naca0012_m02_a2_re15e5 --products --json
& $PY -m cfl3d_agent post runs --runs-root runs --output runs\post_summary.csv
& $PY -m cfl3d_agent post runs --runs-root runs --products --output runs\postprocess_summary.csv --summary-json runs\postprocess_summary.json
& $PY -m cfl3d_agent rag ingest-runs --runs-root runs --index knowledge\smoke_index
```

Expected outputs include case manifest, solver logs, `report.json`, `post.json`,
`post\postprocess_report.json`, force/residual/Cp CSV files, force and moment
curves, Cp distribution, and Mach/Cp contours when the needed CFL3D files exist.

## Validation

When changing workflow code or docs, run:

```powershell
& $PY -m unittest discover -s tests
& $PY -m cfl3d_agent --help
& $PY -m cfl3d_agent auto run --help
& $PY -m cfl3d_agent chat --help
& $PY -m cfl3d_agent sweep alpha --help
```

For smoke validation without a real solver run:

```powershell
& $PY -m cfl3d_agent sweep alpha --case-prefix sweep_dry_smoke --airfoil ah63k127 --grid code\coord-trans-encoding-main\differentiable_metrics\train_mesh_point\ah63k127.p3d --mach 0.2 --re 1000000 --ncyc 1 --alpha-list 0,2,4 --dry-run --json
```



## Mesh Independence Study

Use the dedicated `mesh-study` subcommand to run a grid-convergence study
across three default mesh densities (coarse / medium / fine) for the same
flow condition. The study automates case preparation, solver execution,
post-processing, and comparison for each density level.

Default grid levels are all normalized to `4n+1` for Construct2D and chosen to
remain compatible with the default three-level CFL3D multigrid schedule:

| Level | Surface points (`nsrf`) | Normal points (`jmax`) |
| --- | --- | --- |
| coarse | 105, within the requested 80-120 range | 65 |
| medium | 241, within the requested 150-280 range | 129 |
| fine | 401, within the requested 400-500 range | 257 |

Results are written to a study directory under `runs/{case_prefix}/`:

- `mesh_study_results.json`: machine-readable comparison including all force
  coefficients per level and convergence metrics.
- `mesh_study_report.txt`: human-readable summary table.

### Basic Usage

Automatic meshing with Construct2D is the default for `mesh-study`:

```powershell
& $PY -m cfl3d_agent mesh-study `
  --case-prefix naca0012_ms `
  --airfoil naca0012 `
  --mach 0.2 `
  --alpha 2.0 `
  --re 1e6 `
  --grid-topology ogrid
```

This creates three cases: `naca0012_ms_coarse`, `naca0012_ms_medium`, and
`naca0012_ms_fine`.

Do not use a single existing `--grid` for mesh independence studies. Reusing one
mesh for all three levels is not a grid-convergence test, so the command rejects
single-grid input. If external grids are needed later, add explicit separate
coarse/medium/fine grid arguments before enabling that workflow.

### Dry-Run Preview

```powershell
& $PY -m cfl3d_agent mesh-study `
  --case-prefix naca0012_preview `
  --airfoil naca0012 `
  --mach 0.2 `
  --alpha 2.0 `
  --re 1e6 `
  --dry-run `
  --json
```

A successful dry run returns `status: "dry_run"`; real solver completion returns
`status: "completed"`. If any level fails preflight or meshing, the study returns
`status: "blocked"`.

### Reading Results

After the study completes, the output under the study directory includes both a
machine-readable JSON file and a plain-text report with a comparison table:

```text
  Level      nsrf   jmax   Cl           Cd           Cm
  ---------------------------------------------------------
  coarse     105    65     0.123456     0.012345    -0.001234
  medium     241    129    0.124321     0.011987    -0.001201
  fine       401    257    0.124567     0.011876    -0.001189

  CL fine-vs-medium change: 0.198%
  CD fine-vs-medium change: 0.934%
```

If the change drops below a few percent from medium to fine for both CL and CD,
the solution is approaching grid independence.


## Migrating To A New Computer

Moving the project to another machine is a bootstrap step, not a code edit. The
agent resolves its Python interpreter and native binaries (`cfl3d_seq`,
`construct2d`) per machine; the two native programs are compiled from source and
everything else is pure Python. Full guide: `docs\MIGRATION_CROSS_PLATFORM.md`.

On the new machine, drive the agent with that machine's own Python and run the
bootstrap once. The script captures its own interpreter (`sys.executable`), so
this is how the target machine's Python location is detected.

```bash
# Linux / macOS
python3 tools/bootstrap.py
```

```powershell
# Windows: point at the MSYS2/UCRT64 toolchain
python tools\bootstrap.py --msys-root <msys2-root>
```

`bootstrap` detects the toolchain, compiles Construct2D (Makefile) and CFL3D seq
(CMake, no MPI/CGNS/complex), and writes `configs\local_env.json` with the
resolved Python, binary paths, and runtime PATH dirs. The agent reads that file
first, so no source paths are hard-coded. Useful flags: `--check` (detect
toolchain only), `--dry-run` (print build commands), `--skip-cfl3d`,
`--skip-construct2d`, `--jobs N`.

Toolchain prerequisites: macOS `brew install gcc cmake make`; Linux
`sudo apt-get install gfortran cmake make ninja-build`; Windows install MSYS2
then `pacman -S --needed mingw-w64-ucrt-x86_64-gcc-fortran
mingw-w64-ucrt-x86_64-cmake mingw-w64-ucrt-x86_64-ninja`.

Verify with `python -m cfl3d_agent doctor`. It now reports the platform, the
interpreter to use, the resolved binaries, the build toolchain, and whether each
solver actually starts; a missing binary prints a hint to run
`tools\bootstrap.py`. To repoint binaries without rebuilding, set `CFL3D_SOLVER`,
`CONSTRUCT2D`, or `CFL3D_RUNTIME_PATHS`, or edit `configs\local_env.json`
(copy `configs\local_env.example.json` to start).
## Final Response

Summarize the exact command used, whether the run was dry or real, where results were written, what the LLM repaired, and what remains for the user to inspect.

