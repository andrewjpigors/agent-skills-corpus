---
name: ci-mobile-ads-interstitial
description: >-
  Add a Content Ignite interstitial (full-screen) ad to an Android or iOS app. Use
  this skill when the user wants to add, load, or show an interstitial ad — a
  full-screen ad shown at a natural transition point — using the Content Ignite
  Mobile SDK / CI Mobile Ads. Covers Android and iOS (SwiftUI and UIKit). Requires
  the SDK to already be initialised — if not, run ci-mobile-ads-get-started first.
metadata:
  version: 1.0.0
  category: ContentIgnite
---

# Add a Content Ignite interstitial ad

Interstitial ads are full-screen ads shown at natural transition points (e.g. between
levels, after finishing an article). They are loaded ahead of time, then shown.

## Prerequisite

The SDK must already be installed and initialised (`CIMobileAds.initialise`). If it
isn't, run the `ci-mobile-ads-get-started` skill first, then return here.

## Step 1 — Get the placement ID

You need a **`placementID`** from Content Ignite for this interstitial. During
development, test ads (enabled at init via `setTestAds`) render without a live
placement. Never use a Google ad-unit ID.

## Step 2 — Identify the platform

Detect from the project; ask only if genuinely ambiguous:

- **Android** (Compose or View-based — the API is the same) → [references/android-interstitial.md](references/android-interstitial.md)
- **iOS + SwiftUI** → [references/ios-swiftui-interstitial.md](references/ios-swiftui-interstitial.md)
- **iOS + UIKit** → [references/ios-uikit-interstitial.md](references/ios-uikit-interstitial.md)

## Step 3 — Follow the reference

The lifecycle is always: **create → load → show**, and you observe events via
`CIInterstitialEventListener`:

- `interstitialLoaded` — ready to show
- `interstitialLoadFailed` — did not load (handle gracefully; don't block the user)
- `interstitialDismissed` — the user closed the ad (resume your flow here)

Key platform difference: **Android** `show(activity)` takes the current `Activity`;
**iOS** `show()` takes no argument.

## Step 4 — Finish

- Load the ad in advance of the transition, and only `show()` once loaded.
- Continue the app flow from `interstitialDismissed`.
- Remind the user to use their real `placementID` and disable test ads for production.

## Optional — fallback to an existing ad implementation

The interstitial API accepts an optional `publisher` fallback lambda, letting an app
that already serves its own interstitial keep doing so while Content Ignite rollout
ramps (rate controlled remotely in Fusion). Mainly relevant during migration — see
`ci-mobile-ads-migrate-from-google`.

## Reference implementations

Each platform reference above links to a complete, working demo app on GitLab. If a
step is ambiguous, open the relevant demo for a full, compiling example in context
rather than guessing — the demos track the latest SDK release.
