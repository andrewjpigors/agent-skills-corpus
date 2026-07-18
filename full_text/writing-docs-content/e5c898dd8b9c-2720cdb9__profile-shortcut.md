---
name: profile-shortcut
description: >-
  Creates shell profile shortcuts that cd into a repo and run a README-derived
  command with forwarded args. Supports a simple one-function shortcut (Mode A)
  or an optional two-level personal CLI — my <group> <command> [args] (Mode B,
  PowerShell). Resolves repo paths from ~/GitHub or common folders, edits the
  user's default shell on Windows (PowerShell), macOS, and Linux (bash, zsh,
  fish). Use for terminal shortcuts, profile aliases, grouped personal commands,
  cross-repo maintenance (git pull / sync / open / status), reload profile, or
  pass args to dotnet/npm/pnpm/cargo/docker.
metadata:
  author: lasaths
  version: "2.1.0"
  license: MIT
---

# Profile Shortcut

## Workflow checklist

```
- [ ] Simple shortcut (Mode A) OR extend `my` dispatcher (Mode B) OR add git commands?
- [ ] Mode A: command name + repo name | Mode B: group name + command name + target | Git: pull/sync/open/status
- [ ] Resolve target path; verify it exists
- [ ] Detect platform and active shell
- [ ] Read target README → pick underlying command (or ask user)
- [ ] Mode A: add/replace flat function | Mode B: extend registry hashtables OR flat switch + help UI | Git: add group + handlers
- [ ] Mode B: detect registry (`$MyCommands`) vs flat switch before editing
- [ ] Reload profile in the same shell
- [ ] Test with a real invocation and flags (not only help / my / my <group>)
- [ ] If wrapping a .ps1 with param(), verify PositionalBinding=$false + ValueFromRemainingArguments
- [ ] Confirm: mode, shell, profile path, README source, usage
```

## Purpose

Help the user create custom shell commands in their **default terminal profile** that jump into a specific repo folder and run a repo-dependent command.

Works on **Windows, macOS, and Linux** using whatever shell the user's terminal session uses (PowerShell, bash, zsh, or fish).

Examples of repo-dependent commands (typically found in README):

```text
dotnet build
npm run build
pnpm dev
python main.py
cargo build
docker compose up
```

## When to use this skill

Use this skill when the user wants to:

* Create a shortcut command in their terminal
* Add a function or alias to their shell profile
* Run a repo-specific command from a specific folder
* Make a command like `bapp`, `build-api`, `run-site`, or another custom name
* Group multiple shortcuts under a personal CLI: `my <group> <command> [args]`
* Run fleet commands across **all** repos (`git pull`, `git sync` pull+push, `git open`, `git status`)
* Reload their shell profile
* Pass extra arguments to the underlying command

## Choose shortcut mode

| Mode | Use when |
|------|----------|
| **A — Simple shortcut** | One repo, one action, rarely grows |
| **B — `my` dispatcher** | Multiple repos/actions; user wants one entry point and grouped help |

**Decision rules:**

1. **Read the profile first** — detect which Mode B shape already exists:
   - `$MyCommands` hashtable → **registry pattern** (extend hashtables; see below)
   - `function my` with `switch` branches → **flat switch pattern** (add help row + switch branch)
   - No `my` → choose skeleton based on expected growth (see Mode B variants)
2. If `function my` already exists → **extend Mode B**; do not add another top-level function for the same intent.
3. User asks for grouped, personal, or namespaced shortcuts → **Mode B**.
4. Single repo, single action, no existing `my` → offer both; default to **Mode A** unless the user prefers grouping.

Mode B is **PowerShell-only** today (colored help + `$args` forwarding). Mode A works on bash, zsh, fish, and PowerShell.

**Mode B variants (PowerShell):**

| Variant | Use when |
|---------|----------|
| **Registry** (recommended) | User already has `$MyCommands`, or expects many groups/commands |
| **Flat switch** | First `my` with only 1–2 commands; minimal boilerplate |

Concept for Mode B:

```text
my <group> <command> [args...]
```

- `my` — generic personal namespace (not user-specific)
- `<group>` — project family or area (e.g. framework, tooling, client work)
- `<command>` — short action (build, dev, migrate, test, …)
- `[args]` — forwarded to the real tool unchanged

User runs `my` alone for full help, `my <group>` for group-scoped help.

## Required first step

Gather fields based on mode. If the user already provided values, do not ask again.

### Mode A — Simple shortcut

1. **Command name** — the shortcut to type (e.g. `build-api`, `dev-site`).
2. **Repo name** — folder name (e.g. `MyApi`, `my-site`), not the full path.

```text
What should the shortcut be called, and which repo is it for?

Example:
Command name: build-api
Repo name: MyApi
```

### Mode B — `my` dispatcher

1. **Group name** — lowercase, short domain label (e.g. `api`, `web`, `tools`).
2. **Command name** — short verb/noun within that group (e.g. `build`, `dev`, `test`).
3. **Target** — repo folder name or full path (resolve like Mode A).

Group by **domain/intent**, not necessarily folder layout — a script inside repo A can live under group B if that matches how the user thinks about it.

If `AskQuestion` is available, use it to gather missing fields in one step (include mode choice when unclear).

## Resolve repo name to path

If the user gives a **full path** instead of a repo name, use it directly.

Otherwise resolve `REPO_NAME` by checking these locations **in order** (first match wins):

