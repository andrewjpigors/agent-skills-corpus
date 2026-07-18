---
name: ci-mobile-ads-app-open
description: >-
  Add Content Ignite App Open ads to an Android or iOS app. Use this skill when the
  user wants to add, enable, or implement App Open ads — full-screen ads shown when
  the app is opened or brought back from the background — using the Content Ignite
  Mobile SDK / CI Mobile Ads. Covers Android (Compose and View-based) and iOS
  (SwiftUI and UIKit), including the cold-start/splash flow and the resume-from-
  background flow. Requires enabling App Open at SDK initialisation.
metadata:
  version: 1.0.0
  category: ContentIgnite
---

# Add Content Ignite App Open ads

App Open ads are full-screen ads shown when the user opens the app or returns to it
from the background. There are two flows, designed to be used together:

1. **Cold start (splash screen)** — while the app loads, request an ad and show it
   before the home screen (raced against a short timeout).
2. **Resume from background** — when the app returns to the foreground, show a
   pre-loaded ad if one is available, otherwise load one for next time.

## Step 1 — Enable App Open at initialisation

App Open ads must be turned on when the SDK is initialised, by adding
`.enableAppOpen("<PLACEMENT-ID>")` (Android) / `.enableAppOpen(placementID: "<PLACEMENT-ID>")`
(iOS) to the `CIMobileAdsConfiguration.Builder`. If the SDK isn't set up yet, run
`ci-mobile-ads-get-started` first and add this builder call.

Note the App Open pattern often moves SDK initialisation to the **splash screen** so
the first ad can be loaded during launch — the references show this.

## Step 2 — Identify platform and UI framework

- **Android + Jetpack Compose** → [references/android-compose-app-open.md](references/android-compose-app-open.md)
- **Android + View-based** → [references/android-view-app-open.md](references/android-view-app-open.md)
- **iOS + SwiftUI** → [references/ios-swiftui-app-open.md](references/ios-swiftui-app-open.md)
- **iOS + UIKit** → [references/ios-uikit-app-open.md](references/ios-uikit-app-open.md)

## Step 3 — Follow the reference

All ads are managed by **`CIAppOpenAdManager`** (a singleton; `CIAppOpenAdManager.shared`
on iOS). Its lifecycle:

- `loadAd()` — request an ad
- `show(activity)` (Android) / `show()` (iOS) — display a loaded ad
- `isAdAvailable()` — is an ad ready to show
- `isShowingAd()` (Android) — is an ad currently on screen
- `state` — a flow/stream of `LOADED` / `LOAD_FAILED` / `DISMISSED`
  (Android `AppOpenState`) or `.loaded` / `.loadFailed` / `.dismissed` (iOS)

## Step 4 — Finish

- Cold start: load with a timeout (~5s); if it doesn't load in time, navigate to home
  and don't block the user.
- Resume: only show when the app is actually returning to foreground and the splash has
  completed, to avoid showing an ad over the wrong screen.
- Remind the user to use their real `placementID` and disable test ads for production.

## Reference implementations

Each platform reference above links to a complete, working demo app on GitLab. If a
step is ambiguous, open the relevant demo for a full, compiling example in context
rather than guessing — the demos track the latest SDK release.
