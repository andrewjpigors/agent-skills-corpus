---
name: macos-ui-ux
description: "macOS visual design, window management, and system layout."
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Macos, Ui, Ux, Design, Reference]
---

# macOS UI/UX Design and Architecture

A comprehensive reference of macOS user interface and user experience — visual design language, window management, system layout, gestures, system apps, and the low-level building blocks beneath the surface. It is knowledge the agent can recall and reason over, not a procedure. It does not assume a live macOS machine; most facts are stable and versioned for easy lookup.

## When to Use

- "How does macOS handle window management?"
- "What's the difference between Mission Control and Stage Manager?"
- "Where does app X store its data?"
- "Explain Aqua / Liquid Glass / Big Sur design."
- "What are traffic lights / Dock / Menu Bar / Control Center?"
- "macOS filesystem layout, ~/Library, .plist files."
- "What keyboard shortcut / trackpad gesture does X?"
- "How does Gatekeeper / SIP / TCC work?"
- "What changed in macOS 15 Sequoia or macOS 26 Tahoe?"
- "What's the path to the system fonts / user caches / keychain?"

## Prerequisites

None. Pure knowledge reference. No install, no credentials, no commands required. The verification section at the end shows what to check on a live macOS if one is available.

## How to Run

Load the skill with `skill_view(name='macos-ui-ux')` and read the relevant section. The body is a reference, not a scripted workflow — pick the section you need.

## Quick Reference

| Topic | Where it lives | Section |
| --- | --- | --- |
| Visual design history | Aqua → Liquid Glass | Design Aesthetic |
| Window management | Mission Control / Stage Manager / Spaces | Window Manager |
| Filesystem layout | `/System`, `/Library`, `/Users` | What Lives Where |
| System apps | `/System/Applications`, `/Applications` | System Apps |
| Gestures and shortcuts | Trackpad, Magic Mouse, keyboard | Input & Gestures |
| Power user | `defaults`, `.plist`, `launchd` | Power User |
| Internals | WindowServer, AppKit, Quartz | Low-Level Internals |
| Recent changes | macOS 15 Sequoia, macOS 26 Tahoe | Recent Releases |

## Procedure

### 1. Design Aesthetic (Visual Language)

#### 1.1 Eras
- **Aqua (2001, Mac OS X 10.0 Cheetah)** — the original glossy, translucent, candy-like look. Translucent blue menu bar, pinstripe window backgrounds.
- **Brushed Metal (2002, 10.2 Jaguar)** — metal-looking apps (Finder, QuickTime, parts of System Preferences at the time). Contested; walked back over time.
- **Pinstripe (2003, 10.3 Panther)** — full-window pinstripe backgrounds, brushed metal retained for some apps.
- **Tiger (2005, 10.4)** — Spotlight, Dashboard, "brushed metal" pruned from most apps.
- **Leopard (2007, 10.5)** — the 3D reflective Dock, refined Aqua, Time Machine, Spaces.
- **iOS-influenced (2011, 10.7 Lion)** — scrollbars hidden by default, Launchpad, Mission Control unified Exposé + Spaces, full-screen apps.
- **Flat redesign (2014, 10.10 Yosemite)** — killed most skeuomorphism. Translucent menu bar, Helvetica Neue → San Francisco font, flatter icons.
- **Dark mode (2018, 10.14 Mojave)** — system-wide dark theme, dynamic desktop wallpapers.
- **Big Sur (2020, 11)** — biggest visual refresh since Yosemite. Rounded squares (macOS 11+ apps), translucent sidebars, the colorful iOS-influenced icon style, redesigned Control Center and Notification Center.
- **Monterey (2021, 12)** — Universal Control, Shortcuts, Focus modes.
- **Ventura (2022, 13)** — System Settings redesign (sidebar-driven, iOS-style), Stage Manager.
- **Sonoma (2023, 14)** — desktop widgets, Game Mode, video screen savers.
- **Sequoia (2024, 15)** — native window tiling, iPhone Mirroring, Passwords app, Math Notes, Apple Intelligence.
- **Tahoe (2025, 26)** — year-based naming, **Liquid Glass** design language inspired by visionOS: translucent, layered, glass-like panels; more depth; more generous corner radii.

