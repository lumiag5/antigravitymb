# ESTADO ATUAL DO PROJETO

## PROJETO
Antigravity Mobile

## OBJETIVO DO PROJETO
Desenvolver o "Antigravity Mobile", um companion para celular que atua como uma tela secundária para o Antigravity IDE no PC:
1. **Monitoramento do Chat em Tempo Real**: Acompanhar o fluxo de mensagens e conclusões do agente enquanto o desenvolvedor se afasta do PC.
2. **Alertas Sensoriais de Conclusão**: Piscar a tela do celular (flash duplo), reproduzir aviso sonoro personalizável e vibração quando a tarefa de código for finalizada.
3. **Métricas Oficiais de Quota**: Exibição em tempo real da porcentagem de uso diário (5h) e semanal do modelo de IA via RPC interna com adaptação dinâmica entre grupos de modelos.
4. **Conectividade Flexível**: Suporte à rede local (Wi-Fi) e acesso remoto global via túnel HTTPS seguro (Cloudflare) sem configuração de portas.

## FUNCIONALIDADES IMPLEMENTADAS (v2.5.1 • Build 2510)
- **Verificador e Atualizador do Local Server no Terminal**:
  - Verificação automática de atualizações do servidor do PC no GitHub logo após a seleção de idioma.
  - Tentativa dupla (2x) com recuperação inteligente se a conexão falhar, continuando a inicialização normalmente sem travar o uso offline.
  - Download do pacote do Local Server com barra de progresso visual, velocidade em MB/s e percentual (`%`) ao vivo no console.
  - Extração automática de arquivos (`.7z` e `.zip`) e substituição segura dos arquivos do servidor.
  - Análise rigorosa de arquivos: comparação de hash SHA-256 e tamanho de cada arquivo antes de aplicar; se os arquivos já forem idênticos aos remotos, o servidor dispensa reinicializações e inicia instantaneamente.
  - Persistência e blindagem de versão via `version.json` e `config.py` para impedir regressão acidental de versões.
  - Exibição destacada da versão ativa do Local Server (`v2.5.1`) no cabeçalho do terminal e aviso após atualizar solicitando reiniciar a janela.
  - Atalho sob demanda no teclado: pressione a tecla `U` a qualquer momento para buscar atualizações do Local Server.
- **Tela Cheia Imersiva (Ocultação da HUD do Celular)**:
  - No APK Android: modo imersivo sticky (`WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE`) ocultando a barra de status do topo, com suporte a entalhes de câmera (*short edges cutout*) e área de respiro dinâmica (`safe-area-inset-top`).
  - No Navegador / IP: PWA configurado com `display: fullscreen` em `manifest.json` e suporte à Fullscreen API via toque inicial ou seletor no menu de configurações.
- **Monitor de Bateria em Tempo Real**:
  - Indicador centralizado no rodapé (entre latência e Chats) exibindo estritamente a porcentagem atual da bateria e status de carregamento, sem rótulos de texto.
  - Leitura nativa via `ACTION_BATTERY_CHANGED` no APK e `navigator.getBattery` na versão web.
- **Harmonização do Rodapé**:
  - Alinhamento dos 5 elementos (`Menu`, `Latência`, `Bateria`, `Chats`, `OLED`) em linha única, com altura padronizada em `28px` e estilo *pill* arredondado.
- **Sincronização Instantânea em Tempo Real (Thinking / Pensando...)**:
  - Leitura direta dos passos de execução no banco SQLite da conversa ativa (`conversations/<conv_id>.db`). Assim que o usuário envia uma solicitação e o Antigravity PC entra no modo "Thinking...", o app mobile comuta **instantaneamente** para **"Pensando..."** com dot roxo pulsante (`#a855f7`), sem aguardar flush de logs no disco.
- **Correção da Transição para "Concluído" (*Done*)**:
  - Eliminação da dependência do `conversation_summaries.db` que mantinha o app preso em "Executando Tarefa".
  - Ao término da geração da resposta final, o status transiciona imediatamente para **"Concluído"** (*Done*), acionando o som de conclusão, flash visual e o temporizador de 1 minuto.
- **Unificação de "Background Task" com "Task Running"**:
  - Toda tarefa em segundo plano (*Background Task*, subagentes, comandos de fundo `manage_task`, `schedule`, `invoke_subagent`, `run_command` assíncronos) é mapeada rigorosamente para o mesmo status: **"Executando Tarefa..."** (*Task Running...* / *Ejecutando Tarea...*) com indicador ciano pulsante (`#0ea5e9`).
