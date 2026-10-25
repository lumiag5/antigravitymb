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
    """Verifica e instala automaticamente dependências ausentes (FastAPI, Uvicorn, etc.) caso o usuário ainda não as tenha instalado."""
    required = ["fastapi", "uvicorn", "websockets", "pydantic", "qrcode"]
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
from tunnel import tunnel_manager
import atexit

atexit.register(tunnel_manager.stop_tunnel)

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

def print_banner(local_ip: str):
    port = config.PORT
    t = language_manager.get_dict()
    lang = language_manager.current_lang
    lang_names = {"pt": "Português (Brasil)", "en": "English", "es": "Español"}

    print("\n" + "=" * 68, flush=True)
    print(f"        [*] ANTIGRAVITY MOBILE - {t['terminal_title']}", flush=True)
    print("                 Desenvolvido por Dev LumiaG5", flush=True)
    print("=" * 68, flush=True)
    print(f" * {t['terminal_local_pc']}:             http://localhost:{port}", flush=True)
    print(f" * {t['terminal_mobile_wifi']}:       http://{local_ip}:{port}", flush=True)
    if tunnel_manager.public_url:
        https_label = t.get("terminal_mobile_https", "Mobile (HTTPS Seguro)")
        print(f" * {https_label}:     {tunnel_manager.public_url}", flush=True)
    print(f" * {t['terminal_active_lang']}:         {lang_names.get(lang, lang)}", flush=True)
    print("-" * 68, flush=True)
    
    # Exibe QR Code para conexão imediata via câmera do celular
    base_target = tunnel_manager.public_url if tunnel_manager.public_url else f"http://{local_ip}:{port}"
    target_url = f"{base_target}?pin={auth_manager.current_pin}"
    qr_title = t.get("terminal_qr_title", "[QR CODE - ESCANEIE COM A CÂMERA DO CELULAR PARA CONECTAR]:")
    print_qr_code(target_url, qr_title)
    print("-" * 68, flush=True)

    print(f" {t.get('terminal_tutorial_header', 'GUIA RÁPIDO PARA CONECTAR NO CELULAR:')}", flush=True)
    print(f" {t.get('terminal_tutorial_step1', '  1. Conecte o celular na mesma rede Wi-Fi deste computador.')}", flush=True)
    step2 = t.get('terminal_tutorial_step2', '  2. No navegador do celular, abra: http://{ip}:{port}').format(ip=local_ip, port=port)
    print(f" {step2}", flush=True)
    print(f" {t.get('terminal_tutorial_step3', '  3. Digite o PIN gerado no terminal para liberar (salvo em cache por 24h).')}", flush=True)
    if t.get('terminal_tutorial_step4'):
        print(f" {t['terminal_tutorial_step4']}", flush=True)
    print("-" * 68, flush=True)
    print(f" {t['server_notice']}", flush=True)
    print(f" {t['press_key_notice']}", flush=True)
    print("=" * 68 + "\n", flush=True)

def start_keyboard_listener(local_ip: str):
    """Thread que detecta pressionamento de tecla para gerar novo PIN ou alternar idioma em tempo real."""
    def listener():
        try:
            import msvcrt
            while True:
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
                    else:
                        # Qualquer outra tecla: gera novo PIN e atualiza o banner
                        auth_manager.generate_pin(notify=False)
                        print_banner(local_ip)
                time.sleep(0.12)
        except Exception:
            pass

    t = threading.Thread(target=listener, daemon=True)
    t.start()

def main():
    # 1. Solicita e salva o idioma do usuário se ainda não estiver configurado
    language_manager.prompt_language_selection()

    # 2. Detecta IP e imprime o banner no idioma selecionado com PIN inicial
    local_ip = get_local_ip()
    print_banner(local_ip)

    # 3. Inicia o túnel Cloudflare HTTPS em segundo plano para notificações e acesso seguro
    def run_tunnel():
        url = tunnel_manager.start_tunnel(port=config.PORT)
        if url:
            print_banner(local_ip)
            try:
                from server import manager
                loop = asyncio.new_event_loop()
                loop.run_until_complete(manager.broadcast({
                    "event": "tunnel_ready",
                    "data": {"https_url": url}
                }))
                loop.close()
            except Exception:
                pass

    threading.Thread(target=run_tunnel, daemon=True).start()

    # 4. Inicia escuta de teclado (gerar novo PIN ou pressionar L para alternar idioma)
    start_keyboard_listener(local_ip)

    # 5. Inicia o servidor uvicorn sem access_log ruidoso (elimina o spam de 403 no terminal)
    uvicorn.run(
        "server:app",
        host=config.HOST,
        port=config.PORT,
        log_level="warning",
        access_log=False,
        reload=False,
        app_dir=str(SCRIPT_DIR)
    )

if __name__ == "__main__":
    main()