| Platform | Search paths |
|----------|--------------|
| Windows | `%USERPROFILE%\GitHub\REPO_NAME`, `%USERPROFILE%\Projects\REPO_NAME`, `%USERPROFILE%\Developer\REPO_NAME`, `%USERPROFILE%\repos\REPO_NAME` |
| macOS / Linux | `~/GitHub/REPO_NAME`, `~/Projects/REPO_NAME`, `~/Developer/REPO_NAME`, `~/repos/REPO_NAME` |

Run a directory check in the shell (e.g. `Test-Path` on Windows, `test -d` on Unix) before proceeding.

If no folder is found, ask the user for the full repo path.

After resolving the path, **verify the folder exists** before reading the README or editing any profile.

**Mode B registry:** add the resolved path to `$MyRepoPaths` under a stable key (usually the folder name). Reference that key from `Entry.Repo` in `$MyCommands`.

## Detect platform and shell

Run detection in the user's shell **before** choosing a profile file or function syntax.

### Windows

If the session is PowerShell (`$PSVersionTable` is set):

- Shell: **PowerShell**
- Profile: run `$PROFILE` to get the path
- Typical path: `~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` (pwsh) or `~\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1` (Windows PowerShell)

If the session is cmd or Git Bash on Windows, detect explicitly:

- **Git Bash / bash**: `~/.bashrc` or `~/.bash_profile`
- **PowerShell** is preferred when available; use bash only if that is the active shell

### macOS and Linux

Detect the **active shell** (not only login shell):

```bash
echo $0
# or
ps -p $$ -o comm=
```

Map to profile file:

| Shell | Profile file (check in order) |
|-------|-------------------------------|
| **zsh** | `~/.zshrc` (macOS default since Catalina) |
| **bash** | `~/.bashrc`; on macOS also check `~/.bash_profile` if `.bashrc` is missing or not sourced |
| **fish** | `~/.config/fish/config.fish` |

If `$SHELL` and the active shell disagree, use the **active shell** — that is what the user is running in their terminal.

Do not assume PowerShell on macOS/Linux unless the active session is PowerShell (`pwsh`).

## Determine the command from the README

After you have the resolved repo path, **read the repo README** to determine what command to run. Do not guess or assume a default like `dotnet build`.

1. Look for a README in the repo root, in this order:
   - `README.md`
   - `README.MD`
   - `readme.md`
   - `README`
   - `README.txt`
2. Read the file with the Read tool. If none exists, ask the user which command to run.
3. Extract candidate commands from common README sections:
   - Getting started / Quick start / Development / Running locally
   - Build / Compile / Test / Deploy
   - Code blocks in shell/bash/zsh/fish/powershell/cmd fences
   - Tables or bullet lists of npm/pnpm/yarn/dotnet/cargo/make/docker commands
4. Prefer commands that match the user's intent (e.g. "dev shortcut" → `pnpm dev`; "build shortcut" → `dotnet build`).
5. If multiple commands fit, pick the best match or ask the user to choose. Show what you found and which command you selected.
6. If the README has no runnable command, ask the user explicitly.

## Edit the profile directly

Do not only show a snippet — **edit the user's shell profile file** for them.

1. **Detect platform and shell** (see above).
2. **Resolve the profile path** for that shell.
3. **Create the profile if missing**:
   - PowerShell: `New-Item -ItemType File -Path $PROFILE -Force`
   - bash/zsh/fish: `mkdir -p "$(dirname PROFILE_PATH)"` then `touch PROFILE_PATH` if needed
4. **Read the existing profile** with the Read tool before editing.
5. **Add or update the shortcut**:
   - **Mode A**: If a function/block with the same command name already exists, replace it entirely. Otherwise append at the end, preceded by one blank line if the file is not empty.
   - **Mode B**: If `$MyCommands` exists, extend registry hashtables (+ special handler if needed). If `function my` exists with flat `switch`, extend help + branches. If `my` does not exist, append registry skeleton (preferred for multi-command) or flat switch skeleton (1–2 commands). Do not replace the whole dispatcher unless the user asks to restructure. Precede with one blank line if the file is not empty.