- **Critério Estrito para o Status "Concluído" (*Done*)**:
  - O status **"Concluído"** (*Done*) **SÓ É ATIVADO** quando não houver absolutamente nenhuma atividade em execução no projeto atual (`conversation_summaries.db`: `status == 'CASCADE_RUN_STATUS_IDLE'` e `not_fully_idle == 0`, ausência de tarefas em `.system_generated/tasks/` e ausência de subagentes ou etapas em andamento).
  - Enquanto qualquer tarefa em background ou processo estiver ativo no projeto atual, o status permanece em `TASK_RUNNING` ("Executando Tarefa..."). Ao término total de todas as atividades, o status transiciona para `DONE` ("Concluído") e dispara o alerta sensorial e o temporizador de 1 minuto.
- **Correção de Rolamento Vertical do Chat no APK**: Remoção do `SwipeRefreshLayout` em `activity_main.xml` e no `MainActivity.kt`, restaurando 100% a rolagem nativa de mensagens anteriores no APK Android, igual à versão por IP.
- **Navegação Multi-Conversas com Botão "Chats"**:
  - Botão `💬 Chats` no centro inferior do rodapé (entre Menu/Latência e o botão OLED).
  - Modal com listagem de conversas e projetos sincronizados do Antigravity PC com leitura de transcripts em background.
  - Correção definitiva do carregamento remoto e eliminação do toast indevido de erro ao abrir conversas (`updateProjectName`).
  - Indicadores pulsantes estritos na frente de cada conversa: **somente dot laranja (`🟠`)** se o Antigravity estiver processando algo, ou **somente dot verde (`🟢`)** se estiver ocioso, sem textos frontais.
  - Carregamento de histórico completo com liberdade remota pelo smartphone sem alterar nem clicar na conversa aberta no PC.
- **Status de Tarefa, Unificação e Temporizador de Conclusão**:
  - Unificação de **"Thought"** e **"Thinking"** mapeados para o mesmo estado: **"Pensando..."** (*Thinking...*) com dot roxo pulsante (`#a855f7`).
  - Remoção dos estados "Analyzed" e "Ran" a pedido do usuário, mantendo os estados principais: "Pensando...", "Trabalhando...", "Executando Tarefa..." e "Concluído" (por 1 minuto).
  - Renomeação de "Processando" para **"Trabalhando..."** (*Working*).
  - Adição do status **"Executando Tarefa..."** (*Task Running*) com indicador visual ciano pulsante (`#0ea5e9`).
  - O status **"Concluído"** (*Done*) permanece ativo por **1 minuto** (ou até iniciar nova atividade) antes de transicionar para "Conectado".
  - Paridade total e traduções em PT-BR, EN e ES para ambas as versões (APK e IP/Web).
- **Remoção Global do Ícone "✕" de Fechar**:
  - Eliminação do "✕" em todos os modais (Tutorial, Menu, Log, Chats). Todos os modais se auto-fecham ao tocar no fundo externo (backdrop click) ou via botão "Fechar" limpo no rodapé.
- **Diferenciação de Versão no Badge (APK vs IP)**:
  - O cabeçalho identifica automaticamente se está executando no APK Android (`vX.X.X (APK) • Dev LumiaG5`) ou via navegador IP (`v2.4.3 (IP) • Dev LumiaG5`).
- **Atualização Automática no Menu (Exclusiva para Android APK)**:
  * Seção no modal `⚙️ Menu` exibida apenas no APK nativo para checagem com 1 clique de novas releases no GitHub, download em background e instalação automática via `FileProvider`.
- **Auditoria de Segurança**:
  * Confirmação de ausência de chaves, tokens GitHub ou credenciais vazadas.
  * Proteção e sanitização contra *Path Traversal* adicionada no endpoint de mensagens.

- **Desktop Bridge Daemon (PC)** (`antrigavitymb/desktop-bridge/`):
  - **QR Code no Terminal**: Renderização de QR Code em ASCII compacto diretamente no console do PC para conexão instantânea pela câmera do celular.
  - **Detecção Dinâmica de Modelos de IA**: Detecção em tempo real de comutação entre modelos Gemini, Claude Sonnet e GPT durante a própria conversa via decodificação de tags Protobuf específicas (campo 28 `\xe2\x01` para Claude/GPT e campo 19 `\x9a\x01` para Gemini).
  - **Sincronização Dinâmica de Cotas**: Comutação automática das métricas de cota entre `Gemini Models` e `Claude and GPT models` na API interna RPC (`LanguageServerService/RetrieveUserQuotaSummary`).
  - **Monitoramento em Segundo Plano (*Background Task Guard*)**: Vigia tarefas em andamento mesmo com troca de conversa no PC.
  - **Engine Assíncrona com *Tail-Seek***: Leitura rápida dos últimos bytes de logs (`transcript.jsonl` de 40+ MB).
  - **Segurança com Autenticação por PIN Dinâmico**: PIN aleatório de 4 dígitos com cache de autorização por 24 horas no navegador.
  - **Servidor FastAPI**: WebSockets com ping de latência (`/ws`) e REST (`/api/status`, `/api/messages`, `/api/quota`, `/api/auth/*`).
  - **Túnel HTTPS Automático**: Integração nativa com Cloudflare Quick Tunnel com suporte global para dados móveis (3G/4G/5G).
  - **Internacionalização Tríplice**: Suporte completo a Português, Inglês e Espanhol com troca a quente via tecla `L`.

