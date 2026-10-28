# Antigravity Mobile

<p align="center">
  <a href="README.md">Português</a> &bull; <b>English</b> &bull; <a href="README.es.md">Español</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v2.4.4-blue?style=flat-square" alt="Version v2.4.4">
  <img src="https://img.shields.io/badge/platform-Windows_%7C_Android-success?style=flat-square" alt="Platforms">
  <img src="https://img.shields.io/badge/android-7.0%2B_%28API_24%2B%29-green?style=flat-square" alt="Android 7+">
  <img src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/build-GitHub_Actions_Passing-brightgreen?style=flat-square" alt="GitHub Actions">
</p>

Mobile app and web dashboard for monitoring **Antigravity IDE** tasks in real time from your phone. Displays filtered chat output, notifies you when a task completes (audio chime, screen flash, vibration), tracks AI quota usage, and lets you browse conversations and projects. Works over local Wi-Fi or Cloudflare tunnels via native Android app (APK) or browser.

---

## Features

### Chat & Navigation
* **Real-time chat**: Shows user prompts and final assistant responses without clutter from intermediate tool logs.
* **Markdown & code**: Syntax-highlighted code blocks, tables, and smooth message scrolling.
* **Conversations browser (Chats)**: Lists PC conversations and projects with live status dots (`🟠` working / `🟢` idle). Inspect message history from your phone without switching windows on your PC.

### Status & Alerts
* **Live status**: Displays current task phase (*Thinking...*, *Working...*, *Task Running...*, and *Done*).
* **Completion alerts**: Plays an audio chime (4 selectable sounds with volume control), flashes the screen green twice, and vibrates when a task finishes.
* **Quota tracking**: Reads 5-hour and weekly quotas directly from the Antigravity service (Gemini, Claude, GPT).
* **Ping indicator**: Real-time WebSocket latency badge.
* **Real-time battery level**: Current battery percentage displayed in the center of the footer next to latency, keeping the UI clean.

### Native Android App (APK)
* **Immersive fullscreen**: Hides top system status bars on APK and supports fullscreen mode in browsers/IP for full visual focus.
* **OLED True Black**: Deep `#000000` background for battery efficiency.
* **QR Code pairing**: One-tap sign in via camera scanner reading the PC console QR code.
* **Session resume**: Reconnect to active sessions without retyping the PIN.
* **In-app updater**: Check and install new releases directly from the settings menu. See APK changelogs: [Português](android/CHANGELOG.md) &bull; [English](android/CHANGELOG.en.md) &bull; [Español](android/CHANGELOG.es.md).

---

## Project Structure

```text
antigravity-mobile/
├── .github/workflows/
│   └── build-apk.yml          # CI/CD: Automated APK build via GitHub Actions
├── android/                   # Native Android app (Kotlin / Gradle)
│   ├── app/src/main/
│   │   ├── java/.../MainActivity.kt  # WebView, ZXing camera, session manager
│   │   ├── res/layout/activity_main.xml
│   │   └── AndroidManifest.xml
│   ├── CHANGELOG.md           # APK changelog (Português)
│   ├── CHANGELOG.en.md        # APK changelog (English)
│   └── CHANGELOG.es.md        # APK changelog (Español)
├── desktop-bridge/            # Local Windows server (Python / FastAPI)
│   ├── Start_Server.bat       # Windows launcher
│   ├── run.py                 # CLI with terminal QR Code
│   ├── server.py              # FastAPI & WebSocket (/ws) server
│   ├── auth.py                # PIN authentication
│   ├── monitor.py             # Log & SQLite watcher for Antigravity IDE
│   ├── antigravity_api.py     # RPC client for IDE quota metrics
│   ├── tunnel.py              # Cloudflare tunnel manager
│   ├── language_manager.py    # Localization (pt, en, es)
│   └── static/                # Web frontend (HTML, CSS, JS)
│       ├── index.html
│       └── manifest.json
├── CHANGELOG.md               # Main changelog (Português)
├── CHANGELOG.en.md            # Main changelog (English)
├── CHANGELOG.es.md            # Main changelog (Español)
├── LICENSE                    # MIT License
└── TUTORIAL.txt
```

---

## Getting Started

### 1. On your PC
1. Requires **Python 3.10+** on Windows.
2. Clone the repository:
   ```bash
   git clone https://github.com/lumiag5/antigravitymb.git
   cd antigravitymb
   ```
3. Run `Start_Server.bat` (inside `desktop-bridge/`).
   Dependencies are checked automatically and the terminal displays the local URL, Cloudflare tunnel, and QR code.

### 2. On your Phone (Android)

#### Native APK (Recommended)
1. Download the APK from [Releases](https://github.com/lumiag5/antigravitymb/releases).
2. Install it on your device.
3. Open the app and tap **Sign in with QR Code** pointing at your PC terminal.

#### Mobile Browser
1. Connect to the same Wi-Fi network and open `http://[PC_IP]:8765`.
2. For remote access (mobile data), use the `https://*.trycloudflare.com` link.
3. Enter the 4-digit PIN shown on the PC terminal.

---

## Console Shortcuts

While the server is running on the PC:
* **`P`**: Generate a new PIN and update the QR code.
* **`L`**: Toggle language (Português / English / Español).
* **`Q`**: Refresh quota metrics.
* **`Ctrl + C`**: Stop server and close the tunnel.

---

## License

Distributed under the **MIT** License. See [LICENSE](LICENSE) for details.
