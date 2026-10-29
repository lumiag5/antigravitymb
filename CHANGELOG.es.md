# Changelog

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.md">Português</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.en.md">English</a> &bull; <b>Español</b>
</p>

Todos los cambios notables de **Antigravity Mobile** se documentan en este archivo.

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
* **Pantalla completa inmersiva**: Ocultación de la barra de estado superior en el APK de Android (con soporte para muescas de cámara *notch*), y modo pantalla completa en el navegador/IP mediante toque o desde el menú de ajustes.
* **Nivel de batería en tiempo real**: Indicador centrado en el pie de página (entre latencia y chats) mostrando el porcentaje de batería y estado de carga, sin textos innecesarios.
* **Diseño armonizado del pie de página**: Alineación simétrica y uniforme de todos los botones e indicadores en una sola fila, con esquinas redondeadas y soporte para el tema OLED.

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Corregido
* **Desplazamiento en el APK**: Eliminación de `SwipeRefreshLayout` en Android, permitiendo desplazarse libremente por el chat sin bloqueos de gestos.
* **Eliminación de botones "✕"**: Los modales ahora se cierran al tocar fuera o mediante el botón "Cerrar" en el pie.

### Añadido
* **Botón "Chats"**: Modal para alternar entre conversaciones y proyectos sincronizados de la PC, con indicadores de estado (`🟠` procesando / `🟢` ocioso).
* **Lectura remota de conversaciones**: Permite ver el historial completo de cualquier conversación en el móvil sin cambiar la pantalla activa en la PC.
* **Estados en tiempo real**: Se añadieron los estados *Pensando...*, *Trabajando...*, *Ejecutando Tarea...* (con punto cian) y *Completado* (visible durante 1 minuto al finalizar).
* **Identificación de versión**: La cabecera ahora indica si la versión en ejecución es nativa `(APK)` o navegador `(IP)`.
* **Actualización del APK en el menú**: Opción en el menú para descargar e instalar nuevas versiones directamente desde GitHub Releases.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Añadido
* **Acceso con Código QR**: Escáner de cámara nativo (ZXing) en el APK para leer el código QR de la terminal con PIN integrado.
* **Reconexión de sesión**: Botón "Volver a la Sesión" para reconectar al servidor activo sin tener que reingresar el PIN.
* **Opción "Nueva Sesión" y botón "Salir"**: Accesos rápidos para cambiar de servidor o cerrar sesión desde el menú.
* **Pantalla de sesión inicial**: La app abre en la pantalla de conexión para proteger el feed activo.
* **Diseño limpio**: Eliminación de accesos directos heredados en favor del tema OLED Black `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Corregido
* **Ajuste de protocolo (HTTP/HTTPS)**: Uso de `http://` en IPs locales y `https://` solo en túneles y dominios públicos, evitando errores de TLS.
* **Puerto predeterminado automático**: Añade `:8765` automáticamente si se ingresa una IP sin puerto.
* **Gestión de errores en WebView**: Diagnóstico más claro de fallos de conexión y compatibilidad con Android 7 a 9.

### Añadido
* **Accesos rápidos de conexión**: Botones directos para emulador (`10.0.2.2`), Wi-Fi local y Cloudflare, además de botón para pegar desde el portapapeles.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Añadido
* **Código QR en la terminal**: Visualización de código QR ASCII en la consola para emparejamiento rápido con la cámara del móvil.
* **Menú de configuración**: Preferencias de alertas, audio, red e historial unificadas en un único menú en el pie de página.
* **Personalización de audio**: 4 tonos de alerta y barra de volumen con guardado local.
* **Medidor de ping**: Indicador visual de latencia WebSocket junto al menú.
* **Historial de tareas**: Modal con registro de tareas finalizadas recientemente (proyecto, modelo y hora).

---

## [2.3.6] - 2026-10-25 (Build 2417)

### Añadido
* **Cambio de modelo en tiempo real**: Detección automática del cambio de modelo de IA (Gemini, Claude, GPT) mediante decodificación Protobuf.
* **Conmutación de cuotas**: Las barras de cuota alternan dinámicamente entre Gemini y Claude/GPT según el modelo en uso.
* **Conexión SQLite en solo lectura**: Uso de `mode=ro` para evitar bloqueos de base de datos mientras el IDE escribe.

---

## [2.3.5] - 2026-10-25 (Build 2416)

### Lanzamiento Inicial
* **Monitoreo de chat**: Feed en tiempo real con mensajes del usuario y respuestas finales del asistente.
* **Renderizado**: Soporte para Markdown, bloques de código resaltados y tema oscuro OLED.
* **Alertas**: Notificaciones al terminar tareas con sonido, doble parpadeo de pantalla y vibración.
* **Cuotas**: Monitoreo de cuotas de 5 horas y semanal desde la API de Antigravity.
* **Conexión segura**: Vinculación por PIN de 4 dígitos (sesión de 24h) y túnel Cloudflare para acceso remoto.
* **Idiomas**: Soporte completo para Portugués, Inglés y Español.
