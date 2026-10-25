# Changelog

<p align="center">
  <a href="CHANGELOG.md">Português</a> &bull; <b>English</b> &bull; <a href="CHANGELOG.es.md">Español</a>
</p>

All notable changes to **Antigravity Mobile** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Added / Session Management & Camera QR Scanner
* **App Lifecycle Session Guard**: App now automatically returns to the session gateway screen on fresh launch, protecting ongoing monitoring sessions.
* **"Resume Session" Option**: If the desktop bridge is still running on the PC, a single tap resumes monitoring immediately without retyping a PIN.
* **"Sign in with QR Code" Camera Scanner**: Native camera scanner integration (ZXing) with runtime camera permission to scan the terminal's ASCII QR code directly.
* **Zero-Touch QR Authentication**: The PC terminal now encodes the active PIN into the QR code (`?pin=XXXX`), authenticating and connecting immediately upon scanning.
* **"New Session" Option**: Flushes the previous cached token and brings up connection controls to authorize with a fresh PIN.
* **"Disconnect Session" in Settings Menu**: Dedicated logout button added to the `⚙️ Menu` modal.
* **Minimalist OLED Layout**: Removed all previous preset chips for a clean, distraction-free OLED True Black interface.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Fixed / Native Android Application
* **Smart Protocol Deduction (HTTP vs HTTPS)**: Fixed an issue where local network IP connections (e.g. `192.168.0.6:8765` or `10.0.2.2:8765`) were automatically forced into `https://`, causing TLS handshake errors (`Invalid HTTP request received`) and blank black screens. The app now recognizes local subnets and assigns `http://`, reserving `https://` for Cloudflare tunnels and web domains.
* **Auto-Port Completion**: If a local IP is entered without a port, default port `:8765` is appended automatically.
* **One-Tap Quick Presets on Connect Screen**: Added 3 quick-fill preset chips:
  - `💻 Emulator (LDPlayer / Nox)`: Inserts `http://10.0.2.2:8765` (standard host loopback).
  - `📶 Wi-Fi Local (PC)`: Inserts `http://192.168.0.6:8765`.
  - `🌐 Cloudflare Tunnel`: Inserts `https://` for pasting remote tunnels.
* **Clipboard Paste Shortcut**: Added dedicated "📋 Paste" button to paste copied links straight from the device or emulator clipboard with one tap.
* **Detailed Error Diagnostics**: The error view now displays the exact URL attempted, failure reason, and error codes returned by the WebView engine.
* **Legacy WebView Compatibility**: Added dual error interception (modern `WebResourceRequest` and legacy `onReceivedError(int, String, String)`) ensuring status screens appear properly across Android 7 through 14.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Added / UI Enhancements
* **ASCII QR Code in PC Terminal**: Automatic generation of a compact ASCII QR code on the Desktop Bridge console for instant phone camera pairing, bypassing manual URL typing.
* **Unified Settings Menu**: New `⚙️ Menu` button located on the footer (in place of Sound & Flash), bringing together alerts, audio, network, and history settings.
* **Customizable Audio Ringtones**: Choice of 4 ringtone styles synthesized via Web Audio API (*Modern Chime*, *Zen Bell*, *Sci-Fi Pulse*, and *Classic Beep*) with instant preview test button.
* **Volume Slider Control**: Master gain slider (0% to 100%) stored locally in browser storage.
* **Real-Time Latency Meter (Ping in ms)**: Badge next to the Menu button featuring dynamic health coloring (Green <130ms, Amber 130-320ms, Red >320ms) with a toggle to hide or show.
* **Task Completion History (Log)**: History modal logging recently finished tasks with project name, conversation title, active AI model, and exact completion timestamp, plus a clear log button.
* **OLED Button Repositioning**: The `🌓 OLED` button is now situated where Notifications used to be on the footer, streamlining navigation.

---

## [2.3.6] - 2026-10-25 (Build 2417)