#### 1.2 Visual primitives that survive across eras
- **Translucency / vibrancy** — windows and panels let the wallpaper show through a blur. `NSVisualEffectView` (AppKit) / `Material` (SwiftUI) is the underlying primitive.
- **SF Pro** — system font since Yosemite, replaced Helvetica Neue.
- **SF Symbols** — Apple's icon system: thousands of vector glyphs that scale and tint.
- **Rounded rectangles** — every UI element is a rounded rect; corner radius varies by version (larger under Liquid Glass).
- **Shadow / depth** — windows cast subtle shadows; layering conveys z-order.
- **Hit areas** — Apple uses larger invisible hot zones than the visible element (Dock magnification, slider track).
- **Spring-loaded folders** — drag onto a folder and it springs open after a short delay.

#### 1.3 Color and appearance
- System Settings → Appearance: Light / Dark / Auto (Auto introduced in Catalina).
- Accent color (graphite, red, orange, yellow, green, blue, purple, pink, multi-color).
- Highlight color (text selection).
- Sidebar icon size (Small / Medium / Large).
- Tinted windows (Sonoma+) — windows take on the accent color.
- Wallpaper: dynamic, light/dark variants, set per display.

### 2. Window Manager

#### 2.1 The three layers
macOS window management is layered:
- **Quartz Window Server** (`WindowServer` process) — owns the screen, composes all on-screen content, handles events.
- **AppKit** — `NSWindow`, `NSWindowController`. Each window has a level (`normal`, `floating`, `modalPanel`, `mainMenu`, `popUpMenu`, etc.).
- **Mission Control / Stage Manager** — the user-facing layer. Swipe up with 4 fingers (or F3) for Mission Control.

#### 2.2 Traffic lights (window controls)
Top-left of every window. Three buttons:
- Red — close (`Cmd+W` or click).
- Yellow — minimize. Animates the window into the Dock with the **Genie** effect (default) or **Scale** (set in System Settings → Desktop & Dock → Minimize windows using).
- Green — zoom / full-screen. Hold **Option** while clicking to maximize (not full-screen). Full-screen mode (since Lion) sends the app to its own Space.

#### 2.3 Mission Control (F3 / 4-finger swipe up)
- Shows all open windows of the current app (top row) and all open apps (lower rows).
- Shows each **Space** as a thumbnail across the top of the screen.
- Drag a window to a Space thumbnail to move it.
- Drag two windows onto each other to create a Split View.
- Click a Space thumbnail to switch to it.
- "+" button in the upper-right creates a new Space.

#### 2.4 Spaces (virtual desktops)
- Each Space is a full desktop. Apps live on whichever Space they were last in.
- Apps can be **assigned to all Spaces** (System Settings → Desktop & Dock).
- Spaces persist across reboots (with the windows that were in them).

#### 2.5 Split View (10.11+)
- Two apps side-by-side in a full-screen Space.
- Trigger: hold the green button in a window's title bar → drag to one side of the screen → pick a window from the other side.
- Or: in Mission Control, drag one window onto another.

#### 2.6 Stage Manager (macOS 13 Ventura+)
- An alternative to Mission Control. The active app's window is centered; other windows stack as cards on the side.
- Stage Manager lives in its own space, separate from Mission Control Spaces.
- A "Stage" is a saved group of windows.
- Trigger from Control Center, the app's Dock menu, or System Settings.

#### 2.7 Native window tiling (macOS 15 Sequoia+)
- Drag a window to the left or right edge → it snaps to half the screen.
- Drag to a corner → quarter.
- Keyboard: hold **Option**, then arrow keys to tile the focused window.
- System Settings → Desktop & Dock → "Window snapping".

#### 2.8 Window Groups (macOS 15+)
- An app can declare a "Window Group" — the app's windows are tiled together as a unit.
- When you click an app in the Dock, all its windows appear tiled; clicking a single window expands it.

#### 2.9 Full-screen mode
- Green button → app goes full-screen; menu bar auto-hides.
- Swipe with 4 fingers (or 3 on older trackpads) to switch between full-screen apps.
- A full-screen app gets its own Space.

#### 2.10 WindowServer (the engine)
- The system process `WindowServer` (launched by `launchd` at boot).
- Renders every pixel on the screen. Talks to the GPU.
- The login window is also rendered by WindowServer (`loginwindow.app`).
- If WindowServer crashes, the screen goes black; macOS auto-relaunches it.
- `launchctl print system | grep -A 3 WindowServer` to see process state.
- `log show --predicate 'process == "WindowServer"' --last 1h` for recent logs.

