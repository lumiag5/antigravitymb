# Changelog &bull; Antigravity Mobile APK (Android Nativo)

<p align="center">
  <b>Português</b> &bull; <a href="CHANGELOG.en.md">English</a> &bull; <a href="CHANGELOG.es.md">Español</a>
</p>

Todas as alterações, correções e novos recursos dedicados exclusivamente ao aplicativo nativo Android (**Antigravity Mobile APK**) estão documentados neste arquivo.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e as convenções do [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### ⚡ Sincronização em Tempo Real (Thinking) & Transição Concluído (Done)
* **Correção da Transição para "Done" (Concluído)**:
  * Eliminada a trava que mantinha o app preso em *"Executando Tarefa"* mesmo após os resultados terem sido apresentados no PC.
  * O monitor agora reconhece a resposta final do modelo imediatamente, transicionando o status com precisão para **"Concluído"** (*Done*), disparando o alerta sonoro suave, o flash de tela e o temporizador de 1 minuto.
* **Detecção Instantânea do Status "Pensando..." (*Thinking*)**:
  * Implementada leitura direta e em tempo real dos passos de execução no banco SQLite da conversa ativa (`conversations/<conv_id>.db`).
  * Assim que o usuário envia uma solicitação e o Antigravity PC entra em modo **"Thinking..."**, o aplicativo mobile comuta **instantaneamente** para **"Pensando..."** (*Thought* / *Thinking* com dot roxo pulsante `#a855f7`), eliminando a espera pelo término do raciocínio e sincronizando perfeitamente ambas as telas.

### ⚙️ Unificação de Background Task & Critério Rigoroso de Conclusão (Done)
* **Unificação de "Background Task" com "Task Running"**:
  * Tarefas em segundo plano do Antigravity PC (*Background Task*, subagentes `invoke_subagent`, temporizadores `schedule`, comandos `manage_task` e tarefas assíncronas de shell) foram unificadas exatamente sob o mesmo status visual e sonoro de **"Executando Tarefa..."** (*Task Running...* / *Ejecutando Tarea...*).
  * Indicador visual: ponto pulsante ciano elétrico (`#0ea5e9`).
* **Critério Estrito para o Status "Concluído" (*Done*)**:
  * O status **"Concluído"** (*Done*) agora **SÓ É DECLARADO** quando não houver absolutamente nenhuma atividade em execução no projeto atual (`conversation_summaries.db`: `status == 'CASCADE_RUN_STATUS_IDLE'` e `not_fully_idle == 0`, ausência de logs ativos em `.system_generated/tasks/` e nenhum subagente em andamento).
  * Enquanto houver qualquer tarefa em background ativa no projeto atual, o status permanece em `TASK_RUNNING` ("Executando Tarefa..."). Ao término total de todas as atividades, o status transiciona para `DONE` ("Concluído"), disparando o alerta sonoro e iniciando o temporizador de 1 minuto.

### 🐛 Correções de Rolamento & Gestos
* **Correção Definitiva do Scroll do Chat no APK**:
  * Remoção completa do wrapper `SwipeRefreshLayout` no layout nativo (`activity_main.xml`) e de seus ouvintes no `MainActivity.kt`.
  * Como a página web possui altura fixa (100vh) com rolagem interna em `#chat-feed`, o `SwipeRefreshLayout` interceptava indevidamente todos os gestos de arrasto para baixo (`canScrollVertically(-1) == false`), travando o rolamento e impedindo o usuário de ver mensagens anteriores no APK.
  * O `WebView` agora opera diretamente dentro do `FrameLayout` com `isVerticalScrollBarEnabled = true` e `OVER_SCROLL_IF_CONTENT_SCROLLS`, restaurando rolagem nativa 100% fluida para todo o histórico de mensagens anteriores.
  * Desativação de cache do WebView (`LOAD_NO_CACHE`) para garantir que novas telas e scripts sejam carregados imediatamente.

### 💬 Navegação de Chats & Correção do Toast de Histórico
* **Correção do Aviso Indevido de Erro ao Abrir Histórico**:
  * Corrigida a chamada de atualização do título do projeto ativo na barra superior (`updateProjectName`), eliminando o erro de referência de script que disparava o toast indevido *"Falha ao abrir histórico da conversa"* mesmo quando as mensagens já haviam sido carregadas com sucesso na tela.
* **Botão "Chats" Central no Rodapé**:
  * Novo botão `💬 Chats` posicionado no centro inferior da tela (entre Menu/Latência e o botão OLED).
  * Abertura instantânea de modal responsivo listando todas as conversas e projetos recentes do PC.
* **Correção do "Erro ao carregar conversas do pc"**:
  * Adicionado fallback com varredura direta dos subdiretórios em `brain/`, garantindo que a lista de projetos e conversas nunca falhe mesmo se o banco SQLite de resumos estiver bloqueado ou inacessível.
* **Indicadores Pulsantes Exclusivos (Sem Texto Frontal)**:
  * Conversas ativas/processando: exibem estritamente um ponto pulsante laranja (`🟠`).
  * Conversas ociosas: exibem estritamente um ponto pulsante verde (`🟢`).
  * Conforme especificação, sem nenhuma mensagem ou texto posicionado na frente do ponto indicador.
* **Inspeção de Histórico Remota e Independente**:
  * Ao tocar em qualquer projeto/chat, o app puxa todo o histórico de conversas do PC sem simular cliques de mouse ou trocar a conversa ativa na tela do computador.

### 🔄 Estados de Execução & Unificação
* **Status "Pensando..." (Unificação de "Thought" e "Thinking")**:
  * Correção e unificação dos estados "Thought" e "Thinking", mapeados exatamente para "Pensando..." (PT-BR) / "Thinking..." (EN) / "Pensando..." (ES) com indicador roxo pulsante (`#a855f7`).
* **Ajuste de Estados Solicitado**:
  * Estados intermediários "Analyzed" e "Ran" removidos conforme solicitado pelo usuário, consolidando a execução nas fases principais: "Pensando...", "Trabalhando...", "Executando Tarefa..." e "Concluído" (por 1 minuto).
* **Status Existentes Preservados**:
  * "Processando" renomeado para "Trabalhando...".
  * "Executando Tarefa..." (*Task Running*) com indicador ciano elétrico pulsante.
  * "Concluído" permanece exibido por 1 minuto ao finalizar uma tarefa antes de retornar para "Conectado".

### 🧹 Remoção de Ícones "✕" & Fechamento por Toque Externo
* **Remoção Global do "✕" de Fechar**:
  * Ícone "✕" removido de todos os modais da interface (Tutorial, Menu de Configurações, Histórico de Conclusões e Modal de Chats).
  * Todos os modais fecham automaticamente ao tocar na área externa/fundo (backdrop click) ou através de um botão limpo "Fechar" posicionado na base inferior.

### 📱 Diferenciação de Versão & Atualizador Automático
* **Badge de Versão Dinâmico no Cabeçalho**:
  * Identificação automática do ambiente de execução: o APK detecta a versão do binário nativo instalado no aparelho e exibe `vX.X.X (APK) • Dev LumiaG5`, corrigindo a discrepância onde exibia versões legadas da web. Na versão acessada por IP, o badge exibe `v2.4.3 (IP) • Dev LumiaG5`.
* **Atualização Automática do APK Integrada ao Menu**:
  * Nova seção exclusiva para o APK dentro do modal `⚙️ Menu`.
  * Consulta automática de novas releases no GitHub com comparação semântica de versão (SemVer).
  * Download em segundo plano do instalador `.apk` e acionamento automático do instalador do Android via `FileProvider` seguro (`ACTION_VIEW`).
* **Auditoria de Segurança**:
  * Varredura completa confirmando ausência de chaves de API, PATs do GitHub ou dados sensíveis no código e no histórico do Git.
  * Sanitização de parâmetros contra *Path Traversal* adicionada no servidor.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### 🚀 Novos Recursos & Segurança de Sessão
* **Logout Automático ao Fechar o App**:
  * Ao fechar o aplicativo no celular/emulador e abri-lo novamente, o app sempre inicia na tela de **Gerenciador de Sessão**, evitando exibição de dados ou sessões desprotegidas.
  * O botão nativo "Voltar" do Android enquanto o usuário estiver dentro do chat agora também desloga com segurança para a tela de sessão.
  * Adicionado atalho direto **`🚪 Sair / Desconectar da Sessão`** dentro do menu `⚙️ Menu` do companion.

* **Opção "▶ Voltar à Sessão" (Sem Novo PIN)**:
  * Se o servidor já estava configurado e continua rodando no PC, um cartão com indicador verde exibe o endereço do servidor e o botão **"Voltar à Sessão"**.
  * Clicando nele, o app aproveita o cache de autorização e reconecta imediatamente sem precisar digitar o PIN novamente, respeitando a janela segura de 24 horas.

* **Opção "📷 Entrar com QR Code" via Câmera Nativa (ZXing)**:
  * Integração com a biblioteca de visão computacional ZXing Android Embedded.
  * Solicitação nativa da permissão `android.permission.CAMERA` em tempo de execução.
  * O terminal do PC agora gera o QR Code com o PIN embutido (`?pin=XXXX`). Ao apontar a câmera do celular/emulador para o terminal do PC, o app faz a leitura e a autenticação de forma 100% instantânea, sem necessidade de tocar no teclado.

* **Opção "⚡ Nova Sessão"**:
  * Permite iniciar uma nova sessão do zero, limpando os tokens antigos em cache no WebView e permitindo digitar um novo PIN ou conectar a um novo servidor.

* **Interface Limpa OLED True Black**:
  * Remoção completa de todos os botões de atalhos rápidos antigos de emulador/rede, deixando o visual minimalista, moderno e com economia máxima de bateria em telas AMOLED/OLED (`#000000`).

---

## [2.4.1] - 2026-10-25 (Build 2419)

### 🐛 Correções de Conexão & Rede
* **Dedução Inteligente de Protocolo (HTTP vs HTTPS)**:
  * Correção do erro em que links com IP local (ex: `192.168.0.6:8765` ou `10.0.2.2:8765`) eram forçados para `https://`, gerando falha de handshake TLS no servidor Python/Uvicorn (`WARNING: Invalid HTTP request received`) e travamento em tela preta.
  * O aplicativo agora detecta automaticamente IPs locais (`192.168.x.x`, `10.x.x.x`, `172.x.x.x`, `127.0.0.1`, `localhost` e `:8765`) e aplica estritamente `http://`, reservando `https://` para túneis Cloudflare e domínios web.

* **Auto-completar de Porta Padrão**:
  * Se o usuário digitar um IP local sem porta (ex: `192.168.0.6`), a porta `:8765` é anexada automaticamente.

* **Diagnóstico Detalhado de Erros**:
  * A tela de desconexão agora exibe a URL exata tentada e o código/motivo retornado pelo WebView, além dos botões para "Tentar Novamente" e "Trocar Servidor".

* **Compatibilidade Retroativa de WebView**:
  * Tratamento de erro duplo (`WebResourceRequest` moderno e legado `onReceivedError(int, String, String)`) para garantir estabilidade e exibição de erros mesmo em emuladores rodando Android 7 ou 9 (como LDPlayer).

---

## [2.4.0] - 2026-10-25 (Build 2418)

### 📱 Lançamento Inicial do Wrapper Nativo
* **Estrutura Nativa Kotlin / Gradle**:
  * Pacote oficial `com.lumiag5.antigravitymobile`.
  * `minSdk = 24` (Android 7.0+) e `targetSdk = 34` (Android 14).
* **WebView Otimizado**:
  * Aceleração por hardware, suporte a WebSockets (`/ws`), Web Audio API e `domStorage` para armazenamento persistente de preferências.
  * Cores de sistema em OLED True Black (`#000000`) na barra de status e navegação via `WindowCompat`.
* **Permissões de Sistema**:
  * Suporte nativo a notificações push em segundo plano (`POST_NOTIFICATIONS` no Android 13+).
  * Habilitação de tráfego limpo (`usesCleartextTraffic="true"`) para suporte a conexões HTTP locais via Wi-Fi.
* **Pipeline de CI/CD (GitHub Actions)**:
  * Fluxo automatizado `.github/workflows/build-apk.yml` compilando releases e debugs automaticamente na nuvem a cada push de tag ou commit no repositório.
