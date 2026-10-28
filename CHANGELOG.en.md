# Changelog

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.md">Português</a> &bull; <b>English</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.es.md">Español</a>
</p>

All notable changes to **Antigravity Mobile** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### 🐛 Fixed
* **Native APK Chat Scrolling**: Resolved an issue where users were unable to scroll up to view earlier messages on Android. Removed `SwipeRefreshLayout` from the native Android layout (`activity_main.xml`), allowing `WebView` to handle touch drags directly without gesture interception, ensuring full parity with the web version.
* **Global Removal of "✕" Close Crosses**: Removed the "✕" button from all modals (Tutorial, Menu, Log, and Chats). All modal windows now auto-close by clicking outside (backdrop click) or via a bottom "Close" button.

### 🚀 Added
* **Central "Chats" Button in Footer**:
  * Located in the bottom center of the screen (between Menu/Latency to the left and the OLED button to the right).
  * Opens a modal to select conversations and projects synchronized from Antigravity PC in both versions (APK and IP/Web).
* **Strict Pulsing Dot Status by Conversation**:
  * If Antigravity is processing something in that conversation: displays **only a pulsing orange dot (`🟠`)**, with no text or message in front.
  * If idle/not processing: displays **only a pulsing green dot (`🟢`)**, with no text or message in front.
* **Fully Independent Remote Reading**:
  * Selecting any chat/project in the list loads and renders the full transcript history directly without changing the active conversation or window on the PC and without simulating mouse clicks.
  * Banner with "Return to Live PC" button to quickly switch back to real-time synchronization.
* **Statuses "Working...", "Thinking...", and "Task Running..."**:
  * Status "Processing" renamed to **"Working..."** (*Trabalhando...*).
  * Status **"Thinking..."** (*Thought* / *Thinking*).
  * New status **"Task Running..."** (*Executando Tarefa...*) with cyan pulsing indicator (`#0ea5e9`).
  * Upon task completion, status **"Completed"** (*Concluído*) activates and remains displayed for **1 minute** (or until a new activity starts), reverting to "Connected" after the countdown ends.
* **Version Badge Differentiation (APK vs IP)**:
  * The header now differentiates between the installed APK version on device (`vX.X.X (APK) • Dev LumiaG5`) and the companion IP version (`v2.4.3 (IP) • Dev LumiaG5`), eliminating cache confusion.
* **Android In-App Auto-Update Feature in Menu (Exclusive to Android)**:
  * Dedicated section in `⚙️ Menu` of the APK to check and download new versions in 1 tap directly from GitHub Releases, opening the native system installer via `FileProvider`.
