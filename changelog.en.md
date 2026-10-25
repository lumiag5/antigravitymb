# Changelog

<p align="center">
  <a href="changelog.md">Português</a>; <b>English</b> <a href="changelog.en.md">; <a href="CHANGELOG.es.md">Español</a>
</p>

All notable changes to **Antigravity Mobile** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
