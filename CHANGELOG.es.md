# Changelog

<p align="center">
  <a href="CHANGELOG.md">Português</a> &bull; <a href="CHANGELOG.en.md">English</a> &bull; <b>Español</b>
</p>

Todos los cambios notables de **Antigravity Mobile** se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.4.3] - 2026-10-27 (Build 2421)

### 🐛 Corregido
* **Desplazamiento Vertical del Chat en el APK**: Corregido el problema donde no era posible desplazarse hacia arriba para ver mensajes anteriores. Se eliminó `SwipeRefreshLayout` del diseño nativo (`activity_main.xml`), permitiendo que `WebView` maneje los eventos táctiles directamente sin intercepción.
* **Directivas Táctiles en el Feed Web**: Añadidos `-webkit-overflow-scrolling: touch; touch-action: pan-y; overscroll-behavior-y: contain;` para suavidad táctil total en navegadores móviles.

### 🚀 Añadido
* **Botón Central "Chats" en el Pie de Página**:
  * Ubicado en el centro inferior de la pantalla (entre Menú/Latencia y el botón OLED).
  * Abre un modal con todas las conversaciones y proyectos sincronizados de Antigravity PC (tanto en APK como en Web/IP).
* **Indicadores Pulsantes Estrictos (Sin Texto al Frente)**:
  * Si la conversación está procesando: muestra **solamente un punto pulsante naranja (`🟠`)**, sin texto ni mensaje al frente.
  * Si la conversación está ociosa: muestra **solamente un punto pulsante verde (`🟢`)**, sin texto ni mensaje al frente.
* **Inspección Remota Totalmente Independiente**:
  * Al seleccionar cualquier chat en el móvil, carga todo el historial completo de mensajes sin modificar la ventana ni la conversación activa en la PC.
  * Botón "Volver a la PC en Vivo" para retomar la sincronización en tiempo real con un toque.
* **Nuevos Estados "Trabajando...", "Pensando..." y "Ejecutando Tarea..."**:
  * "Procesando" renombrado a **"Trabajando..."** (*Working*).
  * Añadido estado **"Pensando..."** (*Thought*).
  * Añadido estado **"Ejecutando Tarea..."** (*Task Running*) con indicador cian pulsante (`#0ea5e9`) para comandos en segundo plano, subagentes y automatizaciones.
  * Al finalizar tareas, el estado muestra **"Completado"** (*Done*) durante **1 minuto** antes de regresar a "Conectado" (o hasta que comience una nueva actividad).
  * Traducciones completas en español, portugués e inglés.
* **Diferenciación de Versión en Encabezado (APK vs IP)**:
  * El distintivo de versión ahora detecta si está en el APK nativo (`vX.X.X (APK) • Dev LumiaG5`) o en el navegador por IP (`v2.4.3 (IP) • Dev LumiaG5`).
* **Actualización Automática de APK en el Menú (Exclusivo Android)**:
  * Nueva sección en el modal `⚙️ Menú` para comprobar nuevas versiones en GitHub Releases y descargar/instalar con 1 toque mediante `FileProvider`.
* **Auditoría de Seguridad**:
  * Confirmación de cero credenciales o tokens en código o historial Git.
  * Sanitización contra *Path Traversal* en endpoints del servidor.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Añadido / Gestión de Sesión y Escáner de Cámara QR
* **Protección de Sesión al Cerrar**: La app ahora siempre inicia en la pantalla de sesión al abrirse, pausando el feed activo por seguridad.
* **Opción "Volver a la Sesión"**: Si el servidor ya fue configurado y sigue abierto en la PC, un solo toque reconecta al dashboard sin pedir nuevo PIN.
* **Opción "Entrar con Código QR" vía Cámara Nativa**: Integración con escáner de cámara nativo (ZXing) con solicitud de permisos en tiempo de ejecución.
* **Autenticación Automática por QR**: El código QR de la terminal ahora incluye el PIN dinámico (`?pin=XXXX`), permitiendo conexión y autorización inmediata.
* **Opción "Nueva Sesión"**: Limpia el token anterior y permite ingresar con un nuevo PIN o cambiar de servidor.
* **Botón "Cerrar Sesión" en el Menú**: Botón directo en `⚙️ Menú` para desconectar y volver a la pantalla de sesión.
* **Diseño Minimalista OLED**: Eliminados todos los botones antiguos de atajos para una interfaz limpia en OLED Black `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Corregido / Aplicación Android Nativa
* **Deducción Inteligente de Protocolo (HTTP vs HTTPS)**: Corrección del error donde las conexiones a IPs locales (ej: `192.168.0.6:8765` o `10.0.2.2:8765`) se forzaban a `https://`, causando fallos de handshake TLS (`Invalid HTTP request received`) y pantalla negra. La app ahora detecta redes locales y aplica `http://`, reservando `https://` para túneles Cloudflare y dominios públicos.
* **Auto-completado de Puerto**: Al ingresar una IP local sin puerto, se añade automáticamente `:8765`.
* **Accesos Rápidos en Pantalla de Conexión**: 3 botones de selección rápida con un toque:
  - `💻 Emulador (LDPlayer / Nox)`: Inserta `http://10.0.2.2:8765` (loopback estándar hacia el PC anfitrión).
  - `📶 Wi-Fi Local (PC)`: Inserta `http://192.168.0.6:8765`.
  - `🌐 Túnel Cloudflare`: Inserta `https://` para ingresar fácilmente el enlace remoto.
