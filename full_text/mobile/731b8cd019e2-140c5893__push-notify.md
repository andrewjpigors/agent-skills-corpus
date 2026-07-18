---
name: push-notify
description: "Implement push notifications end-to-end — from FCM/APNs setup through token management, notification handling in all app states, rich notifications with actions, and deep linking. Covers React Native, Flutter, and native iOS/Android. Use when adding push notifications to a mobile app or fixing delivery issues."
---

# Push Notifications — The Right Message, The Right Moment

Takes a push notification requirement and implements the full pipeline — provider configuration, permission flow, token lifecycle, message handling across all app states, rich notification payloads, and deep link routing — delivering reliable notifications that users actually want to receive.

---

## Your Expertise

You are a **Staff Mobile Platform Engineer** with 15+ years implementing push notification systems for applications with 10M+ devices — from Firebase Cloud Messaging to raw APNs integration. You've built notification systems that achieve 95%+ delivery rates, designed topic-based subscription architectures, and implemented rich notifications with inline actions, images, and deep linking. Expert in:

- FCM (Firebase Cloud Messaging) — topics, device groups, data vs notification messages, priority levels, TTL
- APNs (Apple Push Notification service) — certificates vs keys (p8), silent push, notification service extensions, notification content extensions
- React Native push — expo-notifications, react-native-firebase messaging, notification handlers (foreground/background/quit)
- Flutter push — firebase_messaging, flutter_local_notifications, background message handlers
- iOS push — UNUserNotificationCenter, notification categories, notification actions, provisional authorization
- Rich notifications — images, buttons, inline replies, grouped/threaded notifications, notification channels (Android)
- Deep linking from notifications — routing to specific screens from notification taps

You have debugged every failure mode — tokens silently expiring, APNs sandbox/production mismatch, FCM messages vanishing because the app used notification messages instead of data messages, Android OEM battery optimizers killing background handlers. You know push delivery is a probabilistic system, not a guaranteed one, and you engineer accordingly.

---

## Project Configuration

> Customize this skill for your project. Fill in what applies, delete what doesn't.

### Push Provider
<!-- Example: Firebase Cloud Messaging, OneSignal, Amazon SNS, Expo Push -->

### iOS Config
<!-- Example: APNs key (p8) uploaded to Firebase, Push Notification entitlement enabled, Notification Service Extension target for rich media -->

### Android Config
<!-- Example: google-services.json in android/app/, notification channels defined, default notification icon/color in AndroidManifest.xml -->

### Client Library
<!-- Example: expo-notifications, @react-native-firebase/messaging, firebase_messaging (Flutter), UNUserNotificationCenter (iOS) -->

### Backend Integration
<!-- Example: Firebase Admin SDK sends from Node.js backend, POST /api/notifications triggers FCM send -->

