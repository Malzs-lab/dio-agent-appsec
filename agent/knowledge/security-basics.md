# 🛡️ Base de Conhecimento: Fundamentos de Segurança da Informação & AppSec

Este documento estabelece o alicerce conceitual e analítico para o agente em tarefas de análise de vulnerabilidades, auditoria defensiva e revisão segura de código e infraestrutura.

---

## 1. O Triângulo Fundamental: Vulnerabilidade, Ameaça e Risco

Em cibersegurança e engenharia defensiva, termos como "vulnerabilidade" e "ameaça" frequentemente são confundidos. O agente deve sempre distinguir com precisão:

```
+--------------------------------------------------------------------------+
|                                  RISCO                                   |
|                Risco = Probabilidade (Ameaça) × Impacto                  |
+--------------------------------------------------------------------------+
       ▲                                                    ▲
       │                                                    │
+--------------+                                     +--------------+
|   AMEAÇA     |                                     |VULNERABILIDADE|
| Agente /     |  ====== Explora através de =====>   | Fraqueza /   |
| Motivação /  |                                     | Falha no     |
| Capacidade   |                                     | Sistema      |
+--------------+                                     +--------------+
```

### 1.1 Vulnerabilidade (*Weakness / Flaw*)
* **Definição:** Uma fraqueza, falha ou brecha existente no design, na arquitetura, no código-fonte, na configuração de software/hardware ou nos processos organizacionais.
* **Exemplos práticos:**
  - Concatenação direta de strings não tratadas em consultas SQL (CWE-89).
  - Porta de SSH (22) aberta para a internet sem proteção contra força bruta ou com autenticação por senha fraca.
  - Software ou biblioteca com CVE conhecido e sem atualização de patches.
* **Características:** A vulnerabilidade existe independentemente de alguém estar tentando explorá-la no momento.

### 1.2 Ameaça (*Threat*)
* **Definição:** Qualquer circunstância, agente ou evento com o potencial de causar danos explorando uma vulnerabilidade.
* **Atores de Ameaça (*Threat Actors*):**
  - Hackers criminosos (buscando ganhos financeiros ou exfiltração de dados).
  - Bots automatizados e scanners de vulnerabilidades em massa (raspando a internet).
  - *Insiders* maliciosos ou desatentos (funcionários, terceirizados).
  - Desastres naturais ou falhas físicas de hardware.
* **Vetor de Ataque (*Attack Vector*):** O caminho ou método que o agente malicioso utiliza para entregar o payload ou alcançar o alvo (ex: requisição HTTP manipulada, phishing, túnel reverso).

### 1.3 Risco (*Risk*)
* **Definição:** A estimativa do dano potencial resultante da probabilidade de uma ameaça conseguir explorar com sucesso uma vulnerabilidade, multiplicado pelo impacto gerado para o negócio ou aplicação.
* **Fórmula Operacional:**
  $$\text{Risco} = \text{Probabilidade} \times \text{Impacto}$$
* **Níveis de Severidade de Risco:**
  - **Crítico (P1):** Vulnerabilidade com exploração trivial, remota, sem necessidade de autenticação, gerando perda total de controle ou vazamento massivo (ex: SQLi de bypass de login, RCE em serviço público).
  - **Alto (P2):** Exploração viável, comprometendo gravemente dados sensíveis ou escalando privilégios parciais.
  - **Médio (P3):** Requer condições específicas de acesso, ataque em cadeia ou afeta recursos não críticos.
  - **Baixo (P4):** Divulgação mínima de metadados (banner grabbing), sem impacto operacional direto imediato.

---

## 2. A Tríade CIA (Confidencialidade, Integridade, Disponibilidade)

A segurança da informação e a segurança de aplicações orbitam em torno de três pilares fundamentais. Qualquer avaliação de vulnerabilidade deve classificar explicitamente qual pilar está sob ameaça:

### 2.1 Confidencialidade (*Confidentiality*)
* **Objetivo:** Garantir que dados, credenciais e comunicações sejam acessíveis apenas por indivíduos, processos ou sistemas autorizados.
* **Violações típicas:**
  - Injeção de SQL permitindo extração não autorizada do banco (`UNION SELECT ...`).
  - Vazamento de senhas, chaves de API ou tokens de sessão em repositórios públicos ou logs de produção.
  - Falta de criptografia em trânsito (HTTP puro em vez de HTTPS/TLS).
* **Controles:** Criptografia forte (AES-GCM, TLS 1.3), hashing salgado (bcrypt, Argon2), RBAC (*Role-Based Access Control*).

### 2.2 Integridade (*Integrity*)
* **Objetivo:** Assegurar a precisão, confiabilidade e não-adulteração dos dados e instruções durante armazenamento, trânsito ou processamento.
* **Violações típicas:**
  - Injeção de SQL ou comandos modificando dados de tabelas (`UPDATE users SET role = 'admin'`).
  - Man-in-the-Middle (MitM) alterando requisições em trânsito.
  - Deserialização insegura de objetos serializados corrompendo o estado da aplicação.
* **Controles:** Hashes unidirecionais com verificação de assinatura (SHA-256), HMAC, Prepared Statements, controle de transações ACID.

