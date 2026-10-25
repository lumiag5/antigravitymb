# Antigravity Mobile

<p align="center">
  <a href="README.md">Português</a> &bull; <a href="README.en.md">English</a> &bull; <b>Español</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versión-v2.4.2-blue?style=flat-square" alt="Versión v2.4.2">
  <img src="https://img.shields.io/badge/plataforma-Windows_%7C_Android-success?style=flat-square" alt="Plataformas">
  <img src="https://img.shields.io/badge/android-7.0%2B_%28API_24%2B%29-green?style=flat-square" alt="Android 7+">
  <img src="https://img.shields.io/badge/licencia-MIT-yellow?style=flat-square" alt="Licencia MIT">
  <img src="https://img.shields.io/badge/build-GitHub_Actions_Passing-brightgreen?style=flat-square" alt="GitHub Actions">
</p>

Companion móvil que convierte tu teléfono en una **segunda pantalla inteligente** para **Antigravity IDE** en la PC. Monitorea el progreso del chat de código en tiempo real, recibe alertas sensoriales (sonido personalizable, destellos y vibración) al finalizar cada tarea, consulta el consumo oficial de cuotas de IA (Gemini, Claude Sonnet y GPT) y conéctate con un toque desde la **aplicación nativa de Android** o el navegador.

---

## 🎯 ¿Por qué Antigravity Mobile?

Cuando asignas tareas extensas a Antigravity IDE — como refactorizaciones masivas, generación de componentes, suites de pruebas o depuración compleja —, es normal alejarse del escritorio. El desafío es saber:
- Si el agente de IA terminó o si está esperando una confirmación en la terminal.
- En qué modelo está trabajando el asistente (Gemini, Claude 3.5 Sonnet o GPT-4o).
- Cuánto queda de tu cuota de 5 horas y semanal de IA.

**Antigravity Mobile** conecta tu PC directamente con tu móvil mediante Wi-Fi local o a través de un **túnel HTTPS global (Cloudflare)** seguro sin necesidad de abrir puertos en tu router.

---

## ⚡ Características Principales

### 💬 Chat en Tiempo Real con Filtrado de Ruido
* **Foco en lo relevante**: Antigravity genera cientos de líneas de ejecución interna y terminal. El companion limpia el ruido, mostrando únicamente los prompts y las conclusiones finales del asistente.
* **Renderizado de Markdown y Código**: Resaltado de sintaxis en bloques de código, tablas y tipografía adaptada a la del IDE (fuentes Inter y JetBrains Mono).
* **Auto-Scroll Inteligente**: Sigue el flujo de texto automáticamente y se pausa si te desplazas hacia arriba para revisar el historial.

### 🔔 Alertas Sensoriales de Finalización
* **Doble Destello en Pantalla**: Dos parpadeos verde esmeralda con intervalo de 1 segundo (visibles incluso con el móvil apoyado en la mesa).
* **Sintetizador de Tonos (Web Audio API)**: Elige entre 4 estilos de tonos (*Chime Moderno*, *Campana Zen*, *Pulso Sci-Fi* y *Pitido Clásico*) con control deslizante de volumen (0% a 100%) y botón de prueba.
* **Vibración Táctil**: Patrón de vibración doble para entornos silenciosos o reuniones.
* **Notificaciones Push**: Web Notifications nativas entregadas incluso con la pantalla bloqueada.

### 🧠 Detección en Tiempo Real de Modelos de IA
* **Gemini, Claude y GPT**: Identificación al instante del cambio de modelos durante la conversación mediante decodificación binaria de tags Protobuf (campo 28 `\xe2\x01` para Claude/GPT y campo 19 `\x9a\x01` para Gemini), sin requerir reinicios.

### 📊 Seguimiento Oficial de Cuotas (RPC Interna)
* **Métricas Reales sin Estimaciones**: Conexión directa con el servicio RPC interno de Antigravity (`LanguageServerService/RetrieveUserQuotaSummary`).
* **Sincronización Dinámica de Cuotas**: Alterna automáticamente entre los grupos de cuota `Gemini Models` y `Claude and GPT models` según el modelo en ejecución.
* **Barras de Uso**: Porcentaje de consumo de cuota de 5 Horas y Semanal, con tiempo exacto para la renovación.

### 📶 Medidor de Latencia en Tiempo Real (Ping)
* **Distintivo Dinámico**: Indicador visual junto al menú con round-trip en milisegundos vía WebSocket:
  * 🟢 **Verde**: Latencia óptima (<130ms)
  * 🟡 **Amarillo**: Latencia media (130ms a 320ms)
  * 🔴 **Rojo**: Conexión lenta (>320ms)

### 📜 Historial de Tareas Finalizadas (Log)
* Modal retráctil con el registro de las tareas completadas por el agente, indicando proyecto, título, modelo de IA utilizado y hora exacta de conclusión.