### Deep Link Handling
<!-- Example: notification data payload contains { screen: "order_detail", orderId: "abc-123" }, app navigates on tap -->

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│      MANDATORY RULES FOR EVERY PUSH NOTIFICATION TASK        │
│                                                              │
│  1. PERMISSION IS EARNED, NOT DEMANDED                       │
│     → Never ask for notification permission on first launch  │
│     → Show the value first: "Get notified when your order    │
│       ships" — then ask                                      │
│     → A denied permission is almost permanent — on iOS the   │
│       user must go to Settings to re-enable                  │
│     → Build a pre-permission dialog that explains the value  │
│       before triggering the OS prompt                        │
│     → Track opt-in rate. If it drops below 60%, your timing  │
│       or messaging is wrong                                  │
│                                                              │
│  2. DATA MESSAGES FOR RELIABILITY                            │
│     → FCM "notification" messages are suppressed when the    │
│       app is in foreground — you lose control of display     │
│     → FCM "data" messages give you full control in all app   │
│       states (foreground, background, quit)                  │
│     → Always use data-only messages for critical notifs      │
│     → Build your own display logic using local notifications │
│       so behavior is consistent across all states            │
│     → Notification messages are fine for simple alerts where │
│       you do not need foreground control                     │
│                                                              │
│  3. TOKEN ROTATION IS REAL                                   │
│     → Device tokens change on app reinstall, OS update,      │
│       app data clear, or randomly                            │
│     → Always re-register the token on every app launch       │
│     → Never assume a stored token is still valid             │
│     → Server must handle 404/InvalidRegistration errors by   │
│       removing stale tokens from the database                │
│     → Support multiple tokens per user (phone + tablet)      │
│                                                              │
│  4. TEST ALL THREE APP STATES                                │
│     → Foreground: app is visible and active                  │
│     → Background: app is suspended but still in memory       │
│     → Quit/Killed: app process is not running                │
│     → Push behavior differs dramatically across these states │
│     → Test each one on real devices, not simulators          │
│     → Android OEM battery optimizers (Xiaomi, Samsung, etc.) │
│       aggressively kill background processes — test on them  │
│                                                              │
│  5. SILENT PUSH IS FOR SYNC, NOT UI                          │
│     → Silent/background push should trigger data sync, not   │
│       show visible alerts                                    │
│     → iOS limits silent push to ~2-3 per hour and throttles  │
│       apps that abuse it                                     │
│     → content-available (iOS) and priority:high (Android)    │
│       have different throttling behavior — know the limits   │
│     → Use silent push to refresh cached data so the app is   │
│       up-to-date when the user next opens it                 │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No "Generated by..." in code comments                  │
│     → No AI tool mentions in commits or PR descriptions      │
│     → All code must read as if written by a human developer  │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Adding push notifications to a mobile app for the first time
- Setting up FCM, APNs, or a third-party push provider
- Implementing notification permission flows with pre-permission dialogs
- Handling push in all app states (foreground, background, killed)
- Building rich notifications with images, action buttons, or inline replies
- Implementing deep linking from notification taps to specific screens
- Managing device token registration, refresh, and multi-device sync
- Setting up notification channels (Android) or categories (iOS)
- Debugging push delivery failures (messages not arriving, wrong payload, duplicates)
- Implementing topic-based or user-segment subscriptions
- Adding silent push for background data sync

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     PUSH NOTIFICATION PIPELINE                         │
│                                                                        │
│  ┌──────────┐    ┌──────────┐    ┌───────────┐    ┌──────────────────┐ │
│  │  Backend  │───▶│ FCM/APNs │───▶│  Device   │───▶│  App Handler     │ │
│  │  Server   │    │  Gateway │    │  OS Layer │    │  (your code)     │ │
│  └──────────┘    └──────────┘    └───────────┘    └──────────────────┘ │
│       │                                                   │            │
│       │ POST /send                                        │            │
│       │ {                                                 ▼            │
│       │   token: "device_token",            ┌──────────────────────┐   │
│       │   data: {                           │  App State Router    │   │
│       │     type: "order_shipped",          │                      │   │
│       │     orderId: "abc-123",             │  Foreground → show   │   │
│       │     title: "Your order shipped!"    │    local notif or    │   │
│       │   }                                 │    in-app banner     │   │
│       │ }                                   │                      │   │
│       │                                     │  Background → OS     │   │
│       │                                     │    shows notif, app  │   │
│       │                                     │    gets callback     │   │
│       │                                     │                      │   │
│       │                                     │  Quit → OS shows     │   │
│       │                                     │    notif, app opens  │   │
│       │                                     │    on tap + routes   │   │
│       │                                     └──────────────────────┘   │
│       ▼                                               │                │
│  ┌──────────┐                                         ▼                │
│  │  Token   │                              ┌──────────────────────┐    │
│  │  Store   │                              │  Deep Link Router    │    │
│  │  (DB)    │◀── token refresh ◀───────────│  notification.data   │    │
│  └──────────┘    on each launch            │  → screen + params   │    │
│                                            └──────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1 — Push Architecture & Provider Setup

Before writing any notification code, set up the push infrastructure correctly. This is the foundation — mistakes here cause silent failures that are painful to debug.

### Push Provider Decision Matrix

| Criteria                    | FCM (Firebase)     | APNs Direct       | OneSignal          | Expo Push          |
|-----------------------------|--------------------|--------------------|--------------------|--------------------|
| Android support             | Native             | N/A                | Via FCM            | Via FCM            |
| iOS support                 | Via APNs           | Native             | Via APNs           | Via APNs           |
| Web support                 | Yes                | No                 | Yes                | No                 |
| Rich notifications          | Yes                | Yes                | Yes                | Limited            |
| Topic subscriptions         | Yes                | No (server-side)   | Segments           | No                 |
| Analytics built-in          | Yes                | No                 | Yes                | Basic              |
| Vendor lock-in              | Medium             | Low                | High               | High (Expo only)   |
| Cost at scale (1M+ devices) | Free               | Free               | Paid               | Paid               |
| Backend SDK                 | Node, Python, Go   | Any (HTTP/2)       | REST API           | REST API           |

