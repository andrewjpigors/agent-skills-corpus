---
name: ci-mobile-ads-get-started
description: >-
  Install, configure and initialise the Content Ignite Mobile SDK in an Android
  or iOS app. Use this skill when the user wants to get started with, install,
  set up, add, or configure Content Ignite / CI Mobile Ads / the Content Ignite
  Mobile SDK. The SDK embeds and orchestrates Google Mobile Ads (Ad Manager) plus
  Prebid, so it replaces a separate Google Mobile Ads integration — if the app
  already uses the Google Mobile Ads SDK, use ci-mobile-ads-migrate-from-google
  instead.
metadata:
  version: 1.0.0
  category: ContentIgnite
---

# Get started with the Content Ignite Mobile SDK

The Content Ignite Mobile SDK monetises an app by orchestrating **Google Ad Manager**,
**Prebid** header bidding and additional SSPs behind one remotely configurable
interface. It **embeds the Google Mobile Ads SDK** — do not add Google Mobile Ads
separately, and if the app already has it, stop and use the
`ci-mobile-ads-migrate-from-google` skill instead.

## Step 1 — Confirm you have the credentials

The developer must have, from Content Ignite:

- A **`publisherId`** (identifies the publisher in the Fusion platform).
- A **Google Ad Manager app ID** of the form `ca-app-pub-################~##########`.
- One or more **placement IDs** (used later, per ad format).

If any are missing, tell the user to contact their Content Ignite account manager.
Do not invent IDs. For development you can use test ads (Step 4) without real
placement IDs.

## Step 2 — Identify the platform and UI framework

Detect from the project, and ask only if it is genuinely ambiguous:

- **Android** → open [references/android-get-started.md](references/android-get-started.md)
- **iOS** → open [references/ios-get-started.md](references/ios-get-started.md)
  (covers both SwiftUI and UIKit)

## Step 3 — Follow the platform reference

Each reference guide walks through, in order:

1. Prerequisites (min OS / tooling versions).
2. Adding the SDK dependency — **resolve the latest version live** (see below).
3. Providing the Google Ad Manager app ID (Android: in code; iOS: in `Info.plist`).
4. Building `CIMobileAdsConfiguration` and calling `CIMobileAds.initialise(...)`
   **as early as possible** in the app lifecycle, on a background/async context.
5. Verifying the initialisation status.

## Step 4 — Before you finish

- **Enable test ads during development.** Set `.setTestAds(enabled: true)` on the
  configuration builder so you don't generate invalid traffic against live Ad Manager
  inventory. Remove it (or set `false`) for production.
- **Consent first.** If the app serves EEA/UK users it must gather consent through a
  TCF-certified CMP **before** `CIMobileAds.initialise(...)` runs, so a valid TC String
  is in platform storage before the first ad request. See
  [references/android-get-started.md](references/android-get-started.md) /
  [references/ios-get-started.md](references/ios-get-started.md) for the ordering rule.
- **app-ads.txt.** Remind the user to host an `app-ads.txt` on their developer website
  domain (the one on their store listings) with the lines Content Ignite provides.

## Step 5 — Add an ad format

Once initialisation succeeds, point the user to the next skill:

- `ci-mobile-ads-banner` — inline banner ads
- `ci-mobile-ads-interstitial` — full-screen ads at transitions
- `ci-mobile-ads-app-open` — ads on cold start / resume from background

## Rules that apply to every Content Ignite integration

- **Never hard-code an SDK version.** Resolve the latest release at integration time
  from the product's GitLab tags API (the reference files give the exact endpoint) and
  write that into the version catalog / Package pin / Podfile.
- **`googleId` is Android-only.** On Android it is a required builder parameter; on iOS
  the Google Ad Manager app ID goes in `Info.plist` as `GADApplicationIdentifier` and
  is **not** passed to the builder.
- **Do not add or initialise the Google Mobile Ads SDK yourself** — it is pulled in
  transitively and initialised by Content Ignite.
- **Developers never write Google ad-unit IDs.** They pass a Content Ignite
  `placementID`; the real Ad Manager unit is resolved internally.
- **`initialise` is suspending (Android) / async (iOS)** — run it off the main thread /
  in a `Task`, and as early as possible after consent.

## Reference implementations

Each platform reference above links to a complete, working demo app on GitLab. If a
step is ambiguous, open the relevant demo for a full, compiling example in context
rather than guessing — the demos track the latest SDK release.
