---
name: package-cooldown
description: >
  Protect any Python or Node.js project from supply-chain attacks by enforcing
  a package publication cooldown on every major package manager (npm, bun, pnpm,
  yarn, uv, pip) and mise runtime manager. Use when the user asks to: "secure
  packages", "add supply-chain protection", "protect from npm attacks", "pin
  dependencies", "set up package cooldown", or mentions incidents like tj-actions,
  polyfill.io, or tanstack. Starts with a pinning diagnosis and Renovate/Dependabot
  audit before making any changes. Applies machine-level guards (~/.npmrc,
  ~/.bunfig.toml, ~/.config/pip/pip.conf, mise settings) AND project-level guards
  (pinned exact versions, fresh lockfiles committed to git). Always deletes
  node_modules + lockfile and reinstalls so the committed lockfile actually reflects
  pinned versions. Configures Renovate `minimumReleaseAge` or Dependabot
  `cooldown.default-days` (GA July 2025) so future automated PRs respect the same
  cooldown. On GitHub-hosted repos, also proposes a Socket Basics PR-scan workflow
  as the second layer of defense (SAST + secret + reachability scanning on every
  dependency-touching PR), and for bun projects wires up Bun's native install-time
  Security Scanner API with @socketsecurity/bun-security-scanner.
---

# Package Cooldown — Supply-Chain Protection

## Scripts

This skill ships three executable files in `scripts/`. Use them instead of writing
config files by hand — they handle edge cases, preserve existing content, and write
atomically so a crash never leaves a half-written file.

```
scripts/
  cooldown.sh        # Main entry point — run this
  lib.sh             # Sourced by cooldown.sh; do not run directly
  merge_config.py    # Python config-merge backend; called by cooldown.sh
```

### cooldown.sh — machine-wide package-manager configuration

```bash
# Apply 7-day cooldown to every detected package manager (non-interactive)
bash scripts/cooldown.sh --days 7 --non-interactive

# Apply to specific managers only
bash scripts/cooldown.sh --days 7 --manager bun,uv,pnpm

# Preview changes without writing anything
bash scripts/cooldown.sh --days 7 --dry-run

# Quiet mode for CI (only ok/warn/err lines)
bash scripts/cooldown.sh --days 7 --quiet --non-interactive
```

Supported managers: `npm pnpm yarn pip uv bun deno cargo go conda`  
Managers not on PATH are skipped with a warning (never a hard error).  
When stdin is not a TTY (CI, agents, pipes), `--non-interactive` is applied automatically.

### merge_config.py — low-level config merger (call directly for one-off edits)

```bash
MERGE="scripts/merge_config.py"

# .npmrc — upsert key=value (handles commented-out lines)
python3 "${MERGE}" npmrc ~/.npmrc save-exact true

# pnpm global rc — flat key=value
python3 "${MERGE}" flat_kv ~/.config/pnpm/rc minimumReleaseAge 10080

# INI file — upsert key under [section]
python3 "${MERGE}" ini ~/.config/pip/pip.conf install uploaded-prior-to 2026-01-01T00:00:00Z

# Yarn Berry .yarnrc.yml
python3 "${MERGE}" yarnrc ~/.yarnrc.yml 7d

# bunfig.toml — [install] minimumReleaseAge (seconds)
python3 "${MERGE}" bunfig ~/.bunfig.toml 604800

# uv.toml — root-level exclude-newer (relative or ISO-8601 timestamp)
python3 "${MERGE}" uv_toml ~/.config/uv/uv.toml "7 days"

# deno.json — minimumDependencyAge ISO-8601 duration
python3 "${MERGE}" deno ~/.config/deno/deno.json 7

# .condarc — informational comment block
python3 "${MERGE}" condarc ~/.condarc 7

# Print UTC timestamp N days ago (for pip's uploaded-prior-to)
python3 "${MERGE}" utc_ago 7
```

All merge_config.py operations are:
- **Atomic** — writes to a temp file in the same directory, then `os.replace()` so
  a crash never leaves a corrupt config
- **Idempotent** — running twice produces the same file
- **Preserving** — all existing lines and comments are kept; only the target key changes

### Shell compatibility

| Shell | Works? | Notes |
|-------|--------|-------|
| bash  | yes    | native; requires 3.2+ (macOS default) |
| zsh   | yes    | invokes via `#!/usr/bin/env bash` shebang |
| fish  | yes    | invokes as a subprocess; shebang handles it |
| CI (sh)| yes  | stdin not a TTY → auto non-interactive |
| Agents | yes  | same as CI; pipe or call with `--non-interactive` |

---

## Why this matters

Most malicious package versions are live for only a few hours before detection.
Refusing to install any package published within the last N days eliminates the
attack window entirely — for current and future incidents.

Default cooldown: **7 days** (604 800 seconds).
Minimum accepted: **3 days** — anything shorter is ineffective.

## Defense-in-depth stack (what this skill builds)

Five layers, each cheap to add, each closing a different attack window:

| Layer | Where it lives                                            | What it blocks                                                  |
|-------|-----------------------------------------------------------|-----------------------------------------------------------------|
| 1     | **Manifest pins** — `package.json`, `pyproject.toml`, `mise.toml` | `^`/`~`/`latest`/`>=` from silently resolving to a fresh bad version |
| 2     | **Manager cooldown** — `bunfig.toml`, `pnpm-workspace.yaml`, `~/.npmrc` (via socket) | Installing any version younger than N days, on every dev's machine |
| 3     | **Bot cooldown** — Renovate `minimumReleaseAge` OR Dependabot `cooldown.default-days` | Automated PRs auto-merging fresh versions before they can be reviewed |
| 4     | **Install-time scanner** — bun `[install.security]` + `@socketsecurity/bun-security-scanner` (bun) or `socket npm/pnpm install` wrapper | Known-malicious / typosquat / compromised packages, even if they're old |
| 5     | **PR-time scanner** — `.github/workflows/socket-basics.yml` (SAST + secrets + reachability) | Issues *inside* the code that did get installed                 |

Cooldown alone is not enough. Scanner alone is not enough. **Layer all five.**

---

## Ecosystem Support Matrix

