---
name: ci-mobile-ads-migrate-from-google
description: >-
  Migrate an Android or iOS app that already uses the Google Mobile Ads SDK
  (AdMob / Ad Manager) onto the Content Ignite Mobile SDK. Use this skill when the
  app already integrates Google Mobile Ads (GADMobileAds / MobileAds.initialize /
  GADApplicationIdentifier / the google-mobile-ads dependency) and the user wants
  to adopt Content Ignite / CI Mobile Ads. The Content Ignite SDK embeds Google
  Mobile Ads, so the separate Google integration must be removed.
metadata:
  version: 1.0.0
  category: ContentIgnite
---

# Migrate from the Google Mobile Ads SDK to Content Ignite

The Content Ignite Mobile SDK **embeds and orchestrates** the Google Mobile Ads SDK
(plus Prebid and other SSPs). An app must not run the Google Mobile Ads SDK
*separately* alongside it — the separate dependency and initialisation must be removed
and replaced with Content Ignite's.

Content Ignite keeps the same Google Ad Manager app ID the app already uses, so you are
re-plumbing initialisation and ad creation, not changing ad accounts.

## Step 1 — Detect the existing Google Mobile Ads integration

Before changing anything, confirm what's there and where. Follow
[references/detect-existing-gma.md](references/detect-existing-gma.md) to find the
dependency, the initialisation call, the app-ID declaration, and every place an ad
view/object is created. Make an inventory — you'll replace each item.

## Step 2 — Migrate per platform

- **Android** → [references/android-migrate.md](references/android-migrate.md)
- **iOS** → [references/ios-migrate.md](references/ios-migrate.md)

At a high level:

1. **Remove** the Google Mobile Ads dependency and its `initialize` call.
2. **Move the app ID.** Android: delete the manifest `APPLICATION_ID` meta-data and
   pass the ID as `googleId` in the Content Ignite config builder. iOS: keep
   `GADApplicationIdentifier` in `Info.plist` — Content Ignite reads it from there.
3. **Install + initialise Content Ignite** — run `ci-mobile-ads-get-started`.
4. **Replace each ad** with the Content Ignite equivalent — run `ci-mobile-ads-banner`,
   `ci-mobile-ads-interstitial`, and/or `ci-mobile-ads-app-open`. Each Google ad unit
   maps to a Content Ignite **`placementID`** (obtained from Content Ignite); you do
   not reuse Google ad-unit IDs in the new code.

## Step 3 — Optional: keep existing ads during rollout (the `publisher` fallback)

Every Content Ignite ad format takes a `publisher` fallback slot (Compose slot /
`() -> View` / SwiftUI `@ViewBuilder` / `() -> UIView`). You can wire the app's
**existing** ad view into that slot for a placement, so it still serves while Content
Ignite ramps up. The fallback rate is controlled remotely in Fusion — a safe way to
migrate gradually rather than switching everything at once. See the per-platform
references for exactly what to pass.

## Step 4 — Verify the migration

- Grep the project again — there should be **no** remaining Google Mobile Ads
  dependency, `initialize`/`start` call, or (Android) manifest `APPLICATION_ID`.
- Build and run with test ads enabled; confirm ads render through Content Ignite.
- Confirm consent (CMP) still runs **before** `CIMobileAds.initialise`.
- Only then switch test ads off and use production `placementID`s.

## Reference implementations

Each platform reference above links to a complete, working demo app on GitLab. If a
step is ambiguous, open the relevant demo for a full, compiling example in context
rather than guessing — the demos track the latest SDK release.
