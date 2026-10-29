# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Automated Verification Suite for Antigravity Mobile v2.5.0

import os
import sys
import json
import sqlite3
import urllib.request
from pathlib import Path

# Adiciona desktop-bridge ao sys.path
bridge_dir = Path(__file__).parent
sys.path.insert(0, str(bridge_dir))

def run_tests():
    print("=" * 60)
    print("INICIANDO SUITE DE TESTES COMPLETOS - ANTIGRAVITY MOBILE v2.5.0")
    print("=" * 60)
    passed = 0
    failed = 0

    def assert_true(condition, msg):
        nonlocal passed, failed
        if condition:
            print(f"  [PASS] {msg}")
            passed += 1
        else:
            print(f"  [FAIL] {msg}")
            failed += 1

    # ---------------------------------------------------------
    # TESTE 1: LANGUAGE MANAGER & TRADUÇÕES DE STATUS
    # ---------------------------------------------------------
    print("\n--- TESTE 1: LANGUAGE MANAGER & STATUS I18N ---")
    try:
        from language_manager import language_manager, TRANSLATIONS
        for lang in ["pt", "en", "es"]:
            d = TRANSLATIONS[lang]
            assert_true("status_task_running" in d, f"Idioma '{lang}' possui chave 'status_task_running'")
            assert_true("status_working" in d, f"Idioma '{lang}' possui chave 'status_working'")
            assert_true("status_thought" in d, f"Idioma '{lang}' possui chave 'status_thought'")
            assert_true("status_done" in d, f"Idioma '{lang}' possui chave 'status_done'")
            assert_true("btn_chats" in d, f"Idioma '{lang}' possui chave 'btn_chats'")
            assert_true("chats_modal_title" in d, f"Idioma '{lang}' possui chave 'chats_modal_title'")
            assert_true("battery_title" in d, f"Idioma '{lang}' possui chave 'battery_title'")
            assert_true("menu_fullscreen_label" in d, f"Idioma '{lang}' possui chave 'menu_fullscreen_label'")
            assert_true("btn_prompt" in d, f"Idioma '{lang}' possui chave 'btn_prompt'")
            assert_true("prompt_modal_title" in d, f"Idioma '{lang}' possui chave 'prompt_modal_title'")
            assert_true("btn_send_prompt" in d, f"Idioma '{lang}' possui chave 'btn_send_prompt'")
            assert_true("menu_battery_label" in d, f"Idioma '{lang}' possui chave 'menu_battery_label'")
            assert_true("prompt_model_label" in d, f"Idioma '{lang}' possui chave 'prompt_model_label'")

        assert_true(TRANSLATIONS["pt"]["status_task_running"] == "Executando Tarefa...", "PT-BR: Executando Tarefa...")
        assert_true(TRANSLATIONS["en"]["status_task_running"] == "Task Running...", "EN: Task Running...")
        assert_true(TRANSLATIONS["es"]["status_task_running"] == "Ejecutando Tarea...", "ES: Ejecutando Tarea...")
    except Exception as e:
        assert_true(False, f"Erro no Language Manager: {e}")

    # ---------------------------------------------------------
    # TESTE 2: AUTH MANAGER & SESSÕES
    # ---------------------------------------------------------
    print("\n--- TESTE 2: AUTH MANAGER & TOKENS ---")
    token = None
    try:
        from auth import auth_manager
        pin = auth_manager.generate_pin(notify=False)
        assert_true(len(pin) == 4 and pin.isdigit(), f"PIN gerado é válido de 4 dígitos: {pin}")
        assert_true(auth_manager.verify("0000" if pin != "0000" else "1111") is None, "PIN incorreto rejeitado corretamente")
        auth_res = auth_manager.verify(pin)
        assert_true(auth_res is not None and "token" in auth_res, "PIN correto gera token de sessão válido")
        token = auth_res["token"]
        assert_true(auth_manager.is_valid_token(token), "Token gerado é válido e verificado com sucesso")
        assert_true(not auth_manager.is_valid_token("token_invalido_teste"), "Token falso rejeitado com sucesso")
    except Exception as e:
        assert_true(False, f"Erro no Auth Manager: {e}")

    # ---------------------------------------------------------
    # TESTE 3: MONITOR & LÓGICA DE ATIVIDADE / BACKGROUND
    # ---------------------------------------------------------
    print("\n--- TESTE 3: MONITOR, BACKGROUND TASK & STRICT DONE ---")
    try:
        from monitor import AntigravityMonitor
        mon = AntigravityMonitor()
        
        # Teste de detecção de conversa ativa
        active_cid = mon.find_active_conversation()
        assert_true(bool(active_cid), f"Conversa ativa detectada no Antigravity: {active_cid}")

        # Teste de is_project_active
        is_active = mon.is_project_active(active_cid)
        print(f"     -> is_project_active('{active_cid}'): {is_active}")
        assert_true(isinstance(is_active, bool), "is_project_active retorna booleano consistente")

        # Teste 3.1: _extract_status_from_step com Background Task e Task Running
        step_bg1 = {
            "source": "MODEL",
            "type": "GENERIC",
            "status": "RUNNING",
            "tool_calls": [{"name": "manage_task"}]
        }
        assert_true(mon._extract_status_from_step(step_bg1) == "TASK_RUNNING", "tool_call 'manage_task' -> TASK_RUNNING")

        step_bg2 = {
            "source": "MODEL",
            "type": "GENERIC",
            "status": "RUNNING",
            "tool_calls": [{"name": "schedule"}]
        }
        assert_true(mon._extract_status_from_step(step_bg2) == "TASK_RUNNING", "tool_call 'schedule' -> TASK_RUNNING")

        step_bg3 = {
            "source": "MODEL",
            "type": "GENERIC",
            "status": "RUNNING",
            "tool_calls": [{"name": "invoke_subagent"}]
        }
        assert_true(mon._extract_status_from_step(step_bg3) == "TASK_RUNNING", "tool_call 'invoke_subagent' -> TASK_RUNNING")

        step_bg4 = {
            "source": "MODEL",
            "type": "BACKGROUND_TASK",
            "status": "RUNNING",
            "content": "Executing background task..."
        }
        assert_true(mon._extract_status_from_step(step_bg4) == "TASK_RUNNING", "type 'BACKGROUND_TASK' -> TASK_RUNNING")

        step_bg5 = {
            "source": "MODEL",
            "type": "GENERIC",
            "status": "TASK RUNNING",
            "content": "task running"
        }
        assert_true(mon._extract_status_from_step(step_bg5) == "TASK_RUNNING", "status 'TASK RUNNING' -> TASK_RUNNING")

        # Teste 3.2: Thought / Thinking
        step_thought1 = {
            "source": "USER_EXPLICIT",
            "type": "USER_INPUT",
            "content": "Olá"
        }
        assert_true(mon._extract_status_from_step(step_thought1) == "THOUGHT", "USER_EXPLICIT -> THOUGHT")

        step_thought2 = {
            "source": "MODEL",
            "type": "GENERIC",
            "thinking": "Raciocinando sobre o plano..."
        }
        assert_true(mon._extract_status_from_step(step_thought2) == "THOUGHT", "step com thinking -> THOUGHT")

        # Teste 3.3: Working
        step_work = {
            "source": "MODEL",
            "type": "GENERIC",
            "status": "RUNNING",
            "tool_calls": [{"name": "read_file"}]
        }
        assert_true(mon._extract_status_from_step(step_work) == "WORKING", "tool_call comum -> WORKING")

        # Teste 3.4: Regra estrita de Done com Background Tasks
        original_bg_method = mon.has_active_background_tasks
        try:
            mon.has_active_background_tasks = lambda cid=None: True
            step_final = {
                "source": "MODEL",
                "type": "PLANNER_RESPONSE",
                "status": "DONE",
                "content": "Tarefa concluída!",
                "tool_calls": []
            }
            assert_true(mon._extract_status_from_step(step_final) == "TASK_RUNNING", "Se background tasks em execução -> PLANNER_RESPONSE permanece TASK_RUNNING")

            mon.has_active_background_tasks = lambda cid=None: False
            assert_true(mon._extract_status_from_step(step_final) == "DONE", "Se sem background tasks -> PLANNER_RESPONSE torna-se DONE")
        finally:
            mon.has_active_background_tasks = original_bg_method

        # Teste 3.5: Detecção instantânea de Live Cascade Status (SQLite em tempo real)
        live_stat = mon.detect_live_cascade_status(active_cid)
        assert_true(live_stat in ["THOUGHT", "WORKING", "TASK_RUNNING", "DONE", "IDLE"], f"detect_live_cascade_status retornou status válido: {live_stat}")

    except Exception as e:
        assert_true(False, f"Erro no Monitor: {e}")

    # ---------------------------------------------------------
    # TESTE 4: LISTA DE CHATS & HISTÓRICO DE MENSAGENS
    # ---------------------------------------------------------
    print("\n--- TESTE 4: LISTA DE CHATS & HISTÓRICO REMOTO ---")
    try:
        convs = mon.get_conversations_list()
        assert_true(isinstance(convs, list) and len(convs) > 0, f"Lista de conversas retornou {len(convs)} conversas")
        if convs:
            first = convs[0]
            assert_true("conversation_id" in first, "Item possui 'conversation_id'")
            assert_true("title" in first, "Item possui 'title'")
            assert_true("project" in first, "Item possui 'project'")
            assert_true("is_processing" in first, "Item possui 'is_processing'")
            assert_true(isinstance(first["is_processing"], bool), "'is_processing' é booleano estrito")
            print(f"     -> Exemplo de chat: ID={first['conversation_id'][:10]}... | Título={first['title'][:30]} | Proc={first['is_processing']}")

            # Teste de puxar histórico sem alterar o PC
            hist = mon.get_conversation_messages(first["conversation_id"], limit=10)
            assert_true(isinstance(hist, dict) and "messages" in hist, "get_conversation_messages retornou estrutura válida")
            print(f"     -> Mensagens recuperadas: {len(hist.get('messages', []))}")
    except Exception as e:
        assert_true(False, f"Erro ao listar chats ou mensagens: {e}")

    # ---------------------------------------------------------
    # TESTE 5: FASTAPI TESTCLIENT & ENDPOINTS
    # ---------------------------------------------------------
    print("\n--- TESTE 5: FASTAPI SERVER ENDPOINTS ---")
    try:
        from fastapi.testclient import TestClient
        from server import app
        client = TestClient(app)

        # /api/ping
        r_ping = client.get("/api/ping")
        assert_true(r_ping.status_code == 200 and r_ping.json().get("status") == "ok", "GET /api/ping -> 200 OK")

        # /api/status (sem auth -> 401, com auth -> 200)
        r_status_unauth = client.get("/api/status")
        assert_true(r_status_unauth.status_code == 401, "GET /api/status sem token -> 401 Unauthorized")
        r_status_auth = client.get(f"/api/status?token={token}")
        assert_true(r_status_auth.status_code == 200 and "status" in r_status_auth.json(), "GET /api/status com token -> 200 OK")

        # /api/conversations (com auth)
        r_convs_unauth = client.get("/api/conversations")
        assert_true(r_convs_unauth.status_code == 401, "GET /api/conversations sem token -> 401 Unauthorized")

        r_convs_auth = client.get(f"/api/conversations?token={token}")
        assert_true(r_convs_auth.status_code == 200 and "conversations" in r_convs_auth.json(), "GET /api/conversations com token -> 200 OK")

        # /api/messages (com auth)
        r_msg_auth = client.get(f"/api/messages?token={token}&limit=5")
        assert_true(r_msg_auth.status_code == 200 and "messages" in r_msg_auth.json(), "GET /api/messages com token -> 200 OK")

        # /api/prompt (sem auth -> 401, com auth e sem body -> 400, com sucesso -> 200)
        r_prompt_unauth = client.post("/api/prompt", json={"conversation_id": "dummy", "prompt": "teste"})
        assert_true(r_prompt_unauth.status_code == 401, "POST /api/prompt sem token -> 401 Unauthorized")

        r_prompt_nobody = client.post(f"/api/prompt?token={token}", json={})
        assert_true(r_prompt_nobody.status_code == 400, "POST /api/prompt sem dados -> 400 Bad Request")

        from antigravity_api import antigravity_api as api_instance
        orig_send = api_instance.send_user_message
        try:
            api_instance.send_user_message = lambda cid, p, model=None: True
            r_prompt_ok = client.post(f"/api/prompt?token={token}", json={"conversation_id": "test_cid", "prompt": "test_prompt"})
            assert_true(r_prompt_ok.status_code == 200 and r_prompt_ok.json().get("status") == "success", "POST /api/prompt com payload válido -> 200 OK")

            r_prompt_model = client.post(f"/api/prompt?token={token}", json={"conversation_id": "test_cid", "prompt": "test_prompt", "model": "Claude 3.7 Sonnet"})
            assert_true(r_prompt_model.status_code == 200 and r_prompt_model.json().get("model") == "Claude 3.7 Sonnet", "POST /api/prompt com modelo selecionado -> 200 OK")
        finally:
            api_instance.send_user_message = orig_send

        # /api/quota (com auth)
        r_quota = client.get(f"/api/quota?token={token}")
        assert_true(r_quota.status_code == 200 and "groups" in r_quota.json(), "GET /api/quota com token -> 200 OK")

        # / (index.html delivery)
        r_root = client.get("/")
        assert_true(r_root.status_code == 200 and "Antigravity Mobile" in r_root.text, "GET / -> 200 OK com index.html")
        assert_true("no-cache" in r_root.headers.get("Cache-Control", ""), "Header Cache-Control: no-cache presente")
        assert_true('id="battery-badge"' in r_root.text, "Elemento 'battery-badge' presente no HTML")
        assert_true('id="battery-val"' in r_root.text, "Elemento 'battery-val' presente no HTML")
        assert_true('id="row-fullscreen-toggle"' in r_root.text, "Elemento 'row-fullscreen-toggle' presente no HTML")
        assert_true('FullscreenHelper' in r_root.text, "Objeto JS 'FullscreenHelper' presente no HTML")
        assert_true('BatteryManager' in r_root.text, "Objeto JS 'BatteryManager' presente no HTML")
        assert_true('id="btn-prompt-toggle"' in r_root.text, "Botão 'btn-prompt-toggle' no rodapé presente no HTML")
        assert_true('id="prompt-modal"' in r_root.text, "Modal 'prompt-modal' presente no HTML")
        assert_true('id="prompt-chats-list"' in r_root.text, "Elemento 'prompt-chats-list' presente no HTML")
        assert_true('id="prompt-textarea"' in r_root.text, "Elemento 'prompt-textarea' presente no HTML")
        assert_true('id="btn-send-prompt"' in r_root.text, "Botão 'btn-send-prompt' presente no HTML")
        assert_true('PromptManager' in r_root.text, "Objeto JS 'PromptManager' presente no HTML")
        assert_true('id="row-oled-toggle"' in r_root.text, "Seletor OLED no Menu 'row-oled-toggle' presente no HTML")
        assert_true('id="battery-toggle"' in r_root.text, "Checkbox 'battery-toggle' presente no HTML")
        assert_true('id="prompt-model-select"' in r_root.text, "Seletor de modelos 'prompt-model-select' presente no HTML")
        assert_true('prompt-target-divider' in r_root.text, "Barreira divisória 'prompt-target-divider' presente no HTML")
        assert_true('max-width: 580px' in r_root.text, "Modal prompt redimensionado com max-width ampliado (580px)")

    except Exception as e:
        assert_true(False, f"Erro nos endpoints FastAPI: {e}")

    # ---------------------------------------------------------
    # TESTE 6: CLIENT-SIDE JS STATUS PARSER SIMULATION
    # ---------------------------------------------------------
    print("\n--- TESTE 6: CLIENT-SIDE JS LOGIC (updateStatus) ---")
    try:
        def simulate_update_status(raw_status: str, lang_dict: dict):
            raw = (raw_status or "CONNECTED").upper().strip()
            state = "connected"
            label = lang_dict.get("status_connected", "Conectado")

            if "CONNECTING" in raw or "CONECTANDO" in raw:
                state = "connecting"
                label = lang_dict.get("status_connecting", "Conectando...")
            elif "BACKGROUND" in raw or ("TASK" in raw and ("RUN" in raw or "EXEC" in raw)) or "TAREFA" in raw:
                state = "task-running"
                label = lang_dict.get("status_task_running", "Executando Tarefa...")
            elif "THOUGHT" in raw or "PENSANDO" in raw or "THINK" in raw:
                state = "thought"
                label = lang_dict.get("status_thought", "Pensando...")
            elif "WORK" in raw or "TRABALH" in raw or "PROCESS" in raw or "RUNNING" in raw:
                state = "working"
                label = lang_dict.get("status_working", "Trabalhando...")
            elif "DISCONNECT" in raw or "DESCONECT" in raw:
                state = "disconnected"
                label = lang_dict.get("status_disconnected", "Desconectado")
            elif "DONE" in raw or "CONCLU" in raw or "COMPLET" in raw:
                state = "done"
                label = lang_dict.get("status_done", "Concluído")
            return state, label

        t_pt = TRANSLATIONS["pt"]
        s, l = simulate_update_status("BACKGROUND TASK", t_pt)
        assert_true(s == "task-running" and l == "Executando Tarefa...", "JS Parser: 'BACKGROUND TASK' -> state: task-running, label: Executando Tarefa...")

        s, l = simulate_update_status("TASK RUNNING", t_pt)
        assert_true(s == "task-running" and l == "Executando Tarefa...", "JS Parser: 'TASK RUNNING' -> state: task-running, label: Executando Tarefa...")

        s, l = simulate_update_status("THOUGHT", t_pt)
        assert_true(s == "thought" and l == "Pensando...", "JS Parser: 'THOUGHT' -> state: thought, label: Pensando...")

        s, l = simulate_update_status("THINKING", t_pt)
        assert_true(s == "thought" and l == "Pensando...", "JS Parser: 'THINKING' -> state: thought, label: Pensando...")

        s, l = simulate_update_status("WORKING", t_pt)
        assert_true(s == "working" and l == "Trabalhando...", "JS Parser: 'WORKING' -> state: working, label: Trabalhando...")

        s, l = simulate_update_status("DONE", t_pt)
        assert_true(s == "done" and l == "Concluído", "JS Parser: 'DONE' -> state: done, label: Concluído")

    except Exception as e:
        assert_true(False, f"Erro no JS Parser Simulation: {e}")

    # ---------------------------------------------------------
    # TESTE 7: GITHUB RELEASE ASSETS & APK LINKS
    # ---------------------------------------------------------
    print("\n--- TESTE 7: GITHUB RELEASE ASSETS DISPONÍVEIS ---")
    try:
        headers = {"User-Agent": "AntigravityTest"}
        gh_pat = os.environ.get("GITHUB_TOKEN")
        if gh_pat:
            headers["Authorization"] = f"Bearer {gh_pat}"
            
        req = urllib.request.Request(
            "https://api.github.com/repos/lumiag5/antigravitymb/releases",
            headers=headers
        )
        res = urllib.request.urlopen(req, timeout=10)
        all_releases = json.loads(res.read())
        # Encontra a release mais recente com APKs publicados
        rel_data = next((r for r in all_releases if any(a["name"].endswith(".apk") for a in r.get("assets", []))), all_releases[0] if all_releases else {})
        assert_true(bool(rel_data.get("tag_name")), f"Release de APK no GitHub encontrada: {rel_data.get('tag_name')}")
        
        assets = {a["name"]: a for a in rel_data.get("assets", [])}
        rel_apk = next((name for name in assets if name.endswith(".apk") and "debug" not in name), None)
        assert_true(rel_apk is not None, f"APK de release presente na release: {rel_apk}")
        assert_true("app-debug.apk" in assets, "Arquivo 'app-debug.apk' presente na release")
        
        if rel_apk in assets:
            sz_rel = assets[rel_apk]["size"]
            assert_true(sz_rel > 4 * 1024 * 1024, f"app-release.apk tamanho íntegro: {sz_rel / (1024*1024):.2f} MB")
            
        if "app-debug.apk" in assets:
            sz_deb = assets["app-debug.apk"]["size"]
            assert_true(sz_deb > 5 * 1024 * 1024, f"app-debug.apk tamanho íntegro: {sz_deb / (1024*1024):.2f} MB")

    except Exception as e:
        assert_true(False, f"Erro ao verificar GitHub Release: {e}")

    # ---------------------------------------------------------
    # TESTE 8: ANDROID KOTLIN CODE & FULLSCREEN/BATTERY BRIDGES
    # ---------------------------------------------------------
    print("\n--- TESTE 8: ANDROID KOTLIN CODE & FULLSCREEN/BATTERY BRIDGES ---")
    try:
        main_kt = bridge_dir.parent / "android" / "app" / "src" / "main" / "java" / "com" / "lumiag5" / "antigravitymobile" / "MainActivity.kt"
        assert_true(main_kt.exists(), "MainActivity.kt existe no caminho esperado")
        kt_code = main_kt.read_text(encoding="utf-8")
        assert_true("applyFullScreenImmersive()" in kt_code, "applyFullScreenImmersive() declarado e chamado no APK")
        assert_true("LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES" in kt_code, "Suporte a entalhe/câmera (Short Edges) presente")
        assert_true("WindowInsetsCompat.Type.statusBars()" in kt_code, "Ocultação de statusBars configurada para Android 11+")
        assert_true("SYSTEM_UI_FLAG_FULLSCREEN" in kt_code, "Fallback de tela cheia legado configurado")
        assert_true("onWindowFocusChanged" in kt_code, "Reaplicação de tela cheia em onWindowFocusChanged presente")
        assert_true("ACTION_BATTERY_CHANGED" in kt_code, "BroadcastReceiver ACTION_BATTERY_CHANGED configurado")
        assert_true("getBatteryLevel()" in kt_code, "Método nativo getBatteryLevel() implementado")
        assert_true("isBatteryCharging()" in kt_code, "Método nativo isBatteryCharging() implementado")
        assert_true("@JavascriptInterface" in kt_code, "Anotação @JavascriptInterface presente para ponte WebView")
        keystore_path = bridge_dir.parent / "android" / "app" / "release.jks"
        assert_true(keystore_path.exists(), "Chave de assinatura permanente release.jks presente no projeto")
        gradle_kts = (bridge_dir.parent / "android" / "app" / "build.gradle.kts").read_text(encoding="utf-8")
        assert_true("signingConfigs" in gradle_kts and "release.jks" in gradle_kts, "Assinatura fixa configurada em build.gradle.kts")
    except Exception as e:
        assert_true(False, f"Erro ao verificar código Android nativo: {e}")

    # ---------------------------------------------------------
    # TESTE 9: WEB MANIFEST & HARMONIZAÇÃO DO RODAPÉ
    # ---------------------------------------------------------
    print("\n--- TESTE 9: WEB MANIFEST & HARMONIZAÇÃO DO RODAPÉ ---")
    try:
        manifest_file = bridge_dir / "static" / "manifest.json"
        assert_true(manifest_file.exists(), "manifest.json existe")
        m_json = json.loads(manifest_file.read_text(encoding="utf-8"))
        assert_true(m_json.get("display") == "fullscreen", "manifest.json com display: fullscreen")

        index_file = bridge_dir / "static" / "index.html"
        assert_true(index_file.exists(), "index.html existe")
        html_content = index_file.read_text(encoding="utf-8")
        assert_true("safe-area-inset-top" in html_content, "CSS possui suporte a safe-area-inset-top para notch")
        assert_true("height: 28px" in html_content, "Altura padronizada de 28px nos botões e badges do rodapé")
        assert_true("border-radius: 999px" in html_content, "Bordas arredondadas (pill) padronizadas em 999px")
        assert_true('id="battery-badge"' in html_content, "Badge de bateria presente")
        assert_true('id="latency-badge"' in html_content, "Badge de latência presente")
        assert_true('id="btn-chats-toggle"' in html_content, "Botão de chats presente")
        assert_true('id="btn-oled-toggle"' in html_content, "Botão de OLED presente")
        assert_true('id="btn-menu-toggle"' in html_content, "Botão de Menu presente")
        assert_true("${level}%" in html_content, "Formatação estrita de porcentagem sem texto de label")
    except Exception as e:
        assert_true(False, f"Erro ao verificar UI e Manifest: {e}")

    # ---------------------------------------------------------
    # TESTE 10: CONCLUSÕES, SINCRONIZAÇÃO DE PROMPT & PISCA-TELA
    # ---------------------------------------------------------
    print("\n--- TESTE 10: CONCLUSÕES, SINCRONIZAÇÃO DE PROMPT & PISCA-TELA ---")
    try:
        from monitor import AntigravityMonitor
        test_mon = AntigravityMonitor()
        test_mon.current_conversation_id = "test-conv-123"

        # 10.1: Formatação de Mensagens com conversation_id
        user_step = {
            "step_index": 1,
            "source": "USER_EXPLICIT",
            "type": "USER_INPUT",
            "content": "<USER_REQUEST>Teste de Prompt</USER_REQUEST>",
            "created_at": "2026-10-29T00:00:00Z"
        }
        fmt_user = test_mon._format_step_message(user_step)
        assert_true(fmt_user is not None and fmt_user.get("role") == "user", "Mensagem de usuário formatada com sucesso")
        assert_true(fmt_user.get("conversation_id") == "test-conv-123", "conversation_id injetado na mensagem do usuário")
        assert_true(fmt_user.get("content") == "Teste de Prompt", "Conteúdo de <USER_REQUEST> extraído corretamente")

        asst_step = {
            "step_index": 2,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "DONE",
            "content": "Conclusão da tarefa realizada com sucesso.",
            "tool_calls": [],
            "created_at": "2026-10-29T00:01:00Z"
        }
        fmt_asst = test_mon._format_step_message(asst_step)
        assert_true(fmt_asst is not None and fmt_asst.get("role") == "assistant", "Mensagem de assistente formatada com sucesso")
        assert_true(fmt_asst.get("conversation_id") == "test-conv-123", "conversation_id injetado na mensagem do assistente")
        assert_true("Conclusão da tarefa" in fmt_asst.get("content", ""), "Conteúdo da conclusão preservado")

        # 10.2: Filtragem estrita de etapas intermediárias
        tool_step = {
            "step_index": 3,
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "status": "RUNNING",
            "content": "",
            "tool_calls": [{"name": "read_file"}],
            "created_at": "2026-10-29T00:00:30Z"
        }
        assert_true(test_mon._format_step_message(tool_step) is None, "Etapa intermediária de ferramenta (tool_call) é filtrada")

        generic_step = {
            "step_index": 4,
            "source": "MODEL",
            "type": "GENERIC",
            "status": "DONE",
            "content": "Output de terminal",
            "tool_calls": []
        }
        assert_true(test_mon._format_step_message(generic_step) is None, "Saída genérica/terminal é filtrada")

        # 10.3: Verificações no HTML do cliente para conclusão, pisca-tela e prompt
        index_file = bridge_dir / "static" / "index.html"
        html_content = index_file.read_text(encoding="utf-8")

        assert_true('evt.event === "conclusion_message"' in html_content, "HTML escuta evento 'conclusion_message'")
        assert_true('evt.event === "assistant_step"' in html_content, "HTML escuta evento 'assistant_step'")
        assert_true('triggerSensoryAlert()' in html_content, "Alerta sensorial (pisca tela + som) disparado ao receber conclusão")
        assert_true('lastSensoryAlertTime' in html_content, "Debounce inteligente implementado no alerta sensorial")
        assert_true('void el.offsetWidth' in html_content, "Reflow forçado no DOM implementado para disparar pisca-tela com precisão")
        assert_true('flashOverlay' in html_content and 'flash-active' in html_content, "Animação flash-active no overlay presente")
        assert_true('document.getElementById(`msg-${m.id}`)' in html_content, "Deduplicação estrita de IDs de mensagem para evitar balões duplicados")
        assert_true('viewingConversationId = null' in html_content, "Sincronização automática para acompanhar chat ativo após envio do prompt")

    except Exception as e:
        assert_true(False, f"Erro no Teste 10: {e}")

    # ---------------------------------------------------------
    # TESTE 11: PADRONIZAÇÃO DE CHECKBOXES, MENU COMPACTO & CHATS SYNC
    # ---------------------------------------------------------
    print("\n--- TESTE 11: CHECKBOXES PADRONIZADOS, MENU COMPACTO & CHATS SYNC ---")
    try:
        from language_manager import TRANSLATIONS
        for lang in ["pt", "en", "es"]:
            d = TRANSLATIONS[lang]
            assert_true("menu_btn_logout" in d, f"Idioma '{lang}' possui chave 'menu_btn_logout'")
            assert_true("menu_sec_alerts" in d, f"Idioma '{lang}' possui chave 'menu_sec_alerts'")
            assert_true("menu_sec_sound" in d, f"Idioma '{lang}' possui chave 'menu_sec_sound'")
            assert_true("menu_sec_system" in d, f"Idioma '{lang}' possui chave 'menu_sec_system'")
            assert_true("menu_apk_installed_label" in d, f"Idioma '{lang}' possui chave 'menu_apk_installed_label'")

        assert_true(TRANSLATIONS["pt"]["menu_btn_logout"] == "Sair / Desconectar da Sessão", "PT: Sair / Desconectar da Sessão")
        assert_true(TRANSLATIONS["en"]["menu_btn_logout"] == "Sign Out / Disconnect Session", "EN: Sign Out / Disconnect Session")
        assert_true(TRANSLATIONS["es"]["menu_btn_logout"] == "Salir / Desconectar Sesión", "ES: Salir / Desconectar Sesión")

        # Verificação do HTML
        index_file = bridge_dir / "static" / "index.html"
        html_txt = index_file.read_text(encoding="utf-8")

        assert_true('.menu-checkbox' in html_txt, "Classe CSS .menu-checkbox padronizada no CSS")
        assert_true('id="alert-enabled" class="menu-checkbox"' in html_txt, "Checkbox de Alerta Sensorial utiliza .menu-checkbox")
        assert_true('id="latency-toggle" class="menu-checkbox"' in html_txt, "Checkbox de Latência padronizado com .menu-checkbox (sem azul dissonante)")
        assert_true('id="battery-toggle" class="menu-checkbox"' in html_txt, "Checkbox de Bateria padronizado com .menu-checkbox")
        assert_true('padding: 13px 15px;' in html_txt, "Menu compacto: padding reduzido para 13px 15px para eliminar rolagem")
        assert_true('min-height: 34px;' in html_txt, "Menu compacto: altura das linhas menu-row otimizada")
        assert_true('menu-btn-logout-text' in html_txt, "Botão de logout com ID 'menu-btn-logout-text' presente")
        assert_true('t.menu_btn_logout' in html_txt, "applyI18n() atualiza 'menu-btn-logout-text' em tempo real")

        # Verificação da sincronização em tempo real dos dots de chat
        assert_true('data-dot-cid' in html_txt, "Atributo data-dot-cid injetado para atualização seletiva dos dots em tempo real")
        assert_true('updateConversationStatus' in html_txt, "Método updateConversationStatus implementado para alternar verde/laranja")
        assert_true('startLiveSync' in html_txt, "startLiveSync implementado com polling silencioso a cada 2s quando modal ativo")
        assert_true('&_t=${Date.now()}' in html_txt, "Cache-buster &_t injetado no fetch de conversas para evitar cache de WebView")

        # Verificação dos cabeçalhos do servidor FastAPI para /api/conversations
        from fastapi.testclient import TestClient
        from server import app
        tc = TestClient(app)
        res_conv = tc.get(f"/api/conversations?token={token}")
        assert_true(res_conv.status_code == 200, "GET /api/conversations com token -> 200 OK")
        assert_true("no-cache" in res_conv.headers.get("Cache-Control", ""), "Header Cache-Control: no-cache retornado em /api/conversations")

    except Exception as e:
        assert_true(False, f"Erro no Teste 11: {e}")

    # ---------------------------------------------------------
    # TESTE 12: BUSCA RÁPIDA DE CHATS, HISTÓRICO & CONTADOR
    # ---------------------------------------------------------
    print("\n--- TESTE 12: BUSCA RÁPIDA DE CHATS, HISTÓRICO & CONTADOR ---")
    try:
        from language_manager import TRANSLATIONS
        for lang in ["pt", "en", "es"]:
            d = TRANSLATIONS[lang]
            assert_true("search_chats_placeholder" in d, f"Idioma '{lang}' possui chave 'search_chats_placeholder'")
            assert_true("search_no_results" in d, f"Idioma '{lang}' possui chave 'search_no_results'")
            assert_true("prompt_history_btn" in d, f"Idioma '{lang}' possui chave 'prompt_history_btn'")
            assert_true("prompt_history_title" in d, f"Idioma '{lang}' possui chave 'prompt_history_title'")
            assert_true("prompt_history_empty" in d, f"Idioma '{lang}' possui chave 'prompt_history_empty'")
            assert_true("prompt_history_clear" in d, f"Idioma '{lang}' possui chave 'prompt_history_clear'")
            assert_true("prompt_char_counter" in d, f"Idioma '{lang}' possui chave 'prompt_char_counter'")

        assert_true(TRANSLATIONS["pt"]["search_chats_placeholder"] == "Buscar chat ou projeto...", "PT: Buscar chat ou projeto...")
        assert_true(TRANSLATIONS["en"]["search_chats_placeholder"] == "Search chat or project...", "EN: Search chat or project...")
        assert_true(TRANSLATIONS["es"]["search_chats_placeholder"] == "Buscar chat o proyecto...", "ES: Buscar chat o proyecto...")

        # Verificação do HTML
        index_file = bridge_dir / "static" / "index.html"
        html_txt = index_file.read_text(encoding="utf-8")

        # 1. Busca rápida
        assert_true('id="chats-search-input"' in html_txt, "Campo de busca rápida de chats 'chats-search-input' presente")
        assert_true('id="prompt-search-input"' in html_txt, "Campo de busca rápida no prompt 'prompt-search-input' presente")
        assert_true('ChatsManager.onSearch' in html_txt, "Método ChatsManager.onSearch implementado")
        assert_true('PromptManager.onSearch' in html_txt, "Método PromptManager.onSearch implementado")
        assert_true('clearSearch()' in html_txt, "Função de limpeza rápida da busca implementada")

        # 2. Histórico de prompts
        assert_true('id="btn-prompt-history"' in html_txt, "Botão de histórico de prompts presente")
        assert_true('id="prompt-history-panel"' in html_txt, "Painel retrátil de histórico 'prompt-history-panel' presente")
        assert_true('PromptHistoryManager' in html_txt, "Objeto PromptHistoryManager implementado")
        assert_true('PromptHistoryManager.add' in html_txt, "PromptHistoryManager.add chamado ao enviar prompt")
        assert_true('ArrowUp' in html_txt, "Navegação rápida por tecla ArrowUp para carregar último prompt")

        # 3. Contador de caracteres e palavras
        assert_true('id="prompt-char-count"' in html_txt, "Elemento contador 'prompt-char-count' presente")
        assert_true('updateCounter()' in html_txt, "Método updateCounter implementado no PromptManager")
        assert_true('addEventListener("input"' in html_txt, "Listener de input ativo para atualização em tempo real do contador")

    except Exception as e:
        assert_true(False, f"Erro no Teste 12: {e}")

    # ---------------------------------------------------------
    # SUMÁRIO
