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
        "terminal_version": "Versão do Servidor",
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
        "press_key_notice": "Ações: [P] Novo PIN  |  [L] Trocar idioma  |  [U] Atualizar Local Server",
        "terminal_actions_label": "ATALHOS DO TERMINAL",
        "terminal_btn_pin": "[P] Novo PIN",
        "terminal_btn_lang": "[L] Idioma",
        "terminal_btn_update": "[U] Atualizar Servidor (GitHub)",
        "terminal_btn_update_new": "[U] ATUALIZAR PARA {version}",
        
        # Atualizador do Local Server no Terminal
        "updater_checking": "Verificando atualizações do Local Server no GitHub...",
        "updater_retry": "Falha na tentativa {attempt}. Tentando novamente em instantes ({attempt}/{total})...",
        "updater_failed": "Não foi possível verificar atualizações no momento (sem conexão com GitHub). Continuando inicialização...",
        "updater_up_to_date": "Local Server já está na versão mais recente ({version})!",
        "updater_found": "Nova versão encontrada: {new_version} (versão atual: {current_version})",
        "updater_ask_confirm": "Deseja atualizar o Local Server agora? [S/N]:",
        "updater_cancelled": "Atualização adiada. Pressione [U] no terminal quando quiser atualizar.",
        "updater_downloading": "Baixando atualização do Local Server...",
        "updater_extracting": "Extraindo e atualizando arquivos do servidor...",
        "updater_success_title": "ATUALIZAÇÃO DO SERVIDOR CONCLUÍDA COM SUCESSO!",
        "updater_restart_prompt": "Os arquivos do Local Server foram atualizados para a versão {version}.\n Por favor, feche esta janela do terminal e abra-a novamente para carregar as alterações.",
        "updater_no_restart_needed": "Atualizado para {version} sem precisar reiniciar o servidor!",
        "updater_auto_restarting": "Atualização aplicada ({version}). Reiniciando o servidor automaticamente nesta janela...",
        "updater_available_banner": "Atualização disponível no GitHub: {version} (pressione [U] para atualizar)",
        "updater_press_enter": "Pressione Enter para encerrar este terminal...",
        "updater_no_asset": "Nova versão {new_version} encontrada, mas nenhum arquivo de pacote do Local Server foi disponibilizado no release.",
        "updater_files_identical": "Todos os arquivos locais já estão atualizados e idênticos aos do GitHub!",
        
        # Web / Mobile App UI
        "pin_badge": "ACESSO LOCAL",
        "pin_instruction": "Digite o PIN de 4 dígitos exibido no terminal do PC.",
        "btn_unlock": "Conectar",
        "btn_new_pin": "Gerar novo PIN",
        "pin_verifying": "Verificando...",
        "pin_authorized": "Conectado!",
        "pin_error": "PIN incorreto. Confira no terminal do PC.",
        
        "quota_5h_title": "Limite 5 Horas",
        "quota_weekly_title": "Limite Semanal",
        "quota_syncing": "Sincronizando...",
        "quota_available": "100% Disponível",
        
        "empty_title": "Nenhuma atividade ainda",
        "empty_sub": "As respostas aparecem aqui quando uma tarefa rodar no PC.",
        "footer_alert": "Som e Flash",
        "footer_test_btn": "Testar alerta",
        "msg_user": "Você",
        "msg_assistant": "Antigravity",
        
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
        "btn_check_update": "Verificar atualização",
        "update_up_to_date": "O app já está atualizado!",
        "update_available": "Nova versão encontrada: ",
        "update_downloading": "Baixando atualização do APK...",

        # Botão e Modal de Chats
        "btn_chats": "Chats",
        "chats_modal_title": "Conversas no PC",
        "chats_current_pc": "No PC",
        "chats_live_pc_btn": "Voltar ao chat ativo",
        "chats_viewing_custom": "Vendo outra conversa",
        "chats_no_active": "Nenhuma conversa encontrada",
        "chats_error": "Erro ao carregar conversas do PC.",
        
        # Tutorial de Conexão Rápido
        "tutorial_btn": "Como conectar",
        "tutorial_title": "Como conectar",
        "tutorial_step1_title": "1. Mesma rede Wi-Fi",
        "tutorial_step1_desc": "Deixe o computador e o celular conectados no mesmo Wi-Fi.",
        "tutorial_step2_title": "2. Abra o endereço no celular",
        "tutorial_step2_desc": "Digite o endereço IP exibido no terminal (ex: http://192.168.0.6:8765) ou escaneie o QR Code.",
        "tutorial_step3_title": "3. Informe o PIN",
        "tutorial_step3_desc": "Digite os 4 números mostrados no terminal. A sessão fica salva por 24 horas.",
        "tutorial_step4_title": "4. Tudo pronto",
        "tutorial_step4_desc": "Acompanhe respostas, uso do modelo e envie prompts direto do celular.",
        "tutorial_btn_close": "Fechar",

        # Features v2.2.0 (OLED, Notificações, Scroll, Workspace)
        "project_label": "Projeto",
        "project_title_prefix": "Projeto: ",
        "btn_oled": "OLED",
        "oled_active": "Modo OLED ativo",
        "oled_disabled": "Modo OLED desativado",
        "btn_notifications": "Notificações",
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
        "btn_menu": "Menu",
        "btn_menu_title": "Configurações",
        "menu_title": "Configurações",
        "menu_notifications_label": "Notificações no navegador",
        "menu_sensory_label": "Som e flash de alerta",
        "menu_tone_label": "Toque",
        "tone_modern": "Chime moderno",
        "tone_bell": "Sino",
        "tone_scifi": "Pulso",
        "tone_classic": "Bip clássico",
        "menu_volume_label": "Volume",
        "menu_latency_label": "Mostrar latência (ping)",
        "menu_btn_log": "Histórico de conclusões",
        "menu_btn_test_sound": "Testar toque",
        "menu_close": "Fechar",
        "log_title": "Histórico de conclusões",
        "log_empty": "Nenhuma conclusão registrada ainda.",
        "log_clear": "Limpar",
        "log_cleared": "Histórico limpo.",
        "latency_label": "Latência",
        "menu_fullscreen_label": "Tela cheia",
        "btn_fullscreen": "Alternar",
        "fullscreen_active": "Tela cheia ativada",
        "fullscreen_disabled": "Tela cheia desativada",
        "battery_title": "Bateria",
        "btn_prompt": "Prompt",
        "prompt_modal_title": "Enviar prompt",
        "prompt_step1_subtitle": "Escolha a conversa de destino",
        "prompt_step2_badge": "Mensagem",
        "prompt_back_btn": "← Voltar",
        "prompt_input_label": "Mensagem:",
        "prompt_placeholder": "Escreva seu prompt...",
        "btn_send_prompt": "Enviar",
        "prompt_sending": "Enviando...",
        "prompt_sent_success": "Prompt enviado ao PC!",
        "prompt_empty_warn": "Digite um prompt antes de enviar.",
        "prompt_error": "Não foi possível enviar o prompt ao PC.",
        "menu_oled_label": "Modo OLED puro",
        "menu_battery_label": "Mostrar bateria",
        "prompt_model_label": "Modelo:",
        "menu_sec_alerts": "Alertas",
        "menu_sec_sound": "Áudio",
        "menu_sec_system": "Sistema",
        "menu_apk_installed_label": "Versão instalada:",
        "menu_btn_logout": "Sair da sessão",
        "search_chats_placeholder": "Buscar chat ou projeto...",
        "search_no_results": "Nenhuma conversa encontrada",
        "prompt_history_btn": "Recentes",
        "prompt_history_title": "Prompts recentes",
        "prompt_history_empty": "Nenhum prompt recente.",
        "prompt_history_clear": "Limpar",
        "prompt_char_counter": "{chars} caracteres • {words} palavras",
        "copy_response": "Copiar resposta",
        "response_copied": "Copiado para a área de transferência.",
        "copy_failed": "Não foi possível copiar.",
        "thinking_indicator": "Antigravity está pensando...",
        "favorite_chat_title": "Fixar conversa",
        "unfavorite_chat_title": "Desafixar conversa",
        "quick_prompts_title": "Atalhos:",
        "snippet_continue": "Continue",
        "snippet_run_tests": "Rode os testes",
        "snippet_summarize": "Resuma o progresso",
        "snippet_check_errors": "Verifique erros",
        "share_response": "Compartilhar resposta",
        "share_chat_title": "Antigravity Mobile",
        "share_success": "Compartilhado!"
    },
    "en": {
        "lang_code": "en-US",
        "lang_name": "English",
        "title": "Antigravity Mobile",
        
        # Terminal strings
        "terminal_title": "DESKTOP BRIDGE DAEMON",
        "terminal_version": "Server Version",
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
        "press_key_notice": "Actions: [P] New PIN  |  [L] Language  |  [U] Update Local Server",
        "terminal_actions_label": "TERMINAL ACTIONS",
        "terminal_btn_pin": "[P] New PIN",
        "terminal_btn_lang": "[L] Language",
        "terminal_btn_update": "[U] Update Server (GitHub)",
        "terminal_btn_update_new": "[U] UPDATE TO {version}",
        
        # Local Server Terminal Updater
        "updater_checking": "Checking for Local Server updates on GitHub...",
        "updater_retry": "Attempt {attempt} failed. Retrying shortly ({attempt}/{total})...",
        "updater_failed": "Unable to check for updates at this time (could not reach GitHub). Continuing startup...",
        "updater_up_to_date": "Local Server is up to date ({version})!",
        "updater_found": "New version available: {new_version} (current version: {current_version})",
        "updater_ask_confirm": "Do you want to update Local Server now? [Y/N]:",
        "updater_cancelled": "Update postponed. Press [U] in the terminal whenever you want to update.",
        "updater_downloading": "Downloading Local Server update...",
        "updater_extracting": "Extracting and updating server files...",
        "updater_success_title": "LOCAL SERVER UPDATE INSTALLED SUCCESSFULLY!",
        "updater_restart_prompt": "Local Server files have been updated to version {version}.\n Please close this terminal window and reopen it to apply the new version.",
        "updater_no_restart_needed": "Updated to {version} without needing to restart the server!",
        "updater_auto_restarting": "Update applied ({version}). Restarting server automatically in this window...",
        "updater_available_banner": "Update available on GitHub: {version} (press [U] to update)",
        "updater_press_enter": "Press Enter to close this terminal...",
        "updater_no_asset": "New version {new_version} found, but no Local Server archive asset was found in the release.",
        "updater_files_identical": "All local files are already up to date and identical to GitHub!",
        
        # Web / Mobile App UI
        "pin_badge": "LOCAL ACCESS",
        "pin_instruction": "Enter the 4-digit PIN shown in the PC terminal.",
        "btn_unlock": "Connect",
        "btn_new_pin": "New PIN",
        "pin_verifying": "Checking...",
        "pin_authorized": "Connected!",
        "pin_error": "Wrong PIN. Check the PC terminal.",
        
        "quota_5h_title": "5-Hour Limit",
        "quota_weekly_title": "Weekly Limit",
        "quota_syncing": "Syncing...",
        "quota_available": "100% Available",
        
        "empty_title": "No activity yet",
        "empty_sub": "Responses will show up here when a task runs on your PC.",
        "footer_alert": "Sound & Flash",
        "footer_test_btn": "Test alert",
        "msg_user": "You",
        "msg_assistant": "Antigravity",
        
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
        "btn_check_update": "Check for updates",
        "update_up_to_date": "App is already up to date.",
        "update_available": "New version found: ",
        "update_downloading": "Downloading APK update...",

        # Chats Button and Modal
        "btn_chats": "Chats",
        "chats_modal_title": "PC Chats",
        "chats_current_pc": "On PC",
        "chats_live_pc_btn": "Back to active chat",
        "chats_viewing_custom": "Viewing another chat",
        "chats_no_active": "No conversations found",
        "chats_error": "Could not load PC chats.",
        
        # Quick Connection Tutorial
        "tutorial_btn": "How to connect",
        "tutorial_title": "How to connect",
        "tutorial_step1_title": "1. Same Wi-Fi",
        "tutorial_step1_desc": "Make sure your PC and phone are on the same Wi-Fi network.",
        "tutorial_step2_title": "2. Open the local address",
        "tutorial_step2_desc": "Enter the IP address shown in the terminal (e.g. http://192.168.0.6:8765) or scan the QR Code.",
        "tutorial_step3_title": "3. Enter the PIN",
        "tutorial_step3_desc": "Type the 4 digits displayed on the PC terminal. The session stays cached for 24 hours.",
        "tutorial_step4_title": "4. Ready",
        "tutorial_step4_desc": "Follow replies, check quota usage, and send prompts from your phone.",
        "tutorial_btn_close": "Close",

        # Features v2.2.0 (OLED, Notifications, Scroll, Workspace)
        "project_label": "Project",
        "project_title_prefix": "Project: ",
        "btn_oled": "OLED",
        "oled_active": "OLED mode enabled",
        "oled_disabled": "OLED mode disabled",
        "btn_notifications": "Notifications",
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
        "btn_menu": "Menu",
        "btn_menu_title": "Settings",
        "menu_title": "Settings",
        "menu_notifications_label": "Browser notifications",
        "menu_sensory_label": "Sound and flash alert",
        "menu_tone_label": "Ringtone",
        "tone_modern": "Modern Chime",
        "tone_bell": "Bell",
        "tone_scifi": "Pulse",
        "tone_classic": "Classic Beep",
        "menu_volume_label": "Volume",
        "menu_latency_label": "Show latency (ping)",
        "menu_btn_log": "Task history",
        "menu_btn_test_sound": "Test sound",
        "menu_close": "Close",
        "log_title": "Task history",
        "log_empty": "No completed tasks recorded yet.",
        "log_clear": "Clear",
        "log_cleared": "History cleared.",
        "latency_label": "Latency",
        "menu_fullscreen_label": "Fullscreen",
        "btn_fullscreen": "Toggle",
        "fullscreen_active": "Fullscreen enabled",
        "fullscreen_disabled": "Fullscreen disabled",
        "battery_title": "Battery",
        "btn_prompt": "Prompt",
        "prompt_modal_title": "Send prompt",
        "prompt_step1_subtitle": "Choose target conversation",
        "prompt_step2_badge": "Message",
        "prompt_back_btn": "← Back",
        "prompt_input_label": "Message:",
        "prompt_placeholder": "Write your prompt...",
        "btn_send_prompt": "Send",
        "prompt_sending": "Sending...",
        "prompt_sent_success": "Prompt sent to PC!",
        "prompt_empty_warn": "Type a prompt before sending.",
        "prompt_error": "Could not send prompt to PC.",
        "menu_oled_label": "Pure OLED mode",
        "menu_battery_label": "Show battery",
        "prompt_model_label": "Model:",
        "menu_sec_alerts": "Alerts",
        "menu_sec_sound": "Audio",
        "menu_sec_system": "System",
        "menu_apk_installed_label": "Installed version:",
        "menu_btn_logout": "Sign out",
        "search_chats_placeholder": "Search chat or project...",
        "search_no_results": "No conversations found",
        "prompt_history_btn": "Recent",
        "prompt_history_title": "Recent prompts",
        "prompt_history_empty": "No recent prompts.",
        "prompt_history_clear": "Clear",
        "prompt_char_counter": "{chars} chars • {words} words",
        "copy_response": "Copy response",
        "response_copied": "Copied to clipboard.",
        "copy_failed": "Could not copy.",
        "thinking_indicator": "Antigravity is thinking...",
        "favorite_chat_title": "Pin chat",
        "unfavorite_chat_title": "Unpin chat",
        "quick_prompts_title": "Shortcuts:",
        "snippet_continue": "Continue",
        "snippet_run_tests": "Run tests",
        "snippet_summarize": "Summarize progress",
        "snippet_check_errors": "Check errors",
        "share_response": "Share response",
        "share_chat_title": "Antigravity Mobile",
        "share_success": "Shared!"
    },
    "es": {
        "lang_code": "es-ES",
        "lang_name": "Español",
        "title": "Antigravity Mobile",
        
        # Terminal strings
        "terminal_title": "SERVIDOR DESKTOP BRIDGE",
        "terminal_version": "Versión del Servidor",
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
        "press_key_notice": "Acciones: [P] Nuevo PIN  |  [L] Idioma  |  [U] Actualizar Local Server",
        "terminal_actions_label": "ATAJOS DE TERMINAL",
        "terminal_btn_pin": "[P] Nuevo PIN",
        "terminal_btn_lang": "[L] Idioma",
        "terminal_btn_update": "[U] Actualizar Servidor (GitHub)",
        "terminal_btn_update_new": "[U] ACTUALIZAR A {version}",
        
        # Actualizador de Local Server en Terminal
        "updater_checking": "Buscando actualizaciones de Local Server en GitHub...",
        "updater_retry": "El intento {attempt} falló. Reintentando en breve ({attempt}/{total})...",
        "updater_failed": "No fue posible comprobar actualizaciones en este momento (sin conexión con GitHub). Continuando inicio...",
        "updater_up_to_date": "¡Local Server ya está en la versión más reciente ({version})!",
        "updater_found": "Nueva versión encontrada: {new_version} (versión actual: {current_version})",
        "updater_ask_confirm": "¿Desea actualizar Local Server ahora? [S/N]:",
        "updater_cancelled": "Actualización pospuesta. Presione [U] en la terminal cuando quiera actualizar.",
        "updater_downloading": "Descargando actualización de Local Server...",
        "updater_extracting": "Extrayendo y actualizando archivos del servidor...",
        "updater_success_title": "¡ACTUALIZACIÓN DEL SERVIDOR COMPLETADA CON ÉXITO!",
        "updater_restart_prompt": "Los archivos de Local Server se actualizaron a la versión {version}.\n Por favor, cierre esta ventana de terminal y ábrala de nuevo para cargar la nueva versión.",
        "updater_no_restart_needed": "¡Actualizado a {version} sin necesidad de reiniciar el servidor!",
        "updater_auto_restarting": "Actualización aplicada ({version}). Reiniciando el servidor automáticamente en esta ventana...",
        "updater_available_banner": "Actualización disponible en GitHub: {version} (presione [U] para actualizar)",
        "updater_press_enter": "Presione Enter para cerrar este terminal...",
        "updater_no_asset": "Se encontró la nueva versión {new_version}, pero no hay paquete de Local Server disponible en el release.",
        "updater_files_identical": "¡Todos los archivos locales ya están actualizados e idénticos a los de GitHub!",
        
        # Web / Mobile App UI
        "pin_badge": "ACCESO LOCAL",
        "pin_instruction": "Ingresa el PIN de 4 dígitos mostrado en la terminal de la PC.",
        "btn_unlock": "Conectar",
        "btn_new_pin": "Nuevo PIN",
        "pin_verifying": "Verificando...",
        "pin_authorized": "¡Conectado!",
        "pin_error": "PIN incorrecto. Revisa la terminal de la PC.",
        
        "quota_5h_title": "Límite 5 Horas",
        "quota_weekly_title": "Límite Semanal",
        "quota_syncing": "Sincronizando...",
        "quota_available": "100% Disponible",
        
        "empty_title": "Sin actividad aún",
        "empty_sub": "Las respuestas aparecerán aquí cuando ejecutes una tarea en la PC.",
        "footer_alert": "Sonido y Flash",
        "footer_test_btn": "Probar alerta",
        "msg_user": "Tú",
        "msg_assistant": "Antigravity",
        
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
        "menu_update_section_title": "App Android",
        "btn_check_update": "Buscar actualización",
        "update_up_to_date": "La app ya está actualizada.",
        "update_available": "Nueva versión encontrada: ",
        "update_downloading": "Descargando actualización APK...",

        # Botón y Modal de Chats
        "btn_chats": "Chats",
        "chats_modal_title": "Chats en PC",
        "chats_current_pc": "En PC",
        "chats_live_pc_btn": "Volver al chat activo",
        "chats_viewing_custom": "Viendo otro chat",
        "chats_no_active": "No se encontraron conversaciones",
        "chats_error": "No se pudieron cargar los chats de la PC.",
        
        # Tutorial de Conexión Rápido
        "tutorial_btn": "Cómo conectar",
        "tutorial_title": "Cómo conectar",
        "tutorial_step1_title": "1. Misma red Wi-Fi",
        "tutorial_step1_desc": "Asegúrate de que la PC y el teléfono estén en la misma red Wi-Fi.",
        "tutorial_step2_title": "2. Abre la dirección local",
        "tutorial_step2_desc": "Ingresa la dirección IP de la terminal (ej: http://192.168.0.6:8765) o escanea el código QR.",
        "tutorial_step3_title": "3. Ingresa el PIN",
        "tutorial_step3_desc": "Escribe los 4 dígitos mostrados en la terminal. La sesión se guarda por 24 horas.",
        "tutorial_step4_title": "4. Listo",
        "tutorial_step4_desc": "Sigue las respuestas, revisa el uso del modelo y envía prompts desde el móvil.",
        "tutorial_btn_close": "Cerrar",

        # Features v2.2.0 (OLED, Notificaciones, Scroll, Workspace)
        "project_label": "Proyecto",
        "project_title_prefix": "Proyecto: ",
        "btn_oled": "OLED",
        "oled_active": "Modo OLED activado",
        "oled_disabled": "Modo OLED desactivado",
        "btn_notifications": "Notificaciones",
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
        "btn_menu": "Menú",
        "btn_menu_title": "Ajustes",
        "menu_title": "Ajustes",
        "menu_notifications_label": "Notificaciones en navegador",
        "menu_sensory_label": "Sonido y flash de alerta",
        "menu_tone_label": "Tono",
        "tone_modern": "Chime moderno",
        "tone_bell": "Campana",
        "tone_scifi": "Pulso",
        "tone_classic": "Pitido clásico",
        "menu_volume_label": "Volumen",
        "menu_latency_label": "Mostrar latencia (ping)",
        "menu_btn_log": "Historial de tareas",
        "menu_btn_test_sound": "Probar tono",
        "menu_close": "Cerrar",
        "log_title": "Historial de tareas",
        "log_empty": "Aún no hay conclusiones registradas.",
        "log_clear": "Limpiar",
        "log_cleared": "Historial borrado.",
        "latency_label": "Latencia",
        "menu_fullscreen_label": "Pantalla completa",
        "btn_fullscreen": "Alternar",
        "fullscreen_active": "Pantalla completa activada",
        "fullscreen_disabled": "Pantalla completa desactivada",
        "battery_title": "Batería",
        "btn_prompt": "Prompt",
        "prompt_modal_title": "Enviar prompt",
        "prompt_step1_subtitle": "Elige la conversación de destino",
        "prompt_step2_badge": "Mensaje",
        "prompt_back_btn": "← Volver",
        "prompt_input_label": "Mensaje:",
        "prompt_placeholder": "Escribe tu prompt...",
        "btn_send_prompt": "Enviar",
        "prompt_sending": "Enviando...",
        "prompt_sent_success": "¡Prompt enviado a la PC!",
        "prompt_empty_warn": "Escribe un prompt antes de enviar.",
        "prompt_error": "No se pudo enviar el prompt a la PC.",
        "menu_oled_label": "Modo OLED puro",
        "menu_battery_label": "Mostrar batería",
        "prompt_model_label": "Modelo:",
        "menu_sec_alerts": "Alertas",
        "menu_sec_sound": "Audio",
        "menu_sec_system": "Sistema",
        "menu_apk_installed_label": "Versión instalada:",
        "menu_btn_logout": "Cerrar sesión",
        "search_chats_placeholder": "Buscar chat o proyecto...",
        "search_no_results": "No se encontraron conversaciones",
        "prompt_history_btn": "Recientes",
        "prompt_history_title": "Prompts recientes",
        "prompt_history_empty": "No hay prompts recientes.",
        "prompt_history_clear": "Limpiar",
        "prompt_char_counter": "{chars} caracteres • {words} palabras",
        "copy_response": "Copiar respuesta",
        "response_copied": "Copiado al portapapeles.",
        "copy_failed": "No se pudo copiar.",
        "thinking_indicator": "Antigravity está pensando...",
        "favorite_chat_title": "Fijar chat",
        "unfavorite_chat_title": "Quitar de fijados",
        "quick_prompts_title": "Atajos:",
        "snippet_continue": "Continúa",
        "snippet_run_tests": "Ejecuta las pruebas",
        "snippet_summarize": "Resume el progreso",
        "snippet_check_errors": "Verifica errores",
        "share_response": "Compartir respuesta",
        "share_chat_title": "Antigravity Mobile",
        "share_success": "¡Compartido!"
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