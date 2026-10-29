# Changelog

<p align="center">
  <b>Português</b> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.en.md">English</a> &bull; <a href="https://github.com/lumiag5/antigravitymb/blob/main/CHANGELOG.es.md">Español</a>
</p>

Todas as alterações notáveis do **Antigravity Mobile** são documentadas neste arquivo.

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
* **Tela cheia imersiva**: Ocultação da barra de status do celular no APK (com suporte a entalhes de câmera *notch*), e modo tela cheia no navegador/IP ativado por toque ou pelo menu de configurações.
* **Nível de bateria em tempo real**: Porcentagem atual da bateria exibida no centro do rodapé (entre latência e chats), sem poluição visual nem textos adicionais.
* **Harmonização do rodapé**: Alinhamento simétrico e padronização visual de todos os botões e indicadores em linha única, com cantos arredondados e suporte ao tema OLED.

---

## [2.4.3] - 2026-10-28 (Build 2425)

### Corrigido
* **Rolagem no APK**: Remoção do `SwipeRefreshLayout` no app Android, permitindo rolar o histórico do chat livremente sem travas de toque.
* **Remoção de botões "✕"**: Modais agora fecham ao tocar fora ou pelo botão "Fechar" no rodapé.

### Adicionado
* **Botão "Chats"**: Modal para alternar entre conversas e projetos sincronizados do PC, com indicadores de status (`🟠` processando / `🟢` ocioso).
* **Leitura remota de conversas**: Permite visualizar o histórico completo de qualquer conversa no celular sem alterar a tela ativa no PC.
* **Status em tempo real**: Adicionados os status *Pensando...*, *Trabalhando...*, *Executando Tarefa...* (com ponto ciano) e *Concluído* (exibido por 1 minuto ao finalizar).
* **Identificação de versão**: O cabeçalho agora mostra se a versão em execução é nativa `(APK)` ou navegador `(IP)`.
* **Atualização do APK no menu**: Opção no menu para baixar e instalar novas versões direto do GitHub Releases.

---

## [2.4.2] - 2026-10-25 (Build 2420)

### Adicionado
* **Login com QR Code**: Leitor de câmera nativo (ZXing) no APK para escanear o QR Code do terminal do PC com PIN embutido.
* **Reconexão de sessão**: Botão "Voltar à Sessão" para reconectar ao servidor ativo sem precisar redigitar o PIN.
* **Opção "Nova Sessão" e botão "Sair"**: Atalhos para trocar de servidor ou encerrar a sessão pelo menu.
* **Tela de sessão inicial**: O app inicia na tela de conexão ao ser aberto para proteger o feed ativo.
* **Limpeza de interface**: Remoção de atalhos legados em favor do tema OLED Black `#000000`.

---

## [2.4.1] - 2026-10-25 (Build 2419)

### Corrigido
* **Ajuste de protocolo (HTTP/HTTPS)**: Uso de `http://` em IPs locais e `https://` apenas em túneis e domínios públicos, evitando falha de TLS.
* **Porta padrão automática**: Adiciona `:8765` automaticamente se um IP for inserido sem porta.
* **Tratamento de erros no WebView**: Diagnóstico mais claro de falhas de conexão e compatibilidade com Android 7 a 9.

### Adicionado
* **Atalhos de conexão**: Botões rápidos para emulador (`10.0.2.2`), Wi-Fi local e Cloudflare, além de botão para colar link da área de transferência.

---

## [2.4.0] - 2026-10-25 (Build 2418)

### Adicionado
* **QR Code no terminal**: Exibição de QR Code ASCII no console para pareamento rápido com a câmera do celular.
* **Menu de configurações**: Centralização de preferências de alertas, áudio, rede e histórico em um menu único no rodapé.
* **Personalização de áudio**: 4 opções de alertas sonoros e slider de volume com persistência local.
* **Medidor de ping**: Indicador visual de latência da conexão WebSocket ao lado do menu.
* **Histórico de tarefas**: Modal com log das últimas tarefas concluídas (projeto, modelo e horário).

---

## [2.3.6] - 2026-10-25 (Build 2417)

### Adicionado
* **Troca de modelo em tempo real**: Detecção automática de mudança de modelo de IA (Gemini, Claude, GPT) durante a conversa via decodificação Protobuf.
* **Comutação de cotas**: As barras de cota alternam dinamicamente entre Gemini e Claude/GPT conforme o modelo em uso.
* **Conexão SQLite somente leitura**: Uso de `mode=ro` para evitar bloqueios de banco de dados enquanto o IDE grava informações.

---

## [2.3.5] - 2026-10-25 (Build 2416)

### Lançamento Inicial
* **Monitoramento do chat**: Feed em tempo real exibindo mensagens do usuário e respostas finais do assistente.
* **Renderização**: Suporte a Markdown, blocos de código com destaque e tema escuro OLED.
* **Alertas**: Notificações ao concluir tarefas com som, flash duplo na tela e vibração.
* **Cotas**: Leitura das cotas de 5 horas e semanal da API do Antigravity.
* **Conexão segura**: Pareamento por PIN de 4 dígitos (sessão de 24h) e suporte a túnel Cloudflare para acesso remoto.
* **Idiomas**: Suporte a Português, Inglês e Espanhol.