| Manager       | Native release-age gate?  | Postinstall blocked by default? | Install-time scanner API? | Other supply-chain features |
|---------------|---------------------------|---------------------------------|---------------------------|-----------------------------|
| **pnpm v10+** | **YES** (`minimumReleaseAge`, minutes) | **YES** (allow via `allowBuilds`) | NO (use `socket pnpm add` wrapper) | `blockExoticSubdeps`, `trustPolicy`, signed-publisher gating |
| **bun** 1.2+  | **YES** (`minimumReleaseAge`, seconds) | YES (only `trustedDependencies` runs) | **YES** — `[install.security]` + `@socketsecurity/bun-security-scanner` | `ignoreScripts`, `minimumReleaseAgeExcludes` |
| npm 11        | NO (`minimum-release-age` is silently ignored) | NO (opt-in via `ignore-scripts=true`) | NO (use `socket npm install` wrapper) | Verdaccio proxy for cooldown |
| yarn v1       | NO (inherits npm)         | NO (opt-in via `ignore-scripts=true` in `.npmrc`) | Same as npm |
| yarn berry v4+| NO                        | YES with `enableScripts: false` | Verdaccio proxy for cooldown |
| uv            | NO                        | n/a (Python wheels have no JS-style scripts) | `uv.lock` + SHA256 hashes |
| pip           | NO                        | n/a                             | `--require-hashes` + `pip-audit` |
| mise          | NO                        | n/a                             | Exact version pins + `paranoid = true` SHA512/GPG |

> **Common mistake**: `min-release-age` / `minimum-release-age` in `~/.npmrc` are
> **Verdaccio-only** as far as npm itself is concerned. npm 11 parses the field but
> does not honor it during install resolution. Do not rely on it for standard npm.
> Use pnpm or bun for native cooldown; for npm, use a proxy (Verdaccio) or `socket` CLI.

---

## Step 0 — Detect what's in use

Run all detection first; record results before touching any file.

```bash
echo "=== Node ecosystem ==="
test -f package.json      && echo "package.json found"
test -f bun.lockb         && echo "lockfile: bun.lockb (binary)"
test -f bun.lock          && echo "lockfile: bun.lock (text)"
test -f pnpm-lock.yaml    && echo "lockfile: pnpm-lock.yaml"
test -f yarn.lock         && echo "lockfile: yarn.lock"
test -f package-lock.json && echo "lockfile: package-lock.json"

echo "=== Python ecosystem ==="
test -f pyproject.toml    && echo "pyproject.toml"
test -f requirements.txt  && echo "requirements.txt"
test -f requirements.in   && echo "requirements.in"
test -f uv.lock           && echo "lockfile: uv.lock"
test -f poetry.lock       && echo "lockfile: poetry.lock"
test -f Pipfile.lock      && echo "lockfile: Pipfile.lock"

echo "=== Mise ==="
test -f mise.toml         && echo "mise.toml"
test -f .tool-versions    && echo ".tool-versions"

echo "=== Package managers on PATH ==="
which npm bun pnpm yarn uv pip pip3 mise 2>/dev/null

echo "=== GitHub / Socket Basics ==="
git remote -v 2>/dev/null | grep -q github.com \
  && echo "github repo: yes  → will propose Socket Basics workflow" \
  || echo "github repo: no   → Socket Basics not applicable"
test -f .github/workflows/socket-basics.yml \
  && echo "socket-basics.yml: present (will audit, not overwrite)" \
  || echo "socket-basics.yml: missing"

echo "=== Existing machine config ==="
test -f ~/.npmrc              && cat ~/.npmrc      || echo "~/.npmrc missing"
test -f ~/.bunfig.toml        && cat ~/.bunfig.toml || echo "~/.bunfig.toml missing"
test -f ~/.config/pip/pip.conf && cat ~/.config/pip/pip.conf || echo "pip.conf missing"
test -f ~/.config/mise/config.toml && cat ~/.config/mise/config.toml || echo "mise global config missing"
```

Determine the **active Node package manager** by checking in order:
1. `packageManager` field in `package.json` (e.g. `"packageManager": "bun@1.3.13"`)
2. Which lockfile exists: `bun.lock`/`bun.lockb` → bun, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `package-lock.json` → npm
3. Which binary is on PATH

---

## Step 1 — Pinning Diagnosis (read-only audit, no changes yet)

Before touching anything, produce a clear diagnosis of the current security posture.
This gives the user a before/after picture and surfaces the exact problems to fix.

### 1a. Node — audit `package.json`

```bash
if [ -f package.json ]; then
  echo "=== package.json pinning audit ==="

  # Count total deps
  node -e "
    const p = require('./package.json');
    const sections = ['dependencies','devDependencies','peerDependencies','optionalDependencies'];
    let pinned=0, unpinned=[], total=0;
    for (const s of sections) {
      for (const [k,v] of Object.entries(p[s]||{})) {
        total++;
        if (/^[\^~]|>=|>/.test(v)) unpinned.push({section:s,name:k,version:v});
        else pinned++;
      }
    }
    console.log('Total deps:', total);
    console.log('Pinned:', pinned);
    console.log('Unpinned:', unpinned.length);
    unpinned.forEach(d => console.log('  UNPINNED', d.section, d.name, d.version));
  " 2>/dev/null || \
  python3 -c "
import json, re, sys
with open('package.json') as f: p = json.load(f)
sections = ['dependencies','devDependencies','peerDependencies','optionalDependencies']
unpinned = []
total = pinned = 0
for s in sections:
    for k,v in (p.get(s) or {}).items():
        total += 1
        if re.match(r'^[\^~]|>=|>', v): unpinned.append((s,k,v))
        else: pinned += 1
print(f'Total: {total}  Pinned: {pinned}  Unpinned: {len(unpinned)}')
for s,k,v in unpinned: print(f'  UNPINNED  {s}  {k}  {v}')
"
fi
```

### 1b. Node — audit lockfile freshness

```bash
# Check if lockfile exists and is committed to git
for f in bun.lock bun.lockb package-lock.json pnpm-lock.yaml yarn.lock; do
  if [ -f "$f" ]; then
    git ls-files --error-unmatch "$f" 2>/dev/null \
      && echo "COMMITTED: $f" \
      || echo "NOT IN GIT: $f  ← must be committed"
  fi
done
```

### 1c. Python — audit pyproject.toml / requirements.txt

```bash
if [ -f pyproject.toml ]; then
  echo "=== pyproject.toml range specifiers ==="
  grep -nE '>=|~=|!=|>|<|\*|\^' pyproject.toml \
    && echo "WARNING: range specifiers found above" \
    || echo "No range specifiers found"
fi

if [ -f requirements.txt ]; then
  echo "=== requirements.txt pinning audit ==="
  # Lines without == are unpinned
  grep -vE '^\s*#|^\s*$|==' requirements.txt \
    && echo "WARNING: unpinned packages above" \
    || echo "All requirements pinned with =="
  # Lines without --hash are hash-less
  grep -c '\-\-hash=' requirements.txt \
    && echo "hash entries found" \
    || echo "WARNING: no --hash entries — not hash-pinned"
fi
```

### 1d. mise — audit version pins

```bash
for f in mise.toml .tool-versions; do
  if [ -f "$f" ]; then
    echo "=== $f pinning audit ==="
    # Flag versions that are not fully pinned (no patch version)
    grep -E 'latest|lts|^[0-9]+$|^[0-9]+\.[0-9]+$' "$f" \
      && echo "WARNING: fuzzy version strings above (missing patch version)" \
      || echo "All tool versions appear fully pinned"
  fi
done
```

