# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import re
import ssl
import copy
import json
import glob
import urllib.request
import urllib.error
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from config import config

MODEL_LABEL_TO_ENUM: Dict[str, str] = {
    "gemini 4 hydrogen (high)": "MODEL_PLACEHOLDER_M525",
    "gemini 4 hydrogen (xhigh)": "MODEL_PLACEHOLDER_M528",
    "gemini 4 hydrogen (medium)": "MODEL_PLACEHOLDER_M526",
    "gemini 4 hydrogen (low)": "MODEL_PLACEHOLDER_M527",
    "gemini 4 hydrogen": "MODEL_PLACEHOLDER_M525",
    "gemini 3.8 flash (high)": "MODEL_PLACEHOLDER_M318",
    "gemini 3.8 flash high": "MODEL_PLACEHOLDER_M318",
    "gemini 3.8 flash (medium)": "MODEL_PLACEHOLDER_M319",
    "gemini 3.8 flash (low)": "MODEL_PLACEHOLDER_M320",
    "gemini 3.8 flash": "MODEL_PLACEHOLDER_M318",
    "claude sonnet 4.6 (thinking)": "MODEL_PLACEHOLDER_M35",
    "claude opus 4.6 (thinking)": "MODEL_PLACEHOLDER_M26",
    "gpt-oss 120b (medium)": "MODEL_OPENAI_GPT_OSS_120B_MEDIUM",
    # Aliases de compatibilidade
    "claude 3.7 sonnet": "MODEL_PLACEHOLDER_M35",
    "claude 3.5 sonnet": "MODEL_PLACEHOLDER_M35",
    "gemini 3.8 pro": "MODEL_PLACEHOLDER_M525",
    "gpt-4o": "MODEL_OPENAI_GPT_OSS_120B_MEDIUM",
}

DEFAULT_MODELS_FALLBACK: List[Dict[str, Any]] = [
    {"label": "Gemini 4 Hydrogen (High)", "model_enum": "MODEL_PLACEHOLDER_M525", "model_id": "gemini-4-hydrogen-high"},
    {"label": "Gemini 4 Hydrogen (XHigh)", "model_enum": "MODEL_PLACEHOLDER_M528", "model_id": "gemini-4-hydrogen-xhigh"},
    {"label": "Gemini 4 Hydrogen (Medium)", "model_enum": "MODEL_PLACEHOLDER_M526", "model_id": "gemini-4-hydrogen-medium"},
    {"label": "Gemini 4 Hydrogen (Low)", "model_enum": "MODEL_PLACEHOLDER_M527", "model_id": "gemini-4-hydrogen-low"},
    {"label": "Gemini 3.8 Flash (High)", "model_enum": "MODEL_PLACEHOLDER_M318", "model_id": "gemini-3.8-flash-high"},
    {"label": "Gemini 3.8 Flash (Medium)", "model_enum": "MODEL_PLACEHOLDER_M319", "model_id": "gemini-3.8-flash-medium"},
    {"label": "Gemini 3.8 Flash (Low)", "model_enum": "MODEL_PLACEHOLDER_M320", "model_id": "gemini-3.8-flash-low"},
    {"label": "Claude Sonnet 4.6 (Thinking)", "model_enum": "MODEL_PLACEHOLDER_M35", "model_id": "claude-sonnet-4-6"},
    {"label": "Claude Opus 4.6 (Thinking)", "model_enum": "MODEL_PLACEHOLDER_M26", "model_id": "claude-opus-4-6-thinking"},
    {"label": "GPT-OSS 120B (Medium)", "model_enum": "MODEL_OPENAI_GPT_OSS_120B_MEDIUM", "model_id": "gpt-oss-120b-medium"},
]


