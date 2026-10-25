# Antigravity Mobile

<p align="center">
  <b>Português</b> &bull; <a href="README.en.md">English</a> &bull; <a href="README.es.md">Español</a>
</p>

Companion leve para monitorar o **Antigravity IDE** pelo celular em tempo real. Acompanhe o progresso das tarefas da IA, receba alertas sonoros/visuais quando o código terminar de rodar e visualize o consumo oficial da sua cota do Gemini sem precisar instalar nenhum app da Play Store ou App Store.

---

## Motivação

Quando você coloca o Antigravity para rodar tarefas longas — como refatorações pesadas, geração de múltiplos componentes ou suítes de testes —, você geralmente sai de perto do PC para fazer outra coisa. O problema é que não dá pra saber se a IA terminou, se ela parou pedindo confirmação de terminal ou se a cota de 5 horas estourou. Ficar levantando a cada cinco minutos ou dando Alt-Tab para conferir quebra o foco.

O **Antigravity Mobile** resolve isso com um pequeno servidor local (daemon em Python) que roda no PC e se conecta ao seu celular via rede local (Wi-Fi) ou túnel HTTPS seguro. Ele entrega uma interface web escura, limpa e pensada para telas mobile, avisando quando o trabalho estiver pronto.

---

## Funcionalidades

### Chat em Tempo Real & Filtragem de Ruído
* **Foco no que interessa**: O Antigravity gera centenas de linhas de logs de ferramentas internas e saídas de terminal. O companion filtra tudo isso e exibe apenas o prompt enviado e a conclusão final do assistente.
* **Markdown & Código**: Renderização com blocos de código formatados, tabelas e listas com tipografia idêntica à do IDE (Inter e JetBrains Mono).
* **Auto-scroll**: Acompanha novas mensagens automaticamente, pausando caso você role para cima para ler histórico anterior.

### Troca Automática de Projetos e Conversas
* **Detecção em tempo real**: O servidor monitora os locks de foco (`presence/`), o banco SQLite e metadados do IDE. Quando você clica em outra conversa ou projeto no PC, a tela do celular muda imediatamente (`📁 Projeto • Título da Conversa`).
* **Vigilância em background**: Se você trocar de conversa no PC enquanto uma tarefa ainda estiver processando (*Working...*), o servidor continua acompanhando a tarefa anterior em segundo plano e notifica assim que ela concluir.

### Alertas de Conclusão de Tarefa
Assim que a IA encerra o turno de resposta:
* **Flash na tela**: 2 piscadas em verde esmeralda com intervalo de 1 segundo (visível mesmo com o celular apoiado na mesa).
* **Aviso sonoro**: Tom sintetizado via Web Audio API com volume calibrado (+dB) para ser audível em ambientes com ruído.
* **Vibração**: Padrão tátil duplo para celulares em modo silencioso.
* **Notificações do sistema**: Suporte a Web Notifications nativas do navegador com a tela bloqueada.

### Acompanhamento Oficial de Cotas (RPC Interna)
* **Sem estimativas de tokens**: Conecta diretamente no endpoint RPC local do Antigravity (`LanguageServerService/RetrieveUserQuotaSummary`) descobrindo dinamicamente a porta e o token CSRF.
* **Métricas reais**: Barras de progresso com porcentagem de consumo da cota de 5 Horas e da cota Semanal, tempo exato de renovação e modelo ativo (ex: *Gemini 3.8 Flash High*).

### Modo OLED Black
* Fundo preto absoluto (`#000000`) para economia de energia em telas AMOLED/OLED.
* Balão de mensagem do usuário adaptado para cinza escuro de alto contraste, evitando cansaço visual em ambientes escuros.

### Segurança com PIN & Sessão de 24h
* Ao abrir no celular pela primeira vez, o terminal do PC exibe um PIN aleatório de 4 dígitos.
* Após parear, a sessão fica salva em cache local por 24 horas — você pode recarregar a página ou trocar de aba sem precisar digitar o PIN novamente.
* Proteção anti-spam no daemon para bloquear tentativas incorretas.

### Túnel HTTPS Automático (Cloudflare)
* Já vem com o binário standalone do Cloudflare Tunnel embutido.
* Gera automaticamente uma URL pública segura (`https://*.trycloudflare.com`), permitindo que as notificações do navegador funcionem no Android/Chrome sem bloqueios de segurança do protocolo HTTP.

### Multi-idioma
* Interface disponível em **Português (Brasil)**, **English** e **Español**.
* A troca pode ser feita pelo terminal do PC pressionando a tecla `L`.

---

## Como Rodar