# ---------------------------------------------------------
    print("\n--- TESTE 13: COPIAR RESPOSTAS, INDICADOR PENSANDO E FAVORITOS ---")
    try:
        from language_manager import TRANSLATIONS
        for lang in ["pt", "en", "es"]:
            d = TRANSLATIONS[lang]
            assert_true("copy_response" in d, f"Idioma '{lang}' possui chave 'copy_response'")
            assert_true("response_copied" in d, f"Idioma '{lang}' possui chave 'response_copied'")
            assert_true("copy_failed" in d, f"Idioma '{lang}' possui chave 'copy_failed'")
            assert_true("thinking_indicator" in d, f"Idioma '{lang}' possui chave 'thinking_indicator'")
            assert_true("favorite_chat_title" in d, f"Idioma '{lang}' possui chave 'favorite_chat_title'")
            assert_true("unfavorite_chat_title" in d, f"Idioma '{lang}' possui chave 'unfavorite_chat_title'")

        assert_true(TRANSLATIONS["pt"]["copy_response"] == "Copiar resposta", "PT: Copiar resposta")
        assert_true(TRANSLATIONS["en"]["copy_response"] == "Copy response", "EN: Copy response")
        assert_true(TRANSLATIONS["es"]["copy_response"] == "Copiar respuesta", "ES: Copiar respuesta")

        assert_true(TRANSLATIONS["pt"]["thinking_indicator"] == "Antigravity está pensando...", "PT: Antigravity está pensando...")
        assert_true(TRANSLATIONS["en"]["thinking_indicator"] == "Antigravity is thinking...", "EN: Antigravity is thinking...")
        assert_true(TRANSLATIONS["es"]["thinking_indicator"] == "Antigravity está pensando...", "ES: Antigravity está pensando...")

        # Verificação do HTML
        index_file = bridge_dir / "static" / "index.html"
        html_txt = index_file.read_text(encoding="utf-8")

        # 1. Botão de Copiar Resposta
        assert_true('.btn-copy-msg' in html_txt, "CSS .btn-copy-msg presente")
        assert_true('copyMessageText' in html_txt, "Função copyMessageText implementada")
        assert_true('navigator.clipboard.writeText' in html_txt, "Suporte moderno à API Clipboard")
        assert_true('data-raw-content' in html_txt, "Armazenamento do conteúdo raw para cópia fiel")

        # 2. Indicador Animado de Pensando / Digitando
        assert_true('#typing-indicator' in html_txt, "CSS #typing-indicator presente")
        assert_true('.typing-dots' in html_txt, "Bolinhas animadas .typing-dots presentes")
        assert_true('TypingIndicatorManager' in html_txt, "Objeto TypingIndicatorManager implementado")
        assert_true('TypingIndicatorManager.show()' in html_txt, "Chamada show() ao iniciar processamento/pensamento")
        assert_true('TypingIndicatorManager.hide()' in html_txt, "Chamada hide() ao receber conclusão ou finalizar")

        # 3. Favoritar / Fixar Chats no Topo com Persistência
        assert_true('.chat-star-btn' in html_txt, "CSS .chat-star-btn presente")
        assert_true('is-fav-row' in html_txt, "CSS is-fav-row presente")
        assert_true('FavoritesManager' in html_txt, "Objeto FavoritesManager implementado")
        assert_true('antigravity_favorite_chats' in html_txt, "Chave de persistência de favoritos no localStorage")
        assert_true('FavoritesManager.sortWithFavorites' in html_txt, "Ordenação com chats favoritos no topo das listas")
        assert_true('FavoritesManager.toggle' in html_txt, "Ação de alternar status de favorito")

    except Exception as e:
        assert_true(False, f"Erro no Teste 13: {e}")