* **Botón "Pegar Enlace" del Portapapeles**: Acceso directo para pegar el link desde el portapapeles del dispositivo o emulador.
* **Diagnóstico Detallado de Errores**: La pantalla de error muestra la URL exacta intentada y el motivo/código devuelto por WebView.
* **Compatibilidad con Emuladores Android**: Soporte de intercepción de errores doble para total compatibilidad desde Android 7 hasta Android 14.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Añadido / Mejoras de Interfaz
* **Código QR en la Terminal de la PC**: Dibujo automático de un código QR en ASCII en la consola del Desktop Bridge para emparejamiento inmediato con la cámara del móvil, sin necesidad de escribir la URL.
* **Menú de Configuración Unificado**: Nuevo botón `⚙️ Menú` en el pie de página (en lugar de Sonido y Flash), agrupando alertas, audio, red e historial.
* **Selector de Tonos Personalizados**: 4 estilos de tonos sintetizados mediante Web Audio API (*Chime Moderno*, *Campana Zen*, *Pulso Sci-Fi* y *Pitido Clásico*) con botón de prueba instantánea.
* **Control Deslizante de Volumen**: Ajuste de volumen (0% a 100%) guardado automáticamente en el almacenamiento local.
* **Indicador de Latencia en Tiempo Real (Ping en ms)**: Distintivo dinámico junto al botón Menú con indicador de color (Verde <130ms, Amarillo 130-320ms, Rojo >320ms) y opción para mostrar u ocultar.
* **Historial de Tareas Completadas (Log)**: Ventana de historial que registra las tareas finalizadas con proyecto, título, modelo de IA y hora exacta, además de botón de borrado.
* **Reposicionamiento del Botão OLED**: El botón `🌓 OLED` ahora se encuentra en la posición donde estaba Notificaciones en el pie de página.

---

## [2.3.6] - 2026-10-25 (Build 2417)

### Añadido / Corregido
* **Detección en Tiempo Real de Modelos de IA (Claude, GPT, Gemini)**: El daemon identifica al instante si el desarrollador cambia el modelo de IA en Antigravity IDE (ej.: alternando de Gemini a Claude Sonnet) durante la conversación, sin necesidad de reiniciar el servidor ni recargar la pantalla.
* **Decodificación Protobuf Específica para Claude y GPT**: Soporte para el campo binario 28 (`\xe2\x01`) usado por Antigravity para modelos Claude y GPT, priorizando su detección sobre cadenas residuales en prompts anteriores.
* **Sincronización Dinámica de Grupos de Cuota RPC**: Los medidores de uso (5 horas y semanal) se adaptan automáticamente entre los grupos de cuota `Gemini Models` y `Claude and GPT models` según la familia del modelo activo.
* **Nuevo Evento WebSocket `model_changed`**: Notificación push en tiempo real a la interfaz móvil con el nombre del modelo actualizado y los nuevos valores de cuota.
* **Propagación del Modelo en Todos los Eventos**: Todos los eventos de mensajes, conclusiones y estado incluyen el `active_model` para garantizar consistencia visual continua.
* **Acceso SQLite de Solo Lectura (`mode=ro`)**: Conexión con base de datos de resúmenes en modo URI de solo lectura para evitar contención de bloqueos WAL mientras el IDE escribe.

---

## [2.3.5] - 2026-10-25 (Build 2416)

### Lanzamiento Inicial (Primera Versión Pública en GitHub)

Primera versión pública oficial de **Antigravity Mobile** para la monitorización remota de Antigravity IDE en tiempo real desde el móvil.

