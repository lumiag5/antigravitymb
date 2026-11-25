# Changelog

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.md">Português</a> &bull; <b>English</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.es.md">Español</a>
</p>

All notable changes to **Antigravity Mobile** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.5.2] - 2026-11-24 (Build 2520)

### Added
* **In-app "Stop" button (`POST /api/cancel`)**: While a task is running on PC, a **Stop** button appears next to Prompt so you can cancel the execution from your phone via `CancelCascadeInvocation`.
* **Windows System Tray icon**: New zero-dependency `tray.py` module and `[T] Tray` terminal shortcut to hide/restore the console near the clock, with right-click menu (show terminal, open browser, new PIN, update server, exit).

### Fixed
* **Gemini 4 Hydrogen detection**: Fixed model parser and placeholder mapping (`MODEL_PLACEHOLDER_M525`..`M528`) so Hydrogen displays as Hydrogen instead of Argon.
* **Remote prompt dispatch on newer Antigravity PC**: Updated `antigravity_api.py` to discover ports and CSRF tokens from `daemon/hub_*.json` (Antigravity 2.34+) and forward `cascade_config.planner_config.plan_model` properly.
* **Stale orange activity dot**: Fixed false-positive processing dots in Chats by checking `GetAllCascadeTrajectories` and SQLite timestamp freshness on idle conversations.
* **Hydrogen tier detection & stable latency**: Live detection of Hydrogen tiers (*High*, *Medium*, *Low*, *XHigh*) via `GetCascadeTrajectory` and offloaded blocking RPC/SQLite calls via `asyncio.to_thread` to keep WebSocket ping latency steady.

### Changed
* **Single QR code**: Removed the emergency Cloudflare tunnel startup and second QR code banner in the terminal, keeping only the primary local Wi-Fi QR code.
* **Cleaner UI**: Replaced heavy emoji clutter with crisp inline SVG icons, trimmed robotic copy across screens, and added `/api/models` live model syncing.
* **Interactive terminal updater**: Startup GitHub check now asks `[Y/N]` before downloading, terminal action bar includes `[U] Update Server (GitHub)` with progress bar, applies static updates without restarting, and auto-restarts in the same window when Python files change.

---

## [2.5.1] - 2026-10-29 (Build 2510)

### Added
* **Local Server Terminal Updater**:
  - Automatic update check against GitHub releases right after language selection.
  - Dual attempt (2x) retry mechanism that gracefully falls back without blocking offline startup if unreachable.
  - Live console progress bar displaying download percentage (`%`), downloaded megabytes, and transfer speed in MB/s.
  - Archive extraction (`.7z` and `.zip`) and safe replacement of server files.
  - Prominent server version display (`v2.5.1`) in the terminal banner and restart prompt on update completion.
  - On-demand keyboard shortcut: press `U` at any time in the terminal to check for Local Server updates.

### Fixed
* **Infinite update loop**: The updater now analyzes SHA-256 hashes and file sizes of all extracted files; if all local files are already identical to remote release files, the server does not ask to restart and starts immediately.
* **Version persistence**: Added `version.json` state tracking and hard synchronization to prevent `config.py` from downgrading to previous releases.

---

## [2.5.0] - 2026-10-29 (Build 2500)

### Added
* **Remote prompt dispatch**: Send prompts directly from your phone to Antigravity on PC (`POST /api/prompt`) with AI model selection (Gemini 3.8 Flash, Pro, Claude 3.7 Sonnet, GPT-4o, etc.).
* **Quick prompt snippets**: One-tap shortcut chips (🔄 *Continue*, 🧪 *Run tests*, 📋 *Summarize progress*, 🐞 *Check errors*).
* **Prompt history & counter**: Recent prompts recall with arrow-up key navigation and live character/word count.
* **Smart back navigation**: Pressing back hierarchically closes open modals (History, Prompt, Chats, Menu, Log, Tutorial) or returns to the active PC chat. On the home screen, double-tap cleanly exits without opening the session screen.
* **Native text selection & copy**: Removed the long-press interceptor that triggered the reconnect screen. Holding down on message text now invokes Android's native text selection toolbar.
* **Battery & performance optimizations**:
  - Native lifecycle hooks with `onPause`/`onResume` on WebView to halt GPU repaints when the screen turns off or the app is minimized.
  - Pauses CSS animations and network ping timers via Page Visibility API (`body.app-paused`).
  - WebSocket reconnection with exponential backoff to avoid draining battery when the PC server is offline.
  - Automatic low battery profile (<= 20% unplugged) disabling heavy box-shadows and reducing ping frequency.
  - Parallelized initial data loading with `Promise.allSettled`.
