# Changelog

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.md">Português</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.en.md">English</a> &bull; <b>Español</b>
</p>

Todos los cambios notables de **Antigravity Mobile** se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### 🐛 Corregido
* **Desplazamiento Vertical de Mensajes en el APK**: Resuelto el problema en que el usuario no podía desplazarse hacia arriba en el APK para ver el historial anterior. Se eliminó `SwipeRefreshLayout` del diseño nativo de Android para que `WebView` reciba todos los toques sin captura indebida de gestos, garantizando paridad total con la versión web por IP.
* **Eliminación Global del Ícono "✕" de Cierre**: El botón "✕" fue retirado de todos los modales (Tutorial, Menú, Historial y Chats). Todos los modales se auto-cierran al hacer clic fuera de la ventana (backdrop click) o mediante un botón limpio "Cerrar" en el pie.

### 🚀 Añadido
* **Botón "Chats" Central en el Pie de Página**:
  * Ubicado en el centro inferior de la pantalla (entre Menú/Latencia a la izquierda y el botón OLED a la derecha).
  * Abre el modal de selección de conversaciones y proyectos sincronizados de Antigravity PC en ambas versiones (APK e IP/Web).
* **Indicadores Pulsantes Estrictos por Conversación**:
  * Si Antigravity está procesando algo en esa conversación: muestra **únicamente un punto pulsante naranja (`🟠`)**, sin texto ni mensaje al frente.
  * Si está ocioso/no procesando: muestra **únicamente un punto pulsante verde (`🟢`)**, sin texto ni mensaje al frente.
* **Lectura Remota Totalmente Independiente**:
  * Al seleccionar cualquier chat/proyecto en la lista desde el móvil, la app obtiene y renderiza el historial completo directamente del transcript sin alterar la ventana ni la conversación abierta en la PC y sin simular clics remotos de ratón.
  * Banner con botón "Volver a la PC en Vivo" para alternar rápidamente de regreso a la sincronización en tiempo real.
* **Estados "Trabajando...", "Pensando..." y "Ejecutando Tarea..."**:
  * Estado "Procesando" renombrado a **"Trabajando..."** (*Working*).
  * Estado **"Pensando..."** (*Thought* / *Thinking*).
  * Nuevo estado **"Ejecutando Tarea..."** (*Task Running*) con indicador visual cian pulsante (`#0ea5e9`).
  * Al concluir tareas, el estado **"Completado"** (*Done*) se activa y permanece visible durante **1 minuto** (o hasta que inicie una nueva actividad), regresando a "Conectado" al finalizar el tiempo.
* **Diferenciación Visual de Versión (APK vs IP)**:
  * El encabezado ahora diferencia la versión del APK instalado en el dispositivo (`vX.X.X (APK) • Dev LumiaG5`) y la versión companion por IP (`v2.4.3 (IP) • Dev LumiaG5`), eliminando confusiones de caché.
* **Actualización Automática del APK en el Menú (Exclusiva para Android)**:
  * Añadida sección dedicada en el menú `⚙️ Menú` del APK para comprobación y descarga en 1 toque de nuevas versiones directamente desde GitHub Releases, abriendo el instalador nativo del sistema vía `FileProvider`.