#### Chat e Interfaz Móvil
* **Feed en Tiempo Real Limpio**: Filtrado estricto de llamadas a herramientas internas, volcados de terminal y diferencias intermedias. Muestra únicamente la solicitud del usuario y la conclusión final del asistente de IA.
* **Renderizado de Markdown y Código**: Compatibilidad con bloques de código resaltados, tablas y listas que coinciden con la tipografía del IDE en el PC (Inter y JetBrains Mono).
* **Auto-Scroll Inteligente**: Sigue las nuevas respuestas automáticamente, pausándose si te desplazas hacia arriba para revisar el historial anterior.
* **Modo OLED Black Puro**: Fondo `#000000` para ahorro máximo de batería en pantallas AMOLED/OLED y burbuja del usuario adaptada a gris oscuro de alto contraste.
* **Diseño Anti-Corte**: Interfaz responsiva adaptada a las safe areas de los móviles para evitar solapamientos con las barras de navegación de Android e iOS.

#### Sincronización e Inteligencia de Sesión
* **Detección Multi-Fuente de Foco**: Monitorización activa de conversaciones agregando bloqueos de presencia (`presence/*.lock`), anotaciones protobuf (`annotations/*.pbtxt`) y base de datos SQLite (`conversation_summaries.db`).
* **Identificación de Proyecto y Conversación**: Cabecera móvil con distintivo legible que muestra el proyecto y el título de la conversación (`📁 Proyecto • Título de la Conversación`).
* **Vigilancia en Segundo Plano (Background Task Guard)**: Monitorización continua de tareas en ejecución (*Working...*) si el usuario cambia de conversación en el PC, notificando y alternando automáticamente al concluir.
* **Motor Tail-Seek de Bajo Consumo**: Lectura asíncrona optimizada de los últimos bytes de los archivos de registro (`transcript.jsonl`), gestionando historiales de más de 40 MB con un consumo despreciable de CPU y memoria RAM.

#### Alertas Sensoriales de Conclusión
* **Destello en Pantalla**: 2 parpadeos en verde esmeralda separados por 1 segundo al finalizar la tarea.
* **Aviso Sonoro**: Tono sintetizado en tiempo real en el navegador mediante Web Audio API con volumen reforzado (+dB) para entornos con ruido.
* **Vibración Háptica**: Patrón de doble pulso táctil para teléfonos en modo silencio (Web Vibration API).
* **Notificaciones del Sistema**: Notificaciones nativas del sistema operativo incluso con la pantalla bloqueada.

#### Métricas Oficiales de Cuotas
* **Integración RPC con Antigravity**: Conexión directa con la API interna del IDE (`LanguageServerService/RetrieveUserQuotaSummary`) con descubrimiento dinámico de puerto y token CSRF.
* **Barras de Consumo en Tiempo Real**: Monitorización exacta del consumo porcentual de la cuota de 5 Horas y Semanal del modelo Gemini.
* **Cuenta Regresiva de Renovación**: Tiempo exacto restante para el reinicio de la cuota con descripciones localizadas.
* **Identificación de Modelo Activo**: Detección del modelo en ejecución (ej.: *Gemini 3.8 Flash High*).

#### Seguridad, Red y Acceso
* **Autenticación por PIN Dinámico**: Generación de un PIN aleatorio de 4 dígitos en la consola del PC en la primera conexión.
* **Caché de Sesión de 24 Horas**: Sesión autorizada guardada localmente durante 24 horas en el navegador para evitar introducir el PIN repetidamente al recargar la página.
* **Protección Anti-Spam**: Drenaje silencioso de intentos no autorizados y limitación de peticiones abusivas en el demonio.
* **Túnel HTTPS Automático**: Binario standalone oficial de Cloudflare Tunnel integrado, generando enlaces públicos seguros (`https://*.trycloudflare.com`) para permitir notificaciones push móviles sin abrir puertos en el router.

#### Usabilidad e Internacionalización
* **Soporte Trilingüe (i18n)**: Interfaz y notificaciones localizadas en portugués (Brasil), inglés y español.
* **Atajo de Idioma**: Tecla `L` en la consola del PC para alternar el idioma de la interfaz al instante.
* **Arranque en 1 Clic**: Script `Start_Server.bat` para inicio automático en Windows con comprobación de dependencias.
* **Zero-Install (PWA)**: Compatible con cualquier navegador móvil moderno (Chrome, Safari, Firefox, Edge, Opera, Samsung Internet) y opción de añadir a la pantalla de inicio.
