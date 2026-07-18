---
name: uix1-uix2-migration
description: Migration playbook for converting legacy M-Files UIX1 extensions to UIX2 with analyzer-first workflow, deterministic codemods, adapter mapping, and mandatory validation gates.
---

# UIXv1 → UIXv2 Migration Skill

Purpose: help migrate legacy UIXv1 (Classic Desktop/Web) extensions to UIXv2 (New Desktop/vNext).

## Current converter support status

- ✅ Supported now: `<module environment="shellui">`
- ✅ Supported now: dashboard conversions
- ⏳ Not supported yet: `<module environment="vaultui">` (planned for later)
- ⏳ Not supported yet: other non-shellui module environments

## How to use this skill

> **📁 Project-specific workspace:** This project uses `src/Legacy/` as the migration workspace root.
> - Place UIX1 source codebases or archives in `src/Legacy/`
> - `src/Legacy/SPEC.md` — reverse-engineered specification of the legacy codebase (Phase 0 output)
> - Migration workspace structure per app:
>   - `src/Legacy/<app>/source-uix1/` — extracted original UIX1 files (always created)
>   - `src/Legacy/<app>/converted-uix2/` — scratch workspace for iterating on conversion (**scratch workflow only**)
>   - `src/Legacy/<app>/notes/` — migration notes, TODO, analyzer output, migration assessment (always created)
>
> **Two conversion workflows** (choose during migration assessment):
>
> | Workflow | Where conversion happens | Best for | Rollback |
> |----------|------------------------|----------|----------|
> | **Direct** | `src/Frontend/TemplateApp.UIExt/` | Simple apps (1-2 core files, no React, no backend changes) | Git history |
> | **Scratch workspace** | `src/Legacy/<app>/converted-uix2/` → graduates to `src/Frontend/` | Complex apps (multi-file, React dashboard, backend mods, high risk) | Delete `converted-uix2/` and start over |
>
> **Decision rule:** The migration assessment must explicitly record the chosen workflow (`Direct` or `Scratch workspace`) and a short justification before implementation starts. If the workflow choice changes later, record it in the Assessment Delta Log before continuing implementation.
>
> **Direct workflow:** Convert directly in `src/Frontend/TemplateApp.UIExt/`. Keep `source-uix1/` as reference for diffing. Git commit before starting conversion provides the rollback point. No graduation step needed — code is already in the production directory. Use `git diff` to compare against the pre-conversion state.
>
> **Scratch workspace workflow:** Convert in `converted-uix2/`. When code is validated, graduate into `src/Frontend/TemplateApp.UIExt/`. The existing code in `src/Frontend/` is untouched until graduation. Use `diff` between `source-uix1/` and `converted-uix2/` to track changes.
>
> **Production targets — do NOT create new project folders:**
> - `src/Frontend/TemplateApp.UIExt/` — UIX2 module code, dashboards, assets (has build scripts, ESLint, `appdef.xml`)
> - `src/Backend/TemplateApp.VAF/` — VAF backend for server-side logic (has deploy scripts, `appdef.xml`)
> - Use the existing build and deploy scripts — see `CLAUDE.md` for commands.
> - See also: [UIX2 development skill](../uix2-app/SKILL.md) for target platform constraints
>
> **Platform rule:** UIX2 applications must always support both Desktop and Web clients. This is not a per-migration decision — do NOT ask the user about target platforms. Use only APIs that work in both clients. If a legacy feature cannot work on web (e.g., local filesystem access), treat it as a blocker and list alternatives.
>
> **jQuery rule:** Always remove jQuery during migration — do NOT ask the user. For simple apps, use vanilla JavaScript ES6+. For complex dashboard UIs with significant interactivity, use React with Vite (see [react-dashboard.md](../uix2-app/references/react-dashboard.md)). This is a technical decision based on complexity, not a user question.

1. Read [references/index.md](references/index.md).
2. Read analyzer CLI docs: [scripts/README.md](scripts/README.md).
3. **Phase 0: Discovery & Specification** (mandatory, see section below).
4. Run analyzer + write migration assessment.
5. Start with app triage checklist.
6. Run migration in this order:
   - Codemod
   - Adapter layer
   - Manual fixes for unsupported features

### Mandatory command gate (must run)

Two separate tools exist for different phases. Do NOT confuse them:

**1. Analyzer (`uix_analyzer.js`) — Phase 0 only, archives only**
- Accepts `.zip` or `.mfappx` archive files — NOT raw source folders
- Use during Phase 0 to analyze the legacy UIX1 codebase before conversion
- CLI input scope: accepts only one input target per run (`--file` or `--path`)
- For multiple archives, run analyzer multiple times
- Command:
   - `node scripts/uix_analyzer.js --file <archive.zip> --json <output.json> --html`
   - `node scripts/uix_analyzer.js --path <folder-with-archives> -recursive --html`

**2. Verifier (`verify_ts_output.js`) — post-conversion, source folders**
- Accepts raw source folders — run on wherever the converted code lives
- Use after conversion to validate the converted JS/TS code for leftover UIX1/COM patterns
- Command (adjust path based on workflow):
   - Scratch workflow: `node scripts/verify_ts_output.js --path <src/Legacy/<app>/converted-uix2> --app-root <src/Legacy/<app>/converted-uix2> --strict --json <src/Legacy/<app>/notes/verify-output.json> --todo <src/Legacy/<app>/notes/verify-output.TODO.md>`
   - Direct workflow: `node scripts/verify_ts_output.js --path <src/Frontend/TemplateApp.UIExt> --app-root <src/Frontend/TemplateApp.UIExt> --strict --json <src/Legacy/<app>/notes/verify-output.json> --todo <src/Legacy/<app>/notes/verify-output.TODO.md>`

If verifier returns findings, migration is not complete until findings are fixed or explicitly documented as justified false positives in conversion notes.

> **Common mistake:** Do NOT run the analyzer on source folders — it only accepts archives. Use the verifier for post-conversion validation.

## Phase 0: Discovery & Specification (mandatory)

**This phase must be completed before any conversion work begins.**

When a legacy codebase first appears in `src/Legacy/`, the AI agent must produce two documents before proceeding to triage or conversion. No assumptions — the codebase and any other content in `src/Legacy/` is the **single source of truth**.

### Step 0.1 — Read the entire codebase

