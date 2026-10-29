# Changelog &bull; Antigravity Mobile APK (Android)

<p align="center">
  <b>Português</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.en.md">English</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.es.md">Español</a>
</p>

Todas as alterações do aplicativo nativo Android (**Antigravity Mobile APK**) são documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este projeto segue o [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.5.0] - 2026-10-29 (Build 2500)

### Adicionado
* **Envio remoto de prompts**: Envie comandos diretamente do celular para o Antigravity no PC (`POST /api/prompt`) escolhendo o modelo de IA desejado (Gemini 3.8 Flash, Pro, Claude 3.7 Sonnet, GPT-4o, etc.).
* **Atalhos rápidos (Snippets)**: Barra de chips para preencher o prompt com um toque (🔄 *Continue*, 🧪 *Rode os testes*, 📋 *Resuma o progresso*, 🐞 *Verifique erros*).
* **Histórico de prompts e contador**: Consulta aos últimos prompts enviados com navegação pela tecla seta para cima e contador dinâmico de caracteres e palavras.
* **Navegação com botão/gesto voltar do Android**: Fechamento hierárquico de modais abertos (Histórico, Prompt, Chats, Menu, Log, Tutorial) e retorno de conversas secundárias para a conversa ativa no PC. Quando na tela inicial, clique duplo em voltar fecha o app sem abrir a tela de gerenciamento de sessão por engano.
* **Seleção e cópia nativa de texto**: Remoção da interceptação de toque longo que abria a tela de reconexão. Segurar o dedo no texto da conversa ativa a barra nativa do Android para selecionar e copiar trechos.
* **Economia de bateria e performance**:
  - Ciclo de vida nativo com `onPause`/`onResume` no WebView para suspender repaints de GPU quando o app for minimizado ou a tela apagar.
  - Pausa de animações CSS e timers de rede via Page Visibility API (`body.app-paused`).
  - Reconexão WebSocket com backoff exponencial para não drenar bateria quando o PC estiver desligado.
  - Perfil automático para bateria fraca (<= 20% sem carregador) desativando sombras pesadas e reduzindo pings.
  - Carregamento inicial paralelizado com `Promise.allSettled`.
* **Ações rápidas nas respostas**: Botão para copiar a resposta completa com confirmação visual (📋 ➔ ✅) e botão de compartilhamento nativo (📤 via Web Share API) para enviar direto para WhatsApp, Telegram ou Notas.
* **Indicador de pensamento dinâmico**: Animação de bolinhas saltitantes enquanto a IA está processando ou executando tarefas.
* **Favoritar conversas**: Botão de estrela (⭐) para fixar conversas no topo da lista com persistência local.
* **Busca rápida de conversas**: Campo de busca instantânea com filtro por nome e projeto nos modais de Chats e Prompt.

---

## [2.4.4] - 2026-10-28 (Build 2426)

### Adicionado
* **Tela cheia imersiva**: Ocultação da barra de status e notificações do topo do celular via `WindowInsetsControllerCompat`, com suporte a entalhes de câmera (*short edges cutout mode*) e área de respiro dinâmica.
* **Monitor de bateria em tempo real**: Leitura em tempo real do nível de carga e status de carregamento via `BroadcastReceiver` do sistema, refletida no rodapé do app sem textos redundantes.
* **Alinhamento do rodapé**: Botões e indicadores padronizados com altura uniforme de 28px e cantos arredondados.

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Corrigido
* **Rolagem no APK**: Remoção do `SwipeRefreshLayout` do layout nativo, permitindo rolar mensagens livremente sem travas de toque.
* **Transição para Concluído**: O status transiciona imediatamente para "Concluído" assim que o modelo finaliza a resposta.
* **Aviso ao abrir histórico**: Corrigido toast de erro indevido ao abrir conversas pelo modal de chats.
* **Remoção de botões "✕"**: Modais agora fecham ao tocar fora ou pelo botão "Fechar" no rodapé.

### Adicionado
* **Sincronização do status "Pensando..."**: Detecção em tempo real via SQLite da conversa ativa, comutando imediatamente para "Pensando...".
* **Unificação de Background Task**: Tarefas em segundo plano foram integradas ao status "Executando Tarefa...". O status "Concluído" só é ativado quando não houver atividade pendente no projeto.
* **Botão "Chats"**: Modal para alternar entre conversas e projetos sincronizados do PC, com indicadores de status (`🟠` processando / `🟢` ocioso).
* **Leitura remota de conversas**: Permite visualizar o histórico completo de qualquer conversa no celular sem alterar a tela ativa no PC.
* **Badge de versão do APK**: O cabeçalho identifica se a versão em execução é nativa `(APK)` ou navegador `(IP)`.
* **Atualizador no menu**: Opção dentro do menu do app para verificar, baixar e instalar atualizações direto do GitHub Releases.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Adicionado
* **Leitor de QR Code nativo**: Integração com a câmera via ZXing para escanear o QR Code do terminal do PC com PIN embutido.
* **Gerenciador de sessão**: O app inicia na tela de conexão ao ser aberto para proteger o feed ativo.
* **Reconexão de sessão**: Botão "Voltar à Sessão" para reconectar ao servidor ativo sem precisar redigitar o PIN.
* **Opção "Nova Sessão" e botão "Sair"**: Atalhos para trocar de servidor ou encerrar a sessão pelo menu.
* **Visual OLED Black**: Remoção de botões legados em favor da interface com fundo `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Corrigido
* **Protocolo de rede (HTTP/HTTPS)**: Aplica `http://` para IPs locais e `https://` apenas em túneis e domínios públicos, prevenindo erros de TLS.
* **Porta padrão automática**: Anexa `:8765` automaticamente quando um IP for inserido sem porta.
* **Tratamento de erros no WebView**: Diagnósticos claros de conexão e compatibilidade com Android 7 a 9.

### Adicionado
* **Atalhos rápidos**: Botões de preenchimento para emulador, Wi-Fi local e Cloudflare, além de atalho para colar da área de transferência.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Lançamento Inicial do APK
* **Estrutura nativa Android**: Projeto Kotlin com `minSdk = 24` (Android 7.0+) e `targetSdk = 34` (Android 14).
* **WebView acelerado**: Aceleração por hardware, suporte a WebSockets (`/ws`), Web Audio API e tema OLED Black `#000000`.
* **Permissões**: Suporte nativo a notificações (`POST_NOTIFICATIONS`) e conexões HTTP em rede local (`usesCleartextTraffic`).
* **CI/CD no GitHub Actions**: Build e empacotamento automático de releases do APK a cada push ou tag.