- **Web Companion Mobile (HTML5 / PWA)** (`antrigavitymb/desktop-bridge/static/`):
  - **Manifest PWA Oficial**: `manifest.json` com ícones, tema preto OLED `#000000` e exibição standalone.
  - **Menu de Configurações Unificado**: Botão `⚙️ Menu` no rodapé (substituindo a antiga posição de "Som & Flash") reunindo todas as preferências.
  - **Seletor de Toques Sonoros**: 4 toques sintetizados via Web Audio API (*Chime Moderno*, *Sino Zen*, *Pulso Sci-Fi*, *Bip Clássico*) com botão de teste imediato.
  - **Controle de Volume**: Slider de ganho master (0% a 100%) salvo no armazenamento local.
  - **Medidor de Latência em Tempo Real (Ping)**: Badge ao lado direito do botão Menu com indicador colorido pulsante (Verde <130ms, Amarelo 130-320ms, Vermelho >320ms) e opção de ocultação/exibição.
  - **Histórico de Conclusões (Log)**: Janela de log com registro das tarefas finalizadas, projeto, título, modelo e horário.
  - **Posicionamento do Botão OLED**: Botão `🌓 OLED` reposicionado no canto direito do rodapé (onde ficava Notificações).
  - **Notificações Push com Tela Bloqueada**: Web Notifications nativas suportadas via HTTPS.

- **Aplicativo Android Nativo (APK Wrapper)** (`android/`):
  - **Projeto Gradle/Kotlin**: Estrutura nativa com pacote `com.lumiag5.antigravitymobile`.
  - **WebView Otimizado**: Aceleração de hardware, `domStorage` para persistência de tokens e preferências, e suporte a WebSockets/Web Audio.
  - **Gerenciador de Conexão com Servidor**: Tela de configuração de URL no primeiro acesso (suportando Wi-Fi local ou Cloudflare HTTPS) e atalho de toque longo para troca de endereço.
  - **Suporte a Notificações Nativas**: Solicitação automática da permissão `POST_NOTIFICATIONS` no Android 13+.
  - **Pipeline de CI/CD (GitHub Actions)** (`.github/workflows/build-apk.yml`): Compilação automatizada do APK na nuvem a cada push ou tag de versão, anexando o instalador `.apk` diretamente aos artefatos e lançamentos do GitHub sem exigir ambiente pesado no PC local.

## DOCUMENTAÇÃO OFICIAL PARA GITHUB
- **README**:
  - `README.md`, `README.en.md`, `README.es.md` (Markdown trilíngue atualizado com v2.4.2, badges e instruções completas de APK e PWA).
- **CHANGELOG**:
  - `android/CHANGELOG.md` (Histórico de alterações exclusivo do aplicativo nativo Android APK).
  - `CHANGELOG.md`, `CHANGELOG.en.md`, `CHANGELOG.es.md` (Changelog geral do ecossistema cobrindo v2.3.5 a v2.4.2).
- **LICENÇA & TUTORIAL**:
  - `LICENSE` (Licença MIT oficial - Copyright © 2026 Dev LumiaG5).
  - `TUTORIAL.txt` (Guia passo a passo de conexão em pt, en, es).

## ÚLTIMA ALTERAÇÃO
- **Compatibilidade Antigravity 2.34+ (Hydrogen), Prompt, Fix Dot Laranja, QR Único e Visual Orgânico (v2.5.2 • Build 2520)**:
  - Corrigida detecção de modelo para identificar `Gemini 4 Hydrogen` (`MODEL_PLACEHOLDER_M525`..`M528`) corretamente em vez de Argon.
  - Descoberta da API local atualizada em `antigravity_api.py` lendo `daemon/hub_*.json` (`httpsPort`/`httpPort` + `csrfToken`) e enviando `cascade_config.planner_config.plan_model` no `SendUserCascadeMessage`.
  - Novo endpoint `GET /api/models` sincronizando os modelos ativos do `GetUserStatus` no app.
  - Corrigido bug do ponto laranja em conversas antigas/paradas usando `GetAllCascadeTrajectories` e verificação temporal em `detect_live_cascade_status`.
  - Removido o segundo QR Code e túnel Cloudflare de emergência na inicialização do terminal em `run.py`, mantendo apenas o QR Code Wi-Fi principal.
  - Interface web e tela inicial Android simplificadas com ícones SVG limpos, menos emojis e textos naturais/orgânicos.

