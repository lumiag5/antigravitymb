# Changelog &bull; Antigravity Mobile APK (Android Nativo)

Todas as alterações, correções e novos recursos dedicados exclusivamente ao aplicativo nativo Android (**Antigravity Mobile APK**) estão documentados neste arquivo.

O formato segue o padrão [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e as convenções do [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
