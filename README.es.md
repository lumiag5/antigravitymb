# Antigravity Mobile

<p align="center">
  <a href="README.md">Português</a> &bull; <a href="README.en.md">English</a> &bull; <b>Español</b>
</p>

Companion ligero para monitorizar **Antigravity IDE** desde el móvil en tiempo real. Sigue el razonamiento de la IA, recibe alertas sensoriales (sonido/pantalla/vibración) cuando finalicen las tareas de código y consulta el consumo oficial de tu cuota de Gemini sin necesidad de instalar ninguna aplicación de tiendas.

---

## Motivación

Cuando le pides a Antigravity que realice tareas largas —como refactorizaciones pesadas, generación de múltiples componentes o ejecución de tests—, sueles levantarte del escritorio para tomar un café o descansar en el sofá. El problema es que no sabes cuándo termina el agente, si se ha quedado esperando una confirmación en la terminal o si tu cuota de 5 horas ha llegado al límite. Levantarse a cada momento o alternar ventanas con Alt-Tab rompe la concentración.

**Antigravity Mobile** soluciona esto mediante un pequeño demonio local en Python ejecutándose en tu PC que se conecta a tu teléfono a través de la red Wi-Fi local o un túnel HTTPS seguro. Ofrece una interfaz web oscura (OLED), rápida y adaptada a pantallas móviles que te avisa en el instante exacto en que tu código está listo.

---

## Funcionalidades

### Chat en Tiempo Real y Filtrado de Ruido
* **Enfoque en lo importante**: Antigravity genera cientos de líneas de registros de herramientas internas y salidas de consola. El companion filtra todo ese ruido y muestra únicamente la solicitud enviada y la respuesta final del asistente.
* **Markdown y Código**: Renderizado con bloques de código resaltados, listas y tablas con tipografía idéntica a la del IDE (Inter y JetBrains Mono).
* **Auto-scroll inteligente**: Sigue las nuevas respuestas automáticamente, pausándose si te desplazas hacia arriba para revisar el historial.

### Cambio Automático de Proyectos y Conversaciones
* **Detección de foco en vivo**: El servidor monitoriza los bloqueos de presencia (`presence/`), bases de datos SQLite y metadatos de la interfaz. En cuanto haces clic en otra conversación o proyecto en el PC, el móvil se actualiza al instante (`📁 Proyecto • Título de la Conversación`).
* **Vigilancia en segundo plano**: Si cambias de conversación en el PC mientras una tarea sigue procesándose (*Working...*), el servidor continúa monitorizando la tarea original en segundo plano y te avisa cuando finalice.

### Alertas de Conclusión de Tarea
En el instante en que el agente de IA termina su trabajo:
* **Parpadeo de pantalla**: 2 destellos en verde esmeralda separados por 1 segundo (visible incluso con el teléfono apoyado en la mesa).
* **Aviso sonoro**: Tono sintetizado directamente en el navegador mediante la Web Audio API con volumen reforzado (+dB) para entornos con ruido.
* **Vibración háptica**: Patrón táctil doble para teléfonos en modo silencio.
* **Notificaciones del sistema**: Soporte nativo para Web Notifications con la pantalla bloqueada.

### Monitor Oficial de Cuotas de IA (RPC Interno)
* **Sin estimaciones aproximadas**: Se conecta directamente al servicio RPC local de Antigravity (`LanguageServerService/RetrieveUserQuotaSummary`), descubriendo dinámicamente el puerto y el token CSRF.
* **Métricas reales**: Barras de progreso que muestran el consumo porcentual exacto de la cuota de **5 Horas** y **Semanal**, cuenta regresiva de renovación y modelo activo (ej.: *Gemini 3.8 Flash High*).

### Modo OLED Black Puro
* Fondo negro absoluto (`#000000`) para ahorrar batería en pantallas AMOLED/OLED.
* Burbuja de mensaje del usuario adaptada a gris oscuro de alto contraste para una lectura cómoda en la oscuridad.

### Seguridad con PIN y Sesión de 24h
* La primera vez que te conectas, la terminal del PC muestra un PIN aleatorio de 4 dígitos.
* Tras emparejar, la sesión queda guardada en la caché local durante 24 horas (puedes recargar la página o cambiar de app sin volver a introducir el PIN).
* Protección anti-fuerza bruta y registro silencioso de intentos denegados.

### Túnel HTTPS Automático (Cloudflare)
* Incluye el binario standalone oficial de Cloudflare Tunnel.
* Genera automáticamente una URL pública segura (`https://*.trycloudflare.com`), permitiendo que las notificaciones funcionen en Chrome para Android sin restricciones del protocolo HTTP ni necesidad de abrir puertos en el router.