- Read **every** source file in `src/Legacy/`: code, config, manifests, scripts, HTML, CSS, settings, README, install docs, registry files, solution files.
- Identify all components: UIX shell extensions, desktop apps, VAF backends, COM references, external tool integrations.
- Trace the data flow end-to-end: what triggers the app, what data it reads, what it does, what the user sees.
- Do **not** skip commented-out code — it often reveals removed features, alternative modes, or planned functionality that informs the specification.

**Note: Backend-coupled apps — read event handlers and extension methods**

If the legacy app has a VAF backend, read all `[EventHandler(...)]` and `[VaultExtensionMethod(...)]` attributes in the backend C# code during this step. Document which extension methods the frontend calls and what event handlers exist. In rare cases, the backend may use event handlers (e.g., `BeforeCreateNewObjectFinalize`) that expect the frontend to use a specific API pattern — if so, note this in the spec's call chain section.

### Step 0.2 — Write `src/Legacy/SPEC.md`

Write a comprehensive, verbose markdown specification of what the codebase actually does. This is a reverse-engineered functional specification, not a migration plan.

Follow the template in [references/spec-template.md](references/spec-template.md). Key sections:

1. **Overview** — one-paragraph summary of the application from end-user perspective
2. **Architecture** — all components, how they interact, launch/invocation mechanisms
3. **Functional specification** — per-feature: trigger, input, processing steps, output/side effects
4. **M-Files integration points** — vault operations, aliases, object types, classes, property definitions, workflows, search conditions
5. **External dependencies** — COM objects, filesystem access, network services, Outlook/Office interop, registry
6. **Configuration** — settings files, hardcoded values, environment assumptions
7. **File inventory** — table mapping every source file to its purpose
8. **Data flow** — text description of how data moves through the system
9. **Critical call chains** — frontend → backend sequences, especially extension method calls and any event handler dependencies

Rules:
- Be comprehensive and verbose — this document is the foundation for all migration decisions
- The codebase is the single source of truth — do not assume behavior from naming conventions or external knowledge
- Include exact vault alias strings, property definition aliases, class aliases found in code
- Document both active code and significant commented-out code (mark commented-out sections clearly)
- If the codebase contains multiple versions (archives, build output), document which version the spec covers
- **For apps with a backend:** Document which extension methods the frontend calls and any event handler dependencies. Most apps use `RunExtensionMethod` calls; in rare cases a backend event handler may depend on a specific frontend API pattern (e.g., two-step create to trigger `BeforeCreateNewObjectFinalize`) — note these if found.

### Step 0.3 — Run analyzer + write `src/Legacy/<app>/notes/migration-assessment.md`

After `SPEC.md` is complete, run the analyzer on `.zip` or `.mfappx` archives found in the codebase:

- **Inspect ignored files too:** During Phase 0 inventory, explicitly check ignored files in legacy directories before creating any new archive. Existing `.zip` or `.mfappx` files are often hidden by `.gitignore` patterns but still represent the real release artifacts.
- If multiple versions of the same app exist (e.g., `App-1.0.zip`, `App-1.1.zip`), **analyze only the latest version** — that's the deployed behavior to migrate.
- Note older versions in the assessment for reference (version history may inform migration decisions), but do not analyze them separately.
- **Mixed archive types:** If `src/Legacy/` contains both `.zip` (source/release) and `.mfappx` (M-Files package), prefer the `.mfappx` — it represents what was actually deployed. List the `.zip` as reference.
- **Nested archives:** If a release `.zip` contains `.mfappx` files inside it, extract and analyze the inner `.mfappx`. The outer `.zip` is just packaging.
- **Multiple different apps:** If `src/Legacy/` contains archives for different applications, analyze each app's latest archive separately and write separate assessment sections.
- **No version number in filename:** Cross-reference against `appdef.xml` inside the archive to determine the version. If multiple undated archives exist, ask the user which is the latest deployed version.
- **Backend-only archives (.mfappx with no JS):** The UIX analyzer only processes UIX1 JavaScript. For VAF-only packages, skip the analyzer — instead, extract and read `appdef.xml` + source code to document the backend in `SPEC.md`.
- **Create a new archive only as a fallback:** If no suitable release archive exists, create a temporary `.zip` from the actual shippable app payload and document why the fallback was necessary in the migration assessment.

```
node .github/skills/uix1-uix2-migration/scripts/uix_analyzer.js --file <archive> --json <output.json> --html
```

Then write a migration assessment that combines analyzer output with architectural analysis from the spec. Follow the template in [references/assessment-template.md](references/assessment-template.md). Key sections:

1. **Analyzer results summary** — interpreted findings (not raw JSON), categorized by risk
2. **Migration classification** — `Auto` / `Semi-auto` / `Manual` / `Blocked` with justification
3. **Backend classification** — one of:
   - `Frontend-only` — legacy app is pure UIX1 with no server-side logic; no Backend package needed
   - `Existing VAF as-is` — legacy app already has a working VAF backend that stays unchanged; only migrate the frontend
   - `Existing VAF merge` — legacy app has an existing VAF that should be migrated/merged into `src/Backend/` (e.g., upgrading from older VAF framework version). Ask the user whether to preserve the original VAF application GUID for in-place upgrade or use a new GUID.
   - `Backend modification required` — migration requires new or changed VAF extension methods (no pre-existing VAF)
4. **Architecture impact** — what moves to VAF backend, what becomes UIX2 dashboard, what becomes UIX2 module, what gets dropped
5. **Blocker analysis** — per blocker: what, why, and proposed alternative
6. **Effort estimate** — rough T-shirt sizing per component
7. **Recommended migration strategy** — ordered steps for this specific app

**If the migration introduces or changes a backend:** before logic work proceeds, identify and align the backend identity surfaces that control extension-method registration:
- `.csproj` `AssemblyName`
- `.csproj` `RootNamespace`
- backend `appdef.xml` `<assembly>`
- the actual namespace/class that exposes the extension methods

If these drift apart, M-Files may load the backend package but leave extension methods effectively unavailable, producing misleading "not found" or generic runtime errors from the frontend.

### Phase 0 completion gate

Phase 0 is complete when:
- [ ] Every source file in `src/Legacy/` has been read
- [ ] `src/Legacy/SPEC.md` exists and covers all sections
- [ ] Analyzer has been run on the latest relevant archive per app (skip backend-only `.mfappx` with no JS)
- [ ] `src/Legacy/<app>/notes/migration-assessment.md` exists
- [ ] Migration classification has been determined
- [ ] Backend classification is marked as **provisional** (validated at Runtime Smoke Gate, see below)
- [ ] If backend work is involved, the assessment records the intended `AssemblyName` / `RootNamespace` / backend `appdef.xml` `<assembly>` alignment before implementation starts

