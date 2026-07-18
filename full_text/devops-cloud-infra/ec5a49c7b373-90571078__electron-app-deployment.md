---
name: electron-app-deployment
description: Electron app building, code signing, notarization, auto-updates, and CI/CD release pipeline
version: 3.0.0
---

# Electron App Deployment Skill

Complete reference for building, signing, notarizing, and distributing an Electron desktop app across macOS, Windows, and Linux. Covers two toolchains: **electron-forge** (ForgeApp) and **electron-builder** (BuilderApp).

## Architecture Overview

### Electron Forge (ForgeApp)

```
┌─────────────────────────────────────────────────────────┐
│                    Build Pipeline                        │
│                                                         │
│  build:mcp  →  electron-forge publish --arch={arch}     │
│  (TypeScript     (Vite build + package + sign           │
│   compile)        + notarize + publish to GitHub)       │
│                                                         │
│  afterSign hook: scripts/notarize.cjs (macOS only)     │
│  osxSign: configured in forge.config.ts                │
└─────────────────────────────────────────────────────────┘
```

### Electron Builder (BuilderApp)

```
┌─────────────────────────────────────────────────────────┐
│                    Build Pipeline                        │
│                                                         │
│  prepare-server.mjs  →  vite build  →  electron-builder │
│  (bundle server +       (client +      (package + sign  │
│   local packages)        preload)       + notarize)     │
│                                                         │
│  afterPack hook: rebuild-server-natives.cjs              │
│  afterSign hook: notarize.cjs (macOS only)              │
└─────────────────────────────────────────────────────────┘
```

### Shared CI/CD Pattern

```
┌─────────────────────────────────────────────────────────┐
│                  GitHub Actions CI/CD                    │
│                                                         │
│  release.yml (triggered on release publish or tag push) │
│                                                         │
│  verify-version → build-common (shared artifacts)       │
│                          │                              │
│         ┌────────────────┼────────────────┐             │
│         ▼                ▼                ▼             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ macOS    │  │ Windows  │  │  Linux   │  (parallel)  │
│  │ arm64+x64│  │   x64    │  │   x64    │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          ▼                              │
│                  upload-release                          │
│               (softprops/action-gh-release)              │
│                                                         │
│  Both macOS archs run on macos-latest (ARM runner)      │
│  x64 is cross-compiled via --arch flag                  │
└─────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                    Auto-Update                           │
│                                                         │
│  Public repo:  provider: "github" → GitHub Releases     │
│  Private repo: provider: "generic" → Website Proxy      │
│                Website rewrites YML + proxies downloads  │
│                using server-side GITHUB_TOKEN            │
│  Channels: latest, beta                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Electron Forge Configuration (ForgeApp)

File: `forge.config.ts`

```typescript
import type { ForgeConfig } from '@electron-forge/shared-types';

