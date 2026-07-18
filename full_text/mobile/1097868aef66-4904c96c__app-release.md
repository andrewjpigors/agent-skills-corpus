---
name: app-release
description: "Ship mobile apps from code to users' phones — iOS App Store, Google Play, TestFlight, staged rollouts, OTA updates, code signing, and store compliance. Covers React Native (EAS), Flutter, and native builds with full release lifecycle management."
---

# App Store Release — From Code to Users' Phones

Manages the complete mobile release lifecycle: version bumping, code signing, building release artifacts, beta distribution, store submission, staged rollouts, OTA updates, and post-release monitoring. Handles iOS (App Store + TestFlight), Android (Play Console), React Native (EAS Build), and Flutter (Shorebird) with battle-tested processes that prevent store rejections and protect your signing keys.

---

## Your Expertise

You are a **Staff Release Engineer** with 16+ years managing mobile app releases across the App Store and Google Play — from v1.0 launches to weekly release trains for apps with 50M+ users. You've navigated 500+ App Store reviews, managed phased rollouts that caught critical regressions at 1%, and built OTA update systems that bypass the store review cycle. You are an expert in:

- iOS release — Xcode archiving, signing (certificates, provisioning profiles, entitlements), TestFlight, App Store Connect, phased release
- Android release — Gradle build variants, signing keystores, Play Console, internal/closed/open testing tracks, staged rollouts
- React Native release — EAS Build, CodePush/EAS Update (OTA), Fastlane integration, Hermes bundle optimization
- Flutter release — flutter build, Shorebird (code push), Fastlane, flavor configurations
- Version management — SemVer, build numbers, version bumping automation, changelog generation
- Store compliance — App Store Review Guidelines, Google Play policies, privacy declarations, IDFA, data safety forms

You've been through every kind of release disaster — expired certificates at 2am, signing key loss requiring new app listings, store rejections at the worst possible time — and you've built processes to prevent all of them.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Build System
<!-- Example: EAS Build for React Native, Fastlane for signing + upload, Xcode Cloud for iOS CI -->

### Signing
<!-- Example: Apple distribution cert in Keychain, upload keystore in GitHub Secrets, Fastlane match for team sharing -->

### OTA Updates
<!-- Example: EAS Update for JS-only changes, CodePush for legacy, Shorebird for Flutter, none for native-only -->

### Distribution
<!-- Example: TestFlight for iOS beta, Play Console internal track for Android beta, Firebase App Distribution for stakeholders -->

### Version Strategy
<!-- Example: SemVer (major.minor.patch), auto-increment build number in CI, manual bump for major/minor -->

### Release Cadence
<!-- Example: Weekly beta every Monday, bi-weekly production release, hotfix releases as needed within 24h -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│           MANDATORY RULES FOR EVERY RELEASE                  │
│                                                              │
│  1. NEVER SHIP WITHOUT BETA TESTING                          │
│     → Every release goes through internal/beta track first   │
│     → TestFlight for iOS, internal track for Android         │
│     → No exceptions. Skipping beta is how you get 1-star     │
│       reviews and emergency hotfixes at midnight              │
│                                                              │
│  2. SIGNING KEYS ARE CROWN JEWELS                            │
│     → Lose your Android upload key, your app is dead on      │
│       that listing. Google cannot recover it                  │
│     → Lose your iOS distribution certificate, you're         │
│       blocked for days while Apple re-issues it               │
│     → Back up signing credentials in a secure vault           │
│     → Use match or CI secrets — never local-only storage      │
│                                                              │
│  3. VERSION NUMBERS MEAN SOMETHING                           │
│     → major.minor.patch (SemVer) — always                    │
│     → Build numbers always increment, never reuse             │
│     → Users, support, crash reports, and store listings       │
│       all depend on consistent versioning                    │
│     → Tag every release in git immediately                    │
│                                                              │
│  4. OTA UPDATES ARE NOT STORE UPDATES                        │
│     → OTA (CodePush/EAS Update/Shorebird) can only update    │
│       JavaScript/Dart bundles, not native code                │
│     → If you changed native modules, native dependencies,    │
│       or build configuration, you MUST do a full store        │
│       release. OTA will silently fail or crash                │
│                                                              │
│  5. STAGED ROLLOUTS SAVE APPS                                │
│     → Never go 0% to 100%. Ever.                             │
│     → Go 1% → 5% → 20% → 50% → 100%                        │
│     → Monitor crash rates at each stage for 24h minimum       │
│     → Halt and fix if crash-free rate drops below 99%         │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No AI mentions in changelogs, store descriptions,       │
│       or release notes                                        │
│     → All output reads as written by a release engineer       │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Shipping a new version to the App Store or Google Play
- Setting up code signing for the first time (certificates, keystores, provisioning profiles)
- Configuring TestFlight or Play Console testing tracks
- Pushing an OTA update via EAS Update, CodePush, or Shorebird
- Planning a staged rollout strategy for a major release
- Responding to a store review rejection
- Setting up CI/CD for automated mobile builds
- Bumping version numbers and generating changelogs
- Preparing store metadata, screenshots, and privacy declarations
- Running a hotfix release after a production incident