- **Verificador e Atualizador Automático do Local Server no Terminal (v2.5.1 • Build 2510)**:
  - Verificação automática de atualizações do Local Server diretamente no terminal do computador logo após a seleção/carregamento do idioma.
  - Resiliência de conexão: 2 tentativas automáticas com intervalo de espera caso a primeira tentativa falhe (offline ou erro temporário de rede), prosseguindo sem bloquear a inicialização.
  - Filtro dedicado para arquivos do Local Server (`.7z` ou `.zip`), ignorando os instaladores do APK Android.
  - Barra de progresso gráfica ao vivo no terminal com indicador em percentual (`%`), download em megabytes e velocidade de transferência (`MB/s`).
  - Análise rigorosa por SHA-256 e tamanho de arquivo: se todos os arquivos já forem idênticos aos remotos, o servidor dispensa re-downloads e reinicializações, iniciando de imediato.
  - Persistência e blindagem de versão via `version.json` e `config.py` para impedir downloads em loop.
  - Exibição destacada da versão do Local Server no banner do terminal.
  - Mensagem clara orientando o fechamento e reabertura do terminal após a atualização.
  - Atalho manual no terminal (`Tecla U`) para verificar atualizações sob demanda enquanto o servidor estiver rodando.
  - Suporte completo trilíngue (PT, EN, ES) com textos orgânicos e naturais.
  - Suite de testes expandida para 382 testes automatizados 100% aprovados.

- **Envio Remoto de Prompts, Gestos de Navegação, Seleção de Texto e Otimizações de Bateria (v2.5.0 • Build 2500)**:
  - Envio remoto de prompts do celular para o PC com seleção dinâmica de modelo de IA (Gemini, Claude, GPT).
  - Atalhos rápidos (snippets) para inserção de comandos frequentes com um toque e feedback háptico (vibração tátil).
  - Histórico de prompts enviados com navegação por tecla de seta para cima e contador dinâmico de palavras/caracteres.
  - Botão/gesto voltar inteligente no Android com fechamento em pilha de modais e proteção contra encerramento acidental.
  - Seleção nativa de texto em mensagens com barra de opções do Android para copiar trechos para o clipboard.
  - Ações rápidas nas respostas da IA: cópia rápida com feedback visual e compartilhamento nativo via Web Share API.
  - Indicador dinâmico de pensamento com animação de pontos saltitantes e fixação de conversas favoritas (⭐).
  - Economia de bateria: hooks de ciclo de vida (`onPause`/`onResume`) no WebView, suspensão de animações de GPU e timers via Page Visibility API, reconexão WebSocket com backoff exponencial e perfil automático de bateria fraca.

- **Tela Cheia Imersiva, Monitor de Bateria e Harmonização do Rodapé (v2.4.4 • Build 2426)**:
  - Ocultação da barra de status no APK e suporte a tela cheia no navegador.
  - Indicador de porcentagem de bateria em tempo real centralizado no rodapé.
  - Alinhamento simétrico e padronização visual dos componentes inferiores.

- **Gerenciamento de Sessão com Logout ao Fechar, Leitura de QR Code via Câmera e Layout Minimalista (v2.4.2 • Build 2420)**:
  - O app agora sempre inicia na tela de sessão ao ser aberto, deslogando a visualização direta por segurança.
  - Adicionada opção **"Voltar à Sessão"**: se o servidor no PC continuar aberto, reconecta imediatamente sem pedir novo PIN.
  - Adicionada opção **"Entrar com QR Code"**: ativa a câmera do celular/emulador para escanear o QR Code gerado no terminal do PC via biblioteca ZXing.
  - O QR Code do console agora transporta o PIN dinâmico (`?pin=XXXX`), permitindo login 100% automático e instantâneo ao escanear com a câmera.
  - Adicionada opção **"Nova Sessão"**: limpa a autenticação anterior e permite inserir novo PIN ou trocar de servidor.
  - Adicionado botão **"Sair / Desconectar da Sessão"** dentro do modal de Configurações (`⚙️ Menu`).
  - Removidos todos os atalhos rápidos antigos de emulador/rede, deixando a tela minimalista e focada em OLED Black.

## ESTADO ATUAL
- Versão v2.5.2 (Build 2520) compatível com Antigravity 2.34+ (Gemini 4 Hydrogen), envio de prompts via daemon JSON, QR Code único, visual orgânico e 396 testes automatizados aprovados.