#### 2.11 Dock
- The persistent bottom bar (or left/right edge, configurable).
- Holds app icons (favorites), running-app indicators (a dot under the icon), minimized-window thumbnails, the Trash, and a divider between apps and files.
- Magnification: hovering makes icons grow. Enable in System Settings → Desktop & Dock.
- Right-click an icon → Options (Open at Login, Keep in Dock, etc.), Quit, Show in Finder.
- Drag a file onto a Dock icon to open it with that app.
- Drag an app onto a folder in the Dock to spring-open the folder.
- The Dock itself is `Dock.app` at `/System/Applications/Dock.app/Contents/MacOS/Dock`.
- Configure via `defaults read com.apple.dock` and friends.

#### 2.12 Menu Bar (top of screen)
- Always at the top of the main display (configurable to hide).
- Left side: **Apple menu** (About This Mac, System Settings, Sleep, Restart, Recent Items, Force Quit, App Store, Log Out).
- App menus: bold app name → File, Edit, View, Window, Help, plus app-specific menus.
- Right side: status menu extras — Control Center, Spotlight, Siri, Date & Time, Notifications, Battery, Wi-Fi, Bluetooth, Time Machine, and third-party extras (1Password, Dropbox).
- Cmd-drag a status icon to reorder or remove it.

#### 2.13 Control Center (right-side menu bar icon)
- Resembles the iOS Control Center. Modules: Wi-Fi, Bluetooth, AirDrop, Focus, Stage Manager, Screen Mirroring, Display Brightness, Sound, Now Playing, plus extras (Accessibility Shortcuts, Fast User Switching, Keyboard Brightness).
- Expand a module to reveal more controls.
- Drag a module to the menu bar to make it always-visible.

#### 2.14 Notification Center
- Triggered by clicking the date/time in the menu bar, or by swiping left from the right edge of the trackpad with two fingers.
- Today View (widgets) and Notifications list (chronological).
- Stage Manager state appears here.

### 3. What Lives Where

#### 3.1 The Filesystem Hierarchy

```
/
├── Applications/                  # User-installed apps + /Applications/Utilities
├── System/                        # Read-only system files (since Catalina 10.15)
│   ├── Applications/              # Apple system apps (Finder, Safari, Mail, ...)
│   ├── Library/
│   │   ├── CoreServices/          # Finder, loginwindow, Dock
│   │   ├── Frameworks/            # AppKit, CoreFoundation, ...
│   │   └── ...
│   └── Volumes/                   # Hidden volume used to mount / (firmlinks)
├── Library/                       # System-wide data, fonts, startup items
│   ├── Application Support/
│   ├── Caches/
│   ├── Extensions/                # System-wide extensions (kexts, system extensions)
│   ├── Frameworks/
│   ├── LaunchAgents/              # Per-user launch agents (legacy location)
│   ├── LaunchDaemons/             # System launch daemons
│   ├── Logs/
│   ├── Preferences/               # System-wide .plist files
│   ├── Receipts/                  # Install receipts
│   └── ...
├── Users/
│   └── <username>/
│       ├── Desktop/
│       ├── Documents/
│       ├── Downloads/
│       ├── Movies/
│       ├── Music/
│       ├── Pictures/
│       ├── Public/                # Public folder (file sharing)
│       ├── Library/               # HIDDEN by default in Finder
│       │   ├── Application Support/   # App data
│       │   ├── Caches/                # Caches (excluded from Time Machine)
│       │   ├── Preferences/           # Per-user .plist files
│       │   ├── Logs/                  # App logs
│       │   ├── Containers/            # Sandboxed app data
│       │   ├── Group Containers/      # App groups
│       │   ├── Saved Application State/  # Per-app "Reopen windows" state
│       │   ├── Cookies/               # Browser cookies
│       │   ├── Keychains/             # Login + system keychains
│       │   ├── Application Scripts/   # Per-user app scripts
│       │   ├── Autosave Information/  # Auto-save backups
│       │   ├── Fonts/                 # User-installed fonts
│       │   ├── Services/              # Per-user Services (right-click menu)
│       │   ├── Developer/             # Xcode derived data
│       │   ├── Mail/                  # Mail.app storage
│       │   ├── Messages/              # chat.db (SQLite)
│       │   ├── Calendars/
│       │   └── Safari/                # History, cache, etc.
│       ├── .Trash/                # User's trash
│       ├── .ssh/                  # SSH keys
│       └── ...                    # Many dotfiles (zshrc, bash_profile, gitconfig, ...)
├── Volumes/                       # Mounted drives, disk images
├── Network/                       # Network mounts (often empty)
├── private/                       # Symlink farm (older Unix paths)
│   ├── var/ -> /var
│   ├── tmp/ -> /tmp
│   └── etc/ -> /etc
├── usr/                           # Unix system resources (read-only)
│   ├── bin/ -> /usr/bin (firmlink)
│   ├── lib/
│   ├── local/                     # Homebrew, etc.
│   └── sbin/
├── bin/ -> /usr/bin (firmlink)
├── sbin/ -> /usr/sbin (firmlink)
├── etc/ -> /private/etc (firmlink)
├── var/ -> /private/var (firmlink)
├── tmp/ -> /private/tmp (firmlink)
├── dev/                           # Devices
├── opt/ -> /private/var/opt (firmlink, Homebrew)
├── cores/                         # Crash dumps (.crash, .ips)
├── .Spotlight-V100/               # Spotlight index (hidden)
├── .fseventsd/                    # File system events daemon
└── .DocumentRevisions-V100/       # Document revisions
```

