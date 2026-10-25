# Changelog

<p align="center">
  <b>Português</b> &bull; <a href="CHANGELOG.en.md">English</a> &bull; <a href="changelog.es.md">Español</a>
</p>

Todas as alterações notáveis do **Antigravity Mobile** serão documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este projeto segue o [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
