# Changelog &bull; Antigravity Mobile APK (Android)

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.md">Português</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.en.md">English</a> &bull; <b>Español</b>
</p>

Todos los cambios de la aplicación nativa Android (**Antigravity Mobile APK**) se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.5.0] - 2026-10-29 (Build 2500)

### Añadido
* **Envío remoto de prompts**: Envía instrucciones directamente desde el móvil a Antigravity en la PC (`POST /api/prompt`) con selección de modelo de IA (Gemini 3.8 Flash, Pro, Claude 3.7 Sonnet, GPT-4o, etc.).
* **Atajos rápidos (Snippets)**: Botones interactivos para rellenar el prompt con un toque (🔄 *Continúa*, 🧪 *Ejecuta las pruebas*, 📋 *Resume el progreso*, 🐞 *Verifica errores*).
* **Historial y contador**: Acceso a prompts anteriores con la tecla flecha arriba y contador de caracteres/palabras en tiempo real.
* **Navegación inteligente con botón volver**: Cierra modales jerárquicamente o regresa al chat principal. Pulsar dos veces salir en el inicio cierra la app limpiamente sin abrir la pantalla de sesión por error.
* **Selección y copia nativa de texto**: Se eliminó el interceptor de pulsación prolongada. Mantener presionado el texto activa el menú nativo de Android para seleccionar y copiar.
* **Ahorro de batería y rendimiento**:
  - Ciclo de vida nativo con `onPause`/`onResume` en WebView para detener renderizados de GPU con la pantalla apagada.
  - Pausa de animaciones CSS y temporizadores de red via Page Visibility API (`body.app-paused`).
  - Reconexión WebSocket con retroceso exponencial para no agotar la batería si la PC está apagada.
  - Perfil automático para batería baja (<= 20% sin cargador) desactivando sombras y reduciendo pings.
  - Carga inicial paralelizada con `Promise.allSettled`.
* **Acciones en respuestas**: Botón de copia con confirmación visual (📋 ➔ ✅) y botón para compartir (📤 via Web Share API) directamente a WhatsApp, Telegram o Notas.
* **Indicador animado de pensamiento**: Puntos animados que indican cuando la IA está pensando o procesando tareas.
* **Fijar favoritos**: Botón de estrella (⭐) para mantener conversaciones prioritarias arriba con guardado local.
* **Búsqueda rápida de chats**: Filtro instantáneo por título o proyecto en los modales de Chats y Prompt.

---

## [2.4.4] - 2026-10-28 (Build 2426)

### Añadido
* **Pantalla completa inmersiva**: Ocultación de la barra de estado superior mediante `WindowInsetsControllerCompat`, con soporte para muescas de cámara (*short edges cutout mode*) y margen de seguridad dinámico.
* **Monitor de batería en tiempo real**: Lectura en tiempo real del nivel y estado de carga mediante `BroadcastReceiver` del sistema, visible en el pie de página sin textos innecesarios.
* **Alineación del pie de página**: Botones e indicadores estandarizados con altura uniforme de 28px y esquinas redondeadas.

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Corregido
* **Desplazamiento en el APK**: Eliminación de `SwipeRefreshLayout` en el diseño nativo, permitiendo desplazarse libremente sin bloqueos de gestos.
* **Transición a Completado**: El estado cambia de inmediato a "Completado" en cuanto el modelo finaliza la respuesta.
* **Aviso al abrir historial**: Corregida la notificación errónea de error al abrir conversaciones desde el modal de chats.
* **Eliminación de botones "✕"**: Los modales ahora se cierran al tocar fuera o mediante el botón "Cerrar" en el pie.

### Añadido
* **Sincronización del estado "Pensando..."**: Detección en tiempo real mediante SQLite de la conversación activa, cambiando inmediatamente a "Pensando...".
* **Unificación de Background Task**: Las tareas en segundo plano se integraron en el estado "Ejecutando Tarea...". El estado "Completado" solo se activa cuando no queda actividad pendiente en el proyecto.
* **Botón "Chats"**: Modal para alternar entre conversaciones y proyectos sincronizados de la PC, con indicadores de estado (`🟠` procesando / `🟢` ocioso).
* **Lectura remota de conversaciones**: Permite consultar el historial completo de cualquier conversación en el móvil sin cambiar la pantalla activa en la PC.
* **Insignia de versión del APK**: La cabecera indica si la versión en ejecución es nativa `(APK)` o navegador `(IP)`.
* **Actualizador en el menú**: Opción dentro del menú de la app para buscar, descargar e instalar actualizaciones directamente desde GitHub Releases.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Añadido
* **Escáner de código QR nativo**: Integración de cámara mediante ZXing para escanear el código QR de la terminal con PIN integrado.
* **Gestor de sesión**: La app abre en la pantalla de conexión para proteger el feed activo.
* **Reanudación de sesión**: Botón "Volver a la Sesión" para reconectar al servidor activo sin reingresar el PIN.
* **Opción "Nueva Sesión" y botón "Salir"**: Accesos directos para cambiar de servidor o cerrar sesión desde el menú.
* **Diseño OLED Black**: Eliminación de botones heredados en favor de una interfaz con fondo `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Corregido
* **Protocolo de red (HTTP/HTTPS)**: Aplica `http://` a IPs locales y `https://` solo en túneles y dominios públicos, previniendo errores de TLS.
* **Puerto predeterminado automático**: Añade `:8765` automáticamente cuando se ingresa una IP sin puerto.
* **Gestión de errores en WebView**: Diagnósticos claros de conexión y compatibilidad con Android 7 a 9.

### Añadido
* **Accesos directos**: Botones de autocompletado para emulador, Wi-Fi local y Cloudflare, además de acceso para pegar del portapapeles.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Lanzamiento Inicial del APK
* **Estructura nativa Android**: Proyecto Kotlin con `minSdk = 24` (Android 7.0+) y `targetSdk = 34` (Android 14).
* **WebView acelerado**: Aceleración por hardware, soporte para WebSockets (`/ws`), Web Audio API y tema OLED Black `#000000`.
* **Permisos del sistema**: Notificaciones nativas (`POST_NOTIFICATIONS`) y tráfico limpio en red local (`usesCleartextTraffic`).
* **CI/CD en GitHub Actions**: Compilación y empaquetado automático de versiones APK con cada push o tag.