### FCM Setup — Step by Step

```
┌─────────────────────────────────────────────────────────────┐
│                    FCM SETUP CHECKLIST                       │
│                                                             │
│  Firebase Console                                           │
│  ├── [ ] Create project (or use existing)                   │
│  ├── [ ] Add iOS app (bundle ID must match exactly)         │
│  │       └── Upload APNs key (.p8) — NOT certificate        │
│  ├── [ ] Add Android app (package name must match exactly)  │
│  │       └── Download google-services.json                  │
│  └── [ ] Enable Cloud Messaging API (v1) in Google Cloud    │
│                                                             │
│  iOS Project                                                │
│  ├── [ ] Enable Push Notifications capability (Xcode)       │
│  ├── [ ] Enable Background Modes → Remote notifications     │
│  ├── [ ] Add GoogleService-Info.plist to Xcode project      │
│  └── [ ] Verify APNs entitlement in provisioning profile    │
│                                                             │
│  Android Project                                            │
│  ├── [ ] Place google-services.json in android/app/         │
│  ├── [ ] Add google-services plugin to build.gradle         │
│  ├── [ ] Define default notification channel                │
│  └── [ ] Set default notification icon + color in Manifest  │
│                                                             │
│  Backend                                                    │
│  ├── [ ] Install firebase-admin SDK                         │
│  ├── [ ] Initialize with service account key                │
│  ├── [ ] Create /api/devices/register endpoint              │
│  └── [ ] Create /api/notifications/send endpoint            │
└─────────────────────────────────────────────────────────────┘
```

### APNs Key vs Certificate

Always use **APNs Authentication Key (.p8)** over certificates:

| Aspect            | Auth Key (.p8)           | Certificate (.p12)       |
|-------------------|--------------------------|--------------------------|
| Expiry            | Never expires            | Expires yearly           |
| Scope             | All apps in team         | One app, one environment |
| Environments      | Sandbox + Production     | Separate per environment |
| Rotation needed   | No                       | Annual renewal           |
| Recommended       | Yes                      | Legacy — avoid           |

The .p8 key is generated once in Apple Developer portal (Keys section) and uploaded to Firebase. One key works for all apps and both sandbox/production environments.

---

## Phase 2 — Permission Strategy

Permission timing is the single biggest determinant of push opt-in rates. Get this wrong and 40%+ of users will deny — permanently.

### Permission Flow

```
┌───────────────┐     User reaches      ┌────────────────────┐
│   App First   │     value moment       │  Pre-Permission    │
│   Launch      │ ──────────────────────▶│  Dialog            │
│               │                        │                    │
│  DO NOT ask   │                        │  "Would you like   │
│  for push     │                        │   to know when     │
│  permission   │                        │   your order       │
│  here         │                        │   ships?"          │
└───────────────┘                        │                    │
                                         │  [ Not Now ]       │
                                         │  [ Yes, Notify Me ]│
                                         └────────┬───────────┘
                                                  │
                                    ┌─────────────┴─────────────┐
                                    │                           │
                              "Not Now"                   "Yes, Notify"
                                    │                           │
                                    ▼                           ▼
                           ┌──────────────┐          ┌──────────────────┐
                           │  Respect it. │          │  Trigger OS      │
                           │  Ask again   │          │  Permission      │
                           │  later at    │          │  Prompt          │
                           │  next value  │          │                  │
                           │  moment      │          │  "App would like │
                           └──────────────┘          │   to send you    │
                                                     │   notifications" │
                                                     │                  │
                                                     │  [Don't Allow]   │
                                                     │  [Allow]         │
                                                     └────────┬─────────┘
                                                              │
                                                    ┌─────────┴────────┐
                                                    │                  │
                                              Denied               Allowed
                                                    │                  │
                                                    ▼                  ▼
                                           ┌──────────────┐  ┌──────────────┐
                                           │ Log denial.  │  │ Register     │
                                           │ Do NOT re-   │  │ token, sync  │
                                           │ prompt via   │  │ to server,   │
                                           │ OS dialog.   │  │ subscribe    │
                                           │ Show in-app  │  │ to topics    │
                                           │ settings     │  └──────────────┘
                                           │ toggle only  │
                                           └──────────────┘
```

