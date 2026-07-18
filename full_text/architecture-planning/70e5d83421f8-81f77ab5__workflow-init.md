---
name: workflow-init
description: Bootstrap a new project with a guided discovery interview — installs the starter, scaffolds the framework, configures a framework-aware CI/CD and PR workflow, suggests MCPs based on stack, proposes a roadmap, fills the strategy/overview/spec templates, then recommends a first feature. Optional argument is the target directory; defaults to the current working directory. Supports Claude Code, Codex, and any AI agent that loads agent skills.
---

# Workflow Init

> **Cross-agent note**: where this skill says "use a structured-question prompt," use whatever mechanism your agent offers. In Claude Code that's `AskUserQuestion`. In Codex / other agents, it's natural-language prose with clear option lists. Same end behavior — the agent presents 2-4 choices, the user picks one.

End-to-end project bootstrap. Ten stages, executed sequentially:

```
0  Idempotency check       (skip stages already done if re-run)
1  Pre-flight              (project type → target dir → scaffold/existing → AI-native? → framework → shadcn → preset → starter UI)
2  Scaffold                (only for new Web projects — run create-* commands)
3  Install workflow files  (drop CLAUDE.md / AGENTS.md / GEMINI.md / docs/ / .claude/ / .agents/)
4  Discovery interview     (identity → stack → strategy → surfaces, with elaboration)
5  Repository + delivery + MCP setup (GitHub/hosting, CI/CD, project tracking, pick MCPs)
6  Roadmap proposal        (draft + iterate + save — skipped for existing projects)
7  Fill templates          (edit all template files; delivery status and MCP commands recorded)
8  Recommend first feature (pick from roadmap's "Now" milestone)
9  Hand off                (repo/delivery status + MCP install commands + next steps)
```

**🚨 Critical ordering rule:** MCP installs require an agent restart, which wipes conversation context. Stage 5 can optionally connect GitHub/hosting because that does not require an agent restart, but Stage 5 only picks MCPs and never installs them. MCP install commands surface at Stage 9 — *after* Stages 6-7 have written every interview answer, roadmap entry, and template to disk. By then a restart is harmless.

> **The workflow is project-agnostic.** Web app, backend service, mobile, CLI tool, library — the docs (thesis, overview, roadmap, feature specs) work for any codebase. Only **Stage 2 (scaffold)** is web-specific because that's the only category with reliable, tested scaffolders. Non-web projects skip Stage 2 and get the docs installed in their existing/empty directory; the user runs whatever init their stack needs (e.g. `cargo init`, `python -m venv`, `flutter create`) themselves.

Don't dump templates and walk away. The template files (thesis, overview, spec, root briefs, roadmap) have `{{Placeholders}}` and `[Replace with...]` prompts — those need real content to be useful, and the user has the answers in their head right now. The interview surfaces them.

## Stage 0 — Idempotency check

Before anything else, check if `/workflow-init` has run before in this target. Look for either of:

- `docs/context/current-feature.md` exists and has content beyond the empty placeholder comments
- `docs/context/roadmap.md` exists and has content beyond the empty template

If yes, ask the user:

> "This project already has workflow files. Do you want to:
> - **Resume** — keep existing context, just check what's set up
> - **Refresh skill files only** — re-install `.claude/skills/` and `.agents/skills/` if they've moved
> - **Start fresh** — wipe and re-run the full interview (destructive)
> - **Abort** — leave things alone"

Default to "Resume." Only run the full interview if the user explicitly asks for "Start fresh." This protects against accidental re-runs trashing their populated docs.

If no prior install detected, proceed normally.

## Stage 1 — Pre-flight

Decide the working location:

1. If the user provided a target directory after the command name → that's the **parent** directory (where the new project lives or will live). Resolve relative paths against the user's current working directory.
2. If no target was provided → use the current working directory as the parent.

Ask the user the relevant sub-questions in sequence (each is a separate structured-question prompt or short prose prompt because options differ).

### 1.1 What kind of project?

Four options:

| Option | Examples |
|---|---|
| **Web app or site** *(recommended for most)* | Dashboard, marketing site, docs site, web app, e-commerce |
| **Backend / API / service** | REST API, GraphQL service, worker, daemon, microservice |
| **Mobile or desktop app** | iOS / Android / Expo / Flutter / Tauri / Electron / egui / gpui / SwiftUI / WPF / Qt — anything not running in a browser tab |
| **Other** | CLI tool, library/package, data/ML project, custom stack |

This decides whether Stage 2 (scaffold) runs:

- **Web** → immediately ask the AI-native follow-up below, then continue to 1.2 (we have tested scaffolders for AI Elements, Next.js, Astro, SvelteKit, and TanStack Start).
- **Backend / Mobile / Desktop / Other** → SKIP Stages 1.2 through 1.7 and Stage 2 entirely. The workflow installs the docs into the parent directory; the user runs whatever init their stack needs themselves (e.g. `cargo init`, `python -m venv`, `flutter create`, `npx create-hono`). Go directly to Stage 3.

> **Why no backend/mobile scaffolders?** Those ecosystems have many equally valid tools and the "right" choice varies by team. Rather than pick one and be wrong half the time, we let the user run their stack's idiomatic init command separately. The workflow's value (docs + skills + agents) applies regardless.

If the user picked **Web**, ask one follow-up before 1.2:

> "Is this an AI-native web app? Examples: chatbot, agent workspace, AI dashboard, prompt tool, model-powered workflow, voice/chat UI."

Two options:

| Option | What happens |
|---|---|
| **No, regular web app/site** *(recommended unless AI UI is central)* | Continue through the normal framework + shadcn path below. |
| **Yes, AI-native app** | If scaffolding new, Stage 2 uses `npx -y ai-elements@latest` instead of the normal framework/shadcn path. |

Capture this as `ai_native_web_app: yes | no`. If yes and the user is scaffolding a new project, skip Stages 1.3 through 1.7 entirely — the AI Elements CLI asks for framework, component library, and preset/theme itself.

### 1.2 New project or existing? *(only if Web in 1.1)*

Two options:

- **Scaffold a new project** — agent runs a `create-*` command in Stage 2
- **Use existing project** — agent skips scaffolding entirely

If "Use existing project" → jump straight to Stage 3 (install workflow files). Skip 1.3 through 1.7 and Stage 2 entirely.

### 1.3 Which framework? *(only if scaffolding a new non-AI Web project)*

Skip this if `ai_native_web_app = yes`; the AI Elements CLI handles the framework prompt.

Four options:

| Option | What runs (high-level) |
|---|---|
| **Next.js** *(recommended)* | With shadcn → `shadcn@latest init --template next` (single-command scaffold). Without → `create-next-app` (TS + Tailwind + App Router + Turbopack) |
| **Astro** | With shadcn → `shadcn@latest init --template astro` (scaffolds + React + Tailwind + shadcn in one). Without → `npm create astro` + `astro add tailwind` |
| **SvelteKit** | `sv create` (minimal, TS) + `sv add tailwindcss`. shadcn opt-in uses `shadcn-svelte` (community Svelte port) |
| **TanStack Start** | With shadcn → `shadcn@latest init --template start`. Without → `create-tsrouter-app` with Start + Tailwind + ESLint + Prettier add-ons |

Frame: "Which framework?" — recommend Next.js as the default for new React UI projects.

### 1.4 Add shadcn? *(only if a framework was picked)*

Two options. Contextual framing per framework:

- **Next.js / TanStack Start**: "Add shadcn for UI components? (Recommended — most React + Tailwind projects use it.)"
- **Astro**: "Add shadcn for React UI islands? (Optional — useful for interactive components on a content site.)"
- **SvelteKit**: "Add shadcn-svelte for UI components? (Community port of shadcn for Svelte.)"