Only after this gate is passed may you proceed to triage, workspace setup, and conversion.

> **⚠️ Backend classification is PROVISIONAL until Runtime Smoke Gate.**
> Static analysis cannot detect vault-version API gaps (e.g., `GetObjectDataOfMultipleObjects` returning 501). The Phase 0 classification is a design anchor, not a commitment. It MUST be validated against the live target vault during the Runtime Smoke Gate (see below). If the smoke gate reveals API unavailability, reclassify and document the change in the assessment delta log.

## Execution model for large migrations (mandatory)

- Do **not** one-shot large conversions.
- Start each app migration by writing:
   - a short migration plan
   - `src/Legacy/<app>/notes/TODO.md`
- Execute conversion iteratively against TODO items and update status continuously.
- Do not package final zip until TODO is complete and validation is green.

## Runtime Smoke Gate (mandatory)

**When:** Immediately after the first deployable slice is built and installed — before polishing UI or adding remaining features.

**Purpose:** Validate that the architecture classification from Phase 0 holds in the real target vault. This gate catches API availability issues, sandbox restrictions, and environment-specific failures early.

### Smoke test checklist

Run through each applicable item and record pass/fail:

- [ ] **Module loads:** `OnNewShellUI` fires (check parent DevTools console, F12)
- [ ] **Shell frame ready:** `NewShellFrame` + `Started` events fire
- [ ] **Commands appear:** context menu / taskbar buttons visible on correct object types
- [ ] **Dashboard opens:** popup or tab dashboard renders (not blank)
- [ ] **`OnNewDashboard` fires:** switch DevTools to dashboard iframe context — confirm dashboard initialization log appears
- [ ] **Data path probe:** the primary data-loading API call succeeds (e.g., `SearchObjects`, `GetObjectDataOfMultipleObjects`, `RunExtensionMethod`). Test with a real vault object, not just UI rendering.
- [ ] **VAF responds (if applicable):** extension method call returns expected data shape
- [ ] **Backend identity aligned (if applicable):** if an extension method is unexpectedly "not found", verify `.csproj` `AssemblyName`, `.csproj` `RootNamespace`, backend `appdef.xml` `<assembly>`, and the extension-method class namespace all agree before changing business logic
- [ ] **Environment clean:** Uninstall any template/sample apps (e.g., TemplateApp.UIExt) from the vault before smoke testing. Leftover apps pollute console traces and increase ambiguity when diagnosing failures.
- [ ] **No blocking console errors:** check for the errors below. Ignore non-blocking noise (optional asset 404s, favicon probes, harmless warnings).

### Blocking vs non-blocking errors

| Blocking (fail the gate) | Non-blocking (log but continue) |
|--------------------------|--------------------------------|
| 501 Not Implemented | 404 for optional icons/assets |
| Unhandled promise rejection | Favicon.ico 404 |
| DataCloneError | CSS/font loading warnings |
| `undefined is not a function` | Deprecation warnings |
| Extension method not found | Console.info/debug noise |

### If smoke gate fails

1. **API unavailable (501, method not found):** Trigger reclassification — switch to API Fallback Ladder (see below)
2. **Dashboard blank:** Check `mfiles.extensibility.protocol.js` is in `<head>` (see protocol script checklist below)
3. **DataCloneError:** Non-serializable data in `CustomData` — review structured clone compliance
4. **Commands missing:** Verify enum names, `Started` event timing, boolean guard
5. **Dashboard bridge methods missing:** Do not assume every documented `IDashboard` method exists in the active runtime proxy. Inspect available members immediately, prefer `UpdateCustomData()` + `MFiles.Event.CustomDataChanged` for ShellUI ↔ Dashboard communication, and use `dashboard.Window.Close()` if `dashboard.Close()` is unavailable.
6. **Extension method not found:** Before renaming methods or changing frontend calls, inspect backend identity alignment: `.csproj` `AssemblyName`, `.csproj` `RootNamespace`, backend `appdef.xml` `<assembly>`, and the extension-method class namespace.

### Reclassification protocol

If the smoke gate proves the Phase 0 backend classification wrong:

1. Update `migration-assessment.md` — change the classification field
2. Add an entry to the **Assessment Delta Log** section (see assessment template)
3. Document: what changed, when, why (the specific error/behavior that triggered it)
4. Adjust the migration strategy and TODO accordingly
5. Do NOT restart from scratch — adapt the existing work

## API Fallback Ladder (mandatory for data-heavy migrations)

When a UIX2 gRPC API call fails at runtime in the target vault (501, unsupported, or returns incorrect data), follow this prescribed fallback order:

| Level | Approach | When to use |
|-------|----------|-------------|
| **1. UIX2 direct call** | `vault.objectOperations.GetObjectDataOfMultipleObjects(...)` etc. | Default — always try first |
| **2. VAF extension bridge** | Frontend calls `RunExtensionMethod`, VAF does the vault operation server-side | UIX2 call returns 501, is unavailable in target vault version, or hits sandbox restrictions |
| **3. Simplified fallback** | Reduce feature scope — show less data, skip optional fields, degrade gracefully | Both L1 and L2 fail or are impractical |
| **4. User notification** | Show clear message: "Feature X requires M-Files Server version Y+" | Feature genuinely cannot work in this environment |

### Switching levels

- **L1 → L2:** When the UIX2 API call returns 501, throws "not implemented", or silently returns wrong data. This is the most common escalation.
- **L2 → L3:** When adding a VAF extension method is disproportionate to the feature value, or when the backend cannot be modified.
- **L3 → L4:** When the feature fundamentally cannot work without the unavailable API.

**Document every level switch** in the migration notes with: which API failed, what error, which fallback was chosen, and why.

### Stop after first data-path failure (mandatory)

If the Runtime Smoke Gate reveals that the primary data-loading API call fails (501, unsupported method, or returns wrong/unrelated data), **stop immediately and escalate to the next fallback level.** Do NOT try alternative L1 approaches (e.g., switching from `GetObjectDataOfMultipleObjects` to `GetProperties` to `SearchObjects`). Each failed attempt costs a build-deploy-test cycle and delays the migration.

**The rule:** One L1 data-path failure at the smoke gate = escalate to L2. The smoke gate exists to catch environment-specific gaps early — honour its verdict.