class AntigravityLocalAPI:
    """Cliente para comunicar com o Language Server local do Antigravity."""

    def __init__(self):
        self.csrf_token: Optional[str] = None
        self.port: Optional[int] = None
        self.base_url: Optional[str] = None
        self.last_error: Optional[str] = None
        self._ssl_ctx = ssl.create_default_context()
        self._ssl_ctx.check_hostname = False
        self._ssl_ctx.verify_mode = ssl.CERT_NONE
        self._models_cache: List[Dict[str, Any]] = []

    def _get_running_ls_processes(self) -> List[Dict[str, Any]]:
        """Lista processos language_server.exe ativos com PID e CommandLine."""
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
                return []
            data = json.loads(res.stdout)
            if isinstance(data, dict):
                return [data]
            if isinstance(data, list):
                return data
        except Exception:
            pass
        return []

    def _probe_endpoint(self, base_url: str, token: str, timeout: float = 1.5) -> bool:
        """Verifica se uma URL base + CSRF token responde ao LanguageServerService."""
        try:
            url = f"{base_url}/exa.language_server_pb.LanguageServerService/RetrieveUserQuotaSummary"
            req = urllib.request.Request(
                url,
                data=b"{}",
                headers={
                    "X-Codeium-Csrf-Token": token,
                    "Content-Type": "application/json"
                }
            )
            ctx = self._ssl_ctx if base_url.startswith("https://") else None
            with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                return resp.status == 200
        except Exception:
            return False

    def discover_connection(self) -> bool:
        """Descobre porta e CSRF token do language_server.exe (suporta Antigravity 2.34+ via daemon/*.json e versões legadas via CLI)."""
        try:
            procs = self._get_running_ls_processes()
            active_pids = {int(p["ProcessId"]) for p in procs if p.get("ProcessId")}

            # 1. Método moderno (Antigravity 2.34+): arquivos daemon/hub_*.json
            daemon_dir = config.ANTIGRAVITY_DIR / "daemon"
            if daemon_dir.exists():
                json_files = sorted(
                    glob.glob(str(daemon_dir / "*.json")),
                    key=lambda p: Path(p).stat().st_mtime,
                    reverse=True
                )
                candidates: List[Tuple[int, Dict[str, Any]]] = []
                for jf in json_files:
                    try:
                        with open(jf, "r", encoding="utf-8") as f:
                            info = json.load(f)
                        pid = info.get("pid")
                        token = info.get("csrfToken")
                        if not token:
                            continue
                        priority = 0 if (pid and int(pid) in active_pids) else 1
                        candidates.append((priority, info))
                    except Exception:
                        continue

                # Prioriza arquivos cujo PID corresponde ao processo language_server.exe ativo
                candidates.sort(key=lambda item: item[0])
                for _, info in candidates:
                    token = info.get("csrfToken")
                    https_port = info.get("httpsPort")
                    http_port = info.get("httpPort")
                    for scheme, p in [("https", https_port), ("http", http_port)]:
                        if not p:
                            continue
                        base = f"{scheme}://127.0.0.1:{int(p)}"
                        if self._probe_endpoint(base, token):
                            self.port = int(p)
                            self.csrf_token = token
                            self.base_url = base
                            return True

            # 2. Fallback legado: --csrf_token na linha de comando + netstat
            for p_info in procs:
                pid = p_info.get("ProcessId")
                cmdline = p_info.get("CommandLine", "")
                csrf_match = re.search(r"--csrf_token\s+([a-f0-9-]+)", cmdline)
                if not csrf_match or not pid:
                    continue
                token = csrf_match.group(1)
                ns = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=5)
                for line in ns.stdout.splitlines():
                    if str(pid) in line and "LISTENING" in line:
                        match = re.search(r"127\.0\.0\.1:(\d+)", line)
                        if match:
                            port = int(match.group(1))
                            base = f"https://127.0.0.1:{port}"
                            if self._probe_endpoint(base, token):
                                self.port = port
                                self.csrf_token = token
                                self.base_url = base
                                return True

            return False
        except Exception as e:
            print(f"[AntigravityLocalAPI] Falha na descoberta: {e}")
            return False

    def _call_rpc(self, method: str, payload: Dict[str, Any], timeout: float = 3.0) -> Optional[Dict[str, Any]]:
        """Executa uma chamada JSON ao LanguageServerService com redescoberta automática em caso de falha."""
        if not self.base_url or not self.csrf_token:
            if not self.discover_connection():
                self.last_error = "Language Server do Antigravity não encontrado"
                return None

        data_bytes = json.dumps(payload).encode("utf-8")
        for attempt in range(2):
            try:
                url = f"{self.base_url}/exa.language_server_pb.LanguageServerService/{method}"
                req = urllib.request.Request(
                    url,
                    data=data_bytes,
                    headers={
                        "X-Codeium-Csrf-Token": self.csrf_token,
                        "Content-Type": "application/json"
                    }
                )
                ctx = self._ssl_ctx if self.base_url.startswith("https://") else None
                with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
                    self.last_error = None
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw.strip() else {}
            except urllib.error.HTTPError as e:
                err_body = ""
                try:
                    err_body = e.read().decode("utf-8", errors="ignore")
                except Exception:
                    pass
                self.last_error = f"HTTP {e.code}: {err_body or e.reason}"
                if e.code in (401, 403) and attempt == 0 and self.discover_connection():
                    continue
                return None
            except Exception as e:
                self.last_error = str(e)
                if attempt == 0 and self.discover_connection():
                    continue
                return None
        return None

    def get_quota_summary(self) -> Optional[Dict[str, Any]]:
        """Consulta em tempo real a cota oficial idêntica ao menu View Usage do Antigravity."""
        data = self._call_rpc("RetrieveUserQuotaSummary", {}, timeout=2.5)
        if data is not None:
            return data.get("response")
        return None

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Obtém a lista oficial de modelos ativos direto do Antigravity PC (GetUserStatus)."""
        data = self._call_rpc("GetUserStatus", {}, timeout=2.5)
        if data:
            configs = (
                data.get("userStatus", {})
                .get("cascadeModelConfigData", {})
                .get("clientModelConfigs", [])
            )
            models = []
            for cfg in configs:
                if cfg.get("disabled", False):
                    continue
                label = cfg.get("label", "").strip()
                model_enum = cfg.get("modelOrAlias", {}).get("model", "").strip()
                model_id = cfg.get("modelId", "").strip()
                if label and model_enum:
                    models.append({
                        "label": label,
                        "model_enum": model_enum,
                        "model_id": model_id
                    })
            if models:
                self._models_cache = models
                return models
        return self._models_cache or list(DEFAULT_MODELS_FALLBACK)

    def resolve_model_enum(self, model_name: Optional[str]) -> Optional[str]:
        """Converte nome amigável ou ID de modelo para o enum oficial (ex: MODEL_PLACEHOLDER_M525)."""
        if not model_name:
            return None
        clean = model_name.strip()
        if clean.startswith("MODEL_"):
            return clean

        lower = clean.lower()
        # 1. Procura na lista dinâmica obtida do GetUserStatus
        models = self._models_cache or self.get_available_models()
        for m in models:
            if (
                m["label"].lower() == lower
                or m.get("model_id", "").lower() == lower
                or m.get("model_enum", "").lower() == lower
            ):
                return m["model_enum"]

        # 2. Fallback no mapeamento estático
        if lower in MODEL_LABEL_TO_ENUM:
            return MODEL_LABEL_TO_ENUM[lower]

        for key, enum_val in MODEL_LABEL_TO_ENUM.items():
            if key in lower or lower in key:
                return enum_val

        return None

    def get_all_cascade_summaries(self) -> Dict[str, Dict[str, Any]]:
        """Retorna os resumos em memória das conversas carregadas no language_server."""
        data = self._call_rpc("GetAllCascadeTrajectories", {}, timeout=2.0)
        if data and isinstance(data.get("trajectorySummaries"), dict):
            return data["trajectorySummaries"]
        return {}

    def get_trajectory_info(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Carrega a trajetória da conversa no language_server e retorna o último userConfig e modelDisplayName."""
        data = self._call_rpc("GetCascadeTrajectory", {"cascade_id": conversation_id}, timeout=4.0)
        if not data or "trajectory" not in data:
            return None

        traj = data["trajectory"]
        steps = traj.get("steps", [])
        last_user_config = None
        for step in reversed(steps):
            if step.get("type") == "CORTEX_STEP_TYPE_USER_INPUT":
                ui = step.get("userInput", {})
                if isinstance(ui.get("userConfig"), dict):
                    last_user_config = ui["userConfig"]
                    break

        gen_metas = traj.get("generatorMetadata", [])
        model_display = None
        model_raw = None
        for gm in reversed(gen_metas):
            cm = gm.get("chatModel") or {}
            if cm.get("modelDisplayName"):
                model_display = cm["modelDisplayName"]
                model_raw = cm.get("responseModel") or cm.get("model")
                break
            if cm.get("responseModel") or cm.get("model"):
                model_raw = cm.get("responseModel") or cm.get("model")
                break

        return {
            "user_config": last_user_config,
            "model_display_name": model_display,
            "model_raw": model_raw
        }

    def send_user_message(self, conversation_id: str, message_text: str, model: Optional[str] = None) -> bool:
        """Envia um prompt/comando para a conversa especificada no Antigravity PC."""
        if not self.base_url or not self.csrf_token:
            if not self.discover_connection():
                self.last_error = "Não foi possível localizar o processo do Antigravity PC"
                return False

        # Garante que a trajetória esteja carregada em memória e obtém seu userConfig atual
        traj_info = self.get_trajectory_info(conversation_id)
        model_enum = self.resolve_model_enum(model)

        payload: Dict[str, Any] = {
            "cascade_id": conversation_id,
            "items": [{"text": message_text}]
        }

        if model_enum:
            if traj_info and isinstance(traj_info.get("user_config"), dict):
                cfg = copy.deepcopy(traj_info["user_config"])
                planner = cfg.setdefault("plannerConfig", {})
                planner["planModel"] = model_enum
                payload["cascade_config"] = cfg
            else:
                payload["cascade_config"] = {
                    "planner_config": {
                        "plan_model": model_enum
                    }
                }

        res = self._call_rpc("SendUserCascadeMessage", payload, timeout=8.0)
        if res is not None:
            return True

        print(f"[AntigravityLocalAPI] Falha ao enviar mensagem: {self.last_error}")
        return False


antigravity_api = AntigravityLocalAPI()
