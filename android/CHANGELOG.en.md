# Changelog &bull; Antigravity Mobile APK (Native Android)

<p align="center">
  <a href="CHANGELOG.md">Português</a> &bull; <b>English</b> &bull; <a href="CHANGELOG.es.md">Español</a>
</p>

All notable changes, bug fixes, and new features dedicated exclusively to the native Android app (**Antigravity Mobile APK**) are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### ⚡ Real-Time Thinking Sync & Done Transition
* **Fixed Transition to "Done" (Completed)**:
  * Eliminated the lock that caused the app to stay stuck in *"Task Running"* even after test results and answers had been fully rendered on PC.
  * The monitor now recognizes the final assistant completion instantly, smoothly transitioning status to **"Completed"** (*Done*), triggering the pleasant audio chime, dual screen flash, and starting the 1-minute completion timer.
* **Instant "Thinking" Status Synchronization**:
  * Implemented sub-second direct reading of execution steps within the active conversation's SQLite database (`conversations/<conv_id>.db`).
  * As soon as a user prompt is dispatched and Antigravity PC enters **"Thinking..."** mode, the mobile app switches **instantaneously** to **"Thinking..."** (*Thought* / *Thinking* with pulsing purple indicator `#a855f7`), eliminating delay and achieving real-time screen parity.

### ⚙️ Background Task Unification & Strict Completion (Done)
* **Unification of "Background Task" with "Task Running"**:
  * Antigravity PC background tasks (*Background Task*, subagents `invoke_subagent`, `schedule` timers, `manage_task` commands, and asynchronous shell jobs) are now strictly unified under the exact same status of **"Task Running..."** (*Executando Tarefa...* / *Ejecutando Tarea...*).
  * Visual indicator: pulsing electric cyan dot (`#0ea5e9`).
* **Strict Rule for "Done" (Completed) Status**:
  * The **"Done"** (*Completed*) status **is ONLY declared when there is absolutely no activity running in the current project** (`conversation_summaries.db`: `status == 'CASCADE_RUN_STATUS_IDLE'` and `not_fully_idle == 0`, no active task logs in `.system_generated/tasks/`, and no running subagents).
  * As long as any background activity is active in the project, the status remains `TASK_RUNNING` ("Task Running..."). Only upon total conclusion of all tasks does it transition to `DONE` ("Completed"), sounding the chime and starting the 1-minute visual timer.

### 🐛 Scrolling & Gesture Fixes
* **Definitive Fix for Chat Scrolling on APK**:
  * Completely removed the `SwipeRefreshLayout` wrapper from the native layout (`activity_main.xml`) and its listeners in `MainActivity.kt`.
  * Because the web app uses a fixed viewport (100vh) with internal `#chat-feed` scrolling, `SwipeRefreshLayout` was mistakenly intercepting downward touch gestures (`canScrollVertically(-1) == false`), locking up the view and preventing users from scrolling up to see previous messages on Android.
  * `WebView` now sits directly inside `FrameLayout` with `isVerticalScrollBarEnabled = true` and `OVER_SCROLL_IF_CONTENT_SCROLLS`, restoring 100% smooth native touch scrolling through entire message histories.
  * Disabled WebView caching (`LOAD_NO_CACHE`) ensuring newly deployed web scripts and styles reload immediately.

### 💬 Chats Navigation & History Toast Fix
* **Eliminated Misleading Error Toast on Opening History**:
  * Fixed active project header title update call (`updateProjectName`), preventing a script ReferenceError that triggered the misleading toast *"Failed to open conversation history"* even when chat messages rendered perfectly.
* **Central "Chats" Button in Footer**:
  * New `💬 Chats` button positioned in the bottom center of the screen (between Menu/Latency and OLED buttons).
  * Instant access to a responsive modal listing all recent conversations and projects synchronized from the PC.
* **Fix for "Error loading PC chats"**:
  * Added fallback scanning of `brain/` directory folders, ensuring the project and conversation list never fails even if SQLite summaries are locked or busy.
* **Strict Pulsing Dot Status (No Preceding Text)**:
  * Processing/active conversations: display strictly a pulsing orange dot (`🟠`).
  * Idle conversations: display strictly a pulsing green dot (`🟢`).
  * In accordance with requirements, without any text or message prefix preceding the dot.
* **Independent Remote History Inspection**:
  * Tapping any chat or project loads its full message transcript without simulating mouse clicks or changing the active window/project on the host PC.

### 🔄 Execution Statuses & Unification
* **"Thinking..." Status (Unified "Thought" & "Thinking")**:
  * Merged both "Thought" and "Thinking" states into "Thinking..." (EN) / "Pensando..." (PT/ES) with pulsing purple indicator (`#a855f7`).
* **Cleaned Intermediate States**:
  * Intermediate "Analyzed" and "Ran" states removed as requested, consolidating execution into primary phases: "Thinking...", "Working...", "Task Running...", and "Done" (for 1 minute).