### Pré-requisitos
* **Windows 10 ou 11** com o Antigravity IDE em execução.
* **Python 3.10 ou superior** instalado e adicionado ao PATH.
* Celular conectado no mesmo Wi-Fi do computador (ou usando a URL HTTPS gerada).

### Instalação Rápida

1. Clone o repositório:
   ```bash
   git clone https://github.com/LumiaG5/antigravity-mobile.git
   cd antigravity-mobile
   ```

2. Inicie o servidor:
   * Dê dois cliques em `antrigavitymb/Start_Server.bat`; **OU**
   * Pelo terminal:
     ```bash
     cd antrigavitymb/desktop-bridge
     pip install -r requirements.txt
     python run.py
     ```

3. Conecte pelo celular:
   O terminal exibirá os endereços disponíveis:
   ```text
   ====================================================================
           [*] ANTIGRAVITY MOBILE - SERVIDOR DESKTOP BRIDGE
                    Desenvolvido por Dev LumiaG5
   ====================================================================
    * PC Local:              http://localhost:8765
    * Mobile (Wi-Fi):        http://192.168.0.X:8765
    * Mobile (HTTPS Seguro): https://seu-tunnel.trycloudflare.com
    * Idioma Ativo:          Português (Brasil)
   --------------------------------------------------------------------
    PIN DE ACESSO:           [ 4821 ]
   ====================================================================
   ```
   * Abra o link no navegador do celular (recomenda-se o HTTPS para ativar notificações).
   * Digite o PIN de 4 dígitos mostrado no terminal.
   * *(Opcional)* No menu do navegador do celular, selecione **"Adicionar à Tela Inicial"** para usar em tela cheia como PWA.

---

## Atalhos do Terminal

Com o servidor rodando no console do PC, você pode usar os seguintes atalhos:

| Tecla | Ação |
| :--- | :--- |
| **Qualquer tecla** | Gera um novo PIN aleatório para parear outro dispositivo |
| **`L`** | Alterna o idioma do sistema (Português / Inglês / Espanhol) |
| **`Ctrl + C`** | Encerra o servidor e fecha o túnel Cloudflare de forma limpa |

---

## Estrutura do Repositório

```
antrigavitymb/
├── desktop-bridge/            # Daemon em Python (FastAPI + WebSockets)
│   ├── run.py                 # Menu interativo do terminal e atalhos de teclado
│   ├── server.py              # Rotas REST e canal de streaming WebSocket
│   ├── monitor.py             # Parser de transcripts, locks de presença e banco SQLite
│   ├── auth.py                # Controle de PIN e sessões em cache (TTL 24h)
│   ├── language_manager.py    # Gerenciador de traduções (pt, en, es)
│   ├── tunnel.py              # Integração do túnel Cloudflare
│   ├── antigravity_api.py     # Cliente RPC para leitura das cotas do Antigravity
│   ├── config.py              # Detecção automática de caminhos no Windows
│   ├── bin/cloudflared.exe    # Binário do túnel seguro
│   └── static/
│       ├── index.html         # Frontend Web Companion (HTML5/CSS3/Vanilla JS)
│       └── antigravity-icon.png
├── mobile-app/                # Base em React Native / Expo (caso queira gerar APK)
├── Start_Server.bat           # Script de inicialização automática no Windows
└── COMO_CONECTAR.txt          # Instruções rápidas de rede e conexão
```

---

## Perguntas Frequentes

**Preciso compilar o APK para usar no celular?**  
Não. O Web Companion foi projetado para rodar direto pelo navegador (Chrome, Safari, Firefox, Edge, Opera, Samsung Internet) com suporte a som, vibração e notificações push, sem a burocracia de instalar APKs.

**Funciona no iPhone / iOS?**  
Sim. No Safari do iOS o dashboard funciona normalmente. Para receber notificações com a tela bloqueada no iOS, adicione a página à Tela de Início.

**O Antigravity precisa estar aberto no PC?**  
Sim. O daemon monitora os arquivos de trabalho e as APIs locais criadas pelo Antigravity durante a sua sessão de código.

**Como funciona a segurança do túnel HTTPS?**  
O túnel é gerado temporariamente pela rede da Cloudflare com criptografia ponta a ponta (TLS). Nenhuma porta do seu roteador precisa ser aberta manualmente, e o acesso só é liberado após a validação do PIN de 4 dígitos.

---

## Autor

Desenvolvido por **Dev LumiaG5**  
GitHub: [@LumiaG5](https://github.com/LumiaG5)

---

## Licença

Este projeto está sob a licença [MIT](LICENSE.txt). Consulte o arquivo `LICENSE.txt` para mais detalhes.