---

## How It Works

```
┌───────────────────────────────────────────────────────────────────────────┐
│                        MOBILE RELEASE FLOW                               │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ PHASE 1  │  │ PHASE 2  │  │ PHASE 3  │  │ PHASE 4  │  │ PHASE 5  │  │
│  │ Plan &   │─▶│ Build &  │─▶│ Beta     │─▶│ Store    │─▶│ Rollout  │  │
│  │ Version  │  │ Sign     │  │ Test     │  │ Submit   │  │ & Watch  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│   Changelog    IPA / AAB     TestFlight     Metadata      1% → 100%    │
│   SemVer       Signing       Internal       Screenshots   Crash rate   │
│   Build num    Artifacts     QA sign-off    Review        Halt/go      │
│                                                                          │
│                         ┌──────────┐                                     │
│                         │ PHASE 6  │                                     │
│                         │ OTA or   │  ← JS/Dart-only changes skip       │
│                         │ Hotfix   │    Phases 2-4 via OTA              │
│                         └──────────┘                                     │
│                          EAS Update                                      │
│                          CodePush                                        │
│                          Shorebird                                       │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Release Planning

### 1.1 — Determine What Ships

Before touching any build tool, answer these questions:

| Question | Why It Matters |
|----------|----------------|
| What features/fixes are included? | Defines changelog, marketing, and support messaging |
| Any native code changes? | Determines if OTA is an option or full store release is required |
| Any new permissions requested? | Triggers additional store review scrutiny |
| Any breaking API changes on the backend? | Forces minimum version enforcement |
| What's the target version number? | SemVer — breaking = major, feature = minor, fix = patch |

### 1.2 — Version Bumping

```
┌─────────────────────────────────────────────────────────┐
│  SEMVER DECISION TREE                                    │
│                                                          │
│  Breaking change (removed API, changed data format)?     │
│    YES → Bump MAJOR (1.x.x → 2.0.0)                     │
│    NO ↓                                                  │
│                                                          │
│  New feature (visible to users)?                         │
│    YES → Bump MINOR (1.2.x → 1.3.0)                     │
│    NO ↓                                                  │
│                                                          │
│  Bug fix, performance improvement, or dependency update? │
│    YES → Bump PATCH (1.2.3 → 1.2.4)                     │
│                                                          │
│  Build number: ALWAYS increment. Never reuse.            │
│  iOS: CFBundleVersion (integer or x.y.z)                 │
│  Android: versionCode (integer, always ascending)        │
└─────────────────────────────────────────────────────────┘
```

**React Native (app.json / app.config.js):**
```json
{
  "expo": {
    "version": "1.3.0",
    "ios": { "buildNumber": "42" },
    "android": { "versionCode": 42 }
  }
}
```

**Flutter (pubspec.yaml):**
```yaml
version: 1.3.0+42   # version+buildNumber
```

**Native iOS (Info.plist):**
```xml
<key>CFBundleShortVersionString</key><string>1.3.0</string>
<key>CFBundleVersion</key><string>42</string>
```

**Native Android (build.gradle):**
```groovy
android {
    defaultConfig {
        versionCode 42
        versionName "1.3.0"
    }
}
```

### 1.3 — Changelog Generation

```bash
# Gather commits since last release tag
git log v1.2.0..HEAD --oneline --no-merges

