# Changelog

<p align="center">
  <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.md">Português</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.en.md">English</a> &bull; <b>Español</b>
</p>

Todos los cambios notables de **Antigravity Mobile** se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

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
