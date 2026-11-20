# 🛡️ DIO Agent: Especialização em AppSec & Análise Defensiva de Vulnerabilidades

![Status](https://img.shields.io/badge/Status-Concluído%20%26%20Validado-brightgreen)
![Harness](https://img.shields.io/badge/Harness-Nous%20Hermes%20%7C%20Antigravity-blue)
![Padrão](https://img.shields.io/badge/Standard-AGENTS.md%20%7C%20Skills-orange)
![AppSec](https://img.shields.io/badge/Specialization-AppSec%20%26%20DevSecOps-red)
![Comunidade](https://img.shields.io/badge/Bootcamp-DIO%20Cybersecurity-purple)

Repositório de especialização do **DIO Agent** com foco em **Segurança de Aplicações (AppSec), Análise Defensiva de Vulnerabilidades e Engenharia de Prompt Baseada em Arquivos**, reproduzindo e expandindo o fluxo prático conduzido pela Expert Isadora na plataforma da **DIO (Digital Innovation One)**.

Nenhum modelo de IA foi retreinado ou teve pesos modificados: todo o aprendizado e calibração de raciocínio ocorrem via **In-Context Learning**, alimentado por instruções em arquivos Markdown estruturados (`AGENTS.md`, `agent/persona.md`, `agent/knowledge/` e `skills/`).

---

## 🎯 Por Que Esta Especialização Foi Criada?

Assistentes de IA tradicionais e genéricos costumam falhar gravemente em tarefas de segurança por dois motivos:
1. **Respostas cegas e imediatas:** Entregam scripts ou comandos destrutivos sem questionar o contexto do ambiente (o que pode travar portas de rede e derrubar servidores em produção).
2. **Correções superficiais:** Apenas colam uma correção sem ensinar o desenvolvedor a entender o impacto no negócio, o vetor de ataque do invasor e a necessidade de testes de regressão.

Esta especialização transforma o DIO Agent em um **Consultor e Mentor Sênior em AppSec**:
* **Contexto em Primeiro Lugar:** O agente **sempre pergunta** sobre o tipo de ambiente (lab vs. produção), biblioteca de banco, portas abertas e restrições antes de propor qualquer intervenção.
* **Matriz Padronizada de Risco:** Toda falha é quantificada com métricas de **Impacto (1-5)**, **Probabilidade (1-5)** e **Severidade Consolidada** (Crítica, Alta, Média, Baixa).
* **Mapeamento em Padrões Globais:** Conexão direta com **CWE**, **OWASP Top 10** e **MITRE ATT&CK**.
* **Defesa em Profundidade (*Secure by Design*):** Não aceita sanitizações paliativas; exige consultas parametrizadas (*Prepared Statements*), hashing moderno com salt único (PBKDF2/bcrypt) e linters de SAST.

---

## 🏗️ Arquitetura do Repositório e Arquivos do Projeto

```text
dio-agent-appsec/
├── README.md                           # Documentação principal para humanos (avaliação e portfólio)
├── AGENTS.md                           # Fonte única de verdade lida automaticamente pelos harnesses
├── CLAUDE.md                           # Atalhos e diretrizes específicas para o Claude Code
├── HERMES.md                           # Guia passo a passo de execução no Nous Hermes Agent
│
├── agent/                              
│   ├── persona.md                      # Persona do mentor: empático, socrático e rigoroso em AppSec
│   └── knowledge/                      # Bases de conhecimento técnicas estáticas
│       ├── security-basics.md          # Vulnerabilidade vs Ameaça vs Risco, Tríade CIA, OWASP e MITRE
│       └── dio.md                      # Cultura pedagógica e histórico da DIO
│
├── skills/                             # Habilidades modulares acionadas por demanda (Progressive Disclosure)
│   ├── vulnerability-analysis/         # ⭐ SKILL PRINCIPAL: Análise defensiva e triagem de vulnerabilidades
│   │   ├── SKILL.md                    # Roteiro formal em 6 fases com YAML frontmatter
│   │   └── README.md                   # Explicação da skill para desenvolvedores
│   │
│   ├── security-test-guide/            # 🚀 MELHORIA DE EVOLUÇÃO: Criação de testes automatizados e SAST
│   │   ├── SKILL.md                    # Roteiro para testes unitários com injeção e linters
│   │   └── README.md                   # Explicação para humanos
│   │
│   ├── study-plan/                     # Skill nativa da DIO para cronogramas de estudo
│   ├── unblock-challenge/              # Skill nativa para destravar desafios de código
│   ├── explain-concept/                # Skill nativa para didática com analogias
│   └── portfolio-review/               # Skill nativa para avaliação de projetos no GitHub
│
├── lab-security/                       # Ambiente prático de testes e laboratório isolado
│   ├── app_vulneravel.py               # Script em Python com login vulnerável a SQL Injection (CWE-89)
│   ├── app_seguro.py                   # Script refatorado com consultas parametrizadas e PBKDF2
│   ├── test_sql_injection.py           # Suite automatizada de testes comprovando mitigação
│   └── cenario_ubuntu_lab.md           # Simulação da defesa de servidor exposto à internet
│
└── docs/                               # Evidências e materiais de apoio
    ├── demonstracao_comparativa.md     # Transcrição: IA Genérica vs. DIO Agent Especializado
    └── guia_mitre_owasp.md             # Tabela técnica detalhada de CWE, OWASP e MITRE ATT&CK
```

---

## ⚡ Como Rodar o Agente no Harness (Hermes / VS Code)

O agente foi desenhado para rodar em harnesses modernos compatíveis com o padrão aberto `AGENTS.md`. Abaixo está o fluxo com o **Hermes**, como ensinado pela Expert Isadora:

### 1. Instalação do Hermes CLI
```bash
pip install hermes-agent
```

### 2. Configurar a Chave de API
* **No Windows (PowerShell):**
  ```powershell
  $env:OPENAI_API_KEY="sua_chave_aqui"
  # ou OpenRouter:
  $env:OPENROUTER_API_KEY="sua_chave_aqui"
  ```
* **No Linux / macOS (Bash):**
  ```bash
  export OPENAI_API_KEY="sua_chave_aqui"
  ```

### 3. Ponto Crítico de Execução
> [!WARNING]
> Abra o terminal **obrigatoriamente na pasta raiz do projeto** (`dio-agent-appsec`). Se você executar o comando em outro diretório, o harness não encontrará os arquivos de skills e persona!

```bash
cd dio-agent-appsec
hermes
```

---

## 🔬 Laboratório Prático: Código Vulnerável e Validação de Mitigação

### 1. Código Vulnerável (`lab-security/app_vulneravel.py`)
Implementa uma tela de login onde o SQL é concatenado via f-string:
```python
# ❌ VULNERABILIDADE CRÍTICA (CWE-89): Concatenação de entrada externa
query_insegura = f"SELECT id, username, role FROM users WHERE username = '{usuario_input}' AND password = '{senha_input}'"
cursor.execute(query_insegura)
```
* **Vetor de Ataque:** O payload `' OR '1'='1` ou `admin' --` altera a lógica booleana da consulta, garantindo acesso completo sem senha.

### 2. Código Corrigido e Protegido (`lab-security/app_seguro.py`)
Implementa as recomendações da skill `vulnerability-analysis`:
```python
# ✅ PROTEÇÃO COMPROVADA: Consulta Parametrizada (Prepared Statement)
query_parametrizada = "SELECT id, username, password_hash, salt, role FROM users WHERE username = ?"
cursor.execute(query_parametrizada, (usuario_input,))
```
* **Medidas Adicionais:**
  - Hashing salgado de senhas com `hashlib.pbkdf2_hmac('sha256', ...)`.
  - Validação estrita de formato de usuário via regex (`^[a-zA-Z0-9_]{3,30}$`).
  - Comparação de senha em tempo constante (`hmac.compare_digest`) imune a timing attacks.

### 3. Execução dos Testes Automatizados (`lab-security/test_sql_injection.py`)
Para rodar a bateria de testes que comprova a falha no código antigo e o bloqueio no código novo:
```bash
cd lab-security
python test_sql_injection.py
```
**Resultado Esperado dos Testes:**
```text
test_vuln_falha_de_seguranca_bypass_tautologia ... OK (Permitiu o bypass no inseguro)
test_sec_bloqueio_efetivo_tautologia ... OK (Bloqueou com sucesso no seguro)
test_sec_bloqueio_efetivo_bypass_admin ... OK (Bloqueou sequestro de admin)
Ran 6 tests in 0.052s - OK
```

---

## 📸 Evidências de Interação com o Agente (Prints / Transcrições)

### Teste 1: Análise do `app.py` Vulnerável
```text
[USUÁRIO]:
"Sou desenvolvedor júnior e criei este login:
query = f"SELECT * FROM users WHERE user = '{usuario}' AND pass = '{senha}'"
Avalie se há problemas de segurança."

[DIO AGENT]:
"Olá! Analisando seu trecho de código, identifiquei uma vulnerabilidade de severidade CRÍTICA.
Antes de propor a refatoração, me responda:
1. Qual biblioteca de banco você utiliza (sqlite3, psycopg2, MySQL)?
2. As senhas no seu banco já usam hash ou ainda estão em texto simples?

--- DIAGNÓSTICO DE RISCO ---
* Impacto: 5/5 (Acesso total administrativo e vazamento de base)
* Probabilidade: 5/5 (Trivialmente explorável via internet)
* Severidade: 🔴 CRÍTICA (Score 25)
* Mapeamento: CWE-89 | OWASP A03:2021 (Injection) | MITRE ATT&CK T1190
* Tríade CIA: Viola Confidencialidade e Integridade

--- MECANISMO DE EXPLORAÇÃO ---
Se alguém digitar no campo de usuário: admin' --
O comando executado vira:
SELECT * FROM users WHERE user = 'admin' --' AND pass = '...'
Os dois traços ignoram a checagem da senha!

Aguarde para implementarmos Consultas Parametrizadas e hashing PBKDF2!"
```

### Teste 2: Cenário do Servidor Ubuntu Exposto
```text
[USUÁRIO]:
"Tenho um servidor Ubuntu 22.04 exposto na internet. O que devo rodar para deixá-lo seguro?"

[DIO AGENT]:
"Olá! Antes de colar qualquer regra de firewall ou comando de terminal, precisamos ter cautela extrema: aplicar comandos cegos de rede pode derrubar seu próprio acesso SSH (lockout)!

Por favor, me responda 4 perguntas sobre o seu ambiente:
1. Quais serviços precisam ficar abertos para a internet (ex: só SSH na 22, porta 80/443 web)?
2. A sua autenticação SSH é feita por senha simples ou por chave pública (ed25519)?
3. Você acessa de um IP fixo conhecido ou de qualquer lugar?
4. Você tem acesso ao console web da sua VPS/nuvem caso a rede caia?"
```

---

## 🌟 Melhorias de Evolução Implementadas

Como proposto no desafio, além da base original da Expert Isadora, incorporamos:
1. **Skill de Testes Automatizados (`security-test-guide`):** Roteiro formal para guiar desenvolvedores na criação de suites unitárias negativas de injeção e integração de linters SAST (`bandit`, `pip-audit`).
2. **Matriz Quantitativa Padronizada:** Todo diagnóstico emite o cálculo numérico de $\text{Risco} = \text{Impacto} \times \text{Probabilidade}$, permitindo comparar múltiplos incidentes no backlog de segurança.
3. **Mapeamento MITRE ATT&CK & OWASP:** Cada vulnerabilidade identificada recebe classificação formal de tática e técnica adversária.
4. **Laboratório Executável Real:** Arquivos `app_vulneravel.py`, `app_seguro.py` e `test_sql_injection.py` 100% funcionais com SQLite em memória.

---

## ✅ Checklist de Submissão

- [x] Skill nova `vulnerability-analysis` com `SKILL.md` contendo `name` e `description` válidos.
- [x] Skill nova documentada em `README.md` explicativo para humanos.
- [x] Skill listada e mapeada na tabela central do `AGENTS.md`.
- [x] Base de conhecimento `agent/knowledge/security-basics.md` abordando vulnerabilidade, ameaça, risco e Tríade CIA.
- [x] Persona atualizada em `agent/persona.md` instruindo a postura inquisitiva e socrática.
- [x] Testes e cenários executados exclusivamente em ambiente isolado de laboratório.
- [x] Todas as pastas e arquivos citados na documentação existem e possuem conteúdo detalhado.
- [x] Repositório público no GitHub com nome padronizado em minúsculas e sem acentos: `dio-agent-appsec`.

---

## 👨‍💻 Autor & Agradecimentos
* **Autor:** MALZS
* **Bootcamp:** Cibersegurança & AI Agent Builders — Digital Innovation One (DIO)
* **Mentoria:** Expert Isadora Ferrão
* **Licença:** MIT
