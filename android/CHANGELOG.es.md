# Changelog &bull; Antigravity Mobile APK (Android Nativo)

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.md">Português</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.en.md">English</a> &bull; <b>Español</b>
</p>

Todos los cambios notables, correcciones de errores y nuevas funciones dedicadas exclusivamente a la aplicación nativa de Android (**Antigravity Mobile APK**) se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### ⚡ Sincronización en Tiempo Real (Thinking) & Transición Completado (Done)
* **Corrección de Transición a "Done" (Completado)**:
  * Se eliminó el bloqueo que mantenía a la aplicación atascada en *"Ejecutando Tarea"* tras haberse completado las tareas y pruebas en la PC.
  * El monitor ahora reconoce la conclusión final del modelo inmediatamente, transicionando con exactitud a **"Completado"** (*Done*), activando el timbre de audio suave, el doble destello de pantalla y el temporizador de 1 minuto.
* **Detección Instantánea del Estado "Pensando..." (*Thinking*)**:
  * Implementada lectura directa y en tiempo real de los pasos de ejecución en la base de datos SQLite de la conversación activa (`conversations/<conv_id>.db`).
  * En cuanto se envía una solicitud y Antigravity PC entra en modo **"Thinking..."**, la app móvil conmuta **instantáneamente** a **"Pensando..."** (*Thought* / *Thinking* con punto púrpura pulsante `#a855f7`), eliminando demoras y logrando sincronización visual inmediata.

### ⚙️ Unificación de Background Task & Criterio Riguroso de Conclusión (Done)
* **Unificación de "Background Task" con "Task Running"**:
  * Las tareas en segundo plano de Antigravity PC (*Background Task*, subagentes `invoke_subagent`, temporizadores `schedule`, comandos `manage_task` y procesos asíncronos de shell) quedan unificadas exactamente bajo el mismo estado visual y sonoro de **"Ejecutando Tarea..."** (*Task Running...* / *Executando Tarefa...*).
  * Indicador visual: punto cian eléctrico pulsante (`#0ea5e9`).
* **Criterio Estricto para el Estado "Completado" (*Done*)**:
  * El estado **"Completado"** (*Done*) ahora **ÚNICAMENTE SE DECLARA** cuando no existe absolutamente ninguna actividad en ejecución en el proyecto actual (`conversation_summaries.db`: `status == 'CASCADE_RUN_STATUS_IDLE'` y `not_fully_idle == 0`, sin logs activos en `.system_generated/tasks/` y sin subagentes en progreso).
  * Mientras haya cualquier tarea activa en segundo plano en el proyecto, el estado permanece en `TASK_RUNNING` ("Ejecutando Tarea..."). Al concluir la totalidad de actividades, el estado pasa a `DONE` ("Completado"), emitiendo la alerta sonora y activando el temporizador de 1 minuto.

### 🐛 Correcciones de Desplazamiento & Gestos
* **Corrección Definitiva del Desplazamiento de Chat en APK**:
  * Eliminación completa de `SwipeRefreshLayout` en el diseño nativo (`activity_main.xml`) y de sus escuchas en `MainActivity.kt`.
  * Debido a que la interfaz web tiene altura fija (100vh) con desplazamiento interno en `#chat-feed`, `SwipeRefreshLayout` interceptaba erróneamente los gestos táctiles hacia abajo (`canScrollVertically(-1) == false`), bloqueando el desplazamiento e impidiendo que el usuario leyera mensajes anteriores.
  * `WebView` ahora reside directamente dentro de `FrameLayout` con `isVerticalScrollBarEnabled = true` y `OVER_SCROLL_IF_CONTENT_SCROLLS`, recuperando un scroll táctil 100% fluido por todo el historial.
  * Caché de WebView desactivado (`LOAD_NO_CACHE`) para garantizar la carga inmediata de nuevos scripts y estilos.

### 💬 Navegación de Chats & Corrección de Notificación de Historial
* **Corrección de Notificación Errónea al Abrir Historial**:
  * Corregida la llamada de actualización del nombre del proyecto en la cabecera (`updateProjectName`), eliminando el fallo de script que disparaba erróneamente la notificación *"Error al abrir historial de la conversación"* a pesar de que los mensajes cargaban correctamente.
* **Botón Central "Chats" en el Pie de Página**:
  * Nuevo botón `💬 Chats` ubicado en el centro inferior de la pantalla (entre Menú/Latencia y el botón OLED).
  * Apertura instantánea de un modal responsivo que enumera todas las conversaciones y proyectos sincronizados de la PC.
* **Solución a "Error al cargar conversaciones de la PC"**:
  * Implementado mecanismo de respaldo escaneando directamente las carpetas en `brain/`, garantizando que la lista de conversaciones cargue siempre aunque SQLite esté bloqueado.
* **Indicadores Pulsantes Estrictos (Sin Texto al Frente)**:
  * Conversaciones activas o procesando: muestran estrictamente un punto pulsante naranja (`🟠`).
  * Conversaciones en reposo / ociosas: muestran estrictamente un punto pulsante verde (`🟢`).
  * Conforme a lo solicitado, sin texto alguno ni mensaje prefijado delante del punto.
* **Inspección de Historial Remota e Independiente**:
  * Al seleccionar cualquier proyecto o chat en el móvil, se carga todo el historial completo sin alterar la ventana ni la conversación activa en la PC.