* **Response quick actions**: One-tap copy button with visual feedback (📋 ➔ ✅) and native share button (📤 via Web Share API) to send responses to WhatsApp, Telegram, or Notes.
* **Dynamic thinking indicator**: Bouncing dots animation indicating when the AI is reasoning or working.
* **Favorite chats**: Star button (⭐) to pin important conversations to the top with persistent local storage.
* **Fast chat search**: Instant search filter by title or project in Chats and Prompt modals.

---

## [2.4.4] - 2026-10-28 (Build 2426)

### Added
* **Immersive fullscreen mode**: Hides the top system status bar and notifications on Android APK (with display notch support), plus fullscreen mode for browser/IP via tap or settings menu toggle.
* **Real-time battery indicator**: Centered in the footer (between latency and chats) displaying battery percentage and charging status with zero extra text clutter.
* **Harmonized footer layout**: Symmetrical, balanced bottom bar aligning all buttons and status badges in a single row with rounded pill styling and OLED theme support.

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Fixed
* **APK Scrolling**: Removed `SwipeRefreshLayout` from the Android app, allowing free scrolling through chat history without gesture locks.
* **Removal of "✕" Buttons**: Modals now close by tapping outside or via the "Close" button in the footer.

### Added
* **"Chats" Button**: Modal to switch between conversations and synced projects from PC, with status indicators (`🟠` working / `🟢` idle).
* **Remote Conversation Reading**: View full conversation history on mobile without changing the active screen on PC.
* **Live Statuses**: Added *Thinking...*, *Working...*, *Task Running...* (with cyan dot), and *Done* (displayed for 1 minute upon completion).
* **Version Identification**: The header now shows whether the running version is native `(APK)` or browser `(IP)`.
* **In-App APK Updater**: Option in the menu to check and install new versions directly from GitHub Releases.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Added
* **QR Code Sign-in**: Native camera scanner (ZXing) in the APK to scan the PC terminal QR code with embedded PIN.
* **Session Resume**: "Return to Session" button to reconnect to the active server without retyping the PIN.
* **"New Session" and "Sign Out"**: Shortcuts to switch servers or disconnect via the menu.
* **Initial Session Screen**: App opens to the connection screen when launched to keep the active feed secure.
* **Clean Interface**: Removed legacy shortcut buttons in favor of the OLED True Black theme `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Fixed
* **Protocol Handling (HTTP/HTTPS)**: Uses `http://` for local IPs and `https://` only for tunnels and public domains, preventing TLS handshake errors.
* **Automatic Default Port**: Automatically appends `:8765` if an IP is entered without a port.
* **WebView Error Handling**: Clearer connection diagnostics and compatibility with Android 7 through 9.

### Added
* **Connection Shortcuts**: Quick buttons for emulator (`10.0.2.2`), local Wi-Fi, and Cloudflare, plus a button to paste from clipboard.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Added
* **Terminal QR Code**: ASCII QR code in the console for quick camera pairing.
* **Settings Menu**: Consolidated preferences for alerts, audio, network, and history into a single footer menu.
* **Audio Customization**: 4 alert sound options and volume slider with local persistence.
* **Ping Metric**: Visual WebSocket latency indicator next to the menu.
* **Task History**: Modal logging recent completed tasks (project, model, and timestamp).

---

## [2.3.6] - 2026-10-25 (Build 2417)

### Added
* **Real-time Model Detection**: Automatic detection of AI model switches (Gemini, Claude, GPT) via Protobuf decoding.
* **Dynamic Quota Switching**: Quota bars adapt dynamically between Gemini and Claude/GPT based on the active model.
* **Read-only SQLite Mode**: Uses `mode=ro` to prevent database locks while the IDE writes data.

---

## [2.3.5] - 2026-10-25 (Build 2416)

### Initial Release
* **Chat Monitoring**: Real-time feed showing user prompts and final assistant responses.
* **Rendering**: Markdown support, syntax-highlighted code blocks, and OLED dark theme.
* **Alerts**: Notifications upon task completion with sound, dual screen flash, and vibration.
* **Quotas**: Tracks 5-hour and weekly quotas from the Antigravity API.
* **Secure Connection**: 4-digit PIN pairing (24h session) and Cloudflare tunnel support for remote access.
* **Languages**: Full support for Portuguese, English, and Spanish.