### 1.5 shadcn preset? *(only if official shadcn was picked)*

Ask this only when the user picked the official `shadcn` CLI path:

- Next.js + shadcn
- Astro + shadcn
- TanStack Start + shadcn

Do **not** ask this for SvelteKit + shadcn-svelte; that is a different CLI.

Ask in prose:

> "Which shadcn preset should we use? Press Enter for `b0`. You can create or browse presets at https://ui.shadcn.com/create — click **Get Code**, then copy only the preset token between `--preset` and `--template` (for example, `b5eZT0sHS`)."

Rules:

- If the user presses Enter or sends an empty answer, set `$SHADCN_PRESET` to `b0`.
- Otherwise trim the answer and use it exactly as `$SHADCN_PRESET`.
- If the user pastes a full shadcn command from **Get Code**, extract only the token after `--preset` and before the next flag (usually `--template`) and use that as `$SHADCN_PRESET`.
- Do not invent preset names from memory.
- If the chosen preset is rejected by the CLI, follow the invalid-preset handler in Stage 2.2.

### 1.6 Include starter UI? *(only if Next.js + shadcn was picked)*

Two options:

| Option | What runs |
|---|---|
| **No** *(recommended if the user wants to design from scratch)* | No block install. Keep the base shadcn scaffold only. |
| **Yes** | Ask Stage 1.7 for which starter UI to install. |

Frame: "Include starter UI?"

Only ask this for **Next.js + shadcn**. The official shadcn blocks write an App Router-shaped route such as `app/dashboard/page.tsx`; do not auto-install them into Astro, SvelteKit, or TanStack Start unless the user explicitly asks for adaptation work.

### 1.7 Starter UI style? *(only if Stage 1.6 is Yes)*

Two options:

| Option | What runs |
|---|---|
| **Minimal** | Clone `arhamkhnz/next-shadcn-admin-dashboard`, then prune it down to the sidebar shell and a blank dashboard page. |
| **Regular starter** *(recommended for dashboards/admin apps)* | Clone `arhamkhnz/next-shadcn-admin-dashboard` as the full Studio Admin-style dashboard template. |

Frame: "Which starter UI should we install: Minimal or Regular starter?"

### Branch summary

| 1.1 type | 1.2 new/existing | Path |
|---|---|---|
| Backend / Mobile / Desktop / Other | (skipped) | → Stage 3 (docs only) |
| Web | Existing project | → Stage 3 (docs only) |
| Web | New + AI-native app | → Stage 2 with `ai-elements@latest` → Stage 3 |
| Web | New + Next.js (± shadcn, optional starter UI) | → Stage 2 → Stage 3 |
| Web | New + Astro (± shadcn) | → Stage 2 → Stage 3 |
| Web | New + SvelteKit (± shadcn-svelte) | → Stage 2 → Stage 3 |
| Web | New + TanStack Start (± shadcn) | → Stage 2 → Stage 3 |

## Stage 2 — Scaffold

Only run this if a new Web scaffold was chosen in Stage 1, either the normal framework path or the AI Elements path.

> **Critical: keep `-y` in every `npx -y <command>`.** Without it, npx asks "Ok to proceed? (y)" before downloading the package the first time, and an agent session **cannot auto-respond** to that prompt — the user would have to manually type `y` in the shell. Each command below has `-y` in the right position; do not drop it. The `--yes` later in the command (for `create-next-app`, `shadcn`, etc.) is a different flag — that one accepts the framework's defaults. Both are needed.

### 2.1 Project name

Ask in prose: "What should we name the project? (lowercase, hyphens — this becomes the directory name and the `name` field in `package.json`)."

Invoke the elaboration loop if the user wants to brainstorm names. Once settled, paraphrase: "So the project name is `<name>` — directory will be `<parent>/<name>`. Sound good?"

### 2.2 Run the scaffolder

Pick the command set based on the user's Stage 1 choices.

**For AI-native Web app (interactive AI Elements scaffold):**

```bash
cd "$PARENT" && npx -y ai-elements@latest
```

This is the Vercel AI Elements path. It scaffolds an AI-native frontend and sets up shadcn/ui through the AI Elements CLI instead of the normal `shadcn init` path. AI Elements is a custom registry built on shadcn/ui, so this branch still lands in the shadcn component model the user prefers.

Important behavior:

- Run this in an interactive TTY. The CLI uses arrow-key prompts; if the command prints a prompt and exits or hangs in a non-TTY tool, rerun it with a TTY. If the current agent cannot provide a TTY, ask the user to run the command manually in their terminal, then resume at Stage 3 with the created directory.
- Run it from a parent/workspace directory that does **not** contain a `package.json` when the intent is to create a new subproject. If `$PARENT/package.json` exists, the CLI may install AI Elements into that existing project instead of creating `<name>`. In that case, stop and ask whether to use the existing project or choose a different parent directory.
- When prompted to start a new project, choose the user's requested framework. If they have no preference, choose **Next.js**.
- When prompted for the project name, enter `<name>` from Stage 2.1.
- When prompted for component library, choose **Radix** unless the user asked for another option.
- When prompted for preset/theme, let the user choose if they care. If they do not, choose **Mira** when it is listed; otherwise ask from the live list the CLI shows. Do not invent preset names from memory.
- Do not ask the separate shadcn preset question, do not run `shadcn init`, and do not offer the Next.js admin starter UI after this path. AI Elements is the scaffold/UI route for AI-native apps.

After the command finishes, verify which directory was created by checking for `<name>/package.json`. If the CLI created a different directory name, set `$TARGET` to the actual generated project directory and use that name in the docs.

