# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Licensed under the MIT License.

import os
import json
import time
import glob
import asyncio
import re
import sqlite3
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Tuple
from config import config
from antigravity_api import antigravity_api
from language_manager import language_manager

class AntigravityMonitor:
    def __init__(self, on_event: Optional[Callable[[Dict[str, Any]], Any]] = None):
        self.on_event = on_event
        self.current_conversation_id: Optional[str] = None
        self.current_transcript_path: Optional[Path] = None
        self.file_offset: int = 0
        self.last_step_index: int = -1
        self.is_running: bool = False
        
        # Controle de navegação do usuário e tarefas em segundo plano
        self.suppressed_view_until_key: Optional[Tuple[float, float, Any]] = None
        self.background_working_conversations: Dict[str, Dict[str, Any]] = {}
        
        # Estado do turno atual
        self.current_turn_status: str = "IDLE"  # IDLE, RUNNING, DONE
        self.last_notified_step: int = -1
        self.active_model: str = "Gemini 3.8 Flash High"
        self.active_project: str = "Antigravity"
        self.current_conversation_title: str = ""
        
        # Cache de cota
        self.quota_stats: Dict[str, Any] = {
            "is_official": True,
            "groups": [],
            "active_group": "Gemini Models",
            "daily_pct": 100.0,
            "weekly_pct": 100.0,
            "five_hour_pct": 100.0,
            "five_hour_desc": "100% Disponível",
            "weekly_desc": "100% Disponível",
            "active_model": self.active_model,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def find_user_viewed_conversation(self) -> Tuple[Optional[str], Tuple[float, float, str]]:
        """Localiza a conversa que o usuário está VISUALIZANDO na interface do Antigravity PC
        agregando TODAS as fontes possíveis (anotações .pbtxt, presença .lock, summaries e logs).
        Retorna (cid, (view_score, file_mtime, cid)).
        """
        all_cids = set()
        summaries: Dict[str, float] = {}

        # 1. Coleta todas as conversas registradas em conversation_summaries.db
        summaries_db = config.ANTIGRAVITY_DIR / "conversation_summaries.db"
        if summaries_db.exists():
            try:
                conn = sqlite3.connect(f"file:{summaries_db}?mode=ro", uri=True, timeout=0.8)
                cursor = conn.cursor()
                rows = cursor.execute(
                    "SELECT conversation_id, last_modified_time FROM conversation_summaries"
                ).fetchall()
                conn.close()
                for r in rows:
                    cid, lmt = r
                    if cid:
                        all_cids.add(cid)
                        if lmt:
                            try:
                                dt = datetime.fromisoformat(lmt.replace("Z", "+00:00"))
                                summaries[cid] = dt.timestamp()
                            except Exception:
                                pass
            except Exception:
                pass

        # 2. Agrega CIDs de arquivos em annotations/*.pbtxt
        try:
            for f in glob.glob(str(config.ANNOTATIONS_DIR / "*.pbtxt")):
                all_cids.add(Path(f).stem)
        except Exception:
            pass

        # 3. Agrega CIDs de arquivos em presence/*.lock
        try:
            for f in glob.glob(str(config.PRESENCE_DIR / "*.lock")):
                all_cids.add(Path(f).stem)
        except Exception:
            pass

        # 4. Agrega CIDs de diretórios brain/*/transcript.jsonl
        try:
            pattern = str(config.BRAIN_DIR / "*" / ".system_generated" / "logs" / "transcript.jsonl")
            for f in glob.glob(pattern):
                cid = Path(f).parents[2].name
                if cid != "tempmediaStorage":
                    all_cids.add(cid)
        except Exception:
            pass

        best_cid = None
        best_key = (-1.0, -1.0, "")

        for cid in all_cids:
            if cid == "tempmediaStorage":
                continue

            view_ts = 0.0
            file_mtime = 0.0

            # A. Verifica anotação .pbtxt (timestamp oficial de visualização da UI)
            pf = config.ANNOTATIONS_DIR / f"{cid}.pbtxt"
            if pf.exists():
                try:
                    mtime = os.path.getmtime(pf)
                    file_mtime = max(file_mtime, mtime)
                    with open(pf, "r", encoding="utf-8", errors="ignore") as af:
                        txt = af.read()
                    match = re.search(r"last_user_view_time:\s*\{\s*seconds:\s*(\d+)(?:\s*nanos:\s*(\d+))?", txt)
                    if match:
                        sec = int(match.group(1))
                        nanos = int(match.group(2)) if match.group(2) else 0
                        view_ts = max(view_ts, float(sec) + float(nanos) / 1e9)
                except Exception:
                    pass

            # B. Verifica presença .lock (atualizado quando o Antigravity foca uma conversa)
            lf = config.PRESENCE_DIR / f"{cid}.lock"
            if lf.exists():
                try:
                    file_mtime = max(file_mtime, os.path.getmtime(lf))
                except Exception:
                    pass

            # Pontuação principal: instante em que a conversa foi visualizada ou focada
            score = max(view_ts, file_mtime)

            # Fallback para conversas que não possuem .pbtxt nem .lock
            if score == 0.0 and cid in summaries:
                score = summaries[cid] * 0.5

            key = (score, file_mtime, cid)
            if key > best_key:
                best_key = key
                best_cid = cid

        return best_cid, best_key

    def find_fallback_conversation(self) -> Optional[str]:
        """Fallback para inicialização caso o Antigravity não tenha gerado anotações com timestamp de visualização."""
        candidates: Dict[str, float] = {}

        # 1. Checa conversation_summaries.db
        summaries_db = config.ANTIGRAVITY_DIR / "conversation_summaries.db"
        if summaries_db.exists():
            try:
                conn = sqlite3.connect(f"file:{summaries_db}?mode=ro", uri=True, timeout=0.5)
                cursor = conn.cursor()
                rows = cursor.execute(
                    "SELECT conversation_id, last_modified_time FROM conversation_summaries ORDER BY last_modified_time DESC LIMIT 10"
                ).fetchall()
                conn.close()
                for row in rows:
                    cid, mtime_str = row[0], row[1]
                    if cid and mtime_str:
                        try:
                            dt = datetime.fromisoformat(mtime_str.replace("Z", "+00:00"))
                            candidates[cid] = max(candidates.get(cid, 0.0), dt.timestamp())
                        except Exception:
                            pass
            except Exception:
                pass

        # 2. Checa arquivos conversations/*.db
        try:
            conv_files = glob.glob(str(config.CONVERSATIONS_DIR / "*.db*"))
            for cf in conv_files:
                cid = Path(cf).stem.replace(".db", "").replace("-wal", "").replace("-shm", "")
                try:
                    st = os.stat(cf)
                    candidates[cid] = max(candidates.get(cid, 0.0), st.st_mtime)
                except Exception:
                    pass
        except Exception:
            pass

        # 3. Checa presence/*.lock
        try:
            lock_files = glob.glob(str(config.PRESENCE_DIR / "*.lock"))
            for lf in lock_files:
                cid = Path(lf).stem
                candidates[cid] = max(candidates.get(cid, 0.0), os.path.getmtime(lf))
        except Exception:
            pass

        # 4. Checa transcripts em brain/*/transcript.jsonl
        try:
            pattern = str(config.BRAIN_DIR / "*" / ".system_generated" / "logs" / "transcript.jsonl")
            files = glob.glob(pattern)
            for f in files:
                cid = Path(f).parents[2].name
                candidates[cid] = max(candidates.get(cid, 0.0), os.path.getmtime(f))
        except Exception:
            pass

        if not candidates:
            return None

        sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        for cid, _ in sorted_candidates:
            transcript = config.BRAIN_DIR / cid / ".system_generated" / "logs" / "transcript.jsonl"
            conv_db = config.CONVERSATIONS_DIR / f"{cid}.db"
            if transcript.exists() or conv_db.exists():
                return cid

        return sorted_candidates[0][0]

    def find_active_conversation(self) -> Optional[str]:
        """Localiza a conversa ativa para inicialização priorizando a visualização do usuário."""
        cid, _ = self.find_user_viewed_conversation()
        if cid:
            return cid
        return self.find_fallback_conversation()

    def _is_conversation_working(self, cid: str) -> bool:
        """Verifica se uma conversa possui uma tarefa em andamento ("Working...")."""
        if not cid:
            return False
        tpath = config.BRAIN_DIR / cid / ".system_generated" / "logs" / "transcript.jsonl"
        if not tpath.exists():
            return False
        try:
            # Se o arquivo não foi modificado nos últimos 30 minutos, consideramos inativo
            if time.time() - os.path.getmtime(tpath) > 1800:
                return False

            size = os.path.getsize(tpath)
            if size == 0:
                return False

            read_len = min(size, 16384)
            with open(tpath, "r", encoding="utf-8", errors="ignore") as f:
                if size > read_len:
                    f.seek(size - read_len)
                lines = [l.strip() for l in f if l.strip()]
                if not lines:
                    return False
                
                last_step = json.loads(lines[-1])
                st = last_step.get("status", "")
                tc = last_step.get("tool_calls", [])
                src = last_step.get("source", "")
                stype = last_step.get("type", "")

                if st == "RUNNING" or tc or src == "USER_EXPLICIT" or stype == "USER_INPUT":
                    return True

                if src == "MODEL" and stype == "PLANNER_RESPONSE" and not tc and bool(last_step.get("content")):
                    return False

                # Se o último step for SYSTEM_MESSAGE ou GENERIC, verifica passos anteriores recentes
                for prev in reversed(lines[-8:]):
                    p = json.loads(prev)
                    p_tc = p.get("tool_calls", [])
                    p_src = p.get("source", "")
                    p_stype = p.get("type", "")
                    p_st = p.get("status", "")
                    if p_src == "MODEL" and p_stype == "PLANNER_RESPONSE" and not p_tc and bool(p.get("content")):
                        return False
                    if p_st == "RUNNING" or p_tc or p_src == "USER_EXPLICIT":
                        return True
        except Exception:
            pass
        return False

    def detect_initial_background_tasks(self):
        """No arranque, detecta se existem conversas recentes ainda em andamento ("Working...")."""
        try:
            pattern = str(config.BRAIN_DIR / "*" / ".system_generated" / "logs" / "transcript.jsonl")
            files = glob.glob(pattern)
            for f in files:
                cid = Path(f).parents[2].name
                if cid == self.current_conversation_id:
                    continue
                if self._is_conversation_working(cid):
                    size = os.path.getsize(f)
                    self.background_working_conversations[cid] = {
                        "offset": max(0, size - 4096),
                        "transcript_path": Path(f)
                    }
                    print(f"[Monitor] Tarefa em andamento pré-existente detectada na conversa {cid}. Monitorando em segundo plano!")
        except Exception:
            pass

    async def switch_conversation(self, conv_id: str, notify: bool = True, status: Optional[str] = None):
        """Altera a conversa monitorada, redefine ponteiros e notifica os clientes em tempo real."""
        if not conv_id:
            return

        self.current_conversation_id = conv_id
        self.current_transcript_path = (
            config.BRAIN_DIR / conv_id / ".system_generated" / "logs" / "transcript.jsonl"
        )
        self.detect_model_name(conv_id)
        self.active_project, self.current_conversation_title = self.detect_project_and_title(conv_id)

        # Inicia o offset no final do arquivo atual com leitura rápida do tail (evita travar em arquivos de 40MB)
        if self.current_transcript_path.exists():
            try:
                size = os.path.getsize(self.current_transcript_path)
                self.file_offset = size
                if size > 0:
                    read_len = min(size, 8192)
                    with open(self.current_transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                        if size > read_len:
                            f.seek(size - read_len)
                        lines = [l.strip() for l in f if l.strip()]
                        if lines:
                            last_step = json.loads(lines[-1])
                            self.last_step_index = last_step.get("step_index", -1)
                            self.last_notified_step = self.last_step_index
                            if status:
                                self.current_turn_status = status
                            else:
                                st = last_step.get("status", "")
                                tc = last_step.get("tool_calls", [])
                                src = last_step.get("source", "")
                                stype = last_step.get("type", "")
                                if st == "RUNNING" or tc or src == "USER_EXPLICIT" or stype == "USER_INPUT":
                                    self.current_turn_status = "PROCESSANDO"
                                else:
                                    self.current_turn_status = "CONECTADO"
            except Exception:
                self.last_step_index = -1
                self.current_turn_status = status or "CONECTADO"
        else:
            self.file_offset = 0
            self.last_step_index = -1
            self.current_turn_status = status or "CONECTADO"

        t = language_manager.get_dict()
        msg = t.get("terminal_monitoring_conv", "Monitorando conversa: {conv_id} ({model}) - Offset inicial: {offset}").format(
            conv_id=conv_id,
            model=self.active_model,
            offset=self.file_offset
        )
        print(f"[Monitor] {msg}")

        # Notifica clientes conectados via WebSocket com histórico limpo da nova conversa
        if notify and self.on_event:
            recent_msgs = self.get_recent_messages(30)
            await self.on_event({
                "event": "conversation_switched",
                "data": {
                    "conversation_id": conv_id,
                    "active_model": self.active_model,
                    "active_project": self.active_project,
                    "conversation_title": self.current_conversation_title,
                    "status": self.current_turn_status,
                    "quota": self.quota_stats,
                    "messages": recent_msgs
                }
            })

    def detect_project_and_title(self, conv_id: Optional[str] = None) -> Tuple[str, str]:
        """Detecta o nome limpo do workspace/projeto e o título descritivo da conversa atual."""
        cid = conv_id or self.current_conversation_id
        if not cid:
            return "Antigravity", ""

        proj_name = "Antigravity"
        title_name = ""

        # 1. Tenta obter das anotações .pbtxt
        pf = config.ANNOTATIONS_DIR / f"{cid}.pbtxt"
        if pf.exists():
            try:
                with open(pf, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
                m = re.search(r'title:\s*\"([^\"\r\n]+)\"', txt)
                if m:
                    title_name = m.group(1).strip()
            except Exception:
                pass

        # 2. Tenta obter do banco conversation_summaries.db
        summaries_db = config.ANTIGRAVITY_DIR / "conversation_summaries.db"
        if summaries_db.exists():
            try:
                conn = sqlite3.connect(f"file:{summaries_db}?mode=ro", uri=True, timeout=0.8)
                cursor = conn.cursor()
                row = cursor.execute(
                    "SELECT workspace_uris, title FROM conversation_summaries WHERE conversation_id = ?",
                    (cid,)
                ).fetchone()
                conn.close()
                if row:
                    ws_uris_raw, db_title = row[0], row[1]
                    if not title_name and db_title and db_title.strip():
                        title_name = db_title.strip()
                    if ws_uris_raw:
                        try:
                            uris = json.loads(ws_uris_raw)
                            if isinstance(uris, list) and len(uris) > 0 and uris[0]:
                                raw_path = urllib.parse.unquote(uris[0])
                                clean = raw_path.replace("file:///", "").rstrip("/\\")
                                folder = clean.split("/")[-1].split("\\")[-1]
                                if folder.strip():
                                    proj_name = folder.strip()
                        except Exception:
                            pass
            except Exception:
                pass

        return proj_name, title_name

    def detect_project_name(self, conv_id: Optional[str] = None) -> str:
        """Compatibilidade reversa: retorna o nome do projeto."""
        proj, _ = self.detect_project_and_title(conv_id)
        return proj

    def detect_model_name(self, conv_id: Optional[str] = None) -> str:
        """Detecta o nome oficial e formatado do modelo ativo a partir do banco da conversa ou logs."""
        cid = conv_id or self.current_conversation_id
        if not cid:
            return self.active_model

        db_path = config.CONVERSATIONS_DIR / f"{cid}.db"
        model_found = None

        if db_path.exists():
            try:
                # Conecta em modo somente leitura com URI para nunca travar com locks ativos do Antigravity
                con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=0.8)
                cur = con.cursor()
                rows = cur.execute("SELECT data FROM gen_metadata ORDER BY idx DESC LIMIT 3").fetchall()
                for row in rows:
                    if row and row[0]:
                        raw_data = row[0]

                        # 1. Procura pela tag de modelo protobuf (campo 28 \xe2\x01\xlen <model> - comum no Claude)
                        m_claude = re.search(rb'\xe2\x01[\x01-\x40]((?:claude|gemini|gpt)[a-zA-Z0-9_.-]+)', raw_data)
                        if m_claude and len(m_claude.group(1)) >= 4:
                            cand = m_claude.group(1).decode("utf-8", errors="ignore")
                            if any(k in cand.lower() for k in ["claude", "gemini", "gpt", "sonnet", "opus", "flash", "pro"]):
                                model_found = cand
                                break

                        # 2. Procura pela tag de modelo protobuf (campo 19 \x9a\x01\xlen <model>)
                        m = re.search(rb'\x9a\x01[\x01-\x40]((?:claude|gemini|gpt)[a-zA-Z0-9_.-]+)', raw_data)
                        if m and len(m.group(1)) >= 4:
                            cand = m.group(1).decode("utf-8", errors="ignore")
                            if any(k in cand.lower() for k in ["claude", "gemini", "gpt", "sonnet", "opus", "flash", "pro"]):
                                model_found = cand
                                break

                        # 3. Busca por strings literais de modelos (prioriza Claude/GPT para evitar falso positivo do prompt de sistema)
                        for candidate in [
                            "claude-sonnet-4-6", "claude-opus-4-6",
                            "claude-3-7-sonnet", "claude-3.7-sonnet",
                            "claude-3-5-sonnet", "claude-3.5-sonnet",
                            "claude-3-5-haiku", "claude-3.5-haiku",
                            "claude-sonnet", "claude-opus", "claude-haiku",
                            "gpt-oss-120b", "gpt-4o", "gpt-4",
                            "gemini-3.8-pro", "gemini-4-argon",
                            "gemini-3.8-flash-control", "gemini-3.8-flash-n",
                            "gemini-3.8-flash-high", "gemini-3.8-flash"
                        ]:
                            if candidate.encode("utf-8") in raw_data:
                                model_found = candidate
                                break

                    if model_found:
                        break
                con.close()
            except Exception:
                pass

        if model_found:
            formatted = self.format_model_display_name(model_found)
            if formatted != self.active_model:
                self.active_model = formatted
                self.quota_stats["active_model"] = formatted

        return self.active_model

    @staticmethod
    def format_model_display_name(raw: str) -> str:
        """Mapeia identificadores internos para os nomes visuais oficiais do Antigravity."""
        r = raw.lower().strip()
        if "gemini-3.8-flash" in r or "gemini-3-8-flash" in r or "flash-n" in r or "flash-high" in r:
            return "Gemini 3.8 Flash High"
        if "gemini-3.8-pro" in r or "gemini-3-8-pro" in r:
            return "Gemini 3.8 Pro"
        if "gemini-4" in r or "argon" in r:
            return "Gemini 4 Argon"
        if "claude-sonnet-4" in r or "sonnet-4" in r:
            return "Claude Sonnet 4.6 (Thinking)"
        if "claude-opus" in r or "opus-4" in r:
            return "Claude Opus 4.6 (Thinking)"
        if "claude-3-7" in r or "claude-3.7" in r:
            return "Claude 3.7 Sonnet"
        if "claude-3-5" in r or "claude-3.5" in r:
            return "Claude 3.5 Sonnet"
        if "gpt-oss" in r:
            return "GPT-OSS 120B (Medium)"
        if "gpt-4o" in r:
            return "GPT-4o"
        if "gpt-4" in r:
            return "GPT-4"
        if "claude" in r:
            return "Claude Sonnet"
        if "gemini" in r:
            return "Gemini 3.8 Flash High"
        return raw

    def calculate_quota(self) -> Dict[str, Any]:
        """Consulta a cota oficial em tempo real do Antigravity e associa ao modelo em uso."""
        official_summary = antigravity_api.get_quota_summary()
        t = language_manager.get_dict()
        
        # Identifica se o modelo ativo é Claude/GPT ou Gemini
        is_claude_or_gpt = any(m in self.active_model.lower() for m in ["claude", "gpt"])
        target_group_keyword = "claude" if is_claude_or_gpt else "gemini"

        if official_summary and "groups" in official_summary:
            groups_data = []
            active_weekly_pct = 100.0
            active_5h_pct = 100.0
            active_5h_desc = ""
            active_weekly_desc = ""
            active_group_name = ""

            all_groups = official_summary.get("groups", [])
            for grp in all_groups:
                name = grp.get("displayName", "")
                is_active_group = target_group_keyword in name.lower()
                
                parsed_group = {
                    "name": name,
                    "description": grp.get("description", ""),
                    "limits": []
                }
                for b in grp.get("buckets", []):
                    rem_frac = b.get("remainingFraction", 1.0)
                    rem_pct = round(rem_frac * 100, 1)
                    window = b.get("window", "")
                    reset_time = b.get("resetTime", "")
                    raw_desc = b.get("description", "")
                    desc = language_manager.format_quota_desc(raw_desc, reset_time, rem_pct)
                    
                    parsed_group["limits"].append({
                        "name": t.get("quota_weekly_title", "Limite Semanal") if window == "weekly" else t.get("quota_5h_title", "Limite 5 Horas"),
                        "window": window,
                        "remaining_pct": rem_pct,
                        "reset_time": reset_time,
                        "description": desc
                    })

                    # Associa as métricas principais ao grupo do modelo ativo
                    if is_active_group or not active_group_name:
                        if window == "weekly":
                            active_weekly_pct = rem_pct
                            active_weekly_desc = desc
                        elif window == "5h":
                            active_5h_pct = rem_pct
                            active_5h_desc = desc

                if is_active_group:
                    active_group_name = name

                groups_data.append(parsed_group)

            avail_text = t.get("quota_available", "100% Disponível")
            self.quota_stats = {
                "is_official": True,
                "groups": groups_data,
                "active_group": active_group_name or ("Claude and GPT models" if is_claude_or_gpt else "Gemini Models"),
                "daily_pct": active_5h_pct,
                "weekly_pct": active_weekly_pct,
                "five_hour_pct": active_5h_pct,
                "five_hour_desc": active_5h_desc or avail_text,
                "weekly_desc": active_weekly_desc or avail_text,
                "active_model": self.active_model,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            return self.quota_stats

        # Fallback caso a API local não responda no momento
        self.quota_stats["timestamp"] = datetime.now(timezone.utc).isoformat()
        return self.quota_stats

    def get_recent_messages(self, limit: int = 30) -> List[Dict[str, Any]]:
        """Retorna as mensagens formatadas mais recentes da conversa ativa com leitura ultra-rápida do tail (fim do arquivo)."""
        if not self.current_transcript_path or not self.current_transcript_path.exists():
            return []

        messages: List[Dict[str, Any]] = []
        try:
            size = os.path.getsize(self.current_transcript_path)
            if size == 0:
                return []

            # Para arquivos grandes (>256KB), faz seek no tail para não travar CPU com 25.000 linhas
            read_bytes = min(size, 262144)  # 256 KB
            with open(self.current_transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                if size > read_bytes:
                    f.seek(size - read_bytes)
                lines = f.readlines()

            # Descarta a primeira linha caso o seek tenha caído no meio de uma linha
            if size > read_bytes and len(lines) > 1:
                lines = lines[1:]

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    step = json.loads(line)
                    parsed = self._format_step_message(step)
                    if parsed:
                        messages.append(parsed)
                except Exception:
                    continue

            # Se pegou poucas mensagens e o arquivo é maior, tenta uma janela maior de 1MB
            if len(messages) < limit and size > read_bytes:
                read_bytes_large = min(size, 1048576)
                with open(self.current_transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                    f.seek(size - read_bytes_large)
                    lines = f.readlines()
                if len(lines) > 1:
                    lines = lines[1:]
                messages = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        step = json.loads(line)
                        parsed = self._format_step_message(step)
                        if parsed:
                            messages.append(parsed)
                    except Exception:
                        continue
        except Exception as e:
            print(f"[Monitor] Erro ao ler histórico: {e}")

        return messages[-limit:]

    def _format_step_message(self, step: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Converte um step do transcript em mensagem amigável para o app mobile.
        FILTRAGEM ESTRITA: Exibe SOMENTE a mensagem do usuário e a CONCLUSÃO FINAL da tarefa.
        Não exibe saídas de terminal, chamadas de ferramentas ou etapas intermediárias.
        """
        step_index = step.get("step_index", 0)
        source = step.get("source", "")
        step_type = step.get("type", "")
        status = step.get("status", "DONE")
        content = step.get("content", "")
        tool_calls = step.get("tool_calls", [])
        created_at = step.get("created_at", datetime.now(timezone.utc).isoformat())

        # 1. Mensagem enviada pelo usuário
        if source == "USER_EXPLICIT" or step_type == "USER_INPUT":
            if content and "<USER_REQUEST>" in content:
                match = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                if match:
                    content = match.group(1).strip()
            # Ignora prompts internos ou mensagens vazias
            if not content.strip():
                return None
            return {
                "id": f"{self.current_conversation_id}_{step_index}",
                "step_index": step_index,
                "role": "user",
                "status": "DONE",
                "content": content,
                "timestamp": created_at
            }

        # 2. Resposta FINAL de conclusão do agente (quando terminou todas as ferramentas e concluiu a edição)
        is_final_conclusion = (
            source == "MODEL" 
            and step_type == "PLANNER_RESPONSE" 
            and not tool_calls 
            and bool(content)
        )

        if is_final_conclusion:
            return {
                "id": f"{self.current_conversation_id}_{step_index}",
                "step_index": step_index,
                "role": "assistant",
                "status": status,
                "content": content,
                "timestamp": created_at
            }

        # Qualquer outra etapa (saída de terminal, tool_call, tool_result, log interno) é filtrada e ignorada
        return None

    async def check_user_navigation(self):
        """Verifica se o usuário navegou explicitamente para outra conversa/projeto no PC."""
        viewed_cid, viewed_key = self.find_user_viewed_conversation()
        if not viewed_cid or viewed_cid == self.current_conversation_id:
            return

        # Se uma conclusão de segundo plano acabou de comutar a tela,
        # só permitimos nova troca quando o usuário fizer um NOVO clique/visualização no PC
        if self.suppressed_view_until_key and viewed_key <= self.suppressed_view_until_key:
            return

        self.suppressed_view_until_key = None
        print(f"[Monitor] Usuário navegou para nova conversa no PC: {self.current_conversation_id} -> {viewed_cid}")
        
        # Se a conversa anterior estava em andamento ("Working..."), move para monitoramento em segundo plano!
        prev_cid = self.current_conversation_id
        if prev_cid and (self.current_turn_status == "PROCESSANDO" or self._is_conversation_working(prev_cid)):
            self.background_working_conversations[prev_cid] = {
                "offset": self.file_offset,
                "transcript_path": self.current_transcript_path
            }
            print(f"[Monitor] Conversa {prev_cid} está trabalhando. Monitoramento em segundo plano ativado!")

        # Se a nova conversa estava no background, remove do background pois agora está em primeiro plano
        self.background_working_conversations.pop(viewed_cid, None)

        # Comuta a visualização do app para a conversa selecionada pelo usuário
        await self.switch_conversation(viewed_cid)

    async def poll_background_conversations(self):
        """Monitora conversas em execução em segundo plano para detectar conclusão ("Working..." finalizado)."""
        if not self.background_working_conversations:
            return

        for bg_cid in list(self.background_working_conversations.keys()):
            if bg_cid == self.current_conversation_id:
                self.background_working_conversations.pop(bg_cid, None)
                continue

            bg_info = self.background_working_conversations.get(bg_cid)
            if not bg_info:
                continue

            tpath = bg_info.get("transcript_path") or (config.BRAIN_DIR / bg_cid / ".system_generated" / "logs" / "transcript.jsonl")
            if not tpath.exists():
                continue

            try:
                size = os.path.getsize(tpath)
                offset = bg_info.get("offset", 0)
                if size < offset:
                    offset = 0

                if size == offset:
                    continue

                with open(tpath, "r", encoding="utf-8", errors="ignore") as f:
                    f.seek(offset)
                    new_lines = f.readlines()
                    bg_info["offset"] = f.tell()

                for line in new_lines:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        step = json.loads(line)
                        status = step.get("status", "")
                        source = step.get("source", "")
                        step_type = step.get("type", "")
                        tool_calls = step.get("tool_calls", [])
                        content = step.get("content", "")
                        step_index = step.get("step_index", 0)

                        is_final_response = (
                            status == "DONE"
                            and source == "MODEL"
                            and step_type == "PLANNER_RESPONSE"
                            and not tool_calls
                            and bool(content)
                        )

                        if is_final_response:
                            print(f"[Monitor] *** TAREFA EM SEGUNDO PLANO CONCLUÍDA ({bg_cid} - Step {step_index}) ***")
                            self.background_working_conversations.pop(bg_cid, None)
                            
                            # Captura a chave de visualização atual para suprimir retorno imediato até nova ação do usuário
                            _, current_view_key = self.find_user_viewed_conversation()
                            self.suppressed_view_until_key = current_view_key
                            
                            # 1. Comuta automaticamente para a conversa que concluiu
                            await self.switch_conversation(bg_cid, notify=True, status="CONCLUÍDO")
                            
                            # 2. Dispara alerta sensorial duplo: Flash 2x na tela + som ampliado + notificação Web
                            if self.on_event:
                                await self.on_event({
                                    "event": "task_completed",
                                    "data": {
                                        "step_index": step_index,
                                        "summary": content[:180] + "..." if len(content) > 180 else content,
                                        "timestamp": datetime.now(timezone.utc).isoformat(),
                                        "quota": self.quota_stats
                                    }
                                })
                            break
                    except Exception:
                        pass
            except Exception as e:
                print(f"[Monitor] Erro no polling de segundo plano ({bg_cid}): {e}")

    async def poll_updates(self):
        """Verifica navegação do usuário, tarefas em segundo plano e novos eventos."""
        # 1. Se ainda não há conversa ativa, inicializa
        if not self.current_conversation_id:
            active_id = self.find_active_conversation()
            if active_id:
                await self.switch_conversation(active_id)
            return

        # 2. Verifica se o usuário trocou de conversa/projeto no PC (respeita a seleção humana e não interrompe com updates em background)
        await self.check_user_navigation()

        # 3. Monitora se alguma tarefa em execução em segundo plano concluiu ("Working..." finalizado)
        await self.poll_background_conversations()

        # 4. Monitora em tempo real se o modelo de IA foi trocado na conversa ativa
        if self.current_conversation_id:
            old_model = self.active_model
            new_model = self.detect_model_name(self.current_conversation_id)
            if new_model and new_model != old_model:
                print(f"[Monitor] Modelo de IA alterado em tempo real: {old_model} -> {new_model}")
                self.active_model = new_model
                self.quota_stats["active_model"] = new_model
                self.calculate_quota()
                if self.on_event:
                    await self.on_event({
                        "event": "model_changed",
                        "data": {
                            "active_model": self.active_model,
                            "quota": self.quota_stats
                        }
                    })
            
        if not self.current_transcript_path or not self.current_transcript_path.exists():
            return

        try:
            current_size = os.path.getsize(self.current_transcript_path)
            if current_size < self.file_offset:
                self.file_offset = 0

            if current_size == self.file_offset:
                return

            with open(self.current_transcript_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self.file_offset)
                new_lines = f.readlines()
                self.file_offset = f.tell()

            for line in new_lines:
                line = line.strip()
                if not line:
                    continue
                try:
                    step = json.loads(line)
                    await self._process_step(step)
                except Exception as e:
                    print(f"[Monitor] Erro processando linha: {e}")

        except Exception as e:
            print(f"[Monitor] Erro no polling: {e}")

    async def _process_step(self, step: Dict[str, Any]):
        """Analisa a etapa recebida e dispara eventos de WebSocket."""
        # Revalida modelo ativo na chegada de novas etapas
        if self.current_conversation_id:
            self.detect_model_name(self.current_conversation_id)

        step_index = step.get("step_index", 0)
        source = step.get("source", "")
        step_type = step.get("type", "")
        status = step.get("status", "")
        tool_calls = step.get("tool_calls", [])
        content = step.get("content", "")

        self.last_step_index = step_index
        formatted = self._format_step_message(step)
        if formatted:
            formatted["active_model"] = self.active_model

        # 1. Usuário fez uma solicitação no PC
        if source == "USER_EXPLICIT" or step_type == "USER_INPUT":
            self.current_turn_status = "PROCESSANDO"
            if self.on_event and formatted:
                await self.on_event({
                    "event": "user_message",
                    "data": formatted
                })
        elif status == "RUNNING" or tool_calls:
            self.current_turn_status = "PROCESSANDO"
            if self.on_event:
                await self.on_event({
                    "event": "status_change",
                    "data": {
                        "status": "PROCESSANDO",
                        "active_model": self.active_model
                    }
                })
        elif status == "DONE":
            is_final_response = (
                source == "MODEL" 
                and step_type == "PLANNER_RESPONSE" 
                and not tool_calls 
                and bool(content)
            )

            if is_final_response and self.last_notified_step != step_index:
                self.last_notified_step = step_index
                self.current_turn_status = "CONCLUÍDO"
                
                # Recalcula cota oficial ao concluir
                self.calculate_quota()
                
                print(f"[Monitor] *** CONCLUSÃO FINAL DETECTADA (Step {step_index}) ***")
                if self.on_event and formatted:
                    await self.on_event({
                        "event": "conclusion_message",
                        "data": formatted
                    })
                    # DISPARO DO ALERTA: Aciona flash na tela e som suave no celular
                    await self.on_event({
                        "event": "task_completed",
                        "data": {
                            "step_index": step_index,
                            "active_model": self.active_model,
                            "summary": content[:180] + "..." if len(content) > 180 else content,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "quota": self.quota_stats
                        }
                    })

    async def run_loop(self):
        """Loop contínuo de monitoramento assíncrono."""
        self.is_running = True
        quota_ticker = 0
        while self.is_running:
            try:
                # A cada 5 segundos atualiza a cota oficial e transmite em tempo real
                quota_ticker += 1
                if quota_ticker >= 10:
                    quota_ticker = 0
                    if self.current_conversation_id:
                        self.detect_model_name(self.current_conversation_id)
                    self.calculate_quota()
                    if self.on_event:
                        await self.on_event({
                            "event": "quota_update",
                            "data": self.quota_stats
                        })
                
                await self.poll_updates()
            except Exception as e:
                print(f"[Monitor] Erro no loop de monitoramento: {e}")
            await asyncio.sleep(config.POLL_INTERVAL)

    def stop(self):
        self.is_running = False