### 1e. Print diagnosis summary

After running the checks above, print a concise table:

```
=== DIAGNOSIS REPORT ===

Node / package.json:
  Total deps:    N
  Pinned:        N  (exact semver, no ^ or ~)
  Unpinned:      N  ← will be fixed in Step 7
    UNPINNED  dependencies    react          ^18.2.0
    UNPINNED  devDependencies typescript     ~5.4.0
    ...

Lockfile:
  bun.lock ............. present / MISSING
  committed to git ..... YES / NO  ← must be committed

Python:
  uv.lock .............. present / MISSING
  requirements.txt ..... pinned / N unpinned packages
  hash-pinned .......... YES / NO

mise:
  mise.toml ............ pinned / N fuzzy versions
  committed to git ..... YES / NO

Overall risk level:
  HIGH   — unpinned deps + no lockfile committed
  MEDIUM — lockfile committed but deps have ^ or ~
  LOW    — all pinned + lockfile committed
```

Do NOT make any changes yet. Present this report and confirm with the user before
proceeding to Step 2.

---

## Step 2 — Renovate / Dependabot Audit

Renovate and Dependabot are the long-term automation layer: they open PRs when
new versions are available, and **as of July 2025 both support a native
release-age cooldown.** This step makes sure that gate exists and is set
correctly. Without it, the manual cooldown you set in Step 4–6 protects the
machine doing the install, but Renovate/Dependabot would still flood you with
PRs containing fresh, unverified versions.

### 2a. Renovate vs Dependabot — choose one

| Capability                                      | Renovate                                       | Dependabot (GitHub-hosted)                       |
|-------------------------------------------------|------------------------------------------------|--------------------------------------------------|
| Cooldown setting                                | `minimumReleaseAge` (duration string)          | `cooldown.default-days` (integer days)           |
| Per-update-type cooldown (major/minor/patch)    | yes (`packageRules` + `matchUpdateTypes`)      | yes (`semver-major-days`, `semver-minor-days`, `semver-patch-days`) |
| Per-package allowlist/denylist                  | yes (`matchPackageNames`)                      | yes (`include` / `exclude`, wildcards, 150 max)  |
| **Applies to security updates?**                | **yes (configurable)**                         | **NO — version updates only** (security PRs bypass cooldown) |
| `rangeStrategy: "pin"` to keep deps exact       | yes                                            | no equivalent — relies on `package.json` already pinned |
| Auto-merge                                      | built-in `automerge` field                     | none (use GitHub Auto-merge + branch protection) |
| Setup                                           | install GitHub App, no workflow needed         | commit `.github/dependabot.yml`, no app          |
| SHA-pin GitHub Actions / Docker tags            | yes (`pinDigests: true`)                       | yes (default for `github-actions` ecosystem)     |
| Default cooldown if unset                       | **0** — immediate PRs                          | **0** — immediate PRs                            |

**Decision rule:**
- Repo already on **Dependabot** → upgrade its config in place. No reason to migrate.
- Repo has nothing → **Renovate** is the broader tool (security updates also gated, finer
  control), but **Dependabot is fine** and has a lighter setup.
- Repo on **Renovate** → keep it.

> **The security-update caveat for Dependabot matters.** A "security update" PR
> from Dependabot does not respect `cooldown` — it's opened immediately based on
> the GitHub Advisory Database. That's usually what you want (fast patching),
> but it does mean a malicious advisory or compromised yanked-and-republished
> version could still arrive on day 0. Renovate's cooldown applies to security
> updates too unless you opt out.

### 2b. Detect existing configuration

```bash
echo "=== Renovate config ==="
for f in renovate.json renovate.json5 .renovaterc .renovaterc.json \
          .github/renovate.json .github/renovate.json5 \
          .gitlab/renovate.json .gitlab/renovate.json5; do
  test -f "$f" && echo "FOUND: $f" && cat "$f"
done

echo "=== Renovate self-hosted workflow ==="
find .github/workflows -type f \( -name "*.yml" -o -name "*.yaml" \) 2>/dev/null \
  | xargs grep -l -i "renovate" 2>/dev/null

echo "=== Dependabot config ==="
for f in .github/dependabot.yml .github/dependabot.yaml; do
  test -f "$f" && echo "FOUND: $f" && cat "$f"
done
```

### 2c. Assess existing config

**For Renovate**, check these settings exist:

```bash
RENOVATE_CFG=$(ls renovate.json* .renovaterc* .github/renovate.json* 2>/dev/null | head -1)
if [ -n "$RENOVATE_CFG" ]; then
  grep -q '"minimumReleaseAge"' "$RENOVATE_CFG" \
    && echo "✓ minimumReleaseAge configured" \
    || echo "✗ MISSING minimumReleaseAge — fresh packages will be PR'd immediately"
  grep -q '"rangeStrategy"' "$RENOVATE_CFG" \
    && echo "✓ rangeStrategy set" \
    || echo "✗ MISSING rangeStrategy — ^/~ may sneak back in on update"
  grep -q '"pinDigests"' "$RENOVATE_CFG" \
    && echo "✓ pinDigests set" \
    || echo "⚠ pinDigests not set — Docker/Actions only pinned to mutable tags"
fi
```

**For Dependabot**, check the `cooldown` block exists per ecosystem:

```bash
if [ -f .github/dependabot.yml ]; then
  grep -q 'cooldown:' .github/dependabot.yml \
    && echo "✓ cooldown block present" \
    || echo "✗ MISSING cooldown — version updates will be PR'd immediately"
  grep -q 'default-days:' .github/dependabot.yml \
    && echo "✓ default-days set" \
    || echo "✗ MISSING default-days inside cooldown"
fi
```

### 2d. Apply or upgrade — Renovate path

