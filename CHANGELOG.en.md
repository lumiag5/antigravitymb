# Changelog

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.md">Português</a> &bull; <b>English</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.es.md">Español</a>
</p>

All notable changes to **Antigravity Mobile** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