#### 3.2 Firmlinks and the Signed System Volume
- **Firmlinks** are an Apple filesystem feature (since 10.15 Catalina) that makes a single directory appear in multiple paths.
- Example: `/Users/<user>/Library/Application Support` and `/Library/Application Support` are both valid; content is shared via the underlying **Data** volume.
- The system volume is **Signed System Volume (SSV)**: every byte is hashed; tampering breaks the boot. macOS refuses to mount a broken SSV.
- Two volumes in one APFS container: `Macintosh HD` (read-only system) + `Macintosh HD - Data` (read-write data), plus `Preboot`, `Recovery`, `VM`.

#### 3.3 APFS
- **Apple File System** — default since 10.13 High Sierra. Replaced HFS+.
- Features: snapshots, clones, encryption, space sharing across volumes.
- A typical install has multiple APFS volumes in one container.
- Disk Utility shows the tree under the container.

#### 3.4 Hidden files and folders
- Finder hides files starting with `.` (Unix) and certain Apple-specific files.
- Show hidden files in Finder: **Cmd+Shift+.** (period) toggles them.
- Show the user Library: hold **Option** and click the **Go** menu → Library appears.
- Or: `chflags nohidden ~/Library` (some macOS versions ignore this).
- Globally enable hidden files: `defaults write -g AppleShowAllFiles -bool true` (then re-toggle with Cmd+Shift+.).

#### 3.5 Spotlight and the index
- Spotlight (Cmd+Space) searches files, app contents, calendar, contacts, etc.
- Index lives at `/.Spotlight-V100` on the root of each volume.
- Exclude a drive/folder: System Settings → Siri & Spotlight → Privacy → drag it onto the list.
- Rebuild: `sudo mdutil -E /` (root volume), or per-volume `sudo mdutil -E /Volumes/Foo`.
- Inspect metadata for a file: `mdls /path/to/file`.

#### 3.6 Time Machine
- Backs up `/Users` and system files to an external or network target.
- The first backup is a full snapshot; subsequent backups are incremental.
- Backups are stored in a `Backups.backupdb` directory on the target, with date-named folders.
- Enter Time Machine: Launchpad → Time Machine, or System Settings → General → Time Machine → Enter Time Machine.

#### 3.7 Trash
- Each user has `~/.Trash/`. The Dock Trash icon is the unified visual.
- Files in Trash count against disk usage but don't trigger "low disk" warnings until you empty.
- Force-empty: `rm -rf ~/.Trash/*` (be careful).
- Secure Empty Trash was removed in 10.12; "Immediately delete" replaced it.

#### 3.8 Where apps put their data
- **Modern sandboxed apps**: `~/Library/Containers/com.example.app/Data/...` (or similar) — each app gets its own container.
- **Non-sandboxed apps**: `~/Library/Application Support/AppName/...`
- **Preferences**: `~/Library/Preferences/com.example.app.plist`
- **Caches**: `~/Library/Caches/com.example.app/`
- **Logs**: `~/Library/Logs/AppName/`
- **App Store / iCloud**: `~/Library/Mobile Documents/com~apple~CloudDocs/`
- **Group containers**: `~/Library/Group Containers/...` for data shared between apps in the same entitlement group.