### Soporte Multi-idioma
* Disponible en **Portugués (Brasil)**, **Inglés** y **Español**.
* Puedes cambiar el idioma en cualquier momento pulsando la tecla **`L`** en la consola del PC.

---

## Cómo Empezar

### Requisitos Previos
* **Windows 10 o 11** con Antigravity IDE en ejecución.
* **Python 3.10 o superior** instalado y agregado al PATH.
* Teléfono móvil conectado a la misma red Wi-Fi que el PC (o utilizando el enlace HTTPS generado).

### Inicio Rápido

1. Clona el repositorio:
   ```bash
   git clone https://github.com/LumiaG5/antigravity-mobile.git
   cd antigravity-mobile
   ```

2. Inicia el servidor:
   * Haz doble clic en `antrigavitymb/Start_Server.bat`; **O**
   * Por terminal:
     ```bash
     cd antrigavitymb/desktop-bridge
     pip install -r requirements.txt
     python run.py
     ```

3. Conecta desde el Teléfono:
   La consola mostrará las direcciones de conexión:
   ```text
   ====================================================================
           [*] ANTIGRAVITY MOBILE - SERVIDOR DESKTOP BRIDGE
                    Desarrollado por Dev LumiaG5
   ====================================================================
    * PC Local:              http://localhost:8765
    * Móvil (Wi-Fi):         http://192.168.0.X:8765
    * Móvil (HTTPS Seguro):  https://tu-tunnel.trycloudflare.com
    * Idioma Activo:         Español
   --------------------------------------------------------------------
    PIN DE ACCESO:           [ 4821 ]
   ====================================================================
   ```
   * Abre el enlace en el navegador del móvil (se recomienda HTTPS para activar notificaciones).
   * Introduce el PIN de 4 dígitos mostrado en la terminal.
   * *(Opcional)* En el menú del navegador del teléfono, selecciona **"Añadir a la pantalla de inicio"** para usarlo a pantalla completa como PWA.

---

## Atajos de la Terminal del PC

Con el servidor ejecutándose en la consola, puedes usar estos atajos:

| Tecla | Acción |
| :--- | :--- |
| **Cualquier tecla** | Genera un nuevo PIN aleatorio para emparejar otro dispositivo |
| **`L`** | Cambia el idioma de la interfaz (Portugués / Inglés / Español) |
| **`Ctrl + C`** | Detiene el servidor y cierra el túnel seguro de forma limpia |

---

## Estructura del Repositorio

```
antrigavitymb/
├── desktop-bridge/            # Demonio en Python (FastAPI + WebSockets)
│   ├── run.py                 # Ejecutable interactivo de consola y atajos de teclado
│   ├── server.py              # Rutas REST y canales de streaming por WebSocket
│   ├── monitor.py             # Parser de transcripts (tail-seek), locks y base SQLite
│   ├── auth.py                # Verificación de PIN y sesiones en caché (TTL 24h)
│   ├── language_manager.py    # Gestor de traducciones (pt, en, es)
│   ├── tunnel.py              # Integración con el túnel seguro Cloudflare
│   ├── antigravity_api.py     # Cliente RPC para obtención de cuotas
│   ├── config.py              # Detección automática de rutas en Windows
│   ├── bin/cloudflared.exe    # Binario standalone del túnel Cloudflare
│   └── static/
│       ├── index.html         # Frontend Web Companion (HTML5 / CSS3 / Vanilla JS)
│       └── antigravity-icon.png
├── mobile-app/                # Base en React Native / Expo (por si deseas compilar APK)
├── Start_Server.bat           # Script de arranque en 1 clic para Windows
└── COMO_CONECTAR.txt          # Guía rápida de conexión trilingüe
```

---

## Preguntas Frecuentes

**¿Necesito compilar el APK para usarlo en el móvil?**  
No. El Web Companion funciona directamente en el navegador (Chrome, Safari, Firefox, Edge, Opera, Samsung Internet) con soporte completo para sonido, vibración y notificaciones push sin instalar ningún APK.

**¿Funciona en iPhone / iOS?**  
Sí. En Safari para iOS el panel y las alertas funcionan de forma nativa. Para recibir notificaciones con la pantalla bloqueada en iOS, añade la página a la Pantalla de Inicio.

**¿Antigravity necesita estar abierto en el PC?**  
Sí. El demonio monitoriza los archivos de sesión y las interfaces RPC generadas por el IDE mientras programas.

**¿Es seguro el túnel HTTPS?**  
Sí. Utiliza la red de Cloudflare con cifrado TLS punto a punto. No es necesario abrir puertos en tu router y todos los accesos requieren la validación previa del PIN de 4 dígitos.

---

## Autor

Desarrollado por **Dev LumiaG5**  
GitHub: [@LumiaG5](https://github.com/LumiaG5)

---

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE.txt). Consulta el archivo `LICENSE.txt` para más detalles.