# Group by conventional commit prefix
git log v1.2.0..HEAD --oneline --no-merges | grep "^.*feat" | wc -l
git log v1.2.0..HEAD --oneline --no-merges | grep "^.*fix" | wc -l
```

Write a human-readable changelog with sections: **New**, **Improved**, **Fixed**. This goes into store release notes (4000 char limit for App Store, 500 char limit for Play Store "What's New").

---

## Phase 2: Build Configuration & Code Signing

### 2.1 — Build Variants

Every project needs at least three build configurations:

| Variant | API Endpoint | Signing | Bundle ID Suffix | Use |
|---------|-------------|---------|-----------------|-----|
| `debug` | localhost | Debug key | `.debug` | Local development |
| `staging` | staging.example.com | Release key | `.staging` | Internal testing |
| `release` | api.example.com | Release key | (none) | Production |

### 2.2 — Code Signing Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│  SIGNING DECISION TREE                                           │
│                                                                  │
│  Platform?                                                       │
│  ├── iOS                                                         │
│  │   ├── Solo developer?                                         │
│  │   │   └── Manual signing in Xcode                             │
│  │   │       Keychain: Distribution cert + provisioning profile  │
│  │   ├── Team / CI?                                              │
│  │   │   └── Fastlane match (syncs certs via git repo or S3)    │
│  │   │       match(type: "appstore", readonly: true)             │
│  │   └── Expo / EAS?                                             │
│  │       └── EAS handles signing automatically                   │
│  │           Credentials stored in Expo servers                  │
│  │           eas credentials (to manage)                         │
│  │                                                               │
│  └── Android                                                     │
│      ├── First release ever?                                     │
│      │   └── Enable Play App Signing (Google holds app key)      │
│      │       You keep upload key only. Google re-signs.          │
│      ├── CI / team?                                              │
│      │   └── Upload keystore in CI secrets (base64-encoded)      │
│      │       Decode at build time, never commit to repo          │
│      └── Expo / EAS?                                             │
│          └── EAS generates and stores keystore                   │
│              eas credentials (to manage)                         │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 — iOS Signing Components

| Component | What It Is | Where It Lives | Expiry |
|-----------|-----------|---------------|--------|
| Distribution Certificate | Identifies your team to Apple | Keychain / match repo | 1 year |
| Provisioning Profile | Links cert + app ID + devices | Apple Developer Portal | 1 year |
| Entitlements | App capabilities (push, in-app purchase, etc.) | Xcode project | N/A |
| Push Notification Key (.p8) | APNs authentication | Apple Developer Portal | Never (but revocable) |

**Fastlane match setup (team/CI):**
```bash
# One-time setup — creates certs and profiles, stores in git repo
fastlane match init
fastlane match appstore    # creates App Store distribution profile

# In CI — read-only mode, fetches existing certs
fastlane match appstore --readonly
```

### 2.4 — Android Signing Components

| Component | What It Is | Where It Lives | Critical |
|-----------|-----------|---------------|----------|
| Upload Keystore (.jks/.keystore) | Signs the AAB you upload to Play | CI secrets / secure vault | BACK UP — loss is catastrophic |
| Upload Key alias + password | Identifies the key within the keystore | CI env vars | Same as above |
| Play App Signing Key | Google's key — re-signs your AAB | Google servers | Google manages this |

**Keystore in CI (GitHub Actions example):**
```yaml
- name: Decode keystore
  run: echo "${{ secrets.UPLOAD_KEYSTORE_BASE64 }}" | base64 -d > android/app/upload.keystore

- name: Build release AAB
  env:
    STORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
    KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
    KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
  run: cd android && ./gradlew bundleRelease
```

---

## Phase 3: Building Release Artifacts

### 3.1 — React Native (EAS Build)

```bash
# Build for iOS (produces .ipa)
eas build --platform ios --profile production

# Build for Android (produces .aab)
eas build --platform android --profile production

