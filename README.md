# Antigravity Mobile

<p align="center">
  <b>Português</b> &bull; <a href="README.en.md">English</a> &bull; <a href="README.es.md">Español</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versão-v2.4.3-blue?style=flat-square" alt="Versão v2.4.3">
  <img src="https://img.shields.io/badge/plataforma-Windows_%7C_Android-success?style=flat-square" alt="Plataformas">
  <img src="https://img.shields.io/badge/android-7.0%2B_%28API_24%2B%29-green?style=flat-square" alt="Android 7+">
  <img src="https://img.shields.io/badge/licença-MIT-yellow?style=flat-square" alt="Licença MIT">
  <img src="https://img.shields.io/badge/build-GitHub_Actions_Passing-brightgreen?style=flat-square" alt="GitHub Actions">
</p>

Companion mobile para transformar seu celular em uma **segunda tela inteligente** para o **Antigravity IDE** no PC. Monitore o progresso do chat de código em tempo real, receba alertas sensoriais (som personalizável, flash e vibração) ao término de cada tarefa, acompanhe o consumo oficial das suas cotas de IA (Gemini, Claude Sonnet e GPT) e conecte-se com um toque pelo **aplicativo Android nativo** ou navegador.

---

## 🎯 Por que o Antigravity Mobile?

Quando você coloca o Antigravity IDE para rodar tarefas longas — como refatorações de código, suítes completas de testes, depurações complexas ou criação de múltiplos módulos —, é natural se afastar da mesa de trabalho. O desafio é saber:
- Se o agente de IA terminou de programar ou se parou aguardando aprovação de terminal.
- Em qual modelo o assistente está operando (Gemini, Claude 3.5 Sonnet ou GPT-4o).
- Quanto resta da sua cota de 5 horas e semanal da IA.

O **Antigravity Mobile** resolve tudo isso conectando o PC diretamente ao seu celular através de uma conexão Wi-Fi local ou por um **túnel HTTPS global (Cloudflare)** seguro e sem necessidade de abrir portas no roteador.

---

## ⚡ Principais Funcionalidades

### 💬 Chat em Tempo Real com Feed Filtrado
* **Foco no que interessa**: O Antigravity IDE gera centenas de linhas de logs internos de execução e chamadas de ferramentas. O companion filtra os ruídos e exibe apenas o prompt do desenvolvedor e a conclusão final do assistente.
* **Renderização Markdown & Código**: Realce de sintaxe em blocos de código, tabelas e tipografia alinhada à do IDE (fontes Inter e JetBrains Mono).
* **Auto-Scroll Inteligente & Rolagem Livre**: Acompanha o fluxo das respostas automaticamente e permite rolar livremente para cima no histórico de mensagens sem travas no APK ou no navegador.

### 💬 Navegação Central "Chats" & Multi-Projetos
* **Botão "Chats" no Rodapé**: Acesso direto a todas as conversas e projetos sincronizados do Antigravity PC com um único toque.
* **Indicadores Pulsantes Estritos**:
  * `🟠` **Ponto Laranja Pulsante**: O Antigravity está ativamente trabalhando/processando naquela conversa.
  * `🟢` **Ponto Verde Pulsante**: A conversa está em repouso/ociosa.
  *(Visual 100% limpo, sem textos poluindo a lista).*
* **Inspeção Remota Independente**: Leia todo o histórico de qualquer projeto pelo celular sem alternar janelas ou interferir no trabalho ativo no computador, com botão de retorno à sincronização ao vivo.

### ⚡ Status Dinâmicos & Sincronização em Tempo Real
* **"Pensando..." (*Thinking*) Instantâneo**: Monitoramento direto dos passos no SQLite (`conversations/<conv_id>.db`) que ativa o status roxo pulsante (`#a855f7`) no exato milissegundo em que o PC entra em modo de reflexão.
* **Unificação de "Background Task" & "Executando Tarefa..."**: Subagentes `invoke_subagent`, temporizadores `schedule`, comandos `manage_task` e tarefas de terminal são exibidos sob o status ciano pulsante (`#0ea5e9`).
* **Critério Rigoroso para "Concluído" (*Done*)**: O status só passa para "Concluído" quando **todas as atividades do projeto estiverem 100% finalizadas**, permanecendo visível por **1 minuto** com toque sonoro e duplo flash.