### 2.3 Disponibilidade (*Availability*)
* **Objetivo:** Assegurar que serviços, sistemas e dados estejam continuamente acessíveis e utilizáveis por usuários autorizados quando necessário.
* **Violações típicas:**
  - Ataques de Negação de Serviço (DoS/DDoS) sobrecarregando sockets de rede ou pooling de conexões.
  - Consultas pesadas ou injeção de `SLEEP()` que travam threads de banco de dados.
  - Bloqueio acidental de contas legítimas por ausência de políticas refinadas de rate limiting.
* **Controles:** Balanceamento de carga, rate limiting, autoscaling, redundância geográfica, backups automatizados com teste periódico de restauração.

---

## 3. Frameworks e Padrões Globais de Segurança

### 3.1 OWASP Top 10 (Aplicações Web)
* **A01:2021 - Broken Access Control:** Falhas em restringir o que usuários autenticados comuns podem fazer ou ver (ex: IDOR, acesso a `/admin`).
* **A02:2021 - Cryptographic Failures:** Uso de algoritmos fracos (MD5, SHA1 sem salt), tráfego em texto claro, armazenamento de senhas puras.
* **A03:2021 - Injection:** Dados fornecidos pelo usuário são interpretados como comandos ou queries (SQL Injection, Command Injection, LDAP Injection).
* **A04:2021 - Insecure Design:** Falta de modelagem de ameaças e arquitetura segura concebida antes da escrita do código.
* **A05:2021 - Security Misconfiguration:** Configurações default mantidas, portas desnecessárias expostas, mensagens de erro com stack trace detalhado em produção.
* **A06:2021 - Vulnerable and Outdated Components:** Bibliotecas e dependências desatualizadas com vulnerabilidades conhecidas (CVEs).
* **A07:2021 - Identification and Authentication Failures:** Ausência de MFA, suscetibilidade a ataques de força bruta/spray de credenciais, gerenciamento frágil de sessões.
* **A08:2021 - Software and Data Integrity Failures:** Uso de plugins ou pipelines de CI/CD sem validação de hash e assinatura criptográfica.
* **A09:2021 - Security Logging and Monitoring Failures:** Falta de registro de eventos de segurança críticos ou incapacidade de detecção de brechas em tempo hábil.
* **A10:2021 - Server-Side Request Forgery (SSRF):** A aplicação web busca um recurso remoto sem validar a URL fornecida pelo usuário, permitindo acessar serviços internos da nuvem.

### 3.2 MITRE ATT&CK (Matriz Tática Corporativa)
O MITRE ATT&CK organiza comportamentos adversários em Táticas (o objetivo do atacante) e Técnicas (como o objetivo é alcançado):
* **T1190 - Exploit Public-Facing Application:** Exploração de vulnerabilidades em serviços expostos à internet (ex: SQL Injection, vulnerabilidade em servidor web Apache/Nginx).
* **T1110 - Brute Force:** Ataques de tentativa e erro contra mecanismos de autenticação (Portas 22 SSH, 3389 RDP, rotas `/login`).
* **T1078 - Valid Accounts:** O atacante utiliza credenciais obtidas ilegitimamente para transitar como usuário regular no ambiente.
* **T1059 - Command and Scripting Interpreter:** Uso de interpretadores nativos do SO (PowerShell, Bash, Python) para executar instruções arbitrárias.
* **T1046 - Network Service Discovery:** Varredura de portas e serviços ativos na rede (ex: scans com Nmap ou scanners customizados).
* **T1562 - Impair Defenses:** Desativação ou adulteração de ferramentas de segurança (ex: parar firewalls, apagar logs de eventos).

---

## 4. Princípios de Engenharia Defensiva (Secure by Design & DevSecOps)

Ao orientar desenvolvedores e administradores, o agente deve seguir rigorosamente as regras cardeais:

1. **Nunca Confie em Entradas do Usuário (*Zero Trust Input*):** Todo dado vindo de fora (parâmetros de URL, corpo JSON, headers HTTP, formulários) é potencialmente malicioso.
2. **Separação Rígida de Código e Dados:** O interpretador SQL nunca deve tratar dados do usuário como comandos de consulta. O uso de **Consultas Parametrizadas (*Prepared Statements*)** é obrigatório; sanitização por regex ou `replace()` artesanal é insuficiente e propensa a bypass.
3. **Princípio do Menor Privilégio (*Least Privilege*):** Aplicações web nunca devem conectar no banco como superusuário (`root` ou `sa`). Devem ter permissão restrita apenas às tabelas e comandos necessários (`SELECT`, `INSERT`, `UPDATE`), sem permissão de `DROP` ou leitura de metadados do sistema.
4. **Defesa em Profundidade (*Defense in Depth*):** Não dependa de uma única barreira. A proteção deve ocorrer em camadas:
   - Camada de Borda/Rede: Firewall (WAF, UFW, Security Groups).
   - Camada de Aplicação: Parametrização, validação de tipos, CSRF tokens, rate limit.
   - Camada de Dados: Hashing salgado (Argon2id / bcrypt), criptografia em repouso.
5. **Falha Segura (*Fail-Safe Defaults*):** Em caso de erro inesperado ou exceção não tratada, o sistema deve recusar o acesso (bloqueio seguro) em vez de liberar a passagem por padrão.
6. **Perguntar o Contexto Antes de Sugerir Remediações:**
   - Ambientes em produção têm tolerâncias e janelas de manutenção distintas de laboratórios.
   - Modificar regras de firewall ou reiniciar daemons pode derrubar acessos legítimos.
   - O agente deve primeiro qualificar arquitetura, versão do SO/banco e escopo operacional antes de fornecer comandos imperativos.
