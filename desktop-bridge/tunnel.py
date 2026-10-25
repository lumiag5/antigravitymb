# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import re
import time
import socket
import urllib.request
import subprocess
import threading
from pathlib import Path
from typing import Optional

BIN_DIR = Path(__file__).parent / "bin"
CLOUDFLARED_EXE = BIN_DIR / "cloudflared.exe"
DOWNLOAD_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"

class TunnelManager:
    def __init__(self):
        self.process: Optional[subprocess.Popen] = None
        self.public_url: Optional[str] = None
        self.is_starting: bool = False
        self._lock = threading.Lock()

    def ensure_binary(self) -> bool:
        """Garante que o executável oficial do cloudflared exista localmente."""
        if CLOUDFLARED_EXE.exists() and CLOUDFLARED_EXE.stat().st_size > 1000000:
            return True

        BIN_DIR.mkdir(parents=True, exist_ok=True)
        print("[Tunnel] Baixando binário oficial Cloudflare Tunnel para HTTPS gratuito...", flush=True)
        try:
            req = urllib.request.Request(DOWNLOAD_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as resp, open(CLOUDFLARED_EXE, "wb") as f:
                f.write(resp.read())
            print("[Tunnel] Cloudflare Tunnel pronto para uso!", flush=True)
            return True
        except Exception as e:
            print(f"[Tunnel] Erro ao baixar Cloudflare Tunnel: {e}", flush=True)
            return False

    def start_tunnel(self, port: int = 8765, timeout: int = 20) -> Optional[str]:
        """Inicia o túnel Cloudflare seguro e extrai a URL pública HTTPS válida."""
        with self._lock:
            if self.public_url:
                return self.public_url

            if not self.ensure_binary():
                return None

            try:
                # Inicia o processo cloudflared criando um Quick Tunnel gratuito com SSL válido
                self.process = subprocess.Popen(
                    [
                        str(CLOUDFLARED_EXE.resolve()),
                        "tunnel",
                        "--url",
                        f"http://127.0.0.1:{port}",
                        "--no-autoupdate"
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    encoding="utf-8",
                    errors="ignore"
                )

                # Monitora a saída até extrair a URL HTTPS .trycloudflare.com
                start_time = time.time()
                while time.time() - start_time < timeout:
                    line = self.process.stdout.readline()
                    if not line:
                        time.sleep(0.08)
                        continue
                    m = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
                    if m:
                        self.public_url = m.group(0).strip()
                        break

                # Inicia thread em background para drenar logs do túnel e evitar travamento de buffer
                def drain_output():
                    try:
                        while self.process and self.process.poll() is None:
                            self.process.stdout.readline()
                    except Exception:
                        pass

                t = threading.Thread(target=drain_output, daemon=True)
                t.start()

                return self.public_url
            except Exception as e:
                print(f"[Tunnel] Falha ao iniciar túnel Cloudflare: {e}", flush=True)
                return None

    def stop_tunnel(self):
        """Encerra o túnel com segurança ao desligar o servidor."""
        with self._lock:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=2)
                except Exception:
                    try:
                        self.process.kill()
                    except Exception:
                        pass
                self.process = None
                self.public_url = None

tunnel_manager = TunnelManager()
