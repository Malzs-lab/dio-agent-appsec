# 📚 Referência Técnica: Mapeamento MITRE ATT&CK, OWASP Top 10 e CWE

Este documento fornece a base de consulta técnica sobre os padrões internacionais referenciados pelo **DIO Agent**.

---

## 1. CWE-89: Injeção de SQL (SQL Injection)
* **Nome Formal:** *Improper Neutralization of Special Elements used in an SQL Command*
* **Descrição:** A aplicação recebe dados de entrada externos sem a devida neutralização ou parametrização e os insere diretamente na montagem de um comando SQL.
* **Mecanismo:** Permite que o invasor altere a lógica booleana da consulta, injete instruções subordinadas (`UNION`, `SELECT`), comente condições de segurança (`--`, `/*`) ou execute múltiplos comandos caso o driver permita (*Stacked Queries*).
* **Solução Primária:** Consultas Parametrizadas (*Prepared Statements*). O motor do banco compila a árvore sintática da instrução antes da passagem dos parâmetros.

---

## 2. OWASP Top 10:2021 — Categoria A03 (Injection)
* **Escopo:** Abrange falhas onde dados não confiáveis são enviados a um interpretador como parte de um comando ou consulta.
* **Tipos comuns:**
  - SQL Injection (SQLi)
  - Cross-Site Scripting (XSS - Injeção de scripts no navegador)
  - Command Injection (Injeção em comandos do sistema operacional)
  - LDAP / NoSQL Injection
* **Controles Recomendados pela OWASP:**
  1. Uso de APIs seguras que evitem o uso direto do interpretador ou forneçam interface parametrizada.
  2. Validação rigorosa de entrada baseada em lista permitida (*whitelisting*).
  3. Para qualquer consulta dinâmica residual, escapar caracteres especiais usando a API nativa do banco de dados.

---

## 3. MITRE ATT&CK: T1190 — Exploit Public-Facing Application
* **Tática:** *Initial Access (TA0001)*
* **ID da Técnica:** `T1190`
* **Definição:** Adversários tentam explorar fraquezas em programas, softwares ou serviços conectados à internet (ex: servidores web, APIs, bancos expostos, gateways de VPN) para obter acesso inicial à infraestrutura interna da vítima.
* **Exemplos no Mundo Real:**
  - Injeção de SQL para contornar telas de autenticação e obter hashes de administradores.
  - Exploração de bugs de estouro de buffer (*buffer overflow*) ou desserialização em servidores web Apache/Nginx.
* **Detecção:**
  - Monitoramento de logs de acesso web e application firewall (WAF) buscando requisições anômalas contendo caracteres `'`, `"`, `--`, `UNION`, `SELECT`.
  - Telemetria de banco de dados alertando sobre picos repentinos de consultas malformadas ou com sintaxe inválida (`sqlite3.OperationalError`).
