# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import json
import asyncio
import logging
from pathlib import Path
from typing import List, Set, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from monitor import AntigravityMonitor
from config import config
from auth import auth_manager
from language_manager import language_manager
from tunnel import tunnel_manager

# Filtro para suprimir logs repetitivos de erro 401/403 e handshakes rejeitados
class SuppressAuthSpamFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        if any(term in msg for term in ["403", "401", "connection rejected", "handshake"]):
            return False
        return True

logging.getLogger("uvicorn.access").addFilter(SuppressAuthSpamFilter())
logging.getLogger("uvicorn.error").addFilter(SuppressAuthSpamFilter())

app = FastAPI(title="Antigravity Mobile Bridge", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        t = language_manager.get_dict()
        msg = t.get("terminal_client_connected", "Client connected. Total active: {count}").format(count=len(self.active_connections))
        print(f"[WebSocket] {msg}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        t = language_manager.get_dict()
        msg = t.get("terminal_client_disconnected", "Client disconnected. Total active: {count}").format(count=len(self.active_connections))
        print(f"[WebSocket] {msg}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        dead_connections = set()
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.add(connection)
        for dead in dead_connections:
            self.active_connections.discard(dead)

manager = ConnectionManager()

async def on_monitor_event(event: dict):
    await manager.broadcast(event)

monitor = AntigravityMonitor(on_event=on_monitor_event)

@app.on_event("startup")
async def startup_event():
    active = monitor.find_active_conversation()
    if active:
        await monitor.switch_conversation(active, notify=False)
    monitor.detect_initial_background_tasks()
    monitor.calculate_quota()
    asyncio.create_task(monitor.run_loop())
    t = language_manager.get_dict()
    msg = t.get("terminal_server_started", "Bridge successfully started and monitoring in background.")
    print(f"[Server] {msg}")

@app.on_event("shutdown")
def shutdown_event():
    monitor.stop()
    tunnel_manager.stop_tunnel()

@app.post("/api/auth/new-pin")
@app.get("/api/auth/new-pin")
def request_new_pin():
    """Gera um novo PIN de 4 dígitos aleatório e exibe no terminal do PC."""
    auth_manager.generate_pin()
    return {
        "status": "success",
        "message": "Novo PIN gerado e exibido no console do PC."
    }

@app.post("/api/auth/verify")
async def verify_auth(request: Request):
    """Valida o PIN inserido no aplicativo."""
    try:
        body = await request.json()
        pin = str(body.get("pin", "")).strip()
    except Exception:
        raise HTTPException(status_code=400, detail="Formato inválido")
    
    auth_res = auth_manager.verify(pin)
    if not auth_res:
        raise HTTPException(status_code=401, detail="PIN incorreto. Verifique o terminal do PC.")
    return {
        "success": True,
        "token": auth_res["token"],
        "expires_at": auth_res["expires_at"],
        "expires_in": auth_res["expires_in"],
        "message": "Autenticado com sucesso"
    }

@app.get("/api/auth/check")
def check_auth(token: Optional[str] = None):
    if not auth_manager.is_valid_token(token):
        raise HTTPException(status_code=401, detail="Sessão expirada ou PIN inválido")
    return {
        "authenticated": True,
        "expires_at": auth_manager.get_token_expiry(token)
    }

@app.get("/api/config/i18n")
def get_i18n():
    """Retorna os textos da interface no idioma selecionado no PC."""
    return {
        "language": language_manager.current_lang,
        "dict": language_manager.get_dict(),
        "https_url": tunnel_manager.public_url
    }

@app.get("/antigravity-icon.png")
def get_icon():
    return FileResponse(STATIC_DIR / "antigravity-icon.png", media_type="image/png")

@app.get("/manifest.json")
def get_manifest():
    return FileResponse(STATIC_DIR / "manifest.json", media_type="application/manifest+json")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: Optional[str] = Query(None)):
    if config.REQUIRE_AUTH and not auth_manager.is_valid_token(token):
        auth_manager.notify_unauthorized_access()
        await websocket.close(code=4003)
        return

    await manager.connect(websocket)
    try:
        lang_dict = language_manager.get_dict()
        current_status = monitor.current_turn_status
        if current_status in ["IDLE", "DONE", "CONNECTED", "CONECTADO"]:
            current_status = lang_dict.get("status_connected", "CONECTADO")
        elif current_status in ["RUNNING", "PROCESSANDO"]:
            current_status = lang_dict.get("status_processing", "PROCESSANDO")

        await websocket.send_json({
            "event": "init",
            "data": {
                "conversation_id": monitor.current_conversation_id,
                "active_model": monitor.active_model,
                "active_project": monitor.active_project,
                "conversation_title": monitor.current_conversation_title,
                "https_url": tunnel_manager.public_url,
                "status": current_status,
                "quota": monitor.calculate_quota(),
                "messages": monitor.get_recent_messages(30),
                "i18n": lang_dict
            }
        })
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"[WebSocket] Erro no canal: {e}")
        manager.disconnect(websocket)

@app.get("/api/status")
def get_status(token: Optional[str] = None):
    if config.REQUIRE_AUTH and not auth_manager.is_valid_token(token):
        raise HTTPException(status_code=401, detail="PIN de acesso inválido ou expirado")
    current_status = monitor.current_turn_status
    if current_status in ["IDLE", "DONE", "CONNECTED"]:
        current_status = "CONECTADO"
    elif current_status == "RUNNING":
        current_status = "PROCESSANDO"
    return {
        "conversation_id": monitor.current_conversation_id,
        "status": current_status,
        "active_model": monitor.active_model,
        "active_project": monitor.active_project,
        "conversation_title": monitor.current_conversation_title,
        "https_url": tunnel_manager.public_url,
        "clients_connected": len(manager.active_connections)
    }

@app.get("/api/messages")
def get_messages(limit: int = 30, token: Optional[str] = None):
    if config.REQUIRE_AUTH and not auth_manager.is_valid_token(token):
        raise HTTPException(status_code=401, detail="PIN de acesso inválido ou expirado")
    return {
        "conversation_id": monitor.current_conversation_id,
        "active_model": monitor.active_model,
        "active_project": monitor.active_project,
        "conversation_title": monitor.current_conversation_title,
        "status": monitor.current_turn_status,
        "messages": monitor.get_recent_messages(limit)
    }

@app.get("/api/quota")
def get_quota(token: Optional[str] = None):
    if config.REQUIRE_AUTH and not auth_manager.is_valid_token(token):
        raise HTTPException(status_code=401, detail="PIN de acesso inválido ou expirado")
    return monitor.calculate_quota()

@app.post("/api/test-alert")
async def trigger_test_alert():
    alert_event = {
        "event": "task_completed",
        "data": {
            "step_index": -1,
            "summary": "Tarefa finalizada com sucesso! O teste de som e flash visual foi acionado.",
            "timestamp": "now",
            "quota": monitor.quota_stats,
            "is_test": True
        }
    }
    await manager.broadcast(alert_event)
    return {"message": "Alerta de teste enviado com sucesso!", "clients": len(manager.active_connections)}

@app.get("/api/ping")
def ping():
    return {"status": "ok", "service": "antigravity-mobile-bridge"}

@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")