### 🔔 Alertas Sensoriais de Conclusão de Tarefa
* **Duplo Flash Visual**: A tela do celular pisca duas vezes em verde esmeralda com intervalo de 1 segundo (visível mesmo com o celular repousado sobre a mesa).
* **Sintetizador de Toques (Web Audio API)**: Escolha entre 4 estilos sonoros (*Chime Moderno*, *Sino Zen*, *Pulso Sci-Fi* e *Bip Clássico*) com slider de controle de volume (0% a 100%) e botão de teste imediato.
* **Vibração Tátil**: Padrão de vibração dupla para ambientes onde o celular deve permanecer em modo silencioso.
* **Notificações Push**: Suporte a Web Notifications nativas mesmo com o aparelho com tela bloqueada.

### 🧠 Detecção em Tempo Real de Modelos de IA
* **Gemini, Claude e GPT**: O servidor monitora em tempo real a comutação de modelos na conversa do IDE através da decodificação de tags binárias Protobuf (campo 28 `\xe2\x01` para Claude/GPT e campo 19 `\x9a\x01` para Gemini), sem exigir reinicialização do daemon.

### 📊 Acompanhamento Oficial de Cotas (RPC Interna)
* **Métricas Reais sem Estimativas**: Conexão direta com o serviço RPC interno do Antigravity (`LanguageServerService/RetrieveUserQuotaSummary`).
* **Comutação Dinâmica de Cotas**: Alterna automaticamente entre as cotas dos grupos `Gemini Models` e `Claude and GPT models` conforme a família do modelo em execução no instante exato.
* **Barras de Uso**: Exibe o consumo percentual da cota de 5 Horas e da cota Semanal, com indicação do tempo para renovação.

### 📶 Medidor de Latência em Tempo Real (Ping)
* **Badge Dinâmico**: Indicador visual colorido ao lado do menu com round-trip em milissegundos via WebSocket:
  * 🟢 **Verde**: Latência excelente (<130ms)
  * 🟡 **Amarelo**: Latência intermediária (130ms a 320ms)
  * 🔴 **Vermelho**: Conexão lenta (>320ms)

### 📜 Histórico de Conclusões de Tarefas (Log)
* Modal retrátil com registro das tarefas finalizadas pelo agente, contendo o projeto, título da tarefa, modelo de IA utilizado e horário exato de término.

### 📱 Aplicativo Nativo Android (APK Kotlin)
Disponível em pacote `.apk` com integração profunda ao sistema:
* **Atualização Automática no Menu**: Verificação em 1 toque de novas releases publicadas no GitHub com download e instalação direta via `FileProvider`.
* **Badge de Versão Dinâmico**: Identifica explicitamente se você está no APK (`vX.X.X (APK)`) ou no navegador IP (`vX.X.X (IP)`).
* **Modo OLED True Black (`#000000`)**: Máxima economia de bateria em telas AMOLED e conforto visual.
* **Interface Limpa sem Botões "✕"**: Fechamento simplificado ao tocar fora da janela (backdrop click) ou no botão "Fechar" inferior.
* **Logout Automático ao Fechar o App**: Ao fechar o app, a sessão é pausada, garantindo privacidade.
* **▶ Voltar à Sessão (Sem Novo PIN)**: Se o servidor estiver ativo no PC, um único toque reconecta ao dashboard mantendo a autorização válida por 24 horas.
* **📷 Entrar com QR Code via Câmera (ZXing)**: Scanner nativo de câmera integrado para ler o QR Code do terminal do PC com PIN dinâmico embutido (`?pin=XXXX`), liberando o acesso instantaneamente sem necessidade de digitação.
* **⚡ Nova Sessão**: Atalho para limpar tokens anteriores e iniciar novo pareamento.
* **CI/CD Automatizado**: O APK é compilado na nuvem via **GitHub Actions** a cada versão. Veja os changelogs do APK: [Português](android/CHANGELOG.md) &bull; [English](android/CHANGELOG.en.md) &bull; [Español](android/CHANGELOG.es.md).

---

## 🛠️ Arquitetura do Projeto