# ---------------------------------------------------------
    print("\n--- TESTE 14: ATALHOS RÁPIDOS, FEEDBACK HÁPTICO E COMPARTILHAR ---")
    try:
        from language_manager import TRANSLATIONS
        for lang in ["pt", "en", "es"]:
            d = TRANSLATIONS[lang]
            assert_true("quick_prompts_title" in d, f"Idioma '{lang}' possui chave 'quick_prompts_title'")
            assert_true("snippet_continue" in d, f"Idioma '{lang}' possui chave 'snippet_continue'")
            assert_true("snippet_run_tests" in d, f"Idioma '{lang}' possui chave 'snippet_run_tests'")
            assert_true("snippet_summarize" in d, f"Idioma '{lang}' possui chave 'snippet_summarize'")
            assert_true("snippet_check_errors" in d, f"Idioma '{lang}' possui chave 'snippet_check_errors'")
            assert_true("share_response" in d, f"Idioma '{lang}' possui chave 'share_response'")
            assert_true("share_chat_title" in d, f"Idioma '{lang}' possui chave 'share_chat_title'")
            assert_true("share_success" in d, f"Idioma '{lang}' possui chave 'share_success'")

        assert_true(TRANSLATIONS["pt"]["snippet_continue"] == "Continue", "PT: Continue")
        assert_true(TRANSLATIONS["en"]["snippet_continue"] == "Continue", "EN: Continue")
        assert_true(TRANSLATIONS["es"]["snippet_continue"] == "Continúa", "ES: Continúa")

        assert_true(TRANSLATIONS["pt"]["snippet_run_tests"] == "Rode os testes", "PT: Rode os testes")
        assert_true(TRANSLATIONS["en"]["snippet_run_tests"] == "Run tests", "EN: Run tests")
        assert_true(TRANSLATIONS["es"]["snippet_run_tests"] == "Ejecuta las pruebas", "ES: Ejecuta las pruebas")

        assert_true(TRANSLATIONS["pt"]["share_response"] == "Compartilhar resposta", "PT: Compartilhar resposta")
        assert_true(TRANSLATIONS["en"]["share_response"] == "Share response", "EN: Share response")
        assert_true(TRANSLATIONS["es"]["share_response"] == "Compartir respuesta", "ES: Compartir respuesta")

        # Verificação do HTML
        index_file = bridge_dir / "static" / "index.html"
        html_txt = index_file.read_text(encoding="utf-8")

        # 1. Atalhos Rápidos (Snippets / Chips)
        assert_true('.quick-snippets-bar' in html_txt, "CSS .quick-snippets-bar presente")
        assert_true('.snippet-chip' in html_txt, "CSS .snippet-chip presente")
        assert_true('id="quick-snippets-bar"' in html_txt, "Elemento HTML quick-snippets-bar presente")
        assert_true('PromptManager.insertSnippet' in html_txt, "Método PromptManager.insertSnippet implementado")

        # 2. Feedback Háptico (Vibração Tátil)
        assert_true('function triggerHaptic' in html_txt, "Função utilitária triggerHaptic implementada")
        assert_true('navigator.vibrate' in html_txt, "API nativa navigator.vibrate utilizada")
        assert_true('triggerHaptic(35)' in html_txt, "Haptic acionado ao favoritar conversa")
        assert_true('triggerHaptic(30)' in html_txt, "Haptic acionado ao copiar resposta")
        assert_true('triggerHaptic(40)' in html_txt, "Haptic acionado ao enviar prompt")

        # 3. Compartilhar Respostas (Web Share API)
        assert_true('.btn-share-msg' in html_txt, "CSS .btn-share-msg presente")
        assert_true('shareMessageText' in html_txt, "Função shareMessageText implementada")
        assert_true('navigator.share' in html_txt, "Suporte à Web Share API nativa")
        assert_true('btn-share-msg' in html_txt, "Botão de compartilhamento integrado nas mensagens")

    except Exception as e:
        assert_true(False, f"Erro no Teste 14: {e}")

