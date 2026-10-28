# Antigravity Mobile

<p align="center">
  <a href="README.md">Português</a> &bull; <b>English</b> &bull; <a href="README.es.md">Español</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v2.4.3-blue?style=flat-square" alt="Version v2.4.3">
  <img src="https://img.shields.io/badge/platform-Windows_%7C_Android-success?style=flat-square" alt="Platforms">
  <img src="https://img.shields.io/badge/android-7.0%2B_%28API_24%2B%29-green?style=flat-square" alt="Android 7+">
  <img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/build-GitHub_Actions_Passing-brightgreen?style=flat-square" alt="GitHub Actions">
</p>

Mobile companion that turns your smartphone into a **smart second screen** for the **Antigravity IDE** on your PC. Monitor real-time coding progress, receive sensorial alerts (customizable sound tones, screen flashes, and vibrations) upon task completion, track official AI model quotas (Gemini, Claude Sonnet, and GPT), and connect with one tap via the **native Android app** or mobile browser.

---

## 🎯 Why Antigravity Mobile?

When running long agentic tasks in Antigravity IDE — such as massive refactors, complex component generation, test suites, or multi-file debugging —, stepping away from your desk is natural. But keeping track is hard:
- Did the AI agent finish, or is it waiting for terminal approval?
- Which model is currently working (Gemini, Claude 3.5 Sonnet, or GPT-4o)?
- How much of your 5-Hour and Weekly AI quota remains?

**Antigravity Mobile** bridges your PC and phone directly over local Wi-Fi or via an automated **global HTTPS tunnel (Cloudflare)** without manual port forwarding or complex networking.

---

## ⚡ Key Features

### 💬 Real-Time Chat & Noise Filtering
* **Focus on what matters**: Antigravity generates hundreds of internal tool execution and terminal lines. The companion cleans out internal noise, displaying only user prompts and assistant conclusions.
* **Markdown & Code Rendering**: Syntax highlighted code blocks, tables, and typography matching the IDE (Inter and JetBrains Mono fonts).
* **Smart Auto-Scroll & Free Scroll**: Automatically follows incoming responses and lets you scroll up freely through earlier history without gesture traps on both APK and web.

### 💬 Central "Chats" Navigation & Multi-Projects
* **Central "Chats" Button in Footer**: Instant one-tap access to all recent conversations and projects synchronized from Antigravity PC.
* **Strict Pulsing Dot Status**:
  * `🟠` **Pulsing Orange Dot**: Antigravity is actively working/processing in that conversation.
  * `🟢` **Pulsing Green Dot**: Conversation is idle/standby.
  *(100% clean visual with no cluttering text).*
* **Independent Remote History**: Inspect full conversation history on mobile without switching active windows or interfering with work on the PC, featuring a "Return to Live PC" button.

### ⚡ Dynamic Statuses & Real-Time Sync
* **Instant "Thinking" Detection**: Direct sub-second SQLite step inspection (`conversations/<conv_id>.db`) switches immediately to pulsing purple (`#a855f7`) the exact millisecond the PC enters thinking mode.
* **Background Task & Task Running Unification**: Subagents `invoke_subagent`, `schedule` timers, `manage_task` commands, and terminal jobs are unified under pulsing cyan (`#0ea5e9`).
* **Strict "Done" Completion Rule**: Status transitions to "Completed" (*Done*) only when **all activities in the project have fully concluded**, displaying for **1 minute** alongside a chime sound and dual screen flash.

### 🔔 Sensory Completion Alerts
* **Dual Screen Flash**: Two emerald green screen flashes spaced 1 second apart (clearly visible even if your phone is sitting on your desk).
* **Synthesized Audio Ringtones (Web Audio API)**: Choose between 4 distinct sound signatures (*Modern Chime*, *Zen Bell*, *Sci-Fi Pulse*, and *Classic Beep*) with master volume control (0% to 100%) and instant preview.
* **Haptic Vibration**: Dual vibration pattern for meetings and quiet environments.
* **System Push Notifications**: Native Web Notifications delivered to locked screens.

### 🧠 Real-Time AI Model Detection
* **Gemini, Claude, and GPT**: Tracks active model switching on-the-fly mid-conversation via native binary Protobuf wire decoding (field 28 `\xe2\x01` for Claude/GPT and field 19 `\x9a\x01` for Gemini), with zero server reloads needed.

### 📊 Official Quota Tracking (Internal RPC)
* **Real Metrics, Zero Token Guesses**: Directly connects to Antigravity's local RPC service (`LanguageServerService/RetrieveUserQuotaSummary`).
* **Dynamic Model Quota Sync**: Automatically toggles quota bars between `Gemini Models` and `Claude and GPT models` according to the family of the active model.
* **Usage Gauges**: Displays 5-Hour and Weekly consumption percentages alongside precise renewal countdowns.

### 📶 Live Latency Meter (Ping Badge)
* **Interactive Metric**: Color-coded WebSocket round-trip ping badge next to the menu:
  * 🟢 **Green**: Excellent latency (<130ms)
  * 🟡 **Yellow**: Moderate latency (130ms to 320ms)
  * 🔴 **Red**: Slow connection (>320ms)

### 📜 Task Completion History (Log)
* Sliding history modal documenting completed agent tasks with project name, conversation title, active AI model, and exact completion timestamp.