If creating fresh, write `.github/renovate.json`:

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "minimumReleaseAge": "7 days",
  "rangeStrategy": "pin",
  "pinDigests": true,
  "dependencyDashboard": true,
  "automerge": false,
  "schedule": ["after 9am and before 5pm every weekday"],
  "vulnerabilityAlerts": {
    "minimumReleaseAge": "3 days"
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "minimumReleaseAge": "3 days"
    },
    {
      "matchUpdateTypes": ["minor", "major"],
      "minimumReleaseAge": "7 days"
    },
    {
      "matchDepTypes": ["devDependencies"],
      "minimumReleaseAge": "3 days"
    }
  ]
}
```

Then install the [Renovate GitHub App](https://github.com/apps/renovate) on the
repository. No workflow file needed for the hosted service.

### 2e. Apply or upgrade — Dependabot path (cooldown GA July 2025)

If creating fresh or adding cooldown to an existing config, write
`.github/dependabot.yml`. The verbatim field names are
`cooldown.default-days`, `cooldown.semver-major-days`,
`cooldown.semver-minor-days`, `cooldown.semver-patch-days`,
`cooldown.include`, `cooldown.exclude`.

```yaml
# Verified against
# https://docs.github.com/en/code-security/dependabot/working-with-dependabot/dependabot-options-reference#cooldown
version: 2
updates:
  - package-ecosystem: "npm"          # or "bun", "pnpm" via npm ecosystem
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels: ["dependencies"]
    cooldown:
      default-days: 7
      semver-major-days: 30           # majors: extra time for ecosystem to react
      semver-minor-days: 7
      semver-patch-days: 3            # patches usually safe sooner
      include:
        - "*"
      exclude: []                     # add internal scopes here if needed
    groups:
      production-dependencies:
        dependency-type: "production"
        update-types: ["minor", "patch"]
      development-dependencies:
        dependency-type: "development"
        update-types: ["minor", "patch"]

  - package-ecosystem: "pip"          # or "uv" via the pip ecosystem
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels: ["dependencies"]
    cooldown:
      default-days: 7
      semver-major-days: 30
      semver-minor-days: 7
      semver-patch-days: 3
    groups:
      python-dependencies:
        patterns: ["*"]
        update-types: ["minor", "patch"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels: ["dependencies", "ci"]
    cooldown:
      default-days: 7
```

Notes:

- Dependabot has **no `automerge:` field** — automerge is configured via
  GitHub Auto-merge + branch protection, or via a separate Action. Omitting it
  is the safe default.
- **Security updates bypass `cooldown`.** Track this consciously: if a known
  CVE lands, Dependabot will open the PR immediately regardless of `cooldown`.
  Pair with `permissions: read-only` workflows and human-approval branch
  protection for high-risk repos.
- For Docker / containers, add a `docker` block with cooldown to avoid pulling
  base images within hours of publish.

### 2f. If both Renovate and Dependabot exist

Pick one and disable the other. Running both creates duplicate PRs, doubles
the review load, and makes it ambiguous which tool is enforcing cooldown.

- Keep **Renovate** if you want cooldown on security updates too.
- Keep **Dependabot** if you want a zero-app, in-repo config with weekly cadence.

Then delete the unused config file in the same PR.

### 2g. Verify after merge

```bash
# Renovate
gh issue list --label "renovate" --state open 2>/dev/null | head
# Dependabot — last 5 PRs and their cooldown effect
gh pr list --author "app/dependabot" --state all --limit 5 \
  --json number,title,createdAt,baseRefName \
  --jq '.[] | "\(.number) \(.createdAt) \(.title)"'
```

If you see a Dependabot PR opened within 24 h of a release date, the cooldown
isn't in effect — re-check the YAML indentation under the right ecosystem block.

---

## Step 3 — npm (machine-wide)

npm has NO native release-age filtering. `min-release-age` in `.npmrc` is Verdaccio-only
and is silently ignored by npm itself.

### 1a. Edit `~/.npmrc`

Read first, preserve every existing line (auth tokens, registries, etc.), then append
only what is missing:

```ini
# supply-chain hardening
save-exact=true
```

`save-exact=true` prevents `^` from creeping back in on every future `npm install`.

### 1b. Block postinstall scripts (npm) — `ignore-scripts`

The fastest, most reliable npm-side mitigation. Most malicious npm versions exfiltrate
secrets through `postinstall` scripts that run within seconds of `npm install`.
Disable them globally and re-enable per-project only when genuinely needed.

Add to `~/.npmrc`:

```ini
ignore-scripts=true
```

For packages that legitimately need install scripts (native modules like `esbuild`,
`@swc/core`, `sharp`, `better-sqlite3`), enable per-invocation:

```bash
npm install --ignore-scripts=false   # explicit opt-in
```

### 1c. socket.dev — npm-native supply-chain scanning

```bash
npm install -g socket
socket --version
```

Use as a drop-in wrapper for install commands:

```bash
socket npm install          # replaces: npm install
socket npm install lodash   # replaces: npm install lodash
socket pnpm add lodash      # also wraps pnpm and yarn
```

Or add to `package.json` as a pre-install guard:

```json
{
  "scripts": {
    "preinstall": "npx -y socket npm install --dry-run"
  }
}
```

### 1c. Verdaccio — true team-wide release-age cooldown (enterprise)

```bash
npm install -g verdaccio verdaccio-package-age
```

`~/.config/verdaccio/config.yaml`:

```yaml
packages:
  '**':
    access: $all
    proxy: npmjs
    release-age:
      min-age: 604800   # 7 days in seconds
```

Start: `verdaccio &`

Point `.npmrc` at it:

```ini
registry=http://localhost:4873
min-release-age=604800
```

### 1d. Verify

```bash
npm config get save-exact   # → true
```

---

## Step 4 — Bun (machine-wide) — NATIVE SUPPORT

Bun has first-class release-age support: `--minimum-release-age <seconds>`.

### 2a. Edit `~/.bunfig.toml`

Read the file first. If an `[install]` block already exists, merge `minimumReleaseAge`
into it. Otherwise append:

```toml
[install]
# Refuse packages published < 7 days ago (604800 seconds)
minimumReleaseAge = 604800

# Pin all `bun add` writes to exact versions (no ^ or ~).
exact = true

# CI safety: fail when bun.lock would be modified instead of silently rewriting.
frozenLockfile = true

# Use the diff-friendly text lockfile so it reviews like a real file in PRs.
saveTextLockfile = true

# Bun already only runs install scripts for packages listed in `trustedDependencies`
# in package.json — so explicit script blocking is rarely needed. To be extra strict:
# ignoreScripts = true
```

> Bun merges `~/.bunfig.toml` (global) with the project-level `bunfig.toml`.
> The CLI flag `--minimum-release-age=<seconds>` overrides both.
> By default, bun **does not** run lifecycle scripts for installed dependencies —
> only those listed under `trustedDependencies` in `package.json`. This is already
> safer than npm/yarn-v1 out of the box.

### 4c. Install-time scanner — `bun` Security Scanner API (Bun 1.2+)

Bun ships a native Security Scanner API that runs *during* `bun install` /
`bun add` and can **stop the install** before the malicious code lands on disk.
This is the strongest defense bun offers, and it's complementary to the cooldown:

- `minimumReleaseAge` — refuses **fresh** versions (time-based).
- Security scanner — refuses **known-malicious** versions (signature-based),
  no matter how old.

Use Socket's free scanner — it works without a Socket account; an API key only
unlocks org-specific policy:

```bash
# Add the scanner as a dev dependency (project-level)
bun add -d @socketsecurity/bun-security-scanner
```

Merge into the project's `bunfig.toml` (NOT the global one — scanners are
per-project):

```toml
[install]
minimumReleaseAge = 604800           # 7 days
exact = true
frozenLockfile = true
saveTextLockfile = true

[install.security]
scanner = "@socketsecurity/bun-security-scanner"
```

How it behaves:

| Advisory level | Interactive shell             | CI / non-TTY                   |
|----------------|-------------------------------|--------------------------------|
| `fatal`        | install stops, non-zero exit  | install stops, non-zero exit   |
| `warn`         | prompt: continue? [y/N]       | install stops, non-zero exit   |

Bun also disables `--auto-install` automatically when a scanner is configured —
no more silent transitive resolution.

Optional: enable org-policy mode by setting `SOCKET_API_KEY` (scope: `packages`)
in CI secrets. Without the key, the scanner falls back to Socket's free public
API, which still flags known typosquats and compromised packages.

> Reference: https://bun.com/docs/pm/security-scanner-api
> Custom scanner template: https://github.com/oven-sh/security-scanner-template

### 2b. Verify

```bash
cat ~/.bunfig.toml
```

---

## Step 5 — pnpm (machine-wide + project) — NATIVE SUPPORT (v10+)

pnpm v10/v11 has the most complete supply-chain feature set of any Node manager. All
settings below go in **`pnpm-workspace.yaml`** at the repo root (NOT `.npmrc`, NOT
`package.json`).

### 5a. Project-level: `pnpm-workspace.yaml`

Create or merge into the existing file:

```yaml
# Release-age cooldown — refuse versions published less than N minutes ago.
# 10080 = 7 days. Set to 0 to disable.
minimumReleaseAge: 10080

# Refuse to install when registry timestamp metadata is missing or unreliable
# (catches registries that strip publish timestamps to bypass the cooldown).
minimumReleaseAgeStrict: true
minimumReleaseAgeIgnoreMissingTime: false

# Default range prefix for `pnpm add` — empty string == exact pin (no ^ or ~).
savePrefix: ""

# Block transitive deps from exotic sources (git URLs, tarballs).
# Forces every transitive dep through the configured registry.
blockExoticSubdeps: true

# Refuse a version whose trust evidence regressed vs. a previous version.
# (e.g. previous version was provenance-signed but this one isn't.)
trustPolicy: no-downgrade

# Skip trust checks for packages older than this — useful for legacy deps
# that predate provenance/signing requirements.
trustPolicyIgnoreAfter: 30d

# Allowlist for packages that may bypass trustPolicy (rare; document each entry).
# trustPolicyExclude:
#   - 'some-legacy-pkg@<2.0.0'

# Catch-all kill switch. Must stay false; the per-package `allowBuilds`
# allowlist below is the only way scripts should be enabled.
dangerouslyAllowAllBuilds: false

# Allowlist of packages permitted to run postinstall / lifecycle scripts.
# Default is empty — meaning NO dependency runs install scripts.
# Add only packages that genuinely require a native build step.
allowBuilds:
  esbuild: true
  '@swc/core': true
  # sharp: true
  # better-sqlite3: true
```

### 5d. `package.json` — declare the required pnpm major

Add to `package.json` so a fresh clone fails fast on the wrong version:

```json
{
  "packageManager": "pnpm@<verified-latest>",
  "devEngines": {
    "packageManager": {
      "name": "pnpm",
      "version": ">=11.0.0",
      "onFail": "download"
    }
  }
}
```

**Don't hardcode the version.** Resolve the current pnpm `latest` first:

```bash
npm view pnpm dist-tags --json
# → { "latest": "11.x.y", ... } — use that exact string in `packageManager`
```

Treat pnpm < 11 as a hardening gap, not as "good enough." pnpm 10 lacks
`trustPolicy` and the v11 allowBuilds model.

### 5b. Machine-wide: `~/.npmrc` (still relevant)

pnpm reads `~/.npmrc` for registry/auth and for `save-exact`:

```ini
save-exact=true
strict-peer-dependencies=true
```

### 5c. Verify

```bash
pnpm config get minimumReleaseAge      # → 10080
pnpm config get blockExoticSubdeps     # → true
pnpm config get trustPolicy            # → no-downgrade
```

Try a fresh install and confirm refusal of brand-new versions:

```bash
pnpm add some-package@latest    # should refuse if version is < 7 days old
```

### Key concepts

| Setting                   | What it stops                                                         |
|---------------------------|-----------------------------------------------------------------------|
| `minimumReleaseAge`       | The "fast-moving malware" window (most attacks are caught in hours)   |
| `allowBuilds` (allowlist) | Compromised package running `postinstall` to drop a payload at install |
| `blockExoticSubdeps`      | A normal-looking dep silently pulling a malicious git repo as a transitive dep |
| `trustPolicy: no-downgrade` | A version going from "signed by known publisher" to "unsigned"      |
| `dangerouslyAllowAllBuilds: false` (default) | Catch-all: lifecycle scripts only run when the user explicitly allowlists them |

---

## Step 6 — Yarn (machine-wide)

**Yarn v1** — inherits `~/.npmrc`. Step 1a covers it.

**Yarn Berry (v2+)** — append to `~/.yarnrc.yml` (create if missing):

```yaml
enableStrictSsl: true
nodeLinker: node-modules

# Block all dependency lifecycle scripts (postinstall, etc.)
# Re-enable per package via dependenciesMeta in package.json if genuinely needed.
enableScripts: false
```

To allow one specific package to run install scripts, add to `package.json`:

```json
{
  "dependenciesMeta": {
    "esbuild@0.21.5": { "built": true }
  }
}
```

True release-age filtering for Yarn Berry requires a Verdaccio proxy (Step 1c).

---

## Step 7 — uv (machine-wide + project)

uv has no release-age gate, but its lockfile model is the strongest Python supply-chain
tool available.

### 5a. Machine-wide: pip hash enforcement

Edit `~/.config/pip/pip.conf` (macOS/Linux). Read first, preserve existing, append:

```ini
[install]
require-hashes = true
```

`require-hashes` activates when requirements files contain `--hash=sha256:...` lines.
It does not block uv (uv has its own hash verification via `uv.lock`).

### 5b. Project: generate `uv.lock`

`uv.lock` is uv's full resolution lockfile — it pins every transitive dependency to an
exact version and SHA256 hash. This is the Python equivalent of `bun.lock`.

```bash
# If pyproject.toml exists (preferred):
uv lock                          # creates/updates uv.lock
uv sync                          # installs from uv.lock

# If requirements.in exists:
uv pip compile requirements.in --hash -o requirements.txt
uv pip sync requirements.txt

# Verify lockfile is up to date (use in CI):
uv lock --check                  # exits non-zero if uv.lock is stale
```

### 5c. Pin exact versions in pyproject.toml

Check `[project.dependencies]` for range specifiers and tighten them:

```bash
grep -E '>=|~=|!=|\*|\^|>|<' pyproject.toml && echo "WARNING: range specifiers found"
```

Replace ranges with exact pins where possible:

```toml
# Before
dependencies = ["httpx>=0.24", "pydantic~=2.0"]

# After
dependencies = ["httpx==0.27.0", "pydantic==2.7.1"]
```

> For libraries (not apps), exact pins in `pyproject.toml` are too strict — use ranges
> there and rely on `uv.lock` for the locked install. Warn the user if this is a library.

### 5d. pip-audit in CI

```bash
uv tool install pip-audit        # install globally via uv tools
# or: pip install pip-audit

pip-audit                        # audit current venv
pip-audit -r requirements.txt    # audit a file
```

### 5e. Verify

```bash
test -f uv.lock && echo "uv.lock present" && head -5 uv.lock
```

---

## Step 8 — mise (machine-wide + project)

mise manages runtime versions (Node, Python, Ruby, Go, etc.). Unpinned tool versions
(`latest`, `20.x`, `3.x`) let mise silently install a newly published — potentially
compromised — runtime.

### 6a. Detect tool version files

```bash
test -f mise.toml      && cat mise.toml
test -f .tool-versions && cat .tool-versions
mise ls                # list currently installed tools
```

### 6b. Pin exact versions in `mise.toml`

Read the file. Replace any fuzzy version with the exact installed version.

```toml
# BEFORE (dangerous — resolves to whatever is latest at install time)
[tools]
node = "20"
python = "3.12"
bun = "latest"

# AFTER (safe — pinned to exact version)
[tools]
node = "20.19.1"
python = "3.12.9"
bun = "1.3.13"
```

Get current exact versions to use as pin targets:

```bash
node --version    # → v20.19.1
python3 --version # → Python 3.12.9
bun --version     # → 1.3.13
mise ls           # → full list with current versions
```

### 6c. Pin exact versions in `.tool-versions` (asdf-style)

```
# BEFORE
nodejs 20
python 3.12

# AFTER
nodejs 20.19.1
python 3.12.9
```

### 6d. Enable mise checksum verification (machine-wide)

mise verifies SHA512 checksums of downloaded tool archives. Ensure it's not disabled.

Edit `~/.config/mise/config.toml` (create if missing):

```toml
[settings]
# Never skip checksum verification on tool downloads
paranoid = true
```

`paranoid = true` also enables GPG signature verification where available.

### 6e. Commit mise config

```bash
git add mise.toml .tool-versions 2>/dev/null || true
```

### 6f. Verify

```bash
mise install          # installs all pinned versions
mise doctor           # checks for config issues
```

---

## Step 9 — Pin exact versions in `package.json`

Read `package.json`. Strip `^` and `~` from **every** version string under:
- `dependencies`
- `devDependencies`
- `peerDependencies`
- `optionalDependencies`
- `resolutions` / `overrides`

Rules:
- `"^1.2.3"` → `"1.2.3"`
- `"~1.2.3"` → `"1.2.3"`
- `">=1.2.3"` — leave as-is, warn user (dangerous range)
- `"*"` or `"latest"` — leave as-is, warn user (very dangerous)
- Workspace refs (`"workspace:*"`) — leave unchanged
- GitHub refs (`"github:owner/repo#abc123"`) — leave unchanged

For monorepos: repeat for every workspace `package.json`, not just the root.

Verify after editing:

```bash
grep -E '"[\^~]' package.json && echo "WARNING: unpinned deps remain" || echo "All deps pinned"
```

---

## Step 10 — Nuke and reinstall (Node)

**This step is required.** Simply pinning `package.json` does not update the lockfile.
You must delete and regenerate it so the committed lockfile actually reflects the pinned
versions. Without this step the lockfile still points at whatever `^1.x` resolved to
before.

### Detect which package manager is active, then run the matching block:

**bun:**

```bash
rm -rf node_modules bun.lock bun.lockb
bun install
# Verify the cooldown is active:
# bun will print "minimum release age: 604800s" when the bunfig.toml setting is read
```

**npm:**

```bash
rm -rf node_modules package-lock.json
npm install
```

**pnpm:**

```bash
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

**yarn v1:**

```bash
rm -rf node_modules yarn.lock
yarn install
```

**yarn berry (v2+):**

```bash
rm -rf node_modules .yarn/cache yarn.lock
yarn install
```

After install, verify the lockfile was regenerated:

```bash
test -f bun.lock || test -f bun.lockb || test -f package-lock.json \
  || test -f pnpm-lock.yaml || test -f yarn.lock \
  && echo "Lockfile regenerated" || echo "ERROR: no lockfile found after install"
```

---

## Step 11 — Nuke and reinstall (Python / uv)

For uv projects, delete the virtual environment and reinstall from the lockfile to
ensure a clean, reproducible state:

```bash
# uv project (pyproject.toml + uv.lock)
rm -rf .venv
uv lock          # regenerate uv.lock from pinned pyproject.toml
uv sync          # install into fresh .venv from uv.lock

# requirements.txt project
rm -rf .venv
uv venv
uv pip sync requirements.txt   # install from hash-pinned requirements
```

For pip without uv:

```bash
rm -rf .venv venv env
python3 -m venv .venv
source .venv/bin/activate
pip install --require-hashes -r requirements.txt
```

---

## CI install hardening — what to grep for and flag

Before the Socket Basics workflow, audit existing CI for the patterns that
turn a cooldown into theater. Each of these in a workflow file is a finding
unless the user can point to a written reason:

- **Unfrozen installs**: `npm install`, `yarn install`, `pnpm install` (without
  `--frozen-lockfile`), `bun install` (without `--frozen-lockfile`).
  CI must rebuild from the lockfile, never rewrite it. Use:

  ```yaml
  - run: pnpm install --frozen-lockfile     # pnpm
  - run: bun install --frozen-lockfile      # bun
  - run: npm ci                             # npm fallback
  ```

- **`pull_request_target`** workflows that check out or run PR code. This
  exposes secrets to fork PRs and is the standard escalation vector. Allow
  only with a reviewed reason; never combine with `actions/checkout` of
  `github.event.pull_request.head.ref`.

- **Shared caches feeding publish/release jobs.** GitHub Actions cache,
  Turborepo remote cache, and Nx Cloud cache are all writable by PR runs.
  A privileged release job that warms from the same cache key can be poisoned
  via a PR. Use scoped cache keys (`${{ github.workflow }}-${{ github.sha }}`)
  or skip the cache entirely on publish.

- **`toJSON(secrets)`** anywhere in a workflow expression. There is no
  legitimate reason to serialize the whole secrets bag — it almost always
  ends up in step logs.

- **Lockfile rewrites in CI/deploy.** If a deploy job runs `pnpm install`
  without `--frozen-lockfile`, it accepts whatever the package manager
  resolves *at deploy time*, defeating the committed lockfile entirely.

- **Broad publish credentials.** `NPM_TOKEN` exposed to every job in a
  workflow vs. scoped only to the publish step. Use job-level `env:` and
  publish from a separate workflow when possible.

Quick scan:

```bash
grep -rEn 'pull_request_target|toJSON\(secrets\)|npm install[^[:space:]-]|yarn install[^[:space:]-]' .github/workflows/ 2>/dev/null
grep -rEn 'pnpm install([^-]|$)|bun install([^-]|$)' .github/workflows/ 2>/dev/null
```

Findings here block the Socket Basics suggestion until resolved — there's
no point scanning PRs while the install path itself is exploitable.

---

## Socket Basics PR scanning workflow — recommended second layer

Socket Basics is the free, open-source companion to `socket` (the CLI). As a
GitHub Action, it runs SAST, secret scanning, dependency analysis, and (when
installed natively) Trivy container scanning on every PR — and posts a single
consolidated comment with the findings.

**Always propose this step by default.** Cooldown blocks a malicious version
from landing during install; Socket Basics catches issues *in the code that
already got installed* (transitive vulnerabilities, leaked secrets, dangerous
dependency reachability). They're complementary — running both is the standard
configuration.

### Trigger logic

Run this check first, then act per the table:

```bash
# Is this a GitHub repo?
git remote -v 2>/dev/null | grep -q github.com && echo "github=yes" || echo "github=no"

# Does the workflow already exist?
test -f .github/workflows/socket-basics.yml && echo "exists=yes" || echo "exists=no"
```

| GitHub repo? | Workflow exists? | Action |
|--------------|------------------|--------|
| no           | —                | Skip silently. Note in final report: "Socket Basics not applicable — not a GitHub repo." |
| yes          | yes              | Read the existing file. If it lacks `paths:` filters or `concurrency`, propose an upgrade diff. Otherwise note "Socket Basics already configured." |
| yes          | no               | **Propose creation by default.** Tell the user the file the skill will create, then ask once: *"Create `.github/workflows/socket-basics.yml`? (Y/n)"* — default Yes. |

If the user doesn't have a Socket API key yet, still create the workflow file
and tell them: *"Get a free key at https://socket.dev/dashboard, then run
`gh secret set SOCKET_SECURITY_API_KEY`."* The workflow is harmless without
the key — it just won't run until the secret is set.

### Workflow template

Create `.github/workflows/socket-basics.yml`:

> **Tailor the `paths:` filter to the repo's actual package manager.** A bun-only
> repo doesn't need `pnpm-lock.yaml`, `yarn.lock`, or `package-lock.json` in the
> filter — including unused lockfiles just adds maintenance noise. Trim to match
> what Step 0 detected.

```yaml
name: Socket Basics — supply-chain scan

on:
  workflow_dispatch:        # allow manual runs for testing the workflow itself
  pull_request:
    branches: [develop, main]
    types: [opened, synchronize, reopened]
    paths:
      # Node manifests + lockfiles
      - 'package.json'
      - '**/package.json'
      - 'package-lock.json'
      - 'pnpm-lock.yaml'
      - 'pnpm-workspace.yaml'
      - 'yarn.lock'
      - 'bun.lock'
      - 'bun.lockb'
      # Python manifests + lockfiles
      - 'pyproject.toml'
      - 'requirements.txt'
      - 'requirements.in'
      - 'uv.lock'
      - 'poetry.lock'
      - 'Pipfile'
      - 'Pipfile.lock'
      # Workflow itself
      - '.github/workflows/socket-basics.yml'

# Cancel in-flight runs when a new commit is pushed to the same PR.
concurrency:
  group: socket-basics-${{ github.event.pull_request.number || github.ref }}
  cancel-in-progress: true

permissions:
  contents: read

jobs:
  security-scan:
    name: Socket Basics
    runs-on: ubuntu-24.04
    timeout-minutes: 15
    permissions:
      contents: read
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd # v6.0.2
        with:
          # Full history lets Socket diff dependency changes accurately.
          fetch-depth: 0

      - name: Run Socket Basics
        # SHA-pinned per Socket's recommendation — Dependabot keeps it current.
        # Comment tracks the human-readable version; the SHA is what runs.
        # Verified SHA for v2.0.3 as of 2026-05-13. Re-resolve with:
        #   git ls-remote https://github.com/SocketDev/socket-basics refs/tags/v2.0.3
        uses: SocketDev/socket-basics@fe6259f624e25d30fddf87fd7c255545295cab94 # v2.0.3
        env:
          GITHUB_PR_NUMBER: ${{ github.event.pull_request.number }}
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          socket_security_api_key: ${{ secrets.SOCKET_SECURITY_API_KEY }}
          # socket_org: your-org-slug    # Enterprise: enable Dashboard policy sync
          # SAST — enable only the languages you actually ship.
          # python_sast_enabled: 'true'
          # javascript_sast_enabled: 'true'
          # typescript_sast_enabled: 'true'
          secret_scanning_enabled: 'true'
          socket_tier_1_enabled: 'true'
          console_tabular_enabled: 'true'
```

### Pinning the action

Resolve the SHA for the current release once, then commit it. Dependabot will
keep it fresh:

```bash
git ls-remote https://github.com/SocketDev/socket-basics refs/tags/v2.0.3
# → <SHA>  refs/tags/v2.0.3
# Replace <PIN-A-SHA-HERE> in the workflow with that SHA.
```

Add to `.github/dependabot.yml` (or merge into an existing one):

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
```

### Add the secret

```bash
gh secret set SOCKET_SECURITY_API_KEY --body "<key from socket.dev/dashboard>"
```

`GITHUB_TOKEN` is provided automatically — no setup needed.

### Improvements over the stock template

This template adds, vs. the upstream "Quick Start":

| Addition                       | Why                                                                |
|--------------------------------|--------------------------------------------------------------------|
| `branches: [develop, main]`    | Limits the gate to long-lived branches; feature-branch PRs don't burn minutes. |
| Comprehensive `paths:` filter  | Scan runs only when dependency files change — saves CI time and Socket API quota. |
| Includes `pnpm-workspace.yaml` | Where pnpm v10+ supply-chain policies live; changes here matter.   |
| Includes Python lockfiles      | `pyproject.toml`, `uv.lock`, `poetry.lock`, `Pipfile.lock`.        |
| `concurrency` block            | Cancels stale runs when a PR is force-pushed.                      |
| `fetch-depth: 0`               | Lets Socket compute accurate dep diffs against the base branch.    |
| `timeout-minutes: 15`          | Hard cap so a hung scan never blocks the queue.                    |
| Self-trigger on workflow edits | Catches mistakes in this file during review of the PR that adds it. |
| SHA-pinned with `# v2.0.3` comment | Immutable reference; comment keeps the human-readable version visible. |

### What it won't catch

Socket Basics is not a replacement for the cooldown — it analyzes the code that
*made it through* installation. A 7-day cooldown stops malicious versions from
landing in `node_modules` in the first place. Use both layers together.

---

## Step 12 — Commit everything

Unsigned, uncommitted lockfiles can be silently replaced in CI.

```bash
# Node lockfiles
git add bun.lock bun.lockb package-lock.json pnpm-lock.yaml yarn.lock 2>/dev/null || true

# Python lockfiles
git add uv.lock poetry.lock Pipfile.lock requirements.txt 2>/dev/null || true

# Manifests
git add package.json pyproject.toml 2>/dev/null || true

# Mise config
git add mise.toml .tool-versions 2>/dev/null || true

git diff --cached --name-only   # preview what will be committed

git commit -m "chore: pin exact deps + supply-chain cooldown guards"
```

If no git repo:

```bash
git init && git add -A && git commit -m "chore: initial commit with supply-chain guards"
```

---

## Step 13 — Report

Print a structured summary after completing all steps:

```
=== Package Cooldown Report ===

Machine-level guards:
  ✓/✗ ~/.npmrc               — save-exact=true
  ✓/✗ ~/.bunfig.toml         — minimumReleaseAge=604800 (REAL bun feature, 7 days)
  ✓/✗ ~/.config/pip/pip.conf — require-hashes=true
  ✓/✗ ~/.config/mise/config.toml — paranoid=true
  ✓/✗ socket.dev             — installed (npm install -g @socketsecurity/cli)
  ✗   Verdaccio              — not configured (needed for true npm/pnpm/yarn cooldown)

Project-level guards:
  ✓/✗ package.json    — N deps pinned (list any ranges left unpinned)
  ✓/✗ node_modules    — deleted and reinstalled with [bun|npm|pnpm|yarn]
  ✓/✗ [lockfile]      — regenerated and committed
  ✓/✗ pyproject.toml  — M deps pinned
  ✓/✗ uv.lock         — generated and committed
  ✓/✗ mise.toml       — exact versions pinned, committed
  ✓/✗ .tool-versions  — exact versions pinned, committed

Automation cooldown (Renovate OR Dependabot — pick one):
  ✓/✗ .github/renovate.json    — minimumReleaseAge: "7 days", rangeStrategy: "pin", vulnerabilityAlerts cooldown
  ✓/✗ .github/dependabot.yml   — cooldown.default-days: 7, semver-major-days: 30, exclude: []
  ⚠   ONE of the above, not both — duplicate PRs from both tools doubles review load

CI / PR-time guards:
  ✓/✗ .github/workflows/socket-basics.yml  — Socket Basics PR scan (SAST + secrets + reachability)
  ✓/✗ SOCKET_SECURITY_API_KEY              — repo secret set (gh secret set SOCKET_SECURITY_API_KEY)
  ✓/✗ .github/dependabot.yml               — also keeps Socket Basics action SHA pinned + current

Install-time scanners (where supported):
  ✓/✗ bunfig.toml [install.security]       — bun's native Security Scanner API
  ✓/✗ @socketsecurity/bun-security-scanner  — devDependency installed

Warnings:
  - List any "*", "latest", ">=x", or range specifiers left in place, with reason
  - List any tool managed by mise that still uses a fuzzy version

Next steps:
  - npm/pnpm/yarn: install socket.dev or set up Verdaccio proxy for true cooldown
  - All: add `--frozen-lockfile` (bun/pnpm/yarn) or `--ci` (npm) to CI install
  - Python: run pip-audit in CI (`uv tool run pip-audit`)
  - Consider: add a pre-commit hook that blocks ^ and ~ from re-entering package.json
```

---

## Quick reference — cooldown + lifecycle-script settings

| Manager     | Config file                  | Key                          | Value     | Unit    |
|-------------|------------------------------|------------------------------|-----------|---------|
| pnpm v10+   | `pnpm-workspace.yaml`        | `minimumReleaseAge`          | 10080     | minutes |
| pnpm v10+   | `pnpm-workspace.yaml`        | `blockExoticSubdeps`         | true      | bool    |
| pnpm v10+   | `pnpm-workspace.yaml`        | `trustPolicy`                | `no-downgrade` | enum  |
| pnpm v10+   | `pnpm-workspace.yaml`        | `allowBuilds`                | `{ esbuild: true }` | map |
| bun         | `~/.bunfig.toml [install]`   | `minimumReleaseAge`          | 604800    | seconds |
| bun         | `~/.bunfig.toml [install]`   | `ignoreScripts`              | true      | bool    |
| npm         | `~/.npmrc`                   | `save-exact`                 | true      | bool    |
| npm         | `~/.npmrc`                   | `ignore-scripts`             | true      | bool    |
| npm         | `~/.npmrc`                   | `min-release-age`            | N/A       | NO — Verdaccio only; npm 11 ignores it |
| yarn berry  | `~/.yarnrc.yml`              | `enableScripts`              | false     | bool    |
| yarn berry  | (no native cooldown)         | —                            | —         | —       |
| pip         | `~/.config/pip/pip.conf [install]` | `require-hashes`       | true      | bool    |
| uv          | `uv.lock` (hashes)           | —                            | —         | —       |
| mise        | `~/.config/mise/config.toml [settings]` | `paranoid`        | true      | bool    |

---

## Edge cases to handle gracefully

- **Monorepo (Node)**: delete `node_modules` in root AND every workspace. Reinstall from root.
- **Monorepo (Python)**: run `uv sync --all-packages` if using uv workspaces.
- **`.npmrc` in project root**: also add `save-exact=true` there (project overrides user-level).
- **Verdaccio / private registry**: `min-release-age` belongs on the server config, not client `.npmrc`.
- **CI environments**: machine-level `~/.npmrc` / `~/.bunfig.toml` don't apply in ephemeral containers. Commit a project-level `.npmrc` (no secrets) and `bunfig.toml`.
- **Auth tokens**: never remove or overwrite `//registry.npmjs.org/:_authToken` lines.
- **Frozen lockfile in CI**: always add `--frozen-lockfile` (bun/pnpm/yarn) or `npm ci` to CI install steps so lockfile drift fails the build.
- **uv library vs app**: for libraries, keep range specifiers in `pyproject.toml` but always commit `uv.lock`. Warn the user if the project is a library.
- **mise `latest`**: replacing `latest` requires knowing the currently installed version — run `mise ls` first to get the exact version string to pin.
