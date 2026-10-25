# Antigravity Mobile

<p align="center">
  <a href="README.md">Português</a> &bull; <b>English</b> &bull; <a href="README.es.md">Español</a>
</p>

Lightweight mobile companion monitor for **Antigravity IDE**. Track real-time AI reasoning, receive sensory alerts (sound/flash/vibration) when coding tasks finish, and check your official Gemini quota consumption directly in your phone's browser — no app store installation required.

---

## Motivation

When you give Antigravity a heavy task — like refactoring a large module, scaffolding multiple components, or running end-to-end tests —, you usually step away from your desk to grab a coffee or relax on the couch. The catch? You have no idea when the agent finishes, whether it's waiting for terminal confirmation, or if your 5-hour quota just hit its limit. Getting up every few minutes or constantly Alt-Tabbing kills your focus.

**Antigravity Mobile** fixes this with a tiny local daemon (Python) running on your PC that connects to your phone over local Wi-Fi or a secure HTTPS tunnel. It delivers a fast, dark (OLED-friendly) web interface designed for phone screens, letting you know the moment your task is done.

---

## Features

### Real-Time Chat & Noise Filtering
* **Focus on what matters**: Antigravity spits out hundreds of lines of internal tool calls, diffs, and terminal outputs. The companion filters all the noise, showing only the prompt sent and the assistant's final response.
* **Markdown & Code**: Clean rendering with highlighted code blocks, formatted lists, and tables using IDE-matching typography (Inter and JetBrains Mono).
* **Smart Auto-Scroll**: Automatically tracks new incoming messages without interrupting if you scroll up to inspect previous output.

### Automatic Project & Conversation Switching
* **Live Focus Detection**: The server monitors workspace presence locks (`presence/`), SQLite databases, and protobuf metadata. The second you click on another conversation or workspace on your PC, the phone updates instantly (`📁 Project • Conversation Title`).
* **Background Task Guard**: If you switch to another project on your PC while a task is still executing (*Working...*), the server keeps tracking the original task in the background and notifies you once it completes.

### Completion Alerts
The moment the AI agent finishes running:
* **Screen Flash**: 2 emerald flashes spaced 1 second apart (noticeable even with your phone lying on the desk).
* **Audio Cue**: Subtle chime synthesized directly in the browser via Web Audio API with boosted gain (+dB) for noisy environments.
* **Haptic Vibration**: Dual vibration pulse for phones in silent mode.
* **OS Notifications**: Native Web Notifications support with screen locked.

### Official AI Quota Tracking (Internal RPC)
* **No token guesswork**: Connects directly to Antigravity's local RPC service (`LanguageServerService/RetrieveUserQuotaSummary`), discovering port and CSRF tokens automatically.
* **Real usage stats**: Visual progress bars showing exact consumption for both **5-Hour** and **Weekly** quotas, precise renewal countdowns, and active model name (e.g., *Gemini 3.8 Flash High*).

### OLED True Black Mode
* Pure `#000000` background to conserve battery on AMOLED/OLED displays.
* User message bubble styled in high-contrast dark gray for strain-free reading in dark environments.

### PIN Security & 24h Session Cache
* A random 4-digit PIN is displayed in the PC terminal on your first connection.
* Once paired, the session is cached locally for 24 hours — reload or switch tabs without having to type the PIN every time.
* Built-in brute-force throttle and silent rejection logging on the server daemon.

### Automatic HTTPS Tunnel (Cloudflare)
* Bundled with the official standalone Cloudflare Tunnel binary.
* Automatically provisions a temporary secure URL (`https://*.trycloudflare.com`), enabling Web Push Notifications on mobile Chrome/Android without self-signed SSL hassle or router port forwarding.

### Multi-Language Support
* Available in **Portuguese (Brazil)**, **English**, and **Spanish**.
* Switch language anytime directly in the PC console by pressing the **`L`** key.

---

## Quick Start

