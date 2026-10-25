# Changelog

<p align="center">
  <a href="changelog.md">Português</a> <a href="changelog.en.md">English</a> <b>Español</b><a href="changelog.es.md">
</p>

Todos los cambios notables de **Antigravity Mobile** se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

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