const config: ForgeConfig = {
  packagerConfig: {
    asar: true,
    name: 'YourApp',
    executableName: 'yourapp',  // REQUIRED for Linux deb/rpm makers
    icon: 'resources/icon',
    extraResource: ['resources/some-file.json', 'dist-mcp'],
    osxSign: {
      identity: process.env.APPLE_IDENTITY || '-',
      optionsForFile: () => ({
        entitlements: 'entitlements.mac.plist',
        'entitlements-inherit': 'entitlements.mac.plist',
      }),
    },
    // Use afterSign hook for async notarization — NOT osxNotarize
    // osxNotarize blocks the build waiting for Apple (5-30+ min)
    afterSign: './scripts/notarize.cjs',
  },
  makers: [
    new MakerSquirrel({
      setupIcon: 'resources/icon.ico',
      certificateFile: process.env.WIN_CERTIFICATE_FILE,
      certificatePassword: process.env.WIN_CERTIFICATE_PASSWORD,
    }),
    new MakerZIP({}, ['darwin']),
    new MakerDMG({ format: 'ULFO', icon: 'resources/icon.icns' }),
    new MakerDeb({}),
    new MakerRpm({}),
  ],
  plugins: [
    new VitePlugin({ /* ... */ }),
    new AutoUnpackNativesPlugin({}),
    new FusesPlugin({
      version: FuseVersion.V1,
      [FuseV1Options.RunAsNode]: false,
      [FuseV1Options.EnableCookieEncryption]: true,
      [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false,
      [FuseV1Options.EnableNodeCliInspectArguments]: false,
      [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true,
      [FuseV1Options.OnlyLoadAppFromAsar]: true,
    }),
  ],
  publishers: [
    new PublisherGithub({
      repository: { owner: 'your-org', name: 'your-repo' },
      prerelease: false,
    }),
  ],
};
```

**Critical: `executableName`**
- On Linux, deb/rpm makers look for the binary by `executableName` (lowercase)
- Without it, the binary is named after `name` (e.g., `YourApp`) but installers expect lowercase (`yourapp`)
- Error: `could not find the Electron app binary at ".../{Name}-linux-x64/{name}"`
- On macOS/Windows this field is ignored

**Critical: `afterSign` vs `osxNotarize`**
- **Never use `osxNotarize`** in packagerConfig — it calls `@electron/notarize` synchronously and blocks the build for 5-30+ minutes waiting for Apple
- Use `afterSign` hook with `--no-wait` instead (see Section 6)

## 2. Electron-Builder Configuration (BuilderApp)

Located in `apps/ui/package.json` under the `"build"` key:

```json
{
  "build": {
    "appId": "com.your-app.app",
    "productName": "YourApp",
    "artifactName": "${productName}-${version}-${arch}.${ext}",
    "npmRebuild": false,
    "afterPack": "./scripts/rebuild-server-natives.cjs",
    "afterSign": "./scripts/notarize.cjs",
    "directories": { "output": "release" },
    "publish": {
      "provider": "generic",
      "url": "https://yoursite.com/updates"
    },
    "mac": {
      "category": "public.app-category.developer-tools",
      "hardenedRuntime": true,
      "notarize": false,
      "entitlements": "entitlements.mac.plist",
      "entitlementsInherit": "entitlements.mac.plist"
    },
    "win": {
      "target": [{ "target": "nsis", "arch": ["x64"] }]
    },
    "linux": {
      "target": [
        { "target": "AppImage", "arch": ["x64"] },
        { "target": "deb", "arch": ["x64"] }
      ],
      "category": "Development",
      "executableName": "your-app"
    }
  }
}
```

**Key decisions:**
- `npmRebuild: false` — native modules rebuilt manually via `afterPack` hook
- `notarize: false` — electron-builder's built-in notarization is disabled; handled by custom `afterSign` hook with `--no-wait`
- `afterSign` — notarization runs async, build continues immediately

---

## 3. macOS Entitlements

File: `entitlements.mac.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.cs.allow-jit</key>
    <true/>
    <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/>
    <key>com.apple.security.network.client</key>
    <true/>
    <key>com.apple.security.network.server</key>
    <true/>
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>
</dict>
</plist>
```

**Included entitlements and why:**

| Entitlement | Purpose |
|---|---|
| `cs.allow-jit` | Required for V8/Node.js JIT compilation in Electron |
| `cs.allow-unsigned-executable-memory` | Required for Node.js native addons and V8 |
| `network.client` | Outbound network access (API calls, updates) |
| `network.server` | Local server (e.g., Express backend running inside Electron) |
| `files.user-selected.read-write` | File picker access |

**Additional entitlements (add only if needed):**
- `com.apple.security.cs.disable-library-validation` — for unsigned dylibs
- `com.apple.security.files.downloads.read-write` — for Downloads folder access
- `com.apple.security.automation.apple-events` — for AppleScript automation

---

## 4. Server Bundling (BuilderApp-style monorepo only)

Script: `scripts/prepare-server.mjs`

Bundles the backend server and workspace packages into `server-bundle/` for `extraResources`:

1. Clean previous `server-bundle/` directory
2. Build server TypeScript
3. Copy `dist/` and local workspace packages (dist + package.json only)
4. Create minimal `package.json` with `file:` references
5. `npm install --omit=dev`
6. Replace symlinks with actual copies (npm `file:` creates symlinks that break in packaged apps)
7. `npm rebuild` for native modules

**Critical:** Symlink replacement is essential — electron-builder copies files, not symlinks.

---

## 5. Code Signing

### macOS — Certificate Import (CI)

The actual production approach uses a randomly generated keychain password and `$RUNNER_TEMP` for the keychain path:

```bash
# Decode certificate from GitHub secret (base64-encoded .p12)
echo "$MACOS_CERTIFICATE" | base64 --decode > certificate.p12

# Generate a random keychain password (no need to store as a secret)
KEYCHAIN_PATH=$RUNNER_TEMP/app-signing.keychain-db
KEYCHAIN_PASSWORD=$(openssl rand -base64 32)

# Create temporary keychain with 6-hour lock timeout
security create-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security set-keychain-settings -lut 21600 "$KEYCHAIN_PATH"    # CRITICAL: prevents auto-lock
security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
security import certificate.p12 -k "$KEYCHAIN_PATH" \
  -P "$MACOS_CERTIFICATE_PASSWORD" -T /usr/bin/codesign
security set-key-partition-list -S apple-tool:,apple:,codesign: \
  -s -k "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"

# Add to keychain search list so codesign can find it
security list-keychain -d user -s "$KEYCHAIN_PATH"

rm certificate.p12
```

**Key details:**
- `KEYCHAIN_PASSWORD` is generated randomly with `openssl rand -base64 32` — no need to store it as a GitHub secret
- `$RUNNER_TEMP` ensures unique path per workflow run, avoiding conflicts
- `security list-keychain -d user -s` is **required** — without it, codesign may not find the imported certificate
- `-lut 21600` sets a 6-hour lock timeout; without this, the keychain auto-locks during long builds and signing fails silently

**Verification after build:**
```bash
codesign --verify --deep --strict --verbose=2 "$APP_PATH"
```

### Windows — Two Options

**Option A: Standard OV Certificate (.pfx)**

electron-forge (via MakerSquirrel):
```typescript
new MakerSquirrel({
  certificateFile: process.env.WIN_CERTIFICATE_FILE,
  certificatePassword: process.env.WIN_CERTIFICATE_PASSWORD,
})
```

electron-builder (via env vars — used by BuilderApp):
```
WIN_CSC_LINK=<base64-encoded .pfx or URL to .pfx>
WIN_CSC_KEY_PASSWORD=<certificate password>
```

These are the standard electron-builder env vars; no config changes needed. electron-builder auto-detects them.

**Option B: Azure Key Vault EV Certificate**

```javascript
execSync(
  `AzureSignTool sign ` +
  `-kvu "${AZURE_KEY_VAULT_URI}" ` +
  `-kvt "${AZURE_KEY_VAULT_TENANT_ID}" ` +
  `-kvi "${AZURE_KEY_VAULT_CLIENT_ID}" ` +
  `-kvs "${AZURE_KEY_VAULT_CLIENT_SECRET}" ` +
  `-kvc "${AZURE_KEY_VAULT_CERT_NAME}" ` +
  `-tr http://timestamp.digicert.com ` +
  `-td sha256 ` +
  `"${filePath}"`
);
```

Prerequisite: `dotnet tool install --global AzureSignTool`

### Linux — No Code Signing Required

Linux distributions (AppImage, deb) do not require code signing. No certificates or secrets needed.

---

## 6. macOS Notarization

### The Problem

Apple notarization can take 5-30+ minutes. If your build tool (electron-forge's `osxNotarize` or electron-builder's `notarize: true`) waits synchronously, your CI job can timeout or waste minutes sitting idle.

### The Solution: Async `--no-wait`

Script: `scripts/notarize.cjs` (used as `afterSign` hook in both toolchains)

```javascript
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

exports.default = async function notarizing(context) {
  const { electronPlatformName, appOutDir } = context;

  if (electronPlatformName !== 'darwin') return;

  // NOTE: BuilderApp uses APPLE_APP_SPECIFIC_PASSWORD (not APP_SPECIFIC_PASSWORD)
  // ForgeApp uses APP_SPECIFIC_PASSWORD — match your project's convention
  const { APPLE_ID, APPLE_APP_SPECIFIC_PASSWORD, APPLE_TEAM_ID } = process.env;

  if (!APPLE_ID || !APPLE_APP_SPECIFIC_PASSWORD || !APPLE_TEAM_ID) {
    console.log('Skipping notarization - credentials not provided');
    return;
  }

  const appName = context.packager.appInfo.productFilename;
  const appPath = `${appOutDir}/${appName}.app`;
  const arch = context.arch || 'unknown';

  // Zip the .app for submission
  const zipPath = path.join(appOutDir, `${appName}-notarize.zip`);
  console.log(`Zipping ${appName}.app for notarization (${arch})...`);
  execSync(`ditto -c -k --keepParent "${appPath}" "${zipPath}"`, { stdio: 'inherit' });

  // Submit for notarization WITHOUT waiting
  console.log(`Submitting ${appName} (${arch}) for notarization (no-wait)...`);
  const result = execSync(
    `xcrun notarytool submit "${zipPath}" ` +
    `--apple-id "${APPLE_ID}" ` +
    `--password "${APPLE_APP_SPECIFIC_PASSWORD}" ` +
    `--team-id "${APPLE_TEAM_ID}" ` +
    `--no-wait`,
    { encoding: 'utf-8' }
  );
  console.log(result);

  // Extract and save submission ID for CI verification step
  const idMatch = result.match(/id:\s*([0-9a-f-]+)/);
  if (idMatch) {
    const submissionId = idMatch[1];
    console.log(`Notarization submitted: ${submissionId}`);

    // Write submission ID to file so CI verification step can report it
    const idFile = path.join(appOutDir, 'notarization-id.txt');
    fs.writeFileSync(idFile, submissionId);
    console.log(`Submission ID saved to ${idFile}`);
  }

  // Clean up the zip
  fs.unlinkSync(zipPath);
  console.log('Notarization submitted - build continues without waiting for Apple.');
  console.log('Gatekeeper will verify online when users download the app.');
};
```

### How it works without stapling

- The `--no-wait` flag submits to Apple and returns immediately
- Apple processes the notarization in the background (usually 2-15 min)
- When users download the app, macOS Gatekeeper checks Apple's servers online
- The app runs fine without stapling — stapling just embeds the ticket for offline use

### Optional: Separate Verification Job (BuilderApp-style)

If you want to staple the notarization ticket for offline verification, add a separate CI job:

```yaml
verify-notarization:
  needs: [build-mac]
  if: always()
  runs-on: macos-latest
  timeout-minutes: 20
  steps:
    - name: Download macOS artifacts
      uses: actions/download-artifact@v4
      # ...

    - name: Wait for notarization and staple
      run: |
        for DMG in artifacts/**/*.dmg; do
          ATTEMPTS=0
          MAX_ATTEMPTS=30  # 30 × 30s = 15 minutes
          while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
            if xcrun stapler staple "$DMG" 2>/dev/null; then
              echo "Stapled: $(basename "$DMG")"
              break
            fi
            ATTEMPTS=$((ATTEMPTS + 1))
            echo "Waiting... ($ATTEMPTS/$MAX_ATTEMPTS)"
            sleep 30
          done
        done
```

This is **optional** and non-fatal — most users have internet, so Gatekeeper checks online.

---

## 7. CI/CD Pipeline (GitHub Actions)

### Setting Up GitHub Secrets

Before the pipeline will work, configure these secrets in your GitHub repository settings (Settings → Secrets and variables → Actions):

#### macOS Secrets

| Secret Name | How to Generate |
|---|---|
| `MACOS_CERTIFICATE` | Export your Developer ID Application certificate from Keychain Access as .p12, then `base64 -i certificate.p12 \| pbcopy` |
| `MACOS_CERTIFICATE_PASSWORD` | The password you set when exporting the .p12 |
| `APPLE_ID` | Your Apple Developer account email |
| `APPLE_APP_SPECIFIC_PASSWORD` | Generate at appleid.apple.com → Sign-In and Security → App-Specific Passwords |
| `APPLE_TEAM_ID` | Found at developer.apple.com/account → Membership Details |

#### Windows Secrets

| Secret Name | How to Generate |
|---|---|
| `WIN_CSC_LINK` | Base64-encoded .pfx certificate: `base64 -i cert.pfx \| pbcopy` |
| `WIN_CSC_KEY_PASSWORD` | The .pfx certificate password |

#### General

| Secret Name | Description |
|---|---|
| `GITHUB_TOKEN` | Auto-provided by GitHub Actions (no setup needed) |

### Prerequisite: Apple Developer Account Setup

1. **Enroll** in [Apple Developer Program](https://developer.apple.com/programs/) ($99/year)
2. **Create a Developer ID Application certificate** in Certificates, Identifiers & Profiles
3. **Download and install** the certificate in Keychain Access
4. **Export as .p12** from Keychain Access (right-click → Export) with a strong password
5. **Generate app-specific password** at [appleid.apple.com](https://appleid.apple.com) → Sign-In and Security → App-Specific Passwords

### BuilderApp-style Pipeline (electron-builder, separate jobs)

File: `.github/workflows/release.yml`

This is the actual production pipeline used by the BuilderApp project:

```yaml
name: Release Build

on:
  release:
    types: [published]

permissions:
  contents: write

env:
  NODE_VERSION: '22'

jobs:
  # Step 1: Verify that the git tag matches package.json version
  verify-version:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Verify version matches tag
        run: |
          TAG_VERSION="${{ github.event.release.tag_name }}"
          TAG_VERSION="${TAG_VERSION#v}"
          PKG_VERSION=$(node -p "require('./apps/ui/package.json').version")
          if [ "$TAG_VERSION" != "$PKG_VERSION" ]; then
            echo "Tag version ($TAG_VERSION) does not match package.json ($PKG_VERSION)"
            exit 1
          fi
          echo "Version verified: $TAG_VERSION"

  # Step 2: Build shared artifacts once (not per-platform)
  build-common:
    needs: verify-version
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - name: Build packages
        run: npm run build:packages
      - name: Prepare server bundle
        run: node scripts/prepare-server.mjs
        working-directory: apps/ui
        env:
          SKIP_NATIVE_REBUILD: 'true'
      - name: Build Vite
        run: npx vite build
        working-directory: apps/ui
      - name: Upload shared build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: shared-build
          path: |
            apps/ui/server-bundle/
            apps/ui/dist/
            apps/ui/dist-electron/
          retention-days: 3

  # Step 3a: macOS build (arm64 + x64 in parallel matrix)
  build-mac:
    needs: [verify-version, build-common]
    runs-on: macos-latest
    timeout-minutes: 20
    strategy:
      fail-fast: false
      matrix:
        arch: [x64, arm64]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - name: Download shared build artifacts
        uses: actions/download-artifact@v4
        with:
          name: shared-build
          path: apps/ui
      - name: Import Code Signing Certificate
        env:
          MACOS_CERTIFICATE: ${{ secrets.MACOS_CERTIFICATE }}
          MACOS_CERTIFICATE_PASSWORD: ${{ secrets.MACOS_CERTIFICATE_PASSWORD }}
        if: env.MACOS_CERTIFICATE != ''
        run: |
          echo "$MACOS_CERTIFICATE" | base64 --decode > certificate.p12
          KEYCHAIN_PATH=$RUNNER_TEMP/app-signing.keychain-db
          KEYCHAIN_PASSWORD=$(openssl rand -base64 32)
          security create-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
          security set-keychain-settings -lut 21600 "$KEYCHAIN_PATH"
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
          security import certificate.p12 -k "$KEYCHAIN_PATH" -P "$MACOS_CERTIFICATE_PASSWORD" -T /usr/bin/codesign
          security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$KEYCHAIN_PASSWORD" "$KEYCHAIN_PATH"
          security list-keychain -d user -s "$KEYCHAIN_PATH"
          rm certificate.p12
      - name: Build macOS app (${{ matrix.arch }})
        run: npx electron-builder --mac --${{ matrix.arch }} -p never
        working-directory: apps/ui
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APPLE_APP_SPECIFIC_PASSWORD: ${{ secrets.APPLE_APP_SPECIFIC_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
          CSC_IDENTITY_AUTO_DISCOVERY: ${{ secrets.MACOS_CERTIFICATE != '' }}
      - name: Verify code signing
        if: env.APPLE_ID != ''
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
        run: |
          APP_PATH=$(find apps/ui/release -name "*.app" -type d | head -1)
          if [ -z "$APP_PATH" ]; then
            echo "No .app found"
            exit 1
          fi
          echo "Found app: $APP_PATH"
          echo "Verifying code signature..."
          codesign --verify --deep --strict --verbose=2 "$APP_PATH"
          echo "Code signing verified"
          ID_FILE=$(find apps/ui/release -name "notarization-id.txt" | head -1)
          if [ -n "$ID_FILE" ]; then
            echo "Notarization submission ID: $(cat "$ID_FILE")"
          fi
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: macos-builds-${{ matrix.arch }}
          path: |
            apps/ui/release/*.dmg
            apps/ui/release/*.zip
            apps/ui/release/latest-mac.yml
            apps/ui/release/beta-mac.yml
          retention-days: 30
          if-no-files-found: ignore

  # Step 3b: Windows build
  build-win:
    needs: [verify-version, build-common]
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - name: Download shared build artifacts
        uses: actions/download-artifact@v4
        with:
          name: shared-build
          path: apps/ui
      - name: Build Windows app
        run: npx electron-builder --win -p never
        working-directory: apps/ui
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          WIN_CSC_LINK: ${{ secrets.WIN_CSC_LINK }}
          WIN_CSC_KEY_PASSWORD: ${{ secrets.WIN_CSC_KEY_PASSWORD }}
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: windows-builds
          path: |
            apps/ui/release/*.exe
            apps/ui/release/latest.yml
            apps/ui/release/beta.yml
          retention-days: 30
          if-no-files-found: ignore

  # Step 3c: Linux build (no signing needed)
  build-linux:
    needs: [verify-version, build-common]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - name: Download shared build artifacts
        uses: actions/download-artifact@v4
        with:
          name: shared-build
          path: apps/ui
      - name: Build Linux app
        run: npx electron-builder --linux -p never
        working-directory: apps/ui
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: linux-builds
          path: |
            apps/ui/release/*.AppImage
            apps/ui/release/*.deb
            apps/ui/release/latest-linux.yml
            apps/ui/release/beta-linux.yml
          retention-days: 30
          if-no-files-found: ignore

  # Step 4: Collect all artifacts and upload to GitHub Release
  upload-release:
    needs: [build-mac, build-win, build-linux]
    runs-on: ubuntu-latest
    steps:
      - name: Download macOS x64 artifacts
        uses: actions/download-artifact@v4
        with:
          name: macos-builds-x64
          path: artifacts/macos-builds
        continue-on-error: true
      - name: Download macOS arm64 artifacts
        uses: actions/download-artifact@v4
        with:
          name: macos-builds-arm64
          path: artifacts/macos-builds
        continue-on-error: true
      - name: Download Windows artifacts
        uses: actions/download-artifact@v4
        with:
          name: windows-builds
          path: artifacts/windows-builds
        continue-on-error: true
      - name: Download Linux artifacts
        uses: actions/download-artifact@v4
        with:
          name: linux-builds
          path: artifacts/linux-builds
        continue-on-error: true
      - name: Upload to GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          files: |
            artifacts/macos-builds/*
            artifacts/windows-builds/*
            artifacts/linux-builds/*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### ForgeApp-style Pipeline (electron-forge, single job matrix)

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: macos-latest
            platform: darwin
            arch: arm64
          - os: macos-latest
            platform: darwin
            arch: x64
          - os: windows-latest
            platform: win32
            arch: x64
          - os: ubuntu-latest
            platform: linux
            arch: x64

    runs-on: ${{ matrix.os }}
    timeout-minutes: ${{ matrix.platform == 'darwin' && 5 || 15 }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci

      - name: Build prerequisites
        run: npm run build:mcp

      # macOS: Code signing
      - name: Import macOS certificates
        if: matrix.platform == 'darwin'
        env:
          APPLE_CERTIFICATE: ${{ secrets.APPLE_CERTIFICATE }}
          APPLE_CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          if [ -n "$APPLE_CERTIFICATE" ]; then
            echo "$APPLE_CERTIFICATE" | base64 --decode > certificate.p12
            security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
            security set-keychain-settings -lut 21600 build.keychain
            security default-keychain -s build.keychain
            security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
            security import certificate.p12 -k build.keychain -P "$APPLE_CERTIFICATE_PASSWORD" -T /usr/bin/codesign
            security set-key-partition-list -S apple-tool:,apple:,codesign: -s -k "$KEYCHAIN_PASSWORD" build.keychain
            rm certificate.p12
          fi

      # Windows: Code signing
      - name: Import Windows certificate
        if: matrix.platform == 'win32'
        env:
          WIN_CERTIFICATE_BASE64: ${{ secrets.WIN_CERTIFICATE_BASE64 }}
        shell: powershell
        run: |
          if ($env:WIN_CERTIFICATE_BASE64) {
            $certBytes = [Convert]::FromBase64String($env:WIN_CERTIFICATE_BASE64)
            $certPath = Join-Path $env:RUNNER_TEMP "win-cert.pfx"
            [IO.File]::WriteAllBytes($certPath, $certBytes)
            echo "WIN_CERTIFICATE_FILE=$certPath" >> $env:GITHUB_ENV
          }

      - name: Publish distributables
        env:
          APPLE_ID: ${{ secrets.APPLE_ID }}
          APP_SPECIFIC_PASSWORD: ${{ secrets.APP_SPECIFIC_PASSWORD }}
          APPLE_TEAM_ID: ${{ secrets.APPLE_TEAM_ID }}
          APPLE_IDENTITY: ${{ secrets.APPLE_IDENTITY }}
          WIN_CERTIFICATE_FILE: ${{ env.WIN_CERTIFICATE_FILE }}
          WIN_CERTIFICATE_PASSWORD: ${{ secrets.WIN_CERTIFICATE_PASSWORD }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npm run publish -- --arch=${{ matrix.arch }}
```

### Key CI/CD Decisions

| Decision | Rationale |
|----------|-----------|
| **`verify-version` job** | Catches tag/package.json mismatches before wasting build time |
| **`build-common` shared artifacts** | Build Vite + server bundle once on cheap Ubuntu runner, not per-platform |
| **`-p never` for electron-builder** | Prevents auto-publish; the `upload-release` job handles it centrally |
| **`continue-on-error: true` on artifact downloads** | Release still publishes if one platform fails |
| **Both macOS archs on `macos-latest`** | `macos-13` runners are deprecated. Cross-compile x64 on ARM via `--arch` flag |
| **`timeout-minutes: 20` for macOS** | Allows for npm ci + native rebuild + build |
| **Random keychain password** | Generated with `openssl rand -base64 32` — no need to store as a secret |
| **`security list-keychain -d user -s`** | Required for codesign to find the imported certificate |
| **`CSC_IDENTITY_AUTO_DISCOVERY`** | Set to `true`/`false` based on whether certificate secret exists |

---

## 8. Auto-Update System

Uses `electron-updater` to check for and download updates. Two provider strategies depending on repo visibility:

### Provider Strategy: Public vs Private Repos

| Repo Type | Provider | How It Works |
|-----------|----------|--------------|
| **Public** | `github` | electron-updater hits GitHub Releases API directly — no auth needed |
| **Private** | `generic` + proxy | electron-updater hits your website, which proxies requests to GitHub with a server-side token |

**The `github` provider will NOT work for private repos** — electron-updater has no way to pass a GitHub token at runtime. You must use the `generic` provider with a proxy.

### Public Repo Setup (Simple)

```json
// package.json → build.publish
{
  "provider": "github",
  "owner": "your-org",
  "repo": "your-repo",
  "releaseType": "release"
}
```

No additional infrastructure needed. electron-updater reads `latest-mac.yml` etc. directly from GitHub Releases.

### Private Repo Setup (Proxy Pattern)

This is the production pattern used by BuilderApp. The Electron app points to a generic URL, and a website proxy handles GitHub authentication server-side.

#### 1. electron-builder config

```json
// package.json → build.publish
{
  "provider": "generic",
  "url": "https://yoursite.com/updates"
}
```

#### 2. URL rewrite (Vercel example)

```json
// vercel.json
{
  "rewrites": [
    { "source": "/updates/:filename", "destination": "/api/update-feed?file=:filename" }
  ]
}
```

electron-updater requests `https://yoursite.com/updates/latest-mac.yml` → rewrites to `/api/update-feed?file=latest-mac.yml`.

#### 3. Update feed proxy (`/api/update-feed`)

This endpoint:
1. Fetches the latest GitHub Release using `GITHUB_TOKEN` (server-side secret)
2. Finds the requested YML asset (e.g., `latest-mac.yml`)
3. Downloads the YML content
4. **Rewrites `url:` lines** to point through the download proxy
5. Returns the modified YML

```javascript
// Key: rewrite bare filenames to proxied download URLs
const assetMap = {};
for (const a of release.assets) {
  assetMap[a.name] = `https://yoursite.com/api/download?id=${a.id}`;
}

yml = yml.replace(/^(\s*-?\s*url:\s*)(.+)$/gm, (match, prefix, filename) => {
  const trimmed = filename.trim().replace(/^["']|["']$/g, '');
  if (assetMap[trimmed]) {
    return `${prefix}${assetMap[trimmed]}`;
  }
  return match;
});
```

**Critical:** Only rewrite `url:` lines, NOT `path:` lines. electron-updater uses `path` for local file naming on disk — rewriting it to a URL creates invalid filenames.

**Fallback:** If `/releases/latest` returns 404 (can happen for draft-only releases), fall back to `/releases?per_page=5` and find the first non-draft release.

#### 4. Download proxy (`/api/download`)

This endpoint:
1. Receives an asset ID from electron-updater
2. Requests the asset from GitHub API with `Accept: application/octet-stream` and `GITHUB_TOKEN`
3. GitHub returns a 302 redirect to a temporary pre-signed S3 URL
4. Proxy redirects the client to that URL (client downloads directly from S3)

```javascript
const response = await fetch(
  `https://api.github.com/repos/${GITHUB_REPO}/releases/assets/${id}`,
  {
    headers: {
      Accept: 'application/octet-stream',
      Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
      'User-Agent': 'YourApp-Website',
    },
    redirect: 'manual',  // Don't follow — capture the redirect URL
  }
);

const location = response.headers.get('location');
if (location) {
  return res.redirect(302, location);
}
```

**Key:** Use `redirect: 'manual'` — if you follow the redirect server-side, you'd stream the entire binary through your serverless function. Instead, capture the pre-signed URL and redirect the client to download directly.

#### Architecture diagram

```
┌─────────────┐     GET /updates/latest-mac.yml      ┌─────────────────┐
│  Electron    │ ──────────────────────────────────▶  │  Website/Proxy  │
│  App         │                                      │  (Vercel etc.)  │
│              │  ◀── rewritten YML with proxy URLs── │                 │
│              │                                      │  GITHUB_TOKEN   │
│              │     GET /api/download?id=123         │  (server-side)  │
│              │ ──────────────────────────────────▶  │                 │
│              │  ◀── 302 redirect to S3 URL ──────  │                 │
│              │                                      └────────┬────────┘
│              │     GET (pre-signed S3 URL)                    │
│              │ ──────────────────────────────────▶  GitHub API
└─────────────┘                                      (private repo)
```

#### Environment variables for proxy

| Variable | Where | Description |
|----------|-------|-------------|
| `GITHUB_TOKEN` | Server/Vercel env | ForgeAppl access token or fine-grained token with `contents:read` on the private repo |
| `GITHUB_REPO` | Server/Vercel env | `owner/repo` (e.g., `your-org/your-app`) |

### Main Process Implementation (BuilderApp pattern)

```typescript
import { autoUpdater, UpdateInfo, ProgressInfo } from 'electron-updater';

function initAutoUpdater() {
  if (!app.isPackaged) return;

  autoUpdater.channel = getUpdateChannel();  // 'latest' or 'beta'
  autoUpdater.autoDownload = true;           // Download immediately when found
  autoUpdater.autoInstallOnAppQuit = false;  // Explicit user consent only

  // File logging for debugging
  const logPath = path.join(app.getPath('userData'), 'updater.log');
  autoUpdater.logger = {
    info: (m) => fs.appendFileSync(logPath, `[INFO] ${new Date().toISOString()} ${m}\n`),
    warn: (m) => fs.appendFileSync(logPath, `[WARN] ${new Date().toISOString()} ${m}\n`),
    error: (m) => fs.appendFileSync(logPath, `[ERROR] ${new Date().toISOString()} ${m}\n`),
  };

  // Retry with exponential backoff
  let retryCount = 0;
  const checkWithRetry = () => {
    autoUpdater.checkForUpdates().catch((err) => {
      if (retryCount < 3) {
        retryCount++;
        setTimeout(checkWithRetry, 60000 * retryCount); // 60s, 120s, 180s
      }
    });
  };

  // First check 10s after launch
  setTimeout(checkWithRetry, 10000);

  // Broadcast state to all windows
  autoUpdater.on('update-not-available', () => { /* state → idle */ });
  autoUpdater.on('update-available', (info) => { /* state → downloading */ });
  autoUpdater.on('download-progress', (progress) => { /* update progress % */ });
  autoUpdater.on('update-downloaded', (info) => { /* state → ready */ });
  autoUpdater.on('error', (err) => { /* state → error */ });
}
```

### Update Channels

Channels are persisted in user settings (`{userData}/settings.json`):

```typescript
// Set channel
ipcMain.handle('update:setChannel', (_, channel: string) => {
  settings.updateChannel = channel;
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
  autoUpdater.channel = channel;
  autoUpdater.checkForUpdates(); // Check immediately after switch
});
```

Channels map to YML manifests: `latest-mac.yml` vs `beta-mac.yml`. electron-builder generates separate manifests per channel when you set `channel` in the build config or name your release appropriately.

### IPC Channels

| Channel | Direction | Payload |
|---------|-----------|---------|
| `update:check` | renderer → main | void |
| `update:install` | renderer → main | void (calls `autoUpdater.quitAndInstall(false, true)`) |
| `update:setChannel` | renderer → main | `'latest' \| 'beta'` |
| `update:getState` | renderer → main | returns `UpdateState` |
| `update-status` | main → renderer | `UpdateState` (broadcast to all windows) |

### Update Manifests

Generated automatically by electron-builder on publish:
- `latest-mac.yml` / `beta-mac.yml` — macOS
- `latest.yml` / `beta.yml` — Windows
- `latest-linux.yml` / `beta-linux.yml` — Linux

These must be uploaded to the GitHub Release alongside the binaries. The proxy rewrites download URLs inside them.

---

## 9. Version Kill-Switch

Remote config to block broken versions or enforce minimum versions:

```typescript
// Fetches from your server: /api/remote-config
interface RemoteConfig {
  minVersion: string;         // Minimum supported version (semver)
  blockedVersions?: string[]; // Exact versions to block
  message?: string;           // Custom message for blocked users
}
```

If version is below minimum, shows a dialog and forces update via `autoUpdater.quitAndInstall()`.

---

## 10. Environment Variables Reference

### Code Signing — macOS

| Variable | Description | Used By |
|----------|-------------|---------|
| `MACOS_CERTIFICATE` | Base64-encoded .p12 certificate | BuilderApp (GitHub secret) |
| `MACOS_CERTIFICATE_PASSWORD` | Certificate password | BuilderApp (GitHub secret) |
| `APPLE_CERTIFICATE` | Base64-encoded .p12 certificate | ForgeApp (GitHub secret) |
| `APPLE_CERTIFICATE_PASSWORD` | Certificate password | ForgeApp (GitHub secret) |
| `KEYCHAIN_PASSWORD` | Keychain password (ForgeApp stores as secret, BuilderApp generates randomly) | CI only |
| `APPLE_IDENTITY` | Signing identity string | ForgeApp (electron-forge osxSign) |
| `CSC_IDENTITY_AUTO_DISCOVERY` | Auto-discover signing identity | BuilderApp (electron-builder) |

### Notarization — macOS

| Variable | Description | Used By |
|----------|-------------|---------|
| `APPLE_ID` | Apple Developer account email | Both |
| `APPLE_APP_SPECIFIC_PASSWORD` | App-specific password (not account password) | BuilderApp |
| `APP_SPECIFIC_PASSWORD` | App-specific password (not account password) | ForgeApp |
| `APPLE_TEAM_ID` | Apple Developer Team ID | Both |

### Code Signing — Windows

| Variable | Description | Used By |
|----------|-------------|---------|
| `WIN_CSC_LINK` | Certificate (base64 or path/URL) | BuilderApp (electron-builder) |
| `WIN_CSC_KEY_PASSWORD` | Certificate password | BuilderApp (electron-builder) |
| `WIN_CERTIFICATE_BASE64` | Base64-encoded .pfx | ForgeApp (decoded to file in CI) |
| `WIN_CERTIFICATE_FILE` | Path to .pfx file on disk | ForgeApp (electron-forge) |
| `WIN_CERTIFICATE_PASSWORD` | Certificate password | ForgeApp (electron-forge) |

### Auto-Update Proxy (Private Repos)

| Variable | Description | Where |
|----------|-------------|-------|
| `GITHUB_TOKEN` | PAT or fine-grained token with `contents:read` on private repo | Website/Vercel env (server-side only) |
| `GITHUB_REPO` | `owner/repo` for GitHub API calls (default: your repo) | Website/Vercel env |

### General

| Variable | Description |
|----------|-------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | GitHub token for releases (CI builds) |

---

## 11. Packages Required

### electron-builder (BuilderApp)

```json
{
  "devDependencies": {
    "electron": "^39.x",
    "electron-builder": "^26.x",
    "@electron/rebuild": "^3.x"
  },
  "dependencies": {
    "electron-updater": "^6.x"
  }
}
```

### electron-forge (ForgeApp)

```json
{
  "devDependencies": {
    "electron": "^39.x",
    "@electron-forge/cli": "^7.x",
    "@electron-forge/maker-squirrel": "^7.x",
    "@electron-forge/maker-zip": "^7.x",
    "@electron-forge/maker-deb": "^7.x",
    "@electron-forge/maker-rpm": "^7.x",
    "@electron-forge/maker-dmg": "^7.x",
    "@electron-forge/plugin-vite": "^7.x",
    "@electron-forge/plugin-auto-unpack-natives": "^7.x",
    "@electron-forge/plugin-fuses": "^7.x",
    "@electron-forge/publisher-github": "^7.x",
    "@electron/fuses": "^1.x"
  },
  "dependencies": {
    "electron-updater": "^6.x"
  }
}
```

### macOS CLI Tools (pre-installed on GitHub Actions runners)

- `xcrun notarytool` — Apple's notarization CLI (part of Xcode Command Line Tools)
- `codesign` — Apple's code signing tool
- `ditto` — Apple's archive tool (creates zip for notarization submission)
- `security` — Keychain management CLI

---

## 12. Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| macOS build hangs 10+ min | Using `osxNotarize` (synchronous) | Switch to `afterSign` hook with `--no-wait` |
| `macos-13` runner not supported | GitHub retired `macos-13` runners | Use `macos-latest` for both archs, cross-compile x64 |
| Linux deb/rpm: "could not find binary" | Missing `executableName` | Add `executableName: 'yourapp'` (lowercase) |
| Keychain locks during build | No lock timeout set | Add `security set-keychain-settings -lut 21600` |
| Codesign can't find certificate | Missing `list-keychain` call | Add `security list-keychain -d user -s "$KEYCHAIN_PATH"` |
| macOS job timeout | No `timeout-minutes` set | Add `timeout-minutes: 20` with safety margin |
| Wrong arch built | Host arch used by default | Pass `--arch=${{ matrix.arch }}` explicitly |
| Notarization not stapled | Using `--no-wait` (expected) | Gatekeeper checks online; optionally add stapling job |
| Tag doesn't match version | Forgot to bump `package.json` | Add `verify-version` job to catch early |
| Wasted build time per platform | Building Vite/server on each OS | Use `build-common` job on Ubuntu, share artifacts |
| `APPLE_APP_SPECIFIC_PASSWORD` vs `APP_SPECIFIC_PASSWORD` | Different naming conventions | Match your project's notarize.cjs — check which env var it reads |
| `CSC_IDENTITY_AUTO_DISCOVERY` not set | electron-builder tries to sign without certificate | Set to `${{ secrets.MACOS_CERTIFICATE != '' }}` |
| Auto-update 401/403 on private repo | `provider: "github"` can't auth from packaged app | Use `provider: "generic"` + website proxy with server-side `GITHUB_TOKEN` |
| YML `path:` rewritten to URL | Proxy rewrites `path:` lines too | Only rewrite `url:` lines — `path:` is used for local file naming |
| Download proxy streams entire binary | Proxy follows GitHub 302 redirect | Use `redirect: 'manual'`, capture `location` header, redirect client to pre-signed S3 URL |
| `/releases/latest` returns 404 | No published (non-draft) release exists | Fall back to `/releases?per_page=5` and find first non-draft release |

---

## 13. Release Workflow Checklist

1. Bump version in `package.json` (for electron-builder: `apps/ui/package.json`)
2. Commit and push to main
3. Create a GitHub Release with tag `v{version}` (must match package.json)
4. CI automatically:
   - Verifies tag matches `package.json` version
   - Builds shared artifacts once (Vite + server bundle)
   - Builds for macOS (arm64 + x64 cross-compiled), Windows (x64), Linux (x64)
   - Signs macOS builds with Developer ID certificate
   - Submits macOS builds for Apple notarization (async, `--no-wait`)
   - Verifies code signature with `codesign --verify --deep --strict`
   - Reports notarization submission ID from `notarization-id.txt`
   - Signs Windows builds with certificate (if secrets configured)
   - Publishes all artifacts to GitHub Release via `softprops/action-gh-release`
5. Existing users receive auto-update notification via electron-updater
6. Gatekeeper verifies notarization online when new users download

---

## 14. Troubleshooting Notarization

### Check notarization status manually

```bash
xcrun notarytool info <submission-id> \
  --apple-id "$APPLE_ID" \
  --password "$APPLE_APP_SPECIFIC_PASSWORD" \
  --team-id "$APPLE_TEAM_ID"
```

### View notarization log (on failure)

```bash
xcrun notarytool log <submission-id> \
  --apple-id "$APPLE_ID" \
  --password "$APPLE_APP_SPECIFIC_PASSWORD" \
  --team-id "$APPLE_TEAM_ID"
```

### Common notarization failures

| Error | Cause | Fix |
|-------|-------|-----|
| "The software is not signed" | Missing or invalid code signature | Verify with `codesign --verify --deep --strict` |
| "The signature does not include a secure timestamp" | Missing timestamp | Ensure `hardenedRuntime: true` in config |
| "The executable does not have the hardened runtime enabled" | Missing hardened runtime | Add `hardenedRuntime: true` to mac config |
| "The binary uses an SDK older than 10.9" | Old SDK | Update Xcode / Electron version |
| Invalid credentials | Wrong app-specific password | Regenerate at appleid.apple.com |
