# Changelog

<p align="center">
  <b>Português</b> &bull; <a href="CHANGELOG.en.md">English</a> &bull; <a href="CHANGELOG.es.md">Español</a>
</p>

Todas as alterações notáveis do **Antigravity Mobile** serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este projeto segue o [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### ⚡ Sincronização em Tempo Real (Thinking) & Transição Concluído (Done)
* **Correção da Transição para "Done" (Concluído)**: Corrigido o problema onde o app mobile permanecia com o status "Executando Tarefa" mesmo após a conclusão das tarefas e testes no PC. O status agora transiciona perfeitamente para **"Concluído"** (*Done*) ao finalizar a resposta.
* **Detecção em Tempo Real do Status "Pensando..." (*Thinking*)**: Através de leitura direta dos passos no SQLite da conversa ativa (`conversations/<conv_id>.db`), o aplicativo mobile comuta **instantaneamente** para **"Pensando..."** assim que o Antigravity PC entra no modo "Thinking...", eliminando atrasos de sincronização.

### ⚙️ Unificação de Background Task & Conclusão Estrita
* **Unificação de "Background Task" com "Task Running"**: O status "Background Task" do Antigravity PC (tarefas de segundo plano, temporizadores `schedule`, comandos `manage_task`, subagentes `invoke_subagent` e tarefas assíncronas de terminal) foi unificado rigorosamente como o mesmo status de **"Executando Tarefa..."** (*Task Running...* / *Ejecutando Tarea...*) com dot ciano pulsante (`#0ea5e9`).
* **Critério Estrito para o Status "Concluído" (*Done*)**: O status "Done" (*Concluído*) **só é declarado quando não houver atividade alguma em execução no projeto atual** (verificação rigorosa de `status == 'CASCADE_RUN_STATUS_IDLE'`, `not_fully_idle == 0`, ausência de tarefas ativas em `.system_generated/tasks/` e subagentes concluídos). Enquanto houver tarefas em execução, o status permanece em `TASK_RUNNING` ("Executando Tarefa...").

### 🐛 Corrigido
* **Aviso de Erro ao Abrir Histórico no Chats**: Corrigida a chamada da função de atualização do cabeçalho de projetos (`updateProjectName`), eliminando o erro de script que disparava indevidamente o alerta *"Falha ao abrir histórico da conversa"* no topo da tela quando o histórico era carregado.
* **Rolamento Vertical de Mensagens no APK**: Resolvido o problema em que o usuário não conseguia rolar o chat para cima no APK para ver o histórico anterior. O `SwipeRefreshLayout` foi removido do layout nativo Android para que o `WebView` receba todos os toques sem captura indevida de gestos, garantindo paridade total com a versão web por IP.
* **Carregamento de Conversas no Botão "Chats"**: Resolvido o erro *"Erro ao carregar conversas do pc"* com a implementação de fallback robusto varrendo diretamente a pasta `brain/` e garantindo envio transparente do token de autenticação em cache.
* **Remoção Global do Ícone "✕" de Fechar**: O botão "✕" foi retirado de todos os modais (Tutorial, Menu, Log e Chats). Todos os modais se auto-fecham ao clicar fora da janela (backdrop click) ou através de um botão "Fechar" limpo no rodapé.
* **Unificação dos Estados "Thought" e "Thinking"**: Ambos os estados agora convergem para **"Pensando..."** com indicador roxo pulsante (`#a855f7`).

### 🚀 Adicionado
* **Botão "Chats" Central no Rodapé**:
  * Localizado no centro inferior da tela (entre o menu/latência à esquerda e o botão OLED à direita).
  * Abre modal de seleção de conversas e projetos sincronizados do Antigravity PC em ambas as versões (APK e IP/Web).
* **Indicadores Pulsantes Estritos por Conversa**:
  * Se o Antigravity estiver processando algo naquela conversa: exibe **apenas um ponto pulsante laranja (`🟠`)**, sem nenhum texto ou mensagem na frente.
  * Se estiver ocioso/não processando: exibe **apenas um ponto pulsante verde (`🟢`)**, sem nenhum texto ou mensagem na frente.
* **Leitura Remota Totalmente Independente**:
  * Ao selecionar qualquer chat/projeto na lista pelo celular, o app busca e renderiza o histórico completo diretamente do transcript sem alterar a janela ou conversa aberta no PC e sem simular cliques remotos de mouse.
  * Banner com botão "Voltar ao PC ao Vivo" para alternar rapidamente de volta à sincronização em tempo real.
* **Status "Trabalhando...", "Pensando..." e "Executando Tarefa..."**:
  * Status "Processando" renomeado para **"Trabalhando..."** (*Working*).
  * Status **"Pensando..."** (*Thought* / *Thinking*).
  * Novo status **"Executando Tarefa..."** (*Task Running*) com indicador visual ciano pulsante (`#0ea5e9`).
  * Ao concluir tarefas, o status **"Concluído"** é ativado e permanece exibido por **1 minuto** (ou até que uma nova atividade comece), retornando para "Conectado" após o término do tempo.
* **Diferenciação Visual de Versão (APK vs IP)**:
  * O cabeçalho agora diferencia a versão do APK instalado no dispositivo (`vX.X.X (APK) • Dev LumiaG5`) e a versão companion por IP (`v2.4.3 (IP) • Dev LumiaG5`), eliminando confusões visuais de cache.
* **Atualização Automática do APK no Menu (Exclusiva para Android)**:
  * Adicionada seção dedicada no menu `⚙️ Menu` do APK para verificação e download em 1 toque de novas versões diretamente do GitHub Releases, abrindo o instalador nativo do sistema via `FileProvider`.
* **Auditoria Completa de Segurança**:
  * Varredura do histórico Git e repositório confirmando ausência total de tokens, senhas ou dados sensíveis.
  * Sanitização de entradas contra *Path Traversal* adicionada no servidor.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Adicionado / Melhorias de Sessão e Câmera
* **Gerenciamento de Sessão com Desconexão ao Fechar**: O app agora sempre inicia na tela de sessão ao ser aberto, pausando o feed ativo para segurança.
* **Opção "Voltar à Sessão"**: Se o servidor já foi configurado e continua ativo no computador, um único toque reconecta ao dashboard em tempo real sem solicitar um novo PIN.
* **Opção "Entrar com QR Code" via Câmera Nativa**: Integração com scanner nativo de câmera (ZXing) com permissão em tempo de execução para ler o QR Code diretamente do terminal do PC.
* **Autenticação Automática via QR Code**: O terminal agora embuti o PIN dinâmico no QR Code (`?pin=XXXX`), permitindo conexão e autorização instantânea com um simples escaneamento de câmera.
* **Opção "Nova Sessão"**: Limpa o token anterior e abre a interface para digitar o novo PIN ou trocar de servidor.
* **Botão "Sair da Sessão" no Menu**: Adicionado atalho no menu `⚙️ Menu` para desconectar imediatamente e retornar à tela inicial.
* **Interface Limpa OLED**: Remoção de todos os atalhos rápidos antigos de emulador/rede, deixando o visual minimalista em OLED Black `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Corrigido / Aplicativo Android Nativo
* **Dedução Inteligente de Protocolo (HTTP vs HTTPS)**: Correção do problema em que conexões por IP local (ex: `192.168.0.6:8765` ou `10.0.2.2:8765`) eram forçadas para `https://`, causando erro de handshake TLS (`Invalid HTTP request received`) e travamento na tela preta. Agora o app detecta automaticamente redes locais e utiliza `http://`, reservando `https://` para túneis Cloudflare e domínios públicos.
* **Auto-completar de Porta Padrão**: Se um IP local for digitado sem porta (ex: `192.168.0.6`), a porta `:8765` é anexada automaticamente.
* **Atalhos Rápidos na Tela de Conexão**: Adicionados 3 botões de preenchimento rápido em um toque:
  - `💻 Emulador (LDPlayer / Nox)`: Insere `http://10.0.2.2:8765` (loopback padrão de emuladores para o PC hospedeiro).
  - `📶 Wi-Fi Local (PC)`: Insere `http://192.168.0.6:8765`.
  - `🌐 Túnel Cloudflare`: Preenche `https://` para entrada rápida do link público.
* **Botão "Colar Link" da Área de Transferência**: Atalho dedicado para colar a URL diretamente do clipboard do celular ou emulador com um único clique.
* **Diagnóstico Detalhado de Erros**: A tela de erro agora exibe a URL exata que falhou e o código/motivo retornado pelo WebView, além de manter os botões "Tentar Novamente" e "Trocar Servidor".
* **Compatibilidade Retroativa de WebView**: Implementado tratamento de erro duplo (`WebResourceRequest` moderno e legado `onReceivedError(int, String, String)`) para garantir exibição correta de status em emuladores e aparelhos com versões anteriores do Android (Android 7 a 9).

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Adicionado / Melhorias de Interface
* **QR Code no Terminal do PC**: Exibição automática de um QR Code em ASCII compacto no console do Desktop Bridge para pareamento instantâneo via câmera do celular, eliminando a digitação manual de URLs.
* **Menu de Configurações Unificado**: Novo botão `⚙️ Menu` posicionado no rodapé (no lugar de Som & Flash), reunindo todas as preferências de alertas, áudio, rede e histórico.
* **Seletor de Toques Sonoros Personalizáveis**: Escolha entre 4 assinaturas sonoras sintetizadas em tempo real via Web Audio API (*Chime Moderno*, *Sino Zen*, *Pulso Sci-Fi* e *Bip Clássico*) com botão para teste imediato.
* **Controle Deslizante de Volume**: Slider de ganho com porcentagem de volume ajustável (0% a 100%) salvo no armazenamento do navegador.
* **Indicador de Latência em Tempo Real (Ping)**: Badge ao lado direito do botão Menu com indicador visual dinâmico (Verde <130ms, Amarelo 130-320ms, Vermelho >320ms) e opção no menu para exibir ou ocultar.
* **Histórico de Conclusões de Tarefas (Log)**: Janela retrátil de log que grava as últimas tarefas finalizadas com projeto, título, modelo de IA e horário exato de término, com botão de limpeza.
* **Reposicionamento do Botão OLED**: O botão `🌓 OLED` agora ocupa a posição de Notificações no rodapé, deixando a interface limpa e simétrica.

---

## [2.3.6] - 2026-10-25 (Build 2417)

### Adicionado / Corrigido
* **Detecção em Tempo Real de Modelos de IA (Claude, GPT, Gemini)**: O daemon agora identifica instantaneamente quando o desenvolvedor altera o modelo de IA no Antigravity IDE (ex.: alternando entre Gemini e Claude Sonnet) durante a própria conversa, sem necessidade de reiniciar o servidor ou recarregar a tela.
* **Decodificação Protobuf Específica**: Adicionado suporte à leitura do campo binário 28 (`\xe2\x01`) do Antigravity para modelos Claude e GPT, priorizando a extração do modelo ativo e eliminando falsos positivos com nomes de modelos contidos em prompts de sistema legados.
* **Sincronização Dinâmica dos Grupos de Quota RPC**: O cálculo das barras de uso diário (5 Horas) e semanal comuta automaticamente entre os grupos de cota `Gemini Models` e `Claude and GPT models` conforme a família do modelo em execução no instante exato.
* **Novo Evento WebSocket `model_changed`**: Notificação push instantânea para a interface mobile com o nome do novo modelo e os dados recalculados de quota.
* **Propagação de Modelo em Todos os Eventos de Mensagem**: Todas as mensagens de usuário, conclusões e atualizações de status agora transportam o `active_model` ativo para consistência de interface.
* **Conexão SQLite Somente Leitura (`mode=ro`)**: Conexão com os bancos de resumo aberta com URI de leitura sem bloqueio, prevenindo contenção de locks de WAL enquanto o IDE grava informações.

---

## [2.3.5] - 2026-10-25 (Build 2416)

### Lançamento Inicial (Primeira Versão Pública no GitHub)

Primeira versão pública oficial do **Antigravity Mobile** para monitoramento remoto do Antigravity IDE em tempo real pelo celular.

#### Chat & Interface Mobile
* **Feed em Tempo Real Limpo**: Filtragem estrita de ruídos, logs de terminal e execuções intermediárias de ferramentas. Exibe exclusivamente o prompt do usuário e a conclusão final do assistente de IA.
* **Renderizador Markdown & Código**: Suporte a blocos de código com destaque visual, tabelas e listas com tipografia idêntica à do PC (Inter e JetBrains Mono).
* **Auto-Scroll Inteligente**: Acompanhamento automático das novas mensagens, pausando a rolagem caso o usuário suba a tela para ler o histórico anterior.
* **Modo OLED Black Puro**: Fundo `#000000` para economia de bateria em telas AMOLED/OLED e balão do usuário ajustado para cinza escuro de alto contraste.
* **Layout Anti-Corte**: Interface responsiva adaptada para safe areas de celulares (evita sobreposição com barras de navegação do Android e iOS).

#### Sincronização & Inteligência de Sessão
* **Detecção Multi-Fonte de Foco**: Monitoramento em tempo real de conversas ativas através da agregação de locks de presença (`presence/*.lock`), anotações protobuf (`annotations/*.pbtxt`) e banco SQLite (`conversation_summaries.db`).
* **Identificação de Workspace & Conversa**: Cabeçalho móvel com badge legível exibindo o projeto e o título real da conversa (`📁 Projeto • Título da Conversa`).
* **Vigilância em Segundo Plano (Background Task Guard)**: Monitoramento contínuo de tarefas em execução (*Working...*) em segundo plano caso o desenvolvedor troque de conversa no PC, notificando e comutando assim que a tarefa original for concluída.
* **Engine Tail-Seek de Baixo Consumo**: Leitura assíncrona otimizada dos últimos bytes dos arquivos de log (`transcript.jsonl`), suportando históricos de 40 MB ou mais sem consumo relevante de CPU ou RAM.

#### Alertas Sensoriais de Conclusão
* **Alerta Visual**: Flash duplo esmeralda na tela do celular com intervalo de 1 segundo ao finalizar a resposta.
* **Alerta Sonoro**: Aviso sonoro sintetizado em tempo real no navegador via Web Audio API, com ganho de volume reforçado (+dB) para ambientes barulhentos.
* **Vibração Háptica**: Padrão de pulso tátil duplo para celulares em modo silencioso (Web Vibration API).
* **Web Notifications**: Suporte a notificações nativas do sistema operacional móvel mesmo com a tela bloqueada.

#### Métricas Oficiais de Cota
* **Integração RPC com Antigravity**: Conexão direta com a API interna do IDE (`LanguageServerService/RetrieveUserQuotaSummary`) com descoberta dinâmica de porta e token CSRF.
* **Barras de Consumo em Tempo Real**: Monitoramento exato do consumo percentual da cota de 5 Horas e da cota Semanal do modelo Gemini.
* **Contador de Renovação**: Exibição do tempo exato restante para reset da cota com traduções dinâmicas de tempo.
* **Identificação de Modelo**: Exibição do modelo de IA em execução ativa (ex.: *Gemini 3.8 Flash High*).

#### Segurança, Rede & Acesso
* **Autenticação por PIN Dinâmico**: Geração de PIN aleatório de 4 dígitos no terminal do PC na primeira conexão.
* **Cache de Sessão de 24 Horas**: Sessão autorizada salva localmente por 24 horas no navegador, dispensando redigitação do PIN em recarregamentos de página.
* **Proteção Anti-Spam**: Dreno silencioso de tentativas inválidas e bloqueio de abusos no daemon.
* **Túnel HTTPS Automático**: Binário standalone oficial do Cloudflare Tunnel integrado, gerando link público seguro (`https://*.trycloudflare.com`) para habilitar notificações no Chrome/Android sem necessidade de abrir portas no roteador.

#### Usabilidade & Internacionalização
* **Suporte Trilíngue (i18n)**: Interface e mensagens com suporte completo a Português (Brasil), English e Español.
* **Atalho de Idioma**: Tecla `L` no terminal do PC para alternar instantaneamente o idioma da interface móvel.
* **Inicialização Rápida**: Script `Start_Server.bat` para arranque automático com verificação de Python e auto-instalação de dependências.
* **Zero-Install (PWA)**: Compatibilidade universal com qualquer navegador moderno (Chrome, Safari, Firefox, Edge, Opera, Samsung Internet) com suporte a instalação na tela inicial.