```text
antigravity-mobile/
├── .github/workflows/
│   └── build-apk.yml          # CI/CD: Compilação automatizada do APK na nuvem
├── android/                   # Projeto Nativo Android (Kotlin / Gradle)
│   ├── app/src/main/
│   │   ├── java/.../MainActivity.kt  # Gerenciador de Sessão, WebView e ZXing Scanner
│   │   ├── res/layout/activity_main.xml  # Layout OLED True Black
│   │   └── AndroidManifest.xml
│   ├── CHANGELOG.md           # Histórico de versões do APK (Português)
│   ├── CHANGELOG.en.md        # APK Changelog (English)
│   └── CHANGELOG.es.md        # Changelog del APK (Español)
├── desktop-bridge/            # Daemon Local para Windows (Python / FastAPI)
│   ├── Start_Server.bat       # Inicializador em 1 clique para Windows
│   ├── run.py                 # CLI com ASCII QR Code e atalhos de teclado
│   ├── server.py              # Servidor FastAPI e WebSockets (/ws)
│   ├── auth.py                # Segurança com PIN de 4 dígitos e cache de 24h
│   ├── monitor.py             # Parser Protobuf e monitoramento em segundo plano
│   ├── antigravity_api.py     # Cliente RPC para leitura das cotas do IDE
│   ├── tunnel.py              # Gerenciador de túneis Cloudflare
│   ├── language_manager.py    # Internacionalização (pt, en, es)
│   └── static/                # Interface Mobile PWA (HTML5, CSS, JS, Web Audio)
│       ├── index.html         # Painel completo do companion
│       └── manifest.json      # Especificações oficiais PWA
├── CHANGELOG.md               # Changelog geral do ecossistema (Português)
├── CHANGELOG.en.md            # General project changelog (English)
├── CHANGELOG.es.md            # Changelog general del proyecto (Español)
├── LICENSE                    # Licença MIT (Copyright © 2026 Dev LumiaG5)
└── TUTORIAL.txt               # Guia de conexão passo a passo
```

---

## 🚀 Como Executar

### 1. No Computador (PC)
1. Certifique-se de ter o **Python 3.10+** instalado no Windows.
2. Clone o repositório ou baixe o código:
   ```bash
   git clone https://github.com/lumiag5/antigravitymb.git
   cd antigravitymb
   ```
3. Execute o inicializador:
   * Dê dois cliques em **`Start_Server.bat`** (dentro da pasta `desktop-bridge/`).
   *(O script verificará as dependências e abrirá o terminal com o endereço local, o túnel HTTPS e o QR Code em ASCII).*

---

### 2. No Celular ou Emulador (Android)

#### Opção A: Pelo Aplicativo Nativo (Recomendado)
1. Acesse as [Releases](https://github.com/lumiag5/antigravitymb/releases) ou os [Artifacts do GitHub Actions](https://github.com/lumiag5/antigravitymb/actions) e baixe o arquivo `AntigravityMobile-Release-APK`.
2. Instale o arquivo `.apk` no celular ou arraste para dentro do seu emulador (ex: LDPlayer, Nox).
3. Abra o app:
   * **Conexão Instantânea**: Clique em **`📷 Entrar com QR Code`** e aponte a câmera para o terminal do PC!
   * **Voltar ao Trabalho**: Se você fechou o app e o PC continua ligado, clique em **`▶ Voltar à Sessão`** para entrar sem precisar digitar PIN.

#### Opção B: Pelo Navegador Mobile (PWA)
1. Conecte o celular na mesma rede Wi-Fi do computador e acesse o endereço `http://[IP_DO_PC]:8765` exibido no terminal.
2. Ou use o link seguro **`https://*.trycloudflare.com`** exibido no terminal para acessar de qualquer lugar via 4G/5G.
3. Digite o PIN de 4 dígitos informado no console do PC para liberar o acesso.

---

## ⌨️ Comandos do Console do PC

Durante a execução do `Start_Server.bat`, você pode interagir com o console pelas teclas de atalho:
* **`P`**: Gera um novo PIN de segurança de 4 dígitos e atualiza o QR Code.
* **`L`**: Alterna instantaneamente o idioma da interface (Português &harr; English &harr; Español).
* **`Q`**: Força a leitura imediata das cotas oficiais do modelo.
* **`Ctrl + C`**: Encerra o servidor e fecha o túnel com segurança.

---

## 📄 Licença & Autoria

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para obter mais informações.

Desenvolvido por **Dev LumiaG5** &bull; Copyright &copy; 2026. Todos os direitos reservados.
