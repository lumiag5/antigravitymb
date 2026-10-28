# Changelog &bull; Antigravity Mobile APK (Android)

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.md">Português</a> &bull; <b>English</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.es.md">Español</a>
</p>

All notable changes to the native Android app (**Antigravity Mobile APK**) are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Fixed
* **APK Scrolling**: Removed `SwipeRefreshLayout` from the native layout, allowing free message scrolling without touch traps.
* **Transition to Done**: Status transitions to "Completed" immediately when the model finishes its response.
* **History Toast Warning**: Fixed misleading error toast when opening conversations from the chats modal.
* **Removal of "✕" Buttons**: Modals now close by tapping outside or via the "Close" button in the footer.

### Added
* **Real-time "Thinking" Sync**: Instant detection via SQLite of the active conversation, switching immediately to "Thinking...".
* **Background Task Unification**: Background tasks are unified under "Task Running...". Status transitions to "Done" only when no activity remains in the project.
* **"Chats" Button**: Modal to switch between conversations and synced projects from PC, with status indicators (`🟠` working / `🟢` idle).
* **Remote Conversation Reading**: View full conversation history on mobile without changing the active screen on PC.
* **APK Version Badge**: The header indicates whether the running version is native `(APK)` or browser `(IP)`.
* **In-App Updater**: Option in the app menu to check, download, and install updates directly from GitHub Releases.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Added
* **Native QR Code Scanner**: Camera scanner integration via ZXing to scan PC terminal QR codes with embedded PIN.
* **Session Manager**: App opens to the connection screen when launched to keep the active feed secure.
* **Session Resume**: "Return to Session" button to reconnect to the active server without retyping the PIN.
* **"New Session" and "Sign Out"**: Shortcuts to switch servers or disconnect via the menu.
* **OLED Black UI**: Removed legacy buttons in favor of a clean `#000000` background.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Fixed
* **Network Protocol (HTTP/HTTPS)**: Uses `http://` for local IPs and `https://` only for tunnels and public domains, preventing TLS errors.
* **Automatic Default Port**: Automatically appends `:8765` when an IP is entered without a port.
* **WebView Error Handling**: Clear connection diagnostics and compatibility with Android 7 through 9.

### Added
* **Connection Shortcuts**: Quick-fill buttons for emulator, local Wi-Fi, and Cloudflare, plus a button to paste from clipboard.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Initial APK Release
* **Native Android Structure**: Kotlin project targeting `minSdk = 24` (Android 7.0+) and `targetSdk = 34` (Android 14).
* **Accelerated WebView**: Hardware acceleration, WebSockets (`/ws`), Web Audio API, and OLED Black theme `#000000`.
* **System Permissions**: Native push notification support (`POST_NOTIFICATIONS`) and cleartext local traffic (`usesCleartextTraffic`).
* **CI/CD via GitHub Actions**: Automated build and packaging of APK releases on every push or tag.