### Default to L2 for non-shell-script vault operations

If the legacy app performs vault searches, document reads, or metadata extraction outside the UIX1 shell script (e.g., in a companion EXE, COM automation tool, or background process), **start at Level 2 (VAF bridge)** for those operations. Do not attempt L1 UIX2 direct calls. The spec tells you where operations happened — if they were in a desktop process with full COM/MFilesAPI access, the UIX2 gRPC sandbox is unlikely to replicate them directly.

### VAF extension bridge pattern

When escalating from L1 to L2, use this standard pattern:

```csharp
// VAF side — VaultApplication.cs
[VaultExtensionMethod("AppName.GetSomeData", RequiredVaultAccess = MFVaultAccess.MFVaultAccessNone)]
private string GetSomeData(EventHandlerEnvironment env)
{
    var input = JsonConvert.DeserializeObject<InputModel>(env.Input);
    // Use full server-side Vault API here — no sandbox restrictions
    var result = env.Vault.ObjectOperations.GetObjectInfo(...);
    return JsonConvert.SerializeObject(new { Success = true, Data = result });
}
```

```javascript
// Frontend side — dashboard or module
try {
    const resp = await vault.VaultExtensionMethodsOperations.RunExtensionMethod({
        method_name: "AppName.GetSomeData",
        input: JSON.stringify(inputData)
    });
    const parsed = resp.output ? JSON.parse(resp.output) : null;
    if (!parsed || !parsed.Success) throw new Error(parsed?.Error || "Unknown error");
    // Use parsed.Data
} catch (err) {
    console.error("Extension method failed:", err);
    // Show user-friendly error or degrade gracefully
}
```

## Required conversion workflow notes

- **Unzip first:** to inspect and convert actual source files, first extract the UIXv1 archive into a working folder.
- **Build migration under `src/Legacy/`:** keep old and new side-by-side in the same app workspace.
- **Create app migration workspace:** create a dedicated folder per migrated app under `src/Legacy/`:
   - `src/Legacy/<app-id-or-name>/source-uix1/` — always created (reference copy)
   - `src/Legacy/<app-id-or-name>/notes/` — always created (TODO, assessment, verifier output)
   - `src/Legacy/<app-id-or-name>/converted-uix2/` — **scratch workflow only** (not needed for direct workflow)

### Choosing the conversion workflow

The conversion workflow is chosen during the migration assessment. Document the choice in the assessment.

| Criteria | Direct workflow | Scratch workspace workflow |
|----------|----------------|---------------------------|
| **App complexity** | Simple (1-2 core files, vanilla JS dashboard or no dashboard) | Complex (multi-file, React dashboard, significant restructuring) |
| **Backend changes** | None or existing VAF as-is | Backend modification required or VAF merge |
| **Risk tolerance** | Low risk — straightforward API replacements | High risk — architectural redesign, uncertain API compatibility |
| **Rollback mechanism** | `git checkout -- src/Frontend/` restores original files | Delete `converted-uix2/` and start over |
| **Where conversion happens** | Directly in `src/Frontend/TemplateApp.UIExt/` | In `src/Legacy/<app>/converted-uix2/`, then graduate |
| **Graduation step** | Not needed — code already in production directory | Required — copy validated code to `src/Frontend/` |
| **Reference diffing** | `git diff` against pre-conversion commit; `source-uix1/` for original reference | `diff` between `source-uix1/` and `converted-uix2/` |

### Direct workflow steps

1. Extract UIX1 source into `src/Legacy/<app>/source-uix1/` (reference copy — never modify)
2. Convert directly in `src/Frontend/TemplateApp.UIExt/` — replace template code with migrated implementation (rollback: `git checkout -- src/Frontend/` restores original files)
3. Update `appdef.xml` in `src/Frontend/` to reference new files
4. Run verifier on `src/Frontend/TemplateApp.UIExt/`
5. Build, lint, deploy using existing project scripts

### Scratch workspace workflow steps

1. Extract UIX1 source into `src/Legacy/<app>/source-uix1/` (reference copy — never modify)
2. **Copy** original files as-is from `source-uix1/` to `converted-uix2/` — do not start from synthetic files
3. Edit the copies in `converted-uix2/` to make UIX2 compatibility changes
4. Run verifier on `converted-uix2/`
5. **Graduate** validated code to `src/Frontend/TemplateApp.UIExt/` (and `src/Backend/` if needed):
   - UIX2 module code (main.js, dashboards, assets) → `src/Frontend/TemplateApp.UIExt/`
   - VAF backend code → `src/Backend/TemplateApp.VAF/` (**only if backend classification requires it**)
   - The existing code in production directories is a **placeholder example** — it can and should be replaced
   - Do NOT create new project folders — use existing ones with build scripts, `appdef.xml`, and ESLint config
   - Update `appdef.xml` in the target project to reference new files
   - The `converted-uix2/` workspace remains in `src/Legacy/` for traceability
6. Build, lint, deploy using existing project scripts

### Common rules (both workflows)

- **UIX2 ShellUI module file rule (mandatory):** if source has multiple `<file>` entries under the same `<module environment="shellui">`, merge them into one JS file and keep only that single file entry in `appdef.xml`.
   - Preserve original execution order when merging (same order as source `<file>` entries).
   - Keep original source files in `source-uix1/` for traceability.
- **Start notes immediately:** at conversion start, write a notes file (for example `notes/conversion-notes.md`) that lists:
   - missing capabilities
   - features that are hard to convert
   - expected manual redesign areas
   - final migration classification (`Auto` / `Semi-auto` / `Manual` / `Blocked`)
- **Create TODO tracker immediately:** create `notes/TODO.md` and include at least:
   - customData clone-safety audit
   - script path validation
   - event-handler conversion pass
   - invalid assignment scan pass
   - final validation and packaging gate

## Output correctness rules (important)

- Preserve original app structure as much as possible.
- Preserve original file set as baseline by copying source files first, then patching.
- Do **not** invent generic runtime files (for example `dashboard.js`) unless they are explicitly needed by the migrated app.
- Dashboard conversion should follow source reality:
   - keep original dashboard HTML files and ids
   - keep referenced JS/CSS assets (or migrate inline scripts carefully)
   - avoid replacing real dashboard logic with a placeholder unless user explicitly asks for scaffold-only output