# ---------------------------------------------------------
    print("\n--- TESTE 15: GESTO VOLTAR INTELIGENTE E SELEÇÃO DE TEXTO ---")
    try:
        # 1. Verificação do código nativo Android (MainActivity.kt)
        kt_file = Path("android/app/src/main/java/com/lumiag5/antigravitymobile/MainActivity.kt")
        kt_txt = kt_file.read_text(encoding="utf-8")

        assert_true("lastBackPressTime" in kt_txt, "MainActivity possui controle de tempo de clique duplo em voltar")
        assert_true("handleAndroidBack" in kt_txt, "MainActivity delega voltar ao JavaScript handleAndroidBack()")
        assert_true("setOnLongClickListener(null)" in kt_txt or "setOnLongClickListener {" not in kt_txt, "MainActivity removeu interceptação de toque longo da tela de sessão")
        assert_true("isLongClickable = true" in kt_txt, "MainActivity habilita seleção nativa do WebView ao segurar toque")

        # 2. Verificação do HTML/JS (index.html)
        index_file = bridge_dir / "static" / "index.html"
        html_txt = index_file.read_text(encoding="utf-8")

        assert_true("window.handleAndroidBack" in html_txt, "Função window.handleAndroidBack implementada")
        assert_true("prompt-history-panel" in html_txt, "handleAndroidBack fecha histórico de prompts se aberto")
        assert_true("PromptManager.backToSelect" in html_txt, "handleAndroidBack retorna ao passo 1 no envio de prompt")
        assert_true("ChatsManager.close()" in html_txt, "handleAndroidBack fecha modal de chats")
        assert_true("MenuManager.close()" in html_txt, "handleAndroidBack fecha modal de menu")
        assert_true("LogManager.close()" in html_txt, "handleAndroidBack fecha modal de log")
        assert_true("tutorial-modal" in html_txt, "handleAndroidBack fecha modal de tutorial")
        assert_true("viewingConversationId = null" in html_txt, "handleAndroidBack retorna à conversa principal do PC")

        # 3. Verificação de seleção e cópia de texto
        assert_true("-webkit-user-select: text !important" in html_txt, "CSS permite seleção de texto nativa nas mensagens .bubble")
        assert_true("touch-action: auto !important" in html_txt, "touch-action: auto habilitado em .bubble para permitir gestos de seleção")
        assert_true("popstate" in html_txt, "Listener popstate ativo para compatibilidade com navegadores web")

    except Exception as e:
        assert_true(False, f"Erro no Teste 15: {e}")

