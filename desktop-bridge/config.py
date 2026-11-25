# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import json
from pathlib import Path

VERSION_FILE = Path(__file__).parent / "version.json"

def get_installed_version() -> str:
    """Carrega a versão oficial do Local Server com garantia de persistência."""
    if VERSION_FILE.exists():
        try:
            with open(VERSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                ver = data.get("version", "").strip()
                if ver:
                    return ver
        except Exception:
            pass
    return "2.5.2"

class BridgeConfig:
    VERSION: str = get_installed_version()

    @classmethod
    def refresh_version(cls) -> str:
        """Atualiza a versão carregada em memória a partir de version.json."""
        cls.VERSION = get_installed_version()
        return cls.VERSION
    GITHUB_REPO: str = os.getenv("BRIDGE_GITHUB_REPO", "lumiag5/antigravitymb")
    HOST: str = os.getenv("BRIDGE_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("BRIDGE_PORT", "8765"))
    
    # Caminho do diretório de estado do Antigravity
    ANTIGRAVITY_DIR: Path = Path(os.getenv(
        "ANTIGRAVITY_DIR", 
        Path.home() / ".gemini" / "antigravity"
    ))
    
    BRAIN_DIR: Path = ANTIGRAVITY_DIR / "brain"
    PRESENCE_DIR: Path = ANTIGRAVITY_DIR / "presence"
    CONVERSATIONS_DIR: Path = ANTIGRAVITY_DIR / "conversations"
    ANNOTATIONS_DIR: Path = ANTIGRAVITY_DIR / "annotations"
    
    # Orçamentos de tokens padrão (podem ser calibrados conforme o plano do Gemini/Antigravity)
    DEFAULT_DAILY_TOKEN_LIMIT: int = int(os.getenv("DAILY_TOKEN_LIMIT", "2000000"))
    DEFAULT_WEEKLY_TOKEN_LIMIT: int = int(os.getenv("WEEKLY_TOKEN_LIMIT", "10000000"))
    
    # Chave de segurança / PIN de pareamento para conexões locais e remotas
    AUTH_PIN: str = os.getenv("BRIDGE_PIN", "")
    REQUIRE_AUTH: bool = os.getenv("REQUIRE_AUTH", "true").lower() == "true"
    
    # Intervalo de verificação de atualizações do transcript (em segundos)
    POLL_INTERVAL: float = 0.5

config = BridgeConfig()
