# Antigravity Mobile

<p align="center">
  <b>Português</b> &bull; <a href="README.en.md">English</a> &bull; <a href="README.es.md">Español</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/versão-v2.5.0-blue?style=flat-square" alt="Versão v2.5.0">
  <img src="https://img.shields.io/badge/plataforma-Windows_%7C_Android-success?style=flat-square" alt="Plataformas">
  <img src="https://img.shields.io/badge/android-7.0%2B_%28API_24%2B%29-green?style=flat-square" alt="Android 7+">
  <img src="https://img.shields.io/badge/licença-MIT-yellow?style=flat-square" alt="Licença MIT">
  <img src="https://img.shields.io/badge/build-GitHub_Actions_Passing-brightgreen?style=flat-square" alt="GitHub Actions">
</p>

Aplicativo e painel web para acompanhar as tarefas do **Antigravity IDE** no celular em tempo real. Exibe o chat filtrado, avisa quando uma tarefa termina (som, flash na tela e vibração), monitora cotas de IA e permite navegar entre conversas e projetos. Funciona via Wi-Fi local ou túnel Cloudflare, por aplicativo nativo Android (APK) ou navegador.

---

## Recursos

### Envio de Prompts e Ações Remotas
* **Envio remoto de prompts**: Dispare comandos diretamente do celular para o Antigravity no PC (`POST /api/prompt`) escolhendo o modelo de IA desejado (Gemini 3.8 Flash, Pro, Claude 3.7 Sonnet, GPT-4o, etc.).
* **Atalhos rápidos (Snippets)**: Chips de comandos frequentes (🔄 *Continue*, 🧪 *Rode os testes*, 📋 *Resuma o progresso*, 🐞 *Verifique erros*) para preencher com um toque.
* **Histórico e contador**: Histórico dos últimos prompts enviados (navegação com tecla seta para cima) e contador de caracteres/palavras em tempo real.
* **Ações nas respostas**: Botão para copiar a resposta completa com confirmação visual (📋 ➔ ✅) e botão de compartilhamento nativo (📤 via Web Share API) para WhatsApp, Telegram e notas.
* **Favoritar conversas**: Fixação de conversas importantes no topo da lista com persistência local (⭐).

### Chat e Navegação
* **Chat em tempo real**: Exibe as mensagens do usuário e a resposta final do assistente, sem poluição de logs intermediários de ferramentas.
* **Seleção nativa de texto**: Segure o dedo sobre qualquer balão da conversa para selecionar trechos e copiar usando a barra de ferramentas nativa do Android.
* **Gesto/botão voltar inteligente**: Fecha modais em ordem hierárquica (Histórico, Prompt, Chats, Menu, Log) ou retorna à conversa principal do PC. Se estiver na tela inicial, clique duplo sai do app sem abrir a tela de gerenciamento de sessão por engano.
* **Markdown e código**: Suporte a blocos de código com destaque de sintaxe, tabelas e rolagem suave pelo histórico.
* **Navegação entre conversas (Chats)**: Lista projetos e conversas do PC com indicadores de status em tempo real (`🟠` processando / `🟢` ocioso) e busca rápida com filtro.

### Status e Alertas
* **Status em tempo real**: Mostra o estado atual da tarefa (*Pensando...*, *Trabalhando...*, *Executando Tarefa...* e *Concluído*).
* **Alertas de conclusão**: Toca um aviso sonoro (4 opções com volume ajustável), pisca a tela em verde duas vezes e vibra o celular quando a tarefa termina.
* **Monitoramento de cotas**: Leitura das cotas de 5 horas e semanal da API do Antigravity (Gemini, Claude e GPT).
* **Indicador de ping**: Medidor de latência da conexão via WebSocket em tempo real.
* **Bateria em tempo real**: Porcentagem atual da bateria exibida no centro do rodapé, ao lado da latência, sem poluição visual.