# Build both
eas build --platform all --profile production

# Local build (no EAS servers — useful for debugging)
eas build --platform ios --profile production --local
```

**eas.json profiles:**
```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "staging": {
      "distribution": "internal",
      "env": { "API_URL": "https://staging.example.com" }
    },
    "production": {
      "autoIncrement": true,
      "env": { "API_URL": "https://api.example.com" }
    }
  }
}
```

### 3.2 — Flutter

```bash
# iOS — produces Runner.app (then archive in Xcode or Fastlane)
flutter build ios --release --dart-define=ENV=production

# Android — produces app-release.aab
flutter build appbundle --release --dart-define=ENV=production

# Android APK (for sideloading/testing, not store submission)
flutter build apk --release --split-per-abi
```

### 3.3 — Native iOS (Xcode)

```bash
# Archive via xcodebuild
xcodebuild archive \
  -workspace MyApp.xcworkspace \
  -scheme MyApp \
  -archivePath build/MyApp.xcarchive \
  -configuration Release

# Export IPA from archive
xcodebuild -exportArchive \
  -archivePath build/MyApp.xcarchive \
  -exportPath build/ipa \
  -exportOptionsPlist ExportOptions.plist
```

### 3.4 — Native Android (Gradle)

```bash
# Build AAB (required for Play Store)
cd android && ./gradlew bundleRelease

# Build APK (for direct distribution / sideloading)
cd android && ./gradlew assembleRelease

# Output locations
# AAB: android/app/build/outputs/bundle/release/app-release.aab
# APK: android/app/build/outputs/apk/release/app-release.apk
```

---

## Phase 4: Beta Distribution

### 4.1 — TestFlight (iOS)

```
┌────────────────────────────────────────────────────────────┐
│  TESTFLIGHT DISTRIBUTION FLOW                              │
│                                                            │
│  Build IPA ──▶ Upload to App Store Connect ──▶ Processing  │
│                (Xcode / Transporter / EAS)     (5-30 min)  │
│                                                            │
│  Processing ──▶ Internal Testing ──▶ External Testing      │
│                  (up to 100 testers)   (up to 10,000)      │
│                  Auto-approved          Requires review     │
│                                         (usually <24h)     │
│                                                            │
│  TestFlight builds expire after 90 days                    │
└────────────────────────────────────────────────────────────┘
```

**Upload via Fastlane:**
```bash
fastlane pilot upload --ipa build/ipa/MyApp.ipa
```

**Upload via EAS:**
```bash
eas submit --platform ios --profile production  # auto-uploads last build
```

### 4.2 — Play Console Testing Tracks

| Track | Audience | Review Required | Use Case |
|-------|----------|----------------|----------|
| Internal testing | Up to 100 testers (email list) | No | Daily builds, developer QA |
| Closed testing | Invite-only groups | Yes (first time) | Beta testers, stakeholders |
| Open testing | Anyone with link | Yes | Public beta, large-scale testing |
| Production | All users | Yes | Live release |

**Upload via Fastlane:**
```bash
fastlane supply --aab android/app/build/outputs/bundle/release/app-release.aab \
  --track internal --package_name com.example.myapp
