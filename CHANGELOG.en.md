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