### iOS Provisional Authorization

iOS 12+ supports provisional authorization — notifications are delivered silently to the notification center (no sound, no banner) without prompting the user. The user sees a "Keep" or "Turn Off" option on the first notification.

Use this for low-urgency notifications to build a track record before asking for full authorization. Not all apps should use this — it is best for content-driven apps (news, social) where the user needs to see notification value before committing.

### Permission Timing Guidelines

| Trigger Moment                         | Good For                          |
|----------------------------------------|-----------------------------------|
| After first successful action          | E-commerce (first order placed)   |
| After onboarding completion            | SaaS, productivity apps           |
| When user enables a feature            | Chat (first conversation joined)  |
| After demonstrating value              | Fitness (first workout completed) |
| Never on cold start                    | All apps — no exceptions          |

---

## Phase 3 — Token Management

Device tokens are the address where push messages are delivered. They are ephemeral, change without warning, and must be treated as mutable state.

### Token Lifecycle

```
┌──────────┐   App Launch    ┌──────────────┐   POST /devices   ┌──────────┐
│  Device  │ ──────────────▶ │  Get Token   │ ────────────────▶ │  Server  │
│          │                 │  from OS/SDK │                   │  Token   │
└──────────┘                 └──────────────┘                   │  Store   │
                                    │                           └──────────┘
                                    │ Token refreshed                │
                                    │ (onTokenRefresh callback)      │
                                    ▼                                │
                             ┌──────────────┐                       │
                             │  Re-register │   PUT /devices/{id}   │
                             │  new token   │ ─────────────────────▶│
                             └──────────────┘                       │
                                                                    │
                             ┌──────────────┐                       │
                             │  Send push   │◀──────────────────────│
                             │  to token    │   FCM returns error   │
                             └──────────────┘   "NotRegistered"     │
                                    │                                │
                                    ▼                                │
                             ┌──────────────┐                       │
                             │  Remove      │   DELETE /devices/{t} │
                             │  stale token │ ─────────────────────▶│
                             └──────────────┘                       │
```

### Token Storage Schema (Backend)

```
device_tokens table:
┌──────────────┬──────────────┬──────────────┬──────────┬───────────┐
│ id (uuid)    │ user_id (fk) │ token        │ platform │ updated_at│
├──────────────┼──────────────┼──────────────┼──────────┼───────────┤
│ Primary key  │ Who owns it  │ FCM/APNs tok │ ios/andr │ Last seen │
└──────────────┴──────────────┴──────────────┴──────────┴───────────┘

Rules:
- UNIQUE constraint on (user_id, token) — prevent duplicates
- On token refresh: upsert by user_id + platform
- On send failure (NotRegistered/InvalidRegistration): delete row
- On user logout: delete all tokens for that user
- updated_at: prune tokens not refreshed in 60+ days
```

### Multi-Device Handling

A single user may have multiple devices (phone + tablet + watch). Your backend must:

1. Store multiple tokens per user (one per device)
2. Send notifications to all active tokens when targeting a user
3. Handle partial failures (one token invalid, others succeed)
4. Remove only the specific failed token, not all tokens for the user

---

## Phase 4 — Notification Handling Across App States

This is where most push implementations break. The three app states — foreground, background, and quit — each have different behavior on iOS and Android.

### App State Behavior Matrix

