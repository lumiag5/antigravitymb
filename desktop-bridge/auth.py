# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import sys
import json
import time
import random
import secrets
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from language_manager import language_manager

SESSIONS_FILE = Path(__file__).parent / "auth_sessions.json"
SESSION_TTL_SECONDS = 24 * 3600  # 24 horas de validade de cache

class AuthManager:
    """Gerenciador de autenticação com PIN dinâmico e sessões em cache por 24 horas."""

    def __init__(self):
        self.current_pin: str = f"{random.randint(1000, 9999)}"
        # Dicionário de sessões ativas: token -> expires_at_timestamp
        self.active_sessions: Dict[str, float] = {}
        self.last_pin_generated_at = datetime.now(timezone.utc)
        self.last_notice_time: float = 0.0
        self.load_sessions()

    def load_sessions(self):
        """Carrega sessões em cache salvas no disco se ainda estiverem dentro do prazo de 24h."""
        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    now = time.time()
                    # Mantém apenas as sessões cuja expiração é futura
                    self.active_sessions = {
                        token: float(exp) for token, exp in data.items() if float(exp) > now
                    }
            except Exception:
                self.active_sessions = {}

    def save_sessions(self):
        """Persiste as sessões ativas no disco para manter o cache entre reinicializações."""
        try:
            now = time.time()
            clean_sessions = {
                token: exp for token, exp in self.active_sessions.items() if exp > now
            }
            with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(clean_sessions, f, indent=2)
        except Exception as e:
            print(f"[AuthManager] Erro ao persistir sessões: {e}")

    def generate_pin(self, notify: bool = True) -> str:
        """Gera um novo PIN de 4 dígitos aleatório e imprime o banner limpo."""
        self.current_pin = f"{random.randint(1000, 9999)}"
        self.last_pin_generated_at = datetime.now(timezone.utc)
        if notify:
            self.print_pin_banner()
        return self.current_pin

    def print_pin_banner(self):
        """Exibe o PIN de 4 dígitos no terminal do PC de forma limpa e sem repetições."""
        t = language_manager.get_dict()
        print(f"\n[{t['terminal_security_tag']}] {t['terminal_new_pin_banner']}: [ {self.current_pin} ]\n", flush=True)

    def notify_unauthorized_access(self):
        """Silencioso: não repete mensagens no terminal para mantê-lo 100% limpo."""
        pass

    def verify(self, pin: str) -> Optional[Dict[str, Any]]:
        """Valida o PIN digitado. Se correto, emite token com validade de 24 horas."""
        clean_pin = str(pin).strip()
        if clean_pin == self.current_pin:
            token = secrets.token_hex(16)
            now = time.time()
            expires_at = now + SESSION_TTL_SECONDS
            self.active_sessions[token] = expires_at
            self.save_sessions()

            t = language_manager.get_dict()
            msg = t.get('terminal_paired_success', 'Device successfully paired and unlocked via PIN {pin}!').format(pin=self.current_pin)
            print(f"\n[OK] {msg} [Sessão válida por 24 horas]", flush=True)
            return {
                "token": token,
                "expires_at": expires_at,
                "expires_in": SESSION_TTL_SECONDS
            }
        else:
            self.notify_unauthorized_access()
            return None

    def is_valid_token(self, token: Optional[str]) -> bool:
        """Verifica se o token ou PIN fornecido é válido e está dentro da janela de 24 horas."""
        if not token:
            return False
        clean = token.strip()
        now = time.time()

        # Aceita o PIN mestre ativo diretamente
        if clean == self.current_pin:
            return True

        # Valida token de sessão em cache
        if clean in self.active_sessions:
            if now < self.active_sessions[clean]:
                return True
            else:
                # Sessão expirou após 24 horas
                del self.active_sessions[clean]
                self.save_sessions()
                return False

        return False

    def get_token_expiry(self, token: Optional[str]) -> Optional[float]:
        """Retorna o timestamp de expiração da sessão."""
        if not token:
            return None
        clean = token.strip()
        return self.active_sessions.get(clean)

auth_manager = AuthManager()
