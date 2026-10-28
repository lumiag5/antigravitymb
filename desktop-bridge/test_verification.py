# Copyright (c) 2026 Dev LumiaG5. All rights reserved.
# Automated Verification Suite for Antigravity Mobile v2.4.4

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
    print("INICIANDO SUITE DE TESTES COMPLETOS - ANTIGRAVITY MOBILE v2.4.4")
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
    # SUMÁRIO
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