### 🔄 Estados de Ejecución & Unificación
* **Estado "Pensando..." (Unificación de "Thought" y "Thinking")**:
  * Corrección y unificación de ambos estados en "Pensando..." (ES/PT) / "Thinking..." (EN) con indicador púrpura pulsante (`#a855f7`).
* **Ajuste de Estados Solicitado**:
  * Se retiraron los estados intermedios "Analyzed" y "Ran", consolidando el flujo en: "Pensando...", "Trabajando...", "Ejecutando Tarea..." y "Completado" (durante 1 minuto).
* **Estados Existentes Conservados**:
  * "Procesando" renombrado a "Trabajando...".
  * "Ejecutando Tarea..." (*Task Running*) con indicador cian eléctrico pulsante.
  * "Completado" (*Done*) se muestra durante 1 minuto antes de retornar a "Conectado".

### 🧹 Eliminación de Botones "✕" & Cierre al Tocar Fuera
* **Eliminación Total de la "✕" de Cierre**:
  * Se eliminó el botón "✕" de todos los modales (Tutorial, Menú de Configuración, Historial de Tareas y Chats).
  * Todos los modales se cierran al tocar fuera (backdrop click) o mediante el botón "Cerrar" en la parte inferior.

### 📱 Distintivo de Versión Dinámico & Actualizador Automático
* **Distintivo de Versión en Encabezado**:
  * Detección automática del entorno: el APK detecta la versión instalada en el dispositivo y muestra `vX.X.X (APK) • Dev LumiaG5`. En acceso por navegador IP muestra `v2.4.3 (IP) • Dev LumiaG5`.
* **Actualización Automática del APK en el Menú (Exclusivo Android)**:
  * Nueva sección en el modal `⚙️ Menú`.
  * Consulta automática de nuevas releases en GitHub mediante comparación semántica de versiones (SemVer).
  * Descarga en segundo plano del archivo `.apk` y apertura del instalador nativo del sistema vía `FileProvider` seguro (`ACTION_VIEW`).
* **Auditoría de Seguridad**:
  * Escaneo completo confirmando cero credenciales, PATs de GitHub o claves de API en código e historial de Git.
  * Sanitización contra *Path Traversal* en endpoints del servidor.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### 🚀 Nuevas Funciones & Seguridad de Sesión
* **Cierre Automático de Sesión al Salir**:
  * Al reabrir la app, siempre inicia en la pantalla de **Gestión de Sesión**, protegiendo las sesiones de monitoreo.
  * El botón nativo "Atrás" de Android dentro del chat desconecta de forma segura a la pantalla de sesión.
  * Atajo directo **`🚪 Salir / Desconectar Sesión`** dentro del menú `⚙️ Menú`.
* **Opción "▶ Volver a la Sesión" (Sin Nuevo PIN)**:
  * Si el servidor sigue corriendo en la PC, un solo toque reconecta inmediatamente sin solicitar nuevo PIN, aprovechando la sesión de 24 horas.
* **Opción "📷 Entrar con Código QR" vía Cámara Nativa (ZXing)**:
  * Integración con la librería ZXing Android Embedded.
  * Solicitud en tiempo de ejecución del permiso `android.permission.CAMERA`.
  * La terminal de la PC incluye el PIN en el código QR (`?pin=XXXX`). Con solo apuntar la cámara, la conexión se realiza de forma instantánea.
* **Opción "⚡ Nueva Sesión"**:
  * Permite iniciar una nueva sesión desde cero, limpiando la caché para conectar a otro servidor o ingresar un nuevo PIN.
* **Interfaz OLED True Black Limpia**:
  * Eliminación de botones obsoletos para una experiencia visual minimalista y con máximo ahorro de batería (`#000000`).

---

## [2.4.1] - 2026-10-25 (Build 2419)

### 🐛 Correcciones de Red & Conexión
* **Deducción Inteligente de Protocolo (HTTP vs HTTPS)**:
  * Corrección del fallo donde IPs locales eran forzadas a `https://`, causando error TLS en Uvicorn (`WARNING: Invalid HTTP request received`).
  * La aplicación detecta automáticamente IPs locales y fuerza `http://`, reservando `https://` para dominios y túneles Cloudflare.
* **Autocompletado de Puerto por Defecto**:
  * Anexa automáticamente `:8765` si no se especifica puerto en IPs locales.
* **Diagnóstico Detallado de Errores**:
  * Pantalla de error muestra la URL y el motivo devuelto por WebView.
* **Compatibilidad con Versiones Anteriores de Android**:
  * Manejo dual de errores para compatibilidad con Android 7 a 9 en emuladores como LDPlayer.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### 📱 Lanzamiento Inicial del Wrapper Nativo
* **Estructura Nativa en Kotlin / Gradle**:
  * Paquete oficial `com.lumiag5.antigravitymobile`.
  * `minSdk = 24` (Android 7.0+) y `targetSdk = 34` (Android 14).
* **WebView Optimizado**:
  * Soporte a WebSockets (`/ws`), Web Audio API y almacenamiento local.
  * Barra de estado en OLED True Black (`#000000`) vía `WindowCompat`.
* **Permisos del Sistema**:
  * Soporte a notificaciones push nativas (`POST_NOTIFICATIONS` en Android 13+).
  * Tráfico claro habilitado (`usesCleartextTraffic="true"`) para Wi-Fi local.
* **Pipeline de CI/CD (GitHub Actions)**:
  * Flujo automatizado `.github/workflows/build-apk.yml` compilando releases en la nube.