### Added / Fixed
* **Real-Time AI Model Detection (Claude, GPT, Gemini)**: The desktop bridge now detects on-the-fly when the developer switches models in the Antigravity IDE (e.g. from Gemini to Claude Sonnet) mid-conversation, without needing server restarts or page refreshes.
* **Protobuf Wire Type Decoding for Claude & GPT**: Added native parsing for Antigravity's field 28 (`\xe2\x01`) used by Claude models, ensuring reliable priority extraction over residual Gemini prompt tags.
* **Dynamic RPC Quota Group Synchronization**: Quota meters (5-hour and weekly limits) automatically toggle between `Gemini Models` and `Claude and GPT models` based on the active model currently running.
* **New `model_changed` WebSocket Event**: Push notification fired directly to mobile clients with the new model name and refreshed quota metrics.
* **Model Propagation in All Message Events**: All user message, completion, and status updates now carry the current `active_model` payload to ensure interface consistency.
* **Lock-Free SQLite Reads (`mode=ro`)**: SQLite summary databases are now opened via read-only URI to prevent WAL lock contention while Antigravity writes active session data.

---

## [2.3.5] - 2026-10-25 (Build 2416)

### Initial Release (First Public Version on GitHub)

Initial official public release of **Antigravity Mobile** for real-time mobile monitoring of Antigravity IDE.

#### Chat & Mobile UI
* **Clean Real-Time Feed**: Strict filtering of internal tool calls, terminal dumps, and intermediate diffs. Displays exclusively the user's prompt and the AI assistant's final conclusion.
* **Markdown & Code Renderer**: Full support for highlighted code blocks, tables, and lists matching the desktop IDE typography (Inter and JetBrains Mono).
* **Smart Auto-Scroll**: Automatically tracks new incoming messages without interrupting if you scroll up to inspect previous output.
* **OLED True Black Mode**: Pure `#000000` background to conserve battery on AMOLED/OLED mobile screens, with high-contrast dark gray user chat bubbles.
* **Safe-Area Layout**: Mobile-optimized layout avoiding overlaps with Android and iOS system navigation bars.

#### Synchronization & Session Intelligence
* **Multi-Source Focus Detection**: Real-time active conversation tracking aggregating presence locks (`presence/*.lock`), protobuf annotations (`annotations/*.pbtxt`), and SQLite databases (`conversation_summaries.db`).
* **Workspace & Conversation Badging**: Responsive header displaying clean project and conversation titles (`📁 Project • Conversation Title`).
* **Background Task Guard**: Continues tracking active tasks (*Working...*) in the background if the user switches to another project on PC, automatically switching and alerting upon completion.
* **Low-Resource Tail-Seek Engine**: Asynchronous tail seek on log files (`transcript.jsonl`), effortlessly handling 40+ MB transcripts with negligible CPU and RAM consumption.

#### Sensory Completion Alerts
* **Screen Flash**: 2 emerald flashes spaced 1 second apart upon task completion.
* **Audio Cue**: Real-time synthesized chime via Web Audio API with boosted gain (+dB) for noisy environments.
* **Haptic Vibration**: Dual vibration pulse for phones in silent mode (Web Vibration API).
* **Web Notifications**: Native OS notification support even when the phone screen is locked.

#### Official AI Quota Metrics
* **Antigravity RPC Integration**: Direct integration with the IDE's local RPC service (`LanguageServerService/RetrieveUserQuotaSummary`) with dynamic port and CSRF discovery.
* **Real-Time Quota Bars**: Exact percentage tracking for both 5-Hour and Weekly Gemini quotas.
* **Renewal Countdown**: Live remaining time until quota reset with localized descriptions.
* **Active Model Tracking**: Real-time identification of the model in use (e.g., *Gemini 3.8 Flash High*).

#### Security, Networking & Access
* **Dynamic PIN Authentication**: Random 4-digit PIN generated in the PC console on first connection.
* **24-Hour Session Cache**: Authorized session cached locally for 24 hours, eliminating repetitive PIN entry on page reloads.
* **Anti-Spam Throttling**: Silent rejection of unauthorized probes and flood prevention on the daemon.
* **Automated HTTPS Tunnel**: Bundled standalone Cloudflare Tunnel binary generating secure public URLs (`https://*.trycloudflare.com`) to enable mobile push notifications without router configuration.

#### Usability & Internationalization
* **Trilingual Support (i18n)**: Full interface and notification localization in Portuguese (Brazil), English, and Spanish.
* **Language Hotkey**: Press `L` in the PC terminal to cycle interface language on the fly.
* **One-Click Startup**: `Start_Server.bat` script for instant Windows launch with automated dependency checking.
* **Zero-Install (PWA)**: Works out of the box in all modern mobile browsers (Chrome, Safari, Firefox, Edge, Opera, Samsung Internet) with "Add to Home Screen" support.