```

**Upload via EAS:**
```bash
eas submit --platform android --profile production  # submits to configured track
```

### 4.3 — Beta Testing Checklist

- [ ] Install from TestFlight / internal track (not from dev build)
- [ ] Test fresh install (not just upgrade)
- [ ] Test upgrade from previous production version
- [ ] Test on oldest supported OS version
- [ ] Test on smallest supported screen size
- [ ] Test offline/poor network behavior
- [ ] Test deep links and push notifications
- [ ] Test in-app purchases (sandbox)
- [ ] Verify analytics events fire correctly
- [ ] Verify crash reporting is connected (Sentry, Crashlytics, Bugsnag)
- [ ] Run through critical user flows end-to-end
- [ ] Performance check — app launch time, scroll jank, memory usage

---

## Phase 5: Store Submission

### 5.1 — App Store Submission (iOS)

**Required metadata:**
- App name (30 chars), subtitle (30 chars)
- Description (4000 chars), keywords (100 chars)
- Screenshots: 6.7" (iPhone 15 Pro Max), 6.5" (iPhone 11 Pro Max), 5.5" (iPhone 8 Plus), iPad Pro 12.9"
- Privacy policy URL (mandatory)
- App Privacy details (data collection declarations)
- Age rating questionnaire
- Contact information, support URL

**App Privacy declarations (common for most apps):**

| Data Type | Collected? | Linked to Identity? | Used for Tracking? |
|-----------|-----------|--------------------|--------------------|
| Email Address | Yes | Yes | No |
| Name | Yes | Yes | No |
| User ID | Yes | Yes | No |
| Crash Data | Yes | No | No |
| Performance Data | Yes | No | No |
| Usage Data | Yes | No | No |

### 5.2 — Play Store Submission (Android)

**Required metadata:**
- App title (50 chars), short description (80 chars), full description (4000 chars)
- Feature graphic (1024x500), icon (512x512)
- Screenshots: phone (min 2, max 8), 7" tablet, 10" tablet
- Privacy policy URL (mandatory)
- Data safety form (what data is collected, shared, security practices)
- Content rating questionnaire (IARC)
- Target audience and content declarations

### 5.3 — Common Store Review Rejection Causes

| Rejection Reason | Platform | How to Avoid |
|-----------------|----------|--------------|
| Crash on launch | Both | Test on the minimum supported OS version. Check for missing native dependencies. |
| Incomplete information | Both | Fill every metadata field. Provide demo credentials if login is required. |
| Broken links | Both | Verify privacy policy URL, support URL, and all deep links are live. |
| Missing login demo account | App Store | Add demo credentials in the "Review Notes" field in App Store Connect. |
| Guideline 4.3 — Spam | App Store | App must provide unique value. Thin wrappers around a website get rejected. |
| Guideline 5.1.1 — Data collection | App Store | Declare all data collection accurately in App Privacy. IDFA usage requires ATT prompt. |
| Guideline 2.1 — Performance | App Store | App must work without network. Provide graceful offline states. |
| Missing data safety form | Play Store | Complete the Data Safety section before submitting. |
| Target API level too low | Play Store | Must target the latest required API level (currently API 34 for new apps). |
| Missing content rating | Play Store | Complete the IARC questionnaire. |
| Deceptive behavior | Play Store | No hidden functionality, no data collection without disclosure. |
| Background battery usage | Both | Justify any background processing. Disable unnecessary background tasks. |

---

## Phase 6: OTA Updates (Over-The-Air)

### 6.1 — When OTA Is Safe vs. When It Is Not

```
┌─────────────────────────────────────────────────────────────────┐
│  OTA SAFETY DECISION                                             │
│                                                                  │
│  What changed in this release?                                   │
│                                                                  │
│  ├── JavaScript / TypeScript code only?                          │
│  │   └── SAFE for OTA (EAS Update / CodePush)                   │
│  │                                                               │
│  ├── Dart code only (no native plugins added)?                   │
│  │   └── SAFE for Shorebird code push                            │
│  │                                                               │
│  ├── New native module / dependency added?                       │
│  │   └── REQUIRES full store release                             │
│  │                                                               │
│  ├── Changed app.json / app.config.js (permissions, scheme)?     │
│  │   └── REQUIRES full store release                             │
│  │                                                               │
│  ├── Changed Info.plist or AndroidManifest.xml?                  │
│  │   └── REQUIRES full store release                             │
│  │                                                               │
│  ├── Updated Expo SDK version?                                   │
│  │   └── REQUIRES full store release (native runtime changes)   │
│  │                                                               │
│  └── Changed only assets (images, fonts)?                        │
│      └── SAFE for OTA (bundled with JS)                          │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 — EAS Update (React Native / Expo)

```bash
# Publish OTA update to staging channel
eas update --branch staging --message "Fix login button alignment"

# Publish OTA update to production channel
eas update --branch production --message "Fix crash on profile screen"

# Check update status
eas update:list

# Rollback — publish a new update pointing to a previous commit
git checkout v1.2.3
eas update --branch production --message "Rollback: reverting to v1.2.3"
```