6. **Reload the profile** in the same shell (see Reloading below).
7. **Test the shortcut** by running a **real invocation with flags** in the shell (or explain if the agent's session cannot run it):
   - Mode A: e.g. `COMMAND_NAME -c Release`, not only bare `COMMAND_NAME` or `-?`
   - Mode B: e.g. `my GROUP COMMAND -flag value`, not only `my` or `my GROUP`
   - If the target is a `.ps1` with `param()` and subcommands, test a real subcommand — help can succeed while forwarding is broken.
8. **Confirm** what was added, which README snippet you used, profile path, shell, and mode used.

If profile editing fails (permissions, path not writable), show the snippet and manual steps as fallback.

## Preferred patterns by shell

Use the detected shell. Replace `COMMAND_NAME`, `REPO_PATH`, and `REPO_COMMAND`.

### PowerShell (Windows, or pwsh on macOS/Linux) — Mode A

```powershell
function COMMAND_NAME {
    Push-Location "REPO_PATH"
    REPO_COMMAND @args
    Pop-Location
}
```

For npm scripts: `npm run build -- @args`

**Hyphenated names** (e.g. `build-api`): valid in PowerShell as-is.

**`.ps1` scripts with `param()`** (especially subcommand CLIs): use the call operator and explicit arg forwarding. A parameterless function with bare `@args` often passes `-?` / `help` but drops or mis-binds subcommand tokens.

```powershell
function COMMAND_NAME {
    [CmdletBinding(PositionalBinding = $false)]
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]] $RemainingArgs
    )
    Push-Location "REPO_PATH"
    & "REPO_PATH\path\to\script.ps1" @RemainingArgs
    Pop-Location
}
```

Read the script's `param()` block before choosing the wrapper. `PositionalBinding = $false` stops the function from consuming positional tokens; `ValueFromRemainingArguments` collects everything for `@RemainingArgs` splatting into the script.

### bash / zsh (macOS, Linux, Git Bash)

If `COMMAND_NAME` contains `-`, bash cannot define `build-api()` directly. Use a helper + alias:

```bash
__build_api() {
    ( cd "REPO_PATH" && REPO_COMMAND "$@" )
}
alias build-api='__build_api'
```

Replace `build-api` / `__build_api` with the user's command name and a valid helper name (hyphens → underscores in the helper).

If `COMMAND_NAME` has no hyphens:

```bash
COMMAND_NAME() {
    ( cd "REPO_PATH" && REPO_COMMAND "$@" )
}
```

For npm scripts: `npm run build -- "$@"`

Use absolute paths or `$HOME`-based paths. Quote paths that contain spaces.

### fish

```fish
function COMMAND_NAME
    cd "REPO_PATH"; and REPO_COMMAND $argv; cd -
end
```

For npm scripts: `npm run build -- $argv`

## Personal subcommand CLI (`my`) — Mode B

PowerShell-only. Placeholders below — never bake real paths or commands into the skill.

### Naming conventions

| Piece | Rule | Examples |
|-------|------|----------|
| Dispatcher | Always `my` | `my` |
| Groups | lowercase, short | `api`, `web`, `tools`, `client` |
| Commands | short verbs/nouns | `build`, `dev`, `test`, `deploy`, `migrate` |

### UI guidelines

- Colored header with **`my`** highlighted (Cyan or Magenta)
- Groups as section labels (Yellow) with optional tagline (DarkGray)
- Rows: gray `my <group>` prefix + **cyan command** + gray description; align columns when possible
- Usage line: `my <group> <command> [args]`
- Partial help: `my <group>` lists only that group's commands
- Unknown group/command: friendly `Write-Host` messages — avoid noisy `Write-Error`
- **Single-action groups** (e.g. `my katha`): omit command column in help; `my <group> [args]` runs `_default`

### Registry pattern (recommended)

Use when the profile already has `$MyCommands`, or the user will accumulate many shortcuts. One place to register repos, groups, and run logic — no growing `switch` trees.

**Read the profile first.** If `$MyCommands` exists, extend these hashtables; do not replace the dispatcher or revert to flat switches.

#### Registry schema

```powershell
$MyGitHub = Join-Path $env:USERPROFILE 'GitHub'   # or user's actual clone root

$MyRepoPaths = @{
    'REPO_KEY' = Join-Path $MyGitHub 'FolderName'
    # one entry per repo; key matches Entry.Repo below
}

$MyGroupOrder = @('GROUP_A', 'GROUP_B')   # help display order

$MyGroupMeta = @{
    GROUP_A = @{ Tagline = 'short label'; SingleAction = $false }
    GROUP_B = @{ Tagline = 'one-shot tool'; SingleAction = $true }
}

$MyCommands = @{
    GROUP_A = @{
        build = @{
            Desc = 'Human description'
            Repo = 'REPO_KEY'                              # key into $MyRepoPaths
            Run  = { param([string[]] $a) dotnet build @a }
        }
    }
    GROUP_B = @{
        _default = @{
            Desc = 'Runs without subcommand'
            Repo = 'REPO_KEY'
            Run  = { param([string[]] $a) uv run tool @a }
        }
    }
}
```

**Entry fields:**

| Field | Required | Purpose |
|-------|----------|---------|
| `Desc` | yes | Help text |
| `Repo` | usually | Key into `$MyRepoPaths`; omitted only for `Special` handlers |
| `Run` | usually | Scriptblock: `param([string[]] $a)` then the repo command; invoked after `Push-Location` |
| `Special` | no | Named handler in `my` for non–cd+run cases (external script, fixed args, multi-step) |

**Smart defaults inside `Run`:** when no args, run a sensible default (e.g. `if ($a.Count -eq 0) { dotnet build -c Release } else { dotnet build @a }`).

**Location stack:** always wrap registry invocations in `Push-Location` / `try` / `finally` / `Pop-Location` so failures still restore cwd.

#### Register a new command (registry)

1. Add repo folder to `$MyRepoPaths` if missing (resolve path like Mode A).
2. Add group to `$MyGroupOrder` and `$MyGroupMeta` if new group.
3. Add command entry under `$MyCommands.<group>` (or `_default` for single-action).
4. Read target README → implement `Run` scriptblock (or `Special` + handler function inside `my`).
5. Reload `. $PROFILE`; test with real flags: `my GROUP COMMAND -c Release`.

#### Special handlers

When README command is not a simple `cd` + tool (wrapper script, baked-in project IDs, output paths):

1. Set `Special = 'handler_name'` on the entry (no `Run` / `Repo` needed if fully custom).
2. Add `function Invoke-MyHandlerName { param([string[]] $CliArgs) ... }` inside `my` (keeps profile namespace clean).
3. Branch in dispatcher: `if ($entry.Special -eq 'handler_name') { Invoke-MyHandlerName $subArgs; return }`.

#### Cross-repo (fleet) commands

Some commands act on **every** repo, not one — e.g. pull all, status all, fetch all. These are `Special` handlers that iterate over multiple directories instead of `cd`-ing into a single `Entry.Repo`.

**Performance Note:** Git fleet commands use **lazy evaluation** to avoid directory scanning during profile load. Directory paths are configured as simple strings, and scanning only occurs when you actually run `my git *` commands.

Register without a `Repo` (the handler owns the looping):

```powershell
git = @{
    pull   = @{ Desc = 'Fast-forward pull every repo (skips on conflict)'; Special = 'pullall' }
    sync   = @{ Desc = 'Pull then push every repo (ff-only; skips on conflict)'; Special = 'gitsync' }
    open   = @{ Desc = 'Show repos with uncommitted changes'; Special = 'gitopen' }
    status = @{ Desc = 'Show git status for all repos'; Special = 'gitstatus' }
}
```

Handlers — key choices below the code:

```powershell
function Invoke-GitPullAll {
    Write-Host 'Pulling all repos...' -ForegroundColor Cyan
    
    $totalRepos = $MyRepoPaths.Count
    $results = @()
    $skipped = @()
    $checkedRepos = 0
    
    foreach ($repo in $MyRepoPaths.GetEnumerator()) {
        $checkedRepos++
        $name = $repo.Key
        $path = $repo.Value
        
        # Show progress
        $progress = [math]::Round(($checkedRepos / $totalRepos) * 100)
        Write-Progress -Activity 'Pulling repositories' -Status "Processing $checkedRepos of $totalRepos" -PercentComplete $progress
        
        if (-not (Test-Path (Join-Path $path '.git'))) { continue }

        $out = git -C $path pull --ff-only 2>&1
        $status = if ($LASTEXITCODE -ne 0) { 'skipped' }
                  elseif ($out -match 'Already up to date') { 'up to date' }
                  else { 'updated' }
        $results += [pscustomobject]@{ Name = $name; Status = $status }
    }
    
    # Complete the progress display
    Write-Progress -Activity 'Pulling repositories' -Completed
    
    Write-Host ''
    foreach ($r in ($results | Sort-Object Name)) {
        Write-Host ("  {0,-36} " -f $r.Name) -NoNewline
        switch ($r.Status) {
            'updated'    { Write-Host 'updated' -ForegroundColor Green }
            'up to date' { Write-Host 'up to date' -ForegroundColor DarkGray }
            'skipped'    { Write-Host 'SKIPPED (not fast-forward)' -ForegroundColor Red; $skipped += $r.Name }
        }
    }
    if ($skipped.Count -gt 0) {
        Write-Host ("  {0} repo(s) need manual attention:" -f $skipped.Count) -ForegroundColor Red
        $skipped | ForEach-Object { Write-Host ("    - {0}" -f $_) -ForegroundColor Yellow }
    }
    Write-Host ''
}

# ponytail: pull then push per repo; rebase/merge when sync alone isn't enough
function Invoke-GitSyncAll {
    Write-Host 'Syncing all repos (pull + push)...' -ForegroundColor Cyan
    $allRepoPaths = @()
    foreach ($root in $MyGitRootRaw) {
        if (Test-Path $root -PathType Container) {
            $allRepoPaths += Get-ChildItem -Path $root -Directory
        }
    }
    $results = @(); $failed = @(); $n = 0
    foreach ($repo in $allRepoPaths) {
        $n++; $name = $repo.Name; $path = $repo.FullName
        if (-not (Test-Path (Join-Path $path '.git'))) { continue }
        Write-Progress -Activity 'Syncing repositories' -Status "$n / $($allRepoPaths.Count)" -PercentComplete ([math]::Round(($n / $allRepoPaths.Count) * 100))
        $pullOut = git -C $path pull --ff-only 2>&1
        if ($LASTEXITCODE -ne 0) { $results += [pscustomobject]@{ Name = $name; Status = 'pull skipped' }; continue }
        $pulled = $pullOut -notmatch 'Already up to date'
        $pushOut = git -C $path push 2>&1
        if ($LASTEXITCODE -ne 0) { $results += [pscustomobject]@{ Name = $name; Status = 'push failed' }; continue }
        $pushed = $pushOut -notmatch 'Everything up-to-date'
        $status = if ($pulled -and $pushed) { 'pulled+pushed' } elseif ($pulled) { 'pulled' } elseif ($pushed) { 'pushed' } else { 'up to date' }
        $results += [pscustomobject]@{ Name = $name; Status = $status }
    }
    Write-Progress -Activity 'Syncing repositories' -Completed
    Write-Host ''
    foreach ($r in ($results | Sort-Object Name)) {
        Write-Host ("  {0,-36} " -f $r.Name) -NoNewline
        switch ($r.Status) {
            'pulled+pushed' { Write-Host 'pulled + pushed' -ForegroundColor Green }
            'pulled'        { Write-Host 'pulled' -ForegroundColor Green }
            'pushed'        { Write-Host 'pushed' -ForegroundColor Green }
            'up to date'    { Write-Host 'up to date' -ForegroundColor DarkGray }
            'pull skipped'  { Write-Host 'SKIPPED (pull not ff)' -ForegroundColor Red; $failed += $r.Name }
            'push failed'   { Write-Host 'PUSH FAILED' -ForegroundColor Red; $failed += $r.Name }
        }
    }
    Write-Host ''
    if ($failed.Count -eq 0) { Write-Host '  All repos synced.' -ForegroundColor Green }
    else {
        Write-Host ("  {0} repo(s) need manual attention:" -f $failed.Count) -ForegroundColor Red
        $failed | ForEach-Object { Write-Host ("    - {0}" -f $_) -ForegroundColor Yellow }
    }
    Write-Host ''
}

function Invoke-GitOpenChanges {
    Write-Host 'Scanning repos for changes...' -ForegroundColor Cyan
    
    $githubPath = $MyGitHub
    $reposWithChanges = @{}
    
    # Fast parallel scan of all repos
    $allRepos = Get-ChildItem -Path $githubPath -Directory | ForEach-Object -Parallel {
        $repoName = $_.Name
        $repoPath = $_.FullName
        $gitDir = Join-Path $repoPath '.git'
        
        if (Test-Path $gitDir) {
            $changes = git -C $repoPath status --porcelain 2>$null
            if ($changes) {
                $changeCount = ($changes -split '\n').Count
                $branch = git -C $repoPath rev-parse --abbrev-ref HEAD 2>$null
                @{
                    Repo = $repoName
                    Changes = $changeCount
                    Branch = $branch
                }
            }
        }
    } | Where-Object { $_ -ne $null }
    
    if ($allRepos.Count -eq 0) {
        Write-Host 'No repos with open changes' -ForegroundColor DarkGray
    } else {
        Write-Host "Found $($allRepos.Count) repos with changes:" -ForegroundColor Cyan
        Write-Host ""
        
        foreach ($repo in ($allRepos | Sort-Object { $_.Repo })) {
            Write-Host ("  {0,-36} " -f $repo.Repo) -NoNewline
            
            if ($repo.Changes -lt 10) {
                Write-Host "$($repo.Changes) file(s)" -ForegroundColor DarkGray
            } else {
                Write-Host "$($repo.Changes) file(s)" -ForegroundColor Red
            }
        }
        
        Write-Host ""
    }
}

function Invoke-GitStatusAll {
    Write-Host 'Getting git status for all repos...' -ForegroundColor Cyan
    
    $githubPath = $MyGitHub
    $allStatus = @()
    
    # Fast parallel scan of all repos
    $allRepos = Get-ChildItem -Path $githubPath -Directory | ForEach-Object -Parallel {
        $repoName = $_.Name
        $repoPath = $_.FullName
        $gitDir = Join-Path $repoPath '.git'
        
        if (Test-Path $gitDir) {
            $status = git -C $repoPath status --porcelain 2>$null
            $branch = git -C $repoPath rev-parse --abbrev-ref HEAD 2>$null
            @{
                Repo = $repoName
                Branch = $branch
                Status = $status
                HasChanges = (-not [string]::IsNullOrWhiteSpace($status))
            }
        }
    } | Where-Object { $_ -ne $null }
    
    $withChanges = $allStatus | Where-Object { $_.HasChanges }
    $noChanges = $allStatus | Where-Object { -not $_.HasChanges }
    
    if ($withChanges.Count -eq 0) {
        Write-Host 'All repos clean' -ForegroundColor Green
    } else {
        Write-Host "Repos with changes ($($withChanges.Count)):" -ForegroundColor Yellow
        foreach ($repo in ($withChanges | Sort-Object { $_.Repo })) {
            Write-Host "  $($repo.Repo) [$($repo.Branch)]" -ForegroundColor Yellow
        }
        Write-Host ""
    }
    
    Write-Host "Clean repos ($($noChanges.Count)):" -ForegroundColor Green
    foreach ($repo in ($noChanges | Sort-Object { $_.Repo })) {
        Write-Host "  $($repo.Repo) [$($repo.Branch)]" -ForegroundColor Gray
    }
    Write-Host ""
}
```

- **Abort-safe by construction:** `git pull --ff-only` refuses to merge when a clean fast-forward isn't possible, so no merge ever starts and there is nothing to `--abort`. Report the refusal; never auto-merge across a fleet.
- **`git -C $path`** instead of `Push-Location` — each parallel runspace stays isolated; no shared cwd to corrupt.
- **`ForEach-Object -Parallel`** (PowerShell 7+) collapses network-bound waits — a 15-repo serial pull (~1 min) drops to seconds. Throttle 8 is a sane default. On Windows PowerShell 5.1, drop `-Parallel` for a plain serial `foreach`.
- **Inside `-Parallel` use only `$_` and locals.** Outer variables need `$using:`; enumerating `$MyRepoPaths` outside the block avoids that.
- Wire it like any special handler: `if ($entry.Special -eq 'pullall') { Invoke-GitPullAll; return }` (same for `gitsync` → `Invoke-GitSyncAll`, etc.).
- **`my git sync`:** after a successful `pull --ff-only`, run `git push`. Report `pulled` / `pushed` / `pulled+pushed` / `up to date`; on pull refusal or push failure list the repo for manual attention. Keep sync serial (push after pull per repo) — do not parallelize pull+push on the same path.

#### Registry dispatcher core

Keep `function my` thin: parse args → lookup `$MyCommands` → `Invoke-MyRegistryCommand` or special handler. Nested helpers (`Show-MyHelp`, `Write-MyCommandRow`, …) may live **inside** `my` to avoid polluting global scope.

```powershell
function Invoke-MyRegistryCommand {
    param([hashtable] $Entry, [string[]] $SubArgs)
    Push-Location $MyRepoPaths[$Entry.Repo]
    try { & $Entry.Run $SubArgs }
    finally { Pop-Location }
}

function my {
    $RemainingArgs = @($args)
    # ... Show-MyHelp, Show-MyGroupHelp (iterate $MyGroupOrder + $MyCommands) ...
    # SingleAction: $subArgs = Skip 1; Invoke-MyRegistryCommand $MyCommands[$group]['_default']
    # Normal: $subArgs = Skip 2; lookup $MyCommands[$group][$command]; Special or Invoke-MyRegistryCommand
}
```

Help is **generated from `$MyCommands`** — do not maintain duplicate `Write-MyCommand` rows per command.

### Flat switch skeleton (minimal)

Use for the first `my` with only 1–2 commands, or when the user explicitly wants no registry. Append or extend in `$PROFILE`. Replace `GROUP_NAME`, `COMMAND_NAME`, `REPO_PATH`, `REPO_COMMAND`, and description strings.

```powershell
function Write-MyCommand {
    param(
        [string] $Prefix,
        [string] $Command,
        [string] $Description
    )
    Write-Host $Prefix -NoNewline -ForegroundColor DarkGray
    Write-Host $Command -NoNewline -ForegroundColor Cyan
    Write-Host " $Description" -ForegroundColor DarkGray
}

function Show-MyGroupHelp {
    param([string] $Group)
    Write-Host ""
    Write-Host "  my " -NoNewline -ForegroundColor DarkGray
    Write-Host $Group -NoNewline -ForegroundColor Yellow
    Write-Host " — commands" -ForegroundColor DarkGray
    Write-Host ""
    switch ($Group) {
        'GROUP_NAME' {
            Write-MyCommand "    my GROUP_NAME " "COMMAND_NAME" "Short description"
            # Add more Write-MyCommand lines per command in this group
        }
    }
    Write-Host ""
    Write-Host "  Usage: my <group> <command> [args]" -ForegroundColor DarkGray
    Write-Host ""
}

function Show-MyHelp {
    Write-Host ""
    Write-Host "  " -NoNewline
    Write-Host "my" -NoNewline -ForegroundColor Cyan
    Write-Host " — personal shortcuts" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  GROUP_NAME" -ForegroundColor Yellow
    Write-MyCommand "    my GROUP_NAME " "COMMAND_NAME" "Short description"
    # Repeat group label + Write-MyCommand rows for each group
    Write-Host ""
    Write-Host "  Usage: my <group> <command> [args]" -ForegroundColor DarkGray
    Write-Host "         my <group>              group help" -ForegroundColor DarkGray
    Write-Host ""
}

function my {
    $RemainingArgs = @($args)

    if ($RemainingArgs.Count -eq 0) {
        Show-MyHelp
        return
    }

    switch ($RemainingArgs[0]) {
        'GROUP_NAME' {
            if ($RemainingArgs.Count -lt 2) {
                Show-MyGroupHelp 'GROUP_NAME'
                return
            }
            switch ($RemainingArgs[1]) {
                'COMMAND_NAME' {
                    $SubArgs = @($RemainingArgs | Select-Object -Skip 2)
                    Push-Location "REPO_PATH"
                    REPO_COMMAND @SubArgs
                    Pop-Location
                }
                default {
                    Write-Host "Unknown command: $($RemainingArgs[1])" -ForegroundColor Yellow
                    Show-MyGroupHelp 'GROUP_NAME'
                }
            }
        }
        default {
            Write-Host "Unknown group: $($RemainingArgs[0])" -ForegroundColor Yellow
            Show-MyHelp
        }
    }
}
```

### Register a new group or command (flat switch only)

Skip if using the **registry pattern** — update hashtables instead.

1. Add a `Write-MyCommand` row in `Show-MyHelp` under the group section label.
2. Add matching rows in `Show-MyGroupHelp` for that group.
3. Add an outer `switch` branch for the group (if new group) or an inner `switch` branch for the command.
4. Read the target README → set `REPO_PATH` and `REPO_COMMAND` in the branch body.

### Forward args to underlying tools

Inside a command branch, after `$SubArgs = @($RemainingArgs | Select-Object -Skip 2)`:

| Target | Pattern |
|--------|---------|
| dotnet / cargo / python | `dotnet build @SubArgs` (etc.) |
| npm / pnpm / yarn script | `npm run build -- @SubArgs` |
| docker | `docker compose up @SubArgs` |
| `.ps1` with `param()` | `& "REPO_PATH\scripts\tool.ps1" @SubArgs` — use `[CmdletBinding(PositionalBinding=$false)]` + `ValueFromRemainingArguments` on a **wrapper function**, not on `my` itself |

Always `Push-Location` / `Pop-Location` around the repo command when the tool expects to run from the repo root.

### PowerShell pitfalls (dispatcher)

These apply to **`my` itself** — different rules than Mode A `.ps1` wrappers:

1. **Use `$args`, not `param(ValueFromRemainingArguments)`** on `my` — otherwise flags like `-v` bind to common parameters instead of forwarding.
2. **No `[CmdletBinding]` on `my`** — same binding issue.
3. **Sub-args via `Select-Object -Skip 2`**, not array slicing like `$RemainingArgs[2..($RemainingArgs.Count - 1)]` — slicing breaks when an arg starts with `-`.
4. **`.ps1` wrappers** (when a branch calls a script directly): keep the existing Mode A pattern — `PositionalBinding = $false` + `ValueFromRemainingArguments` on a dedicated helper or inline before `& script.ps1`.
5. **No blank lines after backticks** in profile continuations — PowerShell line continuation breaks.

### Deprecated pattern

Flat per-repo functions (`build-api`, `dev-site`, …) remain valid for **Mode A** simple cases. If the user already has `my`, register new shortcuts under the dispatcher instead of adding more top-level functions — unless the user explicitly wants a standalone command.

### bash / zsh / fish

Mode B is not defined for Unix shells in this skill. Use Mode A per shell, or ask the user if they want a future `my()` dispatcher for their shell.

## Reloading the profile

After editing, reload in the **same shell type** you edited for. Do not only tell the user — run the reload command.

| Shell | Reload command |
|-------|----------------|
| PowerShell | `. $PROFILE` |
| bash | `source ~/.bashrc` or `source ~/.bash_profile` (whichever you edited) |
| zsh | `source ~/.zshrc` |
| fish | `source ~/.config/fish/config.fish` |

If reload fails, show the error and suggest opening a new terminal tab/window.

## Usage

**Mode A** — show usage with the user's chosen command name:

```text
build-api
build-api -c Release
build-api --watch
```

**Mode B** — show grouped usage:

```text
my
my GROUP_NAME
my GROUP_NAME COMMAND_NAME
my GROUP_NAME COMMAND_NAME -c Release
my GROUP_NAME COMMAND_NAME --watch
```

## Style

Keep the answer practical and copy-paste friendly.

Use short explanations.

Assume the user wants the profile edited and the shortcut working immediately in their default terminal.

Always use the user's mode (A or B), command/group names, repo name, resolved path, README-derived command, detected shell, and profile path in the final summary.

Briefly cite which README section or snippet you used to pick the command.

## Common troubleshooting

**Command not found after edit**

Reload the profile (see table above) or open a new terminal.

**PowerShell — script execution blocked (Windows only)**

```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Do not recommend system-wide policy changes unless the user explicitly asks.

**macOS — `.bashrc` not loaded**

macOS Terminal often sources `~/.bash_profile` instead. Edit whichever file is actually sourced, or add to `~/.bash_profile`:

```bash
[ -f ~/.bashrc ] && source ~/.bashrc
```

**Wrong shell detected**

Ask which terminal app and shell they use (Terminal.app/zsh, iTerm/zsh, Ubuntu/bash, Windows Terminal/PowerShell, etc.) and edit the matching profile.

**PowerShell — shortcut help works but subcommands fail**

The profile function likely uses bare `@args` without `PositionalBinding = $false` and `ValueFromRemainingArguments`. Replace with the `.ps1` wrapper pattern above, reload `$PROFILE`, then retest with a real subcommand — not only `-?` or `help`.

**PowerShell — `my` drops flags or binds them incorrectly**

The dispatcher likely uses `param()` or `[CmdletBinding]` on `function my`. Remove both; use bare `$args` and `@($RemainingArgs | Select-Object -Skip 2)` for sub-args. Retest with `my GROUP COMMAND -flag value`.

**PowerShell — `my` fails when an forwarded arg starts with `-`**

Sub-args were probably collected with array slicing (`[2..$n]`). Switch to `@($RemainingArgs | Select-Object -Skip 2)`.

## Built-in Git Commands

The profile-shortcut skill includes built-in git commands for managing repos across your fleet with **minimal profile load impact**.

### `my git pull` — Parallel fast-forward pull across all accounts
Fast-forward pull every repo across all your git directories, skipping any that can't be cleanly merged (no auto-merge conflicts).

```powershell
my git pull
```

**Features:**
- **Multi-account support**: Scans all git directories (GitHub, Projects, Developer, repos)
- **Parallel execution**: Pulls all repos simultaneously (PowerShell 7+)
- **Abort-safe**: Uses `git pull --ff-only`, never starts a merge you need to abort
- **Conflict reporting**: Lists repos that need manual attention
- **Progress feedback**: Shows progress during operation

**Example output:**
```
Pulling all repos...

  ABxM.Core                            up to date
  cassis                               up to date
  FabFramework.LCRL.Roof               updated
  VizorGH                              SKIPPED (not fast-forward)

  1 repo(s) need manual attention:
    - VizorGH
```

### `my git sync` — Pull then push every repo
Fast-forward pull, then push, for every repo across your git directories. Skips repos that cannot pull cleanly; reports push failures separately.

```powershell
my git sync
```

**Features:**
- **Pull + push**: `git pull --ff-only` then `git push` per repo
- **Abort-safe pull**: same `--ff-only` rules as `my git pull`
- **Status labels**: `pulled`, `pushed`, `pulled + pushed`, `up to date`, or failure
- **Serial per repo**: push waits for that repo's pull (safe; not fleet-parallel)

**Example output:**
```
Syncing all repos (pull + push)...

  ABxM.Core                            up to date
  cassis                               pulled
  FabFramework                         pushed
  VizorGH                              SKIPPED (pull not ff)

  1 repo(s) need manual attention:
    - VizorGH
```

### `my git open` — Show repos with uncommitted changes across all accounts
Quick scan to see which repos have work in progress across all your git directories.

```powershell
my git open
```

**Features:**
- **Parallel scanning**: Checks all repos simultaneously using `ForEach-Object -Parallel`
- **Minimal output**: Just repo names and file counts
- **Color coding**: DarkGray for 1-9 files, Red for 10+ files
- **Fast execution**: Uses `git -C` commands, no directory changes

**Example output:**
```
Scanning repos for changes...
Found 3 repos with changes:

  ABxM.Agentic                         6 file(s)
  FabFramework.LCRL.Roof               82 file(s)
  cassis                               2 file(s)
```

### `my git status` — Full git status for all repos across all accounts
Get a comprehensive status overview of all repositories across all your git directories.

```powershell
my git status
```

**Features:**
- **Comprehensive**: Shows repos with and without changes
- **Branch info**: Displays current branch for each repo
- **Organized output**: Separate sections for repos with changes vs clean repos
- **Parallel scanning**: Fast execution across all repos

**Example output:**
```
Getting git status for all repos...
Repos with changes (2):
  ABxM.Core [develop]
  cassis [fix/mcp-hang-hardening]

Clean repos (13):
  ABxM.PlateStructures [master]
  FabFramework [develop]
  ...
```

### Setting up Git Commands

Add the git group to your profile configuration:

```powershell
# In $MyGroupOrder
$MyGroupOrder = @('your-existing-groups', 'git')

# In $MyGroupMeta  
$MyGroupMeta = @{
    # your existing groups...
    git = @{ Tagline = 'repo maintenance'; SingleAction = $false }
}

# In $MyCommands
git = @{
    pull   = @{ Desc = 'Fast-forward pull every repo'; Special = 'pullall' }
    sync   = @{ Desc = 'Pull then push every repo (ff-only)'; Special = 'gitsync' }
    open   = @{ Desc = 'Show repos with uncommitted changes'; Special = 'gitopen' }
    status = @{ Desc = 'Show git status for all repos'; Special = 'gitstatus' }
}
```

Then wire the special handlers in your `my` dispatcher:

```powershell
if ($entry.Special -eq 'pullall') { Invoke-GitPullAll; return }
if ($entry.Special -eq 'gitsync') { Invoke-GitSyncAll; return }
if ($entry.Special -eq 'gitopen') { Invoke-GitOpenChanges; return }
if ($entry.Special -eq 'gitstatus') { Invoke-GitStatusAll; return }
```

**Placement:** Add the handler functions (`Invoke-GitPullAll`, `Invoke-GitSyncAll`, `Invoke-GitOpenChanges`, `Invoke-GitStatusAll`) inside `function my` (nested, keeps global scope clean) or at the same level as `my`. Nesting is fine — wire the `Special` branches in the same dispatcher.

### Customizing Git Commands

**Change GitHub paths:** The git functions scan multiple directories by default. Customize `$MyGitRoots` to add or remove directories:

```powershell
$MyGitRoots = @(
    Join-Path $env:USERPROFILE 'GitHub',      # Primary GitHub account
    'C:\custom\git\path',                 # Custom git directory  
    'D:\work\repos'                         # Work repositories
) | Where-Object { Test-Path $_ -PathType Container }
```

**Adjust parallelism:** Change `-ThrottleLimit` for performance tuning:

```powershell
ForEach-Object -ThrottleLimit 4 -Parallel { ... }  # Limit to 4 simultaneous pulls
```

**Add more git commands:** Follow the same pattern for other fleet operations like `my git fetch`, `my git stash-clear`, etc.

### Requirements

- **PowerShell 7+** for parallel operations (`ForEach-Object -Parallel`)
- **Git** installed and available in PATH
- **Fast internet** for parallel pulls to be noticeably faster

For Windows PowerShell 5.1, the commands still work but run sequentially instead of in parallel.

### Performance

- **Fast profile load:** Git configuration uses lazy evaluation - no directory scanning during profile load (~50-100ms savings)
- **Parallel execution:** Git commands run in parallel (PowerShell 7+) when you call them
- **Multi-account support:** Scans all configured git directories when git commands are invoked
- **One-time scanning:** Each git command scans directories once per invocation, not during profile load

## Examples

**Windows (PowerShell) — Mode A**

User: Add shortcut `build-api` for repo `MyApi`.

1. Resolve `MyApi` → repo path under `GitHub\MyApi`
2. Read README → `dotnet build`
3. Edit `$PROFILE`, append function, run `. $PROFILE`
4. Test: `build-api -c Release`

**Windows (PowerShell) — Mode B**

User: Add `my api build` for repo `MyApi`.

1. Read `$PROFILE` — no existing `my`; use full skeleton
2. Group `api`, command `build`, resolve repo path
3. Read README → `dotnet build`
4. Add help rows + switch branches, reload `. $PROFILE`
5. Test: `my api build -c Release` (not only `my` or `my api`)

**Windows (PowerShell) — extend existing `my` (registry)**

User: Add `my web dev` for repo `my-site`.

1. Read `$PROFILE` — `$MyCommands` exists; extend hashtables only
2. Add `my-site` to `$MyRepoPaths`; add `web` to `$MyGroupOrder` / `$MyGroupMeta` if new
3. Add `dev` entry with `Run = { param([string[]] $a) pnpm dev @a }`
4. Read README → confirm `pnpm dev`
5. Test: `my web dev --host`

**Windows (PowerShell) — extend existing `my` (flat switch)**

User: Add `my web dev` for repo `my-site`.

1. Read `$PROFILE` — `function my` exists with `switch`; extend, do not replace
2. Add `web` group (or new command under existing group) in help + switches
3. Read README → `pnpm dev`
4. Test: `my web dev --host`

**macOS (zsh) — Mode A**

User: Add shortcut `dev-site` for repo `my-site`.

1. Resolve `my-site` → `~/GitHub/my-site`
2. Read README → `pnpm dev`
3. Edit `~/.zshrc`, append function (helper + alias if name has hyphens), run `source ~/.zshrc`
4. Test: `dev-site`

**No README**

Ask the user which command to run, then proceed with profile edit.