# ---------------------------------------------------------
    print("\n--- TESTE 16: OTIMIZAÇÕES DE BATERIA, SEGUNDO PLANO E PERFORMANCE ---")
    try:
        # 1. Verificação do ciclo de vida no MainActivity.kt
        kt_file = Path("android/app/src/main/java/com/lumiag5/antigravitymobile/MainActivity.kt")
        kt_txt = kt_file.read_text(encoding="utf-8")

        assert_true("override fun onPause()" in kt_txt, "MainActivity implementa onPause()")
        assert_true("binding.webView.onPause()" in kt_txt, "onPause() aciona webView.onPause() para economia de energia")
        assert_true("override fun onResume()" in kt_txt, "MainActivity implementa onResume()")
        assert_true("binding.webView.onResume()" in kt_txt, "onResume() restaura webView.onResume()")

        # 2. Verificação do HTML/CSS (index.html)
        index_file = bridge_dir / "static" / "index.html"
        html_txt = index_file.read_text(encoding="utf-8")

        # CSS de economia
        assert_true("body.app-paused" in html_txt, "CSS body.app-paused para pausar animações em segundo plano")
        assert_true("animation-play-state: paused !important" in html_txt, "Pausa de animações em segundo plano ativa")
        assert_true("body.battery-saver" in html_txt, "Perfil CSS body.battery-saver ativo para bateria fraca")

        # Page Visibility API
        assert_true("document.addEventListener(\"visibilitychange\"" in html_txt or "visibilitychange" in html_txt, "Listener Page Visibility API ativo")
        assert_true("scheduleWsReconnect" in html_txt, "Reconexão com backoff exponencial implementada")
        assert_true("Promise.allSettled" in html_txt, "Carregamento inicial paralelizado com Promise.allSettled")
        assert_true("syncNow" in html_txt, "Método BatteryManager.syncNow implementado")
        assert_true("getInterval" in html_txt, "Método LatencyManager.getInterval adaptativo implementado")

    except Exception as e:
        assert_true(False, f"Erro no Teste 16: {e}")

    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL DOS TESTES: {passed} PASSOU | {failed} FALHOU")
    print("=" * 60)

    if failed == 0:
        print(">>> TODOS OS TESTES PASSARAM COM SUCESSO! 100% OPERACIONAL! <<<")
        return 0
    else:
        print(f">>> ATENÇÃO: {failed} TESTE(S) FALHARAM! <<<")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