### 📱 Native Android App (Kotlin APK)
Standalone `.apk` package offering deep Android OS integration:
* **In-App Auto-Updater**: One-tap check for new releases on GitHub with background download and direct install via `FileProvider`.
* **Dynamic Version Badge**: Distinguishes whether running on native APK (`vX.X.X (APK)`) or IP browser (`vX.X.X (IP)`).
* **OLED True Black Mode (`#000000`)**: Battery saving on AMOLED screens with true black styling.
* **Clean UI without "✕" Buttons**: Modals auto-close by clicking outside (backdrop) or via a bottom "Close" button.
* **Auto-Logout on App Close**: Pauses the active session whenever the app is closed for privacy.
* **▶ Resume Session (No PIN needed)**: Single tap restores connection to the running PC daemon, backed by a 24-hour cryptographic session cache.
* **📷 Sign in with QR Code via Native Camera (ZXing)**: Integrated camera scanner reads the PC console's ASCII QR code with embedded PIN (`?pin=XXXX`) for instant zero-touch pairing.
* **⚡ New Session**: Flushes previous tokens to pair afresh with a new PIN or different server.
* **Automated Cloud CI/CD**: APK compiled automatically in the cloud on **GitHub Actions**. See the APK Changelogs: [Português](android/CHANGELOG.md) &bull; [English](android/CHANGELOG.en.md) &bull; [Español](android/CHANGELOG.es.md).

---

## 🛠️ Project Architecture

```text
antigravity-mobile/
├── .github/workflows/
│   └── build-apk.yml          # CI/CD: Automated cloud APK compilation
├── android/                   # Native Android Project (Kotlin / Gradle)
│   ├── app/src/main/
│   │   ├── java/.../MainActivity.kt  # Session Manager, WebView, and ZXing Scanner
│   │   ├── res/layout/activity_main.xml  # OLED True Black layout
│   │   └── AndroidManifest.xml
│   ├── CHANGELOG.md           # Android APK Version History (Português)
│   ├── CHANGELOG.en.md        # Android APK Version History (English)
│   └── CHANGELOG.es.md        # Android APK Version History (Español)
├── desktop-bridge/            # PC Bridge Daemon (Python / FastAPI)
│   ├── Start_Server.bat       # One-click Windows launcher
│   ├── run.py                 # CLI with ASCII QR Code and keyboard hotkeys
│   ├── server.py              # FastAPI server and WebSockets (/ws)
│   ├── auth.py                # 4-digit PIN security with 24h cache and auto-rotation
│   ├── monitor.py             # Protobuf wire decoder and background task watcher
│   ├── antigravity_api.py     # Local RPC client for IDE quota metrics
│   ├── tunnel.py              # Cloudflare Quick Tunnel manager
│   ├── language_manager.py    # Trilingual localization (pt, en, es)
│   └── static/                # Mobile PWA companion (HTML5, CSS, JS, Web Audio)
│       ├── index.html         # Full companion dashboard
│       └── manifest.json      # Official PWA specifications
├── CHANGELOG.md               # Global project changelog (Português)
├── CHANGELOG.en.md            # Global project changelog (English)
├── CHANGELOG.es.md            # Global project changelog (Español)
├── LICENSE                    # MIT License (Copyright © 2026 Dev LumiaG5)
└── TUTORIAL.txt               # Step-by-step setup guide
```

---

## 🚀 Quick Start Guide

### 1. On your PC
1. Ensure **Python 3.10+** is installed on Windows.
2. Clone the repository:
   ```bash
   git clone https://github.com/lumiag5/antigravitymb.git
   cd antigravitymb
   ```
3. Run the launcher:
   * Double-click **`Start_Server.bat`** (located in `desktop-bridge/`).
   *(The script verifies dependencies and starts the server, displaying your local IP, HTTPS tunnel, and an ASCII QR Code in the terminal).*

---

### 2. On your Android Device or Emulator

#### Option A: Native Android App (Recommended)
1. Go to [Releases](https://github.com/lumiag5/antigravitymb/releases) or [GitHub Actions Artifacts](https://github.com/lumiag5/antigravitymb/actions) and download `AntigravityMobile-Release-APK`.
2. Install the `.apk` on your phone or drag it into your emulator (e.g., LDPlayer, Nox).
3. Open the app:
   * **Instant Connect**: Tap **`📷 Sign in with QR Code`** and point your camera at the PC terminal!
   * **Resume Work**: If returning after closing the app, tap **`▶ Resume Session`** to jump right in without typing a PIN.

#### Option B: Mobile Browser (PWA)
1. Connect your device to the same Wi-Fi and browse to `http://[PC_IP]:8765`.
2. Or use the secure **`https://*.trycloudflare.com`** URL to monitor remotely over cellular data (4G/5G).
3. Type the 4-digit PIN printed in the PC terminal to authorize the session.

---

## ⌨️ PC Console Hotkeys

While `Start_Server.bat` is running, control the daemon via keyboard shortcuts:
* **`P`**: Generates a new 4-digit security PIN and refreshes the QR Code.
* **`L`**: Instantly switches language (Português &harr; English &harr; Español).
* **`Q`**: Forces an immediate refresh of official quota metrics.
* **`Ctrl + C`**: Safely terminates server and shuts down tunnels.

---

## 📄 License & Attribution

Distributed under the **MIT** license. See [LICENSE](LICENSE) for details.

Developed by **Dev LumiaG5** &bull; Copyright &copy; 2026. All rights reserved.