* **Preserved Core Statuses**:
  * "Processing" renamed to "Working...".
  * "Task Running..." (*Executando Tarefa...*) with electric cyan pulsing indicator.
  * "Done" (*Completed*) remains displayed for 1 minute before reverting to "Connected".

### 🧹 Removed "✕" Icons & Backdrop Click-to-Close
* **Global Removal of "✕" Close Button**:
  * Removed "✕" button from all modal interfaces (Tutorial, Settings Menu, Completion History Log, and Chats Modal).
  * Modals auto-close by tapping outside (backdrop click) or via a clean "Close" button at the bottom.

### 📱 Dynamic Version Badge & In-App Auto-Updater
* **Dynamic Header Version Badge**:
  * Automatic runtime environment detection: native APK displays its installed binary version (`vX.X.X (APK) • Dev LumiaG5`), fixing the discrepancy where it displayed cached web versions. On browser/IP access, it displays `v2.4.3 (IP) • Dev LumiaG5`.
* **In-App APK Auto-Updater in Settings Menu**:
  * Dedicated native section inside `⚙️ Menu`.
  * Automatically checks latest GitHub releases using SemVer comparison.
  * Background download of new `.apk` release with native Android installation triggered via secure `FileProvider` (`ACTION_VIEW`).
* **Security Audit**:
  * Complete repository and Git history scan confirming zero leaked API keys, tokens, or credentials.
  * Path traversal sanitization added to backend server endpoints.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### 🚀 New Features & Session Security
* **Auto-Logout on App Close**:
  * Reopening the mobile app always launches into the **Session Manager** screen, keeping monitoring sessions safe and private.
  * Native Android "Back" button inside chat safely disconnects to the session screen.
  * Added direct shortcut **`🚪 Sign Out / Disconnect Session`** inside the `⚙️ Menu`.
* **"▶ Resume Session" (No PIN needed)**:
  * If the desktop bridge is still running on the PC, a green-badged card displays the server address with a **"Resume Session"** button.
  * Tapping it restores access immediately using the cached 24-hour cryptographic auth token.
* **"📷 Sign in with QR Code" via Native Camera (ZXing)**:
  * Integrated ZXing Android Embedded computer vision library.
  * Native runtime camera permission request (`android.permission.CAMERA`).
  * PC terminal embeds PIN directly into ASCII QR Code (`?pin=XXXX`). Pointing the camera at the terminal establishes 100% instant pairing without typing.
* **"⚡ New Session"**:
  * Allows starting afresh, clearing cached tokens and enabling connection to a new server or typing a new PIN.
* **Clean OLED True Black UI**:
  * Cleaned up legacy shortcut clutter for a minimalist aesthetic saving battery on AMOLED/OLED displays (`#000000`).

---

## [2.4.1] - 2026-10-25 (Build 2419)

### 🐛 Connection & Network Fixes
* **Intelligent Protocol Deduction (HTTP vs HTTPS)**:
  * Fixed an issue where local IP addresses (e.g., `192.168.0.6:8765` or `10.0.2.2:8765`) were forced to `https://`, triggering TLS handshake failures on Python/Uvicorn (`WARNING: Invalid HTTP request received`) and black screen stalls.
  * App now detects local IPs (`192.168.x.x`, `10.x.x.x`, `172.x.x.x`, `127.0.0.1`, `localhost`, and `:8765`) and strictly enforces `http://`, reserving `https://` for Cloudflare tunnels and web domains.
* **Default Port Auto-Completion**:
  * Automatically appends `:8765` if a local IP is entered without a port number.
* **Detailed Error Diagnostics**:
  * Error screen displays the exact target URL and reason/code returned by WebView, alongside "Try Again" and "Switch Server" options.
* **WebView Backward Compatibility**:
  * Dual error handling (`WebResourceRequest` modern and legacy `onReceivedError`) ensures reliability on older Android 7 and 9 environments (like LDPlayer emulators).

---

## [2.4.0] - 2026-10-25 (Build 2418)

### 📱 Initial Native Wrapper Release
* **Native Kotlin / Gradle Foundation**:
  * Official package `com.lumiag5.antigravitymobile`.
  * `minSdk = 24` (Android 7.0+) and `targetSdk = 34` (Android 14).
* **Optimized WebView**:
  * Hardware acceleration, WebSockets (`/ws`), Web Audio API, and persistent `domStorage`.
  * System bars styled in OLED True Black (`#000000`) via `WindowCompat`.
* **System Permissions**:
  * Push notification support (`POST_NOTIFICATIONS` on Android 13+).
  * Cleartext traffic enabled (`usesCleartextTraffic="true"`) for local Wi-Fi HTTP connections.
* **Automated CI/CD Pipeline (GitHub Actions)**:
  * `.github/workflows/build-apk.yml` builds Release and Debug APKs on every tag or commit.