### 📱 Aplicación Nativa Android (APK Kotlin)
Paquete `.apk` independiente con integración profunda en Android:
* **Modo OLED True Black (`#000000`)**: Máximo ahorro de batería en pantallas AMOLED.
* **Cierre Automático de Sesión al Salir**: Pausa la sesión al cerrar la app para total privacidad.
* **▶ Volver a la Sesión (Sin Nuevo PIN)**: Reconexión inmediata si el servidor sigue abierto en la PC, con sesión criptográfica de 24 horas.
* **📷 Entrar con Código QR vía Cámara (ZXing)**: Escáner nativo de cámara integrado para leer el código QR de la terminal de la PC con PIN dinámico incorporado (`?pin=XXXX`) para conexión instantánea sin tocar el teclado.
* **⚡ Nueva Sesión**: Limpia los tokens anteriores para iniciar un nuevo emparejamiento.
* **CI/CD Automatizado**: El APK se compila automáticamente en la nube vía **GitHub Actions**. Consulta el [Changelog exclusivo del APK](android/CHANGELOG.md).

---

## 🛠️ Arquitectura del Proyecto

```text
antigravity-mobile/
├── .github/workflows/
│   └── build-apk.yml          # CI/CD: Compilación automatizada del APK en la nube
├── android/                   # Proyecto Nativo Android (Kotlin / Gradle)
│   ├── app/src/main/
│   │   ├── java/.../MainActivity.kt  # Gestor de Sesión, WebView y ZXing Scanner
│   │   ├── res/layout/activity_main.xml  # Diseño OLED True Black
│   │   └── AndroidManifest.xml
│   └── CHANGELOG.md           # Historial de versiones del APK de Android
├── desktop-bridge/            # Daemon Local para Windows (Python / FastAPI)
│   ├── Start_Server.bat       # Iniciador en 1 clic para Windows
│   ├── run.py                 # CLI con código QR en ASCII y atajos de teclado
│   ├── server.py              # Servidor FastAPI y WebSockets (/ws)
│   ├── auth.py                # Seguridad con PIN de 4 dígitos y sesión de 24h
│   ├── monitor.py             # Decodificador Protobuf y monitor en segundo plano
│   ├── antigravity_api.py     # Cliente RPC para métricas de cuota del IDE
│   ├── tunnel.py              # Administrador de túneles Cloudflare
│   ├── language_manager.py    # Internacionalización (pt, en, es)
│   └── static/                # Companion móvil PWA (HTML5, CSS, JS, Web Audio)
│       ├── index.html         # Panel completo del companion
│       └── manifest.json      # Especificaciones oficiales PWA
├── CHANGELOG.md               # Changelog general del proyecto
├── LICENSE                    # Licencia MIT (Copyright © 2026 Dev LumiaG5)
└── TUTORIAL.txt               # Guía paso a paso de conexión
```

---

## 🚀 Inicio Rápido

### 1. En la Computadora (PC)
1. Asegúrate de tener **Python 3.10+** instalado en Windows.
2. Clona el repositorio:
   ```bash
   git clone https://github.com/lumiag5/antigravitymb.git
   cd antigravitymb
   ```
3. Ejecuta el iniciador:
   * Haz doble clic en **`Start_Server.bat`** (dentro de `desktop-bridge/`).
   *(El script comprobará dependencias e iniciará el servidor mostrando tu IP local, túnel HTTPS y el código QR en ASCII).*

---

### 2. En tu Móvil o Emulador (Android)

#### Opción A: Aplicación Nativa Android (Recomendada)
1. Accede a las [Releases](https://github.com/lumiag5/antigravitymb/releases) o a los [Artefactos de GitHub Actions](https://github.com/lumiag5/antigravitymb/actions) y descarga `AntigravityMobile-Release-APK`.
2. Instala el `.apk` en tu móvil o arrástralo dentro de tu emulador (ej: LDPlayer, Nox).
3. Abre la app:
   * **Conexión Inmediata**: Pulsa en **`📷 Entrar con Código QR`** y apunta la cámara a la terminal de la PC.
   * **Volver a la Sesión**: Si cerraste la app y la PC sigue encendida, pulsa en **`▶ Volver a la Sesión`** para ingresar sin PIN.

#### Opción B: Navegador Móvil (PWA)
1. Conecta el móvil a la misma red Wi-Fi y navega a `http://[IP_DE_LA_PC]:8765`.
2. O utiliza el enlace seguro **`https://*.trycloudflare.com`** para monitorear a distancia con datos móviles (4G/5G).
3. Escribe el PIN de 4 dígitos indicado en la consola de la PC para autorizar el acceso.

---

## ⌨️ Comandos de la Consola de la PC

Durante la ejecución de `Start_Server.bat`:
* **`P`**: Genera un nuevo PIN de seguridad de 4 dígitos y actualiza el código QR.
* **`L`**: Alterna instantáneamente el idioma (Português &harr; English &harr; Español).
* **`Q`**: Fuerza una lectura inmediata de las cuotas oficiales.
* **`Ctrl + C`**: Cierra el servidor y el túnel de forma segura.

---

## 📄 Licencia y Autoría

Distribuido bajo licencia **MIT**. Consulta [LICENSE](LICENSE) para más información.

Desarrollado por **Dev LumiaG5** &bull; Copyright &copy; 2026. Todos los derechos reservados.
