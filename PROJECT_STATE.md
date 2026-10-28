# ESTADO ATUAL DO PROJETO

## PROJETO
Antigravity Mobile

## OBJETIVO DO PROJETO
Desenvolver o "Antigravity Mobile", um companion para celular que atua como uma tela secundária para o Antigravity IDE no PC:
1. **Monitoramento do Chat em Tempo Real**: Acompanhar o fluxo de mensagens e conclusões do agente enquanto o desenvolvedor se afasta do PC.
2. **Alertas Sensoriais de Conclusão**: Piscar a tela do celular (flash duplo), reproduzir aviso sonoro personalizável e vibração quando a tarefa de código for finalizada.
3. **Métricas Oficiais de Quota**: Exibição em tempo real da porcentagem de uso diário (5h) e semanal do modelo de IA via RPC interna com adaptação dinâmica entre grupos de modelos.
4. **Conectividade Flexível**: Suporte à rede local (Wi-Fi) e acesso remoto global via túnel HTTPS seguro (Cloudflare) sem configuração de portas.

## FUNCIONALIDADES IMPLEMENTADAS (v2.4.3 • Build 2421)
- **Correção de Rolamento Vertical do Chat no APK**: Remoção do `SwipeRefreshLayout` em `activity_main.xml` e no `MainActivity.kt`, restaurando 100% a rolagem nativa de mensagens anteriores no APK Android, igual à versão por IP.
- **Navegação Multi-Conversas com Botão "Chats"**:
  - Botão `💬 Chats` no centro inferior do rodapé (entre Menu/Latência e o botão OLED).
  - Modal com listagem de conversas e projetos sincronizados do Antigravity PC com leitura de transcripts em background.
  - Indicadores pulsantes estritos na frente de cada conversa: **somente dot laranja (`🟠`)** se o Antigravity estiver processando algo, ou **somente dot verde (`🟢`)** se estiver ocioso, sem textos frontais.
  - Carregamento de histórico completo com liberdade remota pelo smartphone sem alterar nem clicar na conversa aberta no PC.
- **Novos Status de Tarefa e Temporizador de Conclusão**:
  - Renomeação de "Processando" para **"Trabalhando..."** (*Working*).
  - Adição do status **"Pensando..."** (*Thought*).
  - Adição do status **"Executando Tarefa..."** (*Task Running*) com indicador visual ciano pulsante (`#0ea5e9`).
  - O status **"Concluído"** (*Done*) permanece ativo por **1 minuto** (ou até iniciar nova atividade) antes de transicionar para "Conectado".
  - Paridade total e traduções em PT-BR, EN e ES para ambas as versões (APK e IP/Web).
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
- **Gerenciamento de Sessão com Logout ao Fechar, Leitura de QR Code via Câmera e Layout Minimalista (v2.4.2 • Build 2420)**:
  - O app agora sempre inicia na tela de sessão ao ser aberto, deslogando a visualização direta por segurança.
  - Adicionada opção **"Voltar à Sessão"**: se o servidor no PC continuar aberto, reconecta imediatamente sem pedir novo PIN.
  - Adicionada opção **"Entrar com QR Code"**: ativa a câmera do celular/emulador para escanear o QR Code gerado no terminal do PC via biblioteca ZXing.
  - O QR Code do console agora transporta o PIN dinâmico (`?pin=XXXX`), permitindo login 100% automático e instantâneo ao escanear com a câmera.
  - Adicionada opção **"Nova Sessão"**: limpa a autenticação anterior e permite inserir novo PIN ou trocar de servidor.
  - Adicionado botão **"Sair / Desconectar da Sessão"** dentro do modal de Configurações (`⚙️ Menu`).
  - Removidos todos os atalhos rápidos antigos de emulador/rede, deixando a tela minimalista e focada em OLED Black.

## ESTADO ATUAL
- Versão v2.4.2 (Build 2420) com controle avançado de ciclo de vida de sessão, scanner nativo de QR Code e compilação automatizada no GitHub Actions.