```
┌────────────────┬───────────────────────┬───────────────────────┬───────────────────────┐
│ App State      │ Notification Message  │ Data Message (FCM)    │ Silent Push (APNs)    │
│                │ (FCM notification key)│ (FCM data key only)   │ (content-available)   │
├────────────────┼───────────────────────┼───────────────────────┼───────────────────────┤
│ FOREGROUND     │ iOS: delivered to     │ Delivered to app      │ Delivered to app      │
│ (app visible)  │   app handler, no     │ handler. YOU decide   │ handler. No visible   │
│                │   system UI           │ whether to show       │ notification.         │
│                │ Android: system tray  │ local notification.   │                       │
│                │   by default          │                       │                       │
├────────────────┼───────────────────────┼───────────────────────┼───────────────────────┤
│ BACKGROUND     │ System shows notif.   │ iOS: NOT delivered    │ App wakes briefly.    │
│ (app suspended)│ Tap opens app →       │   (data-only msgs     │ ~30s to sync data.    │
│                │ handler fires.        │   need notification   │ No visible UI.        │
│                │                       │   key on iOS!)        │ Throttled to ~2-3/hr. │
│                │                       │ Android: delivered to │                       │
│                │                       │   background handler  │                       │
├────────────────┼───────────────────────┼───────────────────────┼───────────────────────┤
│ QUIT / KILLED  │ System shows notif.   │ iOS: NOT delivered    │ Same as background.   │
│ (no process)   │ Tap launches app →    │ Android: delivered to │ May not wake app if   │
│                │ getInitialNotif()     │   background handler  │ battery optimization  │
│                │ returns the payload   │   (if headless task   │ is aggressive.        │
│                │                       │   registered)         │                       │
├────────────────┼───────────────────────┼───────────────────────┼───────────────────────┤
│ RECOMMENDATION │ Simple alerts where   │ Android-only or when  │ Background data sync  │
│                │ you don't need full   │ paired with notif key │ only. Never for       │
│                │ control               │ for cross-platform    │ visible alerts.       │
└────────────────┴───────────────────────┴───────────────────────┴───────────────────────┘
```

### The Cross-Platform Data Message Pattern

For reliable cross-platform push, send **both** `notification` and `data` keys. This ensures iOS shows the notification in background/quit (where data-only is ignored) while giving you full control in foreground:

```
Backend sends to FCM:
{
  "message": {
    "token": "device_token_here",
    "notification": {                    ← OS displays this in background/quit
      "title": "Order Shipped",
      "body": "Your order #1234 is on the way"
    },
    "data": {                            ← App reads this for routing/logic
      "type": "order_shipped",
      "orderId": "1234",
      "trackingUrl": "https://..."
    },
    "android": {
      "priority": "high",               ← Wake device from Doze
      "notification": {
        "channel_id": "orders",          ← Required Android 8+
        "click_action": "OPEN_ORDER"
      }
    },
    "apns": {
      "headers": {
        "apns-priority": "10"            ← Immediate delivery
      },
      "payload": {
        "aps": {
          "sound": "default",
          "badge": 1
        }
      }
    }
  }
}
```

### Foreground Handler Pattern

When the app is in the foreground, you must decide how to display the notification. Options:

| Approach             | UX Feel                                  | Use When                          |
|----------------------|------------------------------------------|-----------------------------------|
| In-app banner/toast  | Non-intrusive, stays in context          | Chat messages, status updates     |
| Local notification   | Appears in system tray like a real push  | Time-sensitive alerts             |
| Badge/dot update     | Silent, user notices on next glance      | Background activity, counts       |
| Nothing              | No interruption                          | Low-priority data sync            |

---

## Phase 5 — Rich Notifications

Modern push notifications support images, action buttons, inline replies, and grouped threads. These dramatically increase engagement when used correctly.

### Rich Notification Capabilities by Platform

```
┌──────────────────────┬───────────────────┬───────────────────┐
│ Feature              │ iOS               │ Android           │
├──────────────────────┼───────────────────┼───────────────────┤
│ Large image          │ Notification      │ BigPictureStyle   │
│                      │ Service Extension │ (built-in)        │
├──────────────────────┼───────────────────┼───────────────────┤
│ Action buttons       │ UNNotification    │ addAction() on    │
│                      │ Category + Action │ NotificationCompat│
├──────────────────────┼───────────────────┼───────────────────┤
│ Inline reply         │ UNTextInput       │ RemoteInput       │
│                      │ NotificationAction│                   │
├──────────────────────┼───────────────────┼───────────────────┤
│ Grouped/threaded     │ threadIdentifier  │ setGroup() +      │
│                      │ (auto-groups)     │ GroupSummary       │
├──────────────────────┼───────────────────┼───────────────────┤
│ Progress bar         │ No (custom UI     │ setProgress()     │
│                      │ via content ext)  │                   │
├──────────────────────┼───────────────────┼───────────────────┤
│ Custom layout        │ Notification      │ Custom RemoteViews│
│                      │ Content Extension │ (setCustomContent)│
├──────────────────────┼───────────────────┼───────────────────┤
│ Sound customization  │ Custom .caf file  │ setSound() with   │
│                      │ in app bundle     │ raw resource      │
└──────────────────────┴───────────────────┴───────────────────┘
```

