# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
from pathlib import Path

class BridgeConfig:
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