- If placeholder output is intentionally produced, mark it clearly in notes and filenames as scaffold/WIP.
- Prefer fidelity-first conversion: source-equivalent behavior target first, synthetic simplifications second.
- **Treat reverse-engineered quirks as suspicious:** When the spec documents unusual code behavior (e.g., "first line of file is always ignored", "empty lines are skipped", encoding hacks), do NOT blindly preserve it. Flag it for user validation before implementing. These quirks may be accidental artifacts of the original code, not intentional business rules. Implementing them faithfully can cause visible regressions (e.g., content truncation) that are harder to debug than omitting them.

### Additional mandatory checks

- **CustomData clone safety:** verify no functions, DOM elements, window objects, shell frame objects, or other non-structured-clone values are passed in dashboard `CustomData`.
   - Convert payloads to postMessage-compatible plain data (primitives/plain objects/arrays).
- **Script path validation:** verify every dashboard `<script src="...">` path exists relative to the dashboard file location.
- **Event model migration:** convert return-object event handlers (for example `OnNewShellUI` returning `OnNewShellFrame`) to explicit `Events.Register(...)` calls based on the first callback argument object.
- **Invalid assignment scan:** detect and fix invalid left-hand assignments (for example `foo() = 1`).
- **Packaging gate:** do not produce final `.zip` while TODO items are still open.

### Discovery Checkpoint (MANDATORY before writing UIX2 code)

When converting ANY UIX1 API call to UIX2, you MUST verify the replacement exists before writing it. UIX1/COM training data is **actively harmful** — patterns that look plausible fail silently in UIX2's gRPC proxy environment.

**Verification hierarchy (use in order):**
1. **Skill docs** — Check `common-tasks.md`, `migration-uix1.md`, and `boilerplate-main.md` for working examples
2. **Gotchas list** — Check CLAUDE.md/GEMINI.md/copilot-instructions.md for known traps
3. **Developer Portal** — Fetch the API reference page to confirm method signatures (see `.github/skills/uix2-app/URL-REFERENCE.md` for URL patterns)
4. **gRPC type definitions** — Check `references/grpc_utils/dist-public/*.d.ts` for actual UIX2 object shapes, property paths, and method signatures. These are the M-Files gRPC TypeScript definitions and are authoritative for `snake_case` property names (e.g., `obj_id.item_id.internal_id`)
5. **`console.log()` discovery** — If none of the above cover it, deploy a discovery build that logs the object shape, wait for user output, then write the real code

**The 3-Strike Rule:** If you deploy 3 versions that fail at the same API call, you MUST stop and switch to `console.log()` discovery. Do not guess a 4th time.

