# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

LANGUAGE_FILE = Path(__file__).parent / "user_language.json"

TRANSLATIONS: Dict[str, Dict[str, Any]] = {
    "pt": {
        "lang_code": "pt-BR",
        "lang_name": "Português (Brasil)",
        "title": "Antigravity Mobile",
        
        # Terminal strings
        "terminal_title": "SERVIDOR DESKTOP BRIDGE",
        "terminal_local_pc": "PC Local",
        "terminal_mobile_wifi": "Mobile (Wi-Fi)",
        "terminal_mobile_https": "Mobile (HTTPS Seguro)",
        "terminal_active_lang": "Idioma Ativo",
        "terminal_pairing_pin": "PIN DE PAREAMENTO",
        "terminal_security_tag": "SEGURANÇA",
        "terminal_new_pin_banner": "NOVO PIN DE PAREAMENTO GERADO",
        "terminal_pin_prompt": "DIGITE ESTE PIN NO CELULAR PARA LIBERAR",
        "terminal_paired_success": "Dispositivo pareado e liberado com sucesso via PIN {pin}!",
        "terminal_server_started": "Bridge iniciado com sucesso e monitorando em background.",
        "terminal_client_connected": "Cliente conectado. Total ativos: {count}",
        "terminal_client_disconnected": "Cliente desconectado. Total ativos: {count}",
        "terminal_monitoring_conv": "Monitorando conversa: {conv_id} ({model}) - Offset inicial: {offset}",
        "terminal_tutorial_header": "GUIA RÁPIDO PARA CONECTAR NO CELULAR:",
        "terminal_tutorial_step1": "  1. Conecte o celular na mesma rede Wi-Fi deste computador.",
        "terminal_tutorial_step2": "  2. No navegador do celular, abra: http://{ip}:{port}",
        "terminal_tutorial_step3": "  3. Digite o PIN gerado no terminal para liberar (salvo em cache por 24h).",
        "terminal_tutorial_step4": "  4. Para ativar notificações no celular, use o link HTTPS Seguro acima.",
        "server_notice": "Cheque o PIN enviado no terminal, e insira-o no App Antigravity Mobile",
        "press_key_notice": "Pressione qualquer tecla para novo PIN | Tecla L para alternar idioma",
        
        # Web / Mobile App UI
        "pin_badge": "PAREAMENTO SEGURO",
        "pin_instruction": "Digite o PIN de 4 dígitos exibido no terminal do computador para liberar o acesso.",
        "btn_unlock": "Desbloquear Acesso",
        "btn_new_pin": "🔄 Gerar Novo PIN no Terminal",
        "pin_verifying": "Verificando...",
        "pin_authorized": "Autorizado com sucesso!",
        "pin_error": "PIN incorreto. Verifique o terminal do PC.",
        
        "quota_5h_title": "Limite 5 Horas",
        "quota_weekly_title": "Limite Semanal",
        "quota_syncing": "Sincronizando...",
        "quota_available": "100% Disponível",
        
        "empty_title": "Aguardando edições no PC",
        "empty_sub": "As conclusões das tarefas aparecerão aqui automaticamente.",
        "footer_alert": "Som & Flash",
        "footer_test_btn": "🔔 Testar Alerta",
        "msg_user": "Você",
        "msg_assistant": "Antigravity (Conclusão)",
        
        "status_connected": "Conectado",
        "status_processing": "Trabalhando...",
        "status_working": "Trabalhando...",
        "status_thought": "Pensando...",
        "status_thinking": "Pensando...",
        "status_task_running": "Executando Tarefa...",
        "status_done": "Concluído",
        "status_disconnected": "DESCONECTADO",
        "status_connecting": "CONECTANDO...",

        # Atualizador do APK Android
        "menu_update_section_title": "Aplicativo Android",
        "btn_check_update": "Verificar e Atualizar App",
        "update_up_to_date": "O app já está atualizado!",
        "update_available": "Nova versão encontrada: ",
        "update_downloading": "Baixando atualização do APK...",

        # Botão e Modal de Chats
        "btn_chats": "Chats",
        "chats_modal_title": "Conversas no PC",
        "chats_current_pc": "No PC",
        "chats_live_pc_btn": "⚡ Voltar ao Chat Ativo do PC",
        "chats_viewing_custom": "Visualizando conversa selecionada",
        "chats_no_active": "Nenhuma conversa encontrada",
        "chats_error": "Erro ao carregar conversas do PC.",
        
        # Tutorial de Conexão Rápido
        "tutorial_btn": "❓ Como Conectar ao Celular",
        "tutorial_title": "Guia Rápido de Conexão",
        "tutorial_step1_title": "1. Mesma Rede Wi-Fi",
        "tutorial_step1_desc": "Certifique-se de que o computador e o celular estão conectados na mesma rede Wi-Fi.",
        "tutorial_step2_title": "2. Acesse o Endereço no Celular",
        "tutorial_step2_desc": "Abra o navegador no celular e digite o endereço IP mostrado no terminal (ex: http://192.168.0.6:8765).",
        "tutorial_step3_title": "3. Digite o PIN de 4 Dígitos",
        "tutorial_step3_desc": "Insira o PIN exibido no terminal do computador. A sessão é gravada em cache por 24 horas!",
        "tutorial_step4_title": "4. Pronto!",
        "tutorial_step4_desc": "Acompanhe as respostas, cotas de IA oficiais e receba alertas sonoros e flash de tela.",
        "tutorial_btn_close": "Entendido",

        # Features v2.2.0 (OLED, Notificações, Scroll, Workspace)
        "project_label": "Projeto",
        "project_title_prefix": "Projeto: ",
        "btn_oled": "🌓 OLED",
        "oled_active": "Modo OLED Ativo",
        "oled_disabled": "Modo OLED Desativado",
        "btn_notifications": "🔔 Notificações",
        "btn_notifications_label": "Notificações",
        "notifications_enabled": "Notificações ativadas!",
        "notifications_disabled": "Notificações desativadas",
        "notifications_silenced": "Notificações silenciadas",
        "notifications_turn_off": "Toque para desativar",
        "notifications_turn_on": "Toque para ativar",
        "notifications_blocked": "Navegadores exigem HTTPS para notificações. Alertas com Som e Flash 2x ativos!",
        "notifications_http_notice": "Navegadores exigem HTTPS para notificações push. Alertas com Som e Flash 2x ativos!",
        "notifications_redirect_toast": "Abrindo versão HTTPS segura para ativar notificações...",
        "btn_open_https": "🔒 Abrir Versão HTTPS",
        "notifications_not_supported": "Navegador não suporta notificações.",
        "scroll_to_bottom": "Ir para o fim",
        "new_messages_badge": "{count} nova(s)",
        "task_completed_notify_title": "Antigravity • Tarefa Concluída",

        # Features v2.4.0 (Menu, QR Code, Latência, Sons, Histórico/Log)
        "terminal_qr_title": "[QR CODE - ESCANEIE COM A CÂMERA DO CELULAR PARA CONECTAR]:",
        "btn_menu": "⚙️ Menu",
        "btn_menu_title": "Configurações e Preferências",
        "menu_title": "Configurações",
        "menu_notifications_label": "Notificações no Navegador",
        "menu_sensory_label": "Alerta Sensorial (Som & Flash)",
        "menu_tone_label": "Toque de Alerta",
        "tone_modern": "Chime Moderno",
        "tone_bell": "Sino Zen",
        "tone_scifi": "Pulso Sci-Fi",
        "tone_classic": "Bip Clássico",
        "menu_volume_label": "Volume do Toque",
        "menu_latency_label": "Exibir Latência em Tempo Real (Ping)",
        "menu_btn_log": "📜 Ver Histórico de Conclusões",
        "menu_btn_test_sound": "▶️ Testar Toque",
        "menu_close": "Fechar",
        "log_title": "Histórico de Conclusões",
        "log_empty": "Nenhuma conclusão registrada ainda.",
        "log_clear": "Limpar Histórico",
        "log_cleared": "Histórico limpo com sucesso!",
        "latency_label": "Latência",
        "menu_fullscreen_label": "Modo Tela Cheia",
        "btn_fullscreen": "Alternar",
        "fullscreen_active": "Tela cheia ativada",
        "fullscreen_disabled": "Tela cheia desativada",
        "battery_title": "Bateria",
        "btn_prompt": "Prompt",
        "prompt_modal_title": "Enviar Prompt ao PC",
        "prompt_step1_subtitle": "1º Passo: Escolha o chat ou projeto de destino",
        "prompt_step2_badge": "2º Passo",
        "prompt_back_btn": "← Voltar",
        "prompt_input_label": "Escreva sua solicitação para a IA:",
        "prompt_placeholder": "Digite aqui o que você deseja que o Antigravity faça...",
        "btn_send_prompt": "Enviar para o PC",
        "prompt_sending": "Enviando...",
        "prompt_sent_success": "Prompt enviado com sucesso ao PC!",
        "prompt_empty_warn": "Por favor, digite um prompt para enviar.",
        "prompt_error": "Erro ao enviar prompt para o PC.",
        "menu_oled_label": "Tema OLED True Black",
        "menu_battery_label": "Exibir Nível de Bateria",
        "prompt_model_label": "Modelo IA:",
        "menu_sec_alerts": "Alertas & Notificações",
        "menu_sec_sound": "Áudio & Toques",
        "menu_sec_system": "Rede & Histórico",
        "menu_apk_installed_label": "Versão Instalada:",
        "menu_btn_logout": "Sair / Desconectar da Sessão",
        "search_chats_placeholder": "Buscar chat ou projeto...",
        "search_no_results": "Nenhuma conversa encontrada",
        "prompt_history_btn": "Histórico",
        "prompt_history_title": "Prompts Recentes",
        "prompt_history_empty": "Nenhum prompt anterior registrado.",
        "prompt_history_clear": "Limpar",
        "prompt_char_counter": "{chars} caracteres • {words} palavras",
        "copy_response": "Copiar resposta",
        "response_copied": "Resposta copiada para a área de transferência!",
        "copy_failed": "Falha ao copiar resposta.",
        "thinking_indicator": "Antigravity está pensando...",
        "favorite_chat_title": "Favoritar conversa",
        "unfavorite_chat_title": "Remover dos favoritos",
        "quick_prompts_title": "Atalhos rápidos:",
        "snippet_continue": "Continue",
        "snippet_run_tests": "Rode os testes",
        "snippet_summarize": "Resuma o progresso",
        "snippet_check_errors": "Verifique erros",
        "share_response": "Compartilhar resposta",
        "share_chat_title": "Antigravity Mobile • Resposta da IA",
        "share_success": "Compartilhado com sucesso!"
    },
    "en": {
        "lang_code": "en-US",
        "lang_name": "English",
        "title": "Antigravity Mobile",
        
        # Terminal strings
        "terminal_title": "DESKTOP BRIDGE DAEMON",
        "terminal_local_pc": "Local PC",
        "terminal_mobile_wifi": "Mobile (Wi-Fi)",
        "terminal_mobile_https": "Mobile (Secure HTTPS)",
        "terminal_active_lang": "Active Language",
        "terminal_pairing_pin": "PAIRING PIN",
        "terminal_security_tag": "SECURITY",
        "terminal_new_pin_banner": "NEW PAIRING PIN GENERATED",
        "terminal_pin_prompt": "ENTER THIS PIN ON MOBILE TO UNLOCK",
        "terminal_paired_success": "Device successfully paired and unlocked via PIN {pin}!",
        "terminal_server_started": "Bridge successfully started and monitoring in background.",
        "terminal_client_connected": "Client connected. Total active: {count}",
        "terminal_client_disconnected": "Client disconnected. Total active: {count}",
        "terminal_monitoring_conv": "Monitoring conversation: {conv_id} ({model}) - Initial offset: {offset}",
        "terminal_tutorial_header": "QUICK GUIDE TO CONNECT ON MOBILE:",
        "terminal_tutorial_step1": "  1. Connect your phone to the same Wi-Fi network as this PC.",
        "terminal_tutorial_step2": "  2. On mobile browser, open: http://{ip}:{port}",
        "terminal_tutorial_step3": "  3. Enter the PIN generated on the terminal to unlock (cached for 24h).",
        "terminal_tutorial_step4": "  4. To enable mobile notifications, use the Secure HTTPS link above.",
        "server_notice": "Check the PIN sent to the terminal, and enter it in the Antigravity Mobile App",
        "press_key_notice": "Press any key to refresh the server | Press L to change language",
        
        # Web / Mobile App UI
        "pin_badge": "SECURE PAIRING",
        "pin_instruction": "Enter the 4-digit PIN displayed on the computer terminal to unlock access.",
        "btn_unlock": "Unlock Access",
        "btn_new_pin": "🔄 Generate New PIN on Terminal",
        "pin_verifying": "Verifying...",
        "pin_authorized": "Authorized successfully!",
        "pin_error": "Incorrect PIN. Check the PC terminal.",
        
        "quota_5h_title": "5-Hour Limit",
        "quota_weekly_title": "Weekly Limit",
        "quota_syncing": "Syncing...",
        "quota_available": "100% Available",
        
        "empty_title": "Waiting for edits on PC",
        "empty_sub": "Task conclusions will appear here automatically.",
        "footer_alert": "Sound & Flash",
        "footer_test_btn": "🔔 Test Alert",
        "msg_user": "You",
        "msg_assistant": "Antigravity (Conclusion)",
        
        "status_connected": "Connected",
        "status_processing": "Working...",
        "status_working": "Working...",
        "status_thought": "Thinking...",
        "status_thinking": "Thinking...",
        "status_task_running": "Task Running...",
        "status_done": "Completed",
        "status_disconnected": "DISCONNECTED",
        "status_connecting": "CONNECTING...",

        # Android APK Updater
        "menu_update_section_title": "Android App",
        "btn_check_update": "Check & Update App",
        "update_up_to_date": "App is already up to date!",
        "update_available": "New version found: ",
        "update_downloading": "Downloading APK update...",

        # Chats Button and Modal
        "btn_chats": "Chats",
        "chats_modal_title": "Chats on PC",
        "chats_current_pc": "On PC",
        "chats_live_pc_btn": "⚡ View Live PC Chat",
        "chats_viewing_custom": "Viewing selected conversation",
        "chats_no_active": "No conversations found",
        "chats_error": "Error loading PC chats.",
        
        # Quick Connection Tutorial
        "tutorial_btn": "❓ How to Connect",
        "tutorial_title": "Quick Connection Guide",
        "tutorial_step1_title": "1. Same Wi-Fi Network",
        "tutorial_step1_desc": "Make sure your PC and mobile device are connected to the same local Wi-Fi network.",
        "tutorial_step2_title": "2. Open the URL on Mobile",
        "tutorial_step2_desc": "Open your mobile browser and type the IP address shown on the PC terminal (e.g. http://192.168.0.6:8765).",
        "tutorial_step3_title": "3. Enter the 4-Digit PIN",
        "tutorial_step3_desc": "Type the PIN displayed on the PC terminal. Your session will be cached for 24 hours!",
        "tutorial_step4_title": "4. All Set!",
        "tutorial_step4_desc": "Monitor responses, official AI quotas, and get audio chime & screen flash alerts.",
        "tutorial_btn_close": "Got it",

        # Features v2.2.0 (OLED, Notifications, Scroll, Workspace)
        "project_label": "Project",
        "project_title_prefix": "Project: ",
        "btn_oled": "🌓 OLED",
        "oled_active": "OLED Mode Active",
        "oled_disabled": "OLED Mode Disabled",
        "btn_notifications": "🔔 Notifications",
        "btn_notifications_label": "Notifications",
        "notifications_enabled": "Notifications enabled!",
        "notifications_disabled": "Notifications disabled",
        "notifications_silenced": "Notifications silenced",
        "notifications_turn_off": "Tap to disable",
        "notifications_turn_on": "Tap to enable",
        "notifications_blocked": "Browsers require HTTPS for notifications. Dual Sound and 2x Flash alerts are active!",
        "notifications_http_notice": "Browsers require HTTPS for push notifications. Dual Sound and 2x Flash alerts are active!",
        "notifications_redirect_toast": "Opening secure HTTPS version to enable notifications...",
        "btn_open_https": "🔒 Open HTTPS Version",
        "notifications_not_supported": "Browser does not support notifications.",
        "scroll_to_bottom": "Scroll to bottom",
        "new_messages_badge": "{count} new",
        "task_completed_notify_title": "Antigravity • Task Completed",

        # Features v2.4.0 (Menu, QR Code, Latency, Ringtones, History/Log)
        "terminal_qr_title": "[QR CODE - SCAN WITH PHONE CAMERA TO CONNECT]:",
        "btn_menu": "⚙️ Menu",
        "btn_menu_title": "Settings & Preferences",
        "menu_title": "Settings",
        "menu_notifications_label": "Browser Notifications",
        "menu_sensory_label": "Sensory Alert (Sound & Flash)",
        "menu_tone_label": "Alert Ringtone",
        "tone_modern": "Modern Chime",
        "tone_bell": "Zen Bell",
        "tone_scifi": "Sci-Fi Pulse",
        "tone_classic": "Classic Beep",
        "menu_volume_label": "Ringtone Volume",
        "menu_latency_label": "Show Real-Time Latency (Ping)",
        "menu_btn_log": "📜 View Task History",
        "menu_btn_test_sound": "▶️ Test Sound",
        "menu_close": "Close",
        "log_title": "Task Completion History",
        "log_empty": "No task completions logged yet.",
        "log_clear": "Clear History",
        "log_cleared": "History cleared successfully!",
        "latency_label": "Latency",
        "menu_fullscreen_label": "Fullscreen Mode",
        "btn_fullscreen": "Toggle",
        "fullscreen_active": "Fullscreen enabled",
        "fullscreen_disabled": "Fullscreen disabled",
        "battery_title": "Battery",
        "btn_prompt": "Prompt",
        "prompt_modal_title": "Send Prompt to PC",
        "prompt_step1_subtitle": "Step 1: Choose target chat or project",
        "prompt_step2_badge": "Step 2",
        "prompt_back_btn": "← Back",
        "prompt_input_label": "Write your prompt for AI:",
        "prompt_placeholder": "Type here what you want Antigravity to do...",
        "btn_send_prompt": "Send to PC",
        "prompt_sending": "Sending...",
        "prompt_sent_success": "Prompt successfully sent to PC!",
        "prompt_empty_warn": "Please type a prompt to send.",
        "prompt_error": "Failed to send prompt to PC.",
        "menu_oled_label": "OLED True Black Theme",
        "menu_battery_label": "Show Battery Level",
        "prompt_model_label": "AI Model:",
        "menu_sec_alerts": "Alerts & Notifications",
        "menu_sec_sound": "Audio & Ringtone",
        "menu_sec_system": "Network & History",
        "menu_apk_installed_label": "Installed Version:",
        "menu_btn_logout": "Sign Out / Disconnect Session",
        "search_chats_placeholder": "Search chat or project...",
        "search_no_results": "No conversations found",
        "prompt_history_btn": "History",
        "prompt_history_title": "Recent Prompts",
        "prompt_history_empty": "No previous prompts recorded.",
        "prompt_history_clear": "Clear",
        "prompt_char_counter": "{chars} chars • {words} words",
        "copy_response": "Copy response",
        "response_copied": "Response copied to clipboard!",
        "copy_failed": "Failed to copy response.",
        "thinking_indicator": "Antigravity is thinking...",
        "favorite_chat_title": "Favorite chat",
        "unfavorite_chat_title": "Remove from favorites",
        "quick_prompts_title": "Quick shortcuts:",
        "snippet_continue": "Continue",
        "snippet_run_tests": "Run tests",
        "snippet_summarize": "Summarize progress",
        "snippet_check_errors": "Check errors",
        "share_response": "Share response",
        "share_chat_title": "Antigravity Mobile • AI Response",
        "share_success": "Shared successfully!"
    },
    "es": {
        "lang_code": "es-ES",
        "lang_name": "Español",
        "title": "Antigravity Mobile",
        
        # Terminal strings
        "terminal_title": "SERVIDOR DESKTOP BRIDGE",
        "terminal_local_pc": "PC Local",
        "terminal_mobile_wifi": "Móvil (Wi-Fi)",
        "terminal_mobile_https": "Móvil (HTTPS Seguro)",
        "terminal_active_lang": "Idioma Activo",
        "terminal_pairing_pin": "PIN DE EMPAREJAMIENTO",
        "terminal_security_tag": "SEGURIDAD",
        "terminal_new_pin_banner": "NUEVO PIN DE EMPAREJAMIENTO GENERADO",
        "terminal_pin_prompt": "INGRESE ESTE PIN EN EL MÓVIL PARA DESBLOQUEAR",
        "terminal_paired_success": "¡Dispositivo emparejado y desbloqueado con éxito mediante PIN {pin}!",
        "terminal_server_started": "Bridge iniciado con éxito y monitoreando en segundo plano.",
        "terminal_client_connected": "Cliente conectado. Total activos: {count}",
        "terminal_client_disconnected": "Cliente desconectado. Total activos: {count}",
        "terminal_monitoring_conv": "Monitoreando conversación: {conv_id} ({model}) - Offset inicial: {offset}",
        "terminal_tutorial_header": "GUÍA RÁPIDA PARA CONECTAR EN EL MÓVIL:",
        "terminal_tutorial_step1": "  1. Conecte el teléfono a la misma red Wi-Fi de esta PC.",
        "terminal_tutorial_step2": "  2. En el navegador del móvil, abra: http://{ip}:{port}",
        "terminal_tutorial_step3": "  3. Ingrese el PIN generado en la terminal para desbloquear (guardado en caché por 24h).",
        "terminal_tutorial_step4": "  4. Para habilitar notificaciones en el móvil, use el enlace HTTPS Seguro de arriba.",
        "server_notice": "Consulte el PIN enviado en la terminal e ingréselo en la App Antigravity Mobile",
        "press_key_notice": "Presione cualquier tecla para actualizar el servidor | Tecla L para cambiar idioma",
        
        # Web / Mobile App UI
        "pin_badge": "EMPAREJAMIENTO SEGURO",
        "pin_instruction": "Ingrese el PIN de 4 dígitos mostrado en la terminal de la computadora para desbloquear el acceso.",
        "btn_unlock": "Desbloquear Acceso",
        "btn_new_pin": "🔄 Generar Nuevo PIN en la Terminal",
        "pin_verifying": "Verificando...",
        "pin_authorized": "¡Autorizado con éxito!",
        "pin_error": "PIN incorrecto. Consulte la terminal de la PC.",
        
        "quota_5h_title": "Límite 5 Horas",
        "quota_weekly_title": "Límite Semanal",
        "quota_syncing": "Sincronizando...",
        "quota_available": "100% Disponible",
        
        "empty_title": "Esperando ediciones en la PC",
        "empty_sub": "Las conclusiones de las tareas aparecerán aquí automáticamente.",
        "footer_alert": "Sonido y Flash",
        "footer_test_btn": "🔔 Probar Alerta",
        "msg_user": "Tú",
        "msg_assistant": "Antigravity (Conclusión)",
        
        "status_connected": "Conectado",
        "status_processing": "Trabajando...",
        "status_working": "Trabajando...",
        "status_thought": "Pensando...",
        "status_thinking": "Pensando...",
        "status_task_running": "Ejecutando Tarea...",
        "status_done": "Completado",
        "status_disconnected": "DESCONECTADO",
        "status_connecting": "CONECTANDO...",

        # Actualizador de APK Android
        "menu_update_section_title": "Aplicación Android",
        "btn_check_update": "Verificar y Actualizar App",
        "update_up_to_date": "¡La app ya está actualizada!",
        "update_available": "Nueva versión encontrada: ",
        "update_downloading": "Descargando actualización del APK...",

        # Botón y Modal de Chats
        "btn_chats": "Chats",
        "chats_modal_title": "Conversaciones en PC",
        "chats_current_pc": "En PC",
        "chats_live_pc_btn": "⚡ Ver Conversación Activa de PC",
        "chats_viewing_custom": "Viendo conversación seleccionada",
        "chats_no_active": "No se encontraron conversaciones",
        "chats_error": "Error al cargar conversaciones de la PC.",
        
        # Tutorial de Conexión Rápido
        "tutorial_btn": "❓ Cómo Conectar al Móvil",
        "tutorial_title": "Guía Rápida de Conexión",
        "tutorial_step1_title": "1. Misma Red Wi-Fi",
        "tutorial_step1_desc": "Asegúrate de que la computadora y el teléfono móvil estén conectados a la misma red Wi-Fi.",
        "tutorial_step2_title": "2. Abre la Dirección en el Móvil",
        "tutorial_step2_desc": "Abre el navegador en el móvil e ingresa la dirección IP mostrada en la terminal (ej: http://192.168.0.6:8765).",
        "tutorial_step3_title": "3. Ingresa el PIN de 4 Dígitos",
        "tutorial_step3_desc": "Ingresa el PIN mostrado en la terminal de la PC. ¡La sesión se guarda en caché durante 24 horas!",
        "tutorial_step4_title": "4. ¡Listo!",
        "tutorial_step4_desc": "Monitorea respuestas, cuotas de IA oficiales y recibe alertas de sonido y destello.",
        "tutorial_btn_close": "Entendido",

        # Features v2.2.0 (OLED, Notificaciones, Scroll, Workspace)
        "project_label": "Proyecto",
        "project_title_prefix": "Proyecto: ",
        "btn_oled": "🌓 OLED",
        "oled_active": "Modo OLED Activo",
        "oled_disabled": "Modo OLED Desactivado",
        "btn_notifications": "🔔 Notificaciones",
        "btn_notifications_label": "Notificaciones",
        "notifications_enabled": "¡Notificaciones activadas!",
        "notifications_disabled": "Notificaciones desactivadas",
        "notifications_silenced": "Notificaciones silenciadas",
        "notifications_turn_off": "Toca para desactivar",
        "notifications_turn_on": "Toca para activar",
        "notifications_blocked": "Los navegadores requieren HTTPS para notificaciones. ¡Alertas de Sonido y Flash 2x activas!",
        "notifications_http_notice": "Los navegadores requieren HTTPS para notificaciones push. ¡Alertas de Sonido y Flash 2x activas!",
        "notifications_redirect_toast": "Abriendo versión HTTPS segura para activar notificaciones...",
        "btn_open_https": "🔒 Abrir Versión HTTPS",
        "notifications_not_supported": "El navegador no admite notificaciones.",
        "scroll_to_bottom": "Ir al final",
        "new_messages_badge": "{count} nueva(s)",
        "task_completed_notify_title": "Antigravity • Tarea Completada",

        # Features v2.4.0 (Menú, QR Code, Latencia, Tonos, Historial/Log)
        "terminal_qr_title": "[CÓDIGO QR - ESCANEA CON LA CÁMARA PARA CONECTAR]:",
        "btn_menu": "⚙️ Menú",
        "btn_menu_title": "Ajustes y Preferencias",
        "menu_title": "Ajustes",
        "menu_notifications_label": "Notificaciones del Navegador",
        "menu_sensory_label": "Alerta Sensorial (Sonido y Destello)",
        "menu_tone_label": "Tono de Alerta",
        "tone_modern": "Chime Moderno",
        "tone_bell": "Campana Zen",
        "tone_scifi": "Pulso Sci-Fi",
        "tone_classic": "Pitido Clásico",
        "menu_volume_label": "Volumen del Tono",
        "menu_latency_label": "Mostrar Latencia en Tiempo Real (Ping)",
        "menu_btn_log": "📜 Ver Historial de Tareas",
        "menu_btn_test_sound": "▶️ Probar Tono",
        "menu_close": "Cerrar",
        "log_title": "Historial de Conclusiones",
        "log_empty": "Aún no hay conclusiones registradas.",
        "log_clear": "Limpiar Historial",
        "log_cleared": "¡Historial borrado con éxito!",
        "latency_label": "Latencia",
        "menu_fullscreen_label": "Modo Pantalla Completa",
        "btn_fullscreen": "Alternar",
        "fullscreen_active": "Pantalla completa activada",
        "fullscreen_disabled": "Pantalla completa desactivada",
        "battery_title": "Batería",
        "btn_prompt": "Prompt",
        "prompt_modal_title": "Enviar Prompt a la PC",
        "prompt_step1_subtitle": "Paso 1: Elige el chat o proyecto de destino",
        "prompt_step2_badge": "Paso 2",
        "prompt_back_btn": "← Volver",
        "prompt_input_label": "Escribe tu solicitud para la IA:",
        "prompt_placeholder": "Escribe aquí lo que deseas que haga Antigravity...",
        "btn_send_prompt": "Enviar a la PC",
        "prompt_sending": "Enviando...",
        "prompt_sent_success": "¡Prompt enviado con éxito a la PC!",
        "prompt_empty_warn": "Por favor, escribe un prompt para enviar.",
        "prompt_error": "Error al enviar el prompt a la PC.",
        "menu_oled_label": "Tema OLED True Black",
        "menu_battery_label": "Mostrar Nivel de Batería",
        "prompt_model_label": "Modelo IA:",
        "menu_sec_alerts": "Alertas y Notificaciones",
        "menu_sec_sound": "Audio y Tonos",
        "menu_sec_system": "Red e Historial",
        "menu_apk_installed_label": "Versión Instalada:",
        "menu_btn_logout": "Salir / Desconectar Sesión",
        "search_chats_placeholder": "Buscar chat o proyecto...",
        "search_no_results": "No se encontraron conversaciones",
        "prompt_history_btn": "Historial",
        "prompt_history_title": "Prompts Recientes",
        "prompt_history_empty": "No hay prompts anteriores registrados.",
        "prompt_history_clear": "Limpiar",
        "prompt_char_counter": "{chars} caracteres • {words} palabras",
        "copy_response": "Copiar respuesta",
        "response_copied": "¡Respuesta copiada al portapapeles!",
        "copy_failed": "Error al copiar respuesta.",
        "thinking_indicator": "Antigravity está pensando...",
        "favorite_chat_title": "Marcar como favorito",
        "unfavorite_chat_title": "Quitar de favoritos",
        "quick_prompts_title": "Atajos rápidos:",
        "snippet_continue": "Continúa",
        "snippet_run_tests": "Ejecuta las pruebas",
        "snippet_summarize": "Resume el progreso",
        "snippet_check_errors": "Verifica errores",
        "share_response": "Compartir respuesta",
        "share_chat_title": "Antigravity Mobile • Respuesta de IA",
        "share_success": "¡Compartido con éxito!"
    }
}

