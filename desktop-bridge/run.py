# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import subprocess
from pathlib import Path

# Garante que o diretorio do script esta no sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Garante suporte UTF-8 no terminal Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def ensure_dependencies():
    """Verifica e instala automaticamente dependências ausentes (FastAPI, Uvicorn, py7zr, etc.) caso o usuário ainda não as tenha instalado."""
    required = ["fastapi", "uvicorn", "websockets", "pydantic", "qrcode", "py7zr"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        print("\n" + "=" * 68, flush=True)
        print(" [*] ANTIGRAVITY MOBILE - INSTALAÇÃO DE DEPENDÊNCIAS", flush=True)
        print("=" * 68, flush=True)
        print(f" [!] Módulos necessários ausentes: {', '.join(missing)}", flush=True)
        print(" [*] Baixando e instalando automaticamente via pip... Aguarde um momento.\n", flush=True)
        try:
            req_file = SCRIPT_DIR / "requirements.txt"
            if req_file.exists():
                cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_file), "--disable-pip-version-check"]
            else:
                cmd = [sys.executable, "-m", "pip", "install", "fastapi>=0.115.0", "uvicorn[standard]>=0.30.0", "websockets>=13.0", "pydantic>=2.0.0", "--disable-pip-version-check"]
            try:
                subprocess.check_call(cmd)
            except subprocess.CalledProcessError:
                cmd.append("--user")
                subprocess.check_call(cmd)
            print("\n [OK] Todas as dependências foram instaladas com sucesso!\n", flush=True)
        except Exception as e:
            print(f"\n [ERRO] Falha ao instalar dependências automaticamente: {e}", flush=True)
            print(" >> Execute manualmente no terminal: pip install -r requirements.txt\n", flush=True)
            try:
                input("Pressione Enter para fechar...")
            except Exception:
                pass
            sys.exit(1)

ensure_dependencies()

import time
import socket
import threading
import asyncio
import uvicorn
from config import config
from auth import auth_manager
from language_manager import language_manager
import atexit

