# Antigravity Mobile

<p align="center">
  <a href="README.md">Português</a> &bull; <a href="README.en.md">English</a> &bull; <b>Español</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versión-v2.5.0-blue?style=flat-square" alt="Versión v2.5.0">
  <img src="https://img.shields.io/badge/plataforma-Windows_%7C_Android-success?style=flat-square" alt="Plataformas">
  <img src="https://img.shields.io/badge/android-7.0%2B_%28API_24%2B%29-green?style=flat-square" alt="Android 7+">
  <img src="https://img.shields.io/badge/licencia-MIT-yellow?style=flat-square" alt="Licencia MIT">
  <img src="https://img.shields.io/badge/build-GitHub_Actions_Passing-brightgreen?style=flat-square" alt="GitHub Actions">
</p>

Aplicación móvil y panel web para monitorear las tareas de **Antigravity IDE** desde el teléfono en tiempo real. Muestra el chat filtrado, avisa cuando una tarea finaliza (sonido, parpadeo de pantalla y vibración), consulta cuotas de IA y permite navegar entre proyectos y conversaciones. Funciona mediante Wi-Fi local o túnel Cloudflare, por app nativa Android (APK) o navegador.

---

## Características

### Chat y Navegación
* **Chat en tiempo real**: Muestra las instrucciones del usuario y la respuesta final del asistente, sin registros internos de herramientas.
* **Markdown y código**: Bloques de código con resaltado de sintaxis, tablas y desplazamiento fluido por el historial.
* **Navegador de conversaciones (Chats)**: Lista proyectos y conversaciones de la PC con indicadores de estado (`🟠` procesando / `🟢` en reposo). Permite consultar el historial de cualquier conversación sin cambiar de ventana en la computadora.

### Estados y Alertas
* **Estados en tiempo real**: Muestra la fase actual (*Pensando...*, *Trabajando...*, *Ejecutando Tarea...* y *Completado*).
* **Alertas de finalización**: Emite un tono sonoro (4 opciones con volumen ajustable), parpadea la pantalla dos veces en verde y vibra al terminar la tarea.
* **Monitoreo de cuotas**: Consulta el consumo de cuota de 5 horas y semanal de Antigravity (Gemini, Claude, GPT).
* **Medidor de ping**: Indicador de latencia WebSocket en tiempo real.
* **Batería en tiempo real**: Porcentaje actual de batería ubicado en el centro del pie de página, junto a la latencia, sin textos innecesarios.

### App Android Nativa (APK)
* **Pantalla completa inmersiva**: Oculta la barra de estado superior en el APK y ofrece soporte de pantalla completa en el navegador/IP para mayor enfoque.
* **Modo OLED Black**: Fondo `#000000` para ahorrar batería.
* **Acceso por código QR**: Emparejamiento con la cámara leyendo el código QR de la terminal.
* **Reanudación de sesión**: Opción de volver a la sesión activa sin volver a ingresar el PIN.
* **Actualizador integrado**: Búsqueda e instalación de nuevas versiones directamente desde el menú de la app. Consulta los changelogs del APK: [Português](android/CHANGELOG.md) &bull; [English](android/CHANGELOG.en.md) &bull; [Español](android/CHANGELOG.es.md).

---

## Estructura del Proyecto

```text
antigravity-mobile/
├── .github/workflows/
│   └── build-apk.yml          # CI/CD: compilación automática de APK en GitHub Actions
├── android/                   # App nativa de Android (Kotlin / Gradle)
│   ├── app/src/main/
│   │   ├── java/.../MainActivity.kt  # WebView, cámara ZXing y gestor de sesión
│   │   ├── res/layout/activity_main.xml
│   │   └── AndroidManifest.xml
│   ├── CHANGELOG.md           # Changelog del APK (Português)
│   ├── CHANGELOG.en.md        # Changelog del APK (English)
│   └── CHANGELOG.es.md        # Changelog del APK (Español)
├── desktop-bridge/            # Servidor local para Windows (Python / FastAPI)
│   ├── Start_Server.bat       # Iniciador para Windows
│   ├── run.py                 # CLI con código QR en la terminal
│   ├── server.py              # API FastAPI y WebSocket (/ws)
│   ├── auth.py                # Autenticación por PIN
│   ├── monitor.py             # Monitor de logs y base de datos SQLite del IDE
│   ├── antigravity_api.py     # Cliente RPC para cuotas del IDE
│   ├── tunnel.py              # Túnel Cloudflare para acceso externo seguro
│   ├── language_manager.py    # Internacionalización (pt, en, es)
│   └── static/                # Interfaz web móvil (HTML, CSS, JS)
│       ├── index.html
│       └── manifest.json
├── CHANGELOG.md               # Changelog general (Português)
├── CHANGELOG.en.md            # Changelog general (English)
├── CHANGELOG.es.md            # Changelog general (Español)
├── LICENSE                    # Licencia MIT
└── TUTORIAL.txt
```

---

## Cómo Usar

### 1. En la PC
1. Requiere **Python 3.10+** en Windows.
2. Clona el repositorio:
   ```bash
   git clone https://github.com/lumiag5/antigravitymb.git
   cd antigravitymb
   ```
3. Ejecuta `Start_Server.bat` (dentro de `desktop-bridge/`).
   El script verifica dependencias e inicia la terminal mostrando la IP local, el enlace Cloudflare y el código QR.

### 2. En el Teléfono (Android)

#### Mediante APK Nativo (Recomendado)
1. Descarga el APK desde la sección de [Releases](https://github.com/lumiag5/antigravitymb/releases).
2. Instálalo en el dispositivo.
3. Abre la app y presiona **Entrar con Código QR** apuntando a la terminal de la PC.

#### Mediante el Navegador
1. Conecta el teléfono a la misma red Wi-Fi y accede a `http://[IP_DE_LA_PC]:8765`.
2. Para acceso remoto (datos móviles), usa el enlace `https://*.trycloudflare.com`.
3. Ingresa el PIN de 4 dígitos indicado en la terminal.

---

## Atajos de la Consola

Con el servidor corriendo en la PC:
* **`P`**: Genera un nuevo PIN y actualiza el código QR.
* **`L`**: Cambia el idioma (Português / English / Español).
* **`Q`**: Actualiza las métricas de cuota.
* **`Ctrl + C`**: Detiene el servidor y cierra el túnel.

---

## Licencia

Distribuido bajo licencia **MIT**. Consulta [LICENSE](LICENSE) para más detalles.
