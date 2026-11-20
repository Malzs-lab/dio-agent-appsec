# 🚀 Guia de Execução no Harness Hermes (Nous Hermes Agent)

Este guia reproduz o fluxo de trabalho demonstrado pela Expert Isadora durante as aulas da DIO, executando o agente diretamente no terminal integrado do VS Code através do harness open-source **Hermes**.

---

## 1. O Que É o Hermes?
O **Hermes** é um harness (orquestrador de execução de agentes de IA) que lê automaticamente arquivos de configuração no formato `AGENTS.md` e pastas de `skills/`, gerenciando o ciclo de raciocínio, ferramentas e memória do modelo sem necessidade de retreinar pesos de rede neural. O agente aprende exclusivamente através do contexto inserido nos arquivos Markdown!

---

## 2. Instalação e Preparação do Ambiente

### Passo 1: Pré-Requisitos
Certifique-se de possuir Python 3.10+ e `pip` instalados no seu sistema (seja Windows, Linux/WSL ou macOS).

### Passo 2: Instalação do Hermes CLI
No terminal do seu sistema operacional, instale o pacote oficial do Hermes CLI:
```bash
pip install hermes-agent
```
*(Ou conforme a versão indicada na documentação oficial do projeto)*

### Passo 3: Configuração da Chave de API
O Hermes necessita de acesso a um modelo de linguagem para inferência (como OpenRouter, OpenAI, Anthropic ou Google Gemini). Configure a variável de ambiente:
* **No PowerShell (Windows):**
  ```powershell
  $env:OPENAI_API_KEY="sua_chave_aqui"
  # ou para OpenRouter/Gemini:
  $env:OPENROUTER_API_KEY="sua_chave_aqui"
  ```
* **No Bash (Linux/macOS):**
  ```bash
  export OPENAI_API_KEY="sua_chave_aqui"
  ```

---

## 3. Ponto Crítico de Execução (O Cuidado Obrigatório)

> [!WARNING]
> **ATENÇÃO AO DIRETÓRIO DE EXECUÇÃO:**
> O Hermes descobre as skills e personas procurando o arquivo `AGENTS.md` **no diretório atual de trabalho (CWD)**. Se você abrir o terminal em outra pasta (ex: na raiz do seu usuário) e rodar o comando, ele não encontrará os seus arquivos de segurança!

### Como Rodar Corretamente:
1. Abra o **Visual Studio Code**.
2. Abra a pasta do projeto: `File -> Open Folder -> dio-agent-appsec`.
3. Abra o terminal integrado (`Ctrl + ~` ou `Terminal -> New Terminal`).
4. Verifique se o prompt do terminal indica que você está dentro da pasta do repositório:
   ```powershell
   # No Windows:
   pwd
   # Deve exibir: ...\CyberSecurityProjects\dio-agent-appsec
   ```
5. Inicie o harness do agente:
   ```bash
   hermes
   ```
   *(ou `hermes chat` / `hermes run` dependendo da versão do CLI)*

---

## 4. Testando a Especialização no Terminal
Assim que o prompt do Hermes abrir:
1. Cole o código vulnerável:
   > *"Sou desenvolvedor e montei este login em Python: `cursor.execute(f"SELECT * FROM users WHERE user='{user}' AND pass='{password}'")`. Avalie como especialista em AppSec."*
2. Observe o comportamento:
   - O agente **não dá o código pronto de imediato**.
   - Ele ativa a skill `vulnerability-analysis`.
   - Ele pergunta qual banco está sendo usado, se há validação prévia e qual o ambiente de deploy.
   - Ele gera a **Matriz de Risco (Impacto 5, Probabilidade 5, Severidade Crítica)**.
   - Ele cita **CWE-89**, **OWASP A03:2021** e **MITRE ATT&CK T1190**.
   - Ele ensina a corrigir com **Consultas Parametrizadas** e hash de senhas!
