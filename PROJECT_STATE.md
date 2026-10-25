# ESTADO ATUAL DO PROJETO

## PROJETO
Antigravity Mobile

## OBJETIVO DO PROJETO
Desenvolver o "Antigravity Mobile", um companion para celular que atua como uma tela secundária para o Antigravity IDE no PC:
1. **Monitoramento do Chat em Tempo Real**: Acompanhar o fluxo de mensagens e conclusões do agente enquanto o desenvolvedor se afasta do PC.
2. **Alertas Sensoriais de Conclusão**: Piscar a tela do celular (flash duplo), reproduzir aviso sonoro personalizável e vibração quando a tarefa de código for finalizada.
3. **Métricas Oficiais de Quota**: Exibição em tempo real da porcentagem de uso diário (5h) e semanal do modelo de IA via RPC interna com adaptação dinâmica entre grupos de modelos.
4. **Conectividade Flexível**: Suporte à rede local (Wi-Fi) e acesso remoto global via túnel HTTPS seguro (Cloudflare) sem configuração de portas.

## FUNCIONALIDADES IMPLEMENTADAS (v2.4.1 • Build 2419)
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
  - `README.md`, `README.en.md`, `README.es.md` (Markdown com seletor trilíngue).
- **CHANGELOG**:
  - `CHANGELOG.md`, `CHANGELOG.en.md`, `CHANGELOG.es.md` (Markdown no padrão Keep a Changelog cobrindo v2.3.5, v2.3.6 e v2.4.0).
- **LICENÇA & TUTORIAL**:
  - `LICENSE` (Licença MIT oficial - Copyright © 2026 Dev LumiaG5).
  - `TUTORIAL.txt` (Guia passo a passo de conexão em pt, en, es).

## ÚLTIMA ALTERAÇÃO
- **Correção de Protocolo HTTP/HTTPS, Presets Rápidos e Compatibilidade com Emuladores no APK (v2.4.1 • Build 2419)**:
  - Implementada dedução inteligente de protocolo (`cleanServerUrl`) no APK: IPs locais (`192.168.x.x`, `10.0.2.2`, `localhost`) utilizam estritamente `http://` para evitar rejeição TLS do Uvicorn (`Invalid HTTP request received`).
  - Auto-completar de porta `:8765` para IPs locais sem especificação de porta.
  - Tela de conexão atualizada com 3 botões de atalho rápido: `💻 Emulador (10.0.2.2:8765)`, `📶 Wi-Fi Local (192.168.0.6:8765)` e `🌐 Túnel Cloudflare (https://)`.
  - Adicionado botão dedicado para colar a URL da Área de Transferência (`btnPasteClipboard`).
  - Diagnóstico aprimorado de erros de rede: exibe URL tentada e código de erro legível, prevenindo tela preta sem feedback.
  - Intercepção de erro dupla garantindo compatibilidade com versões antigas do WebView em emuladores como LDPlayer (Android 7 a 9).

## ESTADO ATUAL
- Versão v2.4.1 (Build 2419) pronta para compilação automática no GitHub Actions com suporte total para emuladores e conexões locais e remotas.