#### 3.9 System Settings vs System Preferences
- `System Preferences` (10.0 → 12) was renamed to `System Settings` in macOS 13 Ventura, with an iOS-style sidebar layout.
- Underlying preferences live in `~/Library/Preferences/` and `/Library/Preferences/` as `.plist` files.
- Panels include: General, Appearance, Accessibility, Control Center, Siri & Spotlight, Notifications, Focus, Screen Time, Privacy & Security, Network, Bluetooth, Sound, Displays, Wallpaper, Screen Saver, Battery, Energy, Keyboard, Mouse, Trackpad, Printers & Scanners, Internet Accounts, Wallet & Apple Pay, Extensions, Sharing, Time Machine, Users & Groups, Login Items, Lock Screen, Software Update.

### 4. Input, Gestures, and Shortcuts

#### 4.1 Trackpad gestures
- Two-finger scroll (natural or classic).
- Pinch with two fingers to zoom.
- Rotate with two fingers.
- Three-finger drag: System Settings → Accessibility → Pointer Control → Trackpad Options.
- Three-finger swipe up: Mission Control.
- Three-finger swipe down: App Exposé.
- Three-finger swipe left/right: switch full-screen apps or pages.
- Four-finger pinch: Launchpad.
- Four-finger spread: Show Desktop.
- Force Touch / Haptic Touch: click and hold for a deeper press (Quick Look in Finder, dictionary lookups).

#### 4.2 Magic Mouse gestures
- One-finger scroll.
- Two-finger swipe between full-screen apps.
- Two-finger double-tap: Mission Control (configurable).