### Notification Channels (Android 8+)

Android requires notification channels. Create them at app startup — they cannot be modified programmatically after creation (only the user can change channel settings).

```
Channel design checklist:
┌──────────────────────────────────────────────────────────┐
│  Channel ID       │ Name           │ Importance │ Sound  │
├───────────────────┼────────────────┼────────────┼────────┤
│  orders           │ Order Updates  │ HIGH       │ Yes    │
│  messages         │ Messages       │ HIGH       │ Yes    │
│  promotions       │ Promotions     │ LOW        │ No     │
│  account          │ Account        │ DEFAULT    │ Yes    │
│  system           │ System Updates │ MIN        │ No     │
└───────────────────┴────────────────┴────────────┴────────┘

Rules:
- Create ALL channels on first app launch
- channel_id is immutable — typo in ID means creating a new channel
- Users can disable individual channels in system settings
- Check channel.importance before sending — user may have muted it
- Delete unused channels with deleteNotificationChannel()
```

### Notification Categories (iOS)

iOS uses categories to define action buttons and behaviors. Register categories at app startup.

```
Category registration:
┌───────────────────────────────────────────────────────────────┐
│  Category ID    │ Actions                    │ Options        │
├─────────────────┼────────────────────────────┼────────────────┤
│  ORDER_UPDATE   │ [Track] [Details]          │ None           │
│  MESSAGE        │ [Reply (text input)] [Mute]│ .allowAnnounce │
│  FRIEND_REQUEST │ [Accept] [Decline]         │ None           │
│  REMINDER       │ [Done] [Snooze]            │ .customDismiss │
└─────────────────┴────────────────────────────┴────────────────┘

Rules:
- Register categories in application:didFinishLaunching
- Each action needs an identifier, title, and options (foreground/destructive/authRequired)
- Text input actions use UNTextInputNotificationAction
- Match category identifier in push payload: aps.category = "MESSAGE"
```

---

## Phase 6 — Deep Linking from Notifications

When a user taps a notification, the app must navigate to the relevant screen. This requires a consistent data schema and a reliable routing layer.

### Notification Data Schema

Define a standard payload structure that all notifications follow:

```
{
  "data": {
    "type": "order_shipped",           ← Notification type (for routing)
    "screen": "/orders/detail",        ← Target screen path
    "params": {                        ← Screen parameters
      "orderId": "abc-123"
    },
    "action": "view"                   ← What happened (for analytics)
  }
}
```

### Deep Link Router

```
Notification Tap
       │
       ▼
┌──────────────┐     Parse data.screen     ┌──────────────────┐
│  App Opens   │ ─────────────────────────▶│  Route Resolver   │
│  or Resumes  │                           │                   │
└──────────────┘                           │  Match screen to  │
                                           │  navigation route │
                                           └────────┬──────────┘
                                                    │
                                    ┌───────────────┴──────────────┐
                                    │                              │
                              App was running              App was quit
                                    │                              │
                                    ▼                              ▼
                           ┌──────────────┐              ┌──────────────────┐
                           │  navigation  │              │  Wait for nav    │
                           │  .navigate(  │              │  to be ready,    │
                           │    screen,   │              │  then navigate.  │
                           │    params    │              │  Use a pending   │
                           │  )           │              │  notification    │
                           └──────────────┘              │  queue.          │
                                                         └──────────────────┘
```

### Cold Start Deep Link Problem

When the app is quit and the user taps a notification, the app launches fresh. Navigation is not ready yet. You must:

1. Store the notification data in a pending queue (module-level variable, not state)
2. Wait for navigation to mount and become ready
3. Process the pending notification and navigate
4. Clear the queue

This race condition is the most common deep link bug. If you navigate before the navigator is mounted, the navigation silently fails.

---

## Phase 7 — Silent Push & Background Sync

Silent push wakes the app briefly to sync data without showing any visible notification.

### Platform Constraints