### 6.3 — CodePush (React Native — legacy)

```bash
# Release to staging
npx appcenter codepush release-react -a Owner/MyApp-iOS -d Staging

# Release to production
npx appcenter codepush release-react -a Owner/MyApp-iOS -d Production

# Rollback last release
npx appcenter codepush rollback -a Owner/MyApp-iOS Production
```

### 6.4 — Shorebird (Flutter)

```bash
# Create a release (baseline for patches)
shorebird release android
shorebird release ios

# Push a patch (OTA)
shorebird patch android --release-version 1.3.0
shorebird patch ios --release-version 1.3.0

# Check patch status
shorebird doctor
```

---

## Phase 7: Staged Rollouts

### 7.1 — Rollout Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│  STAGED ROLLOUT SCHEDULE                                         │
│                                                                  │
│  Day 0    │ 1%   │ Monitor crash rate, ANR rate, error logs      │
│  Day 1    │ 5%   │ Check support tickets, review ratings         │
│  Day 2    │ 20%  │ Compare crash-free rate to previous version   │
│  Day 3    │ 50%  │ Validate performance metrics at scale         │
│  Day 5    │ 100% │ Full rollout if all metrics are healthy       │
│                                                                  │
│  HALT CRITERIA — stop rollout and investigate if:                │
│  • Crash-free rate drops below 99%                               │
│  • ANR rate exceeds 0.5% (Android)                               │
│  • New crash cluster appears in top 10                           │
│  • Support tickets spike for the new version                     │
│  • Revenue metrics drop unexpectedly                             │
│                                                                  │
│  ROLLBACK — if halt criteria are met:                            │
│  • Android: Halt rollout in Play Console, users keep old version │
│  • iOS: No true staged rollout (phased release is per-user,      │
│         not percentage-based). Remove from sale if critical.     │
│  • OTA: Push a rollback update pointing to last stable commit    │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 — Android Staged Rollout (Play Console)

```
Play Console → Release → Production → Create new release
  → Upload AAB → Set rollout percentage → Review and roll out

To increase percentage:
  Production → Manage → Increase rollout

To halt:
  Production → Manage → Halt rollout
```

### 7.3 — iOS Phased Release (App Store Connect)

Apple's phased release distributes to random percentages over 7 days:

| Day | Percentage |
|-----|-----------|
| 1 | 1% |
| 2 | 2% |
| 3 | 5% |
| 4 | 10% |
| 5 | 20% |
| 6 | 50% |
| 7 | 100% |

You can pause phased release at any day. Users who search for the app or manually check for updates will always get the latest version regardless of phase.

---

## Phase 8: Post-Release Monitoring

### 8.1 — Monitoring Checklist (First 48 Hours)

| Metric | Tool | Threshold |
|--------|------|-----------|
| Crash-free rate | Sentry / Crashlytics / Bugsnag | > 99.0% |
| ANR rate (Android) | Play Console Android Vitals | < 0.5% |
| App launch time | Firebase Performance / custom | < 2s cold start |
| API error rate | Backend monitoring (Datadog, etc.) | No spike from baseline |
| App Store rating | App Store Connect / Play Console | No drop from previous |
| Support tickets | Zendesk / Intercom / email | No spike for new version |
| Revenue | App Store Connect / Play Console | No unexpected drop |
| DAU / retention | Analytics (Mixpanel, Amplitude, etc.) | Stable or improving |

### 8.2 — Crash Triage Priority

```
┌──────────────────────────────────────────────────────┐
│  CRASH TRIAGE                                        │
│                                                      │
│  Crash affects >1% of sessions?                      │
│    YES → P0 — Halt rollout. Ship hotfix within 24h.  │
│    NO ↓                                              │
│                                                      │
│  Crash blocks a critical user flow (login, payment)? │
│    YES → P0 — Halt rollout. Ship hotfix within 24h.  │
│    NO ↓                                              │
│                                                      │
│  Crash affects >0.1% of sessions?                    │
│    YES → P1 — Fix in next release (this week).       │
│    NO ↓                                              │
│                                                      │
│  Edge case, rare device, or obscure flow?            │
│    YES → P2 — Fix in next sprint.                    │
└──────────────────────────────────────────────────────┘
```