**NEVER:**
- Use hardcoded numeric constants for enums (`7`, `10`, `43`) — use `MFiles.Event.NewShellFrame` etc.
- Guess property paths from UIX1 conventions (`ObjVer.ID` → WRONG)
- Assume constructors exist (`new MFiles.SearchCriteria()` → doesn't exist at runtime)
- Use UIX1 callback return patterns (`return { OnNewShellFrame: ... }` → ignored in UIX2)
- Bump version and retry with a different guess after an API error — discover first
- Keep guessing after a dashboard/runtime proxy method is missing — log available members immediately with `Object.keys(...)`, then switch to a documented fallback

**UIX2 Anti-Patterns (NEVER DO THESE):**

| Anti-Pattern | Why It Fails | Correct Approach |
|-------------|-------------|-----------------|
| Hardcoded numeric event/enum IDs | Values unreadable, environment-dependent | Full enum: `MFiles.Event.NewShellFrame` |
| `return { OnNewShellFrame: ... }` | UIX1 callback pattern, ignored in UIX2 | `shellUI.Events.Register(MFiles.Event.NewShellFrame, ...)` |
| `shellUI.ShellFrame` / `shellUI.Vault` | Don't exist in UIX2 | Register for events; use `shellFrame.ShellUI.Vault` |
| Commands in multiple events "for safety" | Creates duplicates | `Started` only, with boolean guard |
| `shellFrame._myFlag` state | Fragile | Use closure variables |
| Version bump + retry after API error | Leads to 13-version spirals | `console.log()` discovery first |
| UIX1 paths (`ObjVer.ID`, `VersionData.DisplayID`) | Don't exist in UIX2 | Discover with `console.log()`, use `snake_case` |

**Golden Template:** See `.github/skills/uix2-app/references/boilerplate-main.md` for the correct lifecycle pattern.

### Deprecated API replacement checks (mandatory)

Validate migrated code against the official deprecated-features map:
- Source: https://developer.m-files.com/Frameworks/User-Interface-Extensibility-Framework/Reference/Upgrading/deprecated_features/

UIX interface replacements to enforce:
- `CommandLocation_TaskPane` → use `CommandLocation.TaskBar` with `ICommands`.
- `IShellFrame.ITaskPane` → use `ICommands`.
- `ITaskPane.CreateGroup` → use `ICommands.CreateTaskbarGroup()`.
- `TaskPane.AddCustomCommandToGroup` → use `ICommands.AddCustomCommandToMenu(...)` in Taskbar group flow.
- `ICommands.SetIconFromPath` → use `SetIcon(...)` or `SetTaskbarGroupIcon(...)`.
- `ICommonFunctions.ExecuteURL` → use `await MFiles.OpenExternalWebLink(url)` (global static method, NOT via shellFrame.ShellUI.CommonFunctions). Only supports `http`, `https`, and `mailto` protocols — `file://` and custom protocols are NOT supported.
- `ICommonFunction.ReadTextFile` → move logic to VAF/server-side workaround.
- `IDashboard.Vault` → use `IDashboard.ShellFrame.ShellUI.Vault` access path.
- `MFiles.CreateInstance(...)` → use `new` constructors (for example `new MFiles.ObjVer()`).
- `SessionInfo.ClientCulture` → use `GetClientLocale()`.

Vault API replacements to enforce:
- `ClassOperations.GetObjectClassIDByAlias` → `GetMetadataStructureItemIdByAlias`.
- `ObjectTypeOperations.GetObjectTypeIDByAlias` → `GetMetadataStructureItemIdByAlias`.
- `PropertyDefOperations.GetPropertyDefIDByAlias` → `GetMetadataStructureItemIdByAlias`.
- `WorkflowOperations.GetWorkflowIDByAlias` / `GetWorkflowStateIDByAlias` → `GetMetadataStructureItemIdByAlias`.
- `UserGroupOperations.GetUserGroupIDByAlias` → `GetMetadataStructureItemIdByAlias`.
- `ObjectSearchOperations.SearchForObjectsByConditions` / `...Ex` → `SearchObjects`.

#### Search API Migration

| UIX1 (COM) | UIX2 (gRPC) | Notes |
|------------|-------------|-------|
| `new MFiles.SearchConditions()` | Plain object `{ value: [...] }` | `MFiles.SearchConditionArray` is NOT a constructor at runtime despite TypeScript definitions. Use plain objects with `value` property |
| `new MFiles.SearchConditionEx()` | Not needed | Build conditions as plain `{expression, type, value}` objects |
| `new MFiles.SearchCriteria()` | Not available as constructor | Use `SearchPane.GetSearchCriteria()` to get current criteria, or build conditions manually |
| `new MFiles.View()` | Not available as constructor | Use VAF `ViewOperations` or restructure as search-based approach |
| `conditions.AppendFromExportedSearchString()` | Not available in UIX2 | Use VAF extension method for import/export |
| `vault.ObjectSearchOperations.SearchForObjectsByConditions(...)` | `await vault.searchOperations.SearchObjects({ conditions: [{ value: conditionsArray }] })` | `conditions` param (not `search_conditions`), async |

**Critical: `SearchConditionArray.value` vs `SearchPane.conditions`**

`SearchPane.GetSearchCriteria()` returns `{ conditions: [...] }` but the `SearchConditionArray` gRPC type uses `{ value: [...] }`. You MUST remap when passing to `SearchObjects`:

```javascript
const criteria = await shellFrame.SearchPane.GetSearchCriteria();
// criteria = { conditions: [ {expression, type, value}, ... ] }

// WRONG — conditions silently ignored, returns ALL objects:
await vault.searchOperations.SearchObjects({ conditions: [criteria] });

// CORRECT — remap "conditions" to "value":
await vault.searchOperations.SearchObjects({
    conditions: [{ value: criteria.conditions }],
    limit: 0,
    timeout_in_seconds: 60
});
```
- `ObjectOperations.GetLatestObjectVersionAndProperties` → `GetObjectDataOfMultipleObjects`.
- `ObjectOperations.GetObjectInfo` → `GetObjectDataOfMultipleObjects` with needed flags.
- `ObjectOperations.GetMFilesURLForObject` → `GetWebLink`.
- `ObjectOperations.CheckOut` / `CheckIn` → `CheckOutMultiple` / `CheckInMultiple`.
- `ObjectOperations.CreateNewObject` / `CreateNewObjectEx` → `AddObjectWithFiles`.
- `ObjectPropertyOperations.SetProperty` → `SetPropertiesMultiple`.
- `ObjectOperations.GetObjectPermissions` / `IObjectVersionPermissions.AccessControlList` → `GetEffectivePermissions`.

Unsupported/deprecated feature checks to enforce:
- `IShellUI.CreatePersistentBrowserContent` is deprecated and not supported in UIX2.
- Detect and block ActiveX/COM usage (`ActiveXObject`, `WScript.Shell`, `Outlook.Application`, `Scripting.FileSystemObject`, `Shell.Application`, `MFilesAPI.MFilesClientApplication`).
- Detect unsupported legacy browser APIs (`navigator.msSaveOrOpenBlob`, `msFullscreenElement`).
- For `window.open`, `window.alert`, `window.prompt`: these require explicit sandbox attributes (`allow-popups`, `allow-modals`) in `appdef.xml`. Document the decision in conversion notes. See [Sandbox Attributes Support](https://developer.m-files.com/Frameworks/User-Interface-Extensibility-Framework/Reference/Samples/SandboxAttributesSupport/).

### ActiveX/COM blocker resolution (mandatory)

For every ActiveX/COM blocker found, consult the official deprecated features reference for recommended alternatives:
- **Reference:** https://developer.m-files.com/Frameworks/User-Interface-Extensibility-Framework/Reference/Upgrading/deprecated_features/#activex-and-com-objects

Do **not** default to a single replacement. For each blocker, document **all viable alternatives** with trade-offs so the user can make an informed choice. Consider:
- What the original code actually does (read the code, don't assume from the API name)
- Whether the replacement preserves the original user experience (e.g., user review step vs auto-send)
- Client-side alternatives (modern web APIs, `mailto:`, `OpenExternalWebLink()`)
- Server-side alternatives (VAF + SMTP, Graph API, file generation)
- Hybrid approaches (VAF generates artifact, client downloads/opens it)

#### `WScript.Shell` use-case breakdown

`WScript.Shell` is used for multiple distinct purposes. Each requires a different migration path:

| Use Case | What Code Does | UIX2 Alternative | Platform | Notes |
|----------|---------------|------------------|----------|-------|
| **Launch EXE** | `WScript.Shell.Run("app.exe args")` | VAF extension method that performs the equivalent logic server-side; or `MFiles.OpenExternalWebLink()` if the EXE just opens a URL/file | Desktop+Web (VAF) / Desktop-only (OpenExternalWebLink) | If core business logic lives in the EXE, treat the EXE source code as primary spec input (see below) |
| **Open file/URL** | `WScript.Shell.Run("<web-url>")` or `WScript.Shell.Run("file.pdf")` | `await MFiles.OpenExternalWebLink(url)` for `http`/`https`/`mailto` only; local `file://` paths are NOT supported — use VAF for file operations | Desktop+Web | Only web URLs and mailto links; local file launches require VAF |
| **Run batch/script** | `WScript.Shell.Run("script.bat")` | Move logic to VAF extension method | Desktop+Web (via VAF) | Batch scripts cannot run from sandboxed iframe |
| **Read registry** | `WScript.Shell.RegRead(...)` | VAF extension method that reads registry server-side; or move config to Named Value Storage | Desktop+Web (via VAF) | Registry access is never available in web client |
| **Write file** | `WScript.Shell` + `Scripting.FileSystemObject` | VAF extension method; or Blob download via dashboard | Desktop+Web (via VAF) | Local filesystem access is fully blocked in UIX2 |
| **Send keystrokes** | `WScript.Shell.SendKeys(...)` | No equivalent — feature must be redesigned or dropped | N/A | Keystroke injection is fundamentally incompatible with web |

#### EXE companion tool migration (critical)

When a UIX1 app launches a companion `.exe` (e.g., `WScript.Shell.Run("VersionCompareTool.exe")`), the migration risk is commonly underestimated because the UIX1 shell script looks simple. **The core business logic lives in the EXE, not in `shellui.js`.**

**Mandatory steps for EXE-launch patterns:**
1. **Read the EXE source code immediately** — treat it as primary functional spec input, not an afterthought
2. **Document all EXE functionality** in `SPEC.md` under a dedicated section
3. **Assess EXE complexity** — this drives the real effort estimate, not the UIX1 shell code
4. **Choose migration path:**
   - **Simple EXE logic:** Port to VAF extension method + UIX2 dashboard UI
   - **Complex EXE with WinForms/WPF:** Port business logic to VAF, build equivalent UI as React dashboard
   - **EXE requires local resources:** May be a blocker for web client — document trade-offs
5. **Update backend classification** — EXE-based apps almost always require `Backend modification required`

> **Lesson learned — default to backend-bridge-first:** Any legacy app that performs vault searches, document reads, or metadata operations *outside* the UIX1 shell script (e.g., in a companion EXE, COM process, or desktop automation tool) should default to Level 2 (VAF extension bridge) from the start. Do NOT spend iterations trying UIX2 direct calls (`SearchObjects`, `GetObjectDataOfMultipleObjects`, `GetProperties`) for operations that the legacy code performed server-side or in a privileged desktop process. The UIX2 sandbox and gRPC proxy layer often cannot replicate what COM-based vault operations did. The spec tells you where the operations happened — trust it.

#### `Outlook.Application` example

- `mailto:` link via `OpenExternalWebLink()` — simple, no attachment support
- VAF generates `.eml` file, client downloads and opens — preserves attachment + user review
- VAF sends via SMTP/Graph API — auto-sends, changes behavior (no user review)

List alternatives in the migration assessment's Blocker Analysis section with a clear recommendation and trade-off notes for the user to decide.

## Finalization checklist (mandatory)

- Validate `appdef.xml` against UIX2 schema (`appdef-client-v5.xsd`).
- Confirm each `shellui` module has exactly one `<file>` entry (single merged JS module payload).
- Confirm analyzer was executed on legacy archives (Phase 0) and report artifacts are present in notes/.
- Confirm verifier (`verify_ts_output.js`) was executed on the conversion target directory (either `converted-uix2/` or `src/Frontend/TemplateApp.UIExt/` depending on workflow) in `--strict` mode and findings are resolved or justified in notes. Do NOT run the analyzer on source folders — it only accepts archives.
- Run deprecated-API scan and confirm all mapped replacements above are applied or explicitly documented as blocked.
- **Dashboard protocol script check:** Confirm every dashboard HTML file includes `<script src="mfiles.extensibility.protocol.js"></script>` in `<head>` before any other scripts. This applies to both plain HTML dashboards and React bridge HTML files. Without this script, M-Files will NEVER call `OnNewDashboard` — the dashboard renders but stays blank with no errors. This file is served by M-Files at runtime — do not include it in source, do not try to create it, and **do not remove it if the verifier flags it as missing** (known false positive).
- **Dashboard communication fallback:** If the migrated workflow needs ShellUI ↔ Dashboard round-tripping, prefer `UpdateCustomData()` on the dashboard plus `MFiles.Event.CustomDataChanged` on the ShellUI side. Do not assume UIX1-era patterns such as `CustomEvent` exist in the active UIX2 proxy. If a method is unexpectedly missing, log available members with `Object.keys(...)` before changing direction.
- **Runtime Smoke Gate passed:** Confirm the smoke test checklist above has been completed and all items pass. If reclassification occurred, confirm the assessment delta log is updated.
- Repackage and smoke-check migrated app package.
- Verify and align with [.github/skills/uix2-app/SKILL.md](../uix2-app/SKILL.md) constraints before final delivery.

### Graduation checklist (production integration)

> **Direct workflow:** If you used the direct workflow, code is already in `src/Frontend/TemplateApp.UIExt/`. Skip to the "Confirm `appdef.xml`" step below and continue from there.

**The Backend steps below are conditional on the backend classification from the migration assessment.**

- **Scratch workflow only:** Confirm converted UIX2 code has been integrated into `src/Frontend/TemplateApp.UIExt/` (not left in `converted-uix2/`).
- Confirm `appdef.xml` in `src/Frontend/` has been updated with new files, dashboards, and resources.
- **If `Frontend-only`:** No Backend graduation needed. Remove `<master-application-guid>` from frontend `appdef.xml` if present. Remove the template Backend project from the solution (`Uixv2Template.sln`) so it is not built or deployed — it is unrelated placeholder code. Skip all Backend build/deploy steps below.
- **If `Existing VAF as-is`:** No Backend changes needed. Document which existing VAF is reused. Remove the template Backend project from the solution (`Uixv2Template.sln`) — the migrated frontend depends on an external VAF, not the template. Skip Backend build steps but ensure the existing external VAF remains deployed. Verify frontend extension method calls match the existing VAF's method names and input/output contracts.
- **If `Existing VAF merge`:**
   - **Ask the user:** Should the original VAF application GUID be preserved in `src/Backend/` `appdef.xml`? Preserving the GUID allows in-place upgrade on existing vault installations (no uninstall/reinstall). Using a new GUID creates a separate application (old one must be manually uninstalled).
   - Migrate/merge the legacy VAF code into `src/Backend/TemplateApp.VAF/`, updating to the current VAF framework version.
   - If preserving the GUID: replace the `<guid>` in `src/Backend/TemplateApp.VAF/appdef.xml` with the original VAF's GUID. Set `<version>` higher than the currently deployed version.
   - Confirm extension methods, event handlers, and configuration from the original VAF are carried over or intentionally dropped (document any dropped functionality).
- **If `Backend modification required`:**
   - Confirm VAF backend code has been integrated into `src/Backend/TemplateApp.VAF/`.
   - Confirm `appdef.xml` in `src/Backend/` has been updated with new extension methods.
   - Confirm version numbers have been incremented in both `appdef.xml` files.
   - Confirm Backend builds: `dotnet build Uixv2Template.sln`
- **Align application identity surfaces:** Do not stop at namespaces or method names. Confirm the migrated app's identity is consistent across all relevant surfaces:
   - Frontend `appdef.xml` `<name>` should be `{AppName}`
   - Backend `appdef.xml` `<name>` should be `{AppName}.VAF` if a backend is part of the migrated app
   - Backend `.csproj` `AssemblyName`, `.csproj` `RootNamespace`, backend `appdef.xml` `<assembly>`, and the extension-method class namespace should agree when a backend is part of the migrated app
   - Frontend and Backend should have aligned `<version>`, `<publisher>`, and `<copyright>` values when both ship together
   - Review project/folder names, namespaces, extension method names, package filenames, and deploy logs for leftover template names such as `TemplateApp`
   - Note: Backend `.mfappx` filename derives from `.csproj`/folder naming, but the display name in M-Files Admin comes from `<name>` in `appdef.xml`
- **Verify `build-package.ps1` collects all files:** The build script reads `appdef.xml` dynamically to determine which files go into the `.mfappx` package. It must collect files from BOTH `<modules>` (e.g., `main.js`) AND `<resources>` (e.g., dashboards, CSS, images). If new files were added during migration, confirm they are listed in the appropriate `appdef.xml` section. If the build script only reads `<resources>`, fix it to also read `<modules>`.
- Confirm Frontend version has been incremented in `appdef.xml`.
- Confirm the Frontend build script works: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "build/scripts/build-and-deploy-frontend.ps1" -BuildOnly`
- **Verify package contents:** Check the build output log to confirm ALL expected files are listed as "Copied:" — especially `main.js` (module entry point). A missing module file means the extension installs but never starts (no console output, no errors). This is the #1 packaging mistake.
- Confirm ESLint passes: `cd src/Frontend/TemplateApp.UIExt && npm run lint`
- The `src/Legacy/` workspace (source-uix1, notes, and converted-uix2 if scratch workflow was used) remains intact for traceability.
- **Post-conversion smoke test:** After deploying the build from `src/Frontend/` (and `src/Backend/` if applicable), run the Runtime Smoke Gate checklist again on the production build. This catches packaging/path issues.

## Analyzer quick start

- Run portfolio scan directly with the analyzer script.
- Recommended baseline command pattern:
   - `node scripts/uix_analyzer.js --path <apps-folder> -recursive --html`
- Use outputs (`stats.json`, `stats-merged.json`, HTML report) to drive migration classification.

> Important: analyzer results are **directional** (suuntaa-antavia), not absolute truth. Always validate findings against extracted source files before final conversion decisions.

## Quick triage checklist

- Uses `ActiveXObject`? → high-risk/manual redesign.
- Uses TaskPane/TaskPane command group APIs? → convert to Taskbar (`ICommands`) mapping.
- Uses `SetIconFromPath`, `ExecuteURL`, `CreateInstance`, or `SessionInfo.ClientCulture`? → apply mandatory replacements.
- Uses sync COM APIs heavily? → codemod + adapter candidate.
- Uses TaskPane APIs? → map to top menu/taskbar.
- Sends callbacks/functions to dashboards? → redesign with command/message callbacks.
- Uses offline/client-only APIs? → capability-gap review.
- Depends on `vaultui` or `vaultcore` modules? → redesign needed.

## Runtime Issues Discovered During Migration

These issues are NOT obvious from documentation and were discovered via actual runtime testing:

### API Differences (UIX1 → UIX2)

| UIX1 API | UIX2 Status | Fix |
|----------|-------------|-----|
| `vault.GetGUID()` | **Does not exist** | Use VAF extension method to return GUID, or remove feature |
| `ServerVault.*` | **DataCloneError** | Avoid `ServerVault` - cannot serialize across MESP boundary in web |
| `MenuLocation_ContextMenu_Top` | **Does not exist** | Use `MenuLocation_ContextMenu_Bottom` only |
| `CommandState_Inactive` | **Does not exist** | UIX2 only has `CommandState_Active` and `CommandState_Hidden` |
| `MenuLocation_TaskPane_ViewAndModify` | **Does not exist** | Use `MenuLocation_TaskBar_MainActions` or other `TaskBar_*` variants |
| `new MFiles.SearchCriteria()` / `new MFiles.View()` | **Not available** | `MFiles.SearchConditionArray` is NOT a constructor at runtime — use plain objects `{ value: [...] }` |

### Dashboard Debugging

| Issue | Symptom | Fix |
|-------|---------|-----|
| Dashboard `console.log()` invisible | Logs from `OnNewDashboard` don't appear in parent console | Dashboard runs in sandboxed iframe — switch dev tools context selector to the dashboard iframe to see its logs |

### VAF Extension Method Responses

| Issue | Symptom | Fix |
|-------|---------|-----|
| Empty string config values | UI labels/buttons appear blank | VAF may return empty strings (`""`) for unconfigured fields. Always use `value \|\| "fallback"` for user-visible strings |

### Method Signatures Changed

| Method | UIX1 | UIX2 |
|--------|------|------|
| `CreateTaskbarGroup` | May accept 1-2 args | **Requires all 3**: `(name, location, priority)` |

### Timing/Lifecycle Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| SelectionChanged fires before Started | `commandId is Null` | Guard: `if (!Commands.myCommand) return;` |
| ShowContextMenu renders before async completes | Context menu shows stale data | Create commands in `SelectionChanged`, not `ShowContextMenu` |

### SearchReady Event (Web Client)

| Issue | Symptom | Fix |
|-------|---------|-----|
| `SearchReady` event doesn't fire reliably on web | Task pane commands never appear | Create task pane/taskbar commands in `Started` event instead of `SearchReady` |

### Clipboard API Restriction

| Issue | Error | Fix |
|-------|-------|-----|
| Document not focused | `NotAllowedError: Document is not focused` | Use `document.execCommand('copy')` first, Clipboard API as fallback |

See: [UIX2 Troubleshooting](../uix2-app/references/troubleshooting.md#uix2-api-gotchas-discovered-via-migration)

## Main migration strategy

- Keep auto-fixes deterministic.
- Emulate high-frequency UIXv1 patterns with adapter wrappers.
- Detect unsupported features early and fail with clear guidance.

## Reference map

- SPEC.md template (Phase 0): [references/spec-template.md](references/spec-template.md)
- Migration assessment template (Phase 0): [references/assessment-template.md](references/assessment-template.md)
- Overview: [references/migration-overview.md](references/migration-overview.md)
- App manifest migration (v4 → v5): [references/appdef-migration.md](references/appdef-migration.md)
- Compatibility challenges: [references/compatibility-challenges.md](references/compatibility-challenges.md)
- Adapter layer: [references/adapter-layer.md](references/adapter-layer.md)
- Codemod: [references/codemod.md](references/codemod.md)
- Analyzer: [references/analyzer.md](references/analyzer.md)
- Findings and estimates: [references/findings-and-estimates.md](references/findings-and-estimates.md)