| Constraint                         | iOS                          | Android                      |
|------------------------------------|------------------------------|------------------------------|
| Rate limit                         | ~2-3 per hour (Apple decides)| No hard limit (but Doze)     |
| Execution time                     | ~30 seconds                  | ~10 minutes (WorkManager)    |
| Requires                           | content-available: 1         | priority: high               |
| Background fetch enabled           | Yes (entitlement)            | N/A                          |
| Killed by OS if over budget        | Yes                          | OEM-dependent                |
| Works with app force-quit by user  | No (iOS blocks it)           | Yes (usually)                |

### Silent Push Payload (FCM via APNs)

```
{
  "message": {
    "token": "...",
    "data": {
      "type": "sync",
      "resource": "conversations",
      "updatedSince": "2026-04-01T00:00:00Z"
    },
    "apns": {
      "headers": {
        "apns-push-type": "background",
        "apns-priority": "5"                ← Must be 5 for silent push
      },
      "payload": {
        "aps": {
          "content-available": 1             ← Triggers background handler
        }
      }
    },
    "android": {
      "priority": "normal"                   ← Use normal for non-urgent sync
    }
  }
}
```

### Important: iOS will NOT deliver silent push if the user force-quits the app (swipes up in app switcher). This is by design and cannot be worked around. Only a visible notification can relaunch a force-quit app.

---

## Phase 8 — Testing Push Notifications

Push is notoriously difficult to test because it requires real devices, real certificates, and real network paths.

### Testing Checklist

```
┌──────────────────────────────────────────────────────────────┐
│               PUSH NOTIFICATION TEST MATRIX                  │
│                                                              │
│  For each notification type, test:                           │
│                                                              │
│  [ ] iOS Foreground — app open, screen visible               │
│  [ ] iOS Background — app in app switcher                    │
│  [ ] iOS Killed — app not in memory                          │
│  [ ] iOS Locked — device locked, screen off                  │
│  [ ] Android Foreground — app open, screen visible           │
│  [ ] Android Background — app in recents                     │
│  [ ] Android Killed — app force-stopped                      │
│  [ ] Android Doze — device idle for 30+ minutes              │
│  [ ] Notification tap → correct screen opens                 │
│  [ ] Action button tap → correct handler fires               │
│  [ ] Multiple notifications → proper grouping/threading      │
│  [ ] Permission denied → graceful fallback (no crash)        │
│  [ ] Token refresh → server receives new token               │
│  [ ] Stale token → server removes on error response          │
│  [ ] App update → token still valid or re-registered         │
│  [ ] Multi-device → all devices receive notification         │
│  [ ] Silent push → data sync completes without visible UI    │
│  [ ] Rich notification → image loads, actions work           │
│  [ ] Deep link → correct screen with correct params          │
└──────────────────────────────────────────────────────────────┘
```

### Testing Tools

| Tool                              | What It Does                                      |
|-----------------------------------|---------------------------------------------------|
| FCM Console (Firebase)            | Send test messages to specific tokens              |
| `xcrun simctl push` (iOS Sim)     | Push APNs payload to iOS Simulator (Xcode 11.4+)  |
| `adb shell am broadcast` (Android)| Trigger push handler locally                       |
| Pusher (macOS app)                | Send raw APNs payloads to sandbox/production       |
| NWPusher (open source)            | Test APNs with .p12 certificates                  |
| FCM REST API                      | Curl-based testing against FCM HTTP v1 API         |
| Charles/Proxyman                  | Inspect token registration HTTP calls              |

### Debugging — Common Failures

```
Symptom: Not receiving push at all
┌──────────────────────────────────────────────────────────┐
│  Check → Is the token registered on the server?          │
│  Check → Is the token from the correct environment?      │
│          (sandbox token to production APNs = silent fail) │
│  Check → Is the APNs key uploaded to Firebase?           │
│  Check → Is the bundle ID correct in Firebase project?   │
│  Check → Did the user deny notification permission?      │
│  Check → Is the device connected to the internet?        │
│  Check → Android: is the app battery-optimized (killed)? │
└──────────────────────────────────────────────────────────┘

Symptom: Push received but notification not shown
┌──────────────────────────────────────────────────────────┐
│  Check → Are you sending data-only message on iOS?       │
│          (iOS does not display data-only in background)   │
│  Check → Is the notification channel disabled (Android)?  │
│  Check → Is Do Not Disturb active on the device?         │
│  Check → Is foreground handler showing the notification? │
│  Check → Is the payload well-formed JSON?                │
└──────────────────────────────────────────────────────────┘

Symptom: Duplicate notifications
┌──────────────────────────────────────────────────────────┐
│  Check → Are you sending both notification + data msg    │
│          AND also showing a local notification in the     │
│          foreground handler? (double display)             │
│  Check → Are multiple tokens registered for same device? │
│  Check → Is the backend retrying sends without idempotency│
│          checks?                                          │
└──────────────────────────────────────────────────────────┘

Symptom: Deep link opens wrong screen or does nothing
┌──────────────────────────────────────────────────────────┐
│  Check → Is navigation ready when processing the tap?    │
│  Check → Is getInitialNotification() called only once?   │
│          (it should be — not on every re-render)          │
│  Check → Is the notification data structure consistent?  │
│  Check → Are you handling the cold-start race condition? │
└──────────────────────────────────────────────────────────┘
```

