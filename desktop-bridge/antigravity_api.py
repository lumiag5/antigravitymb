# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import re
import ssl
import json
import urllib.request
import subprocess
from typing import Optional, Dict, Any, List

class AntigravityLocalAPI:
    """Cliente para comunicar com o Language Server local do Antigravity."""
    
    def __init__(self):
        self.csrf_token: Optional[str] = None
        self.port: Optional[int] = None
        self._ssl_ctx = ssl.create_default_context()
        self._ssl_ctx.check_hostname = False
        self._ssl_ctx.verify_mode = ssl.CERT_NONE
        
    def discover_connection(self) -> bool:
        """Descobre automaticamente a porta HTTPS e o CSRF token do processo language_server.exe."""
        try:
            ps_cmd = (
                "Get-CimInstance Win32_Process -Filter \"Name = 'language_server.exe'\" | "
                "Select-Object ProcessId, CommandLine | ConvertTo-Json"
            )
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_cmd],
                capture_output=True,
                text=True,
                timeout=5
            )
            if not res.stdout.strip():
                return False
                
            data = json.loads(res.stdout)
            if isinstance(data, list):
                data = data[0]
                
            pid = data.get("ProcessId")
            cmdline = data.get("CommandLine", "")
            
            csrf_match = re.search(r"--csrf_token\s+([a-f0-9-]+)", cmdline)
            if not csrf_match:
                return False
            self.csrf_token = csrf_match.group(1)
            
            # Descobre portas LISTENING desse PID
            ns = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=5)
            listening_ports: List[int] = []
            for line in ns.stdout.splitlines():
                if str(pid) in line and "LISTENING" in line:
                    match = re.search(r"127\.0\.0\.1:(\d+)", line)
                    if match:
                        listening_ports.append(int(match.group(1)))
                        
            # Testa qual porta responde ao LanguageServerService com SSL
            for port in listening_ports:
                try:
                    url = f"https://127.0.0.1:{port}/exa.language_server_pb.LanguageServerService/RetrieveUserQuotaSummary"
                    req = urllib.request.Request(
                        url,
                        data=b"{}",
                        headers={
                            "X-Codeium-Csrf-Token": self.csrf_token,
                            "Content-Type": "application/json"
                        }
                    )
                    with urllib.request.urlopen(req, context=self._ssl_ctx, timeout=1.5) as resp:
                        if resp.status == 200:
                            self.port = port
                            return True
                except Exception:
                    continue
                    
            return False
        except Exception as e:
            print(f"[AntigravityLocalAPI] Falha na descoberta: {e}")
            return False

    def get_quota_summary(self) -> Optional[Dict[str, Any]]:
        """Consulta em tempo real a cota oficial idêntica ao menu View Usage do Antigravity."""
        if not self.port or not self.csrf_token:
            if not self.discover_connection():
                return None
                
        try:
            url = f"https://127.0.0.1:{self.port}/exa.language_server_pb.LanguageServerService/RetrieveUserQuotaSummary"
            req = urllib.request.Request(
                url,
                data=b"{}",
                headers={
                    "X-Codeium-Csrf-Token": self.csrf_token,
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, context=self._ssl_ctx, timeout=2.0) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data.get("response")
        except Exception:
            # Tenta redescobrir caso o processo tenha reiniciado
            if self.discover_connection():
                try:
                    url = f"https://127.0.0.1:{self.port}/exa.language_server_pb.LanguageServerService/RetrieveUserQuotaSummary"
                    req = urllib.request.Request(
                        url,
                        data=b"{}",
                        headers={
                            "X-Codeium-Csrf-Token": self.csrf_token,
                            "Content-Type": "application/json"
                        }
                    )
                    with urllib.request.urlopen(req, context=self._ssl_ctx, timeout=2.0) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                        return data.get("response")
                except Exception:
                    return None
            return None

antigravity_api = AntigravityLocalAPI()