class LanguageManager:
    def __init__(self):
        self.current_lang = self.load_saved_language() or "pt"

    def load_saved_language(self) -> Optional[str]:
        """Carrega o idioma previamente selecionado se existir no arquivo de configuração."""
        if LANGUAGE_FILE.exists():
            try:
                with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    lang = data.get("language", "").lower().strip()
                    if lang in TRANSLATIONS:
                        self.current_lang = lang
                        return lang
            except Exception:
                pass
        return None

    def save_language(self, lang: str):
        """Salva o idioma escolhido para não perguntar novamente."""
        if lang not in TRANSLATIONS:
            lang = "pt"
        self.current_lang = lang
        try:
            with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
                json.dump({"language": lang}, f, indent=2)
        except Exception as e:
            print(f"[LanguageManager] Erro ao salvar idioma: {e}")

    def prompt_language_selection(self, force: bool = False) -> str:
        """Solicita ao usuário a escolha de idioma no terminal, caso não esteja salvo ou forçado."""
        if not force:
            saved = self.load_saved_language()
            if saved:
                self.current_lang = saved
                return saved

        is_interactive = bool(sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty())
        if not is_interactive and not force:
            self.save_language("pt")
            return "pt"

        print("\n" + "=" * 70, flush=True)
        print(" SELECIONE SEU IDIOMA | SELECT YOUR LANGUAGE | SELECCIONE SU IDIOMA", flush=True)
        print("=" * 70, flush=True)
        print("  Português-Brasil, English ou Español", flush=True)
        print("  (Tecla B para Brasil | Press E for English | Tecla S para Español)", flush=True)
        print("=" * 70, flush=True)

        selected = "pt"
        try:
            import msvcrt
            print(" >> Opção / Option / Opción: ", end="", flush=True)
            ch = msvcrt.getch()
            char = ch.decode("utf-8", errors="ignore").lower().strip()
            print(char, flush=True)
            if char in ['b', '1', 'p']:
                selected = "pt"
            elif char in ['e', '2']:
                selected = "en"
            elif char in ['s', '3', 'i']:
                selected = "es"
            else:
                selected = "pt"
        except Exception:
            selected = "pt"

        lang_names = {"pt": "Português (Brasil)", "en": "English", "es": "Español"}
        print(f" [OK] Idioma selecionado: {lang_names.get(selected, selected)}\n", flush=True)
        self.save_language(selected)
        return selected

    def get_dict(self) -> Dict[str, Any]:
        # Recarrega caso o usuário tenha editado o arquivo manualmente
        self.load_saved_language()
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS["pt"])

    def format_quota_desc(self, raw_text: str = "", reset_time_iso: str = "", rem_pct: float = 100.0) -> str:
        """Formata a renovação da cota de forma concisa e elegante (ex: 'Resets in 5d 23h', '100% Available')."""
        lang = self.current_lang

        if rem_pct >= 99.9 and not raw_text:
            if lang == "en":
                return "100% Available"
            elif lang == "es":
                return "100% Disponible"
            else:
                return "100% Disponível"

        # Tenta extrair dias, horas e minutos
        days_m = re.search(r'(\d+)\s*days?', raw_text, re.IGNORECASE)
        hours_m = re.search(r'(\d+)\s*hours?', raw_text, re.IGNORECASE)
        mins_m = re.search(r'(\d+)\s*min', raw_text, re.IGNORECASE)

        d = int(days_m.group(1)) if days_m else 0
        h = int(hours_m.group(1)) if hours_m else 0
        m = int(mins_m.group(1)) if mins_m else 0

        # Se não tiver duração textual mas tiver reset_time ISO
        if d == 0 and h == 0 and m == 0 and reset_time_iso:
            try:
                from datetime import datetime, timezone
                reset_dt = datetime.fromisoformat(reset_time_iso.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                diff = reset_dt - now
                if diff.total_seconds() > 0:
                    d = diff.days
                    h = int(diff.seconds // 3600)
                    m = int((diff.seconds % 3600) // 60)
            except Exception:
                pass

        time_parts = []
        if d > 0:
            time_parts.append(f"{d}d")
        if h > 0:
            time_parts.append(f"{h}h")
        if m > 0 and d == 0:  # Exibe minutos somente se menos de 1 dia restante
            time_parts.append(f"{m}m")

        time_str = " ".join(time_parts) if time_parts else ""

        if not time_str:
            if lang == "en":
                return "100% Available" if rem_pct >= 99.9 else "Refreshes soon"
            elif lang == "es":
                return "100% Disponible" if rem_pct >= 99.9 else "Renueva pronto"
            else:
                return "100% Disponível" if rem_pct >= 99.9 else "Renova em breve"

        if lang == "en":
            return f"Resets in {time_str}"
        elif lang == "es":
            return f"Renueva en {time_str}"
        else:
            return f"Renova em {time_str}"

language_manager = LanguageManager()