### Prerequisites
* **Windows 10 or 11** with Antigravity IDE running.
* **Python 3.10 or higher** installed and added to PATH.
* Mobile phone on the same Wi-Fi network (or using the generated HTTPS link).

### Running the Server

1. Clone the repository:
   ```bash
   git clone https://github.com/LumiaG5/antigravity-mobile.git
   cd antigravity-mobile
   ```

2. Start the server:
   * Double-click `antrigavitymb/Start_Server.bat`; **OR**
   * Via terminal:
     ```bash
     cd antrigavitymb/desktop-bridge
     pip install -r requirements.txt
     python run.py
     ```

3. Connect with your Phone:
   The console will display the available connection URLs:
   ```text
   ====================================================================
           [*] ANTIGRAVITY MOBILE - DESKTOP BRIDGE SERVER
                    Developed by Dev LumiaG5
   ====================================================================
    * Local PC:              http://localhost:8765
    * Mobile (Wi-Fi):        http://192.168.0.X:8765
    * Mobile (Secure HTTPS): https://your-tunnel.trycloudflare.com
    * Active Language:       English
   --------------------------------------------------------------------
    ACCESS PIN:              [ 4821 ]
   ====================================================================
   ```
   * Open the link in your phone's browser (HTTPS is recommended for notifications).
   * Enter the 4-digit PIN displayed in the terminal.
   * *(Optional)* In your mobile browser menu, tap **"Add to Home Screen"** to run full-screen as a PWA.

---

## Terminal Shortcuts

While the daemon is running in the PC console, you can use these shortcuts:

| Key | Action |
| :--- | :--- |
| **Any key** | Generates a new random PIN to pair another device |
| **`L`** | Cycles the interface language (Portuguese / English / Spanish) |
| **`Ctrl + C`** | Cleanly terminates the server and shuts down the tunnel |

---

## Repository Structure

```
antrigavitymb/
├── desktop-bridge/            # Python Daemon (FastAPI + WebSockets)
│   ├── run.py                 # Interactive terminal runner and keyboard listeners
│   ├── server.py              # REST routes and WebSocket streaming channels
│   ├── monitor.py             # Transcript tail-seeking parser, locks, and SQLite inspector
│   ├── auth.py                # PIN verification and session cache (24h TTL)
│   ├── language_manager.py    # Multi-language dictionary manager (pt, en, es)
│   ├── tunnel.py              # Cloudflare Tunnel integration
│   ├── antigravity_api.py     # Local RPC client for quota retrieval
│   ├── config.py              # Windows directory auto-discovery
│   ├── bin/cloudflared.exe    # Standalone secure tunnel binary
│   └── static/
│       ├── index.html         # Web Companion Frontend (HTML5 / CSS3 / Vanilla ES6)
│       └── antigravity-icon.png
├── mobile-app/                # React Native / Expo base (for standalone APK build)
├── Start_Server.bat           # 1-click Windows startup script
└── COMO_CONECTAR.txt          # Quick connection guide in 3 languages
```

---

## FAQ

**Do I need to build the APK to use this?**  
No. The Web Companion runs straight in your mobile browser (Chrome, Safari, Firefox, Edge, Opera, Samsung Internet) with full support for sound, vibration, and push alerts without installing an APK.

**Does it work on iPhone / iOS?**  
Yes. In iOS Safari, the dashboard, alerts, and OLED mode work out of the box. To receive alerts with the screen locked on iOS, choose "Add to Home Screen".

**Does Antigravity need to remain open on PC?**  
Yes. The daemon monitors the live log files and RPC services generated by Antigravity IDE during your session.

**Is the HTTPS tunnel secure?**  
Yes. It uses Cloudflare's edge network with end-to-end TLS encryption. No router ports need to be forwarded, and all endpoints are protected by the 4-digit PIN authentication.

---

## Author

Developed by **Dev LumiaG5**  
GitHub: [@LumiaG5](https://github.com/LumiaG5)

---

## License

This project is licensed under the [MIT License](LICENSE.txt). See the `LICENSE.txt` file for full legal terms.
