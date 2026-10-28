# Changelog &bull; Antigravity Mobile APK (Android)

<p align="center">
  <b>Português</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.en.md">English</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/android/CHANGELOG.es.md">Español</a>
</p>

Todas as alterações do aplicativo nativo Android (**Antigravity Mobile APK**) são documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este projeto segue o [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Corrigido
* **Rolamento no APK**: Remoção do `SwipeRefreshLayout` do layout nativo, permitindo rolar mensagens livremente sem travas de toque.
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