def get_local_ip() -> str:
    """Detecta o IP da máquina na rede local Wi-Fi/Ethernet."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def print_qr_code(url: str, title: str = ""):
    """Gera e imprime um QR Code compacto em ASCII no console para fácil escaneamento com celular."""
    try:
        import qrcode
        import io
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        buf = io.StringIO()
        qr.print_ascii(out=buf, invert=True)
        lines = [line for line in buf.getvalue().splitlines() if line.strip()]
        if title:
            print(f" {title}", flush=True)
        for line in lines:
            print(f"   {line}", flush=True)
    except Exception:
        pass

MANAGED_RESTART = "--managed" in sys.argv
JUST_UPDATED_MARKER = SCRIPT_DIR / ".just_updated"
active_server = None
restart_requested = threading.Event()

def trigger_in_place_restart():
    """Reinicia o Local Server na mesma janela do terminal após atualização de código."""
    try:
        JUST_UPDATED_MARKER.write_text("1", encoding="utf-8")
    except Exception:
        pass
    if MANAGED_RESTART:
        sys.exit(42)
    else:
        rc = subprocess.call([sys.executable, str(SCRIPT_DIR / "run.py")])
        sys.exit(rc)

def print_banner(local_ip: str):
    port = config.PORT
    t = language_manager.get_dict()
    lang = language_manager.current_lang
    lang_names = {"pt": "Português (Brasil)", "en": "English", "es": "Español"}
    ver_label = t.get("terminal_version", "Versão do Servidor")

    try:
        import updater
        available_update = updater.AVAILABLE_UPDATE
    except Exception:
        available_update = None

    print("\n" + "=" * 68, flush=True)
    print(f"        [*] ANTIGRAVITY MOBILE - {t['terminal_title']} (v{config.VERSION})", flush=True)
    print("                 Desenvolvido por Dev LumiaG5", flush=True)
    print("=" * 68, flush=True)
    print(f" * {ver_label}:             v{config.VERSION}", flush=True)
    print(f" * {t['terminal_local_pc']}:             http://localhost:{port}", flush=True)
    print(f" * {t['terminal_mobile_wifi']}:       http://{local_ip}:{port}", flush=True)
    print(f" * {t['terminal_active_lang']}:         {lang_names.get(lang, lang)}", flush=True)
    if available_update:
        avail_msg = t.get(
            "updater_available_banner",
            "Atualização disponível no GitHub: {version} (pressione [U] para atualizar)"
        ).format(version=available_update)
        print(f" ! {avail_msg}", flush=True)
    print("-" * 68, flush=True)
    
    # Exibe QR Code único para conexão imediata via câmera do celular
    target_url = f"http://{local_ip}:{port}?pin={auth_manager.current_pin}"
    qr_title = t.get("terminal_qr_title", "[QR CODE - ESCANEIE COM A CÂMERA DO CELULAR PARA CONECTAR]:")
    print_qr_code(target_url, qr_title)
    print("-" * 68, flush=True)

    print(f" {t.get('terminal_tutorial_header', 'GUIA RÁPIDO PARA CONECTAR NO CELULAR:')}", flush=True)
    print(f" {t.get('terminal_tutorial_step1', '  1. Conecte o celular na mesma rede Wi-Fi deste computador.')}", flush=True)
    step2 = t.get('terminal_tutorial_step2', '  2. No navegador do celular, abra: http://{ip}:{port}').format(ip=local_ip, port=port)
    print(f" {step2}", flush=True)
    print(f" {t.get('terminal_tutorial_step3', '  3. Digite o PIN gerado no terminal para liberar (salvo em cache por 24h).')}", flush=True)
    print("-" * 68, flush=True)
    btn_pin = t.get("terminal_btn_pin", "[P] Novo PIN")
    btn_lang = t.get("terminal_btn_lang", "[L] Idioma")
    btn_tray = t.get("terminal_btn_tray", "[T] Bandeja")
    if available_update:
        btn_upd = t.get("terminal_btn_update_new", "[U] ATUALIZAR PARA {version}").format(version=available_update)
    else:
        btn_upd = t.get("terminal_btn_update", "[U] Atualizar Servidor (GitHub)")
    actions_lbl = t.get("terminal_actions_label", "ATALHOS DO TERMINAL")
    print(f" {actions_lbl}:", flush=True)
    print(f"   {btn_pin}  |  {btn_lang}  |  {btn_tray}  |  {btn_upd}", flush=True)
    print("-" * 68, flush=True)
    print(f" {t['server_notice']}", flush=True)
    print("=" * 68 + "\n", flush=True)

def start_keyboard_listener(local_ip: str):
    """Thread que detecta pressionamento de tecla para gerar novo PIN, alternar idioma ou atualizar Local Server."""
    def listener():
        try:
            import msvcrt
            while not restart_requested.is_set():
                if msvcrt.kbhit():
                    ch = msvcrt.getch()
                    char_str = ch.decode("utf-8", errors="ignore").lower().strip()
                    if char_str == 'l':
                        # Alterna idioma: pt -> en -> es -> pt
                        cycle = {"pt": "en", "en": "es", "es": "pt"}
                        new_lang = cycle.get(language_manager.current_lang, "pt")
                        language_manager.save_language(new_lang)
                        
                        # Dispara evento para o servidor notificar todos os clientes conectados
                        try:
                            from server import manager
                            loop = asyncio.new_event_loop()
                            loop.run_until_complete(manager.broadcast({
                                "event": "i18n_update",
                                "data": {
                                    "language": new_lang,
                                    "dict": language_manager.get_dict()
                                }
                            }))
                            loop.close()
                        except Exception:
                            pass
                        
                        print_banner(local_ip)
                    elif char_str == 't':
                        # Tecla T: Minimiza o terminal para a bandeja do Windows (System Tray)
                        try:
                            from tray import tray_manager
                            if tray_manager.is_supported():
                                tray_manager.hide_console(notify=True)
                        except Exception:
                            pass
                    elif char_str == 'u':
                        # Tecla U: Botão para verificar e atualizar o Local Server via GitHub
                        from updater import check_and_update_local_server
                        if check_and_update_local_server(force_check=False, ask_confirmation=True, server_running=True):
                            restart_requested.set()
                            if active_server is not None:
                                active_server.should_exit = True
                            break
                        print_banner(local_ip)
                    else:
                        # Tecla P ou qualquer outra tecla: gera novo PIN e atualiza o banner
                        auth_manager.generate_pin(notify=False)
                        print_banner(local_ip)
                time.sleep(0.12)
        except Exception:
            pass

    t = threading.Thread(target=listener, daemon=True)
    t.start()

def main():
    global active_server

    # 1. Solicita e salva o idioma do usuário se ainda não estiver configurado
    language_manager.prompt_language_selection()

    # 1.1. Verificação inicial de atualização no GitHub (usuário decide S/N se houver versão nova)
    if JUST_UPDATED_MARKER.exists():
        try:
            JUST_UPDATED_MARKER.unlink()
        except Exception:
            pass
    else:
        from updater import check_and_update_local_server
        if check_and_update_local_server(force_check=False, ask_confirmation=True, server_running=False):
            trigger_in_place_restart()

    # 2. Detecta IP e imprime o banner único no idioma selecionado com PIN inicial, QR Code e botões de atalho
    local_ip = get_local_ip()
    print_banner(local_ip)

    # 3. Inicia escuta de teclado (P = novo PIN, L = idioma, T = bandeja, U = atualizar servidor no GitHub)
    start_keyboard_listener(local_ip)

    # 3.1. Inicia ícone na bandeja do Windows (System Tray) se disponível
    try:
        from tray import tray_manager
        if tray_manager.is_supported():
            def _tray_new_pin():
                auth_manager.generate_pin(notify=False)
                print_banner(local_ip)

            def _tray_check_update():
                from updater import check_and_update_local_server
                if check_and_update_local_server(force_check=False, ask_confirmation=True, server_running=True):
                    restart_requested.set()
                    if active_server is not None:
                        active_server.should_exit = True
                else:
                    print_banner(local_ip)

            def _tray_exit():
                if active_server is not None:
                    active_server.should_exit = True

            tray_manager.start(
                icon_png=SCRIPT_DIR / "static" / "antigravity-icon.png",
                on_new_pin=_tray_new_pin,
                on_check_update=_tray_check_update,
                on_exit=_tray_exit,
                get_url=lambda: f"http://localhost:{config.PORT}?pin={auth_manager.current_pin}",
                get_labels=language_manager.get_dict,
            )
    except Exception:
        pass

    # 4. Inicia o servidor uvicorn gerenciado (permite reinício limpo caso arquivos Python sejam atualizados)
    uvi_config = uvicorn.Config(
        "server:app",
        host=config.HOST,
        port=config.PORT,
        log_level="warning",
        access_log=False,
        reload=False
    )
    active_server = uvicorn.Server(uvi_config)
    try:
        active_server.run()
    finally:
        try:
            from tray import tray_manager
            tray_manager.stop()
        except Exception:
            pass

    if restart_requested.is_set():
        trigger_in_place_restart()

if __name__ == "__main__":
    main()