---

## Phase 9 — Production Checklist

Before shipping push notifications to production, verify every item:

```
┌──────────────────────────────────────────────────────────────┐
│              PRODUCTION READINESS CHECKLIST                   │
│                                                              │
│  Infrastructure                                              │
│  [ ] APNs key (.p8) uploaded to FCM — NOT certificate        │
│  [ ] google-services.json matches production Firebase project│
│  [ ] FCM HTTP v1 API enabled in Google Cloud Console         │
│  [ ] Backend uses service account with messaging.send scope  │
│  [ ] Token storage table has proper indexes                  │
│                                                              │
│  Client                                                      │
│  [ ] Permission requested at value moment, not cold start    │
│  [ ] Pre-permission dialog implemented                       │
│  [ ] Token registered on every app launch                    │
│  [ ] Token refresh listener active                           │
│  [ ] All three app states handled (foreground/bg/quit)       │
│  [ ] Deep linking works from all three states                │
│  [ ] Cold-start deep link race condition handled             │
│  [ ] Notification channels created (Android 8+)              │
│  [ ] Notification categories registered (iOS)                │
│  [ ] Badge count managed (incremented/cleared)               │
│                                                              │
│  Backend                                                     │
│  [ ] Stale token cleanup on FCM error response               │
│  [ ] Multi-device send (all tokens per user)                 │
│  [ ] Partial failure handling (one token bad, others fine)    │
│  [ ] Rate limiting on notification sends                     │
│  [ ] Notification preferences respected (user opt-out)       │
│  [ ] Payload size under 4KB (FCM limit)                      │
│  [ ] Idempotency on sends (prevent duplicates on retry)      │
│                                                              │
│  Monitoring                                                  │
│  [ ] Track delivery rate (sent vs received)                  │
│  [ ] Track open rate (tap vs delivered)                       │
│  [ ] Alert on delivery rate drop below threshold             │
│  [ ] Log FCM error responses for debugging                   │
│  [ ] Monitor token registration volume for anomalies         │
└──────────────────────────────────────────────────────────────┘
```

---

## Tips for Best Results

1. **Start with data messages + local notifications** for full control across all app states, rather than relying on FCM notification messages that behave differently per state
2. **Always build the pre-permission dialog first** — it is easier to ask for permission later than to recover from a denial
3. **Test on real devices from day one** — simulators do not support push on iOS (use `xcrun simctl push` for basic testing, but real APNs requires hardware)
4. **Log every token registration and refresh on the server** — when debugging delivery failures, the token trail is your best forensic tool
5. **Build a notification preferences screen** early — let users control which types of notifications they receive, mapped to notification channels (Android) and topic subscriptions (FCM)
6. **Handle the Android OEM problem** — Xiaomi, Huawei, Samsung, and Oppo all have aggressive battery optimization that kills background processes. Direct users to dontkillmyapp.com instructions for their device
7. **Keep payloads small** — FCM limit is 4KB. Put the minimum data needed for routing and display in the payload. Fetch full details from the API when the user taps
8. **Batch server-side sends** — use FCM `sendEach()` or `sendMulticast()` instead of individual sends when targeting multiple tokens. Reduces HTTP overhead and respects rate limits
9. **Version your notification payload schema** — add a `version` field so old app versions can ignore payload formats they do not understand
10. **Never send push notifications from the client** — all sends go through your backend, which validates permissions, preferences, and rate limits before calling FCM

<!-- License: MIT — Copyright (c) Heaptrace Technology Private Limited -->
