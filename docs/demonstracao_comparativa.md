# 📊 Demonstração Comparativa: Chatbot Genérico vs. DIO Agent (AppSec Edition)

Uma das maiores contribuições destacadas pela Expert Isadora durante as aulas da DIO é demonstrar como um modelo de IA genérico responde superficialmente, enquanto um agente guiado por **persona**, **conhecimento estruturado** e **skills operacionais** conduz uma análise de segurança com profundidade de nível corporativo.

---

## 1. Cenário de Teste: Consulta SQL Insegura

O usuário envia a seguinte solicitação:
> *"Fiz este código para o login da minha API:  
> `query = f"SELECT * FROM users WHERE user = '{usuario}' AND pass = '{senha}'"`  
> O que você acha?"*

---

### Caso A: Assistente de IA Genérico (Sem Contexto / Sem Persona)
* **Comportamento Observado:**
  - Responde de forma imediata e simplória: *"Seu código tem SQL Injection. Troque por `execute("SELECT ...", (usuario, senha))`"*.
  - Não avalia impacto no negócio.
  - Não faz perguntas sobre o banco utilizado ou sobre a arquitetura.
  - Não alerta sobre o fato de estar armazenando senhas em texto puro no banco de dados.
  - Não fornece referências internacionais (CWE, OWASP, MITRE ATT&CK).
  - O desenvolvedor copia a linha sugerida sem entender o vetor de exploração e sem implementar defesa em profundidade.

---

### Caso B: DIO Agent Especializado (Com `vulnerability-analysis`)
* **Comportamento Observado:**

> **DIO Agent:**  
> *"Olá! Analisando o trecho compartilhado, identifiquei um ponto de atenção crítico de segurança de aplicações (AppSec).  
>  
> Antes de propor qualquer refatoração no seu código, preciso entender dois pontos do seu ambiente:  
> 1. Qual biblioteca ou driver de banco você está utilizando? (ex: `sqlite3`, `psycopg2` para PostgreSQL, `mysql-connector` ou um ORM como SQLAlchemy)?  
> 2. Como as senhas estão salvas na sua tabela `users`? (Em texto puro ou com hash como bcrypt/Argon2)?  
>  
> Enquanto você me confirma isso, veja o diagnóstico inicial de risco da sua implementação atual:  
>  
> ### 🛡️ Matriz de Avaliação de Risco  
> * **Impacto (1-5):** **5 (Crítico)** — Permite que um atacante ignore completamente a checagem de senha, faça login como administrador e leia ou apague registros de todo o banco.  
> * **Probabilidade (1-5):** **5 (Quase Certa)** — O vetor é trivialmente explorável pela internet pública com payloads comuns como `' OR '1'='1`.  
> * **Severidade Consolidada:** 🔴 **CRÍTICA (Score 25)**  
> * **Tríade CIA Afetada:** Confidencialidade (leitura não autorizada), Integridade (adulteração de registros) e Disponibilidade (risco de truncamento de tabelas).  
>  
> ### 🌐 Mapeamento em Padrões Globais  
> * **CWE:** `CWE-89: Improper Neutralization of Special Elements used in an SQL Command`  
> * **OWASP Top 10:** `A03:2021 - Injection`  
> * **MITRE ATT&CK:** `T1190 - Exploit Public-Facing Application`  
>  
> ### 🔍 Como o Atacante Pensa (Exploração Lógica)  
> Ao concatenar com f-string, o interpretador SQL não sabe onde termina o comando e onde começam os seus dados. Se o atacante digitar no campo de usuário:  
> `admin' --`  
> A query montada será:  
> `SELECT * FROM users WHERE user = 'admin' --' AND pass = '...'`  
> Os dois traços (`--`) transformam toda a checagem de senha em um mero comentário. O banco executa a busca apenas pelo usuário `admin` e retorna o registro logado com sucesso!  
>  
> ### 🛠️ Próximo Passo Defensivo  
> A correção definitiva exige **Consultas Parametrizadas (*Prepared Statements*)**, onde o banco compila a sintaxe antes de receber os valores, impedindo que dados se transformem em comandos. Me confirme sua biblioteca de banco para estruturarmos a refatoração e adicionarmos o hashing de senhas!"*

---

## 2. Comparativo de Atributos

| Critério de Avaliação | IA Genérica Tradicional | DIO Agent Especializado |
| :--- | :---: | :---: |
| **Pausa para Qualificar Contexto** | ❌ Não (responde cego) | ✅ **Sim (obrigatoriamente)** |
| **Métrica Quantitativa de Risco (1 a 5)** | ❌ Inexistente | ✅ **Impacto, Probabilidade e Score** |
| **Classificação de Severidade** | ❌ Apenas "é perigoso" | ✅ **Matriz Crítica / Alta / Média / Baixa** |
| **Violação da Tríade CIA** | ❌ Não cita | ✅ **Confidencialidade, Integridade e Disponibilidade** |
| **Mapeamento MITRE ATT&CK** | ❌ Raro / Omitido | ✅ **Técnica T1190 formalizada** |
| **Mapeamento OWASP & CWE** | ❌ Genérico | ✅ **CWE-89 e OWASP A03:2021** |
| **Defesa em Profundidade (Hashing + Validação)** | ❌ Frequentemente ignora | ✅ **Abordagem integral de segurança** |
| **Estímulo Pedagógico Socrático** | ❌ Dá resposta pronta | ✅ **Ensina a raciocinar como AppSec** |