**For Next.js + shadcn + No starter UI (use shadcn's unified scaffolder — one command):**

```bash
SHADCN_PRESET="<preset-from-stage-1.5>"
cd "$PARENT" && npx -y shadcn@latest init \
  --template next \
  --name <name> \
  --preset "$SHADCN_PRESET" \
  --yes
```

This is the modern path. shadcn scaffolds Next.js + installs shadcn in one step. Different (and slightly better) result than `create-next-app` followed by `shadcn init` — fewer post-hoc config tweaks, shadcn's preferred defaults baked in.

> **Why every flag matters (DO NOT drop any):**
> - `--template next` — picks the Next.js template
> - `--name <name>` — sets project + directory name (skips "what's your project name?" prompt)
> - `--preset "$SHADCN_PRESET"` — uses the user's selected preset, defaulting to `b0` on blank input. **A preset is a complete config bundle** — it encodes the component library, monorepo decision, color scheme, and other choices in one go. This is the single flag that prevents shadcn from asking interactive questions.
> - `--yes` — accepts remaining defaults (separate from the `-y` after `npx`)
>
> Without `--preset`, shadcn's init can hang on arrow-key prompts ("Select a component library", "Which preset?") that an agent session can't auto-respond to. Don't try to add `--base radix` / `--no-monorepo` etc. separately unless the user explicitly asks — those choices belong to the preset and add surface area for CLI drift.

**For Next.js + shadcn + Regular starter (clone the admin dashboard template):**

```bash
cd "$PARENT" && git clone --depth 1 \
  https://github.com/arhamkhnz/next-shadcn-admin-dashboard.git \
  <name>

cd "$PARENT/<name>" && rm -rf .git media
cd "$PARENT/<name>" && npm pkg set name="<name>" version="0.0.1"
cd "$PARENT/<name>" && npm install
```

This uses the user's preferred template directly: `arhamkhnz/next-shadcn-admin-dashboard`. It is a full Next.js 16 + shadcn admin template with the sidebar, multiple dashboards, auth screens, theme/layout controls, data tables, and supporting dependencies.

Important: this path does **not** run `shadcn init`. The template is already a complete shadcn app. Stage 1.5 still captures the user's shadcn preset for the base/no-starter path and future context, but the cloned template ships its own theme/preset system.

Architecture reference: the admin dashboard explicitly follows the colocation-first pattern documented in `arhamkhnz/next-colocation-template`. When Stage 7 fills docs for this starter, mention that route-specific components and logic live beside their route segments, with shared primitives/config/hooks staying in top-level `src/components`, `src/config`, `src/hooks`, `src/lib`, and `src/navigation`.

**For Next.js + shadcn + Minimal starter (clone the same template, then prune):**

```bash
cd "$PARENT" && git clone --depth 1 \
  https://github.com/arhamkhnz/next-shadcn-admin-dashboard.git \
  <name>

cd "$PARENT/<name>" && rm -rf .git media
cd "$PARENT/<name>" && npm pkg set name="<name>" version="0.0.1"

# Keep the app shell/sidebar infrastructure, remove demo-heavy routes.
cd "$PARENT/<name>" && find 'src/app/(main)/dashboard' -mindepth 1 -maxdepth 1 \
  ! -name '_components' \
  ! -name 'layout.tsx' \
  ! -name 'page.tsx' \
  -exec rm -rf {} +

cd "$PARENT/<name>" && rm -rf 'src/app/(main)/mail'

cat > "$PARENT/<name>/src/app/(main)/dashboard/page.tsx" <<'EOF'
export default function Page() {
  return (
    <main className="flex min-h-[calc(100vh-var(--dashboard-header-height)-3rem)] flex-col gap-4">
      <section className="rounded-lg border border-dashed p-8">
        <h1 className="font-semibold text-2xl tracking-tight">Dashboard</h1>
        <p className="mt-2 max-w-2xl text-muted-foreground text-sm">
          Sidebar shell is installed. Replace this page with your first real screen.
        </p>
      </section>
    </main>
  );
}
EOF

cd "$PARENT/<name>" && npm install
```

This gives the project the same sidebar/layout/theme foundation as the regular template without bringing over all of the demo dashboard pages as starter content.

Architecture reference: keep the same colocation-first explanation as the Regular starter. Minimal still uses the dashboard template's `src/app/(main)/dashboard/layout.tsx`, `src/app/(main)/dashboard/_components/`, `src/navigation/sidebar/`, preferences store, and top-level shared UI/config folders.

**For Next.js without shadcn (Tailwind only, no UI lib):**

```bash
cd "$PARENT" && npx -y create-next-app@latest <name> \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --turbopack \
  --import-alias '@/*' \
  --use-npm \
  --yes
```

(All Next.js framework defaults included: TypeScript, Tailwind v4, ESLint, App Router, Turbopack, `@/*` import alias.)

**For Astro + shadcn (use shadcn's unified scaffolder — one command):**

```bash
SHADCN_PRESET="<preset-from-stage-1.5>"
cd "$PARENT" && npx -y shadcn@latest init \
  --template astro \
  --name <name> \
  --preset "$SHADCN_PRESET" \
  --yes
```

shadcn scaffolds Astro + adds React + Tailwind + initializes shadcn in one step. `--preset "$SHADCN_PRESET"` is the flag that prevents any interactive preset prompt — see the Next.js block above for the full rationale.

**For Astro without shadcn (content site, no React UI needed):**

```bash
cd "$PARENT" && npm create astro@latest <name> -- \
  --template minimal \
  --typescript strictest \
  --install \
  --no-git \
  --yes

cd "$PARENT/<name>" && npx -y astro add tailwind --yes
```

(Astro doesn't ship ESLint as a default convention — `astro check` is the type checker and Prettier handles formatting. Tailwind is added explicitly because no Astro template includes it by default.)

**For SvelteKit:**

```bash
cd "$PARENT" && npx -y sv create <name> \
  --template minimal \
  --types ts \
  --add-ons eslint,prettier,tailwindcss \
  --install npm \
  --no-git
```

(Adds the SvelteKit-recommended defaults: ESLint, Prettier, Tailwind. The `sv create` CLI handles all three as add-ons in one shot — no separate `sv add` step needed.)

If they picked **SvelteKit + shadcn-svelte**, follow up:

```bash
cd "$PARENT/<name>" && npx -y shadcn-svelte@latest init --base-color zinc
```

(Note: `shadcn-svelte` is the community Svelte port of shadcn, not the official `shadcn` CLI — different package.)

**For TanStack Start + shadcn (use shadcn's unified scaffolder — one command):**

```bash
SHADCN_PRESET="<preset-from-stage-1.5>"
cd "$PARENT" && npx -y shadcn@latest init \
  --template start \
  --name <name> \
  --preset "$SHADCN_PRESET" \
  --yes
```

shadcn scaffolds TanStack Start + initializes shadcn in one step. `--preset "$SHADCN_PRESET"` is the flag that prevents any interactive preset prompt — see the Next.js block above for the full rationale.

**For TanStack Start without shadcn:**

```bash
cd "$PARENT" && npx -y create-tsrouter-app@latest <name> \
  --add-ons start,tailwind,eslint,prettier \
  --package-manager npm
```

(Includes TanStack's recommended add-ons: Start SSR + Tailwind + ESLint + Prettier.)

CLI flag names occasionally shift between versions across all scaffolders. If a flag is rejected, drop the offending flag and re-run rather than tweaking endlessly — the defaults are reasonable. For the AI Elements path, prefer answering the CLI's live prompts over trying to force non-existent flags.

**Invalid shadcn preset handler:**

If `shadcn init` exits non-zero with an invalid preset error, do not retry the same command unchanged. Capture and show the useful part of the error, especially the `Available presets:` list if present. Then ask the user to pick one of the listed presets.

Example error shape:

```text
Invalid preset: b0. Available presets: nova, vega, maia, lyra, mira, luma, sera, rhea
```

Recovery flow:

1. Tell the user: "`<preset>` was rejected by the installed shadcn CLI. Available presets are: `<list>`."
2. Ask which listed preset to use. If `b0` is not in the list, do not present it as the default for the retry.
3. Set `$SHADCN_PRESET` to the user's listed choice and re-run the same scaffold command once.
4. If the retry fails, stop and offer Retry / Continue without shadcn / Abort.

**Known shadcn CLI shifts to watch for:**
- `--base-color zinc` (old) is gone from the official shadcn CLI path. Use `--preset "$SHADCN_PRESET"` instead.
- `npx shadcn@latest init --help` shows the `--preset` flag but may not list valid preset names. Invalid-preset errors often include the live `Available presets:` list; prefer that list over memory.

**If the scaffolder hangs on an interactive prompt anyway** (would mean `--preset "$SHADCN_PRESET"` isn't doing its job): do NOT pipe `printf 'N\n\n\n'` to dodge arrow-key prompts — it sometimes works for y/N but never works for arrow-key list pickers, and the agent will waste minutes retrying. Instead:
1. Cancel the hung command.
2. Fall back to the two-step path: run `create-next-app` (or framework-specific creator) without shadcn, THEN run `cd <name> && npx -y shadcn@latest init --preset "$SHADCN_PRESET" --yes` inside the freshly-created project.
3. Move on.

### 2.3 Starter UI note

There is no separate `shadcn add` step for starter UI. If Stage 1.6 selected **Yes**, the starter UI is handled in Stage 2.2 by cloning `arhamkhnz/next-shadcn-admin-dashboard` directly:

- **Minimal** clones the template and prunes it to the sidebar shell.
- **Regular starter** clones the full template.

Do not run `shadcn add sidebar-07` or `shadcn add dashboard-01` for this workflow. Those are official shadcn blocks, not the user's chosen template source.

### 2.4 Clear scaffolder-generated agent files

Some scaffolders (notably `create-next-app` ≥ v15) now generate their own `AGENTS.md` as part of the recommended defaults. **We always want our version** — that's the whole point of the workflow starter, and the scaffolder's version doesn't reference the `docs/context/*` structure.

Before Stage 3, scrub any agent files the scaffolder may have dropped:

```bash
cd "$PARENT/<name>" && rm -f AGENTS.md CLAUDE.md GEMINI.md
```

Don't ask the user about this — it's a structural fix, not a preference.

### 2.5 Set the target

The workflow target is now `$PARENT/<name>`. Set `$TARGET` to that absolute path for Stage 3.

### What if scaffolding fails?

If any command errors (network blip, flag mismatch in a newer version of the scaffolder, etc.), stop the flow. Report the error verbatim. Offer:

- **Retry** (most failures are transient)
- **Drop the failing step** (e.g., scaffold succeeded but shadcn init failed → continue with workflow install in the partly-scaffolded project)
- **Skip scaffolding entirely** and continue with workflow install only in the parent dir
- **Abort**

Don't silently continue past a failed scaffold.

## Stage 3 — Install workflow files

Sanity checks:
- If target doesn't exist, ask the user before creating it (`mkdir -p`).
- If target is empty (or just scaffolded), the CLI installs cleanly — proceed.
- If target has files unrelated to scaffolding, the CLI will detect conflicts and abort — surface that, don't bypass.

Run the install:

```bash
npx -y @digitaloutbreak/workflow init "$TARGET"
```

Quote the CLI's file list and next-steps output back to the user. Then tell them: **"Files are in. Let me ask you a few questions so we can fill them with real content instead of placeholders."**

## Stage 4 — Discovery interview

Use structured-question prompts for bounded choices, plain prose for open-ended ones. Run in rounds so the user isn't overwhelmed by a 10-question form.

### Elaboration loops — the universal rule for prose rounds

After the user's first answer to ANY prose question, do not race to the next question. Ask:

> "Want to dig into that more, refine it, or are you good to move on?"

Three modes:

1. **"Move on"** → record answer verbatim, advance.
2. **"Let me think out loud"** → engage. Follow-ups, mirror back, propose tighter phrasings, point out tensions.
3. **"Help me figure it out"** → recommend. Offer 2-3 framings from what's already known, ask which lands.

When you finally capture the answer, **paraphrase back in one sentence** and confirm. "So you'd say: <X>. Sound right?" If they tweak, accept and move on.

### Round 1 — Identity (required, may iterate)

Ask in prose, one question at a time:
- "What's the project's name?" *(skip if already captured in Stage 2.1)*
- "One sentence — what does it do?"
- "Who's the primary user? (you / a team / a customer / the public)"

For each: ask → first answer → elaboration loop. The one-sentence description is the most worth iterating on.

### Round 2 — Tech stack (structured-question prompt)

**The exact questions depend on the project type from Stage 1.1.** Pick the matching block.

#### If project type = Web

**Framework is already known by the time Round 2 runs:**
- New + scaffolded → picked in Stage 1.3 (e.g., Next.js + shadcn)
- New + AI Elements scaffold → detect from `package.json` and `components.json`; record the UI layer as `AI Elements + shadcn/ui`
- Existing project → detect from `package.json` deps (`next` / `astro` / `svelte` / `@tanstack/start-router`) and confirm with the user

So skip the framework question. Ask the remaining 3:

1. **Database** — I'll add it later *(default)* / Postgres via Neon *(recommended)* / SQLite / None
2. **ORM** — I'll add it later *(default)* / Drizzle *(recommended)* / Prisma / None
3. **Auth** — I'll add it later *(default)* / Better Auth *(recommended)* / Clerk / None

#### If project type = Backend / API / service

Ask 4 sub-questions in one prompt:

1. **Runtime / language** — Node *(TypeScript)* / Bun *(TypeScript)* / Python / Go / Rust / Other
2. **Server framework** — I'll add it later *(default)* / Hono / Express / NestJS / FastAPI / Other
3. **Database** — I'll add it later *(default)* / Postgres / SQLite / MongoDB / None
4. **Auth** — I'll add it later *(default)* / JWT-only / Better Auth / Clerk / Auth0 / None

#### If project type = Mobile or desktop

The Mobile/Desktop space is too varied for a fixed dropdown — Tauri+React, egui, gpui, SwiftUI, Flutter, Electron, native iOS, native Android, Qt, slint, and a dozen others are all valid. Ask freeform questions with rich examples instead of a closed option list.

Ask 3 sub-questions in plain prose, one at a time:

1. **Stack** — "Describe your stack in one line. A few examples to anchor the answer:
   - `Tauri + React + TypeScript` (Rust shell with web UI inside)
   - `Electron + Svelte` (Node shell with web UI inside)
   - `egui` (pure Rust, immediate-mode GUI — like dear ImGui)
   - `gpui` (pure Rust, GPU-accelerated retained-mode — like Zed editor)
   - `iced` (pure Rust, Elm-style)
   - `SwiftUI` for macOS / iOS / both
   - `Flutter` for mobile / desktop / both (cross-platform Dart)
   - `React Native via Expo` (cross-platform JS)
   - `WinUI + C#` (Windows native)
   - `Qt + C++` (cross-platform native)
   - `Undecided — I'll pick during the project`

   Plain language is fine — I just need enough to know how to frame the rest."

2. **Local data** — "How will you store local data? Examples: SQLite, Core Data, Realm, Tauri SQL plugin, plain files, none, undecided."

3. **Auth** — "Auth, if any? Examples: Sign in with Apple, Better Auth, Clerk, Firebase Auth, custom, none."

### Adapt subsequent stages to the Mobile/Desktop stack answer

The agent uses the freeform Stack answer (Q1) to adapt downstream stages. Don't apply blindly — read what the user wrote and judge:

| Stack signal in Q1 | Agent adapts by |
|---|---|
| Mentions web-tech shell (Tauri, Electron, Neutralino, Wails) + a JS framework (React/Vue/Svelte/Solid) | Asks shadcn opt-in late ("Most React/Vue desktop GUIs use shadcn for the inner UI — want me to add a roadmap entry for installing it?"). Round 4 framing = "screens." MCPs: context7 + playwright (the inner UI is web). |
| Mentions pure Rust GUI (egui, gpui, iced, slint, druid) | NO shadcn. NO web-related MCPs. Round 4 framing = "panels" or "windows." MCPs: context7 only. Suggest `cargo` workflows in the roadmap. |
| Mentions Apple-native (SwiftUI, AppKit, UIKit) | NO shadcn. NO JS tooling. Round 4 framing = "screens" or "views." MCPs: context7 only. Suggest XCTest + Apple HIG in the roadmap. |
| Mentions Microsoft-native (WPF, WinUI, MAUI) | NO shadcn. NO JS tooling. MCPs: context7 only. Suggest XAML + .NET conventions. |
| Mentions cross-platform native (Flutter, Qt, KMP) | NO shadcn. MCPs: context7 only. Roadmap follows the framework's conventions (Flutter widgets, Qt slots/signals). |
| User said "Undecided" | Add a roadmap entry to the "Now" phase: "Decide UI framework — evaluate <2-3 candidates relevant to the project>." Defer all framework-specific advice until that decision lands. |

This isn't an exhaustive table — it's a sanity check. Use judgment. The point: **don't pretend egui or SwiftUI are web projects; don't pretend Tauri+React isn't.**

#### If project type = Other (CLI, library, ML/data, custom)

Ask 2 sub-questions in one prompt:

1. **Language / runtime** — Node *(TypeScript)* / Bun / Python / Go / Rust / Other
2. **Purpose** — CLI tool / Library or SDK / ML or data project / Other

Skip Database, ORM, Auth — these usually don't apply. If they do for a niche case, the user can mention it in the freeform Strategy round.

---

Semantic distinction (applies to all blocks):
- **"I'll add it later"** = wants one, just hasn't decided. Docs stay generic.
- **"None"** = doesn't need this layer at all.

**Skip ORM** if Database = None.

### Round 3 — Strategy (open-ended, expect iteration)

Longest round. Ask in prose, one at a time, elaboration loop after each:

- **"Why does this need to exist? In one or two sentences — the bet you're making."**
- **"What's your unfair advantage here?"**
- **"What's the smallest thing that proves the bet?"**

### Round 4 — Surfaces or entry points (structured-question prompt + elaboration if needed)

The framing depends on project type from Stage 1.1:

- **Web or Mobile/Desktop with screens** (web app, Tauri+React, SwiftUI, Flutter, etc.) — ask about *surfaces* (screens, pages, views). Suggest 2-4 plausible v1 surfaces. Multi-select with "let me describe in my own words" fallback.
- **Mobile/Desktop without traditional screens** (egui/gpui/iced — panel/window-based) — ask about *panels or windows*. "What are the 2-4 main panels/windows for v1?"
- **Backend / API / service** — ask about *endpoints or capabilities* instead. "What are the 2-4 most important endpoints or capabilities for v1? (e.g. `POST /users`, webhook receiver, background job, etc.)"
- **CLI tool** — ask about *commands*. "What are the 2-4 most important commands for v1?"
- **Library / SDK** — ask about *public API surface*. "What are the 2-4 most important functions/classes the library will expose in v1?"
- **ML or data project** — ask about *pipelines or notebooks*. "What are the 2-4 most important pipelines, notebooks, or analyses for v1?"

If pushed back, drop into elaboration. Whichever framing you use, capture 2-4 items — those drive the roadmap proposal and the first-feature recommendation.

## Stage 5 — Repository, delivery, and MCP setup

> **🚨 Critical workflow rule — DO NOT install MCPs at this stage.**
>
> MCP installs require an agent restart. A restart at Stage 5 destroys the conversation context, so everything captured in the discovery interview (Rounds 1-4) and the roadmap (Stage 6, not yet run) is **permanently lost** before Stage 7 writes it to disk. Stage 5 may connect GitHub/hosting if the user asks because those actions do not require an agent restart. But MCP installs stay decision-only here — pick which MCPs to recommend, then move on to Stages 6-7 so the docs are filled. Install commands surface in Stage 9 (hand-off), after every interview answer is safely persisted to the filesystem.

### Stage 5.0 — Repository, project tracking, and deployment setup (optional)

Ask in a structured prompt:

> "Do you want to connect this project to GitHub and a hosting provider now?"

Options:

| Option | What happens |
|---|---|
| **Skip for now** *(recommended if the project is exploratory)* | No repo or deploy setup. Docs record "not connected yet." |
| **Record plan only** | Ask provider choices and write the plan into `README.md` / `project-overview.md`, but do not connect anything. |
| **GitHub only** | Create/connect the GitHub repo if tools are available. Ask public/private. |
| **GitHub + hosting** | Create/connect GitHub and connect the selected hosting provider if tools are available. |

If the user chooses any option except "Skip for now", ask:

1. **GitHub visibility** — Public / Private. Default Private for client/internal/product work; Public only if the user explicitly chooses it.
2. **Hosting provider** — Vercel / Cloudflare Pages or Workers / Netlify / Other / None.
3. **GitHub Project** — Create or link one / Record a plan / Skip. Recommend a project for product work with a roadmap; skip it for tiny experiments or one-off libraries.
4. **Connect now or document commands only?** Default to "connect now" only when the relevant plugin/MCP/CLI is available and authenticated.

Safety rules:

- Do not create a public GitHub repo unless the user explicitly chose Public.
- Do not commit, push, deploy, link domains, or write provider environment variables without a direct yes in this stage.
- If the tree has untracked/generated scaffold files and the user wants GitHub setup, ask before creating the initial commit. Suggested commit message: `chore: bootstrap project`.
- If tools are not authenticated, do not keep retrying. Record the exact command(s) in docs and handoff instead.
- A GitHub Project is the execution view, while `docs/context/roadmap.md` remains the product-planning source of truth. Do not create two competing roadmaps.

Tool preference:

1. Prefer installed agent plugins/connectors when available (GitHub plugin for repository creation; Vercel plugin/MCP for Vercel project linking/deploy setup; Cloudflare plugin/Wrangler for Cloudflare; Netlify CLI if available).
2. Otherwise use authenticated local CLIs if present:
   - GitHub: `gh auth status`, then `gh repo create <owner>/<repo> --private|--public --source=. --remote=origin`
   - Vercel: `vercel link` / `vercel deploy` only if user explicitly asks to deploy
   - Cloudflare: `wrangler pages project create` or framework-specific Cloudflare setup
   - Netlify: `netlify init`
3. Otherwise document the setup steps and move on.

Record these captured decisions for Stage 7:

```text
repo_setup_mode: Skip | Record plan only | GitHub only | GitHub + hosting
github_visibility: Public | Private | n/a
github_repo: <owner>/<repo> | not connected
github_project: <owner/project-number + URL> | planned | skipped
hosting_provider: Vercel | Cloudflare | Netlify | Other | None
hosting_project: <name/url> | not connected
deployment_status: connected | planned | skipped
```

### Stage 5.1 — Delivery baseline

Ask:

> "Set up the pull-request and CI/CD baseline now?"

Options:

| Option | What happens |
|---|---|
| **Configure now** *(recommended for anything intended to ship)* | Generate project-specific CI, dependency updates, a pull-request template, tests where appropriate, and branch-protection steps. |
| **Record plan only** | Fill `delivery-workflow.md` with the pending setup and exact next actions. |
| **Skip for now** | Appropriate only for a disposable experiment. Record that delivery automation is intentionally absent. |

#### Detect before generating

Inspect the repository instead of assuming a stack:

1. Detect the package manager from the lockfile (`pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, `bun.lockb`, `package-lock.json`) or the ecosystem's standard tooling (`Cargo.lock`, `uv.lock`, `poetry.lock`, etc.).
2. Read the real scripts and tool configuration. Never invent `typecheck`, `lint`, `test`, `build`, format, audit, or browser-test commands that the project does not support.
3. Reuse existing CI, tests, and deployment configuration. Extend narrowly rather than replacing a working setup.
4. For an existing project, run the proposed commands locally before making them required in CI.

#### Files to configure

When GitHub is selected, create or update:

- `.github/workflows/quality.yml` with a stable job display name of `Quality`
- `.github/dependabot.yml` for the detected package ecosystem, using a low-noise weekly schedule
- `.github/pull_request_template.md` covering intent, changes, verification, screenshots or evidence, migrations, rollback, and remaining risk
- `docs/context/delivery-workflow.md` with the real commands and current automation status

CI rules:

- Use least-privilege workflow permissions, concurrency cancellation for superseded branch runs, a lockfile-based install, and pinned major versions or full commit SHAs for trusted GitHub Actions.
- Run all applicable existing gates: formatting check, production dependency audit, typecheck, lint, tests, build, and browser behavior tests.
- Do not turn pre-existing warnings into unrelated cleanup work. Record them separately unless they make the new gate unreliable.
- Keep the required context name stable as `Quality`; branch protection depends on it.

#### Behavior and smoke tests

- For a newly scaffolded Web project, add one small browser smoke test for the real initial route and run it in CI. Prefer the project's existing Playwright setup; if none exists, install and configure Playwright only when the scaffold has a reliable dev/start command.
- For an existing Web project, reuse its browser-test harness. Do not replace it or guess at authentication fixtures.
- For backend, CLI, mobile, desktop, and library projects, use the closest meaningful executable smoke test instead of forcing a browser test.
- If hosting is connected and there is a stable production URL, add or plan a post-merge smoke workflow that verifies the exact merged commit reached the provider before checking the primary health route or workflow.
- If exact-commit deployment verification cannot be configured safely yet, mark production smoke as `planned`; do not fake it with a generic URL ping.

#### Branch protection

Only enable protection after the workflow exists on GitHub and `Quality` has completed successfully at least once.
For a solo-maintained repository, use this default:

- Pull request required
- `Quality` required and branch must be current with the default branch
- Conversation resolution required
- Administrator enforcement enabled
- Linear history enabled
- Force pushes and branch deletion disabled
- Required approving reviews: `0`

Do not require deployment, secret-scanning, or review-bot contexts unless they are installed and report consistently.
Never use an administrator override to merge a failing pull request.

Capture for Stage 7 and Stage 9:

```text
delivery_setup_mode: Configure now | Record plan only | Skip
ci_status: configured | planned | skipped
behavior_test_status: configured | planned | not applicable
pull_request_template_status: configured | planned | skipped
dependency_updates_status: configured | planned | skipped
branch_protection_status: configured | pending first successful Quality run | planned | skipped
preview_status: configured | planned | not applicable
production_smoke_status: configured | planned | not applicable
```

### Stage 5.2 — Ask about external service calls

Before deciding which MCPs to suggest (or whether to skip the stage), ask in plain prose:

> "Quick check before I suggest MCPs: will this project call any external services from code? Examples: Stripe / payment processors, OpenAI / AI providers, Vercel deploys, Figma, lead systems like GHL, transactional email, analytics, etc. Just a yes/no or a quick list of which ones."

This drives two decisions:
- Whether to skip the MCP recommendation subsection (skip rule below)
- Which MCPs to suggest (a "yes, Stripe" answer pulls Stripe MCP into the list)

### Skip rule

> **Skip MCP recommendations if the project is "simple"** — defined as ALL of:
> - Database = None
> - Auth = None
> - User answered "no" to the external-services question (Stage 5.2)
>
> Examples that skip: portfolio sites, static content pages, pure CLI utilities with no external calls, libraries with no external integrations. MCPs don't help much when there's no data layer or external behavior to talk to.

For non-simple projects, based on Round 2 stack picks, propose MCPs that make agent work meaningfully faster on this stack. Explain MCP concept first if the user looks unfamiliar:

> **What's MCP?** Model Context Protocol — lets me talk to external tools (your database, docs sites, your browser) directly instead of you copy-pasting things. Plugins for the agent. Quick install per MCP, big quality-of-life win.

Then suggest based on stack:

| Stack pick | MCP to suggest | What it unlocks |
|---|---|---|
| Postgres via Neon | `neon` MCP | Inspect schema, run queries, manage branches |
| Postgres self-hosted | `postgres` MCP | Generic Postgres queries + inspection |
| Supabase | `supabase` MCP | DB + auth + storage |
| Any project with library docs needs | `context7` MCP | Up-to-date docs for any library |
| Project with web-tech UI (1.1 = Web, OR Mobile/Desktop stack contains Tauri/Electron/Neutralino/Wails) AND Round 4 ≠ empty | `playwright` MCP | Drive browser, screenshots, E2E |
| User mentions Figma | Figma MCP | Pull design files, Code Connect |
| Vercel deployments | `vercel` MCP | Deploys, logs, env vars |
| Stripe billing | `stripe` MCP | Subscriptions, test webhooks |

Limit to 2-3 most relevant MCPs. Don't dump a 10-item list — that's noise.

### Ask the user which to recommend — do NOT show install commands

Structured-question prompt: which of the suggested MCPs do you want to recommend? Multi-select with an "all of them" default.

Frame the choice this way (paraphrase as needed):

> "I'll record the ones you pick in `docs/context/project-overview.md` with install commands. **You'll run the installs at the very end of this flow, after we've filled all the docs** — that way an agent restart for MCP loading doesn't wipe this conversation. Until then, we keep moving."

Capture the chosen MCP list (with names + install commands per agent) — it's needed in Stage 7 (template fill) and Stage 9 (hand-off). Do NOT run `claude mcp add`, do NOT tell the user to restart, do NOT promise "I'll record them later" in a way that requires future agent action.

### Install command reference (write into project-overview.md at Stage 7)

For each chosen MCP, the install command the user will run at the end of Stage 9:

```bash
# Claude Code
claude mcp add <name> --scope user -- npx -y <package or remote URL>

# Codex / Gemini / other agents — use their respective install commands
# Agent picks the right form based on which tool the user is running
```

Common Claude Code commands:

```bash
claude mcp add context7   --scope user -- npx -y @upstash/context7-mcp
claude mcp add playwright --scope user -- npx -y @playwright/mcp@latest
claude mcp add neon       --scope user -- npx -y mcp-remote@latest https://mcp.neon.tech/sse
claude mcp add postgres   --scope user -- npx -y @modelcontextprotocol/server-postgres <DB_URL>
claude mcp add supabase   --scope user -- npx -y @supabase/mcp-server-supabase
claude mcp add vercel     --scope user -- npx -y mcp-remote@latest https://mcp.vercel.com/sse
claude mcp add stripe     --scope user -- npx -y @stripe/mcp
```

(If an exact package name has shifted, the agent should look it up rather than guess — `context7` MCP itself can help here once installed.)

## Stage 6 — Roadmap proposal

> **Skip this stage if "Use existing project" was picked in Stage 1.2** (Web flow) OR if the project type from Stage 1.1 is Backend / Mobile / Desktop / Other and the parent directory already contains a codebase. For existing projects, the agent doesn't know what's already built — proposing a roadmap that says "Build app shell" when one exists is wrong. Instead, briefly inspect the codebase and either skip the roadmap or propose a roadmap that picks up from current state.

For new projects, generate a roadmap proposal based on:
- Product description (Round 1)
- Stack picks (Round 2)
- Strategy answers (Round 3)
- v1 surfaces (Round 4)
- Senior-engineering ordering principles (below)

### Senior-engineering ordering principles to apply

| Idiom | What it means |
|---|---|
| **Irreversible decisions before reversible ones** | Schema, RLS, auth model, tenant boundary first. Visual polish last. |
| **Shell + types + data layer are parallel tracks in "Now"** | They have no dependencies on each other. Build the type contract first (Item, etc.), then shell and data layer can proceed in parallel. |
| **Read before write** | Viewing surfaces before mutation surfaces. Mutations add audit, invalidation, error paths — defer until reads are nailed. |
| **One vertical end-to-end before horizontal scaling** | First surface should be complete (UI + data + behavior) before starting a second. Proves the pattern. |
| **Internal/manual before automated/public** | Seeded data before live webhooks. Internal demo before public launch. |
| **Hardcoded before parameterized** | "Three before abstraction" — easier to extract pattern after seeing it 3x. |
| **Critical path first** | What's the smallest thing that proves the bet? Ship that. |

### Propose the roadmap as a DRAFT

Critical framing — the agent must present the roadmap as a draft that the user reviews and edits, NOT a verdict:

> "Here's my **proposed** roadmap — let's adjust before saving. What feels wrong or out of order?"

Then iterate. Don't write `roadmap.md` until the user explicitly approves. Accept edits like:
- "Swap milestones 2 and 3"
- "Drop the auth phase, I'll do that later"
- "Add a 'mobile-responsive' phase before launch"

When the user says "looks good" or equivalent, save to `docs/context/roadmap.md` using the template structure (see template file for the shape).

### Proposed roadmap template the agent fills in

```markdown
# Roadmap

What's coming, in roughly what order. Living document — items move through phases as they ship.

## Reasoning
2-3 sentences explaining the chosen sequence and why this order makes sense for THIS project.
The agent fills this in based on which idioms applied.

## Now (parallel tracks — start in any order)
- **Types + sample data** — define the core types (Item, etc.) and a small mock dataset conforming to them. The contract every other layer depends on.
- **App shell** — layout, theme, nav, mock surfaces rendering from sample data.
- **Data layer foundation** — schema designed to produce the contract types. [Skip if Database = None]
- **Agent capabilities (MCPs)** — install MCPs that match your stack. [Skip if simple project]
- **Delivery foundation** — configure CI, pull requests, and branch protection. [Include only when Stage 5 recorded this as planned rather than configured]

## Next (1-2 milestones away)
- **<First surface> (live data)** — swap mock import for live query.
- **<Second surface>** — extending the pattern.

## Later (3+ milestones away)
- **Mutations bundle** — turn read-only into write-capable: add/edit/delete/etc.
- **<Other surfaces>**
- **Auth & authorization** — Better Auth setup, sessions, login flow. [If Auth ≠ None]
- **Production polish** — SEO, OG images, analytics, error monitoring, accessibility audit.

## Shipped
(none yet — pre-launch)

## Recurring cadence
- Every 2-3 milestones, spawn the bundled `code-scanner` agent (`.claude/agents/code-scanner.md`) on the changed areas — security + quality + dead-code pass in parallel.
- Every 2-3 milestones, do a manual UI audit pass: walk the user-facing flows, check accessibility (keyboard nav + screen reader + contrast), check responsive breakpoints. Use harness-built-in slash commands if your agent has them (`/audit`, `/critique`, `/polish` in Claude Code).
- Bugfixes go on `fix/<slug>` branches, NOT in this roadmap.
```

## Stage 7 — Fill the templates

Now edit the freshly-installed files with the user's answers. **Edit in place — don't ask permission for each edit.** The user opted into this by running the skill.

Files to update, in priority order:

### `CLAUDE.md`
- Replace `{{Project Name}}` with the real name (multiple occurrences).
- Replace the one-line description with the user's tight version.
- Keep it thin: root import contract and pointers only.
- Do not add project commands, project layout, workflow rules, or coding rules here. Those belong in `docs/context/coding-standards.md` and `docs/context/ai-interaction.md`.

### `docs/context/thesis.md`
- Replace `{{Project Name}}`, `{{Your Name}}`, `{{role}}`, `{{org}}` (ask if not obvious from context).
- Section 01 — fill thesis with user's "why" + "bet" answer.
- Section 04 — fill Laboratory with unfair-advantage answer.
- Section 05 — fill First Useful Product with v1-shippable answer.
- Section 12 — fill "This week's only job" from the first feature recommendation (Stage 8).

### `docs/context/project-overview.md`
- Top — product description, "Built for", v1 scope from user's answers.
- Tech stack table — update Framework, Database, ORM, Auth from Round 2.
- If the user picked the AI Elements scaffold, record it under **Tech stack** or **Interface principles**:
  ```markdown
  ### AI interface stack

  This project was scaffolded with Vercel AI Elements via `npx ai-elements@latest`.
  AI Elements is a shadcn/ui-based component registry for AI-native interfaces. AI UI
  primitives live under `components/ai-elements/` or `src/components/ai-elements/`
  depending on the generated project structure, alongside normal shadcn primitives.

  Component library: **Radix** unless changed during the CLI prompt.
  Preset/theme: **{chosen AI Elements preset, e.g. Mira}**.
  ```
  Keep this factual from the actual CLI choices. Do not claim an AI Gateway key or provider integration exists unless the user set it up.
- If the user picked Next.js + shadcn + starter UI from `arhamkhnz/next-shadcn-admin-dashboard`, add or update an architecture note under **Tech stack** or **Interface principles**:
  ```markdown
  ### Starter architecture

  This project started from [`arhamkhnz/next-shadcn-admin-dashboard`](https://github.com/arhamkhnz/next-shadcn-admin-dashboard).
  Its folder structure follows the colocation-first pattern documented in
  [`arhamkhnz/next-colocation-template`](https://github.com/arhamkhnz/next-colocation-template):
  route-specific pages, layouts, components, and supporting logic live together under
  `src/app/...`, usually in route-local `_components/` folders. Shared primitives and reusable
  infrastructure live at the top level in `src/components`, `src/config`, `src/hooks`, `src/lib`,
  `src/navigation`, and `src/stores`.

  Starter UI mode: **{Minimal | Regular starter}**.
  ```
  For **Minimal**, add that demo dashboard routes were pruned and the retained shell is the dashboard layout/sidebar foundation. For **Regular starter**, add that the full template dashboard/auth/theme/layout surfaces were retained.
- Add or update a **Repository and deployment** section from Stage 5.0:
  ```markdown
  ## 🚀 Repository and deployment

  | Area | Status |
  |---|---|
  | GitHub | {not connected | planned | connected: owner/repo} |
  | GitHub Project | {linked: URL | planned | skipped} |
  | Visibility | {private | public | n/a} |
  | Hosting | {Vercel | Cloudflare | Netlify | Other | None} |
  | Deployment status | {skipped | planned | connected} |
  | CI | {configured | planned | skipped} |
  | Branch protection | {configured | pending first successful Quality run | planned | skipped} |

  {If planned only: include exact next commands.}
  {If connected: include project URL/dashboard URL if known.}
  ```
  Keep this factual. Do not claim a repo/deployment exists unless Stage 5.0 actually created or linked it.
- Add `docs/context/delivery-workflow.md` to the documentation map and point to it for exact commands and gates.
- **§ Agent capabilities** — handle in three cases:
  - **Stage 5 ran and user chose MCPs** → rewrite the section's table with the actual chosen MCPs + their install commands. **MCPs are NOT yet installed** — the user runs the commands at the end of Stage 9. Status header: "Recommended — install at end of `/workflow-init`":
    ```markdown
    ## 🤖 Agent capabilities

    MCPs recommended for this stack. Install commands run at the end of `/workflow-init`
    (Stage 9 hand-off) — keeping installs out of the discovery flow means an agent
    restart never wipes the interview context.

    | MCP | Purpose | Install command (Claude Code) |
    |---|---|---|
    | `context7` | Up-to-date library docs | `claude mcp add context7 --scope user -- npx -y @upstash/context7-mcp` |
    | `playwright` | Browser-driven testing | `claude mcp add playwright --scope user -- npx -y @playwright/mcp@latest` |
    | `neon` | DB introspection + queries | `claude mcp add neon --scope user -- npx -y mcp-remote@latest https://mcp.neon.tech/sse` |

    After install: restart your agent. Verify with `claude mcp list`.
    ```
    Use the actual MCP set captured in Stage 5. If running on Codex/Gemini, swap the install command syntax to that agent's equivalent.
  - **Stage 5 ran but user chose no MCPs** → replace the template's placeholder content with a one-line note: `_No MCPs recommended for this project — agent works fine without external integrations._`
  - **Stage 5 was skipped entirely (simple project)** → DELETE the entire `## 🤖 Agent capabilities` section. Leave no placeholder behind. A simple project's overview shouldn't carry a TBD that'll never resolve.
- "What we're building → v1 surfaces" — populate from Round 4.
- "Definition of done for v1" — derive 3-5 concrete behaviors.

### `docs/context/delivery-workflow.md`

- Replace every command placeholder with a command verified from the actual repository, or the explicit text `Not configured` / `Not applicable`.
- Record which checks run locally and in the stable `Quality` CI job.
- Record the GitHub Project, branch-protection status, preview provider, production URL, smoke workflow, and rollback path truthfully.
- If setup is planned, include exact next commands or provider steps and name the missing prerequisite.
- Do not claim branch protection is configured until `Quality` has reported successfully and the repository settings have been verified.
- Do not claim production smoke is configured unless it verifies the exact deployed commit before checking behavior.
- Remove all remaining `{{...}}` placeholders before finishing Stage 7.

### `README.md` *(if present)*
- Update the project name and one-line purpose.
- Add a short setup section using the actual package manager/scripts in `package.json`.
- Add a **Repository and deployment** section using Stage 5.0 decisions:
  ```markdown
  ## Repository and deployment

  - GitHub: {not connected | planned | owner/repo}
  - Visibility: {private | public | n/a}
  - Hosting: {Vercel | Cloudflare | Netlify | Other | None}
  - Deployment: {skipped | planned | connected}
  - CI: {configured | planned | skipped}
  - Protected default branch: {configured | pending | planned | skipped}
  - Delivery guide: `docs/context/delivery-workflow.md`
  ```
- If provider setup was only planned, include next commands but mark them as pending.
- If using the admin dashboard starter, mention the starter source and colocation reference in one sentence, then point detailed architecture notes to `docs/context/project-overview.md`.

### `docs/context/roadmap.md`
- The roadmap drafted and approved in Stage 6 — write that content here. Don't re-edit; the user already approved it.

### `docs/context/coding-standards.md`
- If user picked defaults the file documents (Next.js + TS + Tailwind v4 + Drizzle), leave untouched.
- If "I'll add it later" for any of Database / ORM / Auth — strip specifics, replace with TBD note: "Database: TBD — pick when ready, then update this section."
- If specific different choice, replace relevant sections (Drizzle → Prisma section, etc.).
- Update opening starter-note to reflect actual chosen stack.
- Put project commands and project layout here, not in `CLAUDE.md`, `AGENTS.md`, or `GEMINI.md`.

### `docs/specs/project-spec.md`
- Replace `{{Project Name}}` references.
- Section 2 (Data layer) — note the database choice but leave schema decisions as TODO.
- Section 3 (Auth) — note the provider, leave specifics TODO.

### `docs/context/current-feature.md`
- Leave Status/Goals/Notes empty (placeholder comments stay).
- Append a **History** entry: "**[today's date] — Project bootstrap.** Initialized via `/workflow-init`. Stack: {framework} + {database} + {orm} + {auth}. v1 surfaces: {list}. First feature target: {feature name} (see Stage 8). Repository/delivery: {GitHub status}, {CI status}, {branch-protection status}, {hosting status}. MCPs recommended (install pending — see `project-overview.md` § Agent capabilities): {list}."

### `AGENTS.md` and `GEMINI.md`
- Replace `{{Project Name}}` with the real name.
- Replace the one-line description.
- Preserve the required `@docs/context/...` context import block. Do not downgrade it to plain Markdown links only.
- Everything else stays.

## Stage 8 — Recommend a first feature

Pick the smallest thing that proves the product's core promise from the roadmap's "Now" milestones. Typically the first feature for "Types + sample data" if the project needs data, or the first content page for a static site.

For the proposed first feature:
- Pitch in 2-3 sentences. Say *why* it's the right first slice (proves which assumption, defers which complexity).
- Invoke the elaboration loop — user might counter-propose, ask for alternatives, or reject the framing.
- When settled, paraphrase: "So feature #1 is: <X>. The bet it tests: <Y>. What you're punting: <Z>."

Then ask:

> "Want me to `/feature spec` this now, or hold off?" (In Codex, use `$feature spec`.)

If yes — including natural approvals like "go ahead", "do it", "sounds good", "yeah", or "yep" — invoke `/feature spec` in Claude Code or `$feature spec` in Codex. The user does not need to retype the command. If no, leave the recommendation as part of the history entry in `current-feature.md` and stop.

## Stage 9 — Hand off

Three parts: repository/delivery status, MCP install commands (if any were chosen in Stage 5), then the standard next steps.

### Part A — Repository and delivery status

Summarize Stage 5.0 truthfully:

```text
Repository/deployment:
  GitHub: <not connected | planned | owner/repo>
  GitHub Project: <linked URL | planned | skipped>
  Visibility: <private | public | n/a>
  Hosting: <Vercel | Cloudflare | Netlify | Other | None>
  Deployment: <skipped | planned | connected>
  CI: <configured | planned | skipped>
  Browser/executable smoke: <configured | planned | not applicable>
  Branch protection: <configured | pending first successful Quality run | planned | skipped>
  Production smoke: <configured | planned | not applicable>
```

If setup was planned but not connected, surface the exact commands recorded in README/project-overview. If connected, include dashboard/project URLs when known.

When the user chose **Configure now**, finish the setup rather than claiming it is ready early:

1. Run every configured command locally.
2. For an existing GitHub repository, put the delivery baseline on a chore branch and open a pull request.
3. For a brand-new repository with no default branch, explain that one user-approved bootstrap commit and push is needed to establish `main`; all later work goes through pull requests.
4. Wait for the first `Quality` run to succeed.
5. Enable and verify the recorded branch-protection policy when authorized and supported by the connected GitHub account.
6. Report any remaining pending item explicitly.

### Part B — MCP install (if any chosen)

Surface the install commands captured in Stage 5 verbatim, and explain that restarting now is safe because every interview answer is already persisted to disk:

```
Before you start the first feature, install your recommended MCPs:

  <install command 1>
  <install command 2>
  ...

Then restart your agent so they load.

  Safe to restart now — the interview, roadmap, and feature recommendation
  are all written to docs/context/. The next agent session reads them as
  context automatically, so you lose nothing.
```

Skip Part B entirely if Stage 5 was skipped or the user chose no MCPs.

### Part C — Next steps (always)

```
You're set up.

• docs/context/ has the docs filled with your real context. Edit as you learn more.
• docs/context/roadmap.md has the proposed roadmap. Re-order, add, or remove as priorities shift.
• docs/context/delivery-workflow.md explains CI/CD, exact quality commands, branch protection, previews, production smoke, and rollback.
• docs/context/designs/ is empty — drop visual references (screenshots, Figma exports, mockups) for features in subfolders matching the feature slug.
• Run `/feature spec` when you're ready to start the first feature.
• Run `/feature load <slug>` to load a spec.
• Run `/feature start` to cut the branch and start implementing.

Codex uses `$feature spec`, `$feature load <slug>`, and `$feature start` instead of slash commands.

Bug fixes go on `fix/<slug>` branches — NOT in the roadmap, NOT in current-feature.md history.

The full workflow is documented in docs/context/ai-interaction.md.
```

## Conflict handling

If the CLI exits non-zero with a conflict list during Stage 3, do not run the interview — the install didn't happen. Quote the conflict list back to the user and let them decide:
- Remove/rename the conflicting files, then re-run `/workflow-init`
- Or pick a fresh target directory

## If the user just wants the bare install

If the user explicitly says "skip the interview" or "just install the files," run Stage 3 only. Don't pester — they know what they want.

## If `npx` isn't available

Fall back to `npx github:DigitalOutbreak/workflow` (works via the GitHub form even on machines that haven't been logged into npm). If neither npx form works, suggest installing Node.js (https://nodejs.org/).