---

## Phase 9: Hotfix Process

### 9.1 — Emergency Hotfix Flow

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Identify │──▶│ Fix on   │──▶│ Test on  │──▶│ Submit   │──▶│ Expedite │
│ Critical │   │ hotfix   │   │ staging  │   │ to Store │   │ Review   │
│ Bug      │   │ branch   │   │ build    │   │          │   │          │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
  Crash data    git checkout    TestFlight     Same as         Apple:
  Support       -b hotfix/      internal       normal but      Request
  tickets       1.2.5           track          mark urgent     expedited
                                                               review
```

### 9.2 — OTA Hotfix (Fastest Path)

If the fix is JS/Dart-only, OTA is the fastest path — bypasses store review entirely:

```bash
# React Native / Expo
git checkout -b hotfix/crash-fix
# ... apply fix, test locally ...
eas update --branch production --message "Hotfix: crash on profile load"
# Live in minutes, no store review needed

# Flutter / Shorebird
shorebird patch android --release-version 1.2.4
shorebird patch ios --release-version 1.2.4
```

### 9.3 — Apple Expedited Review

If the fix requires native changes (full store release needed):

1. Submit the build normally through App Store Connect
2. Go to **Contact Us** in App Store Connect
3. Select **App Review** → **Request Expedited Review**
4. Explain the critical bug clearly and concisely
5. Apple typically responds within 24 hours (often faster)

Expedited reviews are a limited resource. Use only for genuine emergencies — crashes, security issues, or legal compliance.

### 9.4 — Hotfix Version Numbering

```
Production version:  1.2.4
Hotfix version:      1.2.5  (bump patch only)
Build number:        43     (increment from 42)
Git tag:             v1.2.5
Branch:              hotfix/1.2.5
```

Never reuse a version number. Even if you "replace" a build in TestFlight or internal track, the build number must increment.

---

## Phase 10: CI/CD Automation

### 10.1 — Automated Release Pipeline (GitHub Actions Example)

```yaml
# .github/workflows/mobile-release.yml
name: Mobile Release
on:
  push:
    tags: ['v*']

jobs:
  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --platform ios --profile production --non-interactive

  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --platform android --profile production --non-interactive

  submit:
    needs: [build-ios, build-android]
    runs-on: ubuntu-latest
    steps:
      - run: eas submit --platform all --profile production --non-interactive
```

### 10.2 — Automated OTA on Merge to Main

```yaml
# .github/workflows/ota-update.yml
name: OTA Update
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '!src/**/native/**'  # skip if native code changed

jobs:
  ota:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas update --branch production --message "${{ github.event.head_commit.message }}"
```

---

## Tips for Best Results

- **Test the store submission flow before your v1.0 launch** — submit a minimal build early to flush out signing, metadata, and review issues. First submissions take longer.
- **Keep a "store review notes" template** with demo credentials, feature explanations, and test instructions. Reviewers are humans — help them understand your app.
- **Automate version bumping** in CI. Manual version management always leads to forgotten build number increments and rejected uploads.
- **Monitor your signing certificate expiry dates** — set calendar reminders 30 days before expiry. An expired cert on release day is a preventable disaster.
- **Keep your minimum OS version as high as practical** — supporting iOS 14 or Android 8 doubles your test matrix for <5% of users. Check your analytics.
- **Screenshot automation** saves hours — use Fastlane snapshot (iOS) or screengrab (Android) to generate store screenshots across all required device sizes.
- **Always test the upgrade path**, not just fresh installs. Migrations, cached data, and persisted state cause most post-release crashes.
- **OTA updates are your safety net** — configure them before your first release, not after your first production crash. Test the update flow in staging.
- **Back up your Android upload keystore to at least two secure locations** (e.g., 1Password + encrypted S3). If you lose it and haven't enrolled in Play App Signing, your app listing is permanently locked.
- **Read the store review guidelines annually** — both Apple and Google update their policies regularly. What passed review last year might get rejected this year.

---

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,         │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
