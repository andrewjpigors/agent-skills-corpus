---
name: ci-mobile-ads-banner
description: >-
  Add a Content Ignite banner ad to an Android or iOS app. Use this skill when the
  user wants to add, place, or implement a banner ad (an inline, flexibly sized ad)
  using the Content Ignite Mobile SDK / CI Mobile Ads. Covers Android (Jetpack
  Compose and View-based) and iOS (SwiftUI and UIKit). Requires the SDK to already
  be initialised — if not, run ci-mobile-ads-get-started first.
metadata:
  version: 1.0.0
  category: ContentIgnite
---

# Add a Content Ignite banner ad

Banner ads are inline, flexibly sized ads you place anywhere in a layout.

## Prerequisite

The SDK must already be installed and initialised (`CIMobileAds.initialise`). If it
isn't, run the `ci-mobile-ads-get-started` skill first, then return here.

## Step 1 — Get the placement ID

You need a **`placementID`** from Content Ignite for this banner slot. During
development, test ads (enabled at init via `setTestAds`) render without a live
placement. In production, use the real `placementID` — never a Google ad-unit ID.

## Step 2 — Identify platform and UI framework

Detect from the project; ask only if genuinely ambiguous:

- **Android + Jetpack Compose** → [references/android-compose-banner.md](references/android-compose-banner.md)
- **Android + View-based (XML)** → [references/android-view-banner.md](references/android-view-banner.md)
- **iOS + SwiftUI** → [references/ios-swiftui-banner.md](references/ios-swiftui-banner.md)
- **iOS + UIKit** → [references/ios-uikit-banner.md](references/ios-uikit-banner.md)

## Step 3 — Consider the placement

Note where the banner goes (bottom bar, inline in a feed, inside a scroll view). The
banner sizes to the space you give it via the layout/modifier/frame — so give it a
sensible width and height in the container it lives in.

## Step 4 — Follow the reference and wire events (optional)

Each reference shows how to create the banner, size it, pass `pageUrl`/`targeting`,
and — optionally — respond to the four events: `bannerLoaded`, `bannerLoadFailed`,
`bannerClicked`, `bannerImpression`.

## Step 5 — Finish

- Confirm the banner renders (a Google test creative if `setTestAds` is on).
- Remind the user to use their real Content Ignite `placementID` and turn test ads off
  for production.

## Optional — fallback to an existing ad implementation

Every banner API accepts a `publisher` fallback (a Compose slot / `() -> View` /
SwiftUI `@ViewBuilder` / `() -> UIView`). It lets an app that already serves its own
ad for this slot keep doing so while Content Ignite rollout ramps — the fallback rate
is controlled remotely in Fusion. This is mainly relevant during migration; see
`ci-mobile-ads-migrate-from-google`.

## Reference implementations

Each platform reference above links to a complete, working demo app on GitLab. If a
step is ambiguous, open the relevant demo for a full, compiling example in context
rather than guessing — the demos track the latest SDK release.