#### 4.3 Keyboard shortcuts (indispensable)
- **Cmd+Space** — Spotlight search.
- **Cmd+Tab** — app switcher.
- **Cmd+`** (backtick) — switch windows of the current app.
- **Cmd+Shift+3** — screenshot full screen.
- **Cmd+Shift+4** — screenshot selection.
- **Cmd+Shift+5** — Screenshot toolbar (record too).
- **Cmd+Option+Esc** — Force Quit.
- **Cmd+Shift+.** — show/hide hidden files in Finder.
- **Cmd+,** — Preferences.
- **Cmd+W** — close window.
- **Cmd+Q** — quit app.
- **Cmd+H** — hide app.
- **Cmd+M** — minimize.
- **Cmd+Option+H** — hide all other apps.
- **Cmd+Control+Q** — lock screen.
- **Cmd+Shift+Q** — log out.
- **Cmd+Option+Power** — sleep.
- **F3** — Mission Control.
- **F4** — Launchpad (configurable; on newer Macs often Stage Manager).
- **Cmd+F3** — Show Desktop (on some keyboards).

#### 4.4 Hot corners
- System Settings → Desktop & Dock → Hot Corners. Each corner can trigger: Mission Control, Application Windows, Show Desktop, Launchpad, Notification Center, Disable Screen Saver, Put Display to Sleep, Start Screen Saver, Quick Note.

### 5. System Apps (default install)

- **Finder** — file manager. Always running; cannot be quit.
- **Safari** — default browser.
- **Mail** — default email client. Storage in `~/Library/Mail/`.
- **Messages** — iMessage. Database at `~/Library/Messages/chat.db` (SQLite).
- **Maps**, **Photos**, **Music**, **Podcasts**, **TV**, **Books**, **News**, **Stocks**, **Weather**, **Voice Memos**, **Home**, **Shortcuts**, **Reminders**, **Notes**, **Calendar**, **Contacts**, **FaceTime**, **Translate**, **Freeform**, **Passwords** (macOS 15+).
- **Productivity**: Pages, Numbers, Keynote (iWork).
- **Creative**: iMovie, GarageBand, Clips, Photos.
- **Developer**: Xcode, Swift Playgrounds, Terminal, Activity Monitor, Console, Disk Utility, Migration Assistant, ColorSync Utility, Audio MIDI Setup, Bluetooth File Exchange, Digital Color Meter, Grapher, Keychain Access, Script Editor, System Information (Apple menu → About This Mac → More Info), VoiceOver Utility, Wireless Diagnostics.
- **Other**: App Store, Calculator, Clock, Dictionary, Font Book, Image Capture, Photo Booth, Preview, QuickTime Player, Stickies, TextEdit, Time Machine, Automator, Utilities folder.

### 6. Power User

#### 6.1 defaults
- The `defaults` command reads/writes preference plists.
- `defaults read com.apple.dock` — read Dock preferences.
- `defaults write com.apple.dock tilesize -int 36` — change Dock icon size.
- `defaults write -g AppleShowAllFiles -bool true` — show hidden files globally.
- `defaults write -g ApplePressAndHoldEnabled -bool false` — disable press-and-hold accent menu.
- After a change, `killall <App>` (e.g. `killall Dock`, `killall Finder`) to apply.
- `defaults domains` — list all domains.
- `defaults find <keyword>` — search for a setting.

#### 6.2 Property lists (.plist)
- macOS preference files. Binary by default, convertible to XML.
- `defaults read` shows them.
- `plutil -convert xml1 foo.plist` — binary to XML.
- `plutil -lint foo.plist` — syntax check.
- Edit with Xcode (File → Open) or a text editor.

#### 6.3 The .app bundle
- A macOS app is a directory with a `.app` extension.
- Inside: `Contents/Info.plist` (metadata), `Contents/MacOS/Executable` (the binary), `Contents/Resources/` (icons, nibs, localizations), `Contents/Frameworks/` (embedded private frameworks), `Contents/PlugIns/` (loadable bundles), `Contents/_CodeSignature/` (code signature).
- Right-click an app → "Show Package Contents" to inspect.
- `codesign -dvv /Applications/Foo.app` — show code signature.
- `spctl -a -t exec -vv /Applications/Foo.app` — Gatekeeper assessment.

#### 6.4 AppleScript, JXA, Apple Events
- **AppleScript** — the original scripting language. `osascript -e 'tell application "Safari" to activate'`.
- **JXA (JavaScript for Automation)** — modern alternative. `osascript -l JavaScript -e 'Application("Safari").activate();'`.
- **Apple Events** — IPC mechanism for AppleScript, Automator, accessibility.
- **Automator** — GUI workflow builder (`/Applications/Automator.app`).
- **Shortcuts** (since macOS 12) — iOS-style automation, more modern than Automator.
- Synthetic input via System Events requires Accessibility permission: `osascript -e 'tell application "System Events" to keystroke "hello"'`.

#### 6.5 launchd
- macOS's init system. Replaced `init`, `rc`, and `cron` (kinda).
- Two domains: `system` (LaunchDaemons in `/Library/LaunchDaemons/` and `/System/Library/LaunchDaemons/`) and `user/$uid` (LaunchAgents in `~/Library/LaunchAgents/` and `/Library/LaunchAgents/`).
- `launchctl list` — list loaded services.
- `launchctl load -w ~/Library/LaunchAgents/com.example.foo.plist` — load and persist.
- `launchctl unload ~/Library/LaunchAgents/com.example.foo.plist` — unload.
- `launchctl print system` or `launchctl print gui/$(id -u)` — detailed state.
- `brew services` is the Homebrew wrapper for user-managed daemons.

#### 6.6 System Integrity Protection (SIP)
- Introduced in 10.11 El Capitan.
- Locks down `/System`, `/usr` (except `/usr/local`), and certain processes.
- Even root cannot write to SIP-protected paths without disabling SIP (boot to Recovery, `csrutil disable`).
- `csrutil status` to check.
- SIP also blocks code injection into system processes and unsigned kernel extensions.

#### 6.7 Gatekeeper, XProtect, Notarization
- **Gatekeeper** — verifies that downloaded apps are signed and notarized.
- `xattr -d com.apple.quarantine /path/to/app` removes the quarantine flag (only if you trust the app).
- **XProtect** — built-in malware scanner, auto-updating. Checks apps at launch.
- **Notarization** — Apple scans uploaded apps for malware and signs them. Required for distribution outside the Mac App Store since 10.14.5.

#### 6.8 TCC (Transparency, Consent, Control)
- Manages which apps have access to private data: contacts, calendar, photos, microphone, camera, screen recording, accessibility, full disk access, automation, etc.
- Database at `~/Library/Application Support/com.apple.TCC/TCC.db` (SQLite).
- The "Foo wants to access the camera" dialogs are TCC.
- Reset: `tccutil reset All` or `tccutil reset Camera` (or specific subsystem).
- Modifying the database directly requires Full Disk Access for the editing tool.

#### 6.9 Keychain
- macOS's password store. `Keychain Access.app` in Utilities.
- Items: internet passwords, Wi-Fi passwords, certificates, secure notes, encryption keys.
- CLI: `security find-internet-password -s example.com`.
- iCloud Keychain syncs across devices.
- Items live in `~/Library/Keychains/login.keychain-db` and `/Library/Keychains/System.keychain`.

#### 6.10 Activity Monitor
- View processes, CPU, memory, energy, disk, network.
- "Energy" tab: Energy Impact per app (finds battery hogs).
- "Sample" process: capture a stack trace.
- "Open Files and Ports" tab — see which files a process has open.
- CLI equivalents: `top`, `htop`, `ps`, `lsof`, `iostat`, `vm_stat`, `fs_usage`, `powermetrics`.

#### 6.11 Console (unified log)
- GUI viewer for the unified log system (introduced in 10.12 Sierra).
- `log show --predicate 'subsystem == "com.apple.dock"' --last 1h` — equivalent CLI.
- `log stream --predicate 'process == "WindowServer"'` — stream live.
- The unified log replaces the older syslog/ASL.

#### 6.12 Shell
- Default shell is **zsh** since 10.15 Catalina (was bash before).
- `/etc/zshrc`, `/etc/zshenv`, `~/.zshrc`, `~/.zshenv`, `~/.zprofile`.
- Apple ships `/etc/zshrc` with prompts and a `_omb` helper.
- PATH modifications: prefer `~/.zshrc` for user, `/etc/paths` for system-wide directories, `/etc/paths.d/*.path` for drop-in additions (one per line).

### 7. Low-Level Internals

#### 7.1 Frameworks
- **AppKit** — `NSApplication`, `NSWindow`, `NSView`, `NSButton`, etc. The Cocoa UI framework.
- **SwiftUI** — modern declarative UI. Cross-platform with iOS/iPadOS. Replaces much of AppKit for new code.
- **UIKit** — iOS UI; available on macOS via Mac Catalyst and via "iOS Apps on Mac" (Apple Silicon).
- **CoreGraphics / Quartz** — 2D drawing, PDF generation, image I/O.
- **CoreAnimation** — animation engine; uses the GPU.
- **CoreText** — text layout and rendering.
- **Metal** — modern GPU API. macOS uses Metal under the hood for almost all rendering.
- **OpenGL** — deprecated on macOS since 10.14 (still works for old code, no new features).
- **WebKit** — the rendering engine for Safari and `WKWebView`.
- **JavaScriptCore** — the JS engine that powers Safari and is exposed to apps.
- **CoreData** — object graph + persistence.
- **Foundation** — `NSString`, `NSArray`, `NSDate`, etc.

#### 7.2 The macOS kernel
- **XNU** — "X is Not Unix" — hybrid Mach + BSD kernel.
- Mach microkernel + BSD layer.
- Drivers: IOKit.
- Kernel extensions (`.kext`) — being deprecated in favor of DriverKit and System Extensions.
- `uname -a` shows the Darwin kernel version.
- Boot shortcuts: Option (Startup Manager), Cmd+R (Recovery), Cmd+Option+P+R (PRAM/NVRAM reset), Cmd+V (verbose), Cmd+S (single-user), Shift (Safe Mode), T (Target Disk Mode).

#### 7.3 Boot process (Apple Silicon vs Intel)
- **Apple Silicon (M1/M2/M3/M4)**:
  1. Boot ROM → iBoot → load kernel.
  2. Signed System Volume (SSV) verified.
  3. Kernel → launchd → loginwindow.
  4. Touch ID authenticates the user; no password screen by default.
- **Intel**:
  1. EFI → boot.efi.
  2. Kernel cache loaded.
  3. launchd starts.
  4. loginwindow shows password screen.

#### 7.4 Security architecture (Apple Silicon)
- **Secure Boot** — verifies the chain from Boot ROM to kernel.
- **Signed System Volume (SSV)** — every byte of the system volume is hashed.
- **Activation Lock** — tied to Apple ID, prevents re-use if stolen.
- **T2 chip (Intel Macs 2018-2020)** — equivalent security processor.
- **FileVault 2** — full-disk AES-XTS encryption.
- **Gatekeeper, XProtect, Notarization** — covered above.

### 8. Recent Releases (the "what's new")

#### 8.1 macOS 15 Sequoia (2024)
- Native window tiling (drag to edge).
- Window Groups (apps can declare tiled-together window sets).
- iPhone Mirroring (drag-drop between iPhone and Mac; use iPhone apps from Mac).
- Apple Intelligence (system-wide AI features, with privacy-preserving Private Cloud Compute).
- Math Notes in the Notes app (evaluate LaTeX-style math).
- Passwords app (separated from Safari).
- Live Activities on Mac.
- Standalone Audio apps, screen-sharing updates.

#### 8.2 macOS 26 Tahoe (2025)
- Year-based naming (Apple dropped the 10/11 scheme; macOS 26 = Tahoe, named after Lake Tahoe).
- **Liquid Glass** design — translucent, layered, glass-like UI inspired by visionOS. More depth in toolbars, sidebars, and panels; more generous corner radii.
- Phone app on Mac (continuity; mirrors iPhone Phone app).
- Live Activities on Mac (continued).
- New Spotlight refinements, new Control Center modules.
- Notes app updates (Markdown rendering, transcription).
- Calculator updates.
- Cross-platform continuity with iOS 26, iPadOS 26, watchOS 26, visionOS 26, tvOS 26.

### 9. Useful One-Liners

```bash
# macOS version
sw_vers
# expected: ProductName: macOS, ProductVersion: 26.x (Tahoe) or 15.x (Sequoia)

# Hardware model
system_profiler SPHardwareDataType | grep "Model Name"

# CPU
sysctl -n machdep.cpu.brand_string

# APFS volumes
diskutil apfs list

# Current user's launchd services
launchctl print gui/$(id -u)

# System report
system_profiler > ~/Desktop/system-report.spx

# Open the user Library in Finder
open ~/Library

# Open a path in Finder from terminal
open /etc

# Which app has a file open
lsof | grep -i <pattern>

# Tail unified log
log stream --predicate 'subsystem == "com.apple.windowserver"' --info

# Battery cycle count
system_profiler SPPowerDataType | grep "Cycle Count"

# Reset Launchpad layout
defaults write com.apple.dock ResetLaunchPad -bool true; killall Dock

# Show hidden files in Finder (toggle via Cmd+Shift+. also works)
defaults write com.apple.finder AppleShowAllFiles -bool true; killall Finder
```

## Pitfalls

- **The Library folder is hidden by default** — `~/Library` is the single most useful folder and the single most hidden. Press `Cmd+Shift+.` in Finder, hold **Option** and click the **Go** menu, or `chflags nohidden ~/Library`.
- **SIP is invisible** — you cannot write to `/System` or `/usr` (except `/usr/local`) even as root. If a tool says "permission denied" on a system file, that's SIP, not your user. You need Recovery Mode + `csrutil disable` to override.
- **Apple's `defaults` system is read at app launch** — many preference changes only apply after the app restarts. `killall <App>` to force the read.
- **The unified log truncates aggressively** — older messages get pruned. Forensics also check `~/Library/Logs/DiagnosticReports/`, `/Library/Logs/DiagnosticReports/`, and Console's "Crash Reports" section.
- **Spotlight index corruption** — if Spotlight searches return nothing, rebuild with `sudo mdutil -E /`. For a specific volume: `sudo mdutil -E /Volumes/Foo`.
- **macOS case-insensitive by default, case-preserving** — APFS can be case-sensitive (set at install time; hard to change later). `File.txt` and `file.txt` are the same file in case-insensitive mode.
- **Trash on external drives** — when you eject an external drive, its Trash is gone with it.
- **Right-click "Open With" sticks to old app versions** — if an old app is offered, use "Get Info" → "Open with" → "Change All" to fix.
- **Quarantine flags block unsigned apps** — if a downloaded app won't open, `xattr -d com.apple.quarantine /path/to/app` (only if you trust it). Or right-click → Open → Open (the second Open is the Gatekeeper bypass).
- **macOS doesn't have a system-wide "Documents" folder** — `~/Documents` is just a folder. Apps are encouraged to store data in `~/Library/Application Support/`, not in `~/Documents`.
- **Time Machine purges old backups when the target is full** — oldest are deleted first.
- **Stage Manager is a separate mental model from Mission Control** — switching between them mid-workflow can disorient. Pick one (or full-screen Spaces).

## Verification

This skill is a knowledge reference. To verify any fact on a live macOS:

```bash
# macOS version
sw_vers
# expected: ProductName: macOS, ProductVersion: 26.x (Tahoe) or 15.x (Sequoia), BuildVersion: 25A...

# Hardware model and serial
system_profiler SPHardwareDataType

# User Library exists and is hidden in Finder
ls -ld ~/Library

# Spotlight index integrity
mdls -name kMDItemContentType /path/to/file

# Gatekeeper
spctl --status
# expected: assessments enabled

# SIP
csrutil status
# expected: System Integrity Protection status: enabled

# Known preference domains
defaults domains | tr ',' '\n' | head -20

# WindowServer launchd state
launchctl print system | grep -A 3 WindowServer
```

On a Linux host (this skill's home), no live verification is possible — the knowledge is sourced from public Apple documentation and macOS usage history, versioned by macOS release.