### App Android Nativo (APK) e Economia de Bateria
* **Economia de energia inteligente**: O motor WebKit entra em modo de baixo consumo ao desligar a tela ou minimizar (`onPause`/`onResume`), pausando animações de GPU e timers desnecessários via Page Visibility API.
* **Reconexão com backoff exponencial**: Evita drenar a bateria tentando reconectar em loop rápido caso o PC esteja desligado.
* **Perfil de bateria fraca**: Desativa sombras pesadas e reduz frequência de ping automaticamente quando a bateria atinge <= 20%.
* **Tela cheia imersiva**: Oculta a barra de status/notificações no APK e oferece suporte a tela cheia no navegador/IP para foco visual total.
* **Tema OLED Black**: Fundo `#000000` absoluto por padrão para economia de até 60% em telas AMOLED/OLED.
* **Login por QR Code**: Pareamento com a câmera lendo o QR Code do terminal do PC.
* **Reconexão automática**: Opção de voltar à sessão ativa sem precisar redigitar o PIN.
* **Atualizador integrado**: Verificação e instalação de novas versões direto pelo menu do app. Veja os changelogs do APK: [Português](android/CHANGELOG.md) &bull; [English](android/CHANGELOG.en.md) &bull; [Español](android/CHANGELOG.es.md).

---

## Estrutura do Projeto

```text
antigravity-mobile/
├── .github/workflows/
│   └── build-apk.yml          # CI/CD: build automático do APK no GitHub Actions
├── android/                   # App nativo Android (Kotlin / Gradle)
│   ├── app/src/main/
│   │   ├── java/.../MainActivity.kt  # WebView, câmera ZXing e gerenciador de sessão
│   │   ├── res/layout/activity_main.xml
│   │   └── AndroidManifest.xml
│   ├── CHANGELOG.md           # Changelog do APK (Português)
│   ├── CHANGELOG.en.md        # Changelog do APK (English)
│   └── CHANGELOG.es.md        # Changelog do APK (Español)
├── desktop-bridge/            # Servidor local Windows (Python / FastAPI)
│   ├── Start_Server.bat       # Inicializador para Windows
│   ├── run.py                 # CLI com QR Code no terminal
│   ├── server.py              # API FastAPI e WebSocket (/ws)
│   ├── auth.py                # Autenticação por PIN
│   ├── monitor.py             # Monitoramento de logs e banco SQLite do IDE
│   ├── antigravity_api.py     # Leitura das cotas via RPC interna
│   ├── tunnel.py              # Túnel Cloudflare (acesso externo seguro)
│   ├── language_manager.py    # Internacionalização (pt, en, es)
│   └── static/                # Interface web móvel (HTML, CSS, JS)
│       ├── index.html
│       └── manifest.json
├── CHANGELOG.md               # Changelog geral (Português)
├── CHANGELOG.en.md            # Changelog geral (English)
├── CHANGELOG.es.md            # Changelog geral (Español)
├── LICENSE                    # Licença MIT
└── TUTORIAL.txt
```

---

## Como Usar

### 1. No PC
1. Requer **Python 3.10+** no Windows.
2. Clone o repositório:
   ```bash
   git clone https://github.com/lumiag5/antigravitymb.git
   cd antigravitymb
   ```
3. Execute `Start_Server.bat` (dentro da pasta `desktop-bridge/`).
   O script instala dependências e abre o terminal com o IP local, link Cloudflare e o QR Code.

### 2. No Celular (Android)

#### Pelo App APK (Recomendado)
1. Baixe o APK na aba [Releases](https://github.com/lumiag5/antigravitymb/releases).
2. Instale no celular.
3. Abra o app e toque em **Entrar com QR Code** apontando para o terminal do PC (ou use a reconexão automática se já tiver pareado).

#### Pelo Navegador
1. Conecte o celular no mesmo Wi-Fi do computador e acesse `http://[IP_DO_PC]:8765`.
2. Para acesso remoto (4G/5G), use o link `https://*.trycloudflare.com`.
3. Digite o PIN de 4 dígitos informado no terminal.

---

## Atalhos do Console

Com o servidor rodando no PC:
* **`P`**: Gera um novo PIN e atualiza o QR Code.
* **`L`**: Alterna o idioma (Português / English / Español).
* **`Q`**: Atualiza a leitura das cotas do modelo.
* **`Ctrl + C`**: Encerra o servidor e fecha o túnel.

---

## Licença

Distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para mais detalhes.
